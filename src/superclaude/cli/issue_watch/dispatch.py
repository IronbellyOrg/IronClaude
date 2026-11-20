"""The dispatcher core: one sweep over every Orca repository (plan Task 23, R5, R15, R16, R26, R32).

One cron entry runs a sweep. A sweep:

1. lists the usable repositories with ``orca repo list`` (Task 18). A failed or unreadable list is
   an error result, never a clean one (R15);
2. for a repository with no config, generates one (Task 19) and runs its first-run check (Task 21);
   a repository whose config is not enabled is skipped with a reason, not run;
3. starts ``superclaude issue-watch once --config <file>`` as a child process for each enabled
   repository, one after another, through the ``Runner`` (absolute paths only: cron has no PATH).

Rules:

* the whole loop stops starting children after ``LOOP_CAP_S`` (270 s); each child is killed after
  ``CHILD_TIMEOUT_S`` (255 s), longer than the cycle's own 240 s deadline. A repository not reached is
  skipped with a reason and reported;
* the order rotates every sweep: the next start index is kept in ``rotation.json`` under the state
  directory. A sweep that did not reach every repository starts the next one at the first repository
  it did not reach;
* the loop stops starting children after the first child whose output holds a ``launched:`` or an
  ``attempted:`` line. A child that was killed (by a signal) or timed out counts as a launch attempt and stops the
  loop too, unless that repository's ``dispatch.json`` (read through ``record.py``, read only) shows no
  pending, launched or unknown entry created during this sweep. A child that cannot run, or that
  exits non-zero without launching, never stops the loop, and a timeout never kills it;
* ``DAY_CAP`` stays per repository: the cycle of each child applies it.

Each child's exit code and reason are kept in ``ChildResult`` for the report (Task 25). This module
runs nothing itself: every command goes through the ``Runner``.
"""

from __future__ import annotations

import json
import os
import re
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from . import cycle, record, repo_init
from .defaults import Defaults
from .first_run import first_run
from .generate import Base, _projects, ensure_config
from .launch import check_origin
from .predicates import format_utc, parse_utc
from .repos import OrcaRepo, RepoListError, list_repos
from .runner import Runner

LOOP_CAP_S = 270.0
CHILD_TIMEOUT_S = 255.0
GIT_TIMEOUT_S = 15.0
ROTATION_FILE = "rotation.json"
RATE_WAIT_FILE = "account-rate-wait.json"
LOCK_FILE = "run-all.lock"
SUBDIR = "issue-watch.d"

# Every reason a sweep gives for a repository it did not run (plan Tasks 23 and 24). The reasons that
# also exist in ``audit.REASON_TABLE`` keep their meaning; the rest are documented here.
SKIP_REASONS: dict[str, str] = {
    "stopped_after_launch": "an earlier repo launched or attempted a launch this sweep",
    "loop_cap": "the 270 second loop cap was reached before this repo",
    "account_rate_wait": "a child hit the account rate limit; no child starts until its time",
    "not_enabled": "the config is enabled: false (the first run did not pass, or the owner set it)",
    "config_unreadable": "the config file cannot be read as JSON",
    "config_invalid": "cycle.load_config refused the config (audit reason config_invalid)",
    "worktree_invalid": "the Coordinator worktree is not an existing directory (audit reason)",
    "worktree_not_git": "the Coordinator worktree has no .git entry",
    "origin_mismatch": "the worktree's origin does not name the repo (audit reason)",
    "label_missing": "the trigger label is missing on the repo (the loop never creates it)",
    "label_check_failed": "the label list could not be read",
    "approved_field_missing": "the organization has no single-select Approved field with the option",
    "approved_field_check_failed": "the organization issue fields could not be read",
    "no_project": "the repo has no Project",
    "project_ambiguous": "several Projects and the defaults map does not name the configured one",
    "project_mismatch": "the configured Project is not one of the repo's Projects",
    "project_check_failed": "the repo's Projects could not be read",
    "not_generated": "the config generator gave no reason (should not happen)",
    "project_read_failed": "the repo's Projects could not be read (config generation)",
    "bad_name": "the Orca repo name is not a safe file name (config generation)",
    "bad_repo": "the origin owner/name is not a strict owner/name (config generation)",
    "approvers_file_exists": "an approvers file is there without a config; never overwritten (generation)",
    "account_read_failed": "gh api user could not be read (config generation)",
    "approver_read_failed": "a fixed approver login could not be turned into an id (generation)",
    "maintainers_read_failed": "the repo's maintainers could not be read (config generation)",
    "no_approvers": "no approver is left once the launch account is removed (config generation)",
    "generated_invalid": "the generated config failed its own validation and was removed (generation)",
    "path_in_tmp": "the Orca repo path is under /tmp (from the repo list)",
    "origin_unreadable": "git could not read the repo's origin (from the repo list)",
    "origin_not_github": "the repo's origin is not on github.com (from the repo list)",
    "foreign_owner": "the repo's owner is not an allowed owner (from the repo list)",
}

