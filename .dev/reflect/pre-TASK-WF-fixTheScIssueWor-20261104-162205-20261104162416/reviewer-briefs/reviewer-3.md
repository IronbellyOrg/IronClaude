# Reviewer 3 brief (persona: refactorer, model class: opus)

Mode: UC-1 pre-execution. Audit the proposed tasklist for structural problems: ambiguous exact-text instructions an executor could copy wrongly, duplication that will drift, wording that contradicts other rules in the same agent files, and edits whose placement is underspecified. Assume mistakes exist. Return findings only (each with file:line evidence, a class from {authorized, necessary, drift, regression} or a grounding gap, severity blocking|minor, and a one-line recommendation), plus a self-reported confidence 0.00-1.00.

Tasklist under review: `.dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/TASK-WF-fixTheScIssueWor-20261104-162205.md` (Read it in full).
Spec: `.dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/source.md`.

## T1 card excerpt

- F4 (byte-exactness risk): the plan's Constraints quote the exact texts inside single-backtick code spans that themselves contain backticks (for example `` `.dev/issues/` `` inside the paragraph). The outer backticks are delimiters, which an executor must infer; a mis-copy would be caught only if the test constant and agent text diverge (both are written from the same plan text, so a consistent mis-copy would pass).
- F5 (duplication): the same rule appears in two places per agent file (early section + Rules pointer) and a third time in SKILL.md; the Rules bullet references the early section by heading text, so a later heading rename would orphan it. The test pins both.
- F6: the identical worker file list includes files a given tier never writes (t3 never writes summary.md); the paragraph scopes it with "every file your job names", so no contradiction.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T16:24:30Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command projectPath=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command

### src/superclaude/agents/issue-worker-t1.md:1-31

Read the whole file (frontmatter, opening paragraph at line 11, jobs 13-20, Rules 22-30). Compare with issue-worker-t2.md and issue-worker-t3.md (t3: jobs 13-19, Rules 21-29).

### src/superclaude/skills/sc-issue-protocol/SKILL.md:52-65

Read this range ("Workers and the spawn rule").

## Coverage slice

| Requirement | Task | Status | Grounding |
|---|---|---|---|
| Exact early section, Rules bullet, SKILL.md line (plan Constraints) | Tasks 1-3 | to audit | plan Constraints section |
