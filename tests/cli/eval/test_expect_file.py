"""Per-primitive tests for ``Expect.file`` (COMP-010.1 / D-0065 / T04.02).

Covers all five named arguments of
``Expect.file(path, exists=None, contains=None, regex=None, equals=None)``
with positive and negative cases, plus the failure-side unified-diff
contract for ``equals``.

T04.01's ``tests/cli/eval/test_expect_primitives.py`` exercises the
declarative surface and one happy / one sad path; this module is the
COMP-010.1 acceptance harness — it must touch each named argument in
isolation and in combination, plus argument edge cases (absolute path,
UTF-8, multiline regex, ``exists=False`` skip semantics).
"""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

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
        eval_id="ExpectFileEval1",
        home_root=scratch_root,
        session_id="sess-expect-file-001",
    )
    iso.setup(config=EvalConfig(allowed_scratch_roots=(scratch_root,)))
    return iso


@pytest.fixture
def eval_spec() -> EvalSpec:
    return EvalSpec(id="ExpectFileEval1", title="expect.file coverage")


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


# ---------------------------------------------------------------------------
# path resolution
# ---------------------------------------------------------------------------


def test_relative_path_resolves_under_home(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Relative ``path`` resolves against ``ctx.home_path`` (DM-006)."""
    target = home.home_path / "report.txt"
    target.write_text("ok\n", encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path="report.txt", exists=True)(ctx)
    assert result.passed, result.message
    assert isinstance(result, ExpectResult)
    assert result.name == "file"
    assert result.details["path"] == str(target)


def test_absolute_path_is_used_verbatim(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Absolute ``path`` bypasses home_path resolution."""
    target = tmp_path / "absolute.txt"
    target.write_text("ok\n", encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path=str(target), exists=True)(ctx)
    assert result.passed
    assert result.details["path"] == str(target)


# ---------------------------------------------------------------------------
# exists
# ---------------------------------------------------------------------------


def test_exists_true_passes_when_present(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    (home.home_path / "a.txt").write_text("x", encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path="a.txt", exists=True)(ctx)
    assert result.passed


def test_exists_true_fails_when_missing(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path="missing.txt", exists=True)(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expect_name == "file"
    assert result.failure.expected == {"exists": True}
    assert result.failure.actual == {"exists": False}


def test_exists_false_passes_when_missing(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """When the file is missing and ``exists=False``, primitive passes
    without attempting further content assertions."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path="not-there.txt", exists=False)(ctx)
    assert result.passed
    assert result.failure is None


def test_exists_false_fails_when_present(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    (home.home_path / "a.txt").write_text("x", encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path="a.txt", exists=False)(ctx)
    assert not result.passed
    assert result.failure is not None


# ---------------------------------------------------------------------------
# contains
# ---------------------------------------------------------------------------


def test_contains_passes_on_substring_hit(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    (home.home_path / "log.txt").write_text(
        "harness started\nready to run\n", encoding="utf-8"
    )
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path="log.txt", contains="ready")(ctx)
    assert result.passed


def test_contains_fails_on_substring_miss(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    (home.home_path / "log.txt").write_text("harness started\n", encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path="log.txt", contains="ready")(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expected == {"contains": "ready"}
    # Actual carries the full content for downstream diffing / triage.
    assert result.failure.actual == "harness started\n"


def test_contains_supports_utf8(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    (home.home_path / "u.txt").write_text("héllo — wörld\n", encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path="u.txt", contains="wörld")(ctx)
    assert result.passed


# ---------------------------------------------------------------------------
# regex
# ---------------------------------------------------------------------------


def test_regex_passes_on_match(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    (home.home_path / "out.txt").write_text(
        "session-id: abc123\n", encoding="utf-8"
    )
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path="out.txt", regex=r"session-id:\s+\w+")(ctx)
    assert result.passed


def test_regex_fails_on_no_match(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    (home.home_path / "out.txt").write_text("nothing here\n", encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path="out.txt", regex=r"^ERROR\b")(ctx)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.expected == {"regex": r"^ERROR\b"}


def test_regex_matches_across_lines_via_search(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``re.compile(regex).search`` scans the whole buffer, so a pattern
    that anchors to a non-first line still matches."""
    (home.home_path / "m.txt").write_text(
        "line one\nERROR: boom\nline three\n", encoding="utf-8"
    )
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path="m.txt", regex=r"ERROR:\s+\w+")(ctx)
    assert result.passed


# ---------------------------------------------------------------------------
# equals + unified diff contract (D-0065 AC)
# ---------------------------------------------------------------------------


def test_equals_passes_on_exact_match(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    body = "PASS\n"
    (home.home_path / "x.txt").write_text(body, encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path="x.txt", equals=body)(ctx)
    assert result.passed


def test_equals_fails_with_unified_diff_in_details(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """AC: failure ExpectResult includes a unified diff snippet between
    expected and actual content."""
    (home.home_path / "x.txt").write_text(
        "line one\nline two\nline three\n", encoding="utf-8"
    )
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    expected = "line one\nLINE TWO\nline three\n"
    result = Expect.file(path="x.txt", equals=expected)(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expected == expected
    assert result.failure.actual == "line one\nline two\nline three\n"
    diff = result.details["diff"]
    # Unified diff format markers + the differing lines.
    assert diff.startswith("--- expected/")
    assert "+++ actual/" in diff
    assert "-LINE TWO" in diff or "-LINE TWO\n" in diff
    assert "+line two" in diff or "+line two\n" in diff


# ---------------------------------------------------------------------------
# Combined argument cases
# ---------------------------------------------------------------------------


def test_contains_and_regex_both_evaluated(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """When both ``contains`` and ``regex`` are set, both must hold."""
    (home.home_path / "c.txt").write_text(
        "status=ok pid=4242\n", encoding="utf-8"
    )
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    assert Expect.file(
        path="c.txt", contains="status=ok", regex=r"pid=\d+"
    )(ctx).passed
    # Substring match but regex misses.
    miss = Expect.file(
        path="c.txt", contains="status=ok", regex=r"pid=[a-z]+"
    )(ctx)
    assert not miss.passed


def test_exists_true_with_contains_fails_when_substring_missing(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``exists=True`` is satisfied but ``contains`` mismatch wins."""
    (home.home_path / "c.txt").write_text("PASS\n", encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path="c.txt", exists=True, contains="FAIL")(ctx)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.expected == {"contains": "FAIL"}


def test_no_assertions_passes_when_file_readable(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """With all named args ``None``, the primitive only asserts the file
    exists and is readable."""
    (home.home_path / "n.txt").write_text("x", encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.file(path="n.txt")(ctx)
    assert result.passed
    assert result.failure is None


# ---------------------------------------------------------------------------
# ExpectResult timing + name conventions
# ---------------------------------------------------------------------------


def test_result_carries_primitive_name_and_timing(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    (home.home_path / "t.txt").write_text("ok\n", encoding="utf-8")
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    callable_ = Expect.file(path="t.txt", exists=True)
    assert callable_.__name__ == "file"
    result = callable_(ctx)
    assert result.name == "file"
    assert result.duration_sec >= 0.0
