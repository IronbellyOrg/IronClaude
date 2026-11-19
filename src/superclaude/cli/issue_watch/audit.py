"""Audit log for the issue watcher: the closed reason table, the append-only
``audit.jsonl`` writer with rotation, the stderr fallback and the line builders.

The builders accept typed scalar fields only, and each value must also match a
closed shape (an enum, a fixed pattern or a range, see ``_RULES``). The one
exception is ``host`` and ``login``: they take any printable token of bounded
length (``login`` without whitespace), so a caller can still put arbitrary text
there. No issue title, body, label or stderr text has a key or a typed slot on
a line. This module imports nothing from the package and never reads the wall
clock for a decision.

The table has 62 reasons (design 4.7). ``origin_mismatch`` has ONE meaning, one
kind and one exit code (finding F4 of issue 665): the ``origin`` of a listed
repository's checkout does not name that repository (or the orchestrator
repository's own ``origin`` does not). It is a cycle reason with exit 2. For one
repository's checkout the issue is skipped, the cycle goes on and the exit code
is 2, so the owner sees it; an orchestrator that finds the same fault at wave 1
reports it to the poll only as the free text of its acknowledgment, never as
this reason. The acknowledgment skip reasons of an orchestrator (for example
``claimed_elsewhere``, ``malformed_item`` and ``co_assigned``) are NOT rows of
this table (finding F3 of issue 665): the poll stores them as the free
``ack_reason`` text of the entry, after a pattern check, and they never reach a
``reason`` key.
"""

from __future__ import annotations

import datetime
import json
import os
import re
import socket
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

# Closed reason table: name -> (kind, exit).
REASON_TABLE: dict[str, tuple[str, int]] = {
    # Cycle reasons, exit 2.
    "config_invalid": ("cycle", 2),
    "platform_unsupported": ("cycle", 2),
    "origin_mismatch": ("cycle", 2),
    "orca_not_found": ("cycle", 2),
    "account_id_mismatch": ("cycle", 2),
    "repos_invalid": ("cycle", 2),
    "orchestrator_repo_invalid": ("cycle", 2),
    "registry_invalid": ("cycle", 2),
    # Cycle reasons, exit 6.
    "store_invalid": ("cycle", 6),
    "store_missing": ("cycle", 6),
    "lock_missing": ("cycle", 6),
    "lock_invalid": ("cycle", 6),
    "state_dir_unwritable": ("cycle", 6),
    "wake_write_failed": ("cycle", 6),
    # Cycle reason, exit 7: a plan call taken and not finished in time (4.11).
    "plan_stuck": ("cycle", 7),
    # Cycle reasons, exit 3.
    "login_invalid": ("cycle", 3),
    "gh_auth_failed": ("cycle", 3),
    "gh_timeout": ("cycle", 3),
    "gh_non_json": ("cycle", 3),
    # Cycle reasons, exit 4.
    "truncated": ("cycle", 4),
    "discovery_duplicate": ("cycle", 4),
    # Cycle reasons, exit 5.
    "rate_limited": ("cycle", 5),
    "rate_limit_clamped": ("cycle", 5),
    # Cycle reason, exit 75.
    "lock_held": ("cycle", 75),
    # Cycle reason, exit 1: an unexpected exception out of ``run_cycle``,
    # written by ``once`` only.
    "cycle_crashed": ("cycle", 1),
    # Cycle reasons, exit 0.
    "disabled": ("cycle", 0),
    "disabled_mid_cycle": ("cycle", 0),
    "not_enabled": ("cycle", 0),
    # A cycle that ran to its end with no stop; its cycle line names this,
    # never a skip or entry reason.
    "cycle_complete": ("cycle", 0),
    # Skip reasons, exit 0.
    "unassigned": ("skip", 0),
    "assigned_other": ("skip", 0),
    "already_dispatched": ("skip", 0),
    "in_backoff": ("skip", 0),
    "day_cap": ("skip", 0),
    "budget_exhausted": ("skip", 0),
    "revalidation_failed": ("skip", 0),
    "repo_not_listed": ("skip", 0),
    "repo_disabled": ("skip", 0),
    "checkout_missing": ("skip", 0),
    "held_incomplete": ("skip", 0),
    "held_backlog": ("skip", 0),
    "hold_removed_by_hand": ("skip", 0),
    # Entry reasons.
    "wake_line_invalid": ("entry", 7),
    "revalidation_transient": ("entry", 7),
    "attempts_exhausted": ("entry", 7),
    "spawn_error": ("entry", 7),
    "wake_unknown": ("entry", 7),
    "no_session": ("entry", 7),
    "ack_not_observed": ("entry", 7),
    "pending_orphan": ("entry", 0),  # means "resend", never "abandon"
    "woken": ("entry", 0),
    "acked": ("entry", 0),
    # Hold notes (exit 0): the value of a ``note`` key, or the reason of a
    # decision line that has no skip reason of its own.
    "hold_applied": ("note", 0),
    "hold_released": ("note", 0),
    "plan_requested": ("note", 0),
    # Warning reasons.
    "discovery_count": ("warning", 0),
    "clock_skew": ("warning", 0),
    "dry_run_shadow_reset": ("warning", 0),
    "reset_refused": ("warning", 2),
    "mailbox_unavailable": ("warning", 0),
    "hold_write_failed": ("warning", 0),
    # Operator reset: decision line for an entry, warning line for the rate limit.
    "operator_reset": ("skip/warning", 0),
}

