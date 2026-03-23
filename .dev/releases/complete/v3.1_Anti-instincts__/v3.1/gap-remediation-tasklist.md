# Gap Remediation Tasklist: v3.1 Anti-Instincts Gate

**Source**: `roadmap-gap-analysis-merged.md` (2026-03-21)
**Branch**: `v3.0-AuditGates`
**Total tasks**: 14
**Total waves**: 5
**Bugs addressed**: 11 (BUG-001 through BUG-011)
**Recommendations implemented**: P0 through P8

---

## Summary

| Wave | Tasks | Purpose | Parallelism |
|------|-------|---------|-------------|
| 1 | T01, T02, T03 | Instantiate infrastructure objects in `execute_sprint()` | Full parallel |
| 2 | T04, T05, T06 | Wire `execute_sprint()` to `execute_phase_tasks()`, add `TrailingGateResult` wrapping, wire `SprintGatePolicy` | Sequential (T04 depends on W1; T05, T06 depend on T04) |
| 3 | T07, T08, T09, T10 | KPI report call, remediation delegation, documentation fixes | Full parallel |
| 4 | T11, T12 | Integration tests for production path | Full parallel |
| 5 | T13, T14 | End-to-end verification and regression sweep | Sequential |

## Dependency Graph

```
Wave 1 (parallel):
  T01 ──┐
  T02 ──┼──> Wave 2
  T03 ──┘

Wave 2 (sequential within wave):
  T04 (depends on T01, T02, T03)
  T05 (depends on T04)
  T06 (depends on T04)

Wave 3 (parallel, depends on Wave 2):
  T07 ──┐
  T08 ──┤
  T09 ──┼──> Wave 4
  T10 ──┘

Wave 4 (parallel, depends on Wave 3):
  T11 ──┐
  T12 ──┼──> Wave 5

Wave 5 (sequential):
  T13 (depends on T11, T12)
  T14 (depends on T13)
```

---

## Wave 1: Infrastructure Instantiation

### Task T01: Construct `TurnLedger` in `execute_sprint()`
- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Description**:
  1. In `execute_sprint()`, after `sprint_result = SprintResult(config=config)` (line 874), add:
     ```python
     ledger = TurnLedger(
         total_budget=config.max_turns * len(config.active_phases),
         reimbursement_rate=0.8,
     )
     ```
  2. `TurnLedger` is already imported at line 28. No new imports needed.
  3. The `ledger` variable must be in scope for the phase loop so it can be passed to `execute_phase_tasks()` in T04.
- **Source recommendation**: P0 (resolves BUG-001)
- **Depends on**: none
- **Acceptance criteria**:
  - `execute_sprint()` constructs a `TurnLedger` before entering the phase loop.
  - `uv run pytest tests/sprint/test_executor.py -v` passes.
  - Grep for `TurnLedger(` in `execute_sprint` body returns a match.
- **Risk**: Incorrect budget calculation if `max_turns * len(active_phases)` does not match the intended budget model. Verify against `SprintConfig` defaults.
- **Wave**: 1

---

### Task T02: Construct `ShadowGateMetrics` in `execute_sprint()`
- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Description**:
  1. In `execute_sprint()`, immediately after the `TurnLedger` construction added in T01 (or in the same block), add:
     ```python
     shadow_metrics = ShadowGateMetrics()
     ```
  2. `ShadowGateMetrics` is already imported at line 21. No new imports needed.
  3. The variable must be in scope for the phase loop.
- **Source recommendation**: P0 (resolves BUG-002)
- **Depends on**: none
- **Acceptance criteria**:
  - `execute_sprint()` constructs a `ShadowGateMetrics` before entering the phase loop.
  - Grep for `ShadowGateMetrics()` in `execute_sprint` body returns a match.
- **Risk**: Low. `ShadowGateMetrics` is a simple metrics collector with no required constructor args.
- **Wave**: 1

---

### Task T03: Construct `DeferredRemediationLog` in `execute_sprint()`
- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Description**:
  1. In `execute_sprint()`, in the same initialization block, add:
     ```python
     from superclaude.cli.pipeline.trailing_gate import DeferredRemediationLog
     remediation_log = DeferredRemediationLog(
         persist_path=config.results_dir / "remediation.json",
     )
     ```
  2. Note: `DeferredRemediationLog` is NOT currently imported at the top of the file. Either add a top-level import or use a lazy import in the function body. Lazy import is consistent with existing patterns in this file (see line 885).
  3. The variable must be in scope for the phase loop and for the KPI report call added in T07.
