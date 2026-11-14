"""Owner-authorised time-cap exception (OVERRIDE.md): values.tce_entry, run-panel.sh TIME_CAP_EXCEPTION on and off,
the stamped results columns, and arm_summary keeping exception rows apart."""

import json
import sys
from pathlib import Path

import arm_summary as asum
import pytest
from r4help import DE, R4, fixture, make_sbr, run, write_values
from test_arm_summary import A1, P3, row
from test_launcher import FAKE, launch, refusals

import values


@pytest.fixture
def ready(env, tmp_path):
    make_sbr(env)
    fixture(env, FAKE, tmp_path)
    return env


def tce(env):
    return dict(env, TIME_CAP_EXCEPTION="1")


# ---------------------------------------------------------------- lib/values.py

def test_tce_entry_vectors():
    # EL2 control package, Spike 4 values: measured k = 0 -> forced to 1, hang guard 3.0 B, finish keeps its distance to the guard
    e = values.tce_entry({"B_A1": 114.121, "hang_s": 171.181, "finish_offset_s": 58.038, "k": 0})
    assert e == {"k": 1, "k_measured": 0, "k_forced": True, "finish_offset_s": 229.22, "hang_s": 342.363}
    # SL2 control package: measured k = 1 stays 1 (not forced), timers still widened
    e = values.tce_entry({"B_A1": 258.964, "hang_s": 388.446, "finish_offset_s": 312.131, "k": 1})
    assert (e["k"], e["k_forced"], e["hang_s"], e["finish_offset_s"]) == (1, False, 776.892, 700.577)
    # measured k = 2 stays 2
    assert values.tce_entry({"B_A1": 100, "hang_s": 150, "finish_offset_s": 100, "k": 2})["k"] == 2
    # an existing hang guard already above 3.0 B is kept (max), and so is the finish offset
    e = values.tce_entry({"B_A1": 100, "hang_s": 400, "finish_offset_s": 380, "k": 0})
    assert (e["hang_s"], e["finish_offset_s"]) == (400, 380)


def test_tce_entry_does_not_mutate_and_matches_the_formulas():
    v = {"B_A1": 116, "hang_s": values.hang_s(116), "finish_offset_s": values.finish_offset(116, 23, 23), "k": 0}
    before = dict(v)
    e = values.tce_entry(v)
    assert v == before
    assert e["hang_s"] == 348.0 and e["hang_s"] - e["finish_offset_s"] == pytest.approx(v["hang_s"] - v["finish_offset_s"])


def test_tce_cli_prints_entry_and_writes_nothing(tmp_path):
    p = tmp_path / "v.json"
    p.write_text(json.dumps({"packages": {"X": {"B_A1": 10, "hang_s": 15, "finish_offset_s": 12, "k": 0}}}))
    r = run([sys.executable, "-I", R4 / "lib" / "values.py", "tce", "--values", p, "--pkg", "X"])
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout) == {"k": 1, "k_measured": 0, "k_forced": True, "finish_offset_s": 27.0, "hang_s": 30.0}
    assert [f.name for f in tmp_path.iterdir()] == ["v.json"]


# ---------------------------------------------------------------- launcher refusals

def test_override_refusals(ready, tmp_path):
    env = ready
    k0 = write_values(env, B=6.0, name="k0.json")
    plan = Path(env["R4_OUT"]) / "values" / "plan.json"
    d = json.loads(k0.read_text())
    d["kind"] = "planning"
    values.write_pinned(str(plan), d)
    nodel = write_values(env, B=6.0, deliver=False, name="nodel.json")
    cases = [
        ("TIME_CAP_EXCEPTION is not 0 or 1", launch(dict(env, TIME_CAP_EXCEPTION="2"), "z1", values=k0)),
        ("needs PANEL_COLLAB=1", launch(tce(env), "z2", collab=0, values=k0)),
        ("needs measured values", launch(tce(env), "z3", values=plan)),
        ("needs deliver true", launch(tce(env), "z4", values=nodel)),
        # off (unset or 0): the original rule still refuses a row in which every package has k = 0
        ("k = 0 on every package", launch(env, "z5", values=k0)),
        ("k = 0 on every package", launch(dict(env, TIME_CAP_EXCEPTION="0"), "z6", values=k0)),
    ]
    for want, r in cases:
        assert r.returncode == 2 and want in r.stderr, (want, r.stderr)
    assert len(refusals(env)) == len(cases)
    assert not any((Path(env["R4_OUT"]) / "runs" / f"z{i}").exists() for i in range(1, 7))
    assert not (Path(env["FAKE_LOG"]) / "argv.jsonl").exists()  # no reviewer ever started


