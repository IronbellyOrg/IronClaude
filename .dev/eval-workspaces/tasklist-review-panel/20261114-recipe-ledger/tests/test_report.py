"""REQ-31 (the break-even row cost of DESIGN 10.2, and the report that prints it next to the measured values), REQ-40
(three shares, never summed) and REQ-45 (the claim sentence), on the report that analysis/analyze.py writes for the
F-RUNS-RL fixture."""

import re
from pathlib import Path

import pytest
from analysis_support import fixture

from analysis import analyze as az
from rl import lens
from scaffold import clock

TESTING = Path(__file__).resolve().parents[1] / "TESTING.md"
REQ45 = (
    "raises the per-run found fraction; consistency is expected only for I4 and I7 (classes C4 and C8), "
    "and only for Redesign 1 at the high end of its range"
)
SHARE_LABELS = ("Z0 - Z0raw", "K - Z0", "RL - Z0")
SHARE_NAMES = ("H share", "prompting share", "redesign share")


@pytest.fixture(scope="module")
def report(tmp_path_factory):
    return az.build_report(fixture(tmp_path_factory).metrics)


@pytest.mark.parametrize(
    ("b", "rows", "expected"),
    [
        (100, 14, 2.07),
        (100, 12, 2.42),
        (120, 14, 2.57),
        (122, 14, 2.62),
        (116, 14, 2.47),
    ],
)
def test_breakeven_values(b, rows, expected):
    assert clock.breakeven_row_cost(b, rows) == expected
    assert clock.breakeven_row_cost(b=b, rows=rows) == expected


def test_breakeven_agrees_with_the_row_cap():
    # at b 100 the budget left for rows is 0.35 * 100 - 6 = 29 s: 14 rows fit at 2.07 s, 12 rows at 2.41 s
    assert lens.lens_row_cap(100, 2.07, 14) == 14
    assert lens.lens_row_cap(100, 2.41, 14) == 12
    assert clock.lens_row_cap is lens.lens_row_cap


def table_row(report, quantity):
    """The cells of the row of the time table whose first cell starts with `quantity`."""
    for ln in report.splitlines():
        if ln.startswith(f"| {quantity}"):
            return [c.strip() for c in ln.strip("|").split("|")]
    raise AssertionError(f"no row {quantity!r}")


def test_report_shows_planned_and_measured(report):
    assert "## Time: planned and measured (REQ-31)" in report
    assert "| quantity | planned | measured |" in report
    # planned from values.json, measured from the fixture runs (Z0 slowest reviewer 103 s on doc-a, luna 96 s against 80 s)
    be = table_row(report, "break-even row cost")
    assert be[1:] == [
        f"{clock.breakeven_row_cost(100, 14):.2f}",
        f"{clock.breakeven_row_cost(103, 14):.2f}",
    ]
    assert be[1:] == ["2.07", "2.15"]
    assert table_row(report, "luna cost per row")[1:] == ["2.00", "3.29"]
    assert table_row(report, "b,")[1:] == ["100.0", "103.0"]
    assert table_row(report, "luna row cap")[1:] == [
        "14",
        "9",
    ]  # floor((0.35 x 103 - 6) / 3.294)


def test_three_shares_separate(report):
    lines = [ln for ln in report.splitlines() if any(lab in ln for lab in SHARE_LABELS)]
    assert len(lines) == 3
    for ln, label, name in zip(lines, SHARE_LABELS, SHARE_NAMES, strict=True):
        assert label in ln and ln.startswith(name)
        assert [lab for lab in SHARE_LABELS if lab in ln] == [label]
    values = [float(re.search(r"([+-]\d\.\d+)$", ln).group(1)) for ln in lines]
    assert values == [
        pytest.approx(0.117, abs=5e-4),
        pytest.approx(0.092, abs=5e-4),
        pytest.approx(0.292, abs=5e-4),
    ]


def test_no_summed_headline(report):
    shares = list(zip(SHARE_NAMES, SHARE_LABELS, strict=True))
    for ln in report.splitlines():
        named = [s for s in shares if s[0] in ln or s[1] in ln]
        assert len(named) <= 1, ln  # no line holds the name or label of two shares
        if named:
            assert "+ " not in ln and "total" not in ln.lower() and " and " not in ln, (
                ln
            )
    assert "total" not in report.lower()
    headline = report.split("## Decision")[1].split("##")[0]
    assert not any(n in headline for n in (*SHARE_NAMES, *SHARE_LABELS))


def test_claim_template_text(report):
    assert az.CLAIM == REQ45
    assert REQ45 in TESTING.read_text(
        encoding="utf-8"
    )  # the sentence of REQ-45 as the test document words it
    claims = [ln for ln in report.splitlines() if REQ45 in ln]
    assert claims == [f"Claim: {REQ45}."]
    for ln in report.splitlines():
        if re.search(r"consisten", ln, re.I) and ln not in claims:
            assert not re.search(r"\bC[1-8]\b|\bI\d\b", ln), (
                ln
            )  # no other sentence calls a class consistent
