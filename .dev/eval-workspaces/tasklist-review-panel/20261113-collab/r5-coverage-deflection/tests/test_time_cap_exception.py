"""Owner-authorised time-cap exception (2026-11-14, OVERRIDE.md): TIME_CAP_EXCEPTION=1, off by default."""
import json
import os

import pytest
from conftest import CT, bin_, fake_log, run, write_values
from r5 import alarms, read_json, timing
from test_faults import base_scenario, judge_score, put

# The six Spike 4 value sets on disk (config/values/{el2,hl2}): B_A1, turn p90, report p90, measured k (0 everywhere), file hang offset.
REAL = [("el2", "design", 116.782, 40.382, 57.42, 175.173), ("el2", "designSpec", 120.1605, 43.812, 88.421, 180.24075),
        ("el2", "alias", 144.4515, 31.487, 73.543, 216.67725), ("hl2", "design", 209.4955, 59.515, 91.265, 314.24325),
        ("hl2", "designSpec", 220.9375, 94.584, 247.7, 331.40625), ("hl2", "alias", 264.0575, 76.654, 84.685, 396.08625)]


def vals(B=100.0, turn=10.0, rep_=20.0, k=0, **kw):
    v = {"B_f_s": B, "turn_p90_s": turn, "T_report_p90_s": rep_, "k": k, "finish_offset_s": 1.35 * B - turn - rep_,
         "hang_offset_s": 1.5 * B, "slowdown_s": 0.1, "slowdown_limit": 0.2, "budget_ok": True}
    return {**v, **kw}


# ------------------------------------------------------------------ the switch itself


def test_switch_default_off(monkeypatch):
    monkeypatch.delenv("TIME_CAP_EXCEPTION", raising=False)
    assert timing.time_cap_exception() == 0
    monkeypatch.setenv("TIME_CAP_EXCEPTION", "")
    assert timing.time_cap_exception() == 0
    monkeypatch.setenv("TIME_CAP_EXCEPTION", "0")
    assert timing.time_cap_exception() == 0
    monkeypatch.setenv("TIME_CAP_EXCEPTION", "1")
    assert timing.time_cap_exception() == 1


@pytest.mark.parametrize("bad", ["2", "-1", "true", "1.0", " 1", "01"])
def test_switch_rejects_other_values(monkeypatch, bad):
    monkeypatch.setenv("TIME_CAP_EXCEPTION", bad)
    with pytest.raises(ValueError, match="TIME_CAP_EXCEPTION"):
        timing.time_cap_exception()


# ------------------------------------------------------------------ off: nothing computed changes


@pytest.mark.parametrize("v", [vals(), vals(k=2, budget_ok=False), vals(B=273.7, turn=14, rep_=51.8, k=1, slack_s=30, hang_offset_s=410.55)])
def test_off_returns_the_file_numbers_unchanged(v):
    p = timing.exception_plan(v, False)
    assert p["time_cap_exception"] is False and p["k_forced"] is False
    assert p["k_run"] == v["k"] and p["k_measured"] == v["k"]
    assert p["hang_offset_s"] == v["hang_offset_s"] and p["finish_offset_s"] == v["finish_offset_s"]
    assert p["slowdown_limit"] == v["slowdown_limit"] and p["budget_ok"] == v["budget_ok"]
    assert p["time_cap_s"] == pytest.approx(1.35 * v["B_f_s"] + v.get("slack_s", 0))


def test_off_leaves_the_formulas_alone(monkeypatch):  # the pinned numbers of test_timing.py stand with the variable set to 1 too
    monkeypatch.setenv("TIME_CAP_EXCEPTION", "1")
    assert timing.k(100, 6.4, 13.9) == 0 and timing.k(116, 6.4, 6.4) == 2
    assert timing.finish_offset(116, 6.4, 6.4) == pytest.approx(143.8) and timing.hang_offset(273.7) == pytest.approx(410.55)
    assert timing.slowdown_limit(273.7, 2, 14) == pytest.approx(0.1381, abs=5e-5)


# ------------------------------------------------------------------ on


def test_on_forces_k1_only_where_measured_k_is_0():
    zero = timing.exception_plan(vals(k=0), True)
    assert zero["k_run"] == 1 and zero["k_forced"] is True and zero["k_measured"] == 0
    for kk in (1, 2):
        p = timing.exception_plan(vals(k=kk), True)
        assert p["k_run"] == kk and p["k_forced"] is False and p["k_measured"] == kk


