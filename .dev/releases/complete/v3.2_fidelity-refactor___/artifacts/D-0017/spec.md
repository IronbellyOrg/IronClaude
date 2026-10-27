# D-0017: SOFT Mode and Null-Ledger Compatibility

## Location
`src/superclaude/cli/sprint/executor.py` — `run_post_task_wiring_hook()`

## SOFT Mode (Goal-5b)
- Surfaces critical findings as warnings via `_wiring_logger.warning()`
- Task status unchanged (no FAIL set)
- Credits wiring turns back after analysis
- Functionally distinct from SHADOW (warnings are user-visible) and BLOCKING (no task failure)

## Null-Ledger Compatibility (NFR-004)
All TurnLedger operations guarded with `if ledger is not None`:
- Budget guard: skipped when `ledger is None` (analysis runs unconditionally)
- `debit_wiring()`: skipped
- `credit_wiring()`: skipped
- `can_remediate()`: skipped
- No crashes, no budget operations
- Behavior matches prior (pre-hook) state exactly

## Verification
- `run_post_task_wiring_hook(task, config, result, ledger=None)` with off mode: status unchanged
- `run_post_task_wiring_hook(task, config, result, ledger=None)` with shadow mode: status unchanged
- No AttributeError or NoneType errors on null ledger path
