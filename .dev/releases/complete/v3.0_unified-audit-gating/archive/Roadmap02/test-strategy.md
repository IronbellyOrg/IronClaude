

---
complexity_class: HIGH
validation_philosophy: continuous-parallel
validation_milestones: 5
work_milestones: 5
interleave_ratio: "1:1"
major_issue_policy: stop-and-fix
---

## Issue Classification

| Severity | Action | Gate Impact |
|----------|--------|-------------|
| CRITICAL | Stop-and-fix immediately | Blocks current phase |
| MAJOR | Stop-and-fix before next phase | Blocks next phase |
| MINOR | Track and fix in next sprint | No gate impact |
| COSMETIC | Backlog | No gate impact |

---

## 1. Validation Milestones Mapped to Roadmap Phases

Each roadmap phase (P0–P4) receives a paired validation milestone (V0–V4) executed at phase completion before the go/no-go gate.

| Validation Milestone | Roadmap Phase | Gate Focus | Key Success Criteria |
|---------------------|---------------|------------|---------------------|
| **V0** | P0 — Prerequisites & P0 Defect Fixes | Defect verification, dead code retirement, governance closure | SC-003, SC-004, FR-046 |
| **V1** | P1 — Foundation | Core detection correctness, deterministic replay, standalone emission | SC-001, SC-002, SC-005, SC-009, SC-010, SC-012, SC-013 |
| **V2** | P2 — Integration | Cross-subsystem wiring, lease/retry determinism, shadow readiness | SC-011, NFR-005, Blocker 6 resolved |
| **V3** | P3 — Enforcement | Transition blocking, override rules, TUI rendering, audit trail completeness | SC-006, SC-008, SC-014, SC-016 |
| **V4** | P4 — Promotion | KPI stability, rollback drill, calibration sign-off, production hardening | SC-007, SC-015, NFR-010, NFR-011 |

---

## 2. Test Categories

### 2.1 Unit Tests

| Test Area | Files Under Test | Key Assertions |
|-----------|-----------------|----------------|
| Suspicion score calculation | `silent_success.py` | Composite formula correctness, band boundaries (0.29/0.30, 0.49/0.50, 0.74/0.75), weight sum = 1.0 |
| Signal suite S1/S2/S3 | `silent_success.py` | Individual signal scoring, edge cases (empty artifacts, zero traces, stale timestamps) |
| Failure class taxonomy | `audit_gate_models.py` | `policy.silent_success`, `policy.smoke_failure.*`, `policy.fidelity_deterministic` correctly instantiated |
| Regex inventory extraction | `fidelity_inventory.py` | `_DISPATCH_TABLE_PATTERN` matches `UPPER_CASE = {` and `dict()`; `_STEP_DISPATCH_CALL` matches `_run_*()` and `step_result =` |
| D-03/D-04 deterministic override | `fidelity_inventory.py` | `dispatch_tables_preserved: false` → gate failed regardless of `high_severity_count` |
| Artifact hash freshness | `audit_gate_models.py` | SHA-256 hash comparison, stale detection logic |
| Smoke test check hierarchy | `smoke_gate.py` | Timing < 5s = WARN only; artifact absence = ERROR; content evidence = ERROR |
| Smoke test constants | `smoke_gate.py` | `SMOKE_NOOP_CEILING_S=5`, `SMOKE_MIN_REAL_EXECUTION_S=10`, `SMOKE_TIMEOUT_S=600` |
| `AuditGateResult` schema | `audit_gate_models.py` | All three extension blocks present, required fields populated, naming disambiguation from `GateResult` |
| Outcome enum extension | `cli/cli_portify/models.py` | `SILENT_SUCCESS_SUSPECTED` and `SUSPICIOUS_SUCCESS` values exist and are distinct |
| `SilentSuccessConfig` disable | `silent_success.py` | `enabled=False` bypasses detection cleanly |
| All-EXEMPT detection | `silent_success.py` | Zero real steps without `--dry-run` → `policy` failure |
| Lease field validation | `audit_lease.py` | ISO-8601 UTC format enforcement, heartbeat interval ≤ timeout/3 |
| Retry budget counter | `audit_lease.py` | Durable counter increments, budget exhaustion produces terminal state |
| `audit_gate_required` derivation | tasklist generator | `Tier == STRICT OR Risk == High OR Critical Path Override == true` → `true` |

