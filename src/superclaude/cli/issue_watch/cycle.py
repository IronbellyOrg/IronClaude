"""One poll cycle of the issue watcher (design 4.2 to 4.11).

The poll finds issues assigned to the user in the listed repositories, holds the
ones that have no plan (4.11), decides which are new and delivers them to the
orchestrator of their repository as a wake (section 3). It claims nothing and
starts no worker; its only GitHub writes are adding and removing the label
``hold:plan``. Part 1 holds the constants, the configuration and its
validators, the clock and deadline, the ``Deps`` and ``CycleResult`` records and
the exit-code rules. Part 2 is the cycle. Part 3 is ``status`` and the
service-level numbers.

This module never imports ``subprocess``: every command runs through the
injected ``Runner``. Time is read only through the ``Clock``. Nothing here
touches ``fcntl`` or ``/proc`` at import time.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from . import audit, github, hold, launch, predicates, record, repos, route, wake
from .predicates import (
    DiscoveredIssue,
    InfoItem,
    format_utc,
    issue_key,
    parse_utc,
    split_issue_key,
)
from .record import Entry, Hold, LockError, LockHeld, Store, StoreDoc, StoreError
from .runner import CommandResult, Runner

# Design section 14 defaults. They are module constants, not operator knobs.
MAX_CANDIDATES = 10
DAY_CAP = 6
GH_TIMEOUT_S = 20.0
PROBE_TIMEOUT_S = 10.0
GIT_TIMEOUT_S = 10.0
LAUNCH_TIMEOUT_S = 120.0
"""Bounds the session start and one wake send."""
DEADLINE_TOTAL_S = 240.0
GH_FLOOR_S = 5.0
LAUNCH_CUTOFF_S = 120.0
"""After this many seconds no wake is sent and no session is started."""
SKEW_WARN_S = 60
HEALTH_AGE_S = 900
STALE_AGE_S = 86400
DISCOVERY_WARN = 80
RATE_BASE_S = 300
RATE_MAX_S = 3600
INFO_OVERLAP = timedelta(minutes=5)
"""``since`` of the information streams is the previous cycle's start minus this (4.3)."""
MAX_EVIDENCE_BRANCHES = 5
"""Linked branches whose date one evidence read looks at (bounds the calls of E2)."""

# Filesystem types a state directory must not live on (design 4.2, DF-53).
NETWORK_FS_TYPES = frozenset(
    {"nfs", "nfs4", "cifs", "smb3", "sshfs", "fuse.sshfs", "9p"}
)

SCHEMA_VERSION = 2
"""Schema of the poll's configuration file (the keys changed in design 4.4)."""

DEFAULT_TAG_PREFIX = "orchestrator"
_TOP_KEYS = frozenset(
    {
        "schema_version",
        "enabled",
        "owner_account_id",
        "orchestrator_repo",
        "state_dir",
        "session_tag_prefix",
    }
)
_ACCOUNT_ID_MAX = 10**20 - 1
_TAG_PREFIX = re.compile(r"[a-z][a-z0-9]{0,11}")
_UTC_TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
_MOUNTINFO = "/proc/self/mountinfo"
_OCTAL_ESCAPE = re.compile(r"\\(040|011|012|134)")
UNREAD_REASONS = frozenset(
    {"no_session", "ack_not_observed", "attempts_exhausted", "plan_stuck"}
)
"""The exit-7 conditions that also mark the orchestrator workspace unread (DQ2)."""


class ConfigError(Exception):
    """A configuration, platform, repos or orchestrator-repo failure.

    ``reason`` is a key of ``audit.REASON_TABLE`` (``config_invalid``,
    ``platform_unsupported``, ``repos_invalid`` or ``orchestrator_repo_invalid``).
    ``detail`` is a short fixed text for the operator; it never holds a value
    read from the file.
    """

    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(reason, detail)
        self.reason = reason
        self.detail = detail


@dataclass(frozen=True)
class Config:
    """The validated configuration file (design 4.4)."""

    enabled: bool
    owner_account_id: int | None
    orchestrator_repo: Path
    state_dir: Path
    session_tag_prefix: str = DEFAULT_TAG_PREFIX


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
    """Read and validate the JSON configuration file (design 4.4, FR-027).

    Makes no external call and writes nothing. Every failure is
    ``ConfigError("config_invalid")``. A ``~`` inside a JSON value is not
    expanded, so it fails the absolute-path rule (DF-13). A ``state_dir`` on a
    network filesystem is refused; an unreadable mountinfo skips that check. The
    repository list is not here: it lives in ``<orchestrator_repo>/repos.yaml``.
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
        raise _invalid(f"schema_version must be the integer {SCHEMA_VERSION}")

    enabled = raw.get("enabled", False)
    if not isinstance(enabled, bool):
        raise _invalid("enabled must be a JSON boolean")

    owner = raw.get("owner_account_id")
    if "owner_account_id" in raw and (
        not _is_int(owner) or not 1 <= owner <= _ACCOUNT_ID_MAX
    ):
        raise _invalid("owner_account_id must be an integer from 1 to 10**20-1")

    if not _is_abs_path(raw.get("orchestrator_repo")):
        raise _invalid(
            "orchestrator_repo must be an absolute path (a ~ is not expanded)"
        )

    prefix = raw.get("session_tag_prefix", DEFAULT_TAG_PREFIX)
    if not isinstance(prefix, str) or _TAG_PREFIX.fullmatch(prefix) is None:
        raise _invalid(
            "session_tag_prefix must be 1 to 12 lower-case letters or digits"
        )

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
        owner_account_id=owner if "owner_account_id" in raw else None,
        orchestrator_repo=Path(raw["orchestrator_repo"]),
        state_dir=state_dir,
        session_tag_prefix=prefix,
    )


def check_platform() -> None:
    """Raise ``ConfigError("platform_unsupported")`` unless running on Linux."""
    if sys.platform != "linux":
        raise ConfigError(
            "platform_unsupported", "the issue watcher runs on Linux only"
        )


def validate_setup(
    config: Config, runner: Runner, timeout: float = PROBE_TIMEOUT_S
) -> repos.ReposDoc:
    """Check the orchestrator repository, then read and validate its ``repos.yaml``.

    Returns the validated ``ReposDoc``. A missing directory is
    ``orchestrator_repo_invalid``; a bad ``repos.yaml`` (or an unreadable tier
    list) is ``repos_invalid``; both are exit 2.
    """
    if not os.path.isdir(config.orchestrator_repo):
        raise ConfigError(
            "orchestrator_repo_invalid",
            "the orchestrator repository is not an existing directory",
        )
    try:
        return repos.load_repos(config.orchestrator_repo, runner, timeout)
    except repos.ReposError as exc:
        raise ConfigError("repos_invalid", exc.detail) from None


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
    """The cycle's time budget (design 8.5): 240 s, a 5 s floor, a 120 s wake cutoff."""

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
    waker: wake.Waker
    clock: Clock
    audit: audit.AuditLog
    config: Config
    which: Callable[[str], str | None]
    host: str
    label_guard: github.Guard | None = None
    wake_token: Callable[[], str] | None = None


@dataclass(frozen=True)
class CycleResult:
    """What one cycle did: the exit code, the cycle reason and the lines written."""

    exit_code: int
    reason: str
    cycle_id: str
    woken: tuple[str, ...] = ()
    would_wake: tuple[str, ...] = ()
    would_hold: tuple[str, ...] = ()
    would_release: tuple[str, ...] = ()
    would_request: tuple[str, ...] = ()
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


# --- Part 2: the poll cycle (design 4.5, steps 1 to 12) ------------------------------

_LOGIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")
_SEEN_SKIPS = frozenset({"repo_not_listed", "repo_disabled", "checkout_missing"})
"""Skips that cannot change on their own: the issue is recorded as seen (``--take`` hands it over)."""


class _Skip(Exception):
    """One issue is skipped with ``reason``; the cycle goes on."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class _Transient(Exception):
    """A re-read call timed out or failed with a 5xx (``failed``, FR-014)."""


class _Stop(Exception):
    """The cycle ends with the cycle-level ``reason`` (design 4.5 "Stop")."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


@dataclass
class _Cand:
    """One assignment or plan request under examination."""

    row: DiscoveredIssue
    entry: Entry | None
    first_seen_at: datetime
    checkout_state: str = "ok"
    hold: Hold | None = None
    missing: tuple[str, ...] = ()


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


