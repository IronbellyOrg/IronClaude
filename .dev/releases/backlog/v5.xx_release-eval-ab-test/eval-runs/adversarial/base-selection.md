# Base Selection: Scoring & Ranking

## Methodology

For each proposal, the final Value and Complexity scores are computed as the average of Advocate and Skeptic scores (normalized to 1-10 scale where 10=highest value, 10=most complex). The **Priority Ratio** = Value / Complexity, representing value-per-unit-of-effort. Higher ratio = better ROI.

Where Advocate and Skeptic disagreed by >4 points on Value, a tiebreaker assessment was applied based on:
1. Strength of evidence from the actual eval run
2. Whether the spec already handles the concern
3. Whether the proposal addresses a systemic vs one-off problem

## Tiebreaker Resolutions

**Proposal A (gap: 5 points)**: Skeptic's argument that K eliminates the need is strong but incomplete — K (eval-mode) solves the *execution* gap, but evidence tiers remain useful for runs where eval-mode is not used (production evals). Split resolved toward Skeptic: Value adjusted to 5.

**Proposal G (gap: 4 points)**: Skeptic's argument that L2 correctly catches this is partially valid — if exit code is non-zero, L2 handles it. But the evidence shows exit code WAS 0. Split resolved toward Advocate slightly: Value adjusted to 5.

**Proposal I (gap: 3 points)**: Skeptic's argument that F + FR-EVAL.14 cover this is strong. Value stays at 3.5, rounded to 4.

## Final Scores

| Proposal | Final Value | Final Complexity | Priority Ratio | Rank |
|----------|------------|-----------------|----------------|------|
| C+L | 8.7 | 2.3 | **3.78** | 1 |
| K | 8.0 | 2.5 | **3.20** | 2 |
| F | 7.5 | 2.0 | **3.75** | 3 |
| B | 7.5 | 4.5 | **1.67** | 4 |
| M | 6.0 | 3.5 | **1.71** | 5 |
| E | 3.0 | 1.5 | **2.00** | 6 |
| D | 5.5 | 4.0 | **1.38** | 7 |
| A | 5.0 | 4.0 | **1.25** | 8 |
| G | 5.0 | 5.5 | **0.91** | 9 |
| H | 4.5 | 5.5 | **0.82** | 10 |
| J | 3.5 | 1.0 | **3.50** | 11 |
| I | 3.5 | 3.0 | **1.17** | 12 |

Note: J ranks 11th despite high ratio because its absolute value (3.5) is too low to justify a spec change — it is an implementation detail. The ranking uses ratio as primary sort but applies a minimum value threshold of 5.0 for "recommended" status.

## Verdict Categories

### ACCEPT (Value ≥ 7.0, clear evidence, manageable complexity)
1. **C+L**: Ternary verdict model — both analysts independently converged; eval literally violated spec
2. **K**: Eval-mode execution — addresses root cause of incomplete coverage
3. **F**: Partial run scoring — all 4 runs were PARTIAL; trivial implementation
4. **B**: Correct failure classification — spec-fidelity proved this gap exists

### CONSIDER (Value 5.0-6.9, or ratio ≥ 1.5 but needs more evidence)
5. **M**: Auto-detect LLM fabrication — clever structural test but narrow applicability
6. **E**: Duration variance — near-zero cost but weak signal; add as informational only

### DEFER (Value < 5.0 or complexity disproportionate to value)
7. **D**: Regression-guard mode — existing L4 can be configured for this
8. **A**: Code-level evidence tier — K eliminates most of the need
9. **G**: Gate rejection layer — pipeline-specific, L2 handles adequately
10. **H**: Per-step variance — premature with N=2 data
11. **J**: Worktree reuse — implementation detail
12. **I**: Minimum completeness — F + FR-EVAL.14 cover this
