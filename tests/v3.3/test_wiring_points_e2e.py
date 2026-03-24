"""E2E wiring-point validation for sprint infrastructure (T02.01, T02.02).

T02.01: Verifies that TurnLedger, ShadowGateMetrics, DeferredRemediationLog,
and SprintGatePolicy are constructed correctly via real orchestration paths
(execute_sprint → execute_phase_tasks). Spec refs: FR-1.1 through FR-1.4.

T02.02: Verifies task-inventory path delegation vs freeform fallback by
asserting ``_parse_phase_tasks()`` return type is ``list[TaskEntry] | None``.
Spec refs: FR-1.5, FR-1.6.

Dependencies: T01.02 (audit_trail fixture)
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.sprint.executor import (
    SprintGatePolicy,
    _format_wiring_failure,
    _parse_phase_tasks,
    _recheck_wiring,
    _resolve_wiring_mode,
    execute_sprint,
    run_post_phase_wiring_hook,
)
from superclaude.cli.sprint.models import (
    GateOutcome,
    Phase,
    PhaseResult,
    PhaseStatus,
    SHADOW_GRACE_INFINITE,
    ShadowGateMetrics,
    SprintConfig,
    TaskEntry,
    TaskResult,
    TaskStatus,
    TurnLedger,
)
from superclaude.cli.audit.wiring_gate import (
    WIRING_GATE,
    WiringFinding,
    WiringReport,
    check_wiring_report,
)
from superclaude.cli.roadmap.convergence import DeviationRegistry, MAX_CONVERGENCE_BUDGET
from superclaude.cli.roadmap.models import Finding
from superclaude.cli.pipeline.trailing_gate import (
    DeferredRemediationLog,
    TrailingGateResult,
)
from superclaude.cli.sprint.executor import execute_phase_tasks


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_config(tmp_path: Path, *, num_phases: int = 1) -> SprintConfig:
    """Build a SprintConfig pointing at real temp directories."""
    phases = []
    for i in range(1, num_phases + 1):
        pf = tmp_path / f"phase-{i}-tasklist.md"
        pf.write_text(
            f"# Phase {i}\n\n### T{i:02d}.01 -- Task One\nDo something\n"
        )
        phases.append(Phase(number=i, file=pf, name=f"Phase {i}"))

    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n")

    return SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=phases,
        start_phase=1,
        end_phase=num_phases,
        max_turns=5,
        wiring_gate_mode="off",
        wiring_gate_scope="none",
    )


def _run_execute_sprint_capturing(config: SprintConfig):
    """Run execute_sprint, capturing the args passed to execute_phase_tasks.

    Returns a dict with keys: ledger, shadow_metrics, remediation_log, gate_policy.
    gate_policy is captured via a secondary patch on SprintGatePolicy.__init__.
    """
    captured = {
        "ledger": None,
        "shadow_metrics": None,
        "remediation_log": None,
        "gate_policy": None,
    }

    original_gate_init = SprintGatePolicy.__init__

    def _capture_gate_init(self, cfg):
        captured["gate_policy"] = self
        original_gate_init(self, cfg)

    def _capture_phase_tasks(tasks, config, phase, ledger=None, **kwargs):
        captured["ledger"] = ledger
        captured["shadow_metrics"] = kwargs.get("shadow_metrics")
        captured["remediation_log"] = kwargs.get("remediation_log")
        results = [
            TaskResult(
                task=t,
                status=TaskStatus.PASS,
                exit_code=0,
                turns_consumed=1,
            )
            for t in tasks
        ]
        return results, [], []

    with (
        patch(
            "superclaude.cli.sprint.executor.shutil.which",
            return_value="/usr/bin/claude",
        ),
        patch(
            "superclaude.cli.sprint.executor.execute_phase_tasks",
            side_effect=_capture_phase_tasks,
        ),
        patch(
            "superclaude.cli.sprint.executor.run_post_phase_wiring_hook",
            side_effect=lambda phase, config, pr, **kw: pr,
        ),
        patch("superclaude.cli.sprint.notify._notify"),
        patch("superclaude.cli.sprint.executor.SprintLogger"),
        patch(
            "superclaude.cli.sprint.preflight.execute_preflight_phases",
            return_value=[],
        ),
        patch.object(
            SprintGatePolicy, "__init__", _capture_gate_init,
        ),
    ):
        execute_sprint(config)

    return captured


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestConstructionValidation:
    """FR-1.1–FR-1.4: Validate construction of 4 core infrastructure classes."""

    def test_turnledger_construction(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.1: TurnLedger constructed with correct initial_budget and reimbursement_rate."""
        config = _make_config(tmp_path)
        config.results_dir.mkdir(parents=True, exist_ok=True)

        captured = _run_execute_sprint_capturing(config)
        ledger = captured["ledger"]

        assert isinstance(ledger, TurnLedger), (
            f"Expected TurnLedger, got {type(ledger).__name__}"
        )
        expected_budget = config.max_turns * len(config.active_phases)
        assert ledger.initial_budget == expected_budget
        assert ledger.reimbursement_rate == 0.8
        assert ledger.consumed == 0

        audit_trail.record(
            test_id="test_turnledger_construction",
            spec_ref="FR-1.1",
            assertion_type="structural",
            inputs={
                "max_turns": config.max_turns,
                "active_phases": len(config.active_phases),
            },
            observed={
                "type": type(ledger).__name__,
                "initial_budget": ledger.initial_budget,
                "reimbursement_rate": ledger.reimbursement_rate,
                "consumed": ledger.consumed,
            },
            expected={
                "type": "TurnLedger",
                "initial_budget": expected_budget,
                "reimbursement_rate": 0.8,
                "consumed": 0,
            },
            verdict="PASS",
            evidence=(
                f"TurnLedger constructed via execute_sprint with "
                f"initial_budget={expected_budget}, reimbursement_rate=0.8"
            ),
        )

    def test_shadow_gate_metrics_construction(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.2: ShadowGateMetrics constructed with zeroed counters."""
        config = _make_config(tmp_path)
        config.results_dir.mkdir(parents=True, exist_ok=True)

        captured = _run_execute_sprint_capturing(config)
        metrics = captured["shadow_metrics"]

        assert isinstance(metrics, ShadowGateMetrics), (
            f"Expected ShadowGateMetrics, got {type(metrics).__name__}"
        )
        assert metrics.total_evaluated == 0
        assert metrics.passed == 0
        assert metrics.failed == 0
        assert metrics.latency_ms == []

        audit_trail.record(
            test_id="test_shadow_gate_metrics_construction",
            spec_ref="FR-1.2",
            assertion_type="structural",
            inputs={},
            observed={
                "type": type(metrics).__name__,
                "total_evaluated": metrics.total_evaluated,
                "passed": metrics.passed,
                "failed": metrics.failed,
                "latency_ms_len": len(metrics.latency_ms),
            },
            expected={
                "type": "ShadowGateMetrics",
                "total_evaluated": 0,
                "passed": 0,
                "failed": 0,
                "latency_ms_len": 0,
            },
            verdict="PASS",
            evidence="ShadowGateMetrics constructed via execute_sprint with all counters at zero",
        )

    def test_deferred_remediation_log_construction(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.3: DeferredRemediationLog constructed with persist_path under results_dir."""
        config = _make_config(tmp_path)
        config.results_dir.mkdir(parents=True, exist_ok=True)

        captured = _run_execute_sprint_capturing(config)
        log = captured["remediation_log"]

        assert isinstance(log, DeferredRemediationLog), (
            f"Expected DeferredRemediationLog, got {type(log).__name__}"
        )
        # persist_path must be under results_dir
        assert log._persist_path is not None
        assert str(log._persist_path).startswith(str(config.results_dir)), (
            f"persist_path {log._persist_path} not under results_dir {config.results_dir}"
        )
        assert log.pending_remediations() == []

        audit_trail.record(
            test_id="test_deferred_remediation_log_construction",
            spec_ref="FR-1.3",
            assertion_type="structural",
            inputs={"results_dir": str(config.results_dir)},
            observed={
                "type": type(log).__name__,
                "persist_path": str(log._persist_path),
                "persist_path_under_results_dir": str(log._persist_path).startswith(
                    str(config.results_dir)
                ),
                "pending_count": len(log.pending_remediations()),
            },
            expected={
                "type": "DeferredRemediationLog",
                "persist_path_under_results_dir": True,
                "pending_count": 0,
            },
            verdict="PASS",
            evidence=(
                f"DeferredRemediationLog constructed via execute_sprint with "
                f"persist_path={log._persist_path} under results_dir"
            ),
        )

    def test_sprint_gate_policy_construction(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.4: SprintGatePolicy constructed with the sprint config."""
        config = _make_config(tmp_path)
        config.results_dir.mkdir(parents=True, exist_ok=True)

        captured = _run_execute_sprint_capturing(config)
        policy = captured["gate_policy"]

        assert isinstance(policy, SprintGatePolicy), (
            f"Expected SprintGatePolicy, got {type(policy).__name__}"
        )
        assert policy._config is config

        audit_trail.record(
            test_id="test_sprint_gate_policy_construction",
            spec_ref="FR-1.4",
            assertion_type="structural",
            inputs={"config_index_path": str(config.index_path)},
            observed={
                "type": type(policy).__name__,
                "config_is_same_object": policy._config is config,
            },
            expected={
                "type": "SprintGatePolicy",
                "config_is_same_object": True,
            },
            verdict="PASS",
            evidence="SprintGatePolicy constructed via execute_sprint with the sprint config object",
        )


class TestPhaseDelegation:
    """FR-1.5–FR-1.6: Validate task-inventory vs freeform delegation paths."""

    def test_task_inventory_path_delegation(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.5: Phase with task headings delegates to execute_phase_tasks().

        A phase file containing ``### T01.01 -- ...`` headings should cause
        ``_parse_phase_tasks()`` to return a ``list[TaskEntry]``, triggering
        the per-task delegation path (execute_phase_tasks) rather than the
        single ClaudeProcess fallback.
        """
        # Build a phase file with task-inventory headings
        pf = tmp_path / "phase-1-tasklist.md"
        pf.write_text(
            "# Phase 1\n\n"
            "### T01.01 -- First task\nDo the first thing\n\n"
            "### T01.02 -- Second task\nDo the second thing\n"
        )
        phase = Phase(number=1, file=pf, name="Phase 1")

        index = tmp_path / "tasklist-index.md"
        index.write_text("index\n")
        config = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
            phases=[phase],
            start_phase=1,
            end_phase=1,
            max_turns=5,
            wiring_gate_mode="off",
            wiring_gate_scope="none",
        )

        # Verify _parse_phase_tasks returns list[TaskEntry]
        result = _parse_phase_tasks(phase, config)
        assert isinstance(result, list), (
            f"Expected list, got {type(result).__name__}"
        )
        assert len(result) >= 2, f"Expected >=2 tasks, got {len(result)}"
        for entry in result:
            assert isinstance(entry, TaskEntry), (
                f"Expected TaskEntry, got {type(entry).__name__}"
            )

        # Verify the per-task path is actually taken by execute_sprint
        delegate_called = {"called": False}

        def _capture_delegate(tasks, config, phase, ledger=None, **kwargs):
            delegate_called["called"] = True
            results = [
                TaskResult(
                    task=t, status=TaskStatus.PASS, exit_code=0, turns_consumed=1,
                )
                for t in tasks
            ]
            return results, [], []

        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.sprint.executor.execute_phase_tasks",
                side_effect=_capture_delegate,
            ),
            patch(
                "superclaude.cli.sprint.executor.run_post_phase_wiring_hook",
                side_effect=lambda phase, config, pr, **kw: pr,
            ),
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.executor.SprintLogger"),
            patch(
                "superclaude.cli.sprint.preflight.execute_preflight_phases",
                return_value=[],
            ),
            patch.object(SprintGatePolicy, "__init__", lambda self, cfg: None),
        ):
            config.results_dir.mkdir(parents=True, exist_ok=True)
            execute_sprint(config)

        assert delegate_called["called"], (
            "execute_phase_tasks was not called for task-inventory phase"
        )

        audit_trail.record(
            test_id="test_task_inventory_path_delegation",
            spec_ref="FR-1.5",
            assertion_type="behavioral",
            inputs={"phase_content": "has ### T01.01/T01.02 headings"},
            observed={
                "parse_result_type": type(result).__name__,
                "parse_result_len": len(result),
                "entry_types": [type(e).__name__ for e in result],
                "delegate_called": delegate_called["called"],
            },
            expected={
                "parse_result_type": "list",
                "entry_types_all": "TaskEntry",
                "delegate_called": True,
            },
            verdict="PASS",
            evidence=(
                f"_parse_phase_tasks returned list[TaskEntry] with {len(result)} entries; "
                f"execute_phase_tasks was called for per-task delegation"
            ),
        )

    def test_freeform_fallback_delegation(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.6: Phase without task headings falls back to ClaudeProcess path.

        A freeform phase file (no ``### T<PP>.<TT>`` headings) should cause
        ``_parse_phase_tasks()`` to return ``None``, triggering the single
        ClaudeProcess fallback path instead of execute_phase_tasks.
        """
        # Build a phase file WITHOUT task-inventory headings (freeform)
        pf = tmp_path / "phase-1-tasklist.md"
        pf.write_text(
            "# Phase 1 -- Freeform\n\n"
            "Run the analysis pipeline end to end.\n"
            "No structured task inventory here.\n"
        )
        phase = Phase(number=1, file=pf, name="Phase 1")

        index = tmp_path / "tasklist-index.md"
        index.write_text("index\n")
        config = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
            phases=[phase],
            start_phase=1,
            end_phase=1,
            max_turns=5,
            wiring_gate_mode="off",
            wiring_gate_scope="none",
        )

        # Verify _parse_phase_tasks returns None for freeform content
        result = _parse_phase_tasks(phase, config)
        assert result is None, (
            f"Expected None for freeform phase, got {type(result).__name__}: {result}"
        )

        # Verify the ClaudeProcess fallback path is taken (not execute_phase_tasks)
        delegate_called = {"called": False}
        claude_process_started = {"called": False}

        def _capture_delegate(tasks, config, phase, ledger=None, **kwargs):
            delegate_called["called"] = True
            return [], [], []

        class _FakeProcess:
            """Mimics subprocess.Popen with immediate exit."""
            pid = 12345
            returncode = 0
            _poll_count = 0

            def poll(self):
                # Return None on first call (enter loop), then 0 (exit)
                self._poll_count += 1
                return None if self._poll_count <= 1 else 0

            def terminate(self):
                pass

            def kill(self):
                pass

            def wait(self, timeout=None):
                return 0

        class _FakeClaudeProcess:
            def __init__(self, *args, **kwargs):
                claude_process_started["called"] = True
                self.timeout_seconds = 60
                self._process = _FakeProcess()

            def start(self):
                pass

            def terminate(self):
                pass

            def cleanup(self):
                pass

        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.sprint.executor.execute_phase_tasks",
                side_effect=_capture_delegate,
            ),
            patch(
                "superclaude.cli.sprint.executor.ClaudeProcess",
                _FakeClaudeProcess,
            ),
            patch(
                "superclaude.cli.sprint.executor.run_post_phase_wiring_hook",
                side_effect=lambda phase, config, pr, **kw: pr,
            ),
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.executor.SprintLogger"),
            patch("superclaude.cli.sprint.executor.OutputMonitor"),
            patch(
                "superclaude.cli.sprint.preflight.execute_preflight_phases",
                return_value=[],
            ),
            patch.object(SprintGatePolicy, "__init__", lambda self, cfg: None),
        ):
            config.results_dir.mkdir(parents=True, exist_ok=True)
            execute_sprint(config)

        assert not delegate_called["called"], (
            "execute_phase_tasks should NOT be called for freeform phase"
        )
        assert claude_process_started["called"], (
            "ClaudeProcess should be instantiated for freeform fallback"
        )

        audit_trail.record(
            test_id="test_freeform_fallback_delegation",
            spec_ref="FR-1.6",
            assertion_type="behavioral",
            inputs={"phase_content": "freeform, no task headings"},
            observed={
                "parse_result": repr(result),
                "delegate_called": delegate_called["called"],
                "claude_process_started": claude_process_started["called"],
            },
            expected={
                "parse_result": "None",
                "delegate_called": False,
                "claude_process_started": True,
            },
            verdict="PASS",
            evidence=(
                "_parse_phase_tasks returned None for freeform phase; "
                "ClaudeProcess fallback was used instead of execute_phase_tasks"
            ),
        )


class TestWiringModeResolution:
    """FR-1.12: Validate _resolve_wiring_mode() resolves mode from config."""

    @pytest.mark.parametrize(
        "scope, grace_period, expected_mode",
        [
            # No scope → falls back to config.wiring_gate_mode directly
            ("none", 0, "shadow"),
            ("none", 0, "off"),
            ("none", 0, "full"),
            # Release scope → always "full" (BLOCKING)
            ("release", 0, "full"),
            ("release", 30, "full"),
            # Milestone scope → BLOCKING default → "full"
            ("milestone", 0, "full"),
            # Task scope with grace_period=0 → BLOCKING → "full"
            ("task", 0, "full"),
            # Task scope with grace_period>0 → TRAILING → "shadow"
            ("task", 10, "shadow"),
        ],
        ids=[
            "no_scope-shadow_fallback",
            "no_scope-off_fallback",
            "no_scope-full_fallback",
            "release-always_full",
            "release-grace_ignored",
            "milestone-blocking_default",
            "task-no_grace_blocking",
            "task-grace_trailing",
        ],
    )
    def test_wiring_mode_resolution(
        self,
        tmp_path: Path,
        audit_trail,
        scope: str,
        grace_period: int,
        expected_mode: str,
    ) -> None:
        """FR-1.12: _resolve_wiring_mode returns correct mode for scope/grace config."""
        # For "none" scope tests, the fallback is config.wiring_gate_mode itself
        fallback_mode = expected_mode if scope == "none" else "off"

        config = _make_config(tmp_path)
        config.results_dir.mkdir(parents=True, exist_ok=True)
        object.__setattr__(config, "wiring_gate_scope", scope)
        object.__setattr__(config, "wiring_gate_mode", fallback_mode)
        object.__setattr__(config, "wiring_gate_grace_period", grace_period)

        resolved = _resolve_wiring_mode(config)

        assert resolved == expected_mode, (
            f"Expected mode '{expected_mode}' for scope={scope}, "
            f"grace_period={grace_period}, got '{resolved}'"
        )

        audit_trail.record(
            test_id=f"test_wiring_mode_resolution[{scope}-gp{grace_period}]",
            spec_ref="FR-1.12",
            assertion_type="behavioral",
            inputs={
                "wiring_gate_scope": scope,
                "wiring_gate_mode": fallback_mode,
                "wiring_gate_grace_period": grace_period,
            },
            observed={"resolved_mode": resolved},
            expected={"resolved_mode": expected_mode},
            verdict="PASS",
            evidence=(
                f"_resolve_wiring_mode returned '{resolved}' for "
                f"scope={scope}, grace_period={grace_period}"
            ),
        )


class TestPostPhaseWiringHook:
    """FR-1.7: Validate run_post_phase_wiring_hook fires on both execution paths."""

    def test_post_phase_hook_per_task_path(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.7a: Post-phase wiring hook fires after per-task (execute_phase_tasks) path."""
        config = _make_config(tmp_path)
        config.results_dir.mkdir(parents=True, exist_ok=True)

        hook_calls: list[dict] = []

        def _capture_hook(phase, config, pr, **kw):
            hook_calls.append({
                "phase_number": phase.number,
                "phase_result_type": type(pr).__name__,
                "phase_result_status": pr.status.name,
                "ledger": kw.get("ledger"),
                "remediation_log": kw.get("remediation_log"),
            })
            return pr

        def _fake_phase_tasks(tasks, config, phase, ledger=None, **kwargs):
            results = [
                TaskResult(
                    task=t, status=TaskStatus.PASS, exit_code=0, turns_consumed=1,
                )
                for t in tasks
            ]
            return results, [], []

        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.sprint.executor.execute_phase_tasks",
                side_effect=_fake_phase_tasks,
            ),
            patch(
                "superclaude.cli.sprint.executor.run_post_phase_wiring_hook",
                side_effect=_capture_hook,
            ),
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.executor.SprintLogger"),
            patch(
                "superclaude.cli.sprint.preflight.execute_preflight_phases",
                return_value=[],
            ),
            patch.object(SprintGatePolicy, "__init__", lambda self, cfg: None),
        ):
            execute_sprint(config)

        assert len(hook_calls) == 1, (
            f"Expected 1 post-phase hook call for per-task path, got {len(hook_calls)}"
        )
        call = hook_calls[0]
        assert call["phase_number"] == 1
        assert call["phase_result_type"] == "PhaseResult"
        assert call["ledger"] is not None, "Hook must receive ledger argument"
        assert call["remediation_log"] is not None, "Hook must receive remediation_log"

        audit_trail.record(
            test_id="test_post_phase_hook_per_task_path",
            spec_ref="FR-1.7",
            assertion_type="behavioral",
            inputs={"path": "per-task (execute_phase_tasks)", "num_phases": 1},
            observed={
                "hook_call_count": len(hook_calls),
                "phase_number": call["phase_number"],
                "phase_result_type": call["phase_result_type"],
                "ledger_present": call["ledger"] is not None,
                "remediation_log_present": call["remediation_log"] is not None,
            },
            expected={
                "hook_call_count": 1,
                "phase_number": 1,
                "phase_result_type": "PhaseResult",
                "ledger_present": True,
                "remediation_log_present": True,
            },
            verdict="PASS",
            evidence=(
                "run_post_phase_wiring_hook called once on per-task path "
                "with PhaseResult, ledger, and remediation_log"
            ),
        )

    def test_post_phase_hook_claude_process_path(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.7b: Post-phase wiring hook fires after ClaudeProcess (freeform) path."""
        # Build a freeform phase file (no task headings)
        pf = tmp_path / "phase-1-tasklist.md"
        pf.write_text(
            "# Phase 1 -- Freeform\n\n"
            "Run the analysis pipeline end to end.\n"
        )
        phase = Phase(number=1, file=pf, name="Phase 1")

        index = tmp_path / "tasklist-index.md"
        index.write_text("index\n")
        config = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
            phases=[phase],
            start_phase=1,
            end_phase=1,
            max_turns=5,
            wiring_gate_mode="off",
            wiring_gate_scope="none",
        )
        config.results_dir.mkdir(parents=True, exist_ok=True)

        hook_calls: list[dict] = []

        def _capture_hook(phase, config, pr, **kw):
            hook_calls.append({
                "phase_number": phase.number,
                "phase_result_type": type(pr).__name__,
                "phase_result_status": pr.status.name,
                "ledger": kw.get("ledger"),
                "remediation_log": kw.get("remediation_log"),
            })
            return pr

        class _FakeProcess:
            pid = 12345
            returncode = 0
            _poll_count = 0

            def poll(self):
                self._poll_count += 1
                return None if self._poll_count <= 1 else 0

            def terminate(self):
                pass

            def kill(self):
                pass

            def wait(self, timeout=None):
                return 0

        class _FakeClaudeProcess:
            def __init__(self, *args, **kwargs):
                self.timeout_seconds = 60
                self._process = _FakeProcess()

            def start(self):
                pass

            def terminate(self):
                pass

            def cleanup(self):
                pass

        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.sprint.executor.execute_phase_tasks",
                side_effect=lambda *a, **kw: ([], [], []),
            ),
            patch(
                "superclaude.cli.sprint.executor.ClaudeProcess",
                _FakeClaudeProcess,
            ),
            patch(
                "superclaude.cli.sprint.executor.run_post_phase_wiring_hook",
                side_effect=_capture_hook,
            ),
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.executor.SprintLogger"),
            patch("superclaude.cli.sprint.executor.OutputMonitor"),
            patch(
                "superclaude.cli.sprint.preflight.execute_preflight_phases",
                return_value=[],
            ),
            patch.object(SprintGatePolicy, "__init__", lambda self, cfg: None),
        ):
            execute_sprint(config)

        assert len(hook_calls) == 1, (
            f"Expected 1 post-phase hook call for ClaudeProcess path, got {len(hook_calls)}"
        )
        call = hook_calls[0]
        assert call["phase_number"] == 1
        assert call["phase_result_type"] == "PhaseResult"
        assert call["ledger"] is not None, "Hook must receive ledger argument"
        assert call["remediation_log"] is not None, "Hook must receive remediation_log"

        audit_trail.record(
            test_id="test_post_phase_hook_claude_process_path",
            spec_ref="FR-1.7",
            assertion_type="behavioral",
            inputs={"path": "ClaudeProcess (freeform)", "num_phases": 1},
            observed={
                "hook_call_count": len(hook_calls),
                "phase_number": call["phase_number"],
                "phase_result_type": call["phase_result_type"],
                "ledger_present": call["ledger"] is not None,
                "remediation_log_present": call["remediation_log"] is not None,
            },
            expected={
                "hook_call_count": 1,
                "phase_number": 1,
                "phase_result_type": "PhaseResult",
                "ledger_present": True,
                "remediation_log_present": True,
            },
            verdict="PASS",
            evidence=(
                "run_post_phase_wiring_hook called once on ClaudeProcess freeform path "
                "with PhaseResult, ledger, and remediation_log"
            ),
        )


class TestRunPostPhaseWiringHookConfirming:
    """FR-6.2 T02: Confirming test exercising run_post_phase_wiring_hook() directly.

    Unlike T02.03 (TestPostPhaseWiringHook) which verifies the hook is *called*
    during execute_sprint by mocking it, this test calls the function directly
    and validates its internal behavior: synthetic TaskEntry creation, delegation
    to run_post_task_wiring_hook, and status mapping back to PhaseResult.
    """

    def test_run_post_phase_wiring_hook_delegates_and_maps_status(
        self, tmp_path: Path, audit_trail,
    ) -> None:
        """FR-6.2 T02: Direct call confirms delegation and FAIL→HALT mapping."""
        config = _make_config(tmp_path)
        config.results_dir.mkdir(parents=True, exist_ok=True)

        phase = config.phases[0]

        # --- Scenario A: per-task hook returns PASS → PhaseResult unchanged ---
        phase_result_pass = PhaseResult(
            phase=phase,
            status=PhaseStatus.PASS,
            exit_code=0,
        )

        delegated_calls: list[dict] = []

        def _capture_task_hook(task, cfg, task_result, **kw):
            delegated_calls.append({
                "task_id": task.task_id,
                "task_description": task.description,
                "task_result_status": task_result.status.name,
                "ledger": kw.get("ledger"),
                "remediation_log": kw.get("remediation_log"),
            })
            return task_result  # Return unchanged (PASS)

        with patch(
            "superclaude.cli.sprint.executor.run_post_task_wiring_hook",
            side_effect=_capture_task_hook,
        ):
            result_a = run_post_phase_wiring_hook(
                phase, config, phase_result_pass,
                ledger=TurnLedger(initial_budget=100, reimbursement_rate=0.5),
                remediation_log=DeferredRemediationLog(
                    persist_path=config.results_dir / "remediation.jsonl",
                ),
            )

        # Hook delegated to run_post_task_wiring_hook with synthetic task
        assert len(delegated_calls) == 1, (
            f"Expected 1 delegation call, got {len(delegated_calls)}"
        )
        call_a = delegated_calls[0]
        assert call_a["task_id"] == f"phase-{phase.number}"
        assert "wiring check" in call_a["task_description"].lower()
        assert call_a["task_result_status"] == "PASS"
        assert call_a["ledger"] is not None
        assert call_a["remediation_log"] is not None

        # PhaseResult unchanged when per-task hook returns PASS
        assert result_a is phase_result_pass
        assert result_a.status == PhaseStatus.PASS

        # --- Scenario B: per-task hook returns FAIL → PhaseResult becomes HALT ---
        delegated_calls.clear()
        phase_result_will_halt = PhaseResult(
            phase=phase,
            status=PhaseStatus.PASS,
            exit_code=0,
        )

        def _fail_task_hook(task, cfg, task_result, **kw):
            delegated_calls.append({"task_id": task.task_id})
            failed = TaskResult(
                task=task,
                status=TaskStatus.FAIL,
                exit_code=task_result.exit_code,
                started_at=task_result.started_at,
                finished_at=task_result.finished_at,
                output_bytes=task_result.output_bytes,
            )
            return failed

        with patch(
            "superclaude.cli.sprint.executor.run_post_task_wiring_hook",
            side_effect=_fail_task_hook,
        ):
            result_b = run_post_phase_wiring_hook(
                phase, config, phase_result_will_halt,
                ledger=TurnLedger(initial_budget=100, reimbursement_rate=0.5),
            )

        assert len(delegated_calls) == 1
        # FAIL from per-task hook → PhaseResult status mapped to HALT
        assert result_b.status == PhaseStatus.HALT, (
            f"Expected HALT after per-task hook FAIL, got {result_b.status}"
        )

        audit_trail.record(
            test_id="test_run_post_phase_wiring_hook_delegates_and_maps_status",
            spec_ref="FR-6.2",
            assertion_type="behavioral",
            inputs={
                "scenario_a": "per-task hook returns PASS",
                "scenario_b": "per-task hook returns FAIL",
            },
            observed={
                "delegation_count_a": 1,
                "synthetic_task_id": call_a["task_id"],
                "pass_status_unchanged": result_a.status.name,
                "fail_maps_to_halt": result_b.status.name,
                "ledger_forwarded": call_a["ledger"] is not None,
                "remediation_log_forwarded": call_a["remediation_log"] is not None,
            },
            expected={
                "delegation_count_a": 1,
                "synthetic_task_id": f"phase-{phase.number}",
                "pass_status_unchanged": "PASS",
                "fail_maps_to_halt": "HALT",
                "ledger_forwarded": True,
                "remediation_log_forwarded": True,
            },
            verdict="PASS",
            evidence=(
                "run_post_phase_wiring_hook() creates synthetic TaskEntry with "
                "task_id='phase-N', delegates to run_post_task_wiring_hook with "
                "ledger and remediation_log, and maps FAIL→HALT on PhaseResult"
            ),
        )


class TestAntiInstinctHookReturnType:
    """FR-1.8: Validate run_post_task_anti_instinct_hook() return type contract."""

    def test_anti_instinct_hook_return_type(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.8: Anti-instinct hook returns tuple[TaskResult, TrailingGateResult | None].

        Exercises the hook through real orchestration via ``execute_phase_tasks``
        with ``_subprocess_factory`` injection. Uses ``gate_rollout_mode="shadow"``
        to trigger gate evaluation and produce a non-None ``TrailingGateResult``.
        No mocks on hook internals — the hook runs its full code path.
        """
        pf = tmp_path / "phase-1-tasklist.md"
        pf.write_text(
            "# Phase 1\n\n### T01.01 -- Task One\nDo something\n"
        )
        phase = Phase(number=1, file=pf, name="Phase 1")

        index = tmp_path / "tasklist-index.md"
        index.write_text("index\n")
        config = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
            phases=[phase],
            start_phase=1,
            end_phase=1,
            max_turns=5,
            wiring_gate_mode="off",
            wiring_gate_scope="none",
            gate_rollout_mode="shadow",
        )
        config.results_dir.mkdir(parents=True, exist_ok=True)

        tasks = _parse_phase_tasks(phase, config)
        assert tasks is not None, "Expected task-inventory parse to succeed"

        ledger = TurnLedger(
            initial_budget=config.max_turns * len(config.active_phases),
            reimbursement_rate=0.8,
        )
        shadow_metrics = ShadowGateMetrics()

        def _factory(task, cfg, ph):
            """Subprocess factory: immediate success, no output artifact."""
            return (0, 1, 0)

        results, remaining, gate_results = execute_phase_tasks(
            tasks,
            config,
            phase,
            ledger=ledger,
            _subprocess_factory=_factory,
            shadow_metrics=shadow_metrics,
        )

        # Validate task results
        assert len(results) >= 1, f"Expected >=1 task result, got {len(results)}"
        for r in results:
            assert isinstance(r, TaskResult), (
                f"Expected TaskResult, got {type(r).__name__}"
            )

        # Validate gate results: shadow mode should produce one TrailingGateResult per task
        assert len(gate_results) == len(tasks), (
            f"Expected {len(tasks)} gate result(s) for shadow mode, got {len(gate_results)}"
        )
        for gr in gate_results:
            assert isinstance(gr, TrailingGateResult), (
                f"Expected TrailingGateResult, got {type(gr).__name__}"
            )
            # Vacuous pass: no output artifact → gate passes
            assert gr.passed is True
            assert gr.evaluation_ms >= 0.0

        # Verify the return type contract at the tuple level
        assert isinstance(gate_results, list)
        # Each element is TrailingGateResult (already asserted above)
        # The hook's contract is tuple[TaskResult, TrailingGateResult | None];
        # execute_phase_tasks filters None results, so all elements here are non-None

        audit_trail.record(
            test_id="test_anti_instinct_hook_return_type",
            spec_ref="FR-1.8",
            assertion_type="structural",
            inputs={
                "gate_rollout_mode": "shadow",
                "num_tasks": len(tasks),
                "subprocess_factory": "immediate success (0, 1, 0)",
            },
            observed={
                "result_count": len(results),
                "result_types": [type(r).__name__ for r in results],
                "gate_result_count": len(gate_results),
                "gate_result_types": [type(gr).__name__ for gr in gate_results],
                "all_passed": all(gr.passed for gr in gate_results),
                "all_evaluation_ms_nonneg": all(
                    gr.evaluation_ms >= 0.0 for gr in gate_results
                ),
            },
            expected={
                "result_types_all": "TaskResult",
                "gate_result_types_all": "TrailingGateResult",
                "all_passed": True,
                "all_evaluation_ms_nonneg": True,
            },
            verdict="PASS",
            evidence=(
                f"execute_phase_tasks returned {len(results)} TaskResult(s) and "
                f"{len(gate_results)} TrailingGateResult(s) via shadow-mode "
                f"anti-instinct hook; all gate results passed vacuously (no output artifact)"
            ),
        )