### 2.2 Integration Tests

| Test Area | Components Involved | Key Assertions |
|-----------|-------------------|----------------|
| Executor instrumentation | `executor.run()` + `SilentSuccessDetector` | `_step_traces` populated, `time.monotonic()` wrapping active, `snapshot_pre_run()` called |
| Standalone emission (P0-B) | Executor → `return-contract.yaml` | `SilentSuccessResult` block emitted before `_emit_return_contract()` |
| Sprint executor wiring | `execute_sprint()` + `SprintGatePolicy` | Gate evaluation triggered at post-subprocess point |
| `OutputMonitor` heartbeat | `OutputMonitor` + lease model | Heartbeat events parsed as distinct event class |
| `TrailingGateRunner` scopes | `TrailingGateRunner` + `GateScope.MILESTONE/RELEASE` | Phase-scope and release-scope evaluation paths exercised |
| G-012 registration | `GATE_REGISTRY` + `smoke_gate.py` | G-012 registered after G-011, invoked in gate sequence |
| D-03/D-04 in `SPEC_FIDELITY_GATE` | `roadmap/gates.py` + `fidelity_inventory.py` | Check functions wired and invoked during spec fidelity evaluation |
| Deviation analysis step | `_build_steps()` + `_get_all_step_ids()` | Step appears after `spec-fidelity`, `deviation-analysis.md` produced |
| Tasklist `audit_gate_required` | Tasklist generator → phase files | Per-task flag emitted, phase-level aggregation correct |
| Gate state persistence | `_save_state()` + audit block | Gate results survive persistence round-trip |
| Lease timeout → failure | Lease model + executor | Missing heartbeat past timeout → `audit_*_failed(timeout)` |
| Wall-clock ceiling | Retry budget + outer timeout | Evaluation terminates within `max_turns * 120 + 300 s` |

### 2.3 Regression Tests

| Test Area | Fixtures Required | Key Assertions |
|-----------|------------------|----------------|
| v2.25 dispatch table regression | `.dev/releases/complete/v2.25-cli-portify-cli/` spec + roadmap | `dispatch_tables_preserved: false`, `dispatch_functions_preserved: false`, gate rejects (SC-002) |
| Smoke fixture content anchors | `sc-smoke-skill/SKILL.md` | `InputValidator`, `DataProcessor`, `OutputFormatter` present (`test_fixture_content_matches_gate_patterns`) |
| Stale gate result rejection | Persisted gate result with outdated artifact hash | Re-evaluation triggered, staleness recorded in `OverrideRecord` |
| Deterministic replay | Identical input executed twice | Byte-identical `AuditGateResult` output (SC-010, NFR-006) |
| No-op pipeline detection | Executor with no `step_runner` | `suspicion_score = 1.0`, `SILENT_SUCCESS_SUSPECTED`, non-zero exit (SC-001) |

### 2.4 End-to-End Tests

| Test Area | Scope | Key Assertions |
|-----------|-------|----------------|
| Full pipeline no-op detection | CLI invocation → `return-contract.yaml` | Complete flow from executor through detector to contract emission |
| G-012 against known-bad executor | CLI + broken executor + fixture | Fails with both `policy.smoke_failure.timing` AND `policy.smoke_failure.artifact_absence` (SC-005) |
| G-012 after P0-A fixes | CLI + fixed executor + fixture | All checks pass (SC-006) |
| Transition blocking end-to-end | Sprint executor + gates + TUI | Phase completion blocked on gate failure; release blocked on gate failure |
| Shadow mode full cycle | Gates evaluate + metrics emitted + no blocking | KPI data collected without transition interference |
| Override flow | Soft-fail + override attempt | Task/milestone override accepted with `OverrideRecord`; release override rejected |
| `--mock-llm` CI flow | G-012 + mock mode | Gate evaluates without LLM API; artifact-absence checks remain active |

### 2.5 Acceptance Tests

