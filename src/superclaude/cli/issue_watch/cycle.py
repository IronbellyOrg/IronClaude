"""One poll cycle of the issue watcher (design sections 4.2, 4.3, 5.4 and 8.5).

Part 1 holds the constants, the configuration and its validators, the approvers
file check, the clock and deadline, the ``Deps`` and ``CycleResult`` records
and the exit-code rules. This module never imports ``subprocess``: every
command runs through the injected ``Runner``. Time is read only through the
``Clock``. Nothing here touches ``fcntl`` or ``/proc`` at import time.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import stat
import sys
import time
import unicodedata
from collections.abc import Callable, Iterable
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from . import audit, github, launch, predicates, record
from .launch import Launcher
from .predicates import ApprovalResult, DiscoveredIssue, format_utc, parse_utc
from .record import Entry, LockError, LockHeld, Store, StoreDoc, StoreError
from .runner import CommandResult, Runner

# Design section 14 defaults. They are module constants, not operator knobs.
MAX_CANDIDATES = 10
MAX_LAUNCHES_PER_CYCLE = 1
DAY_CAP = 6
GH_TIMEOUT_S = 20.0
PROBE_TIMEOUT_S = 10.0
GIT_TIMEOUT_S = 10.0
LAUNCH_TIMEOUT_S = 120.0
DEADLINE_TOTAL_S = 240.0
GH_FLOOR_S = 5.0
LAUNCH_CUTOFF_S = 120.0
SKEW_WARN_S = 60
HEALTH_AGE_S = 900
STALE_AGE_S = 86400
DISCOVERY_WARN = 80

# Filesystem types a state directory must not live on (design 4.2, DF-53).
NETWORK_FS_TYPES = frozenset(
    {"nfs", "nfs4", "cifs", "smb3", "sshfs", "fuse.sshfs", "9p"}
)

SCHEMA_VERSION = 1
DEFAULT_TRIGGER_LABEL = "issue-watch:trigger"
DEFAULT_APPROVAL_LABEL = "issue-watch:approved"

_TOP_KEYS = frozenset(
    {
        "schema_version",
        "enabled",
        "labels",
        "project_id",
        "owner_account_id",
        "worktree",
        "approvers_file",
        "state_dir",
    }
)
_LABEL_KEYS = frozenset({"trigger", "approval"})
_LABEL_MAX = 50
_PROJECT_ID = re.compile(r"PVT_[A-Za-z0-9_-]{1,64}")
_APPROVER_LINE = re.compile(r"[1-9][0-9]{0,19}")
_ACCOUNT_ID_MAX = 10**20 - 1
_APPROVERS_MAX_BYTES = 1024 * 1024
_UTC_TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
_MOUNTINFO = "/proc/self/mountinfo"
_OCTAL_ESCAPE = re.compile(r"\\(040|011|012|134)")


class ConfigError(Exception):
    """A configuration, platform, worktree or approvers failure.

    ``reason`` is a key of ``audit.REASON_TABLE`` (``config_invalid``,
    ``approvers_invalid``, ``platform_unsupported`` or ``worktree_invalid``).
    ``detail`` is a short fixed text for the operator; it never holds a value
    read from the file.
    """

    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(reason, detail)
        self.reason = reason
        self.detail = detail


@dataclass(frozen=True)
class Config:
    """The validated configuration file (design 4.2)."""

    enabled: bool
    trigger_label: str
    approval_label: str
    project_id: str
    owner_account_id: int | None
    worktree: Path
    approvers_file: Path
    state_dir: Path


def _invalid(detail: str) -> ConfigError:
    return ConfigError("config_invalid", detail)


def _is_int(value: object) -> bool:
    return type(value) is int


def _is_abs_path(value: object) -> bool:
    return (
        isinstance(value, str)
        and value != ""
        and "\0" not in value
        and os.path.isabs(value)
    )


def _label(raw: object, field: str) -> str:
    if not isinstance(raw, str) or not 1 <= len(raw) <= _LABEL_MAX:
        raise _invalid(
            f"labels.{field} must be a string of 1 to {_LABEL_MAX} characters"
        )
    if any(unicodedata.category(c) == "Cc" for c in raw):
        raise _invalid(f"labels.{field} must not contain control characters")
    # DF-20: `gh issue list --label` splits on commas; a leading dash reads as a flag.
    if "," in raw or '"' in raw or raw.startswith("-"):
        raise _invalid(
            f"labels.{field} must not contain a comma or a quote, or start with a dash"
        )
    return raw


def _decode_mount_point(field: str) -> str:
    return _OCTAL_ESCAPE.sub(lambda m: chr(int(m.group(1), 8)), field)


def fs_type_of(path: str | os.PathLike[str], mountinfo_text: str) -> str | None:
    """Return the filesystem type holding ``path`` according to ``mountinfo_text``.

    Field 5 of a mountinfo line is the mount point, with the octal escapes
    ``\\040``, ``\\011``, ``\\012`` and ``\\134`` decoded; the type is the first
    field after the ``-`` separator. The longest mount point that is a path
    prefix of ``os.path.realpath(path)`` wins (a later line wins a tie, because
    it is mounted on top). A path that does not exist is matched through its
    nearest existing parent, since ``realpath`` keeps the missing tail. None
    when no line matches.
    """
    target = os.path.realpath(os.fspath(path))
    best_len = -1
    best_type: str | None = None
    for text_line in mountinfo_text.splitlines():
        parts = text_line.split()
        if len(parts) < 7 or "-" not in parts[5:]:
            continue
        sep = parts.index("-", 5)
        if sep + 1 >= len(parts):
            continue
        mount_point = _decode_mount_point(parts[4])
        if mount_point == "/":
            matches = True
        else:
            matches = target == mount_point or target.startswith(mount_point + "/")
        if matches and len(mount_point) >= best_len:
            best_len = len(mount_point)
            best_type = parts[sep + 1]
    return best_type


def _read_mountinfo() -> str | None:
    """Return the text of ``/proc/self/mountinfo``, or None when unreadable."""
    try:
        with open(_MOUNTINFO, encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return None


def _default_state_dir() -> Path:
    try:
        base = os.environ.get("XDG_STATE_HOME") or Path.home() / ".local/state"
    except (RuntimeError, KeyError):  # no home directory can be resolved
        raise _invalid("state_dir has no default: HOME is not set") from None
    return Path(base) / "superclaude" / "issue-watch"


def load_config(path: str | os.PathLike[str]) -> Config:
    """Read and validate the JSON configuration file (design 4.2, FR-027).

    Makes no external call and writes nothing. Every failure is
    ``ConfigError("config_invalid")``. A ``~`` inside a JSON value is not
    expanded, so it fails the absolute-path rule (DF-13). A ``state_dir`` on a
    network filesystem is refused; an unreadable mountinfo skips that check.
    """
    try:
        with open(path, "rb") as handle:
            raw = json.loads(handle.read())
    except (
        OSError,
        ValueError,
        RecursionError,
    ):  # ValueError covers bad JSON and UTF-8
        raise _invalid(
            "the configuration file is missing or is not valid JSON"
        ) from None
    if not isinstance(raw, dict):
        raise _invalid("the configuration must be a JSON object")
    unknown = set(raw) - _TOP_KEYS
    if unknown:
        raise _invalid(
            "unknown configuration key: " + ", ".join(sorted(map(str, unknown)))
        )

    if (
        not _is_int(raw.get("schema_version"))
        or raw["schema_version"] != SCHEMA_VERSION
    ):
        raise _invalid("schema_version must be the integer 1")

    enabled = raw.get("enabled", False)
    if not isinstance(enabled, bool):
        raise _invalid("enabled must be a JSON boolean")

    labels = raw.get("labels", {})
    if not isinstance(labels, dict):
        raise _invalid("labels must be an object")
    unknown_labels = set(labels) - _LABEL_KEYS
    if unknown_labels:
        raise _invalid(
            "unknown labels key: " + ", ".join(sorted(map(str, unknown_labels)))
        )
    trigger = _label(labels.get("trigger", DEFAULT_TRIGGER_LABEL), "trigger")
    approval = _label(labels.get("approval", DEFAULT_APPROVAL_LABEL), "approval")
    if trigger == approval:
        raise _invalid("labels.approval must differ from labels.trigger")

    project_id = raw.get("project_id")
    if not isinstance(project_id, str) or _PROJECT_ID.fullmatch(project_id) is None:
        raise _invalid(
            "project_id must match PVT_ followed by 1 to 64 letters, digits, _ or -"
        )

    owner = raw.get("owner_account_id")
    if "owner_account_id" in raw and (
        not _is_int(owner) or not 1 <= owner <= _ACCOUNT_ID_MAX
    ):
        raise _invalid("owner_account_id must be an integer from 1 to 10**20-1")

    for key in ("worktree", "approvers_file"):
        if not _is_abs_path(raw.get(key)):
            raise _invalid(f"{key} must be an absolute path (a ~ is not expanded)")

    if "state_dir" in raw:
        if not _is_abs_path(raw["state_dir"]):
            raise _invalid("state_dir must be an absolute path (a ~ is not expanded)")
        state_dir = Path(raw["state_dir"])
    else:
        state_dir = _default_state_dir()
        if not state_dir.is_absolute():
            raise _invalid("state_dir must be absolute: XDG_STATE_HOME is relative")

    mountinfo = _read_mountinfo()
    if mountinfo is not None and fs_type_of(state_dir, mountinfo) in NETWORK_FS_TYPES:
        raise _invalid("state_dir is on a network filesystem")

    return Config(
        enabled=enabled,
        trigger_label=trigger,
        approval_label=approval,
        project_id=project_id,
        owner_account_id=owner if "owner_account_id" in raw else None,
        worktree=Path(raw["worktree"]),
        approvers_file=Path(raw["approvers_file"]),
        state_dir=state_dir,
    )


def check_platform() -> None:
    """Raise ``ConfigError("platform_unsupported")`` unless running on Linux."""
    if sys.platform != "linux":
        raise ConfigError(
            "platform_unsupported", "the issue watcher runs on Linux only"
        )


def _approvers_invalid(detail: str) -> ConfigError:
    return ConfigError("approvers_invalid", detail)


def validate_approvers(path: str | os.PathLike[str]) -> frozenset[int]:
    """Return the approver account ids in ``path`` (design 4.2, FR-027).

    The file must be a regular file (a symlink is refused), owned by the
    effective UID, not group- or other-writable, and hold at least one id. Blank
    lines and lines starting with ``#`` are ignored; any other line must be a
    decimal id. Any failure is ``ConfigError("approvers_invalid")``.
    """
    try:
        st = os.lstat(path)
    except OSError:
        raise _approvers_invalid(
            "the approvers file is missing or unreadable"
        ) from None
    if not stat.S_ISREG(st.st_mode):
        raise _approvers_invalid("the approvers file is not a regular file")
    unreadable = "the approvers file cannot be read as UTF-8 text"
    try:
        # O_NONBLOCK: a FIFO swapped in after lstat must not block the open; the
        # fstat checks below then refuse it (no effect on regular-file reads).
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK)
    except OSError:
        raise _approvers_invalid(unreadable) from None
    # Owner and mode are judged on the open descriptor, and the descriptor must be
    # the inode lstat saw: a writer to the parent directory cannot swap the file
    # between a path check and the open (same pattern as record.py's lock open).
    try:
        try:
            fst = os.fstat(fd)
            if (fst.st_dev, fst.st_ino) != (st.st_dev, st.st_ino):
                raise _approvers_invalid(
                    "the approvers file changed while it was being checked"
                )
            if not stat.S_ISREG(fst.st_mode):
                raise _approvers_invalid("the approvers file is not a regular file")
            if fst.st_uid != os.geteuid():
                raise _approvers_invalid(
                    "the approvers file is not owned by the effective user"
                )
            if fst.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
                raise _approvers_invalid(
                    "the approvers file is group- or other-writable"
                )
            with os.fdopen(fd, "rb", closefd=False) as handle:
                data = handle.read(_APPROVERS_MAX_BYTES + 1)
            text = data.decode("utf-8")
        except (OSError, ValueError):
            raise _approvers_invalid(unreadable) from None
    finally:
        os.close(fd)
    if len(data) > _APPROVERS_MAX_BYTES:
        raise _approvers_invalid("the approvers file is too large")
    ids: set[int] = set()
    for text_line in text.split("\n"):
        if text_line.strip() == "" or text_line.startswith("#"):
            continue
        if _APPROVER_LINE.fullmatch(text_line) is None:
            raise _approvers_invalid(
                "the approvers file holds a line that is not an account id"
            )
        ids.add(int(text_line))
    if not ids:
        raise _approvers_invalid("the approvers file holds no account id")
    return frozenset(ids)


def approvers_summary(path: str | os.PathLike[str]) -> tuple[str, int]:
    """Return the file's mtime as a UTC ``Z`` string and its id count (R10)."""
    count = len(validate_approvers(path))
    mtime = datetime.fromtimestamp(os.stat(path).st_mtime, tz=timezone.utc)
    return mtime.strftime(_UTC_TS_FORMAT), count


