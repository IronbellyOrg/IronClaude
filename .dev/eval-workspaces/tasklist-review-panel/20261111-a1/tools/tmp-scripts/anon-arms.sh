#!/bin/bash
# Build blind scoring inputs: arms/scoring/<pkg>/<label>/merged-anon.md
# Anonymizes reviewer ids and file paths; strips sha/paths header.
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
PKGS="TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415"
# Random label assignment per package (independent per package for blinding)
for P in $PKGS; do
  KEY="$EVAL/arms/scoring/$P/arm-key.json"
  mkdir -p "$EVAL/arms/scoring/$P"
  if [ ! -f "$KEY" ]; then
    LAB=$(printf 'X\nY\nZ\n' | shuf)
    L1=$(echo "$LAB" | sed -n 1p); L2=$(echo "$LAB" | sed -n 2p); L3=$(echo "$LAB" | sed -n 3p)
    jq -n --arg a "$L1" --arg b "$L2" --arg c "$L3" '{A:$a, B:$b, C:$c}' > "$KEY"
  fi
  for ARM in A B C; do
    L=$(jq -r ".$ARM" "$KEY")
    D="$EVAL/arms/scoring/$P/$L"; mkdir -p "$D"
    SRC="$EVAL/arms/$ARM/$P/merged-1.md"
    # collect reviewer ids in report, map to R1..Rn
    IDS=$(grep -oE '\bt[0-9a-z]+-[0-9]+\b' "$SRC" | sort -u)
    sed "s|$EVAL|<EVAL>|g" "$SRC" > "$D/merged-anon.md"
    i=1
    for ID in $IDS; do
      sed -i "s/\b$ID\b/R$i/g" "$D/merged-anon.md"
      i=$((i+1))
    done
    # strip absolute candidate path line, keep sha only
    sed -i 's|^candidate: <EVAL>/[^ ]*/candidate.md sha256|candidate: <candidate file> sha256|' "$D/merged-anon.md"
    sed -i 's|report <EVAL>/[^ ,]*|report <redacted>|g' "$D/merged-anon.md"
    echo "$P $ARM -> $L ($(echo "$IDS" | wc -l) ids)"
  done
done
echo KEYFILES:; ls "$EVAL"/arms/scoring/*/arm-key.json
