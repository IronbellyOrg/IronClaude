"""Tests for Portify monitoring: timing capture and the OutputMonitor metrics.

Covers:
- All 7 failure types exist (live FailureClassification)
- Timing capture records per-phase and per-step durations
- OutputMonitor eight-field metrics, stall, growth, convergence, findings,
  placeholders

C01 (cleanup-debt-reduction): the disconnected EventRecord/EventLogger,
classify_failure and generate_diagnostic_report helpers had no production
caller. Their requirement-bearing assertions now live at the real owners
(ExecutionLog: test_logging.py; DiagnosticsCollector: test_diagnostics.py;
production dispatch: test_executor.py). Helper-only mechanics tests (event
dict keys, test-local signal strings, report rendering/counts, and the
user-rejection-over-timeout ordering that existed only inside
classify_failure) were retired with them.
"""

from __future__ import annotations

import time

from superclaude.cli.cli_portify.models import FailureClassification
from superclaude.cli.cli_portify.monitor import TimingCapture


def test_all_seven_types_covered():
    """Verify all 7 FailureClassification values exist."""
    expected = {
        "timeout",
        "missing_artifact",
        "malformed_frontmatter",
        "gate_failure",
        "user_rejection",
        "budget_exhaustion",
        "partial_artifact",
    }
    actual = {fc.value for fc in FailureClassification}
    assert actual == expected


class TestTimingCapture:
    """Timing capture records per-phase and per-step durations."""

    def test_step_timing(self):
        tc = TimingCapture()
        tc.start_step("analyze-workflow", phase=2)
        time.sleep(0.01)
        tc.end_step("analyze-workflow")
        st = tc.get_step_timing("analyze-workflow")
        assert st is not None
        assert st.duration_seconds > 0

    def test_phase_timing(self):
        tc = TimingCapture()
        tc.start_step("s1", phase=1)
        tc.end_step("s1")
        tc.start_step("s2", phase=1)
        tc.end_step("s2")
        pt = tc.get_phase_timing(1)
        assert pt is not None
        assert len(pt.step_timings) == 2

    def test_pipeline_total_duration(self):
        tc = TimingCapture()
        tc.start_pipeline()
        time.sleep(0.01)
        tc.end_pipeline()
        assert tc.total_duration > 0

    def test_step_timings_list(self):
        tc = TimingCapture()
        tc.start_step("a", phase=1)
        tc.end_step("a")
        tc.start_step("b", phase=2)
        tc.end_step("b")
        assert len(tc.step_timings) == 2

    def test_unknown_step_returns_none(self):
        tc = TimingCapture()
        assert tc.get_step_timing("nonexistent") is None


# ---------------------------------------------------------------------------
# T03.11 acceptance criteria: test_output_monitor
# ---------------------------------------------------------------------------


class TestOutputMonitor:
    """T03.11 — OutputMonitor tracks all 8 metrics and detects stalls.

    Validation command: uv run pytest tests/ -k "test_output_monitor"
    """

    def test_output_monitor_instantiates(self):
        from superclaude.cli.cli_portify.monitor import OutputMonitor

        mon = OutputMonitor()
        assert mon.state.output_bytes == 0
        assert mon.state.growth_rate_bps == 0.0

    def test_output_monitor_tracks_output_bytes(self):
        from superclaude.cli.cli_portify.monitor import OutputMonitor

        mon = OutputMonitor()
        mon.update(1024)
        assert mon.state.output_bytes == 1024

    def test_output_monitor_tracks_events(self):
        from superclaude.cli.cli_portify.monitor import OutputMonitor

        mon = OutputMonitor()
        mon.update(100)
        mon.update(200)
        assert mon.state.events == 2

    def test_output_monitor_tracks_line_count(self):
        from superclaude.cli.cli_portify.monitor import OutputMonitor

        mon = OutputMonitor()
        mon.update(100, new_lines=5)
        mon.update(200, new_lines=3)
        assert mon.state.line_count == 8

    def test_output_monitor_stall_detection_accumulates(self):
        import time

        from superclaude.cli.cli_portify.monitor import OutputMonitor

        mon = OutputMonitor(
            stall_threshold_bps=1000.0,  # High threshold → immediate stall
            stall_timeout_seconds=0.0,  # Zero timeout → stall accumulates immediately
        )
        # First call establishes baseline
        mon.update(0)
        # Second call with no byte growth triggers stall accumulation
        time.sleep(0.01)
        mon.update(0)
        assert mon.state.stall_seconds > 0

    def test_output_monitor_has_all_eight_fields(self):
        from superclaude.cli.cli_portify.models import MonitorState

        fields = set(MonitorState.__dataclass_fields__.keys())
        expected = {
            "output_bytes",
            "growth_rate_bps",
            "stall_seconds",
            "events",
            "line_count",
            "convergence_iteration",
            "findings_count",
            "placeholder_count",
        }
        assert expected == fields


