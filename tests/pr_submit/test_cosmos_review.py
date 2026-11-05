"""Cosmos lifecycle/boundary regressions (PR266-shaped, sanitized fixture).

IDs/SHAs and the review envelope reflect PR266; timestamps, path, prose and opaque
GraphQL IDs are representative test data, not a verbatim live API recording.
"""

from __future__ import annotations

import copy
import json
from datetime import datetime, timezone

import pytest

from superclaude.pr_submit import (
    DetectionContract,
    actionable_finding_comments,
    classify,
    has_augment_activity,
    poll_augment_review,
    poll_succeeded,
)

CONTRACT = DetectionContract(
    augment_bot_login="augmentcode[bot]", augment_app_slug="augmentcode"
)
HEAD = "13d246ec9e0d5aad4b6ea70529bebd9496a776e5"
OLD = "0f5fef56e1abf1958708473f2004c5627a0a163d"
WATERMARK = "2026-10-16T19:30:00Z"


@pytest.fixture
def snapshot(load_fixture):
    return load_fixture("cosmos-pr266.json")


def set_marker(snapshot, **changes):
    review = snapshot["reviews"][-1]
    marker = json.loads(
        review["body"].split("cosmos-review-status:v1 ")[1].split(" -->")[0]
    )
    marker.update(changes)
    review["body"] = "<!-- cosmos-review-status:v1 " + json.dumps(marker) + " -->"


def assert_polling(snapshot, **context):
    assert classify(snapshot, CONTRACT, **context) == "polling"
    assert actionable_finding_comments(snapshot, CONTRACT, **context) == []


@pytest.mark.parametrize("line", [None, 172])
def test_a1_a5_resolved_old_thread_never_poisons_clean(snapshot, line):
    snapshot["threads"][0]["line"] = line
    snapshot["threads"][0]["comments"]["nodes"][0]["line"] = line
    snapshot["comments"][0]["line"] = line
    assert classify(snapshot, CONTRACT, watermark=WATERMARK) == "clean"
    assert actionable_finding_comments(snapshot, CONTRACT, watermark=WATERMARK) == []


def test_a2_old_head_only_polls(snapshot):
    snapshot["reviews"].pop()
    assert_polling(snapshot)
    snapshot["head_sha"] = OLD
    assert_polling(snapshot)
    # The old positive completion still cannot act on a resolved/missing detail.
    assert_polling(snapshot, current_head_sha=HEAD)


def test_a4_a14_older_open_root_survives_zero_count_and_watermark(snapshot):
    snapshot["threads"][0]["isResolved"] = False
    before = copy.deepcopy(snapshot)
    assert classify(snapshot, CONTRACT, watermark=WATERMARK) == "findings"
    selected = actionable_finding_comments(snapshot, CONTRACT, watermark=WATERMARK)
    assert len(selected) == 1
    root = selected[0]
    assert root["comment_id"] == root["databaseId"] == 4296483537
    assert root["thread_id"] == "PRRT_pr266_example"
    assert root["review_id"] == root["pullRequestReview"]["databaseId"] == 5550158176
    assert root["id"] == "PRRC_pr266_example"
    assert root["line"] is None and root["original_line"] == 172
    assert root["is_outdated"] is True and root["is_resolved"] is False
    assert snapshot == before
    root["body"] = "caller-local edit"
    assert snapshot == before


@pytest.mark.parametrize("count", [1, 2])
def test_a3_a14_positive_count_requires_enough_detail_no_partial_dispatch(
    snapshot, count
):
    set_marker(snapshot, unresolved_count=count)
    if count == 2:
        snapshot["threads"][0]["isResolved"] = False
    assert_polling(snapshot)


def test_count_is_lower_bound_not_equality_with_historical_threads(snapshot):
    snapshot["threads"][0]["isResolved"] = False
    second = copy.deepcopy(snapshot["threads"][0])
    second["id"] += "2"
    second["comments"]["nodes"][0]["id"] += "2"
    second["comments"]["nodes"][0]["databaseId"] += 1
    snapshot["threads"].append(second)
    set_marker(snapshot, unresolved_count=1)
    assert classify(snapshot, CONTRACT) == "findings"
    assert len(actionable_finding_comments(snapshot, CONTRACT)) == 2


