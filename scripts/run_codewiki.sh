#!/usr/bin/env bash
#
# Einen CodeWiki-Lauf durchfuehren und vollstaendig protokollieren.
#
#   ./scripts/run_codewiki.sh <repo> <bedingung> <tag> [--pages]
#
# Beispiel:
#   ./scripts/run_codewiki.sh dokchess-en nocom 01
#
# Im Hintergrund (ueberlebt das Kappen der SSH-Verbindung):
#   nohup ./scripts/run_codewiki.sh dokchess-en nocom 01 \
#       > ~/cw-nocom-01.out 2>&1 &
#   echo $! > ~/cw.pid
#   tail -f ~/cw-nocom-01.out
#
# Eingabe wird unter $INPUT_ROOT erwartet, ausserhalb des Auswertungs-Repos:
#   /root/cw-input/<repo>-<bedingung>/
# Ausgabe landet unter runs/<repo>/<bedingung>-<tag>/.
#
# Der HTML-Viewer wird immer erzeugt; --no-pages als viertes Argument
# damit im Ausgabeverzeichnis nur Markdown liegt und die Dateizaehlung
# nicht durch Viewer-Artefakte verfaelscht wird.

set -euo pipefail

INPUT_ROOT=${INPUT_ROOT:-/root/cw-input}

REPO=${1:?repo, z.B. dokchess-en}
COND=${2:?bedingung, z.B. withcom oder nocom}
TAG=${3:?laufnummer, z.B. 01}
PAGES=${4:-}

ROOT=$(cd "$(dirname "$0")/.." && pwd)
PROJ="$INPUT_ROOT/$REPO-$COND"
OUT="$ROOT/runs/$REPO/$COND-$TAG"

# --- Vorbedingungen -------------------------------------------------------

[ -d "$PROJ" ] || { echo "Eingabe fehlt: $PROJ" >&2; exit 1; }
[ -e "$OUT" ]  && { echo "Lauf existiert schon: $OUT" >&2; exit 1; }

command -v codewiki >/dev/null || { echo "codewiki nicht im PATH" >&2; exit 1; }

SRC_FILES=$(find "$PROJ" \( -name '*.java' -o -name '*.cpp' -o -name '*.h' \) \
            | wc -l)
[ "$SRC_FILES" -gt 0 ] || { echo "Keine Quelldateien unter $PROJ" >&2; exit 1; }

mkdir -p "$OUT"

PAGES_FLAG="--github-pages"
[ "$PAGES" = "--no-pages" ] && PAGES_FLAG=""

echo "Repo:       $REPO"
echo "Bedingung:  $COND (Lauf $TAG)"
echo "Eingabe:    $PROJ  ($SRC_FILES Dateien)"
echo "Ausgabe:    $OUT"
echo

# --- Konfiguration sichern (ohne API-Key) ---------------------------------

codewiki config show 2>&1 \
    | grep -viE 'api[-_ ]?key|token.*sk-|secret' > "$OUT/config.txt" || true

# --- Lauf -----------------------------------------------------------------

START=$(date +%s)
START_ISO=$(date -u +%FT%TZ)

set +e
( cd "$PROJ" && PYTHONUNBUFFERED=1 codewiki generate \
      --output "$OUT/docs" \
      --verbose \
      $PAGES_FLAG ) > "$OUT/codewiki.log" 2>&1
RC=$?
set -e

END=$(date +%s)
DURATION=$((END - START))

# --- Protokoll ------------------------------------------------------------

MD_COUNT=0
MD_WORDS=0
if [ -d "$OUT/docs" ]; then
    MD_COUNT=$(find "$OUT/docs" -name '*.md' | wc -l)
    MD_WORDS=$(find "$OUT/docs" -name '*.md' -print0 \
               | xargs -0 --no-run-if-empty cat | wc -w)
fi

INPUT_CHARS=$(find "$PROJ" \( -name '*.java' -o -name '*.cpp' -o -name '*.h' \) \
              -print0 | xargs -0 --no-run-if-empty cat | wc -c)

upstream_commit=""
upstream_dirty=""
if [ -d "$ROOT/upstream/$REPO/.git" ] || [ -f "$ROOT/upstream/$REPO/.git" ]; then
    upstream_commit=$(git -C "$ROOT/upstream/$REPO" rev-parse HEAD 2>/dev/null || echo "")
    upstream_dirty=$(git -C "$ROOT/upstream/$REPO" status --porcelain 2>/dev/null | wc -l)
fi

cat > "$OUT/run.json" <<JSON
{
  "repo": "$REPO",
  "condition": "$COND",
  "tag": "$TAG",
  "exit_code": $RC,
  "started": "$START_ISO",
  "duration_s": $DURATION,
  "input_dir": "$PROJ",
  "input_files": $SRC_FILES,
  "input_chars": $INPUT_CHARS,
  "output_md_files": $MD_COUNT,
  "output_md_words": $MD_WORDS,
  "github_pages": $([ -n "$PAGES_FLAG" ] && echo true || echo false),
  "upstream_commit": "$upstream_commit",
  "upstream_dirty_files": ${upstream_dirty:-null},
  "eval_commit": "$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo '')",
  "codewiki_version": "$(codewiki --version 2>&1 | head -1 | tr -d '"')",
  "host": "$(hostname)"
}
JSON

# --- Zusammenfassung ------------------------------------------------------

echo
if [ $RC -ne 0 ]; then
    echo "FEHLGESCHLAGEN (exit $RC) nach ${DURATION}s"
    echo "Letzte Logzeilen:"
    tail -20 "$OUT/codewiki.log" | sed 's/^/  /'
    echo
    echo "Vollstaendiges Log: $OUT/codewiki.log"
    exit $RC
fi

echo "Fertig nach ${DURATION}s"
echo "  Markdown-Dateien: $MD_COUNT"
echo "  Woerter gesamt:   $MD_WORDS"
echo "  Ausgabe:          $OUT"
echo

if [ -f "$OUT/docs/module_tree.json" ]; then
    echo "Modulbaum:"
    python3 -c "
import json,sys
d=json.load(open('$OUT/docs/module_tree.json'))
def walk(n,depth=0):
    if isinstance(n,dict):
        for k,v in n.items():
            print('  '*(depth+1)+str(k)); walk(v,depth+1)
    elif isinstance(n,list):
        for i in n: walk(i,depth)
walk(d)
" 2>/dev/null | head -30 || echo "  (nicht lesbar)"
    echo
fi

echo "Naechste Schritte:"
echo "  ls $OUT/docs/"
echo "  git add runs/$REPO/$COND-$TAG && git commit -m 'Lauf $REPO/$COND-$TAG'"
