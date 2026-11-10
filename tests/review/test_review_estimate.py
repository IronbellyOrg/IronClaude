"""Tests for the capture-recapture estimators (PN3).

All expected values are hand-computed from the formulas in the plan.
"""

from __future__ import annotations

import json
import math

import pytest
from click.testing import CliRunner

from superclaude.cli.review import estimate as est
from superclaude.cli.review.estimate_cmd import command


def rows(*sets):
    return [frozenset(s) for s in sets]


# --- hand-computed matrices -------------------------------------------------

# M1: k=2. A={1,2}, B={1}, C={2}, D={1}
M1 = rows({1, 2}, {1}, {2}, {1})
# M2: k=3, three defects each captured once by a different occasion (Q2 = 0)
M2 = rows({1}, {2}, {3})
# M3: k=3, four defects captured by every occasion
M3 = rows({1, 2, 3}, {1, 2, 3}, {1, 2, 3}, {1, 2, 3})
# M4: k=2, disjoint
M4 = rows({1}, {2})
# M5: k=4 mixed
M5 = rows({1, 2, 3, 4}, {1, 2}, {3}, {4}, {1}, {2, 3})


def test_counts_m1():
    c = est.counts(M1, 2)
    assert c["S_obs"] == 4
    assert c["Q"] == {1: 3, 2: 1}
    assert c["q"] == {1: 2, 2: 1}


def test_chapman_m1():
    r = est.estimate_matrix(M1, 2)
    assert r["chapman"]["N"] == pytest.approx(5.0)
    assert r["chapman"]["var"] == pytest.approx(2.0)
    lo, hi = r["chapman"]["ci95"]
    assert lo == pytest.approx(max(4.0, 5 - 1.96 * math.sqrt(2)))
    assert hi == pytest.approx(5 + 1.96 * math.sqrt(2))


def test_chao2_m1():
    r = est.estimate_matrix(M1, 2)
    c = r["chao2"]
    assert c["f0"] == pytest.approx(2.25)
    assert c["N"] == pytest.approx(6.25)
    assert c["var"] == pytest.approx(14.0625)
    cfac = math.exp(1.96 * math.sqrt(math.log(1 + 14.0625 / 2.25**2)))
    assert c["ci95"][0] == pytest.approx(4 + 2.25 / cfac, abs=1e-5)
    assert c["ci95"][1] == pytest.approx(4 + 2.25 * cfac, abs=1e-5)


def test_jackknife_m1():
    r = est.estimate_matrix(M1, 2)
    assert r["jackknife1"]["N"] == pytest.approx(5.5)
    assert r["jackknife1"]["var"] == pytest.approx(0.25)
    lo, hi = r["jackknife1"]["ci95"]
    assert lo == pytest.approx(5.5 - 1.96 * 0.5)
    assert hi == pytest.approx(5.5 + 1.96 * 0.5)
    assert r["jackknife2"]["N"] == pytest.approx(5.5)


def test_q2_zero_m2():
    r = est.estimate_matrix(M2, 3)
    assert r["S_obs"] == 3
    assert r["Q"] == {"1": 3, "2": 0, "3": 0}
    assert r["chapman"] is None
    c = r["chao2"]
    assert c["f0"] == pytest.approx(2.0)
    assert c["N"] == pytest.approx(5.0)
    assert c["var"] == pytest.approx(2 + (4 / 9) * 3 * 25 / 4 - (4 / 9) * 81 / 20)
    assert r["jackknife1"]["N"] == pytest.approx(5.0)
    assert r["jackknife1"]["var"] == pytest.approx(0.0)
    assert r["jackknife1"]["ci95"] == [3.0 + 2.0, 3.0 + 2.0] or r["jackknife1"]["ci95"][
        0
    ] == pytest.approx(5.0)
    assert r["jackknife2"]["N"] == pytest.approx(6.0)
    assert r["stop"] is False


