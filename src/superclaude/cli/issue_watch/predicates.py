"""Pure predicates for the issue watcher (spec Section 3 definitions).

This module performs no I/O and reads no clock: every time is a parameter.
It imports nothing from ``superclaude`` so every other module may import it.
"""

from __future__ import annotations

import re
from collections.abc import Collection, Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

CLAIM_MARKER = "<!-- sc:issue:claim -->"
"""Claim-comment marker; ``github.MARKER_JQ`` is built from this constant."""

SKEW_TOLERANCE_S = 300
"""Seconds a claim marker may precede ``pending_at`` and still count."""

MAX_ISSUE_NUMBER = 999_999_999
"""Largest issue number the watcher accepts."""

_UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
_UTC_SHAPE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")


def parse_utc(text: str) -> datetime:
    """Parse a GitHub ``YYYY-MM-DDTHH:MM:SSZ`` time into an aware UTC datetime.

    Raises ``ValueError`` for any other input (DF-35: no ``fromisoformat``). The
    shape is checked first with ASCII digits and a capital ``Z`` only, because
    ``strptime`` alone accepts unpadded fields, a lower-case ``z`` and non-ASCII
    digits.
    """
    if not isinstance(text, str):
        raise ValueError("time value is not a string")
    if _UTC_SHAPE.fullmatch(text) is None:
        raise ValueError("time value is not YYYY-MM-DDTHH:MM:SSZ")
    return datetime.strptime(text, _UTC_FORMAT).replace(tzinfo=timezone.utc)


def format_utc(value: datetime) -> str:
    """Format an aware datetime as ``YYYY-MM-DDTHH:MM:SSZ`` in UTC.

    Raises ``ValueError`` for a naive datetime, whose zone would be guessed.
    """
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("naive datetime")
    return value.astimezone(timezone.utc).strftime(_UTC_FORMAT)


def valid_issue_number(value: object) -> bool:
    """Return True for an ``int`` (never ``bool``) in 1..``MAX_ISSUE_NUMBER``."""
    return type(value) is int and 1 <= value <= MAX_ISSUE_NUMBER


OPERATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
"""Operation ids that may be stored and printed in a retry command (design 9.2).

``launch.OPERATION_ID_PATTERN`` is a second copy, because ``launch`` may import
only ``runner`` (design 5.3); a test pins the two patterns equal.
"""


def valid_operation_id(value: object) -> bool:
    """Return True for a ``str`` that fully matches ``OPERATION_ID_PATTERN``."""
    return isinstance(value, str) and OPERATION_ID_PATTERN.fullmatch(value) is not None


@dataclass(frozen=True)
class Login:
    """Own login, account id and the reply's ``Date`` header (G1)."""

    login: str
    account_id: int
    server_date: datetime | None


@dataclass(frozen=True)
class DiscoveredIssue:
    """One issue from the discovery read (G2)."""

    number: int
    labels: tuple[str, ...]
    assignees: tuple[str, ...]
    state: str


@dataclass(frozen=True)
class LabelEvent:
    """One issue event; ``label`` is None for events without a label."""

    id: int
    event: str
    label: str | None
    actor_id: int | None
    actor_login: str | None
    actor_type: str | None
    created_at: datetime


@dataclass(frozen=True)
class IssueSnapshot:
    """Issue state, labels and assignees from the pre-launch re-read."""

    number: int
    state: str
    labels: tuple[str, ...]
    assignees: tuple[str, ...]


@dataclass(frozen=True)
class ProjectItem:
    """One ``projectItems`` entry of an issue (G6)."""

    is_archived: bool
    project_id: str
    status_name: str | None


@dataclass(frozen=True)
class MarkerEvidence:
    """One comment's author, times and whether it holds ``CLAIM_MARKER``."""

    id: int
    login: str
    created_at: datetime
    updated_at: datetime
    marker: bool


@dataclass(frozen=True)
class CommentEdit:
    """Creation and last-edit times of one comment (no text)."""

    database_id: int
    author_login: str | None
    created_at: datetime
    last_edited_at: datetime | None


@dataclass(frozen=True)
class EditEvidence:
    """Issue body and comment edit times (G5)."""

    issue_created_at: datetime
    issue_last_edited_at: datetime | None
    comments: tuple[CommentEdit, ...]


@dataclass(frozen=True)
class ApprovalResult:
    """Outcome of ``approval_of``; ``reason`` is set only when not approved."""

    approved: bool
    reason: str | None
    approver_id: int | None
    approval_event_id: int | None
    approved_at: datetime | None


def is_intended_owner(
    assignees: Iterable[str], own_login: str
) -> tuple[bool, str | None]:
    """Return ``(True, None)`` only when the assignee set is exactly {own login}.

    Otherwise the skip reason is ``unassigned`` (empty set) or ``assigned_other``.
    """
    names = set(assignees)
    if names == {own_login}:
        return True, None
    if not names:
        return False, "unassigned"
    return False, "assigned_other"


