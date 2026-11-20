"""List the Orca repositories the watcher may serve (plan Task 18, requirement R15).

``orca repo list`` prints one line per repository: ``<id>  <name>  <path>`` (fields joined by
two or more spaces; checked on 2026-11-18). For each line this module reads the path's git
``origin`` and keeps the repository only when it is usable. A repository that is not usable is
skipped with a closed reason, never silently:

* ``path_in_tmp``: the path is ``/tmp`` or under it (a throwaway checkout);
* ``origin_unreadable``: ``git remote get-url origin`` failed, timed out or printed nothing;
* ``origin_not_github``: the origin is not a ``github.com`` ``owner/name`` URL;
* ``foreign_owner``: the origin owner is not one of ``allowed_owners`` (case-insensitive).

A failed or timed-out ``orca repo list``, or output that cannot be read, raises
``RepoListError``: it never gives an empty list, because an empty list would look like "nothing
to watch". An empty but successful list returns no repositories.

Every command runs through the ``Runner`` (an argv list, no shell).
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import PurePosixPath

from .launch import parse_origin
from .runner import CommandResult, Runner

LIST_TIMEOUT_S = 30.0
GIT_TIMEOUT_S = 15.0

_FIELDS = re.compile(r" {2,}")
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}")


class RepoListError(Exception):
    """``orca repo list`` could not be run or read. ``reason`` is a closed word."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


@dataclass(frozen=True)
class OrcaRepo:
    """One usable repository."""

    orca_id: str
    name: str
    path: str
    slug: str
    """``owner/name`` read from the path's git ``origin``."""


@dataclass(frozen=True)
class Skipped:
    """One repository the watcher will not serve, and why."""

    orca_id: str
    name: str
    path: str
    reason: str


@dataclass(frozen=True)
class RepoList:
    repos: tuple[OrcaRepo, ...]
    skipped: tuple[Skipped, ...]


def _in_tmp(path: str) -> bool:
    parts = PurePosixPath(path).parts
    return len(parts) >= 2 and parts[0] == "/" and parts[1] == "tmp"


def _parse_lines(text: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        fields = _FIELDS.split(line, maxsplit=2)
        if len(fields) != 3:
            raise RepoListError("unreadable_list")
        orca_id, name, path = (f.strip() for f in fields)
        if not _ID.fullmatch(orca_id) or not name or not path.startswith("/"):
            raise RepoListError("unreadable_list")
        rows.append((orca_id, name, path))
    return rows


def _failed(result: CommandResult) -> bool:
    return result.timed_out or result.spawn_error is not None or result.returncode != 0


def _origin(runner: Runner, path: str, timeout: float) -> str | None:
    """The ``owner/name`` of the path's origin; ``""`` for a non-GitHub URL; None when unread."""
    argv = ["git", "-C", path, "remote", "get-url", "origin"]
    result = runner.run(argv, timeout)
    if _failed(result) or not result.stdout.strip():
        return None
    return parse_origin(result.stdout) or ""


def list_repos(
    runner: Runner,
    orca: str,
    allowed_owners: Iterable[str],
    *,
    list_timeout: float = LIST_TIMEOUT_S,
    git_timeout: float = GIT_TIMEOUT_S,
) -> RepoList:
    """Run ``orca repo list`` and return the usable repositories and the skipped ones.

    ``orca`` is the Orca CLI path or name the caller already proved (``launch.find_orca``).
    Raises ``RepoListError`` (``list_failed``, ``list_timeout`` or ``unreadable_list``).
    """
    owners = {o.lower() for o in allowed_owners}
    result = runner.run([orca, "repo", "list"], list_timeout)
    if result.timed_out:
        raise RepoListError("list_timeout")
    if result.spawn_error is not None or result.returncode != 0:
        raise RepoListError("list_failed")
    repos: list[OrcaRepo] = []
    skipped: list[Skipped] = []
    for orca_id, name, path in _parse_lines(result.stdout):

        def skip(reason: str) -> None:
            skipped.append(Skipped(orca_id, name, path, reason))

        if _in_tmp(path):
            skip("path_in_tmp")
            continue
        slug = _origin(runner, path, git_timeout)
        if slug is None:
            skip("origin_unreadable")
        elif not slug:
            skip("origin_not_github")
        elif slug.split("/")[0].lower() not in owners:
            skip("foreign_owner")
        else:
            repos.append(OrcaRepo(orca_id, name, path, slug))
    return RepoList(tuple(repos), tuple(skipped))
