# Round 2 — Card 1 (analyzer) rebuttal

(a) Partly rebut. F2 is an omission finding: its proof is the AC text at plan:70 plus the verified absence of any pid-capture step across the full T1-T5 step list. The negative half is exhaustive by construction, not "a single quote." The medium severity stands — an executor cannot demonstrate T4.AC4 without inventing a baseline step.

(b) Concede both. I did not trace remediation-source hardening (Card 2 F1) or diff plan text against HEAD (Card 3 F1); my executable-artifact lens covered neither. Real gaps. Card 3's argument that HC5 is discharged by this very audit means Card 2's F1 half-stands (HC1); my miss is unchanged.

(c) Counter-evidence on X-001. Card 3's inference smuggles category into severity: "Necessary deviation" explains why the executor diverged; it does not grade the plan defect. The defect is an AC unmeetable as written plus a contrary claim at plan:82, proven by t5-checks.log:28. One successful improvisation is survivorship evidence — the next executor in a fresh worktree hits the same drift with no planned step, and Card 2's own F2 text concedes exactly that fresh-worktree failure.

Updated assessment. X-001 resolves at MEDIUM: above MINOR (unmeetable AC, false plan claim, recurrence risk), below MAJOR (landed outcome correct; the deviation was detected and fixed in-run). Card 2 already concedes toward medium — the panel converges there.

New evidence. None.
