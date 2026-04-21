# Section 8 — Implementation Plan

**Date:** 2026-04-03
**Scope:** Closing the per-task verification gap in the sprint executor
**Source Files:** `research/01` through `research/08`
**Constraint:** Every step cites actual files and line numbers from research findings. No generic actions.

---

## Phase 1 — Prompt Enrichment

**Goal:** Replace the 3-line prompt in `_run_task_subprocess()` with a rich prompt modeled on Path B's `build_prompt()`, including `/sc:task-unified` invocation, sprint context, scope boundary, and result file contract.

**Current state:** `_run_task_subprocess()` at `src/superclaude/cli/sprint/executor.py:1053` sends only task ID, title, phase file path, and description (Research 01, Section 4b). Path B's `build_prompt()` at `src/superclaude/cli/sprint/process.py:123` sends a ~40-line prompt with full behavioral governance (Research 01, Section 5b).

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 1.1 | Create `build_task_prompt()` function | `src/superclaude/cli/sprint/process.py` (new function, after `build_prompt()` at line 123) | Model on `build_prompt()` (process.py:123) but scoped to a single task. Accept `task: TaskEntry`, `phase: Phase`, `config: SprintConfig`, `prior_results: list[TaskResult]`. Return a `str` prompt. |
| 1.2 | Include `/sc:task-unified` invocation | `src/superclaude/cli/sprint/process.py` (inside `build_task_prompt()`) | Emit `"/sc:task-unified Execute task {task.task_id} in @{phase.file} --compliance strict --strategy systematic"`. This matches Path B's command format (process.py:123, Research 01 Section 5b) and triggers loading of `sc-task-unified-protocol/SKILL.md` (Research 03, Section 6). |
| 1.3 | Include Sprint Context block | `src/superclaude/cli/sprint/process.py` (inside `build_task_prompt()`) | Emit sprint name (`config.sprint_name`), phase number (`phase.number`), artifact root (`config.results_dir`), prior-phase dirs — identical fields to Path B's Sprint Context (process.py:123, Research 01 Section 5b). |
| 1.4 | Include Execution Rules block | `src/superclaude/cli/sprint/process.py` (inside `build_task_prompt()`) | Emit tier-based behavior rules: STRICT stops on fail, others log and continue. Mirror Path B's Execution Rules section (process.py:123, Research 01 Section 5b). Include task classifier from `task.classifier` (parsed by `parse_tasklist()` at config.py:306, Research 01 Section 3). |
| 1.5 | Include Scope Boundary | `src/superclaude/cli/sprint/process.py` (inside `build_task_prompt()`) | Emit `"After completing task {task.task_id}, STOP immediately. Do NOT proceed to other tasks."`. Path B says "After completing all tasks, STOP immediately" (Research 01 Section 5b) — this is the single-task equivalent. |
| 1.6 | Include Result File contract | `src/superclaude/cli/sprint/process.py` (inside `build_task_prompt()`) | Emit exact output path (Phase 2 will define per-task paths) and required content format including `EXIT_RECOMMENDATION: CONTINUE/HALT`. Mirrors Path B's Result File instructions (Research 01 Section 5b). |
| 1.7 | Replace 3-line prompt in `_run_task_subprocess()` | `src/superclaude/cli/sprint/executor.py:1053-1068` | Replace the inline `prompt = (f"Execute task...")` block with a call to `build_task_prompt(task, phase, config, prior_results)`. Import `build_task_prompt` from `process.py`. |
| 1.8 | Fix the `__new__` bypass pattern | `src/superclaude/cli/sprint/executor.py:1070-1085` | Replace the `ClaudeProcess.__new__()` + `_Base.__init__()` bypass (Research 01 Section 4c) with proper sprint `ClaudeProcess` construction. Either: (a) add a `task_prompt` parameter to the sprint `ClaudeProcess.__init__()` that overrides `build_prompt()`, or (b) create a `TaskClaudeProcess` subclass that calls `build_task_prompt()` instead of `build_prompt()`. Option (a) is less invasive. |

