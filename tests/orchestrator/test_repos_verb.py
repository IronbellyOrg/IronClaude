"""``repos`` (4.4, 5.6): check, add and refresh keep repos.yaml current; the three keys of Clay's go only through ``set``."""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from superclaude.cli.issue_watch import repos
from superclaude.cli.orchestrator import actions, ext, limits, repos_file
from superclaude.cli.orchestrator.group import orchestrator_group
from superclaude.cli.orchestrator.repos_verb import question_key

from .fake_world import (
    REPO,
    World,
    answer,
    asked,
    call,
    install,
    make_root,
    repos_text,
    snapshot,
)

NEW = "IronbellyGroup/example"
UNSAFE_RIGHTS = {
    "admin": False,
    "maintain": False,
    "push": False,
    "triage": False,
    "pull": True,
}


@pytest.fixture
def world(monkeypatch) -> World:
    w = install(monkeypatch, World())
    w.set_repo(NEW, methods=("squash",))
    w.set_repo(REPO, default_branch="master", protected=False)
    yield w
    assert not w.unexpected, w.unexpected
    assert [c for c in w.calls if limits.refuse(list(c)) is not None] == []
    assert [c for c in w.calls if "-X" in c] == []  # the repos verbs only read GitHub


def guarded_text() -> str:
    """A file that already holds all three keys of Clay's, so a write that drops one shows."""
    entry = {
        "repo": REPO,
        "enabled": True,
        "checkout": "/abs/ironclaude",
        "default_branch": "master",
        "merge_method": "squash",
        "can_merge": True,
        "protected": False,
        "reach_daily_max": 5,
        "merge_safety_files": [".github/workflows/**", "CODEOWNERS"],
    }
    return repos_text(repos=[entry])


@pytest.fixture
def root(tmp_path: Path, world: World) -> Path:
    return make_root(tmp_path, text=guarded_text(), run=False)


def parsed(root: Path) -> dict:
    return yaml.safe_load((root / "repos.yaml").read_text())


def entry_of(root: Path, repo: str) -> dict:
    return next(e for e in parsed(root)["repos"] if e["repo"] == repo)


def valid_for_the_poll(root: Path, world: World) -> repos.ReposDoc:
    """The poll's own validator accepts the file as the verbs left it."""
    return repos.load_repos(root, world, 5)


# --- check ---------------------------------------------------------------------------------------


def test_check_prints_what_the_poll_would_read(root: Path) -> None:
    code, out = call(root, "repos", "check")
    assert code == 0 and out["ok"] is True
    assert out["orgs"] == ["IronbellyOrg", "IronbellyGroup"]
    assert out["grants"] == ["issue.comment", "issue.assign"]
    (listed,) = out["repos"]
    assert (
        listed["repo"] == REPO
        and listed["short"] == "ironclaude"
        and listed["enabled"] is True
    )
    assert listed["max_in_flight"] == 3 and listed["reach_daily_max"] == 5
    assert listed["merge_safety_files"] == [".github/workflows/**", "CODEOWNERS"]
    assert (listed["default_branch"], listed["protected"], listed["can_merge"]) == (
        "master",
        False,
        True,
    )
    assert "tier1b" in out["tiers"]


@pytest.mark.parametrize(
    "text",
    [
        "schema_version: 2\n",
        "not: [valid",
        "- a list\n",
        repos_text(grants="issue.comment"),
    ],
)
def test_check_names_repos_invalid_for_a_file_the_poll_would_refuse(
    tmp_path: Path, world: World, text: str
) -> None:
    code, out = call(make_root(tmp_path, text=text, run=False), "repos", "check")
    assert (code, out["reason"]) == (2, "repos_invalid") and out["detail"]


def test_check_cannot_validate_without_the_tier_list(root: Path, world: World) -> None:
    world.fail_when.append(lambda argv: argv[0] == "ccsession")
    code, out = call(root, "repos", "check")
    assert (code, out["reason"]) == (2, "repos_invalid")


def test_check_with_no_file_is_repos_invalid(tmp_path: Path, world: World) -> None:
    code, out = call(tmp_path, "repos", "check")
    assert (code, out["reason"]) == (2, "repos_invalid")


# --- add -----------------------------------------------------------------------------------------


