---
title: "Chunk 2: Sprint TUI v2 — Path A/B Refactoring Analysis"
chunk: sprint-tui-v2
spec_sections: "3.2, 4.2"
---

# Sprint TUI v2 -- Refactoring Analysis

## Executive Summary

The v3.7 TUI v2 spec defines 10 features (F1-F10) that depend on NDJSON parsing via the `OutputMonitor` daemon thread. Path A (`execute_phase_tasks`) **does not use `OutputMonitor` at all** -- it constructs ad-hoc `MonitorState` objects with only `events_received`, `last_event_time`, and `last_task_id` populated. This means 6 of 10 features (F1, F2-partial, F3-partial, F4, F5, F8) assume Path B's single-subprocess NDJSON stream and require explicit adaptation for Path A. Features that operate on post-phase or post-sprint aggregate data (F6, F7, F8-partial, F9, F10) are inherently path-agnostic but need their data sources wired from Path A's `TaskResult` accumulator rather than from `MonitorState`.

## Critical Architectural Discovery

**Path A does not start the `OutputMonitor`.** Evidence:

- `executor.py:1201-1233` -- when `tasks` is truthy (Path A), the code calls `execute_phase_tasks()` and then `continue`, skipping the block at lines 1240-1244 where `monitor.reset()` and `monitor.start()` are called.
- `executor.py:978-984` and `1042-1048` -- Path A constructs throwaway `MonitorState()` objects with 3 fields set manually, bypassing the NDJSON parsing infrastructure entirely.
- `executor.py:1078` -- all per-task subprocesses write to the **same** `phase-N-output.txt` file, meaning each task overwrites the previous task's NDJSON output.

**Consequence**: Every TUI v2 feature that reads from `MonitorState` fields populated by `OutputMonitor._extract_signals_from_event()` receives default/zero values under Path A. The spec's data model additions (8 new `MonitorState` fields in Section 7.1) are dead code for production sprints.

## Per-Feature Analysis

### F1: Activity Stream

- **Current assumption**: Path B single-stream. The spec defines a 3-line FIFO ring buffer of tool calls extracted from `tool_use` NDJSON events. Data source is `MonitorState.activity_log: list[tuple[float, str, str]]`, populated by `OutputMonitor._extract_signals_from_event()`.
- **Path A compatibility**: Incompatible. Path A never starts `OutputMonitor`, so `activity_log` is always `[]`. Even if the monitor were started, each task subprocess overwrites `phase-N-output.txt`, so the monitor would lose context between tasks.
- **Data source difference**: Path B has one continuous NDJSON stream per phase; Path A has N sequential NDJSON streams (one per task), all written to the same file path with no append guarantee.
- **Recommendation**: NEEDS PATH A ADAPTATION
- **Adaptation needed**: Two options:
  1. **Per-task OutputMonitor**: Start/reset the monitor for each task subprocess within `execute_phase_tasks()`. The monitor would parse each task's NDJSON and populate `activity_log`. Requires changing the output file to per-task (`phase-N-task-TPPTT-output.txt`) or appending to a shared file.
  2. **Synthetic activity entries**: After each task subprocess completes, append a synthetic entry to `activity_log` from `TaskResult` data (task ID, status, duration). Cheaper but lower fidelity than real-time tool-call streaming.
  - **Recommended**: Option 2 for v3.7 (low cost, provides useful signal), Option 1 deferred to v3.8 when per-task output files are addressed.

### F2: Enhanced Phase Table

- **Current assumption**: Mixed. Adding Turns/Output columns reads from `PhaseResult.turns`/`output_bytes` (post-phase, path-agnostic) for completed phases. For the running phase, reads from `MonitorState.turns`/`output_size_display` (Path B only -- populated by NDJSON parsing).
- **Path A compatibility**: Partially compatible. Completed-phase columns work for both paths. Running-phase live data is unavailable under Path A because `MonitorState.turns` is never populated (no `OutputMonitor`).
- **Data source difference**: Path B populates `MonitorState.turns` by counting `"type":"assistant"` NDJSON events in real time. Path A has no equivalent real-time signal. However, Path A *does* have per-task `turns_consumed` on `TaskResult` -- these could be accumulated as tasks complete.
- **Recommendation**: NEEDS PATH A ADAPTATION (minor)
- **Adaptation needed**: In the Path A TUI update hooks (executor.py:978-984, 1042-1048), populate `MonitorState.turns` by summing `TaskResult.turns_consumed` from completed tasks in the current phase. Note: `turns_consumed` is currently always 0 (Deficiency 2 from context-01), so this requires the TurnLedger bug fix first. Also populate `MonitorState.output_bytes` from `TaskResult.output_bytes` accumulation. The `PhaseResult.turns` and `PhaseResult.output_bytes` fields should be set from aggregated `TaskResult` data when Path A builds `PhaseResult` (executor.py:1217-1219).

