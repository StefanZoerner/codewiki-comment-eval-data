#!/usr/bin/env python3
"""
vocab_in_docs.py -- Wieviel vom Wortschatz der Kommentare landet in der
generierten Dokumentation?

Ergaenzt vocab_overlap.py, das nur den Quelltext betrachtet. Hier kommen die
generierten Dokumente dazu, und zwar beide Bedingungen: einmal mit
Kommentaren im Input, einmal ohne. Die Differenz ist das Signal.

  python3 vocab_in_docs.py \\
      --source work/umoria/nocom --lang cpp \\
      --corpus results/umoria/comments.jsonl \\
      --withcom-docs runs/umoria/single-flash-full/withcom \\
      --nocom-docs   runs/umoria/single-flash-full/nocom

Drei Gruppen werden getrennt ausgewiesen:

  Bezeichnerwoerter    Kontrollmessung. Sollte in beiden Bedingungen
                       aehnlich hoch liegen -- der Code ist ja identisch.
                       Weicht das stark ab, stimmt etwas am Aufbau nicht.

  Kommentarwoerter     Alle Woerter aus den Kommentaren. Ein hoher Wert
                       sagt wenig, weil rund 60 % davon ohnehin in
                       Bezeichnern stehen.

  nur in Kommentaren   Die eigentliche Messung: Woerter, die im
                       kommentarfreien Quelltext NICHT vorkommen. Sie
                       koennen nur ueber die Kommentare in die Doku
                       gelangen.
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

LANG_SUFFIXES = {
    "cpp": (".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx"),
    "java": (".java",),
    "python": (".py",),
}

KEYWORDS = set("""
auto break case char const continue default do double else enum extern float
for goto if inline int long register restrict return short signed sizeof
static struct switch typedef union unsigned void volatile while bool true
false class namespace template typename public private protected virtual
new delete this operator friend using explicit nullptr try catch throw
constexpr override final static_cast dynamic_cast const_cast reinterpret_cast
abstract assert boolean byte extends implements import instanceof interface
native package super synchronized throws transient def elif except from
global lambda none nonlocal not pass raise with yield and or is in as
include define ifdef ifndef endif pragma undef
std string vector map set list pair size_t uint int8 int16 int32 int64
""".split())

STOPWORDS = set("""
a an the this that these those it its is are was were be been being am
of to in for with on at by from into out up down off over under again
and or but not no nor so than then when where which who whom what how
all any both each few more most other some such only own same too very
can will just should now also may might must shall would could does did
do done has have had having here there we you they he she him her his
their our your my me us them if else while until because since about
against between through during before after above below one two three
first second next last new old
""".split())

COMMENT_MARKER_RE = re.compile(r"^\s*(/\*+!?|\*+/|\*(?!/)|//+[!/]?)", re.M)
JAVADOC_TAG_RE = re.compile(r"@\w+")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")

FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
HTML_RE = re.compile(r"<[^>]+>")
LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def split_identifier(name):
    out = []
    for p in re.split(r"[_\-\d]+", name):
        if not p:
            continue
        for w in re.findall(r"[A-Z]+(?![a-z])|[A-Z][a-z]+|[a-z]+", p):
            out.append(w.lower())
    return out


def identifier_words(path, suffixes, lang):
    try:
        from tree_sitter import Language, Parser
        mod = __import__(f"tree_sitter_{lang}")
        parser = Parser(Language(mod.language()))
    except ImportError:
        sys.exit(f"Fehlt: pip install tree-sitter tree-sitter-{lang}")

    counter = Counter()
    for f in sorted(Path(path).rglob("*")):
        if f.suffix not in suffixes or not f.is_file():
            continue
        src = f.read_bytes()
        stack = [parser.parse(src).root_node]
        while stack:
            node = stack.pop()
            if node.type.endswith("identifier"):
                name = src[node.start_byte:node.end_byte].decode("utf-8", "replace")
                for w in split_identifier(name):
                    if len(w) > 1 and w not in KEYWORDS:
                        counter[w] += 1
            else:
                stack.extend(node.children)
    return counter


def comment_words(corpus_path, categories):
    counter = Counter()
    for line in Path(corpus_path).open(encoding="utf-8"):
        rec = json.loads(line)
        if categories and rec["category"] not in categories:
            continue
        text = COMMENT_MARKER_RE.sub(" ", rec["text"])
        text = JAVADOC_TAG_RE.sub(" ", text)
        text = text.replace("*/", " ").replace("/*", " ")
        for w in WORD_RE.findall(text):
            lw = w.lower().strip("'-")
            if len(lw) > 1:
                counter[lw] += 1
    return counter


def doc_words(path, keep_code):
    """
    Wortschatz der generierten Dokumentation.

    Ohne --keep-code werden Codebloecke und Inline-Code entfernt: Bezeichner
    dort stammen aus dem Quelltext und sagen nichts ueber Formulierung aus.
    Fuer die Kontrollmessung an Bezeichnerwoertern ist das Gegenteil
    sinnvoll, deshalb der Schalter.
    """
    counter = Counter()
    files = 0
    for f in sorted(Path(path).glob("*.md")):
        files += 1
        text = f.read_text(encoding="utf-8", errors="replace")
        if not keep_code:
            text = FENCE_RE.sub(" ", text)
            text = INLINE_CODE_RE.sub(" ", text)
        text = LINK_RE.sub(r"\1", text)
        text = HTML_RE.sub(" ", text)
        for w in re.findall(r"[A-Za-z][A-Za-z0-9_'-]*", text):
            for part in (split_identifier(w) if any(c.isupper() for c in w[1:])
                         or "_" in w else [w.lower()]):
                if len(part) > 1:
                    counter[part] += 1
    return counter, files


def coverage(vocabulary, doc_vocab):
    """Anteil der Woerter aus `vocabulary`, die in der Doku vorkommen."""
    if not vocabulary:
        return 0.0, 0, 0
    hits = sum(1 for w in vocabulary if w in doc_vocab)
    return 100.0 * hits / len(vocabulary), hits, len(vocabulary)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True,
                    help="kommentarfreier Quelltext")
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--withcom-docs", required=True)
    ap.add_argument("--nocom-docs", required=True)
    ap.add_argument("--lang", choices=sorted(LANG_SUFFIXES), default="cpp")
    ap.add_argument("--categories", default="")
    ap.add_argument("--keep-code", action="store_true",
                    help="Codebloecke in der Doku mitzaehlen")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--csv")
    args = ap.parse_args()

    cats = set(c.strip() for c in args.categories.split(",") if c.strip())

    idents = identifier_words(args.source, LANG_SUFFIXES[args.lang], args.lang)
    comms = comment_words(args.corpus, cats)
    with_docs, n_with = doc_words(args.withcom_docs, args.keep_code)
    no_docs, n_no = doc_words(args.nocom_docs, args.keep_code)

    ident_v = {w for w in idents if w not in STOPWORDS}
    comm_v = {w for w in comms if w not in STOPWORDS}
    only_v = comm_v - ident_v

    print(f"Quelltext        : {args.source}")
    print(f"Kommentare       : {args.corpus}")
    print(f"Doku mit Komm.   : {args.withcom_docs}  ({n_with} Dateien)")
    print(f"Doku ohne Komm.  : {args.nocom_docs}  ({n_no} Dateien)")
    print(f"Codebloecke      : {'mitgezaehlt' if args.keep_code else 'entfernt'}")
    print()
    print(f"Wortschatz: {len(ident_v)} aus Bezeichnern, {len(comm_v)} aus "
          f"Kommentaren, davon {len(only_v)} nur in Kommentaren\n")

    rows = []
    header = f"  {'Gruppe':22} {'Woerter':>8}  {'mit Komm.':>16}  {'ohne Komm.':>16}  {'Diff.':>8}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for label, vocab in (("Bezeichnerwoerter", ident_v),
                         ("Kommentarwoerter", comm_v),
                         ("nur in Kommentaren", only_v)):
        pw, hw, n = coverage(vocab, with_docs)
        pn, hn, _ = coverage(vocab, no_docs)
        print(f"  {label:22} {n:8d}  {hw:6d} ({pw:5.1f} %)  "
              f"{hn:6d} ({pn:5.1f} %)  {pw - pn:+7.1f}")
        rows.append({"group": label, "vocab_size": n,
                     "hits_withcom": hw, "pct_withcom": round(pw, 2),
                     "hits_nocom": hn, "pct_nocom": round(pn, 2),
                     "diff_pp": round(pw - pn, 2)})

    print("\n  Die erste Zeile ist eine Kontrolle: Der Code ist in beiden "
          "Bedingungen\n  identisch, die Werte sollten also nah beieinander "
          "liegen.\n  Die letzte Zeile ist die eigentliche Messung.")

    gained = Counter({w: comms[w] for w in only_v
                      if w in with_docs and w not in no_docs})
    if gained:
        print(f"\n  Nur-Kommentar-Woerter, die ausschliesslich mit Kommentaren "
              f"auftauchen ({len(gained)}):")
        print("   ", ", ".join(w for w, _ in gained.most_common(args.top)))

    lost = Counter({w: comms[w] for w in only_v
                    if w in no_docs and w not in with_docs})
    if lost:
        print(f"\n  Gegenprobe -- nur OHNE Kommentare aufgetaucht ({len(lost)}):")
        print("   ", ", ".join(w for w, _ in lost.most_common(args.top)))

    if args.csv:
        import csv
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"\n  CSV: {args.csv}")


if __name__ == "__main__":
    main()
