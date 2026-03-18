# Release Split Recommendation: Observability & Adaptive Alerting System

## Verdict: SPLIT into two phases

The spec should be split into two releases with a deliberate data-collection interval between them. This is not merely a preference for smaller releases -- it is driven by a fundamental data dependency that makes monolithic delivery counterproductive.

---

## Rationale

### The core argument: you cannot adaptively alert on data that does not exist

The spec's own Section 2 ("The Unknown: Alert Thresholds") states the problem clearly: we do not know what normal looks like for our pipelines. The adaptive alert engine (R5) requires a bootstrap period of at least 20 runs per pipeline. The cross-pipeline correlation engine (R8) requires volume across multiple pipeline types. These are not code dependencies -- they are data dependencies with an irreducible time component.

Shipping telemetry collection and adaptive alerting simultaneously means the alerting system will sit dormant for its bootstrap period anyway. Users receive a feature they cannot use until enough data accumulates. Worse, without real data to inform the design, the alert engine's statistical assumptions (e.g., that metrics follow a normal distribution suitable for sigma-based detection) remain untested.

### Value flows earlier with a split

Phase 1 gives operators structured observability immediately. The three incidents described in Section 2 all involve patterns that are visible in raw metrics and dashboards -- a human looking at a trend chart would catch repeated gate rejections or anomalous finding counts. Full adaptive alerting makes this automatic, but manual dashboard review is already a massive improvement over grepping stdout logs.

### The split aligns with the spec's own rollout plan

Section 7 (Rollout Plan) already sequences the work as: (1) telemetry, (2) metrics, (3) dashboard, (4) alert engine after sufficient telemetry, (5) cross-pipeline correlation after sufficient data. The spec's authors recognized this natural ordering. The recommendation here is simply to formalize it as two distinct releases rather than one release with a phased rollout.

---

## Proposed Split

### Phase 1: v4.5.0 -- Observability Foundation

**Requirements included:** R1, R2, R3, R4, R7

**Scope:**
- Telemetry SDK with structured event schema (R1)
- Instrumentation of all four pipeline executors (R2)
- Metrics aggregation engine with SQLite storage, CLI query interface, and basic anomaly flagging at >2 sigma (R3)
- Dashboard UI for pipeline health visualization (R4)
- Historical baseline import from existing pipeline artifacts (R7)

**Estimated size:** 1200-1500 lines of production code

**Deliverables:**
- `superclaude metrics show [pipeline] [--period 7d]` CLI command
- `superclaude dashboard` web UI
- Telemetry auto-collection on all pipeline runs
- Historical data import for baseline bootstrapping

**Exit criteria:**
- All four pipelines emit structured telemetry
- Telemetry overhead < 5% of pipeline runtime
- Metrics DB computes rolling baselines
- Dashboard renders pipeline health trends
- Historical import backfills at least 2 weeks of prior pipeline data

**What Phase 1 deliberately excludes:** Adaptive alerting, alert configuration, cross-pipeline correlation. These are deferred to Phase 2.

### Data Collection Interval

Between Phase 1 and Phase 2, real pipeline usage generates telemetry. The minimum bootstrap period is 20 runs per pipeline type (configurable in R5). With typical usage patterns, this likely requires 2-4 weeks.

During this interval:
- The team monitors the dashboard to understand real data distributions
- Anomaly detection (>2 sigma) in R3 provides early signal without formal alerting
- Historical import (R7) may partially satisfy the bootstrap requirement

### Phase 2: v4.6.0 -- Adaptive Alerting & Correlation

**Requirements included:** R5, R6, R8

**Scope:**
- Adaptive alert engine with threshold learning from accumulated baselines (R5)
- Alert rule configuration via YAML with preset profiles (R6)
- Cross-pipeline correlation analysis and predictive estimation (R8)

**Estimated size:** 600-900 lines of production code

**Deliverables:**
- Alert engine with anomaly, trend, and failure_pattern detection
- `superclaude alert ack <id>` feedback mechanism
- `~/.superclaude/alerts.yaml` configuration
- Correlation matrix in dashboard
- Predictive pipeline outcome estimation

**Entry criteria (from Phase 1):**
- Metrics DB contains >= 20 runs per pipeline type OR historical import has backfilled equivalent data
- Baseline statistics (mean, stddev, percentiles) are computed and stable
- Dashboard confirms data distributions match statistical assumptions

**Exit criteria:**
- Alert engine achieves < 10% false positive rate after bootstrap
- Anomaly detection catches the three incident patterns from spec Section 2
- Users can tune alert sensitivity via alerts.yaml without code changes
- Cross-pipeline correlations surface at least one actionable insight

---

## What stays together and why

**R1 + R2 are inseparable.** The SDK (R1) without instrumentation (R2) emits nothing. Instrumentation without the SDK has nothing to call. These must ship together.

**R3 ships with R1+R2.** Raw telemetry without aggregation forces users to parse JSONL files manually. The metrics engine transforms raw events into queryable, meaningful data. Including it in Phase 1 provides immediate analytical value.

**R4 ships with R3.** The dashboard is the primary user interface for the metrics engine. Without it, users must use the CLI query interface exclusively. The dashboard makes the value of telemetry collection tangible and visible, which drives adoption (and therefore data generation for Phase 2).

**R7 ships with Phase 1.** Historical import accelerates the bootstrap period for Phase 2. The earlier it runs, the sooner baselines stabilize. It also provides immediate dashboard content rather than showing empty charts.

**R5 + R6 are inseparable.** The alert engine (R5) without configuration (R6) has no way for users to tune sensitivity. Configuration without the engine configures nothing.

**R8 ships with R5+R6.** Cross-pipeline correlation is a natural extension of the alert engine -- both require accumulated multi-pipeline data and both enhance the analytical layer.

---

## Risks of this split

1. **Phase 2 delay risk (MEDIUM):** If Phase 1 adoption is slow, the bootstrap period extends. Mitigation: R7 (historical import) partially satisfies bootstrap requirements from existing artifacts.

2. **Dashboard rework (LOW):** Phase 2 adds correlation visualizations to the dashboard. The Phase 1 dashboard architecture must accommodate extension. Mitigation: use a modular dashboard design with pluggable chart components.

3. **Schema evolution (LOW):** Phase 2 may need telemetry fields not anticipated in Phase 1's schema. Mitigation: the JSONL event schema includes a `metadata` map for extensibility, and the metrics DB schema should include a schema version.

---

## Summary

| Aspect | Phase 1 (v4.5.0) | Phase 2 (v4.6.0) |
|--------|------------------|------------------|
| Requirements | R1, R2, R3, R4, R7 | R5, R6, R8 |
| Focus | Collect, aggregate, visualize | Alert, adapt, correlate |
| Est. size | 1200-1500 lines | 600-900 lines |
| Data needed | None (starts collection) | 20+ runs per pipeline |
| Key deliverable | Dashboard + CLI metrics | Adaptive alerting |
| Independent value | Yes -- replaces log grepping | Yes -- automates anomaly detection |
