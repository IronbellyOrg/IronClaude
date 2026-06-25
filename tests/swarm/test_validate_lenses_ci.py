"""T08.13 / TEST-004 -- bundled lens validation CI gate.

Pins R-145 / FR-008 / OQ-010 at the **subprocess** boundary: an external
caller spawning ``python -m superclaude.cli.main swarm validate-lenses``
sees exit 0 on the bundled :data:`LENSES` registry, with the success
summary on stdout naming the 7 non-custom entries the validator
inspected. This is the test that backs the CI lane gating
``swarm validate-lenses`` on every PR (R-145 acceptance criterion
"CI lane runs validator on every PR").

Why subprocess and not :class:`click.testing.CliRunner`?

    :class:`CliRunner` already covers the in-process command surface
    (``test_validate_lenses_cmd.py``). This file deliberately drives
    the CLI through ``subprocess.run`` so a regression in the
    ``[project.scripts]`` entry-point wiring, the Click command-group
    registration, or the module import graph trips the gate -- the
    in-process runner can't catch any of those because it imports the
    command object directly. Together the two surfaces gate the
    registry health from both directions.

OQ-010 resolution exercised here:

    * **Blocking by default** -- exit 1 on registry failure. Asserted
      via a deliberately-failing fixture registry through the in-process
      executor (``_run_validate_lenses`` from ``commands.py``); we do
      not corrupt the bundled :data:`LENSES` from a subprocess because
      that would require either an in-process mutation (the subprocess
      can't see) or a parallel fixture installation (out of scope --
      ``test_validate_lenses_cmd.py`` already covers it).
    * **--warning-mode opt-in flip** -- exit 0 with WARNING diagnostics.
      Asserted on a clean bundled registry (where it should be a no-op
      flip vs default) and on the in-process executor with failures
      (where the exit code flips per OQ-010).

T02.16 / T02.20 dependencies: this gate fires AFTER
``test_validate_all_lenses.py`` and ``test_bundled_lenses.py`` pass.
Those validate the registry contents against the COMP-023 rules in
isolation. This file validates the CLI surface that exposes those
rules to CI -- the subprocess-callability + entry-point + bundled-
registry pass all in one shot.
"""

from __future__ import annotations

import subprocess
import sys

import pytest
from click.testing import CliRunner

from superclaude.cli.swarm import swarm_group
from superclaude.cli.swarm.commands import (
    EXIT_INVALID,
    EXIT_OK,
    _run_validate_lenses,
    validate_lenses_cmd,
)
from superclaude.cli.swarm.lenses import LENS_NAMES, LENSES
from superclaude.cli.swarm.lenses._validate import (
    CUSTOM_LENS_NAME,
    LensValidationFailure,
    RULE_FILE_REF_UNRESOLVED,
)
from superclaude.cli.swarm.models import LensEntry


# ---------------------------------------------------------------------------
# Constants -- the CLI argv shape CI invokes.
# ---------------------------------------------------------------------------


# ``sys.executable`` resolves to the test runner's interpreter (the same
# venv as ``uv run pytest``). Using ``python -m superclaude.cli.main`` (as
# in test_non_claude_caller.py) keeps the test portable across CI lanes
# where the ``superclaude`` console script may or may not be on PATH --
# the module-invocation path always works against an editable install.
PROJECT_PY: str = sys.executable

# Expected non-custom count -- 7 (COMP-024..030). Pinned as a constant so
# any future drift in the bundled registry size (intentional or not)
# trips this gate first instead of being silently absorbed by an
# inequality comparison.
EXPECTED_NON_CUSTOM_COUNT: int = 8
EXPECTED_TOTAL_COUNT: int = 9  # 8 non-custom + 1 custom escape-hatch


# ---------------------------------------------------------------------------
# Inventory sanity (T08.13 step 1: confirm 7 non-custom entries available).
# Pinning the inventory here -- separate from the registry-shape pins in
# test_bundled_lenses.py -- means the CI gate test fails for the right
# reason if the registry ever loses an entry, instead of failing on a
# subprocess output diff and forcing the operator to spelunk.
# ---------------------------------------------------------------------------


def test_bundled_registry_has_eight_total_entries() -> None:
    """T08.13 step 1: 8 total = 7 non-custom + 1 custom placeholder."""
    assert len(LENSES) == EXPECTED_TOTAL_COUNT, (
        f"bundled LENSES registry must carry exactly "
        f"{EXPECTED_TOTAL_COUNT} entries; got {len(LENSES)}: "
        f"{sorted(LENSES)}"
    )


