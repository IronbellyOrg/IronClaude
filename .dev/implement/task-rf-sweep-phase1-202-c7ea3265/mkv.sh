#!/usr/bin/env bash
# review prompt for a verifier item: mkv.sh Tn item "agent type" report-file
D=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/implement/task-rf-sweep-phase1-202-c7ea3265
cd /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
Q=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/${GATE:-r3-b1}
t=$1; item=$2; kind=$3; rep=$4
cat > $D/work/$t/diff.txt <<EOT
The task (item $item, a QA-gate verification spawn, agent type $kind) produced one new untracked file: $Q/$rep ($(wc -l < $Q/$rep) lines). Read it from disk; it is the whole output. The spawned agent was given the item's verifier preamble verbatim, the inputs named in the item's Context (the consolidated findings file, the cycle-1 fix log, the cycle ledger with the cycle-0 PASS set and the gate inputs) and the report path. The report's own last lines read: $(tail -2 $Q/$rep | tr '\n' ' '). No other file changed from this task. To judge the item's Verification line, read the consolidated findings file (its F_0 list) and the cycle ledger cycle-0 PASS set, and check that the report gives RESOLVED or OPEN for every F_0 id and a PASS or FAIL for every check id of that set.
EOT
bash $D/mkprompt.sh $t 1 1 $D/work/$t/brief.txt $D/work/$t/diff.txt
