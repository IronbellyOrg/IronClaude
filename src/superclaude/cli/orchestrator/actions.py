"""The action log: ``<orchestrator repo>/.orchestrator/actions.jsonl`` (design 5.6, "Every answer is checked").

One JSON object per line, appended and never rewritten, mode 0600. A row holds the id
(``a-<UTC time>-<8 hex>``), the time, the ``kind`` and the fields of that kind. The id of
an ``answer-check`` row is what ``--answer-ref`` carries: ``find`` returns the row, so a
verb that is told "Clay said yes" checks the row and not the word of the caller. A row
never holds the text of an answer (it may hold a secret that a person typed).

Kinds written so far: ``answer-check`` (every run, accepted or refused, with the results)
and ``repos-write`` (a change of ``grants``, ``reach_daily_max`` or ``merge_safety_files``,
with the ref that allowed it). Appends hold ``state.lock``, the lock of ``asks.json``.
"""

from __future__ import annotations

import json
import os
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Final

from superclaude.cli.issue_watch.predicates import format_utc
from superclaude.cli.issue_watch.route import STATE_DIR

from . import state

ACTIONS_FILE: Final = "actions.jsonl"
_REF: Final = re.compile(r"a-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}")


def actions_path(root: Path | str) -> Path:
    """``<root>/.orchestrator/actions.jsonl``."""
    return Path(root) / STATE_DIR / ACTIONS_FILE


def new_ref(now: datetime) -> str:
    """A fresh action id."""
    return f"a-{now.strftime('%Y%m%dT%H%M%SZ')}-{secrets.token_hex(4)}"


def append(
    root: Path | str, kind: str, *, now: datetime | None = None, **fields: Any
) -> str:
    """Append one row and return its id (the row is on disk when this returns)."""
    stamp = now if now is not None else datetime.now(timezone.utc)
    ref = new_ref(stamp)
    row = {"id": ref, "ts": format_utc(stamp), "kind": kind, **fields}
    line = (json.dumps(row, sort_keys=True) + "\n").encode("ascii")
    path = actions_path(root)
    with state.locked(root):
        os.makedirs(path.parent, mode=0o700, exist_ok=True)
        fd = os.open(
            path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW, 0o600
        )
        try:
            os.write(fd, line)
            os.fsync(fd)
        finally:
            os.close(fd)
    return ref


def used_for(root: Path | str, ref: str, kind: str) -> bool:
    """True when a row of ``kind`` already names ``ref`` (an OK is used for one write only)."""
    try:
        with open(actions_path(root), "rb") as handle:
            for raw in handle:
                try:
                    row = json.loads(raw.decode("utf-8"))
                except (ValueError, RecursionError):
                    continue
                if (
                    isinstance(row, dict)
                    and row.get("kind") == kind
                    and row.get("ref") == ref
                ):
                    return True
    except OSError:
        return False
    return False


def find(root: Path | str, ref: object) -> dict[str, Any] | None:
    """The row with id ``ref``, or None (a line that cannot be read is skipped)."""
    if not isinstance(ref, str) or _REF.fullmatch(ref) is None:
        return None
    try:
        with open(actions_path(root), "rb") as handle:
            for raw in handle:
                try:
                    row = json.loads(raw.decode("utf-8"))
                except (ValueError, RecursionError):
                    continue
                if isinstance(row, dict) and row.get("id") == ref:
                    return row
    except OSError:
        return None
    return None
