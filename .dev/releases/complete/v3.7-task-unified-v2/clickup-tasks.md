# ClickUp Task Plan — v3.7 task-unified-v2

Paste-ready structure: **1 parent task + 10 phase subtasks**. Phase ordering follows Section 6.2 "Recommended Implementation Order" of `v3.7-UNIFIED-RELEASE-SPEC-merged.md`, with a new **Phase 0** for pipeline discovery added per request.

Source spec: `.dev/releases/backlog/v3.7-task-unified-v2/v3.7-UNIFIED-RELEASE-SPEC-merged.md`

---

## PARENT TASK

### Title
v3.7 task-unified-v2 — Checkpoint Enforcement, Sprint TUI v2, Naming Consolidation

### Description
Deliver three interconnected improvements to the Sprint CLI pipeline in a single coordinated release:

1. **Checkpoint Enforcement** — Three-layer defense (Prevention → Detection → Remediation) so checkpoint files are always written during sprint execution. Closes the OntRAG R0+R1 triple-failure chain where Phase 3 passed but wrote neither checkpoint file.
2. **Sprint TUI v2** — Visual UX overhaul surfacing rich stream-json telemetry: activity stream, enhanced phase table, dual progress bars, conditional error panel, LLM context preview, post-phase Haiku summaries, tmux summary pane, and release retrospective.
3. **Naming Consolidation** — Resolve the three-layer collision between `/sc:task`, `task-unified.md`, and `sc:task-unified-protocol`. Canonicalize on `/sc:task`.

**Total scope**: ~1,480+ LOC across ~15 files (3 new). Rollout is gated: Checkpoint gate ships in `shadow` mode by default and progresses to `soft` then `full` after 2 clean sprint cycles.

**Domain conflicts** (see Section 8.4 of the spec):
- `executor.py` — Checkpoint W1–W3 + TUI SummaryWorker (order: Checkpoint → TUI)
- `process.py` — Checkpoint W1 + Naming N5 (order: Naming → Checkpoint, both touch `build_prompt()`)
- `models.py` — Checkpoint W2–W3 + TUI all waves (additive, different sections)
- `SKILL.md` (tasklist) — Naming N7 + Checkpoint W4 (order: Naming → Checkpoint)

### Acceptance Criteria
- [ ] All 10 phase subtasks are complete (or Phase 9 explicitly deferred to next release cycle per spec)
- [ ] Checkpoint write rate is 100% (Section 11.1 target, measured via Wave 2 JSONL `checkpoint_verification` events)
- [ ] Checkpoint gate mode reaches at least `soft` in the rollout window; `full` targeted for Sprint +2
- [ ] `/sc:task` resolves to the unified command; `/sc:task-unified` fully removed from live source (`src/superclaude/`, `.claude/`)
- [ ] `make verify-sync` passes (src/ and .claude/ in sync)
- [ ] All existing sprint tests pass; new tests added per Section 12.2 pass with coverage targets in Section 12.4 met (>90% `checkpoints.py`, >80% `summarizer.py`/`retrospective.py`)
- [ ] Release retrospective (`results/release-retrospective.md`) generated automatically at sprint end
- [ ] `superclaude sprint verify-checkpoints <dir>` works retroactively on OntRAG R0+R1 sprint output and recovers the missing P03 checkpoint with `--recover`
- [ ] Zero regressions in existing TUI rendering tests

---

## SUBTASK — Phase 0 — Sprint CLI Pipeline Deep-Dive (Discovery, NEW)

### Description
Pre-implementation reading phase. Build a deep mental model of the Sprint CLI pipeline before any code changes, because every subsequent phase modifies core pipeline files (`process.py`, `executor.py`, `models.py`, `monitor.py`, `tui.py`, `tmux.py`, `logging_.py`, `commands.py`, `config.py`). Without this grounding the work risks mis-wiring hook points, missing cross-cutting invariants (e.g., the `PASS_MISSING_CHECKPOINT` / TUI rendering dependency in Section 5.1), and duplicating logic across Checkpoint and TUI streams.

