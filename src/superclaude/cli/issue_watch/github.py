"""Build, run and read every ``gh`` call the issue watcher makes (design 4.2, 4.10, 4.11).

Every argv is built here from module constants plus caller values, each checked
here before it enters an argv (``ValueError`` otherwise): the repository
(``owner/name``), the issue number (``str(n)`` after ``valid_issue_number``),
the login, the organisation, the search time and one of four fixed stream names.
No repository is a constant: the poll searches by ``org:<owner>`` and every
result row is checked again against the repository list.

The reads carry text of the issue (the S1 ``title`` and ``body``, the re-read
``body``). It is held in memory for the plan check and for one plan request; no
audit line, store field or argv carries it. This module reads no clock.

The only writes are the label writes of the hold (4.11 point 2): create the label
when it is absent, add it, remove it. ``LabelWriter`` builds them from fixed
argv builders; the only ``DELETE`` it can issue is
``repos/<R>/issues/<N>/labels/hold:plan``, and an injected ``guard`` may refuse
any argv before it runs (PR B passes ``limits.refuse``).
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

from .predicates import (
    HOLD_LABEL,
    DiscoveredIssue,
    InfoItem,
    IssueSnapshot,
    Login,
    format_utc,
    parse_utc,
    valid_issue_number,
    valid_repo,
)
from .runner import CommandResult, Runner

PAGE_SIZE = 100
"""REST ``per_page`` value; a full page means another page may follow."""

PAGE_CAP = 5
"""Most pages one paged read may fetch."""

CALL_CAP = 35
"""Most ``gh`` calls one cycle may make (NFR-009)."""

RESERVED_CALLS = 12
"""Calls of ``CALL_CAP`` kept for the re-read: ``MAX_CANDIDATES`` (10) plus 2 (4.6)."""

_HOLD_LABEL_COLOR = "FBCA04"
_HOLD_LABEL_TEXT = "The issue has no plan yet; set by the issue watcher"

# --- jq projections (design 4.2, 4.11) --------------------------------------

_SEARCH_ROW_JQ = (
    "repository_url, number, state, updated_at, "
    "labels: [.labels[].name], assignees: [.assignees[].login], "
    "pull_request: (.pull_request != null)"
)
SEARCH_ASSIGNED_JQ = (
    "{total_count, incomplete_results, items: [.items[] | {"
    + _SEARCH_ROW_JQ
    + ', title, body: (.body // "")}]}'
)
"""S1 projection: a row carries the title and body the plan check needs."""

SEARCH_INFO_JQ = (
    "{total_count, incomplete_results, items: [.items[] | "
    "{repository_url, number, updated_at, pull_request: (.pull_request != null)}]}"
)
"""S2 to S4 projection: no text at all."""

REREAD_JQ = (
    "{number, state, labels: [.labels[].name], assignees: [.assignees[].login], "
    'body: (.body // "")}'
)
"""The pre-wake issue re-read."""

TIMELINE_JQ = (
    '[.[] | select(.event == "cross-referenced" or .event == "connected") | '
    "{event, created_at, pull_request: ((.source.issue.pull_request // null) != null)}]"
)
"""E3: the events of an issue's timeline that show a linked or mentioning pull request."""

BRANCH_JQ = "{date: .commit.commit.committer.date}"
"""E2: the date of a branch's newest commit."""

# --- argv builders ------------------------------------------------------------
# Every REST path call carries --method GET (gh defaults to POST once parameters
# are added).

_BRANCH_NAME = re.compile(r"[A-Za-z0-9._/-]{1,200}")
_ORG = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")
_LOGIN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")
STREAMS = ("mentions", "could_assign", "affects")
"""The three information streams S2, S3 and S4."""


def _issue_arg(n: object) -> str:
    """Return ``str(n)`` for a valid issue number, else raise ``ValueError``."""
    if not valid_issue_number(n):
        raise ValueError("invalid issue number")
    return str(n)


