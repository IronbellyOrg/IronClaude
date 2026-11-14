"""TIME_CAP_EXCEPTION (owner decision 2026-11-14, OVERRIDE.md): a forced n of 1 where the measured n is 0."""

import subprocess
from pathlib import Path

import pytest
from conftest import (
    CONTROL,
    default_rules,
    jload,
    launch,
    mini_sandbox,
    write_plan,
    write_values,
)
from test_summary import P, row

from r3lib import metrics, paths, values

# EL2 design package, Spike 4 numbers (values/el2.json): B_A1, luna turn p90, report turn p90.
B, TURN, REPORT = 137.81000018119812, 12.176000118255615, 13.604000091552734


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    monkeypatch.delenv("TIME_CAP_EXCEPTION", raising=False)
    monkeypatch.delenv("PANEL_SLACK_S", raising=False)
    monkeypatch.delenv("R3_VALUES_FILE", raising=False)


def _plan(forced=1):
    v, _ = values.load("el2")
    return v, values.tce_all(forced, "el2", v)[CONTROL]


# ---------------------------------------------------------------- off: nothing changes
def test_off_by_default_and_floor_is_identity():
    assert values.tce_forced() == 0
    assert values.tce_floor_n(0, None, 155.0, 6, TURN, 2) == 0
    assert values.tce_floor_n(2, None, 0.0, 6, TURN, 2) == 2
    # the pinned n and k formulas are untouched
    assert values.compute_n(0, B, 155.0, 35, 2, 6, TURN) == 0
    assert values.compute_k(B, TURN, REPORT) == 0
    assert values.load("el2", smoke=True)[1] is None  # smoke still uses planning values
    assert paths.values_file("el2") == paths.R3 / "values" / "el2.json"


@pytest.mark.parametrize("raw,want", [("", 0), ("0", 0), ("1", 1), ("2", 2), ("3", 3)])
def test_forced_value_parsing(monkeypatch, raw, want):
    monkeypatch.setenv("TIME_CAP_EXCEPTION", raw)
    assert values.tce_forced() == want


@pytest.mark.parametrize("bad", ["abc", "-1", "4", "1.5", "yes"])
def test_bad_value_refused(monkeypatch, bad):
    monkeypatch.setenv("TIME_CAP_EXCEPTION", bad)
    with pytest.raises(SystemExit, match="E_TCE"):
        values.tce_forced()


# ---------------------------------------------------------------- on: numbers
def test_plan_numbers_el2_design():
    v, t = _plan()
    assert t["B_A1"] == pytest.approx(B) and t["B_A1_source"] == "frozen"
    assert t["hang_offset_s"] == pytest.approx(3.0 * B)  # max(1.5 B_f, 3.0 B_A1)
    assert t["p2_deadline_offset_s"] == pytest.approx(3.0 * B + 16 + 2 * 1 * TURN)
    # finish offset: widened cap (3.0 B) minus the critical (luna) turn and the report turn
    assert t["finish_offset_s"] == pytest.approx(3.0 * B - TURN - REPORT)
    assert t["finish_offset_cap_s"] == pytest.approx(
        values.finish_offset(B, TURN, REPORT)
    )
    assert t["k_measured"] == 0 and t["forced_n"] == 1
    # the widened values never fall below the existing ones
    p = v["packages"][CONTROL]
    assert t["hang_offset_s"] >= 1.5 * p["B_f"]
    assert t["p2_deadline_offset_s"] >= 1.30 * p["B_f"]
    assert t["finish_offset_s"] >= p["panel_finish_offset_s"]


def test_floor_only_where_measured_n_is_zero():
    _, t = _plan()
    assert values.compute_n(0, B, 155.0, 35, 2, 6, TURN) == 0  # measured 0
    assert values.tce_floor_n(0, t, 155.0, 6, TURN, 2) == 1  # forced 1
    assert values.tce_floor_n(1, t, 90.0, 6, TURN, 2) == 1  # measured value kept
    assert values.tce_floor_n(2, t, 90.0, 6, TURN, 2) == 2  # never lowered
    # a launch so late that the widened deadline has no room for one challenge stays 0
    late = t["p2_deadline_offset_s"] - 6 - 2 * TURN + 0.5
    assert values.tce_floor_n(0, t, late, 6, TURN, 2) == 0
    assert values.tce_floor_n(0, t, late - 1.0, 6, TURN, 2) == 1
    # a fresh fallback start (16 s) needs more room
    assert values.tce_floor_n(0, t, late - 1.0, 16, TURN, 2) == 0
    # forced 3 is bounded by the receiver's cap
    t3 = dict(t, forced_n=3)
    assert values.tce_floor_n(0, t3, 155.0, 6, TURN, 2) == 2


def test_prefer_frozen_only_with_exception():
    v, sha = values.load("el2", smoke=True, prefer_frozen=True)
    assert sha is not None and v["status"] == "frozen"
    assert values.load("el2", smoke=True)[1] is None


# ---------------------------------------------------------------- summary: rows never mix
def _exc_row(arm="A3", el=300.0, delivered=None):
    r = row(arm, el)
    r["time_cap_exception"] = True
    r["tce"] = {
        "forced_n": 1,
        "by_pkg": {
            P: {
                "B_A1": 100.0,
                "B_A1_source": "frozen",
                "elapsed_s": el,
                "ratio": el / 100.0,
                "forced_n": 1,
                "delivered": delivered or {"t2b-1": 1, "t4-1": 1, "t3-1": 0},
            }
        },
    }
    return r


