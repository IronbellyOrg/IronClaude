# v3.1 Roadmap Gap Analysis (Agent B)

**Spec**: `anti-instincts-gate-unified.md`
**Roadmaps**: `roadmap.md` (Opus), `roadmap-haiku-architect.md` (Haiku)
**Execution Log**: 4 phases, all PASS, 49m 18s total
**Analysis Date**: 2026-03-21
**Analyzer**: Agent B (TurnLedger integration focus)

---

## Roadmap Phase-by-Phase Status

### Opus Roadmap (4 phases)

| Phase | Scope | Status | Evidence |
|-------|-------|--------|----------|
| Phase 1: Core Detection Modules | FR-MOD1.1-1.8, FR-MOD2.1-2.6, FR-MOD3.1-3.4, FR-MOD4.1-4.3 | IMPLEMENTED | All 4 modules exist with tests |
| Phase 2: Gate Definition + Executor Wiring + Prompts | FR-GATE.1-3, FR-EXEC.1-4, FR-PROMPT.1-2 | IMPLEMENTED | ANTI_INSTINCT_GATE in gates.py, step in executor.py, prompt blocks in prompts.py |
| Phase 3: Sprint Integration + Rollout Mode | FR-SPRINT.1-5 | PARTIALLY IMPLEMENTED | gate_rollout_mode exists, hook exists, but KPI/remediation-log wiring missing |
| Phase 4: Shadow Validation + Graduation | SC-008, NFR-011 | NOT YET (operational) | Requires live sprint runs; not a code deliverable |

### Haiku Roadmap (7 phases, Phase 0-6)

| Phase | Scope | Status |
|-------|-------|--------|
| Phase 0: Architecture Lock | OQ resolution, merge coordination | ASSUMED DONE (implicit in implementation) |
| Phase 1: Analyzer Modules | Same as Opus Phase 1 | IMPLEMENTED |
| Phase 2: Gate + Executor | Same as Opus Phase 2 | IMPLEMENTED |
| Phase 3: Prompt Hardening | FR-PROMPT.1-2 | IMPLEMENTED |
| Phase 4: Sprint Integration | FR-SPRINT.1-5 | PARTIALLY IMPLEMENTED |
| Phase 5: E2E Validation | SC-001 through SC-009, NFR-011 | PARTIALLY (tests exist, shadow runs pending) |
| Phase 6: Rollout | Operational | NOT YET |

---

## Present in Code

### New Source Files (4/4 complete)

| File | Status | Evidence |
|------|--------|----------|
| `src/superclaude/cli/roadmap/obligation_scanner.py` | PRESENT | Exists on disk |
| `src/superclaude/cli/roadmap/integration_contracts.py` | PRESENT | Exists on disk |
| `src/superclaude/cli/roadmap/fingerprint.py` | PRESENT | Exists on disk |
| `src/superclaude/cli/roadmap/spec_structural_audit.py` | PRESENT | Exists on disk |

### New Test Files (8/8 complete)

| File | Status |
|------|--------|
| `tests/roadmap/test_obligation_scanner.py` | PRESENT |
| `tests/roadmap/test_integration_contracts.py` | PRESENT |
| `tests/roadmap/test_fingerprint.py` | PRESENT |
| `tests/roadmap/test_spec_structural_audit.py` | PRESENT |
| `tests/roadmap/test_anti_instinct_integration.py` | PRESENT |
| `tests/sprint/test_anti_instinct_sprint.py` | PRESENT |
| `tests/sprint/test_shadow_mode.py` | PRESENT |
| `tests/pipeline/test_full_flow.py` | PRESENT |

### Modified Files (5/5 touched)