- **Source recommendation**: P2 (resolves BUG-005)
- **Depends on**: none
- **Acceptance criteria**:
  - `execute_sprint()` constructs a `DeferredRemediationLog` with a persist path under `results_dir`.
  - Grep for `DeferredRemediationLog(` in `execute_sprint` body returns a match.
- **Risk**: If `results_dir` does not exist at sprint start, the persist path will fail on first write. Verify that `results_dir` is created before this point (it is -- `config.results_dir` is created by `SprintConfig` initialization).
- **Wave**: 1

---

## Wave 2: Core Wiring

### Task T04: Wire `execute_sprint()` to call `execute_phase_tasks()` for per-task phases
- **Type**: refactor
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Description**:
  This is the critical architectural fix. The current `execute_sprint()` phase loop (lines 890-1156) launches one `ClaudeProcess` per phase with no per-task orchestration. It must be modified to delegate to `execute_phase_tasks()` for phases that have task inventories.

  **Approach** (per-task delegation with fallback):

  1. Inside the phase loop, after the `execution_mode` checks (lines 896-911), before launching `ClaudeProcess`, add a check for whether the phase has a task inventory:
     ```python
     # Check if this phase has a parseable task inventory
     tasks = _parse_phase_tasks(phase, config)
     if tasks:
         # Delegate to per-task orchestration (enables hooks, budget, gates)
         task_results, remaining = execute_phase_tasks(
             tasks=tasks,
             config=config,
             phase=phase,
             ledger=ledger,
             shadow_metrics=shadow_metrics,
         )
         # Record phase result from task results
         started_at = datetime.now(timezone.utc)
         all_passed = all(r.status == TaskStatus.PASS for r in task_results)
         status = PhaseStatus.PASS if all_passed else PhaseStatus.ERROR
         phase_result = PhaseResult(
             phase=phase,
             status=status,
             exit_code=0 if all_passed else 1,
             started_at=started_at,
             finished_at=datetime.now(timezone.utc),
         )
         sprint_result.phase_results.append(phase_result)
         logger.write_phase_result(phase_result)
         # Accumulate TrailingGateResults (T05 adds this)
         continue
     ```

  2. Add a helper function `_parse_phase_tasks(phase, config) -> list[TaskEntry] | None` that attempts to parse the phase file for task entries. If the phase file does not contain a task inventory (i.e., it is a freeform prompt), return `None` so the phase falls through to the existing `ClaudeProcess` path.

  3. The existing `ClaudeProcess` path (lines 913-1156) remains as the fallback for phases without task inventories. This preserves backward compatibility.

  4. Pass `ledger`, `shadow_metrics` to `execute_phase_tasks()`. The `remediation_log` will be wired in T05 when `TrailingGateResult` wrapping is added.

  **Key constraint**: The fallback to `ClaudeProcess` must remain intact. Not all phases have task inventories. The refactor adds a conditional branch, not a replacement.
- **Source recommendation**: P0 (resolves BUG-003, and enables BUG-001/BUG-002 fixes to take effect)
- **Depends on**: T01, T02, T03
- **Acceptance criteria**:
  - `execute_sprint()` calls `execute_phase_tasks()` when a phase has a task inventory.
  - Phases without task inventories still use the `ClaudeProcess` subprocess path.
  - `ledger` and `shadow_metrics` are passed to `execute_phase_tasks()`.
  - `uv run pytest tests/sprint/ -v` passes (no regressions).
- **Risk**: HIGH. This is the most invasive change. The `_parse_phase_tasks` helper must correctly distinguish task-inventory phases from freeform-prompt phases. Incorrect parsing could route all phases to the wrong path. Test with both types of phase files.
- **Wave**: 2

---

