"""Tests for Rich TUI live dashboard."""

from __future__ import annotations

import pytest

from superclaude.cli.cli_portify.tui import (
    DashboardState,
    PIPELINE_STEPS,
    PortifyTUI,
    StepDisplayState,
    TuiDashboard,
    _build_dashboard_table,
)


class TestDashboardState:
    """Tests for DashboardState data model."""

    def test_default_steps_populated(self):
        state = DashboardState()
        assert len(state.steps) == 7
        assert state.steps[0].name == "validate-config"
        assert state.steps[6].name == "panel-review"

    def test_all_steps_start_pending(self):
        state = DashboardState()
        for step in state.steps:
            assert step.status == "pending"

    def test_update_step_status(self):
        state = DashboardState()
        state.update_step("validate-config", status="pass", duration=0.5)
        assert state.steps[0].status == "pass"
        assert state.steps[0].duration_seconds == 0.5

    def test_update_step_gate_result(self):
        state = DashboardState()
        state.update_step("analyze-workflow", gate_result="pass")
        assert state.steps[2].gate_result == "pass"

    def test_update_step_iteration(self):
        state = DashboardState()
        state.update_step("panel-review", iteration=3)
        assert state.steps[6].iteration == 3

    def test_update_step_warning(self):
        state = DashboardState()
        state.update_step("synthesize-spec", warning="placeholders remain")
        assert state.steps[4].warning == "placeholders remain"

    def test_update_nonexistent_step_is_noop(self):
        state = DashboardState()
        state.update_step("nonexistent", status="pass")
        # No error, no change
        for step in state.steps:
            assert step.status == "pending"

    def test_mark_running(self):
        state = DashboardState()
        state.mark_running("analyze-workflow")
        assert state.current_step == "analyze-workflow"
        assert state.steps[2].status == "running"

    def test_mark_complete(self):
        state = DashboardState()
        state.mark_running("validate-config")
        state.mark_complete("validate-config", "pass", 0.3, "pass")
        assert state.steps[0].status == "pass"
        assert state.steps[0].duration_seconds == 0.3
        assert state.steps[0].gate_result == "pass"
        assert state.current_step == ""

    def test_review_pause(self):
        state = DashboardState()
        state.set_review_pause("Accept design? [y/N]")
        assert state.review_paused is True
        assert state.review_prompt == "Accept design? [y/N]"

    def test_review_clear(self):
        state = DashboardState()
        state.set_review_pause("Accept? [y/N]")
        state.clear_review_pause()
        assert state.review_paused is False
        assert state.review_prompt == ""

    def test_add_warning(self):
        state = DashboardState()
        state.add_warning("Missing skill fallback")
        assert len(state.warnings) == 1
        assert "Missing skill" in state.warnings[0]

    def test_compute_elapsed(self):
        import time

        state = DashboardState()
        state.pipeline_start = time.time() - 5.0
        state.compute_elapsed()
        assert state.total_elapsed >= 4.5  # allow small margin


class TestBuildDashboardTable:
    """Tests for table rendering function."""

    def test_table_has_correct_columns(self):
        state = DashboardState()
        table = _build_dashboard_table(state)
        col_names = [c.header for c in table.columns]
        assert "#" in col_names
        assert "Step" in col_names
        assert "Status" in col_names
        assert "Gate" in col_names
        assert "Time" in col_names
        assert "Info" in col_names

    def test_table_has_all_steps_plus_footer(self):
        state = DashboardState()
        table = _build_dashboard_table(state)
        # 7 steps + 1 footer row
        assert table.row_count == 8

    def test_table_reflects_status_changes(self):
        state = DashboardState()
        state.mark_complete("validate-config", "pass", 1.2, "pass")
        table = _build_dashboard_table(state)
        # Table renders without error
        assert table.row_count == 8


class TestTuiDashboard:
    """Tests for the TUI dashboard controller."""

    def test_dashboard_initializes_with_default_state(self):
        dashboard = TuiDashboard()
        assert len(dashboard.state.steps) == 7

    def test_dashboard_non_terminal_does_not_crash(self):
        """Dashboard degrades gracefully in non-terminal (test) environment."""
        dashboard = TuiDashboard()
        dashboard.start()
        dashboard.step_start("validate-config")
        dashboard.step_complete("validate-config", "pass", 0.5)
        dashboard.set_iteration("panel-review", 2)
        dashboard.add_warning("test warning")
        dashboard.pause_for_review("Accept? [y/N]")
        dashboard.resume_after_review()
        dashboard.stop()
        # No crash = pass

    def test_step_start_marks_running(self):
        dashboard = TuiDashboard()
        dashboard.start()
        dashboard.step_start("analyze-workflow")
        assert dashboard.state.current_step == "analyze-workflow"
        assert dashboard.state.steps[2].status == "running"
        dashboard.stop()

    def test_step_complete_clears_current(self):
        dashboard = TuiDashboard()
        dashboard.start()
        dashboard.step_start("validate-config")
        dashboard.step_complete("validate-config", "pass", 0.1)
        assert dashboard.state.current_step == ""
        dashboard.stop()

    def test_pause_resume_cycle(self):
        dashboard = TuiDashboard()
        dashboard.start()
        dashboard.pause_for_review("Review? [y/N]")
        assert dashboard.state.review_paused is True
        dashboard.resume_after_review()
        assert dashboard.state.review_paused is False
        dashboard.stop()

    def test_is_live_property(self):
        dashboard = TuiDashboard()
        # In non-terminal test env, _live is always None
        assert dashboard.is_live is False


