"""Run-log substrate tests (spec §11) + the NFR-7/NFR-8 additions.

T-N20 log existence + per-event timestamp/round/state populated; T-N21 JSONL
well-formedness + event ordering; T-N22 JSONL validity (every line parses,
`event_id` monotonic). T-N51 (NFR-7): no token/credential reaches the JSONL.
T-N52 (NFR-8): replaying a fixture twice yields identical deterministic decisions.
"""

from __future__ import annotations

import json

import pytest

from superclaude.pr_submit.conflicts import conflict_resume_plan
from superclaude.pr_submit.fsm import (
    RunConfig,
    build_push_triad,
    evaluate_push_decision,
    run_skill,
)
from superclaude.pr_submit.models import EventType, Finding
from superclaude.pr_submit.run_log import RunLog, fix_key


@pytest.mark.recovery
def test_tn20_log_exists_and_events_populated(tmp_path):
    """T-N20: the run-log exists and each event carries timestamp/round/state fields."""
    rl = RunLog(42, tmp_path)
    rl.append(
        {
            "event_type": "run_started",
            "timestamp": "2026-06-11T00:00:00Z",
            "round_counter": 0,
            "state_after": "S0_IDLE",
        }
    )
    rl.append(
        {
            "event_type": "monitor_armed",
            "timestamp": "2026-06-11T00:00:30Z",
            "round_counter": 0,
            "state_after": "S2_CLASSIFY",
        }
    )
    assert rl.jsonl_path.exists()
    events = rl.read_events()
    assert len(events) == 2
    for ev in events:
        assert ev.get("timestamp") is not None
        assert "round_counter" in ev
        assert ev.get("state_after") is not None


def test_tn21_jsonl_well_formed_and_ordered(tmp_path):
    """T-N21: every line is well-formed JSON and events are in append order."""
    rl = RunLog(7, tmp_path)
    for i, et in enumerate(
        ["run_started", "poll_attempt", "poll_result", "review_detected"]
    ):
        rl.append({"event_type": et, "seq": i})
    lines = rl.jsonl_path.read_text(encoding="utf-8").splitlines()
    parsed = [json.loads(line) for line in lines if line.strip()]
    assert [p["seq"] for p in parsed] == [0, 1, 2, 3]  # append order preserved


def test_tn22_jsonl_validity_event_id_monotonic(tmp_path):
    """T-N22: every line parses and `event_id` is unique + monotonically increasing."""
    rl = RunLog(9, tmp_path)
    for et in [
        "run_started",
        "poll_attempt",
        "round_incremented",
        "push_completed",
        "terminal_clean",
    ]:
        rl.append({"event_type": et})
    ids = [
        json.loads(line)["event_id"]
        for line in rl.jsonl_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert ids == sorted(ids)
    assert len(ids) == len(set(ids))  # unique
    assert ids == list(range(1, len(ids) + 1))  # monotonic from 1


@pytest.mark.recovery
def test_tn51_no_credentials_reach_jsonl(tmp_path):
    """T-N51 (NFR-7): token/credential patterns are redacted before reaching the JSONL."""
    rl = RunLog(11, tmp_path)
    rl.append(
        {
            "event_type": "fix_applied",
            "body": "set token=ghp_ABCDEFGHIJKLMNOP0123456789 and Authorization: Bearer abcd1234efgh",
            "nested": {
                "cmd": "export GITHUB_TOKEN=github_pat_11ABCDEFGHIJKLMNOPQRSTU",
                "ok": True,
            },
        }
    )
    raw = rl.jsonl_path.read_text(encoding="utf-8")
    # No raw token survives in the JSONL.
    for leak in ("ghp_ABCDEFGHIJKLMNOP", "github_pat_11ABCDEFGH", "Bearer abcd1234"):
        assert leak not in raw
    assert "[REDACTED]" in raw


def test_tn52_replay_determinism(tmp_path):
    """T-N52 (NFR-8): replaying the same input twice yields identical deterministic decisions."""

    def make_config():
        return RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            findings=[
                Finding(
                    path="src/a.py",
                    line=1,
                    body="bug",
                    in_diff=True,
                    verification_status="verified",
                    comment_id=1,
                )
            ],
            rereview_findings=[
                [
                    Finding(
                        path="src/a.py",
                        line=2,
                        body="bug2",
                        in_diff=True,
                        verification_status="verified",
                        comment_id=2,
                    )
                ]
            ],
        )

    r1 = run_skill(make_config())
    r2 = run_skill(make_config())
    # Identical classifier/counter/route/terminal-outcome decisions.
    assert (
        r1.state,
        r1.round_counter,
        r1.push_count,
        r1.reply_count,
        r1.applied_edits,
    ) == (r2.state, r2.round_counter, r2.push_count, r2.reply_count, r2.applied_edits)


