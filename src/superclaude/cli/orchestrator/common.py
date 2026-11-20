"""What every ``superclaude orchestrator`` verb shares: the root, the JSON answer and the exit code.

A verb prints one JSON object on stdout, ``{"ok": true, ...}`` or
``{"ok": false, "reason": "<code>", ...}``, and exits 0 or with the code of its
reason. The model that calls a verb reads the JSON; the reason is a fixed code and
never holds an argument value. A refusal of ``limits.refuse`` exits ``EXIT_REFUSED``
(2) the same way.

The root is the orchestrator repo, the folder that holds ``.orchestrator/``: the
``--root`` option of the group, the environment variable
``SUPERCLAUDE_ORCHESTRATOR_ROOT``, or the current directory (an orchestrator session
runs in the orchestrator repo, design 5.1).
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any, NoReturn

import click

from .limits import EXIT_REFUSED, Refused
from .state import EXIT_INVALID, StateError

ROOT_ENV = "SUPERCLAUDE_ORCHESTRATOR_ROOT"


def emit(payload: dict[str, Any]) -> None:
    """Print one JSON object on stdout."""
    click.echo(json.dumps(payload, sort_keys=True))


def fail(reason: str, code: int, **info: object) -> NoReturn:
    """Print ``{"ok": false, "reason": ...}`` and exit with ``code``."""
    emit({"ok": False, "reason": reason, **info})
    click.get_current_context().exit(code)
    raise AssertionError("unreachable")  # pragma: no cover


def root() -> Path:
    """The orchestrator repo of this call (``root_invalid``, exit 2, when it is not a folder)."""
    ctx = click.get_current_context()
    path = Path((ctx.obj or {}).get("root") or Path.cwd())
    if not path.is_dir():
        fail("root_invalid", EXIT_INVALID)
    return path


def run(action: Callable[[], dict[str, Any]]) -> None:
    """Run ``action``, print its result with ``ok: true``, or print the reason it failed."""
    try:
        result = action()
    except StateError as exc:
        fail(exc.reason, exc.code, **exc.info)
    except Refused as exc:
        fail(exc.reason, EXIT_REFUSED)
    except ValueError:  # a bad repo, number or time reached a parser
        fail("invalid_input", EXIT_INVALID)
    emit({"ok": True, **result})
