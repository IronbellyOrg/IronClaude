# Reviewer 1 brief (persona: analyzer, model: sonnet) — pre-review 2

Task: pre-execution review (UC-1) of a regenerated plan against its spec. Assume the plan has mistakes and find them. Read-only. Paths are relative to `/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule`.
Plan: `.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261102-042031/TASK-WF-removeTheAnyIssu-20261102-042031.md`. Spec: same folder `source.md`. Site lists: `.dev/review-severity-rule/inventory.md`, `.dev/review-severity-rule/cap-sites.md`.
Lens: correctness of the CAP tasks (12-16) and the pinned-line tasks (3, 6). For each IN row of cap-sites.md that a task names, will the task's instruction plus its acceptance check reliably produce the replacement and detect a miss? Test CAP_PATTERN (plan Constraints) against the replacement-target lines yourself with grep: which IN lines does it NOT match, so a miss would pass? Check count semantics in Task 15 (cli-portify iterations) and Task 16 (prd range(max_cycles + 1)).
Grade each finding blocking (wrong behaviour, false claim, missing required deliverable, or a check that cannot pass or cannot detect the failure it exists for) or minor. Already found (do not re-report; extend or dispute only): see Grounding hunks. Return one finding per line: id, blocking|minor, claim, file:line evidence you Read, suggested fix. If you find nothing new, give a Self-Audit naming what you checked. Under 50 lines.

## T1 card excerpt

```yaml
  - id: T1-F1
    severity: blocking
    claim: "R-003 not met and Task 5's grep cannot pass: lite at-cap rule 'unresolved issues become Open Questions' at 01_mdtm_template_generic_task.md:938 and 02_mdtm_template_complex_task.md:1090 is not in Task 5's edit list."
```

## Grounding hunks

codegraph run state: index_state=unknown checked_at=2026-11-02T04:30Z worktree_root=/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule projectPath=/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule (do not call codegraph)

### .dev/reflect/pre-removeTheAnyIssu-20261102042426/artifacts/coverage-matrix.yaml:1-400

Wave 1B matrix. Already-found blocking gaps: (a) T1-F1 above; (b) at-cap "Open Questions" rules at task-builder/SKILL.md:1420 and roadmap/SKILL.md:569 in no task; rf-task-builder.md:384/386 cells uncheckable; (c) CAP_PATTERN misses 11 IN lines (tech-reference:177, roadmap:554, cli_portify/commands.py:100-101, sc-cli-portify-protocol/SKILL.md:355/363/364/374/534, decisions.yaml:123, ib_agent_core.md:933) and leftover 3s on lines it does match (convergence.py:149, task-builder:1310, 02_mdtm:753/1090, qa-fix-summary:105, readme:2034, operational-guide:1349); (d) Task 18(d) checks canonical cap text only in pragmatic.md.

### .dev/review-severity-rule/cap-sites.md:1-400

## Coverage slice

| Requirement | Task | Status |
|---|---|---|
| R-004 | Tasks 3, 6, 12-16 | partial (CAP_PATTERN gaps) |
| R-011 | Tasks 7, 15, 16 | covered; check count semantics |
| R-012 | Task 6 | partial (blocking-only FIX trigger unchecked) |
| R-013 | Task 16 | partial (ib_agent_core:933 unchecked) |
