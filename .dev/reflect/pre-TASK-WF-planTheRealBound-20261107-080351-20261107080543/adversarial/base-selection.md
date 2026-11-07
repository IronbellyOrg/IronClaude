# Base Selection

Scoring was done by the orchestrator in one pass. The position-bias mitigation (a second evaluation in reverse order with disagreement resolution) was NOT run as a separate evaluator pass; this is a recorded deviation and it lowers confidence in the margin between V1 and V3.

## Quantitative Scoring (50% weight)
Source "requirements" for these cards are the 18 content themes C-001..C-018 of diff-analysis.md (the cards carry no requirement IDs, so the topic-level fallback applies).

| Metric | Weight | V1 | V2 | V3 | Computation |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.67 | 0.33 | 0.67 | V1 covers 12 of 18 themes (C-001..006, 008, 011..015); V2 covers 6 (C-001, 002, 007, 009, 010, 017); V3 covers 12 (C-001..007, 013, 014, 016, 017, 018) |
| Internal consistency (IC) | 0.25 | 0.92 | 0.83 | 0.96 | one conceded overgeneralization in V1 (R1-01), one overstated claim in V2 (QA-3), none conceded in V3 |
| Specificity ratio (SR) | 0.15 | 0.90 | 0.85 | 0.90 | share of findings with a file:line citation; V2 cites "plan lines" without a path |
| Dependency completeness (DC) | 0.15 | 0.95 | 0.90 | 0.95 | cited references that resolved on Read |
| Section coverage (SC) | 0.15 | 1.00 | 0.50 | 0.50 | V1 has two sections (`verified_true_claims`, `findings`); V2 and V3 one |
| **quant_score** | | **0.859** | **0.644** | **0.794** | RC×0.30 + IC×0.25 + SR×0.15 + DC×0.15 + SC×0.15 |

## Qualitative Scoring (50% weight), additive binary rubric (criteria met out of 5 per dimension, evidence is the finding ids and file:line cited in the cards and rebuttals)
| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4 | 3 | 4 |
| Correctness | 4 | 4 | 5 |
| Structure | 3 | 3 | 3 |
| Clarity | 4 | 4 | 4 |
| Risk coverage | 4 | 3 | 4 |
| Invariant and edge-case coverage | 4 | 3 | 4 |
| **total of 30** | **23** | **20** | **24** |
| **qual_score** | **0.767** | **0.667** | **0.800** |

Edge-case floor (at least 1 of 5): all three variants pass.

## Combined Scoring
| | V1 | V2 | V3 |
|---|---|---|---|
| 0.50 × quant | 0.430 | 0.322 | 0.397 |
| 0.50 × qual | 0.383 | 0.333 | 0.400 |
| **variant_score** | **0.813** | **0.656** | **0.797** |

Margin V1 over V3: 0.016, inside the 5% tiebreaker band.

## Tiebreaker
- Level 1 (debate performance, points won in the debate-transcript scoring matrix): V1 wins C-003, C-004, C-005, C-006, C-008, C-011, C-012, C-015, S-002 (9); V3 wins C-001 (severity), C-013, C-014, C-016, C-018 (5) with C-017 shared. V1 leads.
- Tiebreaker applied: yes (level 1). Evidence: points won.

## Selected Base: Variant 1 (analyzer card, sonnet-class)
- Selection rationale: highest combined score and the tiebreaker win; the only card that checked the plan against the helper and the live probe.
- Strengths to preserve: feasibility findings R1-01 (reparent shape only), R1-02, R1-03, R1-05, R1-08, R1-09; the verified-versus-inferred separation.
- Strengths to incorporate from non-base variants: V3 severity ordering (R3-F1 high, R3-F13 folded in), R3-F3 merged with QA-6, R3-F6 baseline, R3-F7, R3-F8 (low, both tasks), R3-F5 low; V2 QA-3 (medium, reworded), QA-4 (narrowed to Task 2 criterion 1, Task 6, Task 7), QA-5, QA-2 merged with R3-F11.
- Probe-sourced additions (undebated): INV-001 to INV-011 as listed in invariant-probe.md.
