# Sprint TUI — Current State Analysis & 10 Improvement Proposals

Scope: investigate the three reported symptoms — frozen progress bars, no real-time indicators, and prompt cut-off in wider terminals — diagnose root causes with file:line evidence, and propose ten concrete remediations.

Branch under analysis: `feat/workspace-rca-remediation` (HEAD `f79b1bd`).

---

## 1. TUI code surface

| Concern | File | Key entry points |
|---|---|---|
| Rich-based renderer | `src/superclaude/cli/sprint/tui.py` (623 lines) | `SprintTUI.start/stop/update/_render`, `_build_phase_table`, `_build_progress`, `_build_active_panel`, `_build_error_panel`, `_build_terminal_panel`, module helpers `_render_bar`/`_render_percent`/`_truncate` |
| Sprint orchestrator + poll loops | `src/superclaude/cli/sprint/executor.py` (2057 lines) | `execute_sprint` (line 1113), `execute_phase_tasks` (line ~860–1051), `_run_task_subprocess` (line 1054), inner poll loop (lines 1298–1382) |
| NDJSON output → MonitorState | `src/superclaude/cli/sprint/monitor.py` (569 lines) | `OutputMonitor.start/stop/reset`, `_poll_loop`, `_extract_signals_from_event`, `_handle_assistant_event`, `_handle_user_event`, ring-buffer caps `ACTIVITY_LOG_MAX=3`, `ERRORS_MAX=10` |
| Per-task prompt and Phase.prompt_preview source | `src/superclaude/cli/sprint/process.py` (385 lines) — sprint `ClaudeProcess.build_prompt`; `src/superclaude/cli/sprint/config.py:167` — `_extract_phase_prompt_preview` | `build_prompt` (process.py:123), `_PHASE_INTENT_RE` (config.py:161), `_extract_phase_prompt_preview` (config.py:167) |
| Data model | `src/superclaude/cli/sprint/models.py` | `Phase.prompt_preview` (line 296), `Phase.prompt_display` (308), `MonitorState` (590–657), `SprintResult.duration_display` (542–547) |

Libraries used: **Rich** only (`rich.live.Live`, `rich.panel.Panel`, `rich.table.Table`, `rich.text.Text`, `rich.console.Group`). No use of `rich.progress.Progress`, `rich.progress.BarColumn`, or `textual`. Bars are hand-rolled with U+2588 / U+2591 block characters at a fixed width of 20 (`_BAR_WIDTH = 20`, tui.py:30).

`Live` is constructed with `refresh_per_second=2, screen=False` (tui.py:101–106). Live's auto-refresh runs at 2 Hz on a background thread, but it re-renders **the same renderable** that was last set via `Live.update(...)`. Any field whose computation reads live state from `self.monitor_state` only updates when the executor calls `SprintTUI.update(...)`.

---

## 2. Root-cause diagnosis

### 2.1 Progress bars hang and don't update

**Two distinct execution paths** exist in the sprint loop, with very different update characteristics:

1. **Freeform / single-prompt phases** (executor.py:1266–1390): a fresh `OutputMonitor` is started (line 1277), then a polling loop runs at 0.5 s cadence — inside that loop the executor calls `tui.update(sprint_result, monitor.state, phase)` (line 1373) on every tick. This path works as designed.

