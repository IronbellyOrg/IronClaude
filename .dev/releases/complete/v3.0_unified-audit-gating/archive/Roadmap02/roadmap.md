---
spec_source: "spec-refactor-plan-merged.md"
complexity_score: 0.92
adversarial: true
base_variant: "A (Opus Architect)"
convergence_score: 0.78
debate_rounds: 3
variant_scores: "A:82 B:72"
generated: "2026-03-18"
---

## Executive Summary

This roadmap delivers a **multi-scope audit gate framework** (milestone + release) for v1.2.1, with three behavioral gate extensions: Silent Success Detection, Smoke Test Gate (G-012), and Spec Fidelity Deterministic Checks (D-03/D-04). The system integrates into the existing sprint executor and pipeline gate infrastructure, blocking completion and release transitions unless gates pass.

### Strategic Objectives

1. **Prevent false-success releases** by introducing mandatory behavioral audit gates that detect no-op executions, broken artifact production, and spec drift.
2. **Make gate decisions deterministic and auditable** through explicit result schemas, freshness validation, and deterministic semantic checks.
3. **Harden transition control** so milestone/release completion cannot proceed on stale, missing, or bypassed evidence.
4. **Roll out safely** via Shadow → Soft → Full promotion with measurable KPI gates and rollback readiness.

### Scope

- **47 functional + 18 non-functional requirements** across 6 domains (backend, security, CLI, testing, devops, observability).
- **Task-scope gating is explicitly deferred to v1.3.**
- **Delivery strategy**: 5-phase rollout (Prerequisites → Foundation → Integration → Enforcement → Promotion) with go/no-go gates at each transition.
- **Estimated 25+ files changed** across sprint executor, cli-portify, roadmap, audit, tasklist, and TUI subsystems.

### Key Architectural Decision

All new gate logic builds on the existing `cli/pipeline/` gate substrate (`GateCriteria`, `TrailingGateRunner`, `GateScope`). The new `AuditGateResult` dataclass avoids namespace collision with the existing 2-field `GateResult` in `cli/audit/evidence_gate.py`.

### Scope Boundaries

#### In scope for v1.2.1

- Milestone-scope and release-scope audit gates
- `SilentSuccessDetector`
- Smoke Test Gate G-012
- Spec Fidelity checks D-03 and D-04
- Lease/heartbeat/retry model
- Audit persistence, freshness validation, TUI exposure, rollout telemetry

#### Explicitly deferred to v1.3

- Task-scope gate enforcement
- Activation of task-scope transitions beyond annotation and deferral markers

---

## Phased Implementation Plan

### Phase 0 — Prerequisites and P0 Defect Fixes

**Duration**: 1–2 weeks
**Primary schedule drivers**: blocker ownership latency, design ratification turnaround

#### 0.1 — Governance and Decision Closure

1. Assign named owners for Reliability, Policy, Tasklist, and Program Management roles
2. Ratify canonical terms (FR-008): `AuditLease`, `audit_lease_timeout`, `max_turns`, `Critical Path Override`, `audit_gate_required`, `audit_attempts`
3. Lock per-scope implementation policy: v1.2.1 = milestone + release only (FR-006)
4. Add `[v1.3 -- deferred]` markers to all task-scope transitions in SS4.1 (FR-009)

#### 0.2 — P0-A Defect Fixes (Blocker 9)

1. **Fix Defect 1** (FR-031): `run_portify()` in `cli/cli_portify/executor.py` must pass `step_runner` to `PortifyExecutor`; create `STEP_DISPATCH` mapping from step IDs to imported step functions
2. **Fix Defect 2** (FR-032): `cli/cli_portify/commands.py` must call `validate_portify_config()` before `run_portify()`; exit non-zero on validation errors
3. Verify SC-003 and SC-004 pass after fixes

#### 0.3 — Dead Code Retirement (FR-046)

1. Retire `_apply_resume_after_spec_patch()` from roadmap executor
2. Retire `_find_qualifying_deviation_files()` from roadmap executor
3. Confirm no live references via `find_referencing_symbols`

