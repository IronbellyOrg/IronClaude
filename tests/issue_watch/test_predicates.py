"""Tests for the pure predicates of the issue watcher, part A.

Part A covers ``approval_of`` (spec Section 3 "Approved by a human", threat
rows T2 and T3) and ``unchanged_since`` (threat row T4). Every input is a
hand-built frozen dataclass; there are no fakes.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from superclaude.cli.issue_watch.audit import REASONS
from superclaude.cli.issue_watch.predicates import (
    CommentEdit,
    DiscoveredIssue,
    EditEvidence,
    LabelEvent,
    MarkerEvidence,
    ProjectItem,
    approval_of,
    eligibility_order,
    format_utc,
    is_intended_owner,
    marker_in_window,
    parse_utc,
    project_check,
    unchanged_since,
    valid_issue_number,
    valid_operation_id,
)

T0 = datetime(2026, 11, 1, 12, 0, 0, tzinfo=timezone.utc)
TRIGGER = "sc:issue"
APPROVAL = "approved"
APPROVER_ID = 101
OUTSIDER_ID = 999
OWN_LOGIN = "watcher-bot"


def at(seconds: int) -> datetime:
    """Return ``T0`` plus ``seconds``."""
    return T0 + timedelta(seconds=seconds)


def event(
    event_id: int,
    kind: str,
    label: str | None,
    seconds: int,
    *,
    actor_id: int | None = APPROVER_ID,
    login: str | None = "alice",
    actor_type: str | None = "User",
) -> LabelEvent:
    """Build one ``LabelEvent`` at ``T0`` plus ``seconds``."""
    return LabelEvent(
        id=event_id,
        event=kind,
        label=label,
        actor_id=actor_id,
        actor_login=login,
        actor_type=actor_type,
        created_at=at(seconds),
    )


def trigger_on(event_id: int = 1, seconds: int = 10) -> LabelEvent:
    """The trigger ``labeled`` event."""
    return event(event_id, "labeled", TRIGGER, seconds, actor_id=7, login="owner")


def approval_on(event_id: int = 2, seconds: int = 60, **actor) -> LabelEvent:
    """An approval ``labeled`` event; ``actor`` overrides the actor fields."""
    return event(event_id, "labeled", APPROVAL, seconds, **actor)


def approval_off(event_id: int, seconds: int, **actor) -> LabelEvent:
    """An approval ``unlabeled`` event; ``actor`` overrides the actor fields."""
    return event(event_id, "unlabeled", APPROVAL, seconds, **actor)


def decide(events, *, labels_now=(TRIGGER, APPROVAL), store_created_at=T0):
    """Run ``approval_of`` with the shared labels and allow-list."""
    return approval_of(
        events,
        labels_now=labels_now,
        trigger_label=TRIGGER,
        approval_label=APPROVAL,
        approvers={APPROVER_ID},
        store_created_at=store_created_at,
    )


def assert_skipped(result, reason: str) -> None:
    """Assert a not-approved result with ``reason`` and no approval fields."""
    assert result.approved is False
    assert result.reason == reason
    assert result.approver_id is None
    assert result.approval_event_id is None
    assert result.approved_at is None


# --- approval_of: the passing case -------------------------------------------


def test_ac3_allow_listed_user_approves__fr005() -> None:
    """AC-3, FR-005: an allow-listed User after trigger and init passes."""
    approval = approval_on(event_id=42, seconds=60)
    result = decide([trigger_on(), approval])
    assert result.approved is True
    assert result.reason is None
    assert result.approver_id == APPROVER_ID
    assert result.approval_event_id == 42
    assert result.approved_at == approval.created_at == at(60)


# --- approval_of: not_approved rows ------------------------------------------


@pytest.mark.parametrize(
    ("actor", "labels_now"),
    [
        pytest.param(
            {"actor_id": OUTSIDER_ID, "login": "mallory"},
            (TRIGGER, APPROVAL),
            id="actor-id-not-on-allow-list",
        ),
        pytest.param(
            {"actor_type": "Bot", "login": "alice"},
            (TRIGGER, APPROVAL),
            id="actor-type-bot",
        ),
        pytest.param(
            {"login": "x[bot]"},
            (TRIGGER, APPROVAL),
            id="login-ends-bot-suffix",
        ),
        pytest.param(
            {},
            (TRIGGER,),
            id="approval-label-no-longer-on-issue",
        ),
    ],
)
def test_ac3_not_approved_rows__fr005(actor, labels_now) -> None:
    """AC-3, FR-005 (T2, T3): outsider, Bot, ``x[bot]`` and a removed label skip."""
    result = decide([trigger_on(), approval_on(**actor)], labels_now=labels_now)
    assert_skipped(result, "not_approved")


def test_ac3_outsider_relabel__fr005_fr006() -> None:
    """AC-3, FR-005, FR-006: approver labeled, outsider unlabeled and relabeled."""
    outsider = {"actor_id": OUTSIDER_ID, "login": "mallory"}
    events = [
        trigger_on(),
        approval_on(event_id=2, seconds=60),
        approval_off(3, 70, **outsider),
        approval_on(event_id=4, seconds=80, **outsider),
    ]
    assert_skipped(decide(events), "not_approved")


def test_ac3_unlabeled_after_approval_voids_it__fr005() -> None:
    """AC-3, FR-005 (T2): an ``unlabeled`` event after the approval skips."""
    events = [trigger_on(), approval_on(seconds=60), approval_off(3, 70)]
    assert_skipped(decide(events), "not_approved")


def test_ac3_unlabeled_before_relabel_still_approves__fr006() -> None:
    """AC-3, FR-006: an ``unlabeled`` event before the latest ``labeled`` is moot."""
    events = [
        trigger_on(),
        approval_on(event_id=2, seconds=50),
        approval_off(3, 60),
        approval_on(event_id=4, seconds=70),
    ]
    result = decide(events)
    assert result.approved is True
    assert result.approval_event_id == 4
    assert result.approved_at == at(70)


@pytest.mark.parametrize(
    "actor",
    [
        pytest.param({"login": None}, id="login-none"),
        pytest.param({"actor_type": None}, id="type-none"),
        pytest.param({"actor_id": None}, id="id-none"),
        pytest.param(
            {"actor_id": None, "login": None, "actor_type": None}, id="all-none"
        ),
        pytest.param({"actor_type": "user"}, id="type-wrong-case"),
        pytest.param({"actor_type": "Organization"}, id="type-organization"),
    ],
)
def test_ac3_approval_event_with_missing_actor_fields_is_not_approved__fr005(
    actor,
) -> None:
    """AC-3, FR-005 (T2, T3): absent actor evidence is never positive, never raises."""
    result = decide([trigger_on(), approval_on(**actor)])
    assert_skipped(result, "not_approved")


def test_ac3_bool_actor_id_is_not_an_allow_listed_id__fr005() -> None:
    """FR-005: ``True`` equals 1 in a set, but a bool is not an account id."""
    events = [trigger_on(), approval_on(actor_id=True)]  # type: ignore[arg-type]
    result = approval_of(
        events,
        labels_now=(TRIGGER, APPROVAL),
        trigger_label=TRIGGER,
        approval_label=APPROVAL,
        approvers={1},
        store_created_at=T0,
    )
    assert_skipped(result, "not_approved")


def test_ac3_no_approval_event_in_history__fr005() -> None:
    """AC-3, FR-005: a label on the issue with no ``labeled`` event is not approved."""
    assert_skipped(decide([trigger_on()]), "not_approved")


# --- approval_of: ordering reasons -------------------------------------------


def test_ac3_approval_before_trigger__fr005() -> None:
    """AC-3, FR-005: an approval older than the latest trigger event skips."""
    events = [approval_on(seconds=60), trigger_on(event_id=3, seconds=100)]
    assert_skipped(decide(events), "approval_before_trigger")


def test_ac3_approval_before_init__fr005() -> None:
    """AC-3, FR-005: an approval older than the store's ``created_at`` skips."""
    events = [trigger_on(), approval_on(seconds=60)]
    result = decide(events, store_created_at=at(90))
    assert_skipped(result, "approval_before_init")


