"""Owner-authorised time-cap exception (OVERRIDE.md): TIME_CAP_EXCEPTION=1, default off.
values.py (exception_values and the 9 frozen files), launch-panel.sh preflight, collab_metrics.py stamps, results row,
summarize_arm.py separation, and a full launch with the fake `claude` with the override on and off."""
import hashlib
import json
import shutil
import sys

import pytest
from conftest import CONTROL, PKGS, PY, R2, report, run
from test_collab_metrics import T0, build
from test_summarize_arm import BASE, row

sys.path.insert(0, str(PY))
import collab_metrics as CM  # noqa: E402
import summarize_arm as SA  # noqa: E402
import values as V  # noqa: E402

PKG = CONTROL
LS = {"tool": "Bash", "input": {"command": "ls"}, "response": {"stdout": "x"}}
# Spike 4 EL2 on the control package, as pinned in config/values/EL2/<control>.json (measured k = 0)
EL2_MEASURED = ("EL2", PKG, 102.8185, 12.519, 15.563, 102.8185, 12.519, 15.563)


def measured(**kw):
    v = V.compute(*EL2_MEASURED, source="spike4", n_runs=4)
    v.update(kw)
    return v


# ---------------------------------------------------------------- values.py

def test_switch_default_is_off(monkeypatch):
    monkeypatch.delenv("TIME_CAP_EXCEPTION", raising=False)
    assert V.time_cap_exception() == 0
    monkeypatch.setenv("TIME_CAP_EXCEPTION", "")
    assert V.time_cap_exception() == 0
    monkeypatch.setenv("TIME_CAP_EXCEPTION", "0")
    assert V.time_cap_exception() == 0
    monkeypatch.setenv("TIME_CAP_EXCEPTION", "1")
    assert V.time_cap_exception() == 1


@pytest.mark.parametrize("bad", ["2", "-1", "abc", "true", "1.0"])
def test_switch_bad_value_refused(monkeypatch, bad):
    monkeypatch.setenv("TIME_CAP_EXCEPTION", bad)
    with pytest.raises(ValueError, match="TIME_CAP_EXCEPTION"):
        V.time_cap_exception()


def test_off_never_changes_computed_values(monkeypatch):
    before = V.compute(*EL2_MEASURED)
    monkeypatch.setenv("TIME_CAP_EXCEPTION", "1")  # the switch is read by the launcher only; compute() ignores it
    assert V.compute(*EL2_MEASURED) == before
    assert before["k"] == 0 and before["panel_finish_at_s"] == 110.723 and before["hang_s"] == 154.228
    assert "time_cap_exception" not in before


def test_exception_forces_k1_and_widens_the_guards():
    m = measured()
    e = V.exception_values(m)
    assert m["k"] == 0 and e["k"] == 1
    assert e["hang_s"] == round(3.0 * 102.8185, 3) == 308.456
    assert e["panel_finish_at_s"] == pytest.approx(e["hang_s"] - 12.519 - 15.563, abs=1e-3) == pytest.approx(280.374, abs=1e-3)
    assert e["sweeper_kill_s"] == pytest.approx(e["panel_finish_at_s"] - 2 * 12.519, abs=1e-3)
    assert e["hang_s"] > m["hang_s"] and e["panel_finish_at_s"] > m["panel_finish_at_s"] and e["sweeper_kill_s"] > m["sweeper_kill_s"]
    x = e["time_cap_exception"]
    assert x == {"B_A1": 102.8185, "k_measured": 0, "k_forced": 1, "applied": True, "hang_s_measured": 154.228,
                 "panel_finish_at_s_measured": 110.723, "sweeper_kill_s_measured": 85.685}
    # one message fits the widened finish by the design's own D-2 rule
    assert V.k(e["panel_finish_at_s"], e["E_recv"], e["turn_p90_recv"]) >= 1
    # everything else is the measured file
    assert {k: v for k, v in e.items() if k not in ("k", "hang_s", "panel_finish_at_s", "sweeper_kill_s", "time_cap_exception")} == \
           {k: v for k, v in m.items() if k not in ("k", "hang_s", "panel_finish_at_s", "sweeper_kill_s")}


def test_exception_leaves_a_package_with_measured_k_alone():
    m = V.compute("SL2", PKG, 294.588, 26.142, 25.433, 106.087, 12.593, 13.078, "spike4", 4)
    assert m["k"] == 2
    e = V.exception_values(m)
    assert e["time_cap_exception"]["applied"] is False and e["time_cap_exception"]["k_forced"] == 2
    assert {k: v for k, v in e.items() if k != "time_cap_exception"} == m


