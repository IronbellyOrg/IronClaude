"""M2 — the per-task stall watchdog poll loop must be bounded by a wall-clock ceiling.

Before this fix, ``_poll_with_stall_watchdog`` had its only ``break`` inside the
``stall_action == "kill"`` branch. In the default ``warn`` mode a child that never
produced output and never exited caused ``while underlying.poll() is None:`` to spin
forever — the bounded tail ``proc.wait()`` was never reached. This file pins the
wall-clock ceiling (derived from ``proc.timeout_seconds``) that guarantees the warn-mode
loop terminates and falls through to the bounded wait, while asserting that the kill-mode
and disabled paths are unchanged.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.sprint.executor import _poll_with_stall_watchdog
from superclaude.cli.sprint.models import Phase, SprintConfig


def _make_config(tmp_path: Path) -> SprintConfig:
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


class _NeverExitsProc:
    """A child that NEVER exits and NEVER produces output -> the pre-fix infinite spin."""

    def __init__(self, timeout_seconds: int) -> None:
        self.timeout_seconds = timeout_seconds
        self._process = self
        self._waited = False

    def poll(self):
        return None  # never exits on its own

    def terminate(self) -> None:
        pass

    def wait(self) -> None:
        self._waited = True  # the bounded tail wait (executor.py:1465)


@pytest.mark.unit
def test_warn_mode_poll_loop_is_bounded_by_proc_timeout(tmp_path: Path) -> None:
    config = _make_config(tmp_path)
    config.startup_stall_timeout = 1
    config.stall_action = "warn"
    proc = _NeverExitsProc(timeout_seconds=10)

    out = tmp_path / "task-out.txt"  # never grows -> stall fires once

    # Deterministic clock: monotonic advances 5s per call so the ceiling (10s) trips
    # fast with no real wall-time. Against the unfixed (unbounded) loop this test HANGS;
    # it PASSES only when the ceiling is present.
    ticks = iter(float(i) * 5 for i in range(1000))
    with (
        patch("superclaude.cli.sprint.executor.time.sleep"),
        patch(
            "superclaude.cli.sprint.executor.time.monotonic",
            side_effect=lambda: next(ticks),
        ),
    ):
        _poll_with_stall_watchdog(
            proc, config, output_path=out
        )  # MUST return, not hang

    assert proc._waited, (
        "warn-mode poll loop did not fall through to the bounded proc.wait() "
        "— ceiling missing (M2)"
    )


class _KillModeProc:
    """A child that exits only once terminated; records that terminate fired."""

    def __init__(self, timeout_seconds: int) -> None:
        self.timeout_seconds = timeout_seconds
        self._process = self
        self._terminated = False
        self._waited = False

    def poll(self):
        return 0 if self._terminated else None

    def terminate(self) -> None:
        self._terminated = True

    def wait(self) -> None:
        self._waited = True


@pytest.mark.unit
def test_kill_mode_still_terminates_on_stall(tmp_path: Path) -> None:
    """The M2 ceiling fix must NOT regress kill mode: a stalled child under
    stall_action="kill" must still be terminated (executor.py:1459-1464)."""
    config = _make_config(tmp_path)
    config.startup_stall_timeout = 1
    config.stall_action = "kill"
    # Large timeout so the ceiling does not trip before the stall branch fires.
    proc = _KillModeProc(timeout_seconds=100000)

    out = tmp_path / "task-out.txt"  # never grows -> stall fires

    ticks = iter(float(i) * 5 for i in range(1000))
    with (
        patch("superclaude.cli.sprint.executor.time.sleep"),
        patch(
            "superclaude.cli.sprint.executor.time.monotonic",
            side_effect=lambda: next(ticks),
        ),
    ):
        _poll_with_stall_watchdog(proc, config, output_path=out)

    assert proc._terminated, (
        "kill mode must still terminate the stalled child "
        "(M2 must not regress kill mode)"
    )


@pytest.mark.unit
def test_disabled_path_uses_plain_wait(tmp_path: Path) -> None:
    """With startup_stall_timeout <= 0 the watchdog is disabled and degrades to a
    single bare proc.wait() (executor.py:1424-1426) — unchanged by the M2 fix."""
    config = _make_config(tmp_path)
    config.startup_stall_timeout = 0
    proc = _NeverExitsProc(timeout_seconds=10)

    out = tmp_path / "task-out.txt"
    _poll_with_stall_watchdog(proc, config, output_path=out)

    assert proc._waited, "disabled path must reach the plain proc.wait()"
