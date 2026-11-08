"""Dispatch record of the issue watcher (design section 7, ``dispatch.json``).

Times are aware UTC datetimes in memory and ``YYYY-MM-DDTHH:MM:SSZ`` strings on
disk; JSON object keys are decimal strings on disk and ``int`` in memory. This
module never reads the wall clock (every time is a ``now`` parameter), never
runs a command, and imports only the standard library and ``predicates`` at
module level.
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
from typing import Protocol

from superclaude.cli.issue_watch.predicates import (
    ApprovalResult,
    format_utc,
    parse_utc,
    valid_issue_number,
    valid_operation_id,
)

SCHEMA_VERSION = 1
"""Store schema version this module reads and writes."""

ENTRY_STATES = frozenset(
    {"pending", "launched", "unknown", "failed", "abandoned", "claimed"}
)
"""The six entry states of design section 7.3."""


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
    """A (state, trigger) pair that no section 7.4 transition row allows."""


class StateExists(Exception):
    """``init_state`` found an existing store and refused to replace it."""


@dataclass(frozen=True)
class Entry:
    """One issue's dispatch entry; every field is always present (None = null)."""

    issue: int
    state: str
    attempts: int
    launches: int
    operation_id: str | None
    approver_id: int | None
    approval_event_id: int | None
    approved_at: datetime | None
    launch_cwd: str | None
    launch_login: str | None
    launch_account_id: int | None
    consumed_at: datetime | None
    pending_at: datetime | None
    created_at: datetime
    updated_at: datetime
    lease_expires_at: datetime | None
    last_reason: str | None


@dataclass(frozen=True)
class StoreDoc:
    """The whole ``dispatch.json`` document, keyed by ``int`` issue numbers."""

    schema_version: int
    created_at: datetime
    next_permitted_at: datetime | None
    last_completed_cycle_at: datetime | None
    considered: Mapping[int, datetime]
    consumed_log: tuple[datetime, ...]
    entries: Mapping[int, Entry]


@dataclass(frozen=True)
class PendingContext:
    """Approval and launch fields the ``pending`` write copies into the entry.

    Neither the design nor the spec defines this type; it is the minimal set of
    Entry fields set by transition T-4 (Open Question OQ-48).
    """

    approver_id: int
    approval_event_id: int
    approved_at: datetime
    launch_cwd: str
    launch_login: str
    launch_account_id: int


_STORE_KEYS = frozenset(
    {
        "schema_version",
        "created_at",
        "next_permitted_at",
        "last_completed_cycle_at",
        "considered",
        "consumed_log",
        "entries",
    }
)
_ENTRY_KEYS = frozenset(Entry.__dataclass_fields__)
_DECIMAL_KEY = re.compile(r"[1-9][0-9]{0,8}")  # at most 9 digits: int() stays cheap


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


def _issue_key(key: object) -> int:
    if not isinstance(key, str) or _DECIMAL_KEY.fullmatch(key) is None:
        raise _invalid()
    number = int(key)
    if not valid_issue_number(number):
        raise _invalid()
    return number


