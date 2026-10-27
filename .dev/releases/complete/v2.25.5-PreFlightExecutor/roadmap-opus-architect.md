

---
spec_source: sprint-preflight-executor-spec.md
complexity_score: 0.55
primary_persona: architect
---

# Preflight Executor — Project Roadmap

## Executive Summary

This feature introduces a **pre-sprint preflight execution mode** that runs Python/shell-based phases locally via `subprocess.run()` before the main Claude loop begins. The core value proposition is eliminating API token waste on deterministic, automatable tasks (e.g., environment checks, file generation) — reducing a prior 857s timeout to <30s with zero token consumption.

The scope is moderate: ~400 LOC of new code across 3 new files, ~100 LOC of modifications to 3 existing files, and ~200 LOC of tests. All work stays within `src/superclaude/cli/sprint/`. No external dependencies are introduced.

**Key architectural decisions:**
- Execution mode is **phase-level**, not per-task — keeps the model simple
- Preflight runs **before** the main loop, not inline — clean separation of concerns
- Result files reuse `AggregatedPhaseReport.to_markdown()` — zero parser changes needed
- Single-line rollback by removing one function call

## Phased Implementation Plan

### Phase 1: Data Model & Parsing Extensions
**Milestone: All data structures in place, round-trip tested**

1. Add `execution_mode: str = "claude"` field to `Phase` dataclass
2. Extend `discover_phases()` to read `Execution Mode` column from `tasklist-index.md`
   - Case-insensitive normalization
   - `click.ClickException` on unrecognized values
   - Default to `"claude"` when column is absent
3. Add `command: str = ""` field to `TaskEntry` dataclass
4. Extend `parse_tasklist()` to extract `**Command:**` field
   - Strip backtick delimiters
   - Preserve pipes, redirects, quoted arguments verbatim
5. Add `classifier: str = ""` field to `TaskEntry` for `| Classifier |` metadata extraction
6. Add `PhaseStatus.PREFLIGHT_PASS = "preflight_pass"` to enum
   - `is_success` returns `True`, `is_failure` returns `False`

**Tests (Phase 1):**
- Unit tests for `Phase` with all three execution modes
- Unit tests for `TaskEntry.command` extraction (empty, simple, pipes, quotes)
- Unit tests for `TaskEntry.classifier` extraction
- Unit test for `PhaseStatus.PREFLIGHT_PASS` behavior
- Round-trip test: write `tasklist-index.md` with `Execution Mode` column → parse → verify

**Deliverables:** Modified `config.py` (or equivalent model file), modified `parse_tasklist()`, updated `PhaseStatus` enum.

---

### Phase 2: Classifier Registry
**Milestone: Registry operational with built-in classifier**

1. Create `src/superclaude/cli/sprint/classifiers.py`
2. Define `CLASSIFIERS: dict[str, Callable[[int, str, str], str]]`
3. Implement `empirical_gate_v1` classifier
   - Signature: `(exit_code: int, stdout: str, stderr: str) -> str`
   - Returns classification label (e.g., `"pass"`, `"fail"`)
4. Validate classifier lookup: missing key raises `KeyError`
5. Wrap classifier invocation: catch exceptions, log, treat as task failure

**Tests (Phase 2):**
- Unit test `empirical_gate_v1` with known pass/fail inputs
- Unit test `KeyError` on missing classifier name
- Unit test exception handling in classifier invocation

**Deliverables:** New `classifiers.py` module.

---

### Phase 3: Preflight Executor Core
**Milestone: Preflight runs commands and produces results**

1. Create `src/superclaude/cli/sprint/preflight.py`
2. Implement `execute_preflight_phases(config) -> list[PhaseResult]`
   - Filter `config.active_phases` where `execution_mode == "python"`
   - For each phase: `parse_tasklist()`, iterate tasks
   - For each task: `shlex.split(command)`, `subprocess.run(shell=False, capture_output=True, timeout=120)`
   - Capture stdout, stderr, exit_code, wall-clock duration
   - Apply classifier from registry
   - Build `TaskResult` per task, `PhaseResult` per phase
