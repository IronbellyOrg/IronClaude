# Pytest Summary

**Command:** `uv run pytest tests/roadmap/ -v`
**Result:** **PASSED**
**Exit code:** 0
**Date:** 2026-05-27

## Counts

- Total tests run: 1715 passed + 12 skipped = **1727**
- Tests passed: **1715**
- Tests failed: **0**
- Tests skipped: **12** (includes the new `test_structural_checkers_properties.py` module — module-level `pytest.importorskip("hypothesis")` cleanly skips when hypothesis is not installed; the same posture applies to other pre-existing property-based tests in the repo)
- Time: 5.00s

## Failed tests

| Test name | Error type | Brief message |
|---|---|---|
| _(none)_ | — | — |

## New tests added in Phases 4-5 — confirmation

| # | Test name | Status |
|---|---|---|
| 1 | `test_phantom_id_canonicalizes_zero_padded_d_ids` | ✅ PASSED |
| 2 | `test_phantom_id_genuine_phantom_still_emits_high` | ✅ PASSED |
| 3 | `test_phantom_id_canonicalizes_fr_subids` | ✅ PASSED |
| 4 | `test_phantom_id_canonicalizes_nfr_padding` | ✅ PASSED |
| 5 | `test_phantom_id_idempotent_on_unpadded` | ✅ PASSED |
| 6 | `test_canonicalization_property_holds_across_families` | ⏭ SKIPPED (hypothesis not installed — module skip is the intended posture per task spec) |
| 7 | `test_flatline_halt_emits_structural_verdict` | ✅ PASSED |
| 8 | `test_loop_reports_structural_when_all_remediations_exceed_diff_guard` | ✅ PASSED |

7 / 8 new tests RUN and PASS; 1 SKIPS cleanly when hypothesis is unavailable (the importorskip guard is exactly the behavior the task spec requested at Step 5.1).

## Fix cycles

1. **Cycle 1:** Initial run after Phase 5 + lint fix produced 3 failures in `TestSeverityRules`:
   - `test_exactly_19_rules` — expected 19 SEVERITY_RULES entries; the new `("signatures", "id_schema_drift"): "MEDIUM"` makes 20.
   - `test_11_medium_rules` — expected 11 MEDIUM rules; the new entry makes 12.
   - `test_all_canonical_rules_present` — expected set of 19 rule keys; missing the new `id_schema_drift` key.

   These are encoding-of-count tests that legitimately need to be updated to reflect the new rule. Updated via Edit on `tests/roadmap/test_structural_checkers.py`:
   - Renamed `test_exactly_19_rules` → `test_exactly_20_rules` (assertion updated to 20).
   - Renamed `test_11_medium_rules` → `test_12_medium_rules` (assertion updated to 12).
   - Added `("signatures", "id_schema_drift")` to the `expected` set in `test_all_canonical_rules_present`.

2. **Cycle 2:** Re-ran `uv run pytest tests/roadmap/ -v` — **all 1715 tests passed, 12 skipped, 0 failed.**

## Regression check

No pre-existing tests that were passing before this task now fail. The 3 failing tests in Cycle 1 were tests of *the SEVERITY_RULES table size*, not of structural behavior — they failed because the rules table grew by exactly the 1 entry the task spec required, and the count assertions had to be updated in lockstep with the table.

## Verdict: PASS — Green light for Phase 7 (restrictions audit).
