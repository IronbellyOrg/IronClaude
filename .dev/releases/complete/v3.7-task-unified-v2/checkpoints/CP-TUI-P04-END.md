# Checkpoint: End of Sprint TUI v2 Wave 4 — Tmux Integration

**Checkpoint ID:** CP-TUI-P04-END
**Release:** v3.7-task-unified-v2
**Phase:** TUI v2 Wave 4 (ClickUp Phase 8)
**Status:** PASS
**Timestamp (UTC):** 2026-04-22

## Scope

Final wave of Sprint TUI v2. Converts the 2-pane tmux layout into a
3-pane layout so the per-phase summary (F8 from Wave 3) has a
dedicated display slot, and provides a `--no-tmux` fallback so
operators without tmux still see every summary. Wires the
`SummaryWorker.on_summary_ready` callback (new in this wave) through
to the correct UI surface.

Work items:

- **`tmux.py`** — complete rewrite of the panel-splitting flow:
  - New canonical constants `TUI_PANE = "0.0"`, `SUMMARY_PANE = "0.1"`,
    `TAIL_PANE = "0.2"`.
  - `launch_in_tmux` now splits twice: :0.0 → :0.1 at 50%, then
    :0.1 → :0.2 at 50%, giving 50% / 25% / 25%.
  - The summary pane hosts an idle `bash --noprofile --norc` prompt
    with a placeholder line so it is ready to receive `send-keys`.
  - `update_tail_pane` migrated from `:0.1` to `:0.2`.
  - New `update_summary_pane(session, summary_file)` sends
    `clear && cat <path>\n` to `:0.1`; no-op when the file does not
    exist.
- **`summarizer.py`**:
  - `PhaseSummary.path: Optional[Path]` field populated by
    `PhaseSummarizer.write` so downstream fanout never has to rebuild
    the path.
  - `SummaryWorker` accepts an `on_summary_ready` callback fired from
    inside the worker thread **after** the summary commits to
    `_summaries` (callback is exception-isolated).
- **`tui.py`**:
  - `SprintTUI.latest_summary_notification: str | None = None` new
    field. Rendered as a dim `Summary: …` line beneath the phase
    table whenever set. Hidden when `None` so the tmux-mode render is
    untouched.
- **`executor.py`**:
  - Imports `update_summary_pane` from `tmux`.
  - Inlines a `_summary_fanout` closure that routes each completed
    summary to either `update_summary_pane(session, summary.path)`
    (tmux mode) or `tui.latest_summary_notification = "Phase N summary
    ready: …"` (`--no-tmux` mode).
  - `SummaryWorker` is constructed with this callback.

## Files Modified

| File | Action | Summary |
|------|--------|---------|
| `src/superclaude/cli/sprint/tmux.py` | MODIFY | 3-pane layout, pane constants, `update_summary_pane`, `:0.1 → :0.2` tail migration |
| `src/superclaude/cli/sprint/summarizer.py` | MODIFY | `PhaseSummary.path` field; `SummaryWorker.on_summary_ready` callback (exception-isolated) |
| `src/superclaude/cli/sprint/tui.py` | MODIFY | `SprintTUI.latest_summary_notification` field + render line |
| `src/superclaude/cli/sprint/executor.py` | MODIFY | `update_summary_pane` import; `_summary_fanout` closure routes to tmux pane or TUI notification |
| `tests/sprint/test_tmux.py` | CREATE | 11 tests — session helpers, 3-pane layout creation, split-failure cleanup, `:0.2` tail target, `update_summary_pane` send-keys, pane-constant regression guard |
| `tests/sprint/test_summarizer.py` | MODIFY | +4 callback tests (fires once, exception isolation, not called on summarize failure, `summary.path` stamping) |
| `tests/sprint/test_tui_v2_wave2.py` | MODIFY | +2 notification tests (default none, renders when set) |

## Verification

### Spec Section 4.2 Wave 4 — acceptance criteria

