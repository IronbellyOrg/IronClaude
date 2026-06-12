# Atom 1 — Test Summary

**Command:** `uv run pytest tests/cli/prd/ -v`
**Date:** 2026-06-08
**Raw output:** `atom1-pytest-output.txt`

## Overall Result: PASSED

| Metric | Count |
|--------|-------|
| Total | 155 |
| Passed | 155 |
| Failed | 0 |
| Skipped | 0 |

## New tests (Atom 1) — explicit results

| Test | Result |
|------|--------|
| `test_models.py::...::test_is_hard_failure_membership` (is_hard_failure membership) | PASSED |
| `test_e2e.py::test_e2e_standard_tier_error_halts_pipeline` (STANDARD ERROR halts) | PASSED |
| `test_e2e.py::test_e2e_standard_tier_validation_fail_does_not_halt` (STANDARD VALIDATION_FAIL does NOT halt) | PASSED |

## Pre-existing tests confirmed still passing

| Test | Result |
|------|--------|
| `test_e2e.py::test_e2e_budget_exhaustion` (budget exhaustion → halt) | PASSED |
| `test_integration.py::test_prd_pipeline_budget_exhaustion` | PASSED |
| `test_models.py::...::test_prd_step_status_properties` (is_failure/is_terminal membership) | PASSED |

STRICT-halt semantics are exercised by the broader e2e/integration/gate suites
(e.g. STRICT gates in `test_spec_flag.py`, `test_integration.py`) — all green.

## Failures

None.
