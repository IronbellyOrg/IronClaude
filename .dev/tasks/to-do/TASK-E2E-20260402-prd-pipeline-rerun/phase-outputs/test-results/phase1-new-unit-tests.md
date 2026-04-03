# Phase 1 New QA-Added Unit Tests

**Date:** 2026-04-02
**Command:** `uv run pytest tests/cli/test_tdd_extract_prompt.py -v`

## Results: 68 passed in 0.10s (ALL PASS)

### New Test Classes (23 tests)
| Class | Tests | Status |
|-------|-------|--------|
| TestPrdDetection | 4 (real fixture, synthetic signals, not-confused-with-tdd, not-confused-with-spec) | ALL PASS |
| TestThreeWayBoundary | 4 (below-threshold-is-spec, at-threshold-is-prd, tdd-only-is-tdd, both-prd-wins) | ALL PASS |
| TestMultiFileRouting | 10 (single-spec, single-tdd, single-prd-raises, spec+tdd, spec+prd, tdd+prd, all-three, duplicate-raises, too-many-raises, conflict-raises) | ALL PASS |
| TestBackwardCompat | 3 (single-positional, explicit-input-type-override, explicit-tdd-flag) | ALL PASS |
| TestOverridePriority | 2 (input-type-ignored-multifile, explicit-prd-flag-multifile) | ALL PASS |

### Original Test Classes (45 tests) — All Still Pass
TestAutoDetection, TestExtractPromptTddContent, TestExtractPromptTddWithPrd, TestMergePromptTddPrd, TestOldSchemaStateBackwardCompat, TestDetectionThresholdBoundary, TestSameFileGuard, TestPrdFileOverrideOnResume, TestRedundancyGuardStatePersistence
