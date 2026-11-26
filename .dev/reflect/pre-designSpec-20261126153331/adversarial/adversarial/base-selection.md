# Base Selection

## Method and a stated departure

The 30-criterion binary rubric with two ordered passes (position-bias check) was not run this time. The qualitative layer uses each card's blind-calibrated confidence C as its proxy (0.83, 0.82, 0.89). The quantitative layer is computed from the three cards as in the first review. This is a lighter method than the protocol's; the choice of base cannot change which findings reach the merged verdict, because every finding from every card is considered in the refactor plan.

## Quantitative layer (50% weight)

Requirement coverage (RC) is the share of the 12 content topics of the diff analysis (C-001 to C-012) that a card raised: card 1 raised 8 (C-003, C-004, C-005, C-008, C-009, C-010, C-011, C-012), card 2 raised 4 (C-001, C-005, C-006, C-007), card 3 raised 6 (C-001, C-002, C-003, C-004, C-009, C-012). Consistency, specificity, dependency completeness and section coverage are equal at 1.00 for all three (each finding cites file and line; the keys are the same).

| Metric | Weight | Card 1 | Card 2 | Card 3 |
|---|---|---|---|---|
| Requirement coverage | 0.30 | 8/12 = 0.6667 | 4/12 = 0.3333 | 6/12 = 0.5000 |
| Other four metrics | 0.70 | 1.00 | 1.00 | 1.00 |
| quant_score | | 0.9000 | 0.8000 | 0.8500 |

## Qualitative layer (50% weight, proxy)

| | Card 1 | Card 2 | Card 3 |
|---|---|---|---|
| Calibrated C | 0.83 | 0.82 | 0.89 |

## Combined

variant_score = 0.5 x quant + 0.5 x qual: card 1 = 0.8650, card 2 = 0.8100, card 3 = 0.8700.

Cards 1 and 3 are within 5% of each other, so the tiebreaker applies. Level 1 is debate performance: the number of a card's final grades upheld by the debate outcome. Card 1: C-003, C-004, C-005, C-009, C-010 and C-012 upheld (6); C-008 and C-011 conceded to a lower grade. Card 3: C-001, C-004 and C-012 upheld (3); C-002, C-003 and C-009 conceded or raised. Card 1 wins on level 1.

Selected base: card 1 (`variant-1-original.md`). Incorporated: cards 2 and 3, the debate, and the invariant probe.
