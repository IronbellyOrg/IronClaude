# D-0014: run_post_task_wiring_hook Refactor

## Location
`src/superclaude/cli/sprint/executor.py`

## Changes

### New function: `_resolve_wiring_mode(config)`
Helper that maps `config.wiring_gate_scope` through `resolve_gate_mode()` (Goal-5d).
Falls back to `config.wiring_gate_mode` string when scope resolution is not applicable.

### Refactored: `run_post_task_wiring_hook(task, config, task_result, ledger=None)`
- Added `ledger: TurnLedger | None = None` parameter
- Budget guard: `ledger.can_run_wiring_gate()` check before analysis
- Debit-before-analysis: `ledger.debit_wiring(config.wiring_analysis_turns)` before running
- Mode-specific credit/debit on findings:
  - shadow/soft: credit turns back after analysis
  - full: debit remediation_cost on blocking findings via callable interface
- Callable-based remediation: `can_remediate` and `debit` from ledger (Constraint 7)
- Budget exhaustion handled: logs BUDGET_EXHAUSTED without crash

### Updated call site: `execute_phase_tasks()`
Now passes `ledger=ledger` to `run_post_task_wiring_hook()`.

## NFR-006 Verification
Zero modifications to `pipeline/models.py`, `pipeline/gates.py`, `pipeline/trailing_gate.py`.
