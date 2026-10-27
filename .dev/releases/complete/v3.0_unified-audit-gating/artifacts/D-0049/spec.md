# D-0049: Mode-Aware Wiring Hook Behavior

## Deliverable
Mode-aware behavior table for sprint wiring hook, integrated in `run_post_task_wiring_hook()`.

## Mode Semantics
| Mode | Analysis | Logging | Status Change | Gate Effect |
|------|----------|---------|---------------|-------------|
| off | Skipped | None | None | None |
| shadow | Runs | INFO (findings count) | None (SC-006) | None |
| soft | Runs | WARNING (critical) | None | None |
| full | Runs | ERROR (blocking) | FAIL if blocking > 0 | GateOutcome.FAIL |

## Blocking Count by Mode
- shadow: always 0 (never blocks)
- soft: critical unsuppressed only
- full: critical + major unsuppressed
