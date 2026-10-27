# D-0021: TurnLedger Credit/Remediation with None Guards

**Task**: T03.02
**Status**: COMPLETE

## Implementation

In `run_post_task_anti_instinct_hook()`:
- PASS path: `if ledger is not None: ledger.credit(int(turns * rate))`
- FAIL path: `if ledger is not None and not ledger.can_remediate(): BUDGET_EXHAUSTED`
- Full mode FAIL: `task_result.status = TaskStatus.FAIL`

ALL TurnLedger calls guarded with `if ledger is not None` per NFR-007.

## Verification
- 738 sprint tests pass with zero regressions
- Sprint runs without TurnLedger do not raise
