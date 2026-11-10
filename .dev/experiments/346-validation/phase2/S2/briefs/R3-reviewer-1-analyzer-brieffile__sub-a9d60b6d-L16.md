# Reviewer 1 brief (persona: analyzer, model: sonnet) — pre-review 3 of 3 (final)

Task: pre-execution review (UC-1) of the final plan against its spec. Assume the plan has mistakes and find them. Read-only. Paths are relative to `/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule`.
Plan: `.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261102-053741/TASK-WF-removeTheAnyIssu-20261102-053741.md`. Spec: same folder `source.md`. Site lists: `.dev/review-severity-rule/inventory.md` (severity) and `.dev/review-severity-rule/cap-edits.yaml` (161 literal cap/at-cap rows, mechanically verified: applying all rows leaves every old absent and every new present; rows hold only cap fragments).
Lens: correctness of Tasks 1-11 (severity edits) and Task 6: follow each task literally against the current files; will the result state the rule correctly, keep what must stay (binary verdict, Rule 6, tails), and does every acceptance command pass on a correct result and fail on a wrong one? Look especially at rules that still count or recheck minor findings (for example the issue-count monotonicity / halt-guard rules near rf-qa.md:391-406 and rf-qa-qualitative.md:798, and task-builder's PR-02 monotonicity section) and whether any task changes them.
Severity rule for your findings: blocking = the plan as written produces wrong behaviour, a false claim, a missing required deliverable, or a check that cannot pass or cannot detect the failure it exists for; minor = wording, a moved line number, a weak but not wrong check. Do not re-report the already-found items below (extend or dispute only). Return one finding per line: id, blocking|minor, claim, file:line evidence you Read, suggested fix. If you find nothing new, give a Self-Audit naming what you checked. Under 45 lines.

## T1 card excerpt

```yaml
  - id: T1-F1
    severity: blocking
    claim: "task-builder's generated post-execution reflect step lets the executor append unresolved Regression/unauthorized Drift deviations to Open Questions and finish (task-builder/SKILL.md:2225, :2231, :2232, :2239); no task or cap-edits row covers it."
```

## Grounding hunks

codegraph run state: index_state=unknown checked_at=2026-11-02T05:55Z worktree_root=/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule projectPath=/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule (do not call codegraph)

### .dev/reflect/pre-removeTheAnyIssu-20261102054021/artifacts/coverage-matrix.yaml:1-400

Already found: (1) blocking: Task 6's acceptance (plan:101) cannot detect an unchanged FIX trigger at rf-team-lead.md:462 because "blocking" is also in the kept HALT clause; (2) minor: line-number drift in several acceptance criteria; Task 18's grep forbids "both repairs are unspent" though 2 repairs per task remain (ledger.md:143, retry.md:193); Task 19(f) excludes all of sc-implement-protocol; R-008 runs only in Task 19; nothing checks the Fix Cycle re-verify scope, "Must resolve ALL [N] issues", or the issue-count monotonicity rule (rf-qa.md:391, rf-qa-qualitative.md:798) that still counts minors; Task 15's "listed with its reason" is ambiguous; Task 19(g) passes if one readme copy survives; docs/reference/nfr-conv-2-prose-determinism.md:130-131 out of scope.

### .dev/review-severity-rule/cap-edits.yaml:1-1400

## Coverage slice

| Requirement | Task | Status |
|---|---|---|
| R-001..R-015 | Tasks 1-20 | all mapped exactly; see matrix |
| R-012 | Task 6 | check cannot detect unchanged trigger (blocking, already found) |
