"""K5 and AO-5: bin/freeze.sh hashes the frozen files into config/freeze.json and prints the `git tag` command; it never
tags. The synthetic root holds invented files; the real RL is only read (`--no-write`)."""

import hashlib
import json
import os
import stat
import subprocess

from helpers import REPO
from order_support import FREEZE, FROZEN, git, init_repo, make_root, run


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def real_tags():
    return subprocess.run(
        ["git", "-C", str(REPO), "tag", "-l"], capture_output=True, text=True
    ).stdout


def test_freeze_prints_but_never_tags(tmp_path):
    # 1. no git command is started at all: a `git` on PATH that logs its calls and fails
    shim = tmp_path / "shim"
    shim.mkdir()
    log = tmp_path / "git-calls.log"
    (shim / "git").write_text(f'#!/bin/sh\necho "$@" >> {log}\nexit 1\n')
    (shim / "git").chmod((shim / "git").stat().st_mode | stat.S_IXUSR)
    root = make_root(tmp_path / "root")
    r = run(FREEZE, root, env={"PATH": f"{shim}{os.pathsep}{os.environ['PATH']}"})
    assert r.returncode == 0, r.stderr
    assert not log.exists()
    freeze = json.loads((root / "config" / "freeze.json").read_text())
    tag = freeze["freeze_tag"]
    assert f'git tag -a {tag} -m "Recipe Ledger freeze {tag}" HEAD' in r.stdout
    assert "never does" in r.stdout

    # 2. in a real repository around the root the tag list is the same before and after
    repo = init_repo(tmp_path / "repo")
    inside = make_root(repo / "rl-root")
    before = git(repo, "tag", "-l")
    assert run(FREEZE, inside).returncode == 0
    assert git(repo, "tag", "-l") == before == ""
    assert git(repo, "status", "--porcelain") == "?? rl-root/"  # nothing staged

    # 3. the real RL: read-only mode, the real tag list does not change and nothing is written
    tags = real_tags()
    r = subprocess.run(
        ["bash", str(FREEZE), "--no-write"], capture_output=True, text=True
    )
    assert r.returncode == 0, r.stderr
    assert "git tag -a rl-freeze-" in r.stdout
    assert real_tags() == tags


def test_freeze_json_names_the_files_and_the_tag(tmp_path):
    root = make_root(tmp_path / "root")
    assert run(FREEZE, root).returncode == 0
    first = (root / "config" / "freeze.json").read_text()
    freeze = json.loads(first)
    assert freeze["schema"] == "rl-freeze/1"
    assert set(freeze["files"]) == set(
        FROZEN
    )  # recipes, lenses, cards, briefs, rl/*.py
    assert freeze["files"]["recipes/rl-block.txt"] == sha(
        FROZEN["recipes/rl-block.txt"]
    )
    assert freeze["freeze_tag"] == f"rl-freeze-{freeze['combined_sha256'][:12]}"
    # the same files give the same record; one changed byte gives a new tag name
    assert run(FREEZE, root).returncode == 0
    assert (root / "config" / "freeze.json").read_text() == first
    (root / "rl" / "render.py").write_text("X = 2\n")
    assert run(FREEZE, root).returncode == 0
    assert (
        json.loads((root / "config" / "freeze.json").read_text())["freeze_tag"]
        != freeze["freeze_tag"]
    )


def test_no_write_and_missing_file(tmp_path):
    root = make_root(tmp_path / "root")
    r = run(FREEZE, root, "--no-write")
    assert r.returncode == 0 and not (root / "config" / "freeze.json").exists()
    (root / "recipes" / "search-form.txt").unlink()
    r = run(FREEZE, root, "--no-write")
    assert r.returncode == 2 and "E_MISSING: recipes/search-form.txt" in r.stderr
