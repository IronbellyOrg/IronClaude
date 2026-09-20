"""T17 discriminator rows — R-04 acceptance test. Harness §3 T17."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.troubleshoot._procedures import (
    check_rows,
    enumerate_producers,
    write_producers_md,
)

FIX = Path(__file__).parent / "fixtures" / "procedures" / "rows"
PRODUCERS = """## Producers
| id | line | statement | exit statement | marker | walltime | observable | surviving |
|---|---|---|---|---|---|---|---|
| P1 | a.sh:1 | x | return | before | yes | y | surviving=yes |
"""


@pytest.mark.parametrize(
    "name,expect",
    [
        (
            "distinguishing",
            {
                "invalid": False,
                "control": True,
                "distinguishing": True,
                "verdict": "partial",
            },
        ),
        ("indistinguishable", {"invalid": False}),
        ("exact-only", {"invalid": True}),
        ("overflow", {"invalid": False}),
    ],
    ids=["distinguishing", "indistinguishable", "exact-only", "overflow"],
)
def test_discriminator_rows(name: str, expect: dict) -> None:
    """R-04: pair completeness, distinguishing/indistinguishable, overflow truncation."""
    md = (FIX / f"{name}.md").read_text()
    got = check_rows(md, PRODUCERS)
    for k, v in expect.items():
        assert got[k] == v, (name, k, got)
    if name == "indistinguishable":
        assert "indistinguishable" in md
    if name == "overflow":
        assert got["truncated"] == "1", got


def test_reopened_producers_require_discriminator_pairs(tmp_path: Path) -> None:
    p = enumerate_producers({"a.sh": "rc=OK"}, "OK", "rc")
    p.rows[0]["surviving"] = "no"
    md = write_producers_md(p, tmp_path / "producers.md")
    assert check_rows("indistinguishable: P1", md)["invalid"]