#### 0.4 — Architecture Survey and Collision Avoidance

1. Survey `cli/audit/` for naming and model overlap
2. Confirm `AuditGateResult` avoids collision with existing `GateResult`
3. Confirm integration points: sprint executor, trailing gate runner, output monitor, tasklist generator, roadmap gate system, TUI/state persistence

#### Go/No-Go Criteria

- [ ] SC-003: `run_portify()` produces intermediate artifacts
- [ ] SC-004: `commands.py` exits non-zero on validation errors
- [ ] Dead code retired with zero remaining references
- [ ] All 6 canonical terms documented
- [ ] All Phase 1 prerequisites have explicit owners and deadlines
- [ ] No ambiguity remains about v1.2.1 scope boundaries

---

### Phase 1 — Foundation: Data Models, Detectors, and Gates

**Duration**: 2–3 weeks
**Primary schedule drivers**: C3 per-task artifact resolution, D-03/D-04 regex coverage validation

#### 1.1 — Core Data Models

1. **`AuditGateResult` dataclass** (FR-022, FR-023):
   - Disambiguated name to avoid collision with `cli/audit/evidence_gate.py::GateResult`
   - `artifacts` block with SHA-256 version hashes for freshness validation
   - `silent_success_audit` block (FR-018): `suspicion_score`, per-signal scores (S1-S3), `band`, `diagnostics`, `gate_decision`, `thresholds`
   - `smoke_test_result` block (FR-019): `gate_id`, `fixture_path`, `elapsed_s`, `artifacts_found`, `checks_passed`, `checks_failed`, `failure_class`, `tmpdir_cleaned`
   - `fidelity_deterministic` block (FR-020): dispatch tables/functions found/preserved booleans, checks run/excluded lists

2. **Failure class taxonomy** (FR-014):
   - Extend `policy` failure class with sub-types: `policy.silent_success`, `policy.smoke_failure` (`.timing`, `.artifact_absence`, `.content_evidence`), `policy.fidelity_deterministic`

3. **Outcome enum extension** (FR-035):
   - Add `PortifyOutcome.SILENT_SUCCESS_SUSPECTED` and `PortifyOutcome.SUSPICIOUS_SUCCESS` to `cli/cli_portify/models.py`

#### 1.2 — Silent Success Detector (FR-002, FR-024, FR-025, FR-033)

1. Implement `silent_success.py` (~300 lines):
   - `FileSnapshot`, `StepTrace`, `SilentSuccessConfig`, `SilentSuccessDetector`, `SilentSuccessResult`, `SilentSuccessError`
   - Signal suite: S1 (Artifact Content, 0.35), S2 (Execution Trace, 0.35), S3 (Output Freshness, 0.30)
   - Composite formula: `suspicion_score = ((1-S1) × 0.35) + ((1-S2) × 0.35) + ((1-S3) × 0.30)`
   - Bands: 0.0–0.29 pass, 0.30–0.49 warn, 0.50–0.74 soft-fail, 0.75–1.00 hard-fail
2. `SilentSuccessConfig(enabled=False)` for test harnesses (NFR-002)
3. All-EXEMPT/SKIPPED with zero real steps = `policy` failure unless `--dry-run` (FR-007, FR-017)
4. Absence of `silent_success_audit` block = `failed` at STRICT tier (NFR-004)

#### 1.3 — Smoke Test Gate G-012 (FR-003, FR-027, FR-037)

> **Note**: If a single implementer is responsible for both gate logic and integration, defer G-012 implementation to Phase 2 and build against real integration interfaces. If multiple implementers are available, build gate logic here with integration wiring in Phase 2.

1. Implement `smoke_gate.py` (~400 lines):
   - `SmokeTestConfig`, `SmokeTestResult` dataclasses
   - `run_smoke_test()` function
   - Check hierarchy: timing (<5s = WARN only), artifact absence (ERROR, blocking), content evidence (ERROR, blocking)
   - Constants: `SMOKE_NOOP_CEILING_S=5`, `SMOKE_MIN_REAL_EXECUTION_S=10`, `SMOKE_TIMEOUT_S=600`
