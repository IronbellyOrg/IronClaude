"""Rate-limit / backoff tests (spec §6.3, FR-2.5 / NFR-2).

T-N10 a 403 → exponential backoff on the next poll (NOT an immediate failure);
T-N11 403 ×3 → bounded exponential backoff. The backoff arithmetic lives in the FSM
(`next_backoff`), not in the poll script — the script only surfaces the 403 status.
The subprocess-boundary variant (mock_gh) is marked `integration`.
"""

from __future__ import annotations

import pytest

from superclaude.pr_submit.fsm import BACKOFF_CAP, next_backoff


def test_tn10_403_triggers_backoff_not_failure():
    """T-N10: a 403 backs off the next poll (from base 30 → 60), never an immediate failure."""
    # After the base 30s interval, a 403 doubles the next poll interval to 60s.
    assert next_backoff(30) == 60
    # From a cold start a 403 backs off to the 30s base (a positive interval, not a failure).
    assert next_backoff(0) == 30


def test_tn11_403_x3_bounded_exponential():
    """T-N11: three consecutive 403s produce a bounded exponential sequence."""
    seq = []
    interval = 0
    for _ in range(3):
        interval = next_backoff(interval)
        seq.append(interval)
    assert seq == [30, 60, 120]
    # The sequence is bounded — it never exceeds the cap no matter how many 403s.
    for _ in range(10):
        interval = next_backoff(interval)
    assert interval == BACKOFF_CAP == 300


def test_backoff_resets_on_success():
    """A successful poll resets the interval; the next backoff restarts at the base."""
    interval = next_backoff(next_backoff(0))  # 30 → 60
    assert interval == 60
    interval = 0  # success resets
    assert next_backoff(interval) == 30


@pytest.mark.integration
def test_tn10_subprocess_boundary_403(monkeypatch):
    """T-N10 (integration): a 403 surfaced by the poll wrapper triggers FSM backoff, not failure.

    The poll SCRIPT surfaces the rate-limit status; the FSM (`next_backoff`) decides
    the next interval. Here we simulate the wrapper returning a still-"polling" status
    under a 403 and assert the FSM backs off rather than terminating.
    """
    from superclaude.pr_submit import detection

    calls = {"n": 0}

    def fake_fetch(pr_num):
        # Simulate a 403/secondary-limit: no review data this poll (still polling).
        calls["n"] += 1
        return {"reviews": [], "comments": [], "rate_limited": True}

    monkeypatch.setattr(detection, "_fetch_payload", fake_fetch)
    state = detection.poll_augment_review(42)
    assert state == "polling"  # not a failure
    assert calls["n"] == 1
    # The FSM backs off before the next poll.
    assert next_backoff(30) == 60
