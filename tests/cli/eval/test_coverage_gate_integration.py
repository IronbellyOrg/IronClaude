"""FR-G5 coverage-gate integration tests (T05.25 / D-0102 / TEST-013).

End-to-end CLI assertions for the hook-matcher coverage gate as wired
into ``eval doctor --check-coverage`` and ``eval run``. The unit-level
behaviours of :mod:`superclaude.cli.eval.coverage` are covered by
``tests/cli/eval/test_coverage_gate.py``; this module pins the *integrated*
contract:

* ``doctor --check-coverage --suite <path>`` exits 0 when every matcher
  in ``~/.claude/settings.json`` has a covering eval.
* ``doctor --check-coverage --suite <path>`` exits ``2`` and names every
  uncovered matcher on stderr when a 4th matcher is added without a
  matching eval.
* ``eval run --suite <path>`` exits ``2`` at the top of the run when the
  same uncovered matcher is present, BEFORE any worker dispatch.
* A ``coverage_missing:<pattern>`` artifact lands in the run output
  directory whenever ``eval run`` short-circuits on the gate.

Fixtures live under ``tests/cli/eval/fixtures/coverage_gate/``:

* ``suite.yaml`` — three evals covering the v1 MCP prefixes.
* ``settings_complete.json`` — three matchers, fully covered.
* ``settings_missing.json`` — four matchers (3 covered + 1 uncovered).
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
    sanitize_pattern_for_filename,
)


# ---------------------------------------------------------------------------
# Fixture roots
# ---------------------------------------------------------------------------


FIXTURE_DIR: Path = Path(__file__).parent / "fixtures" / "coverage_gate"
SUITE_FIXTURE: Path = FIXTURE_DIR / "suite.yaml"
SETTINGS_COMPLETE: Path = FIXTURE_DIR / "settings_complete.json"
SETTINGS_MISSING: Path = FIXTURE_DIR / "settings_missing.json"


UNCOVERED_PATTERN: str = "mcp__auggie__novel_tool_v2"
"""The 4th matcher in ``settings_missing.json`` with no covering eval.

Chosen because it (a) passes :func:`default_matcher_filter` (contains
the ``mcp__auggie__`` prefix) and (b) does not appear inside any of
the fixture suite's ``expect_tool_call`` strings, so the regex
``re.search("mcp__auggie__novel_tool_v2", <tool-call>)`` returns
``None`` for every eval and the matcher is reported as ``missing``.
"""


@pytest.fixture
def clean_host(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict:
    """Redirect ``Path.home()`` and the doctor's claude-version probe.

    Mirrors :func:`tests/cli/eval/test_coverage_gate.clean_host` so the
    doctor + run wirings load the staged ``~/.claude/settings.json``
    instead of the real dev host's. Every binary on PATH is stubbed via
    :func:`shutil.which` so :func:`build_doctor_report` does not report
    a HARD failure that would mask the coverage-gate exit code.
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


def _stage_settings(claude_home: Path, source: Path) -> Path:
    """Copy a fixture settings.json into the monkeypatched home."""
    dest = claude_home / "settings.json"
    dest.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return dest


# ---------------------------------------------------------------------------
# doctor --check-coverage — PASS path
# ---------------------------------------------------------------------------


def test_doctor_check_coverage_passes_when_suite_covers_all_matchers(
    clean_host: dict,
) -> None:
    """3-matcher settings + 3-eval suite → gate green, exit 0, JSON ``passed``.

    Pins the AC bullet: "complete coverage passes".
    """
    _stage_settings(clean_host["claude_home"], SETTINGS_COMPLETE)
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "doctor",
            "--check-coverage",
            "--suite",
            str(SUITE_FIXTURE),
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output + (result.stderr or "")
    payload = json.loads(result.stdout)
    coverage = payload["coverage_gate"]
    assert coverage["status"] == "passed"
    matcher_patterns = {m["pattern"] for m in coverage["result"]["matchers"]}
    assert matcher_patterns == {
        "mcp__auggie__.*",
        "mcp__auggie-mcp__.*",
        "mcp__airis-mcp-gateway__.*",
    }
    assert coverage["result"]["missing"] == []
    covered_eval_ids = {
        eid
        for ids in coverage["result"]["coverage_map"].values()
        for eid in ids
    }
    assert covered_eval_ids == {"E1", "E2", "E3"}


# ---------------------------------------------------------------------------
# doctor --check-coverage — FAIL path
# ---------------------------------------------------------------------------


def test_doctor_check_coverage_fails_when_fourth_matcher_uncovered(
    clean_host: dict,
) -> None:
    """4-matcher settings + 3-eval suite → exit 2, stderr roster present.

    Pins the AC bullet: "missing matcher fails with exit 2".
    """
    _stage_settings(clean_host["claude_home"], SETTINGS_MISSING)
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "doctor",
            "--check-coverage",
            "--suite",
            str(SUITE_FIXTURE),
        ],
    )
    assert result.exit_code == COVERAGE_GATE_FAILED_EXIT_CODE
    assert "coverage gate FAILED" in result.stderr


