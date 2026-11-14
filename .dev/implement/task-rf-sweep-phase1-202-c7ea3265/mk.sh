#!/usr/bin/env bash
# review prompt for a gate-lens item: mk.sh Tn item lens report-file
D=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/implement/task-rf-sweep-phase1-202-c7ea3265
cd /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
Q=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/r3-b1
t=$1; item=$2; lens=$3; rep=$4
cat > $D/work/$t/diff.txt <<EOT
The task (item $item, a QA-gate report-only lens agent spawn, $lens lens) produced one new untracked file: $Q/$rep ($(wc -l < $Q/$rep) lines). Read it from disk; it is the whole output. The spawned agent was given the item's report-only preamble, the item's lens prompt, the r3-b1 scope note, the input list and the report path (the item's Action text is in the brief). The report's own last lines read: $(tail -2 $Q/$rep | tr '\n' ' '). No other file changed from this task.
EOT
bash $D/mkprompt.sh $t 1 1 $D/work/$t/brief.txt $D/work/$t/diff.txt
