---
release: 2
parent-spec: .dev/releases/backlog/v3.7-task-unified-v2/v3.7-UNIFIED-RELEASE-SPEC-merged.md
split-proposal: .dev/releases/backlog/v3.7-task-unified-v2/release-split/split-proposal-final.md
scope: Sprint TUI v2 — Visual UX overhaul with rich telemetry, summaries, and tmux integration
status: draft
validation-gate: "blocked until R1 real-world validation passes"
---

# Release 2 — v3.7b Sprint TUI v2

## Objective

Surface rich real-time telemetry from Claude's stream-json output into the sprint dashboard. Add 10 features across 7 files: activity stream, enhanced phase table, dual progress bars, conditional error panel, LLM context preview, enhanced terminal panels, sprint name display, post-phase summary generation with Haiku narratives, tmux summary pane integration, and release retrospective generation.

## Scope

### Included

#### TUI Data Infrastructure (Wave 1)

1. **MonitorState — 8 new fields**: activity_log, turns, errors, last_assistant_text, total_tasks_in_phase, completed_task_estimate, tokens_in, tokens_out
   From: [parent-spec] Section 7.1
2. **PhaseResult — 3 new fields**: turns, tokens_in, tokens_out
   From: [parent-spec] Section 7.2
3. **SprintResult — 5 new properties**: total_turns, total_tokens_in, total_tokens_out, total_output_bytes, total_files_changed
   From: [parent-spec] Section 7.3
4. **SprintConfig.total_tasks**: Pre-scanned total task count
   From: [parent-spec] Section 7.4
5. **SprintTUI.latest_summary_notification**: Notification for --no-tmux mode
   From: [parent-spec] Section 7.7
6. **Monitor extraction updates**: Turn counting, token tracking, activity log, error detection, assistant text, task counting, pre-scan
   From: [parent-spec] Section 4.2 Wave 1

#### TUI Rendering (Wave 2)

7. **F1: Activity Stream** — 3-line FIFO ring buffer of tool calls. Format: `HH:MM:SS ToolName condensed_input`. Tool name shortening. Thinking indicator when no tool call for >2s.
   From: [parent-spec] Section 4.2 Wave 2, F1 detail
8. **F2: Enhanced Phase Table** — Add Turns (width=6) and Output (width=8) columns. Remove Tasks column.
   From: [parent-spec] Section 4.2 Wave 2, F2 detail
9. **F3: Task-Level Progress Bar** — Dual progress bar (phase + task) on single line using block characters. Pre-scan task count via regex.
   From: [parent-spec] Section 4.2 Wave 2, F3 detail
10. **F4: Conditional Error Panel** — Hidden when empty. Red border, max 10 stored, max 5 displayed with overflow count. Data from tool_result events with is_error or non-zero exit code.
    From: [parent-spec] Section 4.2 Wave 2, F4 detail
11. **F5: LLM Context Lines** — Prompt preview (~60 chars) and agent reasoning text (~60 chars) in active panel.
    From: [parent-spec] Section 4.2 Wave 2, F5 detail
12. **F6: Enhanced Terminal Panels** — Success: Result, Duration, Turns, Tokens, Output, Files, Log. Halt: adds Completed, Last task + failure, Errors, Resume command.
    From: [parent-spec] Section 4.2 Wave 2, F6 detail
13. **F7: Sprint Name in Title** — `[bold]SUPERCLAUDE SPRINT RUNNER[/] [dim]== {release_name}[/]`
    From: [parent-spec] Section 4.2 Wave 2, F7 detail

#### Summary Infrastructure (Wave 3)

14. **F8: Post-Phase Summary (summarizer.py)** — Non-blocking background thread per phase. PhaseSummary dataclass, PhaseSummarizer class, SummaryWorker daemon thread pool. Programmatic NDJSON extraction (5 categories), Haiku narrative (3-5 sentences, 30s timeout), markdown output.
    From: [parent-spec] Section 3.2, Section 4.2 Wave 3, F8 detail

    **Critical Invariants**:
    - Summary failure must never affect sprint execution. All exceptions caught.
    - `SummaryWorker._summaries` dict MUST be guarded by `threading.Lock`.
    From: [parent-spec] Section 3.2 Critical Invariants