**Reading / exploration scope:**
- `src/superclaude/cli/sprint/` — full module tour: `executor.py`, `process.py`, `monitor.py`, `tui.py`, `tmux.py`, `models.py`, `logging_.py`, `commands.py`, `config.py`
- Phase completion flow: `execute_phase()` → `determine_phase_status()` → `_check_checkpoint_pass()` (existing, crash-recovery only) → phase advance
- `build_prompt()` in `process.py` (lines ~169–203) — the `/sc:task-unified` hardcoded prompt string; the `## Scope Boundary` / `## Result File` sections that Checkpoint W1 extends
- MonitorState event extraction (`_extract_signals_from_event()`) — understand which stream-json event types carry turn counts, token counts, assistant text, tool_use, tool_result, is_error
- Tmux pane model in `tmux.py` — current 2-pane (`:0.0` TUI 75% + `:0.1` tail 25%); hardcoded pane indexes that shift under F9
- Existing `PhaseStatus` enum members and `is_failure` semantics (new `PASS_MISSING_CHECKPOINT` joins `PASS_NO_SIGNAL`, `PASS_NO_REPORT`, `PASS_RECOVERED`)
- Checkpoint-related artifacts from the OntRAG R0+R1 sprint: `.dev/releases/current/feature-Ont-RAG/feature-OntRAG_r0-r1/checkpoints/CP-P*.md` — checkpoint file format, frontmatter, verification sections (context for Wave 3 auto-recovery)
- Appendix C "Codebase Integration Map" in the spec
- Source analysis documents referenced in Appendix D

**No artifacts produced.** This phase is read-only understanding. Outputs live in the implementer's head and get applied directly in Phases 1–8.

### Acceptance Criteria
- [ ] Implementer can describe the end-to-end phase completion flow without re-reading the code: `ClaudeProcess` subprocess → `build_prompt()` → Claude subprocess → `determine_phase_status()` → (future) checkpoint verification → (future) summary worker → next phase
- [ ] Implementer knows where in `executor.py` each new call site will go: `_warn_missing_checkpoints()` (T01.02), `_verify_checkpoints()` (T02.04), `summary_worker.submit()` (TUI Wave 3), `build_manifest()` at sprint start + end (T03.05) — and the ordering constraint from Section 6.4
- [ ] Implementer understands the `PASS_MISSING_CHECKPOINT` / TUI rendering cross-dependency (Section 5.1) and why Phase 4 must stub the status before Phase 5 can ship
- [ ] Implementer has read enough of the OntRAG R0+R1 checkpoint files to design the T03.03 auto-recovery template confidently
- [ ] Priority=Medium open questions in Section 14 (CE-Q2, CE-Q4, TUI-Q1, TUI-Q4, NC-Q1, NC-Q4) have been read and have a mental answer or an explicit "resolve during Phase N" parking
- [ ] No code changes made in this phase — read-only

---

## SUBTASK — Phase 1 — Naming Consolidation

### Description
Mechanical rename of the command/skill layer to canonicalize `/sc:task`. Done first (per Section 6.2) because it reduces noise in every subsequent diff — most other phases touch `process.py` and `tasklist-protocol/SKILL.md`.

**Work items** (Section 4.3 tasks N1–N12):
- N1: Delete deprecated legacy `task.md` / `task-legacy` files (src/ + .claude/)
- N2: Rename `src/superclaude/commands/task-unified.md` → `task.md` (frontmatter `name: task` unchanged)
- N3: Rename `src/superclaude/skills/sc-task-unified-protocol/` → `sc-task-protocol/`
- N4: Update skill frontmatter `name: sc:task-unified-protocol` → `sc:task-protocol`
- N5: `src/superclaude/cli/sprint/process.py:170` — `/sc:task-unified` → `/sc:task`
- N6: `src/superclaude/cli/cleanup_audit/prompts.py` — 5 prompt builders
- N7: `sc-tasklist-protocol/SKILL.md` — 12 references
- N8: `tasklist.md` (8), `help.md` (2), other commands
- N9: `sc-roadmap-protocol`, `sc-cli-portify-protocol`, `sc-validate-tests-protocol`, `sc-release-split-protocol`
- N10: Core docs — `COMMANDS.md`, `ORCHESTRATOR.md`
- N11: `make sync-dev` + `make verify-sync`
- N12: Confirm/clean up `task-mcp.md`

**Dependency order (parallel-aware):** N1 → N2 → N3 → N4 → (N5 ‖ N6) → (N7 ‖ N8 ‖ N9 ‖ N10) → N11

**Risks** (Section 10.3): NC-1 missed reference in obscure file — mitigate with comprehensive grep; NC-2 Claude Code command resolution ambiguity — test `/sc:task` resolution after rename; NC-3 classification header `SC:TASK-UNIFIED:CLASSIFICATION` stability; NC-4 `task-mcp.md` cleanup.

