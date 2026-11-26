"""Tests for the submodule rows of ``vcs_submodules.py`` (T-07): the fact rows, the derived
``state`` of every row, the ``update`` and ``commit_pointer`` eligibility objects and the
``submodules`` verb of ``vcs.py``.

Real git runs only on the throwaway repositories of the ``submodule_repo`` and ``repo``
fixtures; the submodule is a ``file://`` clone of a local folder. Whether the ``file://``
tests also pass on CI is UNVERIFIED (the fixture sets ``protocol.file.allow`` only inside
its own repositories).
"""

from __future__ import annotations

import importlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from .conftest import SCRIPTS, git_in, sub_url

MODULE_FILE = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/skills/sc-git-protocol/scripts/vcs_submodules.py"
)
PREFIX = ["git", "--no-optional-locks", "-c", "core.fsmonitor=false"]
# The pattern of tests/skills/test_worker_contract.py (WRITE_VERB_RE), copied so a
# phrase it would flag is caught here first.
WRITE_VERB_RE = re.compile(
    r"\b(?:git(?:\s+-C\s+\S+)?\s+(?:add|commit|push|merge|stash|update-ref|worktree\s+(?:add|remove))"
    r"|gh\s+(?:pr|api))(?![\w-])"
)
SUB = "libs/lib"


@pytest.fixture
def mods(scripts_dir):
    return (
        importlib.import_module("vcs_submodules"),
        importlib.import_module("vcs_plan"),
        importlib.import_module("vcs_rules"),
    )


@pytest.fixture
def facts(mods):
    """Collect the facts of a repository with a person-invoked runner."""
    sm, plan, _ = mods

    def collect(repo, **kw):
        return sm.collect_submodules(
            plan.GitRunner(repo.work, person_invoked=True, **kw)
        )

    return collect


def row_of(result, path=SUB):
    return next(r for r in result["rows"] if r["path"] == path)


def sub_git(repo, *args, **kw):
    return git_in(repo.work / SUB, *args, **kw)


def test_no_submodules_gives_an_empty_list(facts, repo):
    result = facts(repo)
    assert result["rows"] == []
    assert result["superproject"]["branch"] == "main"
    assert result["superproject"]["head"] == repo.git("rev-parse", "HEAD").strip()
    assert result["warnings"] == []


def test_clean_submodule_row(facts, submodule_repo):
    row = row_of(facts(submodule_repo))
    head = sub_git(submodule_repo, "rev-parse", "HEAD").strip()
    assert row["gitlink"] == head
    assert row["head"] == head
    assert row["initialized"] is True
    assert row["conflicted"] is False
    assert row["branch"] == "main"
    assert row["commit_changed"] is False
    assert row["tracked_dirty"] is False
    assert row["untracked_dirty"] is False
    assert row["target_local"] is True
    assert row["contained"] is True
    assert row["nested"] is False
    assert row["reason"] is None


def test_uninitialized_submodule_has_null_facts(facts, submodule_repo):
    submodule_repo.git("submodule", "deinit", "-q", "-f", "--", SUB)
    row = row_of(facts(submodule_repo))
    assert row["initialized"] is False
    assert row["gitlink"] is not None
    for key in (
        "head", "branch", "commit_changed", "tracked_dirty", "untracked_dirty",
        "target_local", "contained", "nested",
    ):  # fmt: skip
        assert row[key] is None, key


def test_dirty_tracked_file_sets_only_the_tracked_flag(facts, submodule_repo):
    (submodule_repo.work / SUB / "lib.txt").write_text("changed\n", encoding="utf-8")
    row = row_of(facts(submodule_repo))
    assert (row["tracked_dirty"], row["untracked_dirty"]) == (True, False)
    assert row["commit_changed"] is False


def test_untracked_file_sets_only_the_untracked_flag(facts, submodule_repo):
    (submodule_repo.work / SUB / "new.txt").write_text("new\n", encoding="utf-8")
    row = row_of(facts(submodule_repo))
    assert (row["tracked_dirty"], row["untracked_dirty"]) == (False, True)