15. **F10: Release Retrospective (retrospective.py)** — Blocking, runs before terminal panel display. ReleaseRetrospective dataclass, RetrospectiveGenerator class. Reads all phase summaries, aggregates programmatically, Haiku narrative (4-8 sentences), writes `results/release-retrospective.md`.
    From: [parent-spec] Section 3.2, Section 4.2 Wave 3, F10 detail

16. **Haiku Narrative Pipeline** — Shared pattern for F8 and F10: check `shutil.which("claude")`, build prompt, strip `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT` env vars, run `claude --print --model claude-haiku-4-5 --max-turns 1 --dangerously-skip-permissions`, 30s timeout, graceful failure.
    From: [parent-spec] Section 3.2 Haiku Narrative Pipeline

17. **Executor integration** — SummaryWorker integration, RetrospectiveGenerator blocking call, PhaseResult population with new fields.
    From: [parent-spec] Section 4.2 Wave 3 Executor row

#### Tmux Integration (Wave 4)

18. **F9: Tmux Summary Pane** — 3-pane layout: TUI 50% + summary 25% + tail 25%. Summary pane initially shows waiting message. Updated via `tmux send-keys`. Tail pane index shifts from `:0.1` to `:0.2`. `--no-tmux` fallback with notification line.
    From: [parent-spec] Section 4.2 Wave 4, F9 detail

#### Checkpoint Display Integration

19. **STATUS_STYLES dict** — Add entry for `PASS_MISSING_CHECKPOINT` (yellow/amber styling)
    From: [parent-spec] Section 5.1, Section 5.4
20. **STATUS_ICONS dict** — Add entry for `PASS_MISSING_CHECKPOINT` (warning icon)
    From: [parent-spec] Section 5.1, Section 5.4

#### Cross-Cutting

21. **Post-phase hook ordering in executor.py** — Explicit call order: (1) `_verify_checkpoints()` (R1), (2) `summary_worker.submit()`, (3) manifest update (R1). `_verify_checkpoints()` SHOULD complete within 5s; if exceeded, log warning but do not block `summary_worker.submit()`.
    From: [parent-spec] Section 6.4

22. **Token display helper** — `_format_tokens(n)` with K/M suffixes. Place in `tui.py` or shared `utils.py`.
    From: [parent-spec] Section 6.5

### Excluded (assigned to Release 1)

1. **Naming Consolidation (N1-N12)** — Completed in Release 1
2. **Checkpoint Enforcement Waves 1-3** — Completed in Release 1
3. **PASS_MISSING_CHECKPOINT enum, CheckpointEntry, checkpoint_gate_mode** — Created in Release 1
4. **checkpoints.py module** — Created in Release 1
5. **verify-checkpoints CLI** — Created in Release 1

### Excluded (deferred beyond this split)

6. **Checkpoint Wave 4 (T04.01-T04.03)** — Tasklist normalization, next release cycle (breaking change)
   Deferred to: Next release cycle per original spec
7. **TUI `--compact` flag** — Deferred per original spec
8. **Cost tracking, MCP health indicators, ETA estimation** — Deferred per original spec
9. **Sprint status/logs stubs, modal overlay, configurable summary model** — Deferred per original spec

## Dependencies

### Prerequisites (from Release 1)

| R1 Deliverable | R2 Consumer | Nature |
|---------------|------------|--------|
| PhaseStatus.PASS_MISSING_CHECKPOINT | STATUS_STYLES, STATUS_ICONS in tui.py | Hard — enum must exist for display entries |
| executor.py post-checkpoint hook site | SummaryWorker.submit() call site | Hard — R2 adds call after R1's _verify_checkpoints() |
| checkpoints.py module | executor.py post-phase hook ordering | Soft — R2 calls summary after R1's checkpoint verification |
| Naming consolidation complete | Clean references in all files R2 touches | Soft — avoids double-rename in process.py |

### External Dependencies

- `claude` CLI available on PATH (for Haiku narrative subprocess)
- Python >=3.10, UV for execution
- tmux (for F9, with --no-tmux fallback)

### Intra-Release Ordering Constraints