def test_ac3_approval_exactly_at_store_creation_is_before_init__fr005() -> None:
    """Spec (d): the approval must be LATER than the store, so equal skips."""
    events = [trigger_on(), approval_on(seconds=60)]
    assert_skipped(decide(events, store_created_at=at(60)), "approval_before_init")
    just_before = decide(events, store_created_at=at(59))
    assert just_before.approved is True
    assert just_before.approved_at == at(60)


# --- approval_of: ties and the order key -------------------------------------


@pytest.mark.parametrize(
    "events",
    [
        pytest.param(
            [
                trigger_on(),
                approval_on(event_id=2, seconds=60),
                approval_off(3, 60),
            ],
            id="labeled-and-unlabeled-same-second",
        ),
        pytest.param(
            [
                trigger_on(event_id=1, seconds=60),
                approval_on(event_id=2, seconds=60),
            ],
            id="approval-and-trigger-labeled-same-second",
        ),
    ],
)
def test_ac3_opposing_tie_is_events_incomplete__fr006(events) -> None:
    """AC-3, FR-006: an opposing tie in one second skips ``events_incomplete``."""
    assert_skipped(decide(events), "events_incomplete")


def test_ac3_missing_trigger_event_is_events_incomplete__fr006() -> None:
    """AC-3, FR-006: no trigger ``labeled`` event means incomplete history."""
    assert_skipped(decide([approval_on()]), "events_incomplete")


