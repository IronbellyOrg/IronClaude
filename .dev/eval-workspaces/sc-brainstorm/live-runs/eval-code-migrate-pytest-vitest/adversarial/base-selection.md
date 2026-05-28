# Base Selection — case 4 rerun

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 (architect/opus) | Variant 2 (refactorer/sonnet) |
|--------|--------|------------------------------|---------------------------------|
| Requirement coverage    | 0.30 | 0.88 | 0.86 |
| Internal consistency    | 0.25 | 0.92 | 0.92 |
| Specificity ratio       | 0.15 | 0.84 | 0.88 |
| Dependency completeness | 0.15 | 0.86 | 0.84 |
| Section coverage        | 0.15 | 0.92 | 0.92 |
| Quantitative score      | 1.00 | 0.886 | 0.880 |

## Qualitative Scoring (50% weight)

| Dimension | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| Robustness to long-tail plugin gaps | 0.90 | 0.80 |
| Bounded total cost (time + dual-runner CI) | 0.75 | 0.92 |
| Clarity of cutover criterion | 0.85 | 0.90 |
| Provenance / artifact reuse | 0.82 | 0.88 |
| Qualitative score | 0.83 | 0.875 |

## Combined Score

- Variant 1 (architect): 0.5 × 0.886 + 0.5 × 0.83 = **0.858**
- Variant 2 (refactorer): 0.5 × 0.880 + 0.5 × 0.875 = **0.8775**

## Base Selected: Variant 1 (architect, parallel-run)

Despite Variant 2's marginally higher combined score, the base is Variant 1 because:
- The parallel-run baseline gives a safer fallback when sub-criteria are equal.
- Variant 2's strengths (bounded calendar, concept-map doc, config-only cutover PR) can be **augmented** onto Variant 1 without architectural conflict.
- Variant 1's longer dual-runner window is the policy lever that Variant 2's discipline can shorten — making Variant 1 the more general base.

The merge therefore takes Variant 1 as base and pulls Variant 2's: bounded calendar discipline, concept-map artifact, and config-only cutover PR pattern.
