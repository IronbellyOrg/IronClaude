"""Dispatch record of the issue watcher (design 4.3, 4.10 and 4.11, ``dispatch.json``).

Schema 2. Times are aware UTC datetimes in memory and ``YYYY-MM-DDTHH:MM:SSZ``
strings on disk. An entry is keyed ``owner/repo#N`` (a string). This module
never reads the wall clock (every time is a ``now`` parameter), never runs a
command, and imports only the standard library and ``predicates`` at module
level.

The store holds three kinds of fact: the ``entries`` (one per issue the poll
has seen and routed or recorded), the ``holds`` (one per issue that carries the
label ``hold:plan``, with the delivery state of its plan request) and the
bookkeeping of the cycle (``info_seen``, ``last_poll_at``, ``rate_streak``,
``baseline``, ``consumed_log``).

Deviations from the field list of design 4.10 and 4.11, each for a stated reason:

* ``launches`` is not kept: ``wake_attempts`` (0 to 3) replaces it, because an
  entry is now woken up to three times.
* ``Hold`` has the extra fields ``plan_wake_id``, ``plan_attempts`` and
  ``plan_woken_at`` (the delivery bookkeeping that rule 4 of 4.3 needs for a
  plan request) and ``evidence_kind`` (the signal that holds the issue, which
  ``status`` prints, K26). ``plan_request`` also has the state ``skipped`` (an
  orchestrator acknowledged the request as ``skipped``; it ends the count of
  the place, finding F21 of issue 675).
* ``StoreDoc.baseline`` is True from ``init_state`` until the first completed
  cycle has recorded every issue already assigned (4.3 rule 5).
"""

from __future__ import annotations

import json
import os
import re
import stat
from collections.abc import Callable, Iterable, Iterator, Mapping
from contextlib import AbstractContextManager, contextmanager
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import NamedTuple, Protocol

from superclaude.cli.issue_watch.predicates import (
    ACK_REASON_PATTERN,
    ORCHESTRATOR_ID_PATTERN,
    WAKE_ID_PATTERN,
    format_utc,
    issue_key,
    parse_utc,
    split_issue_key,
    valid_issue_number,
    valid_operation_id,
    valid_repo,
)

SCHEMA_VERSION = 2
"""Store schema version this module reads and writes."""

ENTRY_STATES = frozenset(
    {"pending", "woken", "acked", "unknown", "failed", "abandoned"}
)
"""The six entry states of design 4.10."""

HOLD_STATES = frozenset({"held", "hand_removed"})
PLAN_REQUEST_STATES = frozenset(
    {"pending", "woken", "acked", "skipped", "abandoned", "stuck"}
)
EVIDENCE_KINDS = frozenset({"edit", "branch", "pull_request", "session"})
MISSING_TOKENS = ("priority", "fix_approach", "test_plan")
INFO_STREAMS = ("mentions", "could_assign", "affects")
MAX_INFO_SEEN = 500
"""The newest ``info_seen`` keys the store keeps (4.3 rule 3)."""


class StoreError(Exception):
    """The store cannot be used; ``reason`` is a closed audit reason."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class LockHeld(Exception):
    """Another process holds the store lock (exit 75 ``lock_held``)."""


class LockError(Exception):
    """The lock file is missing or unsafe; ``reason`` is a closed audit reason."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class TransitionError(Exception):
    """A (state, trigger) pair that no transition row allows."""


class StateExists(Exception):
    """``init_state`` found an existing store and refused to replace it."""


@dataclass(frozen=True)
class Entry:
    """One issue's dispatch entry; every field is always present (None = null)."""

    repo: str
    issue: int
    state: str
    attempts: int
    wake_attempts: int
    operation_id: str | None
    wake_id: str | None
    woken_at: datetime | None
    ack_reason: str | None
    orchestrator: str | None
    consumed_at: datetime | None
    pending_at: datetime | None
    created_at: datetime
    updated_at: datetime
    lease_expires_at: datetime | None
    last_reason: str | None

    @property
    def key(self) -> str:
        """The store key ``owner/repo#N``."""
        return issue_key(self.repo, self.issue)


@dataclass(frozen=True)
class Hold:
    """One held issue (design 4.11 point 6)."""

    state: str
    first_held_at: datetime
    seen_updated_at: datetime | None = None
    last_evidence_at: datetime | None = None
    evidence_kind: str | None = None
    plan_requested_at: datetime | None = None
    plan_request_orchestrator: str | None = None
    plan_request: str | None = None
    plan_acked_at: datetime | None = None
    plan_wake_id: str | None = None
    plan_attempts: int = 0
    plan_woken_at: datetime | None = None
    missing: tuple[str, ...] = ()


@dataclass(frozen=True)
class StoreDoc:
    """The whole ``dispatch.json`` document."""

    schema_version: int
    created_at: datetime
    next_permitted_at: datetime | None
    last_completed_cycle_at: datetime | None
    last_poll_at: datetime | None
    rate_streak: int
    baseline: bool
    info_seen: tuple[str, ...]
    consumed_log: tuple[datetime, ...]
    entries: Mapping[str, Entry]
    holds: Mapping[str, Hold]


