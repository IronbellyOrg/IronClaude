# Invariant Probe Results

## Round 2.5 - Fault-Finder Analysis

The fault-finder agent did not read the debate files and probed the plan and spec from the consensus summary the orchestrator supplied. Plan line numbers are from `TASK-WF-designSpec-20261107-075614.md`, spec line numbers from `source.md`.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | Fixing M1 to M4 makes the plan executable (M4 fix cannot satisfy both "names L3 and draft" and "test forbids them") | ADDRESSED (orchestrator adjudication) | HIGH as reported | plan 137, 140; spec 241. Adjudication: plan 137 itself says the test bans "`L3 only` or `draft` gate wording", so the AC at 140 ("names an L3 or `draft` condition") reads as gate wording; V2 and V3 both conceded non-blocking in Round 2. Kept as MAJOR non-blocking finding G4 so the wording gets fixed. |
| INV-002 | guard_conditions | decision tables work for `guard is None` | ADDRESSED | LOW (reported MEDIUM) | spec 133-143, 114-125. The first-engage path in Task 11's acceptance trace (plan 170) runs with no guard and would fail on an AttributeError. |
| INV-003 | state_variables | M3 is only a missing second-cycle test | UNADDRESSED | MEDIUM | spec 108, 166, 184, 194-206; plan 56-64. Merged into finding G3. |
| INV-004 | interaction_effects | resume row 4 can re-enter release_decision with only `push_completed=True` | UNADDRESSED | MEDIUM | spec 152-157, 166; plan 77. No task says `target_sha` and `applied_edits` come from the `push_initiated` and `fix_applied` events. Finding G12. |
| INV-005 | sufficiency_challenge | per-cycle `applied_edits` is available to the SKILL | UNADDRESSED | MEDIUM | spec 107; plan 70, 124. Merged into finding G12. |
| INV-006 | interaction_effects | Task 11 can reuse Task 7's fake `gh` | UNADDRESSED | MEDIUM | plan 108, 111-112, 166-172. Finding G13. |
| INV-007 | collection_boundaries | `:a<k>` retry counting is covered | UNADDRESSED | LOW | spec 184; plan 62 |
| INV-008 | count_divergence | fold test covers every row | UNADDRESSED | LOW | spec 194-206; plan 60 (V2 withdrew C-012 on the "covers every row" wording) |
| INV-009 | guard_conditions | dependency edges complete | UNADDRESSED | LOW | plan 120-122, 134-135, 179-180 |
| INV-010 | state_variables | O1 resolves to one place and Task 10 matches | UNADDRESSED | LOW | plan 127, 150 |

## Summary

- **Total findings**: 10
- **ADDRESSED**: 2 (INV-001 by adjudication, INV-002)
- **UNADDRESSED**: 8
  - HIGH: 0 (after adjudication)
  - MEDIUM: 4 (INV-003, INV-004, INV-005, INV-006)
  - LOW: 4