def _entry(key: object, raw: object) -> Entry:
    number = _issue_key(key)
    if not isinstance(raw, dict) or set(raw) != _ENTRY_KEYS:
        raise _invalid()
    if not valid_issue_number(raw["issue"]) or raw["issue"] != number:
        raise _invalid()
    if not isinstance(raw["state"], str) or raw["state"] not in ENTRY_STATES:
        raise _invalid()
    if not _is_int(raw["attempts"]) or raw["attempts"] < 0:
        raise _invalid()
    if not _is_int(raw["launches"]) or raw["launches"] not in (0, 1):
        raise _invalid()
    for name in ("launch_login", "last_reason"):
        _opt(raw[name], lambda v: isinstance(v, str))
    # status prints this id inside a shell command, so only a safe id is stored.
    _opt(raw["operation_id"], valid_operation_id)
    _opt(raw["launch_cwd"], lambda v: isinstance(v, str) and os.path.isabs(v))
    for name in ("approver_id", "approval_event_id", "launch_account_id"):
        _opt(raw[name], _is_int)
    entry = Entry(
        issue=number,
        state=raw["state"],
        attempts=raw["attempts"],
        launches=raw["launches"],
        operation_id=raw["operation_id"],
        approver_id=raw["approver_id"],
        approval_event_id=raw["approval_event_id"],
        approved_at=_opt_time(raw["approved_at"]),
        launch_cwd=raw["launch_cwd"],
        launch_login=raw["launch_login"],
        launch_account_id=raw["launch_account_id"],
        consumed_at=_opt_time(raw["consumed_at"]),
        pending_at=_opt_time(raw["pending_at"]),
        created_at=_time(raw["created_at"]),
        updated_at=_time(raw["updated_at"]),
        lease_expires_at=_opt_time(raw["lease_expires_at"]),
        last_reason=raw["last_reason"],
    )
    if entry.launches == 1 and (entry.consumed_at is None or entry.pending_at is None):
        raise _invalid()
    if entry.state == "failed" and entry.launches != 0:
        raise _invalid()
    return entry


def validate(raw: object) -> StoreDoc:
    """Check a parsed ``dispatch.json`` (design section 7.2) and convert it.

    Raises ``StoreError("store_invalid")`` on any deviation: a key set that is
    not exact at either level, a wrong type, ``issue`` unequal to its key,
    ``launches`` outside {0, 1}, ``launches == 1`` without ``consumed_at`` and
    ``pending_at``, a ``failed`` entry with ``launches`` 1, a time string that
    is not ``YYYY-MM-DDTHH:MM:SSZ``, or a ``schema_version`` other than
    ``SCHEMA_VERSION`` (run ``migrate`` first). ``last_reason`` is checked as a
    ``str`` or null only; its membership in the reason table is pinned by the
    tests, because this module may not import ``audit`` (DF-42).
    """
    if not isinstance(raw, dict) or set(raw) != _STORE_KEYS:
        raise _invalid()
    if not _is_int(raw["schema_version"]) or raw["schema_version"] != SCHEMA_VERSION:
        raise _invalid()
    considered = raw["considered"]
    consumed_log = raw["consumed_log"]
    entries = raw["entries"]
    if not isinstance(considered, dict) or not isinstance(entries, dict):
        raise _invalid()
    if not isinstance(consumed_log, list):
        raise _invalid()
    return StoreDoc(
        schema_version=raw["schema_version"],
        created_at=_time(raw["created_at"]),
        next_permitted_at=_opt_time(raw["next_permitted_at"]),
        last_completed_cycle_at=_opt_time(raw["last_completed_cycle_at"]),
        considered={_issue_key(k): _time(v) for k, v in considered.items()},
        consumed_log=tuple(_time(t) for t in consumed_log),
        entries={_issue_key(k): _entry(k, v) for k, v in entries.items()},
    )


MIGRATIONS: dict[int, Callable[[dict], dict]] = {}
"""Version v -> pure function producing the v + 1 document; ships empty."""


def migrate(
    doc: object, migrations: Mapping[int, Callable[[dict], dict]] = MIGRATIONS
) -> dict:
    """Return ``doc`` raised to ``SCHEMA_VERSION`` by chaining ``migrations``.

    A document already at ``SCHEMA_VERSION`` is returned as is; this function
    never mutates ``doc``. A ``schema_version`` that is not an ``int``, is
    higher than ``SCHEMA_VERSION`` or has no registered step, or a step whose
    result is not a dict at the next version, raises
    ``StoreError("store_invalid")``. ``migrations`` is the test seam (design
    section 7.2).
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


def _to_raw(doc: StoreDoc) -> dict:
    """Return ``doc`` as the JSON-ready dict ``validate`` accepts (round trip)."""
    return {
        "schema_version": doc.schema_version,
        "created_at": format_utc(doc.created_at),
        "next_permitted_at": _opt_utc(doc.next_permitted_at),
        "last_completed_cycle_at": _opt_utc(doc.last_completed_cycle_at),
        "considered": {str(n): format_utc(t) for n, t in doc.considered.items()},
        "consumed_log": [format_utc(t) for t in doc.consumed_log],
        "entries": {str(n): _entry_raw(e) for n, e in doc.entries.items()},
    }


def _fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


class Store(Protocol):
    """The dispatch-record seam of design section 5.4 (``CrashingStore`` wraps it)."""

    state_dir: Path

    def load(self) -> StoreDoc: ...

    def save(self, doc: StoreDoc) -> None: ...

    def lock(self) -> AbstractContextManager[None]: ...

    def disabled(self) -> bool: ...

    def disabled_since(self) -> datetime | None: ...


class FileStore:
    """``Store`` over the files of ``state_dir`` (design sections 7.1 and 7.6)."""

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
        """Hold an exclusive ``flock`` on ``state_dir/lock`` (design section 7.6).

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

