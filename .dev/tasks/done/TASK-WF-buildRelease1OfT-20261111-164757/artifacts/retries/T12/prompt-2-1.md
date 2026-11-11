070b5c110c47c9b4b6c478c2cdfd97ded5908394
Review one task for spec compliance.

Task brief: 
## Task 12: Build the click command and interaction loop `commands.py`

Depends on: Task 1, Task 7, Task 9, Task 10, Task 11

Create `src/superclaude/cli/observe/commands.py` and `tests/observe/test_commands.py`, following `ARCHITECTURE-SPINE.md` AD-1, AD-2 (command body only, not the registration), AD-14, AD-17 and AD-20, and `rendering-rules.md` section "Keys". Define the click group `observe_group` with one default behaviour and options `--once`, `--width <160|116|80>`, `--ascii`, `--fixture <variant>`, `--run <runId>` and `--snapshot PATH`. Fixture mode (`--fixture`) builds a `FixtureSource` and shows `SYNTHETIC FIXTURE <variant>, not Orca data`; otherwise live mode builds the production `LiveSource` (production runner, `_find_orca` discovery). `--once` runs one synchronous cycle, writes `record_text` to stdout encoded with `terminal.output_encoding()` and `errors="replace"` (no raw mode needed on any platform), and with `--width` prints the width-bound screen text instead through a recorded console. Interactive mode requires a POSIX terminal: elsewhere it prints `interactive mode needs a POSIX terminal; use --once` and exits non-zero without importing `keys.py`; on POSIX it imports `keys.py` lazily, runs `Live(screen=True)` with a console from `make_console`, redraws on a new `CycleResult` or a key, applies `apply_cycle` and `apply_key`, performs `EXPORT` by writing a timestamped text record under `state_dir()` and showing `exported <path>` or `export failed: <reason>`, and performs `QUIT`. In live mode the loop writes exactly one snapshot per published cycle, after failures as well as successes, to `--snapshot` or the default state directory; a render exception stops the screen, restores the terminal and exits non-zero. The help text states that caps are per observer process and several observers multiply the load on Orca. No code path builds a second argv or calls Orca outside `adapter.py`.

Acceptance criteria:
- [T12.AC1] `uv run pytest tests/observe/test_commands.py -v` passes.
- [T12.AC2] A test imports `commands.py` with `termios`, `tty` and `fcntl` blocked and `--once --fixture base` still prints a record with no ESC byte; on a simulated non-POSIX platform interactive mode prints the exact message and exits non-zero without importing `keys.py`.
- [T12.AC3] T36 (command half): `--once` in live mode with a fake runner and fake discovery only ever produces the allow-listed argv, and with `Discover` returning `None` prints `worker-list NOT AVAILABLE (no Orca CLI validated)` and not an empty fleet.
- [T12.AC4] A test runs `--once --fixture base --width 80` and `--width 116` and `--width 160` and asserts every line has `cell_len <= width` and the gap notice is present.
- [T12.AC5] A test runs the interaction loop with a scripted key source and fake collector: `j`, `/`, text, Enter, `h`, `m`, `e` and `q` change session state as in Task 9, `e` writes one file under a temporary `XDG_STATE_HOME`, and `q` ends the loop and restores the terminal state.
- [T12.AC6] A test shows live mode with `--snapshot <tmp>` writes one snapshot per published cycle including a failed one, validated against `snapshot.schema.json`, and that fixture mode writes none without `--snapshot`.
- [T12.AC7] A source scan test asserts no module in the package other than `adapter.py` imports `subprocess`.

Global constraints: 
## Constraints

