"""Shared fixtures for the R5 tests. Synthetic ground truth only; the fake `claude` never calls a model."""
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

R5 = Path(__file__).resolve().parents[1]
FIX = R5 / "tests" / "fixtures"
REAL_EVAL = R5.parents[1] / "20261111-a1"
DS, AL, CT = ("TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415")
PKGS = (DS, AL, CT)
BASES = json.loads((R5 / "config" / "bases.json").read_text())
SYNTH_GT = {
    DS: [("GT%d" % i, i in (1, 2, 3, 6)) for i in range(1, 11)],
    AL: [("GT1", True), ("GT2", False), ("GT3", True), ("GT4", False)],
    CT: [("GT1", False), ("GT2", False)],
}


def cand_text(pkg):
    return (FIX / "candidates" / f"{pkg}.md").read_text()


def heading_anchor(pkg, tid):
    """An exact candidate substring that lies inside Task <n> (its heading text)."""
    for line in cand_text(pkg).splitlines():
        if line.startswith(f"## Task {tid[1:]}:"):
            return line[3:63]
    raise KeyError(tid)


def finding(fid, anchor, claim="The stated check cannot pass for the mapping rule.", sev="MAJOR", blocking=False, cat="contradiction", **kw):
    return {"id": fid, "severity": sev, "blocking": blocking, "category": cat, "anchor": anchor, "refs": [], "claim": claim, **kw}


def report(findings, prose="review: 1 of 3\n\n## Coverage\nI read every Task.\n", raw_lines=()):
    body = "\n".join([json.dumps(f) for f in findings] + list(raw_lines))
    return f"{prose}\n## Findings block\n\n```findings-v1\n{body}\n```\nverdict: FAIL\n"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write_eval(root: Path) -> Path:
    ev = root / "eval"
    for p in PKGS:
        (ev / p).mkdir(parents=True)
        shutil.copy(FIX / "candidates" / f"{p}.md", ev / p / "candidate.md")
        shutil.copy(FIX / "resolution" / f"{p}.json", ev / p / "resolution-live7.json")
        items = [{"id": g, "class": "x", "blocking_in_implement": b, "cost": "", "evidence": "",
                  "description": f"synthetic defect {g} in fixtures/zz_{g.lower()}.py", "plan_quote": f"QQ synthetic quote {g} QQ zz"} for g, b in SYNTH_GT[p]]
        (ev / p / "ground-truth.json").write_text(json.dumps({"items": items}))
    tools = ev / "tools" / "tmp-scripts"
    tools.mkdir(parents=True)
    judge = (REAL_EVAL / "tools" / "tmp-scripts" / "judge-one.sh").read_text()
    judge = "\n".join(f"EVAL={ev}" if line.startswith("EVAL=") else line for line in judge.split("\n"))
    (tools / "judge-one.sh").write_text(judge)
    shutil.copy(REAL_EVAL / "tools" / "run-reviewer.sh", ev / "tools" / "run-reviewer.sh")
    (ev / "arms" / "scoring" / "combos").mkdir(parents=True)
    return ev


def write_sb(root: Path) -> Path:
    sb = root / "sb"
    man = {}
    for p in PKGS:
        repo = sb / p / "repo"
        repo.mkdir(parents=True)
        (repo / "README.md").write_text("sandbox\n")
        g = ["git", "-C", str(repo)]
        subprocess.run(g + ["init", "-q"], check=True)
        subprocess.run(g + ["add", "-A"], check=True)
        subprocess.run(g + ["-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", "commit", "-qm", "s"], check=True)
        c = sb / "cand" / p
        c.mkdir(parents=True)
        shutil.copy(FIX / "candidates" / f"{p}.md", c / "candidate.md")
        (c / "source.md").write_text("source document\n")
        src = root / "repo" / ".dev" / "tasks" / "done" / p / "source.md"  # R5_REPO stand-in for sandbox-build.sh
        src.parent.mkdir(parents=True)
        src.write_text("source document\n")
        tree = subprocess.run(g + ["rev-parse", "HEAD^{tree}"], capture_output=True, text=True).stdout.strip()
        man[p] = {"base": BASES[p]["base"], "tree": tree, "candidate_sha256": sha(c / "candidate.md"), "source_sha256": sha(c / "source.md")}
    (sb / "manifest.json").write_text(json.dumps(man))
    return sb


def write_values(cfg: Path, panel: str, pkgs=PKGS, **over):
    vd = cfg / "values" / panel
    vd.mkdir(parents=True, exist_ok=True)
    sums = []
    for p in pkgs:
        v = {"panel": panel, "pkg": p, "B_f_s": 10, "turn_p90_s": 0.5, "T_report_p90_s": 0.5, "hooks_s": 2, "k": 2,
             "finish_offset_s": 12, "hang_offset_s": 15, "slowdown_s": 0.01, "slowdown_limit": 0.1, "budget_ok": True,
             "runs": [], "measured_at": "test"}
        v.update(over.get(p, over.get("all", {})))
        text = json.dumps(v, indent=1) + "\n"
        (vd / f"{p}.json").write_text(text)
        sums.append(f"{hashlib.sha256(text.encode()).hexdigest()}  {p}.json\n")
    (vd / "SHA256SUMS").write_text("".join(sums))


@pytest.fixture
def env(tmp_path, monkeypatch):
    """A full sandboxed environment: R5_* paths in tmp, fake claude first on PATH, copied config, test pins."""
    ev = write_eval(tmp_path)
    sb = write_sb(tmp_path)
    cfg = tmp_path / "config"
    shutil.copytree(R5 / "config", cfg, ignore=shutil.ignore_patterns("values"))
    pins = json.loads((R5 / "config" / "pins.json").read_text())
    pins["judge_one_sha256"] = sha(ev / "tools" / "tmp-scripts" / "judge-one.sh")
    (tmp_path / "pins.json").write_text(json.dumps(pins))
    fake = tmp_path / "fake"
    fake.mkdir()
    fakebin = tmp_path / "fakebin"
    fakebin.mkdir()
    shutil.copy(R5 / "tests" / "fake" / "claude", fakebin / "claude")
    os.chmod(fakebin / "claude", 0o755)
    e = {
        "R5_OUT": str(tmp_path / "out"), "R5_SB": str(sb), "R5_EVAL": str(ev), "R5_CONFIG": str(cfg),
        "R5_PINS": str(tmp_path / "pins.json"), "R5_REPO": str(tmp_path / "repo"), "CLAUDE_PROJECTS_DIR": str(tmp_path / "projects"),
        "FAKE_DIR": str(fake), "FAKE_LOG": str(fake / "log.jsonl"), "NOFALLBACK": "1", "R5_POLL_S": "0.2",
        "PATH": f"{fakebin}:{os.environ['PATH']}",
    }
    for k, v in e.items():
        monkeypatch.setenv(k, v)
    for k in ("PANEL_COLLAB", "PANEL_KIT", "SPIKE4", "DRY_RUN"):
        monkeypatch.delenv(k, raising=False)
    (tmp_path / "out").mkdir()
    return {"tmp": tmp_path, "eval": ev, "sb": sb, "cfg": cfg, "fake": fake, "out": tmp_path / "out"}


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def bin_(name):
    return str(R5 / "bin" / name)


def fake_log(env):
    p = env["fake"] / "log.jsonl"
    return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []
