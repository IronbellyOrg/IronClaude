# HO-2 notes

Plan sha256 5ba3dd1b... equals the plan hash in the report's input-snapshot.yaml and the ledger. The report's plan line cites (:20, :37, :40, :58, :64, :73, :95) were checked and match the copied plan.

## Included (10)
B-1..B-4 (blocking, GT1-GT4); non-blocking GT5-GT10: R1-F4, R1-F6, R1-F7, R1-F8, M-CONSTRAINTS, R1-F10.
- R1-F4 is `blocking_in_implement: false`: REPORT.md and merged-verdict.yaml grade it minor. Note that artifacts/amendments.md AMD-03 (grade blocking) lists R1-F4 beside M-SCANNER, covering its continuation half. I followed the finding's own grade.
- M-CONSTRAINTS and R1-F10 are outside the "R1-F3..F8" range given in the brief but are listed in REPORT.md's minor findings and verified in the plan (:20 vs :120; :92).

## Dropped (not plan defects, or not requested)
- R1-F3: the plan's `uv run --no-project python` is kept by the review ("refinement, keep"); the finding asks only for a note. Wording.
- R1-F9 (CHANGELOG scope addition): scope remark, not a wrong build.
- R1-F11 (timing case vs 128 KB limit), M-TASK7 (bypassPermissions), M-HEREDOC-TEXT, M-ARRAY, M-CEILINGS, M-AWK-LOCALE: documented minors, left out to keep the set strict (they refine design choices of the implemented scanner or live check).
- M-COVERAGE: a defect of the review's coverage matrix, not of the plan.
- Report grounding gaps G-1, G-2 (dropped by the report itself).
- amendments.md AMD-06..AMD-08 map to the dropped minors above.

## Base
`start sha=0f91559c...` is a tree object. Base = HEAD in artifacts/retries/T1/q0-head: 119622e3a78284f83377f920e3858f864ac7e6c6 (commit, ancestor of implementing commit 605da2ffb). The plan folder is untracked there (present only in the tree snapshot; the tree has it under .dev/tasks/to-do/). masked_paths: [] (nothing the implementation added exists at base).
