"""Generate one repository's watcher configuration (plan Task 19, requirements R2 to R4, R12).

For a repository with no ``<config dir>/issue-watch.d/<name>.json`` this module reads four things
from GitHub (every call is a read), then writes the approvers file and the config, both mode 600:

1. the launch account: ``gh api user`` (R2);
2. the repository's Project: a GraphQL read of ``projectsV2`` (R3). None gives the skip reason
   ``no_project``; several use the id of the defaults map when it names one of them, else give
   ``project_ambiguous``;
3. the approvers (R4): the fixed logins of the defaults, turned into account ids with
   ``gh api users/<login>``, plus the repository's maintainers from
   ``gh api repos/<owner>/<name>/collaborators?permission=maintain``. The launch account's own
   id is never written to a generated approvers file (the warn-only exclusion of Task 9 stays the
   owner's choice for a hand-written one).

The result is checked with ``cycle.load_config`` and ``cycle.validate_approvers`` before it is
kept. A file that exists is never overwritten, and a generated config starts ``enabled: false``.
The ``state_dir`` is an explicit absolute path per repository (R12), so two repositories never
share state; this module does not create it (the first run does).

Every command runs through the ``Runner`` (an argv list, no shell). The GitHub calls are reads:
each REST call carries ``--method GET`` and the GraphQL call is a query.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

from . import cycle
from .defaults import Defaults
from .github import _repo_arg
from .repos import OrcaRepo
from .runner import CommandResult, Runner

TIMEOUT_S = 30.0
WORKTREES_DIR = "/home/coder/workspaces/worktrees"
DEFAULT_CONFIG_DIR = "~/.config/superclaude"
DEFAULT_STATE_DIR = "~/.local/state/superclaude"
SUBDIR = "issue-watch.d"

_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}")
_LOGIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")
_ID_MAX = 10**20 - 1

PROJECTS_QUERY = """query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    projectsV2(first: 100) {
      nodes { id number }
      pageInfo { hasNextPage }
    }
  }
}"""
"""The repository's Projects (R3): only ids and numbers are read."""


@dataclass(frozen=True)
class Base:
    """Where one generated configuration and its state live."""

    config_dir: Path
    state_dir: Path
    worktrees_dir: Path

    @classmethod
    def default(cls) -> Base:
        return cls(
            Path(DEFAULT_CONFIG_DIR).expanduser(),
            Path(DEFAULT_STATE_DIR).expanduser(),
            Path(WORKTREES_DIR),
        )


@dataclass(frozen=True)
class Outcome:
    """``generated``, ``exists`` (left untouched) or ``skipped`` with a closed reason."""

    status: str
    name: str
    reason: str | None = None
    config_path: Path | None = None
    approvers_path: Path | None = None
    state_dir: Path | None = None


# --- argv builders: every one is a read ---------------------------------------------------


def argv_account() -> list[str]:
    return ["gh", "api", "--method", "GET", "user", "--jq", "{id}"]


def argv_user_id(login: str) -> list[str]:
    if not _LOGIN.fullmatch(login):
        raise ValueError("invalid login")
    return ["gh", "api", "--method", "GET", f"users/{login}", "--jq", "{id}"]


def argv_projects(repo: str) -> list[str]:
    owner, name = _repo_arg(repo).split("/")
    return [
        "gh",
        "api",
        "graphql",
        "-f",
        f"query={PROJECTS_QUERY}",
        "-f",
        f"owner={owner}",
        "-f",
        f"name={name}",
    ]


def argv_maintainers(repo: str) -> list[str]:
    return [
        "gh",
        "api",
        "--method",
        "GET",
        f"repos/{_repo_arg(repo)}/collaborators?permission=maintain&per_page=100",
        "--jq",
        "[.[] | {id}]",
    ]


# --- reading -----------------------------------------------------------------------------


def _json(result: CommandResult) -> object | None:
    if result.timed_out or result.spawn_error is not None or result.returncode != 0:
        return None
    try:
        parsed = json.loads(result.stdout)
    except ValueError:
        return None
    if isinstance(parsed, dict) and parsed.get("errors"):
        return None
    return parsed


def _account_id(value: object) -> int | None:
    if type(value) is int and 1 <= value <= _ID_MAX:
        return value
    return None


def _read_id(runner: Runner, argv: list[str]) -> int | None:
    data = _json(runner.run(argv, TIMEOUT_S))
    return _account_id(data.get("id")) if isinstance(data, dict) else None


