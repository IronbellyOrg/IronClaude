"""Monitor-arming tests (spec FR-1.5/FR-2.4).

T-109 `--monitor 1` → Monitor armed exactly once; T-110 `--monitor 0` → Monitor
NEVER armed (the zero-regression guard, AC-1); T-230 session close mid-poll →
run-log records the interruption and `--resume` reconstructs (logging + resume
only — no code assertion beyond that, per FR-2.4; the run-log writer and the
resume rebuild are exercised by test_run_log / test_crash_recovery in Phase 8).
"""

from __future__ import annotations

from superclaude.pr_submit.fsm import RunConfig, parse_args, run_skill
from superclaude.pr_submit.models import MonitorState


class _ArmRecorder:
    """Stand-in for the ``mock_monitor`` fixture: records each arm call."""

    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, *_args, **_kwargs) -> None:
        self.calls += 1


def test_t109_monitor_armed_exactly_once_at_l1():
    """T-109: `--monitor 1` arms the Monitor exactly once."""
    recorder = _ArmRecorder()
    run_skill(
        RunConfig(monitor_ordinal=1, arm_monitor=recorder, review_state="polling")
    )
    assert recorder.calls == 1


def test_t110_monitor_never_armed_at_l0():
    """T-110: `--monitor 0` NEVER arms the Monitor (zero-regression guard, AC-1)."""
    recorder = _ArmRecorder()
    result = run_skill(
        RunConfig(monitor_ordinal=0, arm_monitor=recorder, review_state="polling")
    )
    assert recorder.calls == 0
    # L0 FSM never leaves S0_IDLE.
    assert result.state == MonitorState.S0_IDLE


def test_t230_session_close_midpoll_is_resumable():
    """T-230: a mid-poll interruption is resumable via `--resume` (logging + resume only).

    Per FR-2.4 there is no code assertion beyond logging + resume: the Monitor is
    in-session ("session close = monitor lost"), and durability comes from the
    write-ahead JSONL run-log + `--resume`. Here we assert the mid-poll state is the
    recoverable polling state and that `--resume` is accepted; the run-log
    `session`-interruption record and the JSONL rebuild are covered in Phase 8.
    """
    mid_poll = run_skill(RunConfig(monitor_ordinal=1, review_state="polling"))
    assert mid_poll.state == MonitorState.S2_CLASSIFY  # armed, awaiting the review
    # `--resume` is a first-class flag the recovery path consumes.
    assert parse_args(["--resume", "/abs/monitor-run-42.jsonl"]).resume.endswith(
        ".jsonl"
    )
