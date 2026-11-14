"""Shared helpers for the offline tests (design section 6). No test calls a real model:
tests/fake-claude is put first on PATH as `claude`, and HOME is a temporary directory."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

R4 = Path(__file__).resolve().parents[1]
REPO = R4.parents[4]
EVAL = REPO / ".dev/eval-workspaces/tasklist-review-panel/20261111-a1"
DS, AL, DE = "TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"
PKGS = [DS, AL, DE]
sys.path.insert(0, str(R4 / "lib"))


def now_ms() -> int:
    return int(time.time() * 1000)


def run(cmd, env=None, input=None, cwd=None, timeout=300):
    return subprocess.run([str(c) for c in cmd], env=env, input=input, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def jsonl(p):
    p = Path(p)
    if not p.exists():
        return []
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]


@pytest.fixture
def env(tmp_path):
    home = tmp_path / "home"
    (home / ".claude" / "projects").mkdir(parents=True)
    fakebin = tmp_path / "fakebin"
    fakebin.mkdir()
    (fakebin / "claude").symlink_to(R4 / "tests" / "fake-claude")
    uv_cache = subprocess.run(["uv", "cache", "dir"], capture_output=True, text=True).stdout.strip()
    e = {
        "PATH": f"{fakebin}:{os.environ['PATH']}",
        "HOME": str(home),
        "UV_CACHE_DIR": uv_cache,
        "UV_PYTHON_INSTALL_DIR": os.path.expanduser("~/.local/share/uv/python"),
        "R4_SBR": str(tmp_path / "sbr"),
        "R4_OUT": str(tmp_path / "out"),
        "R4_REPO": str(REPO),
        "FAKE_LOG": str(tmp_path / "fakelog"),
        "NOFALLBACK": "1",
        "LANG": "C.UTF-8",
    }
    (tmp_path / "out").mkdir()
    return e


def fixture(env, obj, tmp_path):
    p = tmp_path / f"fake-{len(list(tmp_path.glob('fake-*.json')))}.json"
    p.write_text(json.dumps(obj))
    env["FAKE_CLAUDE_SCRIPT"] = str(p)
    return p


def flat_file(src: Path, dst: Path):
    text = src.read_text()
    dst.write_text(" ".join(text.replace("\n", " ").split()) + "\n")


def make_sbr(env, pkgs=PKGS):
    """Small stand-in sandboxes (one committed file each) plus real candidate/source copies and a manifest."""
    sbr, out = Path(env["R4_SBR"]), Path(env["R4_OUT"])
    man = []
    for p in pkgs:
        repo = sbr / "sb" / p / "repo"
        repo.mkdir(parents=True)
        (repo / "README.md").write_text("sandbox\n")
        for c in (["init", "-q"], ["add", "-A"], ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "s"]):
            subprocess.run(["git", "-C", str(repo)] + c, check=True)
        (sbr / "sb" / p / "built.json").write_text(json.dumps({"tree": "x", "files": 1, "removed": []}))
        cd = sbr / "cand" / p
        cd.mkdir(parents=True)
        shutil.copy(EVAL / p / "candidate.md", cd / "candidate.md")
        shutil.copy(REPO / ".dev/tasks/done" / p / "source.md", cd / "source.md")
        flat_file(cd / "candidate.md", cd / "candidate.flat")
        man.append({"package": p, "candidate_sha256": hashlib.sha256((cd / "candidate.md").read_bytes()).hexdigest()})
    (out / "manifest.json").write_text(json.dumps({"sbr": str(sbr), "packages": man}))


def write_values(env, panel="EL2", B=20.0, turn=0.5, rep=0.5, deliver=True, name=None, per_pkg=None):
    import values
    pk = {}
    for p in PKGS:
        b, t, r = (per_pkg or {}).get(p, (B, turn, rep))
        pk[p] = {"B_A1": b, "turn_p90": t, "T_report_p90": r, "finish_offset_s": values.finish_offset(b, t, r),
                 "hang_s": values.hang_s(b), "k": values.k_of(b, t, r), "deliver": deliver, "cp_role": "adjudicator",
                 "n_runs": 0, "source_rows": []}
    d = Path(env["R4_OUT"]) / "values"
    d.mkdir(exist_ok=True)
    path = d / (name or f"test-{panel}.json")
    values.write_pinned(str(path), {"panel": panel, "kind": "test", "packages": pk})
    return path


def r4_copy(tmp_path) -> Path:
    """A copy of bin/, lib/ and frozen/ for tests that must change a frozen file."""
    c = tmp_path / "r4copy"
    for d in ("bin", "lib", "frozen"):
        shutil.copytree(R4 / d, c / d)
    return c


def first_card_anchor(pkg=DE, n=0, length=60):
    """A real sentence prefix from the candidate (flattened) usable as a card anchor."""
    text = " ".join((EVAL / pkg / "candidate.md").read_text().split())
    starts = [i for i in range(len(text)) if text.startswith("## Task", i)]
    i = starts[n % len(starts)] if starts else 0
    return text[i:i + length]


def make_board(tmp_path, cand_pkg=DE, flagger="t2b-1", peers=("t4-1", "t3-1")):
    b = tmp_path / "board"
    for d in ("msgs", "state", "snap", "metrics", "settings", "bin"):
        (b / d).mkdir(parents=True, exist_ok=True)
    cf = tmp_path / "candidate.flat"
    flat_file(EVAL / cand_pkg / "candidate.md", cf)
    return b, cf


def post(board, cf, *, anchor, move="M3", category="other", severity="MAJOR", cap=4, r=0, fin=None, rid="t2b-1",
         peers="t4-1,t3-1", calls=2, env=None, extra=None):
    if calls is not None:
        (board / "state" / f"{rid}.calls").write_text(f"{calls}\n")
    args = [R4 / "bin" / "panel-post", "--board", board, "--rid", rid, "--run", "row/pkg", "--cand-flat", cf, "--cap", cap,
            "--t0-ms", now_ms(), "--finish-ms", fin or now_ms() + 3_600_000, "--r", r, "--peers", peers]
    args += extra if extra is not None else ["--anchor", anchor, "--move", move, "--category", category, "--severity", severity]
    return run(args, env=env)


def hook(board, rid, *, role="adjudicator", flagger="t2b-1", k=2, deliver=1, c=0, fin=None, tp="", agent_id=None, env=None):
    args = [R4 / "bin" / "r4-hook", "--board", board, "--rid", rid, "--role", role, "--flagger", flagger, "--t0-ms", now_ms(),
            "--finish-ms", fin or now_ms() + 3_600_000, "--k", k, "--deliver", deliver, "--c", c]
    inp = {"session_id": "s", "transcript_path": str(tp), "cwd": "/tmp", "hook_event_name": "PostToolUse"}
    if agent_id:
        inp["agent_id"] = agent_id
    return run(args, input=json.dumps(inp), env=env)
