# Domain Analysis: Sprint TUI v2

**Source:** `.dev/releases/backlog/v3.7-task-unified-v2/sprint-tui-v2-requirements.md`
**Date:** 2026-04-02
**Analyst:** rf-analyst (claude-opus-4-6)
**Depth:** Deep

---

## 1. Executive Summary

### What TUI v2 Delivers

The Sprint TUI v2 is a comprehensive visual UX refactor that surfaces rich real-time telemetry from Claude's `stream-json` output into the sprint dashboard. The current TUI displays minimal information (header, phase table with 5 columns, single progress bar, basic active panel, and terminal panel). The target state adds 10 features across 7 files that provide: a live activity stream of tool calls, enhanced phase table with turn/output columns, dual progress bars (phase + task), conditional error panel, LLM context preview lines, post-phase summary generation with Haiku narratives, tmux summary pane integration, and release retrospective generation.

**Source:** Requirements spec, "Summary" section (lines 9-11) and "Current State" section (lines 15-17).

### Current State vs Target State

| Dimension | Current | Target |
|-----------|---------|--------|
| Phase table columns | #, Phase, Status, Duration, Tasks | #, Phase, Status, Duration, Turns, Output |
| Progress bars | 1 (phase-level only) | 2 (phase + task on single line) |
| Active panel content | File, Status, Last task/tool, Output size, Files changed | Status, Task/Tool/Files, Prompt preview, Agent text, 3-line activity stream |
| Error visibility | None (errors buried in output) | Conditional red-bordered error panel (max 5 displayed) |
| Post-phase analysis | None | Background SummaryWorker thread with Haiku narrative |
| Release summary | None | Blocking retrospective with aggregated stats + narrative |
| Tmux panes | 2 (TUI 75% + tail 25%) | 3 (TUI 50% + summary 25% + tail 25%) |
| Token/turn tracking | Not displayed | Header shows turns; terminal panel shows tokens in/out |

### Scope

- **5 modified files:** `models.py`, `monitor.py`, `tui.py`, `executor.py`, `tmux.py`
- **2 new files:** `summarizer.py`, `retrospective.py`
- **Output artifacts per sprint:** `results/phase-N-summary.md`, `results/release-retrospective.md`

**Source:** "File Inventory" section (lines 1115-1135).

---

## 2. Feature Inventory

### F1: Activity Stream (3 lines, scrolling)

- **Purpose:** Show real-time tool call activity so users can see what the agent is doing without reading raw output. Replaces the opaque "active" status with concrete tool-by-tool visibility.
- **User value:** Eliminates the need to tail output files to understand current agent activity. Provides immediate feedback on agent progress.
- **Data sources:** `tool_use` events from stream-json. Extracts `event.content[type=tool_use].name` and first argument from `.input`. (Source: lines 131-132)
- **MonitorState fields:**
  - `activity_log: list[tuple[float, str, str]]` -- (timestamp, tool_name, description), max 3 entries (Source: lines 133-135)
- **Implementation approach:**
  - Located at bottom of active phase panel, no sub-border, indented timestamp lines
  - FIFO ring buffer of 3 entries
  - Tool name shortening: `TodoWrite` -> `Todo`, `ToolSearch` -> `Search`, `MultiEdit` -> `Multi` (Source: line 126)
  - Tool inputs truncated to fit width; file paths shortened to basename for long paths (Source: line 127)
  - Thinking indicator: when no tool call for >2 seconds, insert `[thinking... Ns]` line updating in place (Source: line 128)
  - Format: `HH:MM:SS  ToolName  condensed_input` (Source: line 125)
- **Dependencies:** Requires monitor.py changes to extract tool_use events (F1 data extraction in `_extract_signals_from_event`)

### F2: Enhanced Phase Table

- **Purpose:** Add turn count and output size columns to the phase table for at-a-glance phase performance metrics.
- **User value:** Users can see how many turns each phase consumed and how much output was generated without checking logs.
- **Data sources:**
  - Completed phases: `PhaseResult.turns` and `PhaseResult.output_bytes` (Source: line 145)
  - Running phase: `MonitorState.turns` and `MonitorState.output_size_display` (Source: line 147)
- **MonitorState fields:**
  - `turns: int = 0` (Source: line 863)
- **PhaseResult fields:**
  - `turns: int = 0` (Source: line 887)
- **Implementation approach:**
  - Add columns: **Turns** (width=6, right-aligned), **Output** (width=8, right-aligned) (Source: lines 141-142)
  - Remove existing **Tasks** column (task info moves to active panel) (Source: line 143)
  - Keep existing: #, Phase, Status, Duration
- **Dependencies:** Requires MonitorState.turns from F2 monitor extraction, PhaseResult.turns populated in executor

### F3: Task-Level Progress Bar (same line as phase bar)

