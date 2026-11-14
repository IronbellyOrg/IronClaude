"""PANEL_SLACK_S (owner decision 2026-11-14): the time cap is 1.35 B + SLACK_S. Default 0 leaves every old value unchanged."""

import json
import shutil
from pathlib import Path

import pytest
from r4help import R4, REPO, make_sbr, run, write_values

import values


def test_default_unchanged(monkeypatch):
    monkeypatch.delenv("PANEL_SLACK_S", raising=False)
    assert values.slack_s() == 0
    assert values.k_of(116, 6.4, 6.4) == values.k_of(116, 6.4, 6.4, slack=0) == 2
    assert values.finish_offset(116, 6.4, 6.4) == pytest.approx(143.8)
    monkeypatch.setenv("PANEL_SLACK_S", "0")
    assert values.finish_offset(116, 6.4, 6.4) == pytest.approx(143.8)
    assert values.slowdown_limit(116, 6.4, 1) == pytest.approx(0.167, abs=5e-4)


def test_slack_changes_k_from_zero(monkeypatch):
    monkeypatch.delenv("PANEL_SLACK_S", raising=False)
    assert values.k_of(116, 14, 14) == 0                 # 40.6 - 2 - 28 = 10.6 s, less than 2 turns
    assert values.k_of(116, 14, 14, slack=30) == 1       # 40.6 + 30 - 2 - 28 = 40.6 s, 1.45 x 28
    assert values.k_of(258.964, 15.382, 22.088) == 1     # measured SL2 design package
    assert values.k_of(258.964, 15.382, 22.088, slack=30) == 2
    monkeypatch.setenv("PANEL_SLACK_S", "30")
    assert values.k_of(116, 14, 14) == 1                 # the environment gives the same answer as the argument


def test_slack_integer_ms_threshold(monkeypatch):
    # (0.35 * 100 + 30 - 2 - 6.4 - 13.9) / 12.8 = 42.7 / 12.8 -> k 3 capped to 2; at turn 23: (35 + 30 - 2 - 23 - 23) / 46 = 17/46 -> 0
    assert values.k_of(100, 6.4, 13.9, slack=30) == 2
    assert values.k_of(100, 23, 23, slack=30) == 0
    assert values.k_of(100, 20, 20, slack=30) == 0       # 65 - 2 - 40 = 23 s, 20 s turn needs 40 s
    assert values.k_of(100, 10, 10, slack=30) == 2       # 65 - 2 - 20 = 43 s / 20 s = 2.15 -> 2


def test_finish_offset_and_hang(monkeypatch):
    assert values.finish_offset(116, 6.4, 6.4, slack=30) == pytest.approx(143.8 + 30)
    monkeypatch.setenv("PANEL_SLACK_S", "30")
    assert values.finish_offset(116, 6.4, 6.4) == pytest.approx(173.8)
    assert values.hang_s(116) == pytest.approx(174.0)    # the hang guard is not derived from the 35% cap


def test_slowdown_limit_with_slack():
    assert values.slowdown_limit(116, 6.4, 1, slack=30) == pytest.approx(0.167 + 30 / 116, abs=5e-4)
    assert values.slowdown_limit(116, 6.4, 0, slack=30) is None


def test_bad_slack_env(monkeypatch):
    monkeypatch.setenv("PANEL_SLACK_S", "abc")
    with pytest.raises(SystemExit):
        values.slack_s()


def test_cli_writes_slack_dir_and_stamp(env, tmp_path):
    env = dict(env, PANEL_SLACK_S="30")
    r = run(["uv", "run", "--frozen", "--project", str(REPO), "python", str(R4 / "lib" / "values.py"), "planning", "--panel", "EL2"], env=env)
    assert r.returncode == 0, r.stderr
    p = tmp_path / "out" / "values-slack30" / "planning-EL2.json"
    assert r.stdout.strip() == str(p) and not (tmp_path / "out" / "values").exists()
    d = json.loads(p.read_text())
    assert d["slack_s"] == 30
    pl = d["packages"][next(iter(d["packages"]))]
    assert pl["finish_offset_s"] == pytest.approx(values.finish_offset(pl["B_A1"], pl["turn_p90"], pl["T_report_p90"], slack=30))


def test_arm_summary_slack(monkeypatch):
    import importlib

    import arm_summary
    monkeypatch.setenv("PANEL_SLACK_S", "30")
    importlib.reload(arm_summary)
    try:
        assert arm_summary.SLACK_S == 30
    finally:
        monkeypatch.delenv("PANEL_SLACK_S")
        importlib.reload(arm_summary)
    assert arm_summary.SLACK_S == 0


def _launch(env, row, **extra):
    return run([R4 / "bin" / "run-panel.sh", "--panel", "EL2", "--row", row, "--seed", "5"], env=dict(env, PANEL_COLLAB="1", **extra))


def test_launcher_slack_refusals(env, monkeypatch):
    make_sbr(env)
    out = Path(env["R4_OUT"])
    # 1. PANEL_SLACK_S=30 and no slack values for the panel: exit 2 with a clear message, nothing started
    r = _launch(env, "sl1", PANEL_SLACK_S="30")
    assert r.returncode == 2 and "slack values file for EL2 is missing" in r.stderr, r.stderr
    # 2. a values file without slack (the old values) is refused under PANEL_SLACK_S=30
    old = write_values(env, B=4.0, turn=40, rep=40, name="old.json")
    r = run([R4 / "bin/run-panel.sh", "--panel", "EL2", "--row", "sl2", "--values", old], env=dict(env, PANEL_COLLAB="1", PANEL_SLACK_S="30"))
    assert r.returncode == 2 and "slack_s (0) differs from PANEL_SLACK_S=30" in r.stderr, r.stderr
    # 3. a slack values file is refused when PANEL_SLACK_S is not set
    monkeypatch.setenv("PANEL_SLACK_S", "30")
    new = write_values(env, B=4.0, turn=40, rep=40, name="new.json")
    monkeypatch.delenv("PANEL_SLACK_S")
    sd = out / "values-slack30"
    sd.mkdir()
    for s in ("", ".sha256"):
        shutil.copy(str(new) + s, sd / f"EL2.json{s}")
    r = run([R4 / "bin/run-panel.sh", "--panel", "EL2", "--row", "sl3", "--values", sd / "EL2.json"], env=dict(env, PANEL_COLLAB="1"))
    assert r.returncode == 2 and "slack_s (30) differs from PANEL_SLACK_S=0" in r.stderr, r.stderr
    # 4. with PANEL_SLACK_S=30 and no --values the launcher picks values-slack30/EL2.json (B = 4 s: k = 0 on every package, still refused)
    r = _launch(env, "sl4", PANEL_SLACK_S="30")
    assert r.returncode == 2 and "F7 not runnable on EL2: k = 0 on every package" in r.stderr, r.stderr
    assert not (out / "runs" / "sl4").exists()
    r = run([R4 / "bin/run-panel.sh", "--panel", "EL2", "--row", "sl5"], env=dict(env, PANEL_COLLAB="1", PANEL_SLACK_S="30x"))
    assert r.returncode == 2 and "not a plain non-negative number" in r.stderr
