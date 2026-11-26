"""T-15: the unchanged judge-one.sh writes inside the tmp scoring root through the relative-path trick."""

import hashlib
import json
import os

from conftest import A1DIR, STUB_BIN, jload, run

DS = "TASK-WF-designSpec-20261107-075614"
PIN = "a01bd70d370d73cb32b55a7368aa28e2c12d93403237211c3a71f339ae82cfcc"


def listing(p):
    return sorted(str(x.relative_to(p)) for x in p.rglob("*"))


def test_judge_writes_under_tmp(tmp_path):
    judge = A1DIR / "tools" / "tmp-scripts" / "judge-one.sh"
    assert hashlib.sha256(judge.read_bytes()).hexdigest() == PIN
    combos = A1DIR / "arms" / "scoring" / "combos"
    before = listing(combos)
    opaque = tmp_path / "scoring" / "0123456789ab"
    out = opaque / DS / "R"
    out.mkdir(parents=True)
    (out / "merged-anon.md").write_text("# merged\n")
    stub = tmp_path / "stub"
    stub.mkdir()
    (stub / "score.body").write_text(json.dumps({"label": "R", "gt_covered_any": ["GT2"], "gt_covered_blocking": [], "wrong_blockers": 0}))
    (stub / "plan").write_text(f"judge {stub / 'score.body'}\n")
    c = os.path.relpath(opaque, combos)
    env = dict(os.environ, PATH=f"{STUB_BIN}:{os.environ['PATH']}", STUB_DIR=str(stub))
    r = run(["bash", str(judge), c, DS, "R"], env=env)
    assert r.returncode == 0 and r.stdout.startswith("OK"), r.stdout + r.stderr
    assert jload(out / "score.json")["gt_covered_any"] == ["GT2"] and (out / "judge.json").exists()
    assert listing(combos) == before
    argv = (stub / "argv.1").read_text().splitlines()
    assert argv[argv.index("--model") + 1] == "claude-opus-5-5"
