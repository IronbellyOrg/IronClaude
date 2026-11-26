"""T-05: what ``git commit --only`` does with the entries outside the commit set (FR-033,
FR-062).

The design relies on this: after ``git add -- .dev/tasks`` and a commit ``--only`` the commit
set, every other staged entry is still staged and is not in the commit. The tests run it on
real repositories with the argv the helper prints (the FR-035 shape: a NUL-delimited
pathspec file and a message file outside the work tree), once with no hook and once under
the hook emulator, and then ask ``verify`` about the commit made under the full procedure.
"""

from __future__ import annotations

import importlib
import os

import pytest

from .conftest import git_in
from .test_hook_refusal import Flow


@pytest.fixture
def vcs(scripts_dir):
    return importlib.import_module("vcs")


def stage_unrelated(repo):
    """A modification, an addition and a task-folder file, all staged and none in the set."""
    repo.write("other.txt", "unrelated, modified and staged\n")
    repo.write("added.txt", "unrelated, added and staged\n")
    repo.write(".dev/tasks/to-do/other-pkg/note.md", "another package\n")
    repo.git("add", "--", "other.txt", "added.txt")
    repo.git("add", "--", ".dev/tasks")  # FR-062: staging is not committing


def base(repo):
    repo.write("a.txt", "a\n")
    repo.write("gone.txt", "gone\n")
    repo.write("other.txt", "other\n")
    repo.commit("base")
    repo.write("a.txt", "a changed by the task\n")
    os.remove(repo.work / "gone.txt")  # a deletion inside the set


def run_plan(vcs, repo, commit):
    """Write the two files the agent writes, then run the printed add and commit argv."""
    plan = vcs.run_stage_plan(str(repo.work), ["a.txt", "gone.txt"])
    assert plan["status"] == "ok", plan
    files = {
        plan["pathspec_file"]["path"]: plan["pathspec_file"]["content"],
        plan["message_path"]: "feat: the task\n",
    }
    try:
        for path, text in files.items():
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(text)
        git_in(repo.work, *plan["add_argv"])
        return commit(plan)
    finally:
        for path in files:
            if os.path.exists(path):
                os.remove(path)


def check_outcome(repo, before_staged):
    changed = repo.git("show", "--name-only", "--format=", "HEAD").split()
    assert sorted(changed) == ["a.txt", "gone.txt"]  # only the set is in the commit
    staged = repo.git("diff", "--cached", "--name-only").split()
    assert sorted(staged) == sorted(before_staged)  # and the rest is still staged
    for name in before_staged:  # still the same staged content, not committed
        assert repo.git("ls-files", "--stage", "--", name).strip() != ""
    assert (repo.work / "other.txt").read_text(encoding="utf-8").startswith("unrelated")


def test_only_leaves_other_staged_entries_staged_and_out_of_the_commit(repo, vcs):
    base(repo)
    stage_unrelated(repo)
    before = repo.git("diff", "--cached", "--name-only").split()
    assert sorted(before) == [
        ".dev/tasks/to-do/other-pkg/note.md",
        "added.txt",
        "other.txt",
    ]

    run_plan(vcs, repo, lambda plan: git_in(repo.work, *plan["commit_argv"]))

    check_outcome(repo, before)
    assert repo.git("diff", "--cached", "--name-only", "--", ".dev/tasks").split() == [
        ".dev/tasks/to-do/other-pkg/note.md"
    ]


def test_the_same_holds_under_a_hook_that_stashes_and_restores(
    repo, vcs, hook_emulator
):
    base(repo)
    stage_unrelated(repo)
    repo.write("README.md", "person edit\n")  # unstaged: the hook stashes it
    before = repo.git("diff", "--cached", "--name-only").split()

    run_plan(vcs, repo, lambda plan: git_in(repo.work, *plan["commit_argv"]))

    check_outcome(repo, before)
    assert len(hook_emulator.patches()) == 1  # the hook ran and saved the unstaged edit
    assert (repo.work / "README.md").read_text(encoding="utf-8") == "person edit\n"


def test_a_partly_staged_file_in_the_set_commits_its_work_tree_content(repo, vcs):
    """``--only`` takes the whole current content of a named path, staged or not, and
    leaves an unrelated staged path alone; the helper's S therefore names whole files."""
    base(repo)
    repo.write("a.txt", "staged half\n")
    repo.git("add", "--", "a.txt")
    repo.write("a.txt", "staged half\nand an unstaged half\n")
    stage_unrelated(repo)

    run_plan(vcs, repo, lambda plan: git_in(repo.work, *plan["commit_argv"]))

    assert repo.git("show", "HEAD:a.txt") == "staged half\nand an unstaged half\n"
    assert "other.txt" in repo.git("diff", "--cached", "--name-only").split()


def test_verify_proves_the_commit_and_the_staged_entries_are_no_difference(
    repo, vcs, hook_emulator
):
    f = Flow(repo, vcs, hook_emulator)
    repo.write("unrelated.txt", "staged by the person\n")
    repo.git("add", "--", "unrelated.txt")
    f.ready()
    done = f.commit()
    assert done.returncode == 0, done.stderr

    res = f.verify(0)

    assert res["status"] == "committed", res
    assert res["changed_paths"] == ["src/a.py"]
    assert (res["outside"], res["outside_changed"]) == ("unchanged", 0)
    assert repo.git("diff", "--cached", "--name-only").split() == ["unrelated.txt"]
    assert "unrelated.txt" not in repo.git("show", "--name-only", "--format=", "HEAD")