def test_rebuild_from_jsonl_is_authoritative(tmp_path):
    """§11.1: rebuilding state from the JSONL reconstructs counters + idempotency sets."""
    rl = RunLog(13, tmp_path)
    rl.append({"event_type": "fix_applied", "fix_key": fix_key("a.py", 1, "bug")})
    rl.append({"event_type": "round_incremented"})
    rl.append({"event_type": "push_completed", "target_sha": "abc123"})
    rl.append({"event_type": "reply_posted", "comment_id": 55})
    state = rl.rebuild_state()
    assert state["round_counter"] == 1
    assert state["push_count"] == 1
    assert state["reply_count"] == 1
    assert "abc123" in state["pushed_commit_shas"]
    assert 55 in state["replied_comment_ids"]
    assert state["silence_rerequested_at"] is None


# --- V1.1 closed-enum count + new-event folds (addendum §6.1/§6.3) ------------


def test_eventtype_is_45_members_with_silence_reviewer_conflict_and_guard_events():
    """The closed EventType enum has EXACTLY 45 members, including INV-S1, the two
    reviewer-presence events, the two conflict-cycle events and the two merge-guard
    events."""
    assert len(EventType) == 45
    assert len(list(EventType)) == 45
    assert EventType.DRAFT_GUARD_REQUESTED.value == "draft_guard_requested"
    assert EventType.DRAFT_GUARD_SETTLED.value == "draft_guard_settled"
    assert EventType.SYNC_STARTED.value == "sync_started"
    assert EventType.SYNC_CONCLUDED.value == "sync_concluded"
    assert EventType.REVIEWER_ABSENT.value == "reviewer_absent"
    assert EventType.REVIEWER_INCOMPLETE.value == "reviewer_incomplete"
    assert EventType.REREVIEW_REQUESTED.value == "rereview_requested"
    assert EventType.DECLINE_DETECTED.value == "decline_detected"
    assert EventType.AUGGIE_FALLBACK_INVOKED.value == "auggie_fallback_invoked"
    assert EventType.MAX_ROUNDS_CLAMPED.value == "max_rounds_clamped"
    assert EventType.SILENCE_REREQUESTED.value == "silence_rerequested"
    assert (
        EventType.TERMINAL_AUGMENT_NO_RESPONSE.value == "terminal_augment_no_response"
    )


def test_new_v11_events_pass_closed_enum_append_validation(tmp_path):
    """Each new event_type is a valid closed-enum value — append() does NOT raise."""
    rl = RunLog(31, tmp_path)
    for member in (
        EventType.REREVIEW_REQUESTED,
        EventType.DECLINE_DETECTED,
        EventType.AUGGIE_FALLBACK_INVOKED,
        EventType.MAX_ROUNDS_CLAMPED,
        EventType.SILENCE_REREQUESTED,
        EventType.TERMINAL_AUGMENT_NO_RESPONSE,
    ):
        rec = rl.append({"event_type": member.value})
        assert rec["event_type"] == member.value
    # And an UNKNOWN event_type still raises (the closed set is enforced).
    with pytest.raises(ValueError):
        rl.append({"event_type": "not_a_real_event"})


def test_guard_events_pass_closed_enum_append_validation(tmp_path):
    """The two merge-guard events are valid closed-enum values, and an unknown type
    is still rejected with the updated member count in the message."""
    rl = RunLog(32, tmp_path)
    for member in (EventType.DRAFT_GUARD_REQUESTED, EventType.DRAFT_GUARD_SETTLED):
        rec = rl.append({"event_type": member.value})
        assert rec["event_type"] == member.value
    with pytest.raises(ValueError, match=r"not one of the 45 closed EventType values"):
        rl.append({"event_type": "not_a_real_event"})