BACKOFF = timedelta(minutes=10)
"""Wait after a ``failed`` write before the issue is eligible again (T-2)."""

LEASE = timedelta(minutes=60)
"""Reporting lease of a ``launched`` entry (T-5, T-9)."""

DAY_CAP_WINDOW = timedelta(hours=24)
"""Day-cap window and ``consumed_log`` retention (design section 7.5)."""

_FAIL_REASONS = frozenset({"prompt_invalid", "revalidation_transient"})
_CLAIMABLE = frozenset({"launched", "unknown", "abandoned"})  # T-10
_RESETTABLE = frozenset({"abandoned", "unknown"})  # T-13


def _refuse(n: int, state: str | None, trigger: str) -> TransitionError:
    return TransitionError(f"issue {n}: no transition from {state} on {trigger}")


def _state_of(doc: StoreDoc, n: int) -> str | None:
    entry = doc.entries.get(n)
    return None if entry is None else entry.state


def _with_entry(doc: StoreDoc, entry: Entry) -> StoreDoc:
    entries = dict(doc.entries)
    entries[entry.issue] = entry
    return replace(doc, entries=entries)


def _new_entry(n: int, state: str, now: datetime) -> Entry:
    if not valid_issue_number(n):
        raise ValueError(f"invalid issue number {n!r}")
    return Entry(
        issue=n,
        state=state,
        attempts=0,
        launches=0,
        operation_id=None,
        approver_id=None,
        approval_event_id=None,
        approved_at=None,
        launch_cwd=None,
        launch_login=None,
        launch_account_id=None,
        consumed_at=None,
        pending_at=None,
        created_at=now,
        updated_at=now,
        lease_expires_at=None,
        last_reason=None,
    )


def _positive_id(value: object) -> bool:
    return type(value) is int and value > 0


def _check_approval(approver_id: object, event_id: object, at: object) -> None:
    """Audit lines need positive ids and a UTC time; refuse anything else."""
    if not _positive_id(approver_id) or not _positive_id(event_id):
        raise ValueError("approval ids must be positive integers")
    if not isinstance(at, datetime):
        raise ValueError("approved_at must be a datetime")
    format_utc(at)  # raises ValueError for a naive datetime


def fail(doc: StoreDoc, n: int, reason: str, now: datetime) -> StoreDoc:
    """T-1 and T-3 (plus DF-43): record a pre-pending failure of issue ``n``.

    Allowed from no entry and from ``failed``; ``attempts`` grows by one and at
    ``MAX_ATTEMPTS`` the entry becomes ``abandoned`` ``attempts_exhausted``.
    ``reason`` must be ``prompt_invalid`` or ``revalidation_transient``.
    """
    state = _state_of(doc, n)
    if reason not in _FAIL_REASONS or state not in (None, "failed"):
        raise _refuse(n, state, reason)
    entry = doc.entries.get(n) or _new_entry(n, "failed", now)
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
    """T-2: True when a ``failed`` entry may be examined again.

    Elapsed iff ``now >= updated_at + BACKOFF`` and ``attempts < MAX_ATTEMPTS``.
    """
    if entry.state != "failed":
        raise _refuse(entry.issue, entry.state, "backoff_elapsed")
    return entry.attempts < MAX_ATTEMPTS and now >= entry.updated_at + BACKOFF


