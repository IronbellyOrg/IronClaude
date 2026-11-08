"""Tests for the ``superclaude issue-watch`` command group, part A.

Covers the group and its registration, the config path (DF-13), ``check-config``,
``once`` and ``status`` (design 4.1, 4.3 and 10.2). Everything runs in process
with Click's ``CliRunner``. ``HOME`` and ``XDG_STATE_HOME`` point into
``tmp_path`` for every test, ``/proc/self/mountinfo`` is replaced by a fixed
text, and ``SubprocessRunner.run`` raises, so no real process can start.

Only ``result.output`` and ``result.exit_code`` are read: with Click 8.1 the
default runner mixes stderr into the output, and Click 8.2 and later returns the
interleaved stdout and stderr in ``output``. The stderr audit fallback is
therefore found as the JSON line in the output.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import shutil
import socket
import stat
import sys
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.issue_watch import audit, cli, cycle, launch, record
from superclaude.cli.issue_watch import runner as runner_mod
from superclaude.cli.issue_watch.cli import issue_watch_group
from superclaude.cli.issue_watch.record import Entry
from superclaude.cli.main import main

from .conftest import (
    CYCLE_NOW,
    FIXED_NOW,
    FailingStore,
    FakeClock,
    make_config,
    make_deps,
)
from .conftest import result as command_result

# The real assembly, taken before the autouse fixture below replaces it, so one
# test can run it (Gate C fix C-12).
_REAL_BUILD_DEPS = cli.build_deps

EXPECTED_COMMANDS = ["check-config", "init-state", "once", "reset", "status"]
LOCAL_MOUNTINFO = "1 0 0:1 / / rw - ext4 /dev/sda1 rw\n"
NFS_MOUNTINFO = "1 0 0:1 / / rw - nfs4 server:/export rw\n"
NOW = CYCLE_NOW  # 2026-11-07T13:00:00Z
_DROP = object()

# ==============================================================================
# Helpers and fixtures
# ==============================================================================


@pytest.fixture(autouse=True)
def runner_calls(tmp_path, monkeypatch) -> list[tuple[str, ...]]:
    """Isolate HOME, XDG and mountinfo; make any real subprocess call a failure.

    Returns the list of argvs that reached ``SubprocessRunner.run``; every test
    that runs a command also fails on the ``AssertionError`` the guard raises.
    """
    (tmp_path / "home").mkdir()
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg"))
    monkeypatch.setattr(cycle, "_read_mountinfo", lambda: LOCAL_MOUNTINFO)
    calls: list[tuple[str, ...]] = []

    def refuse(self, argv, timeout, *, cwd=None):
        calls.append(tuple(argv))
        raise AssertionError(f"a real subprocess call was attempted: {argv!r}")

    def no_deps(config):
        raise AssertionError("build_deps was called")

    monkeypatch.setattr(runner_mod.SubprocessRunner, "run", refuse)
    monkeypatch.setattr(cli, "build_deps", no_deps)
    return calls


@pytest.fixture
def config(tmp_path) -> cycle.Config:
    """A valid enabled config whose paths are all inside ``tmp_path``."""
    return make_config(tmp_path)


def write_config(path: Path, config: cycle.Config, **over: object) -> Path:
    """Write ``config`` as the JSON file; ``over`` replaces keys, ``_DROP`` removes."""
    raw: dict[str, object] = {
        "schema_version": 1,
        "enabled": config.enabled,
        "project_id": config.project_id,
        "worktree": str(config.worktree),
        "approvers_file": str(config.approvers_file),
        "state_dir": str(config.state_dir),
    }
    raw.update(over)
    raw = {k: v for k, v in raw.items() if v is not _DROP}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(raw), encoding="utf-8")
    return path


@pytest.fixture
def default_config_file(tmp_path, config) -> Path:
    """The config at the default path under the monkeypatched HOME."""
    return write_config(tmp_path / "home/.config/superclaude/issue-watch.json", config)


@pytest.fixture
def config_file(tmp_path, config) -> Path:
    """A valid config file at an explicit path."""
    return write_config(tmp_path / "explicit.json", config)


def run(*args: str):
    """Invoke ``issue-watch <args>``; anything but a clean exit is a failure."""
    result = CliRunner().invoke(issue_watch_group, list(args))
    assert result.exception is None or isinstance(result.exception, SystemExit), repr(
        result.exception
    )
    return result


def snapshot(root: Path) -> dict[str, tuple]:
    """Mode, mtime, size and content hash of every path under ``root``."""
    snap: dict[str, tuple] = {}
    for path in [root, *sorted(root.rglob("*"))]:
        st = path.lstat()
        digest = None
        if stat.S_ISREG(st.st_mode):
            try:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError:
                digest = "unreadable"
        snap[str(path.relative_to(root))] = (
            st.st_mode,
            st.st_mtime_ns,
            st.st_size,
            digest,
        )
    return snap


def run_readonly(tmp_path: Path, *args: str):
    """As ``run``, and fail if any path under ``tmp_path`` changed."""
    before = snapshot(tmp_path)
    result = run(*args)
    assert snapshot(tmp_path) == before
    return result


def fallback_lines(output: str) -> list[dict]:
    """The stderr audit fallback lines (JSON objects) found in ``output``."""
    return [json.loads(ln) for ln in output.splitlines() if ln.startswith("{")]


def assert_fallback(output: str, reason: str) -> None:
    """Exactly one fallback line for ``reason`` with exit 2 and the fixed key set."""
    (line,) = fallback_lines(output)
    assert set(line) == {"kind", "ts", "host", "exit", "reason"}
    assert (line["kind"], line["exit"], line["reason"]) == ("cycle", 2, reason)
    assert any(ln.startswith(f"issue-watch: {reason}: ") for ln in output.splitlines())


def audit_lines(state_dir: Path) -> list[dict]:
    """Every line of ``audit.jsonl``, parsed one by one."""
    path = state_dir / "audit.jsonl"
    if not path.exists():
        return []
    return [json.loads(ln) for ln in path.read_text("utf-8").splitlines()]


def entry(n: int, state: str, updated_at: datetime, **over: object) -> Entry:
    """A valid ``Entry``; ``launches`` 1 needs ``consumed_at`` and ``pending_at``."""
    fields: dict[str, object] = {
        "issue": n,
        "state": state,
        "attempts": 1,
        "launches": 0,
        "operation_id": None,
        "approver_id": 1001,
        "approval_event_id": 2,
        "approved_at": NOW - timedelta(days=2),
        "launch_cwd": None,
        "launch_login": None,
        "launch_account_id": None,
        "consumed_at": None,
        "pending_at": None,
        "created_at": NOW - timedelta(days=2),
        "updated_at": updated_at,
        "lease_expires_at": None,
        "last_reason": None,
    }
    fields.update(over)
    return Entry(**fields)  # type: ignore[arg-type]


def seed_store(
    config: cycle.Config,
    *,
    last_completed: datetime | None = None,
    next_permitted: datetime | None = None,
    entries: tuple[Entry, ...] = (),
) -> record.FileStore:
    """Create the state directory and store, then replace the interesting fields."""
    store = record.init_state(config.state_dir, NOW - timedelta(days=3))
    store.save(
        replace(
            store.load(),
            last_completed_cycle_at=last_completed,
            next_permitted_at=next_permitted,
            entries={e.issue: e for e in entries},
        )
    )
    return store


def retry_argv(orca: str, n: int, cwd: str, op: str) -> list[str]:
    """The full original 12-element launch argv with the retry flag before --json."""
    return [
        orca,
        "agent",
        "launch",
        "--agent",
        "claude",
        "--worktree",
        f"path:{cwd}",
        "--surface",
        "terminal",
        "--prompt",
        f"/sc:issue --claim {n}",
        "--retry-launch",
        op,
        "--json",
    ]


def set_path(monkeypatch, tmp_path: Path, *names: str) -> Path:
    """PATH holds only ``tmp_path/bin``, with an executable file per name."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    for name in names:
        exe = bin_dir / name
        exe.write_text("#!/bin/sh\n", encoding="utf-8")
        exe.chmod(0o755)
    monkeypatch.setenv("PATH", str(bin_dir))
    return bin_dir