---

## Phase 2 — Output Isolation

**Goal:** Give each task its own output file instead of all tasks in a phase sharing `config.output_file(phase)`, which causes file collision (Research 01, Section 4d).

**Current state:** `_run_task_subprocess()` at executor.py:1070-1085 passes `config.output_file(phase)` and `config.error_file(phase)` to `ClaudeProcess.__init__()`. Since multiple tasks per phase invoke this with the same phase, each task overwrites the previous (Research 01, Section 4d).

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 2.1 | Add `task_output_file()` method to SprintConfig | `src/superclaude/cli/sprint/models.py` (after `output_file()` method, approx line 420) | `def task_output_file(self, phase: Phase, task_id: str) -> Path:` returns `self.results_dir / f"phase-{phase.number}-{task_id}-output.txt"`. Follows the existing `output_file()` pattern (models.py, used at executor.py:1076, Research 01 Section 4c). |
| 2.2 | Add `task_error_file()` method to SprintConfig | `src/superclaude/cli/sprint/models.py` (adjacent to `task_output_file()`) | `def task_error_file(self, phase: Phase, task_id: str) -> Path:` returns `self.results_dir / f"phase-{phase.number}-{task_id}-errors.txt"`. Mirrors `error_file()` pattern. |
| 2.3 | Add `task_result_file()` method to SprintConfig | `src/superclaude/cli/sprint/models.py` (adjacent) | `def task_result_file(self, phase: Phase, task_id: str) -> Path:` returns `self.results_dir / f"phase-{phase.number}-{task_id}-result.md"`. The result file contract from Phase 1 Step 1.6 will reference this path. |
| 2.4 | Update `_run_task_subprocess()` to use per-task paths | `src/superclaude/cli/sprint/executor.py:1076-1078` | Replace `config.output_file(phase)` with `config.task_output_file(phase, task.task_id)` and `config.error_file(phase)` with `config.task_error_file(phase, task.task_id)`. |
| 2.5 | Store output path on TaskResult | `src/superclaude/cli/sprint/models.py` (TaskResult dataclass, approx line 95) | Ensure `TaskResult.output_path` is populated with the per-task output file path. Currently `output_path` exists on the dataclass (Research 04 Section 2.1) but may not be set correctly in `_run_task_subprocess()`. Verify and fix at executor.py where TaskResult is constructed (approx line 990-1010). |
| 2.6 | Update anti-instinct hook file reference | `src/superclaude/cli/sprint/executor.py:828` | The anti-instinct gate reads `task_result.output_path` (Research 04 Section 2.3). Since Step 2.5 ensures this is correctly set to the per-task path, verify that the hook reads the right file. No code change expected if 2.5 is correct, but verify. |

---

## Phase 3 — Context Injection

**Goal:** Wire `build_task_context()` into the per-task prompt so each task has visibility into what prior tasks accomplished.

**Current state:** `build_task_context()` at `src/superclaude/cli/sprint/process.py:245` is confirmed dead code with zero callers (Research 01, Section 6). It was purpose-built for cross-task context injection. Related dead code: `get_git_diff_context()` (line 310) and `compress_context_summary()` (line 335).

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 3.1 | Verify `build_task_context()` API compatibility | `src/superclaude/cli/sprint/process.py:245-308` | Read the function signature and return type. It accepts prior task results and returns a context string. Confirm it can accept `list[TaskResult]` (from `execute_phase_tasks()` accumulation at executor.py:949, Research 08 Section 4). |
| 3.2 | Call `build_task_context()` from `build_task_prompt()` | `src/superclaude/cli/sprint/process.py` (inside `build_task_prompt()` created in Phase 1) | If `prior_results` is non-empty, call `build_task_context(prior_results)` and prepend the returned context string to the prompt. This activates the existing dead code with zero new logic. |
| 3.3 | Pass accumulated results through the call chain | `src/superclaude/cli/sprint/executor.py:912-1050` | In `execute_phase_tasks()`, the per-task loop accumulates results at line 949 (`results.append(task_result)`). Pass the current `results` list to `_run_task_subprocess()` as a new `prior_results` parameter. Update `_run_task_subprocess()` signature at line 1053 to accept `prior_results: list[TaskResult] = []`. |
| 3.4 | Update `_run_task_subprocess()` to pass results to prompt builder | `src/superclaude/cli/sprint/executor.py:1053` | Pass `prior_results` to `build_task_prompt()` (created in Phase 1, Step 1.7). |
| 3.5 | Validate `get_git_diff_context()` and `compress_context_summary()` | `src/superclaude/cli/sprint/process.py:310, 335` | These are only called by `build_task_context()` (Research 01 Section 6). Once `build_task_context()` is activated, verify they still function correctly. `get_git_diff_context()` runs `git diff` — confirm it works in the isolation directory context (Research 03 Section 3: only `CLAUDE_WORK_DIR` is set, `GIT_CEILING_DIRECTORIES` is NOT set). |