def test_ac3_order_key_is_created_at_then_id__fr006() -> None:
    """AC-3, FR-006: input order is ignored; ``(created_at, id)`` picks the latest."""
    events = [approval_on(event_id=2, seconds=60), trigger_on(event_id=1, seconds=10)]
    assert decide(events).approved is True
    outsider = {"actor_id": OUTSIDER_ID, "login": "mallory"}
    # Same second, same label, so the higher event id is the latest one.
    outsider_last = [
        trigger_on(),
        approval_on(event_id=6, seconds=60, **outsider),
        approval_on(event_id=5, seconds=60),
    ]
    assert_skipped(decide(outsider_last), "not_approved")
    approver_last = [
        trigger_on(),
        approval_on(event_id=6, seconds=60),
        approval_on(event_id=5, seconds=60, **outsider),
    ]
    result = decide(approver_last)
    assert result.approved is True
    assert result.approval_event_id == 6


# --- unchanged_since ----------------------------------------------------------

APPROVED_AT = at(1000)


def comment(
    database_id: int,
    author: str | None,
    created: int,
    edited: int | None = None,
) -> CommentEdit:
    """Build a ``CommentEdit`` with times at ``T0`` plus the given seconds."""
    return CommentEdit(
        database_id=database_id,
        author_login=author,
        created_at=at(created),
        last_edited_at=None if edited is None else at(edited),
    )


def edits(
    *comments: CommentEdit, body_edited: int | None = None, body_created: int = 0
) -> EditEvidence:
    """Build ``EditEvidence`` for an issue created at ``T0`` plus ``body_created``."""
    return EditEvidence(
        issue_created_at=at(body_created),
        issue_last_edited_at=None if body_edited is None else at(body_edited),
        comments=tuple(comments),
    )


def renamed(seconds: int) -> LabelEvent:
    """A ``renamed`` event; it carries no label."""
    return event(77, "renamed", None, seconds)


def check(evidence: EditEvidence, events=()) -> str | None:
    """Run ``unchanged_since`` for ``APPROVED_AT`` and ``OWN_LOGIN``."""
    return unchanged_since(APPROVED_AT, evidence, events, own_login=OWN_LOGIN)


@pytest.mark.parametrize(
    ("evidence", "events"),
    [
        pytest.param(edits(body_edited=1001), (), id="body-edited-1s-after"),
        pytest.param(
            edits(comment(1, "alice", created=1001)),
            (),
            id="non-own-comment-created-after",
        ),
        pytest.param(
            edits(comment(1, "alice", created=900, edited=1500)),
            (),
            id="non-own-comment-edited-after",
        ),
        pytest.param(edits(), (renamed(1200),), id="renamed-event-after"),
    ],
)
def test_ac3_edit_after_approval_skips__fr005(evidence, events) -> None:
    """AC-3, FR-005 (T4): a later edit, comment or rename skips the issue."""
    assert check(evidence, events) == "edited_after_approval"


@pytest.mark.parametrize(
    ("evidence", "events"),
    [
        pytest.param(edits(body_edited=1000), (), id="body-edited-exactly-at"),
        pytest.param(
            edits(comment(1, "alice", created=1000)),
            (),
            id="non-own-comment-created-exactly-at",
        ),
        pytest.param(
            edits(comment(1, "alice", created=900, edited=1000)),
            (),
            id="non-own-comment-edited-exactly-at",
        ),
        pytest.param(edits(), (renamed(1000),), id="renamed-event-exactly-at"),
    ],
)
def test_ac3_equal_timestamp_counts_as_changed__fr005(evidence, events) -> None:
    """AC-3, FR-005: an exactly equal timestamp is treated as changed."""
    assert check(evidence, events) == "edited_after_approval"


