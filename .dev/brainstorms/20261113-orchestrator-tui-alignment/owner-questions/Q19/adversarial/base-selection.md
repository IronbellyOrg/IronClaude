# Base Selection Report: Q19

Performed by: the orchestrating session (group 4 worker), inline, as the debate-orchestrator role. Variant 1 = proposal-A (summary and named steps first, in the sweep), Variant 2 = proposal-B (no first ask yet), Variant 3 = proposal-C (Fleet Quilt or Decision Desk first, in the observer).

## Quantitative Scoring (50% weight)

Source "requirements" = 6 items: OB-09; the release 3 gates (QUESTION-LINK, OB-06, OB-02); the contract note (XC-05, XC-07); the shared capture (XC-03); review 05's D7 ordering; the data-source findings (review 01 F-08 to F-11).

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 0.67 (4 of 6; no note, no capture) | 0.83 (5 of 6; no D7) | 1.00 (6 of 6) |
| internal_consistency | 0.25 | 1.00 | 1.00 | 1.00 |
| specificity_ratio | 0.15 | 0.90 | 0.85 | 0.85 |
| dependency_completeness | 0.15 | 1.00 | 1.00 | 1.00 |
| section_coverage | 0.15 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | **0.885** | **0.928** | **0.978** |

## Qualitative Scoring (50% weight): Additive Binary Rubric (CEV, condensed)

| Dimension / criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|
| Completeness 1: covers OB-09 and the question's two parts (which ask, which program) | MET | NOT MET | MET | V2 answers neither part |
| Completeness 2: edge cases and failures | MET | MET | MET | V1 depends on #539; V2 drift; V3 blocked gates |
| Completeness 3: dependencies | MET | MET | MET | |
| Completeness 4: completion criteria | MET | MET | MET | Ledger record in each |
| Completeness 5: out of scope stated | MET | NOT MET | NOT MET | V1 excludes links explicitly |
| Correctness 1: no factual errors | MET | MET | MET | Off-by-one line citations in V2 and V3 (review 05 line 65 and 252 for 66 and 254); facts correct |
| Correctness 2: feasible under stated constraints | NOT MET | MET | MET | V1's handoff read needs an allow-list change not shown to be permitted (UNVERIFIED) |
| Correctness 3: consistent terminology | MET | MET | MET | |
| Correctness 4: no internal contradiction | MET | MET | MET | |
| Correctness 5: claims supported | MET | MET | MET | |
| Structure 1 to 5 | 5 MET | 5 MET | 5 MET | Identical layout |
| Clarity 1: unambiguous | MET | MET | NOT MET | V3 leaves "Fleet Quilt or Decision Desk" open |
| Clarity 2, 3 | 2 MET | 2 MET | 2 MET | |
| Clarity 4: terms glossed | MET | MET | MET | QUESTION-LINK, AC-S, XC-03, XC-07 glossed |
| Clarity 5: next step clear | MET | NOT MET | MET | V2's next step is "ask again later" |
| Risk 1: probability and impact | NOT MET | NOT MET | NOT MET | |
| Risk 2: mitigation per risk | NOT MET | NOT MET | NOT MET | |
| Risk 3: failure and recovery | NOT MET | NOT MET | NOT MET | |
| Risk 4: external dependencies | MET | MET | MET | PR #539, QUESTION-LINK |
| Risk 5: monitoring | NOT MET | NOT MET | NOT MET | |
| Invariant 1: collection boundaries | NOT MET | NOT MET | NOT MET | |
| Invariant 2: state across components | MET | NOT MET | MET | V1 worker-reported state into the sweep; V3 field meanings from the note and capture |
| Invariant 3: guard gaps | MET | MET | MET | V1 state words only from `worker_status`; V2 and V3 gate on QUESTION-LINK |
| Invariant 4: count divergence | NOT MET | NOT MET | NOT MET | Not applicable |
| Invariant 5: interaction effects | MET | NOT MET | MET | V1 interacts with Q17; V3 with the release 3 gates |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 5/5 | 3/5 | 4/5 |
| Correctness | 4/5 | 5/5 | 5/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 5/5 | 4/5 | 4/5 |
| Risk Coverage | 1/5 | 1/5 | 1/5 |
| Invariant and Edge Case | 3/5 | 1/5 | 3/5 |
| **qual_score** | **23/30 = 0.767** | **19/30 = 0.633** | **22/30 = 0.733** |

### Edge Case Floor Check
All at least 1/5; all eligible.

## Position-Bias Mitigation
Single evaluator, two passes (1, 2, 3 then 3, 2, 1). The passes disagreed on Correctness 2 for V1 (is an unverified allow-list change a feasibility failure?). Re-evaluated NOT MET: no source shows the sweep may read handoff files, and review 01 line 86 says it reads none today. Disagreements re-evaluated: 1. Final verdicts changed: 0 relative to pass 1.

## Combined Scoring

| Variant | Quant x 0.50 | Qual x 0.50 | Final Score |
|---|---|---|---|
| V1 (proposal-A) | 0.443 | 0.383 | 0.826 |
| V2 (proposal-B) | 0.464 | 0.317 | 0.781 |
| V3 (proposal-C) | 0.489 | 0.367 | 0.856 |

Margin V3 over V1: 3.0 points (below the 5 point threshold). Tiebreaker applied: yes, level 1 (debate points won on S, C, X and A points): V1 won 5 (C-003, C-004, X-002, X-003, A-001), V3 won 4 (C-001, C-002, C-005, X-001), V2 won 0; A-002 split. Following the skill's rule ("Variant with more diff points won"), **V1 is the selected base**.

Recorded tension: the overall advocate verdicts went the other way (V3 by 2 of 3: advocates 2 and 3; advocate 1 kept V1). The base therefore carries V1's data finding, and the refactor plan restructures its answer to take V3's direction, which won the "which ask" and "which program" points. final.md reports this as a split debate.

## Selected Base: Variant 1 (proposal-A, summary and named steps first, in the sweep)

### Selection Rationale
Selected by tiebreaker level 1 (debate points won, 5 against 4) after a 3.0 point combined margin. It owns the debate's strongest new fact (a deterministic, ungated data source) and the unanimous points on gates, data source and the sweep's read-only rule.

### Strengths to Preserve from Base
1. The deterministic data source for summary and named steps (review 01 F-08, F-10; WC-15).
2. Links excluded until a GitHub read is decided.

### Strengths to Incorporate from Non-Base Variants
1. From V3 (C-001, C-002, C-005, X-001, won 2 of 3 or 3 of 3): the first screen ask in the observer (Fleet Quilt or Decision Desk) as the direction, recorded now; review 01 item 9 (line 167) also says choose the direction first, then add only the fields it needs.
2. From V3 (U-003): one release-gates row per ask with its data gate.
3. From V1 advocate's concession: absent `worker_status` shows as unknown.
4. From all advocates (A-001): re-read the 2026-11-11 comment before recording the ordering.
5. From V3 advocate: suggested pick Fleet Quilt, because it carries no release 3 gate.
