"""T3 producers enumeration — R-02 acceptance test. Harness §3 T3."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.troubleshoot._procedures import (
    enumerate_producers,
    menu_equal,
    producer_rows,
    surviving_yes,
    table_rows,
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
    """R-02: stable identities, eight columns, hit count and contradiction recovery."""
    text = (FIX / src).read_text()
    p = enumerate_producers({src: text}, value, var)
    md = write_producers_md(p, tmp_path / "producers.md")
    assert "observation-kind:" in md, md[:200]
    header = next(line for line in md.splitlines() if line.startswith("| id"))
    assert header.count("|") == 9, header
    assert [r[0] for r in table_rows(md)] == [
        f"P{i}" for i in range(1, p.grep_hits + 1)
    ]
    assert [r[2] for r in table_rows(md)] == [r["statement"] for r in p.rows]
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
    assert "producer-count: unknown" in reopened
    assert surviving_yes(reopened) == len(p.rows)
    assert menu_equal(reopened, reopened)
    assert [r[:2] for r in table_rows(reopened)] == [r[:2] for r in table_rows(md)]
    assert all(r["surviving"] == "no" for r in p.rows)
    assert write_producers_md(p, tmp_path / "reopened.md") == reopened
    assert (tmp_path / "reopened.md").read_text() == reopened


@pytest.mark.parametrize("cell", [r"a || b", r"a\|b", r"C:\work\\logs", "|edge|"])
def test_producer_cells_roundtrip(cell: str, tmp_path: Path) -> None:
    p = enumerate_producers({"b.sh": "rc=OK", "a.sh": "rc=OK\nrc=OK"}, "OK", "rc")
    assert [(r["id"], r["line"]) for r in p.rows] == [
        ("P1", "a.sh:1"),
        ("P2", "a.sh:2"),
        ("P3", "b.sh:1"),
    ]
    p.rows[0]["statement"] = cell
    p.rows[0]["exit_statement"] = cell
    md = write_producers_md(p, tmp_path / "producers.md")
    assert table_rows(md)[0][2:4] == [cell, cell]


def test_reopen_preserves_only_supplied_exclusion_evidence(tmp_path: Path) -> None:
    p = enumerate_producers({"a.sh": "rc=OK\nrc=OK"}, "OK", "rc")
    for row in p.rows:
        row["surviving"] = "no"
    p.rows[0]["exit_statement"] = "a.sh:9 observed return"
    md = write_producers_md(p, tmp_path / "producers.md")
    audit = md.split("## Contradiction audit", 1)[1]
    assert "P1 a.sh:1" in audit and "P2 a.sh:2" in audit
    assert "prior surviving=no" in audit
    assert "a.sh:9 observed return" in audit
    assert "prior exit statement=''" in audit
    assert table_rows(md)[0][3] == "a.sh:9 observed return"
