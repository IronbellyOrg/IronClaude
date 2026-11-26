#!/usr/bin/env bash
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
RR="$EVAL/tools/run-reviewer.sh"
DS=TASK-WF-designSpec-20261107-075614; AL=TASK-WF-makeTheAliasOnly-20261105-051649; DE=TASK-WF-design-20261108-041415
run() { echo "START $(date -u +%T) $4/$1/$2=$3"; bash "$RR" "$EVAL" "$1" "$2" "$3" "combos/$4"; echo "END $(date -u +%T) $4/$1/$2 $(jq -c '[.observed_model,.model_ok,.findings_block]' "$EVAL/$1/reviews/combos/$4/$2.meta.json" 2>/dev/null)"; }
# gate: start only when at most 2 muse reviewer bash procs are live; keep whole-row muse usage <= 2 concurrent with the b4 runner's muse runs
while [ "$(pgrep -f 'run-reviewer.sh.*muse-wonder-1.0' | wc -l)" -gt 2 ]; do sleep 60; done
echo "GATE_OPEN $(date -u +%T)"
for p in $DS $AL $DE; do
  run "$p" t2b-1 muse-wonder-1.0 n3-muse-luna-grok-src
  run "$p" t4-1 gpt-6-luna n3-muse-luna-grok-src
  run "$p" t4-2 grok-4.7 n3-muse-luna-grok-src
done
echo N3_SRC_DONE
