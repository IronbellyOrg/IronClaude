---
release: 2
parent-spec: .claude/skills/sc-release-split-protocol-workspace/evals/files/spec-learning-loop-observability.md
split-proposal: split-proposal-final.md
scope: "Adaptive alert engine, alert configuration, cross-pipeline correlation"
status: draft
validation-gate: "blocked until R1 real-world validation passes"
---

# Release 2 — Adaptive Alerting & Cross-Pipeline Intelligence

## Objective

Build an intelligent alerting system on top of the telemetry foundation established in Release 1. Using real baseline data collected during Release 1's operational period, design adaptive alert thresholds that learn from observed pipeline behavior rather than relying on arbitrary static values. Add cross-pipeline correlation to detect relationships between different pipeline outcomes and enable predictive capabilities.

## Scope

### Included

1. **R5: Adaptive Alert Engine (P1)** — From: original-spec Section 3, R5
   - Bootstrap period: collect N runs (configurable, default 20) before activating alerts
   - Threshold learning: compute per-pipeline, per-metric alert thresholds from historical distribution
   - Alert types: anomaly (deviation from baseline), trend (sustained drift), failure_pattern (repeating errors)
   - Alert channels: CLI notification on next run, optional webhook for external integration
   - Threshold adaptation: recalculate thresholds weekly from rolling window
   - User feedback: `superclaude alert ack <id>` to mark false positives, which adjusts future thresholds
   - Alert fatigue prevention: suppress repeated alerts for same pattern, aggregate similar alerts
   - **Design informed by R1 data**: Alert threshold initial values and bootstrap configuration should be calibrated using real baseline data collected during Release 1's operational period

2. **R6: Alert Rule Configuration (P1)** — From: original-spec Section 3, R6
   - YAML configuration file: `~/.superclaude/alerts.yaml`
   - Override learned thresholds per metric
   - Silence rules: suppress specific alert types or pipelines
   - Escalation: different channels for warning vs. critical
   - Preset profiles: `conservative` (fewer alerts), `aggressive` (catch everything), `adaptive` (default)

3. **R8: Cross-Pipeline Correlation (P2)** — From: original-spec Section 3, R8
   - Spec complexity to sprint duration correlation
   - Roadmap gate rejection to subsequent sprint failure correlation
   - Audit finding density to code change volume correlation
   - Predictive: estimate pipeline outcomes before running based on input characteristics
   - Visualization: correlation matrix in dashboard

### Excluded (delivered in Release 1)

1. **R1: Telemetry Collection SDK** — Delivered in: Release 1. Foundation for all R2 features.
2. **R2: Pipeline Instrumentation** — Delivered in: Release 1. Provides the telemetry events R5 consumes.
3. **R3: Metrics Aggregation Engine** — Delivered in: Release 1. Provides the metrics DB that R5 queries for thresholds and R8 uses for correlation analysis.
4. **R4: Dashboard UI** — Delivered in: Release 1. R2 extends it with alert visualizations and correlation matrix.
5. **R7: Historical Baseline Import** — Delivered in: Release 1. May have already provided sufficient historical data to shorten R5's bootstrap period.

## Dependencies

### Prerequisites (from Release 1)

| Dependency | Required For | Type | Validation |
|-----------|-------------|------|-----------|
| Telemetry SDK operational (R1) | R5 reads telemetry events | Hard | Telemetry JSONL files being written for all 4 pipelines |
| Pipeline instrumentation active (R2) | R5 needs structured events | Hard | All 4 pipelines emitting telemetry |
| Metrics DB populated (R3) | R5 queries baselines, R8 queries correlations | Hard | SQLite DB contains aggregated metrics from real runs |
| Metrics schema with alert tables (R3) | R5 stores thresholds and feedback | Hard | Alert threshold and feedback tables exist in schema |
| Dashboard running (R4) | R8 adds correlation visualization | Soft | Dashboard functional; R8 adds panels |
| Historical data imported (R7) | R5 bootstrap acceleration | Soft | If available, shortens bootstrap period |

### External Dependencies

- No additional external dependencies beyond Release 1's stack
- R5 webhook integration requires user-provided endpoint (optional feature)

## Real-World Validation Requirements

These validation scenarios must use actual pipeline functionality. No mocks or simulated tests.

1. **Bootstrap period validation**: Start with a fresh alert engine against a metrics DB that has accumulated N+ runs from Release 1 production usage. Verify that the bootstrap period completes and thresholds are computed from real data. Verify the computed thresholds are reasonable (not absurdly wide or narrow) by comparing against manual inspection of the metrics distribution.

2. **Anomaly alert accuracy**: After bootstrap, run pipelines that produce known anomalies (e.g., a sprint with unusually high token count due to a complex spec). Verify the alert engine fires for genuine anomalies. Run 10+ normal pipelines and verify no false alerts fire. Target: <10% false positive rate as specified in original success criteria.

3. **Trend alert detection**: Over a series of 10+ pipeline runs, gradually increase a metric (e.g., average phase duration). Verify the trend alert fires when sustained drift is detected. Verify it does not fire for random variation.

4. **Failure pattern detection**: Trigger the same pipeline failure 3 times (matching the Section 2 incident pattern: "Roadmap gate rejected 3 consecutive runs with the same validation error"). Verify the failure_pattern alert fires after the 2nd or 3rd occurrence.

5. **User feedback loop**: Acknowledge a false positive alert via `superclaude alert ack <id>`. Run subsequent pipelines with similar characteristics. Verify the threshold has adjusted and the same pattern no longer triggers an alert.

6. **Alert configuration**: Create a custom alerts.yaml with specific overrides (e.g., silence sprint alerts, set aggressive threshold for roadmap gate rejections). Verify the configuration is respected.

7. **Cross-pipeline correlation**: Run a series of sprints with varying spec complexity. Verify the correlation engine detects the spec_complexity-to-sprint_duration relationship. Verify the dashboard displays the correlation matrix correctly.

8. **Incident reproduction**: Reproduce the three incidents from original-spec Section 2:
   - Sprint phases hitting max_turns with correlated task counts — verify detection
   - Roadmap gate rejecting 3 consecutive runs — verify pattern alert
   - Audit pipeline producing 40% fewer findings than baseline — verify anomaly alert

## Success Criteria

- Alert engine achieves < 10% false positive rate after bootstrap period (from original-spec Section 8)
- Anomaly detection catches the three incident patterns from original-spec Section 2 (from original-spec Section 8)
- Users can tune alert sensitivity without code changes (from original-spec Section 8)
- Cross-pipeline correlation identifies statistically significant relationships
- Dashboard displays alert status and correlation matrix
- User feedback mechanism measurably adjusts thresholds

## Planning Gate

> **This release's roadmap and tasklist generation may proceed only after Release 1 has passed real-world validation and the results have been reviewed.**
>
> **Validation criteria from Release 1**:
> - All 4 pipelines confirmed emitting structured telemetry in production use
> - Metrics aggregation producing accurate rollups verified against manual calculation
> - Anomaly detection (>2sigma) producing useful signals (not drowning in noise or missing obvious anomalies)
> - Dashboard rendering real pipeline data correctly
> - Telemetry overhead confirmed <5% of pipeline runtime
> - Metrics DB has accumulated sufficient data for meaningful baseline computation (minimum 20 pipeline runs across at least 2 pipeline types)
>
> **Review process**: Engineering lead reviews Release 1 validation results. Key review questions:
> - Does the metrics schema adequately support alert threshold storage?
> - Are the collected metrics granular enough for R5's threshold learning?
> - Did R3's anomaly detection produce signals that align with what R5 should alert on?
> - Based on observed data distributions, what should R5's default bootstrap period be?
>
> **If validation fails**:
> - If telemetry or metrics issues: fix in Release 1 patch before proceeding
> - If schema inadequacy: revise R3 schema in Release 1 patch, re-validate
> - If insufficient data accumulated: extend Release 1 operational period before proceeding
> - If fundamental design flaw discovered: re-evaluate whether the split should be merged back into a single release

## Traceability

| Release 2 Item | Original Spec Source | Status |
|----------------|---------------------|--------|
| Adaptive Alert Engine | Section 3, R5 | PRESERVED + informed-by-R1-data addition |
| Alert Rule Configuration | Section 3, R6 | PRESERVED |
| Cross-Pipeline Correlation | Section 3, R8 | PRESERVED |
| R1 data-informed design | New (split-enabled improvement) | VALID-ADDITION |
| Planning gate | New (protocol requirement) | VALID-ADDITION |