def _repo_arg(repo: object) -> str:
    """Return ``repo`` when it is ``owner/name``, else raise ``ValueError``."""
    if not valid_repo(repo):
        raise ValueError("invalid repo")
    return str(repo)


def _login_arg(login: object) -> str:
    """Return ``login`` when it matches the GitHub login pattern, else raise."""
    if not isinstance(login, str) or _LOGIN_RE.fullmatch(login) is None:
        raise ValueError("invalid login")
    return login


def _org_arg(owner: object) -> str:
    """Return ``owner`` when it is an organisation or user name, else raise."""
    if not isinstance(owner, str) or _ORG.fullmatch(owner) is None:
        raise ValueError("invalid organisation")
    return owner


def _branch_arg(name: object) -> str:
    """Return ``name`` when it is a branch name that cannot read as an option."""
    if (
        not isinstance(name, str)
        or _BRANCH_NAME.fullmatch(name) is None
        or name.startswith("-")
        or ".." in name
    ):
        raise ValueError("invalid branch name")
    return name


def argv_user() -> list[str]:
    """G1: own login, account id and the ``Date`` header (FR-002)."""
    return ["gh", "api", "user", "--include"]


def _argv_search(query: str, jq: str) -> list[str]:
    return [
        "gh",
        "api",
        "--method",
        "GET",
        "search/issues",
        "-f",
        f"q={query}",
        "-F",
        f"per_page={PAGE_SIZE}",
        "--jq",
        jq,
    ]


def argv_search_assigned(owner: str, login: str) -> list[str]:
    """S1: open issues assigned to ``login`` in organisation ``owner`` (the only trigger)."""
    query = f"is:issue is:open assignee:{_login_arg(login)} org:{_org_arg(owner)}"
    return _argv_search(query, SEARCH_ASSIGNED_JQ)


def argv_search_info(stream: str, owner: str, login: str, since: datetime) -> list[str]:
    """S2 to S4: an information stream, limited to items changed since ``since``."""
    org, who, when = _org_arg(owner), _login_arg(login), format_utc(since)
    if stream == "mentions":
        query = f"mentions:{who} updated:>={when} org:{org}"
    elif stream == "could_assign":
        query = f"is:issue is:open no:assignee created:>={when} org:{org}"
    elif stream == "affects":
        query = f"involves:{who} updated:>={when} org:{org} -assignee:{who}"
    else:
        raise ValueError("invalid stream")
    return _argv_search(query, SEARCH_INFO_JQ)


def argv_reread(repo: str, n: int) -> list[str]:
    """Re-read one issue of ``repo``: number, state, labels, assignees and body."""
    return [
        "gh",
        "api",
        "--method",
        "GET",
        f"repos/{_repo_arg(repo)}/issues/{_issue_arg(n)}",
        "--jq",
        REREAD_JQ,
    ]


def argv_issue_updated(repo: str, n: int) -> list[str]:
    """One read of the issue's ``updatedAt`` (after the poll's own write, 4.11 E1)."""
    return [
        "gh",
        "issue",
        "view",
        _issue_arg(n),
        "--repo",
        _repo_arg(repo),
        "--json",
        "updatedAt",
    ]


def argv_issue_labels(repo: str, n: int) -> list[str]:
    """The live label read that confirms a removal by hand (4.11 row 5)."""
    return [
        "gh",
        "issue",
        "view",
        _issue_arg(n),
        "--repo",
        _repo_arg(repo),
        "--json",
        "labels",
    ]


def argv_develop_list(repo: str, n: int) -> list[str]:
    """E2: the branches linked to the issue."""
    return [
        "gh",
        "issue",
        "develop",
        "--list",
        _issue_arg(n),
        "--repo",
        _repo_arg(repo),
    ]


def argv_branch_date(repo: str, name: str) -> list[str]:
    """E2: the date of the newest commit of a linked branch."""
    return [
        "gh",
        "api",
        "--method",
        "GET",
        f"repos/{_repo_arg(repo)}/branches/{_branch_arg(name)}",
        "--jq",
        BRANCH_JQ,
    ]


