"""Per-primitive tests for ``Expect.jsonl`` (COMP-010.2 / D-0066 / T04.03).

Covers all five named arguments of
``Expect.jsonl(path, line_count=None, filter=None, assert_each=None, assert_any=None)``
with positive and negative cases, plus the predicate semantics
documented in :mod:`superclaude.cli.eval.expect`.

The fixture rows mirror the hook-telemetry shape that the sticky-
lifecycle (E1) and matcher-coverage (E2.x) evals will assert against:
each row is a ``{event, matcher, tool, status, ts}`` mapping written one
per line in UTF-8. ``Expect.jsonl`` resolves ``path`` against the
context's named ``jsonl_paths`` mapping first, falling back to
``ctx.home_path`` — both branches are exercised here.

T04.01's ``tests/cli/eval/test_expect_primitives.py`` covers the
declarative surface and one happy path per primitive; this module is the
COMP-010.2 acceptance harness: every named argument is touched in
isolation and in combination, including error-path coverage for missing
files and malformed lines.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import pytest

from superclaude.cli.eval.config import EvalConfig
from superclaude.cli.eval.expect import Expect
from superclaude.cli.eval.isolation import HomeIsolation
from superclaude.cli.eval.models import (
    EvalContext,
    EvalSpec,
    ExpectFailure,
    ExpectResult,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def scratch_root(tmp_path: Path) -> Path:
    root = tmp_path / "scratch"
    root.mkdir()
    return root


@pytest.fixture
def home(scratch_root: Path) -> HomeIsolation:
    iso = HomeIsolation(
        eval_id="ExpectJsonlEval1",
        home_root=scratch_root,
        session_id="sess-expect-jsonl-001",
    )
    iso.setup(config=EvalConfig(allowed_scratch_roots=(scratch_root,)))
    return iso


@pytest.fixture
def eval_spec() -> EvalSpec:
    return EvalSpec(id="ExpectJsonlEval1", title="expect.jsonl coverage")


def _make_ctx(
    *,
    eval_spec: EvalSpec,
    home: HomeIsolation,
    run_dir: Path,
    jsonl_paths: Mapping[str, Path] | None = None,
) -> EvalContext:
    artifacts_dir = home.home_path / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = artifacts_dir / "stdout.log"
    stderr_path = artifacts_dir / "stderr.log"
    transcript_path = artifacts_dir / "pty.transcript"
    stdout_path.write_text("", encoding="utf-8")
    stderr_path.write_text("", encoding="utf-8")
    return EvalContext.from_runner_state(
        eval_spec=eval_spec,
        home=home,
        run_dir=run_dir,
        artifacts_dir=artifacts_dir,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        transcript_path=transcript_path,
        jsonl_paths=jsonl_paths or {},
        env={"HOME": str(home.home_path)},
        exit_code=0,
        stdout="",
        stderr="",
        duration_sec=0.0,
        artifacts={},
    )


# Canonical hook-telemetry fixture used across the test matrix.
# Shape mirrors the per-eval ``hooks.jsonl`` emitted by the runner's
# HookAdapter (T02.16 / T03.06): one JSON object per line, each carrying
# event, matcher, tool, status, and a monotonically increasing ts.
HOOK_ROWS: tuple[dict[str, Any], ...] = (
    {
        "event": "PreToolUse",
        "matcher": "mcp__auggie__*",
        "tool": "mcp__auggie__codebase-retrieval",
        "status": "allow",
        "ts": 1,
    },
    {
        "event": "PostToolUse",
        "matcher": "mcp__auggie__*",
        "tool": "mcp__auggie__codebase-retrieval",
        "status": "ok",
        "ts": 2,
    },
    {
        "event": "PreToolUse",
        "matcher": "mcp__airis-mcp-gateway__*",
        "tool": "mcp__airis-mcp-gateway__list",
        "status": "allow",
        "ts": 3,
    },
    {
        "event": "PostToolUse",
        "matcher": "mcp__airis-mcp-gateway__*",
        "tool": "mcp__airis-mcp-gateway__list",
        "status": "ok",
        "ts": 4,
    },
    {
        "event": "Stop",
        "matcher": None,
        "tool": None,
        "status": "session_end",
        "ts": 5,
    },
)


def _write_jsonl(path: Path, rows: tuple[Mapping[str, Any], ...]) -> Path:
    """Serialize ``rows`` to ``path`` as one JSON object per line (UTF-8)."""
    payload = "".join(json.dumps(r) + "\n" for r in rows)
    path.write_text(payload, encoding="utf-8")
    return path


@pytest.fixture
def hook_log(home: HomeIsolation) -> Path:
    return _write_jsonl(home.home_path / "hooks.jsonl", HOOK_ROWS)


# ---------------------------------------------------------------------------
# path resolution
# ---------------------------------------------------------------------------


def test_named_path_resolves_via_jsonl_paths(
    eval_spec: EvalSpec, home: HomeIsolation, hook_log: Path, tmp_path: Path
) -> None:
    """``path`` first resolves against ``ctx.jsonl_paths`` by name."""
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        jsonl_paths={"hook_log": hook_log},
    )
    result = Expect.jsonl(path="hook_log", line_count=len(HOOK_ROWS))(ctx)
    assert result.passed, result.message
    assert isinstance(result, ExpectResult)
    assert result.name == "jsonl"
    assert result.details["path"] == str(hook_log)


def test_relative_path_resolves_under_home(
    eval_spec: EvalSpec, home: HomeIsolation, hook_log: Path, tmp_path: Path
) -> None:
    """When ``path`` is not a named lookup, it resolves against home_path."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.jsonl(path="hooks.jsonl", line_count=len(HOOK_ROWS))(ctx)
    assert result.passed, result.message
    assert result.details["path"] == str(hook_log)