| Test Area | Acceptance Criteria | Owner |
|-----------|-------------------|-------|
| P0-A defect resolution | `run_portify()` produces intermediate artifacts (SC-003); CLI exits non-zero on validation errors (SC-004) | Phase 0 delivery |
| Silent success blocks release | No-op pipeline cannot reach "Sprint Complete" | QA |
| Spec fidelity blocks release | Missing dispatch tables block gate regardless of LLM output | QA |
| Smoke gate blocks release | Artifact-absent execution blocked at release tier | QA |
| Override scoping | Release-scope override impossible for hard-fail; task/milestone override requires `OverrideRecord` | Policy Owner |
| TUI operator guidance | `audit_*_failed` states show actionable guidance panel | TUI Engineer + QA |
| Rollback drill | Full rollback from Full → Soft → Shadow completes successfully | Reliability Owner |

### 2.6 Operational / Stress Tests

| Test Area | Method | Key Assertions |
|-----------|--------|----------------|
| Lease expiry and recovery | Simulate heartbeat loss | Timeout transition fires, retry budget decremented, recovery on next attempt |
| Retry exhaustion | Exhaust `audit_attempts` budget | Terminal failure state, no infinite retry loops |
| Deadlock detection | Concurrent lease acquisition + timeout + retry | All paths terminate (NFR-005), no hung states |
| Shadow metric emission | Shadow mode with known inputs | M1, M7, M9 metrics emitted to instrumentation sink |
| TUI state rendering | Rapid state transitions | `AuditWorkflowState` values render without flicker or stale display |

---

## 3. Test-Implementation Interleaving Strategy

### Ratio Justification

**Complexity class HIGH → 1:1 interleave ratio**. Every implementation phase receives a full validation milestone before the go/no-go gate permits progression. This is non-negotiable given:

- **0.92 complexity score** with cross-cutting concerns spanning 6 subsystems
- **State machine with lease/heartbeat/retry** — correctness failures compound across phases
- **Deterministic gate semantics** — silent regressions in Phase 1 would invalidate all Phase 2+ integration work
- **Provisional thresholds** throughout — validation surfaces miscalibration before enforcement

### Interleaving Schedule

```
P0 (Implement) → V0 (Validate) → GO/NO-GO
P1 (Implement) → V1 (Validate) → GO/NO-GO
P2 (Implement) → V2 (Validate) → GO/NO-GO
P3 (Implement) → V3 (Validate) → GO/NO-GO
P4 (Implement) → V4 (Validate) → GO/NO-GO
```

### Within-Phase Test Cadence

Tests are written **concurrently with implementation**, not after. Specifically:

- **Unit tests**: Written alongside each module (TDD where appropriate — especially for `silent_success.py` signal math and `fidelity_inventory.py` regex patterns)
- **Integration tests**: Written as soon as integration points are wired (e.g., executor instrumentation tests written with FR-034)
- **Regression tests**: Prepared during Phase 0 using v2.25 fixtures; executed from Phase 1 onward
- **E2E tests**: Written in the phase where the full path becomes testable (G-012 E2E in Phase 1 for known-bad, Phase 3 for post-fix)

---

## 4. Risk-Based Test Prioritization

### Priority 1 — CRITICAL (Test First, Block on Failure)

| Risk | Test Priority Rationale | When |
|------|------------------------|------|
| **R3: P0-A defects block G-012** | If defects aren't fixed and verified, all downstream smoke testing is invalid | V0 — must pass before P1 starts |
| **R2: EXEMPT aggregate bypass** | False-pass on all-EXEMPT is a silent security hole in the gate system | V1 — `test_all_exempt_produces_policy_failure` |
| **R6: State machine deadlocks** | Deadlocks in lease/retry are unrecoverable in production | V2 — stress tests for all timeout/retry paths |
| **R5: Stale gate results** | Stale results allowing incorrect transitions defeats the entire gating purpose | V2 — freshness validation integration test |

### Priority 2 — HIGH (Test Early, Major Issue if Failing)

| Risk | Test Priority Rationale | When |
|------|------------------------|------|
| **R1: S2 calibration gap** | Uncalibrated thresholds produce false positives in production | V1 — deterministic replay; V4 — calibration review |
| **R4: Orphaned dead code** | Accidental activation under pressure creates undefined behavior | V0 — verify zero references after retirement |
| **R7: C3 per-task artifact addressability** | Structural blocker for task-scope path in v1.3 | V1 — explicit C3 validation checkpoint |
| **R9: `reimbursement_rate` dead field** | Unresolved dead field creates maintenance confusion | V2 — verify resolution (wired or removed) |