def test_on_numbers():
    p = timing.exception_plan(vals(B=100, turn=10, rep_=20), True)
    assert p["hang_offset_s"] == pytest.approx(300) and p["time_cap_s"] == pytest.approx(270)
    assert p["finish_offset_s"] == pytest.approx(270 - 10 - 20)
    assert p["slowdown_limit"] == pytest.approx((270 - 100 - (2 + 2 * 1 * 10)) / 100)
    assert p["B_A1_s"] == 100


def test_on_hang_is_max_of_existing_and_3_b():
    assert timing.exception_plan(vals(B=100, hang_offset_s=500), True)["hang_offset_s"] == 500
    assert timing.exception_plan(vals(B=100, hang_offset_s=150), True)["hang_offset_s"] == pytest.approx(300)


def test_on_budget_ok_uses_the_widened_cap():
    assert timing.exception_plan(vals(B=100, turn=10, slowdown_s=0.5), True)["budget_ok"] is True    # 0.5 <= 1.48
    assert timing.exception_plan(vals(B=100, turn=10, slowdown_s=2.0), True)["budget_ok"] is False
    assert timing.exception_plan(vals(slowdown_s=None), True)["budget_ok"] is False                   # no kit measurement: not runnable


@pytest.mark.parametrize("panel,pkg,B,turn,report,hang0", REAL)
def test_on_real_spike4_numbers(panel, pkg, B, turn, report, hang0):
    p = timing.exception_plan(vals(B=B, turn=turn, rep_=report, hang_offset_s=hang0), True)
    assert p["k_run"] == 1 and p["k_forced"]
    assert p["hang_offset_s"] == pytest.approx(3.0 * B)
    assert p["finish_offset_s"] > 0                                        # the finish signal is not already past at T0
    assert p["finish_offset_s"] + turn + report <= p["hang_offset_s"]      # the report turn fits inside the hang guard
    assert B + timing.HOOKS_S + 2 * turn <= p["time_cap_s"]                # the one forced exchange fits inside the widened cap


def test_cli_exception_prints_the_plan(tmp_path, monkeypatch):
    f = tmp_path / "v.json"
    f.write_text(json.dumps(vals(B=100, turn=10, rep_=20)))
    for env_v, forced in (("0", False), ("1", True)):
        monkeypatch.setenv("TIME_CAP_EXCEPTION", env_v)
        r = run(["uv", "run", "--no-sync", "python", "-m", "r5.timing", "exception", str(f)], env=os.environ.copy())
        assert r.returncode == 0, r.stderr
        assert json.loads(r.stdout)["k_forced"] is forced


# ------------------------------------------------------------------ launcher


def launch(panel, row, extra, pkgs=CT):
    return run(["bash", bin_("launch.sh"), panel, row, "--pkgs", pkgs], env={**os.environ, **extra})


def test_launch_refuses_exception_without_collab(env):
    r = launch("sl2", "r-x0", {"TIME_CAP_EXCEPTION": "1", "PANEL_COLLAB": "0", "PANEL_KIT": "0"})
    assert r.returncode == 2 and "collaboration arm only" in r.stderr and fake_log(env) == []


@pytest.mark.parametrize("extra,msg", [({"TIME_CAP_EXCEPTION": "2"}, "must be 0 or 1"),
                                       ({"TIME_CAP_EXCEPTION": "1", "PANEL_SLACK_S": "30"}, "exclusive")])
def test_launch_refuses_bad_switch(env, extra, msg):
    r = launch("sl2", "r-xb", extra)
    assert r.returncode == 2 and msg in r.stderr and fake_log(env) == []


def test_launch_k0_everywhere_is_refused_without_the_exception(env):  # the old rule stays: exit 3, no model call
    write_values(env["cfg"], "sl2", all={"k": 0})
    r = launch("sl2", "r-off", {})
    assert r.returncode == 3 and "k = 0 on every package" in r.stderr and fake_log(env) == []


def test_launch_k0_everywhere_runs_with_the_exception(env):
    write_values(env["cfg"], "sl2", all={"k": 0})
    base_scenario(env, calls=15, gap=0.3)
    judge_score(env)
    r = launch("sl2", "r-on", {"TIME_CAP_EXCEPTION": "1"})
    assert r.returncode in (0, 1), r.stderr
    lj = read_json(env["out"] / "runs" / "r-on" / "launch.json")
    assert lj["env"]["TIME_CAP_EXCEPTION"] == 1 and lj["time_cap_exception"] is True
    assert lj["time_cap_plan"][CT]["k_forced"] is True and lj["time_cap_plan"][CT]["k_run"] == 1