def rate_wait_seconds(streak: int) -> int:
    """The wait after a rate limit with no header: ``min(3600, 300 x 2^(streak - 1))`` (4.6).

    ``streak`` counts the consecutive rate-limited cycles including this one,
    so the first waits 300 s (one poll interval), then 600, 1200, 2400, 3600.
    """
    return min(RATE_MAX_S, RATE_BASE_S * 2 ** max(0, streak - 1))


class _Cycle:
    """The state of one ``run_cycle`` call; every step is one method."""

    def __init__(self, deps: Deps, dry_run: bool) -> None:
        self.deps = deps
        self.dry_run = dry_run
        self.cycle_id = uuid4().hex
        self.deadline = Deadline(deps.clock)
        self.budget = github.CallBudget()
        self.labels = github.LabelWriter(deps.runner, deps.label_guard)
        self.lines: list[dict] = []
        self.conds: list[tuple[str, int]] = []  # (reason, exit) of each condition
        self.login: str | None = None
        self.account_id: int | None = None
        self.rdoc: repos.ReposDoc | None = None
        self.doc: StoreDoc | None = None
        self.dirty = False
        self.stop_reason: str | None = None
        self.discovery_count: int | None = None
        self.clock_skew_s: int | None = None
        self.created_at: datetime | None = None  # the server time of the first read
        self.s1: list[DiscoveredIssue] = []
        self.s1_done = False
        self.info_new: list[InfoItem] = []
        self.skips: list[wake.SkippedItem] = []
        self.cands: list[_Cand] = []  # assignments chosen by the filters (step 8)
        self.plan_due: list[_Cand] = []  # plan requests due (row 6 of 4.11)
        self.resend_keys: list[str] = []
        self.plan_resend_keys: list[str] = []
        self.unread: set[str] = set()
        self.woken: list[str] = []
        self.would_wake: list[str] = []
        self.would_hold: list[str] = []
        self.would_release: list[str] = []
        self.would_request: list[str] = []
        self.info_sent: list[str] = []
        self.orca: str | None = None
        self.orca_checked = False
        self.origin_state: dict[str, str] = {}
        self.reserved_day_cap = 0
        self.shadow_reset = False
        self.rate_limited = False
        self._registry: route.Registry = {}

    # -- small helpers -------------------------------------------------------

    def now(self) -> datetime:
        return self.deps.clock.now()

    def _ts(self) -> str:
        return format_utc(self.now())

    def _tf(self) -> float | None:
        """Timeout of the next per-issue ``gh`` call (None: none may start)."""
        return self.deadline.timeout_for(GH_TIMEOUT_S)

    def _tf_shared(self) -> float | None:
        """As ``_tf`` for G1 and the searches, counting a started call in ``gh_calls``."""
        timeout = self.deadline.timeout_for(GH_TIMEOUT_S)
        if timeout is not None:
            self.budget.spend_shared()
        return timeout

    def _cond(self, reason: str) -> None:
        self.conds.append((reason, exit_for(reason)))
        if reason in UNREAD_REASONS:
            self.unread.add(reason)

    def _stopped(self, reason: str) -> None:
        self.stop_reason = reason
        self._cond(reason)

    def _exit(self) -> int:
        return resolve_exit(frozenset(code for _, code in self.conds))

    def _set(self, doc: StoreDoc) -> None:
        self.doc = doc
        self.dirty = True

    def _save(self) -> None:
        if (
            self.dry_run
        ):  # a dry run keeps the document in memory; ``_commit_shadow`` writes it
            return
        try:
            self.deps.store.save(self.doc)  # type: ignore[arg-type]
        except OSError:
            raise _Stop("state_dir_unwritable") from None
        self.dirty = False

    def _warn(self, reason: str, **fields: object) -> None:
        self.lines.append(
            audit.warning_line(
                ts=self._ts(),
                host=self.deps.host,
                login=self.login,
                cycle_id=self.cycle_id,
                dry_run=self.dry_run,
                reason=reason,
                **fields,  # type: ignore[arg-type]
            )
        )

    def _decision(
        self,
        reason: str,
        repo: str,
        number: int,
        state: str | None = None,
        **extra: str | None,
    ) -> None:
        self.lines.append(
            audit.decision_line(
                ts=self._ts(),
                host=self.deps.host,
                login=self.login,
                cycle_id=self.cycle_id,
                dry_run=self.dry_run,
                reason=reason,
                repo=repo,
                issue=number,
                state=None if self.dry_run else state,  # a dry run writes no entry
                **extra,
            )
        )

    def _rate_stop(self) -> _Stop:
        """A rate limit with no header to read: exponential backoff (4.6)."""
        assert self.doc is not None
        streak = self.doc.rate_streak + 1
        when = self.now() + timedelta(seconds=rate_wait_seconds(streak))
        self._set(record.set_next_permitted(self.doc, when, streak))
        self.rate_limited = True
        return _Stop("rate_limit_clamped")

    def _find_orca(self) -> str | None:
        """The Orca CLI, probed once per cycle (None when not found or no time is left)."""
        if self.orca_checked:
            return self.orca
        out_of_time = False

        def allowance() -> float | None:
            nonlocal out_of_time
            left = self.deadline.timeout_for(PROBE_TIMEOUT_S)
            out_of_time = left is None
            return left

        self.orca = launch.find_orca(
            self.deps.runner, which=self.deps.which, timeout=allowance
        )
        self.orca_checked = not out_of_time
        return self.orca

    # -- the cycle -----------------------------------------------------------

    def run(self) -> CycleResult:
        deps = self.deps
        try:
            if not deps.config.enabled and not self.dry_run:
                raise _Stop("not_enabled")
            timeout = self.deadline.timeout_for(PROBE_TIMEOUT_S)
            if timeout is None:
                raise _Stop("gh_timeout")
            try:
                self.rdoc = validate_setup(deps.config, deps.runner, timeout)
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
        self._ack_step()
        self._sweep()
        self._discover()
        assert self.doc is not None
        if self.doc.baseline:
            self._baseline()
            return
        self._select()
        self._reread()
        self._route_and_wake()

    def _load(self) -> None:
        store = self.deps.store
        try:
            doc = store.load()
        except StoreError as exc:
            raise _Stop(exc.reason) from None
        if not self.dry_run and getattr(store, "migrated", False):
            self.doc = doc
            self._save()  # DF-17: only a real cycle saves the migrated store
        if self.dry_run:
            shadow, self.shadow_reset = record.load_dry_run(store.state_dir)
            if self.shadow_reset:
                self._warn("dry_run_shadow_reset")
            doc = shadow if shadow is not None else doc
        self.doc = doc
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
                if reason == "rate_limit_clamped":
                    raise self._rate_stop()
                self._set(
                    record.set_next_permitted(self.doc, when, self.doc.rate_streak + 1)
                )
                self.rate_limited = True
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
        self.created_at = server if server is not None else self.now()
        if server is not None:
            skew = abs((server - self.now()).total_seconds())
            self.clock_skew_s = int(round(skew))  # S 100: on the cycle line every cycle
            if skew > SKEW_WARN_S:  # only the warning line has a threshold
                self._warn("clock_skew", clock_skew_s=self.clock_skew_s)

    # -- step 5: the acknowledgments ------------------------------------------

    def _wake_item_keys(self, wake_id: str) -> list[str]:
        """The keys of a wake file's ``assigned`` then ``plan_requests`` (for rejected indexes)."""
        path = self.deps.config.orchestrator_repo / wake.WAKES_DIR / f"{wake_id}.json"
        try:
            raw = json.loads(path.read_bytes().decode("utf-8"))
            return [
                issue_key(i["repo"], i["number"])
                for i in (*raw["assigned"], *raw["plan_requests"])
            ]
        except (OSError, ValueError, KeyError, TypeError, RecursionError):
            return []

    def _ack_step(self) -> None:
        """Move entries whose wake was acknowledged (3.6). A dry run has no acknowledgments."""
        if self.dry_run:
            return
        assert self.doc is not None
        by_wake: dict[str, list[tuple[str, str]]] = {}
        for key, e in self.doc.entries.items():
            if e.wake_id and (
                e.state in ("pending", "woken", "unknown")
                or (e.state == "abandoned" and e.last_reason == "ack_not_observed")
            ):
                by_wake.setdefault(e.wake_id, []).append(("entry", key))
        for key, h in self.doc.holds.items():
            if h.plan_wake_id and h.plan_request in ("pending", "woken"):
                by_wake.setdefault(h.plan_wake_id, []).append(("plan", key))
        cfg = self.deps.config
        done: list[str] = []
        for wake_id in sorted(by_wake):
            ack = wake.read_ack(cfg.orchestrator_repo, wake_id)
            if ack is None:
                continue
            keys = self._wake_item_keys(wake_id) if ack.rejected_indexes else []
            rejected = {keys[i] for i in ack.rejected_indexes if i < len(keys)}
            decided = 0
            for kind, key in by_wake[wake_id]:
                repo, number = split_issue_key(key)
                reason: str | None
                if (repo, number) in ack.taken:
                    reason = None
                elif (repo, number) in ack.skipped:
                    reason = ack.skipped[(repo, number)]
                elif key in rejected:
                    reason = "malformed_item"
                else:
                    continue
                decided += 1
                if kind == "entry":
                    self._set(record.mark_acked(self.doc, key, self.now(), reason))
                    e = self.doc.entries[key]
                    self._decision(
                        "acked", repo, number, "acked",
                        orchestrator=e.orchestrator, wake_id=wake_id,
                    )  # fmt: skip
                else:
                    h = self.doc.holds[key]
                    changed = (
                        replace(h, plan_request="acked", plan_acked_at=self.now())
                        if reason is None
                        else replace(h, plan_request="skipped")
                    )
                    self._set(record.set_hold(self.doc, key, changed))
                    self._decision(
                        "acked", repo, number,
                        orchestrator=h.plan_request_orchestrator, wake_id=wake_id,
                    )  # fmt: skip
            if decided == len(by_wake[wake_id]):
                done.append(wake_id)
        if done:
            self._save()  # the transitions are durable before the files move away
            for wake_id in done:
                wake.move_to_done(cfg.orchestrator_repo, wake_id)

    # -- step 6: the sweep ----------------------------------------------------

    def _sweep(self) -> None:
        assert self.doc is not None
        now = self.now()
        swept = record.sweep(self.doc, now)
        if swept.orphans or swept.abandoned or swept.resend:
            self._set(swept.doc)  # a dry run keeps it in memory only
        for e in swept.abandoned:
            self._cond("ack_not_observed")
            self._decision(
                "ack_not_observed", e.repo, e.issue, "abandoned",
                orchestrator=e.orchestrator,
            )  # fmt: skip
        for key in swept.orphans:
            e = swept.doc.entries[key]
            self._decision(
                "pending_orphan",
                e.repo,
                e.issue,
                "pending",
                orchestrator=e.orchestrator,
            )
        self.resend_keys = [e.key for e in swept.resend]
        self._sweep_plans(now)

    def _sweep_plans(self, now: datetime) -> None:
        """Resend plan requests like wakes; raise ``plan_stuck`` once for a lost plan call."""
        assert self.doc is not None
        cfg = self.deps.config
        for key in sorted(self.doc.holds):
            h = self.doc.holds[key]
            repo, number = split_issue_key(key)
            if h.state != "held":
                continue  # the label was taken off by hand: the request is moot (the hold ended)
            if h.plan_request == "pending":
                self.plan_resend_keys.append(key)
            elif h.plan_request == "woken" and (
                h.plan_woken_at is None or now >= h.plan_woken_at + record.LEASE
            ):
                if h.plan_attempts >= record.MAX_WAKE_ATTEMPTS:
                    self._set(
                        record.set_hold(
                            self.doc, key, replace(h, plan_request="abandoned")
                        )
                    )
                    self._cond("ack_not_observed")
                    self._decision(
                        "ack_not_observed", repo, number, "abandoned",
                        orchestrator=h.plan_request_orchestrator,
                    )  # fmt: skip
                else:
                    self._set(
                        record.set_hold(
                            self.doc, key, replace(h, plan_request="pending")
                        )
                    )
                    self.plan_resend_keys.append(key)
            elif (
                h.plan_request == "acked"
                and h.plan_acked_at is not None
                and h.plan_requested_at is not None
                and now - h.plan_acked_at
                >= timedelta(minutes=hold.PLAN_CALL_MAX_MINUTES)
            ):
                status = route.plan_record_status(
                    cfg.orchestrator_repo, repo, number, h.plan_requested_at
                )
                if status in (None, "in_progress"):
                    self._set(
                        record.set_hold(self.doc, key, replace(h, plan_request="stuck"))
                    )
                    self._cond("plan_stuck")  # raised once: the entry is now ``stuck``
                    self._decision(
                        "plan_stuck",
                        repo,
                        number,
                        orchestrator=h.plan_request_orchestrator,
                    )

    # -- step 7: discovery ------------------------------------------------------

    def _val(self, read: github.Read) -> object:
        """Return the value of a shared read, or raise the stop."""
        if read.reason is None:
            return read.value
        if read.kind == "rate_limited":
            raise self._rate_stop()
        raise _Stop(read.reason)

    def _discover(self) -> None:
        assert self.doc is not None and self.rdoc is not None
        d = self.deps
        login = self.login or ""
        for org in self.rdoc.orgs:
            rows = self._val(
                github.search_assigned(d.runner, org, login, self._tf_shared)
            )
            self.s1.extend(rows)  # type: ignore[arg-type]
        seen_keys = [r.key for r in self.s1]
        if len(set(seen_keys)) != len(seen_keys):
            raise _Stop("discovery_duplicate")
        self.s1_done = True
        self.discovery_count = len(self.s1)
        if len(self.s1) >= DISCOVERY_WARN:
            self._warn("discovery_count", discovery_count=len(self.s1))
        since = (self.doc.last_poll_at or self.doc.created_at) - INFO_OVERLAP
        seen = set(self.doc.info_seen)
        found: dict[str, InfoItem] = {}
        for org in self.rdoc.orgs:
            for stream in github.STREAMS:
                rows = self._val(
                    github.search_info(
                        d.runner, stream, org, login, since, self._tf_shared
                    )
                )
                if len(rows) >= github.DISCOVERY_BOUND:  # type: ignore[arg-type]
                    self._warn("discovery_count", discovery_count=len(rows))  # type: ignore[arg-type]
                for item in rows:  # type: ignore[attr-defined]
                    if stream == "could_assign" and self.rdoc.get(item.repo) is None:
                        continue  # S3 is kept only for repos in the list
                    if item.seen_key not in seen:
                        found.setdefault(item.seen_key, item)
        self.info_new = [found[k] for k in sorted(found)]
        self._set(record.prune_holds(self.doc, seen_keys))

    def _baseline(self) -> None:
        """The first cycle after ``init-state``: every issue already assigned counts as seen (4.3 rule 5)."""
        assert self.doc is not None and self.created_at is not None
        doc = self.doc
        for row in self.s1:
            doc = record.record_seen(doc, row.repo, row.number, "baseline", self.now())
        doc = record.add_info_seen(doc, (i.seen_key for i in self.info_new))
        self._set(record.end_baseline(doc))
        self.info_new = []

    # -- steps 7a and 8: the hold and the filters -----------------------------------

    def _day_cap_reached(self) -> bool:
        assert self.doc is not None
        used = record.day_cap_count(self.doc, self.now()) + self.reserved_day_cap
        return used >= DAY_CAP

    def _select(self) -> None:
        assert (
            self.doc is not None
            and self.rdoc is not None
            and self.created_at is not None
        )
        for row in sorted(self.s1, key=lambda r: (r.repo, r.number)):
            if len(self.cands) >= MAX_CANDIDATES:
                break
            entry = self.doc.entries.get(row.key)
            try:
                c = self._examine(row, entry)
            except _Skip as skip:
                self._skip(row, skip.reason)
                continue
            if c is not None:
                self.cands.append(c)
        # the hold step reserves a place of the day cap for each plan request it queued
        self.plan_due.sort(key=lambda c: (c.row.repo, c.row.number))

    def _skip(self, row: DiscoveredIssue, reason: str) -> None:
        assert self.doc is not None
        if reason in _SEEN_SKIPS:
            self._set(
                record.record_seen(self.doc, row.repo, row.number, reason, self.now())
            )
        if reason in ("repo_not_listed", "repo_disabled", "assigned_other", "day_cap"):
            self.skips.append(wake.SkippedItem(row.repo, row.number, reason))
        self._decision(reason, row.repo, row.number)

    def _examine(self, row: DiscoveredIssue, entry: Entry | None) -> _Cand | None:
        """Steps 7a and 8 for one S1 issue: a candidate, None (clear but not new), or ``_Skip``."""
        assert (
            self.doc is not None
            and self.rdoc is not None
            and self.created_at is not None
        )
        if entry is not None:
            if entry.state != "failed":
                return None  # already woken, acknowledged or abandoned: never woken again (4.3)
            if not record.backoff_elapsed(entry, self.now()):
                raise _Skip("in_backoff")
        repo_entry = self.rdoc.get(row.repo)
        if repo_entry is None:
            raise _Skip("repo_not_listed")
        if not repo_entry.enabled:
            raise _Skip("repo_disabled")
        owned, why = predicates.is_intended_owner(row.assignees, self.login or "")
        if not owned:
            raise _Skip(why or "assigned_other")
        verdict = self._hold_step(row, entry)
        if verdict == "skip":
            return None
        if self._day_cap_reached():
            raise _Skip("day_cap")
        self.reserved_day_cap += 1
        first = entry.created_at if entry is not None else self.created_at
        if verdict == "request":
            h = self.doc.holds[row.key]
            c = _Cand(
                row, entry, first, hold=h, missing=hold.plan_check(row.body).missing
            )
            self.plan_due.append(c)
            return None
        return _Cand(row, entry, first)

    def _hold_write_ok(self, row: DiscoveredIssue) -> bool:
        """The grant ``issue.hold`` is required for every write of the hold (DQ6)."""
        assert self.rdoc is not None
        if self.rdoc.has_grant("issue.hold"):
            return True
        self._warn("hold_write_failed", repo=row.repo, issue=row.number)
        return False

    def _label_write(self, row: DiscoveredIssue, remove: bool) -> bool:
        """Ensure, add or remove the label; False (a warning is written) when it fails."""
        write = self.labels
        results = []
        if not remove:
            results.append(write.ensure(self.budget, row.repo, self._tf))
        if not results or results[0].reason is None:
            op = write.remove if remove else write.add
            results.append(op(self.budget, row.repo, row.number, self._tf))
        failed = next((r for r in results if r.reason is not None), None)
        if failed is None:
            return True
        if failed.kind == "rate_limited":
            raise self._rate_stop()
        self._warn("hold_write_failed", repo=row.repo, issue=row.number)
        return False

    def _hold_step(self, row: DiscoveredIssue, entry: Entry | None) -> str:
        """The decision table of 4.11 point 3: ``clear`` (go on), ``skip`` or ``request``."""
        assert self.doc is not None and self.created_at is not None
        now = self.now()
        check = hold.plan_check(row.body)
        h = self.doc.holds.get(row.key)
        label = predicates.HOLD_LABEL in row.labels
        if self.dry_run and h is not None and h.state == "held":
            label = True  # a dry run wrote no label: the shadow entry stands for it
        backlog = predicates.BACKLOG_LABEL in row.labels
        number = hold.table_row(backlog=backlog, passes=check.ok, label=label, entry=h)
        if number == 1:  # nothing else, ever, while the label stands
            self._decision("held_backlog", row.repo, row.number)
            return "skip"
        if number == 2:  # clear; a left-over entry is dropped (finding F1)
            if h is not None:
                self._set(record.drop_hold(self.doc, row.key))
            return "clear"
        if number == 3:  # the plan exists: lift the hold, wake next cycle
            if self.dry_run:
                self.would_release.append(row.key)
            elif not self._hold_write_ok(row) or not self._label_write(
                row, remove=True
            ):
                return "skip"
            self._set(record.drop_hold(self.doc, row.key))
            self._decision("hold_released", row.repo, row.number)
            return "skip"
        if number == 4:  # no plan, no label, no entry: hold it
            seen = row.updated_at
            if self.dry_run:
                self.would_hold.append(row.key)
            else:
                if not self._hold_write_ok(row) or not self._label_write(
                    row, remove=False
                ):
                    return "skip"
                read = github.issue_updated_at(
                    self.deps.runner, self.budget, row.repo, row.number, self._tf
                )
                if read.reason is None:
                    seen = read.value  # type: ignore[assignment]
            self._set(
                record.set_hold(
                    self.doc, row.key, hold.new_hold(now, seen, check.missing)
                )
            )
            self._decision("hold_applied", row.repo, row.number)
            return "skip"
        assert h is not None or number == 6
        if number == 5:
            if h.state == "hand_removed":  # no call is made for it again
                self._decision("hold_removed_by_hand", row.repo, row.number)
                return "skip"
            read = github.issue_labels(
                self.deps.runner, self.budget, row.repo, row.number, self._tf
            )
            if read.reason is not None:
                if read.kind == "rate_limited":
                    raise self._rate_stop()
                self._decision("budget_exhausted", row.repo, row.number)
                return "skip"
            if predicates.HOLD_LABEL not in read.value:  # type: ignore[operator]
                self._set(
                    record.set_hold(self.doc, row.key, replace(h, state="hand_removed"))
                )
                self._decision("hold_removed_by_hand", row.repo, row.number)
                return "skip"
        return self._held(row, h, check.missing, now)

    def _held(
        self,
        row: DiscoveredIssue,
        h: Hold | None,
        missing: tuple[str, ...],
        now: datetime,
    ) -> str:
        """Row 6: the issue is held. Wait for plan work elsewhere, then ask for a plan."""
        assert self.doc is not None
        if h is None or h.state == "hand_removed":
            h = hold.new_hold(
                now, row.updated_at, missing
            )  # a label put back restarts the hour
        else:
            h = replace(h, missing=missing)
            seen = h.seen_updated_at
            if seen is None or row.updated_at > seen:  # E1: any change by anyone
                h = hold.with_evidence(h, row.updated_at, "edit")
        if hold.plan_request_due(h, now):
            if self._day_cap_reached():
                self._set(record.set_hold(self.doc, row.key, h))
                raise _Skip("day_cap")
            h = self._evidence(row, h, now)
            if h is None:
                self._decision("held_incomplete", row.repo, row.number)
                return "skip"
            if hold.plan_request_due(h, now):
                self._set(record.set_hold(self.doc, row.key, h))
                return "request"
        self._set(record.set_hold(self.doc, row.key, h))
        self._decision("held_incomplete", row.repo, row.number)
        return "skip"

    def _read_failed(self, read: github.Read) -> bool:
        """True when an evidence read failed and the request waits; a rate limit stops the cycle."""
        if read.reason is None:
            return False
        if read.kind == "rate_limited":
            raise self._rate_stop()
        return True

    def _evidence(self, row: DiscoveredIssue, h: Hold, now: datetime) -> Hold | None:
        """E2 to E4, read once at the moment the request would go out (4.11 point 5).

        Returns the entry with the newest signal, or None when a read could not
        be made (the request waits for the next cycle).
        """
        d = self.deps
        found = github.linked_branches(
            d.runner, self.budget, row.repo, row.number, self._tf
        )
        if self._read_failed(found):
            return None
        for name in found.value[:MAX_EVIDENCE_BRANCHES]:  # type: ignore[index]
            when = github.branch_date(d.runner, self.budget, row.repo, name, self._tf)
            if self._read_failed(when):
                return None
            h = hold.with_evidence(h, when.value, "branch")  # type: ignore[arg-type]
        stamp = github.timeline_evidence(
            d.runner, self.budget, row.repo, row.number, self._tf
        )
        if self._read_failed(stamp):
            return None
        if stamp.value is not None:
            h = hold.with_evidence(h, stamp.value, "pull_request")  # type: ignore[arg-type]
        orca = self._find_orca()
        timeout = self.deadline.timeout_for(PROBE_TIMEOUT_S)
        if timeout is None:
            return None
        alive = hold.session_evidence(
            d.runner, orca, row.number, wake.issue_url(row.repo, row.number), timeout
        )
        if alive is None:
            return None
        if alive:
            h = hold.with_evidence(h, now, "session")
        return h

    # -- step 9: the re-read and the origin check -------------------------------------

    def _rv(self, read: github.Read) -> object:
        """A re-read result: the value, or the skip, the stop or the transient."""
        if read.reason is None:
            return read.value
        if read.kind == "rate_limited":
            raise self._rate_stop()
        if read.kind == "budget_exhausted":
            raise _Skip("budget_exhausted")
        if read.kind in ("timeout", "transient"):
            raise _Transient
        raise _Skip("revalidation_failed")

    def _checkout(self, row: DiscoveredIssue) -> str:
        """The per-repo origin check (4.4): ``ok`` or ``missing``; a mismatch is skipped."""
        return self._checkout_of(row.repo)

    def _checkout_of(self, repo: str) -> str:
        assert self.rdoc is not None
        entry = self.rdoc.get(repo)
        if entry is None:
            # a stored entry of a repo that repos.yaml no longer lists (removed by hand)
            raise _Skip("repo_not_listed")
        state = self.origin_state.get(entry.repo)
        if state is None:
            if entry.checkout is None or not os.path.isdir(entry.checkout):
                state = "missing" if entry.clone_parent is not None else "no_checkout"
            else:
                timeout = self.deadline.timeout_for(GIT_TIMEOUT_S)
                if timeout is None:
                    raise _Skip("budget_exhausted")
                bad = launch.check_origin(
                    self.deps.runner, entry.checkout, entry.repo, timeout
                )
                if bad is not None:
                    self._cond(
                        "origin_mismatch"
                    )  # exit 2: a checkout names another repo
                state = "origin_mismatch" if bad else "ok"
            self.origin_state[entry.repo] = state
        if state == "no_checkout":
            raise _Skip("checkout_missing")
        if state == "origin_mismatch":
            raise _Skip("origin_mismatch")
        return state

    def _fail(self, c: _Cand, reason: str) -> None:
        assert self.doc is not None
        self._set(record.fail(self.doc, c.row.repo, c.row.number, reason, self.now()))
        self._cond(reason)  # exit 7, also when the third failure abandons it
        entry = self.doc.entries[c.row.key]
        shown = entry.last_reason if entry.state == "abandoned" else reason
        self._decision(shown or reason, c.row.repo, c.row.number, entry.state)

    def _reread(self) -> None:
        """Step 9: re-read each candidate once (4.5); the check must still give the same answer."""
        keep: list[_Cand] = []
        for c in self.cands:
            try:
                self._check_candidate(c, plan=False)
            except _Skip as skip:
                self._skip(c.row, skip.reason)
            except _Transient:
                self._fail(c, "revalidation_transient")
            else:
                keep.append(c)
        self.cands = keep
        keep = []
        for c in self.plan_due:
            try:
                self._check_candidate(c, plan=True)
            except _Skip as skip:
                self._skip(c.row, skip.reason)
            except _Transient:
                self._decision("revalidation_transient", c.row.repo, c.row.number)
            else:
                keep.append(c)
        self.plan_due = keep

    def _check_candidate(self, c: _Cand, *, plan: bool) -> None:
        assert self.doc is not None
        snap: predicates.IssueSnapshot = self._rv(  # type: ignore[assignment]
            github.reread(
                self.deps.runner, self.budget, c.row.repo, c.row.number, self._tf
            )
        )
        if snap.state.lower() != "open":
            raise _Skip("revalidation_failed")
        owned, why = predicates.is_intended_owner(snap.assignees, self.login or "")
        if not owned:
            raise _Skip(why or "assigned_other")
        if predicates.BACKLOG_LABEL in snap.labels:
            raise _Skip("held_backlog")
        passes = hold.plan_check(snap.body).ok
        has_label = predicates.HOLD_LABEL in snap.labels
        if plan:
            # it must still fail and the label must still be there (a dry run wrote none)
            if passes or not (has_label or self.dry_run):
                raise _Skip("revalidation_failed")
        elif not passes or has_label:
            raise _Skip("revalidation_failed")
        if self.deps.store.disabled():
            raise _Stop("disabled_mid_cycle")
        c.checkout_state = self._checkout(c.row)
        if not self.deadline.launch_allowed():
            raise _Skip("budget_exhausted")

    # -- steps 10 and 11: route and wake -------------------------------------------------

    def _make_wake_id(self) -> str:
        assert self.created_at is not None
        token = self.deps.wake_token() if self.deps.wake_token else None
        return wake.new_wake_id(self.created_at, token)

    def _checkout_for(self, repo: str) -> str:
        try:
            return self._checkout_of(repo)
        except _Skip:
            return "origin_mismatch"

    def _route_and_wake(self) -> None:
        assert (
            self.doc is not None
            and self.rdoc is not None
            and self.created_at is not None
        )
        cfg = self.deps.config
        # What must go out: new assignments, resends, plan requests (new and resent).
        resend_entries = [
            self.doc.entries[k] for k in self.resend_keys if k in self.doc.entries
        ]
        plan_resends = [  # a hold the hold step ended this cycle (label removed by hand) sends nothing
            (k, self.doc.holds[k])
            for k in self.plan_resend_keys
            if k in self.doc.holds and self.doc.holds[k].state == "held"
        ]
        s1_by_key = {r.key: r for r in self.s1}
        if self.dry_run:
            self._dry_route()
            return
        work = bool(self.cands or self.plan_due or resend_entries or plan_resends)
        if not work:
            # Nothing new and nothing to resend: no wake file, no mailbox message,
            # no typed line, no session start (4.3 rule 6). Only a registry that
            # holds an active orchestrator needs a look (its session may be gone
            # with work in flight) and can take the information items.
            try:
                registry = route.load_registry(cfg.orchestrator_repo)
            except route.RegistryError:
                raise _Stop("registry_invalid") from None
            if not any(e.status == "active" for e in registry.values()):
                return
        orca = self._find_orca()
        if orca is None:
            if work:
                raise _Stop("orca_not_found")
            return
        wakes, keys_of = self._plan_wakes(orca, resend_entries, plan_resends, s1_by_key)
        self._send_wakes(orca, wakes, keys_of)

    def _plan_wakes(
        self,
        orca: str,
        resend_entries: list[Entry],
        plan_resends: list[tuple[str, Hold]],
        s1_by_key: dict[str, DiscoveredIssue],
    ) -> tuple[list[tuple[wake.Wake, str | None]], dict[str, list[tuple[str, str]]]]:
        """Step 10 under ``.orchestrator/state.lock``: route, save ``pending``, write the wake files."""
        assert (
            self.doc is not None
            and self.rdoc is not None
            and self.created_at is not None
        )
        cfg, now = self.deps.config, self.now()
        try:
            with route.state_lock(cfg.orchestrator_repo):
                return self._route_locked(
                    orca, resend_entries, plan_resends, s1_by_key, now
                )
        except route.StateLockBusy:
            raise _Stop("lock_held") from None
        except route.RegistryError:
            raise _Stop("registry_invalid") from None
        except OSError:
            raise _Stop("state_dir_unwritable") from None

    def _run_status(self, ident: str) -> str | None:
        return route.read_run(self.deps.config.orchestrator_repo, ident).status

    def _route_locked(
        self,
        orca: str,
        resend_entries: list[Entry],
        plan_resends: list[tuple[str, Hold]],
        s1_by_key: dict[str, DiscoveredIssue],
        now: datetime,
    ):
        assert (
            self.doc is not None
            and self.rdoc is not None
            and self.created_at is not None
        )
        cfg = self.deps.config
        registry = route.load_registry(cfg.orchestrator_repo)
        before = dict(registry)
        state_files = route.read_state_files(cfg.orchestrator_repo)

        def plan_status(repo: str, n: int, at: datetime) -> str | None:
            return route.plan_record_status(cfg.orchestrator_repo, repo, n, at)

        counts = route.in_flight(registry, self.doc, state_files, plan_status)
        in_progress = {
            sf.orchestrator
            for sf in state_files.values()
            if sf.orchestrator and sf.readable and sf.status == "in_progress"
        } | route.plan_in_progress(self.doc, plan_status)
        live: dict[str, bool | None] = {}
        for e in registry.values():
            if e.status == "active":
                found = self.deps.waker.find_session(
                    orca,
                    cfg.orchestrator_repo,
                    e.tag,
                    self.deadline.timeout_for(PROBE_TIMEOUT_S) or 1.0,
                )
                live[e.id] = None if found is None else bool(found)
        _, resume = route.end_finished(
            registry, counts, in_progress, self._run_status, lambda e: live.get(e.id)
        )
        prefix = cfg.session_tag_prefix
        order = sorted((c.row.repo, c.row.number) for c in self.cands)
        routed = [
            r
            for r in route.route(
                registry, counts, order, self.rdoc, prefix, now, self._run_status
            )
            if isinstance(r, route.Routed)
        ]
        plan_order = sorted((c.row.repo, c.row.number) for c in self.plan_due)
        plan_routed = [
            r
            for r in route.route(
                registry,
                counts,
                plan_order,
                self.rdoc,
                prefix,
                now,
                self._run_status,
                plan_requests=True,
            )  # fmt: skip
            if isinstance(r, route.Routed)
        ]
        # The registry first, then the entries: a crash in between leaves an empty
        # orchestrator, never an entry routed to an id the registry does not know.
        if registry != before:
            route.save_registry(cfg.orchestrator_repo, registry)
        by_key = {c.row.key: c for c in self.cands}
        doc = self.doc
        for r in routed:
            doc = record.mark_pending(doc, r.repo, r.number, r.orchestrator, now)
        for r in plan_routed:
            h = doc.holds[r.key]
            doc = record.set_hold(
                doc,
                r.key,
                replace(
                    h,
                    plan_requested_at=now,
                    plan_request_orchestrator=r.orchestrator,
                    plan_request="pending",
                    plan_attempts=0,
                    plan_wake_id=None,
                    plan_woken_at=None,
                ),
            )
            doc = record.add_consumed(doc, now)
            self._decision(
                "plan_requested", r.repo, r.number, orchestrator=r.orchestrator
            )
        self._set(doc)
        self._save()  # FR-010: durable before anything is sent

        # Group everything by orchestrator and build the wakes.
        items: dict[str, dict[str, list]] = {}

        def bucket(ident: str) -> dict[str, list]:
            return items.setdefault(ident, {"assigned": [], "plans": [], "keys": []})

        for r in routed:
            c = by_key[r.key]
            b = bucket(r.orchestrator)
            b["assigned"].append(
                wake.AssignedItem(
                    r.repo,
                    r.number,
                    tuple(sorted(c.row.assignees)),
                    c.first_seen_at,
                    c.checkout_state,
                )
            )
            b["keys"].append(("entry", r.key))
        for e in resend_entries:
            if e.orchestrator is None or e.orchestrator not in registry:
                continue
            state = self._checkout_for(e.repo)
            if state == "origin_mismatch":
                continue
            row = s1_by_key.get(e.key)
            names = tuple(sorted(row.assignees)) if row else (self.login or "",)
            b = bucket(e.orchestrator)
            b["assigned"].append(
                wake.AssignedItem(e.repo, e.issue, names, e.created_at, state)
            )
            b["keys"].append(("entry", e.key))
        plan_keys = [(r.key, r.orchestrator) for r in plan_routed] + [
            (k, h.plan_request_orchestrator)
            for k, h in plan_resends
            if h.plan_request_orchestrator
        ]
        for key, ident in plan_keys:
            if ident is None or ident not in registry:
                continue
            row = s1_by_key.get(key)
            h = doc.holds[key]
            if (
                row is None
                or h.plan_requested_at is None
                or predicates.BACKLOG_LABEL in row.labels  # deferred since the request
            ):
                continue
            bucket(ident)["plans"].append(
                wake.PlanRequestItem(
                    row.repo,
                    row.number,
                    wake.clean_title(row.title),
                    wake.issue_url(row.repo, row.number),
                    h.missing or hold.plan_check(row.body).missing,
                    h.first_held_at,
                    h.plan_requested_at,
                )
            )
            bucket(ident)["keys"].append(("plan", key))
        for ident in resume:
            bucket(ident)  # an empty bucket is a resume wake
        wakes: list[tuple[wake.Wake, str | None]] = []
        keys_of: dict[str, list[tuple[str, str]]] = {}
        first = True
        for ident in sorted(items, key=lambda i: (registry[i].repo, route.n_of(i))):
            b = items[ident]
            entry = registry[ident]
            is_resume = ident in resume and not b["assigned"] and not b["plans"]
            chunks_a = [
                b["assigned"][i : i + wake.MAX_ASSIGNED]
                for i in range(0, len(b["assigned"]), wake.MAX_ASSIGNED)
            ]
            chunks_p = [
                b["plans"][i : i + wake.MAX_PLAN_REQUESTS]
                for i in range(0, len(b["plans"]), wake.MAX_PLAN_REQUESTS)
            ]
            count = max(len(chunks_a), len(chunks_p), 1)
            for n in range(count):
                assigned = tuple(chunks_a[n]) if n < len(chunks_a) else ()
                plans = tuple(chunks_p[n]) if n < len(chunks_p) else ()
                wid = self._make_wake_id()
                attempt = 1
                for a in assigned:
                    prior = self.doc.entries.get(issue_key(a.repo, a.number))
                    if prior is not None:
                        attempt = max(attempt, min(3, prior.wake_attempts + 1))
                for p in plans:
                    hh = self.doc.holds.get(issue_key(p.repo, p.number))
                    if hh is not None:
                        attempt = max(attempt, min(3, hh.plan_attempts + 1))
                w = wake.Wake(
                    wake_id=wid,
                    created_at=self.created_at,
                    cycle_id=self.cycle_id,
                    host=self.deps.host,
                    login=self.login or "",
                    since=(self.doc.last_poll_at or self.doc.created_at) - INFO_OVERLAP,
                    gh_calls=self.budget.total,
                    target=wake.WakeTarget(ident, entry.tag, entry.repo, is_resume),
                    attempt=attempt,
                    assigned=assigned,
                    plan_requests=plans,
                )
                if first and not is_resume:
                    w = self._with_extras(w)
                    first = False
                try:
                    wake.write_wake_file(cfg.orchestrator_repo, w)
                except wake.WakeError:
                    self._cond("wake_write_failed")
                    continue
                wakes.append((w, ident))
                keys_of[wid] = _keys_of_wake(b["keys"], assigned, plans)
        if first and self.info_new:  # information only: the first active orchestrator
            active = sorted(
                (e for e in registry.values() if e.status == "active"),
                key=lambda e: (e.repo, route.n_of(e.id)),
            )
            if active:
                e = active[0]
                w = wake.Wake(
                    wake_id=self._make_wake_id(),
                    created_at=self.created_at,
                    cycle_id=self.cycle_id,
                    host=self.deps.host,
                    login=self.login or "",
                    since=(self.doc.last_poll_at or self.doc.created_at) - INFO_OVERLAP,
                    gh_calls=self.budget.total,
                    target=wake.WakeTarget(e.id, e.tag, e.repo, False),
                    attempt=1,
                )
                w = self._with_extras(w)
                try:
                    wake.write_wake_file(cfg.orchestrator_repo, w)
                    wakes.append((w, e.id))
                    keys_of[w.wake_id] = []
                except wake.WakeError:
                    self._cond("wake_write_failed")
        self._registry = registry
        return wakes, keys_of

    def _with_extras(self, w: wake.Wake) -> wake.Wake:
        """The information items and the skipped list ride on the first wake of the cycle."""

        def refs(stream: str) -> tuple[wake.InfoRef, ...]:
            return tuple(
                wake.InfoRef(i.repo, i.number, i.kind, i.updated_at)
                for i in self.info_new
                if i.stream == stream
            )[: wake.MAX_INFO]

        return replace(
            w,
            mentions=refs("mentions"),
            could_assign=refs("could_assign"),
            affects=refs("affects"),
            skipped=tuple(self.skips[: wake.MAX_SKIPPED]),
        )

    def _send_wakes(
        self,
        orca: str,
        wakes: list[tuple[wake.Wake, str | None]],
        keys_of: dict[str, list[tuple[str, str]]],
    ) -> None:
        """Step 11: deliver each wake to exactly its target, then mark the entries."""
        assert self.doc is not None
        cfg = self.deps.config
        registry: route.Registry = self._registry
        for w, ident in wakes:
            if not self.deadline.launch_allowed():
                break  # the rest stay ``pending`` and are sent next cycle as orphans
            timeout = self.deadline.timeout_for(LAUNCH_TIMEOUT_S)
            if timeout is None or ident is None:
                break
            entry = registry[ident]
            rdoc_entry = self.rdoc.get(entry.repo) if self.rdoc else None  # type: ignore[union-attr]
            tier = (
                rdoc_entry.orchestrator_tier
                if rdoc_entry
                else repos.DEFAULT_TIERS["orchestrator_tier"]
            )
            run = route.read_run(cfg.orchestrator_repo, ident)
            target = wake.WakeTargetRun(
                ident, entry.tag, cfg.orchestrator_repo, run.run_id, tier
            )
            info_only = not keys_of.get(w.wake_id) and not w.target.resume
            out = self.deps.waker.deliver(
                orca,
                target,
                w.wake_id,
                self.now(),
                timeout,
                start_session=not info_only,
            )
            self._after_delivery(w, ident, out, keys_of.get(w.wake_id, []), info_only)

    def _after_delivery(
        self,
        w: wake.Wake,
        ident: str,
        out: wake.WakeOutcome,
        keys: list[tuple[str, str]],
        info_only: bool,
    ) -> None:
        assert self.doc is not None
        now = self.now()
        stages = ",".join(out.stages) or None
        if out.mailbox == "unavailable":
            self._warn("mailbox_unavailable")
        if out.started and (out.tier or out.fallback_from):
            self._note_tier(ident, out)
        if info_only:
            if out.kind == "woken":
                self.info_sent += self._carried_info_keys(w)
            return
        for kind, key in keys:
            repo, number = split_issue_key(key)
            if kind == "plan":
                h = self.doc.holds[key]
                if out.kind == "spawn_error":  # as an entry: ended, never retried
                    self._set(
                        record.set_hold(
                            self.doc, key, replace(h, plan_request="abandoned")
                        )
                    )
                elif out.kind in ("woken", "unknown", "no_session"):
                    # every try counts, and the next one waits for the lease, like an entry
                    self._set(
                        record.set_hold(
                            self.doc,
                            key,
                            replace(
                                h,
                                plan_request="woken",
                                plan_wake_id=w.wake_id,
                                plan_woken_at=now,
                                plan_attempts=h.plan_attempts + 1,
                            ),
                        )
                    )
                if out.kind != "woken":
                    self._failure_cond(out)
                self._decision("woken" if out.kind == "woken" else _FAIL_REASON.get(out.kind, "wake_unknown"),
                               repo, number, orchestrator=ident, wake_id=w.wake_id, stages=stages)  # fmt: skip
                continue
            if out.kind == "woken":
                self._set(record.mark_woken(self.doc, key, w.wake_id, now))
                self.woken.append(key)
                self._decision("woken", repo, number, "woken", orchestrator=ident, wake_id=w.wake_id, stages=stages)  # fmt: skip
            elif out.kind == "spawn_error":
                self._set(record.mark_spawn_error(self.doc, key, now))
                self._failure_cond(out)
                self._decision(
                    "spawn_error", repo, number, "abandoned", orchestrator=ident
                )
            else:
                reason = "no_session" if out.kind == "no_session" else "wake_unknown"
                self._set(
                    record.mark_unknown(self.doc, key, w.wake_id, None, now, reason)
                )
                self._failure_cond(out)
                self._decision(reason, repo, number, "unknown", orchestrator=ident, wake_id=w.wake_id)  # fmt: skip
        if not keys and w.target.resume and out.kind != "woken":
            self._failure_cond(out)
        if out.kind == "woken":
            self.info_sent += self._carried_info_keys(w)

    def _carried_info_keys(self, w: wake.Wake) -> list[str]:
        """The ``info_seen`` keys of the information items this wake actually carries.

        Items cut by ``MAX_INFO``, and items riding on another wake, stay unseen
        so a later cycle can still deliver them.
        """
        carried = {
            (stream, r.repo, r.number, r.kind, r.updated_at)
            for stream, refs in (
                ("mentions", w.mentions),
                ("could_assign", w.could_assign),
                ("affects", w.affects),
            )
            for r in refs
        }
        return [
            i.seen_key
            for i in self.info_new
            if (i.stream, i.repo, i.number, i.kind, i.updated_at) in carried
        ]

    def _failure_cond(self, out: wake.WakeOutcome) -> None:
        self._cond(_FAIL_REASON.get(out.kind, "wake_unknown"))

    def _note_tier(self, ident: str, out: wake.WakeOutcome) -> None:
        """Record the tier the started session got, and the fallback, in the registry (5.8 point 3)."""
        cfg = self.deps.config
        try:
            with route.state_lock(cfg.orchestrator_repo):
                reg = route.load_registry(cfg.orchestrator_repo)
                if ident in reg:
                    reg[ident] = replace(
                        reg[ident], tier=out.tier, fallback_from=out.fallback_from
                    )
                    route.save_registry(cfg.orchestrator_repo, reg)
        except (route.StateLockBusy, route.RegistryError, OSError):
            pass  # the record is a convenience; the session itself is started

    # -- dry run ----------------------------------------------------------------------

    def _dry_route(self) -> None:
        """A dry run decides and reports; it writes no wake file, calls no Orca and saves no registry."""
        assert self.doc is not None and self.rdoc is not None
        cfg, now = self.deps.config, self.now()
        try:
            registry = route.load_registry(cfg.orchestrator_repo)
        except route.RegistryError:
            raise _Stop("registry_invalid") from None
        state_files = route.read_state_files(cfg.orchestrator_repo)
        counts = route.in_flight(
            registry, self.doc, state_files,
            lambda repo, n, at: route.plan_record_status(cfg.orchestrator_repo, repo, n, at),
        )  # fmt: skip
        order = sorted((c.row.repo, c.row.number) for c in self.cands)
        doc = self.doc
        for r in route.route(
            registry,
            counts,
            order,
            self.rdoc,
            cfg.session_tag_prefix,
            now,
            self._run_status,
        ):
            if not isinstance(r, route.Routed):
                continue
            doc = record.mark_pending(doc, r.repo, r.number, r.orchestrator, now)
            doc = record.mark_woken(doc, r.key, self._make_wake_id(), now)
            doc = record.mark_acked(
                doc, r.key, now, "dry_run"
            )  # the shadow never resends
            self.would_wake.append(r.key)
            self._decision("woken", r.repo, r.number, orchestrator=r.orchestrator)
        plan_order = sorted((c.row.repo, c.row.number) for c in self.plan_due)
        for r in route.route(
            registry,
            counts,
            plan_order,
            self.rdoc,
            cfg.session_tag_prefix,
            now,
            self._run_status,
            plan_requests=True,
        ):
            if not isinstance(r, route.Routed):
                continue
            h = doc.holds[r.key]
            doc = record.set_hold(
                doc, r.key,
                replace(h, plan_requested_at=now, plan_request_orchestrator=r.orchestrator, plan_request="skipped"),
            )  # fmt: skip
            doc = record.add_consumed(doc, now)
            self.would_request.append(r.key)
            self._decision(
                "plan_requested", r.repo, r.number, orchestrator=r.orchestrator
            )
        self._set(doc)

    # -- step 12 ----------------------------------------------------------------------

    def _commit(self) -> None:
        """Step 12: the one final write (the store, or the dry-run shadow)."""
        if self.stop_reason == "state_dir_unwritable":
            return
        try:
            if self.dry_run:
                self._commit_shadow()
            else:
                self._commit_store()
        except OSError:
            self._stopped("state_dir_unwritable")

    def _finished_doc(self) -> StoreDoc | None:
        doc = self.doc
        if doc is None:
            return None
        now = self.now()
        if self.s1_done and self.created_at is not None and self.stop_reason is None:
            doc = record.set_last_poll(doc, self.created_at)
        if self.info_sent:
            doc = record.add_info_seen(doc, self.info_sent)
        if not self.rate_limited:
            doc = replace(
                doc, rate_streak=0
            )  # a cycle with no rate limit ends the streak
        if self.stop_reason is None and self._exit() == 0:
            doc = record.set_last_completed(doc, now)  # health stamp
        return record.prune_consumed_log(doc, now)

    def _commit_store(self) -> None:
        doc = self._finished_doc()
        if doc is None:
            return
        if self.dirty or doc != self.doc or self.stop_reason is None:
            self.doc = doc
            self.deps.store.save(doc)
            self.dirty = False

    def _commit_shadow(self) -> None:
        doc = self._finished_doc()
        if doc is None or not self.s1_done:
            return
        record.save_dry_run(self.deps.store.state_dir, doc)

    def _cycle_reason(self, exit_code: int) -> str:
        if exit_code != 0:
            for reason, code in self.conds:
                if code == exit_code:
                    return reason
        if self.stop_reason is not None:
            return self.stop_reason
        # A cycle that ran to its end names the cycle-kind reason cycle_complete
        # (exit 0). A skip or entry reason belongs to a decision line, never to
        # this cycle line (DF-41).
        return "cycle_complete"

    def _mark_unread(self) -> None:
        """Mark the orchestrator workspace unread for an exit-7 condition (DQ2)."""
        if self.dry_run or not self.unread:
            return
        orca = self.orca if self.orca_checked else self._find_orca()
        timeout = self.deadline.timeout_for(PROBE_TIMEOUT_S)
        if orca is None or timeout is None:
            return
        self.deps.waker.mark_unread(
            orca, self.deps.config.orchestrator_repo, sorted(self.unread)[0], timeout
        )

    def _conclude(self, locked: bool) -> CycleResult:
        """Step 12: unread mark, decision lines, then the cycle line."""
        if locked:
            self._mark_unread()
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
            woken=tuple(self.woken),
            would_wake=tuple(self.would_wake),
            would_hold=tuple(self.would_hold),
            would_release=tuple(self.would_release),
            would_request=tuple(self.would_request),
            lines=lines,
        )


