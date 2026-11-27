"""T-02: the printed ``add_argv`` and ``commit_argv`` have the FR-035 shape and never hold a
token of FR-063, over every planning case.

The argv lists are the words after ``git``. The tests also run them on throwaway
repositories (the agent's own call, with the file written outside the work tree) to show
that a literal path list stages and commits exactly the named paths.
"""

from __future__ import annotations

import importlib
import os

import pytest

from .conftest import git_in

# FR-063, token for token.
FR063_FORBIDDEN = (
    "-A",
    "--all",
    ".",
    "-a",
    "--amend",
    "--no-verify",
    "-n",
    "--force",
    "-f",
    "--allow-empty",
    "-c",
    "--no-edit",
)


@pytest.fixture
def vcs(scripts_dir):
    return importlib.import_module("vcs")


def run_plan(vcs, repo, *paths):
    return vcs.run_stage_plan(str(repo.work), list(paths) if paths else None)


def path_case_plain(repo):
    repo.write("a.txt", "x\n")
    repo.write("b.txt", "x\n")
    return ["a.txt", "b.txt"]


def path_case_magic(repo):
    names = [
        ":(glob)*",
        "-nfile.txt",
        "has space.txt",
        "d/how to merge.md",
        "-A",
        "--all",
    ]
    for name in names:
        repo.write(name, "x\n")
    return names


def path_case_deletion(repo):
    repo.write("gone.txt", "x\n")
    repo.commit("add gone")
    os.remove(repo.work / "gone.txt")
    return ["gone.txt"]


def path_case_with_skips(repo):
    repo.write("a.txt", "x\n")
    repo.write(".dev/implement/run-1/ledger.md", "x\n")
    return ["a.txt", ".dev/implement/run-1/ledger.md", "nope.txt"]


def path_case_many(repo):
    names = [f"m/f{i:03d}.txt" for i in range(230)]
    for name in names:
        repo.write(name, "x\n")
    return names


def path_case_pathless(repo):
    repo.write("one.txt", "1\n")
    repo.write("-n.txt", "2\n")
    repo.git("add", "--", "one.txt", "-n.txt")
    return []


CASES = [
    path_case_plain,
    path_case_magic,
    path_case_deletion,
    path_case_with_skips,
    path_case_many,
    path_case_pathless,
]


@pytest.mark.parametrize("case", CASES, ids=lambda c: c.__name__)
def test_no_planned_argv_holds_an_fr063_token(case, repo, vcs):
    paths = case(repo)
    result = run_plan(vcs, repo, *paths)
    assert result["status"] == "ok"
    for argv in (result["add_argv"], result["commit_argv"]):
        for token in argv:
            assert token not in FR063_FORBIDDEN, argv
            if token.startswith("-"):
                assert token.split("=", 1)[0] not in FR063_FORBIDDEN, argv
    # the agent-argv rule of the runner module agrees
    rules = importlib.import_module("vcs_rules")
    rules.validate_agent_argv(result["add_argv"])
    rules.validate_agent_argv(result["commit_argv"])


@pytest.mark.parametrize("case", CASES[:-1], ids=lambda c: c.__name__)
def test_pathful_argv_has_exactly_the_fr035_shape(case, repo, vcs):
    paths = case(repo)
    result = run_plan(vcs, repo, *paths)
    spec = result["pathspec_file"]["path"]
    assert result["add_argv"] == [
        "--literal-pathspecs",
        "add",
        f"--pathspec-from-file={spec}",
        "--pathspec-file-nul",
    ]
    assert result["commit_argv"] == [
        "--literal-pathspecs",
        "commit",
        "--only",
        "-F",
        result["message_path"],
        f"--pathspec-from-file={spec}",
        "--pathspec-file-nul",
    ]
    # no path is spelled in an argv: the paths travel in the file only
    for name in result["commit_paths"]:
        assert name not in result["add_argv"] + result["commit_argv"]


def test_pathless_argv_is_commit_dash_f_only(repo, vcs):
    path_case_pathless(repo)
    result = run_plan(vcs, repo)
    assert result["add_argv"] == []
    assert result["commit_argv"] == ["commit", "-F", result["message_path"]]
    assert result["pathspec_file"] is None


def test_a_refused_or_empty_plan_prints_no_argv(repo, vcs):
    repo.write("x,y.txt", "x\n")
    refused = run_plan(vcs, repo, "x,y.txt")
    nothing = run_plan(vcs, repo, "README.md")
    for result in (refused, nothing):
        assert result["add_argv"] == [] and result["commit_argv"] == []
        assert result["pathspec_file"] is None and result["message_path"] is None


# --- the argv, run as the agent would run it -------------------------------------------------
def write_files(result, message="subject line\n"):
    with open(result["pathspec_file"]["path"], "w", encoding="utf-8", newline="") as f:
        f.write(result["pathspec_file"]["content"])
    with open(result["message_path"], "w", encoding="utf-8") as f:
        f.write(message)


def cleanup(result):
    for path in (result["pathspec_file"]["path"], result["message_path"]):
        if os.path.exists(path):
            os.remove(path)


def test_the_add_argv_stages_exactly_the_named_literal_paths(repo, vcs):
    names = path_case_magic(repo)
    repo.write("other.txt", "not named\n")
    result = run_plan(vcs, repo, *names)
    write_files(result)
    try:
        git_in(repo.work, *result["add_argv"])
    finally:
        cleanup(result)
    staged = repo.git("diff", "--cached", "--name-only", "-z").rstrip("\0").split("\0")
    assert sorted(staged) == sorted(names)


def test_the_commit_argv_commits_only_the_named_paths(repo, vcs):
    repo.write("named.txt", "named\n")
    repo.write("staged-other.txt", "other\n")
    repo.git("add", "--", "staged-other.txt")
    result = run_plan(vcs, repo, "named.txt")
    write_files(result)
    try:
        # the flow of FR-038: the add argv first, then the commit argv
        git_in(repo.work, *result["add_argv"])
        git_in(repo.work, *result["commit_argv"])
    finally:
        cleanup(result)
    assert repo.git("show", "--name-only", "--format=", "HEAD").split() == ["named.txt"]
    # the person's other staged change stays staged
    assert repo.git("diff", "--cached", "--name-only").split() == ["staged-other.txt"]


def test_the_commit_argv_commits_a_deletion(repo, vcs):
    repo.write("gone.txt", "x\n")
    repo.commit("add gone")
    os.remove(repo.work / "gone.txt")
    result = run_plan(vcs, repo, "gone.txt")
    write_files(result)
    try:
        git_in(repo.work, *result["commit_argv"])
    finally:
        cleanup(result)
    assert repo.git("show", "--name-status", "--format=", "HEAD").split() == [
        "D",
        "gone.txt",
    ]


def test_the_pathless_commit_argv_commits_exactly_the_staged_index(repo, vcs):
    repo.write("part.txt", "v1\n")
    repo.commit("part")
    repo.write("part.txt", "v2\n")
    repo.git("add", "--", "part.txt")
    repo.write("part.txt", "v3\n")  # unstaged edit in a partly staged file
    result = run_plan(vcs, repo)
    with open(result["message_path"], "w", encoding="utf-8") as f:
        f.write("subject line\n")
    try:
        git_in(repo.work, *result["commit_argv"])
    finally:
        if os.path.exists(result["message_path"]):
            os.remove(result["message_path"])
    assert repo.git("show", "HEAD:part.txt") == "v2\n"
    assert (repo.work / "part.txt").read_text(encoding="utf-8") == "v3\n"
