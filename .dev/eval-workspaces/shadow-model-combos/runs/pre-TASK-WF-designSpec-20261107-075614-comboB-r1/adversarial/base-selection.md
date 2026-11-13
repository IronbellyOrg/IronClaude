# Base Selection

Abbreviated: the quantitative metrics below were estimated by the orchestrator from the card text, not computed by a script; the 30-criterion rubric is reported as dimension subtotals with one evidence line each, not as 30 CEV rows; the reverse-order second pass was not run. Recorded as a deviation from the full protocol.

## Quantitative Scoring (50% weight)
| Metric | Weight | V1 | V2 | V3 |
|---|---|---|---|---|
| Requirement coverage (plan tasks examined / 13) | 0.30 | 0.31 (4 of 13) | 0.85 (all rows, 10 unmatched rows checked) | 0.85 (Tasks 1-13) |
| Internal consistency (1 - false claims / claims) | 0.25 | 0.90 (2 citation slips) | 0.85 (F3 meta-claim unverifiable) | 0.85 (one false claim: dependencies all complete) |
| Specificity ratio | 0.15 | 0.80 | 0.75 | 0.85 |
| Dependency completeness (cited lines resolve) | 0.15 | 0.80 | 0.90 | 0.90 |
| Section coverage | 0.15 | 0.29 | 0.71 | 1.00 |
| quant_score | | 0.62 | 0.83 | 0.88 |

## Qualitative Scoring (50% weight)
| Dimension (5 each) | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|
| Completeness | 2 | 4 | 5 | V1 states 9 tasks unchecked; V3 covers spec sections 4.1-4.7, 5, 6, 7, 8, 10 |
| Correctness | 4 | 4 | 4 | V1 no false claim; V2 F3 unverifiable; V3 "all complete" withdrawn |
| Structure | 3 | 4 | 4 | tables with evidence columns (V2, V3) |
| Clarity | 3 | 4 | 4 | named wrong outcome per finding |
| Risk Coverage | 2 | 2 | 4 | only V3 raises a safety scenario (C-003) |
| Invariant and edge-case coverage | 1 | 0 | 4 | V1 `guard is None` rows discussed; V2 none; V3 held-guard, dict, count |
| qual_score (/30) | 15 | 18 | 25 | |
| qual fraction | 0.50 | 0.60 | 0.83 | |

Edge Case Floor Check: V2 scores 0/5 on invariant and edge-case coverage and is ineligible as base; V1 1/5 and V3 4/5 eligible.

## Combined Scoring
variant_score = 0.5 x quant + 0.5 x qual: V1 = 0.56, V2 = 0.72 (ineligible), V3 = 0.86. Margin between eligible top two: 0.30. No tiebreaker.

## Selected Base: Variant 3 (reviewer-3, refactorer, opus class)
Rationale: widest coverage of the plan, the only finding with a concrete failure sequence (C-003), refutes two T1 candidates with evidence, separates HEAD-only evidence.
Strengths to preserve: findings F1-F7 with line-cited quotes; refuted-candidates section; HEAD-only evidence labelled.
Strengths to incorporate: V2 F1 and F2 (dependency edges, flags-guide paragraph); V1 rows-checked discipline; probe INV-001 and INV-002; severity consensus MEDIUM for C-001 and C-003.
