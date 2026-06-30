# Base Selection

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (resolved) | Variant B (ours) | Variant C (theirs) |
|--------|--------|----------------------|------------------|--------------------|
| Requirement coverage (RC) — asserts production-true value | 0.30 | 1.00 | 1.00 | 0.00 (asserts false value) |
| Internal consistency (IC) — assertion vs production | 0.25 | 1.00 | 1.00 | 0.00 (test fails) |
| Specificity (SR) | 0.15 | 1.00 | 1.00 | 1.00 |
| Dependency completeness (DC) — rename completeness | 0.15 | 1.00 | 1.00 | 0.66 (comment+class stale) |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | **1.00** | **1.00** | **0.40** |

## Qualitative Scoring (50% weight)
Dominant criterion is Correctness #1 ("No factual errors") and Correctness #4 ("No internal contradictions"). Variant C fails both: it asserts a model string production does not emit. Executed evidence (pytest) is the verdict.

| Dimension | Variant A/B | Variant C |
|-----------|-------------|-----------|
| Correctness (test passes vs production) | MET | NOT MET (pytest: 1 failed) |
| Completeness (rename fully applied) | MET | NOT MET (Haiku class/comment remain) |
| **qual_score (indicative)** | ~1.00 | ~0.50 |

## Combined Scoring
- Variant A: (0.50 × 1.00) + (0.50 × 1.00) = **1.00**
- Variant B: **1.00** (identical to A)
- Variant C: (0.50 × 0.40) + (0.50 × 0.50) = **0.45**

## Selected Base: Variant A (resolved / proposed) — equivalently B (ours)
**Selection rationale**: A/B asserts the alias `"sonnet"` that production actually emits (`SONNET_MODEL = "sonnet"`, summarizer.py:51/331), completes the `Haiku→Sonnet` rename, and passes all 25 tests against production. Variant C's literal `claude-sonnet-4-5` assertion is empirically falsified (pytest `1 failed`) and contradicts the production guidance comment at summarizer.py:49.

**Strengths to preserve**: alias-based model assertion; complete rename; full green suite.
**Strengths to incorporate from C**: none — C is a strict subset of A/B's intent.
