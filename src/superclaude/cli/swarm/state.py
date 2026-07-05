r"""T03.03 -- COMP-011 ``.swarm-state.json`` atomic state transitions.

This module owns the persistence surface for :class:`SwarmState`
(DM-014). It exposes exactly two functions:

* :func:`write_state` -- serialize a :class:`SwarmState` to ``path``
  via the tmp-file + :func:`os.replace` idiom so transitions are
  observed atomically by any concurrent reader (the resume path in
  M6 / FR-015).
* :func:`read_state` -- load ``path`` back into a :class:`SwarmState`
  instance, returning ``None`` when the file does not exist and
  raising on corrupt JSON.

NFR-002 atomicity contract
==========================

Every write goes ``path.with_suffix(path.suffix + ".tmp")`` first,
then :func:`os.replace` swaps it in. The live path is **never** opened
directly for writing -- a mid-write kill therefore leaves either the
prior file in place or no file at all, never a partial one. The
matching enforcement test lives in
``tests/swarm/test_imm6_atomic_write.py`` (T03.13); the per-module
acceptance grep is::

    grep -nE 'open\(.*".*state.*\.json.*w' src/superclaude/cli/swarm/state.py

and must return zero hits.

``updated`` stamping
====================

:class:`SwarmState.updated` carries an ISO 8601 UTC timestamp of the
last transition. The dataclass default is the empty string; the state
module stamps it on every write so callers do not have to remember to
update it (and so the wall-clock ordering of state transitions is
recoverable from the file alone). The stamp uses the ``Z`` suffix
(UTC, no offset) to keep the format stable across machines.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union

from superclaude.cli.swarm.models import SwarmState, from_dict, to_dict

__all__ = ["OutputConfinementError", "confine_path", "read_state", "write_state"]


class OutputConfinementError(ValueError):
    """NFR-013 / AC-014 -- write attempted outside the ``--output`` root.

    Raised by :func:`confine_path` when the resolved target path would
    land outside the resolved ``--output`` directory. Subclasses
    :class:`ValueError` so callers that catch broad input-validation
    failures still see it, while the distinct type lets the per-writer
    audit grep (`grep -RnE "confine_path\\(" src/superclaude/cli/swarm/`)
    and the NFR-013 test suite assert the explicit-exception contract.
    """


def confine_path(
    path: Union[str, os.PathLike[str]],
    output_dir: Union[str, os.PathLike[str]],
) -> Path:
    """NFR-013 / AC-014 -- confine ``path`` to ``output_dir``.

    Resolves both ``path`` and ``output_dir`` and verifies the resolved
    target is the output directory itself or a descendant of it. The
    resolution step collapses ``..`` segments, absolutises any relative
    component, and follows symlinks -- so a relative ``../etc/passwd``,
    an absolute ``/etc/passwd``, and a symlink pointing outside the
    root all collapse to the same check and are rejected with
    :class:`OutputConfinementError`.

    Resolution semantics:
        * Both arguments are pushed through :meth:`Path.resolve` with
          ``strict=False`` so the call works for paths that do not yet
          exist (the common case -- writers call ``confine_path`` to
          validate the *target* before opening the file).
        * Symlinks are followed -- a symlink whose target escapes the
          root is rejected, matching the NFR-013 "symlink escape" test
          branch.
        * ``output_dir`` itself is allowed (``out / "" == out`` is
          treated as a valid descendant) so callers can confine the
          root directory before stamping per-job sub-paths inside it.

    Args:
        path: the write target. May be relative (resolved against the
            current working directory) or absolute. Need not exist.
        output_dir: the job's ``--output`` root. Resolved with the same
            rules; need not exist (the run command creates it during
            Wave 0 preflight, but ``confine_path`` is also called from
            paths that run before ``mkdir`` -- e.g. the manifest writer
            asserts confinement before creating the directory).

    Returns:
        The resolved absolute :class:`Path` of ``path``. Callers should
        use this value for the actual write so the on-disk path is the
        same one that passed the check (closing the TOCTOU window for
        the simple cases -- a follow-up symlink-swap between the check
        and the write is still possible but out of scope; the M5
        threat model treats the writer's filesystem as trusted).

    Raises:
        OutputConfinementError: ``path`` resolves outside ``output_dir``
            (absolute escape, ``..`` traversal, or symlink target
            outside the root). The message names both resolved paths
            so operator triage does not need to re-resolve.
    """
    resolved_target = Path(path).resolve(strict=False)
    resolved_root = Path(output_dir).resolve(strict=False)

    # ``Path.is_relative_to`` (3.9+) returns True for the root itself
    # and any descendant; that matches the "root or below" contract.
    if not resolved_target.is_relative_to(resolved_root):
        raise OutputConfinementError(
            f"path {resolved_target!s} escapes output_dir {resolved_root!s} "
            "(NFR-013 / AC-014 output confinement violation)"
        )
    return resolved_target


def _utc_now_iso() -> str:
    """ISO 8601 UTC timestamp with ``Z`` suffix (no microseconds).

    Format: ``YYYY-MM-DDTHH:MM:SSZ``. Matches the timestamp shape used
    by the manifest (DM-016) so artifacts cross-reference cleanly.
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_state(
    path: Union[str, os.PathLike[str]],
    state: SwarmState,
    *,
    output_dir: Optional[Union[str, os.PathLike[str]]] = None,
) -> None:
    """Persist ``state`` to ``path`` atomically.

    The write is performed via a sibling ``.tmp`` file followed by
    :func:`os.replace`, so a concurrent reader sees either the prior
    file or the new file, never a half-written one. The parent
    directory is created if it does not exist (mirrors the executor's
    expectation that the output directory is materialized before the
    first state transition).

    ``state.updated`` is rewritten with a fresh ISO 8601 UTC stamp
    immediately before serialization; callers do not need to manage
    the timestamp themselves.

    NFR-013 / AC-014 confinement: when ``output_dir`` is supplied,
    :func:`confine_path` is invoked before any directory or file is
    created -- a target outside the root raises
    :class:`OutputConfinementError` and no side effects are observable.
    ``output_dir`` defaults to ``None`` for backwards compatibility
    with the T03.03 acceptance shape (mid-write-kill test does not
    care about confinement); production callers (the run command, the
    preflight orchestrator) always supply the job's ``--output``.
    """
    if output_dir is not None:
        path = confine_path(path, output_dir)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    state.updated = _utc_now_iso()
    payload = json.dumps(to_dict(state), sort_keys=True, indent=2) + "\n"

    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_text(payload, encoding="utf-8")
    os.replace(tmp, target)


def read_state(path: Union[str, os.PathLike[str]]) -> Optional[SwarmState]:
    """Load ``path`` into a :class:`SwarmState`.

    Returns ``None`` when the file does not exist -- the resume path
    (FR-015) interprets that as "no prior run, start from preflight".
    Raises :class:`json.JSONDecodeError` on corrupt JSON and
    :class:`ValueError` when the payload is shape-valid JSON but does
    not satisfy :class:`SwarmState` invariants (e.g. an unknown
    ``state`` Literal value). The caller decides whether a corrupt
    state file is fatal or a resume short-circuit.
    """
    target = Path(path)
    try:
        raw = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None

    payload = json.loads(raw)
    return from_dict(SwarmState, payload)