@pytest.mark.parametrize(
    "field,value",
    [
        ("specialist", ""),
        ("specialist", "  "),
        ("specialist", None),
        ("specialist", []),
        ("status", "pending"),
        ("status", "unknown"),
        ("status", True),
        ("head", "13d246e"),
        ("head", "g" * 40),
        ("head", 123),
        ("baseline", "a" * 39),
        ("baseline", None),
        ("unresolved_count", True),
        ("unresolved_count", False),
        ("unresolved_count", -1),
        ("unresolved_count", "0"),
        ("unresolved_count", 0.0),
        ("unresolved_count", None),
    ],
)
def test_a6_marker_field_validation(snapshot, field, value):
    set_marker(snapshot, **{field: value})
    assert_polling(snapshot)


@pytest.mark.parametrize(
    "body",
    [
        "<!-- cosmos-review-status:v1 {not json} -->",
        "<!-- cosmos-review-status:v2 {} -->",
        "<!-- cosmos-review-status: v1 {} -->",
        "<!-- cosmos-review-status:v1 {}",
        "<!-- cosmos-review-status:v1 [] -->",
        "<!-- cosmos-review-status:v1 null -->",
        "<!-- cosmos-review-status:v1 " + "x" * 8193 + " -->",
        '<!-- cosmos-review-status:v1 {"head":"a","head":"b"} -->',
    ],
)
def test_a6_bad_marker_never_falls_back_to_legacy_clean(snapshot, body):
    snapshot["reviews"][-1]["body"] = body
    assert_polling(snapshot)


def test_duplicate_marker_even_unsupported_duplicate_blocks_completion(snapshot):
    review = snapshot["reviews"][-1]
    review["body"] += "\n<!-- cosmos-review-status:v2 {} -->"
    assert_polling(snapshot)


def test_recognizable_live_header_without_marker_is_not_legacy_clean(snapshot):
    snapshot["reviews"][-1]["body"] = snapshot["reviews"][-1]["body"].split("<!--")[0]
    snapshot["reviews"] = snapshot["reviews"][-1:]
    assert_polling(snapshot)
    assert has_augment_activity(snapshot, CONTRACT)


@pytest.mark.parametrize("commit", [OLD, "short", None, True])
def test_a7_review_commit_and_marker_must_agree(snapshot, commit):
    snapshot["reviews"][-1]["commit_id"] = commit
    assert_polling(snapshot)


def test_a7_explicit_head_is_not_ignored(snapshot):
    assert_polling(snapshot, current_head_sha=OLD)
    assert_polling(snapshot, current_head_sha="short")
    assert_polling(snapshot, current_head_sha="")
    snapshot.pop("head_sha")
    assert_polling(snapshot)
    assert classify(snapshot, CONTRACT, current_head_sha=HEAD) == "clean"


@pytest.mark.parametrize("watermark", ["2026-10-16T20:00:00Z", "2026-10-16T21:00:00Z"])
def test_a8_completion_must_be_strictly_newer(snapshot, watermark):
    assert_polling(snapshot, watermark=watermark)
    assert classify(snapshot, CONTRACT, watermark=WATERMARK) == "clean"


@pytest.mark.parametrize(
    "watermark", ["invalid", 123, True, {}, [], datetime(2026, 10, 16)]
)
def test_unknown_watermark_types_are_safe_and_unattributed(snapshot, watermark):
    assert_polling(snapshot, watermark=watermark)


def test_actual_instants_not_lexical_timestamp_order(snapshot):
    # 20:00Z completion is BEFORE 22:30+02:00, despite lexical string order.
    assert_polling(snapshot, watermark="2026-10-16T22:30:00+02:00")
    # 20:00Z completion is AFTER 22:30+03:00.
    assert (
        classify(snapshot, CONTRACT, watermark="2026-10-16T22:30:00+03:00") == "clean"
    )
    assert (
        classify(
            snapshot,
            CONTRACT,
            watermark=datetime(2026, 10, 16, 19, 30, tzinfo=timezone.utc),
        )
        == "clean"
    )


def test_a9_unordered_reviews_human_and_other_bot_are_ignored(snapshot):
    clean = snapshot["reviews"].pop()
    snapshot["reviews"].insert(0, clean)
    for author in ("operator", "different[bot]"):
        snapshot["reviews"].append(
            {
                "user": {"login": author},
                "body": "<!-- cosmos-review-status:v9 -->",
                "state": "PENDING",
            }
        )
    assert classify(snapshot, CONTRACT) == "clean"


