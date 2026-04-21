# 05 — Pipeline QA Systems: Gate System Integration Analysis

**Status**: Complete
**Date**: 2026-04-03
**Investigation Type**: Integration Mapper
**Research Question**: The pipeline executor in `src/superclaude/cli/pipeline/` has gates, retry logic, and deliverable decomposition — but sprint does NOT use it. Why? What would it take to wire it in?

---

## 1. Pipeline Module Overview

The pipeline module (`src/superclaude/cli/pipeline/`) is a generic step sequencer designed via composition-via-callable. It provides:

### 1.1 Core Components

| File | Purpose | Key Exports |
|------|---------|-------------|
| `executor.py` | Generic step sequencer with retry, gates, parallel dispatch | `execute_pipeline()` |
| `gates.py` | Pure Python gate validation (no subprocess, no LLM) | `gate_passed()` |
| `models.py` | Shared dataclasses: Step, StepResult, GateCriteria, etc. | `Step`, `StepResult`, `StepStatus`, `GateCriteria`, `PipelineConfig`, `GateMode` |
| `deliverables.py` | Behavioral detection and Implement/Verify decomposition | `is_behavioral()`, `decompose_deliverables()` |
| `trailing_gate.py` | Async gate evaluation, deferred remediation, scope-based gate strategy | `TrailingGateRunner`, `DeferredRemediationLog`, `attempt_remediation()`, `resolve_gate_mode()` |
| `process.py` | Claude subprocess wrapper | `ClaudeProcess` |
| `__init__.py` | Public API surface (42+ symbols) | All of the above plus M2-M4 analysis passes |

### 1.2 NFR-007 Enforcement

Every pipeline module has `NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.` This is a hard architectural boundary -- the pipeline module is intentionally agnostic to its consumers.

---

## 2. The Gate System in Detail

### 2.1 Gate Tiers (`gates.py`, lines 20-74)

`gate_passed(output_file, criteria)` validates step outputs against `GateCriteria` with tier-proportional checks:

| Tier | Checks |
|------|--------|
| **EXEMPT** | Always passes |
| **LIGHT** | File exists + non-empty |
| **STANDARD** | + min line count + required YAML frontmatter fields |
| **STRICT** | + semantic checks (custom `check_fn` callables on content) |

The `GateCriteria` dataclass (`models.py`, line 68) has fields:
- `required_frontmatter_fields: list[str]`
- `min_lines: int`
- `enforcement_tier: Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"]`
- `semantic_checks: list[SemanticCheck] | None` -- each is a `(name, check_fn, failure_message)` triple

### 2.2 Gate Modes (`models.py`, lines 46-56)

Two modes:
- **BLOCKING** (default): Step must pass gate before next step begins.
- **TRAILING**: Step runs, gate evaluated async; failures collected at pipeline end.

### 2.3 execute_pipeline() Flow (`executor.py`, lines 46-171)

The executor processes a `list[Step | list[Step]]` where:
- Single `Step` = sequential execution
- `list[Step]` = parallel execution group (via threads)

For each step:
1. Call `on_step_start(step)`
2. Call `run_step(step, config, cancel_check)` -- the consumer-injected StepRunner
3. If step has `gate` criteria:
   - BLOCKING mode: run `gate_passed()` synchronously; halt on failure
   - TRAILING mode: submit to `TrailingGateRunner`; continue immediately
4. On gate failure + retry budget remaining: retry
5. On gate failure + retries exhausted: HALT pipeline
6. Call `on_step_complete(step, result)` and `on_state_update(state)`

After main loop, deferred TRAILING-mode steps that were never reached still execute. A final sync point collects all trailing gate results.

### 2.4 Trailing Gate Infrastructure (`trailing_gate.py`)

- **TrailingGateRunner** (line 93): Daemon-thread gate evaluator. `submit(step)` spawns a thread to evaluate gate criteria. `wait_for_pending(timeout)` blocks for collection.
- **GateResultQueue** (line 49): Thread-safe result collection.
- **DeferredRemediationLog** (line 494): Persistent log of gate failures requiring remediation. Supports JSON serialization and `--resume` recovery.
- **TrailingGatePolicy** (line 232): Protocol for consumer-owned hooks: `build_remediation_step()` and `files_changed()`.
- **attempt_remediation()** (line 359): Retry-once semantics with budget integration. State machine: Pre-check budget, Attempt 1, Attempt 2, PERSISTENT_FAILURE.
- **resolve_gate_mode()** (line 598): Scope-based strategy -- Release scope always BLOCKING; Milestone configurable; Task trails when grace_period > 0.

