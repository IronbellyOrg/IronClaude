"""Every ``gh`` call the watcher builds and every reply it reads (design 4.2, 4.10, 4.11)."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import github
from superclaude.cli.issue_watch.github import CallBudget, LabelWriter
from superclaude.cli.issue_watch.runner import CommandResult

from .conftest import FakeRunner, load_fixture, result

NOW = datetime(2026, 11, 19, 12, 0, 0, tzinfo=timezone.utc)
SINCE = NOW - timedelta(minutes=5)


def tf() -> float:
    return 10.0


def search_reply(
    items: list[dict], *, total: int | None = None, incomplete: bool = False
) -> CommandResult:
    return result(
        stdout=json.dumps(
            {
                "total_count": len(items) if total is None else total,
                "incomplete_results": incomplete,
                "items": items,
            }
        )
    )


def row(repo: str = "IronbellyOrg/IronClaude", number: int = 5, **over) -> dict:
    base = load_fixture("gh_search_assigned.json")["payload"]["items"][0]
    base.update(repository_url=f"https://api.github.com/repos/{repo}", number=number)
    base.update(over)
    return base


# --- argv builders ----------------------------------------------------------------------


def test_s1_is_pinned_by_org_with_no_label_project_or_graphql_text():
    argv = github.argv_search_assigned("IronbellyOrg", "owner-login")
    assert argv[:6] == ["gh", "api", "--method", "GET", "search/issues", "-f"]
    assert argv[6] == "q=is:issue is:open assignee:owner-login org:IronbellyOrg"
    assert "per_page=100" in argv
    text = " ".join(argv).lower()
    for banned in ("graphql", "project", "issue-watch:", "--repo"):
        assert banned not in text
    assert "label:" not in argv[6]  # the labels of a row are read, never queried


def test_s2_to_s4_are_the_three_information_streams_since_the_last_poll():
    since = "2026-11-19T11:55:00Z"
    queries = {
        s: github.argv_search_info(s, "IronbellyGroup", "owner-login", SINCE)[6]
        for s in github.STREAMS
    }
    assert (
        queries["mentions"]
        == f"q=mentions:owner-login updated:>={since} org:IronbellyGroup"
    )
    assert queries["could_assign"] == (
        f"q=is:issue is:open no:assignee created:>={since} org:IronbellyGroup"
    )
    assert queries["affects"] == (
        f"q=involves:owner-login updated:>={since} org:IronbellyGroup -assignee:owner-login"
    )
    assert all("org:IronbellyGroup" in q for q in queries.values())


@pytest.mark.parametrize(
    "call",
    [
        lambda: github.argv_search_assigned("bad org", "x"),
        lambda: github.argv_search_assigned("IronbellyOrg", "a b"),
        lambda: github.argv_search_assigned("IronbellyOrg", "-x"),
        lambda: github.argv_search_info("bogus", "IronbellyOrg", "x", SINCE),
        lambda: github.argv_search_info(
            "mentions", "IronbellyOrg", "x", datetime(2026, 1, 1)
        ),
        lambda: github.argv_reread("not-a-repo", 5),
        lambda: github.argv_reread("o/r", 0),
        lambda: github.argv_reread("o/r", True),
        lambda: github.argv_branch_date("o/r", "--exec"),
        lambda: github.argv_branch_date("o/r", "a/../b"),
        lambda: github.argv_label_remove("o/r;x", 1),
    ],
)
def test_a_value_that_is_unsafe_as_an_argument_never_reaches_an_argv(call):
    with pytest.raises(ValueError):
        call()


def test_the_reread_and_every_evidence_read_is_pinned_to_the_issues_repo():
    for argv in (
        github.argv_reread("IronbellyGroup/example", 7),
        github.argv_issue_updated("IronbellyGroup/example", 7),
        github.argv_issue_labels("IronbellyGroup/example", 7),
        github.argv_develop_list("IronbellyGroup/example", 7),
        github.argv_branch_date("IronbellyGroup/example", "feat/x"),
        github.argv_timeline("IronbellyGroup/example", 7),
    ):
        assert "IronbellyGroup/example" in " ".join(argv)
        assert "IronbellyOrg" not in " ".join(argv)


def test_the_only_delete_is_the_hold_label_of_one_issue():
    deletes = [
        argv
        for argv in (
            github.argv_label_get("o/r"),
            github.argv_label_create("o/r"),
            github.argv_label_add("o/r", 3),
            github.argv_label_remove("o/r", 3),
        )
        if "DELETE" in argv
    ]
    assert deletes == [
        ["gh", "api", "--method", "DELETE", "repos/o/r/issues/3/labels/hold:plan"]
    ]


def test_removed_names_are_gone_from_the_module():
    source = Path(github.__file__).read_text(encoding="utf-8")
    for name in (
        "EVENTS_JQ", "MARKER_JQ", "EDITS_QUERY", "PROJECT_ITEMS_QUERY", "TRIGGER_MAX_CHARS",
        "_trigger_arg", "argv_events", "argv_comments", "argv_edits", "argv_project_items",
        "argv_discover", "def discover", "def events", "def marker_comments", "def edits",
        "def project_items", "_graphql_read", "_errors_kind", "scope_missing", "scope_types",
        "scope_stderr", "issue-watch:",
    ):  # fmt: skip
        assert name not in source, name
    assert not hasattr(github, "REPO")


# --- S1 -----------------------------------------------------------------------------------


def test_search_assigned_reads_the_fixture_shape(fake_runner):
    payload = load_fixture("gh_search_assigned.json")["payload"]
    argv = github.argv_search_assigned("IronbellyOrg", "owner-login")
    runner = fake_runner({tuple(argv): result(stdout=json.dumps(payload))})
    read = github.search_assigned(runner, "IronbellyOrg", "owner-login", tf)
    assert read.reason is None
    (issue,) = read.value
    assert (issue.repo, issue.number, issue.assignees) == (
        "IronbellyOrg/IronClaude",
        101,
        ("owner-login",),
    )
    assert issue.title == "A title" and "## Priority" in issue.body
    assert issue.key == "IronbellyOrg/IronClaude#101"
    assert issue.updated_at == datetime(2026, 11, 19, 10, 0, tzinfo=timezone.utc)


def test_a_result_of_a_hundred_rows_fails_closed_as_truncated(fake_runner):
    argv = tuple(github.argv_search_assigned("IronbellyOrg", "x"))
    many = [row(number=n) for n in range(1, 101)]
    for reply in (search_reply(many), search_reply(many[:3], total=100)):
        read = github.search_assigned(
            fake_runner({argv: reply}), "IronbellyOrg", "x", tf
        )
        assert (read.value, read.reason, read.kind) == (None, "truncated", "truncated")
    ok = github.search_assigned(
        fake_runner({argv: search_reply(many[:99])}), "IronbellyOrg", "x", tf
    )
    assert len(ok.value) == 99


def test_a_row_of_another_org_or_a_pull_request_is_dropped_and_a_repeat_stops(
    fake_runner,
):
    argv = tuple(github.argv_search_assigned("IronbellyOrg", "x"))
    rows = [row(), row(repo="Other/Thing", number=6), row(number=7, pull_request=True)]
    read = github.search_assigned(
        fake_runner({argv: search_reply(rows)}), "IronbellyOrg", "x", tf
    )
    assert [(i.repo, i.number) for i in read.value] == [("IronbellyOrg/IronClaude", 5)]
    dup = github.search_assigned(
        fake_runner({argv: search_reply([row(), row()])}), "IronbellyOrg", "x", tf
    )
    assert (dup.reason, dup.kind) == ("discovery_duplicate", "discovery_duplicate")


@pytest.mark.parametrize(
    "bad",
    [
        search_reply([row()], incomplete=True),
        search_reply([row(repository_url="https://example.com/x")]),
        search_reply([row(number="5")]),
        search_reply([row(number=True)]),
        search_reply([row(updated_at="yesterday")]),
        search_reply([row(assignees="owner-login")]),
        search_reply([row(pull_request=None)]),
        result(stdout='{"total_count": "1", "incomplete_results": false, "items": []}'),
        result(stdout='{"incomplete_results": false}'),
        result(stdout="[]"),
    ],
)
def test_a_reply_of_the_wrong_shape_is_gh_non_json(fake_runner, bad):
    argv = tuple(github.argv_search_assigned("IronbellyOrg", "x"))
    read = github.search_assigned(fake_runner({argv: bad}), "IronbellyOrg", "x", tf)
    assert (read.value, read.reason) == (None, "gh_non_json")


@pytest.mark.parametrize(
    ("reply", "reason"),
    [
        (result(timed_out=True), "gh_timeout"),
        (result(stderr="HTTP 502", returncode=1), "gh_timeout"),
        (result(stderr="HTTP 401: bad credentials", returncode=1), "gh_auth_failed"),
        (result(stderr="HTTP 429 rate limit exceeded", returncode=1), "rate_limited"),
        (
            result(stderr="boom", returncode=1),
            "gh_auth_failed",
        ),  # unknown text: auth until the live test
        (result(stdout="not json"), "gh_non_json"),
    ],
)
def test_a_failed_search_maps_to_a_cycle_reason(fake_runner, reply, reason):
    argv = tuple(github.argv_search_assigned("IronbellyOrg", "x"))
    assert (
        github.search_assigned(
            fake_runner({argv: reply}), "IronbellyOrg", "x", tf
        ).reason
        == reason
    )


def test_a_search_with_no_time_left_starts_no_call(fake_runner):
    runner = fake_runner()
    read = github.search_assigned(runner, "IronbellyOrg", "x", lambda: None)
    assert read.reason == "gh_timeout" and runner.calls == []


# --- S2 to S4 -------------------------------------------------------------------------------


def test_search_info_reads_rows_and_marks_a_pull_request(fake_runner):
    payload = load_fixture("gh_search_info.json")["payload"]
    payload["items"].append(dict(payload["items"][0], number=13, pull_request=True))
    payload["items"].append(
        dict(payload["items"][0], repository_url="https://api.github.com/repos/Other/x")
    )
    argv = tuple(github.argv_search_info("mentions", "IronbellyGroup", "x", SINCE))
    read = github.search_info(
        fake_runner({argv: result(stdout=json.dumps(payload))}),
        "mentions", "IronbellyGroup", "x", SINCE, tf,
    )  # fmt: skip
    assert [(i.repo, i.number, i.kind) for i in read.value] == [
        ("IronbellyGroup/example", 12, "issue"),
        ("IronbellyGroup/example", 13, "pull_request"),
    ]
    assert (
        read.value[0].seen_key
        == "mentions IronbellyGroup/example#12 2026-11-19T10:12:41Z"
    )


def test_search_info_is_cut_at_a_hundred_and_never_fails_for_size(fake_runner):
    argv = tuple(github.argv_search_info("affects", "IronbellyOrg", "x", SINCE))
    items = [
        {"repository_url": "https://api.github.com/repos/IronbellyOrg/r", "number": n,
         "updated_at": "2026-11-19T10:00:00Z", "pull_request": False}
        for n in range(1, 151)
    ]  # fmt: skip
    read = github.search_info(
        fake_runner({argv: search_reply(items)}),
        "affects",
        "IronbellyOrg",
        "x",
        SINCE,
        tf,
    )
    assert read.reason is None and len(read.value) == github.DISCOVERY_BOUND


def test_search_info_incomplete_results_is_a_malformed_reply(fake_runner):
    argv = tuple(github.argv_search_info("mentions", "IronbellyOrg", "x", SINCE))
    read = github.search_info(
        fake_runner({argv: search_reply([], incomplete=True)}),
        "mentions", "IronbellyOrg", "x", SINCE, tf,
    )  # fmt: skip
    assert read.reason == "gh_non_json"


# --- the re-read and the small reads ------------------------------------------------------------


def test_reread_gives_a_snapshot_with_the_body_and_checks_the_number(fake_runner):
    budget = CallBudget()
    payload = load_fixture("gh_issue_reread.json")["payload"]
    argv = tuple(github.argv_reread("IronbellyOrg/IronClaude", 101))
    runner = fake_runner({argv: result(stdout=json.dumps(payload))})
    snap = github.reread(runner, budget, "IronbellyOrg/IronClaude", 101, tf).value
    assert (snap.repo, snap.number, snap.state, snap.assignees) == (
        "IronbellyOrg/IronClaude",
        101,
        "open",
        ("owner-login",),
    )
    assert "## Fix approach" in snap.body
    argv2 = tuple(github.argv_reread("IronbellyOrg/IronClaude", 102))
    other = github.reread(
        fake_runner({argv2: result(stdout=json.dumps(payload))}),
        budget, "IronbellyOrg/IronClaude", 102, tf,
    )  # fmt: skip
    assert (other.reason, other.kind) == (
        "revalidation_failed",
        "non_json",
    )  # another number


@pytest.mark.parametrize(
    ("reply", "reason"),
    [
        (result(timed_out=True), "revalidation_transient"),
        (result(stderr="HTTP 503", returncode=1), "revalidation_transient"),
        (result(stderr="HTTP 404", returncode=1), "revalidation_failed"),
    ],
)
def test_reread_failures_are_transient_or_failed(fake_runner, reply, reason):
    argv = tuple(github.argv_reread("o/r", 5))
    assert (
        github.reread(fake_runner({argv: reply}), CallBudget(), "o/r", 5, tf).reason
        == reason
    )


def test_the_reread_uses_a_reserved_call_and_stops_when_the_budget_is_spent(
    fake_runner,
):
    budget = CallBudget()
    budget.calls = github.CALL_CAP  # every call is spent, the reserved ones too
    read = github.reread(fake_runner(), budget, "o/r", 5, tf)
    assert (read.reason, read.kind) == ("budget_exhausted", "budget_exhausted")


def test_updated_at_and_labels_reads(fake_runner):
    budget = CallBudget()
    updated = load_fixture("gh_issue_view_updated.json")["payload"]
    labels = load_fixture("gh_issue_view_labels.json")["payload"]
    runner = fake_runner(
        {
            tuple(github.argv_issue_updated("o/r", 5)): result(
                stdout=json.dumps(updated)
            ),
            tuple(github.argv_issue_labels("o/r", 5)): result(
                stdout=json.dumps(labels)
            ),
        }
    )
    got = github.issue_updated_at(runner, budget, "o/r", 5, tf).value
    assert got == datetime(2026, 11, 19, 10, 0, 5, tzinfo=timezone.utc)
    assert github.issue_labels(runner, budget, "o/r", 5, tf).value == ("hold:plan",)
    for reply in (result(stdout="{}"), result(stdout='{"updatedAt": 5}')):
        bad = fake_runner({tuple(github.argv_issue_updated("o/r", 5)): reply})
        assert (
            github.issue_updated_at(bad, budget, "o/r", 5, tf).reason
            == "hold_write_failed"
        )


# --- the evidence reads (E2, E3) -------------------------------------------------------------------


def test_linked_branches_reads_text_lines_and_ignores_what_is_not_a_branch(fake_runner):
    argv = tuple(github.argv_develop_list("o/r", 5))
    text = (
        load_fixture("gh_issue_develop_list.json")["stdout"]
        + "No branches found\n--evil\n\n"
    )
    read = github.linked_branches(
        fake_runner({argv: result(stdout=text)}), CallBudget(), "o/r", 5, tf
    )
    assert read.value == ("issue-655-x",)
    empty = github.linked_branches(
        fake_runner({argv: result(stdout="")}), CallBudget(), "o/r", 5, tf
    )
    assert empty.value == ()
    down = github.linked_branches(
        fake_runner({argv: result(returncode=1, stderr="HTTP 502")}),
        CallBudget(),
        "o/r",
        5,
        tf,
    )
    assert down.reason == "hold_write_failed"


def test_branch_date_and_timeline_evidence(fake_runner):
    budget = CallBudget()
    date = load_fixture("gh_branch_date.json")["payload"]
    timeline = load_fixture("gh_timeline_evidence.json")["payload"]
    runner = fake_runner(
        {
            tuple(github.argv_branch_date("o/r", "feat/x")): result(
                stdout=json.dumps(date)
            ),
            tuple(github.argv_timeline("o/r", 5)): result(stdout=json.dumps(timeline)),
        }
    )
    assert github.branch_date(runner, budget, "o/r", "feat/x", tf).value == datetime(
        2026, 11, 19, 10, 30, tzinfo=timezone.utc
    )
    assert github.timeline_evidence(runner, budget, "o/r", 5, tf).value == datetime(
        2026, 11, 19, 10, 41, tzinfo=timezone.utc
    )
    quiet = fake_runner({tuple(github.argv_timeline("o/r", 5)): result(stdout="[]")})
    assert github.timeline_evidence(quiet, budget, "o/r", 5, tf).value is None
    # a cross-reference that is not a pull request is not plan work
    only_issue = [
        {
            "event": "cross-referenced",
            "created_at": "2026-11-19T10:00:00Z",
            "pull_request": False,
        }
    ]
    noisy = fake_runner(
        {tuple(github.argv_timeline("o/r", 5)): result(stdout=json.dumps(only_issue))}
    )
    assert github.timeline_evidence(noisy, budget, "o/r", 5, tf).value is None


# --- the label writer -----------------------------------------------------------------------------------


def test_the_label_writer_reads_creates_when_absent_adds_and_removes(fake_runner):
    runner = fake_runner(
        {
            tuple(github.argv_label_get("o/r")): result(
                stderr="gh: Not Found (HTTP 404)", returncode=1
            ),
            tuple(github.argv_label_create("o/r")): result(
                stdout='{"name":"hold:plan"}'
            ),
            tuple(github.argv_label_add("o/r", 5)): result(
                stdout='[{"name":"hold:plan"}]'
            ),
            tuple(github.argv_label_remove("o/r", 5)): result(stdout="[]"),
        }
    )
    writer, budget = LabelWriter(runner), CallBudget()
    assert writer.ensure(budget, "o/r", tf).reason is None
    assert writer.add(budget, "o/r", 5, tf).value is True
    assert writer.remove(budget, "o/r", 5, tf).value is True
    assert runner.argvs() == [
        tuple(github.argv_label_get("o/r")),
        tuple(github.argv_label_create("o/r")),
        tuple(github.argv_label_add("o/r", 5)),
        tuple(github.argv_label_remove("o/r", 5)),
    ]
    writer.ensure(
        budget, "o/r", tf
    )  # remembered for the rest of the cycle: no second read
    assert len(runner.calls) == 4


def test_an_existing_label_is_not_created_again(fake_runner):
    runner = fake_runner(
        {tuple(github.argv_label_get("o/r")): result(stdout='{"name":"hold:plan"}')}
    )
    assert LabelWriter(runner).ensure(CallBudget(), "o/r", tf).reason is None
    assert len(runner.calls) == 1


@pytest.mark.parametrize(
    "reply",
    [
        result(stderr="HTTP 403: Resource not accessible", returncode=1),
        result(stderr="HTTP 422: Validation failed", returncode=1),
        result(timed_out=True),
    ],
)
def test_a_refused_creation_a_403_or_a_timeout_is_hold_write_failed(fake_runner, reply):
    runner = fake_runner(
        {
            tuple(github.argv_label_get("o/r")): result(
                stderr="HTTP 404", returncode=1
            ),
            tuple(github.argv_label_create("o/r")): reply,
            tuple(github.argv_label_add("o/r", 5)): reply,
            tuple(github.argv_label_remove("o/r", 5)): reply,
        }
    )
    writer, budget = LabelWriter(runner), CallBudget()
    assert writer.ensure(budget, "o/r", tf).reason == "hold_write_failed"
    assert writer.add(budget, "o/r", 5, tf).reason == "hold_write_failed"
    assert writer.remove(budget, "o/r", 5, tf).reason == "hold_write_failed"


def test_a_label_that_is_already_gone_is_a_done_removal_and_a_rate_limit_is_a_kind(
    fake_runner,
):
    runner = fake_runner(
        {
            tuple(github.argv_label_remove("o/r", 5)): result(
                stderr="Label does not exist (HTTP 404)", returncode=1
            ),
            tuple(github.argv_label_add("o/r", 5)): result(
                stderr="HTTP 429 rate limit", returncode=1
            ),
        }
    )
    writer = LabelWriter(runner)
    assert writer.remove(CallBudget(), "o/r", 5, tf).value is True
    limited = writer.add(CallBudget(), "o/r", 5, tf)
    assert (limited.reason, limited.kind) == ("hold_write_failed", "rate_limited")


def test_the_injected_guard_can_refuse_any_argv_and_the_call_is_not_run(fake_runner):
    runner = fake_runner()
    seen: list[list[str]] = []

    def guard(argv: list[str]) -> str | None:
        seen.append(argv)
        return "refused" if "DELETE" in argv else None

    writer = LabelWriter(runner, guard)
    read = writer.remove(CallBudget(), "o/r", 5, tf)
    assert read.reason == "hold_write_failed" and runner.calls == []
    assert seen == [github.argv_label_remove("o/r", 5)]


def test_the_writer_makes_no_comment_call_of_any_kind(fake_runner):
    runner = fake_runner(
        {
            tuple(github.argv_label_get("o/r")): result(
                stderr="HTTP 404", returncode=1
            ),
            tuple(github.argv_label_create("o/r")): result(stdout="{}"),
            tuple(github.argv_label_add("o/r", 5)): result(stdout="[]"),
            tuple(github.argv_label_remove("o/r", 5)): result(stdout="[]"),
        }
    )
    writer, budget = LabelWriter(runner), CallBudget()
    writer.ensure(budget, "o/r", tf)
    writer.add(budget, "o/r", 5, tf)
    writer.remove(budget, "o/r", 5, tf)
    text = " ".join(" ".join(a) for a in runner.argvs())
    assert "comment" not in text and "PATCH" not in text and "issue edit" not in text


# --- kept machinery (classification, rate limits, budget) --------------------------------------------


def test_classify_maps_the_kept_signs():
    assert github.classify(result(timed_out=True)).kind == "timeout"
    assert github.classify(result(stdout="{}")).kind == "ok"
    assert github.classify(result(stdout="x")).kind == "non_json"
    assert (
        github.classify(result(stderr="HTTP 401", returncode=1)).kind == "auth_failed"
    )
    assert (
        github.classify(result(stderr="HTTP 403 rate limit", returncode=1)).kind
        == "rate_limited"
    )
    assert github.classify(result(stderr="HTTP 500", returncode=1)).kind == "transient"
    assert github.classify(result(stderr="HTTP 404", returncode=1)).kind == "failed"
    assert set(github.GH_ERROR_SIGNS) == {
        "auth_stderr",
        "rate_status_stderr",
        "rate_text_stderr",
        "transient_stderr_re",
    }


def test_rate_limit_wait_reads_headers_and_clamps_the_rest():
    headed = result(
        stdout="HTTP/2 429\nRetry-After: 60\n\n{}", stderr="HTTP 429 rate limit", returncode=1,
        argv=tuple(github.argv_user()),
    )  # fmt: skip
    assert github.rate_limit_wait(headed, NOW) == (
        NOW + timedelta(seconds=60),
        "rate_limited",
    )
    bare = result(
        stderr="HTTP 429 rate limit", returncode=1, argv=tuple(github.argv_user())
    )
    assert github.rate_limit_wait(bare, NOW) == (
        NOW + timedelta(seconds=3600),
        "rate_limit_clamped",
    )


def test_the_budget_keeps_the_last_calls_for_the_reread():
    assert github.RESERVED_CALLS == 12 == 10 + 2  # MAX_CANDIDATES plus 2 (4.6)
    budget = CallBudget()
    spent = 0
    while budget.spend():
        spent += 1
    assert spent == github.CALL_CAP - github.RESERVED_CALLS
    assert budget.spend(reserved=True)
    budget.spend_shared()
    assert budget.total == spent + 2


def test_rest_read_pages_and_drops_items():
    """``_rest_read`` is kept as it is (design 4.10); it has no production caller now."""
    pages = {
        1: result(stdout=json.dumps([{"id": i} for i in range(1, 101)])),
        2: result(stdout=json.dumps([{"id": 101}])),
    }
    runner = FakeRunner()
    calls: list[int] = []

    def argv_for(page: int) -> list[str]:
        calls.append(page)
        argv = ["gh", "page", str(page)]
        runner.script[tuple(argv)] = pages[page]
        return argv

    read = github._rest_read(
        runner, CallBudget(), tf, argv_for,
        lambda d: None if d["id"] == 2 else d["id"], "unreadable", "incomplete", False,
    )  # fmt: skip
    assert calls == [1, 2] and len(read.value) == 100
