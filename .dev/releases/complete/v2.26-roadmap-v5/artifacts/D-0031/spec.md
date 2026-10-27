# D-0031: _check_remediation_budget() Implementation

## Summary

Implemented `_check_remediation_budget()` in `src/superclaude/cli/roadmap/executor.py`.

## Function Signature

```python
def _check_remediation_budget(
    state_file: Path,
    max_attempts: int = 2,
) -> bool:
```

## Behavior

- Reads `remediation_attempts` from state file; coerces to int (WARNING on failure, treat as 0)
- Returns True if `attempts < max_attempts` (budget allows another attempt)
- On `attempts >= max_attempts`: calls `_print_terminal_halt()`, returns False
- Does NOT call `sys.exit(1)` directly (Constraint #12 compliance)
- Caller is responsible for `sys.exit(1)` on False return

## Configurable max_attempts

- Default: 2 (FR-040: max 2 remediation attempts)
- `max_attempts=1`: triggers halt on second attempt
- `max_attempts=3`: allows third attempt

## Test Results

`uv run pytest tests/sprint/test_executor.py -v -k "budget"` — **11 passed**
- Attempts 0, 1 → True (allowed)
- Attempt 2 → False (budget exhausted), calls _print_terminal_halt
- No state file → True (first attempt)
- sys.exit NOT called directly — confirmed
- max_attempts=1 triggers halt on second attempt
- max_attempts=3 allows third attempt
- Non-integer coerced to 0 with WARNING
