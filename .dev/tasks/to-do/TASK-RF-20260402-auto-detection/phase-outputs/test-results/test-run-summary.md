# Test Run Summary

**Date:** 2026-04-02
**Command:** `uv run pytest tests/cli/test_tdd_extract_prompt.py tests/roadmap/ tests/tasklist/ -v --tb=short`

## Overall Result: PASSED

| Metric | Count |
|--------|-------|
| Total tests | 1637 |
| Passed | 1627 |
| Failed | 0 |
| Skipped | 10 |

## Fix Cycle

- **Run 1 (pre-QA):** 66 passed in test_tdd_extract_prompt.py, 2 failed (TestSameFileGuard tests expected old SystemExit, got click.UsageError)
- **Fix 1:** Updated TestSameFileGuard to expect click.UsageError (behavioral change from inline guard to _route_input_files)
- **Run 2 (pre-QA):** 68 passed in test_tdd_extract_prompt.py, 0 failed (but only ran detection tests, not full scope)
- **QA Run 1:** Full scope per step 6.1 command -- 1620 passed, 7 failed, 10 skipped. 7 failures in tests/roadmap/test_spec_patch_cycle.py (regression from _route_input_files + dataclasses.replace on MagicMock configs)
- **Fix 2 (QA):** Added `tdd_file=None`, `prd_file=None`, `input_type="auto"` to `_make_mock_config()` and created `_routing_patches()` helper to mock `_route_input_files` and `dataclasses.replace` in 7 affected tests
- **QA Run 2:** 1627 passed, 0 failed, 10 skipped

## New Tests Added (22 tests across 5 classes)

- TestPrdDetection: 4 tests (real fixture, synthetic signals, TDD/spec confusion)
- TestThreeWayBoundary: 4 tests (below threshold, at threshold, TDD only, both signals)
- TestMultiFileRouting: 10 tests (single file x3, multi-file x4, error cases x3)
- TestBackwardCompat: 3 tests (single positional, explicit override, flag supplement)
- TestOverridePriority: 2 tests (input-type ignored for multi, explicit prd flag)

## Existing Tests: All 1605 passed across 3 test directories (no regressions after QA fix)

## Skipped Tests (10)

All 10 skipped tests are pre-existing skips unrelated to this task (in tests/roadmap/).
