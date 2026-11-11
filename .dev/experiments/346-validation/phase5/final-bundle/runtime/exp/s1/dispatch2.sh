#!/usr/bin/env bash
# usage: dispatch2.sh <worktree-suffix e.g. ctl-r1> <step-id> <task-text-file> [--probe]
set -u
n="$1"; step="$2"; file="$3"
wt=/home/coder/workspaces/worktrees/IronClaude/exp346-ab-$n
old=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs
log=/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase4/coordinator-log.md
[ -f "$log" ] || printf '# Controlled A/B coordinator log (phase 4). One line per dispatched step. All step workers: claude-opus-5-5.\n\n| time | worktree | step | dispatch | task | brief | repo-root substitutions | spec-panel sha256[:12] at dispatch | task text hash |\n|---|---|---|---|---|---|---|---|---|\n' > "$log"
out=/tmp/impl/exp/s1/ab-$n-$step.txt
sed "s#$old#$wt#g" "$file" > "$out"
cnt=$(grep -o -F "$old" "$file" | wc -l)
sha=$(sha256sum ~/.claude/commands/sc/spec-panel.md | cut -c1-12)
cd /home/coder/workspaces/worktrees/IronClaude/issue-346-review-loop-convergence
orca orchestration worker-start --spec "$(cat "$out")" --task-title "AB $n $step" --worktree path:$wt --agent claude --model claude-opus-5-5 --run run_58af03dbfa92 --json > /tmp/impl/exp/s1/ab-start-$n-$step.json 2>&1
d=$(jq -r '.result.dispatchId // "FAILED"' /tmp/impl/exp/s1/ab-start-$n-$step.json)
t=$(jq -r '.result.taskId // "-"' /tmp/impl/exp/s1/ab-start-$n-$step.json)
printf '| %s | %s | %s | %s | %s | %s | %s | %s | %s |\n' "$(date -u +%FT%TZ)" "$n" "$step" "$d" "$t" "$(basename "$file")" "$cnt" "$sha" "$(sha256sum "$out" | cut -c1-16)" >> "$log"
echo "$n $step $d $t"
