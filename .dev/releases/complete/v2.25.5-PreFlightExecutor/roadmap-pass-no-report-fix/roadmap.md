---
spec_source: pass-no-report-fix-spec.md
complexity_score: 0.62
adversarial: true
---

# Roadmap: Pass-No-Report Fix (Preliminary Result Writer)

## Executive Summary

This roadmap addresses a defect in the sprint executor where phases completing with `exit_code == 0` but no agent-written result file produce `PASS_NO_REPORT` instead of `PASS`. The fix introduces a deterministic fallback: a preliminary result file written by the executor immediately after a successful subprocess exit, ensuring `_determine_phase_status()` always finds a valid result file for passing phases.

The change surface is small (~60 lines across 2 source files) but architecturally sensitive due to a strict ordering invariant across three functions and mtime-based freshness semantics. The roadmap front-loads verification and baseline establishment before any code changes, with interleaved testing as the default cadence.

### Target Outcome

After implementation:

- Successful phases with no agent result file classify as `PhaseStatus.PASS`.
- Fresh agent-written `HALT` files remain authoritative.
- Stale or zero-byte files are safely replaced with `EXIT_RECOMMENDATION: CONTINUE`.
- Final executor report still overwrites the preliminary file as the authoritative end state.
- Python/skip preflight phases remain unaffected.
- `PhaseStatus.PASS_NO_REPORT` remains in the enum and reachable via direct classifier calls.

### Architectural Approach

Implement as a localized patch in `executor.py` and `process.py`, with no signature changes to `_determine_phase_status()` and no expansion of scope into unrelated execution paths. This minimizes regression risk while satisfying all functional and non-functional requirements.

## Phased Implementation Plan

### Phase 0: Baseline Validation and Code Reconnaissance

**Milestone M0**: Implementation prerequisites verified, no hidden blockers found.

**Timeline**: 0.25 phase-days

#### Actions

1. **Run pre-implementation baseline**
   - Execute `uv run pytest tests/sprint/ -v` and record pass/fail counts
   - If any failures exist, triage and resolve before proceeding

2. **Resolve open questions by reading source**
   - OQ-001: Confirm exact attribute name in `ClaudeProcess.__init__` for phase access (`self.phase` vs `self._phase`)
   - OQ-002: Verify current line numbers in `execute_sprint()` for `started_at`, `finished_at`, signal handler check, and `_determine_phase_status()` call
   - OQ-003: Locate `_write_crash_recovery_log()` and `_write_executor_result_file()` definitions for insertion point
   - OQ-004: Confirm `started_at` capture site (subprocess launch, not executor startup)
   - OQ-005: Verify `_determine_phase_status()` handles `exit_code < 0` correctly; if it raises, flag as blocking prerequisite
   - OQ-006: Confirm `debug_log` availability and behavior at the injection site
   - OQ-007: Confirm `_setup_tui_monitor_mocks` helper existence in test files
   - OQ-008: Verify any existing tests asserting `PASS_NO_REPORT` as direct output of `execute_sprint()` with `exit_code=0` — confirm they are isolated direct-call tests, not integration tests

3. **Inspect `_determine_phase_status()` body**
   - Confirm `PASS_NO_REPORT` code path
   - Confirm sentinel parsing for `CONTINUE`
   - Confirm negative exit code handling

#### Exit Criteria

All open questions answered. Baseline test suite green. No blocking unknowns identified. OQ identifiers are informational tracking; formal resolution records are not required as a gate, but answers must be captured before Phase 1 begins.

---

### Phase 1: Core Implementation — `_write_preliminary_result()`

**Milestone M1**: Deterministic preliminary result writer implemented with freshness and safety semantics, unit-tested in isolation.

**Timeline**: 0.5 phase-days

#### Implementation

