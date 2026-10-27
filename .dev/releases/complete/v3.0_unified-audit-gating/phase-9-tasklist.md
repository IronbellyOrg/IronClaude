# Phase 9 -- Activation and Hardening

Progress from soft to full enforcement based on measured operational evidence. This phase achieves milestone M6b: enforcement level advanced only on measured evidence. Activation proceeds only if Phase 8 readiness criteria are met.

### T09.01 -- Activate Soft Mode if Phase 8 Readiness Criteria Met

| Field | Value |
|---|---|
| Roadmap Item IDs | R-047 |
| Why | Section 7 Phase 2 requires soft mode activation only after readiness report confirms FPR/TPR/latency thresholds are met |
| Effort | S |
| Risk | Medium |
| Risk Drivers | compliance (section 7 Phase 2 activation gate) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0042 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0042/evidence.md

**Deliverables:**
- Soft mode activation: `wiring_gate_mode` changed from `"shadow"` to `"soft"` in SprintConfig defaults and roadmap pipeline configuration

**Steps:**
1. **[PLANNING]** Verify Phase 8 readiness report recommends "Proceed to soft mode" (do not activate if recommendation is "Extend shadow")
2. **[PLANNING]** Identify all configuration points: SprintConfig default, roadmap pipeline gate mode
3. **[EXECUTION]** Update SprintConfig default from `"shadow"` to `"soft"` in `sprint/models.py`
4. **[EXECUTION]** Update roadmap pipeline wiring-verification step to use soft gate mode
5. **[VERIFICATION]** Run existing shadow/soft/full mode tests to confirm soft mode behavior is correct
6. **[COMPLETION]** Record activation timestamp and readiness report reference in evidence artifact

**Acceptance Criteria:**
- `SprintConfig` default `wiring_gate_mode` is `"soft"` after activation
- Roadmap pipeline wiring-verification step operates in soft mode
- Soft mode correctly warns on critical findings and allows major/minor to pass
- Activation is traceable to readiness report recommendation

**Validation:**
- `uv run pytest tests/integration/ -k "soft_mode" -v` exits 0 confirming soft mode behavior
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0042/evidence.md

**Dependencies:** T08.06 (readiness report with "proceed" recommendation)
**Rollback:** Revert `wiring_gate_mode` default to `"shadow"` in SprintConfig and roadmap config

---

### T09.02 -- Monitor Soft Mode for 5+ Sprints for Stability Tracking

| Field | Value |
|---|---|
| Roadmap Item IDs | R-048 |
| Why | Section 7 Phase 3 requires stability tracking over 5+ sprints before full mode activation can be evaluated |
| Effort | L |
| Risk | Medium |
| Risk Drivers | performance (ongoing stability monitoring), compliance (section 7 Phase 3 observation period) |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0043 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0043/evidence.md

**Deliverables:**
- Soft mode stability tracking data from 5+ consecutive sprints: finding counts, warning frequency, false positive reports, whitelist changes, developer feedback

**Steps:**
1. **[PLANNING]** Define stability tracking metrics: warnings per sprint, false positive reports filed, whitelist additions, developer escalations
2. **[PLANNING]** Set up tracking template for per-sprint data collection
3. **[EXECUTION]** Collect stability data during sprint 1 of soft mode operation
4. **[EXECUTION]** Repeat data collection for sprints 2-5 (minimum)
5. **[EXECUTION]** Aggregate stability data and assess trend: stable, improving, or degrading
6. **[VERIFICATION]** Verify >=5 sprints of data collected with no material regressions
7. **[COMPLETION]** Store aggregated stability data at intended artifact path

**Acceptance Criteria:**
- Stability data spans >=5 consecutive sprints with soft mode active
- Each sprint entry includes: warning count, false positive count, whitelist changes, developer feedback summary
- No material regressions in audit pipeline quality during soft mode operation
- Trend assessment is documented: stable/improving/degrading with supporting data

**Validation:**
- Manual check: stability tracking data file exists with >=5 sprint entries
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0043/evidence.md

**Dependencies:** T09.01 (soft mode active)
**Rollback:** TBD (observational data; no code rollback needed)

---

### T09.03 -- Validate Full-Mode Criteria: FPR < 5% and TPR > 80%

| Field | Value |
|---|---|
| Roadmap Item IDs | R-049 |
| Why | Section 7 Phase 3 requires stricter statistical thresholds (FPR < 5%, TPR > 80%) before full enforcement mode can be activated |
| Effort | S |
| Risk | Medium |
| Risk Drivers | compliance (section 7 Phase 3 statistical gate) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0044 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0044/evidence.md

**Deliverables:**
- Full-mode criteria validation: FPR < 5% and TPR > 80% evaluated as PASS or FAIL with supporting computation from soft-mode operational data

**Steps:**
1. **[PLANNING]** Load soft-mode operational data from T09.02 stability tracking
2. **[PLANNING]** Classify findings from soft-mode operation as true positive / false positive
3. **[EXECUTION]** Compute FPR and TPR from soft-mode data with same methodology as T08.02
4. **[EXECUTION]** Compare against full-mode thresholds: FPR < 5%, TPR > 80%
5. **[VERIFICATION]** Cross-check computation against raw data; verify whitelist is stable for 5+ sprints
6. **[COMPLETION]** Record PASS or FAIL result with exact values and methodology in evidence artifact

