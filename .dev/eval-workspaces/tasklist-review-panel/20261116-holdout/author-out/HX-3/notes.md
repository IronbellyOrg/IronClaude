# HX-3 notes

## Which report
- Earlier report `pre-TASK-WF-scIssueCommand-20261104-064713-20261104070955`: its snapshot lists the plan with sha256 eb19aa0f..., but the plan file is e54e8903.... It reviewed a different plan version, so it was NOT used and none of its findings were taken.
- Later report `...-20261104081732`: plan sha256 e54e8903... equals the plan file (version 2); source sha256 043015b3... equals source.md. Used.

## Kept (12 of 18)
F-01, F-02, F-03, F-05, F-08, F-09, F-10, F-11, F-13, F-14, F-16, F-18. All are minor in the report (the report has 0 blocking findings), so `blocking_in_implement` is false for every item.
- The executor's `artifacts/round2-minor-findings.md` shows F-01, F-02, F-03, F-05, F-08, F-11, F-13, F-14, F-16, F-18 were applied as corrections during implementation, which supports them as real defects of the plan text. F-09 and F-10 were logged as not applied, but each was checked against source.md (474 and 319) and the plan text, and both are real omissions.
- Source lines were read for F-01 (143, 470), F-03 (336, 340), F-08 (471), F-09 (474), F-10 (319), F-11 (298, 304-309), F-13 (310) and F-18 (148, 154, 159). F-14 was confirmed: `src/superclaude/agents/evidence-validator.md:8` has `permissionMode: plan` at base.

## Dropped (6 report findings, plus 1 implementation record)
- F-04 (Task 16 comparison method): Task 16 ended pending, and the finding is about a live run method, not a build error.
- F-06 (no trigger for 'approval at that moment'): overlaps F-01, F-02 and F-11. Kept out to avoid duplicates.
- F-07 (Task 17 depends only on Task 14): metadata only for this executor, and the report says so.
- F-12 (item 4 needs a post-Task-13 session): overlaps F-01 and F-02.
- F-15 (tier proxy may rewrite the model name): the transcript side is tagged [INFERRED] in the report and not verified.
- F-17 (D26 sentence unpinned): wording-level.
- T1 review-1 F1.1 (blocking): scheme-less claim URLs get the wrong error code. This is a defect in code written during implementation, not in the plan text. It concerns the URL check that was added because of F-01, which is why F-01 is NOT marked blocking.
- The report's evidence-validator drops G-001 and G-002 are citation problems in the report, not plan defects.

## Base commit
- The `start sha=` lines are tree objects. Tree 55c06cba equals commit 119622e3 plus the untracked plan folder, `docs/designs/sc-issue-command.md` (the source) and some handoff files. 119622e3 is used as base.
- `masked_paths` is `[]`: every file the implementation created (sc-issue-protocol, issue-worker agents, `commands/issue.md`, new tests) is absent at base (checked with `git ls-tree`).

## Not verified
- Quote F-18 relies on the report's statement that an open pull request reports `OPEN`; `gh issue edit` on a pull request number is UNVERIFIED in the report and was not run.
