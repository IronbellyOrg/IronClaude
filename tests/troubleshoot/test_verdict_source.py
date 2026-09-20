"""T5b verdict source — R-01 acceptance test. Harness §3 T5b."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.troubleshoot._procedures import verdict_from_log

FIX = Path(__file__).parent / "fixtures" / "procedures" / "verdict-source"


def verdict_is_fail(v: str) -> bool:
    return v != "PASS"


@pytest.mark.parametrize(
    "log,expect",
    [
        ("marker.log", "FAIL"),
        ("no-marker.log", "unobservable"),
        ("conclusion-only.log", "unobservable"),
    ],
    ids=["marker", "no-marker", "conclusion-only"],
)
def test_verdict_from_log(log: str, expect: str) -> None:
    """R-01: last RESULT marker wins; conclusion: is never a source."""
    text = (FIX / log).read_text()
    got = verdict_from_log(text)
    assert got == expect, got
    if expect == "unobservable":
        assert verdict_is_fail(got)
    assert not (got == "PASS" and "conclusion:" in text)