2. **Per-task phases** (`tasks = _parse_phase_tasks(phase, config)` is truthy at executor.py:1234 — the modern code path used by virtually every current sprint, since task-listed phases match the `### T<PP>.<TT>` heading convention): control is handed to `execute_phase_tasks` at executor.py:1239. Inside that function the TUI is updated **exactly twice per task** — once right before launch (lines 980–985) and once right after completion (lines 1044–1049). In between, `_run_task_subprocess` calls `proc.wait()` (process.py-equivalent at executor.py:1088). `wait()` is a blocking call. **No `OutputMonitor` is started for per-task phases at all** (grep confirms: only the freeform path on lines 1276–1390 starts one).

   - executor.py:981: `_tui_state = MonitorState()` — a fresh, empty state object is constructed for every per-task update. Even if `Live` repaints at 2 Hz, the live data fields the renderer reads (`monitor_state.stall_seconds`, `monitor_state.last_event_time`, `monitor_state.completed_task_estimate`, `monitor_state.activity_log`) are **all zero/empty by definition** for the duration of every per-task subprocess.

   - The `Tasks` progress bar (`_build_progress`, tui.py:303–334) sums `r.phase.file`'s task count for completed phase results (line 355) plus `monitor_state.completed_task_estimate` for the running phase (line 357). On the per-task path, `completed_task_estimate` stays 0 the whole phase, so the Tasks bar visually "jumps" from N tasks/phase to N+M tasks/phase at phase boundaries with **no intra-phase movement**.

   - The `Phases` progress bar's denominator is `len(self.config.active_phases)` and numerator counts terminal-status results (tui.py:336–340). It moves only when a phase ends, again a step function, not a fill.

**Net effect**: from the user's seat, both bars sit at the post-last-phase value for the entire duration of every task subprocess (often minutes). The phase Duration column likewise reads `int(monitor_state.stall_seconds)` (tui.py:269) which is permanently 0 in per-task mode, so it shows `0s` while the phase is actually running — a strong "hung" signal.

Even on the freeform path there is a secondary bug:
- **tui.py:269** — for `PhaseStatus.RUNNING` the Duration cell shows `stall_seconds` (idle gap since last NDJSON line) instead of *elapsed time since phase started*. That metric *decreases* whenever new output arrives, then *increases* during quiet thinking — visually erratic and not what "Duration" conventionally means.

### 2.2 No real-time indicators

The TUI has *no perpetually-moving widget*:

- **No animated spinner** anywhere. Rich's `rich.spinner.Spinner` is not imported or used. The status icons in `STATUS_ICONS` (tui.py:58–72) are static markup strings; `RUNNING` is the bare text `[yellow]RUNNING[/]` (line 69) — no spinner frame cycling.
- **No "heartbeat" or pulse** in the active panel. The closest thing is `[thinking... Ns]` (tui.py:432–435) which only appears after `_THINKING_IDLE_SECONDS = 2` of idle, then *replaces* the last activity line. When events ARE flowing it disappears — which means the only "live" indicator is hidden when work is most active.
- **`Live` auto-refresh paints the same render-tree** every 500 ms. The only fields that mutate without an explicit executor call are `SprintResult.duration_display` (tui.py:217 → models.py:542 — computed against `datetime.now()`) and the `_render_activity_stream` idle counter (tui.py:431–435 — computed against `time.time()`). Everything else is frozen between executor `tui.update(...)` calls.
- **Per-task path provides no event stream at all** (see 2.1) — no activity log entries, no Agent line, no token counter movement, no growth rate. The `Activity:` section (tui.py:404–406) shows three em-dashes — — — for the whole task.
- The PreFlight + summary worker phases (executor.py:1196–1206, 1158–1174) update the TUI only once each.

### 2.3 Prompt cuts off in wider terminal

The prompt text shown on the active panel's `Prompt:` line is double-truncated to a hard-coded 60 characters, completely independent of terminal width:

1. **Extraction-time truncation** (config.py:167–204):
   - Line 179: fallback `return phase_name[:60]`
   - Line 193: `return m.group(1).strip()[:60]` for matched `**Goal:**`/`**Scope:**`/etc.
   - Line 203: `return first_body_line[:60]` for paragraph fallback
   - Line 204: `return phase_name[:60]` final fallback
   This stores at most 60 chars in `Phase.prompt_preview`.

2. **Render-time truncation** (tui.py:34, 386):
   - `_LLM_LINE_MAX = 60` (constant)
   - `prompt_text = _truncate(self.current_phase.prompt_display, _LLM_LINE_MAX)`
   - `_truncate` (tui.py:614–623) clips to `limit-3` characters and appends `"..."`.

