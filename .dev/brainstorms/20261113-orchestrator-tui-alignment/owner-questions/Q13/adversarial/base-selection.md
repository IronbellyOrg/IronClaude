# Base Selection: Q13

Scored by the orchestrating worker. Position-bias mitigation was a reverse-order re-check by the same evaluator, not an independent pass.

## Quantitative Scoring (50% weight)

Source requirements for RC: a verdict on the bare-name fallback; the `ORCA_CLI_COMMAND` difference; effect on hosts; what the note (XC-05) says; build divergence (A-009).

| Metric | Weight | V1 | V2 | V3 | Note |
|---|---|---|---|---|---|
| Requirement coverage | 0.30 | 1.00 | 1.00 | 0.80 | V3 gives no verdict on the fallback |
| Internal consistency | 0.25 | 1.00 | 1.00 | 1.00 | |
| Specificity ratio | 0.15 | 0.90 | 0.90 | 0.80 | |
| Dependency completeness | 0.15 | 1.00 | 1.00 | 1.00 | |
| Section coverage | 0.15 | 1.00 | 1.00 | 1.00 | |
| quant_score | | 0.985 | 0.985 | 0.910 | |

## Qualitative Scoring (50% weight)

| Dimension | V1 | V2 | V3 | Criteria not met (evidence) |
|---|---|---|---|---|
| Completeness (5) | 4 | 4 | 3 | All: no explicit out-of-scope; V3 also leaves the core question unanswered |
| Correctness (5) | 4 | 4 | 5 | V1 criterion 5: "both are accepted" is claimed safe on a probe that does not prove sameness (X-001, conceded); V2 criterion 2: motive (same binary) is mostly already met on a healthy host because `orca-ide` is tried first (its advocate's concession) |
| Structure (5) | 5 | 5 | 5 | |
| Clarity (5) | 5 | 5 | 4 | V3 criterion 5: next step for a future caller undefined |
| Risk coverage (5) | 3 | 3 | 3 | All: no recovery path |
| Invariant and edge case (5) | 3 | 3 | 2 | V1 and V2 name the screen-reader guard, `ORCA_CLI_COMMAND` divergence and host-shape cases; V3 names two |
| Total (30) | 24 | 24 | 22 | |
| qual_score | 0.800 | 0.800 | 0.733 | |

## Combined Scoring

| Variant | Score |
|---|---|
| V1 | 0.893 |
| V2 | 0.893 |
| V3 | 0.822 |

V1 and V2 tie: tiebreaker level 1, scored points won outright or shared: V1 won C-001, C-005 and shares C-002, C-004, X-002 (5); V2 won C-003, X-001, X-003 (3). Variant 1 selected; matches 2 of 3 unassigned picks.

## Selected Base: Variant 1 (proposal-A)

- Rationale: verdict with reasons, no code change, keeps `orca`-only hosts working, spec's recommendation.
- Incorporate: from V2, the precise limit of the probe ("is Orca", not "the same Orca"), the `ORCA_CLI_COMMAND` split stated as part of the accepted difference, and the silent fallback on a failed `orca-ide` probe; from V3, the build-string record as the re-ask trigger, plus "or `ORCA_CLI_COMMAND` is in use"; from V1's advocate, the observer's missing absolute-path check logged as a follow-up (not fixed by this answer).
