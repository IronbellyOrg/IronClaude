"""REQ-38: cards/README.md lists, per target type, what a maintainer must re-derive."""

import re

from helpers import SW

README = SW / "cards" / "README.md"
ROWS = (
    "block patterns",
    "command dialect",
    "test and root-document paths",
    "severity guidance",
    "location of truth",
    "snapshot",
)
TARGETS = ("plan", "specification", "documentation")


def table():
    """{row name (lower-case): [cell per target type]} for the re-derive table; its header names the target types."""
    lines = [
        ln
        for ln in README.read_text(encoding="utf-8").splitlines()
        if ln.startswith("|")
    ]
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
    header = next(r for r in rows if r[0].lower() == "re-derive")
    assert [h.lower().split(" (")[0] for h in header[1:]] == list(TARGETS)
    return {r[0].lower(): r[1:] for r in rows if r is not header and len(r) == 4}


def test_readme_lists_rederive_rows():
    t = table()
    for row in ROWS:
        matches = [k for k in t if k.startswith(row)]
        assert len(matches) == 1, row
        cells = t[matches[0]]
        assert len(cells) == len(TARGETS)
        for target, cell in zip(TARGETS, cells):
            assert len(cell) >= 20, (row, target)
            assert cell.lower() != row, (row, target)
        assert len({c.lower() for c in cells}) == len(cells), row


def test_readme_footer_keeps_the_second_reader_open():
    text = README.read_text(encoding="utf-8")
    footer = text[text.index("## Open manual checks") :]
    assert re.search(r"second reader.*REQ-38.*OPEN", footer, re.S | re.I)
    assert "swap_test" in footer
    assert re.search(r"reader: _+\s+date: _+", footer)
