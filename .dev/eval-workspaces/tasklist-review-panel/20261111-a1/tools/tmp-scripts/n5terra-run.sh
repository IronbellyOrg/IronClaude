#!/usr/bin/env bash
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
D=combos/n5-terra
for P in TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415; do
 for R in "t2b-1 muse-wonder-1.0" "t3-1 glm-5.3" "t4-1 gpt-6-luna" "t2-1 gpt-6.1-terra"; do
  set -- $R
  echo "START $P $1 $2 $(date -u +%T)"
  bash $EVAL/tools/run-reviewer.sh $EVAL $P $1 $2 $D
  M=$EVAL/$P/reviews/$D/$1.meta.json
  echo "END $P $1 $(jq -c '{observed_model,model_ok,findings_block,attempt,wall_s,output_tokens_all}' $M)"
  if [ "$1" = t2b-1 ] && [ "$(jq -r .model_ok $M)" != true ]; then echo "STOP muse failed check twice"; exit 3; fi
 done
done
echo ALLDONE
