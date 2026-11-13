#!/usr/bin/env bash
E=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
P=$1; r=$2; id=$3; model=$4
NOFALLBACK=1 bash $E/tools/run-reviewer.sh $E $P $id $model combos/$r
echo "RERUN $r/$P/$id $(jq -c '[.observed_model,.model_ok,.findings_block]' $E/$P/reviews/combos/$r/$id.meta.json 2>/dev/null)"