_STORE_KEYS = frozenset(
    {
        "schema_version",
        "created_at",
        "next_permitted_at",
        "last_completed_cycle_at",
        "last_poll_at",
        "rate_streak",
        "baseline",
        "info_seen",
        "consumed_log",
        "entries",
        "holds",
    }
)
_ENTRY_KEYS = frozenset(Entry.__dataclass_fields__)
_HOLD_KEYS = frozenset(Hold.__dataclass_fields__)
_INFO_SEEN = re.compile(
    r"(mentions|could_assign|affects) [^ #]+#[1-9][0-9]{0,8} "
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z"
)


def _invalid() -> StoreError:
    return StoreError("store_invalid")


def _is_int(value: object) -> bool:
    return type(value) is int


def _time(value: object) -> datetime:
    try:
        return parse_utc(value)  # type: ignore[arg-type]
    except ValueError:
        raise _invalid() from None


def _opt_time(value: object) -> datetime | None:
    return None if value is None else _time(value)


def _opt(value: object, check: Callable[[object], bool]) -> None:
    if value is not None and not check(value):
        raise _invalid()


def _pattern(pattern: re.Pattern[str]) -> Callable[[object], bool]:
    return lambda v: isinstance(v, str) and pattern.fullmatch(v) is not None


def _key(key: object) -> tuple[str, int]:
    try:
        return split_issue_key(key)
    except ValueError:
        raise _invalid() from None


def _entry(key: object, raw: object) -> Entry:
    repo, number = _key(key)
    if not isinstance(raw, dict) or set(raw) != _ENTRY_KEYS:
        raise _invalid()
    if raw["repo"] != repo or raw["issue"] != number or not valid_issue_number(number):
        raise _invalid()
    if not isinstance(raw["state"], str) or raw["state"] not in ENTRY_STATES:
        raise _invalid()
    if not _is_int(raw["attempts"]) or raw["attempts"] < 0:
        raise _invalid()
    if not _is_int(raw["wake_attempts"]) or not 0 <= raw["wake_attempts"] <= 3:
        raise _invalid()
    _opt(raw["last_reason"], lambda v: isinstance(v, str))
    _opt(raw["operation_id"], valid_operation_id)
    _opt(raw["wake_id"], _pattern(WAKE_ID_PATTERN))
    _opt(raw["ack_reason"], _pattern(ACK_REASON_PATTERN))
    _opt(raw["orchestrator"], _pattern(ORCHESTRATOR_ID_PATTERN))
    entry = Entry(
        repo=repo,
        issue=number,
        state=raw["state"],
        attempts=raw["attempts"],
        wake_attempts=raw["wake_attempts"],
        operation_id=raw["operation_id"],
        wake_id=raw["wake_id"],
        woken_at=_opt_time(raw["woken_at"]),
        ack_reason=raw["ack_reason"],
        orchestrator=raw["orchestrator"],
        consumed_at=_opt_time(raw["consumed_at"]),
        pending_at=_opt_time(raw["pending_at"]),
        created_at=_time(raw["created_at"]),
        updated_at=_time(raw["updated_at"]),
        lease_expires_at=_opt_time(raw["lease_expires_at"]),
        last_reason=raw["last_reason"],
    )
    if entry.state == "pending" and (
        entry.orchestrator is None
        or entry.consumed_at is None
        or entry.pending_at is None
    ):
        raise _invalid()
    if entry.state == "woken" and (
        entry.orchestrator is None
        or entry.wake_id is None
        or entry.woken_at is None
        or entry.wake_attempts < 1
    ):
        raise _invalid()
    if entry.state == "failed" and entry.wake_attempts != 0:
        raise _invalid()
    return entry


def _hold(key: object, raw: object) -> Hold:
    _key(key)
    if not isinstance(raw, dict) or set(raw) != _HOLD_KEYS:
        raise _invalid()
    if raw["state"] not in HOLD_STATES:
        raise _invalid()
    _opt(raw["plan_request"], lambda v: v in PLAN_REQUEST_STATES)
    _opt(raw["evidence_kind"], lambda v: v in EVIDENCE_KINDS)
    _opt(raw["plan_request_orchestrator"], _pattern(ORCHESTRATOR_ID_PATTERN))
    _opt(raw["plan_wake_id"], _pattern(WAKE_ID_PATTERN))
    if not _is_int(raw["plan_attempts"]) or not 0 <= raw["plan_attempts"] <= 3:
        raise _invalid()
    missing = raw["missing"]
    if (
        not isinstance(missing, list)
        or len(set(missing)) != len(missing)
        or any(m not in MISSING_TOKENS for m in missing)
    ):
        raise _invalid()
    hold = Hold(
        state=raw["state"],
        first_held_at=_time(raw["first_held_at"]),
        seen_updated_at=_opt_time(raw["seen_updated_at"]),
        last_evidence_at=_opt_time(raw["last_evidence_at"]),
        evidence_kind=raw["evidence_kind"],
        plan_requested_at=_opt_time(raw["plan_requested_at"]),
        plan_request_orchestrator=raw["plan_request_orchestrator"],
        plan_request=raw["plan_request"],
        plan_acked_at=_opt_time(raw["plan_acked_at"]),
        plan_wake_id=raw["plan_wake_id"],
        plan_attempts=raw["plan_attempts"],
        plan_woken_at=_opt_time(raw["plan_woken_at"]),
        missing=tuple(missing),
    )
    if (hold.plan_requested_at is None) != (hold.plan_request is None):
        raise _invalid()
    if hold.plan_request is not None and hold.plan_request_orchestrator is None:
        raise _invalid()
    return hold


