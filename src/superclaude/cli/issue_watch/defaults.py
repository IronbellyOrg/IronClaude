"""The central defaults of the issue watcher (plan Task 17, requirement R1).

``issue-watch-defaults.json`` is the file the Coder template saves under the config
directory (``~/.config/superclaude`` by default). It holds the values every repository
shares: who may approve, the trigger label, the approval issue field, the owners whose
repositories may be served and an optional map from ``owner/name`` to a Project node id.

This module is pure: it reads that one file and runs no command. A key the file leaves out
takes its built-in value, and an absent file gives the built-ins. Unknown keys, a wrong
type, a bad login, a bad repository name or a Project id that is not ``PVT_...`` raise
``ConfigError("config_invalid")`` with a fixed detail text that never quotes the file.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from .cycle import ConfigError
from .github import valid_repo
from .predicates import APPROVAL_FIELD_NAME, APPROVAL_FIELD_VALUE

DEFAULTS_FILE = "issue-watch-defaults.json"
DEFAULT_CONFIG_DIR = "~/.config/superclaude"

BUILTIN_APPROVER_LOGINS = ("ironbelly", "clayphi")
BUILTIN_TRIGGER_LABEL = "issue-watch:trigger"
BUILTIN_ALLOWED_OWNERS = ("IronbellyOrg",)

_KEYS = frozenset(
    {
        "approver_logins",
        "trigger_label",
        "approval_field",
        "approval_option",
        "allowed_owners",
        "projects",
    }
)
_MAX_BYTES = 64 * 1024
_LOGIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")
_OWNER = _LOGIN
_PROJECT_ID = re.compile(r"PVT_[A-Za-z0-9_-]{1,64}")
_NAME_MAX = 50


@dataclass(frozen=True)
class Defaults:
    """The validated central defaults."""

    approver_logins: tuple[str, ...] = BUILTIN_APPROVER_LOGINS
    trigger_label: str = BUILTIN_TRIGGER_LABEL
    approval_field: str = APPROVAL_FIELD_NAME
    approval_option: str = APPROVAL_FIELD_VALUE
    allowed_owners: tuple[str, ...] = BUILTIN_ALLOWED_OWNERS
    projects: dict[str, str] = field(default_factory=dict)
    """``owner/name`` to a Project node id; empty by default."""


def _invalid(detail: str) -> ConfigError:
    return ConfigError("config_invalid", f"{DEFAULTS_FILE}: {detail}")


def _name(value: object, key: str) -> str:
    """A short single-line name with no comma, no control character and no leading dash."""
    if (
        not isinstance(value, str)
        or not 0 < len(value) <= _NAME_MAX
        or value.startswith("-")
        or "," in value
        or any(ord(c) < 32 or ord(c) == 127 for c in value)
    ):
        raise _invalid(f"{key} must be a short single-line name")
    return value


def _logins(value: object, key: str, pattern: re.Pattern[str]) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or not value
        or not all(isinstance(v, str) and pattern.fullmatch(v) for v in value)
    ):
        raise _invalid(f"{key} must be a non-empty list of GitHub names")
    if len({v.lower() for v in value}) != len(value):
        raise _invalid(f"{key} must not repeat a name")
    return tuple(value)


def _projects(value: object) -> dict[str, str]:
    if not isinstance(value, dict):
        raise _invalid("projects must be an object of owner/name to a PVT_ id")
    for repo, project_id in value.items():
        if not valid_repo(repo):
            raise _invalid("a projects key must be owner/name")
        if not isinstance(project_id, str) or not _PROJECT_ID.fullmatch(project_id):
            raise _invalid("a projects value must be a PVT_ Project node id")
    return dict(value)


def load_defaults(config_dir: str | Path = DEFAULT_CONFIG_DIR) -> Defaults:
    """Read ``issue-watch-defaults.json`` from ``config_dir``; the built-ins when it is absent.

    Reads one file and runs no command. A present file that cannot be read or parsed, or that
    holds an unknown key or a bad value, raises ``ConfigError("config_invalid")``.
    """
    path = Path(config_dir).expanduser() / DEFAULTS_FILE
    try:
        if not path.is_file():
            if path.exists() or path.is_symlink():
                raise _invalid("it is not a regular file")
            return Defaults()
        with open(path, "rb") as handle:
            data = handle.read(_MAX_BYTES + 1)
    except ConfigError:
        raise
    except OSError:
        raise _invalid("it cannot be read") from None
    if len(data) > _MAX_BYTES:
        raise _invalid("it is larger than 64 KiB")
    try:
        raw = json.loads(data)
    except (ValueError, RecursionError):  # ValueError covers bad JSON and UTF-8
        raise _invalid("it is not valid JSON") from None
    if not isinstance(raw, dict):
        raise _invalid("it must be a JSON object")
    unknown = set(raw) - _KEYS
    if unknown:
        raise _invalid("it holds an unknown key")
    base = Defaults()
    return Defaults(
        approver_logins=_logins(raw["approver_logins"], "approver_logins", _LOGIN)
        if "approver_logins" in raw
        else base.approver_logins,
        trigger_label=_name(raw["trigger_label"], "trigger_label")
        if "trigger_label" in raw
        else base.trigger_label,
        approval_field=_name(raw["approval_field"], "approval_field")
        if "approval_field" in raw
        else base.approval_field,
        approval_option=_name(raw["approval_option"], "approval_option")
        if "approval_option" in raw
        else base.approval_option,
        allowed_owners=_logins(raw["allowed_owners"], "allowed_owners", _OWNER)
        if "allowed_owners" in raw
        else base.allowed_owners,
        projects=_projects(raw["projects"]) if "projects" in raw else {},
    )
