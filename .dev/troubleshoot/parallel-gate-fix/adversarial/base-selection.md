# Base Selection

## Quantitative layer (0.50)
| Metric (weight) | A | B | Notes |
|---|---|---|---|
| Correctness on live case (0.30) | 0.5 | 1.0 | A passes only by introducing a Phase-6 FN; B has neither FP nor FN |
| Generality across lengths (0.25) | 0.2 | 1.0 | A: FP on short, FN on long; B: length-invariant |
| FP elimination (0.15) | 0.4 | 1.0 | A leaves residual FP (completion ≤ phase 5) |
| FN avoidance (0.15) | 0.3 | 0.9 | A drops work-phase 6+ checks; B keeps all work phases |
| Immediate unblock (0.15) | 1.0 | 1.0 | tie (INV-001) |
| **Quant** | **0.43** | **0.985** | |

## Qualitative layer (0.50) — selected criteria
- Correctness: A 2/5 (fixes instance, breaks coverage), B 5/5.
- Structure/consistency: B 5/5 (symmetric with existing Phase-1 exemption), A 3/5.
- Clarity/maintainability: A 2/5 (magic 5, falsified convention), B 4/5.
- Risk coverage: A 3/5 (low mechanical risk but high semantic risk), B 4/5.
- Edge/invariant coverage: A 2/5, B 4/5 (handles N≤2, non-contiguous phases via max()).
- **Qual:** A ≈ 0.40, B ≈ 0.88.

## Combined
- A = 0.50×0.43 + 0.50×0.40 = **0.42**
- B = 0.50×0.985 + 0.50×0.88 = **0.93**
- Margin: 51 pts — far outside the 5% tiebreaker band. **No tiebreaker needed.**

## Selected base: **Variant B (exempt final phase)**
**Strengths to preserve:** semantic final-phase exemption; symmetry with the existing Phase-1 (setup) exemption; length-invariance.
**Strength to graft from A (U-001):** keep the change *small and self-contained* — implement B as a tight, well-tested helper edit, not a refactor; preserve the existing early-return and error-message wire string so nothing downstream shifts.
