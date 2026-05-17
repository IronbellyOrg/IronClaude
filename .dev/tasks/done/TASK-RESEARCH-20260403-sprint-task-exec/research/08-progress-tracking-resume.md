# 08 - Progress Tracking and Resume

**Status**: Complete
**Investigator**: Code Tracer
**Date**: 2026-04-03
**Research Question**: What gets logged during sprint execution, at what granularity, how does resume work, and what state survives a crash?

## Files Under Investigation

| File | Key Symbols |
|------|-------------|
| `src/superclaude/cli/sprint/logging_.py` | SprintLogger, write_header, write_phase_start, write_phase_result, write_summary |
| `src/superclaude/cli/sprint/models.py` | SprintResult, TaskResult, TaskStatus, TurnLedger, resume_command(), build_resume_output() |
| `src/superclaude/cli/sprint/commands.py` | --start/--end flags, run subcommand |
| `src/superclaude/cli/sprint/executor.py` | execute_phase_tasks(), execute_sprint() |

---

## 1. What Gets Written to execution-log.jsonl

**File**: `src/superclaude/cli/sprint/logging_.py` (lines 12-184)

The SprintLogger writes **four event types** to the JSONL file via `_jsonl()` (line 173), which appends one JSON object per line:

### Event: `sprint_start` (write_header, line 30)
Fields: `event`, `timestamp`, `index` (path to tasklist-index.md), `phases` (range string like "1-last"), `max_turns`, `model`.

### Event: `phase_start` (write_phase_start, line 58)
Fields: `event`, `phase` (number), `phase_name`, `phase_file` (path), `timestamp`.

### Event: `phase_complete` (write_phase_result, line 88)
Fields: `event`, `phase`, `phase_name`, `status` (PhaseStatus value), `exit_code`, `started_at`, `finished_at`, `duration_seconds`, `output_bytes`, `error_bytes`, `last_task_id`, `files_changed`.

### Event: `phase_interrupt` (write_phase_interrupt, line 70)
Fields: `event`, `phase`, `phase_name`, `started_at`, `interrupted_at`, `duration_seconds`, `exit_code`. This is written when a signal interrupts mid-phase to ensure every `phase_start` has a closing event.

### Event: `sprint_complete` (write_summary, line 153)
Fields: `event`, `outcome` (SprintOutcome value), `duration_seconds`, `phases_passed`, `phases_failed`, `halt_phase`.

**Critical finding: Logging is PHASE-LEVEL only.** There are no `task_start` or `task_complete` events in the JSONL log. Individual task results within `execute_phase_tasks()` are never written to `execution-log.jsonl`.

---

## 2. Execution-log.md (Human-Readable Log)

**File**: `src/superclaude/cli/sprint/logging_.py` (lines 44-56, 108-119, 166-171)

The markdown log consists of:
- A header with sprint metadata (written once by `write_header`)
- A table with columns: Phase, Status, Started, Completed, Duration, Exit
- Phase rows appended by `write_phase_result` (line 118) -- only for non-`PASS_NO_SIGNAL` statuses
- A footer with Outcome, Total duration, and a Resume command if halted (line 171)

Again, no per-task rows -- purely phase-level.

---

## 3. How --start/--end Work for Resume

**File**: `src/superclaude/cli/sprint/commands.py` (lines 73-86)

The `run` subcommand accepts:
- `--start` (`start_phase`, default=1): Start from phase N
- `--end` (`end_phase`, default=0 meaning last discovered): End at phase N

These values flow into `SprintConfig.start_phase` and `SprintConfig.end_phase` (models.py lines 309-310). The `active_phases` property (line 404) filters the full phase list to only those within `[start_phase, end_phase]`.

**Resume mechanism**: When a sprint halts, `SprintResult.resume_command()` (models.py line 490) generates a command like:
```
superclaude sprint run <index_path> --start <halt_phase> --end <end_phase>
```

This is written to both:
- The markdown log footer (logging_.py line 171)
- The TUI display (tui.py line 279)

**There is NO `--resume` flag on the CLI.** The resume mechanism works exclusively through `--start`, which simply skips all phases before the specified number. This means:
- Resume is phase-granularity only
- If a phase with 20 tasks crashed after completing 15, resume re-runs the entire phase from task 1
- There is no task-level checkpoint

---

## 4. Per-Task Disk Writes Within execute_phase_tasks()

**File**: `src/superclaude/cli/sprint/executor.py` (lines 912-1050)

The `execute_phase_tasks()` function iterates over tasks and spawns subprocesses. Within its per-task loop, the following disk writes occur:

1. **ClaudeProcess subprocess output** -- the subprocess itself writes to stdout/stderr files, but these are managed by the subprocess, not by `execute_phase_tasks()`.
2. **TUI updates** (lines 979-984, 1043-1048) -- in-memory only, no disk write.
3. **Wiring hook** (line 1028) -- may write to `remediation.json` via `DeferredRemediationLog`.
4. **Anti-instinct hook** (line 1034) -- may update `ShadowGateMetrics`, which is in-memory.

**There is no JSONL logging of individual task completions.** The `SprintLogger` is not passed to or called within `execute_phase_tasks()`. Task results are accumulated in an in-memory `results: list[TaskResult]` (line 949) and returned to the caller.

The `AggregatedPhaseReport` class (executor.py line ~196) has `to_yaml()` and `to_markdown()` methods that could serialize per-task data, but `aggregate_task_results()` (line 298) is **defined but never called** from production code.

