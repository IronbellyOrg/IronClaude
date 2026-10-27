# D-0028: TurnLedger Integration

## Summary
Conditional import of TurnLedger from `superclaude.cli.sprint.models` via `_get_turnledger_class()` helper. Only imported when convergence mode is active. Pipeline executor constructs TurnLedger when `convergence_enabled=true`.

## Implementation
- `_get_turnledger_class()` in `convergence.py` provides conditional import
- `can_launch()` guard checked before each checker run
- `can_remediate()` guard checked before each remediation
- Budget exhaustion halts with diagnostic report including TurnLedger state

## Verification
- `uv run pytest tests/roadmap/test_convergence.py -v -k "turnledger or budget or reimburse"` — all pass