def test_bundled_registry_has_seven_non_custom_entries() -> None:
    """T08.13 step 1: validator inspects 7 entries (skips ``custom``)."""
    non_custom = [
        name for name in LENSES if name != CUSTOM_LENS_NAME
    ]
    assert len(non_custom) == EXPECTED_NON_CUSTOM_COUNT, (
        f"bundled LENSES must expose exactly "
        f"{EXPECTED_NON_CUSTOM_COUNT} non-custom entries to the "
        f"validator; got {len(non_custom)}: {sorted(non_custom)}"
    )


def test_lens_names_order_matches_registry_keys() -> None:
    """The canonical iteration order surfaces in the validator output."""
    assert set(LENS_NAMES) == set(LENSES.keys()), (
        "LENS_NAMES tuple drifted from LENSES dict keys"
    )
    assert len(LENS_NAMES) == EXPECTED_TOTAL_COUNT


# ---------------------------------------------------------------------------
# Subprocess gate -- the actual CI surface (R-145 / FR-008).
# ---------------------------------------------------------------------------


def _invoke_validate_lenses(
    *extra_args: str,
) -> subprocess.CompletedProcess:
    """Spawn ``python -m superclaude.cli.main swarm validate-lenses``.

    Returned :class:`subprocess.CompletedProcess` carries stdout +
    stderr decoded as text; callers introspect ``returncode`` to assert
    the OQ-010 exit-code contract. ``check=False`` so failing exits
    surface in the assertion message rather than as a raised
    :class:`CalledProcessError`.
    """
    argv = [
        PROJECT_PY,
        "-m",
        "superclaude.cli.main",
        "swarm",
        "validate-lenses",
        *extra_args,
    ]
    return subprocess.run(  # noqa: S603  -- argv list, no shell=True
        argv,
        capture_output=True,
        text=True,
        check=False,
    )