| Acceptance criterion | Result |
|---|---|
| `tmux.py` creates 3 panes: TUI 50%, summary 25%, tail 25% | PASS (`TestThreePaneLayout::test_launch_creates_three_panes`) |
| All hardcoded `:0.1` tail-pane references updated to `:0.2` | PASS (only `update_tail_pane` was updated; `TestUpdateTailPane::test_targets_pane_zero_two` verifies) |
| `update_tail_pane` and similar write to the correct pane after migration | PASS |
| Summary pane shows waiting message on sprint start | PASS (placeholder printed in pane's bash command) |
| Summary pane updates via `tmux send-keys` + `cat` when a new `results/phase-N-summary.md` appears | PASS (`update_summary_pane` + `SummaryWorker.on_summary_ready` callback) |
| `--no-tmux` mode: TUI shows `Phase N summary ready: results/phase-N-summary.md` notification line | PASS (`SprintTUI.latest_summary_notification`, rendered under phase table; `TestLatestSummaryNotification` verifies) |
| `SprintTUI.latest_summary_notification` field added and wired | PASS |
| `tests/sprint/test_tmux.py` passes for layout, summary updates, pane-index handling | PASS (11/11) |
| Pane-constant regression guard (`TUI_PANE == "0.0"` etc.) | PASS |

### Regression Status

| Suite | Before Wave 4 | After Wave 4 |
|-------|---------------|--------------|
| Full `tests/sprint/` | 904 passed, 57 failed | 921 passed, 57 failed |
| New tests added | — | +17 (11 tmux + 4 callback + 2 notification) |
| Regressions introduced | — | 0 |

Lint on authored files is clean after `ruff --fix` reordered imports in
two files. Remaining ruff findings are pre-existing in `models.py`.

## Cross-wave dependencies satisfied

- **Wave 3 summary output** — `SummaryWorker.on_summary_ready`
  callback now fires with a PhaseSummary whose `path` attribute always
  points to the freshly-written markdown file. The callback is
  exception-isolated so a broken tmux session cannot bring down a
  sprint.
- **Wave 2 terminal panels** — still render without modification. The
  `latest_summary_notification` line is optional and appears beneath
  the phase table, so it does not collide with the success/halt
  terminal panels.
- **`PASS_MISSING_CHECKPOINT`** — still renders via the pre-existing
  `STATUS_STYLES`/`STATUS_ICONS` entries.

## Open items

- **`--no-tmux` flag wiring** — the spec-mentioned `--no-tmux` CLI flag
  is not touched here; the current behaviour is that `config.tmux_session_name`
  is either set (tmux mode) or empty (non-tmux mode), and the
  `_summary_fanout` closure branches accordingly. Adding an explicit
  `--no-tmux` flag surface remains a Naming Consolidation / CLI
  concern, not a Wave 4 concern.
- **Naming Consolidation** — still pending per §6.2; expected to land
  before `make release` because it renames the command surface that
  `process.py` invokes (`/sc:task-unified` → `/sc:task`).

## Next steps

All four TUI v2 waves have landed:

| Wave | Commit | Theme |
|------|--------|-------|
| 1 | `430a1c9` | Data model + monitor extraction |
| 2 | `3e293c4` | Rendering refactor |
| 3 | `5115dfa` | Summary + retrospective infrastructure |
| 4 | (this commit) | Tmux integration + --no-tmux fallback |

The remaining v3.7-task-unified-v2 work items are:

- Naming Consolidation (§4.3 / §6.2, Tier 1-3 renames).
- Checkpoint Wave 4 (tasklist normalisation) already shipped
  (`8eba113`, `CP-CE-P04-END.md`) per `clickup-tasks.md` Phase 9 which
  was intended to be deferred — confirm with release manager whether
  that shipment should be reverted.

**Source**: `v3.7-UNIFIED-RELEASE-SPEC-merged.md` §4.2 Wave 4, §7.7
(`SprintTUI.latest_summary_notification`); `clickup-tasks.md` Phase 8.
