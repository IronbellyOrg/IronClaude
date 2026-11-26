"""T-19 anonymiser (R-10, R-29, MR:953) and T-21 judge path (D9)."""
import json
import os
from pathlib import Path

from conftest import CT, R5, bin_, run
from r5 import read_jsonl


def merged(env, text, row="row"):
    d = env["out"] / "runs" / row / CT
    d.mkdir(parents=True)
    (d / "run.json").write_text(json.dumps({"arm": "F6-sl2"}))
    (d / "merged-1.md").write_text(text)
    return d


def anon(env, row="row"):
    r = run(["bash", bin_("anon.sh"), row, CT])
    tok, lab = r.stdout.split()
    return r.returncode, env["out"] / "scoring" / tok / CT / lab / "merged-anon.md"


def test_anon_rewrites(env):
    text = (f"candidate: {env['eval']}/{CT}/candidate.md sha256 abc\n"
            "| L1 | t1b-1 t4-1 T3-1 | report " + str(env["eval"]) + "/x/y.md, more |\n"
            f"see {R5}/runs/row and /tmp/evalsb-collab-r5/{CT}/repo\n"
            '{"id":"F1","origin":"peer","claim":"applying M7 as the panel request asked, Task 9"}\n'
            "#### L1.R2 (m1)\nprose Task-6 and T1bModel01-03\n")
    merged(env, text)
    rc, f = anon(env)
    out = f.read_text()
    assert rc == 0
    assert "R1" in out and "R3" in out and "t1b-1" not in out.lower() and "t3-1" not in out.lower()
    assert "candidate: <candidate file> sha256" in out and str(env["eval"]) not in out
    assert "report <redacted>" in out and str(R5) not in out and "evalsb-collab" not in out
    assert '"origin"' not in out and "M7" not in out and "panel request" not in out.lower()
    assert "Task-6" in out and "T1bModel01-03" in out and "(<redacted>)" in out
    key = read_jsonl(env["out"] / "results" / "scoring-keys.jsonl")[-1]
    assert key["status"] == "ok" and key["redactions"] >= 3 and key["arm"] == "F6-sl2"


def test_anon_postcheck_blocks(env):
    merged(env, "a path /x/board/y stays\n")
    rc, _f = anon(env)
    assert rc == 1
    st = json.loads((env["out"] / "runs" / "row" / CT / "pkg-status.json").read_text())
    assert st["anon"] == "anon_failed"


def test_judge_path_resolves(env):  # T-21
    tok = "abcdef012345"
    r = run(["bash", bin_("judge.sh"), tok, CT, "Q"], env={**os.environ, "DRY_RUN": "1"})
    assert r.returncode == 0, r.stderr
    combo = r.stdout.split("COMBO: ")[1].strip()
    resolved = os.path.realpath(os.path.join(env["eval"], "arms", "scoring", "combos", combo))
    assert resolved == os.path.realpath(env["out"] / "scoring" / tok)


def test_judge_default_path_matches_design():
    e = {k: v for k, v in os.environ.items() if not k.startswith("R5_")}
    r = run(["bash", bin_("judge.sh"), "abcdef012345", CT, "Q"], env={**e, "DRY_RUN": "1"})
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "COMBO: ../../../../20261113-collab/r5-coverage-deflection/scoring/abcdef012345"


def test_judge_refuses_wrong_sum(env):
    pins = Path(os.environ["R5_PINS"])
    p = json.loads(pins.read_text())
    p["judge_one_sha256"] = "0" * 64
    pins.write_text(json.dumps(p))
    r = run(["bash", bin_("judge.sh"), "abcdef012345", CT, "Q"])
    assert r.returncode == 2 and "refused" in r.stderr
