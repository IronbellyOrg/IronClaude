"""The first-run check of one repository's generated configuration (plan Task 21, R7, R18, R28).

A freshly generated config starts ``enabled: false``. ``first_run`` turns it on only after a
fixed list of checks all pass, in this order:

1. ``config``: the platform, ``cycle.load_config`` and ``cycle.validate_setup`` (the logic of
   ``check-config``);
2. ``label``: the trigger label exists on the repository (created through ``repo_init``);
3. ``init_state``: the state directory and store exist (a store that already exists is kept, never
   re-initialised);
4. ``dry_run``: one dry-run cycle exits 0 (the logic of ``once --dry-run``);
5. ``lock``: while the store lock is held, a second cycle ends with exit 75;
6. ``restart``: the state document reloads, a second dry-run exits 0, and ``dispatch.json`` is
   byte-for-byte what it was before the first dry-run.

When every step passes the config is rewritten with ``enabled: true`` (an atomic replace that
keeps mode 600). When one fails the config stays ``enabled: false``. Either way a short report is
written to ``<state dir>/first-run.txt``: the result line, the ship gate (``GOVERNED_LEVELS_ALLOWED``
of ``launch.py``: closed means only Pipeline None launches), the check of the ``Approved`` field and
``warning: approver_is_launch_account`` when the approvers file holds the launch account.

It is idempotent: a repository whose config is already enabled is left alone and runs no check.
Nothing here runs a process itself: the dry-run cycles take their dependencies from the caller's
``deps_factory`` and every ``gh`` call goes through the caller's ``Runner``. The base directories
and the clock are injectable, so a test writes only under ``tmp_path``.
"""

from __future__ import annotations

import json
import os
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from . import cycle, launch, record, repo_init
from .defaults import Defaults
from .runner import Runner

REPORT_FILE = "first-run.txt"
LOCK_HELD_EXIT = 75

STEPS = ("config", "label", "init_state", "dry_run", "lock", "restart")


@dataclass(frozen=True)
class Step:
    name: str
    ok: bool
    reason: str = "ok"


@dataclass(frozen=True)
class FirstRunResult:
    """``enabled`` is the config's ``enabled`` after the call; ``status`` says what happened."""

    status: str  # "enabled", "failed" or "already_enabled"
    enabled: bool
    steps: tuple[Step, ...] = ()
    report: str = ""
    report_path: Path | None = None
    notes: list[str] = field(default_factory=list)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _raw_config(path: Path) -> dict | None:
    try:
        raw = json.loads(path.read_bytes())
    except (OSError, ValueError, RecursionError):
        return None
    return raw if isinstance(raw, dict) else None


def _report_dir(config_path: Path, raw: dict | None) -> Path:
    """The state dir named in the config, else the folder that holds the config."""
    state = raw.get("state_dir") if raw else None
    if isinstance(state, str) and os.path.isabs(state):
        return Path(state)
    return config_path.parent


def _write_report(directory: Path, text: str, name: str = REPORT_FILE) -> Path | None:
    path = directory / name
    try:
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
    except OSError:
        return None
    return path


def _enable(config_path: Path, raw: dict) -> bool:
    """Rewrite the config with ``enabled: true``; an atomic replace that keeps mode 600."""
    staged = config_path.with_name(f".{config_path.name}.enable")
    try:
        fd = os.open(
            staged, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600
        )
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(
                json.dumps({**raw, "enabled": True}, indent=2, sort_keys=True) + "\n"
            )
        cycle.load_config(staged)  # the rewritten file must still load
        os.replace(staged, config_path)
        return True
    except (OSError, cycle.ConfigError):
        return False
    finally:
        staged.unlink(missing_ok=True)


def _store_bytes(state_dir: Path) -> bytes | None:
    try:
        return (state_dir / record.STORE_FILE).read_bytes()
    except OSError:
        return None


