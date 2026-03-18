---
spec_source: "spec-refactor-plan-merged.md"
complexity_score: 0.92
primary_persona: architect
---

# Unified Audit-Gating Roadmap — v1.2.1

## Executive Summary

This roadmap delivers a **multi-scope audit gate framework** (milestone + release) with three behavioral gate extensions: Silent Success Detection, Smoke Test Gate (G-012), and Spec Fidelity Deterministic Checks (D-03/D-04). The system integrates into the existing sprint executor and pipeline gate infrastructure, blocking completion/release transitions unless gates pass.

**Scope**: 47 functional + 18 non-functional requirements across 6 domains (backend, security, CLI, testing, devops, observability). Task-scope gating is explicitly deferred to v1.3.

**Delivery strategy**: 4-phase rollout (Foundation → Integration → Enforcement → Promotion) with go/no-go gates at each transition. Estimated 25+ files changed across sprint executor, cli-portify, roadmap, audit, tasklist, and TUI subsystems.

**Key architectural decision**: All new gate logic builds on the existing `cli/pipeline/` gate substrate (`GateCriteria`, `TrailingGateRunner`, `GateScope`). The new `AuditGateResult` dataclass avoids namespace collision with the existing 2-field `GateResult` in `cli/audit/evidence_gate.py`.

---

## Phase 0: Prerequisites & P0 Defect Fixes

**Duration**: 3–5 days
**Milestone**: P0 blockers resolved, canonical terms defined, dead code retired

### 0.1 — P0-A Defect Fixes (Blockers 9)

1. **Fix Defect 1** (FR-031): `run_portify()` in `cli/cli_portify/executor.py` must pass `step_runner` to `PortifyExecutor`; create `STEP_DISPATCH` mapping from step IDs to imported step functions
2. **Fix Defect 2** (FR-032): `cli/cli_portify/commands.py` must call `validate_portify_config()` before `run_portify()`; exit non-zero on validation errors
3. Verify SC-003 and SC-004 pass after fixes

### 0.2 — Dead Code Retirement (FR-046)

1. Retire `_apply_resume_after_spec_patch()` from roadmap executor
2. Retire `_find_qualifying_deviation_files()` from roadmap executor
3. Confirm no live references via `find_referencing_symbols`

### 0.3 — Canonical Term Definition (FR-008)

1. Define and document 6 terms in glossary: `AuditLease`, `audit_lease_timeout`, `max_turns`, `Critical Path Override`, `audit_gate_required`, `audit_attempts`
2. Add `[v1.3 -- deferred]` markers to all task-scope transitions in SS4.1 (FR-009)

### 0.4 — Locked Decision Registration (FR-006)

1. Register locked decision #6 in SS2.1: v1.2.1 = phase-scope + sprint-scope only

### Go/No-Go Criteria
- [ ] SC-003: `run_portify()` produces intermediate artifacts
- [ ] SC-004: `commands.py` exits non-zero on validation errors
- [ ] Dead code retired with zero remaining references
- [ ] All 6 canonical terms documented

---

## Phase 1: Foundation — Data Models, Detectors & Gates

**Duration**: 10–14 days
**Milestone**: All three behavioral gate extensions pass unit tests; standalone emission works

### 1.1 — Core Data Models

1. **`AuditGateResult` dataclass** (FR-022, FR-023):
   - Disambiguated name to avoid collision with `cli/audit/evidence_gate.py::GateResult`
   - Include `artifacts` block with SHA-256 version hashes for freshness validation
   - Include `silent_success_audit` block (FR-018): `suspicion_score`, per-signal scores (S1-S3), `band`, `diagnostics`, `gate_decision`, `thresholds`
   - Include `smoke_test_result` block (FR-019): `gate_id`, `fixture_path`, `elapsed_s`, `artifacts_found`, `checks_passed`, `checks_failed`, `failure_class`, `tmpdir_cleaned`
   - Include `fidelity_deterministic` block (FR-020): dispatch tables/functions found/preserved booleans, checks run/excluded lists

2. **Failure class taxonomy** (FR-014):
   - Extend `policy` failure class with sub-types: `policy.silent_success`, `policy.smoke_failure` (`.timing`, `.artifact_absence`, `.content_evidence`), `policy.fidelity_deterministic`

3. **Outcome enum extension** (FR-035):
   - Add `PortifyOutcome.SILENT_SUCCESS_SUSPECTED` and `PortifyOutcome.SUSPICIOUS_SUCCESS` to `cli/cli_portify/models.py`

### 1.2 — Silent Success Detector (FR-002, FR-024, FR-025, FR-033)

