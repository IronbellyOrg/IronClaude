# Base Selection

## Quantitative Scoring (50% weight)
Estimated by reading (quick, not scripted). Source requirements = the review task: audit the plan against the spec, cite lines, grade findings, answer the coverage rows.

| Metric | Weight | V1 (reviewer 1) | V2 (reviewer 2) |
|---|---|---|---|
| Requirement coverage | 0.30 | 1.00 (answers all 10 coverage rows) | 1.00 (answers all rows, grouped) |
| Internal consistency | 0.25 | 0.95 (F8 graded Note while saying the rule requires it) | 1.00 |
| Specificity ratio | 0.15 | 0.90 | 0.93 |
| Dependency completeness | 0.15 | 0.90 (plan citations point at wrong lines) | 1.00 |
| Section coverage | 0.15 | 0.80 (4 sections) | 1.00 (6 sections incl. disposition and summary) |
| **quant_score** | | **0.9250** | **0.9895** |

## Qualitative Scoring (50% weight)
| Dimension (5 each) | V1 | V2 | Deciding evidence |
|---|---|---|---|
| Completeness | 4 | 4 | each missed findings the other found |
| Correctness | 3 | 5 | V1 plan line numbers are all offset by 31 (criterion 1 and 5 NOT MET); V2's lines are real |
| Structure | 4 | 4 | |
| Clarity | 4 | 4 | |
| Risk coverage | 4 | 3 | V1 has negative checks and unspecified-behaviour gaps |
| Invariant and edge-case coverage | 3 | 3 | floor (1 of 5) met by both |
| **qual_score (of 30)** | **22 / 30 = 0.7333** | **23 / 30 = 0.7667** | |

Position-bias check (reading both orders): no verdict changed. Disagreements: 0.

## Combined Scoring
V1 = 0.5 x 0.9250 + 0.5 x 0.7333 = 0.8292. V2 = 0.5 x 0.9895 + 0.5 x 0.7667 = 0.8781. Margin 4.9 points, inside the 5% tiebreaker band, so the tiebreak applies.
Tiebreaker level 1 (diff points won): V1 11, V2 10: V1 leads by one. Level 2 (correctness criteria met): V2 5, V1 3: V2 leads. Level 2 decides.

## Selected Base: Variant 2 (reviewer 2, qa)
- Rationale: higher combined score, higher correctness count; its citations are exact.
- Strengths to preserve: exact line citations; spec-versus-plan drift findings (stale age, main-checkout predicate, staging); grouped coverage verdicts.
- Strengths to incorporate from V1: duplicate-row risk (F2), Task 8 `Decision:` gap (F3), empty-ledger case (F6), negative checks, calibrated grades for the scratch Run.
- Added from the invariant probe: INV-001, INV-002, INV-006 (HIGH) and the six MEDIUM entries.
