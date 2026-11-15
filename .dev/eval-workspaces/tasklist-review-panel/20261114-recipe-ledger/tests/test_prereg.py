"""REQ-41 (the per-class act bands are pre-registered) and REQ-44 (arms, run counts, the consistency definition and the
gates are written down before the first hold-out run): the record `analysis/analyze.py prereg` writes. Every test
writes to a temporary folder; the build never writes RL/config/prereg.json."""

import json
from pathlib import Path

import pytest

from analysis import analyze as az

RL = Path(__file__).resolve().parents[1]
CLASSES = [f"C{n}" for n in range(1, 9)]


def test_act_bands_for_all_classes(tmp_path):
    rec = az.prereg()
    assert set(rec["act_bands"]) == set(CLASSES)
    for cls in CLASSES:
        lo, hi = rec["act_bands"][cls]
        assert 0 <= lo < hi <= 1, cls
    # the defaults are the act ranges of DESIGN 12.2
    assert rec["act_bands"]["C1"] == [0.10, 0.30] and rec["act_bands"]["C4"] == [
        0.40,
        0.70,
    ]
    assert rec["act_bands"]["C3"] == [0.05, 0.20] and rec["act_bands"]["C8"] == [
        0.20,
        0.45,
    ]
    out = tmp_path / "prereg.json"
    assert az.main(["prereg", "--write", "--out", str(out)]) == 0
    written = json.loads(out.read_text(encoding="utf-8"))
    assert written["act_bands"] == rec["act_bands"]
    assert not (
        RL / "config" / "prereg.json"
    ).exists()  # the build writes no real record


def test_prereg_holds_arms_counts_consistency_and_gates():
    rec = az.prereg()
    assert rec["arms"]["stage1"] == ["Z0", "K", "RL"] and rec["arms"][
        "stage1_harness"
    ] == ["Z0-raw"]
    assert (
        rec["run_counts"]["stage1_panel_runs"],
        rec["run_counts"]["stage2_panel_runs"],
    ) == (75, 154)
    assert (
        rec["consistency"]["reach_at"] == 0.6
        and "3 of 5" in rec["consistency"]["definition"]
    )
    assert set(rec["gates"]) == {"G0", "D1", "D2", "D3", "D4", "D5", "D6", "D7"}
    assert (
        "blocking" in rec["gates"]["D6"]
        and "1.35" in rec["gates"]["D1"]
        and "0.12" in rec["gates"]["D2"]
    )


def test_owner_values_replace_bands(tmp_path):
    owner = tmp_path / "owner.json"
    owner.write_text(
        json.dumps({"act_bands": {"C2": [0.2, 0.4], "C6": [0.0, 0.5]}}),
        encoding="utf-8",
    )
    out = tmp_path / "p.json"
    assert (
        az.main(["prereg", "--write", "--owner-values", str(owner), "--out", str(out)])
        == 0
    )
    bands = json.loads(out.read_text(encoding="utf-8"))["act_bands"]
    assert bands["C2"] == [0.2, 0.4] and bands["C6"] == [0.0, 0.5]
    assert bands["C1"] == [0.10, 0.30]  # a class the owner leaves out keeps its default


@pytest.mark.parametrize("band", [[0.3, 0.3], [0.5, 0.2], [-0.1, 0.4], [0.2, 1.2]])
def test_invalid_owner_band_is_refused(tmp_path, band, capsys):
    owner = tmp_path / "owner.json"
    owner.write_text(json.dumps({"act_bands": {"C5": band}}), encoding="utf-8")
    out = tmp_path / "p.json"
    assert (
        az.main(["prereg", "--write", "--owner-values", str(owner), "--out", str(out)])
        == 2
    )
    assert "E_PREREG" in capsys.readouterr().err and not out.exists()
    with pytest.raises(ValueError):
        az.prereg({"act_bands": {"C5": band}})


def test_prereg_without_write_prints_only(tmp_path, capsys):
    assert az.main(["prereg"]) == 0
    assert json.loads(capsys.readouterr().out)["schema"] == "rl-prereg/1"