def validate_setup(config: Config) -> frozenset[int]:
    """Check the worktree, then the approvers file; return the approver ids."""
    if not os.path.isdir(config.worktree):
        raise ConfigError(
            "worktree_invalid", "the worktree is not an existing directory"
        )
    return validate_approvers(config.approvers_file)


class Clock(Protocol):
    """Wall and monotonic time; every time read in a cycle goes through it."""

    def now(self) -> datetime:
        """Return the current time as a timezone-aware UTC datetime."""
        ...

    def monotonic(self) -> float:
        """Return a monotonic reading in seconds."""
        ...


class SystemClock:
    """The real ``Clock``."""

    def now(self) -> datetime:
        return datetime.now(timezone.utc)

    def monotonic(self) -> float:
        return time.monotonic()


class Deadline:
    """The cycle's time budget (design 8.5): 240 s, a 5 s floor, a 120 s launch cutoff."""

    def __init__(self, clock: Clock, total: float = DEADLINE_TOTAL_S) -> None:
        self._clock = clock
        self._total = float(total)
        self._start = clock.monotonic()

    def elapsed(self) -> float:
        """Seconds since the deadline was created."""
        return self._clock.monotonic() - self._start

    def remaining(self) -> float:
        """Seconds left, never below zero."""
        return max(0.0, self._total - self.elapsed())

    def timeout_for(self, configured: float) -> float | None:
        """Return the lesser of ``configured`` and the time left.

        None when fewer than ``GH_FLOOR_S`` seconds remain: the call must not
        start, and the caller must test for None before it calls a ``Runner``.
        """
        left = self.remaining()
        if left < GH_FLOOR_S:
            return None
        return min(float(configured), left)

    def launch_allowed(self) -> bool:
        """False once more than ``LAUNCH_CUTOFF_S`` seconds have elapsed."""
        return self.elapsed() <= LAUNCH_CUTOFF_S


