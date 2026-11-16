"""REQ-33, REQ-36, REQ-44: bin/check-order.sh compares commit times and hashes in a temporary repository.
Commit times are set by the tests (the times below are epoch seconds), so the order is exact."""

import hashlib
import json
import os
import subprocess
from types import SimpleNamespace

from helpers import SW
from order_support import FROZEN, make_repo, mark, save, write

CHECK = SW / "bin" / "check-order.sh"
FREEZE = SW / "bin" / "freeze.sh"
GT_FILE = '{"items": []}\n'
GT_PATH = "sw/holdout-gt/HO-1/ground-truth.json"


def sub(roots, name):
    """Another root under the test's folder, so that one test can hold several repositories."""
    p = roots.root / name
    p.mkdir()
    return SimpleNamespace(root=p, with_env=roots.with_env)


def check(roots, mode, **kw):
    cmd = ["bash", str(CHECK), mode]
    for k, v in kw.items():
        cmd += [f"--{k.replace('_', '-')}", str(v)]
    return subprocess.run(cmd, capture_output=True, text=True, env=roots.with_env())


def run_freeze(roots, tree, tag):
    out = tree / "config" / "freeze.json"
    r = subprocess.run(
        ["bash", str(FREEZE), "--sw", str(tree), "--out", str(out), "--tag", tag],
        capture_output=True,
        text=True,
        env=roots.with_env(),
    )
    assert r.returncode == 0, r.stderr
    return out


def frozen_repo(roots, tag_time=1100, tag="sweep-freeze-test", tagged=True):
    """A repository with the frozen files committed at 1000, freeze.json (made by bin/freeze.sh) committed and, unless
    `tagged` is False, tagged at `tag_time`. Returns (repo, freeze.json path)."""
    repo = make_repo(roots.root)
    save(repo, {f"sw/{k}": v for k, v in FROZEN.items()}, 1000)
    out = run_freeze(roots, repo / "sw", tag)
    save(repo, {}, tag_time, "freeze record")
    if tagged:
        mark(repo, tag, tag_time)
    return repo, out


def freeze_args(repo, freeze):
    return {"repo": repo, "freeze": freeze, "gt": repo / "sw" / "holdout-gt"}


def test_freeze_tag_before_gt_commit(tmp_roots):
    repo, freeze = frozen_repo(tmp_roots)
    save(repo, {GT_PATH: GT_FILE}, 2000)  # the hold-out author writes it after the tag
    r = check(tmp_roots, "freeze", **freeze_args(repo, freeze))
    assert r.returncode == 0, r.stderr
    assert (
        "ORDER_OK freeze: tag sweep-freeze-test (1100) is earlier than the first ground-truth commit (2000)"
        in r.stdout
    )


def test_gt_before_tag_fails(tmp_roots):
    repo = make_repo(tmp_roots.root)
    save(repo, {GT_PATH: GT_FILE}, 500)  # the ground truth first: the wrong order
    save(repo, {f"sw/{k}": v for k, v in FROZEN.items()}, 1000)
    freeze = run_freeze(tmp_roots, repo / "sw", "late")
    save(repo, {}, 1100)
    mark(repo, "late", 1100)
    r = check(tmp_roots, "freeze", **freeze_args(repo, freeze))
    assert (
        r.returncode == 1
        and "(1100) is not earlier than the first ground-truth commit (500)" in r.stderr
    )
    # the same time is not earlier either: the order cannot be shown
    same_root = sub(tmp_roots, "same")
    repo2, freeze2 = frozen_repo(same_root, tag_time=1100)
    save(repo2, {GT_PATH: GT_FILE}, 1100)
    r = check(tmp_roots, "freeze", **freeze_args(repo2, freeze2))
    assert (
        r.returncode == 1
        and "(1100) is not earlier than the first ground-truth commit (1100)"
        in r.stderr
    )


def test_freeze_needs_the_tag_and_a_committed_ground_truth(tmp_roots):
    repo, freeze = frozen_repo(tmp_roots, tagged=False)
    write(repo, {GT_PATH: GT_FILE})  # written, not committed
    args = freeze_args(repo, freeze)
    r = check(tmp_roots, "freeze", **args)
    assert (
        r.returncode == 1 and "freeze tag sweep-freeze-test does not exist" in r.stderr
    )
    mark(repo, "sweep-freeze-test", 1100)
    r = check(tmp_roots, "freeze", **args)
    assert (
        r.returncode == 1 and "is not committed" in r.stderr
    )  # an uncommitted ground truth shows no order
    r = check(tmp_roots, "freeze", **{**args, "freeze": repo / "nope.json"})
    assert r.returncode == 2 and "no freeze record" in r.stderr
    assert check(tmp_roots, "nonsense").returncode == 2


def test_freeze_json_hashes_match_files(tmp_roots):
    repo, freeze = frozen_repo(tmp_roots)
    save(repo, {GT_PATH: GT_FILE}, 2000)
    args = freeze_args(repo, freeze)
    assert check(tmp_roots, "freeze", **args).returncode == 0
    # an extractor changed after the freeze, committed or not: the hash check fails
    write(repo, {"sw/sweep/extractors.py": "EXTRACTORS = {'E1': 1}\n"})
    r = check(tmp_roots, "freeze", **args)
    assert (
        r.returncode == 1 and "sweep/extractors.py changed after the freeze" in r.stderr
    )
    assert "cards/C1.json" not in r.stderr  # only the changed file is named
    save(repo, {}, 2100, "extractor edit")
    assert check(tmp_roots, "freeze", **args).returncode == 1
    write(
        repo, {"sw/sweep/extractors.py": FROZEN["sweep/extractors.py"]}
    )  # restored: the recorded hash holds again
    assert check(tmp_roots, "freeze", **args).returncode == 0
    rec = json.loads(freeze.read_text())
    assert (
        rec["files"]["sweep/extractors.py"]
        == hashlib.sha256(FROZEN["sweep/extractors.py"].encode()).hexdigest()
    )