def test_dirty_facts_survive_an_ignore_all_setting(facts, submodule_repo):
    submodule_repo.git("config", "submodule.lib.ignore", "all")
    (submodule_repo.work / SUB / "lib.txt").write_text("changed\n", encoding="utf-8")
    assert row_of(facts(submodule_repo))["tracked_dirty"] is True


def test_new_commit_in_the_module_sets_commit_changed(facts, submodule_repo):
    gitlink = sub_git(submodule_repo, "rev-parse", "HEAD").strip()
    (submodule_repo.work / SUB / "lib.txt").write_text("two\n", encoding="utf-8")
    sub_git(submodule_repo, "commit", "-q", "-am", "second")
    row = row_of(facts(submodule_repo))
    assert row["commit_changed"] is True
    assert row["gitlink"] == gitlink
    assert row["head"] != gitlink
    assert row["contained"] is True  # the branch main holds it
    sub_git(submodule_repo, "switch", "-q", "--detach", "HEAD")
    sub_git(submodule_repo, "branch", "-q", "-D", "main")
    row = row_of(facts(submodule_repo))
    assert row["branch"] is None
    assert row["contained"] is False  # in no local or remote-tracking branch


def test_unfetched_gitlink_gives_target_local_false(facts, submodule_repo):
    origin = submodule_repo.sub_origin
    (origin / "lib.txt").write_text("upstream\n", encoding="utf-8")
    git_in(origin, "commit", "-q", "-am", "upstream second")
    new = git_in(origin, "rev-parse", "HEAD").strip()
    submodule_repo.git("update-index", "--cacheinfo", f"160000,{new},{SUB}")
    submodule_repo.git("commit", "-q", "-m", "bump pointer")
    row = row_of(facts(submodule_repo))
    assert row["gitlink"] == new
    assert row["target_local"] is False
    assert row["commit_changed"] is True


def test_recursion_config_tells_unset_from_false(facts, repo):
    result = facts(repo)
    assert result["config"] == {
        "submodule_recurse": None,
        "push_recurse_submodules": None,
    }
    repo.git("config", "submodule.recurse", "false")
    repo.git("config", "push.recurseSubmodules", "check")
    result = facts(repo)
    assert result["config"]["submodule_recurse"] == "false"
    assert result["config"]["push_recurse_submodules"] == "check"
    assert result["warnings"] == []


def test_recurse_true_warns_about_a_later_push(facts, repo):
    repo.git("config", "submodule.recurse", "true")
    warnings = facts(repo)["warnings"]
    assert len(warnings) == 1
    assert "submodule.recurse" in warnings[0]
    assert "push" in warnings[0]


def test_nested_submodule_is_reported_not_inspected(facts, submodule_repo):
    (submodule_repo.work / SUB / ".gitmodules").write_text("", encoding="utf-8")
    row = row_of(facts(submodule_repo))
    assert row["nested"] is True
    assert "nested-not-inspected" in row["reason"]


def test_rows_are_sorted_by_path(facts, submodule_repo, tmp_path):
    other = tmp_path / "other-origin"
    other.mkdir()
    git_in(other, "init", "-q", "-b", "main")
    (other / "o.txt").write_text("o\n", encoding="utf-8")
    git_in(other, "add", "-A")
    git_in(other, "-c", "user.name=t", "-c", "user.email=t@example.invalid",
           "commit", "-q", "-m", "o")  # fmt: skip
    submodule_repo.git(
        "submodule", "add", "-q", "--name", "other", sub_url(other), "a-first",
        config=["protocol.file.allow=always"],
    )  # fmt: skip
    paths = [r["path"] for r in facts(submodule_repo)["rows"]]
    assert paths == ["a-first", SUB]


def test_a_runner_that_is_not_person_invoked_is_refused(mods, submodule_repo):
    sm, plan, rules = mods
    with pytest.raises(rules.ForbiddenArgv):
        sm.collect_submodules(plan.GitRunner(submodule_repo.work))


