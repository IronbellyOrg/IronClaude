"""Shared fixtures: temp roots under /tmp, fake claude on PATH, sandbox and report builders (DESIGN 15)."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

R3 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R3))

from superclaude.cli.review import findings as F  # noqa: E402

from r3lib import paths  # noqa: E402

REPO = paths.REPO
EVAL = paths.EVAL
CONTROL = "TASK-WF-design-20261108-041415"
DESIGNSPEC = "TASK-WF-designSpec-20261107-075614"
ALIAS = "TASK-WF-makeTheAliasOnly-20261105-051649"
PKGS = [DESIGNSPEC, ALIAS, CONTROL]


def candidate(pkg=CONTROL) -> str:
    return (EVAL / pkg / "candidate.md").read_text(encoding="utf-8")


def cand_line(sub: str, pkg=CONTROL, n=150) -> str:
    for ln in candidate(pkg).splitlines():
        if sub in ln:
            s = F.flat(ln)
            return s[s.index(sub) :][:n].strip()
    raise KeyError(sub)


ANCH = {
    "only": "Edit only under",
    "mustnot": "must not contain the string",
    "never": "The skill never creates a label",
    "reread": "must be re-read in the live file",
    "cmd": "uv run pytest tests -k",
    "every": "every other feature gives Feature",
}


def finding(
    fid,
    key_or_anchor,
    category="missing-requirement",
    claim=None,
    severity="MAJOR",
    blocking=False,
    **kw,
):
    a = cand_line(ANCH[key_or_anchor]) if key_or_anchor in ANCH else key_or_anchor
    o = {
        "id": fid,
        "severity": severity,
        "blocking": blocking,
        "category": category,
        "anchor": a,
        "refs": [],
        "claim": claim
        or f"Claim {fid}: the text leaves the implementer unable to pass the stated check.",
    }
    o.update(kw)
    return o


def report(findings, verdict="PASS", raw_lines=None, heading=True, blocks=1) -> str:
    lines = [json.dumps(f) for f in findings] + list(raw_lines or [])
    body = "```findings-v1\n" + "\n".join(lines) + "\n```\n"
    head = "## Findings block\n" if heading else ""
    pre = (
        "```findings-v1\n" + json.dumps(findings[0]) + "\n```\n"
        if blocks == 2 and findings
        else ""
    )
    return f"review: 1 of 3\n\nCovered: the candidate and the source document.\n\n{head}{pre}{body}verdict: {verdict}\n"


@pytest.fixture
def env(tmp_path):
    """Environment for running harness scripts with every root under the pytest temp dir."""
    root = tmp_path
    assert str(root).startswith("/tmp/")
    e = dict(os.environ)
    e.update(
        {
            "R3_RUNS_ROOT": str(root / "runs"),
            "R3_SB_ROOT": str(root / "sb"),
            "R3_SCORING_ROOT": str(root / "scoring"),
            "R3_RESULTS_ROOT": str(root / "results"),
            "R3_CLAUDE_PROJECTS": str(root / "projects"),
            "R3_VALUES_FILE": str(root / "values" / "el2.json"),
            "PATH": f"{R3 / 'tests' / 'fakes'}:{os.environ['PATH']}",
            "FAKE_CLAUDE_PY": sys.executable,
            "FAKE_CLAUDE_PLAN": str(root / "plan.json"),
            "NOFALLBACK": "1",
            "FAKE_PGREP_TOTAL": "0",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    e.pop("R3_SMOKE", None)
    e.pop("R3_SPIKE4", None)
    e.pop("PANEL_COLLAB", None)
    e.pop("TIME_CAP_EXCEPTION", None)
    (root / "values").mkdir()
    return {"root": root, "env": e}


def write_values(env, B=40.0, turn=1.5, pkgs=(CONTROL,), panel="el2"):
    v = {
        "schema": "r3-values/1",
        "panel": panel,
        "status": "frozen",
        "source_runs": ["test"],
        "frozen_at": "x",
        "turn_p90": {
            m: turn
            for m in (
                "muse-ember-1.0",
                "gpt-6-luna",
                "claude-haiku-5-5",
                "claude-sonnet-5-5",
            )
        },
        "packages": {
            p: {
                "B_f": B,
                "T_report_p90": turn,
                "k": 0,
                "panel_finish_offset_s": 1.35 * B - 2 * turn,
            }
            for p in pkgs
        },
        "slowdown_s": None,
    }
    f = Path(env["env"]["R3_VALUES_FILE"])
    f.write_text(json.dumps(v))
    import hashlib

    Path(str(f) + ".sha256").write_text(
        hashlib.sha256(f.read_bytes()).hexdigest() + "\n"
    )


def mini_sandbox(env, pkg=CONTROL):
    """A small valid sandbox: the masked files at the base commit, one snap commit, candidate and source copied."""
    sb = Path(env["env"]["R3_SB_ROOT"])
    pk = paths.cfg("packages.json")["packages"][pkg]
    repo = sb / pkg / "repo"
    repo.mkdir(parents=True)
    for mp in pk["masked_paths"]:
        r = subprocess.run(
            ["git", "-C", str(REPO), "show", f"{pk['base']}:{mp}"], capture_output=True
        )
        if r.returncode == 0:
            (repo / mp).parent.mkdir(parents=True, exist_ok=True)
            (repo / mp).write_bytes(r.stdout)
    (repo / ".gitignore").write_text(".venv/\n__pycache__/\n")
    (repo / "README.md").write_text("sandbox\n")
    subprocess.run(
        "git init -q && git add -A && git -c user.name=r3 -c user.email=r3@x commit -q -m snap",
        shell=True,
        cwd=repo,
        check=True,
    )
    (sb / pkg / "active").mkdir(exist_ok=True)
    c = sb / "cand" / pkg
    c.mkdir(parents=True, exist_ok=True)
    shutil.copy(EVAL / pkg / "candidate.md", c / "candidate.md")
    shutil.copy(REPO / ".dev/tasks/done" / pkg / "source.md", c / "source.md")
    return repo


def write_plan(env, rules):
    Path(env["env"]["FAKE_CLAUDE_PLAN"]).write_text(json.dumps(rules))


def fixture_file(env, name, text):
    d = env["root"] / "fx"
    d.mkdir(exist_ok=True)
    p = d / name
    p.write_text(text)
    return str(p)


SCORE = {
    "label": "A",
    "combo": "x",
    "package": CONTROL,
    "gt_total": 2,
    "gt_covered_any": ["GT1"],
    "gt_covered_blocking": [],
    "ledger_rows_total": 3,
    "ledger_rows_blocking": 0,
    "blocking_rows_gt_matched": 0,
    "wrong_blockers": 0,
    "notes": "fake",
}


def default_rules(env, p1=None, p2=None, judge=True):
    """Phase-1 reports per model, a phase-2 reply and a judge score."""
    p1 = p1 or {
        "muse-ember-1.0": [
            finding("F1", "only", "unpassable-check"),
            finding("F2", "every", "missing-requirement"),
            finding("F3", "cmd", "unpassable-check"),
        ],
        "gpt-6-luna": [
            finding("F1", "never", "missing-requirement"),
            finding("F2", "reread", "contradiction"),
        ],
    }
    rules = []
    for model, fs in p1.items():
        rules.append(
            {
                "match": {
                    "model": model,
                    "resume": False,
                    "prompt_contains": "review 1 of 3",
                },
                "action": {"report": fixture_file(env, f"p1-{model}.md", report(fs))},
            }
        )
    p2text = (
        p2
        if p2 is not None
        else (
            "Checked.\n"
            + json.dumps(
                finding(
                    "C1",
                    "mustnot",
                    "missing-requirement",
                    claim="New: the rule has no finite check.",
                )
            )
            + "\nno finding C2\n\n## Findings block\n```findings-v1\n"
            + json.dumps(
                finding(
                    "C1",
                    "mustnot",
                    "missing-requirement",
                    claim="New: the rule has no finite check.",
                )
            )
            + "\n```\nverdict: PASS\n"
        )
    )
    rules.append(
        {
            "match": {"resume": True, "prompt_contains": "Second pass"},
            "action": {"text": p2text},
        }
    )
    rules.append(
        {
            "match": {"resume": False, "prompt_contains": "Second pass"},
            "action": {"text": p2text},
        }
    )
    if judge:
        rules.append(
            {
                "match": {"prompt_contains": "blind scoring judge"},
                "action": {"judge_score": SCORE, "text": "score.json written"},
            }
        )
    return rules


def launch(
    env, panel="el2", collab=1, pkgs=(CONTROL,), extra=(), timeout=300, envx=None
):
    e = dict(env["env"])
    e["PANEL_COLLAB"] = str(collab)
    e.update(envx or {})
    cmd = ["bash", str(R3 / "bin/launch-panel.sh"), panel, "--pkgs", *pkgs, *extra]
    r = subprocess.run(cmd, env=e, capture_output=True, text=True, timeout=timeout)
    runs = (
        sorted(Path(e["R3_RUNS_ROOT"]).glob("*"))
        if Path(e["R3_RUNS_ROOT"]).exists()
        else []
    )
    return r, (runs[-1] if runs else None)


def plan_state(env):
    p = Path(env["env"]["FAKE_CLAUDE_PLAN"]).with_suffix(".state.json")
    return json.loads(p.read_text()) if p.exists() else {}


def jload(p):
    return json.loads(Path(p).read_text())


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "slow: fault-injection tests that launch the harness on the fake claude",
    )