_FAIL_REASON = {
    "no_session": "no_session",
    "spawn_error": "spawn_error",
    "unknown": "wake_unknown",
}


def _keys_of_wake(
    keys: list[tuple[str, str]],
    assigned: tuple[wake.AssignedItem, ...],
    plans: tuple[wake.PlanRequestItem, ...],
) -> list[tuple[str, str]]:
    """The ``(kind, key)`` of the items of one wake out of those of its orchestrator."""
    have = {("entry", issue_key(a.repo, a.number)) for a in assigned} | {
        ("plan", issue_key(p.repo, p.number)) for p in plans
    }
    return [k for k in keys if k in have]


def routing_preview(
    config: Config, rdoc: repos.ReposDoc, store: Store, now: datetime
) -> list[dict]:
    """The routing ``check-config`` prints: per listed repo, its orchestrators and what each holds.

    Reads the registry, the state files and the store; writes nothing. Raises
    ``route.RegistryError`` for a registry that cannot be read.
    """
    registry = route.load_registry(config.orchestrator_repo)
    try:
        doc = _read_store_doc(store)
    except StoreError:
        doc = record.empty_doc(now)  # no store yet: only the state files count
    counts = route.in_flight(
        registry,
        doc,
        route.read_state_files(config.orchestrator_repo),
        lambda repo, n, at: route.plan_record_status(
            config.orchestrator_repo, repo, n, at
        ),
    )
    out = []
    for r in rdoc.repos:
        mine = sorted(
            (e for e in registry.values() if e.repo.lower() == r.repo.lower()),
            key=lambda e: route.n_of(e.id),
        )
        free = next(
            (
                e.id
                for e in mine
                if e.status == "active" and len(counts.get(e.id, ())) < r.max_in_flight
            ),
            None,
        )
        out.append(
            {
                "repo": r.repo,
                "short": r.short,
                "enabled": r.enabled,
                "max_in_flight": r.max_in_flight,
                "orchestrator_tier": r.orchestrator_tier,
                "orchestrators": [
                    {
                        "id": e.id,
                        "status": e.status,
                        "in_flight": len(counts.get(e.id, ())),
                    }
                    for e in mine
                ],
                "next_issue_goes_to": free
                or f"a new {route.orchestrator_id(r.short, route.next_n(registry, r.short))}",
            }
        )
    return out