def test_exception_never_narrows_an_existing_guard():
    # existing hang guard above 3 B: kept
    e = V.exception_values(measured(hang_s=1000.0))
    assert e["hang_s"] == 1000.0 and e["panel_finish_at_s"] == pytest.approx(1000.0 - 12.519 - 15.563, abs=1e-3)


def test_exception_refuses_when_one_message_still_does_not_fit():
    with pytest.raises(ValueError, match="does not fit one message"):
        V.exception_values(measured(E_recv=5000.0))


@pytest.mark.parametrize("panel", ["EL2", "SL2", "HL2"])
@pytest.mark.parametrize("pkg", PKGS)
def test_frozen_exception_values_derive_from_the_pinned_ones(panel, pkg):
    old = json.loads((R2 / f"config/values/{panel}/{pkg}.json").read_text())
    path = R2 / f"config/values-exception/{panel}/{pkg}.json"
    new = json.loads(path.read_text())
    assert new == V.exception_values(old)
    x = new["time_cap_exception"]
    assert x["B_A1"] == old["B_f"] and x["k_measured"] == old["k"] and x["applied"] == (old["k"] == 0)
    assert new["k"] == max(old["k"], 1) and new["hang_s"] >= old["hang_s"]
    if x["applied"]:
        assert new["hang_s"] >= round(3.0 * old["B_f"], 3) and new["panel_finish_at_s"] > old["panel_finish_at_s"]
    else:
        assert all(new[k] == old[k] for k in ("k", "hang_s", "panel_finish_at_s", "sweeper_kill_s"))
    pins = json.loads((R2 / "config/manifest-exception.json").read_text())["sha256"]
    assert pins[f"values-exception/{panel}/{pkg}.json"] == hashlib.sha256(path.read_bytes()).hexdigest()


def test_frozen_exception_manifest_has_the_same_non_value_pins_as_the_base_manifest():
    a, b = (json.loads((R2 / f"config/{n}").read_text()) for n in ("manifest-exception.json", "manifest.json"))
    keep = lambda m: {k: v for k, v in m["sha256"].items() if not k.startswith("values")}  # noqa: E731
    assert keep(a) == keep(b) and a["base_sha"] == b["base_sha"]


# ---------------------------------------------------------------- collab.json (collab_metrics.py)

def _values_json(pd, v):
    (pd / "values.json").write_text(json.dumps(v))


def test_collab_off_is_not_stamped_and_keeps_the_old_slo_rule(tmp_path):
    pd = build(tmp_path, B=100)
    (pd / "elapsed_s").write_text("160.0")
    out = CM.compute(pd, "EL2", pd / "values.json", "F4", "row", "pkg")
    assert out["time_cap_exception"] is False and out["time_cap_exception_applied"] is False
    assert out["slo_breach"] is True                      # 160 > 1.5 x 100, as before the override existed
    assert out["B_A1"] == 100 and out["k_measured"] == out["k"] == 2 and out["elapsed_over_baseline"] == 1.6
    assert out["messages_delivered"] == {"t2b-1": 0, "t4-1": 0, "t3-1": 0}


def test_collab_on_records_the_exception_columns(tmp_path):
    pd = build(tmp_path, B=100, k=1)
    (pd / "elapsed_s").write_text("160.0")
    dl = [{"ev": "deliver", "t": T0 + 5000, "c": 6, "fact": "f-0", "i": 0}]
    (pd / "board/metrics/t4-1.jsonl").write_text("".join(json.dumps(x) + "\n" for x in dl))
    (pd / "board/msgs/board.jsonl").write_text(json.dumps({"id": "f-0", "t": T0 + 1000, "from": "sw-1", "move": "M1", "items": []}) + "\n")
    _values_json(pd, {"B_f": 100, "k": 1, "panel_finish_at_s": 280.0, "hang_s": 300.0,
                      "time_cap_exception": {"B_A1": 100, "k_measured": 0, "k_forced": 1, "applied": True}})
    out = CM.compute(pd, "EL2", pd / "values.json", "F4", "row", "pkg")
    assert out["time_cap_exception"] is True and out["time_cap_exception_applied"] is True
    assert out["B_A1"] == 100 and out["k"] == 1 and out["k_measured"] == 0 and out["elapsed_s"] == 160.0
    assert out["elapsed_over_baseline"] == 1.6
    assert out["messages_delivered"]["t4-1"] == 1 and out["messages_delivered"]["t3-1"] == 0
    assert out["slo_breach"] is False                     # 160 s is inside the widened hang guard (300 s)


