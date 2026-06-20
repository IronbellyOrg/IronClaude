---
phase: 5
step: 5.5
verdict: PASS
exit_code: 0
command: uv run python .dev/eval-workspaces/sc-brainstorm/compare_live_runs.py
created_date: 2026-05-26
---

# Comparison Script Run — PASS

## Result

- **Verdict:** PASS (command executed without error)
- **Exit code:** 0
- **Regenerated output paths:**
  - `.dev/eval-workspaces/sc-brainstorm/live-runs/comparison-against-iteration-2.json`
  - `.dev/eval-workspaces/sc-brainstorm/live-runs/comparison-against-iteration-2.md`

## Compared Cases

- 8 cases compared: ids 4, 5, 6, 7, 8, 9, 10, 11
- Case 12 intentionally EXCLUDED with explicit reason rendered in both JSON and Markdown output:
  > Case 12 (architecture-graphql-public-api) is excluded because live invocation is blocked by the command/skill registry error `Unknown skill: sc:brainstorm-protocol`. Bringing case 12 into the comparison requires a separate scope decision and a registry-compatibility task.

## Structural Pass Rates (Pre-Rerun Baseline — Phase 5 not Phase 6)

These metrics reflect the EXISTING pre-remediation live artifacts in `.dev/eval-workspaces/sc-brainstorm/live-runs/eval-*/`. They are NOT post-remediation acceptance metrics — Phase 6 will rerun cases 4-11 against the Phase 2/3 protocol changes and regenerate this comparison.

- Mean baseline structural pass rate: 100.00%
- Mean live structural pass rate (pre-rerun): 81.69%
- Per-case pass deltas vs baseline (live - baseline):
  - Case 4 (`code-migrate-pytest-vitest`): -38.46% (16/26 vs 26/26)
  - Case 5 (`architecture-worker-pool-errors`): +0.00% (27/27)
  - Case 6 (`process-contributor-onboarding`): -16.00% (21/25)
  - Case 7 (`research-bun-vs-node`): -13.04% (20/23)
  - Case 8 (`code-api-caching-tasklist`): -16.00% (21/25)
  - Case 9 (`code-feature-flag-task`): -8.33% (11/12)
  - Case 10 (`incident-payment-webhook-q1`): -25.00% (21/28)
  - Case 11 (`code-duplicate-auth-blind`): -29.63% (19/27)

These are the pre-existing regression deltas surfaced in the remediation plan. Phase 6 must regenerate live artifacts to determine remediated values.

## Quality Availability

- Quality scores available: **0 of 8**
- Quality unavailable (explicit gap): **8 of 8**
- Availability gap message: `explicit gap: strict quality grading not yet covering compared cases`

This is an EXPLICIT availability gap, NOT a silent pass. The remediation acceptance pass requires either (a) quality scores becoming available for cases 4-11, or (b) qualitative review covering these cases via `pg-6-qualitative-acceptance-review.md` in Phase 6. Phase 5 does not inflate the structural pass rate to compensate for missing quality data.

## Live Timing / Token Telemetry Availability

- Telemetry available: **0 of 8**
- Telemetry unavailable (explicit gap): **8 of 8**
- Availability gap message: `explicit gap: live runs do not write timing.json / token telemetry; comparison cannot validate telemetry assertions until this lands`

Telemetry assertions are scoped (per `evals.json` `telemetry_scope_note`): absent telemetry is reported as `status: unavailable`, NOT silent pass. No inflation occurs.

## Case 12 Exclusion

Confirmed in regenerated output:
- JSON `summary.excluded_case_ids == [12]`
- JSON `summary.excluded_case_reason` matches the script constant verbatim
- Markdown `## Scope` section renders Compared / Excluded / Exclusion rationale

This exclusion is intentional and explicitly documented. It remains in place until command/skill registry compatibility is brought into scope.

## UV-Only Execution

Command invoked with `uv run python ...` — no bare `python`, `python -m`, `pip`, or direct script execution. The UV environment-mismatch warning (`VIRTUAL_ENV=/lsiopy does not match the project environment path .venv`) is the operator-environment notice; it does NOT prevent execution and the script completes successfully.

## No Fabricated Metrics

All metrics in the regenerated outputs come from the live-run artifacts and the iteration-2 baseline benchmark — no values were synthesized or inflated. Unavailable quality and unavailable telemetry are reported as such, never as available.
