"""GitHub reads that turn comment text into booleans and ids (plan Task 5).

The reads reuse ``argv_events``, ``argv_edits`` (a fixed GraphQL query that ``gh api
graphql`` sends as a POST) and the call budget and page cap of
``superclaude.cli.issue_watch.github``. The comments argv is built with
``_argv_rest_page(n, "comments", page, COMMENTS_JQ)`` as ``argv_comments`` does, with one
new jq projection in the manner of ``MARKER_JQ``: the body never leaves jq. Per comment it
returns the id, author login, author id, author type, created time and values computed
inside jq (whether the whole body matches an approval form, the record id and hash of a long
form, and the plan-reply marker with its hash). Python re-validates every captured value
against a fixed pattern before it is used.

Portability note: ``gh --jq`` runs gojq, not jq. The projection uses only ``test``, ``scan``,
``split``, ``ltrimstr``, ``\\A`` and ``\\z`` with no named groups, which both accept; FU-1
(precondition j) re-checks it against a live reply.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass

from superclaude.cli.issue_watch import github as gh
from superclaude.cli.issue_watch.github import (
    CallBudget,
    Read,
    _argv_rest_page,
    _check,
    _pos_int,
    _rest_read,
    _text,
    _time,
)
from superclaude.cli.issue_watch.predicates import EditEvidence, LabelEvent
from superclaude.cli.issue_watch.runner import Runner

from .stage_predicates import CommentFact, PlanMarker

_RECORD_ID = r"ap-[1-9][0-9]*-plan-[0-9a-f]{12}"
_LONG_LINE = rf"\\Aapproved {_RECORD_ID} plan-sha256=[0-9a-f]{{64}}\\z"
_MARKER = rf"<!-- sc:stage:plan id={_RECORD_ID} plan=[0-9a-f]{{64}} -->"

COMMENTS_JQ = (
    '[.[] | (.body // "") as $b'
    f' | ($b | test("{_LONG_LINE}")) as $long'
    f' | ([$b | scan("{_MARKER}")] | first) as $m'
    " | {id, login: .user.login, user_id: .user.id, user_type: .user.type, created_at,"
    ' matches_approval_line: ($b == "approved" or $long),'
    ' approval_form: (if $b == "approved" then "short" elif $long then "long" else null end),'
    ' approval_record_id: (if $long then ($b | split(" ")[1]) else null end),'
    ' approval_hash: (if $long then ($b | split("=")[1]) else null end),'
    ' plan_marker_record_id: (if $m then ($m | split(" ")[2] | ltrimstr("id=")) else null end),'
    ' plan_marker_hash: (if $m then ($m | split(" ")[3] | ltrimstr("plan=")) else null end)}]'
)
"""The comments projection: the body becomes booleans and fixed-pattern ids."""

_RECORD_ID_RE = re.compile(_RECORD_ID)
_HASH_RE = re.compile(r"[0-9a-f]{64}")
_LOGIN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}(\[bot\])?")
_TYPE_RE = re.compile(r"[A-Za-z]{1,20}")
COMMENTS_UNREADABLE = "comments_unreadable"


def argv_comments_projected(n: int, page: int) -> list[str]:
    """One REST page of the issue's comments, reduced by ``COMMENTS_JQ``."""
    return _argv_rest_page(n, "comments", page, COMMENTS_JQ)


def _pattern_or_none(value: object, pattern: re.Pattern[str]) -> str | None:
    if value is None:
        return None
    text = _text(value)
    _check(pattern.fullmatch(text) is not None)
    return text


def _comment_fact(item: dict) -> CommentFact:
    """One projected comment, every captured value re-validated (a bad shape is malformed)."""
    form = item.get("approval_form")
    _check(form in (None, "short", "long"))
    _check(type(item.get("matches_approval_line")) is bool)
    _check(item["matches_approval_line"] == (form is not None))
    record_id = _pattern_or_none(item.get("approval_record_id"), _RECORD_ID_RE)
    digest = _pattern_or_none(item.get("approval_hash"), _HASH_RE)
    _check((form == "long") == (record_id is not None and digest is not None))
    marker_id = _pattern_or_none(item.get("plan_marker_record_id"), _RECORD_ID_RE)
    marker_hash = _pattern_or_none(item.get("plan_marker_hash"), _HASH_RE)
    _check((marker_id is None) == (marker_hash is None))
    user_id = item.get("user_id")
    _check(user_id is None or (type(user_id) is int and user_id > 0))
    return CommentFact(
        id=_pos_int(item.get("id")),
        author_login=_pattern_or_none(item.get("login"), _LOGIN_RE),
        author_id=user_id,
        author_type=_pattern_or_none(item.get("user_type"), _TYPE_RE),
        created_at=_time(item.get("created_at")),
        approval_form=form,
        approval_record_id=record_id,
        approval_hash=digest,
        plan_marker=PlanMarker(marker_id, marker_hash) if marker_id and marker_hash else None,
    )


def comments(
    runner: Runner, budget: CallBudget, n: int, timeout_for: Callable[[], float | None]
) -> Read:
    """A tuple of ``CommentFact`` for the issue's comments; every failure is ``comments_unreadable``."""
    return _rest_read(
        runner,
        budget,
        timeout_for,
        lambda page: argv_comments_projected(n, page),
        _comment_fact,
        COMMENTS_UNREADABLE,
        COMMENTS_UNREADABLE,
        False,
    )


@dataclass(frozen=True)
class StageEvidence:
    comments: tuple[CommentFact, ...]
    events: tuple[LabelEvent, ...]
    edits: EditEvidence


def read_stage_evidence(
    runner: Runner,
    n: int,
    timeout_for: Callable[[], float | None],
    budget: CallBudget | None = None,
) -> Read:
    """Read events, comments and edits under one ``CallBudget``.

    Returns ``Read(StageEvidence)``, or the first failed ``Read`` (value None, a closed
    reason): a partial read never yields an approval.
    """
    budget = budget or CallBudget()
    events = gh.events(runner, budget, n, timeout_for)
    if events.value is None:
        return events
    found = comments(runner, budget, n, timeout_for)
    if found.value is None:
        return found
    edits = gh.edits(runner, budget, n, timeout_for)
    if edits.value is None:
        return edits
    return Read(StageEvidence(found.value, events.value, edits.value))  # type: ignore[arg-type]


__all__ = [
    "COMMENTS_JQ",
    "COMMENTS_UNREADABLE",
    "StageEvidence",
    "argv_comments_projected",
    "comments",
    "read_stage_evidence",
]
