"""Fixtures for the R2 harness tests. Every fixture is synthetic: a small fake repo, candidate, source, ground truth
and a stub judge. The fake `claude` (tests/fakes/claude) is put first on PATH. No test calls a real model."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

import pytest

R2 = Path(__file__).resolve().parents[1]
BIN = R2 / "bin"
PY = R2 / "py"
FAKES = R2 / "tests" / "fakes"
REAL_EVAL = R2.parents[1] / "20261111-a1"
PKGS = json.loads((R2 / "config/panels.json").read_text())["packages"]
CONTROL = "TASK-WF-design-20261108-041415"
CAND_A = "so that every greeting uses the new wording"


def pytest_configure(config):
    config.addinivalue_line("markers", "live: needs real gateway models (skipped unless R2_LIVE=1)")


@pytest.fixture(autouse=True)
def _no_ambient_slack(monkeypatch):
    """PANEL_SLACK_S defaults to 0 in every test unless the test sets it."""
    monkeypatch.delenv("PANEL_SLACK_S", raising=False)


def pytest_collection_modifyitems(config, items):
    if os.environ.get("R2_LIVE") == "1":
        return
    skip = pytest.mark.skip(reason="live test: set R2_LIVE=1")
    for it in items:
        if "live" in it.keywords:
            it.add_marker(skip)


CANDIDATE = """# Plan: change the greeting

## Task 1: Update the greeting
Edit `src/app.py` so that every greeting uses the new wording.
Acceptance: `uv run pytest tests/test_app.py` passes.

## Task 2: Document the change
Update `docs/guide.md` with the new wording; all examples in the guide use it.
Acceptance: the guide shows the new wording in every example.

## Task 3: Release note
Add one line to the release notes describing the new wording.
"""

SOURCE = """# Source: greeting change
1. The greeting must use the new wording everywhere.
2. The guide must show the new wording.
3. Tests must cover the greeting.
4. The changelog records the change.
"""


def report(findings: list[dict] | None = None, extra: str = "") -> str:
    if findings is None:
        findings = [{"id": "F1", "severity": "MAJOR", "blocking": True, "category": "contradiction",
                     "anchor": CAND_A, "refs": [], "claim": "The greeting change leaves another caller unchanged."}]
    body = "\n".join(json.dumps(f) for f in findings)
    return f"review: 1 of 3\n\nCovered tasks 1-3.{extra}\n\n## Findings block\n\n```findings-v1\n{body}\n```\n\nverdict: FAIL\n"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(cmd, env=None, cwd=None, input=None, timeout=120, check=False):
    r = subprocess.run(cmd, env=env, cwd=cwd, input=input, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode != 0:
        raise AssertionError(f"{cmd} rc={r.returncode}\nSTDOUT {r.stdout}\nSTDERR {r.stderr}")
    return r


class World:
    """A fake REPO / EVAL / SBR / OUT tree plus the environment the scripts need."""

    def __init__(self, tmp: Path):
        self.tmp = tmp
        self.repo, self.eval, self.sbr, self.out = tmp / "repo", tmp / "eval", tmp / "sbr", tmp / "out"
        self.state = tmp / "fake-state"
        self.scenario = tmp / "scenario.json"
        self.log = tmp / "claude-argv.jsonl"
        self._build()

    def _build(self):
        r = self.repo
        for rel, text in {
            "src/app.py": "def greet():\n    return 'hello'\n",
            "src/other.py": "from app import greet\n",
            "tests/test_app.py": "def test_greet():\n    assert True\n",
            "tests/test_other.py": "# checks the greeting wording\ndef test_other():\n    assert 'hello'\n",
            "docs/guide.md": "Say hello.\n",
            "CHANGELOG.md": "# Changelog\n- greeting wording\n- other\n",
            "README.md": "readme greeting\n",
            ".dev/reflect/leak.md": "leak\n", ".dev/research/r.md": "r\n", ".dev/eval-workspaces/e.md": "e\n",
        }.items():
            (r / rel).parent.mkdir(parents=True, exist_ok=True)
            (r / rel).write_text(text)
        for p in PKGS:
            (r / f".dev/tasks/done/{p}").mkdir(parents=True, exist_ok=True)
            (r / f".dev/tasks/done/{p}/source.md").write_text(SOURCE)
        run(["git", "init", "-q"], cwd=r, check=True)
        run(["git", "add", "-A"], cwd=r, check=True)
        run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "base"], cwd=r, check=True)
        self.base = run(["git", "rev-parse", "HEAD"], cwd=r, check=True).stdout.strip()
        for p in PKGS:
            d = self.eval / p
            d.mkdir(parents=True)
            (d / "candidate.md").write_text(CANDIDATE)
            gt = {"package": p, "items": [
                {"id": "GT1", "class": "x", "blocking_in_implement": True, "description": "tests/test_other.py is not updated",
                 "plan_quote": "all examples in the guide use it"},
                {"id": "GT2", "class": "x", "blocking_in_implement": False, "description": "release note", "plan_quote": "Add one line to the release notes"}]}
            (d / "ground-truth.json").write_text(json.dumps(gt))
            shutil.copy(REAL_EVAL / p / "resolution-live7.json", d / "resolution-live7.json")
        (self.eval / "arms/scoring/combos").mkdir(parents=True)
        jd = self.eval / "tools/tmp-scripts"
        jd.mkdir(parents=True)
        self.judge = jd / "judge-one.sh"
        self.judge.write_text(f"""#!/bin/bash