- **Purpose:** Show task-level completion alongside phase-level completion on a single compact line.
- **User value:** Provides granular progress insight -- "25% of phases but 51% of tasks done" tells a different story than phase progress alone.
- **Data sources:**
  - Phase bar: existing `phases_passed / len(active_phases)` (Source: line 157)
  - Task bar total: Pre-scanned `T\d{2}\.\d{2}` patterns across all phase files, stored in `SprintConfig.total_tasks` (Source: lines 159-160)
  - Task bar completed: Sum of completed tasks from finished phases + estimate from `MonitorState.last_task_id` ordinal position (Source: lines 160-161)
- **MonitorState fields:**
  - `total_tasks_in_phase: int = 0` (Source: line 875)
  - `completed_task_estimate: int = 0` (Source: line 876)
- **SprintConfig fields:**
  - `total_tasks: int = 0` (Source: line 919)
- **Implementation approach:**
  - Single `Text` line with manual bar characters using Rich markup (Source: lines 163-170)
  - Block characters: `\u2588` (full block) for filled, `\u2591` (light shade) for empty (Source: line 172)
  - Two `Progress` widgets side-by-side explicitly rejected as approach (Source: line 163)
  - New method: `_build_dual_progress()` returns `Text` (Source: lines 165-170)
  - Layout: `Phases ======-------- 25% 1/4    Tasks ==========------ 51% 20/39` (Source: lines 152-154)
- **Dependencies:** Requires SprintConfig.total_tasks populated during config loading, MonitorState task counting

### F4: Conditional Error Panel

- **Purpose:** Surface errors immediately in the TUI instead of burying them in output files.
- **User value:** Critical for real-time error awareness. Users see errors as they happen without waiting for phase completion.
- **Data sources:** `tool_result` events where `is_error` field is true, or `type: "tool_result"` with error content. Also Bash tool results with `exit_code != 0`. (Source: lines 182-183)
- **MonitorState fields:**
  - `errors: list[tuple[str, str, str]]` -- (task_id, tool_name, message), max 10 stored, max 5 displayed (Source: lines 186-188)
- **Implementation approach:**
  - Hidden when error count is 0 (Source: line 177)
  - Appears below active panel (Source: line 177)
  - Each line: `TaskID  ToolName  error_message_truncated` (Source: line 179)
  - Max 5 displayed; if >5, show `(+N more)` on last line (Source: lines 180-181)
  - Task ID extracted from context if available, otherwise `-` (Source: line 181)
  - Panel styling: Red border, title `ERRORS (N)` (Source: line 190)
  - New method: `_build_error_panel()` returns `Panel | None` (Source: line 997)
- **Dependencies:** Requires monitor.py error detection from tool_result events

### F5: LLM Context Lines

- **Purpose:** Show what the agent was asked (prompt preview) and what it's thinking (last assistant text) directly in the TUI.
- **User value:** Provides insight into agent reasoning without reading output. The "Agent:" line is particularly valuable for understanding agent decision-making in real time.
- **Data sources:**
  - Prompt: `ClaudeProcess.build_prompt()`, truncated to ~60 chars (Source: line 197)
  - Agent text: `assistant` events with `content[type=text].text`, truncated to ~60 chars (Source: line 198)
- **MonitorState fields:**
  - `last_assistant_text: str` -- last ~80 chars of assistant text output (Source: lines 200-201)
- **Implementation approach:**
  - Located inside active panel, between Task/Tool line and activity stream (Source: line 195)
  - Two lines: `Prompt:  <first ~60 chars>...` and `Agent:   <first ~60 chars>...` (Source: lines 197-198)
  - Static prompt per phase, stored in `SprintConfig` or `Phase` object via `prompt_preview: str` field (Source: line 205)
  - Agent text updates on each assistant event (Source: line 198)
- **Dependencies:** Requires monitor.py assistant text extraction, Phase or SprintConfig prompt_preview field

### F6: Enhanced Terminal Summary Panels

- **Purpose:** Replace the minimal terminal panels with comprehensive aggregate statistics.
- **User value:** Complete sprint outcome at a glance without checking log files.
- **Data sources:** All aggregate from `SprintResult` properties (Source: line 215)
- **SprintResult properties (new):**
  - `total_turns -> int` (Source: lines 896-897)
  - `total_tokens_in -> int` (Source: lines 899-900)
  - `total_tokens_out -> int` (Source: lines 902-903)
  - `total_output_bytes -> int` (Source: lines 905-906)
  - `total_files_changed -> int` (Source: lines 908-909)
- **PhaseResult fields (new):**
  - `tokens_in: int = 0` (Source: line 888)
  - `tokens_out: int = 0` (Source: line 889)
- **Implementation approach:**
  - Success panel: Result, Duration, Turns (total + avg/phase), Tokens (in/out), Output, Files, Log path (Source: lines 210-211)
  - Halt panel: Result, Duration, Completed (phases + tasks), Turns, Tokens, Last task + failure reason, Files, Errors folded in, Resume command, Log path (Source: lines 213-214)
  - Token display helper: `_format_tokens(n)` returns human-readable format (K/M suffixes) (Source: lines 1089-1096)