@pytest.mark.parametrize(
    "other",
    [
        pytest.param(("labeled", APPROVAL, 1000), id="labeled-exactly-at-approval"),
        pytest.param(("labeled", TRIGGER, 1500), id="labeled-after-approval"),
        pytest.param(("unlabeled", APPROVAL, 1200), id="unlabeled-after-approval"),
        pytest.param(("assigned", None, 1300), id="assigned-after-approval"),
        pytest.param(("milestoned", None, 1400), id="milestoned-after-approval"),
    ],
)
def test_ac3_only_renamed_events_count_as_changes__fr005(other) -> None:
    """FR-005 (T4): the approval's own ``labeled`` event (created_at == approved_at)
    is always in the history and must not read as an edit; only ``renamed`` does."""
    kind, label, seconds = other
    later = event(5, kind, label, seconds)
    assert check(edits(), (later,)) is None
    assert check(edits(), (later, renamed(1200))) == "edited_after_approval"


def test_ac3_own_login_comment_edit_is_ignored__fr005() -> None:
    """AC-3, FR-005: a comment by the own login edited after approval is ignored."""
    evidence = edits(comment(1, OWN_LOGIN, created=900, edited=1500))
    assert check(evidence) is None


def test_ac3_everything_strictly_earlier_passes__fr005() -> None:
    """AC-3, FR-005: body, comments and renames all before approval pass."""
    evidence = edits(
        comment(1, "alice", created=100, edited=999),
        comment(2, OWN_LOGIN, created=500),
        body_created=0,
        body_edited=999,
    )
    assert check(evidence, (renamed(999),)) is None


# --- Part B: is_intended_owner (spec Section 3 "Intended owner") -------------


@pytest.mark.parametrize(
    ("assignees", "expected"),
    [
        pytest.param({"other"}, (False, "assigned_other"), id="other-only"),
        pytest.param(set(), (False, "unassigned"), id="empty"),
        pytest.param(
            {OWN_LOGIN, "other"}, (False, "assigned_other"), id="own-and-other"
        ),
        pytest.param({OWN_LOGIN}, (True, None), id="own-only"),
    ],
)
def test_fr003_intended_owner_is_exactly_own_login(assignees, expected) -> None:
    """FR-003, FR-008, AC-4: only the set {own login} is the intended owner."""
    assert is_intended_owner(assignees, OWN_LOGIN) == expected


# --- project_check -----------------------------------------------------------

PROJECT_ID = "PVT_project"


def item(
    *,
    project_id: str = PROJECT_ID,
    archived: bool = False,
    status: str | None = "Backlog",
) -> ProjectItem:
    """Build a ``ProjectItem`` that is live, in ``PROJECT_ID`` and in Backlog."""
    return ProjectItem(is_archived=archived, project_id=project_id, status_name=status)


def test_fr007_one_live_backlog_item_passes() -> None:
    """FR-007: exactly one live item in the project at Backlog passes."""
    assert project_check([item()], PROJECT_ID) is None


@pytest.mark.parametrize(
    "items",
    [
        pytest.param([item(project_id="PVT_other")], id="wrong-project"),
        pytest.param([item(), item()], id="two-items"),
        pytest.param([item(archived=True)], id="archived-item"),
        pytest.param([item(status="In progress")], id="status-in-progress"),
        pytest.param([item(status="Backlog ")], id="status-near-miss"),
        pytest.param([item(status=None)], id="status-missing"),
        pytest.param([], id="no-items"),
    ],
)
def test_fr007_project_mismatch_rows(items) -> None:
    """FR-007, AC-4: any other project item shape skips ``project_mismatch``."""
    assert project_check(items, PROJECT_ID) == "project_mismatch"


def test_fr007_archived_item_does_not_count_toward_the_one() -> None:
    """FR-007: an archived duplicate is ignored, so one live item still passes."""
    assert project_check([item(archived=True), item()], PROJECT_ID) is None


# --- marker_in_window (DF-16, spec Section 3 "Claimed") ----------------------

PENDING_AT = at(5000)


def marker(
    *,
    login: str = OWN_LOGIN,
    created: int = 6000,
    updated: int | None = None,
    has_marker: bool = True,
) -> MarkerEvidence:
    """Build a ``MarkerEvidence``; ``updated`` defaults to ``created``."""
    return MarkerEvidence(
        id=1,
        login=login,
        created_at=at(created),
        updated_at=at(created if updated is None else updated),
        marker=has_marker,
    )


