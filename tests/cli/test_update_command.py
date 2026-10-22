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


_NATIVE_INSTALLER = "superclaude.cli.install_mcp.install_codebase_memory_mcp"


@pytest.fixture(autouse=True)
def native_phase_guard(tmp_path, monkeypatch):
    from superclaude.cli import install_codebase_memory as native
    from superclaude.cli import install_mcp, install_user_setup

    home = tmp_path / "isolated-home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(home / "config"))
    monkeypatch.setattr(native.platform, "system", lambda: "Linux")
    monkeypatch.setattr(native.platform, "machine", lambda: "x86_64")
    state = SimpleNamespace(
        home=home, calls=[], found=native.Discovery("missing"), known=True, entry=None
    )

    def phase(*, scope):
        state.calls.append({"scope": scope})
        return True, "Codebase Memory shared phase fixture"

    monkeypatch.setattr(install_mcp, "install_codebase_memory_mcp", phase)
    monkeypatch.setattr(native, "discover_executable", lambda: state.found)
    monkeypatch.setattr(
        install_mcp, "read_user_mcp_entry", lambda name: (state.known, state.entry)
    )
    monkeypatch.setattr(
        native,
        "acquire_codebase_memory",
        lambda **kwargs: pytest.fail("real native acquisition"),
    )
    monkeypatch.setattr(
        native, "_run_bounded", lambda *a, **k: pytest.fail("real native process")
    )
    monkeypatch.setattr(
        install_mcp, "_run_command", lambda *a, **k: pytest.fail("real Claude CLI")
    )
    # The existing real-framework ccsession fixture must not download plugins or
    # Orca skills while exercising the new mandatory native phase.
    monkeypatch.setattr(
        install_user_setup, "install_plugins", lambda **kwargs: (True, "Plugin fixture")
    )
    monkeypatch.setattr(
        install_user_setup,
        "install_orca_skills",
        lambda **kwargs: (True, "Orca fixture"),
    )
    return state


def _stub_installers(monkeypatch, *, failing: str | None = None):
    calls: list[str] = []

    for path in (*_INSTALLERS, _NATIVE_INSTALLER):
        name = path.rsplit(".", 1)[-1]

        def fake(*args, _name=name, **kwargs):
            if _name == "install_codebase_memory_mcp":
                assert not args and kwargs == {"scope": "user"}
            calls.append(_name)
            return (_name != failing, f"{_name} result")

        monkeypatch.setattr(path, fake)

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
        "install_codebase_memory_mcp",
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


@pytest.mark.parametrize(
    "stage", ["download", "verification", "registration", "platform"]
)
def test_install_native_failure_is_mandatory_and_preserves_framework_work(
    monkeypatch, native_phase_guard, stage
):
    calls = _stub_installers(monkeypatch)
    marker = native_phase_guard.home / "framework-work-kept"

    def core(*, force):
        calls.append("install_core_files")
        marker.write_text("existing successful framework phase")
        return True, "framework phase completed"

    def native_phase(*, scope):
        assert scope == "user"
        calls.append("install_codebase_memory_mcp")
        return False, f"Native {stage} fixture failure"

    monkeypatch.setattr("superclaude.cli.install_core.install_core_files", core)
    monkeypatch.setattr(_NATIVE_INSTALLER, native_phase)
    result = CliRunner().invoke(main, ["install"])
    assert result.exit_code == 1, result.output
    assert stage in result.output and "incomplete" in result.output.lower()
    assert "retry" in result.output.lower() and "superclaude install" in result.output
    assert marker.read_text() == "existing successful framework phase"
    assert calls[-2:] == ["install_user_setup", "install_codebase_memory_mcp"]


