#!/usr/bin/env python3
"""
strip_comments.py -- Kommentare aus Java- oder C/C++-Quelltext entfernen.

Zwei Modi:
  blank     Kommentare durch Leerzeichen ersetzen, Zeilen- und Spaltenzahl
            bleiben exakt erhalten.  Fuer den Bytecode-/Objektvergleich.
  collapse  Kommentare entfernen und leer gewordene Zeilen loeschen.
            Der eigentliche Input fuer CodeWiki.

Kategorien:
  license   Kopfkommentar vor der ersten Deklaration mit Lizenzwortlaut
  doc       Javadoc /** */ bzw. Doxygen /** */, /*! */, ///, //!
  block     sonstige /* */
  line      sonstige //
  code      auskommentierter Quelltext (Heuristik, siehe --code-report)

--strip waehlt, was aus dem Quelltext entfernt wird.
--corpus-categories waehlt unabhaengig davon, was in den Kommentarkorpus
geschrieben wird.  Fuer die Ueberlappungsmessung will man dort nur die
Kategorien, die die Bedingungen unterscheiden -- typischerweise doc und
line, aber nicht license und nicht code.

Beispiele:
  # DokChess: Mit-Kommentare-Variante (nur Lizenzheader raus)
  strip_comments.py upstream/dokchess-en/src work/withcom --strip license

  # DokChess: Ohne-Kommentare-Variante, Korpus gleich mitnehmen
  strip_comments.py upstream/dokchess-en/src work/nocom \\
      --strip license,doc,line,block \\
      --corpus results/comments.jsonl --corpus-categories doc,line

  # umoria (C++), historical/ ausgeschlossen
  strip_comments.py upstream/umoria/src work/umoria/nocom --lang cpp \\
      --strip doc,line,block --exclude historical \\
      --corpus results/umoria/comments.jsonl --corpus-categories doc,line

  # nachtraegliche Pruefung
  strip_comments.py upstream/umoria/src work/umoria/nocom --lang cpp --verify
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from tree_sitter import Language, Parser
except ImportError:
    sys.exit("Fehlt: pip install tree-sitter")

LANGS = {
    "java": {
        "module": "tree_sitter_java",
        "suffixes": (".java",),
        "decl_types": ("package_declaration", "import_declaration"),
    },
    "cpp": {
        "module": "tree_sitter_cpp",
        "suffixes": (".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx"),
        "decl_types": ("preproc_include", "preproc_ifdef", "preproc_def",
                       "namespace_definition", "declaration",
                       "function_definition"),
    },
}

ALL_CATEGORIES = ("license", "doc", "block", "line", "code")

LICENSE_RE = re.compile(
    r"copyright|licen[cs]e|SPDX-|all rights reserved|free software",
    re.IGNORECASE)

# Heuristik fuer auskommentierten Quelltext.
CODE_PATTERNS = [
    r"^[\w\s\*&\[\]:<>,]+\([^)]*\)\s*[;{]\s*$",       # Aufruf/Signatur
    r"^[\w\.\[\]]+(->[\w\[\]]+)*\s*(=[^=]|\+=|-=|\*=|/=)[^;]*;\s*$",
    r"^[\w\.\[\]]+(\+\+|--)\s*;\s*$",
    r"^(if|for|while|switch)\s*\(",                   # mit Klammer!
    r"^return\b[^.]*;\s*$",
    r"^(else|do)\s*\{",
    r"^goto\s+\w+\s*;",
    r"^#\s*(include|define|ifdef|ifndef|endif|pragma)\b",
    r"^(public|private|protected|static|final|class|struct|void|int|char|"
    r"bool|float|double|unsigned|const|auto|typedef|enum)\b[\w\s\*&]*[;{(]",
    r"^(void|int|char|bool|float|double|unsigned|long|short|const|static|"
    r"auto|uint\w*|int\d+_t)\s+[\w\*\[\]]+\s*=[^;]*;\s*$",
    r"^\}\s*;?\s*$",
    r"^[\w:]+\s*::\s*\w+\s*[({]",
]
CODE_RE = re.compile("|".join(f"(?:{p})" for p in CODE_PATTERNS))


def load_language(name):
    spec = LANGS[name]
    try:
        mod = __import__(spec["module"])
    except ImportError:
        sys.exit(f"Fehlt: pip install {spec['module'].replace('_', '-')}")
    return Language(mod.language()), spec


def strip_markers(text):
    """Kommentarzeichen entfernen, damit die Heuristik den Inhalt sieht."""
    t = re.sub(r"^\s*/\*+!?|\*+/\s*$", "", text)
    t = re.sub(r"^\s*//+[!/]?", "", t, flags=re.M)
    t = re.sub(r"^\s*\*(?!/)", "", t, flags=re.M)
    return t.strip()


def looks_like_code(text):
    body = strip_markers(text)
    if not body:
        return False
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    if not lines:
        return False
    hits = sum(1 for l in lines if CODE_RE.match(l))
    return hits / len(lines) >= 0.5


def classify(node, text, before_decl):
    """Kategorie eines Kommentarknotens bestimmen."""
    if node.type == "line_comment" or text.startswith("//"):
        is_doc = text.startswith("///") or text.startswith("//!")
        kind = "doc" if is_doc else "line"
    elif text.startswith("/**") or text.startswith("/*!"):
        kind = "doc"
    else:
        kind = "block"

    if before_decl and LICENSE_RE.search(text) and len(text) > 80:
        return "license"
    if looks_like_code(text):
        return "code"
    return kind


def find_comments(tree, src: bytes, spec):
    """Alle Kommentarknoten mit Kategorie, in Dokumentreihenfolge."""
    decl_start = len(src)
    for child in tree.root_node.children:
        if child.type in ("block_comment", "line_comment", "comment"):
            continue
        decl_start = child.start_byte
        break

    out, stack = [], [tree.root_node]
    while stack:
        node = stack.pop()
        if node.type in ("block_comment", "line_comment", "comment"):
            text = src[node.start_byte:node.end_byte].decode("utf-8", "replace")
            line_start = src.rfind(b"\n", 0, node.start_byte) + 1
            own_line = src[line_start:node.start_byte].strip() == b""
            out.append({
                "category": classify(node, text, node.start_byte < decl_start),
                "start": node.start_byte,
                "end": node.end_byte,
                "line": node.start_point[0] + 1,
                "own_line": own_line,
                "text": text,
            })
        else:
            stack.extend(node.children)
    out.sort(key=lambda c: c["start"])

    # Zusammenhaengende Zeilenkommentare im Dateikopf bilden oft gemeinsam
    # den Lizenzblock (umoria: "// Copyright (c) ..." ueber mehrere Zeilen).
    # Einzeln greift die Laengenpruefung nicht, als Gruppe schon.
    head, prev_line = [], None
    for c in out:
        if c["start"] >= decl_start:
            break
        if prev_line is not None and c["line"] > prev_line + 1:
            break
        head.append(c)
        prev_line = c["line"]
    if head:
        joined = "\n".join(c["text"] for c in head)
        if LICENSE_RE.search(joined) and len(joined) > 80:
            for c in head:
                c["category"] = "license"
    return out


def words(text):
    return len(re.findall(r"[A-Za-z][A-Za-z'-]+", strip_markers(text)))


def merge_adjacent(comments):
    """
    Unmittelbar aufeinanderfolgende Zeilenkommentare zu einem Block
    zusammenfassen.

    In C-Code laufen zusammenhaengende Erlaeuterungen ueber mehrere
    `//`-Zeilen. Als Einzeleintraege im Korpus koennen n-Gramme nicht ueber
    die Zeilengrenze reichen, was laengere Uebereinstimmungen unsichtbar
    macht. Zusammengefasst verhalten sie sich wie ein Javadoc-Block.

    Zusammengefasst wird nur, was direkt untereinander steht und dieselbe
    Kategorie hat; die Zeilennummer des ersten Kommentars bleibt erhalten.
    """
    merged = []
    for c in comments:
        prev = merged[-1] if merged else None
        can_merge = (
            prev is not None
            and prev["category"] == c["category"]
            and c["text"].lstrip().startswith("//")
            and prev["text"].lstrip().startswith("//")
            and c["line"] == prev["end_line"] + 1
            # Nachgestellte Kommentare (hinter Code) gehoeren zu ihrer
            # eigenen Zeile. Sie zusammenzufassen wuerde n-Gramme ueber
            # unzusammenhaengende Erlaeuterungen hinweg erzeugen.
            and c.get("own_line") and prev.get("own_line")
        )
        if can_merge:
            prev["text"] += "\n" + c["text"]
            prev["end_line"] = c["line"]
        else:
            d = dict(c)
            d["end_line"] = c["line"] + c["text"].count("\n")
            merged.append(d)
    return merged


def strip_source(src: bytes, comments, categories, mode):
    targets = [c for c in comments if c["category"] in categories]
    if not targets:
        return src

    out = bytearray(src)
    for c in reversed(targets):
        chunk = src[c["start"]:c["end"]]
        out[c["start"]:c["end"]] = bytes(
            b if b == 0x0A else 0x20 for b in chunk)

    text = out.decode("utf-8", "replace")
    if mode == "blank":
        return text.encode("utf-8")

    original = src.decode("utf-8", "replace").splitlines()
    kept = []
    for i, line in enumerate(text.splitlines()):
        if line.strip() == "" and i < len(original) and original[i].strip():
            continue
        kept.append(line.rstrip())
    collapsed = []
    for line in kept:
        if line == "" and collapsed and collapsed[-1] == "":
            continue
        collapsed.append(line)
    while collapsed and collapsed[0] == "":
        collapsed.pop(0)
    return ("\n".join(collapsed) + "\n").encode("utf-8")


def ast_signature(parser, src: bytes):
    """Strukturvergleich ohne Kommentare und ohne Positionen."""
    sig = []

    def walk(node):
        if node.type in ("block_comment", "line_comment", "comment"):
            return
        if node.child_count == 0:
            sig.append((node.type, node.text.decode("utf-8", "replace")))
        else:
            sig.append((node.type,))
            for c in node.children:
                walk(c)

    walk(parser.parse(src).root_node)
    return sig


def source_files(root: Path, spec, excludes):
    for f in sorted(root.rglob("*")):
        if f.suffix not in spec["suffixes"] or not f.is_file():
            continue
        rel = f.relative_to(root)
        if any(part in excludes for part in rel.parts):
            continue
        yield f, rel


def cmd_strip(args, parser, spec):
    categories = set(c.strip() for c in args.strip.split(",") if c.strip())
    corpus_cats = set(c.strip() for c in args.corpus_categories.split(",")
                      if c.strip()) or categories
    unknown = (categories | corpus_cats) - set(ALL_CATEGORIES)
    if unknown:
        sys.exit(f"Unbekannte Kategorie: {', '.join(sorted(unknown))}")

    src_root, dst_root = Path(args.source), Path(args.dest)
    excludes = set(x.strip() for x in args.exclude.split(",") if x.strip())
    files = list(source_files(src_root, spec, excludes))
    if not files:
        sys.exit(f"Keine {args.lang}-Quelldateien unter {src_root}")

    corpus = open(args.corpus, "w", encoding="utf-8") if args.corpus else None
    counts = dict.fromkeys(ALL_CATEGORIES, 0)
    merged_blocks = dict.fromkeys(ALL_CATEGORIES, 0)
    wordcount = dict.fromkeys(ALL_CATEGORIES, 0)
    failed, parse_errors, code_samples = [], [], []

    for f, rel in files:
        raw = f.read_bytes()
        tree = parser.parse(raw)
        if tree.root_node.has_error:
            parse_errors.append(str(rel))

        comments = find_comments(tree, raw, spec)

        corpus_entries = (merge_adjacent(comments) if args.merge_adjacent
                          else comments)

        for c in comments:
            cat = c["category"]
            counts[cat] += 1
            wordcount[cat] += words(c["text"])
            if cat == "code" and len(code_samples) < 5:
                code_samples.append((str(rel), c["line"],
                                     strip_markers(c["text"])[:70]))
            if re.search(r"\\u[0-9a-fA-F]{4}", c["text"]):
                print(f"  WARNUNG {rel}:{c['line']} Unicode-Escape im Kommentar",
                      file=sys.stderr)

        if corpus:
            for c in corpus_entries:
                if c["category"] in corpus_cats:
                    corpus.write(json.dumps({
                        "file": str(rel), "line": c["line"],
                        "category": c["category"], "text": c["text"],
                    }, ensure_ascii=False) + "\n")
                    merged_blocks[c["category"]] += 1

        stripped = strip_source(raw, comments, categories, args.mode)

        if not tree.root_node.has_error:
            if ast_signature(parser, raw) != ast_signature(parser, stripped):
                failed.append(str(rel))

        target = dst_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(stripped)

    copied = 0
    if args.copy_others:
        for f in sorted(src_root.rglob("*")):
            if not f.is_file() or f.suffix in spec["suffixes"]:
                continue
            rel = f.relative_to(src_root)
            if any(part in excludes for part in rel.parts):
                continue
            target = dst_root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(f.read_bytes())
            copied += 1

    if corpus:
        corpus.close()

    print(f"{len(files)} Dateien -> {dst_root}  "
          f"(Sprache: {args.lang}, Modus: {args.mode})")
    if excludes:
        print(f"ausgeschlossen: {', '.join(sorted(excludes))}")
    if copied:
        print(f"zusaetzlich kopiert: {copied} Nicht-Quelldateien")
    print()
    print(f"  {'Kategorie':12} {'Anzahl':>8} {'Woerter':>9}   entfernt  Korpus")
    for cat in ALL_CATEGORIES:
        s = "  ja  " if cat in categories else "  --  "
        k = "  ja" if cat in corpus_cats and args.corpus else "  --"
        print(f"  {cat:12} {counts[cat]:8d} {wordcount[cat]:9d}   {s}    {k}")

    if code_samples and args.code_report:
        print("\n  Als auskommentierter Code erkannt (Stichprobe):")
        for rel, line, text in code_samples:
            print(f"    {rel}:{line}  {text}")

    if args.corpus:
        total = sum(merged_blocks.values())
        print(f"\nKorpus: {args.corpus}  ({total} Bloecke"
              + (", aufeinanderfolgende //-Zeilen zusammengefasst"
                 if args.merge_adjacent else "") + ")")

    if parse_errors:
        print(f"\nWARNUNG: Parserfehler in {len(parse_errors)} Datei(en) -- "
              f"dort wurde die AST-Verifikation uebersprungen:", file=sys.stderr)
        for p in parse_errors:
            print("  " + p, file=sys.stderr)

    if failed:
        print("\nFEHLER -- AST veraendert in:", file=sys.stderr)
        for f in failed:
            print("  " + f, file=sys.stderr)
        return 1

    checked = len(files) - len(parse_errors)
    print(f"\nAST-Verifikation ok: Struktur unveraendert "
          f"({checked}/{len(files)} Dateien geprueft).")
    return 0


def cmd_verify(args, parser, spec):
    a_root, b_root = Path(args.source), Path(args.dest)
    excludes = set(x.strip() for x in args.exclude.split(",") if x.strip())
    bad, missing, skipped = [], [], 0
    files = list(source_files(a_root, spec, excludes))
    for f, rel in files:
        other = b_root / rel
        if not other.exists():
            missing.append(str(rel))
            continue
        raw = f.read_bytes()
        if parser.parse(raw).root_node.has_error:
            skipped += 1
            continue
        if ast_signature(parser, raw) != ast_signature(parser, other.read_bytes()):
            bad.append(str(rel))
    print(f"{len(files)} Dateien geprueft, {skipped} wegen Parserfehler "
          f"uebersprungen.")
    for label, items in (("fehlend", missing), ("abweichend", bad)):
        if items:
            print(f"  {label}: {len(items)}")
            for i in items[:10]:
                print("    " + i)
    if not missing and not bad:
        print("  identische AST-Struktur in allen geprueften Dateien.")
        return 0
    return 1


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source")
    ap.add_argument("dest")
    ap.add_argument("--lang", choices=sorted(LANGS), default="java")
    ap.add_argument("--mode", choices=("blank", "collapse"), default="collapse")
    ap.add_argument("--strip", default="license,doc,block,line,code",
                    help="zu entfernende Kategorien: " + ",".join(ALL_CATEGORIES))
    ap.add_argument("--corpus", metavar="DATEI")
    ap.add_argument("--corpus-categories", default="",
                    help="Kategorien fuer den Korpus (Vorgabe: wie --strip)")
    ap.add_argument("--exclude", default="",
                    help="Pfadbestandteile ueberspringen, z.B. historical")
    ap.add_argument("--copy-others", action="store_true",
                    help="Nicht-Quelldateien mitkopieren (Ressourcen, Header)")
    ap.add_argument("--no-merge-adjacent", dest="merge_adjacent",
                    action="store_false",
                    help="aufeinanderfolgende //-Zeilen NICHT zu einem "
                         "Korpusblock zusammenfassen")
    ap.add_argument("--code-report", action="store_true",
                    help="Stichprobe der als Code erkannten Kommentare zeigen")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    lang, spec = load_language(args.lang)
    parser = Parser(lang)
    sys.exit(cmd_verify(args, parser, spec) if args.verify
             else cmd_strip(args, parser, spec))


if __name__ == "__main__":
    main()
