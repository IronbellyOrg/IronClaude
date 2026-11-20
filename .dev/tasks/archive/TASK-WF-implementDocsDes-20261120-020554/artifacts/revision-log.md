# Revision log 1 (surgical edit of TASK-WF-implementDocsDes-20261120-005507)

Original plan sha256: d4c233ede3218a6fc00d9ee3bc92f8e65b4696caf0f10772166ef9a4c769d5fa (byte copy in ./old-plan.md; the archived original is unchanged).
Edits were made with the Edit tool on a copy in /tmp, 31 calls, one finding group per call group. Only blocking findings (B1 to B12 of the review report, ./prior-findings.md) and the same-spot Medium wording were touched.

| Finding | Edit |
|---|---|
| B1 plugin command mirror and test | Constraints mirror rule names `commands/workflow.md`; Task 8 mirrors the file, updates `argument-hint`, adds the `cmp` and `tests/commands` criteria |
| B2 git-HEAD tests | Task 2 rewrites the two tests in `test_shadow_skill_contract.py`; new acceptance bullet |
| B3 id recorded before placement | Task 4 gains `reserve`; `archive` and `place` take the reserved id; test for a collision suffix |
| B4 gate on the copy | Task 4 `prepare` renames the copy and rewrites `slug` to the reserved id; Task 5 states the order |
| B5 Task 13 check | Acceptance names the two packages the grep really returns; the 20261116 package has no contract |
| B6 no Agent tool | Task 6 adds the Agent tool to `allowed-tools` and limits the fan-out ban |
| B7 Wave 5 target | Task 6 makes Wave 5 write to the final placed package |
| B8 no writer for fields | Task 4 adds `mark` |
| B9 Revision section and artifacts | Task 4 `place` writes them |
| B10 unknown replacement id | Task 4 `archive --superseded-by none`; Task 13 uses it for six packages |
| B11 lint version | Task 2 accepts 1.8.0 and 1.9.0 |
| B12 plugin mirror of new files | Constraints and Task 6 mirror the new ref and script, creating `scripts/` |
| Mediums folded in | restore undo, stdlib-only script, test-pinned wording in Task 7, `qa.md` STOP list in Task 9, 4.3a sentence in Task 1, panel mapping of medium and note, forced regenerate order, Task 10 dependency on Task 7, counts source in Task 5 |