### Priority 3 — MEDIUM (Test in Phase, Minor Issue if Failing)

| Risk | Test Priority Rationale | When |
|------|------------------------|------|
| **R6: Fixture drift** | Content anchor breaks are caught by unit test | V1 — `test_fixture_content_matches_gate_patterns` |
| **R8: Smoke test CI false positives** | Timing-as-WARN design mitigates; verify in CI | V1 — verify timing is WARN-only |
| **R11: `--mock-llm` scope** | Must be defined before Phase 2 CI | V2 — mock mode test matrix |
| **R13: Regex undercoverage** | D-03/D-04 patterns may miss edge cases | V1 — test against representative spec corpus |

### Priority 4 — LOW (Test When Convenient)

| Risk | Test Priority Rationale | When |
|------|------------------------|------|
| **R17: Anti-Instincts overlap** | Feature flag is cheap insurance; test flag toggle | V1 — feature flag unit test |
| **R18: M1/M8 KPI miscalibration** | Addressed by shadow mode recalibration | V4 — verify recalibrated thresholds |

---

## 5. Acceptance Criteria per Milestone

### V0 — Prerequisites Validated

| ID | Criterion | Method | Severity if Failing |
|----|-----------|--------|-------------------|
| V0-1 | SC-003 passes: `run_portify()` produces intermediate artifacts | Integration test | CRITICAL |
| V0-2 | SC-004 passes: `commands.py` exits non-zero on validation errors | CLI exit code test | CRITICAL |
| V0-3 | `_apply_resume_after_spec_patch()` has zero references | `find_referencing_symbols` | MAJOR |
| V0-4 | `_find_qualifying_deviation_files()` has zero references | `find_referencing_symbols` | MAJOR |
| V0-5 | 6 canonical terms documented in spec glossary | Document review | MAJOR |
| V0-6 | All Phase 1 prerequisites have named owners and deadlines | Registry check | MAJOR |
| V0-7 | v1.2.1 scope boundaries unambiguous (task-scope deferred) | Document review | MAJOR |

### V1 — Foundation Validated

| ID | Criterion | Method | Severity if Failing |
|----|-----------|--------|-------------------|
| V1-1 | SC-001: No-op pipeline → `suspicion_score = 1.0`, non-zero exit | Unit + E2E test | CRITICAL |
| V1-2 | SC-002: v2.25 regression → `dispatch_tables_preserved: false`, gate rejects | Regression test | CRITICAL |
| V1-3 | SC-005: G-012 against known-bad executor fails correctly | E2E test | CRITICAL |
| V1-4 | SC-009: All-EXEMPT → `failed(policy.silent_success)` | Unit test | CRITICAL |
| V1-5 | SC-010: Deterministic replay — identical results | Regression test | CRITICAL |
| V1-6 | SC-012: `deviation-analysis.md` produced | Pipeline output test | MAJOR |
| V1-7 | SC-013: C3 per-task artifacts individually addressable | Structural validation | MAJOR (escalate if failing) |
| V1-8 | NFR-006: Same input → same gate result | Deterministic replay | CRITICAL |
| V1-9 | `AuditGateResult` has no naming collision with existing `GateResult` | Import/instantiation test | MAJOR |
| V1-10 | All three extension blocks schema-valid | Schema validation test | MAJOR |
| V1-11 | `SilentSuccessConfig(enabled=False)` disables detection | Unit test | MINOR |
| V1-12 | Fixture stability test passes | `test_fixture_content_matches_gate_patterns` | MAJOR |
| V1-13 | Standalone emission to `return-contract.yaml` complete | Integration test | MAJOR |

### V2 — Integration Validated