@pytest.mark.parametrize("bad", ["pending", "bad marker", "missing time", "equal time"])
def test_newer_or_unorderable_same_head_evidence_cannot_be_bypassed(snapshot, bad):
    newer = copy.deepcopy(snapshot["reviews"][-1])
    newer["id"] += 1
    newer["submitted_at"] = "2026-10-16T21:00:00Z"
    if bad == "pending":
        newer["state"] = "PENDING"
        newer["submitted_at"] = None
    elif bad == "bad marker":
        newer["body"] = "<!-- cosmos-review-status:v1 {} -->"
    elif bad == "missing time":
        newer.pop("submitted_at")
    else:
        newer["submitted_at"] = snapshot["reviews"][-1]["submitted_at"]
    snapshot["reviews"].insert(0, newer)
    assert_polling(snapshot)


def test_latest_review_order_uses_offset_aware_submission_not_creation(snapshot):
    newer = copy.deepcopy(snapshot["reviews"][-1])
    newer.update(
        id=123,
        submitted_at="2026-10-16T19:30:00-01:00",
        createdAt="2026-10-16T18:00:00Z",
        body="<!-- cosmos-review-status:v1 {} -->",
    )
    snapshot["reviews"].insert(0, newer)
    assert_polling(snapshot)


def test_graphql_review_shape_and_case_insensitive_full_sha(snapshot):
    for review in snapshot["reviews"]:
        review["author"] = review.pop("user")
        review["author"]["login"] = "augmentcode"
        review["commit"] = {"oid": review.pop("commit_id").upper()}
        review["submittedAt"] = review.pop("submitted_at")
    assert classify(snapshot, CONTRACT, current_head_sha=HEAD.upper()) == "clean"
    snapshot["reviews"][-1]["commit_id"] = OLD
    assert_polling(snapshot)


@pytest.mark.parametrize("flag", ["comments_ok", "reviews_ok", "threads_ok"])
@pytest.mark.parametrize("value", [False, None, "true", 1, "missing"])
def test_a11_incomplete_flags_block_both_public_seams(snapshot, flag, value):
    snapshot["threads"][0]["isResolved"] = False
    if value == "missing":
        snapshot.pop(flag)
    else:
        snapshot[flag] = value
    assert_polling(snapshot)
    assert poll_succeeded(snapshot) is False


@pytest.mark.parametrize("surface", ["reviews", "comments", "threads"])
def test_malformed_complete_collection_does_not_look_empty(snapshot, surface):
    snapshot[surface] = None
    assert_polling(snapshot)


def test_a12_root_only_selection_and_human_root_with_bot_reply(snapshot):
    thread = snapshot["threads"][0]
    thread["isResolved"] = False
    root = thread["comments"]["nodes"][0]
    reply = {**root, "id": "reply", "databaseId": 123, "replyTo": {"id": root["id"]}}
    thread["comments"]["nodes"].append(reply)
    assert len(actionable_finding_comments(snapshot, CONTRACT)) == 1
    root["author"]["login"] = "human"
    assert classify(snapshot, CONTRACT) == "clean"
    assert actionable_finding_comments(snapshot, CONTRACT) == []


@pytest.mark.parametrize(
    "mutation",
    [
        "missing location",
        "reply",
        "future",
        "missing origin",
        "bad outdated",
        "duplicate",
    ],
)
def test_incomplete_or_ambiguous_root_never_dispatches_partial_findings(
    snapshot, mutation
):
    thread = snapshot["threads"][0]
    thread["isResolved"] = False
    root = thread["comments"]["nodes"][0]
    if mutation == "missing location":
        root["originalLine"] = None
    elif mutation == "reply":
        root["replyTo"] = {"id": "human-root"}
    elif mutation == "future":
        root["createdAt"] = "2026-10-16T21:00:00Z"
    elif mutation == "missing origin":
        root["pullRequestReview"] = None
    elif mutation == "bad outdated":
        thread["isOutdated"] = None
    else:
        snapshot["threads"].append(copy.deepcopy(thread))
    assert_polling(snapshot)