def test_max_rounds_clamped_monotone_min_fold_inv_r3(tmp_path):
    """INV-R3: appending two MAX_ROUNDS_CLAMPED events with DIFFERENT
    effective_max_rounds rebuilds to the SMALLER (monotone non-increasing). The
    higher value is ordered AFTER the lower one to prove it never raises the result."""
    rl = RunLog(41, tmp_path)
    # Seed default: never-clamped → None.
    assert rl.rebuild_state()["effective_max_rounds"] is None
    rl.append(
        {"event_type": EventType.MAX_ROUNDS_CLAMPED.value, "effective_max_rounds": 1}
    )
    # A LATER, HIGHER clamp must NOT raise the rebuilt value back up.
    rl.append(
        {"event_type": EventType.MAX_ROUNDS_CLAMPED.value, "effective_max_rounds": 3}
    )
    assert rl.rebuild_state()["effective_max_rounds"] == 1


def test_rereview_count_and_auggie_set_folds(tmp_path):
    """REREVIEW_REQUESTED events count into rereview_request_count (INV-R1 IDIOM A);
    AUGGIE_FALLBACK_INVOKED folds the pr_number into the auggie_review_invoked set
    (INV-R2 IDIOM B)."""
    rl = RunLog(99, tmp_path)
    rl.append({"event_type": EventType.REREVIEW_REQUESTED.value})
    rl.append({"event_type": EventType.REREVIEW_REQUESTED.value})
    rl.append({"event_type": EventType.AUGGIE_FALLBACK_INVOKED.value, "pr_number": 99})
    state = rl.rebuild_state()
    assert state["rereview_request_count"] == 2
    assert state["auggie_review_invoked"] == [99]


def test_rereview_count_folds_by_distinct_cycle_across_reviewers(tmp_path):
    """One push cycle that re-triggers Augment and Codex counts once (INV-R1)."""
    rl = RunLog(100, tmp_path)
    for reviewer in ("augment", "codex"):
        rl.append(
            {
                "event_type": EventType.REREVIEW_REQUESTED.value,
                "cycle_id": "c1",
                "reviewer": reviewer,
            }
        )
    assert rl.rebuild_state()["rereview_request_count"] == 1


def test_absent_reviewers_fold_is_a_set_and_seeded_empty(tmp_path):
    """reviewer_absent folds into a sorted set; a log without it rebuilds to []."""
    rl = RunLog(101, tmp_path)
    assert rl.rebuild_state()["absent_reviewers"] == []
    rl.append({"event_type": EventType.REVIEWER_ABSENT.value, "reviewer": "codex"})
    rl.append({"event_type": EventType.REVIEWER_ABSENT.value, "reviewer": "codex"})
    assert rl.rebuild_state()["absent_reviewers"] == ["codex"]


# --- issue #305: kind-aware, conflict-cycle-aware fold (design section 6.3) ----

_SHA_A = "a" * 40
_SHA_B = "b" * 40
_SHA_C = "c" * 40
_SHA_D = "d" * 40
_SHA_E = "e" * 40