def _not_approved(reason: str) -> ApprovalResult:
    return ApprovalResult(False, reason, None, None, None)


def _second(value: datetime) -> datetime:
    return value.replace(microsecond=0)


def approval_of(
    events: Iterable[LabelEvent],
    *,
    labels_now: Collection[str],
    trigger_label: str,
    approval_label: str,
    approvers: Collection[int],
    store_created_at: datetime,
) -> ApprovalResult:
    """Apply spec Section 3 "Approved by a human" checks (a) to (e).

    ``events`` must be the complete event history; absent evidence never
    counts as positive.
    """
    ordered = sorted(events, key=lambda e: (e.created_at, e.id))
    appr_on = [e for e in ordered if e.event == "labeled" and e.label == approval_label]
    appr_off = [
        e for e in ordered if e.event == "unlabeled" and e.label == approval_label
    ]
    trig_on = [e for e in ordered if e.event == "labeled" and e.label == trigger_label]
    on_seconds = {_second(e.created_at) for e in appr_on}
    if on_seconds & {_second(e.created_at) for e in appr_off} or on_seconds & {
        _second(e.created_at) for e in trig_on
    }:
        return _not_approved("events_incomplete")
    if approval_label not in labels_now or not appr_on:
        return _not_approved("not_approved")
    approval = appr_on[-1]
    key = (approval.created_at, approval.id)
    if any((e.created_at, e.id) > key for e in appr_off):
        return _not_approved("not_approved")
    if (
        approval.actor_type != "User"
        or approval.actor_login is None
        or approval.actor_login.endswith("[bot]")
        or type(approval.actor_id) is not int
        or approval.actor_id not in approvers
    ):
        return _not_approved("not_approved")
    # OQ-38: no trigger `labeled` event means check (c) cannot pass; this also
    # covers an absent trigger label (absent evidence never counts as positive).
    if not trig_on:
        return _not_approved("events_incomplete")
    if approval.created_at <= trig_on[-1].created_at:
        return _not_approved("approval_before_trigger")
    if approval.created_at <= store_created_at:
        return _not_approved("approval_before_init")
    return ApprovalResult(
        True, None, approval.actor_id, approval.id, approval.created_at
    )


def unchanged_since(
    approved_at: datetime,
    edits: EditEvidence,
    events: Iterable[LabelEvent],
    *,
    own_login: str,
) -> str | None:
    """Return ``edited_after_approval`` unless everything predates ``approved_at``.

    Checks the issue body, every comment not authored by ``own_login`` and
    every ``renamed`` event; an equal timestamp counts as changed (OQ-37).
    """
    times: list[datetime | None] = [
        edits.issue_created_at,
        edits.issue_last_edited_at,
    ]
    for comment in edits.comments:
        if comment.author_login != own_login:
            times += [comment.created_at, comment.last_edited_at]
    times += [e.created_at for e in events if e.event == "renamed"]
    if any(t is not None and t >= approved_at for t in times):
        return "edited_after_approval"
    return None


def project_check(items: Iterable[ProjectItem], project_id: str) -> str | None:
    """Return ``project_mismatch`` unless exactly one live item is in Backlog.

    The item must be non-archived, in ``project_id`` and have Status
    ``Backlog``.
    """
    matching = [i for i in items if not i.is_archived and i.project_id == project_id]
    if len(matching) == 1 and matching[0].status_name == "Backlog":
        return None
    return "project_mismatch"


def marker_time(marker: MarkerEvidence) -> datetime:
    """Return the later of the marker comment's creation and update (DF-16)."""
    return max(marker.created_at, marker.updated_at)


def marker_in_window(
    marker: MarkerEvidence,
    *,
    own_login: str,
    pending_at: datetime | None,
    approved_at: datetime | None,
) -> bool:
    """Return True for an own-login claim marker inside the claim window.

    With ``pending_at`` set the marker counts at or after ``pending_at`` minus
    ``SKEW_TOLERANCE_S``; otherwise only strictly after ``approved_at``.
    """
    if not marker.marker or marker.login != own_login:
        return False
    when = marker_time(marker)
    if pending_at is not None:
        return when >= pending_at - timedelta(seconds=SKEW_TOLERANCE_S)
    return approved_at is not None and when > approved_at


def eligibility_order(
    discovered: Iterable[DiscoveredIssue], considered: Mapping[int, datetime]
) -> list[int]:
    """Order issue numbers: never-examined first by number, then oldest examined.

    Examined issues sort by ``considered[n]`` with ties by number; the
    ``max_candidates`` cap is applied by the cycle.
    """
    numbers = [issue.number for issue in discovered]
    fresh = sorted(n for n in numbers if n not in considered)
    seen = sorted(
        (n for n in numbers if n in considered), key=lambda n: (considered[n], n)
    )
    return fresh + seen