@dataclass(frozen=True)
class Deps:
    """Everything ``run_cycle`` needs, injected (design 5.4, DF-45)."""

    runner: Runner
    store: Store
    launcher: Launcher
    clock: Clock
    audit: audit.AuditLog
    config: Config
    which: Callable[[str], str | None]
    host: str


@dataclass(frozen=True)
class CycleResult:
    """What one cycle did: the exit code, the cycle reason and the lines written."""

    exit_code: int
    reason: str
    cycle_id: str
    launched_issue: int | None = None
    would_launch: int | None = None
    probe: str | None = None
    lines: tuple[dict, ...] = ()


# Exit precedence (design 4.3, OD-10).
_PRECEDENCE = (2, 6, 7, 5, 3, 4)
_LOCK_HELD_EXIT = 75


def resolve_exit(conditions: frozenset[int]) -> int:
    """Return the exit code for a set of raised exit conditions.

    The first present of 2, 6, 7, 5, 3, 4; else 75 only when it is the sole
    condition; else 0. This is the only place conditions are combined.
    """
    for code in _PRECEDENCE:
        if code in conditions:
            return code
    if set(conditions) - {0} == {_LOCK_HELD_EXIT}:
        return _LOCK_HELD_EXIT
    return 0


def exit_for(reason: str) -> int:
    """Return the exit code of ``reason`` from ``audit.REASON_TABLE`` (DF-41)."""
    return audit.REASON_TABLE[reason][1]


# --- Part 2: the poll cycle (design section 6.2, steps 1 to 15) ---------------

_LOGIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")
_RATE_CLAMP = timedelta(seconds=github.RATE_LIMIT_MAX_WAIT_S)


