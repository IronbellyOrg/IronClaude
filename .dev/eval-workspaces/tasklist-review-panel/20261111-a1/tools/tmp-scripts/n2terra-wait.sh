#!/usr/bin/env bash
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
P="TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415"
i=0
while true; do
  n=0; for p in $P; do for r in t2b-1 t4-1 t4-2 t2-1; do [ -f $EVAL/$p/reviews/combos/n2-terra/$r.cost.json ] && n=$((n+1)); done; done
  [ $n -ge 12 ] && { echo "ALL12 done"; exit 0; }
  if ! pgrep -f 'job.sh n2-terra' >/dev/null; then sleep 20; pgrep -f 'job.sh n2-terra' >/dev/null || { echo "NO_RUNNING_JOBS done=$n/12"; exit 1; }; fi
  i=$((i+1)); if [ $((i%10)) -eq 0 ]; then orca orchestration send --from term_f82b4485-9352-4e8f-a993-8bcaa09e3db2 --type heartbeat --subject alive --task-id task_af879259575a --dispatch-id ctx_49211f70a0d8 --phase "waiting for driver ($n/12)" >/dev/null 2>&1; fi
  sleep 30
done