2. Register G-012 as `smoke-test` in `GATE_REGISTRY` (cli_portify/gates.py) after G-011
3. Failure routing (FR-015): API/network errors → `transient`; timing/artifact/content → `policy.smoke_failure.*`
4. `--mock-llm` mode for CI (FR-028)
5. `tmpdir_cleaned: bool` for AC-006 compliance (NFR-015)

#### 1.4 — Spec Fidelity Deterministic Checks D-03/D-04 (FR-004, FR-029, FR-030, FR-036)

1. Implement `fidelity_inventory.py` (~150 lines):
   - `SpecInventory` dataclass, `build_spec_inventory()`
   - `_DISPATCH_TABLE_PATTERN`: regex for `UPPER_CASE_NAME = {` or `dict(`
   - `_STEP_DISPATCH_CALL`: regex for `_run_*()` or `step_result =`
   - `_DEP_ARROW_PATTERN` regex
2. Wire D-03 and D-04 into `SPEC_FIDELITY_GATE` in `cli/roadmap/gates.py`
3. Deterministic checks override LLM output (FR-021): `dispatch_tables_preserved: false` OR `dispatch_functions_preserved: false` → gate failed regardless of `high_severity_count`
4. Feature flag for Anti-Instincts overlap (NFR-014) — ~10 lines, cheap insurance against timeline shifts

#### 1.5 — Standalone Emission (P0-B)

1. Instrument executor with `_step_traces`, `time.monotonic()` wrapping (FR-034)
2. `snapshot_pre_run()` call before execution
3. Post-loop detector invocation
4. `SilentSuccessResult` standalone emission to `return-contract.yaml` (FR-002)

#### 1.6 — Deviation Analysis Integration (FR-047)

1. Wire `deviation-analysis` step into roadmap `_build_steps()` after `spec-fidelity`
2. Update `_get_all_step_ids()`
3. Write `build_deviation_analysis_prompt()`

#### Go/No-Go Criteria

- [ ] SC-001: No-op pipeline → `suspicion_score = 1.0`, `SILENT_SUCCESS_SUSPECTED`, non-zero exit
- [ ] SC-002: v2.25 regression → `dispatch_tables_preserved: false`, gate rejects
- [ ] SC-005: G-012 against known-bad executor fails correctly
- [ ] SC-009: All-EXEMPT registry → `failed(policy.silent_success)`
- [ ] SC-010: Deterministic replay stability verified
- [ ] SC-012: Roadmap pipeline produces `deviation-analysis.md`
- [ ] SC-013: C3 validation — per-task artifacts individually addressable
- [ ] NFR-006: Same input → same gate result

---

### Phase 2 — Integration: State Machine, Leases, and Executor Wiring

**Duration**: 3–4 weeks
**Primary schedule drivers**: `reimbursement_rate` resolution (Blocker 6), `--mock-llm` CI semantics, lease timeout approval

#### 2.1 — Lease Model (FR-010, FR-011)

1. Implement `AuditLease` with fields: `lease_id`, `owner`, `acquired_at`, `expires_at`, `renewed_at` (all ISO-8601 UTC)
2. Heartbeat renewal interval ≤ `audit_lease_timeout / 3`
3. Missing heartbeat past timeout → `audit_*_failed(timeout)`
4. Per-scope configurable timeout values (requires Reliability Owner approval)
5. Lease timeout independent of and ≤ outer subprocess wall-clock timeout (NFR-001)

#### 2.2 — Retry Budget (FR-012, FR-013)

1. Durable `audit_attempts` counter per scope
2. Provisional defaults: milestone=2, release=1 (normative after calibration per SS8.2)
3. Outer wall-clock ceiling: `max_turns * 120 + 300 s`
4. Audit gate evaluation must complete within ceiling

#### 2.3 — Sprint Executor Integration

