# Plan corrections made by the implementer before Task 1 started

Why: the advisory reflect review of this plan (`.dev/reflect/pre-TASK-WF-specWorktreeClea-20261120174527/REPORT.md`, verdict FAIL) found factual defects in the plan text. The managed protocol lets the plan be edited and re-pinned until the first task's `start` line is written, so the fixes were made now, before any task started. Reflect itself never edits a plan; this was done by the implementer, and nothing about the design or the 11 decisions of the spec changed.

| Reflect finding | Correction in the plan |
|---|---|
| M-1 (checks that wait for later tasks; no tests for the fact collectors) | Task 2 now creates `tests/worktree_cleanup/__init__.py`, a first `conftest.py` and `test_runner.py`; Tasks 3 to 5 own `test_facts.py` and save their own fixtures; Task 4's repository helper lives in `conftest.py`; Task 7 only extends and shares them; the "branch kept" check moved to Task 13; checks that name Task 13 (Tasks 2, 5, 11, 12) are declared deferrals of cross-verb tests |
| M-2 (no pull-request step) | Constraints now state that the finishing step of the run opens it with `/sc:pr-submit --monitor 3`; no task does |
| M-3 (14 versus 15 rows) | Task 19 says 15 rows and keeps the spec's own labels beside the closest of the three words |
| M-4 (item 1 fallback) | Task 1 states the spec's item 1 fallback and what the script does because no deregister command is proven; Task 11 reports "removed in git but still listed in Orca" |
| M-5 (open pull request proof) | Task 1 runs the helper on an open pull request as well (or records that none was open) |
| M-8 (command list in the JSON) | Task 12 writes a `commands` list into the `.json` |
| M-9 (denylist runner) | Task 2 makes `check_allowed` a positive allowlist, with the banned shapes as extra refusals |
| INV-004 (item 7) | Task 1 keeps item 7 NOT PROVEN with the note "pending the Task 20 dry run" |
| INV-005 (write-verb classification) | Task 14 names the `WRITE_VERB_CLASSIFICATION` scan |
| INV-009 (Task 20 dependencies) | Task 20 now depends on Tasks 12, 13, 17, 18 and 19 |

Not changed: M-6 (patch-and-bundle manual archive) stays an owner decision; INV-006, INV-007 and INV-008 are carried as implementation notes (no pull-request task; Task 13 adds a test for a new ignored `.dev` file after the save; the registration call for the runner arrives in Task 11).
