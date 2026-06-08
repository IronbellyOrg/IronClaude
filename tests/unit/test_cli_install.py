"""
Unit tests for CLI install command

Tests the command installation functionality.
"""

from superclaude.cli.install_commands import (
    install_commands,
    list_available_commands,
    list_installed_commands,
)


class TestInstallCommands:
    """Test suite for install commands functionality"""

    def test_list_available_commands(self):
        """Test listing available commands"""
        commands = list_available_commands()

        assert isinstance(commands, list)
        assert len(commands) > 0
        assert "research" in commands
        assert "index-repo" in commands

    def test_install_commands_to_temp_dir(self, tmp_path):
        """Test installing commands to a temporary directory"""
        target_dir = tmp_path / "commands"

        success, message = install_commands(target_path=target_dir, force=False)

        assert success is True
        assert "Installed" in message
        assert target_dir.exists()

        # Check that command files were copied
        command_files = list(target_dir.glob("*.md"))
        assert len(command_files) > 0

        # Verify specific commands
        assert (target_dir / "research.md").exists()
        assert (target_dir / "index-repo.md").exists()

    def test_install_commands_skip_existing(self, tmp_path):
        """Test that existing commands are skipped without --force"""
        target_dir = tmp_path / "commands"

        # First install
        success1, message1 = install_commands(target_path=target_dir, force=False)
        assert success1 is True

        # Second install without force
        success2, message2 = install_commands(target_path=target_dir, force=False)
        assert success2 is True
        assert "Skipped" in message2

    def test_install_commands_force_reinstall(self, tmp_path):
        """Test force reinstall of existing commands"""
        target_dir = tmp_path / "commands"

        # First install
        success1, message1 = install_commands(target_path=target_dir, force=False)
        assert success1 is True

        # Modify a file
        research_file = target_dir / "research.md"
        research_file.write_text("modified")
        assert research_file.read_text() == "modified"

        # Force reinstall
        success2, message2 = install_commands(target_path=target_dir, force=True)
        assert success2 is True
        assert "Installed" in message2

        # Verify file was overwritten
        content = research_file.read_text()
        assert content != "modified"
        assert "research" in content.lower()

    def test_list_installed_commands(self, tmp_path):
        """Test listing installed commands"""
        target_dir = tmp_path / "commands"

        # Before install
        # Note: list_installed_commands checks ~/.claude/commands by default
        # We can't easily test this without mocking, so just verify it returns a list
        installed = list_installed_commands()
        assert isinstance(installed, list)

        # After install to temp dir
        install_commands(target_path=target_dir, force=False)

        # Verify files exist
        command_files = list(target_dir.glob("*.md"))
        assert len(command_files) > 0

    def test_install_commands_creates_target_directory(self, tmp_path):
        """Test that target directory is created if it doesn't exist"""
        target_dir = tmp_path / "nested" / "commands"

        assert not target_dir.exists()

        success, message = install_commands(target_path=target_dir, force=False)

        assert success is True
        assert target_dir.exists()

    def test_available_commands_format(self):
        """Test that available commands have expected format"""
        commands = list_available_commands()

        # Should be list of strings
        assert all(isinstance(cmd, str) for cmd in commands)

        # Should not include file extensions
        assert all(not cmd.endswith(".md") for cmd in commands)

        # Should be sorted
        assert commands == sorted(commands)

    def test_research_command_exists(self, tmp_path):
        """Test that research command specifically gets installed"""
        target_dir = tmp_path / "commands"

        install_commands(target_path=target_dir, force=False)

        research_file = target_dir / "research.md"
        assert research_file.exists()

        content = research_file.read_text()
        assert "research" in content.lower()
        assert len(content) > 100  # Should have substantial content

    def test_all_expected_commands_available(self):
        """Test that all expected commands are available"""
        commands = list_available_commands()

        expected = ["agent", "index-repo", "recommend", "research"]

        for expected_cmd in expected:
            assert expected_cmd in commands, (
                f"Expected command '{expected_cmd}' not found"
            )