@pytest.fixture
def fixed_clock(monkeypatch) -> FakeClock:
    """``status`` and the other verbs read time from a clock fixed at ``NOW``."""
    monkeypatch.setattr(cycle, "SystemClock", lambda: FakeClock(NOW))
    return FakeClock(NOW)


# ==============================================================================
# The group (DF-06)
# ==============================================================================


def _listed(output: str) -> list[str]:
    """Command names in a Click ``Commands:`` section (two-space indent only)."""
    section = output.split("Commands:", 1)[1]
    return [
        m.group(1) for ln in section.splitlines() if (m := re.match(r"^  (\S+)", ln))
    ]


def test_the_group_lists_exactly_the_five_commands__df06():
    result = CliRunner().invoke(main, ["issue-watch", "--help"])
    assert result.exit_code == 0, result.output
    assert sorted(_listed(result.output)) == EXPECTED_COMMANDS
    assert len(_listed(result.output)) == 5
    direct = CliRunner().invoke(issue_watch_group, ["--help"])
    assert direct.exit_code == 0
    assert _listed(direct.output) == _listed(result.output)
    assert sorted(issue_watch_group.commands) == EXPECTED_COMMANDS
    top = CliRunner().invoke(main, ["--help"])
    assert top.exit_code == 0
    assert "issue-watch" in top.output


def test_the_help_examples_keep_one_line_each():
    result = CliRunner().invoke(issue_watch_group, ["--help"])
    lines = [ln.strip() for ln in result.output.splitlines()]
    block = [
        "superclaude issue-watch check-config",
        "superclaude issue-watch init-state",
        "superclaude issue-watch once --dry-run",
        "superclaude issue-watch status --json",
    ]
    at = lines.index(block[0])
    assert lines[at : at + 4] == block


@pytest.mark.parametrize("verb", EXPECTED_COMMANDS)
def test_every_command_takes_the_shared_config_option(verb):
    result = CliRunner().invoke(issue_watch_group, [verb, "--help"])
    assert result.exit_code == 0
    assert "--config" in result.output
    assert "~/.config/superclaude/issue-watch.json" in result.output


# ==============================================================================
# The config path (DF-13)
# ==============================================================================


def test_check_config_without_config_reads_the_default_path_under_home__df13(
    tmp_path, default_config_file
):
    result = run("check-config")
    assert result.exit_code == 0, result.output
    assert result.output.startswith("configuration is valid\n")


def test_a_passed_config_with_a_tilde_is_expanded__df13(tmp_path, config):
    write_config(tmp_path / "home/custom.json", config)
    result = run("check-config", "--config", "~/custom.json")
    assert result.exit_code == 0, result.output


def test_a_tilde_inside_the_json_is_not_expanded__df13(tmp_path, config):
    path = write_config(tmp_path / "bad.json", config, worktree="~/worktree")
    result = run("check-config", "--config", str(path))
    assert result.exit_code == 2
    assert_fallback(result.output, "config_invalid")


def test_a_missing_default_config_is_exit_2(tmp_path):
    result = run("check-config")
    assert result.exit_code == 2
    assert_fallback(result.output, "config_invalid")


# ==============================================================================
# check-config
# ==============================================================================


def test_check_config_prints_the_mtime_and_count_and_writes_nothing(
    tmp_path, config, config_file
):
    """AC-17, FR-026: check-config exits 0, prints its summary and writes nothing."""
    config.approvers_file.write_text("7654321\n# a note\n\n1001\n7654321\n", "utf-8")
    stamp = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc).timestamp()
    os.utime(config.approvers_file, (stamp, stamp))
    result = run_readonly(tmp_path, "check-config", "--config", str(config_file))
    assert result.exit_code == 0
    assert result.output == (
        "configuration is valid\n"
        f"state_dir: {config.state_dir}\n"
        "approvers_file mtime: 2026-01-02T03:04:05Z\n"
        "approvers_file entries: 2\n"
    )
    assert "7654321" not in result.output  # nothing else about the file
    assert not config.state_dir.exists()


def _bad_config(tmp_path, config, config_file):
    write_config(config_file, config, project_id="not-a-project")


def _bad_line(tmp_path, config, config_file):
    config.approvers_file.write_text("1001\nnot-an-id\n", "utf-8")


def _group_writable(tmp_path, config, config_file):
    config.approvers_file.chmod(0o620)


def _empty_approvers(tmp_path, config, config_file):
    config.approvers_file.write_text("# only a comment\n", "utf-8")


def _missing_approvers(tmp_path, config, config_file):
    config.approvers_file.unlink()


def _missing_worktree(tmp_path, config, config_file):
    config.worktree.rmdir()


@pytest.mark.parametrize(
    ("break_it", "reason"),
    [
        (_bad_config, "config_invalid"),
        (_bad_line, "approvers_invalid"),
        (_group_writable, "approvers_invalid"),
        (_empty_approvers, "approvers_invalid"),
        (_missing_approvers, "approvers_invalid"),
        (_missing_worktree, "worktree_invalid"),
    ],
)
def test_check_config_exits_2_for_an_invalid_setup(
    tmp_path, config, config_file, break_it, reason
):
    break_it(tmp_path, config, config_file)
    result = run_readonly(tmp_path, "check-config", "--config", str(config_file))
    assert result.exit_code == 2
    assert "configuration is valid" not in result.output
    assert_fallback(result.output, reason)


def test_check_config_exits_2_on_an_unsupported_platform(
    tmp_path, config_file, monkeypatch
):
    monkeypatch.setattr(sys, "platform", "darwin")
    result = run_readonly(tmp_path, "check-config", "--config", str(config_file))
    assert result.exit_code == 2
    assert_fallback(result.output, "platform_unsupported")


def test_check_config_exits_2_for_a_deny_listed_filesystem__df52(
    tmp_path, config_file, monkeypatch
):
    monkeypatch.setattr(cycle, "_read_mountinfo", lambda: NFS_MOUNTINFO)
    result = run_readonly(tmp_path, "check-config", "--config", str(config_file))
    assert result.exit_code == 2
    assert_fallback(result.output, "config_invalid")
    assert "network filesystem" in result.output


# ==============================================================================
# once
# ==============================================================================


@pytest.mark.parametrize(
    ("code", "reason"),
    [
        (0, "disabled"),
        (2, "origin_mismatch"),
        (3, "gh_auth_failed"),
        (4, "truncated"),
        (5, "rate_limited"),
        (6, "store_invalid"),
        (7, "launch_unknown"),
        (75, "lock_held"),
    ],
)
def test_once_exits_with_the_exit_code_of_the_cycle(
    config, config_file, monkeypatch, code, reason
):
    """AC-17, FR-026: once exits with the code the cycle returns (section 4)."""
    seen: list[tuple[object, bool]] = []
    built: list[cycle.Config] = []
    sentinel = object()

    def fake_build(cfg):
        built.append(cfg)
        return sentinel

    def fake_cycle(deps, dry_run):
        seen.append((deps, dry_run))
        return cycle.CycleResult(exit_code=code, reason=reason, cycle_id="0" * 32)

    monkeypatch.setattr(cli, "build_deps", fake_build)
    monkeypatch.setattr(cycle, "run_cycle", fake_cycle)
    result = run("once", "--config", str(config_file))
    assert result.exit_code == code
    assert result.output == f"cycle: {reason}\nexit: {code}\n"
    assert built == [config]
    assert seen == [(sentinel, False)]


