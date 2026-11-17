# Base Selection

Method note (recorded deviation, `fallback_mode: true`): the variants are 4 to 7 finding reviewer cards, not long documents. The 5 quantitative metrics were computed by the orchestrator by hand over the card text with the "source requirements" replaced by the 11 findings retained after the debate; the 30-criterion rubric was scored at dimension level with one evidence line per dimension rather than 30 CEV rows; the reverse-order second pass was NOT run. Treat the scores as an approximation, not a repeatable computation.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 | V2 | V3 | Basis |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.364 | 0.545 | 0.364 | retained findings present in the card: 4/11, 6/11, 4/11 |
| Internal consistency (IC) | 0.25 | 1.000 | 0.857 | 0.750 | claims withdrawn or downgraded after debate: 0/4, 1/7, 1/4 plus 2 bad citations |
| Specificity (SR) | 0.15 | 0.90 | 0.90 | 0.90 | all cards quote lines; not discriminating, held equal |
| Dependency completeness (DC) | 0.15 | 1.00 | 0.95 | 0.80 | citation ranges that resolve: V2 has 2 off-by-one ranges, V3 has 2 unresolvable ranges |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | each card has a body and a findings block |
| quant_score | | 0.794 | 0.805 | 0.702 | |

## Qualitative Scoring (50% weight), dimension level

| Dimension (5 each) | V1 | V2 | V3 | Evidence (one line) |
|---|---|---|---|---|
| Completeness | 3 | 4 | 3 | V2 has 7 findings across tests, verbs and artifacts; V1 and V3 have 4 |
| Correctness | 5 | 4 | 3 | V1 no finding withdrawn; V2 C-012 withdrawn; V3 has 2 bad citations and a weak finding |
| Structure | 4 | 4 | 4 | all use the findings-v2 block |
| Clarity | 4 | 4 | 4 | |
| Risk coverage | 2 | 3 | 2 | V2 covers the blocking L3 wording and phrase-only checks; V3 holds the blocking Task 8 item |
| Invariant and edge case coverage | 3 | 2 | 1 | V1 has state-mechanics findings (slack, cycle id); V3 has one |
| Subtotal /30 | 21 | 21 | 17 | |
| qual_score | 0.700 | 0.700 | 0.567 | |

Edge-case floor (1/5): V1 3, V2 2, V3 1; all eligible (V3 at the floor).

## Combined Scoring

| Variant | 0.5 quant + 0.5 qual |
|---|---|
| V1 (reviewer-1, analyzer) | 0.747 |
| V2 (reviewer-2, qa) | 0.753 |
| V3 (reviewer-3, refactorer) | 0.634 |

Top two are within 5%. Tiebreaker level 1 (debate points won): V2 won 6 (S-002, C-003, C-008, C-009, C-010, C-011), V1 won 3 (C-004, C-005, C-006). V2 wins.

## Selected Base: Variant 2 (reviewer-2, qa, Claude Haiku class)

Strengths to preserve: 7-finding breadth; test-adequacy lens; the Task 9 contradiction.
Strengths to incorporate: V3 C-001 (Task 8 omission, now blocking, with source 240); V1 C-004, C-005, C-006; V3 C-007 (corrected citation); fault-finder INV-004 to INV-006.
