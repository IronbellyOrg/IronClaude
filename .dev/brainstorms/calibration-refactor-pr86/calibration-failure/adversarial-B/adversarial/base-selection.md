# Base Selection — Hybrid Scoring

## Quantitative Layer (weight 0.50)

| Metric | Weight | A | B | C |
|---|---|---|---|---|
| Requirement coverage (3 theories + evidence + fix) | 0.30 | 1.00 | 1.00 | 0.95 |
| Internal consistency (no contradictions in own claims) | 0.25 | 1.00 | 1.00 | 1.00 |
| Specificity ratio (concrete file:line citations / claims) | 0.15 | 0.95 | 1.00 | 0.90 |
| Dependency completeness (resolved internal refs) | 0.15 | 1.00 | 1.00 | 0.95 |
| Section coverage (vs max sections across variants) | 0.15 | 0.85 | 1.00 | 0.95 |
| **Quant subscore** | | **0.970** | **1.000** | **0.948** |

## Qualitative Layer (weight 0.50) — 30-criterion rubric

| Dimension | A met | B met | C met |
|---|---|---|---|
| Completeness (5) | 5/5 | 5/5 | 5/5 |
| Correctness (5) | 5/5 | 5/5 | 4/5 (C3 confidence 0.45 is barely above noise; weakens correctness of stated framing) |
| Structure (5) | 5/5 | 4/5 (heavy reflection-meta in §1 dilutes theory density) | 5/5 |
| Clarity (5) | 4/5 (T3 stripped-context is most abstract) | 5/5 | 4/5 (meta-recursive section is dense) |
| Risk Coverage (5) | 5/5 | 5/5 | 4/5 (does not name verdict-direction asymmetry as a risk) |
| Invariant & Edge Case (5) | 4/5 | 5/5 (verdict-direction is an edge case the rubric misses) | 5/5 (eval-suite pin tests are invariant guards) |
| **Total** | **28/30** | **29/30** | **27/30** |
| **Qual subscore** | **0.933** | **0.967** | **0.900** |

## Combined Score

| Variant | quant×0.50 | qual×0.50 | Combined |
|---|---|---|---|
| A | 0.485 | 0.467 | **0.952** |
| B | 0.500 | 0.483 | **0.983** |
| C | 0.474 | 0.450 | **0.924** |

**Position-bias check (reverse-order C, B, A)**: B remains top; ranking stable.

## Tiebreaker
Top variants within 5%? A (0.952) and B (0.983) differ by 3.2% → within tiebreaker zone.
- Level 1 (debate performance — points won in Step 2): B won 3 diff points (C-001, C-002, C-003) vs A's 1 (U-003) and C's 1 (U-001). **B wins.**

## Base Selection: Variant B

**Rationale**:
- Highest combined score (0.983) and highest debate-points-won (3).
- Cleanest, most-implementable systemic fixes (equation-shaped).
- Honest §1 about /sc:reflect channel degradation increases meta-integrity.
- Verdict-direction asymmetry (B3) is the most decision-theoretically novel third theory.

**Non-base contributions to integrate**:
- A's cross-theory implications section (multiplicative compounding of T1×T2; T3 upstream).
- C's Theory 2 — eval suite silent-green coverage / pin-test prescription (becomes Theory M4 in merge).
- A's substrate-vs-H3 fidelity caveat (most explicit framing of the inference gap).