**Wave 1 must be code-complete and passing all tests before Wave 2 implementation begins**: All TUI features depend on the data model and monitor extraction layer.
From: [parent-spec] Section 4.2 Wave 1 Rationale

**Wave 3 can proceed in parallel with Wave 2**: Summary infrastructure (new modules) has no rendering dependency on Wave 2.
From: [parent-spec] Section 4.2 Wave 3 Rationale

**Wave 4 depends on Wave 3**: Summary files must exist for the tmux summary pane to display them.
From: [parent-spec] Section 4.2 Wave 4 Rationale

## Real-World Validation Requirements

1. **Visual layout verification**: Run a real sprint (3+ phases). Visually confirm the TUI displays: activity stream updates, dual progress bars, Turns/Output columns in phase table, sprint name in title.

2. **Error panel test**: Run a sprint where at least one tool call fails. Verify the error panel appears with red border and accurate error content.

3. **Post-phase summary**: After each phase completes, verify `results/phase-N-summary.md` is written within 30 seconds. Verify it contains structured data (tasks, files, validations) and, if Haiku is available, a narrative section.

4. **Release retrospective**: After all phases complete, verify `results/release-retrospective.md` is generated before the terminal panel displays. Verify it aggregates data from all phase summaries.

5. **Tmux 3-pane**: Run a sprint in a tmux session. Verify 3 panes appear (TUI 50%, summary 25%, tail 25%). Verify summary pane updates after each phase.

6. **--no-tmux fallback**: Run a sprint outside tmux. Verify notification line appears in TUI when summary is ready.

7. **PASS_MISSING_CHECKPOINT display**: Set checkpoint gate to `full` mode (from R1). Trigger a missing checkpoint scenario. Verify TUI renders the status with appropriate yellow/amber styling and warning icon.

8. **SummaryWorker thread safety**: Run a sprint with 4+ phases. Verify no threading errors or deadlocks. All phase summaries written correctly.

9. **Haiku failure graceful degradation**: Run a sprint with `claude` CLI not on PATH. Verify summaries are written without narrative section and no errors surface in the TUI.

10. **Test suite**: `make test` passes. All existing tests updated for new fields/columns. New test files pass (test_summarizer.py, test_retrospective.py, test_tmux.py).

## Success Criteria

| Metric | Current | Target |
|--------|---------|--------|
| Information visible without log inspection | Minimal | Comprehensive (turns, tokens, errors, activity, reasoning) |
| Post-phase analysis availability | Manual | Automatic (within 30s of phase completion) |
| Error visibility latency | End of phase | Real-time (within 1 event cycle) |
| Release summary availability | None | Automatic (before terminal panel) |

From: [parent-spec] Section 11.2

## Planning Gate

> Release 2 roadmap/tasklist generation may proceed only after Release 1 has passed real-world validation and the results have been reviewed.
>
> **Validation criteria**: Release 1 must demonstrate:
> - Checkpoint write rate: 100% over at least 2 sprint runs
> - Zero false positives in checkpoint gate over 2 sprint cycles
> - `/sc:task` resolves correctly in Claude Code sessions
> - `verify-checkpoints` CLI produces accurate manifest
> - `make test` passes with no regressions
>
> **Review process**: Developer reviews sprint JSONL logs and CLI output, confirms all R1 success metrics are met.
>
> **If validation fails**: Revise Release 1 before proceeding. Do not begin Release 2 implementation until R1 issues are resolved.

## File Inventory

| File | Wave | Action | Changes |
|------|------|--------|---------|
| `src/superclaude/cli/sprint/models.py` | 1 | MODIFY | MonitorState (8 fields), PhaseResult (3 fields), SprintResult (5 properties), SprintConfig (1 field), SprintTUI (1 field) |
| `src/superclaude/cli/sprint/monitor.py` | 1 | MODIFY | Turn counting, token tracking, activity log, error detection, assistant text, task counting, pre-scan |
| `src/superclaude/cli/sprint/tui.py` | 2 | MODIFY | New layout, dual progress, activity stream, error panel, LLM context, terminal panels, summary notification, PASS_MISSING_CHECKPOINT display |
| `src/superclaude/cli/sprint/executor.py` | 3 | MODIFY | SummaryWorker integration, RetrospectiveGenerator, PhaseResult population |
| `src/superclaude/cli/sprint/tmux.py` | 4 | MODIFY | 3-pane layout, summary pane management, pane index update |
| `src/superclaude/cli/sprint/summarizer.py` | 3 | CREATE | PhaseSummary, PhaseSummarizer, SummaryWorker |
| `src/superclaude/cli/sprint/retrospective.py` | 3 | CREATE | ReleaseRetrospective, RetrospectiveGenerator |

