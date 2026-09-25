"""Silence / no-activity detection for sc:pr-submit (PR-SUBMIT-AUGMENT-NO-RESPONSE)."""

from __future__ import annotations

import pytest

from superclaude.pr_submit import (
    DetectionContract,
    classify,
    has_augment_activity,
    poll_succeeded,
)
from superclaude.pr_submit.fsm import (
    DEFAULT_SILENCE_TIMEOUT,
    parse_args,
    poll_outcome,
    transition,
)
from superclaude.pr_submit.models import MonitorState, SkillResult

LIVE = DetectionContract(
    augment_bot_login="augmentcode[bot]",
    augment_app_slug="augmentcode",
    locked=True,
)


def test_silence_empty_is_not_activity(load_fixture):
    payload = load_fixture("silence-empty.json")
    assert has_augment_activity(payload, LIVE) is False
    assert poll_succeeded(payload) is True
    assert classify(payload, LIVE) == "polling"


def test_fail_soft_empty_is_not_silence(load_fixture):
    payload = load_fixture("fail-soft-empty.json")
    assert poll_succeeded(payload) is False
    assert has_augment_activity(payload, LIVE) is False
    silent = poll_succeeded(payload) and not has_augment_activity(payload, LIVE)
    assert silent is False
    assert (
        poll_outcome("polling", 300, 600, silent=silent, monitor_ordinal=3)
        == MonitorState.S2_CLASSIFY
    )


def test_comment_fetch_miss_is_not_silence():
    payload = {
        "pr": 243,
        "head_sha": "abc",
        "comments_ok": False,
        "reviews": [],
        "comments": [],
    }
    assert poll_succeeded(payload) is False
    silent = poll_succeeded(payload) and not has_augment_activity(payload, LIVE)
    assert silent is False


def test_opt_in_241_is_activity_and_declined(load_fixture):
    payload = load_fixture("opt-in-241.json")
    assert has_augment_activity(payload, LIVE) is True
    assert classify(payload, LIVE) == "declined"


def test_summary_only_is_activity_and_polling(load_fixture):
    payload = load_fixture("summary-only.json")
    assert has_augment_activity(payload, LIVE) is True
    assert classify(payload, LIVE) == "polling"


def test_empty_identity_is_not_activity(load_fixture):
    payload = load_fixture("summary-only.json")
    assert has_augment_activity(payload, DetectionContract()) is False


def test_l1_silent_at_silence_timeout_is_no_response():
    assert (
        poll_outcome(
            "polling",
            300,
            600,
            silent=True,
            silence_timeout=300,
            monitor_ordinal=1,
        )
        == MonitorState.TERMINAL_AUGMENT_NO_RESPONSE
    )


def test_l3_silent_at_300_of_600_is_rerequest_sentinel():
    result = SkillResult()
    state = poll_outcome(
        "polling",
        300,
        600,
        silent=True,
        silence_timeout=300,
        monitor_ordinal=3,
    )
    assert state == MonitorState.S5C_SILENCE_REREQUEST
    assert result.round_counter == 0


def test_l3_already_requested_at_timeout_is_no_response():
    assert (
        poll_outcome(
            "polling",
            600,
            600,
            silent=True,
            silence_timeout=300,
            rerequested=True,
            rerequested_at=300,
            monitor_ordinal=3,
        )
        == MonitorState.TERMINAL_AUGMENT_NO_RESPONSE
    )


def test_summary_only_timeout_is_terminal_timeout(load_fixture):
    payload = load_fixture("summary-only.json")
    assert has_augment_activity(payload, LIVE) is True
    assert (
        poll_outcome("polling", 600, 600, silent=False) == MonitorState.TERMINAL_TIMEOUT
    )


def test_declined_still_routes_to_s5b():
    assert (
        transition(MonitorState.S2_CLASSIFY, "declined")
        == MonitorState.S5B_AUGGIE_FALLBACK
    )
    assert (
        transition(MonitorState.S5_AWAITING_REREVIEW, "declined")
        == MonitorState.S5B_AUGGIE_FALLBACK
    )


def test_t221_positional_polling_still_terminal_timeout():
    assert (
        poll_outcome("polling", elapsed_seconds=1800, timeout=1800)
        == MonitorState.TERMINAL_TIMEOUT
    )


def test_silence_timeout_flag_default_min_and_clamp():
    assert parse_args([]).silence_timeout == DEFAULT_SILENCE_TIMEOUT == 300
    with pytest.raises(ValueError, match="minimum is 30 seconds"):
        parse_args(["--silence-timeout", "29"])
    assert parse_args(["--silence-timeout", "30"]).silence_timeout == 30
    clamped = parse_args(["--timeout", "120", "--silence-timeout", "300"])
    assert clamped.silence_timeout == 120


def test_l3_second_wait_keeps_polling_before_deadline():
    assert (
        poll_outcome(
            "polling",
            400,
            600,
            silent=True,
            silence_timeout=300,
            rerequested=True,
            rerequested_at=300,
            monitor_ordinal=3,
        )
        == MonitorState.S2_CLASSIFY
    )


def test_rerequested_without_clock_stays_polling():
    assert (
        poll_outcome(
            "polling",
            300,
            600,
            silent=True,
            silence_timeout=300,
            rerequested=True,
            rerequested_at=None,
            monitor_ordinal=3,
        )
        == MonitorState.S2_CLASSIFY
    )


def test_rerequested_without_clock_still_times_out():
    assert (
        poll_outcome(
            "polling",
            600,
            600,
            silent=True,
            silence_timeout=300,
            rerequested=True,
            rerequested_at=None,
            monitor_ordinal=3,
        )
        == MonitorState.TERMINAL_AUGMENT_NO_RESPONSE
    )


def test_already_rerequested_at_same_elapsed_is_not_s5c():
    assert (
        poll_outcome(
            "polling",
            300,
            600,
            silent=True,
            silence_timeout=300,
            rerequested=True,
            rerequested_at=300,
            monitor_ordinal=3,
        )
        == MonitorState.S2_CLASSIFY
    )