class _Skip(Exception):
    """One issue is skipped with ``reason``; the cycle goes on."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class _Transient(Exception):
    """A re-read call timed out or failed with a 5xx (``failed``, FR-014)."""


class _Stop(Exception):
    """The cycle ends with the cycle-level ``reason`` (design 6.2 "Stop").

    ``stamp`` says whether the candidate being examined still gets a
    ``considered`` stamp: yes after a launch-step stop, no when a read failed.
    """

    def __init__(self, reason: str, stamp: bool = False) -> None:
        super().__init__(reason)
        self.reason = reason
        self.stamp = stamp


@dataclass
class _Cand:
    """One candidate under examination."""

    n: int
    issue: DiscoveredIssue
    entry: Entry | None
    approval: ApprovalResult | None = None
    launching: bool = False  # True once the issue passed every GitHub check


class _LastResult:
    """A ``Runner`` that keeps the last ``CommandResult`` (G1 headers, DF-35)."""

    def __init__(self, runner: Runner) -> None:
        self._runner = runner
        self.last: CommandResult | None = None

    def run(
        self, argv: list[str], timeout: float, *, cwd: str | None = None
    ) -> CommandResult:
        self.last = self._runner.run(argv, timeout, cwd=cwd)
        return self.last


class _Cycle:
    """The state of one ``run_cycle`` call; every step is one method."""

    def __init__(self, deps: Deps, dry_run: bool) -> None:
        self.deps = deps
        self.dry_run = dry_run
        self.cycle_id = uuid4().hex
        self.deadline = Deadline(deps.clock)
        self.budget = github.CallBudget()
        self.lines: list[dict] = []
        self.conds: list[tuple[str, int]] = []  # (reason, exit) of each condition
        self.login: str | None = None
        self.account_id: int | None = None
        self.approvers: frozenset[int] = frozenset()
        self.doc: StoreDoc | None = None
        self.dirty = False
        self.stop_reason: str | None = None
        self.discovery_count: int | None = None
        self.clock_skew_s: int | None = None
        self.discovered: tuple[DiscoveredIssue, ...] | None = None
        self.examined: list[int] = []
        self.halt = False
        self.launched_issue: int | None = None
        self.would_launch: int | None = None
        self.shadow: record.DryRunDoc | None = None
        self.shadow_reset = False

    # -- small helpers -------------------------------------------------------

    def now(self) -> datetime:
        return self.deps.clock.now()

    def _ts(self) -> str:
        return format_utc(self.now())

    def _tf(self) -> float | None:
        """Timeout of the next per-issue ``gh`` call (None: none may start)."""
        return self.deadline.timeout_for(GH_TIMEOUT_S)

    def _tf_shared(self) -> float | None:
        """As ``_tf`` for G1 and G2, counting a started call in ``gh_calls``."""
        timeout = self.deadline.timeout_for(GH_TIMEOUT_S)
        if timeout is not None:
            self.budget.spend_shared()
        return timeout

    def _cond(self, reason: str) -> None:
        self.conds.append((reason, exit_for(reason)))

    def _stopped(self, reason: str) -> None:
        self.stop_reason = reason
        self._cond(reason)

    def _exit(self) -> int:
        return resolve_exit(frozenset(code for _, code in self.conds))

    def _set(self, doc: StoreDoc) -> None:
        self.doc = doc
        self.dirty = True

    def _save(self) -> None:
        try:
            self.deps.store.save(self.doc)  # type: ignore[arg-type]
        except OSError:
            raise _Stop("state_dir_unwritable") from None
        self.dirty = False

    def _warn(self, reason: str, **fields: int) -> None:
        self.lines.append(
            audit.warning_line(
                ts=self._ts(),
                host=self.deps.host,
                login=self.login,
                cycle_id=self.cycle_id,
                dry_run=self.dry_run,
                reason=reason,
                **fields,
            )
        )

    def _decision(
        self,
        reason: str,
        issue: int,
        state: str | None,
        approver_id: int | None,
        event_id: int | None,
        approved_at: datetime | None,
        note: str | None = None,
    ) -> dict:
        return audit.decision_line(
            ts=self._ts(),
            host=self.deps.host,
            login=self.login,
            cycle_id=self.cycle_id,
            dry_run=self.dry_run,
            reason=reason,
            issue=issue,
            state=None if self.dry_run else state,  # a dry-run writes no entry
            approver_id=approver_id,
            approval_event_id=event_id,
            approved_at=None if approved_at is None else format_utc(approved_at),
            note=note,
        )

    def _issue_line(self, c: _Cand, reason: str, state: str | None = None) -> None:
        a, e = c.approval, c.entry
        if a is not None:
            ids = (a.approver_id, a.approval_event_id, a.approved_at)
        elif e is not None:
            ids = (e.approver_id, e.approval_event_id, e.approved_at)
        else:
            ids = (None, None, None)
        reapproved = (
            a is not None
            and e is not None
            and e.approval_event_id is not None
            and e.approval_event_id != a.approval_event_id
        )
        note = "re-approved" if reapproved else None
        self.lines.append(self._decision(reason, c.n, state, *ids, note))

    def _rate_stop(self) -> _Stop:
        """A rate limit with no header to read: clamp to 3600 s (DF-51, C22)."""
        assert self.doc is not None
        when = self.now() + _RATE_CLAMP
        self._set(record.set_next_permitted(self.doc, when))
        return _Stop("rate_limit_clamped")

    def _origin_ok(self, timeout: float) -> bool:
        """Run the origin check with a ``timeout`` the caller took from the deadline.

        True when the origin is the fork. The caller tests the deadline first
        (``Deadline.timeout_for`` is None when no time is left) and never passes
        None, so a ``Runner`` never gets one (design 8.5).
        """
        worktree = self.deps.config.worktree
        return launch.check_origin(self.deps.runner, worktree, timeout) is None

    # -- the cycle -----------------------------------------------------------

    def run(self) -> CycleResult:
        deps = self.deps
        try:
            if not deps.config.enabled and not self.dry_run:
                raise _Stop("not_enabled")
            try:
                self.approvers = validate_setup(deps.config)
            except ConfigError as exc:
                raise _Stop(exc.reason) from None
        except _Stop as stop:
            self._stopped(stop.reason)
            return self._conclude(locked=False)
        try:
            with deps.store.lock():
                self._locked_body()
                return self._conclude(locked=True)
        except LockHeld:
            self._stopped("lock_held")
        except LockError as exc:
            self._stopped(exc.reason)
        return self._conclude(locked=False)

    def _locked_body(self) -> None:
        try:
            self._steps()
        except _Stop as stop:
            self._stopped(stop.reason)
        self._commit()

    def _steps(self) -> None:
        if self.deps.store.disabled():
            raise _Stop("disabled")
        self._load()
        self._login_step()
        timeout = self.deadline.timeout_for(GIT_TIMEOUT_S)
        if timeout is None:
            # Gate C fix C-1: no time left is not a mismatch. The origin check is
            # a shared call, so design 8.5 gives exit 3 gh_timeout (no git call).
            raise _Stop("gh_timeout")
        if not self._origin_ok(timeout):
            raise _Stop("origin_mismatch")
        self._sweep()
        issues = self._discover()
        by_number = {i.number: i for i in issues}
        if self.dry_run:
            self.shadow, self.shadow_reset = record.load_dry_run(
                self.deps.store.state_dir
            )
            if self.shadow_reset:
                self._warn("dry_run_shadow_reset")
            considered = self.shadow.considered
        else:
            assert self.doc is not None
            considered = self.doc.considered
        order = predicates.eligibility_order(issues, considered)[:MAX_CANDIDATES]
        self._candidates(order, by_number)

    def _load(self) -> None:
        store = self.deps.store
        try:
            doc = store.load()
        except StoreError as exc:
            raise _Stop(exc.reason) from None
        self.doc = doc
        if not self.dry_run and getattr(store, "migrated", False):
            self._save()  # DF-17: only a real cycle saves the migrated store
        wait = doc.next_permitted_at
        if wait is not None and self.now() < wait:
            raise _Stop("rate_limited")

    def _login_step(self) -> None:
        cfg = self.deps.config
        capture = _LastResult(self.deps.runner)
        read = github.user(capture, self._tf_shared)
        if read.reason is not None:
            if read.kind == "rate_limited" and capture.last is not None:
                assert self.doc is not None
                when, reason = github.rate_limit_wait(capture.last, self.now())
                self._set(record.set_next_permitted(self.doc, when))
                raise _Stop(reason)
            raise _Stop(read.reason)
        who = read.value
        if _LOGIN.fullmatch(who.login) is None:  # type: ignore[union-attr]
            raise _Stop("login_invalid")
        self.login = who.login  # type: ignore[union-attr]
        self.account_id = who.account_id  # type: ignore[union-attr]
        if cfg.owner_account_id is not None and cfg.owner_account_id != who.account_id:  # type: ignore[union-attr]
            raise _Stop("account_id_mismatch")
        server = who.server_date  # type: ignore[union-attr]
        if server is not None:
            skew = abs((server - self.now()).total_seconds())
            self.clock_skew_s = int(round(skew))  # S 100: on the cycle line every cycle
            if skew > SKEW_WARN_S:  # only the warning line has a threshold
                self._warn("clock_skew", clock_skew_s=self.clock_skew_s)

    def _sweep(self) -> None:
        assert self.doc is not None
        doc, changed = record.sweep(self.doc, self.now())
        if changed:
            self._set(doc)  # a dry-run keeps it in memory only
        for e in changed:
            self.lines.append(
                self._decision(
                    e.last_reason or "pending_orphan",
                    e.issue,
                    "abandoned",
                    e.approver_id,
                    e.approval_event_id,
                    e.approved_at,
                )
            )

    def _discover(self) -> tuple[DiscoveredIssue, ...]:
        cfg = self.deps.config
        read = github.discover(
            self.deps.runner, cfg.trigger_label, self.login or "", self._tf_shared
        )
        if read.reason is not None:
            if read.kind == "rate_limited":
                raise self._rate_stop()
            raise _Stop(read.reason)
        issues: tuple[DiscoveredIssue, ...] = read.value  # type: ignore[assignment]
        self.discovered = issues
        self.discovery_count = len(issues)
        if len(issues) >= DISCOVERY_WARN:
            self._warn("discovery_count", discovery_count=len(issues))
        return issues

    # -- candidates (steps 10 and 11) ------------------------------------------

    def _candidates(
        self, order: list[int], by_number: dict[int, DiscoveredIssue]
    ) -> None:
        for n in order:
            if self.halt:
                break
            assert self.doc is not None
            c = _Cand(n, by_number[n], self.doc.entries.get(n))
            try:
                reason, state = self._examine(c)
            except _Skip as skip:
                reason, state = skip.reason, None
            except _Stop as stop:
                # Gate C fix C-2 (strict DF-41): the candidate that ends the cycle
                # gets no decision line; the cycle line carries the stop reason.
                if stop.stamp:
                    self.examined.append(n)
                raise
            self._issue_line(c, reason, state)
            if reason != "budget_exhausted":
                self.examined.append(n)
            if c.launching:
                self.halt = True  # S1: nothing after a launch-step outcome (DF-50)

    def _val(self, read: github.Read, fallback: str | None = None) -> object:
        """Return the value of a per-issue read, or raise the skip or the stop."""
        if read.reason is None:
            return read.value
        if read.kind == "rate_limited":
            raise self._rate_stop()
        if read.kind == "scope_missing":
            raise _Stop("project_read_failed")
        if read.kind == "budget_exhausted":
            raise _Skip("budget_exhausted")
        raise _Skip(fallback or read.reason)

    def _hit(
        self,
        markers: object,
        pending_at: datetime | None,
        approved_at: datetime | None,
    ) -> bool:
        """True when an own marker is in the window; never without a floor."""
        if pending_at is None and approved_at is None:
            return False
        return any(
            predicates.marker_in_window(
                m,
                own_login=self.login or "",
                pending_at=pending_at,
                approved_at=approved_at,
            )
            for m in markers  # type: ignore[attr-defined]
        )

    def _day_cap_reached(self) -> bool:
        assert self.doc is not None
        now = self.now()
        used = record.day_cap_count(self.doc, now)
        if self.shadow is not None:
            window = record.DAY_CAP_WINDOW
            used += sum(
                1 for t in self.shadow.shadow_launches if now - window < t <= now
            )
        return used >= DAY_CAP

    def _approve(
        self, c: _Cand, events: object, fallback: str | None = None
    ) -> ApprovalResult:
        assert self.doc is not None
        cfg = self.deps.config
        result = predicates.approval_of(
            events,  # type: ignore[arg-type]
            labels_now=c.issue.labels,
            trigger_label=cfg.trigger_label,
            approval_label=cfg.approval_label,
            approvers=self.approvers,
            store_created_at=self.doc.created_at,
        )
        if not result.approved:
            raise _Skip(fallback or result.reason or "not_approved")
        c.approval = result
        return result

    def _claim(self, c: _Cand, approval: ApprovalResult | None) -> tuple[str, str]:
        assert self.doc is not None
        self._set(record.mark_claimed(self.doc, c.n, self.now(), approval))
        return "claimed", "claimed"

    def _reclaim(self, c: _Cand, fallback: str) -> tuple[str, str]:
        """A tombstone or a ``failed`` entry in backoff: find the approval floor."""
        d = self.deps
        markers = self._val(
            github.marker_comments(d.runner, self.budget, c.n, self._tf)
        )
        events = self._val(
            github.events(d.runner, self.budget, c.n, self._tf), fallback
        )
        approval = self._approve(c, events, fallback)
        if self._hit(markers, None, approval.approved_at):
            return self._claim(c, approval)
        raise _Skip(fallback)

    def _examine(self, c: _Cand) -> tuple[str, str | None]:
        """Steps 10 and 11 for one candidate: ``(reason, entry state or None)``."""
        d, cfg = self.deps, self.deps.config
        e = c.entry
        state = e.state if e is not None else None
        if state in ("claimed", "pending"):
            raise _Skip("already_dispatched")
        if e is not None and (
            state in ("launched", "unknown")
            or (state == "abandoned" and e.pending_at is not None)
        ):
            markers = self._val(
                github.marker_comments(d.runner, self.budget, c.n, self._tf)
            )
            if self._hit(markers, e.pending_at, None):
                return self._claim(c, None)  # T-10
            raise _Skip("already_dispatched")
        if state == "abandoned":  # an attempts_exhausted tombstone
            return self._reclaim(c, "already_dispatched")
        if e is not None and not record.backoff_elapsed(e, self.now()):
            return self._reclaim(c, "in_backoff")  # OQ-36
        if self._day_cap_reached():
            raise _Skip("day_cap")
        owned, why = predicates.is_intended_owner(c.issue.assignees, self.login or "")
        if not owned:
            raise _Skip(why or "assigned_other")
        markers = self._val(
            github.marker_comments(d.runner, self.budget, c.n, self._tf)
        )
        events = self._val(github.events(d.runner, self.budget, c.n, self._tf))
        approval = self._approve(c, events)
        if self._hit(markers, None, approval.approved_at):
            return self._claim(c, approval)  # T-11, T-12
        edits = self._val(github.edits(d.runner, self.budget, c.n, self._tf))
        why = predicates.unchanged_since(
            approval.approved_at,  # type: ignore[arg-type]
            edits,  # type: ignore[arg-type]
            events,  # type: ignore[arg-type]
            own_login=self.login or "",
        )
        if why is not None:
            raise _Skip(why)
        items = self._val(github.project_items(d.runner, self.budget, c.n, self._tf))
        why = predicates.project_check(items, cfg.project_id)  # type: ignore[arg-type]
        if why is not None:
            raise _Skip(why)
        return self._launch(c, approval)

    # -- step 12: the launch steps ---------------------------------------------

    def _rv(self, read: github.Read) -> object:
        """A re-read result: the value, or the skip, the stop or the transient."""
        if read.reason is None:
            return read.value
        if read.kind == "rate_limited":
            raise self._rate_stop()
        if read.kind == "scope_missing":
            raise _Stop("project_read_failed")
        if read.kind == "budget_exhausted":
            raise _Skip("budget_exhausted")
        if read.kind in ("timeout", "transient"):
            raise _Transient
        raise _Skip("revalidation_failed")

    def _revalidate(self, c: _Cand) -> None:
        """FR-011: G7, G3' and G6' with the 3 reserved calls."""
        d, cfg = self.deps, self.deps.config
        snap: predicates.IssueSnapshot = self._rv(  # type: ignore[assignment]
            github.reread(d.runner, self.budget, c.n, self._tf)
        )
        if (
            snap.state.lower() != "open"
            or cfg.trigger_label not in snap.labels
            or cfg.approval_label not in snap.labels
        ):
            raise _Skip("revalidation_failed")
        owned, why = predicates.is_intended_owner(snap.assignees, self.login or "")
        if not owned:
            raise _Skip(why or "assigned_other")
        assert self.doc is not None and c.approval is not None
        events = self._rv(
            github.events(d.runner, self.budget, c.n, self._tf, reserved=True)
        )
        again = predicates.approval_of(
            events,  # type: ignore[arg-type]
            labels_now=snap.labels,
            trigger_label=cfg.trigger_label,
            approval_label=cfg.approval_label,
            approvers=self.approvers,
            store_created_at=self.doc.created_at,
        )
        # A voided approval, or a newer approval event (edits are not re-read), fails.
        if (
            not again.approved
            or again.approval_event_id != c.approval.approval_event_id
        ):
            raise _Skip("revalidation_failed")
        items = self._rv(
            github.project_items(d.runner, self.budget, c.n, self._tf, reserved=True)
        )
        if predicates.project_check(items, cfg.project_id) is not None:  # type: ignore[arg-type]
            raise _Skip("revalidation_failed")

    def _fail(self, c: _Cand, reason: str) -> tuple[str, str]:
        assert self.doc is not None
        self._set(record.fail(self.doc, c.n, reason, self.now()))
        self._cond(reason)  # exit 7, also when the third failure abandons it
        entry = self.doc.entries[c.n]
        shown = entry.last_reason if entry.state == "abandoned" else reason
        return shown or reason, entry.state

    def _launch(self, c: _Cand, approval: ApprovalResult) -> tuple[str, str | None]:
        d, cfg = self.deps, self.deps.config
        c.launching = True
        if self.dry_run:  # no probe, no Orca call, nothing written (FR-019, OQ-39)
            assert self.shadow is not None
            self.would_launch = c.n
            self.shadow = replace(
                self.shadow, shadow_launches=(*self.shadow.shadow_launches, self.now())
            )
            return "launched", None
        timeout = self.deadline.timeout_for(PROBE_TIMEOUT_S)
        if timeout is None:
            raise _Skip("budget_exhausted")
        out_of_time = False

        def probe_allowance() -> float | None:
            # Re-read before each probe: the first probe may have used the time.
            nonlocal out_of_time
            left = self.deadline.timeout_for(PROBE_TIMEOUT_S)
            out_of_time = left is None
            return left

        orca = launch.find_orca(d.runner, which=d.which, timeout=probe_allowance)
        if orca is None:
            if out_of_time:  # a deadline problem is not "orca not found"
                raise _Skip("budget_exhausted")
            raise _Stop("orca_not_found", stamp=True)
        try:
            prompt = launch.build_claim_prompt(c.n)
        except ValueError:
            return self._fail(c, "prompt_invalid")
        try:
            self._revalidate(c)
        except _Transient:
            return self._fail(c, "revalidation_transient")
        if self._day_cap_reached():
            raise _Skip("day_cap")
        if d.store.disabled():
            raise _Stop("disabled_mid_cycle", stamp=True)
        # Gate C fix C-1 (design 647-649): when the 120 s cut-off has passed or
        # fewer than 5 s are left, no git call starts and the step ends with no
        # entry and a budget_exhausted decision line. origin_mismatch (exit 2)
        # is only for a git call that ran and failed.
        if not self.deadline.launch_allowed():
            raise _Skip("budget_exhausted")
        origin_timeout = self.deadline.timeout_for(GIT_TIMEOUT_S)
        if origin_timeout is None:
            raise _Skip("budget_exhausted")
        if not self._origin_ok(origin_timeout):
            raise _Stop("origin_mismatch", stamp=True)
        # Gate C cycle 2 (N-1): the git call may itself have crossed the cut-off,
        # so the launch must not start after it (design 647).
        if not self.deadline.launch_allowed():
            raise _Skip("budget_exhausted")
        assert self.doc is not None and self.login is not None
        assert self.account_id is not None
        ctx = record.PendingContext(
            approver_id=approval.approver_id,  # type: ignore[arg-type]
            approval_event_id=approval.approval_event_id,  # type: ignore[arg-type]
            approved_at=approval.approved_at,  # type: ignore[arg-type]
            launch_cwd=str(cfg.worktree),
            launch_login=self.login,
            launch_account_id=self.account_id,
        )
        before_pending = self.doc  # restored whole: a partial undo fails validate
        self._set(record.mark_pending(self.doc, c.n, ctx, self.now()))
        self._save()  # FR-010: durable before the launch call
        # Reflect R-1: the pending save may itself have crossed the 120 s cut-off
        # (design 647, AC-19). Put the previous document back and start no launch.
        if not self.deadline.launch_allowed():
            self._set(before_pending)
            self._save()
            raise _Skip("budget_exhausted")
        outcome = d.launcher.launch(orca, cfg.worktree, prompt, LAUNCH_TIMEOUT_S)
        now = self.now()
        if outcome.kind == "launched":
            op = outcome.operation_id or ""
            self._set(record.mark_launched(self.doc, c.n, op, now))
            self.launched_issue = c.n
            return "launched", "launched"
        if outcome.kind == "unknown":
            self._set(record.mark_unknown(self.doc, c.n, outcome.operation_id, now))
            self._cond("launch_unknown")
            return "launch_unknown", "unknown"
        self._set(record.mark_spawn_error(self.doc, c.n, now))
        self._cond("spawn_error")
        return "spawn_error", "abandoned"

    # -- steps 13 to 15 ----------------------------------------------------------

    def _commit(self) -> None:
        """Step 13 and 14: the one final write (the store, or the dry-run shadow)."""
        if self.stop_reason == "state_dir_unwritable":
            return
        try:
            if self.dry_run:
                self._commit_shadow()
            else:
                self._commit_store()
        except OSError:
            self._stopped("state_dir_unwritable")

    def _commit_store(self) -> None:
        doc = self.doc
        if doc is None:
            return
        now = self.now()
        changed = self.dirty
        if self.examined and self.discovered is not None:
            numbers = [i.number for i in self.discovered]
            doc = record.set_considered(doc, self.examined, numbers, now)
            changed = True
        if self.stop_reason is None and self._exit() == 0:
            doc = record.set_last_completed(doc, now)  # step 14
            changed = True
        if changed:
            self.doc = record.prune_consumed_log(doc, now)
            self.deps.store.save(self.doc)
            self.dirty = False

    def _commit_shadow(self) -> None:
        shadow = self.shadow
        if shadow is None or self.discovered is None:
            return
        launched = self.would_launch is not None
        if not (self.examined or launched or self.shadow_reset):
            return
        now = self.now()
        keep = {i.number for i in self.discovered}
        considered = {n: t for n, t in shadow.considered.items() if n in keep}
        considered.update((n, now) for n in self.examined if n in keep)
        cutoff = now - record.DAY_CAP_WINDOW
        launches = tuple(t for t in shadow.shadow_launches if t > cutoff)
        record.save_dry_run(
            self.deps.store.state_dir,
            record.DryRunDoc(considered=considered, shadow_launches=launches),
        )

    def _cycle_reason(self, exit_code: int) -> str:
        if exit_code != 0:
            for reason, code in self.conds:
                if code == exit_code:
                    return reason
        if self.stop_reason is not None:
            return self.stop_reason
        # [PROPOSAL] (Gate C fix C-2, executor decision): a cycle that ran to its
        # end names the cycle-kind reason cycle_complete (exit 0). A skip or entry
        # reason belongs to a decision line, never to this cycle line (DF-41).
        return "cycle_complete"

    def _conclude(self, locked: bool) -> CycleResult:
        """Step 15: decision lines, then the cycle line."""
        exit_code = self._exit()
        reason = self._cycle_reason(exit_code)
        cycle = audit.cycle_line(
            ts=self._ts(),
            host=self.deps.host,
            login=self.login,
            cycle_id=self.cycle_id,
            dry_run=self.dry_run,
            exit_code=exit_code,
            reason=reason,
            gh_calls=self.budget.total,
            duration_ms=int(self.deadline.elapsed() * 1000),
            discovery_count=self.discovery_count,
            clock_skew_s=self.clock_skew_s,
        )
        lines = (*self.lines, cycle)
        try:
            if self.stop_reason == "state_dir_unwritable":
                raise OSError("state_dir_unwritable")  # stderr only (FR-020)
            if locked:
                self.deps.audit.rotate_if_needed()
            for ln in lines:
                self.deps.audit.append(ln)
        except OSError:
            audit.stderr_fallback(reason, exit_code, ts=self._ts(), host=self.deps.host)
        return CycleResult(
            exit_code=exit_code,
            reason=reason,
            cycle_id=self.cycle_id,
            launched_issue=self.launched_issue,
            would_launch=self.would_launch,
            probe="skipped" if self.would_launch is not None else None,
            lines=lines,
        )


def run_cycle(deps: Deps, dry_run: bool) -> CycleResult:
    """Run one poll cycle (design 6.2) and return what it did.

    ``check_platform`` is the caller's. Never calls ``subprocess`` (every
    command goes through ``deps.runner`` and ``deps.launcher``), reads time only
    through ``deps.clock``, writes ``dispatch.json`` never in a dry-run, and
    leaves the lock to the context manager of ``deps.store.lock()``.
    """
    return _Cycle(deps, dry_run).run()


# --- Part 3: the status report and the SLO numbers (design 10.2 and 10.3) -----

_SLO_WINDOW = timedelta(days=7)
_SLO_EXCLUDED_REASONS = frozenset({"disabled", "not_enabled"})


def _read_store_doc(store: Store) -> StoreDoc:
    """Read ``dispatch.json`` with a plain read-only ``open``: no lock, no write.

    Migrates in memory only, like ``FileStore.load``. Raises ``StoreError``.
    """
    path = Path(store.state_dir) / record.STORE_FILE
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except FileNotFoundError:
        raise StoreError("store_missing") from None
    except OSError:
        raise StoreError("store_invalid") from None
    migrations = getattr(store, "migrations", record.MIGRATIONS)
    try:
        return record.validate(record.migrate(json.loads(data), migrations))
    except (ValueError, RecursionError):  # bad JSON, bad UTF-8, deep nesting
        raise StoreError("store_invalid") from None


def _is_stale(entry: Entry, now: datetime) -> bool:
    """An ``unknown`` or ``abandoned`` ``pending_orphan`` entry older than 24 h."""
    if entry.state == "unknown":
        pass
    elif entry.state == "abandoned" and entry.last_reason == "pending_orphan":
        pass
    else:
        return False
    return (now - entry.updated_at).total_seconds() > STALE_AGE_S


def _retry_orca(which: Callable[[str], str | None]) -> str:
    """First ``_ORCA_CLIS`` name ``which`` resolves, else the first name (OQ-50)."""
    for name in launch._ORCA_CLIS:
        if which(name):
            return name
    return launch._ORCA_CLIS[0]


def status_report(
    store: Store,
    audit: audit.AuditLog | None,
    now: datetime,
    *,
    which: Callable[[str], str | None] = shutil.which,
) -> dict:
    """Return the ``status --json`` fields of design 10.2.

    Reads ``dispatch.json`` and the ``DISABLED`` mtime and nothing else: no
    lock, no write, no probe, no ``gh``. ``audit`` is accepted for the fixed
    signature and not read. Only typed scalars are returned, never issue text.
    An unreadable store raises ``StoreError``. The retry argv uses the first
    ``_ORCA_CLIS`` name ``which`` resolves; with none resolved it uses the bare
    first name and does not raise (OQ-50).
    """
    doc = _read_store_doc(store)
    last = doc.last_completed_cycle_at
    age = None if last is None else int((now - last).total_seconds())
    counts: dict[str, int] = {}
    for entry in doc.entries.values():
        counts[entry.state] = counts.get(entry.state, 0) + 1
    since = store.disabled_since()
    next_at = doc.next_permitted_at
    orca = _retry_orca(which)
    stale: list[dict] = []
    retry: list[dict] = []
    for n in sorted(doc.entries):
        entry = doc.entries[n]
        if _is_stale(entry, now):
            stale.append(
                {
                    "issue": n,
                    "state": entry.state,
                    "last_reason": entry.last_reason,
                    "updated_at": format_utc(entry.updated_at),
                }
            )
        if entry.state == "unknown" and entry.operation_id and entry.launch_cwd:
            try:
                argv = launch.retry_argv(
                    orca,
                    entry.launch_cwd,
                    launch.build_claim_prompt(n),
                    entry.operation_id,
                )
            except ValueError:  # an id that cannot be printed as a command
                continue
            retry.append(
                {
                    "issue": n,
                    "operation_id": entry.operation_id,
                    "cwd": entry.launch_cwd,
                    "argv": argv,
                }
            )
    return {
        "healthy": age is not None and age <= HEALTH_AGE_S,
        "last_completed_cycle_age_seconds": age,
        "disabled_since": None if since is None else format_utc(since),
        "next_permitted_at": None if next_at is None else format_utc(next_at),
        "counts": counts,
        "day_cap_used": record.day_cap_count(doc, now),
        "stale": stale,
        "retry": retry,
    }


@dataclass(frozen=True)
class SloNumbers:
    """NFR-013's four numbers; a share or p95 is None when it has no samples."""

    approval_to_launch_p95_s: float | None
    cycle_exit0_share: float | None
    claimed_within_lease_share: float | None
    stale_count: int


