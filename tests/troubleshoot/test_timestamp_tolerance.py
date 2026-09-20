"""T12 timestamp tolerance — R-14 A3/C5 acceptance test. Harness §3 T12."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from tests.troubleshoot._procedures import timestamp_ok

MTIME = datetime(2026, 9, 18, 18, 36, 0, tzinfo=timezone.utc)


@pytest.mark.parametrize(
    "delta,ok",
    [(299, True), (301, False)],
    ids=["+4m59s", "+5m01s"],
)
def test_timestamp_tolerance(delta: int, ok: bool) -> None:
    """R-14: +4m59s is in tolerance; +5m01s is not."""
    ts = (MTIME + timedelta(seconds=delta)).strftime("%Y-%m-%dT%H:%M:%SZ")
    assert timestamp_ok(ts, MTIME) is ok, ts


def test_midnight_always_fails() -> None:
    """R-14: T00:00:00Z always fails."""
    assert timestamp_ok("2026-09-19T00:00:00Z", MTIME) is False
