"""Contract tests for GateKPIReport ensuring spec fields, computed properties,
and report formatting remain stable across releases.

Covers:
- Presence of T10/R6 wiring KPI attributes
- wiring_net_cost computed property
- format_report() output includes wiring-related labels
- format_report() documents key field names in output
"""

from superclaude.cli.sprint.kpi import GateKPIReport


class TestGateKPIReportContract:
    """Verify the GateKPIReport public contract stays intact."""

    def test_kpi_report_has_all_spec_fields(self):
        """GateKPIReport must expose wiring_analyses_run,
        wiring_remediations_attempted, and wiring_net_cost."""
        report = GateKPIReport()

        assert hasattr(report, "wiring_analyses_run"), (
            "Missing attribute: wiring_analyses_run"
        )
        assert hasattr(report, "wiring_remediations_attempted"), (
            "Missing attribute: wiring_remediations_attempted"
        )
        assert hasattr(report, "wiring_net_cost"), (
            "Missing attribute: wiring_net_cost (computed property)"
        )

    def test_kpi_net_cost_computed(self):
        """wiring_net_cost must equal wiring_turns_used - wiring_turns_credited."""
        report = GateKPIReport(
            wiring_turns_used=10,
            wiring_turns_credited=3,
        )

        assert report.wiring_net_cost == 7, (
            f"Expected net cost 7, got {report.wiring_net_cost}"
        )

    def test_kpi_format_report_includes_new_fields(self):
        """format_report() output must contain labels for wiring KPI fields."""
        report = GateKPIReport(
            wiring_analyses_run=5,
            wiring_remediations_attempted=2,
            wiring_turns_used=8,
            wiring_turns_credited=1,
            wiring_findings_total=3,
        )
        output = report.format_report()

        required_labels = [
            "Analyses run",
            "Remediations attempted",
            "Net cost",
            "Turns used",
            "Turns credited",
        ]
        for label in required_labels:
            assert label in output, (
                f"format_report() missing label '{label}'"
            )

    def test_frontmatter_fields_documented(self):
        """format_report() output must reference the key wiring field names
        so consumers can parse or verify them."""
        report = GateKPIReport(
            wiring_analyses_run=1,
            wiring_remediations_attempted=1,
            wiring_turns_used=4,
            wiring_turns_credited=2,
            wiring_findings_total=1,
            files_skipped=0,
            whitelist_entries_applied=0,
        )
        output = report.format_report()

        # The formatted report must contain a Wiring Gate section with these
        # key data points so downstream tooling can locate them.
        assert "Wiring Gate" in output, (
            "format_report() must include a 'Wiring Gate' section header"
        )
        # Verify numeric values appear in the output (not just labels)
        assert "4" in output, "Turns used value missing from output"
        assert "2" in output, "Turns credited value missing from output"
        assert "1" in output, "Analyses run value missing from output"
