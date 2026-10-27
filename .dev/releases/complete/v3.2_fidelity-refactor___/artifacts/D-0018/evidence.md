# D-0018: TurnLedger Unit Test Evidence

## Test Location
`tests/sprint/test_models.py` — class `TestTurnLedgerWiringExtensions`

## Test Results
```
tests/sprint/test_models.py::TestTurnLedgerWiringExtensions::test_wiring_debit_tracks_correctly PASSED
tests/sprint/test_models.py::TestTurnLedgerWiringExtensions::test_credit_wiring_floor_to_zero PASSED
tests/sprint/test_models.py::TestTurnLedgerWiringExtensions::test_debit_credit_wiring_cycle PASSED
```

All 3 tests passing. Full suite: 233 tests passing across models, executor, shadow mode, and anti-instinct sprint tests.

## Test Descriptions

### test_wiring_debit_tracks_correctly
- `debit_wiring(1)` increments `wiring_turns_used` to 1 and `consumed` to 1
- `available()` returns 99 (100 - 1)
- `wiring_budget_exhausted` remains 0 when budget is plentiful

### test_credit_wiring_floor_to_zero (SC-012)
- `credit_wiring(1, 0.8)` returns exactly 0 (floor-to-zero by design, R7)
- `wiring_turns_credited` remains 0
- `reimbursed` remains 0

### test_debit_credit_wiring_cycle (SC-013)
- Cycle 1: debit 3, credit 3 at 0.8 -> int(3*0.8)=2 credits
  - wiring_turns_used=3, wiring_turns_credited=2, available=99
- Cycle 2: debit 5, credit 5 at 0.8 -> int(5*0.8)=4 credits
  - wiring_turns_used=8, wiring_turns_credited=6, available=98

## Additional Verification
- Pre-existing executor tests updated to use `wiring_gate_mode="off"` to isolate budget arithmetic from wiring hook behavior
- 77 executor tests passing
- 18 pre-existing TurnLedger budget tests still passing
