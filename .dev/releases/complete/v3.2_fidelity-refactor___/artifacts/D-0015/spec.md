# D-0015: BLOCKING Mode Path (full)

## Location
`src/superclaude/cli/sprint/executor.py` — `run_post_task_wiring_hook()`, `mode == "full"` branch

## Implementation
- Fails sprint task when blocking findings detected: `task_result.status = TaskStatus.FAIL`
- Sets `task_result.gate_outcome = GateOutcome.FAIL`
- Invokes remediation via callable interface (Constraint 7):
  - `can_remediate = ledger.can_remediate` (callable, no TurnLedger import in trailing_gate)
  - `debit = lambda turns: ledger.debit(turns)` (callable wrapper)
  - If `can_remediate()`: debits `config.remediation_cost` turns
  - If not: logs BUDGET_EXHAUSTED warning without crash
- When no blocking findings: credits turns back via `ledger.credit_wiring()`
- Functionally distinct from SHADOW (log only) and SOFT (warn only)

## Goal-5c Compliance
- BLOCKING mode causes sprint task failure on wiring defect detection
- Triggers remediation via callable interface
