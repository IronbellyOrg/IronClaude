"""Per-primitive tests for ``Expect.exit_code`` (COMP-010.4 / D-0068 / T04.05).

Covers all three named arguments of
``Expect.exit_code(equals=0, in_set=None, not_equals=None)`` with positive
and negative cases, the default-``equals=0`` behaviour, the mutual-
exclusion guard between ``equals`` and ``in_set``, and the
ExpectResult envelope contract (DM-009).

T04.01's ``tests/cli/eval/test_expect_primitives.py`` already covers the
declarative surface and one happy / one sad path; this module is the
COMP-010.4 acceptance harness — it touches each named argument in
isolation and in combination, including edge cases around the sentinel
default, iterable ``in_set`` inputs, and combining ``not_equals`` with
``equals`` / ``in_set``.
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
        eval_id="ExpectExitCodeEval1",
        home_root=scratch_root,
        session_id="sess-expect-exit-code-001",
    )
    iso.setup(config=EvalConfig(allowed_scratch_roots=(scratch_root,)))
    return iso


@pytest.fixture
def eval_spec() -> EvalSpec:
    return EvalSpec(id="ExpectExitCodeEval1", title="expect.exit_code coverage")


def _make_ctx(
    *,
    eval_spec: EvalSpec,
    home: HomeIsolation,
    run_dir: Path,
    exit_code: int,
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
        jsonl_paths={},
        env={"HOME": str(home.home_path)},
        exit_code=exit_code,
        stdout="",
        stderr="",
        duration_sec=0.0,
        artifacts={},
    )


# ---------------------------------------------------------------------------
# Default behaviour — equals=0 is implicit
# ---------------------------------------------------------------------------


def test_default_passes_on_zero(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """No-argument invocation asserts ``equals=0``."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=0)
    result = Expect.exit_code()(ctx)
    assert isinstance(result, ExpectResult)
    assert result.passed, result.message
    assert result.name == "exit_code"
    assert result.failure is None
    assert result.details["actual"] == 0


