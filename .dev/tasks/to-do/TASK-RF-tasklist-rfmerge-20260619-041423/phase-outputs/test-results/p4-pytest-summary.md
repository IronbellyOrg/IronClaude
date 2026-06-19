# P4 Pytest Summary

**Command:** `uv run pytest tests/tasklist/ -v`
**Raw output:** `p4-pytest.txt`

## Result

- **Total collected:** 73
- **Passed:** 73
- **Failed:** 0
- **Duration:** 0.21s
- **Status:** ✅ 73 passed

## Regression check vs baseline

- Baseline: 71/71 (see `baseline-summary.md`).
- After P4: 73/73 → **+2 new tests** (`test_gate_results_passthrough`,
  `test_self_check_count_is_20_not_17`), **zero regressions** against the 71/71 baseline.

## New P4 tests (both PASS)

| Test | Result |
|------|--------|
| `TestP4EvidenceAnchoredValidation::test_gate_results_passthrough` | PASSED |
| `TestP4EvidenceAnchoredValidation::test_self_check_count_is_20_not_17` | PASSED |

## Failures

None.