@pytest.mark.parametrize(
    "state,registration,expected",
    [
        ("canonical", "matching", "matches verified"),
        ("external", "matching", "external"),
        ("canonical", "stale", "stale"),
        ("canonical", "absent", "absent"),
        ("missing", "absent", "missing"),
        ("non_runnable", "absent", "non_runnable"),
        ("ambiguous", "absent", "ambiguous"),
        ("canonical", "unknown", "unknown"),
    ],
)
def test_install_list_reports_native_and_exact_user_status_without_repair(
    monkeypatch, native_phase_guard, state, registration, expected
):
    from superclaude.cli import install_codebase_memory as native

    calls = _stub_installers(monkeypatch)
    _stub_listings(monkeypatch)
    executable = native_phase_guard.home / ".local/bin/codebase-memory-mcp"
    native_phase_guard.found = native.Discovery(
        state, executable, "0.12.1" if state in {"canonical", "external"} else None
    )
    native_phase_guard.known = registration != "unknown"
    if registration in {"matching", "stale"}:
        native_phase_guard.entry = {
            "type": "stdio",
            "command": str(executable),
            "args": [] if registration == "matching" else ["--stale"],
        }
    before = sorted(str(path) for path in native_phase_guard.home.rglob("*"))
    result = CliRunner().invoke(
        main,
        [
            "install",
            "--list",
            "--force",
            "--target",
            str(native_phase_guard.home / "unused-target"),
        ],
    )
    assert result.exit_code == 0, result.output
    assert "Codebase Memory MCP" in result.output and expected in result.output
    assert "User registration" in result.output
    assert calls == [] and native_phase_guard.calls == []
    assert sorted(str(path) for path in native_phase_guard.home.rglob("*")) == before


def test_install_list_reports_unsupported_native_without_probe(
    monkeypatch, native_phase_guard
):
    from superclaude.cli import install_codebase_memory as native

    calls = _stub_installers(monkeypatch)
    _stub_listings(monkeypatch)
    monkeypatch.setattr(native.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        native, "discover_executable", lambda: pytest.fail("unsupported native probe")
    )
    result = CliRunner().invoke(main, ["install", "--list"])
    assert result.exit_code == 0 and "unavailable" in result.output.lower()
    assert "Linux" in result.output and calls == []


def test_install_force_target_do_not_redirect_or_force_native(
    monkeypatch, native_phase_guard
):
    _stub_installers(monkeypatch)
    captured = {}
    target = native_phase_guard.home / "custom commands"

    def commands(*, target_path, force):
        captured["commands"] = (target_path, force)
        return True, "command fixture"

    def user_setup(*, force):
        captured["setup"] = force
        return True, "setup fixture"

    def native_phase(*, scope):
        captured["native"] = {"scope": scope}
        return True, "native fixture"

    monkeypatch.setattr("superclaude.cli.install_commands.install_commands", commands)
    monkeypatch.setattr(
        "superclaude.cli.install_user_setup.install_user_setup", user_setup
    )
    monkeypatch.setattr(_NATIVE_INSTALLER, native_phase)
    result = CliRunner().invoke(main, ["install", "--force", "--target", str(target)])
    assert result.exit_code == 0, result.output
    assert captured == {
        "commands": (target, True),
        "setup": True,
        "native": {"scope": "user"},
    }


@pytest.mark.parametrize(
    "shared_result",
    [
        "Already correct; no-op",
        "Missing user registration repaired without acquisition",
        "External binary reused without replacement",
    ],
)
def test_repeated_install_delegates_shared_noop_repair_external_policy(
    monkeypatch, native_phase_guard, shared_result
):
    _stub_installers(monkeypatch)
    external = native_phase_guard.home / "external manager" / "codebase-memory-mcp"
    external.parent.mkdir()
    external.write_bytes(b"external installation sentinel")
    calls = []

    def native_phase(*, scope):
        calls.append({"scope": scope})
        return True, shared_result

    monkeypatch.setattr(_NATIVE_INSTALLER, native_phase)
    for flags in ([], ["--force"]):
        result = CliRunner().invoke(main, ["install", *flags])
        assert result.exit_code == 0 and shared_result in result.output
    assert calls == [{"scope": "user"}, {"scope": "user"}]
    assert external.read_bytes() == b"external installation sentinel"


def test_update_never_restores_native_but_later_install_calls_shared_phase(
    monkeypatch, native_phase_guard
):
    from superclaude.cli import install_codebase_memory as native

    calls = _stub_installers(monkeypatch)
    monkeypatch.setattr(
        native,
        "discover_executable",
        lambda: pytest.fail("native discovery during update"),
    )
    result = CliRunner().invoke(main, ["update"])
    assert result.exit_code == 0
    assert calls == [path.rsplit(".", 1)[-1] for path in _INSTALLERS]
    assert not (native_phase_guard.home / ".local/bin/codebase-memory-mcp").exists()
    calls.clear()
    result = CliRunner().invoke(main, ["install"])
    assert result.exit_code == 0 and calls[-1] == "install_codebase_memory_mcp"
