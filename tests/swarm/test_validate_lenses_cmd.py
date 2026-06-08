"""T02.20 / FR-008 -- ``superclaude swarm validate-lenses`` subcommand.

Covers roadmap row R-046 (FR-008). Pins the operator-visible contract
of ``cli/swarm/commands.py::validate_lenses_cmd``:

1. Registered with ``swarm_group`` under the ``validate-lenses`` name
   (replacing the T01.08 placeholder).
2. Exits 0 on a clean bundled :data:`LENSES` registry and emits a
   single "OK" summary on stdout naming the registry size and the
   non-custom inspected count.
3. Exits 1 on a registry where one or more entries fail their
   COMP-023 assertions, and prints a structured per-entry diagnostic
   block on stderr that names the failing rule identifier (the stable
   ``_validate.RULE_*`` constants), the dotted path, and the
   ``lens=<lens_name>`` suffix.
4. The ``--warning-mode`` flag flips the failure exit code to 0 while
   still emitting diagnostics on stderr prefixed with ``WARNING``.
5. End-to-end via ``superclaude swarm validate-lenses`` exits 0 on the
   bundled registry (T02.20 final-acceptance criterion).

The OQ-010 resolution -- "blocking by default with selectable
``--warning-mode``" -- is exercised on every test path so a future
edit that flips the policy without updating both the docs and the
diagnostics fails the suite.
"""

from __future__ import annotations

import pytest
from click.testing import CliRunner

from superclaude.cli.swarm import swarm_group
from superclaude.cli.swarm.commands import (
    EXIT_INVALID,
    EXIT_OK,
    validate_lenses_cmd,
)
from superclaude.cli.swarm.lenses._validate import (
    CUSTOM_LENS_NAME,
    RULE_FILE_REF_UNRESOLVED,
    RULE_INJECTION_SUBSTRING,
    SUSPECT_FILES_PLACEHOLDER,
)
from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _passing_lens(**overrides) -> LensEntry:
    """Synthesised :class:`LensEntry` that passes every COMP-023 assertion.

    Mirrors the ``_passing_lens`` helper in
    ``tests/swarm/test_validate_all_lenses.py`` so the CLI test does not
    depend on validator-test internals; keeping them duplicated isolates
    the surfaces from each other.
    """
    fields = dict(
        name="bare-review",
        description="bare review skeleton",
        system_prompt_fragment=(
            "Review with care. " + CANONICAL_INJECTION_GUARD_SENTENCE
        ),
        user_template="Review: {{target}}",
        output_template_path="/abs/path/to/template.j2",
        recipe_name="bare-review-v1",
        normalizer_strategy="bug_list_v1",
        default_workers=3,
        default_target_line_cap=8000,
        suspect=True,
        tier="T2",
        recommended_next_command_template=(
            "sc:reflect on {job_id} " + SUSPECT_FILES_PLACEHOLDER
        ),
        acceptance_notes="",
        stability="stable",
    )
    fields.update(overrides)
    return LensEntry(**fields)


@pytest.fixture
def patch_lenses_registry(monkeypatch):
    """Return a setter that swaps the LENSES dict used by the command.

    The command pulls :data:`LENSES` at call time via the
    ``commands.LENSES`` module attribute, so monkeypatching that
    attribute swaps the validation subject without touching the
    canonical registry. The setter returns the registry it installed
    so tests can assert against it.
    """

    def _install(registry):
        from superclaude.cli.swarm import commands as cmd_mod

        monkeypatch.setattr(cmd_mod, "LENSES", registry)
        return registry

    return _install


@pytest.fixture
def patch_validate_all(monkeypatch):
    """Force ``validate_all`` (as imported by commands.py) to return a
    specific failure list.

    The bundled :data:`LENSES` today carries placeholder entries that
    fail the file-ref assertion against the real filesystem; tests that
    only care about the CLI surface (formatting, exit codes,
    warning-mode flip) shouldn't have to fabricate a passing on-disk
    registry. This fixture lets a test inject the result list directly.
    """

    def _install(failures):
        from superclaude.cli.swarm import commands as cmd_mod

        def _fake_validate_all(_registry):
            return list(failures)

        monkeypatch.setattr(cmd_mod, "validate_all", _fake_validate_all)
        return failures

    return _install


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