def test_once_dry_run_passes_the_flag_and_prints_probe_and_would_launch(
    config_file, monkeypatch
):
    seen: list[bool] = []

    def fake_cycle(deps, dry_run):
        seen.append(dry_run)
        return cycle.CycleResult(
            exit_code=0,
            reason="not_approved",
            cycle_id="0" * 32,
            would_launch=42,
            probe="skipped",
        )

    monkeypatch.setattr(cli, "build_deps", lambda cfg: object())
    monkeypatch.setattr(cycle, "run_cycle", fake_cycle)
    result = run("once", "--dry-run", "--config", str(config_file))
    assert result.exit_code == 0
    assert result.output == (
        "cycle: not_approved\nexit: 0\nprobe: skipped\nwould_launch: 42\n"
    )
    assert seen == [True]


def test_once_without_dry_run_prints_no_probe_or_would_launch_line(
    config_file, monkeypatch
):
    monkeypatch.setattr(cli, "build_deps", lambda cfg: object())
    monkeypatch.setattr(
        cycle,
        "run_cycle",
        lambda deps, dry_run: cycle.CycleResult(
            exit_code=0,
            reason="launched",
            cycle_id="0" * 32,
            launched_issue=42,
            would_launch=42,
            probe="skipped",
        ),
    )
    result = run("once", "--config", str(config_file))
    assert result.exit_code == 0
    assert result.output == "cycle: launched\nexit: 0\n"


def test_once_on_a_config_error_writes_the_fallback_and_exits_2(
    tmp_path, config, monkeypatch, runner_calls
):
    path = write_config(tmp_path / "bad.json", config, project_id=_DROP)
    monkeypatch.setattr(
        cycle, "run_cycle", lambda *a: pytest.fail("run_cycle must not run")
    )
    result = run("once", "--config", str(path))
    assert result.exit_code == 2
    assert_fallback(result.output, "config_invalid")
    assert runner_calls == []


def test_once_runs_a_real_cycle_over_the_fakes_when_not_enabled(
    tmp_path, tmp_state, monkeypatch
):
    config = make_config(tmp_path, enabled=False)
    path = write_config(tmp_path / "off.json", config)
    deps = make_deps(tmp_path, tmp_state, config=config)
    monkeypatch.setattr(cli, "build_deps", lambda cfg: deps)
    before = (tmp_state.state_dir / "dispatch.json").read_bytes()
    result = run("once", "--config", str(path))
    assert result.exit_code == 0
    assert result.output == "cycle: not_enabled\nexit: 0\n"
    assert deps.runner.calls == []
    assert deps.launcher.calls == []
    assert (tmp_state.state_dir / "dispatch.json").read_bytes() == before
    (line,) = audit_lines(tmp_state.state_dir)
    assert (line["kind"], line["reason"], line["exit"], line["dry_run"]) == (
        "cycle",
        "not_enabled",
        0,
        False,
    )
    assert line["host"] == "test-host"


def test_once_dry_run_runs_a_real_cycle_and_never_launches(
    tmp_path, tmp_state, gh_world, monkeypatch
):
    world = gh_world()
    world.issue(9)
    path = write_config(tmp_path / "on.json", world.config)
    deps = world.deps(tmp_path, tmp_state)
    monkeypatch.setattr(cli, "build_deps", lambda cfg: deps)
    before = (tmp_state.state_dir / "dispatch.json").read_bytes()
    result = run("once", "--dry-run", "--config", str(path))
    assert result.exit_code == 0, result.output
    first, *rest = result.output.splitlines()
    assert first.startswith("cycle: ")
    assert rest == ["exit: 0", "probe: skipped", "would_launch: 9"]
    assert deps.launcher.calls == []
    assert (tmp_state.state_dir / "dispatch.json").read_bytes() == before
    assert audit_lines(tmp_state.state_dir)[-1]["dry_run"] is True


# -- build_deps: the one production assembly of Deps (DF-45, Gate C fix C-12) ------


def test_build_deps_wires_the_real_dependencies_from_the_config(config, monkeypatch):
    seen: list[tuple[list[str], float, str | None]] = []

    def record_run(self, argv, timeout, *, cwd=None):
        seen.append((list(argv), timeout, cwd))
        return command_result(stdout="{}")

    monkeypatch.setattr(runner_mod.SubprocessRunner, "run", record_run)
    deps = _REAL_BUILD_DEPS(config)
    assert deps.config is config
    assert isinstance(deps.runner, runner_mod.SubprocessRunner)
    assert isinstance(deps.store, record.FileStore)
    assert deps.store.state_dir == config.state_dir
    assert isinstance(deps.audit, audit.AuditLog)
    assert deps.audit.state_dir == config.state_dir
    assert deps.audit.path == config.state_dir / "audit.jsonl"
    assert isinstance(deps.clock, cycle.SystemClock)
    assert deps.which is shutil.which
    assert deps.host == socket.gethostname()
    # The launcher is the Orca launcher and runs through a SubprocessRunner, with
    # the worktree as the working directory (the one call that passes cwd).
    assert isinstance(deps.launcher, launch.OrcaLauncher)
    deps.launcher.launch("orca-x", config.worktree, "/sc:issue --claim 9", 30.0)
    assert seen == [
        (
            launch.launch_argv("orca-x", config.worktree, "/sc:issue --claim 9"),
            30.0,
            str(config.worktree),
        )
    ]


# -- once: an unexpected exception (Gate C fix C-3, C-7) ---------------------------


def _once_over(tmp_path, tmp_state, gh_world, monkeypatch, store_error=None):
    """An idle ``once`` whose first (final) save raises ``store_error``."""
    world = gh_world()
    path = write_config(tmp_path / "on.json", world.config)
    deps = world.deps(tmp_path, tmp_state)
    if store_error is not None:
        deps = replace(
            deps, store=FailingStore(tmp_state, fail_saves=(1,), error=store_error)
        )
    monkeypatch.setattr(cli, "build_deps", lambda cfg: deps)
    return path


def test_once_turns_an_unexpected_exception_into_exit_1_and_one_fallback_line(
    tmp_path, tmp_state, gh_world, monkeypatch
):
    secret = "issue title that must never reach the output"  # pragma: allowlist secret
    path = _once_over(tmp_path, tmp_state, gh_world, monkeypatch, RuntimeError(secret))
    before = (tmp_state.state_dir / "dispatch.json").read_bytes()
    result = run("once", "--config", str(path))
    assert result.exit_code == 1
    (fallback,) = fallback_lines(result.output)
    assert set(fallback) == {"kind", "ts", "host", "exit", "reason"}
    assert (fallback["kind"], fallback["exit"], fallback["reason"]) == (
        "cycle",
        1,
        "cycle_crashed",
    )
    assert "issue-watch: cycle_crashed: RuntimeError" in result.output.splitlines()
    assert secret not in result.output  # only the class name is printed
    assert "Traceback" not in result.output
    assert audit_lines(tmp_state.state_dir) == []
    assert (tmp_state.state_dir / "dispatch.json").read_bytes() == before
    with tmp_state.lock():  # the lock was released
        pass


