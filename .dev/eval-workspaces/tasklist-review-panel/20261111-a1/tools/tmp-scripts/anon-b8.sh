#!/bin/bash
# Anonymize combo merged reports for blind scoring: arms/scoring/combos/<C>/<P>/<L>/merged-anon.md
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
PKGS="TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415"
COMBOS="g1-ember-luna2-r1 g1-ember-luna2-r2 g1-ember-luna2-r3 g1-ember-luna2-r4 g2-sonnet-ember-r1 g2-sonnet-ember-r2 g2-sonnet-ember-r3 g2-sonnet-ember-r4 g3-sonnet-luna-ember-r1 g3-sonnet-luna-ember-r2 g3-sonnet-luna-ember-r3 g3-sonnet-luna-ember-r4 g4-haiku-ember-terra-r1 g4-haiku-ember-terra-r2 g4-haiku-ember-terra-r3 g4-haiku-ember-terra-r4 g5-ember2-luna-r1 g5-ember2-luna-r2 g5-ember2-luna-r3 g5-ember2-luna-r4 g6-luna2-ember2-r1 g6-luna2-ember2-r2 g6-luna2-ember2-r3 g6-luna2-ember2-r4 g7-haiku-luna2-r1 g7-haiku-luna2-r2 g7-haiku-luna2-r3 g7-haiku-luna2-r4 g8-ember-terra-r1 g8-ember-terra-r2 g8-ember-terra-r3 g8-ember-terra-r4 g9-ember-luna-r1 g9-ember-luna-r2 g9-ember-luna-r3 g9-ember-luna-r4"
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