_LAUNCHED = re.compile(r"^launched: ([1-9][0-9]{0,8})$", re.M)
_ATTEMPTED = re.compile(r"^attempted: ([1-9][0-9]{0,8})$", re.M)
_REASON = re.compile(r"^cycle: ([a-z][a-z0-9_]{0,63})$", re.M)
_OPEN_STATES = ("pending", "launched", "unknown")


@dataclass(frozen=True)
class ChildResult:
    """What one child did; kept for the report."""

    name: str
    repo: str
    exit_code: int | None
    reason: str | None
    launched: int | None = None
    attempted: int | None = None
    killed: bool = False
    seconds: float = 0.0


@dataclass(frozen=True)
class Skipped:
    name: str
    reason: str


@dataclass(frozen=True)
class SweepResult:
    """``error`` is set (and ``ok`` false) when the repository list could not be read."""

    ok: bool
    error: str | None = None
    children: tuple[ChildResult, ...] = ()
    skipped: tuple[Skipped, ...] = ()
    stopped_after: str | None = None
    elapsed_s: float = 0.0
    generated: tuple[str, ...] = ()
    waiting_until: datetime | None = None
    """Set when the account rate wait stopped the whole sweep (no list, no child)."""
    would_run: tuple[str, ...] = ()
    would_generate: tuple[str, ...] = ()
    """Filled by a dry run only: the repos a real sweep would run, and generate a config for."""
    notes: list[str] = field(default_factory=list)


def _now() -> datetime:
    return datetime.now(timezone.utc)


# --- the loop lock ---------------------------------------------------------------------------


class LoopLockHeld(Exception):
    """Another sweep holds the loop lock."""


@contextmanager
def loop_lock(base: Base) -> Iterator[None]:
    """Hold an exclusive ``flock`` on ``<state dir>/issue-watch/run-all.lock`` for one sweep.

    Raises ``LoopLockHeld`` at once when another sweep holds it (never waits). The lock is
    released and its descriptor closed in a ``finally``.
    """
    import fcntl  # not at module level: importing the package must work off Linux

    path = base.state_dir.expanduser() / "issue-watch" / LOCK_FILE
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise LoopLockHeld from None
        yield
    finally:
        os.close(fd)  # closing the descriptor releases the flock


# --- rotation ------------------------------------------------------------------------------


def _rotation_path(base: Base) -> Path:
    return base.state_dir.expanduser() / "issue-watch" / ROTATION_FILE


def _read_rotation(base: Base) -> int:
    try:
        raw = json.loads(_rotation_path(base).read_text(encoding="utf-8"))
        value = raw["next"]
    except (OSError, ValueError, KeyError, TypeError):
        return 0
    return value if type(value) is int and value >= 0 else 0


def _write_rotation(base: Base, value: int) -> None:
    path = _rotation_path(base)
    try:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        staged = path.with_name(f".{path.name}.new")
        fd = os.open(staged, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps({"next": value}) + "\n")
        os.replace(staged, path)
    except OSError:
        pass  # the rotation is a fairness aid; losing it only restarts at the first repo


# --- children -----------------------------------------------------------------------------


def _config_path(base: Base, name: str) -> Path:
    return base.config_dir.expanduser() / SUBDIR / f"{name}.json"


def _enabled(path: Path) -> bool | None:
    try:
        raw = json.loads(path.read_bytes())
    except (OSError, ValueError, RecursionError):
        return None
    return raw.get("enabled") if isinstance(raw, dict) else None


def _opened_this_sweep(config_path: Path, since: datetime) -> bool:
    """True unless the repo's store shows no open entry created at or after ``since``.

    Read only, through ``record.py``. A store that cannot be read counts as open: the loop stops.
    """
    try:
        config = cycle.load_config(config_path)
        doc = record.FileStore(config.state_dir).load()
    except (cycle.ConfigError, record.StoreError, OSError):
        return True
    return any(
        e.state in _OPEN_STATES and e.pending_at is not None and e.pending_at >= since
        for e in doc.entries.values()
    )


def _rate_wait_path(base: Base) -> Path:
    return base.state_dir.expanduser() / "issue-watch" / RATE_WAIT_FILE


