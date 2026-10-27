---
spec_source: "spec-refactor-plan-merged.md"
complexity_score: 0.92
primary_persona: architect
---

# 1. Executive summary

This roadmap delivers **unified audit-gating for milestone and release scope in v1.2.1**, while explicitly **deferring task-scope gating to v1.3**. The program is architecturally high-risk because it spans the sprint executor, audit model, roadmap fidelity checks, CLI-portify smoke validation, workflow state persistence, and operational rollout controls.

## Strategic objectives
1. **Prevent false-success releases** by introducing mandatory behavioral audit gates.
2. **Make gate decisions deterministic and auditable** through explicit result schemas, freshness validation, and deterministic semantic checks.
3. **Harden transition control** so milestone/release completion cannot proceed on stale, missing, or bypassed evidence.
4. **Roll out safely** via Shadow → Soft → Full promotion with measurable KPI gates and rollback readiness.

## Architectural priorities
- **Priority 1:** Fix blocking defects that make legitimate execution indistinguishable from no-op execution.
- **Priority 2:** Establish canonical domain model and state machine before broad integration.
- **Priority 3:** Integrate behavioral gates as first-class audit results, not side-channel checks.
- **Priority 4:** Validate deterministic replay, timeout handling, and override restrictions before promotion.
- **Priority 5:** Preserve extensibility for v1.3 task-scope activation without implementing it now.

## Scope boundaries
### In scope for v1.2.1
- Milestone-scope and release-scope audit gates
- `SilentSuccessDetector`
- Smoke Test Gate G-012
- Spec Fidelity checks D-03 and D-04
- Lease/heartbeat/retry model
- Audit persistence, freshness validation, TUI exposure, rollout telemetry

### Explicitly deferred to v1.3
- Task-scope gate enforcement
- Activation of task-scope transitions beyond annotation and deferral markers

---

# 2. Phased implementation plan with milestones

## Phase 0 — Governance, defect closure, and architecture baseline

### Goals
- Resolve blockers that would invalidate later gates.
- Freeze terminology, ownership, and rollout constraints.
- Remove known dead/orphaned paths before integrating new behavior.

### Workstreams
1. **Governance and decision closure**
   - Assign named owners for Reliability, Policy, Tasklist, and Program Management.
   - Ratify canonical terms:
     - `AuditLease`
     - `audit_lease_timeout`
     - `max_turns`
     - `Critical Path Override`
     - `audit_gate_required`
     - `audit_attempts`
   - Lock per-scope implementation policy:
     - v1.2.1 = milestone + release only
     - task scope retained with `[v1.3 -- deferred]` markers

2. **Blocking defect remediation**
   - Fix `run_portify()` to pass `step_runner` and establish `STEP_DISPATCH`.
   - Enforce `validate_portify_config()` before `run_portify()` with non-zero exit on validation failure.
   - Retire:
     - `_apply_resume_after_spec_patch()`
     - `_find_qualifying_deviation_files()`

3. **Architecture survey and collision avoidance**
   - Survey `cli/audit/` for naming and model overlap.
   - Introduce `AuditGateResult` to avoid collision with existing `GateResult`.
   - Confirm integration points:
     - sprint executor
     - trailing gate runner
     - output monitor
     - tasklist generator
     - roadmap gate system
     - TUI/state persistence

### Milestones
- **M0.1** Owners and unresolved decisions assigned.
- **M0.2** P0-A defect fixes verified.
- **M0.3** Dead roadmap executor paths removed.
- **M0.4** Canonical architecture contract approved.

### Exit criteria
- SC-003 and SC-004 pass.
- All Phase 1 prerequisites have explicit owners and deadlines.
- No ambiguity remains about v1.2.1 scope boundaries.

---

## Phase 1 — Deterministic audit foundation

### Goals
- Build the core data model and deterministic evidence layer.
- Enable reliable post-run behavioral detection before gate orchestration.
- Add deterministic fidelity validation and roadmap deviation analysis.