def argv_timeline(repo: str, n: int) -> list[str]:
    """E3: the issue's timeline, projected to the events that show a pull request."""
    return [
        "gh",
        "api",
        "--method",
        "GET",
        f"repos/{_repo_arg(repo)}/issues/{_issue_arg(n)}/timeline",
        "-F",
        f"per_page={PAGE_SIZE}",
        "--jq",
        TIMELINE_JQ,
    ]


def argv_label_get(repo: str) -> list[str]:
    """Read the hold label of ``repo`` (does it exist yet?)."""
    return [
        "gh",
        "api",
        "--method",
        "GET",
        f"repos/{_repo_arg(repo)}/labels/{HOLD_LABEL}",
    ]


def argv_label_create(repo: str) -> list[str]:
    """Create the hold label in ``repo`` (the first time the repo needs it)."""
    return [
        "gh",
        "api",
        "--method",
        "POST",
        f"repos/{_repo_arg(repo)}/labels",
        "-f",
        f"name={HOLD_LABEL}",
        "-f",
        f"color={_HOLD_LABEL_COLOR}",
        "-f",
        f"description={_HOLD_LABEL_TEXT}",
    ]


def argv_label_add(repo: str, n: int) -> list[str]:
    """Add the hold label to issue ``n`` of ``repo``."""
    return [
        "gh",
        "api",
        "--method",
        "POST",
        f"repos/{_repo_arg(repo)}/issues/{_issue_arg(n)}/labels",
        "-f",
        f"labels[]={HOLD_LABEL}",
    ]


def argv_label_remove(repo: str, n: int) -> list[str]:
    """Remove the hold label from issue ``n``: the one ``DELETE`` the poll may issue."""
    return [
        "gh",
        "api",
        "--method",
        "DELETE",
        f"repos/{_repo_arg(repo)}/issues/{_issue_arg(n)}/labels/{HOLD_LABEL}",
    ]


# --- reply classification (design 8.2) --------------------------------------

# [UNVERIFIED] gh stderr text (design 4.6 and 7.1). Kept in this ONE table so the
# live test can correct it in one place. The Project scope signs are gone: the
# poll reads no Project and no GraphQL.
GH_ERROR_SIGNS: dict[str, tuple[str, ...]] = {
    "auth_stderr": ("HTTP 401", "gh auth login"),
    "rate_status_stderr": ("HTTP 403", "HTTP 429"),
    "rate_text_stderr": ("rate limit",),  # matched case-insensitively
    "transient_stderr_re": (r"HTTP 5[0-9]{2}",),
}
"""Every stderr substring and regex ``classify`` matches."""


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
    if _any_in("auth_stderr", stderr):
        return Reply("auth_failed", result, None)
    rate_text = any(s in stderr.lower() for s in GH_ERROR_SIGNS["rate_text_stderr"])
    if _any_in("rate_status_stderr", stderr) and rate_text:
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
"""A search result at or above this count fails closed for S1 (spec 4.2)."""

_SHARED_REASONS = {
    "timeout": "gh_timeout",
    "transient": "gh_timeout",
    "non_json": "gh_non_json",
    "rate_limited": "rate_limited",
}
"""Cycle reason of a failed G1 or search reply; anything else is ``gh_auth_failed``."""


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


# --- typed reads: item parsers (DF-18 null rules) ----------------------------

_API_REPO = re.compile(r"https://api\.github\.com/repos/(?P<repo>[^/]+/[^/]+)")


def _row_repo(item: dict, owner: str) -> str | None:
    """The repo of a search row; None for a row outside ``owner`` (dropped).

    A ``repository_url`` of any other shape is malformed, so a reply that changed
    shape is never read as "no rows".
    """
    match = _API_REPO.fullmatch(_text(item.get("repository_url")))
    _check(match is not None and valid_repo(match["repo"]))
    repo = match["repo"]  # type: ignore[index]
    return repo if repo.split("/", 1)[0].lower() == owner.lower() else None


