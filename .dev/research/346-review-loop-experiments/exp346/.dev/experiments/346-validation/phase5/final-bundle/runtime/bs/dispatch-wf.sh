#!/usr/bin/env bash
set -u; shopt -u patsub_replacement 2>/dev/null
team="$1"; d=/tmp/impl/bs
log=/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/coordinator-log.md
c=$(cat $d/workflow-common.txt); c=${c//__TEAM__/$team}
printf '%s\n' "$c" > $d/wf-filled-$team.txt
cd /home/coder/workspaces/worktrees/IronClaude/issue-346-review-loop-convergence
orca orchestration worker-start --spec "$c" --task-title "BS346 $team workflow" --worktree path:/home/coder/workspaces/worktrees/IronClaude/bs346-$team --agent claude --model claude-opus-5-5 --run run_58af03dbfa92 --json > $d/start-wf-$team.json 2>&1
dd=$(jq -r '.result.dispatchId // "FAILED"' $d/start-wf-$team.json); tt=$(jq -r '.result.taskId // "-"' $d/start-wf-$team.json)
printf '| %s | workflow %s | %s | %s |\n' "$(date -u +%FT%TZ)" "$team" "$dd" "$tt" >> $log
echo "$team $dd $tt"