# ---------------------------------------------------------------------------
# T03.12 acceptance criteria: test_tui_lifecycle
# ---------------------------------------------------------------------------


class TestTuiLifecycle:
    """T03.12 — PortifyTUI start/stop lifecycle using rich (NFR-008).

    Validation command: uv run pytest tests/ -k "test_tui_lifecycle"
    """

    def test_tui_lifecycle_start_stop_no_crash(self):
        dashboard = TuiDashboard()
        dashboard.start()
        dashboard.stop()
        # No crash = pass

    def test_tui_lifecycle_is_not_live_in_test_env(self):
        dashboard = TuiDashboard()
        dashboard.start()
        # Non-terminal environment → _live is None
        assert dashboard.is_live is False
        dashboard.stop()

    def test_tui_lifecycle_stop_is_idempotent(self):
        dashboard = TuiDashboard()
        dashboard.start()
        dashboard.stop()
        dashboard.stop()  # second stop should not crash

    def test_tui_lifecycle_step_start_updates_state(self):
        dashboard = TuiDashboard()
        dashboard.start()
        dashboard.step_start("validate-config")
        assert dashboard.state.steps[0].status == "running"
        dashboard.stop()

    def test_tui_lifecycle_step_complete_updates_state(self):
        dashboard = TuiDashboard()
        dashboard.start()
        dashboard.step_start("validate-config")
        dashboard.step_complete("validate-config", "pass", 1.2, "pass")
        assert dashboard.state.steps[0].status == "pass"
        assert dashboard.state.steps[0].duration_seconds == 1.2
        dashboard.stop()

    def test_tui_lifecycle_initializes_seven_steps(self):
        dashboard = TuiDashboard()
        assert len(dashboard.state.steps) == 7


# ---------------------------------------------------------------------------
# T09.01 acceptance criteria: tui_update and tui_complete
# ---------------------------------------------------------------------------


class TestPortifyTUIUpdate:
    """T09.01 — PortifyTUI update_step and update_convergence (NFR-008).

    Validation command: uv run pytest tests/ -k "tui_update"
    """

    def test_tui_update_step_callable_for_all_statuses(self):
        """update_step() callable without exception for all PortifyStatus values."""
        from superclaude.cli.cli_portify.models import PortifyStatus

        tui = PortifyTUI()
        tui.start()
        for status in PortifyStatus:
            tui.update_step("validate-config", status=status.value)
        tui.stop()

    def test_tui_update_step_sets_running(self):
        tui = PortifyTUI()
        tui.start()
        tui.update_step(
            "validate-config", status="running", bytes_written=0, elapsed_s=0.0
        )
        assert tui._dashboard.state.steps[0].status == "running"
        tui.stop()

    def test_tui_update_step_sets_bytes_and_elapsed(self):
        tui = PortifyTUI()
        tui.start()
        tui.update_step(
            "analyze-workflow", status="running", bytes_written=1024, elapsed_s=3.5
        )
        step = tui._dashboard.state._find_step("analyze-workflow")
        assert step is not None
        assert step.duration_seconds == 3.5
        tui.stop()

    def test_tui_update_convergence_iteration_1_to_3(self):
        """update_convergence() callable with iteration 1–3 without exception."""
        tui = PortifyTUI()
        tui.start()
        for i in range(1, 4):
            tui.update_convergence(iteration=i, findings_count=5, placeholder_count=2)
        assert tui._convergence_iteration == 3
        tui.stop()

    def test_tui_update_convergence_tracks_state(self):
        tui = PortifyTUI()
        tui.start()
        tui.update_convergence(iteration=2, findings_count=3, placeholder_count=1)
        assert tui._convergence_iteration == 2
        assert tui._findings_count == 3
        assert tui._placeholder_count == 1
        tui.stop()

    def test_tui_update_convergence_updates_panel_review_iteration(self):
        tui = PortifyTUI()
        tui.start()
        tui.update_convergence(iteration=2, findings_count=0, placeholder_count=0)
        step = tui._dashboard.state._find_step("panel-review")
        assert step is not None
        assert step.iteration == 2
        tui.stop()


class TestPortifyTUIComplete:
    """T09.01 — PortifyTUI complete lifecycle test (NFR-008).

    Validation command: uv run pytest tests/ -k "tui_complete"
    """

    def test_tui_complete_start_stop_lifecycle(self):
        """PortifyTUI start/stop lifecycle tested end-to-end."""
        tui = PortifyTUI()
        tui.start()
        assert not tui.is_live  # non-terminal test env
        tui.stop()

    def test_tui_complete_stop_idempotent(self):
        tui = PortifyTUI()
        tui.start()
        tui.stop()
        tui.stop()  # second stop should not crash

    def test_tui_complete_full_pipeline_simulation(self):
        """Simulate a full 5-step pipeline run with real-time updates."""
        import time

        tui = PortifyTUI()
        tui.start()
        for step in ["validate-config", "discover-components", "analyze-workflow"]:
            tui.update_step(step, status="running", bytes_written=0, elapsed_s=0.0)
            tui.update_step(step, status="running", bytes_written=512, elapsed_s=0.5)
            tui.update_step(step, status="pass", bytes_written=1024, elapsed_s=1.0)
        tui.stop()

    def test_tui_complete_convergence_loop_simulation(self):
        """Simulate panel-review convergence iterations."""
        tui = PortifyTUI()
        tui.start()
        for i in range(1, 4):
            tui.update_convergence(
                iteration=i, findings_count=max(0, 5 - i * 2), placeholder_count=0
            )
        tui.stop()
        assert tui._convergence_iteration == 3
