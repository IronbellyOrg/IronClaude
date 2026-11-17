"""Release a bound worker from the launch-level guard (G2, route A).

The coordinator calls this after it has recorded a plan approval. It creates the
worker session's ``.ok`` file, the file ``launch-level-guard.sh`` already reads
(a worktree-level session with an ``.ok`` file becomes ``worktree (approved)``),
so no release logic is added to the guard. The worker itself cannot do this: a
command that names the store is blocked for a bound session (LL-TAMPER).

Nothing here prints file text; every result is a closed word.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

_SESSION_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}")  # the guard's own rule
_WORKTREE_RECORDS = ("worktree", "worktree\n")


class ReleaseError(Exception):
    """A closed refusal; ``reason`` never holds file or user text."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


def default_store() -> Path:
    return Path.home() / ".claude" / "state" / "launch-level"


def _real_dir(path: Path) -> bool:
    return path.is_dir() and not path.is_symlink() and path.stat().st_uid == os.getuid()


def release(session_id: str, store: str | Path | None = None) -> str:
    """Create ``sessions/<session_id>.ok``; return ``released`` or ``already-released``.

    Refuses (``ReleaseError``) an id the guard would not accept, a store or
    session record that is missing, a link or not owned by this user, and a
    session that is not at the worktree level (only that level has a release).
    """
    if not isinstance(session_id, str) or not _SESSION_ID.fullmatch(session_id):
        raise ReleaseError("bad-session-id")
    sessions = Path(store if store is not None else default_store()) / "sessions"
    if not _real_dir(sessions):
        raise ReleaseError("no-store")
    record = sessions / session_id
    if not record.is_file() or record.is_symlink():
        raise ReleaseError("not-bound")
    if record.read_text(encoding="utf-8", errors="replace")[:13] not in (
        _WORKTREE_RECORDS
    ):
        raise ReleaseError("not-worktree-level")
    try:
        fd = os.open(
            sessions / f"{session_id}.ok",
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
        )
    except FileExistsError:
        return "already-released"
    os.close(fd)
    return "released"
