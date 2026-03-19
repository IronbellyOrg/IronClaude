---
release: 1
parent-spec: .claude/skills/sc-release-split-protocol-workspace/evals/files/spec-learning-loop-observability.md
split-proposal: split-proposal-final.md
scope: "Telemetry foundation, metrics engine, dashboard, historical import"
status: draft
validation-gate: null
---

# Release 1 — Telemetry Foundation & Metrics Visibility

## Objective

Deliver a complete observability layer for SuperClaude's CLI pipelines: structured telemetry collection, metrics aggregation with anomaly detection, a visual dashboard, and historical baseline import. This release replaces the current "grep through stdout logs" workflow with queryable, visual pipeline health monitoring. It also begins collecting the baseline telemetry data that Release 2's adaptive alert engine requires for threshold learning.

## Scope

### Included

1. **R1: Telemetry Collection SDK (P0)** — From: original-spec Section 3, R1
   - Event schema: pipeline_type, phase, event_type, timestamp, duration_ms, token_count, status, metadata
   - Collection modes: local file (default), remote endpoint (opt-in)
   - Local storage: append-only JSONL files in `~/.superclaude/telemetry/`
   - Event types: pipeline_start, phase_start, phase_end, gate_check, gate_result, error, pipeline_end
   - Zero-overhead when disabled: telemetry collection must not slow pipelines
   - Privacy: no prompt content or LLM responses in telemetry — only structural metadata

2. **R2: Pipeline Instrumentation (P0)** — From: original-spec Section 3, R2
   - Sprint executor: phase start/end, task count, turn count, status, max_turns hit
   - Roadmap generator: phase start/end, gate checks, validation results, artifact counts
   - Tasklist generator: phase start/end, task decomposition metrics, tier distribution
   - Audit pipeline: pass start/end, finding counts by severity, scan coverage metrics
   - Must not change pipeline behavior — telemetry is read-only observation

3. **R3: Metrics Aggregation Engine (P0)** — From: original-spec Section 3, R3
   - Time-series aggregation: hourly, daily, weekly rollups
   - Per-pipeline baselines: mean, stddev, percentiles for key metrics (duration, tokens, success rate)
   - Anomaly detection: flag runs that deviate >2sigma from rolling baseline
   - Correlation analysis: identify relationships (e.g., task_count vs. phase_duration)
   - Storage: SQLite database in `~/.superclaude/metrics.db`
   - CLI query interface: `superclaude metrics show [pipeline] [--period 7d]`
   - **Forward-compatibility constraint**: Metrics schema must include tables/columns for alert threshold storage (initially empty) and user feedback tracking (initially unused) to support Release 2 without schema migration

4. **R4: Dashboard UI (P1)** — From: original-spec Section 3, R4
   - Pipeline health overview: success rate, avg duration, avg token cost per pipeline
   - Trend charts: metrics over time with anomaly highlighting
   - Run detail view: drill into individual pipeline executions
   - Comparison view: overlay multiple pipeline types or time periods
   - Tech stack: lightweight local server (Flask/FastAPI), Chart.js for visualizations
   - Launch: `superclaude dashboard` opens browser to localhost
   - **Alert placeholder**: Dashboard must include an "Alerts" panel/tab displaying status messaging about the upcoming adaptive alert engine (Release 2)

5. **R7: Historical Baseline Import (P2)** — From: original-spec Section 3, R7
   - Parse existing `phase-N-result.md` files for sprint metrics
   - Parse existing roadmap artifacts for gate pass/fail history
   - Parse existing audit reports for finding baselines
   - Backfill telemetry database with historical data
   - Estimate confidence intervals based on data density

### Excluded (assigned to Release 2)

1. **R5: Adaptive Alert Engine (P1)** — Deferred to: Release 2, Section "Included" item 1. Reason: requires bootstrap period of accumulated telemetry data from real pipeline runs. Cannot be meaningfully validated without baselines established by Release 1 production usage.

