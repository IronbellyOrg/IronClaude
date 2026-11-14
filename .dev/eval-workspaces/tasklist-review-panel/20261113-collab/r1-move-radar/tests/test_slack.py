# ruff: noqa: N803, F811  (B is the design's own symbol; lenv is the imported fixture)
"""PANEL_SLACK_S (owner decision 2026-11-14): the cap is 1.35 B + SLACK_S. Default 0 must leave every earlier value unchanged."""

import hashlib
import importlib.util
import json
import os

import pytest
from conftest import TOOLS, jload, run
from test_launch import DS, lenv  # noqa: F401  (the fixture and the package id)
from test_values import _row, attempt_fixture

spec = importlib.util.spec_from_file_location("values_slack", TOOLS / "values.py")
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)

# Measured sl2 / designSpec inputs (values/sl2/<DS>.json, Spike 4 rows sl2-c0-r1..3): k reader was 0 without slack.
SL2_B = 165.823
SL2_TURN = {"searcher": 33.472999811172485, "reader": 15.739000082015991}
SL2_TREP = {"searcher": 52.08899998664856, "reader": 62.17400002479553}
SL2_E = {"searcher": 199.436, "reader": 124.989}


@pytest.fixture
def slack30(monkeypatch):
    monkeypatch.setenv("PANEL_SLACK_S", "30")


@pytest.fixture
def slack0(monkeypatch):
    monkeypatch.delenv("PANEL_SLACK_S", raising=False)


def test_default_is_zero_and_unchanged(slack0):
    assert V.slack_s() == 0 and V.values_dir() == "values"
    assert V.k_for(100, 6.4, 13.9) == 0 and V.k_for(116, 6.4, 6.4) == 2
    assert V.finish_offset(100, 10, 5) == pytest.approx(120.0)
    assert V.guard_offset(100, 120.0, 47) == pytest.approx(88.0)


def test_empty_value_is_zero_and_negative_is_refused(monkeypatch):
    monkeypatch.setenv("PANEL_SLACK_S", "")
    assert V.slack_s() == 0
    monkeypatch.setenv("PANEL_SLACK_S", "-1")
    with pytest.raises(SystemExit):
        V.slack_s()


def test_slack30_changes_k_finish_and_guard(slack30):
    assert V.values_dir() == "values-slack30"
    assert V.k_for(100, 6.4, 13.9) == 2  # was 0 at slack 0 (the case pinned in test_values.py): (35 + 30 - 2 - 6.4 - 13.9) / 12.8 = 3.4
    assert V.k_for(238, 23, 23) == 1  # was 0 (pinned in test_values.py): (83.3 + 30 - 2 - 23 - 23) / 46 = 1.42
    assert V.finish_offset(100, 10, 5) == pytest.approx(150.0)  # +30
    assert V.guard_offset(100, 150.0, 47) == pytest.approx(118.0)  # 1.35 B - G + 30


def test_slack30_sl2_designspec_reader_k_0_to_1(monkeypatch):
    cfg = jload(TOOLS.parent / "config" / "panels.json")["sl2"]
    monkeypatch.delenv("PANEL_SLACK_S", raising=False)
    old = V.compute("sl2", cfg, SL2_B, SL2_TURN, SL2_TREP, SL2_E)
    monkeypatch.setenv("PANEL_SLACK_S", "30")
    new = V.compute("sl2", cfg, SL2_B, SL2_TURN, SL2_TREP, SL2_E)
    assert old["k"] == {"searcher": 0, "reader": 0}
    assert new["k"] == {"searcher": 0, "reader": 1}
    assert new["finish_offset_s"] == pytest.approx(old["finish_offset_s"] + 30)
    assert new["guard_offset_s"] == pytest.approx(old["guard_offset_s"] + 30)
    assert new["hang_offset_s"] == old["hang_offset_s"] == pytest.approx(1.5 * SL2_B)  # the hang guard is not derived from the cap
    assert new["slack_s"] == 30 and old["slack_s"] == 0


def test_finish_offset_plus_30_on_every_panel(monkeypatch):
    cfg = jload(TOOLS.parent / "config" / "panels.json")
    for p in ("el2", "sl2", "hl2"):
        monkeypatch.delenv("PANEL_SLACK_S", raising=False)
        a = V.planning(p, cfg[p])
        monkeypatch.setenv("PANEL_SLACK_S", "30")
        b = V.planning(p, cfg[p])
        assert b["finish_offset_s"] == pytest.approx(a["finish_offset_s"] + 30)
        assert b["hang_offset_s"] == a["hang_offset_s"]
        assert all(b["k"][r] >= a["k"][r] for r in a["k"])


def _fill_rows(root):
    for i, row in enumerate(["el2-c0-r1", "el2-c0-r2", "el2-c0-r3"]):
        for p in V.PKGS:
            _row(root, row, p, 0, {"t2b-1": 100_000 + i * 1000, "t4-1": 110_000, "t3-1": 120_000 + i * 2000}, attempt_fixture())


def spike4(root, env):
    return run(["uv", "run", "python", str(TOOLS / "values.py"), "spike4", "el2", "el2-c0-r1", "el2-c0-r2", "el2-c0-r3", "--root", str(root)], env=env)


