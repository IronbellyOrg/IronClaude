# Base Selection (condensed; scored by the orchestrator, no separate position-bias passes)

Honesty note: the 30-criterion rubric with dual-pass position-bias mitigation was NOT run as two independent evaluator passes. The orchestrator scored once, with each criterion backed by one cited line, and ran the tiebreaker. Return contract carries `fallback_mode: true`.

## Quantitative Scoring (50% weight)
| Metric (weight) | V1 | V2 | V3 | Basis |
|---|---|---|---|---|
| Requirement coverage RC (0.30) | 0.33 | 0.78 | 0.40 | share of the 45 inferred rows whose gap area each card touches: V1 rows 15-27 lens, V2 all rows, V3 plan structure |
| Internal consistency IC (0.25) | 0.90 | 0.75 | 0.95 | V2 claims that its own advocate withdrew (F1, F3, F6 and 7 blocking flags) count as contradictions with the plan text |
| Specificity SR (0.15) | 0.95 | 0.95 | 0.95 | all findings cite lines and quote |
| Dependency completeness DC (0.15) | 1.00 | 1.00 | 1.00 | every reference resolves in the plan or spec |
| Section coverage SC (0.15) | 0.60 | 1.00 | 0.70 | held / refuted / defect sections present |
| quant_score | 0.70 | 0.85 | 0.72 | RC 0.30 + IC 0.25 + SR 0.15 + DC 0.15 + SC 0.15 |

## Qualitative Scoring (50% weight)
Dimension subtotals (of 5 each), one evidence line per dimension, no partial credit.
| Dimension | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|
| Completeness | 2 | 4 | 3 | V2 reads the whole plan against the spec; V1 names only Tasks 3, 4, 5, 7, 8 |
| Correctness | 4 | 2 | 4 | V2 F1, F3 and F6 were conceded wrong or overstated; V1 F2 is conditional |
| Structure | 4 | 4 | 4 | each card has held / refuted / findings |
| Clarity | 4 | 4 | 4 | claims fit the 300-character schema |
| Risk coverage | 4 | 3 | 2 | V1 traces a cross-cycle data-loss path; V3 finds only structural risks |
| Invariant and edge case coverage | 3 | 2 | 1 | V1 traces fold and release rows; V3 checks shared-file order only |
| Total (of 30) | 21 | 19 | 18 | |
| qual_score | 0.70 | 0.63 | 0.60 | |

Edge Case Floor Check: all variants score at least 1/5; all eligible.

## Combined Scoring
| Variant | Quant x0.5 | Qual x0.5 | Combined |
|---|---|---|---|
| V1 | 0.350 | 0.350 | 0.700 |
| V2 | 0.425 | 0.315 | 0.740 |
| V3 | 0.360 | 0.300 | 0.660 |

Margin V2 over V1: 0.040, under 0.05, so the tiebreaker applies. Level 1, diff points won in the scoring matrix: V2 7 (C-001, C-003, C-005, C-006, C-007, C-008, C-009), V1 3 (C-002, C-004, C-011), V3 2 (C-010, C-012). V2 wins at level 1.

## Selected Base: Variant 2 (reviewer-2 card, qa persona, haiku class)
- Rationale: widest coverage of the plan and spec (12 findings, 6 of them survive as real criterion gaps), and the most findings per diff point won.
- Strengths to preserve: the criterion-failability method (F4, F5, F7), the citations (62 of 62 verified resolvable against a repo-relative snapshot).
- Strengths to incorporate: V1's cross-cycle trace (C-004, lowered to MINOR), V1's Task 7 timeline-count gap (C-002), V3's `Depends on` gaps (C-010), V1's fold variant gap (C-011), the probe's fold gaps INV-001 and INV-002.
- Weaknesses to correct: all seven `blocking: true` flags (none survives), F1 (mislabel only), F3 (the plan does specify the retry), F6 (plan lines 170-172 assert content).