def _read_rate_wait(base: Base) -> datetime | None:
    """The stored account wait time, or None when there is none or it cannot be read."""
    try:
        raw = json.loads(_rate_wait_path(base).read_text(encoding="utf-8"))
        return parse_utc(raw["next_permitted_at"])
    except (OSError, ValueError, KeyError, TypeError):
        return None


def _write_rate_wait(base: Base, when: datetime) -> None:
    path = _rate_wait_path(base)
    try:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        staged = path.with_name(f".{path.name}.new")
        fd = os.open(staged, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps({"next_permitted_at": format_utc(when)}) + "\n")
        os.replace(staged, path)
    except OSError:
        pass  # without the file the next sweep still stops: each child honours its own store


def _child_next_permitted(config_path: Path) -> datetime | None:
    """The child's ``next_permitted_at`` from its store (read only), else None."""
    try:
        config = cycle.load_config(config_path)
        return record.FileStore(config.state_dir).load().next_permitted_at
    except (cycle.ConfigError, record.StoreError, OSError):
        return None


def _precheck(
    runner: Runner,
    config: cycle.Config,
    defaults: Defaults,
    field_cache: dict[str, str],
) -> str | None:
    """The reads that run before a child (R14); the skip reason of the first that fails.

    Nothing is created here: a missing label or field is reported and the repo is skipped.
    """
    if not config.worktree.is_dir():
        return "worktree_invalid"
    if not (config.worktree / ".git").exists():
        return "worktree_not_git"
    if check_origin(runner, config.worktree, GIT_TIMEOUT_S, config.repo) is not None:
        return "origin_mismatch"
    label = repo_init.trigger_label_state(config.repo, defaults, runner)
    if label != repo_init.PRESENT:
        return "label_missing" if label == repo_init.MISSING else "label_check_failed"
    owner = config.repo.split("/")[0]
    if owner not in field_cache:
        field_cache[owner] = repo_init.check_approved_field(owner, defaults, runner)
    if field_cache[owner] != repo_init.FIELD_PRESENT:
        if field_cache[owner] == repo_init.FIELD_MISSING:
            return "approved_field_missing"
        return "approved_field_check_failed"
    ids = _projects(runner, config.repo)
    if ids is None:
        return "project_check_failed"
    if not ids:
        return "no_project"
    if config.project_id not in ids:
        return "project_mismatch"
    if len(ids) > 1 and defaults.projects.get(config.repo) != config.project_id:
        return "project_ambiguous"
    return None


def _run_child(
    runner: Runner,
    superclaude: str,
    repo: OrcaRepo,
    config_path: Path,
    monotonic: Callable[[], float],
) -> ChildResult:
    argv = [superclaude, "issue-watch", "once", "--config", str(config_path)]
    started = monotonic()
    result = runner.run(argv, CHILD_TIMEOUT_S)
    seconds = round(monotonic() - started, 3)
    # A child ended by a signal has a negative return code and no launch line, so it is the same
    # unknown outcome as a timeout: the store check decides whether it opened a launch.
    if result.timed_out or (result.returncode is not None and result.returncode < 0):
        reason = "child_timeout" if result.timed_out else "child_signal"
        return ChildResult(
            repo.name, repo.slug, None, reason, killed=True, seconds=seconds
        )
    if result.spawn_error is not None:
        return ChildResult(repo.name, repo.slug, None, "spawn_error", seconds=seconds)
    launched = _LAUNCHED.search(result.stdout)
    attempted = _ATTEMPTED.search(result.stdout)
    reason = _REASON.search(result.stdout)
    return ChildResult(
        repo.name,
        repo.slug,
        result.returncode,
        reason.group(1) if reason else None,
        launched=int(launched.group(1)) if launched else None,
        attempted=int(attempted.group(1)) if attempted else None,
        seconds=seconds,
    )


