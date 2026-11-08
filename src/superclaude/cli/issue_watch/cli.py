"""The ``superclaude issue-watch`` command group (design sections 4.1, 5.2, 10.2).

Part 1: the group, the shared ``--config`` option, ``build_deps`` and the verbs
``once``, ``status``, ``check-config`` and ``init-state``. Part 2: ``reset``
(design 4.1, DF-03, DF-04, DF-57). This module only
sequences calls into the package and maps results to exit codes; it holds no
business logic and never imports ``subprocess`` (every command runs through
``runner.SubprocessRunner``). It never catches ``SystemExit`` or
``BaseException`` around a cycle.
"""

from __future__ import annotations

import json
import shlex
import shutil
import socket
import sys
from datetime import datetime
from pathlib import Path
from typing import NoReturn
from uuid import uuid4

import click

from . import audit, cycle, record
from .launch import MAX_ISSUE_NUMBER, OrcaLauncher
from .record import FileStore, LockError, LockHeld, StoreError
from .runner import SubprocessRunner

_DEFAULT_CONFIG = "~/.config/superclaude/issue-watch.json"

# Exit codes of design 4.3 that this module returns itself.
_EXIT_UNHEALTHY = 1
_EXIT_CRASH = 1  # [PROPOSAL] C-3: an unexpected exception out of the cycle
_EXIT_CONFIG = 2
_EXIT_STORE = 6
_EXIT_LOCK_HELD = 75


def _expand_config(ctx: click.Context, param: click.Parameter, value: Path) -> Path:
    """Expand a leading ``~`` in the default and in a passed value (DF-13)."""
    try:
        return value.expanduser()
    except RuntimeError:  # no home directory can be resolved
        raise click.BadParameter("cannot expand ~: no home directory") from None


def _config_option(func):
    """The shared ``--config`` option; the file need not exist (it is exit 2)."""
    return click.option(
        "--config",
        "config_path",
        type=click.Path(path_type=Path),
        default=_DEFAULT_CONFIG,
        show_default=True,
        callback=_expand_config,
        help="Path of the JSON configuration file.",
    )(func)


def build_deps(config: cycle.Config) -> cycle.Deps:
    """Build the real ``Deps`` for one cycle (design 5.4, DF-45)."""
    runner = SubprocessRunner()
    return cycle.Deps(
        runner=runner,
        store=FileStore(config.state_dir),
        launcher=OrcaLauncher(runner),
        clock=cycle.SystemClock(),
        audit=audit.AuditLog(config.state_dir),
        config=config,
        which=shutil.which,
        host=socket.gethostname(),
    )


def _config_exit(exc: cycle.ConfigError) -> NoReturn:
    """Write the stderr audit fallback and a one-line message; exit 2."""
    audit.stderr_fallback(exc.reason, _EXIT_CONFIG)
    click.echo(f"issue-watch: {exc.reason}: {exc.detail}", err=True)
    sys.exit(_EXIT_CONFIG)


def _load_config(config_path: Path, *, platform: bool = True) -> cycle.Config:
    """Check the platform (unless ``platform`` is False) and load the config."""
    try:
        if platform:
            cycle.check_platform()
        return cycle.load_config(config_path)
    except cycle.ConfigError as exc:
        _config_exit(exc)


@click.group("issue-watch")
def issue_watch_group():
    """Poll GitHub for approved issues and start one Orca claim session each.

    Run `once` from a timer. `status` and `check-config` are read-only;
    `init-state` creates the state directory; `reset` forfeits a guarantee.

    Examples:

    \b
        superclaude issue-watch check-config
        superclaude issue-watch init-state
        superclaude issue-watch once --dry-run
        superclaude issue-watch status --json
    """


