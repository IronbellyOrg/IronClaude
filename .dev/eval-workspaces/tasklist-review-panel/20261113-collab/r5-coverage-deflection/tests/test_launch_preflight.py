"""T-20 launch preflight (constraints, R-30, R-39) and T-22 sandbox build (R-03, R-09)."""
import json
import os
import subprocess
from pathlib import Path

import pytest
from conftest import CT, bin_, fake_log, run, write_values


def launch(panel, row, extra_env=None, pkgs=CT):
    return run(["bash", bin_("launch.sh"), panel, row, "--pkgs", pkgs], env={**os.environ, **(extra_env or {})})


def set_panel_model(env, model):
    p = env["cfg"] / "panels.json"
    j = json.loads(p.read_text())
    j["sl2"]["reviewers"][1]["model"] = model
    p.write_text(json.dumps(j))


def test_nofallback_required(env):
    r = launch("sl2", "r-nf", {"NOFALLBACK": ""})
    assert r.returncode == 2 and "NOFALLBACK" in r.stderr


@pytest.mark.parametrize("model", ["glm-5.3", "Qwen3.8-max", "claude-opus-5-5"])
def test_forbidden_models(env, model):
    set_panel_model(env, model)
    r = launch("sl2", "r-m", {"PANEL_COLLAB": "0", "SPIKE4": "1"})
    assert r.returncode == 2 and "forbidden" in r.stderr
    assert fake_log(env) == []


def test_judge_sum_wrong(env):
    pins = Path(os.environ["R5_PINS"])
    p = json.loads(pins.read_text())
    p["judge_one_sha256"] = "1" * 64
    pins.write_text(json.dumps(p))
    r = launch("sl2", "r-j", {"PANEL_COLLAB": "0", "SPIKE4": "1"})
    assert r.returncode == 2 and "judge-one.sh" in r.stderr


def test_parser_sums_differ(env):
    other = env["tmp"] / "findings.py"
    other.write_text("# different\n")
    pins = Path(os.environ["R5_PINS"])
    p = json.loads(pins.read_text())
    p["parser"]["installed_findings"] = str(other)
    pins.write_text(json.dumps(p))
    r = launch("sl2", "r-p", {"PANEL_COLLAB": "0", "SPIKE4": "1"})
    assert r.returncode == 2 and "installed findings.py" in r.stderr


def test_existing_row(env):
    (env["out"] / "runs" / "r-e").mkdir(parents=True)
    r = launch("sl2", "r-e", {"PANEL_COLLAB": "0", "SPIKE4": "1"})
    assert r.returncode == 2 and "already exists" in r.stderr


def test_f6_all_k0(env):  # also AC-10: hl2 with k = 0 everywhere exits 3 with the reason
    write_values(env["cfg"], "hl2", all={"k": 0, "T_report_p90_s": 40})
    r = launch("hl2", "r-k0", pkgs="TASK-WF-designSpec-20261107-075614,TASK-WF-makeTheAliasOnly-20261105-051649," + CT)
    assert r.returncode == 3 and "k = 0 on every package" in r.stderr and "T_report_p90" in r.stderr
    assert json.loads((env["out"] / "runs" / "r-k0" / "launch.json").read_text())["exit"] == 3
    assert fake_log(env) == []


def test_f6_budget_false(env):
    write_values(env["cfg"], "sl2", all={"budget_ok": False})
    assert launch("sl2", "r-b").returncode == 3


def test_f6_values_sum_mismatch(env):  # F-10 as well
    write_values(env["cfg"], "sl2")
    v = env["cfg"] / "values" / "sl2" / f"{CT}.json"
    v.write_text(v.read_text().replace('"k": 2', '"k": 1'))
    r = launch("sl2", "r-s")
    assert r.returncode == 3 and "sum mismatch" in r.stderr
    assert fake_log(env) == []


# ---------------------------------------------------------------- T-22 sandbox


@pytest.fixture
def src_repo(tmp_path):
    repo = tmp_path / "srcrepo"
    for rel in ("a.txt", ".dev/reflect/r.md", ".dev/tasks/done/P1/source.md", ".dev/research/x.md", ".dev/eval-workspaces/e.md",
                ".dev/tasks/to-do/keep.md"):
        f = repo / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(rel)
    g = ["git", "-C", str(repo)]
    subprocess.run(g + ["init", "-q"], check=True)
    subprocess.run(g + ["add", "-A"], check=True)
    subprocess.run(g + ["-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", "commit", "-qm", "c"], check=True)
    base = subprocess.run(g + ["rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    (cfg / "bases.json").write_text(json.dumps({"P1": {"base": base}}))
    ev = tmp_path / "ev" / "P1"
    ev.mkdir(parents=True)
    (ev / "candidate.md").write_text("cand\n")
    return {"R5_REPO": str(repo), "R5_SB": str(tmp_path / "sbx"), "R5_CONFIG": str(cfg), "R5_EVAL": str(tmp_path / "ev")}


def test_sandbox_build(src_repo):
    e = {**os.environ, **src_repo}
    r = run(["bash", bin_("sandbox-build.sh"), "P1"], env=e)
    assert r.returncode == 0, r.stderr
    sb = Path(src_repo["R5_SB"])
    repo = sb / "P1" / "repo"
    for gone in (".dev/reflect", ".dev/tasks/done", ".dev/research", ".dev/eval-workspaces"):
        assert not (repo / gone).exists()
    assert (repo / ".dev/tasks/to-do/keep.md").exists()
    assert subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True).stdout == ""
    assert (repo / ".git").is_dir() and (sb / "cand" / "P1" / "source.md").read_text() == ".dev/tasks/done/P1/source.md"
    assert json.loads((sb / "manifest.json").read_text())["P1"]["candidate_sha256"]
    assert run(["bash", bin_("sandbox-build.sh"), "P1"], env=e).returncode == 0  # second run: matches manifest
    bad = run(["bash", bin_("sandbox-build.sh"), "--rebuild", "../outside"], env=e)
    assert bad.returncode == 2 and "refused" in bad.stderr
    assert run(["bash", bin_("sandbox-build.sh"), "--rebuild", "P1"], env=e).returncode == 0
