"""The wake: the wake file, its parser, the acknowledgment and the delivery (design section 3).

A wake has three artifacts and one id (3.1): the wake file (every fact), a
mailbox message to the target's Run (the id only) and a typed line (the id
only). This module writes and parses the first, reads the acknowledgment, and
delivers the other two with ``Waker``. It never decides which issue goes to
which orchestrator (``route``) and holds no store (``record``).

The session lookup is a port of the IronFlow script ``orca_term.py``
(``find_session`` by running process and tag, never by title; ``claude_processes``,
``typing_or_fresh``, ``is_idle``, ``send``, about 100 lines). It duplicates that
script on purpose; consolidating the two is a follow-up (design section 11).

Guarantees (3.7): no GitHub text reaches a typed line or a mailbox subject (the
line and the subject hold the wake id, built by ``launch.build_wake_line`` and a
pattern-checked id); the poll never writes ``.ack.json`` or ``.rejected.json``
and the orchestrator never writes the wake file; a wake of a dry run is never
written.
"""

from __future__ import annotations

import glob
import json
import os
import re
import secrets
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from . import launch, repos
from .predicates import (
    ORCHESTRATOR_ID_PATTERN,
    WAKE_ID_PATTERN,
    format_utc,
    parse_utc,
    valid_issue_number,
    valid_login,
    valid_repo,
)
from .runner import CommandResult, Runner

WAKE_SCHEMA = "orchestrator-wake/1"
ACK_SCHEMA = "orchestrator-wake-ack/1"
MAX_WAKE_BYTES = 64 * 1024
"""A wake file is at most 64 KiB (3.4)."""

MAX_ASSIGNED = 10
MAX_PLAN_REQUESTS = 10
"""``plan_requests[]`` has a maximum, like ``assigned[]`` (finding F5 of issue 675)."""
MAX_INFO = 50
MAX_SKIPPED = 100
MAX_ASSIGNEES = 10
PLAN_TITLE_MAX = 256
"""A plan request's title is 1 to 256 printable characters (finding F4 of issue 675)."""

CHECKOUT_STATES = ("ok", "missing", "origin_mismatch")
INFO_KINDS = ("issue", "pull_request")
MISSING_TOKENS = ("priority", "fix_approach", "test_plan")
RECEIPT_STAGES = ("input_accepted", "turn_started")
FRESH_OUTPUT_SECONDS = 60
"""A session with output newer than this is busy (DQ2, ``orca_term.py:13``)."""

WAKES_DIR = ".orchestrator/wakes"
_CYCLE_ID = re.compile(r"[0-9a-f]{32}")
_TOKEN = re.compile(r"[a-z][a-z0-9_]{0,39}")
_HOST = re.compile(r"[ -~]{1,255}")
_URL = re.compile(
    r"https://github\.com/[A-Za-z0-9._-]+/[A-Za-z0-9._-]+/issues/[1-9][0-9]{0,8}"
)


# --- the model ------------------------------------------------------------------


@dataclass(frozen=True)
class AssignedItem:
    """One issue given to the target as an assignment."""

    repo: str
    number: int
    assignees: tuple[str, ...]
    first_seen_at: datetime
    checkout_state: str


@dataclass(frozen=True)
class InfoRef:
    """One information item (S2 to S4)."""

    repo: str
    number: int
    kind: str
    updated_at: datetime


@dataclass(frozen=True)
class PlanRequestItem:
    """One plan request (4.11 point 5): the only place an issue title travels."""

    repo: str
    number: int
    title: str
    url: str
    missing: tuple[str, ...]
    held_since: datetime
    requested_at: datetime


@dataclass(frozen=True)
class SkippedItem:
    """An issue the poll skipped, with a reason of the closed list of 4.7."""

    repo: str
    number: int
    reason: str


@dataclass(frozen=True)
class WakeTarget:
    """The one orchestrator a wake is for (3.4 ``target``)."""

    orchestrator: str
    tag: str
    repo: str
    resume: bool = False


