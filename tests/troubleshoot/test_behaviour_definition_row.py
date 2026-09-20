"""T18 behaviour-definition row — R-09 acceptance test. Harness §3 T18."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.troubleshoot._assertions import CalibratorInputs, evaluate_calibrator
from tests.troubleshoot._procedures import behaviour_row

FIX = Path(__file__).parent / "fixtures" / "procedures" / "behaviour"


@pytest.mark.parametrize(
    "name,expect",
    [
        ("fetched", {"query_ok": True, "order_ok": True}),
        ("recalled", {"probe_row_appended": True}),
        ("missing", {"c8_cap": 0.5}),
    ],
    ids=["fetched", "recalled", "missing"],
)
def test_behaviour_row(name: str, expect: dict) -> None:
    """R-09: row before fetch; recalled appends; missing fires C8 cap."""
    text = (FIX / f"{name}.md").read_text()
    log = ["write-row", "fetch"] if name != "missing" else ["fetch"]
    got = behaviour_row(text, log)
    for k, v in expect.items():
        assert got.get(k) == v, (name, got)
    if name == "missing":
        result = evaluate_calibrator(
            CalibratorInputs(
                card="behaviour-definition: row 1\n",
                behaviour_text=text,
            )
        )
        assert "behaviour-cite: missing" in result.flags, result.flags
        assert result.cap == 0.5, result.cap
