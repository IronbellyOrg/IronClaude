"""Tests for ``superclaude eval describe`` (FR-CLI3 / Task T01.22 / D-0019).

Covers the four acceptance criteria from the phase tasklist:

1. ``superclaude eval describe --suite <name>`` prints the validated
   post-parameterize manifest content for the suite.
2. ``--eval <id>`` filters output to a single eval; missing id exits 2
   with ``EvalNotFound`` on stderr.
3. Validation runs BEFORE any print operation; invalid manifests exit 2
   (schema / eval-id regex / capability resolution rejections route
   through the same SuiteLoader gate chain as ``eval run``).
4. ``artifacts/D-0019/spec.md`` records flag semantics.

The default suites directory ships only ``suite.schema.json`` at M1, so
populated cases route through ``--suites-dir`` pointing at a tmp dir
seeded from ``tests/cli/eval/fixtures/``. Cross-references:
FR-CLI3 (R-019), FR-SCH1 (R-004), FR-SCH2 (R-005), COMP-002 (R-006).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import yaml
from click.testing import CliRunner

from superclaude.cli.eval.commands import (
    EVAL_NOT_FOUND_EXIT_CODE,
    SUITE_NOT_FOUND_EXIT_CODE,
    EvalNotFound,
    SuiteNotFound,
    _evalspec_to_dict,
    _parsed_suite_to_dict,
    describe_suite,
    eval_group,
    render_describe_json,
    render_describe_yaml,
    resolve_suite_manifest,
)
from superclaude.cli.eval.loader import (
    SUITE_LOADER_ERROR_EXIT_CODE,
    ParsedSuite,
    SuiteLoader,
)

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _seed_reference_suite(tmp_path: Path, filename: str = "reference.yaml") -> Path:
    """Copy the reference fixture into ``tmp_path`` under ``filename``.

    Naming the copy ``reference.yaml`` exercises the stem-lookup
    resolution path (``<suites_dir>/<token>.yaml``); the fixture's
    ``name:`` field is already ``reference`` so name-based lookup is
    also exercised by the same file.
    """

    dst = tmp_path / filename
    shutil.copy(FIXTURES_DIR / "valid_suite.yaml", dst)
    return dst


def _seed_static_suite(tmp_path: Path, filename: str = "no_parameterize.yaml") -> Path:
    dst = tmp_path / filename
    shutil.copy(FIXTURES_DIR / "no_parameterize_suite.yaml", dst)
    return dst


# ---------------------------------------------------------------------------
# Pure projection helpers
# ---------------------------------------------------------------------------


def test_evalspec_to_dict_omits_default_optional_fields(tmp_path: Path) -> None:
    manifest_path = _seed_static_suite(tmp_path)
    parsed: ParsedSuite = SuiteLoader().load(manifest_path)
    # D15 declares no requires, no inputs beyond expects; verify defaults skipped.
    d15 = next(spec for spec in parsed.evals if spec.id == "D15")
    payload = _evalspec_to_dict(d15)
    assert payload["id"] == "D15"
    assert payload["title"] == "static-id eval two"
    assert "category" not in payload  # category defaulted to ""
    assert "requires" not in payload  # empty tuple
    assert "timeout_sec" not in payload  # None
    assert "isolation" not in payload
    assert "inputs" not in payload
    # ``expects`` IS present because the fixture declares one expects row.
    assert payload["expects"] == [{"type": "exit_code", "value": 0}]


def test_evalspec_to_dict_preserves_post_expansion_id(tmp_path: Path) -> None:
    manifest_path = _seed_reference_suite(tmp_path)
    parsed: ParsedSuite = SuiteLoader().load(manifest_path)
    expanded_ids = {spec.id for spec in parsed.evals}
    # FR-SCH2 expansion: E2 → E2.1, E2.2, E2.3.
    assert {"E1", "E2.1", "E2.2", "E2.3"} == expanded_ids
    e2_first = next(spec for spec in parsed.evals if spec.id == "E2.1")
    payload = _evalspec_to_dict(e2_first)
    assert payload["id"] == "E2.1"
    # Parameterize rows are preserved on the expanded entry (the loader
    # round-trips them; describe is not responsible for substitution).
    assert "parameterize" in payload
    assert len(payload["parameterize"]) == 3


def test_parsed_suite_to_dict_envelope_shape(tmp_path: Path) -> None:
    manifest_path = _seed_reference_suite(tmp_path)
    parsed = SuiteLoader().load(manifest_path)
    payload = _parsed_suite_to_dict(parsed)
    assert payload["name"] == "reference"
    assert payload["version"] == "1.0"
    assert payload["description"].startswith("Reference v1 manifest")
    assert payload["defaults"]["per_eval_timeout_sec"] == 120
    assert len(payload["required_binaries"]) == 4
    assert len(payload["optional_capabilities"]) == 3
    # evals is the post-expansion list (1 static + 3 parameterized rows).
    assert len(payload["evals"]) == 4


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------


def test_render_describe_yaml_round_trips(tmp_path: Path) -> None:
    manifest_path = _seed_reference_suite(tmp_path)
    parsed = SuiteLoader().load(manifest_path)
    payload = _parsed_suite_to_dict(parsed)
    text = render_describe_yaml(payload)
    decoded = yaml.safe_load(text)
    assert decoded == payload


def test_render_describe_yaml_preserves_field_order(tmp_path: Path) -> None:
    manifest_path = _seed_reference_suite(tmp_path)
    parsed = SuiteLoader().load(manifest_path)
    payload = _parsed_suite_to_dict(parsed)
    text = render_describe_yaml(payload)
    # Suite-envelope field order matches the schema declaration so the
    # YAML reads like the source manifest. Assert by string offset.
    name_idx = text.index("name:")
    version_idx = text.index("version:")
    description_idx = text.index("description:")
    evals_idx = text.index("evals:")
    assert name_idx < version_idx < description_idx < evals_idx


def test_render_describe_json_is_deterministic(tmp_path: Path) -> None:
    manifest_path = _seed_reference_suite(tmp_path)
    parsed = SuiteLoader().load(manifest_path)
    payload = _parsed_suite_to_dict(parsed)
    assert render_describe_json(payload) == render_describe_json(payload)


# ---------------------------------------------------------------------------
# Suite resolution
# ---------------------------------------------------------------------------


def test_resolve_suite_manifest_accepts_direct_path(tmp_path: Path) -> None:
    manifest_path = _seed_reference_suite(tmp_path, filename="custom.yaml")
    resolved = resolve_suite_manifest(str(manifest_path), tmp_path)
    assert resolved == manifest_path


def test_resolve_suite_manifest_finds_by_filename_stem(tmp_path: Path) -> None:
    manifest_path = _seed_reference_suite(tmp_path, filename="my-suite.yaml")
    resolved = resolve_suite_manifest("my-suite", tmp_path)
    assert resolved == manifest_path


def test_resolve_suite_manifest_finds_by_name_field(tmp_path: Path) -> None:
    # Filename stem is "valid_suite" but manifest name is "reference".
    manifest_path = _seed_reference_suite(tmp_path, filename="valid_suite.yaml")
    resolved = resolve_suite_manifest("reference", tmp_path)
    assert resolved == manifest_path


def test_resolve_suite_manifest_skips_broken_neighbours(tmp_path: Path) -> None:
    """A schema-broken neighbour MUST NOT prevent locating the target."""
    shutil.copy(
        FIXTURES_DIR / "missing_name_suite.yaml",
        tmp_path / "broken.yaml",
    )
    manifest_path = _seed_reference_suite(tmp_path, filename="valid.yaml")
    resolved = resolve_suite_manifest("reference", tmp_path)
    assert resolved == manifest_path


def test_resolve_suite_manifest_raises_when_missing(tmp_path: Path) -> None:
    _seed_reference_suite(tmp_path)
    try:
        resolve_suite_manifest("does-not-exist", tmp_path)
    except SuiteNotFound as exc:
        assert exc.suite == "does-not-exist"
        assert exc.suites_dir == tmp_path
    else:  # pragma: no cover - assertion path
        raise AssertionError("expected SuiteNotFound")


# ---------------------------------------------------------------------------
# describe_suite (the function exposed to tests)
# ---------------------------------------------------------------------------


def test_describe_suite_returns_envelope_without_eval_filter(tmp_path: Path) -> None:
    _seed_reference_suite(tmp_path)
    payload = describe_suite("reference", suites_dir=tmp_path)
    assert payload["name"] == "reference"
    assert len(payload["evals"]) == 4  # post-expansion


def test_describe_suite_filters_to_single_eval(tmp_path: Path) -> None:
    _seed_reference_suite(tmp_path)
    payload = describe_suite("reference", suites_dir=tmp_path, eval_id="E1")
    assert payload["id"] == "E1"
    assert "evals" not in payload  # single-eval projection, not envelope
    # Verify post-expansion id filter too.
    payload2 = describe_suite("reference", suites_dir=tmp_path, eval_id="E2.2")
    assert payload2["id"] == "E2.2"


def test_describe_suite_raises_eval_not_found(tmp_path: Path) -> None:
    _seed_reference_suite(tmp_path)
    try:
        describe_suite("reference", suites_dir=tmp_path, eval_id="ZZ99")
    except EvalNotFound as exc:
        assert exc.eval_id == "ZZ99"
        assert exc.suite_name == "reference"
        assert "E1" in exc.known_ids
        assert "E2.1" in exc.known_ids
    else:  # pragma: no cover - assertion path
        raise AssertionError("expected EvalNotFound")


# ---------------------------------------------------------------------------
# CLI integration
# ---------------------------------------------------------------------------


def test_cli_describe_prints_yaml_envelope(tmp_path: Path) -> None:
    _seed_reference_suite(tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        ["describe", "--suite", "reference", "--suites-dir", str(tmp_path)],
    )
    assert result.exit_code == 0, result.output
    decoded = yaml.safe_load(result.output)
    assert decoded["name"] == "reference"
    assert decoded["version"] == "1.0"
    # Post-expansion count is the operator-facing contract.
    assert len(decoded["evals"]) == 4
    assert {entry["id"] for entry in decoded["evals"]} == {
        "E1",
        "E2.1",
        "E2.2",
        "E2.3",
    }


def test_cli_describe_json_emits_valid_json(tmp_path: Path) -> None:
    _seed_reference_suite(tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "describe",
            "--suite",
            "reference",
            "--json",
            "--suites-dir",
            str(tmp_path),
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["name"] == "reference"
    assert len(payload["evals"]) == 4


def test_cli_describe_filters_to_single_eval_yaml(tmp_path: Path) -> None:
    _seed_reference_suite(tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "describe",
            "--suite",
            "reference",
            "--eval",
            "E1",
            "--suites-dir",
            str(tmp_path),
        ],
    )
    assert result.exit_code == 0, result.output
    decoded = yaml.safe_load(result.output)
    assert decoded["id"] == "E1"
    # Single-eval projection does NOT carry the suite envelope.
    assert "evals" not in decoded


def test_cli_describe_filters_to_post_expansion_id(tmp_path: Path) -> None:
    """``--eval E2.1`` MUST resolve against the expanded id list."""
    _seed_reference_suite(tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "describe",
            "--suite",
            "reference",
            "--eval",
            "E2.2",
            "--json",
            "--suites-dir",
            str(tmp_path),
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["id"] == "E2.2"


def test_cli_describe_exit2_on_missing_eval(tmp_path: Path) -> None:
    _seed_reference_suite(tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "describe",
            "--suite",
            "reference",
            "--eval",
            "ZZ99",
            "--suites-dir",
            str(tmp_path),
        ],
    )
    assert result.exit_code == EVAL_NOT_FOUND_EXIT_CODE
    assert "EvalNotFound" in result.stderr


def test_cli_describe_exit2_on_missing_suite(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "describe",
            "--suite",
            "ghost",
            "--suites-dir",
            str(tmp_path),
        ],
    )
    assert result.exit_code == SUITE_NOT_FOUND_EXIT_CODE
    assert "SuiteNotFound" in result.stderr


def test_cli_describe_exit2_on_schema_violation(tmp_path: Path) -> None:
    """FR-SCH1: schema rejection MUST surface as exit 2 with class name."""
    shutil.copy(
        FIXTURES_DIR / "missing_name_suite.yaml",
        tmp_path / "broken.yaml",
    )
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "describe",
            "--suite",
            str(tmp_path / "broken.yaml"),
            "--suites-dir",
            str(tmp_path),
        ],
    )
    assert result.exit_code == SUITE_LOADER_ERROR_EXIT_CODE
    assert "SchemaError" in result.stderr


def test_cli_describe_exit2_on_invalid_eval_id(tmp_path: Path) -> None:
    """FR-SCH2: traversal-pattern id MUST surface InvalidEvalId at exit 2."""
    shutil.copy(
        FIXTURES_DIR / "invalid_eval_entry_suite.yaml",
        tmp_path / "broken.yaml",
    )
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "describe",
            "--suite",
            str(tmp_path / "broken.yaml"),
            "--suites-dir",
            str(tmp_path),
        ],
    )
    assert result.exit_code == SUITE_LOADER_ERROR_EXIT_CODE
    # Either InvalidEvalId or SchemaError is acceptable — both routes
    # block the print and exit 2 per FR-SCH1+FR-SCH2.
    assert ("InvalidEvalId" in result.stderr) or ("SchemaError" in result.stderr)


def test_cli_describe_validation_runs_before_any_stdout(tmp_path: Path) -> None:
    """T01.22 AC: validation runs before any print operation.

    The pre-flight ordering claim is verified by snapshotting stdout on a
    rejection path — it MUST be empty because the loader raises before
    any ``click.echo`` of the payload is reached.
    """
    shutil.copy(
        FIXTURES_DIR / "missing_name_suite.yaml",
        tmp_path / "broken.yaml",
    )
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "describe",
            "--suite",
            str(tmp_path / "broken.yaml"),
            "--suites-dir",
            str(tmp_path),
        ],
    )
    assert result.exit_code == SUITE_LOADER_ERROR_EXIT_CODE
    # stdout is empty — only stderr carries the error class line.
    assert result.stdout == ""


def test_cli_describe_yaml_is_deterministic(tmp_path: Path) -> None:
    _seed_reference_suite(tmp_path)
    runner = CliRunner()
    first = runner.invoke(
        eval_group,
        ["describe", "--suite", "reference", "--suites-dir", str(tmp_path)],
    ).output
    second = runner.invoke(
        eval_group,
        ["describe", "--suite", "reference", "--suites-dir", str(tmp_path)],
    ).output
    assert first == second


def test_cli_describe_requires_suite_option() -> None:
    runner = CliRunner()
    result = runner.invoke(eval_group, ["describe"])
    # Click emits its own usage error → exit code 2 (Click default).
    assert result.exit_code != 0
    assert "--suite" in result.output or "--suite" in result.stderr
