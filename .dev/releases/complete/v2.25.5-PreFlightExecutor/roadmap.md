

---
spec_source: sprint-preflight-executor-spec.md
complexity_score: 0.55
adversarial: true
---

# Preflight Executor — Final Merged Roadmap

## Executive Summary

This feature introduces a **pre-sprint preflight execution mode** that runs Python/shell-based phases locally via `subprocess.run()` before the main Claude loop begins. The core value proposition is eliminating API token waste on deterministic, automatable tasks (e.g., environment checks, file generation) — reducing a prior 857s timeout to <30s with zero token consumption.

The scope is moderate: ~400 LOC of new code across 3 new files, ~100 LOC of modifications to 3 existing files, and ~200 LOC of tests. All work stays within `src/superclaude/cli/sprint/`. No external dependencies are introduced.

The architecture crosses four domains — **phase discovery/config parsing, task parsing, subprocess execution, and result/status integration** — but remains contained within the existing sprint package. The highest-risk boundary is result file compatibility with `_determine_phase_status()`, mitigated by reusing `AggregatedPhaseReport.to_markdown()` directly and enforcing format contracts through shared test fixtures.

**Key architectural decisions:**
- Execution mode is **phase-level**, not per-task — keeps the model simple
- Preflight runs **before** the main loop, not inline — clean separation of concerns
- Result files reuse `AggregatedPhaseReport.to_markdown()` — zero parser changes needed
- Single-line rollback by removing one function call
- Explicit validation for missing commands in python-mode tasks (fail-fast with actionable errors)
- OQ-001 through OQ-004 resolved upfront; OQ-005 (ordering semantics) flagged for stakeholder confirmation

## Phased Implementation Plan

### Phase 1: Data Model and Parsing Extensions

**Milestone: All data structures in place, round-trip tested**

1. Add `execution_mode: str = "claude"` field to `Phase` dataclass
2. Extend `discover_phases()` to read `Execution Mode` column from `tasklist-index.md`
   - Case-insensitive normalization
   - Accept only `claude`, `python`, `skip`
   - `click.ClickException` on unrecognized values
   - Default to `"claude"` when column is absent
3. Add `command: str = ""` field to `TaskEntry` dataclass
4. Extend `parse_tasklist()` to extract `**Command:**` field
   - Strip backtick delimiters
   - Preserve pipes, redirects, quoted arguments verbatim
5. Add `classifier: str = ""` field to `TaskEntry` for `| Classifier |` metadata extraction
6. Add `PhaseStatus.PREFLIGHT_PASS = "preflight_pass"` to enum
   - `is_success` returns `True`, `is_failure` returns `False`
7. **Add explicit validation for python-mode tasks with empty commands**
   - If a phase has `execution_mode == "python"` and any task has `command == ""`, raise `click.ClickException(f"Task {task_id} in python-mode phase has no command")`
   - Validates at parse time, not execution time — produces actionable errors instead of subprocess tracebacks

**Tests (Phase 1):**
- Unit tests for `Phase` with all three execution modes
- Unit tests for `TaskEntry.command` extraction (empty, simple, pipes, quotes)
- Unit tests for `TaskEntry.classifier` extraction
- Unit test for `PhaseStatus.PREFLIGHT_PASS` behavior
- Unit test for missing-command validation in python-mode phases
- Round-trip test: write `tasklist-index.md` with `Execution Mode` column → parse → verify

**Deliverables:** Modified config/model file, modified `parse_tasklist()`, updated `PhaseStatus` enum.

### Phase 2: Classifier Registry

**Milestone: Registry operational with built-in classifier**

1. Create `src/superclaude/cli/sprint/classifiers.py`
2. Define `CLASSIFIERS: dict[str, Callable[[int, str, str], str]]`
3. Implement `empirical_gate_v1` classifier
   - Signature: `(exit_code: int, stdout: str, stderr: str) -> str`
   - Returns classification label (e.g., `"pass"`, `"fail"`)
4. Validate classifier lookup: missing key raises `KeyError`
5. Wrap classifier invocation: catch exceptions, log at WARNING, return `"error"` classification, treat as `TaskStatus.FAIL`

**Tests (Phase 2):**
- Unit test `empirical_gate_v1` with known pass/fail inputs
- Unit test `KeyError` on missing classifier name
- Unit test exception handling in classifier invocation

**Deliverables:** New `classifiers.py` module.

> **Note:** Phases 1 and 2 are independent and can be developed in parallel.

### Phase 3: Preflight Executor Core and Evidence Artifacts

**Milestone: Preflight runs commands and produces all output artifacts**

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
5. Verify `_determine_phase_status()` parses generated results with no modifications

**Tests (Phase 3):**
- Integration test: preflight executes `echo hello` and captures output
- Integration test: timeout triggers after configured duration
- Integration test: evidence file written with correct structure
- Integration test: result file parseable by `_determine_phase_status()`
- Unit test: stdout/stderr truncation at limits
- Compatibility fixture: validate both preflight-origin and Claude-origin result files parse identically