1. Implement `silent_success.py` (~300 lines) in `cli/pipeline/` or `cli/audit/`:
   - `FileSnapshot`, `StepTrace`, `SilentSuccessConfig`, `SilentSuccessDetector`, `SilentSuccessResult`, `SilentSuccessError`
   - Signal suite: S1 (Artifact Content, 0.35), S2 (Execution Trace, 0.35), S3 (Output Freshness, 0.30)
   - Composite formula: `suspicion_score = ((1-S1) × 0.35) + ((1-S2) × 0.35) + ((1-S3) × 0.30)`
   - Bands: 0.0-0.29 pass, 0.30-0.49 warn, 0.50-0.74 soft-fail, 0.75-1.00 hard-fail
2. `SilentSuccessConfig(enabled=False)` for test harnesses (NFR-002)
3. All-EXEMPT/SKIPPED with zero real steps = `policy` failure unless `--dry-run` (FR-007, FR-017)
4. Absence of `silent_success_audit` block = `failed` at STRICT tier (NFR-004)

### 1.3 — Smoke Test Gate G-012 (FR-003, FR-027, FR-037)

1. Implement `smoke_gate.py` (~400 lines):
   - `SmokeTestConfig`, `SmokeTestResult` dataclasses
   - `run_smoke_test()` function
   - Check hierarchy: timing (<5s = WARN only), artifact absence (ERROR, blocking), content evidence (ERROR, blocking)
   - Constants: `SMOKE_NOOP_CEILING_S=5`, `SMOKE_MIN_REAL_EXECUTION_S=10`, `SMOKE_TIMEOUT_S=600`
2. Register G-012 as `smoke-test` in `GATE_REGISTRY` (cli_portify/gates.py) after G-011
3. Failure routing (FR-015): API/network errors → `transient`; timing/artifact/content → `policy.smoke_failure.*`
4. `--mock-llm` mode for CI (FR-028)
5. `tmpdir_cleaned: bool` for AC-006 compliance (NFR-015)

### 1.4 — Spec Fidelity Deterministic Checks D-03/D-04 (FR-004, FR-029, FR-030, FR-036)

1. Implement `fidelity_inventory.py` (~150 lines):
   - `SpecInventory` dataclass, `build_spec_inventory()`
   - `_DISPATCH_TABLE_PATTERN`: regex for `UPPER_CASE_NAME = {` or `dict(`
   - `_STEP_DISPATCH_CALL`: regex for `_run_*()` or `step_result =`
   - `_DEP_ARROW_PATTERN` regex
2. Wire D-03 and D-04 into `SPEC_FIDELITY_GATE` in `cli/roadmap/gates.py`
3. Deterministic checks override LLM output (FR-021): `dispatch_tables_preserved: false` OR `dispatch_functions_preserved: false` → gate failed regardless of `high_severity_count`
4. Feature flag consideration for Anti-Instincts overlap (NFR-014)

### 1.5 — Standalone Emission (P0-B)

1. Instrument executor with `_step_traces`, `time.monotonic()` wrapping (FR-034)
2. `snapshot_pre_run()` call before execution
3. Post-loop detector invocation
4. `SilentSuccessResult` standalone emission to `return-contract.yaml` (FR-002)

### 1.6 — Deviation Analysis Integration (FR-047)

1. Wire `deviation-analysis` step into roadmap `_build_steps()` after `spec-fidelity`
2. Update `_get_all_step_ids()`
3. Write `build_deviation_analysis_prompt()`

### Go/No-Go Criteria
- [ ] SC-001: No-op pipeline → `suspicion_score = 1.0`, `SILENT_SUCCESS_SUSPECTED`, non-zero exit
- [ ] SC-002: v2.25 regression → `dispatch_tables_preserved: false`, gate rejects
- [ ] SC-005: G-012 against known-bad executor fails correctly
- [ ] SC-009: All-EXEMPT registry → `failed(policy.silent_success)`
- [ ] SC-010: Deterministic replay stability verified
- [ ] SC-012: Roadmap pipeline produces `deviation-analysis.md`
- [ ] SC-013: C3 validation — per-task artifacts individually addressable
- [ ] NFR-006: Same input → same gate result

---

## Phase 2: Integration — State Machine, Leases & Executor Wiring

**Duration**: 10–14 days
**Milestone**: Audit gates operational in shadow mode within sprint executor

### 2.1 — Lease Model (FR-010, FR-011)

1. Implement `AuditLease` with fields: `lease_id`, `owner`, `acquired_at`, `expires_at`, `renewed_at` (all ISO-8601 UTC)
2. Heartbeat renewal interval ≤ `audit_lease_timeout / 3`
3. Missing heartbeat past timeout → `audit_*_failed(timeout)`
4. Per-scope configurable timeout values (requires Reliability Owner approval)
5. Lease timeout independent of and ≤ outer subprocess wall-clock timeout (NFR-001)

### 2.2 — Retry Budget (FR-012, FR-013)