### Acceptance Criteria
- [ ] All 3 "naming variants in live source" collapsed to 2 (`task`, `task-protocol`) — verified by `grep -rn "task-unified" src/superclaude/ .claude/ | wc -l` returning 0 live-source hits
- [ ] `src/superclaude/commands/task.md` exists with frontmatter `name: task`; legacy `task-legacy` file deleted
- [ ] `src/superclaude/skills/sc-task-protocol/SKILL.md` exists with frontmatter `name: sc:task-protocol`
- [ ] `src/superclaude/cli/sprint/process.py` line ~170 emits `/sc:task`
- [ ] All 5 prompt builders in `cli/cleanup_audit/prompts.py` emit `/sc:task`
- [ ] `sc-tasklist-protocol/SKILL.md` has 0 remaining `sc:task-unified` references
- [ ] `make verify-sync` passes — `src/` and `.claude/` are identical
- [ ] Smoke test: run a minimal sprint — `/sc:task` resolves correctly, subprocess prompt is well-formed
- [ ] `task-mcp.md` deprecation status confirmed or file removed (NC-4)
- [ ] Historical artifacts in `.dev/releases/complete/` intentionally NOT updated (archival)

---

## SUBTASK — Phase 2 — Checkpoint Wave 1: Prompt-Level Enforcement

### Description
Transform checkpoint writing from emergent to instructed behavior. This is the single highest-value, lowest-risk Checkpoint change — ~60 LOC, ships in 1 day. Addresses Cause 1 (primary root cause) from the triple-failure chain.

**Tasks** (Section 4.1 Phase 1):
- **T01.01** — Add `## Checkpoints` section to `build_prompt()` in `src/superclaude/cli/sprint/process.py`. 5-line instruction block placed between task execution and `## Scope Boundary`. Amend `## Scope Boundary` to "After completing all tasks AND writing all checkpoint reports, STOP immediately". Amend `## Result File` to require result file written after checkpoints. Confidence: 95%.
- **T01.02** — Add `_warn_missing_checkpoints(phase_file, checkpoints_dir, phase_number) -> list[str]` to `src/superclaude/cli/sprint/executor.py`. Parses `Checkpoint Report Path:` from phase tasklist, checks file existence, logs `logger.warning()` for missing. Called after `determine_phase_status()` returns PASS. **Warning-only — does NOT modify phase status.** Confidence: 90%.

**Cross-wave dependency:** T02.04 in Phase 5 will REPLACE this function with the full `_verify_checkpoints()` gate. Phase 1's warning is interim coverage. Per Section 4.1 rollback note: if Wave 2 is reverted, manually re-apply T01.02.

**Integration with Naming:** Phase 1 (Naming) must ship first — both touch `build_prompt()`.

### Acceptance Criteria
- [ ] `build_prompt()` output contains `## Checkpoints` section with 5 instruction lines (scan phase file for `### Checkpoint:` sections, extract path, write structured report, write checkpoints BEFORE result file, skip if no checkpoints)
- [ ] `## Scope Boundary` mentions checkpoint reports
- [ ] `## Result File` mentions writing after checkpoints
- [ ] `_warn_missing_checkpoints()` exists in `executor.py`, parses `Checkpoint Report Path:`, checks existence, logs `logger.warning()` per missing file
- [ ] Function called after phase PASS determination; does NOT modify `PhaseStatus`
- [ ] Both `process.py` and `executor.py` load without error
- [ ] No regressions in existing sprint tests (`test_process.py`, `test_executor.py`, `test_tui.py`)
- [ ] Manual verification: dry-run `build_prompt()` output shows checkpoint section

---

## SUBTASK — Phase 3 — TUI v2 Wave 1: Data Model + Monitor Extraction

### Description
Foundation wave for all TUI features. Extend data models and extract rich telemetry from stream-json events. All subsequent TUI waves depend on this layer (Section 4.2 rationale).

**Data model changes** (`src/superclaude/cli/sprint/models.py`, Section 7):
- **MonitorState** (8 new fields): `activity_log: list[tuple[float, str, str]]` (F1, max 3), `turns: int` (F2), `errors: list[tuple[str, str, str]]` (F4, max 10), `last_assistant_text: str` (F5), `total_tasks_in_phase: int` (F3), `completed_task_estimate: int` (F3), `tokens_in: int` (F6), `tokens_out: int` (F6)
- **PhaseResult** (3 new fields): `turns`, `tokens_in`, `tokens_out`
- **SprintResult** (5 new aggregate properties): `total_turns`, `total_tokens_in`, `total_tokens_out`, `total_output_bytes`, `total_files_changed`
- **SprintConfig** (1 new): `total_tasks: int = 0` (pre-scanned task count across all phase files)

**Monitor extraction** (`src/superclaude/cli/sprint/monitor.py`) — `_extract_signals_from_event()`:
- F2: Turn counting (assistant message events)
- F5: Assistant text extraction (last ~80 chars)
- F4: Error detection (`tool_result` with `is_error: true`, Bash `exit_code != 0`)
- F1: Activity log from `tool_use` events — format `HH:MM:SS  ToolName  condensed_input`; shorten `TodoWrite`→`Todo`, `ToolSearch`→`Search`, `MultiEdit`→`Multi`
- F6: Token tracking (input/output accumulation)

