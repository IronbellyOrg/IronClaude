# v3.1 Roadmap Gap Analysis (Agent A)

**Analyzed**: 2026-03-21
**Release**: v3.1 Anti-Instinct Gate
**Branch**: v3.0-AuditGates
**Execution Log**: All 4 phases reported PASS (49m 18s total)

---

## Roadmap Phase-by-Phase Status

### Phase 1: Core Detection Modules & Architecture Decisions -- IMPLEMENTED

| Roadmap Item | Status | Evidence |
|---|---|---|
| R-001: Day-1 Architecture Decisions (OQ-003, OQ-004, OQ-005, OQ-010) | DONE | Decisions reflected in implementation choices |
| R-002: Obligation Scanner (`obligation_scanner.py`) | DONE | File exists at `src/superclaude/cli/roadmap/obligation_scanner.py` |
| R-003: Integration Contract Extractor (`integration_contracts.py`) | DONE | File exists at `src/superclaude/cli/roadmap/integration_contracts.py` |
| R-004: Fingerprint Extraction (`fingerprint.py`) | DONE | File exists at `src/superclaude/cli/roadmap/fingerprint.py` |
| R-005: Spec Structural Audit (`spec_structural_audit.py`) | DONE | File exists at `src/superclaude/cli/roadmap/spec_structural_audit.py` |
| R-006: Unit Tests for All Modules | NOT VERIFIED | Test files not confirmed in this analysis scope |
| R-007: Validation Gate (Checkpoint A) | DONE | Execution log shows Phase 1 PASS |

### Phase 2: Gate Definition, Executor Wiring & Prompt Hardening -- IMPLEMENTED

| Roadmap Item | Status | Evidence |
|---|---|---|
| R-008: `ANTI_INSTINCT_GATE` in `gates.py` | DONE | `ANTI_INSTINCT_GATE` at line 995, inserted into `ALL_GATES` at line 1084 |
| R-009: Executor integration in `roadmap/executor.py` | DONE | `_run_structural_audit()` at line 220, `_run_anti_instinct_audit()` at line 265, `"anti-instinct"` step at line 846, in `_get_all_step_ids()` at line 963 |
| R-010: Prompt modifications in `prompts.py` | DONE | `_INTEGRATION_ENUMERATION_BLOCK` at line 38, `_INTEGRATION_WIRING_DIMENSION` at line 51, wired into prompt builders |
| R-011: Integration tests | NOT VERIFIED | `test_anti_instinct_integration.py` not confirmed |
| R-012: Validation Gate | DONE | Execution log shows Phase 2 PASS |

### Phase 3: Sprint Integration & Rollout Mode -- PARTIALLY IMPLEMENTED

| Roadmap Item | Status | Evidence |
|---|---|---|
| R-013: `gate_rollout_mode` in `SprintConfig` | DONE | Line 325 in `models.py`: `gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"` |
| R-014: Sprint Executor Wiring | PARTIAL | `run_post_task_anti_instinct_hook()` exists with rollout mode matrix. See TurnLedger Wiring Gaps below. |
| R-015: Sprint Integration Tests | DONE | `tests/sprint/test_anti_instinct_sprint.py` exists with 8 rollout mode scenarios, None-safe tests, independence tests, budget exhaustion tests |
| R-016: Validation Gate (Checkpoint B) | DONE | Execution log shows Phase 3 PASS |

### Phase 4: Shadow Validation & Graduation -- NOT APPLICABLE YET

| Roadmap Item | Status | Evidence |
|---|---|---|
| R-017: Shadow Mode Activation | DEFERRED | Requires live sprint runs; not code-implementable |
| R-018: Threshold Calibration | DEFERRED | Requires shadow data |
| R-019: Open Question Resolution | DEFERRED | Requires shadow data |
| R-020: Graduation Criteria | DEFERRED | Requires 5+ sprint runs |

---

## Present in Code

