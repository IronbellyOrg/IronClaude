"""Read and write ``<orchestrator repo>/repos.yaml`` for the verbs (design 4.4, 5.6).

Reading is ``issue_watch.repos`` (PR A), the poll's own validator, so a file that these
verbs accept is a file the poll accepts. Writing goes through ``edit`` and nowhere else:

* the file as it stands must be valid, and the new text is validated before anything is
  written (a file the poll would refuse as ``repos_invalid`` is never written);
* the read, the change and the write happen under ``.orchestrator/state.lock``, and the
  file is replaced whole (temporary file and ``rename``), so the poll never reads half of it;
* the three keys that are Clay's alone, ``grants``, ``reach_daily_max`` and
  ``merge_safety_files`` (5.6), are guarded here: a change that touches one of them is
  refused (exit 2, nothing written) unless the caller holds an accepted ``answer-check`` row,
  and the write is logged with that row's id. It does not matter which verb asks, so
  ``add`` and ``refresh`` cannot change them by accident either.

The file is read and written with PyYAML ``safe_load`` and ``safe_dump``: a comment in the
file is not kept, and keys keep their order. The orchestrator owns the file and edits it
only through these verbs, so there is no hand-written comment to lose.
"""

from __future__ import annotations

import copy
import os
import stat
from collections.abc import Callable
from pathlib import Path
from typing import Any, Final

import yaml

from superclaude.cli.issue_watch import repos
from superclaude.cli.issue_watch.runner import Runner
from superclaude.cli.swarm.atomic import write_prepared_bytes

from . import actions, state
from .ext import CALL_TIMEOUT_S
from .state import EXIT_INVALID, StateError

GUARDED_KEYS: Final = ("grants", "reach_daily_max", "merge_safety_files")
_MAX_BYTES: Final = 1024 * 1024
_ABSENT: Final = object()


def repos_path(root: Path | str) -> Path:
    """``<root>/repos.yaml``."""
    return Path(root) / repos.REPOS_FILE


def _invalid(exc: repos.ReposError) -> StateError:
    return StateError("repos_invalid", EXIT_INVALID, detail=exc.detail)


def read_text(root: Path | str) -> str:
    """The text of ``repos.yaml`` (``repos_invalid`` when it is missing or too large)."""
    try:
        with open(repos_path(root), "rb") as handle:
            data = handle.read(_MAX_BYTES + 1)
        if len(data) > _MAX_BYTES:
            raise ValueError
        return data.decode("utf-8")
    except (OSError, ValueError):
        raise StateError(
            "repos_invalid",
            EXIT_INVALID,
            detail="repos.yaml is missing or cannot be read",
        ) from None


def load_doc(root: Path | str, runner: Runner) -> repos.ReposDoc:
    """The validated file (``repos.load_repos``; the tier list comes from ``ccsession --help``)."""
    try:
        return repos.load_repos(Path(root), runner, CALL_TIMEOUT_S)
    except repos.ReposError as exc:
        raise _invalid(exc) from None


def require_grant(doc: repos.ReposDoc, repo: str, grant: str) -> repos.RepoEntry:
    """The listed entry of ``repo``, or the refusal of a write that has no right to happen (exit 2).

    ``repo_not_listed`` and ``repo_disabled`` are ``E-REPO-UNLISTED`` of 5.2; ``no_grant`` is
    ``E-NO-GRANT``: a GitHub write that a verb makes is allowed only on a listed, enabled
    repo and only when ``grants`` lists the action (DQ6).
    """
    entry = doc.get(repo)
    if entry is None:
        raise StateError("repo_not_listed", EXIT_INVALID)
    if not entry.enabled:
        raise StateError("repo_disabled", EXIT_INVALID)
    if not doc.has_grant(grant):
        raise StateError("no_grant", EXIT_INVALID, grant=grant)
    return entry


def guarded_changes(old: dict[str, Any], new: dict[str, Any]) -> list[str]:
    """The guarded keys that differ between two parsed files (a new repo that carries one counts)."""
    changed: set[str] = set()
    if old.get("grants", _ABSENT) != new.get("grants", _ABSENT):
        changed.add("grants")
    before = {
        str(r["repo"]).lower(): r
        for r in old.get("repos") or []
        if isinstance(r, dict) and "repo" in r
    }
    for entry in new.get("repos") or []:
        if not isinstance(entry, dict):
            continue
        prior = before.get(str(entry.get("repo")).lower(), {})
        for key in GUARDED_KEYS[1:]:
            if prior.get(key, _ABSENT) != entry.get(key, _ABSENT):
                changed.add(key)
    return sorted(changed)


def edit(
    root: Path | str,
    runner: Runner,
    change: Callable[[dict[str, Any]], dict[str, Any] | None],
    answer_row: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Change the parsed file with ``change`` and write it; the one way ``repos.yaml`` is written.

    ``change`` edits the parsed mapping in place and may return values for the result.
    ``answer_row`` is the accepted ``answer-check`` row (``answer_check.require_accepted``),
    needed only when the change touches a guarded key. Result: ``{"guarded": [keys
    changed], ...}``.
    """
    listed = repos.listed_tiers(runner, CALL_TIMEOUT_S)
    path = repos_path(root)
    with state.locked(root):
        text = read_text(root)
        try:
            repos.parse_repos(text, listed)
        except repos.ReposError as exc:
            raise _invalid(exc) from None
        old = yaml.safe_load(text)
        new = copy.deepcopy(old)
        extra = change(new) or {}
        guarded = guarded_changes(old, new)
        if guarded and answer_row is None:
            raise StateError("answer_ref_required", EXIT_INVALID, keys=guarded)
        if guarded and actions.used_for(root, answer_row["id"], "repos-write"):
            # one OK, one write: Clay's word for one change never opens a second
            raise StateError("answer_ref_used", EXIT_INVALID, keys=guarded)
        out = yaml.safe_dump(new, sort_keys=False, default_flow_style=False)
        try:
            repos.parse_repos(out, listed)
        except repos.ReposError as exc:
            raise _invalid(exc) from None
        mode = stat.S_IMODE(os.stat(path).st_mode)
        write_prepared_bytes(path, out.encode("utf-8"))
        os.chmod(path, mode)
        if guarded and answer_row is not None:
            actions.append(root, "repos-write", keys=guarded, ref=answer_row["id"])
    return {"guarded": guarded, **extra}
