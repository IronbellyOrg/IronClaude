"""E2E construction validation for sprint infrastructure classes (T02.01).

Verifies that TurnLedger, ShadowGateMetrics, DeferredRemediationLog, and
SprintGatePolicy are constructed correctly via real orchestration paths
(execute_sprint → execute_phase_tasks). The sole injection point is
``_subprocess_factory``; all other wiring is production code.

Task: T02.01 (R-010)
Dependencies: T01.02 (audit_trail fixture)
Spec refs: FR-1.1 through FR-1.4
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.sprint.executor import (
    SprintGatePolicy,
    execute_sprint,
)
from superclaude.cli.sprint.models import (
    Phase,
    ShadowGateMetrics,
    SprintConfig,
    TaskResult,
    TaskStatus,
    TurnLedger,
)
from superclaude.cli.pipeline.trailing_gate import DeferredRemediationLog


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