def test_collab_on_still_flags_a_breach_of_the_widened_hang_guard(tmp_path):
    pd = build(tmp_path, B=100, k=1)
    (pd / "elapsed_s").write_text("310.0")
    _values_json(pd, {"B_f": 100, "k": 1, "panel_finish_at_s": 280.0, "hang_s": 300.0,
                      "time_cap_exception": {"B_A1": 100, "k_measured": 0, "k_forced": 1, "applied": True}})
    assert CM.compute(pd, "EL2", pd / "values.json", "F4", "row", "pkg")["slo_breach"] is True


def test_collab_on_but_not_applied_keeps_the_cap_rule(tmp_path):
    pd = build(tmp_path, B=100)
    (pd / "elapsed_s").write_text("160.0")
    _values_json(pd, {"B_f": 100, "k": 2, "panel_finish_at_s": 120.0, "hang_s": 150.0,
                      "time_cap_exception": {"B_A1": 100, "k_measured": 2, "k_forced": 2, "applied": False}})
    out = CM.compute(pd, "EL2", pd / "values.json", "F4", "row", "pkg")
    assert out["time_cap_exception"] is True and out["time_cap_exception_applied"] is False and out["slo_breach"] is True


# ---------------------------------------------------------------- summarize_arm.py

def exc(r, ratio=2.0, applied=True):
    r["time_cap_exception"] = True
    r["per_package"]["p"].update({"time_cap_exception": True, "time_cap_exception_applied": applied, "B_A1": 100.0,
                                  "elapsed_over_baseline": ratio, "k_measured": 0, "messages_delivered": {"t4-1": 1, "t3-1": 0}})
    return r


def test_summary_refuses_to_mix_exception_and_cap_rows():
    with pytest.raises(ValueError, match="must not be mixed"):
        SA.summarize([exc(row("x")), row("y")], [exc(row(f"a{i}")) for i in range(2)])
    with pytest.raises(ValueError, match="must not be mixed"):
        SA.summarize([exc(row("x"))], BASE)            # exception arm against cap-obeying baseline rows
    with pytest.raises(ValueError, match="must not be mixed"):
        SA.summarize([row("x")], [exc(row("a"))])


def test_summary_mixing_exits_2(tmp_path):
    from conftest import pyrun
    (tmp_path / "r.json").write_text(json.dumps(exc(row("x"))))
    (tmp_path / "b.json").write_text(json.dumps(BASE[0]))
    r = pyrun("summarize_arm.py", "--rows", str(tmp_path / "r.json"), "--baseline-rows", str(tmp_path / "b.json"), "--out", str(tmp_path / "o.json"))
    assert r.returncode == 2 and "time_cap_exception" in r.stdout


def test_summary_reports_the_exception_columns_and_waives_the_elapsed_cap():
    base = [exc(row(f"a{i}")) for i in range(4)]
    rows = [exc(row(f"r{i}", elapsed=100.0)) for i in range(10)] + [exc(row("x", elapsed=250.0)), exc(row("y", elapsed=250.0))]
    s = SA.summarize(rows, base)
    assert s["time_cap_exception"] is True and "slo_budget" not in s["reasons"]
    col = [c for c in s["time_cap_exception_columns"] if c["row"] == "x"][0]
    assert col == {"row": "x", "package": "p", "applied": True, "B_A1": 100.0, "elapsed_s": 250.0, "elapsed_over_baseline": 2.0,
                   "k_measured": 0, "k": 2, "messages_delivered": {"t4-1": 1, "t3-1": 0}}
    # a row's own slo_breach (hang_kill or above the widened hang guard) still counts
    bad = rows + [exc(row("z", slo=True)), exc(row("w", slo=True))]
    assert "slo_budget" in SA.summarize(bad, base)["reasons"]


def test_summary_off_is_unchanged_and_has_no_columns():
    s = SA.summarize([row("x")], BASE)
    assert s["time_cap_exception"] is False and s["time_cap_exception_columns"] is None
    rows = [row(f"r{i}") for i in range(10)] + [row("x", elapsed=250.0), row("y", elapsed=250.0)]
    assert "slo_budget" in SA.summarize(rows, BASE)["reasons"]


