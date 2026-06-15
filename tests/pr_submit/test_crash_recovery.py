"""Crash-recovery tests (spec §12.2 FM-1..FM-12 + §12.1 INV-007 crash window).

Each FM in the catalog has a recovery semantic; plus T-CRASH-WINDOW-NO-DOUBLE-PUSH
(Branch-A landed): `push_count == 2`, `resume_state == S5_AWAITING_REREVIEW`,
`push_completed.recovered == True` — and crucially NO second actual push.
"""

from __future__ import annotations

import pytest

from superclaude.pr_submit.classifier import classify
from superclaude.pr_submit.detection import DetectionContract
from superclaude.pr_submit.fsm import (
    RunConfig,
    next_backoff,
    poll_outcome,
    run_skill,
)
from superclaude.pr_submit.models import Finding, MonitorState
from superclaude.pr_submit.recovery import (
    BRANCH_A_LANDED,
    BRANCH_B_NOT_LANDED,
    BRANCH_C_AMBIGUOUS,
    detect_crash_window,
    resolve_crash_window,
)
from superclaude.pr_submit.run_log import RunLog

AUGMENT = "augment-code[bot]"
CONTRACT = DetectionContract(augment_bot_login=AUGMENT, locked=True)


def _vf(line=1, **kw) -> Finding:
    base = dict(
        path="src/a.py", body="bug", in_diff=True, verification_status="verified"
    )
    base.update(kw)
    return Finding(line=line, **base)


@pytest.mark.recovery
def test_fm1_review_never_arrives_timeout():
    """FM-1: review never arrives → terminal_timeout, no edits/push."""
    assert poll_outcome("polling", 1800, 1800) == MonitorState.TERMINAL_TIMEOUT


@pytest.mark.recovery
def test_fm2_rate_limit_backoff():
    """FM-2: primary/secondary rate limit → exponential backoff (continues to timeout)."""
    assert next_backoff(30) == 60
    assert next_backoff(60) == 120


@pytest.mark.recovery
def test_fm3_unknown_shape_keep_polling():
    """FM-3: unknown Augment emission shape → keep polling (no Augment review detected)."""
    # A payload with no recognizable Augment review classifies as polling.
    assert (
        classify(
            {"reviews": [{"author": {"login": "weird-bot"}}], "comments": []}, CONTRACT
        )
        == "polling"
    )


@pytest.mark.recovery
def test_fm4_unknown_bot_ignored():
    """FM-4: unknown bot identity → ignored as no-review (fail-safe, NFR-4)."""
    assert (
        classify(
            {
                "reviews": [
                    {"author": {"login": "github-actions[bot]"}, "has_findings": True}
                ],
                "comments": [],
            },
            CONTRACT,
        )
        == "polling"
    )


@pytest.mark.recovery
def test_fm5_validation_failure_no_push():
    """FM-5: validation failure → no push/reply/resolve."""
    result = run_skill(
        RunConfig(
            monitor_ordinal=3, findings=[_vf()], run_validation=lambda **_: "failed"
        )
    )
    assert result.state == MonitorState.VALIDATION_FAIL
    assert result.push_count == 0


@pytest.mark.recovery
def test_fm6_crash_after_push_before_reply_no_refix(tmp_path):
    """FM-6: crash after push before reply → resume posts the missing reply once, no re-fix."""
    rl = RunLog(6, tmp_path)
    fk = "fixkey-6"
    rl.append({"event_type": "fix_applied", "fix_key": fk})
    rl.append(
        {
            "event_type": "push_completed",
            "target_sha": "sha6",
            "idempotency_key": "push:r:c:pre:feat",
        }
    )
    # No reply yet. On resume the fix is already recorded → not re-applied.
    assert rl.check_idempotent("processed_finding_ids", fk) is False  # skip re-fix
    # The reply is still pending (not yet in replied set).
    assert rl.check_idempotent("replied_comment_ids", 600) is True


@pytest.mark.recovery
def test_fm7_crash_after_reply_before_resolve(tmp_path):
    """FM-7: crash after reply before resolve → resolve the missing thread, no duplicate reply."""
    rl = RunLog(7, tmp_path)
    rl.check_idempotent("replied_comment_ids", 700)
    rl.append({"event_type": "reply_posted", "comment_id": 700})
    # Resume: reply already done (skip duplicate), resolve still pending.
    assert rl.check_idempotent("replied_comment_ids", 700) is False
    assert rl.check_idempotent("resolved_thread_ids", "PRRT_700") is True


@pytest.mark.recovery
def test_fm8_duplicate_payload_idempotency_skip(tmp_path):
    """FM-8: duplicate review/poll payload → idempotency_skip, no route/fix/reply."""
    rl = RunLog(8, tmp_path)
    assert rl.check_idempotent("processed_review_ids", 880) is True
    rl.append(
        {"event_type": "findings_normalized", "review_id": 880}
    )  # records the review id
    assert (
        rl.check_idempotent("processed_review_ids", 880) is False
    )  # duplicate skipped