def test_launch_exception_budget_still_checked_against_widened_cap(env):
    write_values(env["cfg"], "sl2", all={"k": 0, "slowdown_s": 5.0})  # 5.0 > (1.7 x 10 - (2 + 1)) / 10 = 1.4
    r = launch("sl2", "r-xbud", {"TIME_CAP_EXCEPTION": "1"})
    assert r.returncode == 3 and "budget_ok false" in r.stderr and fake_log(env) == []


# ------------------------------------------------------------------ end to end with the fake claude


def run_row(env, row, extra, k=0, **over):
    write_values(env["cfg"], "sl2", all={"B_f_s": 8, "turn_p90_s": 0.5, "T_report_p90_s": 0.5, "k": k, "finish_offset_s": 10,
                                         "hang_offset_s": 12, "slowdown_s": 0.01, **over})
    base_scenario(env, calls=15, gap=0.3)
    judge_score(env)
    r = launch("sl2", row, extra)
    assert r.returncode in (0, 1), r.stderr
    return env["out"] / "runs" / row / CT


def test_e2e_exception_on_forces_k1_and_stamps_everything(env):
    d = run_row(env, "r-e1", {"TIME_CAP_EXCEPTION": "1"})
    run_ = read_json(d / "run.json")
    assert run_["time_cap_exception"] is True and run_["k"] == 1 and run_["k_measured"] == 0 and run_["k_forced"] is True
    assert run_["hang_ms"] - run_["T0"] == pytest.approx(3.0 * 8 * 1000, abs=2)     # max(12, 3.0 x 8) = 24 s
    assert run_["finish_ms"] - run_["T0"] == pytest.approx((2.7 * 8 - 0.5 - 0.5) * 1000, abs=2)
    assert run_["k0_isolated"] is False and (d / "board").is_dir()                  # the collaboration path ran, not an A2 stand-in
    eff = read_json(d / "values-effective.json")
    assert eff["k"] == 1 and eff["hang_offset_s"] == pytest.approx(24) and eff["time_cap_exception"] is True
    c = read_json(d / "collab.json")
    assert c["time_cap_exception"] is True and c["B_A1_s"] == 8 and c["k_measured"] == 0 and c["k_forced"] is True and c["k"] == 1
    assert c["elapsed_over_baseline"] == pytest.approx(c["elapsed_s"] / 8)
    assert c["messages_delivered"] == {"t1b-1": 1, "t4-1": 0, "t3-1": 0}
    assert all(len(x["items"]) <= 1 for x in c["cards"] if x["items"])
    res = read_json(env["out"] / "results" / "r-e1.json")
    assert res["time_cap_exception"] is True
    tc = res["time_cap"][CT]
    assert tc["B_A1_s"] == 8 and tc["k_measured"] == 0 and tc["k_forced"] is True and tc["k_run"] == 1
    assert tc["elapsed_s"] == c["elapsed_s"] and tc["elapsed_over_baseline"] == c["elapsed_over_baseline"]
    assert tc["messages_delivered"]["t1b-1"] == 1
    assert res["collab"][CT]["requests_delivered"] >= 1
    # the identity checks and the allow-list stay on
    assert all(m in ("claude-sonnet-5-5", "gpt-6-luna") for m in res["models"].values()) and res["switches"]["NOFALLBACK"] == 1
    assert read_json(d / "audit.json")["status"] == "pass"


def test_run_panel_off_k0_is_the_old_a2_behaviour(env):  # k = 0 without the exception: no board, no cards, k0_isolated
    write_values(env["cfg"], "sl2", all={"B_f_s": 8, "k": 0, "finish_offset_s": 10, "hang_offset_s": 12})
    base_scenario(env)
    r = run(["bash", bin_("run-panel.sh"), "r-p00", "sl2", CT], env={**os.environ, "PANEL_COLLAB": "1"})
    assert r.returncode == 0, r.stderr
    d = env["out"] / "runs" / "r-p00" / CT
    run_ = read_json(d / "run.json")
    assert not (d / "board").exists() and run_["k0_isolated"] is True and run_["k"] == 0 and run_["time_cap_exception"] is False


