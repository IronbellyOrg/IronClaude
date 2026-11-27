"""Tests for vcs_rules.py: the safety constants and the argv allow-list table.

The 2.25 value of MIN_GIT is UNVERIFIED until the preflight task tests it on a real git.
"""

from __future__ import annotations

import importlib
import re
from pathlib import Path

import pytest

RULES_FILE = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/skills/sc-git-protocol/scripts/vcs_rules.py"
)


@pytest.fixture
def rules(scripts_dir):
    return importlib.import_module("vcs_rules")


def test_constants_equal_fr_030_and_fr_013(rules):
    assert rules.PROTECTED_BRANCHES == ("master", "main", "integration")
    assert rules.DEV_MIRROR_ALLOW == ("settings.json",)
    assert rules.FORBIDDEN_FLAGS == (
        "--no-verify",
        "-n",
        "--amend",
        "--force",
        "-f",
        "-D",
        "--delete",
        "-A",
        "--all",
        ".",
        "-a",
        "--allow-empty",
        "--no-edit",
        "--remote",
        "--recurse-submodules=on-demand",
        "--discard-changes",
    )
    assert rules.MIN_GIT == (2, 25)


@pytest.mark.parametrize(
    "argv",
    [
        ["rev-parse", "--show-toplevel"],
        ["rev-parse", "--verify", "--quiet", "HEAD^{commit}"],
        ["symbolic-ref", "--short", "-q", "HEAD"],
        ["symbolic-ref", "refs/remotes/origin/HEAD"],
        ["status", "--porcelain=v2", "-z", "--ignore-submodules=all"],
        ["status", "--porcelain=v2", "--ignore-submodules=none", "--branch"],
        ["diff", "--name-only", "-z", "--cached", "--ignore-submodules=all"],
        ["diff", "--exit-code", "--quiet", "HEAD", "--", "src/a.py"],
        ["ls-files", "-z", "--others", "--exclude-standard"],
        ["ls-tree", "HEAD", "--", "libs/lib"],
        ["cat-file", "-e", "abc^{commit}"],
        ["check-ignore", "-q", "--", "a.log"],
        ["config", "--get", "core.hooksPath"],
        ["config", "--get-regexp", r"^filter\."],
        ["config", "--file", ".gitmodules", "-z", "--get-regexp", r"^submodule\."],
        ["submodule", "status"],
        ["submodule", "status", "--cached", "--", "libs/lib"],
        ["for-each-ref", "--contains", "abc", "refs/heads", "refs/remotes"],
        ["for-each-ref", "--format=%(refname)", "refs/heads"],
        ["rev-list", "--count", "HEAD"],
        ["log", "--format=%H", "-n", "3"],
        ["merge-base", "--is-ancestor", "abc", "def"],
        ["branch", "--show-current"],
        ["hash-object", "--stdin"],
        ["version"],
        ["--version"],
    ],
)
def test_validate_argv_accepts_read_forms(rules, argv):
    rules.validate_argv(argv)


@pytest.mark.parametrize(
    "argv",
    [
        ["read-tree", "--empty"],
        ["read-tree", "HEAD"],
        ["add", "-A"],
        ["add", "--pathspec-from-file=/tmp/paths", "--pathspec-file-nul"],
        ["write-tree"],
    ],
)
def test_validate_argv_accepts_private_index_forms(rules, argv, tmp_path):
    rules.validate_argv(argv, index_file=str(tmp_path / "idx"))


@pytest.mark.parametrize(
    "argv",
    [
        ["branch", "-D", "feature/x"],
        ["branch", "feature/new"],
        ["branch", "--show-current", "extra"],
        ["config", "--unset", "core.hooksPath"],
        ["config", "core.hooksPath", "x"],
        ["config", "--get", "--add", "a.b"],
        ["config", "--file", ".gitmodules", "submodule.lib.url", "x"],
        ["config", "--file", ".gitmodules", "--unset", "submodule.lib.url"],
        ["update-ref", "refs/heads/x", "abc"],
        ["hash-object", "-w", "--stdin"],
        ["symbolic-ref", "HEAD", "refs/heads/x"],
        ["symbolic-ref", "--delete", "HEAD"],
        ["merge-base", "HEAD", "origin/main"],
        ["submodule", "update"],
        ["submodule", "status", "--recursive"],
        ["diff", "--output=/tmp/out"],
        ["log", "--output=/tmp/out"],
        ["version", "--build-options"],
        ["--version", "--build-options"],
        ["--version", "x"],
        ["--exec-path"],
        ["-c", "core.fsmonitor=true", "status"],
        ["commit", "-m", "x"],
        ["push"],
        ["checkout", "--", "."],
        ["reset", "--hard"],
        ["stash"],
        [],
    ],
)
def test_validate_argv_refuses_writes_and_unknown_options(rules, argv):
    with pytest.raises(rules.ForbiddenArgv):
        rules.validate_argv(argv)


