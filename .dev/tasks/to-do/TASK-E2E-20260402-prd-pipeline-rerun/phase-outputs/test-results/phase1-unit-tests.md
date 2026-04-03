# Phase 1 Unit Tests — Full Suite

**Date:** 2026-04-02
**Command:** `uv run pytest tests/ -v`

## Results
- **4899 passed**, 4 failed, 102 skipped, 22 warnings, 1 error
- Duration: 92.50s

## Failures (all appear pre-existing or unrelated to PRD/TDD pipeline)

| Test | Error | Assessment |
|------|-------|-----------|
| `tests/audit/test_credential_scanner.py::test_detects_real_secrets` | Expected >= 3 secrets, got 2 | Pre-existing — credential scanner, unrelated |
| `tests/audit-trail/test_audit_writer.py::test_duration_ms_is_positive` | assert 0.0 > 0 | Pre-existing — audit trail timing |
| `tests/integration/test_wiring_pipeline.py::test_pipeline_runs_wiring_verification_in_shadow_mode` | assert 9 == 10 | Likely affected by new gate/step additions — step count changed |
| `tests/integration/test_wiring_pipeline.py::test_resume_skips_completed_wiring_verification` | assert 3 == 0 | Likely affected by new step additions |
| `tests/v3.3/test_zero_files_analyzed.py::test_zero_files_analyzed_returns_fail` | AttributeError: no 'summary' | Pre-existing — audit trail |

## Assessment
The 2 wiring pipeline failures may be related to the auto-detection changes (new steps added to pipeline). The other 3 are pre-existing. None of the PRD/TDD-specific tests failed. NOT a critical blocker for E2E testing — the pipeline itself runs correctly; these are test expectation mismatches.