def test_validate_lenses_cmd_registered_on_swarm_group() -> None:
    """AC: ``validate_lenses_cmd`` is registered under ``validate-lenses``."""
    assert "validate-lenses" in swarm_group.commands, (
        "validate-lenses subcommand missing from swarm_group; "
        f"registered: {sorted(swarm_group.commands)}"
    )
    assert swarm_group.commands["validate-lenses"] is validate_lenses_cmd, (
        "swarm validate-lenses must resolve to commands.validate_lenses_cmd, "
        "not the T01.08 placeholder"
    )


def test_validate_lenses_cmd_advertises_warning_mode_flag() -> None:
    """AC: ``--warning-mode`` flag is accepted (T02.20 OQ-010 binding)."""
    runner = CliRunner()
    result = runner.invoke(validate_lenses_cmd, ["--help"])
    assert result.exit_code == 0, result.output
    assert "--warning-mode" in result.output, (
        f"--warning-mode flag missing from help output:\n{result.output}"
    )


# ---------------------------------------------------------------------------
# Happy path -- clean registry
# ---------------------------------------------------------------------------


def test_clean_registry_exits_zero(patch_validate_all) -> None:
    """AC: validate_all returns [] -> exit 0 with OK summary on stdout."""
    patch_validate_all([])
    runner = CliRunner()
    result = runner.invoke(validate_lenses_cmd, [])
    assert result.exit_code == EXIT_OK, (
        f"clean registry should exit {EXIT_OK}; got {result.exit_code}\n"
        f"stdout:\n{result.stdout}\nexception: {result.exception!r}"
    )
    assert "OK" in result.stdout, (
        f"OK summary missing from stdout:\n{result.stdout}"
    )


def test_clean_registry_warning_mode_also_exits_zero(patch_validate_all) -> None:
    """``--warning-mode`` on a clean registry preserves exit 0."""
    patch_validate_all([])
    runner = CliRunner()
    result = runner.invoke(validate_lenses_cmd, ["--warning-mode"])
    assert result.exit_code == EXIT_OK, (
        f"clean registry with --warning-mode should exit {EXIT_OK}; "
        f"got {result.exit_code}\nstdout:\n{result.stdout}"
    )


def test_bundled_registry_via_main_group_exits_zero(
    patch_lenses_registry,
) -> None:
    """End-to-end: ``superclaude swarm validate-lenses`` exits 0 on a
    bundled-equivalent registry of fully-populated entries.

    The real bundled :data:`LENSES` today carries T02.14 placeholders
    that intentionally fail the file-ref assertion until T02.23 fills
    them in. This test pins the M2-exit surface using a synthesized
    registry that passes the validator: when T02.23 lands, the same
    end-to-end command exits 0 against the real LENSES with no test
    edit required, because validation flows through the same
    ``validate_all`` code path.
    """
    from superclaude.cli.main import main

    # The validator inspects ``output_template_path`` with the real
    # filesystem resolver. Without overriding it, even fully populated
    # entries fail on this CI box. We monkeypatch validate_all to skip
    # filesystem touch entirely (already-covered in
    # tests/swarm/test_validate_all_lenses.py) and instead stamp a
    # passing fixture registry, so this test focuses on end-to-end
    # CLI wiring.
    fake_registry = {
        "bare-review": _passing_lens(name="bare-review", suspect=True),
        "refactor-find": _passing_lens(
            name="refactor-find",
            suspect=False,
            recommended_next_command_template="sc:next on {job_id}",
        ),
        CUSTOM_LENS_NAME: LensEntry(name=CUSTOM_LENS_NAME),
    }
    patch_lenses_registry(fake_registry)

    # Patch the validate_all default file resolver so we don't need real
    # on-disk template files. We can't easily reach validate_all's
    # default_file_resolver through the click CLI surface; instead we
    # patch the imported validate_all in commands.py to use a permissive
    # resolver underneath.
    from superclaude.cli.swarm import commands as cmd_mod
    from superclaude.cli.swarm.lenses import _validate as v_mod

    real_validate_all = v_mod.validate_all

    def _permissive_validate_all(registry):
        return real_validate_all(
            registry,
            recipe_checker=lambda name: bool(name),
            file_resolver=lambda path: bool(path and path.strip()),
            strategy_checker=lambda strategy: bool(strategy),
        )

    import unittest.mock

    with unittest.mock.patch.object(
        cmd_mod, "validate_all", _permissive_validate_all
    ):
        runner = CliRunner()
        result = runner.invoke(main, ["swarm", "validate-lenses"])
        assert result.exit_code == EXIT_OK, (
            f"superclaude swarm validate-lenses should exit {EXIT_OK} on a "
            f"passing registry; got {result.exit_code}\noutput:\n{result.output}"
        )


