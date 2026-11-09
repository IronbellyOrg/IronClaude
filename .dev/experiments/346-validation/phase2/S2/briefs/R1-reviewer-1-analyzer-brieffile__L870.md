# Reviewer 1 brief (persona: analyzer, model: sonnet)

Task: pre-execution review (UC-1) of a plan against its spec. Assume the plan has mistakes and find them. Read-only. All paths are relative to `/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule`.
Plan: `.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261101-225635/TASK-WF-removeTheAnyIssu-20261101-225635.md`. Spec: same folder `source.md`. Site list the plan relies on: `.dev/review-severity-rule/inventory.md`.
Lens: correctness of the plan's instructions. Will each task, followed literally, produce the required change without breaking something or leaving a site behind? Check the replacement wording, the sha256 propagation, the /sc:implement option A edits, and whether the acceptance checks can pass and would catch the failure they target.
Grade each finding blocking (the plan as written produces wrong behaviour, a false claim, a missing required deliverable, or a check that cannot pass) or minor (wording, a moved line number, a weak but not wrong check). Return one finding per line: id, blocking|minor, claim, file:line evidence you Read, suggested fix. If you find nothing, give a Self-Audit naming what you checked.

## T1 card excerpt

```yaml
  - id: T1-F1
    severity: blocking
    claim: "R-004 (Max 3 drops to 2) is not met for cli_portify: Task 11 lowers the SKILL.md/decisions.yaml text to 2 but the executable ConvergenceEngine default and its panel_review caller stay at 3, so docs and code disagree."
  - id: T1-F2
    severity: blocking
    claim: "R-004 is not met for the prd CLI pipeline: max_research_fix_cycles defaults to 3 in code; no task changes it or its tests."
  - id: T1-F3
    severity: blocking
    claim: "R-002 is not met for the prd CLI prompt: prompts.py:1173 keeps 'FAIL: ALL findings must be resolved', the shared line Task 6 replaces in prd/refs/agent-prompts.md:283; no task edits prompts.py."
```

## Grounding hunks

codegraph run state: index_state=unknown checked_at=2026-11-02T03:10Z worktree_root=/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule projectPath=/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule (do not call codegraph; use Read/Grep/Glob)

### .dev/reflect/pre-removeTheAnyIssu-20261101225845/artifacts/grounding-hunks.md:1-40

Read this file: hunks H1-H5 (cli_portify and prd code caps, prd prompts.py:1173, "Max fix cycles: 3" summary lines, verified-present sha and option A sites).

### src/superclaude/skills/sc-implement-protocol/refs/retry.md:133-149

Repair round items 1-13 (the option A edit target). Also read `refs/retry.md:187-193` (Cost and caps) and `refs/qa.md:255-275`.

## Coverage slice

| Requirement | Task | Status | Grounding |
|---|---|---|---|
| R-001 | Task 1 | covered | plan Task 1 |
| R-003 | Tasks 5, 9 | covered | plan Tasks 5, 9 |
| R-004 | Task 11 | partial (T1-F1, T1-F2, T1-F4) | grounding-hunks.md H1, H2, H4 |
| R-005 | Task 12 | covered; check that A3-A5 and `halt review=5 reason=ladder-end` survive is absent | plan Task 12 acceptance |
