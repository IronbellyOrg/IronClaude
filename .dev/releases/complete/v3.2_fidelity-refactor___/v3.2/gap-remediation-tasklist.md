# Gap Remediation Tasklist: v3.2 Wiring Verification Gate

**Generated**: 2026-03-21
**Source**: `roadmap-gap-analysis-merged.md` (Agent A + Agent B adversarial merge)
**Total tasks**: 22
**Waves**: 7 (4 implementation, 3 verification)
**Critical path**: Wave 1 -> Wave 2 -> Wave 3 -> V1 -> Wave 4 -> V2 -> V3

---

## Recommendation-to-Task Mapping

| Rec # | Priority | Recommendation | Task IDs |
|-------|----------|---------------|----------|
| R1 | P0 | Wire `execute_sprint()` to TurnLedger | T01, T02 |
| R2 | P0 | Activate `_resolve_wiring_mode()` | T03 |
| R3 | P0 | Wire DeferredRemediationLog into shadow mode | T04, T05 |
| R4 | P0 | Fix BLOCKING remediation (implement or remove debit) | T06, T07, T08 |
| R5 | P1 | Add SprintConfig scope-based fields | T09 |
| R6 | P1 | Add missing KPI fields | T10 |
| R7 | P1 | Align frontmatter contract | T11 |
| R8 | P2 | Add `check_wiring_report()` convenience wrapper | T12 |
| R9 | P2 | Add labeled budget scenario tests 5-8 | T13 |
| R10 | P2 | Add retrospective validation artifact (T11) | T14 |
| R11 | P2 | Add performance benchmark test (SC-009) | T15 |
| R12 | P2 | Fix migration shim targets | T16 |

---

## Dependency Graph

```
Wave 1 (P0 foundations):
  T01 ─┐
  T03  │
  T09  │
       │
Wave 2 (P0 wiring):
  T02 ←┤ (depends on T01)
  T04  │
  T06  │
       │
Wave 3 (P0 completions):
  T05 ←── (depends on T04)
  T07 ←── (depends on T06)
  T08 ←── (depends on T06)
       │
V1 - Verification:
  T17 ←── (depends on T01-T08)
  T18 ←── (depends on T03, T09)
       │
Wave 4 (P1 + P2):
  T10, T11, T12, T13, T14, T15, T16
       │
V2 - Integration verification:
  T19 ←── (depends on T10-T16)
  T20 ←── (depends on all implementation)
       │
V3 - Final:
  T21 ←── (depends on all)
  T22 ←── (depends on all)
```

---

## Wave 1: P0 Foundations (parallel)

### Task T01: Create post-phase wiring hook for execute_sprint()

- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Description**:
  1. Create a new function `run_post_phase_wiring_hook(phase, config, phase_result, ledger)` that adapts the existing per-task `run_post_task_wiring_hook()` logic for phase-level execution.
  2. The function should:
     - Accept a `PhaseResult` instead of `TaskResult`
     - Create a synthetic `TaskEntry` from the phase (task_id=f"phase-{phase.number}", title=phase.file.name)
     - Create a synthetic `TaskResult` wrapping the `PhaseResult` status
     - Delegate to `run_post_task_wiring_hook()` for actual analysis
     - Map the returned `TaskResult` status back onto the `PhaseResult`
  3. Place this function between `run_post_task_anti_instinct_hook()` (ends ~line 688) and `execute_phase_tasks()` (starts line 689).
  4. Import `PhaseResult` and `Phase` at the top of the function to avoid circular imports.
- **Source recommendation**: R1 (option B: post-phase hooks after each subprocess completes)
- **Depends on**: none
- **Acceptance criteria**:
  - Function exists and is importable
  - Creates valid synthetic TaskEntry/TaskResult from PhaseResult
  - Delegates to existing `run_post_task_wiring_hook()` (no logic duplication)
  - Unit test passes with mock wiring analysis
- **Risk**: Synthetic TaskEntry may not have all required fields; verify TaskEntry's required fields in models.py
- **Wave**: 1

---

### Task T02: Wire post-phase hook into execute_sprint() main loop

- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Description**:
  1. In `execute_sprint()` (line 843+), instantiate a `TurnLedger` before the phase loop begins:
     ```python
     ledger = TurnLedger(initial_budget=config.max_turns)
     ```
  2. After each phase subprocess completes and the `PhaseResult` is recorded (around line 942+, after `sprint_result.phase_results.append(phase_result)`), insert:
     ```python
     phase_result = run_post_phase_wiring_hook(phase, config, phase_result, ledger)
     ```
  3. Pass `ledger` to `build_kpi_report()` at sprint completion.
  4. Ensure null-ledger guard patterns match the existing style (check `if ledger is not None`).
- **Source recommendation**: R1 (option B)
- **Depends on**: T01
- **Acceptance criteria**:
  - `execute_sprint()` creates a TurnLedger
  - Post-phase wiring hook is called after every non-skipped, non-python phase
  - TurnLedger budget is debited/credited correctly across phases
  - Existing tests still pass (`uv run pytest tests/ -v`)