---

## Phase 4 — Semantic Verification Gate

**Goal:** Add a post-task hook that checks whether the task produced its required deliverables and met acceptance criteria keywords, filling the gap identified in Research 04 (neither existing gate verifies task-specific acceptance criteria).

**Current state:** Two post-task hooks exist (Research 04). The wiring gate (executor.py:450) checks codebase structural integrity but is completely task-agnostic. The anti-instinct gate (executor.py:787) reads the task output file but checks roadmap-specific frontmatter fields (`undischarged_obligations`, etc.), making it a no-op for sprint tasks (Research 04, Section 4). Extension Path B (new third hook) was identified as the cleanest approach (Research 04, Section 5).

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 4.1 | Extend `TaskEntry` with `acceptance_criteria` field | `src/superclaude/cli/sprint/models.py:26` | Add `acceptance_criteria: list[str] = field(default_factory=list)` to the `TaskEntry` dataclass. Currently the dataclass has `task_id`, `title`, `description`, `dependencies`, `command`, `classifier` (Research 01 Section 3). The new field will hold parsed acceptance criteria strings. |
| 4.2 | Extend `parse_tasklist()` to extract acceptance criteria | `src/superclaude/cli/sprint/config.py:306-364` | After existing field extraction (description from `**Deliverables:**`, dependencies from `**Dependencies:**`, classifier from table row — Research 01 Section 3), add extraction of `**Acceptance Criteria:**` section content. Parse bullet points as individual criteria strings. |
| 4.3 | Extend `TaskEntry` with `deliverable_paths` field | `src/superclaude/cli/sprint/models.py:26` | Add `deliverable_paths: list[str] = field(default_factory=list)` to TaskEntry. Parsed from `**Deliverables:**` section file path references (e.g., lines matching `src/...` or `tests/...`). |
| 4.4 | Create `run_post_task_semantic_hook()` | `src/superclaude/cli/sprint/executor.py` (after `run_post_task_anti_instinct_hook()` at line 909) | New function with same signature pattern as existing hooks (Research 04 Section 1.1): `run_post_task_semantic_hook(task, config, task_result, ledger) -> TaskResult`. |
| 4.5 | Implement deliverable path existence check | Inside `run_post_task_semantic_hook()` | For each path in `task.deliverable_paths`, check `(config.release_dir / path).exists()`. This is a pure-Python check compatible with the `gate_passed()` model (Research 04 Section 3). Report missing deliverables as `failure_reason`. |
| 4.6 | Implement acceptance criteria keyword check | Inside `run_post_task_semantic_hook()` | Read `task_result.output_path` content. For each string in `task.acceptance_criteria`, check if key terms appear in the output (simple substring/regex match). This follows the `SemanticCheck` pattern from `GateCriteria` (Research 04 Section 3, Research 05 Section 2.1). |
| 4.7 | Build `GateCriteria` dynamically per task | `src/superclaude/cli/sprint/executor.py` (inside `run_post_task_semantic_hook()`) | Use `GateCriteria` from `src/superclaude/cli/pipeline/models.py:68` with `enforcement_tier="STANDARD"` and dynamic `semantic_checks` built from the task's acceptance criteria. Call `gate_passed()` from `src/superclaude/cli/pipeline/gates.py:20`. This reuses the existing gate engine (Research 04 Section 5, Extension Path C). |
| 4.8 | Wire the new hook into `execute_phase_tasks()` | `src/superclaude/cli/sprint/executor.py:1028-1040` | Add `task_result = run_post_task_semantic_hook(task, config, task_result, ledger)` after the existing wiring hook (line 1028) and before the anti-instinct hook (line 1034). Follow the same mode resolution pattern (`_resolve_wiring_mode()` defined at line 421, called at line 475, or add a new `_resolve_semantic_mode()`). |
| 4.9 | Honor gate rollout modes | Inside `run_post_task_semantic_hook()` | Support `off`/`shadow`/`soft`/`full` modes matching the existing pattern (Research 04 Sections 1.3, 2.4). In `shadow` mode, log findings to `DeferredRemediationLog` without affecting task status. In `full` mode, set `TaskStatus.FAIL` on blocking findings. |

