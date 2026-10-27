# D-0033: Regression Detection Trigger

## Summary
Regression trigger fires when `current_run.structural_high_count > previous_run.structural_high_count`.

## Behavior
- Structural HIGH increase triggers `handle_regression()`
- Semantic HIGH increases alone do NOT trigger regression (logged as warning)
- `ledger.debit(REGRESSION_VALIDATION_COST)` called BEFORE `handle_regression()` invocation
- `handle_regression()` does not perform any ledger operations internally
- Regression only checked on run_idx > 0 (Run 1 is baseline)

## Verification
- `uv run pytest tests/roadmap/test_convergence.py -v -k "regression_trigger"` — all pass