- **Dependencies:** Requires PhaseResult.turns/tokens populated by executor, SprintResult aggregate properties

### F7: Sprint Name in Outer Panel Title

- **Purpose:** Show the release name in the panel border for at-a-glance identification.
- **User value:** When running multiple sprints or reviewing terminal history, immediately identifies which release this dashboard belongs to.
- **Data sources:** `config.index_path.parent.name` (already computed in `_build_header()`) (Source: line 234)
- **Implementation approach:**
  - Current: `[bold]SUPERCLAUDE SPRINT RUNNER[/]` (Source: line 232)
  - New: `[bold]SUPERCLAUDE SPRINT RUNNER[/] [dim]== {release_name}[/]` (Source: line 233)
  - Rich `Panel(title=...)` auto-adjusts border padding (Source: line 236)
  - Release name removed from header (moved to panel title) (Source: line 1015)
- **Dependencies:** None -- purely cosmetic, uses existing data

### F8: Post-Phase Summary (Hybrid: Programmatic + Haiku Narrative)

- **Purpose:** After each phase completes, generate a structured summary of accomplishments, file changes, validations, and agent reasoning. Eliminates the need to read raw output files.
- **User value:** The highest-value feature in this spec. Users get a human-readable phase report automatically without manual output inspection.
- **Data sources:** `phase-N-output.txt` (NDJSON), parsed programmatically (Source: lines 317-319)
- **Implementation approach:**
  - **Execution model:** Non-blocking. Phase N+1 starts immediately; SummaryWorker thread spawns in background. (Source: lines 246-265)
  - **Step 1:** Programmatic extraction from NDJSON -- tasks, files, validations, reasoning, errors, stats (Source: lines 317-328)
  - **Step 2:** Haiku narrative call via `claude --print --model claude-haiku-4-5 -p "<prompt>"` with 30s timeout (Source: lines 333-348)
  - **Step 3:** Write `results/phase-N-summary.md` (Source: line 262)
  - **Step 4:** Update tmux summary pane or TUI notification (Source: line 264)
  - **Failure mode:** If Haiku call fails or times out, summary written without narrative section (Source: line 350)
  - **Programmatic extraction details (5 categories):**
    1. Task status table: Parse TodoWrite events, match `T\d{2}\.\d{2}` patterns (Source: lines 320-321)
    2. Files changed: Extract from Write/Edit/MultiEdit/Bash tool_use events (Source: lines 323-324)
    3. Validation evidence: Identify verification tool calls (Read after Write, ls/test/diff/grep on recent files) (Source: lines 326-327)
    4. Agent reasoning excerpts: Sentences with "because", "decided", "checked", etc., top 3-5 snippets ~80 chars (Source: lines 329-330)
    5. Errors: `is_error: true`, non-zero Bash exit codes, "error"/"failed" text (Source: line 331)
  - **New module:** `summarizer.py` with `PhaseSummary` dataclass and `PhaseSummarizer` class (Source: lines 510-618)
  - **New class:** `SummaryWorker` in `executor.py` -- background thread pool (Source: lines 698-745)
- **Dependencies:** Requires `claude` binary in PATH, executor integration, tmux pane management

### F9: Tmux Summary Pane

- **Purpose:** Dedicate a tmux pane to displaying phase summaries, so users can read summaries alongside the TUI without switching context.
- **User value:** Eliminates context-switching between TUI and file reading. Summaries appear automatically as phases complete.
- **Data sources:** `results/phase-N-summary.md` files written by SummaryWorker (Source: line 372)
- **Implementation approach:**
  - **Layout change:** 3 panes instead of 2: TUI (50%) + summary (25%) + output tail (25%) (Source: lines 357-368)
  - Summary pane initially shows `Waiting for first phase to complete...` (Source: line 371)
  - Updated via `tmux send-keys` piping `cat results/phase-N-summary.md` to the pane (Source: lines 378-391)
  - User can zoom with `Ctrl-B z` (Source: line 375)
  - **Pane index shift:** Tail pane moves from `:0.1` to `:0.2` (Source: line 833)
  - **`--no-tmux` fallback:** Summary files still written; TUI shows notification line below header: `Phase 1 summary ready: results/phase-1-summary.md` (Source: lines 839-848)
  - Notification stored in `SprintTUI.latest_summary_notification: str | None` (Source: line 845)
- **Dependencies:** Requires F8 (SummaryWorker), tmux.py 3-pane layout changes

### F10: Release Retrospective

- **Purpose:** After all phases complete, generate a release-level synthesis aggregating all phase summaries with cross-phase analysis and a Haiku narrative.
- **User value:** Provides a single document summarizing the entire sprint execution -- ready for review, archiving, or sharing.
- **Data sources:** All `phase-N-summary.md` files (Source: line 408)
- **Implementation approach:**
  - **Execution model:** Blocking -- runs before terminal panel display (Source: line 407)
  - **Step 1:** Read all phase summaries (Source: line 408)
  - **Step 2:** Programmatic aggregation: total stats, combined file list, combined validation matrix, combined errors, cross-phase patterns (Source: lines 482-488)
  - **Step 3:** Haiku narrative (4-8 sentences) (Source: lines 490-506)
  - **Step 4:** Write `results/release-retrospective.md` (Source: line 418)
  - **Step 5:** Display in terminal panel and/or summary pane (Source: line 420)
  - **Cross-phase analysis:** Files modified in multiple phases, error patterns, validation coverage gaps, timing trends (Source: lines 484-488)
  - **New module:** `retrospective.py` with `ReleaseRetrospective` dataclass and `RetrospectiveGenerator` class (Source: lines 620-694)