### Task T05: Add `TrailingGateResult` wrapping in anti-instinct hook and accumulate in sprint loop
- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Description**:
  Two changes required:

  **Part A: Modify `run_post_task_anti_instinct_hook()` to return `TrailingGateResult`**

  1. Change the return type from `TaskResult` to `tuple[TaskResult, TrailingGateResult | None]`.
  2. After the gate evaluation (line 629), create a `TrailingGateResult`:
     ```python
     gate_result = TrailingGateResult(
         step_id=task.task_id,
         passed=passed,
         evaluation_ms=evaluation_ms,
         failure_reason=failure_reason,
     )
     ```
  3. Return `(task_result, gate_result)` instead of `task_result` at each return point.
  4. For the `mode == "off"` early return (line 611), return `(task_result, None)`.
  5. **IMPORTANT**: The shadow mode early return (line 643-645) must return `(task_result, gate_result)` with the evaluated `TrailingGateResult`, NOT `(task_result, None)`. The gate IS evaluated in shadow mode; the result must be captured for KPI accumulation. Only `mode == "off"` should return None for the gate result.

  **Part B: Update callers**

  1. In `execute_phase_tasks()` (line 792-794), update the call to unpack the tuple:
     ```python
     result, anti_instinct_gate_result = run_post_task_anti_instinct_hook(
         task, config, result, ledger=ledger, shadow_metrics=shadow_metrics,
     )
     ```
  2. Return the gate results from `execute_phase_tasks()` by changing the return type to `tuple[list[TaskResult], list[str], list[TrailingGateResult]]` and accumulating `anti_instinct_gate_result` into a list.

  **Part C: Accumulate in `execute_sprint()`**

  1. Add `all_gate_results: list[TrailingGateResult] = []` before the phase loop.
  2. In the per-task delegation branch (added in T04), after `execute_phase_tasks()` returns, extend `all_gate_results` with the returned gate results.
  3. For each failed gate result, append to `remediation_log`:
     ```python
     for gr in gate_results:
         if not gr.passed and remediation_log is not None:
             remediation_log.append(gr)
     ```

- **Source recommendation**: P1 (resolves BUG-004), P2 partial (BUG-005 remediation log population)
- **Depends on**: T04
- **Acceptance criteria**:
  - `run_post_task_anti_instinct_hook()` creates and returns a `TrailingGateResult` for each evaluation.
  - `execute_phase_tasks()` returns accumulated gate results.
  - `execute_sprint()` accumulates all gate results in `all_gate_results`.
  - Failed gate results are appended to `remediation_log`.
  - `uv run pytest tests/sprint/test_anti_instinct_sprint.py -v` passes (may need updates to match new return signature).
- **Risk**: Changing the return type of `run_post_task_anti_instinct_hook()` is a breaking change for all callers. Search for all call sites with `grep -rn "run_post_task_anti_instinct_hook"` and update each one. The only production caller is `execute_phase_tasks()` (line 792). Test callers in `tests/sprint/test_anti_instinct_sprint.py` will also need updates.
- **Wave**: 2

---

### Task T06: Instantiate `SprintGatePolicy` in `execute_sprint()`
- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Description**:
  1. In `execute_sprint()`, in the initialization block (after T01-T03 additions), add:
     ```python
     gate_policy = SprintGatePolicy(config)
     ```
  2. `SprintGatePolicy` is defined at line 56 in the same file. No import needed.
  3. Store in scope for potential use by remediation paths. Currently this just makes the class reachable; the remediation workflow that uses it is addressed in T08.
- **Source recommendation**: P5 (resolves BUG-006)
- **Depends on**: T04
- **Acceptance criteria**:
  - `SprintGatePolicy` is instantiated in `execute_sprint()`.
  - Grep for `SprintGatePolicy(` in `execute_sprint` body returns a match.
- **Risk**: Low. The policy object is lightweight and has no side effects on construction.
- **Wave**: 2

---

## Wave 3: Downstream Integration

### Task T07: Call `build_kpi_report()` at sprint completion
- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Description**:
  1. In `execute_sprint()`, after the phase loop completes and before `logger.write_summary(sprint_result)` (line 1179), add:
     ```python
     # Build KPI report from accumulated gate results
     from superclaude.cli.sprint.kpi import build_kpi_report
     kpi_report = build_kpi_report(
         gate_results=all_gate_results,
         remediation_log=remediation_log,
         turn_ledger=ledger,
     )
     # Write KPI report to disk
     kpi_path = config.results_dir / "gate-kpi-report.md"
     kpi_path.write_text(kpi_report.format_report())
     ```
  2. The `build_kpi_report()` function is in `src/superclaude/cli/sprint/kpi.py` (line 137). It accepts `gate_results`, `remediation_log`, `conflict_reviews_total`, `conflicts_detected`, `turn_ledger`, and `wiring_report`.
  3. Pass the `all_gate_results` list (from T05) and `remediation_log` (from T03) and `ledger` (from T01).
  4. **IMPORTANT**: Use `kpi_report.format_report()` for serialization, NOT `str(kpi_report)`. `GateKPIReport` has no `__str__` method; `str()` would produce a raw dataclass repr. The `format_report()` method (kpi.py line 102) returns human-readable formatted text.
