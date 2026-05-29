"""Tests for the top-level ``superclaude eval`` Click group (COMP-001 / T04.09 / D-0071).

T04.09 registers the four-subcommand surface (``run``, ``list``,
``describe``, ``doctor``) on :data:`eval_group` so the group's
``--help`` already advertises the full FR-CLI1 / FR-CLI2 / FR-CLI3 /
FR-CLI4 surface. Tests pin the three acceptance bullets from the
phase-4 tasklist:

1. ``superclaude eval --help`` lists ``run``, ``list``, ``describe``,
   and ``doctor`` as subcommands.
2. The group is registered at the ``superclaude`` CLI entry point so
   existing top-level commands remain reachable.
3. ``superclaude --help`` continues to surface the ``eval`` group from
   the T01.26 / FR-G3 wiring.
"""

from __future__ import annotations

from click.testing import CliRunner

from superclaude.cli.eval.commands import eval_group
from superclaude.cli.main import main

# ---------------------------------------------------------------------------
# Group surface — four subcommands registered in the documented order
# ---------------------------------------------------------------------------


EXPECTED_SUBCOMMANDS: tuple[str, ...] = ("describe", "doctor", "list", "run")
"""Lexicographic subcommand set the group MUST expose at T04.09.

Click's default ``--help`` rendering sorts subcommands alphabetically;
asserting against the sorted set rather than the registration order
keeps the test resilient to source-file reorderings that do not change
the user-visible surface.
"""


def test_eval_group_registers_four_subcommands() -> None:
    """The group object directly exposes the four T04.09 subcommands."""

    assert set(eval_group.commands.keys()) == set(EXPECTED_SUBCOMMANDS)


def test_eval_group_help_lists_all_four_subcommands() -> None:
    """``superclaude eval --help`` advertises all four subcommands."""

    runner = CliRunner()
    result = runner.invoke(eval_group, ["--help"])
    assert result.exit_code == 0, result.output
    for name in EXPECTED_SUBCOMMANDS:
        assert name in result.output, (
            f"subcommand {name!r} missing from `eval --help` output:\n{result.output}"
        )


def test_top_level_main_lists_eval_group() -> None:
    """T01.26 / FR-G3 wiring: ``superclaude --help`` surfaces the group."""

    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0, result.output
    assert "eval" in result.output, (
        "top-level `superclaude --help` no longer lists the eval group; "
        "T01.26 wiring has regressed.\n"
        f"{result.output}"
    )


def test_eval_invoked_through_main_lists_subcommands() -> None:
    """Help dispatched through the entry point reaches the group surface."""

    runner = CliRunner()
    result = runner.invoke(main, ["eval", "--help"])
    assert result.exit_code == 0, result.output
    for name in EXPECTED_SUBCOMMANDS:
        assert name in result.output, (
            f"subcommand {name!r} missing from `superclaude eval --help` "
            f"output:\n{result.output}"
        )


# ---------------------------------------------------------------------------
# ``run`` subcommand help surface
# ---------------------------------------------------------------------------


def test_run_help_lists_subcommand() -> None:
    """``eval run --help`` resolves without invoking the body."""

    runner = CliRunner()
    result = runner.invoke(eval_group, ["run", "--help"])
    assert result.exit_code == 0, result.output
    assert "run" in result.output
