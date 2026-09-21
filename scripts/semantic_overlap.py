#!/usr/bin/env python3
"""
semantic_overlap.py -- Wieviel der generierten Dokumentation ist inhaltlich
aus den Quelltext-Kommentaren uebernommen, auch ohne woertliche Uebernahme?

Die n-Gramm-Messung beantwortet nur, ob abgeschrieben wurde. Ein Modell kann
den Inhalt eines Kommentars vollstaendig uebernehmen und trotzdem jedes Wort
aendern. Dieses Skript misst deshalb Satzaehnlichkeit ueber Embeddings.

  python3 semantic_overlap.py --docs RUNS/withcom/docs \\
      --corpus results/umoria/comments.jsonl \\
      --null-docs RUNS/nocom/docs

Der Kern ist der Vergleich zweier Verteilungen, nicht eine einzelne Zahl:

  Fuer jeden Satz der Dokumentation wird die hoechste Aehnlichkeit zu
  irgendeinem Kommentarsatz bestimmt. Das ergibt eine Verteilung. Dieselbe
  Verteilung wird fuer die Dokumentation gebildet, die OHNE Kommentare
  erzeugt wurde -- dort ist jede Aehnlichkeit zwangslaeufig zufaellig.
  Verschiebt sich die erste Verteilung sichtbar nach rechts, hat das Modell
  inhaltlich aus den Kommentaren geschoepft.

Damit muss keine Aehnlichkeitsschwelle geraten werden. Die ausgewiesenen
Schwellenwerte sind nur Lesehilfen, nicht die Aussage.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np

FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s.*$", re.M)
TABLE_RE = re.compile(r"^\s*\|.*$", re.M)
LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
HTML_RE = re.compile(r"<[^>]+>")
BULLET_RE = re.compile(r"^\s*([-*+]|\d+\.)\s+", re.M)

JAVADOC_INLINE_RE = re.compile(r"\{@\w+\s*([^}]*)\}")
JAVADOC_TAG_RE = re.compile(r"@\w+")
MARKER_RE = re.compile(r"^\s*(/\*+!?|\*+/|\*(?!/)|//+[!/]?)", re.M)

SENT_SPLIT_RE = re.compile(r"(?<=[.!?:;])\s+|\n{2,}")
WORD_RE = re.compile(r"[A-Za-z]{2,}")


def clean_markdown(text):
    text = FENCE_RE.sub(" ", text)
    text = HEADING_RE.sub(" ", text)
    text = TABLE_RE.sub(" ", text)
    text = INLINE_CODE_RE.sub(" ", text)
    text = LINK_RE.sub(r"\1", text)
    text = HTML_RE.sub(" ", text)
    text = BULLET_RE.sub("", text)
    return text


def clean_comment(text):
    text = JAVADOC_INLINE_RE.sub(r"\1", text)
    text = MARKER_RE.sub(" ", text)
    text = text.replace("*/", " ").replace("/*", " ")
    text = JAVADOC_TAG_RE.sub(" ", text)
    text = HTML_RE.sub(" ", text)
    return text


def sentences(text, min_words):
    out = []
    for raw in SENT_SPLIT_RE.split(text):
        s = " ".join(raw.split())
        if len(WORD_RE.findall(s)) >= min_words:
            out.append(s)
    return out


def load_docs(path, min_words):
    """Liste von (dateiname, satz, kontext); Kontext ist hier der Satz selbst."""
    items = []
    for f in sorted(Path(path).glob("*.md")):
        raw = f.read_text(encoding="utf-8", errors="replace")
        for s in sentences(clean_markdown(raw), min_words):
            items.append((f.name, s, s))
    return items


def load_corpus(path, min_words, categories, unit="sentence"):
    """
    Liste von (herkunft, text, kontext).

    `text` ist das, was verglichen wird; `kontext` der vollstaendige
    Kommentarblock, aus dem der Satz stammt. Kommentare laufen oft ueber
    mehrere Saetze ("A simple, fast, integer-based line-of-sight algorithm.
    By Joseph Hall, ..."), und ohne den Block sieht man in der Ausgabe
    weniger, als tatsaechlich uebereinstimmt.
    """
    items = []
    for line in Path(path).open(encoding="utf-8"):
        rec = json.loads(line)
        if categories and rec["category"] not in categories:
            continue
        origin = f"{rec['file']}:{rec['line']}"
        cleaned = clean_comment(rec["text"])
        block = " ".join(cleaned.split())
        if unit == "block":
            if len(WORD_RE.findall(block)) >= min_words:
                items.append((origin, block, block))
        else:
            for s in sentences(cleaned, min_words):
                items.append((origin, s, block))
    return items


def max_similarity(model, doc_items, corpus_items, batch=256):
    """Hoechste Kosinusaehnlichkeit jedes Doku-Satzes zu einem Kommentarsatz."""
    doc_emb = model.encode([it[1] for it in doc_items], batch_size=batch,
                           convert_to_numpy=True, normalize_embeddings=True,
                           show_progress_bar=False)
    cor_emb = model.encode([it[1] for it in corpus_items], batch_size=batch,
                           convert_to_numpy=True, normalize_embeddings=True,
                           show_progress_bar=False)
    best_val = np.empty(len(doc_emb), dtype=np.float32)
    best_idx = np.empty(len(doc_emb), dtype=np.int64)
    step = 512
    for i in range(0, len(doc_emb), step):
        sims = doc_emb[i:i + step] @ cor_emb.T
        best_idx[i:i + step] = sims.argmax(axis=1)
        best_val[i:i + step] = sims.max(axis=1)
    return best_val, best_idx


def histogram(values, lo=0.0, hi=1.0, bins=10):
    counts, edges = np.histogram(values, bins=bins, range=(lo, hi))
    return counts, edges


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--docs", required=True)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--null-docs",
                    help="Dokumentation ohne Kommentare (Nullmodell)")
    ap.add_argument("--categories", default="",
                    help="nur diese Korpuskategorien, z.B. doc,line")
    ap.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    ap.add_argument("--comment-unit", choices=("sentence", "block"),
                    default="sentence",
                    help="Kommentare satzweise oder als ganze Bloecke "
                         "vergleichen (Bloecke sind laenger, dadurch sinken "
                         "die Aehnlichkeiten zu kurzen Doku-Saetzen)")
    ap.add_argument("--min-words", type=int, default=5,
                    help="Saetze mit weniger Woertern ignorieren")
    ap.add_argument("--thresholds", default="0.6,0.7,0.8,0.9")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--csv", help="Aehnlichkeit je Doku-Satz als CSV")
    args = ap.parse_args()

    from sentence_transformers import SentenceTransformer

    cats = set(c.strip() for c in args.categories.split(",") if c.strip())
    docs = load_docs(args.docs, args.min_words)
    corpus = load_corpus(args.corpus, args.min_words, cats,
                         args.comment_unit)
    if not docs:
        sys.exit(f"Keine Saetze in {args.docs}")
    if not corpus:
        sys.exit(f"Keine Saetze in {args.corpus}")
    nulls = load_docs(args.null_docs, args.min_words) if args.null_docs else None

    print(f"Dokumentation : {len(docs)} Saetze aus {args.docs}")
    unit_label = "Bloecke" if args.comment_unit == "block" else "Saetze"
    print(f"Kommentare    : {len(corpus)} {unit_label}"
          + (f"  [nur {','.join(sorted(cats))}]" if cats else ""))
    if nulls:
        print(f"Nullmodell    : {len(nulls)} Saetze aus {args.null_docs}")
    print(f"Modell        : {args.model}")
    print()

    model = SentenceTransformer(args.model)
    best, best_idx = max_similarity(model, docs, corpus)
    null_best = None
    if nulls:
        null_best, _ = max_similarity(model, nulls, corpus)

    # --- Verteilung
    print("Verteilung der hoechsten Aehnlichkeit je Doku-Satz")
    counts, edges = histogram(best)
    ncounts = histogram(null_best)[0] if null_best is not None else None
    head = f"  {'Bereich':>12}  {'mit Komm.':>18}"
    if ncounts is not None:
        head += f"  {'ohne Komm.':>18}"
    print(head)
    print("  " + "-" * (len(head) - 2))
    for i in range(len(counts)):
        rng = f"{edges[i]:.1f}-{edges[i+1]:.1f}"
        pa = 100.0 * counts[i] / len(best)
        line = f"  {rng:>12}  {counts[i]:>8} ({pa:5.1f}%)"
        if ncounts is not None:
            pb = 100.0 * ncounts[i] / len(null_best)
            line += f"  {ncounts[i]:>8} ({pb:5.1f}%)"
        print(line)

    # --- Kennzahlen
    print()
    print("Kennzahlen")
    rows = [("Median", np.median), ("Mittelwert", np.mean),
            ("90. Perzentil", lambda v: np.percentile(v, 90)),
            ("99. Perzentil", lambda v: np.percentile(v, 99))]
    for name, fn in rows:
        line = f"  {name:16} {fn(best):.3f}"
        if null_best is not None:
            line += f"   Nullmodell {fn(null_best):.3f}" \
                    f"   Differenz {fn(best)-fn(null_best):+.3f}"
        print(line)

    print()
    print("Anteil Saetze ueber Schwelle")
    for t in [float(x) for x in args.thresholds.split(",")]:
        a = 100.0 * (best >= t).mean()
        line = f"  >= {t:.2f}   {a:6.2f}%"
        if null_best is not None:
            b = 100.0 * (null_best >= t).mean()
            line += f"   Nullmodell {b:6.2f}%   Differenz {a-b:+6.2f} Pp"
        print(line)

    # --- Beispiele
    print()
    print(f"Aehnlichste Satzpaare (Top {args.top})")
    print("-" * 60)
    order = np.argsort(-best)[:args.top]
    for i in order:
        dname, dsent, _ = docs[i]
        oname, osent, oblock = corpus[best_idx[i]]
        print(f"\n  {best[i]:.3f}  {dname}  <-  {oname}")
        print(f"    Doku:      {dsent[:200]}")
        print(f"    Kommentar: {osent[:200]}")
        if oblock != osent:
            print(f"    im Block:  {oblock[:200]}")

    if args.csv:
        import csv
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["condition", "doc_file", "similarity",
                        "doc_sentence", "comment_origin", "comment_sentence",
                        "comment_block"])
            for i in range(len(docs)):
                w.writerow(["withcom", docs[i][0], f"{best[i]:.4f}",
                            docs[i][1], corpus[best_idx[i]][0],
                            corpus[best_idx[i]][1], corpus[best_idx[i]][2]])
            if null_best is not None:
                for i in range(len(nulls)):
                    w.writerow(["nocom", nulls[i][0], f"{null_best[i]:.4f}",
                                nulls[i][1], "", "", ""])
        print(f"\nCSV: {args.csv}")


if __name__ == "__main__":
    main()
