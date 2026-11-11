"""``superclaude observe``: the click command and the interaction loop (AD-1, AD-14, AD-17, AD-20).

Read-only. The only Orca calls are the ones ``adapter.py`` makes; no key and no option here
builds an argv or calls Orca. ``keys.py`` (POSIX only) is imported lazily inside the
interactive branch, so ``--once`` works on every platform.
"""

from __future__ import annotations

import io
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import click
from rich.live import Live

from superclaude.cli.observe.adapter import (
    ArgvRejected,
    LiveSource,
    check_run_id,
    production_runner,
)
from superclaude.cli.observe.collector import Collector, FixtureSource
from superclaude.cli.observe.export import (
    record_path,
    record_text,
    snapshot_json,
    snapshot_path,
    state_dir,
    write_atomic,
)
from superclaude.cli.observe.parse import load_fixture
from superclaude.cli.observe.render import render
from superclaude.cli.observe.terminal import (
    detect_size,
    make_console,
    output_encoding,
    resolve_policy,
)
from superclaude.cli.observe.view import (
    Effect,
    Session,
    apply_cycle,
    apply_key,
    build_view,
)

POSIX_ONLY_TEXT = (
    "interactive mode needs a POSIX terminal; use --once"  # PROPOSED wording
)
NO_TERMINAL_TEXT = "interactive mode needs a terminal on standard input; use --once"
READ_TIMEOUT = 0.1  # seconds a key read may wait; the loop redraws between reads
REDRAW_SECONDS = (
    0.5  # ages and STALE move with time, so the screen repaints at least this often
)
WIDTHS = ("160", "116", "80")

# The live coordinator-questions read is guarded by this one constant. It stays False until
# the owner has written a record that QUESTION-OBSERVATION passed (release-gates.md, "Agents
# cite the owner's statement, never write it"); plan Task 18 may flip it only against that
# record, cited by path. While False, ``--questions`` makes no Orca call, not even discovery.
QUESTION_GATE_PASSED = False
QUESTION_GATE_TEXT = (
    "question read not enabled: QUESTION-OBSERVATION has not passed"  # PROPOSED wording
)
QUESTIONS_NEED_RUN_TEXT = (
    "--questions needs --run <runId>: it reads the questions of one named Run only"
)
QUESTIONS_NEED_LIVE_TEXT = (
    "--questions needs a live source; it cannot be combined with --fixture"
)

HELP = """Read-only terminal observer for Orca workers.

Shows the worker ledger Orca reports for its workers (verbatim next-action kind,
freshness, collected / reported counts) and can write a plain-text record and a versioned JSON
snapshot. It never writes to Orca: no key and no option maps to an Orca call.

Poll caps (one read every 15 s, at most 5 calls per read) are per observer process; several
observers running at once multiply the load on Orca.

Coordinator questions (--questions, off until the owner records that QUESTION-OBSERVATION
passed): with --run <runId> the observer lists the messages of type question of that one
named Run, from one read per cycle. Run it from the terminal that already holds the Run: the
observer never runs run-use and never binds to a Run. The list is bounded best effort;
coverage unknown; bursts over 100 rows between reads may be lost. Message bodies are
received by this process; subjects are shown, bodies are not kept.
"""


# -- the real clock ------------------------------------------------------------------------------


class SystemClock:
    """The injected clock the rest of the package reads: monotonic, wall and local time zone."""

    def monotonic(self) -> float:
        return time.monotonic()

    def wall(self) -> float:
        return time.time()

    def local_tz(self) -> Any:
        return datetime.now().astimezone().tzinfo


# -- options and dependencies ------------------------------------------------------------------------


@dataclass(frozen=True)
class Options:
    once: bool = False
    width: int | None = None
    ascii: bool = False
    fixture: str | None = None
    run_id: str | None = None
    snapshot: str | None = None
    questions: bool = False  # R2: list the coordinator questions of the one --run Run


@dataclass
class Deps:
    """Everything outside the package, replaceable in tests. ``None`` means the real thing."""

    runner: Callable | None = None
    discover: Callable | None = None
    clock: Any = None
    env: Any = None
    encoding: str | None = None
    size: Callable[[], tuple[int, int]] | None = None
    platform: str | None = None
    key_source: Any = None
    screen_factory: Callable[[], Any] | None = None
    state_directory: Path | None = None
    stdout: Any = None
    interval: float | None = None
    extra: dict = field(default_factory=dict)


def _policy_maker(options: Options, deps: Deps) -> Callable[[], Any]:
    env = os.environ if deps.env is None else deps.env
    encoding = deps.encoding if deps.encoding is not None else output_encoding()
    size = deps.size or detect_size

    def make() -> Any:
        columns, rows = size()
        return resolve_policy(
            env, encoding, {"ascii": options.ascii}, options.width or columns, rows
        )

    return make