def in_window(
    evidence: MarkerEvidence,
    *,
    pending_at: datetime | None = PENDING_AT,
    approved_at: datetime | None = APPROVED_AT,
) -> bool:
    """Run ``marker_in_window`` for ``OWN_LOGIN``."""
    return marker_in_window(
        evidence, own_login=OWN_LOGIN, pending_at=pending_at, approved_at=approved_at
    )


def test_fr009_marker_exactly_at_skew_floor_counts() -> None:
    """FR-009: a marker at exactly ``pending_at - 300 s`` counts."""
    assert in_window(marker(created=5000 - 300)) is True


def test_fr009_marker_one_second_before_skew_floor_does_not_count() -> None:
    """FR-009: a marker at ``pending_at - 301 s`` does not count."""
    assert in_window(marker(created=5000 - 301)) is False


def test_fr009_pending_at_wins_over_approval_floor() -> None:
    """FR-009: with ``pending_at`` set, a marker before approval can still count."""
    evidence = marker(created=400)
    assert evidence.created_at < APPROVED_AT
    assert in_window(evidence, pending_at=at(500)) is True
    assert in_window(evidence, pending_at=None) is False


def test_fr009_without_pending_at_marker_must_be_strictly_after_approval() -> None:
    """FR-009: with no ``pending_at`` the floor is strictly after ``approved_at``."""
    assert in_window(marker(created=1001), pending_at=None) is True
    assert in_window(marker(created=1000), pending_at=None) is False
    assert in_window(marker(created=999), pending_at=None) is False


def test_fr009_not_own_login_marker_does_not_count() -> None:
    """FR-009: a marker comment by another login never counts."""
    assert in_window(marker(login="mallory")) is False


def test_fr009_comment_without_marker_does_not_count() -> None:
    """FR-009: an own-login comment that lacks the marker does not count."""
    assert in_window(marker(has_marker=False)) is False


def test_fr009_df16_edited_old_comment_counts() -> None:
    """FR-009, DF-16: old ``created_at`` with a new ``updated_at`` counts."""
    old = marker(created=100, updated=6000)
    assert in_window(old) is True
    assert in_window(marker(created=100, updated=100)) is False


def test_fr009_no_pending_at_and_no_approval_never_counts() -> None:
    """FR-009: with neither floor known the marker cannot count."""
    assert in_window(marker(), pending_at=None, approved_at=None) is False


# --- eligibility_order -------------------------------------------------------


def discovered(number: int) -> DiscoveredIssue:
    """Build a ``DiscoveredIssue`` that only needs its number."""
    return DiscoveredIssue(number=number, labels=(), assignees=(), state="OPEN")


def test_fr023_new_issue_first_then_oldest_examined() -> None:
    """FR-023: never-examined issue 9 leads; examined 7 (T1) precedes 8 (T2)."""
    considered = {7: at(100), 8: at(200)}
    order = eligibility_order([discovered(8), discovered(9), discovered(7)], considered)
    assert order == [9, 7, 8]


def test_fr023_ties_break_by_number_and_new_issues_by_number() -> None:
    """FR-023: equal times sort by number; several new issues sort by number."""
    considered = {12: at(100), 11: at(100)}
    discovered_all = [discovered(n) for n in (12, 20, 11, 15)]
    assert eligibility_order(discovered_all, considered) == [15, 20, 11, 12]


def test_fr023_considered_issue_not_discovered_is_dropped() -> None:
    """FR-023: only discovered issues are ordered."""
    assert eligibility_order([discovered(3)], {99: at(1)}) == [3]


# --- parse_utc, format_utc, valid_issue_number (DF-35) -----------------------


