# Reviewer 2 brief (persona: qa, model class: haiku)

Mode: UC-1 pre-execution. Audit the proposed tasklist against its driving spec. Find defects: requirements dropped or distorted, tests that would not actually catch the defect, acceptance criteria that cannot be met or verified, and existing tests the planned text would break. Assume mistakes exist. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Return findings only (each with file:line evidence, a class from {authorized, necessary, drift, regression} or a grounding gap, severity blocking|minor, and a one-line recommendation), plus a self-reported confidence 0.00-1.00.

Tasklist under review: `.dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/TASK-WF-fixTheScIssueWor-20261104-162205.md` (Read it in full).
Spec: `.dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/source.md`.

## T1 card excerpt

- All five inferred requirements map: INF-001..003 to Task 2, INF-004 to Task 1, INF-005 to Tasks 1-2.
- Task 1 acceptance requires a red run saved to `./artifacts/t1-red.log` before Tasks 2-3: proof the tests fail on old text without reverting real files (negative tests use tmp_path).
- The new rule text must survive existing scans in tests/skills/test_issue_worker_agents.py: `gh_lines_missing_repo` (lines 31-48; "gh --body-file" has no issue/pr/label token), `skills_lookups_missing_project_copy` (lines 135-148; no `~/.claude/skills/` in new text), `test_no_source_tree_path_or_brace_placeholder` (lines 115-119).

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T16:24:30Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command projectPath=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command

### .dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/source.md:1 (full spec body)

```text
Fix the /sc:issue worker agents so they always write their files: add to each issue-worker-t*.md Rules section a rule that the files they write under .dev/issues/ are input files for the orchestrator's next tool calls (gh --body-file posts, /sc:recommend), not report files, so the general harness note against writing report .md files does not apply to them, and returning the content as text instead is a failure (E-WORKER-NO-OUTPUT). Add a regression test in tests/skills/test_issue_worker_agents.py that every issue-worker agent file carries that rule. Files: src/superclaude/agents/issue-worker-t1.md, issue-worker-t2.md, issue-worker-t3.md, tests/skills/test_issue_worker_agents.py
```

### tests/skills/test_issue_worker_agents.py:1-196

Read the whole file: helpers `gh_lines_missing_repo` (31-48), `split_frontmatter` (51-59), `skills_lookups_missing_project_copy` (135-148), and the existing negative-case pattern `test_skills_lookup_check_fails_on_old_rubric_line` (159-169) that copies an agent file to tmp_path.

### tests/skills/test_issue_protocol.py

Read as needed to check whether the planned SKILL.md line could break it (for example a line-count limit at line 126: `assert len(text.splitlines()) < 500`).

## Coverage slice

| Requirement | Task | Status | Grounding |
|---|---|---|---|
| INF-004 regression test that every agent file carries the rule | Task 1 | covered | source.md:1 |
| INF-005 files in scope | Task 1, Task 2 | covered | source.md:1 |