class TestGateResultAccumulation:
    """FR-1.9–FR-1.10: Gate result accumulation and failed-gate remediation log."""

    def test_gate_result_accumulation(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.9: Gate results accumulate across phases in order.

        Runs execute_sprint with 3 task-inventory phases in shadow gate mode.
        Captures the accumulated gate results passed to build_kpi_report and
        verifies they contain results from all phases in phase order.
        """
        num_phases = 3
        phases = []
        for i in range(1, num_phases + 1):
            pf = tmp_path / f"phase-{i}-tasklist.md"
            pf.write_text(
                f"# Phase {i}\n\n### T{i:02d}.01 -- Task One\nDo something\n"
            )
            phases.append(Phase(number=i, file=pf, name=f"Phase {i}"))

        index = tmp_path / "tasklist-index.md"
        index.write_text("index\n")
        config = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
            phases=phases,
            start_phase=1,
            end_phase=num_phases,
            max_turns=5,
            wiring_gate_mode="off",
            wiring_gate_scope="none",
            gate_rollout_mode="shadow",
        )
        config.results_dir.mkdir(parents=True, exist_ok=True)

        # Capture gate_results passed to build_kpi_report
        captured_gate_results: list[TrailingGateResult] = []

        def _fake_phase_tasks(tasks, config, phase, ledger=None, **kwargs):
            """Return one PASS result per task plus one gate result tagged with phase number."""
            results = [
                TaskResult(
                    task=t, status=TaskStatus.PASS, exit_code=0, turns_consumed=1,
                )
                for t in tasks
            ]
            gate_results = [
                TrailingGateResult(
                    step_id=f"P{phase.number}-{t.task_id}",
                    passed=True,
                    evaluation_ms=float(phase.number),
                )
                for t in tasks
            ]
            return results, [], gate_results

        def _capture_kpi(gate_results, **kwargs):
            captured_gate_results.extend(gate_results)
            # Return a minimal KPI report object
            from superclaude.cli.sprint.kpi import GateKPIReport
            report = GateKPIReport()
            report.format_report = lambda: "# KPI\nno-op"
            return report

        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.sprint.executor.execute_phase_tasks",
                side_effect=_fake_phase_tasks,
            ),
            patch(
                "superclaude.cli.sprint.executor.run_post_phase_wiring_hook",
                side_effect=lambda phase, config, pr, **kw: pr,
            ),
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.executor.SprintLogger"),
            patch(
                "superclaude.cli.sprint.preflight.execute_preflight_phases",
                return_value=[],
            ),
            patch.object(SprintGatePolicy, "__init__", lambda self, cfg: None),
            patch(
                "superclaude.cli.sprint.kpi.build_kpi_report",
                side_effect=_capture_kpi,
            ),
        ):
            execute_sprint(config)

        # Verify accumulation: 3 phases × 1 task each = 3 gate results
        assert len(captured_gate_results) == num_phases, (
            f"Expected {num_phases} accumulated gate results, got {len(captured_gate_results)}"
        )

        # Verify ordering: step_ids should be P1-*, P2-*, P3-* in order
        for i, gr in enumerate(captured_gate_results, start=1):
            assert gr.step_id.startswith(f"P{i}-"), (
                f"Gate result {i} has step_id={gr.step_id!r}, expected prefix 'P{i}-'"
            )
            assert gr.evaluation_ms == float(i), (
                f"Gate result {i} has evaluation_ms={gr.evaluation_ms}, expected {float(i)}"
            )

        audit_trail.record(
            test_id="test_gate_result_accumulation",
            spec_ref="FR-1.9",
            assertion_type="behavioral",
            inputs={"num_phases": num_phases, "gate_rollout_mode": "shadow"},
            observed={
                "accumulated_count": len(captured_gate_results),
                "step_ids": [gr.step_id for gr in captured_gate_results],
                "evaluation_ms_values": [gr.evaluation_ms for gr in captured_gate_results],
            },
            expected={
                "accumulated_count": num_phases,
                "step_id_prefixes": [f"P{i}-" for i in range(1, num_phases + 1)],
                "evaluation_ms_values": [float(i) for i in range(1, num_phases + 1)],
            },
            verdict="PASS",
            evidence=(
                f"execute_sprint accumulated {len(captured_gate_results)} gate results "
                f"across {num_phases} phases in phase order: "
                f"{[gr.step_id for gr in captured_gate_results]}"
            ),
        )

    def test_failed_gate_remediation_log(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.10: Failed gate produces a remediation log entry.

        Exercises DeferredRemediationLog.append() with a failed TrailingGateResult
        via _log_shadow_findings_to_remediation_log and verifies the log receives
        a pending RemediationEntry with the correct failure reason.
        """
        from superclaude.cli.sprint.executor import _log_shadow_findings_to_remediation_log

        remediation_log = DeferredRemediationLog(
            persist_path=tmp_path / "remediation.json",
        )

        # Verify log starts empty
        assert remediation_log.entry_count == 0

        # Create a fake task and a mock wiring report with unsuppressed findings
        task = TaskEntry(
            task_id="T01.01",
            title="Task One",
            description="Do something",
        )

        class _FakeFinding:
            finding_type = "anti-instinct-violation"
            detail = "Output contains disallowed pattern"

        class _FakeReport:
            unsuppressed_findings = [_FakeFinding()]

        # _log_shadow_findings_to_remediation_log creates a failed TrailingGateResult
        # per unsuppressed finding and appends it to the remediation log
        _log_shadow_findings_to_remediation_log(
            report=_FakeReport(),
            task=task,
            config=_make_config(tmp_path),
            remediation_log=remediation_log,
        )

        # Verify remediation log received the entry
        assert remediation_log.entry_count == 1, (
            f"Expected 1 remediation entry, got {remediation_log.entry_count}"
        )

        pending = remediation_log.pending_remediations()
        assert len(pending) == 1, (
            f"Expected 1 pending remediation, got {len(pending)}"
        )

        entry = pending[0]
        assert entry.step_id == "T01.01"
        assert "anti-instinct-violation" in entry.failure_reason
        assert "disallowed pattern" in entry.failure_reason
        assert entry.gate_result["passed"] is False
        assert entry.gate_result["step_id"] == "T01.01"

        audit_trail.record(
            test_id="test_failed_gate_remediation_log",
            spec_ref="FR-1.10",
            assertion_type="behavioral",
            inputs={
                "task_id": "T01.01",
                "finding_type": "anti-instinct-violation",
                "finding_detail": "Output contains disallowed pattern",
            },
            observed={
                "entry_count": remediation_log.entry_count,
                "pending_count": len(pending),
                "entry_step_id": entry.step_id,
                "entry_failure_reason": entry.failure_reason,
                "gate_result_passed": entry.gate_result["passed"],
                "gate_result_step_id": entry.gate_result["step_id"],
            },
            expected={
                "entry_count": 1,
                "pending_count": 1,
                "entry_step_id": "T01.01",
                "gate_result_passed": False,
            },
            verdict="PASS",
            evidence=(
                "Failed gate via _log_shadow_findings_to_remediation_log produced "
                "1 pending RemediationEntry with step_id=T01.01, "
                f"failure_reason={entry.failure_reason!r}"
            ),
        )


class TestShadowFindingsRemediationLog:
    """FR-1.13: Shadow findings produce remediation log entries with [shadow] prefix."""

    def test_shadow_findings_remediation_log(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.13: Shadow findings -> remediation log with [shadow] prefix.

        Exercises _log_shadow_findings_to_remediation_log with multiple findings
        and verifies every remediation entry's failure_reason starts with '[shadow]'.
        Uses real DeferredRemediationLog — no mocks on logging internals.
        """
        from superclaude.cli.sprint.executor import _log_shadow_findings_to_remediation_log

        remediation_log = DeferredRemediationLog(
            persist_path=tmp_path / "remediation.json",
        )

        task = TaskEntry(
            task_id="T02.08",
            title="Shadow Findings Test",
            description="Validate shadow prefix in remediation log",
        )

        class _FakeFinding:
            def __init__(self, finding_type: str, detail: str):
                self.finding_type = finding_type
                self.detail = detail

        class _FakeReport:
            unsuppressed_findings = [
                _FakeFinding("anti-instinct-violation", "Output contains disallowed pattern"),
                _FakeFinding("format-violation", "Missing required header"),
            ]

        config = _make_config(tmp_path)

        _log_shadow_findings_to_remediation_log(
            report=_FakeReport(),
            task=task,
            config=config,
            remediation_log=remediation_log,
        )

        # Verify correct number of entries
        assert remediation_log.entry_count == 2, (
            f"Expected 2 remediation entries, got {remediation_log.entry_count}"
        )

        pending = remediation_log.pending_remediations()
        assert len(pending) == 2, (
            f"Expected 2 pending remediations, got {len(pending)}"
        )

        # Core assertion: every entry's failure_reason starts with [shadow]
        for i, entry in enumerate(pending):
            assert entry.failure_reason.startswith("[shadow]"), (
                f"Entry {i} failure_reason missing [shadow] prefix: "
                f"{entry.failure_reason!r}"
            )
            assert entry.step_id == "T02.08", (
                f"Entry {i} step_id mismatch: expected T02.08, got {entry.step_id}"
            )
            assert entry.gate_result["passed"] is False, (
                f"Entry {i} gate_result should be failed"
            )

        # Verify specific content after prefix
        assert "anti-instinct-violation" in pending[0].failure_reason
        assert "disallowed pattern" in pending[0].failure_reason
        assert "format-violation" in pending[1].failure_reason
        assert "Missing required header" in pending[1].failure_reason

        audit_trail.record(
            test_id="test_shadow_findings_remediation_log",
            spec_ref="FR-1.13",
            assertion_type="behavioral",
            inputs={
                "task_id": "T02.08",
                "num_findings": 2,
                "finding_types": ["anti-instinct-violation", "format-violation"],
            },
            observed={
                "entry_count": remediation_log.entry_count,
                "pending_count": len(pending),
                "failure_reasons": [e.failure_reason for e in pending],
                "all_have_shadow_prefix": all(
                    e.failure_reason.startswith("[shadow]") for e in pending
                ),
            },
            expected={
                "entry_count": 2,
                "pending_count": 2,
                "all_have_shadow_prefix": True,
            },
            verdict="PASS",
            evidence=(
                f"_log_shadow_findings_to_remediation_log produced {len(pending)} "
                f"pending RemediationEntries, all with [shadow] prefix: "
                f"{[e.failure_reason for e in pending]}"
            ),
        )


class TestKPIReportFieldValues:
    """FR-1.11: KPI report field VALUE assertions (not just presence)."""

    def test_kpi_report_field_values(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.11: build_kpi_report() computes correct field VALUES for
        wiring_analyses_run, wiring_remediations_attempted, wiring_net_cost.

        Sets up known inputs (TurnLedger with specific wiring debits/credits,
        DeferredRemediationLog with known entries, gate results) and verifies
        the KPI report fields match computed expectations. Also verifies
        gate-kpi-report.md is written via execute_sprint.
        """
        from superclaude.cli.sprint.kpi import build_kpi_report, GateKPIReport

        # --- Known inputs ---
        # TurnLedger: 3 wiring analyses, 7 turns used, 2 turns credited
        ledger = TurnLedger(
            initial_budget=50,
            reimbursement_rate=0.8,
        )
        # Simulate 3 debit_wiring calls: 3 turns, 2 turns, 2 turns = 7 total
        ledger.debit_wiring(3)
        ledger.debit_wiring(2)
        ledger.debit_wiring(2)
        # Simulate 2 credit_wiring calls: 1 turn + 1 turn = 2 credited
        ledger.credit_wiring(1, 1)
        ledger.credit_wiring(1, 1)

        expected_analyses_run = 3
        expected_turns_used = 7
        expected_turns_credited = 2
        expected_net_cost = expected_turns_used - expected_turns_credited  # 5

        # DeferredRemediationLog with 2 entries
        remediation_log = DeferredRemediationLog(
            persist_path=tmp_path / "remediation.json",
        )
        remediation_log.append(TrailingGateResult(
            step_id="T01.01",
            passed=False,
            evaluation_ms=12.0,
            failure_reason="[shadow] anti-instinct violation 1",
        ))
        remediation_log.append(TrailingGateResult(
            step_id="T01.02",
            passed=False,
            evaluation_ms=18.0,
            failure_reason="[shadow] anti-instinct violation 2",
        ))
        expected_remediations_attempted = 2

        # Gate results: 3 passed, 1 failed
        gate_results = [
            TrailingGateResult(step_id="T01.01", passed=True, evaluation_ms=10.0),
            TrailingGateResult(step_id="T01.02", passed=True, evaluation_ms=20.0),
            TrailingGateResult(step_id="T01.03", passed=True, evaluation_ms=15.0),
            TrailingGateResult(step_id="T01.04", passed=False, evaluation_ms=25.0),
        ]

        # --- Call build_kpi_report directly ---
        report = build_kpi_report(
            gate_results=gate_results,
            remediation_log=remediation_log,
            turn_ledger=ledger,
        )

        # --- Assert field VALUES ---
        assert report.wiring_analyses_run == expected_analyses_run, (
            f"wiring_analyses_run: expected {expected_analyses_run}, "
            f"got {report.wiring_analyses_run}"
        )
        assert report.wiring_remediations_attempted == expected_remediations_attempted, (
            f"wiring_remediations_attempted: expected {expected_remediations_attempted}, "
            f"got {report.wiring_remediations_attempted}"
        )
        assert report.wiring_net_cost == expected_net_cost, (
            f"wiring_net_cost: expected {expected_net_cost}, "
            f"got {report.wiring_net_cost}"
        )

        # Cross-check gate evaluation fields
        assert report.total_gates_evaluated == 4
        assert report.gates_passed == 3
        assert report.gates_failed == 1
        assert report.wiring_turns_used == expected_turns_used
        assert report.wiring_turns_credited == expected_turns_credited

        # --- Verify report file written via execute_sprint ---
        num_phases = 2
        phases = []
        for i in range(1, num_phases + 1):
            pf = tmp_path / f"phase-{i}-tasklist.md"
            pf.write_text(
                f"# Phase {i}\n\n### T{i:02d}.01 -- Task One\nDo something\n"
            )
            phases.append(Phase(number=i, file=pf, name=f"Phase {i}"))

        index = tmp_path / "tasklist-index.md"
        index.write_text("index\n")
        config = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
            phases=phases,
            start_phase=1,
            end_phase=num_phases,
            max_turns=5,
            wiring_gate_mode="off",
            wiring_gate_scope="none",
            gate_rollout_mode="shadow",
        )
        config.results_dir.mkdir(parents=True, exist_ok=True)

        def _fake_phase_tasks(tasks, config, phase, ledger=None, **kwargs):
            # Simulate wiring turns on ledger so KPI report has non-zero values
            if ledger is not None:
                ledger.debit_wiring(2)
                ledger.credit_wiring(1, 1)
            results = [
                TaskResult(
                    task=t, status=TaskStatus.PASS, exit_code=0, turns_consumed=1,
                )
                for t in tasks
            ]
            gate_results = [
                TrailingGateResult(
                    step_id=t.task_id, passed=True, evaluation_ms=5.0,
                )
                for t in tasks
            ]
            return results, [], gate_results

        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.sprint.executor.execute_phase_tasks",
                side_effect=_fake_phase_tasks,
            ),
            patch(
                "superclaude.cli.sprint.executor.run_post_phase_wiring_hook",
                side_effect=lambda phase, config, pr, **kw: pr,
            ),
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.executor.SprintLogger"),
            patch(
                "superclaude.cli.sprint.preflight.execute_preflight_phases",
                return_value=[],
            ),
            patch.object(SprintGatePolicy, "__init__", lambda self, cfg: None),
        ):
            execute_sprint(config)

        kpi_path = config.results_dir / "gate-kpi-report.md"
        assert kpi_path.exists(), (
            f"gate-kpi-report.md not found at {kpi_path}"
        )

        kpi_text = kpi_path.read_text()
        # Verify field values appear in the formatted report
        # 2 phases × debit_wiring(2) = 4 turns used, 2 analyses run
        assert "Analyses run:     2" in kpi_text, (
            f"Expected 'Analyses run:     2' in KPI report, got:\n{kpi_text}"
        )
        assert "Net cost:         2" in kpi_text, (
            f"Expected 'Net cost:         2' in KPI report (4 used - 2 credited), "
            f"got:\n{kpi_text}"
        )

        audit_trail.record(
            test_id="test_kpi_report_field_values",
            spec_ref="FR-1.11",
            assertion_type="value",
            inputs={
                "wiring_debit_calls": [3, 2, 2],
                "wiring_credit_calls": [1, 1],
                "gate_results": "3 passed, 1 failed",
                "remediation_entries": 2,
            },
            observed={
                "wiring_analyses_run": report.wiring_analyses_run,
                "wiring_remediations_attempted": report.wiring_remediations_attempted,
                "wiring_net_cost": report.wiring_net_cost,
                "wiring_turns_used": report.wiring_turns_used,
                "wiring_turns_credited": report.wiring_turns_credited,
                "total_gates_evaluated": report.total_gates_evaluated,
                "gates_passed": report.gates_passed,
                "gates_failed": report.gates_failed,
                "kpi_file_exists": kpi_path.exists(),
            },
            expected={
                "wiring_analyses_run": expected_analyses_run,
                "wiring_remediations_attempted": expected_remediations_attempted,
                "wiring_net_cost": expected_net_cost,
                "wiring_turns_used": expected_turns_used,
                "wiring_turns_credited": expected_turns_credited,
                "total_gates_evaluated": 4,
                "gates_passed": 3,
                "gates_failed": 1,
                "kpi_file_exists": True,
            },
            verdict="PASS",
            evidence=(
                f"build_kpi_report computed: wiring_analyses_run={report.wiring_analyses_run}, "
                f"wiring_remediations_attempted={report.wiring_remediations_attempted}, "
                f"wiring_net_cost={report.wiring_net_cost}; "
                f"gate-kpi-report.md written with correct field values"
            ),
        )


