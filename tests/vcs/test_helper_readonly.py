"""Tests for GitRunner in vcs_plan.py: the one read-only seam through which the helper runs git (T-03).

Real git runs only on the throwaway repositories of the ``repo`` fixture. The
``--no-optional-locks`` and ``core.fsmonitor`` prefix, the allow-list check, the
scratch child environment and the private index are the properties checked here.
"""

from __future__ import annotations

import importlib
import re
import subprocess
from pathlib import Path

import pytest

from .conftest import git_in

PLAN_FILE = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/skills/sc-git-protocol/scripts/vcs_plan.py"
)
PREFIX = ["git", "--no-optional-locks", "-c", "core.fsmonitor=false"]
# The pattern of tests/skills/test_worker_contract.py (WRITE_VERB_RE), copied so a
# phrase it would flag is caught here first.
WRITE_VERB_RE = re.compile(
    r"\b(?:git(?:\s+-C\s+\S+)?\s+(?:add|commit|push|merge|stash|update-ref|worktree\s+(?:add|remove))"
    r"|gh\s+(?:pr|api))(?![\w-])"
)


@pytest.fixture
def mods(scripts_dir):
    return (importlib.import_module("vcs_plan"), importlib.import_module("vcs_rules"))


@pytest.fixture
def plan(mods):
    return mods[0]


@pytest.fixture
def spy(plan, monkeypatch):
    """Replace subprocess.run inside the module under test; records each call."""
    calls = []

    def fake(cmd, **kw):
        calls.append((list(cmd), kw))
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(plan.subprocess, "run", fake)
    return calls


def test_every_argv_carries_the_prefix(plan, repo):
    runner = plan.GitRunner(repo.work, record=True)
    runner.run(["rev-parse", "--show-toplevel"])
    runner.run(["status", "--porcelain=v2"])
    runner.run(["diff", "--name-only"])
    runner.run(["--version"])
    runner.run(["ls-files", "-z"], directory=".")
    assert len(runner.calls) == 5
    for cmd in runner.calls:
        assert cmd[:4] == PREFIX
    assert runner.calls[4][4:6] == ["-C", "."]


def test_recording_mode_without_execution(plan, repo, spy):
    runner = plan.GitRunner(repo.work, record=True, dry_run=True)
    assert runner.run(["rev-parse", "HEAD"]) == (0, "")
    assert runner.calls == [[*PREFIX, "rev-parse", "HEAD"]]
    assert spy == []


@pytest.mark.parametrize(
    "argv",
    [
        ["branch", "-D", "x"],
        ["config", "--unset", "core.hooksPath"],
        ["update-ref", "refs/heads/x", "HEAD"],
        ["hash-object", "-w", "--stdin"],
        ["commit", "-m", "x"],
    ],
)
def test_forbidden_argv_raises_before_any_process(plan, mods, repo, spy, argv):
    runner = plan.GitRunner(repo.work, record=True)
    with pytest.raises(mods[1].ForbiddenArgv):
        runner.run(argv)
    assert spy == []
    assert runner.calls == []


@pytest.mark.parametrize("argv", [["read-tree", "HEAD"], ["add", "-A"], ["write-tree"]])
def test_private_index_verbs_refuse_without_an_index(plan, mods, repo, spy, argv):
    with pytest.raises(mods[1].ForbiddenArgv):
        plan.GitRunner(repo.work).run(argv)
    assert spy == []


def test_an_index_file_the_runner_did_not_create_is_refused(plan, mods, repo, spy):
    runner = plan.GitRunner(repo.work)
    with pytest.raises(mods[1].ForbiddenArgv):
        runner.run(["write-tree"], index_file=str(repo.work / ".git" / "index"))
    with pytest.raises(mods[1].ForbiddenArgv):
        runner.run(["write-tree"], index_file="/tmp/not-made-by-the-runner")
    assert spy == []


def test_child_environment_is_built_from_scratch(plan, repo, spy, monkeypatch):
    monkeypatch.setenv("GIT_INDEX_FILE", str(repo.work / ".git" / "index"))
    monkeypatch.setenv("GIT_DIR", str(repo.work / ".git"))
    monkeypatch.setenv("GIT_SSH_COMMAND", "evil")
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    plan.GitRunner(repo.work).run(["rev-parse", "HEAD"])
    ((_, kw),) = spy
    env = kw["env"]
    assert env["GIT_TERMINAL_PROMPT"] == "0"
    assert {k for k in env if k.startswith("GIT_")} == {"GIT_TERMINAL_PROMPT"}
    assert env["PATH"] == "/usr/bin:/bin"
    assert kw["timeout"] == 10
    assert kw["cwd"] == str(repo.work)
    assert kw["stdin"] is subprocess.DEVNULL