3. Write evidence artifacts per task to `artifacts/<task_id>/evidence.md`
   - Command, exit code, stdout (truncated 10KB), stderr (truncated 2KB), duration, classification
   - `mkdir(parents=True, exist_ok=True)`
4. Write `phase-N-result.md` via `AggregatedPhaseReport.to_markdown()`
   - YAML frontmatter includes `source: preflight`
   - `EXIT_RECOMMENDATION: CONTINUE` or `HALT`

**Tests (Phase 3):**
- Integration test: preflight executes `echo hello` and captures output
- Integration test: timeout triggers after configured duration
- Integration test: evidence file written with correct structure
- Integration test: result file parseable by `_determine_phase_status()`
- Unit test: stdout/stderr truncation at limits

**Deliverables:** New `preflight.py` module, evidence and result file generation.

---

### Phase 4: Sprint Integration & Skip Mode
**Milestone: End-to-end sprint with mixed modes works correctly**

1. Call `execute_preflight_phases()` in `execute_sprint()` before the main phase loop
2. Main loop skips phases where `execution_mode == "python"` (already handled)
3. Main loop skips phases where `execution_mode == "skip"` with `PhaseStatus.SKIPPED`
4. Merge preflight `PhaseResult` list with main loop results for final sprint outcome
5. Verify logger and TUI handle `PREFLIGHT_PASS` and `SKIPPED` without errors

**Tests (Phase 4):**
- Integration test: sprint with mixed `python`/`claude`/`skip` phases produces correct combined results
- Integration test: removing `execute_preflight_phases()` call reverts to all-Claude behavior
- Integration test: `skip` phases produce `SKIPPED` status, no subprocess launched
- Integration test: zero `ClaudeProcess` instantiation for python-mode phases

**Deliverables:** Modified `execute_sprint()` (or `process.py`), complete end-to-end flow.

---

### Phase 5: Polish & Validation
**Milestone: All success criteria met, ready for merge**

1. Run full test suite: 14 unit + 8 integration tests passing
2. Verify SC-001: python-mode phase completes <30s with zero API tokens
3. Verify SC-002: nested `claude --print -p "hello"` works without deadlock
4. Verify SC-007: single-line rollback works
5. Run `make lint && make format`
6. Run `make sync-dev && make verify-sync`
7. Update execution log and any relevant documentation

**Deliverables:** Green test suite, passing lint, synced dev copies.

## Risk Assessment & Mitigation

| Risk | Severity | Mitigation | Phase Addressed |
|------|----------|------------|-----------------|
| **RISK-001: Result file format drift** | High | Shared fixture test validates both `to_markdown()` output and `_determine_phase_status()` parsing. No parser modifications allowed. | Phase 3 |
| **RISK-002: Environment mismatch** | Medium | Evidence files capture full stderr and environment context. Preflight logs command details for diagnosis. | Phase 3 |
| **RISK-003: Command quoting/escaping** | Medium | Use `shlex.split()` with comprehensive test cases covering pipes, redirects, quoted args. Document `shell=False` limitation. | Phase 3 |
| **RISK-004: Classifier bugs** | Low | Unit tests per classifier with known I/O. Exceptions caught, logged, treated as failure. | Phase 2 |
| **RISK-005: Future mixed-mode phases** | Low | Defer. Phase-level annotation covers all current patterns. Per-task annotation is a non-breaking future migration. | N/A |

**Additional architect concerns:**
- **Deadlock risk with nested Claude calls** — `subprocess.run()` with `capture_output=True` uses pipes; large output from nested `claude --print` could theoretically fill pipe buffers. The 120s timeout is the backstop, but SC-002 explicitly validates this case.
- **`shlex.split()` on Windows** — `shlex.split()` uses POSIX mode by default. If cross-platform support matters, this needs `posix=False` on Windows. Current target appears Linux-only, so this is acceptable.

