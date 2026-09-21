#!/usr/bin/env python3
"""
vocab_overlap.py -- Wieviel vom Wortschatz der Kommentare steckt schon in den
Bezeichnern?

Hintergrund: Die Messungen zeigen, dass Kommentare sich in der generierten
Dokumentation kaum niederschlagen. Eine sparsame Erklaerung waere, dass sie
wenig Neues beitragen -- weil derselbe Wortschatz bereits in Klassen-,
Methoden- und Variablennamen steckt. `playerComputeDiggingAbility` enthaelt
"compute", "digging" und "ability" auch ohne Kommentar.

Bezeichner werden dafuer in ihre Bestandteile zerlegt: CamelCase,
snake_case, SCREAMING_CASE und Bindestriche.

  python3 vocab_overlap.py --source work/umoria/nocom --lang cpp \\
      --corpus results/umoria/comments.jsonl \\
      --out results/umoria/vocab

Legt unter --out vier Textdateien ab, damit die Listen nachlesbar sind:
  comment-words.txt      Wortschatz der Kommentare, nach Haeufigkeit
  identifier-words.txt   Wortschatz der Bezeichner, nach Haeufigkeit
  shared.txt             Schnittmenge
  comment-only.txt       nur in Kommentaren -- das ist der eigentliche Zugewinn

Der Quelltext sollte die KOMMENTARFREIE Fassung sein, sonst zaehlt man die
Kommentare doppelt.
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

# Schluesselwoerter und Typen der Sprache. Sie stehen in jeder Datei und
# sagen nichts ueber den fachlichen Wortschatz aus.
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

# Allerweltswoerter des Englischen. Kommentare bestehen ueberwiegend daraus,
# Bezeichner fast nie -- ohne diesen Filter waere die Ueberlappung
# kuenstlich niedrig.
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

TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_]*")
COMMENT_MARKER_RE = re.compile(r"^\s*(/\*+!?|\*+/|\*(?!/)|//+[!/]?)", re.M)
JAVADOC_TAG_RE = re.compile(r"@\w+")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")


def split_identifier(name):
    """
    handleEvent      -> handle, event
    player_move      -> player, move
    MAX_HP           -> max, hp
    XMLHttpRequest   -> xml, http, request
    """
    parts = re.split(r"[_\-\d]+", name)
    out = []
    for p in parts:
        if not p:
            continue
        # CamelCase und Akronyme trennen
        for w in re.findall(r"[A-Z]+(?![a-z])|[A-Z][a-z]+|[a-z]+", p):
            out.append(w.lower())
    return out


def identifier_words(path, suffixes, lang):
    """Wortschatz aus allen Bezeichnern des Quelltexts."""
    try:
        import tree_sitter
        from tree_sitter import Language, Parser
        mod = __import__(f"tree_sitter_{lang}")
        parser = Parser(Language(mod.language()))
    except ImportError:
        sys.exit(f"Fehlt: pip install tree-sitter tree-sitter-{lang}")

    counter = Counter()
    files = 0
    for f in sorted(Path(path).rglob("*")):
        if f.suffix not in suffixes or not f.is_file():
            continue
        files += 1
        src = f.read_bytes()
        stack = [parser.parse(src).root_node]
        while stack:
            node = stack.pop()
            if node.type in ("identifier", "field_identifier", "type_identifier",
                             "namespace_identifier", "statement_identifier"):
                name = src[node.start_byte:node.end_byte].decode("utf-8", "replace")
                for w in split_identifier(name):
                    if len(w) > 1 and w not in KEYWORDS:
                        counter[w] += 1
            else:
                stack.extend(node.children)
    return counter, files


def comment_words(corpus_path, categories):
    """Wortschatz aus dem Kommentarkorpus."""
    counter = Counter()
    blocks = 0
    for line in Path(corpus_path).open(encoding="utf-8"):
        rec = json.loads(line)
        if categories and rec["category"] not in categories:
            continue
        blocks += 1
        text = COMMENT_MARKER_RE.sub(" ", rec["text"])
        text = JAVADOC_TAG_RE.sub(" ", text)
        text = text.replace("*/", " ").replace("/*", " ")
        for w in WORD_RE.findall(text):
            lw = w.lower().strip("'-")
            if len(lw) > 1:
                counter[lw] += 1
    return counter, blocks


def write_list(path, counter, header):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"# {header}\n# {len(counter)} verschiedene Woerter, "
                 f"{sum(counter.values())} Vorkommen\n#\n")
        for w, n in counter.most_common():
            fh.write(f"{n:7d}  {w}\n")


def report(label, comments, identifiers, stop):
    """Anteil der Kommentarwoerter, die auch in Bezeichnern vorkommen."""
    c = Counter({w: n for w, n in comments.items() if w not in stop})
    i = Counter({w: n for w, n in identifiers.items() if w not in stop})

    shared = set(c) & set(i)
    types_pct = 100.0 * len(shared) / len(c) if c else 0.0

    hits = sum(n for w, n in c.items() if w in i)
    total = sum(c.values())
    tokens_pct = 100.0 * hits / total if total else 0.0

    print(f"  {label}")
    print(f"    verschiedene Woerter in Kommentaren  {len(c):6d}")
    print(f"    davon auch in Bezeichnern           {len(shared):6d}   "
          f"{types_pct:5.1f} %")
    print(f"    Vorkommen in Kommentaren            {total:6d}")
    print(f"    davon Woerter, die auch in           {hits:6d}   "
          f"{tokens_pct:5.1f} %")
    print(f"    Bezeichnern vorkommen")
    return c, i, shared


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True,
                    help="kommentarfreier Quelltext")
    ap.add_argument("--corpus", required=True, help="Kommentarkorpus (JSONL)")
    ap.add_argument("--lang", choices=sorted(LANG_SUFFIXES), default="cpp")
    ap.add_argument("--categories", default="",
                    help="nur diese Korpuskategorien, z.B. doc,line")
    ap.add_argument("--out", required=True, help="Verzeichnis fuer die Listen")
    ap.add_argument("--top", type=int, default=25,
                    help="Anzahl Beispiele in der Ausgabe")
    args = ap.parse_args()

    cats = set(c.strip() for c in args.categories.split(",") if c.strip())
    suffixes = LANG_SUFFIXES[args.lang]

    idents, n_files = identifier_words(args.source, suffixes, args.lang)
    comms, n_blocks = comment_words(args.corpus, cats)

    print(f"Quelltext  : {args.source}  ({n_files} Dateien)")
    print(f"Kommentare : {args.corpus}  ({n_blocks} Bloecke)")
    print()

    # Beide Varianten berichten -- die Stoppwortentscheidung veraendert das
    # Ergebnis erheblich, also nicht eine davon stillschweigend waehlen.
    print("Ueberlappung des Wortschatzes\n")
    report("mit Allerweltswoertern", comms, idents, set())
    print()
    c, i, shared = report("ohne Allerweltswoerter", comms, idents, STOPWORDS)

    only = Counter({w: n for w, n in c.items() if w not in i})
    print()
    print(f"  Haeufigste Woerter, die NUR in Kommentaren vorkommen:")
    print("   ", ", ".join(w for w, _ in only.most_common(args.top)))

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_list(out / "comment-words.txt", c,
               "Wortschatz der Kommentare (ohne Allerweltswoerter)")
    write_list(out / "identifier-words.txt", i,
               "Wortschatz der Bezeichner (ohne Allerweltswoerter)")
    write_list(out / "shared.txt",
               Counter({w: c[w] for w in shared}),
               "In Kommentaren UND Bezeichnern, Haeufigkeit aus Kommentaren")
    write_list(out / "comment-only.txt", only,
               "Nur in Kommentaren -- der eigentliche Zugewinn")
    print(f"\n  Listen: {out}/")


if __name__ == "__main__":
    main()