REASONS = frozenset(REASON_TABLE)

ROTATE_BYTES = 5 * 1024 * 1024
_ROTATIONS = 4


def _fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _encode(line: dict) -> bytes:
    text = json.dumps(line, sort_keys=True, ensure_ascii=True)
    return (text + "\n").encode("ascii")


class AuditLog:
    """Append-only ``state_dir / "audit.jsonl"`` with rotations ``.1`` to ``.4``."""

    def __init__(self, state_dir: Path) -> None:
        self.state_dir = Path(state_dir)
        self.path = self.state_dir / "audit.jsonl"

    def append(self, line: dict) -> None:
        """Write one JSON line with a single ``os.write`` on an append fd."""
        data = _encode(line)
        fd = os.open(self.path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        try:
            written = os.write(fd, data)
        finally:
            os.close(fd)
        if written != len(data):
            raise OSError(f"short audit write: {written} of {len(data)} bytes")

    def rotate_if_needed(self) -> None:
        """Rotate at ``ROTATE_BYTES`` or more; call only with the lock held."""
        try:
            size = os.stat(self.path).st_size
        except FileNotFoundError:
            return
        if size < ROTATE_BYTES:
            return
        base = str(self.path)
        for n in range(_ROTATIONS - 1, 0, -1):
            try:
                os.replace(f"{base}.{n}", f"{base}.{n + 1}")
            except FileNotFoundError:
                pass
        os.replace(base, f"{base}.1")
        _fsync_dir(self.state_dir)


_COMMON = frozenset({"kind", "ts", "host", "login", "cycle_id", "dry_run", "reason"})

# Line kind -> (required keys, optional keys).
_KEYS: dict[str, tuple[frozenset[str], frozenset[str]]] = {
    "cycle": (
        _COMMON | {"exit", "gh_calls", "duration_ms"},
        frozenset({"discovery_count", "clock_skew_s"}),
    ),
    "decision": (
        _COMMON | {"repo", "issue"},
        frozenset({"state", "note", "orchestrator", "wake_id", "stages"}),
    ),
    "warning": (
        _COMMON,
        frozenset({"repo", "issue", "discovery_count", "clock_skew_s"}),
    ),
}

# Key -> (accepted type, null allowed).
_TYPES: dict[str, tuple[type, bool]] = {
    "kind": (str, False),
    "ts": (str, False),
    "host": (str, False),
    "login": (str, True),
    "cycle_id": (str, False),
    "dry_run": (bool, False),
    "exit": (int, False),
    "reason": (str, False),
    "gh_calls": (int, False),
    "duration_ms": (int, False),
    "repo": (str, False),
    "issue": (int, False),
    "state": (str, False),
    "orchestrator": (str, False),
    "wake_id": (str, False),
    "stages": (str, False),
    "discovery_count": (int, False),
    "clock_skew_s": (int, False),
    "note": (str, False),
}


_UTC_TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
_UTC_TS_SHAPE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
_CYCLE_ID_SHAPE = re.compile(r"[0-9a-f]{32}")  # uuid4().hex
_MAX_ISSUE = 999_999_999  # the same bound as predicates.MAX_ISSUE_NUMBER
_ENTRY_STATES = frozenset(
    {"pending", "woken", "acked", "unknown", "failed", "abandoned"}
)
# The same patterns as ``predicates.REPO_PATTERN``, ``launch.WAKE_ID_PATTERN`` and
# ``route.ORCHESTRATOR_ID_PATTERN`` (this module imports nothing from the
# package; a test pins the copies equal).
_REPO_SHAPE = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9._-]{1,100}")
_WAKE_ID_SHAPE = re.compile(r"[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}")
_ORCHESTRATOR_SHAPE = re.compile(r"[a-z0-9]{1,12}-[1-9][0-9]{0,5}")
_STAGES_SHAPE = re.compile(
    r"(input_accepted|turn_started)(,(input_accepted|turn_started)){0,1}"
)


