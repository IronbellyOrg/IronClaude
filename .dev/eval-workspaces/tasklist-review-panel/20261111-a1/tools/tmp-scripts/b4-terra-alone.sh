#!/usr/bin/env bash
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
RR="$EVAL/tools/run-reviewer.sh"
DS=TASK-WF-designSpec-20261107-075614; AL=TASK-WF-makeTheAliasOnly-20261105-051649; DE=TASK-WF-design-20261108-041415
run() { echo "START $(date -u +%T) $4/$1/$2=$3"; bash "$RR" "$EVAL" "$1" "$2" "$3" "combos/$4"; echo "END $(date -u +%T) $4/$1/$2 $(jq -c '[.observed_model,.model_ok,.findings_block]' "$EVAL/$1/reviews/combos/$4/$2.meta.json" 2>/dev/null)"; }
for p in $DS $AL $DE; do run "$p" t2-1 gpt-6.1-terra terra-alone-src; done
echo TERRA_ALONE_DONE