def _line_time(ln: dict, key: str) -> datetime | None:
    """Return the time under ``key``, or None when absent or malformed."""
    value = ln.get(key)
    if value is None:
        return None
    try:
        return parse_utc(value)
    except ValueError:
        return None


def slo_numbers(lines: Iterable[dict], doc: StoreDoc, now: datetime) -> SloNumbers:
    """Reduce audit lines (oldest first) and the store to the four SLO numbers.

    Pure: no I/O. Dry-run lines count toward none of (a) to (c). A line that
    lacks a field, or holds a malformed time, drops out of the number that
    needs it and never raises.
    """
    waits: list[float] = []
    cycles = ok_cycles = 0
    launched: list[tuple[int, datetime]] = []
    claimed: dict[int, list[datetime]] = {}
    for ln in lines:
        if not isinstance(ln, dict) or ln.get("dry_run") is True:
            continue
        ts = _line_time(ln, "ts")
        if ts is None:
            continue
        kind, reason = ln.get("kind"), ln.get("reason")
        if kind == "cycle":
            if ts < now - _SLO_WINDOW or reason in _SLO_EXCLUDED_REASONS:
                continue
            cycles += 1
            ok_cycles += ln.get("exit") == 0
        elif kind == "decision" and type(ln.get("issue")) is int:
            if reason == "launched":
                launched.append((ln["issue"], ts))
                approved = _line_time(ln, "approved_at")
                if approved is not None:
                    waits.append((ts - approved).total_seconds())
            elif reason == "claimed":
                claimed.setdefault(ln["issue"], []).append(ts)
    p95 = None
    if waits:
        waits.sort()
        p95 = waits[-(-95 * len(waits) // 100) - 1]  # nearest rank: ceil(0.95 n)
    due = reached = 0
    for n, at in launched:
        end = at + record.LEASE
        hit = any(at <= c < end for c in claimed.get(n, ()))
        if hit or now >= end:
            due += 1
            reached += hit
    return SloNumbers(
        approval_to_launch_p95_s=p95,
        cycle_exit0_share=ok_cycles / cycles if cycles else None,
        claimed_within_lease_share=reached / due if due else None,
        stale_count=sum(1 for e in doc.entries.values() if _is_stale(e, now)),
    )