def validate(raw: object) -> StoreDoc:
    """Check a parsed ``dispatch.json`` and convert it.

    Raises ``StoreError("store_invalid")`` on any deviation: a key set that is
    not exact at any level, a wrong type, an entry whose repo or number differ
    from its key, a time string that is not ``YYYY-MM-DDTHH:MM:SSZ``, or a
    ``schema_version`` other than ``SCHEMA_VERSION`` (run ``migrate`` first).
    ``last_reason`` is checked as a ``str`` or null only; its membership in the
    reason table is pinned by the tests, because this module may not import
    ``audit``.
    """
    if not isinstance(raw, dict) or set(raw) != _STORE_KEYS:
        raise _invalid()
    if not _is_int(raw["schema_version"]) or raw["schema_version"] != SCHEMA_VERSION:
        raise _invalid()
    entries, holds = raw["entries"], raw["holds"]
    info_seen, consumed_log = raw["info_seen"], raw["consumed_log"]
    if not isinstance(entries, dict) or not isinstance(holds, dict):
        raise _invalid()
    if not isinstance(info_seen, list) or not isinstance(consumed_log, list):
        raise _invalid()
    if len(info_seen) > MAX_INFO_SEEN or not all(
        isinstance(k, str) and _INFO_SEEN.fullmatch(k) for k in info_seen
    ):
        raise _invalid()
    if not _is_int(raw["rate_streak"]) or raw["rate_streak"] < 0:
        raise _invalid()
    if type(raw["baseline"]) is not bool:
        raise _invalid()
    return StoreDoc(
        schema_version=raw["schema_version"],
        created_at=_time(raw["created_at"]),
        next_permitted_at=_opt_time(raw["next_permitted_at"]),
        last_completed_cycle_at=_opt_time(raw["last_completed_cycle_at"]),
        last_poll_at=_opt_time(raw["last_poll_at"]),
        rate_streak=raw["rate_streak"],
        baseline=raw["baseline"],
        info_seen=tuple(info_seen),
        consumed_log=tuple(_time(t) for t in consumed_log),
        entries={k: _entry(k, v) for k, v in entries.items()},
        holds={k: _hold(k, v) for k, v in holds.items()},
    )


def _drop_version_1(doc: dict) -> dict:
    """``MIGRATIONS[1]``: a version-1 store is dropped (it never ran live).

    The result is an empty version-2 store that keeps ``created_at`` and asks
    for the baseline, so nobody is woken for an issue that is already assigned.
    """
    created = doc.get("created_at")
    if not isinstance(created, str):
        raise _invalid()
    return {
        "schema_version": 2,
        "created_at": created,
        "next_permitted_at": None,
        "last_completed_cycle_at": None,
        "last_poll_at": None,
        "rate_streak": 0,
        "baseline": True,
        "info_seen": [],
        "consumed_log": [],
        "entries": {},
        "holds": {},
    }


MIGRATIONS: dict[int, Callable[[dict], dict]] = {1: _drop_version_1}
"""Version v -> pure function producing the v + 1 document."""


def migrate(
    doc: object, migrations: Mapping[int, Callable[[dict], dict]] = MIGRATIONS
) -> dict:
    """Return ``doc`` raised to ``SCHEMA_VERSION`` by chaining ``migrations``.

    A document already at ``SCHEMA_VERSION`` is returned as is; this function
    never mutates ``doc``. A ``schema_version`` that is not an ``int``, is
    higher than ``SCHEMA_VERSION`` or has no registered step, or a step whose
    result is not a dict at the next version, raises
    ``StoreError("store_invalid")``. ``migrations`` is the test seam.
    """
    if not isinstance(doc, dict):
        raise _invalid()
    version = doc.get("schema_version")
    if not _is_int(version) or version > SCHEMA_VERSION:
        raise _invalid()
    while version < SCHEMA_VERSION:
        step = migrations.get(version)
        if step is None:
            raise _invalid()
        doc = step(doc)
        version += 1
        if not isinstance(doc, dict) or not _is_int(doc.get("schema_version")):
            raise _invalid()
        if doc["schema_version"] != version:
            raise _invalid()
    return doc


STORE_FILE = "dispatch.json"
LOCK_FILE = "lock"
DISABLED_FILE = "DISABLED"


def _opt_utc(value: datetime | None) -> str | None:
    return None if value is None else format_utc(value)


def _entry_raw(entry: Entry) -> dict:
    return {
        key: format_utc(value) if isinstance(value, datetime) else value
        for key, value in asdict(entry).items()
    }


