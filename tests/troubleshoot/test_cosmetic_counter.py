"""T8 cosmetic counter — R-08 acceptance test. Harness §3 T8."""

from __future__ import annotations

from pathlib import Path

from tests.troubleshoot._procedures import cosmetic_counter

FIX = Path(__file__).parent / "fixtures" / "counters" / "cosmetic-log.txt"


def test_cosmetic_counter_fires_exempts_and_resets() -> None:
    """R-08: fires at 5, 14, 19; exempts ls/Write/job-log; resets on source Read."""
    lines = [ln for ln in FIX.read_text().splitlines() if ln.strip()]
    assert cosmetic_counter(lines, "out/") == [5, 14, 19], lines
