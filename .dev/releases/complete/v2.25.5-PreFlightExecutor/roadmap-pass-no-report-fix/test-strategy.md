---
validation_milestones: 5
interleave_ratio: "1:2"
---

# Test Strategy: Pass-No-Report Fix (Preliminary Result Writer)

## 1. Validation Milestones Mapped to Roadmap Phases

### M0 — Baseline Validation (Phase 0)
**Purpose**: Establish green baseline and resolve all open questions before any code changes.

**Tests to run**:
- `uv run pytest tests/sprint/ -v` — full suite, record exact pass/fail count
- Triage any pre-existing failures; block implementation until suite is green

**Reconnaissance checks** (not test failures, but blocking gates):
- OQ-001: Read `ClaudeProcess.__init__` to confirm phase attribute name
- OQ-002: Confirm line numbers for `started_at`, `finished_at`, signal handler, `_determine_phase_status()` call
- OQ-003: Confirm `_write_crash_recovery_log()` and `_write_executor_result_file()` locations
- OQ-005: Verify `_determine_phase_status()` does not raise on `exit_code < 0`
- OQ-007: Confirm `debug_log` is in scope at injection site
- OQ-008: Verify `_setup_tui_monitor_mocks` helper exists in test files

**Gate**: Suite green + all OQs answered. No code changes until M0 closes.

---

### M1 — Unit Tests for `_write_preliminary_result()` (Phase 1)
**Purpose**: Validate the new function's file-state matrix in complete isolation.

**Test file**: `tests/sprint/test_executor.py`

| Test ID | Description | Input State | Expected Outcome |
|---------|-------------|-------------|------------------|
| T-001 | File absent | No result file | Returns `True`, file contains `EXIT_RECOMMENDATION: CONTINUE\n` |
| T-002 | Fresh non-empty agent file | `st_mtime >= started_at`, `st_size > 0` | Returns `False`, file unchanged |
| T-002b | Zero-byte file | `st_size == 0` | Returns `True`, file overwritten with CONTINUE |
| T-003-stale | Stale file (`st_mtime < started_at`) | Any content, stale mtime | Returns `True`, file overwritten with CONTINUE |
| T-005 | `OSError` on write | Filesystem write fails | Returns `False`, no exception raised, WARNING logged |

**Assertions per test**:
- T-001: `result == True`, `path.read_text() == "EXIT_RECOMMENDATION: CONTINUE\n"`
- T-002: `result == False`, original content unchanged
- T-002b: `result == True`, `path.read_text() == "EXIT_RECOMMENDATION: CONTINUE\n"`
- T-003-stale: `result == True`, content overwritten
- T-005: `result == False`, `caplog` contains WARNING

**Run command**: `uv run pytest tests/sprint/test_executor.py -v -k "preliminary_result"`

**Gate**: All 5 unit tests pass. Sentinel contract comment present in `_determine_phase_status()`.

---

### M2 — Integration Tests for `execute_sprint()` (Phase 2)
**Purpose**: Validate end-to-end flow from subprocess exit through status classification.

**Test file**: `tests/sprint/test_phase8_halt_fix.py`

| Test ID | Description | Setup | Expected `PhaseStatus` |
|---------|-------------|-------|----------------------|
| T-003 | `exit_code=0`, no agent file | Popen mock returns 0, no result file written | `PASS` (not `PASS_NO_REPORT`) |
| T-004 | Non-zero exit code | Popen mock returns 1 | `_write_preliminary_result` NOT called; status unchanged |
| T-006 | Stale HALT from prior run | Result file exists with HALT content, `st_mtime < started_at` | `PASS` (not `HALT`) |

**Additional assertions for T-003**:
- `config.result_file(phase).read_text()` contains `EXIT_RECOMMENDATION: CONTINUE` after executor overwrite
- `PhaseStatus.PASS` returned (SC-004, SC-005)

**Regression verification**:
- `PhaseStatus.PASS_NO_REPORT` still present in enum
- Direct calls to `_determine_phase_status()` with no file still return `PASS_NO_REPORT`
- `TestBackwardCompat.test_three_arg_call` (DEP-005) still passes

**Run command**: `uv run pytest tests/sprint/ -v`

**Gate**: T-003, T-004, T-006 pass. Zero regressions in full suite.

---

### M3 — Prompt Contract Test (Phase 3)
**Purpose**: Validate `build_prompt()` section ordering and content correctness.

**Test file**: `tests/sprint/test_executor.py` or dedicated prompt test

| Test | Assertion |
|------|-----------|
| Section ordering | `prompt.rindex("## Result File") > prompt.rindex("## Important")` |
| Path correctness | Path in `## Result File` is absolute POSIX format matching `config.result_file(phase).as_posix()` |
| Content instruction | Prompt contains `EXIT_RECOMMENDATION: CONTINUE` instruction |
| No section reordering | `## Sprint Context`, `## Execution Rules`, `## Scope Boundary` appear before `## Result File` |
| No hardcoded paths | Prompt path changes when `config.result_file(phase)` changes |