def _hold_raw(hold: Hold) -> dict:
    raw = {
        key: format_utc(value) if isinstance(value, datetime) else value
        for key, value in asdict(hold).items()
    }
    raw["missing"] = list(hold.missing)
    return raw


def _to_raw(doc: StoreDoc) -> dict:
    """Return ``doc`` as the JSON-ready dict ``validate`` accepts (round trip)."""
    return {
        "schema_version": doc.schema_version,
        "created_at": format_utc(doc.created_at),
        "next_permitted_at": _opt_utc(doc.next_permitted_at),
        "last_completed_cycle_at": _opt_utc(doc.last_completed_cycle_at),
        "last_poll_at": _opt_utc(doc.last_poll_at),
        "rate_streak": doc.rate_streak,
        "baseline": doc.baseline,
        "info_seen": list(doc.info_seen),
        "consumed_log": [format_utc(t) for t in doc.consumed_log],
        "entries": {k: _entry_raw(e) for k, e in doc.entries.items()},
        "holds": {k: _hold_raw(h) for k, h in doc.holds.items()},
    }


def _fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


class Store(Protocol):
    """The dispatch-record seam (``CrashingStore`` wraps it in the tests)."""

    state_dir: Path

    def load(self) -> StoreDoc: ...

    def save(self, doc: StoreDoc) -> None: ...

    def lock(self) -> AbstractContextManager[None]: ...

    def disabled(self) -> bool: ...

    def disabled_since(self) -> datetime | None: ...


class FileStore:
    """``Store`` over the files of ``state_dir``."""

    def __init__(
        self,
        state_dir: Path,
        migrations: Mapping[int, Callable[[dict], dict]] | None = None,
    ) -> None:
        self.state_dir = Path(state_dir)
        self.migrations = MIGRATIONS if migrations is None else migrations
        # True after a load that migrated a lower version; load never saves (DF-17).
        self.migrated = False

    def load(self) -> StoreDoc:
        """Read, migrate in memory and validate ``dispatch.json``; never writes.

        Raises ``StoreError("store_missing")`` for a missing file and
        ``StoreError("store_invalid")`` for an unreadable, unparseable or invalid
        one (NFR-011). ``migrated`` tells the caller whether a save is due.
        """
        self.migrated = False
        try:
            data = (self.state_dir / STORE_FILE).read_bytes()
        except FileNotFoundError:
            raise StoreError("store_missing") from None
        except OSError:
            raise _invalid() from None
        try:
            raw = json.loads(data)
            version = raw.get("schema_version") if isinstance(raw, dict) else None
            doc = validate(migrate(raw, self.migrations))
        except (ValueError, RecursionError):  # deep nesting is a RecursionError
            raise _invalid() from None
        self.migrated = version != SCHEMA_VERSION
        return doc

    def save(self, doc: StoreDoc) -> None:
        """Write ``doc`` atomically, force mode 0600, then fsync ``state_dir``."""
        from superclaude.cli.swarm.atomic import write_prepared_bytes  # C18

        text = json.dumps(_to_raw(doc), sort_keys=True, indent=2, ensure_ascii=True)
        path = self.state_dir / STORE_FILE
        write_prepared_bytes(path, text.encode() + b"\n")
        os.chmod(path, 0o600)
        _fsync_dir(self.state_dir)

    @contextmanager
    def lock(self) -> Iterator[None]:
        """Hold an exclusive ``flock`` on ``state_dir/lock``.

        Raises ``LockError("lock_missing")``, ``LockError("lock_invalid")`` or
        ``LockHeld``. The lock is released and its descriptor closed in a
        ``finally``, so a ``SystemExit`` passing through the ``with`` leaves the
        lock free for the next run (DF-15).
        """
        import fcntl  # not at module level: importing the package must work off Linux

        path = self.state_dir / LOCK_FILE
        try:
            fd = os.open(path, os.O_RDWR | os.O_NOFOLLOW | os.O_CLOEXEC)
        except FileNotFoundError:
            raise LockError("lock_missing") from None
        except OSError:  # a directory, a symlink (ELOOP), no permission, ...
            raise LockError("lock_invalid") from None
        try:
            st = os.fstat(fd)
            if not stat.S_ISREG(st.st_mode) or st.st_uid != os.geteuid():
                raise LockError("lock_invalid")
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise LockHeld() from None
            try:
                try:
                    ps = os.stat(path, follow_symlinks=False)
                except FileNotFoundError:
                    raise LockHeld() from None
                if (ps.st_dev, ps.st_ino) != (st.st_dev, st.st_ino):
                    raise LockHeld()
                if os.fstat(fd).st_nlink == 0:
                    raise LockHeld()
                yield
            finally:
                fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)

    def disabled(self) -> bool:
        """True while ``state_dir/DISABLED`` exists (a dangling symlink counts)."""
        return os.path.lexists(self.state_dir / DISABLED_FILE)

    def disabled_since(self) -> datetime | None:
        """The ``DISABLED`` file's mtime as an aware UTC datetime, or None."""
        try:
            mtime = os.stat(self.state_dir / DISABLED_FILE).st_mtime
        except FileNotFoundError:
            return None
        return datetime.fromtimestamp(mtime, tz=timezone.utc)