def test_every_git_call_goes_through_the_runner(mods, submodule_repo):
    sm, plan, _ = mods
    runner = plan.GitRunner(submodule_repo.work, person_invoked=True, record=True)
    sm.collect_submodules(runner)
    assert runner.calls
    assert all(cmd[:4] == PREFIX for cmd in runner.calls)
    assert any(cmd[4:6] == ["-C", SUB] for cmd in runner.calls)


def test_module_file_has_no_write_verb_phrase_and_no_process_call():
    text = MODULE_FILE.read_text(encoding="utf-8")
    assert not WRITE_VERB_RE.search(text)
    assert "subprocess" not in text
    assert "src/superclaude/" not in text


# --- derived state and eligibility (second part of T-07) ----------------------------------
def sub_commit(repo, text="two\n"):
    """Commit a change inside the module on its current branch; returns the new sha."""
    (repo.work / SUB / "lib.txt").write_text(text, encoding="utf-8")
    sub_git(repo, "commit", "-q", "-am", text.strip())
    return sub_git(repo, "rev-parse", "HEAD").strip()


def bump(repo, sha):
    """Record ``sha`` as the gitlink in a new superproject commit."""
    repo.git("update-index", "--cacheinfo", f"160000,{sha},{SUB}")
    repo.git("commit", "-q", "-m", "bump pointer")


def orphan_the_head(repo):
    """Detach the module on a new commit that no branch holds."""
    sub_commit(repo)
    sub_git(repo, "switch", "-q", "--detach", "HEAD")
    sub_git(repo, "branch", "-q", "-D", "main")


def make_conflict(repo):
    """Leave the gitlink unmerged (stages 1 to 3), as a conflicting merge does."""
    gitlink = sub_git(repo, "rev-parse", "HEAD").strip()
    lines = f"0 {'0' * 40}\t{SUB}\n" + "".join(
        f"160000 {sha} {stage}\t{SUB}\n"
        for stage, sha in ((1, gitlink), (2, "1" * 40), (3, "2" * 40))
    )
    subprocess.run(
        ["git", "update-index", "--index-info"],
        cwd=repo.work,
        input=lines,
        text=True,
        check=True,
    )


def make_pointer_moved(repo):
    newer = sub_commit(repo)
    sub_git(repo, "switch", "-q", "--detach", "HEAD~1")
    bump(repo, newer)


def make_diverged(repo):
    sub_git(repo, "switch", "-q", "-c", "side")
    side = sub_commit(repo, "side\n")
    sub_git(repo, "switch", "-q", "main")
    sub_commit(repo, "main\n")
    bump(repo, side)


def make_target_not_local(repo):
    origin = repo.sub_origin
    (origin / "lib.txt").write_text("upstream\n", encoding="utf-8")
    git_in(origin, "commit", "-q", "-am", "upstream second")
    bump(repo, git_in(origin, "rev-parse", "HEAD").strip())


def make_published_detached(repo):
    """The module is detached on a commit a remote-tracking ref of its origin holds."""
    origin = repo.sub_origin
    (origin / "lib.txt").write_text("upstream\n", encoding="utf-8")
    git_in(origin, "commit", "-q", "-am", "upstream second")
    sub_git(repo, "fetch", "-q", "origin")
    sub_git(repo, "switch", "-q", "--detach", "origin/main")


STATE_CASES = {
    "conflict": make_conflict,
    "dirty-tracked": lambda r: (r.work / SUB / "lib.txt").write_text("x\n"),
    "dirty-untracked": lambda r: (r.work / SUB / "new.txt").write_text("x\n"),
    "detached-new-commits": orphan_the_head,
    "uninitialized": lambda r: r.git("submodule", "deinit", "-q", "-f", "--", SUB),
    "target-not-local": make_target_not_local,
    "submodule-ahead": sub_commit,
    "submodule-diverged": make_diverged,
    "pointer-moved": make_pointer_moved,
    "in-sync": lambda r: None,
}


