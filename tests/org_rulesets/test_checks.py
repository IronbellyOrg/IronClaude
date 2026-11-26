"""read_repo, check_push (the 90-day direct-push check) and read_existing."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

NOW = datetime(2026, 11, 26, 17, 0, tzinfo=timezone.utc)
CUTOFF = "2026-08-28T17:00:00Z"  # NOW minus 90 days
IN_WINDOW = "2026-10-01T10:00:00Z"
OLD = "2026-08-01T10:00:00Z"
REPO = "repos/acme/acme-one"


def sha(n):
    return f"{n:040x}"


def event(kind, when=IN_WINDOW):
    return {"activity_type": kind, "timestamp": when}


def activity_path(branch):
    return f"{REPO}/activity?ref=refs/heads/{branch}&time_period=quarter&per_page=100"


def commits_path(branch):
    return f"{REPO}/commits?sha={branch}&since={CUTOFF}&per_page=100"


@pytest.fixture
def make(fake_runner_cls):
    """A fake runner whose canned answers are given as a dict of GET paths."""

    def build(gets):
        return fake_runner_cls({("GET", path): answer for path, answer in gets.items()})

    return build


# --- read_repo ---------------------------------------------------------------------


def repo_answer(ok, **changes):
    data = {
        "owner": {"login": "acme"},
        "name": "acme-one",
        "archived": False,
        "default_branch": "main",
        "permissions": {"admin": True},
    }
    return ok({**data, **changes})


def test_read_repo_uses_the_canonical_spelling(make, orr, fake_runner_cls):
    ok = fake_runner_cls.ok
    runner = make(
        {
            "repos/ACME/Acme-One": repo_answer(ok),
            f"{REPO}/branches/master": ok({}),
            f"{REPO}/branches/integration": fake_runner_cls.http(404),
        }
    )
    info = orr.read_repo(runner, "ACME", "Acme-One")
    assert (info["owner"], info["name"]) == ("acme", "acme-one")
    assert info["default_branch"] == "main"
    assert info["existing"] == ["master"]
    assert info["refusals"] == []
    # the branch calls name the canonical repo in full
    assert runner.commands[1].argv[-1] == f"{REPO}/branches/integration"


@pytest.mark.parametrize(
    ("changes", "reasons"),
    [
        ({"archived": True}, ["archived"]),
        ({"permissions": {"admin": False}}, ["no-admin"]),
        ({"permissions": None}, ["no-admin"]),
        ({"default_branch": None}, ["no-default-branch"]),
        (
            {"archived": True, "permissions": {}, "default_branch": ""},
            ["archived", "no-admin", "no-default-branch"],
        ),
    ],
)
def test_read_repo_refusal_reasons(make, orr, fake_runner_cls, changes, reasons):
    ok = fake_runner_cls.ok
    runner = make(
        {
            REPO: repo_answer(ok, **changes),
            f"{REPO}/branches/master": ok({}),
            f"{REPO}/branches/integration": ok({}),
        }
    )
    assert orr.read_repo(runner, "acme", "acme-one")["refusals"] == reasons


def test_read_repo_unreadable(make, orr, fake_runner_cls):
    runner = make({REPO: fake_runner_cls.http(404)})
    info = orr.read_repo(runner, "acme", "acme-one")
    assert info["refusals"] == ["unreadable"] and info["status"] == 404
    assert len(runner.executed) == 1


def test_read_repo_branch_lookup_failure_is_a_refusal(make, orr, fake_runner_cls):
    ok = fake_runner_cls.ok
    runner = make(
        {
            REPO: repo_answer(ok),
            f"{REPO}/branches/master": fake_runner_cls.http(500),
            f"{REPO}/branches/integration": ok({}),
        }
    )
    info = orr.read_repo(runner, "acme", "acme-one")
    assert info["refusals"] == ["unreadable-branch"]
    assert info["existing"] == ["integration"]


# --- check_push --------------------------------------------------------------------


def test_zero_direct_pushes_pass(make, orr, fake_runner_cls):
    ok = fake_runner_cls.ok
    runner = make(
        {
            activity_path("master"): ok([event("pr_merge"), event("branch_creation")]),
            activity_path("integration"): fake_runner_cls.pages([], []),
        }
    )
    got = orr.check_push(runner, "acme", "acme-one", ["integration", "master"], NOW)
    assert got["result"] == "pass" and got["cutoff"] == CUTOFF
    assert got["branches"]["master"]["direct_pushes"] == 0
    assert got["branches"]["master"]["examined"] == 2
    assert got["branches"]["master"]["source"] == "activity"


@pytest.mark.parametrize("kind", ["push", "force_push", "branch_deletion"])
def test_a_direct_push_in_the_window_blocks(make, orr, fake_runner_cls, kind):
    ok = fake_runner_cls.ok
    runner = make({activity_path("master"): ok([event("pr_merge"), event(kind)])})
    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
    assert got["result"] == "blocked"
    assert got["branches"]["master"]["direct_pushes"] == 1


def test_old_events_and_merges_are_ignored(make, orr, fake_runner_cls):
    ok = fake_runner_cls.ok
    events = [event("push", OLD), event("force_push", OLD), event("pr_merge")]
    runner = make({activity_path("master"): ok(events)})
    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
    assert got["result"] == "pass"


def test_pages_are_joined(make, orr, fake_runner_cls):
    pages = fake_runner_cls.pages([event("pr_merge")], [event("push")])
    runner = make({activity_path("master"): pages})
    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
    assert got["result"] == "blocked"


def commit_runner(make, fake_runner_cls, branch, commits, pulls):
    """Activity answers 403; the commit list and the pull lookups are canned."""
    gets = {
        activity_path(branch): fake_runner_cls.http(403),
        commits_path(branch): fake_runner_cls.ok([{"sha": sha(n)} for n in commits]),
    }
    for n, answer in pulls.items():
        gets[f"{REPO}/commits/{sha(n)}/pulls"] = answer
    return make(gets)


def merged(branch="master"):
    return [{"merged_at": "2026-10-01T10:00:00Z", "base": {"ref": branch}}]


def test_fallback_a_merged_commit_is_not_a_direct_push(make, orr, fake_runner_cls):
    ok = fake_runner_cls.ok
    runner = commit_runner(
        make, fake_runner_cls, "master", [1, 2], {1: ok(merged()), 2: ok(merged())}
    )
    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
    assert got["result"] == "pass"
    assert got["branches"]["master"]["source"] == "commits"
    assert got["branches"]["master"]["examined"] == 2


def test_fallback_a_commit_with_no_merged_pull_is_a_direct_push(
    make, orr, fake_runner_cls
):
    ok = fake_runner_cls.ok
    opened = [{"merged_at": None, "base": {"ref": "master"}}]
    other = merged("other")
    pulls = {1: ok(merged()), 2: ok([]), 3: ok(opened), 4: ok(other)}
    runner = commit_runner(make, fake_runner_cls, "master", [1, 2, 3, 4], pulls)
    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
    assert got["result"] == "blocked"
    assert got["branches"]["master"]["direct_pushes"] == 3


def test_both_sources_forbidden_is_incomplete(make, orr, fake_runner_cls):
    http = fake_runner_cls.http
    runner = make(
        {activity_path("master"): http(403), commits_path("master"): http(403)}
    )
    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
    assert got["result"] == "incomplete"


def test_a_failed_pull_lookup_is_incomplete(make, orr, fake_runner_cls):
    ok = fake_runner_cls.ok
    pulls = {1: ok(merged()), 2: fake_runner_cls.http(502)}
    runner = commit_runner(make, fake_runner_cls, "master", [1, 2], pulls)
    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
    assert got["result"] == "incomplete"


def test_a_direct_push_wins_over_a_failed_lookup(make, orr, fake_runner_cls):
    ok = fake_runner_cls.ok
    pulls = {1: fake_runner_cls.http(502), 2: ok([])}
    runner = commit_runner(make, fake_runner_cls, "master", [1, 2], pulls)
    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
    assert got["result"] == "blocked"


def test_a_truncated_page_chain_is_incomplete(make, orr, fake_runner_cls):
    too_many = fake_runner_cls.pages(*[[] for _ in range(orr.PAGE_CAP + 1)])
    runner = make({activity_path("master"): too_many, commits_path("master"): too_many})
    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
    assert got["result"] == "incomplete"
    assert got["branches"]["master"]["source"] == "commits"


def test_activity_past_the_cap_falls_back_to_commits(make, orr, fake_runner_cls):
    ok = fake_runner_cls.ok
    too_many = fake_runner_cls.pages(*[[] for _ in range(orr.PAGE_CAP + 1)])
    runner = make({activity_path("master"): too_many, commits_path("master"): ok([])})
    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
    assert got["result"] == "pass"
    assert got["branches"]["master"]["source"] == "commits"


def test_201_lookups_is_incomplete_and_200_are_made(make, orr, fake_runner_cls):
    ok = fake_runner_cls.ok
    numbers = list(range(1, 202))
    pulls = {n: ok(merged()) for n in numbers}
    runner = commit_runner(make, fake_runner_cls, "master", numbers, pulls)
    got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
    assert got["result"] == "incomplete"
    looked_up = [c for c in runner.commands if c.argv[-1].endswith("/pulls")]
    assert len(looked_up) == orr.LOOKUP_CAP == 200


def test_exactly_200_lookups_can_pass(make, orr, fake_runner_cls):
    ok = fake_runner_cls.ok
    numbers = list(range(1, 201))
    pulls = {n: ok(merged()) for n in numbers}
    runner = commit_runner(make, fake_runner_cls, "master", numbers, pulls)
    assert (
        orr.check_push(runner, "acme", "acme-one", ["master"], NOW)["result"] == "pass"
    )


def test_overall_result_blocked_beats_incomplete_beats_pass(make, orr, fake_runner_cls):
    ok = fake_runner_cls.ok
    http = fake_runner_cls.http
    gets = {
        activity_path("integration"): ok([]),
        activity_path("master"): ok([event("push")]),
        activity_path("main"): http(403),
        commits_path("main"): http(403),
    }
    runner = make(gets)
    run = orr.check_push
    assert (
        run(runner, "acme", "acme-one", ["integration", "master"], NOW)["result"]
        == "blocked"
    )
    assert (
        run(runner, "acme", "acme-one", ["integration", "main"], NOW)["result"]
        == "incomplete"
    )
    assert run(runner, "acme", "acme-one", ["integration"], NOW)["result"] == "pass"
    assert (
        run(runner, "acme", "acme-one", ["master", "main"], NOW)["result"] == "blocked"
    )


def test_no_branch_is_never_a_pass(make, orr):
    assert (
        orr.check_push(make({}), "acme", "acme-one", [], NOW)["result"] == "incomplete"
    )


def test_garbage_from_both_sources_is_incomplete(make, orr, fake_runner_cls):
    for text in ("", "not json", '{"a": 1}', '[{"timestamp": "x"}]'):
        bad = orr.Result(0, text, "")
        runner = make({activity_path("master"): bad, commits_path("master"): bad})
        got = orr.check_push(runner, "acme", "acme-one", ["master"], NOW)
        assert got["result"] == "incomplete", text


# --- read_existing -----------------------------------------------------------------


def test_read_existing_reports_each_part(make, orr, fake_runner_cls):
    ok, http = fake_runner_cls.ok, fake_runner_cls.http
    runner = make(
        {
            f"{REPO}/rulesets?per_page=100": fake_runner_cls.pages(
                [{"id": 9, "name": "protect-master"}], [{"id": 10, "name": "other"}]
            ),
            f"{REPO}/branches/integration/protection": ok({}),
            f"{REPO}/branches/master/protection": http(404),
            f"{REPO}/branches/main/protection": http(500),
            f"{REPO}/git/matching-refs/tags/v?per_page=100": ok([{}, {}, {}]),
        }
    )
    got = orr.read_existing(
        runner, "acme", "acme-one", ["integration", "master", "main"]
    )
    assert got["rulesets"] == {"protect-master": 9, "other": 10}
    assert got["protection"] == {
        "integration": "classic",
        "master": "none",
        "main": "unknown",
    }
    assert got["v_tags"] == 3


def test_read_existing_unknown_when_the_reads_fail(make, orr, fake_runner_cls):
    http = fake_runner_cls.http
    runner = make(
        {
            f"{REPO}/rulesets?per_page=100": http(403),
            f"{REPO}/git/matching-refs/tags/v?per_page=100": http(403),
        }
    )
    got = orr.read_existing(runner, "acme", "acme-one", [])
    assert got["rulesets"] is None and got["rulesets_status"] == 403
    assert got["v_tags"] is None and got["protection"] == {}


def test_read_existing_no_rulesets_and_no_tags(make, orr, fake_runner_cls):
    ok = fake_runner_cls.ok
    runner = make(
        {
            f"{REPO}/rulesets?per_page=100": ok([]),
            f"{REPO}/git/matching-refs/tags/v?per_page=100": ok([]),
        }
    )
    got = orr.read_existing(runner, "acme", "acme-one", [])
    assert got["rulesets"] == {} and got["v_tags"] == 0