@pytest.mark.parametrize("extra", [(), ("--dry-run",)], ids=["real", "dry_run"])
def test_once_exits_2_on_an_unsupported_platform_and_runs_nothing__design_4_1(
    tmp_path, config_file, monkeypatch, extra
):
    """Design line 69: `once` refuses another platform, as `check-config` does."""
    calls: list[str] = []
    monkeypatch.setattr(sys, "platform", "darwin")
    monkeypatch.setattr(cli, "build_deps", lambda cfg: calls.append("build_deps"))
    monkeypatch.setattr(
        cycle, "run_cycle", lambda deps, dry_run: calls.append("run_cycle")
    )
    result = run_readonly(tmp_path, "once", *extra, "--config", str(config_file))
    assert result.exit_code == 2
    assert_fallback(result.output, "platform_unsupported")
    assert calls == []  # no dependency was built and no cycle ran


def test_once_turns_a_build_deps_failure_into_exit_1(
    tmp_path, config_file, monkeypatch
):
    def broken(cfg):
        raise RuntimeError("no hostname")

    monkeypatch.setattr(cli, "build_deps", broken)
    result = run("once", "--config", str(config_file))
    assert result.exit_code == 1
    (fallback,) = fallback_lines(result.output)
    assert (fallback["exit"], fallback["reason"]) == (1, "cycle_crashed")


@pytest.mark.parametrize(
    "error",
    [SystemExit(42), KeyboardInterrupt()],
    ids=["SystemExit", "KeyboardInterrupt"],
)
def test_once_lets_system_exit_and_keyboard_interrupt_through(
    tmp_path, tmp_state, gh_world, monkeypatch, capsys, error
):
    path = _once_over(tmp_path, tmp_state, gh_world, monkeypatch, error)
    with pytest.raises(type(error)) as caught:
        cli.once_command.callback(dry_run=False, config_path=path)
    assert caught.value is error
    assert "cycle_crashed" not in capsys.readouterr().err
    assert audit_lines(tmp_state.state_dir) == []


def test_once_exits_with_the_code_a_system_exit_carries(
    tmp_path, tmp_state, gh_world, monkeypatch
):
    path = _once_over(tmp_path, tmp_state, gh_world, monkeypatch, SystemExit(42))
    result = run("once", "--config", str(path))
    assert result.exit_code == 42
    assert "cycle_crashed" not in result.output


def test_once_prints_exit_6_when_the_final_save_fails(
    tmp_path, tmp_state, gh_world, monkeypatch
):
    path = _once_over(tmp_path, tmp_state, gh_world, monkeypatch, OSError("disk full"))
    result = run("once", "--config", str(path))
    assert result.exit_code == 6
    assert "cycle: state_dir_unwritable" in result.output.splitlines()
    assert "exit: 6" in result.output.splitlines()
    (fallback,) = fallback_lines(result.output)
    assert (fallback["kind"], fallback["exit"], fallback["reason"]) == (
        "cycle",
        6,
        "state_dir_unwritable",
    )
    assert audit_lines(tmp_state.state_dir) == []
    assert tmp_state.load().last_completed_cycle_at is None


# ==============================================================================
# status
# ==============================================================================

_CWD = "/srv/worktree"


def seed_rich_store(config: cycle.Config) -> None:
    """Two unknown, one stale abandoned and one claimed entry; DISABLED present."""
    seed_store(
        config,
        last_completed=NOW - timedelta(seconds=120),
        next_permitted=NOW + timedelta(minutes=10),
        entries=(
            entry(
                5,
                "unknown",
                NOW - timedelta(hours=25),
                launches=1,
                consumed_at=NOW - timedelta(hours=25),
                pending_at=NOW - timedelta(hours=25),
                operation_id="op:5.abc",
                launch_cwd=_CWD,
                last_reason="launch_unknown",
            ),
            entry(
                6,
                "abandoned",
                NOW - timedelta(hours=25),
                last_reason="pending_orphan",
            ),
            entry(
                7,
                "claimed",
                NOW - timedelta(minutes=30),
                launches=1,
                consumed_at=NOW - timedelta(hours=1),
                pending_at=NOW - timedelta(hours=1),
                last_reason="claimed",
            ),
            entry(
                8,
                "unknown",
                NOW - timedelta(hours=23),
                launches=1,
                consumed_at=NOW - timedelta(hours=23),
                pending_at=NOW - timedelta(hours=23),
                operation_id="op-8",
                launch_cwd=_CWD,
                last_reason="launch_unknown",
            ),
        ),
    )
    disabled = config.state_dir / "DISABLED"
    disabled.write_text("", encoding="utf-8")
    os.utime(disabled, (FIXED_NOW.timestamp(), FIXED_NOW.timestamp()))


def test_status_json_has_exactly_the_design_fields(
    tmp_path, config, config_file, fixed_clock, monkeypatch, runner_calls
):
    seed_rich_store(config)
    set_path(monkeypatch, tmp_path, "orca-ide")
    result = run_readonly(tmp_path, "status", "--json", "--config", str(config_file))
    assert result.exit_code == 0, result.output
    report = json.loads(result.output)
    assert set(report) == {
        "healthy",
        "last_completed_cycle_age_seconds",
        "disabled_since",
        "next_permitted_at",
        "counts",
        "day_cap_used",
        "stale",
        "retry",
    }
    assert report == {
        "healthy": True,
        "last_completed_cycle_age_seconds": 120,
        "disabled_since": "2026-11-07T12:00:00Z",
        "next_permitted_at": "2026-11-07T13:10:00Z",
        "counts": {"abandoned": 1, "claimed": 1, "unknown": 2},
        "day_cap_used": 2,  # entries 7 and 8; entry 5 consumed 25 h ago is outside
        "stale": [
            {
                "issue": 5,
                "state": "unknown",
                "last_reason": "launch_unknown",
                "updated_at": "2026-11-06T12:00:00Z",
            },
            {
                "issue": 6,
                "state": "abandoned",
                "last_reason": "pending_orphan",
                "updated_at": "2026-11-06T12:00:00Z",
            },
        ],
        "retry": [
            {
                "issue": 5,
                "operation_id": "op:5.abc",
                "cwd": _CWD,
                "argv": retry_argv("orca-ide", 5, _CWD, "op:5.abc"),
            },
            {
                "issue": 8,
                "operation_id": "op-8",
                "cwd": _CWD,
                "argv": retry_argv("orca-ide", 8, _CWD, "op-8"),
            },
        ],
    }
    assert runner_calls == []


def test_status_text_lists_stale_entries_and_the_retry_commands(
    tmp_path, config, config_file, fixed_clock, monkeypatch
):
    """AC-9, FR-015, FR-021: status lists the full retry argv of an unknown entry."""
    seed_rich_store(config)
    set_path(monkeypatch, tmp_path, "orca-ide")
    result = run_readonly(tmp_path, "status", "--config", str(config_file))
    assert result.exit_code == 0
    assert result.output == (
        "healthy: yes\n"
        "last completed cycle age: 120s\n"
        "disabled since: 2026-11-07T12:00:00Z\n"
        "next permitted at: 2026-11-07T13:10:00Z\n"
        "day cap used: 2\n"
        "counts: abandoned=1, claimed=1, unknown=2\n"
        "stale: 2\n"
        "  issue 5 unknown launch_unknown updated 2026-11-06T12:00:00Z\n"
        "  issue 6 abandoned pending_orphan updated 2026-11-06T12:00:00Z\n"
        "retry: 2\n"
        f"  issue 5: run from {_CWD}\n"
        f"    {shlex.join(retry_argv('orca-ide', 5, _CWD, 'op:5.abc'))}\n"
        f"  issue 8: run from {_CWD}\n"
        f"    {shlex.join(retry_argv('orca-ide', 8, _CWD, 'op-8'))}\n"
    )