- **Dependencies:** Requires F8 (phase summaries must exist), `claude` binary, executor integration

---

## 3. Architecture Changes

### New Modules

#### `summarizer.py` (Source: lines 510-618)

Contains three components:

1. **`PhaseSummary` dataclass** -- Structured summary of a completed phase:
   - `phase: Phase`, `phase_result: PhaseResult`
   - `tasks: list[dict]` -- `[{id, tier, status, description}]`
   - `files_changed: list[dict]` -- `[{action, path}]`
   - `validations: list[dict]` -- `[{task, method, command, result}]`
   - `reasoning_excerpts: list[str]` -- top 3-5 snippets
   - `errors: list[dict]` -- `[{task, tool, message}]`
   - `narrative: str` -- Haiku-generated, may be empty
   - Property: `summary_path -> Path` -- `results/phase-N-summary.md`

2. **`PhaseSummarizer` class** -- Orchestrates extraction + narrative:
   - `__init__(config: SprintConfig)`
   - `summarize(phase, phase_result) -> PhaseSummary` -- full pipeline
   - `_extract_structured(output_file, summary)` -- NDJSON parsing
   - `_generate_narrative(summary)` -- Haiku subprocess call
   - `_build_narrative_prompt(summary) -> str` -- prompt template
   - `_write_summary(summary)` -- markdown generation

3. **`SummaryWorker` class** (in `executor.py`, Source: lines 698-745) -- Background threading:
   - `__init__(config: SprintConfig)` -- creates PhaseSummarizer
   - `submit(phase, phase_result)` -- spawns daemon thread
   - `_run(phase, phase_result)` -- thread target, catches all exceptions
   - `wait_all(timeout=60)` -- join all threads
   - Property: `latest_summary_path -> Path | None`
   - Thread naming: `summary-phase-{phase.number}`
   - Thread storage: `_threads: list[threading.Thread]`, `_summaries: dict[int, PhaseSummary]`

#### `retrospective.py` (Source: lines 620-694)

Contains two components:

1. **`ReleaseRetrospective` dataclass**:
   - `sprint_result: SprintResult`
   - `phase_outcomes: list[dict]` -- `[{phase, name, duration, tasks, status, key_outcome}]`
   - `all_files: list[dict]` -- `[{phase, action, path}]`
   - `validation_matrix: list[dict]` -- `[{task, tier, method, command, result}]`
   - `all_errors: list[dict]`
   - `validation_coverage: str`
   - `narrative: str`

2. **`RetrospectiveGenerator` class**:
   - `__init__(config: SprintConfig)`
   - `generate(sprint_result) -> ReleaseRetrospective` -- full pipeline
   - `_read_phase_summaries() -> list[str]`
   - `_aggregate(summaries, retro)`
   - `_generate_narrative(retro)` -- same Haiku pattern as PhaseSummarizer
   - `_write_retrospective(retro)` -- writes to `config.results_dir / "release-retrospective.md"`

### SummaryWorker Threading Model

- **Pattern:** Submit-and-forget with background daemon threads
- **Concurrency:** One thread per completed phase, running in parallel with the next phase's execution
- **Safety:** Exception handling wraps entire thread body -- summary failure never affects sprint execution (Source: line 731)
- **Synchronization:** `wait_all(timeout=60)` called after sprint loop exits, before retrospective generation (Source: line 755)
- **Tmux notification:** Thread calls `update_summary_pane()` after writing summary file (Source: lines 728-729)
- **Thread lifecycle:** Daemon threads (`daemon=True`) so they don't block process exit on crash (Source: line 717)

### Haiku Narrative Generation Pipeline

Both `PhaseSummarizer` and `RetrospectiveGenerator` follow the same pattern:

1. Check `shutil.which("claude")` is not None (Source: line 583)
2. Build prompt from structured data
3. Strip CLAUDECODE and CLAUDE_CODE_ENTRYPOINT from environment (Source: lines 588-589)
4. Run: `claude --print --model claude-haiku-4-5 --max-turns 1 --dangerously-skip-permissions -p "<prompt>"` (Source: lines 594-600)
5. Timeout: 30s (Source: line 604)
6. On failure: silently swallow exception, summary written without narrative (Source: lines 607-609)

---

## 4. Data Model Changes

### MonitorState -- New Fields (Source: lines 855-879)

