#!/bin/bash
# Generate 39 blind judge dispatches (13 combos x 3 packages) as a run-list file.
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
OUT=/tmp/combo-judges.tsv
: > "$OUT"
find "$EVAL/arms/scoring/combos" -name merged-anon.md | while read -r F; do
  P=$(echo "$F" | sed 's|.*/scoring/combos/[^/]*/||; s|/[^/]*$||')
  C=$(echo "$F" | sed 's|.*/scoring/combos/||; s|/.*||')
  L=$(basename "$(dirname "$F")")
  echo -e "$C\t$P\t$L\t$F" >> "$OUT"
done
wc -l "$OUT"
