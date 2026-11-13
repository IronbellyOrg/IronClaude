| Combo | Models | 2x model | Runs | Defect-rich found /14 mean (range) | Blocking /8 mean (range) | Wrong blockers (DR) | Control found /2 | Control wrong blk | Tokens (mean) | Wall: reviewer-s summed / elapsed s |
|---|---|---|---|---|---|---|---|---|---|---|
| ember + luna (1x baseline) | ember, luna | - | 4 | 2.2 (2-3) | 0.5 (0-1) | 2.0 | 0.00 | 1.50 | 52,398 | 432 / 300 |
| ember + 2x luna | ember, luna x2 | luna 2x | 6 | 1.8 (1-2) | 1.0 (1-1) | 1.8 | 0.83 | 0.83 | 63,644 | 761 / 348 |
| 2x ember + luna | ember x2, luna | ember 2x | 5 | 1.6 (1-2) | 1.0 (1-1) | 1.8 | 0.60 | 1.20 | 84,527 | 597 / 322 |
| 2x luna + 2x ember | luna x2, ember x2 | luna 2x, ember 2x | 4 | 1.8 (1-3) | 0.5 (0-1) | 4.8 | 0.25 | 1.50 | 91,416 | 855 / 342 |
| ember + terra | ember, terra | - | 4 | 0.5 (0-1) | 0.2 (0-1) | 2.8 | 0.50 | 1.25 | 37,255 | 266 / 162 |
| sonnet + ember | sonnet, ember | - | 4 | 2.5 (2-4) | 0.2 (0-1) | 0.2 | 0.75 | 1.25 | 142,967 | 910 / 766 |
| sonnet + luna + ember | sonnet, luna, ember | - | 5 | 2.2 (2-3) | 0.6 (0-1) | 2.0 | 0.80 | 1.00 | 138,551 | 1,135 / 676 |
| haiku + ember + terra | haiku, ember, terra | - | 5 | 2.0 (2-2) | 0.6 (0-1) | 3.2 | 1.00 | 1.40 | 191,128 | 971 / 684 |
| haiku + 2x luna | haiku, luna x2 | luna 2x (no 1x baseline) | 5 | 2.2 (2-3) | 1.4 (1-2) | 3.0 | 0.80 | 1.60 | 191,018 | 1,355 / 715 |
| (ref, single run) grok + ember + luna | grok, ember, luna | - | 1 | 2.0 (2-2) | 1.0 (1-1) | 4.0 | 1.00 | 0.00 | 240,961 | 4,401 / 3,897 |
| (ref, single run) haiku + ember + luna | haiku, ember, luna | - | 1 | 2.0 (2-2) | 1.0 (1-1) | 2.0 | 0.00 | 1.00 | 264,641 | 1,412 / 910 |
| (ref, single run) haiku + 2x ember | haiku, ember x2 | ember 2x | 1 | 2.0 (2-2) | 1.0 (1-1) | 2.0 | 0.00 | 2.00 | 197,084 | 843 / 609 |

| Doubling vs the 1x baseline (ember + luna) | Runs (2x vs 1x) | Delta defect-rich found | Delta blocking | Delta wrong blockers | Delta control found | Delta tokens | Delta wall (reviewer-s / elapsed) |
|---|---|---|---|---|---|---|---|
| 2nd luna (ember + luna x2 vs ember + luna) | 6 vs 4 | -0.42 (within noise) | +0.50 (within noise) | -0.2 | +0.83 (beyond noise) | +11,246 | +329 / +47 |
| 2nd ember (ember x2 + luna vs ember + luna) | 5 vs 4 | -0.65 (within noise) | +0.50 (within noise) | -0.2 | +0.60 (beyond noise) | +32,129 | +164 / +22 |
| 2nd luna AND 2nd ember | 4 vs 4 | -0.50 (within noise) | +0.00 (within noise) | +2.8 | +0.25 (within noise) | +39,018 | +423 / +42 |
| 2nd ember on top of 2x luna | 4 vs 6 | -0.08 (within noise) | -0.50 (within noise) | +2.9 | -0.58 (within noise) | +27,772 | +94 / -5 |
| 2nd luna on top of 2x ember | 4 vs 5 | +0.15 (within noise) | -0.50 (within noise) | +3.0 | -0.35 (within noise) | +6,889 | +258 / +20 |

| Model | 1x panels: at least one reviewer raises control GT2 | 2x panels: at least one of the two raises it |
|---|---|---|
| luna | 1/4 | 5/6 |
| ember | 2/4 | 3/5 |