def test_add_reads_the_repo_from_github_and_lists_it(root: Path, world: World) -> None:
    code, out = call(root, "repos", "add", "--repo", NEW, "--checkout", "/abs/example")
    assert code == 0 and out["enabled"] is True and out["can_merge"] is True
    assert out["allowed_methods"] == ["squash"] and out["merge_method"] == "squash"
    assert world.argvs("gh") == [
        ("gh", "api", f"repos/{NEW}"),
        ("gh", "api", f"repos/{NEW}/branches/master"),
    ]
    assert entry_of(root, NEW) == {
        "repo": NEW,
        "enabled": True,
        "checkout": "/abs/example",
        "clone_parent": None,
        "default_branch": "master",
        "merge_method": "squash",
        "release_merge_method": None,
        "release_head": None,
        "protected": False,
        "can_merge": True,
    }
    assert valid_for_the_poll(root, world).get(NEW).enabled is True


def test_add_with_several_methods_allowed_asks_for_the_choice_and_keeps_none_by_default(
    root: Path, world: World
) -> None:
    world.set_repo(NEW, methods=("squash", "merge", "rebase"))
    code, out = call(root, "repos", "add", "--repo", NEW)
    assert code == 0 and out["merge_method"] is None
    code, out = call(root, "repos", "add", "--repo", "IronbellyGroup/second")
    assert (code, out["reason"]) == (
        6,
        "external_failed",
    )  # GitHub does not know it: nothing is written
    assert [e["repo"] for e in parsed(root)["repos"]] == [REPO, NEW]


def test_add_takes_the_method_the_caller_names_when_the_repo_allows_it(
    root: Path, world: World
) -> None:
    world.set_repo(NEW, methods=("squash", "merge"))
    code, out = call(
        root, "repos", "add", "--repo", NEW, "--merge-method", "squash",
        "--release-merge-method", "merge", "--release-head", "integration",
        "--reviewers", "augment,codex", "--max-in-flight", "2",
    )  # fmt: skip
    assert code == 0
    e = entry_of(root, NEW)
    assert (e["merge_method"], e["release_merge_method"], e["release_head"]) == (
        "squash",
        "merge",
        "integration",
    )
    assert (e["reviewers"], e["max_in_flight"]) == (["augment", "codex"], 2)
    assert valid_for_the_poll(root, world).get(NEW).reviewers == ("augment", "codex")


def test_add_refuses_a_method_the_repo_does_not_allow(root: Path, world: World) -> None:
    before = snapshot(root)
    code, out = call(root, "repos", "add", "--repo", NEW, "--merge-method", "rebase")
    assert (code, out["reason"]) == (2, "method_not_allowed")
    assert snapshot(root) == before


def test_a_repo_with_read_access_only_is_stored_disabled(
    root: Path, world: World
) -> None:
    world.set_repo(NEW, permissions=UNSAFE_RIGHTS)
    code, out = call(root, "repos", "add", "--repo", NEW)
    assert code == 0 and (out["enabled"], out["can_merge"]) == (False, False)
    e = entry_of(root, NEW)
    assert (e["enabled"], e["can_merge"]) == (False, False)


def test_add_with_disabled_lists_a_mergeable_repo_disabled(
    root: Path, world: World
) -> None:
    code, out = call(root, "repos", "add", "--repo", NEW, "--disabled")
    assert code == 0 and (out["enabled"], out["can_merge"]) == (False, True)


def test_add_never_lists_a_repo_twice(root: Path, world: World) -> None:
    world.set_repo(REPO.lower())  # the same repo spelled in lower case
    before = snapshot(root)
    code, out = call(root, "repos", "add", "--repo", REPO.lower())
    assert (code, out["reason"]) == (3, "already_listed")
    assert snapshot(root) == before


@pytest.mark.parametrize(
    ("repo", "why"),
    [("Outsider/example", "owner"), ("IronbellyGroup/Iron-Claude", "short name")],
)
def test_add_writes_nothing_the_poll_would_refuse(
    root: Path, world: World, repo: str, why: str
) -> None:
    world.set_repo(repo)
    before = snapshot(root)
    code, out = call(root, "repos", "add", "--repo", repo)
    assert (code, out["reason"]) == (2, "repos_invalid"), why
    assert snapshot(root) == before


def test_a_github_failure_or_an_unreadable_answer_writes_nothing(
    root: Path, world: World
) -> None:
    before = snapshot(root)
    world.fail_when.append(lambda argv: argv[2].endswith("/branches/master"))
    code, out = call(root, "repos", "add", "--repo", NEW)
    assert (code, out["reason"]) == (6, "external_failed") and "stderr" not in out
    world.fail_when.clear()
    world.repo_meta[NEW]["permissions"] = "nope"
    code, out = call(root, "repos", "add", "--repo", NEW)
    assert (code, out["reason"]) == (6, "external_unreadable")
    assert snapshot(root) == before


