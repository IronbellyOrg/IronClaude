# Base Selection (Step 3)

## Quantitative Scoring (50% weight)

Weights: RC 0.30, IC 0.25, SR 0.15, DC 0.15, SC 0.15. "Requirements" = the reviewer-brief obligations (cover correctness, coverage, deviation classification over the plan; cite evidence; actionable recommendations).

| Metric | Variant 1 (R1 card) | Variant 2 (QA card) | Notes |
|---|---|---|---|
| RC requirement coverage | 0.85 | 0.45 | V1 covers driver, sessions, cleanup, runbook edit, authorization, secrets; V2 covers gates, wait semantics, AC coherence, evidence tests (calibration: coverage 0.55) |
| IC internal consistency | 0.90 | 0.95 | V1's R1-F14 self-inconsistency (claims a mark the plan's own list excludes); V2 uniform blocking severity is consistent but unranked |
| SR specificity | 0.85 | 0.75 | Both concrete; V1 names exact commands and state keys |
| DC dependency completeness | 0.60 | 0.85 | 7 of V1's plan citations mislocated (calibration-confirmed); V2's citations resolve |
| SC section coverage | 1.00 | 0.70 | V1 has findings against Phases 1-6; V2 none against Phase 1-2 setup or cleanup |
| quant_score | 0.815 | 0.695 | (0.85x.30)+(0.90x.25)+(0.85x.15)+(0.60x.15)+(1.00x.15); (0.45x.30)+(0.95x.25)+(0.75x.15)+(0.85x.15)+(0.70x.15) |

## Qualitative Scoring (50% weight) — CEV summary

Position-bias mitigation: dual pass (input order, then reverse) produced identical dimension verdicts for both variants; 0 disagreements, 0 verdicts changed.

| Dimension | V1 | V2 | Deciding evidence |
|---|---|---|---|
| Completeness | 4/5 | 2/5 | V2's own calibration: "no finding touches setup, session A, cleanup or the secret-scan or release guards" |
| Correctness | 3/5 | 4/5 | V1: 7 mislocated plan citations + R1-F14 ungrounded; V2: all four claims survive verification (one severity adjusted) |
| Structure | 5/5 | 5/5 | Both follow card schema cleanly |
| Clarity | 4/5 | 4/5 | Both unambiguous; V1's dual citations aid triangulation |
| Risk coverage | 4/5 | 3/5 | V1 covers push guard, store writes, staging; V2 covers launch gates |
| Invariant & edge case | 4/5 | 2/5 | V1 probes boundaries (baseline deletion, crash restore); V2's gated-outcome case (QA-3) is its sole boundary finding |
| qual_score | 24/30 = 0.80 | 20/30 = 0.667 | Edge-case floor (>=1/5): both eligible |

## Combined Scoring

| Variant | quant | qual | final |
|---|---|---|---|
| Variant 1 (reviewer-1-card) | 0.815 | 0.800 | **0.81** |
| Variant 2 (reviewer-2-card) | 0.695 | 0.667 | 0.68 |

Margin 0.13 (>5%): no tiebreaker. Calibrated confidence weighting (V1 C=0.75, V2 C=0.67) preserves the ordering.

## Selected Base: Variant 1 (reviewer-1-card.yaml, analyzer persona)

Selection rationale: broader requirement and section coverage with equally actionable recommendations; V2's citation accuracy advantage does not offset its coverage gaps, and every V1 mislocated citation was mechanically correctable from the calibration map plus fresh reads.

Strengths to preserve (base): all 14 R1 rows, differentiated severity scale, dual citations.

Strengths to incorporate (non-base): QA-1 (notice-wait — complements R1-F01 in the same `send` block), QA-2 (per-subcommand gate for `c`), QA-3 (gated-outcome satisfiability — the only finding proving the plan's own ACs conflict with its gates), QA-4 (FAIL-classification test coverage for the gate-feeding evidence script).
