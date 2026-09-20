"""T3 producers enumeration — R-02 acceptance test. Harness §3 T3."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.troubleshoot._procedures import (
    enumerate_producers,
    producer_rows,
    write_producers_md,
)

FIX = Path(__file__).parent / "fixtures" / "procedures" / "producers"


@pytest.mark.parametrize(
    "src,value,var,expect_unknown",
    [
        ("io.sh", "runner-unavailable", "rc", True),
        ("nonio.py", "DEAD_LETTER", "status", False),
    ],
    ids=["io", "nonio"],
)
def test_producers_md_header_columns_and_row_count(
    src: str, value: str, var: str, expect_unknown: bool, tmp_path: Path
) -> None:
    """R-02: producers.md header, 7 columns, rows==grep_hits, unknown flag."""
    text = (FIX / src).read_text()
    p = enumerate_producers({src: text}, value, var)
    md = write_producers_md(p, tmp_path / "producers.md")
    assert "observation-kind:" in md, md[:200]
    header = next(line for line in md.splitlines() if line.startswith("| line"))
    assert header.count("|") == 8, header
    assert producer_rows(md) == p.grep_hits, (producer_rows(md), p.grep_hits)
    assert p.count_unknown is expect_unknown, p.count_unknown
    assert "## Mechanism rows" not in md.split("## Producers", 1)[-1].split("|")[0]
    if src == "io.sh":
        assert p.grep_hits == 5, p.grep_hits
    for r in p.rows:
        r["surviving"] = "no"
    p.count_unknown = False
    reopened = write_producers_md(p, tmp_path / "reopened.md")
    assert reopened.count("surviving=re-opened") == len(p.rows), reopened
