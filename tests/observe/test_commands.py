"""Command and interaction-loop tests (AD-1, AD-2 command body, AD-14, AD-17, AD-20; T36 command half)."""
# ruff: noqa: E741  (``l`` is an output line in the comprehensions below)

from __future__ import annotations

import io
import json
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest
from click.testing import CliRunner
from jsonschema import Draft7Validator
from rich.cells import cell_len

import superclaude.cli.observe as observe_pkg
import superclaude.cli.observe.commands as commands
from superclaude.cli.observe.adapter import LiveSource
from superclaude.cli.observe.collector import Collector, FixtureSource
from superclaude.cli.observe.commands import (
    NO_TERMINAL_TEXT,
    POSIX_ONLY_TEXT,
    Deps,
    Options,
    SystemClock,
    execute,
    observe_group,
    run_loop,
)
from superclaude.cli.observe.export import SCHEMA
from superclaude.cli.observe.view import GAP_NOTICE, Key
from tests.observe.conftest import FakeDiscover, FakeRunner, make_envelope, make_rows

VALIDATOR = Draft7Validator(SCHEMA)
KEYS_MODULE = "superclaude.cli.observe.keys"


def reply(n=3):
    return 0, json.dumps(make_envelope(make_rows(n, 1), total=n))


def deps_for(clock, **kw):
    base = {
        "clock": clock,
        "size": lambda: (160, 40),
        "encoding": "utf-8",
        "env": {},
        "stdout": io.StringIO(),
    }
    base.update(kw)
    return Deps(**base)


def once(options, deps):
    code = execute(options, deps)
    return code, deps.stdout.getvalue()


# -- --once: no raw mode, every platform ----------------------------------------------------------------


@pytest.mark.observe_real_process
def test_once_works_with_termios_tty_and_fcntl_blocked_and_never_imports_keys():
    code = (
        "import sys\n"
        # The rest of the CLI (pexpect, pty) legitimately uses these modules, so load it first,
        # then forget the observer and import it again with them blocked.
        "import superclaude.cli\n"
        "for name in [m for m in sys.modules if m.startswith('superclaude.cli.observe')]:\n"
        "    del sys.modules[name]\n"
        "for name in ('termios', 'tty', 'fcntl'):\n"
        "    sys.modules[name] = None\n"
        "from click.testing import CliRunner\n"
        "from superclaude.cli.observe.commands import observe_group\n"
        "r = CliRunner().invoke(observe_group, ['--once', '--fixture', 'base'])\n"
        f"sys.stdout.write('KEYS=%s\\n' % ('{KEYS_MODULE}' in sys.modules))\n"
        "sys.stdout.write('EXIT=%d\\n' % r.exit_code)\n"
        "sys.stdout.write(r.output)\n"
    )
    done = subprocess.run(
        [sys.executable, "-I", "-c", code], capture_output=True, text=True, timeout=120
    )
    assert done.returncode == 0, done.stderr
    lines = done.stdout.splitlines()
    assert lines[0] == "KEYS=False" and lines[1] == "EXIT=0"
    assert (
        lines[2].startswith("ORCA OBSERVER")
        and "SYNTHETIC FIXTURE base, not Orca data" in lines[2]
    )
    assert "\x1b" not in done.stdout and any(l.startswith("dispatchId=") for l in lines)


def test_once_fixture_prints_the_record_through_click_with_no_escape_byte():
    result = CliRunner().invoke(observe_group, ["--once", "--fixture", "base"])
    assert result.exit_code == 0
    assert "\x1b" not in result.output
    assert "SYNTHETIC FIXTURE base, not Orca data" in result.output.splitlines()[0]
    assert (
        len([l for l in result.output.splitlines() if l.startswith("dispatchId=")])
        == 80
    )


@pytest.mark.parametrize("width", [160, 116, 80])
def test_once_with_width_prints_the_bound_screen_with_the_gap_notice(fake_clock, width):
    code, out = once(
        Options(once=True, fixture="base", width=width),
        deps_for(fake_clock, size=lambda: (200, 40)),
    )
    lines = out.splitlines()
    assert code == 0 and lines and all(cell_len(l) <= width for l in lines)
    assert GAP_NOTICE in lines and "\x1b" not in out
    assert any("collected 80 / reported 80" in l for l in lines)
    via_click = CliRunner().invoke(
        observe_group, ["--once", "--fixture", "base", "--width", str(width)]
    )
    assert via_click.exit_code == 0 and all(
        cell_len(l) <= width for l in via_click.output.splitlines()
    )


