# Checkpoint: End of Sprint TUI v2 Wave 2 — Rendering

**Checkpoint ID:** CP-TUI-P02-END
**Release:** v3.7-task-unified-v2
**Phase:** TUI v2 Wave 2 (ClickUp Phase 4)
**Status:** PASS
**Timestamp (UTC):** 2026-04-22

## Scope

Visible TUI refactor. Consumes the data model + monitor extraction
laid down in Wave 1 (`CP-TUI-P01-END`) and rewrites `tui.py` to expose
every v3.7 display feature (F1/F2/F3/F4/F5/F6/F7) while preserving the
`PASS_MISSING_CHECKPOINT` / gate-column cross-domain invariants from
Section 5.1 of the merged spec.

Work items:

- **F7** — Outer panel title now reads
  `SUPERCLAUDE SPRINT RUNNER == {release_name}` derived from
  `SprintConfig.release_dir` with an index-parent fallback.
- **F2** — Phase table drops `Tasks` (moved to the progress bar) and
  adds `Turns` and `Output` columns. The gate column (TUI-Q9) still
  renders only when `grace_period > 0`.
- **F3** — Custom dual progress bar using block characters (`█`/`░`)
  on a single `Text` line, sourced from `SprintResult.phase_results`
  for the phases segment and `MonitorState.completed_task_estimate`
  plus completed-phase re-scans for the tasks segment.
- **F5** — Active panel surfaces a `Prompt:` line (per-phase static,
  from the new `Phase.prompt_preview` field) and an `Agent:` line
  (live, from `MonitorState.last_assistant_text`).
- **F1** — 3-line activity stream at the bottom of the active panel
  (`HH:MM:SS  ToolName  description`). Padding keeps the panel height
  stable; `[thinking... Ns]` replaces the last line when idle > 2 s.
- **F4** — Conditional error panel returns `None` when
  `MonitorState.errors` is empty; otherwise renders up to 5 rows with a
  `+N more` overflow marker and a red border.
- **F6** — Enhanced terminal panels:
  - Success variant — Result, Duration, Turns (total + avg/phase),
    Tokens (in/out with K/M suffixes), Output, Files, Log.
  - Halt variant — adds Completed (phases + tasks), folded errors
    (up to 5 + overflow), Last task, Resume command.

TUI-Q1 resolved: the prompt preview lives on `Phase.prompt_preview`
(populated in `load_sprint_config`) rather than on `SprintConfig`,
because the preview is materially different per phase.

Ancillary Wave 1 polish landed here (kept scoped with a follow-up
timestamp fix rather than a separate commit):

- `OutputMonitor._append_activity` now stores `time.time()` wall-clock
  timestamps so the TUI can render `HH:MM:SS` directly.
- `OutputMonitor._extract_signals_from_text` parses the two-digit
  ordinal from `last_task_id` into `MonitorState.completed_task_estimate`
  to feed the F3 progress bar.

## Files Modified

| File | Change |
|------|--------|
| `src/superclaude/cli/sprint/tui.py` | Full Wave 2 rewrite: release-name title, new phase columns, dual block-bar progress, Prompt/Agent lines, activity stream, conditional error panel, enhanced success/halt terminal panels, `_format_tokens` / `_format_bytes` / `_render_bar` / `_render_percent` / `_format_timestamp` / `_truncate` helpers |
| `src/superclaude/cli/sprint/models.py` | `Phase.prompt_preview: str = ""` + `Phase.prompt_display` property (TUI-Q1) |
| `src/superclaude/cli/sprint/config.py` | `_PHASE_INTENT_RE` pattern + `_extract_phase_prompt_preview` helper; `load_sprint_config` populates `phase.prompt_preview` |
| `src/superclaude/cli/sprint/monitor.py` | `_append_activity` wall-clock timestamps; `_extract_signals_from_text` parses task ordinal into `completed_task_estimate` |
| `tests/sprint/test_tui_gate_column.py` | Updated column-count assertions to Wave 2 layout (6 columns / 7 with gate); asserts header ordering |
| `tests/sprint/test_tui_v2_wave2.py` | +32 new tests covering helpers, title, phase table, dual progress, Prompt/Agent/activity, error panel, success/halt panels, `PASS_MISSING_CHECKPOINT` render |

## Verification

### Spec Section 4.2 Wave 2 — Acceptance criteria