# ---------------------------------------------------------------- launch-panel.sh

def harness(world):
    h = world.tmp / "h"
    for d in ("bin", "config", "py"):
        shutil.copytree(R2 / d, h / d)
    return h


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fast_values():
    """A small, fast measured file for the fake claude: measured k = 0, so the exception applies."""
    return {"panel": "EL2", "pkg": PKG, "B_f": 20.0, "turn_p90_crit": 1.0, "T_report_p90_crit": 1.0, "E_recv": 10.0,
            "turn_p90_recv": 1.0, "T_report_p90_recv": 1.0, "hooks_s": 2.0, "panel_finish_at_s": 25.0, "k": 0,
            "sweeper_kill_s": 23.0, "hang_s": 30.0, "source": "spike4", "n_runs": 4}


def frozen_world(world):
    """A harness copy with a measured values file and its exception variant, both pinned (base + exception manifests)."""
    h = harness(world)
    for d in ("values", "values-exception"):
        shutil.rmtree(h / "config" / d)
        (h / "config" / d / "EL2").mkdir(parents=True)
    base = fast_values()
    (h / f"config/values/EL2/{PKG}.json").write_text(json.dumps(base) + "\n")
    (h / f"config/values-exception/EL2/{PKG}.json").write_text(json.dumps(V.exception_values(base)) + "\n")
    m = json.loads(world.manifest.read_text())
    m["sha256"][f"values/EL2/{PKG}.json"] = sha(h / f"config/values/EL2/{PKG}.json")
    world.manifest.write_text(json.dumps(m))
    m["sha256"][f"values-exception/EL2/{PKG}.json"] = sha(h / f"config/values-exception/EL2/{PKG}.json")
    (world.tmp / "manifest-exception.json").write_text(json.dumps(m))
    return h


def launch(world, h, row_name, *extra, env=None, collab=1):
    e = world.env
    e["PANEL_COLLAB"] = str(collab)
    e["R2_FINDINGS_PY"] = str(R2.parents[4] / "src/superclaude/cli/review/findings.py")  # the harness copy sits outside the repo
    e.update(env or {})
    return run(["bash", str(h / "bin/launch-panel.sh"), "--panel", "EL2", "--row", row_name, "--packages", PKG, *extra], env=e, timeout=300)


def test_bad_switch_value_refused_before_any_model_call(world):
    r = launch(world, harness(world), "x", env={"TIME_CAP_EXCEPTION": "2"})
    assert r.returncode == 2 and "TIME_CAP_EXCEPTION must be" in r.stderr and world.argv_log() == []


def test_on_without_manifest_copy_refused(world):
    r = launch(world, harness(world), "x", env={"TIME_CAP_EXCEPTION": "1"})
    assert r.returncode == 2 and "manifest-exception.json" in r.stderr and world.argv_log() == []


def test_on_with_slack_or_planning_refused(world):
    h = frozen_world(world)
    shutil.copy(world.tmp / "manifest-exception.json", world.tmp / "manifest-slack30.json")  # get past the slack checks
    r = launch(world, h, "x", env={"TIME_CAP_EXCEPTION": "1", "PANEL_SLACK_S": "30"})
    assert r.returncode == 2 and "cannot be combined" in r.stderr and world.argv_log() == []
    r = launch(world, h, "x", "--planning-values", env={"TIME_CAP_EXCEPTION": "1"})
    assert r.returncode == 2 and "planning" in r.stderr and world.argv_log() == []


def test_on_missing_exception_values_refused(world):
    h = frozen_world(world)
    shutil.rmtree(h / "config/values-exception")
    r = launch(world, h, "x", env={"TIME_CAP_EXCEPTION": "1"})
    assert r.returncode == 2 and "values-exception" in r.stderr and "TIME_CAP_EXCEPTION=1" in r.stderr and world.argv_log() == []


def test_on_values_sha_mismatch_refused(world):
    h = frozen_world(world)
    (h / f"config/values-exception/EL2/{PKG}.json").write_text(json.dumps({**V.exception_values(fast_values()), "hang_s": 9999}) + "\n")
    r = launch(world, h, "x", env={"TIME_CAP_EXCEPTION": "1"})
    assert r.returncode == 2 and "differs from manifest (values-exception/EL2/" in r.stderr and world.argv_log() == []


