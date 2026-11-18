# Targeted independent check of plan revision 2 (2026-11-18)

Checker: a fresh read-only reviewer agent (reflect-reviewer class, alias opus) that did not write the plan or its revision. It re-read the plan, the diff, the review report and the cited repo lines. It ran no tests and did not check this contract file or the other files in artifacts/.

Verdict on the first draft of revision 2: PASS, no blocking defect, 5 medium findings and 4 notes. Findings M1 to M12 and recommendations R-001 to R-005 were each fixed or recorded. The new stop-rule text agrees across Tasks 3, 4, 5 and 7 and with the Constraints; it keeps `test_st2_pipeline_and_submit_stop_rules_come_after_the_old_ones` and `test_no_source_tree_path` passing; the quoted lines the edits point at all exist once.

Medium findings and what was done (all applied to revision 2 before it replaced revision 1):
1. Task 7 left the Impact cell of the architecture reference row (line 1557) saying a bare `--submit` is allowed by reading: added to Task 7 and to its acceptance check.
2. Task 8 gave line numbers 66, 78, 87 without naming the file: now names `docs/designs/sc-issue-claim-pipeline-flag.md`.
3. Task 8 would have put a plain line under a table row at `docs/designs/sc-issue-command.md` line 238: now a bullet in its Notes list after the line 248 bullet.
4. Task 4 did not say where an already-launched level is read: now the `launch` entry of `.dev/issues/<N>/worktree.json`.
5. `docs/designs/sc-issue-claim-pipeline-flag.md:274` still stated the old `--submit` condition: Task 8 now adds a note beside it.

Notes applied: Task 1 acceptance now points at the `Plan boundary` rule in `refs/claim.md`; Task 8 acceptance refers to lines "as they were before the edit"; Task 10 now depends on Tasks 1 to 9; Task 4 also covers Wave 8 in SKILL.md (line 92).

The second draft was not re-reviewed by a second checker; its edits are the five fixes and four notes above, listed in artifacts/plan-rev1-to-rev2.diff.
