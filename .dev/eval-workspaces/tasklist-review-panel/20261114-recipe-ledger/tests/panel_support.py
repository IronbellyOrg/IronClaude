"""Shared by the launcher tests (Task 13): a sandbox built from the invented F-REPO under /tmp/evalsb-recipe-test-*, and a
call of bin/run-panel.sh on the fake claude. Nothing here starts a model; the run folders go to a temporary folder
(RL_RUNS_ROOT), never to RL/runs."""

import itertools
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from types import SimpleNamespace

import pytest
from conftest import FAKES, assert_fake_first
from helpers import SW

from fixtures.repos.build_repo import build_repo

SCRIPT = SW / "bin" / "run-panel.sh"
BUILD = SW / "bin" / "build-sandbox.sh"
EMBER, L1, L2 = "t2b-1", "t4-1", "t3-1"  # reviewer ids of the primary panel
EMBER_MODEL, LUNA_MODEL = "muse-ember-1.0", "gpt-6-luna"
_count = itertools.count(1)


def base_env(root: Path) -> dict:
    env = {
        k: v for k, v in os.environ.items() if not k.startswith(("SW_", "FAKE_", "RL_"))
    }
    env.update(
        PATH=f"{FAKES}{os.pathsep}{os.environ['PATH']}",
        SW_SB_ROOT=str(root / "sb"),
        NOFALLBACK="1",
        PYTHONDONTWRITEBYTECODE="1",
        RL_RUNS_ROOT=str(root / "runs"),
    )
    assert_fake_first(env)
    return env


def make_sandbox(root: Path, raw=False, source=True) -> SimpleNamespace:
    """The sandbox of one invented document (and, with raw, its repo-raw) under root/sb."""
    root.mkdir(parents=True, exist_ok=True)
    fx = build_repo(root / "src")
    packages = {
        "schema": "sweep-packages/1",
        "packages": {
            fx.doc_id: {
                "kind": "plan",
                "set": "fixture",
                "base": fx.base,
                "candidate": str(SW / "fixtures" / "plans" / "p_basic.md"),
                "source": str(SW / "fixtures" / "plans" / "source.md")
                if source
                else None,
                "masked_paths": [],
            }
        },
        "order": [fx.doc_id],
    }
    pk = root / "packages.json"
    pk.write_text(json.dumps(packages), encoding="utf-8")
    env = dict(base_env(root), SW_SRC_REPO=str(fx.repo))
    for flags in ([], ["--raw"]) if raw else ([],):
        r = subprocess.run(
            ["bash", str(BUILD), *flags, "--packages", str(pk), fx.doc_id],
            capture_output=True,
            text=True,
            env=env,
            timeout=120,
        )
        assert r.returncode == 0, r.stderr
    sb = root / "sb"
    return SimpleNamespace(
        root=root,
        doc=fx.doc_id,
        sb=sb,
        repo=sb / fx.doc_id / "repo",
        cand=sb / "cand" / fx.doc_id / "candidate.md",
        source=sb / "cand" / fx.doc_id / "source.md",
    )


def new_root() -> Path:
    return Path(tempfile.mkdtemp(prefix="evalsb-recipe-test-", dir="/tmp"))


@pytest.fixture(scope="session")
def sandbox():
    """One clean sandbox for the tests that only read it (the launcher leaves it clean)."""
    root = new_root()
    yield make_sandbox(root, raw=True)
    shutil.rmtree(root, ignore_errors=True)


@pytest.fixture
def own_sandbox():
    """A sandbox of its own, for a test that dirties it."""
    root = new_root()
    yield make_sandbox(root)
    shutil.rmtree(root, ignore_errors=True)


def calls(path: Path) -> list[list[str]]:
    """[[epoch, scenario, requested model, kind]] of the fake claude's call log."""
    return (
        [ln.split("\t") for ln in path.read_text().splitlines()]
        if path.exists()
        else []
    )


def run_panel(
    box, scenario="ok", arm="RL", panel="primary", b="100", extra=(), env=None, drop=()
):
    """Run the launcher on the fake claude; returns a namespace with the result, the run folder and its call log."""
    run_id = f"t{next(_count)}-{os.getpid()}"
    root = box.root
    log = root / f"{run_id}.calls"
    e = dict(
        base_env(root), FAKE_SCENARIO=scenario, FAKE_CALL_LOG=str(log), **(env or {})
    )
    for k in drop:
        e.pop(k, None)
    cmd = [
        "bash",
        str(SCRIPT),
        "--arm",
        arm,
        "--panel",
        panel,
        "--doc",
        box.doc,
        "--replicate",
        "1",
        "--block",
        "1",
    ]
    cmd += ["--seed", "1", "--run-id", run_id, *(["--b", b] if b else []), *extra]
    r = subprocess.run(cmd, capture_output=True, text=True, env=e, timeout=180)
    run = root / "runs" / run_id

    def js(name):
        return json.loads((run / name).read_text())

    return SimpleNamespace(
        rc=r.returncode,
        out=r.stdout,
        err=r.stderr,
        run=run,
        log=log,
        calls=calls(log),
        js=js,
        env=e,
        cmd=cmd,
    )


@pytest.fixture(scope="session")
def ok_runs(sandbox):  # noqa: F811
    """Three finished runs shared by the tests that only read run folders: RL ok, Z0 ok, RL with a PROBLEM row."""
    runs = SimpleNamespace(
        rl=run_panel(sandbox),
        z0=run_panel(sandbox, arm="Z0"),
        problem=run_panel(sandbox, "problem"),
    )
    for r in (runs.rl, runs.z0, runs.problem):
        assert r.rc == 0, r.err
    return runs