def _build_source(options: Options, deps: Deps) -> Any:
    if options.fixture:
        return FixtureSource(options.fixture)
    kwargs: dict[str, Any] = {}
    if deps.discover is not None:
        kwargs["discover"] = deps.discover
    return LiveSource(deps.runner or production_runner, **kwargs)


def _questions_on(options: Options) -> bool:
    """True only when ``--questions`` is asked for and the gate guard is open."""
    return bool(options.questions and QUESTION_GATE_PASSED)


def _question_refusal(options: Options) -> tuple[int, str] | None:
    """(exit code, plain message) when ``--questions`` cannot run; checked before any Orca call."""
    if not options.questions:
        return None
    if options.fixture:
        return 2, QUESTIONS_NEED_LIVE_TEXT
    if not options.run_id:
        return 2, QUESTIONS_NEED_RUN_TEXT
    try:
        check_run_id(options.run_id)
    except ArgvRejected as exc:
        return 2, f"--questions needs a valid --run id: {exc}"
    if not QUESTION_GATE_PASSED:
        return 1, QUESTION_GATE_TEXT
    return None


def _emit(text: str, deps: Deps) -> None:
    if deps.stdout is not None:
        deps.stdout.write(text)
        return
    encoding = deps.encoding if deps.encoding is not None else output_encoding()
    buffer = getattr(sys.stdout, "buffer", None)
    if buffer is None:
        sys.stdout.write(text)
        return
    buffer.write(text.encode(encoding, errors="replace"))
    buffer.flush()


def _write_snapshot(view: Any, target: Path) -> str | None:
    """One snapshot file, replaced atomically; the error text when it could not be written."""
    try:
        write_atomic(target, snapshot_json(view))
    except OSError as exc:
        return f"snapshot failed: {exc}"
    return None


# -- --once ----------------------------------------------------------------------------------------------


def run_once(options: Options, deps: Deps) -> int:
    clock = deps.clock or SystemClock()
    source = _build_source(options, deps)
    collector = Collector(
        source, clock, run_id=options.run_id, questions=_questions_on(options)
    )
    result = collector.run_once()
    session = apply_cycle(Session(), result, clock)
    view = build_view(result, session, clock)
    if options.width is not None:  # the width-bound screen, through a recorded console
        policy = _policy_maker(options, deps)()
        console = make_console(policy, file=io.StringIO(), record=True)
        console.print(render(view, policy))
        text = console.export_text()
    else:
        text = record_text(view)
    _emit(text, deps)
    if options.snapshot:
        failure = _write_snapshot(view, Path(options.snapshot))
        if failure:
            click.echo(failure, err=True)
            return 1
    return 0


# -- the interaction loop -------------------------------------------------------------------------------------


class LiveScreen:
    """The real screen: ``Live(screen=True)`` over a console made by ``make_console``."""

    def __init__(self) -> None:
        self._live: Live | None = None
        self._shape: tuple | None = None

    def draw(self, view: Any, policy: Any, message: str | None) -> None:
        shape = (policy.width, policy.height, policy.ascii, policy.no_color)
        group = render(view, policy, message)
        if self._live is None or shape != self._shape:
            self.close()
            self._live = Live(
                group, console=make_console(policy), screen=True, auto_refresh=False
            )
            self._live.start()
            self._shape = shape
        self._live.update(group, refresh=True)

    def close(self) -> None:
        if self._live is not None:
            self._live.stop()
            self._live = None


def run_loop(
    collector: Any,
    keys: Any,
    screen: Any,
    clock: Any,
    *,
    make_policy: Callable[[], Any],
    directory: Path,
    snapshot_file: Path,
    write_snapshots: bool,
) -> int:
    """Poll, read keys, redraw. Keys change the session only; ``q`` or Ctrl-C ends it."""
    session = Session()
    seen = -1
    written = 0
    message: str | None = None
    last_draw: float | None = None
    collector.start()
    try:
        while True:
            result = collector.latest()
            dirty = False
            if result.cycle != seen:
                session = apply_cycle(session, result, clock)
                seen = result.cycle
                dirty = True
                if write_snapshots and result.cycle > written:
                    written = (
                        result.cycle
                    )  # exactly one write per cycle, after failures too
                    failure = _write_snapshot(
                        build_view(result, session, clock), snapshot_file
                    )
                    message = failure or message
            view = build_view(result, session, clock)
            key = keys.read(READ_TIMEOUT)
            if key is not None:
                session, effect = apply_key(session, key, view, clock)
                message = None
                dirty = True
                if effect is Effect.QUIT:
                    return 0
                if effect is Effect.EXPORT:
                    target = record_path(directory, view)
                    try:
                        write_atomic(target, record_text(view))
                        message = f"exported {target}"
                    except OSError as exc:
                        message = f"export failed: {exc}"
                view = build_view(result, session, clock)
            if keys.consume_redraw():
                dirty = True
            now = clock.monotonic()
            if dirty or last_draw is None or now - last_draw >= REDRAW_SECONDS:
                screen.draw(view, make_policy(), message)
                last_draw = now
    except KeyboardInterrupt:
        return 0
    except (
        Exception
    ) as exc:  # a render failure stops the screen; it never retries silently
        screen.close()
        click.echo(f"observe: display failed: {exc}", err=True)
        return 1
    finally:
        collector.stop()
        screen.close()


