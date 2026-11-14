"""bin/judge.sh (D-7): the unchanged judge writes under OUT/scoring; a sha mismatch judges nothing."""
import os

from conftest import BIN, run

PKG = "TASK-WF-design-20261108-041415"


def prep(world):
    d = world.out / "scoring/op1" / PKG / "Q"
    d.mkdir(parents=True)
    (d / "merged-anon.md").write_text("x")
    return d


def test_resolves_under_out_scoring(world):
    d = prep(world)
    r = run(["bash", str(BIN / "judge.sh"), "op1", PKG, "Q"], env=world.env)
    assert r.returncode == 0, r.stderr
    assert (d / "score.json").exists()
    D = (world.tmp / "judge-calls.txt").read_text().strip()
    assert "/arms/scoring/combos/../" in D
    real = run(["realpath", "-m", D]).stdout.strip()
    assert real == str(d) and real.startswith(str(world.out / "scoring") + "/")
    assert not any((world.eval / "arms/scoring/combos").iterdir())  # nothing new under EVAL


def test_sha_mismatch_exits_5(world):
    d = prep(world)
    world.write_manifest(judge_sha="0" * 64)
    r = run(["bash", str(BIN / "judge.sh"), "op1", PKG, "Q"], env=world.env)
    assert r.returncode == 5 and not (d / "score.json").exists() and not os.path.exists(world.tmp / "judge-calls.txt")
