# Round 2 — Card 2 (qa) rebuttal

(a) Accept MEDIUM. Card 1's counter to Card 3's survivorship argument is correct: a deviation taxonomy explains what happened; it does not grade the plan defect. X-001/C-001 is an AC unmeetable as written (t5-checks.log:28), a contrary claim at plan:82, and guaranteed recurrence in any fresh worktree. My own F2 text already conceded the fresh-worktree failure. MINOR was understated; withdrawn.

(b) Accept the narrowing, keep the finding. HC5 is discharged by this very review process — flagged in Round 1 — so F1's scope halves to HC1 only: a Pipeline Hardening requirement absent from both the coverage matrix and the tasklist. Still an untraced spec requirement, no longer "the largest coverage hole."

(c) Concede. My meetability line was proven only in the fixture environment (stderr is a file, isatty() False). Task 3 alone satisfies the plan's ACs as written, but it certifies nothing about tty-path behavior — which strengthens Card 3's F1 (an uncovered behavior branch), not mine.

Updated assessment. F1: HC1-only, MEDIUM (scope halved). F2 (verify-sync): MEDIUM, aligned with Card 1. F3: unchanged, MINOR. Meetability analysis: environment-conditional, demoted to context. A-001/A-002 accepts stand.

New evidence. None.