def _launched_like(n: int, state: str, reason: str, **over: object) -> Entry:
    """An entry past its launch call that carries an operation id and a cwd."""
    when = NOW - timedelta(minutes=30)
    return entry(
        n,
        state,
        when,
        launches=1,
        consumed_at=when,
        pending_at=when,
        operation_id=f"op-{n}",
        launch_cwd=_CWD,
        last_reason=reason,
        **over,
    )


def test_status_retry_lists_only_unknown_entries_with_an_id_and_a_cwd__ac9_fr015(
    tmp_path, config, config_file, fixed_clock, monkeypatch
):
    """AC-9, FR-015: launched, claimed and abandoned entries never get a retry."""
    seed_store(
        config,
        last_completed=NOW - timedelta(seconds=60),
        entries=(
            _launched_like(5, "launched", "launched"),
            _launched_like(6, "claimed", "claimed"),
            _launched_like(7, "abandoned", "claim_not_observed"),
            _launched_like(8, "unknown", "launch_unknown"),
        ),
    )
    set_path(monkeypatch, tmp_path, "orca-ide")
    as_json = run_readonly(tmp_path, "status", "--json", "--config", str(config_file))
    assert as_json.exit_code == 0, as_json.output
    report = json.loads(as_json.output)
    assert report["counts"] == {
        "abandoned": 1,
        "claimed": 1,
        "launched": 1,
        "unknown": 1,
    }
    assert report["retry"] == [
        {
            "issue": 8,
            "operation_id": "op-8",
            "cwd": _CWD,
            "argv": retry_argv("orca-ide", 8, _CWD, "op-8"),
        }
    ]
    as_text = run_readonly(tmp_path, "status", "--config", str(config_file))
    assert as_text.exit_code == 0, as_text.output
    assert "retry: 1\n" in as_text.output
    assert as_text.output.count("run from") == 1
    for n in (5, 6, 7):
        assert f"issue {n}: run from" not in as_text.output
        assert f"op-{n}" not in as_text.output


@pytest.mark.parametrize(("age", "code"), [(100, 0), (900, 0), (901, 1), (1000, 1)])
def test_status_exit_code_follows_the_age_of_the_last_completed_cycle(
    tmp_path, config, config_file, fixed_clock, age, code
):
    seed_store(config, last_completed=NOW - timedelta(seconds=age))
    result = run_readonly(tmp_path, "status", "--json", "--config", str(config_file))
    assert result.exit_code == code
    report = json.loads(result.output)
    assert report["last_completed_cycle_age_seconds"] == age
    assert report["healthy"] is (code == 0)


def test_status_is_unhealthy_when_no_cycle_ever_completed(
    tmp_path, config, config_file, fixed_clock
):
    seed_store(config)
    result = run_readonly(tmp_path, "status", "--config", str(config_file))
    assert result.exit_code == 1
    assert result.output.startswith(
        "healthy: no\nlast completed cycle age: never\ndisabled since: no\n"
    )
    as_json = run_readonly(tmp_path, "status", "--json", "--config", str(config_file))
    assert as_json.exit_code == 1
    assert json.loads(as_json.output)["last_completed_cycle_age_seconds"] is None


def test_status_exits_6_for_a_missing_store(tmp_path, config, config_file):
    config.state_dir.mkdir()
    result = run_readonly(tmp_path, "status", "--config", str(config_file))
    assert result.exit_code == 6
    assert result.output == "issue-watch: store_missing\n"


def test_status_exits_6_for_an_invalid_store(tmp_path, config, config_file):
    config.state_dir.mkdir()
    (config.state_dir / "dispatch.json").write_text("{not json", encoding="utf-8")
    result = run_readonly(tmp_path, "status", "--json", "--config", str(config_file))
    assert result.exit_code == 6
    assert result.output == "issue-watch: store_invalid\n"


@pytest.mark.skipif(os.geteuid() == 0, reason="root reads any file")
def test_status_exits_6_for_an_unreadable_store(tmp_path, config, config_file):
    seed_store(config)
    store_file = config.state_dir / "dispatch.json"
    store_file.chmod(0)
    try:
        result = run_readonly(tmp_path, "status", "--config", str(config_file))
    finally:
        store_file.chmod(0o600)
    assert result.exit_code == 6
    assert result.output == "issue-watch: store_invalid\n"


def test_status_exits_2_for_a_config_error_and_touches_nothing(tmp_path, config):
    seed_store(config)
    path = write_config(tmp_path / "bad.json", config, schema_version=2)
    result = run_readonly(tmp_path, "status", "--config", str(path))
    assert result.exit_code == 2
    assert_fallback(result.output, "config_invalid")


def test_status_leaves_every_mtime_unchanged_and_creates_no_audit_file__fr021(
    tmp_path, config, config_file, fixed_clock
):
    seed_rich_store(config)
    before = snapshot(tmp_path)
    for args in (["status"], ["status", "--json"]):
        run(*args, "--config", str(config_file))
        assert snapshot(tmp_path) == before
    assert not (config.state_dir / "audit.jsonl").exists()
    assert not (config.state_dir / "dry-run.json").exists()


# -- AC-9: the retry command's first element, with PATH pinned (OQ-50) ---------


def _retry_argv0(tmp_path, config, config_file) -> tuple[int, list[str]]:
    seed_store(
        config,
        last_completed=NOW - timedelta(seconds=60),
        entries=(
            entry(
                9,
                "unknown",
                NOW - timedelta(hours=25),
                launches=1,
                consumed_at=NOW - timedelta(hours=25),
                pending_at=NOW - timedelta(hours=25),
                operation_id="op-9",
                launch_cwd=_CWD,
                last_reason="launch_unknown",
            ),
        ),
    )
    result = run_readonly(tmp_path, "status", "--json", "--config", str(config_file))
    report = json.loads(result.output)
    assert [i["issue"] for i in report["stale"]] == [9]
    (item,) = report["retry"]
    return result.exit_code, item["argv"]


def test_status_retry_uses_orca_ide_when_it_is_on_path__ac9(
    tmp_path, config, config_file, fixed_clock, monkeypatch
):
    bin_dir = set_path(monkeypatch, tmp_path, "orca-ide")
    assert shutil.which("orca-ide") == str(bin_dir / "orca-ide")
    code, argv = _retry_argv0(tmp_path, config, config_file)
    assert code == 0
    assert argv == retry_argv("orca-ide", 9, _CWD, "op-9")
    assert argv[-3:] == ["--retry-launch", "op-9", "--json"]


def test_status_retry_uses_the_second_name_when_only_it_is_on_path__ac9(
    tmp_path, config, config_file, fixed_clock, monkeypatch
):
    set_path(monkeypatch, tmp_path, "orca")
    code, argv = _retry_argv0(tmp_path, config, config_file)
    assert code == 0
    assert argv == retry_argv("orca", 9, _CWD, "op-9")


def test_status_retry_uses_the_bare_first_name_when_none_is_on_path__oq50(
    tmp_path, config, config_file, fixed_clock, monkeypatch
):
    set_path(monkeypatch, tmp_path)  # an empty directory is the whole PATH
    assert shutil.which("orca-ide") is None
    code, argv = _retry_argv0(tmp_path, config, config_file)
    assert code == 0
    assert argv == retry_argv("orca-ide", 9, _CWD, "op-9")