def test_private_index_is_set_only_for_its_own_file(plan, repo, spy):
    runner = plan.GitRunner(repo.work, timeout=3)
    with runner.private_index() as idx:
        assert ".git" not in Path(idx).parts
        runner.run(["read-tree", "HEAD"], index_file=idx)
        assert spy[-1][1]["env"]["GIT_INDEX_FILE"] == idx
        assert spy[-1][1]["timeout"] == 3
        runner.run(["rev-parse", "HEAD"])
        assert "GIT_INDEX_FILE" not in spy[-1][1]["env"]
    assert not Path(idx).parent.exists()


def test_inherited_index_is_ignored_and_the_persons_index_is_unchanged(
    plan, repo, monkeypatch
):
    person_index = repo.work / ".git" / "index"
    monkeypatch.setenv("GIT_INDEX_FILE", str(person_index))
    repo.write("new.txt", "fresh\n")
    before = person_index.read_bytes()
    head_tree = repo.git("rev-parse", "HEAD^{tree}").strip()
    runner = plan.GitRunner(repo.work)

    rc, out = runner.run(["status", "--porcelain"])
    assert rc == 0 and "?? new.txt" in out

    with runner.private_index() as idx:
        assert runner.run(["read-tree", "HEAD"], index_file=idx)[0] == 0
        assert runner.run(["add", "-A"], index_file=idx)[0] == 0
        rc, tree = runner.run(["write-tree"], index_file=idx)
    assert rc == 0
    tree = tree.strip()
    assert tree != head_tree
    listing = git_in(repo.work, "ls-tree", "-r", "--name-only", tree)
    assert "new.txt" in listing.split()
    assert person_index.read_bytes() == before
    assert "?? new.txt" in git_in(repo.work, "status", "--porcelain")


def test_is_ancestor_rc_1_and_rc_128_stay_apart(plan, repo):
    first = repo.git("rev-parse", "HEAD").strip()
    repo.write("b.txt", "b\n")
    second = repo.commit("second")
    runner = plan.GitRunner(repo.work)
    assert runner.run(["merge-base", "--is-ancestor", first, second])[0] == 0
    assert runner.run(["merge-base", "--is-ancestor", second, first])[0] == 1
    rc, _ = runner.run(["merge-base", "--is-ancestor", "0" * 40, second])
    assert rc == 128


def test_ignore_submodules_is_added_to_implement_side_status_and_diff(plan, repo):
    runner = plan.GitRunner(repo.work, record=True)
    runner.run(["status", "--porcelain"])
    runner.run(["diff", "--name-only", "--", "a.py"])
    runner.run(["status", "--ignore-submodules=all"])
    runner.run(["rev-parse", "HEAD"])
    runner.run(["submodule", "status"])
    tails = [c[4:] for c in runner.calls]
    assert tails[0] == ["status", "--ignore-submodules=all", "--porcelain"]
    assert tails[1] == ["diff", "--ignore-submodules=all", "--name-only", "--", "a.py"]
    assert tails[2] == ["status", "--ignore-submodules=all"]
    assert tails[3] == ["rev-parse", "HEAD"]
    assert tails[4] == ["submodule", "status"]


def test_only_person_invoked_status_may_see_submodules(plan, mods, repo):
    rules = mods[1]
    implement = plan.GitRunner(repo.work, record=True)
    with pytest.raises(rules.ForbiddenArgv):
        implement.run(["status", "--ignore-submodules=none"])
    with pytest.raises(rules.ForbiddenArgv):
        implement.run(["diff", "--ignore-submodules=dirty"])
    person = plan.GitRunner(repo.work, record=True, person_invoked=True)
    person.run(["status", "--porcelain=v2", "--ignore-submodules=none"])
    assert person.calls[0][4:] == [
        "status",
        "--porcelain=v2",
        "--ignore-submodules=none",
    ]
    with pytest.raises(rules.ForbiddenArgv):
        person.run(["diff", "--ignore-submodules=none"])
    # A person-invoked status without the option reports submodules (the option is
    # added as "none", not "all").
    person.run(["status", "--porcelain"])
    assert person.calls[1][4:6] == ["status", "--ignore-submodules=none"]


def test_a_timeout_is_a_named_sentinel_not_an_exit_code_of_git(plan, repo, monkeypatch):
    def boom(cmd, **kw):
        raise subprocess.TimeoutExpired(cmd, kw["timeout"])

    monkeypatch.setattr(plan.subprocess, "run", boom)
    runner = plan.GitRunner(repo.work, timeout=1)
    assert runner.run(["rev-parse", "HEAD"]) == (plan.TIMEOUT_RC, "")
    assert plan.TIMEOUT_RC not in (0, 1, 128)


def test_stderr_of_the_last_call_is_kept(plan, repo):
    runner = plan.GitRunner(repo.work)
    rc, _ = runner.run(["merge-base", "--is-ancestor", "0" * 40, "HEAD"])
    assert rc == 128 and runner.last_stderr


def test_file_has_no_write_verb_phrase_and_no_source_tree_path():
    text = PLAN_FILE.read_text(encoding="utf-8")
    hits = [ln for ln in text.splitlines() if WRITE_VERB_RE.search(ln)]
    assert hits == []
    assert "src/superclaude/" not in text
