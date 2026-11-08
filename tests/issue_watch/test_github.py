"""Tests for ``github.py`` of the issue watcher, part A.

Part A covers the argv builders G1 to G7 (design 8.1), the jq and GraphQL
constants, ``classify`` (design 8.2), the rate-limit time (design 8.3, DF-35)
and the ``_assumed_shape`` fixtures (DF-32). Every expected argv is written out
literally; no case runs a real command.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import github
from superclaude.cli.issue_watch.predicates import (
    CLAIM_MARKER,
    CommentEdit,
    DiscoveredIssue,
    EditEvidence,
    IssueSnapshot,
    LabelEvent,
    Login,
    MarkerEvidence,
    ProjectItem,
    approval_of,
)

from .conftest import result

FIXTURES = Path(__file__).parent / "fixtures" / "_assumed_shape"
NOW = datetime(2026, 11, 7, 12, 0, 0, tzinfo=timezone.utc)
G1_ARGV = ("gh", "api", "user", "--include")
EVENTS_JQ = (
    "[.[] | {id, event, label: .label.name, actor_id: .actor.id, "
    "actor_login: .actor.login, actor_type: .actor.type, created_at}]"
)
MARKER_JQ = (
    "[.[] | {id, login: .user.login, created_at, updated_at, "
    'marker: (.body | contains("<!-- sc:issue:claim -->"))}]'
)
REREAD_JQ = "{number, state, labels: [.labels[].name], assignees: [.assignees[].login]}"

# The two GraphQL drafts, written out literally (plan step 3.6): a change to the
# page size, a field name or the paging block in github.py must fail a test.
EDITS_QUERY = """query($number: Int!, $after: String) {
  repository(owner: "IronbellyOrg", name: "IronClaude") {
    issue(number: $number) {
      createdAt
      lastEditedAt
      comments(first: 100, after: $after) {
        nodes { databaseId author { login } createdAt lastEditedAt }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}"""
PROJECT_ITEMS_QUERY = """query($number: Int!, $after: String) {
  repository(owner: "IronbellyOrg", name: "IronClaude") {
    issue(number: $number) {
      projectItems(first: 100, after: $after) {
        nodes {
          isArchived
          project { id }
          fieldValueByName(name: "Status") {
            ... on ProjectV2ItemFieldSingleSelectValue { name }
          }
        }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}"""


def load(name: str) -> dict:
    """Return one ``_assumed_shape`` fixture as a dict."""
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def fail(
    stderr: str, *, stdout: str = "", returncode: int = 1, argv: tuple[str, ...] = ()
):
    """A non-zero ``gh`` result."""
    return result(stdout=stdout, stderr=stderr, returncode=returncode, argv=argv)


def g1_result(headers: list[str], argv: tuple[str, ...] = G1_ARGV):
    """A G1 result: status line, ``headers``, a blank line, then a JSON body.

    [UNVERIFIED, assumed shape] design 835 (the ``--include`` layout) and 838
    (``Retry-After``, ``x-ratelimit-reset``); the captured-layout twin is the
    fixture ``gh_api_user_include_429.json``. FU-1 replaces both.
    """
    head = "".join(f"{h}\n" for h in headers)
    stdout = f"HTTP/2.0 429 Too Many Requests\n{head}\n{{}}\n"
    return result(stdout=stdout, returncode=1, argv=argv)


def all_argvs() -> list[list[str]]:
    """Every argv the builders can make, with and without a cursor, every page."""
    argvs = [
        github.argv_user(),
        github.argv_discover("sc:issue", "owner-login"),
        github.argv_reread(42),
    ]
    for page in range(1, 6):
        argvs.append(github.argv_events(42, page))
        argvs.append(github.argv_comments(42, page))
    for after in (None, "Y3Vyc29yOjE="):
        argvs.append(github.argv_edits(42, after))
        argvs.append(github.argv_project_items(42, after))
    return argvs


# --- argv G1 to G7 (design 8.1) ------------------------------------------------


def test_g1_argv_is_literal__fr002() -> None:
    assert github.argv_user() == ["gh", "api", "user", "--include"]


def test_g2_argv_is_the_fr003_literal__fr003() -> None:
    assert github.argv_discover("sc:issue", "owner-login") == [
        "gh",
        "issue",
        "list",
        "--repo",
        "IronbellyOrg/IronClaude",
        "--state",
        "open",
        "--label",
        "sc:issue",
        "--assignee",
        "owner-login",
        "--json",
        "number,labels,assignees,state",
        "-L",
        "100",
    ]


def test_g3_argv_is_literal__fr005_fr006() -> None:
    assert github.argv_events(42, 2) == [
        "gh",
        "api",
        "--method",
        "GET",
        "repos/IronbellyOrg/IronClaude/issues/42/events",
        "-F",
        "per_page=100",
        "-F",
        "page=2",
        "--jq",
        EVENTS_JQ,
    ]


def test_g4_argv_is_literal__fr009() -> None:
    assert github.argv_comments(7, 1) == [
        "gh",
        "api",
        "--method",
        "GET",
        "repos/IronbellyOrg/IronClaude/issues/7/comments",
        "-F",
        "per_page=100",
        "-F",
        "page=1",
        "--jq",
        MARKER_JQ,
    ]


def test_g5_argv_first_page_has_no_cursor__fr003() -> None:
    assert github.argv_edits(42) == [
        "gh",
        "api",
        "graphql",
        "-f",
        f"query={EDITS_QUERY}",
        "-F",
        "number=42",
    ]


def test_g5_argv_later_page_adds_the_cursor() -> None:
    assert github.argv_edits(42, "Y3Vyc29yOjE=") == [
        "gh",
        "api",
        "graphql",
        "-f",
        f"query={EDITS_QUERY}",
        "-F",
        "number=42",
        "-f",
        "after=Y3Vyc29yOjE=",
    ]


def test_g6_argv_first_page_has_no_cursor__fr007() -> None:
    assert github.argv_project_items(42) == [
        "gh",
        "api",
        "graphql",
        "-f",
        f"query={PROJECT_ITEMS_QUERY}",
        "-F",
        "number=42",
    ]


def test_g6_argv_later_page_adds_the_cursor__fr007() -> None:
    assert github.argv_project_items(42, "Y3Vyc29yOjI=") == [
        "gh",
        "api",
        "graphql",
        "-f",
        f"query={PROJECT_ITEMS_QUERY}",
        "-F",
        "number=42",
        "-f",
        "after=Y3Vyc29yOjI=",
    ]


def test_g7_argv_is_literal__fr011() -> None:
    assert github.argv_reread(42) == [
        "gh",
        "api",
        "--method",
        "GET",
        "repos/IronbellyOrg/IronClaude/issues/42",
        "--jq",
        REREAD_JQ,
    ]


def test_every_gh_api_argv_but_g1_and_graphql_has_method_get() -> None:
    """Design line 554 and DF-28: REST path calls carry ``--method GET``."""
    checked = 0
    for argv in all_argvs():
        if argv[1] != "api" or argv == list(G1_ARGV) or argv[2] == "graphql":
            continue
        checked += 1
        i = argv.index("--method")
        assert argv[i + 1] == "GET"
    assert checked == 11  # 5 events pages, 5 comments pages, one re-read


def test_no_graphql_argv_has_method() -> None:
    """GraphQL is POST by design (DF-28): no ``--method`` anywhere in it."""
    graphql = [a for a in all_argvs() if a[1] == "api" and a[2] == "graphql"]
    assert len(graphql) == 4
    assert all("--method" not in a for a in graphql)


# --- constants -----------------------------------------------------------------


@pytest.mark.parametrize("query", [github.EDITS_QUERY, github.PROJECT_ITEMS_QUERY])
def test_graphql_constants_name_the_repo_and_never_mutate(query: str) -> None:
    assert 'owner: "IronbellyOrg", name: "IronClaude"' in query
    assert "mutation" not in query.lower()
    assert "$after: String" in query
    assert "$after: String!" not in query
    assert re.search(r"\$after: String(?!!)", query)


def test_graphql_constants_equal_the_literal_drafts__df14() -> None:
    assert github.EDITS_QUERY == EDITS_QUERY
    assert github.PROJECT_ITEMS_QUERY == PROJECT_ITEMS_QUERY


@pytest.mark.parametrize(
    ("query", "tokens"),
    [
        (
            github.EDITS_QUERY,
            [
                "comments(first: 100, after: $after)",
                "createdAt",
                "lastEditedAt",
                "databaseId",
                "author { login }",
                "pageInfo { hasNextPage endCursor }",
            ],
        ),
        (
            github.PROJECT_ITEMS_QUERY,
            [
                "projectItems(first: 100, after: $after)",
                "isArchived",
                "project { id }",
                'fieldValueByName(name: "Status")',
                "ProjectV2ItemFieldSingleSelectValue { name }",
                "pageInfo { hasNextPage endCursor }",
            ],
        ),
    ],
    ids=["G5", "G6"],
)
def test_graphql_query_asks_for_what_the_parsers_read__df14(
    query: str, tokens: list[str]
) -> None:
    """DF-14: page size 100 and every field ``github.py`` parses must be requested."""
    for token in tokens:
        assert token in query, token


def test_repo_and_caps_are_literal() -> None:
    assert github.REPO == "IronbellyOrg/IronClaude"
    assert github.PAGE_SIZE == 100
    assert github.PAGE_CAP == 5


def test_marker_jq_embeds_the_claim_marker__fr009() -> None:
    assert CLAIM_MARKER in github.MARKER_JQ
    assert github.MARKER_JQ == MARKER_JQ


def test_events_jq_equals_the_design_projection__fr005_fr006() -> None:
    assert github.EVENTS_JQ == EVENTS_JQ


def test_reread_jq_equals_the_design_projection__fr011() -> None:
    assert github.REREAD_JQ == REREAD_JQ


def test_no_argv_requests_title_or_body_as_an_output_field__fr003_nfr002() -> None:
    """Design line 556: the only body access is ``contains(<marker>)`` in G4."""
    contains_marker = "(.body | contains(" + json.dumps(CLAIM_MARKER) + "))"
    assert github.MARKER_JQ.count("body") == 1
    assert contains_marker in github.MARKER_JQ
    for argv in all_argvs():
        for element in argv:
            assert "title" not in element
            if element != github.MARKER_JQ:
                assert "body" not in element
    g4 = github.argv_comments(42, 1)
    assert g4[g4.index("--jq") + 1] == github.MARKER_JQ


def test_no_argv_names_the_upstream_or_a_placeholder() -> None:
    for argv in all_argvs():
        for element in argv:
            assert "SuperClaude-Org" not in element
            assert "{owner}" not in element
            assert "{repo}" not in element


@pytest.mark.parametrize("bad", [0, -1, True, "42", None, 1.0])
def test_bad_issue_number_never_reaches_an_argv(bad: object) -> None:
    with pytest.raises(ValueError):
        github.argv_reread(bad)  # type: ignore[arg-type]


@pytest.mark.parametrize("page", [0, 6, True, "1"])
def test_bad_page_never_reaches_an_argv(page: object) -> None:
    with pytest.raises(ValueError):
        github.argv_events(42, page)  # type: ignore[arg-type]


# --- classify (design 8.2) -----------------------------------------------------


def test_classify_timeout() -> None:
    reply = github.classify(result(timed_out=True))
    assert reply.kind == "timeout"
    assert reply.payload is None


def test_classify_ok_parses_the_json() -> None:
    reply = github.classify(result(stdout='[{"number": 1}]'))
    assert reply.kind == "ok"
    assert reply.payload == [{"number": 1}]


def test_classify_exit_zero_with_text_is_non_json() -> None:
    assert github.classify(result(stdout="not json")).kind == "non_json"
    assert github.classify(result(stdout="")).kind == "non_json"


def test_classify_g1_is_parsed_after_the_header_block__fr002() -> None:
    fixture = load("gh_api_user_include.json")
    reply = github.classify(
        result(stdout=fixture["raw"], argv=G1_ARGV), include_headers=True
    )
    assert reply.kind == "ok"
    assert reply.payload == {"login": "owner-login", "id": 1001}


def test_classify_g1_without_a_header_block_is_non_json__fr002() -> None:
    reply = github.classify(
        result(stdout='{"login": "x", "id": 1}', argv=G1_ARGV), include_headers=True
    )
    assert reply.kind == "non_json"


def test_classify_auth_failed_from_the_401_fixture() -> None:
    fixture = load("gh_stderr_auth_401.json")
    reply = github.classify(fail(fixture["stderr"], returncode=fixture["exit"]))
    assert reply.kind == "auth_failed"


def test_classify_auth_failed_from_gh_auth_login_alone() -> None:
    reply = github.classify(fail("To get started with GitHub CLI, run: gh auth login"))
    assert reply.kind == "auth_failed"


@pytest.mark.parametrize(
    "stdout, stderr",
    [
        (
            json.dumps(load("gh_graphql_insufficient_scopes.json")["payload"]),
            "gh: exit status 1",
        ),
        ("", load("gh_stderr_scope_read_project.json")["stderr"]),
    ],
    ids=["graphql-fixture", "stderr-read-project"],
)
def test_classify_scope_missing(stdout: str, stderr: str) -> None:
    assert github.classify(fail(stderr, stdout=stdout)).kind == "scope_missing"


@pytest.mark.parametrize(
    "stdout, stderr",
    [
        ("", load("gh_stderr_rate_403.json")["stderr"]),
        ("", load("gh_stderr_rate_429.json")["stderr"]),
        ("", "gh: HTTP 403: Secondary RATE LIMIT hit"),
        (
            json.dumps(load("gh_graphql_rate_limited.json")["payload"]),
            "gh: exit status 1",
        ),
    ],
    ids=["403-fixture", "429-fixture", "case-insensitive", "graphql-fixture"],
)
def test_classify_rate_limited__fr028(stdout: str, stderr: str) -> None:
    assert github.classify(fail(stderr, stdout=stdout)).kind == "rate_limited"


def test_classify_403_without_rate_limit_text_is_failed() -> None:
    assert github.classify(fail("gh: HTTP 403: Resource not accessible")).kind == (
        "failed"
    )


def test_classify_transient_for_http_502() -> None:
    fixture = load("gh_stderr_http_502.json")
    reply = github.classify(fail(fixture["stderr"], returncode=fixture["exit"]))
    assert reply.kind == "transient"


# [UNVERIFIED, assumed shape] The inline stderr strings in the classify tests
# below stand in for gh text that design 838 / DF-37 mark as unverified; the
# captured-text twins are the ``gh_stderr_*.json`` fixtures. FU-1 replaces both.
@pytest.mark.parametrize(
    "stderr", ["gh: something else went wrong", "", "gh: HTTP 404: Not Found"]
)
def test_classify_anything_else_is_failed(stderr: str) -> None:
    assert github.classify(fail(stderr)).kind == "failed"


def test_classify_spawn_error_is_failed() -> None:
    assert github.classify(result(spawn_error="FileNotFoundError")).kind == "failed"


def test_classify_gh_error_signs_table_is_the_one_place() -> None:
    assert set(github.GH_ERROR_SIGNS) == {
        "auth_stderr",
        "scope_types",
        "scope_stderr",
        "rate_status_stderr",
        "rate_text_stderr",
        "rate_types",
        "transient_stderr_re",
    }


# --- rate-limit time (design 8.3, DF-35) ---------------------------------------


def test_retry_after_reads_the_g1_header__fr028() -> None:
    assert github.retry_after(g1_result(["Retry-After: 120"])) == 120


def test_retry_after_is_none_when_absent_or_unparseable__fr028() -> None:
    assert github.retry_after(g1_result([])) is None
    assert github.retry_after(g1_result(["Retry-After: soon"])) is None
    assert github.retry_after(g1_result(["Retry-After: -5"])) is None


def test_retry_after_is_none_for_a_call_without_include__fr028() -> None:
    other = g1_result(["Retry-After: 120"], argv=("gh", "api", "user"))
    assert github.retry_after(other) is None


EPOCH = int(NOW.timestamp())


@pytest.mark.parametrize(
    "headers, seconds, reason",
    [
        (["Retry-After: 120"], 120, "rate_limited"),
        (["Retry-After: 1"], 1, "rate_limited"),
        (["Retry-After: 3600"], 3600, "rate_limited"),
        (["Retry-After: 3601"], 3600, "rate_limit_clamped"),
        (["Retry-After: 0"], 3600, "rate_limit_clamped"),
        ([], 3600, "rate_limit_clamped"),
        (["Retry-After: soon"], 3600, "rate_limit_clamped"),
        (["Retry-After: Wed, 21 Oct 2026 07:28:00 GMT"], 3600, "rate_limit_clamped"),
        ([f"x-ratelimit-reset: {EPOCH + 1800}"], 1800, "rate_limited"),
        ([f"X-RateLimit-Reset: {EPOCH + 3600}"], 3600, "rate_limited"),
        ([f"x-ratelimit-reset: {EPOCH + 3601}"], 3600, "rate_limit_clamped"),
        ([f"x-ratelimit-reset: {EPOCH - 10}"], 3600, "rate_limit_clamped"),
        (["x-ratelimit-reset: tomorrow"], 3600, "rate_limit_clamped"),
        (["Retry-After: 60", f"x-ratelimit-reset: {EPOCH + 1800}"], 60, "rate_limited"),
    ],
)
def test_rate_limit_wait_rows__fr028(
    headers: list[str], seconds: int, reason: str
) -> None:
    when, why = github.rate_limit_wait(g1_result(headers), NOW)
    assert when == NOW + timedelta(seconds=seconds)
    assert when.tzinfo is not None
    assert why == reason


def test_rate_limit_wait_clamps_a_call_without_include__fr028() -> None:
    """Absent is clamped: only G1 carries headers (design 8.3)."""
    other = g1_result(
        ["Retry-After: 120"], argv=("gh", "api", "--method", "GET", "repos/x")
    )
    assert github.rate_limit_wait(other, NOW) == (
        NOW + timedelta(seconds=3600),
        "rate_limit_clamped",
    )


# --- the Date header and the G1 header parse -----------------------------------


def test_date_header_parses_the_fixture() -> None:
    fixture = load("gh_api_user_include.json")
    parsed = github.date_header(result(stdout=fixture["raw"], argv=G1_ARGV))
    assert parsed == datetime(2026, 11, 7, 12, 0, 0, tzinfo=timezone.utc)


def test_date_header_is_none_when_absent_unparseable_or_not_g1() -> None:
    assert github.date_header(g1_result([])) is None
    assert github.date_header(g1_result(["Date: not a date"])) is None
    fixture = load("gh_api_user_include.json")
    no_include = result(stdout=fixture["raw"], argv=("gh", "api", "user"))
    assert github.date_header(no_include) is None


def test_user_reads_login_id_and_date_from_the_g1_fixture__fr002(fake_runner) -> None:
    fixture = load("gh_api_user_include.json")
    runner = fake_runner({G1_ARGV: result(stdout=fixture["raw"], argv=G1_ARGV)})
    read = github.user(runner, lambda: 30.0)
    assert read.reason is None
    assert read.value == Login(
        "owner-login", 1001, datetime(2026, 11, 7, 12, 0, 0, tzinfo=timezone.utc)
    )
    assert runner.calls == [(G1_ARGV, None)]


# --- fixtures (DF-32) ----------------------------------------------------------


def test_every_assumed_shape_fixture_parses_and_is_labelled() -> None:
    """Stands in for the check-json hook that is not installed locally."""
    files = sorted(FIXTURES.glob("*.json"))
    assert len(files) == 19
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["_assumed_shape"] is True, path.name
        assert isinstance(data["source"], str) and data["source"], path.name


def test_every_assumed_shape_fixture_is_read_by_a_test__df32() -> None:
    """A fixture no test reads pins nothing, so FU-1 could not detect a wrong shape.

    This test names no fixture itself, so a file is found only if some test file
    of the suite loads it by name.
    """
    source = "\n".join(
        p.read_text(encoding="utf-8")
        for p in sorted(Path(__file__).parent.glob("test_*.py"))
    )
    for path in sorted(FIXTURES.glob("*.json")):
        assert f'"{path.name}"' in source, f"no test reads {path.name}"


# ==============================================================================
# Part B: paging, null rules, discovery and the call budget (design 8.2, DF-02,
# DF-18, DF-19). Every scripted argv is the literal builder output.
# ==============================================================================

STAMP = "2026-11-07T10:00:00Z"
STAMPED = datetime(2026, 11, 7, 10, 0, 0, tzinfo=timezone.utc)


def timeout() -> float:
    """A ``timeout_for`` that always allows the next call."""
    return 30.0


def ok(payload: object, argv: tuple[str, ...] = ()):
    """An exit-0 ``gh`` result whose stdout is ``payload`` as JSON."""
    return result(stdout=json.dumps(payload), argv=argv)


def event_item(i: int, event: str = "labeled", **over: object) -> dict:
    """One projected G3 item; ``over`` replaces fields.

    [UNVERIFIED, assumed shape] design 836; twin: ``rest_events_page.json``.
    """
    item: dict = {
        "id": i,
        "event": event,
        "label": "sc:issue",
        "actor_id": 1001,
        "actor_login": "owner-login",
        "actor_type": "User",
        "created_at": STAMP,
    }
    item.update(over)
    return item


def marker_item(i: int, **over: object) -> dict:
    """One projected G4 item; ``over`` replaces fields.

    [UNVERIFIED, assumed shape] design 546; twin: ``rest_comments_marker.json``.
    """
    item: dict = {
        "id": i,
        "login": "owner-login",
        "created_at": STAMP,
        "updated_at": STAMP,
        "marker": False,
    }
    item.update(over)
    return item


def full_page(item, page: int) -> list[dict]:
    """100 items with ids that no other full page shares."""
    return [item(i) for i in range((page - 1) * 100 + 1, page * 100 + 1)]


def page_script(argv_for, pages: list[list[dict]]) -> dict:
    """Script page ``p`` of issue 42 to the JSON of ``pages[p - 1]``."""
    script = {}
    for page, items in enumerate(pages, start=1):
        argv = tuple(argv_for(42, page))
        script[argv] = ok(items, argv)
    return script


def page_argvs(argv_for, last: int) -> list[tuple[str, ...]]:
    """The literal argvs of pages 1 to ``last`` of issue 42."""
    return [tuple(argv_for(42, page)) for page in range(1, last + 1)]


REST_READS = pytest.mark.parametrize(
    "read, argv_for, item, unreadable, incomplete",
    [
        (
            github.events,
            github.argv_events,
            event_item,
            "events_unreadable",
            "events_incomplete",
        ),
        (
            github.marker_comments,
            github.argv_comments,
            marker_item,
            "marker_unreadable",
            "marker_unreadable",
        ),
    ],
    ids=["events", "marker"],
)


# --- REST paging (design 8.2, DF-19) ---------------------------------------------


@REST_READS
def test_rest_99_items_is_one_complete_call__fr005_fr006_fr009(
    fake_runner, read, argv_for, item, unreadable, incomplete
) -> None:
    runner = fake_runner(page_script(argv_for, [[item(i) for i in range(1, 100)]]))
    budget = github.CallBudget()
    got = read(runner, budget, 42, timeout)
    assert (got.reason, got.kind) == (None, "ok")
    assert len(got.value) == 99
    assert runner.calls == [(page_argvs(argv_for, 1)[0], None)]
    assert budget.calls == 1


@REST_READS
def test_rest_exactly_100_items_fetches_page_2__fr005_fr006_fr009(
    fake_runner, read, argv_for, item, unreadable, incomplete
) -> None:
    pages = [full_page(item, 1), [item(101), item(102)]]
    runner = fake_runner(page_script(argv_for, pages))
    budget = github.CallBudget()
    got = read(runner, budget, 42, timeout)
    assert (got.reason, got.kind) == (None, "ok")
    assert len(got.value) == 102
    assert [call[0] for call in runner.calls] == page_argvs(argv_for, 2)
    assert budget.calls == 2


@REST_READS
def test_rest_101_items_in_one_page_is_unreadable_not_incomplete__df19(
    fake_runner, read, argv_for, item, unreadable, incomplete
) -> None:
    pages = [[item(i) for i in range(1, 102)]]
    runner = fake_runner(page_script(argv_for, pages))
    got = read(runner, github.CallBudget(), 42, timeout)
    assert got.value is None
    assert got.reason == unreadable
    assert got.kind == "non_json"
    assert got.reason != "events_incomplete"
    assert len(runner.calls) == 1


@REST_READS
def test_rest_repeated_id_across_pages_is_incomplete__fr005_fr006_fr009(
    fake_runner, read, argv_for, item, unreadable, incomplete
) -> None:
    pages = [full_page(item, 1), [item(100)]]
    runner = fake_runner(page_script(argv_for, pages))
    got = read(runner, github.CallBudget(), 42, timeout)
    assert got.value is None
    assert (got.reason, got.kind) == (incomplete, "incomplete")
    assert [call[0] for call in runner.calls] == page_argvs(argv_for, 2)


@REST_READS
def test_rest_repeated_id_inside_one_page_is_incomplete__fr005_fr006_fr009(
    fake_runner, read, argv_for, item, unreadable, incomplete
) -> None:
    runner = fake_runner(page_script(argv_for, [[item(1), item(2), item(1)]]))
    got = read(runner, github.CallBudget(), 42, timeout)
    assert got.value is None
    assert (got.reason, got.kind) == (incomplete, "incomplete")


@REST_READS
def test_rest_page_cap_never_fetches_a_sixth_page__fr005_fr006_fr009(
    fake_runner, read, argv_for, item, unreadable, incomplete
) -> None:
    pages = [full_page(item, page) for page in range(1, 6)]
    runner = fake_runner(page_script(argv_for, pages))
    budget = github.CallBudget()
    got = read(runner, budget, 42, timeout)
    assert got.value is None
    assert (got.reason, got.kind) == (incomplete, "incomplete")
    assert [call[0] for call in runner.calls] == page_argvs(argv_for, 5)
    assert budget.calls == 5
    assert github.PAGE_CAP == 5


@REST_READS
def test_rest_refused_budget_mid_paging_makes_no_further_call__nfr009(
    fake_runner, read, argv_for, item, unreadable, incomplete
) -> None:
    runner = fake_runner(page_script(argv_for, [full_page(item, 1)]))
    budget = github.CallBudget()
    for _ in range(github.CALL_CAP - github.RESERVED_CALLS - 1):
        assert budget.spend()
    got = read(runner, budget, 42, timeout)
    assert got.value is None
    assert (got.reason, got.kind) == ("budget_exhausted", "budget_exhausted")
    assert [call[0] for call in runner.calls] == page_argvs(argv_for, 1)
    assert budget.calls == github.CALL_CAP - github.RESERVED_CALLS


@REST_READS
def test_rest_timeout_for_none_makes_no_runner_call__fr029_nfr008(
    fake_runner, read, argv_for, item, unreadable, incomplete
) -> None:
    runner = fake_runner()
    budget = github.CallBudget()
    got = read(runner, budget, 42, lambda: None)
    assert got.value is None
    assert (got.reason, got.kind) == ("budget_exhausted", "budget_exhausted")
    assert runner.calls == []
    assert budget.calls == 0


@REST_READS
def test_rest_timeout_for_none_before_page_2_stops_paging__fr029_nfr008(
    fake_runner, read, argv_for, item, unreadable, incomplete
) -> None:
    runner = fake_runner(page_script(argv_for, [full_page(item, 1)]))
    budget = github.CallBudget()
    allowed = iter([30.0])
    got = read(runner, budget, 42, lambda: next(allowed, None))
    assert got.value is None
    assert got.reason == "budget_exhausted"
    assert [call[0] for call in runner.calls] == page_argvs(argv_for, 1)
    assert budget.calls == 1


def test_events_reserved_flag_spends_the_reserved_calls__nfr009(fake_runner) -> None:
    """G3' may use the last 3 calls; the ordinary G3 may not."""
    argv = tuple(github.argv_events(42, 1))
    runner = fake_runner({argv: ok([event_item(1)], argv)})
    budget = github.CallBudget()
    for _ in range(github.CALL_CAP - github.RESERVED_CALLS):
        assert budget.spend()
    refused = github.events(runner, budget, 42, timeout)
    assert refused.reason == "budget_exhausted"
    assert runner.calls == []
    allowed = github.events(runner, budget, 42, timeout, reserved=True)
    assert allowed.reason is None
    assert len(allowed.value) == 1
    assert budget.calls == github.CALL_CAP - github.RESERVED_CALLS + 1


# --- DF-18 null rules ------------------------------------------------------------


def read_events(fake_runner, items: list[dict]):
    """Run G3 over one scripted page of ``items``."""
    runner = fake_runner(page_script(github.argv_events, [items]))
    return github.events(runner, github.CallBudget(), 42, timeout)


def read_markers(fake_runner, items: list[dict]):
    """Run G4 over one scripted page of ``items``."""
    runner = fake_runner(page_script(github.argv_comments, [items]))
    return github.marker_comments(runner, github.CallBudget(), 42, timeout)


def test_renamed_event_with_null_label_and_actor_parses__df18_fr005_fr006(
    fake_runner,
) -> None:
    renamed = event_item(
        5,
        "renamed",
        label=None,
        actor_id=None,
        actor_login=None,
        actor_type=None,
    )
    got = read_events(fake_runner, [renamed, event_item(6)])
    assert got.reason is None
    assert got.value[0] == LabelEvent(5, "renamed", None, None, None, None, STAMPED)
    assert got.value[1].event == "labeled"
    assert got.value[1].label == "sc:issue"


@pytest.mark.parametrize("event", ["labeled", "unlabeled"])
@pytest.mark.parametrize("field", ["label", "actor_id", "actor_login", "actor_type"])
def test_labeled_event_with_a_null_predicate_field_is_unreadable__df18_fr005_fr006(
    fake_runner, event: str, field: str
) -> None:
    got = read_events(fake_runner, [event_item(5, event, **{field: None})])
    assert got.value is None
    assert (got.reason, got.kind) == ("events_unreadable", "non_json")


@pytest.mark.parametrize("field", ["event", "created_at"])
def test_any_event_with_a_null_core_field_is_unreadable__df18_fr005_fr006(
    fake_runner, field: str
) -> None:
    got = read_events(fake_runner, [{**event_item(5, "renamed"), field: None}])
    assert got.value is None
    assert got.reason == "events_unreadable"


def test_event_with_a_bad_time_is_unreadable__df18_fr005_fr006(fake_runner) -> None:
    got = read_events(fake_runner, [event_item(5, created_at="yesterday")])
    assert (got.value, got.reason) == (None, "events_unreadable")


@pytest.mark.parametrize("bad", [True, 0, -3, "7", 1.0, None])
def test_event_with_a_bool_or_non_positive_id_is_unreadable__df18_fr005_fr006(
    fake_runner, bad: object
) -> None:
    got = read_events(fake_runner, [event_item(bad)])  # type: ignore[arg-type]
    assert (got.value, got.reason) == (None, "events_unreadable")


@pytest.mark.parametrize("bad", [True, 0, -3, "7", 1.0, None])
def test_marker_with_a_bool_or_non_positive_id_is_unreadable__df18_fr009(
    fake_runner, bad: object
) -> None:
    got = read_markers(fake_runner, [marker_item(bad)])  # type: ignore[arg-type]
    assert (got.value, got.reason) == (None, "marker_unreadable")


def test_marker_with_a_null_login_parses_as_not_own__df18_fr009(fake_runner) -> None:
    got = read_markers(
        fake_runner, [marker_item(1, login=None, marker=True), marker_item(2)]
    )
    assert got.reason is None
    assert got.value == (MarkerEvidence(2, "owner-login", STAMPED, STAMPED, False),)


def test_marker_read_keeps_the_marker_flag__fr009(fake_runner) -> None:
    got = read_markers(fake_runner, [marker_item(3, marker=True)])
    assert got.value == (MarkerEvidence(3, "owner-login", STAMPED, STAMPED, True),)


@pytest.mark.parametrize("field", ["marker", "created_at", "updated_at"])
def test_marker_with_a_null_required_field_is_unreadable__df18_fr009(
    fake_runner, field: str
) -> None:
    got = read_markers(fake_runner, [marker_item(1, **{field: None})])
    assert got.value is None
    assert (got.reason, got.kind) == ("marker_unreadable", "non_json")


@pytest.mark.parametrize("reply", ["{}", '"text"', "null", "7"])
def test_rest_reply_that_is_not_an_array_is_unreadable__df19(
    fake_runner, reply: str
) -> None:
    for argv_for, read, reason in (
        (github.argv_events, github.events, "events_unreadable"),
        (github.argv_comments, github.marker_comments, "marker_unreadable"),
    ):
        argv = tuple(argv_for(42, 1))
        runner = fake_runner({argv: result(stdout=reply, argv=argv)})
        got = read(runner, github.CallBudget(), 42, timeout)
        assert (got.value, got.reason) == (None, reason)


# --- GraphQL paging, G5 and G6 (design line 575, DF-19) ----------------------------


# [UNVERIFIED, assumed shape] The helpers ``gql``, ``comment_node`` and
# ``item_node`` and the inline ``errors`` bodies below build GraphQL replies in
# the shape of design 837 / 838 (G5, G6, error ``type`` names). The captured-shape
# twins are ``graphql_edits.json``, ``graphql_project_items.json`` and the
# ``gh_graphql_*.json`` fixtures, which part C reads. FU-1 replaces them all.


def gql(connection: str, nodes: list, more: bool, cursor: object, **issue: object):
    """A GraphQL reply body: ``issue`` fields plus one paged connection."""
    page_info = {"hasNextPage": more, "endCursor": cursor}
    issue[connection] = {"nodes": nodes, "pageInfo": page_info}
    return {"data": {"repository": {"issue": issue}}}


def comment_node(i: int, **over: object) -> dict:
    """One G5 comment node; ``over`` replaces fields."""
    node: dict = {
        "databaseId": i,
        "author": {"login": "owner-login"},
        "createdAt": STAMP,
        "lastEditedAt": None,
    }
    node.update(over)
    return node


def item_node(i: int = 0, **over: object) -> dict:
    """One G6 Project item node (``i`` only fits the shared node signature)."""
    node: dict = {
        "isArchived": False,
        "project": {"id": "PVT_1"},
        "fieldValueByName": {"name": "Backlog"},
    }
    node.update(over)
    return node


def edits_page(nodes: list, more: bool = False, cursor: object = None, **issue):
    """A G5 reply; the issue times are set unless ``issue`` replaces them."""
    fields = {"createdAt": STAMP, "lastEditedAt": None, **issue}
    return gql("comments", nodes, more, cursor, **fields)


def project_page(nodes: list, more: bool = False, cursor: object = None, **issue):
    """A G6 reply."""
    return gql("projectItems", nodes, more, cursor, **issue)


def cursor_script(argv_for, replies: list) -> dict:
    """Script reply ``k`` to the call after cursor ``c{k}`` (the first has none)."""
    script = {}
    for k, reply in enumerate(replies):
        argv = tuple(argv_for(42, None if k == 0 else f"c{k}"))
        script[argv] = ok(reply, argv)
    return script


GQL_READS = pytest.mark.parametrize(
    "read, argv_for, page, node, unreadable",
    [
        (github.edits, github.argv_edits, edits_page, comment_node, "edits_unreadable"),
        (
            github.project_items,
            github.argv_project_items,
            project_page,
            item_node,
            "project_unreadable",
        ),
    ],
    ids=["edits", "project"],
)


def test_edits_has_next_page_then_false_reads_both_pages__fr005_fr006(
    fake_runner,
) -> None:
    replies = [
        edits_page([comment_node(1), comment_node(2)], True, "c1"),
        edits_page([comment_node(3, lastEditedAt=STAMP, author=None)], False, "c2"),
    ]
    runner = fake_runner(cursor_script(github.argv_edits, replies))
    budget = github.CallBudget()
    got = github.edits(runner, budget, 42, timeout)
    assert (got.reason, got.kind) == (None, "ok")
    assert got.value == EditEvidence(
        STAMPED,
        None,
        (
            CommentEdit(1, "owner-login", STAMPED, None),
            CommentEdit(2, "owner-login", STAMPED, None),
            CommentEdit(3, None, STAMPED, STAMPED),
        ),
    )
    assert [c[0] for c in runner.calls] == [
        tuple(github.argv_edits(42)),
        tuple(github.argv_edits(42, "c1")),
    ]
    assert budget.calls == 2


def test_project_items_has_next_page_then_false_reads_both_pages__fr007(
    fake_runner,
) -> None:
    replies = [
        project_page([item_node()], True, "c1"),
        project_page([item_node(fieldValueByName=None, isArchived=True)], False, None),
    ]
    runner = fake_runner(cursor_script(github.argv_project_items, replies))
    got = github.project_items(runner, github.CallBudget(), 42, timeout)
    assert (got.reason, got.kind) == (None, "ok")
    assert got.value == (
        ProjectItem(False, "PVT_1", "Backlog"),
        ProjectItem(True, "PVT_1", None),
    )
    assert [c[0] for c in runner.calls] == [
        tuple(github.argv_project_items(42)),
        tuple(github.argv_project_items(42, "c1")),
    ]


@GQL_READS
def test_graphql_repeated_end_cursor_is_incomplete__df19(
    fake_runner, read, argv_for, page, node, unreadable
) -> None:
    replies = [page([node(1)], True, "c1"), page([node(2)], True, "c1")]
    runner = fake_runner(cursor_script(argv_for, replies))
    got = read(runner, github.CallBudget(), 42, timeout)
    assert got.value is None
    assert (got.reason, got.kind) == (unreadable, "incomplete")
    assert len(runner.calls) == 2


@GQL_READS
@pytest.mark.parametrize("cursor", ["", None])
def test_graphql_empty_cursor_with_has_next_page_is_incomplete__df19(
    fake_runner, read, argv_for, page, node, unreadable, cursor: object
) -> None:
    runner = fake_runner(cursor_script(argv_for, [page([node(1)], True, cursor)]))
    got = read(runner, github.CallBudget(), 42, timeout)
    assert got.value is None
    assert (got.reason, got.kind) == (unreadable, "incomplete")
    assert len(runner.calls) == 1


@GQL_READS
def test_graphql_page_cap_never_fetches_a_sixth_page__df19(
    fake_runner, read, argv_for, page, node, unreadable
) -> None:
    replies = [page([node(k + 1)], True, f"c{k + 1}") for k in range(5)]
    runner = fake_runner(cursor_script(argv_for, replies))
    budget = github.CallBudget()
    got = read(runner, budget, 42, timeout)
    assert got.value is None
    assert (got.reason, got.kind) == (unreadable, "incomplete")
    assert len(runner.calls) == 5
    assert tuple(argv_for(42, "c5")) not in [c[0] for c in runner.calls]
    assert budget.calls == 5


@GQL_READS
def test_graphql_101_nodes_in_one_page_is_unreadable__df19(
    fake_runner, read, argv_for, page, node, unreadable
) -> None:
    replies = [page([node(i) for i in range(1, 102)])]
    runner = fake_runner(cursor_script(argv_for, replies))
    got = read(runner, github.CallBudget(), 42, timeout)
    assert got.value is None
    assert (got.reason, got.kind) == (unreadable, "non_json")


@GQL_READS
def test_graphql_100_nodes_in_one_page_is_complete__df19(
    fake_runner, read, argv_for, page, node, unreadable
) -> None:
    replies = [page([node(i) for i in range(1, 101)])]
    runner = fake_runner(cursor_script(argv_for, replies))
    got = read(runner, github.CallBudget(), 42, timeout)
    assert got.reason is None
    assert len(runner.calls) == 1


@GQL_READS
def test_graphql_errors_list_is_unreadable_even_with_data__df02(
    fake_runner, read, argv_for, page, node, unreadable
) -> None:
    body = {**page([node(1)]), "errors": [{"type": "SOMETHING_ELSE", "message": "x"}]}
    runner = fake_runner(cursor_script(argv_for, [body]))
    got = read(runner, github.CallBudget(), 42, timeout)
    assert got.value is None
    assert (got.reason, got.kind) == (unreadable, "failed")


@GQL_READS
def test_graphql_scope_error_with_exit_zero_surfaces_as_scope_missing__df02(
    fake_runner, read, argv_for, page, node, unreadable
) -> None:
    body = {"data": None, "errors": [{"type": "INSUFFICIENT_SCOPES", "message": "x"}]}
    runner = fake_runner(cursor_script(argv_for, [body]))
    got = read(runner, github.CallBudget(), 42, timeout)
    assert got.value is None
    assert (got.reason, got.kind) == (unreadable, "scope_missing")


@GQL_READS
def test_graphql_scope_missing_reply_surfaces_as_the_reply_kind__df02(
    fake_runner, read, argv_for, page, node, unreadable
) -> None:
    payload = load("gh_graphql_insufficient_scopes.json")["payload"]
    argv = tuple(argv_for(42, None))
    runner = fake_runner(
        {argv: fail("gh: exit status 1", stdout=json.dumps(payload), argv=argv)}
    )
    got = read(runner, github.CallBudget(), 42, timeout)
    assert got.value is None
    assert (got.reason, got.kind) == (unreadable, "scope_missing")


@GQL_READS
@pytest.mark.parametrize("more", [None, "true", 1])
def test_graphql_non_bool_has_next_page_is_unreadable__df19(
    fake_runner, read, argv_for, page, node, unreadable, more: object
) -> None:
    runner = fake_runner(cursor_script(argv_for, [page([node(1)], more, "c1")]))
    got = read(runner, github.CallBudget(), 42, timeout)
    assert (got.value, got.reason) == (None, unreadable)


@GQL_READS
@pytest.mark.parametrize("body", [[], "text", {"data": None}, {"data": {}}])
def test_graphql_reply_of_the_wrong_shape_is_unreadable__df19(
    fake_runner, read, argv_for, page, node, unreadable, body: object
) -> None:
    runner = fake_runner(cursor_script(argv_for, [body]))
    got = read(runner, github.CallBudget(), 42, timeout)
    assert (got.value, got.reason, got.kind) == (None, unreadable, "non_json")


def test_edits_null_created_at_is_unreadable__df18_fr005_fr006(fake_runner) -> None:
    replies = [edits_page([comment_node(1)], createdAt=None)]
    runner = fake_runner(cursor_script(github.argv_edits, replies))
    got = github.edits(runner, github.CallBudget(), 42, timeout)
    assert (got.value, got.reason) == (None, "edits_unreadable")


@pytest.mark.parametrize("field", ["createdAt", "databaseId"])
def test_edits_comment_with_a_null_field_is_unreadable__df18_fr005_fr006(
    fake_runner, field: str
) -> None:
    replies = [edits_page([comment_node(1, **{field: None})])]
    runner = fake_runner(cursor_script(github.argv_edits, replies))
    got = github.edits(runner, github.CallBudget(), 42, timeout)
    assert (got.value, got.reason) == (None, "edits_unreadable")


@pytest.mark.parametrize(
    "over",
    [{"isArchived": None}, {"isArchived": "no"}, {"project": None}, {"project": {}}],
)
def test_project_item_with_a_null_field_is_unreadable__df18_fr007(
    fake_runner, over: dict
) -> None:
    replies = [project_page([item_node(**over)])]
    runner = fake_runner(cursor_script(github.argv_project_items, replies))
    got = github.project_items(runner, github.CallBudget(), 42, timeout)
    assert (got.value, got.reason) == (None, "project_unreadable")


def test_project_items_reserved_flag_spends_the_reserved_calls__nfr009(
    fake_runner,
) -> None:
    runner = fake_runner(cursor_script(github.argv_project_items, [project_page([])]))
    budget = github.CallBudget()
    for _ in range(github.CALL_CAP - github.RESERVED_CALLS):
        assert budget.spend()
    refused = github.project_items(runner, budget, 42, timeout)
    assert refused.reason == "budget_exhausted"
    assert runner.calls == []
    allowed = github.project_items(runner, budget, 42, timeout, reserved=True)
    assert (allowed.reason, allowed.value) == (None, ())


@GQL_READS
def test_graphql_timeout_for_none_makes_no_runner_call__fr029_nfr008(
    fake_runner, read, argv_for, page, node, unreadable
) -> None:
    runner = fake_runner()
    budget = github.CallBudget()
    got = read(runner, budget, 42, lambda: None)
    assert got.value is None
    assert (got.reason, got.kind) == ("budget_exhausted", "budget_exhausted")
    assert runner.calls == []
    assert budget.calls == 0


# --- discovery, G2 (FR-003, FR-004) ------------------------------------------------


def discovered(number: object) -> dict:
    """One G2 element.

    [UNVERIFIED, assumed shape] design 834; twin: ``gh_issue_list.json``.
    """
    return {
        "number": number,
        "labels": [{"name": "sc:issue"}],
        "assignees": [{"login": "owner-login"}],
        "state": "OPEN",
    }


def read_discovery(fake_runner, items: list):
    """Run G2 over a scripted reply of ``items``."""
    argv = tuple(github.argv_discover("sc:issue", "owner-login"))
    runner = fake_runner({argv: ok(items, argv)})
    got = github.discover(runner, "sc:issue", "owner-login", timeout)
    assert runner.calls == [(argv, None)]
    return got


def test_discover_99_valid_results_are_all_read__ac2_fr003_fr004(fake_runner) -> None:
    got = read_discovery(fake_runner, [discovered(n) for n in range(1, 100)])
    assert (got.reason, got.kind) == (None, "ok")
    assert len(got.value) == 99
    assert got.value[0] == DiscoveredIssue(1, ("sc:issue",), ("owner-login",), "OPEN")


@pytest.mark.parametrize("count", [100, 101])
def test_discover_100_or_more_results_are_truncated__ac2_fr004(
    fake_runner, count: int
) -> None:
    got = read_discovery(fake_runner, [discovered(n) for n in range(1, count + 1)])
    assert got.value is None
    assert (got.reason, got.kind) == ("truncated", "truncated")


def test_discover_repeated_number_is_a_duplicate__ac2_fr004(fake_runner) -> None:
    got = read_discovery(fake_runner, [discovered(4), discovered(5), discovered(4)])
    assert got.value is None
    assert (got.reason, got.kind) == ("discovery_duplicate",) * 2


@pytest.mark.parametrize("bad", [True, 7.0, "7", 0, 10**9, -1, None])
def test_discover_element_with_a_bad_number_is_non_json__ac2_fr003(
    fake_runner, bad: object
) -> None:
    got = read_discovery(fake_runner, [discovered(1), discovered(bad)])
    assert got.value is None
    assert (got.reason, got.kind) == ("gh_non_json", "non_json")


def test_discover_empty_list_is_an_empty_read__fr003(fake_runner) -> None:
    got = read_discovery(fake_runner, [])
    assert (got.reason, got.value) == (None, ())


@pytest.mark.parametrize("reply", ["{}", "null", '"x"', "[7]", '[{"number": 3}]'])
def test_discover_reply_of_the_wrong_shape_is_non_json__fr003(
    fake_runner, reply: str
) -> None:
    argv = tuple(github.argv_discover("sc:issue", "owner-login"))
    runner = fake_runner({argv: result(stdout=reply, argv=argv)})
    got = github.discover(runner, "sc:issue", "owner-login", timeout)
    assert (got.value, got.reason, got.kind) == (None, "gh_non_json", "non_json")


def test_discover_timeout_for_none_makes_no_runner_call__fr029_nfr008(
    fake_runner,
) -> None:
    runner = fake_runner()
    got = github.discover(runner, "sc:issue", "owner-login", lambda: None)
    assert got.value is None
    assert (got.reason, got.kind) == ("gh_timeout", "timeout")
    assert runner.calls == []


def test_user_timeout_for_none_makes_no_runner_call__fr029_nfr008(fake_runner) -> None:
    runner = fake_runner()
    got = github.user(runner, lambda: None)
    assert got.value is None
    assert (got.reason, got.kind) == ("gh_timeout", "timeout")
    assert runner.calls == []


# --- CallBudget (NFR-009) -----------------------------------------------------------


def test_call_budget_allows_32_ordinary_calls_and_refuses_the_33rd__nfr009() -> None:
    budget = github.CallBudget()
    assert all(budget.spend() for _ in range(32))
    assert budget.spend() is False
    assert budget.calls == 32
    assert budget.total == 32


def test_call_budget_allows_3_reserved_calls_up_to_35__nfr009() -> None:
    budget = github.CallBudget()
    for _ in range(32):
        assert budget.spend()
    assert [budget.spend(reserved=True) for _ in range(4)] == [True] * 3 + [False]
    assert budget.calls == 35
    assert budget.spend() is False
    assert github.CALL_CAP == 35
    assert github.RESERVED_CALLS == 3


def test_call_budget_reserved_calls_may_come_first__nfr009() -> None:
    budget = github.CallBudget()
    assert budget.spend(reserved=True)
    assert budget.calls == 1
    assert sum(budget.spend() for _ in range(40)) == 31


def test_call_budget_shared_calls_count_in_total_not_against_the_cap__nfr009() -> None:
    budget = github.CallBudget()
    budget.spend_shared()
    budget.spend_shared()
    assert (budget.calls, budget.shared_calls, budget.total) == (0, 2, 2)
    assert all(budget.spend() for _ in range(32))
    assert budget.spend() is False
    assert all(budget.spend(reserved=True) for _ in range(3))
    assert (budget.calls, budget.shared_calls, budget.total) == (35, 2, 37)


# ==============================================================================
# Part C: Gate A fix cycle 1. Fixture-driven reads (A-1, A-3), failure mapping of
# every read (A-10, A-11, A-12), G7 (A-9), per-call timeouts (A-17), CRLF headers
# (A-18), missing-key edits (A-6) and hostile argv values (A-8).
# ==============================================================================


def utc(*parts: int) -> datetime:
    """An aware UTC time from year, month, day, hour, minute, second."""
    return datetime(*parts, tzinfo=timezone.utc)


# --- A-1: the five replies that only fixtures described --------------------------


def test_discover_reads_the_gh_issue_list_fixture__fr003(fake_runner) -> None:
    got = read_discovery(fake_runner, load("gh_issue_list.json")["payload"])
    assert (got.reason, got.kind) == (None, "ok")
    assert got.value == (
        DiscoveredIssue(
            101,
            ("issue-watch:trigger", "issue-watch:approved"),
            ("owner-login",),
            "OPEN",
        ),
        DiscoveredIssue(102, ("issue-watch:trigger",), ("owner-login",), "OPEN"),
    )


def test_events_reads_the_rest_events_fixture__fr005_fr006(fake_runner) -> None:
    got = read_events(fake_runner, load("rest_events_page.json")["payload"])
    assert got.reason is None
    assert got.value == (
        LabelEvent(
            1001,
            "labeled",
            "trigger-label",
            2001,
            "issue-author",
            "User",
            utc(2026, 1, 1, 0, 0, 0),
        ),
        LabelEvent(
            1002,
            "labeled",
            "approval-label",
            2002,
            "allowed-approver",
            "User",
            utc(2026, 1, 1, 0, 5, 0),
        ),
        LabelEvent(
            1003,
            "unlabeled",
            "approval-label",
            2002,
            "allowed-approver",
            "User",
            utc(2026, 1, 1, 0, 10, 0),
        ),
        LabelEvent(1004, "renamed", None, None, None, None, utc(2026, 1, 1, 0, 15, 0)),
    )
    # The fixture's approval is unlabeled again, so the predicate must refuse it.
    verdict = approval_of(
        got.value,
        labels_now=("trigger-label", "approval-label"),
        trigger_label="trigger-label",
        approval_label="approval-label",
        approvers={2002},
        store_created_at=utc(2025, 12, 31, 0, 0, 0),
    )
    assert (verdict.approved, verdict.reason) == (False, "not_approved")


def test_marker_comments_reads_the_rest_comments_fixture__fr009(fake_runner) -> None:
    got = read_markers(fake_runner, load("rest_comments_marker.json")["payload"])
    assert got.reason is None
    # Comment 3003 has a null login and is dropped (DF-18).
    assert got.value == (
        MarkerEvidence(
            3001,
            "watcher-bot",
            utc(2026, 1, 1, 1, 0, 0),
            utc(2026, 1, 1, 1, 0, 0),
            True,
        ),
        MarkerEvidence(
            3002,
            "other-user",
            utc(2026, 1, 1, 1, 5, 0),
            utc(2026, 1, 1, 1, 5, 0),
            False,
        ),
    )


def test_edits_reads_the_graphql_edits_fixture__fr005(fake_runner) -> None:
    payload = load("graphql_edits.json")["payload"]
    argv = tuple(github.argv_edits(42))
    runner = fake_runner({argv: ok(payload, argv)})
    got = github.edits(runner, github.CallBudget(), 42, timeout)
    assert (got.reason, got.kind) == (None, "ok")
    assert got.value == EditEvidence(
        utc(2026, 1, 1, 0, 0, 0),
        None,
        (
            CommentEdit(1001, "test-user", utc(2026, 1, 1, 0, 10, 0), None),
            CommentEdit(
                1002, None, utc(2026, 1, 1, 0, 20, 0), utc(2026, 1, 1, 0, 30, 0)
            ),
        ),
    )


def test_project_items_reads_the_graphql_project_fixture__fr007(fake_runner) -> None:
    payload = load("graphql_project_items.json")["payload"]
    argv = tuple(github.argv_project_items(42))
    runner = fake_runner({argv: ok(payload, argv)})
    got = github.project_items(runner, github.CallBudget(), 42, timeout)
    assert (got.reason, got.kind) == (None, "ok")
    assert got.value == (ProjectItem(False, "PVT_test_project_0001", "Backlog"),)
    assert re.fullmatch(r"PVT_[A-Za-z0-9_-]{1,64}", got.value[0].project_id)


# --- A-3: fixtures for the replies that had none ---------------------------------


def test_user_rate_limited_g1_fixture_carries_retry_after__fr028(fake_runner) -> None:
    fixture = load("gh_api_user_include_429.json")
    reply = result(
        stdout=fixture["raw"],
        stderr=fixture["stderr"],
        returncode=fixture["exit"],
        argv=G1_ARGV,
    )
    got = github.user(fake_runner({G1_ARGV: reply}), timeout)
    assert (got.value, got.reason, got.kind) == (None, "rate_limited", "rate_limited")
    assert got.retry_after_s == 120
    assert github.rate_limit_wait(reply, NOW) == (
        NOW + timedelta(seconds=120),
        "rate_limited",
    )


# --- A-10: failure mapping of the shared reads G1 and G2 --------------------------

SHARED_FAILURES = [
    pytest.param(result(timed_out=True), "gh_timeout", "timeout", id="timeout"),
    pytest.param(
        fail(load("gh_stderr_http_502.json")["stderr"]),
        "gh_timeout",
        "transient",
        id="5xx",
    ),
    pytest.param(result(stdout="not json"), "gh_non_json", "non_json", id="non-json"),
    pytest.param(
        fail(load("gh_stderr_rate_403.json")["stderr"]),
        "rate_limited",
        "rate_limited",
        id="rate-limited",
    ),
    pytest.param(
        fail(load("gh_stderr_scope_read_project.json")["stderr"]),
        "project_read_failed",
        "scope_missing",
        id="scope-missing",
    ),
    pytest.param(
        fail(load("gh_stderr_auth_401.json")["stderr"]),
        "gh_auth_failed",
        "auth_failed",
        id="auth-failed",
    ),
    pytest.param(
        fail("gh: something else went wrong"),
        "gh_auth_failed",
        "failed",
        id="other-failure",
    ),
    pytest.param(
        result(spawn_error="FileNotFoundError"),
        "gh_auth_failed",
        "failed",
        id="spawn-error",
    ),
]


@pytest.mark.parametrize("reply, reason, kind", SHARED_FAILURES)
def test_user_failure_mapping__fr002_fr028(fake_runner, reply, reason, kind) -> None:
    got = github.user(fake_runner({G1_ARGV: reply}), timeout)
    assert (got.value, got.reason, got.kind) == (None, reason, kind)
    assert got.retry_after_s is None


@pytest.mark.parametrize("reply, reason, kind", SHARED_FAILURES)
def test_discover_failure_mapping__fr003_fr028(
    fake_runner, reply, reason, kind
) -> None:
    argv = tuple(github.argv_discover("sc:issue", "owner-login"))
    got = github.discover(
        fake_runner({argv: reply}), "sc:issue", "owner-login", timeout
    )
    assert (got.value, got.reason, got.kind) == (None, reason, kind)
    assert got.retry_after_s is None  # only G1 carries headers


def g1_failure(headers: list[str], stderr: str):
    """A failed G1 result with header lines. [UNVERIFIED, assumed shape] design 835."""
    head = "".join(f"{h}\n" for h in headers)
    stdout = f"HTTP/2.0 429 Too Many Requests\n{head}\n{{}}\n"
    return result(stdout=stdout, stderr=stderr, returncode=1, argv=G1_ARGV)


@pytest.mark.parametrize(
    "headers, expected",
    [
        (["Retry-After: 120"], 120),
        (["Retry-After: 1"], 1),
        ([], None),
        (["Retry-After: soon"], None),
    ],
)
def test_user_rate_limit_carries_retry_after_seconds__fr028(
    fake_runner, headers, expected
) -> None:
    stderr = load("gh_stderr_rate_429.json")["stderr"]
    reply = g1_failure(headers, stderr)
    got = github.user(fake_runner({G1_ARGV: reply}), timeout)
    assert (got.reason, got.kind) == ("rate_limited", "rate_limited")
    assert got.retry_after_s == expected


G1_OK_RAW = load("gh_api_user_include.json")["raw"]


def g1_ok(body: str):
    """A successful G1 result around ``body``. [UNVERIFIED, assumed shape] design 835."""
    return result(stdout=f"HTTP/2.0 200 OK\n\n{body}\n", argv=G1_ARGV)


@pytest.mark.parametrize(
    "body",
    [
        '{"login": "x", "id": true}',
        '{"login": "x", "id": 0}',
        '{"login": "x", "id": -4}',
        '{"login": "x", "id": "7"}',
        '{"login": "x", "id": 7.0}',
        '{"login": null, "id": 7}',
        '{"login": 5, "id": 7}',
        '{"id": 7}',
        '{"login": "x"}',
        "[]",
        '"text"',
    ],
)
def test_user_malformed_body_is_non_json__fr002(fake_runner, body) -> None:
    got = github.user(fake_runner({G1_ARGV: g1_ok(body)}), timeout)
    assert (got.value, got.reason, got.kind) == (None, "gh_non_json", "non_json")


def test_user_without_a_date_header_still_reads__fr002(fake_runner) -> None:
    got = github.user(fake_runner({G1_ARGV: g1_ok('{"login": "x", "id": 7}')}), timeout)
    assert got.reason is None
    assert got.value == Login("x", 7, None)


# --- A-9: G7, the FR-011 pre-launch re-read ---------------------------------------


def reread_body(n: int = 42, **over: object) -> dict:
    """One projected G7 reply. [UNVERIFIED, assumed shape] design 8.1 G7."""
    body: dict = {
        "number": n,
        "state": "open",
        "labels": ["sc:issue", "approved"],
        "assignees": ["owner-login"],
    }
    body.update(over)
    return body


def run_reread(fake_runner, reply, n: int = 42, budget=None, timeout_for=timeout):
    argv = tuple(github.argv_reread(n))
    runner = fake_runner({argv: reply})
    budget = budget or github.CallBudget()
    return github.reread(runner, budget, n, timeout_for), runner, budget


def test_reread_reads_the_snapshot_with_one_call__fr011(fake_runner) -> None:
    got, runner, budget = run_reread(fake_runner, ok(reread_body()))
    assert (got.reason, got.kind) == (None, "ok")
    assert got.value == IssueSnapshot(
        42, "open", ("sc:issue", "approved"), ("owner-login",)
    )
    assert runner.calls == [(tuple(github.argv_reread(42)), None)]
    assert budget.calls == 1


def test_reread_reads_the_g7_fixture__fr011(fake_runner) -> None:
    fixture = load("gh_issue_reread.json")
    got, _, _ = run_reread(fake_runner, ok(fixture["payload"]), n=101)
    assert got.value == IssueSnapshot(
        101, "open", ("issue-watch:trigger", "issue-watch:approved"), ("owner-login",)
    )


def test_reread_accepts_empty_labels_and_assignees__fr011(fake_runner) -> None:
    got, _, _ = run_reread(fake_runner, ok(reread_body(labels=[], assignees=[])))
    assert got.value == IssueSnapshot(42, "open", (), ())


def test_reread_may_use_the_reserved_calls_but_not_a_36th__nfr009(fake_runner) -> None:
    argv = tuple(github.argv_reread(42))
    runner = fake_runner({argv: ok(reread_body())})
    budget = github.CallBudget()
    for _ in range(github.CALL_CAP - github.RESERVED_CALLS):
        assert budget.spend()
    got = github.reread(runner, budget, 42, timeout)
    assert got.reason is None
    assert budget.calls == github.CALL_CAP - github.RESERVED_CALLS + 1
    for _ in range(github.RESERVED_CALLS - 1):
        assert budget.spend(reserved=True)
    assert budget.calls == github.CALL_CAP
    runner.calls.clear()
    refused = github.reread(runner, budget, 42, timeout)
    assert (refused.value, refused.reason, refused.kind) == (
        None,
        "budget_exhausted",
        "budget_exhausted",
    )
    assert runner.calls == []
    assert budget.calls == github.CALL_CAP


def test_reread_timeout_for_none_makes_no_call__fr029_nfr008(fake_runner) -> None:
    got, runner, budget = run_reread(
        fake_runner, ok(reread_body()), timeout_for=lambda: None
    )
    assert (got.value, got.reason, got.kind) == (
        None,
        "budget_exhausted",
        "budget_exhausted",
    )
    assert runner.calls == []
    assert budget.calls == 0


@pytest.mark.parametrize(
    "number",
    [41, "42", None, 42.5, [42]],
    ids=["other", "str", "none", "float", "list"],
)
def test_reread_reply_for_another_issue_is_revalidation_failed__fr011(
    fake_runner, number
) -> None:
    got, _, _ = run_reread(fake_runner, ok(reread_body(number=number)))
    assert (got.value, got.reason, got.kind) == (
        None,
        "revalidation_failed",
        "non_json",
    )


def test_reread_bool_number_is_not_issue_1__fr011(fake_runner) -> None:
    """``True == 1`` in Python, so only ``valid_issue_number`` keeps this out."""
    got, _, _ = run_reread(fake_runner, ok(reread_body(1, number=True)), n=1)
    assert (got.value, got.reason, got.kind) == (
        None,
        "revalidation_failed",
        "non_json",
    )


@pytest.mark.parametrize(
    "over",
    [
        {"state": None},
        {"state": 7},
        {"labels": None},
        {"labels": "sc:issue"},
        {"labels": [1]},
        {"labels": [None]},
        {"assignees": None},
        {"assignees": [1]},
        {"assignees": "owner-login"},
    ],
)
def test_reread_malformed_fields_are_revalidation_failed__fr011(
    fake_runner, over
) -> None:
    got, _, _ = run_reread(fake_runner, ok(reread_body(**over)))
    assert (got.value, got.reason, got.kind) == (
        None,
        "revalidation_failed",
        "non_json",
    )


@pytest.mark.parametrize("missing", ["number", "state", "labels", "assignees"])
def test_reread_missing_key_is_revalidation_failed__fr011(fake_runner, missing) -> None:
    body = reread_body()
    del body[missing]
    got, _, _ = run_reread(fake_runner, ok(body))
    assert (got.value, got.reason, got.kind) == (
        None,
        "revalidation_failed",
        "non_json",
    )


@pytest.mark.parametrize("payload", [[], "text", None, 7])
def test_reread_reply_that_is_not_an_object_is_revalidation_failed__fr011(
    fake_runner, payload
) -> None:
    got, _, _ = run_reread(fake_runner, ok(payload))
    assert (got.value, got.reason, got.kind) == (
        None,
        "revalidation_failed",
        "non_json",
    )


@pytest.mark.parametrize(
    "reply, reason, kind",
    [
        pytest.param(
            result(timed_out=True), "revalidation_transient", "timeout", id="timeout"
        ),
        pytest.param(
            fail(load("gh_stderr_http_502.json")["stderr"]),
            "revalidation_transient",
            "transient",
            id="5xx",
        ),
        pytest.param(
            fail(load("gh_stderr_auth_401.json")["stderr"]),
            "revalidation_failed",
            "auth_failed",
            id="auth",
        ),
        pytest.param(
            fail(load("gh_stderr_rate_403.json")["stderr"]),
            "revalidation_failed",
            "rate_limited",
            id="rate-limited",
        ),
        pytest.param(
            fail(load("gh_stderr_scope_read_project.json")["stderr"]),
            "revalidation_failed",
            "scope_missing",
            id="scope",
        ),
        pytest.param(
            fail("gh: something else went wrong"),
            "revalidation_failed",
            "failed",
            id="other",
        ),
        pytest.param(
            result(stdout="not json"), "revalidation_failed", "non_json", id="non-json"
        ),
        pytest.param(
            result(spawn_error="FileNotFoundError"),
            "revalidation_failed",
            "failed",
            id="spawn-error",
        ),
    ],
)
def test_reread_failure_split_transient_versus_failed__fr011(
    fake_runner, reply, reason, kind
) -> None:
    got, runner, _ = run_reread(fake_runner, reply)
    assert (got.value, got.reason, got.kind) == (None, reason, kind)
    assert len(runner.calls) == 1


# --- A-11: REST reads given a non-ok reply ---------------------------------------

REST_FAILURES = [
    pytest.param(result(timed_out=True), "timeout", id="timeout"),
    pytest.param(
        fail(load("gh_stderr_auth_401.json")["stderr"]), "auth_failed", id="401"
    ),
    pytest.param(
        fail(load("gh_stderr_rate_403.json")["stderr"]), "rate_limited", id="rate-limit"
    ),
    pytest.param(
        fail(load("gh_stderr_http_502.json")["stderr"]), "transient", id="5xx"
    ),
    pytest.param(fail("gh: something else went wrong"), "failed", id="failure"),
    pytest.param(result(stdout="not json"), "non_json", id="non-json"),
    pytest.param(result(spawn_error="FileNotFoundError"), "failed", id="spawn-error"),
]


@REST_READS
@pytest.mark.parametrize("reply, kind", REST_FAILURES)
def test_rest_failed_first_page_is_unreadable__df02_fr005_fr009(
    fake_runner, read, argv_for, item, unreadable, incomplete, reply, kind
) -> None:
    argv = tuple(argv_for(42, 1))
    runner = fake_runner({argv: reply})
    budget = github.CallBudget()
    got = read(runner, budget, 42, timeout)
    assert (got.value, got.reason, got.kind) == (None, unreadable, kind)
    assert got.retry_after_s is None
    assert len(runner.calls) == 1
    assert budget.calls == 1


@REST_READS
@pytest.mark.parametrize("reply, kind", REST_FAILURES)
def test_rest_failed_page_2_discards_page_1__df02_fr005_fr009(
    fake_runner, read, argv_for, item, unreadable, incomplete, reply, kind
) -> None:
    script = page_script(argv_for, [full_page(item, 1)])
    script[tuple(argv_for(42, 2))] = reply
    runner = fake_runner(script)
    got = read(runner, github.CallBudget(), 42, timeout)
    assert (got.value, got.reason, got.kind) == (None, unreadable, kind)
    assert [call[0] for call in runner.calls] == page_argvs(argv_for, 2)


# --- A-12: exit-0 GraphQL ``errors`` lists ----------------------------------------


@GQL_READS
@pytest.mark.parametrize(
    "errors, kind",
    [
        pytest.param(
            load("gh_graphql_rate_limited.json")["payload"]["errors"],
            "rate_limited",
            id="rate-limited-fixture",
        ),
        pytest.param([{"type": "RATE_LIMITED"}], "rate_limited", id="rate-limited"),
        pytest.param(
            [{"type": "INSUFFICIENT_SCOPES"}, {"type": "RATE_LIMITED"}],
            "scope_missing",
            id="scope-wins-over-rate",
        ),
        pytest.param(
            [{"type": "SOMETHING_ELSE"}, {"type": "RATE_LIMITED"}],
            "rate_limited",
            id="rate-after-other",
        ),
        pytest.param(["not a dict"], "failed", id="non-dict-item"),
        pytest.param([{"message": "no type"}], "failed", id="no-type"),
        pytest.param([{"type": 5}], "failed", id="int-type"),
        pytest.param([{"type": None}], "failed", id="null-type"),
        pytest.param("boom", "failed", id="errors-is-a-string"),
        pytest.param({"type": "RATE_LIMITED"}, "failed", id="errors-is-a-dict"),
    ],
)
def test_graphql_exit_zero_errors_kind__df02_fr028(
    fake_runner, read, argv_for, page, node, unreadable, errors, kind
) -> None:
    body = {**page([node(1)]), "errors": errors}
    runner = fake_runner(cursor_script(argv_for, [body]))
    got = read(runner, github.CallBudget(), 42, timeout)
    assert (got.value, got.reason, got.kind) == (None, unreadable, kind)


# --- A-6: a missing ``lastEditedAt`` key is not "never edited" --------------------


def test_edits_explicit_null_last_edited_at_means_never_edited__df18(
    fake_runner,
) -> None:
    runner = fake_runner(
        cursor_script(github.argv_edits, [edits_page([comment_node(1)])])
    )
    got = github.edits(runner, github.CallBudget(), 42, timeout)
    assert got.reason is None
    assert got.value.issue_last_edited_at is None
    assert got.value.comments[0].last_edited_at is None


def test_edits_issue_without_the_last_edited_at_key_is_unreadable__df18(
    fake_runner,
) -> None:
    reply = edits_page([comment_node(1)])
    del reply["data"]["repository"]["issue"]["lastEditedAt"]
    runner = fake_runner(cursor_script(github.argv_edits, [reply]))
    got = github.edits(runner, github.CallBudget(), 42, timeout)
    assert (got.value, got.reason, got.kind) == (None, "edits_unreadable", "non_json")


def test_edits_comment_without_the_last_edited_at_key_is_unreadable__df18(
    fake_runner,
) -> None:
    node = comment_node(1)
    del node["lastEditedAt"]
    runner = fake_runner(cursor_script(github.argv_edits, [edits_page([node])]))
    got = github.edits(runner, github.CallBudget(), 42, timeout)
    assert (got.value, got.reason, got.kind) == (None, "edits_unreadable", "non_json")


# --- A-17: the per-call timeout reaches the runner -------------------------------


def timeouts_from(*values: float):
    """A ``timeout_for`` that returns ``values`` in order."""
    it = iter(values)
    return lambda: next(it)


def test_user_passes_its_timeout_to_the_runner__fr029_nfr008(fake_runner) -> None:
    runner = fake_runner({G1_ARGV: result(stdout=G1_OK_RAW, argv=G1_ARGV)})
    assert github.user(runner, timeouts_from(11.5)).reason is None
    assert runner.timeouts == [11.5]


def test_discover_passes_its_timeout_to_the_runner__fr029_nfr008(fake_runner) -> None:
    argv = tuple(github.argv_discover("sc:issue", "owner-login"))
    runner = fake_runner({argv: ok([], argv)})
    github.discover(runner, "sc:issue", "owner-login", timeouts_from(12.5))
    assert runner.timeouts == [12.5]


def test_reread_passes_its_timeout_to_the_runner__fr029_nfr008(fake_runner) -> None:
    _, runner, _ = run_reread(
        fake_runner, ok(reread_body()), timeout_for=timeouts_from(9.75)
    )
    assert runner.timeouts == [9.75]


@REST_READS
def test_rest_pages_pass_each_timeout_to_the_runner__fr029_nfr008(
    fake_runner, read, argv_for, item, unreadable, incomplete
) -> None:
    pages = [full_page(item, 1), [item(101)]]
    runner = fake_runner(page_script(argv_for, pages))
    got = read(runner, github.CallBudget(), 42, timeouts_from(30.0, 17.25))
    assert got.reason is None
    assert runner.timeouts == [30.0, 17.25]


@GQL_READS
def test_graphql_pages_pass_each_timeout_to_the_runner__fr029_nfr008(
    fake_runner, read, argv_for, page, node, unreadable
) -> None:
    replies = [page([node(1)], True, "c1"), page([node(2)], False, None)]
    runner = fake_runner(cursor_script(argv_for, replies))
    got = read(runner, github.CallBudget(), 42, timeouts_from(30.0, 17.25))
    assert got.reason is None
    assert runner.timeouts == [30.0, 17.25]


# --- A-18: CRLF header blocks and malformed header lines --------------------------


def crlf(text: str) -> str:
    return text.replace("\n", "\r\n")


def test_classify_g1_with_crlf_line_endings_is_parsed__fr002() -> None:
    raw = crlf(load("gh_api_user_include.json")["raw"])
    assert "\r\n\r\n" in raw
    reply = github.classify(result(stdout=raw, argv=G1_ARGV), include_headers=True)
    assert reply.kind == "ok"
    assert reply.payload == {"login": "owner-login", "id": 1001}


def test_crlf_g1_headers_are_read__fr002_fr028() -> None:
    fixture = load("gh_api_user_include_429.json")
    reply = result(
        stdout=crlf(fixture["raw"]),
        stderr=fixture["stderr"],
        returncode=fixture["exit"],
        argv=G1_ARGV,
    )
    assert github.retry_after(reply) == 120
    assert github.date_header(reply) == utc(2026, 11, 7, 12, 0, 0)
    assert github.classify(reply, include_headers=True).kind == "rate_limited"


def test_user_reads_a_crlf_reply__fr002(fake_runner) -> None:
    raw = crlf(load("gh_api_user_include.json")["raw"])
    got = github.user(fake_runner({G1_ARGV: result(stdout=raw, argv=G1_ARGV)}), timeout)
    assert got.value == Login("owner-login", 1001, utc(2026, 11, 7, 12, 0, 0))


@pytest.mark.parametrize(
    "raw",
    [
        'HTTP/2.0 200 OK\nnot-a-header-line\n\n{"login": "x", "id": 1}\n',
        'Status: 200\n\n{"login": "x", "id": 1}\n',
        'HTTP/2.0 200 OK\nDate: x\n{"login": "x", "id": 1}\n',
    ],
    ids=["no-colon", "no-status-line", "no-blank-line"],
)
def test_classify_g1_malformed_header_block_is_non_json__fr002(raw: str) -> None:
    reply = github.classify(result(stdout=raw, argv=G1_ARGV), include_headers=True)
    assert reply.kind == "non_json"
    assert github.retry_after(result(stdout=raw, argv=G1_ARGV)) is None
    assert github.date_header(result(stdout=raw, argv=G1_ARGV)) is None


# --- A-8: hostile values never reach an argv --------------------------------------


@pytest.mark.parametrize(
    "trigger",
    ["", "a,b", "-x", "x" * 51, "bad\nlabel", "bad\x00", "tab\there", "\x7f", None, 5],
)
def test_argv_discover_rejects_an_unsafe_trigger__fr003(trigger) -> None:
    with pytest.raises(ValueError, match="invalid trigger label"):
        github.argv_discover(trigger, "owner-login")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "trigger", ["issue-watch:trigger", "sc:issue", "x" * 50, "with space", "a"]
)
def test_argv_discover_accepts_a_safe_trigger__fr003(trigger: str) -> None:
    argv = github.argv_discover(trigger, "owner-login")
    assert argv[argv.index("--label") + 1] == trigger


@pytest.mark.parametrize(
    "login",
    [
        "",
        "-x",
        "-",
        "a b",
        "a,b",
        "x" * 40,
        "a\x00b",
        "a\nb",
        "bot[bot]",
        "_x",
        None,
        5,
    ],
)
def test_argv_discover_rejects_an_unsafe_login__fr003(login) -> None:
    with pytest.raises(ValueError, match="invalid login"):
        github.argv_discover("sc:issue", login)  # type: ignore[arg-type]


@pytest.mark.parametrize("login", ["owner-login", "a", "x" * 39, "A1-b", "a-"])
def test_argv_discover_accepts_a_github_login__fr003(login: str) -> None:
    argv = github.argv_discover("sc:issue", login)
    assert argv[argv.index("--assignee") + 1] == login


def test_discover_with_an_unsafe_value_makes_no_call__fr003(fake_runner) -> None:
    runner = fake_runner()
    with pytest.raises(ValueError):
        github.discover(runner, "a,b", "owner-login", timeout)
    with pytest.raises(ValueError):
        github.discover(runner, "sc:issue", "a b", timeout)
    assert runner.calls == []


@pytest.mark.parametrize("argv_for", [github.argv_edits, github.argv_project_items])
@pytest.mark.parametrize(
    "after",
    ["", "a b", "a\nb", "x" * 257, "a\x00b", "é", "a;b", "$(x)", 5, b"x"],
)
def test_graphql_argv_rejects_an_unsafe_cursor__df19(argv_for, after) -> None:
    with pytest.raises(ValueError, match="invalid cursor"):
        argv_for(42, after)


@pytest.mark.parametrize("argv_for", [github.argv_edits, github.argv_project_items])
@pytest.mark.parametrize("after", ["Y3Vyc29yOjE=", "abc_-.:/+=", "x" * 256])
def test_graphql_argv_accepts_a_cursor_alphabet__df19(argv_for, after: str) -> None:
    argv = argv_for(42, after)
    assert argv[-2:] == ["-f", f"after={after}"]


@GQL_READS
@pytest.mark.parametrize("cursor", ["a b", "a\nb", "x" * 257, "é", "$(touch x)"])
def test_graphql_hostile_end_cursor_is_unreadable_and_not_sent__df19(
    fake_runner, read, argv_for, page, node, unreadable, cursor
) -> None:
    runner = fake_runner(cursor_script(argv_for, [page([node(1)], True, cursor)]))
    got = read(runner, github.CallBudget(), 42, timeout)
    assert (got.value, got.reason, got.kind) == (None, unreadable, "non_json")
    assert len(runner.calls) == 1


@GQL_READS
def test_graphql_odd_end_cursor_on_the_last_page_is_still_complete__df19(
    fake_runner, read, argv_for, page, node, unreadable
) -> None:
    """The cursor is checked only when it is about to be sent."""
    runner = fake_runner(cursor_script(argv_for, [page([node(1)], False, "a b")]))
    got = read(runner, github.CallBudget(), 42, timeout)
    assert got.reason is None
