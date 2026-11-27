"""The hook-manager emulator (FR-118, risk 15): what a stashing hook does to edits outside
the commit set S under ``git commit --only``.

The emulator in ``conftest.py`` replays the command sequence of the pre-commit
framework's ``pre_commit/staged_files_only.py``, version 4.6.2 from PyPI (the revision
checked by the spike in ``test_precommit_spike.py``; ``artifacts/precommit-spike.md``
records that run). The cases here only prove what the emulator does; whether it matches
the real framework is the job of the spike, which skips when ``pre-commit`` is absent.
"""

from __future__ import annotations

PERSON_EDIT = "person edit outside the commit set\n"


def _setup(repo):
    """a.txt is the task file (S); b.txt is a tracked file the person edits."""
    repo.write("a.txt", "a\n")
    repo.write("b.txt", "b\n")
    repo.commit("add a and b")
    repo.write("a.txt", "a changed by the task\n")
    return repo.git("rev-parse", "HEAD").strip()


def _read(repo, name):
    return (repo.work / name).read_text(encoding="utf-8")


def test_success_restores_unstaged_edit_outside_the_commit_set(repo, hook_emulator):
    head = _setup(repo)
    repo.write("b.txt", PERSON_EDIT)

    done = hook_emulator.commit(["a.txt"])

    assert done.returncode == 0, done.stderr
    assert repo.git("rev-parse", "HEAD").strip() != head
    assert repo.git("show", "--name-only", "--format=", "HEAD").split() == ["a.txt"]
    assert _read(repo, "b.txt") == PERSON_EDIT  # restored from the saved patch
    assert repo.git("status", "--porcelain").split() == ["M", "b.txt"]
    assert len(hook_emulator.patches()) == 1  # the framework keeps its patch file


def test_sigkill_during_the_hook_leaves_the_edit_only_in_the_saved_patch(
    repo, hook_emulator
):
    head = _setup(repo)
    repo.write("b.txt", PERSON_EDIT)

    proc = hook_emulator.start_blocked_commit(["a.txt"])
    hook_emulator.kill_group(proc)

    assert repo.git("rev-parse", "HEAD").strip() == head
    assert _read(repo, "b.txt") == "b\n"  # the edit is gone from the work tree
    (patch,) = hook_emulator.patches()
    assert PERSON_EDIT.strip() in patch.read_text(encoding="utf-8")
    assert repo.git("stash", "list").strip() == ""  # and no stash entry holds it


def test_edit_to_an_assume_unchanged_file_is_overwritten_without_a_kill(
    repo, hook_emulator
):
    """The diff step cannot see the edit (the flag hides it), but the checkout step runs
    as soon as any other unstaged change exists (here c.txt) and rewrites the file from
    the index. Nothing is saved for it and no kill is needed."""
    repo.write("c.txt", "c\n")
    _setup(repo)  # commits c.txt with a.txt and b.txt, then edits a.txt
    repo.git("update-index", "--assume-unchanged", "b.txt")
    repo.write("b.txt", PERSON_EDIT)
    repo.write("c.txt", "visible unstaged edit\n")

    done = hook_emulator.commit(["a.txt"])

    assert done.returncode == 0, done.stderr
    assert _read(repo, "b.txt") == "b\n"  # overwritten, with no patch holding it
    assert _read(repo, "c.txt") == "visible unstaged edit\n"  # saved and restored
    (patch,) = hook_emulator.patches()
    assert PERSON_EDIT.strip() not in patch.read_text(encoding="utf-8")


def test_an_assume_unchanged_edit_alone_is_left_alone(repo, hook_emulator):
    """With no other unstaged change the framework skips its checkout, so the hidden edit
    survives. Observed with git 2.47.3; other git versions are UNVERIFIED."""
    _setup(repo)
    repo.git("update-index", "--assume-unchanged", "b.txt")
    repo.write("b.txt", PERSON_EDIT)

    done = hook_emulator.commit(["a.txt"])

    assert done.returncode == 0, done.stderr
    assert _read(repo, "b.txt") == PERSON_EDIT
    assert hook_emulator.patches() == []


def test_a_hook_that_exits_1_leaves_head_unchanged_and_restores_the_edit(
    repo, hook_emulator
):
    head = _setup(repo)
    repo.write("b.txt", PERSON_EDIT)
    hook_emulator.set_action("exit1")

    done = hook_emulator.commit(["a.txt"])

    assert done.returncode == 1
    assert repo.git("rev-parse", "HEAD").strip() == head
    assert _read(repo, "b.txt") == PERSON_EDIT
    assert _read(repo, "a.txt") == "a changed by the task\n"


def test_a_hook_that_rewrites_a_commit_set_file_and_exits_1_commits_nothing(
    repo, hook_emulator
):
    head = _setup(repo)
    hook_emulator.set_action("rewrite_exit1", "a.txt")

    done = hook_emulator.commit(["a.txt"])

    assert done.returncode == 1
    assert repo.git("rev-parse", "HEAD").strip() == head
    assert _read(repo, "a.txt").endswith("rewritten-by-hook\n")


def test_a_hook_that_rewrites_and_stages_the_file_commits_the_rewrite(
    repo, hook_emulator
):
    _setup(repo)
    repo.write("b.txt", PERSON_EDIT)
    hook_emulator.set_action("rewrite_add", "a.txt")

    done = hook_emulator.commit(["a.txt"])

    assert done.returncode == 0, done.stderr
    assert repo.git("show", "HEAD:a.txt").endswith("rewritten-by-hook\n")
    assert _read(repo, "b.txt") == PERSON_EDIT
