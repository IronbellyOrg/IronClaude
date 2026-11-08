"""Build, run and read every ``gh`` call the issue watcher makes (design section 8).

Every argv is built here from module constants plus five caller values, each
checked here before it enters an argv (``ValueError`` otherwise): the issue
number (``str(n)`` after ``valid_issue_number``), the page number, the paging
cursor, the trigger label and the login. The repository is the literal
``REPO``. No argv asks for a title, body or comment text: the only
body access is ``contains(<marker>)`` inside ``MARKER_JQ``, evaluated by ``gh``'s
embedded jq, so this process receives a boolean. This module reads no clock.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import TypeVar

from .predicates import (
    CLAIM_MARKER,
    CommentEdit,
    DiscoveredIssue,
    EditEvidence,
    IssueSnapshot,
    LabelEvent,
    Login,
    MarkerEvidence,
    ProjectItem,
    parse_utc,
    valid_issue_number,
)
from .runner import CommandResult, Runner

REPO = "IronbellyOrg/IronClaude"
"""The one repository every argv names (design 8.1, ``R``)."""

PAGE_SIZE = 100
"""REST ``per_page`` value; a full page means another page may follow."""

PAGE_CAP = 5
"""Most pages one paged read may fetch (REST pages or GraphQL cursors)."""

CALL_CAP = 35
"""Most ``gh`` calls one cycle may make (NFR-009)."""

RESERVED_CALLS = 3
"""Calls of ``CALL_CAP`` kept for the FR-011 re-read."""

# --- jq projections (design 8.1, G3, G4, G7) --------------------------------

EVENTS_JQ = (
    "[.[] | {id, event, label: .label.name, actor_id: .actor.id, "
    "actor_login: .actor.login, actor_type: .actor.type, created_at}]"
)
"""G3 projection of one events page."""

# json.dumps gives a jq string literal, so the marker text is never retyped (DF-21).
MARKER_JQ = (
    "[.[] | {id, login: .user.login, created_at, updated_at, "
    f"marker: (.body | contains({json.dumps(CLAIM_MARKER)}))}}]"
)
"""G4 projection of one comments page: the body becomes a boolean."""

REREAD_JQ = "{number, state, labels: [.labels[].name], assignees: [.assignees[].login]}"
"""G7 projection of the FR-011 issue re-read."""

# --- GraphQL queries (design 8.1, G5, G6) -----------------------------------
# [PROPOSAL, UNVERIFIED] drafts from decision DF-14 (research 06, Table 1.5).
# Field names follow the public schema; reply shapes are unverified (FU-1, FU-3).

EDITS_QUERY = """query($number: Int!, $after: String) {
  repository(owner: "IronbellyOrg", name: "IronClaude") {
    issue(number: $number) {
      createdAt
      lastEditedAt
      comments(first: 100, after: $after) {
        nodes { databaseId author { login } createdAt lastEditedAt }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}"""
"""G5: issue and comment edit timestamps."""

PROJECT_ITEMS_QUERY = """query($number: Int!, $after: String) {
  repository(owner: "IronbellyOrg", name: "IronClaude") {
    issue(number: $number) {
      projectItems(first: 100, after: $after) {
        nodes {
          isArchived
          project { id }
          fieldValueByName(name: "Status") {
            ... on ProjectV2ItemFieldSingleSelectValue { name }
          }
        }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}"""
"""G6: the issue's Project items with their Status value."""

# --- argv builders (design 8.1, G1 to G7) -----------------------------------
# Every REST path call carries --method GET (gh defaults to POST once parameters
# are added); the GraphQL calls are POST and carry no --method (DF-28).


def _issue_arg(n: object) -> str:
    """Return ``str(n)`` for a valid issue number, else raise ``ValueError``."""
    if not valid_issue_number(n):
        raise ValueError("invalid issue number")
    return str(n)


def _page_arg(page: object) -> str:
    """Return ``str(page)`` for an ``int`` page in 1..``PAGE_CAP``."""
    if type(page) is not int or not 1 <= page <= PAGE_CAP:
        raise ValueError("invalid page number")
    return str(page)


# [UNVERIFIED] The cursor alphabet (base64 and URL-safe base64 plus ``:`` and
# ``.``) is assumed; FU-1 confirms it against a captured ``endCursor``.
_CURSOR_RE = re.compile(r"[A-Za-z0-9+/=_.:-]{1,256}")

TRIGGER_MAX_CHARS = 50
"""Longest trigger label the watcher accepts (design 131)."""

# The cycle's login regex (design 348, plan step 6.1); checked here too so no
# other login string can reach a ``--assignee`` argument.
_LOGIN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")


def _valid_cursor(text: object) -> bool:
    return isinstance(text, str) and _CURSOR_RE.fullmatch(text) is not None


def _cursor_args(after: str | None) -> list[str]:
    """Return ``["-f", "after=<cursor>"]``, or nothing on the first page."""
    if after is None:
        return []
    if not _valid_cursor(after):
        raise ValueError("invalid cursor")
    return ["-f", f"after={after}"]


def _trigger_arg(trigger: object) -> str:
    """Return ``trigger`` when it is safe as one ``--label`` value.

    Non-empty, at most ``TRIGGER_MAX_CHARS`` characters, no control character,
    no comma (``gh`` splits ``--label`` on commas and ANDs the parts) and no
    leading dash.
    """
    if (
        not isinstance(trigger, str)
        or not 0 < len(trigger) <= TRIGGER_MAX_CHARS
        or trigger.startswith("-")
        or "," in trigger
        or any(ord(c) < 32 or ord(c) == 127 for c in trigger)
    ):
        raise ValueError("invalid trigger label")
    return trigger


def _login_arg(login: object) -> str:
    """Return ``login`` when it matches the GitHub login pattern, else raise."""
    if not isinstance(login, str) or _LOGIN_RE.fullmatch(login) is None:
        raise ValueError("invalid login")
    return login


def argv_user() -> list[str]:
    """G1: own login, account id and the ``Date`` header (FR-002)."""
    return ["gh", "api", "user", "--include"]


def argv_discover(trigger: str, login: str) -> list[str]:
    """G2: open issues carrying ``trigger`` and assigned to ``login`` (FR-003)."""
    return [
        "gh",
        "issue",
        "list",
        "--repo",
        REPO,
        "--state",
        "open",
        "--label",
        _trigger_arg(trigger),
        "--assignee",
        _login_arg(login),
        "--json",
        "number,labels,assignees,state",
        "-L",
        "100",  # the FR-004 fail-closed bound, not PAGE_SIZE
    ]


def _argv_rest_page(n: object, kind: str, page: object, jq: str) -> list[str]:
    """One REST page of ``repos/R/issues/N/<kind>`` projected by ``jq``."""
    return [
        "gh",
        "api",
        "--method",
        "GET",
        f"repos/{REPO}/issues/{_issue_arg(n)}/{kind}",
        "-F",
        f"per_page={PAGE_SIZE}",
        "-F",
        f"page={_page_arg(page)}",
        "--jq",
        jq,
    ]


def argv_events(n: int, page: int) -> list[str]:
    """G3: one page of the issue's event history (FR-005, FR-006)."""
    return _argv_rest_page(n, "events", page, EVENTS_JQ)


def argv_comments(n: int, page: int) -> list[str]:
    """G4: one page of the issue's comments, reduced to marker evidence (FR-009)."""
    return _argv_rest_page(n, "comments", page, MARKER_JQ)


def _argv_graphql(query: str, n: object, after: str | None) -> list[str]:
    """One GraphQL page; ``-F`` sends ``number`` typed, no ``after`` sends null."""
    return [
        "gh",
        "api",
        "graphql",
        "-f",
        f"query={query}",
        "-F",
        f"number={_issue_arg(n)}",
        *_cursor_args(after),
    ]


def argv_edits(n: int, after: str | None = None) -> list[str]:
    """G5: one page of issue and comment edit timestamps."""
    return _argv_graphql(EDITS_QUERY, n, after)


def argv_project_items(n: int, after: str | None = None) -> list[str]:
    """G6: one page of the issue's Project items (FR-007)."""
    return _argv_graphql(PROJECT_ITEMS_QUERY, n, after)


def argv_reread(n: int) -> list[str]:
    """G7: re-read the issue's number, state, labels and assignees (FR-011)."""
    return [
        "gh",
        "api",
        "--method",
        "GET",
        f"repos/{REPO}/issues/{_issue_arg(n)}",
        "--jq",
        REREAD_JQ,
    ]


# --- reply classification (design 8.2) --------------------------------------

# [UNVERIFIED] gh stderr text and GraphQL error type names (design line 590,
# DF-37). Kept in this ONE table so the live test can correct them in one place.
GH_ERROR_SIGNS: dict[str, tuple[str, ...]] = {
    "auth_stderr": ("HTTP 401", "gh auth login"),
    "scope_types": ("INSUFFICIENT_SCOPES",),
    "scope_stderr": ("read:project",),
    "rate_status_stderr": ("HTTP 403", "HTTP 429"),
    "rate_text_stderr": ("rate limit",),  # matched case-insensitively
    "rate_types": ("RATE_LIMITED",),
    "transient_stderr_re": (r"HTTP 5[0-9]{2}",),
}
"""Every stderr substring, regex and GraphQL error type ``classify`` matches."""


@dataclass(frozen=True)
class Reply:
    """One classified runner result; ``payload`` is the parsed JSON when ``ok``."""

    kind: str
    result: CommandResult
    payload: object


def _split_include(stdout: str) -> tuple[dict[str, str], str] | None:
    """Split ``--include`` output into lower-cased headers and the body.

    Layout (shape unverified): status line, ``Name: value`` lines, a blank line,
    then the body. Any other layout gives None.
    """
    head, sep, body = stdout.replace("\r\n", "\n").partition("\n\n")
    lines = head.split("\n")
    if not sep or not lines[0].startswith("HTTP/"):
        return None
    headers: dict[str, str] = {}
    for line in lines[1:]:
        name, colon, value = line.partition(":")
        if not colon:
            return None
        headers[name.strip().lower()] = value.strip()
    return headers, body


def _body(result: CommandResult, include_headers: bool) -> str | None:
    """Return the reply body, or None when the ``--include`` layout is wrong."""
    if not include_headers:
        return result.stdout
    split = _split_include(result.stdout)
    return None if split is None else split[1]


def _parse_json(text: str | None) -> tuple[bool, object]:
    """Return ``(True, value)`` when ``text`` parses as JSON, else ``(False, None)``."""
    if text is None:
        return False, None
    try:
        return True, json.loads(text)
    except (ValueError, RecursionError):
        return False, None


def _graphql_error_types(text: str | None) -> set[str]:
    """Return the string ``errors[].type`` values of a GraphQL reply body."""
    ok, value = _parse_json(text)
    errors = value.get("errors") if ok and isinstance(value, dict) else None
    if not isinstance(errors, list):
        return set()
    return {
        e["type"]
        for e in errors
        if isinstance(e, dict) and isinstance(e.get("type"), str)
    }


def _any_in(signs: str, text: str) -> bool:
    """True when ``text`` contains one of the ``GH_ERROR_SIGNS[signs]`` substrings."""
    return any(s in text for s in GH_ERROR_SIGNS[signs])


def classify(result: CommandResult, *, include_headers: bool = False) -> Reply:
    """Map one runner result to a ``Reply`` (design table 8.2, rows in order).

    ``include_headers`` is True only for G1, whose JSON follows the header
    block. There is no exit-code rule beyond exit 0 (DF-37); a spawn error has
    no output and falls to ``failed``.
    """
    if result.timed_out:
        return Reply("timeout", result, None)
    body = _body(result, include_headers)
    if result.returncode == 0:
        ok, value = _parse_json(body)
        return Reply("ok", result, value) if ok else Reply("non_json", result, None)
    stderr = result.stderr
    types = _graphql_error_types(body)
    if _any_in("auth_stderr", stderr):
        return Reply("auth_failed", result, None)
    if types & set(GH_ERROR_SIGNS["scope_types"]) or _any_in("scope_stderr", stderr):
        return Reply("scope_missing", result, None)
    rate_text = any(s in stderr.lower() for s in GH_ERROR_SIGNS["rate_text_stderr"])
    if (_any_in("rate_status_stderr", stderr) and rate_text) or types & set(
        GH_ERROR_SIGNS["rate_types"]
    ):
        return Reply("rate_limited", result, None)
    if any(re.search(p, stderr) for p in GH_ERROR_SIGNS["transient_stderr_re"]):
        return Reply("transient", result, None)
    return Reply("failed", result, None)


# --- rate-limit time (design 8.3, DF-35) ------------------------------------

RATE_LIMIT_MAX_WAIT_S = 3600
"""Longest wait taken from a header; anything else clamps to this (FR-028)."""


def _g1_header(result: CommandResult, name: str) -> str | None:
    """Return header ``name`` of a G1 (``--include``) result, else None."""
    if "--include" not in result.argv:
        return None
    split = _split_include(result.stdout)
    return None if split is None else split[0].get(name)


def _header_int(result: CommandResult, name: str) -> int | None:
    """Return a G1 header as a non-negative ``int``, or None when unparseable."""
    value = _g1_header(result, name)
    if value is None or not re.fullmatch(r"[0-9]+", value):
        return None
    return int(value)


def retry_after(result: CommandResult) -> int | None:
    """Return the ``Retry-After`` seconds of a G1 result, or None when absent."""
    return _header_int(result, "retry-after")


def date_header(result: CommandResult) -> datetime | None:
    """Return the G1 ``Date`` header as an aware time, or None when unparseable.

    An unparseable ``Date`` skips the skew check (DF-35).
    """
    value = _g1_header(result, "date")
    if value is None:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError, IndexError, OverflowError):
        return None
    if parsed is None:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def rate_limit_wait(result: CommandResult, now: datetime) -> tuple[datetime, str]:
    """Return ``(next_permitted_at, reason)`` for a rate-limited result.

    ``Retry-After`` in 1..3600 s wins; else an ``x-ratelimit-reset`` epoch later
    than ``now`` by at most 3600 s; else now + 3600 s, ``rate_limit_clamped``.
    ``now`` must be timezone-aware.
    """
    seconds = retry_after(result)
    if seconds is not None and 0 < seconds <= RATE_LIMIT_MAX_WAIT_S:
        return now + timedelta(seconds=seconds), "rate_limited"
    reset = _header_int(result, "x-ratelimit-reset")
    if reset is not None and 0 < reset - now.timestamp() <= RATE_LIMIT_MAX_WAIT_S:
        return datetime.fromtimestamp(reset, tz=timezone.utc), "rate_limited"
    return now + timedelta(seconds=RATE_LIMIT_MAX_WAIT_S), "rate_limit_clamped"


# --- call budget (NFR-009) and read results ----------------------------------


class CallBudget:
    """Counts one cycle's ``gh`` calls against ``CALL_CAP`` (NFR-009).

    Per-issue calls share ``CALL_CAP``; the last ``RESERVED_CALLS`` of them are
    kept for the FR-011 re-read. Shared calls (G1, G2) are counted apart.
    """

    def __init__(self) -> None:
        self.calls = 0
        self.shared_calls = 0

    def spend(self, reserved: bool = False) -> bool:
        """Count one per-issue call; False (nothing counted) when it would breach."""
        cap = CALL_CAP if reserved else CALL_CAP - RESERVED_CALLS
        if self.calls >= cap:
            return False
        self.calls += 1
        return True

    def spend_shared(self) -> None:
        """Count one shared call; shared calls are never refused."""
        self.shared_calls += 1

    @property
    def total(self) -> int:
        """Every call counted this cycle, the ``gh_calls`` audit value."""
        return self.calls + self.shared_calls


@dataclass(frozen=True)
class Read:
    """The result of one typed read.

    ``value`` is the parsed data, ``reason`` the skip reason (None when read),
    ``kind`` the ``Reply`` kind and ``retry_after_s`` a G1 ``Retry-After`` value.
    """

    value: object
    reason: str | None = None
    kind: str = "ok"
    retry_after_s: int | None = None


# --- typed reads: shared machinery (design 8.2, DF-18, DF-19) ----------------
# A failed read has ``value`` None. Its ``kind`` is the ``Reply`` kind, or
# ``non_json`` (an ok reply of the wrong shape), ``incomplete`` (page cap,
# repeated id or cursor), ``budget_exhausted`` (no call made) and, for
# discovery only, ``truncated`` or ``discovery_duplicate``.

DISCOVERY_BOUND = 100
"""Discovery results at or above this count fail closed (FR-004)."""

_SHARED_REASONS = {
    "timeout": "gh_timeout",
    "transient": "gh_timeout",
    "non_json": "gh_non_json",
    "rate_limited": "rate_limited",
    "scope_missing": "project_read_failed",
}
"""Cycle reason of a failed G1 or G2 reply; anything else is ``gh_auth_failed``."""


class _Malformed(Exception):
    """Raised inside a parser when an ok reply has a shape the read rejects."""


def _check(ok: bool) -> None:
    if not ok:
        raise _Malformed


def _obj(value: object) -> dict:
    if not isinstance(value, dict):
        raise _Malformed
    return value


def _list(value: object) -> list:
    if not isinstance(value, list):
        raise _Malformed
    return value


def _pos_int(value: object) -> int:
    """An ``int`` above zero; ``bool`` fails ``type(v) is int`` (DF-18)."""
    if type(value) is not int or value <= 0:
        raise _Malformed
    return value


def _text(value: object) -> str:
    if not isinstance(value, str):
        raise _Malformed
    return value


def _opt_text(value: object) -> str | None:
    return None if value is None else _text(value)


def _time(value: object) -> datetime:
    try:
        return parse_utc(_text(value))
    except ValueError:
        raise _Malformed from None


def _opt_time(value: object) -> datetime | None:
    return None if value is None else _time(value)


def _names(value: object, key: str) -> tuple[str, ...]:
    """The ``key`` strings of a list of objects, e.g. ``labels[].name``."""
    return tuple(_text(_obj(v).get(key)) for v in _list(value))


def _texts(value: object) -> tuple[str, ...]:
    return tuple(_text(v) for v in _list(value))


def _call(
    runner: Runner,
    budget: CallBudget | None,
    timeout_for: Callable[[], float | None],
    argv: list[str],
    *,
    reserved: bool = False,
    include_headers: bool = False,
) -> Reply | None:
    """Spend one call, then run ``argv``; None when no call may start.

    ``budget`` is None for the shared calls G1 and G2, which the cycle counts
    with ``CallBudget.spend_shared``.
    """
    timeout = timeout_for()
    if timeout is None:
        return None
    if budget is not None and not budget.spend(reserved):
        return None
    result = runner.run(argv, timeout)
    return classify(result, include_headers=include_headers)


def _failed(reply: Reply, reason: str) -> Read:
    return Read(None, reason, reply.kind, retry_after(reply.result))


def _shared_failed(reply: Reply) -> Read:
    return _failed(reply, _SHARED_REASONS.get(reply.kind, "gh_auth_failed"))


_NO_CALL = Read(None, "budget_exhausted", "budget_exhausted")
_SHARED_NO_CALL = Read(None, "gh_timeout", "timeout")


def _rest_read(
    runner: Runner,
    budget: CallBudget,
    timeout_for: Callable[[], float | None],
    argv_for_page: Callable[[int], list[str]],
    parse: Callable[[dict], object | None],
    unreadable: str,
    incomplete: str,
    reserved: bool,
) -> Read:
    """Page a G3 or G4 read (design 8.2 table, DF-19); ``parse`` None drops an item."""
    values: list[object] = []
    seen: set[int] = set()
    for page in range(1, PAGE_CAP + 1):
        reply = _call(
            runner, budget, timeout_for, argv_for_page(page), reserved=reserved
        )
        if reply is None:
            return _NO_CALL
        if reply.kind != "ok":
            return _failed(reply, unreadable)
        try:
            items = _list(reply.payload)
            _check(len(items) <= PAGE_SIZE)
            for item in items:
                item_id = _pos_int(_obj(item).get("id"))
                if item_id in seen:
                    return Read(None, incomplete, "incomplete")
                seen.add(item_id)
                parsed = parse(item)
                if parsed is not None:
                    values.append(parsed)
        except _Malformed:
            return Read(None, unreadable, "non_json")
        if len(items) < PAGE_SIZE:
            return Read(tuple(values))
    return Read(None, incomplete, "incomplete")


def _errors_kind(result: CommandResult) -> str:
    """Kind of an exit-0 GraphQL reply that carries an ``errors`` list."""
    types = _graphql_error_types(result.stdout)
    if types & set(GH_ERROR_SIGNS["scope_types"]):
        return "scope_missing"
    if types & set(GH_ERROR_SIGNS["rate_types"]):
        return "rate_limited"
    return "failed"


_I = TypeVar("_I")
_N = TypeVar("_N")


def _graphql_read(
    runner: Runner,
    budget: CallBudget,
    timeout_for: Callable[[], float | None],
    argv_for_cursor: Callable[[str | None], list[str]],
    connection: str,
    parse_issue: Callable[[dict], _I],
    parse_node: Callable[[object], _N],
    unreadable: str,
    reserved: bool,
) -> Read | tuple[_I, tuple[_N, ...]]:
    """Page a G5 or G6 read (design line 575, DF-19).

    Returns ``(parse_issue(first page's issue), nodes)``, or a failed ``Read``.
    Complete only when ``hasNextPage`` is false; every failure gives
    ``unreadable``.
    """
    nodes_out: list[_N] = []
    first: list[_I] = []  # the first page's issue fields
    cursors: set[str] = set()
    after: str | None = None
    for page in range(1, PAGE_CAP + 1):
        reply = _call(
            runner, budget, timeout_for, argv_for_cursor(after), reserved=reserved
        )
        if reply is None:
            return _NO_CALL
        if reply.kind != "ok":
            return _failed(reply, unreadable)
        try:
            body = _obj(reply.payload)
            if body.get("errors") is not None:
                return Read(None, unreadable, _errors_kind(reply.result))
            issue = _obj(_obj(_obj(body.get("data")).get("repository")).get("issue"))
            conn = _obj(issue.get(connection))
            nodes = _list(conn.get("nodes"))
            _check(len(nodes) <= PAGE_SIZE)
            info = _obj(conn.get("pageInfo"))
            more = info.get("hasNextPage")
            _check(type(more) is bool)
            cursor = _opt_text(info.get("endCursor"))
            fields = parse_issue(issue)
            nodes_out += [parse_node(n) for n in nodes]
        except _Malformed:
            return Read(None, unreadable, "non_json")
        if page == 1:
            first.append(fields)
        if cursor and cursor in cursors:
            return Read(None, unreadable, "incomplete")
        if not more:
            return first[0], tuple(nodes_out)
        if not cursor:
            return Read(None, unreadable, "incomplete")
        if not _valid_cursor(cursor):  # it is about to become an argv item
            return Read(None, unreadable, "non_json")
        cursors.add(cursor)
        after = cursor
    return Read(None, unreadable, "incomplete")


# --- typed reads: item parsers (DF-18 null rules) ----------------------------


def _event(item: dict) -> LabelEvent:
    """One G3 item; label and actor fields are required only for (un)labeled."""
    event = _text(item.get("event"))
    labelled = event in ("labeled", "unlabeled")
    text = _text if labelled else _opt_text
    actor_id = item.get("actor_id")
    return LabelEvent(
        id=_pos_int(item.get("id")),
        event=event,
        label=text(item.get("label")),
        actor_id=_pos_int(actor_id) if labelled or actor_id is not None else None,
        actor_login=text(item.get("actor_login")),
        actor_type=text(item.get("actor_type")),
        created_at=_time(item.get("created_at")),
    )


def _marker(item: dict) -> MarkerEvidence | None:
    """One G4 item; a null ``login`` is never the own login, so it is dropped."""
    marker = item.get("marker")
    _check(type(marker) is bool)
    value = MarkerEvidence(
        id=_pos_int(item.get("id")),
        login=_opt_text(item.get("login")) or "",
        created_at=_time(item.get("created_at")),
        updated_at=_time(item.get("updated_at")),
        marker=bool(marker),
    )
    return value if value.login else None


def _edited_at(d: dict) -> datetime | None:
    """``lastEditedAt``: an explicit null is "never edited"; a missing key is not.

    A reply without the key is a shape change, and incomplete evidence must not
    read as "unchanged" (``predicates.unchanged_since``), so it is malformed.
    """
    _check("lastEditedAt" in d)
    return _opt_time(d["lastEditedAt"])


def _edit_issue(issue: dict) -> tuple[datetime, datetime | None]:
    return _time(issue.get("createdAt")), _edited_at(issue)


def _comment_edit(node: object) -> CommentEdit:
    d = _obj(node)
    author = d.get("author")
    return CommentEdit(
        database_id=_pos_int(d.get("databaseId")),
        author_login=None if author is None else _text(_obj(author).get("login")),
        created_at=_time(d.get("createdAt")),
        last_edited_at=_edited_at(d),
    )


def _project_item(node: object) -> ProjectItem:
    d = _obj(node)
    archived = d.get("isArchived")
    _check(type(archived) is bool)
    # [UNVERIFIED] reply shape (design 837, FU-1): treated as None when the value
    # is null or has no name; any other non-object value is malformed.
    status = d.get("fieldValueByName")
    return ProjectItem(
        is_archived=bool(archived),
        project_id=_text(_obj(d.get("project")).get("id")),
        status_name=None if status is None else _opt_text(_obj(status).get("name")),
    )


# --- typed reads: public API --------------------------------------------------
# ``timeout_for`` returns the next call's timeout, or None when no new ``gh``
# call may start (under 5 s left, design 8.5). Every read returns a ``Read`` and
# never raises for a malformed reply.


def user(runner: Runner, timeout_for: Callable[[], float | None]) -> Read:
    """G1: a ``Login`` (own login, account id, ``Date`` header) (FR-002).

    The login regex and the ``owner_account_id`` compare are the cycle's.
    """
    reply = _call(runner, None, timeout_for, argv_user(), include_headers=True)
    if reply is None:
        return _SHARED_NO_CALL
    if reply.kind != "ok":
        return _shared_failed(reply)
    try:
        d = _obj(reply.payload)
        value = Login(
            _text(d.get("login")), _pos_int(d.get("id")), date_header(reply.result)
        )
    except _Malformed:
        return Read(None, "gh_non_json", "non_json")
    return Read(value)


def discover(
    runner: Runner, trigger: str, login: str, timeout_for: Callable[[], float | None]
) -> Read:
    """G2: a tuple of ``DiscoveredIssue`` (FR-003, FR-004).

    ``DISCOVERY_BOUND`` or more results give ``truncated``, a repeated number
    ``discovery_duplicate`` and any malformed element ``non_json``. Raises
    ``ValueError`` before any call for a ``trigger`` or ``login`` that is unsafe
    as a command-line value (the cycle checks both first).
    """
    reply = _call(runner, None, timeout_for, argv_discover(trigger, login))
    if reply is None:
        return _SHARED_NO_CALL
    if reply.kind != "ok":
        return _shared_failed(reply)
    issues: list[DiscoveredIssue] = []
    seen: set[int] = set()
    try:
        items = _list(reply.payload)
        if len(items) >= DISCOVERY_BOUND:
            return Read(None, "truncated", "truncated")
        for item in items:
            d = _obj(item)
            number = _pos_int(d.get("number"))
            _check(valid_issue_number(number))
            if number in seen:
                return Read(None, "discovery_duplicate", "discovery_duplicate")
            seen.add(number)
            issues.append(
                DiscoveredIssue(
                    number=number,
                    labels=_names(d.get("labels"), "name"),
                    assignees=_names(d.get("assignees"), "login"),
                    state=_text(d.get("state")),
                )
            )
    except _Malformed:
        return Read(None, "gh_non_json", "non_json")
    return Read(tuple(issues))


def events(
    runner: Runner,
    budget: CallBudget,
    n: int,
    timeout_for: Callable[[], float | None],
    *,
    reserved: bool = False,
) -> Read:
    """G3 (G3' with ``reserved``): a tuple of ``LabelEvent`` (FR-005, FR-006)."""
    return _rest_read(
        runner,
        budget,
        timeout_for,
        lambda page: argv_events(n, page),
        _event,
        "events_unreadable",
        "events_incomplete",
        reserved,
    )


def marker_comments(
    runner: Runner, budget: CallBudget, n: int, timeout_for: Callable[[], float | None]
) -> Read:
    """G4: a tuple of ``MarkerEvidence`` for comments with a login (FR-009).

    Every failure, including an incomplete read, is ``marker_unreadable`` and
    never counts as claimed (DF-02).
    """
    return _rest_read(
        runner,
        budget,
        timeout_for,
        lambda page: argv_comments(n, page),
        _marker,
        "marker_unreadable",
        "marker_unreadable",
        False,
    )


def edits(
    runner: Runner, budget: CallBudget, n: int, timeout_for: Callable[[], float | None]
) -> Read:
    """G5: an ``EditEvidence``; every failure is ``edits_unreadable`` (DF-02)."""
    out = _graphql_read(
        runner,
        budget,
        timeout_for,
        lambda after: argv_edits(n, after),
        "comments",
        _edit_issue,
        _comment_edit,
        "edits_unreadable",
        False,
    )
    if isinstance(out, Read):
        return out
    (created, edited), comments = out
    return Read(EditEvidence(created, edited, comments))


def project_items(
    runner: Runner,
    budget: CallBudget,
    n: int,
    timeout_for: Callable[[], float | None],
    *,
    reserved: bool = False,
) -> Read:
    """G6 (G6' with ``reserved``): a tuple of ``ProjectItem`` (FR-007).

    Every failure is ``project_unreadable``; a ``scope_missing`` kind tells the
    cycle to exit 3 ``project_read_failed``.
    """
    out = _graphql_read(
        runner,
        budget,
        timeout_for,
        lambda after: argv_project_items(n, after),
        "projectItems",
        lambda issue: None,
        _project_item,
        "project_unreadable",
        reserved,
    )
    return out if isinstance(out, Read) else Read(out[1])


def reread(
    runner: Runner, budget: CallBudget, n: int, timeout_for: Callable[[], float | None]
) -> Read:
    """G7: an ``IssueSnapshot`` from one reserved call (FR-011).

    A timeout or 5xx is ``revalidation_transient``; any other failure, or a
    reply for another number, is ``revalidation_failed``.
    """
    reply = _call(runner, budget, timeout_for, argv_reread(n), reserved=True)
    if reply is None:
        return _NO_CALL
    if reply.kind != "ok":
        transient = reply.kind in ("timeout", "transient")
        reason = "revalidation_transient" if transient else "revalidation_failed"
        return _failed(reply, reason)
    try:
        d = _obj(reply.payload)
        _check(d.get("number") == n and valid_issue_number(d.get("number")))
        value = IssueSnapshot(
            number=n,
            state=_text(d.get("state")),
            labels=_texts(d.get("labels")),
            assignees=_texts(d.get("assignees")),
        )
    except _Malformed:
        return Read(None, "revalidation_failed", "non_json")
    return Read(value)
