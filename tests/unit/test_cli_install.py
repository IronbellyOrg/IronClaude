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

    def test_command_activated_skill_is_not_command_backed(self):
        """A thin command cannot replace the skill it explicitly activates."""
        from superclaude.cli.install_skills import _has_corresponding_command

        assert _has_corresponding_command("sc-recommend") is False

    def test_install_all_skills_installs_command_activated_skill(self, tmp_path):
        """The global install payload includes /sc:recommend's backing skill."""
        from superclaude.cli.install_skills import install_all_skills

        target = tmp_path / "skills"
        success, message = install_all_skills(target_path=target, force=True)

        assert success is True
        assert (target / "sc-recommend" / "SKILL.md").exists()
        assert "sc-recommend → /sc:recommend" not in message

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


class TestPostReleaseCommandContract:
    """Contract tests for the /sc:post-release command-backed refactor.

    Verifies: command discovery (5.1), command install (5.2), command Activation
    text (5.3), protocol skill discovery + standalone install (5.4),
    _has_corresponding_command mapping (5.5), compatibility wrapper discovery +
    install (5.6), wrapper delegation content (5.7), and protocol skill
    frontmatter (5.8). The post-release-update skill is retained for one cycle
    as a thin deprecated wrapper (KEEP-WRAPPER branch, OQ-1).
    """

    # --- 5.1 command discovery ---
    def test_post_release_command_discoverable(self):
        """/sc:post-release command file is discoverable by list_available_commands."""
        assert "post-release" in list_available_commands()

    # --- 5.2 command install ---
    def test_post_release_command_installed_to_target(self, tmp_path):
        """post-release.md is copied into the target commands dir on install."""
        target_dir = tmp_path / "commands"
        success, _message = install_commands(target_path=target_dir, force=False)
        assert success is True
        assert (target_dir / "post-release.md").exists()

    # --- 5.3 command Activation text ---
    def test_post_release_command_activation_text(self):
        """Command Activation section contains the dev-guide handoff tokens.

        Protects both Claude Code command behavior and cli-portify/resolution.py
        Activation parsing: the ## Activation section must contain BOTH the
        ``> Skill sc:post-release-protocol`` handoff AND the prohibition sentence.
        """
        import pathlib

        cmd_path = (
            pathlib.Path(__file__).resolve().parents[2]
            / "src"
            / "superclaude"
            / "commands"
            / "post-release.md"
        )
        text = cmd_path.read_text()

        # Extract the ## Activation section (from the header to the next ## header).
        lines = text.splitlines()
        activation = []
        in_section = False
        for line in lines:
            if line.strip() == "## Activation":
                in_section = True
                continue
            if in_section and line.startswith("## "):
                break
            if in_section:
                activation.append(line)
        activation_text = "\n".join(activation)

        assert "> Skill sc:post-release-protocol" in activation_text
        assert (
            "Do NOT proceed with protocol execution using only this command file."
            in activation_text
        )

    # --- 5.4 protocol skill discovery + standalone install ---
    def test_post_release_protocol_skill_discoverable(self):
        from superclaude.cli.install_skill import list_available_skills

        assert "sc-post-release-protocol" in list_available_skills()

    def test_post_release_protocol_skill_installed_standalone(self, tmp_path):
        """Protocol skill installs standalone (not swept by served-by-command)."""
        from superclaude.cli.install_skills import install_all_skills

        target = tmp_path / "skills"
        success, _message = install_all_skills(target_path=target, force=True)
        assert success is True
        assert (target / "sc-post-release-protocol").exists()

    # --- 5.5 _has_corresponding_command mapping ---
    def test_post_release_command_skill_mapping(self):
        """Lock the command↔protocol split: bare sc-post-release is command-served;
        sc-post-release-protocol and the legacy post-release-update are NOT."""
        from superclaude.cli.install_skills import _has_corresponding_command

        assert _has_corresponding_command("sc-post-release") is True
        assert _has_corresponding_command("sc-post-release-protocol") is False
        assert _has_corresponding_command("post-release-update") is False

    # --- 5.6 compatibility wrapper discovery + install (KEEP-WRAPPER branch) ---
    def test_post_release_update_wrapper_discoverable(self):
        from superclaude.cli.install_skill import list_available_skills

        assert "post-release-update" in list_available_skills()

    def test_post_release_update_wrapper_installed(self, tmp_path):
        """The legacy non-sc- wrapper is NOT command-served, so it installs standalone."""
        from superclaude.cli.install_skills import install_all_skills

        target = tmp_path / "skills"
        success, _message = install_all_skills(target_path=target, force=True)
        assert success is True
        assert (target / "post-release-update").exists()

    # --- 5.7 wrapper delegation content ---
    def test_post_release_update_wrapper_is_thin_delegating_stub(self):
        """The wrapper retains name/allowed-tools/delegation and drops the protocol body."""
        import pathlib

        wrapper_path = (
            pathlib.Path(__file__).resolve().parents[2]
            / "src"
            / "superclaude"
            / "skills"
            / "post-release-update"
            / "SKILL.md"
        )
        text = wrapper_path.read_text()

        # (a) frontmatter name retained
        assert "name: post-release-update" in text
        # (b) Skill still in allowed-tools (delegation can fire)
        assert "Skill" in text.split("---")[1]
        # (c) delegation reference present
        assert "Skill sc:post-release-protocol" in text
        # thinness: the wrapper is short and has NO full five-workstream protocol body
        assert len(text.splitlines()) < 100

    # --- 5.8 protocol skill frontmatter ---
    def test_post_release_protocol_skill_frontmatter(self):
        import pathlib

        skill_path = (
            pathlib.Path(__file__).resolve().parents[2]
            / "src"
            / "superclaude"
            / "skills"
            / "sc-post-release-protocol"
            / "SKILL.md"
        )
        text = skill_path.read_text()
        frontmatter = text.split("---")[1]

        assert "name: sc:post-release-protocol" in frontmatter
        assert "allowed-tools:" in frontmatter
        assert "argument-hint:" in frontmatter
        assert "<version>" in frontmatter