# ==============================================================================
# Part B: init-state and reset with their audit lines (DF-03, DF-04, DF-57)
# ==============================================================================

HOST = "test-host"
TS = "2026-11-07T13:00:00Z"  # the fixed clock, as the audit ts of every reset line
CYCLE_ID_SHAPE = re.compile(r"[0-9a-f]{32}")
ISSUE_FLAGS = ("9", "--forfeit-guarantee")
RATE_FLAGS = ("--rate-limit",)
BOTH_FORMS = pytest.mark.parametrize(
    "flags", [ISSUE_FLAGS, RATE_FLAGS], ids=["issue", "rate"]
)
NOT_ROOT = pytest.mark.skipif(os.geteuid() == 0, reason="root ignores file modes")


def assert_lock_free(config: cycle.Config) -> None:
    """A lock taken after the run succeeds: the run released (or never took) it."""
    lock = config.state_dir / "lock"
    if lock.is_symlink() or not lock.is_file():
        return
    with record.FileStore(config.state_dir).lock():
        pass


@pytest.fixture
def reset_env(config, config_file, fixed_clock, monkeypatch, runner_calls):
    """A fixed clock and host; ``reset`` may never run a cycle, Orca or a process."""
    monkeypatch.setattr(cli.socket, "gethostname", lambda: HOST)

    def never(*args, **kwargs):
        raise AssertionError("reset must never launch")

    monkeypatch.setattr(cycle, "run_cycle", never)
    monkeypatch.setattr(cli.OrcaLauncher, "launch", never)
    yield config
    assert runner_calls == []
    assert_lock_free(config)


class LockHolder:
    """Holds ``flock`` on the lock file through a second open file description."""

    def __init__(self) -> None:
        self.fd: int | None = None

    def acquire(self, config: cycle.Config) -> None:
        import fcntl

        self.fd = os.open(config.state_dir / "lock", os.O_RDWR)
        fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def release(self) -> None:
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None


@pytest.fixture
def holder():
    held = LockHolder()
    yield held
    held.release()


def reset(config_file: Path, *args: str):
    return run("reset", *args, "--config", str(config_file))


def store_bytes(config: cycle.Config) -> bytes:
    return (config.state_dir / "dispatch.json").read_bytes()


def state_files(config: cycle.Config) -> dict[str, bytes]:
    """Every file in the state directory except the audit log, with its bytes."""
    return {
        p.name: p.read_bytes()
        for p in sorted(config.state_dir.iterdir())
        if p.name != "audit.jsonl"
    }


def the_cycle_id(line: dict) -> str:
    """Pop and return ``cycle_id`` after checking it is a ``uuid4().hex``."""
    cid = line.pop("cycle_id")
    assert CYCLE_ID_SHAPE.fullmatch(cid)
    return cid


def one_line(config: cycle.Config, kind: str, reason: str, **extra: object) -> str:
    """The audit file holds exactly one line, exactly this one; returns its cycle_id."""
    (got,) = audit_lines(config.state_dir)
    cid = the_cycle_id(got)
    assert got == {
        "kind": kind,
        "ts": TS,
        "host": HOST,
        "login": None,
        "dry_run": False,
        "reason": reason,
        **extra,
    }
    return cid


def abandoned9(**over: object) -> Entry:
    over.setdefault("last_reason", "pending_orphan")
    return entry(9, "abandoned", NOW - timedelta(hours=1), **over)


def unknown9() -> Entry:
    t = NOW - timedelta(hours=2)
    return entry(
        9,
        "unknown",
        NOW - timedelta(hours=1),
        launches=1,
        consumed_at=t,
        pending_at=t,
        operation_id="op-9",
        launch_cwd=_CWD,
        last_reason="launch_unknown",
    )


def consumed(state: str, hours: int = 5) -> Entry:
    t = NOW - timedelta(hours=hours)
    return entry(
        9, state, NOW - timedelta(hours=1), launches=1, consumed_at=t, pending_at=t
    )


def seed_reset_store(config: cycle.Config, *entries: Entry) -> record.StoreDoc:
    """A store with ``entries``, a claimed entry 10, a rate limit and a consumed_log."""
    t = NOW - timedelta(hours=1)
    other = entry(
        10,
        "claimed",
        NOW - timedelta(minutes=5),
        launches=1,
        consumed_at=t,
        pending_at=t,
    )
    store = seed_store(
        config,
        last_completed=NOW - timedelta(seconds=60),
        next_permitted=NOW + timedelta(minutes=10),
        entries=(*entries, other),
    )
    store.save(replace(store.load(), consumed_log=(NOW - timedelta(hours=3),)))
    return store.load()


# -- init-state -----------------------------------------------------------------


def test_init_state_creates_the_directory_the_store_and_the_lock(
    tmp_path, config, config_file, fixed_clock
):
    """AC-17, FR-026: init-state creates the state directory, the store and lock."""
    assert not config.state_dir.exists()
    result = run("init-state", "--config", str(config_file))
    assert result.exit_code == 0, result.output
    assert result.output == f"state created: {config.state_dir}\n"
    assert stat.S_IMODE(config.state_dir.stat().st_mode) == 0o700
    for name in ("dispatch.json", "lock"):
        assert stat.S_IMODE((config.state_dir / name).stat().st_mode) == 0o600
    assert sorted(p.name for p in config.state_dir.iterdir()) == [
        "dispatch.json",
        "lock",
    ]
    doc = record.FileStore(config.state_dir).load()
    assert (doc.created_at, doc.entries, doc.consumed_log) == (NOW, {}, ())
    assert doc.next_permitted_at is None and doc.last_completed_cycle_at is None
    assert_lock_free(config)


def test_a_second_init_state_exits_6_and_changes_nothing(
    tmp_path, config, config_file, fixed_clock
):
    assert run("init-state", "--config", str(config_file)).exit_code == 0
    store, lock = store_bytes(config), (config.state_dir / "lock").read_bytes()
    result = run_readonly(tmp_path, "init-state", "--config", str(config_file))
    assert result.exit_code == 6
    assert result.output == "issue-watch: a store already exists; nothing changed\n"
    assert store_bytes(config) == store
    assert (config.state_dir / "lock").read_bytes() == lock
    assert_lock_free(config)


@pytest.mark.parametrize("gone", ["dispatch.json", "lock"])
def test_init_state_refuses_when_either_file_already_exists(
    tmp_path, config, config_file, fixed_clock, gone
):
    assert run("init-state", "--config", str(config_file)).exit_code == 0
    (config.state_dir / gone).unlink()
    result = run_readonly(tmp_path, "init-state", "--config", str(config_file))
    assert result.exit_code == 6
    assert "a store already exists" in result.output
    assert not (config.state_dir / gone).exists()


@NOT_ROOT
def test_init_state_exits_6_when_the_parent_is_not_writable(tmp_path, config_file):
    parent = tmp_path / "ro"
    parent.mkdir()
    path = write_config(
        tmp_path / "ro.json", make_config(tmp_path, state_dir=parent / "state")
    )
    parent.chmod(0o500)
    try:
        result = run("init-state", "--config", str(path))
    finally:
        parent.chmod(0o700)
    assert result.exit_code == 6
    assert result.output == "issue-watch: state_dir_unwritable\n"
    assert list(parent.iterdir()) == []