1. **Add `_write_preliminary_result()` to `executor.py`**
   - Insert after `_write_crash_recovery_log()`, before `_write_executor_result_file()` (insertion point confirmed in M0)
   - Signature: `(config: SprintConfig, phase: Phase, started_at: float) -> bool`
   - Freshness guard: if file `exists() AND st_size > 0 AND st_mtime >= started_at` → no-op, return `False`
   - Zero-byte files treated as absent → overwrite
   - Stale files (`st_mtime < started_at`) treated as absent → overwrite
   - `mkdir(parents=True, exist_ok=True)` before write
   - Write exactly `EXIT_RECOMMENDATION: CONTINUE\n`
   - Wrap in `try/except OSError` with WARNING log, return `False` on error
   - Return `True` if the file was written by this function (Option D path); return `False` if the file was a no-op (fresh agent-written file preserved) or if an OSError prevented the write
   - The boolean return value is used by the Phase 2 call site to log telemetry: `_wrote_preliminary = _write_preliminary_result(...)` then `debug_log(f"preliminary_result_write path={'option_d' if _wrote_preliminary else 'option_a_or_noop'}")`
   - Document in docstring:
     - Ordering invariant: must be called after `finished_at` and before `_determine_phase_status()`
     - Single-threaded concurrency assumption (current); `O_EXCL` required if parallelized in future
     - Sentinel contract: `EXIT_RECOMMENDATION: CONTINUE` is the exact string parsed by the classifier

2. **Add sentinel contract comment in `_determine_phase_status()`** (NFR-006)
   - At the `CONTINUE` sentinel parsing point, add a comment documenting the contract
   - Place here in Phase 1 while implementation context is fully loaded — do not defer

#### Unit Tests (T-001, T-002, T-002b, T-005)

Add to `tests/sprint/test_executor.py`:

- **T-001**: `_write_preliminary_result()` writes file when absent → returns `True`, content is `EXIT_RECOMMENDATION: CONTINUE\n`
- **T-002**: Fresh non-empty agent file preserved (`st_mtime >= started_at`, `st_size > 0`) → returns `False`, file unchanged
- **T-002b**: Zero-byte file treated as absent → overwritten, returns `True`
- **T-005**: `OSError` on write → returns `False`, no exception raised, WARNING emitted
  via the module logger (`logging.getLogger(__name__)`) with the exact message format:
  `"preliminary result write failed: %s; phase may report PASS_NO_REPORT"` (FR-001)

  ```python
  def test_write_preliminary_result_oserror_returns_false_and_warns(tmp_path, caplog):
      """OSError on write must be caught: returns False, no exception propagated, WARNING logged."""
      from superclaude.cli.sprint.executor import _write_preliminary_result
      import logging

      config = _make_config(tmp_path)
      phase = config.phases[0]
      started_at = datetime.now(timezone.utc).timestamp() - 1

      result_path = config.result_file(phase)
      with patch.object(type(result_path), "write_text", side_effect=OSError("disk full")):
          with caplog.at_level(logging.WARNING, logger="superclaude.cli.sprint.executor"):
              return_val = _write_preliminary_result(config, phase, started_at)

      assert return_val is False, "OSError path must return False, not raise"
      assert any(
          "preliminary result write failed" in r.message
          for r in caplog.records
          if r.levelno == logging.WARNING
      ), "A WARNING containing 'preliminary result write failed' must be logged"
  ```

  **Note on logger patching**: The `caplog`-based approach is implementation-agnostic — it captures the WARNING regardless of whether the implementation uses a module-level `logger = logging.getLogger(__name__)` or an inline `_logging.getLogger(__name__)` pattern inside the `except OSError` block. The test MUST assert `return_val is False`. The WARNING message must contain `"preliminary result write failed"`.

**Run**: `uv run pytest tests/sprint/test_executor.py -v` — all 4 new tests pass before proceeding.

#### Exit Criteria

`_write_preliminary_result()` passes all unit tests (T-001, T-002, T-002b, T-005). Function signature is `-> bool`; returns `True` on write, `False` on no-op or OSError. Sentinel contract comment in place per NFR-006 (comment added at the `CONTINUE`-check point inside `_determine_phase_status()` documenting the `EXIT_RECOMMENDATION: CONTINUE` sentinel contract). TOCTOU/concurrency limitation documented in `_write_preliminary_result()` docstring per NFR-002. No regressions in existing test suite.

---

### Phase 2: Execution Flow Integration in `execute_sprint()`

**Milestone M2**: Execution flow updated with ordered-triple invariant preserved.

**Timeline**: 0.25 phase-days

#### Implementation

1. **Insert call site in `execute_sprint()`** (FR-002)
   - Location: after `finished_at = datetime.now(timezone.utc)` and signal/shutdown check, before `_determine_phase_status()`
   - Guard: `if exit_code == 0:`
   - Call: `_write_preliminary_result(config, phase, started_at.timestamp())`
   - Log at DEBUG level using combined terminology: primary labels `executor-preliminary` / `agent-written` (operator-readable), with `option_d` / `option_a_or_noop` as parenthetical context in the DEBUG message body