def test_once_ascii_flag_gives_ascii_only_output(fake_clock):
    code, out = once(
        Options(once=True, fixture="long-identifiers", width=80, ascii=True),
        deps_for(fake_clock),
    )
    assert code == 0 and out.isascii()


# -- T36, command half ------------------------------------------------------------------------------------------


def test_live_once_only_ever_produces_allow_listed_argv(fake_clock, argv_log):
    runner = FakeRunner(argv_log, [reply(3)])
    deps = deps_for(fake_clock, runner=runner, discover=FakeDiscover(argv_log))
    code, out = once(Options(once=True), deps)
    assert code == 0 and "mode=live" in out.splitlines()[0]
    assert len([l for l in out.splitlines() if l.startswith("dispatchId=")]) == 3
    assert argv_log[0][1:] == ["skills", "list", "--json"]
    assert [a[1:6] for a in argv_log[1:]] == [
        ["orchestration", "worker-list", "--json", "--limit", "100"]
    ]
    deps = deps_for(fake_clock, runner=runner, discover=FakeDiscover(argv_log))
    once(Options(once=True, run_id="run-a"), deps)
    assert argv_log[-1][-2:] == ["--run", "run-a"]


def test_no_validated_orca_prints_not_available_and_not_an_empty_fleet(
    fake_clock, argv_log
):
    runner = FakeRunner(argv_log, [reply(3)])
    deps = deps_for(fake_clock, runner=runner, discover=FakeDiscover(argv_log, None))
    code, out = once(Options(once=True), deps)
    assert code == 0 and "worker-list NOT AVAILABLE (no Orca CLI validated)" in out
    assert runner.calls == 0 and "no successful worker-list read yet" in out
    assert not any(l.startswith("dispatchId=") for l in out.splitlines())
    assert "0 workers" not in out and "not proof none exist" not in out


# -- snapshot files ----------------------------------------------------------------------------------------------


def test_once_writes_a_snapshot_only_when_asked(fake_clock, argv_log, tmp_path):
    target = tmp_path / "snap.json"
    code, _ = once(
        Options(once=True, fixture="base", snapshot=str(target)), deps_for(fake_clock)
    )
    assert (
        code == 0 and list(VALIDATOR.iter_errors(json.loads(target.read_text()))) == []
    )
    live_dir = tmp_path / "state"
    runner = FakeRunner(argv_log, [reply(2)])
    once(
        Options(once=True),
        deps_for(
            fake_clock,
            runner=runner,
            discover=FakeDiscover(argv_log),
            state_directory=live_dir,
        ),
    )
    once(
        Options(once=True, fixture="empty"),
        deps_for(fake_clock, state_directory=live_dir),
    )
    assert (
        not live_dir.exists()
        and [p.name for p in tmp_path.iterdir() if p.name != "snap.json"] == []
    )


def test_an_unwritable_snapshot_path_exits_non_zero_with_a_message(
    fake_clock, tmp_path, capsys
):
    code, _ = once(
        Options(once=True, fixture="base", snapshot=str(tmp_path)), deps_for(fake_clock)
    )
    assert code == 1 and "snapshot failed" in capsys.readouterr().err


# -- click wiring ---------------------------------------------------------------------------------------------------


def test_help_lists_every_option_and_the_per_process_cap_warning():
    out = CliRunner().invoke(observe_group, ["--help"]).output
    for option in ("--once", "--width", "--ascii", "--fixture", "--run", "--snapshot"):
        assert option in out
    flat = " ".join(out.split())
    assert "per observer process" in flat and "multiply the load on Orca" in flat
    assert "read-only" in flat.lower() or "never writes to Orca" in flat


@pytest.mark.parametrize(
    "args",
    [
        ["--once", "--fixture", "nope"],
        ["--once", "--run", "-x"],
        ["--once", "--run", "bad id"],
        ["--once", "--width", "100"],
    ],
)
def test_bad_option_values_are_rejected_before_anything_runs(args):
    result = CliRunner().invoke(observe_group, args)
    assert result.exit_code == 2 and "Traceback" not in result.output


# -- interactive mode -----------------------------------------------------------------------------------------------------


