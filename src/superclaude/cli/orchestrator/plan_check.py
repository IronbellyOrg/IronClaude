"""The verb ``superclaude orchestrator plan-check``: are the three plan sections of an issue body filled in (4.11, 5.3).

    plan-check --body-file <file>

The check is ``issue_watch.hold.plan_check`` and nothing else: this module imports it, so
the poll that holds an issue and the orchestrator that re-reads it live decide with one
function (a test asserts the identity). It reads text only: no model and no GitHub call.
The body is read from a file (the caller wrote the live body there), never from an
argument. A body that passes prints ``{"ok": true, "missing": []}`` and exits 0; one that
does not prints ``{"ok": false, "reason": "plan_incomplete", "missing": [...]}`` with the
closed tokens ``priority``, ``fix_approach`` and ``test_plan``, and exits 3.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

import click

from superclaude.cli.issue_watch.hold import plan_check

from . import common
from .state import EXIT_CONFLICT, StateError

MAX_BODY_BYTES: Final = 1024 * 1024


def _read_body(path: Path) -> str:
    try:
        with open(path, "rb") as handle:
            data = handle.read(MAX_BODY_BYTES + 1)
    except OSError:
        raise StateError("body_unreadable", 2) from None
    if len(data) > MAX_BODY_BYTES:
        raise StateError("body_too_large", 2)
    return data.decode("utf-8")


@click.command("plan-check")
@click.option(
    "--body-file",
    required=True,
    type=click.Path(dir_okay=False, path_type=Path),
    help="A file that holds the issue body (read live, written by the caller).",
)
def plan_check_cmd(body_file: Path) -> None:
    """Say whether ## Priority, ## Fix approach and ## Test plan are each present once and filled in."""

    def action() -> dict[str, Any]:
        result = plan_check(_read_body(body_file))
        if not result.ok:
            raise StateError(
                "plan_incomplete", EXIT_CONFLICT, missing=list(result.missing)
            )
        return {"missing": []}

    common.run(action)
