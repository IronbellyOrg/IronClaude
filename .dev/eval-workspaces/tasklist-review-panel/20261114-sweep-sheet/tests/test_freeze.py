"""K5, AO-5: bin/freeze.sh hashes the frozen files and prints the tag command; it never tags, stages or commits."""

import hashlib
import json
import subprocess

from helpers import SW
from order_support import FROZEN, git, gitcheck, make_repo, save, tags

FREEZE = SW / "bin" / "freeze.sh"


def run_freeze(roots, repo, *extra):
    tree = repo / "sw"
    cmd = [
        "bash",
        str(FREEZE),
        "--sw",
        str(tree),
        "--out",
        str(tree / "config" / "freeze.json"),
        *extra,
    ]
    return subprocess.run(cmd, capture_output=True, text=True, env=roots.with_env())


def committed_tree(tmp_roots):
    repo = make_repo(tmp_roots.root)
    save(repo, {f"sw/{k}": v for k, v in FROZEN.items()}, 1000)
    return repo


def test_freeze_prints_but_never_tags(tmp_roots):
    repo = committed_tree(tmp_roots)
    before_tags, before_log = tags(repo), git(repo, "log", "--format=%H").stdout
    r = run_freeze(tmp_roots, repo, "--tag", "sweep-freeze-test")
    assert r.returncode == 0, r.stderr
    # K5: git tag -l is unchanged, nothing was staged or committed, and the command is printed for a person
    assert tags(repo) == before_tags == []
    assert git(repo, "log", "--format=%H").stdout == before_log
    assert git(repo, "status", "--porcelain").stdout.split() == [
        "??",
        "sw/config/",
    ]  # the record only, untracked
    assert (
        '  git tag -a sweep-freeze-test -m "Sweep Sheet freeze"'
        in r.stdout.splitlines()
    )
    assert "Nothing was staged, committed or tagged" in r.stdout
    # the record: the tag name the launcher copies into run.json, and the sha256 of every frozen file
    rec = json.loads((repo / "sw" / "config" / "freeze.json").read_text())
    assert (
        rec["schema"] == "sweep-freeze/1" and rec["freeze_tag"] == "sweep-freeze-test"
    )
    assert rec["files"] == {
        k: hashlib.sha256(v.encode()).hexdigest() for k, v in sorted(FROZEN.items())
    }


def test_freeze_refuses_files_that_are_not_committed_as_they_are(tmp_roots):
    repo = committed_tree(tmp_roots)
    (repo / "sw" / "sweep" / "words.py").write_text(
        "WORDS = ('changed',)\n"
    )  # a change after the commit
    r = run_freeze(tmp_roots, repo)
    assert r.returncode == 3 and "E_UNCOMMITTED" in r.stderr and "words.py" in r.stderr
    assert not (repo / "sw" / "config" / "freeze.json").exists() and tags(repo) == []
    git(repo, "checkout", "--", "sw/sweep/words.py")
    (repo / "sw" / "briefs" / "extra.txt").write_text(
        "not committed\n"
    )  # a new frozen file that was never committed
    r = run_freeze(tmp_roots, repo)
    assert r.returncode == 3 and "extra.txt" in r.stderr


def test_freeze_needs_every_frozen_file_and_a_sane_path(tmp_roots, tmp_path):
    repo = committed_tree(tmp_roots)
    (repo / "sw" / "sweep" / "rank.py").unlink()
    r = run_freeze(tmp_roots, repo)
    assert r.returncode == 2 and "E_MISSING" in r.stderr
    r = subprocess.run(
        ["bash", str(FREEZE), "--sw", "/etc"],
        capture_output=True,
        text=True,
        env=tmp_roots.with_env(),
    )
    assert r.returncode == 2 and "E_OVERRIDE" in r.stderr
    r = subprocess.run(
        [
            "bash",
            str(FREEZE),
            "--sw",
            str(repo / "sw"),
            "--out",
            "/var/tmp/sw-freeze-refused.json",
        ],
        capture_output=True,
        text=True,
        env=tmp_roots.with_env(),
    )
    assert r.returncode == 2 and "E_NOT_WRITABLE" in r.stderr


def test_gitcheck_probe_and_the_bin_folder_is_clean(tmp_path):
    # the check is not vacuous: a file with a git add line is reported
    probe = tmp_path / "probe.sh"
    probe.write_text("#!/bin/bash\ngit add -A\n")
    assert gitcheck(tmp_path) == [f"{probe}:2:git add -A"]
    # a sandbox directory variable, a printed line and a comment are allowed
    probe.write_text(
        'git -C "$SBT" add -A -f\nprintf "  git tag -a x"\n# git push\n  echo "git commit"\n'
    )
    assert gitcheck(tmp_path) == []
    assert (
        gitcheck(SW / "bin") == []
    )  # no script of the harness stages, commits, tags or pushes except in a sandbox