1. **Wire `SprintGatePolicy`** into `execute_sprint()` at post-subprocess point (FR-038)
2. **Extend `OutputMonitor`** for audit lease heartbeat events (FR-039)
3. **Wire `TrailingGateRunner`** for phase-scope evaluation with `GateScope.MILESTONE` and `GateScope.RELEASE` (FR-040)
4. **Wire `ShadowGateMetrics`** for shadow mode data collection (FR-041)
5. Expose `--grace-period` CLI flag in sprint commands (FR-042)

#### 2.4 — Audit Gate Derivation (FR-043)

1. `audit_gate_required` per-task: `true` when `Tier == STRICT OR Risk == High OR Critical Path Override == true`
2. Phase-level aggregation: `phase_requires_audit = any(task.audit_gate_required for task in phase.tasks)`
3. Wire into tasklist generator (`cli/tasklist/`) for parsing and emission

#### 2.5 — Gate State Persistence (FR-045)

1. Add `audit` block to `_save_state()` for gate result persistence
2. Artifact version hashes enable freshness validation (FR-016)
3. Stale gate results trigger re-evaluation; staleness recorded in `OverrideRecord`

#### 2.6 — KPI Instrumentation (NFR-017)

1. Lease acquisition/duration → M1
2. Lease timeouts → M7
3. OverrideRecord events → M9
4. All wired before shadow mode activation

#### 2.7 — `reimbursement_rate` Resolution (Blocker 6)

1. Decision: wire as turn-recovery credit OR remove entirely
2. Must be resolved before Phase 2 GO

#### Go/No-Go Criteria

- [ ] NFR-005: All timeout/retry paths terminate deterministically, no deadlocks
- [ ] SC-011: Timeout/retry determinism verified
- [ ] Lease model functional with heartbeat renewal
- [ ] Shadow mode collecting metrics without blocking transitions
- [ ] Blocker 6 (`reimbursement_rate`) resolved
- [ ] Reliability Owner approves per-scope timeout values

---

### Phase 3 — Enforcement: Transition Blocking, TUI, and Override Rules

**Duration**: 2–3 weeks
**Primary schedule drivers**: TUI engineer availability, override policy finalization

> **Note on TUI placement**: If a dedicated TUI engineer is available, TUI work (§3.3) may begin as a parallel workstream in Phase 2, reading the `AuditWorkflowState` enum defined in Phase 1. Default placement is Phase 3 to avoid coordination overhead during integration.

#### 3.1 — Transition Enforcement (FR-001, FR-005, FR-016)

1. Milestone gate: blocks phase completion unless gate passes
2. Release gate: blocks sprint release unless gate passes
3. Current gate result must reference artifact version under evaluation
4. Stale results trigger re-evaluation with staleness in `OverrideRecord`

#### 3.2 — Override Rules (FR-026)

1. Soft-fail (0.50–0.74) overridable at task/milestone scope
2. Hard-fail (≥0.75) never overridable at release tier (LD-3)
3. Override at release scope blocked; task/milestone override requires valid `OverrideRecord` (SC-008)
4. EXEMPT aggregate bypass prohibition enforced (FR-017)

#### 3.3 — TUI Extension (FR-044)

1. Extend phase table to display `AuditWorkflowState` values
2. Release guard blocking "Sprint Complete" unless `audit_release_passed`
3. Operator guidance panel for `audit_*_failed` states

#### 3.4 — Unified Audit Trail

1. `SilentSuccessResult` appears in trail with `failure_class: policy.silent_success` (SC-008)
2. `AuditGateResult` blocks include all three extension blocks when their gates ran
3. Block MUST be written even when `suspicion_score = 0.0` (FR-018)

#### Go/No-Go Criteria

- [ ] SC-006: G-012 after P0-A fixes passes against smoke fixture
- [ ] SC-008: Silent success in audit trail, override enforcement correct
- [ ] SC-014: Transition blocking/override rules enforced per scope
- [ ] SC-016: All 9 blockers closed with owner/deadline

