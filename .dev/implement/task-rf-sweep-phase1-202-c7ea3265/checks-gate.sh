#!/usr/bin/env bash
# T21: list the check ids of every qa-*-report.md in qa/${GATE:-r3-b1} with PASS or FAIL (read-only).
cd /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/${GATE:-r3-b1} || exit 1
for f in qa-*-report.md; do
  awk -v F="${f%.md}" '
    /^## Checks/ {on=1; next}
    on && /^## / {on=0}
    on && /^\|/ {
      n=split($0, c, "|");
      id=c[2]; gsub(/^ +| +$/, "", id);
      if (id !~ /^C[0-9]+$/) next;
      res=""; for (i=n-1;i>=3;i--) { t=c[i]; gsub(/^ +| +$/, "", t); if (t ~ /^(PASS|FAIL)/) {res=(t ~ /^PASS/)?"PASS":"FAIL"; break} }
      printf "%s\t%s\t%s\n", F, id, res
    }
  ' "$f"
done
