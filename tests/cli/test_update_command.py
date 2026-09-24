"""Tests for the in-package ``superclaude update`` command."""

from __future__ import annotations

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
)


def _stub_installers(monkeypatch, *, failing: str | None = None):
    calls: list[str] = []

    for path in _INSTALLERS:
        name = path.rsplit(".", 1)[-1]

        def fake(*args, _name=name, **kwargs):
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
    ]
    assert "Updating hooks" in result.output


def test_update_propagates_hook_install_failure(monkeypatch):
    calls = _stub_installers(monkeypatch, failing="install_hooks")

    result = CliRunner().invoke(main, ["update"])

    assert result.exit_code == 1
    assert calls[-1] == "install_hooks"
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
    ]


def test_install_list_does_not_wire(monkeypatch):
    calls = _stub_installers(monkeypatch)
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
