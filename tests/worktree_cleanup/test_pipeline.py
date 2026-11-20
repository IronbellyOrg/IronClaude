"""The removal pipeline end to end, through the verbs (Task 13).

Every case runs ``main`` on a throwaway repository under ``tmp_path`` with a local bare
repository standing in for the evidence repo and canned ``gh`` and ``orca`` replies. Nothing
here touches a real worktree, a real Orca terminal or the real evidence repo.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from .conftest import git_in, make_fake_proc
from .test_archive import git_identity  # noqa: F401 - autouse: the evidence commit needs an identity
from .test_facts import write
from .test_verbs import World


@pytest.fixture
def world(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path):
    return World(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path)


def open_terminals(wc, world, name, count=2, on_close=None, close_reply=None):
    """Orca lists ``name`` with live terminals; ``on_close`` runs when the terminals are closed."""
    world.listed = {name}
    path = world.paths[name]

    def orca(argv, cwd):
        key = tuple(argv[1:3])
        if key == ("worktree", "ps"):
            rows = [{"worktreeId": f"id-{name}", "path": str(path), "isPinned": False,
                     "liveTerminalCount": count, "lastActivityAt": None, "linkedPR": None, "comment": ""}]  # fmt: skip
            return wc.Result(
                0, json.dumps({"ok": True, "result": {"worktrees": rows}}), ""
            )
        if key == ("terminal", "close"):
            if on_close is not None:
                on_close()
            return close_reply or wc.Result(0, "", "")
        return World.orca(world, argv, cwd)

    world.runner.replies["orca"] = orca


def position(world, predicate):
    for i, c in enumerate(world.runner.commands):
        if predicate(c.argv):
            return i
    return None


def cleared(world):
    return any(c.argv[:2] == ["xargs", "-0"] for c in world.runner.commands)


def closed_terminals(world):
    return any(
        c.argv[:3] == ["orca", "terminal", "close"] for c in world.runner.commands
    )


# -- decision 3: terminals open and a process inside ---------------------------------------------------------------


def test_terminals_and_a_process_inside_are_closed_first_and_the_second_check_runs(
    wc, world, tmp_path, capsys
):
    world.add("done")
    path = world.paths["done"]
    proc = make_fake_proc(tmp_path / "proc-busy", {42: str(path)})
    world.proc = str(proc)
    open_terminals(
        wc, world, "done", on_close=lambda: os.rename(proc / "42", tmp_path / "exited")
    )  # closing the terminals ends the process
    # a dry run says what would happen and closes nothing
    assert world.run("prune") == 0
    assert "its Orca terminals will be closed first" in capsys.readouterr().out
    assert not closed_terminals(world) and path.exists()
    # under --apply the close comes first, then the second check, then the clear, then the removal
    assert world.run("prune", "--apply") == 0
    assert not path.exists()
    close = position(world, lambda a: a[:3] == ["orca", "terminal", "close"])
    assert world.runner.commands[close].argv[3:] == [
        "--worktree",
        "id:id-done",
        "--all",
    ]
    status = position(world, lambda a: "status" in a and a[0] == "git")
    last_status = max(
        i
        for i, c in enumerate(world.runner.commands)
        if "status" in c.argv and c.argv[0] == "git"
    )
    clear = position(world, lambda a: a[:2] == ["xargs", "-0"])
    removal = position(world, lambda a: a[:3] == ["orca", "worktree", "rm"])
    assert status is not None and close < last_status < clear < removal


@pytest.mark.parametrize(
    "reply", [(0, '{"unverifiable": true}'), (1, ""), (0, "closed, UNVERIFIABLE")]
)
def test_a_terminal_close_that_is_unverifiable_or_fails_keeps_the_worktree(
    wc, world, reply
):
    world.add("done")
    path = world.paths["done"]
    open_terminals(wc, world, "done", close_reply=wc.Result(reply[0], reply[1], ""))
    assert world.run("prune", "--apply") == 69
    assert path.exists() and (path / ".dev" / "tasks" / "note.md").exists()
    assert not cleared(world)
    assert not any(c.argv[1:3] == ["worktree", "remove"] for c in world.runner.commands)


def test_a_process_still_inside_after_the_close_keeps_the_worktree(
    wc, world, tmp_path, capsys
):
    world.add("done")
    path = world.paths["done"]
    world.proc = str(make_fake_proc(tmp_path / "proc-stuck", {42: str(path)}))
    open_terminals(wc, world, "done")  # the close succeeds, the process does not end
    assert world.run("prune", "--apply") == 0
    assert (
        "a process is still inside after its Orca terminals were closed"
        in capsys.readouterr().out
    )
    assert closed_terminals(world) and path.exists() and not cleared(world)


def _new_commit(path):
    git_in(path, "commit", "--allow-empty", "-q", "-m", "late")


def _tracked_edit(path):
    (path / "README.md").write_text("edited meanwhile\n", encoding="utf-8")


def _untracked_outside_dev(path):
    write(path / "stray-notes.txt")


@pytest.mark.parametrize(
    "change", [_new_commit, _tracked_edit, _untracked_outside_dev],
    ids=["new commit", "tracked edit", "untracked file outside .dev"],
)  # fmt: skip
def test_a_change_between_the_save_and_the_close_keeps_the_worktree(
    wc, world, capsys, change
):
    world.add("done")
    path = world.paths["done"]
    open_terminals(wc, world, "done", on_close=lambda: change(path))
    assert world.run("prune", "--apply") == 0
    assert "changed since the terminals were closed" in capsys.readouterr().out
    assert path.exists() and (path / ".dev" / "tasks" / "note.md").exists()
    assert not cleared(world)
    assert not any(c.argv[1:3] == ["worktree", "rm"] for c in world.runner.commands)


# -- decision 2: no save of tracked edits or later commits ----------------------------------------------------------


def test_a_merged_worktree_with_a_tracked_edit_is_kept_and_nothing_is_done(
    world, capsys
):
    path = world.add("edited")
    _tracked_edit(path)
    assert world.run("prune", "--apply") == 0
    assert "changed tracked file" in capsys.readouterr().out
    assert path.exists() and (path / ".dev" / "tasks" / "note.md").exists()
    assert not cleared(world) and not closed_terminals(world)
    assert not Path(world.clone).exists()  # nothing was archived by prune
    assert not any("push" in c.argv for c in world.runner.commands)


def test_a_merged_worktree_with_a_commit_after_the_pull_request_is_kept_and_nothing_is_done(
    wc, world, capsys
):
    path = world.add("later")
    merged_head = world.head("later")
    _new_commit(path)

    def stale_pull_request(argv):  # the pull request ended at the earlier commit
        rows = [{"number": 700, "state": "MERGED", "headRefOid": merged_head,
                 "headRefName": "later", "author": {"login": "example-user"},
                 "mergedAt": "2026-11-10T12:00:00Z", "title": "t", "body": "",
                 "closingIssuesReferences": []}]  # fmt: skip
        return wc.Result(0, json.dumps(rows), "")

    world.gh_override[("pr", "list")] = stale_pull_request
    assert world.run("prune", "--apply") == 0
    row = next(ln for ln in capsys.readouterr().out.splitlines() if "| later |" in ln)
    assert row.endswith("| kept | 1 commit after the pull request |")
    assert path.exists() and (path / ".dev" / "tasks" / "note.md").exists()
    assert not cleared(world) and not closed_terminals(world)
    assert not Path(world.clone).exists()
    assert not any("push" in c.argv for c in world.runner.commands)


# -- the branch ---------------------------------------------------------------------------------------------------------


def test_the_branch_is_removed_with_d_and_a_squash_merge_refusal_reports_kept(
    world, capsys
):
    world.add("done")
    squashed = world.add("squashed")
    write(squashed / "feature.txt")
    git_in(squashed, "add", "feature.txt")
    git_in(squashed, "commit", "-q", "-m", "work that main never received")
    assert world.run("prune", "--apply") == 0
    shown = capsys.readouterr().out
    assert not world.paths["done"].exists() and not squashed.exists()
    branch_commands = [c.argv for c in world.runner.commands if "branch" in c.argv]
    assert branch_commands and all("-D" not in a for a in branch_commands)
    assert git_in(world.repo.main, "branch", "--list", "done").strip() == ""
    # git refuses -d after a squash merge: the branch stays and that is not an error
    assert "squashed" in git_in(world.repo.main, "branch", "--list", "squashed")
    assert "failed 0" in shown
    rows = {ln.split(" | ")[1]: ln for ln in shown.splitlines() if ln.startswith("| ")}
    assert rows["squashed"].endswith(
        "| removed | branch kept (not fully merged, as after a squash merge) |"
    )
    assert rows["done"].endswith("| removed | branch removed |")


# -- a second run, two runs, folders that are not worktrees ----------------------------------------------------------------


def test_a_second_run_finds_nothing_more_to_do(world, capsys):
    world.add("done")
    assert world.run("prune", "--apply") == 0
    capsys.readouterr()
    assert world.run("prune", "--apply") == 0
    assert "nothing more to do" in capsys.readouterr().out
    assert world.removal_commands() == []


def test_two_runs_at_once_do_not_both_remove_the_same_worktree(wc, world, capsys):
    world.add("done")
    first = wc.RepoLocks(world.out)  # the run that is already removing
    assert first.acquire(str(world.repo.main)) is True
    try:
        assert world.run("prune", "--apply") == 0
        pruned = capsys.readouterr().out
        assert world.run("retire", "done", "--apply") == 64  # it was not removed
        retired = capsys.readouterr().out
    finally:
        first.release_all()
    assert "another run holds the lock" in pruned
    assert "another run holds the lock" in retired
    # a worktree skipped because of the lock is work left to do, not "nothing more to do"
    assert "nothing more to do" not in pruned
    assert world.paths["done"].exists() and world.removal_commands() == []


def test_folders_that_are_not_worktrees_of_our_repos_never_appear_and_are_never_touched(
    world, capsys
):
    world.add("done")
    wts = world.repo.root / "wts"
    strays = [wts / "plain-folder", wts / "orca-port-3000", wts / "coder-orca-port"]
    for stray in strays:
        stray.mkdir()
        write(stray / "keep.txt")
    assert world.run("prune", "--apply") == 0
    shown = capsys.readouterr().out
    for stray in strays:
        assert stray.name not in shown
        assert (stray / "keep.txt").exists()


# -- decision 1: exactly the saved paths are cleared --------------------------------------------------------------------------


def test_exactly_the_listed_paths_are_cleared_and_nothing_else(
    wc, runner_cls, throwaway_repo, tmp_path
):
    path = throwaway_repo.add_worktree("topic")
    listed = ".dev/tasks/a b.md"  # a name with a space
    for rel in (listed, ".dev/tasks/unlisted.md", ".dev/local/unlisted-ignored.log"):
        write(path / rel)
    runner = runner_cls(evidence_dir=str(tmp_path / "evidence"))
    runner.register_saved(str(path), [listed])
    stdin = listed.encode() + b"\0"
    done = runner.run(
        ["xargs", "-0", "git", "clean", "-f", "-x", "--"], cwd=str(path), stdin=stdin
    )
    assert done.returncode == 0, done.stderr
    assert not (path / listed).exists()
    assert (
        path / ".dev" / "tasks" / "unlisted.md"
    ).exists()  # an untracked file not listed
    assert (
        path / ".dev" / "local" / "unlisted-ignored.log"
    ).exists()  # an ignored file not listed
    assert (path / "README.md").exists()  # a tracked file
    # a path that is not in the saved list is refused before any process starts
    with pytest.raises(wc.RefusedCommand):
        runner.run(
            ["xargs", "-0", "git", "clean", "-f", "-x", "--"],
            cwd=str(path),
            stdin=b".dev/tasks/unlisted.md\0",
        )
    assert (path / ".dev" / "tasks" / "unlisted.md").exists()


# -- the facts the design leans on, on throwaway repositories only ----------------------------------------------------------


def test_git_worktree_remove_without_force_refuses_dirty_and_removes_ignored_only(
    throwaway_repo,
):
    repo = throwaway_repo
    untracked = repo.add_worktree("untracked")
    write(untracked / "new.txt")
    edited = repo.add_worktree("edited")
    (edited / "README.md").write_text("edited\n", encoding="utf-8")
    ignored = repo.add_worktree("ignored")
    write(ignored / ".venv" / "lib" / "x.py")
    for path in (untracked, edited):
        with pytest.raises(subprocess.CalledProcessError):
            git_in(repo.main, "worktree", "remove", str(path))
        assert path.exists()
    git_in(repo.main, "worktree", "remove", str(ignored))
    assert not ignored.exists()


def test_git_branch_d_refuses_after_a_squash_merge(throwaway_repo):
    repo = throwaway_repo
    path = repo.add_worktree("topic")
    write(path / "feature.txt")
    git_in(path, "add", "feature.txt")
    git_in(path, "commit", "-q", "-m", "work")
    git_in(repo.main, "worktree", "remove", str(path))
    with pytest.raises(subprocess.CalledProcessError) as refused:
        git_in(repo.main, "branch", "-d", "topic")
    assert "not fully merged" in refused.value.stderr