def run_cycle(deps: Deps, dry_run: bool) -> CycleResult:
    """Run one poll cycle (design 4.5) and return what it did.

    ``check_platform`` is the caller's. Never calls ``subprocess`` (every
    command goes through ``deps.runner`` and ``deps.waker``), reads time only
    through ``deps.clock``, writes ``dispatch.json`` never in a dry-run, and
    leaves the lock to the context manager of ``deps.store.lock()``.
    """
    return _Cycle(deps, dry_run).run()


# --- Part 3: the status report and the SLO numbers (design 4.9, 10.2 and 10.3) -----

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
    """An ``unknown`` entry, or one ``abandoned`` as ``ack_not_observed``, older than 24 h."""
    if entry.state == "unknown":
        pass
    elif entry.state == "abandoned" and entry.last_reason == "ack_not_observed":
        pass
    else:
        return False
    return (now - entry.updated_at).total_seconds() > STALE_AGE_S


def status_report(
    store: Store,
    audit: audit.AuditLog | None,
    now: datetime,
) -> dict:
    """Return the ``status --json`` fields (design 10.2 and 4.11).

    Reads ``dispatch.json`` and the ``DISABLED`` mtime and nothing else: no
    lock, no write, no probe, no ``gh``. ``audit`` is accepted for the fixed
    signature and not read. Only typed scalars are returned, never issue text,
    and no command for a person to run (ruling R5). An unreadable store raises
    ``StoreError``. ``held`` lists each held issue with the signal that holds it
    (K26): the kind of the newest sign of plan work while its hour has not run,
    else None.
    """
    doc = _read_store_doc(store)
    last = doc.last_completed_cycle_at
    age = None if last is None else int((now - last).total_seconds())
    counts: dict[str, int] = {}
    for entry in doc.entries.values():
        counts[entry.state] = counts.get(entry.state, 0) + 1
    since = store.disabled_since()
    next_at = doc.next_permitted_at
    stale = [
        {
            "issue": key,
            "state": entry.state,
            "last_reason": entry.last_reason,
            "updated_at": format_utc(entry.updated_at),
        }
        for key, entry in sorted(doc.entries.items())
        if _is_stale(entry, now)
    ]
    held = []
    for key, h in sorted(doc.holds.items()):
        quiet = hold.quiet_since(h)
        waiting = now - quiet < timedelta(minutes=hold.HOLD_QUIET_MINUTES)
        held.append(
            {
                "issue": key,
                "state": h.state,
                "first_held_at": format_utc(h.first_held_at),
                "quiet_since": format_utc(quiet),
                "signal": h.evidence_kind if waiting and h.last_evidence_at else None,
                "plan_request": h.plan_request,
                "missing": list(h.missing),
            }
        )
    return {
        "healthy": age is not None and age <= HEALTH_AGE_S,
        "last_completed_cycle_age_seconds": age,
        "disabled_since": None if since is None else format_utc(since),
        "next_permitted_at": None if next_at is None else format_utc(next_at),
        "rate_streak": doc.rate_streak,
        "counts": counts,
        "day_cap_used": record.day_cap_count(doc, now),
        "baseline_pending": doc.baseline,
        "stale": stale,
        "held": held,
    }


