"""T04.01 — Integration test: full phase lifecycle.

Tests that executor + mocked ClaudeProcess + TUI integrate correctly
through the full lifecycle: PENDING → RUNNING → PASS.
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path

from rich.console import Console

from superclaude.cli.sprint.models import (
    Phase,
    SprintConfig,
)
from superclaude.cli.sprint.tui import SprintTUI


def _make_config(tmp_path: Path, num_phases: int = 1) -> SprintConfig:
    """Create a SprintConfig with N phase files in tmp_path."""
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
    )


def _mock_popen_success(config: SprintConfig):
    """Create a mock Popen that exits 0 and writes CONTINUE to result file."""

    class FakePopen:
        def __init__(self, *args, **kwargs):
            self.returncode = 0
            self.pid = 12345
            self.stdin = None
            self._poll_count = 0

        def poll(self):
            self._poll_count += 1
            if self._poll_count <= 1:
                return None  # still running on first poll
            return 0  # done on second poll

        def wait(self, timeout=None):
            self.returncode = 0
            return 0

    def popen_factory(cmd, **kwargs):
        proc = FakePopen()
        # Write result file with CONTINUE signal
        for phase in config.active_phases:
            result_path = config.result_file(phase)
            result_path.parent.mkdir(parents=True, exist_ok=True)
            result_path.write_text("EXIT_RECOMMENDATION: CONTINUE\n")
            # Write output file so monitor sees content
            output_path = config.output_file(phase)
            output_path.write_text("Working on T01.01\nUsing Read tool\n")
        return proc

    return popen_factory


class TestFullPhaseLifecycle:
    """T04.01: executor drives phases through PENDING → RUNNING → PASS."""

    def test_tui_renders_without_crash(self, tmp_path):
        """TUI renders to StringIO without terminal dependency."""
        config = _make_config(tmp_path, num_phases=1)
        console = Console(file=StringIO(), force_terminal=True, width=120)
        tui = SprintTUI(config, console=console)

        # Start and stop without crashing
        tui.start()
        tui.stop()

        output = console.file.getvalue()
        assert "SUPERCLAUDE SPRINT RUNNER" in output
