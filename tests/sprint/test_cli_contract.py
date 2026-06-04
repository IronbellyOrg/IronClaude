"""T07.03 — CLI contract validation for all subcommands.

Tests that all 5 subcommands (run, attach, status, logs, kill) exist,
respond to --help, and expose documented options.
"""

from __future__ import annotations

from click.testing import CliRunner

from superclaude.cli.sprint.commands import sprint_group


class TestCLIContract:
    """T07.03: All 5 subcommands match documented CLI contract."""

    def setup_method(self):
        self.runner = CliRunner()

    def test_sprint_group_help(self):
        result = self.runner.invoke(sprint_group, ["--help"])
        assert result.exit_code == 0
        assert "sprint" in result.output.lower()
        # All subcommands should be listed
        assert "run" in result.output
        assert "attach" in result.output
        assert "status" in result.output
        assert "logs" in result.output
        assert "kill" in result.output

    def test_run_help(self):
        result = self.runner.invoke(sprint_group, ["run", "--help"])
        assert result.exit_code == 0
        # Required argument
        assert "INDEX_PATH" in result.output or "index_path" in result.output.lower()
        # Documented options
        assert "--start" in result.output
        assert "--end" in result.output
        assert "--max-turns" in result.output
        assert "--model" in result.output
        assert "--dry-run" in result.output
        assert "--no-tmux" in result.output
        assert "--permission-flag" in result.output

    def test_run_help_permission_choices(self):
        result = self.runner.invoke(sprint_group, ["run", "--help"])
        assert result.exit_code == 0
        assert "--dangerously-skip-permissions" in result.output
        assert "--allow-hierarchical-permissions" in result.output

    def test_hidden_internal_option_not_exposed(self):
        result = self.runner.invoke(sprint_group, ["run", "--help"])
        assert result.exit_code == 0
        assert "--tmux-session-name" not in result.output

    def test_attach_help(self):
        result = self.runner.invoke(sprint_group, ["attach", "--help"])
        assert result.exit_code == 0
        assert "tmux" in result.output.lower() or "session" in result.output.lower()

    def test_status_help(self):
        result = self.runner.invoke(sprint_group, ["status", "--help"])
        assert result.exit_code == 0
        assert "status" in result.output.lower()

    def test_logs_help(self):
        result = self.runner.invoke(sprint_group, ["logs", "--help"])
        assert result.exit_code == 0
        assert "--lines" in result.output or "-n" in result.output
        assert "--follow" in result.output or "-f" in result.output

    def test_logs_help_defaults(self):
        result = self.runner.invoke(sprint_group, ["logs", "--help"])
        assert result.exit_code == 0
        assert "50" in result.output  # default lines

    def test_kill_help(self):
        result = self.runner.invoke(sprint_group, ["kill", "--help"])
        assert result.exit_code == 0
        assert "--force" in result.output

    def test_all_subcommands_exit_cleanly(self):
        """All 5 subcommands respond to --help with exit code 0."""
        for subcmd in ["run", "attach", "status", "logs", "kill"]:
            result = self.runner.invoke(sprint_group, [subcmd, "--help"])
            assert result.exit_code == 0, f"{subcmd} --help failed: {result.output}"

    def test_invalid_subcommand(self):
        result = self.runner.invoke(sprint_group, ["nonexistent"])
        assert result.exit_code != 0


class TestRerunTasksContract:
    """rerun-tasks subcommand matches its documented CLI contract."""

    def setup_method(self):
        self.runner = CliRunner()

    def test_rerun_tasks_listed_in_group_help(self):
        result = self.runner.invoke(sprint_group, ["--help"])
        assert result.exit_code == 0
        assert "rerun-tasks" in result.output

    def test_rerun_tasks_help_exposes_documented_options(self):
        result = self.runner.invoke(sprint_group, ["rerun-tasks", "--help"])
        assert result.exit_code == 0
        # Required argument
        assert "INDEX_PATH" in result.output or "index_path" in result.output.lower()
        # Documented options
        assert "--phase" in result.output
        assert "--tasks" in result.output
        assert "--from-reflect-report" in result.output
        assert "--merge-back" in result.output
        assert "--no-merge-back" in result.output
        assert "--dry-run" in result.output
        assert "--include-transitive" in result.output
        assert "--ignore-deps" in result.output
        assert "--force-merge" in result.output
        assert "--allow-loop" in result.output
        assert "--no-verify-checkpoints" in result.output
        assert "--bundle-dir" in result.output
        assert "--restore" in result.output

    def test_rerun_tasks_reflect_report_mutually_exclusive(self):
        # CLAUDE.md is a guaranteed-existing path so the exists=True checks pass
        # and execution reaches the mutual-exclusion guard.
        result = self.runner.invoke(
            sprint_group,
            [
                "rerun-tasks",
                "CLAUDE.md",
                "--from-reflect-report",
                "CLAUDE.md",
                "--tasks",
                "T1",
            ],
        )
        assert result.exit_code != 0
        assert "mutually exclusive" in result.output

    def test_rerun_tasks_requires_phase_without_reflect_report(self):
        result = self.runner.invoke(sprint_group, ["rerun-tasks", "CLAUDE.md"])
        assert result.exit_code != 0
        assert "--phase is required" in result.output

    def test_rerun_tasks_help_exits_cleanly(self):
        result = self.runner.invoke(sprint_group, ["rerun-tasks", "--help"])
        assert result.exit_code == 0, f"rerun-tasks --help failed: {result.output}"
