# Base Selection: Q11

Scored by the orchestrating worker (the skill assigns Step 3 to the orchestrator). Position-bias mitigation was a reverse-order re-check by the same evaluator, not an independent second pass.

## Quantitative Scoring (50% weight)

Source requirements used for RC: the four things an answer to Q11 must address (which report; cadence "3 to 5 minutes"; the contract-note dependency; fidelity to "#409"). Counted by inspection.

| Metric | Weight | V1 | V2 | V3 | Note |
|---|---|---|---|---|---|
| Requirement coverage | 0.30 | 1.00 | 1.00 | 1.00 | All four addressed in each |
| Internal consistency | 0.25 | 1.00 | 1.00 | 1.00 | No self-contradiction found |
| Specificity ratio | 0.15 | 0.85 | 0.85 | 0.80 | V3 has more general wording ("matches what exists") |
| Dependency completeness | 0.15 | 1.00 | 1.00 | 1.00 | No unresolved internal references |
| Section coverage | 0.15 | 1.00 | 1.00 | 1.00 | Five H2 sections each |
| quant_score | | 0.978 | 0.978 | 0.970 | |

## Qualitative Scoring (50% weight), additive binary rubric

Met counts per dimension, with the deciding evidence for any criterion not met.

| Dimension | V1 | V2 | V3 | Criteria not met (evidence) |
|---|---|---|---|---|
| Completeness (5) | 4 | 4 | 4 | All: criterion 5 (explicit out-of-scope) not stated; each lists "unresolved" items only |
| Correctness (5) | 4 | 5 | 5 | V1 criterion 2: "can fill the 3-minute end" presumes a loop that is unbuilt (question.md fact 10) |
| Structure (5) | 5 | 5 | 5 | none |
| Clarity (5) | 4 | 5 | 5 | V1 criterion 5: next steps defer the needed WC-16 and style edits to an unspecified later loop |
| Risk coverage (5) | 4 | 3 | 3 | V2, V3 criterion 3 (failure and recovery) and criterion 5 (monitoring) not met; V1 names Q-1 and load with a check route but no recovery (criterion 3) |
| Invariant and edge case (5) | 3 | 2 | 2 | V1 names the Q-1 binding guard, the 5-minute cap boundary and the word-list interaction; V2 names the cap boundary and the note precondition; V3 names the cap and the per-invocation guard |
| Total (30) | 24 | 24 | 24 | |
| qual_score | 0.800 | 0.800 | 0.800 | |

Edge case floor (at least 1 of 5): all three eligible.

## Position-Bias Mitigation

Reverse-order re-check (V3, V2, V1) by the same evaluator changed no verdict. Disagreements found: 0. Verdicts changed: 0. This is not an independent pass.

## Combined Scoring

| Variant | quant x 0.5 | qual x 0.5 | Score |
|---|---|---|---|
| V1 | 0.489 | 0.400 | 0.889 |
| V2 | 0.489 | 0.400 | 0.889 |
| V3 | 0.485 | 0.400 | 0.885 |

Top three within 5%: tiebreaker applied. Level 1, debate points won (scoring matrix): V2 won 4 (C-002, C-003, X-001, X-003), V1 won 1 counted point (C-005) plus 2 contributions, V3 won 1 counted point (C-004) plus 1 contribution. V2 wins at level 1. Also consistent with all three advocates' unassigned picks.

## Selected Base: Variant 2 (proposal-B, sweep summary only until the contract note)

- Selection rationale: zero edits, matches spec section 6.7, the shipped sweep skill and V5 D2; won the most scored points; every advocate picked it when unassigned.
- Strengths to preserve: one source of facts in chat; reopen trigger inside the contract note; no naming of `observe` in coordinator rules before the note.
- Strengths to incorporate: from V3, an explicit statement that no recurring loop exists so no cadence is claimed as met (U-003, C-004); from V1, the Q-1 check (`observe --once --run <run>` from the coordinator's own terminal) as a precondition before observer text ever joins (U-002); from the orchestrator spot-check, the fact that the #409-layout report already exists as the sweep's report file (orchestrator-mode.md:603), which answers most of C-005.
