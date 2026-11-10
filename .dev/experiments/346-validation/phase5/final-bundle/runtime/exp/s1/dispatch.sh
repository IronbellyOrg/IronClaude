#!/usr/bin/env bash
# usage: dispatch.sh <A|B> <step-id> <task-text-file>
set -u
rep="$1"; step="$2"; file="$3"
wt=/home/coder/workspaces/worktrees/IronClaude/exp346-s1-armA-rep$rep
old=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs
log=/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase3/coordinator-log.md
mkdir -p "$(dirname "$log")"
out=/tmp/impl/exp/s1/task-$rep-$step.txt
sed "s#$old#$wt#g" "$file" > "$out"
n=$(grep -o -F "$old" "$file" | wc -l)
cd /home/coder/workspaces/worktrees/IronClaude/issue-346-review-loop-convergence
orca orchestration worker-start --spec "$(cat "$out")" --task-title "S1 rep$rep $step" --worktree path:$wt --agent claude --model claude-opus-5-5 --run run_58af03dbfa92 --json > /tmp/impl/exp/s1/start-$rep-$step.json 2>&1
d=$(jq -r '.result.dispatchId // "FAILED"' /tmp/impl/exp/s1/start-$rep-$step.json)
t=$(jq -r '.result.taskId // "-"' /tmp/impl/exp/s1/start-$rep-$step.json)
printf '| %s | rep%s | %s | dispatch %s | task %s | source %s | repo-root path substitutions: %s (old repo-root path -> %s) | sha256(task text sent) %s |\n' "$(date -u +%FT%TZ)" "$rep" "$step" "$d" "$t" "$(basename "$file")" "$n" "$wt" "$(sha256sum "$out" | cut -c1-16)" >> "$log"
echo "$rep $step $d $t"