def test_summary_keeps_exception_rows_apart():
    base = [row("A1", 100) for _ in range(3)] + [row("A3", 120)]
    plain = metrics.summarize(base, "el2")
    mixed = metrics.summarize(base + [_exc_row(el=400.0)], "el2")
    # arms and cap check are exactly what they were without the exception row
    assert mixed["arms"] == plain["arms"] and mixed["cap_check"] == plain["cap_check"]
    assert plain["time_cap_exception"]["rows"] == 0
    t = mixed["time_cap_exception"]
    assert t["rows"] == 1 and t["arm_A3_exception"]["runs"] == 1
    d = t["by_pkg"][P]
    assert d["B_A1"] == 100.0 and d["elapsed_s"] == [400.0] and d["ratio"] == [4.0]
    assert d["median_ratio"] == 4.0 and d["delivered"] == {
        "t2b-1": [1],
        "t4-1": [1],
        "t3-1": [0],
    }
    table = metrics.summary_table(mixed)
    assert "time_cap_exception rows" in table and "elapsed/B_A1" in table
    assert "time_cap_exception" not in metrics.summary_table(plain)


# ---------------------------------------------------------------- launcher
def _run(env, extra_env, collab=1):
    e = dict(env["env"], PANEL_COLLAB=str(collab), **extra_env)
    return subprocess.run(
        [
            "bash",
            str(paths.R3 / "bin/launch-panel.sh"),
            "el2",
            "--pkgs",
            CONTROL,
            "--no-judge",
        ],
        env=e,
        capture_output=True,
        text=True,
        timeout=60,
    )


@pytest.mark.parametrize("tce,collab", [("abc", 1), ("4", 1), ("1", 0)])
def test_launcher_refuses_bad_or_baseline_use(env, tce, collab):
    write_values(env)
    r = _run(env, {"TIME_CAP_EXCEPTION": tce}, collab)
    assert r.returncode == 1 and "E_TCE" in r.stderr
    assert not (env["root"] / "runs").exists()


def _tce_launch(env, tce):
    # turn 30 s makes the measured n 0 for every receiver (B_f 40 s), so the exception has something to force
    write_values(env, B=40.0, turn=30.0)
    mini_sandbox(env)
    write_plan(env, default_rules(env))
    return launch(
        env,
        collab=1,
        extra=["--no-judge"],
        envx={"TIME_CAP_EXCEPTION": tce} if tce else {},
    )


@pytest.mark.slow
def test_launch_off_has_no_stamp_and_measured_n_zero(env):
    r, rd = _tce_launch(env, None)
    assert r.returncode in (0, 2), r.stderr
    assert jload(rd / "run.json")["time_cap_exception"] is False
    pj = jload(rd / CONTROL / "pkg.json")
    assert "tce" not in pj
    assert pj["HANG_AT"] - pj["T0"] == pytest.approx(60.0, abs=0.01)
    assert pj["P2_DEADLINE"] - pj["T0"] == pytest.approx(52.0, abs=0.01)
    cj = jload(rd / CONTROL / "collab.json")
    assert cj["time_cap_exception"] is False and cj["tce"] is None
    assert all(
        v["n_launched"] == 0 for v in cj["reviewers"].values()
    )  # nothing delivered
    assert jload(rd / "result.json")["time_cap_exception"] is False


@pytest.mark.slow
def test_launch_on_forces_one_and_stamps_everything(env):
    r, rd = _tce_launch(env, "1")
    assert r.returncode in (0, 2), r.stderr
    run = jload(rd / "run.json")
    assert run["time_cap_exception"] is True and run["tce_forced_n"] == 1
    pj = jload(rd / CONTROL / "pkg.json")
    assert pj["HANG_AT"] - pj["T0"] == pytest.approx(3.0 * 40.0, abs=0.01)
    assert pj["P2_DEADLINE"] - pj["T0"] == pytest.approx(
        3.0 * 40.0 + 16 + 2 * 30.0, abs=0.01
    )
    assert pj["tce"]["B_A1"] == pytest.approx(40.0)
    cj = jload(rd / CONTROL / "collab.json")
    assert cj["time_cap_exception"] is True
    t = cj["tce"]
    assert t["forced_n"] == 1 and t["B_A1"] == pytest.approx(40.0)
    assert t["ratio"] == pytest.approx(t["elapsed_s"] / 40.0)
    assert set(t["delivered"].values()) == {1} and all(t["forced_applied"].values())
    res = jload(rd / "result.json")
    assert res["time_cap_exception"] is True
    bp = res["tce"]["by_pkg"][CONTROL]
    assert bp["B_A1"] == pytest.approx(40.0) and bp["elapsed_s"] == t["elapsed_s"]
    assert bp["delivered"] == t["delivered"] and bp["ratio"] == t["ratio"]
    # observed model equals the requested model in every used session (no fallback)
    for v in cj["reviewers"].values():
        assert v["state"] == "sealed" and not v["hang_kill"] and not v["phase2_timeout"]
    assert Path(rd / CONTROL / "audit.json").exists()
    assert not (jload(rd / CONTROL / "audit.json").get("violations"))
