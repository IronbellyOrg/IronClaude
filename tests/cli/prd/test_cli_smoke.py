"""CLI integration smoke tests for ``superclaude prd``.

Verifies the Click command surface is wired up correctly and that
dry-run mode validates config without launching subprocesses.
"""

from __future__ import annotations

from click.testing import CliRunner

from superclaude.cli.prd.commands import prd_group


def _runner() -> CliRunner:
    return CliRunner()


class TestPrdCliSmoke:
    """Smoke tests for prd CLI surface."""

    def test_prd_help_shows_subcommands(self) -> None:
        """``superclaude prd --help`` lists run and resume."""
        result = _runner().invoke(prd_group, ["--help"])
        assert result.exit_code == 0
        assert "run" in result.output
        assert "resume" in result.output

    def test_prd_run_help_shows_options(self) -> None:
        """``superclaude prd run --help`` lists all expected options."""
        result = _runner().invoke(prd_group, ["run", "--help"])
        assert result.exit_code == 0
        for flag in ["--product", "--where", "--output", "--tier", "--max-turns",
                     "--model", "--dry-run", "--debug"]:
            assert flag in result.output, f"Missing option: {flag}"

    def test_prd_resume_help_shows_options(self) -> None:
        """``superclaude prd resume --help`` lists expected options."""
        result = _runner().invoke(prd_group, ["resume", "--help"])
        assert result.exit_code == 0
        for flag in ["--max-turns", "--model", "--debug"]:
            assert flag in result.output, f"Missing option: {flag}"
        assert "STEP_ID" in result.output

    def test_prd_run_dry_run_exits_zero(self) -> None:
        """``superclaude prd run "test" --dry-run`` exits with code 0."""
        result = _runner().invoke(prd_group, ["run", "test", "--dry-run"])
        assert result.exit_code == 0
        assert "Dry run" in result.output

    def test_prd_run_invalid_tier_exits_nonzero(self) -> None:
        """``superclaude prd run "test" --tier invalid`` exits with non-zero."""
        result = _runner().invoke(prd_group, ["run", "test", "--tier", "invalid"])
        assert result.exit_code != 0

    def test_prd_run_dry_run_validates_config(self) -> None:
        """Dry-run mode validates config fields without subprocess launch."""
        result = _runner().invoke(
            prd_group,
            ["run", "Build a user auth system", "--product", "my-app",
             "--tier", "heavyweight", "--dry-run"],
        )
        assert result.exit_code == 0
        assert "heavyweight" in result.output
        assert "Build a user auth system" in result.output
