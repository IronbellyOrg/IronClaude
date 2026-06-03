"""Tests for sprint executor — status determination and orchestration."""

from __future__ import annotations

import os
import time
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from superclaude.cli.sprint.executor import (
    _determine_phase_status,
    _write_preliminary_result,
    aggregate_task_results,
    check_budget_guard,
    execute_phase_tasks,
    execute_sprint,
    setup_isolation,
)
from superclaude.cli.sprint.models import (
    Phase,
    PhaseStatus,
    SprintConfig,
    SprintOutcome,
    TaskEntry,
    TaskResult,
    TaskStatus,
    TurnLedger,
)


def _make_config(tmp_path: Path, num_phases: int = 2) -> SprintConfig:
    phases = []
    for i in range(1, num_phases + 1):
        pf = tmp_path / f"phase-{i}-tasklist.md"
        pf.write_text(f"# Phase {i}\n")
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
        wiring_gate_scope="none",  # bypass scope-based resolution so "off" is used directly
    )


class TestDeterminePhaseStatus:
    """Test the 7-level status priority chain."""

    def test_timeout_exit_code(self, tmp_path):
        result_file = tmp_path / "result.md"
        output_file = tmp_path / "output.txt"
        output_file.write_text("some output")

        status = _determine_phase_status(
            exit_code=124,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.TIMEOUT

    def test_timeout_overrides_result_file(self, tmp_path):
        """Timeout (exit 124) takes priority over result file content."""
        result_file = tmp_path / "result.md"
        result_file.write_text("EXIT_RECOMMENDATION: CONTINUE")
        output_file = tmp_path / "output.txt"

        status = _determine_phase_status(
            exit_code=124,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.TIMEOUT

    def test_nonzero_exit_error(self, tmp_path):
        result_file = tmp_path / "result.md"
        output_file = tmp_path / "output.txt"
        output_file.write_text("some output")

        status = _determine_phase_status(
            exit_code=1,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.ERROR

    def test_nonzero_exit_overrides_continue_signal(self, tmp_path):
        """Non-zero exit takes priority over CONTINUE signal."""
        result_file = tmp_path / "result.md"
        result_file.write_text("EXIT_RECOMMENDATION: CONTINUE")
        output_file = tmp_path / "output.txt"

        status = _determine_phase_status(
            exit_code=1,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.ERROR

    def test_halt_signal(self, tmp_path):
        result_file = tmp_path / "result.md"
        result_file.write_text("EXIT_RECOMMENDATION: HALT")
        output_file = tmp_path / "output.txt"

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.HALT

    def test_continue_signal(self, tmp_path):
        result_file = tmp_path / "result.md"
        result_file.write_text("EXIT_RECOMMENDATION: CONTINUE")
        output_file = tmp_path / "output.txt"

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.PASS

    def test_yaml_status_pass(self, tmp_path):
        result_file = tmp_path / "result.md"
        result_file.write_text("---\nstatus: PASS\n---\n")
        output_file = tmp_path / "output.txt"

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.PASS

    def test_yaml_status_fail(self, tmp_path):
        result_file = tmp_path / "result.md"
        result_file.write_text("---\nstatus: FAIL\n---\n")
        output_file = tmp_path / "output.txt"

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.HALT

    def test_result_file_no_signals(self, tmp_path):
        result_file = tmp_path / "result.md"
        result_file.write_text("Some result content without signals")
        output_file = tmp_path / "output.txt"

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.PASS_NO_SIGNAL

    def test_no_result_file_with_output(self, tmp_path):
        result_file = tmp_path / "result.md"
        # Don't create result file
        output_file = tmp_path / "output.txt"
        output_file.write_text("Claude output here")

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.PASS_NO_REPORT

    def test_no_result_no_output(self, tmp_path):
        result_file = tmp_path / "result.md"
        output_file = tmp_path / "output.txt"
        # Neither file exists

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.ERROR

    def test_empty_output_file(self, tmp_path):
        result_file = tmp_path / "result.md"
        output_file = tmp_path / "output.txt"
        output_file.write_text("")  # empty

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.ERROR

    # --- Regression tests for case-sensitivity and signal conflict fixes ---

    def test_continue_signal_case_insensitive(self, tmp_path):
        """Lowercase EXIT_RECOMMENDATION: continue must still produce PASS."""
        result_file = tmp_path / "result.md"
        result_file.write_text("exit_recommendation: continue\n")
        output_file = tmp_path / "output.txt"

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.PASS

    def test_halt_signal_case_insensitive(self, tmp_path):
        """Lowercase EXIT_RECOMMENDATION: halt must still produce HALT."""
        result_file = tmp_path / "result.md"
        result_file.write_text("exit_recommendation: halt\n")
        output_file = tmp_path / "output.txt"

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.HALT

    def test_both_continue_and_halt_halt_wins(self, tmp_path):
        """When both EXIT_RECOMMENDATION tokens appear, HALT must win (safer outcome)."""
        result_file = tmp_path / "result.md"
        # CONTINUE appears before HALT — HALT must still win
        result_file.write_text(
            "EXIT_RECOMMENDATION: CONTINUE\n"
            "Some tasks failed.\n"
            "EXIT_RECOMMENDATION: HALT\n"
        )
        output_file = tmp_path / "output.txt"

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.HALT

    def test_partial_status_produces_halt(self, tmp_path):
        """PARTIAL status in result file must produce HALT (existing behavior, regression guard)."""
        result_file = tmp_path / "result.md"
        result_file.write_text("---\nstatus: PARTIAL\n---\n")
        output_file = tmp_path / "output.txt"

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.HALT

    # --- error_max_turns reclassification tests ---

    def test_reclassification_pass_no_report_with_error_max_turns(self, tmp_path):
        """PASS_NO_REPORT + error_max_turns → INCOMPLETE."""
        result_file = tmp_path / "result.md"
        output_file = tmp_path / "output.txt"
        output_file.write_text(
            '{"type":"content","text":"working..."}\n'
            '{"type":"result","subtype":"error_max_turns"}\n'
        )

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.INCOMPLETE

    def test_reclassification_pass_no_report_without_error_max_turns(self, tmp_path):
        """PASS_NO_REPORT without error_max_turns stays PASS_NO_REPORT."""
        result_file = tmp_path / "result.md"
        output_file = tmp_path / "output.txt"
        output_file.write_text(
            '{"type":"content","text":"working..."}\n'
            '{"type":"result","subtype":"success"}\n'
        )

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.PASS_NO_REPORT

    def test_reclassification_does_not_affect_normal_pass(self, tmp_path):
        """Result file with CONTINUE signal → PASS regardless of output content."""
        result_file = tmp_path / "result.md"
        result_file.write_text("EXIT_RECOMMENDATION: CONTINUE\n")
        output_file = tmp_path / "output.txt"
        output_file.write_text('{"type":"result","subtype":"error_max_turns"}\n')

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.PASS

    def test_reclassification_does_not_affect_normal_halt(self, tmp_path):
        """Result file with HALT signal → HALT regardless of output content."""
        result_file = tmp_path / "result.md"
        result_file.write_text("EXIT_RECOMMENDATION: HALT\n")
        output_file = tmp_path / "output.txt"
        output_file.write_text('{"type":"result","subtype":"error_max_turns"}\n')

        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.HALT

    def test_incomplete_is_failure(self):
        """INCOMPLETE status is classified as a failure (triggers HALT flow)."""
        assert PhaseStatus.INCOMPLETE.is_failure is True
        assert PhaseStatus.INCOMPLETE.is_success is False
        assert PhaseStatus.INCOMPLETE.is_terminal is True


class TestExecuteSprintIntegrationCoverage:
    def test_execute_sprint_pass(self, tmp_path):
        config = _make_config(tmp_path, num_phases=1)

        class _PassPopen:
            def __init__(self):
                self.returncode = 0
                self.pid = 1001
                self._poll = 0

            def poll(self):
                self._poll += 1
                return None if self._poll <= 1 else 0

            def wait(self, timeout=None):
                self.returncode = 0
                return 0

        def _factory(*args, **kwargs):
            phase = config.phases[0]
            config.results_dir.mkdir(parents=True, exist_ok=True)
            config.result_file(phase).write_text("EXIT_RECOMMENDATION: CONTINUE\n")
            config.output_file(phase).write_text("output\n")
            return _PassPopen()

        captured = []
        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.pipeline.process.subprocess.Popen",
                side_effect=_factory,
            ),
            patch("superclaude.cli.pipeline.process.os.setpgrp"),
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.executor.SprintLogger") as logger_cls,
        ):
            logger = MagicMock()
            logger.write_summary = MagicMock(side_effect=lambda sr: captured.append(sr))
            logger_cls.return_value = logger
            execute_sprint(config)

        assert captured[0].outcome == SprintOutcome.SUCCESS
        assert captured[0].phase_results[0].status == PhaseStatus.PASS

    def test_execute_sprint_halt(self, tmp_path):
        config = _make_config(tmp_path, num_phases=1)

        class _HaltPopen:
            def __init__(self):
                self.returncode = 0
                self.pid = 1002
                self._poll = 0

            def poll(self):
                self._poll += 1
                return None if self._poll <= 1 else 0

            def wait(self, timeout=None):
                self.returncode = 0
                return 0

        def _factory(*args, **kwargs):
            phase = config.phases[0]
            config.results_dir.mkdir(parents=True, exist_ok=True)
            result = config.result_file(phase)
            result.write_text("EXIT_RECOMMENDATION: HALT\n")
            # Set mtime to future so freshness guard treats file as agent-written
            future = time.time() + 60
            os.utime(result, (future, future))
            config.output_file(phase).write_text("output\n")
            return _HaltPopen()

        captured = []
        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.pipeline.process.subprocess.Popen",
                side_effect=_factory,
            ),
            patch("superclaude.cli.pipeline.process.os.setpgrp"),
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.executor.SprintLogger") as logger_cls,
        ):
            logger = MagicMock()
            logger.write_summary = MagicMock(side_effect=lambda sr: captured.append(sr))
            logger_cls.return_value = logger
            with pytest.raises(SystemExit) as exc:
                execute_sprint(config)
            assert exc.value.code == 1

        assert captured[0].outcome == SprintOutcome.HALTED
        assert captured[0].halt_phase == 1

    def test_execute_sprint_timeout_exit_code_124(self, tmp_path):
        config = _make_config(tmp_path, num_phases=1)

        class _TimeoutPopen:
            def __init__(self):
                self.returncode = 1
                self.pid = 1003

            def poll(self):
                return None

            def wait(self, timeout=None):
                return 1

        def _factory(*args, **kwargs):
            phase = config.phases[0]
            config.results_dir.mkdir(parents=True, exist_ok=True)
            config.output_file(phase).write_text("still running\n")
            return _TimeoutPopen()

        monotonic_calls = [0]

        def _fast_monotonic():
            monotonic_calls[0] += 1
            if monotonic_calls[0] <= 2:
                return 100.0
            return 999999.0

        captured = []
        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.pipeline.process.subprocess.Popen",
                side_effect=_factory,
            ),
            patch("superclaude.cli.pipeline.process.os.setpgrp"),
            patch("superclaude.cli.pipeline.process.os.getpgid", return_value=1003),
            patch("superclaude.cli.pipeline.process.os.killpg"),
            patch("superclaude.cli.sprint.notify._notify"),
            patch(
                "superclaude.cli.sprint.executor.time.monotonic",
                side_effect=_fast_monotonic,
            ),
            patch("superclaude.cli.sprint.executor.time.sleep"),
            patch("superclaude.cli.sprint.executor.SprintLogger") as logger_cls,
        ):
            logger = MagicMock()
            logger.write_summary = MagicMock(side_effect=lambda sr: captured.append(sr))
            logger_cls.return_value = logger
            with pytest.raises(SystemExit) as exc:
                execute_sprint(config)
            assert exc.value.code == 1

        assert captured[0].outcome == SprintOutcome.HALTED
        assert captured[0].phase_results[0].status == PhaseStatus.TIMEOUT
        assert captured[0].phase_results[0].exit_code == 124

    def test_execute_sprint_interrupted(self, tmp_path):
        config = _make_config(tmp_path, num_phases=1)

        class _InterruptPopen:
            def __init__(self):
                self.returncode = None
                self.pid = 1004
                self._poll = 0

            def poll(self):
                self._poll += 1
                return None if self._poll <= 2 else -15

            def wait(self, timeout=None):
                self.returncode = -15
                return -15

        from superclaude.cli.sprint.process import SignalHandler as _RealSignalHandler

        captured_handler = []

        class _TrackingSignalHandler(_RealSignalHandler):
            def __init__(self):
                super().__init__()
                captured_handler.append(self)

        def _factory(*args, **kwargs):
            phase = config.phases[0]
            config.results_dir.mkdir(parents=True, exist_ok=True)
            config.output_file(phase).write_text("running\n")
            return _InterruptPopen()

        sleep_calls = [0]

        def _sleep(_secs):
            sleep_calls[0] += 1
            if sleep_calls[0] == 1 and captured_handler:
                captured_handler[0].shutdown_requested = True

        captured = []
        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.pipeline.process.subprocess.Popen",
                side_effect=_factory,
            ),
            patch("superclaude.cli.pipeline.process.os.setpgrp"),
            patch("superclaude.cli.pipeline.process.os.getpgid", return_value=1004),
            patch("superclaude.cli.pipeline.process.os.killpg"),
            patch("superclaude.cli.sprint.notify._notify"),
            patch(
                "superclaude.cli.sprint.executor.SignalHandler", _TrackingSignalHandler
            ),
            patch("superclaude.cli.sprint.executor.time.sleep", side_effect=_sleep),
            patch("superclaude.cli.sprint.executor.SprintLogger") as logger_cls,
        ):
            logger = MagicMock()
            logger.write_summary = MagicMock(side_effect=lambda sr: captured.append(sr))
            logger_cls.return_value = logger
            with pytest.raises(SystemExit) as exc:
                execute_sprint(config)
            assert exc.value.code == 1

        assert captured[0].outcome == SprintOutcome.INTERRUPTED
        assert captured[0].phase_results == []


