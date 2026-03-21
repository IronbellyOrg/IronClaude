"""Tests for KPI report generation from gate and remediation metrics."""

from pathlib import Path

from superclaude.cli.audit.wiring_gate import WiringFinding, WiringReport
from superclaude.cli.pipeline.trailing_gate import (
    DeferredRemediationLog,
    TrailingGateResult,
)
from superclaude.cli.sprint.kpi import GateKPIReport, build_kpi_report
from superclaude.cli.sprint.models import TurnLedger


def _gate(step_id: str, passed: bool, ms: float) -> TrailingGateResult:
    return TrailingGateResult(
        step_id=step_id,
        passed=passed,
        evaluation_ms=ms,
        failure_reason=None if passed else "test failure",
    )


class TestGateKPIReportProperties:
    """Verify computed properties of the KPI report."""

    def test_empty_report(self):
        r = GateKPIReport()
        assert r.gate_pass_rate == 0.0
        assert r.gate_fail_rate == 0.0
        assert r.remediation_frequency == 0.0
        assert r.conflict_review_rate == 0.0
        assert r.p50_latency_ms == 0.0
        assert r.p95_latency_ms == 0.0

    def test_pass_rate(self):
        r = GateKPIReport(total_gates_evaluated=4, gates_passed=3, gates_failed=1)
        assert r.gate_pass_rate == 0.75
        assert r.gate_fail_rate == 0.25

    def test_remediation_frequency(self):
        r = GateKPIReport(total_gates_evaluated=10, total_remediations=3)
        assert abs(r.remediation_frequency - 0.3) < 0.001

    def test_conflict_review_rate(self):
        r = GateKPIReport(total_conflict_reviews=5, conflicts_detected=2)
        assert abs(r.conflict_review_rate - 0.4) < 0.001

    def test_latency_p50_odd(self):
        r = GateKPIReport(gate_latency_ms=[10.0, 20.0, 30.0, 40.0, 50.0])
        assert r.p50_latency_ms == 30.0

    def test_latency_p50_even(self):
        r = GateKPIReport(gate_latency_ms=[10.0, 20.0, 30.0, 40.0])
        assert r.p50_latency_ms == 25.0

    def test_latency_p95(self):
        r = GateKPIReport(gate_latency_ms=[float(i) for i in range(1, 101)])
        assert r.p95_latency_ms >= 95.0


class TestBuildKPIReport:
    """Verify build_kpi_report aggregates metrics correctly."""

    def test_from_gate_results_all_pass(self):
        results = [_gate(f"T{i}", True, 10.0 * i) for i in range(1, 6)]
        report = build_kpi_report(results)
        assert report.total_gates_evaluated == 5
        assert report.gates_passed == 5
        assert report.gates_failed == 0
        assert report.gate_pass_rate == 1.0

    def test_from_gate_results_mixed(self):
        results = [
            _gate("T1", True, 10.0),
            _gate("T2", False, 20.0),
            _gate("T3", True, 15.0),
            _gate("T4", False, 30.0),
        ]
        report = build_kpi_report(results)
        assert report.total_gates_evaluated == 4
        assert report.gates_passed == 2
        assert report.gates_failed == 2
        assert report.gate_pass_rate == 0.5

    def test_latency_from_gate_results(self):
        results = [
            _gate("T1", True, 10.0),
            _gate("T2", True, 20.0),
            _gate("T3", True, 30.0),
        ]
        report = build_kpi_report(results)
        assert report.p50_latency_ms == 20.0

    def test_with_remediation_log(self):
        results = [_gate("T1", False, 10.0), _gate("T2", False, 20.0)]
        log = DeferredRemediationLog()
        log.append(results[0])
        log.append(results[1])
        log.mark_remediated("T1")

        report = build_kpi_report(results, remediation_log=log)
        assert report.total_remediations == 2
        assert report.remediations_resolved == 1
        assert report.remediations_pending == 1

    def test_with_conflict_reviews(self):
        report = build_kpi_report(
            gate_results=[],
            conflict_reviews_total=10,
            conflicts_detected=3,
        )
        assert report.total_conflict_reviews == 10
        assert report.conflicts_detected == 3
        assert abs(report.conflict_review_rate - 0.3) < 0.001

    def test_empty_inputs(self):
        report = build_kpi_report(gate_results=[])
        assert report.total_gates_evaluated == 0
        assert report.gate_pass_rate == 0.0

    def test_no_remediation_log(self):
        results = [_gate("T1", True, 10.0)]
        report = build_kpi_report(results)
        assert report.total_remediations == 0
        assert report.remediations_resolved == 0
        assert report.remediations_pending == 0


