"""CLI registration surface test for the `recommend` group (CliRunner, no subprocess)."""

from __future__ import annotations

import pytest
from click.testing import CliRunner

from superclaude.cli.main import main


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_recommend_group_registered(runner: CliRunner) -> None:
    """`superclaude --help` exposes `recommend` as a top-level group."""
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0, result.output
    assert "recommend" in result.output


def test_recommend_help_lists_subcommands(runner: CliRunner) -> None:
    """`superclaude recommend --help` is reachable and lists the helper subcommands."""
    result = runner.invoke(main, ["recommend", "--help"])
    assert result.exit_code == 0, result.output
    for name in ("cache", "telemetry", "eval", "dispatch"):
        assert name in result.output, (
            f"expected `{name}` in recommend --help:\n{result.output}"
        )


def test_recommend_eval_run_exposes_mode_choice(runner: CliRunner) -> None:
    """The `--eval`-bearing `eval run` subcommand exposes the constrained mode choice."""
    result = runner.invoke(main, ["recommend", "eval", "run", "--help"])
    assert result.exit_code == 0, result.output
    assert "--mode" in result.output
    for mode in ("none", "quick", "normal", "deep"):
        assert mode in result.output