---

### Phase 4 — Promotion: Shadow → Soft → Full Rollout

**Duration**: 4–6 weeks (inclusive of observation windows)
**Primary schedule drivers**: calibration window length, rollout KPI stability, consecutive-window requirement

#### 4.1 — Shadow Mode

1. Gates evaluate but do not block; results logged for calibration
2. Collect data for M13/M14 provisional → normative calibration
3. Recalibrate M1 runtime threshold for phase-scope (NFR-012)
4. Document S2 calibration methodology (SC-007, NFR-013)
5. Minimum observation window determined by Reliability Owner, with a provisional floor of 2 weeks pending calibration data. Reliability Owner may shorten with documented statistical justification.

#### 4.2 — Shadow → Soft Promotion (NFR-011)

**Requires passing**: M1, M4, M5, M7, M9

1. Soft enforcement: gates block with override path available
2. Monitor suspicion rate: warn >5% in 0.30–0.49 range; fail >1% soft/hard-fail (NFR-009)

#### 4.3 — Soft → Full Promotion (NFR-011)

**Requires**: M1–M12 passing for two consecutive windows + rollback drill (M10)

1. Full enforcement: gates block with no override at release scope
2. Provisional KPI defaults (M13, M14) become normative after Reliability Owner approval (NFR-018)

#### 4.4 — Post-Promotion Hardening

1. Review false-positive/false-negative rates from production data
2. Confirm operator workflow clarity — TUI guidance adequate for common failure modes
3. Freeze v1.2.1 scope and open v1.3 backlog for task-scope activation
4. v1.3 handoff document with annotated task-scope transition inventory

#### Go/No-Go Criteria

- [ ] SC-007: S2 calibration documented and approved
- [ ] SC-015: Phase gates pass by KPI criteria + rollback drill
- [ ] NFR-010: Shadow → Soft → Full promotion sequence completed
- [ ] NFR-011: All promotion gate criteria met at each transition

---

## Sequencing Guardrails

These four rules are absolute and override schedule pressure:

1. **Do not start Phase 2 until P0-A fixes are verified** (SC-003, SC-004 passing).
2. **Do not promote to Soft until calibration protocol is approved** by Reliability Owner.
3. **Do not promote to Full until two consecutive KPI windows pass** with M1–M12 criteria met.
4. **Do not expand scope into task gating during v1.2.1** — annotations and deferral markers only.

---

## Risk Assessment and Mitigation

### High-Risk Items

| # | Risk | Mitigation | Owner |
|---|------|-----------|-------|
| R1 | S2 calibration methodology gap — 50ms/10ms thresholds lack empirical basis | Document calibration protocol before soft-phase M14 activation; run shadow data collection before normative thresholds | Reliability Owner |
| R2 | EXEMPT aggregate bypass — all-EXEMPT produces false pass | C-1 normative rule: treat as `policy` failure (FR-017); implemented in Phase 1 | Phase 1 delivery |
| R3 | P0-A defects block G-012 validity — legitimate executions appear empty | Phase 0 fixes with Blocker 9 scheduling; SC-003/SC-004 as hard prerequisites | Phase 0 delivery |
| R4 | Orphaned `execute_phase_tasks()` dead code | Branch (b) defers to v1.3; no activation under pressure | Architectural constraint |
| R5 | Stale gate results allow incorrect transitions | Artifact hash storage in `AuditGateResult`; mandatory freshness validation; re-evaluation on mismatch | Phase 2 delivery |
| R6 | State-machine deadlocks in lease/retry flows | Deterministic timeout transitions; outer wall-clock ceiling; explicit lease expiry handling and retry budget exhaustion tests | Audit/State Machine Engineer |
| R7 | Per-task artifact addressability uncertainty (C3) — v1.3 task-scope path may be structurally blocked | Treat C3 as explicit go/no-go checkpoint in Phase 1; escalate early if outputs not individually addressable | Program Manager |

### Medium-Risk Items