**Deliverables:** New `preflight.py` module, evidence and result file generation.

### Phase 4: Sprint Integration and Skip Mode

**Milestone: End-to-end sprint with mixed modes works correctly**

1. Call `execute_preflight_phases()` in `execute_sprint()` before the main phase loop
2. Main loop skips phases where `execution_mode == "python"` (already handled by preflight)
3. Main loop skips phases where `execution_mode == "skip"` with `PhaseStatus.SKIPPED`
4. Merge preflight `PhaseResult` list with main loop results for final sprint outcome
5. Verify logger and TUI handle `PREFLIGHT_PASS` and `SKIPPED` without errors

**Tests (Phase 4):**
- Integration test: sprint with mixed `python`/`claude`/`skip` phases produces correct combined results
- Integration test: removing `execute_preflight_phases()` call reverts to all-Claude behavior
- Integration test: `skip` phases produce `SKIPPED` status, no subprocess launched
- Integration test: zero `ClaudeProcess` instantiation for python-mode phases
- **Regression test: all-Claude tasklist (no python/skip phases) behaves identically to pre-feature behavior**

**Deliverables:** Modified `execute_sprint()` (in `process.py`), complete end-to-end flow.

### Phase 5: Validation, Polish, and Release Gate

**Milestone: All success criteria met, ready for merge**

1. Run full test suite: 14 unit + 8 integration tests passing
2. Verify SC-001: python-mode phase completes <30s with zero API tokens
3. Verify SC-002: nested `claude --print -p "hello"` works without deadlock
4. Verify SC-007: single-line rollback works — remove call, run existing suite, all pass
5. Run `make lint && make format`
6. Run `make sync-dev && make verify-sync`
7. Update execution log and any relevant documentation

**Release gate criteria:** Ship only when:
- All compatibility tests pass
- Performance is within threshold (<30s for 5 EXEMPT-tier tasks)
- Rollback is demonstrated
- No regression observed in all-Claude tasklists

**Deliverables:** Green test suite, passing lint, synced dev copies, confirmed release gate.

## Risk Assessment and Mitigation

### RISK-001: Result File Format Drift

**Severity:** High

**Why it matters:** If preflight-generated phase results diverge from Claude-generated format, `_determine_phase_status()` may fail, causing false halts or broken sprint completion logic.

**Mitigation:**
1. Reuse `AggregatedPhaseReport.to_markdown()` directly — no custom format generation
2. Shared compatibility fixture validates both preflight-origin and Claude-origin result files
3. Treat result format as a locked contract in this release

**Contingency:** If compatibility issues appear, block release until report generation is aligned. Do not patch `_determine_phase_status()` as a shortcut.

### RISK-002: Environment Mismatch for Local Commands

**Severity:** Medium

**Why it matters:** Preflight commands may depend on tools, environment variables, or binary availability not present in all execution contexts.

**Mitigation:**
1. Evidence files capture full stderr and environment context
2. Preflight logs exact command and duration for diagnosis
3. Execute in a predictable working directory

**Contingency:** Fail the affected task cleanly and emit actionable evidence rather than retrying implicitly.

### RISK-003: Command Quoting and Escaping Issues

**Severity:** Medium

**Why it matters:** Commands containing quotes, pipes, redirects, or nested CLI strings may break if parsing alters their content.

**Mitigation:**
1. Preserve command strings verbatim in parsing
2. Tokenize only at execution time with `shlex.split()`
3. Comprehensive test cases covering pipes, redirects, quoted arguments, and nested quoted commands
4. Document that shell metacharacters are preserved textually but not shell-expanded under `shell=False`

**Contingency:** If actual workflows require shell features, require explicit spec revision rather than silently enabling `shell=True`.

### RISK-004: Classifier Misclassification

**Severity:** Low

**Why it matters:** A flawed classifier can incorrectly promote or halt downstream work.

**Mitigation:**
1. Keep classifier logic simple and deterministic
2. Unit test built-ins against known fixtures
3. Fail closed on missing classifiers (`KeyError`)
4. Classifier exceptions caught, logged at WARNING, treated as task failure

**Contingency:** Allow registry updates in subsequent releases without executor redesign.

### RISK-005: Orchestration Regression in Existing Claude Flow

**Severity:** Medium

**Why it matters:** A poorly placed hook could unintentionally alter current sprint behavior for all-Claude tasklists.

**Mitigation:**
1. Insert preflight in one orchestrator location only
2. No changes to Claude-mode execution code path
3. Dedicated regression test for all-Claude tasklists
4. Verify one-line rollback property before merge

**Contingency:** Remove the `execute_preflight_phases()` call to revert immediately if late-stage regression is found.

### Additional Architect Concerns

