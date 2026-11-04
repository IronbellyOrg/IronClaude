"""Crash-recovery tests (spec §12.2 FM-1..FM-12 + §12.1 INV-007 crash window).

Each FM in the catalog has a recovery semantic; plus T-CRASH-WINDOW-NO-DOUBLE-PUSH
(Branch-A landed): `push_count == 2`, `resume_state == S5_AWAITING_REREVIEW`,
`push_completed.recovered == True` — and crucially NO second actual push.
"""

from __future__ import annotations

import json

import pytest

from superclaude.pr_submit.classifier import classify
from superclaude.pr_submit.conflicts import (
    ResumePlan,
    conflict_action,
    conflict_resume_plan,
    prior_conflict_cycles,
)
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
    resolve_crash_window_plan,
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
    """FM-11: a misrouted PR URL (wrong owner/repo) → terminal_failed; do not monitor.

    The target repo is RESOLVED from origin and passed in (not a hardcoded fork) — the
    misroute check is the same for any ``owner/repo``.
    """
    from superclaude.pr_submit.fsm import pr_target_ok  # owner verification helper

    # This project's own resolved origin.
    repo = "IronbellyOrg/IronClaude"
    assert (
        pr_target_ok("https://github.com/IronbellyOrg/IronClaude/pull/5", repo) is True
    )
    assert (
        pr_target_ok(
            "https://github.com/SuperClaude-Org/SuperClaude_Framework/pull/5", repo
        )
        is False
    )
    # And generically, for an unrelated repo (de-hardcoding proof).
    assert (
        pr_target_ok("https://github.com/acme/widgets/pull/5", "acme/widgets") is True
    )
    assert (
        pr_target_ok("https://github.com/contoso/gadgets/pull/5", "acme/widgets")
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


# ---------------------------------------------------------------------------
# Issue #305: kind-aware crash recovery (design sections 4.8 and 6.4)
# ---------------------------------------------------------------------------

SHA_PRE = "a" * 40
SHA_TGT = "b" * 40
SHA_BASE = "c" * 40
SHA_OTHER = "d" * 40

# One dangling-push cycle id per kind. Fix and CI cycles never use a reserved
# conflict prefix; the sync and merge cycles are conflict cycles.
_CYCLE = {
    "fix": "c1",
    "absent": "c1",
    "ci": "c-ci-1",
    "sync": "sync-1",
    "merge": "conflict-1",
}
# Branch label -> (remote_reachable, observed_remote_sha).
_BRANCH_INPUT = {"A": (True, None), "B": (False, None), "C": (None, SHA_OTHER)}
_BRANCH_NAME = {
    "A": BRANCH_A_LANDED,
    "B": BRANCH_B_NOT_LANDED,
    "C": BRANCH_C_AMBIGUOUS,
}
_PUSH_OR_REVIEW_STATES = {
    MonitorState.S4_PUSHING,
    MonitorState.S5A_RETRIGGER_REVIEW,
    MonitorState.S5_AWAITING_REREVIEW,
}


def _sync_started(
    cycle_id: str, *, kind: str, hook: str, review_terminal, resumed: bool = False
) -> dict:
    """A ``sync_started`` payload as design section 4.7 lists it."""
    return {
        "event_type": "sync_started",
        "run_id": "r",
        "cycle_id": cycle_id,
        "tier": 1 if kind == "sync" else 2,
        "kind": kind,
        "hook": hook,
        "base_ref": "origin/master",
        "base_sha": SHA_BASE,
        "pre_push_sha": SHA_PRE,
        "merge_tree_oid": "e" * 40,
        "conflict_max_tier": 1 if kind == "sync" else 2,
        "review_terminal": review_terminal,
        "paths": ["uv.lock"],
        "resumed": resumed,
    }


def _initiated(
    cycle_id: str,
    *,
    kind: str | None = None,
    base_sha: str | None = None,
    review_terminal: str | None = None,
    expect_checks: bool | None = None,
) -> dict:
    """A ``push_initiated`` record in the key order ``build_push_triad`` writes."""
    record: dict = {"event_type": "push_initiated", "remote_ref": "origin/feat"}
    if review_terminal is not None:
        record["review_terminal"] = review_terminal
    if expect_checks is not None:
        record["expect_checks"] = expect_checks
    record.update(
        {
            "run_id": "r",
            "cycle_id": cycle_id,
            "idempotency_key": f"push:r:{cycle_id}:{SHA_PRE}:feat",
            "pre_push_sha": SHA_PRE,
            "target_sha": SHA_TGT,
            "target_branch": "feat",
            "target_remote": "origin",
        }
    )
    if kind is not None:
        record["kind"] = kind
    if base_sha is not None:
        record["base_sha"] = base_sha
    return record


def _dangling_for(kind: str) -> tuple[dict | None, dict]:
    """The ``sync_started`` (or ``None``) and the dangling ``push_initiated`` of a kind."""
    cycle_id = _CYCLE[kind]
    if kind == "sync":
        started = _sync_started(
            cycle_id, kind="sync", hook="wave8a", review_terminal="clean"
        )
        return started, _initiated(
            cycle_id,
            kind="sync",
            base_sha=SHA_BASE,
            review_terminal="clean",
            expect_checks=True,
        )
    if kind == "merge":
        started = _sync_started(
            cycle_id, kind="merge", hook="c_initial", review_terminal=None
        )
        return started, _initiated(cycle_id, kind="merge", base_sha=SHA_BASE)
    if kind == "ci":
        return None, _initiated(
            cycle_id, kind="ci", review_terminal="clean", expect_checks=True
        )
    if kind == "fix":
        return None, _initiated(cycle_id, kind="fix")
    return None, _initiated(cycle_id)  # absent: the legacy record shape


def _seed(rl: RunLog, kind: str) -> dict:
    """Append the kind's cycle start (if any) and its dangling push; return the record."""
    started, record = _dangling_for(kind)
    if started is not None:
        rl.append(started)
    rl.append(record)
    dangling = detect_crash_window(rl)
    assert dangling is not None and dangling["cycle_id"] == _CYCLE[kind]
    return dangling


def _plan(rl: RunLog, dangling: dict, branch: str) -> ResumePlan:
    reachable, observed = _BRANCH_INPUT[branch]
    return resolve_crash_window_plan(
        rl, dangling, remote_reachable=reachable, observed_remote_sha=observed
    )


def _of_type(rl: RunLog, event_type: str) -> list[dict]:
    return [e for e in rl.read_events() if e["event_type"] == event_type]


def _skill_close(
    rl: RunLog,
    cycle_id: str,
    *,
    outcome: str,
    reason: str | None = None,
    merge_sha: str | None = None,
) -> bool:
    """The SKILL's guarded close: append only while the cycle is still the open one."""
    open_cycle = rl.rebuild_state()["open_conflict_cycle"]
    if open_cycle is None or open_cycle.get("cycle_id") != cycle_id:
        return False
    rl.append(
        {
            "event_type": "sync_concluded",
            "cycle_id": cycle_id,
            "outcome": outcome,
            "merge_sha": merge_sha,
            "record_path": None,
            "dropped": [],
            "reason": reason,
            "recovered": True,
        }
    )
    return True


def _resume(rl: RunLog, **facts) -> ResumePlan:
    """``conflict_resume_plan`` on the rebuilt state with no foreign operation."""
    args = {
        "foreign_op": None,
        "merge_head_sha": None,
        "local_head_sha": SHA_TGT,
        "local_head_parents": [SHA_PRE, SHA_BASE],
        "dangling": detect_crash_window(rl),
    }
    args.update(facts)
    return conflict_resume_plan(rl.rebuild_state(), **args)


# (kind, branch) -> (directive, state, check_merge_parent, rerun_guard, wave8 fields)
_EXPECTED_PLAN = {
    ("fix", "A"): ("fsm", MonitorState.S5A_RETRIGGER_REVIEW, False, False, False),
    ("fix", "B"): ("fsm", MonitorState.S4_PUSHING, False, False, False),
    ("absent", "A"): ("fsm", MonitorState.S5A_RETRIGGER_REVIEW, False, False, False),
    ("absent", "B"): ("fsm", MonitorState.S4_PUSHING, False, False, False),
    ("merge", "A"): ("fsm", MonitorState.S5A_RETRIGGER_REVIEW, False, False, False),
    ("merge", "B"): ("fsm", MonitorState.S4_PUSHING, True, False, False),
    ("sync", "A"): ("wave8_ci_wait", None, False, False, True),
    ("sync", "B"): ("redrive_then_wave8", None, True, True, True),
    ("ci", "A"): ("wave8_ci_wait", None, False, False, True),
    ("ci", "B"): ("redrive_then_wave8", None, False, True, True),
}


@pytest.mark.recovery
@pytest.mark.parametrize("branch", ["A", "B", "C"])
@pytest.mark.parametrize("kind", ["fix", "merge", "sync", "ci", "absent"])
def test_resolve_crash_window_plan_by_kind(tmp_path, kind, branch):
    """Section 4.8 table 2: the exact ``ResumePlan`` for every kind and branch."""
    rl = RunLog(305, tmp_path)
    dangling = _seed(rl, kind)

    plan = _plan(rl, dangling, branch)

    plan_kind = "fix" if kind == "absent" else kind
    common = {
        "cycle_id": _CYCLE[kind],
        "kind": plan_kind,
        "target_sha": SHA_TGT,
        "base_sha": SHA_BASE if plan_kind in ("sync", "merge") else None,
    }
    if branch == "C":
        expected = ResumePlan(
            "halt",
            state=MonitorState.HALT_HUMAN,
            reason="ambiguous_remote_tip",
            **common,
        )
    else:
        directive, state, merge_parent, rerun, wave8 = _EXPECTED_PLAN[(kind, branch)]
        extra = (
            {"wait_sha": SHA_TGT, "review_terminal": "clean", "expect_checks": True}
            if wave8
            else {}
        )
        expected = ResumePlan(
            directive,
            state=state,
            check_merge_parent=merge_parent,
            rerun_guard=rerun,
            **common,
            **extra,
        )
    assert plan == expected
    # INV-001: sync and ci never resume into a push or review state.
    if plan_kind in ("sync", "ci"):
        assert plan.state not in _PUSH_OR_REVIEW_STATES
    # Only an open conflict cycle settled by Branch A or C gets a sync_concluded.
    closes = plan_kind in ("sync", "merge") and branch in ("A", "C")
    assert len(_of_type(rl, "sync_concluded")) == (1 if closes else 0)


@pytest.mark.recovery
@pytest.mark.parametrize(
    ("kind", "count_key"), [("sync", "sync_push_count"), ("merge", "push_count")]
)
def test_recovered_push_completed_copies_kind_and_base_sha(tmp_path, kind, count_key):
    """Branch A's recovered ``push_completed`` carries ``kind`` and ``base_sha``.

    So the fold counts a recovered sync push in ``sync_push_count`` and a merge
    push in ``push_count``.
    """
    rl = RunLog(305, tmp_path)
    dangling = _seed(rl, kind)
    _plan(rl, dangling, "A")

    [completed] = _of_type(rl, "push_completed")
    assert completed["recovered"] is True
    assert completed["kind"] == kind
    assert completed["base_sha"] == SHA_BASE
    state = rl.rebuild_state()
    assert state[count_key] == 1
    other = "push_count" if count_key == "sync_push_count" else "sync_push_count"
    assert state[other] == 0


# The exact pre-#305 recovery record for a kind-less dangling push, in key order.
_LEGACY_IDENTITY = {
    "run_id": "r",
    "cycle_id": "c1",
    "idempotency_key": f"push:r:c1:{SHA_PRE}:feat",
    "pre_push_sha": SHA_PRE,
    "target_sha": SHA_TGT,
    "target_branch": "feat",
    "target_remote": "origin",
}
_LEGACY_HEAD = {
    "A": {"event_type": "push_completed", "recovered": True},
    "B": {"event_type": "push_aborted_or_not_landed", "recovered": True},
    "C": {
        "event_type": "terminal_halted",
        "recovered": True,
        "reason": "ambiguous_remote_tip",
        "observed_remote_sha": SHA_OTHER,
    },
}
_LEGACY_STATE = {
    "A": MonitorState.S5A_RETRIGGER_REVIEW,
    "B": MonitorState.S4_PUSHING,
    "C": MonitorState.HALT_HUMAN,
}


@pytest.mark.recovery
@pytest.mark.parametrize("branch", ["A", "B", "C"])
def test_legacy_record_recovery_events_unchanged(tmp_path, branch):
    """NFR-12: a kind-less record yields byte-equal recovery events and today's state."""
    rl = RunLog(305, tmp_path)
    dangling = _seed(rl, "absent")

    plan = _plan(rl, dangling, branch)

    assert plan.state == _LEGACY_STATE[branch]
    lines = rl.jsonl_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2  # the dangling push and its one recovery event
    expected = {
        "schema_version": "1.0",
        "event_id": 2,
        **_LEGACY_HEAD[branch],
        **_LEGACY_IDENTITY,
        "timestamp": None,
    }
    assert lines[1] == json.dumps(expected)


@pytest.mark.recovery
@pytest.mark.parametrize("branch", ["A", "B", "C"])
@pytest.mark.parametrize("kind", ["fix", "absent"])
def test_fix_and_absent_wrapper_matches_resolve_crash_window(tmp_path, kind, branch):
    """For kinds ``fix`` and absent the wrapper adds nothing to ``resolve_crash_window``.

    Two identical logs: one settled by the wrapper, one by ``resolve_crash_window``.
    The JSONL bytes are equal and the plan's state is the returned state.
    """
    rl_plan = RunLog(305, tmp_path / "plan")
    rl_today = RunLog(305, tmp_path / "today")
    dangling_plan = _seed(rl_plan, kind)
    dangling_today = _seed(rl_today, kind)
    reachable, observed = _BRANCH_INPUT[branch]

    plan = resolve_crash_window_plan(
        rl_plan,
        dangling_plan,
        remote_reachable=reachable,
        observed_remote_sha=observed,
    )
    branch_today, state_today = resolve_crash_window(
        rl_today,
        dangling_today,
        remote_reachable=reachable,
        observed_remote_sha=observed,
    )

    assert branch_today == _BRANCH_NAME[branch]
    assert plan.state == state_today
    assert rl_plan.jsonl_path.read_bytes() == rl_today.jsonl_path.read_bytes()
    assert rl_plan.rebuild_state() == rl_today.rebuild_state()


@pytest.mark.recovery
def test_rejected_push_record_is_not_a_crash_window(tmp_path):
    """A rejected push is finalized: no crash window, and resume halts ``push_rejected``."""
    rl = RunLog(305, tmp_path)
    started, record = _dangling_for("sync")
    rl.append(started)
    rl.append(record)
    rl.append(
        {
            "event_type": "push_aborted_or_not_landed",
            "idempotency_key": record["idempotency_key"],
            "cycle_id": "sync-1",
            "rejected": True,
            "stderr_tail": "rejected: non-fast-forward",
        }
    )

    assert detect_crash_window(rl) is None
    plan = _resume(rl, dangling=None)
    assert plan == ResumePlan("halt", reason="push_rejected", cycle_id="sync-1")


@pytest.mark.recovery
@pytest.mark.parametrize("case", ["A", "C", "halt"])
@pytest.mark.parametrize("kind", ["sync", "merge"])
def test_conflict_crash_recovery_closes_the_cycle(tmp_path, kind, case):
    """B2: Branch A, Branch C and a halt directive close the open cycle exactly once.

    The halt directive comes from an unusable record: a sync record without
    ``review_terminal`` (settled through Branch B), or a merge cycle whose record
    carries an unknown kind (settled through Branch A).
    """
    rl = RunLog(305, tmp_path)
    started, record = _dangling_for(kind)
    if case == "halt":
        if kind == "sync":
            del record["review_terminal"]
        else:
            record["kind"] = "merg"
    rl.append(started)
    rl.append(record)
    dangling = detect_crash_window(rl)
    assert dangling is not None
    branch = {"A": "A", "C": "C", "halt": "B" if kind == "sync" else "A"}[case]

    plan = _plan(rl, dangling, branch)

    outcome, reason, merge_sha = {
        "A": ("pushed", None, SHA_TGT),
        "C": ("halted", "ambiguous_remote_tip", None),
        "halt": ("halted", "resume_unrepresentable", None),
    }[case]
    if case == "halt":
        assert plan.directive == "halt" and plan.reason == "resume_unrepresentable"
    concluded = _of_type(rl, "sync_concluded")
    assert len(concluded) == 1
    body = {k: v for k, v in concluded[0].items() if k not in ("event_id",)}
    assert body == {
        "schema_version": "1.0",
        "event_type": "sync_concluded",
        "cycle_id": _CYCLE[kind],
        "outcome": outcome,
        "merge_sha": merge_sha,
        "record_path": None,
        "dropped": [],
        "reason": reason,
        "recovered": True,
        "timestamp": None,
    }
    assert rl.rebuild_state()["open_conflict_cycle"] is None
    if case == "C":
        # Today's Branch C record does not finalize the key, so a later resume
        # can reach the wrapper again; the closed cycle is not closed twice.
        assert detect_crash_window(rl) is not None
    else:
        # The settled key is finalized, so a later resume never reaches the wrapper.
        assert detect_crash_window(rl) is None
    # A second wrapper call appends no second sync_concluded (the cycle is closed).
    _plan(rl, dangling, branch)
    assert len(_of_type(rl, "sync_concluded")) == 1


@pytest.mark.recovery
@pytest.mark.parametrize("branch", ["A", "B", "C"])
@pytest.mark.parametrize("kind", ["fix", "ci", "absent"])
def test_non_conflict_kinds_append_no_sync_concluded(tmp_path, kind, branch):
    """Kinds ``fix``, ``ci`` and absent have no conflict cycle and close nothing."""
    rl = RunLog(305, tmp_path)
    dangling = _seed(rl, kind)
    _plan(rl, dangling, branch)
    assert _of_type(rl, "sync_concluded") == []
    assert rl.rebuild_state()["conflict_cycles"] == []


@pytest.mark.recovery
def test_conflict_crash_then_later_fix_crash_resumes_into_fix_window(tmp_path):
    """B2: after a recovered sync crash, a later fix crash reaches the fix window."""
    rl = RunLog(305, tmp_path)
    dangling = _seed(rl, "sync")
    _plan(rl, dangling, "A")
    assert rl.rebuild_state()["open_conflict_cycle"] is None

    fix_record = _initiated("c2")
    rl.append(fix_record)

    assert _resume(rl) == ResumePlan("none")
    fix_dangling = detect_crash_window(rl)
    assert fix_dangling is not None
    assert fix_dangling["idempotency_key"] == fix_record["idempotency_key"]
    plan = resolve_crash_window_plan(rl, fix_dangling, remote_reachable=True)
    assert plan.directive == "fsm"
    assert plan.state == MonitorState.S5A_RETRIGGER_REVIEW
    assert len(_of_type(rl, "sync_concluded")) == 1  # only the sync cycle's
    state = rl.rebuild_state()
    assert state["sync_push_count"] == 1 and state["push_count"] == 1


@pytest.mark.recovery
def test_restart_row_uses_recorded_review_terminal(tmp_path):
    """B3, m3: a row 7 restart re-enters with the recorded ``review_terminal``.

    The router then sees ``prior_conflict_cycles == 0`` (the reused id is
    excluded) and resolves the sync at L3; counting the reused id would hit
    ``sync_cap``.
    """
    rl = RunLog(305, tmp_path)
    rl.append(
        _sync_started(
            "sync-1", kind="sync", hook="wave8a", review_terminal="halt_max_rounds"
        )
    )
    state = rl.rebuild_state()
    assert state["conflict_cycles"] == ["sync-1"]

    plan = _resume(rl, local_head_sha=SHA_PRE, local_head_parents=[SHA_BASE])

    assert plan.directive == "restart"
    assert plan.cycle_id == "sync-1"
    assert plan.hook == "wave8a"
    assert plan.review_terminal == "halt_max_rounds"
    assert _skill_close(rl, "sync-1", outcome="aborted") is True
    rl.append(
        _sync_started(
            "sync-1",
            kind="sync",
            hook="wave8a",
            review_terminal=plan.review_terminal,
            resumed=True,
        )
    )
    state = rl.rebuild_state()
    assert state["conflict_cycles"] == ["sync-1"]  # the restart counts once
    assert state["open_conflict_cycle"]["review_terminal"] == "halt_max_rounds"

    prior = prior_conflict_cycles(state["conflict_cycles"], plan.cycle_id)
    assert prior == 0
    route = {
        "hook": plan.hook,
        "plan_tier": 1,
        "ordinal": 3,
        "entering": plan.review_terminal,
        "conflict_max_tier": 1,
        "round_counter": 0,
        "max_rounds": 3,
        "github_conflicting": True,
    }
    action = conflict_action(prior_conflict_cycles=prior, **route)
    assert (action.action, action.reason) == ("resolve_push", "tier1_sync")
    not_excluded = conflict_action(
        prior_conflict_cycles=len(state["conflict_cycles"]), **route
    )
    assert not_excluded.reason == "sync_cap"


def _branch_b_then_redrive(rl: RunLog) -> dict:
    """A sync crash settled by Branch B, then the re-drive's ``push_initiated``."""
    dangling = _seed(rl, "sync")
    plan = _plan(rl, dangling, "B")
    assert plan.directive == "redrive_then_wave8"
    assert _of_type(rl, "sync_concluded") == []  # Branch B: the SKILL closes later
    _, redrive = _dangling_for("sync")  # same cycle, same key, same target
    rl.append(redrive)
    return redrive


def _assert_4b_prime_halts_and_closes_once(rl: RunLog) -> None:
    assert detect_crash_window(rl) is None  # the reused key is already finalized
    plan = _resume(rl, dangling=None)
    assert plan == ResumePlan(
        "halt",
        reason="resume_unrepresentable",
        cycle_id="sync-1",
        target_sha=SHA_TGT,
    )
    assert _skill_close(rl, "sync-1", outcome="halted", reason=plan.reason) is True
    [concluded] = _of_type(rl, "sync_concluded")
    assert concluded["outcome"] == "halted" and concluded["recovered"] is True
    assert rl.rebuild_state()["open_conflict_cycle"] is None
    # A third resume: no open cycle, row 2, and nothing more is appended.
    assert _resume(rl) == ResumePlan("none")
    assert _skill_close(rl, "sync-1", outcome="halted", reason=plan.reason) is False
    assert len(_of_type(rl, "sync_concluded")) == 1


@pytest.mark.recovery
def test_branch_b_crash_during_redrive_halts_and_closes_once(tmp_path):
    """N1: a crash during the Branch B re-drive reaches row 4b' and closes once."""
    rl = RunLog(305, tmp_path)
    _branch_b_then_redrive(rl)
    # Crash before the re-drive's push_completed.
    _assert_4b_prime_halts_and_closes_once(rl)


@pytest.mark.recovery
def test_branch_b_redrive_push_failed_then_resume_halts_and_closes_once(tmp_path):
    """N1: a re-drive ending ``push_failed`` (no record) halts at row 4b' and closes once.

    No directive along the way plans another push.
    """
    rl = RunLog(305, tmp_path)
    _branch_b_then_redrive(rl)
    rl.append({"event_type": "terminal_halted", "reason": "push_failed"})
    plans = [_resume(rl, dangling=None)]
    _assert_4b_prime_halts_and_closes_once(rl)
    plans.append(_resume(rl))
    for plan in plans:
        assert plan.directive in ("halt", "none")
        assert plan.state != MonitorState.S4_PUSHING


@pytest.mark.recovery
def test_resume_row_1_closes_an_open_cycle(tmp_path):
    """m2: ``push_rejected`` with a cycle still open closes it once as ``halted``."""
    rl = RunLog(305, tmp_path)
    started, record = _dangling_for("sync")
    rl.append(started)
    rl.append(record)
    rl.append(
        {
            "event_type": "push_aborted_or_not_landed",
            "idempotency_key": record["idempotency_key"],
            "cycle_id": "sync-1",
            "rejected": True,
            "stderr_tail": "rejected",
        }
    )

    plan = _resume(rl)
    assert plan.directive == "halt" and plan.reason == "push_rejected"
    assert plan.cycle_id == "sync-1"
    assert _skill_close(rl, plan.cycle_id, outcome="halted", reason=plan.reason)
    [concluded] = _of_type(rl, "sync_concluded")
    assert (concluded["outcome"], concluded["reason"]) == ("halted", "push_rejected")
    assert rl.rebuild_state()["open_conflict_cycle"] is None
    again = _resume(rl)
    assert again == ResumePlan("halt", reason="push_rejected")  # no cycle to close
    assert _skill_close(rl, "sync-1", outcome="halted", reason="x") is False
    assert len(_of_type(rl, "sync_concluded")) == 1


@pytest.mark.recovery
def test_resume_row_4_expect_checks_defaults_true(tmp_path):
    """m6: row 4 with no ``expect_checks`` on the push record reads it as ``True``."""
    rl = RunLog(305, tmp_path)
    rl.append(
        _sync_started("sync-1", kind="sync", hook="wave8a", review_terminal="clean")
    )
    record = _initiated(
        "sync-1", kind="sync", base_sha=SHA_BASE, review_terminal="clean"
    )
    assert "expect_checks" not in record
    rl.append(record)
    rl.append(
        {
            "event_type": "push_completed",
            **{k: record[k] for k in _LEGACY_IDENTITY},
            "cycle_id": "sync-1",
            "idempotency_key": record["idempotency_key"],
            "kind": "sync",
            "base_sha": SHA_BASE,
        }
    )

    plan = _resume(rl)
    assert plan.directive == "complete_after_push"
    assert plan.expect_checks is True
    assert plan.wait_sha == SHA_TGT
    assert plan.state is None  # sync never resumes into S5a or S5


@pytest.mark.recovery
def test_branch_b_redrive_landed_closes_cycle_once(tmp_path):
    """n4: a landed Branch B re-drive is closed once by the SKILL's guarded close."""
    rl = RunLog(305, tmp_path)
    redrive = _branch_b_then_redrive(rl)
    rl.append(
        {
            "event_type": "push_completed",
            **{k: redrive[k] for k in _LEGACY_IDENTITY},
            "cycle_id": "sync-1",
            "idempotency_key": redrive["idempotency_key"],
            "kind": "sync",
            "base_sha": SHA_BASE,
        }
    )
    assert _skill_close(rl, "sync-1", outcome="pushed", merge_sha=SHA_TGT) is True
    [concluded] = _of_type(rl, "sync_concluded")
    assert concluded["outcome"] == "pushed" and concluded["recovered"] is True
    assert concluded["merge_sha"] == SHA_TGT
    assert rl.rebuild_state()["open_conflict_cycle"] is None

    # A later fix-cycle crash window resumes into the fix window through row 2.
    fix_record = _initiated("c2")
    rl.append(fix_record)
    assert _resume(rl) == ResumePlan("none")
    fix_dangling = detect_crash_window(rl)
    assert fix_dangling is not None
    assert fix_dangling["idempotency_key"] == fix_record["idempotency_key"]
    # A second close attempt for the closed cycle appends nothing.
    assert _skill_close(rl, "sync-1", outcome="pushed", merge_sha=SHA_TGT) is False
    assert len(_of_type(rl, "sync_concluded")) == 1


@pytest.mark.recovery
def test_branch_c_event_order(tmp_path):
    """m5: Branch C writes ``terminal_halted`` and then ``sync_concluded``, each once."""
    rl = RunLog(305, tmp_path)
    dangling = _seed(rl, "sync")
    before = len(rl.read_events())

    _plan(rl, dangling, "C")

    added = rl.read_events()[before:]
    assert [e["event_type"] for e in added] == ["terminal_halted", "sync_concluded"]
    assert added[0]["reason"] == "ambiguous_remote_tip"
    assert added[1]["outcome"] == "halted"
    assert added[1]["reason"] == "ambiguous_remote_tip"
