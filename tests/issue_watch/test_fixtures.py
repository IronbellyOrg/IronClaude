"""The ``_assumed_shape`` fixtures: the deleted ones stay deleted, the kept ones still load.

PR A deletes the six fixtures that pinned deleted code (the GraphQL, comment and
event replies of the old approval check). PR E replaces or justifies the rest
after the live test, so each one must stay a parseable, marked file until then.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "_assumed_shape"

DELETED = (
    "gh_graphql_insufficient_scopes.json",
    "gh_graphql_rate_limited.json",
    "graphql_edits.json",
    "graphql_project_items.json",
    "rest_comments_marker.json",
    "rest_events_page.json",
)
# The 13 of the original 19 that PR A keeps, for PR E to replace or justify.
KEPT_OLD = (
    "gh_api_user_include.json",
    "gh_api_user_include_429.json",
    "gh_issue_list.json",
    "gh_issue_reread.json",
    "gh_stderr_auth_401.json",
    "gh_stderr_http_502.json",
    "gh_stderr_rate_403.json",
    "gh_stderr_rate_429.json",
    "gh_stderr_scope_read_project.json",
    "orca_launch_empty_operation_id.json",
    "orca_launch_no_operation_id.json",
    "orca_launch_success.json",
    "orca_launch_unknown.json",
)
# The shapes the new poll reads and the new Orca calls it makes (all still guesses).
NEW = (
    "gh_branch_date.json",
    "gh_issue_develop_list.json",
    "gh_issue_view_labels.json",
    "gh_issue_view_updated.json",
    "gh_search_assigned.json",
    "gh_search_info.json",
    "gh_stderr_http_404.json",
    "gh_timeline_evidence.json",
    "orca_reference_find.json",
    "orca_terminal_create.json",
    "orca_terminal_list.json",
    "orca_terminal_screen.json",
    "orca_terminal_send_receipt.json",
    "orca_terminal_wait_idle.json",
    "orca_worktree_show_found.json",
    "orca_worktree_show_none.json",
)
TEXT_FIXTURES = ("ccsession_help_tiers.txt",)


def test_the_six_fixtures_of_the_deleted_code_are_gone():
    for name in DELETED:
        assert not (FIXTURE_DIR / name).exists(), name


def test_the_folder_holds_exactly_the_kept_and_the_new_fixtures():
    have = sorted(p.name for p in FIXTURE_DIR.iterdir())
    assert have == sorted([*KEPT_OLD, *NEW, *TEXT_FIXTURES])


@pytest.mark.parametrize("name", [*KEPT_OLD, *NEW])
def test_every_json_fixture_parses_and_says_its_shape_is_assumed(name):
    text = (FIXTURE_DIR / name).read_text(encoding="utf-8")
    data = json.loads(text)
    assert text.endswith("\n") and not text.endswith("\n\n"), name
    assert data["_assumed_shape"] is True, name
    assert isinstance(data["source"], str) and data["source"], name
    assert any(k in data for k in ("payload", "raw", "stdout", "stderr")), name


def test_the_tiers_fixture_lists_the_default_tier():
    text = (FIXTURE_DIR / "ccsession_help_tiers.txt").read_text(encoding="utf-8")
    assert text.startswith("Tiers in this workspace")
    assert "* ccsession --tier tier1b" in text