@dataclass(frozen=True)
class Wake:
    """The content of one wake file."""

    wake_id: str
    created_at: datetime
    cycle_id: str
    host: str
    login: str
    since: datetime
    gh_calls: int
    target: WakeTarget
    attempt: int
    assigned: tuple[AssignedItem, ...] = ()
    mentions: tuple[InfoRef, ...] = ()
    could_assign: tuple[InfoRef, ...] = ()
    affects: tuple[InfoRef, ...] = ()
    plan_requests: tuple[PlanRequestItem, ...] = ()
    skipped: tuple[SkippedItem, ...] = ()


class WakeError(Exception):
    """A wake file could not be built or written (the audit reason ``wake_write_failed``)."""


def new_wake_id(created_at: datetime, token: str | None = None) -> str:
    """``<UTC time>-<8 hex>`` of 3.1: the time of the cycle's first GitHub read and a random tail."""
    tail = secrets.token_hex(4) if token is None else token
    wake_id = f"{created_at.strftime('%Y%m%dT%H%M%SZ')}-{tail}"
    if WAKE_ID_PATTERN.fullmatch(wake_id) is None:
        raise ValueError("a wake id needs a UTC time and 8 hex digits")
    return wake_id


def clean_title(title: str) -> str:
    """A plan-request title: control characters become spaces, cut to ``PLAN_TITLE_MAX``.

    The title is data in the wake file only; it never reaches a typed line, a
    mailbox subject or a command line. An empty result becomes ``(no title)``.
    """
    text = "".join(" " if not c.isprintable() else c for c in title)
    text = " ".join(text.split())[:PLAN_TITLE_MAX].strip()
    return text or "(no title)"


def issue_url(repo: str, number: int) -> str:
    """The URL of an issue, built from the repo and number (never taken from GitHub text)."""
    if not valid_repo(repo) or not valid_issue_number(number):
        raise ValueError("invalid repo or issue number")
    return f"https://github.com/{repo}/issues/{number}"


def _info(items: tuple[InfoRef, ...]) -> list[dict]:
    return [
        {
            "repo": i.repo,
            "number": i.number,
            "kind": i.kind,
            "updated_at": format_utc(i.updated_at),
        }
        for i in items
    ]


def wake_to_json(wake: Wake) -> dict:
    """The JSON object of a wake file (3.4). Raises ``WakeError`` for a wake over a limit."""
    if len(wake.assigned) > MAX_ASSIGNED or len(wake.plan_requests) > MAX_PLAN_REQUESTS:
        raise WakeError("a wake holds at most 10 assigned items and 10 plan requests")
    if max(len(wake.mentions), len(wake.could_assign), len(wake.affects)) > MAX_INFO:
        raise WakeError("an info list holds at most 50 items")
    if len(wake.skipped) > MAX_SKIPPED:
        raise WakeError("skipped holds at most 100 items")
    if wake.target.resume and (wake.assigned or wake.plan_requests):
        raise WakeError("a resume wake has no items")
    return {
        "schema": WAKE_SCHEMA,
        "wake_id": wake.wake_id,
        "created_at": format_utc(wake.created_at),
        "poll": {
            "cycle_id": wake.cycle_id,
            "host": wake.host,
            "login": wake.login,
            "since": format_utc(wake.since),
            "gh_calls": wake.gh_calls,
            "dry_run": False,
        },
        "target": {
            "orchestrator": wake.target.orchestrator,
            "tag": wake.target.tag,
            "repo": wake.target.repo,
            "resume": wake.target.resume,
        },
        "attempt": wake.attempt,
        "assigned": [
            {
                "repo": a.repo,
                "number": a.number,
                "assignees": list(a.assignees),
                "first_seen_at": format_utc(a.first_seen_at),
                "checkout_state": a.checkout_state,
            }
            for a in wake.assigned
        ],
        "info": {
            "mentions": _info(wake.mentions),
            "could_assign": _info(wake.could_assign),
            "affects": _info(wake.affects),
        },
        "plan_requests": [
            {
                "repo": p.repo,
                "number": p.number,
                "title": p.title,
                "url": p.url,
                "missing": list(p.missing),
                "held_since": format_utc(p.held_since),
                "requested_at": format_utc(p.requested_at),
            }
            for p in wake.plan_requests
        ],
        "skipped": [
            {"repo": s.repo, "number": s.number, "reason": s.reason}
            for s in wake.skipped
        ],
    }