| # | Risk | Mitigation | Owner |
|---|------|-----------|-------|
| R8 | Smoke test CI false positives from timing | Timing is WARN-only, not blocking (by design) | — |
| R9 | Fixture drift breaks content checks | Stability contract + `test_fixture_content_matches_gate_patterns` unit test | QA |
| R10 | D-05 stub sentinel false positives | Explicitly deferred until section-scope filtering | Deferred |
| R11 | `--mock-llm` scope undefined | Blocker 8 + user decision 8 before Phase 2 CI; preserve artifact-absence checks as non-negotiable | Policy Owner |
| R12 | `reimbursement_rate` dead field | Blocker 6: wire-or-remove before Phase 2 GO | TBD |
| R13 | Regex undercoverage in D-03/D-04 | Validate against representative spec corpus; add allowlist/feature flag if authoring conventions diverge | Architect |
| R14 | KPI threshold drift between scopes | Treat task-scope and phase-scope thresholds independently; require fresh calibration rather than inherited defaults | Reliability Owner |

### Governance-Risk Items

| # | Risk | Mitigation | Owner |
|---|------|-----------|-------|
| R15 | Unowned blockers and decisions — no phase GO without named owner + deadline for each blocker | Program Manager tracks closure before each promotion gate | Program Manager |
| R16 | Scope creep into task-gating — implementation work activates task scope in v1.2.1 | Preserve annotations only; reject implementation work that activates task scope; sequencing guardrail #4 | Program Manager |

### Low-Risk Items

| # | Risk | Mitigation | Owner |
|---|------|-----------|-------|
| R17 | Anti-Instincts overlap with D-03/D-04 | Feature flag if Anti-Instincts ships first (NFR-014) | PM |
| R18 | M1/M8 KPI miscalibration | Recalibrate from shadow mode data (NFR-012) | Reliability Owner |

---

## Resource Requirements

### Required Roles

| Role | Responsibilities |
|------|-----------------|
| **Architect / Technical Lead** | Cross-subsystem design, interface contracts, rollout sequencing, module placement decisions |
| **Reliability Owner** | Timeout values, S2 calibration, M1 recalibration, KPI approval, shadow window determination |
| **Policy Owner** | Failure-class taxonomy, override restrictions, `--mock-llm` scope, profile model alignment |
| **CLI / Execution Engineer** | Executor instrumentation, smoke gate, command validation, trailing gate wiring |
| **Audit / State Machine Engineer** | `AuditGateResult`, lease model, retries, persistence, freshness checks |
| **Roadmap / Semantic Validation Engineer** | D-03/D-04, deviation-analysis step, spec inventory |
| **TUI / UX Engineer** | Audit workflow state rendering, operator guidance panels |
| **QA / Validation Engineer** | Regression fixtures, replay stability, deadlock testing, smoke test matrices |
| **Program Manager** | Blocker closure tracking, owner assignments, promotion evidence, go/no-go readiness, C3 escalation |

### New Source Files (~7)

| File | Lines (est.) | Phase |
|------|-------------|-------|
| `silent_success.py` | ~300 | Phase 1 |
| `smoke_gate.py` | ~400 | Phase 1 |
| `fidelity_inventory.py` | ~150 | Phase 1 |
| `audit_gate_models.py` | ~200 | Phase 1 |
| `audit_lease.py` | ~150 | Phase 2 |
| `shadow_metrics.py` | ~100 | Phase 2 |
| `audit_gate_tui.py` | ~150 | Phase 3 |

### New Test Files (~7)

| Test File | Validates |
|-----------|----------|
| `test_silent_success.py` | SC-001, SC-009, FR-024/25/26 |
| `test_smoke_gate.py` | SC-005, SC-006, FR-027/28 |
| `test_fidelity_inventory.py` | SC-002, FR-029/30 |
| `test_audit_gate_models.py` | FR-018/19/20/22/23 |
| `test_audit_lease.py` | FR-010/11, NFR-001/005 |
| `test_transition_enforcement.py` | SC-008, SC-014, FR-016/17 |
| `test_fixture_stability.py` | NFR-003 (fixture content anchors) |