def test_interactive_mode_on_a_non_posix_platform_prints_the_message_and_never_imports_keys(
    fake_clock, capsys, monkeypatch
):
    monkeypatch.delitem(sys.modules, KEYS_MODULE, raising=False)
    code = execute(Options(), Deps(platform="win32", clock=fake_clock))
    assert code != 0 and capsys.readouterr().out == POSIX_ONLY_TEXT + "\n"
    assert POSIX_ONLY_TEXT == "interactive mode needs a POSIX terminal; use --once"
    assert KEYS_MODULE not in sys.modules
    monkeypatch.setattr(sys, "platform", "win32")
    result = CliRunner().invoke(observe_group, [])
    assert (
        result.exit_code != 0
        and POSIX_ONLY_TEXT in result.output
        and KEYS_MODULE not in sys.modules
    )


class ScriptedKeys:
    """A key source that releases its script once ``gate`` is true, then quits."""

    def __init__(self, keys, gate=lambda: True, available=True, raise_on_read=None):
        self.keys = list(keys)
        self.gate = gate
        self.available = available
        self.entered = self.exited = False
        self.raise_on_read = raise_on_read

    def __enter__(self):
        self.entered = True
        return self

    def __exit__(self, *exc):
        self.exited = True

    def read(self, timeout):
        if self.raise_on_read:
            raise self.raise_on_read
        if not self.gate():
            time.sleep(0.002)
            return None
        return self.keys.pop(0) if self.keys else Key("text", "q")

    def consume_redraw(self):
        return False


class FakeScreen:
    def __init__(self, fail=False):
        self.frames: list[tuple] = []
        self.closed = 0
        self.fail = fail

    def draw(self, view, policy, message):
        if self.fail:
            raise RuntimeError("boom")
        self.frames.append((view, message, policy))

    def close(self):
        self.closed += 1


def text_key(char):
    return Key("text", char)


def live_threads():
    return [t for t in threading.enumerate() if t.name == "observe-collector"]


def test_scripted_keys_drive_the_session_and_q_restores_the_terminal(
    fake_clock, tmp_path
):
    collector = Collector(FixtureSource("base"), fake_clock, interval=0.005)
    keys = ScriptedKeys(
        [
            text_key("j"),
            text_key("/"),
            text_key("w"),
            text_key("-"),
            text_key("0"),
            Key("enter"),
            text_key("h"),
            text_key("m"),
            text_key("e"),
            text_key("q"),
        ],
        gate=lambda: collector.latest().cycle >= 1,
    )
    screen = FakeScreen()
    with keys:
        code = run_loop(
            collector,
            keys,
            screen,
            fake_clock,
            make_policy=lambda: commands.resolve_policy({}, "utf-8", {}, 160, 40),
            directory=tmp_path,
            snapshot_file=tmp_path / "snap.json",
            write_snapshots=False,
        )
    assert (
        code == 0
        and keys.entered
        and keys.exited
        and screen.closed >= 1
        and live_threads() == []
    )
    views = [frame[0] for frame in screen.frames]
    assert any(v.selected is not None and v.selected.selected for v in views)
    assert any(v.focus == "filter" for v in views)
    assert any(v.filter_line and v.filter_line.startswith("filter w-0") for v in views)
    assert any(v.show_historical for v in views)
    assert views[-1].changes_line.startswith("changed since")
    exported = list(tmp_path.glob("observe-*.txt"))
    assert len(exported) == 1 and exported[0].read_text().startswith("ORCA OBSERVER")
    assert any(frame[1] == f"exported {exported[0]}" for frame in screen.frames)
    assert not (tmp_path / "snap.json").exists()


def test_a_failed_export_shows_a_message_and_the_loop_goes_on(fake_clock, tmp_path):
    blocker = tmp_path / "not-a-directory"
    blocker.write_text("x")
    collector = Collector(FixtureSource("base"), fake_clock, interval=0.005)
    keys = ScriptedKeys(
        [text_key("e"), text_key("q")], gate=lambda: collector.latest().cycle >= 1
    )
    screen = FakeScreen()
    code = run_loop(
        collector,
        keys,
        screen,
        fake_clock,
        make_policy=lambda: commands.resolve_policy({}, "utf-8", {}, 160, 40),
        directory=blocker / "sub",
        snapshot_file=tmp_path / "s.json",
        write_snapshots=False,
    )
    assert code == 0 and any(
        (m or "").startswith("export failed:") for _, m, _ in screen.frames
    )


class FakeCollector:
    """Publishes one prepared result per key read, so each cycle is seen exactly once."""

    def __init__(self, results):
        self.results = results
        self.index = 0
        self.started = self.stopped = False

    def latest(self):
        return self.results[self.index]

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True


