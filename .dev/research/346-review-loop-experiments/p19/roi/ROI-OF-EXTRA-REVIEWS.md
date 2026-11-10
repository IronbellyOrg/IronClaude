# ROI of extra first-round reviews (18 runs, 72 reviewer reports, matched to the 44-defect ledger)

Data: first-round reports of 6 earlier PN1 runs (1 Sonnet + 3 Haiku) and the 12 ab5 runs (1 Sonnet + 3 Haiku); each reviewer finding was mapped by a blind Sonnet matcher to ledger defects D01-D44 (or none). Scripts: analyze.py, model2.py. Matches in matches/.

| measure | Sonnet reviewer (n=18) | Haiku reviewer (n=54) |
|---|---|---|
| distinct ledger defects raised per report | 16.8 (blocking 11.7; range 7-26) | 8.5 (blocking 5.4; range 3-15) |
| output tokens per report (ab5 runs) | about 75k | about 45k |

Marginal new ledger defects per added reviewer (Sonnet first, then Haiku): 16.8, +4.4, +3.0, +2.1. A 4-reviewer panel covers 26.3 of 44 on average; across 18 runs (72 reports) 43 of 44 are raised at least once (only D37 never). Pooled union of defects after k whole runs: 26, 33, 36, 37, 38, 39 (k=6), 41 (k=9), 42 (k=12), 43 (k=18). So the first 2 runs give 33 distinct defects, the next 4 add 6, the next 12 add 4 (Chao-style saturation near 43-44).

Conversion: P(defect fixed | raised by 0 reviewers) = 0.03; by 1 = 0.35; by 2 = 0.50; by 3+ = 0.58 (ab5 runs). By pipeline: panel variant 0.23/0.36/0.52, full variant 0.46/0.64/0.64. A defect raised only by Haiku reviewers is fixed 30% of the time, one raised by the Sonnet reviewer 47%.

Model (per-defect capture rates by reviewer type x conversion by number of raisers; bootstrap over runs; calibrated: model 12.0 vs observed 12.0 fixes at 1S+3H):
| panel | extra primary-lane cost | extra parallel cost | change in defects fixed (90% CI), panel variant | full variant |
|---|---|---|---|---|
| 1S+4H (+1 Haiku) | none | +45k | +1.1 (0.7, 1.5) | +1.2 (0.7, 1.6) |
| 1S+6H (+3 Haiku, "double the Haiku") | none | +135k | +2.7 (1.6, 3.9) | +2.8 (1.6, 4.0) |
| 2S+3H (+1 Sonnet) | +75k | none | +2.2 (1.5, 3.0) | +2.7 (1.9, 3.6) |
| 3S+3H (+2 Sonnet, cost-matched to ab5 full) | +150k | none | +3.9 (2.5, 5.6) | +4.3 (2.8, 6.0) |
| 2S+6H | +75k | +135k | +4.3 (2.7, 5.9) | +4.7 (2.9, 6.5) |
| 3S+6H | +150k | +135k | +5.6 (3.4, 7.9) | +5.9 (3.6, 8.2) |

Reading: ratio of added reviews to newly caught-and-fixed defects is about 1 fixed defect per extra Haiku report (declining: 1.2, 1.0, 0.8) and about 2.2-2.7 per extra Sonnet report; ROI is positive for both. Haiku reports are the cheaper lane (parallel, possibly free), so adding Haiku has the better per-token return; the Sonnet report has the better per-report return. Caveats: capture rates assume independence between reviewers and a fixed conversion rate (the reviser may saturate; rows going into ADJ and the reviser also grow with more reports), matcher is a single Sonnet judge, and the live Haiku stand-ins are not the live Tier 2/3 models.
