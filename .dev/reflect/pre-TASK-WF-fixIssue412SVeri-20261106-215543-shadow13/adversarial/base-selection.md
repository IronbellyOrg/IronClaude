# Base Selection — reflect Wave 4 (Mode A)

## Quantitative Scoring (50% weight)

| Metric (weight) | V1 | V2 | V3 |
|---|---|---|---|
| Requirement coverage (0.30) | 1.00 (INF-006/007 cited with spec+plan quotes) | 0.60 (units named in summary, none cited) | 1.00 (INF-001 cited) |
| Internal consistency (0.25) | 1.00 | 1.00 | 1.00 |
| Specificity ratio (0.15) | 0.90 | 0.40 | 0.85 |
| Dependency completeness (0.15) | 1.00 | 1.00 | 1.00 |
| Section coverage (0.15) | 0.75 | 0.50 | 1.00 |
| **quant_score** | **0.96** | **0.74** | **0.98** |

## Qualitative Scoring (50% weight) — 30-criterion binary rubric (CEV)

| Dimension (5 each) | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4 (no out-of-scope statement) | 3 (units unnamed) | 5 |
| Correctness | 5 | 4 (no false claim, none verifiable) | 3 (two findings later refuted) |
| Structure | 4 | 3 | 5 |
| Clarity | 4 | 3 | 4 |
| Risk coverage | 3 | 2 | 4 |
| Invariant & edge-case coverage | 3 | 1 | 4 |
| **qual_score (met/30)** | **23/30 = 0.77** | **16/30 = 0.53** | **25/30 = 0.83** |

Edge-case floor: all three ≥1/5 — eligible.

CEV exemplars: V1 C5 MET ("no task AC gates the staging rule" cited to plan:21 vs tasklist ACs). V3 Crr1 NOT MET (two findings refuted in debate: the 17-item pin covers every first-paragraph sentence; the contents assertion test:367-368 exists). V2 Crr1 NOT MET as stated (its 9/9 claim is uncheckable from the card itself; after evidence it is True but not card-internal).

## Position-Bias Mitigation
Dual pass (V1,V2,V3 then V3,V2,V1) produced identical verdicts on all 90 criterion-variant pairs; 0 disagreements; no re-evaluations needed.

## Combined Scoring

| Variant | quant | qual | combined (0.5/0.5) |
|---|---|---|---|
| V1 | 0.96 | 0.77 | **0.865** |
| V3 | 0.98 | 0.83 | **0.905** |
| V2 | 0.74 | 0.53 | 0.635 |

Margin V3-V1: 0.04 (<0.05) -> tiebreaker Level 1 (debate points): V3 won 0 contested points (both its findings refuted), V1 won C-001 and C-002 -> **base = V1**.

## Selected Base: Variant 1 (analyzer/sonnet card)

Selection rationale: highest correctness under debate pressure (all 3 findings survived cross-examination vs V3's 0/2); debate tiebreaker overrides the small combined-score deficit.
Strengths to preserve: V1's three findings as the merged verdict spine.
Strengths to incorporate: V2's confirmed 9/9 unit-coverage row (as scope qualifier, not finding); V3's refuted-pair with the refutation evidence (as the audit trail for why they are not defects); V3's residual advisory on a possible full-paragraph identity check.
Changes not being made: V3 F1/F2 are NOT merged as findings (refuted on test:17-35 + plan:36 and test:367-368 respectively); V2's zero-defect stance is not adopted as the verdict (its own calibration 0.43 and the conceded rubric mismatch).