MAX_ATTEMPTS = 3
"""Pre-pending failures after which an entry is ``abandoned`` (T-3)."""

MAX_WAKE_ATTEMPTS = 3
"""Deliveries of one wake: the first send and two more (4.3 rule 4)."""

BACKOFF = timedelta(minutes=10)
"""Wait after a ``failed`` write before the issue is eligible again (T-2)."""

LEASE = timedelta(minutes=10)
"""How long a ``woken`` or ``unknown`` entry may wait for its acknowledgment."""

DAY_CAP_WINDOW = timedelta(hours=24)
"""Day-cap window and ``consumed_log`` retention."""

_FAIL_REASONS = frozenset({"wake_line_invalid", "revalidation_transient"})
_ACKABLE = frozenset({"pending", "woken", "unknown", "abandoned"})
_RESETTABLE = frozenset({"abandoned", "unknown"})


def _refuse(key: str, state: str | None, trigger: str) -> TransitionError:
    return TransitionError(f"issue {key}: no transition from {state} on {trigger}")


def _state_of(doc: StoreDoc, key: str) -> str | None:
    entry = doc.entries.get(key)
    return None if entry is None else entry.state


def _with_entry(doc: StoreDoc, entry: Entry) -> StoreDoc:
    entries = dict(doc.entries)
    entries[entry.key] = entry
    return replace(doc, entries=entries)


def _new_entry(repo: str, n: int, state: str, now: datetime) -> Entry:
    if not valid_repo(repo) or not valid_issue_number(n):
        raise ValueError(f"invalid issue {repo!r} #{n!r}")
    return Entry(
        repo=repo,
        issue=n,
        state=state,
        attempts=0,
        wake_attempts=0,
        operation_id=None,
        wake_id=None,
        woken_at=None,
        ack_reason=None,
        orchestrator=None,
        consumed_at=None,
        pending_at=None,
        created_at=now,
        updated_at=now,
        lease_expires_at=None,
        last_reason=None,
    )


def fail(doc: StoreDoc, repo: str, n: int, reason: str, now: datetime) -> StoreDoc:
    """T-1 and T-3: record a pre-pending failure of issue ``n`` of ``repo``.

    Allowed from no entry and from ``failed``; ``attempts`` grows by one and at
    ``MAX_ATTEMPTS`` the entry becomes ``abandoned`` ``attempts_exhausted``.
    ``reason`` must be ``wake_line_invalid`` or ``revalidation_transient``.
    """
    key = issue_key(repo, n)
    state = _state_of(doc, key)
    if reason not in _FAIL_REASONS or state not in (None, "failed"):
        raise _refuse(key, state, reason)
    entry = doc.entries.get(key) or _new_entry(repo, n, "failed", now)
    attempts = entry.attempts + 1
    exhausted = attempts >= MAX_ATTEMPTS
    return _with_entry(
        doc,
        replace(
            entry,
            state="abandoned" if exhausted else "failed",
            attempts=attempts,
            updated_at=now,
            last_reason="attempts_exhausted" if exhausted else reason,
        ),
    )


def backoff_elapsed(entry: Entry, now: datetime) -> bool:
    """True when a ``failed`` entry may be examined again.

    Elapsed iff ``now >= updated_at + BACKOFF`` and ``attempts < MAX_ATTEMPTS``.
    """
    if entry.state != "failed":
        raise _refuse(entry.key, entry.state, "backoff_elapsed")
    return entry.attempts < MAX_ATTEMPTS and now >= entry.updated_at + BACKOFF


def mark_pending(
    doc: StoreDoc, repo: str, n: int, orchestrator: str, now: datetime
) -> StoreDoc:
    """Write ``pending`` for an issue, routed to ``orchestrator`` (from no entry or ``failed``).

    Sets ``consumed_at`` and ``pending_at`` to ``now`` (the day cap counts
    ``consumed_at``); ``attempts`` and ``created_at`` are kept. The entry is
    saved before anything is sent and is never routed to another orchestrator.
    """
    key = issue_key(repo, n)
    state = _state_of(doc, key)
    if state not in (None, "failed"):
        raise _refuse(key, state, "pending")
    if ORCHESTRATOR_ID_PATTERN.fullmatch(orchestrator) is None:
        raise ValueError("orchestrator must match the orchestrator id pattern")
    entry = doc.entries.get(key) or _new_entry(repo, n, "pending", now)
    return _with_entry(
        doc,
        replace(
            entry,
            state="pending",
            orchestrator=orchestrator,
            consumed_at=now,
            pending_at=now,
            updated_at=now,
            # No reason in the closed table names a pending write.
            last_reason=None,
        ),
    )


