#!/usr/bin/env bash
# review prompt for a SKIPPED conditional item: mkskip.sh Tn item "what was skipped"
D=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/implement/task-rf-sweep-phase1-202-c7ea3265
cd /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
F=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md
t=$1; item=$2; what=$3
bash $D/brief.sh $t >/dev/null
start=$(grep -E "^$t: start sha=" $D/progress.md | sed 's/.*sha=//')
git show $start:$F > $D/work/$t/src-before.md
{ echo "The task (item $item, $what) was skipped because the fidelity gate passed at cycle 0 (F_0 empty). The only change is new row(s) in the Execution Log table of the source file (diff of the source file against the start snapshot):"; diff -u $D/work/$t/src-before.md $F | grep -v '^[-+][-+]' | grep '^[-+@]' | cut -c1-300; echo; echo "Evidence for the skip condition: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/fidelity/fix-log-cycle1.md (it reads "SKIPPED: no blocking findings") and qa/fidelity/consolidated-findings-cycle0.md (F_0 empty, |F_0| 0) and the cycle-0 row of qa/fidelity/cycle-ledger.md. The item's Action says: if item 14.38 wrote SKIPPED (the fix cycle) this item is marked SKIPPED, mark it complete with the SKIPPED note. The checkbox tick of the item itself is done by the orchestrator after the verdict and is not part of this diff."; } > $D/work/$t/diff.txt
bash $D/mkprompt.sh $t 1 1 $D/work/$t/brief.txt $D/work/$t/diff.txt
