"""Tests for DiagnosticsCollector and DiagnosticsBundle (FR-042, T09.03).

Acceptance criteria:
- DiagnosticsBundle contains gate_failures, exit_code, missing_artifacts, resume_guidance
- emit_diagnostics() writes diagnostics.md to workdir with all collected fields
- Gate failure from G-003 shows missing section name in diagnostic message

Validation commands:
  uv run pytest tests/cli_portify/test_diagnostics.py -k "diagnostics_collector" -v
  uv run pytest tests/cli_portify/test_diagnostics.py -k "diagnostics_emit" -v
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.cli_portify.diagnostics import (
    DiagnosticsBundle,
    DiagnosticsCollector,
)
from superclaude.cli.cli_portify.gates import GateFailure


# ---------------------------------------------------------------------------
# T09.03 acceptance criteria: diagnostics_collector
# ---------------------------------------------------------------------------


class TestDiagnosticsCollector:
    """DiagnosticsCollector records and bundles failure context.

    Validation command: uv run pytest tests/ -k "diagnostics_collector"
    """

    def test_diagnostics_collector_bundle_has_required_fields(self):
        """DiagnosticsBundle contains gate_failures, exit_code, missing_artifacts, resume_guidance."""
        collector = DiagnosticsCollector()
        bundle = collector.build_bundle(step_id="analyze-workflow")
        assert hasattr(bundle, "gate_failures")
        assert hasattr(bundle, "exit_code")
        assert hasattr(bundle, "missing_artifacts")
        assert hasattr(bundle, "resume_guidance")

    def test_diagnostics_collector_record_gate_failure(self):
        """record_gate_failure() stores GateFailure in bundle."""
        collector = DiagnosticsCollector()
        failure = GateFailure(
            gate_id="G-003",
            check_name="has_required_analysis_sections",
            diagnostic="Missing sections: ['Source Components', 'Step Graph']",
            artifact_path="/workdir/analyze-workflow.md",
            tier="STRICT",
        )
        collector.record_gate_failure(failure)
        bundle = collector.build_bundle(step_id="analyze-workflow")
        assert len(bundle.gate_failures) == 1
        assert bundle.gate_failures[0].gate_id == "G-003"

    def test_diagnostics_collector_record_exit_code(self):
        """record_exit_code() stores the exit code."""
        collector = DiagnosticsCollector()
        collector.record_exit_code(1)
        bundle = collector.build_bundle()
        assert bundle.exit_code == 1

    def test_diagnostics_collector_record_missing_artifact(self):
        """record_missing_artifact() stores path in missing_artifacts list."""
        collector = DiagnosticsCollector()
        collector.record_missing_artifact("/workdir/analyze-workflow.md")
        bundle = collector.build_bundle()
        assert "/workdir/analyze-workflow.md" in bundle.missing_artifacts

    def test_diagnostics_collector_set_resume_guidance(self):
        """set_resume_guidance() stores guidance string."""
        collector = DiagnosticsCollector()
        collector.set_resume_guidance("superclaude portify --start panel-review")
        bundle = collector.build_bundle()
        assert "panel-review" in bundle.resume_guidance

    def test_diagnostics_collector_multiple_gate_failures(self):
        """Multiple gate failures are all recorded."""
        collector = DiagnosticsCollector()
        for i in range(3):
            collector.record_gate_failure(
                GateFailure(
                    gate_id=f"G-00{i}",
                    check_name="test_check",
                    diagnostic=f"failure {i}",
                    artifact_path="/workdir/out.md",
                )
            )
        bundle = collector.build_bundle()
        assert len(bundle.gate_failures) == 3

    def test_diagnostics_collector_g003_shows_missing_section(self):
        """Gate failure from G-003 shows missing section name in diagnostic message."""
        collector = DiagnosticsCollector()
        failure = GateFailure(
            gate_id="G-003",
            check_name="has_required_analysis_sections",
            diagnostic="Missing required analysis sections: ['Source Components']",
            artifact_path="/workdir/analyze-workflow.md",
            tier="STRICT",
        )
        collector.record_gate_failure(failure)
        bundle = collector.build_bundle(step_id="analyze-workflow")
        assert "Source Components" in bundle.gate_failures[0].diagnostic

    def test_diagnostics_collector_initial_state_empty(self):
        """Freshly constructed collector produces empty bundle."""
        collector = DiagnosticsCollector()
        bundle = collector.build_bundle()
        assert bundle.gate_failures == []
        assert bundle.exit_code is None
        assert bundle.missing_artifacts == []
        assert bundle.resume_guidance == ""


# ---------------------------------------------------------------------------
# T09.03 acceptance criteria: diagnostics_emit
# ---------------------------------------------------------------------------


class TestDiagnosticsEmit:
    """emit_diagnostics() writes diagnostics.md to workdir.

    Validation command: uv run pytest tests/ -k "diagnostics_emit"
    """

    def test_diagnostics_emit_creates_file(self, tmp_path):
        """emit_diagnostics() creates diagnostics.md in workdir."""
        collector = DiagnosticsCollector()
        path = collector.emit_diagnostics(tmp_path, step_id="panel-review")
        assert path.name == "diagnostics.md"
        assert path.exists()

    def test_diagnostics_emit_contains_step_id(self, tmp_path):
        """diagnostics.md contains the step_id."""
        collector = DiagnosticsCollector()
        path = collector.emit_diagnostics(tmp_path, step_id="analyze-workflow")
        content = path.read_text()
        assert "analyze-workflow" in content

    def test_diagnostics_emit_contains_exit_code(self, tmp_path):
        """diagnostics.md contains the recorded exit code."""
        collector = DiagnosticsCollector()
        collector.record_exit_code(1)
        path = collector.emit_diagnostics(tmp_path, step_id="synthesize-spec")
        content = path.read_text()
        assert "1" in content

    def test_diagnostics_emit_contains_gate_failure(self, tmp_path):
        """diagnostics.md contains gate failure details."""
        collector = DiagnosticsCollector()
        collector.record_gate_failure(
            GateFailure(
                gate_id="G-003",
                check_name="has_required_analysis_sections",
                diagnostic="Missing sections: ['Step Graph']",
                artifact_path="/workdir/analyze-workflow.md",
                tier="STRICT",
            )
        )
        path = collector.emit_diagnostics(tmp_path, step_id="analyze-workflow")
        content = path.read_text()
        assert "G-003" in content
        assert "Step Graph" in content

    def test_diagnostics_emit_contains_missing_artifacts(self, tmp_path):
        """diagnostics.md contains missing artifact paths."""
        collector = DiagnosticsCollector()
        collector.record_missing_artifact("/workdir/panel-report.md")
        path = collector.emit_diagnostics(tmp_path)
        content = path.read_text()
        assert "panel-report.md" in content

    def test_diagnostics_emit_contains_resume_guidance(self, tmp_path):
        """diagnostics.md contains resume guidance."""
        collector = DiagnosticsCollector()
        collector.set_resume_guidance("superclaude portify --start panel-review")
        path = collector.emit_diagnostics(tmp_path)
        content = path.read_text()
        assert "panel-review" in content

    def test_diagnostics_emit_all_collected_fields(self, tmp_path):
        """diagnostics.md mirrors all collected fields."""
        collector = DiagnosticsCollector()
        collector.record_gate_failure(
            GateFailure(
                gate_id="G-010",
                check_name="has_zero_placeholders",
                diagnostic="Placeholder sentinel found: {{SC_PLACEHOLDER:missing}}",
                artifact_path="/workdir/portify-release-spec.md",
                tier="STRICT",
            )
        )
        collector.record_exit_code(2)
        collector.record_missing_artifact("/workdir/release-spec.md")
        collector.set_resume_guidance("superclaude portify --start synthesize-spec")

        path = collector.emit_diagnostics(tmp_path, step_id="synthesize-spec")
        content = path.read_text()
        assert "G-010" in content
        assert "2" in content
        assert "release-spec.md" in content
        assert "synthesize-spec" in content

    def test_diagnostics_emit_creates_workdir_if_missing(self, tmp_path):
        """emit_diagnostics() creates workdir if it does not exist."""
        new_workdir = tmp_path / "new" / "workdir"
        assert not new_workdir.exists()
        collector = DiagnosticsCollector()
        path = collector.emit_diagnostics(new_workdir)
        assert path.exists()
