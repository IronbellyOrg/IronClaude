"""Tests for the pure merge-guard core (issue #375): ids, fold, status, matchers."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from superclaude.pr_submit import conflicts, recovery
from superclaude.pr_submit import merge_guard as mg
from superclaude.pr_submit.models import EventType

MODULE = Path(mg.__file__)


# --- event builders -------------------------------------------------------------


def _key(cycle: str, to: str, attempt: int = 1) -> str:
    return f"guard:r1:{cycle}:{to}:a{attempt}"


def req(to, *, cycle="fix-1", attempt=1, baseline=None, original=None):
    event = {
        "event_type": "draft_guard_requested",
        "run_id": "r1",
        "cycle_id": cycle,
        "to": to,
        "idempotency_key": _key(cycle, to, attempt),
    }
    if baseline is not None:
        event["timeline_baseline"] = baseline
    if original is not None:
        event["original_is_draft"] = original
    return event


def settled(
    to,
    outcome,
    *,
    changed=False,
    cause=None,
    cycle="fix-1",
    attempt=1,
    original=None,
    with_key=True,
):
    event = {
        "event_type": "draft_guard_settled",
        "run_id": "r1",
        "cycle_id": cycle,
        "to": to,
        "outcome": outcome,
        "changed": changed,
        "cause": cause,
    }
    if with_key:
        event["idempotency_key"] = _key(cycle, to, attempt)
    if original is not None:
        event["original_is_draft"] = original
    return event


def push_completed(cycle, **extra):
    return {"event_type": "push_completed", "cycle_id": cycle, **extra}


ENGAGED = [
    req("draft", baseline=2, original=False),
    settled("draft", "confirmed", changed=True),
]


# --- cycle ids ------------------------------------------------------------------


def test_fix_cycle_id_values_and_errors():
    assert mg.fix_cycle_id("fix", 2) == "fix-2"
    assert mg.fix_cycle_id("ci", 1) == "ci-1"
    for kind, n in (
        ("sync", 1),
        ("conflict", 1),
        ("fix", 0),
        ("ci", -1),
        ("fix", True),
    ):
        with pytest.raises(ValueError):
            mg.fix_cycle_id(kind, n)


@pytest.mark.parametrize("kind", ["fix", "ci"])
def test_fix_cycle_ids_never_look_like_conflict_cycles(kind):
    assert not conflicts.is_conflict_cycle(mg.fix_cycle_id(kind, 1))
    assert not mg.fix_cycle_id(kind, 7).startswith(conflicts.CONFLICT_CYCLE_PREFIXES)


def test_next_cycle_number():
    assert mg.next_cycle_number([], "fix") == 1
    events = [
        {"cycle_id": "fix-1"},
        {"cycle_id": "fix-2"},
        {"cycle_id": "ci-4"},
        {"cycle_id": "sync-9"},
        {},
    ]
    assert mg.next_cycle_number(events, "fix") == 3
    assert mg.next_cycle_number(events, "ci") == 5
    assert mg.next_cycle_number("not a list", "fix") == 1
    with pytest.raises(ValueError):
        mg.next_cycle_number([], "sync")


# --- fold -----------------------------------------------------------------------

FOLD_CASES = {
    "engage_confirmed_changed": (
        ENGAGED,
        {
            "phase": "held",
            "owned_draft": True,
            "run_toggles": 1,
            "unsettled": 0,
            "baseline": 2,
            "original_is_draft": False,
            "failed_mutations": 0,
        },
    ),
    "request_only": (
        [req("draft", baseline=4, original=False)],
        {
            "phase": "engage_pending",
            "unsettled": 1,
            "owned_draft": False,
            "baseline": 4,
        },
    ),
    "draft_failed": (
        [req("draft", baseline=1, original=False), settled("draft", "failed")],
        {
            "phase": "release_pending",
            "failed_mutations": 1,
            "owned_draft": False,
            "run_toggles": 0,
            "unsettled": 0,
        },
    ),
    "draft_confirmed_not_changed": (
        [
            req("draft", baseline=1, original=False),
            settled("draft", "confirmed", changed=False),
        ],
        {"phase": "held", "owned_draft": True, "run_toggles": 0},
    ),
    "ready_confirmed_changed": (
        ENGAGED + [req("ready"), settled("ready", "confirmed", changed=True)],
        {"phase": "released", "owned_draft": False, "run_toggles": 2, "unsettled": 0},
    ),
    "ready_confirmed_not_changed": (
        ENGAGED + [req("ready"), settled("ready", "confirmed", changed=False)],
        {"phase": "released", "owned_draft": False, "run_toggles": 1},
    ),
    "ready_request_only": (
        ENGAGED + [req("ready")],
        {
            "phase": "release_pending",
            "phase_before_request": "held",
            "unsettled": 1,
            "owned_draft": True,
        },
    ),
    "ready_failed": (
        ENGAGED + [req("ready"), settled("ready", "failed")],
        {
            "phase": "release_pending",
            "failed_mutations": 1,
            "owned_draft": True,
            "run_toggles": 1,
        },
    ),
    "skip_already_draft_without_request": (
        [
            settled(
                "draft", "skipped", cause="already_draft", with_key=False, original=True
            )
        ],
        {
            "phase": "disabled",
            "disabled_cause": "already_draft",
            "original_is_draft": True,
            "owned_draft": False,
            "unsettled": 0,
        },
    ),
    "skip_user_override_after_hold": (
        ENGAGED + [settled("ready", "skipped", cause="user_override", with_key=False)],
        {
            "phase": "disabled",
            "disabled_cause": "user_override",
            "owned_draft": False,
            "run_toggles": 1,
        },
    ),
    "retry_after_failed_engage": (
        [
            req("draft", baseline=1, original=False),
            settled("draft", "failed"),
            req("draft", attempt=2),
            settled("draft", "confirmed", changed=True, attempt=2),
        ],
        {
            "phase": "held",
            "failed_mutations": 1,
            "run_toggles": 1,
            "owned_draft": True,
            "baseline": 1,
            "unsettled": 0,
        },
    ),
    "ready_not_applied_returns_to_held": (
        ENGAGED + [req("ready"), settled("ready", "skipped", cause="not_applied")],
        {
            "phase": "held",
            "unsettled": 0,
            "owned_draft": True,
            "run_toggles": 1,
            "failed_mutations": 0,
            "disabled_cause": None,
        },
    ),
    # A ready-direction not_applied returns to the phase before the request, so
    # after a failed release it is RELEASE_PENDING again, and it leaves the failure
    # count and ownership alone whether or not the draft was owned.
    "ready_not_applied_after_failed_release": (
        ENGAGED
        + [
            req("ready"),
            settled("ready", "failed"),
            req("ready", attempt=2),
            settled("ready", "skipped", cause="not_applied", attempt=2),
        ],
        {
            "phase": "release_pending",
            "unsettled": 0,
            "failed_mutations": 1,
            "owned_draft": True,
            "run_toggles": 1,
            "disabled_cause": None,
        },
    ),
    "ready_not_applied_after_failed_engage": (
        [
            req("draft", baseline=1, original=False),
            settled("draft", "failed"),
            req("ready"),
            settled("ready", "skipped", cause="not_applied"),
        ],
        {
            "phase": "release_pending",
            "unsettled": 0,
            "failed_mutations": 1,
            "owned_draft": False,
            "run_toggles": 0,
            "disabled_cause": None,
        },
    ),
    # A failed draft call leaves ownership as it was: still owned after an earlier
    # confirmed engage.
    "draft_failed_keeps_ownership": (
        ENGAGED
        + [req("draft", cycle="fix-2"), settled("draft", "failed", cycle="fix-2")],
        {
            "phase": "release_pending",
            "unsettled": 0,
            "failed_mutations": 1,
            "owned_draft": True,
            "run_toggles": 1,
        },
    ),
    # original_is_draft comes only from the first guard record, never from a later
    # skip settle either.
    "later_skip_does_not_overwrite_original_is_draft": (
        ENGAGED
        + [
            settled(
                "ready",
                "skipped",
                cause="user_override",
                with_key=False,
                original=True,
            )
        ],
        {"phase": "disabled", "original_is_draft": False, "owned_draft": False},
    ),
    "draft_not_applied_after_failed_engage_returns_to_release_pending": (
        [
            req("draft", baseline=1, original=False),
            settled("draft", "failed"),
            req("draft", attempt=2),
            settled("draft", "skipped", cause="not_applied", attempt=2),
        ],
        {
            "phase": "release_pending",
            "unsettled": 0,
            "failed_mutations": 1,
            "owned_draft": False,
            "run_toggles": 0,
            "disabled_cause": None,
        },
    ),
    # A draft-direction not_applied must leave ownership and the toggle counters
    # alone whatever the earlier state was (owned, released or disabled).
    "draft_not_applied_keeps_a_held_state": (
        ENGAGED
        + [
            req("draft", cycle="fix-2"),
            settled("draft", "skipped", cause="not_applied", cycle="fix-2"),
        ],
        {
            "phase": "held",
            "unsettled": 0,
            "owned_draft": True,
            "run_toggles": 1,
            "failed_mutations": 0,
            "disabled_cause": None,
        },
    ),
    "draft_not_applied_keeps_a_released_state": (
        ENGAGED
        + [
            req("ready"),
            settled("ready", "confirmed", changed=True),
            req("draft", cycle="fix-2"),
            settled("draft", "skipped", cause="not_applied", cycle="fix-2"),
        ],
        {
            "phase": "released",
            "unsettled": 0,
            "owned_draft": False,
            "run_toggles": 2,
            "failed_mutations": 0,
            "disabled_cause": None,
        },
    ),
    "draft_not_applied_keeps_a_disabled_state": (
        [
            settled(
                "draft",
                "skipped",
                cause="already_draft",
                with_key=False,
                original=True,
            ),
            req("draft", cycle="fix-2"),
            settled("draft", "skipped", cause="not_applied", cycle="fix-2"),
        ],
        {
            "phase": "disabled",
            "unsettled": 0,
            "owned_draft": False,
            "run_toggles": 0,
            "original_is_draft": True,
            "disabled_cause": "already_draft",
        },
    ),
}


@pytest.mark.parametrize("name", sorted(FOLD_CASES))
def test_fold_effect_table(name):
    events, expected = FOLD_CASES[name]
    state = mg.fold_draft_guard(events)
    assert state is not None
    for key, value in expected.items():
        assert state[key] == value, (name, key, state)


def test_fold_returns_none_without_guard_events():
    assert mg.fold_draft_guard([]) is None
    assert (
        mg.fold_draft_guard([{"event_type": "push_completed", "cycle_id": "fix-1"}])
        is None
    )
    assert mg.fold_draft_guard("not a list") is None


def test_fold_first_request_not_applied_erases_the_record():
    events = [
        req("draft", baseline=1, original=False),
        settled("draft", "skipped", cause="not_applied"),
    ]
    assert mg.fold_draft_guard(events) is None


def test_fold_request_not_applied_request_takes_a_fresh_baseline():
    events = [
        req("draft", baseline=1, original=False),
        settled("draft", "skipped", cause="not_applied"),
        req("draft", cycle="fix-2", baseline=5, original=True),
    ]
    state = mg.fold_draft_guard(events)
    assert state["baseline"] == 5
    assert state["original_is_draft"] is True
    assert state["phase"] == "engage_pending"
    assert state["cycle_id"] == "fix-2"


def test_fold_user_override_sets_disabled_cause_and_feeds_guard_status():
    state = mg.fold_draft_guard(
        ENGAGED + [settled("ready", "skipped", cause="user_override", with_key=False)]
    )
    assert (state["phase"], state["owned_draft"], state["disabled_cause"]) == (
        "disabled",
        False,
        "user_override",
    )
    assert mg.guard_status(state, "draft", 3) == "user_override"


def test_fold_original_is_draft_comes_only_from_the_first_record():
    events = ENGAGED + [
        req("ready", original=True),
        settled("ready", "confirmed", changed=True, original=True),
    ]
    assert mg.fold_draft_guard(events)["original_is_draft"] is False


def test_fold_state_is_plain_data():
    state = mg.fold_draft_guard(ENGAGED)
    assert type(state["phase"]) is str
    assert set(state) == {
        "phase",
        "phase_before_request",
        "cycle_id",
        "original_is_draft",
        "baseline",
        "run_toggles",
        "unsettled",
        "failed_mutations",
        "owned_draft",
        "disabled_cause",
    }


# --- guard_status ---------------------------------------------------------------


def _guard(phase, owned=False, cause=None):
    return {"phase": phase, "owned_draft": owned, "disabled_cause": cause}


STATUS_CASES = [
    (None, "off", 3, "off"),
    (None, "draft", 2, "off"),
    (None, "draft", 3, "released"),
    (_guard("held", True), "draft", 3, "held"),
    (_guard("held", True), "off", 3, "held"),
    (_guard("engage_pending", True), "draft", 3, "held"),
    (_guard("engage_pending", False), "draft", 3, "unavailable"),
    (_guard("release_pending", True), "draft", 3, "held"),
    (_guard("release_pending", False), "draft", 3, "unavailable"),
    (_guard("disabled", False, "user_override"), "draft", 3, "user_override"),
    (_guard("disabled", False, "already_draft"), "draft", 3, "off"),
    (_guard("disabled", False, None), "draft", 3, "unavailable"),
    (_guard("released", False), "draft", 3, "released"),
]


@pytest.mark.parametrize(("guard", "mode", "ordinal", "expected"), STATUS_CASES)
def test_guard_status_mapping(guard, mode, ordinal, expected):
    assert mg.guard_status(guard, mode, ordinal) == expected


def test_failed_engage_reports_unavailable():
    state = mg.fold_draft_guard(
        [req("draft", baseline=1, original=False), settled("draft", "failed")]
    )
    assert mg.guard_status(state, "draft", 3) == "unavailable"


# --- pending_requests and held_cycle_published ----------------------------------


def test_pending_requests_pairs_by_idempotency_key():
    events = [
        req("draft", baseline=1, original=False),
        settled("draft", "failed"),
        req("draft", attempt=2),
        req("ready", cycle="fix-2"),
    ]
    pending = mg.pending_requests(events)
    assert [event["idempotency_key"] for event in pending] == [
        "guard:r1:fix-1:draft:a2",
        "guard:r1:fix-2:ready:a1",
    ]
    assert mg.pending_requests(ENGAGED) == []
    assert mg.pending_requests([]) == []


def test_pending_requests_tell_retries_apart_by_the_attempt_suffix():
    """Settling the a2 retry leaves the unsettled a1 request pending."""
    events = [
        req("draft", baseline=1, original=False),
        req("draft", attempt=2),
        settled("draft", "failed", attempt=2),
    ]
    assert [e["idempotency_key"] for e in mg.pending_requests(events)] == [
        "guard:r1:fix-1:draft:a1"
    ]


def test_held_cycle_published_normal_recovered_and_other_cycle():
    guard = mg.fold_draft_guard(ENGAGED)
    assert mg.held_cycle_published(ENGAGED + [push_completed("fix-1")], guard) is True
    assert (
        mg.held_cycle_published(
            ENGAGED + [push_completed("fix-1", recovered=True)], guard
        )
        is True
    )
    assert mg.held_cycle_published(ENGAGED + [push_completed("fix-2")], guard) is False
    assert mg.held_cycle_published(ENGAGED, guard) is False
    assert mg.held_cycle_published(ENGAGED + [push_completed("fix-1")], None) is False


# --- constants that must equal other modules ------------------------------------


def test_branch_constants_equal_recovery_constants():
    assert mg.BRANCH_LANDED == recovery.BRANCH_A_LANDED
    assert mg.BRANCH_NOT_LANDED == recovery.BRANCH_B_NOT_LANDED
    assert mg.BRANCH_AMBIGUOUS == recovery.BRANCH_C_AMBIGUOUS


def test_event_names_equal_event_type_values():
    assert mg.REQUESTED == EventType.DRAFT_GUARD_REQUESTED.value
    assert mg.SETTLED == EventType.DRAFT_GUARD_SETTLED.value


# --- purity ---------------------------------------------------------------------


def test_module_has_no_version_control_or_hosting_command_word():
    token = re.compile(r"\bgh\b|\bgit\b")
    offenders = [
        f"{number}: {line.strip()}"
        for number, line in enumerate(
            MODULE.read_text(encoding="utf-8").splitlines(), 1
        )
        if token.search(line)
    ]
    assert not offenders, offenders


def test_module_imports_only_the_allowed_modules():
    imports = re.findall(
        r"^(?:from|import)\s+(\S+)", MODULE.read_text(encoding="utf-8"), re.M
    )
    assert set(imports) <= {"__future__", "re", "dataclasses", "enum", ".conflicts"}, (
        imports
    )


# =============================================================================
# classify_toggles, engage_decision, release_decision, resume_decision
# =============================================================================

H = "a" * 40  # head sha
T = "b" * 40  # another sha


def rd(**overrides):
    fields = {
        "ok": True,
        "state": "OPEN",
        "is_draft": True,
        "head_sha": H,
        "auto_merge_armed": False,
        "transitions": 3,
        "complete": True,
    }
    fields.update(overrides)
    return mg.GuardRead(**fields)


def guard(phase="held", **overrides):
    fields = {
        "phase": phase,
        "phase_before_request": None,
        "cycle_id": "fix-1",
        "original_is_draft": False,
        "baseline": 2,
        "run_toggles": 1,
        "unsettled": 0,
        "failed_mutations": 0,
        "owned_draft": True,
        "disabled_cause": None,
    }
    fields.update(overrides)
    return fields


A = mg.GuardAction


def check(decision, action, reason, cause=None, notes=()):
    assert decision.action == action, decision
    assert decision.reason == reason, decision
    assert decision.cause == cause, decision
    assert decision.notes == notes, decision


# --- classify_toggles -----------------------------------------------------------

CLASSIFY_CASES = {
    "incomplete_timeline": (guard(), rd(complete=False), "unreadable"),
    "transitions_missing": (guard(), rd(transitions=None), "unreadable"),
    "read_failed": (guard(), rd(ok=False), "unreadable"),
    "draft_flag_missing": (guard(), rd(is_draft=None), "unreadable"),
    "no_guard": (None, rd(), "unreadable"),
    "baseline_missing": (guard(baseline=None), rd(), "unreadable"),
    "observed_below_run_toggles": (guard(), rd(transitions=2), "unreadable"),
    "one_extra_transition": (guard(), rd(transitions=4), "foreign"),
    "held_but_pr_is_ready": (guard(), rd(is_draft=False), "foreign"),
    "released_but_pr_is_draft": (
        guard("released", run_toggles=2),
        rd(transitions=4, is_draft=True),
        "foreign",
    ),
    "held_matches": (guard(), rd(), "ok"),
    "released_matches": (
        guard("released", run_toggles=2),
        rd(transitions=4, is_draft=False),
        "ok",
    ),
    "equals_run_toggles_plus_failed": (
        guard(failed_mutations=1),
        rd(transitions=4),
        "ok",
    ),
    "failed_call_did_not_land": (guard(failed_mutations=1), rd(transitions=3), "ok"),
    "two_over_with_one_failed": (
        guard(failed_mutations=1),
        rd(transitions=5),
        "foreign",
    ),
    "pending_engage_accepts_draft": (
        guard("engage_pending", run_toggles=0, unsettled=1, owned_draft=False),
        rd(transitions=3, is_draft=True),
        "ok",
    ),
    "pending_engage_accepts_ready": (
        guard("engage_pending", run_toggles=0, unsettled=1, owned_draft=False),
        rd(transitions=2, is_draft=False),
        "ok",
    ),
    "pending_release_accepts_draft": (
        guard("release_pending", unsettled=1),
        rd(transitions=3, is_draft=True),
        "ok",
    ),
    "pending_release_accepts_ready": (
        guard("release_pending", unsettled=1),
        rd(transitions=4, is_draft=False),
        "ok",
    ),
    "failed_on_client_but_landed": (
        guard("release_pending", run_toggles=0, failed_mutations=1, owned_draft=False),
        rd(transitions=3, is_draft=True),
        "ok",
    ),
    "ready_then_user_redrafts": (
        guard("released", run_toggles=2),
        rd(transitions=5, is_draft=True),
        "foreign",
    ),
}


@pytest.mark.parametrize("name", sorted(CLASSIFY_CASES))
def test_classify_toggles(name):
    state, read, expected = CLASSIFY_CASES[name]
    assert mg.classify_toggles(state, read) == expected


# --- engage_decision ------------------------------------------------------------


def engage(**overrides):
    kwargs = {
        "mode": "draft",
        "ordinal": 3,
        "cycle_id": "fix-1",
        "guard": None,
        "read": rd(is_draft=False, transitions=2),
    }
    kwargs.update(overrides)
    return mg.engage_decision(**kwargs)


@pytest.mark.parametrize(
    ("overrides", "reason"),
    [
        ({"mode": "off"}, "mode_off"),
        ({"mode": mg.GuardMode.OFF}, "mode_off"),
        ({"ordinal": 2}, "ordinal"),
        ({"ordinal": 0}, "ordinal"),
        ({"cycle_id": "sync-1"}, "conflict_cycle"),
        ({"cycle_id": "conflict-1"}, "conflict_cycle"),
    ],
)
def test_engage_row_1_inert(overrides, reason):
    check(engage(**overrides), A.NOOP, reason)


def test_engage_row_2_disabled():
    check(
        engage(guard=guard("disabled", disabled_cause="user_override")),
        A.NOOP,
        "disabled",
    )


def test_engage_row_3_read_failed():
    check(engage(read=rd(ok=False, state=None)), A.HALT_UNAVAILABLE, "read_failed")


@pytest.mark.parametrize("state", ["MERGED", "CLOSED"])
def test_engage_row_4_pr_not_open(state):
    check(engage(read=rd(state=state)), A.HALT_PR_NOT_OPEN, "pr_not_open")


def test_engage_row_5_retry_release_when_owned():
    check(engage(guard=guard("release_pending")), A.RETRY_RELEASE, "release_pending")


def test_engage_row_6_hold_when_ownership_unproven():
    check(
        engage(guard=guard("release_pending", owned_draft=False)),
        A.HOLD,
        "ownership_unproven",
    )


def test_engage_row_7_already_held():
    check(engage(guard=guard("held")), A.NOOP, "already_held")


@pytest.mark.parametrize(
    "read", [rd(complete=False, is_draft=False), rd(transitions=None, is_draft=False)]
)
def test_engage_row_8_timeline_unreadable(read):
    check(engage(read=read), A.HALT_UNAVAILABLE, "timeline_unreadable")


def test_engage_row_9_foreign_toggle_skips_engage():
    state = guard("released", run_toggles=2)
    check(
        engage(guard=state, read=rd(transitions=5, is_draft=False)),
        A.SKIP_USER_OVERRIDE,
        "user_override",
        cause="user_override",
    )


def test_engage_row_10_already_draft_without_guard():
    check(
        engage(read=rd(is_draft=True)),
        A.SKIP_ALREADY_DRAFT,
        "already_draft",
        cause="already_draft",
    )


def test_engage_row_11_engage_and_auto_merge_note():
    check(engage(), A.ENGAGE, "engage")
    check(
        engage(read=rd(is_draft=False, auto_merge_armed=True)),
        A.ENGAGE,
        "engage",
        notes=("auto_merge_armed",),
    )


def test_engage_second_cycle_after_a_release_engages_again():
    state = guard("released", run_toggles=2)
    check(
        engage(guard=state, cycle_id="fix-2", read=rd(transitions=4, is_draft=False)),
        A.ENGAGE,
        "engage",
    )


# --- release_decision -----------------------------------------------------------


def release(**overrides):
    kwargs = {
        "mode": "draft",
        "ordinal": 3,
        "cycle_id": "fix-1",
        "guard": guard(),
        "read": rd(),
        "applied_edits": 2,
        "target_sha": H,
        "push_completed": True,
    }
    kwargs.update(overrides)
    return mg.release_decision(**kwargs)


@pytest.mark.parametrize(
    ("overrides", "reason"),
    [
        ({"mode": "off"}, "mode_off"),
        ({"ordinal": 1}, "ordinal"),
        ({"cycle_id": "sync-2"}, "conflict_cycle"),
    ],
)
def test_release_row_1_inert(overrides, reason):
    check(release(**overrides), A.NOOP, reason)


@pytest.mark.parametrize(
    "state",
    [
        None,
        guard("released"),
        guard("disabled", disabled_cause="already_draft"),
        guard("engage_pending"),
    ],
)
def test_release_row_2_not_held(state):
    check(release(guard=state), A.NOOP, "not_held")


def test_release_row_3_read_failed():
    check(release(read=rd(ok=False)), A.HOLD, "read_failed")


def test_release_row_4_pr_not_open():
    check(release(read=rd(state="MERGED")), A.HALT_PR_NOT_OPEN, "pr_not_open")


def test_release_row_5_timeline_unreadable():
    check(release(read=rd(transitions=None)), A.HOLD, "timeline_unreadable")


def test_release_row_6_foreign_toggle():
    check(
        release(read=rd(is_draft=False)),
        A.SKIP_USER_OVERRIDE,
        "user_override",
        cause="user_override",
    )


def test_release_row_7_zero_edits_releases_without_a_push():
    check(
        release(applied_edits=0, push_completed=False, target_sha=None),
        A.RELEASE,
        "no_edits",
        cause="no_edits",
    )


def test_release_row_7_applies_to_a_zero_edit_cycle_after_a_fixing_cycle():
    earlier = guard(cycle_id="fix-2", run_toggles=3, baseline=2)
    read = rd(transitions=5)
    check(
        release(
            guard=earlier,
            cycle_id="fix-2",
            read=read,
            applied_edits=0,
            push_completed=False,
        ),
        A.RELEASE,
        "no_edits",
        cause="no_edits",
    )


def test_release_row_8_published_head_releases():
    check(release(), A.RELEASE, "pushed", cause="pushed")
    check(
        release(guard=guard("release_pending", unsettled=0, failed_mutations=1)),
        A.RELEASE,
        "pushed",
        cause="pushed",
    )


def test_release_row_9_holds_on_moved_head_or_missing_push():
    check(release(read=rd(head_sha=T)), A.HOLD, "head_mismatch")
    check(release(push_completed=False), A.HOLD, "push_not_completed")
    check(release(target_sha=None), A.HOLD, "head_mismatch")


def test_disabled_guard_never_engages_or_releases():
    state = guard("disabled", disabled_cause="already_draft")
    assert engage(guard=state).action == A.NOOP
    assert release(guard=state).action == A.NOOP


# --- resume_decision ------------------------------------------------------------


def resume(**overrides):
    kwargs = {
        "mode": "draft",
        "ordinal": 3,
        "guard": guard(),
        "read": rd(),
        "pending": [],
        "dangling_branch": None,
        "published": False,
        "applied_edits": 1,
        "target_sha": H,
    }
    kwargs.update(overrides)
    return mg.resume_decision(**kwargs)


def pending_request(to):
    return req(to)


def test_resume_row_1_no_guard():
    check(resume(guard=None), A.NOOP, "no_guard")


def test_resume_row_2_report_held_wins_over_reconcile():
    pending_guard = guard(
        "engage_pending", run_toggles=0, unsettled=1, owned_draft=False
    )
    check(
        resume(ordinal=2, guard=pending_guard, pending=[pending_request("draft")]),
        A.REPORT_HELD,
        "held_report",
    )
    check(resume(mode="off"), A.REPORT_HELD, "held_report")
    check(
        resume(mode=mg.GuardMode.OFF, guard=guard("release_pending")),
        A.REPORT_HELD,
        "held_report",
    )


@pytest.mark.parametrize("phase", ["released", "disabled"])
def test_resume_row_2_skips_settled_phases(phase):
    check(resume(ordinal=2, guard=guard(phase)), A.NOOP, "nothing_to_do")
    check(resume(mode="off", guard=guard(phase)), A.NOOP, "nothing_to_do")


ENGAGE_PENDING = guard("engage_pending", run_toggles=0, unsettled=1, owned_draft=False)
RELEASE_PENDING = guard("release_pending", phase_before_request="held", unsettled=1)


@pytest.mark.parametrize(
    ("state", "to", "read", "reason", "cause"),
    [
        (
            ENGAGE_PENDING,
            "draft",
            rd(is_draft=True, transitions=3),
            "resume_reconciled",
            "resume_reconciled",
        ),
        (
            RELEASE_PENDING,
            "ready",
            rd(is_draft=False, transitions=4),
            "resume_reconciled",
            "resume_reconciled",
        ),
        (
            ENGAGE_PENDING,
            "draft",
            rd(is_draft=False, transitions=2),
            "not_applied",
            "not_applied",
        ),
        (
            RELEASE_PENDING,
            "ready",
            rd(is_draft=True, transitions=3),
            "not_applied",
            "not_applied",
        ),
        (ENGAGE_PENDING, "draft", rd(is_draft=True, transitions=2), "ambiguous", None),
        (ENGAGE_PENDING, "draft", rd(is_draft=False, transitions=3), "ambiguous", None),
        (ENGAGE_PENDING, "draft", rd(transitions=None), "ambiguous", None),
        (ENGAGE_PENDING, "draft", rd(ok=False), "ambiguous", None),
        (ENGAGE_PENDING, "draft", None, "ambiguous", None),
    ],
)
def test_resume_row_3_reconcile_reasons(state, to, read, reason, cause):
    check(
        resume(guard=state, pending=[pending_request(to)], read=read),
        A.RECONCILE,
        reason,
        cause=cause,
    )


def test_resume_row_4_release_after_a_landed_recovered_push():
    check(resume(dangling_branch="landed"), A.RELEASE, "pushed", cause="pushed")
    check(
        resume(dangling_branch=recovery.BRANCH_A_LANDED),
        A.RELEASE,
        "pushed",
        cause="pushed",
    )


def test_resume_row_4_release_after_a_normal_completed_push():
    check(resume(published=True), A.RELEASE, "pushed", cause="pushed")


def test_resume_row_4_holds_on_a_moved_head_or_unknown_target():
    check(resume(published=True, read=rd(head_sha=T)), A.HOLD, "head_mismatch")
    check(resume(published=True, target_sha=None), A.HOLD, "head_mismatch")
    check(resume(published=True, read=None), A.HOLD, "read_failed")


def test_resume_row_4_published_with_zero_counter_still_counts_one_edit():
    check(resume(published=True, applied_edits=0), A.RELEASE, "pushed", cause="pushed")


def test_resume_row_9_held_without_publication_is_a_noop():
    check(resume(), A.NOOP, "nothing_to_do")


def test_resume_row_5_not_landed_stays_held():
    check(resume(dangling_branch="not_landed"), A.NOOP, "held_through_redrive")


@pytest.mark.parametrize("phase", ["held", "release_pending", "released"])
def test_resume_row_6_ambiguous_tip_holds(phase):
    check(
        resume(guard=guard(phase), dangling_branch="ambiguous"),
        A.HOLD,
        "ambiguous_remote_tip",
    )


def test_resume_row_7_retry_release_when_owned():
    check(resume(guard=guard("release_pending")), A.RETRY_RELEASE, "release_pending")


def test_resume_row_8_ownership_unproven_when_live_draft():
    unowned = guard("release_pending", owned_draft=False)
    check(resume(guard=unowned, read=rd(is_draft=True)), A.HOLD, "ownership_unproven")
    check(resume(guard=unowned, read=rd(is_draft=False)), A.NOOP, "nothing_to_do")


# --- reconcile allows for earlier failed mutations (review finding on PR 428) --------


def _failed_then_retried_release_log(*, crash_after: str):
    """Cycle 1: engage; the release flips the PR but its check fails; the retry answers
    changed false. Cycle 2: engage, then a ready request that crashed before the call."""
    events = []

    def request(cycle, to, key, **fields):
        events.append(
            {
                "event_type": "draft_guard_requested",
                "cycle_id": cycle,
                "to": to,
                "idempotency_key": key,
                **fields,
            }
        )

    def settle(cycle, to, key, outcome, **fields):
        events.append(
            {
                "event_type": "draft_guard_settled",
                "cycle_id": cycle,
                "to": to,
                "idempotency_key": key,
                "outcome": outcome,
                **fields,
            }
        )

    request("fix-1", "draft", "k1", timeline_baseline=0, original_is_draft=False)
    settle("fix-1", "draft", "k1", "confirmed", changed=True)
    request("fix-1", "ready", "k2a1")
    settle("fix-1", "ready", "k2a1", "failed", changed=False)
    request("fix-1", "ready", "k2a2")
    settle("fix-1", "ready", "k2a2", "confirmed", changed=False)
    request("fix-2", "draft", "k3")
    settle("fix-2", "draft", "k3", "confirmed", changed=True)
    request("fix-2", "ready", "k4")
    if crash_after == "mutation":
        pass  # the ready call landed too: one more transition, never settled
    return events


def _resume_after(events, *, is_draft: bool, transitions: int):
    guard = mg.fold_draft_guard(events)
    read = mg.GuardRead(
        ok=True,
        state="OPEN",
        is_draft=is_draft,
        head_sha="a" * 40,
        transitions=transitions,
        complete=True,
    )
    return mg.resume_decision(
        mode=mg.GuardMode.DRAFT,
        ordinal=3,
        guard=guard,
        read=read,
        pending=mg.pending_requests(events),
        dangling_branch=None,
        published=True,
        target_sha="a" * 40,
    )


def test_reconcile_not_applied_allows_for_an_earlier_failed_mutation():
    events = _failed_then_retried_release_log(crash_after="request")
    guard = mg.fold_draft_guard(events)
    assert (guard["run_toggles"], guard["failed_mutations"]) == (2, 1)
    # Timeline: engage 1, the failed release really flipped 2, engage 3. Still a draft.
    decision = _resume_after(events, is_draft=True, transitions=3)
    assert (decision.action, decision.reason, decision.cause) == (
        mg.GuardAction.RECONCILE,
        "not_applied",
        "not_applied",
    )


def test_reconcile_resume_reconciled_allows_for_an_earlier_failed_mutation():
    events = _failed_then_retried_release_log(crash_after="mutation")
    # The ready call landed before the crash: one more transition, and the PR is ready.
    decision = _resume_after(events, is_draft=False, transitions=4)
    assert (decision.reason, decision.cause) == (
        "resume_reconciled",
        "resume_reconciled",
    )


def test_reconcile_stays_exact_without_a_failed_mutation_and_beyond_the_allowance():
    events = _failed_then_retried_release_log(crash_after="request")
    # Without any failed mutation the old exact rule still applies.
    only_draft = [e for e in events if e["idempotency_key"] in ("k1", "k4")]
    assert mg.fold_draft_guard(only_draft)["failed_mutations"] == 0
    assert (
        _resume_after(only_draft, is_draft=True, transitions=1).reason == "not_applied"
    )
    assert _resume_after(only_draft, is_draft=True, transitions=2).reason == "ambiguous"
    # With one failed mutation the allowance is one: two extra transitions stay ambiguous.
    assert _resume_after(events, is_draft=True, transitions=4).reason == "ambiguous"
    # A live state that matches the request with no new transition is never reconciled.
    assert _resume_after(events, is_draft=False, transitions=2).reason == "ambiguous"