def _fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_wake_file(orchestrator_repo: Path, wake: Wake) -> Path:
    """Write ``<orchestrator-repo>/.orchestrator/wakes/<wake_id>.json`` (3.4).

    Temp file plus ``rename``, mode 0600, at most 64 KiB, before anything is
    sent. Raises ``WakeError`` for a wake over a limit or a failed write. The
    poll's dry run never calls this.
    """
    data = json.dumps(wake_to_json(wake), sort_keys=True, indent=2, ensure_ascii=True)
    raw = data.encode("ascii") + b"\n"
    if len(raw) > MAX_WAKE_BYTES:
        raise WakeError("the wake file would be over 64 KiB")
    directory = Path(orchestrator_repo) / WAKES_DIR
    path = directory / f"{wake.wake_id}.json"
    tmp = directory / f".{wake.wake_id}.json.tmp-{os.getpid()}"
    try:
        os.makedirs(directory, mode=0o700, exist_ok=True)
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        try:
            os.write(fd, raw)
            os.fsync(fd)
        finally:
            os.close(fd)
        os.replace(tmp, path)
        _fsync_dir(directory)
    except OSError:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise WakeError("the wake file could not be written") from None
    return path


# --- the parser (3.4 and 3.5; PR B's ``wake-check`` applies the same rules) -------


