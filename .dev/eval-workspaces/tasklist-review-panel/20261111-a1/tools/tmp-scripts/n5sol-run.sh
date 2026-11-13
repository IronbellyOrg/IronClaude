#!/usr/bin/env bash
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
for p in TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415; do
  for r in "t2b-1 muse-wonder-1.0" "t3-1 glm-5.3" "t4-1 gpt-6-luna" "t2-1 gpt-6.1-sol"; do
    set -- $r
    echo "START $p $1 $(date -u +%T)"
    bash $EVAL/tools/run-reviewer.sh $EVAL $p $1 $2 combos/n5-sol
    echo "END $p $1 $(date -u +%T) $(jq -c '[.attempts,.total_wall_s]' $EVAL/$p/reviews/combos/n5-sol/$1.cost.json) $(jq -c '[.observed_model,.model_ok,.findings_block]' $EVAL/$p/reviews/combos/n5-sol/$1.meta.json)"
  done
done
echo ALLDONE
