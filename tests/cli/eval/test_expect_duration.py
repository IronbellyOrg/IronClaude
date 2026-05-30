"""Per-primitive tests for ``Expect.duration`` (COMP-010.6 / D-0070 /
T04.08).

``Expect.duration`` reads :attr:`EvalContext.duration_sec` (DM-010) and
asserts the eval body ran within an optional ``[min_sec, max_sec]``
envelope. The behaviour matrix per FR-EXP1 / COMP-010.6:

* **No bounds** — informational PASS that records ``observed_sec`` in
  ``ExpectResult.details`` so reports can chart benchmark numbers
  without forcing an assertion.
* **``max_sec`` only** — FAIL when ``observed > max_sec``; the missing
  ``min_sec`` bound is not enforced (informational on that axis).
* **``min_sec`` only** — FAIL when ``observed < min_sec``; the missing
  ``max_sec`` bound is not enforced.
* **Both bounds** — FAIL when either bound is violated; ``max_sec`` is
  checked first so an over-budget run produces the more actionable
  failure payload.

T04.01's ``tests/cli/eval/test_expect_primitives.py`` already covers a
single informational PASS and a single ``max_sec`` FAIL; this module is
the COMP-010.6 acceptance harness — it covers each bound mode, boundary
equality (``observed == bound``), the failure payload contract
(``expected`` / ``actual`` / ``message``), the declarative form, and
the DM-009 ExpectResult envelope.
"""

from __future__ import annotations

from pathlib import Path

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
        eval_id="ExpectDurationEval1",
        home_root=scratch_root,
        session_id="sess-expect-duration-001",
    )
    iso.setup(config=EvalConfig(allowed_scratch_roots=(scratch_root,)))
    return iso


@pytest.fixture
def eval_spec() -> EvalSpec:
    return EvalSpec(id="ExpectDurationEval1", title="expect.duration coverage")


def _make_ctx(
    *,
    eval_spec: EvalSpec,
    home: HomeIsolation,
    run_dir: Path,
    duration_sec: float,
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
        exit_code=0,
        stdout="",
        stderr="",
        duration_sec=duration_sec,
        artifacts={},
    )


# ---------------------------------------------------------------------------
# No bounds — informational PASS
# ---------------------------------------------------------------------------


