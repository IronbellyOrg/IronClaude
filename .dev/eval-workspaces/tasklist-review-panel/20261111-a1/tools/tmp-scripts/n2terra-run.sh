#!/usr/bin/env bash
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
for p in TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415; do
 for r in "t4-1 claude-haiku-5-5" "t2-1 gpt-6.1-terra"; do set -- $r
  echo "START $(date -u +%T) $p $1"
  bash $EVAL/tools/run-reviewer.sh $EVAL $p $1 $2 combos/n2-terra
  echo "END $(date -u +%T) $p $1 $(tr -d '\n ' < $EVAL/$p/reviews/combos/n2-terra/$1.cost.json) $(tr -d '\n ' < $EVAL/$p/reviews/combos/n2-terra/$1.meta.json)"
  orca orchestration send --from term_f82b4485-9352-4e8f-a993-8bcaa09e3db2 --type heartbeat --subject alive --task-id task_af879259575a --dispatch-id ctx_49211f70a0d8 --phase "running $p $1" >/dev/null 2>&1
 done
done
echo ALLDONE