def _search_items(reply: Reply) -> list:
    """The ``items`` of a search reply; ``incomplete_results`` true is malformed."""
    body = _obj(reply.payload)
    _check(body.get("incomplete_results") is False)
    return _list(body.get("items"))


def _bool(value: object) -> bool:
    _check(type(value) is bool)
    return bool(value)


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


def search_assigned(
    runner: Runner, owner: str, login: str, timeout_for: Callable[[], float | None]
) -> Read:
    """S1: a tuple of ``DiscoveredIssue`` for one organisation (spec 4.2).

    ``DISCOVERY_BOUND`` or more rows give ``truncated`` (fail closed), a repeated
    (repo, number) ``discovery_duplicate`` and any malformed row ``non_json``. A
    row of another organisation is dropped; a row with a ``pull_request`` key is
    dropped (it is not an issue). Raises ``ValueError`` before any call for an
    ``owner`` or ``login`` that is unsafe as a command-line value.
    """
    reply = _call(runner, None, timeout_for, argv_search_assigned(owner, login))
    if reply is None:
        return _SHARED_NO_CALL
    if reply.kind != "ok":
        return _shared_failed(reply)
    issues: list[DiscoveredIssue] = []
    seen: set[tuple[str, int]] = set()
    try:
        items = _search_items(reply)
        total = _obj(reply.payload).get("total_count")
        _check(type(total) is int and total >= 0)
        if len(items) >= DISCOVERY_BOUND or total >= DISCOVERY_BOUND:
            return Read(None, "truncated", "truncated")
        for item in items:
            d = _obj(item)
            repo = _row_repo(d, owner)
            number = _pos_int(d.get("number"))
            _check(valid_issue_number(number))
            if repo is None or _bool(d.get("pull_request")):
                continue
            if (repo, number) in seen:
                return Read(None, "discovery_duplicate", "discovery_duplicate")
            seen.add((repo, number))
            issues.append(
                DiscoveredIssue(
                    repo=repo,
                    number=number,
                    labels=_texts(d.get("labels")),
                    assignees=_texts(d.get("assignees")),
                    state=_text(d.get("state")),
                    updated_at=_time(d.get("updated_at")),
                    title=_text(d.get("title")),
                    body=_text(d.get("body")),
                )
            )
    except _Malformed:
        return Read(None, "gh_non_json", "non_json")
    return Read(tuple(issues))


def search_info(
    runner: Runner,
    stream: str,
    owner: str,
    login: str,
    since: datetime,
    timeout_for: Callable[[], float | None],
) -> Read:
    """S2 to S4: a tuple of ``InfoItem``, cut at ``DISCOVERY_BOUND`` (a warning, not a stop).

    A row of another organisation is dropped. The reply shapes of the three
    information streams are UNVERIFIED until the live test (U8); the tests pin
    them with ``_assumed_shape`` fixtures.
    """
    reply = _call(
        runner, None, timeout_for, argv_search_info(stream, owner, login, since)
    )
    if reply is None:
        return _SHARED_NO_CALL
    if reply.kind != "ok":
        return _shared_failed(reply)
    found: list[InfoItem] = []
    seen: set[tuple[str, int]] = set()
    try:
        for item in _search_items(reply)[:DISCOVERY_BOUND]:
            d = _obj(item)
            repo = _row_repo(d, owner)
            number = _pos_int(d.get("number"))
            _check(valid_issue_number(number))
            is_pr = _bool(d.get("pull_request"))
            if repo is None or (repo, number) in seen:
                continue
            seen.add((repo, number))
            found.append(
                InfoItem(
                    stream=stream,
                    repo=repo,
                    number=number,
                    kind="pull_request" if is_pr else "issue",
                    updated_at=_time(d.get("updated_at")),
                )
            )
    except _Malformed:
        return Read(None, "gh_non_json", "non_json")
    return Read(tuple(found))