**Pre-scan**: `T\d{2}\.\d{2}` regex across all phase files at sprint start → `SprintConfig.total_tasks`. Open question TUI-Q10: pre-scan should live in `load_sprint_config()` but `config.py` not in the spec's modified-files list — resolve during this phase.

**Open question TUI-Q4**: `Monitor.reset()` currently doesn't receive the phase file path but F3 needs `count_tasks_in_file()`. Requires interface change to `reset()`.

### Acceptance Criteria
- [ ] All 8 new `MonitorState` fields added with defaults that preserve existing behavior
- [ ] All 3 new `PhaseResult` fields added with `0` defaults
- [ ] All 5 new `SprintResult` properties computed correctly (sums across `phase_results`)
- [ ] `SprintConfig.total_tasks` pre-scan runs at sprint start and populates correctly for OntRAG-scale fixture
- [ ] Monitor extracts turns, tokens in/out, assistant text, activity log entries, and errors from stream-json events — verified by `test_tui_monitor.py` fixtures
- [ ] Tool name shortening applied to activity log entries
- [ ] Error ring buffer capped at 10 stored
- [ ] Activity log ring buffer capped at 3 entries
- [ ] `Monitor.reset()` receives phase file path and counts tasks correctly (TUI-Q4 resolved)
- [ ] All existing tests pass; updated fixtures in `test_models.py` and `test_tui_monitor.py` cover new fields

---

## SUBTASK — Phase 4 — TUI v2 Wave 2: Rendering

### Description
Visible TUI refactor. Depends on Phase 3 data model. All features are additive to the rendering layer; existing tests should continue to pass.

**Features** (Section 4.2 Wave 2):
- **F7** (trivial): Sprint name in outer panel title — `SUPERCLAUDE SPRINT RUNNER == {release_name}`
- **F2** (TUI): Enhanced phase table — add `Turns` (width=6, right-aligned) and `Output` (width=8) columns; remove `Tasks` column (moves to active panel). Preserve `_show_gate_column` logic (TUI-Q9)
- **F3**: Dual progress bar — single `Text` line with two manual renders using `█` full / `░` light shade block chars. `Phases ========-------- 25% 1/4    Tasks ==========------ 51% 20/39`
- **F5** (TUI): LLM context lines in active panel — `Prompt: <~60 chars>...` (static per phase), `Agent: <~60 chars>...` (updates on assistant events)
- **F1** (TUI): Activity stream — 3-line ring buffer at bottom of active panel; `[thinking... Ns]` indicator after >2s idle
- **F4** (TUI): Conditional error panel — hidden when empty, red border, title `ERRORS (N)`, max 5 displayed with `(+N more)` overflow
- **F6** (TUI): Enhanced terminal panels — Success variant (Result, Duration, Turns total+avg, Tokens in/out, Output, Files, Log); Halt variant (adds Completed phases+tasks, Last task + failure reason, Errors folded in, Resume command). Token helper `_format_tokens(n)` with K/M suffixes — place in `tui.py` per Section 6.5.

**Cross-domain dependency (Section 5.1):** TUI's `STATUS_STYLES` and `STATUS_ICONS` dicts (`tui.py` lines 28–56) must include entries for `PASS_MISSING_CHECKPOINT` before Phase 5 ships, or the TUI crashes when the gate downgrades a phase. Add stubs now (yellow/amber styling, warning icon).

**Open question TUI-Q1**: `prompt_preview` field location — decide between `Phase`, `SprintConfig`, or higher-level computation. Resolve during this phase.

### Acceptance Criteria
- [ ] Phase table renders new `Turns` and `Output` columns; `Tasks` column removed
- [ ] `_show_gate_column` conditional still works alongside new columns (existing fixture `test_tui_gate_column.py` updated)
- [ ] Dual progress bar renders correctly with block characters
- [ ] Active panel shows `Prompt:` (static) and `Agent:` (live) lines
- [ ] Activity stream shows last 3 tool calls with shortened names and thinking indicator
- [ ] Error panel hidden when `len(errors) == 0`; renders with red border and overflow count when non-empty
- [ ] Success terminal panel shows all F6 fields with K/M token formatting
- [ ] Halt terminal panel shows Completed, Last task, Errors block, Resume command
- [ ] Outer panel title includes `{release_name}`
- [ ] `STATUS_STYLES`/`STATUS_ICONS` include `PASS_MISSING_CHECKPOINT` entry (TUI/Checkpoint cross-domain dependency)
- [ ] `prompt_preview` storage location decided and documented (TUI-Q1 resolved)
- [ ] All existing TUI tests pass; new assertions in `test_tui.py` cover each rendering change

---

