"""Command line shell of ``superclaude sweep`` (DESIGN 3.2, 5, 7.1).

``sweep run`` is the one impure step: it checks the arguments (exit 2), binds a Run,
calls ``probes.collect``, ``classify.classify_all`` and ``report.render`` (the pure
steps), publishes the report with ``_publish`` (the only function in the package that
writes), and prints one JSON object. Exit 0 means the report was published; 1 is an
internal error with a ``[sweep <stage>]`` stderr prefix; 2 is a usage error. Only
``run`` ends the process.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import click

from . import probes
from .classify import classify_all
from .models import SweepContext
from .report import render, sanitize, to_json

DEFAULT_WINDOW = "6h"  # FR-003, OQ-5
MAX_WINDOW_HOURS = 720  # 30 days
MAX_SUFFIX = 99  # report names: <stem>.md, then <stem>-2.md to <stem>-99.md (FR-017)


class _PublishError(Exception):
    """A failed publication; ``lines`` are the stderr lines, already prefixed."""

    def __init__(self, *lines: str) -> None:
        super().__init__(lines[0])
        self.lines = lines


# --- Argument checks (every failure is a usage error, exit 2, nothing written) ----------


def _parse_window(text: str) -> timedelta:
    """``<N>h`` or ``<N>d``: ASCII digits, 1 to 9999, at most 720h or 30d (FR-003)."""
    if re.fullmatch(r"[1-9][0-9]{0,3}[hd]", text) is not None:
        count, unit = int(text[:-1]), text[-1]
        hours = count if unit == "h" else count * 24
        if hours <= MAX_WINDOW_HOURS:
            return timedelta(hours=hours)
    raise click.UsageError(
        f"invalid --window value: {sanitize(text)} (use <N>h or <N>d, at most 720h or 30d)"
    )


def _has_git(path: Path) -> bool:
    """Plain stat only: ``.git`` may be a folder or, in a linked worktree, a file."""
    try:
        os.stat(path / ".git")
    except OSError:
        return False
    return True


def _find_root(start: Path) -> Path:
    """Walk up from ``start`` to the first folder that holds ``.git`` (FR-004)."""
    here = start.resolve()
    for folder in (here, *here.parents):
        if _has_git(folder):
            return folder
    raise click.UsageError(f"no git checkout found above {sanitize(start)}")


def _check_root(root: str | None) -> Path:
    if root is None:
        return _find_root(Path.cwd())
    path = Path(root)
    try:
        resolved = path.resolve()
        usable = resolved.is_dir() and _has_git(resolved)
    except (OSError, RuntimeError):
        usable = False
    if not usable:
        raise click.UsageError(f"invalid --root: {sanitize(root)}")
    return resolved


def _check_run_ids(values: tuple[str, ...]) -> tuple[str, ...]:
    """Each id must match the Run id regex; duplicates collapse, first-seen order (FR-002)."""
    for value in values:
        if re.fullmatch(probes.RUN_ID_RE, value) is None:
            raise click.UsageError(f"invalid --run value: {sanitize(value)}")
    return tuple(dict.fromkeys(values))


def _within(path: Path, folder: Path) -> bool:
    return path == folder or path.is_relative_to(folder)


def _check_output(output: Path | None, root: Path, inputs: tuple[Path, ...]) -> Path:
    """The resolved output folder: ``<root>/.dev/sweeps/`` or below, and apart from inputs."""
    base = (
        root / ".dev" / "sweeps"
    )  # not resolved: a symlinked sweeps folder must fail below
    try:
        resolved = (output if output is not None else base).resolve()
    except (OSError, RuntimeError):
        raise click.UsageError(f"invalid --output: {sanitize(output)}") from None
    if not _within(resolved, base):
        raise click.UsageError(
            f"invalid --output: {sanitize(output if output is not None else base)} "
            f"(must be {sanitize(base)}/ or a folder below it)"
        )
    for source in inputs:
        try:
            where = source.resolve()
        except (OSError, RuntimeError):
            continue
        if _within(resolved, where) or _within(where, resolved):
            raise click.UsageError(
                f"invalid --output: {sanitize(resolved)} overlaps the input folder "
                f"{sanitize(where)}"
            )
    return resolved


# --- Publication: the one write (DESIGN 3.2) ---------------------------------------------


def _sweeps_base(output_dir: Path) -> Path | None:
    """The ``<root>/.dev/sweeps`` folder that holds ``output_dir`` (it was checked first)."""
    for folder in (output_dir, *output_dir.parents):
        if folder.name == "sweeps" and folder.parent.name == ".dev":
            return folder
    return None


def _drop_own_temp(tmp: Path) -> tuple[str, ...]:
    """Unlink this run's own temp file; a failure becomes one extra stderr line."""
    try:
        os.unlink(tmp)
    except OSError:
        return (f"[sweep publish] left temp file {tmp}",)
    return ()


