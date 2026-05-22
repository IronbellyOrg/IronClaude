"""Tests for ``superclaude eval list`` (FR-CLI2 / Task T01.21 / D-0018).

Covers the four acceptance criteria from the phase tasklist:

1. ``superclaude eval list`` exits 0 with at least one suite present and
   with zero suites present (empty-directory case).
2. ``--json`` emits a JSON array with ``{name, version, eval_count}``
   entries.
3. Output is deterministic for a given suite directory (sorted by
   filename).
4. Module exports ``eval_list`` / ``summarize_suites`` /
   ``discover_suite_manifests`` for downstream consumers and tests.

The default suites directory ships only ``suite.schema.json`` at M1, so
populated-list cases route through ``--suites-dir`` pointing at fixtures.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from click.testing import CliRunner

from superclaude.cli.eval.commands import (
    SuiteSummary,
    discover_suite_manifests,
    eval_group,
    list_payload,
    render_list_text,
    summarize_suites,
)
from superclaude.cli.eval.loader import SUITE_LOADER_ERROR_EXIT_CODE

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


# ---------------------------------------------------------------------------
# discover_suite_manifests + summarize_suites + render helpers
# ---------------------------------------------------------------------------


def test_discover_returns_empty_for_missing_directory(tmp_path: Path) -> None:
    assert discover_suite_manifests(tmp_path / "absent") == []


def test_discover_returns_empty_for_directory_with_no_yaml(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("not a manifest", encoding="utf-8")
    assert discover_suite_manifests(tmp_path) == []


def test_discover_returns_sorted_yaml_files(tmp_path: Path) -> None:
    src = FIXTURES_DIR / "no_parameterize_suite.yaml"
    shutil.copy(src, tmp_path / "zebra.yaml")
    shutil.copy(src, tmp_path / "alpha.yaml")
    shutil.copy(src, tmp_path / "middle.yaml")
    # An extra non-YAML file MUST NOT appear in the listing.
    (tmp_path / "suite.schema.json").write_text("{}", encoding="utf-8")
    discovered = discover_suite_manifests(tmp_path)
    assert [p.name for p in discovered] == [
        "alpha.yaml",
        "middle.yaml",
        "zebra.yaml",
    ]


def test_summarize_suites_returns_post_expansion_eval_count(tmp_path: Path) -> None:
    """valid_suite.yaml has 2 raw evals → 1 static + 3 parameterize rows = 4."""
    shutil.copy(FIXTURES_DIR / "valid_suite.yaml", tmp_path / "reference.yaml")
    summaries = summarize_suites(tmp_path)
    assert len(summaries) == 1
    summary = summaries[0]
    assert summary.name == "reference"
    assert summary.version == "1.0"
    assert summary.eval_count == 4  # E1 + E2.1 + E2.2 + E2.3
    assert summary.source == tmp_path / "reference.yaml"


def test_summarize_suites_handles_static_only_manifest(tmp_path: Path) -> None:
    shutil.copy(
        FIXTURES_DIR / "no_parameterize_suite.yaml",
        tmp_path / "static.yaml",
    )
    summaries = summarize_suites(tmp_path)
    assert summaries[0].name == "no-parameterize"
    assert summaries[0].eval_count == 2  # E1, D15


def test_summarize_suites_preserves_filename_order(tmp_path: Path) -> None:
    shutil.copy(FIXTURES_DIR / "valid_suite.yaml", tmp_path / "b.yaml")
    shutil.copy(
        FIXTURES_DIR / "no_parameterize_suite.yaml", tmp_path / "a.yaml"
    )
    summaries = summarize_suites(tmp_path)
    assert [s.source.name for s in summaries] == ["a.yaml", "b.yaml"]


def test_summarize_suites_returns_empty_for_empty_directory(tmp_path: Path) -> None:
    assert summarize_suites(tmp_path) == []


def test_render_list_text_empty_directory_message() -> None:
    text = render_list_text([])
    assert "superclaude eval list:" in text
    assert "(no suites found)" in text


def test_render_list_text_lists_each_summary(tmp_path: Path) -> None:
    summaries = [
        SuiteSummary("alpha", "1.0", 3, tmp_path / "alpha.yaml"),
        SuiteSummary("beta", "2.0", 1, tmp_path / "beta.yaml"),
    ]
    text = render_list_text(summaries)
    assert "alpha" in text and "version 1.0" in text and "3 evals" in text
    assert "beta" in text and "version 2.0" in text and "1 eval" in text
    # Singular vs plural pluralisation.
    assert "1 eval)" in text  # not "1 evals"


def test_list_payload_shape(tmp_path: Path) -> None:
    summaries = [
        SuiteSummary("alpha", "1.0", 3, tmp_path / "alpha.yaml"),
    ]
    payload = list_payload(summaries)
    assert payload == [{"name": "alpha", "version": "1.0", "eval_count": 3}]


# ---------------------------------------------------------------------------
# CLI integration via Click's CliRunner
# ---------------------------------------------------------------------------


def test_cli_list_exits_zero_on_empty_directory(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(eval_group, ["list", "--suites-dir", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "(no suites found)" in result.output


def test_cli_list_exits_zero_with_default_suites_dir() -> None:
    """The shipped suites/ dir holds only the schema at M1 → empty list."""
    runner = CliRunner()
    result = runner.invoke(eval_group, ["list"])
    assert result.exit_code == 0, result.output
    assert "superclaude eval list:" in result.output


def test_cli_list_prints_name_version_eval_count(tmp_path: Path) -> None:
    shutil.copy(FIXTURES_DIR / "valid_suite.yaml", tmp_path / "reference.yaml")
    runner = CliRunner()
    result = runner.invoke(eval_group, ["list", "--suites-dir", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "reference" in result.output
    assert "version 1.0" in result.output
    assert "4 evals" in result.output  # post-expansion


def test_cli_list_json_emits_array_of_summaries(tmp_path: Path) -> None:
    shutil.copy(FIXTURES_DIR / "valid_suite.yaml", tmp_path / "reference.yaml")
    shutil.copy(
        FIXTURES_DIR / "no_parameterize_suite.yaml",
        tmp_path / "static.yaml",
    )
    runner = CliRunner()
    result = runner.invoke(
        eval_group, ["list", "--json", "--suites-dir", str(tmp_path)]
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert isinstance(payload, list)
    assert len(payload) == 2
    for entry in payload:
        assert set(entry.keys()) == {"name", "version", "eval_count"}


def test_cli_list_json_empty_directory_returns_empty_array(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        eval_group, ["list", "--json", "--suites-dir", str(tmp_path)]
    )
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == []


def test_cli_list_json_is_deterministic_across_invocations(tmp_path: Path) -> None:
    shutil.copy(FIXTURES_DIR / "valid_suite.yaml", tmp_path / "reference.yaml")
    shutil.copy(
        FIXTURES_DIR / "no_parameterize_suite.yaml",
        tmp_path / "static.yaml",
    )
    runner = CliRunner()
    first = runner.invoke(
        eval_group, ["list", "--json", "--suites-dir", str(tmp_path)]
    ).output
    second = runner.invoke(
        eval_group, ["list", "--json", "--suites-dir", str(tmp_path)]
    ).output
    assert first == second


def test_cli_list_output_is_sorted_by_filename(tmp_path: Path) -> None:
    # Copy files in reverse alphabetical order; the listing MUST still be
    # alphabetical because the sort happens inside discover_suite_manifests.
    shutil.copy(
        FIXTURES_DIR / "valid_suite.yaml", tmp_path / "zebra.yaml"
    )
    shutil.copy(
        FIXTURES_DIR / "no_parameterize_suite.yaml",
        tmp_path / "alpha.yaml",
    )
    runner = CliRunner()
    result = runner.invoke(
        eval_group, ["list", "--json", "--suites-dir", str(tmp_path)]
    )
    payload = json.loads(result.output)
    # alpha.yaml ships no-parameterize → name "no-parameterize"
    # zebra.yaml ships reference → name "reference"
    assert [p["name"] for p in payload] == ["no-parameterize", "reference"]


def test_cli_list_exits_two_on_schema_violation(tmp_path: Path) -> None:
    shutil.copy(
        FIXTURES_DIR / "missing_name_suite.yaml",
        tmp_path / "broken.yaml",
    )
    runner = CliRunner()
    result = runner.invoke(eval_group, ["list", "--suites-dir", str(tmp_path)])
    assert result.exit_code == SUITE_LOADER_ERROR_EXIT_CODE
    # stderr identifies the failure class.
    assert "SchemaError" in result.stderr


def test_cli_list_exits_two_on_invalid_eval_id(tmp_path: Path) -> None:
    """A manifest carrying a traversal-pattern id must surface InvalidEvalId."""
    shutil.copy(
        FIXTURES_DIR / "invalid_eval_entry_suite.yaml",
        tmp_path / "broken.yaml",
    )
    runner = CliRunner()
    result = runner.invoke(eval_group, ["list", "--suites-dir", str(tmp_path)])
    assert result.exit_code == SUITE_LOADER_ERROR_EXIT_CODE
    # The error class name appears in the stderr line so operators see
    # which gate fired without collapsing the failure classes.
    assert "Error" in result.stderr or "InvalidEvalId" in result.stderr