## SUBTASK — Phase 5 — Checkpoint Wave 2: Post-Phase Gate (Shadow Mode)

### Description
Add executor-level checkpoint verification after each phase, deployed in `shadow` mode (data collection only, zero behavioral change). Addresses Cause 3 (pipeline gap).

**Tasks** (Section 4.1 Phase 2, ~120 LOC):
- **T02.01** — CREATE `src/superclaude/cli/sprint/checkpoints.py` with `extract_checkpoint_paths(phase_file, release_dir) -> list[tuple[str, Path]]` and `verify_checkpoint_files(paths) -> list[tuple[str, Path, bool]]`. Shared module (eliminates duplication between Wave 2 gate and Wave 3 manifest).
- **T02.02** — Add `PASS_MISSING_CHECKPOINT = "pass_missing_checkpoint"` to `PhaseStatus` enum in `models.py`. `is_failure` returns `False`. Add `checkpoint_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"` to `SprintConfig`. Grep for exhaustive `PhaseStatus` matches and handle the new variant everywhere.
- **T02.03** — Add `write_checkpoint_verification(phase, expected, found, missing)` method to `logging_.py`. Emits JSONL event `{"event": "checkpoint_verification", "phase": N, ...}`.
- **T02.04** — REPLACE Phase 2's `_warn_missing_checkpoints()` with `_verify_checkpoints()` in `executor.py`. Imports from `checkpoints.py`. Gate mode behavior per Section 13.2: `off` no-op, `shadow` JSONL only, `soft` JSONL + stdout warning, `full` JSONL + stdout + downgrade to `PASS_MISSING_CHECKPOINT`. **Shadow is default** — no behavioral change for existing users.
- **T02.05** — Unit tests `tests/sprint/test_checkpoints.py` (0/1/2 checkpoint fixtures for `extract_checkpoint_paths`, existing/missing for `verify_checkpoint_files`) + integration test for `PASS_MISSING_CHECKPOINT` status flow in `full` mode.

**Post-phase hook ordering** (Section 6.4): `_verify_checkpoints()` runs before `summary_worker.submit()`. Should complete within 5s (disk I/O only); log warning if exceeded but don't block summary worker.

**Cross-wave rollback note**: If this wave is reverted, manually re-apply T01.02's `_warn_missing_checkpoints()` to maintain checkpoint awareness.

### Acceptance Criteria
- [ ] `src/superclaude/cli/sprint/checkpoints.py` exists with `extract_checkpoint_paths()` and `verify_checkpoint_files()`
- [ ] `PASS_MISSING_CHECKPOINT` in `PhaseStatus` enum; `is_failure` returns `False`
- [ ] `SprintConfig.checkpoint_gate_mode` defaults to `"shadow"`
- [ ] `write_checkpoint_verification()` emits structured JSONL following existing logger patterns
- [ ] `_verify_checkpoints()` in `executor.py` replaces T01.02's warning function and wires into phase completion flow
- [ ] Shadow mode: JSONL event emitted, no status change, no stdout output — verified end-to-end with a test sprint
- [ ] `full` mode: status downgraded to `PASS_MISSING_CHECKPOINT` — verified via integration test
- [ ] `tests/sprint/test_checkpoints.py` covers 0/1/2 checkpoint scenarios
- [ ] Integration test validates `PASS_MISSING_CHECKPOINT` propagation through phase completion flow
- [ ] Handles edge cases: no checkpoint sections (empty list), relative paths, missing `release_dir`
- [ ] Gate completes within 5s budget on realistic phase; warning logged if exceeded (Section 6.4 invariant)
- [ ] All existing sprint tests pass
- [ ] Phase 4 TUI renders `PASS_MISSING_CHECKPOINT` without crashing

---

## SUBTASK — Phase 6 — TUI v2 Wave 3: Summary Infrastructure

### Description
Two new modules that generate post-phase summaries and a release retrospective using Claude Haiku narratives. Highest-risk TUI wave (F8 is rated High risk in Section 3.2).

**New modules:**

**`src/superclaude/cli/sprint/summarizer.py`** (CREATE):
- `PhaseSummary` dataclass — `phase`, `phase_result`, `tasks`, `files_changed`, `validations`, `reasoning_excerpts`, `errors`, `narrative`, property `summary_path -> Path`
- `PhaseSummarizer` class — orchestrates NDJSON extraction + Haiku narrative + markdown writing
- `SummaryWorker` class — background daemon thread pool, one thread per completed phase, runs in parallel with next phase execution. **Critical invariant (Section 3.2): `_summaries` dict MUST be guarded by `threading.Lock`** — unlike `OutputMonitor` (single writer), SummaryWorker has a thread pool with concurrent writers. Exception handling wraps entire thread body so summary failure never affects sprint execution.

