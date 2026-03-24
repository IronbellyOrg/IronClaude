"""Tests for TUI integration with per-task execution path."""

from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, call

import pytest

from superclaude.cli.sprint.executor import execute_phase_tasks
from superclaude.cli.sprint.models import (
    MonitorState,
    Phase,
    SprintConfig,
    SprintResult,
    TaskEntry,
    TaskStatus,
    TurnLedger,
)


def _make_config(tmp_path: Path) -> SprintConfig:
    """Create a minimal SprintConfig for testing."""
    pf = tmp_path / "phase-1-tasklist.md"
    pf.write_text("# Phase 1\n")
    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n")
    return SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=[Phase(number=1, file=pf, name="Phase 1")],
        start_phase=1,
        end_phase=1,
        max_turns=5,
        wiring_gate_mode="off",
        wiring_gate_scope="none",
    )


def _make_tasks(count: int = 3) -> list[TaskEntry]:
    """Create N dummy task entries."""
    return [
        TaskEntry(
            task_id=f"T01.{i:02d}",
            title=f"Task {i}",
            description=f"Description {i}",
        )
        for i in range(1, count + 1)
    ]


class TestTUITaskUpdates:
    """Verify that execute_phase_tasks() calls tui.update() per task."""

    def test_update_called_twice_per_task(self, tmp_path):
        """TUI.update() should be called before and after each task."""
        config = _make_config(tmp_path)
        tasks = _make_tasks(3)
        phase = config.phases[0]
        mock_tui = MagicMock()
        mock_result = MagicMock(spec=SprintResult)

        def factory(task, cfg, ph):
            return (0, 5, 100)  # exit_code, turns, bytes

        results, remaining, gates = execute_phase_tasks(
            tasks=tasks,
            config=config,
            phase=phase,
            _subprocess_factory=factory,
            tui=mock_tui,
            sprint_result=mock_result,
        )

        # 2 calls per task (before + after) = 6 total for 3 tasks
        assert mock_tui.update.call_count == 2 * len(tasks)

    def test_last_task_id_set_correctly(self, tmp_path):
        """MonitorState passed to tui.update() should have last_task_id set."""
        config = _make_config(tmp_path)
        tasks = _make_tasks(2)
        phase = config.phases[0]
        mock_tui = MagicMock()
        mock_result = MagicMock(spec=SprintResult)

        def factory(task, cfg, ph):
            return (0, 5, 100)

        execute_phase_tasks(
            tasks=tasks,
            config=config,
            phase=phase,
            _subprocess_factory=factory,
            tui=mock_tui,
            sprint_result=mock_result,
        )

        # Check that each call's MonitorState has a task ID
        for call_args in mock_tui.update.call_args_list:
            monitor_state = call_args[0][1]  # second positional arg
            assert isinstance(monitor_state, MonitorState)
            assert monitor_state.last_task_id.startswith("T01.")

    def test_no_tui_no_error(self, tmp_path):
        """When tui=None (default), no errors occur."""
        config = _make_config(tmp_path)
        tasks = _make_tasks(2)
        phase = config.phases[0]

        def factory(task, cfg, ph):
            return (0, 5, 100)

        results, remaining, gates = execute_phase_tasks(
            tasks=tasks,
            config=config,
            phase=phase,
            _subprocess_factory=factory,
            # tui not passed — defaults to None
        )

        assert len(results) == 2
        assert all(r.status == TaskStatus.PASS for r in results)

    def test_events_received_increments(self, tmp_path):
        """events_received should be i before launch, i+1 after."""
        config = _make_config(tmp_path)
        tasks = _make_tasks(3)
        phase = config.phases[0]
        mock_tui = MagicMock()
        mock_result = MagicMock(spec=SprintResult)

        def factory(task, cfg, ph):
            return (0, 5, 100)

        execute_phase_tasks(
            tasks=tasks,
            config=config,
            phase=phase,
            _subprocess_factory=factory,
            tui=mock_tui,
            sprint_result=mock_result,
        )

        events = [
            call_args[0][1].events_received
            for call_args in mock_tui.update.call_args_list
        ]
        # Expected: [0, 1, 1, 2, 2, 3] — (before task 0, after task 0, before task 1, ...)
        assert events == [0, 1, 1, 2, 2, 3]