---

## 3. Who Calls execute_pipeline()

### 3.1 Production Callers (in `src/`)

| Caller | File | Line | Notes |
|--------|------|------|-------|
| **Roadmap executor** | `src/superclaude/cli/roadmap/executor.py` | 2328, 2553 | Primary consumer. Builds 9-step pipeline, passes `roadmap_run_step` as StepRunner. Also used for `--resume` re-execution. |
| **Roadmap validate executor** | `src/superclaude/cli/roadmap/validate_executor.py` | 407 | Validation pipeline, reuses same `execute_pipeline()` with `validate_run_step`. |
| **Tasklist executor** | `src/superclaude/cli/tasklist/executor.py` | 256 | Tasklist fidelity checking, reuses `execute_pipeline()` with `tasklist_run_step`. |
| **Sprint executor** | `src/superclaude/cli/sprint/executor.py` | **NEVER** | Sprint does NOT call `execute_pipeline()`. Has its own orchestration loop. |

### 3.2 Test Callers

Multiple test files call `execute_pipeline()` directly for unit/integration testing:
- `tests/pipeline/test_executor.py`
- `tests/pipeline/test_parallel.py`
- `tests/pipeline/test_full_flow.py`
- `tests/roadmap/test_executor.py`
- `tests/roadmap/test_pipeline_integration.py`
- `tests/integration/test_wiring_pipeline.py`

---

## 4. Who Calls decompose_deliverables() and is_behavioral()

### 4.1 decompose_deliverables()

| Caller | File | Line | Notes |
|--------|------|------|-------|
| **Roadmap executor** | `src/superclaude/cli/roadmap/executor.py` | 2134 | Used during roadmap step building to split behavioral deliverables into Implement/Verify pairs. |

**This is the only production caller.** Sprint does not use it. Tasklist does not use it.

### 4.2 is_behavioral()

| Caller | File | Notes |
|--------|------|-------|
| `deliverables.py` itself | `src/superclaude/cli/pipeline/deliverables.py` | Called by `decompose_deliverables()` internally |
| `fmea_domains.py` | `src/superclaude/cli/pipeline/fmea_domains.py` | Used in FMEA analysis pass |

Test callers: `tests/pipeline/test_behavioral.py`, `tests/pipeline/test_decompose.py`, `tests/pipeline/test_integration_decompose.py`.

**Sprint does not use `is_behavioral()` or `decompose_deliverables()` anywhere.**

---

## 5. Why Sprint Does NOT Use execute_pipeline()

Sprint has its own orchestration loop in `execute_sprint()` (`src/superclaude/cli/sprint/executor.py`, line 1112). Key reasons for the divergence:

### 5.1 Sprint's Unique Requirements

1. **TUI integration**: Sprint drives a real-time Terminal UI (`SprintTUI`) with per-phase state updates, output monitoring, and poll-loop rendering. `execute_pipeline()` has no TUI callback hooks.

2. **Per-task delegation**: Sprint phases can contain multiple tasks. `execute_phase_tasks()` (line 912) iterates over tasks within a phase. `execute_pipeline()` operates on Steps, not on a phase-task hierarchy.

3. **Output monitoring**: Sprint uses `OutputMonitor` with stall detection and watchdog logic (stall_timeout, stall_action="kill"). This is interleaved with the poll loop.

4. **Signal handling**: Sprint installs its own `SignalHandler` for graceful shutdown with `shutdown_requested` checks in the poll loop.

5. **Preflight phases**: Sprint has a preflight executor for python-mode phases that runs before the main loop. This is orthogonal to the pipeline executor's step model.

6. **Phase-level semantics**: Sprint's unit of work is a "phase" (with a file, number, execution_mode), not a pipeline Step. Phases have CONTINUE/HALT parsing from result files.

### 5.2 Sprint's Gate Integration (Inline, Not via execute_pipeline)

Sprint DOES use pipeline gate infrastructure, but inline:

1. **`gate_passed()`**: Called directly at line 819 within the anti-instinct hook (`_run_anti_instinct_gate_hook()`). Not routed through `execute_pipeline()`.

