"""REQ-38: recipes/README.md lists, per target type, what a maintainer must re-derive (DESIGN 11.3)."""

from helpers import SW

README = SW / "recipes" / "README.md"
ROWS = (
    "meaning of edits",
    "meaning of tests and gate",
    "meaning of source",
    "command dialect",
    "test and root-document paths",
    "severity guidance",
    "snapshot",
    "lens assignment",
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


def test_readme_says_the_extractor_sentences_do_not_apply():
    first = " ".join(README.read_text(encoding="utf-8").splitlines()[:4])
    assert "extractor sentences do not apply" in first
