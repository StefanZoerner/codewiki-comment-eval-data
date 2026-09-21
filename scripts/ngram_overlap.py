#!/usr/bin/env python3
"""
ngram_overlap.py -- Wieviel der generierten Dokumentation stammt woertlich
aus den Quelltext-Kommentaren?

Misst n-Gramm-Ueberlappung zwischen generierter Markdown-Dokumentation und
einem Kommentarkorpus (JSONL aus strip_comments.py --corpus).

  python3 ngram_overlap.py --docs RUNS/withcom/docs \\
                           --corpus results/dokchess-en/comments-doc.jsonl \\
                           --null-docs RUNS/nocom/docs

--null-docs ist die Dokumentation, die OHNE Kommentare erzeugt wurde. Sie
dient als Nullmodell: jede Ueberlappung dort ist zwangslaeufig zufaellig,
weil das Modell die Kommentare nie gesehen hat. Ohne diesen Vergleichswert
ist eine Prozentzahl nicht interpretierbar.

Ausgabe:
  1. Ueberlappungskurve ueber n (Doku-Precision und Kommentar-Recall)
  2. Die laengsten woertlichen Uebereinstimmungen mit Fundstelle
  3. Optional CSV fuer die weitere Auswertung
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------- Aufbereitung

FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s.*$", re.M)
TABLE_RE = re.compile(r"^\s*\|.*$", re.M)
LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
HTML_RE = re.compile(r"<[^>]+>")

JAVADOC_TAG_RE = re.compile(r"@\w+")
JAVADOC_INLINE_RE = re.compile(r"\{@\w+\s*([^}]*)\}")
COMMENT_MARKER_RE = re.compile(r"^\s*(/\*+|\*+/|\*|//)", re.M)

WORD_RE = re.compile(r"[a-z0-9]+")


def clean_markdown(text: str) -> str:
    """Fliesstext aus Markdown. Codebloecke, Mermaid, Tabellen, Ueberschriften
    und Inline-Code fliegen raus -- dort waeren Uebereinstimmungen trivial."""
    text = FENCE_RE.sub(" ", text)
    text = HEADING_RE.sub(" ", text)
    text = TABLE_RE.sub(" ", text)
    text = INLINE_CODE_RE.sub(" ", text)
    text = LINK_RE.sub(r"\1", text)
    text = HTML_RE.sub(" ", text)
    return text


def clean_comment(text: str) -> str:
    """Javadoc-Syntax entfernen, Prosa behalten."""
    text = JAVADOC_INLINE_RE.sub(r"\1", text)
    text = COMMENT_MARKER_RE.sub(" ", text)
    text = text.replace("*/", " ").replace("/*", " ")
    text = JAVADOC_TAG_RE.sub(" ", text)
    text = HTML_RE.sub(" ", text)
    return text


def tokenize(text: str):
    return WORD_RE.findall(text.lower())


def ngrams(tokens, n):
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


# ---------------------------------------------------------------- Einlesen

def load_docs(path: Path):
    """{dateiname: tokenliste}"""
    out = {}
    for f in sorted(path.glob("*.md")):
        raw = f.read_text(encoding="utf-8", errors="replace")
        toks = tokenize(clean_markdown(raw))
        if toks:
            out[f.name] = toks
    return out


def load_corpus(path: Path, categories=None):
    """Liste von (herkunft, tokenliste)."""
    out = []
    for line in path.open(encoding="utf-8"):
        rec = json.loads(line)
        if categories and rec["category"] not in categories:
            continue
        toks = tokenize(clean_comment(rec["text"]))
        if toks:
            origin = f"{rec['file']}:{rec['line']}"
            out.append((origin, toks))
    return out


# ---------------------------------------------------------------- Messung

def overlap(doc_tokens_by_file, corpus, n):
    """Precision (Anteil Doku-n-Gramme im Korpus) und Recall (umgekehrt)."""
    corpus_grams = set()
    for _, toks in corpus:
        corpus_grams.update(ngrams(toks, n))

    doc_grams = []
    for toks in doc_tokens_by_file.values():
        doc_grams.extend(ngrams(toks, n))

    if not doc_grams or not corpus_grams:
        return 0.0, 0.0, 0, 0

    hits = sum(1 for g in doc_grams if g in corpus_grams)
    doc_set = set(doc_grams)
    recall_hits = sum(1 for g in corpus_grams if g in doc_set)

    return (100.0 * hits / len(doc_grams),
            100.0 * recall_hits / len(corpus_grams),
            hits, len(doc_grams))


def longest_matches(doc_tokens_by_file, corpus, min_len=6, top=15):
    """Laengste woertliche Uebereinstimmungen, greedy von links."""
    index = defaultdict(list)          # n-Gramm-Startpunkt -> (origin, pos)
    seed = min_len
    for origin, toks in corpus:
        for i, g in enumerate(ngrams(toks, seed)):
            index[g].append((origin, toks, i))

    found = []
    for name, toks in doc_tokens_by_file.items():
        i = 0
        while i <= len(toks) - seed:
            g = tuple(toks[i:i + seed])
            best = None
            for origin, ctoks, j in index.get(g, []):
                k = seed
                while (i + k < len(toks) and j + k < len(ctoks)
                       and toks[i + k] == ctoks[j + k]):
                    k += 1
                if best is None or k > best[0]:
                    best = (k, origin, i)
            if best:
                length, origin, pos = best
                found.append({
                    "length": length,
                    "doc": name,
                    "origin": origin,
                    "text": " ".join(toks[pos:pos + length]),
                })
                i += length
            else:
                i += 1

    found.sort(key=lambda d: -d["length"])
    seen, out = set(), []
    for f in found:
        key = f["text"]
        if key in seen:
            continue
        seen.add(key)
        out.append(f)
        if len(out) >= top:
            break
    return out


# ---------------------------------------------------------------- Ausgabe

def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--docs", required=True, type=Path,
                    help="Verzeichnis mit der zu pruefenden Dokumentation")
    ap.add_argument("--corpus", required=True, type=Path,
                    help="Kommentarkorpus (JSONL)")
    ap.add_argument("--null-docs", type=Path,
                    help="Dokumentation ohne Kommentare (Nullmodell)")
    ap.add_argument("--foreign-corpus", type=Path,
                    help="Kommentarkorpus eines fremden Repos (2. Nullmodell)")
    ap.add_argument("--categories", default="",
                    help="nur diese Kategorien, z.B. javadoc oder javadoc,line")
    ap.add_argument("--min-n", type=int, default=3)
    ap.add_argument("--max-n", type=int, default=12)
    ap.add_argument("--headline-n", type=int, default=8,
                    help="n fuer die Kennzahl im Fliesstext")
    ap.add_argument("--top", type=int, default=15,
                    help="Anzahl der laengsten Treffer in der Ausgabe")
    ap.add_argument("--csv", type=Path, help="Kurve zusaetzlich als CSV")
    args = ap.parse_args()

    cats = set(c.strip() for c in args.categories.split(",") if c.strip())

    docs = load_docs(args.docs)
    corpus = load_corpus(args.corpus, cats or None)
    if not docs:
        sys.exit(f"Keine .md-Dateien unter {args.docs}")
    if not corpus:
        sys.exit(f"Korpus leer: {args.corpus}")

    null_docs = load_docs(args.null_docs) if args.null_docs else None
    foreign = load_corpus(args.foreign_corpus, cats or None) \
        if args.foreign_corpus else None

    doc_words = sum(len(t) for t in docs.values())
    corp_words = sum(len(t) for _, t in corpus)

    print(f"Dokumentation : {args.docs}")
    print(f"                {len(docs)} Dateien, {doc_words} Woerter (Fliesstext)")
    print(f"Kommentare    : {len(corpus)} Bloecke, {corp_words} Woerter"
          + (f"  [nur {','.join(sorted(cats))}]" if cats else ""))
    if null_docs:
        nw = sum(len(t) for t in null_docs.values())
        print(f"Nullmodell    : {len(null_docs)} Dateien, {nw} Woerter")
    if foreign:
        fw = sum(len(t) for _, t in foreign)
        print(f"Fremdkorpus   : {len(foreign)} Bloecke, {fw} Woerter")
    print()

    # --- Kurve
    header = f"{'n':>3}  {'Doku-Precision':>15}  {'Kommentar-Recall':>17}"
    if null_docs:
        header += f"  {'Nullmodell':>11}"
    if foreign:
        header += f"  {'Fremdkorpus':>12}"
    print(header)
    print("-" * len(header))

    rows = []
    for n in range(args.min_n, args.max_n + 1):
        prec, rec, hits, total = overlap(docs, corpus, n)
        line = f"{n:>3}  {prec:>14.2f}%  {rec:>16.2f}%"
        row = {"n": n, "precision": prec, "recall": rec,
               "hits": hits, "total_ngrams": total}
        if null_docs:
            nprec, _, _, _ = overlap(null_docs, corpus, n)
            line += f"  {nprec:>10.2f}%"
            row["null_precision"] = nprec
        if foreign:
            fprec, _, _, _ = overlap(docs, foreign, n)
            line += f"  {fprec:>11.2f}%"
            row["foreign_precision"] = fprec
        print(line)
        rows.append(row)

    # --- Kennzahl
    hn = args.headline_n
    hit = next((r for r in rows if r["n"] == hn), None)
    if hit:
        print()
        print(f"Kennzahl bei n={hn}: {hit['precision']:.2f} % der "
              f"{hit['total_ngrams']} {hn}-Gramme der Dokumentation "
              f"stehen wortgleich in den Kommentaren.")
        if "null_precision" in hit:
            diff = hit["precision"] - hit["null_precision"]
            print(f"  Nullmodell (Doku ohne Kommentare): "
                  f"{hit['null_precision']:.2f} %  ->  Differenz "
                  f"{diff:+.2f} Prozentpunkte")

    # --- Laengste Treffer
    print()
    print(f"Laengste woertliche Uebereinstimmungen (min. 6 Woerter):")
    print("-" * 60)
    matches = longest_matches(docs, corpus, min_len=6, top=args.top)
    if not matches:
        print("  keine")
    for m in matches:
        print(f"\n  {m['length']} Woerter  |  {m['doc']}")
        print(f"  Quelle: {m['origin']}")
        text = m["text"]
        for i in range(0, len(text), 72):
            print(f"    {text[i:i+72]}")

    if args.csv:
        import csv
        keys = list(rows[0].keys())
        with args.csv.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)
        print(f"\nCSV: {args.csv}")


if __name__ == "__main__":
    main()
