"""T07.09 / FR-006 -- ``superclaude swarm scaffold`` subcommand.

Covers roadmap row R-125 (FR-006). Pins the operator-visible contract
of ``cli/swarm/commands.py::scaffold_cmd``:

1. Registered with ``swarm_group`` under the ``scaffold`` name and
   replaces the T01.08 placeholder.
2. ``--lens NAME`` is required; rendering emits a fully-populated
   DM-001 JobSpec as pretty-printed JSON.
3. The emitted spec passes ``swarm validate`` (schema + cross-field
   rules) for every well-known non-custom lens in ``LENS_NAMES``.
4. Stdout-or-file output supported: bare invocation writes to stdout;
   ``--output PATH`` writes the document atomically and emits a
   confirmation line on stderr.
5. ``--lens custom`` is rejected with EXIT_USAGE (FR-021 escape hatch
   has no registry defaults to expand from).
6. Unknown lens names are rejected with EXIT_USAGE and the registry
   listing.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.swarm import swarm_group
from superclaude.cli.swarm.commands import (
    EXIT_OK,
    EXIT_USAGE,
    scaffold_cmd,
    validate_cmd,
)
from superclaude.cli.swarm.lenses import LENS_NAMES
from superclaude.cli.swarm.schema import (
    CANONICAL_INJECTION_GUARD_SENTENCE,
    CURRENT_SPEC_VERSION,
    validate,
)

_NON_CUSTOM_LENSES: tuple[str, ...] = tuple(n for n in LENS_NAMES if n != "custom")


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


def test_scaffold_cmd_registered_on_swarm_group() -> None:
    """AC: ``scaffold_cmd`` is registered under the ``scaffold`` name."""
    assert "scaffold" in swarm_group.commands, (
        "scaffold subcommand missing from swarm_group; "
        f"registered: {sorted(swarm_group.commands)}"
    )
    assert swarm_group.commands["scaffold"] is scaffold_cmd, (
        "swarm scaffold must resolve to commands.scaffold_cmd, "
        "not the T01.08 placeholder"
    )


def test_scaffold_help_lists_lens_and_output_flags() -> None:
    """AC: ``--lens`` and ``--output`` advertised in --help."""
    runner = CliRunner()
    result = runner.invoke(scaffold_cmd, ["--help"])
    assert result.exit_code == 0, result.output
    assert "--lens" in result.output, result.output
    assert "--output" in result.output, result.output


def test_scaffold_requires_lens_flag() -> None:
    """AC: bare invocation without ``--lens`` is a usage error."""
    runner = CliRunner()
    result = runner.invoke(scaffold_cmd, [])
    # Click emits a usage error (exit 2) when a required option is missing.
    assert result.exit_code == EXIT_USAGE, (
        f"missing --lens should exit {EXIT_USAGE}; got {result.exit_code}\n"
        f"output:\n{result.output}"
    )


# ---------------------------------------------------------------------------
# Stdout mode
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("lens_name", _NON_CUSTOM_LENSES)
def test_scaffold_stdout_emits_valid_json_per_lens(lens_name: str) -> None:
    """AC: ``swarm scaffold --lens NAME`` emits parseable JSON on stdout."""
    runner = CliRunner()
    result = runner.invoke(scaffold_cmd, ["--lens", lens_name])
    assert result.exit_code == EXIT_OK, (
        f"scaffold --lens {lens_name} should exit {EXIT_OK}; "
        f"got {result.exit_code}\nstdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
    spec = json.loads(result.stdout)
    assert spec["spec_version"] == CURRENT_SPEC_VERSION
    assert spec["lens"] == lens_name


@pytest.mark.parametrize("lens_name", _NON_CUSTOM_LENSES)
def test_scaffold_output_validates_via_schema(lens_name: str) -> None:
    """AC: scaffold output passes ``swarm validate`` schema + cross-field.

    Uses the in-process :func:`validate` helper rather than re-invoking
    ``swarm validate`` via the runner so the assertion fails on the
    actual rule name when a future scaffold regression slips a rule.
    """
    runner = CliRunner()
    result = runner.invoke(scaffold_cmd, ["--lens", lens_name])
    assert result.exit_code == EXIT_OK, result.stderr
    spec = json.loads(result.stdout)
    failures = validate(spec)
    assert failures == [], (
        f"scaffold output for lens {lens_name!r} must validate; "
        f"failures: {[(f.rule, f.path, f.message) for f in failures]}"
    )


def test_scaffold_output_validates_via_swarm_validate(tmp_path: Path) -> None:
    """End-to-end: scaffold → file → ``swarm validate`` exits 0.

    Mirrors the operator workflow ``swarm scaffold --lens NAME -o spec.json
    && swarm validate spec.json``. The ``--stdin`` variant in the AC
    validation line is aspirational (``validate_cmd`` is positional-only
    today); this file-based path is the binding contract.
    """
    spec_path = tmp_path / "scaffolded.json"
    runner = CliRunner()

    scaffold_result = runner.invoke(
        scaffold_cmd, ["--lens", "bare-review", "--output", str(spec_path)]
    )
    assert scaffold_result.exit_code == EXIT_OK, (
        f"scaffold --output should exit {EXIT_OK}; "
        f"got {scaffold_result.exit_code}\nstderr:\n{scaffold_result.stderr}"
    )
    assert spec_path.is_file(), f"{spec_path} not written"

    validate_result = runner.invoke(validate_cmd, [str(spec_path)])
    assert validate_result.exit_code == EXIT_OK, (
        f"swarm validate on scaffolded spec should exit {EXIT_OK}; "
        f"got {validate_result.exit_code}\noutput:\n{validate_result.output}"
    )
    assert "OK" in validate_result.stdout


def test_scaffold_stdout_carries_injection_guard_substring() -> None:
    """AC: scaffolded prompt.system contains the §11.5 canonical sentence."""
    runner = CliRunner()
    result = runner.invoke(scaffold_cmd, ["--lens", "bare-review"])
    assert result.exit_code == EXIT_OK, result.stderr
    spec = json.loads(result.stdout)
    assert CANONICAL_INJECTION_GUARD_SENTENCE in spec["prompt"]["system"], (
        "scaffolded prompt.system must carry the §11.5 canonical sentence "
        "so the cross-field rule passes"
    )
    assert (
        spec["target"]["injection_guard"]["required_substring"]
        == CANONICAL_INJECTION_GUARD_SENTENCE
    )


def test_scaffold_stdout_is_pure_json(tmp_path: Path) -> None:
    """AC: stdout payload is the entire JSON document with no banner.

    The scaffold-then-pipe-to-validate pattern hinges on stdout being
    pure JSON; any banner / log line on stdout would break the pipe.
    """
    runner = CliRunner()
    result = runner.invoke(scaffold_cmd, ["--lens", "bare-review"])
    assert result.exit_code == EXIT_OK, result.stderr
    # ``json.loads`` on the full stdout payload must succeed; any
    # leading/trailing banner would raise JSONDecodeError.
    spec = json.loads(result.stdout)
    assert isinstance(spec, dict)
    # And no extraneous trailing data beyond a single trailing newline.
    assert result.stdout.endswith("\n")


# ---------------------------------------------------------------------------
# File-output mode
# ---------------------------------------------------------------------------


def test_scaffold_output_writes_file_atomically(tmp_path: Path) -> None:
    """AC: ``--output PATH`` materialises a valid JobSpec JSON file."""
    spec_path = tmp_path / "starter.json"
    runner = CliRunner()
    result = runner.invoke(
        scaffold_cmd, ["--lens", "bare-review", "--output", str(spec_path)]
    )
    assert result.exit_code == EXIT_OK, result.stderr
    assert spec_path.is_file()
    payload = spec_path.read_text(encoding="utf-8")
    spec = json.loads(payload)
    assert spec["lens"] == "bare-review"
    # Stdout stays clean so callers can pipe ``--output`` invocations.
    assert result.stdout == "", (
        f"--output mode must keep stdout clean; got:\n{result.stdout!r}"
    )
    # Confirmation line lands on stderr.
    assert "wrote starter spec" in result.stderr, result.stderr


def test_scaffold_output_short_flag_alias(tmp_path: Path) -> None:
    """``-o`` is accepted as a short alias for ``--output``."""
    spec_path = tmp_path / "alias.json"
    runner = CliRunner()
    result = runner.invoke(
        scaffold_cmd, ["--lens", "doc-completeness", "-o", str(spec_path)]
    )
    assert result.exit_code == EXIT_OK, result.stderr
    assert spec_path.is_file()


def test_scaffold_output_creates_parent_directory(tmp_path: Path) -> None:
    """``--output`` creates missing parent directories for the spec file."""
    spec_path = tmp_path / "nested" / "deeper" / "spec.json"
    runner = CliRunner()
    result = runner.invoke(
        scaffold_cmd, ["--lens", "edge-case-hunt", "--output", str(spec_path)]
    )
    assert result.exit_code == EXIT_OK, result.stderr
    assert spec_path.is_file()


def test_scaffold_output_overwrites_existing_file(tmp_path: Path) -> None:
    """``--output PATH`` replaces an existing file atomically."""
    spec_path = tmp_path / "existing.json"
    spec_path.write_text("stale contents", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(
        scaffold_cmd, ["--lens", "refactor-find", "--output", str(spec_path)]
    )
    assert result.exit_code == EXIT_OK, result.stderr
    payload = spec_path.read_text(encoding="utf-8")
    assert payload != "stale contents"
    spec = json.loads(payload)
    assert spec["lens"] == "refactor-find"


# ---------------------------------------------------------------------------
# Lens guards
# ---------------------------------------------------------------------------


def test_scaffold_rejects_custom_lens() -> None:
    """AC: ``--lens custom`` exits ``EXIT_USAGE`` with FR-021 diagnostic."""
    runner = CliRunner()
    result = runner.invoke(scaffold_cmd, ["--lens", "custom"])
    assert result.exit_code == EXIT_USAGE, (
        f"--lens custom should exit {EXIT_USAGE}; got {result.exit_code}\n"
        f"stderr:\n{result.stderr}"
    )
    assert "FR-021" in result.stderr or "escape hatch" in result.stderr, (
        f"diagnostic should call out FR-021 escape hatch; got stderr:\n{result.stderr}"
    )


def test_scaffold_rejects_unknown_lens() -> None:
    """AC: unknown lens exits ``EXIT_USAGE`` and lists known lenses."""
    runner = CliRunner()
    result = runner.invoke(scaffold_cmd, ["--lens", "no-such-lens"])
    assert result.exit_code == EXIT_USAGE, (
        f"unknown lens should exit {EXIT_USAGE}; got {result.exit_code}\n"
        f"stderr:\n{result.stderr}"
    )
    assert "unknown lens" in result.stderr
    # Diagnostic must enumerate at least one well-known lens so operators
    # see the menu.
    assert "bare-review" in result.stderr, (
        f"diagnostic should list known lenses; got stderr:\n{result.stderr}"
    )


# ---------------------------------------------------------------------------
# End-to-end via ``superclaude swarm`` group
# ---------------------------------------------------------------------------


def test_scaffold_via_main_swarm_group(tmp_path: Path) -> None:
    """End-to-end: ``superclaude swarm scaffold --lens NAME`` exits 0."""
    from superclaude.cli.main import main

    runner = CliRunner()
    result = runner.invoke(main, ["swarm", "scaffold", "--lens", "bare-review"])
    assert result.exit_code == EXIT_OK, (
        f"superclaude swarm scaffold should exit {EXIT_OK}; "
        f"got {result.exit_code}\nstderr:\n{result.stderr}"
    )
    spec = json.loads(result.stdout)
    assert spec["lens"] == "bare-review"
