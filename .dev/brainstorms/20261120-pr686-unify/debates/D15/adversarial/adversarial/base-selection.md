# Base Selection: D15

Scores are single-evaluator estimates by the orchestrator; the dual-pass position-bias run was not performed by an independent agent (same limit as earlier debates).

## Quantitative Scoring (50% weight)
| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) |
|--------|--------|------------------|------------------|
| Requirement coverage (topic asks: list every element, adopt/change/reject, merge strategy, de-duplicated) | 0.30 | 0.65 | 0.55 |
| Internal consistency | 0.25 | 0.97 | 0.95 |
| Specificity ratio | 0.15 | 0.80 | 0.78 |
| Dependency completeness | 0.15 | 1.00 | 1.00 |
| Section coverage | 0.15 | 1.00 | 1.00 |
| **quant_score** | | **0.858** | **0.820** |

## Qualitative Scoring (50% weight), 30 criteria, CEV
| Dimension | V1 | V2 | Evidence note |
|-----------|----|----|---------------|
| Completeness (5) | 3 | 3 | Neither paper contains the element table; both name the capabilities. V1 names the changes per element class. |
| Correctness (5) | 5 | 4 | V2 fact 8 asymmetry and "as built" were withdrawn in Round 1/2. |
| Structure (5) | 5 | 5 | Same layout. |
| Clarity (5) | 4 | 4 | |
| Risk coverage (5) | 4 | 3 | V1 names rename, re-home, coupling risk; V2 names accidental landing only. |
| Invariant and edge case (5) | 3 | 2 | V1 cites M1/M2, test pin, placeholder gap; V2 cites the shared verb contract. Both >= 1/5, floor met. |
| **qual_score (/30)** | **24 = 0.800** | **21 = 0.700** | |

## Combined Scoring
| Variant | Combined |
|---------|----------|
| Variant 1 (OURS) | 0.829 |
| Variant 2 (CLAY) | 0.760 |
Margin 6.9 percent; above the 5 percent tie threshold, so no tiebreaker applied.

## Selected Base: Variant 1 (OURS)
- Rationale: it owns every rule row under the weighting rule and already uses the per-element shape both advocates ended at.
- Strengths to preserve: per-element outcomes with "Needs" and "Change" columns; "narrows, never closes" wording; owner gates.
- Strengths to incorporate from Variant 2: substrate-first build order and the merge path as one tested unit; one verb group and one JSON contract (D:140); T1 to T13 plus U and K registers as the test-plan skeleton; the capability list (cap, restart, ack wake, merge gate, audit, hand-back, nine-row list); the "named amendment list" method; the honest risk register (K12, K22).