### F3: Task-Level Progress Bar

- **Current assumption**: Mixed. Pre-scans task count into `SprintConfig.total_tasks` at sprint start (path-agnostic). Tracks progress via `MonitorState.last_task_id` ordinal position (works for both paths but with different semantics) and sum of completed tasks from finished phases.
- **Path A compatibility**: Mostly compatible. Path A already sets `MonitorState.last_task_id = task.task_id` in its ad-hoc updates (executor.py:983, 1047). The task-level progress bar can use this directly. However, the spec's `MonitorState.total_tasks_in_phase` and `completed_task_estimate` fields are populated by the monitor thread's regex matching, which is Path B only.
- **Data source difference**: Path A knows the exact task count (it has the `tasks` list) and exact completion count (it tracks the loop index `i`). Path B estimates these by regex-scanning NDJSON output. Path A's data is strictly superior.
- **Recommendation**: WORKS FOR BOTH (with minor wiring)
- **Adaptation needed**: In the Path A TUI update hooks, set `MonitorState.total_tasks_in_phase = len(tasks)` and `MonitorState.completed_task_estimate = i` (pre-task) / `i + 1` (post-task). This is more accurate than Path B's regex estimation and requires 2 lines of code.

### F4: Conditional Error Panel

- **Current assumption**: Path B single-stream. Errors are extracted from `tool_result` NDJSON events with `is_error: true` or Bash `exit_code != 0`. Data stored in `MonitorState.errors: list[tuple[str, str, str]]`.
- **Path A compatibility**: Incompatible as specified. Path A does not run `OutputMonitor`, so `errors` is always `[]`. Path A does have `TaskResult.exit_code` and `TaskResult.status`, but these are coarser than per-tool-call error extraction.
- **Data source difference**: Path B gets granular per-tool-call errors in real time. Path A gets per-task pass/fail after the subprocess exits.
- **Recommendation**: NEEDS PATH A ADAPTATION
- **Adaptation needed**: Two levels:
  1. **Task-level errors** (cheap): After each task subprocess, if `TaskResult.status.is_failure`, append `(task.task_id, "subprocess", f"exit code {exit_code}")` to `MonitorState.errors`. Provides basic error visibility.
  2. **Tool-level errors** (expensive): Run `OutputMonitor` per-task to extract granular tool errors. Requires per-task output file changes (same blocker as F1 Option 1).
  - **Recommended**: Level 1 for v3.7. It answers the operator's primary question ("which tasks failed?") without the per-task output file refactor.

### F5: LLM Context Lines

- **Current assumption**: Path B single-stream. Shows two lines: `Prompt: <preview>` (static per phase) and `Agent: <last assistant text>`. `prompt_preview` is stored on `Phase` or `SprintConfig`. `last_assistant_text` comes from `MonitorState.last_assistant_text`, populated by parsing `assistant` NDJSON events.
- **Path A compatibility**: Partially compatible. `prompt_preview` can be set from the per-task prompt string (changes per task, not per phase). `last_assistant_text` is unavailable (no `OutputMonitor`).
- **Data source difference**: Path B has one prompt per phase and a continuous assistant text stream. Path A has N prompts (one per task) and no real-time text stream.
- **Recommendation**: NEEDS PATH A ADAPTATION (consider deprioritization)
- **Adaptation needed**: For Path A, `Prompt:` could show the current task's prompt preview (set in the pre-task TUI hook). `Agent:` would remain blank unless per-task `OutputMonitor` is enabled. The value of showing a 60-character prompt preview for a 3-line task prompt is questionable -- the entire prompt is already visible in the task ID. **Consider deprioritizing F5 for Path A** unless the per-task prompt enrichment from context-02 (Rulings 1, 2, 4) is implemented first, which would make the preview more informative.

### F6: Enhanced Terminal Panels