### Phase 1 -- Core Modules (4/4 complete)
- `obligation_scanner.py` -- scaffold-discharge detection with compiled regex, `ObligationReport`/`Obligation` dataclasses, phase splitting, component context extraction
- `integration_contracts.py` -- 7-category dispatch pattern scanner, `IntegrationAuditResult`/`IntegrationContract`/`WiringCoverage` dataclasses, `check_roadmap_coverage()`
- `fingerprint.py` -- 3-source extraction (backtick, code-block def/class, ALL_CAPS), `_EXCLUDED_CONSTANTS` frozenset, threshold gate logic (0.7 default)
- `spec_structural_audit.py` -- 7 structural indicator counters, `check_extraction_adequacy()` with 0.5 threshold

### Phase 2 -- Pipeline Wiring (complete)
- `ANTI_INSTINCT_GATE` in `roadmap/gates.py` with 3 semantic checks (`_no_undischarged_obligations`, `_integration_contracts_covered`, `_fingerprint_coverage_check`), `enforcement_tier="STRICT"`, `GateScope.TASK`
- `_run_anti_instinct_audit()` in `roadmap/executor.py` -- runs all 3 modules, writes `anti-instinct-audit.md` with YAML frontmatter
- `_run_structural_audit()` -- post-extract warning-only hook
- `"anti-instinct"` step between `"merge"` and `"test-strategy"` with `retry_limit=0`, `timeout_seconds=30`
- `INTEGRATION_ENUMERATION_BLOCK` and `INTEGRATION_WIRING_DIMENSION` in `prompts.py`

### Phase 3 -- Sprint Integration (mostly complete)
- `gate_rollout_mode` field on `SprintConfig` (default `"off"`)
- `run_post_task_anti_instinct_hook()` in `sprint/executor.py` with full rollout mode matrix (off/shadow/soft/full)
- Anti-instinct hook invoked from `execute_phase_tasks()` after wiring hook (NFR-010 independence preserved)
- `ShadowGateMetrics.record()` called in shadow/soft/full modes (FR-SPRINT.4)
- None-safe TurnLedger guards throughout (NFR-007)
- Credit path: `ledger.credit(int(task_result.turns_consumed * ledger.reimbursement_rate))` on PASS (soft/full)
- Fail path: `GateOutcome.FAIL` set; `TaskStatus.FAIL` only in full mode
- Budget exhaustion path: checks `ledger.can_remediate()` before remediation

### Infrastructure already present (from v3.0)
- `TurnLedger` class in `sprint/models.py` with budget tracking, `credit()`, `debit()`, `can_launch()`, `can_remediate()`, `reimbursement_rate=0.8`
- `TrailingGateResult` dataclass in `pipeline/trailing_gate.py`
- `TrailingGateRunner` with daemon-thread gate evaluation
- `DeferredRemediationLog` with persistence and `--resume` support
- `TrailingGatePolicy` protocol and `SprintGatePolicy` implementation
- `attempt_remediation()` with retry-once semantics
- `GateKPIReport` and `build_kpi_report()` in `sprint/kpi.py`
- `GateScope`, `resolve_gate_mode()` in `pipeline/trailing_gate.py`
- `TaskResult` with `gate_outcome`, `reimbursement_amount` fields

---

## Missing from Code

### 1. `execute_sprint()` does NOT construct a TurnLedger
**Severity**: HIGH
**Spec reference**: FR-SPRINT.2, FR-SPRINT.5, A-011

The `execute_sprint()` function (the main orchestration loop at line 843) never instantiates a `TurnLedger`. It never passes `ledger=...` to `execute_phase_tasks()`. The per-task loop in `execute_phase_tasks()` accepts `ledger: TurnLedger | None = None` and the anti-instinct hook is guarded by `if ledger is not None`, but since `execute_sprint()` never constructs one, all ledger paths are dead code in production.

The `execute_sprint()` function uses a per-phase subprocess model (one `ClaudeProcess` per phase), not the per-task model. It does not call `execute_phase_tasks()` at all. The per-task function exists but is only reachable through test factories.

### 2. `execute_sprint()` does NOT construct ShadowGateMetrics
**Severity**: HIGH
**Spec reference**: FR-SPRINT.4

No `ShadowGateMetrics` instance is created in `execute_sprint()`. Since the main loop does not call `execute_phase_tasks()` (which accepts `shadow_metrics`), shadow metrics collection never occurs in production sprint runs.

