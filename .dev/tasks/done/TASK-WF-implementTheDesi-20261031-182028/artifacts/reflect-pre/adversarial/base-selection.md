# Base Selection

Method note: quantitative metrics computed by the orchestrator from the card text; the qualitative 30-criterion rubric was applied in ONE pass by the orchestrator (no separate reverse-order pass agent). This is a recorded deviation from the dual-pass position-bias step; the debate outcome (Step 2) is unanimous on the deciding points, so the deviation cannot change the base.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 | V2 | V3 |
|---|---|---|---|---|
| Requirement coverage (design sections touched / 14 design sections 4-17) | 0.30 | 0.57 | 0.64 | 0.57 |
| Internal consistency (1 - withdrawn or overturned claims / claims) | 0.25 | 0.70 (R1-3 loc, R1-7, R1-6 class overturned) | 0.71 (R2-11, R2-01 sev, R2-05, R2-12 class) | 0.82 (R3-F2 class, R3-F7 withdrawn) |
| Specificity (findings with file:line + concrete fix / findings) | 0.15 | 0.90 | 0.79 | 1.00 |
| Dependency completeness (citations that resolve / citations, per calibrators) | 0.15 | 1.00 | 0.93 | 1.00 |
| Section coverage (findings / max findings) | 0.15 | 0.71 | 1.00 | 0.79 |
| **quant_score** | | 0.75 | 0.79 | 0.81 |

## Qualitative Scoring (50% weight)

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness (5) | 2 | 4 | 2 |
| Correctness (5) | 3 | 3 | 5 |
| Structure (5) | 4 | 4 | 4 |
| Clarity (5) | 4 | 4 | 4 |
| Risk Coverage (5) | 3 | 3 | 4 |
| Invariant & Edge Case (5) | 2 | 2 | 3 |
| **qual_score (/30)** | 18 = 0.60 | 20 = 0.67 | 22 = 0.73 |

Edge-case floor: all variants ≥ 1/5, all eligible.

## Combined Scoring

| Variant | quant×0.5 | qual×0.5 | Total |
|---|---|---|---|
| V1 | 0.375 | 0.300 | 0.675 |
| V2 | 0.395 | 0.335 | 0.730 |
| V3 | 0.405 | 0.365 | 0.770 |

Margin V3 over V2: 0.040 (< 0.05) → tiebreaker level 1 (debate points won): V3 won C-002, C-003, X-001, X-004, part of C-006 (5); V2 won C-008, C-009, part of C-006 (3). V3 selected.

## Selected Base: Variant 3 (opus:refactorer)

- Strengths to preserve: X-001 analysis and fix; X-004 location; C-002 completion-time defect; C-005 count audit; U-009, U-010, U-011.
- Strengths to incorporate: V2's s9/S5 obligations (C-008 at medium, C-009, R2-06, R2-08, R2-13); V1's R1-2 (late tests, dry-check fallback), R1-9, R1-5 (loop-guard rewrite 37 -> 41), R1-6 equality test, explicit Task 9 list; invariant probe INV-001..INV-006 (and LOWs).
