# Base Selection: Q1

Scoring was done inline by the orchestrating worker (no separate debate-orchestrator agent); both rubric passes were run by the same evaluator, so the position-bias passes are not independent. Requirements for the coverage metric are taken from `../question.md`: R1 the ruling names an option; R2 states its premise (SW-01 (2)); R3 authorises the allow-list edit if a fix is chosen (SW-01 (3)); R4 states channel scope (SW-01 (4), Q1 part (b)); R5 handles the 16-plus "read-only" claims (INV-011); R6 states the effect on XC-04; R7 states reversibility.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 | Note |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.857 (6/7; misses R3 for the follow-up) | 0.857 (6/7; misses R2) | 1.000 (7/7; R3 not applicable to an acceptance, counted met) | |
| Internal consistency (IC) | 0.25 | 1.000 | 1.000 | 0.933 (1 of about 15 claims contradicted: X-003) | |
| Specificity ratio (SR) | 0.15 | 0.85 | 0.88 | 0.88 | manual count, estimated |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | every id resolves in `../question.md` |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | five sections each |
| **quant_score** | | **0.934** | **0.939** | **0.965** | |

## Qualitative Scoring (50% weight): Additive Binary Rubric

| Dimension | V1 | V2 | V3 | Deciding evidence (CEV, condensed) |
|---|---|---|---|---|
| Completeness | 4 | 4 | 5 | Criterion 1 (covers all requirements): V1 NOT MET (no allow-list authorisation for the follow-up, V1 advocate concession 5); V2 NOT MET (no premise, V2 advocate concession 1); V3 MET. Criteria 2 to 5 MET for all (each lists failure cases, dependencies, an end condition and an "unresolved" section). |
| Correctness | 4 | 5 | 3 | Criterion 1 (no factual error): V1 NOT MET ("the spec forbids running the unfixed sweep" stated flatly, see CONTRADICTION-1); V3 NOT MET ("an owner exception the spec does not provide", same); V2 MET (its XC-04 claim holds under both readings). Criterion 4 (no internal contradiction): V3 NOT MET (X-003). |
| Structure | 4 | 4 | 4 | Criterion 4 (navigation aids): NOT MET for all; short files without cross-reference index. |
| Clarity | 5 | 5 | 5 | All give concrete next steps and gloss F-options and work items in words. |
| Risk coverage | 3 | 4 | 3 | Criterion 1 (three risks with probability and impact): NOT MET for all. Criterion 5 (detection mechanism): V2 MET (regression test reproducing the probe); V1 NOT MET ("a promise in a table, not a mechanical gate"); V3 NOT MET (void conditions are not detected). |
| Invariant and edge-case coverage | 3 | 4 | 4 | Criterion 1 (collection boundaries): NOT MET for all. Criterion 2 (state across components): V2 MET (git-status scope versus shared path list, INV-039); V3 MET (notes the shared path list is untouched); V1 NOT MET. Criteria 3 to 5 MET for all (guard gaps named; "16 not four", "18 of 29"; XC-04 interaction). |
| **Total** | **23/30 = 0.767** | **26/30 = 0.867** | **24/30 = 0.800** | |

Edge-case floor (at least 1 of 5): all eligible.

## Position-Bias Mitigation

| Pass | Order | Result |
|---|---|---|
| 1 | V1, V2, V3 | totals 23, 26, 24 |
| 2 | V3, V2, V1 | totals 24, 26, 23 |

Disagreements found: 0. Verdicts changed: 0. Caveat: same evaluator for both passes.

## Combined Scoring

| Variant | 0.5 x quant | 0.5 x qual | Combined |
|---|---|---|---|
| Variant 1 | 0.467 | 0.383 | 0.851 |
| Variant 2 | 0.470 | 0.433 | **0.903** |
| Variant 3 | 0.483 | 0.400 | 0.883 |

Margin Variant 2 over Variant 3: 2.0 points (under 5 points), so the tiebreaker applies. Level 1 (debate points won): Variant 2 won 7, Variant 3 won 2. Winner: Variant 2.

## Selected Base: Variant 2 (proposal-B, "fix before merge, neutralise or refuse, all channels")

- Selection rationale: highest combined score after the tiebreaker, 7 of 12 decided debate points, and all three advocates named it as their neutral recommendation (60, 65, 62 percent).
- Strengths to preserve: claims made true in one pass; reversibility; test-enforced channel coverage with "names any channel it leaves out"; scoped allow-list authority; INV-039 separation.
- Strengths to incorporate:
  1. From Variant 3 (C-004): the ruling states its premise, as SW-01 (2) requires for every ruling.
  2. From the debate on A-001: state the requirement by outcome, with the measured list as a minimum, not as the complete set.
  3. From the debate on A-003 and X-003 (Variant 1): say plainly that a fix removes the sweep's fan-out and makes its claim true, but does not by itself remove every `git status` exposure on the host.
  4. From Variant 1 (U-002): keep the fix reviewable on its own (a separate push to #539 with its own description), because #539 is a 1003-file PR.
  5. Record CONTRADICTION-1 so the owner sees the XC-04 advantage depends on the strict reading.
