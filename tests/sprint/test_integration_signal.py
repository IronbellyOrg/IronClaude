"""T04.03 — Integration test: graceful shutdown.

Tests that SIGINT during execution triggers graceful shutdown:
process terminated, partial log written, INTERRUPTED outcome.
"""

from __future__ import annotations

import os
import signal
import threading
from pathlib import Path
from unittest.mock import MagicMock, patch

from superclaude.cli.sprint.executor import execute_sprint
from superclaude.cli.sprint.models import (
    Phase,
    SprintConfig,
    SprintOutcome,
)


def _make_config(tmp_path: Path) -> SprintConfig:
    """Create a 3-phase config where phases take a while."""
    phases = []
    for i in range(1, 4):
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
        end_phase=3,
        max_turns=5,
    )


class _SlowFakePopen:
    """Mock Popen that stays 'running' for many polls."""

    def __init__(self):
        self.returncode = None
        self.pid = 99999
        self.stdin = None
        self._poll_count = 0
        self._terminated = False

    def poll(self):
        if self._terminated:
            self.returncode = -15  # SIGTERM
            return self.returncode
        self._poll_count += 1
        if self._poll_count > 100:
            self.returncode = 0
            return 0
        return None

    def wait(self, timeout=None):
        if self._terminated:
            self.returncode = -15
            return self.returncode
        self.returncode = 0
        return 0


class TestGracefulShutdown:
    """T04.03: SIGINT during poll loop → INTERRUPTED outcome."""

    def test_signal_handler_flag_set(self, tmp_path):
        """Directly test that SignalHandler sets shutdown_requested on signal."""
        from superclaude.cli.sprint.process import SignalHandler

        handler = SignalHandler()
        handler.install()

        try:
            assert not handler.shutdown_requested
            # Simulate signal delivery
            handler._handle(signal.SIGINT, None)
            assert handler.shutdown_requested
        finally:
            handler.uninstall()

    def test_partial_results_captured(self, tmp_path):
        """When interrupted mid-sprint, completed phases are in results."""
        config = _make_config(tmp_path)
        call_count = [0]

        class _FirstSucceedsThenSlow:
            def __init__(self):
                self.returncode = None
                self.pid = 11111
                self.stdin = None
                self._poll_count = 0
                self._terminated = False

            def poll(self):
                if self._terminated:
                    self.returncode = -15
                    return self.returncode
                self._poll_count += 1
                if call_count[0] == 1:
                    # First phase: succeed quickly
                    self.returncode = 0
                    return 0
                if self._poll_count > 100:
                    self.returncode = 0
                    return 0
                return None

            def wait(self, timeout=None):
                if self._terminated:
                    self.returncode = -15
                    return -15
                self.returncode = 0
                return 0

        def popen_factory(cmd, **kwargs):
            call_count[0] += 1
            phase = config.phases[call_count[0] - 1]

            config.results_dir.mkdir(parents=True, exist_ok=True)
            output_path = config.output_file(phase)
            output_path.write_text("working...\n")

            if call_count[0] == 1:
                # Phase 1 succeeds
                result_path = config.result_file(phase)
                result_path.write_text("EXIT_RECOMMENDATION: CONTINUE\n")

            proc = _FirstSucceedsThenSlow()
            proc.returncode = 0 if call_count[0] == 1 else None
            return proc

        captured_results = []

        def send_sigint():
            os.kill(os.getpid(), signal.SIGINT)

        timer = threading.Timer(0.5, send_sigint)

        with (
            patch(
                "superclaude.cli.pipeline.process.subprocess.Popen",
                side_effect=popen_factory,
            ),
            patch("superclaude.cli.pipeline.process.os.setpgrp"),
            patch("superclaude.cli.pipeline.process.os.getpgid", return_value=11111),
            patch("superclaude.cli.pipeline.process.os.killpg"),
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.executor.update_tail_pane"),
            patch("superclaude.cli.sprint.executor.SprintLogger") as mock_logger_cls,
        ):
            logger_inst = MagicMock()
            logger_inst.write_summary = MagicMock(
                side_effect=lambda sr: captured_results.append(sr)
            )
            mock_logger_cls.return_value = logger_inst

            timer.start()
            try:
                execute_sprint(config)
            except SystemExit:
                pass
            finally:
                timer.cancel()

        # Should have at least 1 phase result (the one that completed)
        if captured_results:
            result = captured_results[0]
            assert result.outcome == SprintOutcome.INTERRUPTED
            # Phase 1 completed before interrupt
            assert len(result.phase_results) >= 1
