# Split Proposal — v4.5 Observability & Adaptive Alerting System

## Discovery Analysis

### Spec Summary

The v4.5 release spec defines an observability system for SuperClaude CLI pipelines with 8 requirements across 3 priority tiers:

- **P0**: Telemetry Collection SDK (R1), Pipeline Instrumentation (R2), Metrics Aggregation Engine (R3)
- **P1**: Dashboard UI (R4), Adaptive Alert Engine (R5), Alert Rule Configuration (R6)
- **P2**: Historical Baseline Import (R7), Cross-Pipeline Correlation (R8)

Estimated scope: 1800-2400 lines production code. The spec itself identifies this as "inherently a two-phase problem" (Section 2, "The Unknown: Alert Thresholds").

### Dependency Chain Analysis

The dependency structure reveals a strict layered architecture:

```
Layer 0 (Foundation):  R1 Telemetry SDK → R2 Pipeline Instrumentation
Layer 1 (Processing):  R3 Metrics Aggregation Engine (depends on R1+R2 data)
Layer 2 (Consumption): R4 Dashboard (depends on R3)
                       R5 Adaptive Alerts (depends on R3 + accumulated data)
                       R6 Alert Configuration (depends on R5)
Layer 3 (Advanced):    R7 Historical Baseline Import (depends on R3 schema)
                       R8 Cross-Pipeline Correlation (depends on R3 + R5 data)
```

Critical observation: R5 (Adaptive Alerts) has a **data dependency** — it requires a "bootstrap period" of N runs (default 20) before it can activate. This is not just a code dependency but a temporal one. The alerting system literally cannot be tested meaningfully until enough telemetry has been collected to establish baselines.

### Discovery Questions

**1. What are the dependency chains? Which items are prerequisites for others?**

R1 → R2 → R3 form a strict prerequisite chain. R3 is the convergence point: everything above it depends on having aggregated metrics. R5 has the additional temporal dependency on accumulated data. R7 and R8 are additive features that build on a functioning metrics system.

**2. Are there components that deliver standalone value and can be validated through real-world use before the rest ships?**

Yes. R1 + R2 + R3 together form a complete, independently valuable system: structured telemetry collection, pipeline instrumentation, and queryable metrics with anomaly detection. The CLI query interface (`superclaude metrics show`) provides immediate value — operators can answer "what happened in my last sprint?" without grep-ing log files. The anomaly detection (>2sigma from rolling baseline) provides automated pattern detection.

R4 (Dashboard) also integrates naturally with R3 — it visualizes the same metrics R3 produces. Including it in a first release is viable.

**3. What is the cost of splitting?**

- Integration overhead: Moderate. R5/R6 depend on R3's metrics schema, so the schema must be designed with alerting in mind even in R1. This is manageable because R3 already defines the data model.
- Context switching: Low. The telemetry/metrics layer and the alerting layer are architecturally distinct.
- Release management: One additional release cycle.
- Potential rework: Low if R3's schema is designed extensibly. Higher if the dashboard in R1 creates UI patterns that conflict with alert visualization in R2.

**4. What is the cost of NOT splitting?**

- Delayed feedback: The alerting system cannot be validated until telemetry baselines exist. If shipped together, the alert engine ships untested-with-real-data and may need immediate revision.
- Big-bang risk: 1800-2400 lines in one release across backend, devops, and frontend domains.
- Harder root-cause isolation: If metrics queries are wrong, it's harder to debug when the alert engine is also reading from the same data.
- Missed learning: The spec explicitly states that threshold values are unknown. Shipping telemetry first and observing real patterns would inform better alert design.

**5. Is there a natural foundation vs. application boundary?**

Yes, and the spec itself identifies it. The architecture diagram shows four layers. Layers 0-1 (Telemetry SDK + Metrics Engine) are the **foundation**. Layer 2+ (Dashboard, Alerts, Correlation) are **applications** consuming that foundation. The spec's own rollout plan (Section 7) sequences them this way.

More specifically, there is a natural seam between "data collection and visibility" (R1-R4) and "intelligent automation" (R5-R8). The first group lets humans see what's happening. The second group lets the system act on what it sees.