def first_run(
    config_path: Path,
    defaults: Defaults,
    runner: Runner,
    deps_factory: Callable[[cycle.Config], cycle.Deps],
    *,
    now: Callable[[], datetime] = _now,
) -> FirstRunResult:
    """Run the first-run check for ``config_path`` and enable it when every step passes."""
    config_path = Path(config_path)
    raw = _raw_config(config_path)
    if raw is not None and raw.get("enabled") is True:
        return FirstRunResult("already_enabled", True)
    directory = _report_dir(config_path, raw)
    # A config with no readable state_dir reports next to itself, under its own name, so two
    # repositories never overwrite one report.
    report_name = (
        REPORT_FILE
        if directory != config_path.parent
        else (f"{config_path.stem}-{REPORT_FILE}")
    )
    steps: list[Step] = []
    lines: list[str] = []

    def done(failed: Step | None) -> FirstRunResult:
        ok = failed is None
        enabled = False
        if ok and raw is not None:
            enabled = _enable(config_path, raw)
            if not enabled:
                failed = Step("config", False, "enable_failed")
                steps.append(failed)
                ok = False
        head = (
            "first-run: passed"
            if ok
            else f"first-run: failed {failed.name}: {failed.reason}"
        )  # type: ignore[union-attr]
        gate = "open" if launch.GOVERNED_LEVELS_ALLOWED else "closed"
        gate_note = (
            "all pipeline levels may launch"
            if gate == "open"
            else "only Pipeline None launches"
        )
        text = "\n".join([head, f"ship_gate: {gate} ({gate_note})", *lines]) + "\n"
        path = _write_report(directory, text, report_name)
        return FirstRunResult(
            "enabled" if ok else "failed", enabled, tuple(steps), text, path
        )

    # 1. config: the platform, the file, the worktree and the approvers
    try:
        cycle.check_platform()
        config = cycle.load_config(config_path)
        approvers = cycle.validate_setup(config)
    except cycle.ConfigError as exc:
        step = Step("config", False, exc.reason)
        steps.append(step)
        return done(step)
    steps.append(Step("config", True))
    directory = config.state_dir  # the report now lives in the state directory
    report_name = REPORT_FILE
    if config.owner_account_id in approvers and (
        config.owner_account_id not in config.approval_excluded_ids
    ):
        lines.append("warning: approver_is_launch_account")

    # 2. the trigger label (created when missing) and the Approved field (reported only)
    label = repo_init.ensure_trigger_label(config.repo, defaults, runner)
    lines.append(f"trigger_label: {label}")
    owner = config.repo.split("/")[0]
    lines.append(
        f"approved_field: {repo_init.check_approved_field(owner, defaults, runner)}"
    )
    if label not in (repo_init.CREATED, repo_init.PRESENT):
        step = Step("label", False, "label_failed")
        steps.append(step)
        return done(step)
    steps.append(Step("label", True, label))

    # 3. the state directory and store; an existing store is kept, never re-initialised
    try:
        record.init_state(config.state_dir, now())
        steps.append(Step("init_state", True, "created"))
    except record.StateExists:
        steps.append(Step("init_state", True, "state_exists"))
    except record.StoreError as exc:
        step = Step("init_state", False, exc.reason)
        steps.append(step)
        return done(step)
    baseline = _store_bytes(config.state_dir)

    # 4. one dry-run cycle
    first = cycle.run_cycle(deps_factory(config), True)
    if first.exit_code != 0:
        step = Step("dry_run", False, str(first.reason))
        steps.append(step)
        return done(step)
    steps.append(Step("dry_run", True))

    # 5. the lock test: while the store lock is held, a second cycle ends with exit 75
    second_deps = deps_factory(config)
    with second_deps.store.lock():
        held = cycle.run_cycle(deps_factory(config), True)
    if held.exit_code != LOCK_HELD_EXIT:
        step = Step("lock", False, "lock_not_detected")
        steps.append(step)
        return done(step)
    steps.append(Step("lock", True))

    # 6. the restart test: the state reloads and a second dry-run changes nothing
    try:
        record.FileStore(config.state_dir).load()
    except record.StoreError:
        step = Step("restart", False, "state_not_reloadable")
        steps.append(step)
        return done(step)
    again = cycle.run_cycle(deps_factory(config), True)
    if again.exit_code != 0:
        step = Step("restart", False, f"dry_run:{again.reason}")
        steps.append(step)
        return done(step)
    if _store_bytes(config.state_dir) != baseline:
        step = Step("restart", False, "state_changed")
        steps.append(step)
        return done(step)
    steps.append(Step("restart", True))
    return done(None)
