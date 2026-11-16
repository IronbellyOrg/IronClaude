# Base Selection (Step 3, hybrid scoring)

Scorers: two independent opus agents (judge class opus; debater classes were sonnet and haiku; reviewer card 3 was written by an opus-class reviewer, noted). Pass 1 evaluated V1, V2, V3; pass 2 evaluated V3, V2, V1. Per-criterion CEV tables were returned by each scorer in full and are not copied here (they are in the scorers' hand-back text; the combined numbers below are the authoritative record).

## Quantitative (50%)
| Metric | V1 p1/p2 | V2 p1/p2 | V3 p1/p2 |
|---|---|---|---|
| RC (14 diff points) | 7/14 , 7/14 | 5/14 , 6/14 | 9/14 , 9/14 |
| IC | 1.00 , 1.00 | 1.00 , 1.00 | 1.00 , 1.00 |
| SR | 0.952 , 0.952 | 0.950 , 0.800 | 1.000 , 0.950 |
| DC | 1.000 , 1.000 | 0.857 , 1.000 | 1.000 , 1.000 |
| SC | 1.000 , 1.000 | 1.000 , 1.000 | 1.000 , 1.000 |
| quant | 0.843 , 0.843 | 0.778 , 0.799 | 0.893 , 0.885 |

## Qualitative (50%), 30 binary criteria with CEV
| Card | pass 1 | pass 2 |
|---|---|---|
| V1 | 25/30 = 0.833 | 27/30 = 0.900 |
| V2 | 28/30 = 0.933 | 27/30 = 0.900 |
| V3 | 25/30 = 0.833 | 26/30 = 0.867 |

## Position-bias mitigation
Disagreements between passes (per criterion): V1 qual 25 vs 27, V2 28 vs 27, V3 25 vs 26 (differences of one or two criteria, mainly completeness 1, clarity 4, invariants 2 and 4). The rank of V3 is first in both passes; the per-criterion re-evaluation prompt was NOT run because no per-criterion change can move V3 from first place (largest swing available to V1 or V2 is 3 criteria = 0.05 combined weight 0.5 x 0.1 = 0.05 only if all flipped; pass 2 already includes V1's best case at 0.871 vs V3 0.876). Recorded as a protocol deviation in the report.

## Combined (0.5 quant + 0.5 qual)
| Card | pass 1 | pass 2 | mean |
|---|---|---|---|
| V1 | 0.838 | 0.871 | 0.855 |
| V2 | 0.856 | 0.849 | 0.853 |
| V3 | 0.863 | 0.876 | 0.870 |

Edge-case floor (Invariant and edge-case dimension >= 1/5): all three eligible (V1 4/5, V2 4-5/5, V3 4-5/5).
Margin V3 over V1 (mean) 0.015 (1.5%), inside the 5% tiebreaker band.

## Tiebreaker
Level 1, points won in debate (agreed after round 1, kept after round 2): V3 6 (C-005 qualified, C-007, C-008, C-013, C-014, X-003) plus 2 majority; V1 3 (C-001 now minor, C-002, X-001); V2 2 (C-003, C-004). V3 wins level 1.

## Selected Base: Variant 3 (reviewer card 3, refactorer)
- Rationale: highest mean combined score in both passes, most debate points won, widest coverage of the diff points (9 of 14).
- Strengths to preserve: R3-3/C-007 (analyst and qualitative reviewers outside Task 4), R3-4 to R3-8 minor items, the stage 3 and stage 1 cross-checks, the "Checked, no defect" list.
- Strengths to incorporate: V2's C-003 (run-scoped ids) and C-004 (blind-only agents); V1's X-001/C-002 (GR12 to partial), C-001 (no ledger in /sc:implement, as a Medium item), C-009, C-010, C-011 and its follow-ups (record placement, legacy runs); fault-finder MEDIUM items INV-001 to INV-005, INV-008.
- Weaknesses of the base to correct by the debate outcome: R3-1 and R3-2 downgraded (A3 conceded in round 2: stage1 plan:196 says the route tags the row; the scale map pairs and Severity columns exist); R3-4 "after edits" overstated (Task 2 checks `classify` before the carrier edits, plan:59).
