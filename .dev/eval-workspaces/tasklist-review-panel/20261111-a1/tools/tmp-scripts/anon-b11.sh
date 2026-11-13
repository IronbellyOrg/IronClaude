#!/bin/bash
# Anonymize combo merged reports for blind scoring: arms/scoring/combos/<C>/<P>/<L>/merged-anon.md
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
PKGS="TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415"
COMBOS="j1-sonnet-luna2-r1 j1-sonnet-luna2-r2 j1-sonnet-luna2-r3 j1-sonnet-luna2-r4 j1-sonnet-luna2-r5"
for C in $COMBOS; do
  for P in $PKGS; do
    SRC="$EVAL/combos/$C/$P/merged-1.md"
    [ -f "$SRC" ] || continue
    D="$EVAL/arms/scoring/combos/$C/$P"
    mkdir -p "$D"
    # pick a fresh random label (Q..V range, avoid X/Y/Z already used for arms)
    while :; do L=$(printf 'Q\nR\nS\nT\nU\nV\n' | shuf -n1); [ ! -d "$EVAL/arms/scoring/combos/$C/$P/$L" ] && break; done
    DD="$D/$L"; mkdir -p "$DD"
    echo "{\"label\":\"$L\",\"combo\":\"$C\"}" > "$D/label-key.json"
    IDS=$(grep -oE '\bt[0-9a-z]+-[0-9]+\b' "$SRC" | sort -u)
    sed "s|$EVAL|<EVAL>|g" "$SRC" > "$DD/merged-anon.md"
    i=1
    for ID in $IDS; do
      sed -i "s/\b$ID\b/R$i/g" "$DD/merged-anon.md"
      i=$((i+1))
    done
    sed -i 's|^candidate: <EVAL>/[^ ]*/candidate.md sha256|candidate: <candidate file> sha256|' "$DD/merged-anon.md"
    sed -i 's|report <EVAL>/[^ ,]*|report <redacted>|g' "$DD/merged-anon.md"
  done
done
find "$EVAL/arms/scoring/combos" -name merged-anon.md | wc -l
