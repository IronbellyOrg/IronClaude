# T1 blind calibration (confidence-calibrator, opus; card-only input)

Calibrated C = 0.55 (self-reported 0.72). Recommendation: ESCALATE.

| Dimension | Score |
|---|---|
| Citation grounding | 0.60 |
| Coverage completeness | 0.88 |
| Deviation-classification clarity | 0.30 |
| Risk surface coverage | 0.75 |
| Recommendation actionability | 0.20 |

Mean C = 0.55. The calibrator noted: no file:line anywhere in the card; the card says claude flag hunks are "below" but they are in the reviewer briefs (G11), not in the card; candidate deviations (a) to (c) carry no taxonomy label; the card has no recommendations. The T1 stop was already forbidden by the parse-density pre-filter (coverage_degraded: parsed-sparse); calibration agrees (C < 0.85, rule 6). `calibrator_diversity`: the calibrator ran on opus and one reviewer (refactorer) also runs on opus, so the disjoint set is not available in the built-in Anthropic class set: degraded.
