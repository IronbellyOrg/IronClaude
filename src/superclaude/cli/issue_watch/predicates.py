"""Pure predicates for the issue watcher (design section 4 and 4.11).

This module performs no I/O and reads no clock: every time is a parameter.
It imports nothing from ``superclaude`` so every other module may import it.

The poll finds issues assigned to the user in any listed repository, so every
issue is named by its repository and number: the store key is ``owner/repo#N``
and the per-issue file name of the orchestrator is ``owner__repo__N``.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone

CLAIM_MARKER = "<!-- sc:issue:claim -->"
"""Claim-comment marker, read by the orchestrator CLI and ``test_marker_contract``."""

MAX_ISSUE_NUMBER = 999_999_999
"""Largest issue number the watcher accepts."""

REPO_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9._-]{1,100}")
"""``owner/name`` of a repository (spec 3.4); used with ``fullmatch``."""

LOGIN_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")
"""A GitHub login or organisation name; used with ``fullmatch``."""

HOLD_LABEL = "hold:plan"
"""The label the poll adds and removes (4.11 point 2); a constant of the code, not a setting."""

BACKLOG_LABEL = "hold:backlog"
"""Placed and removed by a person only; the poll reads it and never writes it."""

WAKE_ID_PATTERN = re.compile(r"[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}")
"""A wake id (spec 3.1); ``launch.WAKE_ID_PATTERN`` is a pinned copy."""

ORCHESTRATOR_ID_PATTERN = re.compile(r"[a-z0-9]{1,12}-[1-9][0-9]{0,5}")
"""``<short>-<n>``, the id of one orchestrator (spec 5.7 point 2)."""

ACK_REASON_PATTERN = re.compile(r"[a-z][a-z0-9_]{0,39}")
"""The free text of an acknowledgment skip reason, stored after this check only."""

_KEY_PATTERN = re.compile(r"(?P<repo>[^#]+)#(?P<number>[1-9][0-9]{0,8})")

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


def valid_repo(value: object) -> bool:
    """Return True for an ``owner/name`` string (never ``.`` or ``..`` as a part)."""
    if not isinstance(value, str) or REPO_PATTERN.fullmatch(value) is None:
        return False
    return value.split("/", 1)[1] not in (".", "..")


def valid_login(value: object) -> bool:
    """Return True for a string that fully matches ``LOGIN_PATTERN``."""
    return isinstance(value, str) and LOGIN_PATTERN.fullmatch(value) is not None


def issue_key(repo: object, number: object) -> str:
    """Return the store key ``owner/repo#N``; ``ValueError`` for a bad repo or number."""
    if not valid_repo(repo) or not valid_issue_number(number):
        raise ValueError("invalid repo or issue number")
    return f"{repo}#{number}"


def split_issue_key(key: object) -> tuple[str, int]:
    """Return ``(repo, number)`` of a store key; ``ValueError`` for any other text."""
    match = _KEY_PATTERN.fullmatch(key) if isinstance(key, str) else None
    if match is None or not valid_repo(match["repo"]):
        raise ValueError("invalid issue key")
    number = int(match["number"])
    if not valid_issue_number(number):
        raise ValueError("invalid issue key")
    return match["repo"], number


def file_key(repo: object, number: object) -> str:
    """Return ``owner__repo__N``, the name part of the orchestrator's per-issue files."""
    issue_key(repo, number)  # validates both
    return f"{str(repo).replace('/', '__', 1)}__{number}"


OPERATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
"""Receipt and handle ids that may be stored in the dispatch record.

``launch.HANDLE_PATTERN`` is a second copy, because ``launch`` may import only
``runner``; a test pins the two patterns equal.
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
    """One row of the S1 search (assigned to the user), spec 4.2.

    ``title`` and ``body`` are kept only in memory for the plan check and for a
    plan request; no audit line, store field or argv carries them.
    """

    repo: str
    number: int
    labels: tuple[str, ...]
    assignees: tuple[str, ...]
    state: str
    updated_at: datetime
    title: str = ""
    body: str = ""

    @property
    def key(self) -> str:
        """The store key ``owner/repo#N``."""
        return issue_key(self.repo, self.number)


@dataclass(frozen=True)
class InfoItem:
    """One row of an information stream (S2 mentions, S3 could be assigned, S4 affects)."""

    stream: str
    repo: str
    number: int
    kind: str
    updated_at: datetime

    @property
    def seen_key(self) -> str:
        """The ``info_seen`` key ``stream repo#number updated_at`` (spec 4.3 rule 3)."""
        return f"{self.stream} {issue_key(self.repo, self.number)} {format_utc(self.updated_at)}"


@dataclass(frozen=True)
class IssueSnapshot:
    """Issue state, labels, assignees and body from the pre-wake re-read."""

    repo: str
    number: int
    state: str
    labels: tuple[str, ...]
    assignees: tuple[str, ...]
    body: str = ""


def is_intended_owner(
    assignees: Iterable[str], own_login: str
) -> tuple[bool, str | None]:
    """The DQ1 rule: every assignee is the user and there is at least one.

    The user set is the one own login (owner ruling 11: no bot list). Otherwise
    the skip reason is ``unassigned`` (empty set) or ``assigned_other`` (any
    other assignee, a co-assignee included).
    """
    names = set(assignees)
    if not names:
        return False, "unassigned"
    if names <= {own_login}:
        return True, None
    return False, "assigned_other"


def eligibility_order(
    discovered: Iterable[DiscoveredIssue], known: Mapping[str, object] | None = None
) -> list[DiscoveredIssue]:
    """Order issues by repository, then by number (spec 4.10).

    ``known`` holds the store keys that already have an entry; those are left
    out, so the result is the new issues only. The ``MAX_CANDIDATES`` cap is
    applied by the cycle.
    """
    skip = known or {}
    return sorted(
        (i for i in discovered if i.key not in skip), key=lambda i: (i.repo, i.number)
    )
