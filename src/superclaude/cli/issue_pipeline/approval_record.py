"""The locked, write-ahead approval record helper (plan Task 3).

Two kinds of row live in an approvals directory of their own, never inside the
watcher's state directory and never touching ``dispatch.json``:

* An **adoption row** is keyed (issue, stage). It is created before any plan
  exists, so it needs no plan hash. It is the per-issue reservation that stops a
  second start: state ``reserved``, then ``started`` (with the Dispatch id) or
  ``uncertain`` when ``worker-start`` did not report ready. An ``uncertain`` row is
  settled by a person or by reading ``worker-list``, never by starting again.
* An **approval row** is keyed (issue, stage, plan hash) and hangs under the
  adoption row. States: ``recorded``, ``instructed``, ``acked``, ``revoked``.

Every mutation holds ``FileStore(<dir>).lock()``: an exclusive non-blocking
``flock`` on ``<dir>/lock``, so a second concurrent caller gets ``lock-held`` at
once and the verbs say "retry", never "lost". ``record.py`` of the watcher is not
edited; only its ``FileStore.lock`` is used. Rows are written with
``write_prepared_bytes`` followed by a directory sync, as ``FileStore.save`` does.
Nothing here keeps or prints GitHub text: every stored value matches a fixed pattern.
"""

from __future__ import annotations

import json
import os
import re
import stat
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from superclaude.cli.issue_watch.record import FileStore, LockError, LockHeld
from superclaude.cli.swarm.atomic import write_prepared_bytes

from .approval_line import record_id

LOCK_FILE = "lock"

_STAGE = re.compile(r"[a-z][a-z0-9-]{0,31}")
_HASH = re.compile(r"[0-9a-f]{64}")
_ID = re.compile(r"[0-9A-Za-z_:.=-]{1,80}")
_TIME = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
CHANNELS = ("label", "comment", "reply")
ADOPTION_STATES = ("reserved", "started", "uncertain")
APPROVAL_STATES = ("recorded", "instructed", "acked", "revoked")
_FORWARD = {"recorded": "instructed", "instructed": "acked"}


