"""T04.02 — Integration test: halt and resume command.

Tests that executor halts on failure, produces correct resume_command(),
and does not execute phases after the failure.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.sprint.models import (
    Phase,
    SprintConfig,
)


def _make_config(tmp_path: Path, num_phases: int = 3) -> SprintConfig:
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


class _FakePopenSuccess:
    """Mock Popen that exits 0."""

    def __init__(self):
        self.returncode = 0
        self.pid = 12345
        self.stdin = None
        self._poll_count = 0

    def poll(self):
        self._poll_count += 1
        if self._poll_count <= 1:
            return None
        return 0

    def wait(self, timeout=None):
        self.returncode = 0
        return 0


class _FakePopenFailure:
    """Mock Popen that exits non-zero."""

    def __init__(self):
        self.returncode = 1
        self.pid = 12346
        self.stdin = None
        self._poll_count = 0

    def poll(self):
        self._poll_count += 1
        if self._poll_count <= 1:
            return None
        return 1

    def wait(self, timeout=None):
        self.returncode = 1
        return 1


def _popen_factory_fail_at_phase2(config: SprintConfig):
    """Returns a Popen factory where phase 2 fails, others succeed."""
    call_count = [0]

    def factory(cmd, **kwargs):
        call_count[0] += 1
        phase_num = call_count[0]

        # Ensure results dir exists
        config.results_dir.mkdir(parents=True, exist_ok=True)

        phase = config.phases[phase_num - 1]

        if phase_num == 2:
            # Phase 2 fails — write output but no result file
            output_path = config.output_file(phase)
            output_path.write_text("Phase 2 output\n")
            return _FakePopenFailure()
        else:
            # Other phases succeed
            result_path = config.result_file(phase)
            result_path.parent.mkdir(parents=True, exist_ok=True)
            result_path.write_text("EXIT_RECOMMENDATION: CONTINUE\n")
            output_path = config.output_file(phase)
            output_path.write_text(f"Working on phase {phase_num}\n")
            return _FakePopenSuccess()

    return factory
