#!/usr/bin/env bash
# usage: dispatch.sh <team> ; team in diffgate minfix ponytail stoprule ledger
set -u; shopt -u patsub_replacement 2>/dev/null
team="$1"; d=/tmp/impl/bs
log=/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/coordinator-log.md
mkdir -p "$(dirname "$log")"
[ -f "$log" ] || printf '# Phase 5 coordinator log (brainstorm teams). Workers: claude-opus-5-5, base origin/master.\n\n| time | team | worktree | dispatch | task | brief hash |\n|---|---|---|---|---|---|\n' > "$log"
c=$(cat $d/common.txt); t=$(cat $d/theme-$team.txt)
c=${c//__THEME__/$t}; c=${c//__TEAM__/$team}
printf '%s\n' "$c" > $d/filled-$team.txt
cd /home/coder/workspaces/worktrees/IronClaude/issue-346-review-loop-convergence
orca orchestration worker-start --spec "$c" --task-title "BS346 $team brainstorm" --worktree new-top-level --name bs346-$team --base-branch origin/master --agent claude --model claude-opus-5-5 --run run_58af03dbfa92 --json > $d/start-$team.json 2>&1
dd=$(jq -r '.result.dispatchId // "FAILED"' $d/start-$team.json); tt=$(jq -r '.result.taskId // "-"' $d/start-$team.json)
printf '| %s | %s | bs346-%s | %s | %s | %s |\n' "$(date -u +%FT%TZ)" "$team" "$team" "$dd" "$tt" "$(sha256sum $d/filled-$team.txt | cut -c1-16)" >> "$log"
echo "$team $dd $tt"