# A recorded legacy run-log (pre-#305 shape: no `kind`, no conflict-cycle events),
# written verbatim as JSONL lines. Its pre-change fold, captured from the
# unmodified `rebuild_state` before the #305 edit, is `_LEGACY_EXPECTED`.
_LEGACY_JSONL = (
    '{"schema_version": "1.0", "event_id": 1, "event_type": "run_started", "state_after": "S0_IDLE", "timestamp": "2026-06-11T00:00:01Z"}',
    '{"schema_version": "1.0", "event_id": 2, "event_type": "monitor_armed", "state_after": "S2_CLASSIFY", "timestamp": "2026-06-11T00:00:02Z"}',
    '{"schema_version": "1.0", "event_id": 3, "event_type": "findings_normalized", "review_id": 101, "timestamp": "2026-06-11T00:00:03Z"}',
    '{"schema_version": "1.0", "event_id": 4, "event_type": "fix_applied", "fix_key": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "state_after": "S3_FIXING", "timestamp": "2026-06-11T00:00:04Z"}',
    '{"schema_version": "1.0", "event_id": 5, "event_type": "validation_completed", "state_after": "S7_VALIDATING", "timestamp": "2026-06-11T00:00:05Z"}',
    '{"schema_version": "1.0", "event_id": 6, "event_type": "push_decision", "run_id": "r1", "cycle_id": "c1", "idempotency_key": "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk", "pre_push_sha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", "target_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "timestamp": "2026-06-11T00:00:06Z"}',
    '{"schema_version": "1.0", "event_id": 7, "event_type": "push_initiated", "run_id": "r1", "cycle_id": "c1", "idempotency_key": "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk", "pre_push_sha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", "target_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "state_after": "S4_PUSHING", "timestamp": "2026-06-11T00:00:07Z"}',
    '{"schema_version": "1.0", "event_id": 8, "event_type": "push_completed", "run_id": "r1", "cycle_id": "c1", "idempotency_key": "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk", "pre_push_sha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", "target_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "timestamp": "2026-06-11T00:00:08Z"}',
    '{"schema_version": "1.0", "event_id": 9, "event_type": "reply_posted", "comment_id": 55, "state_after": "S6_REPLYING", "timestamp": "2026-06-11T00:00:09Z"}',
    '{"schema_version": "1.0", "event_id": 10, "event_type": "thread_resolved", "thread_id": "PRRT_1", "state_after": "RESOLVING", "timestamp": "2026-06-11T00:00:10Z"}',
    '{"schema_version": "1.0", "event_id": 11, "event_type": "rereview_requested", "cycle_id": "c1", "reviewer": "augment", "state_after": "S5a_RETRIGGER_REVIEW", "timestamp": "2026-06-11T00:00:11Z"}',
    '{"schema_version": "1.0", "event_id": 12, "event_type": "rereview_requested", "cycle_id": "c1", "reviewer": "codex", "timestamp": "2026-06-11T00:00:12Z"}',
    '{"schema_version": "1.0", "event_id": 13, "event_type": "round_incremented", "state_after": "S5_AWAITING_REREVIEW", "timestamp": "2026-06-11T00:00:13Z"}',
    '{"schema_version": "1.0", "event_id": 14, "event_type": "reviewer_absent", "reviewer": "codex", "timestamp": "2026-06-11T00:00:14Z"}',
    '{"schema_version": "1.0", "event_id": 15, "event_type": "silence_rerequested", "pr_number": 77, "elapsed": 600, "timestamp": "2026-06-11T00:00:15Z"}',
    '{"schema_version": "1.0", "event_id": 16, "event_type": "auggie_fallback_invoked", "pr_number": 77, "timestamp": "2026-06-11T00:00:16Z"}',
    '{"schema_version": "1.0", "event_id": 17, "event_type": "max_rounds_clamped", "effective_max_rounds": 2, "timestamp": "2026-06-11T00:00:17Z"}',
    '{"schema_version": "1.0", "event_id": 18, "event_type": "push_aborted_or_not_landed", "cycle_id": "c2", "idempotency_key": "jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj", "timestamp": "2026-06-11T00:00:18Z"}',
    '{"schema_version": "1.0", "event_id": 19, "event_type": "terminal_clean", "state_after": "TERMINAL_CLEAN", "timestamp": "2026-06-11T00:00:19Z"}',
)
_LEGACY_EXPECTED = {
    "pr_number": 77,
    "state": "TERMINAL_CLEAN",
    "round_counter": 1,
    "push_count": 1,
    "reply_count": 1,
    "rereview_request_count": 1,
    "effective_max_rounds": 2,
    "silence_rerequested_at": 600,
    "absent_reviewers": ["codex"],
    "last_event_id": 19,
    "processed_review_ids": [101],
    "processed_finding_ids": ["f" * 64],
    "replied_comment_ids": [55],
    "resolved_thread_ids": ["PRRT_1"],
    "pushed_commit_shas": [_SHA_A],
    "auggie_review_invoked": [77],
    "silence_rerequest_invoked": [77],
}
_NEW_KEY_DEFAULTS = {
    "sync_push_count": 0,
    "conflict_cycles": [],
    "open_conflict_cycle": None,
    "push_rejected": False,
    "draft_guard": None,
}


