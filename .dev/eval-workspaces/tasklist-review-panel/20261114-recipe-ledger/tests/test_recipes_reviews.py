"""REQ-08: recipes/REVIEWS.md holds one row per recipe; the completeness test needs a person and is not run by the build."""

import pytest
from helpers import SW

REVIEWS = SW / "recipes" / "REVIEWS.md"


def rows():
    """[(recipe, status, reviewer, date)] of the table rows of REVIEWS.md."""
    cells = [
        [c.strip() for c in ln.strip().strip("|").split("|")]
        for ln in REVIEWS.read_text(encoding="utf-8").splitlines()
        if ln.startswith("| C")
    ]
    assert all(len(c) == 4 for c in cells)
    return [tuple(c) for c in cells]


def test_review_record_has_one_row_per_recipe():
    got = rows()
    assert [r[0] for r in got] == [f"C{n}" for n in range(1, 9)]
    assert {r[1] for r in got} <= {"OPEN", "DONE"}


@pytest.mark.freeze
def test_review_record_complete():
    """Written, not run by the build: 8 rows, none with an empty reviewer or date."""
    got = rows()
    assert len(got) == 8
    assert all(
        status == "DONE" and reviewer and date for _, status, reviewer, date in got
    )