**`src/superclaude/cli/sprint/retrospective.py`** (CREATE):
- `ReleaseRetrospective` dataclass — `sprint_result`, `phase_outcomes`, `all_files`, `validation_matrix`, `all_errors`, `validation_coverage`, `narrative`
- `RetrospectiveGenerator` class — reads all phase summaries, aggregates programmatically (cross-phase patterns: multi-phase file modifications, error patterns, validation gaps, timing trends), generates Haiku narrative (4–8 sentences), writes `results/release-retrospective.md`. **Blocking** — runs before terminal panel display.

**Haiku subprocess convention** (Section 6.3, used by both F8 and F10):
1. `shutil.which("claude")` is not None
2. Build prompt from structured data
3. Strip `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT` env vars (prevent recursive Claude Code)
4. Run: `claude --print --model claude-haiku-4-5 --max-turns 1 --dangerously-skip-permissions -p "<prompt>"` with stdin=DEVNULL
5. Timeout: 30s
6. On failure: silently swallow exception, write summary/retrospective without narrative section

**Executor integration** (`executor.py`):
- `SummaryWorker.submit(phase_result)` called after `_verify_checkpoints()` (per Section 6.4 ordering)
- `RetrospectiveGenerator.generate()` called blocking, before terminal panel display

**Outputs:**
- `results/phase-N-summary.md` (per phase, background)
- `results/release-retrospective.md` (per sprint, blocking at end)

**Tests** (Section 12.2):
- `tests/sprint/test_summarizer.py` — programmatic NDJSON extraction, narrative prompt building, markdown generation, SummaryWorker thread safety (lock behavior under concurrent submits)
- `tests/sprint/test_retrospective.py` — aggregation from phase summaries, narrative prompt, retrospective markdown

### Acceptance Criteria
- [ ] `summarizer.py` contains `PhaseSummary` dataclass, `PhaseSummarizer`, and `SummaryWorker` — all in the same module per Section 3.2
- [ ] `SummaryWorker._summaries` dict protected by `threading.Lock`; verified by concurrent-submit test
- [ ] SummaryWorker exception handling wraps thread body; forced exception in narrative step does NOT affect sprint execution
- [ ] `retrospective.py` contains `ReleaseRetrospective` dataclass and `RetrospectiveGenerator`
- [ ] Haiku subprocess strips `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT`, uses `--max-turns 1 --dangerously-skip-permissions`, stdin=DEVNULL, 30s timeout
- [ ] Haiku failure → summary/retrospective written without narrative section (no exception propagated)
- [ ] `results/phase-N-summary.md` written within 30s of each phase completion (in background)
- [ ] `results/release-retrospective.md` written before terminal panel displays
- [ ] Programmatic NDJSON extraction captures 5 categories: task status, files changed, validation evidence, agent reasoning excerpts, errors
- [ ] `test_summarizer.py` and `test_retrospective.py` added with >80% coverage (Section 12.4 target)
- [ ] Executor call order matches Section 6.4: verify_checkpoints → summary_worker.submit → manifest update
- [ ] `shutil.which("claude") is None` path gracefully degrades (no narrative, no crash)

---

## SUBTASK — Phase 7 — Checkpoint Wave 3: Manifest + CLI Verify + Auto-Recovery

### Description
Manifest tracking, CLI verification subcommand, and auto-recovery from evidence artifacts. Addresses the remediation layer. Contains the single highest-risk task in the entire release (T03.03 at 75% confidence).

**Tasks** (Section 4.1 Phase 3, ~200 LOC):
- **T03.01** — Add `CheckpointEntry` dataclass to `models.py`: `phase: int`, `name: str`, `expected_path: Path`, `exists: bool`, `recovered: bool = False`, `recovery_source: str | None = None`. Confidence: 95%.
- **T03.02** — Extend `checkpoints.py` with `build_manifest(tasklist_index, release_dir) -> list[CheckpointEntry]` (scans all phase tasklists, calls `extract_checkpoint_paths()` for each) and `write_manifest(entries, output_path)` (writes `manifest.json` with summary counts + per-checkpoint details). Confidence: 80%.
- **T03.03** — ⚠️ **HIGHEST-RISK TASK (75% confidence)** — Add `recover_missing_checkpoints(manifest, artifacts_dir, phase_tasklists) -> list[CheckpointEntry]` to `checkpoints.py`. Filters for missing entries, reads phase tasklist for verification criteria, reads evidence files, generates checkpoint with `## Note: Auto-Recovered` header and `recovered: true` frontmatter. Must be idempotent (running twice does not overwrite). Template quality depends on evidence file format consistency — **fallback allowed: recovery is opt-in; failure does not block the pipeline**.
- **T03.04** — Add `superclaude sprint verify-checkpoints <dir>` CLI subcommand to `commands.py`. Flags: `--recover` (trigger auto-recovery), `--json` (machine-readable output). Default: print table of expected vs actual checkpoint status. Confidence: 85%.
- **T03.05** — Wire manifest build/verify into `executor.py` sprint lifecycle: `build_manifest()` at sprint start, `build_manifest()` + `write_manifest()` at sprint end, emit `checkpoint_manifest` JSONL event. Confidence: 85%.
- **T03.06** — Unit + integration tests: extend `test_checkpoints.py` for manifest (multi-phase) and recovery (idempotency, `Auto-Recovered` marking); `test_commands.py` for CLI subcommand with all flag combinations.

