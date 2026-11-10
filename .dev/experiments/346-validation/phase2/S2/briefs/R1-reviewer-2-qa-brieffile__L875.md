# Reviewer 2 brief (persona: qa, model: haiku alias)

Task: pre-execution review (UC-1) of a plan against its spec. Assume the plan has mistakes and find them. Read-only. All paths are relative to `/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule`.
Plan: `.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261101-225635/TASK-WF-removeTheAnyIssu-20261101-225635.md`. Spec: same folder `source.md`.
Lens: coverage and acceptance. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. For each requirement, check that some task's acceptance criteria would actually detect a failure to meet it.
Grade each finding blocking (a required deliverable is missing, or a check cannot pass, or a check cannot detect the failure it exists for) or minor (wording, a weak but not wrong check). Return one finding per line: id, blocking|minor, claim, file:line evidence you Read, suggested fix. If you find nothing, give a Self-Audit naming what you checked.

## T1 card excerpt

```yaml
  - id: T1-F4
    severity: blocking
    claim: "R-004 is not met for two summary lines ('Max fix cycles: 3 for research ... 3 for final') absent from inventory 3.2, and Task 11's acceptance grep cannot detect that form or '| 3 |' table cells, so the check passes while 3-cycle caps remain."
  - id: T1-F5
    severity: minor
    claim: "Task 7 and Task 8 acceptance use 'pytest -k tech' / '-k readme or operational' that may select no tests; weak check but not wrong."
```

## Grounding hunks

codegraph run state: index_state=unknown checked_at=2026-11-02T03:10Z worktree_root=/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule projectPath=/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule (do not call codegraph; use Read/Grep/Glob)

### .dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261101-225635/source.md:1-31

The spec body, whole file (31 lines). Read it in full.

### .dev/reflect/pre-removeTheAnyIssu-20261101225845/artifacts/coverage-matrix.yaml:1-200

The coverage matrix built in Wave 1B (10 parsed rows, 6 inferred rows). Its notes already list: the R-008 check command `git diff -U0 ... | grep '^+' | grep -n 'src/superclaude'` also matches `+++ b/src/superclaude/...` headers so it always prints something; tests reading `task-builder/SKILL.md` not in Task 13's run (`tests/cli/reflect/test_no_nesting_guard.py:20`, `tests/troubleshoot/backtest/test_backtest_e5.py:32`); no check that the cap text is written into Task 11 files. Verify these and look for more.

### .dev/reflect/pre-removeTheAnyIssu-20261101225845/artifacts/grounding-hunks.md:1-40

Hunk H4: `operational-guide/SKILL.md:1349`, `readme/SKILL.md:2034`.

## Coverage slice

| Requirement | Task | Status | Grounding |
|---|---|---|---|
| R-002 | Tasks 2-10 | partial (S1-S3 not required in skill_template, analyst-completeness, DNSP contract, build-request templates, rf-analyst) | coverage-matrix.yaml R-002 row |
| R-006 | Task 13 | partial (phrase list misses "remain at any severity", tech-reference/SKILL.md:536) | coverage-matrix.yaml R-006 row |
| R-007 | Tasks 1, 2, 11 | covered | plan |
| R-008 | Constraints, Task 13 | check command cannot pass | coverage-matrix.yaml R-008 row |
| R-009 | Task 14 | covered | plan |
| R-010 | Task 13 | partial (two task-builder readers missing) | coverage-matrix.yaml R-010 row |
| INF-001..INF-006 | Constraints | 2 matched by containment, 4 carried by Constraints | coverage-matrix.yaml |
