#!/usr/bin/env python3
"""
single_prompt.py -- Dokumentation je Quelldatei in einem einzelnen LLM-Aufruf,
ohne CodeWikis Agentenschleife.

Warum: Die Messungen an CodeWiki zeigen keine Spur der Quelltext-Kommentare in
der generierten Dokumentation. Offen ist, ob das am Modell liegt oder an der
Pipeline (Untermodul-Zerlegung, Werkzeugaufrufe, Retries, Zusammenfassungen
ueber mehrere Ebenen). Dieses Skript verwendet denselben Prompt wie CodeWiki,
aber genau einen Aufruf pro Datei: Prompt rein, Markdown raus.

  # Verfuegbarkeit und Determinismus pruefen
  python3 single_prompt.py --check --backend ollama --model qwen3-coder:30b

  # Durchlauf ueber beide Bedingungen
  python3 single_prompt.py \\
      --withcom work/umoria/withcom --nocom work/umoria/nocom \\
      --files rng.cpp dungeon_los.cpp player_traps.cpp \\
      --out runs/umoria/single-prompt-01 \\
      --backend ollama --model qwen3-coder:30b --repeats 1

Ausgabe: <out>/withcom/*.md, <out>/nocom/*.md und <out>/meta.json.
Die vorhandenen Auswertungsskripte laufen unveraendert darauf:

  ngram_overlap.py    --docs <out>/withcom --null-docs <out>/nocom --corpus ...
  semantic_overlap.py --docs <out>/withcom --null-docs <out>/nocom --corpus ...
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import requests

# --------------------------------------------------------------- Backends

BACKENDS = {
    "ollama": {
        # Ollamas OpenAI-kompatibler /v1-Endpunkt reicht seed/temperature
        # nicht zuverlaessig durch; ueber die native API ist die Ausgabe bei
        # temperature 0 und festem seed reproduzierbar.
        "base_url": os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
        "api_key_env": None,
        "native": True,
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key_env": "OPENROUTER_API_KEY",
        "native": False,
    },
}

# --------------------------------------------------------------- Prompts
#
# Uebernommen aus codewiki/src/be/prompt_template.py (LEAF_SYSTEM_PROMPT und
# USER_PROMPT). Geaendert ist nur der Teil, der die Agenten-Werkzeuge
# beschreibt: statt die Datei mit `str_replace_editor` zu schreiben, gibt das
# Modell das Markdown direkt zurueck. Alles andere ist wortgleich, damit der
# Vergleich zu CodeWiki-Laeufen traegt.

SYSTEM_PROMPT = """
<ROLE>
You are an AI documentation assistant. Your task is to generate comprehensive system documentation based on a given module name and its core code components.
</ROLE>

<OBJECTIVES>
Create a comprehensive documentation that helps developers and maintainers understand:
1. The module's purpose and core functionality
2. Architecture and component relationships
3. How the module fits into the overall system
</OBJECTIVES>

<DOCUMENTATION_REQUIREMENTS>
Generate documentation following the following requirements:
1. Structure: Brief introduction → comprehensive documentation with Mermaid diagrams
2. Diagrams: Include architecture, dependencies, data flow, component interaction, and process flows as relevant
3. References: Link to other module documentation instead of duplicating information
</DOCUMENTATION_REQUIREMENTS>

<WORKFLOW>
1. Analyze provided code components and module structure
2. Generate the complete {module_name}.md documentation
</WORKFLOW>

<OUTPUT>
Return the documentation as Markdown. Output nothing but the Markdown itself:
no preamble, no explanation, no surrounding code fence.
</OUTPUT>
""".strip()

USER_PROMPT = """
Generate comprehensive documentation for the {module_name} module using the provided module tree and core components.

<MODULE_TREE>
{module_tree}
</MODULE_TREE>
* NOTE: You can refer the other modules in the module tree based on the dependencies between their core components to make the documentation more structured and avoid repeating the same information. Know that all documentation files are saved in the same folder not structured as module tree. e.g. [alt text]([ref_module_name].md)

