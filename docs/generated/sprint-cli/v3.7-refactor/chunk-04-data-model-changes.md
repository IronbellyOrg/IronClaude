---
title: "Chunk 4: Data Model Changes — Path A/B Refactoring Analysis"
chunk: data-model-changes
spec_sections: "7"
generated: 2026-04-03
---

# Data Model Changes — Refactoring Analysis

## Executive Summary

Section 7 of the v3.7 spec adds 8 fields to `MonitorState`, 3 fields to `PhaseResult`, 5 aggregate properties to `SprintResult`, 2 fields to `SprintConfig`, 1 enum value to `PhaseStatus`, 3 new dataclasses, and 1 field to `SprintTUI`. The data model changes are well-designed for Path B (single freeform subprocess) where a sidecar `OutputMonitor` thread parses the full NDJSON stream. However, **three compounding bugs in Path A make the telemetry fields unpopulable**:

1. `turns_consumed` is hardcoded to 0 at `executor.py:1092`
2. `TaskResult.output_path` is never set at `executor.py:1017-1025`
3. `gate_rollout_mode` defaults to `"off"` so gates never evaluate

The spec's new `PhaseResult.turns`, `PhaseResult.tokens_in`, and `PhaseResult.tokens_out` fields would aggregate to zero for every production sprint until these bugs are fixed. The `MonitorState` fields face a structural challenge: Path A runs N serial subprocesses per phase, each with its own output file, while `OutputMonitor` is designed to watch a single file.

**Verdict**: The data model changes are sound in design but require three prerequisite bug fixes and one architectural adaptation (per-task monitoring) to deliver value on Path A.


## The Three Bugs That Zero Out Path A's Data Model

### How the bugs interact with Section 7 changes

The spec proposes adding `turns`, `tokens_in`, and `tokens_out` to `PhaseResult` (Section 7.2), then aggregating them on `SprintResult` (Section 7.3). The intended data flow is:

```
NDJSON stream -> OutputMonitor -> MonitorState -> PhaseResult -> SprintResult
```

For Path B, this works: one subprocess produces one NDJSON stream, one `OutputMonitor` watches it, and the final `MonitorState` values are copied to `PhaseResult` at phase completion.

For Path A, the intended flow would be:

```
Per-task subprocess -> NDJSON output -> count turns/tokens -> TaskResult -> aggregate to PhaseResult
```

But all three bugs break this chain:

| Bug | Location | Effect on Data Flow |
|-----|----------|-------------------|
| Bug 1: `turns_consumed = 0` | `executor.py:1092` | `TaskResult.turns_consumed` is always 0. `PhaseResult.turns` would be `sum(0, 0, ..., 0) = 0`. Reimbursement credits are `int(0 * 0.8) = 0`. |
| Bug 2: `output_path` unset | `executor.py:1017-1025` | `TaskResult.output_path` defaults to `""`. Anti-instinct gate at line 826-831 checks `if output_path is not None and output_path.exists()` -- always False because `Path("")` does not exist. Gate vacuously passes. Token counts cannot be extracted post-hoc because no code knows where to look. |
| Bug 3: `gate_rollout_mode = "off"` | `models.py:329` | Mode `"off"` returns at `executor.py:814-816` before any evaluation. Even if Bugs 1-2 were fixed, the gate's credit/remediation logic never executes. |

**Critical observation**: Bug 1 is the most damaging for Section 7's data model changes because even if Bug 2 were fixed (enabling the gate to read output), the reimbursement math and turn tracking would still produce zeros. And `count_turns_from_output()` in `monitor.py:114` -- a function that correctly parses NDJSON for turn counts -- exists but is **never called from any runtime code path**.


## Per-Change Analysis

### 7.1 MonitorState -- New Fields

MonitorState is populated by `OutputMonitor` (a sidecar thread in `monitor.py`) that reads incremental NDJSON from a subprocess output file. For Path B, one `OutputMonitor` watches one file for the entire phase. For Path A, there are N serial subprocesses, each writing to `config.output_file(phase)` (the same file path, overwritten each time per `executor.py:1078`).