### Workstreams
1. **Audit result model and persistence**
   - Implement `AuditGateResult` with:
     - artifact hashes
     - freshness metadata
     - `silent_success_audit`
     - `smoke_test_result`
     - `fidelity_deterministic`
   - Persist audit block in `_save_state()`.
   - Enforce completeness rules for STRICT tier.

2. **Silent Success Detection**
   - Implement `silent_success.py`:
     - `FileSnapshot`
     - `StepTrace`
     - `SilentSuccessConfig`
     - `SilentSuccessDetector`
     - `SilentSuccessResult`
     - `SilentSuccessError`
   - Instrument executor:
     - pre-run snapshot
     - step timing capture
     - post-loop detector invocation
     - return-contract emission ordering
   - Add new outcomes:
     - `SILENT_SUCCESS_SUSPECTED`
     - `SUSPICIOUS_SUCCESS`

3. **Deterministic spec fidelity**
   - Implement `fidelity_inventory.py`.
   - Add D-03 and D-04 to `SPEC_FIDELITY_GATE`.
   - Ensure deterministic findings fail the gate even when LLM severity is zero.

4. **Roadmap execution correction**
   - Insert `deviation-analysis` after `spec-fidelity`.
   - Update step registry and prompt builder.

### Milestones
- **M1.1** `AuditGateResult` schema finalized and persisted.
- **M1.2** `SilentSuccessDetector` operational in executor.
- **M1.3** D-03/D-04 deterministic checks wired and failing correctly.
- **M1.4** `deviation-analysis.md` produced by roadmap pipeline.

### Exit criteria
- SC-001, SC-002, SC-010, SC-012 pass.
- Deterministic replay produces stable gate results.
- Missing/unknown deterministic inputs fail safely.

---

## Phase 2 — Gate implementation and workflow integration

### Goals
- Convert behavioral checks into enforceable milestone/release audit gates.
- Introduce lease/heartbeat/retry safety controls.
- Integrate operational state transitions and observability.

### Workstreams
1. **Lease and retry model**
   - Implement audit lease model with:
     - `lease_id`
     - `owner`
     - `acquired_at`
     - `renewed_at`
     - `expires_at`
   - Heartbeat renewal interval:
     - `<= audit_lease_timeout / 3`
   - Timeout transition to `audit_*_failed(timeout)`.
   - Durable `audit_attempts` counter with provisional defaults.

2. **Smoke Test Gate G-012**
   - Implement `smoke_gate.py` with:
     - configs
     - results
     - execution runner
     - timing/artifact/content checks
   - Register as release-tier blocking gate.
   - Support `--mock-llm` mode for CI.
   - Enforce failure routing:
     - network/API failures → transient
     - timing/artifact/content evidence failures → policy.smoke_failure.*

3. **Execution and policy integration**
   - Wire `SprintGatePolicy` into `execute_sprint()`.
   - Wire `TrailingGateRunner` with:
     - `GateScope.MILESTONE`
     - `GateScope.RELEASE`
   - Extend `OutputMonitor` for lease heartbeats.
   - Add `--grace-period` CLI support.

4. **Tasklist and rule propagation**
   - Add `audit_gate_required` derivation to tasklist generation.
   - Preserve task-scope sections with deferral annotations only.

5. **TUI and operator experience**
   - Surface `AuditWorkflowState` in phase table.
   - Add release guard for “Sprint Complete”.
   - Add operator guidance for audit failure states.

### Milestones
- **M2.1** Lease/heartbeat/retry state machine works end-to-end.
- **M2.2** G-012 fails known-bad executor correctly.
- **M2.3** G-012 passes after defect fixes.
- **M2.4** Milestone/release transition blocking enforced.
- **M2.5** TUI/state persistence/operator flows complete.

### Exit criteria
- SC-005, SC-006, SC-008, SC-009, SC-011, SC-014 pass.
- No deadlocks in timeout/retry flows.
- Current-artifact freshness validation blocks stale gate reuse.

---

## Phase 3 — Validation, calibration, and shadow rollout

