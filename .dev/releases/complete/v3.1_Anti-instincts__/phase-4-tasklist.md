# Phase 4 -- Shadow Validation & Graduation

Run shadow mode across real sprint executions to calibrate thresholds and validate accuracy before enabling enforcement. Requires 5+ sprint runs with `gate_rollout_mode=shadow` and `ShadowGateMetrics.pass_rate >= 0.90` before graduation to `soft` mode. Milestone M4: graduation decision documented with calibration evidence.

---

### T04.01 -- Activate Shadow Mode in Test Sprint Configurations

| Field | Value |
|---|---|
| Roadmap Item IDs | R-017 |
| Why | Shadow mode activation across real sprints generates the metrics data needed to calibrate thresholds and validate accuracy before enforcement. |
| Effort | S |
| Risk | Low |
| Risk Drivers | cross-cutting (affects all sprint runs) |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0026, D-0027 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0026/notes.md`
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0027/evidence.md`

**Deliverables:**
1. Shadow mode configuration: `gate_rollout_mode=shadow` set in test sprint configurations
2. `ShadowGateMetrics` data collected from 5+ real sprint runs with all data points recorded

**Steps:**
1. **[PLANNING]** Identify test sprint configuration files and current `gate_rollout_mode` settings
2. **[PLANNING]** Plan 5+ sprint run schedule ensuring diverse roadmap inputs
3. **[EXECUTION]** Set `gate_rollout_mode=shadow` in test sprint configurations
4. **[EXECUTION]** Execute 5+ sprint runs with anti-instinct gate in shadow mode, recording all `ShadowGateMetrics` data points
5. **[EXECUTION]** Collect and aggregate metrics: pass/fail counts, evaluation_ms values, per-module results
6. **[VERIFICATION]** Verify `ShadowGateMetrics` data points exist for all 5+ runs
7. **[COMPLETION]** Record configuration and metrics collection evidence to D-0026/notes.md and D-0027/evidence.md

**Acceptance Criteria:**
- Test sprint configurations have `gate_rollout_mode=shadow` set
- `ShadowGateMetrics` contains data from >= 5 sprint runs
- Each data point records: passed (bool), evaluation_ms (float), and per-module breakdown
- Shadow mode causes no behavioral change to sprint task execution (gate evaluates but result is ignored per `shadow` mode semantics)

**Validation:**
- Manual check: `ShadowGateMetrics` data file contains >= 5 run entries with complete fields
- Evidence: metrics data summary archived to D-0027/evidence.md

**Dependencies:** T03.02, T03.03 (sprint integration must be complete and tested)
**Rollback:** Revert `gate_rollout_mode` to `"off"` in configurations

---

### T04.02 -- Calibrate Fingerprint and Structural Audit Thresholds