def test_spike4_slack_writes_new_dir_and_keeps_the_old(root):
    _fill_rows(root)
    env0 = {k: v for k, v in os.environ.items() if k != "PANEL_SLACK_S"}
    env30 = dict(env0, PANEL_SLACK_S="30")
    assert spike4(root, env0).returncode == 0
    old = (root / "values" / "el2" / f"{V.PKGS[0]}.json").read_bytes()
    r = spike4(root, env30)
    assert r.returncode == 0, r.stderr
    assert (root / "values" / "el2" / f"{V.PKGS[0]}.json").read_bytes() == old  # the original file is untouched
    f = root / "values-slack30" / "el2" / f"{V.PKGS[0]}.json"
    a, b = jload(root / "values" / "el2" / f"{V.PKGS[0]}.json"), jload(f)
    assert b["slack_s"] == 30 and b["B_f"] == a["B_f"] and b["turn_p90"] == a["turn_p90"]
    assert b["finish_offset_s"] == pytest.approx(a["finish_offset_s"] + 30)
    assert f.with_name(f.name + ".sha256").read_text().split()[0] == hashlib.sha256(f.read_bytes()).hexdigest()
    again = spike4(root, env30)
    assert again.returncode == 2 and "written once" in again.stderr and "values-slack30" in again.stderr


def test_load_and_deadlines_follow_the_slack_dir(root):
    _fill_rows(root)
    env0 = {k: v for k, v in os.environ.items() if k != "PANEL_SLACK_S"}
    env30 = dict(env0, PANEL_SLACK_S="30")
    cmd = ["uv", "run", "python", str(TOOLS / "values.py"), "deadlines", "el2", V.PKGS[0], "1", "1000", "--root", str(root)]
    assert run(cmd, env=env30).returncode == 2  # no slack values yet: refused, also for collab 0 (no planning fallback with slack)
    assert run(cmd[:-5] + ["0", "1000", "--root", str(root)], env=env30).returncode == 2
    assert spike4(root, env0).returncode == 0 and spike4(root, env30).returncode == 0
    d0 = json.loads(run(cmd, env=env0).stdout)
    d30 = json.loads(run(cmd, env=env30).stdout)
    assert d30["slack_s"] == 30 and d0["slack_s"] == 0 and d30["values"] != d0["values"]
    assert d30["FINISH_MS"] - d0["FINISH_MS"] == 30_000 and d30["HANG_MS"] == d0["HANG_MS"]
    # a values file computed with another slack than the env is never used
    bad = root / "values" / "el2" / f"{V.PKGS[1]}.json"
    cmd2 = cmd[:6] + [V.PKGS[1]] + cmd[7:]
    (root / "values-slack30" / "el2" / bad.name).write_bytes(bad.read_bytes())
    (root / "values-slack30" / "el2" / (bad.name + ".sha256")).write_bytes((bad.parent / (bad.name + ".sha256")).read_bytes())
    r = run(cmd2, env=env30)
    assert r.returncode != 0 and "slack_s" in r.stderr


def test_alarms_slo_limit_adds_slack(root):
    from test_alarms import P, alarms, row
    rows = [row(0, 1), row(0, 2), row(0, 3), row(1, 1, elapsed=170.0)]  # 1.35 x 116 = 156.6 < 170 < 186.6
    assert alarms(root, rows)[0]["arms"]["collab1"]["slo_spent"] == [["el2-c1-r1", P]]
    os.environ["PANEL_SLACK_S"] = "30"
    try:
        assert alarms(root, rows)[0]["arms"]["collab1"]["slo_spent"] == []
    finally:
        del os.environ["PANEL_SLACK_S"]


# ---------------------------------------------------------------- launch.sh
def test_launcher_refuses_without_slack_values(lenv):
    for collab in (1, 0):
        r = lenv.launch(collab=collab, rep=0, PANEL_SLACK_S=30)
        assert r.returncode == 2 and "values-slack30/el2/" in r.stderr and "PANEL_SLACK_S=30" in r.stderr
        assert not (lenv.root / "runs" / f"el2-c{collab}-r0" / "launch.log").exists()
    for bad in ("abc", "-5", "3.5", "030", ""):
        r = lenv.launch(collab=0, rep=0, PANEL_SLACK_S=bad)
        assert r.returncode == 2 and "PANEL_SLACK_S" in r.stderr, bad


def test_launcher_uses_slack_values(lenv):
    cmd = ["uv", "run", "python", str(TOOLS / "values.py"), "show", "el2", DS, "--root", str(lenv.root)]
    body = run(cmd, env=dict(lenv.env, PANEL_SLACK_S="30")).stdout
    d = lenv.root / "values-slack30" / "el2"
    d.mkdir(parents=True)
    (d / f"{DS}.json").write_text(body)
    (d / f"{DS}.json.sha256").write_text(hashlib.sha256(body.encode()).hexdigest() + f"  {DS}.json\n")
    r = lenv.launch(collab=1, rep=0, PANEL_SLACK_S=30)
    assert r.returncode == 0, r.stdout + r.stderr
    run_json = jload(lenv.d("el2-c1-r0") / "run.json")
    assert run_json["slack_s"] == 30 and run_json["values"] == hashlib.sha256(body.encode()).hexdigest()
    assert run_json["FINISH_MS"] - run_json["T0_MS"] == round(1000 * (1.35 * 116 - 6.4 - 6.4 + 30))  # planning el2, +30 s
    assert run_json["HANG_MS"] - run_json["T0_MS"] == round(1000 * 1.5 * 116)
