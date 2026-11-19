# Text-defects phase notes (plan Phase 3)

## RB-22 (wide blank band after the id column), spec step 2.6: not applied, deferred (Low row)

Measured at the start of the phase on the `ledger` screen, `base` fixture (`scores/baseline.md`): the longest blank run inside a row is 18 cells at 160 columns (threshold N), 48 at 116 and 34 at 80, so RB-22 fails at 116 and 80.

Why step 2.6 was not applied: the step gives `line` and `short` the full-width id rule (`22 + min(extra, 26)`, rest to the flags column). Worked from the formulas in `_columns`:

- at 116 columns the id column would go from 52 to 48 cells (blank run about 43, still above 18);
- at 80 columns it would go from 38 to 42 cells (a wider band, not a narrower one).

Reaching N = 18 needs an id column of about 22 cells, which would cut the long identifiers of the `long-identifiers` fixture with `>` in the list. The spec marks the step optional and the row Low, and a Low row may be logged as deferred. RB-22 is deferred with this reason; the rule that column widths stay static between refreshes (finding M-17) is untouched.

## Phase 3 gate (tasks 10 to 16), all runs in `artifacts/gates/p2/`

Both sub-gates (2a and 2b) were run as one gate after Task 16; iteration 1 failed RB-24 (116, 80), RB-28 (80) and RB-29 (116, 80); iteration 2 passed every in-scope High and Medium row at 160, 116 and 80.

- RB-22 after the space diet: the harness measures a longest blank run of 44 cells at 116 and 25 at 80 (N = 18). The row is Low and stays deferred: the long runs sit between a short fixture id and the next column, and the status column now grows to the widest status shown (a merged status is never cut), so a narrower id column would cut real ids. Reviewers recorded it as out of scope; the script row says fail.
- Rubric conflict, RB-12 versus RB-28: RB-12 (heading and rule at 116 and 80) was scored when it was written; Task 15 and RB-28 then removed the rule row under the heading. The footer rule stays (RB-20). Reviewers scored RB-12 as the heading with no rule row.
- Harness changes to follow the spec (rubric wording untouched): the `(no source)` tail is dropped from the screen count (2.9 (c)); the desk starts with `age <age>` and has no message id (2.9 (d)); desk labels are plain and aligned (2.13); RB-19 is replaced by RB-27 (2.12); script checks were added for RB-24, RB-25, RB-26 and RB-28.
- Plan wording that cannot hold as written (recorded, not blocking): the trailing-hash fixture keeps its four-line cut with `...` only at 80 columns (stripped it is 327 characters and fits four lines at 116 and 160); the selected list row is a strict prefix of the question text ending in `>`, so the string census passes on the whole text but a reviewer may read the prefix as a second mention.
- The worktree note moved to the worker inspector (shown only when the questions are on).