| ID | Criterion | Method | Severity if Failing |
|----|-----------|--------|-------------------|
| V2-1 | NFR-005: All timeout/retry paths terminate, no deadlocks | Stress test + path analysis | CRITICAL |
| V2-2 | SC-011: Timeout/retry determinism verified | Stress test | CRITICAL |
| V2-3 | Lease heartbeat renewal functional | Integration test | CRITICAL |
| V2-4 | Missing heartbeat → `audit_*_failed(timeout)` | Integration test | CRITICAL |
| V2-5 | Shadow mode collects metrics without blocking | E2E test | CRITICAL |
| V2-6 | Blocker 6 (`reimbursement_rate`) resolved | Code review | MAJOR |
| V2-7 | `SprintGatePolicy` wired at correct integration point | Integration test | MAJOR |
| V2-8 | `OutputMonitor` handles heartbeat events | Integration test | MAJOR |
| V2-9 | `TrailingGateRunner` evaluates at MILESTONE and RELEASE scope | Integration test | MAJOR |
| V2-10 | KPI instrumentation (M1, M7, M9) emitting data | Instrumentation test | MAJOR |
| V2-11 | Wall-clock ceiling enforced | Timeout test | MAJOR |
| V2-12 | `audit_gate_required` derivation correct in tasklist output | Integration test | MAJOR |
| V2-13 | Gate state persists across `_save_state()` round-trip | Persistence test | MAJOR |

### V3 — Enforcement Validated

| ID | Criterion | Method | Severity if Failing |
|----|-----------|--------|-------------------|
| V3-1 | SC-014: Milestone gate blocks phase completion on failure | E2E test | CRITICAL |
| V3-2 | SC-014: Release gate blocks sprint release on failure | E2E test | CRITICAL |
| V3-3 | SC-008: `SilentSuccessResult` in audit trail with correct `failure_class` | Audit trail inspection | CRITICAL |
| V3-4 | SC-008: Release-scope override blocked for hard-fail | Override attempt test | CRITICAL |
| V3-5 | SC-008: Task/milestone override requires valid `OverrideRecord` | Override flow test | MAJOR |
| V3-6 | SC-006: G-012 passes against smoke fixture post-P0-A | E2E test | MAJOR |
| V3-7 | SC-016: All 9 blockers closed with owner/deadline | Registry audit | MAJOR |
| V3-8 | Stale gate result triggers re-evaluation | Staleness test | MAJOR |
| V3-9 | TUI displays `AuditWorkflowState` correctly | TUI rendering test | MINOR |
| V3-10 | TUI blocks "Sprint Complete" unless `audit_release_passed` | TUI interaction test | MAJOR |
| V3-11 | Operator guidance panel renders for `audit_*_failed` | TUI rendering test | MINOR |
| V3-12 | Audit block written even when `suspicion_score = 0.0` | Unit test | MAJOR |

### V4 — Promotion Validated

| ID | Criterion | Method | Severity if Failing |
|----|-----------|--------|-------------------|
| V4-1 | SC-007: S2 calibration documented and approved | Document review + sign-off | CRITICAL |
| V4-2 | SC-015: Shadow → Soft promotion criteria (M1, M4, M5, M7, M9) met | KPI review | CRITICAL |
| V4-3 | SC-015: Soft → Full criteria (M1–M12, two consecutive windows) met | KPI review | CRITICAL |
| V4-4 | SC-015: Rollback drill (M10) completed successfully | Operational test | CRITICAL |
| V4-5 | NFR-010: Full promotion sequence Shadow → Soft → Full completed | Process review | CRITICAL |
| V4-6 | NFR-011: All promotion gate criteria met at each transition | Gate evidence | CRITICAL |
| V4-7 | Suspicion rate within thresholds (NFR-009) | Metric analysis | MAJOR |
| V4-8 | M1 recalibrated for phase-scope (NFR-012) | Calibration review | MAJOR |
| V4-9 | Provisional KPI defaults → normative (NFR-018) | Reliability Owner sign-off | MAJOR |
| V4-10 | False-positive/false-negative rates acceptable | Production data review | MAJOR |
| V4-11 | v1.3 handoff document with task-scope inventory | Document review | MINOR |

---

## 6. Quality Gates Between Phases

### Gate G0: P0 → P1

| Gate Criterion | Evidence Required | Blocking? |
|---------------|-------------------|-----------|
| SC-003 passing | Test report showing artifact production | Yes |
| SC-004 passing | Test report showing non-zero exit on validation error | Yes |
| Dead code retired (FR-046) | `find_referencing_symbols` output showing zero references | Yes |
| Canonical terms documented (FR-008) | Updated spec glossary | Yes |
| Phase 1 owners and deadlines assigned | Blocker registry | Yes |
| Scope boundaries documented | Updated spec with `[v1.3 -- deferred]` markers | Yes |

### Gate G1: P1 → P2

