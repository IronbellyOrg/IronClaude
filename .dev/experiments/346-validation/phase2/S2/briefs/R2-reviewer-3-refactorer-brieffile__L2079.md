# Reviewer 3 brief (persona: refactorer, model: opus) — pre-review 2

Task: pre-execution review (UC-1) of a regenerated plan against its spec. Assume the plan has mistakes and find them. Read-only. Paths are relative to `/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule`.
Plan: `.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261102-042031/TASK-WF-removeTheAnyIssu-20261102-042031.md`. Spec: same folder `source.md`. Site lists: `.dev/review-severity-rule/inventory.md`, `.dev/review-severity-rule/cap-sites.md`.
Lens: structure, ordering and single source of truth. Check: (1) task ordering, so that no task's acceptance tests are broken by an earlier task or can pass only after a later one (pay attention to tests/audit runs in Tasks 2-14 while other files are half-edited, the dnsp sha propagation in Task 6, the BASELINE_BLOCK_SHA re-pin in Task 3, and Task 12 editing lines Tasks 2/3/5 already edited); (2) whether a precise, complete acceptance design exists for the cap work, for example checking each cap-sites.md IN row (its "current excerpt" gone and its replacement present) instead of a regex, and whether cap-sites.md rows are precise enough for that (quoted text unique in its file); (3) single-source of S1-S5 and the cap text; (4) plugin twins and R-008.
Grade each finding blocking (a test that fails at the task's own acceptance, a broken twin, a missing deliverable, a check that cannot detect its failure) or minor. Already found (do not re-report; extend or dispute only): see Grounding hunks. One finding per line: id, blocking|minor, claim, file:line evidence you Read, suggested fix. If nothing new, a Self-Audit. Under 50 lines.

## T1 card excerpt

```yaml
  - id: T1-F2
    severity: minor
    claim: "Task 6 keeps the tokens the dnsp test asserts ('HALT and ask user' :406, 'HALT' :646); Task 3's rule-10 rewrite adds no softening token (test_severity_floor_unweakened.py:191-199)."
```

## Grounding hunks

codegraph run state: index_state=unknown checked_at=2026-11-02T04:30Z worktree_root=/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule projectPath=/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule (do not call codegraph)

### .dev/reflect/pre-removeTheAnyIssu-20261102042426/artifacts/coverage-matrix.yaml:1-400

Already-found: Task 5 misses 01_mdtm:938 and 02_mdtm:1090; Open Questions at-cap at task-builder:1420 and roadmap:569; CAP_PATTERN misses 11 IN lines and leftover 3s on matched lines; Task 18(d) only checks pragmatic.md.

### .dev/review-severity-rule/cap-sites.md:1-400

## Coverage slice

| Requirement | Task | Status |
|---|---|---|
| R-004 | Tasks 3, 6, 12-16 | partial |
| R-006 | Task 18 | partial |
| R-008 | all, Task 18 | covered |
| R-012 | Task 6 | partial |