| Field | Type | Path A Applicability | Data Source in Per-Task Model | Recommendation |
|-------|------|---------------------|-------------------------------|----------------|
| `activity_log` | `list[tuple[float, str, str]]` | APPLICABLE but requires per-task monitor | Each task subprocess emits tool-use events in NDJSON. Would need an `OutputMonitor` per task or a cumulative monitor that resets between tasks. | EXTEND: accumulate across tasks, reset `max 3` window per task |
| `turns` | `int` | BLOCKED BY BUG 1 | `count_turns_from_output()` exists in `monitor.py:114` but is never called. For Path A, should be called per-task and summed. | EXTEND TO TASK-LEVEL: add as per-task extraction, aggregate to phase |
| `errors` | `list[tuple[str, str, str]]` | APPLICABLE | NDJSON error events. Each task's errors should be tagged with `task_id` (first tuple element). | KEEP AS-IS: already has `task_id` slot in tuple |
| `last_assistant_text` | `str` | APPLICABLE | Last 80 chars from current task's NDJSON stream. Naturally resets per task. | KEEP AS-IS |
| `total_tasks_in_phase` | `int` | APPLICABLE | Path A already has `len(tasks)` at `executor.py:956`. Trivial to populate. | KEEP AS-IS: Path A can populate directly |
| `completed_task_estimate` | `int` | APPLICABLE and MORE ACCURATE | Path A knows exactly which tasks completed (not an estimate). Could use actual count instead of heuristic. | EXTEND: use `completed_task_count` (exact) on Path A, estimate on Path B |
| `tokens_in` | `int` | BLOCKED: no extraction mechanism | NDJSON `stream-json` events include `usage` blocks with `input_tokens`. `OutputMonitor._parse_event()` would need to extract these. Currently not implemented. | ADD NEW: implement token extraction in `OutputMonitor._parse_event()`, call per-task |
| `tokens_out` | `int` | BLOCKED: no extraction mechanism | Same as `tokens_in` but for `output_tokens`. | ADD NEW: same as tokens_in |

**Architectural note on per-task monitoring**: Path A currently creates one `OutputMonitor` per phase (if TUI is enabled). Since all tasks write to the same output file (`config.output_file(phase)`), and each task subprocess overwrites the file, the monitor would see discontinuities. Two approaches:

- **Option A (simpler)**: After each task subprocess completes, call `count_turns_from_output()` and a new `extract_token_usage()` on the output file, then reset the monitor. No concurrent monitoring.
- **Option B (richer)**: Give each task its own output file (`config.task_output_file(phase, task)`), run `OutputMonitor` per-task for live TUI updates. More invasive but enables real-time per-task telemetry.

**Recommendation**: Option A for v3.7 (minimal change, fixes the data flow), Option B deferred to v3.8.

### 7.2 PhaseResult -- New Fields

| Field | Type | Can Path A Populate? | How? | Recommendation |
|-------|------|---------------------|------|----------------|
| `turns` | `int` | NO (Bug 1) -> YES after fix | Sum `TaskResult.turns_consumed` across all tasks in phase. Requires Bug 1 fix. | EXTEND: `turns = sum(tr.turns_consumed for tr in task_results)` at phase aggregation |
| `tokens_in` | `int` | NO (no extraction) -> YES after new code | Sum per-task `tokens_in` extracted from NDJSON. Requires new `extract_token_usage()` function. | ADD NEW: per-task token extraction, aggregate to phase |
| `tokens_out` | `int` | NO (no extraction) -> YES after new code | Same as `tokens_in`. | ADD NEW: same |

**Key insight**: These fields should not be populated directly on `PhaseResult` for Path A. They should be **derived from `TaskResult` aggregation**. The spec assumes a single-subprocess model where `MonitorState` values are copied to `PhaseResult`. For Path A, the flow must be:

```
Per-task NDJSON -> TaskResult.turns_consumed (fix Bug 1)
                -> TaskResult.tokens_in (new field)
                -> TaskResult.tokens_out (new field)
                -> aggregate to PhaseResult at phase completion
```

This means `TaskResult` needs two new fields: `tokens_in: int = 0` and `tokens_out: int = 0`.

### 7.3 SprintResult -- Aggregate Properties

| Property | Works with zeroed data? | After bug fixes? | Recommendation |
|----------|------------------------|------------------|----------------|
| `total_turns` | Returns 0 (sum of zeros) | Correct | KEEP AS-IS (fix upstream) |
| `total_tokens_in` | Returns 0 (fields don't exist yet) | Correct | KEEP AS-IS (fix upstream) |
| `total_tokens_out` | Returns 0 (fields don't exist yet) | Correct | KEEP AS-IS (fix upstream) |
| `total_output_bytes` | WORKS (output_bytes is already populated) | Same | KEEP AS-IS |
| `total_files_changed` | WORKS (files_changed already populated) | Same | KEEP AS-IS |

The aggregate properties are pure computations on `PhaseResult` fields. They are correctly designed. The problem is entirely upstream: `PhaseResult` fields are zero because `TaskResult` fields are zero because of Bugs 1-3.

### 7.4 SprintConfig -- New Fields

| Field | Path A Applicability | Recommendation |
|-------|---------------------|----------------|
| `total_tasks` | FULLY APPLICABLE. Path A has exact task counts from parsing. Can be populated at sprint start by scanning all phase files. | KEEP AS-IS |
| `checkpoint_gate_mode` | APPLICABLE to both paths. Checkpoint gates operate at phase level, not task level. | KEEP AS-IS |

### 7.5 PhaseStatus -- New Value

`PASS_MISSING_CHECKPOINT` is a phase-level status set by the checkpoint gate after phase completion. It operates identically for both paths since checkpoint verification happens post-phase, not post-task.

**Recommendation**: KEEP AS-IS. No Path A-specific concerns.

### 7.6 New Dataclasses

| Dataclass | Path A Applicability | Recommendation |
|-----------|---------------------|----------------|
| `CheckpointEntry` | APPLICABLE. Checkpoint verification is path-agnostic (checks files on disk post-phase). | KEEP AS-IS |
| `PhaseSummary` | APPLICABLE but richer on Path A. Path A has per-task `TaskResult` objects that could populate `tasks: list[dict]` with actual per-task outcomes instead of heuristic extraction from output text. | EXTEND: populate `tasks` from `TaskResult` list on Path A |
| `ReleaseRetrospective` | APPLICABLE. Operates on `SprintResult` which aggregates from `PhaseResult`. Will produce accurate data once upstream bugs are fixed. | KEEP AS-IS |

### 7.7 SprintTUI -- New Field

`latest_summary_notification` is a UI-level field for `--no-tmux` mode. Path-agnostic.

**Recommendation**: KEEP AS-IS.


## Proposed New Tasks: TurnLedger Bug Fixes

These three bugs must be fixed **before** the Section 7 data model changes can deliver value on Path A. They are prerequisites, not optional enhancements.

### NEW TASK: Fix `turns_consumed` return value (Bug 1)

**Location**: `executor.py:1091-1092`

**Current code**:
```python
# Turn counting is wired separately in T02.06
return (exit_code if exit_code is not None else -1, 0, output_bytes)
```

**Root cause**: The function `count_turns_from_output()` exists at `monitor.py:114-141` and correctly counts `"type":"assistant"` lines in NDJSON output. It is never called. The comment references `T02.06` which does not exist in any release spec.

**Concrete fix**:
```python
from superclaude.cli.sprint.monitor import count_turns_from_output

output_path = config.output_file(phase)
output_bytes = output_path.stat().st_size if output_path.exists() else 0
turns_consumed = count_turns_from_output(output_path)
return (exit_code if exit_code is not None else -1, turns_consumed, output_bytes)
```

**Impact**: Unblocks `TaskResult.turns_consumed`, `PhaseResult.turns`, `SprintResult.total_turns`, TurnLedger reimbursement math, and budget exhaustion signals.

**LOC**: ~3 lines changed in `executor.py`

**Risk**: LOW. `count_turns_from_output()` is already tested and handles missing/empty files gracefully (returns 0).

### NEW TASK: Wire `TaskResult.output_path` (Bug 2)

**Location**: `executor.py:1017-1025`

**Current code**:
```python
result = TaskResult(
    task=task,
    status=status,
    turns_consumed=turns_consumed,
    exit_code=exit_code,
    started_at=started_at,
    finished_at=finished_at,
    output_bytes=output_bytes,
)
```

**Root cause**: `output_path` is known at this point -- it is `config.output_file(phase)` (same value computed at `executor.py:1089`). It is simply not passed to the `TaskResult` constructor.

**Concrete fix**:
```python
result = TaskResult(
    task=task,
    status=status,
    turns_consumed=turns_consumed,
    exit_code=exit_code,
    started_at=started_at,
    finished_at=finished_at,
    output_bytes=output_bytes,
    output_path=str(config.output_file(phase)),
)
```

**Impact**: Unblocks anti-instinct gate evaluation at `executor.py:826-831`. The gate will now find the output file, read it, and perform semantic checks (undischarged obligations, uncovered contracts, fingerprint coverage).

**LOC**: 1 line added to constructor call

**Risk**: LOW. The `output_path` field already exists on `TaskResult` (models.py:176) with type `str` and default `""`. The anti-instinct gate already handles the field correctly when populated.

**Caveat**: All tasks in a phase currently write to the same output file (`config.output_file(phase)`). The anti-instinct gate evaluating task N's output will actually read task N's output (correct, since the file is overwritten per-task). However, if future work introduces per-task output files, this path will need updating.

### NEW TASK: Change `gate_rollout_mode` default from `"off"` to `"shadow"` (Bug 3)

**Location**: `models.py:329`

**Current code**:
```python
gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"
```

**Root cause**: The default `"off"` means anti-instinct gates never evaluate unless the operator explicitly passes `--shadow-gates` or `--gate-rollout-mode`. Since this is an opt-in flag that most operators do not know about, the gate system is effectively dead.

**Concrete fix**:
```python
gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "shadow"
```

**Migration strategy**:
1. Change default to `"shadow"` (evaluate + record metrics, no behavioral impact)
2. This is safe because shadow mode has zero impact on sprint behavior -- it only records metrics via `ShadowGateMetrics`
3. Operators who explicitly set `--gate-rollout-mode off` are unaffected (explicit overrides default)
4. After one release cycle of shadow data collection, promote default to `"soft"` (same progression as `checkpoint_gate_mode` in Section 9.2)

**Impact**: Activates the anti-instinct evaluation pipeline for all sprints. Combined with Bug 2 fix, gates will actually read output files and evaluate semantic quality. Combined with Bug 1 fix, reimbursement credits will flow for passing tasks.

**LOC**: 1 line changed in `models.py`

**Risk**: LOW for shadow mode (metrics-only, no behavioral change). MEDIUM if jumping directly to `"soft"` (would introduce credit/remediation behavior that operators have never seen).

**Dependency**: This fix is most valuable when Bugs 1 and 2 are also fixed. Without Bug 2, the gate vacuously passes (no output to evaluate). Without Bug 1, reimbursement credits are zero even on PASS.


## Additional Proposed Field: TaskResult Token Tracking

The spec adds `tokens_in` and `tokens_out` to `PhaseResult` and `MonitorState`, but there is no per-task equivalent on `TaskResult`. For Path A, where each task is a separate subprocess, token consumption is naturally per-task.

**Proposed addition to `TaskResult`**:
```python
@dataclass
class TaskResult:
    # ... existing fields ...
    tokens_in: int = 0
    tokens_out: int = 0
```

**Proposed extraction function** (new, in `monitor.py`):
```python
def extract_token_usage(output_path: Path) -> tuple[int, int]:
    """Extract cumulative token usage from subprocess NDJSON output.

    Parses "usage" blocks in stream-json events to sum input_tokens
    and output_tokens across all events.

    Returns:
        (tokens_in, tokens_out) tuple. Returns (0, 0) if file missing or unparseable.
    """
```

This function would parse the same NDJSON output that `count_turns_from_output()` already reads, extracting `input_tokens` and `output_tokens` from usage events.

**Integration point**: Called in `_run_task_subprocess()` after `proc.wait()`, alongside the Bug 1 fix for `count_turns_from_output()`.


## Net Changes to Spec

### Fields to ADD to spec (not currently in Section 7):

| Model | Field | Type | Default | Rationale |
|-------|-------|------|---------|-----------|
| `TaskResult` | `tokens_in` | `int` | `0` | Per-task input token tracking for Path A aggregation |
| `TaskResult` | `tokens_out` | `int` | `0` | Per-task output token tracking for Path A aggregation |

### Bug fix tasks to ADD to spec (new implementation tasks):

| Task ID | Title | LOC | Priority |
|---------|-------|-----|----------|
| NEW-DM-01 | Wire `count_turns_from_output()` into `_run_task_subprocess()` | ~3 | P0 (prerequisite for turns/tokens) |
| NEW-DM-02 | Set `TaskResult.output_path` in constructor | ~1 | P0 (prerequisite for gate evaluation) |
| NEW-DM-03 | Change `gate_rollout_mode` default to `"shadow"` | ~1 | P1 (activates gate pipeline) |
| NEW-DM-04 | Implement `extract_token_usage()` in `monitor.py` | ~25 | P1 (prerequisite for tokens_in/out) |
| NEW-DM-05 | Add `tokens_in`/`tokens_out` to `TaskResult` and wire extraction | ~5 | P1 (enables Section 7.2 on Path A) |
| NEW-DM-06 | Add Path A aggregation logic: `TaskResult` list -> `PhaseResult` fields | ~10 | P1 (connects per-task data to phase-level) |

### Fields to KEEP AS-IS in spec:

- All `MonitorState` fields (7.1) -- well-designed, just need upstream data
- All `SprintResult` aggregate properties (7.3) -- pure computation, correct
- `SprintConfig.total_tasks` and `checkpoint_gate_mode` (7.4) -- path-agnostic
- `PhaseStatus.PASS_MISSING_CHECKPOINT` (7.5) -- phase-level, path-agnostic
- All new dataclasses (7.6) -- `CheckpointEntry` and `ReleaseRetrospective` are path-agnostic; `PhaseSummary` benefits from Path A data but works without it
- `SprintTUI.latest_summary_notification` (7.7) -- UI-level, path-agnostic

### Fields to EXTEND in spec (add Path A awareness):

- `PhaseResult.turns` (7.2): document that Path A populates via `sum(TaskResult.turns_consumed)`, not from `MonitorState.turns`
- `PhaseResult.tokens_in` (7.2): document that Path A populates via `sum(TaskResult.tokens_in)`, not from `MonitorState.tokens_in`
- `PhaseResult.tokens_out` (7.2): same pattern as `tokens_in`
- `MonitorState.completed_task_estimate` (7.1): on Path A, this is an exact count, not an estimate

### Dependency ordering for implementation:

```
NEW-DM-01 (fix turns)  ──┐
NEW-DM-02 (fix output_path) ──┤──> NEW-DM-03 (default shadow) ──> Section 7 data model changes
NEW-DM-04 (token extraction)──┤
NEW-DM-05 (TaskResult tokens)─┘
                               └──> NEW-DM-06 (aggregation logic)
```

Bug fixes DM-01, DM-02, DM-04, DM-05 are independent and can be implemented in parallel. DM-03 depends on DM-01 + DM-02 to be meaningful. DM-06 depends on all prior tasks. Section 7 data model changes can proceed in parallel but will produce zeros until the bug fixes land.