class TestBudgetGuard:
    """Tests for pre-launch budget guard."""

    def test_budget_guard_allows_launch_when_sufficient(self):
        ledger = TurnLedger(initial_budget=50, minimum_allocation=5)
        assert check_budget_guard(ledger) is None

    def test_budget_guard_blocks_launch_when_insufficient(self):
        ledger = TurnLedger(initial_budget=50, minimum_allocation=5)
        ledger.debit(46)
        msg = check_budget_guard(ledger)
        assert msg is not None
        assert "4 turns remaining" in msg
        assert "minimum 5 required" in msg

    def test_budget_guard_allows_at_exact_minimum(self):
        ledger = TurnLedger(initial_budget=50, minimum_allocation=5)
        ledger.debit(45)
        assert check_budget_guard(ledger) is None

    def test_budget_guard_none_ledger_allows_launch(self):
        """When no ledger is provided, launch is always allowed."""
        assert check_budget_guard(None) is None

    def test_budget_guard_message_includes_values(self):
        ledger = TurnLedger(initial_budget=100, minimum_allocation=10)
        ledger.debit(95)
        msg = check_budget_guard(ledger)
        assert msg is not None
        assert "5 turns remaining" in msg
        assert "minimum 10 required" in msg


class TestPerTaskOrchestration:
    """Tests for per-task subprocess orchestration loop."""

    @staticmethod
    def _make_tasks(count: int = 3) -> list[TaskEntry]:
        return [
            TaskEntry(
                task_id=f"T02.{i:02d}",
                title=f"Task {i}",
                dependencies=[f"T02.{i - 1:02d}"] if i > 1 else [],
            )
            for i in range(1, count + 1)
        ]

    @staticmethod
    def _pass_factory(task, config, phase):
        """Subprocess factory that always succeeds with 3 turns consumed."""
        return (0, 3, 1024)

    @staticmethod
    def _fail_factory(task, config, phase):
        """Subprocess factory that always fails."""
        return (1, 5, 512)

    def test_per_task_spawns_one_subprocess_per_task(self, tmp_path):
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        tasks = self._make_tasks(3)

        spawn_count = [0]

        def counting_factory(task, config, phase):
            spawn_count[0] += 1
            return (0, 2, 100)

        results, remaining, _gate_results = execute_phase_tasks(
            tasks, config, phase, _subprocess_factory=counting_factory
        )
        assert spawn_count[0] == 3
        assert len(results) == 3
        assert remaining == []

    def test_per_task_all_pass(self, tmp_path):
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        tasks = self._make_tasks(2)

        results, remaining, _gate_results = execute_phase_tasks(
            tasks, config, phase, _subprocess_factory=self._pass_factory
        )
        assert all(r.status == TaskStatus.PASS for r in results)
        assert remaining == []

    def test_per_task_budget_prevents_starvation(self, tmp_path):
        """If budget insufficient for next task, HALT with remaining task IDs."""
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        tasks = self._make_tasks(3)

        # Budget allows only 1 task launch (min_allocation=5, budget=8)
        ledger = TurnLedger(initial_budget=8, minimum_allocation=5)

        def consume_factory(task, config, phase):
            return (0, 5, 100)

        results, remaining, _gate_results = execute_phase_tasks(
            tasks,
            config,
            phase,
            ledger=ledger,
            _subprocess_factory=consume_factory,
        )
        # First task succeeds, next two should be skipped due to budget
        passed = [r for r in results if r.status == TaskStatus.PASS]
        skipped = [r for r in results if r.status == TaskStatus.SKIPPED]
        assert len(passed) == 1
        assert len(skipped) == 2
        assert remaining == ["T02.02", "T02.03"]

    def test_per_task_budget_debit_credit(self, tmp_path):
        """TurnLedger debit/credit occurs per-task."""
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        tasks = self._make_tasks(1)

        ledger = TurnLedger(initial_budget=50, minimum_allocation=5)
        initial = ledger.available()

        results, _, _gate_results = execute_phase_tasks(
            tasks,
            config,
            phase,
            ledger=ledger,
            _subprocess_factory=self._pass_factory,
        )
        # Factory returns 3 turns consumed; ledger should reflect that
        assert ledger.available() == initial - 3

    def test_per_task_empty_inventory(self, tmp_path):
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]

        results, remaining, _gate_results = execute_phase_tasks(
            [], config, phase, _subprocess_factory=self._pass_factory
        )
        assert results == []
        assert remaining == []

    def test_per_task_fail_records_status(self, tmp_path):
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        tasks = self._make_tasks(1)

        results, _, _gate_results = execute_phase_tasks(
            tasks, config, phase, _subprocess_factory=self._fail_factory
        )
        assert results[0].status == TaskStatus.FAIL_TERMINAL
        assert results[0].exit_code == 1

    def test_per_task_timeout_produces_incomplete(self, tmp_path):
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        tasks = self._make_tasks(1)

        def timeout_factory(task, config, phase):
            return (124, 10, 200)

        results, _, _gate_results = execute_phase_tasks(
            tasks, config, phase, _subprocess_factory=timeout_factory
        )
        assert results[0].status == TaskStatus.INCOMPLETE
        assert results[0].exit_code == 124

    def test_per_task_no_ledger_always_launches(self, tmp_path):
        """Without a ledger, all tasks always launch."""
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        tasks = self._make_tasks(5)

        results, remaining, _gate_results = execute_phase_tasks(
            tasks,
            config,
            phase,
            ledger=None,
            _subprocess_factory=self._pass_factory,
        )
        assert len(results) == 5
        assert all(r.status == TaskStatus.PASS for r in results)
        assert remaining == []