### 3. `execute_sprint()` does NOT instantiate SprintGatePolicy
**Severity**: MEDIUM
**Spec reference**: A-014

`SprintGatePolicy` is defined (lines 56-99) but never instantiated in `execute_sprint()`. The remediation step construction path is unreachable.

### 4. `execute_sprint()` does NOT call `build_kpi_report()`
**Severity**: MEDIUM
**Spec reference**: FR-SPRINT.4, Section 9.6

`build_kpi_report()` exists in `sprint/kpi.py` and accepts `gate_results`, `remediation_log`, `turn_ledger`, and `wiring_report`. But `execute_sprint()` never calls it. No KPI report is produced at sprint completion.

### 5. `execute_sprint()` does NOT instantiate DeferredRemediationLog
**Severity**: MEDIUM
**Spec reference**: FR-SPRINT.3

`DeferredRemediationLog` is imported in `pipeline/trailing_gate.py` and used by `sprint/kpi.py`, but `execute_sprint()` never creates one. Gate failure remediation logging does not persist.

### 6. No anti-instinct gate evaluation in the main sprint loop
**Severity**: HIGH
**Spec reference**: FR-SPRINT.2

The `execute_sprint()` main loop processes phases as single subprocess launches. After each phase completes, it determines `PhaseStatus` and records `PhaseResult`. It never runs `run_post_task_anti_instinct_hook()` or any gate evaluation on per-phase results. The hook only exists in `execute_phase_tasks()`, which is not called by `execute_sprint()`.

### 7. `attempt_remediation()` never called from sprint executor
**Severity**: LOW
**Spec reference**: FR-SPRINT.3

`attempt_remediation()` exists in `pipeline/trailing_gate.py` with retry-once semantics, but is never invoked from either `execute_sprint()` or `run_post_task_anti_instinct_hook()`. The anti-instinct hook implements its own inline fail/remediation logic instead of delegating to `attempt_remediation()`.

### 8. Missing test files from spec
**Severity**: LOW
**Spec reference**: Section 12

| Specified Test File | Status |
|---|---|
| `tests/sprint/test_anti_instinct_sprint.py` | EXISTS |
| `tests/sprint/test_shadow_mode.py` | NOT FOUND |
| `tests/pipeline/test_full_flow.py` | NOT FOUND |
| `tests/roadmap/test_anti_instinct_integration.py` | NOT VERIFIED |

---

## TurnLedger Wiring Gaps

### Gap 1: `execute_sprint` ledger construction -- MISSING

`execute_sprint()` is the production entry point. It never constructs a `TurnLedger` or passes one to any downstream function. The entire TurnLedger economic model is disconnected from the production sprint loop.

**What exists**: `execute_phase_tasks()` accepts `ledger: TurnLedger | None = None` and uses it correctly in the per-task loop. But `execute_sprint()` uses a different code path (per-phase `ClaudeProcess` + poll loop) and never calls `execute_phase_tasks()`.

**What's needed**: Either:
- (a) `execute_sprint()` must construct a `TurnLedger` and wire it into its phase loop, OR
- (b) `execute_sprint()` must be refactored to use `execute_phase_tasks()` for task-level orchestration, OR
- (c) A post-phase gate hook must be added to the `execute_sprint()` loop analogous to how `execute_phase_tasks()` calls `run_post_task_anti_instinct_hook()`.

### Gap 2: SprintGatePolicy -- DEFINED BUT NOT INSTANTIATED

`SprintGatePolicy` (line 56) implements `TrailingGatePolicy` with `build_remediation_step()` and `files_changed()`. It is never instantiated by `execute_sprint()`. The remediation workflow is unreachable.

### Gap 3: `attempt_remediation` -- NEVER CALLED

`attempt_remediation()` in `pipeline/trailing_gate.py` provides the retry-once state machine with budget integration. The anti-instinct hook (`run_post_task_anti_instinct_hook`) implements a simpler inline version that checks `can_remediate()` but never actually runs remediation -- it just logs and marks FAIL. The full `attempt_remediation()` flow (debit -> run -> gate -> retry) is never exercised.