- **Source recommendation**: P3 (resolves BUG-007)
- **Depends on**: T05 (needs `all_gate_results`), T03 (needs `remediation_log`), T01 (needs `ledger`)
- **Acceptance criteria**:
  - After sprint completion, `build_kpi_report()` is called with accumulated gate results.
  - A `gate-kpi-report.md` file is written to `results_dir`.
  - `uv run pytest tests/sprint/test_kpi_report.py -v` passes.
- **Risk**: Low after amendment. The `format_report()` method produces well-formatted text with section headers and metrics.
- **Wave**: 3

---

### Task T08: Wire `attempt_remediation()` or document inline decision
- **Type**: fix | verify
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`, `src/superclaude/cli/pipeline/trailing_gate.py`
- **Description**:
  **Decision required**: The hook implements inline fail logic (set `GateOutcome.FAIL`, set `TaskStatus.FAIL` in full mode) instead of delegating to `attempt_remediation()` which provides retry-once semantics.

  **Option A (wire `attempt_remediation`)**: In `run_post_task_anti_instinct_hook()`, in the fail path (lines 661-684), replace the inline logic with:
  ```python
  from superclaude.cli.pipeline.trailing_gate import attempt_remediation
  remediation_result = attempt_remediation(
      gate_result=gate_result,
      policy=gate_policy,
      ledger=ledger,
  )
  ```
  This requires passing `gate_policy` into the hook (signature change).

  **Option B (document intentional deviation)**: Add a code comment in the hook explaining the intentional simplification for v3.1, and add a note to the spec deviation log.

  **Recommendation**: Option B for v3.1 (lower risk), with Option A deferred to v3.2.
- **Source recommendation**: P6 (resolves BUG-009)
- **Depends on**: T05 (needs `gate_result` to exist)
- **Acceptance criteria**:
  - Either `attempt_remediation()` is called from the hook, OR
  - A clear code comment documents the intentional deviation and a spec deviation entry exists.
- **Risk**: Option A changes the hook's behavior and could introduce retry loops that interact with the budget system unexpectedly. Option B is safe.
- **Wave**: 3

---

### Task T09: Document reimbursement operand deviation
- **Type**: verify
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py` (comment), spec deviation log
- **Description**:
  1. In `run_post_task_anti_instinct_hook()`, at line 651 where `task_result.turns_consumed` is used for reimbursement, add a comment:
     ```python
     # SPEC-DEVIATION (BUG-010): Spec says reimbursement should use upstream
     # merge step turns. We use task_result.turns_consumed because it reflects
     # the actual work done by this task, which is more practical and defensible.
     # See: roadmap-gap-analysis-merged.md, D4.
     ```
  2. If a spec deviation log exists in the release directory, add an entry there too.
- **Source recommendation**: P7 (resolves BUG-010)
- **Depends on**: none
- **Acceptance criteria**:
  - The code comment is present at the reimbursement line.
  - No behavioral change.
- **Risk**: None. Documentation-only change.
- **Wave**: 3

---

### Task T10: Document `TrailingGateResult` signature deviation
- **Type**: verify
- **Target file(s)**: `src/superclaude/cli/pipeline/trailing_gate.py` (comment)
- **Description**:
  1. In the `TrailingGateResult` dataclass (line 35 of `trailing_gate.py`), add a docstring note:
     ```python
     # SPEC-DEVIATION (BUG-011): Spec says TrailingGateResult(passed, evaluation_ms, gate_name).
     # Implementation uses (step_id, passed, evaluation_ms, failure_reason) per roadmap v3.0.
     # The roadmap version is authoritative. See: roadmap-gap-analysis-merged.md, D6.
     ```
  2. No behavioral change.
- **Source recommendation**: P8 partial (resolves BUG-011)
- **Depends on**: none
- **Acceptance criteria**:
  - The documentation comment is present on `TrailingGateResult`.
  - No behavioral change.
- **Risk**: None. Documentation-only change.
- **Wave**: 3

---

## Wave 4: Integration Tests