def test_a15_decline_precedence_only_valid_completion_overrides(snapshot):
    decline = {
        "user": {"login": "augmentcode[bot]"},
        "created_at": "2026-10-16T19:45:00Z",
        "body": 'abnormally large; comment "auggie review"',
    }
    snapshot["comments"].append(decline)
    assert classify(snapshot, CONTRACT) == "declined"
    assert classify(snapshot, CONTRACT, watermark=WATERMARK) == "clean"
    set_marker(snapshot, status="pending")
    assert classify(snapshot, CONTRACT, watermark=WATERMARK) == "declined"
    assert actionable_finding_comments(snapshot, CONTRACT, watermark=WATERMARK) == []


def test_a15_legacy_synthetic_and_explicit_attribution():
    review = {
        "user": {"login": "augmentcode[bot]"},
        "state": "COMMENTED",
        "has_findings": True,
    }
    payload = {"reviews": [review], "comments": []}
    assert classify(payload, CONTRACT) == "findings"
    review["has_findings"] = False
    assert classify(payload, CONTRACT) == "clean"
    assert_polling(payload, watermark=WATERMARK)
    payload["head_sha"] = HEAD
    assert_polling(payload)
    review.update(commit_id=OLD, submitted_at="2026-10-16T20:00:00Z")
    assert_polling(payload)
    review["commit_id"] = HEAD
    assert classify(payload, CONTRACT, watermark=WATERMARK) == "clean"
    payload["comments_ok"] = False
    assert_polling(payload)


def test_poll_seam_forwards_both_context_arguments(snapshot, mock_gh):
    mock_gh.payload = snapshot
    assert (
        poll_augment_review(
            266, contract=CONTRACT, watermark=WATERMARK, current_head_sha=HEAD
        )
        == "clean"
    )
    assert (
        poll_augment_review(
            266, contract=CONTRACT, watermark=WATERMARK, current_head_sha=OLD
        )
        == "polling"
    )
    assert (
        poll_augment_review(
            266,
            payload=snapshot,
            contract=CONTRACT,
            watermark="2026-10-16T20:00:00Z",
            current_head_sha=HEAD,
        )
        == "polling"
    )
    assert mock_gh.calls == [266, 266]


@pytest.mark.parametrize("created_field", ["createdAt", "created_at"])
def test_formal_cosmos_creation_time_cannot_replace_submission(snapshot, created_field):
    review = snapshot["reviews"][-1]
    review[created_field] = review.pop("submitted_at")
    assert_polling(snapshot, watermark=WATERMARK)
    # The GraphQL spelling of the actual submission time restores attribution.
    review["submittedAt"] = review[created_field]
    assert classify(snapshot, CONTRACT, watermark=WATERMARK) == "clean"


@pytest.mark.parametrize("head", [None, "", True, "short", {}])
def test_explicit_malformed_legacy_head_is_not_contextfree(head):
    review = {"user": {"login": "augmentcode[bot]"}, "state": "COMMENTED"}
    payload = {"reviews": [review], "comments": []}
    assert classify(payload, CONTRACT) == "clean"
    payload["head_sha"] = head
    assert_polling(payload)


@pytest.mark.parametrize("has_commit", [False, True])
def test_legacy_watermark_requires_expected_head_and_commit(has_commit):
    review = {
        "user": {"login": "augmentcode[bot]"},
        "state": "COMMENTED",
        "submitted_at": "2026-10-16T20:00:00Z",
    }
    if has_commit:
        review["commit_id"] = HEAD
    payload = {"reviews": [review], "comments": []}
    assert_polling(payload, watermark=WATERMARK)
    payload["head_sha"] = HEAD
    if has_commit:
        assert classify(payload, CONTRACT, watermark=WATERMARK) == "clean"
    else:
        assert_polling(payload, watermark=WATERMARK)


@pytest.mark.parametrize(
    "observed", ["missing", None, "bad", True, 123, {}, [], "2026-10-16T22:00:00"]
)
def test_cosmos_requires_trustworthy_snapshot_observation(snapshot, observed):
    if observed == "missing":
        snapshot.pop("observed_at")
    else:
        snapshot["observed_at"] = observed
    assert_polling(snapshot)
    assert poll_succeeded(snapshot) is False