@pytest.mark.parametrize("state", list(STATE_CASES))
def test_every_state_of_the_fr040_list(facts, submodule_repo, state):
    STATE_CASES[state](submodule_repo)
    assert row_of(facts(submodule_repo))["state"] == state


def test_dirty_beats_detached_and_conflict_beats_dirty(facts, submodule_repo):
    orphan_the_head(submodule_repo)
    (submodule_repo.work / SUB / "new.txt").write_text("x\n", encoding="utf-8")
    assert row_of(facts(submodule_repo))["state"] == "dirty-untracked"
    make_conflict(submodule_repo)
    assert row_of(facts(submodule_repo))["state"] == "conflict"


def test_new_rows_leave_the_fact_columns_and_a_clean_reason_alone(
    facts, submodule_repo
):
    row = row_of(facts(submodule_repo))
    assert row["reason"] is None
    assert row["remote_mismatch"] is False
    assert row["gitmodules_url"] == sub_url(submodule_repo.sub_origin)


def test_ancestor_exit_128_is_never_read_as_diverged(mods, submodule_repo):
    sm, plan, _ = mods
    sub_commit(submodule_repo)

    class Unsure(plan.GitRunner):
        def run(self, argv, **kw):
            if argv[0] == "merge-base":
                return 128, ""
            return super().run(argv, **kw)

    row = row_of(
        sm.collect_submodules(Unsure(submodule_repo.work, person_invoked=True))
    )
    assert row["state"] is None
    assert "ancestry-unknown" in row["reason"]
    assert row["update"] == {"ok": False, "reason": "state-unknown", "needs_url": False}


def refusal(row, which):
    assert row[which]["ok"] is False
    return row[which]["reason"]


UPDATE_REFUSALS = {
    "conflict": "conflict",
    "dirty-tracked": "submodule-dirty",
    "dirty-untracked": "submodule-dirty",
    "detached-new-commits": "detached-new-commits",
    "submodule-ahead": "submodule-ahead",
    "submodule-diverged": "submodule-diverged",
    "in-sync": "in-sync",
}


@pytest.mark.parametrize("state", list(UPDATE_REFUSALS))
def test_update_refuses_the_states_fr041_names(facts, submodule_repo, state):
    STATE_CASES[state](submodule_repo)
    assert refusal(row_of(facts(submodule_repo)), "update") == UPDATE_REFUSALS[state]


def test_update_is_allowed_for_a_moved_pointer_with_a_clean_module(
    facts, submodule_repo
):
    make_pointer_moved(submodule_repo)
    row = row_of(facts(submodule_repo))
    assert row["update"] == {"ok": True, "reason": None, "needs_url": False}


def test_update_is_refused_for_a_moved_pointer_over_a_dirty_module(
    facts, submodule_repo
):
    make_pointer_moved(submodule_repo)
    (submodule_repo.work / SUB / "new.txt").write_text("x\n", encoding="utf-8")
    assert refusal(row_of(facts(submodule_repo)), "update") == "submodule-dirty"


def test_update_is_allowed_for_a_missing_target_held_by_a_branch(facts, submodule_repo):
    make_target_not_local(submodule_repo)
    row = row_of(facts(submodule_repo))
    assert row["contained"] is True
    assert row["update"]["ok"] is True


def test_update_of_a_missing_target_with_orphan_commits_is_refused(
    facts, submodule_repo
):
    orphan_the_head(submodule_repo)
    origin = submodule_repo.sub_origin
    (origin / "lib.txt").write_text("upstream\n", encoding="utf-8")
    git_in(origin, "commit", "-q", "-am", "upstream second")
    bump(submodule_repo, git_in(origin, "rev-parse", "HEAD").strip())
    row = row_of(facts(submodule_repo))
    assert row["target_local"] is False
    assert refusal(row, "update") == "detached-new-commits"