| File | Spec Requirement | Status | Details |
|------|-----------------|--------|---------|
| `src/superclaude/cli/roadmap/gates.py` | ANTI_INSTINCT_GATE + 3 semantic checks + ALL_GATES insertion | DONE | Line 995: GateCriteria definition; Line 1084: ALL_GATES insertion between merge and test-strategy |
| `src/superclaude/cli/roadmap/executor.py` | anti-instinct step + structural audit hook + _run_anti_instinct_audit | DONE | _run_structural_audit at L220, _run_anti_instinct_audit at L265, step at L846, step ID at L963 |
| `src/superclaude/cli/roadmap/prompts.py` | INTEGRATION_ENUMERATION_BLOCK + INTEGRATION_WIRING_DIMENSION | DONE | L38 and L51 respectively; wired into build_generate_prompt (L199) and build_spec_fidelity_prompt (L357) |
| `src/superclaude/cli/sprint/models.py` | gate_rollout_mode field on SprintConfig | DONE | L325: `gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"` |
| `src/superclaude/cli/sprint/executor.py` | run_post_task_anti_instinct_hook + TurnLedger integration | PARTIALLY DONE | Hook exists (L585-686), wired into execute_phase_tasks (L792), but missing KPI/remediation-log orchestration |

### Sprint Executor Anti-Instinct Hook (Detailed)

The `run_post_task_anti_instinct_hook` function at L585 correctly implements:
- Mode-based evaluation (off/shadow/soft/full)
- ShadowGateMetrics recording in shadow/soft/full modes
- TurnLedger credit on PASS (soft/full): `ledger.credit(int(turns_consumed * ledger.reimbursement_rate))`
- TurnLedger None-safety (NFR-007): all ledger calls guarded
- GateOutcome setting on pass/fail
- TaskStatus.FAIL only in full mode
- BUDGET_EXHAUSTED path when `ledger.can_remediate()` returns False
- Independent evaluation from wiring gate (NFR-010)

---

## Missing from Code

### M1: `build_kpi_report()` not called from `execute_sprint()`

**Spec Ref**: Section 9.6, FR-SPRINT.4
**Roadmap Ref**: Opus Phase 3.2, Haiku Phase 4

The spec requires: "GateKPIReport (sprint/kpi.py) receives anti-instinct gate results alongside all other gate results at sprint completion via build_kpi_report()."

**Current state**: `build_kpi_report()` exists in `sprint/kpi.py` (L137) and accepts `gate_results: list[TrailingGateResult]`, but `execute_sprint()` never calls it. There is no `_all_gate_results` accumulator list in the sprint executor. The function is defined but dead code from the sprint's perspective.

### M2: `DeferredRemediationLog` not instantiated in `execute_sprint()`

**Spec Ref**: Section 9.5 step 5, Section 16.5
**Roadmap Ref**: Opus Phase 3.2, Haiku Phase 4

The spec requires: "On FAIL: remediation_log.append(gate_result)" and "DeferredRemediationLog entry exits with BUDGET_EXHAUSTED."

**Current state**: `DeferredRemediationLog` is defined in `pipeline/trailing_gate.py` (L489) and is fully functional. However, `execute_sprint()` does not instantiate one. The `run_post_task_anti_instinct_hook` does NOT append to any remediation log -- it handles failure purely through gate_outcome and status mutation. No failure records are persisted for `--resume` recovery.

### M3: `TrailingGateResult` not accumulated for anti-instinct evaluations

**Spec Ref**: Section 9.5 steps 2-3
**Roadmap Ref**: Opus Phase 3.2 FR-SPRINT.2

The spec requires: "Gate result is wrapped in TrailingGateResult(passed, evaluation_ms, gate_name)" and "Result submitted to sprint-level _all_gate_results accumulator."

**Current state**: `run_post_task_anti_instinct_hook` evaluates `gate_passed()` and gets `(passed, failure_reason)` back, but does NOT wrap the result in a `TrailingGateResult` object. It does NOT submit results to any accumulator. The latency measurement (`evaluation_ms`) is computed but only used for logging and ShadowGateMetrics. There is no `_all_gate_results: list[TrailingGateResult]` in `execute_sprint()`.

### M4: KPI report not written to disk at sprint completion

**Spec Ref**: Section 9.6
**Roadmap Ref**: Opus Phase 3.2 FR-SPRINT.4

After sprint completion, no KPI report is generated or written. The `GateKPIReport.format_report()` method exists but is never called during sprint execution.

### M5: `gate_scope=GateScope.TASK` not verified on ANTI_INSTINCT_GATE