2. **`DeferredRemediationLog`**: Instantiated at line 1154-1156 within `execute_sprint()`. Used for recording gate failures.

3. **`TrailingGateResult`**: Built manually at line 844 from gate evaluation results.

4. **`resolve_gate_mode()`** and **`GateScope`**: Imported at line 428 for scope-based gate mode resolution.

5. **`SprintGatePolicy`**: Implements the `TrailingGatePolicy` protocol (line 1159). Used for remediation step building.

Sprint's gate integration is "direct-call" rather than "framework-mediated" -- it calls `gate_passed()` directly and builds `TrailingGateResult` manually, bypassing the retry/sequence/parallel machinery in `execute_pipeline()`.

### 5.3 The SPEC-DEVIATION Comment (BUG-009/P6)

At line 877-881, there is an explicit acknowledgment:

> SPEC-DEVIATION (BUG-009/P6): Spec says this path should delegate to `attempt_remediation()` for retry-once semantics. We use inline fail logic (set GateOutcome.FAIL / TaskStatus.FAIL) as an intentional v3.1 simplification. `attempt_remediation()` has a 6-arg callable-based API that requires more design work to integrate here safely. Deferred to v3.2.

This confirms the disconnect is known and intentional. The pipeline module's `attempt_remediation()` exists and has proper retry-once semantics, but Sprint chose inline fail logic instead.

---

## 6. What It Would Take to Wire Sprint to execute_pipeline()

### 6.1 Option A: Full Migration (Sprint Calls execute_pipeline)

**Barriers:**
1. **Step model mismatch**: Sprint works in phases containing tasks. `execute_pipeline()` works with a flat `list[Step | list[Step]]`. Each sprint task would need to be mapped to a pipeline `Step`.
2. **TUI callbacks**: `execute_pipeline()` provides `on_step_start`, `on_step_complete`, `on_state_update` callbacks, which could potentially drive TUI updates. However, sprint's TUI also needs `MonitorState` data (output bytes, growth rate, stall seconds) which is not in the pipeline callback model.
3. **Poll loop**: Sprint's poll loop (lines 1270-1324) interleaves process monitoring, watchdog stall detection, and TUI updates at ~2 second intervals. `execute_pipeline()` delegates all step execution to the `StepRunner` callable, which would need to encapsulate all of this.
4. **Phase-level concerns**: Preflight phases, skip-mode phases, python-mode phases, and per-task delegation all happen outside the Step model.
5. **Signal handling**: Sprint's `SignalHandler` checks would need to map to `execute_pipeline()`'s `cancel_check` callback.

**Feasibility**: Medium-High effort. Sprint's StepRunner would need to be very complex, essentially recreating the poll-loop/TUI/watchdog logic inside a `StepRunner.__call__()` method. The benefit would be getting retry and gate sequencing for free, but the cost is high.

### 6.2 Option B: Gate Integration Only (Sprint Uses gate_passed + attempt_remediation)

**Barriers:**
1. Sprint already calls `gate_passed()` directly -- this is done.
2. Integrating `attempt_remediation()` requires providing 6 callables: `remediation_step`, `turns_per_attempt`, `can_remediate`, `debit`, `run_step`, `check_gate`. All of these exist in sprint's code but are not factored as standalone callables.
3. This was explicitly deferred (BUG-009/P6) with the note "requires more design work to integrate here safely."

**Feasibility**: Low-Medium effort. The building blocks exist. The main work is wiring sprint's `TurnLedger`, `SprintGatePolicy`, and `ClaudeProcess` into the 6-arg callable interface.

### 6.3 Option C: Hybrid (Sprint Uses Pipeline for Task-Level, Custom for Phase-Level)

Map each task within `execute_phase_tasks()` to a pipeline `Step`, then call `execute_pipeline()` for the per-task sequence within each phase. Keep the phase-level loop (preflight, TUI, signal handling) in sprint's own code.

**Feasibility**: Medium effort. This is the most natural integration point. Tasks are already close to Steps (they have a prompt, output file, and timeout). The phase-level concerns stay in sprint.

---

## 7. Extension Points and Integration Barriers

### 7.1 Extension Points in the Pipeline Module

