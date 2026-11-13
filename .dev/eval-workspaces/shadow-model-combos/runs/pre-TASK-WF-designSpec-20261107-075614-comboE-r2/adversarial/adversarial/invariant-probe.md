# Invariant Probe Results (orchestrator-written; no separate fault-finder agent)
## Round 2.5 - Analysis of the emerging consensus
| ID | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
| INV-001 | state_variables | `original_is_draft` survives a resume | ADDRESSED | LOW | Spec 4.2 (source.md:208) and Task 3 fold ACs |
| INV-002 | guard_conditions | engage rows read `guard.phase` when `guard` is None | ADDRESSED | LOW | Plan line 73: one test per row, including rows with no guard |
| INV-003 | count_divergence | `next_cycle_number` is "highest + 1", not a count | UNADDRESSED | MEDIUM | Plan line 59 uses fix-1 and fix-2 only (merged finding M11) |
| INV-004 | collection_boundaries | an empty log and a sparse log (fix-5 only) | UNADDRESSED | LOW | Empty log tested (plan 59); sparse log is not |
| INV-005 | interaction_effects | the guard's cycle id equals the push triad's id | UNADDRESSED | MEDIUM | No AC compares them (M4); scenario tests hand-match ids |
| INV-006 | sufficiency_challenge | the plan's ACs suffice to make the guard safe | UNADDRESSED | MEDIUM | Falsifier: the ref omits the event fields and key format (M1) while Task 3 and Task 11 tests build their own events and still pass |
## Summary
- Total findings: 6; ADDRESSED 2; UNADDRESSED 4 (HIGH 0, MEDIUM 3, LOW 1)
- No HIGH unaddressed item, so convergence is not blocked. The three MEDIUM items are warnings and map to merged findings M11, M4 and M1.
