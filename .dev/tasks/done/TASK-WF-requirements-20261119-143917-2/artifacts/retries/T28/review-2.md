de0715d338437e59660a63100284c3d5b8d4dba6
# Task 28 review 2 (requirements record)

Earlier blocking findings: none (review 1 had only non-blocking F1.1 and F1.2).

F1.1 resolved (non-blocking). The R24 row in .dev/releases/backlog/issue-watcher-zero-setup/requirements.md no longer holds the "OPEN: the owner said most" sentence; it now ends "Resolved 2026-11-19: all four pipelines end at `In review` (R33 item 5)."
F1.2 resolved (non-blocking). requirements.md:23 now reads "Status values: open, decided, decided (Coder repo) (the Coder repository builds it), built."

AC status
- T28.AC1 met. T28.AC1@requirements.md (status column, read live): R2-R5, R7, R8, R11-R16, R18, R19, R22-R35 = `built`; R1, R6, R9, R10, R17 = `decided (Coder repo)`; R20, R21 = `open`. No R1-R34 row is left as `decided (not built)`. R36 (outside R1-R34) stays `decided (not built)`, which fits.
- T28.AC2 met. T28.AC2@requirements.md "Built and tested" table: one row per task with test file names and counts (unchanged from review 1, where counts were verified by collect-only); the fix pass did not touch them.
- T28.AC3 met. T28.AC3: `make verify-sync` printed "All components in sync." in the live repo.

Other checks: Open decisions section (R20, R21, ship-gate flip, Task 4 outcome, self-approval choice), the R33 decided line and the Coder-rows line are present and unchanged.

Findings: none.