**6. Could splitting INCREASE risk?**

Possible risks:
- R3's metrics schema might not anticipate R5's needs if R5 isn't designed concurrently. Mitigation: design R3's schema with R5's requirements documented as forward-looking constraints.
- Dashboard UI patterns in R1 might conflict with alert visualization needs in R2. Mitigation: reserve dashboard real-estate for alerts in R1, even if the section is empty.
- Users might rely on manual metric inspection in R1 and resist adopting automated alerts in R2. Mitigation: R1 release notes should frame metrics as "phase 1 of observability, with intelligent alerting coming in phase 2."

None of these risks are severe. The seam is natural and well-supported by the spec's own architecture.

### Recommendation: SPLIT

**Confidence: 0.88**

The evidence strongly supports splitting this release. The spec itself identifies the chicken-and-egg problem: adaptive alerting requires historical data that doesn't exist yet. This is the textbook case for a foundation-then-application split.

#### Release 1 Scope: Telemetry Foundation + Metrics Visibility

- R1: Telemetry Collection SDK (P0)
- R2: Pipeline Instrumentation (P0)
- R3: Metrics Aggregation Engine (P0)
- R4: Dashboard UI (P1) — included because it consumes R3 directly and provides immediate operator value
- R7: Historical Baseline Import (P2) — included because it accelerates the bootstrap period for R2's alert engine, and it depends only on R3's schema, not on alerting

**Objective**: Give operators full visibility into pipeline behavior. Start collecting the telemetry data that R2's alert engine needs for baseline learning.

**What's testable in real-world use**:
1. Run each of the 4 pipelines with telemetry enabled. Verify JSONL events are emitted correctly.
2. Run `superclaude metrics show sprint --period 7d` after several sprint runs. Verify aggregated metrics match manual calculation.
3. Trigger a known anomaly (e.g., artificially inflate turn count). Verify the >2sigma anomaly detection flags it.
4. Open the dashboard and verify trend charts render correctly with real pipeline data.
5. Import historical pipeline artifacts via R7. Verify the metrics DB is backfilled and dashboard shows historical trends.

#### Release 2 Scope: Adaptive Alerting + Intelligence

- R5: Adaptive Alert Engine (P1)
- R6: Alert Rule Configuration (P1)
- R8: Cross-Pipeline Correlation (P2)

**Objective**: Build intelligent alerting on top of the data foundation established in R1. Use real baseline data (collected during R1's operational period) to set meaningful thresholds.

**What depends on Release 1**:
- R5 depends on R3's metrics DB and needs N runs of collected data
- R6 depends on R5's alert engine
- R8 depends on R3's cross-pipeline data and R5's alert infrastructure

#### The Seam

The split falls at the boundary between **observation** (collecting and displaying data) and **automation** (acting on patterns in data). This is a natural architectural boundary already reflected in the spec's component stack and rollout plan.

Release 1 answers: "What is happening in my pipelines?"
Release 2 answers: "What should I do about what's happening?"

The temporal data dependency makes this more than a convenience split — it is architecturally necessary. R5's bootstrap period means the alert engine cannot be meaningfully validated without R1 having run in production for a period.

#### Risks of the Split

1. **Schema forward-compatibility**: R3's metrics schema must accommodate R5's future needs. Mitigation: Document R5's data requirements as constraints in R1's schema design.
2. **Dashboard integration surface**: R4 in R1 must leave room for alert visualization in R2. Mitigation: Design dashboard with extensible panel system.
3. **User adoption gap**: Users who adopt R1 may not upgrade to R2. Mitigation: R1 metrics output should include "suggested alert candidates" messaging to build anticipation.

#### Justification: Not "Easiest Work First"

R1 is not merely the easiest subset. It includes R3 (Metrics Aggregation Engine) which involves time-series aggregation, anomaly detection algorithms, SQLite schema design, and a CLI query interface — substantial engineering. It also includes R7 (Historical Baseline Import) which requires parsing multiple artifact formats. R1 delivers a complete, independently valuable product: full pipeline observability with queryable metrics and visual dashboards.

R1 also actively enables R2's success by collecting the baseline data that makes adaptive thresholds meaningful rather than arbitrary.