def run_sweep(
    runner: Runner,
    *,
    orca: str,
    superclaude: str,
    defaults: Defaults,
    base: Base,
    deps_factory: Callable[[cycle.Config], cycle.Deps],
    monotonic: Callable[[], float] = time.monotonic,
    now: Callable[[], datetime] = _now,
    dry_run: bool = False,
) -> SweepResult:
    """Run one sweep; see the module docstring for the rules.

    ``dry_run`` lists the repositories and the decision for each, and only reads: it generates no
    config, writes no rotation or wait file, creates no label and starts no child.
    """
    for label, path in (("orca", orca), ("superclaude", superclaude)):
        if not os.path.isabs(path):
            raise ValueError(f"{label} must be an absolute path (cron has no PATH)")
    began = monotonic()
    since = now()
    wait = _read_rate_wait(base)
    if wait is not None and since < wait:
        # the account is rate limited: no list, no child, until the stored time (R5)
        return SweepResult(True, waiting_until=wait, elapsed_s=0.0)
    try:
        listing = list_repos(runner, orca, defaults.allowed_owners)
    except RepoListError as exc:
        return SweepResult(False, error=exc.reason)
    repos = sorted(listing.repos, key=lambda r: r.name)
    skipped = [Skipped(s.name, s.reason) for s in listing.skipped]
    children: list[ChildResult] = []
    generated: list[str] = []
    would_run: list[str] = []
    would_generate: list[str] = []
    stopped_after: str | None = None
    rate_waiting: datetime | None = None
    field_cache: dict[str, str] = {}
    if not repos:
        return SweepResult(
            True, skipped=tuple(skipped), elapsed_s=round(monotonic() - began, 3)
        )

    start = _read_rotation(base) % len(repos)
    order = repos[start:] + repos[:start]
    first_unreached: int | None = None
    for position, repo in enumerate(order):
        if rate_waiting is not None:
            skipped.append(Skipped(repo.name, "account_rate_wait"))
            first_unreached = (
                first_unreached if first_unreached is not None else position
            )
            continue
        if stopped_after is not None:
            skipped.append(Skipped(repo.name, "stopped_after_launch"))
            first_unreached = (
                first_unreached if first_unreached is not None else position
            )
            continue
        if monotonic() - began >= LOOP_CAP_S:
            skipped.append(Skipped(repo.name, "loop_cap"))
            first_unreached = (
                first_unreached if first_unreached is not None else position
            )
            continue
        config_path = _config_path(base, repo.name)
        if not config_path.exists():
            if (
                dry_run
            ):  # generating writes files and calls GitHub: a dry run only says so
                would_generate.append(repo.name)
                continue
            outcome = ensure_config(repo, defaults, runner, base)
            if outcome.status == "skipped":
                skipped.append(Skipped(repo.name, outcome.reason or "not_generated"))
                continue
            if outcome.status == "generated":
                generated.append(repo.name)
                first_run(config_path, defaults, runner, deps_factory)
        enabled = _enabled(config_path)
        if enabled is not True:
            skipped.append(
                Skipped(
                    repo.name,
                    "not_enabled" if enabled is False else "config_unreadable",
                )
            )
            continue
        try:
            config = cycle.load_config(config_path)
        except cycle.ConfigError:
            skipped.append(Skipped(repo.name, "config_invalid"))
            continue
        why = _precheck(runner, config, defaults, field_cache)
        if why is not None:
            skipped.append(Skipped(repo.name, why))
            continue
        if dry_run:
            would_run.append(repo.name)
            continue
        # shortcut: setup and checks above can take time, so the cap is read again here; a child
        # that starts just under the cap still runs up to 255 s, so a sweep can last 270 + 255 s and
        # the loop lock plus `flock -n` skip one cron tick; upgrade if that tick must not be lost.
        if monotonic() - began >= LOOP_CAP_S:
            skipped.append(Skipped(repo.name, "loop_cap"))
            first_unreached = (
                first_unreached if first_unreached is not None else position
            )
            continue
        child = _run_child(runner, superclaude, repo, config_path, monotonic)
        children.append(child)
        if child.reason == "rate_limited":
            # plain rate_limited only: rate_limit_clamped is the 3600 s clamp and writes nothing
            when = _child_next_permitted(config_path) or since
            rate_waiting = when
            if when > since:
                _write_rate_wait(base, when)
        elif child.launched is not None or child.attempted is not None:
            stopped_after = repo.name
        elif child.killed and _opened_this_sweep(config_path, since):
            stopped_after = repo.name  # a killed child counts as a launch attempt
    if dry_run:
        pass  # a dry run writes no rotation file
    elif first_unreached is None:
        _write_rotation(base, (start + 1) % len(repos))
    else:
        _write_rotation(base, (start + first_unreached) % len(repos))
    return SweepResult(
        True,
        children=tuple(children),
        skipped=tuple(skipped),
        stopped_after=stopped_after,
        elapsed_s=round(monotonic() - began, 3),
        generated=tuple(generated),
        waiting_until=rate_waiting,
        would_run=tuple(would_run),
        would_generate=tuple(would_generate),
    )


__all__ = [
    "CHILD_TIMEOUT_S",
    "LOOP_CAP_S",
    "ChildResult",
    "LoopLockHeld",
    "Skipped",
    "SweepResult",
    "loop_lock",
    "run_sweep",
]
