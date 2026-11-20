"""The verb ``superclaude orchestrator state``: the one way a wave writes its state file (design 5.5).

Every sub-command prints one JSON object (see ``common``). The rules a wave follows:

* ``intent`` before an outward act, ``done`` after it. After a restart,
  ``pending`` (or ``list``, which carries ``pending_intent`` for each file) shows an
  ``intent`` with no ``done``; settle it by reading the outside state, never by
  repeating the act, then write ``done``.
* ``create`` makes the state file of an issue and refuses a second one (exit 3).
* ``set`` records ids, the body hash and the tiers; ``status`` ends or reopens a file.
* ``plan-create``, ``plan-step`` and ``plan-show`` keep the plan record of one plan
  request; ``run-create``, ``run-show`` and ``run-status`` keep ``runs/<id>.json``.

Exit codes: 0 done; 2 invalid input; 3 the state does not allow it (the file exists, an
``intent`` is open, the status is final); 4 a file that cannot be read or is too big,
never overwritten; 5 no such file; 75 the lock stayed held.

With ``SUPERCLAUDE_TEST_FAILPOINTS=1`` the ``intent`` sub-command can end the process
right after it saves its line (``failpoint``); that is for the restart test only.
"""

from __future__ import annotations

import json
from typing import Any

import click

from . import common, failpoint, state
from .state import EXIT_INVALID, StateError

_repo = click.option("--repo", required=True, help="owner/name of the issue's repo.")
_number = click.option("--number", required=True, type=int, help="The issue number.")
_wave = click.option(
    "--wave", required=True, type=click.IntRange(0, 9), help="Wave 0 to 9."
)
_step = click.option(
    "--step", required=True, help="The step name, lower case with underscores."
)
_detail = click.option(
    "--detail", default=None, help="One line of detail (at most 2000 characters)."
)
_requested_at = click.option(
    "--requested-at",
    required=True,
    help="The requested_at of the plan request, UTC like 2026-11-19T10:00:00Z.",
)
_run_id = click.option(
    "--id", "ident", required=True, help="The orchestrator id, like ironclaude-1."
)


def _summary(doc: dict[str, Any]) -> dict[str, Any]:
    keys = ("repo", "number", "orchestrator", "status", "wave", "step")
    return {k: doc[k] for k in keys if k in doc}


@click.group(name="state")
def state_group() -> None:
    """Write and read the state files, plan records and run files under .orchestrator/."""


@state_group.command("create")
@_repo
@_number
@click.option(
    "--orchestrator",
    required=True,
    help="The id of the orchestrator that holds the issue.",
)
@click.option(
    "--wake-id", default=None, help="The wake id; none for a hand-run --take."
)
@click.option("--wave", default=1, type=click.IntRange(0, 9), show_default=True)
@click.option("--step", default="claim", show_default=True)
@click.option(
    "--retake",
    is_flag=True,
    help="Move an escalated closeout or hand-back file aside first (--take).",
)
def create_cmd(repo, number, orchestrator, wake_id, wave, step, retake) -> None:
    """Create the state file of an issue; a second file for one key is refused."""
    common.run(
        lambda: _summary(
            state.create_state(
                common.root(),
                repo,
                number,
                orchestrator,
                wake_id=wake_id,
                wave=wave,
                step=step,
                retake=retake,
            )
        )
    )


@state_group.command("show")
@_repo
@_number
def show_cmd(repo, number) -> None:
    """Print the whole state file and its unsettled intent."""

    def action() -> dict[str, Any]:
        doc = state.load_state(common.root(), repo, number)
        return {"state": doc, "pending_intent": state.pending_intent(doc)}

    common.run(action)


@state_group.command("list")
@click.option(
    "--orchestrator", default=None, help="Only the files of this orchestrator."
)
@click.option("--status", default="in_progress", show_default=True)
def list_cmd(orchestrator, status) -> None:
    """List the files with a status, with the unsettled intent of each (the restart rule)."""
    common.run(lambda: {"items": state.list_open(common.root(), orchestrator, status)})


@state_group.command("intent")
@_repo
@_number
@_wave
@_step
@_detail
def intent_cmd(repo, number, wave, step, detail) -> None:
    """Write the intent line before an outward act."""

    def action() -> dict[str, Any]:
        doc = state.record_intent(common.root(), repo, number, wave, step, detail)
        # Ends the process here, before any output, only when the test variables are set.
        failpoint.after_intent(wave, step)
        return _summary(doc)

    common.run(action)


@state_group.command("done")
@_repo
@_number
@_wave
@_step
@_detail
def done_cmd(repo, number, wave, step, detail) -> None:
    """Write the done line after an outward act (or for an effect already visible outside)."""
    common.run(
        lambda: _summary(
            state.record_done(common.root(), repo, number, wave, step, detail)
        )
    )


