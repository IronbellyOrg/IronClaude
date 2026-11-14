"""launch-panel.sh step 0: refusals before any model call."""
import hashlib
import json
import shutil
import subprocess
import time

import pytest
from conftest import PKGS, R2, run

PKG = PKGS[2]


def copy_harness(world):
    """A private copy of bin/config/py so panels.json and values can be changed without touching R2."""
    h = world.tmp / "h"
    for d in ("bin", "config", "py"):
        shutil.copytree(R2 / d, h / d)
    return h


def launch(world, h=None, *args, env=None):
    e = world.env
    e.update(env or {})
    script = (h or R2) / "bin/launch-panel.sh"
    return run(["bash", str(script), *args], env=e, timeout=120)


def no_model_called(world):
    return world.argv_log() == []


def test_requires_nofallback(world):
    r = launch(world, None, "--panel", "EL2", "--row", "x", "--packages", PKG, "--planning-values", env={"NOFALLBACK": ""})
    assert r.returncode == 2 and "NOFALLBACK" in r.stderr and no_model_called(world)


@pytest.mark.parametrize("model", ["glm-5.3", "Qwen3.8-max", "claude-opus-5-5"])
def test_refuses_sweeper_model(world, model):
    r = launch(world, None, "--panel", "EL2", "--row", "x", "--packages", PKG, "--planning-values", env={"SWEEPER_MODEL": model})
    assert r.returncode == 2 and "not allowed" in r.stderr and no_model_called(world)


@pytest.mark.parametrize("model", ["glm-5.3", "Qwen3.8-max", "claude-opus-5-5"])
def test_refuses_reviewer_model(world, model):
    h = copy_harness(world)
    p = json.loads((h / "config/panels.json").read_text())
    p["EL2"]["reviewers"][0]["model"] = model
    (h / "config/panels.json").write_text(json.dumps(p))
    r = launch(world, h, "--panel", "EL2", "--row", "x", "--packages", PKG, "--planning-values")
    assert r.returncode == 2 and "not allowed" in r.stderr and no_model_called(world)


def test_refuses_values_sha_mismatch(world):
    h = copy_harness(world)
    vf = h / f"config/values/EL2/{PKG}.json"
    vf.parent.mkdir(parents=True, exist_ok=True)  # config/values/ exists since Spike 4 ran
    vf.write_text(json.dumps({"k": 2}))
    m = json.loads(world.manifest.read_text())
    m["sha256"][f"values/EL2/{PKG}.json"] = hashlib.sha256(b"other").hexdigest()
    world.manifest.write_text(json.dumps(m))
    r = launch(world, h, "--panel", "EL2", "--row", "x", "--packages", PKG)
    assert r.returncode == 2 and "differs from manifest" in r.stderr and no_model_called(world)


def test_refuses_missing_values_without_planning(world):
    h = copy_harness(world)
    shutil.rmtree(h / "config/values")  # the real folder exists since Spike 4 ran
    r = launch(world, h, "--panel", "EL2", "--row", "x", "--packages", PKG)
    assert r.returncode == 2 and "values file" in r.stderr


@pytest.mark.parametrize("row", ["Bad", "-x", "a" * 42, "a_b", ""])
def test_refuses_bad_row(world, row):
    r = launch(world, None, "--panel", "EL2", "--row", row, "--packages", PKG, "--planning-values")
    assert r.returncode == 2 and "bad --row" in r.stderr


def test_refuses_when_both_slots_held(world):
    world.sbr.mkdir(parents=True, exist_ok=True)
    holders = [subprocess.Popen(["flock", str(world.sbr / f"slot.{i}"), "sleep", "60"]) for i in (1, 2)]
    try:
        time.sleep(0.5)
        r = launch(world, None, "--panel", "EL2", "--row", "x", "--packages", PKG, "--planning-values")
        assert r.returncode == 2 and "concurrency slots" in r.stderr and no_model_called(world)
    finally:
        for p in holders:
            p.kill()


# ---- PANEL_SLACK_S (cap 1.35 B + 30 s): the launcher uses values-slack30/ and manifest-slack30.json

def slack_manifest(world, h, pkg=PKG, pin=None):
    """manifest-slack30.json next to the world's manifest, with a values-slack30 pin for EL2/pkg."""
    m = json.loads(world.manifest.read_text())
    vf = h / f"config/values-slack30/EL2/{pkg}.json"
    m["sha256"][f"values-slack30/EL2/{pkg}.json"] = pin or (hashlib.sha256(vf.read_bytes()).hexdigest() if vf.exists() else "0" * 64)
    (world.tmp / "manifest-slack30.json").write_text(json.dumps(m))


def test_slack_other_than_0_or_30_refused(world):
    r = launch(world, None, "--panel", "EL2", "--row", "x", "--packages", PKG, env={"PANEL_SLACK_S": "7"})
    assert r.returncode == 2 and "PANEL_SLACK_S must be" in r.stderr and no_model_called(world)


def test_slack30_without_manifest_copy_refused(world):
    r = launch(world, None, "--panel", "EL2", "--row", "x", "--packages", PKG, env={"PANEL_SLACK_S": "30"})
    assert r.returncode == 2 and "manifest-slack30.json" in r.stderr and no_model_called(world)


def test_slack30_missing_slack_values_exit_2_with_message(world):
    h = copy_harness(world)
    shutil.rmtree(h / "config/values-slack30")
    slack_manifest(world, h)
    r = launch(world, h, "--panel", "EL2", "--row", "x", "--packages", PKG, env={"PANEL_SLACK_S": "30"})
    assert r.returncode == 2 and "values-slack30" in r.stderr and "missing" in r.stderr and "PANEL_SLACK_S=30" in r.stderr
    assert no_model_called(world)


def test_slack30_values_sha_mismatch_refused(world):
    h = copy_harness(world)
    slack_manifest(world, h, pin=hashlib.sha256(b"other").hexdigest())
    r = launch(world, h, "--panel", "EL2", "--row", "x", "--packages", PKG, env={"PANEL_SLACK_S": "30"})
    assert r.returncode == 2 and "differs from manifest (values-slack30/EL2/" in r.stderr and no_model_called(world)


def test_slack30_with_planning_values_refused(world):
    h = copy_harness(world)
    slack_manifest(world, h)
    r = launch(world, h, "--panel", "EL2", "--row", "x", "--packages", PKG, "--planning-values", env={"PANEL_SLACK_S": "30"})
    assert r.returncode == 2 and "planning" in r.stderr and no_model_called(world)
