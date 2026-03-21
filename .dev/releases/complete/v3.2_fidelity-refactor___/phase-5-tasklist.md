# Phase 5 -- Rollout Validation

Post-merge engineering validation milestones for the wiring gate. Each milestone produces measurable evidence that informs promotion decisions from shadow to soft to blocking mode. This phase addresses R6 (provider_dir_names mismatch) — the highest-severity risk — which can only be fully validated during real-world operation. Minimum 2-release shadow period mandated by spec.

---

### T05.01 -- Establish Shadow Mode Baseline

| Field | Value |
|---|---|
| Roadmap Item IDs | R-041 |
| Why | Shadow mode baseline validates the gate against real repositories without affecting sprint execution, collecting findings volume, whitelist coverage, and runtime data to inform promotion decisions. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | performance (real workload runtime), data (baseline quality) |
| Tier | EXEMPT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0025, D-0026 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0025/notes.md`
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0026/notes.md`

**Deliverables:**
1. Shadow mode baseline data: findings volume per analysis run, whitelist usage and coverage, zero-findings anomalies (SC-011 warnings), p95 runtime under real workloads
2. Validated `provider_dir_names` and registry patterns against real repository conventions (R6 mitigation layer 3)

**Steps:**
1. **[PLANNING]** Activate Goal-5a (shadow/log-only mode) in production configuration
2. **[EXECUTION]** Collect findings volume per analysis run across minimum 2-release shadow period
3. **[EXECUTION]** Evaluate whitelist usage and coverage; identify false positive patterns
4. **[EXECUTION]** Monitor for zero-findings anomalies (SC-011 warnings indicating potential misconfiguration)
5. **[EXECUTION]** Measure p95 runtime under real workloads; compare against SC-009 threshold
6. **[EXECUTION]** Validate `provider_dir_names` and `registry_patterns` against actual repository directory conventions
7. **[VERIFICATION]** Review collected baseline data for completeness and anomalies
8. **[COMPLETION]** Record baseline data to D-0025/notes.md and provider validation to D-0026/notes.md

**Acceptance Criteria:**
- Shadow mode activated and baseline data collected across minimum 2-release period (spec mandate)
- Findings volume per analysis run evaluated; whitelist usage and coverage assessed; zero-findings anomalies (SC-011 warnings) documented; p95 runtime under real workloads measured
- `provider_dir_names` validated against real repository conventions (R6 mitigation confirmed or adjustments identified)
- p95 runtime under real workloads measured and compared against SC-009 threshold

**Validation:**
- Manual check: baseline data report reviewed for completeness across 2-release period
- Evidence: baseline data produced at D-0025/notes.md and D-0026/notes.md

**Dependencies:** Phase 4 complete (all code merged, tests passing)
**Rollback:** Deactivate shadow mode; delete baseline data artifacts

---

### T05.02 -- Assess Soft Mode Readiness

| Field | Value |
|---|---|
| Roadmap Item IDs | R-042 |
| Why | Soft mode readiness assessment determines whether the whitelist is adequate for FPR management and whether findings are actionable enough to surface as warnings to users. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | data (FPR measurement), cross-cutting (whitelist adequacy across finding types) |
| Tier | EXEMPT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0027 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0027/notes.md`

**Deliverables:**
1. Soft mode readiness assessment: FPR burden analysis and remediation usefulness evaluation (Goal-5b promotion criteria)

**Steps:**
1. **[PLANNING]** Review shadow mode baseline data from T05.01; identify FPR patterns
2. **[EXECUTION]** Measure false-positive burden: what percentage of findings require whitelist suppression?
3. **[EXECUTION]** Evaluate remediation usefulness: are findings actionable for developers?
4. **[EXECUTION]** Verify no regression against legacy `ledger is None` paths
5. **[VERIFICATION]** Review readiness assessment against Goal-5b promotion criteria
6. **[COMPLETION]** Record assessment to D-0027/notes.md

**Acceptance Criteria:**
- False-positive rate shown to be manageable through `wiring_whitelist.yaml` with evidence from real finding data (promotion criterion per Goal-5b)
- Remediation usefulness evaluated: findings actionable or requiring tuning identified
- No regression against legacy `ledger is None` paths confirmed
- Promotion criteria checklist completed with evidence-backed assessment

**Validation:**
- Manual check: readiness assessment reviewed against Goal-5b promotion criteria
- Evidence: assessment produced at D-0027/notes.md

**Dependencies:** T05.01
**Rollback:** Remain in shadow mode; delete D-0027/notes.md

---

### T05.03 -- Authorize Blocking Mode Promotion

| Field | Value |
|---|---|
| Roadmap Item IDs | R-043 |
| Why | Blocking mode authorization is evidence-gated — enforcement mode is selected by evidence, not by schedule. All 5 evidence thresholds must be met before enabling fail+remediate behavior. |
| Effort | M |
| Risk | High |
| Risk Drivers | breaking (enforcement enables task failure), security (remediation correctness), data (evidence threshold validation) |
| Tier | EXEMPT |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0028 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0028/notes.md`

**Deliverables:**
1. Blocking mode authorization decision with evidence checklist: SC-009 stable, SC-010 confirmed in real code, shadow data quality acceptable, whitelist/heuristics calibrated, budget/recursion protections verified

**Steps:**
1. **[PLANNING]** Review T05.01 and T05.02 evidence; compile authorization checklist
2. **[EXECUTION]** Verify SC-009 stable across shadow period (p95 performance consistent)
3. **[EXECUTION]** Verify SC-010 confirmed detection in real code, not just fixtures
4. **[EXECUTION]** Verify shadow data quality acceptable — no silent misconfiguration artifacts
5. **[EXECUTION]** Verify whitelist and provider heuristics calibrated against actual conventions
6. **[EXECUTION]** Verify budget constants and recursion protections in production path
7. **[VERIFICATION]** Review all 5 evidence thresholds; record authorization decision (approve/defer with rationale)
8. **[COMPLETION]** Record authorization decision to D-0028/notes.md

**Acceptance Criteria:**
- All 5 evidence thresholds documented with pass/fail status and supporting data
- Authorization decision recorded: approve blocking mode or defer with specific rationale
- SC-009, SC-010 evidence explicitly referenced from prior milestone data
- Decision based on evidence, not schedule (key principle preserved)

**Validation:**
- Manual check: authorization decision reviewed by stakeholder
- Evidence: authorization decision produced at D-0028/notes.md

**Dependencies:** T05.02
**Rollback:** Remain in soft mode; delete D-0028/notes.md

---

### Checkpoint: End of Phase 5

**Purpose:** Final rollout validation gate — confirm evidence-driven promotion decisions are documented and all success criteria are satisfied.
**Checkpoint Report Path:** `.dev/releases/current/v3.2_fidelity-refactor___/checkpoints/CP-P05-END.md`
**Verification:**
- Shadow mode baseline collected across minimum 2-release period
- `provider_dir_names` validated against real repository conventions (R6 fully mitigated)
- Blocking mode authorization decision documented with evidence checklist
**Exit Criteria:**
- All 3 tasks (T05.01-T05.03) completed with deliverables D-0025 through D-0028 produced
- Evidence-gated promotion model validated: shadow -> soft -> blocking progression documented
- All 15 success criteria (SC-001 through SC-015) satisfied or explicitly dispositioned