The same `_LLM_LINE_MAX = 60` cap is also applied to `last_assistant_text` (tui.py:387) — the Agent: line cuts off identically.

**Console never reads its actual width.** `self.console = console or Console()` (tui.py:80) constructs a default `Console` whose `width` property is auto-detected from the TTY, but nowhere does any render code consult `self.console.width`. Making the outer `Panel` larger (border-style or padding) does not propagate to the truncation limit, which is what the user is observing.

A related contributor: the activity-stream description is hard-truncated to 50 chars at tui.py:424 (`_truncate(desc, 50)`), error messages to 80 chars at tui.py:459 and 539, and the assistant-text tail to 80 chars upstream at monitor.py:121 (`ASSISTANT_TEXT_MAX_LEN = 80`). Each cap is hard-coded.

---

## 3. Ten proposals

Each proposal cites file:line evidence for the change site, describes the concrete edit, expected outcome, effort tier (S = <1 day, M = 1–3 days, L = >3 days), and risk surface.

### P-01: Wire OutputMonitor into the per-task path

- Symptoms addressed: 2.1 (hang), 2.2 (no real-time)
- File:line: `src/superclaude/cli/sprint/executor.py:919-1051` (`execute_phase_tasks`), `1054-1093` (`_run_task_subprocess`)
- Change: in `execute_phase_tasks`, instantiate `OutputMonitor` once per phase (analogous to executor.py:1276–1277), pass it into `_run_task_subprocess` (or have the helper accept a callback), and replace `proc.wait()` (executor.py:1088) with a poll loop mirroring lines 1303–1381: `while proc._process.poll() is None: tui.update(sprint_result, monitor.state, phase); time.sleep(0.5)`. Reset the monitor's `_last_read_pos` and `_seen_files` between tasks so the file offset re-scans the same `output_file(phase)` (the file is rotated per phase, not per task, so seeded offsets are fine to reset). Aggregate `monitor.state.completed_task_estimate` by binding it to the task index *i* in the per-task TUI updates (or have the monitor surface it via the regex on `T<PP>.<TT>` which it already does at monitor.py:540–549).
- Expected behavior: while a task subprocess runs, the activity stream, agent line, tokens, growth rate, and per-phase Duration all update at 2 Hz; the Tasks bar advances as each task completes; `stall_status` switches between `active`, `thinking...`, and `STALLED`.
- Effort: M
- Risk: changes the threading model for the most-used path; per-task subprocess writes to a shared NDJSON file so the monitor's incremental-read pointer must be reset between tasks (otherwise it skips the first task's output). Existing tests in `tests/sprint/test_execute_phase_tasks*.py` may need fixtures to inject `_subprocess_factory` along with a fake monitor.

### P-02: Replace `stall_seconds` with elapsed-since-phase-start in the Duration column

- Symptoms addressed: 2.1 (hang appearance), 2.2 (clearer real-time signal)
- File:line: `src/superclaude/cli/sprint/tui.py:265-273` (Duration cell), `src/superclaude/cli/sprint/models.py:609` (`phase_started_at` already exists on `MonitorState`)
- Change: in `_build_phase_table` replace `f"{int(self.monitor_state.stall_seconds)}s"` with `f"{int(time.monotonic() - self.monitor_state.phase_started_at)}s"`. Optionally render as `m s` when ≥60.
- Expected behavior: Duration ticks up monotonically every second for the active phase; users see *something* numerically moving even before any other plumbing changes land.
- Effort: S
- Risk: very low; `phase_started_at` is already populated via `MonitorState()`'s default factory and set when `monitor.reset(...)` constructs a fresh state (monitor.py:308). For the per-task path the reset doesn't happen today — pair this with P-01 (or wire `phase_started_at` from the TUI side via `time.monotonic()` captured at first observation of `phase` change).