def test_df35_parse_utc_accepts_trailing_z() -> None:
    """DF-35: ``YYYY-MM-DDTHH:MM:SSZ`` parses to an aware UTC datetime."""
    parsed = parse_utc("2026-11-01T12:00:00Z")
    assert parsed == T0
    assert parsed.utcoffset() == timedelta(0)


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("2026-11-01T12:00:00", id="missing-z"),
        pytest.param("2026-11-01T12:00:00+00:00", id="numeric-offset"),
        pytest.param("2026-11-01 12:00:00Z", id="space-separator"),
        pytest.param("", id="empty"),
        pytest.param("2026-1-5T1:2:3Z", id="unpadded-fields"),
        pytest.param("2026-11-01T12:00:00z", id="lower-case-z"),
        pytest.param("２０２６-11-01T12:00:00Z", id="non-ascii-digits"),
        pytest.param("2026-11-01T12:00:00Z\n", id="trailing-newline"),
        pytest.param(" 2026-11-01T12:00:00Z", id="leading-space"),
        pytest.param("2026-11-01T12:00:00.5Z", id="fractional-seconds"),
        pytest.param("2026-13-01T12:00:00Z", id="month-13"),
        pytest.param("2026-11-01T24:00:00Z", id="hour-24"),
    ],
)
def test_df35_parse_utc_rejects_other_shapes(text) -> None:
    """DF-35: a missing ``Z`` or any other shape raises ``ValueError``."""
    with pytest.raises(ValueError):
        parse_utc(text)


def test_df35_parse_utc_rejects_non_string() -> None:
    """DF-35: a non-string raises ``ValueError``, not ``TypeError``."""
    with pytest.raises(ValueError):
        parse_utc(None)  # type: ignore[arg-type]


def test_df35_format_utc_round_trips() -> None:
    """DF-35: ``format_utc`` and ``parse_utc`` are inverses on whole seconds."""
    assert format_utc(T0) == "2026-11-01T12:00:00Z"
    assert parse_utc(format_utc(T0)) == T0
    assert format_utc(parse_utc("2026-02-03T04:05:06Z")) == "2026-02-03T04:05:06Z"


def test_df35_format_utc_converts_to_utc_and_rejects_naive() -> None:
    """DF-35: an aware non-UTC time is converted; a naive time raises."""
    plus_two = timezone(timedelta(hours=2))
    assert format_utc(datetime(2026, 11, 1, 14, 0, 0, tzinfo=plus_two)) == (
        "2026-11-01T12:00:00Z"
    )
    with pytest.raises(ValueError):
        format_utc(datetime(2026, 11, 1, 12, 0, 0))


@pytest.mark.parametrize("value", [1, 7, 10**9 - 1])
def test_valid_issue_number_accepts_range(value) -> None:
    """an int in 1..999999999 is a valid issue number."""
    assert valid_issue_number(value) is True


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(True, id="bool-true"),
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
        pytest.param(10**9, id="too-large"),
        pytest.param(9.0, id="float"),
        pytest.param("9", id="string"),
        pytest.param(None, id="none"),
    ],
)
def test_valid_issue_number_rejects(value) -> None:
    """bool, out-of-range, float and string values are rejected."""
    assert valid_issue_number(value) is False


@pytest.mark.parametrize("value", ["a", "op-1", "A.b_c:d-9", "x" * 128])
def test_valid_operation_id_accepts_the_pattern(value) -> None:
    """1 to 128 characters of ``A-Za-z0-9._:-`` are a safe operation id (design 9.2)."""
    assert valid_operation_id(value) is True


@pytest.mark.parametrize(
    "value",
    [
        "",
        "x" * 129,
        "a;b",
        "$(id)",
        "a b",
        "a/b",
        "op\n1",
        "op-1\n",
        "x; rm -rf ~\n\x1b[31m",
        "ｏｐ",
        None,
        5,
        b"op-1",
        ["op-1"],
        True,
    ],
)
def test_valid_operation_id_rejects(value) -> None:
    """Shell text, control characters, bad length and non-str values are rejected."""
    assert valid_operation_id(value) is False


# --- reason strings ----------------------------------------------------------


def test_every_predicate_reason_is_in_the_audit_table() -> None:
    """Every reason string the predicates can return is a member of ``REASONS``."""
    returned = {
        "not_approved",
        "approval_before_trigger",
        "approval_before_init",
        "events_incomplete",
        "edited_after_approval",
        "project_mismatch",
        "unassigned",
        "assigned_other",
    }
    assert returned <= REASONS
    # The same strings, as the functions really return them.
    observed = {
        decide([trigger_on(), approval_on(actor_id=OUTSIDER_ID)]).reason,
        decide([approval_on(seconds=60), trigger_on(event_id=3, seconds=100)]).reason,
        decide([trigger_on(), approval_on(seconds=60)], store_created_at=at(90)).reason,
        decide([approval_on()]).reason,
        check(edits(body_edited=1001)),
        project_check([], PROJECT_ID),
        is_intended_owner(set(), OWN_LOGIN)[1],
        is_intended_owner({"other"}, OWN_LOGIN)[1],
    }
    assert observed == returned