def _legacy_runlog(tmp_path) -> RunLog:
    """Write the recorded legacy JSONL verbatim, then open it as a resumed RunLog."""
    path = tmp_path / "monitor-run-77.jsonl"
    path.write_text("\n".join(_LEGACY_JSONL) + "\n", encoding="utf-8")
    return RunLog(77, tmp_path)


def _push(
    rl: RunLog,
    cycle_id: str,
    pre_push_sha: str,
    target_sha: str,
    *,
    land: bool = True,
    **extras,
) -> None:
    """Append a push triad built by the real builder (the completed record only if ``land``)."""
    decision = evaluate_push_decision(
        monitor_ordinal=3,
        validation_status="validated",
        needs_human_decision=False,
        round_counter=0,
        max_rounds=3,
        applied_edits=1,
    )
    triad = build_push_triad(
        run_id="r1",
        cycle_id=cycle_id,
        round_counter=0,
        pre_push_sha=pre_push_sha,
        target_sha=target_sha,
        target_branch="feature",
        target_remote="origin",
        decision=decision,
        **extras,
    )
    for record in triad if land else triad[:2]:
        rl.append(record)


def _sync_started(rl: RunLog, cycle_id: str, **overrides) -> None:
    tier = 2 if cycle_id.startswith("conflict-") else 1
    event = {
        "event_type": EventType.SYNC_STARTED.value,
        "run_id": "r1",
        "cycle_id": cycle_id,
        "tier": tier,
        "kind": "merge" if tier == 2 else "sync",
        "hook": "c_initial" if tier == 2 else "wave8a",
        "base_ref": "origin/master",
        "base_sha": _SHA_C,
        "pre_push_sha": _SHA_B,
        "merge_tree_oid": _SHA_E,
        "conflict_max_tier": tier,
        "review_terminal": None if tier == 2 else "clean",
        "paths": ["uv.lock"],
        "resumed": False,
    }
    event.update(overrides)
    rl.append(event)


def _sync_concluded(rl: RunLog, cycle_id: str, outcome: str = "pushed", **extra):
    rl.append(
        {
            "event_type": EventType.SYNC_CONCLUDED.value,
            "cycle_id": cycle_id,
            "outcome": outcome,
            "merge_sha": _SHA_D if outcome == "pushed" else None,
            "record_path": None,
            "dropped": [],
            "reason": None,
            "recovered": False,
            **extra,
        }
    )


def test_fold_old_log_without_kind_rebuilds_identically(tmp_path):
    """NFR-12: a recorded legacy log rebuilds every pre-existing key unchanged and
    the new keys at their defaults; no other key is added."""
    state = _legacy_runlog(tmp_path).rebuild_state()
    assert {k: state[k] for k in _LEGACY_EXPECTED} == _LEGACY_EXPECTED
    assert set(state) == set(_LEGACY_EXPECTED) | set(_NEW_KEY_DEFAULTS)
    assert state == {**_LEGACY_EXPECTED, **_NEW_KEY_DEFAULTS}


def test_legacy_log_rebuilds_with_draft_guard_none(tmp_path):
    """A log written before the merge guard existed has no guard record."""
    state = _legacy_runlog(tmp_path).rebuild_state()
    assert state["draft_guard"] is None
    assert {k: state[k] for k in _LEGACY_EXPECTED} == _LEGACY_EXPECTED


def _guard_requested(rl: RunLog, to: str, **extra) -> None:
    rl.append(
        {
            "event_type": EventType.DRAFT_GUARD_REQUESTED.value,
            "run_id": "r1",
            "cycle_id": "fix-1",
            "to": to,
            "idempotency_key": f"guard:r1:fix-1:{to}:a1",
            **extra,
        }
    )


def _guard_settled(rl: RunLog, to: str, outcome: str, **extra) -> None:
    rl.append(
        {
            "event_type": EventType.DRAFT_GUARD_SETTLED.value,
            "run_id": "r1",
            "cycle_id": "fix-1",
            "to": to,
            "idempotency_key": f"guard:r1:fix-1:{to}:a1",
            "outcome": outcome,
            "changed": outcome == "confirmed",
            "cause": None,
            **extra,
        }
    )