# ---------------------------------------------------------------------------
# T09.02 acceptance criteria: monitor_complete and convergence_tracking
# ---------------------------------------------------------------------------


class TestOutputMonitorComplete:
    """T09.02 — OutputMonitor has all 8 NFR-009 fields and update methods.

    Validation command: uv run pytest tests/ -k "monitor_complete"
    """

    def test_monitor_complete_all_eight_fields_present(self):
        """All 8 NFR-009 fields present in OutputMonitor.state."""
        from superclaude.cli.cli_portify.models import MonitorState
        from superclaude.cli.cli_portify.monitor import OutputMonitor

        OutputMonitor()  # was: mon = OutputMonitor(); mon was unused
        expected = {
            "output_bytes",
            "growth_rate_bps",
            "stall_seconds",
            "events",
            "line_count",
            "convergence_iteration",
            "findings_count",
            "placeholder_count",
        }
        assert set(MonitorState.__dataclass_fields__.keys()) == expected

    def test_monitor_complete_set_convergence_iteration(self):
        """set_convergence_iteration(2) updates monitor.convergence_iteration to 2."""
        from superclaude.cli.cli_portify.monitor import OutputMonitor

        mon = OutputMonitor()
        mon.set_convergence_iteration(2)
        assert mon.state.convergence_iteration == 2

    def test_monitor_complete_increment_findings(self):
        """increment_findings() accumulates count."""
        from superclaude.cli.cli_portify.monitor import OutputMonitor

        mon = OutputMonitor()
        mon.increment_findings(3)
        mon.increment_findings(2)
        assert mon.state.findings_count == 5

    def test_monitor_complete_set_placeholder_count(self):
        """set_placeholder_count(0) reflects in monitor state."""
        from superclaude.cli.cli_portify.monitor import OutputMonitor

        mon = OutputMonitor()
        mon.set_placeholder_count(7)
        assert mon.state.placeholder_count == 7
        mon.set_placeholder_count(0)
        assert mon.state.placeholder_count == 0

    def test_monitor_complete_initial_state_all_zero(self):
        """All 8 fields initialize to zero."""
        from superclaude.cli.cli_portify.monitor import OutputMonitor

        mon = OutputMonitor()
        assert mon.state.output_bytes == 0
        assert mon.state.growth_rate_bps == 0.0
        assert mon.state.stall_seconds == 0.0
        assert mon.state.events == 0
        assert mon.state.line_count == 0
        assert mon.state.convergence_iteration == 0
        assert mon.state.findings_count == 0
        assert mon.state.placeholder_count == 0


class TestConvergenceTracking:
    """T09.02 — OutputMonitor convergence tracking integration.

    Validation command: uv run pytest tests/ -k "convergence_tracking"
    """

    def test_convergence_tracking_iteration_sequence(self):
        """set_convergence_iteration() advances through 1, 2, 3."""
        from superclaude.cli.cli_portify.monitor import OutputMonitor

        mon = OutputMonitor()
        for i in range(1, 4):
            mon.set_convergence_iteration(i)
            assert mon.state.convergence_iteration == i

    def test_convergence_tracking_findings_accumulate(self):
        """increment_findings() called multiple times accumulates."""
        from superclaude.cli.cli_portify.monitor import OutputMonitor

        mon = OutputMonitor()
        mon.increment_findings(5)
        mon.increment_findings(3)
        assert mon.state.findings_count == 8

    def test_convergence_tracking_placeholder_scan_result(self):
        """set_placeholder_count() reflects scan result correctly."""
        from superclaude.cli.cli_portify.monitor import OutputMonitor

        mon = OutputMonitor()
        mon.set_placeholder_count(12)
        assert mon.state.placeholder_count == 12
        # After resolution, should drop to 0
        mon.set_placeholder_count(0)
        assert mon.state.placeholder_count == 0

    def test_convergence_tracking_combined_state(self):
        """All convergence state fields updated in concert."""
        from superclaude.cli.cli_portify.monitor import OutputMonitor

        mon = OutputMonitor()
        mon.set_convergence_iteration(2)
        mon.increment_findings(4)
        mon.set_placeholder_count(1)
        assert mon.state.convergence_iteration == 2
        assert mon.state.findings_count == 4
        assert mon.state.placeholder_count == 1
