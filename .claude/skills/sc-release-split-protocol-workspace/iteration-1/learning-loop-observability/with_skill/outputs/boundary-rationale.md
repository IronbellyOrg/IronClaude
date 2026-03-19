# Split Boundary Rationale

## Split Point

The boundary falls between **data collection and visibility** (R1, R2, R3, R4, R7) and **intelligent automation** (R5, R6, R8). Release 1 answers "What is happening in my pipelines?" Release 2 answers "What should I do about what's happening?"

In terms of the spec's architecture diagram, the split falls between the Telemetry Storage + Metrics Engine layers and the Alert Engine layer.

## Why This Boundary

Four independent lines of evidence converge on this split point:

1. **Temporal data dependency**: R5 (Adaptive Alert Engine) specifies a bootstrap period requiring N accumulated pipeline runs (default 20) before alerts can activate. This creates an irreducible temporal dependency — the alert engine cannot be meaningfully validated without baseline data that only exists after R1 has been running in production. This is not a workaround but a fundamental property of adaptive threshold systems.

2. **Architectural layering**: The spec's own component stack shows a strict bottom-up dependency: Telemetry SDK -> Telemetry Storage -> Metrics Engine -> Alert Engine/Dashboard. All dependency arrows point upward. R5 depends on R3; R3 does not depend on R5. There are zero circular dependencies across the proposed boundary.

3. **Priority alignment**: R1-R3 are all P0 (critical path). R5-R6 are P1 (important but second tier). R7 is P2 but placed in R1 because it depends only on R3's schema and strategically accelerates R2's bootstrap. R8 is P2 and placed in R2 because it requires both accumulated data and alert infrastructure.

4. **Spec self-identification**: Section 2 ("The Unknown: Alert Thresholds") explicitly states: "This is inherently a two-phase problem — you can't build intelligent alerting without historical data to learn from." The spec's own rollout plan (Section 7) sequences telemetry before alerting.

## Release 1 Delivers

- **Complete pipeline observability**: Structured telemetry replaces manual log inspection for all 4 pipelines
- **Queryable metrics**: CLI interface for pipeline health queries (`superclaude metrics show`)
- **Automated anomaly detection**: Statistical (>2sigma) flagging of unusual pipeline behavior
- **Visual dashboard**: Web UI for pipeline health trends, run details, and comparisons
- **Historical baselines**: Import of existing pipeline artifacts to bootstrap the metrics database
- **Data foundation**: Accumulated telemetry that directly enables R2's adaptive alerting

Release 1 is independently valuable — it solves the problem statement's core issue ("no centralized observability") without requiring R2.

## Release 2 Builds On

- **Adaptive alerting**: Uses baselines established by R1 production data to set meaningful, non-arbitrary thresholds
- **Configurable alert policies**: Builds on the alert engine to give users control over sensitivity
- **Cross-pipeline intelligence**: Uses accumulated cross-pipeline data to detect correlations and enable predictions
- **Dashboard extensions**: Adds alert visualization and correlation matrix to R1's dashboard

Release 2 is enhanced by R1's operational period — every day of R1 production usage provides data that makes R2's alerting more accurate.

## Cross-Release Dependencies

| Release 2 Item | Depends On (Release 1) | Type | Risk if R1 Changes |
|----------------|----------------------|------|---------------------|
| R5: Alert threshold learning | R3: Metrics DB schema + accumulated data | Hard | Schema change requires R5 query updates; data format change requires reprocessing |
| R5: Alert feedback storage | R3: Metrics DB alert/feedback tables | Hard | Table schema change requires R5 storage logic updates |
| R5: Bootstrap period | R1+R2: Accumulated telemetry events | Hard | If telemetry format changes, R5 may need recalibration |
| R6: Alert configuration | R5: Alert engine API | Hard | R6 configures R5; any R5 API change affects R6 |
| R8: Correlation analysis | R3: Metrics DB cross-pipeline data | Hard | Requires sufficient data across multiple pipeline types |
| R8: Dashboard visualization | R4: Dashboard framework | Soft | R8 adds panels to R4's UI; framework changes require panel updates |
| R5: Alert display | R4: Dashboard alert placeholder | Soft | R4 reserves UI space; R5 populates it |

## Integration Points

1. **Metrics DB schema**: R3 defines the SQLite schema. R5 reads from metrics tables and writes to alert threshold/feedback tables. The schema is the primary integration contract. R1 must ship with forward-compatible tables for R5.

2. **Dashboard UI framework**: R4 establishes the dashboard architecture (Flask/FastAPI + Chart.js). R5 adds alert panels and R8 adds correlation visualization. R1's dashboard must use an extensible panel/tab system.

3. **Anomaly detection interface**: R3 includes >2sigma anomaly detection. R5 includes adaptive threshold alerting. These are distinct systems but may surface conflicting signals to users. R1 documentation must clearly distinguish the two.

4. **Telemetry event format**: R1+R2 define the JSONL event schema. R5 reads these events. The schema is frozen after R1 ships (additive-only changes permitted).

## Handoff Criteria

Before Release 2 planning begins, Release 1 must demonstrate:

1. All 4 pipelines emitting structured telemetry confirmed in production use
2. Metrics DB contains at least 20 pipeline runs across at least 2 pipeline types
3. Anomaly detection producing useful signals (verified by human review)
4. Dashboard rendering real data correctly
5. Telemetry overhead confirmed <5%
6. Schema forward-compatibility tables exist and are structurally sound
7. Engineering review of observed data distributions to calibrate R5's default bootstrap period

## Reversal Cost

**Low**. If the split decision needs to be reversed:

- R5+R6+R8 code is additive — it does not modify R1 components, only extends them
- Merging back to a single release means adding R5+R6+R8 code to the R1 codebase
- No architectural changes needed because dependency arrows flow one direction only
- The primary cost is coordination: merging two sets of code reviews, test suites, and documentation
- Estimated reversal effort: 1-2 days of integration work

The split is designed to be low-commitment. If R1 production data reveals that the two-phase approach is unnecessary (e.g., synthetic baselines prove sufficient), R2 can be merged back without penalty.