def _is_utc_ts(value: str) -> bool:
    if _UTC_TS_SHAPE.fullmatch(value) is None:
        return False
    try:
        datetime.datetime.strptime(value, _UTC_TS_FORMAT)
    except ValueError:
        return False
    return True


def _is_token(value: str, longest: int) -> bool:
    """A printable string of 1..``longest`` characters."""
    return 0 < len(value) <= longest and value.isprintable()


# Key -> value rule, applied after the type check to a non-null value. The host
# and login rules only bound length and printability (login also bars
# whitespace), so they accept any such token; they do not filter free text. The
# login rule is deliberately looser than the cycle's login regex (design line
# 348), so a rejected login can still be written. Every other key is closed.
_RULES: dict[str, Callable[[Any], bool]] = {
    "ts": _is_utc_ts,
    "repo": lambda v: _REPO_SHAPE.fullmatch(v) is not None,
    "orchestrator": lambda v: _ORCHESTRATOR_SHAPE.fullmatch(v) is not None,
    "wake_id": lambda v: _WAKE_ID_SHAPE.fullmatch(v) is not None,
    "stages": lambda v: _STAGES_SHAPE.fullmatch(v) is not None,
    "cycle_id": lambda v: _CYCLE_ID_SHAPE.fullmatch(v) is not None,
    "state": lambda v: v in _ENTRY_STATES,
    "host": lambda v: _is_token(v, 255),
    "login": lambda v: _is_token(v, 100) and not any(c.isspace() for c in v),
    "issue": lambda v: 1 <= v <= _MAX_ISSUE,
    "exit": lambda v: 0 <= v <= 255,
    "gh_calls": lambda v: v >= 0,
    "duration_ms": lambda v: v >= 0,
    "discovery_count": lambda v: v >= 0,
}


def _check_value(key: str, value: object) -> None:
    expected, nullable = _TYPES[key]
    if value is None:
        if nullable:
            return
        raise ValueError(f"audit key {key!r} must not be null")
    if expected is int and isinstance(value, bool):
        raise ValueError(f"audit key {key!r} must be int, not bool")
    if not isinstance(value, expected):
        raise ValueError(f"audit key {key!r} must be {expected.__name__}")
    rule = _RULES.get(key)
    if rule is not None and not rule(value):
        raise ValueError(f"audit key {key!r} has a value outside its allowed shape")


