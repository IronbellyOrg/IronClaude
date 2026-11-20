"""Stage predicates for the plan stage: the approval label and the ``approved`` comment.

Pure functions over the evidence types of ``issue_watch.predicates``
(``LabelEvent``, ``CommentEdit``, ``EditEvidence``) and one projected-comment type
defined here (``CommentFact``, filled by the jq projection of ``reads.py``).

The watcher's ``approval_of`` and ``unchanged_since`` are not reused: ``unchanged_since``
skips comments written by the host login (the coordinator posts the plan reply as that
login, so an edited plan reply would go unseen), and ``approval_of`` orders an approval
against the trigger label and the store creation time, not against a plan reply.

Rules, written once:

* The plan reply is the latest comment by the host login that carries the hidden marker
  ``<!-- sc:stage:plan id=<record-id> plan=<64 hex> -->``. It must be unedited since it
  was posted, and the plan files must still hash to the marker's value.
* Label channel: applied after the plan reply, still applied, the actor is a ``User`` (not
  a bot) and is the assignee (by login) or listed in the approvers file (by id).
* Comment channel: the whole comment is ``approved`` or the long form; its author is the
  assignee or a listed approver and a ``User``; every other commenter is ignored (the
  repository is public); created after the latest plan reply; never edited; a long form
  carries the latest plan reply's record id and hash; the short form binds by position.
* Both channels map to the same key (issue, stage, plan hash).
* Revocation: removing the approval label after it was applied is a revocation signal;
  deleting or editing an approving comment is not; a Status move back alone is reported.
* A Status move after the plan reply is the visible sign of approval: reported as
  ``status_seen``, never required, never part of the key.
* What the code cannot check is carried as a flag, not hidden: the actor equals the host
  login (an agent on this host could have posted it, Decision 4), and the assignee is the
  host login (the case after a claim).

Equal timestamps never count as "after" (fail closed): GitHub times have one-second
granularity.
"""

from __future__ import annotations

from collections.abc import Collection, Iterable
from dataclasses import dataclass
from datetime import datetime

from superclaude.cli.issue_watch.predicates import CommentEdit, EditEvidence, LabelEvent

STATUS_EVENT = "project_v2_item_status_changed"
STAGE = "plan"


@dataclass(frozen=True)
class PlanMarker:
    """The values of a ``<!-- sc:stage:plan id=... plan=... -->`` marker."""

    record_id: str
    plan_hash: str


@dataclass(frozen=True)
class CommentFact:
    """One comment reduced to booleans and ids by the jq projection (no text)."""

    id: int
    author_login: str | None
    author_id: int | None
    author_type: str | None
    created_at: datetime
    approval_form: str | None  # "short", "long" or None: the whole body matches a form
    approval_record_id: str | None  # captured from a long form
    approval_hash: str | None  # captured from a long form
    plan_marker: PlanMarker | None


@dataclass(frozen=True)
class ChannelResult:
    accepted: bool
    reason: str  # a closed word; "ok" when accepted
    evidence_id: int | None = None  # label event id or comment id
    actor_id: int | None = None
    actor_is_host_login: bool = False


@dataclass(frozen=True)
class StageStatus:
    state: str  # no-plan-reply | plan-reply-invalid | plan-changed | awaiting-approval | approved | revoked
    plan_reason: str  # ok or the closed reason the plan reply is unusable
    plan_reply_id: int | None
    plan_hash: str | None
    record_id: str | None
    key: (
        tuple[int, str, str] | None
    )  # (issue, stage, plan hash); the same for both channels
    label: ChannelResult
    comment: ChannelResult
    approved: bool
    label_revoked: bool
    status_seen: bool
    assignee_is_host_login: bool


_NONE = ChannelResult(False, "no-plan-reply")


def _closed_plan(reason: str, plan_reply_id: int | None = None) -> StageStatus:
    return StageStatus(
        state="no-plan-reply" if reason == "no-plan-reply" else "plan-reply-invalid",
        plan_reason=reason,
        plan_reply_id=plan_reply_id,
        plan_hash=None,
        record_id=None,
        key=None,
        label=_NONE,
        comment=_NONE,
        approved=False,
        label_revoked=False,
        status_seen=False,
        assignee_is_host_login=False,
    )


def latest_plan_reply(
    comments: Iterable[CommentFact], host_login: str
) -> CommentFact | None:
    """The latest comment by the host login that carries the plan marker."""
    candidates = [
        c
        for c in comments
        if c.author_login == host_login and c.plan_marker is not None
    ]
    return max(candidates, key=lambda c: (c.created_at, c.id), default=None)


def _is_allowed_actor(
    login: str | None,
    account_id: int | None,
    assignees: Collection[str],
    approvers: Collection[int],
) -> bool:
    return (login is not None and login in assignees) or (
        account_id is not None and account_id in approvers
    )


def _edit_of(edits: EditEvidence, comment_id: int) -> CommentEdit | None:
    return next((e for e in edits.comments if e.database_id == comment_id), None)