2. **Verify ordering invariant** (FR-001 ordering invariant, FR-002)
   - Confirm the three calls appear in this exact order:
     1. `_write_preliminary_result()`
     2. `_determine_phase_status()`
     3. `_write_executor_result_file()`

3. **Verify non-zero exit paths untouched** (FR-005, NFR-001)
   - Trace TIMEOUT, ERROR, INCOMPLETE, PASS_RECOVERED paths — none should reach `_write_preliminary_result()`
   - Explicitly verify `exit_code < 0` (signal-killed subprocess, e.g. SIGKILL=-9, SIGTERM=-15): `_determine_phase_status()` must fall through to ERROR or INCOMPLETE without raising — not raise an exception (NFR-001)

4. **Verify preflight isolation** (FR-009)
   - Confirm python/skip phases handled by `execute_preflight_phases()` never reach the new code

#### Integration Tests (T-003, T-004, T-006)

Add to `tests/sprint/test_phase8_halt_fix.py`:

- **T-003**: Full `execute_sprint()` with `exit_code=0`, no agent file → `PhaseStatus.PASS`, final file contains `EXIT_RECOMMENDATION: CONTINUE` (SC-004, SC-005)
- **T-004**: `execute_sprint()` with non-zero exit code → `_write_preliminary_result()` NOT called, existing status unchanged
- **T-006**: Stale HALT file from prior run (`st_mtime < started_at`) → overwritten with CONTINUE, result is `PASS` not `HALT` (SC-007)

**Run**: `uv run pytest tests/sprint/ -v` — 0 regressions (SC-002, SC-003, SC-011).

#### Exit Criteria

All new integration tests pass. Full sprint test suite green. `PhaseStatus.PASS_NO_REPORT` still in enum and reachable via direct calls (SC-010, NFR-004).

---

### Phase 3: Prompt Contract Reinforcement in `build_prompt()`

**Milestone M3**: Agent prompt contract strengthened without architectural dependency on agent compliance.

**Timeline**: 0.25 phase-days

#### Implementation

1. **Add `## Result File` section to `build_prompt()` in `process.py`** (FR-006)
   - Append as the LAST `##`-level section, after `## Important`
   - Include exact path via `config.result_file(self.phase).as_posix()` (attribute name confirmed in M0 via OQ-001)
   - Include content instruction: content must be exactly `EXIT_RECOMMENDATION: CONTINUE`
   - Include conditional HALT instruction only for STRICT-tier failure scenarios
   - Preserve existing prompt section order — only the final append changes

2. **Write prompt assertion test**
   - Verify `prompt.rindex("## Result File") > prompt.rindex("## Important")` (SC-013)
   - Verify path is formatted using `config.result_file(self.phase).as_posix()` — assert the path string in the prompt exactly matches `config.result_file(phase).as_posix()` (FR-006 constraint: `as_posix()` is required, not just "absolute with POSIX separators" — a relative POSIX path would satisfy the weaker check but violate the spec)
   - Confirm OQ-001 was resolved in M0: the attribute name used in `build_prompt()` must match the actual attribute set by `ClaudeProcess.__init__` — do not assume `self.phase` without verifying against the constructor (FR-006)
   - Verify no existing sections repositioned

**Run**: `uv run pytest tests/sprint/ -v` — 0 regressions.

#### Exit Criteria

Prompt contains correctly positioned `## Result File` section. Prompt-order test passes. All tests green.

---

### Phase 4: Full Validation and Release Hardening

**Milestone M4/M5**: Regression-resistant validation matrix confirmed. Patch validated, backward compatibility confirmed, ready for merge.

**Timeline**: 0.75 phase-days

#### Validation Layers

##### Layer 1: Baseline Confirmation
- Confirm pre-implementation baseline was captured (M0 gate).

##### Layer 2: Unit Validation
- Run `uv run pytest tests/sprint/test_executor.py -v`
- Verify T-001, T-002, T-002b, T-005 pass (all unit states: absent, fresh, stale, zero-byte, error)

##### Layer 3: Integration Validation
- Run `uv run pytest tests/sprint/test_phase8_halt_fix.py -v`
- Verify T-003, T-004, T-006 pass (exit_code=0 no-file, non-zero exit, stale HALT rerun)