- **Deadlock risk with nested Claude calls (SC-002):** `subprocess.run()` with `capture_output=True` uses pipes; large output from nested `claude --print` could theoretically fill pipe buffers. The 120s timeout is the backstop, and SC-002 explicitly validates this case.
- **`shlex.split()` on Windows:** Uses POSIX mode by default. If cross-platform support is needed, this requires `posix=False` on Windows. Current target is Linux-only, so this is acceptable.

## Resource Requirements

### Engineering Resources

| Role | Responsibility |
|------|---------------|
| Primary backend/CLI engineer | Parser updates, executor implementation, orchestration integration |
| QA/test coverage (same or separate engineer) | Unit/integration coverage, compatibility validation, performance validation |
| Architect/reviewer | Contract review for result/report compatibility, rollback path validation |

### Code Areas Impacted

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

### Dependencies

**Internal (existing, no modifications to their contracts):**
- `AggregatedPhaseReport.to_markdown()` — result file generation
- `_determine_phase_status()` — result file parsing (read-only contract)
- `parse_tasklist()` / `discover_phases()` — extended, not replaced

**Stdlib only:** `subprocess`, `shlex`, `time`, `pathlib` — no new external packages.

### Operational Dependencies
- Local tools referenced by preflight commands must exist in the execution environment
- CI/runtime environment must permit subprocess execution
- Artifact directories must be writable
- UV-based test execution must remain the only Python execution workflow

## Success Criteria and Validation Approach

### Criteria Mapping

| Criterion | Description | Validation Method | Phase |
|-----------|-------------|-------------------|-------|
| SC-001 | <30s, zero tokens for python-mode phase | Wall-clock timing + token counter assertion | 5 |
| SC-002 | Nested `claude --print` works without deadlock | Integration test with real subprocess | 4 |
| SC-003 | Parser compatibility | Shared fixture: preflight result → `_determine_phase_status()` | 3 |
| SC-004 | 14 unit tests pass | `uv run pytest tests/cli/sprint/test_preflight.py -m unit` | 5 |
| SC-005 | 8 integration tests pass | `uv run pytest tests/cli/sprint/test_preflight.py -m integration` | 5 |
| SC-006 | Skip mode works | Assert `PhaseStatus.SKIPPED`, no subprocess | 4 |
| SC-007 | Single-line rollback | Remove call, run existing test suite, all pass | 5 |
| SC-008 | Evidence artifacts complete | Assert file contents against schema | 3 |

### Validation Approach

**Functional validation:**
1. Parser tests for `Execution Mode`, `Command`, and `Classifier` extraction
2. Executor tests for successful, failing, and timing-out commands
3. Status tests for `PREFLIGHT_PASS` and `SKIPPED`
4. Integration tests for mixed preflight + Claude sprint runs

**Non-functional validation:**
1. Time-boxed benchmark for 5 EXEMPT-tier tasks (<30s)
2. Verification that python-mode phases do not instantiate `ClaudeProcess`
3. Rollback validation by removing the preflight hook call and rerunning Claude-only tests

**Regression validation:**
1. All-Claude tasklist produces identical behavior to pre-feature baseline
2. Existing test suite passes with no modifications

## Timeline Estimates

| Phase | Scope | Estimate |
|-------|-------|----------|
| Phase 1: Data Model & Parsing | 3 dataclass changes, parser extension, enum, validation | Small |
| Phase 2: Classifier Registry | 1 new module, 1 built-in classifier | Small |
| Phase 3: Preflight Executor & Artifacts | Core logic, evidence writing, result generation, compatibility | Medium |
| Phase 4: Sprint Integration | Orchestration changes, skip mode, regression test | Small-Medium |
| Phase 5: Validation & Release Gate | Test suite, lint, sync, docs, release criteria | Small |

**Parallelization:** Phases 1 and 2 are independent and can be developed concurrently. Phase 3 depends on both. Phase 4 depends on Phase 3. Phase 5 is a final sweep.

## Open Questions Resolution

| OQ | Resolution | Status |
|----|-----------|--------|
| OQ-001 (multi-line commands) | Defer. If encountered, treat `\`-continuations as part of the raw string passed to `shlex.split()`. Add a test case but don't over-engineer. | Resolved |
| OQ-002 (dry-run interaction) | List python-mode phases with `[preflight]` tag in dry-run output. Low effort, high clarity. | Resolved |
| OQ-003 (classifier exceptions) | Catch, log at WARNING, return `"error"` classification, treat as `TaskStatus.FAIL`. Add to FR-004 acceptance criteria. | Resolved |
| OQ-004 (--phases filter) | Respect `--phases` for preflight phases too. If `--phases 2,3` excludes Phase 1, preflight skips it. Consistent behavior. | Resolved |
| OQ-005 (ordering constraint) | Implement python-first ordering but **do not document as a guaranteed contract**. Flag for stakeholder confirmation before enshrining as permanent behavior. This preserves flexibility for future interleaved execution without creating backward-compatibility constraints. | Pending stakeholder input |