def reread(
    runner: Runner,
    budget: CallBudget,
    repo: str,
    n: int,
    timeout_for: Callable[[], float | None],
) -> Read:
    """An ``IssueSnapshot`` from one reserved call (the pre-wake re-read, 4.5 step 9).

    A timeout or 5xx is ``revalidation_transient``; any other failure, or a
    reply for another number, is ``revalidation_failed``.
    """
    reply = _call(runner, budget, timeout_for, argv_reread(repo, n), reserved=True)
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
            repo=repo,
            number=n,
            state=_text(d.get("state")),
            labels=_texts(d.get("labels")),
            assignees=_texts(d.get("assignees")),
            body=_text(d.get("body")),
        )
    except _Malformed:
        return Read(None, "revalidation_failed", "non_json")
    return Read(value)


def issue_updated_at(
    runner: Runner,
    budget: CallBudget,
    repo: str,
    n: int,
    timeout_for: Callable[[], float | None],
) -> Read:
    """The issue's ``updatedAt`` as a ``datetime`` (read once after the poll's own write)."""
    reply = _call(runner, budget, timeout_for, argv_issue_updated(repo, n))
    if reply is None:
        return _NO_CALL
    if reply.kind != "ok":
        return _failed(reply, "hold_write_failed")
    try:
        return Read(_time(_obj(reply.payload).get("updatedAt")))
    except _Malformed:
        return Read(None, "hold_write_failed", "non_json")


def issue_labels(
    runner: Runner,
    budget: CallBudget,
    repo: str,
    n: int,
    timeout_for: Callable[[], float | None],
) -> Read:
    """The live label names of the issue: one read that confirms a removal by hand."""
    reply = _call(runner, budget, timeout_for, argv_issue_labels(repo, n))
    if reply is None:
        return _NO_CALL
    if reply.kind != "ok":
        return _failed(reply, "revalidation_failed")
    try:
        return Read(_names(_obj(reply.payload).get("labels"), "name"))
    except _Malformed:
        return Read(None, "revalidation_failed", "non_json")


# --- evidence of plan work elsewhere (4.11 point 5, E2 and E3) -----------------


def linked_branches(
    runner: Runner,
    budget: CallBudget,
    repo: str,
    n: int,
    timeout_for: Callable[[], float | None],
) -> Read:
    """E2: the names of the branches linked to the issue (``gh issue develop --list``).

    The output is text, one branch per line, the name first (tab separated).
    [UNVERIFIED] until the live test; a line that is not a branch name is
    ignored. Exit 0 with no output is no branch.
    """
    timeout = timeout_for()
    if timeout is None or not budget.spend():
        return _NO_CALL
    result = runner.run(argv_develop_list(repo, n), timeout)
    if result.returncode != 0 or result.timed_out:
        return _failed(classify(result), "hold_write_failed")
    names: list[str] = []
    for text_line in result.stdout.splitlines():
        name = text_line.split("\t", 1)[0].strip()
        if (
            _BRANCH_NAME.fullmatch(name)
            and not name.startswith("-")
            and ".." not in name
            and name not in names
        ):
            names.append(name)
    return Read(tuple(names))


def branch_date(
    runner: Runner,
    budget: CallBudget,
    repo: str,
    name: str,
    timeout_for: Callable[[], float | None],
) -> Read:
    """E2: the date of the branch's newest commit, as a ``datetime``."""
    reply = _call(runner, budget, timeout_for, argv_branch_date(repo, name))
    if reply is None:
        return _NO_CALL
    if reply.kind != "ok":
        return _failed(reply, "hold_write_failed")
    try:
        return Read(_time(_obj(reply.payload).get("date")))
    except _Malformed:
        return Read(None, "hold_write_failed", "non_json")


