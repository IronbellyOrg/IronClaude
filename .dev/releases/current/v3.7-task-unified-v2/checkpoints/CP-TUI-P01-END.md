# Checkpoint: End of Sprint TUI v2 Wave 1 — Data Model + Monitor Extraction

**Checkpoint ID:** CP-TUI-P01-END
**Release:** v3.7-task-unified-v2
**Phase:** TUI v2 Wave 1 (ClickUp Phase 3)
**Status:** PASS
**Timestamp (UTC):** 2026-04-22

## Scope

Foundation wave for all Sprint TUI v2 features. Extends data models and
stream-json extraction so subsequent TUI waves (rendering, summary,
tmux) have structured telemetry to render.

Five work items:

- **Model fields** — `MonitorState` gains 8 TUI v2 fields; `PhaseResult`
  gains 3; `SprintResult` gains 5 aggregate properties; `SprintConfig`
  gains `total_tasks` with an active-phase pre-scan in
  `load_sprint_config`.
- **Monitor extraction** — `_extract_signals_from_event` now reads the
  real `claude --print --output-format stream-json` event shape:
  `type: assistant` drives F2 turns / F6 tokens / F5 agent text / F1
  activity log (tool_use content blocks), and `type: user` drives F4
  errors (is_error flag + Bash exit_code fallback).
- **Interface** — `OutputMonitor.reset()` accepts an optional
  `phase_file` so the dual progress bar denominator (F3) is populated
  without re-scanning per poll tick (TUI-Q4 resolved).
- **Executor wiring** — `executor.py` passes `phase.file` into
  `monitor.reset()` and pipes `monitor.state.turns/tokens_in/tokens_out`
  into `PhaseResult`.
- **Tests** — 47 new passing tests covering every new field, every
  extraction path, ring-buffer caps, tool-name shortening, Bash error
  detection, and the `count_tasks_in_file` / `SprintConfig.total_tasks`
  pre-scan.

## Files Modified

| File | Change |
|------|--------|
| `src/superclaude/cli/sprint/models.py` | +8 `MonitorState` fields, +3 `PhaseResult` fields, +5 `SprintResult` properties, +1 `SprintConfig` field |
| `src/superclaude/cli/sprint/config.py` | `_TASK_ID_HEADING_RE`, `count_tasks_in_file`, `total_tasks` pre-scan in `load_sprint_config` |
| `src/superclaude/cli/sprint/monitor.py` | `ACTIVITY_LOG_MAX`/`ERRORS_MAX`/`ASSISTANT_TEXT_MAX_LEN` constants, `TOOL_NAME_SHORTENING`, `_shorten_tool_name`, `_condense_tool_input`, `_flatten_tool_result_content`, `_has_nonzero_exit_code`, `_handle_assistant_event`, `_handle_user_event`, `_append_activity`, `_append_error`, extended `reset(phase_file=...)` |
| `src/superclaude/cli/sprint/executor.py` | `monitor.reset(output_path, phase_file=phase.file)`; `PhaseResult` now captures `turns`/`tokens_in`/`tokens_out` |
| `tests/sprint/test_models.py` | +8 tests (PhaseResult Wave 1 defaults + round-trip, SprintResult aggregates, MonitorState Wave 1 defaults + shared-list isolation) |
| `tests/sprint/test_tui_v2_wave1.py` | +39 tests (helpers, Monitor.reset, turn/token extraction, assistant text, activity log, error extraction, count_tasks_in_file, load_sprint_config total_tasks) |

## Verification

### Spec Section 7 — Data Model Changes

| Spec requirement | Result |
|---|---|
| `MonitorState.activity_log: list[tuple[float, str, str]]` default `[]` | PASS (`models.py`, `test_tui_v2_wave1_defaults`) |
| `MonitorState.turns: int = 0` | PASS |
| `MonitorState.errors: list[tuple[str, str, str]]` default `[]` | PASS |
| `MonitorState.last_assistant_text: str = ""` | PASS |
| `MonitorState.total_tasks_in_phase: int = 0` | PASS |
| `MonitorState.completed_task_estimate: int = 0` | PASS |
| `MonitorState.tokens_in / tokens_out: int = 0` | PASS |
| `PhaseResult.turns / tokens_in / tokens_out: int = 0` | PASS (`test_tui_v2_wave1_defaults`, `test_tui_v2_wave1_populated`) |
| `SprintResult.total_turns / total_tokens_in / total_tokens_out / total_output_bytes / total_files_changed` | PASS (4 aggregate tests) |
| `SprintConfig.total_tasks: int = 0` | PASS (populated by `load_sprint_config`) |