def test_doctor_check_coverage_stderr_names_uncovered_pattern(
    clean_host: dict,
) -> None:
    """Stderr roster quotes the 4th matcher verbatim with its event tag.

    Pins the AC bullet: "doctor stderr names the uncovered pattern".
    The roster MUST also exclude the three covered matchers so operators
    can grep for the offending pattern without false positives.
    """
    _stage_settings(clean_host["claude_home"], SETTINGS_MISSING)
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "doctor",
            "--check-coverage",
            "--suite",
            str(SUITE_FIXTURE),
        ],
    )
    assert result.exit_code == COVERAGE_GATE_FAILED_EXIT_CODE
    # Uncovered pattern is named with its event tag.
    assert f"PreToolUse: {UNCOVERED_PATTERN}" in result.stderr
    # Covered matchers do NOT appear in the failure roster — only the
    # missing patterns are listed under "uncovered matcher patterns".
    failure_block = result.stderr.split(
        "uncovered matcher patterns:", maxsplit=1
    )[1]
    assert "mcp__auggie__.*" not in failure_block
    assert "mcp__auggie-mcp__.*" not in failure_block
    assert "mcp__airis-mcp-gateway__.*" not in failure_block


def test_doctor_check_coverage_json_payload_lists_uncovered_pattern(
    clean_host: dict,
) -> None:
    """``--json`` payload exposes the same uncovered pattern in ``missing``.

    The JSON path is the machine-consumable surface used by CI; this
    pins the parity contract between the stderr roster and the JSON
    ``coverage_gate.result.missing`` list.
    """
    _stage_settings(clean_host["claude_home"], SETTINGS_MISSING)
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "doctor",
            "--check-coverage",
            "--suite",
            str(SUITE_FIXTURE),
            "--json",
        ],
    )
    assert result.exit_code == COVERAGE_GATE_FAILED_EXIT_CODE
    payload = json.loads(result.stdout)
    coverage = payload["coverage_gate"]
    assert coverage["status"] == "failed"
    missing = coverage["result"]["missing"]
    assert {"event": "PreToolUse", "pattern": UNCOVERED_PATTERN} in missing
    # Every covered matcher ends up in ``covered``, not ``missing``.
    covered_patterns = {m["pattern"] for m in coverage["result"]["covered"]}
    assert covered_patterns == {
        "mcp__auggie__.*",
        "mcp__auggie-mcp__.*",
        "mcp__airis-mcp-gateway__.*",
    }


# ---------------------------------------------------------------------------
# eval run — top-of-run gate + artifact emission
# ---------------------------------------------------------------------------


def test_run_exits_2_when_settings_has_uncovered_matcher(
    clean_host: dict,
    allowlisted_output_dir: Path,
) -> None:
    """``eval run`` short-circuits with exit 2 at the top-of-run gate.

    The gate runs AFTER suite parse and BEFORE any worker dispatch, so
    a fixture missing-matcher case never spawns a child process.
    """
    _stage_settings(clean_host["claude_home"], SETTINGS_MISSING)
    output_dir = allowlisted_output_dir / "run-out"
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            str(SUITE_FIXTURE),
            "--output-dir",
            str(output_dir),
            "--parallel",
            "1",
        ],
    )
    assert result.exit_code == COVERAGE_GATE_FAILED_EXIT_CODE, (
        result.output + (result.stderr or "")
    )
    assert "coverage gate FAILED" in result.stderr
    assert UNCOVERED_PATTERN in result.stderr


def test_run_writes_coverage_missing_artifact_under_output_dir(
    clean_host: dict,
    allowlisted_output_dir: Path,
) -> None:
    """A ``coverage_missing:<pattern>`` file appears under ``--output-dir``.

    Pins the AC bullet: "Test asserts a ``coverage_missing:<pattern>``
    artifact file is produced". The artifact payload encodes the event
    tag and the pattern so post-mortem tooling can reconstruct the
    breach without re-reading settings.json.
    """
    _stage_settings(clean_host["claude_home"], SETTINGS_MISSING)
    output_dir = allowlisted_output_dir / "run-out"
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            str(SUITE_FIXTURE),
            "--output-dir",
            str(output_dir),
            "--parallel",
            "1",
        ],
    )
    assert result.exit_code == COVERAGE_GATE_FAILED_EXIT_CODE

    expected_filename = (
        f"{COVERAGE_MISSING_ARTIFACT_PREFIX}"
        f"{sanitize_pattern_for_filename(UNCOVERED_PATTERN)}"
    )
    # H1: coverage_missing:<pattern> artifacts land under the
    # compose_run_dir-derived run-dir, not directly under --output-dir.
    eval_runs_root = output_dir / ".dev" / "eval-runs"
    date_dirs = sorted(p for p in eval_runs_root.iterdir() if p.is_dir())
    assert len(date_dirs) == 1
    run_dirs = sorted(p for p in date_dirs[0].iterdir() if p.is_dir())
    assert len(run_dirs) == 1
    per_run_dir = run_dirs[0]

    artifact_path = per_run_dir / expected_filename
    assert artifact_path.is_file(), (
        f"expected artifact {artifact_path} not found; "
        f"per_run_dir contents = {sorted(p.name for p in per_run_dir.iterdir())}"
    )

    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert payload["coverage_missing"] is True
    assert payload["pattern"] == UNCOVERED_PATTERN
    assert payload["event"] == "PreToolUse"
    # Covered matchers MUST NOT have artifacts written; only the missing
    # 4th pattern emits a file.
    covered_artifact_names = [
        p.name
        for p in per_run_dir.iterdir()
        if p.name.startswith(COVERAGE_MISSING_ARTIFACT_PREFIX)
    ]
    assert covered_artifact_names == [expected_filename]