def requeue(doc: StoreDoc, key: str, now: datetime) -> StoreDoc:
    """Put a ``woken`` or ``unknown`` entry back to ``pending`` before a resend.

    Keeps the orchestrator, ``wake_attempts`` and ``consumed_at``: a resend goes
    to the same orchestrator and is the next delivery attempt.
    """
    entry = doc.entries.get(key)
    if entry is None or entry.state not in ("woken", "unknown"):
        raise _refuse(key, _state_of(doc, key), "requeue")
    if entry.wake_attempts >= MAX_WAKE_ATTEMPTS:
        raise _refuse(key, entry.state, "requeue")
    return _with_entry(
        doc,
        replace(
            entry,
            state="pending",
            pending_at=now,
            updated_at=now,
            lease_expires_at=None,
            last_reason="pending_orphan",
        ),
    )


def _pending_to(
    doc: StoreDoc, key: str, trigger: str, now: datetime, **fields: object
) -> StoreDoc:
    entry = doc.entries.get(key)
    if entry is None or entry.state != "pending":
        raise _refuse(key, _state_of(doc, key), trigger)
    return _with_entry(doc, replace(entry, updated_at=now, **fields))


def mark_woken(doc: StoreDoc, key: str, wake_id: str, now: datetime) -> StoreDoc:
    """``pending`` to ``woken``: one more delivery attempt of wake ``wake_id``."""
    if WAKE_ID_PATTERN.fullmatch(wake_id) is None:
        raise ValueError("wake_id must match the wake id pattern")
    entry = doc.entries.get(key)
    attempts = 0 if entry is None else entry.wake_attempts
    return _pending_to(
        doc,
        key,
        "woken",
        now,
        state="woken",
        wake_id=wake_id,
        woken_at=now,
        wake_attempts=attempts + 1,
        lease_expires_at=now + LEASE,
        last_reason="woken",
    )


def mark_unknown(
    doc: StoreDoc,
    key: str,
    wake_id: str | None,
    operation_id: str | None,
    now: datetime,
    reason: str = "wake_unknown",
) -> StoreDoc:
    """``pending`` to ``unknown`` (a send whose outcome is not known, or no session).

    ``reason`` is ``wake_unknown`` or ``no_session``. The delivery counts as an
    attempt, so the entry ends ``abandoned`` after three unacknowledged tries.
    """
    if reason not in ("wake_unknown", "no_session"):
        raise ValueError("reason must be wake_unknown or no_session")
    if operation_id is not None and not valid_operation_id(operation_id):
        raise ValueError("operation_id must be None or match the operation-id pattern")
    if wake_id is not None and WAKE_ID_PATTERN.fullmatch(wake_id) is None:
        raise ValueError("wake_id must be None or match the wake id pattern")
    entry = doc.entries.get(key)
    attempts = 0 if entry is None else entry.wake_attempts
    return _pending_to(
        doc,
        key,
        reason,
        now,
        state="unknown",
        wake_id=wake_id,
        woken_at=now,
        operation_id=operation_id,
        wake_attempts=attempts + 1,
        lease_expires_at=now + LEASE,
        last_reason=reason,
    )


def mark_spawn_error(doc: StoreDoc, key: str, now: datetime) -> StoreDoc:
    """``pending`` to ``abandoned`` ``spawn_error`` (OSError before the child)."""
    return _pending_to(
        doc, key, "spawn_error", now, state="abandoned", last_reason="spawn_error"
    )


def mark_acked(
    doc: StoreDoc, key: str, now: datetime, ack_reason: str | None = None
) -> StoreDoc:
    """An orchestrator acknowledged the entry as ``taken`` or ``skipped``.

    Allowed from ``pending``, ``woken``, ``unknown`` and ``abandoned`` (an
    acknowledgment of an earlier wake can arrive after a resend or after the
    entry was abandoned). ``ack_reason`` is the free skip text of the
    orchestrator, stored only when it matches ``ACK_REASON_PATTERN``; any other
    text is stored as ``unrecognized``.
    """
    entry = doc.entries.get(key)
    if entry is None or entry.state not in _ACKABLE:
        raise _refuse(key, _state_of(doc, key), "acked")
    if ack_reason is not None and ACK_REASON_PATTERN.fullmatch(ack_reason) is None:
        ack_reason = "unrecognized"
    return _with_entry(
        doc,
        replace(
            entry,
            state="acked",
            updated_at=now,
            lease_expires_at=None,
            ack_reason=ack_reason,
            last_reason="acked",
        ),
    )


def record_seen(
    doc: StoreDoc, repo: str, n: int, ack_reason: str, now: datetime
) -> StoreDoc:
    """Record an issue as seen and never woken: the baseline, or a skip that cannot change.

    Creates an ``acked`` entry with no orchestrator (``repo_not_listed``,
    ``repo_disabled``, ``baseline``). A key that already has an entry is left
    as it is.
    """
    key = issue_key(repo, n)
    if key in doc.entries:
        return doc
    if ACK_REASON_PATTERN.fullmatch(ack_reason) is None:
        raise ValueError("ack_reason must match the ack reason pattern")
    entry = replace(
        _new_entry(repo, n, "acked", now), ack_reason=ack_reason, last_reason="acked"
    )
    return _with_entry(doc, entry)