@pytest.mark.recovery
def test_fm9_round_cap_residual_terminal_max_rounds():
    """FM-9: round cap with residual findings → terminal_max_rounds."""
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=1,
            findings=[_vf(1)],
            rereview_findings=[[_vf(2, comment_id=2)]],
        )
    )
    assert result.state == MonitorState.HALT_MAX_ROUNDS


@pytest.mark.recovery
def test_fm10_needs_human_terminal_halted():
    """FM-10: needs_human_decision finding → terminal_halted, no auto-mutation."""
    result = run_skill(
        RunConfig(monitor_ordinal=3, findings=[_vf(needs_human_decision=True)])
    )
    assert result.state == MonitorState.HALT_HUMAN
    assert result.push_count == 0


@pytest.mark.recovery
def test_fm11_misrouted_pr_terminal_failed():
    """FM-11: a misrouted PR URL (wrong owner) → terminal_failed; do not monitor."""
    from superclaude.pr_submit.fsm import pr_target_ok  # owner verification helper

    assert pr_target_ok("https://github.com/IronbellyOrg/IronClaude/pull/5") is True
    assert (
        pr_target_ok("https://github.com/SuperClaude-Org/SuperClaude_Framework/pull/5")
        is False
    )


@pytest.mark.recovery
def test_fm12_corrupt_run_log_terminal_failed(tmp_path):
    """FM-12: a corrupt run-log line → surfaced (not silently trusted)."""
    rl = RunLog(12, tmp_path)
    rl.append({"event_type": "run_started"})
    # Corrupt the JSONL with a non-parseable line.
    with rl.jsonl_path.open("a", encoding="utf-8") as fh:
        fh.write("{not valid json\n")
    import json as _json

    with pytest.raises(_json.JSONDecodeError):
        rl.read_events()


@pytest.mark.recovery
def test_crash_window_no_double_push(tmp_path, load_fixture):
    """T-CRASH-WINDOW-NO-DOUBLE-PUSH (Branch A): completion synthesized, no second push.

    Scenario mirrors crash-after-push-before-completed.json: one prior completed push
    + one dangling push_initiated. Branch A (target reachable on the remote) → append
    push_completed{recovered:true}; push_count==2; NO second actual push. Per V1.1/OQ-1,
    since NO rereview_requested event exists for the dangling cycle (the crash fell
    between push and re-trigger), recovery resumes at S5A_RETRIGGER_REVIEW to post the
    re-trigger comment.
    """
    # Parity: the dedicated fixture encodes exactly one dangling push_initiated
    # (a push_initiated whose idempotency_key has no matching push_completed).
    fixture = load_fixture("crash-after-push-before-completed.json")
    events = fixture["events"]
    completed_keys = {
        e["idempotency_key"] for e in events if e["event_type"] == "push_completed"
    }
    dangling_initiated = [
        e
        for e in events
        if e["event_type"] == "push_initiated"
        and e["idempotency_key"] not in completed_keys
    ]
    assert len(dangling_initiated) == 1  # the single crash-window push
    assert fixture["expected"]["push_count"] == 2
    assert fixture["expected"]["recovered"] is True

    rl = RunLog(99, tmp_path)
    # Prior completed push (cycle 1).
    rl.append(
        {
            "event_type": "push_completed",
            "target_sha": "sha1",
            "idempotency_key": "push:r:c1:pre1:feat",
        }
    )
    # Dangling push_initiated (cycle 2) — the crash window.
    rl.append(
        {
            "event_type": "push_initiated",
            "target_sha": "sha2",
            "idempotency_key": "push:r:c2:pre2:feat",
            "run_id": "r",
            "cycle_id": "c2",
            "pre_push_sha": "pre2",
            "target_branch": "feat",
            "target_remote": "origin",
        }
    )
    initiated_before = [
        e for e in rl.read_events() if e["event_type"] == "push_initiated"
    ]

    dangling = detect_crash_window(rl)
    assert dangling is not None
    branch, resume_state = resolve_crash_window(rl, dangling, remote_reachable=True)

    assert branch == BRANCH_A_LANDED
    # OQ-1: no rereview_requested for the dangling cycle → resume at S5a to POST the
    # re-trigger (the crash fell between push and re-trigger).
    assert resume_state == MonitorState.S5A_RETRIGGER_REVIEW
    state = rl.rebuild_state()
    assert state["push_count"] == 2  # both pushes now completed
    # The synthesized completion is flagged recovered.
    recovered = [
        e
        for e in rl.read_events()
        if e["event_type"] == "push_completed" and e.get("recovered")
    ]
    assert len(recovered) == 1 and recovered[0]["recovered"] is True
    # NO second actual push was initiated by recovery (no double push).
    initiated_after = [
        e for e in rl.read_events() if e["event_type"] == "push_initiated"
    ]
    assert len(initiated_after) == len(initiated_before)


