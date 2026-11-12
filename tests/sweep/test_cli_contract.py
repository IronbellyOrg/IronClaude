"""The command-line contract of ``superclaude sweep run`` (DESIGN section 11, ``test_cli_contract.py`` row).

Covers FR-002 (Run selection and the binding tests), FR-003 (the ``--window`` parser), FR-004
(``--output`` and ``--root``), FR-005 (the 4-row, 2-worktree fixture and the summary
reconciliation), FR-017 (report naming, the golden JSON v1 key set), FR-018 (one test per exit
code), FR-019 (disk-only continuation), NFR-009 and G-1 (the section 3 publication cases).

Every test drives ``sweep_group`` through ``CliRunner`` with the seams patched: ``patch_orca``
and ``patch_git`` from ``conftest.py``, a fixed ``now`` injected into ``commands``, and
``monkeypatch.setattr`` on ``os.link``, ``os.unlink``, ``os.write``, ``os.makedirs`` and
``click.echo`` for the publication failures (those wrappers raise only for a call made from
``commands``, so the rest of the process keeps working). Two tests read the real ``_orca``
over a recorded ``subprocess.run`` so the captured Orca shapes are classified by the real
code; none starts a process.

Recorded minor findings (``qa/impl-cli/consolidated-findings-cycle0.md``) are pinned as
observed and named in a comment beside the case: CLI-F3 and CLI-F33 (what is and is not
sanitized on stderr), CLI-F24 (the SPEC reason ``orca call failed (unknown run)`` is never
produced), CLI-F26 (SPEC ids ``R1``, ``R2``, ``BAD`` are not valid Run ids), CLI-F32 (the
symlinked ``.dev/sweeps`` message), CLI-F37 (``--run ""`` prints an empty value).
"""

from __future__ import annotations

import errno
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import click
import pytest
from click.testing import CliRunner

from superclaude.cli.sweep import commands, probes, sweep_group
from superclaude.cli.sweep.models import CLASSES

FIXTURES = Path(__file__).parent / "fixtures"
_REAL_ORCA = (
    probes._orca
)  # the real seam, kept for the tests that read it over a fake run

# SPEC literals R1, R2 and BAD are not valid under ``run_`` plus 12 lowercase hex (CLI-F26).
RUN = "run_aaaaaaaaaaaa"
RUN2 = "run_bbbbbbbbbbbb"
BAD = "run_000000000000"  # the unknown Run of the captured unknown-Run fixtures
CAPTURED_RUN = "run_a4723d345399"  # the Run of the captured worker-list fixture
STEM = "20261108-120000-sweep"  # fixed_now is 2026-11-08 12:00:00 UTC

RUN_CURRENT = ("orchestration", "run-current")
WORKTREE_PS = ("worktree", "ps", "--json")


def _worker_list(run: str) -> tuple[str, ...]:
    return ("orchestration", "worker-list", "--run", run, "--json")


def _task_list_ready(run: str) -> tuple[str, ...]:
    return ("orchestration", "task-list", "--ready", "--run", run, "--json")


def _task_list(run: str) -> tuple[str, ...]:
    return ("orchestration", "task-list", "--run", run, "--json")


def _worker_show(dispatch: str) -> tuple[str, ...]:
    return ("orchestration", "worker-show", "--dispatch", dispatch, "--json")


def _captured(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text("utf-8"))


# --- Fixtures ---------------------------------------------------------------------------


