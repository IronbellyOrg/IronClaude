# Base Selection: Q12

Scored by the orchestrating worker (Step 3 is the orchestrator's per the skill). Position-bias mitigation was a reverse-order re-check by the same evaluator, not an independent pass.

## Quantitative Scoring (50% weight)

Source requirements for RC: answer yes or no on discoverability; where the entry lives; test impact (INV-029); "person only" (INV-013); timing against PR #539.

| Metric | Weight | V1 | V2 | V3 | Note |
|---|---|---|---|---|---|
| Requirement coverage | 0.30 | 1.00 | 1.00 | 1.00 | All five addressed |
| Internal consistency | 0.25 | 1.00 | 1.00 | 0.90 | V3 says a test "must change", which its own advocate found likely false for the routing table |
| Specificity ratio | 0.15 | 0.80 | 0.85 | 0.90 | V3 cites test lines and work-item steps |
| Dependency completeness | 0.15 | 1.00 | 1.00 | 1.00 | |
| Section coverage | 0.15 | 1.00 | 1.00 | 1.00 | |
| quant_score | | 0.970 | 0.978 | 0.960 | |

## Qualitative Scoring (50% weight)

| Dimension | V1 | V2 | V3 | Criteria not met (evidence) |
|---|---|---|---|---|
| Completeness (5) | 4 | 4 | 4 | All: no explicit out-of-scope statement |
| Correctness (5) | 5 | 4 | 4 | V2 criterion 2: its routability is not feasible (SKILL.md:50-54); V3 criterion 1: "at least one routing test must change" is likely wrong for the routing table (test :105, :336-340; UNVERIFIED by run) |
| Structure (5) | 5 | 5 | 5 | none |
| Clarity (5) | 4 | 5 | 4 | V1 criterion 5: revisit trigger has no date; V3 criterion 5: leaves "which table" to the PR |
| Risk coverage (5) | 3 | 3 | 3 | All: no monitoring and no recovery path stated |
| Invariant and edge case (5) | 2 | 2 | 3 | V3 names both tables' guards, the person-only guard and the #539 file overlap |
| Total (30) | 23 | 23 | 23 | |
| qual_score | 0.767 | 0.767 | 0.767 | |

Edge case floor: all eligible.

## Position-Bias Mitigation
Reverse-order re-check changed no verdict. Not independent.

## Combined Scoring

| Variant | Score |
|---|---|
| V1 | 0.868 |
| V2 | 0.872 |
| V3 | 0.863 |

Within 5%: tiebreaker. Level 1, scored points won: V3 won C-002, C-005, X-001, X-003 and shares C-001 and C-004 (4 outright); V2 won C-003 and X-002 (2 outright) and shares C-001, C-004; V1 won none. Variant 3 is selected. This matches 2 of 3 unassigned picks.

## Selected Base: Variant 3 (proposal-C, one routing row after #539)

- Rationale: the only placement `/sc:recommend` reads (verified); keeps OB-07 unchanged; recommended by the spec and the source review.
- Preserve: own small PR after #539; named test edits; "person only".
- Incorporate: from V2's advocate and V3's own advocate, name the routing table now (not "either table"), cite a numbered section, and run the routing tests before naming any edit, because INV-029 appears overstated for the routing table; from V2, the "person only" text also beside the never-as-worker bullet; from V1 (U-001), describe only what the observer does on master today, no flags or panels that are still off.
