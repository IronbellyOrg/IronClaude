#!/usr/bin/env bash
# freeze.sh [--sw DIR] [--out FILE] [--tag NAME]   (DESIGN AO-5, K5, REQ-33)
# Records the sha256 of every file that the freeze covers (the cards, the extractors, the word lists, the format dictionaries,
# the rank table and the briefs) in config/freeze.json, and PRINTS the git commands that a person then runs. It never runs
# git tag, git add or git commit (K5): the tag is made by a person.
#   --sw DIR    the sweep-sheet tree to hash (default: this one); another tree only under /tmp (a test hook)
#   --out FILE  where the record goes (default <sw>/config/freeze.json); under SW or /tmp
#   --tag NAME  the tag name that is recorded as `freeze_tag` (default sweep-sheet-freeze-<UTC date>)
# Frozen files: cards/*.json, sweep/extractors.py, sweep/words.py, sweep/formats.py, sweep/rank.py (the rank table is one dict
# in that file, so its hash covers the table), briefs/*.txt.
# The record has `freeze_tag` (the name bin/run-panel.sh copies into every run.json), `files` {path relative to the tree:
# sha256} and the date. A frozen file that is not committed, or that differs from the last commit, stops the script (exit 3):
# the tag would name a commit that does not hold what was hashed.
# Exit: 0 recorded and printed; 2 bad argument or missing frozen file; 3 a frozen file is not committed as it is.
set -u -o pipefail
source "$(dirname "$0")/common.sh"

usage() {
  sed -n '2,2p' "$0" | sed 's/^# \{0,1\}//' >&2
  exit 2
}
TREE=$SW OUT= TAGNAME=
while [ $# -gt 0 ]; do
  [ $# -ge 2 ] || usage
  case "$1" in
    --sw) TREE=$2 ;;
    --out) OUT=$2 ;;
    --tag) TAGNAME=$2 ;;
    *) usage ;;
  esac
  shift 2
done
if [ "$(realpath -m -- "$TREE")" != "$(realpath -m -- "$SW")" ]; then
  case "$(realpath -m -- "$TREE")/" in /tmp/?*) ;; *) echo "E_OVERRIDE: --sw $TREE is outside /tmp/" >&2; exit 2 ;; esac
fi
[ -d "$TREE" ] || { echo "E_ARG: no tree $TREE" >&2; exit 2; }
OUT=${OUT:-$TREE/config/freeze.json}
sw_assert_writable "$OUT" || exit 2
TAGNAME=${TAGNAME:-sweep-sheet-freeze-$(date -u +%Y%m%d)}
[[ $TAGNAME =~ ^[A-Za-z0-9][A-Za-z0-9._/-]*$ ]] || { echo "E_ARG: bad tag name $TAGNAME" >&2; exit 2; }

FILES=()
for f in "$TREE"/cards/*.json "$TREE"/briefs/*.txt "$TREE"/sweep/extractors.py "$TREE"/sweep/words.py "$TREE"/sweep/formats.py "$TREE"/sweep/rank.py; do
  [ -f "$f" ] || { echo "E_MISSING: frozen file $f does not exist" >&2; exit 2; }
  FILES+=("${f#"$TREE"/}")
done

# Every frozen file must be committed as it is: git status is read-only.
TOP=$(git -C "$TREE" rev-parse --show-toplevel 2>/dev/null) || { echo "E_GIT: $TREE is not in a git repository" >&2; exit 3; }
DIRTY=$(cd "$TREE" && git status --porcelain -- "${FILES[@]}")
if [ -n "$DIRTY" ]; then
  echo "E_UNCOMMITTED: these frozen files are not committed as they are; commit them first:" >&2
  printf '%s\n' "$DIRTY" >&2
  exit 3
fi

HASHES=$(cd "$TREE" && for f in "${FILES[@]}"; do printf '%s\t%s\n' "$f" "$(sha256sum -- "$f" | cut -d' ' -f1)"; done)
JSON=$(jq -n --arg tag "$TAGNAME" --arg date "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg h "$HASHES" \
  '{schema: "sweep-freeze/1", freeze_tag: $tag, created: $date,
    files: ($h | split("\n") | map(split("\t") | {key: .[0], value: .[1]}) | from_entries)}')
mkdir -p "$(dirname "$OUT")" || exit 2
printf '%s\n' "$JSON" >"$OUT"

N=${#FILES[@]}
printf 'freeze.sh: %s frozen files hashed into %s\n' "$N" "$OUT"
printf 'Nothing was staged, committed or tagged. A person now runs, in %s:\n' "$TOP"
printf '  git add %s && git commit -m "freeze: sweep sheet cards, extractors, words, formats, rank table, briefs"\n' "$OUT"
printf '  git tag -a %s -m "Sweep Sheet freeze"\n' "$TAGNAME"
printf 'The tag must exist before the hold-out ground truth is committed (bin/check-order.sh freeze).\n'
