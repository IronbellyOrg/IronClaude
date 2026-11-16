"""The plan hash: one SHA-256 over a named list of plan files.

The coordinator puts this hash in the plan reply and the worker recomputes it.
Each file contributes its name, its length and its bytes, in the order of the
names sorted by their bytes, so moving bytes between two files changes the hash.
Nothing here ever returns or prints file text.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path, PurePosixPath


class PlanHashError(Exception):
    """A closed refusal. ``reason`` is one of ``REASONS``; it never holds file text."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


REASONS = (
    "no-names",
    "bad-dir",
    "absolute-name",
    "dotdot-name",
    "bad-name",
    "duplicate-name",
    "symlink",
    "missing",
    "outside-dir",
    "not-a-file",
    "unreadable",
)


def _checked_names(names: list[str]) -> list[str]:
    if not names:
        raise PlanHashError("no-names")
    seen: set[str] = set()
    for name in names:
        if not name or "\x00" in name or "\\" in name:
            raise PlanHashError("bad-name")
        if name.startswith("/"):
            raise PlanHashError("absolute-name")
        parts = PurePosixPath(name).parts
        if ".." in parts:
            raise PlanHashError("dotdot-name")
        if name in seen:
            raise PlanHashError("duplicate-name")
        seen.add(name)
    return sorted(names, key=lambda n: n.encode("utf-8"))


def _read_plan_file(root: Path, name: str) -> bytes:
    path = root / name
    # Every component below the report directory must be a real one, no links.
    current = root
    for part in PurePosixPath(name).parts:
        current = current / part
        if current.is_symlink():
            raise PlanHashError("symlink")
    if not os.path.lexists(path):
        raise PlanHashError("missing")
    if not path.resolve().is_relative_to(root.resolve()):
        raise PlanHashError("outside-dir")
    if not path.is_file():
        raise PlanHashError("not-a-file")
    try:
        return path.read_bytes()
    except OSError:
        raise PlanHashError("unreadable") from None


def compute(report_dir: str | Path, names: list[str]) -> tuple[list[str], str]:
    """Return the sorted file list and the 64-character lowercase hex hash."""
    root = Path(report_dir)
    if root.is_symlink() or not root.is_dir():
        raise PlanHashError("bad-dir")
    ordered = _checked_names(list(names))
    digest = hashlib.sha256()
    for name in ordered:
        data = _read_plan_file(root, name)
        raw = name.encode("utf-8")
        # Length prefixes make the framing unambiguous.
        digest.update(len(raw).to_bytes(8, "big") + raw)
        digest.update(len(data).to_bytes(8, "big") + data)
    return ordered, digest.hexdigest()