class WakeRejected(Exception):
    """The whole wake is rejected with a closed reason (3.5 table, rows 1 and 2)."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


REJECT_REASONS = (
    "missing",
    "too_large",
    "not_json",
    "schema_unsupported",
    "id_mismatch",
    "wrong_target",
)


@dataclass(frozen=True)
class ParsedWake:
    """A parsed wake: the wake, the items dropped as malformed and the keys ignored.

    ``rejected`` lists ``(index, "malformed_item")`` where ``index`` counts the
    ``assigned`` items first and the ``plan_requests`` after them.
    """

    wake: Wake
    rejected: tuple[tuple[int, str], ...] = ()
    warnings: tuple[str, ...] = field(default=())


_TOP = {
    "schema", "wake_id", "created_at", "poll", "target", "attempt", "assigned",
    "info", "plan_requests", "skipped",
}  # fmt: skip


def _time(value: object) -> datetime:
    return parse_utc(value)  # type: ignore[arg-type]


def _item_repo_number(d: object) -> tuple[str, int]:
    if not isinstance(d, dict) or not valid_repo(d.get("repo")):
        raise ValueError("bad repo")
    if not valid_issue_number(d.get("number")):
        raise ValueError("bad number")
    return d["repo"], d["number"]


def _assigned(d: object, target_repo: str) -> AssignedItem:
    repo, number = _item_repo_number(d)
    assert isinstance(d, dict)
    names = d.get("assignees")
    if (
        repo.lower() != target_repo.lower()  # repos.yaml may spell it differently
        or not isinstance(names, list)
        or not 1 <= len(names) <= MAX_ASSIGNEES
        or not all(valid_login(n) for n in names)
        or d.get("checkout_state") not in CHECKOUT_STATES
    ):
        raise ValueError("bad assigned item")
    return AssignedItem(
        repo, number, tuple(names), _time(d.get("first_seen_at")), d["checkout_state"]
    )


def _info_ref(d: object) -> InfoRef:
    repo, number = _item_repo_number(d)
    assert isinstance(d, dict)
    if d.get("kind") not in INFO_KINDS:
        raise ValueError("bad kind")
    return InfoRef(repo, number, d["kind"], _time(d.get("updated_at")))


def _plan(d: object) -> PlanRequestItem:
    repo, number = _item_repo_number(d)
    assert isinstance(d, dict)
    title, url, missing = d.get("title"), d.get("url"), d.get("missing")
    if (
        not isinstance(title, str)
        or not 1 <= len(title) <= PLAN_TITLE_MAX
        or not title.isprintable()
        or not isinstance(url, str)
        or _URL.fullmatch(url) is None
        or url != f"https://github.com/{repo}/issues/{number}"
        or not isinstance(missing, list)
        or not missing
        or not all(m in MISSING_TOKENS for m in missing)
        or len(set(missing)) != len(missing)
    ):
        raise ValueError("bad plan request")
    return PlanRequestItem(
        repo,
        number,
        title,
        url,
        tuple(missing),
        _time(d.get("held_since")),
        _time(d.get("requested_at")),
    )


def _skipped(d: object) -> SkippedItem:
    repo, number = _item_repo_number(d)
    assert isinstance(d, dict)
    reason = d.get("reason")
    if not isinstance(reason, str) or _TOKEN.fullmatch(reason) is None:
        raise ValueError("bad skip reason")
    return SkippedItem(repo, number, reason)


def parse_wake(
    data: bytes,
    file_name: str,
    *,
    own_id: str | None = None,
    own_tag: str | None = None,
) -> ParsedWake:
    """Apply every rule of 3.4 and the table of 3.5 to the bytes of a wake file.

    Raises ``WakeRejected`` with one closed reason for a wake that is over
    64 KiB (``too_large``), is not JSON (``not_json``), has another or no schema
    (``schema_unsupported``), has a ``wake_id`` that differs from ``file_name``
    (``id_mismatch``), or names another orchestrator or tag than ``own_id`` and
    ``own_tag`` (``wrong_target``; checked only when they are given). An item
    that fails its rule is dropped and listed in ``ParsedWake.rejected``; an
    unknown extra key is ignored and named in ``warnings``.
    """
    if len(data) > MAX_WAKE_BYTES:
        raise WakeRejected("too_large")
    try:
        raw = json.loads(data.decode("utf-8"))
    except (ValueError, RecursionError):
        raise WakeRejected("not_json") from None
    if not isinstance(raw, dict):
        raise WakeRejected("not_json")
    if raw.get("schema") != WAKE_SCHEMA:
        raise WakeRejected("schema_unsupported")
    wake_id = raw.get("wake_id")
    if (
        not isinstance(wake_id, str)
        or WAKE_ID_PATTERN.fullmatch(wake_id) is None
        or file_name != f"{wake_id}.json"
    ):
        raise WakeRejected("id_mismatch")
    try:
        target_raw = raw["target"]
        target = WakeTarget(
            orchestrator=target_raw["orchestrator"],
            tag=target_raw["tag"],
            repo=target_raw["repo"],
            resume=target_raw["resume"],
        )
        poll = raw["poll"]
        info = raw["info"]
        if (
            not isinstance(target.orchestrator, str)
            or ORCHESTRATOR_ID_PATTERN.fullmatch(target.orchestrator) is None
            or not isinstance(target.tag, str)
            or launch.TAG_PATTERN.fullmatch(target.tag) is None
            or not valid_repo(target.repo)
            or type(target.resume) is not bool
            or type(raw["attempt"]) is not int
            or not 1 <= raw["attempt"] <= 3
            or not isinstance(poll, dict)
            or _CYCLE_ID.fullmatch(poll.get("cycle_id", "")) is None
            or _HOST.fullmatch(poll.get("host", "")) is None
            or not valid_login(poll.get("login"))
            or type(poll.get("gh_calls")) is not int
            or poll["gh_calls"] < 0
            or poll.get("dry_run") is not False
            or not isinstance(info, dict)
        ):
            raise ValueError("bad header")
        created, since = _time(raw["created_at"]), _time(poll["since"])
        arrays = {name: raw[name] for name in ("assigned", "plan_requests", "skipped")}
        lists = {name: info[name] for name in ("mentions", "could_assign", "affects")}
    except (KeyError, TypeError, ValueError):
        raise WakeRejected("not_json") from None
    if not all(isinstance(v, list) for v in (*arrays.values(), *lists.values())):
        raise WakeRejected("not_json")
    if (
        len(arrays["assigned"]) > MAX_ASSIGNED
        or len(arrays["plan_requests"]) > MAX_PLAN_REQUESTS
        or len(arrays["skipped"]) > MAX_SKIPPED
        or any(len(v) > MAX_INFO for v in lists.values())
    ):
        raise WakeRejected("too_large")
    if (own_id is not None and target.orchestrator != own_id) or (
        own_tag is not None and target.tag != own_tag
    ):
        raise WakeRejected("wrong_target")

    rejected: list[tuple[int, str]] = []

    def keep(items: list, build: Callable, offset: int = 0) -> tuple:
        good = []
        for index, item in enumerate(items):
            try:
                good.append(build(item))
            except (ValueError, TypeError, KeyError):
                rejected.append((offset + index, "malformed_item"))
        return tuple(good)

    assigned = keep(arrays["assigned"], lambda d: _assigned(d, target.repo))
    plans = keep(arrays["plan_requests"], _plan, len(arrays["assigned"]))
    wake = Wake(
        wake_id=wake_id,
        created_at=created,
        cycle_id=poll["cycle_id"],
        host=poll["host"],
        login=poll["login"],
        since=since,
        gh_calls=poll["gh_calls"],
        target=target,
        attempt=raw["attempt"],
        assigned=assigned,
        mentions=keep(lists["mentions"], _info_ref),
        could_assign=keep(lists["could_assign"], _info_ref),
        affects=keep(lists["affects"], _info_ref),
        plan_requests=plans,
        skipped=keep(arrays["skipped"], _skipped),
    )
    extra = sorted(str(k) for k in set(raw) - _TOP)
    return ParsedWake(wake, tuple(rejected), tuple(extra))


# --- the acknowledgment (3.6) -----------------------------------------------------


@dataclass(frozen=True)
class Ack:
    """A read acknowledgment: what each entry of the wake was decided as."""

    wake_id: str
    taken: frozenset[tuple[str, int]]
    skipped: dict[tuple[str, int], str]
    rejected_indexes: tuple[int, ...]


def read_ack(orchestrator_repo: Path, wake_id: str) -> Ack | None:
    """Read ``<wake_id>.ack.json``; None when it is missing, unreadable or invalid.

    An acknowledgment the poll cannot trust leaves the entry ``woken``, so it is
    sent again after its 10 minutes. The poll never writes this file.
    """
    if WAKE_ID_PATTERN.fullmatch(wake_id) is None:
        return None
    path = Path(orchestrator_repo) / WAKES_DIR / f"{wake_id}.ack.json"
    try:
        data = path.read_bytes()
        if len(data) > MAX_WAKE_BYTES:
            return None
        raw = json.loads(data.decode("utf-8"))
        if (
            not isinstance(raw, dict)
            or raw.get("schema") != ACK_SCHEMA
            or raw.get("wake_id") != wake_id
        ):
            return None
        taken = frozenset(_item_repo_number(d) for d in raw.get("taken", []))
        skipped: dict[tuple[str, int], str] = {}
        for d in raw.get("skipped", []):
            reason = d.get("reason") if isinstance(d, dict) else None
            skipped[_item_repo_number(d)] = (
                reason
                if isinstance(reason, str) and _TOKEN.fullmatch(reason)
                else "unrecognized"
            )
        rejected = tuple(
            d["index"]
            for d in raw.get("rejected_items", [])
            if isinstance(d, dict) and type(d.get("index")) is int and d["index"] >= 0
        )
    except (OSError, ValueError, TypeError, AttributeError, RecursionError):
        return None
    return Ack(wake_id, taken, skipped, rejected)


def move_to_done(orchestrator_repo: Path, wake_id: str) -> None:
    """Move the wake file and its acknowledgment to ``wakes/done/``; never delete them."""
    if WAKE_ID_PATTERN.fullmatch(wake_id) is None:
        return
    base = Path(orchestrator_repo) / WAKES_DIR
    done = base / "done"
    try:
        os.makedirs(done, mode=0o700, exist_ok=True)
        for suffix in (".json", ".ack.json"):
            src = base / f"{wake_id}{suffix}"
            if src.exists():
                os.replace(src, done / src.name)
    except OSError:
        pass  # a file left in place is read again next cycle and is harmless


# --- the session lookup and the delivery (DQ2) --------------------------------------


def claude_processes(proc_root: str | os.PathLike[str] = "/proc") -> dict[str, str]:
    """``{ORCA_TERMINAL_HANDLE: CLAUDE_TOPIC or ""}`` for every readable running ``claude`` process.

    A terminal's title outlives the Claude that set it, so a live session is
    found by its running process, never by its title (``orca_term.py:31``).
    """
    found: dict[str, str] = {}
    for env_path in glob.glob(os.path.join(os.fspath(proc_root), "[0-9]*", "environ")):
        try:
            cmd = Path(env_path).with_name("cmdline").read_bytes().split(b"\0")[0]
            if not cmd.endswith(b"claude"):
                continue
            text = Path(env_path).read_bytes().decode(errors="replace")
        except OSError:
            continue
        env = dict(kv.split("=", 1) for kv in text.split("\0") if "=" in kv)
        if env.get("ORCA_TERMINAL_HANDLE"):
            found[env["ORCA_TERMINAL_HANDLE"]] = env.get("CLAUDE_TOPIC", "")
    return found


def _find(obj: object, key: str) -> object:
    """The first value of ``key`` anywhere in a nested Orca result."""
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        obj = list(obj.values())
    if isinstance(obj, list):
        for value in obj:
            got = _find(value, key)
            if got is not None:
                return got
    return None


def _reply(result: CommandResult) -> object | None:
    """The ``result`` of an Orca ``--json`` reply, or None when the call failed."""
    if result.timed_out or result.spawn_error is not None or result.returncode != 0:
        return None
    try:
        out = json.loads(result.stdout)
    except (ValueError, RecursionError):
        return None
    if isinstance(out, dict):
        return None if out.get("ok", True) is False else out.get("result", out)
    return None


@dataclass(frozen=True)
class WakeTargetRun:
    """What the poll knows about the target's session when it delivers a wake."""

    orchestrator: str
    tag: str
    workspace: Path
    run_id: str | None
    tier: str