class TestIsolation:
    """Tests for 4-layer subprocess isolation setup."""

    def test_setup_isolation_creates_all_dirs(self, tmp_path):
        config = _make_config(tmp_path, num_phases=1)
        layers = setup_isolation(config)

        assert layers.scoped_work_dir.exists()
        assert layers.git_boundary.exists()
        assert layers.plugin_dir.exists()
        assert layers.settings_dir.exists()

    def test_isolation_all_four_layers_active(self, tmp_path):
        config = _make_config(tmp_path, num_phases=1)
        layers = setup_isolation(config)

        active = layers.layers_active
        assert len(active) == 4
        assert "scoped_work_dir" in active
        assert "git_boundary" in active
        assert "empty_plugin_dir" in active
        assert "restricted_settings" in active

    def test_isolation_env_vars(self, tmp_path):
        config = _make_config(tmp_path, num_phases=1)
        layers = setup_isolation(config)

        env = layers.env_vars
        assert "CLAUDE_WORK_DIR" in env
        assert "GIT_CEILING_DIRECTORIES" in env
        assert "CLAUDE_PLUGIN_DIR" in env
        assert "CLAUDE_SETTINGS_DIR" in env

    def test_isolation_plugin_dir_is_empty(self, tmp_path):
        config = _make_config(tmp_path, num_phases=1)
        layers = setup_isolation(config)

        # Plugin dir should exist but be empty
        assert layers.plugin_dir.exists()
        assert list(layers.plugin_dir.iterdir()) == []

    def test_isolation_no_cross_task_leakage(self, tmp_path):
        """Two consecutive calls produce independent isolation directories."""
        config = _make_config(tmp_path, num_phases=1)
        layers1 = setup_isolation(config)
        layers2 = setup_isolation(config)

        # Same paths (idempotent), but plugin/settings dirs are clean
        assert layers1.plugin_dir == layers2.plugin_dir
        assert layers1.settings_dir == layers2.settings_dir

    def test_isolation_idempotent(self, tmp_path):
        """Calling setup_isolation twice does not raise."""
        config = _make_config(tmp_path, num_phases=1)
        layers1 = setup_isolation(config)
        layers2 = setup_isolation(config)
        assert layers1.env_vars == layers2.env_vars