##### Layer 4: Regression Validation
- Run `uv run pytest tests/sprint/ -v` (SC-011)
- Confirm zero regressions outside intended scope

##### Layer 5: Architect Sign-off Checks
- `_write_preliminary_result()` importable with correct signature (SC-001)
- `PhaseStatus.PASS_NO_REPORT` remains in enum and reachable via direct classifier invocation (SC-010)
- TIMEOUT, ERROR, INCOMPLETE, PASS_RECOVERED behaviors unchanged; `exit_code < 0` handled without exception (SC-006c, NFR-001)
- Python/skip preflight phases still yield `PREFLIGHT_PASS` (architecture invariant from §5 Implication 9; not a spec §9 acceptance criterion — verified by tracing `execute_preflight_phases()` code path)
- Ordered-triple invariant is documented in docstring
- Concurrency limitation documented, not silently ignored
- No new path construction logic introduced outside `config.result_file(phase)`
- No classifier signature or enum contract changes

#### Manual Validation (if environment permits)
- Run v2.25.5 sprint, confirm phases 1–5 report `pass` not `pass_no_report` (SC-008)
- Re-run in same output directory to confirm stale file handling (SC-009)

#### Exit Criteria

All 5 validation layers pass. All 16 success criteria satisfied (SC-001 through SC-013, plus SC-006b, SC-006c, and SC-014). Consolidated testing acceptable if implementer has prior sprint executor familiarity; interleaved cadence (Phases 1–3) is the default recommendation for safety.

---

## Risk Assessment

| Risk | Severity | Impact | Mitigation | Phase |
|------|----------|--------|------------|-------|
| RISK-001: Ordering invariant violation | High | Classification breaks silently | Docstring + integration test encoding sequence | P1, P2 |
| RISK-002: Fresh agent HALT overwritten | High | Suppresses legitimate HALT | Freshness guard: `exists && st_size > 0 && st_mtime >= started_at` + T-002 | P1 |
| RISK-003: Stale file causes incorrect HALT on rerun | Medium | False HALT on rerun | `st_mtime` vs `started_at` comparison; overwrite stale files + T-006 | P1, P2 |
| RISK-004: Non-zero exit path regression | High | TIMEOUT/ERROR/INCOMPLETE reclassified | `if exit_code == 0` guard only; trace all non-zero paths + T-004 | P2 |
| RISK-005: Zero-byte agent file | Medium | Ambiguous success state | `st_size > 0` check; treat as absent + T-002b | P1 |
| RISK-006: OSError on write | Low | File not written; PASS_NO_REPORT returns | `try/except OSError` + WARNING log + T-005 | P1 |
| RISK-007: Agent writes to wrong path | Medium | File not found by classifier | Absolute POSIX path in prompt; Option D is deterministic fallback | P3 |
| RISK-008: TOCTOU race (future) | Low now, High if parallelized | Incorrect file state under concurrent writers | Document single-threaded assumption; `O_EXCL` follow-up note; no premature redesign | P1 (docstring) |
| RISK-009: Existing tests break | None (by design) | — | Pre-implementation baseline (M0); guard-only insertion | P0, P2 |
| RISK-010: OQ not resolved before implementation | Medium | Incorrect insertion point or attribute name | All OQs gated at M0; named for cross-referencing | P0 |

**Highest-priority risks**: Ordering invariant (RISK-001) and fresh HALT overwrite (RISK-002). These are silent failure modes — no exception is raised, but phase classification becomes incorrect. The docstring and T-002/T-006 tests are the primary defect-prevention mechanisms.

## Resource Requirements

### Files Modified

| File | Role | Change Type |
|------|------|-------------|
| `src/superclaude/cli/sprint/executor.py` | Primary | New function + injection site |
| `src/superclaude/cli/sprint/process.py` | Secondary | Prompt section addition |
| `tests/sprint/test_executor.py` | Tests | T-001, T-002, T-002b, T-005 |
| `tests/sprint/test_phase8_halt_fix.py` | Tests | T-003, T-004, T-006 |

### Technical Dependencies

- `SprintConfig.result_file(phase)` as the canonical result path source
- `PhaseStatus` enum retaining `PASS_NO_REPORT`
- Filesystem metadata support: `st_size`, `st_mtime`
- Python stdlib only: `pathlib`, `os`, `logging`, `datetime`
- Test infrastructure: `unittest.mock` (existing patterns)
- UV-based test execution environment

No new packages, no schema changes, no configuration changes.