### P-03: Drive the prompt/agent line width from `console.width` instead of a 60-char constant

- Symptoms addressed: 2.3 (cut-off)
- File:line: `src/superclaude/cli/sprint/tui.py:30-36` (constants), `tui.py:386-387` (truncation calls), `tui.py:80` (`self.console = console or Console()`); also `src/superclaude/cli/sprint/config.py:179,193,203,204` (extraction-time cap)
- Change:
  1. Stop truncating at extraction time: change config.py's `[:60]` slices to `[:240]` (or remove the slice and let the renderer decide).
  2. In `_build_active_panel`, compute an available width from the console: `avail = max(40, self.console.width - 14)` (account for `Prompt:  ` prefix + outer panel border/padding) and pass it as the second arg to `_truncate`.
  3. Apply the same dynamic width to the Agent: line and to error/activity messages.
- Expected behavior: on a 200-column terminal the prompt and agent lines render up to ~180 characters; on an 80-column terminal they still clip cleanly with `...`.
- Effort: S
- Risk: Rich's outer Panel already wraps long lines if you don't truncate, which can change the active panel's height frame-to-frame and cause flicker. Pre-computing `avail` and truncating at that width keeps height stable.

### P-04: Switch the bars to `rich.progress.Progress` driven by a callback

- Symptoms addressed: 2.1 (hang), 2.2 (real-time)
- File:line: `src/superclaude/cli/sprint/tui.py:303-334` (`_build_progress`), `tui.py:30-31` (`_BAR_WIDTH`), `tui.py:588-603` (`_render_bar`, `_render_percent`)
- Change: replace the hand-rolled `█`/`░` line with two `Progress` instances composed via `rich.console.Group`, each using `BarColumn(bar_width=None)` so they auto-stretch to the available width (this was the original v3.7b SPEC at `.dev/releases/complete/v3.7-task-unified-v2/release-split/v3.7b-sprint-tui-v2-SPEC.md:520,535`). Make the Tasks bar `pulse=True` when `current_phase is not None and stall_status in {"thinking...", "STALLED"}` so users get a moving indicator even when no event has just landed.
- Expected behavior: bars stretch to terminal width and the Tasks bar visibly *pulses* during long thinking gaps inside the running phase.
- Effort: M
- Risk: `Progress` widgets must be nested inside `Live` (or use `Live.update(group)` where the group includes the progress); incorrect setup causes double-refresh tearing. The existing v3.7b test suite expects the rendered text format; tests like `test_progress_bar_renders_dual_*` in `tests/sprint/test_tui.py` would need to assert against `BarColumn` output (or render-to-string snapshots).

### P-05: Add a Rich spinner to the RUNNING status cell and the active-panel title

- Symptoms addressed: 2.2 (no real-time)
- File:line: `src/superclaude/cli/sprint/tui.py:58-72` (`STATUS_ICONS`), `tui.py:408-412` (active panel title)
- Change: import `from rich.spinner import Spinner`. In `_build_phase_table`, when `status == PhaseStatus.RUNNING`, set the cell to a `Spinner("dots", text="RUNNING", style="yellow")` instead of `STATUS_ICONS[RUNNING]`. In `_build_active_panel`, prepend a `Spinner("dots2")` to the title so the title bar itself animates. Both spinners advance under `Live`'s auto-refresh — *no* additional plumbing required because `Live` already calls `__rich_console__` on every refresh tick.
- Expected behavior: even when zero NDJSON events have arrived (subprocess startup or long thinking), the RUNNING row visibly spins.
- Effort: S
- Risk: Rich `Spinner` inside `Table.add_row` requires passing the Spinner object (not its rendered string) — confirm cell rendering works with the current `box=None` table. Snapshot-based tests of the table will need to be re-baselined.

### P-06: Add a continuous "events / sec" sparkline or pulse to the active panel

