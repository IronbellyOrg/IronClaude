#!/usr/bin/env bash
# review prompt for a Phase 8 QA gate lens item: mkg8.sh Tn item "kind text" report-file
D=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/implement/task-rf-sweep-phase1-202-c7ea3265
cd /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
t=$1; item=$2; kind=$3; rep=$4
Q=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/tests
cat > $D/work/$t/diff.txt <<EOT
The task (item $item, $kind) produced one new untracked file: $Q/$rep ($(wc -l < $Q/$rep) lines). Read it from disk; it is the whole output. The spawned agent was given the item's report-only preamble, the item's lens prompt, the input list and the report path (saved at $Q/prompts/$t-prompt.md; the item's Action text is in the brief). The report's own last lines read: $(tail -3 $Q/$rep | tr '\n' ' '). No other file changed from this task (the prompt file under $Q/prompts/ was written by the orchestrator before the spawn). To judge the item's Verification line: the report must have a ## Checks table with PASS or FAIL per check id, a Verdict: line and a Blocking count: line. A FAIL verdict with findings does not make the item unmet: the item only requires that the report is written.
EOT
bash $D/mkprompt.sh $t 1 1 $D/work/$t/brief.txt $D/work/$t/diff.txt