class SweepResult(NamedTuple):
    """What ``sweep`` found: the new document and the entries it moved."""

    doc: StoreDoc
    resend: tuple[Entry, ...]
    abandoned: tuple[Entry, ...]
    orphans: tuple[str, ...]


def sweep(doc: StoreDoc, now: datetime) -> SweepResult:
    """Queue what must be sent again and abandon what ran out of attempts (4.5 step 6).

    * a ``pending`` entry at the start of a cycle was left by a cycle that died
      between the save and the send: it is a resend (``orphans`` names it), never
      an abandon;
    * a ``woken`` or ``unknown`` entry whose lease is over goes back to
      ``pending`` and is a resend, unless its ``MAX_WAKE_ATTEMPTS`` are used:
      then it becomes ``abandoned`` ``ack_not_observed``.

    ``resend`` and ``abandoned`` are in key order, so a dry run can report
    without saving.
    """
    resend: list[Entry] = []
    abandoned: list[Entry] = []
    orphans: list[str] = []
    entries = dict(doc.entries)
    for key in sorted(doc.entries):
        entry = doc.entries[key]
        if entry.state == "pending":
            orphans.append(key)
            resend.append(entry)
        elif entry.state in ("woken", "unknown") and (
            entry.lease_expires_at is None or now >= entry.lease_expires_at
        ):
            if entry.wake_attempts >= MAX_WAKE_ATTEMPTS:
                dead = replace(
                    entry,
                    state="abandoned",
                    updated_at=now,
                    lease_expires_at=None,
                    last_reason="ack_not_observed",
                )
                entries[key] = dead
                abandoned.append(dead)
            else:
                queued = replace(
                    entry,
                    state="pending",
                    pending_at=now,
                    updated_at=now,
                    lease_expires_at=None,
                    last_reason="pending_orphan",
                )
                entries[key] = queued
                resend.append(queued)
    return SweepResult(
        replace(doc, entries=entries), tuple(resend), tuple(abandoned), tuple(orphans)
    )


def set_hold(doc: StoreDoc, key: str, hold: Hold) -> StoreDoc:
    """Write the ``holds`` entry of ``key``."""
    _key(key)
    holds = dict(doc.holds)
    holds[key] = hold
    return replace(doc, holds=holds)


def drop_hold(doc: StoreDoc, key: str) -> StoreDoc:
    """Remove the ``holds`` entry of ``key`` (no entry is not an error)."""
    if key not in doc.holds:
        return doc
    return replace(doc, holds={k: h for k, h in doc.holds.items() if k != key})


def prune_holds(doc: StoreDoc, in_s1: Iterable[str]) -> StoreDoc:
    """Drop every hold whose issue left S1 (4.11 point 6)."""
    keep = set(in_s1)
    return replace(doc, holds={k: h for k, h in doc.holds.items() if k in keep})


def add_info_seen(doc: StoreDoc, keys: Iterable[str]) -> StoreDoc:
    """Add information keys; keep the ``MAX_INFO_SEEN`` newest, no key twice."""
    seen = list(doc.info_seen)
    have = set(seen)
    for k in keys:
        if k not in have:
            seen.append(k)
            have.add(k)
    return replace(doc, info_seen=tuple(seen[-MAX_INFO_SEEN:]))


def add_consumed(doc: StoreDoc, now: datetime) -> StoreDoc:
    """Count one more first-time wake in the day cap (a plan request, 4.5 step 8)."""
    return replace(doc, consumed_log=(*doc.consumed_log, now))


def _in_window(t: datetime, now: datetime) -> bool:
    return now - DAY_CAP_WINDOW < t <= now


def prune_consumed_log(doc: StoreDoc, now: datetime) -> StoreDoc:
    """Drop every ``consumed_log`` time ``t <= now - 24 h``."""
    cutoff = now - DAY_CAP_WINDOW
    return replace(doc, consumed_log=tuple(t for t in doc.consumed_log if t > cutoff))


def day_cap_count(doc: StoreDoc, now: datetime) -> int:
    """Count ``consumed_at`` and ``consumed_log`` times in ``(now - 24 h, now]``."""
    times = [e.consumed_at for e in doc.entries.values() if e.consumed_at]
    times.extend(doc.consumed_log)
    return sum(1 for t in times if _in_window(t, now))


def reset_entry(doc: StoreDoc, key: str, now: datetime) -> StoreDoc:
    """Remove an ``abandoned`` or ``unknown`` entry (``reset KEY``).

    A non-null ``consumed_at`` moves to ``consumed_log`` so the day-cap count
    is unchanged, then ``consumed_log`` is pruned. A missing entry or any other
    state raises ``TransitionError`` (the CLI maps it to ``reset_refused``).
    """
    entry = doc.entries.get(key)
    if entry is None or entry.state not in _RESETTABLE:
        raise _refuse(key, _state_of(doc, key), "reset")
    entries = {k: v for k, v in doc.entries.items() if k != key}
    log = doc.consumed_log
    if entry.consumed_at is not None:
        log = (*log, entry.consumed_at)
    return prune_consumed_log(replace(doc, entries=entries, consumed_log=log), now)