- Symptoms addressed: 2.2 (real-time), 2.1 (hang reassurance)
- File:line: `src/superclaude/cli/sprint/tui.py:389-406` (active-panel line composition); `src/superclaude/cli/sprint/models.py:611,616` (existing `events_received`, `growth_rate_bps`)
- Change: maintain a 30-sample ring buffer of `(monotonic, events_received)` deltas on `SprintTUI` (or extend `MonitorState`); render a 20-char Unicode sparkline (`▁▂▃▄▅▆▇█`) and a `events/sec: 3.4` numeric beside the Activity header. The sparkline updates on every `tui.update(...)` call from the executor's poll loop.
- Expected behavior: users see a small histogram of event throughput; even when no new tool call has been issued, the slope tells them whether the subprocess is doing token-only generation.
- Effort: M
- Risk: requires P-01 to be useful on the per-task path; otherwise the sparkline is flat during per-task runs. Sparkline code itself is ~25 lines.

### P-07: Expand `ASSISTANT_TEXT_MAX_LEN` and the error/activity caps to be width-aware

- Symptoms addressed: 2.3 (cut-off)
- File:line: `src/superclaude/cli/sprint/monitor.py:121` (`ASSISTANT_TEXT_MAX_LEN = 80`), `tui.py:424` (activity desc 50), `tui.py:459, 539` (error msg 80)
- Change: stop trimming in the monitor — store the full assistant text (or up to 400 chars, a kilobyte ceiling), then trim at render-time using the same `console.width`-derived budget from P-03. Same for activity descriptions and error messages.
- Expected behavior: when the terminal widens, *all* truncated lines (Agent/Activity/Errors) get more room, not just the outer panel.
- Effort: S
- Risk: error/activity strings can occasionally contain ANSI escape sequences if a tool echoed them — `Text.from_markup` handles `[...]` syntax but raw `\x1b[31m` would render literally. Existing behavior already passes through whatever the SDK emits, so this isn't a regression. Memory growth is negligible (10-entry ring buffer × 400 char cap = 4 KB).

### P-08: Render the active panel using a `Layout` so widths re-flow on terminal resize

- Symptoms addressed: 2.3 (cut-off), 2.2 (cleaner UX)
- File:line: `src/superclaude/cli/sprint/tui.py:154-197` (`_render`), `tui.py:360-412` (active panel)
- Change: replace the flat `RichGroup` and inline `Panel` composition with a `rich.layout.Layout` tree (header / table / progress / errors / active). Set `Layout(name="active", ratio=1)` so the active panel auto-stretches; Rich propagates the layout width to children and respects panel padding. The renderer then truncates strings to layout-derived widths rather than hard-coded numbers.
- Expected behavior: terminal resize during a sprint reflows the entire dashboard; long phase names, prompts, agent text, and errors all use the available column count.
- Effort: M
- Risk: Layouts behave differently with variable-height children (e.g., the error panel conditionally appears). Need explicit `Layout.size` or `Layout.minimum_size` settings for non-stretchy sections. Re-baseline TUI snapshot tests.

### P-09: Convert `tui.update(...)` from "executor-pushes-renderable" to "event-driven via queue.Queue"

- Symptoms addressed: 2.1 (hang), 2.2 (real-time)
- File:line: `src/superclaude/cli/sprint/tui.py:116-152` (`update`), `executor.py:1296,1373,1238,1263,1529,1611` (every `tui.update` call site)
- Change: introduce `SprintTUI._event_queue: queue.Queue` and a `SprintTUI._render_thread: threading.Thread` that loops `while running: event = self._event_queue.get(timeout=0.25); self._apply(event); self._live.update(self._render())`. Callers in the executor enqueue `TUIEvent.PhaseStart(phase)`, `TUIEvent.MonitorTick(state)`, `TUIEvent.TaskComplete(task, result)`, etc. The monitor thread enqueues `MonitorTick` directly from `_poll_once` instead of via the executor. Decoupling means the per-task subprocess wait can run in the foreground without throttling the render cadence, and the freeform poll loop no longer needs an explicit `tui.update` call.
- Expected behavior: a single render thread refreshes at a steady 4 Hz independent of where the executor is in its loop; the per-task path automatically inherits live updates as soon as the monitor is wired (P-01) or even before, since `phase_started_at` ticks etc.
- Expected behavior: render cadence becomes independent of orchestration logic; latency between an NDJSON event landing and the screen updating drops from up to 500 ms to ≤250 ms.
- Effort: L
- Risk: introduces a new thread + queue; care needed around clean shutdown (sentinel event, `_render_thread.join(timeout=2)` in `stop()`); existing tests that simulate `tui.update` directly need to adapt to the event API; potential ordering bugs if `PhaseStart` is processed after a stale `MonitorTick`.