def mark_pending(doc: StoreDoc, n: int, ctx: PendingContext, now: datetime) -> StoreDoc:
    """T-4: write ``pending`` for issue ``n`` (from no entry or ``failed``).

    Sets ``launches`` 1, ``consumed_at`` and ``pending_at`` to ``now`` and the
    six ``PendingContext`` fields; ``attempts`` and ``created_at`` are kept.
    """
    state = _state_of(doc, n)
    if state not in (None, "failed"):
        raise _refuse(n, state, "pending")
    _check_approval(ctx.approver_id, ctx.approval_event_id, ctx.approved_at)
    if not isinstance(ctx.launch_cwd, str) or not os.path.isabs(ctx.launch_cwd):
        raise ValueError("launch_cwd must be an absolute path")
    if not isinstance(ctx.launch_login, str) or not ctx.launch_login:
        raise ValueError("launch_login must be a non-empty string")
    if not _positive_id(ctx.launch_account_id):
        raise ValueError("launch_account_id must be a positive integer")
    entry = doc.entries.get(n) or _new_entry(n, "pending", now)
    return _with_entry(
        doc,
        replace(
            entry,
            state="pending",
            launches=1,
            consumed_at=now,
            pending_at=now,
            updated_at=now,
            # No reason in the closed table names a pending write.
            last_reason=None,
            **asdict(ctx),
        ),
    )


def _pending_to(
    doc: StoreDoc, n: int, trigger: str, now: datetime, **fields: object
) -> StoreDoc:
    entry = doc.entries.get(n)
    if entry is None or entry.state != "pending":
        raise _refuse(n, _state_of(doc, n), trigger)
    return _with_entry(doc, replace(entry, updated_at=now, **fields))


def mark_launched(doc: StoreDoc, n: int, operation_id: str, now: datetime) -> StoreDoc:
    """T-5: ``pending`` to ``launched`` with a safe ``operation_id``.

    The id must match ``OPERATION_ID_PATTERN`` (design 9.2); ``ValueError`` else.
    """
    if not valid_operation_id(operation_id):
        raise ValueError("operation_id must match the operation-id pattern")
    return _pending_to(
        doc,
        n,
        "launched",
        now,
        state="launched",
        operation_id=operation_id,
        lease_expires_at=now + LEASE,
        last_reason="launched",
    )


def mark_unknown(
    doc: StoreDoc, n: int, operation_id: str | None, now: datetime
) -> StoreDoc:
    """T-6: ``pending`` to ``unknown``; keeps an ``operation_id`` if Orca gave one.

    ``operation_id`` must be None or match ``OPERATION_ID_PATTERN``; anything
    else raises ``ValueError`` (a saved store must always load again).
    """
    if operation_id is not None and not valid_operation_id(operation_id):
        raise ValueError("operation_id must be None or match the operation-id pattern")
    return _pending_to(
        doc,
        n,
        "launch_unknown",
        now,
        state="unknown",
        operation_id=operation_id,
        last_reason="launch_unknown",
    )


def mark_spawn_error(doc: StoreDoc, n: int, now: datetime) -> StoreDoc:
    """T-7: ``pending`` to ``abandoned`` ``spawn_error`` (OSError before the child)."""
    return _pending_to(
        doc, n, "spawn_error", now, state="abandoned", last_reason="spawn_error"
    )


