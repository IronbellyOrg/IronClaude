"""py/summarize_arm.py (R-24, R-25, MR 4 rule 3)."""
import json
import sys

import pytest
from conftest import PY, pyrun

sys.path.insert(0, str(PY))
import summarize_arm as SA  # noqa: E402


def row(name, jac=0.3, ledger=10, wrong=1.0, echo=None, snap=0, reruns=0, mism=0, elapsed=100.0, slo=False, k=2,
        posted=0, delivered=(0, 0), planning=False):
    return {"row": name, "planning": planning, "wrong_blockers": wrong,
            "collab": {"own_line_jaccard": {"p": jac}, "echo_rate": {"p": echo}, "reruns": reruns, "rerun_mismatches": mism},
            "per_package": {"p": {"ledger_rows": ledger, "elapsed_s": elapsed, "slo_breach": slo, "snapshot_missing": snap,
                                  "receivers": 2, "k": k, "facts_posted": posted, "facts_harvested": 0,
                                  "facts_delivered": {"t4-1": delivered[0], "t3-1": delivered[1]}}}}


BASE = [row(f"a{i}") for i in range(4)]


def S(rows, base=BASE):
    return SA.summarize(rows, base)


def test_convergence_jaccard():
    s = S([row("x", jac=0.46)] + [row(f"r{i}") for i in range(11)])
    assert s["convergence_fires"] == ["x"]
    assert S([row("x", jac=0.45)] + [row(f"r{i}") for i in range(11)])["convergence_fires"] == []


def test_convergence_ledger_drop():
    assert S([row("x", ledger=7.9)] + [row(f"r{i}") for i in range(11)])["convergence_fires"] == ["x"]  # 21%
    assert S([row("x", ledger=8.1)] + [row(f"r{i}") for i in range(11)])["convergence_fires"] == []    # 19%


def test_independence_guard():
    two = [row(f"c{i}", jac=0.9) for i in range(2)] + [row(f"r{i}") for i in range(10)]
    three = [row(f"c{i}", jac=0.9) for i in range(3)] + [row(f"r{i}") for i in range(9)]
    assert S(two)["independence_guard_pass"] and not S(two)["fail"]
    assert not S(three)["independence_guard_pass"] and "independence_guard" in S(three)["reasons"]


def test_interim_stop_3_of_6():
    s = S([row(f"c{i}", jac=0.9) for i in range(3)] + [row(f"r{i}") for i in range(3)])
    assert s["stop"] and "convergence_interim" in s["reasons"]


def test_echo():
    assert S([row("x", echo=0.61)])["echo_alarms"] and not S([row("x", echo=0.60)])["echo_alarms"]


def test_snapshot():
    assert "snapshot" in S([row("x", snap=2), row("y", snap=1)])["reasons"]  # 3 of 4 receiver runs
    assert "snapshot" not in S([row("x", snap=1), row("y", snap=1)])["reasons"]


def test_rerun_mismatch_threshold():
    assert "rerun_mismatch" in S([row("x", reruns=100, mism=11)])["reasons"]
    assert "rerun_mismatch" not in S([row("x", reruns=100, mism=10)])["reasons"]


def test_slo_budget():
    rows = [row(f"r{i}") for i in range(10)]
    assert "slo_budget" in S(rows + [row("x", slo=True), row("y", slo=True)])["reasons"]
    assert "slo_budget" not in S(rows + [row("x", slo=True), row("y")])["reasons"]


def test_wrong_blockers():
    assert "wrong_blockers" in S([row("x", wrong=2.01)])["reasons"] and S([row("x", wrong=2.01)])["fail"]
    assert "wrong_blockers" not in S([row("x", wrong=2.0)])["reasons"]


def test_flood_reported_not_stop():
    s = S([row("x", posted=4, delivered=(0, 1))])
    assert s["flood"] and not s["stop"] and s["flood_runbook"]


def test_planning_rows_refused(tmp_path):
    with pytest.raises(ValueError):
        S([row("x", planning=True)])
    (tmp_path / "r.json").write_text(json.dumps(row("x", planning=True)))
    (tmp_path / "b.json").write_text(json.dumps(BASE[0]))
    r = pyrun("summarize_arm.py", "--rows", str(tmp_path / "r.json"), "--baseline-rows", str(tmp_path / "b.json"), "--out", str(tmp_path / "o.json"))
    assert r.returncode == 2
