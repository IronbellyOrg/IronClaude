"""Tests for global command-to-skill installation health checks."""

from pathlib import Path

from superclaude.cli.doctor import _check_skills_installed
from superclaude.cli.install_commands import install_commands
from superclaude.cli.install_skills import install_all_skills


def _write_command(commands_dir: Path, name: str, skill_name: str) -> None:
    commands_dir.mkdir(parents=True, exist_ok=True)
    (commands_dir / f"{name}.md").write_text(
        f"# /sc:{name}\n\n## Activation\n\n> Skill {skill_name}\n",
        encoding="utf-8",
    )


def _write_skill(skills_dir: Path, directory_name: str) -> None:
    skill_dir = skills_dir / directory_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {directory_name}\n---\n",
        encoding="utf-8",
    )


def test_skill_check_fails_for_unresolved_command_dependency(tmp_path):
    skills_dir = tmp_path / "skills"
    commands_dir = tmp_path / "commands" / "sc"
    _write_command(commands_dir, "recommend", "sc-recommend")

    result = _check_skills_installed(skills_dir=skills_dir, commands_dir=commands_dir)

    assert result["passed"] is False
    assert result["details"] == ["Missing command-required skill(s): sc-recommend"]


def test_skill_check_resolves_direct_and_namespaced_dependencies(tmp_path):
    skills_dir = tmp_path / "skills"
    commands_dir = tmp_path / "commands" / "sc"
    _write_command(commands_dir, "recommend", "sc-recommend")
    _write_command(commands_dir, "roadmap", "sc:roadmap-protocol")
    _write_skill(skills_dir, "sc-recommend")
    _write_skill(skills_dir, "sc-roadmap-protocol")

    result = _check_skills_installed(skills_dir=skills_dir, commands_dir=commands_dir)

    assert result["passed"] is True
    assert result["details"][0].startswith("2 skill(s) installed:")


def test_skill_check_remains_optional_without_installed_commands(tmp_path):
    result = _check_skills_installed(
        skills_dir=tmp_path / "skills",
        commands_dir=tmp_path / "commands" / "sc",
    )

    assert result == {
        "name": "Skills installed",
        "passed": True,
        "details": ["No skills installed (optional)"],
    }


def test_isolated_install_resolves_every_command_dependency(tmp_path):
    commands_dir = tmp_path / "commands" / "sc"
    skills_dir = tmp_path / "skills"

    commands_ok, _ = install_commands(target_path=commands_dir, force=True)
    skills_ok, _ = install_all_skills(target_path=skills_dir, force=True)
    result = _check_skills_installed(skills_dir=skills_dir, commands_dir=commands_dir)

    assert commands_ok is True
    assert skills_ok is True
    assert (skills_dir / "sc-recommend" / "SKILL.md").exists()
    assert result["passed"] is True, result["details"]