@pytest.mark.parametrize("verb", ["read-tree", "add", "write-tree"])
def test_private_index_verbs_refuse_without_private_index(rules, verb):
    argv = (
        [verb]
        if verb == "write-tree"
        else [verb, "-A"]
        if verb == "add"
        else [verb, "HEAD"]
    )
    with pytest.raises(rules.ForbiddenArgv):
        rules.validate_argv(argv)
    with pytest.raises(rules.ForbiddenArgv):
        rules.validate_argv(argv, index_file=None)


def test_private_index_must_be_outside_dot_git(rules, tmp_path):
    for bad in (str(tmp_path / ".git" / "index"), ".git/index", "repo/.git/x/index"):
        with pytest.raises(rules.ForbiddenArgv):
            rules.validate_argv(["write-tree"], index_file=bad)
    rules.validate_argv(["write-tree"], index_file=str(tmp_path / "private-index"))


def test_private_index_does_not_unlock_other_write_options(rules, tmp_path):
    idx = str(tmp_path / "idx")
    with pytest.raises(rules.ForbiddenArgv):
        rules.validate_argv(["read-tree", "-u", "HEAD"], index_file=idx)
    with pytest.raises(rules.ForbiddenArgv):
        rules.validate_argv(["add", "--force", "x"], index_file=idx)
    with pytest.raises(rules.ForbiddenArgv):
        rules.validate_argv(["commit", "-m", "x"], index_file=idx)


def test_read_verbs_do_not_need_an_index(rules, tmp_path):
    rules.validate_argv(["status", "--porcelain"], index_file=str(tmp_path / "idx"))


def test_agent_argv_refuses_every_forbidden_flag(rules):
    for flag in rules.FORBIDDEN_FLAGS:
        with pytest.raises(rules.ForbiddenArgv):
            rules.validate_agent_argv(["add", flag, "--", "a.py"])
        with pytest.raises(rules.ForbiddenArgv):
            rules.validate_agent_argv(["commit", flag, "-F", "/tmp/m"])


def test_agent_argv_refuses_dash_a_for_add_and_dot_pathspec(rules):
    with pytest.raises(rules.ForbiddenArgv):
        rules.validate_agent_argv(["add", "-A"])
    with pytest.raises(rules.ForbiddenArgv):
        rules.validate_agent_argv(["add", "--", "."])
    with pytest.raises(rules.ForbiddenArgv):
        rules.validate_agent_argv(["commit", "-am", "x"])


def test_agent_argv_accepts_the_normal_commit_and_add_forms(rules):
    rules.validate_agent_argv(
        ["add", "--pathspec-from-file=/tmp/p", "--pathspec-file-nul"]
    )
    rules.validate_agent_argv(["add", "--", "src/a.py", "docs/b.md"])
    rules.validate_agent_argv(
        ["commit", "--only", "-F", "/tmp/msg", "--pathspec-from-file=/tmp/p"]
    )
    # a message or file value that looks like a flag is a value, not a flag
    rules.validate_agent_argv(["commit", "-m", "-n is not used", "--", "a.py"])


def test_agent_argv_checks_flag_name_before_equals(rules):
    with pytest.raises(rules.ForbiddenArgv):
        rules.validate_agent_argv(["add", "--force=yes"])


def test_rules_file_has_no_install_path_and_no_write_verb_phrase(rules):
    text = RULES_FILE.read_text(encoding="utf-8")
    assert "src/superclaude" not in text
    write_verb = re.compile(
        r"\b(?:git(?:\s+-C\s+\S+)?\s+(?:add|commit|push|merge|stash|update-ref"
        r"|worktree\s+(?:add|remove))|gh\s+(?:pr|api))(?![\w-])"
    )
    assert write_verb.search(text) is None
    assert "UNVERIFIED" in text
