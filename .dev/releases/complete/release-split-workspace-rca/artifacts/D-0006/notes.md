# D-0006 — Notes

## Insertion-point rationale

`quick-check.yml` was the natural target per FR-L2.2 (the task names this workflow explicitly). Steps were appended after `Verify pytest plugin` and before `Summary`, matching the workflow's existing flat-step structure (no matrix, no separate jobs). This keeps the new checks colocated with the other lightweight integrity checks (lint, format, plugin) rather than spawning a parallel job — runtime impact is seconds (R-02 = Low/Low per roadmap).

`if: always()` was considered but **not** used: the existing steps in this workflow do not opt into it, and applying it only to the new steps would create asymmetric semantics where lint/format failures short-circuit but architecture failures do not. Default fail-fast behaviour is consistent with the rest of the workflow.

## Local-act vs synthetic-PR evidence choice

Per task Step 5, evidence may be a synthetic test PR **or** a local act run / scripted simulation. A scripted local simulation was used (Bash invocations of the same `make` targets the GitHub runner will invoke), captured in `evidence.md`. Rationale: this repo runs in a sandboxed environment without `act` or PR-creation permissions; the `make` targets behave identically locally and on the runner because the workflow simply shells out to them. The synthetic-PR option remains available to a reviewer who wishes to re-validate end-to-end on the live runner.

## Branch-protection follow-up (repo-admin scoped — out of T02.03 scope)

The workflow now exits non-zero on detection. To translate that into a hard merge-block, repo admins must:

1. Open repo Settings → Branches → Branch-protection rules for `master` (and `integration` if enforced).
2. Add `Quick Test (Python 3.10)` to the **Required status checks** list.
3. Enable **Require branches to be up to date before merging** (recommended for cache freshness).

Without step 2, the workflow runs and reports red but the PR remains technically mergeable. Acceptance Criterion 4 of T02.03 explicitly permits recording this as a follow-up note when branch-protection is admin-gated; this is that record.

## Pre-existing lint-architecture errors (out-of-scope blocker)

`make lint-architecture` currently reports **3 pre-existing errors** on a clean tree (independent of any `*-workspace/` issue):

- Check 1: `src/superclaude/commands/tdd.md` has `## Activation` but no matching skill `sc-tdd-protocol/` directory.
- Check 4: `spec-panel.md` is 651 lines (hard limit 500).
- Check 6: `task.md` missing `## Activation` (paired with `sc-task-protocol`).

These errors are unrelated to INV-002 / workspace misplacement and pre-date Phase 2. They will cause the new CI step to fail on every PR until resolved. **Recommendation:** open follow-up tickets to resolve them before merging the `quick-check.yml` change to `master`, OR resolve them in the same PR that lands T02.03. They are explicitly out of scope for this task per the FR boundary (FR-L2.2 covers wiring, not pre-existing policy debt).

## Tie-breaker note

No Section 4.9 tie-breaker was needed for this task — `quick-check.yml` is the single named target and both `make` targets are pre-existing.