<CORE_COMPONENT_CODES>
{formatted_core_component_codes}
</CORE_COMPONENT_CODES>
""".strip()

EXTENSION_TO_LANGUAGE = {
    ".c": "c", ".h": "c", ".cpp": "cpp", ".hpp": "cpp", ".cc": "cpp",
    ".cxx": "cpp", ".java": "java", ".py": "python", ".js": "javascript",
    ".ts": "typescript", ".cs": "csharp", ".go": "go", ".rb": "ruby",
}

# Fester Platzhalter. Entscheidend ist nur, dass er in BEIDEN Bedingungen
# identisch ist -- sonst vergleicht man Kontexte statt Kommentare.
DEFAULT_MODULE_TREE = "{module_name}\n  {file_name}"


def build_user_prompt(module_name, rel_path, file_text, module_tree):
    suffix = Path(rel_path).suffix
    lang = EXTENSION_TO_LANGUAGE.get(suffix, "")
    codes = (
        f"# File: {rel_path}\n\n"
        f"## Core Components in this file:\n"
        f"- {rel_path}\n\n"
        f"## File Content:\n```{lang}\n{file_text}```\n\n"
    )
    return USER_PROMPT.format(
        module_name=module_name,
        module_tree=module_tree,
        formatted_core_component_codes=codes,
    )


# --------------------------------------------------------------- LLM-Aufruf

def call_llm(backend, model, system, user, temperature, seed, max_tokens,
             timeout=600):
    cfg = BACKENDS[backend]
    headers = {"Content-Type": "application/json"}
    if cfg["api_key_env"]:
        key = os.environ.get(cfg["api_key_env"])
        if not key:
            sys.exit(f"Umgebungsvariable {cfg['api_key_env']} ist nicht gesetzt")
        headers["Authorization"] = f"Bearer {key}"

    messages = [{"role": "system", "content": system},
                {"role": "user", "content": user}]

    if cfg["native"]:
        url = f"{cfg['base_url']}/api/chat"
        options = {"temperature": temperature, "num_predict": max_tokens}
        if seed is not None:
            options["seed"] = seed
        payload = {"model": model, "messages": messages,
                   "stream": False, "options": options}
    else:
        url = f"{cfg['base_url']}/chat/completions"
        payload = {"model": model, "messages": messages,
                   "temperature": temperature, "max_tokens": max_tokens}
        if seed is not None:
            payload["seed"] = seed

    started = time.time()
    resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()

    if cfg["native"]:
        text = data["message"]["content"]
        prompt_tokens = data.get("prompt_eval_count")
        completion_tokens = data.get("eval_count")
        finish = data.get("done_reason", "stop")
    else:
        choice = data["choices"][0]
        text = choice["message"]["content"]
        usage = data.get("usage") or {}
        prompt_tokens = usage.get("prompt_tokens")
        completion_tokens = usage.get("completion_tokens")
        finish = choice.get("finish_reason")

    return {
        "text": strip_fence(text),
        "duration_s": round(time.time() - started, 1),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "finish_reason": finish,
    }


FENCE_RE = re.compile(r"^\s*```(?:markdown|md)?\s*\n(.*)\n```\s*$", re.S)


def strip_fence(text):
    """Manche Modelle umschliessen die Antwort trotz Anweisung mit ```."""
    m = FENCE_RE.match(text.strip())
    return m.group(1) if m else text.strip()


# --------------------------------------------------------------- Ablauf

def module_name_for(rel_path):
    """
    Modulname aus dem Dateipfad.

    Die Endung bleibt Teil des Namens, sonst ueberschreiben sich Header und
    Implementierung gegenseitig: rng.cpp und rng.h ergaeben beide "rng".
    Aus rng.cpp wird also rng_cpp, aus rng.h wird rng_h.
    """
    p = Path(rel_path)
    return f"{p.stem}_{p.suffix.lstrip('.')}" if p.suffix else p.stem


def resolve_files(withcom_dir, nocom_dir, wanted):
    """Dateien, die in beiden Bedingungen vorliegen."""
    a = {str(p.relative_to(withcom_dir)): p
         for p in Path(withcom_dir).rglob("*") if p.is_file()}
    b = {str(p.relative_to(nocom_dir)): p
         for p in Path(nocom_dir).rglob("*") if p.is_file()}
    common = sorted(set(a) & set(b))
    if wanted:
        sel = []
        for w in wanted:
            hits = [c for c in common if c == w or Path(c).name == w]
            if not hits:
                sys.exit(f"Nicht in beiden Bedingungen gefunden: {w}")
            sel.extend(hits)
        common = sel
    return [(rel, a[rel], b[rel]) for rel in common]


def cmd_check(args):
    """Erreichbarkeit und Determinismus pruefen."""
    print(f"Backend: {args.backend}  Modell: {args.model}")
    probe = ("Reply with exactly the word: ready", "You are a test fixture.")
    try:
        first = call_llm(args.backend, args.model, probe[1], probe[0],
                         args.temperature, args.seed, 64)
    except Exception as e:
        sys.exit(f"Aufruf fehlgeschlagen: {e}")
    print(f"  Antwort: {first['text'][:60]!r}  ({first['duration_s']}s)")

    print("\nDeterminismus-Probe: identischer Prompt, zweimal")
    sample = ("Describe what a random number generator does, in two sentences.",
              SYSTEM_PROMPT.format(module_name="probe"))
    runs = [call_llm(args.backend, args.model, sample[1], sample[0],
                     args.temperature, args.seed, 256) for _ in range(2)]
    same = runs[0]["text"] == runs[1]["text"]
    print(f"  Ausgaben identisch: {'ja' if same else 'NEIN'}")
    if not same:
        print("  -> Wiederholungen noetig (--repeats > 1), Varianz wie gehabt.")
    else:
        print("  -> deterministisch; --repeats 1 genuegt.")
    return 0


def cmd_run(args):
    out = Path(args.out)
    if out.exists() and any(out.iterdir()):
        sys.exit(f"Ausgabeverzeichnis nicht leer: {out}")

    files = resolve_files(args.withcom, args.nocom, args.files)
    if not files:
        sys.exit("Keine gemeinsamen Dateien in beiden Bedingungen")

    print(f"{len(files)} Datei(en) x 2 Bedingungen x {args.repeats} "
          f"Wiederholung(en) = {len(files) * 2 * args.repeats} Aufrufe")
    print(f"Backend {args.backend}, Modell {args.model}, "
          f"temperature {args.temperature}, seed {args.seed}\n")

    records, failures = [], 0
    for rep in range(1, args.repeats + 1):
        for rel, path_with, path_no in files:
            module = module_name_for(rel)
            tree = args.module_tree or DEFAULT_MODULE_TREE.format(
                module_name=module, file_name=rel)

            for cond, src in (("withcom", path_with), ("nocom", path_no)):
                tag = f"{module}" if args.repeats == 1 else f"{module}_r{rep}"
                target = out / cond / f"{tag}.md"
                target.parent.mkdir(parents=True, exist_ok=True)

                text = src.read_text(encoding="utf-8", errors="replace")
                user = build_user_prompt(module, rel, text, tree)
                system = SYSTEM_PROMPT.format(module_name=module)

                label = f"  [{rep}/{args.repeats}] {cond:8} {rel}"
                try:
                    res = call_llm(args.backend, args.model, system, user,
                                   args.temperature, args.seed, args.max_tokens)
                except Exception as e:
                    print(f"{label}  FEHLER: {e}")
                    failures += 1
                    continue

                target.write_text(res["text"] + "\n", encoding="utf-8")
                words = len(res["text"].split())
                print(f"{label}  {words:5d} Woerter  {res['duration_s']:6.1f}s"
                      + ("  ABGESCHNITTEN"
                         if res["finish_reason"] in ("length", "limit")
                         else ""))

                records.append({
                    "repeat": rep, "condition": cond, "file": rel,
                    "module": module, "output": str(target.relative_to(out)),
                    "words": words, "input_chars": len(text),
                    **{k: res[k] for k in
                       ("duration_s", "prompt_tokens", "completion_tokens",
                        "finish_reason")},
                })

    meta = {
        "backend": args.backend,
        "model": args.model,
        "temperature": args.temperature,
        "seed": args.seed,
        "max_tokens": args.max_tokens,
        "repeats": args.repeats,
        "withcom_dir": str(args.withcom),
        "nocom_dir": str(args.nocom),
        "module_tree": args.module_tree or "(default placeholder)",
        "failures": failures,
        "runs": records,
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False),
                                   encoding="utf-8")

    print(f"\nFertig. {len(records)} Ausgaben, {failures} Fehler.")
    for cond in ("withcom", "nocom"):
        w = sum(r["words"] for r in records if r["condition"] == cond)
        n = sum(1 for r in records if r["condition"] == cond)
        print(f"  {cond:8} {n:3d} Dateien, {w:6d} Woerter")
    print(f"\nAuswertung:\n"
          f"  python3 scripts/ngram_overlap.py --docs {out}/withcom \\\n"
          f"      --null-docs {out}/nocom --corpus <korpus.jsonl>")
    return 0 if failures == 0 else 1


def cmd_probe(args):
    """
    Nullkontext-Probe: dieselbe Frage ohne jeden Quelltext.

    Prueft, ob das Modell das Projekt aus den Trainingsdaten kennt. Vage
    Antworten ("ein Schachprogramm mit Zuggenerierung") beweisen nichts --
    entscheidend sind ueberpruefbare Details wie Klassen-, Datei- oder
    Formatnamen. Genau die gibt man ueber --probe-terms an.

    Temperatur bewusst > 0 und wechselnde Seeds: einmal richtig geraten ist
    Zufall, fuenfmal derselbe korrekte Name ist Erinnerung.
    """
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    terms = [t.strip() for t in (args.probe_terms or "").split(",") if t.strip()]
    system = ("You are a knowledgeable software engineer. Answer from what you "
              "already know. If you do not know the project, say so plainly "
              "instead of guessing.")

    print(f"Frage:   {args.probe}")
    print(f"Backend: {args.backend}, Modell: {args.model}, "
          f"temperature {args.temperature}, {args.repeats} Durchlaeufe")
    if terms:
        print(f"Gesucht: {', '.join(terms)}")
    print()

    hits = {t: 0 for t in terms}
    texts = []
    for rep in range(1, args.repeats + 1):
        seed = None if args.seed is None else args.seed + rep
        try:
            res = call_llm(args.backend, args.model, system, args.probe,
                           args.temperature, seed, args.max_tokens)
        except Exception as e:
            print(f"  [{rep}] FEHLER: {e}")
            continue
        text = res["text"]
        texts.append(text)
        (out / f"probe_{rep:02d}.md").write_text(text + "\n", encoding="utf-8")

        found = [t for t in terms if t.lower() in text.lower()]
        for t in found:
            hits[t] += 1
        print(f"  [{rep}] {len(text.split()):4d} Woerter, {res['duration_s']:5.1f}s"
              + (f"  Treffer: {', '.join(found)}" if found else
                 ("  keine Treffer" if terms else "")))

    if terms:
        print(f"\n  {'Begriff':32} Treffer")
        print("  " + "-" * 42)
        for t in terms:
            bar = "#" * hits[t]
            print(f"  {t:32} {hits[t]}/{len(texts)}  {bar}")
        total = sum(1 for t in terms if hits[t] > 0)
        print(f"\n  {total} von {len(terms)} Begriffen mindestens einmal genannt.")
        if total == 0:
            print("  -> kein Hinweis auf Vorwissen ueber dieses Projekt.")
        elif total == len(terms):
            print("  -> das Modell kennt das Projekt. Befunde entsprechend "
                  "einschraenken.")
        else:
            print("  -> teilweises Vorwissen; die genannten Begriffe von Hand "
                  "pruefen.")

    (out / "probe_meta.json").write_text(json.dumps({
        "question": args.probe, "backend": args.backend, "model": args.model,
        "temperature": args.temperature, "base_seed": args.seed,
        "repeats": args.repeats, "terms": terms, "hits": hits,
        "answers": len(texts),
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nAntworten: {out}/probe_*.md")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--backend", choices=sorted(BACKENDS), default="ollama")
    ap.add_argument("--model", required=True,
                    help="z.B. qwen3-coder:30b oder qwen/qwen3-coder-flash")
    ap.add_argument("--withcom", help="Quellverzeichnis mit Kommentaren")
    ap.add_argument("--nocom", help="Quellverzeichnis ohne Kommentare")
    ap.add_argument("--files", nargs="*",
                    help="Dateinamen; ohne Angabe alle gemeinsamen")
    ap.add_argument("--out", help="Ausgabeverzeichnis")
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--seed", type=int, default=42,
                    help="fuer Reproduzierbarkeit; --seed -1 laesst ihn weg")
    ap.add_argument("--max-tokens", type=int, default=8192)
    ap.add_argument("--module-tree",
                    help="fester Modulbaum-Text fuer BEIDE Bedingungen")
    ap.add_argument("--check", action="store_true",
                    help="nur Erreichbarkeit und Determinismus pruefen")
    ap.add_argument("--probe", metavar="FRAGE",
                    help="Nullkontext-Probe: diese Frage ohne jeden Quelltext "
                         "stellen, z.B. \"Describe the architecture of the "
                         "DokChess chess engine.\"")
    ap.add_argument("--probe-terms", metavar="LISTE",
                    help="kommagetrennte Begriffe, auf die geprueft wird, "
                         "z.B. ChessRules,MinimaxParallelSearch,Polyglot")
    args = ap.parse_args()

    if args.seed == -1:
        args.seed = None
    if args.check:
        sys.exit(cmd_check(args))
    if args.probe:
        if not args.out:
            sys.exit("Fehlendes Argument: --out")
        if args.temperature == 0.0:
            print("Hinweis: --temperature 0 macht alle Durchlaeufe gleich; "
                  "fuer die Probe ist 0.7 sinnvoller.\n", file=sys.stderr)
        sys.exit(cmd_probe(args))
    missing = [n for n in ("withcom", "nocom", "out") if not getattr(args, n)]
    if missing:
        sys.exit("Fehlende Argumente: " + ", ".join("--" + m for m in missing))
    sys.exit(cmd_run(args))


if __name__ == "__main__":
    main()
