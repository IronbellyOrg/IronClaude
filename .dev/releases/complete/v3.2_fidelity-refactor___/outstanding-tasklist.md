# Outstanding Tasklist: TurnLedger Integration Gap Remediation

**Generated**: 2026-03-22
**Source**: QA execution reflections from v3.05, v3.1, v3.2 gap-remediation cycles
**Purpose**: Consolidates all skipped tasks from the 3 gap-remediation tasklists for execution by `/sc:task-unified`

---

## Summary

| Metric | Value |
|--------|-------|
| **Total tasks** | 22 |
| **Waves** | 6 |
| **v3.05 tasks** | 7 (T07, T08, T10-partial, T11, T12, T14, plus PASS log fix) |
| **v3.1 tasks** | 3 (T04, T05, T11) |
| **v3.2 tasks** | 12 (T02, T13, T15, T17, T18, T19, T20, T21, T22, plus test gaps) |
| **Blocking** | 2 (v3.1-T04 architectural wiring, v3.2-T02 one-line hook call) |

---

## Dependency Graph

```
Wave 1 (blocking fixes — must go first):
  v3.2-T02 (1-line hook call)
  v3.1-T04 (per-task delegation) ──┐
  v3.1-T05 (return type change)  ──┤
                                    │
Wave 2 (v3.05 tests + fixes):      │
  v3.05-T07 (wiring tests)         │
  v3.05-T08 (already partially fixed, verify)
  v3.05-T10 (PASS log budget)      │
  v3.05-T11 (E2E tests)            │
                                    │
Wave 3 (v3.1 integration test):    │
  v3.1-T11 ←───────────────────────┘

Wave 4 (v3.2 tests):
  v3.2-T13 (budget scenario tests)
  v3.2-T15 (performance benchmark)
  v3.2-T17 (execute_sprint TurnLedger integration test)
  v3.2-T18 (_resolve_wiring_mode activation test)
  v3.2-T19 (KPI and contract verification)
  v3.2-T20 (E2E shadow mode pipeline)

Wave 5 (final validation):
  v3.05-T12 (smoke test convergence)
  v3.05-T14 (regenerate wiring-verification)
  v3.2-T21 (full regression suite)

Wave 6 (audit):
  v3.2-T22 (gap closure audit)
```

---

## Wave 1: Blocking Fixes

### Task OT-01: Wire `run_post_phase_wiring_hook()` into `execute_sprint()` (v3.2-T02)
- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Source**: v3.2 gap-remediation-tasklist.md T02, QA reflection: "Critical discrepancy — function defined at line 735 but never called"
- **Description**:
  1. `run_post_phase_wiring_hook()` exists at executor.py:735-784 but is never called from `execute_sprint()`.
  2. Find the line where `sprint_result.phase_results.append(phase_result)` occurs in the phase loop (around line 1344).
  3. Insert BEFORE the append:
     ```python
     phase_result = run_post_phase_wiring_hook(
         phase, config, phase_result,
         ledger=ledger,
         remediation_log=remediation_log,
     )
     ```
  4. This is a 1-line insertion that activates the entire v3.2 wiring hook infrastructure.
- **Depends on**: none
- **Acceptance criteria**:
  - `run_post_phase_wiring_hook()` is called for every Claude-mode phase in `execute_sprint()`.
  - `grep -n "run_post_phase_wiring_hook" src/superclaude/cli/sprint/executor.py` shows a call site inside `execute_sprint()`.
  - `uv run pytest tests/sprint/ -v --tb=short` passes.
- **Risk**: The hook runs wiring analysis on every phase, which adds latency. The `_resolve_wiring_mode()` function controls whether analysis actually runs (mode "off" skips).
- **Wave**: 1

---

