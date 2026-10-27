# D-0012: TurnLedger Extensions

## Location
`src/superclaude/cli/sprint/models.py` — TurnLedger dataclass

## New Fields (NFR-004: all default to 0)
- `wiring_turns_used: int = 0` — cumulative turns consumed by wiring analysis
- `wiring_turns_credited: int = 0` — cumulative turns credited back
- `wiring_budget_exhausted: int = 0` — flag: 1 if budget exhausted

## New Methods
- `debit_wiring(turns=1)` — debit before analysis, tracks wiring-specific consumption, sets exhausted flag
- `credit_wiring(turns, rate)` — floor-to-zero credit arithmetic: `int(turns * rate)`. `credit_wiring(1, 0.8)` returns 0 (R7)
- `can_run_wiring_gate()` — boolean check: not exhausted and available >= minimum_remediation_budget

## Verification
- `credit_wiring(1, 0.8)` returns exactly 0 (floor-to-zero verified)
- All 3 new fields default to 0 (NFR-004 verified)
- `debit_wiring()` decrements available turns and increments wiring_turns_used
- `can_run_wiring_gate()` returns False when budget exhausted