**Retroactive validation**: Run `superclaude sprint verify-checkpoints` against OntRAG R0+R1 sprint output. Should identify all 8 expected checkpoints (7 end-of-phase + 1 mid-phase in P3) and recover the missing P03 checkpoint with `--recover`.

**Open question CE-Q7 / CE-Q8**: `manifest.json` has no version field (low priority); no migration script for existing tasklists to Wave 4 format (low priority, defer).

### Acceptance Criteria
- [ ] `CheckpointEntry` dataclass in `models.py` with all 6 fields typed
- [ ] `build_manifest()` scans all phase tasklists and returns `CheckpointEntry` list
- [ ] `write_manifest()` writes valid JSON with summary + entries
- [ ] Handles phases with 0, 1, or 2 checkpoint sections
- [ ] `recover_missing_checkpoints()` generates valid checkpoint files from evidence
- [ ] Recovered checkpoints clearly marked with `## Note: Auto-Recovered` and `recovered: true` frontmatter
- [ ] Recovery is idempotent — running twice produces same output, does not overwrite existing files
- [ ] `superclaude sprint verify-checkpoints <dir>` prints checkpoint status table
- [ ] `--recover` flag triggers auto-recovery; `--json` outputs machine-readable manifest
- [ ] CLI works retroactively on sprints run before this feature existed
- [ ] Manifest built at sprint start; finalized at sprint end; `manifest.json` written to output dir
- [ ] `checkpoint_manifest` JSONL event emitted at sprint end
- [ ] Sprint execution time NOT noticeably affected (<5s overhead)
- [ ] OntRAG R0+R1 validation: manifest identifies all 8 expected checkpoints; `--recover` successfully regenerates P03 checkpoint
- [ ] Test coverage >90% on `checkpoints.py` (Section 12.4 target)
- [ ] CLI integration test validates all flag combinations

---

## SUBTASK — Phase 8 — TUI v2 Wave 4: Tmux Integration

### Description
Final TUI wave. 3-pane tmux layout with dedicated summary pane. Depends on Phase 6 (summary files must exist for the pane to display them).

**Feature F9** (`src/superclaude/cli/sprint/tmux.py`):
- Current 2-pane layout: TUI 75% (`:0.0`) + tail 25% (`:0.1`)
- Target 3-pane layout: TUI 50% (`:0.0`) + summary 25% (`:0.1`) + tail 25% (`:0.2`)
- **Pane index migration**: Every hardcoded `:0.1` referring to the tail pane must become `:0.2`. Grep for `:0.1` in `tmux.py` (Risk TUI-4).
- Summary pane initialization: shows waiting message ("Phase summaries will appear here...")
- Summary pane updates: `tmux send-keys` piping `cat` of summary file after each phase
- `--no-tmux` fallback: set `SprintTUI.latest_summary_notification: str | None = None`; render one-line notification `Phase N summary ready: results/phase-N-summary.md` in TUI

**Tests** (`tests/sprint/test_tmux.py`, NEW): 3-pane layout creation, summary pane updates, pane index handling.

### Acceptance Criteria
- [ ] `tmux.py` creates 3 panes: TUI 50%, summary 25%, tail 25%
- [ ] All hardcoded `:0.1` tail-pane references updated to `:0.2`
- [ ] `update_tail_pane()` (and any similar functions) write to correct pane index after migration — verified by test
- [ ] Summary pane shows waiting message on sprint start
- [ ] Summary pane updates via `tmux send-keys` + `cat` when a new `results/phase-N-summary.md` appears
- [ ] `--no-tmux` mode: TUI shows `Phase N summary ready: results/phase-N-summary.md` notification line
- [ ] `SprintTUI.latest_summary_notification` field added and wired
- [ ] `tests/sprint/test_tmux.py` passes for layout creation, summary updates, pane index handling
- [ ] Manual validation: run a multi-phase sprint with tmux and without — both modes show summaries correctly

---

## SUBTASK — Phase 9 — Checkpoint Wave 4: Tasklist Normalization (DEFERRED to next release cycle)