def test_absolute_path_is_used_verbatim(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Absolute ``path`` bypasses home_path entirely."""
    target = tmp_path / "absolute.jsonl"
    _write_jsonl(target, HOOK_ROWS[:2])
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.jsonl(path=str(target), line_count=2)(ctx)
    assert result.passed
    assert result.details["path"] == str(target)


def test_missing_file_fails_with_existence_payload(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """A missing path produces a structured failure (no FileNotFoundError)."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.jsonl(path="not-there.jsonl")(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expect_name == "jsonl"
    assert result.failure.expected == {"exists": True}
    assert result.failure.actual == {"exists": False}


# ---------------------------------------------------------------------------
# line_count
# ---------------------------------------------------------------------------


def test_line_count_passes_on_exact_match(
    eval_spec: EvalSpec, home: HomeIsolation, hook_log: Path, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.jsonl(path="hooks.jsonl", line_count=5)(ctx)
    assert result.passed


def test_line_count_fails_on_mismatch(
    eval_spec: EvalSpec, home: HomeIsolation, hook_log: Path, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.jsonl(path="hooks.jsonl", line_count=99)(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expected == {"line_count": 99}
    assert result.failure.actual == {"line_count": 5}


def test_line_count_zero_passes_on_empty_jsonl(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """An empty JSONL satisfies ``line_count=0``."""
    target = home.home_path / "empty.jsonl"
    target.write_text("", encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.jsonl(path="empty.jsonl", line_count=0)(ctx)
    assert result.passed


def test_line_count_ignores_blank_lines(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Blank / whitespace-only lines are not counted (matches loader semantics)."""
    target = home.home_path / "padded.jsonl"
    target.write_text(
        '{"event": "a"}\n\n   \n{"event": "b"}\n', encoding="utf-8"
    )
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.jsonl(path="padded.jsonl", line_count=2)(ctx)
    assert result.passed


# ---------------------------------------------------------------------------
# filter
# ---------------------------------------------------------------------------


def test_filter_narrows_rows_before_line_count(
    eval_spec: EvalSpec, home: HomeIsolation, hook_log: Path, tmp_path: Path
) -> None:
    """``filter`` is applied before ``line_count`` evaluates."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    # Two PreToolUse rows in HOOK_ROWS.
    result = Expect.jsonl(
        path="hooks.jsonl",
        line_count=2,
        filter=lambda r: r.get("event") == "PreToolUse",
    )(ctx)
    assert result.passed, result.message


def test_filter_to_zero_rows_passes_with_count_zero(
    eval_spec: EvalSpec, home: HomeIsolation, hook_log: Path, tmp_path: Path
) -> None:
    """A filter that excludes everything yields an empty filtered set."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.jsonl(
        path="hooks.jsonl",
        line_count=0,
        filter=lambda r: r.get("event") == "Never",
    )(ctx)
    assert result.passed


# ---------------------------------------------------------------------------
# assert_each
# ---------------------------------------------------------------------------


def test_assert_each_passes_when_all_rows_match(
    eval_spec: EvalSpec, home: HomeIsolation, hook_log: Path, tmp_path: Path
) -> None:
    """Filtered set: every PreToolUse row carries ``status='allow'``."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.jsonl(
        path="hooks.jsonl",
        filter=lambda r: r.get("event") == "PreToolUse",
        assert_each=lambda r: r.get("status") == "allow",
    )(ctx)
    assert result.passed, result.message


def test_assert_each_fails_on_first_mismatch(
    eval_spec: EvalSpec, home: HomeIsolation, hook_log: Path, tmp_path: Path
) -> None:
    """``assert_each`` short-circuits on the first failing row."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.jsonl(
        path="hooks.jsonl",
        assert_each=lambda r: r.get("status") == "allow",  # PostToolUse rows say "ok"
    )(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expected == {"assert_each": "predicate true"}
    # The PostToolUse row at index 1 is the first non-"allow" status.
    assert result.details["row_index"] == 1
    assert result.failure.actual["event"] == "PostToolUse"


# ---------------------------------------------------------------------------
# assert_any
# ---------------------------------------------------------------------------


def test_assert_any_passes_when_one_row_matches(
    eval_spec: EvalSpec, home: HomeIsolation, hook_log: Path, tmp_path: Path
) -> None:
    """AC: ``assert_any`` returns ``passed=True`` if at least one filtered
    line satisfies the predicate."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.jsonl(
        path="hooks.jsonl",
        assert_any=lambda r: r.get("matcher") == "mcp__airis-mcp-gateway__*",
    )(ctx)
    assert result.passed


def test_assert_any_fails_when_no_row_matches(
    eval_spec: EvalSpec, home: HomeIsolation, hook_log: Path, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.jsonl(
        path="hooks.jsonl",
        assert_any=lambda r: r.get("matcher") == "mcp__never__*",
    )(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expected == {"assert_any": "any matching row"}


def test_assert_any_runs_against_filtered_subset(
    eval_spec: EvalSpec, home: HomeIsolation, hook_log: Path, tmp_path: Path
) -> None:
    """``filter`` narrows the search space ``assert_any`` walks over."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    # The Stop row has status='session_end'; if filtered out, assert_any fails.
    result = Expect.jsonl(
        path="hooks.jsonl",
        filter=lambda r: r.get("event") != "Stop",
        assert_any=lambda r: r.get("status") == "session_end",
    )(ctx)
    assert not result.passed


# ---------------------------------------------------------------------------
# Malformed input
# ---------------------------------------------------------------------------


def test_invalid_json_line_fails_with_lineno(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """A line that is not valid JSON produces a structured failure
    naming the offending line."""
    target = home.home_path / "bad.jsonl"
    target.write_text(
        '{"event": "a"}\nNOT JSON\n{"event": "b"}\n', encoding="utf-8"
    )
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.jsonl(path="bad.jsonl")(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expected == "valid JSON per line"
    assert result.failure.actual == "NOT JSON"
    assert "line 2" in result.failure.message
    assert result.failure.traceback is not None


# ---------------------------------------------------------------------------
# Combined / envelope
# ---------------------------------------------------------------------------


def test_no_assertions_passes_when_file_parsable(
    eval_spec: EvalSpec, home: HomeIsolation, hook_log: Path, tmp_path: Path
) -> None:
    """With all named args ``None``, the primitive only asserts the file
    exists and contains valid JSON per line."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.jsonl(path="hooks.jsonl")(ctx)
    assert result.passed
    assert result.failure is None
    assert result.details["rows_inspected"] == len(HOOK_ROWS)


def test_combined_filter_line_count_assert_each(
    eval_spec: EvalSpec, home: HomeIsolation, hook_log: Path, tmp_path: Path
) -> None:
    """Realistic hook-telemetry assertion: two auggie matcher rows, all 'allow'."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.jsonl(
        path="hooks.jsonl",
        filter=lambda r: r.get("matcher") == "mcp__auggie__*",
        line_count=2,
        assert_each=lambda r: r.get("status") in {"allow", "ok"},
    )(ctx)
    assert result.passed, result.message


def test_result_carries_primitive_name_and_timing(
    eval_spec: EvalSpec, home: HomeIsolation, hook_log: Path, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    callable_ = Expect.jsonl(path="hooks.jsonl")
    assert callable_.__name__ == "jsonl"
    result = callable_(ctx)
    assert result.name == "jsonl"
    assert result.duration_sec >= 0.0