def test_default_fails_on_nonzero(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """No-argument invocation FAILs when ``ctx.exit_code != 0``."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=1)
    result = Expect.exit_code()(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expect_name == "exit_code"
    assert result.failure.expected == 0
    assert result.failure.actual == 1
    assert "exit_code expected 0 got 1" in result.failure.message


# ---------------------------------------------------------------------------
# equals semantics (explicit)
# ---------------------------------------------------------------------------


def test_equals_explicit_passes_on_match(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Explicit ``equals=N`` passes when ``ctx.exit_code == N``."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=42)
    result = Expect.exit_code(equals=42)(ctx)
    assert result.passed
    assert result.details["actual"] == 42


def test_equals_explicit_fails_on_mismatch(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Explicit ``equals=N`` FAILs when ``ctx.exit_code != N`` and carries
    the failure payload (DM-005)."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=2)
    result = Expect.exit_code(equals=0)(ctx)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.expected == 0
    assert result.failure.actual == 2


def test_equals_supports_nonzero_default_override(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Manifests can pin a non-zero exit code (e.g. expecting a failure
    code from a known-error eval)."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=137)
    result = Expect.exit_code(equals=137)(ctx)
    assert result.passed


# ---------------------------------------------------------------------------
# in_set semantics
# ---------------------------------------------------------------------------


def test_in_set_passes_when_member(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``in_set`` passes when the captured exit code is one of the
    allowed values."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=2)
    result = Expect.exit_code(in_set={0, 1, 2})(ctx)
    assert result.passed
    assert result.details["actual"] == 2


def test_in_set_fails_when_not_member(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``in_set`` FAILs when the captured exit code is outside the
    allowed set; failure payload pins the membership expectation."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=3)
    result = Expect.exit_code(in_set={0, 1})(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expected == {"in_set": [0, 1]}
    assert result.failure.actual == 3


def test_in_set_accepts_list_input(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``in_set`` accepts any iterable, not just ``set``; declarative
    manifests load JSON arrays that arrive as ``list``."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=1)
    result = Expect.exit_code(in_set=[0, 1])(ctx)
    assert result.passed


def test_in_set_accepts_tuple_input(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``in_set`` also accepts tuples (YAML loaders sometimes emit them)."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=0)
    result = Expect.exit_code(in_set=(0,))(ctx)
    assert result.passed


def test_in_set_empty_iterable_always_fails(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """An empty ``in_set`` cannot match any exit code; the primitive
    treats it as a permanent FAIL rather than degenerating to "no check"."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=0)
    result = Expect.exit_code(in_set=set())(ctx)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.expected == {"in_set": []}


# ---------------------------------------------------------------------------
# not_equals semantics
# ---------------------------------------------------------------------------


def test_not_equals_passes_when_different(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``not_equals`` passes when the captured code is different from the
    forbidden value. Combined with the default ``equals=0``, the eval
    code must be 0 AND not the not_equals value — but tests below pin
    each axis separately too."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=0)
    result = Expect.exit_code(not_equals=1)(ctx)
    assert result.passed


def test_not_equals_fails_when_equal(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``not_equals`` FAILs when the captured code matches the forbidden
    value; combined with the implicit ``equals=0`` default it short-
    circuits on the equals branch first when exit_code != 0, so this
    test pins exit_code at 0 and forbids 0 explicitly."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=0)
    result = Expect.exit_code(not_equals=0)(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expected == {"not_equals": 0}
    assert result.failure.actual == 0


def test_not_equals_combines_with_in_set(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``not_equals`` is composable with ``in_set``: code must be in the
    allowed set AND not be the forbidden code."""
    ctx_pass = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=2)
    assert Expect.exit_code(in_set={0, 1, 2}, not_equals=1)(ctx_pass).passed

    ctx_fail = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=1)
    result = Expect.exit_code(in_set={0, 1, 2}, not_equals=1)(ctx_fail)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.expected == {"not_equals": 1}


def test_not_equals_combines_with_equals(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``not_equals`` may also be combined with explicit ``equals``;
    the equals branch is evaluated first."""
    ctx_pass = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=0)
    assert Expect.exit_code(equals=0, not_equals=1)(ctx_pass).passed

    ctx_fail = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=1)
    result = Expect.exit_code(equals=0, not_equals=1)(ctx_fail)
    assert not result.passed
    # equals check fires first — the failure reports the equals mismatch.
    assert result.failure is not None
    assert result.failure.expected == 0
    assert result.failure.actual == 1


# ---------------------------------------------------------------------------
# Mutual-exclusion guard between equals and in_set
# ---------------------------------------------------------------------------


def test_equals_and_in_set_raises_value_error() -> None:
    """Supplying both ``equals`` and ``in_set`` raises at construction
    time so misconfigured manifests fail loudly before runtime."""
    with pytest.raises(ValueError, match="mutually exclusive"):
        Expect.exit_code(equals=0, in_set={0, 1})


def test_default_equals_does_not_collide_with_in_set(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Passing ``in_set`` without ``equals`` must not trip the mutex
    guard — the sentinel default distinguishes implicit-equals from
    explicit-equals. This test pins that contract."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=0)
    # Should NOT raise even though `equals` has a default of 0.
    callable_ = Expect.exit_code(in_set={0, 1})
    result = callable_(ctx)
    assert result.passed


# ---------------------------------------------------------------------------
# Declarative form / ExpectResult envelope
# ---------------------------------------------------------------------------


def test_from_mapping_threads_in_set(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Declarative ``{exit_code: {in_set: [0, 1]}}`` resolves to the same
    callable as the programmatic form."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=1)
    decl = Expect.from_mapping({"exit_code": {"in_set": [0, 1]}})(ctx)
    prog = Expect.exit_code(in_set=[0, 1])(ctx)
    assert decl.passed and prog.passed
    assert decl.name == prog.name == "exit_code"


def test_from_mapping_threads_not_equals(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=0)
    result = Expect.from_mapping(
        {"exit_code": {"equals": 0, "not_equals": 1}}
    )(ctx)
    assert result.passed


def test_result_carries_primitive_name_and_timing(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """ExpectResult envelope (DM-009) records ``name='exit_code'`` and a
    non-negative ``duration_sec``."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=0)
    callable_ = Expect.exit_code()
    assert callable_.__name__ == "exit_code"
    result = callable_(ctx)
    assert result.name == "exit_code"
    assert result.duration_sec >= 0.0
    assert result.details == {"actual": 0}


def test_failure_message_includes_in_set_membership(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """The failure message names the actual exit code and the sorted
    allowed set so log-trawling reviewers can triage without re-running."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, exit_code=9)
    result = Expect.exit_code(in_set={2, 1, 0})(ctx)
    assert not result.passed
    assert result.failure is not None
    # sorted([0, 1, 2]) — deterministic ordering for golden-log comparisons.
    assert result.failure.message == "exit_code 9 not in [0, 1, 2]"
