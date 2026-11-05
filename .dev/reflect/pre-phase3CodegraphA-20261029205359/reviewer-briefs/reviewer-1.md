# Reviewer 1 brief (persona: analyzer)

Plan under review: `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md` (224 lines). Spec: `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md` (405 lines). Mode UC-1 (pre-execution): judge whether the plan fully and correctly implements the spec, whether each task is independently executable by a reviewer who sees only that task plus the Constraints, and whether each acceptance criterion can pass as written. Classify each divergence as Authorized expansion / Necessary deviation / Drift / Regression with a `file:line` citation you Read yourself. Read-only: do not run commands or edit files. Return findings as YAML: `findings: [{id, class, severity, plan_ref, spec_ref, claim, fix}]` plus `self_audit` if you find nothing. Focus: correctness and executability of each task and its acceptance commands, dependency order, and contradictions between plan and spec or between tasks.

## T1 card excerpt

(Deviation and risk sections, verbatim from `.dev/reflect/pre-phase3CodegraphA-20261029205359/t1-card.md`)

## Deviations (UC-1: plan vs spec)

- **D-1 (Drift, plan defect).** Task 14 writes the PR body to `./artifacts/pr-body.md` (plan:218). Commands run from the worktree root (plan:20), so `./artifacts/` is the project-root `artifacts/` folder, which `~/.claude/CLAUDE.md:33` says is never staged, not the package's `artifacts/`. The spec says only `--body-file <body>` (source.md:288). Fix: write the body under `.dev/codegraph-migration/progress/P3-pr-body.md`.
- **D-2 (Necessary, wording).** Task 2's commit criterion says "only the five experiment files and the decision log" (plan:58) while Constraints require also staging `.dev/tasks` (plan:26). Fix: say "plus `.dev/tasks`".
- **D-3 (Necessary, placeholder).** Task 13's installed-path check has a literal `<baseline (a) from the decision log>` placeholder (plan:207). An executor can fill it, but the line is not copy-runnable. Acceptable; noted.

## Risks

- The plan's reference inputs under `.dev/codegraph-migration/` are untracked on the planning branch; the Phase 3 worktree is created from `origin/master`. Task 1 checks they exist and escalates otherwise (plan:44); whether they reach `master` is UNVERIFIED.
- The status-only tool-list branch relies on CLI flags not yet captured (E-2 in Task 2); Tasks 8-9 depend on Task 2's output.

## Grounding hunks

### .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md:1-224

Read the whole plan file; cite by line.

### .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md:264-291

Spec §5 task breakdown (rules for every task, T0-T12): each plan task must match its spec task.

### .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md:17-79

Spec §0 gate and §1.1 standing rules 1-9.

### .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md:193-230

Spec §3 new commands, including the overrides (a)-(e) where the spec wins over DES.

### .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md:292-350

Spec §6 progress reporting and §7 autonomy rules.

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| Task 14 PR body path vs project-root artifacts/ rule | D-1 | drift | plan:218, ~/.claude/CLAUDE.md:33 |
| Task 2 commit file list vs Constraints staging | D-2 | necessary | plan:58, plan:26 |
| Task 13 baseline placeholder | D-3 | necessary | plan:207 |
| Spec §5 T0-T12 → plan Tasks 2-14 | map | covered | source.md:276-288 |