def sweep(doc: StoreDoc, now: datetime) -> tuple[StoreDoc, list[Entry]]:
    """T-8 and T-9: abandon orphaned ``pending`` and lease-expired ``launched``.

    Every ``pending`` entry becomes ``abandoned`` ``pending_orphan``; every
    ``launched`` entry with ``now >= lease_expires_at`` (or no lease) becomes
    ``abandoned`` ``claim_not_observed``. Returns the new document and the
    changed entries in issue order, so a dry-run can report without saving.
    """
    changed: list[Entry] = []
    for n in sorted(doc.entries):
        entry = doc.entries[n]
        if entry.state == "pending":
            reason = "pending_orphan"
        elif entry.state == "launched" and (
            entry.lease_expires_at is None or now >= entry.lease_expires_at
        ):
            reason = "claim_not_observed"
        else:
            continue
        changed.append(
            replace(entry, state="abandoned", updated_at=now, last_reason=reason)
        )
    entries = dict(doc.entries)
    entries.update((e.issue, e) for e in changed)
    return replace(doc, entries=entries), changed


def mark_claimed(
    doc: StoreDoc,
    n: int,
    now: datetime,
    approval: ApprovalResult | None = None,
) -> StoreDoc:
    """T-10, T-11 and T-12: record the session's own claim marker for ``n``.

    T-10 from ``launched``, ``unknown`` or ``abandoned``; T-11 from no entry
    (``launches`` 0, no ``consumed_at``); T-12 from ``failed``. The caller has
    already applied the marker window; ``approval``, when given, replaces the
    approval fields with the current approval.
    """
    state = _state_of(doc, n)
    if state not in _CLAIMABLE and state not in (None, "failed"):
        raise _refuse(n, state, "claimed")
    fields: dict = {}
    if approval is not None:
        _check_approval(
            approval.approver_id, approval.approval_event_id, approval.approved_at
        )
        fields = {
            "approver_id": approval.approver_id,
            "approval_event_id": approval.approval_event_id,
            "approved_at": approval.approved_at,
        }
    entry = doc.entries.get(n) or _new_entry(n, "claimed", now)
    return _with_entry(
        doc,
        replace(
            entry, state="claimed", updated_at=now, last_reason="claimed", **fields
        ),
    )


def _in_window(t: datetime, now: datetime) -> bool:
    return now - DAY_CAP_WINDOW < t <= now


def prune_consumed_log(doc: StoreDoc, now: datetime) -> StoreDoc:
    """Drop every ``consumed_log`` time ``t <= now - 24 h`` (design section 7.5)."""
    cutoff = now - DAY_CAP_WINDOW
    return replace(doc, consumed_log=tuple(t for t in doc.consumed_log if t > cutoff))


def day_cap_count(doc: StoreDoc, now: datetime) -> int:
    """Count ``consumed_at`` and ``consumed_log`` times in ``(now - 24 h, now]``."""
    times = [e.consumed_at for e in doc.entries.values() if e.consumed_at]
    times.extend(doc.consumed_log)
    return sum(1 for t in times if _in_window(t, now))


def reset_entry(doc: StoreDoc, n: int, now: datetime) -> StoreDoc:
    """T-13: remove an ``abandoned`` or ``unknown`` entry (``reset N``).

    A non-null ``consumed_at`` moves to ``consumed_log`` so the day-cap count
    is unchanged, then ``consumed_log`` is pruned. A missing entry or any other
    state raises ``TransitionError`` (the CLI maps it to ``reset_refused``).
    """
    entry = doc.entries.get(n)
    if entry is None or entry.state not in _RESETTABLE:
        raise _refuse(n, _state_of(doc, n), "reset")
    entries = {k: v for k, v in doc.entries.items() if k != n}
    log = doc.consumed_log
    if entry.consumed_at is not None:
        log = (*log, entry.consumed_at)
    return prune_consumed_log(replace(doc, entries=entries, consumed_log=log), now)


def reset_rate_limit(doc: StoreDoc) -> StoreDoc:
    """``reset --rate-limit``: clear ``next_permitted_at``."""
    return replace(doc, next_permitted_at=None)


def set_next_permitted(doc: StoreDoc, when: datetime | None) -> StoreDoc:
    """Set ``next_permitted_at`` (FR-028); None clears it."""
    return replace(doc, next_permitted_at=when)


def set_last_completed(doc: StoreDoc, now: datetime) -> StoreDoc:
    """Stamp ``last_completed_cycle_at`` (design section 6.2 step 14)."""
    return replace(doc, last_completed_cycle_at=now)


