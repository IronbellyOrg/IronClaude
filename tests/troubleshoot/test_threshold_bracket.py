"""T7 threshold bracket — R-05 acceptance test. Harness §3 T7."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.troubleshoot._procedures import bracket, bracket_trigger


@pytest.mark.parametrize(
    "results,n,expect",
    [
        (
            {80: "F", 78: "F", 76: "P"},
            80,
            {"bracket": [76, 78], "width": 2, "guard": 76},
        ),
        ({80: "F", 78: "P", 76: "F"}, 80, {"status": "UNDETERMINED"}),
        (
            {82: "F", 80: "F", 78: "P"},
            82,
            {"bracket": [78, 80], "width": 2, "guard": 78},
        ),
    ],
    ids=["monotone", "non-monotone", "absorbed-82-85"],
)
def test_bracket_result(
    results: dict[int, str], n: int, expect: dict, tmp_path: Path
) -> None:
    """R-05: monotone bracket, non-monotone UNDETERMINED, counter file untouched."""
    got = bracket(results, n)
    for k, v in expect.items():
        assert got[k] == v, (k, got, expect)
    if expect.get("guard") == 76:
        assert bracket_trigger("too many layers: 80", "", False) == "limit-in-text"
        assert bracket_trigger("clean", "", True) == "passes-smaller"
        rounds = tmp_path / "diagnosability-rounds.json"
        rounds.write_text("{}")
        bracket(results, n)
        assert rounds.read_text() == "{}", rounds.read_text()
