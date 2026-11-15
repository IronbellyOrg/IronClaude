"""REQ-33, REQ-36 and REQ-44: bin/check-order.sh. Every test builds a temporary git repository under /tmp with synthetic
files and explicit commit dates (T0 plus whole days); the real repository history is never read."""

import hashlib
import json
import os

from order_support import (
    DAY,
    FREEZE,
    ORDER,
    T0,
    commit,
    git,
    init_repo,
    make_root,
    run,
)

GT = "holdout-gt/HO-1/ground-truth.json"
GT_TEXT = '{"items": [{"id": "I1", "description": "an invented item"}]}\n'


def frozen_repo(tmp_path):
    """A repository whose folder rl-root holds the synthetic frozen files and their config/freeze.json, committed at day 0."""
    repo = init_repo(tmp_path / "repo")
    root = make_root(repo / "rl-root")
    assert run(FREEZE, root).returncode == 0
    commit(repo, "frozen files", day=0)
    tag = json.loads((root / "config" / "freeze.json").read_text())["freeze_tag"]
    return repo, root, tag


def commit_gt(repo, root, day):
    p = root / GT
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(GT_TEXT, encoding="utf-8")
    commit(repo, "hold-out ground truth", day=day)


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def test_freeze_tag_before_gt_commit(tmp_path):
    repo, root, tag = frozen_repo(tmp_path)
    git(repo, "tag", "-a", tag, "-m", "freeze", day=1)
    commit_gt(repo, root, day=2)
    r = run(ORDER, root, "freeze")
    assert r.returncode == 0, r.stdout + r.stderr
    assert f"tag {tag} time {T0 + DAY}" in r.stdout
    assert f"first ground-truth commit time {T0 + 2 * DAY}" in r.stdout
    assert r.stdout.rstrip().endswith("OK")


def test_gt_before_tag_fails(tmp_path):
    # a lightweight tag on the commit that holds the ground truth: its commit time is not earlier
    repo, root, tag = frozen_repo(tmp_path)
    commit_gt(repo, root, day=1)
    git(repo, "tag", tag)
    r = run(ORDER, root, "freeze")
    assert (
        r.returncode == 1
        and "not earlier than the first ground-truth commit" in r.stdout
    )

    # an annotated tag made after the ground truth, on the old frozen commit: its tagger date is what counts
    repo2, root2, tag2 = frozen_repo(tmp_path / "second")
    commit_gt(repo2, root2, day=1)
    git(repo2, "tag", "-a", tag2, "-m", "late", "HEAD~1", day=3)
    r = run(ORDER, root2, "freeze")
    assert r.returncode == 1 and "not earlier" in r.stdout


def test_freeze_needs_a_tag_a_ground_truth_commit_and_a_record(tmp_path):
    repo, root, tag = frozen_repo(tmp_path)
    commit_gt(repo, root, day=2)
    r = run(
        ORDER, root, "freeze"
    )  # the tag does not exist (only a person creates it, K5)
    assert r.returncode == 1 and f"tag {tag} does not exist" in r.stdout
    repo2, root2, tag2 = frozen_repo(tmp_path / "second")
    git(repo2, "tag", "-a", tag2, "-m", "freeze", day=1)
    r = run(
        ORDER, root2, "freeze"
    )  # no ground truth committed yet: the order cannot be shown
    assert r.returncode == 1 and "no ground-truth file is committed" in r.stdout
    (root2 / "config" / "freeze.json").unlink()
    assert run(ORDER, root2, "freeze").returncode == 2


def test_freeze_json_hashes_match_files(tmp_path):
    repo, root, tag = frozen_repo(tmp_path)
    git(repo, "tag", "-a", tag, "-m", "freeze", day=1)
    commit_gt(repo, root, day=2)
    assert run(FREEZE, root, "--check").returncode == 0
    assert run(ORDER, root, "freeze").returncode == 0
    # a recipe, the lens table, a brief, a card or an rl/*.py file changed after the tag fails the check; a new file too
    for rel, word in (
        ("recipes/recipes.json", "CHANGED"),
        ("recipes/search-form.txt", "CHANGED"),
        ("config/lenses.json", "CHANGED"),
        ("briefs/base.txt", "CHANGED"),
        ("cards/C2.json", "CHANGED"),
        ("rl/render.py", "CHANGED"),
        ("rl/new.py", "ADDED"),
        ("briefs/cb9.txt", "ADDED"),
    ):
        p = root / rel
        old = p.read_text() if p.exists() else None
        p.write_text((old or "") + "edit\n")
        r = run(ORDER, root, "freeze")
        assert r.returncode == 1 and f"{word} {rel}" in r.stdout, rel
        assert "edit" not in r.stdout.replace(rel, "")  # paths only
        assert run(FREEZE, root, "--check").returncode == 1
        if old is None:
            p.unlink()
        else:
            p.write_text(old)
    # a removed file
    (root / "cards" / "C1.json").unlink()
    r = run(FREEZE, root, "--check")
    assert r.returncode == 1 and "REMOVED cards/C1.json" in r.stdout


