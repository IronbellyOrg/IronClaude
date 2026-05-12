# Checkpoint: End of Sprint TUI v2 Wave 3 — Summary + Retrospective Infrastructure

**Checkpoint ID:** CP-TUI-P03-END
**Release:** v3.7-task-unified-v2
**Phase:** TUI v2 Wave 3 (ClickUp Phase 6)
**Status:** PASS
**Timestamp (UTC):** 2026-04-22

## Scope

Two new sprint modules plus executor integration. Every completed
phase now gets a background summary thread (F8), and every sprint
finishes with a blocking release retrospective (F10). Both pipelines
call Haiku per the shared subprocess convention in Section 6.3 and
silently tolerate every failure mode (no claude on PATH, non-zero
exit, timeout, OSError, narrative raise) so a summary issue can never
abort an otherwise-healthy sprint.

Work items:

- **`summarizer.py`** (new, ~330 LOC) — `PhaseSummary` dataclass,
  `PhaseSummarizer` orchestrator (extract → narrate → write), and the
  `SummaryWorker` daemon thread pool with a `threading.Lock`-guarded
  result dict. Exception handling wraps the entire thread body.
- **`retrospective.py`** (new, ~260 LOC) — `ReleaseRetrospective`
  dataclass, pure aggregation helpers
  (`_aggregate_phase_outcomes`/`_aggregate_files`/
  `_aggregate_validation_matrix`/`_aggregate_errors`/
  `_assess_validation_coverage`), and `RetrospectiveGenerator` that
  aggregates, narrates, and writes `results/release-retrospective.md`.
- **Haiku subprocess helper** — `invoke_haiku(prompt, timeout=30)` in
  `summarizer.py`, reused by `retrospective.py`. Strips `CLAUDECODE`
  and `CLAUDE_CODE_ENTRYPOINT` env vars, uses `--max-turns 1`,
  `--dangerously-skip-permissions`, `stdin=DEVNULL`; returns `""` on
  any failure.
- **Executor integration** — `SummaryWorker` instantiated before the
  phase loop; `submit(phase, phase_result)` called after the phase
  result is appended (per §6.4 ordering: `_verify_checkpoints` →
  `summary_worker.submit` → manifest update). At sprint end,
  `summary_worker.wait(timeout=90s)` is followed by
  `RetrospectiveGenerator.generate()` (blocking, before the terminal
  panel). Both calls are exception-isolated.
- **Defensive guard** — `RetrospectiveGenerator.narrate` short-circuits
  when `phase_outcomes` is empty. Without this, an interrupted sprint
  that ran zero phases would still shell out to Haiku just to render a
  retrospective with nothing to say; skipping also avoids spurious
  subprocess activity in tests that patch the global `subprocess.Popen`.

## Files Modified

| File | Action | Summary |
|------|--------|---------|
| `src/superclaude/cli/sprint/summarizer.py` | CREATE | `PhaseSummary`, `PhaseSummarizer`, `SummaryWorker`, `invoke_haiku`, NDJSON extractor for 5 signal categories |
| `src/superclaude/cli/sprint/retrospective.py` | CREATE | `ReleaseRetrospective`, `RetrospectiveGenerator`, aggregate helpers, narrative prompt builder, markdown renderer |
| `src/superclaude/cli/sprint/executor.py` | MODIFY | Instantiate `SummaryWorker`; submit per-phase; at sprint end `wait()` + `RetrospectiveGenerator.generate()`; all exception-wrapped |
| `tests/sprint/test_summarizer.py` | CREATE | 21 tests — NDJSON extraction, Haiku subprocess variants, summarizer end-to-end, SummaryWorker thread-safety + exception isolation |
| `tests/sprint/test_retrospective.py` | CREATE | 16 tests — aggregation helpers, narrative prompt, markdown rendering, generator end-to-end, empty-summary edge case |

## Verification

### Spec Section 3.2 + 4.2 Wave 3 — acceptance criteria