def test_fold_guard_request_and_confirmed_settle_rebuild_phase_held(tmp_path):
    rl = RunLog(301, tmp_path)
    _guard_requested(rl, "draft", timeline_baseline=2, original_is_draft=False)
    _guard_settled(rl, "draft", "confirmed")
    guard = rl.rebuild_state()["draft_guard"]
    assert guard["phase"] == "held"
    assert guard["owned_draft"] is True
    assert guard["run_toggles"] == 1
    assert guard["unsettled"] == 0
    assert guard["baseline"] == 2


def test_fold_guard_request_alone_is_engage_pending_with_one_unsettled(tmp_path):
    rl = RunLog(302, tmp_path)
    _guard_requested(rl, "draft", timeline_baseline=0, original_is_draft=False)
    guard = rl.rebuild_state()["draft_guard"]
    assert guard["phase"] == "engage_pending"
    assert guard["unsettled"] == 1
    assert guard["owned_draft"] is False


def test_guard_state_survives_the_snapshot_round_trip(tmp_path):
    """The folded record is plain data, so the rebuildable snapshot can store it."""
    rl = RunLog(303, tmp_path)
    _guard_requested(rl, "draft", timeline_baseline=1, original_is_draft=False)
    _guard_settled(rl, "draft", "confirmed")
    state = rl.materialize_snapshot()
    assert json.loads(rl.snapshot_path.read_text(encoding="utf-8")) == state


def test_fold_sync_push_counts_in_sync_push_count_not_push_count(tmp_path):
    """A landed `kind: "sync"` push counts in sync_push_count only (INV-018)."""
    rl = RunLog(201, tmp_path)
    _push(rl, "sync-1", _SHA_B, _SHA_D, push_kind="sync", base_sha=_SHA_C)
    state = rl.rebuild_state()
    assert state["sync_push_count"] == 1
    assert state["push_count"] == 0
    assert state["pushed_commit_shas"] == [_SHA_D]


@pytest.mark.parametrize("push_kind", ["fix", "ci", "merge", None])
def test_fold_fix_ci_merge_and_kindless_pushes_count_in_push_count(tmp_path, push_kind):
    """`fix`, `ci`, `merge` and kind-less landed pushes count in push_count."""
    rl = RunLog(202, tmp_path)
    _push(rl, "c1", _SHA_B, _SHA_A, push_kind=push_kind)
    # A falsy `kind` reads as `fix` too (absent means fix).
    rl.append(
        {
            "event_type": EventType.PUSH_COMPLETED.value,
            "kind": "",
            "target_sha": _SHA_E,
        }
    )
    state = rl.rebuild_state()
    assert state["push_count"] == 2
    assert state["sync_push_count"] == 0
    assert state["pushed_commit_shas"] == [_SHA_A, _SHA_E]


def test_fold_conflict_cycles_first_seen_order_and_open_cycle(tmp_path):
    """conflict_cycles keeps first-seen order (not sorted) and counts a resume
    restart's reused id once; the open cycle tracks push_initiated / push_completed."""
    rl = RunLog(203, tmp_path)
    _sync_started(rl, "sync-2")
    _sync_concluded(rl, "sync-2", "aborted")
    _sync_started(rl, "conflict-1")
    state = rl.rebuild_state()
    assert state["conflict_cycles"] == ["sync-2", "conflict-1"]
    assert state["open_conflict_cycle"]["cycle_id"] == "conflict-1"
    # A resume restart: close the open attempt, re-open the same id.
    _sync_concluded(rl, "conflict-1", "aborted", recovered=True)
    _sync_started(rl, "conflict-1", resumed=True)
    state = rl.rebuild_state()
    assert state["conflict_cycles"] == ["sync-2", "conflict-1"]
    open_cycle = state["open_conflict_cycle"]
    assert open_cycle["cycle_id"] == "conflict-1"
    assert open_cycle["resumed"] is True
    assert (open_cycle["push_initiated"], open_cycle["push_completed"]) == (
        False,
        False,
    )
    assert open_cycle["target_sha"] is None
    assert open_cycle["expect_checks"] is None
    assert open_cycle["superseded"] is False
    # push_initiated sets its flag, target_sha and a bool expect_checks.
    _push(
        rl,
        "conflict-1",
        _SHA_B,
        _SHA_D,
        land=False,
        push_kind="merge",
        base_sha=_SHA_C,
        expect_checks=False,
    )
    open_cycle = rl.rebuild_state()["open_conflict_cycle"]
    assert (open_cycle["push_initiated"], open_cycle["push_completed"]) == (
        True,
        False,
    )
    assert open_cycle["target_sha"] == _SHA_D
    assert open_cycle["expect_checks"] is False
    # push_completed sets its flag; the cycle stays open until sync_concluded.
    rl.append(
        {
            "event_type": EventType.PUSH_COMPLETED.value,
            "cycle_id": "conflict-1",
            "kind": "merge",
            "target_sha": _SHA_D,
        }
    )
    state = rl.rebuild_state()
    assert state["open_conflict_cycle"]["push_completed"] is True
    assert state["push_count"] == 1
    _sync_concluded(rl, "conflict-1")
    state = rl.rebuild_state()
    assert state["open_conflict_cycle"] is None
    assert state["conflict_cycles"] == ["sync-2", "conflict-1"]


