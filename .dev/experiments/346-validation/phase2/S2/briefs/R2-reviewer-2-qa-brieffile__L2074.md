# Reviewer 2 brief (persona: qa, model: haiku alias) — pre-review 2

Task: pre-execution review (UC-1) of a regenerated plan against its spec. Assume the plan has mistakes and find them. Read-only. Paths are relative to `/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule`.
Plan: `.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261102-042031/TASK-WF-removeTheAnyIssu-20261102-042031.md`. Spec: same folder `source.md`.
Lens: coverage and acceptance. Audit the coverage matrix AGAINST the spec body; surface any requirement-bearing span absent from the matrix. Then focus on Task 18 (the static test): would each of its parts (a)-(g) detect the failure it exists for, pass on a correct implementation, and avoid false failures (for example the old-wording scan hitting text that must stay, such as quoted examples inside tests, CHANGELOG, or the rule text S1-S5 itself)? Check Task 17 (/sc:implement option A) acceptance against `src/superclaude/skills/sc-implement-protocol/refs/retry.md:133-193`, `refs/qa.md:255-275`, `refs/ledger.md:140-165`.
Grade each finding blocking (missing deliverable, check that cannot pass or cannot detect its failure, wrong behaviour) or minor. Already found (do not re-report; extend or dispute only): see Grounding hunks. One finding per line: id, blocking|minor, claim, file:line evidence you Read, suggested fix. If nothing new, a Self-Audit. Under 50 lines.

## T1 card excerpt

```yaml
  - id: T1-F1
    severity: blocking
    claim: "Task 5 grep cannot pass: lite at-cap 'unresolved issues become Open Questions' at 01_mdtm:938 and 02_mdtm:1090 not in Task 5's edit list."
```

## Grounding hunks

codegraph run state: index_state=unknown checked_at=2026-11-02T04:30Z worktree_root=/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule projectPath=/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule (do not call codegraph)

### .dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261102-042031/source.md:1-40

The spec body, whole file. Read it in full.

### .dev/reflect/pre-removeTheAnyIssu-20261102042426/artifacts/coverage-matrix.yaml:1-400

Wave 1B matrix (14 parsed, 7 inferred). Already-found: T1-F1; Open Questions at-cap rules at task-builder/SKILL.md:1420 and roadmap/SKILL.md:569; CAP_PATTERN misses 11 IN lines and leftover 3s on matched lines; Task 18(d) checks cap text only in pragmatic.md; minors: test_nfr_conv_9_zero_trust.py:432 assert, task-builder:901 has no "max-3-cycles" token, Task 17 never checks ledger row V (ledger.md:157), Task 15 says "ten" files but lists nine.

## Coverage slice

| Requirement | Task | Status |
|---|---|---|
| R-005, R-014 | Task 17 | covered; checks incomplete (row V) |
| R-006 | Task 18 | partial |
| R-007 | Tasks 1, 2, 3, 6, 12, 15 | covered |
| R-009 | Task 19 | covered |
| R-010 | all | covered (sync-dev per task) |
| INF-001..007 | Constraints | 2 matched, 5 carried by Constraints |