### Internal Dependencies

| Dependency | Location | Phase Needed |
|------------|----------|--------------|
| `GateResult` (existing 2-field) | `cli/audit/evidence_gate.py` | Phase 1 (coexistence) |
| `TrailingGateRunner` | `cli/pipeline/trailing_gate.py` | Phase 2 |
| `GateScope.MILESTONE`, `GateScope.RELEASE` | `cli/pipeline/trailing_gate.py` | Phase 2 |
| `GATE_REGISTRY` | `cli_portify/gates.py` | Phase 1 |
| `SPEC_FIDELITY_GATE` | `cli/roadmap/gates.py` | Phase 1 |
| Sprint executor | `cli/sprint/executor.py` | Phase 2 |
| `OutputMonitor` | `cli/sprint/monitor.py` | Phase 2 |
| Tasklist generator | `cli/tasklist/` | Phase 2 |
| `return-contract.yaml` | Project root | Phase 1 |
| v2.25 artifacts | `.dev/releases/complete/v2.25-cli-portify-cli/` | Phase 1 (tests) |

### External Dependencies

| Dependency | Impact | Mitigation |
|------------|--------|-----------|
| LLM API | Non-mock smoke gate runs | `--mock-llm` mode; unavailability → `transient` failure |
| `sc-smoke-skill/SKILL.md` | Content evidence anchors | Stability contract (NFR-003) |
| `sc-audit-gate-protocol/SKILL.md` | Transition table definition | Created in Phase 2 |
| `sc-tasklist-protocol/SKILL.md` | `audit_gate_required` derivation | Updated in Phase 2 |

---

## Success Criteria and Validation Approach

### Validation Matrix

| Criterion | Phase | Validation Method |
|-----------|-------|-------------------|
| SC-001 (no-op pipeline detection) | P1 | `test_no_op_pipeline_scores_1_0` |
| SC-002 (v2.25 regression) | P1 | `test_run_deterministic_inventory_cli_portify_case` |
| SC-003 (P0-A Fix 1) | P0 | Integration test: `run_portify()` produces artifacts |
| SC-004 (P0-A Fix 2) | P0 | CLI exit code test |
| SC-005 (G-012 known-bad) | P1 | Smoke gate against broken executor |
| SC-006 (G-012 after fix) | P3 | Smoke gate against fixture post-P0-A |
| SC-007 (S2 calibration) | P4 | Document review + Reliability Owner sign-off |
| SC-008 (silent success trail) | P3 | Audit trail inspection + override blocking |
| SC-009 (all-EXEMPT = fail) | P1 | Unit test: zero real steps → policy failure |
| SC-010 (deterministic replay) | P1 | Repeated execution comparison |
| SC-011 (no deadlocks) | P2 | Timeout path analysis + stress test |
| SC-012 (deviation-analysis.md) | P1 | Roadmap pipeline output validation |
| SC-013 (per-task artifacts) | P1 | C3 structural validation |
| SC-014 (transition enforcement) | P3 | Integration test: blocked transitions |
| SC-015 (KPI + rollback drill) | P4 | Shadow/soft/full promotion gates |
| SC-016 (blockers closed) | P3 | Blocker registry audit |

### Concern-Based Validation Grouping

For test strategy planning, success criteria group into five concerns:

- **Foundation** (SC-001, SC-002, SC-003, SC-004, SC-009, SC-010): Core detection and determinism
- **Integration** (SC-005, SC-006, SC-011, SC-012): Cross-subsystem wiring and end-to-end flows
- **Reliability** (SC-007, SC-013): Calibration and structural readiness
- **Governance** (SC-008, SC-014, SC-016): Policy enforcement and audit completeness
- **Rollout** (SC-015): Promotion criteria and production readiness

### Recommended Test Suites