| Field | Value |
|---|---|
| Roadmap Item IDs | R-018 |
| Why | Shadow-mode metrics reveal whether the default thresholds (fingerprint 0.7, structural audit 0.5) produce acceptable false positive/negative rates on real sprint data. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | data-driven (threshold calibration), performance (false positive/negative rates) |
| Tier | STANDARD |
| Confidence | [███████░░░] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0028, D-0029, D-0030 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0028/notes.md`
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0029/notes.md`
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0030/spec.md`

**Deliverables:**
1. Fingerprint coverage threshold (0.7) analysis: pass/fail distribution, false positive rate, false negative rate against shadow data (NFR-011)
2. Structural audit threshold (0.5) analysis: pass/fail distribution, false positive rate, false negative rate against shadow data (NFR-011)
3. Calibration results document: current thresholds, observed rates, recommended adjustments (if any), threshold rationale

**Steps:**
1. **[PLANNING]** Load `ShadowGateMetrics` data from T04.01; identify per-module breakdowns
2. **[PLANNING]** Define false positive/negative criteria for each module
3. **[EXECUTION]** Analyze fingerprint coverage threshold (0.7) against real shadow data: compute pass rate, false positive rate, false negative rate
4. **[EXECUTION]** Analyze structural audit threshold (0.5) against real shadow data: compute pass rate, false positive rate, false negative rate
5. **[EXECUTION]** Write calibration results document with current thresholds, observed rates, and adjustment recommendations
6. **[VERIFICATION]** Verify analysis covers all shadow data points; check calculations for consistency
7. **[COMPLETION]** Record analyses to D-0028, D-0029 notes.md and calibration document to D-0030/spec.md

**Acceptance Criteria:**
- Fingerprint threshold analysis covers all shadow data points with computed false positive/negative rates
- Structural audit threshold analysis covers all shadow data points with computed false positive/negative rates
- Calibration document explicitly states whether thresholds should be adjusted and provides rationale
- If thresholds are adjusted, new values are applied to module code and verified with regression tests

**Validation:**
- Manual check: calibration document contains quantitative analysis with specific rates and threshold recommendations
- Evidence: calibration results document at D-0030/spec.md

**Dependencies:** T04.01 (shadow metrics data must be collected)
**Rollback:** Revert threshold values to defaults (0.7 fingerprint, 0.5 structural audit)

---

### T04.03 -- Resolve Open Questions OQ-002, OQ-007, OQ-008

| Field | Value |
|---|---|
| Roadmap Item IDs | R-019 |
| Why | These open questions affect detection accuracy and TurnLedger integration correctness; resolution is required before enforcement graduation. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0031, D-0032 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0031/notes.md`
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0032/notes.md`

**Deliverables:**
1. OQ-002 resolution: validation of 60-char context window against diverse roadmaps from shadow runs; adjustment recommendation if needed
2. OQ-007 and OQ-008 resolution: TurnLedger design.md reconciliation verification and multi-component false negative assessment with context extraction expansion plan if needed

**Steps:**
1. **[PLANNING]** Review shadow data for context window adequacy (OQ-002) and multi-component detection (OQ-008)
2. **[PLANNING]** Check TurnLedger design.md for finalized sections (OQ-007)
3. **[EXECUTION]** Validate 60-char context window against diverse roadmaps from shadow runs; document findings for OQ-002
4. **[EXECUTION]** Assess multi-component false negatives from shadow data; document findings for OQ-008
5. **[EXECUTION]** Verify TurnLedger design.md sections are finalized; reconcile any gaps for OQ-007
6. **[COMPLETION]** Record resolutions to D-0031/notes.md and D-0032/notes.md

**Acceptance Criteria:**
- OQ-002 resolution documents whether 60-char window is adequate or needs adjustment, with evidence from shadow runs
- OQ-008 resolution documents multi-component false negative rate and whether context extraction expansion is needed
- OQ-007 resolution confirms TurnLedger design.md sections are finalized or identifies remaining gaps
- All three OQ resolutions are documented with evidence references

**Validation:**
- Manual check: each OQ resolution references specific shadow data evidence
- Evidence: resolution documents at D-0031/notes.md and D-0032/notes.md

**Dependencies:** T04.01 (shadow data required for OQ-002 and OQ-008)
**Rollback:** N/A (read-only analysis)

---

### T04.04 -- Document Graduation Decision and Rollout Plan

| Field | Value |
|---|---|
| Roadmap Item IDs | R-020 |
| Why | The graduation decision formally authorizes rollout advancement based on shadow metrics, completing the enforcement readiness checkpoint (Checkpoint C). |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0033, D-0034 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0033/spec.md`
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0034/spec.md`

**Deliverables:**
1. Graduation decision document: `ShadowGateMetrics.pass_rate` evidence (>= 0.90 over 5+ sprints required), false-positive review results, false-negative documentation with vocabulary/pattern expansion plan, enforcement-related OQ closure status
2. Rollout promotion plan: off -> shadow (after Checkpoint B) -> soft (after SC-008 satisfied) -> full (after stable soft evidence); includes specific criteria for each transition

**Steps:**
1. **[PLANNING]** Aggregate all shadow metrics, threshold calibration results, and OQ resolutions from T04.01-T04.03
2. **[PLANNING]** Evaluate all four graduation criteria from roadmap section 4.4
3. **[EXECUTION]** Write graduation decision document with pass_rate evidence, false-positive review, false-negative plan, OQ closure status
4. **[EXECUTION]** Write rollout promotion plan with specific criteria for each mode transition (off->shadow->soft->full)
5. **[COMPLETION]** Record decision and plan to D-0033/spec.md and D-0034/spec.md

**Acceptance Criteria:**
- Graduation document contains `ShadowGateMetrics.pass_rate` value with evidence of >= 0.90 over 5+ sprints (or explicit documentation of why criteria not yet met)
- False-positive review results documented with specific examples reviewed
- All false negatives documented with vocabulary/pattern expansion plan
- Rollout plan specifies concrete criteria for each transition with no ambiguous conditions

**Validation:**
- Manual check: graduation document addresses all 4 criteria from roadmap section 4.4
- Evidence: graduation decision at D-0033/spec.md and rollout plan at D-0034/spec.md

**Dependencies:** T04.01, T04.02, T04.03
**Rollback:** N/A (documentation only)

---

### Checkpoint: End of Phase 4

**Purpose:** Validate enforcement readiness (Checkpoint C): shadow pass rate meets threshold, false positives reviewed, enforcement-related OQs closed, graduation decision documented.
**Checkpoint Report Path:** `.dev/releases/current/v3.1_Anti-instincts__/checkpoints/CP-P04-END.md`
**Verification:**
- `ShadowGateMetrics.pass_rate >= 0.90` over 5+ sprints (SC-008)
- False-positive rate is operationally acceptable per calibration document
- All enforcement-related open questions (OQ-002, OQ-007, OQ-008) resolved with documented evidence
**Exit Criteria:**
- All 4 tasks (T04.01-T04.04) completed with deliverables D-0026 through D-0034 produced
- Graduation decision document recommends specific rollout mode advancement
- Rollout promotion plan approved and ready for execution