### Spec Section 4.2 Wave 1 — Monitor Extraction

| Feature | Result |
|---|---|
| F2 turn counting (assistant message events) | PASS — 5 tests |
| F5 last_assistant_text, tail truncation to 80 chars | PASS — 4 tests |
| F4 error detection (`is_error: true`) | PASS |
| F4 Bash `exit_code != 0` fallback | PASS |
| F4 error ring buffer capped at 10 | PASS |
| F1 activity log from tool_use content blocks | PASS |
| F1 tool name shortening (`TodoWrite`→`Todo`, `MultiEdit`→`Multi`, etc.) | PASS |
| F1 activity ring buffer capped at 3 | PASS |
| F6 input/output token accumulation | PASS |

### TUI-Q4 — Monitor.reset() interface

`Monitor.reset(output_path, phase_file=None)` accepts an optional phase
file path and pre-counts `### T<PP>.<TT>` headings into
`state.total_tasks_in_phase` so the F3 dual progress bar has a stable
denominator. Verified by 4 tests in `TestMonitorResetWithPhaseFile`.

### TUI-Q10 — Pre-scan location

Pre-scan lives in `superclaude.cli.sprint.config`. `count_tasks_in_file`
is a thin helper reused by both `load_sprint_config`
(populating `SprintConfig.total_tasks` across active phases) and
`OutputMonitor.reset` (per-phase count). `config.py` was already in the
modified-files set for this release, so no new module boundary was
introduced.

## Regression Status

| Suite | Before (HEAD) | After (this wave) |
|-------|---------------|-------------------|
| Full `tests/sprint/` | 788 passed, 57 failed | 835 passed, 57 failed |
| New tests added | — | +47 passing |
| Regressions introduced | — | 0 |

The 57 pre-existing failures (`AttributeError: '_PassPopen' object has
no attribute 'stdin'` and similar) are rooted in mock `Popen` classes
in sprint tests; they are orthogonal to this wave and unchanged.

Lint on the authored code paths (`monitor.py`, `config.py`, `models.py`
new sections, `test_tui_v2_wave1.py`) is clean. Remaining ruff findings
in `models.py` are pre-existing (`F401 StepStatus`, `N806 _OLD_TO_NEW`,
`F541` on redundant f-strings).

## Cross-Wave Dependencies

- **Checkpoint Wave 2** (`PASS_MISSING_CHECKPOINT`) — already shipped.
  The enum value exists in `PhaseStatus`; TUI v2 Wave 2 will add
  `STATUS_STYLES` / `STATUS_ICONS` entries before TUI rendering
  features go live (Section 5.1).
- **TUI v2 Wave 2** (Rendering) — unblocked by this wave. All data
  required by F1/F2/F3/F4/F5/F6 terminal panels is now populated.
- **TUI v2 Wave 3** (Summary Infrastructure) — unblocked. `PhaseResult`
  carries the per-phase totals `PhaseSummarizer` needs; `SprintResult`
  exposes the cross-phase aggregates `RetrospectiveGenerator` needs.

## Next Steps

- TUI v2 Wave 2: rewrite `tui.py` for the new layout (F1/F2/F3/F4/F5/F6/F7),
  including the `PASS_MISSING_CHECKPOINT` status stub in
  `STATUS_STYLES`/`STATUS_ICONS`.
- TUI v2 Wave 3: create `summarizer.py` and `retrospective.py`, wire
  `SummaryWorker` after `_verify_checkpoints()` per Section 6.4.
- Naming Consolidation: still pending; order per Section 6.2 suggests
  it lands before TUI Wave 2 to reduce diff noise.

**Source**: `v3.7-UNIFIED-RELEASE-SPEC-merged.md` §4.2 Wave 1, §7, §5.1;
`clickup-tasks.md` Phase 3.