def _label_channel(
    reply: CommentFact,
    events: Iterable[LabelEvent],
    approval_label: str,
    assignees: Collection[str],
    approvers: Collection[int],
    host_login: str,
) -> tuple[ChannelResult, bool]:
    relevant = sorted(
        (
            e
            for e in events
            if e.label == approval_label and e.event in ("labeled", "unlabeled")
        ),
        key=lambda e: (e.created_at, e.id),
    )
    applied_after = [
        e for e in relevant if e.event == "labeled" and e.created_at > reply.created_at
    ]
    if not applied_after:
        reason = (
            "label-before-plan"
            if any(e.event == "labeled" for e in relevant)
            else "no-label"
        )
        return ChannelResult(False, reason), False
    latest = applied_after[-1]
    removed = any(
        e.event == "unlabeled" and (e.created_at, e.id) > (latest.created_at, latest.id)
        for e in relevant
    )
    if removed:
        return ChannelResult(False, "label-removed", latest.id, latest.actor_id), True
    if latest.actor_type != "User":
        return ChannelResult(False, "actor-not-user", latest.id, latest.actor_id), False
    if not _is_allowed_actor(latest.actor_login, latest.actor_id, assignees, approvers):
        return ChannelResult(
            False, "actor-not-allowed", latest.id, latest.actor_id
        ), False
    return (
        ChannelResult(
            True, "ok", latest.id, latest.actor_id, latest.actor_login == host_login
        ),
        False,
    )


def _comment_channel(
    reply: CommentFact,
    comments: Iterable[CommentFact],
    edits: EditEvidence,
    assignees: Collection[str],
    approvers: Collection[int],
    host_login: str,
) -> ChannelResult:
    assert reply.plan_marker is not None
    first_reason: str | None = (
        None  # why the latest candidate failed, when none is accepted
    )
    for comment in sorted(comments, key=lambda c: (c.created_at, c.id), reverse=True):
        if comment.approval_form is None:
            continue
        # Every other commenter is ignored: the repository is public.
        if comment.author_type != "User" or not _is_allowed_actor(
            comment.author_login, comment.author_id, assignees, approvers
        ):
            first_reason = first_reason or "author-not-allowed"
            continue
        failure = _comment_failure(comment, reply, edits)
        if failure is not None:
            first_reason = first_reason or failure
            continue
        return ChannelResult(
            True,
            "ok",
            comment.id,
            comment.author_id,
            comment.author_login == host_login,
        )
    return ChannelResult(False, first_reason or "no-comment")


def _comment_failure(
    comment: CommentFact, reply: CommentFact, edits: EditEvidence
) -> str | None:
    """The closed reason an otherwise allowed approving comment does not count, or None."""
    assert reply.plan_marker is not None
    if comment.created_at <= reply.created_at:
        return "comment-before-plan"
    edit = _edit_of(edits, comment.id)
    if edit is None:
        return "edit-unknown"
    if edit.last_edited_at is not None:
        return "comment-edited"
    if comment.approval_form == "long" and (
        comment.approval_hash != reply.plan_marker.plan_hash
        or comment.approval_record_id != reply.plan_marker.record_id
    ):
        return "hash-mismatch"
    return None


def evaluate(
    issue: int,
    comments: Iterable[CommentFact],
    events: Iterable[LabelEvent],
    edits: EditEvidence,
    *,
    plan_hash_now: str | None,
    host_login: str,
    assignees: Collection[str],
    approvers: Collection[int],
    approval_label: str,
) -> StageStatus:
    """Apply the rules to one issue's evidence and return a closed result."""
    comments = tuple(comments)
    events = tuple(events)
    reply = latest_plan_reply(comments, host_login)
    if reply is None or reply.plan_marker is None:
        return _closed_plan("no-plan-reply")
    edit = _edit_of(edits, reply.id)
    if edit is None:
        return _closed_plan("plan-reply-edit-unknown", reply.id)
    if edit.last_edited_at is not None:
        return _closed_plan("plan-reply-edited", reply.id)
    marker = reply.plan_marker
    changed = plan_hash_now is None or plan_hash_now != marker.plan_hash
    label, revoked = _label_channel(
        reply, events, approval_label, assignees, approvers, host_login
    )
    comment = _comment_channel(reply, comments, edits, assignees, approvers, host_login)
    status_seen = any(
        e.event == STATUS_EVENT and e.created_at > reply.created_at for e in events
    )
    approved = (label.accepted or comment.accepted) and not changed
    if changed:
        state = "plan-changed"
    elif approved:
        state = "approved"
    elif revoked:
        state = "revoked"
    else:
        state = "awaiting-approval"
    return StageStatus(
        state=state,
        plan_reason="plan-changed" if changed else "ok",
        plan_reply_id=reply.id,
        plan_hash=marker.plan_hash,
        record_id=marker.record_id,
        key=(issue, STAGE, marker.plan_hash),
        label=label,
        comment=comment,
        approved=approved,
        label_revoked=revoked,
        status_seen=status_seen,
        assignee_is_host_login=host_login in assignees,
    )
