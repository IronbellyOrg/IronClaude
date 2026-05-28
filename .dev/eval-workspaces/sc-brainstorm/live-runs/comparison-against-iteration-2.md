# sc-brainstorm live-run comparison against iteration-2 baseline

Generated: 2026-05-27T16:34:45.529561Z

## Scope

- Compared cases: 4, 5, 6, 7, 8, 9, 10, 11
- Excluded cases: 12
- Exclusion rationale: Case 12 (architecture-graphql-public-api) is excluded because live invocation is blocked by the command/skill registry error `Unknown skill: sc:brainstorm-protocol`. Bringing case 12 into the comparison requires a separate scope decision and a registry-compatibility task.

## Summary

- Cases compared: 8 (ids 4, 5, 6, 7, 8, 9, 10, 11)
- Live artifact cases present: 8
- Complete artifact cases: 8
- Mean baseline structural pass rate: 73.87%
- Mean live structural pass rate: 82.42%
- Quality scores available: 0 of 8
- Quality unavailable (explicit gap): 8 of 8
- Live timing/token telemetry available: 0 of 8
- Telemetry unavailable (explicit gap): 8 of 8

### Availability gaps

- Quality: explicit gap: strict quality grading not yet covering compared cases
- Timing/tokens: explicit gap: live runs do not write timing.json / token telemetry; comparison cannot validate telemetry assertions until this lands

Availability gaps are reported as explicit shortfalls rather than silent passes; unavailable quality and unavailable telemetry MUST NOT be treated as remediation acceptance.

## Case comparison

| # | Eval | Baseline pass | Live pass | Δ pass | Artifacts | Baseline time | Live time | Baseline tokens | Live tokens | Contract | Quality | Notes |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| 4 | `code-migrate-pytest-vitest` | 35/46 | 40/46 | +10.87% | 4/4 | 184.4 | unavailable | 38420 | unavailable | success | unavailable | live runtime/token telemetry unavailable; quality score unavailable |
| 5 | `architecture-worker-pool-errors` | 36/47 | 44/47 | +17.02% | 4/4 | 612.8 | unavailable | 178420 | unavailable | success | unavailable | live runtime/token telemetry unavailable; quality score unavailable |
| 6 | `process-contributor-onboarding` | 34/45 | 37/45 | +6.66% | 4/4 | 298.7 | unavailable | 71240 | unavailable | success | unavailable | live runtime/token telemetry unavailable; quality score unavailable |
| 7 | `research-bun-vs-node` | 32/43 | 39/43 | +16.28% | 4/4 | 487.3 | unavailable | 138420 | unavailable | success | unavailable | live runtime/token telemetry unavailable; quality score unavailable |
| 8 | `code-api-caching-tasklist` | 33/45 | 38/45 | +11.11% | 5/5 | 442.2 | unavailable | 124880 | unavailable | success | unavailable | live runtime/token telemetry unavailable; quality score unavailable |
| 9 | `code-feature-flag-task` | 20/32 | 26/32 | +18.75% | 5/5 | 404.2 | unavailable | 104880 | unavailable | success | unavailable | live runtime/token telemetry unavailable; quality score unavailable |
| 10 | `incident-payment-webhook-q1` | 37/49 | 31/49 | -12.24% | 4/4 | 612.5 | unavailable | 187432 | unavailable | success | unavailable | live runtime/token telemetry unavailable; quality score unavailable |
| 11 | `code-duplicate-auth-blind` | 40/52 | 40/52 | +0.00% | 4/4 | 689.1 | unavailable | 198715 | unavailable | success | unavailable | live runtime/token telemetry unavailable; quality score unavailable |
