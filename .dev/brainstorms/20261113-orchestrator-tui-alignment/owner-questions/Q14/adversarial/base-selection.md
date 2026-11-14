# Base Selection: Q14

Scored by the orchestrating worker. Position-bias mitigation was a reverse-order re-check by the same evaluator, not an independent pass.

## Quantitative Scoring (50% weight)

Source requirements for RC: what "#339 is complete" means; capture recorded versus class restored (X-009); the other #339 phases; effect on V2-01, V2-02, SW-14.

| Metric | Weight | V1 | V2 | V3 | Note |
|---|---|---|---|---|---|
| Requirement coverage | 0.30 | 1.00 | 1.00 | 1.00 | |
| Internal consistency | 0.25 | 0.90 | 1.00 | 1.00 | V1's "most catalogue fields come from the sweep" is unsupported (its advocate's concession) |
| Specificity ratio | 0.15 | 0.85 | 0.90 | 0.90 | |
| Dependency completeness | 0.15 | 0.90 | 1.00 | 1.00 | V1's per-feature list does not exist yet |
| Section coverage | 0.15 | 1.00 | 1.00 | 1.00 | |
| quant_score | | 0.938 | 0.985 | 0.985 | |

## Qualitative Scoring (50% weight)

| Dimension | V1 | V2 | V3 | Criteria not met (evidence) |
|---|---|---|---|---|
| Completeness (5) | 4 | 4 | 4 | All: no explicit out-of-scope |
| Correctness (5) | 4 | 4 | 5 | V1 criterion 5 (an unsupported field claim); V2 criterion 2 (a code PR on a planning gate, which W5 calls a conflation, merged-requirements.md:415) |
| Structure (5) | 5 | 5 | 5 | |
| Clarity (5) | 4 | 5 | 5 | V1 criterion 5: the per-feature list is deferred to the activity it gates |
| Risk coverage (5) | 3 | 4 | 3 | V2 names the unbuildable-Rule-5 failure mode and its consequence |
| Invariant and edge case (5) | 2 | 3 | 2 | V2 names the record-versus-test guard, the transition from capture to class and the redesign case |
| Total (30) | 22 | 25 | 24 | |
| qual_score | 0.733 | 0.833 | 0.800 | |

## Combined Scoring

| Variant | Score |
|---|---|
| V1 | 0.836 |
| V2 | 0.909 |
| V3 | 0.893 |

V2 and V3 within 5%: tiebreaker level 1, scored points won: V3 won C-001, X-002, X-003 and shares C-003 (4); V2 won C-005 (1); V1 won C-004 (1). Variant 3 selected; also 3 of 3 unassigned picks.

## Selected Base: Variant 3 (proposal-C)

- Rationale: matches the spec default, V2-02 and SW-14 as written; a gate a ledger entry can check; no code on a planning gate.
- Incorporate: from Variant 2 (U-002), the gate entry states whether the recorded values are enough to build Rule 5's four conditions; from Variant 1 (U-001), an optional fallback if the capture still cannot run by a date the owner sets: the gate drops to #539 merged with live-value fields marked pending.