2. **R6: Alert Rule Configuration (P1)** — Deferred to: Release 2, Section "Included" item 2. Reason: depends on R5 alert engine.

3. **R8: Cross-Pipeline Correlation (P2)** — Deferred to: Release 2, Section "Included" item 3. Reason: requires accumulated cross-pipeline data and integrates with R5's alert infrastructure for predictive features.

## Dependencies

### External Dependencies

- SQLite (bundled with Python, no external dependency)
- Flask or FastAPI (dashboard server)
- Chart.js (dashboard visualizations, CDN or bundled)
- No cloud services required — everything runs locally

## Real-World Validation Requirements

These validation scenarios must use actual pipeline functionality in production-like conditions. No mocks or simulated tests.

1. **Telemetry emission validation**: Execute each of the 4 CLI pipelines (sprint, roadmap, tasklist, audit) on a real project. After each run, verify that the JSONL telemetry file in `~/.superclaude/telemetry/` contains correctly structured events with accurate timestamps, durations, and status codes. Compare event data against manual observation of the pipeline run.

2. **Overhead measurement**: Run the same pipeline on the same project with telemetry enabled and disabled. Measure wall-clock time for both. Verify telemetry overhead is <5% of pipeline runtime across all 4 pipeline types.

3. **Metrics aggregation accuracy**: After accumulating 5+ pipeline runs, execute `superclaude metrics show sprint --period 7d`. Manually calculate mean duration and token count from the raw JSONL data. Verify the CLI output matches manual calculations within rounding tolerance.

4. **Anomaly detection signal quality**: Run a pipeline with artificially inflated parameters (e.g., a sprint with an unusually high task count). Verify that R3's >2sigma anomaly detection flags this run. Verify that normal runs are not flagged.

5. **Dashboard rendering**: Launch the dashboard after 10+ pipeline runs. Verify: (a) pipeline health overview shows correct success rates, (b) trend charts render with real data points, (c) run detail view shows correct per-run information, (d) comparison view correctly overlays selected pipeline types.

6. **Historical import fidelity**: Import existing pipeline artifacts from a project with known execution history. Verify the backfilled metrics match the expected values from historical runs. Verify dashboard correctly displays historical trends alongside live data.

7. **Privacy verification**: Inspect all telemetry events across 10+ pipeline runs. Verify that no prompt content, LLM responses, or user-identifiable data appears in any event — only structural metadata.

## Success Criteria

- All four pipelines instrumented with telemetry (R1+R2)
- Telemetry overhead < 5% of pipeline runtime (R1)
- CLI metrics query returns accurate aggregations (R3)
- Anomaly detection correctly identifies >2sigma deviations (R3)
- Dashboard shows pipeline health trends with real data (R4)
- Historical import successfully backfills metrics database (R7)
- Forward-compatible schema includes alert threshold and feedback tables (R3)
- Dashboard includes alert placeholder panel (R4)

## Documentation Requirements

- Clearly distinguish R3's statistical anomaly detection (>2sigma heuristic) from the adaptive alerting engine coming in Release 2. R3 anomaly detection is a simple, non-configurable statistical flag. Release 2's alert engine will provide configurable, adaptive thresholds with user feedback loops.
- Document the metrics schema design with explicit notes on which tables/columns are reserved for Release 2 alert engine use.

## Traceability

| Release 1 Item | Original Spec Source | Status |
|----------------|---------------------|--------|
| Telemetry Collection SDK | Section 3, R1 | PRESERVED |
| Pipeline Instrumentation | Section 3, R2 | PRESERVED |
| Metrics Aggregation Engine | Section 3, R3 | PRESERVED + forward-compat constraint added |
| Dashboard UI | Section 3, R4 | PRESERVED + alert placeholder added |
| Historical Baseline Import | Section 3, R7 | PRESERVED |
| Schema forward-compatibility | New (supports R2) | VALID-ADDITION |
| Dashboard alert placeholder | New (supports R2) | VALID-ADDITION |
| Anomaly vs alerting documentation | New (user clarity) | VALID-ADDITION |
