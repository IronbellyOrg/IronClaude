# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | interaction_effects | Per-cycle `applied_edits == 0` is always a safe release proof, so the per-cycle finding only needs a call-site criterion | UNADDRESSED | HIGH | source.md:155 (release row 7) precedes row 8 (source.md:156) and ignores earlier cycles; source.md:69 keeps the PR draft with no zero-edit proof; source.md:107 makes the count per cycle on purpose. If fix-1 is committed but unpublished (HOLD) and fix-2 has zero edits, the PR is released with fix-1 never pushed. Plan line 75 tests only a zero after a fixing cycle |
| INV-002 | interaction_effects | Conflict-merge cycles are fully handled by "never engaged" | UNADDRESSED | MEDIUM | source.md:149 (release NOOP for a conflict cycle); a sync push while HELD moves the head so later release row 8 gives head_mismatch; plan line 166 tests only that a conflict-cycle id never engages |
| INV-003 | sufficiency_challenge | The findings include everything the acceptance trace needs | UNADDRESSED | MEDIUM | plan lines 166 and 170 build the trace from a test driver, so release-before-re-trigger holds by construction; plan line 153 pins only that sentences exist; spec line 270 requires the order in a real run |
| INV-004 | sufficiency_challenge | Nothing user-visible beyond the findings is missing | UNADDRESSED | MEDIUM | source.md:143 carries `auto_merge_armed`; source.md:333 (G4) says converting to draft disarms auto-merge; no Task 8 or 13 criterion makes the report or guide say so |
| INV-005 | state_variables | `failed_mutations` slack is harmless | UNADDRESSED | LOW | source.md:199 and 205 only increment it; plan line 74 tests one extra transition only |
| INV-006 | collection_boundaries | `next_cycle_number` is correct for the plan's tests | UNADDRESSED | LOW | source.md:102; plan line 59 tests only fix-1 and fix-2; no fix-10 against fix-9 or unanchored `refix-3` case |
| INV-007 | guard_conditions | Release row 3 is only the read-failed case | UNADDRESSED | LOW | source.md:151-152 puts HOLD for a failed read before the OPEN check; plan line 75 tests HALT_PR_NOT_OPEN only for a successful read |
| INV-008 | count_divergence | The 43-to-45 update is complete when the Task 2 grep is clean | ADDRESSED | LOW | HEAD grep shows no stale enum count; no import cycle through conflicts (fsm and conflicts do not import run_log); Task 5 fresh-interpreter criterion covers it |

## Summary

- **Total findings**: 8
- **ADDRESSED**: 1
- **UNADDRESSED**: 7
  - HIGH: 1
  - MEDIUM: 3
  - LOW: 3

Orchestrator check: INV-001's cited lines were re-read; its row-7 citation (156) was off by one, row 7 is source.md:155.