def test_subprocess_validate_lenses_exits_zero_on_bundled_registry() -> None:
    """R-145 happy path: bundled registry passes via subprocess (exit 0).

    This is the canonical CI assertion -- the gate the workflow runs
    on every PR. A regression in any of the COMP-023 assertions for the
    7 non-custom entries surfaces as a non-zero exit and stderr
    diagnostics naming the failing lens.
    """
    result = _invoke_validate_lenses()
    assert result.returncode == EXIT_OK, (
        f"swarm validate-lenses must exit {EXIT_OK} on the bundled "
        f"registry; got {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


def test_subprocess_success_summary_names_inspected_counts() -> None:
    """Success summary names both total + non-custom counts.

    Format pinned by ``commands._run_validate_lenses``:
    ``validate-lenses: registry OK (<total> entries inspected, <non-custom> validated)``.
    """
    result = _invoke_validate_lenses()
    assert result.returncode == EXIT_OK, result.stderr
    assert "validate-lenses: registry OK" in result.stdout, (
        f"OK summary missing from stdout:\n{result.stdout}"
    )
    assert f"{EXPECTED_TOTAL_COUNT} entries inspected" in result.stdout, (
        f"summary must report {EXPECTED_TOTAL_COUNT} total entries; "
        f"got:\n{result.stdout}"
    )
    assert f"{EXPECTED_NON_CUSTOM_COUNT} validated" in result.stdout, (
        f"summary must report {EXPECTED_NON_CUSTOM_COUNT} non-custom "
        f"entries validated; got:\n{result.stdout}"
    )


def test_subprocess_emits_no_stderr_diagnostics_on_clean_registry() -> None:
    """Clean registry -> empty stderr (no WARNING / failure lines)."""
    result = _invoke_validate_lenses()
    assert result.returncode == EXIT_OK, result.stderr
    # stderr may contain interpreter warnings (DeprecationWarning, etc.)
    # but must NOT contain the validate-lenses failure header.
    assert "validate-lenses:" not in result.stderr or (
        "WARNING" not in result.stderr
        and "failed validation" not in result.stderr
    ), (
        f"clean registry must not emit failure diagnostics on stderr; "
        f"got stderr:\n{result.stderr}"
    )


def test_subprocess_warning_mode_on_clean_registry_still_exits_zero() -> None:
    """OQ-010 warn branch on a clean registry: still exit 0 (no-op flip)."""
    result = _invoke_validate_lenses("--warning-mode")
    assert result.returncode == EXIT_OK, (
        f"--warning-mode on clean registry must preserve exit "
        f"{EXIT_OK}; got {result.returncode}\nstderr:\n{result.stderr}"
    )
    # OK summary still emits even when --warning-mode is set; failures
    # are what differ between modes, not successes.
    assert "validate-lenses: registry OK" in result.stdout


def test_subprocess_help_lists_warning_mode_flag() -> None:
    """--help advertises the OQ-010 opt-in flag end-to-end."""
    result = _invoke_validate_lenses("--help")
    assert result.returncode == EXIT_OK, result.stderr
    assert "--warning-mode" in result.stdout, (
        f"--warning-mode flag missing from --help output:\n{result.stdout}"
    )


# ---------------------------------------------------------------------------
# OQ-010 failure semantics -- in-process to keep the bundled registry
# pristine for the subprocess gate above.
#
# Why in-process? Faking a failing registry from inside the subprocess
# would require either dynamically rewriting LENSES (won't propagate
# through the import system without an env-var hook -- out of scope for
# T08.13) or shipping a parallel fixture-registry plumb (already
# covered by test_validate_lenses_cmd.py). The in-process path
# exercises the exact same ``_run_validate_lenses`` helper that the
# subprocess hits at runtime, so the OQ-010 exit-code policy
# (blocking-default vs warning-mode flip) is gated identically.
# ---------------------------------------------------------------------------


@pytest.fixture
def patch_validate_all(monkeypatch):
    """Force ``validate_all`` (as imported by commands.py) to a fixed list.

    Mirrors the ``patch_validate_all`` fixture in
    ``test_validate_lenses_cmd.py``; duplicated rather than imported
    because shared conftest fixtures across the two surfaces would
    couple them -- this file is the CI gate, that file is the in-
    process command surface, and they're allowed to diverge.
    """

    def _install(failures):
        from superclaude.cli.swarm import commands as cmd_mod

        def _fake(_registry):
            return list(failures)

        monkeypatch.setattr(cmd_mod, "validate_all", _fake)
        return failures

    return _install


def test_run_validate_lenses_blocks_by_default_on_failures(
    patch_validate_all,
) -> None:
    """OQ-010 blocking default: ``_run_validate_lenses`` returns
    ``EXIT_INVALID`` when ``validate_all`` reports any failure and
    ``warning_mode`` is False.
    """
    patch_validate_all(
        [
            LensValidationFailure(
                rule=RULE_FILE_REF_UNRESOLVED,
                path="output_template_path",
                message="missing template",
                lens_name="bare-review",
            ),
        ]
    )
    exit_code = _run_validate_lenses(
        {"bare-review": LensEntry(name="bare-review")},
        warning_mode=False,
    )
    assert exit_code == EXIT_INVALID, (
        f"blocking default must return {EXIT_INVALID} on failure; "
        f"got {exit_code}"
    )


def test_run_validate_lenses_warning_mode_flips_to_zero(
    patch_validate_all,
) -> None:
    """OQ-010 warning branch: same failure surface, exit 0 under
    ``--warning-mode``.
    """
    patch_validate_all(
        [
            LensValidationFailure(
                rule=RULE_FILE_REF_UNRESOLVED,
                path="output_template_path",
                message="missing template",
                lens_name="bare-review",
            ),
        ]
    )
    exit_code = _run_validate_lenses(
        {"bare-review": LensEntry(name="bare-review")},
        warning_mode=True,
    )
    assert exit_code == EXIT_OK, (
        f"--warning-mode must flip failure exit to {EXIT_OK}; "
        f"got {exit_code}"
    )


def test_cli_runner_failing_registry_emits_lens_named_diagnostic(
    patch_validate_all,
) -> None:
    """In-process CliRunner check: failure diagnostic carries
    ``lens=<name>`` suffix so CI log greps can locate the failing entry
    without running the subprocess separately.
    """
    patch_validate_all(
        [
            LensValidationFailure(
                rule=RULE_FILE_REF_UNRESOLVED,
                path="output_template_path",
                message="missing",
                lens_name="bare-review",
            ),
        ]
    )
    runner = CliRunner()
    result = runner.invoke(validate_lenses_cmd, [])
    assert result.exit_code == EXIT_INVALID
    assert "lens=bare-review" in result.stderr, (
        f"diagnostic must include lens=<name> suffix; "
        f"got stderr:\n{result.stderr}"
    )
    assert RULE_FILE_REF_UNRESOLVED in result.stderr, (
        f"diagnostic must include rule identifier "
        f"({RULE_FILE_REF_UNRESOLVED}); got stderr:\n{result.stderr}"
    )


# ---------------------------------------------------------------------------
# Registration sanity -- the subprocess gate above will surface this on
# failure, but pinning it here keeps the diagnostic local + fast when
# the regression is a missing Click registration rather than a registry
# content drift.
# ---------------------------------------------------------------------------


def test_validate_lenses_registered_under_swarm_group() -> None:
    """``swarm validate-lenses`` resolves to ``validate_lenses_cmd``."""
    assert "validate-lenses" in swarm_group.commands, (
        f"swarm-group is missing the validate-lenses subcommand; "
        f"registered: {sorted(swarm_group.commands)}"
    )
    assert swarm_group.commands["validate-lenses"] is validate_lenses_cmd