class AdvancingKeys(ScriptedKeys):
    def __init__(self, collector):
        super().__init__([])
        self.collector = collector

    def read(self, timeout):
        if self.collector.index < len(self.collector.results) - 1:
            self.collector.index += 1
            return None
        return Key("text", "q")


def test_live_mode_writes_exactly_one_snapshot_per_published_cycle_including_a_failed_one(
    fake_clock, argv_log, tmp_path, monkeypatch
):
    runner = FakeRunner(argv_log, [reply(3), (2, "", "boom"), reply(3)])
    source = Collector(LiveSource(runner, FakeDiscover(argv_log)), fake_clock)
    results = [source.latest(), source.run_once(), source.run_once(), source.run_once()]
    assert [r.state for r in results] == ["NOT_POLLED", "OK", "FAILED", "OK"]
    writes: list[tuple[Path, str]] = []
    real = commands.write_atomic

    def spy(path, text):
        writes.append((path, text))
        return real(path, text)

    monkeypatch.setattr(commands, "write_atomic", spy)
    collector = FakeCollector(results)
    keys = AdvancingKeys(collector)
    screen = FakeScreen()
    target = tmp_path / "snapshot.json"
    code = run_loop(
        collector,
        keys,
        screen,
        fake_clock,
        make_policy=lambda: commands.resolve_policy({}, "utf-8", {}, 160, 40),
        directory=tmp_path,
        snapshot_file=target,
        write_snapshots=True,
    )
    assert code == 0 and collector.started and collector.stopped
    datas = [json.loads(text) for _, text in writes]
    assert [d["cycle"] for d in datas] == [1, 2, 3] and {p for p, _ in writes} == {
        target
    }
    assert [d["source"]["status"] for d in datas] == ["OK", "ERROR", "OK"]
    assert (
        datas[1]["source"]["error"] == "exit:2" and len(datas[1]["rows"]) == 3
    )  # the last good rows
    for data in datas:
        assert list(VALIDATOR.iter_errors(data)) == []
    assert json.loads(target.read_text())["cycle"] == 3


def test_fixture_mode_writes_no_snapshot_unless_asked(fake_clock, tmp_path):
    def interactive(options):
        start = time.monotonic()
        keys = ScriptedKeys([], gate=lambda: time.monotonic() - start > 0.15)
        deps = Deps(
            clock=fake_clock,
            key_source=keys,
            screen_factory=FakeScreen,
            state_directory=tmp_path,
            interval=0.005,
            size=lambda: (160, 40),
            encoding="utf-8",
            env={},
        )
        return execute(options, deps)

    assert interactive(Options(fixture="base")) == 0
    assert list(tmp_path.glob("snapshot.json")) == []
    asked = tmp_path / "asked.json"
    assert interactive(Options(fixture="base", snapshot=str(asked))) == 0
    assert list(VALIDATOR.iter_errors(json.loads(asked.read_text()))) == []
    assert live_threads() == []


def test_e_writes_one_record_under_a_temporary_xdg_state_home(
    fake_clock, tmp_path, monkeypatch
):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    start = time.monotonic()
    keys = ScriptedKeys(
        [text_key("e"), text_key("q")], gate=lambda: time.monotonic() - start > 0.15
    )
    deps = Deps(  # no state_directory: the command resolves it through state_dir()
        clock=fake_clock,
        key_source=keys,
        screen_factory=FakeScreen,
        interval=0.005,
        size=lambda: (160, 40),
        encoding="utf-8",
        env={},
    )
    assert execute(Options(fixture="base"), deps) == 0
    records = list((tmp_path / "superclaude" / "observe").glob("observe-*.txt"))
    assert len(records) == 1 and records[0].read_text().startswith("ORCA OBSERVER")
    assert live_threads() == []


def test_a_terminal_that_is_not_a_tty_is_reported_not_crashed(fake_clock, capsys):
    keys = ScriptedKeys([], available=False)
    code = execute(
        Options(fixture="base"),
        Deps(clock=fake_clock, key_source=keys, screen_factory=FakeScreen),
    )
    assert (
        code == 2 and capsys.readouterr().out == NO_TERMINAL_TEXT + "\n" and keys.exited
    )


def test_a_render_exception_stops_the_screen_restores_the_terminal_and_exits_non_zero(
    fake_clock, tmp_path, capsys
):
    collector = Collector(FixtureSource("base"), fake_clock, interval=0.005)
    keys = ScriptedKeys(
        [text_key("x")], gate=lambda: True
    )  # a key read makes the loop draw
    screen = FakeScreen(fail=True)
    with keys:
        code = run_loop(
            collector,
            keys,
            screen,
            fake_clock,
            make_policy=lambda: commands.resolve_policy({}, "utf-8", {}, 160, 40),
            directory=tmp_path,
            snapshot_file=tmp_path / "s.json",
            write_snapshots=False,
        )
    assert code == 1 and screen.closed >= 1 and keys.exited and live_threads() == []
    assert "observe: display failed: boom" in capsys.readouterr().err


