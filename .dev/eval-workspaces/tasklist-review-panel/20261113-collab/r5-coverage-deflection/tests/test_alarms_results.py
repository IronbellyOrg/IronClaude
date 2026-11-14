"""T-16 alarms (R-24, R-25, R-40, R-45) and T-17 results row (MR:22, MR:955)."""
import json

from conftest import AL, CT, DS
from r5 import alarms, results

REF = {"own_line_jaccard": 0.30, "ledger_rows": 10, "union_anchored_tasks": 8}


def test_convergence_own_lines_only():
    # peer-tagged lines raise the all-line Jaccard, but only the own-line value is passed in
    assert alarms.convergence(0.44, 10, REF) is False
    assert alarms.convergence(0.46, 10, REF) is True
    assert alarms.convergence(0.30, 7.9, REF) is True  # 21% below
    assert alarms.convergence(0.30, 8, REF) is False
    assert alarms.convergence(0.9, 1, None) is None


def test_deflection():
    assert alarms.deflection(0.51, 9, REF) is True
    assert alarms.deflection(0.50, 9, REF) is False
    assert alarms.deflection(0.10, 7, REF) is True


def test_snapshot_slo_drift():
    assert alarms.snapshot([1, 1, 0]) is True
    assert alarms.snapshot([1, 0, 0]) is False
    assert alarms.slo_budget(["ok"] * 11 + ["over_cap"])["stop_arm"] is False
    assert alarms.slo_budget(["ok"] * 10 + ["over_cap", "SLO_BREACH"])["stop_arm"] is True
    assert alarms.drift(0.96, 1)["outside_band"] and alarms.drift(1.11, 1)["outside_band"]
    assert not alarms.drift(1.0, 1)["outside_band"]


def test_results_metrics():  # T-17
    gtb = {DS: {f"GT{i}": i in (1, 2, 3, 6) for i in range(1, 11)}, AL: {"GT1": True, "GT2": False, "GT3": True, "GT4": False},
           CT: {"GT1": False, "GT2": False}}
    scores = {DS: {"gt_covered_any": ["GT3", "GT6", "GT9"], "gt_covered_blocking": ["GT3", "GT9"], "wrong_blockers": 1},
              AL: {"gt_covered_any": ["GT4", "GT2"], "gt_covered_blocking": ["GT2"], "wrong_blockers": 2},
              CT: {"gt_covered_any": ["GT1"], "gt_covered_blocking": [], "wrong_blockers": 0}}
    m = results.metrics(scores, gtb)
    assert (m["found_14"], m["real_blocking_8"], m["judge_blocking"], m["wrong_blockers"]) == (5, 1, 3, 3)
    assert (m["control_found_2"], m["control_wrong_blockers"]) == (1, 0)
    assert "I1" in m["issues"]["credited_any"] and "I6" in m["issues"]["credited_any"] and "I7" in m["issues"]["credited_any"]
    assert m["issues"]["target_reach"] is True and m["issues"]["hard_credits"] == 4  # I1 (DS GT6), I4 (DS GT9), I6, I7
    none = results.metrics({DS: {"gt_covered_any": ["GT3"], "gt_covered_blocking": [], "wrong_blockers": 0}}, gtb)
    assert none["issues"]["target_reach"] is False


def test_results_row_partial_on_missing_score(env):
    rd = env["out"] / "runs" / "r1"
    for p in (DS, AL, CT):
        d = rd / p
        (d / "reviews").mkdir(parents=True)
        (d / "run.json").write_text(json.dumps({"arm": "A1-sl2", "panel": "sl2", "models": {}, "switches": {}}))
        (d / "pkg-status.json").write_text(json.dumps({"merge": "ok", "anon": "ok", "judge": "ok" if p != CT else "judge_failed"}))
        (d / "audit.json").write_text(json.dumps({"status": "pass"}))
    (rd / "launch.json").write_text(json.dumps({"pkgs": [DS, AL, CT]}))
    r = results.build("r1")
    assert r["status"] == "partial" and r["found_14"] == 0
