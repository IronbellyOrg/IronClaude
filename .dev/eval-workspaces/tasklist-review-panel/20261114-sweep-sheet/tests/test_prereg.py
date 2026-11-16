"""REQ-41, REQ-44: the pre-registration record (arms, run counts, consistency definition, gates, floor, per-class act bands)."""

import json

import pytest

from analysis import analyze

CLASSES = [f"C{n}" for n in range(1, 9)]


def test_act_bands_for_all_classes():
    rec = analyze.prereg()
    assert sorted(rec["act_bands"]) == CLASSES
    for c, (lo, hi) in rec["act_bands"].items():
        assert 0 <= lo < hi <= 1, c
    # DESIGN 15.1 decision 2, written out here so the code cannot grade itself
    assert rec["act_bands"]["C3"] == [0.03, 0.15] and rec["act_bands"]["C4"] == [
        0.50,
        0.75,
    ]
    assert rec["owner_confirmed"] is False and "not confirmed" in rec["source"]
    assert rec["selection_recall_floor"] == 0.45


def test_owner_values_replace_defaults_and_are_validated(tmp_path):
    rec = analyze.prereg(
        {
            "selection_recall_floor": 0.5,
            "act_bands": {"C3": [0.02, 0.2]},
            "ground_truth_sha256": {"HO-1": "ab" * 32},
        }
    )
    assert rec["act_bands"]["C3"] == [0.02, 0.2] and rec["act_bands"]["C1"] == [
        0.10,
        0.40,
    ]
    assert rec["selection_recall_floor"] == 0.5 and rec["ground_truth_sha256"] == {
        "HO-1": "ab" * 32
    }
    assert rec["owner_confirmed"] is True and rec["source"] == "owner values"
    for bad in ([0.3, 0.3], [0.4, 0.2], [0.1, 1.2], [-0.1, 0.5], [0.1]):
        with pytest.raises(analyze.AnalysisError, match="C3"):
            analyze.prereg({"act_bands": {"C3": bad}})
    with pytest.raises(analyze.AnalysisError, match="exactly"):
        analyze.prereg({"act_bands": {"C9": [0.1, 0.2]}})


def test_record_names_arms_run_counts_consistency_and_gates():
    rec = analyze.prereg()
    assert rec["arms"] == ["Z0-raw", "Z0", "K", "SS"]
    assert rec["stage1_runs"] == {"panel_runs": 75, "arms_z0_k_ss": 60, "z0_raw": 15}
    assert rec["consistency"] == {"reach_at_least": 0.6, "of_runs": "3 of 5"}
    lim = rec["gates"]["limits"]
    assert (lim["d1_median_ratio"], lim["d2_effect"], lim["d3_consistent_items"]) == (
        1.35,
        0.12,
        3,
    )
    assert (
        lim["d4_wrong_blockers"],
        lim["d4_twin_blocking"],
        lim["d6_within"],
        lim["d7_gain"],
    ) == (1.0, 0.7, 0.1, 0.04)
    assert rec["gates"]["blocking"] == ["D6"]


def test_command_writes_only_under_sw_or_tmp(tmp_path, capsys):
    owner = tmp_path / "owner.json"
    owner.write_text(json.dumps({"selection_recall_floor": 0.4}))
    out = tmp_path / "config" / "prereg.json"
    rc = analyze.main(
        ["prereg", "--write", "--owner-values", str(owner), "--out", str(out)]
    )
    assert rc == 0 and json.loads(out.read_text())["selection_recall_floor"] == 0.4
    assert out.read_text().endswith("\n")
    # without --write the record is printed and nothing is written
    capsys.readouterr()
    assert analyze.main(["prereg", "--out", str(tmp_path / "never.json")]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["schema"] == "sweep-prereg/1" and printed["owner_confirmed"] is False
    assert not (tmp_path / "never.json").exists()
    assert (
        analyze.main(["prereg", "--write", "--out", "/var/tmp/sw-prereg-refused.json"])
        == 1
    )