### Human Resources

- **1 backend/CLI engineer** with sprint executor familiarity
- **1 QA reviewer** focused on: success-path classification, stale-file rerun behavior, negative exit-code safety — separate from the implementer to avoid anchoring bias on self-review
- **Lightweight architecture review** recommended: behavior hinges on sequencing rather than large code changes; concurrency implications must be documented accurately

## Success Criteria and Validation Approach

| ID | Criterion | Verified In |
|----|-----------|-------------|
| SC-001 | `_write_preliminary_result()` importable with correct signature | P1 |
| SC-002 | `test_executor.py` passes | P2 |
| SC-003 | `test_phase8_halt_fix.py` passes | P2 |
| SC-004 | `exit_code=0` + no agent file → `PhaseStatus.PASS` | P2 (T-003) |
| SC-005 | Final file contains `EXIT_RECOMMENDATION: CONTINUE` | P2 (T-003) |
| SC-006 | Zero-byte file overwritten → `CONTINUE` written, phase reports `PASS` (T-002b) | P1 |
| SC-006b | `_write_preliminary_result()` returns `False` and logs WARNING on `OSError` (T-005) | P1 |
| SC-006c | `TIMEOUT`, `ERROR`, `INCOMPLETE`, `PASS_RECOVERED` behaviors unchanged; `exit_code < 0` falls to `ERROR`/`INCOMPLETE` without exception (NFR-001) | P2 |
| SC-007 | Stale HALT not propagated | P2 (T-006) |
| SC-008 | Sprint rerun reports `pass` | P4 (manual) |
| SC-009 | Rerun in same dir handles stale files | P4 (manual) |
| SC-010 | `PASS_NO_REPORT` remains in enum and reachable via direct classifier | P2 |
| SC-011 | Full sprint test suite: 0 regressions | P2, P3, P4 |
| SC-012 | Pre-implementation baseline green: `uv run pytest tests/sprint/ -v` passes before any code changes | P0 |
| SC-013 | `## Result File` is last `##` section in built prompt | P3 |
| SC-014 | Sentinel contract comment present in `_determine_phase_status()` at `CONTINUE`-check point (NFR-006) | P1 |

### Critical Path

Phases are strictly sequential with this dependency chain:

1. M0 (baseline + OQ resolution) before any code changes
2. M1 (function + unit tests) before injection
3. M2 (injection + integration tests) before prompt work
4. M3 (prompt update) before full validation
5. M4/M5 (full suite) before merge

**Do not merge until Phase 4 full sprint regression passes.**

## Timeline Estimates

| Phase | Description | Estimate |
|-------|-------------|----------|
| P0 | Baseline Validation and Reconnaissance | 0.25 phase-days |
| P1 | Preliminary Result Writer + Unit Tests | 0.50 phase-days |
| P2 | `execute_sprint()` Integration + Integration Tests | 0.25 phase-days |
| P3 | Prompt Contract Update | 0.25 phase-days |
| P4 | Full Validation and Release Hardening | 0.75 phase-days |
| **Total** | | **2.0 phase-days** |

Estimates are subject to revision after P0 closes open questions. If OQ-005 reveals that `_determine_phase_status()` raises on negative exit codes, a prerequisite fix adds approximately 0.5 phase-days.

## Architect Recommendation Summary

1. **Keep this fix narrow and deterministic.** Do not redesign classification logic. Prepare classifier inputs (write a preliminary file) instead of modifying classifier contracts (`_determine_phase_status()` signature unchanged).

2. **Treat sequencing as the real architecture.** The main risk is not implementation size — it is execution order. The ordered triple `_write_preliminary_result()` → `_determine_phase_status()` → `_write_executor_result_file()` is the architectural invariant this patch depends on. Document it; test it; do not abstract it away.

3. **Preserve authority boundaries.** Agent output is advisory. Executor output is authoritative. A fresh agent-written HALT must still be respected by the freshness guard. The executor's final write always wins at the end.

4. **Document future concurrency debt explicitly.** Current logic is acceptable only because execution is single-threaded. The `exists/stat/write_text` sequence is not safe under concurrent writers. Record this in the docstring; file a follow-up for `O_EXCL` if parallelization is ever introduced.

5. **Test the file-state matrix, not just the happy path.** Missing, fresh, stale, zero-byte, and malformed file states are the true architecture surface here. T-001 through T-006 must cover this matrix before the patch is considered validated.
