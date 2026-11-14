#!/usr/bin/env bash
# anon.sh <row> <pkg> [--root R1]   (DESIGN.md section 5.3, adapted from A1DIR/tools/tmp-scripts/anon-b11.sh)
# runs/<row>/<pkg>/merged-1.md -> scoring/<opaque>/<pkg>/<L>/merged-anon.md; key runs/<row>/<pkg>/label-key.json
# = {"opaque","label"} (never under scoring/). A re-run reuses the recorded key. Prints the scoring path.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
R1REAL=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
A1DIR=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
SB=/tmp/evalsb-collab-r1
ROW=${1:?usage: anon.sh <row> <pkg> [--root R1]}; PKG=${2:?}; shift 2
R1=$R1REAL
while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; *) echo "bad arg $1" >&2; exit 2;; esac; done
D=$R1/runs/$ROW/$PKG; SRC=$D/merged-1.md; KEY=$D/label-key.json
[ -f "$SRC" ] || { echo "FAIL no $SRC" >&2; exit 1; }
if [ -f "$KEY" ]; then
  OP=$(jq -r .opaque "$KEY"); L=$(jq -r .label "$KEY")
else
  OP=$(od -An -N6 -tx1 /dev/urandom | tr -d ' \n')
  L=$(printf 'Q\nR\nS\nT\nU\nV\n' | shuf -n1)
  jq -n -c --arg o "$OP" --arg l "$L" '{opaque:$o,label:$l}' > "$KEY"
fi
OUT=$R1/scoring/$OP/$PKG/$L; mkdir -p "$OUT"
esc() { printf '%s' "$1" | sed 's/[][\.*^$|]/\\&/g'; }
# 1. absolute R1 (the real one and a test root) and A1DIR -> <EVAL>; the sandbox root -> /tmp/evalsb
sed -e "s|$(esc "$R1")|<EVAL>|g" -e "s|$(esc "$R1REAL")|<EVAL>|g" -e "s|$(esc "$A1DIR")|<EVAL>|g" -e "s|$(esc "$SB")|/tmp/evalsb|g" \
  "$SRC" > "$OUT/merged-anon.md.tmp"
# 2. reviewer ids -> R1, R2, R3 in sorted order
i=1
for ID in $(grep -oE '\bt[0-9a-z]+-[0-9]+\b' "$OUT/merged-anon.md.tmp" | sort -u); do
  sed -i "s/\b$ID\b/R$i/g" "$OUT/merged-anon.md.tmp"; i=$((i + 1))
done
# 3. the two rules of anon-b11.sh:24-25, then drop any "origin" key (defensive; F3 never writes one)
sed -i -e 's|^candidate: <EVAL>/[^ ]*/candidate.md sha256|candidate: <candidate file> sha256|' \
       -e 's|report <EVAL>/[^ ,]*|report <redacted>|g' \
       -e 's/,\s*"origin"\s*:\s*"[^"]*"//g' -e 's/"origin"\s*:\s*"[^"]*"\s*,\s*//g' "$OUT/merged-anon.md.tmp"
mv "$OUT/merged-anon.md.tmp" "$OUT/merged-anon.md"
echo "$OUT"
