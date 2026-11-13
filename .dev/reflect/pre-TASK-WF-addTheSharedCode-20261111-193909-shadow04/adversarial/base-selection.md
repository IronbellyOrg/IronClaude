# Base Selection (Step 3)

## Quantitative (50%)

| Metric (weight) | V1 analyzer | V2 qa | V3 refactorer |
|---|---|---|---|
| Requirement coverage (0.30) | 0.95 (all 3 INF rows + executed-state checks) | 0.90 (all rows + Task 11) | 0.85 (INF-003 deferred to analyzer) |
| Internal consistency (0.25) | 1.00 (one overclaim "covered" conceded in R1) | 0.90 (Drift labels wrong, withdrawn) | 0.85 (F2 self-downgraded; Task 10 both "exact" and "interpretation-dependent") |
| Specificity (0.15) | 0.95 (per-field breakdown, heading line numbers) | 0.80 (bare line numbers) | 0.90 (label/number, Makefile lines) |
| Dependency completeness (0.15) | 1.00 | 1.00 | 0.95 |
| Section coverage (0.15) | 1.00 | 1.00 | 1.00 |
| **quant** | **0.977** | **0.922** | **0.907** |

## Qualitative (50%, 30-criterion binary, CEV)

V1: 26/30 — strongest correctness/completeness (only card reading all four references with per-field diff; root-cause U-003). Edge-case floor: 3/5 (met).
V2: 22/30 — strongest verification honesty (blocked posture); classification error cost 3 criteria; no recommendations (actionability 1/5). Edge floor: 2/5.
V3: 24/30 — strongest invariant/edge coverage (mirror, format, tests: 4/5); internal-consistency deductions. Edge floor: 4/5.

## Combined

| Variant | 0.5×quant + 0.5×qual | Score |
|---|---|---|
| V1 | 0.489 + 0.433 | **0.922** |
| V3 | 0.454 + 0.400 | 0.854 |
| V2 | 0.461 + 0.367 | 0.828 |

## Selected Base: Variant 1 (analyzer/sonnet)

Margin 6.8% over V3 (> 5%, no tiebreaker). Rationale: only card that read all four reference agents with a per-field divergence breakdown; produced the root-cause finding (spec self-contradiction) and the dropped-caveats observation; debate points won: U-003, U-004, C-003 (posture adopted with V2's label).

## Strengths to incorporate
- V2: verification-blocked posture for INF-002 ("verified outside grounding root" label); attribution-vs-inclusion distinction.
- V3: U-002 list-style mismatch (LOW); F4 unnamed tests (folded into AC finding); plugin-mirror advisory with pre-existing-gap evidence.
- Probe INV-002/003/006 corrections: 3-of-4 fallback count; "two freshness-gate families" phrasing; severity rationale without behavioral-loss claim.
