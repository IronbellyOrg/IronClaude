#!/usr/bin/env bash
# usage: freeze.sh [--no-write | --check]                                            (DESIGN 11.1 AO-5, K5, REQ-33)
# Hashes what the experiment freezes: recipes/recipes.json, recipes/rl-block.txt, recipes/search-form.txt,
# config/lenses.json, cards/*.json, briefs/* and rl/*.py. Writes the hashes and the name of the freeze tag to
# config/freeze.json and PRINTS the `git tag` command for a person to run. This script makes no git call at all: it never
# tags, commits or adds (K5), and the tag it names does not exist until a person creates it.
#
#   (no option)  write config/freeze.json and print the tag command.
#   --no-write   print the same, write nothing.
#   --check      compare config/freeze.json with the files now: prints one line per file that CHANGED, was ADDED or REMOVED
#                (a path, never content); exit 0 when they agree, 1 when they do not. bin/check-order.sh freeze runs it.
#
# freeze.json: {"schema": "rl-freeze/1", "freeze_tag": "rl-freeze-<12 hex>", "combined_sha256": "...", "files": {path: sha256}}.
# The tag name is the first 12 hex digits of combined_sha256 (the hash of the sorted per-file hash lines), so a new freeze
# (DESIGN 4.6) is a new tag. bin/run-panel.sh reads `freeze_tag` into run.json. Do not leave a config/freeze.json in the
# tree before the freeze: its presence says a freeze happened.
# RL_ROOT (default: the folder above bin/) names another root; the tests point it at synthetic files.
# Exit: 0 done, 1 --check found a difference, 2 usage or a frozen file is missing.
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=${RL_ROOT:-$(cd "$HERE/.." && pwd -P)}
export LC_ALL=C

help() { sed -n '2,/^set -u/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'; }
MODE=write
case "${1:-}" in
  -h | --help) help; exit 0 ;;
  "") ;;
  --no-write) MODE=print ;;
  --check) MODE=check ;;
  *) echo "usage: freeze.sh [--no-write | --check]" >&2; exit 2 ;;
esac
[ $# -le 1 ] || { echo "usage: freeze.sh [--no-write | --check]" >&2; exit 2; }

cd "$ROOT" || { echo "E_ROOT: cannot enter $ROOT" >&2; exit 2; }
shopt -s nullglob
FILES=(recipes/recipes.json recipes/rl-block.txt recipes/search-form.txt config/lenses.json cards/*.json briefs/* rl/*.py)
LIST=()
for f in "${FILES[@]}"; do
  [ -f "$f" ] || { echo "E_MISSING: $f" >&2; exit 2; }
  LIST+=("$f")
done
# "<sha256>  <path>" lines in path order
LINES=$(printf '%s\n' "${LIST[@]}" | sort | while IFS= read -r f; do sha256sum -- "$f"; done)
FILES_JSON=$(jq -R -s -S 'split("\n") | map(select(length > 0) | capture("^(?<h>[0-9a-f]{64})  (?<p>.*)$")) | map({(.p): .h}) | add' <<<"$LINES")
COMBINED=$(printf '%s\n' "$LINES" | sha256sum | cut -d' ' -f1)
TAG="rl-freeze-${COMBINED:0:12}"

if [ "$MODE" = check ]; then
  [ -f config/freeze.json ] || { echo "E_NO_FREEZE: config/freeze.json does not exist; run bin/freeze.sh" >&2; exit 2; }
  REC=$(jq -S '.files' config/freeze.json 2>/dev/null) || { echo "E_FREEZE_JSON: config/freeze.json is not valid JSON" >&2; exit 2; }
  DIFF=$(jq -n -r --argjson a "$REC" --argjson b "$FILES_JSON" \
    '[($a // {} | keys[]), ($b | keys[])] | unique[] as $k
     | if $a[$k] == null then "ADDED \($k)" elif $b[$k] == null then "REMOVED \($k)"
       elif $a[$k] != $b[$k] then "CHANGED \($k)" else empty end')
  [ -z "$DIFF" ] || { echo "$DIFF"; exit 1; }
  echo "freeze hashes match $(jq 'length' <<<"$FILES_JSON") files"
  exit 0
fi

if [ "$MODE" = write ]; then
  mkdir -p config
  jq -n -S --arg tag "$TAG" --arg combined "$COMBINED" --argjson files "$FILES_JSON" \
    '{schema: "rl-freeze/1", freeze_tag: $tag, combined_sha256: $combined, files: $files}' >config/freeze.json.tmp &&
    mv config/freeze.json.tmp config/freeze.json || { echo "E_WRITE: config/freeze.json" >&2; exit 2; }
  echo "wrote config/freeze.json ($(jq 'length' <<<"$FILES_JSON") files)"
fi
echo "$LINES"
echo
echo "combined sha256: $COMBINED"
echo "Commit config/freeze.json and every file above, then a person runs (this script never does):"
echo "  git tag -a $TAG -m \"Recipe Ledger freeze $TAG\" HEAD"
echo "Only after that tag exists does the hold-out ground truth get committed (REQ-33)."