def test_update_of_an_uninitialized_module_needs_the_url_repeat(facts, submodule_repo):
    STATE_CASES["uninitialized"](submodule_repo)
    row = row_of(facts(submodule_repo))
    assert row["update"] == {"ok": True, "reason": None, "needs_url": True}
    assert row["gitmodules_url"] == sub_url(submodule_repo.sub_origin)
    assert row["remote_mismatch"] is None


def test_update_of_an_uninitialized_module_without_a_url_is_refused(
    facts, submodule_repo
):
    STATE_CASES["uninitialized"](submodule_repo)
    submodule_repo.git(
        "config", "--file", ".gitmodules", "--unset", "submodule.lib.url"
    )
    row = row_of(facts(submodule_repo))
    assert row["gitmodules_url"] is None
    assert refusal(row, "update") == "gitmodules-url-unknown"


def test_remote_mismatch_refuses_update_even_when_nothing_else_does(
    facts, submodule_repo
):
    submodule_repo.git("config", "submodule.lib.url", "file:///elsewhere/lib")
    row = row_of(facts(submodule_repo))
    assert row["state"] == "in-sync"
    assert row["remote_mismatch"] is True
    assert refusal(row, "update") == "remote-mismatch"
    make_pointer_moved(submodule_repo)
    assert refusal(row_of(facts(submodule_repo)), "update") == "remote-mismatch"


def test_a_relative_gitmodules_url_is_not_compared_and_blocks_update(
    facts, submodule_repo
):
    """UNVERIFIED: how git resolves a relative url is not modelled; the row refuses."""
    submodule_repo.git(
        "config", "--file", ".gitmodules", "submodule.lib.url", "../lib-origin"
    )
    make_pointer_moved(submodule_repo)
    row = row_of(facts(submodule_repo))
    assert row["remote_mismatch"] is None
    assert "gitmodules-url-relative" in row["reason"]
    assert refusal(row, "update") == "remote-unverifiable"


def test_the_gitmodules_url_is_shown_without_credentials(facts, submodule_repo):
    secret = "https://user:secret@example.invalid/lib.git"
    submodule_repo.git("config", "--file", ".gitmodules", "submodule.lib.url", secret)
    row = row_of(facts(submodule_repo))
    assert row["gitmodules_url"] == "https://example.invalid/lib.git"
    assert "secret" not in json.dumps(row)


def test_commit_pointer_is_allowed_for_a_target_a_gitmodules_remote_holds(
    facts, submodule_repo
):
    make_published_detached(submodule_repo)
    row = row_of(facts(submodule_repo))
    assert row["state"] == "submodule-ahead"
    assert row["branch"] is None
    assert row["commit_pointer"] == {"ok": True, "reason": None}


def test_commit_pointer_refuses_an_unpublished_target(facts, submodule_repo):
    sub_commit(submodule_repo)
    row = row_of(facts(submodule_repo))
    assert refusal(row, "commit_pointer") == "submodule-unpublished"


def test_commit_pointer_needs_a_remote_with_the_gitmodules_url(facts, submodule_repo):
    sub_commit(submodule_repo)
    sub_git(submodule_repo, "remote", "set-url", "origin", "file:///elsewhere/lib")
    row = row_of(facts(submodule_repo))
    assert (
        refusal(row, "commit_pointer")
        == "submodule-unpublished reason=no-gitmodules-remote"
    )


def test_another_remote_holding_the_target_does_not_count(facts, submodule_repo):
    sub_commit(submodule_repo)
    sub_git(submodule_repo, "remote", "add", "other", "file:///elsewhere/lib")
    sub_git(submodule_repo, "update-ref", "refs/remotes/other/main", "HEAD")
    row = row_of(facts(submodule_repo))
    assert refusal(row, "commit_pointer") == "submodule-unpublished"


def test_commit_pointer_refuses_a_target_that_is_in_no_branch(facts, submodule_repo):
    orphan_the_head(submodule_repo)
    row = row_of(facts(submodule_repo))
    assert refusal(row, "commit_pointer") == "detached-new-commits"