**Run command**: `uv run pytest tests/sprint/ -v`

**Gate**: Prompt ordering test passes. Zero regressions.

---

### M4/M5 — Full Validation and Release Gate (Phase 4)
**Purpose**: Regression-resistant confirmation of all 13 success criteria.

**Automated layers** (run in order):
1. `uv run pytest tests/sprint/test_executor.py -v` — unit layer
2. `uv run pytest tests/sprint/test_phase8_halt_fix.py -v` — integration layer
3. `uv run pytest tests/sprint/ -v` — full regression suite

**Manual validation** (if environment permits):
- Run v2.25.5 sprint, confirm phases 1–5 report `pass` not `pass_no_report` (SC-008)
- Rerun in same output directory with stale result files — confirm `pass` not `HALT` (SC-009)

**Architect sign-off checklist**:
- [ ] `_write_preliminary_result()` importable with correct signature (SC-001)
- [ ] `PhaseStatus.PASS_NO_REPORT` in enum, reachable via direct classifier call (SC-010)
- [ ] Ordered-triple invariant documented in docstring (FR-008)
- [ ] Concurrency limitation documented in docstring (NFR-002)
- [ ] No path construction outside `config.result_file(phase)` (NFR-005)
- [ ] No classifier signature changes (NFR-004)

**Gate**: All 5 layers pass. All 13 success criteria satisfied (SC-001 through SC-013).

---

## 2. Test Categories

### Unit Tests
**Location**: `tests/sprint/test_executor.py`
**Scope**: `_write_preliminary_result()` in isolation, mocked filesystem

| ID | What | File State Tested |
|----|------|-------------------|
| T-001 | Write when absent | Absent |
| T-002 | No-op on fresh non-empty file | Fresh, non-empty |
| T-002b | Overwrite zero-byte file | Zero-byte |
| T-003-stale | Overwrite stale file | Stale mtime |
| T-005 | OSError handling | Write failure |

**Mocking strategy**: Use `tmp_path` pytest fixture for real filesystem I/O (preferred over mocking `pathlib`). Mock `OSError` by making the path read-only or patching `Path.write_text`.

### Integration Tests
**Location**: `tests/sprint/test_phase8_halt_fix.py`
**Scope**: Full `execute_sprint()` call with Popen mocked

| ID | What | Integration Surface |
|----|------|---------------------|
| T-003 | PASS_NO_REPORT → PASS regression | execute_sprint + classifier + file I/O |
| T-004 | Non-zero exit isolation | execute_sprint guard |
| T-006 | Stale HALT rerun | execute_sprint + mtime + classifier |

**Mocking strategy**: Use existing `_setup_tui_monitor_mocks` pattern (OQ-008). Patch `subprocess.Popen` to return controlled `returncode`. Use real `tmp_path` for result files to test actual mtime behavior.

### End-to-End / Acceptance Tests
**Location**: Manual validation or `tests/sprint/test_e2e.py` (if exists)
**Scope**: Full sprint execution against v2.25.5 task list

| Scenario | Expected |
|----------|----------|
| Fresh run, phases succeed, no agent writes | All phases report `PASS` |
| Rerun same output dir (stale HALT files) | All phases report `PASS` |
| Agent writes valid HALT on STRICT failure | Phase reports `HALT` |

### Regression Tests (Existing Suite Preservation)
All tests in `tests/sprint/` must remain unmodified and green:
- Direct `_determine_phase_status()` call tests asserting `PASS_NO_REPORT` — must continue passing
- `TestBackwardCompat.test_three_arg_call` — must continue passing
- TIMEOUT, ERROR, INCOMPLETE, PASS_RECOVERED path tests — must continue passing
- PREFLIGHT_PASS path tests — must continue passing

---

## 3. Test-Implementation Interleaving Strategy

**Ratio**: 1:2 (one test-writing/verification cycle per 2 implementation units)

```
Phase 0: Read + verify baseline (no code changes)
    └── Run full suite → record baseline

Phase 1: Implement _write_preliminary_result()
    └── Write T-001, T-002, T-002b, T-003-stale, T-005 IMMEDIATELY after function body
    └── Run: uv run pytest tests/sprint/test_executor.py -v
    └── GATE: all 5 unit tests green before proceeding

Phase 2: Implement execute_sprint() injection
    └── Write T-003, T-004, T-006 IMMEDIATELY after injection
    └── Run: uv run pytest tests/sprint/ -v
    └── GATE: all 3 integration tests green, 0 regressions before proceeding

Phase 3: Implement build_prompt() update
    └── Write prompt ordering test IMMEDIATELY after prompt change
    └── Run: uv run pytest tests/sprint/ -v
    └── GATE: prompt test green, 0 regressions before proceeding

Phase 4: Run all layers in sequence
    └── No new code — validation only
```

**Rationale**: Tests written immediately after each function body while implementation context is fully loaded. This prevents drift between implementation intent and test assertions, and catches ordering-invariant violations before they propagate.