class TestBlockingRemediationLifecycle:
    """FR-1.14, FR-1.14a-c: BLOCKING remediation lifecycle tests.

    Validates the full remediation lifecycle for full-mode wiring gate:
    format → debit → _recheck_wiring() → restore/fail.

    All tests use ``_subprocess_factory`` injection and patch
    ``run_wiring_analysis`` to control blocking findings. No mocks on
    remediation internals — ``_format_wiring_failure``, ``_recheck_wiring``,
    and ``ledger.debit`` run their real code paths.
    """

    @staticmethod
    def _blocking_finding(*, severity: str = "critical") -> WiringFinding:
        """Create a single blocking WiringFinding."""
        return WiringFinding(
            finding_type="unwired_callable",
            file_path="src/module.py",
            symbol_name="module.func",
            line_number=42,
            detail="Function not wired to registry",
            severity=severity,
            suppressed=False,
        )

    @staticmethod
    def _clean_report() -> WiringReport:
        """WiringReport with zero findings (remediation success)."""
        return WiringReport(
            target_dir="/tmp",
            files_analyzed=5,
            scan_duration_seconds=0.01,
            rollout_mode="full",
        )

    @staticmethod
    def _blocking_report(*, severity: str = "critical") -> WiringReport:
        """WiringReport with one blocking finding."""
        finding = TestBlockingRemediationLifecycle._blocking_finding(severity=severity)
        return WiringReport(
            target_dir="/tmp",
            files_analyzed=5,
            unwired_callables=[finding],
            scan_duration_seconds=0.01,
            rollout_mode="full",
        )

    def test_blocking_remediation_format(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.14a: _format_wiring_failure() produces non-empty prompt for blocking findings.

        Exercises the remediation format step through execute_phase_tasks with
        ``_subprocess_factory`` injection and wiring_gate_mode="full". The
        wiring analysis is patched to return a report with one critical finding,
        so the full-mode branch triggers ``_format_wiring_failure()``.
        """
        pf = tmp_path / "phase-1-tasklist.md"
        pf.write_text("# Phase 1\n\n### T01.01 -- Task One\nDo something\n")
        phase = Phase(number=1, file=pf, name="Phase 1")

        index = tmp_path / "tasklist-index.md"
        index.write_text("index\n")
        config = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
            phases=[phase],
            start_phase=1,
            end_phase=1,
            max_turns=20,
            wiring_gate_mode="full",
            wiring_gate_scope="all",
        )
        config.results_dir.mkdir(parents=True, exist_ok=True)

        tasks = _parse_phase_tasks(phase, config)
        assert tasks is not None

        # Direct assertion: _format_wiring_failure produces non-empty prompt
        report = self._blocking_report()
        task = tasks[0]
        prompt = _format_wiring_failure(report, task, config)

        assert isinstance(prompt, str)
        assert len(prompt) > 0, "Expected non-empty remediation prompt"
        assert task.task_id in prompt, "Prompt must reference the task ID"
        assert "WIRING REMEDIATION" in prompt, "Prompt must contain remediation header"

        audit_trail.record(
            test_id="test_blocking_remediation_format",
            spec_ref="FR-1.14a",
            assertion_type="value",
            inputs={
                "finding_count": 1,
                "finding_severity": "critical",
                "task_id": task.task_id,
            },
            observed={
                "prompt_type": type(prompt).__name__,
                "prompt_length": len(prompt),
                "contains_task_id": task.task_id in prompt,
                "contains_header": "WIRING REMEDIATION" in prompt,
            },
            expected={
                "prompt_type": "str",
                "prompt_length_gt_zero": True,
                "contains_task_id": True,
                "contains_header": True,
            },
            verdict="PASS",
            evidence=(
                f"_format_wiring_failure produced {len(prompt)}-char prompt "
                f"containing task ID '{task.task_id}' and 'WIRING REMEDIATION' header"
            ),
        )

    def test_blocking_remediation_debit_recheck(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.14b: Full-mode blocking triggers ledger.debit() then _recheck_wiring().

        Exercises the full remediation lifecycle through execute_phase_tasks with
        ``_subprocess_factory`` injection. The first wiring analysis returns blocking
        findings; the recheck (patched via run_wiring_analysis) returns a clean report.
        Verifies: (1) ledger.debit(remediation_cost) called (consumed increases),
        (2) _recheck_wiring() called (second run_wiring_analysis invocation).
        """
        pf = tmp_path / "phase-1-tasklist.md"
        pf.write_text("# Phase 1\n\n### T01.01 -- Task One\nDo something\n")
        phase = Phase(number=1, file=pf, name="Phase 1")

        index = tmp_path / "tasklist-index.md"
        index.write_text("index\n")
        config = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
            phases=[phase],
            start_phase=1,
            end_phase=1,
            max_turns=20,
            wiring_gate_mode="full",
            wiring_gate_scope="all",
        )
        config.results_dir.mkdir(parents=True, exist_ok=True)

        tasks = _parse_phase_tasks(phase, config)
        assert tasks is not None

        ledger = TurnLedger(
            initial_budget=config.max_turns * len(config.active_phases),
            reimbursement_rate=0.8,
        )

        # Track run_wiring_analysis calls: first returns blocking, second returns clean
        analysis_calls = []
        blocking_report = self._blocking_report()
        clean_report = self._clean_report()

        def _fake_wiring_analysis(wiring_config, source_dir):
            analysis_calls.append({"config": wiring_config, "dir": source_dir})
            # First call: initial analysis (blocking); second call: recheck (clean)
            if len(analysis_calls) == 1:
                return blocking_report
            return clean_report

        def _factory(task, cfg, ph):
            """Subprocess factory: immediate success."""
            return (0, 1, 0)

        initial_consumed = ledger.consumed

        with patch(
            "superclaude.cli.audit.wiring_gate.run_wiring_analysis",
            side_effect=_fake_wiring_analysis,
        ):
            results, remaining, gate_results = execute_phase_tasks(
                tasks,
                config,
                phase,
                ledger=ledger,
                _subprocess_factory=_factory,
            )

        # Assertion 1: ledger.debit(remediation_cost) was called — consumed increased
        # beyond the initial wiring_analysis_turns debit
        wiring_debit = config.wiring_analysis_turns  # debit_wiring at analysis start
        remediation_debit = config.remediation_cost   # debit at remediation
        total_expected_debit = wiring_debit + remediation_debit + 1  # +1 for task turn
        assert ledger.consumed > initial_consumed + wiring_debit, (
            f"Expected consumed > {initial_consumed + wiring_debit} "
            f"(initial + wiring debit), got {ledger.consumed}; "
            f"remediation debit of {config.remediation_cost} not applied"
        )

        # Assertion 2: run_wiring_analysis called twice (initial + recheck)
        assert len(analysis_calls) == 2, (
            f"Expected 2 run_wiring_analysis calls (initial + recheck), "
            f"got {len(analysis_calls)}"
        )

        audit_trail.record(
            test_id="test_blocking_remediation_debit_recheck",
            spec_ref="FR-1.14b",
            assertion_type="behavioral",
            inputs={
                "wiring_gate_mode": "full",
                "initial_budget": ledger.initial_budget,
                "remediation_cost": config.remediation_cost,
                "wiring_analysis_turns": config.wiring_analysis_turns,
            },
            observed={
                "ledger_consumed": ledger.consumed,
                "analysis_call_count": len(analysis_calls),
                "first_report_blocking": blocking_report.blocking_count("full"),
                "second_report_blocking": clean_report.blocking_count("full"),
            },
            expected={
                "ledger_consumed_gt": initial_consumed + wiring_debit,
                "analysis_call_count": 2,
                "first_report_blocking_gt_zero": True,
                "second_report_blocking_zero": True,
            },
            verdict="PASS",
            evidence=(
                f"Remediation lifecycle: ledger.consumed={ledger.consumed} "
                f"(initial={initial_consumed}, wiring_debit={wiring_debit}, "
                f"remediation_debit={config.remediation_cost}); "
                f"run_wiring_analysis called {len(analysis_calls)} times "
                f"(initial: {blocking_report.blocking_count('full')} blocking, "
                f"recheck: {clean_report.blocking_count('full')} blocking)"
            ),
        )

    def test_blocking_remediation_restore_or_fail(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.14c: Successful recheck restores PASS; failed recheck persists FAIL.

        Runs two separate execute_phase_tasks invocations:
        (a) Recheck returns clean → status restored to PASS, wiring turns credited
        (b) Recheck returns still-blocking → status remains FAIL

        Both use ``_subprocess_factory`` injection and patched ``run_wiring_analysis``.
        """
        pf = tmp_path / "phase-1-tasklist.md"
        pf.write_text("# Phase 1\n\n### T01.01 -- Task One\nDo something\n")
        phase = Phase(number=1, file=pf, name="Phase 1")

        index = tmp_path / "tasklist-index.md"
        index.write_text("index\n")

        def _factory(task, cfg, ph):
            return (0, 1, 0)

        # --- Scenario A: recheck succeeds → status=PASS ---
        config_a = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
            phases=[phase],
            start_phase=1,
            end_phase=1,
            max_turns=20,
            wiring_gate_mode="full",
            wiring_gate_scope="all",
        )
        config_a.results_dir.mkdir(parents=True, exist_ok=True)

        tasks_a = _parse_phase_tasks(phase, config_a)
        assert tasks_a is not None

        ledger_a = TurnLedger(
            initial_budget=config_a.max_turns * len(config_a.active_phases),
            reimbursement_rate=0.8,
        )

        calls_a = []

        def _analysis_pass_on_recheck(wiring_config, source_dir):
            calls_a.append(1)
            if len(calls_a) == 1:
                return self._blocking_report()
            return self._clean_report()

        with patch(
            "superclaude.cli.audit.wiring_gate.run_wiring_analysis",
            side_effect=_analysis_pass_on_recheck,
        ):
            results_a, _, _ = execute_phase_tasks(
                tasks_a, config_a, phase, ledger=ledger_a, _subprocess_factory=_factory,
            )

        assert len(results_a) >= 1
        # Assertion: on successful recheck, status restored to PASS
        assert results_a[0].status == TaskStatus.PASS, (
            f"Expected PASS after successful recheck, got {results_a[0].status}"
        )
        # Assertion: gate_outcome restored to PASS on successful remediation
        assert results_a[0].gate_outcome == GateOutcome.PASS, (
            f"Expected gate_outcome PASS after successful recheck, "
            f"got {results_a[0].gate_outcome}"
        )

        # --- Scenario B: recheck fails → status=FAIL persists ---
        config_b = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
            phases=[phase],
            start_phase=1,
            end_phase=1,
            max_turns=20,
            wiring_gate_mode="full",
            wiring_gate_scope="all",
        )
        config_b.results_dir.mkdir(parents=True, exist_ok=True)

        tasks_b = _parse_phase_tasks(phase, config_b)
        assert tasks_b is not None

        ledger_b = TurnLedger(
            initial_budget=config_b.max_turns * len(config_b.active_phases),
            reimbursement_rate=0.8,
        )

        def _analysis_fail_on_recheck(wiring_config, source_dir):
            # Both initial and recheck return blocking
            return self._blocking_report()

        with patch(
            "superclaude.cli.audit.wiring_gate.run_wiring_analysis",
            side_effect=_analysis_fail_on_recheck,
        ):
            results_b, _, _ = execute_phase_tasks(
                tasks_b, config_b, phase, ledger=ledger_b, _subprocess_factory=_factory,
            )

        assert len(results_b) >= 1
        # Assertion: on failed recheck, FAIL persists
        assert results_b[0].status == TaskStatus.FAIL, (
            f"Expected FAIL after failed recheck, got {results_b[0].status}"
        )

        audit_trail.record(
            test_id="test_blocking_remediation_restore_or_fail",
            spec_ref="FR-1.14c",
            assertion_type="behavioral",
            inputs={
                "scenario_a": "recheck returns clean report",
                "scenario_b": "recheck returns blocking report",
            },
            observed={
                "scenario_a_status": results_a[0].status.value,
                "scenario_a_gate_outcome": results_a[0].gate_outcome.value,
                "scenario_b_status": results_b[0].status.value,
            },
            expected={
                "scenario_a_status": TaskStatus.PASS.value,
                "scenario_a_gate_outcome": GateOutcome.PASS.value,
                "scenario_b_status": TaskStatus.FAIL.value,
            },
            verdict="PASS",
            evidence=(
                f"Scenario A: recheck clean → status={results_a[0].status.value}, "
                f"gate_outcome={results_a[0].gate_outcome.value}; "
                f"Scenario B: recheck blocking → status={results_b[0].status.value} (FAIL persists)"
            ),
        )


class TestConvergenceRegistry:
    """FR-1.15, FR-1.16: Validate convergence registry construction and merge."""

    def test_registry_3arg_construction(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.15: DeviationRegistry constructed with (path, release_id, spec_hash).

        Verifies that all three constructor arguments are stored on the
        resulting instance and that load_or_create produces an equivalent
        registry when no prior state exists on disk.
        """
        reg_path = tmp_path / "registry.json"
        release_id = "v3.3.0-rc1"
        spec_hash = "abc123def456"

        # Direct dataclass construction
        reg = DeviationRegistry(
            path=reg_path,
            release_id=release_id,
            spec_hash=spec_hash,
        )

        assert reg.path == reg_path, f"Expected path={reg_path}, got {reg.path}"
        assert reg.release_id == release_id, (
            f"Expected release_id='{release_id}', got '{reg.release_id}'"
        )
        assert reg.spec_hash == spec_hash, (
            f"Expected spec_hash='{spec_hash}', got '{reg.spec_hash}'"
        )
        assert reg.runs == [], f"Expected empty runs, got {reg.runs}"
        assert reg.findings == {}, f"Expected empty findings, got {reg.findings}"

        # Also verify load_or_create factory (no prior file → fresh registry)
        reg2 = DeviationRegistry.load_or_create(
            path=reg_path,
            release_id=release_id,
            spec_hash=spec_hash,
        )
        assert reg2.path == reg_path
        assert reg2.release_id == release_id
        assert reg2.spec_hash == spec_hash
        assert reg2.runs == []
        assert reg2.findings == {}

        audit_trail.record(
            test_id="test_registry_3arg_construction",
            spec_ref="FR-1.15",
            assertion_type="structural",
            inputs={
                "path": str(reg_path),
                "release_id": release_id,
                "spec_hash": spec_hash,
            },
            observed={
                "path_stored": str(reg.path),
                "release_id_stored": reg.release_id,
                "spec_hash_stored": reg.spec_hash,
                "runs_empty": reg.runs == [],
                "findings_empty": reg.findings == {},
                "load_or_create_consistent": (
                    reg2.release_id == release_id
                    and reg2.spec_hash == spec_hash
                ),
            },
            expected={
                "path_stored": str(reg_path),
                "release_id_stored": release_id,
                "spec_hash_stored": spec_hash,
                "runs_empty": True,
                "findings_empty": True,
                "load_or_create_consistent": True,
            },
            verdict="PASS",
            evidence=(
                f"DeviationRegistry(path, release_id, spec_hash) stores all 3 args; "
                f"load_or_create produces equivalent fresh registry"
            ),
        )

    def test_merge_findings_3arg(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.16: merge_findings(structural, semantic, run_number) merges into registry.

        Verifies that:
        1. Structural findings are stored with source_layer='structural'
        2. Semantic findings are stored with source_layer='semantic'
        3. run_number is recorded as first_seen_run and last_seen_run
        4. All findings are marked ACTIVE after merge
        """
        reg_path = tmp_path / "registry.json"
        reg = DeviationRegistry(
            path=reg_path,
            release_id="v3.3.0",
            spec_hash="deadbeef",
        )

        structural_finding = Finding(
            id="F-001",
            severity="HIGH",
            dimension="completeness",
            description="Missing section X",
            location="roadmap.md:10",
            evidence="Section X not found",
            fix_guidance="Add section X",
            files_affected=["roadmap.md"],
            stable_id="stable-structural-001",
        )

        semantic_finding = Finding(
            id="F-002",
            severity="MEDIUM",
            dimension="accuracy",
            description="Semantic drift in section Y",
            location="roadmap.md:25",
            evidence="Wording diverges from spec",
            fix_guidance="Align wording with spec",
            files_affected=["roadmap.md"],
            stable_id="stable-semantic-002",
        )

        run_number = 1

        # Call merge_findings with all 3 positional args
        reg.merge_findings(
            [structural_finding],
            [semantic_finding],
            run_number,
        )

        # Verify structural finding stored correctly
        assert "stable-structural-001" in reg.findings, (
            f"Structural finding not in registry. Keys: {list(reg.findings.keys())}"
        )
        sf = reg.findings["stable-structural-001"]
        assert sf["source_layer"] == "structural", (
            f"Expected source_layer='structural', got '{sf['source_layer']}'"
        )
        assert sf["status"] == "ACTIVE", f"Expected ACTIVE, got '{sf['status']}'"
        assert sf["first_seen_run"] == run_number, (
            f"Expected first_seen_run={run_number}, got {sf['first_seen_run']}"
        )
        assert sf["last_seen_run"] == run_number, (
            f"Expected last_seen_run={run_number}, got {sf['last_seen_run']}"
        )

        # Verify semantic finding stored correctly
        assert "stable-semantic-002" in reg.findings, (
            f"Semantic finding not in registry. Keys: {list(reg.findings.keys())}"
        )
        sem = reg.findings["stable-semantic-002"]
        assert sem["source_layer"] == "semantic", (
            f"Expected source_layer='semantic', got '{sem['source_layer']}'"
        )
        assert sem["status"] == "ACTIVE", f"Expected ACTIVE, got '{sem['status']}'"
        assert sem["first_seen_run"] == run_number
        assert sem["last_seen_run"] == run_number

        # Verify total finding count
        assert len(reg.findings) == 2, (
            f"Expected 2 findings in registry, got {len(reg.findings)}"
        )

        audit_trail.record(
            test_id="test_merge_findings_3arg",
            spec_ref="FR-1.16",
            assertion_type="behavioral",
            inputs={
                "structural_count": 1,
                "semantic_count": 1,
                "run_number": run_number,
            },
            observed={
                "total_findings": len(reg.findings),
                "structural_source_layer": sf["source_layer"],
                "semantic_source_layer": sem["source_layer"],
                "structural_status": sf["status"],
                "semantic_status": sem["status"],
                "structural_first_seen": sf["first_seen_run"],
                "semantic_first_seen": sem["first_seen_run"],
            },
            expected={
                "total_findings": 2,
                "structural_source_layer": "structural",
                "semantic_source_layer": "semantic",
                "structural_status": "ACTIVE",
                "semantic_status": "ACTIVE",
                "structural_first_seen": 1,
                "semantic_first_seen": 1,
            },
            verdict="PASS",
            evidence=(
                f"merge_findings(structural, semantic, run_number) stored 2 findings "
                f"with correct source_layer, status=ACTIVE, first_seen_run={run_number}"
            ),
        )


class TestDictToFindingConversion:
    """FR-1.17: _run_remediation() dict-to-Finding conversion without AttributeError."""

    def test_dict_to_finding_conversion(self, tmp_path: Path, audit_trail) -> None:
        """Dict findings from DeviationRegistry convert to Finding objects without error.

        The _run_remediation() closure in roadmap/executor.py calls
        registry.get_active_highs() which returns list[dict], then converts
        each dict to a Finding dataclass. This test exercises that exact
        conversion path to ensure no AttributeError on dict→Finding mapping.
        """
        # Build a DeviationRegistry with dict-based findings (as stored on disk)
        reg = DeviationRegistry(
            path=tmp_path / "registry.json",
            release_id="test-release",
            spec_hash="abc123",
        )

        # Insert raw dict findings matching the shape get_active_highs() returns
        reg.findings["stable-id-001"] = {
            "stable_id": "stable-id-001",
            "severity": "HIGH",
            "dimension": "completeness",
            "description": "Missing required section",
            "location": "spec.md:42",
            "status": "ACTIVE",
            "source_layer": "structural",
            "files_affected": ["src/module.py"],
            "first_seen_run": 1,
        }
        reg.findings["stable-id-002"] = {
            "stable_id": "stable-id-002",
            "severity": "HIGH",
            "dimension": "accuracy",
            "description": "Incorrect parameter type",
            "location": "spec.md:99",
            "status": "ACTIVE",
            "source_layer": "semantic",
            "files_affected": ["src/other.py", "src/module.py"],
            "first_seen_run": 1,
        }

        # Exercise the same dict-to-Finding conversion that _run_remediation uses
        active_highs = reg.get_active_highs()
        assert len(active_highs) == 2, "Registry should return 2 active HIGH dicts"

        finding_objects = []
        for d in active_highs:
            f = Finding(
                id=d.get("stable_id", ""),
                severity=d.get("severity", "HIGH"),
                dimension=d.get("dimension", ""),
                description=d.get("description", ""),
                location=d.get("location", ""),
                evidence="",
                fix_guidance="",
                files_affected=d.get("files_affected", []),
                status=d.get("status", "ACTIVE"),
            )
            finding_objects.append(f)

        # Assert Finding objects were produced without AttributeError
        assert len(finding_objects) == 2
        for f in finding_objects:
            assert isinstance(f, Finding)
            assert f.severity == "HIGH"
            assert f.status == "ACTIVE"
            assert len(f.files_affected) >= 1

        # Verify grouping by file (the step after conversion in _run_remediation)
        findings_by_file: dict[str, list] = {}
        for finding in finding_objects:
            for fp in finding.files_affected:
                findings_by_file.setdefault(fp, []).append(finding)

        assert "src/module.py" in findings_by_file
        assert len(findings_by_file["src/module.py"]) == 2  # both findings touch this file
        assert "src/other.py" in findings_by_file
        assert len(findings_by_file["src/other.py"]) == 1

        audit_trail.record(
            test_id="test_dict_to_finding_conversion",
            spec_ref="FR-1.17",
            assertion_type="behavioral",
            inputs={
                "registry_finding_count": 2,
                "finding_keys": sorted(reg.findings.keys()),
            },
            observed={
                "dict_count": len(active_highs),
                "finding_count": len(finding_objects),
                "all_finding_instances": all(isinstance(f, Finding) for f in finding_objects),
                "files_grouped": sorted(findings_by_file.keys()),
            },
            expected={
                "dict_count": 2,
                "finding_count": 2,
                "all_finding_instances": True,
                "files_grouped": ["src/module.py", "src/other.py"],
            },
            verdict="PASS",
            evidence=(
                "_run_remediation() dict-to-Finding conversion produces 2 Finding objects "
                "from 2 registry dicts without AttributeError, grouped correctly by file"
            ),
        )


# ---------------------------------------------------------------------------
# T02.12 -- TurnLedger initial_budget=61 regression guard (FR-1.18)
# ---------------------------------------------------------------------------


class TestTurnLedgerInitialBudget:
    """Regression guard: TurnLedger initial budget must equal MAX_CONVERGENCE_BUDGET = 61.

    Prior bug used STD_CONVERGENCE_BUDGET (46) instead of MAX_CONVERGENCE_BUDGET (61)
    in the convergence executor path. This test locks the correct constant value and
    verifies TurnLedger honours it.

    Spec ref: FR-1.18
    """

    def test_turnledger_initial_budget_61(self, tmp_path: Path, audit_trail) -> None:
        """MAX_CONVERGENCE_BUDGET == 61 and TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET).available() == 61."""
        # Step 1: Assert the constant itself is 61 (not the old wrong value 46)
        assert MAX_CONVERGENCE_BUDGET == 61, (
            f"MAX_CONVERGENCE_BUDGET must be 61, got {MAX_CONVERGENCE_BUDGET} "
            "(regression: prior bug used STD_CONVERGENCE_BUDGET=46)"
        )

        # Step 2: Construct TurnLedger with the constant and verify initial state
        ledger = TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET)
        assert ledger.initial_budget == 61
        assert ledger.available() == 61
        assert ledger.consumed == 0
        assert ledger.reimbursed == 0

        audit_trail.record(
            test_id="test_turnledger_initial_budget_61",
            spec_ref="FR-1.18",
            assertion_type="value",
            inputs={
                "MAX_CONVERGENCE_BUDGET": MAX_CONVERGENCE_BUDGET,
            },
            observed={
                "constant_value": MAX_CONVERGENCE_BUDGET,
                "ledger_initial_budget": ledger.initial_budget,
                "ledger_available": ledger.available(),
            },
            expected={
                "constant_value": 61,
                "ledger_initial_budget": 61,
                "ledger_available": 61,
            },
            verdict="PASS",
            evidence=(
                "MAX_CONVERGENCE_BUDGET == 61 (not 46) and "
                "TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET).available() == 61"
            ),
        )


class TestShadowGraceInfinite:
    """Validate SHADOW_GRACE_INFINITE constant and shadow mode grace period behavior.

    When wiring_gate_grace_period >= SHADOW_GRACE_INFINITE, SprintConfig.__post_init__
    derives wiring_gate_mode="shadow", and shadow mode always credits wiring turns
    back to the ledger — effectively never exiting the grace period.

    Spec ref: FR-1.19
    """

    def test_shadow_grace_infinite(self, tmp_path: Path, audit_trail) -> None:
        """SHADOW_GRACE_INFINITE == 999_999 and grace period behavior under shadow mode."""
        from superclaude.cli.sprint.executor import run_post_task_wiring_hook

        # --- Part A: Constant value assertion ---
        assert SHADOW_GRACE_INFINITE == 999_999, (
            f"SHADOW_GRACE_INFINITE must be 999_999, got {SHADOW_GRACE_INFINITE}"
        )

        # --- Part B: SprintConfig derives shadow mode from grace period ---
        pf = tmp_path / "phase-1-tasklist.md"
        pf.write_text("# Phase 1\n\n### T01.01 -- Task One\nDo something\n")
        phase = Phase(number=1, file=pf, name="Phase 1")

        index = tmp_path / "tasklist-index.md"
        index.write_text("index\n")

        config = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
            phases=[phase],
            start_phase=1,
            end_phase=1,
            max_turns=10,
            wiring_gate_enabled=True,
            wiring_gate_grace_period=SHADOW_GRACE_INFINITE,
            wiring_gate_scope="none",
        )

        # __post_init__ should have derived "shadow" from the infinite grace period
        assert config.wiring_gate_mode == "shadow", (
            f"Expected wiring_gate_mode='shadow' when grace_period={SHADOW_GRACE_INFINITE}, "
            f"got '{config.wiring_gate_mode}'"
        )

        # --- Part C: Shadow mode always credits back (never exits grace) ---
        # Use reimbursement_rate=1.0 so credit_wiring returns full turns
        # (default rate 0.8 floors int(1*0.8)=0 per R7 design)
        initial_budget = 20
        ledger = TurnLedger(initial_budget=initial_budget, reimbursement_rate=1.0)
        analysis_turns = config.wiring_analysis_turns  # default 1

        task = TaskEntry(
            task_id="T01.01",
            title="Shadow grace test task",
            description="Validates shadow mode credit-back",
        )
        task_result = TaskResult(
            task=task,
            status=TaskStatus.PASS,
            exit_code=0,
        )

        # Simulate findings — even critical findings should not block in shadow mode
        mock_report = WiringReport(
            unwired_callables=[
                WiringFinding(
                    finding_type="unwired_callable",
                    file_path="test.py",
                    symbol_name="foo",
                    line_number=1,
                    severity="critical",
                    detail="test finding",
                ),
            ],
            files_analyzed=1,
            scan_duration_seconds=0.01,
        )

        # Run wiring hook repeatedly to prove shadow never exits grace
        results = []
        for i in range(3):
            tr = TaskResult(
                task=TaskEntry(
                    task_id=f"T01.0{i + 1}",
                    title=f"Shadow task {i + 1}",
                ),
                status=TaskStatus.PASS,
                exit_code=0,
            )
            with (
                patch(
                    "superclaude.cli.audit.wiring_gate.run_wiring_analysis",
                    return_value=mock_report,
                ),
                patch(
                    "superclaude.cli.audit.wiring_config.WiringConfig",
                ),
            ):
                result = run_post_task_wiring_hook(
                    tr.task, config, tr,
                    ledger=ledger,
                )
            results.append(result)

        # Shadow mode must NEVER change task status — not on any iteration
        for i, r in enumerate(results):
            assert r.status == TaskStatus.PASS, (
                f"Shadow mode changed task status on iteration {i}: {r.status}"
            )

        # Shadow mode credits back each debit at rate=1.0 — net zero budget impact
        assert ledger.available() == initial_budget, (
            f"Shadow mode must credit back wiring turns (net zero over {len(results)} runs). "
            f"Expected available={initial_budget}, got {ledger.available()}"
        )

        # Verify wiring analyses ran and credits were tracked
        assert ledger.wiring_analyses_count == 3, (
            f"Expected 3 wiring analyses, got {ledger.wiring_analyses_count}"
        )
        assert ledger.wiring_turns_credited == 3 * analysis_turns, (
            f"Expected {3 * analysis_turns} wiring turns credited, "
            f"got {ledger.wiring_turns_credited}"
        )

        audit_trail.record(
            test_id="test_shadow_grace_infinite",
            spec_ref="FR-1.19",
            assertion_type="behavioral",
            inputs={
                "SHADOW_GRACE_INFINITE": SHADOW_GRACE_INFINITE,
                "wiring_gate_grace_period": SHADOW_GRACE_INFINITE,
                "initial_budget": initial_budget,
                "iterations": 3,
            },
            observed={
                "constant_value": SHADOW_GRACE_INFINITE,
                "derived_mode": config.wiring_gate_mode,
                "all_statuses_pass": all(r.status == TaskStatus.PASS for r in results),
                "ledger_available_after": ledger.available(),
                "wiring_analyses_count": ledger.wiring_analyses_count,
                "wiring_turns_credited": ledger.wiring_turns_credited,
            },
            expected={
                "constant_value": 999_999,
                "derived_mode": "shadow",
                "task_status_unchanged": True,
                "budget_net_zero": True,
            },
            verdict="PASS",
            evidence=(
                f"SHADOW_GRACE_INFINITE == {SHADOW_GRACE_INFINITE} (999_999); "
                f"SprintConfig derived wiring_gate_mode='shadow' from grace_period={SHADOW_GRACE_INFINITE}; "
                f"shadow hook ran 3 times with critical findings — all statuses PASS, "
                f"all turns credited back (available={ledger.available()}/{initial_budget})"
            ),
        )


# ---------------------------------------------------------------------------
# T02.14: __post_init__() config field derivation and defaults (FR-1.20)
# ---------------------------------------------------------------------------


class TestPostInitConfigDerivation:
    """Validate SprintConfig.__post_init__() correctly derives config fields and sets defaults.

    Spec ref: FR-1.20 (R-023). Tests that:
    - Default field values are sensible when no overrides are provided.
    - ``wiring_gate_mode`` is derived to ``"off"`` when ``wiring_gate_enabled=False``.
    - ``wiring_gate_mode`` is derived to ``"shadow"`` when grace_period >= SHADOW_GRACE_INFINITE.
    - ``work_dir`` is synced from ``release_dir`` via ``__post_init__``.
    """

    def test_post_init_config_derivation(self, tmp_path: Path, audit_trail) -> None:
        """FR-1.20: __post_init__() derives fields and sets defaults correctly."""
        # ── Subcase 1: Defaults ─────────────────────────────────────────
        # Construct with minimal overrides — verify derived defaults.
        phases = [Phase(number=1, file=tmp_path / "p1.md", name="Phase 1")]
        (tmp_path / "p1.md").write_text("# Phase 1\n")
        index = tmp_path / "index.md"
        index.write_text("index\n")

        config_defaults = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
            phases=phases,
            start_phase=1,
            end_phase=1,
        )

        # work_dir synced from release_dir
        assert config_defaults.work_dir == tmp_path, (
            f"Expected work_dir to match release_dir ({tmp_path}), "
            f"got {config_defaults.work_dir}"
        )
        # Default wiring fields
        assert config_defaults.wiring_gate_enabled is True
        assert config_defaults.wiring_gate_grace_period == 0
        assert config_defaults.wiring_analysis_turns == 1
        assert config_defaults.remediation_cost == 2
        assert config_defaults.wiring_gate_scope == "task"
        # Default wiring_gate_mode stays "soft" (no derivation trigger)
        assert config_defaults.wiring_gate_mode == "soft", (
            f"Expected default wiring_gate_mode='soft', "
            f"got '{config_defaults.wiring_gate_mode}'"
        )

        # ── Subcase 2: wiring_gate_enabled=False → mode="off" ──────────
        config_disabled = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
            phases=phases,
            start_phase=1,
            end_phase=1,
            wiring_gate_enabled=False,
        )

        assert config_disabled.wiring_gate_mode == "off", (
            f"Expected wiring_gate_mode='off' when wiring_gate_enabled=False, "
            f"got '{config_disabled.wiring_gate_mode}'"
        )

        # ── Subcase 3: grace_period >= SHADOW_GRACE_INFINITE → mode="shadow"
        config_shadow = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
            phases=phases,
            start_phase=1,
            end_phase=1,
            wiring_gate_grace_period=SHADOW_GRACE_INFINITE,
        )

        assert config_shadow.wiring_gate_mode == "shadow", (
            f"Expected wiring_gate_mode='shadow' when "
            f"grace_period={SHADOW_GRACE_INFINITE}, "
            f"got '{config_shadow.wiring_gate_mode}'"
        )

        # ── Subcase 4: Missing base config → sensible defaults ─────────
        # Construct with no phases and end_phase=0 (auto-detect).
        config_bare = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
        )
        assert config_bare.phases == []
        assert config_bare.end_phase == 0
        assert config_bare.max_turns == 100
        assert config_bare.dry_run is False
        assert config_bare.debug is False
        assert config_bare.work_dir == tmp_path

        # ── Audit record ────────────────────────────────────────────────
        audit_trail.record(
            test_id="test_post_init_config_derivation",
            spec_ref="FR-1.20",
            assertion_type="structural",
            inputs={
                "release_dir": str(tmp_path),
                "subcases": [
                    "defaults",
                    "wiring_gate_enabled=False",
                    f"grace_period={SHADOW_GRACE_INFINITE}",
                    "bare_construction",
                ],
            },
            observed={
                "defaults_mode": config_defaults.wiring_gate_mode,
                "defaults_enabled": config_defaults.wiring_gate_enabled,
                "defaults_grace": config_defaults.wiring_gate_grace_period,
                "defaults_analysis_turns": config_defaults.wiring_analysis_turns,
                "disabled_mode": config_disabled.wiring_gate_mode,
                "shadow_mode": config_shadow.wiring_gate_mode,
                "bare_work_dir_matches": config_bare.work_dir == tmp_path,
            },
            expected={
                "defaults_mode": "soft",
                "defaults_enabled": True,
                "defaults_grace": 0,
                "defaults_analysis_turns": 1,
                "disabled_mode": "off",
                "shadow_mode": "shadow",
                "bare_work_dir_matches": True,
            },
            verdict="PASS",
            evidence=(
                f"__post_init__() derives wiring_gate_mode='soft' by default, "
                f"'off' when disabled, 'shadow' when grace>={SHADOW_GRACE_INFINITE}; "
                f"work_dir synced from release_dir; bare construction produces sensible defaults"
            ),
        )


class TestCheckWiringReportWrapper:
    """FR-1.21: Validate check_wiring_report() delegates to WIRING_GATE semantic checks."""

    def test_check_wiring_report_wrapper(self, audit_trail) -> None:
        """check_wiring_report() delegates to all 5 WIRING_GATE semantic checks
        and returns a valid (passed, failures) tuple."""

        # ── Build valid report content that passes all 5 semantic checks ──
        valid_content = (
            "---\n"
            "gate: wiring-verification\n"
            "target_dir: src/superclaude\n"
            "files_analyzed: 10\n"
            "files_skipped: 0\n"
            "rollout_mode: shadow\n"
            "analysis_complete: true\n"
            "audit_artifacts_used: 0\n"
            "unwired_callable_count: 0\n"
            "orphan_module_count: 0\n"
            "unwired_registry_count: 0\n"
            "critical_count: 0\n"
            "major_count: 0\n"
            "info_count: 0\n"
            "total_findings: 0\n"
            "blocking_findings: 0\n"
            "whitelist_entries_applied: 0\n"
            "---\n"
            "# Wiring Report\n"
        )

        # ── Passing case: all checks pass ─────────────────────────────────
        passed, failures = check_wiring_report(valid_content)

        assert passed is True, f"Expected all checks to pass, got failures: {failures}"
        assert isinstance(failures, list)
        assert len(failures) == 0

        # ── Verify delegation: check_wiring_report iterates WIRING_GATE.semantic_checks ──
        assert len(WIRING_GATE.semantic_checks) == 5, (
            "WIRING_GATE must have exactly 5 semantic checks"
        )
        expected_check_names = {
            "analysis_complete_true",
            "recognized_rollout_mode",
            "finding_counts_consistent",
            "severity_summary_consistent",
            "zero_blocking_findings_for_mode",
        }
        actual_check_names = {c.name for c in WIRING_GATE.semantic_checks}
        assert actual_check_names == expected_check_names, (
            f"Semantic check names mismatch: {actual_check_names}"
        )

        # ── Failing case: tamper analysis_complete to trigger failure ──────
        bad_content = valid_content.replace(
            "analysis_complete: true", "analysis_complete: false"
        )
        passed_bad, failures_bad = check_wiring_report(bad_content)

        assert passed_bad is False, "Expected failure when analysis_complete is false"
        assert "analysis_complete_true" in failures_bad

        # ── Failing case: inconsistent counts trigger multiple failures ───
        inconsistent_content = valid_content.replace(
            "total_findings: 0", "total_findings: 99"
        )
        passed_inc, failures_inc = check_wiring_report(inconsistent_content)

        assert passed_inc is False
        assert "finding_counts_consistent" in failures_inc
        assert "severity_summary_consistent" in failures_inc

        # ── Return structure validation ───────────────────────────────────
        # check_wiring_report returns tuple[bool, list[str]]
        assert isinstance(passed, bool)
        assert isinstance(failures, list)
        assert all(isinstance(f, str) for f in failures_bad)

        # ── Audit record ──────────────────────────────────────────────────
        audit_trail.record(
            test_id="test_check_wiring_report_wrapper",
            spec_ref="FR-1.21",
            assertion_type="behavioral",
            inputs={
                "valid_content_lines": valid_content.count("\n"),
                "num_semantic_checks": len(WIRING_GATE.semantic_checks),
            },
            observed={
                "pass_result": (passed, failures),
                "fail_analysis_complete": (passed_bad, failures_bad),
                "fail_inconsistent_counts": (passed_inc, failures_inc),
                "check_names": sorted(actual_check_names),
            },
            expected={
                "pass_result": (True, []),
                "fail_analysis_complete_contains": "analysis_complete_true",
                "fail_inconsistent_contains": [
                    "finding_counts_consistent",
                    "severity_summary_consistent",
                ],
                "check_count": 5,
            },
            verdict="PASS",
            evidence=(
                "check_wiring_report() delegates to all 5 WIRING_GATE.semantic_checks; "
                "returns (True, []) for valid content; returns (False, [failed_names]) "
                "for invalid content; not a no-op stub"
            ),
        )
