"""Issues #382 and #456: a finished Augment review whose status marker cannot be read.

Real review bodies, fetched with ``gh api`` and saved as fixtures:

- ``cosmos-pr377-malformed-marker.json``: PR 377 review 5776522857 (marker ends ``..." -->``, no ``}``).
- ``cosmos-pr455-malformed-marker.json``: PR 455 review 5819041100 (same defect; "1 suggestion").
- ``cosmos-pr455-malformed-then-good.json``: PR 455 reviews 5819088356 (malformed, 18:29:51Z) and
  5819089721 (well formed, 18:30:18Z, 27 s later) on one head.

Rule under test (written once in ``refs/detection-contract.md``): the strict marker parse is unchanged, so an
unreadable marker is never a clean review and hides nothing. When the newest Augment review of the expected
head has a Cosmos marker that cannot be read, ``augment_marker_defect`` names the reason at once. After a
60 s grace window (a corrected review can follow within seconds) the Augment wait is ``incomplete``
instead of ``pending`` and the round continues with Codex, or ends as a timeout when Codex is absent.
A later readable review of the same head is still accepted by the unchanged ``classify``.
"""

from __future__ import annotations

import copy

import pytest

import superclaude.pr_submit as pr
from superclaude.pr_submit import (
    DetectionContract,
    actionable_finding_comments,
    augment_wait_outcome,
    classify,
    merge_wait,
)
from superclaude.pr_submit.fsm import poll_outcome
from superclaude.pr_submit.models import MonitorState

CONTRACT = DetectionContract(
    augment_bot_login="augmentcode[bot]", augment_app_slug="augmentcode"
)


def defect(payload, **context):
    return pr.augment_marker_defect(payload, CONTRACT, **context)


@pytest.fixture
def pr377(load_fixture):
    return load_fixture("cosmos-pr377-malformed-marker.json")


@pytest.fixture
def pr455(load_fixture):
    return load_fixture("cosmos-pr455-malformed-marker.json")


@pytest.fixture
def pr455_good_later(load_fixture):
    return load_fixture("cosmos-pr455-malformed-then-good.json")


def test_fixtures_are_the_real_malformed_bodies(pr377, pr455):
    for payload, review_id in ((pr377, 5776522857), (pr455, 5819041100)):
        review = payload["reviews"][0]
        assert review["id"] == review_id
        assert (
            review["body"].rstrip().endswith('" -->')
        )  # the closing brace is the missing piece


@pytest.mark.parametrize("name", ["pr377", "pr455"])
def test_master_behaviour_kept_strict_parse_is_polling_never_clean(request, name):
    payload = request.getfixturevalue(name)
    assert (
        classify(payload, CONTRACT, current_head_sha=payload["head_sha"]) == "polling"
    )
    assert actionable_finding_comments(payload, CONTRACT) == []


@pytest.mark.parametrize("name", ["pr377", "pr455"])
def test_malformed_marker_is_named_within_one_poll(request, name):
    payload = request.getfixturevalue(name)
    found = defect(payload)
    assert found is not None
    assert found["reason"] == "marker_not_valid_json"
    assert found["review_id"] == payload["reviews"][0]["id"]
    assert found["submitted_at"] == payload["reviews"][0]["submitted_at"]
    assert found["settled"] is True  # observed 90 s after the review in the fixtures
    assert found["grace_seconds"] == 60


def test_grace_window_then_settled(pr377):
    pr377["observed_at"] = "2026-11-04T22:05:09Z"  # 20 s after the review
    early = defect(pr377)
    assert early["reason"] == "marker_not_valid_json" and early["settled"] is False
    pr377["observed_at"] = "2026-11-04T22:05:49Z"  # exactly 60 s
    assert defect(pr377)["settled"] is True


def test_wait_outcome_pending_in_grace_incomplete_after_never_done(pr377):
    state = classify(pr377, CONTRACT)
    nxt = poll_outcome(state, 30, 600)
    pr377["observed_at"] = "2026-11-04T22:05:09Z"
    assert augment_wait_outcome(state, nxt, marker_defect=defect(pr377)) == "pending"
    pr377["observed_at"] = "2026-11-04T22:06:19Z"
    assert augment_wait_outcome(state, nxt, marker_defect=defect(pr377)) == "incomplete"
    # Without the defect (old callers) nothing changes: still pending until the timeout.
    assert augment_wait_outcome(state, nxt) == "pending"


def test_augment_only_pr_ends_as_timeout_with_a_reason_not_a_silent_full_wait(pr377):
    state = classify(pr377, CONTRACT)
    aug = augment_wait_outcome(
        state, poll_outcome(state, 120, 600), marker_defect=defect(pr377)
    )
    result = merge_wait((aug, state), ("absent", "polling"))
    assert result["outcome"] == "timeout"  # never "clean"
    assert result["incomplete"] == ["augment"] and result["used"] == []


def test_codex_clean_carries_the_round_and_augment_is_reported_incomplete(pr377):
    state = classify(pr377, CONTRACT)
    aug = augment_wait_outcome(
        state, poll_outcome(state, 120, 600), marker_defect=defect(pr377)
    )
    result = merge_wait((aug, state), ("done", "clean"))
    assert result["outcome"] == "clean" and result["used"] == ["codex"]
    assert result["incomplete"] == [
        "augment"
    ]  # becomes reviewer_incomplete{reviewer: augment}


def test_codex_still_pending_keeps_the_round_polling(pr377):
    state = classify(pr377, CONTRACT)
    aug = augment_wait_outcome(
        state, poll_outcome(state, 120, 600), marker_defect=defect(pr377)
    )
    assert merge_wait((aug, state), ("pending", "polling"))["outcome"] == "polling"