# ---------------------------------------------------------------- launcher, override on

def test_override_on_runs_a_k0_package_with_k1_and_stamps_the_row(ready):
    env = ready
    k0 = write_values(env, B=6.0, name="k0.json")  # measured k = 0: refused without the override
    r = launch(tce(env), "tce-on", values=k0, extra=("--packages", DE))
    assert r.returncode == 0, r.stdout + r.stderr
    assert "TIME_CAP_EXCEPTION=1" in r.stderr
    out = Path(env["R4_OUT"])
    rd = out / "runs" / "tce-on"
    pj = json.load(open(rd / DE / "panel.json"))
    # k forced to 1, collaboration on (not k0_isolated), hang guard 3.0 B, finish keeps its original distance to the guard
    assert (pj["k"], pj["k_measured"], pj["k_forced"], pj["collab"], pj["k0_isolated"]) == (1, 0, True, 1, False)
    assert pj["hang_ms"] - pj["t0_ms"] == 18000                  # 3.0 x 6.0 s
    assert pj["finish_ms"] - pj["t0_ms"] == 16100                # 18.0 - (9.0 - 7.1)
    assert pj["time_cap_exception"] is True
    assert "--cap 2 " in (Path(env["R4_SBR"]) / "board" / "tce-on" / DE / "bin" / "card").read_text()
    for rid in ("t2b-1", "t4-1", "t3-1"):
        s = json.load(open(Path(env["R4_SBR"]) / "board/tce-on" / DE / "settings" / f"{rid}.json"))
        cmd = s["hooks"]["PostToolUse"][0]["hooks"][0]["command"]
        assert "--k 1 " in cmd and f"--finish-ms {pj['finish_ms']} " in cmd
    assert json.load(open(rd / "run.json"))["time_cap_exception"] is True
    cj = json.load(open(rd / DE / "collab.json"))
    assert cj["time_cap_exception"] is True and cj["k"] == 1 and cj["k_forced"] is True and cj["k_measured"] == 0
    assert 1 <= cj["cards_sent"] <= 2 and cj["cards_rejected"] >= 1       # the fake flagger posts 4: two are over the cap of 2k
    dpr = cj["delivered_per_reviewer"]
    assert set(dpr) == {"t2b-1", "t4-1", "t3-1"} and dpr["t2b-1"] == 0 and max(dpr.values()) <= 1 and sum(dpr.values()) == cj["cards_delivered"] >= 1
    assert cj["baseline_elapsed_s"] == 6.0
    assert cj["elapsed_over_baseline"] == pytest.approx(cj["elapsed_s"] / 6.0, abs=1e-4)
    res = json.load(open(out / "results" / "tce-on.json"))
    assert res["time_cap_exception"] is True
    c = res["collab"][DE]
    assert c["time_cap_exception"] is True and c["k_forced"] is True and c["k"] == 1 and c["k_measured"] == 0
    assert c["baseline_elapsed_s"] == 6.0 and c["elapsed_s"] == cj["elapsed_s"] and c["elapsed_over_baseline"] == cj["elapsed_over_baseline"]
    assert c["delivered_per_reviewer"] == dpr and c["hang_s"] == 18.0 and c["finish_offset_s"] == 16.1
    assert res["elapsed_s"]["DE"] == cj["elapsed_s"]
    sched = [json.loads(x) for x in (out / "runs" / "schedule.jsonl").read_text().splitlines()]
    assert sched[-1]["time_cap_exception"] is True


