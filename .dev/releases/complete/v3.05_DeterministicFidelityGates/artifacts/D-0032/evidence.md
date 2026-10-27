# D-0032: Legacy Budget Isolation Evidence

## Verification Method
Source code analysis of both convergence.py and executor.py.

## Evidence
1. `convergence.py` contains ZERO references to `_check_remediation_budget` or `_print_terminal_halt`
2. `executor.py` does not import TurnLedger at module level
3. TurnLedger is only available via `_get_turnledger_class()` in convergence.py (conditional import)
4. Legacy remediation budget (2 attempts) is untouched by convergence mode

## Test Coverage
- `TestBudgetIsolation::test_convergence_module_no_legacy_budget_refs` — PASS
- `TestBudgetIsolation::test_turnledger_not_in_legacy_path` — PASS
