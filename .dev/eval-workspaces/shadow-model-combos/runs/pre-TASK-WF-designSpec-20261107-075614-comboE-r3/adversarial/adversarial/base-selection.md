# Base Selection (Step 3)

Limits of this run (stated up front): scoring was done by the orchestrator in ONE pass. The dual-pass position-bias check (reverse-order evaluation with disagreement resolution) was NOT run, and the 30 per-criterion Claim-Evidence-Verdict tables are replaced by per-dimension subtotals with the evidence named below. Source "requirements" for the quantitative layer are the 14 merged findings M-001..M-014 of the final verdict (the debate's own outcome), so requirement coverage measures how much of the settled finding set a card contains.

## Quantitative Scoring (50% weight)
| Metric | Weight | Variant 1 | Variant 2 | Variant 3 |
|--------|--------|-----------|-----------|-----------|
| RC requirement coverage (merged findings contained) | 0.30 | 0.50 (7 of 14: M-001, 003, 004, 007, 008, 009, 014) | 0.21 (3 of 14: M-005, 010, 011) | 0.14 (2 of 14: M-003, 012) |
| IC internal consistency (1 minus defective claims / claims) | 0.25 | 0.79 (3 of 14 claims overstated or dropped: F11, F12, blocking flags) | 0.67 (2 of 3 claims carry a wrong locator) | 1.00 |
| SR specificity ratio | 0.15 | 0.95 | 0.90 | 0.95 |
| DC dependency completeness (references that resolve in the real files) | 0.15 | 0.97 | 0.70 | 1.00 |
| SC section coverage | 0.15 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | **0.786** | **0.621** | **0.735** |

## Qualitative Scoring (50% weight), single pass, subtotals
| Dimension (5 criteria each) | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|
| Completeness | 4 | 2 | 2 | V1 covers tables 4.1/4.2, fold, events; V2 acceptance criteria only; V3 two items |
| Correctness | 3 | 3 | 5 | V1 overstated blocking on 6 findings (conceded in Round 2); V2 locators wrong; V3 all verified |
| Structure | 4 | 4 | 4 | all use the findings-v2 schema and card layout |
| Clarity | 4 | 4 | 4 | claims within 300 characters, quotes present |
| Risk coverage | 4 | 2 | 2 | V1 names resume, reconcile, CI trigger; others name AC-level risks |
| Invariant and edge case coverage | 3 | 1 | 1 | V1 touches fold restore, key suffix, HOLD semantics; floor of 1/5 met by all |
| **qual_score (of 30)** | 22 / 0.733 | 16 / 0.533 | 18 / 0.600 | |

Edge Case Floor Check: V1 3/5, V2 1/5, V3 1/5, all eligible (floor 1/5).

## Combined Scoring
| Variant | quant | qual | combined (0.5 / 0.5) |
|---|---|---|---|
| V1 | 0.786 | 0.733 | **0.760** |
| V2 | 0.621 | 0.533 | 0.577 |
| V3 | 0.735 | 0.600 | 0.668 |
Margin V1 over V3: 0.092 (9.2 points, above the 5% tie band). Tiebreaker not applied.

## Selected Base: Variant 1 (analyzer card, claude-sonnet-5-5 pin; served model per self-report claude-haiku-5-5)
- Selection rationale: widest verified coverage, every cited line verified in the real files by two advocates, the only card that probes tables 4.1/4.2.
- Strengths to preserve: finding F2/F13 (resume inputs), F3 (not_applied restore), F5 (reconcile promise), F7 (CI-fix trigger), minor spec gaps F4, F6, F8, F9, F10, F14.
- Strengths to incorporate: V2 F1 (Task 11 names-only), F2 (autoMergeRequest type), F3 (file:NNN constraint, with corrected locators); V3 F2 (`_RESOLUTION_SCRIPTS` conditional) and V3's MINOR rating of the cycle-id gap; probe items INV-001, INV-002, INV-007 from Round 2.5.
- Weaknesses of the base to fix: six blocking flags withdrawn; F11 and F12 dropped; F1 re-rated MINOR.