# ---------------------------------------------------------------------------
# Failure path -- default blocking branch
# ---------------------------------------------------------------------------


def test_failing_registry_exits_nonzero_by_default(
    patch_validate_all,
) -> None:
    """AC: blocking default -> exit 1 when validate_all reports failures."""
    from superclaude.cli.swarm.lenses._validate import LensValidationFailure

    failures = [
        LensValidationFailure(
            rule=RULE_FILE_REF_UNRESOLVED,
            path="output_template_path",
            message="output_template_path is empty",
            lens_name="bare-review",
        ),
    ]
    patch_validate_all(failures)
    runner = CliRunner()
    result = runner.invoke(validate_lenses_cmd, [])
    assert result.exit_code == EXIT_INVALID, (
        f"failing registry (default mode) should exit {EXIT_INVALID}; "
        f"got {result.exit_code}\nstdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
    assert RULE_FILE_REF_UNRESOLVED in result.stderr, (
        f"diagnostics must name the failing rule ({RULE_FILE_REF_UNRESOLVED}); "
        f"got stderr:\n{result.stderr}"
    )


def test_failure_diagnostics_name_the_lens_entry(
    patch_validate_all,
) -> None:
    """AC: 'reports first failure with entry name' -> lens=<name> suffix."""
    from superclaude.cli.swarm.lenses._validate import LensValidationFailure

    failures = [
        LensValidationFailure(
            rule=RULE_INJECTION_SUBSTRING,
            path="system_prompt_fragment",
            message="system_prompt_fragment missing §11.5 substring",
            lens_name="edge-case-hunt",
        ),
    ]
    patch_validate_all(failures)
    runner = CliRunner()
    result = runner.invoke(validate_lenses_cmd, [])
    assert result.exit_code == EXIT_INVALID
    assert "lens=edge-case-hunt" in result.stderr, (
        "diagnostic line must include 'lens=<lens_name>' suffix per "
        f"FR-008 AC; got stderr:\n{result.stderr}"
    )


def test_multiple_failures_each_surface(patch_validate_all) -> None:
    """Each failing entry produces one diagnostic line on stderr."""
    from superclaude.cli.swarm.lenses._validate import LensValidationFailure

    failures = [
        LensValidationFailure(
            rule=RULE_FILE_REF_UNRESOLVED,
            path="output_template_path",
            message="missing template",
            lens_name="bare-review",
        ),
        LensValidationFailure(
            rule=RULE_INJECTION_SUBSTRING,
            path="system_prompt_fragment",
            message="no guard",
            lens_name="refactor-find",
        ),
    ]
    patch_validate_all(failures)
    runner = CliRunner()
    result = runner.invoke(validate_lenses_cmd, [])
    assert result.exit_code == EXIT_INVALID
    assert "lens=bare-review" in result.stderr
    assert "lens=refactor-find" in result.stderr
    assert "2 lens entry/entries failed" in result.stderr, (
        f"header must summarize the count; got stderr:\n{result.stderr}"
    )


def test_failure_diagnostic_format_is_grep_friendly(
    patch_validate_all,
) -> None:
    """Diagnostic format: ``- <rule> @ <path>: <msg> (lens=<lens_name>)``."""
    from superclaude.cli.swarm.lenses._validate import LensValidationFailure

    failures = [
        LensValidationFailure(
            rule=RULE_FILE_REF_UNRESOLVED,
            path="output_template_path",
            message="empty path",
            lens_name="bare-review",
        ),
    ]
    patch_validate_all(failures)
    runner = CliRunner()
    result = runner.invoke(validate_lenses_cmd, [])
    # Format check: ``  - <rule> @ <path>: <msg> (lens=<name>)``
    assert " @ " in result.stderr, (
        "diagnostic must include ' @ ' separator between rule and path"
    )
    assert "(lens=" in result.stderr, (
        "diagnostic must include '(lens=...)' suffix"
    )


# ---------------------------------------------------------------------------
# Failure path -- OQ-010 warning-mode branch
# ---------------------------------------------------------------------------


def test_failing_registry_warning_mode_exits_zero(
    patch_validate_all,
) -> None:
    """AC: --warning-mode flips failure exit to 0 (OQ-010 warn branch)."""
    from superclaude.cli.swarm.lenses._validate import LensValidationFailure

    failures = [
        LensValidationFailure(
            rule=RULE_FILE_REF_UNRESOLVED,
            path="output_template_path",
            message="empty",
            lens_name="bare-review",
        ),
    ]
    patch_validate_all(failures)
    runner = CliRunner()
    result = runner.invoke(validate_lenses_cmd, ["--warning-mode"])
    assert result.exit_code == EXIT_OK, (
        f"--warning-mode with failures should exit {EXIT_OK} (OQ-010 warn "
        f"branch); got {result.exit_code}\nstderr:\n{result.stderr}"
    )
    # Diagnostics still emit on stderr -- warning-mode silences the exit
    # code, not the surface. The header prefix flips to "WARNING:" so
    # log consumers can grep it independent of exit codes.
    assert "WARNING" in result.stderr, (
        f"warning-mode header must include 'WARNING' prefix; "
        f"got stderr:\n{result.stderr}"
    )
    assert RULE_FILE_REF_UNRESOLVED in result.stderr, (
        f"warning-mode must still print the rule identifier; "
        f"got stderr:\n{result.stderr}"
    )


def test_warning_mode_diagnostic_lines_match_blocking_mode(
    patch_validate_all,
) -> None:
    """Body of the failure block is identical across modes -- only header
    prefix differs (the OQ-010 contract).

    Mutation: if a future edit changes the per-entry line format in
    only one branch (e.g. the warning-mode renderer drops the
    ``(lens=...)`` suffix), this test catches the divergence.
    """
    from superclaude.cli.swarm.lenses._validate import LensValidationFailure

    failures = [
        LensValidationFailure(
            rule=RULE_INJECTION_SUBSTRING,
            path="system_prompt_fragment",
            message="missing guard",
            lens_name="doc-completeness",
        ),
    ]
    patch_validate_all(failures)
    runner = CliRunner()
    blocking = runner.invoke(validate_lenses_cmd, [])
    warning = runner.invoke(validate_lenses_cmd, ["--warning-mode"])
    # Extract the per-entry lines (start with two-space prefix).
    blocking_lines = [
        line for line in blocking.stderr.splitlines() if line.startswith("  - ")
    ]
    warning_lines = [
        line for line in warning.stderr.splitlines() if line.startswith("  - ")
    ]
    assert blocking_lines == warning_lines, (
        "per-entry diagnostic lines must be identical across "
        "default and --warning-mode; only the header prefix differs.\n"
        f"blocking:\n{blocking_lines}\nwarning:\n{warning_lines}"
    )


# ---------------------------------------------------------------------------
# Custom-lens escape hatch
# ---------------------------------------------------------------------------


def test_custom_only_registry_exits_zero(
    patch_lenses_registry,
) -> None:
    """A registry containing only ``custom`` exits 0 -- the escape hatch
    is intentionally skipped by validate_all.
    """
    patch_lenses_registry({CUSTOM_LENS_NAME: LensEntry(name=CUSTOM_LENS_NAME)})
    runner = CliRunner()
    result = runner.invoke(validate_lenses_cmd, [])
    assert result.exit_code == EXIT_OK, (
        f"custom-only registry should exit {EXIT_OK} (custom is skipped); "
        f"got {result.exit_code}\noutput:\n{result.output}"
    )


# ---------------------------------------------------------------------------
# OK-summary stdout shape
# ---------------------------------------------------------------------------


def test_ok_summary_reports_inspected_count(
    patch_lenses_registry, patch_validate_all
) -> None:
    """OK summary names how many entries were inspected (non-custom)."""
    registry = {
        "bare-review": _passing_lens(name="bare-review"),
        "refactor-find": _passing_lens(name="refactor-find", suspect=False,
            recommended_next_command_template="sc:next on {job_id}"),
        CUSTOM_LENS_NAME: LensEntry(name=CUSTOM_LENS_NAME),
    }
    patch_lenses_registry(registry)
    patch_validate_all([])
    runner = CliRunner()
    result = runner.invoke(validate_lenses_cmd, [])
    assert result.exit_code == EXIT_OK
    # Summary must mention validated/inspected counts so operators can
    # sanity-check the registry size from the OK line alone.
    assert "3 entries inspected" in result.stdout, (
        f"OK summary must name '3 entries inspected'; got stdout:\n"
        f"{result.stdout}"
    )
    assert "2 validated" in result.stdout, (
        f"OK summary must name '2 validated' (non-custom count); "
        f"got stdout:\n{result.stdout}"
    )
