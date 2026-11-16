"""Task 4: stage predicates for the approval label and the ``approved`` comment."""

from __future__ import annotations

import json
import re
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from superclaude.cli.issue_pipeline import approval_line
from superclaude.cli.issue_pipeline import stage_predicates as sp
from superclaude.cli.issue_watch.predicates import (
    CommentEdit,
    EditEvidence,
    LabelEvent,
    parse_utc,
)

RECORDED = Path(__file__).parent / "fixtures" / "recorded"
HOST = "host-login"
OWNER = "owner-login"
OWNER_ID = 111
APPROVER_ID = 222
LABEL = "plan-approved"
H_A = "a" * 64
H_B = "b" * 64
BASE = datetime(2026, 11, 16, 10, 0, 0, tzinfo=timezone.utc)


def at(minutes: int) -> datetime:
    return BASE + timedelta(minutes=minutes)


def rid(h: str, issue: int = 9) -> str:
    return approval_line.record_id(issue, h)


def plan_reply(cid: int, minutes: int, h: str = H_A) -> sp.CommentFact:
    return sp.CommentFact(cid, HOST, 1, "User", at(minutes), None, None, None, sp.PlanMarker(rid(h), h))


def approving(
    cid: int, minutes: int, text: str = "approved", *, login: str = OWNER, uid: int = OWNER_ID, kind: str = "User"
) -> sp.CommentFact:
    form, record, digest = approval_line.parse(text)
    return sp.CommentFact(cid, login, uid, kind, at(minutes), None if form == "none" else form, record, digest, None)


def label_event(eid: int, minutes: int, event: str = "labeled", *, login: str = OWNER, uid: int = OWNER_ID, kind: str = "User") -> LabelEvent:
    return LabelEvent(eid, event, LABEL, uid, login, kind, at(minutes))


def status_event(eid: int, minutes: int) -> LabelEvent:
    return LabelEvent(eid, sp.STATUS_EVENT, None, 5, "bot", "Bot", at(minutes))


def edits_for(*comments: sp.CommentFact, edited: dict[int, int] | None = None) -> EditEvidence:
    edited = edited or {}
    rows = tuple(
        CommentEdit(c.id, c.author_login, c.created_at, at(edited[c.id]) if c.id in edited else None) for c in comments
    )
    return EditEvidence(at(-60), None, rows)


def run(comments, events=(), *, edited=None, plan_hash_now=H_A, assignees=(OWNER,), approvers=frozenset()) -> sp.StageStatus:
    return sp.evaluate(
        9,
        comments,
        events,
        edits_for(*comments, edited=edited),
        plan_hash_now=plan_hash_now,
        host_login=HOST,
        assignees=assignees,
        approvers=approvers,
        approval_label=LABEL,
    )


# --- real recorded files ------------------------------------------------------


def _recorded(name: str):
    return json.loads((RECORDED / name).read_text())


def _facts_from_raw_comments(raw: list[dict]) -> list[sp.CommentFact]:
    marker = re.compile(r"<!-- sc:stage:plan id=(ap-[1-9][0-9]*-plan-[0-9a-f]{12}) plan=([0-9a-f]{64}) -->")
    facts = []
    for c in raw:
        form, record, digest = approval_line.parse(c["body"])
        found = marker.search(c["body"])
        facts.append(
            sp.CommentFact(
                c["id"],
                c["user"]["login"],
                c["user"]["id"],
                c["user"]["type"],
                parse_utc(c["created_at"]),
                None if form == "none" else form,
                record,
                digest,
                sp.PlanMarker(found.group(1), found.group(2)) if found else None,
            )
        )
    return facts


def _events_from_raw(raw: list[dict]) -> list[LabelEvent]:
    return [
        LabelEvent(
            e["id"],
            e["event"],
            (e.get("label") or {}).get("name"),
            (e.get("actor") or {}).get("id"),
            (e.get("actor") or {}).get("login"),
            (e.get("actor") or {}).get("type"),
            parse_utc(e["created_at"]),
        )
        for e in raw
    ]


def _edits_from_raw(raw: dict) -> EditEvidence:
    issue = raw["data"]["repository"]["issue"]
    nodes = issue["comments"]["nodes"]
    last = lambda v: parse_utc(v) if v else None  # noqa: E731
    return EditEvidence(
        parse_utc(issue["createdAt"]),
        last(issue["lastEditedAt"]),
        tuple(CommentEdit(n["databaseId"], (n["author"] or {}).get("login"), parse_utc(n["createdAt"]), last(n["lastEditedAt"])) for n in nodes),
    )