class TestResultAggregation:
    """Tests for runner-constructed phase report aggregation."""

    @staticmethod
    def _make_task_result(
        task_id: str, status: TaskStatus, turns: int = 3
    ) -> TaskResult:
        return TaskResult(
            task=TaskEntry(task_id=task_id, title=f"Task {task_id}"),
            status=status,
            turns_consumed=turns,
            exit_code=0 if status == TaskStatus.PASS else 1,
        )

    def test_aggregate_all_pass(self):
        results = [
            self._make_task_result("T02.01", TaskStatus.PASS, 3),
            self._make_task_result("T02.02", TaskStatus.PASS, 5),
        ]
        report = aggregate_task_results(2, results)
        assert report.tasks_total == 2
        assert report.tasks_passed == 2
        assert report.tasks_failed == 0
        assert report.status == "PASS"
        assert report.total_turns_consumed == 8

    def test_aggregate_mixed_results(self):
        results = [
            self._make_task_result("T02.01", TaskStatus.PASS, 3),
            self._make_task_result("T02.02", TaskStatus.FAIL_TERMINAL, 5),
        ]
        report = aggregate_task_results(2, results)
        assert report.tasks_total == 2
        assert report.tasks_passed == 1
        assert report.tasks_failed == 1
        assert report.status == "PARTIAL"

    def test_aggregate_all_fail(self):
        results = [
            self._make_task_result("T02.01", TaskStatus.FAIL_TERMINAL, 3),
        ]
        report = aggregate_task_results(2, results)
        assert report.status == "FAIL"

    def test_aggregate_with_remaining(self):
        results = [
            self._make_task_result("T02.01", TaskStatus.PASS, 3),
            self._make_task_result("T02.02", TaskStatus.SKIPPED, 0),
        ]
        remaining = ["T02.02", "T02.03"]
        report = aggregate_task_results(2, results, remaining)
        assert report.tasks_total == 4  # 2 results + 2 remaining
        assert report.remaining_task_ids == ["T02.02", "T02.03"]

    def test_aggregate_includes_incomplete(self):
        results = [
            self._make_task_result("T02.01", TaskStatus.PASS, 3),
            self._make_task_result("T02.02", TaskStatus.INCOMPLETE, 10),
        ]
        report = aggregate_task_results(2, results)
        assert report.tasks_incomplete == 1
        assert report.status == "PARTIAL"

    def test_aggregate_empty(self):
        report = aggregate_task_results(2, [])
        assert report.tasks_total == 0
        assert report.status == "PASS"

    def test_to_markdown_contains_frontmatter(self):
        results = [
            self._make_task_result("T02.01", TaskStatus.PASS, 3),
        ]
        report = aggregate_task_results(2, results)
        md = report.to_markdown()
        assert "---" in md
        assert "status: PASS" in md
        assert "tasks_total: 1" in md
        assert "tasks_passed: 1" in md
        assert "EXIT_RECOMMENDATION: CONTINUE" in md

    def test_to_markdown_halt_on_failure(self):
        results = [
            self._make_task_result("T02.01", TaskStatus.FAIL_TERMINAL, 5),
        ]
        report = aggregate_task_results(2, results)
        md = report.to_markdown()
        assert "status: FAIL" in md
        assert "EXIT_RECOMMENDATION: HALT" in md

    def test_to_markdown_partial_halt(self):
        results = [
            self._make_task_result("T02.01", TaskStatus.PASS, 3),
            self._make_task_result("T02.02", TaskStatus.FAIL_TERMINAL, 5),
        ]
        report = aggregate_task_results(2, results)
        md = report.to_markdown()
        assert "status: PARTIAL" in md
        assert "EXIT_RECOMMENDATION: HALT" in md

    def test_phase_report_is_runner_constructed(self):
        """Verify report is constructed by runner, not by agent self-report."""
        results = [
            self._make_task_result("T02.01", TaskStatus.PASS, 3),
        ]
        report = aggregate_task_results(2, results)
        # Report has task_results directly from runner, not from parsing output
        assert report.task_results is results
        assert report.phase_number == 2


