# Base Selection (Hybrid Scoring)

## Quantitative Layer (weight 0.50)

| Variant | Req Coverage (0.30) | Internal Consistency (0.25) | Specificity Ratio (0.15) | Dependency Completeness (0.15) | Section Coverage (0.15) | quant_score |
|---------|---------------------|-----------------------------|--------------------------|--------------------------------|-------------------------|-------------|
| A (unmediated) | 1.00 | 1.00 | 0.95 | 1.00 | 1.00 | 0.99 |
| B (sc:reflect-degraded) | 1.00 | 0.95 | 0.95 | 1.00 | 0.85 | 0.96 |
| C (sc:troubleshoot) | 1.00 | 0.95 | 0.95 | 1.00 | 0.95 | 0.97 |

(Req coverage = 3 theories with mechanism+evidence+confidence+fix; all three deliver. B loses on section-coverage for the absent reflect-tool-output section.)

## Qualitative Layer (weight 0.50, 30-criterion rubric)

| Variant | Completeness (5) | Correctness (5) | Structure (5) | Clarity (5) | Risk Coverage (5) | Edge Case (5) | qual_score |
|---------|------------------|------------------|----------------|--------------|---------------------|----------------|-------------|
| A | 5/5 | 5/5 | 5/5 | 5/5 | 4/5 | 4/5 | 28/30 = 0.93 |
| B | 4/5 | 5/5 | 5/5 | 5/5 | 4/5 | 3/5 | 26/30 = 0.87 |
| C | 5/5 | 5/5 | 5/5 | 4/5 | 5/5 | 4/5 | 28/30 = 0.93 |

Edge-case floor: all variants ≥1/5 — no ineligibility.

## Combined Scoring

| Variant | Quant (0.50) | Qual (0.50) | Total |
|---------|--------------|-------------|-------|
| A | 0.495 | 0.465 | **0.960** |
| B | 0.480 | 0.435 | 0.915 |
| C | 0.485 | 0.465 | **0.950** |

## Tiebreaker
- A and C within 1% (0.960 vs 0.950) → invoke tiebreaker
- L1 debate performance: A=1 point won (S-002), C=0 explicit points (but MERGE outcomes for C-003/X-001 favor C's framing) → A wins L1 narrowly
- L1 alt reading: convergence-rich; both produced reusable framings
- L2 correctness criteria: A=5/5, C=5/5 → tie
- L3 input order: A is index 1 → **A wins**

## Selected Base: Variant A (unmediated direct-read)

**Rationale**: A's Cross-theory implications section provides unique analytical lift (compounding T1×T2, T3-upstream framing) that neither B nor C contains. A is also the most complete on substrate-vs-H3 fidelity caveats. C's C2 (pin tests) and B's B3 (verdict-asymmetry) are KEEP-and-integrate, not displace-the-base.