def test_override_on_widens_timers_but_keeps_a_measured_k(ready):
    env = ready
    r = launch(tce(env), "tce-k2", values=write_values(env), extra=("--packages", DE, "--no-judge"))  # B = 20, measured k = 2
    assert r.returncode == 0, r.stdout + r.stderr
    pj = json.load(open(Path(env["R4_OUT"]) / "runs/tce-k2" / DE / "panel.json"))
    assert (pj["k"], pj["k_measured"], pj["k_forced"], pj["time_cap_exception"]) == (2, 2, False, True)
    assert pj["hang_ms"] - pj["t0_ms"] == 60000


# ---------------------------------------------------------------- launcher, override off: nothing computed changes

def test_override_off_keeps_every_computed_value(ready):
    env = ready
    v = write_values(env)  # B = 20, measured k = 2
    ent = json.load(open(v))["packages"][DE]
    r = launch(env, "tce-off", values=v, extra=("--packages", DE, "--no-judge"))
    assert r.returncode == 0, r.stdout + r.stderr
    rd = Path(env["R4_OUT"]) / "runs" / "tce-off"
    pj = json.load(open(rd / DE / "panel.json"))
    assert (pj["k"], pj["k_measured"], pj["k_forced"], pj["time_cap_exception"]) == (2, 2, False, False)
    assert pj["hang_ms"] - pj["t0_ms"] == round(ent["hang_s"] * 1000) == 30000
    assert pj["finish_ms"] - pj["t0_ms"] == round(ent["finish_offset_s"] * 1000)
    assert json.load(open(rd / "run.json"))["time_cap_exception"] is False
    cj = json.load(open(rd / DE / "collab.json"))
    assert cj["time_cap_exception"] is False and cj["k_forced"] is False and cj["elapsed_over_baseline"] is not None
    assert "time_cap_exception" not in json.loads((Path(env["R4_OUT"]) / "runs/schedule.jsonl").read_text().splitlines()[-1])


# ---------------------------------------------------------------- lib/arm_summary.py

def with_tce(r, ratio=3.0):
    r = dict(r, time_cap_exception=True, elapsed_s={s: 100.0 * ratio for s in P3})
    for c in r["collab"].values():
        c.update(time_cap_exception=True, k_measured=0, k_forced=True, k=1, elapsed_over_baseline=ratio,
                 delivered_per_reviewer={"t2b-1": 0, "t4-1": 1, "t3-1": 1})
    return r


def test_summary_keeps_exception_rows_apart():
    arm = [row(f"f{i}") for i in range(12)]
    exc = [with_tce(row("x1", el=300.0)), with_tce(row("x2", el=300.0))]
    plain = asum.summarize("EL2", A1, arm)
    mixed = asum.summarize("EL2", A1 + [with_tce(row("a-x", cards=0, ffo=None))], arm + exc)
    assert mixed.pop("n_arm_time_cap_exception") == 2 and plain.pop("n_arm_time_cap_exception") == 0
    block = mixed.pop("time_cap_exception")
    assert mixed == plain                                   # not one cap-obeying statistic moved
    assert mixed["time_verdict"]["DS"]["ok"] is True        # ratio 3.0 rows did not break the +35% verdict
    assert [r["row"] for r in block["rows"]] == ["x1", "x2"]
    p = block["rows"][0]["packages"]["DS"]
    assert (p["B_A1"], p["elapsed_s"], p["elapsed_over_baseline"], p["k_measured"], p["k_forced"], p["k"]) == (100.0, 300.0, 3.0, 0, True, 1)
    assert p["delivered_per_reviewer"] == {"t2b-1": 0, "t4-1": 1, "t3-1": 1} and p["cards_sent"] == 2
    assert block["stats"]["n_arm"] == 2 and "time_verdict" not in block["stats"] and "slo" not in block["stats"]
    assert "interim_futility" not in block["stats"]


def test_summary_with_only_exception_rows():
    out = asum.summarize("EL2", A1, [with_tce(row("x1"))])
    assert out["n_arm"] == 0 and out["n_arm_time_cap_exception"] == 1 and out["time_cap_exception"]["stats"]["n_arm"] == 1