def test_add_leaves_the_three_guarded_keys_exactly_as_they_were(
    root: Path, world: World
) -> None:
    before = parsed(root)
    call(root, "repos", "add", "--repo", NEW)
    after = parsed(root)
    assert after["grants"] == before["grants"]
    assert entry_of(root, REPO)["reach_daily_max"] == 5
    assert entry_of(root, REPO)["merge_safety_files"] == [
        ".github/workflows/**",
        "CODEOWNERS",
    ]
    assert "reach_daily_max" not in entry_of(
        root, NEW
    ) and "merge_safety_files" not in entry_of(root, NEW)


@pytest.mark.parametrize(
    "option", ["--grants", "--reach-daily-max", "--merge-safety-files"]
)
def test_add_has_no_option_that_writes_a_guarded_key(root: Path, option: str) -> None:
    result = CliRunner().invoke(
        orchestrator_group,
        ["--root", str(root), "repos", "add", "--repo", NEW, option, "1"],
    )
    assert result.exit_code == 2 and "No such option" in result.output


def test_the_file_keeps_its_mode_and_is_replaced_whole(
    root: Path, world: World
) -> None:
    os.chmod(root / "repos.yaml", 0o644)
    call(root, "repos", "add", "--repo", NEW)
    assert stat.S_IMODE((root / "repos.yaml").stat().st_mode) == 0o644
    assert [p.name for p in root.iterdir() if p.name.endswith(".tmp")] == []


# --- refresh -------------------------------------------------------------------------------------


def test_refresh_updates_the_facts_of_every_repo_and_nothing_else(
    root: Path, world: World
) -> None:
    world.set_repo(REPO, default_branch="main", protected=True)
    before = parsed(root)
    code, out = call(root, "repos", "refresh")
    assert code == 0 and out["guarded"] == []
    (row,) = out["repos"]
    assert row == {
        "repo": REPO,
        "changed": {"default_branch": "main", "protected": True},
        "warnings": [],
    }
    after = entry_of(root, REPO)
    assert (after["default_branch"], after["protected"]) == ("main", True)
    after.update(
        default_branch="master", protected=False
    )  # put the two facts back: nothing else moved
    assert after == before["repos"][0]
    assert parsed(root)["grants"] == before["grants"]


def test_refresh_disables_a_repo_whose_rights_fell_and_never_enables_one(
    root: Path, world: World
) -> None:
    world.set_repo(REPO, permissions=UNSAFE_RIGHTS)
    code, out = call(root, "repos", "refresh", "--repo", REPO)
    assert code == 0
    assert out["repos"][0]["changed"] == {"can_merge": False, "enabled": False}
    assert entry_of(root, REPO)["enabled"] is False
    world.set_repo(
        REPO
    )  # the rights are back: refresh reports them but does not enable
    call(root, "repos", "refresh")
    e = entry_of(root, REPO)
    assert (e["can_merge"], e["enabled"]) == (True, False)


def test_refresh_warns_about_a_method_the_repo_no_longer_allows_and_keeps_it(
    root: Path, world: World
) -> None:
    world.set_repo(REPO, methods=("merge",))
    code, out = call(root, "repos", "refresh")
    assert code == 0 and out["repos"][0]["warnings"] == ["merge_method_not_allowed"]
    assert entry_of(root, REPO)["merge_method"] == "squash"


def test_refresh_of_an_unlisted_repo_is_refused(root: Path, world: World) -> None:
    code, out = call(root, "repos", "refresh", "--repo", NEW)
    assert (code, out["reason"]) == (2, "repo_not_listed")


def test_refresh_keeps_the_guarded_keys(root: Path, world: World) -> None:
    world.set_repo(REPO, permissions=UNSAFE_RIGHTS, default_branch="trunk")
    before = entry_of(root, REPO)
    call(root, "repos", "refresh")
    after = entry_of(root, REPO)
    assert after["reach_daily_max"] == before["reach_daily_max"] == 5
    assert after["merge_safety_files"] == before["merge_safety_files"]


# --- set: Clay's three keys, and the one place a write of them is checked ------------------------


GUARDED = [
    ("grants", None, '["issue.comment","pr.merge"]'),
    ("reach_daily_max", REPO, "7"),
    ("merge_safety_files", REPO, '["CODEOWNERS"]'),
]


def set_args(key: str, repo: str | None, value: str, *ref: str) -> list[str]:
    args = ["repos", "set", "--key", key, "--value-json", value]
    if repo is not None:
        args += ["--repo", repo]
    return args + list(ref)