def test_commit_pointer_refuses_when_nothing_differs(facts, submodule_repo):
    assert refusal(row_of(facts(submodule_repo)), "commit_pointer") == "in-sync"


@pytest.mark.parametrize(
    "state", ["conflict", "dirty-tracked", "dirty-untracked", "uninitialized"]
)
def test_commit_pointer_refuses_a_module_that_is_not_initialized_and_clean(
    facts, submodule_repo, state
):
    STATE_CASES[state](submodule_repo)
    row = row_of(facts(submodule_repo))
    assert refusal(row, "commit_pointer") == "submodule-dirty"


@pytest.mark.parametrize("state", list(STATE_CASES))
def test_every_row_carries_both_eligibility_objects(facts, submodule_repo, state):
    STATE_CASES[state](submodule_repo)
    row = row_of(facts(submodule_repo))
    assert set(row["commit_pointer"]) == {"ok", "reason"}
    assert set(row["update"]) == {"ok", "reason", "needs_url"}
    for which in ("update", "commit_pointer"):
        assert isinstance(row[which]["ok"], bool)
        assert (row[which]["reason"] is None) == row[which]["ok"]


# --- the submodules verb -------------------------------------------------------------------
def run_cli(*args, cwd=None):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "vcs.py"), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=60,
    )


def add_second_submodule(repo, tmp_path):
    other = tmp_path / "other-origin"
    other.mkdir()
    git_in(other, "init", "-q", "-b", "main")
    (other / "o.txt").write_text("o\n", encoding="utf-8")
    git_in(other, "add", "-A")
    git_in(other, "-c", "user.name=t", "-c", "user.email=t@example.invalid",
           "commit", "-q", "-m", "o")  # fmt: skip
    repo.git(
        "submodule", "add", "-q", "--name", "other", sub_url(other), "a-first",
        config=["protocol.file.allow=always"],
    )  # fmt: skip


def test_cli_submodules_prints_sorted_rows_with_state_and_eligibility(
    submodule_repo, tmp_path
):
    add_second_submodule(submodule_repo, tmp_path)
    done = run_cli("submodules", "--cwd", str(submodule_repo.work))
    assert done.returncode == 0, done.stderr
    assert done.stdout.count("\n") == 1
    data = json.loads(done.stdout)
    assert (data["vcs_contract"], data["verb"]) == ("1", "submodules")
    assert (data["status"], data["reason"]) == ("ok", None)
    assert [r["path"] for r in data["rows"]] == ["a-first", SUB]
    for row in data["rows"]:
        assert "state" in row
        assert set(row["update"]) >= {"ok", "reason"}
        assert set(row["commit_pointer"]) == {"ok", "reason"}
    assert data["superproject"]["branch"] == "main"
    assert set(data["config"]) == {"submodule_recurse", "push_recurse_submodules"}


def test_cli_submodules_without_submodules_gives_an_empty_list(repo):
    done = run_cli("submodules", cwd=repo.work)
    assert done.returncode == 0, done.stderr
    data = json.loads(done.stdout)
    assert (data["status"], data["rows"]) == ("ok", [])


def test_cli_submodules_outside_a_repository_is_a_refusal(tmp_path):
    done = run_cli("submodules", "--cwd", str(tmp_path))
    assert done.returncode == 0, done.stderr
    data = json.loads(done.stdout)
    assert (data["status"], data["reason"]) == ("refused", "not-a-repo")


def test_cli_submodules_leaves_the_repository_unchanged(submodule_repo):
    before = submodule_repo.git("status", "--porcelain=v2", "--ignore-submodules=none")
    head = submodule_repo.git("rev-parse", "HEAD")
    run_cli("submodules", "--cwd", str(submodule_repo.work))
    assert submodule_repo.git("rev-parse", "HEAD") == head
    after = submodule_repo.git("status", "--porcelain=v2", "--ignore-submodules=none")
    assert after == before


def test_cli_submodules_rejects_an_unknown_option(repo):
    assert run_cli("submodules", "--bogus", cwd=repo.work).returncode == 64