def _write_all(fd: int, data: bytes) -> None:
    view = memoryview(data)
    while view:
        view = view[os.write(fd, view) :]
    os.fsync(fd)


def _publish(text: str, output_dir: Path, now: datetime) -> Path:
    """Write ``text`` to a temp file, then link it to the first free report name."""
    stem = now.strftime("%Y%m%d-%H%M%S") + "-sweep"
    base = _sweeps_base(output_dir)
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as exc:  # no file was written; folders it made may remain
        raise _PublishError(f"[sweep publish] {exc}") from exc
    if base is None or not _within(output_dir.resolve(), base):
        raise _PublishError(
            f"[sweep publish] output dir escaped {base if base else output_dir}/"
        )
    data = text.encode(
        "utf-8"
    )  # before the temp file exists, so an encode error leaves none
    tmp = output_dir / f".{stem}.{os.getpid()}.tmp"
    try:
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666)
    except FileExistsError as exc:  # not ours, so it is left alone
        raise _PublishError(f"[sweep publish] temp file exists: {tmp}") from exc
    except OSError as exc:
        raise _PublishError(f"[sweep publish] {exc}") from exc
    try:
        try:
            _write_all(fd, data)
        finally:
            os.close(fd)
    except OSError as exc:
        raise _PublishError(f"[sweep publish] {exc}", *_drop_own_temp(tmp)) from exc
    names = [f"{stem}.md"] + [f"{stem}-{n}.md" for n in range(2, MAX_SUFFIX + 1)]
    published: Path | None = None
    for name in names:
        try:
            os.link(
                tmp, output_dir / name
            )  # fails when the name exists: never overwrites
        except FileExistsError:
            continue
        except OSError as exc:
            raise _PublishError(
                f"[sweep publish] cannot link report: {exc}", *_drop_own_temp(tmp)
            ) from exc
        published = output_dir / name  # the commit point
        break
    if published is None:
        raise _PublishError(
            f"[sweep publish] report name space exhausted: {output_dir}",
            *_drop_own_temp(tmp),
        )
    try:
        os.unlink(tmp)
    except OSError as exc:  # the complete report stays; no success JSON
        raise _PublishError(
            f"[sweep publish] could not remove temp file {tmp}"
        ) from exc
    return published


# --- The command -------------------------------------------------------------------------


@click.group("sweep")
def sweep_group() -> None:
    """Read-only sweep of Orca Runs, worktrees and sessions."""


@sweep_group.command("run")
@click.option(
    "--run",
    "run_ids",
    multiple=True,
    help="Orca Run id to read; repeat for several. Default: the Run bound to this terminal.",
)
@click.option(
    "--window",
    default=DEFAULT_WINDOW,
    show_default=True,
    help="Activity window: <N>h or <N>d, at most 720h or 30d.",
)
@click.option(
    "--root",
    default=None,
    help="Checkout root. Default: found from the current folder.",
)
@click.option(
    "--output",
    default=None,
    help="Report folder, <root>/.dev/sweeps/ or below. Default: <root>/.dev/sweeps/.",
)
def run(
    run_ids: tuple[str, ...], window: str, root: str | None, output: str | None
) -> None:
    """Collect, classify and publish one read-only report; print one JSON object."""
    stage = "args"
    try:
        now = datetime.now(timezone.utc).replace(microsecond=0)
        span = _parse_window(window)
        checkout = _check_root(root)
        runs = _check_run_ids(tuple(run_ids))
        home = Path.home()
        state = Path(os.environ.get("XDG_STATE_HOME") or (home / ".local" / "state"))
        output_dir = _check_output(
            Path(output) if output is not None else None,
            checkout,
            (
                checkout / ".dev" / "tasks",
                home / ".claude" / "projects",
                state / "ccsession" / "orca-tabs",
            ),
        )
        budget = probes.Budget()
        if not runs:
            stage = "bind"
            runs = (probes.bind_run(budget),)
        ctx = SweepContext(now, span, now - span, checkout, runs)
        stage = "collect"
        collected = probes.collect(ctx, runs, checkout, budget)
        stage = "classify"
        result = classify_all(collected, ctx)
        stage = "render"
        text = render(result, ctx)
        stage = "publish"
        report = _publish(text, output_dir, now)
        stage = "output"
        payload = json.dumps(to_json(result, ctx, str(report)))
        click.echo(payload)
    except (click.UsageError, probes.BindingError) as exc:
        click.echo(getattr(exc, "message", None) or str(exc), err=True)
        sys.exit(2)
    except _PublishError as exc:
        for line in exc.lines:
            click.echo(line, err=True)
        sys.exit(1)
    except Exception as exc:  # an allowlist ValueError or any internal error
        click.echo(f"[sweep {stage}] {sanitize(exc)}", err=True)
        sys.exit(1)
