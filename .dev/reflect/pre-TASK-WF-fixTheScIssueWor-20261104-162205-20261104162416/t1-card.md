# T1 reflection card (UC-1, pre-execution)

Spec: `.dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/source.md`
Tasklist: `.dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/TASK-WF-fixTheScIssueWor-20261104-162205.md`
Coverage: `artifacts/coverage-matrix.md` (5/5 inferred rows mapped; 0 parsed IDs).

## Root-cause / deviation section (analyzer)

- F1 (scope vs source): the plan adds an early section in each agent file and one line in `src/superclaude/skills/sc-issue-protocol/SKILL.md` ("Workers and the spawn rule", after SKILL.md:64). Neither is in source.md:1, which asks only for a Rules-section rule plus a test. The plan's Constraints attribute the expansion to a coordinator follow-up message (retry on #365 still skipped summary.md). Candidate class: authorized expansion, authority recorded only in plan prose (not in source.md).
- F2 (placement): source.md:1 says "add to each issue-worker-t*.md Rules section a rule that ... not report files ... returning the content as text instead is a failure (E-WORKER-NO-OUTPUT)". The plan's Rules bullet is a short pointer ("Write your files ... never return its content as text") and the full statement, including the harness-note exemption and `E-WORKER-NO-OUTPUT`, lives in the new early section. Candidate class: necessary deviation (coordinator asked for early placement, "not only in Rules").
- F3 (`flags-user.md` excluded): the coordinator's list names `flags-user.md`, the plan omits it, citing src/superclaude/skills/sc-issue-protocol/refs/create.md:32 (the orchestrator writes it; t1 must not read it). Grounded.

## Coverage / acceptance section (qa)

- All five inferred requirements map: INF-001..003 to Task 2, INF-004 to Task 1, INF-005 to Tasks 1-2.
- Task 1 acceptance requires a red run saved to `./artifacts/t1-red.log` before Tasks 2-3: proof the tests fail on old text without reverting real files (negative tests use tmp_path).
- The new rule text must survive existing scans in tests/skills/test_issue_worker_agents.py: `gh_lines_missing_repo` (lines 31-48; "gh --body-file" has no issue/pr/label token), `skills_lookups_missing_project_copy` (lines 135-148; no `~/.claude/skills/` in new text), `test_no_source_tree_path_or_brace_placeholder` (lines 115-119).

## Structural / tech-debt section (refactorer)

- F4 (byte-exactness risk): the plan's Constraints quote the exact texts inside single-backtick code spans that themselves contain backticks (for example `` `.dev/issues/` `` inside the paragraph). The outer backticks are delimiters, which an executor must infer; a mis-copy would be caught only if the test constant and agent text diverge (both are written from the same plan text, so a consistent mis-copy would pass).
- F5 (duplication): the same rule appears in two places per agent file (early section + Rules pointer) and a third time in SKILL.md; the Rules bullet references the early section by heading text, so a later heading rename would orphan it. The test pins both.
- F6: the identical worker file list includes files a given tier never writes (t3 never writes summary.md); the paragraph scopes it with "every file your job names", so no contradiction.

## Self-reported confidence: 0.90 (to be re-graded blind)