def test_init_state_exits_6_when_the_parent_is_a_file(tmp_path):
    (tmp_path / "plain").write_text("x", "utf-8")
    path = write_config(
        tmp_path / "f.json", make_config(tmp_path, state_dir=tmp_path / "plain" / "s")
    )
    result = run_readonly(tmp_path, "init-state", "--config", str(path))
    assert result.exit_code == 6
    assert result.output == "issue-watch: state_dir_unwritable\n"


def test_init_state_exits_2_for_an_invalid_config__df53(tmp_path, config, config_file):
    write_config(config_file, config, project_id="not-a-project")
    result = run_readonly(tmp_path, "init-state", "--config", str(config_file))
    assert result.exit_code == 2
    assert_fallback(result.output, "config_invalid")
    assert not config.state_dir.exists()


def test_init_state_exits_2_on_an_unsupported_platform__df53(
    tmp_path, config, config_file, monkeypatch
):
    monkeypatch.setattr(sys, "platform", "darwin")
    result = run_readonly(tmp_path, "init-state", "--config", str(config_file))
    assert result.exit_code == 2
    assert_fallback(result.output, "platform_unsupported")
    assert not config.state_dir.exists()


def test_init_state_exits_2_for_a_deny_listed_filesystem__df53(
    tmp_path, config, config_file, monkeypatch
):
    monkeypatch.setattr(cycle, "_read_mountinfo", lambda: NFS_MOUNTINFO)
    result = run_readonly(tmp_path, "init-state", "--config", str(config_file))
    assert result.exit_code == 2
    assert_fallback(result.output, "config_invalid")
    assert not config.state_dir.exists()


# -- reset: usage errors and Click errors --------------------------------------


@pytest.mark.parametrize(
    "args",
    [
        ("9", "--rate-limit", "--forfeit-guarantee"),
        ("9", "--rate-limit"),
        (),
        ("--forfeit-guarantee",),
        ("9",),
    ],
    ids=["both", "both-no-flag", "neither", "flag-only", "no-flag"],
)
def test_reset_usage_errors_exit_2_with_the_reset_refused_fallback(
    tmp_path, reset_env, config_file, args
):
    seed_reset_store(reset_env, abandoned9())
    result = run_readonly(tmp_path, "reset", *args, "--config", str(config_file))
    assert result.exit_code == 2
    (fb,) = fallback_lines(result.output)
    assert set(fb) == {"kind", "ts", "host", "exit", "reason"}
    assert (fb["kind"], fb["exit"], fb["reason"]) == ("cycle", 2, "reset_refused")
    assert (fb["ts"], fb["host"]) != ("", "")  # stamped by the fallback itself
    assert any(ln.startswith("issue-watch: reset") for ln in result.output.splitlines())
    assert not (reset_env.state_dir / "audit.jsonl").exists()


def test_a_reset_usage_error_is_found_before_the_config_is_read(tmp_path, reset_env):
    result = run_readonly(tmp_path, "reset", "--config", str(tmp_path / "missing.json"))
    assert result.exit_code == 2
    (fb,) = fallback_lines(result.output)
    assert fb["reason"] == "reset_refused"


@pytest.mark.parametrize("args", [("abc",), ("0",), ("--bogus",), ("9", "10")])
def test_click_parse_errors_write_no_audit_line(tmp_path, reset_env, config_file, args):
    seed_reset_store(reset_env, abandoned9())
    result = run_readonly(tmp_path, "reset", *args, "--config", str(config_file))
    assert result.exit_code == 2
    assert fallback_lines(result.output) == []
    assert not (reset_env.state_dir / "audit.jsonl").exists()


def test_reset_exits_2_for_an_invalid_config(tmp_path, reset_env, config_file):
    seed_reset_store(reset_env, abandoned9())
    write_config(config_file, reset_env, project_id="not-a-project")
    result = run_readonly(tmp_path, "reset", *ISSUE_FLAGS, "--config", str(config_file))
    assert result.exit_code == 2
    assert_fallback(result.output, "config_invalid")
    assert not (reset_env.state_dir / "audit.jsonl").exists()


def test_reset_exits_2_on_an_unsupported_platform(
    tmp_path, reset_env, config_file, monkeypatch
):
    seed_reset_store(reset_env, abandoned9())
    monkeypatch.setattr(sys, "platform", "darwin")
    result = run_readonly(tmp_path, "reset", *RATE_FLAGS, "--config", str(config_file))
    assert result.exit_code == 2
    assert_fallback(result.output, "platform_unsupported")
    assert not (reset_env.state_dir / "audit.jsonl").exists()


# -- reset N --forfeit-guarantee: refusals (DF-04) -----------------------------


def _seed_launched(config):
    seed_reset_store(config, consumed("launched"))


def _seed_claimed(config):
    seed_reset_store(config, consumed("claimed"))


def _seed_pending(config):
    seed_reset_store(config, entry(9, "pending", NOW))


def _seed_failed(config):
    seed_reset_store(config, entry(9, "failed", NOW, last_reason="prompt_invalid"))


def _seed_absent(config):  # an abandoned entry 10 must not be taken for 9
    seed_reset_store(config, entry(10, "abandoned", NOW - timedelta(hours=1)))


@pytest.mark.parametrize(
    "seed",
    [_seed_launched, _seed_claimed, _seed_pending, _seed_failed, _seed_absent],
    ids=["launched", "claimed", "pending", "failed", "absent"],
)
def test_reset_refuses_an_entry_that_is_not_abandoned_or_unknown__df04(
    reset_env, config_file, seed
):
    seed(reset_env)
    store = reset_env.state_dir / "dispatch.json"
    before, mtime = store.read_bytes(), store.stat().st_mtime_ns
    result = reset(config_file, *ISSUE_FLAGS)
    assert result.exit_code == 2
    assert result.output == (
        "issue-watch: reset refused: issue 9 has no abandoned or unknown entry; "
        "nothing changed\n"
    )
    assert store.read_bytes() == before
    assert store.stat().st_mtime_ns == mtime
    one_line(reset_env, "warning", "reset_refused", issue=9)


# -- reset N --forfeit-guarantee: success (DF-03) ------------------------------


@pytest.mark.parametrize(
    "target",
    [
        abandoned9(),
        abandoned9(
            launches=1,
            consumed_at=NOW - timedelta(hours=5),
            pending_at=NOW - timedelta(hours=5),
        ),
        unknown9(),
    ],
    ids=["abandoned-never-consumed", "abandoned-consumed", "unknown"],
)
def test_reset_removes_the_entry_and_keeps_the_day_cap_count__df03(
    reset_env, config_file, target
):
    """AC-10, AC-17, FR-024, FR-026: reset N keeps the day-cap count through reset."""
    before = seed_reset_store(reset_env, target)
    result = reset(config_file, *ISSUE_FLAGS)
    assert result.exit_code == 0, result.output
    assert result.output == "issue 9 may now be launched a second time\n"
    after = record.FileStore(reset_env.state_dir).load()
    assert 9 not in after.entries
    assert after.entries[10] == before.entries[10]
    log = before.consumed_log
    if target.consumed_at is not None:
        log = (*log, target.consumed_at)
    assert after == replace(before, entries={10: before.entries[10]}, consumed_log=log)
    assert record.day_cap_count(after, NOW) == record.day_cap_count(before, NOW)
    assert stat.S_IMODE((reset_env.state_dir / "dispatch.json").stat().st_mode) == 0o600
    one_line(
        reset_env,
        "decision",
        "operator_reset",
        issue=9,
        approver_id=None,
        approval_event_id=None,
        approved_at=None,
    )