### Description
**Deferred per Section 1 "Deferred" and Section 9.1 timeline**: breaking change for tasklist generation. Ships with the next release cycle, NOT v3.7.

Eliminates the structural root cause (Cause 2) for all future tasklists. Converts `### Checkpoint:` headings — structurally invisible to the task scanner — into `### T<PP>.<NN>` task entries. Existing tasklists retain the old format; Waves 1–3 (prompt + gate + manifest) continue to handle them as the fallback path.

**Tasks** (Section 4.1 Phase 4, ~200 LOC):
- **T04.01** — Update `sc-tasklist-protocol/SKILL.md` checkpoint generation rules: produce `### T<PP>.<next_num> -- Checkpoint: <name>` (mid-phase) and `### T<PP>.<last_num> -- Checkpoint: End of Phase <PP>` (end-of-phase). Each gets metadata table (Effort=XS, Risk=Low, Tier=LIGHT), steps, acceptance criteria. Rule: checkpoint tasks MUST be last task(s) in phase. Confidence: 80%.
- **T04.02** — Add checkpoint task validation to Sprint Compatibility Self-Check in `SKILL.md`: every `### Checkpoint:` produces a `### T<PP>.<NN> -- Checkpoint:` task; end-of-phase checkpoint is last `### T<PP>.<NN>`; checkpoint metadata includes `Checkpoint Report Path:` reference.
- **T04.03** — Update deliverable registry guidance: checkpoint deliverable type `D-CP<PP>[-MID]` (e.g., `D-CP03`, `D-CP03-MID`); default paths `checkpoints/CP-P<PP>-END.md` or `checkpoints/CP-P<PP>-<NAME>.md`; verify no collision with existing `D-NNNN` IDs.

**Risk CE-3**: Numbering cascade — checkpoint tasks must not collide with existing task numbers. Self-check validation catches errors; Wave 1 prompt still works as fallback.

**Risk CE-5**: Existing OntRAG tasklists are incompatible — accepted; Waves 1-3 provide full coverage; Wave 4 applies to new generation only.

**Conflict with Phase 1 Naming**: Both touch `sc-tasklist-protocol/SKILL.md`. Per Section 5.5, Naming goes first (simple rename), Checkpoint W4 goes second (structural change). Since this phase ships in the NEXT cycle, that ordering is naturally respected.

### Acceptance Criteria
- [ ] SKILL.md produces `### T<PP>.<NN> -- Checkpoint:` entries (verified by generating a fresh test tasklist)
- [ ] Checkpoint tasks include metadata table, steps, acceptance criteria, deliverable references
- [ ] End-of-phase checkpoint is always the last task in its phase
- [ ] No numbering gaps or collisions when regenerating Phase 3 from fixture (5 regular + 1 mid-checkpoint + 1 regular + 1 end-checkpoint = T03.01–T03.08)
- [ ] Three new Sprint Compatibility Self-Check rules catch: missing checkpoint tasks, misplaced checkpoint tasks, missing report path references
- [ ] Checkpoint deliverable type `D-CP<PP>[-MID]` documented; no collision with existing `D-NNNN` IDs
- [ ] All three Checkpoint root causes addressed: Cause 1 (Wave 1 prompt), Cause 2 (Wave 4 structural), Cause 3 (Waves 2+3 gate + manifest)
- [ ] Explicitly documented as next-cycle release — not shipped in v3.7

---

## Notes for the ClickUp user

- **Phase 0** was added per request and is a research-only phase with no code changes. Nothing downstream blocks on it formally — but skipping it risks mis-wiring hook points in Phases 2–7.
- **Phase order** follows Section 6.2 recommended order, not strict Checkpoint/TUI wave numbering. Rationale: Naming goes first to reduce diff noise; Checkpoint W1 before TUI waves to maximize early value; `PASS_MISSING_CHECKPOINT` enum added in Phase 5 has a TUI rendering dependency that Phase 4 must stub (add-only stub, no functional coupling).
- **Parallelization opportunities**: Phase 3 (TUI data model) and Phase 5 (Checkpoint Wave 2) can overlap if different implementers own them — they touch `models.py` in different sections. Phase 6 (TUI summary modules) and Phase 7 (Checkpoint manifest/CLI) can overlap — different files.
- **Hard blockers**: Phase 8 (Tmux) blocks on Phase 6 (summary files must exist). Phase 5 (gate) blocks on Phase 4 having added `PASS_MISSING_CHECKPOINT` TUI stubs, or the TUI will crash when a phase downgrades.
- **Gate rollout**: After Phase 5 ships in `shadow` mode, promote to `soft` at Day 10 (per Section 9.1), then `full` at Sprint +2. The mode transitions are separate operational steps, not code tasks.