@state_group.command("pending")
@_repo
@_number
def pending_cmd(repo, number) -> None:
    """Print the intent line with no done line, or null."""
    common.run(
        lambda: {
            "pending_intent": state.pending_intent(
                state.load_state(common.root(), repo, number)
            )
        }
    )


def _ids(pairs: tuple[str, ...]) -> dict[str, object]:
    ids: dict[str, object] = {}
    for pair in pairs:
        name, sep, value = pair.partition("=")
        if not sep or name not in state.IDS_CHECKS:
            raise StateError("unknown_id_name", EXIT_INVALID)
        digits = state.IDS_CHECKS[name](1)  # the names whose value is a number
        ids[name] = (
            None if value == "" else int(value) if digits and value.isdigit() else value
        )
    return ids


def _tiers(text: str | None) -> dict[str, dict[str, object]] | None:
    if text is None:
        return None
    try:
        tiers = json.loads(text)
    except ValueError:
        raise StateError("invalid_tiers", EXIT_INVALID) from None
    if not isinstance(tiers, dict) or not all(
        isinstance(v, dict) for v in tiers.values()
    ):
        raise StateError("invalid_tiers", EXIT_INVALID)
    return tiers


@state_group.command("set")
@_repo
@_number
@click.option(
    "--id",
    "pairs",
    multiple=True,
    metavar="NAME=VALUE",
    help="An id found so far; an empty value removes it.",
)
@click.option("--body-sha", default=None, help="The hash of the issue body (hex).")
@click.option(
    "--tiers-json", default=None, help='JSON like {"worker": {"requested": "tier2"}}.'
)
def set_cmd(repo, number, pairs, body_sha, tiers_json) -> None:
    """Record ids found so far, the body hash and the tiers."""
    common.run(
        lambda: _summary(
            state.set_fields(
                common.root(),
                repo,
                number,
                ids=_ids(pairs) or None,
                body_sha=body_sha,
                tiers=_tiers(tiers_json),
            )
        )
    )


@state_group.command("status")
@_repo
@_number
@click.argument("new_status")
def status_cmd(repo, number, new_status) -> None:
    """Move the file to a status: done, escalated, skipped, failed or (after an answer) in_progress."""
    common.run(
        lambda: _summary(state.set_status(common.root(), repo, number, new_status))
    )


@state_group.command("plan-create")
@_repo
@_number
@_requested_at
@click.option(
    "--orchestrator",
    required=True,
    help="The id of the orchestrator that took the request.",
)
def plan_create_cmd(repo, number, requested_at, orchestrator) -> None:
    """Create the plan record of one request, or find the one a kill left behind."""

    def action() -> dict[str, Any]:
        doc, created = state.create_plan(
            common.root(), repo, number, requested_at, orchestrator
        )
        return {"created": created, "status": doc["status"], "step": doc["step"]}

    common.run(action)


@state_group.command("plan-step")
@_repo
@_number
@_requested_at
@click.option("--step", required=True, type=click.Choice(state.PLAN_STEPS[1:]))
@_detail
def plan_step_cmd(repo, number, requested_at, step, detail) -> None:
    """Add a step: plan_written (detail: body hash), plan_done, or plan_failed (detail: the reason)."""

    def action() -> dict[str, Any]:
        doc = state.record_plan_step(
            common.root(), repo, number, requested_at, step, detail
        )
        return {"status": doc["status"], "step": doc["step"]}

    common.run(action)


@state_group.command("plan-show")
@_repo
@_number
@_requested_at
def plan_show_cmd(repo, number, requested_at) -> None:
    """Print one plan record."""
    common.run(
        lambda: {"plan": state.load_plan(common.root(), repo, number, requested_at)}
    )


@state_group.command("run-create")
@_run_id
@click.option("--run-id", required=True, help="The Orca Run id.")
@click.option(
    "--tag", required=True, help="The session tag, like orchestrator-ironclaude-1."
)
@click.option("--repo", required=True, help="owner/name of the orchestrator's repo.")
@click.option("--host", required=True, help="The host name.")
def run_create_cmd(ident, run_id, tag, repo, host) -> None:
    """Write runs/<id>.json at once, before anything else; a second one is refused."""
    common.run(
        lambda: {"run": state.create_run(common.root(), ident, run_id, tag, repo, host)}
    )


@state_group.command("run-show")
@_run_id
def run_show_cmd(ident) -> None:
    """Print runs/<id>.json (a missing file means a first start)."""
    common.run(lambda: {"run": state.load_run(common.root(), ident)})


@state_group.command("run-status")
@_run_id
@click.argument("new_status")
def run_status_cmd(ident, new_status) -> None:
    """Move a run: active to ending; ending back to active or on to ended (final)."""
    common.run(lambda: {"run": state.set_run_status(common.root(), ident, new_status)})
