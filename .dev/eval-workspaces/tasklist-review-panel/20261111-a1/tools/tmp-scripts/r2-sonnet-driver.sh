#!/usr/bin/env bash
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
mkdir -p $EVAL/combos/r2-sonnet
(while true; do sleep 285; orca orchestration send --from term_ee024ec7-8132-4850-892e-9ff5158375c0 --type heartbeat --subject alive --task-id task_96be50c1af9f --dispatch-id ctx_9d89f929de48 --phase "running reviewers" >/dev/null 2>&1; done) &
HB=$!
for p in TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415; do
  for r in "t4-1 claude-haiku-5-5" "t3-1 claude-haiku-5-5" "t4-2 grok-4.7" "t1b-1 claude-sonnet-5-5"; do
    set -- $r
    echo "START $p $1 $2 $(date -u +%T)"
    bash $EVAL/tools/run-reviewer.sh $EVAL $p $1 $2 combos/r2-sonnet
    echo "END $p $1 $(cat $EVAL/$p/reviews/combos/r2-sonnet/$1.cost.json | tr -d '\n ') $(date -u +%T)"
  done
done
kill $HB
echo ALL_DONE
