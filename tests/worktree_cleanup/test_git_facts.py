"""Task 7: the test support itself, and the git facts the script relies on.

Everything runs in throwaway repositories under ``tmp_path``; no test touches a real
worktree. The reply shapes in ``fixtures/`` are hand-written from the spec and the Orca
help, not literal captures (see ``fixtures/README.md``), as in
``tests/merged_pr_log/test_merged_pr_log.py``.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from .conftest import STANDARD_NAMES, git_in

FIXTURES = Path(__file__).parent / "fixtures"

SEVEN_SHAPES = {
    "gh_pr_list.json": list,
    "gh_pr_view.json": dict,
    "gh_issue_view.json": dict,
    "orca_repo_list.json": dict,
    "orca_worktree_ps.json": dict,
    "orca_reference_list.json": dict,
    "orca_terminal_list.json": dict,
}


def write(path: Path, text: str = "x\n") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


# --- the support: fixtures, throwaway repos, the recording runner ------------------------------


@pytest.mark.parametrize("name,kind", SEVEN_SHAPES.items())
def test_one_recorded_shape_for_each_of_the_seven_replies(name, kind):
    doc = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
    assert isinstance(doc, kind)
    assert "ghp_" not in (FIXTURES / name).read_text(encoding="utf-8")


def test_the_fixture_shapes_feed_the_script_parsers(wc):
    prs = wc.parse_pull_requests(
        (FIXTURES / "gh_pr_list.json").read_text(encoding="utf-8")
    )
    assert [(p.number, p.state) for p in prs] == [(700, "MERGED"), (650, "CLOSED")]
    assert prs[0].closing == (wc.IssueRef("IronbellyOrg/IronClaude", 21),)
    assert json.loads((FIXTURES / "gh_pr_view.json").read_text())["state"] == "MERGED"
    assert (
        json.loads((FIXTURES / "gh_issue_view.json").read_text())["state"] == "CLOSED"
    )


def test_the_standard_worktrees_cover_every_local_state(
    wc, runner_cls, local_origin_repo
):
    wts = local_origin_repo.add_standard_worktrees()
    assert set(wts) == set(STANDARD_NAMES)
    runner = runner_cls()
    repo = wc.OrcaRepo("r", str(local_origin_repo.main), "example")
    found = {
        os.path.basename(w.path): w
        for w in wc.discover_worktrees(runner, [repo]).worktrees
    }
    assert found["detached"].detached and found["locked"].locked
    states = {}
    for name in ("clean", "tracked-edit", "dev-files", "env-file", "build-only"):
        states[name] = wc.gather_facts(runner, found[name]).state
    assert (
        states["clean"].changed_tracked == [] and states["clean"].ignored_unknown == []
    )
    assert states["tracked-edit"].changed_tracked == ["README.md"]
    assert states["dev-files"].untracked_dev and states["dev-files"].ignored_dev
    assert states["env-file"].ignored_unknown == [".env"]
    assert (
        states["build-only"].ignored_build and not states["build-only"].ignored_unknown
    )
    # the origin is a local bare repository, and a second one stands in for the evidence repo
    assert git_in(local_origin_repo.main, "remote", "get-url", "origin").strip() == str(
        local_origin_repo.bare
    )


def test_a_second_bare_repository_stands_in_for_the_evidence_repo(
    evidence_bare, tmp_path
):
    clone = tmp_path / "evidence-clone"
    git_in(tmp_path, "clone", "-q", str(evidence_bare), str(clone))
    assert (clone / "README.md").read_text(encoding="utf-8") == "evidence\n"


def test_the_fake_proc_builder_is_shared(wc, tmp_path):
    from .conftest import make_fake_proc

    wt = tmp_path / "wt"
    wt.mkdir()
    proc = make_fake_proc(tmp_path / "proc", {11: wt})
    assert wc.processes_inside(wc.scan_processes(str(proc)), str(wt)) == [
        (11, "proc11")
    ]


def test_the_recording_runner_lists_every_command_and_refuses_what_the_real_runner_refuses(
    wc, runner_cls, local_origin_repo
):
    runner = runner_cls()
    runner.run(["git", "rev-parse", "--git-dir"], cwd=str(local_origin_repo.main))
    runner.run(
        ["orca", "repo", "list", "--json"]
    )  # no canned reply: answered 127, recorded
    assert [c.argv for c in runner.commands] == [
        ["git", "rev-parse", "--git-dir"],
        ["orca", "repo", "list", "--json"],
    ]
    real = wc.Runner(evidence_dir=None)
    for argv in (
        ["git", "reset", "--hard"],
        ["git", "branch", "-D", "x"],
        ["git", "worktree", "remove", "--force", "/x"],
        ["orca", "worktree", "rm", "--worktree", "id:1", "--force"],
        ["rm", "-rf", "/x"],
        ["gh", "pr", "merge", "1", "--repo", "IronbellyOrg/IronClaude"],
    ):
        with pytest.raises(wc.RefusedCommand):
            real.check_allowed(argv)
        with pytest.raises(wc.RefusedCommand):
            runner.run(argv)
    assert len(runner.commands) == 2  # the refused ones were never recorded or run


def test_a_real_process_never_starts_outside_the_test_tmp_folder(
    wc, runner_cls, throwaway_repo, tmp_path
):
    runner = runner_cls()
    outside = Path(__file__).resolve().parents[2]  # the real checkout
    refused = [
        (["git", "rev-parse", "--git-dir"], str(outside)),
        (["git", "rev-parse", "--git-dir"], None),
        (["git", "rev-parse", "--git-dir"], str(tmp_path.parent)),
        (
            ["git", "-C", str(outside), "rev-parse", "--git-dir"],
            str(throwaway_repo.main),
        ),
        (["git", "-C", "..", "rev-parse", "--git-dir"], str(tmp_path)),
        (["tar", "-tzf", str(outside / "README.md")], str(tmp_path)),
        (["xargs", "-0", "git", "clean", "-f", "-x", "--"], str(outside)),
    ]
    runner.register_saved(str(outside), ["x"])
    for argv, cwd in refused:
        with pytest.raises(AssertionError, match="outside the test tmp folder"):
            runner.run(argv, cwd=cwd, stdin=b"x\0")
    # inside the tmp folder (also through a symlink, which is resolved) it still runs
    link = tmp_path / "link"
    link.symlink_to(throwaway_repo.main)
    assert runner.run(["git", "rev-parse", "--git-dir"], cwd=str(link)).returncode == 0
    assert (
        runner.run(
            ["git", "-C", str(throwaway_repo.main), "rev-parse", "--git-dir"],
            cwd=str(tmp_path),
        ).returncode
        == 0
    )


# --- the git facts of source section 9 ------------------------------------------------------------


def test_worktree_remove_without_force_refuses_dirty_worktrees_and_removes_ignored_only(
    wc, runner_cls, throwaway_repo
):
    untracked = throwaway_repo.add_worktree("with-untracked")
    write(untracked / "new.txt")
    modified = throwaway_repo.add_worktree("with-edit")
    write(modified / "README.md", "edited\n")
    ignored_only = throwaway_repo.add_worktree("only-ignored")
    write(ignored_only / ".env", "NAME=placeholder\n")
    write(ignored_only / "pkg" / "__pycache__" / "m.pyc")
    runner = runner_cls()
    for path in (untracked, modified):
        res = runner.run(
            ["git", "worktree", "remove", str(path)], cwd=str(throwaway_repo.main)
        )
        assert res.returncode != 0 and path.is_dir()
        assert "contains modified or untracked files" in res.stderr
    res = runner.run(
        ["git", "worktree", "remove", str(ignored_only)], cwd=str(throwaway_repo.main)
    )
    assert res.returncode == 0, res.stderr
    assert not ignored_only.exists()
    listed = git_in(throwaway_repo.main, "worktree", "list", "--porcelain")
    assert str(ignored_only) not in listed and str(untracked) in listed


def test_branch_d_refuses_after_a_squash_merge(wc, runner_cls, throwaway_repo):
    main = throwaway_repo.main
    wt = throwaway_repo.add_worktree("squashed")
    write(wt / "feature.txt")
    git_in(wt, "add", "feature.txt")
    git_in(wt, "commit", "-q", "-m", "feature")
    git_in(main, "merge", "-q", "--squash", "squashed")
    git_in(main, "commit", "-q", "-m", "squash of squashed")
    git_in(main, "worktree", "remove", str(wt))  # the folder is gone; the branch is not
    runner = runner_cls()
    res = runner.run(["git", "branch", "-d", "squashed"], cwd=str(main))
    assert res.returncode != 0 and "not fully merged" in res.stderr
    assert "squashed" in git_in(main, "branch", "--list", "squashed")
    # a branch whose commits are on main is deleted by the same command
    plain = throwaway_repo.add_worktree("plain")
    git_in(main, "worktree", "remove", str(plain))
    assert runner.run(["git", "branch", "-d", "plain"], cwd=str(main)).returncode == 0


def test_git_clean_with_literal_pathspecs_removes_exactly_the_listed_files(
    wc, runner_cls, throwaway_repo
):
    wt = throwaway_repo.add_worktree("cleaning")
    listed = [".dev/a b.txt", ".dev/local/run [1].log", ".dev/tasks/*.md"]
    for rel in listed:
        write(wt / rel)
    unlisted = [
        ".dev/keep.txt",
        "loose.txt",
        ".env",
        ".dev/tasks/other.md",
        ".dev/local/run 1.log",
    ]
    for rel in unlisted:
        write(wt / rel)
    tracked = wt / "README.md"
    runner = runner_cls()
    runner.register_saved(str(wt), listed)
    stdin = "\0".join(listed).encode() + b"\0"
    res = runner.run(
        ["xargs", "-0", "git", "clean", "-f", "-x", "--"], cwd=str(wt), stdin=stdin
    )
    assert res.returncode == 0, res.stderr
    for rel in listed:
        assert not (wt / rel).exists(), rel
    for rel in unlisted:
        assert (wt / rel).exists(), (
            rel
        )  # a glob or a bracket in a name matched nothing else
    assert tracked.read_text(encoding="utf-8") == "example\n"
    assert " " in listed[0]  # the file name with a space was part of the case
    # the same call with an unlisted path is refused before any process starts
    with pytest.raises(wc.RefusedCommand):
        runner.run(
            ["xargs", "-0", "git", "clean", "-f", "-x", "--"],
            cwd=str(wt),
            stdin=b"loose.txt\0",
        )
    assert (wt / "loose.txt").exists()


def test_the_facts_tests_use_only_tmp_path(tmp_path, throwaway_repo):
    assert str(throwaway_repo.main).startswith(str(tmp_path))
    top = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=throwaway_repo.main,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert top.startswith(str(tmp_path))
