import os
import subprocess

import pytest
from conftest import EVAL, R3, REPO, launch

from r3lib import values


def sh(cmd, env=None):
    e = {k: v for k, v in os.environ.items() if not k.startswith("R3_")}
    e.update(env or {})
    return subprocess.run(
        ["bash", "-c", f"source {R3}/lib/common.sh; {cmd}"],
        capture_output=True,
        text=True,
        env=e,
    )


def test_writable_accepts(tmp_path):
    assert sh(f"r3_assert_writable {R3}/runs/x").returncode == 0
    assert sh("r3_assert_writable /tmp/evalsb-collab-r3/TASK-WF-x/repo").returncode == 0
    assert (
        sh(
            f"r3_assert_writable {tmp_path}/runs/a",
            {"R3_RUNS_ROOT": str(tmp_path / "runs")},
        ).returncode
        == 0
    )


def test_writable_refuses(tmp_path):
    others = (
        "r1-move-radar",
        "r2-idle-shift-sweeper",
        "r4-flag-and-adjudicate",
        "r5-coverage-deflection",
    )
    for p in (
        REPO / "src/superclaude/x.py",
        EVAL / "x",
        *(R3 / ".." / o / "x" for o in others),
    ):
        assert sh(f"r3_assert_writable '{p}'").returncode == 1, p
    link = R3 / "zz-test-link-to-eval"
    try:
        os.symlink(EVAL, link)
        assert sh(f"r3_assert_writable '{link}/x'").returncode == 1
    finally:
        link.unlink()
    assert (
        sh(
            f"r3_assert_writable {R3}/runs/x", {"R3_RUNS_ROOT": "/home/coder/not-tmp"}
        ).returncode
        == 1
    )


def admit(tmp_path, total, ember, here):
    fakes = R3 / "tests" / "fakes"
    lock = tmp_path / "admit.lock"
    r = sh(
        f"r3_admit {lock} {here} 1; rc=$?; flock -n {lock} true && echo released; exit $rc",
        {
            "PATH": f"{fakes}:{os.environ['PATH']}",
            "FAKE_PGREP_TOTAL": str(total),
            "FAKE_PGREP_EMBER": str(ember),
        },
    )
    return r.returncode, "released" in r.stdout


def test_admission(tmp_path):
    assert admit(tmp_path, 7, 0, 1) == (0, False) or admit(tmp_path, 7, 0, 1)[0] == 0
    rc, _ = admit(tmp_path, 7, 0, 1)
    assert rc == 0
    rc, rel = admit(tmp_path, 8, 0, 1)
    assert rc == 1 and rel
    assert admit(tmp_path, 3, 3, 1)[0] == 0
    rc, rel = admit(tmp_path, 4, 4, 1)
    assert rc == 1 and rel


def test_admission_lock_released_after_success(tmp_path):
    fakes = R3 / "tests" / "fakes"
    lock = tmp_path / "admit.lock"
    r = sh(
        f"r3_admit {lock} 1 1; flock -u 8; exec 8>&-; flock -n {lock} true && echo released",
        {"PATH": f"{fakes}:{os.environ['PATH']}", "FAKE_PGREP_TOTAL": "0"},
    )
    assert "released" in r.stdout


def test_switches(env):
    for extra, envx, why in (
        ([], {"PANEL_COLLAB": "2"}, "E_BAD_SWITCH"),
        ([], {"NOFALLBACK": "0"}, "E_NOFALLBACK"),
        ([], {"R3_SPIKE4": "1"}, "R3_SPIKE4"),
    ):
        r, _ = launch(env, collab=envx.pop("PANEL_COLLAB", 1), envx=envx)
        assert r.returncode == 1 and why in r.stderr, r.stderr
    r, _ = launch(env)  # no values file at R3_VALUES_FILE
    assert r.returncode == 1 and "values" in r.stderr


def test_values_required_unless_smoke_or_spike4(tmp_path, monkeypatch):
    monkeypatch.setenv("R3_VALUES_FILE", str(tmp_path / "none.json"))
    with pytest.raises(SystemExit):
        values.load("el2")
    assert values.load("el2", smoke=True)[0]["status"] == "planning"
    assert values.load("el2", spike4=True)[0]["status"] == "planning"