def test_ctrl_c_during_a_read_quits_quietly_and_cleans_up(fake_clock, tmp_path):
    collector = Collector(FixtureSource("base"), fake_clock, interval=0.005)
    keys = ScriptedKeys([], raise_on_read=KeyboardInterrupt())
    screen = FakeScreen()
    code = run_loop(
        collector,
        keys,
        screen,
        fake_clock,
        make_policy=lambda: commands.resolve_policy({}, "utf-8", {}, 160, 40),
        directory=tmp_path,
        snapshot_file=tmp_path / "s.json",
        write_snapshots=False,
    )
    assert code == 0 and screen.closed >= 1 and live_threads() == []


def test_the_screen_follows_the_terminal_size_on_every_redraw(fake_clock, tmp_path):
    sizes = iter([(160, 40), (116, 30), (80, 24)] + [(80, 24)] * 100)
    collector = Collector(FixtureSource("base"), fake_clock, interval=0.005)
    keys = ScriptedKeys(
        [text_key("j"), text_key("j")], gate=lambda: collector.latest().cycle >= 1
    )
    screen = FakeScreen()
    run_loop(
        collector,
        keys,
        screen,
        fake_clock,
        make_policy=lambda: commands.resolve_policy({}, "utf-8", {}, *next(sizes)),
        directory=tmp_path,
        snapshot_file=tmp_path / "s.json",
        write_snapshots=False,
    )
    widths = [frame[2].width for frame in screen.frames]
    assert widths[:3] == [160, 116, 80]


# -- clock and module hygiene ----------------------------------------------------------------------------------------------------


def test_system_clock_gives_monotonic_wall_and_a_time_zone():
    clock = SystemClock()
    first = clock.monotonic()
    assert clock.monotonic() >= first and abs(clock.wall() - time.time()) < 5
    assert clock.local_tz() is not None


