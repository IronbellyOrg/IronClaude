# Sprint TUI v2 — Structured Analysis Report

> Generated for unified release spec inclusion.
> Source: `sprint-tui-v2-requirements.md` (~45KB)

---

## A. Executive Summary

Sprint TUI v2 is a visual UX refactor of the SuperClaude Sprint Runner's terminal dashboard. The core insight is that `claude stream-json` already emits rich real-time data (turn counts, token usage, tool call details, assistant text, error signals, model metadata) that the current TUI parses but **does not display**. V2 surfaces this data across 10 features (F1–F10), delivering: a live activity stream, turn/token tracking, task-level progress, conditional error panels, LLM reasoning context lines, automated post-phase summaries (programmatic extraction + Haiku narrative), tmux-integrated summary panes, and a release retrospective. The result is a dashboard that eliminates the need to read raw output files to understand sprint progress and outcomes.

---

## B. Current vs Target State

| Aspect | Current TUI | TUI v2 |
|--------|-------------|--------|
| **Header** | Name + elapsed time | Elapsed + model name + turn counter (turns/max) |
| **Phase table** | 5 columns (#, Phase, Status, Duration, Tasks) | 6 columns (#, Phase, Status, Duration, **Turns**, **Output**); Tasks column removed |
| **Progress** | Single phase-level progress bar | **Dual progress bars** — Phases + Tasks on one line |
| **Active panel** | File, status, last task/tool, output size, files changed | + **Activity stream** (last 3 tool calls), **Prompt preview**, **Agent reasoning line** |
| **Errors** | None displayed during run | **Conditional error panel** (red border, up to 5 errors) |
| **Post-phase info** | None | **Phase summaries** written to `results/phase-N-summary.md` (background thread) |
| **Post-sprint info** | Result + resume command | **Enhanced terminal panels** with aggregate stats (turns, tokens in/out, output bytes, files) |
| **Release summary** | None | **Release retrospective** (`results/release-retrospective.md`) with validation matrix |
| **Tmux layout** | 2 panes (TUI + tail) | **3 panes** (TUI 50% + summary 25% + tail 25%) |
| **Sprint name** | Absent from border | Shown in **outer panel title** |

---

## C. Feature Catalog

### F1: Activity Stream

- **Purpose**: Show last 3 tool calls in real time within the active panel
- **Location**: Bottom of active phase panel (indented timestamp lines, no sub-border)
- **Data source**: `tool_use` events from stream-json — `event.content[type=tool_use].name` + first argument from `.input`
- **MonitorState additions**: `activity_log: list[tuple[float, str, str]]` — max 3 items (FIFO ring buffer)
- **Implementation**: Tool names shortened (e.g., `TodoWrite` → `Todo`), inputs truncated to fit width. When no tool call for >2s, insert updating `[thinking... Ns]` placeholder
- **Dependencies**: None (standalone)

### F2: Enhanced Phase Table

- **Purpose**: Surface turn count and output size per phase in the main table
- **Location**: Phase table (replaces current 5-column layout)
- **Data source**: Completed phases → `PhaseResult.turns` / `.output_bytes`; running phase → `MonitorState.turns` / `.output_size_display`
- **MonitorState additions**: `turns: int = 0`
- **Implementation**: Add **Turns** (width=6, right-aligned) and **Output** (width=8, right-aligned) columns; remove Tasks column
- **Dependencies**: None (standalone)

### F3: Task-Level Progress Bar

- **Purpose**: Show task completion alongside phase completion on a single compact line
- **Location**: Dedicated line between phase table and active panel
- **Data source**: Total tasks pre-scanned from all phase files at sprint start (`T\d{2}\.\d{2}` pattern). Completed tasks = sum from finished phases + ordinal estimate from `MonitorState.last_task_id` for current phase
- **MonitorState additions**: `total_tasks_in_phase: int = 0`, `completed_task_estimate: int = 0`
- **Implementation**: Single `Text` line with manual bar characters (`\u2588` filled, `\u2591` empty), not two `Progress` widgets. Method: `_build_dual_progress()` returning `Text.from_markup()`
- **Dependencies**: F2 (shares phase tracking data), `SprintConfig.total_tasks` pre-scan

### F4: Conditional Error Panel

- **Purpose**: Surface errors as they occur during a sprint, hidden when count is 0
- **Location**: Below the active panel
- **Data source**: `tool_result` events with `is_error` field or error content; Bash tool results with `exit_code != 0`
- **MonitorState additions**: `errors: list[tuple[str, str, str]]` — (task_id, tool_name, message), max 10, display 5
- **Implementation**: Red-bordered `Panel` with title `ERRORS (N)`. Max 5 lines shown; `(+N more)` overflow indicator
- **Dependencies**: None (standalone)

### F5: LLM Context Lines

- **Purpose**: Show what the LLM was prompted with and what it's currently reasoning about
- **Location**: Inside active panel, between Task/Tool line and activity stream
- **Data source**: `Prompt:` — static per phase from `ClaudeProcess.build_prompt()`. `Agent:` — updates on each `assistant` event with `content[type=text].text`
- **MonitorState additions**: `last_assistant_text: str = ""` (last ~80 chars, truncated)
- **Implementation**: Two lines truncated to panel width minus label. Prompt stored in `Phase.prompt_preview` or `SprintConfig`
- **Dependencies**: None (standalone)

### F6: Enhanced Terminal Summary Panels

- **Purpose**: Rich aggregate stats in the post-sprint terminal display
- **Location**: Terminal panel (replaces current simple result + resume display)
- **Data source**: `SprintResult` aggregate properties
- **Model additions**: `SprintResult` properties — `total_turns`, `total_tokens_in`, `total_tokens_out`, `total_output_bytes`, `total_files_changed`
- **Implementation**: Two variants — **Success** panel (`SPRINT COMPLETE`: result, duration, turns total+avg, tokens in/out, output, files, log path) and **Halt** panel (`SPRINT HALTED -- Phase N`: + completed count, last task, errors, resume command)
- **Dependencies**: F2 (turn data), F4 (error data)

### F7: Sprint Name in Outer Panel Title

- **Purpose**: Identify which sprint/release is running in the TUI border
- **Location**: Outer `Panel` title
- **Data source**: `config.index_path.parent.name` (already computed in `_build_header()`)
- **Implementation**: Change `Panel(title=...)` from `[bold]SUPERCLAUDE SPRINT RUNNER[/]` to `[bold]SUPERCLAUDE SPRINT RUNNER[/] [dim]== {release_name}[/]`
- **Dependencies**: None (standalone, trivial)

### F8: Post-Phase Summary (Hybrid: Programmatic + Haiku Narrative)

- **Purpose**: Auto-generate structured + narrative summary after each phase completes, eliminating need to read raw output
- **Location**: Written to `results/phase-N-summary.md`; displayed in tmux summary pane (F9)
- **Data sources**: Phase output NDJSON file (`phase-N-output.txt`)
- **New module**: `summarizer.py` — `PhaseSummary` dataclass + `PhaseSummarizer` class
- **Implementation**: 4-step pipeline executed in background `SummaryWorker` thread:
  1. **Programmatic extraction** (instant): tasks, files changed, validation evidence, agent reasoning excerpts, errors from NDJSON
  2. **Haiku narrative** (10–30s): `claude --print --model claude-haiku-4-5 -p "<prompt>"` for 3–5 sentence summary
  3. **Write** `results/phase-N-summary.md`
  4. **Update** tmux summary pane or TUI notification
- **Failure mode**: If Haiku call fails/times out (15s), summary written without narrative section
- **Dependencies**: F9 (tmux integration for display)

### F9: Tmux Summary Pane

- **Purpose**: Dedicated pane for viewing phase summaries without leaving the TUI
- **Location**: Middle pane in 3-pane tmux layout (25% height)
- **Data source**: `results/phase-N-summary.md` piped to pane via `tmux send-keys`
- **Implementation**: On sprint start create 3-pane layout; update middle pane via `update_summary_pane()` function; `--no-tmux` fallback shows notification in TUI header
- **Dependencies**: F8 (provides the summary content), `tmux.py` modifications

### F10: Release Retrospective

- **Purpose**: Aggregate all phase summaries into a release-level synthesis with validation matrix
- **Location**: Written to `results/release-retrospective.md`; displayed in terminal panel and tmux summary pane
- **New module**: `retrospective.py` — `ReleaseRetrospective` dataclass + `RetrospectiveGenerator` class
- **Data sources**: All `results/phase-N-summary.md` files
- **Implementation**: 5-step pipeline, **blocking** (runs before terminal display):
  1. Read all phase summary files
  2. Programmatic aggregation (combined stats, files, validation matrix, cross-phase patterns)
  3. Haiku narrative (4–8 sentence release narrative)
  4. Write `results/release-retrospective.md`
  5. Display in terminal panel / summary pane
- **Dependencies**: F8 (phase summaries must exist), F6 (terminal panel integration), F9 (tmux display)

---

## D. Target Layouts

### Active Sprint (~25 lines)

Three regions from top to bottom:
1. **Header**: Elapsed, Model, Turns counter
2. **Phase table**: 6-column table (#, Phase, Status, Duration, Turns, Output)
3. **Dual progress line**: `Phases ======-------- 25% 1/4    Tasks ==========------ 51% 20/39`
4. **Active panel** (bordered): Status + throughput, Task/Tool/Files, Prompt line, Agent line, 3 activity stream lines
5. **Error panel** (conditional, red border): Up to 5 error lines

All wrapped in outer `Panel` with title `SUPERCLAUDE SPRINT RUNNER == {release_name}`.

### Sprint Complete

Replaces active panel + error panel with **SPRINT COMPLETE** bordered panel containing:
- Result: ALL PHASES PASSED
- Duration, Turns (total + avg/phase), Tokens (in/out), Output (total KB), Files (created/modified), Log path

Phase table shows all phases as PASS. Dual progress shows 100% on both bars.

### Sprint Halted

Replaces active panel with **SPRINT HALTED -- Phase N** bordered panel containing:
- Result: HALTED at Phase N (reason)
- Duration, Completed (phases + tasks), Turns, Tokens (in/out), Last task + failure reason, Files
- Errors section (folded in, same format as F4)
- Resume command, Log path

Incomplete phases show as `skipped`. Dual progress shows partial completion.

---

## E. New Modules

### `summarizer.py`

**Classes**:

| Class | Purpose |
|-------|---------|
| `PhaseSummary` | Dataclass holding structured extraction results + narrative for one phase |
| `PhaseSummarizer` | Orchestrates extraction + narrative generation + file writing |
| `SummaryWorker` | Background thread pool managing async summary generation (in `executor.py` or `summarizer.py`) |

**`PhaseSummary` fields**:
- `phase: Phase`, `phase_result: PhaseResult`
- `tasks: list[dict]` — `[{id, tier, status, description}]`
- `files_changed: list[dict]` — `[{action, path}]`
- `validations: list[dict]` — `[{task, method, command, result}]`
- `reasoning_excerpts: list[str]` — top 3–5 snippets (~80 chars each)
- `errors: list[dict]` — `[{task, tool, message}]`
- `narrative: str` — Haiku-generated, may be empty
- `summary_path` property → `results/phase-{N}-summary.md`

**`PhaseSummarizer` key methods**:
- `summarize(phase, phase_result) -> PhaseSummary` — full pipeline
- `_extract_structured(output_file, summary)` — NDJSON parsing for 5 categories
- `_generate_narrative(summary)` — Haiku subprocess call with 30s timeout
- `_build_narrative_prompt(summary) -> str` — template construction
- `_write_summary(summary)` — markdown file generation

**Programmatic extraction details** (the heavy lifting):
1. **Tasks**: Parse `TodoWrite` events for task list/status; match `T\d{2}\.\d{2}` patterns
2. **Files**: Extract from `Write`/`Edit`/`MultiEdit` tool_use inputs + Bash commands (`mkdir`, `touch`, `cp`, `mv`)
3. **Validation evidence**: Identify verification patterns (Read after Write to same file, Bash with `ls`/`test`/`diff`/`grep`, assertions in text)
4. **Agent reasoning**: Collect assistant text with signal words ("because", "decided", "checked", "verified"), top 3–5 snippets
5. **Errors**: `is_error: true` tool results, non-zero Bash exit codes, error keywords in text

**Haiku narrative pattern**: Uses `claude --print --model claude-haiku-4-5 --max-turns 1 --dangerously-skip-permissions -p "<prompt>"` via subprocess. Environment strips `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT`. Stdin set to `DEVNULL`. 30s timeout. Produces 3–5 sentence summary. Failure is non-fatal.

**`SummaryWorker` threading model**:
- `submit(phase, phase_result)` — spawns daemon `threading.Thread` named `summary-phase-{N}`
- `_run(phase, phase_result)` — calls `PhaseSummarizer.summarize()`, stores result, notifies tmux pane
- `wait_all(timeout=60)` — joins all threads before retrospective generation
- `latest_summary_path` property — for TUI notification in `--no-tmux` mode
- **Critical invariant**: Summary failure must never affect sprint execution (all exceptions caught)

### `retrospective.py`

**Classes**:

| Class | Purpose |
|-------|---------|
| `ReleaseRetrospective` | Dataclass holding aggregated release-level data + narrative |
| `RetrospectiveGenerator` | Reads phase summaries, aggregates, generates narrative, writes file |

**`ReleaseRetrospective` fields**:
- `sprint_result: SprintResult`
- `phase_outcomes: list[dict]` — `[{phase, name, duration, tasks, status, key_outcome}]`
- `all_files: list[dict]` — `[{phase, action, path}]`
- `validation_matrix: list[dict]` — `[{task, tier, method, command, result}]`
- `all_errors: list[dict]`
- `validation_coverage: str` — e.g., `"39/39 verified (6 STRICT, 28 STANDARD, ...)"`
- `narrative: str`

**`RetrospectiveGenerator` key methods**:
- `generate(sprint_result) -> ReleaseRetrospective` — full pipeline
- `_read_phase_summaries() -> list[str]` — reads all `phase-N-summary.md` files
- `_aggregate(summaries, retro)` — cross-phase analysis (file evolution, error patterns, validation gaps, timing trends)
- `_generate_narrative(retro)` — Haiku call for 4–8 sentence release narrative
- `_write_retrospective(retro)` — writes `results/release-retrospective.md`

**Output**: `config.results_dir / "release-retrospective.md"` — contains phase progression table, all files created/modified, validation evidence matrix, validation coverage stats, error summary, and narrative.

---

## F. Model Changes

### `MonitorState` — 7 new fields

```python
activity_log: list = field(default_factory=list)    # F1: list[tuple[float, str, str]], max 3
turns: int = 0                                       # F2: assistant turn counter
errors: list = field(default_factory=list)           # F4: list[tuple[str, str, str]], max 10
last_assistant_text: str = ""                        # F5: last ~80 chars of assistant text
total_tasks_in_phase: int = 0                        # F3: tasks in current phase
completed_task_estimate: int = 0                     # F3: estimated completed tasks
tokens_in: int = 0                                   # F6: accumulated input tokens
tokens_out: int = 0                                  # F6: accumulated output tokens
```

### `PhaseResult` — 3 new fields

```python
turns: int = 0
tokens_in: int = 0
tokens_out: int = 0
```

### `SprintResult` — 5 new aggregate properties

```python
@property
def total_turns(self) -> int: ...
@property
def total_tokens_in(self) -> int: ...
@property
def total_tokens_out(self) -> int: ...
@property
def total_output_bytes(self) -> int: ...
@property
def total_files_changed(self) -> int: ...
```

### `SprintConfig` — 1 new field

```python
total_tasks: int = 0  # pre-scanned from all phase files on sprint start
```

---

## G. File Inventory

### Modified Files (5)

| File | Change Summary |
|------|----------------|
| `models.py` | Add 7 fields to `MonitorState`, 3 to `PhaseResult`, 5 properties to `SprintResult`, 1 field to `SprintConfig` |
| `monitor.py` | Add turn counting, token tracking, activity log ring buffer, error detection, assistant text extraction, task counting in `_extract_signals_from_event()`. New static `count_tasks_in_file()` method |
| `tui.py` | Rewrite `_render()` layout; add `_build_dual_progress()`, `_build_error_panel()` methods; enhance `_build_active_panel()` with activity stream + LLM context; enhance `_build_terminal_panel()` with aggregate stats; add summary notification support; put release name in outer panel title |
| `executor.py` | Integrate `SummaryWorker` (submit after each phase), `RetrospectiveGenerator` (blocking before terminal), summary notification to TUI for `--no-tmux` mode |
| `tmux.py` | Change to 3-pane layout (50/25/25); add `update_summary_pane()` function; shift tail pane index from `:0.1` to `:0.2`; update `update_tail_pane()` accordingly |

### New Files (2)

| File | Purpose |
|------|---------|
| `summarizer.py` | `PhaseSummary` dataclass, `PhaseSummarizer` (programmatic NDJSON extraction + Haiku narrative generation), `SummaryWorker` (background threading) |
| `retrospective.py` | `ReleaseRetrospective` dataclass, `RetrospectiveGenerator` (phase summary aggregation + Haiku narrative + retrospective file writing) |

### Output Artifacts (per sprint run)

| File | Timing |
|------|--------|
| `results/phase-N-summary.md` | Background, after each phase completes |
| `results/release-retrospective.md` | Blocking, after all phases complete (before terminal panel) |

---

## H. Tmux Integration

### 3-Pane Layout

| Pane | Index | Height | Content |
|------|-------|--------|---------|
| Top | `:0.0` | 50% | Sprint TUI dashboard (Rich live display) |
| Middle | `:0.1` | 25% | Phase summary display (updated per phase) |
| Bottom | `:0.2` | 25% | `tail -f phase-N-output.txt` |

### Summary Pane Management

- **Initial state**: Shows `"Waiting for first phase to complete..."`
- **On phase summary ready**: `update_summary_pane()` sends `C-c` to interrupt, then `clear && cat <summary_file>` plus zoom hint
- **User interaction**: `Ctrl-B z` to zoom/unzoom the summary pane for full-screen reading
- **Each new summary replaces the previous** one in the same pane

### Pane Index Migration

The tail pane moves from `:0.1` (2-pane) to `:0.2` (3-pane). The `update_tail_pane()` function must be updated to reference the new index.

### `--no-tmux` Fallback

- Summary files still written to `results/phase-N-summary.md`
- TUI shows notification line below header: `Phase 1 summary ready: results/phase-1-summary.md`
- Notification stored in `SprintTUI.latest_summary_notification: str | None`
- Updated by executor when `SummaryWorker.latest_summary_path` changes
- Retrospective still generated; path shown in terminal panel

---

## I. Test Impact

### Existing Tests Requiring Updates

| Test File | Changes Needed |
|-----------|----------------|
| `test_tui.py` | New columns in phase table assertions; new `MonitorState` fields in fixtures; new terminal panel content; new `_build_dual_progress()` and `_build_error_panel()` methods; summary notification display |
| `test_models.py` | New fields on `MonitorState`, `PhaseResult`; `SprintResult` aggregate properties; `SprintConfig.total_tasks` |

### New Tests Needed

| Test File | Coverage |
|-----------|----------|
| `test_summarizer.py` | `PhaseSummarizer` programmatic extraction from NDJSON fixtures, narrative prompt building, summary markdown generation, `SummaryWorker` background execution and thread safety |
| `test_retrospective.py` | `RetrospectiveGenerator` aggregation from phase summaries, narrative prompt building, retrospective markdown generation |
| `test_tmux.py` (if exists) | 3-pane layout creation, summary pane updates, pane index handling |

### Tests Not Affected

`test_cli_contract.py`, `test_config.py` (beyond `total_tasks`), `test_process.py`, `test_e2e_*.py`

---

## J. Out of Scope Items (Explicitly Deferred)

1. `--compact` CLI flag to revert to current minimal layout
2. Cost tracking / cache hit ratio display
3. MCP server health indicators in TUI
4. ETA estimation for phase/sprint completion
5. `sprint status` and `sprint logs` command implementations (currently stubs)
6. Modal overlay for summary viewing in `--no-tmux` mode (keyboard input)
7. Configurable summary model (currently hardcoded to `claude-haiku-4-5`)
8. Interactive summary navigation (viewing older phase summaries in tmux pane)

---

## K. Open Questions / Technical Risks

### Technical Risks

1. **Haiku subprocess reliability**: The summary and retrospective depend on `claude --print --model claude-haiku-4-5` subprocess calls. If the `claude` CLI is not available, misconfigured, or the API is rate-limited, narratives will be empty. The spec handles this gracefully (non-fatal), but users may expect narratives to always be present.

2. **Thread safety of `SummaryWorker`**: Background threads access `PhaseResult` and write to shared filesystem paths. While each thread writes to a distinct `phase-N-summary.md`, the `_summaries` dict is mutated from multiple threads without explicit locking. Consider adding a `threading.Lock` around `_summaries` access.

3. **NDJSON parsing robustness**: The programmatic extraction in `_extract_structured()` parses `phase-N-output.txt` which is NDJSON from Claude's stream-json. Malformed lines, unexpected event types, or schema changes could break extraction. The spec does not detail error handling within the parser.

4. **Task counting accuracy**: Task-level progress (F3) uses regex `T\d{2}\.\d{2}` pre-scan and ordinal position estimation from `last_task_id`. Tasks that are skipped, reordered, or have non-standard IDs could produce inaccurate counts. The field is named `completed_task_estimate` acknowledging this.

5. **Tmux pane index fragility**: The 3-pane layout relies on hardcoded pane indices (`:0.0`, `:0.1`, `:0.2`). If pane creation fails partway through, indices could be wrong. The spec has a try/except that kills the session on failure, but partial failures could leave orphaned panes.

6. **Terminal width constraints**: The active sprint layout targets ~25 lines and assumes ~120 column width. Narrower terminals could cause wrapping in the dual progress bar, phase table columns, or activity stream lines. No responsive/adaptive behavior is specified.

7. **Token tracking accuracy**: Token counting uses `usage.input_tokens + cache_read_input_tokens` from assistant message events. If the stream-json schema changes or if some events don't include usage data, totals could be underreported.

### Open Questions

1. **Where does `SummaryWorker` live?** The spec shows it in both `summarizer.py` (class definition) and `executor.py` (integration). The class definition placement is ambiguous — likely intended for `summarizer.py` but should be confirmed.

2. **Prompt preview source**: F5 says prompt is "from `ClaudeProcess.build_prompt()`" but the TUI doesn't currently have access to the full prompt text. The spec suggests adding `prompt_preview: str` to `Phase` or computing from config, but doesn't specify which approach to use.

3. **Token display helper placement**: The `_format_tokens(n: int) -> str` utility is defined in the spec without specifying which module it belongs to. Likely `tui.py` or a shared `utils.py`.

4. **Activity log thinking indicator**: F1 specifies that when no tool call arrives for >2s, a `[thinking... Ns]` line should "update in place". This requires a timer mechanism in the monitor or TUI refresh loop that is not detailed.

5. **Retrospective blocking duration**: F10's retrospective is blocking before terminal display. If the Haiku call takes the full 30s timeout, this delays the user from seeing the final result. No progress indicator is specified for this wait.

6. **`output_bytes` on `PhaseResult`**: F2 notes this field "already exists" but the spec also lists it as new in `SprintResult.total_output_bytes`. Confirm whether `PhaseResult.output_bytes` is truly pre-existing or needs to be added.

7. **`files_changed` tracking**: `SprintResult.total_files_changed` requires `PhaseResult.files_changed`, but this field is not listed as a new addition to `PhaseResult`. It may already exist or need to be added alongside the other new fields.