@pytest.mark.recovery
def test_crash_window_branch_a_retrigger_already_emitted(tmp_path):
    """OQ-1 (V1.1): Branch A resumes at S5_AWAITING_REREVIEW (NOT S5a) when a
    rereview_requested event was already emitted for the dangling cycle — the re-trigger
    comment already went out, so re-posting it would double-post (INV-R1).
    """
    rl = RunLog(96, tmp_path)
    # Dangling push_initiated for cycle c1 (the crash window).
    rl.append(
        {
            "event_type": "push_initiated",
            "target_sha": "shaX",
            "idempotency_key": "push:r:c1:preX:feat",
            "run_id": "r",
            "cycle_id": "c1",
            "pre_push_sha": "preX",
            "target_branch": "feat",
            "target_remote": "origin",
        }
    )
    # The re-trigger comment for THIS cycle was already posted before the crash.
    rl.append({"event_type": "rereview_requested", "cycle_id": "c1"})

    dangling = detect_crash_window(rl)
    assert dangling is not None
    branch, resume_state = resolve_crash_window(rl, dangling, remote_reachable=True)

    assert branch == BRANCH_A_LANDED
    # re-trigger already emitted for cycle c1 → resume awaiting the re-review (no re-post).
    assert resume_state == MonitorState.S5_AWAITING_REREVIEW


@pytest.mark.recovery
def test_crash_window_branch_b_not_landed(tmp_path):
    """INV-007 Branch B: remote_reachable=False → re-drive the SAME cycle, no re-fix.

    A dangling push_initiated (no matching push_completed) is resolved with the live
    remote query returning unreachable: the push did NOT land. Recovery appends
    push_aborted_or_not_landed{recovered:true} and re-drives the SAME cycle's push
    (resume_state == S4_PUSHING) WITHOUT recomputing the fix — crucially it does NOT
    synthesize a push_completed (the fix is preserved, the push is simply re-driven).
    """
    rl = RunLog(98, tmp_path)
    # Dangling push_initiated — the crash window (no matching push_completed).
    rl.append(
        {
            "event_type": "push_initiated",
            "target_sha": "shaB",
            "idempotency_key": "push:r:cB:preB:feat",
            "run_id": "r",
            "cycle_id": "cB",
            "pre_push_sha": "preB",
            "target_branch": "feat",
            "target_remote": "origin",
        }
    )

    dangling = detect_crash_window(rl)
    assert dangling is not None
    branch, resume_state = resolve_crash_window(rl, dangling, remote_reachable=False)

    # Branch B: not landed → re-drive the SAME cycle's push.
    assert branch == BRANCH_B_NOT_LANDED
    assert resume_state == MonitorState.S4_PUSHING

    events = rl.read_events()
    # The push_aborted_or_not_landed recovery event was appended with recovered==True.
    aborted = [
        e
        for e in events
        if e["event_type"] == "push_aborted_or_not_landed" and e.get("recovered")
    ]
    assert len(aborted) == 1 and aborted[0]["recovered"] is True
    # The fix is NOT recomputed — NO push_completed was synthesized (re-drive only).
    completed = [e for e in events if e["event_type"] == "push_completed"]
    assert completed == []


@pytest.mark.recovery
def test_crash_window_branch_c_ambiguous(tmp_path):
    """INV-007 Branch C: remote_reachable=None → HALT_HUMAN with observed remote SHA.

    The remote branch tip moved to an unrelated SHA: ambiguous. Recovery appends a
    terminal_halted event carrying reason "ambiguous_remote_tip" and the observed
    remote SHA, and resumes into HALT_HUMAN (no auto-mutation, human adjudication).
    """
    rl = RunLog(97, tmp_path)
    # Dangling push_initiated — the crash window.
    rl.append(
        {
            "event_type": "push_initiated",
            "target_sha": "shaC",
            "idempotency_key": "push:r:cC:preC:feat",
            "run_id": "r",
            "cycle_id": "cC",
            "pre_push_sha": "preC",
            "target_branch": "feat",
            "target_remote": "origin",
        }
    )

    dangling = detect_crash_window(rl)
    assert dangling is not None
    branch, resume_state = resolve_crash_window(
        rl, dangling, remote_reachable=None, observed_remote_sha="zzz999"
    )

    # Branch C: ambiguous tip → HALT for a human.
    assert branch == BRANCH_C_AMBIGUOUS
    assert resume_state == MonitorState.HALT_HUMAN

    events = rl.read_events()
    halted = [e for e in events if e["event_type"] == "terminal_halted"]
    assert len(halted) == 1
    assert halted[0]["reason"] == "ambiguous_remote_tip"
    assert halted[0]["observed_remote_sha"] == "zzz999"
