#!/usr/bin/env python3
"""
sentence_similarity.py -- Kosinusaehnlichkeit zweier Saetze, fuer den
schnellen Beleg im Text (statt eine ganze Korpusmessung anzustossen).

  python3 sentence_similarity.py \\
      "Compute the digging ability of player; based on strength, and type of tool used" \\
      "Calculates the player's digging effectiveness based on:"

Nutzt dasselbe Modell wie semantic_overlap.py, damit die Zahl zur
Korpusmessung passt.
"""

import argparse
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sentence_a")
    ap.add_argument("sentence_b")
    ap.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    args = ap.parse_args()

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        sys.exit("Fehlt: pip install sentence-transformers")

    model = SentenceTransformer(args.model)
    emb = model.encode([args.sentence_a, args.sentence_b],
                       normalize_embeddings=True, show_progress_bar=False)
    sim = float(emb[0] @ emb[1])

    print(f"Satz A: {args.sentence_a}")
    print(f"Satz B: {args.sentence_b}")
    print(f"Modell: {args.model}")
    print(f"\nKosinusaehnlichkeit: {sim:.3f}")


if __name__ == "__main__":
    main()