## Resource Requirements & Dependencies

**Internal dependencies (all existing, no modifications needed):**
- `AggregatedPhaseReport.to_markdown()` — result file generation
- `_determine_phase_status()` — result file parsing (read-only contract)
- `parse_tasklist()` / `discover_phases()` — extended, not replaced

**Stdlib only:** `subprocess`, `shlex`, `time`, `pathlib` — no new external packages.

**Files modified:**
| File | Change Type |
|------|------------|
| `src/superclaude/cli/sprint/config.py` (or model file) | Extend `Phase`, `TaskEntry` dataclasses |
| `src/superclaude/cli/sprint/process.py` | Add preflight call + skip logic in `execute_sprint()` |
| `PhaseStatus` enum location | Add `PREFLIGHT_PASS` |

**Files created:**
| File | Purpose |
|------|---------|
| `src/superclaude/cli/sprint/classifiers.py` | Classifier registry + `empirical_gate_v1` |
| `src/superclaude/cli/sprint/preflight.py` | `execute_preflight_phases()` core logic |
| `tests/cli/sprint/test_preflight.py` | Unit + integration tests |

## Success Criteria Validation

| Criterion | Validation Method | Phase |
|-----------|-------------------|-------|
| SC-001: <30s, zero tokens | Wall-clock timing + token counter assertion | 5 |
| SC-002: Nested claude --print works | Integration test with real subprocess | 4 |
| SC-003: Parser compatibility | Unit test: preflight result → `_determine_phase_status()` | 3 |
| SC-004: 14 unit tests pass | `uv run pytest tests/cli/sprint/test_preflight.py -m unit` | 5 |
| SC-005: 8 integration tests pass | `uv run pytest tests/cli/sprint/test_preflight.py -m integration` | 5 |
| SC-006: Skip mode works | Assert `PhaseStatus.SKIPPED`, no subprocess | 4 |
| SC-007: Single-line rollback | Remove call, run existing test suite, all pass | 5 |
| SC-008: Evidence artifacts complete | Assert file contents against schema | 3 |

## Timeline Estimates

| Phase | Scope | Estimate |
|-------|-------|----------|
| Phase 1: Data Model & Parsing | 3 dataclass changes, parser extension, enum | Small |
| Phase 2: Classifier Registry | 1 new module, 1 built-in classifier | Small |
| Phase 3: Preflight Executor | Core logic, evidence writing, result generation | Medium |
| Phase 4: Sprint Integration | Orchestration changes, skip mode | Small-Medium |
| Phase 5: Polish & Validation | Test suite, lint, sync, docs | Small |

Phases 1 and 2 are independent and can be developed in parallel. Phase 3 depends on both. Phase 4 depends on Phase 3. Phase 5 is a final sweep.

## Open Questions Resolution Recommendations

1. **OQ-001 (multi-line commands):** Recommend deferring. If encountered, treat `\`-continuations as part of the raw string passed to `shlex.split()`. Add a test case but don't over-engineer.
2. **OQ-002 (dry-run interaction):** Recommend listing python-mode phases with `[preflight]` tag in dry-run output. Low effort, high clarity.
3. **OQ-003 (classifier exceptions):** Recommend formalizing: catch, log at WARNING, return `"error"` classification, treat as `TaskStatus.FAIL`. Add to FR-004 acceptance criteria.
4. **OQ-004 (--phases filter):** Recommend respecting `--phases` for preflight phases too. If `--phases 2,3` excludes Phase 1, preflight skips it. Consistent behavior.
5. **OQ-005 (ordering constraint):** No constraint needed. Preflight runs all python-mode phases in declared order before the loop. If a python phase appears after claude phases in the index, it still runs first — document this explicitly.
