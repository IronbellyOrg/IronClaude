"""G0, the ledger-and-time half (DESIGN 12.3): analysis/g0.py on the F-RUNS-RL fixture and on stubbed inputs.
The numbers come from analysis/analyze.py; this file checks that g0.py applies the two limits to them."""

import pytest
from analysis_support import fixture

from analysis import analyze as az
from analysis import g0


@pytest.fixture(scope="module")
def fx(tmp_path_factory):
    return fixture(tmp_path_factory)


def test_g0_on_fixture_ledger_passes_and_cost_fails(fx, capsys):
    res = g0.g0(fx.runs)
    # ledger_missing: 2 of 23 reviewer runs (one final, one repaired by the accepted re-ask) = 0.087, at most 0.10
    assert res["ledger_missing"]["count"] == 2 and res["ledger_missing"]["pass"]
    # luna cost: (96 - 80 - 4) / (51 / 14) = 3.294 s per row against the break-even (0.35 x 103 - 6) / 14 = 2.15 s
    cost = res["luna_cost_per_row"]
    assert cost["measured"] == pytest.approx(12 / (51 / 14))
    assert cost["breakeven"] == 2.15 and not cost["pass"]
    assert not res["pass"]
    assert g0.main(["--runs", str(fx.fx.runs), "--prefix", "stage1-"]) == 1
    assert "G0 (ledger and time): FAIL" in capsys.readouterr().out


def _stub(monkeypatch, rate_pass, measured, planned_be=2.07, measured_be=None):
    lm = {"count": 0, "rate": 0.0, "limit": 0.1, "pass": rate_pass}
    monkeypatch.setattr(az, "compliance", lambda dirs: {"ledger_missing": lm})
    monkeypatch.setattr(
        az,
        "time_table",
        lambda runs: {
            "luna_cost_per_row": {"planned": 2.0, "measured": measured},
            "breakeven_row_cost_14": {"planned": planned_be, "measured": measured_be},
        },
    )


@pytest.mark.parametrize(
    "rate_pass, measured, measured_be, want",
    [
        (
            True,
            2.0,
            None,
            True,
        ),  # under the planned break-even 2.07 when b was not measured
        (True, 2.07, None, True),  # at the break-even passes
        (True, 2.2, 2.3, True),  # the measured break-even is used when there is one
        (True, 2.2, None, False),  # over the planned break-even
        (False, 1.0, None, False),  # the ledger limit alone fails it
        (True, None, None, False),  # a cost nobody measured is not a pass
    ],
)
def test_g0_limits(monkeypatch, rate_pass, measured, measured_be, want):
    _stub(monkeypatch, rate_pass, measured, measured_be=measured_be)
    assert g0.g0([])["pass"] is want
