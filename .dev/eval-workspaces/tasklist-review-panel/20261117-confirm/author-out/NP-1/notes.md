# NP-1 notes (plan TASK-WF-implementTheDesi-20261031-182028, candidate C7)

## Why the plan counts as the reviewed text
The report (`.dev/reflect/pre-TASK-WF-implementTheDesi-20261031-182028-shadow11/`) reviewed the plan under `.dev/tasks/done/`, not a to-do copy. Every plan line it cites says what the report says: plan:32-35 (EventType count 41), :44, :61, :91, :95, :102-106, :147, :150. The plan's own ledger hash (progress.md line 2, sha256 1f84077e...) equals the sha256 of candidate.md.

## Findings dropped
- M-008 (absolute EventType count 41 is stale, repo now has 45): the report itself says it is time-relative and "not a defect of the original 2026-10-31 execution". At base the enum has 39 members, so "39 to 41" is right when the plan was written.
- M-009 (no AC for the design's active-without-completion timeout path): calibrated only 0.55, and Task 8's AC already lists "incomplete combinations" of the merge table, so the gap is partly covered. Too doubtful to list.
- The dropped evidence citation (progress.md:12-13 for M-001): the report dropped it; M-001 is kept because it stands on plan:44 and design:434-437, both re-read by me.
- Code defects found at implementation time (FINAL 1 false comments in detection.py and SKILL.md:269; CHANGELOG wording; docstrings; T3 extra watermark key; T7 created_at fallback; T10 coverage gap): defects of code or docs written during implementation, not of the plan text.

## Severity of the kept items
- GT1 is the only item graded blocking at implementation time: `artifacts/retries/T2/review-1.md:4` has `F1.1 sev=blocking ... ac=T2.AC2` on the plan:44 wording, and progress.md shows T2 "blocked" followed by a coordinator Ruling that overrode plan line 44.
- GT2 to GT8: the report labels M-001 to M-007 "MAJOR" and M-010 "MINOR". It never uses the word "blocking" for them, and no implementation-time review graded them blocking, so `blocking_in_implement` is false. A reader who counts a MAJOR finding that names a wrong build outcome as blocking would raise GT2 to GT7.

## Could not be verified / caveats
- **Base commit.** `start sha=` lines in progress.md are git tree ids from the executor's snapshot, and the first one (34f8e91c...) is not in this repository at all (`git cat-file -t` fails). Base is therefore the first parent of the squash commit that shipped the plan: d4ac8a3d9 has parent 75d0d1e2c23d3abfa60a075ec0c85b4f9b1e047a (a commit, 2026-10-31 18:09:58Z). The ledger was created 2026-10-31T19:14:27Z, after that commit, and no commit sits between it and d4ac8a3d9. I could not prove the executor's checkout was exactly that commit.
- At base, every file the plan edits exists (models.py, detection.py, run_log.py, classifier.py, severity_router.py, `pr_submit/__init__.py`, test_run_log.py, SKILL.md, commands/pr-submit.md, CHANGELOG.md, both release guides). The files the implementation created (reviewers.py, tests/pr_submit/test_codex_reviews.py, three fixtures) do not exist at base, so `masked_paths` is `[]`.
- **The design file is not at base.** source.md says to implement `.dev/pr-submit-codex/design/pr-submit-codex-design.md`. That file was untracked while the work ran and first enters git in d4ac8a3d9 (`git log --all` shows no earlier commit). A sandbox rebuilt from base will not contain it, so GT1 to GT7 and GT8 (which cite design section 18 lines 434-479 and 378-379) cannot be found from the repo alone. Read it with `git show d4ac8a3d9:.dev/pr-submit-codex/design/pr-submit-codex-design.md`.
- The design's section 18 amendments (A0 to A6) were added after an earlier review of the same plan and before the reviewed text was frozen; the plan was never updated to match them. That is the root of GT1 to GT7.
- Running `uv run python` from inside the repository root rebuilt the editable `superclaude` package in the repo's virtualenv (uv printed "Built/Uninstalled/Installed 1 package"). No tracked file was written by me, but I did not run `git status` (not in the allowed command list), so I cannot rule out an untracked build artefact.