### Gap 4: `build_kpi_report` -- NEVER CALLED

`build_kpi_report()` and `GateKPIReport` exist in `sprint/kpi.py`. The function aggregates gate pass/fail rates, latencies, and remediation metrics. `execute_sprint()` never calls it; no KPI report is produced.

### Gap 5: DeferredRemediationLog -- NEVER INSTANTIATED IN SPRINT

`DeferredRemediationLog` has full persistence and `--resume` support. `run_post_task_anti_instinct_hook()` does not use it -- gate failures are logged but not persisted to a remediation log. The `--resume` recovery path for gate failures is inoperative.

---

## Root Cause Analysis

The root cause is an **architectural mismatch between two execution models**:

1. **`execute_sprint()`** (the production entry point) uses a **per-phase subprocess model**: one `ClaudeProcess` per phase, monitored via a poll loop. It has no concept of individual tasks, TurnLedger budget tracking, or post-step gate evaluation.

2. **`execute_phase_tasks()`** (the per-task function) uses a **per-task subprocess model**: iterates over `TaskEntry` objects, manages budget via `TurnLedger`, and runs post-task hooks (wiring + anti-instinct). This function is correctly wired but is **never called from `execute_sprint()`**.

The v3.1 sprint implemented the anti-instinct gate hooks and TurnLedger integration in `execute_phase_tasks()`, but this function exists in a parallel code path that is only reachable through test factories (`_subprocess_factory`). The main production loop (`execute_sprint()`) is unmodified.

This is the exact class of bug the anti-instinct gate was designed to catch: the components were built but never wired into the production dispatch path. The `execute_sprint()` -> `execute_phase_tasks()` wiring task is the missing integration step.

### Contributing factors:

1. **Dual execution context confusion**: The roadmap correctly identified the dual context (standalone roadmap vs sprint-invoked), but the sprint executor itself has a dual internal architecture (per-phase vs per-task) that was not surfaced in the spec.

2. **Test coverage gap**: The test file `test_anti_instinct_sprint.py` tests `run_post_task_anti_instinct_hook()` directly and `execute_phase_tasks()` with `_subprocess_factory`, both of which work. But no test verifies that `execute_sprint()` actually invokes these paths.

3. **Execution log shows all phases PASS**: The sprint execution reported success (49m 18s), but the "success" refers to task implementation (files created, tests passing), not to production wiring verification.

---

## Recommendations

### Priority 1: Wire `execute_sprint()` to TurnLedger (BLOCKING)

Either refactor `execute_sprint()` to call `execute_phase_tasks()` for task-level orchestration, or add TurnLedger construction and post-phase gate hooks directly to the `execute_sprint()` poll loop. The per-task model is preferred because it enables per-task budget tracking and post-task gate evaluation.

### Priority 2: Instantiate ShadowGateMetrics in production path (BLOCKING)

`execute_sprint()` must create a `ShadowGateMetrics` instance and pass it through to the gate hooks so shadow metrics are actually collected when `gate_rollout_mode=shadow`.

### Priority 3: Call `build_kpi_report()` at sprint completion (MEDIUM)

After the phase loop completes, `execute_sprint()` should call `build_kpi_report()` with accumulated gate results, remediation log, and TurnLedger to produce the KPI report.

### Priority 4: Wire DeferredRemediationLog for `--resume` (MEDIUM)

Instantiate `DeferredRemediationLog` with a persistence path at sprint start. Pass it through to gate hooks. This enables `--resume` to recover from gate failures.

### Priority 5: Integration test for production path (HIGH)

Add a test that exercises `execute_sprint()` end-to-end (with mocked `ClaudeProcess`) and verifies that TurnLedger, ShadowGateMetrics, and gate hooks are invoked. The current test suite only covers the parallel `execute_phase_tasks()` path.

### Priority 6: `attempt_remediation()` integration (LOW)

Decide whether the inline remediation logic in `run_post_task_anti_instinct_hook()` should delegate to `attempt_remediation()` for the retry-once state machine, or whether the current simple fail-and-log behavior is intentional for v3.1.
