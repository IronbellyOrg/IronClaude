"""T01.02 / T01.08 -- CLI registration + placeholder subcommands.

Enforces AC-002 and COMP-001 from the MultiModelSwarm roadmap:

- ``swarm_group`` is imported and registered on ``superclaude.cli.main:main``.
- ``superclaude swarm`` resolves as a top-level verb -- never nested
  under ``sprint`` / ``roadmap`` / ``cleanup-audit`` / ``tasklist``.
- ``superclaude swarm --help`` exits 0 and lists all eight placeholder
  subcommands (run / status / logs / attach / kill / scaffold /
  validate / validate-lenses) per T01.08.
- Each placeholder echoes a "not yet implemented" notice and exits
  non-zero so tests catch premature use.
"""

from __future__ import annotations

import pytest
from click.testing import CliRunner

from superclaude.cli.main import main
from superclaude.cli.swarm import swarm_group

EXPECTED_PLACEHOLDERS: tuple[str, ...] = (
    "run",
    "status",
    "logs",
    "attach",
    "kill",
    "scaffold",
    "validate",
    "validate-lenses",
)

# Subset still in placeholder-message form. T02.19 replaced ``validate``
# with the real ``commands.validate_cmd``; T02.20 replaced
# ``validate-lenses`` with ``commands.validate_lenses_cmd``; T03.01
# replaced ``run`` with ``commands.run_cmd``; T07.04 replaced
# ``status`` with ``commands.status_cmd``; T07.05 replaced ``logs``
# with ``commands.logs_cmd``; T07.07 replaced ``attach`` with
# ``commands.attach_cmd``; T07.08 replaced ``kill`` with
# ``commands.kill_cmd``; T07.09 replaced ``scaffold`` with
# ``commands.scaffold_cmd``. None of those subcommands echo "not yet
# implemented" any more -- ``validate`` emits Click's missing-argument
# usage error without a JOBSPEC_PATH and real diagnostics with one;
# ``validate-lenses`` runs the COMP-023 validator over the bundled
# LENSES dict; ``run`` resolves an input mode and invokes preflight ->
# dispatch; ``status`` reads ``.swarm-state.json`` and reports phase +
# terminal status; ``logs`` dumps / tails ``execution-log.{jsonl,md}``;
# ``attach`` re-attaches to a detached ``swarm-<job_id>`` tmux session;
# ``kill`` terminates the detached tmux session and emits the killed
# terminal-state artifacts; ``scaffold`` emits a starter DM-001 JobSpec
# for the named lens. The parametrized placeholder-exit test below
# iterates this narrower tuple so it doesn't regress against the real
# commands. Other tests (help-listing, group registration, count) still
# iterate the full ``EXPECTED_PLACEHOLDERS`` tuple because every name
# remains present on ``swarm_group``.
_REPLACED_BY_REAL_COMMAND: frozenset[str] = frozenset(
    {
        "run",
        "status",
        "logs",
        "validate",
        "validate-lenses",
        "attach",
        "kill",
        "scaffold",
    }
)
STILL_PLACEHOLDER_SUBCOMMANDS: tuple[str, ...] = tuple(
    name for name in EXPECTED_PLACEHOLDERS if name not in _REPLACED_BY_REAL_COMMAND
)


def test_swarm_group_is_top_level_command() -> None:
    """``swarm`` is registered directly on the root group (AC-002)."""
    commands = main.commands
    assert "swarm" in commands, (
        f"swarm not registered as top-level verb on main; "
        f"got commands: {sorted(commands)}"
    )
    assert commands["swarm"] is swarm_group


def test_swarm_not_nested_under_other_groups() -> None:
    """AC-002 forbids nesting ``swarm`` under sprint/roadmap/etc."""
    forbidden_parents = ("sprint", "roadmap", "cleanup-audit", "tasklist")
    for parent in forbidden_parents:
        parent_group = main.commands.get(parent)
        if parent_group is None:
            continue
        children = getattr(parent_group, "commands", {})
        assert "swarm" not in children, (
            f"swarm must not be nested under '{parent}'; "
            "AC-002 forbids non-top-level placement."
        )


def test_swarm_help_exits_zero() -> None:
    """``superclaude swarm --help`` is invokable and exits 0."""
    runner = CliRunner()
    result = runner.invoke(main, ["swarm", "--help"])
    assert result.exit_code == 0, result.output
    assert "swarm" in result.output.lower()


def test_swarm_help_lists_all_eight_placeholders() -> None:
    """T01.08 -- ``swarm --help`` advertises every placeholder name."""
    runner = CliRunner()
    result = runner.invoke(main, ["swarm", "--help"])
    assert result.exit_code == 0, result.output
    missing = [name for name in EXPECTED_PLACEHOLDERS if name not in result.output]
    assert not missing, (
        f"swarm --help missing placeholders {missing}; got:\n{result.output}"
    )


def test_swarm_group_registers_all_eight_placeholders() -> None:
    """T01.08 -- the Click group object has all eight subcommands."""
    registered = set(swarm_group.commands)
    expected = set(EXPECTED_PLACEHOLDERS)
    assert expected.issubset(registered), (
        f"swarm_group missing placeholders {expected - registered}; "
        f"registered: {sorted(registered)}"
    )


@pytest.mark.parametrize("subcommand", STILL_PLACEHOLDER_SUBCOMMANDS)
def test_placeholder_exits_non_zero_with_message(subcommand: str) -> None:
    """T01.08 -- placeholders echo "not yet implemented" and exit non-zero."""
    runner = CliRunner()
    result = runner.invoke(main, ["swarm", subcommand])
    assert result.exit_code != 0, (
        f"placeholder '{subcommand}' must exit non-zero so tests catch "
        f"premature use; got exit_code=0 with output:\n{result.output}"
    )
    combined = result.output or ""
    assert "not yet implemented" in combined.lower(), (
        f"placeholder '{subcommand}' must echo 'not yet implemented'; "
        f"got output={combined!r}"
    )
    assert subcommand in combined, (
        f"placeholder '{subcommand}' message must name the subcommand; "
        f"got: {combined!r}"
    )


def test_swarm_module_imports_without_error() -> None:
    """T01.08 AC -- module import is side-effect-free beyond registration."""
    # Re-import to confirm no top-level raise; the import at module load
    # would have already failed the test session otherwise.
    import importlib

    import superclaude.cli.swarm as swarm_pkg

    # ``importlib.reload`` re-executes ``__init__`` and rebinds the module's
    # ``swarm_group`` attribute to a FRESH Click group. ``superclaude.cli.main``
    # already registered the ORIGINAL group at import time, so leaving the
    # reloaded object in ``sys.modules`` pollutes global state -- a later
    # ``main.commands["swarm"] is swarm_group`` identity check (see
    # ``test_non_claude_caller``) would then compare the original group against
    # the reloaded one and spuriously fail depending on collection order.
    # Restore the original binding in ``finally`` so the reload stays local.
    original_group = swarm_pkg.swarm_group
    try:
        reloaded = importlib.reload(swarm_pkg)
        assert hasattr(reloaded, "swarm_group")
        assert set(EXPECTED_PLACEHOLDERS).issubset(set(reloaded.swarm_group.commands))
    finally:
        swarm_pkg.swarm_group = original_group
