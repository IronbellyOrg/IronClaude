#!/usr/bin/env bash
# usage: dispatch-impl.sh <team> <plan-id e.g. TASK-WF-spec-20261108-181543> [amend-file]
set -u; shopt -u patsub_replacement 2>/dev/null
team="$1"; pid="$2"; am="${3:-}"; d=/tmp/impl/bs
log=/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/coordinator-log.md
plan=".dev/tasks/to-do/$pid/$pid.md"
if [ -n "$am" ] && [ -f "$am" ]; then a=$(cat "$am"); else a="No amendments for this team; skip step A."; fi
c=$(cat $d/implement-common.txt); c=${c//__TEAM__/$team}; c=${c//__PLAN__/$plan}; c=${c//__AMENDMENTS__/$a}
printf '%s\n' "$c" > $d/impl-filled-$team.txt
cd /home/coder/workspaces/worktrees/IronClaude/issue-346-review-loop-convergence
orca orchestration worker-start --spec "$c" --task-title "BS346 $team implement" --worktree path:/home/coder/workspaces/worktrees/IronClaude/bs346-$team --agent claude --model claude-opus-5-5 --run run_58af03dbfa92 --json > $d/start-impl-$team.json 2>&1
dd=$(jq -r '.result.dispatchId // "FAILED"' $d/start-impl-$team.json); tt=$(jq -r '.result.taskId // "-"' $d/start-impl-$team.json)
printf '| %s | implement %s | %s | %s |\n' "$(date -u +%FT%TZ)" "$team" "$dd" "$tt" >> $log
echo "$team $dd $tt"