@dataclass(frozen=True)
class WakeOutcome:
    """What one delivery did: ``woken``, ``unknown``, ``no_session`` or ``spawn_error``."""

    kind: str
    detail: str
    mailbox: str = "skipped"  # sent | skipped | unavailable
    typed: bool = False
    stages: tuple[str, ...] = ()
    started: bool = False
    tier: str | None = None
    fallback_from: str | None = None


class Waker:
    """The real delivery of a wake: the mailbox message, the typed line, the session start.

    ``now`` for the idle rules comes from the cycle's clock (a parameter of
    ``deliver``), never from here. ``proc_root``, ``sleep`` and ``monotonic`` are
    injected so a test reads no real ``/proc`` and never waits.
    """

    def __init__(
        self,
        runner: Runner,
        launcher: launch.Launcher | None = None,
        *,
        proc_root: str | os.PathLike[str] = "/proc",
        sleep: Callable[[float], None] = time.sleep,
        monotonic: Callable[[], float] = time.monotonic,
    ) -> None:
        self._runner = runner
        self._proc_root = proc_root
        self._launcher = launcher or launch.OrcaLauncher(
            runner,
            lambda: claude_processes(proc_root),
            sleep=sleep,
            monotonic=monotonic,
        )

    # -- the Orca calls --------------------------------------------------------------

    def _orca(self, argv: list[str], timeout: float) -> object | None:
        return _reply(self._runner.run(argv, timeout))

    def _terminals(
        self, orca: str, workspace: Path, timeout: float
    ) -> list[dict] | None:
        """The connected terminals of the workspace; None when the list is cut short or unreadable."""
        res = self._orca(
            [orca, "terminal", "list", "--worktree", f"path:{workspace}", "--json"],
            timeout,
        )
        if not isinstance(res, dict) or res.get("truncated"):
            return (
                None  # a truncated list could hide a terminal: never a partial answer
            )
        terminals = res.get("terminals")
        if not isinstance(terminals, list):
            return None
        return [
            t
            for t in terminals
            if isinstance(t, dict)
            and t.get("connected")
            and isinstance(t.get("handle"), str)
        ]

    def find_session(
        self, orca: str, workspace: Path, tag: str, timeout: float
    ) -> list[dict] | None:
        """The terminals of the workspace that run Claude under ccsession tag ``tag``, newest output first.

        None when the terminal list could not be read (the poll then does not
        start a second session).
        """
        terminals = self._terminals(orca, workspace, timeout)
        if terminals is None:
            return None
        procs = claude_processes(self._proc_root)
        live = [t for t in terminals if procs.get(t["handle"]) == tag]
        return sorted(live, key=lambda t: -(t.get("lastOutputAt") or 0))

    def _unsafe(
        self, orca: str, term: dict, now: datetime, timeout: float
    ) -> str | None:
        """Why it is unsafe to type now, or None (``orca_term.typing_or_fresh``)."""
        res = self._orca(
            [
                orca,
                "terminal",
                "read",
                "--terminal",
                term["handle"],
                "--screen",
                "--json",
            ],
            timeout,
        )
        if res is None:
            return "screen_unreadable"
        draft = _find(res, "draft")
        if not isinstance(draft, str):
            return "screen_unreadable"  # an empty draft must be seen, not assumed (DQ2)
        if draft.strip():
            return "typing"
        last = (term.get("lastOutputAt") or 0) / 1000
        if last and now.timestamp() - last < FRESH_OUTPUT_SECONDS:
            return "fresh_output"
        return None

    def _idle(self, orca: str, handle: str, wait_ms: int = 4000) -> bool:
        """True when the agent's interface is idle; a timeout or error counts as not idle."""
        res = self._orca(
            [orca, "terminal", "wait", "--terminal", handle, "--for", "tui-idle",
             "--timeout-ms", str(wait_ms), "--json"],
            wait_ms / 1000 + 30,
        )  # fmt: skip
        return bool(_find(res, "satisfied")) if res is not None else False

    def _type_line(
        self, orca: str, handle: str, wake_id: str
    ) -> tuple[bool, tuple[str, ...]]:
        """Type ``/sc:orchestrator --wake <id>``; ``(accepted, stages)``."""
        line = launch.build_wake_line(wake_id)
        res = self._orca(
            [orca, "terminal", "send", "--terminal", handle, "--text", line,
             "--enter", "--wait-submit", "15", "--json"],
            75,
        )  # fmt: skip
        if res is None:
            return False, ()
        stages = _find(res, "stages")
        got = (
            tuple(s for s in stages if s in RECEIPT_STAGES)
            if isinstance(stages, list)
            else ()
        )
        accepted = _find(res, "accepted")
        return bool(accepted) or "input_accepted" in got, got

    def _mailbox(self, orca: str, run_id: str, wake_id: str, timeout: float) -> bool:
        """The mailbox message to the target's Run (3.3); True when Orca accepted it."""
        payload = json.dumps(
            {"kind": "orchestrator-wake", "wake_id": wake_id}, separators=(",", ":")
        )
        result = self._runner.run(
            [orca, "orchestration", "send", "--to", f"run:{run_id}", "--type", "status",
             "--subject", f"orchestrator-wake {wake_id}", "--payload", payload, "--json"],
            timeout,
        )  # fmt: skip
        return _reply(result) is not None

    # -- the delivery ---------------------------------------------------------------

    def deliver(
        self,
        orca: str,
        target: WakeTargetRun,
        wake_id: str,
        now: datetime,
        timeout: float,
        *,
        start_session: bool = True,
    ) -> WakeOutcome:
        """Send the mailbox message, then type the line when the session is idle.

        With ``start_session`` False (an information-only wake) a missing session
        is not started: the outcome is ``no_session`` and nothing else happens.

        Session missing: start one (the tier falls once to the next listed tier,
        5.8 point 4) and type the line once it is idle. ``woken`` when the
        mailbox or the typed line was accepted; ``unknown`` when neither was (the
        entry is sent again after 10 minutes); ``no_session`` when no session
        could be started; ``spawn_error`` when the start could not even begin.
        """
        if not isinstance(wake_id, str) or WAKE_ID_PATTERN.fullmatch(wake_id) is None:
            raise ValueError("wake_id must match the wake id pattern")
        mailbox = "skipped"
        if target.run_id is not None:
            mailbox = (
                "sent"
                if self._mailbox(orca, target.run_id, wake_id, timeout)
                else "unavailable"
            )
        live = self.find_session(orca, target.workspace, target.tag, timeout)
        if live is None:
            return WakeOutcome("unknown", "terminal_list", mailbox)
        started = False
        tier: str | None = None
        fallback: str | None = None
        if live:
            handle = live[0]["handle"]
            unsafe = self._unsafe(orca, live[0], now, timeout)
            if unsafe is not None or not self._idle(orca, handle):
                kind = "woken" if mailbox == "sent" else "unknown"
                return WakeOutcome(kind, unsafe or "busy", mailbox)
        else:
            if not start_session:
                return WakeOutcome("no_session", "not_started", mailbox)
            listed = repos.listed_tiers(self._runner, timeout)
            if listed is None:
                return WakeOutcome("no_session", "tiers_unreadable", mailbox)
            tier, fallback = repos.resolve_tier(target.tier, listed)
            if tier is None:
                return WakeOutcome(
                    "no_session", "no_tier", mailbox, fallback_from=fallback
                )
            outcome = self._launcher.start(
                orca, target.workspace, target.tag, tier, timeout
            )
            if outcome.kind == "spawn_error":
                return WakeOutcome(
                    "spawn_error",
                    outcome.detail,
                    mailbox,
                    tier=tier,
                    fallback_from=fallback,
                )
            if outcome.kind != "ready" or outcome.handle is None:
                return WakeOutcome(
                    "no_session",
                    outcome.detail,
                    mailbox,
                    tier=tier,
                    fallback_from=fallback,
                )
            started = True
            handle = outcome.handle
            # A new Claude may still be loading; a later attempt finds it live.
            if not self._idle(orca, handle, wait_ms=90000):
                return WakeOutcome(
                    "unknown",
                    "starting",
                    mailbox,
                    started=True,
                    tier=tier,
                    fallback_from=fallback,
                )
        accepted, stages = self._type_line(orca, handle, wake_id)
        kind = "woken" if accepted or mailbox == "sent" else "unknown"
        return WakeOutcome(
            kind,
            "typed" if accepted else "not_typed",
            mailbox,
            typed=accepted,
            stages=stages,
            started=started,
            tier=tier,
            fallback_from=fallback,
        )

    def mark_unread(
        self, orca: str, workspace: Path, reason: str, timeout: float
    ) -> bool:
        """Mark the orchestrator workspace unread with a fixed note (DQ2); True when Orca took it.

        ``reason`` is a key of the closed reason table; the note holds no text
        from GitHub.
        """
        if not isinstance(reason, str) or _TOKEN.fullmatch(reason) is None:
            raise ValueError("reason must be a reason token")
        return (
            self._orca(
                [orca, "worktree", "set", "--worktree", f"path:{workspace}", "--unread",
                 "--comment", f"issue-watch: {reason}", "--json"],
                timeout,
            )
            is not None
        )  # fmt: skip


__all__ = [
    "ACK_SCHEMA",
    "WAKE_SCHEMA",
    "Ack",
    "AssignedItem",
    "InfoRef",
    "ParsedWake",
    "PlanRequestItem",
    "SkippedItem",
    "Wake",
    "WakeError",
    "WakeOutcome",
    "WakeRejected",
    "WakeTarget",
    "WakeTargetRun",
    "Waker",
    "claude_processes",
    "clean_title",
    "issue_url",
    "move_to_done",
    "new_wake_id",
    "parse_wake",
    "read_ack",
    "wake_to_json",
    "write_wake_file",
]