def _projects(runner: Runner, repo: str) -> list[str] | None:
    data = _json(runner.run(argv_projects(repo), TIMEOUT_S))
    try:
        connection = data["data"]["repository"]["projectsV2"]  # type: ignore[index]
        ids = [n["id"] for n in connection["nodes"]]
        more = connection.get("pageInfo", {}).get("hasNextPage")
    except (KeyError, TypeError, AttributeError):
        return None
    if more:  # shortcut: only the first 100 Projects are read, so more than that is a failed read
        return None
    if not all(
        isinstance(i, str) and re.fullmatch(r"PVT_[A-Za-z0-9_-]{1,64}", i) for i in ids
    ):
        return None
    return ids


def _maintainers(runner: Runner, repo: str) -> set[int] | None:
    data = _json(runner.run(argv_maintainers(repo), TIMEOUT_S))
    if not isinstance(data, list):
        return None
    ids = {_account_id(row.get("id")) for row in data if isinstance(row, dict)}
    if len(ids) != len(data) or None in ids:
        return None
    return {i for i in ids if i is not None}


# --- writing -----------------------------------------------------------------------------


def _write_new(path: Path, text: str) -> None:
    """Create ``path`` with mode 600; never overwrite (``FileExistsError``)."""
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)


def _skip(name: str, reason: str) -> Outcome:
    return Outcome("skipped", name, reason)


def ensure_config(
    repo_record: OrcaRepo, defaults: Defaults, runner: Runner, base: Base | None = None
) -> Outcome:
    """Generate ``<config dir>/issue-watch.d/<name>.json`` for ``repo_record`` when it is absent."""
    base = base or Base.default()
    name = repo_record.name
    if not _NAME.fullmatch(name):
        return _skip(name, "bad_name")
    try:
        repo = _repo_arg(repo_record.slug)
    except ValueError:
        return _skip(name, "bad_repo")
    directory = base.config_dir.expanduser() / SUBDIR
    config_path = directory / f"{name}.json"
    approvers_path = directory / f"{name}-approvers.txt"
    if config_path.exists() or config_path.is_symlink():
        return Outcome("exists", name, config_path=config_path)
    if approvers_path.exists() or approvers_path.is_symlink():
        return _skip(name, "approvers_file_exists")

    account = _read_id(runner, argv_account())
    if account is None:
        return _skip(name, "account_read_failed")

    projects = _projects(runner, repo)
    if projects is None:
        return _skip(name, "project_read_failed")
    if not projects:
        return _skip(name, "no_project")
    if len(projects) == 1:
        project_id = projects[0]
    else:
        mapped = defaults.projects.get(repo)
        if mapped is None or mapped not in projects:
            return _skip(name, "project_ambiguous")
        project_id = mapped

    approvers: set[int] = set()
    for login in defaults.approver_logins:
        found = _read_id(runner, argv_user_id(login))
        if found is None:
            return _skip(name, "approver_read_failed")
        approvers.add(found)
    maintainers = _maintainers(runner, repo)
    if maintainers is None:
        return _skip(name, "maintainers_read_failed")
    approvers |= maintainers
    approvers.discard(
        account
    )  # the launch account never approves from a generated file
    if not approvers:
        return _skip(name, "no_approvers")

    state_dir = base.state_dir.expanduser() / "issue-watch" / name
    raw = {
        "schema_version": cycle.SCHEMA_VERSION,
        "enabled": False,
        "repo": repo,
        "project_id": project_id,
        "owner_account_id": account,
        "worktree": str(base.worktrees_dir / name / "Coordinator"),
        "approvers_file": str(approvers_path),
        "state_dir": str(state_dir),
    }
    if defaults.trigger_label != cycle.DEFAULT_TRIGGER_LABEL:
        raw["labels"] = {"trigger": defaults.trigger_label}

    directory.mkdir(parents=True, exist_ok=True)
    directory.chmod(0o700)
    staged = directory / f".{name}.json.new"
    wrote_approvers = False
    try:
        _write_new(approvers_path, "".join(f"{i}\n" for i in sorted(approvers)))
        wrote_approvers = True
        staged.unlink(missing_ok=True)
        _write_new(staged, json.dumps(raw, indent=2, sort_keys=True) + "\n")
        cycle.load_config(staged)
        cycle.validate_approvers(approvers_path)
        os.link(
            staged, config_path
        )  # fails if the config appeared meanwhile: no overwrite
    except (cycle.ConfigError, OSError):
        if wrote_approvers:  # only a file this call created
            approvers_path.unlink(missing_ok=True)
        return _skip(name, "generated_invalid")
    finally:
        staged.unlink(missing_ok=True)
    return Outcome(
        "generated",
        name,
        config_path=config_path,
        approvers_path=approvers_path,
        state_dir=state_dir,
    )
