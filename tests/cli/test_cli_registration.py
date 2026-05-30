"""Regression tests for the `superclaude` CLI command surface (T01.26 / D-0022).

FR-G3 mandates that the cliEval harness register the `eval` Click group at
the existing CLI entry point **additively** — no pre-existing command path
may change name, help text shape, or top-level registration state.

These tests pin both halves of the contract:

1. `superclaude --help` lists `eval` as a top-level subcommand group, and
   `superclaude eval --help` lists the M1 subcommands (`list`, `describe`,
   `doctor`). Additional `eval` subcommands (`run`, …) land per their
   milestones; the M1 set is the floor.
2. Every pre-existing top-level command is still registered after the
   `eval` group landed. The expected roster is asserted as a fixed set so
   any accidental removal or rename trips the test.

The suite uses Click's :class:`CliRunner` so it can exercise the live
`main` group without spawning a subprocess.
"""

from __future__ import annotations

import pytest
from click.testing import CliRunner

from superclaude.cli.main import main

# Pre-existing top-level commands as of the moment the `eval` group landed.
# The set is intentionally a frozen snapshot — adding or removing a top-level
# command should force a deliberate test update.
EXPECTED_TOP_LEVEL_COMMANDS: frozenset[str] = frozenset(
    {
        "cleanup-audit",
        "cli-portify",
        "doctor",
        "eval",
        "install",
        "install-skill",
        "mcp",
        "prd",
        "roadmap",
        "sprint",
        "tasklist",
        "update",
        "version",
    }
)

# M1 subcommands that MUST appear under `superclaude eval` per FR-CLI2/3/4.
# Later milestones add `run` (FR-CLI1, M4); the M1 floor is asserted here.
EXPECTED_EVAL_SUBCOMMANDS_M1: frozenset[str] = frozenset({"describe", "doctor", "list"})


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_top_level_help_lists_eval_group(runner: CliRunner) -> None:
    """`superclaude --help` exposes `eval` as a subcommand group (FR-G3 AC)."""
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0, result.output
    assert "eval" in result.output
    # The group's docstring is the source-of-truth help summary; confirm a
    # stable fragment from `commands.eval_group.__doc__` is rendered so a
    # rename of the group also fails this test.
    assert "cliEval real-eval harness" in result.output


def test_top_level_command_roster_unchanged(runner: CliRunner) -> None:
    """Every pre-existing top-level command is still registered (regression)."""
    actual = frozenset(main.commands.keys())
    missing = EXPECTED_TOP_LEVEL_COMMANDS - actual
    unexpected = actual - EXPECTED_TOP_LEVEL_COMMANDS
    assert not missing, f"missing top-level commands: {sorted(missing)}"
    assert not unexpected, (
        "unexpected top-level commands present (update "
        f"EXPECTED_TOP_LEVEL_COMMANDS deliberately): {sorted(unexpected)}"
    )


def test_eval_group_help_lists_m1_subcommands(runner: CliRunner) -> None:
    """`superclaude eval --help` lists the M1 subcommands (FR-CLI2/3/4)."""
    result = runner.invoke(main, ["eval", "--help"])
    assert result.exit_code == 0, result.output
    for name in EXPECTED_EVAL_SUBCOMMANDS_M1:
        assert name in result.output, (
            f"expected `{name}` in `eval --help` output:\n{result.output}"
        )


def test_eval_group_registers_m1_subcommands_in_click() -> None:
    """The `eval` group exposes the M1 subcommands at the Click level.

    Complements the help-text check above by reaching into Click's
    command registry, so a help-text-only stub (e.g. an alias that
    docstrings the M1 names but does not implement them) cannot pass.
    """
    eval_group = main.commands["eval"]
    actual = frozenset(eval_group.commands.keys())  # type: ignore[union-attr]
    missing = EXPECTED_EVAL_SUBCOMMANDS_M1 - actual
    assert not missing, f"missing eval subcommands: {sorted(missing)}"


def test_pre_existing_command_help_still_invokable(runner: CliRunner) -> None:
    """Smoke: pre-existing commands still print help with exit 0.

    Asserts the lightweight non-destructive contract that landing the
    `eval` group did not break any pre-existing command's `--help`
    plumbing.
    """
    for name in EXPECTED_TOP_LEVEL_COMMANDS - {"eval"}:
        result = runner.invoke(main, [name, "--help"])
        assert result.exit_code == 0, (
            f"`{name} --help` exited {result.exit_code}:\n{result.output}"
        )