@issue_watch_group.command("once")
@click.option(
    "--dry-run",
    is_flag=True,
    help="Read and decide, but write no store and never call Orca.",
)
@_config_option
def once_command(dry_run: bool, config_path: Path) -> None:
    """Run one poll cycle and exit with its code (design 4.3)."""
    config = _load_config(config_path)
    try:
        result = cycle.run_cycle(build_deps(config), dry_run)
    except Exception as exc:  # never SystemExit, KeyboardInterrupt or BaseException
        # [PROPOSAL] (Gate C fix C-3, executor decision): reason cycle_crashed,
        # exit 1. The lock is already released by its context manager. Only the
        # exception class name is printed, never its message (it may hold text).
        audit.stderr_fallback("cycle_crashed", _EXIT_CRASH)
        click.echo(f"issue-watch: cycle_crashed: {type(exc).__name__}", err=True)
        sys.exit(_EXIT_CRASH)
    click.echo(f"cycle: {result.reason}")
    click.echo(f"exit: {result.exit_code}")
    if dry_run:
        if result.probe is not None:
            click.echo(f"probe: {result.probe}")
        if result.would_launch is not None:
            click.echo(f"would_launch: {result.would_launch}")
    sys.exit(result.exit_code)


def _print_status(report: dict) -> None:
    """The text form of ``status`` (design 10.2)."""
    age = report["last_completed_cycle_age_seconds"]
    click.echo(f"healthy: {'yes' if report['healthy'] else 'no'}")
    click.echo(f"last completed cycle age: {'never' if age is None else f'{age}s'}")
    click.echo(f"disabled since: {report['disabled_since'] or 'no'}")
    click.echo(f"next permitted at: {report['next_permitted_at'] or 'now'}")
    click.echo(f"day cap used: {report['day_cap_used']}")
    counts = report["counts"]
    click.echo(
        "counts: " + (", ".join(f"{k}={counts[k]}" for k in sorted(counts)) or "none")
    )
    click.echo(f"stale: {len(report['stale'])}")
    for item in report["stale"]:
        click.echo(
            f"  issue {item['issue']} {item['state']} {item['last_reason']}"
            f" updated {item['updated_at']}"
        )
    click.echo(f"retry: {len(report['retry'])}")
    for item in report["retry"]:
        click.echo(f"  issue {item['issue']}: run from {item['cwd']}")
        click.echo(f"    {shlex.join(item['argv'])}")


@issue_watch_group.command("status")
@click.option("--json", "as_json", is_flag=True, help="Print the report as JSON.")
@_config_option
def status_command(as_json: bool, config_path: Path) -> None:
    """Report health, counts, stale entries and retry commands (read-only)."""
    config = _load_config(config_path, platform=False)
    clock = cycle.SystemClock()
    try:
        report = cycle.status_report(
            FileStore(config.state_dir), audit.AuditLog(config.state_dir), clock.now()
        )
    except StoreError as exc:
        click.echo(f"issue-watch: {exc.reason}", err=True)
        sys.exit(_EXIT_STORE)
    if as_json:
        click.echo(json.dumps(report, indent=2, sort_keys=True))
    else:
        _print_status(report)
    sys.exit(0 if report["healthy"] else _EXIT_UNHEALTHY)


@issue_watch_group.command("check-config")
@_config_option
def check_config_command(config_path: Path) -> None:
    """Validate the configuration, worktree and approvers file; write nothing."""
    config = _load_config(config_path)
    try:
        cycle.validate_setup(config)
        mtime, count = cycle.approvers_summary(config.approvers_file)
    except cycle.ConfigError as exc:
        _config_exit(exc)
    click.echo("configuration is valid")
    click.echo(f"state_dir: {config.state_dir}")
    click.echo(f"approvers_file mtime: {mtime}")
    click.echo(f"approvers_file entries: {count}")


@issue_watch_group.command("init-state")
@_config_option
def init_state_command(config_path: Path) -> None:
    """Create the state directory, store and lock; refuse if a store exists."""
    config = _load_config(config_path)
    try:
        record.init_state(config.state_dir, cycle.SystemClock().now())
    except record.StateExists:
        click.echo("issue-watch: a store already exists; nothing changed", err=True)
        sys.exit(_EXIT_STORE)
    except StoreError as exc:
        click.echo(f"issue-watch: {exc.reason}", err=True)
        sys.exit(_EXIT_STORE)
    click.echo(f"state created: {config.state_dir}")


def _refuse_reset(message: str) -> NoReturn:
    """A usage error found before ``state_dir`` is known: fallback line, exit 2."""
    audit.stderr_fallback("reset_refused", _EXIT_CONFIG)
    click.echo(f"issue-watch: {message}", err=True)
    sys.exit(_EXIT_CONFIG)