def test_recorded_files_load_and_a_plan_less_issue_has_no_plan_reply() -> None:
    comments = _facts_from_raw_comments(_recorded("comments-page1.json"))
    events = _events_from_raw(_recorded("events-page1.json"))
    edits = _edits_from_raw(_recorded("edits-page1.json"))
    assert comments and events and edits.comments  # real fields were found under the names used here
    status = sp.evaluate(
        452, comments, events, edits, plan_hash_now=None, host_login="ironbelly", assignees=("ironbelly",),
        approvers=frozenset(), approval_label=LABEL,
    )
    assert (status.state, status.approved, status.key) == ("no-plan-reply", False, None)
    assert {e.actor_type for e in events} == {"Bot", "User"}  # the Bot/User field name is the real one


def test_recorded_comments_join_the_recorded_edits_by_database_id() -> None:
    comments = _facts_from_raw_comments(_recorded("comments-page1.json"))
    edits = _edits_from_raw(_recorded("edits-page1.json"))
    assert {c.id for c in comments} == {e.database_id for e in edits.comments}


# --- rules, one test each ------------------------------------------------------


def test_no_plan_reply_yet() -> None:
    status = run([approving(1, 5)])
    assert (status.state, status.plan_reason, status.key) == ("no-plan-reply", "no-plan-reply", None)


def test_plan_reply_and_no_approval_is_awaiting() -> None:
    status = run([plan_reply(10, 0)])
    assert status.state == "awaiting-approval" and not status.approved
    assert status.key == (9, "plan", H_A) and status.record_id == rid(H_A)
    assert (status.label.reason, status.comment.reason) == ("no-label", "no-comment")


def test_the_plan_reply_is_the_latest_host_comment_with_the_marker() -> None:
    other = replace(plan_reply(11, 3), author_login="someone-else")  # not the host login: ignored
    status = run([plan_reply(10, 0), plan_reply(12, 2, H_B), other], plan_hash_now=H_B)
    assert status.plan_reply_id == 12 and status.plan_hash == H_B


def test_label_channel_accepts_after_the_plan_reply() -> None:
    status = run([plan_reply(10, 0)], [label_event(1, 2)])
    assert (status.state, status.label.accepted, status.label.reason) == ("approved", True, "ok")
    assert status.label.evidence_id == 1 and status.label.actor_id == OWNER_ID


def test_label_by_an_approver_id_is_accepted() -> None:
    event = label_event(1, 2, login="approver-login", uid=APPROVER_ID)
    status = run([plan_reply(10, 0)], [event], approvers=frozenset({APPROVER_ID}))
    assert status.label.accepted


def test_comment_channel_accepts_the_short_and_the_long_form() -> None:
    assert run([plan_reply(10, 0), approving(11, 2)]).comment.accepted
    long_text = f"approved {rid(H_A)} plan-sha256={H_A}"
    assert run([plan_reply(10, 0), approving(11, 2, long_text)]).comment.accepted


def test_label_and_comment_for_the_same_plan_give_the_same_key() -> None:
    by_label = run([plan_reply(10, 0)], [label_event(1, 2)])
    by_comment = run([plan_reply(10, 0), approving(11, 2)])
    both = run([plan_reply(10, 0), approving(11, 2)], [label_event(1, 3)])
    assert by_label.key == by_comment.key == both.key == (9, "plan", H_A)
    assert both.label.accepted and both.comment.accepted and both.state == "approved"


def test_an_approval_for_plan_version_a_is_ignored_once_plan_reply_b_exists() -> None:
    comments = [plan_reply(10, 0, H_A), approving(11, 2), plan_reply(12, 5, H_B)]
    status = run(comments, [label_event(1, 3)], plan_hash_now=H_B)
    assert status.plan_hash == H_B and status.key == (9, "plan", H_B)
    assert not status.label.accepted and status.label.reason == "label-before-plan"
    assert not status.comment.accepted and status.comment.reason == "comment-before-plan"
    assert status.state == "awaiting-approval"


# --- one negative per clause ---------------------------------------------------


def test_bot_author_is_ignored_on_both_channels() -> None:
    bot_comment = approving(11, 2, login=OWNER, kind="Bot")
    status = run([plan_reply(10, 0), bot_comment], [label_event(1, 2, kind="Bot")])
    assert not status.comment.accepted and status.comment.reason == "author-not-allowed"
    assert not status.label.accepted and status.label.reason == "actor-not-user"


def test_a_commenter_who_is_neither_assignee_nor_approver_is_ignored() -> None:
    stranger = approving(11, 2, login="stranger", uid=999)
    status = run([plan_reply(10, 0), stranger], [label_event(1, 2, login="stranger", uid=999)])
    assert (status.comment.accepted, status.comment.reason) == (False, "author-not-allowed")
    assert (status.label.accepted, status.label.reason) == (False, "actor-not-allowed")


def test_comment_before_the_plan_reply_does_not_count() -> None:
    status = run([approving(11, 1), plan_reply(10, 2)])
    assert not status.comment.accepted and status.comment.reason == "comment-before-plan"


def test_equal_timestamps_do_not_count_as_after() -> None:
    status = run([plan_reply(10, 2), approving(11, 2)], [label_event(1, 2)])
    assert not status.comment.accepted and not status.label.accepted


