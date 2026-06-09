"""CLI smoke tests for ``superclaude reflect`` -- help/flags/dry-run/print-command.

Mirrors ``tests/cli/prd/test_cli_smoke.py``. The dry-run and print-command paths
must never construct ``ClaudeProcess`` (FR-12), asserted via ``assert_not_called``.
"""

from __future__ import annotations

from unittest.mock import patch

from superclaude.cli.reflect.commands import reflect_group

_SPEC9_FLAGS = [
    "--tmux",
    "--print-command",
    "--no-promote",
    "--promote",
    "--timeout",
    "--depth",
    "--output",
    "--allow-single-vendor",
    "--dry-run",
    "--resume",
]


def test_group_help_shows_run(cli_runner) -> None:
    result = cli_runner.invoke(reflect_group, ["--help"])
    assert result.exit_code == 0
    assert "run" in result.output


def test_run_help_shows_all_spec9_flags(cli_runner) -> None:
    result = cli_runner.invoke(reflect_group, ["run", "--help"])
    assert result.exit_code == 0
    for flag in _SPEC9_FLAGS:
        assert flag in result.output, f"missing option in help: {flag}"


def test_dry_run_never_launches(cli_runner, temp_tasklist, patch_git) -> None:
    """--dry-run derives + previews but never constructs ClaudeProcess (case 9)."""
    with patch("superclaude.cli.reflect.runner.ClaudeProcess") as mock_cls:
        result = cli_runner.invoke(
            reflect_group, ["run", str(temp_tasklist), "--dry-run"]
        )
    assert result.exit_code == 0
    mock_cls.assert_not_called()


def test_print_command_prints_and_never_launches(
    cli_runner, temp_tasklist, patch_git
) -> None:
    """--print-command prints the composed command and never launches (case 13)."""
    with patch("superclaude.cli.reflect.runner.ClaudeProcess") as mock_cls:
        result = cli_runner.invoke(
            reflect_group, ["run", str(temp_tasklist), "--print-command"]
        )
    assert result.exit_code == 0
    assert "/sc:reflect --mode post" in result.output
    assert "claude --print" in result.output
    mock_cls.assert_not_called()


def test_nonexistent_tasklist_is_nonzero(cli_runner) -> None:
    """A nonexistent tasklist path exits non-zero (Click exists=True guard)."""
    result = cli_runner.invoke(reflect_group, ["run", "/no/such/tasklist-xyz.md"])
    assert result.exit_code != 0
