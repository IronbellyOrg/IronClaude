# D-0046: Grep-Audit Report — mock.patch on Gate Functions / Orchestration Logic

**Task:** T04.02
**Date:** 2026-03-23
**Verdict:** PASS — Zero violations found

---

## Scope

All v3.3 test files (`tests/v3.3/*.py`) audited for `mock.patch` / `monkeypatch.setattr` usage targeting gate functions or orchestration logic:

- `execute_phase_tasks()`
- `_run_checkers()`
- `_subprocess_factory` wiring paths
- `check_wiring_report()` / gate decision functions

### Files Audited (11 files)

| File | Lines |
|------|-------|
| `tests/v3.3/__init__.py` | - |
| `tests/v3.3/conftest.py` | - |
| `tests/v3.3/test_session_summary.py` | - |
| `tests/v3.3/test_reachability_eval.py` | - |
| `tests/v3.3/test_turnledger_lifecycle.py` | 1138+ |
| `tests/v3.3/test_gate_rollout_modes.py` | 944+ |
| `tests/v3.3/test_wiring_points_e2e.py` | 1953+ |
| `tests/v3.3/test_integration_regression.py` | 741+ |
| `tests/v3.3/test_zero_files_analyzed.py` | - |
| `tests/v3.3/test_broken_wiring_detection.py` | - |
| `tests/v3.3/test_fidelity_checker.py` | - |

---

## Findings: Protected Targets

### 1. `execute_phase_tasks()` — NOT mocked in integration tests

All integration/lifecycle tests **call `execute_phase_tasks()` directly** via import, passing `_subprocess_factory` as a keyword argument (dependency injection). The function itself executes its real logic.

**Evidence:**
- `test_turnledger_lifecycle.py:381` — `results, remaining, gate_results = execute_phase_tasks(..., _subprocess_factory=_factory)`
- `test_integration_regression.py:206` — same pattern
- `test_gate_rollout_modes.py:628` — same pattern
- `test_wiring_points_e2e.py:1030` — same pattern (FR-2.1 remediation tests)

**Wiring-observation tests** (in `test_wiring_points_e2e.py`) do patch `execute_phase_tasks` at the `execute_sprint` call-site to capture what arguments are passed to it. These tests verify the *caller's wiring* (dispatch routing), not the function's behavior. This is the correct pattern: the function under test is `execute_sprint`, and `execute_phase_tasks` is a dependency being observed, not suppressed.

### 2. `_run_checkers()` — NOT mocked

Tests provide a local `_run_checkers` function via the `run_checkers=` keyword argument (dependency injection). The orchestration logic (`execute_phase_tasks`) runs its real code path including the callback invocation.

**Evidence:**
- `test_turnledger_lifecycle.py:143,173` — defines `_run_checkers`, passes via `run_checkers=_run_checkers`
- `test_turnledger_lifecycle.py:1088,1138` — same pattern

### 3. `_subprocess_factory` wiring paths — NOT mocked

All tests use the `_subprocess_factory=` injection point (a designed test seam), providing a factory function that records calls and returns controlled `(exit_code, turns, output_bytes)` tuples. The orchestration logic executes normally.

**Evidence:**
- `test_turnledger_lifecycle.py:386,625,890,964` — `_subprocess_factory=_factory`
- `test_integration_regression.py:209,302,315,416,513` — same
- `test_gate_rollout_modes.py:932` — `_subprocess_factory=interrupting_factory`
- `test_wiring_points_e2e.py:1035,1803,1909,1953` — same

### 4. Gate decision functions (`check_wiring_report`, `wiring_gate.*`) — NOT mocked

No test patches `check_wiring_report()` or any gate decision function. Tests that need to control wiring analysis results patch `run_wiring_analysis` (the data-gathering layer), allowing the gate decision logic to run on that data unmodified.

---

## Allowlisted Patches (Non-Violations)

The following `patch()` targets appear in v3.3 tests but are **not** gate functions or orchestration logic:

| Target | Purpose | Files |
|--------|---------|-------|
| `shutil.which` | Simulate `claude` CLI presence | wiring_points_e2e, integration_regression |
| `SprintLogger` | Suppress log output | wiring_points_e2e, integration_regression |
| `OutputMonitor` | Suppress output monitoring | wiring_points_e2e |
| `_notify` | Suppress notifications | wiring_points_e2e, integration_regression |
| `execute_preflight_phases` | Skip preflight (not under test) | wiring_points_e2e, integration_regression |
| `run_wiring_analysis` | Control wiring analysis input data | wiring_points_e2e, gate_rollout_modes, turnledger_lifecycle, integration_regression |
| `run_post_phase_wiring_hook` | Observe/control hook firing | wiring_points_e2e, integration_regression |
| `run_post_task_wiring_hook` | Observe hook at task level | wiring_points_e2e |
| `ClaudeProcess` | Fake subprocess for freeform phases | wiring_points_e2e |
| `WiringConfig` | Control config construction | gate_rollout_modes, wiring_points_e2e |
| `_recheck_wiring` | Control recheck result | gate_rollout_modes |
| `build_kpi_report` | Capture KPI data | wiring_points_e2e |

All of these are either I/O boundaries, logging/notification infrastructure, or data-layer stubs — not gate or orchestration logic.

---

## `monkeypatch.setattr` Usage (3 instances)

All 3 instances target `run_wiring_analysis` (data layer, not gate logic):

1. `test_turnledger_lifecycle.py:602` — `monkeypatch.setattr("superclaude.cli.audit.wiring_gate.run_wiring_analysis", ...)`
2. `test_turnledger_lifecycle.py:872` — same target
3. `test_integration_regression.py:131` — same target

---

## Conclusion

**PASS**: Zero `mock.patch` or `monkeypatch.setattr` calls target gate functions (`execute_phase_tasks`, `_run_checkers`, `_subprocess_factory`, `check_wiring_report`) or orchestration decision logic across all 11 v3.3 test files.

All mocking is restricted to:
- I/O boundaries (`run_wiring_analysis`, `ClaudeProcess`, `shutil.which`)
- Infrastructure (`SprintLogger`, `_notify`, `OutputMonitor`)
- Designed injection points (`_subprocess_factory=`, `run_checkers=`)