Similarly, `build_resume_output()` (models.py line 633) generates a resume block with task-level granularity (including a `--resume <task_id>` flag), but it is **defined and never called** -- and the `--resume` flag it references does not exist on the CLI.

---

## 5. What State Is Lost on Crash

### Lost (in-memory only, never persisted during execution):
- **All TaskResult objects** -- accumulated in a list inside `execute_phase_tasks()`, returned to caller only on normal completion
- **TurnLedger state** -- budget consumed, reimbursed, wiring turns -- all in-memory
- **ShadowGateMetrics** -- all gate evaluation metrics
- **TrailingGateResult list** -- accumulated across phases in `all_gate_results`
- **Which task within a phase was last completed** -- no checkpoint

### Persisted (survives crash):
- **execution-log.jsonl** -- all `phase_start` and `phase_complete` events written before the crash (append mode, line 174)
- **execution-log.md** -- phase table rows written before the crash
- **Phase output files** -- `results/phase-N-output.txt` and `results/phase-N-errors.txt` (written by subprocess I/O redirection)
- **Phase result files** -- `results/phase-N-result.md` (written by `_write_executor_result_file` after phase completes, line 1406)
- **remediation.json** -- if DeferredRemediationLog flushed before crash
- **Subprocess output** -- whatever the Claude subprocess wrote to disk during its execution

### Crash scenario analysis:
If the process crashes mid-phase (e.g., between task 15 and 16 of a 20-task phase):
- The JSONL log has a `phase_start` with no matching `phase_complete` (unbalanced)
- No record exists of which tasks completed within that phase
- Resume via `--start N` re-executes the entire phase from scratch
- All work done by completed tasks within the phase is in the filesystem (Claude's output), but there's no structured record of it

---

## 6. What .roadmap-state.json Tracks

**File**: `src/superclaude/cli/sprint/commands.py` (lines 36-68), `src/superclaude/cli/sprint/config.py` (lines 171-186)

`.roadmap-state.json` is **NOT read or written during sprint execution**. It serves two distinct purposes:

### Purpose 1: Fidelity gate (commands.py, `_check_fidelity()`)
Before sprint execution begins, `_check_fidelity()` reads `.roadmap-state.json` from the sprint directory to check if `fidelity_status == "fail"`. If so, the sprint is blocked unless `--force-fidelity-fail` is provided. This is a pre-flight gate, not a progress tracker.

Fields checked: `fidelity_status`, `steps.spec-fidelity.output_file`.

### Purpose 2: Release directory detection (config.py, lines 171-186)
During config loading, the presence of `.roadmap-state.json` in a grandparent directory is used as a heuristic to detect the release directory boundary.

**Key finding**: `.roadmap-state.json` is a roadmap pipeline artifact (created by `superclaude roadmap`), not a sprint progress tracker. The sprint execution loop neither reads from nor writes to this file. Sprint progress state is tracked only via the JSONL/MD logs and the in-memory data structures described above.

---

## Gaps and Questions

1. **No task-level logging to JSONL**: The infrastructure exists (`TaskResult`, `AggregatedPhaseReport.to_yaml()`, `build_resume_output()`) but is not wired into the execution loop. This means crash recovery loses all intra-phase progress.

2. **`build_resume_output()` is dead code**: Defined at models.py line 633, generates `--resume <task_id>` commands, but is never called. The `--resume` CLI flag it references does not exist.

3. **`aggregate_task_results()` is dead code**: Defined at executor.py line 298, never called from production code. It would produce a structured per-task report but isn't used.

4. **No task-level checkpoint file**: Unlike phase-level result files (`phase-N-result.md`), there is no per-task result file written during `execute_phase_tasks()`. If the process dies mid-phase, there is no way to know which tasks completed.

5. **Unbalanced JSONL on crash**: A crash mid-phase leaves a `phase_start` event without a corresponding `phase_complete`. The `read_status_from_log()` function (line 187) is a stub that doesn't parse JSONL at all, so this cannot be detected programmatically.

6. **`status` and `logs` commands are stubs**: Both `read_status_from_log()` (line 187) and `tail_log()` (line 194) print placeholder messages. They cannot reconstruct sprint state from the JSONL log.

7. **Phase-granularity resume is lossy**: For phases with many tasks, a crash-and-resume re-executes all tasks in the phase, potentially duplicating work. The `TurnLedger` state is also lost, so budget accounting restarts.

---

## Summary

The sprint progress tracking system operates at **phase granularity only**. The JSONL log records four event types (sprint_start, phase_start, phase_complete, sprint_complete) with no per-task events. Individual task results exist as in-memory `TaskResult` objects within `execute_phase_tasks()` but are never persisted to disk during execution.

Resume is implemented via the `--start` CLI flag, which skips entire phases. There is no `--resume` flag for task-level recovery despite `build_resume_output()` generating such commands (dead code). On crash, all intra-phase state is lost: which tasks completed, budget consumption, gate metrics. The filesystem retains whatever the Claude subprocess wrote, but there is no structured index of per-task completion.

`.roadmap-state.json` is unrelated to sprint progress -- it's a roadmap pipeline artifact used only as a pre-flight fidelity gate and a directory detection heuristic.

The gap between the data model (which has rich per-task structures) and the logging system (which is phase-only) represents a clear opportunity: wiring `TaskResult` persistence into the `execute_phase_tasks()` loop would enable task-level resume with minimal architectural change.