| Field | Type | Default | Feature | Description |
|-------|------|---------|---------|-------------|
| `activity_log` | `list[tuple[float, str, str]]` | `[]` | F1 | (timestamp, tool_name, description), max 3 |
| `turns` | `int` | `0` | F2 | Count of assistant message events for current phase |
| `errors` | `list[tuple[str, str, str]]` | `[]` | F4 | (task_id, tool_name, message), max 10 |
| `last_assistant_text` | `str` | `""` | F5 | Last ~80 chars of assistant text output |
| `total_tasks_in_phase` | `int` | `0` | F3 | Task count in current phase file |
| `completed_task_estimate` | `int` | `0` | F3 | Estimated completed tasks |
| `tokens_in` | `int` | `0` | F6 | Accumulated input tokens in current phase |
| `tokens_out` | `int` | `0` | F6 | Accumulated output tokens in current phase |

### PhaseResult -- New Fields (Source: lines 885-889)

| Field | Type | Default | Feature | Description |
|-------|------|---------|---------|-------------|
| `turns` | `int` | `0` | F2/F6 | Total assistant turns in this phase |
| `tokens_in` | `int` | `0` | F6 | Total input tokens consumed |
| `tokens_out` | `int` | `0` | F6 | Total output tokens consumed |

**Note:** `output_bytes` and `files_changed` already exist on PhaseResult (confirmed in current codebase, line 446).

### SprintResult -- New Aggregate Properties (Source: lines 895-914)

| Property | Return Type | Computation |
|----------|-------------|-------------|
| `total_turns` | `int` | `sum(r.turns for r in self.phase_results)` |
| `total_tokens_in` | `int` | `sum(r.tokens_in for r in self.phase_results)` |
| `total_tokens_out` | `int` | `sum(r.tokens_out for r in self.phase_results)` |
| `total_output_bytes` | `int` | `sum(r.output_bytes for r in self.phase_results)` |
| `total_files_changed` | `int` | `sum(r.files_changed for r in self.phase_results)` |

### SprintConfig -- New Field (Source: line 919)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `total_tasks` | `int` | `0` | Pre-scanned total task count across all phase files |

### SprintTUI -- New Field (Source: line 845)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `latest_summary_notification` | `str \| None` | `None` | Notification for --no-tmux mode |

---

## 5. UI Layout Specifications

### Layout 1: Active Sprint (~25 lines) (Source: lines 19-51)

```
+=========== SUPERCLAUDE SPRINT RUNNER == {release_name} ===========+
|                                                                    |
|  Elapsed: 12m 34s    Model: claude-opus-4-6    Turns: 23/50       |
|                                                                    |
|  #  Phase                            Status   Duration  Turns  Out |
|  1  Foundation & Architecture        PASS     16s       7     10KB |
|  2  Command & Skill Implementation   RUNNING  2m 34s    23   148KB |
|  3  Integration & Tooling            pending  -         -      -   |
|  4  Validation & Acceptance          pending  -         -      -   |
|                                                                    |
|  Phases ======-------- 25% 1/4    Tasks ==========------ 51% 20/39|
|                                                                    |
|  +---- ACTIVE: phase-2-tasklist.md --------------------------------+
|  | Status:  RUNNING -- active (+312.5 B/s)                         |
|  | Task:    T02.08   Tool: Bash   Files: 3                         |
|  |                                                                  |
|  | Prompt:  Execute all tasks in phase-2-tasklist.md --compliance...|
|  | Agent:   Good -- the directory doesn't exist yet, and there's...|
|  |                                                                  |
|  |  02:53:42  Grep  pyproject.toml (packages config)               |
|  |  02:53:43  Write sc-tasklist-protocol/SKILL.md                  |
|  |  02:53:46  Todo  updated 5 tasks                                |
|  +------------------------------------------------------------------+
|                                                                    |
|  +---- ERRORS (2) --------------------------------------------------+
|  |  T02.04  Bash  exit 1 -- "mkdir: permission denied"             |
|  |  T02.07  STRICT verification failed                             |
|  +------------------------------------------------------------------+
+--------------------------------------------------------------------+
```

