# Base Selection (Step 3)

## Quantitative Scoring (50% weight)

| Metric | Weight | R1 | R2 | R3 |
|---|---|---|---|---|
| Requirement coverage (3 INF rows touched) | 0.30 | 0.67 (2 rows) | 0.67 (2 rows) | 0.33 (1 row) |
| Internal consistency (1 - contradictions/claims) | 0.25 | 0.67 (X-002) | 1.00 | 0.67 (label inconsistency, conceded) |
| Specificity ratio | 0.15 | 0.80 | 0.60 | 0.85 |
| Dependency completeness (citations resolve) | 0.15 | 0.60 (no disk citations) | 0.40 (zero disk citations) | 1.00 (test:228/253 resolve) |
| Section coverage | 0.15 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | 0.70 | 0.73 | 0.73 |

## Qualitative Scoring (50% weight) — blind calibration (disjoint-set empty: calibrator_diversity degraded)

| Dimension | R1 | R2 | R3 |
|---|---|---|---|
| Blind calibrated card score | 0.66 | 0.55 | 0.82 |
| **qual_score (calibration as proxy)** | 0.66 | 0.55 | 0.82 |

## Combined Scoring

| Variant | Combined | Rank |
|---|---|---|
| R3 (refactorer/opus) | 0.78 | **1 — BASE** |
| R2 (qa/haiku) | 0.64 | 2 |
| R1 (analyzer/sonnet) | 0.68 | 2 |

Margin R3 vs R1: 0.10 (> 5%, no tiebreaker). Edge-case floor: all cards carry at least one invariant/edge finding (R3 F4 root cause, R2 F2 row-integrity, R1 F3 gate boundary) — floor satisfied.

## Selected Base: Variant 3 (refactorer/opus)

Rationale: highest blind calibration (0.82), only disk-grounded card (test:228/253), only causal finding (F4), most complete divergence inventory (all three text deltas). Debate confirmed: C-001 winner with both opponents endorsing R3's citations; R1's Round-2 shift ("MAJOR — I shift from MINOR") ratifies the base's central finding.

Strengths to preserve: F1's complete divergence inventory; disk grounding; severity/blocking discipline.
Strengths to incorporate: R1's plan-side citation pair (26/45) and archive-context (reworded per INV-007); R2's matrix-record and evidence-visibility lenses (U-001/U-002 with probe repairs); R1's U-004 gate-ambiguity residue (with INV-008 observable-effect note).
Changes from invariant probe (mandatory repairs): INV-001 citation-set correction; INV-003 matrix-record disposition; INV-002 count fix; INV-005 verification-strength leg dropped; INV-006 rationale corrected; INV-008 effect note added.
