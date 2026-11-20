"""Create the trigger label on a repository and check the ``Approved`` field (plan Task 20).

This module and ``issue_pipeline/complete.py`` are the only code that writes to GitHub. Only the
per-repo first run (Task 21) calls ``ensure_trigger_label``, which creates the label when it is
missing; the loop that runs from cron only calls ``trigger_label_state``, which reads (R14).

The approval is the organization issue field ``Approved`` set to ``Yes`` (R35), not a label. This
module only checks that the field and its option exist (``check_approved_field``, a read); it
never creates the field, which is an organization setting for the owner.

The label, field and option names come from the central defaults (Task 17), never from literals
here. Every command runs through the ``Runner`` (an argv list, no shell).

[UNVERIFIED] The reply shape of ``GET orgs/<owner>/issue-fields`` is read defensively: a list of
fields, or an object holding one under ``fields``, each with a ``name``, a type word that holds
``single_select`` and a list of ``options`` with a ``name``. Anything else is ``failed``.
"""

from __future__ import annotations

import json
import re

from .defaults import Defaults
from .github import _repo_arg
from .runner import CommandResult, Runner

TIMEOUT_S = 30.0
LABEL_LIMIT = 500
LABEL_COLOR = "0E8A16"
LABEL_DESCRIPTION = "The issue watcher may claim this issue once it is approved"

CREATED = "created"
PRESENT = "present"
MISSING = "missing"
FAILED = "failed"
FIELD_PRESENT = "approved_field_present"
FIELD_MISSING = "approved_field_missing"

_OWNER = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")


def _ok(result: CommandResult) -> bool:
    return not (
        result.timed_out or result.spawn_error is not None or result.returncode != 0
    )


def _json(result: CommandResult) -> object | None:
    if not _ok(result):
        return None
    try:
        return json.loads(result.stdout)
    except ValueError:
        return None


def argv_label_list(repo: str) -> list[str]:
    return [
        "gh",
        "label",
        "list",
        "--repo",
        _repo_arg(repo),
        "--json",
        "name",
        "--limit",
        str(LABEL_LIMIT),
    ]


def argv_label_create(repo: str, label: str) -> list[str]:
    return [
        "gh",
        "label",
        "create",
        label,
        "--repo",
        _repo_arg(repo),
        "--color",
        LABEL_COLOR,
        "--description",
        LABEL_DESCRIPTION,
    ]


def argv_issue_fields(owner: str) -> list[str]:
    if not _OWNER.fullmatch(owner):
        raise ValueError("invalid owner")
    return ["gh", "api", "--method", "GET", f"orgs/{owner}/issue-fields"]


def trigger_label_state(repo: str, defaults: Defaults, runner: Runner) -> str:
    """``present``, ``missing`` or ``failed``; reads only, never creates (the cron loop, R14)."""
    data = _json(runner.run(argv_label_list(repo), TIMEOUT_S))
    if not isinstance(data, list) or not all(
        isinstance(row, dict) and isinstance(row.get("name"), str) for row in data
    ):
        return FAILED
    if len(data) >= LABEL_LIMIT:
        return (
            FAILED  # a full list may hide the label; do not create a duplicate blindly
        )
    names = {row["name"] for row in data}
    return PRESENT if defaults.trigger_label in names else MISSING


def ensure_trigger_label(repo: str, defaults: Defaults, runner: Runner) -> str:
    """Create the trigger label when it is missing; ``created``, ``present`` or ``failed``.

    Idempotent: a present label makes no create call. Only the first run calls this.
    """
    state = trigger_label_state(repo, defaults, runner)
    if state != MISSING:
        return state  # PRESENT or FAILED
    created = runner.run(argv_label_create(repo, defaults.trigger_label), TIMEOUT_S)
    return CREATED if _ok(created) else FAILED


def _fields(data: object) -> list[object] | None:
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("fields"), list):
        return data["fields"]
    return None


def check_approved_field(owner: str, defaults: Defaults, runner: Runner) -> str:
    """``approved_field_present``, ``approved_field_missing`` or ``failed``; a read.

    Present means a single-select field named ``defaults.approval_field`` that has the option
    ``defaults.approval_option``. The field is never created here.
    """
    fields = _fields(_json(runner.run(argv_issue_fields(owner), TIMEOUT_S)))
    if fields is None:
        return FAILED
    for field in fields:
        if not isinstance(field, dict) or field.get("name") != defaults.approval_field:
            continue
        kind = str(field.get("data_type") or field.get("type") or "").lower()
        options = field.get("options")
        if "single_select" not in kind or not isinstance(options, list):
            continue
        names = {o.get("name") for o in options if isinstance(o, dict)}
        if defaults.approval_option in names:
            return FIELD_PRESENT
    return FIELD_MISSING