### Task OT-02: Wire `execute_sprint()` to call `execute_phase_tasks()` for per-task phases (v3.1-T04)
- **Type**: refactor
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Source**: v3.1 gap-remediation-tasklist.md T04
- **Description**:
  This is the critical architectural fix. The current `execute_sprint()` phase loop launches one `ClaudeProcess` per phase with no per-task orchestration. It must be modified to delegate to `execute_phase_tasks()` for phases that have task inventories.

  1. Inside the phase loop, after the `execution_mode` checks, before launching `ClaudeProcess`, add a check for whether the phase has a task inventory:
     ```python
     tasks = _parse_phase_tasks(phase, config)
     if tasks:
         started_at = datetime.now(timezone.utc)
         task_results, remaining = execute_phase_tasks(
             tasks=tasks, config=config, phase=phase,
             ledger=ledger, shadow_metrics=shadow_metrics,
             remediation_log=remediation_log,
         )
         all_passed = all(r.status == TaskStatus.PASS for r in task_results)
         status = PhaseStatus.PASS if all_passed else PhaseStatus.ERROR
         phase_result = PhaseResult(
             phase=phase, status=status, exit_code=0 if all_passed else 1,
             started_at=started_at, finished_at=datetime.now(timezone.utc),
         )
         sprint_result.phase_results.append(phase_result)
         logger.write_phase_result(phase_result)
         continue
     ```
  2. Implement `_parse_phase_tasks(phase, config) -> list[TaskEntry] | None` that parses phase files for task entries. Return `None` for freeform-prompt phases to preserve the `ClaudeProcess` fallback.
  3. The existing `ClaudeProcess` path remains as fallback for phases without task inventories.
- **Depends on**: none
- **Acceptance criteria**:
  - `execute_sprint()` calls `execute_phase_tasks()` when a phase has a task inventory.
  - Phases without task inventories still use `ClaudeProcess`.
  - `ledger`, `shadow_metrics`, `remediation_log` are passed through.
  - `uv run pytest tests/sprint/ -v` passes.
- **Risk**: HIGH. The `_parse_phase_tasks` helper must correctly distinguish task-inventory phases from freeform-prompt phases. Test with both types.
- **Wave**: 1

---

### Task OT-03: Add `TrailingGateResult` wrapping to anti-instinct hook (v3.1-T05)
- **Type**: refactor
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Source**: v3.1 gap-remediation-tasklist.md T05
- **Description**:
  **Part A**: Change `run_post_task_anti_instinct_hook()` return type from `TaskResult` to `tuple[TaskResult, TrailingGateResult | None]`.
  - After gate evaluation, create `TrailingGateResult(step_id=task.task_id, passed=passed, evaluation_ms=evaluation_ms, failure_reason=failure_reason)`.
  - Return `(task_result, gate_result)` at each return point.
  - For `mode == "off"`, return `(task_result, None)`.
  - For shadow mode, return `(task_result, gate_result)` — gate IS evaluated, result must be captured.

  **Part B**: Update `execute_phase_tasks()` caller to unpack the tuple and accumulate gate results.

  **Part C**: In `execute_sprint()`, extend `all_gate_results` with returned gate results from `execute_phase_tasks()`.
- **Depends on**: OT-02 (per-task delegation must exist for gate results to flow)
- **Acceptance criteria**:
  - `run_post_task_anti_instinct_hook()` returns `tuple[TaskResult, TrailingGateResult | None]`.
  - `execute_phase_tasks()` accumulates and returns gate results.
  - `all_gate_results` in `execute_sprint()` is populated.
  - All callers updated (grep for `run_post_task_anti_instinct_hook` in tests).
- **Risk**: Breaking change for test callers. Search all test call sites.
- **Wave**: 1

---

## Wave 2: v3.05 Tests and Fixes

### Task OT-04: Write integration tests for `_run_convergence_spec_fidelity()` (v3.05-T07)
- **Type**: test
- **Target file(s)**: New: `tests/roadmap/test_convergence_wiring.py`
- **Source**: v3.05 gap-remediation-tasklist.md T07
- **Description**:
  Create `tests/roadmap/test_convergence_wiring.py` with 7 tests:
  1. `test_registry_construction` — Verify `load_or_create()` receives correct args (path, release_id, spec_hash).
  2. `test_merge_findings_structural_only` — Verify `merge_findings(structural, [], run_number)`.
  3. `test_merge_findings_semantic_only` — Verify `merge_findings([], semantic, run_number)`.
  4. `test_remediation_dict_access` — Verify `get_active_highs()` dicts consumed correctly.
  5. `test_turnledger_budget_params` — Verify `MAX_CONVERGENCE_BUDGET`, `CHECKER_COST`, `REMEDIATION_COST`.
  6. `test_end_to_end_convergence_pass` — Full path with 0 highs -> `passed=True`.
  7. `test_end_to_end_convergence_fail` — Full path with persistent HIGHs -> `passed=False`.
  Use `tmp_path`, mock `run_all_checkers`/`run_semantic_layer`. Follow patterns from `test_convergence.py`.
- **Depends on**: none
- **Acceptance criteria**: All 7 tests pass with `uv run pytest tests/roadmap/test_convergence_wiring.py -v`.
- **Risk**: May need to mock Claude subprocess calls.
- **Wave**: 2

