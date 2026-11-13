# Invariant Probe Results

## Round 2.5 - Fault-Finder Analysis (independent agent, sonnet class)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | guard_conditions | A zero-edit proof for the current cycle is enough to release a guard that may still hold an earlier cycle's unpublished fix | UNADDRESSED | MEDIUM | source.md:155 (release row 7 RELEASE(no_edits) before row 8), :156, :69; plan:75 and :166 require a zero-edit cycle after a fixing cycle to RELEASE; sequence: cycle 1 edits and its push is held (row 9), cycle 2 makes no edits, row 7 readies the PR with cycle 1's commit still local |
| INV-002 | guard_conditions | Engage row order is safe for an originally-draft PR | UNADDRESSED | LOW | source.md:140 (row 8 HALT_UNAVAILABLE timeline_unreadable) precedes :142 (row 10 SKIP_ALREADY_DRAFT); an already-draft PR with a flaky timeline call halts before any edit; plan:70 copies "all 11 rows", plan:73-74 do not cover this ordering |
| INV-003 | state_variables | failed_mutations and unsettled slack stays small and correct | UNADDRESSED | LOW | source.md:199, :205 (no decrement), :119, :122; one extra slack unit stays for the rest of the run; only the is_draft contradiction check backstops it; plan:70 tests only failed-but-landed not-foreign |
| INV-004 | collection_boundaries | next_cycle_number takes a numeric maximum | UNADDRESSED | LOW | source.md:102; plan:59 checks fix-1 and fix-2 giving 3, which a lexicographic implementation also passes (ci-9 versus ci-10) |
| INV-005 | count_divergence | The 43 to 45 count and the test counts are consistent | ADDRESSED | LOW | base-commit 43 claims at models.py:3, :24, run_log.py:117, loop-guard.md:86, :88 all covered by plan:44, :49; 11/9/9 decision rows match plan:70; twelve test names match source.md section 7; residual: plan:60 names no case for settled(ready, failed), settled(ready, confirmed, changed), settled(any, skipped, user_override) |
| INV-006 | sufficiency_challenge | Following the plan delivers a correct guard | UNADDRESSED | MEDIUM | falsifier: held guard across two cycles, crash after fix-2's push; guard keeps cycle_id fix-1 (source.md:139, :108); resume row 4 (:166) sees published true from fix-1; row 8 (:156) gets a target_sha that no spec text or plan task sources (plan:70, :124, :75-77); a conforming implementation passes every acceptance criterion and still fails the scenario; combined with INV-001 one no_edits release erases both safety rules |

## Summary

- **Total findings**: 6
- **ADDRESSED**: 1
- **UNADDRESSED**: 5
  - HIGH: 0
  - MEDIUM: 2 (INV-001, INV-006)
  - LOW: 3 (INV-002, INV-003, INV-004)

Gate result: no HIGH-severity UNADDRESSED item, so convergence is not blocked. MEDIUM items logged as warnings.
