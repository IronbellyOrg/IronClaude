# Evidence: D-0020 — Integration Tests: Execution and Timeout

## Task
T03.05 — Integration Tests for Preflight Execution and Timeout

## Test File
`tests/sprint/test_preflight.py` — class `TestPreflightExecution`

## Tests

### test_preflight_echo_hello
- Command: `echo hello`
- Asserts: `status == PhaseStatus.PREFLIGHT_PASS`, `exit_code == 0`
- Uses real subprocess (no mocking)

### test_preflight_exit_code_captured
- Command: `false`
- Asserts: `status == PhaseStatus.HALT`, `exit_code == 1`
- Uses real subprocess (no mocking)

### test_preflight_timeout
- Patches `subprocess.run` to raise `subprocess.TimeoutExpired`
- Asserts: `status == PhaseStatus.HALT`, graceful handling (no uncaught exception)

### test_preflight_filters_only_python_mode
- Two phases: python + claude mode
- Asserts: only 1 result returned, for phase 1 (python mode only)

## Verification

Test command: `uv run pytest tests/sprint/test_preflight.py -v -k "echo or timeout"` — 2 passed

Full suite: `uv run pytest tests/sprint/test_preflight.py -v` — 46 passed