@pytest.mark.parametrize("raw", ["absent", None, "yes", 1, 0])
def test_fold_push_initiated_expect_checks_fails_closed_to_true(tmp_path, raw):
    """A missing or non-bool expect_checks on the cycle's push_initiated is stored
    as True, so conflict_resume_plan row 4 never reads None or a defaulted False."""
    rl = RunLog(204, tmp_path)
    _sync_started(rl, "sync-1")
    record = {
        "event_type": EventType.PUSH_INITIATED.value,
        "cycle_id": "sync-1",
        "kind": "sync",
        "target_sha": _SHA_D,
    }
    if raw != "absent":
        record["expect_checks"] = raw
    rl.append(record)
    assert rl.rebuild_state()["open_conflict_cycle"]["expect_checks"] is True


def test_fold_push_rejected(tmp_path):
    """push_aborted_or_not_landed with `rejected is True` sets push_rejected; a
    Branch B record without it, or with a truthy non-True value, does not."""
    rl = RunLog(205, tmp_path)
    for rejected in ("absent", False, "true", 1):
        record = {
            "event_type": EventType.PUSH_ABORTED_OR_NOT_LANDED.value,
            "cycle_id": "c1",
        }
        if rejected != "absent":
            record["rejected"] = rejected
        rl.append(record)
    assert rl.rebuild_state()["push_rejected"] is False
    rl.append(
        {
            "event_type": EventType.PUSH_ABORTED_OR_NOT_LANDED.value,
            "cycle_id": "sync-1",
            "rejected": True,
            "stderr_tail": "! [rejected] (fetch first)",
        }
    )
    assert rl.rebuild_state()["push_rejected"] is True


def test_fold_open_cycle_carries_hook_and_review_terminal(tmp_path):
    """B3: the open-cycle entry carries `hook` and `review_terminal` from its
    sync_started, which conflict_resume_plan rows 4c, 5 and 7 read."""
    rl = RunLog(206, tmp_path)
    _sync_started(rl, "sync-1", review_terminal="halt_max_rounds")
    open_cycle = rl.rebuild_state()["open_conflict_cycle"]
    assert open_cycle["hook"] == "wave8a"
    assert open_cycle["review_terminal"] == "halt_max_rounds"
    assert open_cycle["kind"] == "sync"
    assert open_cycle["base_sha"] == _SHA_C
    assert open_cycle["pre_push_sha"] == _SHA_B
    _sync_concluded(rl, "sync-1", "aborted")
    _sync_started(rl, "conflict-1")
    open_cycle = rl.rebuild_state()["open_conflict_cycle"]
    assert open_cycle["hook"] == "c_initial"
    assert open_cycle["review_terminal"] is None
    # The fold's output is exactly what the resume planner reads (row 4: a landed
    # sync push with no expect_checks on its push_initiated reads as True).
    rl2 = RunLog(207, tmp_path / "row4")
    _sync_started(rl2, "sync-1")
    _push(rl2, "sync-1", _SHA_B, _SHA_D, push_kind="sync", base_sha=_SHA_C)
    plan = conflict_resume_plan(
        rl2.rebuild_state(),
        foreign_op=None,
        merge_head_sha=None,
        local_head_sha=_SHA_D,
        local_head_parents=[_SHA_B, _SHA_C],
        dangling=None,
    )
    assert plan.directive == "complete_after_push"
    assert (plan.cycle_id, plan.hook, plan.review_terminal) == (
        "sync-1",
        "wave8a",
        "clean",
    )
    assert plan.wait_sha == _SHA_D
    assert plan.expect_checks is True