| Acceptance criterion | Result |
|---|---|
| `summarizer.py` contains `PhaseSummary`, `PhaseSummarizer`, `SummaryWorker` in the same module | PASS |
| `SummaryWorker._summaries` dict protected by `threading.Lock` (concurrent-submit test) | PASS (`test_concurrent_submit_is_thread_safe`) |
| `SummaryWorker` exception isolation — forced raise does not affect sprint | PASS (`test_summarize_exception_never_propagates`) |
| `retrospective.py` contains `ReleaseRetrospective` + `RetrospectiveGenerator` | PASS |
| Haiku subprocess strips `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT`, uses `--max-turns 1 --dangerously-skip-permissions`, `stdin=DEVNULL`, 30s timeout | PASS (`test_success_returns_stdout_stripped`) |
| Haiku failure → summary/retrospective written without narrative | PASS (`test_summarize_tolerates_narrative_failure`, `test_generate_tolerates_narrative_failure`) |
| `results/phase-N-summary.md` written per phase | PASS (`test_summarize_writes_markdown_file`) |
| `results/release-retrospective.md` written once per sprint | PASS (`test_generate_writes_markdown_file`) |
| NDJSON extraction captures 5 categories (tasks, files, validations, reasoning, errors) | PASS (entire `TestExtractPhaseSignals` class) |
| `shutil.which("claude") is None` path gracefully degrades | PASS (`test_returns_empty_when_claude_not_on_path`) |
| Executor call order: `_verify_checkpoints` → `summary_worker.submit` → manifest update | PASS — confirmed by code inspection and `§6.4` alignment |

### Regression Status

| Suite | Before Wave 3 | After Wave 3 |
|-------|---------------|--------------|
| Full `tests/sprint/` | 867 passed, 57 failed | 904 passed, 57 failed |
| New tests added | — | +37 passing (21 summarizer + 16 retrospective) |
| Regressions introduced | — | 0 (after the `narrate` short-circuit fix) |

Lint on authored code paths (`summarizer.py`, `retrospective.py`,
`tests/sprint/test_summarizer.py`, `tests/sprint/test_retrospective.py`)
is clean; remaining ruff hits in this area are all pre-existing in
`models.py`.

## Post-phase hook ordering (§6.4 confirmation)

Inside the phase loop body, immediately after `phase_result` is
appended to `sprint_result.phase_results`:

```
1. _verify_checkpoints(...)          # Wave 2 (already present)
2. _summary_worker.submit(phase, pr) # Wave 3 (non-blocking)
3. (end-of-sprint) build_manifest()  # Wave 3/Checkpoint (already present)
```

At sprint end, wrap-up order becomes:

```
1. _summary_worker.wait(timeout=90)
2. RetrospectiveGenerator(config).generate(sprint_result, summaries)
3. tui.update(sprint_result, MonitorState(), None)   # terminal panel
4. kpi_report + manifest write  (unchanged)
```

All three new steps are wrapped in a `try/except` so a failing Haiku
subprocess, filesystem error, or aggregation bug never aborts the
sprint's final KPI/manifest/log writes.

## Cross-wave dependencies

- **Wave 1 + Wave 2** — used end-to-end. `SprintResult` aggregates
  drive the retrospective header; `Phase.prompt_preview` and
  `PhaseResult.turns/tokens_*` drive the phase-summary prompt.
- **Wave 4 (Tmux Integration)** — unblocked. The
  `results/phase-N-summary.md` files Wave 4 will `cat` into its
  dedicated pane now exist; the fallback
  `SprintTUI.latest_summary_notification` field is not yet needed
  (Wave 4 will add it).
- **Naming Consolidation** — unchanged; still pending per §6.2.

## Next steps

- TUI v2 Wave 4: 3-pane tmux layout (TUI 50% / summary 25% / tail 25%),
  summary pane updates via `tmux send-keys`, `:0.1 → :0.2` tail pane
  migration, and the `--no-tmux` fallback notification line.
- Naming consolidation still pending; §6.2 places it before Wave 4 to
  minimise diff noise.

**Source**: `v3.7-UNIFIED-RELEASE-SPEC-merged.md` §3.2 (F8/F10), §4.2
Wave 3, §6.3, §6.4, §7.6; `clickup-tasks.md` Phase 6.