### Task T11: Integration test for `execute_sprint()` production path
- **Type**: test
- **Target file(s)**: `tests/sprint/test_executor.py` (or new file `tests/sprint/test_execute_sprint_integration.py`)
- **Description**:
  Write a test that exercises `execute_sprint()` end-to-end with mocked `ClaudeProcess` and verifies that all infrastructure components are instantiated and invoked.

  1. Create a `SprintConfig` with at least one phase that has a task inventory.
  2. Mock `ClaudeProcess` to simulate successful task execution.
  3. Mock `_parse_phase_tasks` (added in T04) to return a known task list.
  4. Call `execute_sprint(config)`.
  5. Assert:
     - `TurnLedger` was constructed (check budget tracking occurred).
     - `ShadowGateMetrics` was constructed (check `record()` was called if `gate_rollout_mode != "off"`).
     - `DeferredRemediationLog` was constructed with correct `persist_path`.
     - `execute_phase_tasks()` was called for the task-inventory phase.
     - `build_kpi_report()` was called after the loop.
     - A `gate-kpi-report.md` file was written.

  Use `unittest.mock.patch` for the subprocess and file I/O. Pattern after existing tests in `tests/sprint/test_e2e_success.py`.
- **Source recommendation**: P4 (resolves BUG-008)
- **Depends on**: T04, T05, T07 (all wiring must be in place)
- **Acceptance criteria**:
  - Test passes: `uv run pytest tests/sprint/test_execute_sprint_integration.py -v`
  - Test verifies TurnLedger, ShadowGateMetrics, DeferredRemediationLog, hooks, and KPI report are all invoked from the production `execute_sprint()` path.
- **Risk**: Mocking complexity. The `execute_sprint()` function has many side effects (TUI, signal handlers, file I/O, subprocess). The test must mock enough to isolate the orchestration logic without making the test brittle.
- **Wave**: 4

---

### Task T12: Update existing anti-instinct and shadow mode tests for new return types
- **Type**: test
- **Target file(s)**: `tests/sprint/test_anti_instinct_sprint.py`, `tests/sprint/test_shadow_mode.py`
- **Description**:
  After T05 changes the return type of `run_post_task_anti_instinct_hook()` from `TaskResult` to `tuple[TaskResult, TrailingGateResult | None]`, existing tests that call this function directly will break.

  1. In `tests/sprint/test_anti_instinct_sprint.py`, update all calls to `run_post_task_anti_instinct_hook()` to unpack the tuple:
     ```python
     # Before: result = run_post_task_anti_instinct_hook(...)
     # After:  result, gate_result = run_post_task_anti_instinct_hook(...)
     ```
  2. Add assertions on the returned `gate_result`:
     - Verify `gate_result.step_id == task.task_id`
     - Verify `gate_result.passed` matches expected outcome
     - Verify `gate_result.evaluation_ms >= 0`
     - Verify `gate_result.failure_reason` is set on failures
  3. In `tests/sprint/test_shadow_mode.py`, apply the same updates.
  4. Also update `execute_phase_tasks()` callers in `tests/sprint/test_executor.py` if the return type changed (T05 Part B).
- **Source recommendation**: P4 (supports BUG-008 resolution)
- **Depends on**: T05
- **Acceptance criteria**:
  - `uv run pytest tests/sprint/test_anti_instinct_sprint.py tests/sprint/test_shadow_mode.py -v` passes.
  - Tests verify `TrailingGateResult` content, not just `TaskResult`.
- **Risk**: Missing a call site. Run `grep -rn "run_post_task_anti_instinct_hook" tests/` to find all test call sites.
- **Wave**: 4

---

## Wave 5: Verification

### Task T13: Full test suite regression check
- **Type**: verify
- **Target file(s)**: All test files
- **Description**:
  1. Run the full test suite: `uv run pytest tests/ -v --tb=short`
  2. Identify any regressions introduced by T01-T12.
  3. Fix any failures.
  4. Confirm zero test failures before proceeding to T14.
- **Source recommendation**: All (regression gate)
- **Depends on**: T11, T12
- **Acceptance criteria**:
  - `uv run pytest tests/ -v` exits with code 0.
  - No tests skipped due to import errors or signature mismatches.
- **Risk**: Cascading failures from return-type changes in T05. The most likely source of regressions.
- **Wave**: 5

---

