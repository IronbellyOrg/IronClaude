"""The pure predicates of the issue watcher: times, keys, the DQ1 rule and the ordering (design 4.2, 4.10)."""

from __future__ import annotations

import ast
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import predicates
from superclaude.cli.issue_watch.predicates import (
    DiscoveredIssue,
    InfoItem,
    eligibility_order,
    file_key,
    format_utc,
    is_intended_owner,
    issue_key,
    parse_utc,
    split_issue_key,
    valid_issue_number,
    valid_login,
    valid_repo,
)

NOW = datetime(2026, 11, 19, 12, 0, tzinfo=timezone.utc)


def issue(repo="o/r", number=1) -> DiscoveredIssue:
    return DiscoveredIssue(repo, number, (), ("me",), "open", NOW)


# --- times -------------------------------------------------------------------------------------------


def test_parse_and_format_utc_round_trip():
    assert parse_utc("2026-11-19T12:00:00Z") == NOW
    assert format_utc(NOW) == "2026-11-19T12:00:00Z"
    assert (
        format_utc(NOW.astimezone(timezone(timedelta(hours=5))))
        == "2026-11-19T12:00:00Z"
    )


@pytest.mark.parametrize(
    "bad",
    [
        "2026-11-19T12:00:00z",
        "2026-11-19 12:00:00Z",
        "2026-11-19T12:00:00",
        "2026-1-19T12:00:00Z",
        "٢٠٢٦-11-19T12:00:00Z",
        "",
        None,
        5,
    ],
)
def test_parse_utc_refuses_every_other_shape(bad):
    with pytest.raises(ValueError):
        parse_utc(bad)


def test_format_utc_refuses_a_naive_time():
    with pytest.raises(ValueError):
        format_utc(datetime(2026, 11, 19, 12, 0))


# --- numbers, repos, logins and keys ----------------------------------------------------------------


def test_valid_issue_number_is_a_real_int_in_range():
    assert valid_issue_number(1) and valid_issue_number(999_999_999)
    for bad in (0, -1, 1_000_000_000, True, "5", 1.0, None):
        assert not valid_issue_number(bad)


@pytest.mark.parametrize(
    "repo", ["IronbellyOrg/IronClaude", "a/b", "A-b/c.d_e", "o/" + "x" * 100]
)
def test_valid_repos(repo):
    assert valid_repo(repo)


@pytest.mark.parametrize(
    "repo",
    [
        "",
        "no-slash",
        "o/",
        "/r",
        "o/r/x",
        "-o/r",
        "o/r\n",
        "o/ r",
        "o/..",
        "o/.",
        "o/" + "x" * 101,
        "x" * 40 + "/r",
        None,
        5,
    ],
)
def test_invalid_repos(repo):
    assert not valid_repo(repo)


def test_valid_login():
    assert valid_login("clayphi") and valid_login("a-b")
    for bad in ("", "-a", "a b", "a" * 40, "a\n", None):
        assert not valid_login(bad)


def test_keys_round_trip_and_refuse_bad_input():
    key = issue_key("IronbellyOrg/IronClaude", 655)
    assert key == "IronbellyOrg/IronClaude#655"
    assert split_issue_key(key) == ("IronbellyOrg/IronClaude", 655)
    for bad in (
        "o/r#0",
        "o/r#01",
        "o/r#1x",
        "or#1",
        "o/r#",
        "#1",
        "o/r#1000000000",
        None,
        5,
    ):
        with pytest.raises(ValueError):
            split_issue_key(bad)
    for repo, number in (("bad", 1), ("o/r", 0), ("o/r", True)):
        with pytest.raises(ValueError):
            issue_key(repo, number)


def test_file_key_is_the_name_part_of_the_orchestrators_files():
    assert file_key("IronbellyOrg/IronClaude", 655) == "IronbellyOrg__IronClaude__655"
    with pytest.raises(ValueError):
        file_key("o/r", 0)


def test_the_issue_and_info_rows_name_their_key():
    assert issue("o/r", 7).key == "o/r#7"
    item = InfoItem("mentions", "o/r", 7, "issue", NOW)
    assert item.seen_key == "mentions o/r#7 2026-11-19T12:00:00Z"


# --- the DQ1 rule -------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("assignees", "owned", "why"),
    [
        (["me"], True, None),
        (["me", "me"], True, None),
        ([], False, "unassigned"),
        (["other"], False, "assigned_other"),
        (["me", "other"], False, "assigned_other"),  # a co-assignee: nobody takes it
        ({"me"}, True, None),
        (iter(["me"]), True, None),
    ],
)
def test_the_user_must_be_the_only_assignee(assignees, owned, why):
    assert is_intended_owner(assignees, "me") == (owned, why)


# --- the order ----------------------------------------------------------------------------------------------------


def test_new_issues_are_ordered_by_repo_then_number_and_known_keys_are_left_out():
    rows = [issue("b/x", 2), issue("a/y", 9), issue("a/y", 3), issue("b/x", 1)]
    assert [i.key for i in eligibility_order(rows)] == [
        "a/y#3",
        "a/y#9",
        "b/x#1",
        "b/x#2",
    ]
    assert [
        i.key for i in eligibility_order(rows, {"a/y#3": object(), "b/x#1": object()})
    ] == ["a/y#9", "b/x#2"]


# --- the contract of the module ------------------------------------------------------------------------------------


def test_the_claim_marker_stays_for_the_orchestrator_and_the_marker_contract_test():
    assert predicates.CLAIM_MARKER == "<!-- sc:issue:claim -->"


def test_the_removed_approval_label_edit_and_project_names_are_gone():
    for name in (
        "LabelEvent", "ProjectItem", "MarkerEvidence", "CommentEdit", "EditEvidence",
        "ApprovalResult", "approval_of", "unchanged_since", "project_check", "marker_time",
        "marker_in_window", "SKEW_TOLERANCE_S",
    ):  # fmt: skip
        assert not hasattr(predicates, name), name


def test_the_module_imports_nothing_from_the_package_and_does_no_io():
    tree = ast.parse(Path(predicates.__file__).read_text(encoding="utf-8"))
    imported = {
        (n.module or "") if isinstance(n, ast.ImportFrom) else a.name
        for n in ast.walk(tree)
        if isinstance(n, (ast.Import, ast.ImportFrom))
        for a in (n.names if isinstance(n, ast.Import) else [n])
    }
    assert not any(m.startswith("superclaude") or m.startswith(".") for m in imported)
    assert not {"os", "subprocess", "time", "socket", "pathlib"} & imported