def test_all_captured_by_every_occasion_m3():
    r = est.estimate_matrix(M3, 3)
    assert r["S_obs"] == 4
    assert r["chao2"]["N"] == pytest.approx(4.0)
    assert r["chao2"]["ci95"] == [4.0, 4.0]
    assert r["jackknife1"]["N"] == pytest.approx(4.0)
    assert r["jackknife2"]["N"] == pytest.approx(4.0)
    assert r["unseen_upper95"] == pytest.approx(0.0)
    assert r["stop"] is True
    assert r["reason"] == "estimated remainder below 1 and no open blocking"


def test_k2_disjoint_m4():
    r = est.estimate_matrix(M4, 2)
    assert r["chapman"]["N"] == pytest.approx(3.0)
    assert r["chapman"]["var"] == pytest.approx(2.0)
    assert r["chao2"]["f0"] == pytest.approx(0.5)
    assert r["chao2"]["N"] == pytest.approx(2.5)
    assert r["jackknife1"]["N"] == pytest.approx(3.0)


def test_k4_mixed_m5():
    r = est.estimate_matrix(M5, 4)
    assert r["S_obs"] == 6
    assert r["Q"] == {"1": 3, "2": 2, "3": 0, "4": 1}
    assert r["chao2"]["f0"] == pytest.approx(1.6875)
    assert r["chao2"]["N"] == pytest.approx(7.6875)
    assert r["chao2"]["var"] == pytest.approx(6.908203125)
    assert r["jackknife1"]["N"] == pytest.approx(8.25)
    assert r["jackknife1"]["var"] == pytest.approx(0.5625)
    assert r["jackknife2"]["N"] == pytest.approx(6 + 3.75 - 2 * 4 / 12)
    assert r["chapman"] is None


def test_empty_capture():
    r = est.estimate_matrix([], 2)
    assert r["S_obs"] == 0
    assert r["chapman"]["N"] == pytest.approx(0.0)
    assert r["chao2"]["N"] == pytest.approx(0.0)
    assert r["jackknife1"]["N"] == pytest.approx(0.0)
    assert r["unseen_upper95"] == pytest.approx(0.0)
    assert r["stop"] is True


def test_unseen_upper95_is_max_of_chao2_and_jack1():
    r = est.estimate_matrix(M5, 4)
    up = max(r["chao2"]["ci95"][1], r["jackknife1"]["ci95"][1]) - r["S_obs"]
    assert r["unseen_upper95"] == pytest.approx(up, abs=1e-5)


def test_stop_rule_open_blocking():
    r = est.estimate_matrix(M3, 3, open_blocking=2)
    assert r["stop"] is False
    assert "open blocking" in r["reason"]


def test_stop_false_when_unseen_large():
    r = est.estimate_matrix(M2, 3)
    assert r["stop"] is False
    assert r["unseen_upper95"] >= 1.0
    assert "unseen" in r["reason"]


def test_k_less_than_two_is_null():
    r = est.estimate_matrix(rows({1}), 1)
    assert r["stop"] is None
    assert r["reason"] == "insufficient occasions"


def test_determinism():
    a = json.dumps(est.estimate_matrix(M5, 4), sort_keys=True)
    b = json.dumps(est.estimate_matrix(list(reversed(M5)), 4), sort_keys=True)
    assert a == b


def test_stop_rule_text_exposed():
    assert "unseen_upper95 < 1.0" in est.RULE
    assert est.estimate_matrix(M3, 3)["rule"] == est.RULE


# --- capture file -----------------------------------------------------------


def capture(defects, occasions=("a", "b", "c")):
    return {
        "schema": "review-capture/1",
        "source": "t",
        "round": 1,
        "doc_sha256": "x",
        "occasions": list(occasions),
        "defects": defects,
    }


def test_from_capture_blocking_only():
    cap = capture(
        [
            {"key": "D1", "blocking": True, "captured_by": ["a", "b"]},
            {"key": "D2", "blocking": False, "captured_by": ["a"]},
            {"key": "D3", "blocking": True, "captured_by": ["c"]},
        ]
    )
    r_all = est.estimate_capture(cap)
    r_blk = est.estimate_capture(cap, blocking_only=True)
    assert r_all["S_obs"] == 3
    assert r_blk["S_obs"] == 2
    assert r_blk["k"] == 3
    assert r_blk["Q"]["1"] == 1 and r_blk["Q"]["2"] == 1


