# Base Selection Report: Q20

Performed by: the orchestrating session (group 4 worker), inline, as the debate-orchestrator role. Variant 1 = proposal-A (hold), Variant 2 = proposal-B (named person owns), Variant 3 = proposal-C (coordinator owns).

## Quantitative Scoring (50% weight)

Source "requirements" = 6 items: WA-03, WA-02 edit 4, WA-04 (FU-1), the day cap, session cleanup, visibility of Run-less sessions (ADJ line 242).

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 0.83 (5 of 6; no visibility) | 1.00 (6 of 6) | 1.00 (6 of 6) |
| internal_consistency | 0.25 | 1.00 | 1.00 | 0.92 (claims ownership of sessions it does not start; its own source recommends "never coordinator-owned") |
| specificity_ratio | 0.15 | 0.80 | 0.90 | 0.85 |
| dependency_completeness | 0.15 | 1.00 | 1.00 | 1.00 |
| section_coverage | 0.15 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | **0.919** | **0.985** | **0.958** |

## Qualitative Scoring (50% weight): Additive Binary Rubric (CEV, condensed)

| Dimension / criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|
| Completeness 1: covers WA-03, edit 4, WA-04 | MET | MET | MET | |
| Completeness 2: edge cases and failures | MET | MET | MET | V1 stall; V2 unattended sessions; V3 session lapse |
| Completeness 3: dependencies | MET | MET | MET | Q2, Q21, WA-05 |
| Completeness 4: completion criteria | MET | MET | MET | Ledger record |
| Completeness 5: out of scope stated | NOT MET | MET | MET | V2 "never coordinator-owned"; V3 closing stays a person's action |
| Correctness 1: no factual errors | MET | MET | MET | |
| Correctness 2: feasible under stated constraints | NOT MET | MET | NOT MET | V1's hold is circular (cleanup needs FU-1's facts); V3 conflicts with WC-16's Run-scoped loop (WORKER-CONTRACT.md line 288) |
| Correctness 3: consistent terminology | MET | MET | MET | |
| Correctness 4: no internal contradiction | MET | MET | NOT MET | V3: "owns" sessions it does not start |
| Correctness 5: claims supported | MET | MET | MET | |
| Structure 1 to 5 | 5 MET | 5 MET | 5 MET | Identical layout |
| Clarity 1 to 5 | 5 MET | 5 MET | 5 MET | WA ids glossed in each |
| Risk 1: probability and impact | NOT MET | NOT MET | NOT MET | |
| Risk 2: mitigation per risk | NOT MET | NOT MET | NOT MET | No variant mitigates accumulation |
| Risk 3: failure and recovery | NOT MET | MET | NOT MET | V2: person closes by hand |
| Risk 4: external dependencies | MET | MET | MET | Live Orca, Q2 |
| Risk 5: monitoring | NOT MET | NOT MET | MET | V3: recurring check |
| Invariant 1: collection boundaries (session count) | MET | MET | MET | All name the 6-a-day pile-up |
| Invariant 2: state across components | NOT MET | MET | MET | V2 and V3: Run-less sessions seen only as transcript rows |
| Invariant 3: guard gaps | MET | MET | NOT MET | V1 and V2: forfeit-guarantee precondition via WA-03 or its hold |
| Invariant 4: count divergence | NOT MET | NOT MET | NOT MET | Not applicable |
| Invariant 5: interaction effects | NOT MET | MET | MET | V2 permission mode (Q2); V3 WA-07 |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4/5 | 5/5 | 5/5 |
| Correctness | 4/5 | 5/5 | 3/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 5/5 | 5/5 | 5/5 |
| Risk Coverage | 1/5 | 2/5 | 2/5 |
| Invariant and Edge Case | 2/5 | 4/5 | 3/5 |
| **qual_score** | **21/30 = 0.700** | **26/30 = 0.867** | **23/30 = 0.767** |

### Edge Case Floor Check
All at least 1/5; all eligible.

## Position-Bias Mitigation
Single evaluator, two passes. The passes disagreed on Correctness 2 for V1 (is a circular hold infeasible or only slow?). Re-evaluated NOT MET: the hold's own exit condition (a cleanup rule) depends on the test it blocks, which its advocate conceded. Disagreements re-evaluated: 1. Final verdicts changed: 0 relative to pass 1.

## Combined Scoring

| Variant | Quant x 0.50 | Qual x 0.50 | Final Score |
|---|---|---|---|
| V1 (proposal-A) | 0.460 | 0.350 | 0.810 |
| V2 (proposal-B) | 0.493 | 0.433 | 0.926 |
| V3 (proposal-C) | 0.479 | 0.383 | 0.862 |

Margin V2 over V3: 6.4 points (above the 5 point threshold). Tiebreaker applied: no.

## Selected Base: Variant 2 (proposal-B, named person owns)

### Selection Rationale
Highest score, unanimous overall verdict (60, 70, 70 percent), and the winner of 8 of 11 points. It matches the watcher's design (a plain process, never an Orca worker), the cap's stated purpose (bounding sessions the owner must review) and the spec's recommendation.

### Strengths to Preserve from Base
1. A named person creates the worktree and owns the agent; sessions stay person-reviewed top-level sessions, never coordinator-owned.
2. WA-03, edit 4 and FU-1 proceed.
3. The `.dev/issues/<N>/` runbook note.

### Strengths to Incorporate from Non-Base Variants
1. From V1 (U-001, C-004), as all three advocates proposed: a written rule on who closes watcher sessions and by when becomes a precondition of enabling the schedule (WA-05), not of FU-1.
2. From the A-001 finding: "up to the confirmed day cap (default 6)"; the cap is a code constant the owner may lower after the shadow run.
3. From advocates 2 and 3: a review cadence for the named person and a fallback (a named substitute, or the schedule disabled while the owner is away).
4. From advocate 1: owning the creation agent is not owning the later watcher sessions; the person is their named reviewer, and closing a session is done by hand in Orca (the runbook gives no command).
5. From V3 (U-003) in the narrow form advocate 2 accepted: the coordinator's check may include a read-only count of open sessions in `issue-watch`, without reading transcripts and without owning them.
6. From A-002: if Q2 keeps the default claim level, the owner also names who owns the `issue-<N>` agents.
