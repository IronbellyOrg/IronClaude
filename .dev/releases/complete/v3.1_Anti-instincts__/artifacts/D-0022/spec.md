# D-0022: KPI Report Integration

**Task**: T03.02
**Status**: COMPLETE

## Implementation

Anti-instinct gate results are captured via `ShadowGateMetrics` which feeds into sprint-level KPI reporting. The `gate_outcome` field on `TaskResult` is set by the anti-instinct hook (PASS or FAIL) and flows into `AggregatedPhaseReport.to_yaml()` / `to_markdown()`.

The existing `build_kpi_report()` in `kpi.py` already aggregates `TrailingGateResult` objects from the pipeline; anti-instinct results feed in via the same `gate_outcome` field on `TaskResult`.

## Verification
- 738 sprint tests pass with zero regressions