def timeline_evidence(
    runner: Runner,
    budget: CallBudget,
    repo: str,
    n: int,
    timeout_for: Callable[[], float | None],
) -> Read:
    """E3: the newest time of a ``connected`` event or a ``cross-referenced`` pull request.

    The value is a ``datetime``, or None when the timeline shows none.
    """
    reply = _call(runner, budget, timeout_for, argv_timeline(repo, n))
    if reply is None:
        return _NO_CALL
    if reply.kind != "ok":
        return _failed(reply, "hold_write_failed")
    newest: datetime | None = None
    try:
        for item in _list(reply.payload):
            d = _obj(item)
            event = _text(d.get("event"))
            linked = event == "connected" or (
                event == "cross-referenced" and _bool(d.get("pull_request"))
            )
            when = _time(d.get("created_at"))
            if linked and (newest is None or when > newest):
                newest = when
    except _Malformed:
        return Read(None, "hold_write_failed", "non_json")
    return Read(newest)


# --- the label writer (4.11 point 2) ------------------------------------------


Guard = Callable[[list[str]], "str | None"]
"""A refusal check for one argv: the reason text to refuse it, None to allow it."""


class LabelWriter:
    """Create, add and remove the hold label: the poll's only GitHub writes.

    Each write returns a ``Read``: ``Read(True)`` when it is done and, when it is
    not, a ``Read`` whose ``reason`` is ``hold_write_failed`` (a refusal, a 403, a
    failed creation) or whose ``kind`` is ``rate_limited`` (the cycle backs off).
    There is no comment call here and no way to build one. ``guard`` is the
    injected refusal check of the orchestrator's limits (spec 5.9 N2); a refused
    argv is not run and counts as ``hold_write_failed``.
    """

    def __init__(self, runner: Runner, guard: Guard | None = None) -> None:
        self._runner = runner
        self._guard = guard
        self._ready: set[str] = set()

    def _run(
        self,
        budget: CallBudget,
        timeout_for: Callable[[], float | None],
        argv: list[str],
    ) -> Reply | None:
        if self._guard is not None and self._guard(list(argv)) is not None:
            return Reply(
                "failed",
                CommandResult(tuple(argv), None, "", "", False, None, 0.0),
                None,
            )
        return _call(self._runner, budget, timeout_for, argv)

    def _done(self, reply: Reply | None, *, absent_ok: bool = False) -> Read:
        if reply is None:
            return _NO_CALL
        if (
            absent_ok
            and reply.result.returncode != 0
            and "HTTP 404" in reply.result.stderr
        ):
            return Read(True)
        if reply.kind == "ok" or (
            reply.kind == "non_json" and reply.result.returncode == 0
        ):
            return Read(True)  # a write reply is not read; exit 0 is the result
        return _failed(reply, "hold_write_failed")

    def ensure(
        self,
        budget: CallBudget,
        repo: str,
        timeout_for: Callable[[], float | None],
    ) -> Read:
        """Read the hold label of ``repo``; create it when it is absent (once per cycle)."""
        if repo in self._ready:
            return Read(True)
        reply = self._run(budget, timeout_for, argv_label_get(repo))
        if reply is None:
            return _NO_CALL
        if reply.kind == "ok":
            self._ready.add(repo)
            return Read(True)
        if reply.result.returncode == 0 or "HTTP 404" not in reply.result.stderr:
            return _failed(reply, "hold_write_failed")
        made = self._done(self._run(budget, timeout_for, argv_label_create(repo)))
        if made.reason is None:
            self._ready.add(repo)
        return made

    def add(
        self,
        budget: CallBudget,
        repo: str,
        n: int,
        timeout_for: Callable[[], float | None],
    ) -> Read:
        """Add the hold label to issue ``n`` (the label must exist: call ``ensure`` first)."""
        return self._done(self._run(budget, timeout_for, argv_label_add(repo, n)))

    def remove(
        self,
        budget: CallBudget,
        repo: str,
        n: int,
        timeout_for: Callable[[], float | None],
    ) -> Read:
        """Remove the hold label; a label that is already gone (HTTP 404) is done."""
        reply = self._run(budget, timeout_for, argv_label_remove(repo, n))
        return self._done(reply, absent_ok=True)
