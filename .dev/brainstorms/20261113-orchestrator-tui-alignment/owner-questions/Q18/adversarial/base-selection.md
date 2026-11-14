# Base Selection Report: Q18

Performed by: the orchestrating session (group 4 worker), inline, as the debate-orchestrator role. Variant 1 = proposal-A (not yet), Variant 2 = proposal-B (yes, design now), Variant 3 = proposal-C (no, drop CO-04).

## Quantitative Scoring (50% weight)

Source "requirements" = 6 items: CO-04, CO-01, Q22, the Q4 link (MR lines 375, 1177), the single-host contract line (MR line 453), and the owner's 2026-11-08 record (ADJ line 306).

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 1.00 (6 of 6) | 1.00 (6 of 6) | 0.83 (5 of 6; no Q4) |
| internal_consistency | 0.25 | 1.00 | 1.00 | 1.00 |
| specificity_ratio | 0.15 | 0.85 | 0.90 | 0.85 |
| dependency_completeness | 0.15 | 1.00 | 1.00 | 1.00 |
| section_coverage | 0.15 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | **0.978** | **0.985** | **0.928** |

## Qualitative Scoring (50% weight): Additive Binary Rubric (CEV, condensed)

| Dimension / criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|
| Completeness 1: covers CO-04 and CO-01 | MET | MET | MET | |
| Completeness 2: edge cases and failures | MET | MET | MET | V1 owner forgets; V2 undesigned receiver; V3 design from nothing |
| Completeness 3: dependencies | MET | MET | MET | Q4, Q22, Q3 named |
| Completeness 4: completion criteria | MET | MET | MET | Ledger record in each |
| Completeness 5: out of scope stated | MET | NOT MET | MET | V1 single-host per MR line 145; V3 "nothing within this program" |
| Correctness 1: no factual errors | NOT MET | MET | MET | V1 claims a later channel "needs no change to the observer's file"; ADJ line 306 says identity and age pieces are missing (its advocate conceded) |
| Correctness 2: feasible under stated constraints | MET | NOT MET | MET | V2 runs against MR line 375 sequencing |
| Correctness 3: consistent terminology | MET | MET | MET | |
| Correctness 4: no internal contradiction | MET | MET | MET | |
| Correctness 5: claims supported | MET | MET | NOT MET | V3's "no TUIBBS planned" has no source; the record says "may" |
| Structure 1 to 5 | 5 MET | 5 MET | 5 MET | Identical layout |
| Clarity 1 to 5 | 5 MET | 5 MET | 5 MET | CO-04, Q22 glossed in each |
| Risk 1: probability and impact | NOT MET | NOT MET | NOT MET | |
| Risk 2: mitigation per risk | NOT MET | MET | NOT MET | V2: read-only, identity-tagged, re-sanitised copy |
| Risk 3: failure and recovery | MET | NOT MET | MET | V1 second #477 edit; V3 new item |
| Risk 4: external dependencies | MET | MET | MET | |
| Risk 5: monitoring | NOT MET | NOT MET | NOT MET | |
| Invariant 1: collection boundaries | NOT MET | NOT MET | NOT MET | |
| Invariant 2: state across components | NOT MET | MET | NOT MET | V2 identity envelope across hosts |
| Invariant 3: guard gaps | MET | MET | NOT MET | V1 and V2: four pieces before any code |
| Invariant 4: count divergence | NOT MET | NOT MET | NOT MET | Not applicable |
| Invariant 5: interaction effects | NOT MET | MET | MET | V2 pulls Q22 and authentication; V3 Q3 link |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 5/5 | 4/5 | 5/5 |
| Correctness | 4/5 | 4/5 | 4/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 5/5 | 5/5 | 5/5 |
| Risk Coverage | 2/5 | 2/5 | 2/5 |
| Invariant and Edge Case | 1/5 | 3/5 | 1/5 |
| **qual_score** | **22/30 = 0.733** | **23/30 = 0.767** | **22/30 = 0.733** |

### Edge Case Floor Check
All at least 1/5; all eligible.

## Position-Bias Mitigation
Single evaluator, two passes. The passes disagreed on Correctness 1 for V1 (is an UNVERIFIED overclaim a factual error?). Re-evaluated NOT MET: the claim contradicts the missing identity and age pieces listed at ADJ line 306. Disagreements re-evaluated: 1. Final verdicts changed: 0 relative to pass 1.

## Combined Scoring

| Variant | Quant x 0.50 | Qual x 0.50 | Final Score |
|---|---|---|---|
| V1 (proposal-A) | 0.489 | 0.367 | 0.856 |
| V2 (proposal-B) | 0.493 | 0.383 | 0.876 |
| V3 (proposal-C) | 0.464 | 0.367 | 0.831 |

Margin V2 over V1: 2.0 points (below the 5 point threshold). Tiebreaker applied: yes, level 1 (debate points won): V1 won 8 (C-001, C-002, C-003, X-001, X-002, X-003, U-001, A-001), V2 won 2 (C-005, U-002), V3 won 2 (U-003, A-002); C-004 split; S-001 tie.

## Selected Base: Variant 1 (proposal-A, not yet)

### Selection Rationale
Within 5 points of V2 on the rubric (V2's edge comes from naming design pieces that only matter if the owner says yes), and decisively ahead in the debate (8 of 12 decided points). All three advocates, including V2's and V3's, judged V1 best overall (70, 72, 65 percent).

### Strengths to Preserve from Base
1. CO-04 stays deferred with both triggers (R4, or an owner statement).
2. No transport or authentication design before Q4, Q18 and authentication are settled (MR line 375).
3. Single-host contract line unchanged.

### Strengths to Incorporate from Non-Base Variants
1. From V2 (C-005, U-002): data exposure as a named concern in the CO-04 design: the snapshot is mode 0600 on purpose (ADJ line 244); decide who may read a copy and whether the whole snapshot or a reduced part leaves the host (advocate 3).
2. From advocates 1 and 3: CO-01 wording "no channel exists; one is deferred until observer R4 or an owner decision on a TUIBBS screen".
3. From advocate 1 concession: drop the overclaim "needs no change to the observer's file".
4. From V3 advocate's fix and V2 (C-004, split): a conditional contract-note sentence: any future off-host copy is read-only and must meet CO-04's preconditions first. Recorded as the orchestrator's resolution of the split point.
5. From advocate 2 (A-002): the ledger is the authoritative record; the CO-01 sentence is its public echo.