**Spec Fidelity**: DEV-005 (MEDIUM)
**Note**: Need to verify the actual GateCriteria definition includes `gate_scope`.

### M6: Spec fidelity deviation DEV-002 -- `TrailingGateResult` signature

The spec defines `TrailingGateResult(passed, evaluation_ms, gate_name)` but the actual implementation at `pipeline/trailing_gate.py:36` uses `TrailingGateResult(step_id, passed, evaluation_ms, failure_reason)`. The field is `step_id` not `gate_name`, and it has a `failure_reason` field instead. The Opus roadmap also had this discrepancy (DEV-002 in spec-fidelity.md). The **codebase follows the roadmap's version**, not the spec's.

---

## TurnLedger Wiring Gaps

### Gap 1: No Gate Result Accumulation (CRITICAL)

**What the spec says**: Anti-instinct gate results must be wrapped in `TrailingGateResult` and accumulated into `_all_gate_results` for KPI aggregation at sprint completion.

**What the code does**: The hook evaluates the gate and logs results. It records to `ShadowGateMetrics` correctly. But it does NOT create `TrailingGateResult` objects or accumulate them anywhere. The `TrailingGateResult` import at L39 of `sprint/executor.py` is used only by `SprintGatePolicy.build_remediation_step()`, not by the anti-instinct hook.

**Impact**: `build_kpi_report()` cannot aggregate anti-instinct gate metrics because no `TrailingGateResult` objects are produced.

### Gap 2: No DeferredRemediationLog in Sprint Loop (MODERATE)

**What the spec says**: On gate FAIL, `remediation_log.append(gate_result)` records the failure. The log supports `--resume` recovery and KPI aggregation.

**What the code does**: `execute_sprint()` does not create a `DeferredRemediationLog`. The `run_post_task_anti_instinct_hook` handles FAIL by setting `gate_outcome` and `status` directly on `TaskResult`, but does not persist failure details to a log.

**Impact**: No persistent record of anti-instinct gate failures. `--resume` cannot identify which tasks failed anti-instinct gates. `build_kpi_report(remediation_log=...)` receives None, so remediation metrics are always zero.

### Gap 3: No `build_kpi_report()` Call at Sprint End (MODERATE)

**What the spec says**: "GateKPIReport receives anti-instinct gate results alongside all other gate results at sprint completion."

**What the code does**: `execute_sprint()` ends with `logger.write_summary(sprint_result)` and `notify_sprint_complete(sprint_result)`. No KPI report is generated.

**Impact**: Gate performance metrics (pass rate, latency p50/p95, remediation frequency) are never computed or reported after sprint completion.

### Gap 4: Reimbursement Credits Correct Operand (LOW)

**What the spec says** (Section 16.5): "ledger.credit(int(upstream_merge_turns * ledger.reimbursement_rate))" -- reimbursement applies to the upstream merge step's turn cost.

**What the code does** (L651): `credit_amount = int(task_result.turns_consumed * ledger.reimbursement_rate)` -- reimbursement applies to the current task's turn cost.

**Impact**: In sprint-invoked mode, the spec intends reimbursement to be based on the *upstream merge step's* LLM cost, not the current task's turns. Since the anti-instinct check itself is 0 LLM turns, the current code uses the task's total turns (which includes the subprocess execution, not just the merge step). This is a semantic divergence -- the current approach is arguably more practical (reimburses based on the task that just ran) but differs from the spec's stated intent.

### Gap 5: Wiring Gate and Anti-Instinct Gate Results Not Unified (LOW)

Both `run_post_task_wiring_hook` and `run_post_task_anti_instinct_hook` produce gate evaluation results independently, but neither feeds into a unified `_all_gate_results` accumulator. The wiring hook has its own separate KPI fields in `GateKPIReport` (wiring_findings_total, wiring_turns_used, etc.) but the anti-instinct gate has no analogous per-gate-type KPI fields.

---

## Root Cause Analysis

The implementation achieved full coverage of the **roadmap pipeline side** (Phases 1-2 of both roadmaps) -- all four detection modules, the gate definition, the executor wiring, and the prompt modifications are complete and tested.

