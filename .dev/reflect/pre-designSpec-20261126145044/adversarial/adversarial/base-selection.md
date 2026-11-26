# Base Selection

## Quantitative Scoring (50% weight)

Measured on the three cards. Requirement coverage (RC) is the share of the 16 consensus topics (C-001 to C-016) that a card raised: card 1 raised 11, card 2 raised 4, card 3 raised 12. Internal consistency, specificity (every finding cites file:line evidence) and dependency completeness measured equal at 1.00 for all cards; section coverage is equal (same keys).

| Metric | Weight | Card 1 | Card 2 | Card 3 |
|---|---|---|---|---|
| Requirement coverage | 0.30 | 11/16 = 0.6875 | 4/16 = 0.2500 | 12/16 = 0.7500 |
| Internal consistency | 0.25 | 1.00 | 1.00 | 1.00 |
| Specificity ratio | 0.15 | 1.00 | 1.00 | 1.00 |
| Dependency completeness | 0.15 | 1.00 | 1.00 | 1.00 |
| Section coverage | 0.15 | 1.00 | 1.00 | 1.00 |
| quant_score | | 0.9062 | 0.7750 | 0.9250 |

## Qualitative Scoring (50% weight)

Two independent passes (order 1, 2, 3 and order 3, 2, 1); full lines in `qual-pass1.md` and `qual-pass2.md`. The passes disagreed on 15 of 90 pairs; each was resolved on the evidence (see the log).

| Dimension | Card 1 | Card 2 | Card 3 |
|---|---|---|---|
| Completeness | 5/5 | 4/5 | 5/5 |
| Correctness | 5/5 | 5/5 | 5/5 |
| Structure | 3/5 | 5/5 | 4/5 |
| Clarity | 3/5 | 5/5 | 3/5 |
| Risk Coverage | 4/5 | 5/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 4/5 | 5/5 |
| **Total** | **25/30** | **28/30** | **26/30** |

### Position-bias log (15 disagreements)

| Pair | Final | Reason |
|---|---|---|
| 1 E4 | MET | F-10 is an off-by-one range (lines 152 to 159 against rows 153 to 158) |
| 1 L1 | NOT MET | only Blocking findings carry a reason (8 of 10 grades have none) |
| 1 L3 | NOT MET | the consequence field mostly holds a fix, not an impact |
| 1 S2 | NOT MET | `blocking_reason` appears on F-1 and F-2 only |
| 2 C3 | MET | F-3 names the prerequisite (injected mock transport and a fake key) |
| 2 E2 | MET | F-2 is a cross-component conversion (exception turned into a result the runner must read) |
| 2 E5 | NOT MET | F-2 links two plan parts but not an interaction between findings |
| 2 L4 | MET | F-4's consequence defines the whole-run preflight |
| 2 S4 | MET | ids F-1 to F-4 and line cross-references exist |
| 3 E4 | MET | F-3: one hash on `tests_passed` against several files checked |
| 3 L1 | NOT MET | Medium and Note findings carry `null` and no reason (same ruling as card 1) |
| 3 L3 | NOT MET | consequences mostly state the fix |
| 3 L4 | MET | F-1 spells the systemic cases out as status and error pairs |
| 3 R2 | MET | every consequence or recommendation names a fix |
| 3 S4 | MET | ids and line cross-references exist |

### Edge Case Floor Check

Card 1 5/5, card 2 4/5, card 3 5/5. The floor is 1/5; all cards are eligible.

## Combined Scoring

| Card | quant | qual | combined |
|---|---|---|---|
| 1 | 0.9062 | 0.8333 | 0.8698 |
| 2 | 0.7750 | 0.9333 | 0.8542 |
| 3 | 0.9250 | 0.8667 | 0.8958 |

Top two: card 3 (0.8958) and card 1 (0.8698); margin 0.0260, which is below 0.05, so the tiebreaker applies. Level 1 (diff points won, meaning the card's grade equals the final consensus grade): card 1 won 6, card 2 won 1, card 3 won 5.

## Selected Base: Card 1

- Rationale: the combined scores of the top two are within 5%; card 1 won more points where its grade matched the final consensus after Round 2.
- Strengths to preserve: card 1's calibration of grade against evidence, its Gate 1 `UNSET` finding (C-008) and its band-mapping finding (C-014).
- Strengths to incorporate: card 3's findings on missing artifacts (C-009, C-010, C-012), card 2's behavioural focus on Task 6 (C-002 to C-004), the invariant probe's four additions.
- Weaknesses of the base to fix: Blocking grade on C-005 and C-006 (fixable checks, downgraded to Medium), C-001 graded Medium (raised to Blocking, Missing), C-007 graded Medium (kept Medium after Round 2).
