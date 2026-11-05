"""Tests for the in-package ``superclaude update`` command."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest
from click.testing import CliRunner

from superclaude.cli.main import main

_INSTALLERS = (
    "superclaude.cli.install_core.install_core_files",
    "superclaude.cli.install_commands.install_commands",
    "superclaude.cli.install_agents.install_agents",
    "superclaude.cli.install_skills.install_all_skills",
    "superclaude.cli.install_ccsession.wire_ccsession",
    "superclaude.cli.install_hooks.install_hooks",
    "superclaude.cli.install_templates.install_templates",
    "superclaude.cli.install_user_setup.install_user_setup",
)

# Runs at the end of ``install`` only; ``update`` never touches MCP registrations.
_RETIRE_STEP = "superclaude.cli.install_retired_mcp.run_retire_step"
# Required phase of ``install`` only, between user setup and the retire step.
_CODEGRAPH_PHASE = "superclaude.cli.install_mcp.install_codegraph_mcp"


@pytest.fixture(autouse=True)
def isolated_home_guard(tmp_path, monkeypatch):
    from superclaude.cli import install_user_setup

    home = tmp_path / "isolated-home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(home / "config"))
    state = SimpleNamespace(home=home)
    # The existing real-framework ccsession fixture must not download plugins or
    # Orca skills while exercising the real install.
    monkeypatch.setattr(
        install_user_setup, "install_plugins", lambda **kwargs: (True, "Plugin fixture")
    )
    monkeypatch.setattr(
        install_user_setup,
        "install_orca_skills",
        lambda **kwargs: (True, "Orca fixture"),
    )
    # The codegraph phase would download and register a real binary.
    monkeypatch.setattr(_CODEGRAPH_PHASE, lambda **kwargs: (True, "codegraph fixture"))
    return state


def _stub_installers(monkeypatch, *, failing: str | None = None):
    calls: list[str] = []

    for path in _INSTALLERS:
        name = path.rsplit(".", 1)[-1]

        def fake(*args, _name=name, **kwargs):
            calls.append(_name)
            return (_name != failing, f"{_name} result")

        monkeypatch.setattr(path, fake)

    def codegraph(**kwargs):
        calls.append("install_codegraph_mcp")
        return (failing != "install_codegraph_mcp", "install_codegraph_mcp result")

    def retire(*args, **kwargs):
        calls.append("run_retire_step")
        return {}

    monkeypatch.setattr(_CODEGRAPH_PHASE, codegraph)
    monkeypatch.setattr(_RETIRE_STEP, retire)
    return calls


def test_update_refreshes_hooks_after_other_components(monkeypatch):
    calls = _stub_installers(monkeypatch)

    result = CliRunner().invoke(main, ["update"])

    assert result.exit_code == 0, result.output
    assert calls == [
        "install_core_files",
        "install_commands",
        "install_agents",
        "install_all_skills",
        "wire_ccsession",
        "install_hooks",
        "install_templates",
        "install_user_setup",
    ]
    assert "Updating hooks" in result.output


def test_update_propagates_hook_install_failure(monkeypatch):
    calls = _stub_installers(monkeypatch, failing="install_hooks")

    result = CliRunner().invoke(main, ["update"])

    assert result.exit_code == 1
    assert "install_hooks" in calls
    assert "install_hooks result" in result.output


def test_install_wires_before_hooks_and_templates(monkeypatch):
    calls = _stub_installers(monkeypatch)
    result = CliRunner().invoke(main, ["install"])
    assert result.exit_code == 0, result.output
    assert calls == [
        "install_core_files",
        "install_commands",
        "install_agents",
        "install_all_skills",
        "wire_ccsession",
        "install_hooks",
        "install_templates",
        "install_user_setup",
        "install_codegraph_mcp",
        "run_retire_step",
    ]


def test_update_propagates_user_setup_failure(monkeypatch):
    _stub_installers(monkeypatch, failing="install_user_setup")
    result = CliRunner().invoke(main, ["update"])
    assert result.exit_code == 1
    assert "install_user_setup result" in result.output


def _stub_listings(monkeypatch):
    for path in (
        "superclaude.cli.install_core.list_core_files",
        "superclaude.cli.install_core.list_installed_core_files",
        "superclaude.cli.install_commands.list_available_commands",
        "superclaude.cli.install_commands.list_installed_commands",
        "superclaude.cli.install_agents.list_available_agents",
        "superclaude.cli.install_agents.list_installed_agents",
        "superclaude.cli.install_skill.list_available_skills",
        "superclaude.cli.install_skills.list_installed_skills",
        "superclaude.cli.install_templates.list_available_templates",
        "superclaude.cli.install_templates.list_installed_templates",
    ):
        monkeypatch.setattr(path, lambda: [])


def test_install_list_does_not_wire(monkeypatch):
    calls = _stub_installers(monkeypatch)
    _stub_listings(monkeypatch)
    result = CliRunner().invoke(main, ["install", "--list"])
    assert result.exit_code == 0, result.output
    assert not calls


@pytest.mark.parametrize("command", ["install", "update"])
def test_install_and_update_wire_failure_exit_nonzero(monkeypatch, command):
    calls = _stub_installers(monkeypatch, failing="wire_ccsession")
    result = CliRunner().invoke(main, [command])
    assert result.exit_code == 1, result.output
    assert "wire_ccsession result" in result.output
    assert calls.index("wire_ccsession") == calls.index("install_all_skills") + 1
    assert calls.index("install_hooks") == calls.index("wire_ccsession") + 1


@pytest.fixture
def native_install(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    target = home / ".claude/commands/sc"
    result = CliRunner().invoke(main, ["install", "--target", str(target)])
    assert result.exit_code == 0, result.output
    return home, target


def test_real_install_launches_ccsession(native_install):
    home, _ = native_install
    skill = home / ".claude/skills/ccsession-tag"
    binary = home / ".local/bin/ccsession"
    assert (skill / "SKILL.md").is_file()
    assert binary.is_symlink() and binary.resolve() == (skill / "ccsession").resolve()
    env = home / ".claude/ccsession.env"
    assert env.is_file() and env.stat().st_mode & 0o777 == 0o600
    settings = json.loads((home / ".claude/settings.json").read_text())
    commands = [
        hook["command"]
        for group in settings["hooks"]["SessionStart"]
        for hook in group["hooks"]
    ]
    assert commands.count("~/.claude/skills/ccsession-tag/hooks/session-start.sh") == 1

    result = subprocess.run(
        [str(binary), "--help"],
        env={
            **os.environ,
            "PATH": str(binary.parent) + os.pathsep + os.environ["PATH"],
        },
        capture_output=True,
        text=True,
        check=True,
    )
    assert "ccsession --help" in result.stdout


def test_real_update_restores_packaged_ccsession(native_install):
    home, target = native_install
    skill = home / ".claude/skills/ccsession-tag"
    source = (
        Path(__file__).resolve().parents[2] / "src/superclaude/skills/ccsession-tag"
    )
    (skill / "ccsession").write_text("modified wrapper")
    (skill / "hooks/session-start.sh").write_text("modified hook")
    env = home / ".claude/ccsession.env"
    env.write_bytes(b"private-token")
    env.chmod(0o640)

    result = CliRunner().invoke(main, ["update", "--target", str(target)])
    assert result.exit_code == 0, result.output
    for name in (
        "ccsession",
        "local-gateway-alias-proxy.py",
        "hooks/session-start.sh",
        "SKILL.md",
    ):
        assert (skill / name).read_bytes() == (source / name).read_bytes()
    assert (home / ".local/bin/ccsession").resolve() == (skill / "ccsession").resolve()
    assert env.read_bytes() == b"private-token"
    assert env.stat().st_mode & 0o777 == 0o640
    assert "private-token" not in result.output


def test_install_force_target_do_not_redirect(monkeypatch, isolated_home_guard):
    _stub_installers(monkeypatch)
    captured = {}
    target = isolated_home_guard.home / "custom commands"

    def commands(*, target_path, force):
        captured["commands"] = (target_path, force)
        return True, "command fixture"

    def user_setup(*, force):
        captured["setup"] = force
        return True, "setup fixture"

    monkeypatch.setattr("superclaude.cli.install_commands.install_commands", commands)
    monkeypatch.setattr(
        "superclaude.cli.install_user_setup.install_user_setup", user_setup
    )
    result = CliRunner().invoke(main, ["install", "--force", "--target", str(target)])
    assert result.exit_code == 0, result.output
    assert captured == {
        "commands": (target, True),
        "setup": True,
    }


def test_install_runs_codegraph_phase_after_user_setup_before_retire(monkeypatch):
    calls = _stub_installers(monkeypatch)
    result = CliRunner().invoke(main, ["install"])
    assert result.exit_code == 0, result.output
    assert calls[-3:] == [
        "install_user_setup",
        "install_codegraph_mcp",
        "run_retire_step",
    ]
    assert "Installing codegraph (required user-level phase)" in result.output


def test_install_codegraph_failure_keeps_framework_work_and_exits_one(monkeypatch):
    calls = _stub_installers(monkeypatch, failing="install_codegraph_mcp")
    result = CliRunner().invoke(main, ["install"])
    assert result.exit_code == 1
    assert "install_codegraph_mcp result" in result.output
    # every other phase ran, and the non-fatal retire step still runs after the failure
    assert calls[:8] == [
        "install_core_files",
        "install_commands",
        "install_agents",
        "install_all_skills",
        "wire_ccsession",
        "install_hooks",
        "install_templates",
        "install_user_setup",
    ]
    assert calls[-1] == "run_retire_step"


def test_install_codegraph_failure_message_reaches_stderr(monkeypatch):
    _stub_installers(monkeypatch)
    monkeypatch.setattr(
        _CODEGRAPH_PHASE, lambda **kwargs: (False, "codegraph checksum failed: x")
    )
    result = CliRunner().invoke(main, ["install"])
    assert result.exit_code == 1
    assert "codegraph checksum failed: x" in result.stderr


def test_install_codegraph_exception_is_a_failure_not_a_traceback(monkeypatch):
    calls = _stub_installers(monkeypatch)

    def boom(**kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(_CODEGRAPH_PHASE, boom)
    result = CliRunner().invoke(main, ["install"])
    assert result.exit_code == 1
    assert "codegraph phase failed (OSError)" in result.output
    assert "disk full" not in result.output
    assert calls[-1] == "run_retire_step"


def test_install_force_is_not_forwarded_to_codegraph(monkeypatch):
    _stub_installers(monkeypatch)
    seen = []
    monkeypatch.setattr(
        _CODEGRAPH_PHASE, lambda **kwargs: seen.append(kwargs) or (True, "ok")
    )
    result = CliRunner().invoke(main, ["install", "--force"])
    assert result.exit_code == 0, result.output
    assert seen == [{"scope": "user"}]


def test_update_never_runs_the_codegraph_phase(monkeypatch):
    calls = _stub_installers(monkeypatch)
    result = CliRunner().invoke(main, ["update"])
    assert result.exit_code == 0, result.output
    assert "install_codegraph_mcp" not in calls


def test_install_list_prints_codegraph_block_read_only(
    monkeypatch, isolated_home_guard, tmp_path
):
    from superclaude.cli import install_codegraph, install_mcp

    _stub_installers(monkeypatch)
    _stub_listings(monkeypatch)
    empty_path = tmp_path / "empty-path"
    empty_path.mkdir()
    monkeypatch.setenv("PATH", str(empty_path))

    def forbidden(*args, **kwargs):
        pytest.fail("install --list must not download or call claude mcp")

    monkeypatch.setattr(install_codegraph, "_download", forbidden)
    monkeypatch.setattr(install_mcp, "_exec_claude", forbidden)
    monkeypatch.setattr(install_mcp, "_run_command", forbidden)
    result = CliRunner().invoke(main, ["install", "--list"])
    assert result.exit_code == 0, result.output
    assert "codegraph MCP (pinned v1.6.2; user scope):" in result.output
    assert "Executable: missing" in result.output
    assert "Owner: none" in result.output
    assert "User registration: absent" in result.output
    assert not (isolated_home_guard.home / ".codegraph").exists()


@pytest.mark.parametrize(
    ("verdict", "line"),
    [
        ((True, ""), "Ready for Serena retirement: yes"),
        ((False, "patched reason"), "Ready for Serena retirement: no (patched reason)"),
    ],
)
def test_one_patched_codegraph_ready_is_seen_by_install_list_install_and_doctor(
    monkeypatch, verdict, line
):
    from superclaude.cli import install_mcp
    from superclaude.cli.doctor import _check_codegraph

    calls = _stub_installers(monkeypatch)
    _stub_listings(monkeypatch)
    monkeypatch.setattr(install_mcp, "codegraph_ready", lambda: verdict)
    retire_args = []
    monkeypatch.setattr(_RETIRE_STEP, lambda *a, **k: retire_args.append((a, k)) or {})

    listed = CliRunner().invoke(main, ["install", "--list"])
    assert line in listed.output
    assert line in "\n".join(_check_codegraph()["details"])
    assert CliRunner().invoke(main, ["install"]).exit_code == 0
    assert "install_codegraph_mcp" in calls
    assert retire_args == [((verdict[0],), {})]


def test_a_ready_registration_does_not_count_when_the_phase_failed(monkeypatch):
    from superclaude.cli import install_mcp

    _stub_installers(monkeypatch, failing="install_codegraph_mcp")
    monkeypatch.setattr(install_mcp, "codegraph_ready", lambda: (True, ""))
    retire_args = []
    monkeypatch.setattr(_RETIRE_STEP, lambda *a, **k: retire_args.append(a) or {})
    assert CliRunner().invoke(main, ["install"]).exit_code == 1
    assert retire_args == [(False,)]
