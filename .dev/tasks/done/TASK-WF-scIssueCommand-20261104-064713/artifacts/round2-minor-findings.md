# Round-2 minor findings: disposition in this run

Source: `.dev/reflect/pre-TASK-WF-scIssueCommand-20261104-064713-20261104081732/REPORT.md` (18 minor, 0 blocking).
Rule: coordinator constraint C4 (`./coordinator-constraints.md`): apply a minor only when it is a correctness fix inside the task being implemented; log every other one as not applied. C1, C2 and C3 cover F-14, F-01 and F-02/F-06/F-11/F-12.

| Finding | Disposition | Task | Reason |
|---|---|---|---|
| F-01 | applied via C2 | 1, 6, 17 | URL-vs-origin check (`E-FOREIGN-REPO`) added to `origin_repo.py` with the listed unit tests; Wave 0 calls it; item 4 verified by those tests; no live run |
| F-02 | applied via C3 | 15, 17 | Task 15 single exit is pending; runbook at the end of Task 17's artifact |
| F-03 | applied | 3, 5, 6, 7 | correctness: every `gh issue/pr/label` mention, prohibitions and the error table included, is written with `--repo <R>` so the fork-safety scan Task 7 requires passes; the placeholder rule is written without the literal brace token |
| F-04 | not applied | 16 | Task 16 is pending under C3, so no live comparison method is needed in this run |
| F-05 | applied (tests only) | 2 | correctness: an exported `CLICKUP_MAX_PAGES` or `CLICKUP_LIST_IDS` would change the page-cap and URL tests, so every test clears all four `CLICKUP_*` variables. The plan:23 wording change is not applied (plan text, not delivered code) |
| F-06 | applied via C3 | 17 | items 1, 2, 3, 5 (first half), 6 and 8 recorded pending; runbook ends with the pre-approval request |
| F-07 | not applied | 17 | dependency metadata only; this executor runs tasks in source order, so Task 15 and 16 finish before Task 17 anyway |
| F-08 | applied | 17 | correctness of the acceptance record: item 5's first half is recorded pending, not run on the script-only `no_token` output |
| F-09 | not applied | 4, 7 | adding a new test is an addition; the template itself starts with the `/model` line as Task 4 already requires, and item 8 stays pending |
| F-10 | not applied | 7 | a new `gh api` path assertion is an addition beyond Task 7's listed tests |
| F-11 | applied via C3 | 16 | Task 16 pending; `CLICKUP_LIST_IDS` named in the runbook |
| F-12 | applied via C3 | 17 | item 4's live run is pending in the runbook; item 4 itself is verified by the C2 unit tests |
| F-13 | applied | 2 | correctness: exit 2 is reserved for bad arguments, so a non-positive or non-integer `CLICKUP_MAX_PAGES` falls back to 20 and the run continues (exit 0); documented in the docstring and tested |
| F-14 | applied via C1 | 3 | no `permissionMode` in the three worker files; the test asserts it is absent |
| F-15 | not applied | 15 | Task 15 pending under C3; the runbook names the evidence rule |
| F-16 | applied | 7 | correctness: the inventory covers `refs/*.md`, `templates/*.md`, `scripts/*.py` only, so `scripts/__pycache__/` cannot fail it |
| F-17 | applied | 6, 8 | correctness: one exact D26 sentence is used in `SKILL.md` and `commands/issue.md`, and the Task 8 test pins that sentence |
| F-18 | applied | 4, 5 | correctness: Wave 2 must STOP `E-NOT-AN-ISSUE` on a pull request number (source.md:159) but decides from `scout.md` alone, so the scout claim section records `url` and `is_pull_request`, and `refs/claim.md` Wave 2 reads it |
