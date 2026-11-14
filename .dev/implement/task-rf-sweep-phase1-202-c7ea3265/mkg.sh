#!/usr/bin/env bash
# review prompt for a QA gate item: mkg.sh Tn item "kind text" report-file gate-folder
D=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/implement/task-rf-sweep-phase1-202-c7ea3265
cd /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
t=$1; item=$2; kind=$3; rep=$4; gate=${5:-r3-b2}
Q=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/$gate
cat > $D/work/$t/diff.txt <<EOT
The task (item $item, $kind) produced one new untracked file: $Q/$rep ($(wc -l < $Q/$rep) lines). Read it from disk; it is the whole output. The spawned agent was given the item's preamble, the item's prompt, the inputs named in the item's Context and the report path (the item's Action text is in the brief). The report's own last lines read: $(tail -2 $Q/$rep | tr '\n' ' '). No other file changed from this task.
EOT
bash $D/mkprompt.sh $t 1 1 $D/work/$t/brief.txt $D/work/$t/diff.txt
