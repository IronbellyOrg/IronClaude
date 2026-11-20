"""Tests for the ``superclaude issue-watch`` command group.

Covers the group and its registration, the config path (DF-13), ``check-config``
with its routing preview, ``once``, ``status`` with the held issues, ``init-state``
and ``reset`` (design 4.1, 4.3, 4.11 and 10.2). Everything runs in process with
Click's ``CliRunner``. ``HOME`` and ``XDG_STATE_HOME`` point into ``tmp_path`` for
every test, ``/proc/self/mountinfo`` is replaced by a fixed text, and
``SubprocessRunner.run`` raises, so no real process can start.

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
import shutil
import socket
import stat
import sys
from dataclasses import replace
from datetime import datetime, timedelta
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.issue_watch import audit, cli, cycle, hold, record, wake
from superclaude.cli.issue_watch import runner as runner_mod
from superclaude.cli.issue_watch.cli import issue_watch_group
from superclaude.cli.main import main

from .conftest import (
    CYCLE_NOW,
    REPO_A,
    TIERS_TEXT,
    FailingStore,
    FakeClock,
    FakeRunner,
    make_config,
    make_deps,
    write_registry,
)
from .conftest import result as command_result

# The real assembly, taken before the autouse fixture below replaces it.
_REAL_BUILD_DEPS = cli.build_deps

EXPECTED_COMMANDS = ["check-config", "init-state", "once", "reset", "status"]
LOCAL_MOUNTINFO = "1 0 0:1 / / rw - ext4 /dev/sda1 rw\n"
NFS_MOUNTINFO = "1 0 0:1 / / rw - nfs4 server:/export rw\n"
NOW = CYCLE_NOW  # 2026-11-07T13:00:00Z
_DROP = object()
WAKE_ID = "20261107T120000Z-0000000a"
ORCH = "ironclaude-1"
KEY9 = f"{REPO_A}#9"

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


@pytest.fixture
def tiers(monkeypatch) -> FakeRunner:
    """``check-config`` reads the tier list from ``ccsession --help``: answer it."""
    fake = FakeRunner({("ccsession", "--help"): command_result(stdout=TIERS_TEXT)})
    monkeypatch.setattr(cli, "SubprocessRunner", lambda: fake)
    return fake


def write_config(path: Path, config: cycle.Config, **over: object) -> Path:
    """Write ``config`` as the JSON file; ``over`` replaces keys, ``_DROP`` removes."""
    raw: dict[str, object] = {
        "schema_version": 2,
        "enabled": config.enabled,
        "orchestrator_repo": str(config.orchestrator_repo),
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


def pending(doc: record.StoreDoc, n: int, at: datetime) -> record.StoreDoc:
    return record.mark_pending(doc, REPO_A, n, ORCH, at)


def woken(doc: record.StoreDoc, n: int, at: datetime) -> record.StoreDoc:
    return record.mark_woken(pending(doc, n, at), f"{REPO_A}#{n}", WAKE_ID, at)


def unknown(doc: record.StoreDoc, n: int, at: datetime) -> record.StoreDoc:
    return record.mark_unknown(pending(doc, n, at), f"{REPO_A}#{n}", None, None, at)


def abandoned(doc: record.StoreDoc, n: int, at: datetime) -> record.StoreDoc:
    return record.mark_spawn_error(pending(doc, n, at), f"{REPO_A}#{n}", at)


def acked(doc: record.StoreDoc, n: int, at: datetime) -> record.StoreDoc:
    return record.mark_acked(woken(doc, n, at), f"{REPO_A}#{n}", at)


def seed_store(
    config: cycle.Config,
    build=lambda doc: doc,
    *,
    last_completed: datetime | None = None,
    next_permitted: datetime | None = None,
    rate_streak: int = 0,
) -> record.FileStore:
    """Create the state directory and store, then fill it with ``build(doc)``."""
    store = record.init_state(config.state_dir, NOW - timedelta(days=3), baseline=False)
    doc = build(store.load())
    store.save(
        replace(
            doc,
            last_completed_cycle_at=last_completed,
            next_permitted_at=next_permitted,
            rate_streak=rate_streak,
        )
    )
    return store


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


def test_the_group_help_says_it_wakes_the_orchestrator():
    result = CliRunner().invoke(issue_watch_group, ["--help"])
    text = " ".join(result.output.split())
    assert "assigned to you" in text and "orchestrator" in text
    assert "claim" not in text and "trigger" not in text


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
    tmp_path, default_config_file, tiers
):
    result = run("check-config")
    assert result.exit_code == 0, result.output
    assert result.output.startswith("configuration is valid\n")


def test_a_passed_config_with_a_tilde_is_expanded__df13(tmp_path, config, tiers):
    write_config(tmp_path / "home/custom.json", config)
    result = run("check-config", "--config", "~/custom.json")
    assert result.exit_code == 0, result.output


def test_a_tilde_inside_the_json_is_not_expanded__df13(tmp_path, config):
    path = write_config(tmp_path / "bad.json", config, orchestrator_repo="~/orch")
    result = run("check-config", "--config", str(path))
    assert result.exit_code == 2
    assert_fallback(result.output, "config_invalid")


def test_a_missing_default_config_is_exit_2(tmp_path):
    result = run("check-config")
    assert result.exit_code == 2
    assert_fallback(result.output, "config_invalid")


def test_a_version_1_config_is_refused_with_the_new_schema_named(tmp_path, config):
    path = write_config(tmp_path / "old.json", config, schema_version=1)
    result = run("check-config", "--config", str(path))
    assert result.exit_code == 2
    assert_fallback(result.output, "config_invalid")
    assert "schema_version must be the integer 2" in result.output


@pytest.mark.parametrize("old_key", ["project_id", "approvers_file", "worktree"])
def test_a_removed_config_key_is_refused(tmp_path, config, old_key):
    path = write_config(tmp_path / "old.json", config, **{old_key: "x"})
    result = run("check-config", "--config", str(path))
    assert result.exit_code == 2
    assert_fallback(result.output, "config_invalid")
    assert old_key in result.output


# ==============================================================================
# check-config
# ==============================================================================


def test_check_config_prints_the_setup_and_the_routing_preview_and_writes_nothing(
    tmp_path, config, config_file, tiers
):
    result = run_readonly(tmp_path, "check-config", "--config", str(config_file))
    assert result.exit_code == 0, result.output
    lines = result.output.splitlines()
    assert lines[0] == "configuration is valid"
    assert lines[1] == f"state_dir: {config.state_dir}"
    assert lines[2] == f"orchestrator_repo: {config.orchestrator_repo}"
    assert lines[3].startswith("repos: 2 in 2 orgs, tiers ")
    assert "tier1b" in lines[3]
    assert (
        f"  {REPO_A} (enabled, max 3 in flight, tier tier1b): "
        "next issue goes to a new ironclaude-1"
    ) in lines
    assert not config.state_dir.exists()
    assert tiers.argvs() == [("ccsession", "--help")]


def test_check_config_lists_each_orchestrator_with_what_it_holds(
    tmp_path, config, config_file, tiers
):
    write_registry(config, {ORCH: {}})
    result = run("check-config", "--config", str(config_file))
    assert result.exit_code == 0, result.output
    assert f"    {ORCH} active holds 0" in result.output.splitlines()
    assert f"next issue goes to {ORCH}" in result.output


def test_check_config_exits_2_for_a_registry_that_cannot_be_read(
    tmp_path, config, config_file, tiers
):
    orch_dir = config.orchestrator_repo / ".orchestrator"
    orch_dir.mkdir()
    (orch_dir / "orchestrators.json").write_text("{not json", "utf-8")
    result = run("check-config", "--config", str(config_file))
    assert result.exit_code == 2
    (line,) = fallback_lines(result.output)
    assert line["reason"] == "registry_invalid"


def test_check_config_names_a_missing_orchestrator_repo(tmp_path, config, tiers):
    gone = tmp_path / "no-such-repo"
    path = write_config(tmp_path / "c.json", config, orchestrator_repo=str(gone))
    result = run_readonly(tmp_path, "check-config", "--config", str(path))
    assert result.exit_code == 2
    assert_fallback(result.output, "orchestrator_repo_invalid")


def test_check_config_names_a_bad_repos_file(tmp_path, config, config_file, tiers):
    (config.orchestrator_repo / "repos.yaml").write_text("repos: [", "utf-8")
    result = run_readonly(tmp_path, "check-config", "--config", str(config_file))
    assert result.exit_code == 2
    assert_fallback(result.output, "repos_invalid")


def test_check_config_names_a_missing_repos_file(tmp_path, config, config_file, tiers):
    (config.orchestrator_repo / "repos.yaml").unlink()
    result = run("check-config", "--config", str(config_file))
    assert result.exit_code == 2
    assert_fallback(result.output, "repos_invalid")


def test_check_config_exits_2_when_the_tier_list_cannot_be_read(
    tmp_path, config, config_file, monkeypatch
):
    fake = FakeRunner({("ccsession", "--help"): command_result(returncode=1)})
    monkeypatch.setattr(cli, "SubprocessRunner", lambda: fake)
    result = run("check-config", "--config", str(config_file))
    assert result.exit_code == 2
    assert_fallback(result.output, "repos_invalid")


def test_check_config_exits_2_for_an_invalid_config_file(tmp_path, config, config_file):
    write_config(config_file, config, enabled="yes")
    result = run_readonly(tmp_path, "check-config", "--config", str(config_file))
    assert result.exit_code == 2
    assert_fallback(result.output, "config_invalid")


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
        (7, "ack_not_observed"),
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


def test_once_dry_run_passes_the_flag_and_prints_what_it_would_do(
    config_file, monkeypatch
):
    seen: list[bool] = []

    def fake_cycle(deps, dry_run):
        seen.append(dry_run)
        return cycle.CycleResult(
            exit_code=0,
            reason="cycle_complete",
            cycle_id="0" * 32,
            would_wake=(f"{REPO_A}#42", f"{REPO_A}#43"),
            would_hold=(f"{REPO_A}#44",),
            would_release=(f"{REPO_A}#45",),
            would_request=(f"{REPO_A}#46",),
        )

    monkeypatch.setattr(cli, "build_deps", lambda cfg: object())
    monkeypatch.setattr(cycle, "run_cycle", fake_cycle)
    result = run("once", "--dry-run", "--config", str(config_file))
    assert result.exit_code == 0
    assert result.output == (
        "cycle: cycle_complete\nexit: 0\n"
        f"would_wake: {REPO_A}#42, {REPO_A}#43\n"
        f"would_hold: {REPO_A}#44\n"
        f"would_release: {REPO_A}#45\n"
        f"would_request: {REPO_A}#46\n"
    )
    assert seen == [True]


def test_once_without_dry_run_prints_no_would_lines(config_file, monkeypatch):
    monkeypatch.setattr(cli, "build_deps", lambda cfg: object())
    monkeypatch.setattr(
        cycle,
        "run_cycle",
        lambda deps, dry_run: cycle.CycleResult(
            exit_code=0,
            reason="cycle_complete",
            cycle_id="0" * 32,
            woken=(KEY9,),
            would_wake=(KEY9,),
        ),
    )
    result = run("once", "--config", str(config_file))
    assert result.exit_code == 0
    assert result.output == "cycle: cycle_complete\nexit: 0\n"


def test_once_on_a_config_error_writes_the_fallback_and_exits_2(
    tmp_path, config, monkeypatch, runner_calls
):
    path = write_config(tmp_path / "bad.json", config, orchestrator_repo=_DROP)
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
    assert deps.waker.deliveries == []
    assert (tmp_state.state_dir / "dispatch.json").read_bytes() == before
    (line,) = audit_lines(tmp_state.state_dir)
    assert (line["kind"], line["reason"], line["exit"], line["dry_run"]) == (
        "cycle",
        "not_enabled",
        0,
        False,
    )
    assert line["host"] == "test-host"


def test_once_dry_run_runs_a_real_cycle_and_wakes_nobody(
    tmp_path, tmp_state, gh_world, monkeypatch
):
    world = gh_world()
    world.issue(REPO_A, 9)
    path = write_config(tmp_path / "on.json", world.config)
    deps = world.deps(tmp_path, tmp_state)
    monkeypatch.setattr(cli, "build_deps", lambda cfg: deps)
    before = (tmp_state.state_dir / "dispatch.json").read_bytes()
    result = run("once", "--dry-run", "--config", str(path))
    assert result.exit_code == 0, result.output
    first, *rest = result.output.splitlines()
    assert first.startswith("cycle: ")
    assert rest == ["exit: 0", f"would_wake: {KEY9}"]
    assert deps.waker.deliveries == []
    assert (tmp_state.state_dir / "dispatch.json").read_bytes() == before
    assert audit_lines(tmp_state.state_dir)[-1]["dry_run"] is True


def test_once_wakes_the_orchestrator_for_an_assigned_issue(
    tmp_path, tmp_state, gh_world, monkeypatch
):
    world = gh_world()
    world.issue(REPO_A, 9)
    path = write_config(tmp_path / "on.json", world.config)
    deps = world.deps(tmp_path, tmp_state)
    monkeypatch.setattr(cli, "build_deps", lambda cfg: deps)
    result = run("once", "--config", str(path))
    assert result.exit_code == 0, result.output
    assert len(deps.waker.deliveries) == 1
    assert tmp_state.load().entries[KEY9].state == "woken"


# -- build_deps: the one production assembly of Deps (DF-45, Gate C fix C-12) ------


def test_build_deps_wires_the_real_dependencies_from_the_config(config, monkeypatch):
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
    # The waker is the real one and runs through a SubprocessRunner.
    assert isinstance(deps.waker, wake.Waker)
    assert deps.label_guard is None and deps.wake_token is None


def test_the_cli_module_never_imports_subprocess():
    text = Path(cli.__file__).read_text(encoding="utf-8")
    assert "import subprocess" not in text and "from subprocess" not in text


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
    text = "issue title that must never reach the output"
    path = _once_over(tmp_path, tmp_state, gh_world, monkeypatch, RuntimeError(text))
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
    assert text not in result.output  # only the class name is printed
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

STATUS_KEYS = {
    "healthy",
    "last_completed_cycle_age_seconds",
    "disabled_since",
    "next_permitted_at",
    "rate_streak",
    "counts",
    "day_cap_used",
    "baseline_pending",
    "stale",
    "held",
}


def seed_rich_store(config: cycle.Config) -> record.FileStore:
    """One stale unknown, one fresh woken, one acked, a quiet hold and a hold with a signal."""
    old = NOW - timedelta(hours=25)

    def build(doc: record.StoreDoc) -> record.StoreDoc:
        doc = unknown(doc, 5, old)
        doc = woken(doc, 6, NOW - timedelta(minutes=3))
        doc = acked(doc, 7, NOW - timedelta(hours=2))
        quiet = hold.new_hold(NOW - timedelta(hours=3), NOW - timedelta(hours=3), ())
        doc = record.set_hold(doc, f"{REPO_A}#20", quiet)
        busy = hold.with_evidence(
            hold.new_hold(
                NOW - timedelta(hours=3), NOW - timedelta(hours=3), ("fix_approach",)
            ),
            NOW - timedelta(minutes=10),
            "branch",
        )
        return record.set_hold(doc, f"{REPO_A}#21", busy)

    store = seed_store(
        config,
        build,
        last_completed=NOW - timedelta(seconds=120),
        next_permitted=NOW + timedelta(minutes=10),
        rate_streak=2,
    )
    (config.state_dir / "DISABLED").write_text("", "utf-8")
    return store


def test_status_json_has_exactly_the_design_fields(
    tmp_path, config, config_file, fixed_clock
):
    seed_rich_store(config)
    result = run_readonly(tmp_path, "status", "--json", "--config", str(config_file))
    assert result.exit_code == 0, result.output
    report = json.loads(result.output)
    assert set(report) == STATUS_KEYS
    assert report["healthy"] is True
    assert report["last_completed_cycle_age_seconds"] == 120
    assert report["disabled_since"] is not None
    assert report["next_permitted_at"] == "2026-11-07T13:10:00Z"
    assert report["rate_streak"] == 2
    assert report["counts"] == {"unknown": 1, "woken": 1, "acked": 1}
    assert report["baseline_pending"] is False
    assert [s["issue"] for s in report["stale"]] == [f"{REPO_A}#5"]
    assert set(report["stale"][0]) == {"issue", "state", "last_reason", "updated_at"}
    assert [h["issue"] for h in report["held"]] == [f"{REPO_A}#20", f"{REPO_A}#21"]
    quiet, busy = report["held"]
    assert quiet["signal"] is None and quiet["plan_request"] is None
    assert busy["signal"] == "branch" and busy["missing"] == ["fix_approach"]
    assert set(busy) == {
        "issue",
        "state",
        "first_held_at",
        "quiet_since",
        "signal",
        "plan_request",
        "missing",
    }


def test_status_text_lists_stale_entries_and_the_held_issues(
    tmp_path, config, config_file, fixed_clock
):
    seed_rich_store(config)
    result = run_readonly(tmp_path, "status", "--config", str(config_file))
    assert result.exit_code == 0, result.output
    lines = result.output.splitlines()
    assert lines[0] == "healthy: yes"
    assert "last completed cycle age: 120s" in lines
    assert "rate-limit streak: 2" in lines
    assert "counts: acked=1, unknown=1, woken=1" in lines
    assert "stale: 1" in lines
    assert any(ln.startswith(f"  issue {REPO_A}#5 unknown") for ln in lines)
    assert "held: 2" in lines
    signal = [ln for ln in lines if ln.startswith(f"  issue {REPO_A}#21 ")]
    assert len(signal) == 1 and "signal branch" in signal[0]
    quiet = [ln for ln in lines if ln.startswith(f"  issue {REPO_A}#20 ")]
    assert len(quiet) == 1 and "signal none" in quiet[0]
    assert "baseline:" not in result.output
    assert "retry" not in result.output  # no command for a person to run (R5)


def test_status_says_when_the_baseline_is_still_pending(
    tmp_path, config, config_file, fixed_clock
):
    record.init_state(config.state_dir, NOW - timedelta(minutes=5))
    result = run("status", "--config", str(config_file))
    assert result.exit_code == 1  # no cycle has completed yet
    assert "baseline: pending" in result.output
    assert json.loads(run("status", "--json", "--config", str(config_file)).output)[
        "baseline_pending"
    ]


@pytest.mark.parametrize(("age", "code"), [(100, 0), (900, 0), (901, 1), (1000, 1)])
def test_status_exit_code_follows_the_age_of_the_last_completed_cycle(
    config, config_file, fixed_clock, age, code
):
    seed_store(config, last_completed=NOW - timedelta(seconds=age))
    result = run("status", "--config", str(config_file))
    assert result.exit_code == code
    assert f"healthy: {'yes' if code == 0 else 'no'}" in result.output


def test_status_is_unhealthy_when_no_cycle_ever_completed(
    config, config_file, fixed_clock
):
    seed_store(config)
    result = run("status", "--json", "--config", str(config_file))
    assert result.exit_code == 1
    report = json.loads(result.output)
    assert report["healthy"] is False
    assert report["last_completed_cycle_age_seconds"] is None


def test_status_exits_6_for_a_missing_store(tmp_path, config, config_file):
    result = run_readonly(tmp_path, "status", "--config", str(config_file))
    assert result.exit_code == 6
    assert result.output == "issue-watch: store_missing\n"


def test_status_exits_6_for_an_invalid_store(tmp_path, config, config_file):
    config.state_dir.mkdir()
    (config.state_dir / "dispatch.json").write_text("{not json", "utf-8")
    result = run_readonly(tmp_path, "status", "--config", str(config_file))
    assert result.exit_code == 6
    assert result.output == "issue-watch: store_invalid\n"


def test_status_reads_a_version_1_store_as_an_empty_one_and_leaves_the_file_alone(
    tmp_path, config, config_file, fixed_clock
):
    """A schema 1 store is dropped in memory: status reads an empty store that wants a baseline."""
    seed_store(config, last_completed=NOW - timedelta(seconds=60))
    path = config.state_dir / "dispatch.json"
    raw = json.loads(path.read_text("utf-8"))
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "created_at": raw["created_at"],
                "next_permitted_at": None,
                "last_completed_cycle_at": raw["last_completed_cycle_at"],
                "consumed_log": [],
                "entries": {},
            }
        ),
        encoding="utf-8",
    )
    before = path.read_bytes()
    result = run("status", "--json", "--config", str(config_file))
    assert result.exit_code == 1, result.output  # no cycle has completed on schema 2
    report = json.loads(result.output)
    assert (report["counts"], report["baseline_pending"]) == ({}, True)
    assert path.read_bytes() == before  # the migration is in memory only


@pytest.mark.skipif(os.geteuid() == 0, reason="root reads any file")
def test_status_exits_6_for_an_unreadable_store(tmp_path, config, config_file):
    seed_store(config)
    path = config.state_dir / "dispatch.json"
    path.chmod(0)
    try:
        result = run("status", "--config", str(config_file))
    finally:
        path.chmod(0o600)
    assert result.exit_code == 6
    assert result.output == "issue-watch: store_invalid\n"


def test_status_exits_2_for_a_config_error_and_touches_nothing(tmp_path, config):
    path = write_config(tmp_path / "bad.json", config, schema_version="2")
    result = run_readonly(tmp_path, "status", "--config", str(path))
    assert result.exit_code == 2
    assert_fallback(result.output, "config_invalid")


def test_status_leaves_every_mtime_unchanged_and_creates_no_audit_file__fr021(
    tmp_path, config, config_file, fixed_clock
):
    seed_rich_store(config)
    before = snapshot(tmp_path)
    for args in (("status",), ("status", "--json")):
        assert run(*args, "--config", str(config_file)).exit_code == 0
        assert snapshot(tmp_path) == before
    assert not (config.state_dir / "audit.jsonl").exists()


def test_status_works_on_another_platform_because_it_only_reads(
    tmp_path, config, config_file, fixed_clock, monkeypatch
):
    seed_store(config, last_completed=NOW - timedelta(seconds=60))
    monkeypatch.setattr(sys, "platform", "darwin")
    assert run("status", "--config", str(config_file)).exit_code == 0


# ==============================================================================
# init-state and reset with their audit lines (DF-03, DF-04, DF-57)
# ==============================================================================

HOST = "test-host"
TS = "2026-11-07T13:00:00Z"  # the fixed clock, as the audit ts of every reset line
CYCLE_ID_SHAPE = re.compile(r"[0-9a-f]{32}")
ISSUE_FLAGS = (KEY9, "--forfeit-guarantee")
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
        raise AssertionError("reset must never run a cycle or wake anyone")

    monkeypatch.setattr(cycle, "run_cycle", never)
    monkeypatch.setattr(wake.Waker, "deliver", never)
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


def seed_reset_store(config: cycle.Config, build) -> record.StoreDoc:
    """A store with issue 9 built by ``build``, an acked issue 10, a rate limit and a log."""
    t = NOW - timedelta(hours=1)

    def both(doc: record.StoreDoc) -> record.StoreDoc:
        doc = build(doc)
        doc = acked(doc, 10, t)
        return replace(doc, consumed_log=(NOW - timedelta(hours=3),))

    store = seed_store(
        config,
        both,
        last_completed=NOW - timedelta(seconds=60),
        next_permitted=NOW + timedelta(minutes=10),
        rate_streak=2,
    )
    return store.load()


def abandoned9(doc: record.StoreDoc) -> record.StoreDoc:
    return abandoned(doc, 9, NOW - timedelta(hours=1))


def unknown9(doc: record.StoreDoc) -> record.StoreDoc:
    return unknown(doc, 9, NOW - timedelta(hours=1))


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
    assert doc.holds == {} and doc.info_seen == ()
    assert doc.next_permitted_at is None and doc.last_completed_cycle_at is None
    assert doc.baseline is True  # the first completed cycle records what is assigned
    assert_lock_free(config)


def test_init_state_with_no_baseline_wakes_the_issues_already_assigned(
    config, config_file, fixed_clock
):
    result = run("init-state", "--no-baseline", "--config", str(config_file))
    assert result.exit_code == 0, result.output
    assert record.FileStore(config.state_dir).load().baseline is False


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
    write_config(config_file, config, schema_version=1)
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
        (KEY9, "--rate-limit", "--forfeit-guarantee"),
        (KEY9, "--rate-limit"),
        (),
        ("--forfeit-guarantee",),
        (KEY9,),
        ("9", "--forfeit-guarantee"),
        ("abc", "--forfeit-guarantee"),
        (f"{REPO_A}#0", "--forfeit-guarantee"),
        (f"{REPO_A}#x", "--forfeit-guarantee"),
    ],
    ids=[
        "both",
        "both-no-flag",
        "neither",
        "flag-only",
        "no-flag",
        "bare-number",
        "word",
        "zero",
        "not-a-number",
    ],
)
def test_reset_usage_errors_exit_2_with_the_reset_refused_fallback(
    tmp_path, reset_env, config_file, args
):
    seed_reset_store(reset_env, abandoned9)
    result = run_readonly(tmp_path, "reset", *args, "--config", str(config_file))
    assert result.exit_code == 2
    (fb,) = fallback_lines(result.output)
    assert set(fb) == {"kind", "ts", "host", "exit", "reason"}
    assert (fb["kind"], fb["exit"], fb["reason"]) == ("cycle", 2, "reset_refused")
    assert (fb["ts"], fb["host"]) != ("", "")  # stamped by the fallback itself
    assert any(ln.startswith("issue-watch: ") for ln in result.output.splitlines())
    assert not (reset_env.state_dir / "audit.jsonl").exists()


def test_a_reset_usage_error_is_found_before_the_config_is_read(tmp_path, reset_env):
    result = run_readonly(tmp_path, "reset", "--config", str(tmp_path / "missing.json"))
    assert result.exit_code == 2
    (fb,) = fallback_lines(result.output)
    assert fb["reason"] == "reset_refused"


@pytest.mark.parametrize("args", [("--bogus",), (KEY9, "10")])
def test_click_parse_errors_write_no_audit_line(tmp_path, reset_env, config_file, args):
    seed_reset_store(reset_env, abandoned9)
    result = run_readonly(tmp_path, "reset", *args, "--config", str(config_file))
    assert result.exit_code == 2
    assert fallback_lines(result.output) == []
    assert not (reset_env.state_dir / "audit.jsonl").exists()


def test_reset_exits_2_for_an_invalid_config(tmp_path, reset_env, config_file):
    seed_reset_store(reset_env, abandoned9)
    write_config(config_file, reset_env, schema_version=1)
    result = run_readonly(tmp_path, "reset", *ISSUE_FLAGS, "--config", str(config_file))
    assert result.exit_code == 2
    assert_fallback(result.output, "config_invalid")
    assert not (reset_env.state_dir / "audit.jsonl").exists()


def test_reset_exits_2_on_an_unsupported_platform(
    tmp_path, reset_env, config_file, monkeypatch
):
    seed_reset_store(reset_env, abandoned9)
    monkeypatch.setattr(sys, "platform", "darwin")
    result = run_readonly(tmp_path, "reset", *RATE_FLAGS, "--config", str(config_file))
    assert result.exit_code == 2
    assert_fallback(result.output, "platform_unsupported")
    assert not (reset_env.state_dir / "audit.jsonl").exists()


# -- reset OWNER/REPO#N --forfeit-guarantee: refusals (DF-04) ------------------


def _seed_woken(doc):
    return woken(doc, 9, NOW - timedelta(hours=1))


def _seed_acked(doc):
    return acked(doc, 9, NOW - timedelta(hours=1))


def _seed_pending(doc):
    return pending(doc, 9, NOW)


def _seed_failed(doc):
    return record.fail(doc, REPO_A, 9, "wake_line_invalid", NOW)


def _seed_absent(doc):  # an abandoned entry 11 must not be taken for 9
    return abandoned(doc, 11, NOW - timedelta(hours=1))


def _seed_other_repo(doc):  # the same number in another repository is another issue
    other = record.mark_pending(doc, "IronbellyGroup/example", 9, ORCH, NOW)
    return record.mark_spawn_error(other, "IronbellyGroup/example#9", NOW)


@pytest.mark.parametrize(
    "seed",
    [
        _seed_woken,
        _seed_acked,
        _seed_pending,
        _seed_failed,
        _seed_absent,
        _seed_other_repo,
    ],
    ids=["woken", "acked", "pending", "failed", "absent", "other-repo"],
)
def test_reset_refuses_an_entry_that_is_not_abandoned_or_unknown__df04(
    reset_env, config_file, seed
):
    seed_reset_store(reset_env, seed)
    store = reset_env.state_dir / "dispatch.json"
    before, mtime = store.read_bytes(), store.stat().st_mtime_ns
    result = reset(config_file, *ISSUE_FLAGS)
    assert result.exit_code == 2
    assert result.output == (
        f"issue-watch: reset refused: {KEY9} has no abandoned or "
        "unknown entry; nothing changed\n"
    )
    assert store.read_bytes() == before
    assert store.stat().st_mtime_ns == mtime
    one_line(reset_env, "warning", "reset_refused", repo=REPO_A, issue=9)


# -- reset OWNER/REPO#N --forfeit-guarantee: success (DF-03) -------------------


@pytest.mark.parametrize(
    "target",
    [abandoned9, unknown9],
    ids=["abandoned", "unknown"],
)
def test_reset_removes_the_entry_and_keeps_the_day_cap_count__df03(
    reset_env, config_file, target
):
    """AC-10, AC-17, FR-024, FR-026: reset keeps the day-cap count through reset."""
    before = seed_reset_store(reset_env, target)
    gone = before.entries[KEY9]
    result = reset(config_file, *ISSUE_FLAGS)
    assert result.exit_code == 0, result.output
    assert result.output == f"issue {KEY9} may now be woken a second time\n"
    after = record.FileStore(reset_env.state_dir).load()
    assert KEY9 not in after.entries
    assert after.entries[f"{REPO_A}#10"] == before.entries[f"{REPO_A}#10"]
    assert after == replace(
        before,
        entries={f"{REPO_A}#10": before.entries[f"{REPO_A}#10"]},
        consumed_log=(*before.consumed_log, gone.consumed_at),
    )
    assert record.day_cap_count(after, NOW) == record.day_cap_count(before, NOW)
    assert stat.S_IMODE((reset_env.state_dir / "dispatch.json").stat().st_mode) == 0o600
    one_line(reset_env, "decision", "operator_reset", repo=REPO_A, issue=9)


def test_reset_rotates_a_full_audit_log_before_its_one_line(reset_env, config_file):
    seed_reset_store(reset_env, abandoned9)
    from superclaude.cli.issue_watch.audit import ROTATE_BYTES

    big = b"{}\n" * (ROTATE_BYTES // 3 + 1)
    audit_file = reset_env.state_dir / "audit.jsonl"
    audit_file.write_bytes(big)
    assert reset(config_file, *ISSUE_FLAGS).exit_code == 0
    assert (reset_env.state_dir / "audit.jsonl.1").read_bytes() == big
    (line,) = audit_lines(reset_env.state_dir)
    assert (line["kind"], line["reason"], line["repo"], line["issue"]) == (
        "decision",
        "operator_reset",
        REPO_A,
        9,
    )


# -- reset --rate-limit --------------------------------------------------------


@pytest.mark.parametrize("limited", [True, False], ids=["limited", "already-clear"])
def test_reset_rate_limit_clears_next_permitted_at_and_the_streak__df03(
    reset_env, config_file, limited
):
    """AC-18, AC-17, FR-026, FR-028: reset --rate-limit clears the wait and the streak."""
    before = seed_reset_store(reset_env, abandoned9)
    if not limited:
        store = record.FileStore(reset_env.state_dir)
        store.save(replace(before, next_permitted_at=None, rate_streak=0))
        before = store.load()
    assert (before.next_permitted_at is not None) is limited
    result = reset(config_file, *RATE_FLAGS)
    assert result.exit_code == 0, result.output
    assert result.output == "rate limit cleared\n"
    after = record.FileStore(reset_env.state_dir).load()
    assert after == replace(before, next_permitted_at=None, rate_streak=0)
    assert after.entries[KEY9] == before.entries[KEY9]  # no entry is touched
    one_line(reset_env, "warning", "operator_reset")  # no issue key at all


def test_every_reset_line_has_its_own_cycle_id__ac17(reset_env, config_file):
    seed_reset_store(reset_env, abandoned9)
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

    seed_reset_store(reset_env, abandoned9)
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
    seed_reset_store(reset_env, abandoned9)
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
    seed_reset_store(reset_env, abandoned9)
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
    seed_reset_store(reset_env, _seed_acked)
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
