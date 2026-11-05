# Reviewer 3 brief — persona: refactorer (model class: opus)

Mode: UC-1 pre-execution. Audit the proposed tasklist `.dev/tasks/to-do/TASK-WF-renameTheScIssue-20261104-174359/TASK-WF-renameTheScIssue-20261104-174359.md` against its spec `.dev/tasks/to-do/TASK-WF-renameTheScIssue-20261104-174359/source.md`. Lens: structure and test design. Check whether the regression test in Task 3 is deterministic, would really fail on the pre-fix text, and would catch a future re-introduction of a blocked name; check the exact-text coupling between Task 2 and Task 3. Classify each finding (authorized | necessary | drift | regression, or grounding gap), grade it blocking or minor, and cite file:line for every claim. Read-only: return findings as text; do not write files.

## T1 card excerpt

- Task 3's `written_md_names` scans every `.md` code span in agent files, SKILL.md and refs, a superset of "files a worker is told to write" (it also picks up `SKILL.md`, `CLAUDE.md`, `ISSUE-HANDOFF.md`). None of those match the harness regex today, so the superset is safe and deterministic; a future reference like `REPORT.md` in a ref would fail the test even if no worker writes it (false positive risk, acceptable).
- The negative test keeps the old paragraph as a literal; the red log runs the checker against ./artifacts/pre/ copies. Real files are never reverted (meets the coordinator constraint).
- The tool-input paragraph text is pinned once in Constraints and reused verbatim by Task 2 and Task 3, so the agent files and `_TOOL_INPUT_PARAGRAPH` cannot drift.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T17:46:40Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command projectPath=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command

### tests/skills/test_issue_worker_agents.py:199-235
(the fix-2 constants `_TOOL_INPUT_HEADING`, `_TOOL_INPUT_PARAGRAPH`, `_TOOL_INPUT_RULES_BULLET`, `_SPAWN_PROMPT_LINE`, `_WORKER_FILES` — Read the range.)

### tests/skills/test_issue_worker_agents.py:246-260
(`tool_input_rule_problems`: requires the heading before `## Jobs for this tier` and the paragraph exactly once.)

### src/superclaude/commands/issue.md:62-70
(the `## Outputs` table; claim row at line 68 lists `summary.md` and `analysis/`.)

### src/superclaude/skills/sc-issue-protocol/refs/claim.md:58-59
```markdown
- when `out_of_date`: runs `/sc:analyze` on the paths the issue touches (`--depth deep` when complex, no `--depth` otherwise) and saves the report under `<D>/analysis/`;
- always writes `<D>/summary.md` from `templates/summary.md`: ...
```

## Coverage slice

| Requirement | Task | Status | Grounding |
|---|---|---|---|
| INF-005 analysis/ file names avoid analysis/report/summary/findings | Task 3 (also Tasks 1, 2) | covered | source.md:1 |
| INF-007 deterministic regression test against the harness regex | Task 3 | covered | source.md:1 |
| INF-008 no reference to old `<D>/summary.md` remains | Task 3 | covered | source.md:1 |
