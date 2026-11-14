# Base Selection: Q15

Scored by the orchestrating worker. Position-bias mitigation was a reverse-order re-check by the same evaluator, not an independent pass. The debate did not converge at point level (73 percent against 80), so per the skill the base is force-selected by score and non-convergence is recorded.

## Quantitative Scoring (50% weight)

Source requirements for RC: answer "ever"; first-release behaviour; the trust-layer link (Q14, ADJ line 699); the #423 relay goal; the worker route (WC-12).

| Metric | Weight | V1 | V2 | V3 | Note |
|---|---|---|---|---|---|
| Requirement coverage | 0.30 | 1.00 | 0.80 | 1.00 | V2 answers "not now" rather than "ever" |
| Internal consistency | 0.25 | 1.00 | 1.00 | 0.90 | V3 states a goal that contradicts the contract's "never messaged" without a planned contract change in its answer |
| Specificity ratio | 0.15 | 0.85 | 0.90 | 0.85 | |
| Dependency completeness | 0.15 | 1.00 | 1.00 | 0.90 | V3's delivery channel is unnamed |
| Section coverage | 0.15 | 1.00 | 1.00 | 1.00 | |
| quant_score | | 0.978 | 0.925 | 0.928 | |

## Qualitative Scoring (50% weight)

| Dimension | V1 | V2 | V3 | Criteria not met (evidence) |
|---|---|---|---|---|
| Completeness (5) | 4 | 4 | 4 | All: no explicit out-of-scope |
| Correctness (5) | 4 | 5 | 4 | V1 criterion 2: binds "any later automated program", beyond the question's scope (its advocate's concession); V3 criterion 2: no channel is known, so delivery feasibility is unshown |
| Structure (5) | 5 | 5 | 5 | |
| Clarity (5) | 5 | 4 | 4 | V2 criterion 5: no reopening trigger; V3 criterion 5: person approval undecided |
| Risk coverage (5) | 3 | 3 | 4 | V3 names poisoned content, the path length and the unknown channel with a gate |
| Invariant and edge case (5) | 2 | 2 | 3 | V3 names the unattended-session edge case and the trust-layer guard |
| Total (30) | 23 | 23 | 24 | |
| qual_score | 0.767 | 0.767 | 0.800 | |

## Combined Scoring

| Variant | Score |
|---|---|
| V1 | 0.872 |
| V2 | 0.846 |
| V3 | 0.864 |

All three within 5 percent: tiebreaker level 1, scored points won: V2 won C-003, X-002 and shares C-005, X-003 (4); V1 won none outright and shares C-005, X-003 (2); V3 won none. Variant 2 selected. This matches all three advocates' unassigned picks.

## Selected Base: Variant 2 (proposal-B)

- Rationale: the adjudicated answer and the default; same first-release safety as Variant 1 without binding unresearched designs; keeps the trust layer off v2's path.
- Incorporate: from Variant 1, a named reopening condition (a delivery channel named, a threat model for poisoned content, whether a person approves each correction) and the optional sentence beside the contract's "never messaged" (by a separate approved PR); from Variant 3, unattended watcher-launched sessions recorded as the open case, and the v2 design's typed fields and audit record shaped so a later delivery release needs no store migration; from the A-001 consensus, v2 hands worker corrections to the coordinator, which decides whether to send a WC-12 follow-up.