def reset_rate_limit(doc: StoreDoc) -> StoreDoc:
    """``reset --rate-limit``: clear ``next_permitted_at`` and the streak."""
    return replace(doc, next_permitted_at=None, rate_streak=0)


def set_next_permitted(
    doc: StoreDoc, when: datetime | None, streak: int | None = None
) -> StoreDoc:
    """Set ``next_permitted_at``; None clears it. ``streak`` sets ``rate_streak`` too."""
    if streak is None:
        return replace(doc, next_permitted_at=when)
    return replace(doc, next_permitted_at=when, rate_streak=streak)


def set_last_completed(doc: StoreDoc, now: datetime) -> StoreDoc:
    """Stamp ``last_completed_cycle_at``; a completed cycle ends a rate-limit streak."""
    return replace(doc, last_completed_cycle_at=now, rate_streak=0)


def set_last_poll(doc: StoreDoc, when: datetime) -> StoreDoc:
    """Stamp ``last_poll_at``: the server time of the cycle's first GitHub read."""
    return replace(doc, last_poll_at=when)


def end_baseline(doc: StoreDoc) -> StoreDoc:
    """The baseline cycle is complete: later issues are new."""
    return replace(doc, baseline=False)


def empty_doc(now: datetime, baseline: bool = False) -> StoreDoc:
    """A store with no entry, hold or history, created at ``now``."""
    return StoreDoc(
        schema_version=SCHEMA_VERSION,
        created_at=now,
        next_permitted_at=None,
        last_completed_cycle_at=None,
        last_poll_at=None,
        rate_streak=0,
        baseline=baseline,
        info_seen=(),
        consumed_log=(),
        entries={},
        holds={},
    )


def disabled_present(state_dir: Path) -> bool:
    """True while ``state_dir/DISABLED`` exists (a dangling symlink counts)."""
    return os.path.lexists(Path(state_dir) / DISABLED_FILE)


def init_state(state_dir: Path, now: datetime, baseline: bool = True) -> FileStore:
    """Create ``state_dir`` (0700), ``lock`` (0600) and an empty ``dispatch.json``.

    With ``baseline`` (the default) the store asks the first completed cycle to
    record every issue already assigned, and every item already in the
    information streams, as seen without waking anyone (4.3 rule 5). Raises
    ``StateExists`` when ``dispatch.json`` or ``lock`` already exists (nothing is
    changed) and ``StoreError("state_dir_unwritable")`` when a write fails; a
    lock this call created is removed again if the store cannot be written.
    """
    state_dir = Path(state_dir)
    doc = empty_doc(now, baseline)
    _to_raw(doc)  # a naive ``now`` raises ValueError before anything is created
    lock_path = state_dir / LOCK_FILE
    for path in (state_dir / STORE_FILE, lock_path):
        if os.path.lexists(path):  # checked first: an existing store is not touched
            raise StateExists(str(path))
    try:
        os.makedirs(state_dir, mode=0o700, exist_ok=True)
        os.chmod(state_dir, 0o700)  # makedirs mode is filtered by the umask
    except OSError:
        raise StoreError("state_dir_unwritable") from None
    try:
        fd = os.open(
            lock_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600
        )
    except FileExistsError:
        raise StateExists(str(lock_path)) from None
    except OSError:
        raise StoreError("state_dir_unwritable") from None
    store = FileStore(state_dir)
    try:
        try:
            os.fchmod(fd, 0o600)
        finally:
            os.close(fd)
        store.save(doc)
    except OSError:
        try:
            os.unlink(lock_path)
        except OSError:
            pass
        raise StoreError("state_dir_unwritable") from None
    return store


DRY_RUN_FILE = "dry-run.json"


def load_dry_run(state_dir: Path) -> tuple[StoreDoc | None, bool]:
    """Read ``dry-run.json``: the shadow store of a dry run (4.9).

    The shadow is a whole schema-2 document, so a dry run runs the same rules as
    a real cycle against it and keeps what it would have woken. A missing file
    gives ``(None, False)``: the first dry run starts from the real store. An
    unreadable, unparseable or invalid file gives ``(None, True)``, so the cycle
    writes the ``dry_run_shadow_reset`` warning.
    """
    try:
        data = (Path(state_dir) / DRY_RUN_FILE).read_bytes()
    except FileNotFoundError:
        return None, False
    except OSError:
        return None, True
    try:
        return validate(migrate(json.loads(data))), False
    except (ValueError, RecursionError, StoreError):
        return None, True


def save_dry_run(state_dir: Path, doc: StoreDoc) -> None:
    """Write ``dry-run.json`` atomically at 0600, as ``FileStore.save`` does."""
    from superclaude.cli.swarm.atomic import write_prepared_bytes  # C18

    text = json.dumps(_to_raw(doc), sort_keys=True, indent=2, ensure_ascii=True)
    state_dir = Path(state_dir)
    path = state_dir / DRY_RUN_FILE
    write_prepared_bytes(path, text.encode() + b"\n")
    os.chmod(path, 0o600)
    _fsync_dir(state_dir)