def line(kind: str, **fields: object) -> dict:
    """Build one audit line, checking the reason and the key set of ``kind``.

    The call site chooses the line kind; the reason is checked for membership
    in ``REASONS`` only.
    """
    if kind not in _KEYS:
        raise ValueError(f"unknown audit line kind {kind!r}")
    required, optional = _KEYS[kind]
    out: dict = {"kind": kind, **fields}
    extra = set(out) - required - optional
    if extra:
        raise ValueError(f"keys not allowed on a {kind} line: {sorted(extra)}")
    missing = required - set(out)
    if missing:
        raise ValueError(f"keys missing from a {kind} line: {sorted(missing)}")
    for key, value in out.items():
        _check_value(key, value)
    reason = out["reason"]
    if reason not in REASONS:
        raise ValueError(f"unknown audit reason {reason!r}")
    # A note is the value of a ``note`` key; only a decision line may also use
    # one as its reason (the hold notes of design 4.11 have no skip reason).
    if REASON_TABLE[reason][0] == "note" and kind != "decision":
        raise ValueError(f"unknown audit reason {reason!r}")
    note = out.get("note")
    if note is not None and REASON_TABLE.get(note, ("",))[0] != "note":
        raise ValueError(f"unknown audit note {note!r}")
    return out


def _optional(**fields: object) -> dict:
    return {key: value for key, value in fields.items() if value is not None}


def cycle_line(
    *,
    ts: str,
    host: str,
    login: str | None,
    cycle_id: str,
    dry_run: bool,
    exit_code: int,
    reason: str,
    gh_calls: int,
    duration_ms: int,
    discovery_count: int | None = None,
    clock_skew_s: int | None = None,
) -> dict:
    """Build a ``cycle`` line; ``exit_code`` is written under the ``exit`` key."""
    return line(
        "cycle",
        ts=ts,
        host=host,
        login=login,
        cycle_id=cycle_id,
        dry_run=dry_run,
        exit=exit_code,
        reason=reason,
        gh_calls=gh_calls,
        duration_ms=duration_ms,
        **_optional(discovery_count=discovery_count, clock_skew_s=clock_skew_s),
    )


def decision_line(
    *,
    ts: str,
    host: str,
    login: str | None,
    cycle_id: str,
    dry_run: bool,
    reason: str,
    repo: str,
    issue: int,
    state: str | None = None,
    note: str | None = None,
    orchestrator: str | None = None,
    wake_id: str | None = None,
    stages: str | None = None,
) -> dict:
    """Build a ``decision`` line; ``state`` only when an entry was written."""
    return line(
        "decision",
        ts=ts,
        host=host,
        login=login,
        cycle_id=cycle_id,
        dry_run=dry_run,
        reason=reason,
        repo=repo,
        issue=issue,
        **_optional(
            state=state,
            note=note,
            orchestrator=orchestrator,
            wake_id=wake_id,
            stages=stages,
        ),
    )


def warning_line(
    *,
    ts: str,
    host: str,
    login: str | None,
    cycle_id: str,
    dry_run: bool,
    reason: str,
    repo: str | None = None,
    issue: int | None = None,
    discovery_count: int | None = None,
    clock_skew_s: int | None = None,
) -> dict:
    """Build a ``warning`` line."""
    return line(
        "warning",
        ts=ts,
        host=host,
        login=login,
        cycle_id=cycle_id,
        dry_run=dry_run,
        reason=reason,
        **_optional(
            repo=repo,
            issue=issue,
            discovery_count=discovery_count,
            clock_skew_s=clock_skew_s,
        ),
    )


def stderr_fallback(
    reason: str,
    exit_code: int,
    *,
    ts: str | None = None,
    host: str | None = None,
) -> None:
    """Write one JSON line to stderr with ``kind ts host exit reason`` only.

    Used when ``audit.jsonl`` cannot be written. ``ts`` and ``host`` default to
    the current UTC time and ``socket.gethostname()`` (a stamp, not a decision).
    """
    if reason not in REASONS:
        raise ValueError(f"unknown audit reason {reason!r}")
    if ts is None:
        now = datetime.datetime.now(datetime.timezone.utc)
        ts = now.strftime(_UTC_TS_FORMAT)
    if host is None:
        host = socket.gethostname()
    for key, value in (("exit", exit_code), ("ts", ts), ("host", host)):
        _check_value(key, value)
    out = {"kind": "cycle", "ts": ts, "host": host, "exit": exit_code, "reason": reason}
    sys.stderr.write(_encode(out).decode("ascii"))
    sys.stderr.flush()
