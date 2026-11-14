"""Shared fixtures for the r1-move-radar tests. Every test writes only under tmp_path."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

R1 = Path(__file__).resolve().parents[1]
REPO = R1.parents[4]
A1DIR = REPO / ".dev/eval-workspaces/tasklist-review-panel/20261111-a1"
FIX = R1 / "tests" / "fixtures"
TOOLS = R1 / "tools"
PKG = "TASK-WF-fixture-20261113-000000"


def run(args, *, stdin=None, env=None, cwd=None, timeout=60):
    return subprocess.run(args, input=stdin, capture_output=True, text=True, env=env, cwd=cwd or REPO, timeout=timeout)


@pytest.fixture
def fake_sb(tmp_path):
    """A sandbox root with one fixture package: SB/<PKG>/repo (root files, src, tests, docs) and SB/cand/<PKG>/."""
    sb = tmp_path / "sb"
    repo = sb / PKG / "repo"
    for rel in ("src/app/core.py", "src/app/scripts/old.sh", "scripts/run.sh", "tests/app/test_core.py",
                "tests/app/test_other.py", "docs/guide.md", "CHANGELOG.md", "Makefile"):
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x\n")
    (repo / "src/app/sub").mkdir()
    cand = sb / "cand" / PKG
    cand.mkdir(parents=True)
    shutil.copy(FIX / "cand" / "candidate.md", cand / "candidate.md")
    (cand / "source.md").write_text("# source\n")
    return sb


@pytest.fixture
def root(tmp_path):
    """A writable R1 output root (index/, runs/, values/ ...) with the real config copied in."""
    r = tmp_path / "r1"
    (r / "config").mkdir(parents=True)
    for f in (R1 / "config").iterdir():
        shutil.copy(f, r / "config" / f.name)
    shutil.copy(R1 / "manifest.json", r / "manifest.json")
    return r


def jload(p):
    return json.loads(Path(p).read_text())


@pytest.fixture
def clean_env():
    return {k: v for k, v in os.environ.items()}


# ---------------------------------------------------------------- hook kit
SEARCHER, READERS = "t2b-1", ["t4-1", "t3-1"]
CAT = jload(R1 / "config" / "catalogue.json")
ORDERS = {"t2b-1": "M2,M7,M4,M1", "t4-1": "M3,M5,M6,M9,M8,M10", "t3-1": "M8,M10,M3,M5,M6,M9",
          "t1b-1": "M7,M4,M1,M2", "t2-1": "M1,M2,M7,M4"}


class Board:
    """A board under tmp_path with ctx/ files, a clock file and a transcript, driven call by call."""

    def __init__(self, tmp_path, sb="/tmp/sbX"):
        self.dir = tmp_path / "board"
        (self.dir / "ctx").mkdir(parents=True)
        shutil.copy(R1 / "config" / "catalogue.json", self.dir / "ctx" / "catalogue.json")
        shutil.copy(FIX / "index.json", self.dir / "ctx" / "index.json")
        self.repo = f"{sb}/{PKG}/repo"
        self.src = f"{sb}/cand/{PKG}/source.md"
        (self.dir / "ctx" / "panel.json").write_text(json.dumps({"searcher": SEARCHER, "readers": READERS, "srcpath": self.src}))
        self.clock = tmp_path / "clock"
        self.set_clock(1000)
        self.transcript = tmp_path / "transcript.jsonl"
        self.transcript.write_text('{"type":"user"}\n{"type":"assistant"}\n')

    def set_clock(self, ms):
        self.clock.write_text(str(ms))

    def stdin(self, tool="Bash", inp=None, agent_id=None, transcript=None):
        d = {"session_id": "s1", "transcript_path": str(transcript or self.transcript), "hook_event_name": "PostToolUse",
             "tool_name": tool, "tool_input": inp if inp is not None else {"command": "ls"}, "tool_response": {}}
        if agent_id:
            d["agent_id"] = agent_id
        return json.dumps(d)

    def args(self, rid, role, k=2, cps=None, finish=10**9, guard=10**9, order=None):
        cps = cps or ((6, 10) if role == "searcher" else (8, 12))
        return [str(self.dir), "row-c1-r0/" + PKG, rid, role, "0", str(finish), str(guard), str(k), str(cps[0]),
                str(cps[1]), order or ORDERS[rid], PKG, str(self.clock)]

    def call(self, rid, role, env=None, raw_stdin=None, **kw):
        a = self.args(rid, role, **{k: v for k, v in kw.items() if k in ("k", "cps", "finish", "guard", "order")})
        s = raw_stdin if raw_stdin is not None else self.stdin(**{k: v for k, v in kw.items() if k in ("tool", "inp", "agent_id", "transcript")})
        r = run(["bash", str(TOOLS / "radar-hook.sh"), *a], stdin=s, env=env)
        assert r.returncode == 0, r.stderr
        return r.stdout.strip()

    def metrics(self, rid):
        p = self.dir / "metrics" / f"{rid}.jsonl"
        return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []

    def metrics_safe(self, rid):
        """Metrics lines that are JSON objects (a test may plant junk lines)."""
        p = self.dir / "metrics" / f"{rid}.jsonl"
        out = []
        for x in p.read_text().splitlines() if p.exists() else []:
            try:
                v = json.loads(x)
            except ValueError:
                continue
            if isinstance(v, dict):
                out.append(v)
        return out

    def events(self, rid, ev):
        return [m for m in self.metrics(rid) if m.get("ev") == ev]

    def tele(self, rid, line):
        p = self.dir / "tele" / f"{rid}.jsonl"
        p.parent.mkdir(exist_ok=True)
        with p.open("a") as f:
            f.write(line + "\n")


def expected_text(move, role):
    if move is None:
        return CAT["src_text"]
    return CAT["moves"][move] + (CAT["observable_suffix"] if role == "searcher" and move in CAT["observable"] else "")


def ctx_text(out):
    d = json.loads(out)
    assert list(d) == ["hookSpecificOutput"] and d["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
    assert set(d["hookSpecificOutput"]) == {"hookEventName", "additionalContext"}
    return d["hookSpecificOutput"]["additionalContext"]


@pytest.fixture
def board(tmp_path):
    return Board(tmp_path)


# ---------------------------------------------------------------- runner kit (stub claude, never the gateway)
STUB_BIN = FIX / "bin"
ANCHOR = "Create `src/app/merge_guard.py` and `src/app/scripts/tool.sh`"


def finding(**kw):
    f = {"id": "F1", "severity": "MAJOR", "blocking": True, "category": "contradiction", "anchor": ANCHOR,
         "refs": [], "claim": "The module and the script disagree."}
    f.update(kw)
    return f


def report(*findings_, raw_lines=()):
    body = "\n".join([json.dumps(f) for f in findings_] + list(raw_lines))
    return f"review: 1 of 3\n\nCovered everything.\n\n## Findings block\n\n```findings-v1\n{body}\n```\n\nverdict: FAIL\n"


def json_reply(text, session="sess-1", tokens=100, model="@@MODEL@@"):
    return json.dumps([
        {"type": "system", "subtype": "init"},
        {"type": "assistant", "timestamp": "2026-11-13T10:00:01.000Z", "parent_tool_use_id": None,
         "message": {"id": "m1", "model": model, "content": [{"type": "text", "text": "ok"}]}},
        {"type": "result", "subtype": "success", "result": text, "session_id": session,
         "usage": {"output_tokens": tokens}, "modelUsage": {model: {"outputTokens": tokens}}}])


def stream_reply(text, session="sess-1", tokens=50):
    return "\n".join(json.dumps(x) for x in [
        {"type": "system", "subtype": "init", "session_id": session},
        {"type": "assistant", "message": {"id": "m2", "model": "@@MODEL@@", "content": [{"type": "text", "text": text}]}},
        {"type": "result", "subtype": "success", "result": text, "session_id": session,
         "modelUsage": {"@@MODEL@@": {"outputTokens": tokens}}}]) + "\n"


class Runner:
    """runs/<row>/<pkg>/ with run.json under a tmp R1 root, a tmp sandbox and a stub plan."""

    def __init__(self, tmp_path, root, hang_s=600, row="el2-c1-r0"):
        self.root, self.row = root, row
        self.sb = tmp_path / "sb"
        (self.sb / PKG / "repo").mkdir(parents=True)
        (self.sb / "cand" / PKG).mkdir(parents=True)
        shutil.copy(FIX / "cand" / "candidate.md", self.sb / "cand" / PKG / "candidate.md")
        (self.sb / "cand" / PKG / "source.md").write_text("# source\n")
        self.d = root / "runs" / row / PKG
        (self.d / "settings").mkdir(parents=True)
        import time
        t0 = int(time.time() * 1000)
        self.t0 = t0
        self.write_run(hang_ms=t0 + int(hang_s * 1000))
        self.stub = tmp_path / "stub"
        self.stub.mkdir()
        self.n = 0
        self.env = dict(os.environ, PATH=f"{STUB_BIN}:{os.environ['PATH']}", NOFALLBACK="1", STUB_DIR=str(self.stub))

    def write_run(self, hang_ms):
        (self.d / "run.json").write_text(json.dumps({"T0_MS": self.t0, "HANG_MS": hang_ms, "FINISH_MS": hang_ms, "GUARD_MS": hang_ms,
                                                     "role": {"t2b-1": "searcher", "t4-1": "reader", "t3-1": "reader"},
                                                     "T_report": {"searcher": 1, "reader": 1}}))

    def file(self, content):
        self.n += 1
        p = self.stub / f"reply{self.n}"
        p.write_text(content)
        return p

    def plan(self, *lines):
        (self.stub / "plan").write_text("\n".join(lines) + "\n")

    def settings(self, rid, board="/nonexistent/board"):
        r = run(["bash", str(TOOLS / "settings-gen.sh"), board, f"{self.row}/{PKG}", rid, "searcher", "0", "99999999999999", "99999999999999", "2", "6",
                 "10", "M2,M7,M4,M1", PKG, ""])
        (self.d / "settings" / f"{rid}.json").write_text(r.stdout)
        return r.stdout.strip()

    def run(self, rid="t2b-1", model="muse-ember-1.0", collab=1, print_cmd=False, timeout=120):
        a = ["bash", str(TOOLS / "run-reviewer.sh")] + (["--print-cmd"] if print_cmd else []) + \
            [self.row, PKG, rid, model, str(collab), str(self.t0), "--root", str(self.root), "--sb", str(self.sb)]
        return run(a, env=self.env, timeout=timeout)

    def meta(self, rid="t2b-1"):
        return jload(self.d / "reviews" / f"{rid}.meta.json")

    def argv(self, k):
        return (self.stub / f"argv.{k}").read_text().splitlines()

    def calls(self):
        return int((self.stub / "count").read_text()) if (self.stub / "count").exists() else 0


@pytest.fixture
def runner(tmp_path, root):
    return Runner(tmp_path, root)


# ---------------------------------------------------------------- package kit (collab_summary, results, launch tests)
class Pkg:
    """runs/<row>/<pkg>/ with run.json, reviews and (collab 1) a live board, a clean git sandbox and a tmp A1DIR."""

    def __init__(self, tmp_path, root, row="el2-c1-r0", collab=1, pkg=PKG):
        self.root, self.row, self.pkg, self.collab = root, row, pkg, collab
        self.sb = tmp_path / "sb"
        repo = self.sb / pkg / "repo"
        if not repo.exists():
            (repo / "src").mkdir(parents=True)
            (repo / "src" / "a.py").write_text("x\n")
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
            subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "s"], cwd=repo, check=True)
        cand = self.sb / "cand" / pkg
        cand.mkdir(parents=True, exist_ok=True)
        shutil.copy(FIX / "cand" / "candidate.md", cand / "candidate.md")
        (cand / "source.md").write_text("# source\n")
        (root / "index").mkdir(exist_ok=True)
        shutil.copy(FIX / "index.json", root / "index" / f"{pkg}.json")
        self.a1 = tmp_path / "a1"
        (self.a1 / pkg).mkdir(parents=True, exist_ok=True)
        shutil.copy(FIX / "ground-truth.json", self.a1 / pkg / "ground-truth.json")
        self.d = root / "runs" / row / pkg
        (self.d / "reviews").mkdir(parents=True, exist_ok=True)
        import hashlib
        self.run = {"row": row, "pkg": pkg, "panel": "el2", "collab": collab, "T0_MS": 0, "FINISH_MS": 10**12, "GUARD_MS": 10**12,
                    "HANG_MS": 174000, "B": 116, "values": "planning", "k": {"searcher": 2, "reader": 2},
                    "T_report": {"searcher": 3.2, "reader": 6.4}, "role": {"t2b-1": "searcher", "t4-1": "reader", "t3-1": "reader"},
                    "model": {"t2b-1": "muse-ember-1.0", "t4-1": "gpt-6-luna", "t3-1": "gpt-6-luna"},
                    "cand_sha256": hashlib.sha256((cand / "candidate.md").read_bytes()).hexdigest()}
        self.write_run()
        self.board = Board(self.d, sb=str(self.sb)) if collab else None
        for rid in self.run["role"]:
            self.review(rid, report())

    def write_run(self):
        (self.d / "run.json").write_text(json.dumps(self.run))

    def review(self, rid, text, end_ms=100_000, **meta):
        (self.d / "reviews" / f"{rid}.md").write_text(text)
        m = {"reviewer_id": rid, "valid": True, "model_ok": True, "start_ms": 0, "end_ms": end_ms, "attempts": 1,
             "session_ids": [f"sess-{rid}"], "reask_s": None, "retry_s": None, "retry_isolated": False, "dropped_lines": 0,
             "hang_kill": False}
        m.update(meta)
        (self.d / "reviews" / f"{rid}.meta.json").write_text(json.dumps(m))

    def summary(self, cmd="pre"):
        return run(["uv", "run", "python", str(TOOLS / "collab_summary.py"), cmd, self.row, self.pkg, "--root", str(self.root),
                    "--sb", str(self.sb), "--a1", str(self.a1)], cwd=REPO)

    def collab_json(self):
        return jload(self.d / "collab.json")

    def audit(self):
        return jload(self.d / "audit.json")


@pytest.fixture
def pkg1(tmp_path, root):
    return Pkg(tmp_path, root)
CAND_LONG = (FIX / "cand" / "candidate.md").read_text().split("\n\n")[-1].strip()