_asked_n = iter(range(1, 10_000))


def ok_for(root: Path, key: str, repo: str | None, accepted: bool = True) -> str:
    """The ref of an ``answer-check`` that Clay's word passed (or failed) for exactly this change."""
    entry = f"repos.{next(_asked_n)}"
    question = question_key(key, repo)
    asked(root, entry=entry, key=question)
    return answer(root, accepted=accepted, entry=entry, key=question)


@pytest.mark.parametrize(("key", "repo", "value"), GUARDED, ids=[g[0] for g in GUARDED])
def test_a_guarded_key_is_refused_without_an_answer_ref_and_nothing_is_written(
    root: Path, key: str, repo: str | None, value: str
) -> None:
    before = snapshot(root)
    code, out = call(root, *set_args(key, repo, value))
    assert (code, out["reason"], out["keys"]) == (2, "answer_ref_required", [key])
    assert snapshot(root) == before


@pytest.mark.parametrize(("key", "repo", "value"), GUARDED, ids=[g[0] for g in GUARDED])
def test_a_ref_that_answer_check_never_made_is_refused(
    root: Path, key: str, repo: str | None, value: str
) -> None:
    before = snapshot(root)
    for ref in ("a-20261119T103000Z-deadbeef", "not even a ref", "x" * 300):
        code, out = call(root, *set_args(key, repo, value, "--answer-ref", ref))
        assert (code, out["reason"]) == (2, "answer_ref_unknown")
    assert snapshot(root) == before


@pytest.mark.parametrize(("key", "repo", "value"), GUARDED, ids=[g[0] for g in GUARDED])
def test_a_ref_that_answer_check_rejected_is_refused(
    root: Path, key: str, repo: str | None, value: str
) -> None:
    ref = ok_for(root, key, repo, accepted=False)
    before = snapshot(root)
    code, out = call(root, *set_args(key, repo, value, "--answer-ref", ref))
    assert (code, out["reason"]) == (2, "answer_ref_rejected")
    assert snapshot(root) == before


def test_a_ref_from_another_kind_of_row_is_not_an_answer(root: Path) -> None:
    ref = actions.append(root, "repos-write", keys=["grants"], ref="a-x")
    code, out = call(root, *set_args("grants", None, "[]", "--answer-ref", ref))
    assert (code, out["reason"]) == (2, "answer_ref_unknown")


def test_an_accepted_ref_lets_each_key_be_written_and_the_write_is_logged(
    root: Path, world: World
) -> None:
    refs = []
    for key, repo, value in GUARDED:
        refs.append(ok_for(root, key, repo))
        code, out = call(root, *set_args(key, repo, value, "--answer-ref", refs[-1]))
        assert code == 0 and out["guarded"] == [key], (key, out)
    doc = parsed(root)
    assert doc["grants"] == ["issue.comment", "pr.merge"]
    assert entry_of(root, REPO)["reach_daily_max"] == 7
    assert entry_of(root, REPO)["merge_safety_files"] == ["CODEOWNERS"]
    assert valid_for_the_poll(root, world).get(REPO).reach_daily_max == 7
    rows = [
        json.loads(line)
        for line in (root / ".orchestrator/actions.jsonl").read_text().splitlines()
    ]
    writes = [r for r in rows if r["kind"] == "repos-write"]
    assert [r["keys"] for r in writes] == [
        ["grants"],
        ["reach_daily_max"],
        ["merge_safety_files"],
    ]
    assert [r["ref"] for r in writes] == refs  # one OK for each write


def test_an_ok_for_one_question_never_opens_another_key_or_another_repo(
    root: Path,
) -> None:
    """The answer to the "merge" question, or to another key, is no word on these three keys."""
    before = snapshot(root)
    asked(root)  # the merge question of the other tests
    merge = answer(root, key="IronbellyOrg__IronClaude__655:8:merge")
    for key, repo, value in GUARDED:
        code, out = call(root, *set_args(key, repo, value, "--answer-ref", merge))
        assert (code, out["reason"]) == (2, "answer_ref_key_mismatch")
    for ok_key, ok_repo in (("grants", None), ("reach_daily_max", REPO)):
        ref = ok_for(root, ok_key, ok_repo)
        code, out = call(
            root, *set_args("merge_safety_files", REPO, "[]", "--answer-ref", ref)
        )
        assert (code, out["reason"]) == (2, "answer_ref_key_mismatch")
    ref = ok_for(root, "reach_daily_max", NEW)  # the same key for another repo
    code, out = call(root, *set_args("reach_daily_max", REPO, "3", "--answer-ref", ref))
    assert (code, out["reason"]) == (2, "answer_ref_key_mismatch")
    code, out = call(
        root, *set_args("grants", None, "[]", "--answer-ref", answer_without_key(root))
    )
    assert (code, out["reason"]) == (
        2,
        "answer_ref_key_mismatch",
    )  # an answer checked for no key
    assert snapshot(root)["repos.yaml"] == before["repos.yaml"]


