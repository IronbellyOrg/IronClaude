"""FR-G5 hook-matcher coverage gate tests (T04.14 / D-0075 / R-075).

The gate enforces design-spec §1.5: for every hook matcher pattern P
registered in ``~/.claude/settings.json``, at least one eval in the
suite under test must issue a tool call whose name matches P. These
tests cover both the pure helpers and the CLI wiring on ``eval doctor
--check-coverage`` and ``eval run``.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.eval import commands as commands_module
from superclaude.cli.eval.commands import eval_group
from superclaude.cli.eval.coverage import (
    COVERAGE_GATE_FAILED_EXIT_CODE,
    COVERAGE_MISSING_ARTIFACT_PREFIX,
    CoverageMatcher,
    CoverageResult,
    coverage_gate,
    default_matcher_filter,
    eval_covers_pattern,
    extract_hook_matchers,
    sanitize_pattern_for_filename,
)
from superclaude.cli.eval.models import EvalSpec


# ---------------------------------------------------------------------------
# Helpers — pattern sanitisation + default matcher filter
# ---------------------------------------------------------------------------


def test_sanitize_pattern_preserves_safe_chars() -> None:
    """Letters, digits, ``_:.-`` survive unchanged."""
    assert (
        sanitize_pattern_for_filename("mcp__auggie__tool-v1.2")
        == "mcp__auggie__tool-v1.2"
    )


def test_sanitize_pattern_replaces_unsafe_chars() -> None:
    """Regex metacharacters and path separators collapse to ``_``."""
    sanitised = sanitize_pattern_for_filename("mcp__auggie__.*|mcp__airis-mcp-gateway__.*")
    # ``*`` and ``|`` are filesystem-unfriendly when piping; both become ``_``.
    assert "*" not in sanitised
    assert "|" not in sanitised
    assert sanitised.startswith("mcp__auggie__")


def test_default_matcher_filter_accepts_auggie_prefix() -> None:
    assert default_matcher_filter("mcp__auggie__.*") is True


def test_default_matcher_filter_accepts_auggie_mcp_prefix() -> None:
    assert default_matcher_filter("mcp__auggie-mcp__ask_question") is True


def test_default_matcher_filter_accepts_airis_prefix() -> None:
    assert default_matcher_filter("mcp__airis-mcp-gateway__.*") is True


def test_default_matcher_filter_rejects_non_mcp_patterns() -> None:
    """Built-in tool matchers (``Edit|Write``) are out of v1 scope."""
    assert default_matcher_filter("Edit|Write") is False
    assert default_matcher_filter(".*") is False


# ---------------------------------------------------------------------------
# extract_hook_matchers
# ---------------------------------------------------------------------------


def test_extract_hook_matchers_walks_every_event() -> None:
    settings = {
        "hooks": {
            "PreToolUse": [
                {"matcher": "mcp__auggie__.*", "hooks": []},
                {"matcher": "Edit|Write"},
            ],
            "PostToolUse": [{"matcher": "mcp__auggie-mcp__.*"}],
        }
    }
    matchers = extract_hook_matchers(settings)
    patterns = [m.pattern for m in matchers]
    events = [m.event for m in matchers]
    assert patterns == [
        "mcp__auggie__.*",
        "Edit|Write",
        "mcp__auggie-mcp__.*",
    ]
    assert events == ["PreToolUse", "PreToolUse", "PostToolUse"]


def test_extract_hook_matchers_skips_entries_without_matcher() -> None:
    settings = {"hooks": {"SessionStart": [{"hooks": [{"type": "command"}]}]}}
    assert extract_hook_matchers(settings) == ()


def test_extract_hook_matchers_handles_missing_hooks_key() -> None:
    assert extract_hook_matchers({}) == ()


# ---------------------------------------------------------------------------
# eval_covers_pattern
# ---------------------------------------------------------------------------


def _spec(eval_id: str, *tool_calls: str) -> EvalSpec:
    inputs = tuple({"expect_tool_call": tc} for tc in tool_calls)
    return EvalSpec(id=eval_id, title=eval_id, inputs=inputs)


def test_eval_covers_pattern_matches_prefix_regex() -> None:
    spec = _spec("E1", "mcp__auggie__ask_question")
    assert eval_covers_pattern(spec, "mcp__auggie__.*") is True


def test_eval_covers_pattern_misses_unrelated_tool_call() -> None:
    spec = _spec("E1", "mcp__serena__find_symbol")
    assert eval_covers_pattern(spec, "mcp__auggie__.*") is False


def test_eval_covers_pattern_handles_invalid_regex() -> None:
    """Unparseable regex returns False rather than raising."""
    spec = _spec("E1", "mcp__auggie__x")
    assert eval_covers_pattern(spec, "[broken") is False


def test_eval_covers_pattern_ignores_non_string_tool_calls() -> None:
    spec = EvalSpec(
        id="E1",
        title="E1",
        inputs=({"expect_tool_call": None},),
    )
    assert eval_covers_pattern(spec, "mcp__auggie__.*") is False


# ---------------------------------------------------------------------------
# coverage_gate — end-to-end behaviours
# ---------------------------------------------------------------------------


def test_coverage_gate_passes_when_settings_missing(tmp_path: Path) -> None:
    """Hosts without settings.json trivially pass the gate."""
    result = coverage_gate(
        settings_path=tmp_path / "nope.json",
        suite=(),
    )
    assert result.passed is True
    assert result.matchers == ()


def test_coverage_gate_passes_when_settings_unreadable_json(tmp_path: Path) -> None:
    """Malformed settings.json is treated as the empty matcher set."""
    bad = tmp_path / "settings.json"
    bad.write_text("{not json", encoding="utf-8")
    result = coverage_gate(settings_path=bad, suite=())
    assert result.passed is True


def test_coverage_gate_passes_when_every_pattern_has_a_covering_eval(
    tmp_path: Path,
) -> None:
    settings = tmp_path / "settings.json"
    settings.write_text(
        json.dumps(
            {
                "hooks": {
                    "PreToolUse": [
                        {"matcher": "mcp__auggie__.*"},
                        {"matcher": "mcp__auggie-mcp__.*"},
                        {"matcher": "mcp__airis-mcp-gateway__.*"},
                    ]
                }
            }
        ),
        encoding="utf-8",
    )
    suite = (
        _spec("E-auggie", "mcp__auggie__ask_question"),
        _spec("E-auggie-mcp", "mcp__auggie-mcp__ask_question"),
        _spec("E-airis", "mcp__airis-mcp-gateway__auggie_ask_question"),
    )
    result = coverage_gate(settings_path=settings, suite=suite, output_dir=tmp_path)
    assert result.passed is True
    assert len(result.matchers) == 3
    assert all(p in result.coverage_map for p in result.coverage_map)
    # No missing → no artifacts written.
    assert result.artifacts == {}


def test_coverage_gate_fails_and_writes_artifact_for_uncovered_pattern(
    tmp_path: Path,
) -> None:
    settings = tmp_path / "settings.json"
    settings.write_text(
        json.dumps(
            {
                "hooks": {
                    "PreToolUse": [
                        {"matcher": "mcp__auggie__.*"},
                        {"matcher": "mcp__airis-mcp-gateway__.*"},
                    ]
                }
            }
        ),
        encoding="utf-8",
    )
    suite = (_spec("E-auggie-only", "mcp__auggie__ask_question"),)
    out_dir = tmp_path / "run-out"
    result = coverage_gate(settings_path=settings, suite=suite, output_dir=out_dir)
    assert result.passed is False
    assert len(result.missing) == 1
    assert result.missing[0].pattern == "mcp__airis-mcp-gateway__.*"
    # Artifact filename pins the documented contract.
    artifact_path = result.artifacts["mcp__airis-mcp-gateway__.*"]
    assert artifact_path.name.startswith(COVERAGE_MISSING_ARTIFACT_PREFIX)
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert payload["coverage_missing"] is True
    assert payload["pattern"] == "mcp__airis-mcp-gateway__.*"
    assert payload["event"] == "PreToolUse"


def test_coverage_gate_fails_when_fourth_matcher_added_without_eval(
    tmp_path: Path,
) -> None:
    """Validation: 4th matcher with no covering eval flips the gate to FAIL.

    Acceptance criterion from the phase-4 tasklist: "stub a settings.json
    with a 4th matcher and confirm gate fails."
    """
    settings = tmp_path / "settings.json"
    settings.write_text(
        json.dumps(
            {
                "hooks": {
                    "PreToolUse": [
                        {"matcher": "mcp__auggie__.*"},
                        {"matcher": "mcp__auggie-mcp__.*"},
                        {"matcher": "mcp__airis-mcp-gateway__.*"},
                        # The 4th matcher — a hypothetical new MCP family that
                        # no eval in the suite issues a tool call for.
                        {"matcher": "mcp__auggie__novel_tool_v2"},
                    ]
                }
            }
        ),
        encoding="utf-8",
    )
    suite = (
        _spec("E-auggie", "mcp__auggie__ask_question"),
        _spec("E-auggie-mcp", "mcp__auggie-mcp__ask_question"),
        _spec("E-airis", "mcp__airis-mcp-gateway__auggie_ask_question"),
    )
    result = coverage_gate(settings_path=settings, suite=suite, output_dir=tmp_path)
    # First three patterns are still covered; only the 4th is uncovered.
    # But the prefix regex ``mcp__auggie__.*`` *would* cover the 4th
    # pattern's literal name as well — so we use a literal string the
    # broad ``.*`` patterns don't share an eval coverage relationship with.
    # Note: ``mcp__auggie__novel_tool_v2`` is searched as a regex against
    # the eval's expect_tool_call strings — none of the evals issue that
    # exact tool, so coverage is empty.
    missing_patterns = {m.pattern for m in result.missing}
    assert "mcp__auggie__novel_tool_v2" in missing_patterns
    assert result.passed is False


def test_coverage_gate_default_filter_skips_non_mcp_matchers(
    tmp_path: Path,
) -> None:
    """v1: ``Edit|Write`` is out of scope even with no covering eval."""
    settings = tmp_path / "settings.json"
    settings.write_text(
        json.dumps(
            {
                "hooks": {
                    "PreToolUse": [
                        {"matcher": "Edit|Write"},
                        {"matcher": "mcp__auggie__.*"},
                    ]
                }
            }
        ),
        encoding="utf-8",
    )
    suite = (_spec("E1", "mcp__auggie__ask_question"),)
    result = coverage_gate(settings_path=settings, suite=suite)
    # Only the auggie pattern is checked (Edit|Write filtered out).
    assert len(result.matchers) == 1
    assert result.matchers[0].pattern == "mcp__auggie__.*"
    assert result.passed is True


def test_coverage_gate_to_dict_serialises_full_result(tmp_path: Path) -> None:
    settings = tmp_path / "settings.json"
    settings.write_text(
        json.dumps({"hooks": {"PreToolUse": [{"matcher": "mcp__auggie__.*"}]}}),
        encoding="utf-8",
    )
    suite = (_spec("E1", "mcp__auggie__ask_question"),)
    result = coverage_gate(settings_path=settings, suite=suite)
    payload = result.to_dict()
    assert payload["passed"] is True
    assert payload["matchers"] == [
        {"event": "PreToolUse", "pattern": "mcp__auggie__.*"}
    ]
    assert payload["covered"] == [
        {"event": "PreToolUse", "pattern": "mcp__auggie__.*"}
    ]
    assert payload["coverage_map"] == {"mcp__auggie__.*": ["E1"]}


# ---------------------------------------------------------------------------
# CLI wiring — doctor --check-coverage
# ---------------------------------------------------------------------------


@pytest.fixture
def clean_host(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict:
    """Clean dev machine: every binary on PATH, ~/.claude/ extant.

    Mirrors :func:`tests/cli/eval/test_doctor.clean_host` so doctor
    invocations under ``--check-coverage`` start from the same baseline.
    """
    claude_home = tmp_path / ".claude"
    claude_home.mkdir()

    def fake_which(name: str) -> str:
        return f"/usr/bin/{name}"

    monkeypatch.setattr(shutil, "which", fake_which)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    monkeypatch.setattr(
        commands_module,
        "_default_claude_version_probe",
        lambda: "claude 0.5.1",
    )
    return {"home": tmp_path, "claude_home": claude_home}


def test_cli_doctor_check_coverage_passes_with_empty_settings(
    clean_host: dict,
) -> None:
    """No settings.json under the monkeypatched home → gate passes."""
    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor", "--check-coverage", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["coverage_gate"]["status"] == "passed"
    assert payload["coverage_gate"]["result"]["matchers"] == []


def test_cli_doctor_check_coverage_fails_when_uncovered_matcher_present(
    clean_host: dict,
) -> None:
    """Stub a settings.json with an uncovered matcher → exit 2 + stderr."""
    settings = clean_host["claude_home"] / "settings.json"
    settings.write_text(
        json.dumps(
            {"hooks": {"PreToolUse": [{"matcher": "mcp__auggie__.*"}]}}
        ),
        encoding="utf-8",
    )
    runner = CliRunner()
    # No --suite supplied: matchers-only mode means the auggie pattern
    # has no covering eval, so the gate fails.
    result = runner.invoke(eval_group, ["doctor", "--check-coverage"])
    assert result.exit_code == COVERAGE_GATE_FAILED_EXIT_CODE
    assert "coverage gate FAILED" in result.stderr
    assert "mcp__auggie__.*" in result.stderr


def test_cli_doctor_check_coverage_json_payload_carries_missing_list(
    clean_host: dict,
) -> None:
    settings = clean_host["claude_home"] / "settings.json"
    settings.write_text(
        json.dumps(
            {"hooks": {"PreToolUse": [{"matcher": "mcp__auggie__.*"}]}}
        ),
        encoding="utf-8",
    )
    runner = CliRunner()
    result = runner.invoke(
        eval_group, ["doctor", "--check-coverage", "--json"]
    )
    assert result.exit_code == COVERAGE_GATE_FAILED_EXIT_CODE
    payload = json.loads(result.stdout)
    assert payload["coverage_gate"]["status"] == "failed"
    missing = payload["coverage_gate"]["result"]["missing"]
    assert missing == [{"event": "PreToolUse", "pattern": "mcp__auggie__.*"}]


# ---------------------------------------------------------------------------
# Module surface contracts
# ---------------------------------------------------------------------------


def test_coverage_gate_exit_code_pins_design_spec_value() -> None:
    """Design-spec §4: every harness-rejection outcome is exit 2."""
    assert COVERAGE_GATE_FAILED_EXIT_CODE == 2


def test_coverage_result_passed_is_true_when_no_missing() -> None:
    result = CoverageResult(
        matchers=(CoverageMatcher(event="PreToolUse", pattern="x"),),
        covered=(CoverageMatcher(event="PreToolUse", pattern="x"),),
    )
    assert result.passed is True


def test_coverage_result_passed_is_false_when_missing_nonempty() -> None:
    result = CoverageResult(
        matchers=(CoverageMatcher(event="PreToolUse", pattern="x"),),
        missing=(CoverageMatcher(event="PreToolUse", pattern="x"),),
    )
    assert result.passed is False