@pytest.fixture
def env(sweep_root, patch_orca, patch_git, monkeypatch, fixed_now):
    """A checkout stand-in with the seams faked and ``now`` fixed at 2026-11-08 12:00:00 UTC.

    ``patch_orca`` answers a read only when the test names it (an unnamed one is a
    ``call_failed``); ``patch_git`` reports a clean branch. ``commands.datetime`` is a
    subclass whose ``now`` returns ``fixed_now``, so a report is named from that second.
    """
    monkeypatch.setattr(probes, "read_orca_version", lambda: None)
    monkeypatch.delenv("ORCA_CLI_COMMAND", raising=False)
    patch_git.default = "## main\0"

    class _Clock(datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed_now

    monkeypatch.setattr(commands, "datetime", _Clock)
    root = sweep_root.root.resolve()
    return SimpleNamespace(
        sweep_root=sweep_root,
        root=root,
        sweeps=root / ".dev" / "sweeps",
        orca=patch_orca,
        git=patch_git,
        now=fixed_now,
        tmp=sweep_root.base,
    )


class _OrcaProcess:
    """Stands in for ``subprocess.run`` when the real ``_orca`` seam is under test."""

    def __init__(self) -> None:
        self.calls: list[list[str]] = []
        self.replies: dict[tuple[str, ...], tuple[int, bytes, bytes]] = {}

    def reply(
        self, *args: str, code: int = 0, out: bytes = b"", err: bytes = b""
    ) -> None:
        self.replies[tuple(args)] = (code, out, err)

    def ok(self, *args: str, result: object) -> None:
        body = {
            "id": "00000000-0000-4000-8000-000000000099",
            "ok": True,
            "result": result,
        }
        self.reply(*args, out=json.dumps(body).encode("utf-8"))

    def argv(self) -> list[tuple[str, ...]]:
        """Every Orca argument tuple the seam ran, without the binary name."""
        return [tuple(call[1:]) for call in self.calls]

    def __call__(self, argv, **kwargs):
        self.calls.append(list(argv))
        code, out, err = self.replies.get(tuple(argv[1:]), (1, b"", b"no canned reply"))
        return SimpleNamespace(returncode=code, stdout=out, stderr=err)


@pytest.fixture
def proc(env, monkeypatch) -> _OrcaProcess:
    """The real ``probes._orca`` over a recorded ``subprocess.run`` (patched after the guard)."""
    recorder = _OrcaProcess()
    monkeypatch.setattr(probes, "_orca", _REAL_ORCA)
    monkeypatch.setattr(probes.subprocess, "run", recorder)
    return recorder


# --- Helpers ----------------------------------------------------------------------------


def _canned(env, run=RUN, *, workers=(), shows=None, ready=(), tasks=()) -> None:
    """Answer the three reads of one Run (and a ``worker-show`` per entry of ``shows``)."""
    env.orca.respond(_worker_list(run), {"workers": list(workers)})
    env.orca.respond(_task_list_ready(run), {"tasks": list(ready)})
    env.orca.respond(_task_list(run), {"tasks": list(tasks)})
    for dispatch, show in (shows or {}).items():
        env.orca.respond(_worker_show(dispatch), show)


def _ps(env, *paths: Path) -> None:
    env.orca.respond(WORKTREE_PS, {"worktrees": [{"path": str(p)} for p in paths]})


def _world(env, *runs: str) -> None:
    """The smallest complete sweep: each Run has no workers and no worktree beyond the root."""
    for run in runs or (RUN,):
        _canned(env, run)
    _ps(env)


def _run(env, *args: str, root: bool = True):
    argv = ["run", *args]
    if root:
        argv += ["--root", str(env.sweep_root.root)]
    return CliRunner().invoke(sweep_group, argv)


def _payload(result) -> dict:
    """The one JSON object of a successful run: exit 0, empty stderr, exactly one line."""
    assert result.exit_code == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout.endswith("\n")
    assert result.stdout.count("\n") == 1
    payload = json.loads(result.stdout)
    assert isinstance(payload, dict)
    return payload


def _failed(result, code: int, stderr: str) -> None:
    """A failed run: the exit code, nothing on stdout and the stderr text byte for byte."""
    assert (result.exit_code, result.stdout, result.stderr) == (code, "", stderr)


_REPORT_NAME = re.compile(r"\d{8}-\d{6}-sweep(-\d+)?\.md")


def _reports(folder: Path) -> list[str]:
    if not folder.is_dir():
        return []
    return sorted(p.name for p in folder.iterdir() if _REPORT_NAME.fullmatch(p.name))


def _temp_files(folder: Path) -> list[str]:
    if not folder.is_dir():
        return []
    return sorted(p.name for p in folder.iterdir() if p.name.endswith(".tmp"))


def _temp_path(env) -> Path:
    return env.sweeps / f".{STEM}.{os.getpid()}.tmp"


def _source(payload: dict, name: str) -> dict:
    (row,) = [s for s in payload["sources"] if s["name"] == name]
    return row


def _row(payload: dict, row_id: str) -> dict:
    (row,) = [r for r in payload["rows"] if r["row_id"] == row_id]
    return row


def _orca_calls(env) -> list[tuple[str, ...]]:
    return [c["args"] for c in env.orca.calls]


def _nothing_written(env) -> None:
    assert not (env.root / ".dev").exists()


def _fail_in_commands(monkeypatch, owner, name: str, replacement) -> None:
    """Patch ``owner.name`` so a call made from ``commands`` goes to ``replacement``.

    ``replacement(real, *args, **kwargs)`` may raise or call ``real``. A call from anywhere
    else (pytest, click, the tmp folder clean-up) reaches the real function.
    """
    real = getattr(owner, name)

    def wrapper(*args, **kwargs):
        if sys._getframe(1).f_globals.get("__name__") == commands.__name__:
            return replacement(real, *args, **kwargs)
        return real(*args, **kwargs)

    monkeypatch.setattr(owner, name, wrapper)


def _raise(exc: BaseException):
    def replacement(real, *args, **kwargs):
        raise exc

    return replacement


# =========================================================================================
# FR-002: Run id checks (exit 2 before any Orca call)
# =========================================================================================


def test_empty_run_id_exits_2_before_any_orca_call(env):
    _world(env)

    result = _run(env, "--run", "")

    # CLI-F37: the message holds the empty value, so it ends in a space before the newline.
    _failed(result, 2, "invalid --run value: \n")
    assert env.orca.calls == []
    _nothing_written(env)


def test_run_id_with_a_semicolon_exits_2_before_any_orca_call(env):
    _world(env)

    result = _run(env, "--run", "r;x")

    _failed(result, 2, "invalid --run value: r;x\n")
    assert env.orca.calls == []
    _nothing_written(env)


@pytest.mark.parametrize(
    "value",
    [
        "R1",
        "BAD",
        "run_AAAAAAAAAAAA",
        "run_aaaaaaaaaaa",
        "run_aaaaaaaaaaaaa",
        " run_aaaaaaaaaaaa",
    ],
    ids=["spec-R1", "spec-BAD", "upper-case-hex", "11-hex", "13-hex", "leading-space"],
)
def test_run_id_that_does_not_match_the_run_pattern_exits_2(env, value):
    # CLI-F26: SPEC examples R1, R2 and BAD are not valid ids under ``run_`` + 12 lowercase hex.
    _world(env)

    result = _run(env, "--run", value)

    _failed(result, 2, f"invalid --run value: {value}\n")
    assert env.orca.calls == []


def test_one_bad_run_id_among_good_ones_exits_2_and_reads_nothing(env):
    _world(env, RUN)

    result = _run(env, "--run", RUN, "--run", "r;x")

    _failed(result, 2, "invalid --run value: r;x\n")
    assert env.orca.calls == []


def test_duplicate_run_ids_collapse_to_one_worker_list_argv(env):
    _world(env, RUN)

    payload = _payload(_run(env, "--run", RUN, "--run", RUN))

    assert _orca_calls(env).count(_worker_list(RUN)) == 1
    assert _orca_calls(env).count(_task_list(RUN)) == 1
    assert payload["scope"]["runs"] == [RUN]


def test_duplicate_run_ids_keep_first_seen_order(env):
    _world(env, RUN, RUN2)

    payload = _payload(_run(env, "--run", RUN2, "--run", RUN, "--run", RUN2))

    assert payload["scope"]["runs"] == [RUN2, RUN]
    lists = [a for a in _orca_calls(env) if a[:2] == ("orchestration", "worker-list")]
    assert lists == [_worker_list(RUN2), _worker_list(RUN)]


def test_unknown_run_then_a_second_run_reads_both_and_exits_0(env, proc, fixed_now):
    # The captured unknown-Run shape (step 1.0a, section 8): worker-list exits 0 with an empty
    # list, task-list exits 1 with ``run_not_found``. The SPEC reason ``orca call failed
    # (unknown run)`` is never produced (CLI-F24); the observed result is asserted instead.
    unknown_list = (FIXTURES / "captured-worker-list-unknown-run.json").read_bytes()
    unknown_tasks = (FIXTURES / "captured-task-list-unknown-run.json").read_bytes()
    proc.reply(*_worker_list(BAD), out=unknown_list)
    # The ready form for an unknown Run was not captured; it gets the same error body.
    proc.reply(*_task_list_ready(BAD), code=1, out=unknown_tasks)
    proc.reply(*_task_list(BAD), code=1, out=unknown_tasks)
    proc.ok(*_worker_list(RUN2), result={"workers": []})
    proc.ok(*_task_list_ready(RUN2), result={"tasks": []})
    proc.ok(*_task_list(RUN2), result={"tasks": []})
    proc.ok(*WORKTREE_PS, result={"worktrees": []})
    env.sweep_root.transcript(stamps=(fixed_now - timedelta(hours=8),))

    payload = _payload(_run(env, "--run", BAD, "--run", RUN2))

    lists = [a for a in proc.argv() if a[:2] == ("orchestration", "worker-list")]
    assert lists == [
        _worker_list(BAD),
        _worker_list(RUN2),
    ]  # R2 is still read after BAD
    assert payload["scope"]["runs"] == [BAD, RUN2]
    assert payload["orca_available"] is True
    assert _source(payload, f"orca worker-list {BAD}")["unscanned"] is None
    assert _source(payload, f"orca task-list {BAD}")["unscanned"] == (
        "orca call failed (exit 1)"
    )
    assert _source(payload, f"orca worker-list {RUN2}")["unscanned"] is None
    assert _source(payload, f"orca task-list {RUN2}")["unscanned"] is None
    # The Run is not confirmed, so an older unjoined transcript stays visible (FR-010).
    row = _row(payload, "transcript:session-0001")
    assert row["notes"] == ["origin unknown: Run not confirmed"]
    assert row["person_started"] is None
    assert payload["summary"]["historical"] == 0


# =========================================================================================
# FR-002 and FR-019: the three binding tests and the fourth gated on step 1.0a
# =========================================================================================


def test_binding_1_no_run_and_first_call_failure_exits_2_with_one_argv(env):
    env.orca.respond(
        RUN_CURRENT, kind="unavailable", reason="binary not found: orca-ide"
    )

    result = _run(env)

    _failed(
        result,
        2,
        "Orca unavailable (binary not found: orca-ide); "
        "no Run binding could be established: pass --run <id>\n",
    )
    assert _orca_calls(env) == [RUN_CURRENT]  # one _orca argv
    _nothing_written(env)  # no report


def test_binding_2_explicit_run_and_first_call_failure_publishes_and_exits_0(
    env, fixed_now
):
    env.orca.respond(
        _worker_list(RUN), kind="unavailable", reason="runtime_unavailable"
    )
    env.sweep_root.transcript(stamps=(fixed_now - timedelta(minutes=5),))

    result = _run(env, "--run", RUN)
    payload = _payload(result)

    assert _orca_calls(env) == [
        _worker_list(RUN)
    ]  # one _orca argv, then no more Orca reads
    assert _reports(env.sweeps) == [f"{STEM}.md"]
    assert payload["orca_available"] is False
    _assert_disk_only_continuation(env, payload, RUN)


def test_binding_3_binding_then_second_call_failure_publishes_and_exits_0(
    env, fixed_now
):
    env.orca.respond(RUN_CURRENT, RUN)  # the binding is established
    env.orca.respond(
        _worker_list(RUN), kind="unavailable", reason="runtime_unavailable"
    )
    env.sweep_root.transcript(stamps=(fixed_now - timedelta(minutes=5),))

    payload = _payload(_run(env))

    assert _orca_calls(env) == [RUN_CURRENT, _worker_list(RUN)]  # two _orca argv
    assert _reports(env.sweeps) == [f"{STEM}.md"]
    assert payload["scope"]["runs"] == [RUN]
    assert payload["orca_available"] is False
    _assert_disk_only_continuation(env, payload, RUN)


def test_orca_answered_but_worktree_list_truncated_prints_the_ps_unscanned_banner(env):
    # DESIGN 7.5, second banner form: Orca answered, only ``orca worktree ps`` is incomplete.
    _canned(env)
    env.orca.respond(WORKTREE_PS, {"worktrees": [], "truncated": True})

    payload = _payload(_run(env, "--run", RUN))

    assert payload["orca_available"] is True
    assert (
        _source(payload, "orca worktree ps")["unscanned"] == "worktree list truncated"
    )
    text = (env.sweeps / f"{STEM}.md").read_text("utf-8")
    assert text.count("[child worktrees not discovered") == 1
    assert (
        "[child worktrees not discovered: orca worktree ps unscanned "
        "(worktree list truncated); worktree count is a lower bound]"
    ) in text.splitlines()
    assert "Orca unavailable" not in text


def _assert_disk_only_continuation(env, payload: dict, run: str) -> None:
    """FR-019: the Orca reads after the failure are unscanned, the disk sources still read."""
    for name in (
        f"orca task-list --ready {run}",
        f"orca task-list {run}",
        "orca worktree ps",
    ):
        assert _source(payload, name)["unscanned"] == "orca unavailable"
    text = (env.sweeps / f"{STEM}.md").read_text("utf-8")
    table = _table_rows(_section(text, "## Source coverage"))
    printed = [ln for ln in table if "unscanned: orca unavailable" in ln]
    assert sorted(ln.split(" | ")[0].lstrip("| ") for ln in printed) == sorted(
        [f"orca task-list --ready {run}", f"orca task-list {run}", "orca worktree ps"]
    )  # the report prints the same three rows
    assert "[child worktrees not discovered: Orca unavailable" in text  # the banner
    # The disk sources were still read: the root worktree and the transcript.
    assert [w["path"] for w in payload["worktrees"]] == [str(env.root)]
    row = _row(payload, "transcript:session-0001")
    assert row["notes"] == ["origin unknown: Orca unavailable"]
    assert payload["summary"]["total"] == 1


_CAPTURE = FIXTURES / "captured-run-current.json"


@pytest.mark.skipif(
    not _CAPTURE.exists(),
    reason="gated on step 1.0a: the no-binding capture is missing",
)
def test_binding_4_captured_no_binding_shape_exits_2_and_reads_nothing_else(env, proc):
    # Gated on step 1.0a. The no-binding shape was captured (exit 0, one plain sentence); the
    # bound shape was never captured, so no test pins how a bound ``run-current`` prints.
    captured = _captured("captured-run-current.json")
    assert captured["exit_code"] == 0
    assert captured["stdout"] == "No Run is bound to this terminal.\n"
    proc.reply(
        *RUN_CURRENT, code=captured["exit_code"], out=captured["stdout"].encode()
    )

    result = _run(env)

    _failed(result, 2, "no Run bound: pass --run <id>\n")
    assert proc.argv() == [RUN_CURRENT]  # no worker-list, no worker-show, nothing else
    _nothing_written(env)


# =========================================================================================
# FR-003: the --window parser
# =========================================================================================


@pytest.mark.parametrize(
    ("text", "hours", "shown"),
    [
        ("1h", 1, "1h"),
        ("6h", 6, "6h"),
        ("2d", 48, "48h"),
        ("3d", 72, "72h"),
        ("720h", 720, "720h"),
        ("30d", 720, "720h"),
        ("9h", 9, "9h"),
        ("100h", 100, "100h"),
    ],
)
def test_valid_windows_parse_and_reach_the_json(env, text, hours, shown):
    _world(env)

    assert commands._parse_window(text) == timedelta(hours=hours)
    payload = _payload(_run(env, "--run", RUN, f"--window={text}"))

    assert payload["window"] == shown


def test_default_window_is_6h(env):
    _world(env)

    assert _payload(_run(env, "--run", RUN))["window"] == "6h"


@pytest.mark.parametrize(
    ("window", "class_name", "historical"),
    [
        ("1h", "idle", 1),
        ("12h", "person session (active)", 0),
        ("2h", "person session (active)", 0),  # the edge: last_activity == window_start
    ],
    ids=["1h-is-idle", "12h-is-active", "2h-edge-is-active"],
)
def test_window_reaches_the_classification(env, window, class_name, historical):
    # TST-F3 (FR-003, FR-007): ``--window`` sets ``window_start``, so the same 2 h old
    # transcript is historical under 1h and an active person session under 12h. An empty
    # Run has no scoped Dispatch row, so the join guard holds and the transcript is judged.
    _world(env)
    env.sweep_root.transcript("aged-session", (env.now - timedelta(hours=2),))

    payload = _payload(_run(env, "--run", RUN, f"--window={window}"))

    assert payload["window"] == window
    assert _row(payload, "transcript:aged-session")["class"] == class_name
    assert payload["summary"]["historical"] == historical
    assert payload["summary"]["visible"] == 1 - historical
    assert payload["summary"]["counts"]["idle"] == historical


@pytest.mark.parametrize(
    "text",
    [
        "0h",
        "0d",
        "6",
        "6m",
        "7m",
        "-1h",
        "721h",
        "31d",
        "999999999d",
        "10000h",
        "06h",
        "1.5h",
        "6H",
        " 6h",
        "6h ",
        "٦h",  # an Arabic-Indic digit: ASCII digits only
        "",
    ],
    ids=lambda t: repr(t),
)
def test_invalid_windows_exit_2_and_write_nothing(env, text):
    _world(env)

    result = _run(env, "--run", RUN, f"--window={text}")

    _failed(
        result,
        2,
        f"invalid --window value: {text} (use <N>h or <N>d, at most 720h or 30d)\n",
    )
    assert env.orca.calls == []
    _nothing_written(env)


# =========================================================================================
# FR-004: --output and --root
# =========================================================================================


def test_default_output_is_dot_dev_sweeps_under_the_root(env):
    _world(env)

    payload = _payload(_run(env, "--run", RUN))

    assert payload["report_path"] == str(env.sweeps / f"{STEM}.md")


def test_output_below_dot_dev_sweeps_is_accepted(env):
    _world(env)
    archive = env.sweeps / "archive"

    payload = _payload(_run(env, "--run", RUN, "--output", str(archive)))

    assert payload["report_path"] == str(archive / f"{STEM}.md")
    assert _reports(archive) == [f"{STEM}.md"]
    assert _reports(env.sweeps) == []


def test_output_equal_to_dot_dev_sweeps_is_accepted(env):
    _world(env)

    payload = _payload(_run(env, "--run", RUN, "--output", str(env.sweeps)))

    assert payload["report_path"] == str(env.sweeps / f"{STEM}.md")


def _must_be(env) -> str:
    return f"(must be {env.sweeps}/ or a folder below it)"


def test_output_outside_dot_dev_sweeps_exits_2_and_writes_nothing(env):
    _world(env)
    outside = env.tmp / "x"

    result = _run(env, "--run", RUN, "--output", str(outside))

    _failed(result, 2, f"invalid --output: {outside} {_must_be(env)}\n")
    assert not outside.exists()
    _nothing_written(env)
    assert env.orca.calls == []  # an exit-2 check runs before any Orca read


@pytest.mark.parametrize(
    "sub",
    [".dev", ".dev/tasks", ".dev/other", ".dev/tasks/to-do/pkg-a", "."],
    ids=["dev", "dev-tasks", "dev-other", "package-folder", "root"],
)
def test_output_in_dot_dev_but_not_sweeps_exits_2_and_writes_nothing(env, sub):
    _world(env)
    env.sweep_root.package(
        "pkg-a", ledger="ledger\n"
    )  # a real package folder to point at
    target = env.root / sub
    before = sorted(p.relative_to(env.root).as_posix() for p in env.root.rglob("*"))

    result = _run(env, "--run", RUN, "--output", str(target))

    _failed(result, 2, f"invalid --output: {target} {_must_be(env)}\n")
    after = sorted(p.relative_to(env.root).as_posix() for p in env.root.rglob("*"))
    assert after == before  # nothing was created or changed
    assert not env.sweeps.exists()


def test_output_symlink_that_escapes_dot_dev_sweeps_exits_2_and_writes_nothing(env):
    _world(env)
    outside = env.tmp / "elsewhere"
    outside.mkdir()
    env.sweeps.mkdir(parents=True)
    link = env.sweeps / "link"
    link.symlink_to(outside, target_is_directory=True)

    result = _run(env, "--run", RUN, "--output", str(link))

    _failed(result, 2, f"invalid --output: {link} {_must_be(env)}\n")
    assert list(outside.iterdir()) == []
    assert list(env.sweeps.iterdir()) == [link]


def test_symlinked_sweeps_folder_without_output_exits_2_and_writes_nothing(env):
    # CLI-F32: the message names an --output option the operator never passed.
    _world(env)
    outside = env.tmp / "elsewhere"
    outside.mkdir()
    (env.root / ".dev").mkdir()
    env.sweeps.symlink_to(outside, target_is_directory=True)

    result = _run(env, "--run", RUN)

    _failed(result, 2, f"invalid --output: {env.sweeps} {_must_be(env)}\n")
    assert list(outside.iterdir()) == []


def test_output_that_overlaps_an_input_folder_exits_2(env):
    # The input folders are ``.dev/tasks``, ``~/.claude/projects`` and ``orca-tabs``; an
    # output that contains one, or sits inside one, is refused (FR-004).
    base = env.root / ".dev" / "sweeps"
    inside_input = base / "inputs"
    inside_input.mkdir(parents=True)
    with pytest.raises(click.UsageError, match="overlaps the input folder") as caught:
        commands._check_output(None, env.root, (inside_input,))
    assert caught.value.message == (
        f"invalid --output: {base} overlaps the input folder {inside_input}"
    )
    with pytest.raises(click.UsageError, match="overlaps the input folder"):
        commands._check_output(inside_input, env.root, (base,))
    assert (
        commands._check_output(None, env.root, (env.root / ".dev" / "tasks",)) == base
    )


def test_explicit_root_without_dot_git_exits_2(env):
    plain = env.tmp / "plain"
    plain.mkdir()

    result = CliRunner().invoke(
        sweep_group, ["run", "--run", RUN, "--root", str(plain)]
    )

    _failed(result, 2, f"invalid --root: {plain}\n")
    assert env.orca.calls == []


def test_explicit_root_that_is_a_file_exits_2(env):
    afile = env.tmp / "afile"
    afile.write_text("x\n")

    result = CliRunner().invoke(
        sweep_group, ["run", "--run", RUN, "--root", str(afile)]
    )

    _failed(result, 2, f"invalid --root: {afile}\n")


def test_missing_explicit_root_exits_2(env):
    missing = env.tmp / "missing"

    result = CliRunner().invoke(
        sweep_group, ["run", "--run", RUN, "--root", str(missing)]
    )

    _failed(result, 2, f"invalid --root: {missing}\n")
    assert not missing.exists()


def test_explicit_root_with_a_dot_git_file_is_accepted(env):
    _world(env)
    linked = env.sweep_root.worktree(
        "wt-linked"
    )  # its .git is a file, as in a worktree

    result = CliRunner().invoke(
        sweep_group, ["run", "--run", RUN, "--root", str(linked)]
    )
    payload = _payload(result)

    assert payload["scope"]["root"] == str(linked.resolve())
    assert _reports(linked / ".dev" / "sweeps") == [f"{STEM}.md"]


def test_default_root_is_found_by_walking_up_to_a_dot_git_folder(env, monkeypatch):
    _world(env)
    deep = env.root / "a" / "b"
    deep.mkdir(parents=True)
    monkeypatch.chdir(deep)

    payload = _payload(_run(env, "--run", RUN, root=False))

    assert payload["scope"]["root"] == str(env.root)
    assert _reports(env.sweeps) == [f"{STEM}.md"]


def test_default_root_is_found_by_walking_up_to_a_dot_git_file(env, monkeypatch):
    _world(env)
    linked = env.sweep_root.worktree("wt-linked").resolve()
    (linked / "sub").mkdir()
    monkeypatch.chdir(linked / "sub")

    payload = _payload(_run(env, "--run", RUN, root=False))

    assert payload["scope"]["root"] == str(linked)
    assert _reports(linked / ".dev" / "sweeps") == [f"{STEM}.md"]


def test_the_root_walk_accepts_a_dot_git_file_or_folder_and_makes_no_git_call(env):
    deep = env.root / "a"
    deep.mkdir()
    linked = env.sweep_root.worktree("wt-linked").resolve()

    assert commands._find_root(deep) == env.root  # a .git folder
    assert commands._find_root(linked) == linked  # a .git file
    assert env.git.calls == []  # plain stat only: no _git argv


def test_a_walk_that_reaches_the_filesystem_root_exits_2(env, monkeypatch):
    nogit = env.tmp / "nogit" / "deep"
    nogit.mkdir(parents=True)
    monkeypatch.chdir(nogit)
    real = commands._has_git
    # Only folders under tmp can hold a .git here, so a .git on the host cannot change the case.
    monkeypatch.setattr(
        commands, "_has_git", lambda p: real(p) if env.tmp in (p, *p.parents) else False
    )

    result = _run(env, "--run", RUN, root=False)

    _failed(result, 2, f"no git checkout found above {Path.cwd()}\n")
    assert env.git.calls == []
    assert env.orca.calls == []


# =========================================================================================
# FR-005: 4 rows, 2 worktrees, (4/4), and the reconciliation equalities
# =========================================================================================


def _captured_world(env) -> Path:
    """Three captured workers, a second worktree and one active transcript (a person session)."""
    listing = _captured("captured-worker-list.json")["result"]
    workers = listing["workers"][:3]
    shows = {}
    for n in range(1, 6):
        show = _captured(f"captured-worker-show-{n}.json")["result"]
        shows[show["dispatch"]["id"]] = show
    other = env.sweep_root.worktree("wt-a")
    env.orca.respond(_worker_list(CAPTURED_RUN), {**listing, "workers": workers})
    env.orca.respond(
        _task_list_ready(CAPTURED_RUN),
        _captured("captured-task-list-ready.json")["result"],
    )
    env.orca.respond(
        _task_list(CAPTURED_RUN), _captured("captured-task-list.json")["result"]
    )
    for row in workers:
        env.orca.respond(_worker_show(row["dispatchId"]), shows[row["dispatchId"]])
    _ps(env, other)
    # The person session: a transcript that is active inside the 6 h window (M9).
    env.sweep_root.transcript(stamps=(env.now - timedelta(minutes=5),), worktree=other)
    return other


def _section(text: str, heading: str) -> str:
    start = text.index(f"\n{heading}\n") + 1
    nxt = text.find("\n## ", start + len(heading))
    return text[start:] if nxt == -1 else text[start:nxt]


def _table_rows(section: str) -> list[str]:
    lines = [ln for ln in section.splitlines() if ln.startswith("|")]
    return lines[2:]  # drop the header and the separator


def test_fr005_three_workers_two_worktrees_one_person_session(env):
    other = _captured_world(env)

    payload = _payload(_run(env, "--run", CAPTURED_RUN))

    assert len(payload["rows"]) == 4
    assert len(payload["worktrees"]) == 2
    assert payload["scope"]["worktrees"] == 2
    ids = [r["row_id"] for r in payload["rows"]]
    assert sum(1 for i in ids if i.startswith("orca:")) == 3
    assert ids.count("transcript:session-0001") == 1
    assert sorted(w["path"] for w in payload["worktrees"]) == sorted(
        [str(env.root), str(other.resolve())]
    )
    text = Path(payload["report_path"]).read_text("utf-8")
    assert "## Sessions (4/4)" in text
    assert "sessions 4/4 " in text  # the header scope line
    assert len(_table_rows(_section(text, "## Worktrees"))) == 2


def test_fr005_summary_reconciles(env):
    _captured_world(env)

    summary = _payload(_run(env, "--run", CAPTURED_RUN))["summary"]

    assert summary["total"] == summary["visible"] + summary["historical"]
    assert (summary["visible"], summary["historical"], summary["total"]) == (4, 0, 4)
    assert sum(summary["counts"].values()) == summary["total"]
    assert summary["counts"]["idle"] == summary["historical"]
    assert 0 <= summary["bound_reached"] <= summary["visible"]
    assert summary["total_is_lower_bound"] is True


def test_fr005_historical_rows_reconcile_with_visible_ones(env):
    # An empty Run: no scoped Dispatch row, so the join guard holds and transcripts are judged.
    # A transcript 8 h old is historical (idle); a fresh one is an active person session; a
    # ready Task is a visible waiting (b) row.
    _canned(
        env, RUN, ready=[{"id": "task_000000000002", "status": "ready", "spec": "x"}]
    )
    _ps(env)
    env.sweep_root.transcript("old-session", (env.now - timedelta(hours=8),))
    env.sweep_root.transcript("new-session", (env.now - timedelta(minutes=5),))

    payload = _payload(_run(env, "--run", RUN))

    summary = payload["summary"]
    assert (summary["visible"], summary["historical"], summary["total"]) == (2, 1, 3)
    assert summary["total"] == summary["visible"] + summary["historical"]
    assert sum(summary["counts"].values()) == len(payload["rows"]) == 3
    assert summary["counts"]["idle"] == 1
    assert summary["counts"]["person session (active)"] == 1
    assert summary["counts"]["waiting on a person"] == 1
    assert _row(payload, "transcript:old-session")["class"] == "idle"
    assert _row(payload, "transcript:new-session")["class"] == "person session (active)"
    text = Path(payload["report_path"]).read_text("utf-8")
    assert "## Sessions (2/3)" in text  # shown rows exclude the historical one


# =========================================================================================
# FR-017 and NFR-009: the golden JSON v1 key set and types, zero counts, waiting ids
# =========================================================================================

_ROW = {
    "row_id": str,
    "class": str,
    "waiting_kind": (str, type(None)),
    "rule": str,
    "evidence": str,
    "notes": [str],
    "policy": (str, type(None)),
    "person_started": (bool, type(None)),
    "safe_to_close": {
        "terminal": str,
        "worktree": str,
        "reason": (str, type(None)),
    },
}
_WORKTREE = {
    "path": str,
    "status_read": bool,
    "uncommitted": (bool, type(None)),
    "unpushed": (bool, type(None)),
    "dev_tasks_unsaved": (bool, type(None)),
    "frozen": (bool, type(None)),
    "packages": [{"id": str, "location": str, "state": str}],
    "shared_package_ids": [str],
    "removable": str,
    "removable_reason": (str, type(None)),
}
GOLDEN_V1 = {
    "schema_version": int,
    "observed_at": str,
    "collected": {"start": str, "end": str},
    "scope": {"runs": [str], "root": str, "worktrees": int},
    "window": str,
    "orca_available": bool,
    "sources": [
        {
            "name": str,
            "coverage": str,
            "age_seconds": (int, type(None)),
            "unscanned": (str, type(None)),
        }
    ],
    "rows": [_ROW],
    "worktrees": [_WORKTREE],
    "waiting": {"a": [str], "b": [str]},
    "summary": {
        "counts": {name: int for name in CLASSES},
        "bound_reached": int,
        "visible": int,
        "historical": int,
        "total": int,
        "total_is_lower_bound": bool,
    },
    "report_path": str,
}


def _misfits(value: object, spec: object, path: str = "$") -> list[str]:
    """Where ``value`` departs from ``spec``: an exact key set per object, exact types."""
    if isinstance(spec, dict):
        if not isinstance(value, dict):
            return [f"{path}: not an object"]
        out = []
        if set(value) != set(spec):
            out.append(f"{path}: keys {sorted(value)} != {sorted(spec)}")
        for key in set(value) & set(spec):
            out += _misfits(value[key], spec[key], f"{path}.{key}")
        return out
    if isinstance(spec, list):
        if not isinstance(value, list):
            return [f"{path}: not a list"]
        return [
            m for i, v in enumerate(value) for m in _misfits(v, spec[0], f"{path}[{i}]")
        ]
    allowed = spec if isinstance(spec, tuple) else (spec,)
    if type(value) not in allowed:  # exact type: a bool is not an int
        return [
            f"{path}: {type(value).__name__} not in {[t.__name__ for t in allowed]}"
        ]
    return []


def test_golden_v1_top_level_key_set_is_twelve_keys_with_schema_version_1(env):
    _captured_world(env)

    payload = _payload(_run(env, "--run", CAPTURED_RUN))

    assert set(payload) == {
        "schema_version",
        "observed_at",
        "collected",
        "scope",
        "window",
        "orca_available",
        "sources",
        "rows",
        "worktrees",
        "waiting",
        "summary",
        "report_path",
    }
    assert len(payload) == 12
    assert payload["schema_version"] == 1
    assert type(payload["schema_version"]) is int


def test_golden_v1_keys_and_types_at_every_level(env):
    other = _captured_world(env)
    env.sweep_root.package("pkg-a", worktree=other, ledger="ledger\n")

    payload = _payload(_run(env, "--run", CAPTURED_RUN))

    assert _misfits(payload, GOLDEN_V1) == []
    # An empty list proves nothing about its element shape, so each list that holds an
    # object type must hold at least one here.
    assert payload["sources"] and payload["rows"] and payload["worktrees"]
    assert any(w["packages"] for w in payload["worktrees"])
    assert any(r["notes"] for r in payload["rows"])
    assert payload["observed_at"] == "2026-11-08T12:00:00Z"
    assert payload["scope"]["runs"] == [CAPTURED_RUN]
    assert payload["scope"]["root"] == str(env.root)
    assert os.path.isabs(payload["report_path"])
    assert list(payload["summary"]["counts"]) == list(CLASSES)
    assert all(
        r["safe_to_close"]["worktree"] != "yes" for r in payload["rows"]
    )  # FR-012


def test_json_worktree_values_are_exact_and_removable_is_never_yes(env):
    # TST-F1: the JSON ``worktrees[]`` copy of the verdict is checked by value, not by type.
    # The fake git reports a clean branch with no upstream line, so both worktrees were read
    # (``status_read`` true), have no uncommitted change and an unknown push state.
    other = _captured_world(env)

    payload = _payload(_run(env, "--run", CAPTURED_RUN))

    by_path = {w["path"]: w for w in payload["worktrees"]}
    assert sorted(by_path) == sorted([str(env.root), str(other.resolve())])
    for w in by_path.values():
        assert w["status_read"] is True
        assert w["uncommitted"] is False
        assert w["unpushed"] is None
        assert w["removable"] == "no"
        assert w["removable_reason"] == "unpushed branch: no upstream"
    # FR-012 and DESIGN 7.4: the machine-readable verdict is never ``yes``.
    assert all(
        w["removable"] in ("no", "could not determine") for w in payload["worktrees"]
    )


def test_the_type_check_rejects_a_wrong_key_set_and_a_wrong_type():
    good = {"a": 1, "b": [True]}
    spec = {"a": int, "b": [bool]}
    assert _misfits(good, spec) == []
    assert _misfits({"a": 1}, spec) != []  # a missing key
    assert _misfits({**good, "c": 0}, spec) != []  # an extra key
    assert _misfits({"a": True, "b": [True]}, spec) != []  # bool is not int
    assert _misfits({"a": 1, "b": [1]}, spec) != []  # int is not bool in a list


def test_zero_counts_are_present_for_every_class(env):
    _world(env)

    payload = _payload(_run(env, "--run", RUN))

    assert payload["rows"] == []
    counts = payload["summary"]["counts"]
    assert list(counts) == list(CLASSES)  # all eight classes, in CLASSES order
    assert set(counts.values()) == {0}
    assert payload["summary"]["bound_reached"] == 0
    assert (payload["summary"]["visible"], payload["summary"]["total"]) == (0, 0)
    assert payload["waiting"] == {"a": [], "b": []}  # present and empty, never omitted
    assert payload["summary"]["total_is_lower_bound"] is True


def test_waiting_lists_hold_row_ids_only(env):
    dispatch, ready = "ctx_000000000001", "task_000000000002"
    worker = {
        "dispatchId": dispatch,
        "taskId": "task_000000000001",
        "runId": RUN,
        "workerState": "running",
        "dispatchStatus": "dispatched",
    }
    # Waiting (a) comes from a blocked contract the Task names (rule 1): the live
    # agentWait field is not read in Phase 1 (open item 6).
    contract = env.sweep_root.contract(worker_status="blocked", reason="needs a person")
    _canned(
        env,
        RUN,
        workers=[worker],
        shows={dispatch: {"dispatch": {"id": dispatch, "status": "dispatched"}}},
        ready=[{"id": ready, "status": "ready", "spec": "x"}],
        tasks=[{"id": "task_000000000001", "spec": f"Write {contract}"}],
    )
    _ps(env)

    payload = _payload(_run(env, "--run", RUN))

    waiting = payload["waiting"]
    assert waiting == {"a": [f"orca:{dispatch}"], "b": [f"orca:{ready}"]}
    for kind in ("a", "b"):
        assert all(type(i) is str for i in waiting[kind])  # ids, never row objects
        from_rows = [r["row_id"] for r in payload["rows"] if r["waiting_kind"] == kind]
        assert waiting[kind] == from_rows
    assert payload["summary"]["counts"]["waiting on a person"] == 2


# =========================================================================================
# FR-017: report names, two runs with one injected now, earlier reports untouched
# =========================================================================================


def test_report_name_is_the_utc_second_with_the_sweep_suffix(env):
    _world(env)

    payload = _payload(_run(env, "--run", RUN))

    report = Path(payload["report_path"])
    assert report == env.sweeps / "20261108-120000-sweep.md"
    text = report.read_text("utf-8")
    assert text.endswith("Report complete\n")
    assert text.splitlines()[0].startswith("READ ONLY . observed 2026-11-08T12:00:00Z")


def test_two_runs_with_one_now_give_stem_md_and_stem_2_md(env):
    _world(env)

    first = _payload(_run(env, "--run", RUN))
    first_report = Path(first["report_path"])
    before = (
        first_report.read_bytes(),
        first_report.stat().st_ino,
        first_report.stat().st_mtime_ns,
    )
    second = _payload(_run(env, "--run", RUN))

    assert first["report_path"] == str(env.sweeps / f"{STEM}.md")
    assert second["report_path"] == str(env.sweeps / f"{STEM}-2.md")
    assert _reports(env.sweeps) == [f"{STEM}-2.md", f"{STEM}.md"]
    after = (
        first_report.read_bytes(),
        first_report.stat().st_ino,
        first_report.stat().st_mtime_ns,
    )
    assert after == before  # the first report was not rewritten or replaced
    third = _payload(_run(env, "--run", RUN))
    assert third["report_path"] == str(env.sweeps / f"{STEM}-3.md")
    assert _temp_files(env.sweeps) == []


def test_an_existing_earlier_report_is_byte_identical_after_a_new_run(env):
    _world(env)
    env.sweeps.mkdir(parents=True)
    earlier = env.sweeps / f"{STEM}.md"
    earlier.write_bytes(b"an earlier observation\n")
    before = (earlier.read_bytes(), earlier.stat().st_ino, earlier.stat().st_mtime_ns)

    payload = _payload(_run(env, "--run", RUN))

    assert payload["report_path"] == str(env.sweeps / f"{STEM}-2.md")
    assert (
        earlier.read_bytes(),
        earlier.stat().st_ino,
        earlier.stat().st_mtime_ns,
    ) == before
    assert _reports(env.sweeps) == [f"{STEM}-2.md", f"{STEM}.md"]  # never renamed


# =========================================================================================
# FR-018: one test per exit code
# =========================================================================================


def test_exit_code_0_means_the_report_was_published(env):
    _world(env)

    result = _run(env, "--run", RUN)

    payload = _payload(result)  # exit 0, empty stderr, one JSON line
    report = Path(payload["report_path"])
    assert report.read_text("utf-8").endswith("Report complete\n")
    assert _reports(env.sweeps) == [report.name]
    assert os.stat(report).st_nlink == 1  # the temp name is gone
    assert _temp_files(env.sweeps) == []


def test_exit_code_1_is_an_internal_error_with_a_sweep_prefix(env, monkeypatch):
    # An allowlist miss: the seam raises ValueError, which ``run`` maps to exit 1.
    def collect_with_a_forbidden_argv(ctx, runs, root, budget):
        probes._orca("check", timeout=1.0)

    monkeypatch.setattr(probes, "collect", collect_with_a_forbidden_argv)

    result = _run(env, "--run", RUN)

    _failed(result, 1, "[sweep collect] orca arguments are not allowed: ('check',)\n")
    _nothing_written(env)  # nothing reached the filesystem


def test_exit_code_2_is_a_usage_error(env):
    result = _run(env, "--run", "r;x")

    _failed(result, 2, "invalid --run value: r;x\n")
    _nothing_written(env)


@pytest.mark.parametrize(
    ("stage", "target", "name"),
    [
        ("collect", probes, "collect"),
        ("classify", commands, "classify_all"),
        ("render", commands, "render"),
    ],
)
def test_an_internal_error_in_each_pure_stage_exits_1_and_writes_nothing(
    env, monkeypatch, stage, target, name
):
    _world(env)
    monkeypatch.setattr(target, name, _raise_always(RuntimeError("boom")))

    result = _run(env, "--run", RUN)

    _failed(result, 1, f"[sweep {stage}] boom\n")
    _nothing_written(env)


def _raise_always(exc: BaseException):
    def fail(*args, **kwargs):
        raise exc

    return fail


# =========================================================================================
# G-1, DESIGN section 3: publication failures
# =========================================================================================


def test_publish_link_failure_exits_1_with_no_report_and_no_temp_file(env, monkeypatch):
    _world(env)
    env.sweeps.mkdir(parents=True)
    earlier = env.sweeps / f"{STEM}.md"
    earlier.write_bytes(b"an earlier observation\n")
    _fail_in_commands(
        monkeypatch,
        commands.os,
        "link",
        _raise(OSError(errno.EPERM, "Operation not permitted")),
    )

    result = _run(env, "--run", RUN)

    # CLI-F3: a publish line is printed as the OSError text, brackets unescaped.
    _failed(
        result,
        1,
        "[sweep publish] cannot link report: [Errno 1] Operation not permitted\n",
    )
    assert _reports(env.sweeps) == [
        f"{STEM}.md"
    ]  # only the earlier one, byte-identical
    assert earlier.read_bytes() == b"an earlier observation\n"
    assert _temp_files(env.sweeps) == []  # this run's temp file was removed


def test_publish_link_failure_and_unlink_failure_name_the_left_temp_file(
    env, monkeypatch
):
    _world(env)
    _fail_in_commands(
        monkeypatch,
        commands.os,
        "link",
        _raise(OSError(errno.EPERM, "Operation not permitted")),
    )
    _fail_in_commands(
        monkeypatch,
        commands.os,
        "unlink",
        _raise(OSError(errno.EACCES, "Permission denied")),
    )

    result = _run(env, "--run", RUN)

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == (
        "[sweep publish] cannot link report: [Errno 1] Operation not permitted\n"
        f"[sweep publish] left temp file {_temp_path(env)}\n"
    )
    assert _reports(env.sweeps) == []
    assert _temp_files(env.sweeps) == [
        _temp_path(env).name
    ]  # its own, dot-prefixed temp file


def test_publish_full_disk_on_write_exits_1_and_removes_the_temp_file(env, monkeypatch):
    _world(env)
    _fail_in_commands(
        monkeypatch,
        commands.os,
        "write",
        _raise(OSError(errno.ENOSPC, "No space left on device")),
    )

    result = _run(env, "--run", RUN)

    _failed(result, 1, "[sweep publish] [Errno 28] No space left on device\n")
    assert _reports(env.sweeps) == []
    assert _temp_files(env.sweeps) == []


def test_publish_write_failure_and_unlink_failure_name_the_left_temp_file(
    env, monkeypatch
):
    _world(env)
    _fail_in_commands(
        monkeypatch,
        commands.os,
        "write",
        _raise(OSError(errno.ENOSPC, "No space left on device")),
    )
    _fail_in_commands(
        monkeypatch,
        commands.os,
        "unlink",
        _raise(OSError(errno.EACCES, "Permission denied")),
    )

    result = _run(env, "--run", RUN)

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == (
        "[sweep publish] [Errno 28] No space left on device\n"
        f"[sweep publish] left temp file {_temp_path(env)}\n"
    )
    assert _reports(env.sweeps) == []


def test_publish_with_every_name_from_stem_to_stem_99_taken_exits_1(env):
    _world(env)
    env.sweeps.mkdir(parents=True)
    names = [f"{STEM}.md"] + [f"{STEM}-{n}.md" for n in range(2, 100)]
    for number, name in enumerate(names):
        (env.sweeps / name).write_bytes(f"earlier {number}\n".encode())

    result = _run(env, "--run", RUN)

    _failed(result, 1, f"[sweep publish] report name space exhausted: {env.sweeps}\n")
    assert sorted(os.listdir(env.sweeps)) == sorted(names)  # no -100, no temp file left
    for number, name in enumerate(names):
        assert (env.sweeps / name).read_bytes() == f"earlier {number}\n".encode()


def test_publish_takes_stem_99_when_stem_to_stem_98_are_taken(env):
    _world(env)
    env.sweeps.mkdir(parents=True)
    taken = [f"{STEM}.md"] + [f"{STEM}-{n}.md" for n in range(2, 99)]
    for name in taken:
        (env.sweeps / name).write_bytes(b"earlier\n")

    payload = _payload(_run(env, "--run", RUN))

    assert payload["report_path"] == str(env.sweeps / f"{STEM}-99.md")  # the last name
    assert _reports(env.sweeps) == sorted([*taken, f"{STEM}-99.md"])
    assert _temp_files(env.sweeps) == []


def test_publish_with_an_existing_temp_name_exits_1_and_leaves_that_file_alone(env):
    _world(env)
    env.sweeps.mkdir(parents=True)
    temp = _temp_path(env)
    temp.write_bytes(b"not this run's file\n")

    result = _run(env, "--run", RUN)

    _failed(result, 1, f"[sweep publish] temp file exists: {temp}\n")
    assert temp.read_bytes() == b"not this run's file\n"  # not touched, not removed
    assert _reports(env.sweeps) == []


def test_publish_makedirs_failure_exits_1_and_writes_nothing(env, monkeypatch):
    _world(env)
    _fail_in_commands(
        monkeypatch,
        commands.os,
        "makedirs",
        _raise(OSError(errno.EACCES, "Permission denied")),
    )

    result = _run(env, "--run", RUN)

    _failed(result, 1, "[sweep publish] [Errno 13] Permission denied\n")
    _nothing_written(env)


def test_publish_output_path_that_escapes_after_makedirs_exits_1(env, monkeypatch):
    _world(env)
    outside = env.tmp / "elsewhere"
    outside.mkdir()
    target = env.sweeps / "sub"

    def makedirs_then_swap_in_a_symlink(real, path, *args, **kwargs):
        real(path, *args, **kwargs)
        os.rmdir(path)  # the folder is replaced after the usage checks passed
        os.symlink(outside, path, target_is_directory=True)

    _fail_in_commands(
        monkeypatch, commands.os, "makedirs", makedirs_then_swap_in_a_symlink
    )

    result = _run(env, "--run", RUN, "--output", str(target))

    _failed(result, 1, f"[sweep publish] output dir escaped {env.sweeps}/\n")
    assert list(outside.iterdir()) == []  # nothing written through the link
    assert _reports(env.sweeps) == [] and _temp_files(env.sweeps) == []


def test_publish_print_failure_after_the_commit_point_leaves_one_complete_report(
    env, monkeypatch
):
    _world(env)

    def echo_fails_on_stdout(real, *args, **kwargs):
        if kwargs.get("err"):
            return real(*args, **kwargs)  # the stderr line still prints
        raise OSError("print failed")

    _fail_in_commands(monkeypatch, commands.click, "echo", echo_fails_on_stdout)

    result = _run(env, "--run", RUN)

    # CLI-F33: the exit-1 handler prints the sanitized exception text with no class name.
    _failed(result, 1, "[sweep output] print failed\n")
    assert _reports(env.sweeps) == [f"{STEM}.md"]
    assert (env.sweeps / f"{STEM}.md").read_text("utf-8").endswith("Report complete\n")
    assert _temp_files(env.sweeps) == []


def test_publish_unlink_failure_after_a_successful_link_leaves_one_complete_report(
    env, monkeypatch
):
    _world(env)
    linked: list[object] = []

    def link_and_note(real, src, dst, *args, **kwargs):
        real(src, dst, *args, **kwargs)
        linked.append(dst)  # recorded only after the link succeeded: the commit point

    def unlink_fails_after_the_link(real, path, *args, **kwargs):
        if linked:
            raise OSError(errno.EACCES, "Permission denied")
        return real(path, *args, **kwargs)

    _fail_in_commands(monkeypatch, commands.os, "link", link_and_note)
    _fail_in_commands(monkeypatch, commands.os, "unlink", unlink_fails_after_the_link)

    result = _run(env, "--run", RUN)

    temp = _temp_path(env)
    _failed(result, 1, f"[sweep publish] could not remove temp file {temp}\n")
    assert len(linked) == 1  # the unlink was attempted after a successful link
    assert _reports(env.sweeps) == [f"{STEM}.md"]  # exactly one complete report
    report = env.sweeps / f"{STEM}.md"
    assert report.read_text("utf-8").endswith("Report complete\n")
    # Two names for one file: the temp file stays, and it holds the same bytes.
    assert _temp_files(env.sweeps) == [temp.name]
    assert temp.read_bytes() == report.read_bytes()
    assert os.stat(report).st_nlink == 2
