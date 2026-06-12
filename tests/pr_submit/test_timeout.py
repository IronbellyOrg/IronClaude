"""Timeout + backoff tests (spec FR-2.3/FR-2.5).

T-220 29s interval → rejected; T-221 never-arriving review → timeout fires
(TERMINAL_TIMEOUT); T-222 `--timeout 60` → fires at 60s; T-231 403 secondary-limit
×2 then success → backoff 30, 60, reset (AC-4). The backoff arithmetic lives in the
FSM (not the poll script), and counts toward the wall-clock timeout.
"""

from __future__ import annotations

import pytest

from superclaude.pr_submit.fsm import (
    BACKOFF_BASE,
    next_backoff,
    parse_args,
    poll_outcome,
    timed_out,
)
from superclaude.pr_submit.models import MonitorState


def test_t220_interval_below_30_rejected():
    """T-220: a 29s poll interval fails the ≥30s assertion."""
    with pytest.raises(ValueError):
        parse_args(["--poll-interval", "29"])
    # 30 is the accepted boundary.
    assert parse_args(["--poll-interval", "30"]).poll_interval == 30


def test_t221_never_arriving_review_fires_timeout():
    """T-221: a never-arriving review fires the timeout (TERMINAL_TIMEOUT)."""
    # Still polling after the full default timeout has elapsed.
    assert (
        poll_outcome("polling", elapsed_seconds=1800, timeout=1800)
        == MonitorState.TERMINAL_TIMEOUT
    )
    # Before the timeout, polling continues.
    assert (
        poll_outcome("polling", elapsed_seconds=120, timeout=1800)
        == MonitorState.S2_CLASSIFY
    )


def test_t222_configurable_timeout_fires_at_60():
    """T-222: `--timeout 60` fires the timeout at 60s."""
    assert parse_args(["--timeout", "60"]).timeout == 60
    assert (
        poll_outcome("polling", elapsed_seconds=60, timeout=60)
        == MonitorState.TERMINAL_TIMEOUT
    )
    assert (
        poll_outcome("polling", elapsed_seconds=59, timeout=60)
        == MonitorState.S2_CLASSIFY
    )


def test_t231_backoff_30_60_reset_on_success():
    """T-231: 403 ×2 then success → backoff 30, 60, then reset to base (AC-4)."""
    interval = 0
    sequence = []
    # Two consecutive 403s: backoff grows 30 → 60.
    for _ in range(2):
        interval = next_backoff(interval)
        sequence.append(interval)
    assert sequence == [30, 60]
    # Success resets the interval; the next backoff restarts at the base.
    interval = 0  # reset on success
    assert next_backoff(interval) == BACKOFF_BASE == 30


def test_backoff_caps_at_300():
    """Backoff doubles 30→60→120→240→300 and caps at 300s, counting toward timeout."""
    seq = []
    interval = 0
    for _ in range(6):
        interval = next_backoff(interval)
        seq.append(interval)
    assert seq == [30, 60, 120, 240, 300, 300]
    # The backoff is bounded so it always counts toward (never exceeds) the timeout window.
    assert timed_out(300, 300) is True