---

## Phase 5 — Per-Task Progress Logging

**Goal:** Write task results to `execution-log.jsonl` as they complete, enabling task-level resume and crash recovery.

**Current state:** The JSONL log records only phase-level events: `sprint_start`, `phase_start`, `phase_complete`, `sprint_complete` (Research 08, Section 1). Individual `TaskResult` objects are accumulated in memory only (Research 08, Section 4). `build_resume_output()` at models.py:633 generates `--resume <task_id>` commands but is dead code (Research 08, Section 4). The `--resume` flag does not exist on the CLI (Research 08, Section 3).

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 5.1 | Add `write_task_start()` to SprintLogger | `src/superclaude/cli/sprint/logging_.py` (after `write_phase_start()` at line 58) | New method: `write_task_start(self, phase: int, task_id: str, task_title: str)`. Emit `{"event": "task_start", "phase": N, "task_id": "T01.01", "task_title": "...", "timestamp": "..."}`. Follow the existing `_jsonl()` append pattern (logging_.py:173, Research 08 Section 1). |
| 5.2 | Add `write_task_complete()` to SprintLogger | `src/superclaude/cli/sprint/logging_.py` (after `write_task_start()`) | New method: `write_task_complete(self, phase: int, task_id: str, status: TaskStatus, duration_seconds: float, gate_outcome: str, output_path: str)`. Emit `{"event": "task_complete", ...}`. Include all `TaskResult` fields needed for resume decisions. |
| 5.3 | Pass SprintLogger to `execute_phase_tasks()` | `src/superclaude/cli/sprint/executor.py:912` | Add `logger: SprintLogger | None = None` parameter to `execute_phase_tasks()`. The logger is created at executor.py:1140 (approx) and is available in `execute_sprint()`. Pass it through. |
| 5.4 | Call logger in per-task loop | `src/superclaude/cli/sprint/executor.py:950-1000` (inside per-task loop) | Before subprocess launch: `logger.write_task_start(phase.number, task.task_id, task.title)`. After result determination: `logger.write_task_complete(phase.number, task.task_id, task_result.status, ...)`. Place these adjacent to existing TUI update calls (lines 979-984, Research 08 Section 4). |
| 5.5 | Write per-task result file to disk | `src/superclaude/cli/sprint/executor.py` (in per-task loop, after task completion) | Write a minimal result file to `config.task_result_file(phase, task.task_id)` (from Phase 2 Step 2.3) containing task status, duration, and gate outcome. This provides a filesystem checkpoint that survives crashes (Research 08 Section 5 identifies this as the critical missing piece). |
| 5.6 | Add task-level skip logic for resume | `src/superclaude/cli/sprint/executor.py:912-950` (top of per-task loop) | Before launching a task subprocess, check if `config.task_result_file(phase, task.task_id).exists()`. If it does and contains `status: PASS`, skip the task. This enables task-level resume within a phase that was interrupted. Log skipped tasks to both JSONL and TUI. |
| 5.7 | Add `--resume-tasks` flag to CLI | `src/superclaude/cli/sprint/commands.py:73-86` | Add `--resume-tasks` boolean flag (default False). When True, enable the task-level skip logic from Step 5.6. When False (default), preserve current behavior of re-executing entire phases. This is safer than always resuming because some tasks may have partial output. |
| 5.8 | Activate `build_resume_output()` | `src/superclaude/cli/sprint/models.py:633` | Currently dead code (Research 08 Section 4). Wire it into `SprintResult` construction so the resume command includes the last completed task ID when `--resume-tasks` is available. |