def test_later_readable_review_of_the_same_head_is_still_accepted(pr455_good_later):
    head = pr455_good_later["head_sha"]
    assert classify(pr455_good_later, CONTRACT, current_head_sha=head) == "clean"
    assert defect(pr455_good_later) is None
    assert (
        augment_wait_outcome(
            "clean", MonitorState.S2_CLASSIFY, marker_defect=defect(pr455_good_later)
        )
        == "done"
    )


def test_malformed_review_alone_in_that_pair_is_flagged_until_the_good_one_arrives(
    pr455_good_later,
):
    pr455_good_later["reviews"] = pr455_good_later["reviews"][
        :1
    ]  # the 18:29:51Z one only
    pr455_good_later["observed_at"] = "2026-11-08T18:30:00Z"
    found = defect(pr455_good_later)
    assert found["review_id"] == 5819088356 and found["settled"] is False


def test_open_findings_of_the_unreadable_review_are_surfaced_not_hidden(load_fixture):
    payload = load_fixture("cosmos-pr377-late-comment.json")
    review = payload["reviews"][0]
    review["body"] = (
        review["body"].rstrip().removesuffix("} -->") + " -->"
    )  # the real defect, applied
    payload["observed_at"] = "2026-11-04T21:47:00Z"
    assert classify(payload, CONTRACT) == "polling"  # strict parse unchanged
    found = defect(payload)
    assert found["reason"] == "marker_not_valid_json"
    assert found["open_threads"] == [4473733769]  # operator must read this by hand


def test_no_open_threads_is_an_empty_list_not_none(pr377):
    assert defect(pr377)["open_threads"] == []


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(
            lambda p: p["reviews"][0].update(commit_id="0" * 39 + "1"),
            id="review-on-another-head",
        ),
        pytest.param(
            lambda p: p.update(head_sha="0" * 39 + "1"), id="expected-head-moved"
        ),
        pytest.param(
            lambda p: p["reviews"][0]["user"].update(login="someone-else"),
            id="not-augment",
        ),
        pytest.param(lambda p: p.update(reviews_ok=False), id="reviews-incomplete"),
        pytest.param(lambda p: p.update(threads_ok=False), id="threads-incomplete"),
        pytest.param(
            lambda p: p.update(observed_at="2026-11-04T22:00:00Z"),
            id="review-after-observation",
        ),
        pytest.param(lambda p: p.pop("observed_at"), id="no-observation-time"),
        pytest.param(
            lambda p: p["reviews"][0].update(state="PENDING"), id="pending-review"
        ),
        pytest.param(
            lambda p: p["reviews"][0].update(submitted_at=None), id="no-submission-time"
        ),
    ],
)
def test_no_defect_unless_everything_ties_the_review_to_this_poll(pr377, mutate):
    mutate(pr377)
    assert defect(pr377) is None
    assert classify(pr377, CONTRACT) == "polling"


def test_older_than_the_retrigger_watermark_is_not_a_defect(pr377):
    assert defect(pr377, watermark="2026-11-04T22:04:49Z") is None  # not strictly newer
    assert (
        defect(pr377, watermark="2026-11-04T22:04:00Z")["reason"]
        == "marker_not_valid_json"
    )


@pytest.mark.parametrize(
    "marker",
    [
        '{"specialist":"deep","status":"running","baseline":"%s","head":"%s","unresolved_count":0}',
        '{"specialist":"deep","status":"reviewed","head":"nope","unresolved_count":0}',
    ],
)
def test_valid_json_with_wrong_fields_is_not_a_malformed_marker(pr377, marker):
    # In-progress or incomplete-but-parseable markers keep polling as before; only an unreadable one is named.
    head = pr377["head_sha"]
    pr377["reviews"][0]["body"] = (
        "x\n<!-- cosmos-review-status:v1 "
        + (marker % (head, head) if "%s" in marker else marker)
        + " -->"
    )
    assert defect(pr377) is None
    assert classify(pr377, CONTRACT) == "polling"


@pytest.mark.parametrize(
    "tail,reason",
    [
        (' {"specialist":"deep" -->', "marker_not_valid_json"),
        (" [1,2] -->", "marker_not_an_object"),
        (" null -->", "marker_not_an_object"),
        (' {"a":1,"a":2} -->', "marker_not_valid_json"),
        (' {"specialist":"deep"', "marker_comment_unreadable"),  # no closing -->
    ],
)
def test_reason_names_how_the_marker_is_unreadable(pr377, tail, reason):
    pr377["reviews"][0]["body"] = (
        "Review completed with 0 suggestions.\n<!-- cosmos-review-status:v1" + tail
    )
    assert defect(pr377)["reason"] == reason


def test_two_marker_tokens_keep_the_old_silent_poll(pr377):
    pr377["reviews"][0]["body"] += "\n<!-- cosmos-review-status:v2 {} -->"
    assert defect(pr377) is None  # ambiguous, not "present once": unchanged behaviour


def test_review_without_any_cosmos_token_is_not_a_defect(pr377):
    pr377["reviews"][0]["body"] = "plain review text"
    assert defect(pr377) is None


def test_helper_does_not_mutate_the_payload(pr377):
    before = copy.deepcopy(pr377)
    defect(pr377)
    assert pr377 == before


def test_non_dict_payload_is_none():
    assert pr.augment_marker_defect(None, CONTRACT) is None
    assert pr.augment_marker_defect({"reviews": "x"}, CONTRACT) is None