def test_no_module_other_than_the_adapter_imports_subprocess_and_none_names_an_orca_verb():
    package = Path(observe_pkg.__file__).parent
    offenders = []
    for path in sorted(package.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        if path.name != "adapter.py" and re.search(
            r"^\s*(import subprocess|from subprocess\b)", text, re.M
        ):
            offenders.append(path.name)
    assert offenders == []
    commands_text = Path(commands.__file__).read_text(encoding="utf-8")
    assert "worker-list" not in commands_text and "orchestration" not in commands_text
    assert not re.search(
        r"^from superclaude\.cli\.observe\.keys|^import superclaude\.cli\.observe\.keys",
        commands_text,
        re.M,
    )


# -- R2: --questions and the gate guard (T56) --------------------------------------------------------------------------------

from tests.observe.conftest import (  # noqa: E402
    QRUN,
    make_question_envelope,
    make_question_rows,
    routed_runner_responses,
)


def question_runner(argv_log, rows=None):
    worker = reply(3)
    rows = make_question_rows(4) if rows is None else rows
    message = (0, json.dumps(make_question_envelope(rows)))
    return FakeRunner(argv_log, [routed_runner_responses(worker, message)])


def messages_in(argv_log):
    return [a for a in argv_log if a[1:3] == ["orchestration", "check"]]


def test_t56_with_the_guard_off_questions_is_refused_and_no_orca_call_is_made(
    fake_clock, argv_log
):
    assert (
        commands.QUESTION_GATE_PASSED is False
    )  # ships OFF until the owner's record exists
    runner = question_runner(argv_log)
    deps = deps_for(fake_clock, runner=runner, discover=FakeDiscover(argv_log))
    code, out = once(Options(once=True, run_id=QRUN, questions=True), deps)
    assert code != 0 and out == ""
    assert argv_log == [] and runner.calls == 0  # not even discovery
    via_click = CliRunner().invoke(
        observe_group, ["--once", "--run", QRUN, "--questions"]
    )
    assert via_click.exit_code != 0
    assert (
        "question read not enabled: QUESTION-OBSERVATION has not passed"
        in via_click.output
    )


def test_the_interactive_path_is_refused_too_with_the_guard_off(fake_clock, argv_log):
    runner = question_runner(argv_log)
    deps = deps_for(fake_clock, runner=runner, discover=FakeDiscover(argv_log))
    assert execute(Options(run_id=QRUN, questions=True), deps) != 0
    assert argv_log == []


def test_with_the_guard_open_one_template_message_call_follows_the_worker_list_calls(
    fake_clock, argv_log, monkeypatch
):
    monkeypatch.setattr(commands, "QUESTION_GATE_PASSED", True)
    runner = question_runner(argv_log)
    deps = deps_for(fake_clock, runner=runner, discover=FakeDiscover(argv_log))
    code, out = once(Options(once=True, run_id=QRUN, questions=True), deps)
    assert code == 0
    message = messages_in(argv_log)
    assert message == [
        [
            "/opt/fake/orca", "orchestration", "check", "--all", "--types", "question",
            "--run", QRUN, "--json",
        ]
    ]  # fmt: skip
    worker = [a for a in argv_log if a[1:3] == ["orchestration", "worker-list"]]
    assert len(worker) == 1 and "--peek" not in message[0]
    lines = out.splitlines()
    assert "COORDINATOR QUESTIONS" in lines and f"one Run only: {QRUN}" in lines
    assert sum("reason unknown" in l for l in lines) == 4
    assert (
        "seen, not resolved: 4 | closed by evidence: unavailable (no source)" in lines
    )


def test_with_the_guard_open_and_a_width_the_screen_shows_the_panel(
    fake_clock, argv_log, monkeypatch
):
    monkeypatch.setattr(commands, "QUESTION_GATE_PASSED", True)
    deps = deps_for(
        fake_clock,
        runner=question_runner(argv_log),
        discover=FakeDiscover(argv_log),
        size=lambda: (160, 50),
    )
    code, out = once(Options(once=True, run_id=QRUN, questions=True, width=116), deps)
    lines = out.splitlines()
    assert code == 0 and all(cell_len(l) <= 116 for l in lines)
    assert "COORDINATOR QUESTIONS" in lines and GAP_NOTICE not in lines


def test_questions_without_a_run_or_with_a_fixture_or_a_bad_run_is_refused_with_no_call(
    fake_clock, argv_log, monkeypatch
):
    for guard in (False, True):
        monkeypatch.setattr(commands, "QUESTION_GATE_PASSED", guard)
        runner = question_runner(argv_log)
        deps = deps_for(fake_clock, runner=runner, discover=FakeDiscover(argv_log))
        for options in (
            Options(once=True, questions=True),
            Options(once=True, questions=True, fixture="base", run_id=QRUN),
            Options(once=True, questions=True, run_id="-x"),
            Options(once=True, questions=True, run_id="bad id"),
        ):
            assert execute(options, deps) == 2
        assert argv_log == []
    for args in (
        ["--once", "--questions"],
        ["--once", "--questions", "--fixture", "base", "--run", QRUN],
        ["--once", "--questions", "--run", "-x"],
        ["--once", "--questions", "--run", "bad id"],
    ):
        result = CliRunner().invoke(observe_group, args)
        assert result.exit_code != 0, args


def test_questions_off_leaves_the_message_source_unused_even_with_a_run(
    fake_clock, argv_log
):
    runner = question_runner(argv_log)
    deps = deps_for(fake_clock, runner=runner, discover=FakeDiscover(argv_log))
    code, out = once(Options(once=True, run_id=QRUN), deps)
    assert code == 0 and messages_in(argv_log) == []
    assert GAP_NOTICE in out.splitlines() and "COORDINATOR" not in out


def test_help_states_the_one_run_rule_the_disclosure_and_that_run_use_is_never_run():
    result = CliRunner().invoke(observe_group, ["--help"])
    flat = " ".join(result.output.split())
    assert result.exit_code == 0 and "--questions" in flat
    assert "never runs run-use" in flat
    assert "the observer never runs run-use and never binds to a Run" in flat
    assert "Run it from the terminal that already holds the Run" in flat
    assert (
        "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost"
        in flat
    )
    assert (
        "Message bodies are received by this process; subjects are shown, bodies are not kept"
        in flat
    )
    assert "one named Run" in flat


def test_the_guard_constant_is_a_literal_false_with_a_comment_naming_the_gate_record():
    text = Path(commands.__file__).read_text(encoding="utf-8")
    assert len(re.findall(r"^QUESTION_GATE_PASSED = (True|False)$", text, re.M)) == 1
    assert "QUESTION_GATE_PASSED = False" in text
    assert "release-gates.md" in text and "Task 18" in text