def test_gt_hash_matches_prereg(tmp_path):
    root = make_root(tmp_path / "root")
    (root / GT).parent.mkdir(parents=True)
    (root / GT).write_text(GT_TEXT, encoding="utf-8")
    prereg = root / "config" / "prereg.json"
    prereg.parent.mkdir(exist_ok=True)
    prereg.write_text(json.dumps({"gt_sha256": {GT: sha(GT_TEXT)}}))
    r = run(ORDER, root, "gt-hash")
    assert r.returncode == 0 and "match 1 files" in r.stdout
    # a changed ground-truth file: the path is named, its content is not
    (root / GT).write_text(GT_TEXT.replace("invented", "secretword"))
    r = run(ORDER, root, "gt-hash")
    assert r.returncode == 1 and f"{GT} does not match" in r.stdout
    assert "secretword" not in r.stdout + r.stderr
    # a ground-truth file that prereg.json does not list, and an entry whose file is gone
    (root / GT).write_text(GT_TEXT)
    other = root / "holdout-gt" / "HO-2" / "ground-truth.json"
    other.parent.mkdir()
    other.write_text("{}\n")
    r = run(ORDER, root, "gt-hash")
    assert (
        r.returncode == 1
        and "holdout-gt/HO-2/ground-truth.json has no entry" in r.stdout
    )
    other.unlink()
    prereg.write_text(
        json.dumps(
            {
                "gt_sha256": {
                    GT: sha(GT_TEXT),
                    "holdout-gt/HO-9/ground-truth.json": "0" * 64,
                }
            }
        )
    )
    r = run(ORDER, root, "gt-hash")
    assert (
        r.returncode == 1 and "HO-9/ground-truth.json, which does not exist" in r.stdout
    )
    assert run(ORDER, tmp_path / "empty-root", "gt-hash").returncode == 2


def test_every_planted_plan_has_twin(tmp_path):
    root = make_root(tmp_path / "root")
    for rel in ("planted/HO-7.md", "twins/HO-7-clean.md", "planted/HO-8.md"):
        p = root / "holdout" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("invented plan\n")
    manifest = root / "holdout-gt" / "planted-set.json"
    manifest.parent.mkdir()
    entries = [
        {"plan": "holdout/planted/HO-7.md", "twin": "holdout/twins/HO-7-clean.md"},
        {"plan": "holdout/planted/HO-8.md", "twin": "holdout/twins/HO-8-clean.md"},
    ]
    manifest.write_text(json.dumps({"planted": entries}))
    r = run(ORDER, root, "twins")  # the second twin file does not exist
    assert (
        r.returncode == 1
        and "twin holdout/twins/HO-8-clean.md of holdout/planted/HO-8.md does not exist"
        in r.stdout
    )
    (root / "holdout" / "twins" / "HO-8-clean.md").write_text("invented twin\n")
    r = run(ORDER, root, "twins")
    assert r.returncode == 0 and "every one of 2 planted plans has a twin" in r.stdout
    entries.append({"plan": "holdout/planted/HO-9.md"})  # no twin named at all
    manifest.write_text(json.dumps({"planted": entries}))
    r = run(ORDER, root, "twins")
    assert r.returncode == 1 and "holdout/planted/HO-9.md names no twin" in r.stdout
    manifest.write_text(json.dumps({"planted": []}))
    assert run(ORDER, root, "twins").returncode == 1


def add_run(repo, root, name, day):
    p = root / "runs" / name / "run.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("{}\n")
    if day is not None:
        commit(repo, f"run {name}", day=day)


def add_prereg(repo, root, day):
    p = root / "config" / "prereg.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('{"schema": "rl-prereg/1"}\n')
    commit(repo, "prereg", day=day)


def test_prereg_commit_before_first_run(tmp_path):
    repo, root, _ = frozen_repo(tmp_path)
    add_prereg(repo, root, day=1)
    r = run(ORDER, root, "prereg")  # no run.json yet
    assert r.returncode == 0 and "no run.json yet" in r.stdout
    add_run(repo, root, "rehearsal-z0", day=0)  # a rehearsal is not a hold-out run
    add_run(repo, root, "r1", day=2)
    add_run(repo, root, "r2", day=3)
    r = run(ORDER, root, "prereg")
    assert r.returncode == 0, r.stdout
    assert f"prereg.json first commit time {T0 + DAY}" in r.stdout
    assert f"first run.json time {T0 + 2 * DAY}" in r.stdout

    # the other order: the first run.json is committed before prereg.json
    repo2, root2, _ = frozen_repo(tmp_path / "second")
    add_run(repo2, root2, "r1", day=1)
    add_prereg(repo2, root2, day=2)
    r = run(ORDER, root2, "prereg")
    assert (
        r.returncode == 1
        and "prereg.json is not earlier than the first run.json" in r.stdout
    )

    # prereg.json not committed at all
    repo3, root3, _ = frozen_repo(tmp_path / "third")
    (root3 / "config" / "prereg.json").write_text("{}\n")
    r = run(ORDER, root3, "prereg")
    assert r.returncode == 1 and "config/prereg.json is not committed" in r.stdout


def test_an_uncommitted_run_counts_at_its_modification_time(tmp_path):
    repo, root, _ = frozen_repo(tmp_path)
    add_prereg(repo, root, day=1)
    add_run(
        repo, root, "r1", day=None
    )  # never committed; modified now, which is before the dated commit
    r = run(ORDER, root, "prereg")
    assert r.returncode == 1
    os.utime(root / "runs" / "r1" / "run.json", (T0 + 5 * DAY, T0 + 5 * DAY))
    assert run(ORDER, root, "prereg").returncode == 0
