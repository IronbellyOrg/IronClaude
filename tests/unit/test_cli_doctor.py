"""Tests for global command-to-skill installation health checks."""

import json
from pathlib import Path

import pytest

from superclaude.cli.doctor import _check_ccsession, _check_skills_installed
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


@pytest.fixture
def ccsession_home(tmp_path, monkeypatch):
    skill = tmp_path / ".claude/skills/ccsession-tag"
    (skill / "hooks").mkdir(parents=True)
    (skill / "SKILL.md").write_text("skill")
    (skill / "ccsession").write_text("wrapper")
    (skill / "hooks/session-start.sh").write_text("hook")
    (tmp_path / ".claude/ccsession.env").write_text("secret-value")
    settings = tmp_path / ".claude/settings.json"
    settings.write_text(
        json.dumps(
            {
                "hooks": {
                    "SessionStart": [
                        {
                            "matcher": "startup|resume",
                            "hooks": [
                                {
                                    "command": "~/.claude/skills/ccsession-tag/hooks/session-start.sh"
                                }
                            ],
                        }
                    ]
                }
            }
        )
    )
    bin_path = tmp_path / ".local/bin/ccsession"
    bin_path.parent.mkdir(parents=True)
    bin_path.symlink_to(skill / "ccsession")
    monkeypatch.setenv("PATH", str(bin_path.parent))
    return tmp_path


@pytest.mark.parametrize(
    "missing",
    [
        ".claude/skills/ccsession-tag/ccsession",
        ".claude/skills/ccsession-tag/hooks/session-start.sh",
        ".claude/ccsession.env",
        ".local/bin/ccsession",
        ".claude/settings.json",
    ],
)
def test_ccsession_doctor_reports_missing(ccsession_home, missing):
    (ccsession_home / missing).unlink()
    result = _check_ccsession(home=ccsession_home)
    assert result["passed"] is False
    assert "secret-value" not in str(result)


def test_ccsession_doctor_rejects_env_directory(ccsession_home):
    env = ccsession_home / ".claude/ccsession.env"
    env.unlink()
    env.mkdir()
    result = _check_ccsession(home=ccsession_home)
    assert result["passed"] is False
    assert str(env) in result["details"]


def test_ccsession_doctor_reports_missing_skill(ccsession_home):
    (ccsession_home / ".claude/skills/ccsession-tag").rename(
        ccsession_home / "removed-skill"
    )
    result = _check_ccsession(home=ccsession_home)
    assert result["passed"] is False
    assert "ccsession-tag" in str(result["details"])


@pytest.mark.parametrize("kind", ["file", "foreign_symlink"])
def test_ccsession_doctor_reports_collision(ccsession_home, kind):
    binary = ccsession_home / ".local/bin/ccsession"
    binary.unlink()
    if kind == "file":
        binary.write_text("user file")
    else:
        binary.symlink_to(ccsession_home / "foreign")
    result = _check_ccsession(home=ccsession_home)
    assert result["passed"] is False
    assert "collision" in str(result["details"])


def test_ccsession_doctor_accepts_placeholder_env_and_warns_about_path(
    ccsession_home, monkeypatch
):
    (ccsession_home / ".claude/ccsession.env").write_text("# placeholder")
    monkeypatch.setenv("PATH", "/usr/bin")
    result = _check_ccsession(home=ccsession_home)
    assert result["passed"] is True
    assert "warning" in result["name"]
    assert "placeholder" not in str(result)


def test_ccsession_doctor_accepts_install_sh_legacy_hook(ccsession_home):
    settings = ccsession_home / ".claude/settings.json"
    command = (
        f'bash "{ccsession_home}/.claude/skills/ccsession-tag/hooks/session-start.sh"'
    )
    settings.write_text(
        json.dumps({"hooks": {"SessionStart": [{"hooks": [{"command": command}]}]}})
    )
    assert _check_ccsession(home=ccsession_home)["passed"] is True
    settings.write_text("malformed")
    assert _check_ccsession(home=ccsession_home)["passed"] is False