def test_duration_no_bounds_passes_informationally(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """No bounds → trivial PASS; observed duration recorded in details
    so reports can chart benchmark numbers without asserting."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=2.5)
    result = Expect.duration()(ctx)
    assert isinstance(result, ExpectResult)
    assert result.passed
    assert result.failure is None
    assert result.name == "duration"
    assert result.details == {"observed_sec": 2.5}
    assert "informational" in result.message


def test_duration_no_bounds_records_zero_duration(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """A 0-second eval still emits an informational PASS rather than
    raising on the degenerate ``observed=0`` edge."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=0.0)
    result = Expect.duration()(ctx)
    assert result.passed
    assert result.details["observed_sec"] == 0.0


# ---------------------------------------------------------------------------
# max_sec only
# ---------------------------------------------------------------------------


def test_duration_max_sec_passes_when_under_budget(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=1.5)
    result = Expect.duration(max_sec=3.0)(ctx)
    assert result.passed
    assert result.failure is None
    assert result.details["observed_sec"] == 1.5


def test_duration_max_sec_passes_at_boundary(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``observed == max_sec`` is PASS — the implementation uses ``>``
    so the boundary is inclusive (allowed)."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=3.0)
    result = Expect.duration(max_sec=3.0)(ctx)
    assert result.passed


def test_duration_max_sec_fails_when_over_budget(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Mirrors the T04.08 validation example:
    ``duration_sec=5`` + ``max_sec=3`` → FAIL."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=5.0)
    result = Expect.duration(max_sec=3.0)(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expect_name == "duration"
    assert result.failure.expected == {"max_sec": 3.0}
    assert result.failure.actual == 5.0
    assert "exceeds max_sec" in result.failure.message
    # observed_sec is still surfaced in details so reports can chart it.
    assert result.details["observed_sec"] == 5.0


# ---------------------------------------------------------------------------
# min_sec only
# ---------------------------------------------------------------------------


def test_duration_min_sec_passes_when_above_floor(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Mirrors the T04.08 validation example:
    ``duration_sec=5`` + ``min_sec=2`` → PASS."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=5.0)
    result = Expect.duration(min_sec=2.0)(ctx)
    assert result.passed
    assert result.failure is None


def test_duration_min_sec_passes_at_boundary(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``observed == min_sec`` is PASS — the implementation uses ``<``
    so the boundary is inclusive (allowed)."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=2.0)
    result = Expect.duration(min_sec=2.0)(ctx)
    assert result.passed


def test_duration_min_sec_fails_when_below_floor(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=0.5)
    result = Expect.duration(min_sec=2.0)(ctx)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.expect_name == "duration"
    assert result.failure.expected == {"min_sec": 2.0}
    assert result.failure.actual == 0.5
    assert "below min_sec" in result.failure.message


# ---------------------------------------------------------------------------
# Both bounds set
# ---------------------------------------------------------------------------


def test_duration_both_bounds_pass_when_within_window(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=2.0)
    result = Expect.duration(min_sec=1.0, max_sec=3.0)(ctx)
    assert result.passed
    assert result.failure is None
    assert result.details["observed_sec"] == 2.0
    assert "within bounds" in result.message


def test_duration_both_bounds_fail_via_max_sec(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=10.0)
    result = Expect.duration(min_sec=1.0, max_sec=3.0)(ctx)
    assert not result.passed
    assert result.failure is not None
    # max_sec is evaluated first so the failure pins the over-budget bound.
    assert result.failure.expected == {"max_sec": 3.0}


def test_duration_both_bounds_fail_via_min_sec(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=0.1)
    result = Expect.duration(min_sec=1.0, max_sec=3.0)(ctx)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.expected == {"min_sec": 1.0}


def test_duration_both_bounds_max_evaluated_before_min(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Degenerate ``min_sec > max_sec`` window with ``observed`` outside
    both bounds: the implementation evaluates ``max_sec`` first, so the
    failure payload pins the over-budget bound regardless of which
    bound the manifest author considered "more wrong"."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=5.0)
    result = Expect.duration(min_sec=10.0, max_sec=3.0)(ctx)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.expected == {"max_sec": 3.0}


# ---------------------------------------------------------------------------
# Single-bound informational behaviour
# ---------------------------------------------------------------------------


def test_duration_max_only_does_not_fail_on_missing_min_bound(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """COMP-010.6 AC: when only one bound is set, the missing other
    bound is informational. A 0.0s eval against ``max_sec=5`` must PASS
    even though a hypothetical ``min_sec=1`` would have failed."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=0.0)
    result = Expect.duration(max_sec=5.0)(ctx)
    assert result.passed
    assert result.failure is None


def test_duration_min_only_does_not_fail_on_missing_max_bound(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Symmetric case: a huge eval against ``min_sec=1`` PASSes even
    though a hypothetical ``max_sec=10`` would have failed."""
    ctx = _make_ctx(
        eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=10_000.0
    )
    result = Expect.duration(min_sec=1.0)(ctx)
    assert result.passed
    assert result.failure is None


# ---------------------------------------------------------------------------
# Declarative form / ExpectResult envelope
# ---------------------------------------------------------------------------


def test_from_mapping_threads_duration_max_sec(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``{duration: {max_sec: 3.0}}`` resolves to the same callable as
    the programmatic form."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=1.0)
    decl = Expect.from_mapping({"duration": {"max_sec": 3.0}})(ctx)
    prog = Expect.duration(max_sec=3.0)(ctx)
    assert decl.passed and prog.passed
    assert decl.name == prog.name == "duration"


def test_from_mapping_threads_duration_both_bounds(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=2.0)
    result = Expect.from_mapping({"duration": {"min_sec": 1.0, "max_sec": 3.0}})(ctx)
    assert result.passed
    assert result.name == "duration"


def test_from_mapping_threads_duration_no_bounds(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``{duration: {}}`` invokes the informational form with no
    arguments."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=4.2)
    result = Expect.from_mapping({"duration": {}})(ctx)
    assert result.passed
    assert result.details == {"observed_sec": 4.2}


def test_duration_result_carries_primitive_name_and_timing(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """ExpectResult envelope (DM-009) records ``name='duration'`` and a
    non-negative ``duration_sec`` (time the assertion itself took, not
    the eval body)."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=1.0)
    callable_ = Expect.duration(max_sec=2.0)
    assert callable_.__name__ == "duration"
    result = callable_(ctx)
    assert result.name == "duration"
    assert result.duration_sec >= 0.0


def test_duration_failure_traceback_field_is_none_for_predicate_miss(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """A predicate miss (over-budget) is *not* an exception; the failure
    record carries ``traceback=None`` so the Reporter does not render a
    stack trace for an ordinary assertion failure."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, duration_sec=5.0)
    result = Expect.duration(max_sec=1.0)(ctx)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.traceback is None
