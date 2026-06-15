"""Regression tests locking in the Augment-review remediation on PR #174.

Each test pins a fix for a specific Augment finding (GitHub review-comment id cited in
the docstring) so the V1.1-regression class the reviewer flagged cannot silently return.
These edge cases were UNCOVERED before remediation (which is why no existing test failed
on the defects). See the troubleshoot REPORT for the full per-finding log.
"""

from __future__ import annotations

import datetime

import pytest

from superclaude.pr_submit import DetectionContract, classify, is_decline
from superclaude.pr_submit.fsm import RunConfig, run_skill
from superclaude.pr_submit.models import Finding, MonitorState
from superclaude.pr_submit.recovery import (
    BRANCH_A_LANDED,
    detect_crash_window,
    resolve_crash_window,
)
from superclaude.pr_submit.run_log import RunLog

AUGMENT = "augment-code[bot]"


@pytest.fixture
def contract() -> DetectionContract:
    return DetectionContract(
        augment_bot_login=AUGMENT,
        emission_shape="review",
        findings_locus="comments[]",
        locked=True,
    )


# --- #1 (comment 3410814003): finding-comment must carry an inline locus ----------


def test_pathless_augment_comment_is_not_a_finding(contract):
    """A bare/summary Augment comment (no path/line) must NOT classify as findings —
    restores the V1.0 inline-locus guard the V1.1 refactor dropped."""
    payload = {
        "reviews": [{"user": {"login": AUGMENT}, "state": "COMMENTED"}],
        "comments": [
            {
                "user": {"login": AUGMENT},
                "body": "Review completed. 6 suggestions posted.",
            }
        ],
    }
    assert classify(payload, contract) == "clean"


def test_inline_augment_comment_is_still_a_finding(contract):
    """A genuine inline comment (path + int line + body) still classifies as findings."""
    payload = {
        "reviews": [{"user": {"login": AUGMENT}, "state": "COMMENTED"}],
        "comments": [
            {"user": {"login": AUGMENT}, "path": "a.py", "line": 5, "body": "bug here"}
        ],
    }
    assert classify(payload, contract) == "findings"


# --- #2 (comment 3410814005): timestamp compare must be fail-safe -----------------


def test_mixed_type_watermark_does_not_raise(contract):
    """A non-order-comparable watermark (datetime vs ISO string) must not raise
    TypeError — the un-comparable timestamp is treated as not-newer (fail-safe)."""
    decline = {
        "user": {"login": AUGMENT},
        "body": "This PR is abnormally large. Comment `auggie review` to retry.",
        "createdAt": "2026-06-15T03:00:00Z",
    }
    payload = {"reviews": [], "comments": [decline]}
    wm = datetime.datetime(2026, 6, 15)  # not comparable to the ISO string
    # Pre-fix this raised TypeError; now it fails safe → stale → not declined → polling.
    assert classify(payload, contract, watermark=wm) == "polling"


# --- #7 (comment 3410821753): is_decline must read submittedAt --------------------


def test_decline_as_review_with_submittedat_is_staleness_checked(contract):
    """A decline arriving as a REVIEW object (only submittedAt) must be staleness-checked
    via submittedAt — pre-fix is_decline only read createdAt/created_at and dropped it."""
    decline_review = {
        "user": {"login": AUGMENT},
        "body": "abnormally large — comment `auggie review`",
        "submittedAt": "2026-06-15T03:00:00Z",
    }
    # Watermark NEWER than the decline → stale → ignored.
    assert (
        is_decline(decline_review, contract, watermark="2026-06-15T04:00:00Z") is False
    )
    # Watermark OLDER → fresh decline → detected (this assertion FAILS pre-fix).
    assert (
        is_decline(decline_review, contract, watermark="2026-06-15T02:00:00Z") is True
    )


# --- #8 (comment 3410821755): scalar YAML field must not char-split ----------------


def test_scalar_accepted_trigger_phrases_not_charsplit():
    """A scalar YAML string for accepted_trigger_phrases must become a one-element list,
    not a list of characters."""
    c = DetectionContract.from_yaml(
        {
            "augment_bot_login": AUGMENT,
            "locked": True,
            "accepted_trigger_phrases": "auggie review",
        }
    )
    assert c.accepted_trigger_phrases == ["auggie review"]


# --- #4 (comment 3410814011): missing cycle_id must fail safe to S5A ---------------


def test_recovery_missing_cycle_id_resumes_s5a(tmp_path):
    """When the dangling push carries no cycle_id, recovery must fail safe to
    S5A_RETRIGGER_REVIEW (re-post the re-trigger) rather than assume a prior re-trigger
    for some OTHER cycle was attributable to this push."""
    rl = RunLog(174, tmp_path)
    rl.append(
        {
            "event_type": "push_initiated",
            "target_sha": "shaX",
            "idempotency_key": "push:r:nocycle:preX:feat",
            "run_id": "r",
            "pre_push_sha": "preX",
            "target_branch": "feat",
            "target_remote": "origin",
        }
    )
    # A prior re-trigger exists, but for a DIFFERENT cycle — not attributable here.
    rl.append({"event_type": "rereview_requested", "cycle_id": "other"})

    dangling = detect_crash_window(rl)
    assert dangling is not None and dangling.get("cycle_id") is None
    branch, resume_state = resolve_crash_window(rl, dangling, remote_reachable=True)
    assert branch == BRANCH_A_LANDED
    # Pre-fix this returned S5_AWAITING_REREVIEW (wrongly assumed already-emitted).
    assert resume_state == MonitorState.S5A_RETRIGGER_REVIEW


# --- #10 (comment 3410830432): unverified human-decision fallback must HALT --------


def test_unverified_human_decision_fallback_halts():
    """An unverified needs_human_decision fallback finding must HALT_HUMAN, not be
    auto-defaulted to TERMINAL_CLEAN via the no-verified→clean path."""
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            review_state="declined",
            fallback_findings=[
                Finding(
                    path="src/x.py",
                    line=1,
                    body="needs a human call",
                    in_diff=True,
                    verification_status="verified",
                    needs_human_decision=True,
                    comment_id=9001,
                )
            ],
            verify=lambda _f: (
                False
            ),  # unverified → pre-fix fell through to TERMINAL_CLEAN
        )
    )
    assert result.state == MonitorState.HALT_HUMAN
