# Reviewer 3 brief (persona: refactorer, model: opus)

Task: pre-execution review (UC-1) of a plan against its spec. Assume the plan has mistakes and find them. Read-only. All paths are relative to `/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule`.
Plan: `.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261101-225635/TASK-WF-removeTheAnyIssu-20261101-225635.md`. Spec: same folder `source.md`. Site list: `.dev/review-severity-rule/inventory.md`.
Lens: structure and single source of truth. The rule text must have one source (`src/superclaude/output-styles/pragmatic.md`) with exact copies elsewhere; plugin twins under `plugins/superclaude/` must stay byte-equal to `src/superclaude/`; installed primitives must not name `src/superclaude/` paths. Check: does any task edit a `src/superclaude/` file that has a tracked twin under `plugins/superclaude/` without copying it (search `plugins/superclaude/` for same-relative-path twins of every file the plan edits); are tasks ordered so that a task's acceptance tests can pass when that task finishes (no test broken by a task and fixed only by a later task); is Task 13's static test designed so the canonical sentences have one source.
Grade each finding blocking (wrong behaviour, a broken twin, a test that fails at the task's own acceptance, a missing deliverable) or minor (style, wording). Return one finding per line: id, blocking|minor, claim, file:line evidence you Read, suggested fix. If you find nothing, give a Self-Audit naming what you checked.

## T1 card excerpt

```yaml
  - id: T1-F1
    severity: blocking
    claim: "R-004 (Max 3 drops to 2) is not met for cli_portify: Task 11 lowers the SKILL.md/decisions.yaml text to 2 but the executable ConvergenceEngine default and its panel_review caller stay at 3, so docs and code disagree."
  - id: T1-F3
    severity: blocking
    claim: "R-002 is not met for the prd CLI prompt: prompts.py:1173 keeps 'FAIL: ALL findings must be resolved', the shared line Task 6 replaces in prd/refs/agent-prompts.md:283; no task edits prompts.py."
```

## Grounding hunks

codegraph run state: index_state=unknown checked_at=2026-11-02T03:10Z worktree_root=/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule projectPath=/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule (do not call codegraph; use Read/Grep/Glob)

### .dev/reflect/pre-removeTheAnyIssu-20261101225845/artifacts/grounding-hunks.md:1-40

Hunks H1-H5.

### .dev/review-severity-rule/inventory.md:13-14

The inventory's twin claim: only `sc-implement-protocol` and `sc-workflow-protocol` have tracked twins under `plugins/superclaude/skills/`. Verify it against `git ls-files plugins/superclaude` by Glob.

## Coverage slice

| Requirement | Task | Status | Grounding |
|---|---|---|---|
| R-001 | Task 1 | covered | plan Task 1 |
| R-005 | Task 12 | covered (twin copy named) | plan Task 12 |
| R-006 | Task 13 | partial (single-source design stated; twin check only for "files edited by this plan") | plan Task 13 |
| R-008 | Constraints | check command flawed (see coverage matrix) | coverage-matrix.yaml R-008 row |