def test_a_long_form_for_an_older_hash_after_a_newer_plan_reply_is_refused() -> None:
    old_long = f"approved {rid(H_A)} plan-sha256={H_A}"
    status = run([plan_reply(10, 0, H_A), plan_reply(12, 1, H_B), approving(11, 2, old_long)], plan_hash_now=H_B)
    assert status.comment.reason == "hash-mismatch" and not status.comment.accepted


def test_wrong_hash_in_the_long_form() -> None:
    wrong = f"approved {rid(H_A)} plan-sha256={H_B}"
    assert run([plan_reply(10, 0), approving(11, 2, wrong)]).comment.reason == "hash-mismatch"


def test_edited_approving_comment_does_not_count() -> None:
    status = run([plan_reply(10, 0), approving(11, 2)], edited={11: 4})
    assert not status.comment.accepted and status.comment.reason == "comment-edited"


def test_missing_edit_evidence_fails_closed() -> None:
    comments = [plan_reply(10, 0), approving(11, 2)]
    status = sp.evaluate(
        9, comments, (), EditEvidence(at(-60), None, edits_for(comments[0]).comments), plan_hash_now=H_A,
        host_login=HOST, assignees=(OWNER,), approvers=frozenset(), approval_label=LABEL,
    )
    assert status.comment.reason == "edit-unknown" and not status.approved


def test_edited_plan_reply_is_unusable_even_when_the_host_login_wrote_it() -> None:
    status = run([plan_reply(10, 0), approving(11, 2)], edited={10: 1})
    assert (status.state, status.plan_reason, status.approved) == ("plan-reply-invalid", "plan-reply-edited", False)


def test_plan_files_changed_after_the_reply() -> None:
    status = run([plan_reply(10, 0), approving(11, 2)], [label_event(1, 3)], plan_hash_now=H_B)
    assert (status.state, status.plan_reason, status.approved) == ("plan-changed", "plan-changed", False)
    assert run([plan_reply(10, 0)], plan_hash_now=None).state == "plan-changed"


def test_label_applied_then_removed_is_a_revocation() -> None:
    status = run([plan_reply(10, 0)], [label_event(1, 2), label_event(2, 4, "unlabeled")])
    assert (status.state, status.label_revoked, status.label.reason) == ("revoked", True, "label-removed")


def test_a_comment_approval_stands_when_the_label_is_removed() -> None:
    status = run([plan_reply(10, 0), approving(11, 2)], [label_event(1, 2), label_event(2, 4, "unlabeled")])
    assert status.approved and status.label_revoked and status.state == "approved"


def test_label_applied_again_after_removal_counts_again() -> None:
    events = [label_event(1, 2), label_event(2, 3, "unlabeled"), label_event(3, 4)]
    assert run([plan_reply(10, 0)], events).label.accepted


def test_deleting_an_approving_comment_is_not_a_revocation() -> None:
    gone = run([plan_reply(10, 0)])  # the comment no longer exists: the predicates see no approval, no revoke signal
    assert gone.state == "awaiting-approval" and not gone.label_revoked


@pytest.mark.parametrize("text", ["approved ", " approved", "approved\n", "Approved", "approved.", "> approved", "I approved"])
def test_comment_text_that_is_not_exactly_an_approval_form_never_approves(text: str) -> None:
    assert not run([plan_reply(10, 0), approving(11, 2, text)]).comment.accepted


# --- Status move and host-login flags ------------------------------------------


def test_label_with_no_status_move_is_accepted_with_status_seen_false() -> None:
    status = run([plan_reply(10, 0)], [label_event(1, 2)])
    assert status.approved and status.status_seen is False


def test_label_with_a_status_move_reports_status_seen_true_and_the_same_key() -> None:
    plain = run([plan_reply(10, 0)], [label_event(1, 2)])
    moved = run([plan_reply(10, 0)], [label_event(1, 2), status_event(2, 3)])
    assert moved.approved and moved.status_seen is True and moved.key == plain.key


def test_a_status_move_before_the_plan_reply_is_not_seen_and_never_approves_alone() -> None:
    status = run([plan_reply(10, 5)], [status_event(2, 3)])
    assert status.status_seen is False and not status.approved
    assert run([plan_reply(10, 0)], [status_event(2, 3)]).approved is False


def test_the_host_login_flag_is_set_and_the_approval_is_still_accepted() -> None:
    by_label = run([plan_reply(10, 0)], [label_event(1, 2, login=HOST)], assignees=(HOST,))
    assert by_label.approved and by_label.label.actor_is_host_login and by_label.assignee_is_host_login
    by_comment = run([plan_reply(10, 0), approving(11, 2, login=HOST)], assignees=(HOST,))
    assert by_comment.approved and by_comment.comment.actor_is_host_login
    plain = run([plan_reply(10, 0)], [label_event(1, 2)])
    assert not plain.label.actor_is_host_login and not plain.assignee_is_host_login