set -u
EVAL={self.eval}
C="$1"; P="$2"; L="$3"
D="$EVAL/arms/scoring/combos/$C/$P/$L"
[ -f "$D/score.json" ] && {{ echo "SKIP"; exit 0; }}
echo "$D" >> {self.tmp}/judge-calls.txt
printf '[{{"type":"result","result":"%s"}}]' "${{JUDGE_RESULT:-score.json written}}" > "$D/judge.json"
cat > "$D/score.json" <<EOF
{{"label":"$L","combo":"$C","package":"$P","gt_total":2,"gt_covered_any":["GT1"],"gt_covered_blocking":["GT1","GT2"],"ledger_rows_total":1,"ledger_rows_blocking":1,"blocking_rows_gt_matched":1,"wrong_blockers":1,"notes":"stub"}}
EOF
echo "OK $C/$P/$L"
""")
        self.manifest = self.tmp / "manifest.json"
        self.write_manifest()
        self.scenario.write_text(json.dumps({"entries": {"default": {"report": report()}}}))

    def write_manifest(self, judge_sha=None):
        m = {"base_sha": {p: self.base for p in PKGS},
             "sha256": {"judge-one.sh": judge_sha or sha(self.judge),
                        "catalogue.json": sha(R2 / "config/catalogue.json"),
                        "brief_a1": sha(R2 / "config/brief-a1.tmpl"),
                        "sweeper_brief": sha(R2 / "config/sweeper-brief.tmpl")}}
        self.manifest.write_text(json.dumps(m))

    @property
    def env(self) -> dict:
        e = dict(os.environ)
        e.update({"R2_REPO": str(self.repo), "R2_EVAL": str(self.eval), "R2_SBR": str(self.sbr), "R2_OUT": str(self.out),
                  "R2_MANIFEST": str(self.manifest), "PATH": f"{FAKES}:{os.environ['PATH']}",
                  "FAKE_CLAUDE_SCENARIO": str(self.scenario), "FAKE_CLAUDE_LOG": str(self.log),
                  "FAKE_CLAUDE_STATE": str(self.state), "FAKE_CLAUDE_PROJECTS": str(self.tmp / "projects"),
                  "NOFALLBACK": "1"})
        e.pop("PANEL_COLLAB", None)
        e.pop("PANEL_SLACK_S", None)
        return e

    def scenario_set(self, entries: dict):
        self.scenario.write_text(json.dumps({"entries": entries}))

    def argv_log(self) -> list[dict]:
        return [json.loads(x) for x in self.log.read_text().splitlines()] if self.log.exists() else []

    # ---- a board + sandbox for hook / validator tests (no launcher)
    def board(self, k=2, finish_in_s=600, cap=None, deal_r=0, named=("src/app.py", "tests/test_app.py", "docs/guide.md")):
        sb = self.sbr / "sb/run1/pkg"
        (sb / "cand").mkdir(parents=True, exist_ok=True)
        if not (sb / "repo").exists():
            shutil.copytree(self.repo, sb / "repo", ignore=shutil.ignore_patterns(".git"))
        (sb / "cand/candidate.md").write_text(CANDIDATE)
        (sb / "cand/source.md").write_text(SOURCE)
        B = self.sbr / "board/run1/pkg"
        for d in ("msgs", "snap", "state", "metrics", "bin"):
            (B / d).mkdir(parents=True, exist_ok=True)
        for f in ("msgs/board.jsonl", "msgs/rejected.jsonl", "state/opened.txt"):
            (B / f).touch()
        (B / "state/seq").write_text("0\n")
        (B / "named.txt").write_text("".join(f"{n}\n" for n in named))
        (B / "cand.flat").write_text(" ".join(CANDIDATE.split()) + "\n")
        now = int(time.time() * 1000)
        conf = {"run": "run1/pkg", "repo": str(sb / "repo"), "cand_dir": str(sb / "cand"),
                "source": str(sb / "cand/source.md"), "finish_ms": now + finish_in_s * 1000,
                "cap": cap if cap is not None else 2 * k, "t0_ms": now}
        (B / "conf.json").write_text(json.dumps(conf))
        tmpl = (BIN / "panel-post.tmpl").read_text()
        post = (tmpl.replace("@BASH@", shutil.which("bash")).replace("@BOARD@", str(B))
                .replace("@LIB@", str(BIN / "lib")).replace("@JQ@", shutil.which("jq")))
        (B / "bin/panel-post").write_text(post)
        (B / "bin/panel-post").chmod(0o755)
        self.B, self.SB, self.conf = B, sb, conf
        return B

    def post(self, *args) -> subprocess.CompletedProcess:
        return run([str(self.B / "bin/panel-post"), *args])

    def hook_settings(self, rid="t4-1", ri=0, k=2, deal_r=0, finish_ms=None, jq=None):
        out = self.tmp / f"settings-{rid}.json"
        run(["bash", str(BIN / "make-settings.sh"), "receiver", "--board", str(self.B), "--rid", rid, "--recv-index", str(ri),
             "--t0-ms", str(self.conf["t0_ms"]), "--finish-ms", str(finish_ms or self.conf["finish_ms"]), "--k", str(k),
             "--deal-r", str(deal_r), "--out", str(out)], env=self.env, check=True)
        s = json.loads(out.read_text())
        if jq:
            cmd = s["hooks"]["PostToolUse"][0]["hooks"][0]["command"]
            s["hooks"]["PostToolUse"][0]["hooks"][0]["command"] = cmd.replace(shutil.which("jq"), jq)
            out.write_text(json.dumps(s))
        return out

    def hook_cmd(self, settings: Path) -> str:
        return json.loads(settings.read_text())["hooks"]["PostToolUse"][0]["hooks"][0]["command"]

    def call_hook(self, settings: Path, tool="Bash", tool_input=None, response=None, transcript=None, envi=False):
        tp = transcript or (self.tmp / "transcript.jsonl")
        if not tp.exists():
            tp.write_text('{"type":"user"}\n')
        payload = {"session_id": "s", "transcript_path": str(tp), "cwd": str(self.SB / "repo"), "hook_event_name": "PostToolUse",
                   "tool_name": tool, "tool_input": tool_input or {"command": "ls"}, "tool_response": response or {"stdout": ""}}
        cmd = ["bash", "-c", self.hook_cmd(settings)]
        if envi:
            cmd = ["env", "-i", "/usr/bin/bash", "-c", self.hook_cmd(settings)]
        r = run(cmd, input=json.dumps(payload), timeout=20)
        assert r.returncode == 0, r.stderr
        return r.stdout.strip()

    def metrics(self, rid) -> list[dict]:
        p = self.B / f"metrics/{rid}.jsonl"
        return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []

    def board_lines(self) -> list[dict]:
        return [json.loads(x) for x in (self.B / "msgs/board.jsonl").read_text().splitlines()]

    def seed(self, *facts):
        """Append facts straight to the board (bypassing the validator) with ids f-<n>."""
        lines = (self.B / "msgs/board.jsonl").read_text().splitlines()
        for f in facts:
            base = {"v": "panel-msg/1", "id": f"f-{len(lines)}", "run": "run1/pkg", "from": "sw-1", "to": "*",
                    "t": int(time.time() * 1000), "kind": "fact", "move": "M1", "cmd": "grep -rln greeting tests/"}
            base.update(f)
            lines.append(json.dumps(base))
        (self.B / "msgs/board.jsonl").write_text("".join(x + "\n" for x in lines))
        (self.B / "state/seq").write_text(str(len(lines)))

    def launch(self, *args, collab=1, timeout=300, extra_env=None):
        e = self.env
        e["PANEL_COLLAB"] = str(collab)
        if extra_env:
            e.update(extra_env)
        return run(["bash", str(BIN / "launch-panel.sh"), *args], env=e, timeout=timeout)


@pytest.fixture
def world(tmp_path):
    return World(tmp_path)


def pyrun(script, *args, env=None):
    return run(["uv", "run", "--no-project", "python", "-I", str(PY / script), *args], env=env)
