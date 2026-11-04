# Reviewer 1 brief (persona: analyzer, model class: sonnet)

Mode: UC-1 pre-execution. Audit the proposed tasklist against its driving spec. Find defects: requirements dropped or distorted, unsupported claims, scope drift, and tasks whose acceptance criteria cannot be met as written. Assume mistakes exist. Return findings only (each with file:line evidence, a class from {authorized, necessary, drift, regression} or a grounding gap, severity blocking|minor, and a one-line recommendation), plus a self-reported confidence 0.00-1.00.

Tasklist under review: `.dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/TASK-WF-fixTheScIssueWor-20261104-162205.md` (Read it in full).
Spec: `.dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/source.md`.

## T1 card excerpt

- F1 (scope vs source): the plan adds an early section in each agent file and one line in `src/superclaude/skills/sc-issue-protocol/SKILL.md` ("Workers and the spawn rule", after SKILL.md:64). Neither is in source.md:1, which asks only for a Rules-section rule plus a test. The plan's Constraints attribute the expansion to a coordinator follow-up message (retry on #365 still skipped summary.md). Candidate class: authorized expansion, authority recorded only in plan prose (not in source.md).
- F2 (placement): source.md:1 says "add to each issue-worker-t*.md Rules section a rule that ... not report files ... returning the content as text instead is a failure (E-WORKER-NO-OUTPUT)". The plan's Rules bullet is a short pointer ("Write your files ... never return its content as text") and the full statement, including the harness-note exemption and `E-WORKER-NO-OUTPUT`, lives in the new early section. Candidate class: necessary deviation (coordinator asked for early placement, "not only in Rules").
- F3 (`flags-user.md` excluded): the coordinator's list names `flags-user.md`, the plan omits it, citing src/superclaude/skills/sc-issue-protocol/refs/create.md:32 (the orchestrator writes it; t1 must not read it). Grounded.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T16:24:30Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command projectPath=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command

### .dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/source.md:1

```text
Fix the /sc:issue worker agents so they always write their files: add to each issue-worker-t*.md Rules section a rule that the files they write under .dev/issues/ are input files for the orchestrator's next tool calls (gh --body-file posts, /sc:recommend), not report files, so the general harness note against writing report .md files does not apply to them, and returning the content as text instead is a failure (E-WORKER-NO-OUTPUT). Add a regression test in tests/skills/test_issue_worker_agents.py that every issue-worker agent file carries that rule. Files: src/superclaude/agents/issue-worker-t1.md, issue-worker-t2.md, issue-worker-t3.md, tests/skills/test_issue_worker_agents.py
```

### src/superclaude/agents/issue-worker-t2.md:9-31

Read this range: opening paragraph (line 11), `## Jobs for this tier` (13-20), `## Rules` (22-30) with the `**Writing only under `.dev/issues/`.**` bullet at line 26 and the `**Return value.**` bullet at line 30. t1 and t3 have the same structure (t3's Rules start at line 21).

### src/superclaude/skills/sc-issue-protocol/SKILL.md:52-65

Read this range: "Workers and the spawn rule"; line 64 is the paragraph starting "Workers make read-only GitHub and git calls" that ends "retried once, then STOP `E-WORKER-NO-OUTPUT` with the expected path."

### src/superclaude/skills/sc-issue-protocol/refs/create.md:32

Read this line: the orchestrator writes `<D>/flags-user.md`, `issue-worker-t1` writes `<D>/flags-t1.md`.

## Coverage slice

| Requirement | Task | Status | Grounding |
|---|---|---|---|
| INF-001 Rules-section rule: files are tool inputs, not reports | Task 2 | covered (placement split, F2) | source.md:1 |
| INF-002 harness note does not apply | Task 2 | covered (early section only) | source.md:1 |
| INF-003 text return is a failure (E-WORKER-NO-OUTPUT) | Task 2 | covered (early section only) | source.md:1 |
