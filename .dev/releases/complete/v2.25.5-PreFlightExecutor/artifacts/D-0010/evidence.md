# D-0010 Evidence — Round-Trip Integration Test for Execution Mode Column

## Task
T01.08 — Round-Trip Integration Test for Execution Mode Column

## Test Class
`TestRoundTripExecutionMode` in `tests/sprint/test_preflight.py`

## Tests

| Test | Description |
|---|---|
| `test_round_trip_execution_mode` | Writes index with python/claude/skip, parses, asserts all 3 modes correct |
| `test_round_trip_execution_mode_absent_column` | Writes index without Execution Mode column, asserts all default to "claude" |
| `test_round_trip_case_normalization` | "Python" normalizes to "python" |
| `test_round_trip_invalid_mode_raises` | "invalid" raises ClickException with actionable message |

## Verification
- `uv run pytest tests/sprint/test_preflight.py -v -m integration` → **4 passed**
- All tests use `tmp_path` fixture — no persistent files left after test run ✓

## Date
2026-03-16