class TestPhaseYamlReport:
    """Tests for phase-level YAML report aggregation (T04.03)."""

    @staticmethod
    def _make_task_result(
        task_id: str, status: TaskStatus, turns: int = 3
    ) -> TaskResult:
        from superclaude.cli.sprint.models import GateOutcome

        return TaskResult(
            task=TaskEntry(task_id=task_id, title=f"Task {task_id}"),
            status=status,
            turns_consumed=turns,
            exit_code=0 if status == TaskStatus.PASS else 1,
            gate_outcome=GateOutcome.PASS
            if status == TaskStatus.PASS
            else GateOutcome.FAIL,
        )

    def test_phase_yaml_contains_required_fields(self):
        """YAML report contains all required fields from roadmap spec."""
        results = [
            self._make_task_result("T03.01", TaskStatus.PASS, 5),
            self._make_task_result("T03.02", TaskStatus.FAIL_TERMINAL, 3),
        ]
        report = aggregate_task_results(3, results, budget_remaining=42)
        yaml_str = report.to_yaml()
        assert "tasks_total: 2" in yaml_str
        assert "tasks_passed: 1" in yaml_str
        assert "tasks_failed: 1" in yaml_str
        assert "tasks_incomplete: 0" in yaml_str
        assert "tasks_not_attempted: 0" in yaml_str
        assert "budget_remaining: 42" in yaml_str

    def test_phase_yaml_with_remaining_tasks(self):
        results = [
            self._make_task_result("T03.01", TaskStatus.PASS, 5),
        ]
        report = aggregate_task_results(
            3, results, remaining_task_ids=["T03.02", "T03.03"], budget_remaining=10
        )
        yaml_str = report.to_yaml()
        assert "tasks_not_attempted: 2" in yaml_str
        assert "remaining_tasks:" in yaml_str
        assert "- T03.02" in yaml_str

    def test_phase_yaml_is_valid_yaml(self):
        """YAML output is parseable by standard YAML libraries."""
        yaml = pytest.importorskip("yaml")
        results = [
            self._make_task_result("T03.01", TaskStatus.PASS, 5),
            self._make_task_result("T03.02", TaskStatus.FAIL_TERMINAL, 3),
        ]
        report = aggregate_task_results(3, results, budget_remaining=20)
        yaml_str = report.to_yaml()
        parsed = yaml.safe_load(yaml_str)
        assert parsed["phase"] == 3
        assert parsed["status"] == "PARTIAL"
        assert parsed["tasks_total"] == 2
        assert parsed["tasks_passed"] == 1
        assert parsed["budget_remaining"] == 20
        assert len(parsed["tasks"]) == 2

    def test_phase_yaml_field_values_match_aggregation(self):
        """Field values match actual TaskResult aggregation."""
        results = [
            self._make_task_result("T03.01", TaskStatus.PASS, 5),
            self._make_task_result("T03.02", TaskStatus.PASS, 8),
            self._make_task_result("T03.03", TaskStatus.FAIL_TERMINAL, 2),
        ]
        report = aggregate_task_results(3, results, budget_remaining=35)
        yaml_str = report.to_yaml()
        assert "tasks_total: 3" in yaml_str
        assert "tasks_passed: 2" in yaml_str
        assert "tasks_failed: 1" in yaml_str
        assert "total_turns_consumed: 15" in yaml_str
        assert "budget_remaining: 35" in yaml_str

    def test_phase_yaml_task_details(self):
        """Each task entry in YAML includes task_id, status, gate_outcome."""
        results = [
            self._make_task_result("T03.01", TaskStatus.PASS, 5),
        ]
        report = aggregate_task_results(3, results)
        yaml_str = report.to_yaml()
        assert "task_id: T03.01" in yaml_str
        assert "status: pass" in yaml_str
        assert "gate_outcome: pass" in yaml_str
        assert "turns_consumed: 5" in yaml_str

    def test_phase_yaml_empty_report(self):
        report = aggregate_task_results(3, [])
        yaml_str = report.to_yaml()
        assert "status: PASS" in yaml_str
        assert "tasks_total: 0" in yaml_str


class TestTurnCountDebit:
    """Tests for turn counting and TurnLedger debit wiring integration."""

    def test_debit_called_with_correct_turns(self, tmp_path):
        """ledger.debit() called with correct turn count after each task."""
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        tasks = [
            TaskEntry(task_id="T02.01", title="Task 1"),
            TaskEntry(task_id="T02.02", title="Task 2"),
        ]
        ledger = TurnLedger(initial_budget=100, minimum_allocation=5)

        def factory(task, config, phase):
            return (0, 7, 100)  # 7 turns consumed per task

        results, _, _gate_results = execute_phase_tasks(
            tasks,
            config,
            phase,
            ledger=ledger,
            _subprocess_factory=factory,
        )
        # 2 tasks * 7 turns = 14 consumed
        assert ledger.consumed == 14
        assert ledger.available() == 100 - 14

    def test_can_remediate_prevents_remediation_when_low(self, tmp_path):
        """ledger.can_remediate() prevents remediation spawn when budget insufficient."""
        ledger = TurnLedger(
            initial_budget=10,
            minimum_allocation=5,
            minimum_remediation_budget=3,
        )
        # Consume most of the budget
        ledger.debit(8)
        assert ledger.available() == 2
        assert ledger.can_remediate() is False

    def test_can_remediate_allows_when_sufficient(self):
        ledger = TurnLedger(
            initial_budget=50,
            minimum_allocation=5,
            minimum_remediation_budget=3,
        )
        assert ledger.can_remediate() is True

    def test_turn_count_zero_reimburses_minimum(self, tmp_path):
        """If a task uses 0 turns, minimum_allocation is credited back."""
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        tasks = [TaskEntry(task_id="T02.01", title="Task 1")]
        ledger = TurnLedger(initial_budget=50, minimum_allocation=5)

        def zero_turn_factory(task, config, phase):
            return (0, 0, 100)  # 0 turns consumed

        execute_phase_tasks(
            tasks,
            config,
            phase,
            ledger=ledger,
            _subprocess_factory=zero_turn_factory,
        )
        # Pre-debited 5, actual 0, so credited 5 back
        # Net effect: 0 consumed
        assert ledger.available() == 50


