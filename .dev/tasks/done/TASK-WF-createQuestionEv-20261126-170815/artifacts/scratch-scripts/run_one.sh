#!/bin/bash
# usage: run_one.sh <name> <depth> <mode> <type> <q> <c> <k|-> <description>
cd /home/coder/workspaces/worktrees/IronClaude/issue-834-rest
export PYTHONDONTWRITEBYTECODE=1
H=/home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/harness
SC=/tmp/createQuestionEv-scratch
name=$1; depth=$2; mode=$3; type=$4; q=$5; c=$6; k=$7; desc=$8
extra=(); [ "$k" != "-" ] && extra=(--expect-comments "$k")
uv run --no-project python $H/run_create.py run --name "$name" --depth "$depth" --mode "$mode" --type "$type" --description "$desc" --expect-questions "$q" --expect-create "$c" "${extra[@]}" > $SC/logs/$name.out 2>&1
echo "exit=$?" >> $SC/logs/$name.out