@pytest.mark.parametrize("submission", ["2026-10-16T22:00:01Z", "9999-01-01T00:00:00Z"])
def test_future_submission_cannot_establish_completion_or_bypass_newer_evidence(
    snapshot, submission
):
    future = copy.deepcopy(snapshot["reviews"][-1])
    future["id"] += 1
    future["submitted_at"] = submission
    snapshot["reviews"].insert(0, future)
    assert_polling(snapshot)


def test_observation_boundary_is_inclusive_and_timezone_aware(snapshot):
    snapshot["observed_at"] = "2026-10-16T22:00:00+02:00"
    assert classify(snapshot, CONTRACT) == "clean"
    snapshot["observed_at"] = "2026-10-16T22:00:00+03:00"
    assert_polling(snapshot)


def test_contextual_legacy_observation_rejects_future_or_invalid_evidence():
    review = {
        "user": {"login": "augmentcode[bot]"},
        "state": "COMMENTED",
        "commit_id": HEAD,
        "submitted_at": "2026-10-16T20:00:00Z",
    }
    payload = {"head_sha": HEAD, "reviews": [review], "comments": []}
    assert classify(payload, CONTRACT, watermark=WATERMARK) == "clean"
    payload["observed_at"] = "2026-10-16T19:59:59Z"
    assert_polling(payload, watermark=WATERMARK)
    payload["observed_at"] = None
    assert_polling(payload, watermark=WATERMARK)
    payload["observed_at"] = "2026-10-16T22:00:00Z"
    review["createdAt"] = review.pop("submitted_at")
    assert_polling(payload, watermark=WATERMARK)


@pytest.fixture
def pr337(load_fixture):
    """Verbatim live poll snapshot of PR 337 (IronbellyOrg/IronClaude, 2026-10-31)."""
    return load_fixture("cosmos-pr337.json")


def _pr337_root(snapshot):
    return snapshot["threads"][0]["comments"]["nodes"][0]


def test_a6_pr337_root_one_second_after_its_review_is_a_finding(pr337):
    """Design 18 A6: a root of the completed review posted after its submission counts."""
    assert pr337["reviews"][-1]["submitted_at"] == "2026-10-31T21:22:29Z"
    assert _pr337_root(pr337)["createdAt"] == "2026-10-31T21:22:30Z"
    assert classify(pr337, CONTRACT) == "findings"
    selected = actionable_finding_comments(pr337, CONTRACT)
    assert [root["comment_id"] for root in selected] == [4433345498]
    assert selected[0]["review_id"] == 5724978140
    watermark = "2026-10-31T21:20:00Z"  # an attributed re-review on the same head
    assert classify(pr337, CONTRACT, watermark=watermark) == "findings"


@pytest.mark.parametrize(
    "origin",
    ["older head review", "other review on the head", "completed id, old head"],
)
def test_a6_newer_root_outside_the_completed_review_still_polls(pr337, origin):
    root = _pr337_root(pr337)
    head = pr337["head_sha"]
    if origin == "older head review":
        older = copy.deepcopy(pr337["reviews"][-1])
        older.update(id=5724900000, node_id="PRR_older", commit_id=OLD)
        older["submitted_at"] = "2026-10-31T21:00:00Z"
        pr337["reviews"].insert(0, older)
        ref = {"id": "PRR_older", "databaseId": 5724900000, "commit": {"oid": OLD}}
        root["pullRequestReview"] = ref
    elif origin == "other review on the head":
        ref = {"id": "PRR_other", "databaseId": 5724999999, "commit": {"oid": head}}
        root["pullRequestReview"] = ref
    else:
        root["pullRequestReview"]["commit"]["oid"] = OLD
    assert_polling(pr337)
    # The same root created no later than the review submission is selected.
    root["createdAt"] = "2026-10-31T21:22:29Z"
    assert classify(pr337, CONTRACT) == "findings"


def test_poll_success_missing_additive_flags_is_legacy_only(snapshot):
    legacy = {"head_sha": HEAD, "reviews": [], "comments": []}
    assert poll_succeeded(legacy) is True
    snapshot["reviews"][-1]["body"] = snapshot["reviews"][-1]["body"].split("<!--")[0]
    snapshot.pop("threads_ok")
    assert poll_succeeded(snapshot) is False
