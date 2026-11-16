# Second author report (plan steps 14.1 and 14.2)

Author: fresh session, claude-sonnet-5-5, 2026-11-15 (UTC). Nothing was staged, committed or pushed. No sub-agent or other model was started.

## Files created

Under `fixtures/recall/` (all paths relative to `.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/`):

- `AUTHORS.md`, `SWAP-NOTES.md`
- one folder per plan, each with `original.md`, `seeded.md`, `seeds.json`, `source.md`:
  - `TASK-WF-diagnosticRefres-20261109-144413/`
  - `TASK-WF-devGuideRefactor-20261104-135403/`
  - `TASK-WF-removeTheAnyIssu-20261102-053741/`
  - `TASK-WF-renameTheScIssue-20261104-174359/`

Edited (only the allowed fields):

- `cards/C1.json` to `cards/C8.json`: the `swap_test` field only.
- `cards/README.md`: the "Swap test (AO-2, REQ-08)" line only; the second-reader line (REQ-38) is untouched and still OPEN.
- `tests/test_cards.py`: the one assertion on `swap_test` (now expects the signed record) plus a one-line comment.

Outside the repository: build and check scripts in `/tmp/second-author-build/` (they write only into `fixtures/recall/` and the card files).

## Seeds (task 14.1)

37 seeds in 4 plans. Plan seed counts: diagnostic refresh 7, developer guide 12, severity rule 11, sc:issue rename 7.

| Class | C1 | C2 | C4 | C5 | C6 | C7 | C8 |
|---|---|---|---|---|---|---|---|
| Seeds | 5 | 7 | 6 | 5 | 6 | 7 | 1 |

Checks run (script, outside the repo): every `original.md` and `source.md` is a byte copy of the package file; every quote in `seeds.json` occurs exactly once in `seeded.md`; the seeded text contains no marker words or comments that the original lacks.

## Swap test (task 14.2)

All eight cards pass (C1 to C8). Reviewer string `second-author-session claude-sonnet-5-5`, date `2026-11-15`, written to each card. No card failed, so `SWAP-NOTES.md` lists no failing card; it holds the one-line reason per card. One observation, not a fail: C5's "plan-unnamed hit" only reads clearly beside the list of hits the sheet shows.

## Test result

Command: `uv run --frozen --project <repo> pytest -p no:cacheprovider <SW>/tests/test_cards.py <SW>/tests/test_readme.py <SW>/tests/test_lint.py -q -m 'not freeze'`

Result: 20 passed, 1 deselected (the freeze-marked test), 0 failed, 0.71 s.

## What I could not do or could not confirm

- **Class C8 has one seed.** I found only one test that pins an edited file, existed before the plan ran, and that the plan never names or runs (the composite invariant test in the severity-rule plan). The E3 recall figure will rest on one seed; more C8 seeds, or a fifth plan with edits to test-pinned files, would be needed for a meaningful figure.
- **Overlap with the hold-out set was not checked** (I cannot know it). If one of the four plans is a hold-out or planted-set document, remove its folder.
- **Class C3 is not seeded** (not in the requested list).
- **The repository is newer than the plans.** All four plans are finished and their results are already in the repository, so a reviewer who opens the repository may see the finished state. Every seed is meant to be visible from the plan text or its source alone.
- **Some seeds fit two classes** (for example, a check wider than its instruction that also cannot pass); each has one label in `seeds.json`.
- **The original plans carry defects of their own.** Reviewers may report them; they count against precision.
- I did not run the freeze marker or any extractor, by instruction, so I do not know which seeds the extractors find.
