# Calibration of reviewer-2 card (blind calibrator, opus alias)

Calibrated C = 0.79 (Citation grounding 0.85, Coverage completeness 0.80, Deviation-classification clarity 0.80, Risk surface coverage 0.75, Recommendation actionability 0.75). Below 0.85. No citation failed to verify.

All ten rows (all graded Blocking by the reviewer) checked:
- Rows 1, 2 (for the `/sc:git` side), 3, 4, 6, 7: true.
- Row 5: true that existing tests run `git branch -d` through argv lists (`tests/worktree_cleanup/test_git_facts.py:211,217`); "cannot pass literally" UNVERIFIED (depends on whether Task 24's scan detects argv-list forms). FR-081 (REQ:631) limits the scan to new code.
- Row 8: true; Blocking only by the letter of the rule (nothing named reads `header_len`, `rule`, `runs`, `segments`).
- Row 9: partly true: the 40-line cap has no acceptance check, but "no implementation instruction" is overstated because PLAN:334 cites FR-054 to FR-067, which includes FR-064, and PLAN:252 cites FR-064.
- Row 10: true; the weakest Blocking grade (changes how the executor works, not a deliverable or an acceptance check).
- Row 1's HIGH label is generous (most readers take "uses" to mean "runs"); Blocking grade stands because fixing the rule text changes it.

Misses the calibrator found: T-12 "Will Not" text has no acceptance check in Task 19 (PLAN:235); T-07 write-side cases (REQ:670: the `--url` repeat rule, the FR-045 two-path partial failure, the `submodule.recurse` warning) are not asserted by Tasks 7, 8, 23.
Not checked by the calibrator: the reviewer's id dispositions and the 191/170 counts.