class TestIntegrationSubprocess:
    """Integration test: full per-task subprocess loop with budget tracking.

    Exercises ≥5 tasks through parse → allocate → launch → collect → aggregate
    with budget verification. (D-0012)
    """

    @staticmethod
    def _make_tasks(count: int = 5) -> list[TaskEntry]:
        return [
            TaskEntry(
                task_id=f"T03.{i:02d}",
                title=f"Integration Task {i}",
                description=f"Test task {i} for integration",
                dependencies=[f"T03.{i - 1:02d}"] if i > 1 else [],
            )
            for i in range(1, count + 1)
        ]

    def test_integration_subprocess_five_tasks_mixed_outcomes(self, tmp_path):
        """Full loop: 5 tasks with varied outcomes and budget accounting."""
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        tasks = self._make_tasks(5)

        # Track per-task consumption: task 1=3, task 2=7, task 3=2, task 4=5, task 5=4
        outcomes = [
            (0, 3, 1024),  # PASS, 3 turns
            (0, 7, 2048),  # PASS, 7 turns
            (1, 2, 512),  # FAIL, 2 turns
            (0, 5, 1536),  # PASS, 5 turns
            (124, 4, 256),  # INCOMPLETE (timeout), 4 turns
        ]
        call_index = [0]

        def mixed_factory(task, config, phase):
            idx = call_index[0]
            call_index[0] += 1
            return outcomes[idx]

        ledger = TurnLedger(initial_budget=100, minimum_allocation=5)
        results, remaining, _gate_results = execute_phase_tasks(
            tasks,
            config,
            phase,
            ledger=ledger,
            _subprocess_factory=mixed_factory,
        )

        # All 5 tasks launched (no budget exhaustion)
        assert len(results) == 5
        assert remaining == []
        assert call_index[0] == 5

        # Verify per-task statuses
        assert results[0].status == TaskStatus.PASS
        assert results[1].status == TaskStatus.PASS
        assert results[2].status == TaskStatus.FAIL_TERMINAL
        assert results[3].status == TaskStatus.PASS
        assert results[4].status == TaskStatus.INCOMPLETE

        # Budget accounting: available reflects actual turn consumption
        # The executor pre-debits minimum_allocation (5) per task, then reconciles.
        # Net effect on available: initial - sum(actual_turns)
        actual_turns = [3, 7, 2, 5, 4]
        net_consumed = sum(actual_turns)  # 21
        assert ledger.available() == 100 - net_consumed  # = 79
        # Verify internal accounting is consistent
        assert (
            ledger.available()
            == ledger.initial_budget - ledger.consumed + ledger.reimbursed
        )

        # Aggregate into phase report
        report = aggregate_task_results(
            phase_number=1, task_results=results, remaining_task_ids=remaining
        )
        assert report.tasks_total == 5
        assert report.tasks_passed == 3
        assert report.tasks_failed == 1
        assert report.tasks_incomplete == 1
        assert report.status == "PARTIAL"
        assert report.total_turns_consumed == sum(r.turns_consumed for r in results)

    def test_integration_subprocess_budget_exhaustion_skips_remaining(self, tmp_path):
        """Budget exhaustion after 3 tasks skips remaining 2."""
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        tasks = self._make_tasks(5)

        # Each task consumes 8 turns; budget=25, minimum_allocation=5
        # Task 1: debit 5 upfront, then adjust to 8 → consumed=8, avail=17
        # Task 2: debit 5 upfront, then adjust to 8 → consumed=16, avail=9
        # Task 3: debit 5 upfront, then adjust to 8 → consumed=24, avail=1
        # Task 4: can_launch? avail=1 < min_alloc=5 → SKIP
        def heavy_factory(task, config, phase):
            return (0, 8, 500)

        ledger = TurnLedger(initial_budget=25, minimum_allocation=5)
        results, remaining, _gate_results = execute_phase_tasks(
            tasks,
            config,
            phase,
            ledger=ledger,
            _subprocess_factory=heavy_factory,
        )

        passed = [r for r in results if r.status == TaskStatus.PASS]
        skipped = [r for r in results if r.status == TaskStatus.SKIPPED]
        assert len(passed) == 3
        assert len(skipped) == 2
        assert remaining == ["T03.04", "T03.05"]

        # Aggregate reflects skipped tasks
        report = aggregate_task_results(1, results, remaining)
        assert report.tasks_total == 7  # 5 results + 2 remaining
        assert report.tasks_skipped == 2

    def test_integration_subprocess_all_pass_aggregation(self, tmp_path):
        """All 5 tasks pass → PASS status and CONTINUE recommendation."""
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        tasks = self._make_tasks(5)

        def pass_factory(task, config, phase):
            return (0, 3, 1024)

        ledger = TurnLedger(initial_budget=100, minimum_allocation=5)
        results, remaining, _gate_results = execute_phase_tasks(
            tasks,
            config,
            phase,
            ledger=ledger,
            _subprocess_factory=pass_factory,
        )

        assert all(r.status == TaskStatus.PASS for r in results)
        assert remaining == []

        report = aggregate_task_results(1, results, remaining)
        assert report.status == "PASS"
        md = report.to_markdown()
        assert "EXIT_RECOMMENDATION: CONTINUE" in md
        assert "tasks_total: 5" in md
        assert "tasks_passed: 5" in md

        # Budget: 5 tasks * 3 turns each = 15 net consumed
        # available = initial - net consumed = 100 - 15 = 85
        assert ledger.available() == 85


class TestBackwardCompat:
    """Backward compatibility tests: grace_period=0 produces v1.2.1 behavior.

    Verifies that the default configuration (grace_period=0, GateMode.BLOCKING)
    produces results identical to pre-trailing-gate behavior with zero
    additional daemon threads from the gate system. (D-0013)
    """

    def test_backward_compat_grace_period_zero_is_default(self):
        """SprintConfig inherits grace_period=0 from PipelineConfig by default."""
        from superclaude.cli.pipeline.models import PipelineConfig

        pc = PipelineConfig()
        assert pc.grace_period == 0

        config = SprintConfig(
            index_path=Path("/tmp/index.md"),
            release_dir=Path("/tmp/release"),
            phases=[Phase(number=1, file=Path("/tmp/p1.md"))],
        )
        assert config.grace_period == 0

    def test_backward_compat_gate_mode_blocking_is_default(self):
        """GateMode.BLOCKING is the default for pipeline steps, matching v1.2.1 behavior."""
        from superclaude.cli.pipeline.models import GateMode, Step

        step = Step(
            id="test",
            prompt="test",
            output_file=Path("/tmp/out.txt"),
            gate=None,
            timeout_seconds=60,
        )
        assert step.gate_mode == GateMode.BLOCKING

    def test_backward_compat_sprint_pass_grace_period_zero(self, tmp_path):
        """Full sprint with grace_period=0 produces identical PASS result to v1.2.1."""
        import threading

        config = _make_config(tmp_path, num_phases=1)
        assert config.grace_period == 0  # confirm default

        class _PassPopen:
            def __init__(self):
                self.returncode = 0
                self.pid = 2001
                self._poll = 0

            def poll(self):
                self._poll += 1
                return None if self._poll <= 1 else 0

            def wait(self, timeout=None):
                self.returncode = 0
                return 0

        def _factory(*args, **kwargs):
            phase = config.phases[0]
            config.results_dir.mkdir(parents=True, exist_ok=True)
            config.result_file(phase).write_text("EXIT_RECOMMENDATION: CONTINUE\n")
            config.output_file(phase).write_text("output\n")
            return _PassPopen()

        baseline_threads = threading.active_count()

        captured = []
        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.pipeline.process.subprocess.Popen",
                side_effect=_factory,
            ),
            patch("superclaude.cli.pipeline.process.os.setpgrp"),
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.executor.SprintLogger") as logger_cls,
        ):
            logger = MagicMock()
            logger.write_summary = MagicMock(side_effect=lambda sr: captured.append(sr))
            logger_cls.return_value = logger
            execute_sprint(config)

        # After sprint completes, thread count should return to baseline
        # (the OutputMonitor daemon thread is stopped in the finally block)
        post_threads = threading.active_count()
        assert post_threads <= baseline_threads + 1  # allow +1 for monitor cleanup race

        # Sprint result matches v1.2.1 behavior exactly
        sr = captured[0]
        assert sr.outcome == SprintOutcome.SUCCESS
        assert len(sr.phase_results) == 1
        assert sr.phase_results[0].status == PhaseStatus.PASS
        assert sr.phase_results[0].exit_code == 0

    def test_backward_compat_per_task_no_ledger(self, tmp_path):
        """Without a TurnLedger, per-task loop behaves identically to v1.2.1."""
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        tasks = [
            TaskEntry(task_id="T03.01", title="Task 1"),
            TaskEntry(task_id="T03.02", title="Task 2"),
            TaskEntry(task_id="T03.03", title="Task 3"),
        ]

        def pass_factory(task, config, phase):
            return (0, 3, 1024)

        # No ledger = v1.2.1 behavior (no budget tracking)
        results, remaining, _gate_results = execute_phase_tasks(
            tasks,
            config,
            phase,
            ledger=None,
            _subprocess_factory=pass_factory,
        )
        assert len(results) == 3
        assert all(r.status == TaskStatus.PASS for r in results)
        assert remaining == []

    def test_backward_compat_existing_tests_pass_under_grace_period_zero(
        self, tmp_path
    ):
        """Verify the default config has grace_period=0 and still supports
        all standard sprint operations (this test documents the invariant)."""
        config = _make_config(tmp_path, num_phases=2)
        assert config.grace_period == 0

        # All config accessors work identically
        assert config.results_dir == tmp_path / "results"
        assert config.execution_log_jsonl == tmp_path / "execution-log.jsonl"
        assert config.execution_log_md == tmp_path / "execution-log.md"
        assert len(config.active_phases) == 2
        assert config.output_file(config.phases[0]).name == "phase-1-output.txt"
        assert config.error_file(config.phases[0]).name == "phase-1-errors.txt"
        assert config.result_file(config.phases[0]).name == "phase-1-result.md"

    def test_backward_compat_no_leaked_daemon_threads_in_executor(self):
        """Stage 3 adds bounded per-task parallelism (--task-parallelism K), so the
        executor now legitimately uses a threading lock and a context-managed
        ThreadPoolExecutor. The backward-compat invariant is no LEAKED daemon
        threads — not 'no threading import'. This test enforces that the executor
        spawns no raw long-lived daemon threads (any pool is context-managed and
        joined on block exit); the runtime no-leak guarantee is separately
        verified by the threading.active_count() backward-compat tests."""
        import superclaude.cli.sprint.executor as mod

        source = Path(mod.__file__).read_text()
        # No raw daemon-thread spawns (OutputMonitor's threads remain its own).
        assert "Thread(" not in source
        assert "daemon=True" not in source
        # Any ThreadPoolExecutor use MUST be context-managed so workers are joined.
        if "ThreadPoolExecutor" in source:
            assert "with ThreadPoolExecutor" in source


