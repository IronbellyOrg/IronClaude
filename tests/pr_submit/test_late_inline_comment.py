"""Issue #381: a finished Augment review whose inline comment is stamped one second later.

Real data: PR 377, review 5776286053 submitted 2026-11-04T21:44:59Z, its one inline comment
4473733769 created 21:45:00Z (``fixtures/cosmos-pr377-late-comment.json``, fetched with ``gh api``).
The thread is open in the fixture; on GitHub today it is resolved and outdated.

Master already classifies this as findings since PR 337 (completion is extended to the creation of the
reviewer's own roots of that review, ``_completion_time``). These tests pin that behaviour for the exact
PR 377 times and pin the limits that must not loosen: a root of another review, or from before a
re-trigger watermark, never counts as new.
"""

from __future__ import annotations

import copy

import pytest

from superclaude.pr_submit import (
    DetectionContract,
    actionable_finding_comments,
    classify,
)

CONTRACT = DetectionContract(
    augment_bot_login="augmentcode[bot]", augment_app_slug="augmentcode"
)
REVIEW_ID = 5776286053
COMMENT_ID = 4473733769


@pytest.fixture
def snapshot(load_fixture):
    return load_fixture("cosmos-pr377-late-comment.json")


def test_fixture_has_the_pr377_one_second_gap(snapshot):
    assert snapshot["reviews"][0]["submitted_at"] == "2026-11-04T21:44:59Z"
    assert snapshot["comments"][0]["created_at"] == "2026-11-04T21:45:00Z"
    root = snapshot["threads"][0]["comments"]["nodes"][0]
    assert root["createdAt"] == "2026-11-04T21:45:00Z"
    assert root["pullRequestReview"]["databaseId"] == REVIEW_ID


def test_pr377_review_with_comment_one_second_later_is_findings_not_polling(snapshot):
    assert classify(snapshot, CONTRACT) == "findings"
    selected = actionable_finding_comments(snapshot, CONTRACT)
    assert [c["comment_id"] for c in selected] == [COMMENT_ID]
    assert selected[0]["review_id"] == REVIEW_ID


def test_late_comment_is_findings_with_an_explicit_head_and_older_watermark(snapshot):
    head = snapshot["head_sha"]
    assert (
        classify(
            snapshot, CONTRACT, current_head_sha=head, watermark="2026-11-04T21:30:00Z"
        )
        == "findings"
    )


@pytest.mark.parametrize("watermark", ["2026-11-04T21:44:59Z", "2026-11-04T21:45:30Z"])
def test_review_not_newer_than_the_retrigger_watermark_still_polls(snapshot, watermark):
    # The watermark rule stays: the review at 21:44:59Z is not strictly newer than either value, so it is
    # not the answer to that re-trigger, whatever its comment times are.
    assert classify(snapshot, CONTRACT, watermark=watermark) == "polling"
    assert actionable_finding_comments(snapshot, CONTRACT, watermark=watermark) == []


def _other_review_root(snapshot, *, created_at, review_id=5776000000):
    """An open Augment root that belongs to a DIFFERENT review of the same head."""
    thread = copy.deepcopy(snapshot["threads"][0])
    thread["id"] += "-other"
    root = thread["comments"]["nodes"][0]
    root["id"] += "-other"
    root["databaseId"] += 1
    root["createdAt"] = created_at
    root["pullRequestReview"]["databaseId"] = review_id
    root["pullRequestReview"]["id"] = f"PRR_other_{review_id}"
    snapshot["threads"].append(thread)


def test_root_of_another_review_created_after_completion_still_polls(snapshot):
    # Completion is stretched only to this review's OWN root (21:45:00Z). A root of another review created
    # one second after that is evidence of a newer review and the gate keeps polling: no blanket time gap.
    _other_review_root(snapshot, created_at="2026-11-04T21:45:01Z")
    assert classify(snapshot, CONTRACT) == "polling"
    assert actionable_finding_comments(snapshot, CONTRACT) == []


def test_own_root_a_minute_late_is_still_part_of_the_review_a6_rule(snapshot):
    # The rule is by ownership (same review id and commit), not by a time gap: documented in
    # refs/detection-contract.md. A root of this review is never "newer than" its own review.
    for node in (
        snapshot["threads"][0]["comments"]["nodes"][0],
        snapshot["comments"][0],
    ):
        node["createdAt" if "createdAt" in node else "created_at"] = (
            "2026-11-04T21:46:00Z"
        )
    snapshot["observed_at"] = "2026-11-04T21:47:00Z"
    assert classify(snapshot, CONTRACT) == "findings"


def test_root_of_this_review_on_an_older_head_is_not_accepted(snapshot):
    root = snapshot["threads"][0]["comments"]["nodes"][0]
    root["pullRequestReview"]["commit"]["oid"] = "0" * 39 + "1"
    assert classify(snapshot, CONTRACT) == "polling"
