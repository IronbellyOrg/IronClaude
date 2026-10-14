"""The routing guide ships as a core file; retired core files do not."""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli import install_commands, install_core

_REPO = Path(__file__).resolve().parents[2]
_GUIDE = _REPO / "src/superclaude/core/HOW-WE-WORK.md"
_RETIRED_CORE = (
    "ORCHESTRATOR.md",
    "COMMANDS.md",
    "PERSONAS.md",
    "MODES.md",
    "FLAGS.md",
    "MCP.md",
)


def test_how_we_work_shipped_in_core():
    assert "HOW-WE-WORK.md" in install_core.list_core_files()


def test_how_we_work_installed_and_listed(tmp_path, monkeypatch):
    target = tmp_path / ".claude"
    ok, message = install_core.install_core_files(target_path=target, force=True)
    assert ok, message
    assert (target / "HOW-WE-WORK.md").read_bytes() == _GUIDE.read_bytes()
    monkeypatch.setattr(install_core.Path, "home", classmethod(lambda cls: tmp_path))
    assert "HOW-WE-WORK.md" in install_core.list_installed_core_files()


def test_retired_core_files_not_shipped():
    assert not set(install_core.list_core_files()) & set(_RETIRED_CORE)
    for name in _RETIRED_CORE:
        assert not (_REPO / "src/superclaude/core" / name).exists(), name
    assert not (_REPO / "plugins/superclaude/core/FLAGS.md").exists()


def test_known_core_set_matches_shipped():
    assert install_core.KNOWN_CORE_FILES == frozenset(install_core.list_core_files())


def _seed(path: Path, data: bytes) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return data


def test_install_never_touches_existing_files_without_force(tmp_path):
    """User rule: installers never delete, move or edit a file already in the target."""
    target = tmp_path / ".claude"
    commands_target = target / "commands" / "sc"
    seeded = {
        target / "FLAGS.md": b"retired FLAGS.md kept by the user\n",
        target / "ORCHESTRATOR.md": b"retired ORCHESTRATOR.md kept by the user\n",
        target / "RULES.md": b"user-edited RULES.md\n",
        commands_target / "README.md": b"user README in commands/sc\n",
    }
    for path, data in seeded.items():
        _seed(path, data)

    ok, message = install_core.install_core_files(target_path=target, force=False)
    assert ok, message
    ok, message = install_commands.install_commands(
        target_path=commands_target, force=False
    )
    assert ok, message

    for path, data in seeded.items():
        assert path.is_file(), f"{path} was removed or moved"
        assert path.read_bytes() == data, f"{path} was edited"


@pytest.mark.parametrize("force", [False, True])
def test_install_never_removes_unshipped_files(tmp_path, force):
    """Retired core files and commands/sc/README.md are not shipped, so even
    a forced install must leave them in place, byte for byte."""
    target = tmp_path / ".claude"
    commands_target = target / "commands" / "sc"
    seeded = {target / name: f"retired {name}\n".encode() for name in _RETIRED_CORE}
    seeded[commands_target / "README.md"] = b"user README in commands/sc\n"
    for path, data in seeded.items():
        _seed(path, data)

    ok, message = install_core.install_core_files(target_path=target, force=force)
    assert ok, message
    ok, message = install_commands.install_commands(
        target_path=commands_target, force=force
    )
    assert ok, message

    for path, data in seeded.items():
        assert path.is_file(), f"{path} was removed or moved"
        assert path.read_bytes() == data, f"{path} was edited"