**Acceptance Criteria:**
- FPR and TPR computed from soft-mode operational data with documented methodology
- Result is unambiguous: PASS (activate full mode) or FAIL (continue soft mode)
- Whitelist stability verified: no material changes over 5+ sprints
- If FAIL, recommendation includes specific remediation path

**Validation:**
- Manual check: full-mode criteria evaluation exists with PASS/FAIL and supporting values
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0044/evidence.md

**Dependencies:** T09.02 (soft-mode stability data)
**Rollback:** TBD (gate decision; no code rollback needed)

---

### T09.04 -- Activate Full Mode if Criteria Met

| Field | Value |
|---|---|
| Roadmap Item IDs | R-050 |
| Why | Section 7 Phase 3 gates full enforcement activation on measured FPR < 5% and TPR > 80% from soft-mode operational data |
| Effort | S |
| Risk | Medium |
| Risk Drivers | compliance (full enforcement activation) |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0045 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0045/evidence.md

**Deliverables:**
- Full mode activation: `wiring_gate_mode` changed from `"soft"` to `"full"` in SprintConfig defaults and roadmap pipeline configuration

**Steps:**
1. **[PLANNING]** Verify T09.03 criteria evaluation is PASS (do not activate if FAIL)
2. **[PLANNING]** Identify all configuration points for mode change
3. **[EXECUTION]** Update SprintConfig default from `"soft"` to `"full"` in `sprint/models.py`
4. **[EXECUTION]** Update roadmap pipeline wiring-verification step to use full gate mode
5. **[VERIFICATION]** Run full mode tests to confirm blocking behavior on critical+major findings
6. **[COMPLETION]** Record activation timestamp and criteria evaluation reference

**Acceptance Criteria:**
- `SprintConfig` default `wiring_gate_mode` is `"full"` after activation
- Full mode correctly blocks on critical and major findings
- Activation is traceable to T09.03 PASS evaluation
- All existing tests continue to pass with full mode as default

**Validation:**
- `uv run pytest tests/integration/ -k "full_mode" -v` exits 0 confirming full mode behavior
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0045/evidence.md

**Dependencies:** T09.03 (PASS criteria evaluation)
**Rollback:** Revert `wiring_gate_mode` default to `"soft"` in SprintConfig and roadmap config

---

### T09.05 -- Schedule v2.1 Improvements if Blocked by Alias Noise

| Field | Value |
|---|---|
| Roadmap Item IDs | R-051 |
| Why | R6 deferred mitigation: if alias/re-export noise prevents meeting FPR thresholds, schedule import alias pre-pass and re-export chain handling for v2.1 |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [███████░░░] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0046 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0046/spec.md

**Deliverables:**
- Either: (a) confirmation that alias noise is resolved and no v2.1 improvements needed, OR (b) v2.1 improvement schedule documenting: import alias pre-pass feature, re-export chain handling feature, and estimated scope

**Steps:**
1. **[PLANNING]** Review T08.04 noise floor characterization and T09.03 criteria evaluation
2. **[PLANNING]** Determine if alias noise blocked full-mode activation (T09.03 FAIL due to FPR)
3. **[EXECUTION]** If not blocked: document "Alias noise resolved; no v2.1 improvements required" with evidence reference
4. **[EXECUTION]** If blocked: create v2.1 improvement schedule with: import alias pre-pass specification, re-export chain handling specification, estimated LOC and effort
5. **[VERIFICATION]** Verify schedule (if created) references specific R6 evidence and noise floor data
6. **[COMPLETION]** Store decision document at intended artifact path

**Acceptance Criteria:**
- Decision document exists with clear determination: alias noise resolved OR v2.1 improvements scheduled
- If v2.1 scheduled: import alias pre-pass and re-export chain handling are specified with scope estimates
- Document references T08.04 noise floor characterization and T09.03 criteria evaluation
- Decision is traceable to measured evidence, not speculation

**Validation:**
- Manual check: decision document exists with resolved/scheduled determination and evidence references
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0046/spec.md

**Dependencies:** T08.04 (noise floor), T09.03 (criteria evaluation)
**Rollback:** TBD (planning document; no code rollback needed)

---

### Checkpoint: End of Phase 9

**Purpose:** Validate milestone M6b: enforcement level advanced only on measured operational evidence.
**Checkpoint Report Path:** .dev/releases/current/v3.0_unified-audit-gating/checkpoints/CP-P09-END.md
**Verification:**
- Soft mode activated only after Phase 8 readiness criteria met
- Full mode activated only after FPR < 5% and TPR > 80% from 5+ sprints of soft-mode data
- v2.1 improvements scheduled if alias noise blocks full activation
**Exit Criteria:**
- Enforcement level matches measured evidence: shadow/soft/full based on thresholds
- No material audit regressions during enforcement transitions
- All activation decisions are traceable to readiness/criteria evaluation documents
