"""Keep help descriptions and install examples aligned with the shipped package."""

import re
from pathlib import Path

import pytest
from click.testing import CliRunner

import superclaude
from superclaude.cli.install_skill import install_skill_command
from superclaude.cli.main import main


@pytest.fixture(autouse=True)
def isolated_home(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / ".claude"))


def test_update_help_lists_all_updated_components():
    result = CliRunner().invoke(main, ["update", "--help"])

    assert result.exit_code == 0, result.output
    help_text = " ".join(result.output.split())
    for component in (
        "core framework files",
        "slash commands",
        "agents",
        "skills",
        "session setup",
        "hooks",
        "templates",
        "user setup",
    ):
        assert component in help_text


def test_install_skill_help_examples_are_packaged_and_installable(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["install-skill", "--help"], terminal_width=240)

    assert result.exit_code == 0, result.output
    names = re.findall(r"(?:e.g., |superclaude install-skill )([\w-]+)", result.output)
    assert len(names) == 3, result.output
    assert len(set(names)) == 1, names
    name = names[0]
    assert f"superclaude install-skill {name} --target ~/.claude/skills --force" in (
        result.output
    )
    assert f"e.g., '{name}'" in install_skill_command.__doc__
    source = Path(superclaude.__file__).resolve().parent / "skills" / name
    assert (source / "SKILL.md").is_file()
    target = tmp_path / "skills"

    for extra_args in ([], ["--force"]):
        installed = runner.invoke(
            main, ["install-skill", name, "--target", str(target), *extra_args]
        )
        assert installed.exit_code == 0, installed.output
        for original in source.rglob("*"):
            if original.is_file():
                assert (target / name / original.relative_to(source)).read_bytes() == (
                    original.read_bytes()
                )
        # The second invocation must replace the existing payload, not skip it.
        if not extra_args:
            (target / name / "SKILL.md").write_text("changed disposable copy\n")