1. **Unit tests**: score bands, regex inventory extraction, failure-class routing, artifact hash freshness logic
2. **Integration tests**: executor instrumentation, smoke gate end-to-end, trailing gate evaluation, tasklist derivation of `audit_gate_required`
3. **Regression tests**: v2.25 spec/roadmap pairs, smoke fixture content anchors, stale gate result rejection
4. **Operational tests**: lease expiry and recovery, retry exhaustion, shadow metric emission, TUI state rendering and operator messaging

---

## Timeline Estimates

Given the **0.92 / HIGH** complexity score and cross-cutting integration density, this roadmap is planned as a **multi-wave delivery**.

| Phase | Duration | Key Schedule Drivers |
|-------|----------|---------------------|
| Phase 0 — Prerequisites | 1–2 weeks | Blocker ownership latency, design ratification |
| Phase 1 — Foundation | 2–3 weeks | C3 resolution, D-03/D-04 regex validation |
| Phase 2 — Integration | 3–4 weeks | `reimbursement_rate` decision, `--mock-llm` semantics, lease timeout approval |
| Phase 3 — Enforcement | 2–3 weeks | TUI engineer availability, override policy finalization |
| Phase 4 — Promotion | 4–6 weeks | Calibration window length, consecutive KPI windows, rollback drill |

**Overall program estimate**: 12–18 weeks (best-case 12, expected 14–16)

---

## Open Decisions Requiring Resolution

| # | Decision | Required By | Assignee |
|---|----------|-------------|----------|
| 1 | Owner assignments for Blockers 5–9 | Phase 0 GO | Program Manager |
| 2 | `audit_lease_timeout` per-scope defaults | Phase 2 | Reliability Owner |
| 3 | `reimbursement_rate` wire-or-remove | Phase 2 GO | TBD |
| 4 | Per-task artifact addressability (C3) | Phase 1 GO | Architect + PM |
| 5 | `--mock-llm` check matrix | Phase 2 | Policy Owner |
| 6 | D-03/D-04 regex generality | Phase 1 | Architect |
| 7 | Anti-Instincts timeline vs D-03/D-04 | Phase 1 | PM |
| 8 | Shadow mode observation window | Phase 4 | Reliability Owner |
| 9 | M1 phase-scope threshold | Phase 4 (shadow) | Reliability Owner |
| 10 | Audit gate time budget fraction | Phase 2 | Reliability Owner |
| 11 | `SilentSuccessConfig` defaults owner | Phase 4 (soft) | PM |
| 12 | Branch (b) reversal escalation timeline | Phase 1 GO | PM |

---

## Architect Recommendations

> These recommendations are guidance for sprint planning, not mandates. Adjust based on current directory structure and team conventions.

1. **Module placement**: Locate `silent_success.py` and `audit_lease.py` under `cli/pipeline/` — these are cross-cutting pipeline concerns. Place `smoke_gate.py` under `cli/cli_portify/` since it tests portify execution. Place `fidelity_inventory.py` under `cli/roadmap/`. Place `audit_gate_models.py` under `cli/pipeline/` or `cli/audit/` depending on existing model conventions.

2. **Resolve C3 before Phase 1 GO**: Per-task artifact addressability is the highest-uncertainty architectural question. If phase subprocess output cannot provide individually addressable per-task artifacts, the audit-gate-required derivation model changes. Do not proceed past Phase 1 without a validated answer.

3. **Shadow mode is non-negotiable**: With a 0.92 complexity score and provisional thresholds throughout, skipping shadow mode would produce immediate false-positive cascades.

4. **Treat the `GateResult` naming collision as a canary**: The existing duplication between `evidence_gate.py` and `manifest_gate.py` indicates the audit subsystem needs a naming convention audit during Phase 1 model design.

5. **D-03/D-04 feature flag is cheap insurance**: Even if Anti-Instincts is months away, the feature flag costs ~10 lines and prevents a forced hotfix if timelines shift.

6. **Assign Reliability Owner immediately**: 4 of 12 open decisions and 3 of 9 blockers require this role. This is the single highest-leverage staffing decision for this release.