- Shorthand used in the tasks below. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`; it holds the canonical contract: `SPEC.md` and its companions `ARCHITECTURE-SPINE.md` (decisions AD-1 to AD-20 and conditional decisions CD-1 to CD-16), `adapter-contract.md`, `rendering-rules.md`, `acceptance-tests.md` (tests T1 to T51), `release-gates.md`, `snapshot-export-schema.md` and `unverified-register.md`. SNAPSRC is `.dev/issues/409/tuibbs-review/architecture-options.md` (last section, the frozen snapshot fields). The package is `src/superclaude/cli/observe/` and its tests are `tests/observe/`. Where SPECDIR and the older `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md` differ, SPECDIR wins.
- Scope is release 1 (R1: live `worker-list`, COUNTS and freshness strips, worker ledger with the verbatim `projection.nextAction.kind` column, capped paging, STALE after 45 s, changes since last look, the one-line question-source notice, the JSON snapshot) plus the offline R0 pieces R1 needs (key-reader spike, sanitizer, cell-width truncation, NO_COLOR and ASCII, fixture variants, text export, fixture mode). The owner chose the staged direction and confirmed Python + Rich with snapshot export in `.dev/issues/409/owner-decisions-20261108.md` (items 1 and 5), so the side-by-side R0 renders of the Attention Ledger and Decision Desk that were only input to that choice are not built.
- Out of scope, not built even as stubs: question rows and any `check`, `inbox` or message read (R2), the SEEN IS NOT RESOLVED and RETAIN CONTEXT panels, the Decision Desk (R3), `--include-remote` (R4), every write path into Orca (approve, retry, terminate, spawn, merge, reply, instruct), persisting the last-look baseline, the `read k of N Runs since start` header token and its collector counters (CD-10 default places it in the Attention Ledger header only), any Go or TUIBBS code, and moving `_find_orca()`.
- Acceptance tests not built because they serve only the excluded views: T7, T10, T17, T19, T45, T46, T50 and T51, and the question half of T12 and T47. Every other test in `acceptance-tests.md` that applies to the ledger view is mapped to a task below, plus the snapshot schema test (no ID assigned in the spec).
- Authorization evidence. The owner's message of 2026-11-11, "Proceed with building the first release", is taken as the go for R0 and R1, including registering `superclaude observe` (reading 1 of "production integration" in `release-gates.md`) and live read-only `worker-list` calls. Caveat: `release-gates.md` says the owner's own dated selection record (check AC-S) states the confirmed reading and the direction. No task here writes that record, and it stays a reviewer-checked item. The final report must say it was not seen.
- Live Orca calls. Only two kinds are ever made, both read-only, both through `adapter.py`: `worker-list --json --limit 100` polling (optional `--run <runId>`, optional `--cursor <value>`, no shell) and the one startup discovery through `_find_orca()` in `src/superclaude/cli/install_user_setup.py` (runs `skills list --json`, at most two candidates, 10 s each, once per process, outside the 15 s cycle budget and the 5-call cap). No key maps to an Orca call. The forbidden set (plain `check`, `--ack`, `--wait`, `--retry-request`, `dispatch`, `inbox`, any other verb) is checked before every call and is never shortened.
- Defaults taken for open owner questions (SPECDIR `ARCHITECTURE-SPINE.md` CD table), changeable by the owner: CD-2 change flags use `stage.worker`, `stage.dispatch`, `nextAction.kind`, `liveness.verdict` and `stage.detail` and `stage.activity` stay inspector-only; CD-3 snapshot rows use timestamp order; CD-4 only the spec-fixed height rules; CD-5 truncation glyph `>`; CD-6 `--once` prints the record text to stdout, `--snapshot PATH` sets the snapshot file, the default directory is `~/.local/state/superclaude/observe/`, files are 0600 and replaced atomically; CD-8 empty palette (plain text, meaning in words); CD-16 a ledger row does not name a shared `worktreeId`.
- Plan-author rules that close gaps in the spec (PROPOSED, the owner may change them). The state directory honours `XDG_STATE_HOME` when set so tests stay out of the real home folder. `--once` with a live source writes a snapshot only when `--snapshot` is given. Fixture mode (`--fixture <variant>`) never calls Orca and never writes a snapshot unless `--snapshot` is given. A failed key-reader spike blocks the interactive tasks and is reported to the owner; the Textual switch in AD-14 is applied only on the owner's say-so, and both toolkits are never built.
- Data handling. Raw Orca output is never logged, committed, or kept in fixtures; committed fixtures hold only redacted identifiers (no absolute path, terminal handle, token or credential). Worker free text (`stage.detail`, `stage.activity`) and failed-poll stderr are shown after control-character sanitizing, labelled `worker-reported`; they are not redacted and no credential or terminal-handle field is exported.
- No code is copied from TUIBBS-scp (AGPL-3.0); the design prototype `canvas.py` is never imported. Python 3.10 compatible, no new dependency (`rich`, `click`, `jsonschema` and `pexpect` are already dependencies in `pyproject.toml`), UV only (`uv run pytest tests/observe -v`, `uv run ruff check src/superclaude/cli/observe tests/observe`), and nothing is written under `.claude/`. Every task leaves ruff clean for the files it touches.
- A fact the source does not give is the single `UNKNOWN` sentinel (never `None`, `0`, `False`, `""`) and renders as the word `unknown`. Facts with no verified source render `unavailable (no source)`. Worker text always renders as literal text, never parsed as Rich markup.

Start sha: 070b5c110c47c9b4b6c478c2cdfd97ded5908394
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/commands.py b/src/superclaude/cli/observe/commands.py
new file mode 100644
index 000000000..ccb220b7a
--- /dev/null
+++ b/src/superclaude/cli/observe/commands.py
@@ -0,0 +1,421 @@
+"""``superclaude observe``: the click command and the interaction loop (AD-1, AD-14, AD-17, AD-20).
+
+Read-only. The only Orca calls are the ones ``adapter.py`` makes; no key and no option here
+builds an argv or calls Orca. ``keys.py`` (POSIX only) is imported lazily inside the
+interactive branch, so ``--once`` works on every platform.
+"""
+
+from __future__ import annotations
+
+import io
+import os
+import sys
+import time
+from dataclasses import dataclass, field
+from datetime import datetime
+from pathlib import Path
+from typing import Any, Callable
+
+import click
+from rich.live import Live
+
+from superclaude.cli.observe.adapter import (
+    ArgvRejected,
+    LiveSource,
+    check_run_id,
+    production_runner,
+)
+from superclaude.cli.observe.collector import Collector, FixtureSource
+from superclaude.cli.observe.export import (
+    record_path,
+    record_text,
+    snapshot_json,
+    snapshot_path,
+    state_dir,
+    write_atomic,
+)
+from superclaude.cli.observe.parse import load_fixture
+from superclaude.cli.observe.render import render
+from superclaude.cli.observe.terminal import (
+    detect_size,
+    make_console,
+    output_encoding,
+    resolve_policy,
+)
+from superclaude.cli.observe.view import (
+    Effect,
+    Session,
+    apply_cycle,
+    apply_key,
+    build_view,
+)
+
+POSIX_ONLY_TEXT = (
+    "interactive mode needs a POSIX terminal; use --once"  # PROPOSED wording
+)
+NO_TERMINAL_TEXT = "interactive mode needs a terminal on standard input; use --once"
+READ_TIMEOUT = 0.1  # seconds a key read may wait; the loop redraws between reads
+REDRAW_SECONDS = (
+    0.5  # ages and STALE move with time, so the screen repaints at least this often
+)
+WIDTHS = ("160", "116", "80")
+
+HELP = """Read-only terminal observer for Orca workers.
+
+Shows the worker ledger Orca reports for its workers (verbatim next-action kind,
+freshness, collected / reported counts) and can write a plain-text record and a versioned JSON
+snapshot. It never writes to Orca: no key and no option maps to an Orca call.
+
+Poll caps (one read every 15 s, at most 5 calls per read) are per observer process; several
+observers running at once multiply the load on Orca.
+"""
+
+
+# -- the real clock ------------------------------------------------------------------------------
+
+
+class SystemClock:
+    """The injected clock the rest of the package reads: monotonic, wall and local time zone."""
+
+    def monotonic(self) -> float:
+        return time.monotonic()
+
+    def wall(self) -> float:
+        return time.time()
+
+    def local_tz(self) -> Any:
+        return datetime.now().astimezone().tzinfo
+
+
+# -- options and dependencies ------------------------------------------------------------------------
+
+
+@dataclass(frozen=True)
+class Options:
+    once: bool = False
+    width: int | None = None
+    ascii: bool = False
+    fixture: str | None = None
+    run_id: str | None = None
+    snapshot: str | None = None
+
+
+@dataclass
+class Deps:
+    """Everything outside the package, replaceable in tests. ``None`` means the real thing."""
+
+    runner: Callable | None = None
+    discover: Callable | None = None
+    clock: Any = None
+    env: Any = None
+    encoding: str | None = None
+    size: Callable[[], tuple[int, int]] | None = None
+    platform: str | None = None
+    key_source: Any = None
+    screen_factory: Callable[[], Any] | None = None
+    state_directory: Path | None = None
+    stdout: Any = None
+    interval: float | None = None
+    extra: dict = field(default_factory=dict)
+
+
+def _policy_maker(options: Options, deps: Deps) -> Callable[[], Any]:
+    env = os.environ if deps.env is None else deps.env
+    encoding = deps.encoding if deps.encoding is not None else output_encoding()
+    size = deps.size or detect_size
+
+    def make() -> Any:
+        columns, rows = size()
+        return resolve_policy(
+            env, encoding, {"ascii": options.ascii}, options.width or columns, rows
+        )
+
+    return make
+
+
+def _build_source(options: Options, deps: Deps) -> Any:
+    if options.fixture:
+        return FixtureSource(options.fixture)
+    kwargs: dict[str, Any] = {}
+    if deps.discover is not None:
+        kwargs["discover"] = deps.discover
+    return LiveSource(deps.runner or production_runner, **kwargs)
+
+
+def _emit(text: str, deps: Deps) -> None:
+    if deps.stdout is not None:
+        deps.stdout.write(text)
+        return
+    encoding = deps.encoding if deps.encoding is not None else output_encoding()
+    buffer = getattr(sys.stdout, "buffer", None)
+    if buffer is None:
+        sys.stdout.write(text)
+        return
+    buffer.write(text.encode(encoding, errors="replace"))
+    buffer.flush()
+
+
+def _write_snapshot(view: Any, target: Path) -> str | None:
+    """One snapshot file, replaced atomically; the error text when it could not be written."""
+    try:
+        write_atomic(target, snapshot_json(view))
+    except OSError as exc:
+        return f"snapshot failed: {exc}"
+    return None
+
+
+# -- --once ----------------------------------------------------------------------------------------------
+
+
+def run_once(options: Options, deps: Deps) -> int:
+    clock = deps.clock or SystemClock()
+    source = _build_source(options, deps)
+    collector = Collector(source, clock, run_id=options.run_id)
+    result = collector.run_once()
+    session = apply_cycle(Session(), result, clock)
+    view = build_view(result, session, clock)
+    if options.width is not None:  # the width-bound screen, through a recorded console
+        policy = _policy_maker(options, deps)()
+        console = make_console(policy, file=io.StringIO(), record=True)
+        console.print(render(view, policy))
+        text = console.export_text()
+    else:
+        text = record_text(view)
+    _emit(text, deps)
+    if options.snapshot:
+        failure = _write_snapshot(view, Path(options.snapshot))
+        if failure:
+            click.echo(failure, err=True)
+            return 1
+    return 0
+
+
+# -- the interaction loop -------------------------------------------------------------------------------------
+
+
+class LiveScreen:
+    """The real screen: ``Live(screen=True)`` over a console made by ``make_console``."""
+
+    def __init__(self) -> None:
+        self._live: Live | None = None
+        self._shape: tuple | None = None
+
+    def draw(self, view: Any, policy: Any, message: str | None) -> None:
+        shape = (policy.width, policy.height, policy.ascii, policy.no_color)
+        group = render(view, policy, message)
+        if self._live is None or shape != self._shape:
+            self.close()
+            self._live = Live(
+                group, console=make_console(policy), screen=True, auto_refresh=False
+            )
+            self._live.start()
+            self._shape = shape
+        self._live.update(group, refresh=True)
+
+    def close(self) -> None:
+        if self._live is not None:
+            self._live.stop()
+            self._live = None
+
+
+def run_loop(
+    collector: Any,
+    keys: Any,
+    screen: Any,
+    clock: Any,
+    *,
+    make_policy: Callable[[], Any],
+    directory: Path,
+    snapshot_file: Path,
+    write_snapshots: bool,
+) -> int:
+    """Poll, read keys, redraw. Keys change the session only; ``q`` or Ctrl-C ends it."""
+    session = Session()
+    seen = -1
+    written = 0
+    message: str | None = None
+    last_draw: float | None = None
+    collector.start()
+    try:
+        while True:
+            result = collector.latest()
+            dirty = False
+            if result.cycle != seen:
+                session = apply_cycle(session, result, clock)
+                seen = result.cycle
+                dirty = True
+                if write_snapshots and result.cycle > written:
+                    written = (
+                        result.cycle
+                    )  # exactly one write per cycle, after failures too
+                    failure = _write_snapshot(
+                        build_view(result, session, clock), snapshot_file
+                    )
+                    message = failure or message
+            view = build_view(result, session, clock)
+            key = keys.read(READ_TIMEOUT)
+            if key is not None:
+                session, effect = apply_key(session, key, view, clock)
+                message = None
+                dirty = True
+                if effect is Effect.QUIT:
+                    return 0
+                if effect is Effect.EXPORT:
+                    target = record_path(directory, view)
+                    try:
+                        write_atomic(target, record_text(view))
+                        message = f"exported {target}"
+                    except OSError as exc:
+                        message = f"export failed: {exc}"
+                view = build_view(result, session, clock)
+            if keys.consume_redraw():
+                dirty = True
+            now = clock.monotonic()
+            if dirty or last_draw is None or now - last_draw >= REDRAW_SECONDS:
+                screen.draw(view, make_policy(), message)
+                last_draw = now
+    except KeyboardInterrupt:
+        return 0
+    except (
+        Exception
+    ) as exc:  # a render failure stops the screen; it never retries silently
+        screen.close()
+        click.echo(f"observe: display failed: {exc}", err=True)
+        return 1
+    finally:
+        collector.stop()
+        screen.close()
+
+
+def run_interactive(options: Options, deps: Deps) -> int:
+    platform = deps.platform if deps.platform is not None else sys.platform
+    if platform == "win32":
+        click.echo(POSIX_ONLY_TEXT)
+        return 2
+    from superclaude.cli.observe.keys import KeySource  # lazy: POSIX only
+
+    clock = deps.clock or SystemClock()
+    keys = deps.key_source or KeySource()
+    with keys:
+        if not keys.available:
+            click.echo(NO_TERMINAL_TEXT)
+            return 2
+        collector = Collector(
+            _build_source(options, deps),
+            clock,
+            interval=deps.interval if deps.interval is not None else 15.0,
+            run_id=options.run_id,
+        )
+        directory = deps.state_directory or state_dir()
+        live = not options.fixture
+        return run_loop(
+            collector,
+            keys,
+            (deps.screen_factory or LiveScreen)(),
+            clock,
+            make_policy=_policy_maker(options, deps),
+            directory=directory,
+            snapshot_file=Path(options.snapshot)
+            if options.snapshot
+            else snapshot_path(directory),
+            write_snapshots=live or bool(options.snapshot),
+        )
+
+
+def execute(options: Options, deps: Deps | None = None) -> int:
+    """Run the command; returns the process exit code."""
+    deps = deps or Deps()
+    if options.once:
+        return run_once(options, deps)
+    return run_interactive(options, deps)
+
+
+# -- click ------------------------------------------------------------------------------------------------------
+
+
+def _check_fixture(
+    ctx: click.Context, param: click.Parameter, value: str | None
+) -> str | None:
+    if value is not None:
+        try:
+            load_fixture(value)
+        except ValueError as exc:
+            raise click.BadParameter(str(exc)) from exc
+    return value
+
+
+def _check_run(
+    ctx: click.Context, param: click.Parameter, value: str | None
+) -> str | None:
+    if value is not None:
+        try:
+            check_run_id(value)
+        except ArgvRejected as exc:
+            raise click.BadParameter(str(exc)) from exc
+    return value
+
+
+@click.group(name="observe", invoke_without_command=True, help=HELP)
+@click.option(
+    "--once",
+    is_flag=True,
+    help="Read once, print the plain-text record to stdout and exit.",
+)
+@click.option(
+    "--width",
+    type=click.Choice(WIDTHS),
+    default=None,
+    help="Bind the output to 160, 116 or 80 columns; with --once prints the screen text instead of the record.",
+)
+@click.option(
+    "--ascii",
+    "ascii_mode",
+    is_flag=True,
+    help="Use ASCII only (also chosen for a non-UTF-8 terminal).",
+)
+@click.option(
+    "--fixture",
+    default=None,
+    callback=_check_fixture,
+    help="Replay a synthetic fixture variant instead of calling Orca (for example base).",
+)
+@click.option(
+    "--run",
+    "run_id",
+    default=None,
+    callback=_check_run,
+    help="Read one Run only (an Orca run id).",
+)
+@click.option(
+    "--snapshot",
+    "snapshot",
+    type=click.Path(dir_okay=False),
+    default=None,
+    help="Write the JSON snapshot to this file (default for live mode: the per-user state directory).",
+)
+@click.pass_context
+def observe_group(
+    ctx: click.Context,
+    once: bool,
+    width: str | None,
+    ascii_mode: bool,
+    fixture: str | None,
+    run_id: str | None,
+    snapshot: str | None,
+) -> None:
+    if ctx.invoked_subcommand is not None:
+        return
+    options = Options(
+        once=once,
+        width=int(width) if width else None,
+        ascii=ascii_mode,
+        fixture=fixture,
+        run_id=run_id,
+        snapshot=snapshot,
+    )
+    code = execute(options)
+    if code:
+        ctx.exit(code)
+
+
+__all__ = ["Deps", "Options", "SystemClock", "execute", "observe_group", "run_loop"]
diff --git a/src/superclaude/cli/observe/render.py b/src/superclaude/cli/observe/render.py
index 95fe694a5..f2c2182aa 100644
--- a/src/superclaude/cli/observe/render.py
+++ b/src/superclaude/cli/observe/render.py
@@ -269,8 +269,13 @@ def _notes(view: View) -> list[str]:
     return ["  ".join(parts)] if parts else []
 
 
-def screen_lines(view: View, policy: TerminalPolicy) -> list[str]:
-    """The screen as plain lines, each at most ``policy.width`` cells wide."""
+def screen_lines(
+    view: View, policy: TerminalPolicy, message: str | None = None
+) -> list[str]:
+    """The screen as plain lines, each at most ``policy.width`` cells wide.
+
+    ``message`` is a one-off notice from the command loop (an export result); it sits above the footer.
+    """
     width = policy.width
     if (
         policy.too_narrow
@@ -294,6 +299,8 @@ def screen_lines(view: View, policy: TerminalPolicy) -> list[str]:
         top += wrap(note, width, policy)
     if view.focus == "filter":
         top += wrap("/" + view.filter_text, width, policy)
+    if message:
+        top += wrap(message, width, policy)
 
     # The footer is one line when it fits, else the key list and the counts on two lines.
     window_probe = view.window(None)
@@ -338,11 +345,11 @@ def screen_lines(view: View, policy: TerminalPolicy) -> list[str]:
     return top + body + footer_lines
 
 
-def render(view: View, policy: TerminalPolicy) -> Group:
+def render(view: View, policy: TerminalPolicy, message: str | None = None) -> Group:
     """The screen as Rich renderables: one plain ``Text`` per line, never reflowed."""
     return Group(
         *(
             Text(line, no_wrap=True, overflow="crop")
-            for line in screen_lines(view, policy)
+            for line in screen_lines(view, policy, message)
         )
     )
diff --git a/tests/observe/test_commands.py b/tests/observe/test_commands.py
new file mode 100644
index 000000000..1eb9fd0df
--- /dev/null
+++ b/tests/observe/test_commands.py
@@ -0,0 +1,594 @@
+"""Command and interaction-loop tests (AD-1, AD-2 command body, AD-14, AD-17, AD-20; T36 command half)."""
+# ruff: noqa: E741  (``l`` is an output line in the comprehensions below)
+
+from __future__ import annotations
+
+import io
+import json
+import re
+import subprocess
+import sys
+import threading
+import time
+from pathlib import Path
+
+import pytest
+from click.testing import CliRunner
+from jsonschema import Draft7Validator
+from rich.cells import cell_len
+
+import superclaude.cli.observe as observe_pkg
+import superclaude.cli.observe.commands as commands
+from superclaude.cli.observe.adapter import LiveSource
+from superclaude.cli.observe.collector import Collector, FixtureSource
+from superclaude.cli.observe.commands import (
+    NO_TERMINAL_TEXT,
+    POSIX_ONLY_TEXT,
+    Deps,
+    Options,
+    SystemClock,
+    execute,
+    observe_group,
+    run_loop,
+)
+from superclaude.cli.observe.export import SCHEMA
+from superclaude.cli.observe.view import GAP_NOTICE, Key
+from tests.observe.conftest import FakeDiscover, FakeRunner, make_envelope, make_rows
+
+VALIDATOR = Draft7Validator(SCHEMA)
+KEYS_MODULE = "superclaude.cli.observe.keys"
+
+
+def reply(n=3):
+    return 0, json.dumps(make_envelope(make_rows(n, 1), total=n))
+
+
+def deps_for(clock, **kw):
+    base = {
+        "clock": clock,
+        "size": lambda: (160, 40),
+        "encoding": "utf-8",
+        "env": {},
+        "stdout": io.StringIO(),
+    }
+    base.update(kw)
+    return Deps(**base)
+
+
+def once(options, deps):
+    code = execute(options, deps)
+    return code, deps.stdout.getvalue()
+
+
+# -- --once: no raw mode, every platform ----------------------------------------------------------------
+
+
+@pytest.mark.observe_real_process
+def test_once_works_with_termios_tty_and_fcntl_blocked_and_never_imports_keys():
+    code = (
+        "import sys\n"
+        # The rest of the CLI (pexpect, pty) legitimately uses these modules, so load it first,
+        # then forget the observer and import it again with them blocked.
+        "import superclaude.cli\n"
+        "for name in [m for m in sys.modules if m.startswith('superclaude.cli.observe')]:\n"
+        "    del sys.modules[name]\n"
+        "for name in ('termios', 'tty', 'fcntl'):\n"
+        "    sys.modules[name] = None\n"
+        "from click.testing import CliRunner\n"
+        "from superclaude.cli.observe.commands import observe_group\n"
+        "r = CliRunner().invoke(observe_group, ['--once', '--fixture', 'base'])\n"
+        f"sys.stdout.write('KEYS=%s\\n' % ('{KEYS_MODULE}' in sys.modules))\n"
+        "sys.stdout.write('EXIT=%d\\n' % r.exit_code)\n"
+        "sys.stdout.write(r.output)\n"
+    )
+    done = subprocess.run(
+        [sys.executable, "-I", "-c", code], capture_output=True, text=True, timeout=120
+    )
+    assert done.returncode == 0, done.stderr
+    lines = done.stdout.splitlines()
+    assert lines[0] == "KEYS=False" and lines[1] == "EXIT=0"
+    assert (
+        lines[2].startswith("ORCA OBSERVER")
+        and "SYNTHETIC FIXTURE base, not Orca data" in lines[2]
+    )
+    assert "\x1b" not in done.stdout and any(l.startswith("dispatchId=") for l in lines)
+
+
+def test_once_fixture_prints_the_record_through_click_with_no_escape_byte():
+    result = CliRunner().invoke(observe_group, ["--once", "--fixture", "base"])
+    assert result.exit_code == 0
+    assert "\x1b" not in result.output
+    assert "SYNTHETIC FIXTURE base, not Orca data" in result.output.splitlines()[0]
+    assert (
+        len([l for l in result.output.splitlines() if l.startswith("dispatchId=")])
+        == 80
+    )
+
+
+@pytest.mark.parametrize("width", [160, 116, 80])
+def test_once_with_width_prints_the_bound_screen_with_the_gap_notice(fake_clock, width):
+    code, out = once(
+        Options(once=True, fixture="base", width=width),
+        deps_for(fake_clock, size=lambda: (200, 40)),
+    )
+    lines = out.splitlines()
+    assert code == 0 and lines and all(cell_len(l) <= width for l in lines)
+    assert GAP_NOTICE in lines and "\x1b" not in out
+    assert any("collected 80 / reported 80" in l for l in lines)
+    via_click = CliRunner().invoke(
+        observe_group, ["--once", "--fixture", "base", "--width", str(width)]
+    )
+    assert via_click.exit_code == 0 and all(
+        cell_len(l) <= width for l in via_click.output.splitlines()
+    )
+
+
+def test_once_ascii_flag_gives_ascii_only_output(fake_clock):
+    code, out = once(
+        Options(once=True, fixture="long-identifiers", width=80, ascii=True),
+        deps_for(fake_clock),
+    )
+    assert code == 0 and out.isascii()
+
+
+# -- T36, command half ------------------------------------------------------------------------------------------
+
+
+def test_live_once_only_ever_produces_allow_listed_argv(fake_clock, argv_log):
+    runner = FakeRunner(argv_log, [reply(3)])
+    deps = deps_for(fake_clock, runner=runner, discover=FakeDiscover(argv_log))
+    code, out = once(Options(once=True), deps)
+    assert code == 0 and "mode=live" in out.splitlines()[0]
+    assert len([l for l in out.splitlines() if l.startswith("dispatchId=")]) == 3
+    assert argv_log[0][1:] == ["skills", "list", "--json"]
+    assert [a[1:6] for a in argv_log[1:]] == [
+        ["orchestration", "worker-list", "--json", "--limit", "100"]
+    ]
+    deps = deps_for(fake_clock, runner=runner, discover=FakeDiscover(argv_log))
+    once(Options(once=True, run_id="run-a"), deps)
+    assert argv_log[-1][-2:] == ["--run", "run-a"]
+
+
+def test_no_validated_orca_prints_not_available_and_not_an_empty_fleet(
+    fake_clock, argv_log
+):
+    runner = FakeRunner(argv_log, [reply(3)])
+    deps = deps_for(fake_clock, runner=runner, discover=FakeDiscover(argv_log, None))
+    code, out = once(Options(once=True), deps)
+    assert code == 0 and "worker-list NOT AVAILABLE (no Orca CLI validated)" in out
+    assert runner.calls == 0 and "no successful worker-list read yet" in out
+    assert not any(l.startswith("dispatchId=") for l in out.splitlines())
+    assert "0 workers" not in out and "not proof none exist" not in out
+
+
+# -- snapshot files ----------------------------------------------------------------------------------------------
+
+
+def test_once_writes_a_snapshot_only_when_asked(fake_clock, argv_log, tmp_path):
+    target = tmp_path / "snap.json"
+    code, _ = once(
+        Options(once=True, fixture="base", snapshot=str(target)), deps_for(fake_clock)
+    )
+    assert (
+        code == 0 and list(VALIDATOR.iter_errors(json.loads(target.read_text()))) == []
+    )
+    live_dir = tmp_path / "state"
+    runner = FakeRunner(argv_log, [reply(2)])
+    once(
+        Options(once=True),
+        deps_for(
+            fake_clock,
+            runner=runner,
+            discover=FakeDiscover(argv_log),
+            state_directory=live_dir,
+        ),
+    )
+    once(
+        Options(once=True, fixture="empty"),
+        deps_for(fake_clock, state_directory=live_dir),
+    )
+    assert (
+        not live_dir.exists()
+        and [p.name for p in tmp_path.iterdir() if p.name != "snap.json"] == []
+    )
+
+
+def test_an_unwritable_snapshot_path_exits_non_zero_with_a_message(
+    fake_clock, tmp_path, capsys
+):
+    code, _ = once(
+        Options(once=True, fixture="base", snapshot=str(tmp_path)), deps_for(fake_clock)
+    )
+    assert code == 1 and "snapshot failed" in capsys.readouterr().err
+
+
+# -- click wiring ---------------------------------------------------------------------------------------------------
+
+
+def test_help_lists_every_option_and_the_per_process_cap_warning():
+    out = CliRunner().invoke(observe_group, ["--help"]).output
+    for option in ("--once", "--width", "--ascii", "--fixture", "--run", "--snapshot"):
+        assert option in out
+    flat = " ".join(out.split())
+    assert "per observer process" in flat and "multiply the load on Orca" in flat
+    assert "read-only" in flat.lower() or "never writes to Orca" in flat
+
+
+@pytest.mark.parametrize(
+    "args",
+    [
+        ["--once", "--fixture", "nope"],
+        ["--once", "--run", "-x"],
+        ["--once", "--run", "bad id"],
+        ["--once", "--width", "100"],
+    ],
+)
+def test_bad_option_values_are_rejected_before_anything_runs(args):
+    result = CliRunner().invoke(observe_group, args)
+    assert result.exit_code == 2 and "Traceback" not in result.output
+
+
+# -- interactive mode -----------------------------------------------------------------------------------------------------
+
+
+def test_interactive_mode_on_a_non_posix_platform_prints_the_message_and_never_imports_keys(
+    fake_clock, capsys, monkeypatch
+):
+    monkeypatch.delitem(sys.modules, KEYS_MODULE, raising=False)
+    code = execute(Options(), Deps(platform="win32", clock=fake_clock))
+    assert code != 0 and capsys.readouterr().out == POSIX_ONLY_TEXT + "\n"
+    assert POSIX_ONLY_TEXT == "interactive mode needs a POSIX terminal; use --once"
+    assert KEYS_MODULE not in sys.modules
+    monkeypatch.setattr(sys, "platform", "win32")
+    result = CliRunner().invoke(observe_group, [])
+    assert (
+        result.exit_code != 0
+        and POSIX_ONLY_TEXT in result.output
+        and KEYS_MODULE not in sys.modules
+    )
+
+
+class ScriptedKeys:
+    """A key source that releases its script once ``gate`` is true, then quits."""
+
+    def __init__(self, keys, gate=lambda: True, available=True, raise_on_read=None):
+        self.keys = list(keys)
+        self.gate = gate
+        self.available = available
+        self.entered = self.exited = False
+        self.raise_on_read = raise_on_read
+
+    def __enter__(self):
+        self.entered = True
+        return self
+
+    def __exit__(self, *exc):
+        self.exited = True
+
+    def read(self, timeout):
+        if self.raise_on_read:
+            raise self.raise_on_read
+        if not self.gate():
+            time.sleep(0.002)
+            return None
+        return self.keys.pop(0) if self.keys else Key("text", "q")
+
+    def consume_redraw(self):
+        return False
+
+
+class FakeScreen:
+    def __init__(self, fail=False):
+        self.frames: list[tuple] = []
+        self.closed = 0
+        self.fail = fail
+
+    def draw(self, view, policy, message):
+        if self.fail:
+            raise RuntimeError("boom")
+        self.frames.append((view, message, policy))
+
+    def close(self):
+        self.closed += 1
+
+
+def text_key(char):
+    return Key("text", char)
+
+
+def live_threads():
+    return [t for t in threading.enumerate() if t.name == "observe-collector"]
+
+
+def test_scripted_keys_drive_the_session_and_q_restores_the_terminal(
+    fake_clock, tmp_path
+):
+    collector = Collector(FixtureSource("base"), fake_clock, interval=0.005)
+    keys = ScriptedKeys(
+        [
+            text_key("j"),
+            text_key("/"),
+            text_key("w"),
+            text_key("-"),
+            text_key("0"),
+            Key("enter"),
+            text_key("h"),
+            text_key("m"),
+            text_key("e"),
+            text_key("q"),
+        ],
+        gate=lambda: collector.latest().cycle >= 1,
+    )
+    screen = FakeScreen()
+    with keys:
+        code = run_loop(
+            collector,
+            keys,
+            screen,
+            fake_clock,
+            make_policy=lambda: commands.resolve_policy({}, "utf-8", {}, 160, 40),
+            directory=tmp_path,
+            snapshot_file=tmp_path / "snap.json",
+            write_snapshots=False,
+        )
+    assert (
+        code == 0
+        and keys.entered
+        and keys.exited
+        and screen.closed >= 1
+        and live_threads() == []
+    )
+    views = [frame[0] for frame in screen.frames]
+    assert any(v.selected is not None and v.selected.selected for v in views)
+    assert any(v.focus == "filter" for v in views)
+    assert any(v.filter_line and v.filter_line.startswith("filter w-0") for v in views)
+    assert any(v.show_historical for v in views)
+    assert views[-1].changes_line.startswith("changed since")
+    exported = list(tmp_path.glob("observe-*.txt"))
+    assert len(exported) == 1 and exported[0].read_text().startswith("ORCA OBSERVER")
+    assert any(frame[1] == f"exported {exported[0]}" for frame in screen.frames)
+    assert not (tmp_path / "snap.json").exists()
+
+
+def test_a_failed_export_shows_a_message_and_the_loop_goes_on(fake_clock, tmp_path):
+    blocker = tmp_path / "not-a-directory"
+    blocker.write_text("x")
+    collector = Collector(FixtureSource("base"), fake_clock, interval=0.005)
+    keys = ScriptedKeys(
+        [text_key("e"), text_key("q")], gate=lambda: collector.latest().cycle >= 1
+    )
+    screen = FakeScreen()
+    code = run_loop(
+        collector,
+        keys,
+        screen,
+        fake_clock,
+        make_policy=lambda: commands.resolve_policy({}, "utf-8", {}, 160, 40),
+        directory=blocker / "sub",
+        snapshot_file=tmp_path / "s.json",
+        write_snapshots=False,
+    )
+    assert code == 0 and any(
+        (m or "").startswith("export failed:") for _, m, _ in screen.frames
+    )
+
+
+class FakeCollector:
+    """Publishes one prepared result per key read, so each cycle is seen exactly once."""
+
+    def __init__(self, results):
+        self.results = results
+        self.index = 0
+        self.started = self.stopped = False
+
+    def latest(self):
+        return self.results[self.index]
+
+    def start(self):
+        self.started = True
+
+    def stop(self):
+        self.stopped = True
+
+
+class AdvancingKeys(ScriptedKeys):
+    def __init__(self, collector):
+        super().__init__([])
+        self.collector = collector
+
+    def read(self, timeout):
+        if self.collector.index < len(self.collector.results) - 1:
+            self.collector.index += 1
+            return None
+        return Key("text", "q")
+
+
+def test_live_mode_writes_exactly_one_snapshot_per_published_cycle_including_a_failed_one(
+    fake_clock, argv_log, tmp_path, monkeypatch
+):
+    runner = FakeRunner(argv_log, [reply(3), (2, "", "boom"), reply(3)])
+    source = Collector(LiveSource(runner, FakeDiscover(argv_log)), fake_clock)
+    results = [source.latest(), source.run_once(), source.run_once(), source.run_once()]
+    assert [r.state for r in results] == ["NOT_POLLED", "OK", "FAILED", "OK"]
+    writes: list[tuple[Path, str]] = []
+    real = commands.write_atomic
+
+    def spy(path, text):
+        writes.append((path, text))
+        return real(path, text)
+
+    monkeypatch.setattr(commands, "write_atomic", spy)
+    collector = FakeCollector(results)
+    keys = AdvancingKeys(collector)
+    screen = FakeScreen()
+    target = tmp_path / "snapshot.json"
+    code = run_loop(
+        collector,
+        keys,
+        screen,
+        fake_clock,
+        make_policy=lambda: commands.resolve_policy({}, "utf-8", {}, 160, 40),
+        directory=tmp_path,
+        snapshot_file=target,
+        write_snapshots=True,
+    )
+    assert code == 0 and collector.started and collector.stopped
+    datas = [json.loads(text) for _, text in writes]
+    assert [d["cycle"] for d in datas] == [1, 2, 3] and {p for p, _ in writes} == {
+        target
+    }
+    assert [d["source"]["status"] for d in datas] == ["OK", "ERROR", "OK"]
+    assert (
+        datas[1]["source"]["error"] == "exit:2" and len(datas[1]["rows"]) == 3
+    )  # the last good rows
+    for data in datas:
+        assert list(VALIDATOR.iter_errors(data)) == []
+    assert json.loads(target.read_text())["cycle"] == 3
+
+
+def test_fixture_mode_writes_no_snapshot_unless_asked(fake_clock, tmp_path):
+    def interactive(options):
+        start = time.monotonic()
+        keys = ScriptedKeys([], gate=lambda: time.monotonic() - start > 0.15)
+        deps = Deps(
+            clock=fake_clock,
+            key_source=keys,
+            screen_factory=FakeScreen,
+            state_directory=tmp_path,
+            interval=0.005,
+            size=lambda: (160, 40),
+            encoding="utf-8",
+            env={},
+        )
+        return execute(options, deps)
+
+    assert interactive(Options(fixture="base")) == 0
+    assert list(tmp_path.glob("snapshot.json")) == []
+    asked = tmp_path / "asked.json"
+    assert interactive(Options(fixture="base", snapshot=str(asked))) == 0
+    assert list(VALIDATOR.iter_errors(json.loads(asked.read_text()))) == []
+    assert live_threads() == []
+
+
+def test_e_writes_one_record_under_a_temporary_xdg_state_home(
+    fake_clock, tmp_path, monkeypatch
+):
+    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
+    start = time.monotonic()
+    keys = ScriptedKeys(
+        [text_key("e"), text_key("q")], gate=lambda: time.monotonic() - start > 0.15
+    )
+    deps = Deps(  # no state_directory: the command resolves it through state_dir()
+        clock=fake_clock,
+        key_source=keys,
+        screen_factory=FakeScreen,
+        interval=0.005,
+        size=lambda: (160, 40),
+        encoding="utf-8",
+        env={},
+    )
+    assert execute(Options(fixture="base"), deps) == 0
+    records = list((tmp_path / "superclaude" / "observe").glob("observe-*.txt"))
+    assert len(records) == 1 and records[0].read_text().startswith("ORCA OBSERVER")
+    assert live_threads() == []
+
+
+def test_a_terminal_that_is_not_a_tty_is_reported_not_crashed(fake_clock, capsys):
+    keys = ScriptedKeys([], available=False)
+    code = execute(
+        Options(fixture="base"),
+        Deps(clock=fake_clock, key_source=keys, screen_factory=FakeScreen),
+    )
+    assert (
+        code == 2 and capsys.readouterr().out == NO_TERMINAL_TEXT + "\n" and keys.exited
+    )
+
+
+def test_a_render_exception_stops_the_screen_restores_the_terminal_and_exits_non_zero(
+    fake_clock, tmp_path, capsys
+):
+    collector = Collector(FixtureSource("base"), fake_clock, interval=0.005)
+    keys = ScriptedKeys(
+        [text_key("x")], gate=lambda: True
+    )  # a key read makes the loop draw
+    screen = FakeScreen(fail=True)
+    with keys:
+        code = run_loop(
+            collector,
+            keys,
+            screen,
+            fake_clock,
+            make_policy=lambda: commands.resolve_policy({}, "utf-8", {}, 160, 40),
+            directory=tmp_path,
+            snapshot_file=tmp_path / "s.json",
+            write_snapshots=False,
+        )
+    assert code == 1 and screen.closed >= 1 and keys.exited and live_threads() == []
+    assert "observe: display failed: boom" in capsys.readouterr().err
+
+
+def test_ctrl_c_during_a_read_quits_quietly_and_cleans_up(fake_clock, tmp_path):
+    collector = Collector(FixtureSource("base"), fake_clock, interval=0.005)
+    keys = ScriptedKeys([], raise_on_read=KeyboardInterrupt())
+    screen = FakeScreen()
+    code = run_loop(
+        collector,
+        keys,
+        screen,
+        fake_clock,
+        make_policy=lambda: commands.resolve_policy({}, "utf-8", {}, 160, 40),
+        directory=tmp_path,
+        snapshot_file=tmp_path / "s.json",
+        write_snapshots=False,
+    )
+    assert code == 0 and screen.closed >= 1 and live_threads() == []
+
+
+def test_the_screen_follows_the_terminal_size_on_every_redraw(fake_clock, tmp_path):
+    sizes = iter([(160, 40), (116, 30), (80, 24)] + [(80, 24)] * 100)
+    collector = Collector(FixtureSource("base"), fake_clock, interval=0.005)
+    keys = ScriptedKeys(
+        [text_key("j"), text_key("j")], gate=lambda: collector.latest().cycle >= 1
+    )
+    screen = FakeScreen()
+    run_loop(
+        collector,
+        keys,
+        screen,
+        fake_clock,
+        make_policy=lambda: commands.resolve_policy({}, "utf-8", {}, *next(sizes)),
+        directory=tmp_path,
+        snapshot_file=tmp_path / "s.json",
+        write_snapshots=False,
+    )
+    widths = [frame[2].width for frame in screen.frames]
+    assert widths[:3] == [160, 116, 80]
+
+
+# -- clock and module hygiene ----------------------------------------------------------------------------------------------------
+
+
+def test_system_clock_gives_monotonic_wall_and_a_time_zone():
+    clock = SystemClock()
+    first = clock.monotonic()
+    assert clock.monotonic() >= first and abs(clock.wall() - time.time()) < 5
+    assert clock.local_tz() is not None
+
+
+def test_no_module_other_than_the_adapter_imports_subprocess_and_none_names_an_orca_verb():
+    package = Path(observe_pkg.__file__).parent
+    offenders = []
+    for path in sorted(package.glob("*.py")):
+        text = path.read_text(encoding="utf-8")
+        if path.name != "adapter.py" and re.search(
+            r"^\s*(import subprocess|from subprocess\b)", text, re.M
+        ):
+            offenders.append(path.name)
+    assert offenders == []
+    commands_text = Path(commands.__file__).read_text(encoding="utf-8")
+    assert "worker-list" not in commands_text and "orchestration" not in commands_text
+    assert not re.search(
+        r"^from superclaude\.cli\.observe\.keys|^import superclaude\.cli\.observe\.keys",
+        commands_text,
+        re.M,
+    )

Delta diff from the previous reviewed tree (empty on the first review): 
diff --git a/tests/observe/test_commands.py b/tests/observe/test_commands.py
index 718fb2e3c..1eb9fd0df 100644
--- a/tests/observe/test_commands.py
+++ b/tests/observe/test_commands.py
@@ -470,6 +470,29 @@ def test_fixture_mode_writes_no_snapshot_unless_asked(fake_clock, tmp_path):
     assert live_threads() == []
 
 
+def test_e_writes_one_record_under_a_temporary_xdg_state_home(
+    fake_clock, tmp_path, monkeypatch
+):
+    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
+    start = time.monotonic()
+    keys = ScriptedKeys(
+        [text_key("e"), text_key("q")], gate=lambda: time.monotonic() - start > 0.15
+    )
+    deps = Deps(  # no state_directory: the command resolves it through state_dir()
+        clock=fake_clock,
+        key_source=keys,
+        screen_factory=FakeScreen,
+        interval=0.005,
+        size=lambda: (160, 40),
+        encoding="utf-8",
+        env={},
+    )
+    assert execute(Options(fixture="base"), deps) == 0
+    records = list((tmp_path / "superclaude" / "observe").glob("observe-*.txt"))
+    assert len(records) == 1 and records[0].read_text().startswith("ORCA OBSERVER")
+    assert live_threads() == []
+
+
 def test_a_terminal_that_is_not_a_tty_is_reported_not_crashed(fake_clock, capsys):
     keys = ScriptedKeys([], available=False)
     code = execute(

Earlier blocking findings of this start (empty on the first review): 
F1.1 sev=blocking trigger=B1 ac=T12.AC5 at=tests/observe/test_commands.py:303 anchor="`e` writes one file under a temporary `XDG_STATE_HOME`" chk=y,n,n,n family=ac5-xdg-not-exercised fix=add a test that sets XDG_STATE_HOME to a temporary folder with monkeypatch, runs execute with no state_directory and scripted e then q, and asserts one observe-*.txt under $XDG_STATE_HOME/superclaude/observe first=A1 origin=new: the scripted-key test passes directory=tmp_path straight to run_loop and no test sets XDG_STATE_HOME, so the state_dir() default is never exercised from the command
Saved-probe re-check hit locations (may be empty): tests/observe/test_commands.py:476

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
