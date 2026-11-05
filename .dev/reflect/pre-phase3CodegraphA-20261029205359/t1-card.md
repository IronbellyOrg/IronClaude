# Tier 1 reflection card (UC-1, pre-execution)

Plan: `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md` (14 tasks, 8 phases). Spec: `source.md` in the same package (405 lines, byte-exact snapshot of the revised Phase 3 spec).

## Coverage

- Pass 1 (ID_REGEX) found 0 labeled ids; Pass 2 extracted 119 quote-pinned rows (`artifacts/inferred-requirements.yaml`). `coverage_degraded: parsed-sparse` (inferred 119 > parsed 0).
- Containment matching: 72/119 matched, `coverage_pct_union = 0.605` (`artifacts/coverage-matrix.yaml`).
- Triage of the 47 unmatched rows (`artifacts/unmapped-triage.yaml`): all 47 are covered by reference (the plan cites the spec section or row range, for example Task 6 "Apply source §1.2 rows 13-18", Task 3 "the seven sections of source §4"). Real gaps: 0.
- Spec task to plan task: §0 gate + baselines → Task 1; T0 → 2; T1 → 3; T2 → 4; T3 → 5; T4 → 6; T5 → 7; T6 → 8; T7 → 9; T8 → 10; T9 → 11; T10 → 12; T11 → 13; T12 → 14.
- Brief requirements: test command in every task's acceptance; commit point every task and an issue-#323 group comment at the last task of each of the 8 phases (groups 0, A-G); decision rules in Constraints (plan:28); final full verification (Task 13).

## Deviations (UC-1: plan vs spec)

- **D-1 (Drift, plan defect).** Task 14 writes the PR body to `./artifacts/pr-body.md` (plan:218). Commands run from the worktree root (plan:20), so `./artifacts/` is the project-root `artifacts/` folder, which `~/.claude/CLAUDE.md:33` says is never staged, not the package's `artifacts/`. The spec says only `--body-file <body>` (source.md:288). Fix: write the body under `.dev/codegraph-migration/progress/P3-pr-body.md`.
- **D-2 (Necessary, wording).** Task 2's commit criterion says "only the five experiment files and the decision log" (plan:58) while Constraints require also staging `.dev/tasks` (plan:26). Fix: say "plus `.dev/tasks`".
- **D-3 (Necessary, placeholder).** Task 13's installed-path check has a literal `<baseline (a) from the decision log>` placeholder (plan:207). An executor can fill it, but the line is not copy-runnable. Acceptable; noted.

## Risks

- The plan's reference inputs under `.dev/codegraph-migration/` are untracked on the planning branch; the Phase 3 worktree is created from `origin/master`. Task 1 checks they exist and escalates otherwise (plan:44); whether they reach `master` is UNVERIFIED.
- The status-only tool-list branch relies on CLI flags not yet captured (E-2 in Task 2); Tasks 8-9 depend on Task 2's output.

## Recommendation

Apply D-1 and D-2 to the plan; no other change.