def prereg_repo(roots, gt_hash=None, prereg_time=100):
    repo = make_repo(roots.root)
    prereg = {
        "schema": "sweep-prereg/1",
        "ground_truth_sha256": {} if gt_hash is None else {"HO-1": gt_hash},
    }
    save(
        repo,
        {GT_PATH: GT_FILE, "sw/config/prereg.json": json.dumps(prereg)},
        prereg_time,
    )
    return repo


def prereg_args(repo):
    return {
        "repo": repo,
        "prereg": repo / "sw" / "config" / "prereg.json",
        "runs": repo / "sw" / "runs",
        "gt_dir": repo / "sw" / "holdout-gt",
    }


def test_gt_hash_matches_prereg(tmp_roots):
    good = hashlib.sha256(GT_FILE.encode()).hexdigest()
    repo = prereg_repo(tmp_roots, gt_hash=good)
    r = check(tmp_roots, "prereg", **prereg_args(repo))
    assert r.returncode == 0, r.stderr
    assert (
        "the ground-truth hashes match" in r.stdout and "none has started" in r.stdout
    )
    # the ground truth is edited after it was hashed: the record no longer matches
    write(repo, {GT_PATH: '{"items": [1]}\n'})
    r = check(tmp_roots, "prereg", **prereg_args(repo))
    assert r.returncode == 1 and "the ground truth of HO-1 has sha256" in r.stderr
    # a hash that the record names for a document with no ground-truth file
    (repo / GT_PATH).unlink()
    r = check(tmp_roots, "prereg", **prereg_args(repo))
    assert r.returncode == 1 and "no ground-truth file for HO-1" in r.stderr
    # prereg.json that was never committed shows no order
    other = make_repo(sub(tmp_roots, "uncommitted").root)
    write(other, {"sw/config/prereg.json": "{}\n"})
    r = check(tmp_roots, "prereg", **prereg_args(other))
    assert r.returncode == 1 and "is not committed" in r.stderr


def test_prereg_commit_before_first_run(tmp_roots):
    repo = prereg_repo(tmp_roots, prereg_time=100)
    save(repo, {"sw/runs/stage1/r1/run.json": "{}\n"}, 200)
    r = check(tmp_roots, "prereg", **prereg_args(repo))
    assert (
        r.returncode == 0 and "is earlier than the first run.json (200)" in r.stdout
    ), r.stderr
    # the first commit of any run.json counts: a second run committed at 150 is the first
    save(repo, {"sw/runs/stage1/r0/run.json": "{}\n"}, 150)
    r = check(tmp_roots, "prereg", **prereg_args(repo))
    assert r.returncode == 0 and "(150)" in r.stdout
    # the other order, and equal times (the order cannot be shown)
    late = prereg_repo(sub(tmp_roots, "late"), prereg_time=300)
    save(late, {"sw/runs/stage1/r1/run.json": "{}\n"}, 300)
    r = check(tmp_roots, "prereg", **prereg_args(late))
    assert (
        r.returncode == 1 and "is not earlier than the first run.json (300)" in r.stderr
    )
    early = prereg_repo(sub(tmp_roots, "early"), prereg_time=300)
    save(
        early, {"sw/runs/stage1/r1/run.json": "{}\n"}, 50
    )  # a run committed before prereg.json
    r = check(tmp_roots, "prereg", **prereg_args(early))
    assert r.returncode == 1 and "(50)" in r.stderr
    # runs that are not committed are timed by their file times
    plain = prereg_repo(sub(tmp_roots, "plain"), prereg_time=1000)
    run = plain / "sw" / "runs" / "stage1" / "r1" / "run.json"
    write(plain, {"sw/runs/stage1/r1/run.json": "{}\n"})
    os.utime(run, (500, 500))  # the run file is older than prereg.json
    r = check(tmp_roots, "prereg", **prereg_args(plain))
    assert r.returncode == 1 and "(500)" in r.stderr
    os.utime(run, (5000, 5000))
    assert check(tmp_roots, "prereg", **prereg_args(plain)).returncode == 0


def test_every_planted_plan_has_twin(tmp_path, tmp_roots):
    d = tmp_path / "planted"
    d.mkdir()
    for name in ("p1.md", "p1-clean.md", "p2.md", "p2-clean.md"):
        (d / name).write_text("text\n")
    manifest = d / "manifest.json"
    entries = [
        {"plan": "p1.md", "twin": "p1-clean.md"},
        {"plan": "p2.md", "twin": "p2-clean.md"},
    ]
    manifest.write_text(json.dumps({"planted": entries}))
    r = check(tmp_roots, "twins", manifest=manifest)
    assert r.returncode == 0 and "all 2 planted plans have an existing twin" in r.stdout
    (d / "p2-clean.md").unlink()  # a twin that is named but missing
    r = check(tmp_roots, "twins", manifest=manifest)
    assert (
        r.returncode == 1 and "the twin p2-clean.md of p2.md does not exist" in r.stderr
    )
    manifest.write_text(
        json.dumps({"planted": [{"plan": "p3.md"}]})
    )  # a planted plan with no twin at all
    r = check(tmp_roots, "twins", manifest=manifest)
    assert r.returncode == 1 and "planted plan p3.md has no clean twin" in r.stderr
    assert check(tmp_roots, "twins").returncode == 2