---

### Task OT-05: Verify wiring-verification target directory fix (v3.05-T08)
- **Type**: verify
- **Target file(s)**: `src/superclaude/cli/roadmap/executor.py` (line ~429)
- **Source**: v3.05 gap-remediation-tasklist.md T08. Note: line 429 was already changed from `config.output_dir.parent` to `Path("src/superclaude")` during v3.05 execution.
- **Description**:
  1. Verify the fix at executor.py line ~429 is correct: `source_dir = Path("src/superclaude") if Path("src/superclaude").exists() else Path(".")`
  2. Confirm this resolves to a directory with Python files.
  3. Run the wiring analysis manually or via test to verify `files_analyzed > 0`.
- **Depends on**: none
- **Acceptance criteria**: Wiring verification scans >0 Python files.
- **Risk**: Low — verification only.
- **Wave**: 2

---

### Task OT-06: Add budget state to PASS log message (v3.05-T10 partial)
- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/roadmap/convergence.py` (lines ~487-490)
- **Source**: v3.05 QA reflection: "PASS log at lines 487-490 still only shows credit turns without budget state"
- **Description**:
  Update the PASS log message to include budget state:
  ```python
  logger.info(
      "Run %d (%s): PASS — 0 active HIGHs. Credit %d turns. "
      "budget: consumed=%d, reimbursed=%d, available=%d",
      run_idx + 1, run_label, CONVERGENCE_PASS_CREDIT,
      ledger.consumed, ledger.reimbursed, ledger.available(),
  )
  ```
- **Depends on**: none
- **Acceptance criteria**: PASS log line includes `budget: consumed=N, reimbursed=N, available=N`.
- **Risk**: None. Log message change only.
- **Wave**: 2

---

### Task OT-07: Create E2E convergence tests (v3.05-T11)
- **Type**: test
- **Target file(s)**: New: `tests/roadmap/test_convergence_e2e.py`
- **Source**: v3.05 gap-remediation-tasklist.md T11
- **Description**:
  Create `tests/roadmap/test_convergence_e2e.py` with 6 tests:
  - **SC-1**: `test_sc1_registry_persistence` — write registry, reload, verify findings survive.
  - **SC-2**: `test_sc2_monotonic_progress` — run 3 cycles, verify HIGHs never increase or regression triggers.
  - **SC-3**: `test_sc3_budget_exhaustion` — set budget to CHECKER_COST+1, verify halt after 1 run.
  - **SC-4**: `test_sc4_regression_handling` — inject increasing HIGHs, verify `handle_regression` called.
  - **SC-5**: `test_sc5_convergence_pass` — inject 0 HIGHs on run 2, verify `passed=True` and credit applied.
  - **SC-6**: `test_sc6_semantic_fluctuation` — vary semantic HIGHs, verify no halt (warning only).
  Use real `DeviationRegistry` and `execute_fidelity_with_convergence()` with mock checkers. Mark `@pytest.mark.integration`.
- **Depends on**: OT-04
- **Acceptance criteria**: All 6 tests pass.
- **Risk**: E2E tests may be slower. Use `tmp_path`.
- **Wave**: 2

---

## Wave 3: v3.1 Integration Test

### Task OT-08: Integration test for `execute_sprint()` production path (v3.1-T11)
- **Type**: test
- **Target file(s)**: New: `tests/sprint/test_execute_sprint_integration.py`
- **Source**: v3.1 gap-remediation-tasklist.md T11
- **Description**:
  Write a test exercising `execute_sprint()` end-to-end with mocked `ClaudeProcess`:
  1. Create `SprintConfig` with at least one phase.
  2. Mock `ClaudeProcess` to simulate success.
  3. Call `execute_sprint(config)`.
  4. Assert: TurnLedger constructed, ShadowGateMetrics constructed, DeferredRemediationLog constructed, SprintGatePolicy constructed, `build_kpi_report()` called, `gate-kpi-report.md` written.
  Pattern after `tests/sprint/test_e2e_success.py`.
- **Depends on**: OT-01, OT-02 (wiring must be in place)
- **Acceptance criteria**: Test passes: `uv run pytest tests/sprint/test_execute_sprint_integration.py -v`.
- **Risk**: Mocking complexity.
- **Wave**: 3

---

## Wave 4: v3.2 Tests

### Task OT-09: Budget scenario tests 5-8 (v3.2-T13)
- **Type**: test
- **Target file(s)**: `tests/sprint/test_wiring_budget_scenarios.py` (new)
- **Source**: v3.2 gap-remediation-tasklist.md T13
- **Description**:
  Create 4 labeled budget scenario tests:
  - `test_scenario_5_credit_floor_to_zero` — `int(1 * 0.8) = 0`, verify single-turn credit is a no-op.
  - `test_scenario_6_blocking_remediation_lifecycle` — format -> debit -> recheck cycle.
  - `test_scenario_7_null_ledger_passthrough` — `ledger=None` doesn't crash.
  - `test_scenario_8_shadow_deferred_log` — shadow findings populate `DeferredRemediationLog`.
- **Depends on**: OT-01
- **Acceptance criteria**: All 4 tests pass.
- **Wave**: 4

---

### Task OT-10: Integration test — `execute_sprint()` TurnLedger threading (v3.2-T17)
- **Type**: test
- **Target file(s)**: `tests/sprint/test_wiring_integration.py` (extend or new)
- **Source**: v3.2 gap-remediation-tasklist.md T17
- **Description**:
  Create tests:
  - `test_execute_sprint_creates_turnledger`
  - `test_post_phase_hook_called_per_phase`
  - `test_turnledger_budget_debit_across_phases`
  - `test_shadow_findings_logged_to_remediation_log`
- **Depends on**: OT-01
- **Acceptance criteria**: All 4 tests pass.
- **Wave**: 4

---

### Task OT-11: Unit test — `_resolve_wiring_mode()` activation (v3.2-T18)
- **Type**: test
- **Target file(s)**: `tests/sprint/test_wiring_mode_resolution.py` (new)
- **Source**: v3.2 gap-remediation-tasklist.md T18
- **Description**:
  Create tests verifying `_resolve_wiring_mode()` call chain:
  - `test_resolve_uses_scope_when_set` — `wiring_gate_scope="task"` resolves via `resolve_gate_mode()`.
  - `test_resolve_falls_back_to_direct_mode` — `wiring_gate_scope="none"` uses `config.wiring_gate_mode`.
  - `test_grace_period_forces_shadow` — `grace_period >= SHADOW_GRACE_INFINITE` -> "shadow".
  - `test_enabled_false_forces_off` — `wiring_gate_enabled=False` -> "off".
- **Depends on**: none
- **Acceptance criteria**: All 4 tests pass.
- **Wave**: 4

---

### Task OT-12: KPI and contract verification tests (v3.2-T19)
- **Type**: test
- **Target file(s)**: `tests/sprint/test_kpi_contract.py` (new)
- **Source**: v3.2 gap-remediation-tasklist.md T19
- **Description**:
  - `test_kpi_report_has_all_spec_fields` — `GateKPIReport` has `wiring_analyses_run`, `wiring_remediations_attempted`, `wiring_net_cost`.
  - `test_kpi_net_cost_computed` — `net_cost = used - credited`.
  - `test_kpi_format_report_includes_new_fields` — `format_report()` output contains new field labels.
  - `test_frontmatter_fields_documented` — `emit_report()` docstring contains mapping table.
- **Depends on**: none
- **Acceptance criteria**: All 4 tests pass.
- **Wave**: 4

---

### Task OT-13: E2E shadow mode pipeline test (v3.2-T20)
- **Type**: test
- **Target file(s)**: `tests/integration/test_wiring_e2e_shadow.py` (new)
- **Source**: v3.2 gap-remediation-tasklist.md T20
- **Description**:
  End-to-end test: configure shadow mode -> run a phase -> verify shadow findings logged to `DeferredRemediationLog` -> verify KPI report includes shadow metrics.
- **Depends on**: OT-01, OT-09
- **Acceptance criteria**: Test passes end-to-end.
- **Wave**: 4

---

### Task OT-14: Performance benchmark test (v3.2-T15)
- **Type**: test
- **Target file(s)**: `tests/sprint/test_wiring_performance.py` (new)
- **Source**: v3.2 gap-remediation-tasklist.md T15
- **Description**:
  - `test_performance_p95_under_5s` — Run wiring analysis 20 times on a synthetic codebase, assert P95 < 5s.
  Mark `@pytest.mark.slow`.
- **Depends on**: none
- **Acceptance criteria**: P95 < 5s on test hardware.
- **Wave**: 4

---

## Wave 5: Final Validation

### Task OT-15: Smoke test convergence path (v3.05-T12)
- **Type**: verify
- **Target file(s)**: `src/superclaude/cli/roadmap/executor.py`
- **Source**: v3.05 gap-remediation-tasklist.md T12
- **Description**:
  1. Create minimal test spec and roadmap in `tmp_path`.
  2. Invoke `_run_convergence_spec_fidelity()` with a real `RoadmapConfig`.
  3. Verify no runtime exceptions, valid `StepResult`, registry JSON written.
- **Depends on**: OT-04, OT-07
- **Acceptance criteria**: No `TypeError`, `AttributeError`, or runtime exceptions.
- **Wave**: 5

---

### Task OT-16: Regenerate wiring-verification artifact (v3.05-T14)
- **Type**: verify
- **Target file(s)**: `.dev/releases/complete/v3.05_DeterministicFidelityGates/wiring-verification.md`
- **Source**: v3.05 gap-remediation-tasklist.md T14
- **Description**:
  After OT-05 confirms the target directory fix, re-run wiring verification. Verify `files_analyzed > 0`.
- **Depends on**: OT-05
- **Acceptance criteria**: `files_analyzed > 0` in regenerated artifact.
- **Wave**: 5

---

### Task OT-17: Full regression suite (v3.2-T21)
- **Type**: verify
- **Target file(s)**: All test files
- **Source**: v3.2 gap-remediation-tasklist.md T21
- **Description**:
  Run `uv run pytest tests/ -v --tb=short`. Verify 0 new failures beyond the 3 pre-existing ones (credential scanner, 2 wiring pipeline step-count tests).
- **Depends on**: All previous tasks
- **Acceptance criteria**: `uv run pytest tests/` exits with same baseline (3 pre-existing failures).
- **Wave**: 5

---

## Wave 6: Audit

### Task OT-18: Gap closure audit (v3.2-T22)
- **Type**: verify
- **Target file(s)**: All 3 `gap-remediation-tasklist.md` files
- **Source**: v3.2 gap-remediation-tasklist.md T22
- **Description**:
  1. Review all 3 gap-remediation tasklists.
  2. For each task, mark status: DONE / SKIPPED / OUTSTANDING.
  3. For each gap in the original `roadmap-gap-analysis-merged.md` files, verify it is now closed.
  4. Produce a closure summary with remaining open items.
- **Depends on**: All previous tasks
- **Acceptance criteria**: All gaps have a disposition (closed, documented-as-deferred, or new-ticket).
- **Wave**: 6

---

## Quick Reference: Task Origin Mapping

| Outstanding Task | Original Release | Original Task ID | Type |
|-----------------|-----------------|-------------------|------|
| OT-01 | v3.2 | T02 | fix (1 line) |
| OT-02 | v3.1 | T04 | refactor (architectural) |
| OT-03 | v3.1 | T05 | refactor (return types) |
| OT-04 | v3.05 | T07 | test (7 new tests) |
| OT-05 | v3.05 | T08 | verify |
| OT-06 | v3.05 | T10 partial | fix (log message) |
| OT-07 | v3.05 | T11 | test (6 new tests) |
| OT-08 | v3.1 | T11 | test (integration) |
| OT-09 | v3.2 | T13 | test (4 scenarios) |
| OT-10 | v3.2 | T17 | test (4 integration) |
| OT-11 | v3.2 | T18 | test (4 unit) |
| OT-12 | v3.2 | T19 | test (4 contract) |
| OT-13 | v3.2 | T20 | test (E2E) |
| OT-14 | v3.2 | T15 | test (benchmark) |
| OT-15 | v3.05 | T12 | verify (smoke) |
| OT-16 | v3.05 | T14 | verify (regenerate) |
| OT-17 | v3.2 | T21 | verify (regression) |
| OT-18 | v3.2 | T22 | verify (audit) |

## Wave Execution Summary

| Wave | Tasks | Type | Parallelism |
|------|-------|------|-------------|
| 1 | OT-01, OT-02, OT-03 | Blocking fixes | OT-01 parallel with OT-02; OT-03 depends on OT-02 |
| 2 | OT-04, OT-05, OT-06, OT-07 | v3.05 tests + fixes | All parallel |
| 3 | OT-08 | v3.1 integration test | Sequential (needs Wave 1) |
| 4 | OT-09 through OT-14 | v3.2 tests | All parallel |
| 5 | OT-15, OT-16, OT-17 | Final validation | Sequential |
| 6 | OT-18 | Audit | Sequential |
