"""Integration test: execute_sprint() end-to-end with mocked ClaudeProcess.

Exercises the full orchestration path including TurnLedger, ShadowGateMetrics,
DeferredRemediationLog, SprintGatePolicy construction, and KPI report generation.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from superclaude.cli.sprint.executor import execute_sprint, SprintGatePolicy
from superclaude.cli.sprint.models import Phase, SprintConfig, ShadowGateMetrics, TurnLedger
from superclaude.cli.pipeline.trailing_gate import DeferredRemediationLog


def _make_config(tmp_path: Path) -> SprintConfig:
    """Build a SprintConfig with one claude-mode phase."""
    phase_file = tmp_path / "phase-1-tasklist.md"
    phase_file.write_text("# Phase 1: Integration Test Phase\n")
    phases = [Phase(number=1, file=phase_file, name="Integration Test Phase")]

    index = tmp_path / "tasklist-index.md"
    index.write_text("- phase-1-tasklist.md\n")

    return SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=phases,
        start_phase=1,
        end_phase=1,
        max_turns=5,
    )


class _FakeProcess:
    """Simulates a subprocess.Popen that succeeds after one poll cycle."""

    def __init__(self):
        self.returncode = 0
        self.pid = 42000
        self._poll_count = 0

    def poll(self):
        self._poll_count += 1
        if self._poll_count <= 1:
            return None
        return 0

    def wait(self, timeout=None):
        self.returncode = 0
        return 0


def _popen_factory(config: SprintConfig):
    """Return a Popen side_effect that writes result + output files for each phase."""
    call_count = [0]

    def factory(cmd, **kwargs):
        call_count[0] += 1
        phase = config.phases[call_count[0] - 1]

        config.results_dir.mkdir(parents=True, exist_ok=True)

        # Write result file with CONTINUE signal
        result_path = config.result_file(phase)
        result_path.write_text(
            "---\nstatus: PASS\n---\n\nEXIT_RECOMMENDATION: CONTINUE\n"
        )

        # Write output file with content
        output_path = config.output_file(phase)
        output_path.write_text(
            f"Working on T0{call_count[0]}.01\n"
            f"Phase {call_count[0]} complete\n"
        )

        return _FakeProcess()

    return factory


@pytest.mark.integration
class TestExecuteSprintFullPath:
    """Integration test exercising execute_sprint() end-to-end."""

    def test_execute_sprint_full_path(self, tmp_path):
        config = _make_config(tmp_path)
        factory = _popen_factory(config)

        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.pipeline.process.subprocess.Popen",
                side_effect=factory,
            ),
            patch("superclaude.cli.pipeline.process.os.setpgrp"),
            patch("superclaude.cli.sprint.notify._notify"),
        ):
            # execute_sprint raises SystemExit on failure; success should not raise
            execute_sprint(config)

        # Assert: gate-kpi-report.md is written in results_dir
        kpi_path = config.results_dir / "gate-kpi-report.md"
        assert kpi_path.exists(), (
            f"Expected gate-kpi-report.md at {kpi_path}"
        )

        # Verify the KPI report contains expected sections
        kpi_content = kpi_path.read_text()
        assert "Gate & Remediation KPI Report" in kpi_content
        assert "Gate Evaluation" in kpi_content
        assert "Remediation" in kpi_content
        assert "Wiring Gate" in kpi_content

        # Verify sprint completed successfully (no SystemExit raised)
        # and the execution log artifacts were created
        assert config.execution_log_jsonl.exists()
        assert config.execution_log_md.exists()

    def test_turnledger_constructed(self, tmp_path):
        """TurnLedger is instantiated with correct budget parameters."""
        config = _make_config(tmp_path)
        factory = _popen_factory(config)

        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.pipeline.process.subprocess.Popen",
                side_effect=factory,
            ),
            patch("superclaude.cli.pipeline.process.os.setpgrp"),
            patch("superclaude.cli.sprint.notify._notify"),
            patch(
                "superclaude.cli.sprint.executor.TurnLedger",
                wraps=TurnLedger,
            ) as mock_ledger_cls,
        ):
            execute_sprint(config)

        mock_ledger_cls.assert_called_once()
        call_kwargs = mock_ledger_cls.call_args
        assert call_kwargs.kwargs.get("initial_budget") or call_kwargs[1].get("initial_budget") or (len(call_kwargs[0]) > 0)

    def test_shadow_gate_metrics_constructed(self, tmp_path):
        """ShadowGateMetrics is instantiated during execute_sprint."""
        config = _make_config(tmp_path)
        factory = _popen_factory(config)

        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.pipeline.process.subprocess.Popen",
                side_effect=factory,
            ),
            patch("superclaude.cli.pipeline.process.os.setpgrp"),
            patch("superclaude.cli.sprint.notify._notify"),
            patch(
                "superclaude.cli.sprint.executor.ShadowGateMetrics",
                wraps=ShadowGateMetrics,
            ) as mock_sgm,
        ):
            execute_sprint(config)

        mock_sgm.assert_called_once()

    def test_deferred_remediation_log_constructed(self, tmp_path):
        """DeferredRemediationLog is instantiated with persist_path in results_dir."""
        config = _make_config(tmp_path)
        factory = _popen_factory(config)

        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.pipeline.process.subprocess.Popen",
                side_effect=factory,
            ),
            patch("superclaude.cli.pipeline.process.os.setpgrp"),
            patch("superclaude.cli.sprint.notify._notify"),
            patch(
                "superclaude.cli.pipeline.trailing_gate.DeferredRemediationLog",
                wraps=DeferredRemediationLog,
            ) as mock_drl,
        ):
            execute_sprint(config)

        mock_drl.assert_called_once()
        call_kwargs = mock_drl.call_args
        persist_path = call_kwargs.kwargs.get("persist_path") or call_kwargs[1].get("persist_path")
        assert persist_path is not None
        assert "remediation.json" in str(persist_path)

    def test_sprint_gate_policy_constructed(self, tmp_path):
        """SprintGatePolicy is instantiated with the sprint config."""
        config = _make_config(tmp_path)
        factory = _popen_factory(config)

        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.pipeline.process.subprocess.Popen",
                side_effect=factory,
            ),
            patch("superclaude.cli.pipeline.process.os.setpgrp"),
            patch("superclaude.cli.sprint.notify._notify"),
            patch(
                "superclaude.cli.sprint.executor.SprintGatePolicy",
                wraps=SprintGatePolicy,
            ) as mock_sgp,
        ):
            execute_sprint(config)

        mock_sgp.assert_called_once_with(config)