| Extension Point | Mechanism | Status in Sprint |
|-----------------|-----------|------------------|
| `StepRunner` protocol | Consumer injects step execution callable | Not used (sprint has its own loop) |
| `on_step_start` callback | Notified when step begins | Not used |
| `on_step_complete` callback | Notified when step ends | Not used |
| `on_state_update` callback | Receives state dict after each step | Not used |
| `cancel_check` callable | External cancellation signal | Not used (sprint uses `SignalHandler`) |
| `TrailingGateRunner` | Async gate evaluation | Not used (sprint evaluates gates inline) |
| `TrailingGatePolicy` protocol | Consumer-owned remediation hooks | Implemented by `SprintGatePolicy` but not connected to `TrailingGateRunner` |
| `attempt_remediation()` | Retry-once with budget | Not used (BUG-009/P6 deferral) |

### 7.2 Integration Barriers

1. **Phase-Task hierarchy**: Pipeline has no concept of phases. Sprint's phases group tasks and have their own lifecycle (preflight, skip, python, claude modes).
2. **TUI coupling**: Sprint's TUI requires real-time process metrics (output bytes, stall detection) that the pipeline callback model doesn't provide.
3. **Inline gate evaluation**: Sprint evaluates `gate_passed()` inside `_run_anti_instinct_gate_hook()` with mode-specific logic (off/shadow/soft/full). The pipeline executor assumes gates always run.
4. **Rollout modes**: Sprint has a `gate_rollout_mode` system (off/shadow/soft/full) that gates the behavioral impact of gate results. Pipeline executor has no rollout mode concept.
5. **Circular import risk**: Sprint already uses lazy imports (`from superclaude.cli.pipeline.gates import gate_passed` at line 819, inside a function) to avoid circular dependencies. Deeper integration would need careful import management.

---

## 8. Gaps and Questions

1. **Why wasn't Option C (hybrid) pursued in v3.1?** The gap-remediation-tasklist.md explicitly deferred `attempt_remediation()` integration to v3.2 (BUG-009/P6). Was there a conscious decision against the hybrid approach, or was it simply time-constrained?

2. **Is decompose_deliverables() intended for sprint?** Currently only the roadmap uses it. Sprint tasks come from tasklist files, not from deliverable decomposition. Is there a planned path where sprint tasks get behavioral decomposition?

3. **TrailingGateRunner is instantiated but never wired**: Sprint creates a `DeferredRemediationLog` (line 1154) and a `SprintGatePolicy` (line 1159) but never creates a `TrailingGateRunner`. All gate evaluation is synchronous inline. The trailing infrastructure exists specifically for sprint's use case but remains unconnected.

4. **Pipeline executor retry logic is unused by sprint**: Sprint's tasks have no retry mechanism. If a task fails, it fails. The pipeline executor's `retry_limit` on `Step` (with automatic re-execution) is a capability sprint could benefit from but does not use.

5. **The 42-symbol public API is overprovisioned**: The pipeline `__init__.py` exports 42+ symbols including M2-M4 analysis passes (guard analysis, FMEA, dataflow tracing) that are not used by any CLI executor in production. These appear to be infrastructure built ahead of demand.

---

## 9. Summary

The pipeline module (`src/superclaude/cli/pipeline/`) is a well-engineered generic step sequencer with tiered gates (EXEMPT/LIGHT/STANDARD/STRICT), retry logic, parallel execution, and trailing gate infrastructure. It is fully used by **roadmap**, **roadmap-validate**, and **tasklist** executors -- all three call `execute_pipeline()` with consumer-specific `StepRunner` callables.

**Sprint does NOT call `execute_pipeline()`**. Instead, it has its own orchestration loop in `execute_sprint()` that handles TUI rendering, process monitoring, stall detection, signal handling, and phase-task hierarchy. Sprint does use individual pipeline components directly -- `gate_passed()`, `DeferredRemediationLog`, `TrailingGateResult`, `resolve_gate_mode()` -- but bypasses the executor's retry, sequencing, and trailing gate machinery.

This disconnect is **known and intentional** (BUG-009/P6 in the codebase). The most natural integration path is **Option C (hybrid)**: use `execute_pipeline()` for per-task execution within `execute_phase_tasks()`, while keeping the phase-level loop in sprint's own code. The key prerequisite is mapping sprint `TaskEntry` objects to pipeline `Step` objects and wiring `attempt_remediation()` via its 6-arg callable interface.

`decompose_deliverables()` is used only by the roadmap executor (1 production caller). Sprint does not use it and there is no obvious path for it to do so, since sprint tasks come from tasklist files rather than deliverable decomposition.
