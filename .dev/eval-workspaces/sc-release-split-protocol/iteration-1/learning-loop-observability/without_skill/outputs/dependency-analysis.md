# Dependency Analysis: Observability & Adaptive Alerting System

## Requirement Dependency Graph

```
R1 (Telemetry SDK)          -- no dependencies, foundation layer
  |
  v
R2 (Pipeline Instrumentation) -- depends on R1 (needs SDK to emit events)
  |
  v
R3 (Metrics Aggregation)     -- depends on R1+R2 (needs telemetry data to aggregate)
  |
  +---> R4 (Dashboard UI)    -- depends on R3 (reads metrics DB)
  |
  +---> R5 (Adaptive Alerts) -- depends on R3 + ACCUMULATED DATA (bootstrap period)
  |       |
  |       v
  |     R6 (Alert Config)    -- depends on R5 (configures alert engine)
  |
  v
R7 (Historical Import)       -- depends on R1+R3 (backfills telemetry/metrics stores)
  |
  v
R8 (Cross-Pipeline Corr.)    -- depends on R3 + R5 + ACCUMULATED CROSS-PIPELINE DATA
```

## Data Dependencies (the critical factor)

The spec explicitly identifies a **learning loop dependency** that makes monolithic delivery problematic:

1. **R5 (Adaptive Alerts)** requires a bootstrap period of N runs (default 20) before it can activate. This is not a code dependency -- it is a *data dependency*. The alert engine literally cannot compute meaningful thresholds without historical observations.

2. **R8 (Cross-Pipeline Correlation)** requires data from multiple pipeline types over time. It cannot produce useful correlations until there is sufficient cross-pipeline telemetry volume.

3. **R3 (Metrics Aggregation)** can compute baselines only after telemetry data exists. The anomaly detection (>2 sigma from rolling baseline) requires enough data points for statistical validity.

## The Learning Loop

```
Collect telemetry (R1+R2)
       |
       v
Accumulate data over real usage (TIME PASSES)
       |
       v
Compute baselines from real data (R3)
       |
       v
Set adaptive thresholds from baselines (R5)
       |
       v
Observe alert accuracy on new data (TIME PASSES)
       |
       v
Tune thresholds from user feedback (R5+R6)
```

Each arrow marked "TIME PASSES" represents a mandatory waiting period where real pipeline executions must occur. No amount of code completeness eliminates this wait.

## Split-Forcing Dependencies

| Dependency Type | Between | Implication |
|----------------|---------|-------------|
| Code dependency | R2 -> R1 | R1 must ship before or with R2 |
| Code dependency | R3 -> R1+R2 | R3 needs telemetry flowing |
| Code dependency | R4 -> R3 | Dashboard needs metrics DB |
| Code dependency | R5 -> R3 | Alert engine needs metrics engine |
| Code dependency | R6 -> R5 | Config needs alert engine |
| **Data dependency** | **R5 -> accumulated telemetry** | **Cannot set thresholds without history** |
| **Data dependency** | **R8 -> accumulated cross-pipeline data** | **Cannot correlate without volume** |
| Data dependency | R3 anomaly detection -> baseline data | Needs enough runs for statistical significance |

The data dependencies are the strongest argument for splitting. They represent irreducible waiting periods.