### Test Files

| File | Action | Scope |
|------|--------|-------|
| `tests/sprint/test_tui.py` | MODIFY | New column assertions, MonitorState fixtures, terminal panels, dual progress, error panel |
| `tests/sprint/test_models.py` | MODIFY | New MonitorState/PhaseResult/SprintResult fields |
| `tests/sprint/test_tui_gate_column.py` | MODIFY | Phase table column assertions (Tasks removed, Turns/Output added) |
| `tests/sprint/test_tui_monitor.py` | MODIFY | Monitor state assertions for new fields |
| `tests/sprint/test_tui_task_updates.py` | MODIFY | Task progress display changes |
| `tests/sprint/test_summarizer.py` | CREATE | PhaseSummarizer, SummaryWorker thread safety |
| `tests/sprint/test_retrospective.py` | CREATE | RetrospectiveGenerator aggregation |
| `tests/sprint/test_tmux.py` | CREATE | 3-pane layout, summary pane |

### Output Artifacts (per sprint)

| File | When Written | Writer |
|------|-------------|--------|
| `results/phase-N-summary.md` | After each phase (background) | SummaryWorker via PhaseSummarizer |
| `results/release-retrospective.md` | After all phases (blocking) | RetrospectiveGenerator |

## Risk Register

| # | Risk | Severity | Likelihood | Mitigation |
|---|------|----------|------------|------------|
| TUI-1 | Haiku narrative call fails | Low | Medium | Graceful degradation: summary without narrative |
| TUI-2 | SummaryWorker thread safety | Medium | Low | threading.Lock mandated for _summaries dict |
| TUI-3 | Task estimation inaccuracy | Low | Low | Labeled as "estimate" in UI |
| TUI-4 | Tmux pane index migration | Medium | Medium | Update hardcoded `:0.1` to `:0.2` |
| TUI-5 | Monitor reset interface gap | Medium | Medium | Add phase_file param to reset() |
| TUI-6 | Gate column interaction | Low | Low | Preserve existing _show_gate_column |
| R2-1 | executor.py merge conflict with R1 | Medium | Medium | Branch from R1 merge commit |

From: [parent-spec] Section 10.2

## Open Questions (carried from parent spec)

| # | Question | Priority |
|---|----------|----------|
| TUI-Q1 | prompt_preview field location | Medium |
| TUI-Q2 | Task estimation accuracy bounds | Low |
| TUI-Q4 | Monitor reset needs phase file path | Medium |
| TUI-Q6 | Error panel task ID extraction | Low |
| TUI-Q7 | Haiku model availability notification | Low |
| TUI-Q8 | Per-task execution mode prompt preview | Low |
| TUI-Q9 | Gate column interaction | Low |
| TUI-Q10 | config.py pre-scan integration | Low |

From: [parent-spec] Section 14.2

## Traceability

| Release 2 Item | Parent Spec Section |
|----------------|-------------------|
| MonitorState fields | Section 7.1 |
| PhaseResult fields | Section 7.2 |
| SprintResult properties | Section 7.3 |
| SprintConfig.total_tasks | Section 7.4 |
| SprintTUI.latest_summary_notification | Section 7.7 |
| PhaseSummary dataclass | Section 7.6 |
| ReleaseRetrospective dataclass | Section 7.6 |
| F1-F10 features | Section 4.2 |
| Haiku narrative pipeline | Section 3.2 |
| Post-phase hook ordering | Section 6.4 |
| Token display helper | Section 6.5 |
| Haiku subprocess conventions | Section 6.3 |
| TUI risks TUI-1 through TUI-6 | Section 10.2 |
| TUI metrics | Section 11.2 |
| TUI tests | Section 12.1-12.4 |
| TUI open questions | Section 14.2 |
| UI layout mockups | Section 15, Appendix B |