**Key field placements:**
- **Outer panel title:** Release name appended with `==`
- **Header:** Elapsed + Model + Turns/MaxTurns (release name removed, moved to title)
- **Phase table:** 6 columns (#, Phase, Status, Duration, Turns, Output)
- **Dual progress bar:** Single line, two bars with block characters
- **Active panel title:** `ACTIVE: {phase_filename}`
- **Active panel body:** Status line, Task/Tool/Files line, blank, Prompt line, Agent line, blank, 3 activity lines
- **Error panel:** Conditional, red border, below active panel

### Layout 2: Sprint Complete (Source: lines 53-79)

- Phase table shows all phases with PASS status, turns, and output
- Dual progress bars at 100%
- Terminal panel titled `SPRINT COMPLETE` with:
  - Result: ALL PHASES PASSED
  - Duration, Turns (total + avg/phase), Tokens (in/out), Output, Files, Log path

### Layout 3: Sprint Halted (Source: lines 83-113)

- Phase table shows completed + HALT + skipped phases
- Dual progress bars at partial completion
- Terminal panel titled `SPRINT HALTED -- Phase N` with:
  - Result, Duration, Completed (phases + tasks), Turns, Tokens
  - Last task + failure reason
  - Files changed
  - Errors section (folded in, same format as error panel)
  - Resume command
  - Log path

---

## 6. Tmux Integration

### 3-Pane Layout (Source: lines 766-810)

```
+---------------------------------------------------+
|  SUPERCLAUDE SPRINT RUNNER (Rich TUI dashboard)   |  <-- 50%
|  Phase table, progress bars, active panel...      |
+---------------------------------------------------+
|  Phase 1 Summary                                  |  <-- 25% (summary pane)
|  Tasks: 4/4 DONE | Files: 5 new                  |
|  Validation: 3 checks passed                      |
|  "Scaffolded directory tree using existing..."    |
+---------------------------------------------------+
|  tail -f phase-2-output.txt                       |  <-- 25% (output tail)
+---------------------------------------------------+
```

**Creation sequence** (Source: lines 770-809):
1. `tmux new-session -d -s {name} -x 120 -y 40 {sprint_cmd}` -- TUI pane (100%)
2. `tmux split-window -t {name} -v -p 50` -- Summary pane (50% of remaining = bottom half)
   - Runs: `echo 'Waiting for first phase to complete...'; read`
3. `tmux split-window -t {name}:0.1 -v -p 50` -- Tail pane (50% of remaining = 25% total)
   - Runs: `touch {output_file} && tail -f {output_file}; read`
4. `tmux select-pane -t {name}:0.0` -- Focus on TUI pane

### Summary Pane Management (Source: lines 814-829)

**Update function:** `update_summary_pane(tmux_session_name, summary_path)`
1. Send `C-c` to `{session}:0.1` to interrupt current content
2. Send `clear && cat {summary_path} && echo '--- Ctrl-B z to zoom/unzoom ---'` to `{session}:0.1`

### Pane Index Changes (Source: line 833)

| Component | Current Index | New Index |
|-----------|---------------|-----------|
| TUI pane | `:0.0` | `:0.0` (unchanged) |
| Summary pane | N/A | `:0.1` (new) |
| Tail pane | `:0.1` | `:0.2` |

**Critical:** `update_tail_pane()` function must update its pane index from `:0.1` to `:0.2`. This is a breaking change -- currently hardcoded as `f"{tmux_session_name}:0.1"` in `tmux.py` lines 160 and 169.

---

## 7. File Inventory

### Modified Files (5)

| File | Current Path | Changes Required |
|------|-------------|------------------|
| `models.py` | `src/superclaude/cli/sprint/models.py` | Add fields: MonitorState (8 new), PhaseResult (3 new), SprintResult (5 new properties), SprintConfig (1 new). Add SprintTUI notification field. |
| `monitor.py` | `src/superclaude/cli/sprint/monitor.py` | Add to `_extract_signals_from_event()`: turn counting (F2), token tracking (F6), activity log (F1), error detection (F4), assistant text extraction (F5). Add `count_tasks_in_file()` static method. Add pre-scan in `reset()`. |
| `tui.py` | `src/superclaude/cli/sprint/tui.py` | Rewrite `_render()` layout. Modify `_build_header()` (remove release name, add turns). Modify `_build_phase_table()` (add Turns/Output columns, remove Tasks). Replace `_build_progress()` with `_build_dual_progress()`. Enhance `_build_active_panel()` (activity stream, LLM context). Add `_build_error_panel()`. Enhance `_build_terminal_panel()`. Add `_mini_bar()` helper. |
| `executor.py` | `src/superclaude/cli/sprint/executor.py` | Integrate SummaryWorker: instantiate at sprint start, `submit()` after each phase, `wait_all()` before retrospective. Integrate RetrospectiveGenerator: blocking call after all phases. Pass new PhaseResult fields (turns, tokens). Add TUI notification for --no-tmux mode. |
| `tmux.py` | `src/superclaude/cli/sprint/tmux.py` | Change `launch_in_tmux()` to 3-pane layout. Add `update_summary_pane()` function. Update `update_tail_pane()` pane index from `:0.1` to `:0.2`. |

### New Files (2)

| File | Target Path | Purpose |
|------|------------|---------|
| `summarizer.py` | `src/superclaude/cli/sprint/summarizer.py` | `PhaseSummary` dataclass, `PhaseSummarizer` class (NDJSON extraction + Haiku narrative) |
| `retrospective.py` | `src/superclaude/cli/sprint/retrospective.py` | `ReleaseRetrospective` dataclass, `RetrospectiveGenerator` class (aggregation + Haiku narrative) |

### Output Artifacts (per sprint)

| File | When Written | Writer |
|------|-------------|--------|
| `results/phase-N-summary.md` | After each phase completes (background thread) | SummaryWorker via PhaseSummarizer |
| `results/release-retrospective.md` | After all phases complete (blocking) | RetrospectiveGenerator |

---

## 8. Test Impact

### Existing Tests Requiring Updates (Source: lines 1140-1148)

| Test File | Changes Needed |
|-----------|---------------|
| `tests/sprint/test_tui.py` | New column assertions in phase table, new MonitorState fields in fixtures, new terminal panel content, new `_build_dual_progress()` and `_build_error_panel()` method tests, summary notification display |
| `tests/sprint/test_models.py` | New fields on MonitorState, PhaseResult, SprintResult aggregate properties, SprintConfig.total_tasks |
| `tests/sprint/test_tui_gate_column.py` | Phase table column assertions may need adjustment (Tasks column removed, Turns/Output added) |
| `tests/sprint/test_tui_monitor.py` | Monitor state assertions may need updating for new fields |
| `tests/sprint/test_tui_task_updates.py` | Task progress display changes |

### New Tests Required (Source: lines 1144-1148)

| Test File | Scope |
|-----------|-------|
| `tests/sprint/test_summarizer.py` | PhaseSummarizer programmatic extraction from NDJSON fixtures, narrative prompt building, summary markdown generation, SummaryWorker background execution and thread safety |
| `tests/sprint/test_retrospective.py` | RetrospectiveGenerator aggregation from phase summaries, narrative prompt building, retrospective markdown generation |
| `tests/sprint/test_tmux.py` | 3-pane layout creation, summary pane updates, pane index handling |

### Tests Confirmed Unchanged (Source: lines 1149-1150)

- `test_cli_contract.py`
- `test_config.py` (beyond total_tasks)
- `test_process.py`
- `test_e2e_*.py`

---

## 9. Out of Scope Items (Source: lines 1100-1109)

These features are explicitly deferred to future PRs:

1. `--compact` CLI flag to show current minimal layout
2. Cost tracking / cache hit ratio display
3. MCP server health indicators
4. ETA estimation
5. `sprint status` and `sprint logs` command implementations (currently stubs)
6. Modal overlay for summary viewing in `--no-tmux` mode (keyboard input)
7. Configurable summary model (currently hardcoded to Haiku)
8. Interactive summary navigation (viewing older phase summaries)

---

## 10. Dependencies on Other Work

### Checkpoint Enforcement (v3.7 prerequisite)

The spec references PASS_MISSING_CHECKPOINT status display indirectly through the existing `PhaseStatus` enum. The current codebase already has:
- `PhaseStatus.PASS_NO_SIGNAL` -- agent wrote result file but no EXIT_RECOMMENDATION
- `PhaseStatus.PASS_NO_REPORT` -- no result file written
- `PhaseStatus.PASS_RECOVERED` -- non-zero exit but checkpoint evidence

**LOW CONFIDENCE:** The requirements spec does not explicitly mention `PASS_MISSING_CHECKPOINT` as a new status. However, the checkpoint enforcement work in v3.7-task-unified-v2 may introduce this status. The TUI's `STATUS_STYLES` and `STATUS_ICONS` dicts (tui.py lines 28-56) would need entries for any new PhaseStatus values. This is an implicit dependency not documented in the spec.

### Existing Gate Infrastructure

The TUI already has a gate column system (`GateDisplayState`, `_show_gate_column`). The TUI v2 changes must preserve this existing gate column functionality. The spec's phase table changes (removing Tasks column, adding Turns/Output) must account for the conditional gate column.

### `ClaudeProcess.build_prompt()`

F5 (LLM Context Lines) references `ClaudeProcess.build_prompt()` for the static prompt preview (Source: line 197). This method must expose a way to get the prompt text for the `prompt_preview` field. The current `process.py` module was not included in the spec's modification list, which may be an oversight -- or the prompt may be computed at a higher level (executor/config).

---

## 11. Implementation Complexity Assessment

### Per-Feature Assessment

| Feature | Effort | Risk | Rationale |
|---------|--------|------|-----------|
| F7: Sprint Name in Title | Trivial | None | One-line change to Panel title, release name already computed |
| F2: Enhanced Phase Table | Low | Low | Add/remove columns in existing table builder, straightforward |
| F5: LLM Context Lines | Low | Low | Two text lines in active panel, monitor extraction is simple |
| F1: Activity Stream | Medium | Low | Ring buffer logic, tool name shortening, thinking indicator timer |
| F4: Conditional Error Panel | Medium | Low | New panel method, error detection in monitor, visibility toggle |
| F3: Task-Level Progress | Medium | Medium | Pre-scan task counting, ordinal estimation from task ID, dual bar rendering |
| F6: Enhanced Terminal Panels | Medium | Low | More content in existing panels, requires aggregate properties to work |
| F9: Tmux Summary Pane | Medium | Medium | 3-pane layout change, pane index migration, update mechanism |
| F8: Post-Phase Summary | High | High | New module, NDJSON parsing, Haiku subprocess, background threading, failure handling |
| F10: Release Retrospective | High | Medium | New module, cross-phase aggregation, Haiku subprocess, blocking before terminal |

### Suggested Wave/Phase Ordering

**Wave 1: Data Model + Monitor (Foundation)**
- F2 monitor extraction (turns), F5 monitor extraction (assistant text), F4 monitor extraction (errors), F1 monitor extraction (activity log), F6 monitor extraction (tokens)
- All MonitorState/PhaseResult/SprintResult/SprintConfig model additions
- Rationale: All TUI features depend on the data model and monitor extraction layer

**Wave 2: TUI Rendering (Display)**
- F7 (title), F2 (table columns), F3 (dual progress), F5 (context lines), F1 (activity stream), F4 (error panel), F6 (terminal panels)
- Rationale: All rendering changes can be developed and tested once data flows are established

**Wave 3: Summary Infrastructure (New Modules)**
- F8 (summarizer.py + SummaryWorker)
- F10 (retrospective.py + RetrospectiveGenerator)
- Executor integration
- Rationale: New modules with subprocess dependencies; can be developed in parallel with Wave 2

**Wave 4: Tmux Integration**
- F9 (3-pane layout, summary pane management, pane index migration)
- Rationale: Depends on Wave 3 (summary files must exist for the pane to display them)

---

## 12. Open Questions / Gaps

### Gap 1: `prompt_preview` Field Location (Medium Severity)

F5 specifies that the static phase prompt should come from `ClaudeProcess.build_prompt()` and be stored in either `SprintConfig` or `Phase` object (Source: line 205: "add a `prompt_preview: str` field to `Phase` or compute from config"). The spec does not specify which approach to use and `process.py` is not in the modified files list. The prompt text must be made available to the TUI without adding `process.py` as a dependency of `tui.py`.

### Gap 2: Task Completion Estimation Accuracy (Low Severity)

F3 estimates completed tasks from `MonitorState.last_task_id` by parsing the `TT` suffix as an ordinal position (Source: lines 160-161). This is explicitly labeled an estimate (`SprintResult.tasks_completed_estimate`). The accuracy depends on tasks being numbered sequentially and the agent working on them in order. Out-of-order execution or re-attempted tasks would produce inaccurate counts. The spec acknowledges this is an estimate but does not define acceptable accuracy bounds.

### Gap 3: SummaryWorker Thread Safety for `_summaries` Dict (Medium Severity)

The `SummaryWorker._summaries` dict is written by background threads and read by `latest_summary_path` property (Source: lines 709, 738-741). No explicit locking mechanism is shown in the spec code. Python's GIL provides some protection for dict operations, but the spec should document the concurrency model explicitly. Multiple threads writing to the dict simultaneously could produce unexpected behavior if the GIL is released during the operation.

### Gap 4: Monitor Reset Does Not Clear New Fields (Medium Severity)

The current `monitor.py` `reset()` method (line 186) creates a new `MonitorState()`, which will correctly default-initialize the new fields. However, the spec's `reset()` also needs to call `count_tasks_in_file()` to set `total_tasks_in_phase` (Source: line 976). This is mentioned in the spec but the exact integration point is not shown -- only "Called during `reset()` to set `self.state.total_tasks_in_phase`." The reset method would need the phase file path, which it currently does not receive.

### Gap 5: `_format_tokens()` Helper Location (Trivial)

The token display format helper (Source: lines 1089-1096) is defined as a standalone function but the spec does not specify which module it belongs to. Likely candidates: `tui.py` (private helper) or `models.py` (shared utility).

### Gap 6: Error Panel Task ID Extraction (Low Severity)

F4 specifies "Task ID extracted from context if available, otherwise `-`" (Source: line 181) but does not define the specific extraction logic for associating an error with a task ID. The monitor would need to track which task ID was most recently mentioned before each error event.

### Gap 7: Haiku Model Availability Assumption (Low Severity)

Both F8 and F10 assume `claude-haiku-4-5` is available via `claude --print`. If the user's Claude installation does not support this model, or if API rate limits are hit, the narrative will silently fail. The spec handles this gracefully (summary without narrative), but there is no user notification that narrative generation failed.

### Gap 8: Phase Prompt Preview for Per-Task Execution Mode (Low Severity)

The spec's F5 assumes single-prompt-per-phase execution, but the current codebase supports per-task execution via `execute_phase_tasks()` (executor.py line 912). In per-task mode, each task has its own prompt. The spec does not address which prompt to show in the `Prompt:` line for per-task phases.

### Gap 9: Interaction with Existing Gate Column (Low Severity)

The current TUI has a conditional gate column (`self._show_gate_column`, tui.py line 73). The spec's phase table changes (remove Tasks, add Turns/Output) do not mention the gate column. The implementation must ensure the gate column remains functional alongside the new columns.

### Gap 10: `config.py` Pre-Scan Integration (Low Severity)

The spec states task pre-scanning should happen in `config.py` `load_sprint_config()` (Source: lines 980-983), but `config.py` is not listed in the modified files inventory (Source: lines 1115-1128). This is either an oversight in the file inventory or the pre-scan should be placed elsewhere.