def run_interactive(options: Options, deps: Deps) -> int:
    platform = deps.platform if deps.platform is not None else sys.platform
    if platform == "win32":
        click.echo(POSIX_ONLY_TEXT)
        return 2
    from superclaude.cli.observe.keys import KeySource  # lazy: POSIX only

    clock = deps.clock or SystemClock()
    keys = deps.key_source or KeySource()
    with keys:
        if not keys.available:
            click.echo(NO_TERMINAL_TEXT)
            return 2
        collector = Collector(
            _build_source(options, deps),
            clock,
            interval=deps.interval if deps.interval is not None else 15.0,
            run_id=options.run_id,
            questions=_questions_on(options),
        )
        directory = deps.state_directory or state_dir()
        live = not options.fixture
        return run_loop(
            collector,
            keys,
            (deps.screen_factory or LiveScreen)(),
            clock,
            make_policy=_policy_maker(options, deps),
            directory=directory,
            snapshot_file=Path(options.snapshot)
            if options.snapshot
            else snapshot_path(directory),
            write_snapshots=live or bool(options.snapshot),
        )


def execute(options: Options, deps: Deps | None = None) -> int:
    """Run the command; returns the process exit code."""
    refusal = _question_refusal(options)  # before any Orca call, discovery included
    if refusal is not None:
        click.echo(refusal[1], err=True)
        return refusal[0]
    deps = deps or Deps()
    if options.once:
        return run_once(options, deps)
    return run_interactive(options, deps)


# -- click ------------------------------------------------------------------------------------------------------


def _check_fixture(
    ctx: click.Context, param: click.Parameter, value: str | None
) -> str | None:
    if value is not None:
        try:
            load_fixture(value)
        except ValueError as exc:
            raise click.BadParameter(str(exc)) from exc
    return value


def _check_run(
    ctx: click.Context, param: click.Parameter, value: str | None
) -> str | None:
    if value is not None:
        try:
            check_run_id(value)
        except ArgvRejected as exc:
            raise click.BadParameter(str(exc)) from exc
    return value


@click.group(name="observe", invoke_without_command=True, help=HELP)
@click.option(
    "--once",
    is_flag=True,
    help="Read once, print the plain-text record to stdout and exit.",
)
@click.option(
    "--width",
    type=click.Choice(WIDTHS),
    default=None,
    help="Bind the output to 160, 116 or 80 columns; with --once prints the screen text instead of the record.",
)
@click.option(
    "--ascii",
    "ascii_mode",
    is_flag=True,
    help="Use ASCII only (also chosen for a non-UTF-8 terminal).",
)
@click.option(
    "--fixture",
    default=None,
    callback=_check_fixture,
    help="Replay a synthetic fixture variant instead of calling Orca (for example base).",
)
@click.option(
    "--run",
    "run_id",
    default=None,
    callback=_check_run,
    help="Read one Run only (an Orca run id).",
)
@click.option(
    "--snapshot",
    "snapshot",
    type=click.Path(dir_okay=False),
    default=None,
    help="Write the JSON snapshot to this file (default for live mode: the per-user state directory).",
)
@click.option(
    "--questions",
    "questions",
    is_flag=True,
    help="List the coordinator questions (message type question) of the one Run named by "
    "--run. Needs --run and a live source; refused until QUESTION-OBSERVATION has passed.",
)
@click.pass_context
def observe_group(
    ctx: click.Context,
    once: bool,
    width: str | None,
    ascii_mode: bool,
    fixture: str | None,
    run_id: str | None,
    snapshot: str | None,
    questions: bool,
) -> None:
    if ctx.invoked_subcommand is not None:
        return
    options = Options(
        once=once,
        width=int(width) if width else None,
        ascii=ascii_mode,
        fixture=fixture,
        run_id=run_id,
        snapshot=snapshot,
        questions=questions,
    )
    code = execute(options)
    if code:
        ctx.exit(code)


__all__ = ["Deps", "Options", "SystemClock", "execute", "observe_group", "run_loop"]
