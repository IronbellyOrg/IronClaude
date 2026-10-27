# D-0020: ShadowGateMetrics Integration

**Task**: T03.02
**Status**: COMPLETE

## Implementation

`ShadowGateMetrics.record(passed, evaluation_ms)` is called in shadow, soft, and full modes within `run_post_task_anti_instinct_hook()`. NOT called in off mode.

The `execute_phase_tasks()` function accepts an optional `shadow_metrics: ShadowGateMetrics | None` parameter, passed through to the anti-instinct hook.

## Verification
- 738 sprint tests pass with zero regressions