| Acceptance criterion | Result |
|---|---|
| Phase table renders new `Turns` and `Output` columns; `Tasks` removed | PASS (`TestPhaseTableColumns::test_default_columns`) |
| `_show_gate_column` still works alongside new columns | PASS (`TestTUIGateColumnBackwardCompat` updated) |
| Dual progress bar renders with block characters | PASS (`TestDualProgressBar`) |
| Active panel shows `Prompt:` (static) and `Agent:` (live) lines | PASS (`TestActivePanelContextAndActivity::test_prompt_preview_rendered`, `test_agent_line_shows_last_assistant_text`) |
| Activity stream shows last 3 tool calls with shortened names | PASS (`test_activity_stream_renders_entries`) |
| `[thinking... Ns]` indicator after >2s idle | PASS (`test_thinking_indicator_when_idle`) |
| Error panel hidden when `len(errors) == 0` | PASS (`TestErrorPanel::test_hidden_when_no_errors`) |
| Error panel renders with red border + overflow count when non-empty | PASS (`test_rendered_when_errors_present`, `test_overflow_marker_when_more_than_five`) |
| Success terminal panel shows all F6 fields with K/M token formatting | PASS (`TestSuccessTerminalPanel::test_renders_aggregates`) |
| Halt terminal panel shows Completed, Last task, Errors, Resume | PASS (`TestHaltTerminalPanel::test_renders_halt_with_resume_and_errors`) |
| Outer panel title includes `{release_name}` | PASS (`TestOuterPanelTitle::test_title_includes_release_name`, `_falls_back_to_index_parent`) |
| `STATUS_STYLES`/`STATUS_ICONS` include `PASS_MISSING_CHECKPOINT` | PASS (present since Wave 2 of Checkpoint Enforcement; re-verified by `TestPassMissingCheckpointRender`) |
| `prompt_preview` storage location decided and documented | PASS — `Phase.prompt_preview` (TUI-Q1) |
| Existing TUI tests pass | PASS — 8/8 `test_tui_gate_column.py`, Wave 1 fully green |

### Regression Status

| Suite | Before Wave 2 | After Wave 2 |
|-------|---------------|--------------|
| Full `tests/sprint/` | 835 passed, 57 failed | 867 passed, 57 failed |
| New tests added | — | +32 passing |
| Regressions introduced | — | 0 |

The 57 pre-existing failures (`AttributeError: '_PassPopen' object has no attribute 'stdin'` and kin) are rooted in sprint-level mock `Popen` classes, orthogonal to this wave, and unchanged.

Lint on the authored code paths (`tui.py`, `config.py` new additions,
`monitor.py` deltas, `tests/sprint/test_tui_v2_wave2.py`) is clean.

## Open questions resolved

- **TUI-Q1** — Prompt storage: lives on `Phase.prompt_preview` (not on
  `SprintConfig`) because it varies per phase. Populated by
  `_extract_phase_prompt_preview` in `load_sprint_config` from the first
  `**Goal:**` / `**Scope:**` / `**Purpose:**` / `**Intent:**` /
  `**Objective:**` line, else the first body paragraph after the H1,
  else `phase.display_name`. Always truncated to 60 chars.

## Cross-wave dependencies

- **Checkpoint Wave 2 (`PASS_MISSING_CHECKPOINT`)** — already shipped;
  `STATUS_STYLES` / `STATUS_ICONS` entries pre-existing. Verified the
  gate-downgrade path still renders via
  `TestPassMissingCheckpointRender`.
- **TUI v2 Wave 3 (Summary Infrastructure)** — unblocked. Terminal
  panel renderers now consume `SprintResult` aggregates
  (`total_turns`, `total_tokens_in/out`, `total_output_bytes`,
  `total_files_changed`); Wave 3 will reuse these via
  `PhaseSummarizer` / `RetrospectiveGenerator`.
- **TUI v2 Wave 4 (Tmux)** — unblocked for layout; Wave 4 only
  migrates pane indices (`:0.1` → `:0.2`) and adds the summary pane.

## Next steps

- TUI v2 Wave 3: new `summarizer.py` + `retrospective.py` modules,
  SummaryWorker thread pool with `threading.Lock`, Haiku subprocess
  invocation per Section 6.3.
- Naming consolidation remains pending; the Section 6.2 recommended
  order places it before Wave 3 to reduce diff noise.

**Source**: `v3.7-UNIFIED-RELEASE-SPEC-merged.md` §4.2 Wave 2, §5.1,
§6.5; `clickup-tasks.md` Phase 4.
