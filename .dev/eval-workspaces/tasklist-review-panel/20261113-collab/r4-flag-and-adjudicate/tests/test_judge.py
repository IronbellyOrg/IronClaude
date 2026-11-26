"""bin/judge.sh with fake-claude as the judge (design 5.1 step 5; R-29)."""

import hashlib
import json
import os
from pathlib import Path

from r4help import DE, EVAL, R4, fixture, jsonl, run

JUDGE = EVAL / "tools" / "tmp-scripts" / "judge-one.sh"
PIN = "a01bd70d370d73cb32b55a7368aa28e2c12d93403237211c3a71f339ae82cfcc"


def setup(tmp_path):
    pd = tmp_path / "row" / DE
    (pd / "scoring").mkdir(parents=True)
    (pd / "panel.json").write_text(json.dumps({"pkg": DE}))
    anon = pd / "scoring" / "merged-anon.md"
    anon.write_text("review: 1 of 3\n# Merged\n")
    stamp = tmp_path / "stamp"
    stamp.write_text("")
    return pd, anon, stamp


def judge_runs(env):
    return [a for a in jsonl(Path(env["FAKE_LOG"]) / "argv.jsonl") if "claude-opus-5-5" in a["argv"]]


def common(pd, env, stamp):
    key = json.load(open(pd / "scoring" / "label-key.json"))
    stage, c = key["stage"], key["C"]
    assert stage.startswith("/tmp/jdg.") and not stage.startswith(env["R4_SBR"])
    assert os.path.realpath(os.path.join(EVAL, "arms/scoring/combos", c)) == stage
    assert not os.path.exists(stage)
    assert run(["find", EVAL, "-newer", stamp]).stdout == ""
    assert hashlib.sha256(JUDGE.read_bytes()).hexdigest() == PIN


def test_one_run(env, tmp_path):
    fixture(env, {"judge": {"score": {"gt_covered_any": ["GT1"], "gt_covered_blocking": [], "wrong_blockers": 0}}}, tmp_path)
    pd, anon, stamp = setup(tmp_path)
    r = run([R4 / "bin" / "judge.sh", pd, anon], env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    assert json.load(open(pd / "scoring" / "score.json"))["gt_covered_any"] == ["GT1"]
    assert (pd / "scoring" / "judge-status").read_text().strip() == "ok"
    assert len(judge_runs(env)) == 1
    common(pd, env, stamp)


def test_api_error_retried_once(env, tmp_path):
    fixture(env, {"judge": [{"api_error": True}, {"score": {"gt_covered_any": [], "gt_covered_blocking": [], "wrong_blockers": 1}}]}, tmp_path)
    pd, anon, stamp = setup(tmp_path)
    r = run([R4 / "bin" / "judge.sh", pd, anon], env=env)
    assert r.returncode == 0
    assert len(judge_runs(env)) == 2
    assert (pd / "scoring" / "judge.attempt1.json").exists()
    common(pd, env, stamp)


def test_double_failure(env, tmp_path):
    fixture(env, {"judge": {"api_error": True}}, tmp_path)
    pd, anon, stamp = setup(tmp_path)
    r = run([R4 / "bin" / "judge.sh", pd, anon], env=env)
    assert r.returncode != 0
    assert (pd / "scoring" / "judge-status").read_text().strip() == "judge_failed"
    assert len(judge_runs(env)) == 2
    common(pd, env, stamp)
