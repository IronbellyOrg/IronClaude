# Risk Assessment: Split vs. Monolithic Delivery

## Option A: Ship Everything at Once (Monolithic)

### Risks

1. **Blind threshold configuration (HIGH)**
   Without real telemetry data, alert thresholds must be guessed. The spec itself acknowledges this: "Setting static thresholds now would produce either too many false alerts (users ignore them) or too few (defeats the purpose)." Shipping adaptive alerting with no data to adapt to is shipping a non-functional feature.

2. **Delayed value delivery (MEDIUM)**
   The telemetry SDK and basic metrics are independently valuable. Holding them back while building alerting delays the time when operators can stop manually grepping logs. The three incidents in Section 2 could start being caught by basic anomaly detection (>2 sigma) as soon as enough data exists.

3. **Large blast radius (MEDIUM)**
   ~2000 lines of production code touching all four pipeline executors, plus a new web server, plus a new SQLite schema, plus a new alerting system. A bug in any component blocks the entire release.

4. **Wasted alert engine effort (MEDIUM)**
   If real telemetry reveals unexpected data patterns (e.g., bimodal distributions, heavy tails), the alert engine design may need revision. Building it before seeing real data risks rework.

### Benefits

- Single release to communicate
- Integrated testing possible from day one
- No intermediate state to maintain

## Option B: Two-Phase Split (Recommended)

### Phase 1: Telemetry + Metrics + Dashboard (R1, R2, R3, R4, R7)

**Risks:**
- Users get metrics but no alerting -- they must check dashboard manually (LOW, still better than grepping logs)
- Dashboard may need revision after seeing real data shapes (LOW, expected iteration)
- Historical import (R7) quality depends on artifact format consistency (LOW)

**Benefits:**
- Delivers immediate value: structured observability replaces log grepping
- Starts the data collection clock -- every day of real telemetry makes Phase 2 better
- Smaller, more testable release (~1200-1500 lines)
- Dashboard provides visual validation that telemetry is working correctly
- Historical import (R7) can bootstrap baselines, shortening the Phase 2 wait

### Phase 2: Adaptive Alerting + Cross-Pipeline Correlation (R5, R6, R8)

**Risks:**
- Alert thresholds may still need tuning after initial deployment (LOW, this is expected and the feedback loop handles it)
- Phase 2 timeline depends on Phase 1 adoption -- if nobody uses the pipelines, no data accumulates (MEDIUM)

**Benefits:**
- Thresholds informed by real data, not guesses
- Can validate anomaly detection against the three known incidents by replaying historical data
- Smaller, focused release (~600-900 lines)
- User feedback loop (alert ack) has data to compare against from day one

## Risk Comparison Matrix

| Risk Factor | Monolithic | Two-Phase |
|-------------|-----------|-----------|
| Alert accuracy | HIGH (guessed thresholds) | LOW (data-informed) |
| Time to first value | LATE (entire system must ship) | EARLY (telemetry + dashboard first) |
| Blast radius | LARGE (all components) | SMALL (per phase) |
| Rework probability | HIGH (alert engine before data) | LOW (alert engine after data) |
| Integration complexity | MEDIUM (all at once) | LOW (additive phases) |
| Communication overhead | LOW (one release) | MEDIUM (two releases) |
