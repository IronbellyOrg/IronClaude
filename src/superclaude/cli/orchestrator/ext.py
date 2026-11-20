"""What the verbs of B2 share when they talk to the outside: the runner, the answers and who I am.

* ``make_runner`` gives a verb its runner: the real ``SubprocessRunner`` behind
  ``limits.GuardedRunner``, so every ``gh``, ``git``, ``orca`` and ``ccsession`` call a
  verb makes passes ``limits.refuse`` first (5.9). A test replaces ``inner_runner``
  with a fake; the guard stays in the path.
* ``run_checked`` runs one call and gives its text, or a fixed reason when the call
  failed. The reason names the program and never holds stderr or an argument value.
* ``identity`` says which orchestrator this session is. The wake, the lease and the
  idle end are all about "my own" orchestrator: the id is taken from ``--orchestrator``,
  else from the session tag (``--tag``, else the environment variable ``CLAUDE_TOPIC``
  that ccsession sets, the same variable the poll reads to find a session), whose last
  two parts are the id (``orchestrator-ironclaude-1`` is ``ironclaude-1``).
* ``write_json`` writes a JSON file whole (temporary file plus ``rename``, mode 0600).
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Final

from superclaude.cli.issue_watch import launch
from superclaude.cli.issue_watch.predicates import ORCHESTRATOR_ID_PATTERN
from superclaude.cli.issue_watch.runner import Runner, SubprocessRunner
from superclaude.cli.swarm.atomic import write_prepared_bytes

from .limits import GuardedRunner
from .state import EXIT_INVALID, StateError

EXIT_EXTERNAL: Final = 6
"""A ``gh`` or ``ccsession`` call failed or its answer cannot be read."""
TAG_ENV: Final = "CLAUDE_TOPIC"
CALL_TIMEOUT_S: Final = 60.0

_ID_AT_END = re.compile(r"(?:^|-)(?P<id>[a-z0-9]{1,12}-[1-9][0-9]{0,5})$")


def inner_runner() -> Runner:
    """The runner behind the guard; a test replaces this to fake ``gh`` and ``ccsession``."""
    return SubprocessRunner()


def make_runner(caller: str, answer_ref: str | None = None) -> GuardedRunner:
    """A guarded runner for the verb ``caller`` (``answer_ref`` only after ``answer-check`` passed)."""
    return GuardedRunner(inner_runner(), caller=caller, answer_ref=answer_ref)


def run_checked(
    runner: Runner, argv: list[str], timeout: float = CALL_TIMEOUT_S
) -> str:
    """Run ``argv`` and return its stdout; ``external_failed`` (exit 6) when it did not succeed."""
    result = runner.run(argv, timeout)
    if result.timed_out or result.spawn_error is not None or result.returncode != 0:
        raise StateError(
            "external_failed", EXIT_EXTERNAL, program=os.path.basename(argv[0])
        )
    return result.stdout


def json_values(text: str) -> list[Any]:
    """Every JSON value in ``text``, one after the other (``gh api --paginate --jq`` output).

    ``external_unreadable`` (exit 6) when a part of the text is not JSON: a list that
    cannot be read whole is never read as a shorter list.
    """
    decoder = json.JSONDecoder()
    values: list[Any] = []
    index, end = 0, len(text)
    try:
        while True:
            while index < end and text[index].isspace():
                index += 1
            if index >= end:
                return values
            value, index = decoder.raw_decode(text, index)
            values.append(value)
    except (ValueError, RecursionError):
        raise StateError("external_unreadable", EXIT_EXTERNAL) from None


def identity(orchestrator: str | None, tag: str | None) -> tuple[str, str | None]:
    """``(orchestrator id, session tag or None)`` of this session (``own_identity_unknown`` when none)."""
    env_tag = os.environ.get(TAG_ENV) or None
    session_tag = tag if tag is not None else env_tag

    def derive(value: str | None) -> str | None:
        match = _ID_AT_END.search(value) if value is not None else None
        return match["id"] if match else None

    # The flags and the tag of the session must all name one orchestrator. A flag that
    # names another one than the environment tag of this session would let it read,
    # acknowledge or end the work of that other orchestrator.
    named = {x for x in (orchestrator, derive(session_tag), derive(env_tag)) if x}
    if len(named) > 1:
        raise StateError("identity_mismatch", EXIT_INVALID)
    ident = next(iter(named), None)
    if ident is None:
        raise StateError("own_identity_unknown", EXIT_INVALID)
    if ORCHESTRATOR_ID_PATTERN.fullmatch(ident) is None:
        raise StateError("invalid_orchestrator_id", EXIT_INVALID)
    if session_tag is not None and launch.TAG_PATTERN.fullmatch(session_tag) is None:
        raise StateError("invalid_tag", EXIT_INVALID)
    return ident, session_tag


def write_json(path: Path, doc: dict[str, Any]) -> None:
    """Write ``doc`` whole at mode 0600 (temporary file, fsync, ``rename``)."""
    os.makedirs(path.parent, mode=0o700, exist_ok=True)
    write_prepared_bytes(
        path, (json.dumps(doc, indent=2, sort_keys=True) + "\n").encode("ascii")
    )
