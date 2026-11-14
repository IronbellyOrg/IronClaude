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
    vf.parent.mkdir(parents=True)
    vf.write_text(json.dumps({"k": 2}))
    m = json.loads(world.manifest.read_text())
    m["sha256"][f"values/EL2/{PKG}.json"] = hashlib.sha256(b"other").hexdigest()
    world.manifest.write_text(json.dumps(m))
    r = launch(world, h, "--panel", "EL2", "--row", "x", "--packages", PKG)
    assert r.returncode == 2 and "differs from manifest" in r.stderr and no_model_called(world)


def test_refuses_missing_values_without_planning(world):
    r = launch(world, None, "--panel", "EL2", "--row", "x", "--packages", PKG)
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