| Gate Criterion | Evidence Required | Blocking? |
|---------------|-------------------|-----------|
| SC-001 passing (no-op detection) | Test report | Yes |
| SC-002 passing (v2.25 regression) | Test report with v2.25 fixtures | Yes |
| SC-005 passing (G-012 known-bad) | Test report | Yes |
| SC-009 passing (all-EXEMPT = fail) | Test report | Yes |
| SC-010 passing (deterministic replay) | Two identical runs compared | Yes |
| SC-012 passing (deviation-analysis.md) | Artifact produced and validated | Yes |
| SC-013 resolved (C3 per-task artifacts) | Validation report or escalation decision | Yes |
| NFR-006 verified | Replay test evidence | Yes |
| `AuditGateResult` coexists with `GateResult` | Import test passing | Yes |
| Fixture stability test passing | `test_fixture_content_matches_gate_patterns` | Yes |

### Gate G2: P2 → P3

| Gate Criterion | Evidence Required | Blocking? |
|---------------|-------------------|-----------|
| NFR-005 verified (no deadlocks) | Stress test report + path analysis | Yes |
| SC-011 passing (timeout determinism) | Test report | Yes |
| Lease model functional | Heartbeat + timeout test reports | Yes |
| Shadow mode collecting without blocking | E2E test report | Yes |
| Blocker 6 resolved | Code change or removal commit | Yes |
| Reliability Owner approves timeout values | Written approval | Yes |
| KPI instrumentation emitting | Metric sample data | Yes |

### Gate G3: P3 → P4

| Gate Criterion | Evidence Required | Blocking? |
|---------------|-------------------|-----------|
| SC-006 passing (G-012 post-fix) | Test report | Yes |
| SC-008 passing (audit trail + overrides) | Audit trail sample + override test report | Yes |
| SC-014 passing (transition enforcement) | Integration test report | Yes |
| SC-016 verified (all blockers closed) | Blocker registry — all rows have owner + deadline + status=closed | Yes |
| TUI renders audit states | TUI test evidence (screenshot or test report) | Yes |
| Release guard blocks without `audit_release_passed` | TUI interaction test | Yes |

### Gate G4: P4 → Release

| Gate Criterion | Evidence Required | Blocking? |
|---------------|-------------------|-----------|
| SC-007 (S2 calibration approved) | Signed document from Reliability Owner | Yes |
| Shadow → Soft criteria met (M1, M4, M5, M7, M9) | KPI dashboard or report | Yes |
| Soft → Full criteria met (M1–M12, two consecutive windows) | KPI evidence for both windows | Yes |
| Rollback drill successful (M10) | Drill report with rollback + recovery evidence | Yes |
| Suspicion rate within NFR-009 thresholds | Metric analysis report | Yes |
| Provisional → normative KPI approval (NFR-018) | Reliability Owner sign-off | Yes |
| v1.3 handoff document complete | Document review | No (MINOR) |

---

## 7. Sequencing Guardrails for Test Strategy

These override schedule pressure and are non-negotiable:

1. **No Phase 1 tests assume P0-A defects are fixed** — V0 must pass G0 before any P1 test execution begins.
2. **No integration testing without deterministic replay proof** — SC-010 must pass in V1 before V2 integration tests rely on gate output stability.
3. **No shadow mode activation without KPI instrumentation verified** — V2-10 must pass before P4 begins.
4. **No promotion gate testing without two full consecutive KPI windows** — cannot be accelerated by combining partial windows.
5. **Deadlock freedom (NFR-005) is a hard prerequisite for enforcement testing** — V2-1 must pass before any V3 transition-blocking tests execute.

---

## 8. Test Infrastructure Requirements

| Requirement | Purpose | Phase Needed |
|-------------|---------|--------------|
| v2.25 spec/roadmap fixture archive | D-03/D-04 regression tests | V1 |
| `sc-smoke-skill/SKILL.md` stability contract | Content anchor verification | V1 |
| Mock LLM harness | G-012 CI integration without API | V1 (basic), V2 (full matrix) |
| Lease timeout simulator | Heartbeat loss and recovery testing | V2 |
| KPI metric sink (test double) | Shadow mode instrumentation verification | V2 |
| TUI test harness | State rendering and interaction testing | V3 |
| Multi-window KPI data generator | Promotion gate validation | V4 |
