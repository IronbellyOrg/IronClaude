"""PANEL_SLACK_S (owner decision 2026-11-14): the time cap is 1.35 x B + SLACK_S."""

import json
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

# EL2 design package, Spike 4 numbers: B_f, luna turn p90, report turn p90.
B, TURN, REPORT = 137.81000018119812, 12.176000118255615, 13.604000091552734


@pytest.fixture(autouse=True)
def _no_slack(monkeypatch):
    monkeypatch.delenv("PANEL_SLACK_S", raising=False)


def test_default_is_zero_and_unchanged():
    assert values.slack_s() == 0
    assert values.compute_k(116, 6.4, 6.4) == 2
    assert abs(values.finish_offset(116, 6.4, 6.4) - 143.8) < 1e-9
    assert values.compute_n(0, 116, 116, 35, 2, 6, 6.4) == 2
    assert values.compute_k(B, TURN, REPORT) == 0
    assert paths.values_file("el2") == paths.R3 / "values" / "el2.json"


def test_k_changes_for_a_measured_case(monkeypatch):
    assert values.compute_k(B, TURN, REPORT) == 0
    monkeypatch.setenv("PANEL_SLACK_S", "30")
    assert (
        values.compute_k(B, TURN, REPORT) == 2
    )  # (0.35B + 30 - 2 - 12.2 - 13.6) / 24.35 = 2.07


def test_finish_offset_plus_slack(monkeypatch):
    base = values.finish_offset(B, TURN, REPORT)
    monkeypatch.setenv("PANEL_SLACK_S", "30")
    assert values.finish_offset(B, TURN, REPORT) == pytest.approx(base + 30)
    assert values.finish_at(1000.0, B, TURN, REPORT) == pytest.approx(1000 + base + 30)


def test_n_box_and_box_cap_plus_slack(monkeypatch):
    assert values.compute_n(0, 116, 116, 35, 2, 6, 12.2) == 1
    assert values.compute_n(0, 116, 132.01, 35, 2, 6, 12.2) == 0
    assert values.compute_n(0, 238, 238, None, 3, 6, 33) == 0
    monkeypatch.setenv("PANEL_SLACK_S", "30")
    assert values.compute_n(0, 116, 116, 35, 2, 6, 12.2) == 2
    assert values.compute_n(0, 116, 132.01, 35, 2, 6, 12.2) == 1
    assert values.compute_n(0, 238, 238, None, 3, 6, 33) == 1


@pytest.mark.parametrize("bad", ["abc", "-1", "nan", "inf"])
def test_bad_slack_refused(monkeypatch, bad):
    monkeypatch.setenv("PANEL_SLACK_S", bad)
    with pytest.raises(SystemExit, match="E_SLACK"):
        values.slack_s()


def test_summary_cap_check_plus_slack(monkeypatch):
    rows = [row("A1", 100) for _ in range(3)] + [
        row("A3", 140),
        row("A3", 160, oj=0.5),
        row("A3", 120, lr=5),
    ]
    monkeypatch.setenv("PANEL_SLACK_S", "30")
    cap = metrics.summarize(rows, "el2")["cap_check"][P]
    # cap is 165 s: median 140 fits, nothing is over it; the 1.5 x B_c limit (150 s) is unchanged
    assert cap["median_ok"] is True and cap["over_135"] == 0 and cap["over_150"] == 1


def test_slack_values_dir_and_checks(monkeypatch, tmp_path):
    monkeypatch.delenv("R3_VALUES_FILE", raising=False)
    monkeypatch.setenv("PANEL_SLACK_S", "7")  # no values-slack7/ exists
    assert paths.values_file("el2") == paths.R3 / "values-slack7" / "el2.json"
    with pytest.raises(SystemExit, match="PANEL_SLACK_S=7 needs the slack values"):
        values.load("el2")
    # planning values (smoke) follow the slack too
    assert values.planning("el2")["slack_s"] == 7
    # a file frozen without slack is refused when slack is on
    f = tmp_path / "el2.json"
    v = {"status": "frozen", "packages": {}, "turn_p90": {}}
    f.write_text(json.dumps(v))
    (tmp_path / "el2.json.sha256").write_text(values.sha256_file(f) + "\n")
    monkeypatch.setenv("R3_VALUES_FILE", str(f))
    # tmp_path is under /tmp/ for pytest on this host
    with pytest.raises(SystemExit, match="frozen with slack_s=0"):
        values.load("el2")
    v["slack_s"] = 7
    f.write_text(json.dumps(v))
    (tmp_path / "el2.json.sha256").write_text(values.sha256_file(f) + "\n")
    assert values.load("el2")[0]["slack_s"] == 7


@pytest.mark.slow
@pytest.mark.parametrize("slack", [0, 30])
def test_launcher_p2_deadline_includes_slack(env, slack):
    """Fake claude, collab 0: pkg.json P2_DEADLINE = T0 + 1.30 B_f + SLACK_S; the hang guard stays 1.5 B_f."""
    write_values(env)
    f = Path(env["env"]["R3_VALUES_FILE"])
    v = json.loads(f.read_text())
    v["slack_s"] = slack
    f.write_text(json.dumps(v))
    Path(str(f) + ".sha256").write_text(values.sha256_file(f) + "\n")
    mini_sandbox(env)
    write_plan(env, default_rules(env))
    r, rd = launch(
        env, collab=0, extra=["--no-judge"], envx={"PANEL_SLACK_S": str(slack)}
    )
    assert r.returncode == 0, r.stderr
    pj = jload(rd / CONTROL / "pkg.json")
    assert pj["P2_DEADLINE"] - pj["T0"] == pytest.approx(1.30 * 40.0 + slack, abs=0.01)
    assert pj["HANG_AT"] - pj["T0"] == pytest.approx(1.5 * 40.0, abs=0.01)
    assert jload(rd / "run.json")["slack_s"] == slack


def test_launcher_exits_2_without_slack_values(env):
    e = dict(env["env"], PANEL_SLACK_S="7", PANEL_COLLAB="1")
    e.pop("R3_VALUES_FILE")
    r = subprocess.run(
        ["bash", str(paths.R3 / "bin/launch-panel.sh"), "el2"],
        env=e,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert r.returncode == 2 and "values-slack7/el2.json" in r.stderr
    assert not (env["root"] / "runs").exists()
