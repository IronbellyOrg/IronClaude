# D-0029: Convergence Budget Constants

## Summary
Module-level cost constants in `convergence.py`:
- `CHECKER_COST=10`
- `REMEDIATION_COST=8`
- `REGRESSION_VALIDATION_COST=15`
- `CONVERGENCE_PASS_CREDIT=5`

Derived budgets:
- `MIN_CONVERGENCE_BUDGET=28`
- `STD_CONVERGENCE_BUDGET=46`
- `MAX_CONVERGENCE_BUDGET=61`

## Implementation
- `reimburse_for_progress()` helper uses `ledger.reimbursement_rate`
- Returns 0 when `curr_structural_highs >= prev_structural_highs`
- Progress credit logged: "Run {n}: progress credit {credit} turns (structural {prev} -> {curr})"

## Verification
- Constants verified in `TestTurnLedgerIntegration` test class