### Task T14: Manual smoke verification
- **Type**: verify
- **Target file(s)**: `src/superclaude/cli/sprint/executor.py`
- **Description**:
  Verify the fix addresses the root cause by tracing the production code path:

  1. Grep `execute_sprint` for `TurnLedger(` -- must find instantiation.
  2. Grep `execute_sprint` for `ShadowGateMetrics()` -- must find instantiation.
  3. Grep `execute_sprint` for `DeferredRemediationLog(` -- must find instantiation.
  4. Grep `execute_sprint` for `execute_phase_tasks(` -- must find delegation call.
  5. Grep `execute_sprint` for `build_kpi_report(` -- must find call after loop.
  6. Grep `execute_sprint` for `SprintGatePolicy(` -- must find instantiation.
  7. Verify `run_post_task_anti_instinct_hook` returns `TrailingGateResult`.
  8. Verify `DeferredRemediationLog.append()` is called for failed gate results.

  All 8 checks must pass. This confirms the "TurnLedger Wiring Status" table from the merged report would show "YES" in the "Instantiated in execute_sprint()?" and "Reachable in production?" columns for all components.
- **Source recommendation**: Final verdict verification
- **Depends on**: T13
- **Acceptance criteria**:
  - All 8 grep checks return matches.
  - The wiring status for every component in the merged report table is now "YES / YES / YES".
- **Risk**: None. Read-only verification.
- **Wave**: 5

---

## Appendix: Bug-to-Task Mapping

| Bug ID | Severity | Task(s) | Status After |
|--------|----------|---------|--------------|
| BUG-001 | CRITICAL | T01, T04 | Fixed |
| BUG-002 | CRITICAL | T02, T04 | Fixed |
| BUG-003 | CRITICAL | T04 | Fixed |
| BUG-004 | HIGH | T05 | Fixed |
| BUG-005 | HIGH | T03, T05 | Fixed |
| BUG-006 | MEDIUM | T06 | Fixed |
| BUG-007 | MEDIUM | T07 | Fixed |
| BUG-008 | MEDIUM | T11 | Fixed |
| BUG-009 | LOW | T08 | Fixed/Documented |
| BUG-010 | LOW | T09 | Documented |
| BUG-011 | LOW | T10 | Documented |

## Appendix: Recommendation-to-Task Mapping

| Rec ID | Priority | Task(s) |
|--------|----------|---------|
| P0 | BLOCKING | T01, T02, T04 |
| P1 | HIGH | T05 |
| P2 | HIGH | T03, T05 |
| P3 | MODERATE | T07 |
| P4 | MODERATE | T11, T12 |
| P5 | LOW | T06 |
| P6 | LOW | T08 |
| P7 | LOW | T09 |
| P8 | LOW | T10 |

---

## Post-Reflection Amendments

**Reflection date**: 2026-03-21
**Reflection report**: `gap-remediation-reflection.md`

### Amendment A1: T07 serialization method (APPLIED)
- **Issue**: Code snippet used `str(kpi_report)` but `GateKPIReport` has no `__str__` method. Would produce raw dataclass repr.
- **Fix**: Changed to `kpi_report.format_report()` which returns human-readable formatted text (kpi.py line 102).
- **Status**: APPLIED to T07 description above.

### Amendment A2: T05 shadow mode return value (APPLIED)
- **Issue**: Tasklist only specified returning `None` for `mode == "off"`. Shadow mode (lines 643-645) also evaluates the gate but the return instruction was missing.
- **Fix**: Added instruction that shadow mode must return `(task_result, gate_result)` with the evaluated TrailingGateResult, not None.
- **Status**: APPLIED to T05 Part A description above.

### Amendment A3: T04 _parse_phase_tasks() specification (NOTED)
- **Issue**: The `_parse_phase_tasks()` helper is referenced but not specified. Its implementation is critical for T04 correctness.
- **Recommendation**: During T04 implementation, either locate an existing tasklist parser in the codebase or implement one that parses markdown headings matching `### Task T\d+` patterns into `TaskEntry` objects. The helper must return `None` for freeform-prompt phases to preserve the ClaudeProcess fallback.
- **Status**: NOT applied as inline edit -- implementer must address during T04.

### Amendment A4: T04 started_at timing (NOTED)
- **Issue**: T04 code snippet sets `started_at = datetime.now(timezone.utc)` after `execute_phase_tasks()` call, but it should be captured before.
- **Status**: NOT applied as inline edit -- implementer must capture started_at before calling execute_phase_tasks().

### Amendment A5: T08 Option A signature mismatch (NOTED)
- **Issue**: Option A's code snippet calls `attempt_remediation(gate_result=..., policy=..., ledger=...)` but actual signature is `attempt_remediation(remediation_step, turns_per_attempt, can_remediate, debit, run_step, check_gate)` -- six callable/value args.
- **Status**: Informational only. Option B is recommended for v3.1. If v3.2 revisits, the code snippet must be rewritten to match the actual API.
