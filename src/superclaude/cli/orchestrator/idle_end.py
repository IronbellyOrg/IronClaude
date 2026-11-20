"""The verb ``superclaude orchestrator idle-end``: end an idle orchestrator without a race (design 5.7 point 5; wave 9).

    idle-end [--orchestrator <id>] [--tag <tag>]

An orchestrator that has had nothing in flight and no unacknowledged wake for 30 minutes ends
itself. The end is one sequence that must hold ``.orchestrator/state.lock`` from the first line
to the last, because the poll routes new issues and writes new wake files under the same lock
(5.7 point 3): between "I looked, there is nothing" and "I am ended" no wake may arrive for
this orchestrator. A model cannot hold a ``flock`` across separate calls, so the sequence is
this one verb:

1. take ``state.lock`` (``lock_busy``, exit 75, when it stays held);
2. set ``runs/<id>.json`` to ``ending`` (the poll never routes to a Run that is not
   ``active``); an ``ending`` file left by an end that was killed half way is taken up again
   here, and an ``ended`` file answers ``already_ended`` and changes nothing;
3. read the wake directory and the state folder again, through ``issue_watch.wake``
   (``parse_wake``, ``read_ack``) and ``state.list_open``;
4. nothing pending: set ``ended`` (final; an id is never reused) and print it. Something
   pending: set ``active`` again, leave the Run ``active`` and exit 3 with ``pending_work`` and
   ``blockers``.

A blocker is one of:

* ``{"kind": "wake", "wake_id": ...}``: a wake file in ``wakes/`` that names this orchestrator
  (``target.orchestrator``) and has no readable acknowledgment. A wake that cannot be parsed
  does not say whom it is for and is listed under ``ignored``, not as a blocker: the poll
  sees no acknowledgment for it and sends the issues again, so nothing is lost;
* ``{"kind": "issue", "repo", "number", "step", "pending_intent"}``: a state file of this
  orchestrator with status ``in_progress``; ``pending_intent`` is the ``intent`` line of an
  act that has no ``done`` line, the thing a restart must settle first;
* ``{"kind": "plan", "repo", "number", "requested_at", "step"}``: an ``in_progress`` plan
  record (an open plan request holds a place, 5.7 point 1);
* ``{"kind": "unreadable", "file": ...}``: a state file or plan record that cannot be read.
  It counts as in flight for the poll (5.7 point 1), so it stops this end too; a person
  must look at it.

The orchestrator then releases its dispatches, prints the return contract and closes its own
terminal; those are the skill's steps and not this verb's.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import click

from superclaude.cli.issue_watch import wake
from superclaude.cli.issue_watch.predicates import WAKE_ID_PATTERN

from . import common, ext, state, wakefiles
from .state import EXIT_CONFLICT, EXIT_NOT_FOUND, StateError


def _wake_blockers(root: Path, ident: str) -> tuple[list[dict[str, Any]], list[str]]:
    blockers: list[dict[str, Any]] = []
    ignored: list[str] = []
    folder = wakefiles.wakes_dir(root)
    try:
        names = sorted(os.listdir(folder))
    except FileNotFoundError:
        return blockers, ignored  # no wake was ever written
    except OSError:  # a folder that cannot be listed is not an empty one
        return [{"kind": "unreadable", "file": "wakes"}], ignored
    for name in names:
        wake_id, dot, rest = name.partition(".")
        if rest != "json" or not dot or WAKE_ID_PATTERN.fullmatch(wake_id) is None:
            continue  # an acknowledgment, a rejection, a temporary file, the done folder
        try:
            data = wakefiles.read_capped(folder / name)
            parsed = wake.parse_wake(data, name)
        except (wake.WakeRejected, OSError):
            ignored.append(name)
            continue
        if (
            parsed.wake.target.orchestrator == ident
            and wake.read_ack(root, wake_id) is None
        ):
            blockers.append({"kind": "wake", "wake_id": wake_id})
    return blockers, ignored


def _file_blockers(root: Path, ident: str) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    for item in state.list_open(root, ident):
        if "reason" in item:
            blockers.append({"kind": "unreadable", "file": item["file"]})
        elif item["kind"] == "plan":
            blockers.append(
                {k: item[k] for k in ("repo", "number", "requested_at", "step")}
                | {"kind": "plan"}
            )
        else:
            blockers.append(
                {k: item[k] for k in ("repo", "number", "step", "pending_intent")}
                | {"kind": "issue"}
            )
    return blockers


def idle_end(root: Path | str, ident: str, wait_s: float = 10.0) -> dict[str, Any]:
    """Run the sequence above; return the result or raise ``pending_work`` with the blockers."""
    path = Path(root)
    with state.locked(path, wait_s):
        try:
            run = state.load_run(path, ident)
        except StateError as exc:
            if exc.reason == "not_found":
                raise StateError("run_not_found", EXIT_NOT_FOUND) from None
            raise
        if run["status"] == "ended":
            return {
                "run_status": "ended",
                "already_ended": True,
                "blockers": [],
                "ignored": [],
            }
        if run["status"] == "active":
            state.set_run_status(path, ident, "ending")
        wake_blockers, ignored = _wake_blockers(path, ident)
        blockers = wake_blockers + _file_blockers(path, ident)
        if blockers:
            state.set_run_status(path, ident, "active")
            raise StateError(
                "pending_work",
                EXIT_CONFLICT,
                run_status="active",
                blockers=blockers,
                ignored=ignored,
            )
        state.set_run_status(path, ident, "ended")
        return {
            "run_status": "ended",
            "already_ended": False,
            "blockers": [],
            "ignored": ignored,
        }


@click.command("idle-end")
@click.option(
    "--orchestrator",
    default=None,
    help="My orchestrator id (default: from the session tag).",
)
@click.option(
    "--tag",
    default=None,
    help="My session tag (default: the CLAUDE_TOPIC of this session).",
)
def idle_end_cmd(orchestrator, tag) -> None:
    """End this orchestrator only if nothing is pending, holding the lock for the whole check."""
    common.run(lambda: idle_end(common.root(), ext.identity(orchestrator, tag)[0]))