### P-10: Add a heartbeat line that always renders `now - last_event_time` and a colored dot

- Symptoms addressed: 2.2 (real-time), 2.1 (hang diagnosis)
- File:line: `src/superclaude/cli/sprint/tui.py:389-401` (active panel composition), `models.py:609` (`last_event_time` already exists), `monitor.py:380` (already updated per event)
- Change: insert a new line just below `Status:` in `_build_active_panel`: `Heartbeat: ● 1.2s ago — tokens 4.5K/s` where the dot color cycles green → yellow (>5 s) → red (>30 s) and the suffix shows the EMA-derived growth-rate-bps converted to tokens/sec. Heartbeat updates on every Live tick via `time.monotonic()`.
- Expected behavior: every Live refresh tick (2 Hz today, 4 Hz with P-09) the heartbeat counter ticks; even if all other widgets are frozen the user sees something move, *and* immediately knows whether the freeze is genuine subprocess silence or a stuck dashboard.
- Effort: S
- Risk: minimal; reuses already-populated fields. On the per-task path before P-01 lands, `last_event_time` is reset to `time.monotonic()` at construction (models.py:609) so the heartbeat would always show `0.0s ago` — fix by either lazily setting `last_event_time = 0` (sentinel "never") or by gating the heartbeat on `events_received > 0`.

---

## 4. Suggested top-5 (initial ranking — adversarial step will re-rank)

| Rank | Proposal | Why it leads |
|---|---|---|
| 1 | **P-01** Wire OutputMonitor into the per-task path | Highest-impact single fix; root cause of both "hang" and "no real-time" symptoms for the most-used execution path. Nothing else moves the needle if this stays broken. |
| 2 | **P-02** Elapsed-since-phase-start in Duration column | One-line change; unblocks a quick perception win and makes P-01's progress visible even before fancier widgets land. |
| 3 | **P-03** Dynamic width for prompt/agent lines from `console.width` | Directly fixes symptom 3; small surface area; un-blocks user trust that "wider terminal helps". |
| 4 | **P-05** Rich spinner on RUNNING + active-panel title | Cheapest "always-moving" indicator; works automatically under existing `Live.refresh_per_second=2` because Rich re-renders spinner state every tick without any external push. |
| 5 | **P-10** Heartbeat line in active panel | Composes well with P-01/P-02; addresses the "is it dead?" question directly and turns the frozen experience into a diagnostic one. |

Held back from top-5 (still valuable):
- P-04 (Rich `Progress` with `BarColumn(bar_width=None)`) — strong structural fix but partly redundant with the hand-rolled bars once P-01 makes them update; cost/benefit lower than the dynamic-width fix.
- P-06 (sparkline) — nice-to-have, depends on P-01.
- P-07 (width-aware caps in monitor) — subsumed mostly by P-03; can land together.
- P-08 (`Layout` tree) — structurally correct but larger refactor with re-baseline cost; queue for a later wave.
- P-09 (event-driven render thread) — strongest long-term architecture but L-effort and reshapes the test surface; defer until P-01..P-05 land and the cadence shortcomings of the push-based model are clearly measured.