@dataclass(frozen=True)
class SloNumbers:
    """NFR-013's four numbers; a share or p95 is None when it has no samples."""

    assignment_to_ack_p95_s: float | None
    cycle_exit0_share: float | None
    acked_within_lease_share: float | None
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

    The time that counts is assignment to acknowledgment (FU-10): from the first
    ``woken`` line of an issue to its ``acked`` line. Pure: no I/O. Dry-run
    lines count toward none of (a) to (c). A line that lacks a field, or holds a
    malformed time, drops out of the number that needs it and never raises.
    """
    waits: list[float] = []
    cycles = ok_cycles = 0
    first_woken: dict[tuple[str, int], datetime] = {}
    woken: list[tuple[tuple[str, int], datetime]] = []
    acked: dict[tuple[str, int], list[datetime]] = {}
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
        elif (
            kind == "decision"
            and type(ln.get("issue")) is int
            and isinstance(ln.get("repo"), str)
        ):
            who = (ln["repo"], ln["issue"])
            if reason == "woken":
                first_woken.setdefault(who, ts)
                woken.append((who, ts))
            elif reason == "acked":
                acked.setdefault(who, []).append(ts)
                start = first_woken.get(who)
                if start is not None:
                    waits.append((ts - start).total_seconds())
    p95 = None
    if waits:
        waits.sort()
        p95 = waits[-(-95 * len(waits) // 100) - 1]  # nearest rank: ceil(0.95 n)
    due = reached = 0
    for who, at in woken:
        end = at + record.LEASE
        hit = any(at <= c < end for c in acked.get(who, ()))
        if hit or now >= end:
            due += 1
            reached += hit
    return SloNumbers(
        assignment_to_ack_p95_s=p95,
        cycle_exit0_share=ok_cycles / cycles if cycles else None,
        acked_within_lease_share=reached / due if due else None,
        stale_count=sum(1 for e in doc.entries.values() if _is_stale(e, now)),
    )