def test_defect_with_no_capture_is_ignored():
    cap = capture([{"key": "D1", "blocking": True, "captured_by": []}])
    assert est.estimate_capture(cap)["S_obs"] == 0


@pytest.mark.parametrize(
    "mutate",
    [
        lambda c: c.update(schema="nope"),
        lambda c: c.update(occasions=[]),
        lambda c: c.update(occasions=["a", "a"]),
        lambda c: c.update(defects="x"),
        lambda c: c["defects"].append(
            {"key": "D1", "blocking": True, "captured_by": ["zz"]}
        ),
        lambda c: c["defects"].append(
            {"key": "D1", "blocking": "yes", "captured_by": ["a"]}
        ),
        lambda c: c["defects"].append(
            {"key": "D1", "blocking": True, "captured_by": ["a"]}
        ),
        lambda c: c["defects"].append({"blocking": True, "captured_by": ["a"]}),
    ],
)
def test_invalid_capture_raises(mutate):
    cap = capture([{"key": "D1", "blocking": True, "captured_by": ["a"]}])
    mutate(cap)
    with pytest.raises(est.CaptureError):
        est.estimate_capture(cap)


# --- CLI --------------------------------------------------------------------


def write(tmp_path, obj, name="cap.json"):
    p = tmp_path / name
    p.write_text(obj if isinstance(obj, str) else json.dumps(obj))
    return str(p)


def test_cli_output(tmp_path):
    cap = capture(
        [
            {"key": "D1", "blocking": True, "captured_by": ["a", "b", "c"]},
            {"key": "D2", "blocking": True, "captured_by": ["a"]},
            {"key": "D3", "blocking": False, "captured_by": ["b"]},
        ]
    )
    res = CliRunner().invoke(command, [write(tmp_path, cap), "--blocking-only"])
    assert res.exit_code == 0, res.output
    out = json.loads(res.output)
    assert out["schema"] == "review-estimate/1"
    assert out["k"] == 3
    assert out["S_obs"] == 2
    for key in (
        "Q",
        "chapman",
        "chao2",
        "jackknife1",
        "jackknife2",
        "unseen_upper95",
        "stop",
        "reason",
        "rule",
    ):
        assert key in out
    assert out["chapman"] is None
    assert set(out["chao2"]) == {"N", "f0", "var", "ci95"}


def test_cli_k2_has_chapman_and_open_blocking(tmp_path):
    cap = capture(
        [{"key": "D1", "blocking": True, "captured_by": ["a", "b"]}],
        occasions=("a", "b"),
    )
    res = CliRunner().invoke(command, [write(tmp_path, cap), "--open-blocking", "1"])
    out = json.loads(res.output)
    assert res.exit_code == 0
    assert out["chapman"]["N"] == pytest.approx(1.0)
    assert out["stop"] is False


def test_cli_deterministic(tmp_path):
    cap = capture([{"key": "D1", "blocking": True, "captured_by": ["a", "c"]}])
    p = write(tmp_path, cap)
    a = CliRunner().invoke(command, [p]).output
    b = CliRunner().invoke(command, [p]).output
    assert a == b


@pytest.mark.parametrize("content", ["not json", "[]", json.dumps({"schema": "x"})])
def test_cli_invalid_exit_2(tmp_path, content):
    res = CliRunner().invoke(command, [write(tmp_path, content)])
    assert res.exit_code == 2


def test_cli_missing_file_exit_2(tmp_path):
    res = CliRunner().invoke(command, [str(tmp_path / "nope.json")])
    assert res.exit_code == 2


def test_registered_under_review_group():
    from superclaude.cli.main import main

    res = CliRunner().invoke(main, ["review", "estimate", "--help"])
    assert res.exit_code == 0
    assert "CAPTURE" in res.output.upper()