class TestInstallCommandsEdgeCases:
    """Test edge cases and error handling"""

    def test_install_to_nonexistent_parent(self, tmp_path):
        """Test installation to path with nonexistent parent directories"""
        target_dir = tmp_path / "a" / "b" / "c" / "commands"

        success, message = install_commands(target_path=target_dir, force=False)

        assert success is True
        assert target_dir.exists()

    def test_empty_target_directory_ok(self, tmp_path):
        """Test that installation works with empty target directory"""
        target_dir = tmp_path / "commands"
        target_dir.mkdir()

        success, message = install_commands(target_path=target_dir, force=False)

        assert success is True


def test_cli_integration():
    """
    Integration test: verify CLI can import and use install functions

    This tests that the CLI main.py can successfully import the functions
    """
    from superclaude.cli.install_commands import (
        list_available_commands,
    )

    # Should not raise ImportError
    commands = list_available_commands()
    assert len(commands) > 0


class TestProtocolSkillInstallMapping:
    """F2 regression guard (sc:reflect 2026-06-03): protocol skills stay standalone.

    The installer's ``_has_corresponding_command`` strips ONLY the ``sc-`` prefix.
    Protocol skills are named ``sc-<command>-protocol`` (e.g. sc-roadmap-protocol
    backing commands/roadmap.md) and are therefore NOT command-backed -- they are
    installed standalone, which is required because each /sc:<command> command
    activates its skill by name via ``Skill sc:<command>-protocol``.

    These tests would FAIL if a future change generalized the match to also strip
    a ``-protocol`` suffix (which would sweep every protocol skill into
    ``served_by_command`` and remove its standalone install).
    """

    def test_new_init_lite_protocol_is_not_command_backed(self):
        from superclaude.cli.install_skills import _has_corresponding_command

        assert _has_corresponding_command("sc-init-lite-protocol") is False

    def test_sample_existing_protocol_skills_not_command_backed(self):
        from superclaude.cli.install_skills import _has_corresponding_command

        for name in ("sc-roadmap-protocol", "sc-reflect-protocol", "sc-task-protocol"):
            assert _has_corresponding_command(name) is False, name

    def test_bare_sc_command_mapping_still_works(self):
        """The strip-``sc-`` behavior is intact: a hypothetical bare sc-<cmd> maps."""
        from superclaude.cli.install_skills import _has_corresponding_command

        # commands/roadmap.md exists, so a bare "sc-roadmap" WOULD be command-backed.
        assert _has_corresponding_command("sc-roadmap") is True
        # Non-sc- skills are never command-backed.
        assert _has_corresponding_command("some-other-skill") is False

    def test_no_available_protocol_skill_is_command_backed(self):
        """Across the real skill roster, zero ``sc-*-protocol`` skills are swept."""
        from superclaude.cli.install_skills import (
            _has_corresponding_command,
            list_available_skills,
        )

        available = list_available_skills()
        protocol_skills = [
            s for s in available if s.startswith("sc-") and s.endswith("-protocol")
        ]
        assert protocol_skills, (
            "expected at least one sc-*-protocol skill in the roster"
        )
        swept = [s for s in protocol_skills if _has_corresponding_command(s)]
        assert swept == [], (
            f"protocol skills wrongly treated as command-backed: {swept}"
        )

    def test_install_all_skills_keeps_protocol_skills_standalone(self, tmp_path):
        """End-to-end: protocol skills are installed standalone, not removed."""
        from superclaude.cli.install_skills import (
            install_all_skills,
            list_available_skills,
        )

        target = tmp_path / "skills"
        success, _message = install_all_skills(target_path=target, force=True)
        assert success is True

        available = set(list_available_skills())
        for name in ("sc-init-lite-protocol", "sc-roadmap-protocol"):
            if name in available:
                assert (target / name).exists(), (
                    f"{name} should be installed standalone"
                )