def test_fold_push_of_another_cycle_marks_open_cycle_superseded(tmp_path):
    """B2 belt: a push_initiated of a different cycle marks the still-open cycle
    superseded (conflict_resume_plan row 3b halts on it); its own push does not."""
    rl = RunLog(208, tmp_path)
    _sync_started(rl, "sync-1")
    _push(rl, "sync-1", _SHA_B, _SHA_D, land=False, push_kind="sync", base_sha=_SHA_C)
    assert rl.rebuild_state()["open_conflict_cycle"]["superseded"] is False
    _push(rl, "fix-cycle-2", _SHA_D, _SHA_A)
    state = rl.rebuild_state()
    open_cycle = state["open_conflict_cycle"]
    assert open_cycle["cycle_id"] == "sync-1"
    assert open_cycle["superseded"] is True
    assert open_cycle["push_completed"] is False  # another cycle's completion
    plan = conflict_resume_plan(
        state,
        foreign_op=None,
        merge_head_sha=None,
        local_head_sha=_SHA_A,
        local_head_parents=[_SHA_D],
        dangling=None,
    )
    assert (plan.directive, plan.reason, plan.cycle_id) == (
        "halt",
        "resume_unrepresentable",
        "sync-1",
    )


def test_rebuild_state_with_a_conflict_push_in_the_fixture(tmp_path):
    """QA-1: the legacy fixture (one fix push, one round tick, one re-triggered
    cycle) plus a Tier 1 sync push and a Tier 2 merge push with its re-review and
    round tick folds to exact counters."""
    rl = _legacy_runlog(tmp_path)
    # Tier 1 sync cycle (Wave 8a): never ticks a round, never counts in push_count.
    _sync_started(rl, "sync-1")
    _push(
        rl,
        "sync-1",
        _SHA_B,
        _SHA_D,
        push_kind="sync",
        base_sha=_SHA_C,
        review_terminal="clean",
        expect_checks=True,
    )
    _sync_concluded(rl, "sync-1")
    # Tier 2 merge cycle (C-initial): counts in push_count, re-review, round tick.
    _sync_started(rl, "conflict-2", pre_push_sha=_SHA_D)
    _push(rl, "conflict-2", _SHA_D, _SHA_E, push_kind="merge", base_sha=_SHA_C)
    _sync_concluded(rl, "conflict-2", merge_sha=_SHA_E)
    for reviewer in ("augment", "codex"):
        rl.append(
            {
                "event_type": EventType.REREVIEW_REQUESTED.value,
                "cycle_id": "conflict-2",
                "reviewer": reviewer,
            }
        )
    rl.append({"event_type": EventType.ROUND_INCREMENTED.value})
    state = rl.rebuild_state()
    assert state["push_count"] == 2  # the legacy fix push + the merge push
    assert state["sync_push_count"] == 1
    assert state["round_counter"] == 2  # the legacy tick + the merge cycle's tick
    assert state["rereview_request_count"] == 2  # cycles c1 and conflict-2
    assert state["conflict_cycles"] == ["sync-1", "conflict-2"]
    assert state["open_conflict_cycle"] is None
    assert state["push_rejected"] is False
    assert state["pushed_commit_shas"] == [_SHA_A, _SHA_D, _SHA_E]


def test_sync_concluded_payload_is_redacted(tmp_path):
    """NFR-7: a token-shaped string in a sync_concluded `dropped` list reaches the
    JSONL as [REDACTED]."""
    rl = RunLog(209, tmp_path)
    token = "ghp_ABCDEFGHIJKLMNOP0123456789"
    _sync_concluded(
        rl,
        "conflict-1",
        dropped=[f"removed the line export GH_TOKEN={token}", token],
    )
    raw = rl.jsonl_path.read_text(encoding="utf-8")
    assert "ghp_ABCDEFGHIJKLMNOP" not in raw
    dropped = json.loads(raw.splitlines()[-1])["dropped"]
    assert dropped[1] == "[REDACTED]"
    assert "[REDACTED]" in dropped[0]