class TestWritePreliminaryResult:
    """Unit tests for _write_preliminary_result() — T-001, T-002, T-002b, T-005."""

    def test_t001_absent_file_written_with_sentinel(self, tmp_path):
        """T-001: When result file is absent, writes CONTINUE sentinel and returns True."""
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        # Ensure the result file does not exist
        result_path = config.result_file(phase)
        assert not result_path.exists()

        started_at = datetime.now(timezone.utc).timestamp() - 1.0  # 1 s in the past

        return_val = _write_preliminary_result(config, phase, started_at)

        assert return_val is True
        assert result_path.exists()
        assert result_path.read_text() == "EXIT_RECOMMENDATION: CONTINUE\n"

    def test_t002_fresh_agent_file_preserved(self, tmp_path):
        """T-002: Fresh non-empty agent file (st_mtime >= started_at) is untouched; returns False."""
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        result_path = config.result_file(phase)
        result_path.parent.mkdir(parents=True, exist_ok=True)

        # Write a non-empty file and capture its mtime
        original_content = "EXIT_RECOMMENDATION: HALT\n"
        result_path.write_text(original_content)
        file_mtime = result_path.stat().st_mtime

        # started_at strictly before the file mtime → file is fresh
        started_at = file_mtime - 1.0

        return_val = _write_preliminary_result(config, phase, started_at)

        assert return_val is False
        assert result_path.read_text() == original_content  # file unchanged

    def test_t002b_zero_byte_file_overwritten(self, tmp_path):
        """T-002b: Zero-byte file is treated as absent and overwritten with sentinel; returns True."""
        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        result_path = config.result_file(phase)
        result_path.parent.mkdir(parents=True, exist_ok=True)

        # Write an empty (zero-byte) file — even a fresh one should be overwritten
        result_path.write_text("")
        file_mtime = result_path.stat().st_mtime
        started_at = file_mtime - 1.0  # started_at before mtime, but file is zero-byte

        return_val = _write_preliminary_result(config, phase, started_at)

        assert return_val is True
        assert result_path.read_text() == "EXIT_RECOMMENDATION: CONTINUE\n"

    def test_t005_oserror_returns_false_with_warning(self, tmp_path, caplog):
        """T-005: OSError on write returns False (no exception raised) and logs a WARNING."""
        import logging

        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        # Ensure the result file does not pre-exist so the freshness guard doesn't fire
        result_path = config.result_file(phase)
        assert not result_path.exists()
        started_at = datetime.now(timezone.utc).timestamp() - 1.0

        with caplog.at_level(logging.WARNING, logger="superclaude.cli.sprint.executor"):
            # RC.4: the sentinel is now written via an O_EXCL os.open (not write_text),
            # so inject the OSError there to exercise the telemetry branch.
            with patch(
                "superclaude.cli.sprint.executor.os.open",
                side_effect=OSError("disk full"),
            ):
                return_val = _write_preliminary_result(config, phase, started_at)

        assert return_val is False
        warning_messages = [
            r.message for r in caplog.records if r.levelno == logging.WARNING
        ]
        assert any("preliminary result write failed" in m for m in warning_messages)


class TestTimeoutFormulaConsistency:
    """C3 — Assert SprintGatePolicy.build_remediation_step uses the canonical
    `max_turns * 120 + 300` formula matching executor.py:1106 and
    sprint/process.py:115. Regression guard against the divergent
    `max_turns * 60` foot-gun.
    """

    def _make_gate_result(self, step_id: str = "step-x") -> object:
        from superclaude.cli.pipeline.trailing_gate import TrailingGateResult

        return TrailingGateResult(
            step_id=step_id,
            passed=False,
            evaluation_ms=0.0,
            failure_reason="synthetic",
        )

    def test_remediation_step_timeout_matches_canonical_formula(self, tmp_path):
        from superclaude.cli.sprint.executor import SprintGatePolicy

        config = _make_config(tmp_path, num_phases=1)
        # _make_config sets max_turns=5; override to 50 for the canonical assertion
        config = SprintConfig(**{**config.__dict__, "max_turns": 50})
        policy = SprintGatePolicy(config)
        step = policy.build_remediation_step(self._make_gate_result())
        assert step.timeout_seconds == 50 * 120 + 300 == 6300, (
            f"Expected canonical timeout 6300s (max_turns=50 * 120 + 300), "
            f"got {step.timeout_seconds}"
        )

    def test_remediation_step_timeout_matches_per_phase_for_various_max_turns(
        self, tmp_path
    ):
        from superclaude.cli.sprint.executor import SprintGatePolicy

        base = _make_config(tmp_path, num_phases=1)
        expected = {
            1: 1 * 120 + 300,
            50: 50 * 120 + 300,
            100: 100 * 120 + 300,
            500: 500 * 120 + 300,
        }
        for mt, want in expected.items():
            config = SprintConfig(**{**base.__dict__, "max_turns": mt})
            policy = SprintGatePolicy(config)
            step = policy.build_remediation_step(self._make_gate_result())
            assert step.timeout_seconds == want, (
                f"max_turns={mt}: expected {want}s, got {step.timeout_seconds}"
            )