def answer_without_key(root: Path) -> str:
    asked(root, entry="nokey.1", key="some:key")
    return answer(root, entry="nokey.1")


def test_an_accepted_ref_is_used_for_one_write_only(root: Path, world: World) -> None:
    ref = ok_for(root, "reach_daily_max", REPO)
    assert (
        call(root, *set_args("reach_daily_max", REPO, "7", "--answer-ref", ref))[0] == 0
    )
    before = snapshot(root)
    code, out = call(
        root, *set_args("reach_daily_max", REPO, "40", "--answer-ref", ref)
    )
    assert (code, out["reason"]) == (2, "answer_ref_used")
    assert snapshot(root) == before
    assert entry_of(root, REPO)["reach_daily_max"] == 7


@pytest.mark.parametrize(
    ("key", "repo", "value"),
    [
        ("reach_daily_max", REPO, "51"),
        ("reach_daily_max", REPO, "-1"),
        ("reach_daily_max", REPO, "true"),
        ("reach_daily_max", REPO, '"5"'),
        ("merge_safety_files", REPO, '[""]'),
        ("merge_safety_files", REPO, "null"),
        ("merge_safety_files", REPO, '"CODEOWNERS"'),
        ("grants", None, '{"a": 1}'),
        ("grants", None, "[1]"),
        ("grants", None, "not json"),
    ],
)
def test_a_value_the_poll_would_misread_is_refused_even_with_an_accepted_ref(
    root: Path, key: str, repo: str | None, value: str
) -> None:
    ref = ok_for(root, key, repo)
    before = snapshot(root)
    code, out = call(root, *set_args(key, repo, value, "--answer-ref", ref))
    assert (code, out["reason"]) == (2, "invalid_value")
    assert snapshot(root) == before


def test_set_needs_the_repo_for_a_per_repo_key_and_refuses_one_for_grants(
    root: Path,
) -> None:
    ref = ok_for(root, "reach_daily_max", None)
    code, out = call(root, *set_args("reach_daily_max", None, "3", "--answer-ref", ref))
    assert out["reason"] == "invalid_input"
    ref = ok_for(root, "grants", REPO)
    assert (
        call(root, *set_args("grants", REPO, "[]", "--answer-ref", ref))[1]["reason"]
        == "invalid_input"
    )
    ref = ok_for(root, "reach_daily_max", NEW)
    code, out = call(root, *set_args("reach_daily_max", NEW, "3", "--answer-ref", ref))
    assert (code, out["reason"]) == (2, "repo_not_listed")


def test_an_empty_safety_list_is_written_only_with_the_ref_and_means_no_hold(
    root: Path, world: World
) -> None:
    assert call(root, *set_args("merge_safety_files", REPO, "[]"))[0] == 2
    ref = ok_for(root, "merge_safety_files", REPO)
    code, _ = call(
        root, *set_args("merge_safety_files", REPO, "[]", "--answer-ref", ref)
    )
    assert (
        code == 0 and valid_for_the_poll(root, world).get(REPO).merge_safety_files == ()
    )


def test_the_choke_point_refuses_any_write_that_touches_a_guarded_key(
    root: Path, world: World
) -> None:
    """Not only ``set``: ``edit`` is the one way the file is written, so ``add`` and ``refresh`` cannot slip one in."""
    runner = ext.make_runner("test")
    before = snapshot(root)
    for change in (
        lambda new: new.update(grants=["issue.comment", "pr.merge"]),
        lambda new: new["repos"][0].update(reach_daily_max=9),
        lambda new: new["repos"][0].pop("merge_safety_files"),
        lambda new: new["repos"].append(
            {"repo": NEW, "enabled": True, "checkout": None, "reach_daily_max": 1}
        ),
    ):
        with pytest.raises(repos_file.StateError) as caught:
            repos_file.edit(root, runner, change)
        assert caught.value.reason == "answer_ref_required"
    assert snapshot(root) == before
    repos_file.edit(
        root, runner, lambda new: new["repos"][0].update(default_branch="main")
    )  # unguarded
    assert entry_of(root, REPO)["default_branch"] == "main"
