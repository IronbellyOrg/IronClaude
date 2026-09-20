"""T16 primitive differential — R-05 acceptance test. Harness §3 T16."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.troubleshoot._procedures import _section, differential_decision

FIX = Path(__file__).parent / "fixtures" / "procedures" / "differential" / "table.md"


@pytest.mark.parametrize(
    "section,expect",
    [
        ("substituted", {"cause_class": "substituted primitive"}),
        (
            "all-unobserved",
            {
                "comparator": "none",
                "headline": "UNDETERMINED — no comparator",
                "cap": 0.4,
            },
        ),
        (
            "single-env",
            {
                "comparator": "none",
                "headline": "UNDETERMINED — no comparator",
                "cap": 0.4,
            },
        ),
    ],
    ids=["substituted", "all-unobserved", "single-env"],
)
def test_differential_decision(section: str, expect: dict) -> None:
    """R-05: substituted primitive vs comparator=none cap 0.4."""
    table = FIX.read_text()
    got = differential_decision(_section(table, section))
    for k, v in expect.items():
        assert got[k] == v, (section, got, expect)
