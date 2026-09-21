#!/usr/bin/env python3
"""
per_file_overlap.py -- Wirkung der Kommentare je Datei statt gemittelt.

Ueber alle Dokumente gemittelt verschwindet der Effekt: Bei manchen Dateien
enthalten die Kommentare Information, die im Code nicht steht (Herleitungen,
Literaturverweise, Grenzfaelle), bei den meisten wiederholen sie nur, was der
Bezeichner schon sagt. Der Mittelwert ueber beides sagt wenig.

Dieses Skript vergleicht deshalb je Datei und stellt die Ergebnisse
sortiert nebeneinander. Die Frage ist nicht "wie stark ist der Effekt",
sondern "bei wie vielen Dateien gibt es ihn ueberhaupt".

  python3 per_file_overlap.py \\
      --withcom runs/umoria/single-flash-full/withcom \\
      --nocom   runs/umoria/single-flash-full/nocom \\
      --corpus  results/umoria/comments.jsonl \\
      --source-nocom work/umoria/nocom \\
      --csv results/umoria/per-file.csv

Verglichen wird ausschliesslich gegen die Kommentare DERSELBEN Quelldatei --
das ist die einzige Menge, die den Unterschied zwischen den Bedingungen
ausmacht. Kommentare anderer Dateien hat das Modell im Einzelprompt nie
gesehen. Die Kandidatenwoerter je Datei sind alle Woerter, die im Kommentar
dieser Datei stehen, aber NICHT im kommentarfreien Quelltext derselben
Datei -- keine Grossschreibungs-Heuristik, nur eine kurze Stoppwortliste.

Gezaehlt werden EINDEUTIGE Woerter (Typen), nicht Vorkommen: ob ein Begriff
einmal oder zehnmal auftaucht, zaehlt fuer die Kernfrage "taucht er ueberhaupt
auf" gleich. Frueher enthielt die Ausgabe zusaetzlich n-Gramm- und Embedding-
Kennzahlen pro Datei; die sind entfernt, weil sie entweder bei den meisten
Dateien ohnehin 0 waren (n-Gramme, seltene lange Uebereinstimmungen) oder
dieselbe Frage nur ungenauer beantworteten (Embeddings, gemittelt und
verrauscht) -- die Wortmessung traegt die Aussage allein.
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

MARKER_RE = re.compile(r"^\s*(/\*+!?|\*+/|\*(?!/)|//+[!/]?)", re.M)
JAVADOC_TAG_RE = re.compile(r"@\w+")
FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s.*$", re.M)
TABLE_RE = re.compile(r"^\s*\|.*$", re.M)
LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
HTML_RE = re.compile(r"<[^>]+>")

# Allerweltswoerter, die in praktisch jedem englischen Fliesstext vorkommen
# und daher nichts ueber Kommentarinhalt aussagen.
STOP = set("""the a an and or of to in for with on at by is are was were be
been being this that these those it its as from into out up down not no if
then than when where which who what how all any some each other more most
can may will would should could must do does did have has had using use used
value values function functions module modules code file files data type
types return returns set sets get gets number numbers new one two also only
here there both same such very much many few less least first last next
previous same else while until after before during over under again once
note notes todo fixme called call calls make makes made take takes given
give gives need needs want wants know known see seen look looks based
because since though although however therefore thus hence via per within
without about above below between through among against along across
result results case cases example examples way ways part parts kind kinds
used using uses def define defined definition""".split())


def clean_markdown(text):
    text = FENCE_RE.sub(" ", text)
    text = HEADING_RE.sub(" ", text)
    text = TABLE_RE.sub(" ", text)
    text = INLINE_CODE_RE.sub(" ", text)
    text = LINK_RE.sub(r"\1", text)
    return HTML_RE.sub(" ", text)


def clean_comment(text):
    text = MARKER_RE.sub(" ", text)
    text = text.replace("*/", " ").replace("/*", " ")
    text = JAVADOC_TAG_RE.sub(" ", text)
    return HTML_RE.sub(" ", text)


# ------------------------------------------------------------- Zuordnung

def source_stem(md_name):
    """
    rng_cpp_r2.md -> rng.cpp ; rng_h.md -> rng.h ; dungeon_los.md -> dungeon_los

    single_prompt.py haengt die Endung mit Unterstrich an, damit sich Header
    und Implementierung nicht ueberschreiben, und bei Wiederholungen zusaetzlich
    _r1, _r2. Beides wird hier zurueckuebersetzt.
    """
    stem = re.sub(r"_r\d+$", "", Path(md_name).stem)
    m = re.match(r"^(.*)_(c|cc|cpp|cxx|h|hh|hpp|hxx|java|py|js|ts)$", stem)
    return f"{m.group(1)}.{m.group(2)}" if m else stem


def group_docs(path):
    """{quelldatei: [(dateiname, text), ...]}"""
    out = defaultdict(list)
    for f in sorted(Path(path).glob("*.md")):
        out[source_stem(f.name)].append(
            (f.name, f.read_text(encoding="utf-8", errors="replace")))
    return out


def group_corpus(path, categories):
    """{quelldatei: [kommentartext, ...]}"""
    out = defaultdict(list)
    for line in Path(path).open(encoding="utf-8"):
        rec = json.loads(line)
        if categories and rec["category"] not in categories:
            continue
        out[Path(rec["file"]).name].append(clean_comment(rec["text"]))
    return out


def load_source_words(source_dir, filename):
    """
    Alle Woerter im kommentarfreien Quelltext EINER Datei.

    Sucht die Datei anhand ihres Namens unterhalb von source_dir, weil der
    relative Pfad im Korpus (z.B. "src/rng.cpp") nicht zwangslaeufig mit dem
    Layout von --source-nocom uebereinstimmt.
    """
    for cand in Path(source_dir).rglob(filename):
        text = cand.read_text(encoding="utf-8", errors="replace").lower()
        return set(re.findall(r"[a-z][a-z0-9_]*", text))
    return None


def comment_only_terms(comment_texts, source_words):
    """
    Eindeutige Woerter, die im Kommentar dieser Datei stehen, aber nicht im
    kommentarfreien Quelltext DERSELBEN Datei -- unabhaengig von
    Gross-/Kleinschreibung, ohne Laengen- oder Formatregel.
    """
    in_comments = set()
    for t in comment_texts:
        for w in re.findall(r"[A-Za-z][A-Za-z0-9'-]{2,}", t):
            lw = w.lower().strip("'-")
            if lw and lw not in STOP:
                in_comments.add(lw)
    if source_words is None:
        return in_comments
    return {w for w in in_comments if w not in source_words}


def doc_word_set(docs):
    """Menge aller eindeutigen Woerter im Fliesstext dieser Dokumente."""
    words = set()
    for _, text in docs:
        for w in re.findall(r"[A-Za-z][A-Za-z0-9'-]{2,}",
                            clean_markdown(text)):
            words.add(w.lower().strip("'-"))
    return words


# ------------------------------------------------------------- Auswertung

def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--withcom", required=True)
    ap.add_argument("--nocom", required=True)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--source-nocom", required=True,
                    help="Verzeichnis mit kommentarfreiem Quelltext; noetig, "
                         "um je Datei die Nur-Kommentar-Woerter zu bestimmen")
    ap.add_argument("--categories", default="")
    ap.add_argument("--top", type=int, default=8,
                    help="Anzahl Beispielbegriffe je Datei in der Ausgabe")
    ap.add_argument("--csv")
    args = ap.parse_args()

    cats = set(c.strip() for c in args.categories.split(",") if c.strip())
    with_docs = group_docs(args.withcom)
    no_docs = group_docs(args.nocom)
    corpus = group_corpus(args.corpus, cats)

    stems = sorted(set(with_docs) & set(no_docs))
    if not stems:
        sys.exit("Keine gemeinsamen Dateien in beiden Bedingungen")

    print(f"{len(stems)} Quelldatei(en), Vergleich je Datei gegen die "
          f"Kommentare derselben Datei\n")

    rows = []
    for stem in stems:
        comments = corpus.get(stem, [])
        if not comments:
            rows.append({"file": stem, "note": "keine Kommentare"})
            continue

        only = comment_only_terms(
            comments, load_source_words(args.source_nocom, stem))
        if not only:
            rows.append({"file": stem, "candidate_words": 0,
                        "note": "keine Kandidatenwoerter"})
            continue

        with_vocab = doc_word_set(with_docs[stem])
        no_vocab = doc_word_set(no_docs[stem])

        found_with = sorted(only & with_vocab)
        found_no = sorted(only & no_vocab)
        examples = sorted(set(found_with) - set(found_no))[:args.top]

        rows.append({
            "file": stem,
            "candidate_words": len(only),
            "found_withcom": len(found_with),
            "found_nocom": len(found_no),
            "examples": ", ".join(examples),
        })

    def strength(r):
        if "note" in r:
            return -1
        return r["found_withcom"] - r["found_nocom"]

    def ratio_str(r):
        w, n = r["found_withcom"], r["found_nocom"]
        if n == 0:
            return "-" if w == 0 else f"{w}x (nur mit)"
        return f"{w / n:.1f}x"

    rows.sort(key=strength, reverse=True)

    print(f"  {'Datei':22} {'Kandidaten':>10} {'mit Komm.':>10} "
          f"{'ohne Komm.':>10}  {'Verhaeltnis':>14}")
    print("  " + "-" * 72)
    for r in rows:
        if "note" in r:
            print(f"  {r['file']:22} {'-':>10}  {r['note']}")
            continue
        print(f"  {r['file']:22} {r['candidate_words']:10d} "
              f"{r['found_withcom']:10d} {r['found_nocom']:10d}  "
              f"{ratio_str(r):>14}")

    print("\n  'Kandidaten': eindeutige Woerter, die nur im Kommentar dieser")
    print("  Datei stehen (nicht im kommentarfreien Quelltext derselben Datei).")
    print("  'mit/ohne Komm.': wie viele davon in der jeweiligen Doku auftauchen.")
    print("  'Verhaeltnis': mit / ohne Komm., je Datei. '-' bei 0 zu 0,")
    print("  '...x (nur mit)' wenn ohne Kommentare kein einziges Wort auftaucht.")

    shown = [r for r in rows if "note" not in r and r["examples"]]
    if shown:
        print("\n  Beispiele (nur mit Kommentaren aufgetaucht):")
        for r in shown:
            if r["examples"]:
                print(f"    {r['file']:22} {r['examples']}")

    effect = sum(1 for r in rows if "note" not in r and strength(r) > 0)
    total = sum(1 for r in rows if "note" not in r)
    print(f"\n  Sichtbarer Effekt bei {effect} von {total} Dateien "
          f"(mindestens ein Kandidatenwort mehr mit als ohne Kommentare).")

    sum_with = sum(r["found_withcom"] for r in rows if "note" not in r)
    sum_no = sum(r["found_nocom"] for r in rows if "note" not in r)
    if sum_no > 0:
        print(f"\n  Ueber alle Dateien: {sum_with} Treffer mit Kommentaren "
              f"gegenueber {sum_no} ohne -- Faktor {sum_with / sum_no:.1f}.")
        print("  (Summe der Treffer, nicht Mittelwert der Einzelverhaeltnisse --")
        print("  sonst wuerden Dateien mit 1 vs. 0 genauso stark zaehlen wie")
        print("  Dateien mit 20 vs. 10.)")
    elif sum_with > 0:
        print(f"\n  Ueber alle Dateien: {sum_with} Treffer mit Kommentaren, "
              f"0 ohne.")

    if args.csv:
        import csv
        keys = ["file", "candidate_words", "found_withcom", "found_nocom",
               "examples", "note"]
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k, "") for k in keys})
        print(f"\n  CSV: {args.csv}")


if __name__ == "__main__":
    main()

