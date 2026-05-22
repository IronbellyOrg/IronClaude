"""Tests for ``superclaude.cli.eval.loader.validate_manifest``.

Covers cliEval Phase 1 / Task T01.04 acceptance criteria (Deliverable D-0004,
FR-SCH1):

* Function exists at ``src/superclaude/cli/eval/loader.py`` and is importable
  from the ``superclaude.cli.eval`` package.
* A schema-valid fixture returns a ``list[EvalSpec]`` whose length matches
  the manifest's ``evals[]`` length and whose ids round-trip the input.
* A fixture missing the top-level ``name`` field raises ``SchemaError`` and
  the error message names ``name`` and uses a ``$``-rooted JSON path.
* A fixture with violations nested inside ``evals[0]`` reports the offending
  JSON path (``$.evals[0]``) so reporter output is stable.
* No filesystem writes hit the default scratch root (``/tmp/eval-runs``)
  during a rejection, per FR-SCH1 / NFR-SEC1.
* ``SchemaError`` maps to ``SCHEMA_ERROR_EXIT_CODE`` (= 2) per design-spec §4.
* Missing manifest files and YAML decode errors also surface as
  ``SchemaError`` so CLI callers only need to catch a single typed error.

Cross-links:
* FR-SCH1 (this task, T01.04)
* DM-011 schema (T01.02)
* DM-002 EvalSpec model (T01.03)
* NFR-SEC1 path-traversal prevention test set (T01.08)
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.eval import (
    SCHEMA_ERROR_EXIT_CODE,
    EvalSpec,
    SchemaError,
    validate_manifest,
)

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
DEFAULT_SCRATCH_ROOT = Path("/tmp/eval-runs")


# --- positive path ----------------------------------------------------------


def test_valid_manifest_returns_list_of_evalspec() -> None:
    specs = validate_manifest(FIXTURES_DIR / "valid_suite.yaml")
    assert isinstance(specs, list)
    assert all(isinstance(s, EvalSpec) for s in specs)


def test_valid_manifest_length_matches_evals_block() -> None:
    specs = validate_manifest(FIXTURES_DIR / "valid_suite.yaml")
    # valid_suite.yaml declares exactly two evals (E1, E2).
    assert len(specs) == 2
    assert [s.id for s in specs] == ["E1", "E2"]


def test_valid_manifest_round_trips_evalspec_fields() -> None:
    specs = validate_manifest(FIXTURES_DIR / "valid_suite.yaml")
    e1 = next(s for s in specs if s.id == "E1")
    assert e1.title.startswith("auggie-first")
    assert e1.category == "hook-lifecycle"
    assert e1.requires == ("mcp_server.auggie",)
    assert e1.timeout_sec == 90
    assert e1.parameterize == ()

    e2 = next(s for s in specs if s.id == "E2")
    assert len(e2.parameterize) == 3  # three substitution rows
    assert e2.parameterize[0]["prefix"] == "mcp__auggie__"


def test_validate_manifest_accepts_str_path() -> None:
    # Ergonomic check: ``str`` should normalise the same as ``Path``.
    specs = validate_manifest(str(FIXTURES_DIR / "valid_suite.yaml"))
    assert [s.id for s in specs] == ["E1", "E2"]


# --- negative path: schema violations --------------------------------------


def test_missing_required_field_raises_schema_error_with_field_name() -> None:
    with pytest.raises(SchemaError) as excinfo:
        validate_manifest(FIXTURES_DIR / "missing_name_suite.yaml")

    err = excinfo.value
    rendered = str(err)
    # Acceptance: error message names the offending JSON path.
    assert "name" in rendered
    # Top-level missing-required errors live at the manifest root.
    assert any(path == "$" and "name" in msg for path, msg in err.violations)


def test_nested_violation_reports_json_path_with_evals_index() -> None:
    with pytest.raises(SchemaError) as excinfo:
        validate_manifest(FIXTURES_DIR / "invalid_eval_entry_suite.yaml")

    paths = {path for path, _ in excinfo.value.violations}
    # The entry at evals[0] is missing `title` and has an unsafe id; both
    # violations should report a path rooted under ``$.evals[0]`` so the
    # reporter can render them deterministically.
    assert any(p.startswith("$.evals[0]") for p in paths), paths


def test_unknown_top_level_key_is_reported() -> None:
    with pytest.raises(SchemaError) as excinfo:
        validate_manifest(FIXTURES_DIR / "unknown_top_level_suite.yaml")
    assert any("mystery_field" in msg for _, msg in excinfo.value.violations)


# --- negative path: read / decode errors -----------------------------------


def test_missing_manifest_file_raises_schema_error(tmp_path: Path) -> None:
    missing = tmp_path / "no-such-suite.yaml"
    with pytest.raises(SchemaError) as excinfo:
        validate_manifest(missing)
    assert excinfo.value.manifest_path == missing


def test_yaml_decode_error_is_schema_error(tmp_path: Path) -> None:
    bad = tmp_path / "broken.yaml"
    bad.write_text("evals: [unterminated\n", encoding="utf-8")
    with pytest.raises(SchemaError) as excinfo:
        validate_manifest(bad)
    assert any("YAML decode failed" in msg for _, msg in excinfo.value.violations)


def test_non_mapping_manifest_is_schema_error(tmp_path: Path) -> None:
    scalar = tmp_path / "scalar.yaml"
    scalar.write_text("just-a-string\n", encoding="utf-8")
    with pytest.raises(SchemaError) as excinfo:
        validate_manifest(scalar)
    assert any("mapping" in msg for _, msg in excinfo.value.violations)


# --- FR-SCH1 invariant: no FS writes before validation ---------------------


def _scratch_snapshot() -> set[str]:
    """Snapshot the default scratch root for write-leak detection.

    The directory is not guaranteed to exist on a fresh dev machine; an
    empty set is treated as a valid baseline. Only the *delta* matters
    for the FR-SCH1 invariant.
    """

    if not DEFAULT_SCRATCH_ROOT.exists():
        return set()
    return {str(p) for p in DEFAULT_SCRATCH_ROOT.rglob("*")}


def test_rejection_does_not_write_to_default_scratch_root() -> None:
    before = _scratch_snapshot()
    with pytest.raises(SchemaError):
        validate_manifest(FIXTURES_DIR / "missing_name_suite.yaml")
    after = _scratch_snapshot()
    assert after == before, (
        "validate_manifest must not touch /tmp/eval-runs before validation "
        "succeeds (FR-SCH1 / NFR-SEC1)"
    )


# --- exit-code mapping ------------------------------------------------------


def test_schema_error_exit_code_is_two() -> None:
    # Single source of truth for the CLI mapping; design-spec §4 exit-code
    # table reserves ``2`` for "Harness error (manifest invalid, ...)".
    assert SCHEMA_ERROR_EXIT_CODE == 2


def test_schema_error_str_includes_manifest_path() -> None:
    manifest = FIXTURES_DIR / "missing_name_suite.yaml"
    with pytest.raises(SchemaError) as excinfo:
        validate_manifest(manifest)
    assert str(manifest) in str(excinfo.value)


def test_violations_ordering_is_deterministic() -> None:
    # Two calls on the same fixture must yield identical violation tuples.
    with pytest.raises(SchemaError) as first:
        validate_manifest(FIXTURES_DIR / "invalid_eval_entry_suite.yaml")
    first_violations = first.value.violations
    with pytest.raises(SchemaError) as second:
        validate_manifest(FIXTURES_DIR / "invalid_eval_entry_suite.yaml")
    assert first_violations == second.value.violations
