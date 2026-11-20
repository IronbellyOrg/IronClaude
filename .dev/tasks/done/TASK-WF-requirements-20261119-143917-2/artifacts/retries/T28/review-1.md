de0715d338437e59660a63100284c3d5b8d4dba6
# Task 28 review 1 (requirements record)

Earlier blocking findings: none (first review).

AC status
- T28.AC1 met. T28.AC1@.dev/releases/backlog/issue-watcher-zero-setup/requirements.md (status column of R1 to R34, read live): R2-R5, R7, R8, R11-R16, R18, R19, R22-R35 = `built`; R1, R6, R9, R10, R17 = `decided (Coder repo)`; R20, R21 = `open`. No R1-R34 row keeps `decided (not built)` or an earlier `open` whose task is done. R36 (outside R1-R34, not a task 1-27 row) stays `decided (not built)`, which fits the owner's withdrawal not yet applied.
- T28.AC2 met. T28.AC2@requirements.md "Built and tested" lines 114-142: one row per Task 1-28 (Task 4a is folded into the Task 4 row), each with a test file and count, or "Docs only" for Tasks 2, 6, 26, 27. I ran `pytest --collect-only` on every named file and every count matches (128, 435, 591, 232, 91, 181, 19, 137, 41, 154, 178, 75, 53, 37, 31, 777, 58, 3925, 134, 14, 21, 43, 34, 26, 27, 27, 16, 4, 42, 78). The final run in /tmp/t28-full.txt ends "10677 passed, 15 skipped in 655.44s", matching the table row.
- T28.AC3 met. T28.AC3: `make verify-sync` printed "All components in sync."; no `.claude/` path is staged.

Other checks, all true against the live repo
- Ledger `.dev/tasks/to-do/TASK-WF-requirements-20261119-143917-2/progress.md` shows T1-T27 `complete verdict=compliant`; T28 started.
- Task 4 observation file `artifacts/t4-updatedat-observation.md` exists.
- Task 26 doc claims hold: `docs/designs/issue-watcher.md:944` is section 19, `docs/designs/issue-watcher-setup.md:708` is section 17.
- Task 27 claims hold: `docs/designs/issue-watcher-zero-setup-coder-handoff.md:28` records `gh auth status` under `env -i` staying logged in; line 14 holds the R20 reproduction step.
- Open decisions section lists R20, R21, the ship-gate flip, the Task 4 outcome and the self-approval choice; `GOVERNED_LEVELS_ALLOWED = False` is live in `src/superclaude/cli/issue_watch/launch.py`. The "R36 safety note" the file cites exists (`amendment-r36-withdraw-r31.md:29`). Coder-repo rows and R33 owner answers are stated.

Findings
F1.1 ac=scope at=.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:50 anchor=`OPEN: the owner said "most", so the pipelines that should end elsewhere are still to be named.` chk=amiss=n,false=y,harm=n,constraint=n family=stale-text fix=drop or mark resolved the "OPEN" sentence in the R24 row (the Open decisions section says all four end at In review, decided 2026-11-19): the R24 row is now `built` but still says an item is open. Non-blocking wording residue; only the status column is in the AC.
F1.2 ac=scope at=.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:23 anchor=`Status values: open, decided, built.` chk=amiss=n,false=y,harm=n,constraint=n family=stale-text fix=add `decided (Coder repo)` to the status vocabulary line. Non-blocking.