1. Durable `audit_attempts` counter per scope
2. Provisional defaults: milestone=2, release=1 (normative after calibration per SS8.2)
3. Outer wall-clock ceiling: `max_turns * 120 + 300 s`
4. Audit gate evaluation must complete within ceiling

### 2.3 — Sprint Executor Integration

1. **Wire `SprintGatePolicy`** into `execute_sprint()` at post-subprocess point (FR-038)
   - Sprint executor already imports `TrailingGatePolicy` and `TrailingGateResult` from pipeline
2. **Extend `OutputMonitor`** for audit lease heartbeat events (FR-039)
3. **Wire `TrailingGateRunner`** for phase-scope evaluation with `GateScope.MILESTONE` and `GateScope.RELEASE` (FR-040)
4. **Wire `ShadowGateMetrics`** for shadow mode data collection (FR-041)
5. Expose `--grace-period` CLI flag in sprint commands (FR-042)

### 2.4 — Audit Gate Derivation (FR-043)

1. `audit_gate_required` per-task: `true` when `Tier == STRICT OR Risk == High OR Critical Path Override == true`
2. Phase-level aggregation: `phase_requires_audit = any(task.audit_gate_required for task in phase.tasks)`
3. Wire into tasklist generator (`cli/tasklist/`) for parsing and emission

### 2.5 — Gate State Persistence (FR-045)

1. Add `audit` block to `_save_state()` for gate result persistence
2. Artifact version hashes enable freshness validation (FR-016)
3. Stale gate results trigger re-evaluation; staleness recorded in `OverrideRecord`

### 2.6 — KPI Instrumentation (NFR-017)

1. Lease acquisition/duration → M1
2. Lease timeouts → M7
3. OverrideRecord events → M9
4. All wired before shadow mode activation

### 2.7 — `reimbursement_rate` Resolution (Blocker 6)

1. Decision: wire as turn-recovery credit OR remove entirely
2. Must be resolved before Phase 2 GO

### Go/No-Go Criteria
- [ ] NFR-005: All timeout/retry paths terminate deterministically, no deadlocks
- [ ] SC-011: Timeout/retry determinism verified
- [ ] Lease model functional with heartbeat renewal
- [ ] Shadow mode collecting metrics without blocking transitions
- [ ] Blocker 6 (`reimbursement_rate`) resolved
- [ ] Reliability Owner approves per-scope timeout values

---

## Phase 3: Enforcement — Transition Blocking & TUI

**Duration**: 7–10 days
**Milestone**: Gates enforce transition blocking at milestone + release scope

### 3.1 — Transition Enforcement (FR-001, FR-005, FR-016)

1. Milestone gate: blocks phase completion unless gate passes
2. Release gate: blocks sprint release unless gate passes
3. Current gate result must reference artifact version under evaluation
4. Stale results trigger re-evaluation with staleness in `OverrideRecord`

### 3.2 — Override Rules (FR-026)

1. Soft-fail (0.50-0.74) overridable at task/milestone scope
2. Hard-fail (≥0.75) never overridable at release tier (LD-3)
3. Override at release scope blocked; task/milestone override requires valid `OverrideRecord` (SC-008)
4. EXEMPT aggregate bypass prohibition enforced (FR-017)

### 3.3 — TUI Extension (FR-044)

1. Extend phase table to display `AuditWorkflowState` values
2. Release guard blocking "Sprint Complete" unless `audit_release_passed`
3. Operator guidance panel for `audit_*_failed` states

### 3.4 — Unified Audit Trail

1. `SilentSuccessResult` appears in trail with `failure_class: policy.silent_success` (SC-008)
2. `AuditGateResult` blocks include all three extension blocks when their gates ran
3. Block MUST be written even when `suspicion_score = 0.0` (FR-018)

### Go/No-Go Criteria
- [ ] SC-006: G-012 after P0-A fixes passes against smoke fixture
- [ ] SC-008: Silent success in audit trail, override enforcement correct
- [ ] SC-014: Transition blocking/override rules enforced per scope
- [ ] SC-016: All 9 blockers closed with owner/deadline

---

## Phase 4: Promotion — Shadow → Soft → Full Rollout

**Duration**: 14–21 days (plus observation windows)
**Milestone**: Full production enforcement with calibrated KPIs

### 4.1 — Shadow Mode

1. Gates evaluate but do not block; results logged for calibration
2. Collect data for M13/M14 provisional → normative calibration
3. Recalibrate M1 runtime threshold for phase-scope (NFR-012)
4. Document S2 calibration methodology (SC-007, NFR-013)

### 4.2 — Shadow → Soft Promotion (NFR-011)

**Requires passing**: M1, M4, M5, M7, M9

1. Soft enforcement: gates block with override path available
2. Monitor suspicion rate: warn >5% in 0.30-0.49 range; fail >1% soft/hard-fail (NFR-009)

### 4.3 — Soft → Full Promotion (NFR-011)