def _save(store: FileStore, doc: record.StoreDoc) -> None:
    """Save ``doc``; a failed write is ``state_dir_unwritable`` (design 7.6)."""
    try:
        store.save(doc)
    except OSError:
        raise StoreError("state_dir_unwritable") from None


def _reset_locked(
    store: FileStore, issue: int | None, now: datetime
) -> tuple[str, int]:
    """Load, check, change and save under the lock (DF-57 order).

    Returns the audit reason and the exit code. The store is written only on
    the two successes.
    """
    try:
        doc = store.load()
        if issue is None:
            _save(store, record.reset_rate_limit(doc))
            return "operator_reset", 0
        try:
            changed = record.reset_entry(doc, issue, now)
        except record.TransitionError:
            return "reset_refused", _EXIT_CONFIG
        _save(store, changed)
        return "operator_reset", 0
    except StoreError as exc:
        return exc.reason, _EXIT_STORE


def _write_reset(
    log: audit.AuditLog,
    stamp: dict,
    issue: int | None,
    reason: str,
    code: int,
    *,
    rotate: bool,
) -> None:
    """Write the ONE audit line of this exit; never a ``cycle`` line (DF-03)."""
    if reason == "state_dir_unwritable":
        audit.stderr_fallback(reason, code, ts=stamp["ts"], host=stamp["host"])
        return
    if reason == "operator_reset" and issue is not None:
        line = audit.decision_line(**stamp, reason=reason, issue=issue)
    else:
        line = audit.warning_line(
            **stamp, reason=reason, issue=issue if reason == "reset_refused" else None
        )
    try:
        if rotate:
            log.rotate_if_needed()
        log.append(line)
    except OSError:
        audit.stderr_fallback(reason, code, ts=stamp["ts"], host=stamp["host"])


@issue_watch_group.command("reset")
@click.argument("issue", type=click.IntRange(1, MAX_ISSUE_NUMBER), required=False)
@click.option(
    "--forfeit-guarantee",
    is_flag=True,
    help="Required with ISSUE: allow that issue to be launched a second time.",
)
@click.option(
    "--rate-limit",
    is_flag=True,
    help="Clear next_permitted_at instead of resetting an issue.",
)
@_config_option
def reset_command(
    issue: int | None, forfeit_guarantee: bool, rate_limit: bool, config_path: Path
) -> None:
    """Forfeit the launch guarantee of one issue, or clear the rate limit.

    Use `reset ISSUE --forfeit-guarantee` (only for an abandoned or unknown
    issue) or `reset --rate-limit`, never both and never neither.

    Examples:

    \b
        superclaude issue-watch reset 42 --forfeit-guarantee
        superclaude issue-watch reset --rate-limit
    """
    by_issue = issue is not None
    if by_issue == rate_limit:
        _refuse_reset("reset needs ISSUE --forfeit-guarantee or --rate-limit, not both")
    if by_issue and not forfeit_guarantee:
        _refuse_reset(f"reset {issue} needs --forfeit-guarantee")
    config = _load_config(config_path)
    store = FileStore(config.state_dir)
    log = audit.AuditLog(config.state_dir)
    now = cycle.SystemClock().now()
    stamp = {
        "ts": cycle.format_utc(now),
        "host": socket.gethostname(),
        "login": None,
        "cycle_id": uuid4().hex,
        "dry_run": False,
    }
    try:
        with store.lock():
            reason, code = _reset_locked(store, issue, now)
            _write_reset(log, stamp, issue, reason, code, rotate=True)
    except LockHeld:
        reason, code = "lock_held", _EXIT_LOCK_HELD
        _write_reset(log, stamp, issue, reason, code, rotate=False)
    except LockError as exc:
        reason, code = exc.reason, _EXIT_STORE
        _write_reset(log, stamp, issue, reason, code, rotate=False)
    if code == 0:
        if by_issue:
            click.echo(f"issue {issue} may now be launched a second time")
        else:
            click.echo("rate limit cleared")
    elif reason == "reset_refused":
        click.echo(
            f"issue-watch: reset refused: issue {issue} has no abandoned or "
            "unknown entry; nothing changed",
            err=True,
        )
    else:
        click.echo(f"issue-watch: {reason}", err=True)
    sys.exit(code)