- **Current assumption**: Path-agnostic (post-sprint aggregate). Reads from `SprintResult` aggregate properties: `total_turns`, `total_tokens_in`, `total_tokens_out`, `total_output_bytes`, `total_files_changed`. These are computed from `PhaseResult` fields.
- **Path A compatibility**: Compatible in structure, but requires data population. Path A builds `PhaseResult` (executor.py:1217-1219) without populating `turns`, `tokens_in`, `tokens_out`, or `files_changed`. These must be aggregated from `TaskResult` data.
- **Data source difference**: Path B populates `PhaseResult` fields from `OutputMonitor` state (turns counted from NDJSON, etc.). Path A must aggregate from per-task results.
- **Recommendation**: WORKS FOR BOTH (with data wiring)
- **Adaptation needed**: After `execute_phase_tasks()` returns, compute:
  ```python
  phase_result.turns = sum(r.turns_consumed for r in task_results)
  phase_result.output_bytes = sum(r.output_bytes for r in task_results)
  phase_result.files_changed = sum(1 for r in task_results if r.status == TaskStatus.PASS)
  ```
  `tokens_in`/`tokens_out` require NDJSON parsing (not available from Path A's current data model). Either: (a) add token counting to `_run_task_subprocess` by scanning the output file post-completion, or (b) defer token display for Path A phases. Note: `turns_consumed` is currently 0 (Deficiency 2), so the TurnLedger fix is a prerequisite.

### F7: Sprint Name in Title

- **Current assumption**: Path-agnostic. One-line change to the TUI panel title.
- **Path A compatibility**: Fully compatible. Reads `release_name` from `SprintConfig`, which exists for both paths.
- **Data source difference**: None.
- **Recommendation**: WORKS FOR BOTH
- **Adaptation needed**: None. Implement as specified.

### F8: Post-Phase Summary

- **Current assumption**: Mixed. Step 1 (NDJSON extraction of 5 categories) assumes Path B's single NDJSON stream. Steps 2-4 (Haiku narrative, write summary, update tmux) are path-agnostic post-phase operations.
- **Path A compatibility**: Step 1 is incompatible as specified. Path A's per-task subprocesses overwrite `phase-N-output.txt`, so the NDJSON file at phase completion contains only the last task's output. Steps 2-4 are fully compatible.
- **Data source difference**: Path B has one complete NDJSON file per phase. Path A has the last task's NDJSON plus structured `TaskResult` data for all tasks.
- **Recommendation**: NEEDS PATH A ADAPTATION
- **Adaptation needed**: For Path A, replace NDJSON-based extraction (Step 1) with `TaskResult`-based extraction:
  - **Task status**: Directly from `TaskResult.status` per task (superior to NDJSON parsing).
  - **Files changed**: From `TaskResult` or post-task git diff (not currently tracked per-task).
  - **Validation evidence**: Not available from `TaskResult` without NDJSON parsing. Could scan the last task's output file as a partial signal.
  - **Agent reasoning excerpts**: Not available without NDJSON parsing.
  - **Errors**: From `TaskResult.status.is_failure` + `exit_code`.
  
  The `PhaseSummarizer` should accept a `list[TaskResult]` as an alternative input to NDJSON, producing a structured summary from orchestrator-level data. The Haiku narrative can work from either input format.

### F9: Tmux Summary Pane

- **Current assumption**: Path-agnostic (depends on F8 output). Creates a 3-pane tmux layout and displays `phase-N-summary.md` files produced by F8.
- **Path A compatibility**: Fully compatible if F8 is adapted for Path A. The tmux pane just displays whatever summary file exists.
- **Data source difference**: None (consumes F8's output file, not NDJSON directly).
- **Recommendation**: WORKS FOR BOTH
- **Adaptation needed**: None beyond F8 adaptation. The tmux integration is display-layer only.

### F10: Release Retrospective

- **Current assumption**: Path-agnostic (post-sprint aggregate). Reads all phase summary files (F8 output), aggregates cross-phase patterns, generates Haiku narrative.
- **Path A compatibility**: Fully compatible if F8 is adapted for Path A.
- **Data source difference**: None (consumes F8's summary files, not NDJSON directly).
- **Recommendation**: WORKS FOR BOTH
- **Adaptation needed**: None beyond F8 adaptation. The retrospective reads from summary files and `SprintResult` aggregate data, both of which are available for both paths.

## Feature Compatibility Matrix

| Feature | Path A Compatible | Path B Compatible | Needs Adaptation | Priority for Path A | Blocked by Deficiency |
|---------|------------------|------------------|-----------------|--------------------|-----------------------|
| F1: Activity Stream | No | Yes | Yes -- synthetic entries or per-task monitor | Medium | Per-task output file sharing |
| F2: Enhanced Phase Table | Partial | Yes | Minor -- wire TaskResult aggregates | High | TurnLedger bug (Deficiency 2) |
| F3: Task-Level Progress | Mostly | Yes | Trivial -- 2 lines in TUI hooks | High | None |
| F4: Conditional Error Panel | No | Yes | Yes -- task-level errors from TaskResult | Medium | None (task-level); per-task output file (tool-level) |
| F5: LLM Context Lines | No | Yes | Yes -- questionable value for Path A | Low | Per-task prompt enrichment |
| F6: Enhanced Terminal Panels | Structure yes, data no | Yes | Moderate -- aggregate from TaskResult | High | TurnLedger bug; token counting |
| F7: Sprint Name in Title | Yes | Yes | None | High (trivial) | None |
| F8: Post-Phase Summary | Step 1 no, Steps 2-4 yes | Yes | Yes -- TaskResult-based extraction | High | Per-task output file sharing (for NDJSON categories) |
| F9: Tmux Summary Pane | Yes (if F8 adapted) | Yes | None beyond F8 | Medium | F8 |
| F10: Release Retrospective | Yes (if F8 adapted) | Yes | None beyond F8 | Medium | F8 |

## Net Changes to Spec

### Must Change

1. **F8 Step 1 must accept `list[TaskResult]` as alternative to NDJSON.** The `PhaseSummarizer` interface should accept either a single NDJSON file path (Path B) or a list of `TaskResult` objects (Path A). Path A's data is structured and more reliable than regex-parsed NDJSON for task status and error categories.

2. **Section 7.1 MonitorState fields must be populated by Path A.** The spec adds 8 fields to `MonitorState` but only the `OutputMonitor` daemon populates them. Path A must populate these fields in its ad-hoc TUI update hooks (executor.py:978-984, 1042-1048), or the fields must be documented as Path B only.

3. **Section 7.2 PhaseResult fields must be wired from TaskResult aggregation.** Path A builds `PhaseResult` at executor.py:1217-1219 without populating `turns`, `tokens_in`, `tokens_out`, or `files_changed`. These must be computed from the `task_results` list.

4. **F2 running-phase columns need a Path A data source.** The spec reads `MonitorState.turns` and `output_size_display` for the running phase, but Path A does not populate these. Running-phase data for Path A should come from accumulated `TaskResult` values within `execute_phase_tasks()`.

### Should Change

5. **Per-task output files should be separated.** Currently all Path A tasks write to `phase-N-output.txt`, overwriting each other. Changing to `phase-N-task-TPPTT-output.txt` would enable per-task `OutputMonitor` for real-time features (F1, F4 tool-level, F5 agent text). This is a prerequisite for full TUI v2 fidelity under Path A but can be deferred.

6. **F5 should be deprioritized for Path A.** The LLM context lines feature provides minimal value when the per-task prompt is a 3-line string. If per-task prompt enrichment (context-02 Rulings 1, 2, 4) is implemented, F5 becomes more useful. Recommend implementing F5 for Path B only in v3.7, revisiting for Path A in v3.8.

7. **F1 should use synthetic entries for Path A in v3.7.** Real-time tool-call streaming requires per-task output file changes. For v3.7, append a synthetic activity entry per completed task (task ID, status, duration) to provide basic activity visibility.

8. **F4 should use task-level granularity for Path A in v3.7.** Per-tool-call error extraction requires `OutputMonitor`. Task-level error entries (task ID, "subprocess", exit code) provide the operator's primary signal without infrastructure changes.

### Prerequisite from Other Chunks

9. **TurnLedger bug fix (Deficiency 2) is a prerequisite for F2 and F6.** `turns_consumed` always returns 0, so turn-based columns and terminal panels will show zeros for Path A phases. The fix in `_run_task_subprocess` (calling `count_turns_from_output()` on the task's NDJSON file) must land before or alongside the TUI v2 features.

10. **The per-task output file overwrite problem (executor.py:1078) is the single largest blocker.** All Path A subprocesses write to the same `phase-N-output.txt`. This prevents per-task NDJSON parsing, loses historical output, and makes post-phase NDJSON extraction (F8 Step 1) see only the last task's data. Fixing this (per-task output files with a phase-level aggregation) unlocks full TUI v2 fidelity for Path A.

### Implementation Priority Order

1. **F7** -- trivial, zero risk, immediate visual improvement
2. **F3** -- 2-line change, high value (task progress is the most important signal for Path A operators)
3. **F2 + F6** -- moderate wiring, high value (after TurnLedger fix)
4. **F4** -- task-level error panel, moderate value
5. **F8** -- dual-input `PhaseSummarizer`, enables F9 and F10
6. **F9 + F10** -- depends on F8, no Path A adaptation needed
7. **F1** -- synthetic entries for v3.7, real-time deferred
8. **F5** -- deprioritize for Path A until per-task prompt enrichment lands
