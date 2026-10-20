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

import re

from superclaude.cli.cli_portify.diagnostics import (
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


# ---------------------------------------------------------------------------
# Live report contract (C01 migration A-18, FR-01/FR-11): the diagnostics.md
# title, empty-section text and failure/exit/missing-artifact/resume fields
# are owned by DiagnosticsCollector, not the monitor-helper report.
# Expected text is characterized from current diagnostics.py output.
# ---------------------------------------------------------------------------

_TITLE = "# CLI Portify — Pipeline Failure Diagnostics"
_GENERATED_RE = re.compile(r"^Generated: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+00:00$")


def _body_after_generated(content: str) -> list[str]:
    """Split the report and return lines after the title/Generated header."""
    lines = content.split("\n")
    assert lines[0] == _TITLE
    assert lines[1] == ""
    assert _GENERATED_RE.match(lines[2]), lines[2]
    assert lines[3] == ""
    return lines[4:]


class TestDiagnosticsReportContract:
    """Exact diagnostics.md structure written by the live collector."""

    def test_diagnostics_report_empty_sections_text(self, tmp_path):
        """No failure data: title, UTC timestamp, three sections with empty-section text."""
        content = DiagnosticsCollector().emit_diagnostics(tmp_path).read_text()
        assert _body_after_generated(content) == [
            "## Gate Failures",
            "",
            "_None recorded._",
            "",
            "## Missing Artifacts",
            "",
            "_None recorded._",
            "",
            "## Resume Guidance",
            "",
            "_No resume command available for this step._",
            "",
        ]
        assert "**Failed Step:**" not in content
        assert "**Exit Code:**" not in content

    def test_diagnostics_report_all_failure_fields(self, tmp_path):
        """Failed step, exit code, gate failure, missing artifacts and resume guidance render exactly."""
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
        collector.record_exit_code(1)
        collector.record_missing_artifact("/workdir/analyze-workflow.md")
        collector.record_missing_artifact("/workdir/portify-analysis.md")
        collector.set_resume_guidance("superclaude portify --start analyze-workflow")

        path = collector.emit_diagnostics(tmp_path, step_id="analyze-workflow")
        assert path == tmp_path / "diagnostics.md"
        assert _body_after_generated(path.read_text(encoding="utf-8")) == [
            "**Failed Step:** `analyze-workflow`",
            "",
            "**Exit Code:** 1",
            "",
            "## Gate Failures",
            "",
            "### G-003 — has_required_analysis_sections",
            "- **Tier:** STRICT",
            "- **Artifact:** `/workdir/analyze-workflow.md`",
            "- **Reason:** Missing sections: ['Step Graph']",
            "",
            "## Missing Artifacts",
            "",
            "- `/workdir/analyze-workflow.md`",
            "- `/workdir/portify-analysis.md`",
            "",
            "## Resume Guidance",
            "",
            "```",
            "superclaude portify --start analyze-workflow",
            "```",
            "",
        ]

    def test_diagnostics_report_exit_code_zero_is_rendered(self, tmp_path):
        """Exit code 0 is recorded and rendered (only None is omitted)."""
        collector = DiagnosticsCollector()
        collector.record_exit_code(0)
        content = collector.emit_diagnostics(tmp_path).read_text()
        assert "**Exit Code:** 0" in content.split("\n")

    def test_diagnostics_report_last_exit_code_and_guidance_win(self, tmp_path):
        """Repeated exit code / resume guidance overwrite; missing artifacts accumulate in order."""
        collector = DiagnosticsCollector()
        collector.record_exit_code(124)
        collector.record_exit_code(2)
        collector.set_resume_guidance("superclaude portify --start brainstorm-gaps")
        collector.set_resume_guidance("superclaude portify --start panel-review")
        collector.record_missing_artifact("/w/a.md")
        collector.record_missing_artifact("/w/a.md")

        bundle = collector.build_bundle(step_id="panel-review")
        assert bundle.exit_code == 2
        assert bundle.resume_guidance == "superclaude portify --start panel-review"
        assert bundle.missing_artifacts == ["/w/a.md", "/w/a.md"]

        lines = collector.emit_diagnostics(tmp_path).read_text().split("\n")
        assert "**Exit Code:** 2" in lines
        assert "**Exit Code:** 124" not in lines
        assert "superclaude portify --start brainstorm-gaps" not in lines
        assert lines.count("- `/w/a.md`") == 2

    def test_diagnostics_bundle_is_snapshot_copy(self):
        """build_bundle() copies lists; later records do not mutate an earlier bundle."""
        collector = DiagnosticsCollector()
        collector.record_missing_artifact("/w/first.md")
        first = collector.build_bundle()
        first.missing_artifacts.append("/w/injected.md")
        collector.record_missing_artifact("/w/second.md")
        assert first.missing_artifacts == ["/w/first.md", "/w/injected.md"]
        assert collector.build_bundle().missing_artifacts == [
            "/w/first.md",
            "/w/second.md",
        ]

    def test_diagnostics_emit_overwrites_existing_report(self, tmp_path):
        """A second emit replaces diagnostics.md instead of appending."""
        (tmp_path / "diagnostics.md").write_text("stale\n", encoding="utf-8")
        collector = DiagnosticsCollector()
        collector.record_exit_code(3)
        content = collector.emit_diagnostics(tmp_path).read_text()
        assert "stale" not in content
        assert content.startswith(_TITLE + "\n")