**Requires**: M1-M12 passing for two consecutive windows + rollback drill (M10)

1. Full enforcement: gates block with no override at release scope
2. Provisional KPI defaults (M13, M14) become normative after Reliability Owner approval (NFR-018)

### Go/No-Go Criteria
- [ ] SC-007: S2 calibration documented and approved
- [ ] SC-015: Phase gates pass by KPI criteria + rollback drill
- [ ] NFR-010: Shadow → Soft → Full promotion sequence completed
- [ ] NFR-011: All promotion gate criteria met at each transition

---

## Risk Assessment & Mitigation

### HIGH Risks

| # | Risk | Mitigation | Owner |
|---|------|-----------|-------|
| R1 | S2 calibration methodology gap — 50ms/10ms thresholds lack empirical basis | Blocker 7: document calibration protocol before soft-phase M14 activation | Reliability Owner [TBD] |
| R2 | EXEMPT aggregate bypass — all-EXEMPT produces false pass | C-1 normative rule: treat as `policy` failure (FR-017) | Implemented in Phase 1 |
| R3 | P0-A defects block G-012 validity | Phase 0 fixes with Blocker 9 scheduling | Phase 0 delivery |
| R4 | Orphaned `execute_phase_tasks()` dead code | Branch (b) defers to v1.3; no activation under pressure | Architectural constraint |

### MEDIUM Risks

| # | Risk | Mitigation | Owner |
|---|------|-----------|-------|
| R5 | Smoke test CI false positives from timing | Timing is WARN-only, not blocking | By design |
| R6 | Fixture drift breaks content checks | Stability contract + `test_fixture_content_matches_gate_patterns` unit test | QA |
| R7 | D-05 stub sentinel false positives | Explicitly deferred until section-scope filtering | Deferred |
| R8 | `--mock-llm` scope undefined | Blocker 8 + user decision 8 before Phase 2 CI | Policy Owner [TBD] |
| R9 | `reimbursement_rate` dead field | Blocker 6: wire-or-remove before Phase 2 GO | [TBD] |
| R10 | Per-task artifact addressability (C3) | Phase 1 go/no-go validation; escalation path defined | Program Manager [TBD] |

### LOW Risks

| # | Risk | Mitigation | Owner |
|---|------|-----------|-------|
| R11 | Anti-Instincts overlap with D-03/D-04 | Feature flag if Anti-Instincts ships first | NFR-014 |
| R12 | M1/M8 KPI miscalibration | Recalibrate from shadow mode data | NFR-012 |

---

## Resource Requirements & Dependencies

### Internal Dependencies (Must Exist Before Integration)

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

### Roles Required (Open Questions 1)

- **Reliability Owner**: Timeout values, S2 calibration, M1 recalibration, KPI approval
- **Policy Owner**: Override rules, `--mock-llm` scope, profile model
- **Tasklist Owner**: `audit_gate_required` field integration
- **Program Manager**: C3 escalation, blocker deadline enforcement

### New Files (~7)

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

---

## Success Criteria Validation Matrix

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

---

## Open Decisions Requiring Resolution

These must be resolved by the indicated phase to avoid blocking:

| # | Decision | Required By | Assignee |
|---|----------|-------------|----------|
| 1 | Owner assignments for Blockers 5-9 | Phase 0 GO | Program Manager |
| 2 | `audit_lease_timeout` per-scope defaults | Phase 2 | Reliability Owner |
| 3 | `reimbursement_rate` wire-or-remove | Phase 2 GO | [TBD] |
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

1. **Locate new modules under `cli/pipeline/`** for silent success and lease model — these are cross-cutting pipeline concerns, not audit-specific. The smoke gate belongs in `cli/cli_portify/` since it tests portify execution. Fidelity inventory belongs in `cli/roadmap/`.

2. **Resolve C3 (per-task artifact addressability) before Phase 1 GO** — this is the highest-uncertainty architectural question. If phase subprocess output cannot provide individually addressable per-task artifacts, the entire audit-gate-required derivation model changes. Do not proceed past Phase 1 without a validated answer.

3. **Shadow mode is non-negotiable** — with a 0.92 complexity score and provisional thresholds throughout, skipping shadow mode would produce immediate false-positive cascades in production. Plan for a minimum 2-week shadow observation window.

4. **Treat the `GateResult` naming collision as a canary** — the existing duplication between `evidence_gate.py` and `manifest_gate.py` indicates the audit subsystem needs a naming convention audit. Consider this during Phase 1 model design.

5. **D-03/D-04 feature flag is cheap insurance** — even if Anti-Instincts is months away, the feature flag costs ~10 lines and prevents a forced hotfix if timelines shift.

6. **Assign Reliability Owner immediately** — 4 of 12 open decisions and 3 of 9 blockers require this role. This is the single highest-leverage staffing decision for this release.