def test_reset_rotates_a_full_audit_log_before_its_one_line(reset_env, config_file):
    seed_reset_store(reset_env, abandoned9())
    from superclaude.cli.issue_watch.audit import ROTATE_BYTES

    big = b"{}\n" * (ROTATE_BYTES // 3 + 1)
    audit_file = reset_env.state_dir / "audit.jsonl"
    audit_file.write_bytes(big)
    assert reset(config_file, *ISSUE_FLAGS).exit_code == 0
    assert (reset_env.state_dir / "audit.jsonl.1").read_bytes() == big
    (line,) = audit_lines(reset_env.state_dir)
    assert (line["kind"], line["reason"], line["issue"]) == (
        "decision",
        "operator_reset",
        9,
    )


# -- reset --rate-limit --------------------------------------------------------


@pytest.mark.parametrize("limited", [True, False], ids=["limited", "already-clear"])
def test_reset_rate_limit_clears_next_permitted_at__df03(
    reset_env, config_file, limited
):
    """AC-18, AC-17, FR-026, FR-028: reset --rate-limit clears next_permitted_at."""
    before = seed_reset_store(reset_env, abandoned9())
    if not limited:
        store = record.FileStore(reset_env.state_dir)
        store.save(replace(before, next_permitted_at=None))
        before = store.load()
    assert (before.next_permitted_at is not None) is limited
    result = reset(config_file, *RATE_FLAGS)
    assert result.exit_code == 0, result.output
    assert result.output == "rate limit cleared\n"
    after = record.FileStore(reset_env.state_dir).load()
    assert after == replace(before, next_permitted_at=None)
    assert after.entries[9] == before.entries[9]  # no entry is touched
    one_line(reset_env, "warning", "operator_reset")  # no issue key at all


def test_every_reset_line_has_its_own_cycle_id__ac17(reset_env, config_file):
    seed_reset_store(reset_env, abandoned9())
    assert reset(config_file, *RATE_FLAGS).exit_code == 0
    assert reset(config_file, *RATE_FLAGS).exit_code == 0
    assert reset(config_file, *ISSUE_FLAGS).exit_code == 0
    assert reset(config_file, *ISSUE_FLAGS).exit_code == 2  # now absent
    lines = audit_lines(reset_env.state_dir)
    assert [(ln["kind"], ln["reason"]) for ln in lines] == [
        ("warning", "operator_reset"),
        ("warning", "operator_reset"),
        ("decision", "operator_reset"),
        ("warning", "reset_refused"),
    ]
    ids = [the_cycle_id(ln) for ln in lines]
    assert len(set(ids)) == 4
    for ln in lines:
        assert (ln["ts"], ln["host"], ln["login"], ln["dry_run"]) == (
            TS,
            HOST,
            None,
            False,
        )
    assert all(ln["kind"] != "cycle" for ln in lines)


# -- reset: lock, store and state directory failures (DF-57) -------------------


@BOTH_FORMS
def test_reset_exits_75_when_the_lock_is_held_and_never_rotates(
    reset_env, config_file, holder, flags
):
    from superclaude.cli.issue_watch.audit import ROTATE_BYTES

    seed_reset_store(reset_env, abandoned9())
    big = b"{}\n" * (ROTATE_BYTES // 3 + 1)
    audit_file = reset_env.state_dir / "audit.jsonl"
    audit_file.write_bytes(big)
    files = state_files(reset_env)
    holder.acquire(reset_env)
    result = reset(config_file, *flags)
    holder.release()
    assert result.exit_code == 75
    assert result.output == "issue-watch: lock_held\n"
    assert state_files(reset_env) == files
    assert not (reset_env.state_dir / "audit.jsonl.1").exists()
    text = audit_file.read_bytes()
    assert text.startswith(big) and len(text) > len(big)
    new = [json.loads(ln) for ln in text[len(big) :].decode().splitlines()]
    assert len(new) == 1
    the_cycle_id(new[0])
    assert new[0] == {
        "kind": "warning",
        "ts": TS,
        "host": HOST,
        "login": None,
        "dry_run": False,
        "reason": "lock_held",
    }


def _break_lock_missing(config, tmp_path):
    (config.state_dir / "lock").unlink()


def _break_lock_symlink(config, tmp_path):
    (config.state_dir / "lock").unlink()
    (tmp_path / "elsewhere").write_text("", "utf-8")
    (config.state_dir / "lock").symlink_to(tmp_path / "elsewhere")


def _break_store_missing(config, tmp_path):
    (config.state_dir / "dispatch.json").unlink()


def _break_store_invalid(config, tmp_path):
    (config.state_dir / "dispatch.json").write_text("{not json", "utf-8")


@BOTH_FORMS
@pytest.mark.parametrize(
    ("break_it", "reason"),
    [
        (_break_lock_missing, "lock_missing"),
        (_break_lock_symlink, "lock_invalid"),
        (_break_store_missing, "store_missing"),
        (_break_store_invalid, "store_invalid"),
    ],
)
def test_reset_exits_6_with_one_warning_line_for_a_lock_or_store_failure(
    tmp_path, reset_env, config_file, flags, break_it, reason
):
    seed_reset_store(reset_env, abandoned9())
    break_it(reset_env, tmp_path)
    files = state_files(reset_env)
    result = reset(config_file, *flags)
    assert result.exit_code == 6
    assert result.output == f"issue-watch: {reason}\n"
    assert state_files(reset_env) == files
    assert sorted(os.listdir(reset_env.state_dir)) == sorted([*files, "audit.jsonl"])
    one_line(reset_env, "warning", reason)  # no issue key, never a cycle line


@BOTH_FORMS
def test_reset_writes_only_the_fallback_when_there_is_no_state_directory(
    tmp_path, reset_env, config_file, flags
):
    result = run_readonly(tmp_path, "reset", *flags, "--config", str(config_file))
    assert result.exit_code == 6
    (fb,) = fallback_lines(result.output)
    assert fb == {
        "kind": "cycle",
        "ts": TS,
        "host": HOST,
        "exit": 6,
        "reason": "lock_missing",
    }
    assert not reset_env.state_dir.exists()


@NOT_ROOT
@BOTH_FORMS
def test_reset_writes_only_the_fallback_for_an_unwritable_state_directory(
    reset_env, config_file, flags
):
    seed_reset_store(reset_env, abandoned9())
    files = state_files(reset_env)
    reset_env.state_dir.chmod(0o500)
    try:
        result = reset(config_file, *flags)
    finally:
        reset_env.state_dir.chmod(0o700)
    assert result.exit_code == 6
    (fb,) = fallback_lines(result.output)
    assert fb == {
        "kind": "cycle",
        "ts": TS,
        "host": HOST,
        "exit": 6,
        "reason": "state_dir_unwritable",
    }
    assert "issue-watch: state_dir_unwritable" in result.output.splitlines()
    assert state_files(reset_env) == files
    assert sorted(os.listdir(reset_env.state_dir)) == sorted(files)  # no audit file


@NOT_ROOT
def test_a_refusal_in_an_unwritable_state_directory_falls_back_to_stderr(
    reset_env, config_file
):
    seed_reset_store(reset_env, consumed("launched"))
    files = state_files(reset_env)
    reset_env.state_dir.chmod(0o500)
    try:
        result = reset(config_file, *ISSUE_FLAGS)
    finally:
        reset_env.state_dir.chmod(0o700)
    assert result.exit_code == 2
    (fb,) = fallback_lines(result.output)
    assert (fb["kind"], fb["exit"], fb["reason"]) == ("cycle", 2, "reset_refused")
    assert state_files(reset_env) == files
    assert not (reset_env.state_dir / "audit.jsonl").exists()