class ApprovalError(Exception):
    """A closed refusal; ``reason`` never holds file or GitHub text."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _need(pattern: re.Pattern[str], value: str, reason: str) -> str:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        raise ApprovalError(reason)
    return value


def _issue(issue: int) -> int:
    if isinstance(issue, bool) or not isinstance(issue, int) or issue < 1:
        raise ApprovalError("bad-issue")
    return issue


def _fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def init_dir(directory: str | Path) -> None:
    """Create the approvals directory (0700) and its ``lock`` file (0600).

    ``FileStore.lock()`` opens an existing file with no create flag and raises
    ``lock_missing`` otherwise, so ``init`` is the only creator. Safe to repeat.
    """
    path = Path(directory)
    if path.is_symlink() or (path.exists() and not path.is_dir()):
        raise ApprovalError("bad-dir")
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    lock = path / LOCK_FILE
    if lock.is_symlink():
        raise ApprovalError("bad-dir")
    fd = os.open(lock, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    os.close(fd)
    os.chmod(path, 0o700)
    os.chmod(lock, 0o600)
    _fsync_dir(path)


def _locked(directory: Path):
    """The lock context, with the closed refusals mapped."""
    if directory.is_symlink() or not directory.is_dir():
        raise ApprovalError("not-initialized")
    return FileStore(directory).lock()


class _Guard:
    def __init__(self, directory: Path) -> None:
        self._cm = _locked(directory)

    def __enter__(self) -> None:
        try:
            self._cm.__enter__()
        except LockHeld:
            raise ApprovalError("lock-held") from None
        except LockError as exc:
            raise ApprovalError(
                "not-initialized" if exc.reason == "lock_missing" else "lock-invalid"
            ) from None

    def __exit__(self, *exc_info: Any) -> bool | None:
        return self._cm.__exit__(*exc_info)


def _adoption_path(directory: Path, issue: int, stage: str) -> Path:
    return (
        directory / f"adoption-{_issue(issue)}-{_need(_STAGE, stage, 'bad-stage')}.json"
    )


def _approval_path(directory: Path, issue: int, stage: str, plan_hash: str) -> Path:
    name = f"approval-{_issue(issue)}-{_need(_STAGE, stage, 'bad-stage')}-{_need(_HASH, plan_hash, 'bad-hash')}.json"
    return directory / name


def _read_row(path: Path) -> dict[str, Any] | None:
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(st.st_mode):
        raise ApprovalError("row-invalid")
    try:
        row = json.loads(path.read_bytes())
    except (OSError, ValueError):
        raise ApprovalError("row-invalid") from None
    if not isinstance(row, dict) or row.get("state") not in (
        *ADOPTION_STATES,
        *APPROVAL_STATES,
    ):
        raise ApprovalError("row-invalid")
    return row


def _write_row(path: Path, row: dict[str, Any]) -> None:
    text = json.dumps(row, sort_keys=True, indent=2, ensure_ascii=True)
    write_prepared_bytes(path, text.encode() + b"\n")
    os.chmod(path, 0o600)
    _fsync_dir(path.parent)


# --- adoption rows ------------------------------------------------------------


def adopt_create(
    directory: str | Path, issue: int, stage: str, now: str | None = None
) -> dict[str, Any]:
    """Reserve (issue, stage). Only the caller that gets ``created`` may start a worker.

    An existing ``reserved`` or ``uncertain`` row refuses with ``uncertain-launch``
    (a start may or may not have happened; never start again), a ``started`` row
    with ``already-started``.
    """
    d = Path(directory)
    path = _adoption_path(d, issue, stage)
    with _Guard(d):
        existing = _read_row(path)
        if existing is not None:
            raise ApprovalError(
                "already-started"
                if existing["state"] == "started"
                else "uncertain-launch"
            )
        stamp = _need(_TIME, now or _now(), "bad-time")
        row = {
            "kind": "adoption",
            "issue": issue,
            "stage": stage,
            "state": "reserved",
            "dispatch_id": None,
            "created_at": stamp,
            "updated_at": stamp,
        }
        _write_row(path, row)
        return {"result": "created", "row": row}


def adopt_mark(
    directory: str | Path,
    issue: int,
    stage: str,
    state: str,
    dispatch_id: str | None = None,
    now: str | None = None,
) -> dict[str, Any]:
    """``reserved`` to ``started`` (needs a Dispatch id) or ``uncertain``; ``uncertain`` to ``started``."""
    d = Path(directory)
    path = _adoption_path(d, issue, stage)
    if state not in ("started", "uncertain"):
        raise ApprovalError("bad-move")
    if state == "started":
        _need(_ID, dispatch_id or "", "bad-dispatch-id")
    with _Guard(d):
        row = _read_row(path)
        if row is None or row.get("kind") != "adoption":
            raise ApprovalError("no-row")
        if (row["state"], state) not in (
            ("reserved", "started"),
            ("reserved", "uncertain"),
            ("uncertain", "started"),
        ):
            raise ApprovalError("bad-move")
        row["state"] = state
        if state == "started":
            row["dispatch_id"] = dispatch_id
        row["updated_at"] = _need(_TIME, now or _now(), "bad-time")
        _write_row(path, row)
        return {"result": "marked", "row": row}


def adopt_show(directory: str | Path, issue: int, stage: str) -> dict[str, Any]:
    row = _read_row(_adoption_path(Path(directory), issue, stage))
    if row is None:
        raise ApprovalError("no-row")
    return row


# --- approval rows ------------------------------------------------------------


def record_create(
    directory: str | Path,
    issue: int,
    stage: str,
    plan_hash: str,
    channel: str,
    evidence_id: str,
    actor: str,
    now: str | None = None,
) -> dict[str, Any]:
    """Create the row for (issue, stage, plan hash), or append evidence to the existing one.

    A second approval for the same key, from any channel, appends evidence and
    returns the existing row, so a label plus a comment never produce two rows.
    A re-approval of the same plan after ``revoked`` reopens the same row.
    """
    d = Path(directory)
    path = _approval_path(d, issue, stage, plan_hash)
    if channel not in CHANNELS:
        raise ApprovalError("bad-channel")
    _need(_ID, evidence_id, "bad-evidence-id")
    _need(_ID, actor, "bad-actor")
    stamp = _need(_TIME, now or _now(), "bad-time")
    with _Guard(d):
        if _read_row(_adoption_path(d, issue, stage)) is None:
            raise ApprovalError("no-adoption")
        evidence = {
            "channel": channel,
            "id": evidence_id,
            "actor": actor,
            "time": stamp,
        }
        row = _read_row(path)
        if row is None:
            row = {
                "kind": "approval",
                "record_id": record_id(issue, plan_hash),
                "issue": issue,
                "stage": stage,
                "plan_hash": plan_hash,
                "state": "recorded",
                "evidence": [evidence],
                "created_at": stamp,
                "updated_at": stamp,
            }
            _write_row(path, row)
            return {"result": "created", "row": row}
        if evidence not in row["evidence"]:
            row["evidence"].append(evidence)
        if row["state"] == "revoked":
            row["state"] = "recorded"
        row["updated_at"] = stamp
        _write_row(path, row)
        return {"result": "exists", "row": row}


def record_show(
    directory: str | Path, issue: int, stage: str, plan_hash: str
) -> dict[str, Any]:
    row = _read_row(_approval_path(Path(directory), issue, stage, plan_hash))
    if row is None:
        raise ApprovalError("no-row")
    return row


def record_mark(
    directory: str | Path,
    issue: int,
    stage: str,
    plan_hash: str,
    state: str,
    now: str | None = None,
) -> dict[str, Any]:
    """Only ``recorded`` to ``instructed`` to ``acked``, and ``revoked`` from any of them."""
    d = Path(directory)
    path = _approval_path(d, issue, stage, plan_hash)
    if state not in APPROVAL_STATES[1:]:
        raise ApprovalError("bad-move")
    stamp = _need(_TIME, now or _now(), "bad-time")
    with _Guard(d):
        row = _read_row(path)
        if row is None or row.get("kind") != "approval":
            raise ApprovalError("no-row")
        current = row["state"]
        allowed = (state == "revoked" and current != "revoked") or _FORWARD.get(
            current
        ) == state
        if not allowed:
            raise ApprovalError("bad-move")
        row["state"] = state
        row["updated_at"] = stamp
        _write_row(path, row)
        return {"result": "marked", "row": row}
