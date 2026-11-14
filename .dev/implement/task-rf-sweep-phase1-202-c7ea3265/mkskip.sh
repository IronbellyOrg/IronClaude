#!/usr/bin/env bash
# review prompt for a SKIPPED conditional item: mkskip.sh Tn item "what was skipped"
D=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/implement/task-rf-sweep-phase1-202-c7ea3265
cd /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
F=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md
t=$1; item=$2; what=$3
bash $D/brief.sh $t >/dev/null
start=$(grep -E "^$t: start sha=" $D/progress.md | sed 's/.*sha=//')
git show $start:$F > $D/work/$t/src-before.md
{ echo "The task (item $item, $what) was skipped because cycle 1 of the ${GATE:-r3-b1} gate passed. The only change is new row(s) in the Execution Log table of the source file (diff of the source file against the start snapshot):"; diff -u $D/work/$t/src-before.md $F | grep -v '^[-+][-+]' | grep '^[-+@]' | cut -c1-300; echo; echo "Evidence for the skip condition: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/${GATE:-r3-b1}/cycle1-decision.md (its outcome line reads PASS at cycle 1, and it lists the skipped items) and the cycle-1 row of .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/${GATE:-r3-b1}/cycle-ledger.md (line 4). The item's Action says: if item 2.21 or 2.18 marked this item SKIPPED, mark it complete with the SKIPPED note. The checkbox tick of the item itself is done by the orchestrator after the verdict and is not part of this diff."; } > $D/work/$t/diff.txt
bash $D/mkprompt.sh $t 1 1 $D/work/$t/brief.txt $D/work/$t/diff.txt
