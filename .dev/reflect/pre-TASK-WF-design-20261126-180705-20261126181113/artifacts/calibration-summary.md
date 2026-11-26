# Blind calibration summary (run 2)

The `confidence-calibrator` agent (opus class, so calibrator diversity is degraded: every class was also a reviewer) re-graded each card without the formation context. Scores are as returned in the session; the per-card calibration transcripts were not saved to separate files in this run (disclosed gap).

| Card | Self-reported | Calibrated |
|---|---|---|
| Tier 1 card (`t1-card.md`) | 0.75 | 0.54 |
| reviewer 1 (analyzer, sonnet) | n/a | 0.70 |
| reviewer 2 (qa, haiku) | n/a | 0.82 |
| reviewer 3 (refactorer, opus) | n/a | 0.74 |

`confidence_calibrated` in the contract is the mean of the three reviewer cards: 0.753, written as 0.75.