### Goals
- Validate real-world behavior without blocking production flows.
- Calibrate timing/KPI thresholds from evidence.
- Ensure rollout readiness with complete telemetry.

### Workstreams
1. **Shadow mode instrumentation**
   - Wire `ShadowGateMetrics`.
   - Emit:
     - lease acquisition/duration
     - lease timeout counts
     - override events
     - suspicion-score band distributions
     - smoke gate outcomes
     - fidelity deterministic failure rates

2. **Threshold calibration**
   - Recalibrate:
     - M1 runtime thresholds for phase scope
     - S2 silent-success timing thresholds
     - M13/M14 provisional KPI defaults
   - Secure Reliability Owner approval.

3. **Regression and replay validation**
   - Run v2.25 artifact regressions.
   - Validate deterministic replay stability across repeated runs.
   - Verify per-task artifact addressability checkpoint C3.

4. **Operational readiness**
   - Produce rollback drill.
   - Validate override restrictions by scope.
   - Confirm no source-file line citations in prohibited sections.

### Milestones
- **M3.1** Shadow mode enabled with full telemetry.
- **M3.2** Calibration protocol documented and approved.
- **M3.3** C3 checkpoint resolved.
- **M3.4** Promotion decision package prepared.

### Exit criteria
- SC-007, SC-013, SC-015 readiness evidence complete.
- NFR rollout promotion criteria satisfied for Shadow → Soft.

---

## Phase 4 — Soft enforcement to full promotion

### Goals
- Progress from advisory visibility to blocking enforcement.
- Verify sustained KPI compliance across consecutive windows.
- Complete rollback and release-readiness validation.

### Workstreams
1. **Soft enforcement**
   - Enable blocking where approved.
   - Allow only authorized override paths at milestone scope.
   - Prohibit release-scope overrides.

2. **Full promotion**
   - Require all M1-M12 criteria across two consecutive windows.
   - Complete rollback drill successfully.
   - Lock normative thresholds after approval.

3. **Post-promotion hardening**
   - Review false-positive/false-negative rates.
   - Confirm operator workflow clarity.
   - Freeze v1.2.1 scope and open v1.3 backlog for task-scope activation.

### Milestones
- **M4.1** Soft mode enabled.
- **M4.2** KPI windows pass consecutively.
- **M4.3** Full mode enabled for release blocking.
- **M4.4** v1.2.1 closeout and v1.3 handoff complete.

### Exit criteria
- SC-015 and SC-016 pass.
- Full promotion approved with rollback evidence and sustained KPI performance.

---

# 3. Risk assessment and mitigation strategies

## High-risk items

1. **Silent-success threshold miscalibration**
   - **Impact:** False positives or missed no-op executions.
   - **Mitigation:**
     - Require documented calibration methodology before soft activation.
     - Run shadow data collection before normative thresholds.
     - Separate warn/soft-fail/hard-fail bands operationally.

2. **Blocking defects invalidate smoke gate**
   - **Impact:** Legitimate executions appear empty; G-012 becomes misleading.
   - **Mitigation:**
     - Make defect fixes a hard dependency before Phase 2.
     - Keep SC-003 and SC-004 as mandatory preconditions.

3. **State-machine deadlocks in lease/retry flows**
   - **Impact:** Hung audit states block completion or require manual recovery.
   - **Mitigation:**
     - Deterministic timeout transitions.
     - Outer wall-clock ceiling enforcement.
     - Explicit lease expiry handling and retry budget exhaustion tests.

4. **Stale gate results allow incorrect transitions**
   - **Impact:** Completion or release may be approved on old evidence.
   - **Mitigation:**
     - Artifact hash storage in `AuditGateResult`.
     - Mandatory freshness validation against current artifact version.
     - Re-evaluation on mismatch.

5. **Per-task artifact addressability uncertainty**
   - **Impact:** v1.3 task-scope path may be structurally blocked.
   - **Mitigation:**
     - Treat C3 as explicit go/no-go checkpoint.
     - Escalate early if outputs are not individually addressable.
     - Avoid backdoor task-scope activation in v1.2.1.

## Medium-risk items