---

## Integration Checklist

This checklist must be verified after all five phases are implemented.

### Prompt Enrichment (Phase 1)
- [ ] `build_task_prompt()` exists in `process.py` and produces a prompt containing `/sc:task-unified`, Sprint Context, Execution Rules, Scope Boundary, and Result File contract
- [ ] `_run_task_subprocess()` at executor.py:1053 calls `build_task_prompt()` instead of inline 3-line prompt
- [ ] The `__new__` bypass pattern at executor.py:1070-1085 is replaced with proper `ClaudeProcess` construction
- [ ] Sprint `ClaudeProcess.__init__()` at process.py:97 accepts an optional `task_prompt` parameter or `TaskClaudeProcess` subclass exists

### Output Isolation (Phase 2)
- [ ] `SprintConfig.task_output_file()`, `task_error_file()`, `task_result_file()` methods exist in models.py
- [ ] `_run_task_subprocess()` uses per-task output paths, not phase-level paths
- [ ] `TaskResult.output_path` is correctly set to the per-task output file
- [ ] No two tasks in the same phase write to the same output file

### Context Injection (Phase 3)
- [ ] `build_task_context()` at process.py:245 is called from `build_task_prompt()`
- [ ] `execute_phase_tasks()` passes accumulated `results` list to `_run_task_subprocess()`
- [ ] `_run_task_subprocess()` passes `prior_results` to `build_task_prompt()`
- [ ] `get_git_diff_context()` and `compress_context_summary()` are validated in the isolation directory context

### Semantic Verification Gate (Phase 4)
- [ ] `TaskEntry` dataclass has `acceptance_criteria` and `deliverable_paths` fields
- [ ] `parse_tasklist()` extracts acceptance criteria and deliverable paths from phase files
- [ ] `run_post_task_semantic_hook()` exists and follows the existing hook signature pattern
- [ ] The hook checks deliverable path existence and acceptance criteria keyword presence
- [ ] The hook supports `off`/`shadow`/`soft`/`full` rollout modes
- [ ] The hook is called from `execute_phase_tasks()` between the wiring hook and anti-instinct hook
- [ ] `GateCriteria` is built dynamically per task and evaluated via `gate_passed()`

### Per-Task Progress Logging (Phase 5)
- [ ] `SprintLogger` has `write_task_start()` and `write_task_complete()` methods
- [ ] `execution-log.jsonl` contains `task_start` and `task_complete` events when per-task execution is used
- [ ] Per-task result files are written to `config.task_result_file(phase, task_id)` after each task completes
- [ ] `--resume-tasks` CLI flag exists and enables task-level skip logic
- [ ] Task-level skip logic checks for existing result files and skips PASS tasks
- [ ] `build_resume_output()` is activated and includes last completed task ID
- [ ] Crash mid-phase followed by `--resume-tasks` re-runs only uncompleted tasks

### Cross-Cutting Concerns
- [ ] No circular imports introduced (sprint imports from pipeline are already lazy — executor.py:819, Research 05 Section 7.2)
- [ ] All new code follows the existing `NFR-007` boundary: pipeline modules do NOT import from sprint (Research 05 Section 1.2)
- [ ] `make test` passes with no new test failures
- [ ] `make lint && make format` passes
- [ ] New functions have type annotations matching existing codebase conventions
- [ ] Dead code activated in Phase 3 (`build_task_context`, `get_git_diff_context`, `compress_context_summary`) has tests covering the activated paths