def test_run_panel_off_row_is_stamped_false_and_untouched(env):
    write_values(env["cfg"], "sl2", all={"B_f_s": 8, "k": 2, "finish_offset_s": 10, "hang_offset_s": 12})
    base_scenario(env)
    r = run(["bash", bin_("run-panel.sh"), "r-p0", "sl2", CT], env={**os.environ, "PANEL_COLLAB": "1"})
    assert r.returncode == 0, r.stderr
    d = env["out"] / "runs" / "r-p0" / CT
    run_ = read_json(d / "run.json")
    assert run_["time_cap_exception"] is False and run_["k"] == 2 and run_["k_forced"] is False and run_["time_cap_s"] is None
    assert run_["hang_ms"] - run_["T0"] == pytest.approx(12000, abs=2) and run_["finish_ms"] - run_["T0"] == pytest.approx(10000, abs=2)
    assert not (d / "values-effective.json").exists()
    c = read_json(d / "collab.json")
    assert c["time_cap_exception"] is False and c["time_cap_s"] == pytest.approx(1.35 * 8)


def test_measured_k_of_2_keeps_k_and_widens_guards_only(env):
    d = run_row(env, "r-e2", {"TIME_CAP_EXCEPTION": "1"}, k=2)
    run_ = read_json(d / "run.json")
    assert run_["k"] == 2 and run_["k_forced"] is False and run_["time_cap_exception"] is True


def test_receiver_between_cap_and_widened_cap_ok_with_exception_killed_without(env):
    """B 2 s, file hang guard 3 s: a 3.5 s receiver is past 1.35 B and past the old guard; inside 2.7 B = 5.4 s and the widened 6 s guard."""
    write_values(env["cfg"], "sl2", all={"B_f_s": 2, "k": 0, "finish_offset_s": 20, "hang_offset_s": 3})
    base_scenario(env, calls=0)
    put(env, "claude-sonnet-5-5", sleep=3.5)
    r = run(["bash", bin_("run-panel.sh"), "r-o1", "sl2", CT], env={**os.environ, "PANEL_COLLAB": "1", "TIME_CAP_EXCEPTION": "1"})
    assert r.returncode == 0, r.stderr
    c = read_json(env["out"] / "runs" / "r-o1" / CT / "collab.json")
    assert c["slo"] == "ok" and c["time_cap_s"] == pytest.approx(5.4) and 3.5 <= c["elapsed_s"] < 5.4
    run(["bash", bin_("run-panel.sh"), "r-o0", "sl2", CT], env={**os.environ, "PANEL_COLLAB": "1"})
    assert read_json(env["out"] / "runs" / "r-o0" / CT / "collab.json")["slo"] == "SLO_BREACH"  # the old 3 s guard kills the same receiver


def test_run_panel_refuses_exception_with_collab_off(env):
    write_values(env["cfg"], "sl2")
    r = run(["bash", bin_("run-panel.sh"), "r-p1", "sl2", CT], env={**os.environ, "PANEL_COLLAB": "0", "TIME_CAP_EXCEPTION": "1"})
    assert r.returncode == 2 and "collaboration arm only" in r.stderr and fake_log(env) == []


# ------------------------------------------------------------------ the summariser never mixes


def _fake_run(root, row, pkg, tcx):
    d = root / "runs" / row / pkg
    d.mkdir(parents=True)
    (d / "collab.json").write_text(json.dumps({
        "slo": "ok", "time_cap_exception": tcx, "B_A1_s": 100, "elapsed_s": 150, "elapsed_over_baseline": 1.5, "k_measured": 0,
        "k_forced": tcx, "messages_delivered": {"t1b-1": 1}, "own_line_jaccard": 0.1, "ledger_rows": 5, "union_anchored_tasks": 4,
        "reviewers": {"t1b-1": {"role": "receiver", "snapshot_missing": 0}}}))


def test_arm_summary_reports_columns_and_refuses_to_mix(env):
    out = env["out"]
    _fake_run(out, "x1", CT, True)
    _fake_run(out, "x2", CT, True)
    _fake_run(out, "c1", CT, False)
    (out / "results").mkdir()
    s = alarms.arm("F6-sl2", ["x1", "x2"])
    assert s["time_cap_exception"] is True and (out / "results" / "arm-summary-F6-sl2-tcx.json").exists()
    assert {r["row"] for r in s["time_cap_runs"][CT]} == {"x1", "x2"}
    assert all(set(r) >= {"B_A1_s", "elapsed_s", "elapsed_over_baseline", "k_measured", "k_forced", "messages_delivered"} for r in s["time_cap_runs"][CT])
    plain = alarms.arm("F6-sl2", ["c1"])
    assert plain["time_cap_exception"] is False and "time_cap_runs" not in plain
    assert (out / "results" / "arm-summary-F6-sl2.json").exists()                                  # the cap-obeying summary is a separate file
    with pytest.raises(SystemExit, match="never summarised together"):
        alarms.arm("F6-sl2", ["x1", "c1"])