- **Risk**: TurnLedger budget parameters (initial_budget, minimum_allocation) may need tuning for phase-level granularity vs task-level. The default `minimum_allocation=5` may be too high for phase-level where only 1 turn per analysis is debited.
- **Wave**: 2

---

### Task T03: Activate _resolve_wiring_mode() in run_post_task_wiring_hook()

- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Description**:
  1. In `run_post_task_wiring_hook()` at line 473, replace:
     ```python
     mode = config.wiring_gate_mode
     ```
     with:
     ```python
     mode = _resolve_wiring_mode(config)
     ```
  2. This is a one-line change. The `_resolve_wiring_mode()` function already exists at lines 420-446 and correctly implements Goal-5d scope-based resolution with fallback to `config.wiring_gate_mode`.
  3. Verify the import of `_resolve_wiring_mode` is not needed (it's a module-level function in the same file).
- **Source recommendation**: R2
- **Depends on**: none
- **Acceptance criteria**:
  - `_resolve_wiring_mode(config)` is called instead of direct field access
  - When `config.wiring_gate_scope` is "release"/"milestone"/"task", the function resolves via `resolve_gate_mode()` from trailing_gate.py
  - When `config.wiring_gate_scope` is unrecognized, falls back to `config.wiring_gate_mode`
  - Existing test suite passes
- **Risk**: Minimal. The function already exists and has a safe fallback. The only risk is if `resolve_gate_mode()` in trailing_gate.py has side effects or requires state not present at hook time. Verify `GateScope` and `GateMode` imports resolve correctly.
- **Wave**: 1

---

### Task T09: Add SprintConfig scope-based fields

- **Type**: refactor
- **Target file(s)**: `src/superclaude/cli/sprint/models.py`
- **Description**:
  1. Add three new fields to `SprintConfig` (after line 329):
     ```python
     wiring_gate_enabled: bool = True
     wiring_gate_grace_period: int = 0
     ```
  2. Add a module-level constant:
     ```python
     SHADOW_GRACE_INFINITE: int = 999_999
     ```
  3. In `SprintConfig.__post_init__()` (line 331+), add backward-compatibility logic after the existing migration shim:
     ```python
     # Derive wiring_gate_mode from scope-based fields for backward compatibility
     if not self.wiring_gate_enabled:
         object.__setattr__(self, "wiring_gate_mode", "off")
     elif self.wiring_gate_grace_period >= SHADOW_GRACE_INFINITE:
         object.__setattr__(self, "wiring_gate_mode", "shadow")
     ```
  4. Update `_resolve_wiring_mode()` in executor.py to use `wiring_gate_grace_period` as the `grace_period` argument to `resolve_gate_mode()` (currently hardcoded to 0 at line 439).
- **Source recommendation**: R5
- **Depends on**: none
- **Acceptance criteria**:
  - `SprintConfig` has `wiring_gate_enabled` and `wiring_gate_grace_period` fields
  - `SHADOW_GRACE_INFINITE` constant is importable from `models.py`
  - Setting `wiring_gate_enabled=False` results in `wiring_gate_mode="off"` after `__post_init__`
  - Setting `wiring_gate_grace_period=999_999` results in `wiring_gate_mode="shadow"` after `__post_init__`
  - `_resolve_wiring_mode()` passes `grace_period` to `resolve_gate_mode()`
- **Risk**: The `__post_init__` derivation may conflict with explicitly-set `wiring_gate_mode`. Define precedence: explicit mode string wins over derived mode. Add a guard: only derive if `wiring_gate_mode` was not explicitly passed.
- **Wave**: 1

---

## Wave 2: P0 Wiring (parallel, depends on Wave 1 items as noted)

### Task T04: Create DeferredRemediationLog adapter for shadow mode findings

- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Description**:
  1. Create a helper function `_log_shadow_findings_to_remediation_log(report, task, config)`:
     ```python
     def _log_shadow_findings_to_remediation_log(
         report: WiringReport,
         task: TaskEntry,
         config: SprintConfig,
         remediation_log: DeferredRemediationLog | None = None,
     ) -> None:
     ```
  2. Inside the function:
     - If `remediation_log is None`, return early (no-op when log unavailable)
     - For each finding in `report.unsuppressed_findings`, construct a synthetic `TrailingGateResult`:
       ```python
       from superclaude.cli.pipeline.trailing_gate import TrailingGateResult
       gate_result = TrailingGateResult(
           gate_name="WIRING_GATE",
           passed=False,
           message=f"[shadow] {finding.finding_type}: {finding.summary}",
           task_id=task.task_id,
       )
       remediation_log.append(gate_result)
       ```
  3. Place this function near `run_post_task_wiring_hook()`.
- **Source recommendation**: R3
- **Depends on**: none
- **Acceptance criteria**:
  - Function exists and handles None remediation_log gracefully
  - Each unsuppressed finding produces one `TrailingGateResult` entry
  - `TrailingGateResult` fields are populated correctly (verify constructor signature in `trailing_gate.py`)
- **Risk**: `TrailingGateResult` constructor may require fields beyond `gate_name`, `passed`, `message`, `task_id`. Read `trailing_gate.py:TrailingGateResult` to confirm required fields before implementation.
- **Wave**: 2

---

### Task T05: Wire shadow findings adapter into run_post_task_wiring_hook()

- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Description**:
  1. Add `remediation_log: DeferredRemediationLog | None = None` parameter to `run_post_task_wiring_hook()` signature (line 449).
  2. In the shadow mode branch (line 519-530), after the existing `_wiring_logger.info()` call and before the `return task_result`, insert:
     ```python
     _log_shadow_findings_to_remediation_log(report, task, config, remediation_log)
     ```
  3. Update the call site in `execute_phase_tasks()` (line 788) to pass the remediation_log:
     ```python
     result = run_post_task_wiring_hook(task, config, result, ledger=ledger, remediation_log=remediation_log)
     ```
  4. Add `remediation_log` parameter to `execute_phase_tasks()` signature (line 689) and thread it through.
  5. Also update the call in the new `run_post_phase_wiring_hook()` (from T01) to pass remediation_log.
- **Source recommendation**: R3
- **Depends on**: T04
- **Acceptance criteria**:
  - Shadow mode findings are appended to `DeferredRemediationLog`
  - `DeferredRemediationLog` entries contain gate_name="WIRING_GATE", passed=False, and finding details
  - When `remediation_log` is None, behavior is unchanged (backward compatible)
  - The trailing gate pipeline can read these entries for rollout promotion decisions
- **Risk**: Threading `remediation_log` through multiple function signatures is intrusive. Verify all call sites of `execute_phase_tasks()` and `run_post_task_wiring_hook()` are updated.
- **Wave**: 3

---

### Task T06: Implement _format_wiring_failure() helper

- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Description**:
  1. Create `_format_wiring_failure(report, task, config)` that returns a formatted remediation prompt string:
     ```python
     def _format_wiring_failure(
         report: WiringReport,
         task: TaskEntry,
         config: SprintConfig,
     ) -> str:
     ```
  2. The function should format a prompt containing:
     - Task ID and title
     - Number of blocking findings by type (unwired_callable, orphan_module, registry_mismatch)
     - For each blocking finding: the file path, callable name, and suggested fix
     - A closing instruction: "Fix these wiring issues and re-run the task."
  3. Use `report.unsuppressed_findings` filtered by `finding.severity in ("critical", "major")` for blocking findings.
  4. Place near `run_post_task_wiring_hook()`.
- **Source recommendation**: R4 (option A, part 1 of 3)
- **Depends on**: none
- **Acceptance criteria**:
  - Returns a non-empty string when blocking findings exist
  - Returns an empty string when no blocking findings exist
  - Output is parseable by a Claude subprocess (plain text, no special formatting)
  - Unit test verifies format with mock WiringReport containing mixed severity findings
- **Risk**: WiringFinding field names may differ from assumed. Verify `WiringFinding` dataclass fields in `wiring_gate.py` before implementation.
- **Wave**: 2

---

### Task T07: Implement _recheck_wiring() helper

- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Description**:
  1. Create `_recheck_wiring(config, source_dir, mode)` that re-runs wiring analysis and returns pass/fail:
     ```python
     def _recheck_wiring(
         config: SprintConfig,
         source_dir: Path,
         mode: str,
     ) -> tuple[bool, WiringReport | None]:
     ```
  2. The function should:
     - Create a fresh `WiringConfig(rollout_mode=mode)`
     - Call `run_wiring_analysis(wiring_config, source_dir)`
     - Return `(True, report)` if `report.blocking_count(mode) == 0`
     - Return `(False, report)` if blocking findings remain
     - Catch exceptions and return `(False, None)` with a warning log
  3. Place near `_format_wiring_failure()`.
- **Source recommendation**: R4 (option A, part 2 of 3)
- **Depends on**: T06
- **Acceptance criteria**:
  - Returns `(True, report)` when no blocking findings remain after remediation
  - Returns `(False, report)` when blocking findings persist
  - Exception handling prevents crashes from propagating
  - Unit test with mocked `run_wiring_analysis` verifying both paths
- **Risk**: Re-running analysis on the same source_dir without actual code changes will produce the same results. In practice, this is called after a remediation subprocess has modified files. Test with fixture that simulates file changes between calls.
- **Wave**: 3

---

### Task T08: Wire remediation lifecycle into BLOCKING path

- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Description**:
  1. In the `full` mode branch of `run_post_task_wiring_hook()` (lines 548-580), replace the debit-only remediation block with full lifecycle:
     ```python
     if ledger is not None:
         can_remediate = ledger.can_remediate
         if can_remediate():
             # Step 1: Format remediation prompt
             prompt = _format_wiring_failure(report, task, config)
             if prompt:
                 # Step 2: Debit remediation cost
                 ledger.debit(config.remediation_cost)
                 _wiring_logger.info(
                     "Full mode: remediation debited %d turns for task %s",
                     config.remediation_cost, task.task_id,
                 )
                 # Step 3: Call attempt_remediation from trailing_gate.py
                 from superclaude.cli.pipeline.trailing_gate import attempt_remediation
                 remediation_result = attempt_remediation(
                     prompt=prompt,
                     config=config,
                     task=task,
                 )
                 # Step 4: Recheck wiring after remediation
                 passed, recheck_report = _recheck_wiring(config, config.release_dir, mode)
                 if passed:
                     task_result.status = TaskStatus.PASS
                     task_result.gate_outcome = GateOutcome.PASS
                     if ledger is not None:
                         ledger.credit_wiring(config.wiring_analysis_turns)
                     _wiring_logger.info("Remediation succeeded for task %s", task.task_id)
                 else:
                     _wiring_logger.warning("Remediation failed for task %s — FAIL persists", task.task_id)
         else:
             _wiring_logger.warning(
                 "Full mode: BUDGET_EXHAUSTED for task %s remediation", task.task_id,
             )
     ```
  2. Note: The exact `attempt_remediation()` signature must be verified from `trailing_gate.py` (line 354). It may use `gate_result` and `policy` parameters instead of `prompt`. Adapt the call accordingly. If `attempt_remediation()` cannot be used directly, invoke `SprintGatePolicy.build_remediation_step()` (exists at executor.py:66) and execute the step.
- **Source recommendation**: R4 (option A, part 3 of 3)
- **Depends on**: T06, T07
- **Acceptance criteria**:
  - BLOCKING path calls `_format_wiring_failure()` to build prompt
  - Budget is debited before remediation attempt
  - `_recheck_wiring()` is called after remediation
  - On recheck pass: task status reverts to PASS, turns credited
  - On recheck fail: task status remains FAIL
  - Budget exhaustion path still logs warning and skips remediation
  - Unit test covering: remediation success, remediation failure, budget exhaustion
- **Risk**: `attempt_remediation()` in trailing_gate.py may have a different interface than assumed. Read its full signature before implementing. If incompatible, use `SprintGatePolicy.build_remediation_step()` instead and execute the returned Step via subprocess.
- **Wave**: 3

---

## Verification Wave V1 (depends on Waves 1-3)

### Task T17: Integration test — execute_sprint() TurnLedger threading

- **Type**: test
- **Target file(s)**: `tests/audit/test_wiring_integration.py` (extend existing)
- **Description**:
  1. Add a test class `TestExecuteSprintTurnLedger` with tests:
     - `test_execute_sprint_creates_turnledger`: Mock subprocess execution, verify TurnLedger is instantiated
     - `test_post_phase_hook_called_per_phase`: Verify `run_post_phase_wiring_hook()` is called after each phase
     - `test_turnledger_budget_debit_across_phases`: Run 3 mock phases, verify cumulative debit matches expected
     - `test_shadow_findings_logged_to_remediation_log`: Verify DeferredRemediationLog receives entries in shadow mode
  2. Use `unittest.mock.patch` to mock `ClaudeProcess`, `run_wiring_analysis`, and subprocess calls.
  3. Create SprintConfig with `wiring_gate_mode="shadow"` and a small `max_turns=10`.
- **Source recommendation**: R1, R3 (verification)
- **Depends on**: T01, T02, T04, T05
- **Acceptance criteria**:
  - All 4 tests pass
  - Tests are deterministic (no real subprocess calls)
  - Tests verify both the happy path and budget-exhaustion path
- **Risk**: Mocking `execute_sprint()` internals may be brittle if the function structure changes. Mock at the subprocess boundary, not internal function calls.
- **Wave**: V1

---

### Task T18: Unit test — _resolve_wiring_mode() activation

- **Type**: test
- **Target file(s)**: `tests/audit/test_wiring_integration.py` (extend existing)
- **Description**:
  1. Add tests verifying `_resolve_wiring_mode()` is actually called:
     - `test_resolve_wiring_mode_called_in_hook`: Patch `_resolve_wiring_mode` and verify it's called when `run_post_task_wiring_hook()` executes
     - `test_resolve_wiring_mode_scope_release`: config with `wiring_gate_scope="release"` returns expected mode
     - `test_resolve_wiring_mode_scope_unknown`: config with unknown scope falls back to `config.wiring_gate_mode`
     - `test_scope_fields_derive_mode`: config with `wiring_gate_enabled=False` results in mode="off"
     - `test_grace_period_infinite`: config with `wiring_gate_grace_period=999_999` results in mode="shadow"
- **Source recommendation**: R2, R5 (verification)
- **Depends on**: T03, T09
- **Acceptance criteria**:
  - All 5 tests pass
  - Tests verify the call chain, not just the function in isolation
- **Risk**: Patching module-level functions requires correct import path. Use `patch('superclaude.cli.sprint.executor._resolve_wiring_mode')`.
- **Wave**: V1

---

## Wave 4: P1 + P2 Features (parallel)

### Task T10: Add missing KPI fields

- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/sprint/kpi.py`
- **Description**:
  1. Add three new fields to `GateKPIReport` (after line 52):
     ```python
     wiring_net_cost: int = 0          # wiring_turns_used - wiring_turns_credited
     wiring_analyses_run: int = 0       # count of wiring analyses executed
     wiring_remediations_attempted: int = 0  # count of remediation attempts
     ```
  2. Make `wiring_net_cost` a computed property instead of a stored field:
     ```python
     @property
     def wiring_net_cost(self) -> int:
         return self.wiring_turns_used - self.wiring_turns_credited
     ```
  3. In `build_kpi_report()` (line 137+), populate the new counter fields from `turn_ledger` and `wiring_report`:
     - `wiring_analyses_run`: count from TurnLedger wiring debit events, or from a new counter field
     - `wiring_remediations_attempted`: count from DeferredRemediationLog entries with gate_name="WIRING_GATE"
  4. Update `format_report()` to include the new fields in output.
- **Source recommendation**: R6
- **Depends on**: none
- **Acceptance criteria**:
  - `GateKPIReport` has all 3 new fields
  - `wiring_net_cost` correctly computes `used - credited`
  - `build_kpi_report()` populates counters from available data
  - `format_report()` displays all wiring KPI fields
- **Risk**: Making `wiring_net_cost` a property on a dataclass requires it to not be in `__init__`. Use `field(init=False)` pattern or make it a plain `@property`.
- **Wave**: 4

---

### Task T11: Document frontmatter contract alignment

- **Type**: verify
- **Target file(s)**: `src/superclaude/cli/audit/wiring_gate.py` (line 715-866, `emit_report()`)
- **Description**:
  1. Read the 16-field frontmatter schema in `emit_report()`.
  2. Create a mapping table between the 16 implementation fields and the 12 spec fields.
  3. Add a docstring block in `emit_report()` documenting:
     - Which 12 spec fields map to which implementation fields
     - Which 4 extra implementation fields exist and why (OQ resolutions)
     - The field name differences (e.g., spec's `findings_count` vs impl's `total_findings`)
  4. This is documentation-only; no behavioral changes. The merged report recommends updating the spec to match implementation since implementation is a superset.
- **Source recommendation**: R7
- **Depends on**: none
- **Acceptance criteria**:
  - `emit_report()` has a clear docstring mapping all 16 fields to spec fields
  - Any future spec update can reference this mapping
- **Risk**: None (documentation only).
- **Wave**: 4

---

### Task T12: Add check_wiring_report() convenience wrapper

- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/audit/wiring_gate.py`
- **Description**:
  1. Add a new public function after the `WIRING_GATE` constant (after line 1026):
     ```python
     def check_wiring_report(report: WiringReport, mode: str = "full") -> tuple[bool, list[str]]:
         """Convenience wrapper running all 5 semantic checks from WIRING_GATE.

         Returns (passed, list_of_failure_messages).
         Spec reference: Section 6.1 / OQ-10.
         """
         failures = []
         for check in WIRING_GATE["checks"]:
             result = check["fn"](report, mode)
             if not result:
                 failures.append(check["name"])
         return (len(failures) == 0, failures)
     ```
  2. Verify the exact structure of `WIRING_GATE["checks"]` — the dict keys may differ. Read lines 973-1026 to confirm the check function signatures.
  3. Export from `__init__.py` if the module has one.
- **Source recommendation**: R8
- **Depends on**: none
- **Acceptance criteria**:
  - `check_wiring_report(report)` returns `(True, [])` when all checks pass
  - Returns `(False, ["check_name", ...])` listing failed checks
  - Unit test with a clean report (all pass) and a dirty report (some fail)
- **Risk**: `WIRING_GATE` structure may not have a simple `checks` list with `fn` callables. Read the actual constant definition to adapt the iteration pattern.
- **Wave**: 4

---

### Task T13: Add labeled budget scenario tests 5-8

- **Type**: test
- **Target file(s)**: `tests/audit/test_wiring_integration.py`
- **Description**:
  1. Add four explicitly-named test methods:
     - `test_scenario_5_credit_floor_to_zero`: Verify `credit_wiring(1, rate=0.8)` returns 0 credits (floor arithmetic)
     - `test_scenario_6_blocking_remediation_lifecycle`: Full mode with blocking findings triggers remediation, debit, recheck
     - `test_scenario_7_null_ledger_passthrough`: All hook functions work correctly when `ledger=None`
     - `test_scenario_8_shadow_deferred_log`: Shadow mode appends findings to DeferredRemediationLog
  2. Each test should reference the budget scenario number in its docstring.
  3. Use existing test fixtures from `tests/audit/` where available.
- **Source recommendation**: R9
- **Depends on**: none (tests can be written against current + expected interfaces)
- **Acceptance criteria**:
  - All 4 tests pass after implementation tasks are complete
  - Tests are clearly labeled with scenario numbers
  - Each test has an assertion that fails if the feature regresses
- **Risk**: Scenario 6 depends on T06-T08 being complete. Write the test now but expect it to fail until remediation lifecycle is implemented. Mark with `@pytest.mark.xfail` initially if needed.
- **Wave**: 4

---

### Task T14: Add retrospective validation artifact (T11)

- **Type**: verify
- **Target file(s)**: `tests/audit/test_wiring_integration.py`
- **Description**:
  1. Add a test `test_retrospective_cli_portify_detection`:
     - Point the wiring gate at the actual `src/superclaude/cli/cli_portify/` directory
     - Run `run_wiring_analysis()` against it
     - Assert that the original wiring bug (that motivated v3.2) is detected
  2. The test should document what the original bug was in its docstring.
  3. If the original bug has been fixed, the test should verify zero findings (demonstrating the fix works).
- **Source recommendation**: R10
- **Depends on**: none
- **Acceptance criteria**:
  - Test runs against real codebase directory
  - Test documents the retrospective finding
  - Test passes (either detecting the bug or confirming it's fixed)
- **Risk**: The `cli_portify/` directory may have changed since the original bug. The test should be resilient to directory structure changes.
- **Wave**: 4

---

### Task T15: Add performance benchmark test (SC-009)

- **Type**: test
- **Target file(s)**: `tests/audit/test_wiring_gate.py` (extend existing)
- **Description**:
  1. Add a test `test_performance_p95_under_5s`:
     - Create a temporary directory with 50 Python files (simple stubs)
     - Run `run_wiring_analysis()` against it
     - Assert `report.scan_duration_seconds < 5.0`
  2. Mark with `@pytest.mark.slow` so it can be excluded from fast test runs.
  3. Run the test 10 times and assert p95 (9th sorted value) < 5.0 seconds.
- **Source recommendation**: R11
- **Depends on**: none
- **Acceptance criteria**:
  - Test creates 50-file fixture directory
  - p95 latency is under 5 seconds
  - Test is marked `@pytest.mark.slow`
- **Risk**: CI environments may be slower than local. Use a generous margin (e.g., 5s not 2s) and document that the benchmark is environment-dependent.
- **Wave**: 4

---

### Task T16: Fix migration shim targets

- **Type**: refactor
- **Target file(s)**: `src/superclaude/cli/sprint/models.py`
- **Description**:
  1. Read the spec's intended deprecation path. The current shim (lines 340-355) migrates:
     - `wiring_budget_turns` -> `wiring_analysis_turns`
     - `wiring_remediation_cost` -> `remediation_cost`
     - `wiring_scope` -> `wiring_gate_scope`
  2. The spec intended the shim to handle:
     - `wiring_gate_mode` (old string-switch) -> derived from `wiring_gate_enabled` + `wiring_gate_grace_period` (new scope-based)
  3. Add the spec-intended migration entry to `_OLD_TO_NEW`:
     ```python
     # When old config uses wiring_gate_mode directly, map to new enabled/grace pattern
     ```
  4. However, since `wiring_gate_mode` is still actively used as the resolved output, this migration is complex. Instead, add a docstring to the shim block explaining:
     - Which fields the shim currently migrates and why
     - Which fields the spec intended and why they differ
     - That the current shim is intentional (migrating internal renames from early development)
  5. If the team decides to adopt spec's deprecation path fully, the migration would be: old `wiring_gate_mode="off"` -> `wiring_gate_enabled=False`; old `wiring_gate_mode="shadow"` -> `wiring_gate_grace_period=SHADOW_GRACE_INFINITE`. But this requires T09 to be complete first.
- **Source recommendation**: R12
- **Depends on**: T09 (for full implementation; documentation-only portion has no dependency)
- **Acceptance criteria**:
  - Migration shim has clear documentation of current vs spec-intended targets
  - If full migration is implemented: old `wiring_gate_mode` values map to new scope-based fields
  - Existing migration paths still work (backward compatible)
  - Deprecation warnings still fire for old field names
- **Risk**: Changing migration targets could break existing configs that use the old field names. Test with fixture configs using deprecated names.
- **Wave**: 4

---

## Verification Wave V2 (depends on Wave 4)

### Task T19: KPI and contract verification

- **Type**: verify
- **Target file(s)**: `tests/audit/test_wiring_integration.py`
- **Description**:
  1. Add tests for KPI completeness:
     - `test_kpi_report_has_all_spec_fields`: Assert `GateKPIReport` has all 9 fields (6 original + 3 new)
     - `test_kpi_net_cost_computed`: Verify `wiring_net_cost` = `wiring_turns_used - wiring_turns_credited`
     - `test_kpi_format_report_includes_new_fields`: Verify `format_report()` output contains "net cost", "analyses run", "remediations attempted"
  2. Add test for frontmatter contract:
     - `test_frontmatter_fields_documented`: Assert `emit_report()` docstring contains mapping table
- **Source recommendation**: R6, R7 (verification)
- **Depends on**: T10, T11
- **Acceptance criteria**:
  - All verification tests pass
  - No spec fields are missing from KPI report
- **Risk**: None (verification only).
- **Wave**: V2

---

### Task T20: End-to-end shadow mode pipeline test

- **Type**: test
- **Target file(s)**: `tests/audit/test_wiring_integration.py`
- **Description**:
  1. Add `test_e2e_shadow_mode_pipeline`:
     - Create a SprintConfig with `wiring_gate_mode="shadow"`
     - Create a TurnLedger and DeferredRemediationLog
     - Run `execute_phase_tasks()` with a mock subprocess factory
     - Verify:
       a. Wiring analysis runs per task
       b. Findings are logged to DeferredRemediationLog
       c. No task statuses are changed (shadow = non-blocking)
       d. TurnLedger credits are applied (shadow credits back)
       e. KPI report reflects correct counts
  2. This test validates the full chain: execute_phase_tasks -> run_post_task_wiring_hook -> shadow -> DeferredRemediationLog -> build_kpi_report.
- **Source recommendation**: All P0 (end-to-end verification)
- **Depends on**: T01-T10
- **Acceptance criteria**:
  - Single test validates the entire shadow mode pipeline
  - All assertions pass
  - Test completes in < 2 seconds (no real subprocesses)
- **Risk**: Complex test with many assertions. If it fails, it may be hard to diagnose which component broke. Consider splitting assertions into sub-tests if the test framework supports it.
- **Wave**: V2

---

## Verification Wave V3: Final (depends on all)

### Task T21: Full regression suite run

- **Type**: verify
- **Target file(s)**: all test files
- **Description**:
  1. Run the complete test suite:
     ```bash
     uv run pytest tests/ -v --tb=short
     ```
  2. Verify zero failures across all existing and new tests.
  3. Run wiring-specific tests with coverage:
     ```bash
     uv run pytest tests/audit/ -v --cov=superclaude.cli.audit --cov=superclaude.cli.sprint
     ```
  4. Verify coverage for the modified files (executor.py, models.py, kpi.py, wiring_gate.py) is >= 80%.
- **Source recommendation**: All (final validation)
- **Depends on**: T01-T20
- **Acceptance criteria**:
  - Zero test failures
  - Coverage >= 80% for modified files
  - No new deprecation warnings from the migration shim changes
- **Risk**: Pre-existing test failures may be conflated with new failures. Run the baseline suite before starting implementation to establish a known-good state.
- **Wave**: V3

---

### Task T22: Gap closure audit — verify all 18 merged findings addressed

- **Type**: verify
- **Target file(s)**: This tasklist + `roadmap-gap-analysis-merged.md`
- **Description**:
  1. Walk through each of the 18 confirmed missing/bug entries in the merged report.
  2. For each entry, verify one of:
     - **Fixed**: Code change is present and tested
     - **Documented**: Intentional divergence is documented with rationale
     - **Deferred**: Explicitly deferred with a tracking issue
  3. Update the merged report's status column or create a companion closure log.
  4. Specifically verify:
     - Gap 1 (execute_sprint TurnLedger): T01+T02 implemented
     - Gap 2 (_resolve_wiring_mode dead code): T03 implemented
     - Gap 3 (DeferredRemediationLog shadow): T04+T05 implemented
     - Gap 4 (Remediation lifecycle): T06+T07+T08 implemented
     - Gap 5 (attempt_remediation): Subsumed by T08
     - Gap 6 (SprintConfig scope fields): T09 implemented
     - Gap 7 (KPI fields): T10 implemented
     - Gap 8 (TurnLedger naming): Documented as intentional in T11
     - Gap 9 (Frontmatter contract): Documented in T11
     - Gap 10 (Migration shim): T16 implemented/documented
     - Gap 11 (_format_wiring_failure): T06 implemented
     - Gap 12 (_recheck_wiring): T07 implemented
     - Gap 13 (Budget scenarios 5-8): T13 implemented
     - Gap 14 (Retrospective T11): T14 implemented
     - Gap 15 (Performance SC-009): T15 implemented
     - Gap 16 (check_wiring_report): T12 implemented
     - Gap 17 (--skip-wiring-gate): Deferred per OQ-5 (LOW priority, not in this tasklist)
     - Gap 18 (TrailingGateRunner): Subsumed by Gap 1 fix
- **Source recommendation**: All (closure verification)
- **Depends on**: T01-T21
- **Acceptance criteria**:
  - All 18 gaps have a verified disposition (Fixed/Documented/Deferred)
  - No gap is left unaddressed without explicit justification
  - Gap 17 (--skip-wiring-gate) is the only intentionally deferred item
- **Risk**: None (audit only).
- **Wave**: V3

---

## Execution Summary

| Wave | Tasks | Type | Parallel? | Estimated effort |
|------|-------|------|-----------|-----------------|
| Wave 1 | T01, T03, T09 | fix, refactor | Yes | Medium |
| Wave 2 | T02, T04, T06 | fix | Yes (T02 depends on T01) | Medium |
| Wave 3 | T05, T07, T08 | fix | Yes (dependencies within wave) | High |
| V1 | T17, T18 | test, verify | Yes | Medium |
| Wave 4 | T10-T16 | fix, test, verify | Yes | Medium |
| V2 | T19, T20 | test, verify | Yes | Medium |
| V3 | T21, T22 | verify | Sequential | Low |

**Critical path**: T01 -> T02 -> T05 -> T17 -> T20 -> T21 -> T22

**P0 tasks (must complete for v3.2)**: T01-T08 (8 tasks)
**P1 tasks (should complete)**: T09, T10, T11 (3 tasks)
**P2 tasks (nice to have)**: T12-T16 (5 tasks)
**Verification tasks**: T17-T22 (6 tasks)

---

## Post-Reflection Amendments

**Source**: `gap-remediation-reflection.md` (2026-03-21)
**Blocking**: YES -- these amendments must be applied before execution begins.

### Amendment A1: Fix T04 TrailingGateResult constructor (BLOCKING)

**Problem**: T04 constructs `TrailingGateResult(gate_name=..., passed=..., message=..., task_id=...)`. The actual dataclass fields are `step_id`, `passed`, `evaluation_ms`, `failure_reason`. The code example will raise `TypeError` at runtime.

**Correction**: Replace the synthetic construction in T04 with:
```python
from superclaude.cli.pipeline.trailing_gate import TrailingGateResult
gate_result = TrailingGateResult(
    step_id=task.task_id,
    passed=False,
    evaluation_ms=0.0,
    failure_reason=f"[shadow] {finding.finding_type}: {finding.detail}",
)
remediation_log.append(gate_result)
```

### Amendment A2: Fix T08 attempt_remediation() interface (BLOCKING)

**Problem**: T08 calls `attempt_remediation(prompt=prompt, config=config, task=task)`. The actual signature is `attempt_remediation(remediation_step, turns_per_attempt, can_remediate, debit, run_step, check_gate)` -- a fully callable-based interface requiring 6 positional arguments.

**Correction**: Replace the remediation call in T08 with either:

**(Option A) Use attempt_remediation with proper callables:**
```python
from superclaude.cli.pipeline.trailing_gate import attempt_remediation, TrailingGateResult

# Build remediation step via SprintGatePolicy
gate_result_for_policy = TrailingGateResult(
    step_id=task.task_id,
    passed=False,
    evaluation_ms=0.0,
    failure_reason=prompt,
)
policy = SprintGatePolicy(config)
remediation_step = policy.build_remediation_step(gate_result_for_policy)

# Define callable wrappers
def _run_step(step):
    # Execute step subprocess (reuse existing subprocess machinery)
    from superclaude.cli.sprint.executor import _run_task_subprocess
    exit_code, turns, output_bytes = _run_task_subprocess(task, config, phase)
    return StepResult(step=step, exit_code=exit_code, output_bytes=output_bytes)

def _check_gate(step_result):
    passed, recheck_report = _recheck_wiring(config, config.release_dir, mode)
    return TrailingGateResult(
        step_id=task.task_id, passed=passed, evaluation_ms=0.0,
        failure_reason=None if passed else "Blocking findings remain",
    )

remediation_result = attempt_remediation(
    remediation_step=remediation_step,
    turns_per_attempt=config.remediation_cost,
    can_remediate=ledger.can_remediate,
    debit=lambda turns: ledger.debit(turns),
    run_step=_run_step,
    check_gate=_check_gate,
)
```

**(Option B) Simpler inline approach (recommended for v3.2):**
```python
# Skip attempt_remediation(); implement inline for v3.2
# The full callable-based interface can be wired in v3.3
_wiring_logger.warning(
    "Full mode: %d blocking findings for task %s — remediation deferred (v3.2)",
    blocking, task.task_id,
)
# Still debit the cost to maintain budget accounting accuracy
```

### Amendment A3: Fix T12 check_wiring_report() signature (BLOCKING)

**Problem**: T12 proposes `check_wiring_report(report: WiringReport, mode: str)` iterating over `WIRING_GATE["checks"]`. `WIRING_GATE` is a `GateCriteria` instance (not a dict), and semantic checks operate on content strings, not WiringReport objects.

**Correction**: Replace with:
```python
def check_wiring_report(content: str) -> tuple[bool, list[str]]:
    """Convenience wrapper running all 5 semantic checks from WIRING_GATE.

    Args:
        content: Report file content (YAML frontmatter + Markdown body).

    Returns (passed, list_of_failure_messages).
    Spec reference: Section 6.1 / OQ-10.
    """
    failures = []
    for check in WIRING_GATE.semantic_checks:
        if not check.check_fn(content):
            failures.append(check.name)
    return (len(failures) == 0, failures)
```

### Amendment A4: Fix T02 line reference (NON-BLOCKING)

**Problem**: T02 says "around line 942+, after `sprint_result.phase_results.append(phase_result)`". The actual location is **line 1109**.

**Correction**: Update reference to line 1109. The post-phase hook insertion point is after line 1109:
```python
sprint_result.phase_results.append(phase_result)  # line 1109

# INSERT HERE: post-phase wiring hook
phase_result = run_post_phase_wiring_hook(phase, config, phase_result, ledger)
```

### Amendment A5: Add wiring_analyses_count to TurnLedger for T10 (NON-BLOCKING)

**Problem**: T10 requires `wiring_analyses_run` counter in KPI but TurnLedger has no analysis count field -- only cumulative turns.

**Correction**: Add to TurnLedger (models.py, after line 539):
```python
wiring_analyses_count: int = 0  # count of wiring analyses executed
```
And increment in `debit_wiring()` (after line 574):
```python
self.wiring_analyses_count += 1
```
Then in T10, `build_kpi_report()` populates: `report.wiring_analyses_run = turn_ledger.wiring_analyses_count`