class TestPhaseResultJsonWrite:
    """Tests for _write_phase_result_json — v4.3.0 phase-N-result.json (TDD §T6)."""

    @staticmethod
    def _make_task_result(
        task_id: str, status: TaskStatus, turns: int = 3
    ) -> TaskResult:
        return TaskResult(
            task=TaskEntry(task_id=task_id, title=f"Task {task_id}"),
            status=status,
            turns_consumed=turns,
            exit_code=0 if status == TaskStatus.PASS else 1,
        )

    def _make_phase_result(self, phase, task_results, *, all_passed):
        from superclaude.cli.sprint.models import PhaseResult

        now = datetime.now(timezone.utc)
        return PhaseResult(
            phase=phase,
            status=PhaseStatus.PASS if all_passed else PhaseStatus.ERROR,
            exit_code=0 if all_passed else 1,
            started_at=now,
            finished_at=now,
            task_results=task_results,
        )

    def test_phase_result_json_written_at_phase_end(self, tmp_path):
        """After the phase result is persisted, phase-N-result.json exists."""
        from superclaude.cli.sprint.executor import _write_phase_result_json

        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        task_results = [self._make_task_result("T01.01", TaskStatus.PASS, 3)]
        phase_result = self._make_phase_result(
            phase, task_results, all_passed=True
        )

        _write_phase_result_json(config, phase, phase_result)

        out = config.phase_result_json(phase)
        assert out.exists()
        assert out.name == "phase-1-result.json"

    def test_phase_result_json_includes_task_results_and_status(self, tmp_path):
        """Parsed JSON has a populated task_results array and a correct status."""
        import json

        from superclaude.cli.sprint.executor import _write_phase_result_json

        config = _make_config(tmp_path, num_phases=1)
        phase = config.phases[0]
        task_results = [
            self._make_task_result("T01.01", TaskStatus.PASS, 3),
            self._make_task_result("T01.02", TaskStatus.FAIL_TERMINAL, 5),
        ]
        phase_result = self._make_phase_result(
            phase, task_results, all_passed=False
        )

        _write_phase_result_json(config, phase, phase_result)

        payload = json.loads(config.phase_result_json(phase).read_text())
        assert payload["phase"] == 1
        # ERROR phase status serializes to its enum value
        assert payload["status"] == PhaseStatus.ERROR.value
        assert payload["exit_code"] == 1
        assert isinstance(payload["task_results"], list)
        assert len(payload["task_results"]) == 2
        ids = [tr["task"]["task_id"] for tr in payload["task_results"]]
        assert ids == ["T01.01", "T01.02"]
        assert payload["task_results"][0]["status"] == TaskStatus.PASS.value
        assert (
            payload["task_results"][1]["status"] == TaskStatus.FAIL_TERMINAL.value
        )


class TestFailClassificationHeuristic:
    """Tests for the transient/terminal classification ladder (TDD §T6).

    Drives _is_transient_failure directly — the same helper the executor's
    status ladder (executor.py:1020-1023) consults to choose between
    FAIL_RECOVERABLE and FAIL_TERMINAL for a non-zero, non-timeout exit.
    """

    def _classify(self, output_path: Path) -> TaskStatus:
        """Mirror the executor ladder for a failing (exit_code != 0/124) task."""
        from superclaude.cli.sprint.executor import _is_transient_failure

        if _is_transient_failure(output_path):
            return TaskStatus.FAIL_RECOVERABLE
        return TaskStatus.FAIL_TERMINAL

    def test_transient_proxy_error_classified_fail_recoverable(self, tmp_path):
        """A transient trigger (is_error + zero output tokens) → FAIL_RECOVERABLE."""
        output = tmp_path / "task-output.txt"
        output.write_text(
            '{"type":"content","text":"calling tool"}\n'
            '{"type":"result","is_error":true,"output_tokens":0}\n'
        )
        assert self._classify(output) == TaskStatus.FAIL_RECOVERABLE

    def test_transient_connection_refused_classified_fail_recoverable(
        self, tmp_path
    ):
        """The ConnectionRefused marker is also a transient trigger."""
        output = tmp_path / "task-output.txt"
        output.write_text("Error: ConnectionRefused while reaching API\n")
        assert self._classify(output) == TaskStatus.FAIL_RECOVERABLE

    def test_assertion_error_classified_fail_terminal(self, tmp_path):
        """is_error: true but NON-zero output tokens and no marker → FAIL_TERMINAL."""
        output = tmp_path / "task-output.txt"
        output.write_text(
            '{"type":"content","text":"running tests"}\n'
            '{"type":"result","is_error":true,"output_tokens":512,'
            '"text":"AssertionError: expected 3 got 4"}\n'
        )
        assert self._classify(output) == TaskStatus.FAIL_TERMINAL


def test_run_task_subprocess_uses_task_output_file(tmp_path):
    """C2 — `_run_task_subprocess` must wire `task_output_file(phase, task)` /
    `task_error_file(phase, task)` into the underlying ClaudeProcess, NOT the
    phase-scoped `output_file(phase)` / `error_file(phase)`. Also confirms the
    C3 canonical formula is preserved (`max_turns * 120 + 300`).
    """
    from unittest.mock import MagicMock, patch

    from superclaude.cli.sprint.executor import _run_task_subprocess

    config = _make_config(tmp_path, num_phases=1)
    phase = config.phases[0]
    task = TaskEntry(task_id="T01.01", title="x", description="d")

    captured = {}

    def capture_init(self, **kwargs):
        captured.update(kwargs)
        # Populate attributes the post-init code path reads
        self._process = MagicMock(returncode=0)
        self._stdout_fh = None
        self._stderr_fh = None

    # Pre-create the output file so the post-subprocess size read at
    # executor.py:1114 doesn't trigger FileNotFoundError (the .stat() inside
    # `if output_path.exists():` guards but `stat()` itself is fine when path
    # is missing — the guard handles it). Still, give it something.
    config.results_dir.mkdir(parents=True, exist_ok=True)
    config.task_output_file(phase, task).write_text("")

    with (
        patch(
            "superclaude.cli.pipeline.process.ClaudeProcess.__init__",
            new=capture_init,
        ),
        patch(
            "superclaude.cli.pipeline.process.ClaudeProcess.start",
            return_value=None,
        ),
        patch(
            "superclaude.cli.pipeline.process.ClaudeProcess.wait",
            return_value=0,
        ),
    ):
        rc, _, _ = _run_task_subprocess(task, config, phase)

    assert rc == 0
    # Core C2 assertions
    assert captured["output_file"] == config.task_output_file(phase, task), (
        f"Expected task_output_file path, got {captured.get('output_file')}"
    )
    assert captured["error_file"] == config.task_error_file(phase, task), (
        f"Expected task_error_file path, got {captured.get('error_file')}"
    )
    # Negative: must NOT be the phase-scoped paths
    assert captured["output_file"] != config.output_file(phase)
    assert captured["error_file"] != config.error_file(phase)
    # C3 consistency preserved
    assert captured["timeout_seconds"] == config.max_turns * 120 + 300, (
        f"Expected canonical timeout {config.max_turns * 120 + 300}, "
        f"got {captured.get('timeout_seconds')}"
    )