6. **Smoke fixture drift**
   - **Mitigation:**
     - Stability contract for named fixture components.
     - Dedicated fixture-content regression test.

7. **`--mock-llm` ambiguity**
   - **Mitigation:**
     - Define active vs skipped check matrix before CI adoption.
     - Preserve artifact-absence checks as non-negotiable.

8. **Regex undercoverage in deterministic fidelity checks**
   - **Mitigation:**
     - Validate against representative spec corpus.
     - Add allowlist/feature flag if authoring conventions diverge.

9. **Overlap with Anti-Instincts**
   - **Mitigation:**
     - Gate D-03/D-04 behind feature flag if sequencing requires coexistence.

10. **KPI threshold drift between scopes**
    - **Mitigation:**
      - Treat task-scope and phase-scope thresholds independently.
      - Require fresh calibration rather than inherited defaults.

## Governance risk
11. **Unowned blockers and decisions**
    - **Mitigation:**
      - No phase GO without named owner + deadline for each blocker.
      - Program manager tracks closure before each promotion gate.

12. **Scope creep into task-gating**
    - **Mitigation:**
      - Preserve annotations only.
      - Reject implementation work that activates task scope in v1.2.1.

---

# 4. Resource requirements and dependencies

## Required roles
1. **Architect / Technical Lead**
   - Owns cross-subsystem design, interface contracts, rollout sequencing.

2. **Reliability Owner**
   - Owns timeout values, calibration protocols, KPI approval, rollout readiness.

3. **Policy Owner**
   - Owns failure-class taxonomy, override restrictions, strictness/profile alignment.

4. **CLI / Execution Engineer**
   - Implements executor instrumentation, smoke gate, command validation, trailing gate wiring.

5. **Audit / State Machine Engineer**
   - Implements `AuditGateResult`, lease model, retries, persistence, freshness checks.

6. **Roadmap / Semantic Validation Engineer**
   - Implements D-03/D-04, deviation-analysis step, spec inventory.

7. **TUI / UX Engineer**
   - Surfaces audit workflow states and operator guidance.

8. **QA / Validation Engineer**
   - Owns regression fixtures, replay stability, deadlock testing, smoke test matrices.

9. **Program Manager**
   - Tracks blocker closure, owner assignments, promotion evidence, and go/no-go readiness.

## Technical dependencies
1. Existing `GateResult` in `cli/audit/evidence_gate.py`
2. Sprint executor integration point
3. `OutputMonitor` extension point
4. `TrailingGateRunner`
5. `GATE_REGISTRY`
6. `SPEC_FIDELITY_GATE`
7. `return-contract.yaml`
8. v2.25 regression artifacts
9. `sc-audit-gate-protocol/SKILL.md`
10. `sc-tasklist-protocol/SKILL.md`
11. Tasklist generator
12. LLM API availability for non-mock smoke runs
13. TUI state rendering infrastructure
14. Audit persistence path in state save/load lifecycle

## Infrastructure and tooling needs
- Stable smoke fixture repository path
- CI lane supporting `--mock-llm`
- Replay test harness
- Shadow telemetry capture and dashboarding
- Artifact hashing capability
- UTC timestamp normalization for lease tracking

---

# 5. Success criteria and validation approach

## Validation strategy

### A. Foundation validation
1. Verify broken executor triggers silent-success hard evidence.
2. Verify deterministic fidelity checks fail incorrect roadmap/spec pairs.
3. Verify config validation prevents invalid execution before runtime.

### B. Integration validation
1. Verify smoke gate fails known-bad executor for the correct reasons.
2. Verify smoke gate passes after executor defects are fixed.
3. Verify current-artifact freshness is enforced during milestone/release transitions.
4. Verify all-EXEMPT flows fail unless valid dry-run conditions apply.

### C. Reliability validation
1. Verify deterministic replay stability.
2. Verify timeout/retry paths terminate without deadlock.
3. Verify lease renewal and expiry behavior under delayed or missing heartbeats.
4. Verify retry budgets are durable and scope-aware.