---

## 4. Risk-Based Test Prioritization

Tests are ordered by severity of failure mode if missed:

| Priority | Test | Risk Addressed | Failure Mode if Missed |
|----------|------|----------------|------------------------|
| P0 (Critical) | T-002 | RISK-002: Fresh HALT overwritten | Silently suppresses legitimate HALT — no exception raised |
| P0 (Critical) | T-006 | RISK-001: Stale HALT on rerun | False HALT on every rerun in same directory |
| P0 (Critical) | T-003 | SC-004/SC-005: Core regression | `PASS_NO_REPORT` still returned — patch has no effect |
| P1 (High) | T-004 | RISK-004: Non-zero exit regression | TIMEOUT/ERROR silently reclassified |
| P1 (High) | T-001 | Happy path: absent file | Primary fix mechanism untested |
| P2 (Medium) | T-002b | RISK-005: Zero-byte file | Ambiguous success state persists |
| P2 (Medium) | T-005 | RISK-006: OSError fallback | Silent write failure not detected |
| P3 (Low) | Prompt ordering | SC-013: Agent instruction quality | Agent writes to wrong path more often |
| P3 (Low) | Regression suite | NFR-003: Backward compat | Unknown breakage in existing paths |

**Key insight**: T-002 and T-006 are the highest-priority tests because their failure modes are silent — incorrect classification with no exception or log warning. These must be written and green before any integration work begins.

---

## 5. Acceptance Criteria Per Milestone

### M0 Acceptance Criteria
- `uv run pytest tests/sprint/ -v` exits 0 with recorded pass count
- All 8 OQs have documented answers
- No blocking unknowns (especially OQ-005 re: negative exit codes)

### M1 Acceptance Criteria
- T-001 through T-005 (5 unit tests) all pass
- Function signature matches `(config: SprintConfig, phase: Phase, started_at: float) -> bool`
- Sentinel contract comment present in `_determine_phase_status()` at CONTINUE parsing point
- No regressions in existing test suite

### M2 Acceptance Criteria
- T-003: `exit_code=0` + no agent file → `PhaseStatus.PASS` (SC-004)
- T-003: final file content contains `EXIT_RECOMMENDATION: CONTINUE` (SC-005)
- T-004: `_write_preliminary_result` not called on non-zero exit
- T-006: stale HALT results in `PASS` not `HALT` (SC-007)
- `PhaseStatus.PASS_NO_REPORT` still in enum, reachable via direct call (SC-010)
- `uv run pytest tests/sprint/ -v`: 0 regressions (SC-011)

### M3 Acceptance Criteria
- `prompt.rindex("## Result File") > prompt.rindex("## Important")` (SC-013)
- Path in section is absolute POSIX, matches `config.result_file(phase).as_posix()`
- No existing prompt sections repositioned
- `uv run pytest tests/sprint/ -v`: 0 regressions

### M4/M5 Acceptance Criteria (Release Gate)
All 13 success criteria satisfied:
- SC-001 through SC-013 all verified (see roadmap table)
- Architect sign-off checklist complete
- Manual E2E validation complete (or documented waiver with rationale)
- Zero regressions in full sprint test suite

---

## 6. Quality Gates Between Phases

```
Phase 0 → Phase 1:
  GATE: uv run pytest tests/sprint/ -v exits 0
  GATE: All OQs answered (especially OQ-001, OQ-005, OQ-008)
  BLOCK: Any pre-existing test failures not triaged

Phase 1 → Phase 2:
  GATE: uv run pytest tests/sprint/test_executor.py -v exits 0 (T-001, T-002, T-002b, T-003-stale, T-005)
  GATE: Sentinel contract comment present in _determine_phase_status()
  GATE: Ordered-triple invariant documented in _write_preliminary_result() docstring
  GATE: Concurrency limitation documented in docstring
  BLOCK: Any unit test failure

Phase 2 → Phase 3:
  GATE: uv run pytest tests/sprint/ -v exits 0 (all T-003, T-004, T-006 pass)
  GATE: PhaseStatus.PASS_NO_REPORT still in enum
  GATE: TestBackwardCompat.test_three_arg_call passes
  BLOCK: Any integration test failure or regression

Phase 3 → Phase 4:
  GATE: uv run pytest tests/sprint/ -v exits 0 (prompt ordering test passes)
  GATE: No existing prompt sections repositioned
  BLOCK: Any regression

Phase 4 → Merge:
  GATE: All 5 validation layers complete (unit, integration, regression, architect checklist, manual)
  GATE: All 13 SC-001–SC-013 satisfied
  GATE: Zero regressions in full sprint suite
  BLOCK: Any SC violation
  BLOCK: Missing docstring invariants
  BLOCK: Manual E2E not completed (or explicit documented waiver)
```

**Hard rule**: Do not merge until Phase 4 full regression passes. The ordering invariant (RISK-001) and fresh-HALT preservation (RISK-002) are silent failure modes — no exception is raised if violated. Only the test matrix catches them.