def set_considered(
    doc: StoreDoc, examined: Iterable[int], discovered: Iterable[int], now: datetime
) -> StoreDoc:
    """FR-023: stamp ``examined`` with ``now`` and prune to ``discovered``."""
    keep = set(discovered)
    considered = {n: t for n, t in doc.considered.items() if n in keep}
    considered.update((n, now) for n in examined if n in keep)
    return replace(doc, considered=considered)


def disabled_present(state_dir: Path) -> bool:
    """True while ``state_dir/DISABLED`` exists (a dangling symlink counts)."""
    return os.path.lexists(Path(state_dir) / DISABLED_FILE)


def init_state(state_dir: Path, now: datetime) -> FileStore:
    """Create ``state_dir`` (0700), ``lock`` (0600) and an empty ``dispatch.json``.

    ``created_at`` is ``now`` (the approval floor). Raises ``StateExists`` when
    ``dispatch.json`` or ``lock`` already exists (nothing is changed) and
    ``StoreError("state_dir_unwritable")`` when a write fails; a lock this call
    created is removed again if the store cannot be written.
    """
    state_dir = Path(state_dir)
    doc = StoreDoc(
        schema_version=SCHEMA_VERSION,
        created_at=now,
        next_permitted_at=None,
        last_completed_cycle_at=None,
        considered={},
        consumed_log=(),
        entries={},
    )
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
_DRY_RUN_KEYS = frozenset({"schema_version", "considered", "shadow_launches"})


@dataclass(frozen=True)
class DryRunDoc:
    """The ``dry-run.json`` shadow state (design section 7.2); dry-run only."""

    considered: Mapping[int, datetime]
    shadow_launches: tuple[datetime, ...]


def _dry_run_doc(raw: object) -> DryRunDoc:
    if not isinstance(raw, dict) or set(raw) != _DRY_RUN_KEYS:
        raise _invalid()
    if not _is_int(raw["schema_version"]) or raw["schema_version"] != SCHEMA_VERSION:
        raise _invalid()
    considered, launches = raw["considered"], raw["shadow_launches"]
    if not isinstance(considered, dict) or not isinstance(launches, list):
        raise _invalid()
    return DryRunDoc(
        considered={_issue_key(k): _time(v) for k, v in considered.items()},
        shadow_launches=tuple(_time(t) for t in launches),
    )


def load_dry_run(state_dir: Path) -> tuple[DryRunDoc, bool]:
    """Read ``dry-run.json``; return the shadow and whether it was replaced.

    A missing file gives an empty shadow and False (the first dry-run). An
    unreadable, unparseable or invalid file gives an empty shadow and True, so
    the cycle writes the ``dry_run_shadow_reset`` warning (design line 449).
    """
    empty = DryRunDoc(considered={}, shadow_launches=())
    try:
        data = (Path(state_dir) / DRY_RUN_FILE).read_bytes()
    except FileNotFoundError:
        return empty, False
    except OSError:
        return empty, True
    try:
        return _dry_run_doc(json.loads(data)), False
    except (ValueError, RecursionError, StoreError):
        return empty, True


def save_dry_run(state_dir: Path, doc: DryRunDoc) -> None:
    """Write ``dry-run.json`` atomically at 0600, as ``FileStore.save`` does."""
    from superclaude.cli.swarm.atomic import write_prepared_bytes  # C18

    raw = {
        "schema_version": SCHEMA_VERSION,
        "considered": {str(n): format_utc(t) for n, t in doc.considered.items()},
        "shadow_launches": [format_utc(t) for t in doc.shadow_launches],
    }
    text = json.dumps(raw, sort_keys=True, indent=2, ensure_ascii=True)
    state_dir = Path(state_dir)
    path = state_dir / DRY_RUN_FILE
    write_prepared_bytes(path, text.encode() + b"\n")
    os.chmod(path, 0o600)
    _fsync_dir(state_dir)