### D. Governance validation
1. Verify release-scope overrides are impossible.
2. Verify milestone overrides require valid `OverrideRecord`.
3. Verify deterministic D-03/D-04 failures cannot be masked by LLM output.
4. Verify missing audit-result blocks fail STRICT tier checks.

### E. Rollout validation
1. Shadow metrics collected and analyzed.
2. KPI thresholds recalibrated and approved.
3. Rollback drill executed successfully.
4. Two consecutive promotion windows pass before full rollout.

## Success criteria mapping
- **Build correctness:** SC-001 through SC-006
- **Determinism and auditability:** SC-007 through SC-012
- **Structural future-readiness:** SC-013
- **Operational policy enforcement:** SC-014 through SC-016

## Recommended test suites
1. **Unit tests**
   - score bands
   - regex inventory extraction
   - failure-class routing
   - artifact hash freshness logic

2. **Integration tests**
   - executor instrumentation
   - smoke gate end-to-end
   - trailing gate evaluation
   - tasklist derivation of `audit_gate_required`

3. **Regression tests**
   - v2.25 spec/roadmap pairs
   - smoke fixture content anchors
   - stale gate result rejection

4. **Operational tests**
   - lease expiry and recovery
   - retry exhaustion
   - shadow metric emission
   - TUI state rendering and operator messaging

---

# 6. Timeline estimates per phase

Given the **0.92 / HIGH** complexity score and cross-cutting integration density, the roadmap should be planned as a **multi-wave delivery** rather than a single sprint.

## Estimated phase durations

1. **Phase 0 — Governance and defect closure**
   - **Estimate:** 1-2 weeks
   - **Reasoning:** blocker closure, owner assignment, design ratification, removal of dead paths

2. **Phase 1 — Deterministic audit foundation**
   - **Estimate:** 2-3 weeks
   - **Reasoning:** new result model, executor instrumentation, silent-success detector, fidelity inventory, roadmap step changes

3. **Phase 2 — Gate implementation and workflow integration**
   - **Estimate:** 3-4 weeks
   - **Reasoning:** state-machine integration, lease/heartbeat/retry logic, smoke gate, transition enforcement, TUI/state persistence

4. **Phase 3 — Shadow rollout and calibration**
   - **Estimate:** 2-4 weeks
   - **Reasoning:** data collection window, KPI calibration, replay validation, C3 checkpoint, operational readiness evidence

5. **Phase 4 — Soft to full promotion**
   - **Estimate:** 2-3 weeks
   - **Reasoning:** consecutive KPI windows, rollback drill, production hardening, closeout

## Overall program estimate
- **Best-case:** 10 weeks
- **Expected architectural planning range:** 12-16 weeks
- **Primary schedule drivers:**
  - blocker ownership latency
  - calibration window length
  - C3 per-task artifact decision
  - `--mock-llm` CI semantics
  - rollout KPI stability

## Recommended sequencing guardrails
1. Do not start Phase 2 until P0-A fixes are verified.
2. Do not promote to Soft until calibration protocol is approved.
3. Do not promote to Full until two consecutive KPI windows pass.
4. Do not expand scope into task gating during v1.2.1.

---

# Recommended architect decisions to make immediately

1. Assign owners and deadlines for all unresolved blockers.
2. Approve provisional milestone/release lease timeout defaults.
3. Decide whether `reimbursement_rate` is removed or productized.
4. Define the exact `--mock-llm` check matrix.
5. Approve the shadow observation window required for KPI normalization.
6. Resolve C3 escalation authority before Phase 3 begins.
7. Decide whether D-03/D-04 ship behind a feature flag based on Anti-Instincts timing.

# Final recommendation

Proceed with a **four-phase delivery plus rollout promotion**, treating **Phase 0 and Phase 1 as mandatory architectural stabilization**. The highest-value path is to first make false-success detection and deterministic fidelity failures undeniable in the system, then enforce milestone/release gating only after timeout, freshness, and rollout controls are operationally proven. This sequencing minimizes release risk while preserving a clean v1.3 path for task-scope expansion.
