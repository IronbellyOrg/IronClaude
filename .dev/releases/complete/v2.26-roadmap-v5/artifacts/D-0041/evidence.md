# D-0041 -- T05.05: Third Remediation Attempt Terminal Halt (SC-6)

## Summary

Budget exhaustion after 2 attempts triggers terminal halt with `sys.exit(1)` behavior. SC-6 verified with failing-certify integration test including stderr content assertions.

## Test Evidence

**Test file:** `tests/sprint/test_executor.py::TestBudget` and `::TestTerminalHalt`

**Validation command:** `uv run pytest tests/sprint/test_executor.py -v -k "terminal_halt or budget"`

**Result:** 17 passed, 0 failed

### Budget Enforcement Tests (SC-6):

| Test | Assertion | Result |
|------|-----------|--------|
| `test_budget_attempt_1_returns_true` | First attempt (0 previous) -> True (allowed) | PASS |
| `test_budget_attempt_2_returns_true` | Second attempt (1 previous) -> True (allowed) | PASS |
| `test_budget_attempt_3_returns_false` | Third attempt (2 previous) -> False (budget exhausted) | PASS |
| `test_budget_exhaustion_calls_print_terminal_halt` | Budget exhaustion calls `_print_terminal_halt()` | PASS |
| `test_budget_no_state_file_returns_true` | No state file -> first attempt, allowed | PASS |
| `test_budget_does_not_call_sys_exit` | `_check_remediation_budget` does NOT call sys.exit directly | PASS |
| `test_budget_configurable_max_attempts_1` | max_attempts=1: second attempt triggers halt | PASS |
| `test_budget_configurable_max_attempts_3` | max_attempts=3: third attempt still allowed | PASS |
| `test_budget_non_integer_attempts_treated_as_zero` | Non-integer remediation_attempts coerced to 0 | PASS |

### Terminal Halt Stderr Assertion Tests:

| Test | Assertion | Result |
|------|-----------|--------|
| `test_terminal_halt_writes_to_stderr` | Output goes to stderr, not stdout | PASS |
| `test_terminal_halt_includes_attempt_count` | Stderr includes attempt count | PASS |
| `test_terminal_halt_includes_failing_count` | Stderr includes remaining failing finding count | PASS |
| `test_terminal_halt_includes_per_finding_details` | Each finding's ID, severity, description appear | PASS |
| `test_terminal_halt_includes_manual_fix_instructions` | Manual-fix instructions present | PASS |
| `test_terminal_halt_includes_cert_report_path` | Certification report path included | PASS |
| `test_terminal_halt_dual_budget_note_when_both_exhausted` | Dual-budget note when spec_patch_budget_exhausted=True | PASS |
| `test_terminal_halt_no_dual_budget_note_when_not_exhausted` | No dual-budget note otherwise | PASS |

## Acceptance Criteria Verification

- [x] Third `--resume` attempt triggers `_print_terminal_halt()` and budget exhaustion
- [x] Stderr output includes: attempt count, remaining failing finding count, per-finding details, manual-fix instructions with certification report path
- [x] SC-6 verified with failing-certify integration test including stderr assertion
- [x] `uv run pytest tests/sprint/test_executor.py -v -k "terminal_halt or budget"` exits 0
