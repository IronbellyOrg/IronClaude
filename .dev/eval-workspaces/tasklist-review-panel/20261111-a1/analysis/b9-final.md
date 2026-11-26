| Combo | Models | Runs | Defect-rich found /14 mean (range) | Blocking /8 mean (range) | Wrong blockers (DR) | Control found /2 | Control wrong blk | Tokens (mean) | Wall: reviewer-s summed / elapsed s | Found per 100k tokens |
|---|---|---|---|---|---|---|---|---|---|---|
| 2x luna + 2x ember (g6) | luna x2, ember x2 | 4 | 1.8 (1-3) | 0.5 (0-1) | 4.8 | 0.25 | 1.50 | 91,416 | 855 / 342 | 1.9 |
| haiku + 2x luna + 2x ember (h1) | haiku, luna x2, ember x2 | 4 | 2.2 (2-3) | 1.8 (1-3) | 3.0 | 1.00 | 1.75 | 246,213 | 1,537 / 682 | 0.9 |
| sonnet + 2x luna + 2x ember (h2) | sonnet, luna x2, ember x2 | 4 | 2.2 (2-3) | 0.8 (0-1) | 3.5 | 1.50 | 0.25 | 189,325 | 1,636 / 738 | 1.2 |
| (ref) haiku + 2x luna | haiku, luna x2 | 5 | 2.2 (2-3) | 1.4 (1-2) | 3.0 | 0.80 | 1.60 | 191,018 | 1,355 / 715 | 1.2 |
| (ref) sonnet + ember | sonnet, ember | 4 | 2.5 (2-4) | 0.2 (0-1) | 0.2 | 0.75 | 1.25 | 142,967 | 910 / 766 | 1.7 |
| (ref) sonnet + luna + ember | sonnet, luna, ember | 5 | 2.2 (2-3) | 0.6 (0-1) | 2.0 | 0.80 | 1.00 | 138,551 | 1,135 / 676 | 1.6 |
| (ref) ember + luna | ember, luna | 4 | 2.2 (2-3) | 0.5 (0-1) | 2.0 | 0.00 | 1.50 | 52,398 | 432 / 300 | 4.3 |

| Effect of adding one reviewer | Runs | Delta defect-rich found | Delta blocking | Delta wrong blockers | Delta control found | Delta tokens | Delta wall (reviewer-s / elapsed) |
|---|---|---|---|---|---|---|---|
| adding haiku to 2x luna + 2x ember | 4 vs 4 | +0.50 (within noise) | +1.25 (beyond noise) | -1.8 | +0.75 (beyond noise) | +154,797 | +682 / +339 |
| adding sonnet to 2x luna + 2x ember | 4 vs 4 | +0.50 (within noise) | +0.25 (within noise) | -1.2 | +1.25 (beyond noise) | +97,909 | +781 / +396 |
| 2nd luna + 2nd ember on top of sonnet + luna + ember | 4 vs 5 | +0.05 (within noise) | +0.15 (within noise) | +1.5 | +0.70 (within noise) | +50,774 | +501 / +62 |
| 2x luna + 1 more ember on top of sonnet + ember | 4 vs 4 | -0.25 (within noise) | +0.50 (within noise) | +3.2 | +0.75 (within noise) | +46,358 | +726 / -28 |
| 2x ember on top of haiku + 2x luna | 4 vs 5 | +0.05 (within noise) | +0.35 (within noise) | +0.0 | +0.20 (within noise) | +55,194 | +182 / -33 |