The gap is concentrated in **sprint-side orchestration wiring** (Phase 3). The root cause is architectural:

1. **Hook-based integration without accumulation**: The `run_post_task_anti_instinct_hook` was implemented as a self-contained function that modifies `TaskResult` in-place and records to `ShadowGateMetrics`. This is operationally correct for off/shadow/soft/full mode behavior, but it bypasses the `TrailingGateResult` + `DeferredRemediationLog` + `build_kpi_report()` accumulation pipeline that the spec's Section 9.5 describes.

2. **Parallel implementation paths diverged**: The wiring hook (`run_post_task_wiring_hook`) follows a similar in-place mutation pattern. Both hooks were implemented to work within `execute_phase_tasks()` (the per-task loop), but the higher-level `execute_sprint()` function was not updated to aggregate their outputs at sprint completion.

3. **Sprint loop is phase-based, not task-based**: The `execute_sprint()` function iterates over phases and launches one Claude subprocess per phase. The `execute_phase_tasks()` function (which handles per-task execution with both hooks) is only called when the sprint uses task-level granularity. The main sprint loop (`execute_sprint`) does not currently use `execute_phase_tasks()` -- it launches one subprocess per phase via `ClaudeProcess` directly. The per-task orchestration with hooks only fires when tasks are explicitly enumerated within a phase.

4. **Missing glue code**: The pieces all exist (`TrailingGateResult`, `DeferredRemediationLog`, `build_kpi_report`, `GateKPIReport`, `ShadowGateMetrics`), but the sprint-level glue that instantiates a `DeferredRemediationLog`, collects `TrailingGateResult` objects from each hook invocation, and calls `build_kpi_report()` at sprint end was never written.

---

## Recommendations

### R1: Add gate result accumulation to `execute_phase_tasks()` (HIGH PRIORITY)

Wrap the anti-instinct hook's evaluation into a `TrailingGateResult` and return it alongside `TaskResult`. Collect all `TrailingGateResult` objects across the sprint for KPI aggregation.

### R2: Instantiate `DeferredRemediationLog` in sprint entrypoint (HIGH PRIORITY)

Add `DeferredRemediationLog` instantiation with a persist path (e.g., `results_dir / "remediation.json"`). Pass it to `execute_phase_tasks()` so that gate failures are recorded and available for `--resume`.

### R3: Call `build_kpi_report()` at sprint completion (MODERATE)

After all phases complete in `execute_sprint()`, aggregate `TrailingGateResult` objects and call `build_kpi_report()`. Write the formatted report to disk alongside the sprint summary.

### R4: Reconcile reimbursement operand with spec intent (LOW)

Decide whether reimbursement should be based on `task_result.turns_consumed` (current) or the upstream merge step's turns (spec). The current approach is simpler and defensible. If the spec's intent is authoritative, the hook needs access to the upstream step's turn count, which requires passing merge-step accounting through the pipeline.

### R5: Consider unifying gate result flow across hooks (LOW)

Both wiring and anti-instinct hooks follow the same pattern. Consider extracting a shared `PostTaskGateHook` protocol that:
- Returns a `TrailingGateResult`
- Appends to `DeferredRemediationLog` on failure
- Is collected by the sprint loop for KPI aggregation

This would close the architectural gap between the hook-based implementation and the spec's accumulation-based design.

---

## Summary

| Category | Count |
|----------|-------|
| Spec requirements fully implemented | ~28 of 35 FR + 8 of 10 NFR |
| Present in code (files) | 12/12 new files + 5/5 modified files |
| TurnLedger wiring gaps | 5 (2 critical, 1 moderate, 2 low) |
| Root cause | Sprint-level orchestration glue not written; hooks work per-task but results not accumulated at sprint scope |

The v3.1 anti-instinct gate is **feature-complete on the roadmap pipeline side** and **behaviorally correct on the sprint hook side** (rollout modes, None-safety, metrics recording). The gap is in the **sprint-level bookkeeping layer**: gate result accumulation, remediation log persistence, and KPI report generation at sprint completion. All required infrastructure components exist; the missing piece is the glue code in `execute_sprint()` that connects them.