class TestKPIReportFormat:
    """KPI report produces human-readable formatted output."""

    def test_format_report_contains_sections(self):
        report = build_kpi_report(
            gate_results=[_gate("T1", True, 15.0), _gate("T2", False, 25.0)],
            conflict_reviews_total=3,
            conflicts_detected=1,
        )
        text = report.format_report()
        assert "Gate Evaluation" in text
        assert "Remediation" in text
        assert "Conflict Review" in text
        assert "p50" in text
        assert "p95" in text

    def test_format_report_accurate_values(self):
        report = GateKPIReport(
            total_gates_evaluated=10,
            gates_passed=8,
            gates_failed=2,
            gate_latency_ms=[10.0, 20.0, 30.0],
            total_remediations=2,
            remediations_resolved=1,
            remediations_pending=1,
            total_conflict_reviews=5,
            conflicts_detected=2,
        )
        text = report.format_report()
        assert "80.0%" in text  # pass rate
        assert "20.0ms" in text  # p50 latency


def _finding(ftype: str, suppressed: bool = False) -> WiringFinding:
    return WiringFinding(
        finding_type=ftype,
        file_path="src/test.py",
        symbol_name="test_fn",
        line_number=1,
        detail="test finding",
        suppressed=suppressed,
    )


class TestWiringKPIFields:
    """Verify the 6 wiring KPI fields are populated from TurnLedger and WiringReport (SC-015)."""

    def test_wiring_fields_default_zero(self):
        r = GateKPIReport()
        assert r.wiring_findings_total == 0
        assert r.wiring_findings_by_type == {}
        assert r.wiring_turns_used == 0
        assert r.wiring_turns_credited == 0
        assert r.whitelist_entries_applied == 0
        assert r.files_skipped == 0

    def test_build_with_turn_ledger(self):
        ledger = TurnLedger(initial_budget=20, wiring_turns_used=5, wiring_turns_credited=3)
        report = build_kpi_report(gate_results=[], turn_ledger=ledger)
        assert report.wiring_turns_used == 5
        assert report.wiring_turns_credited == 3

    def test_build_with_wiring_report(self):
        wr = WiringReport(
            files_skipped=7,
            unwired_callables=[_finding("unwired_callable"), _finding("unwired_callable")],
            orphan_modules=[_finding("orphan_module")],
            unwired_registries=[],
        )
        report = build_kpi_report(gate_results=[], wiring_report=wr)
        assert report.wiring_findings_total == 3
        assert report.files_skipped == 7
        assert report.wiring_findings_by_type == {
            "unwired_callable": 2,
            "orphan_module": 1,
        }

    def test_whitelist_entries_applied(self):
        wr = WiringReport(
            unwired_callables=[
                _finding("unwired_callable", suppressed=True),
                _finding("unwired_callable", suppressed=False),
            ],
            orphan_modules=[_finding("orphan_module", suppressed=True)],
        )
        report = build_kpi_report(gate_results=[], wiring_report=wr)
        assert report.whitelist_entries_applied == 2

    def test_floor_to_zero_credit(self):
        """R7: credited turns never go negative."""
        ledger = TurnLedger(initial_budget=20, wiring_turns_credited=0)
        report = build_kpi_report(gate_results=[], turn_ledger=ledger)
        assert report.wiring_turns_credited >= 0

    def test_build_with_both_turn_ledger_and_wiring_report(self):
        ledger = TurnLedger(initial_budget=20, wiring_turns_used=4, wiring_turns_credited=2)
        wr = WiringReport(
            files_skipped=3,
            unwired_callables=[_finding("unwired_callable")],
        )
        report = build_kpi_report(gate_results=[], turn_ledger=ledger, wiring_report=wr)
        assert report.wiring_turns_used == 4
        assert report.wiring_turns_credited == 2
        assert report.wiring_findings_total == 1
        assert report.files_skipped == 3

    def test_no_wiring_data_preserves_defaults(self):
        report = build_kpi_report(gate_results=[_gate("T1", True, 10.0)])
        assert report.wiring_findings_total == 0
        assert report.wiring_turns_used == 0

    def test_format_report_includes_wiring_section(self):
        report = GateKPIReport(
            wiring_findings_total=5,
            wiring_turns_used=3,
            wiring_turns_credited=2,
            files_skipped=10,
        )
        text = report.format_report()
        assert "Wiring Gate" in text
        assert "Findings total" in text
        assert "Turns used" in text