def test_on_other_checks_stay_in_force(world):
    h = frozen_world(world)
    r = launch(world, h, "x", env={"TIME_CAP_EXCEPTION": "1", "NOFALLBACK": ""})
    assert r.returncode == 2 and "NOFALLBACK" in r.stderr
    r = launch(world, h, "x", env={"TIME_CAP_EXCEPTION": "1", "SWEEPER_MODEL": "glm-5.3"})
    assert r.returncode == 2 and "not allowed" in r.stderr
    mp = world.tmp / "manifest-exception.json"           # the exception manifest is the one the launcher checks
    m = json.loads(mp.read_text())
    m["sha256"]["judge-one.sh"] = "1" * 64
    mp.write_text(json.dumps(m))
    r = launch(world, h, "x", env={"TIME_CAP_EXCEPTION": "1"})
    assert r.returncode == 2 and "judge-one.sh" in r.stderr and world.argv_log() == []


def posts(n):
    return [["--move", "M1", "--cmd", f"grep -rln w{i} tests/", "--item", "tests/test_other.py"] for i in range(n)]


def test_full_launch_on_then_off(world):
    h = frozen_world(world)
    world.scenario_set({"muse-ember-1.0#sw": {"posts": posts(2), "report": "done"},
                        "gpt-6-luna": {"sleep_before": 2, "tool_calls": [LS] * 8, "report": report()},
                        "default": {"report": report()}})
    # ---- on
    r = launch(world, h, "exc-on", env={"TIME_CAP_EXCEPTION": "1"})
    assert r.returncode == 0, r.stdout + r.stderr
    rd = world.out / "runs/exc-on"
    assert (rd / "time_cap_exception").read_text().strip() == "1"
    used = json.loads((rd / PKG / "values.json").read_text())
    assert used["k"] == 1 and used["hang_s"] == 60.0 and used["panel_finish_at_s"] == 58.0 and used["sweeper_kill_s"] == 56.0
    assert used["time_cap_exception"]["applied"] is True
    # the baked receiver hook carries k = 1 and the widened finish offset
    t0 = int((rd / PKG / "t0").read_text())
    cmd = json.loads(next((world.sbr / "board").glob(f"*/settings/{PKG}/t4-1.json")).read_text())["hooks"]["PostToolUse"][0]["hooks"][0]["command"]
    assert " --k 1 " in cmd and f"--finish-ms {t0 + 58000} " in cmd
    sw = json.loads((rd / PKG / "sweeper/sw-1.meta.json").read_text())
    assert sw["skipped_k0"] is False and sw["model_ok"] is True       # with k = 0 the sweeper would have been skipped
    res = json.loads((world.out / "results/exc-on.json").read_text())
    assert res["time_cap_exception"] is True and res["planning"] is False and res["invalid"] == []
    pp = res["per_package"][PKG]
    assert pp["time_cap_exception"] and pp["time_cap_exception_applied"]
    assert pp["B_A1"] == 20.0 and pp["k"] == 1 and pp["k_measured"] == 0
    assert pp["elapsed_over_baseline"] == pytest.approx(pp["elapsed_s"] / 20.0, abs=1e-3)
    assert set(pp["messages_delivered"]) == {"t2b-1", "t4-1", "t3-1"} and all(v <= 1 for v in pp["messages_delivered"].values())
    assert pp["messages_delivered"]["t4-1"] + pp["messages_delivered"]["t3-1"] >= 1
    # ---- resume with the switch changed is refused, no model call
    n = len(world.argv_log())
    r = launch(world, h, "exc-on")
    assert r.returncode == 2 and "TIME_CAP_EXCEPTION differs" in r.stderr and len(world.argv_log()) == n
    # ---- off: same harness, same values dir, nothing stamped, measured k = 0 so the sweeper is skipped
    r = launch(world, h, "exc-off")
    assert r.returncode == 0, r.stdout + r.stderr
    off = json.loads((world.out / "runs/exc-off" / PKG / "values.json").read_text())
    assert off == fast_values() and not (world.out / "runs/exc-off/time_cap_exception").exists()
    assert json.loads((world.out / "runs/exc-off" / PKG / "sweeper/sw-1.meta.json").read_text())["skipped_k0"] is True
    res = json.loads((world.out / "results/exc-off.json").read_text())
    assert res["time_cap_exception"] is False and res["per_package"][PKG]["time_cap_exception"] is False
    assert res["per_package"][PKG]["k"] == 0 and res["per_package"][PKG]["messages_delivered"] == {"t2b-1": 0, "t4-1": 0, "t3-1": 0}
