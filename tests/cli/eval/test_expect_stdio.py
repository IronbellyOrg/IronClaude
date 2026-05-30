"""Per-primitive tests for ``Expect.stderr`` and ``Expect.stdout``
(COMP-010.5 / D-0069 / T04.07).

Both primitives operate on the ANSI-stripped buffer that
:class:`PtyStream` (T02.17) feeds into :class:`EvalContext` (T03.03).
They share a single internal predicate engine; this module exercises
each of the three named arguments — ``contains`` / ``regex`` /
``not_contains`` — against both primitives so any regression in the
shared engine surfaces on the targeted stream.

T04.01's ``tests/cli/eval/test_expect_primitives.py`` already covers
one happy-path stdout assertion and one happy-path stderr regex; this
module is the COMP-010.5 acceptance harness — it covers pass and fail
cases per argument, the ANSI-strip invariant, the declarative form,
and the ExpectResult envelope contract (DM-009).
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
        eval_id="ExpectStdioEval1",
        home_root=scratch_root,
        session_id="sess-expect-stdio-001",
    )
    iso.setup(config=EvalConfig(allowed_scratch_roots=(scratch_root,)))
    return iso


@pytest.fixture
def eval_spec() -> EvalSpec:
    return EvalSpec(id="ExpectStdioEval1", title="expect.stdio coverage")


def _make_ctx(
    *,
    eval_spec: EvalSpec,
    home: HomeIsolation,
    run_dir: Path,
    stdout: str = "",
    stderr: str = "",
) -> EvalContext:
    artifacts_dir = home.home_path / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = artifacts_dir / "stdout.log"
    stderr_path = artifacts_dir / "stderr.log"
    transcript_path = artifacts_dir / "pty.transcript"
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
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
        stdout=stdout,
        stderr=stderr,
        duration_sec=0.0,
        artifacts={},
    )


# ---------------------------------------------------------------------------
# stdout: contains
# ---------------------------------------------------------------------------


def test_stdout_contains_passes_when_substring_present(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stdout="claude is ready for input\n",
    )
    result = Expect.stdout(contains="ready")(ctx)
    assert isinstance(result, ExpectResult)
    assert result.passed, result.message
    assert result.name == "stdout"
    assert result.failure is None
    assert result.details == {"stream": "stdout"}


def test_stdout_contains_fails_when_substring_absent(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stdout="claude says goodbye\n",
    )
    result = Expect.stdout(contains="ready")(ctx)
    assert not result.passed
    assert isinstance(result.failure, ExpectFailure)
    assert result.failure.expect_name == "stdout"
    assert result.failure.expected == {"contains": "ready"}
    assert result.failure.actual == "claude says goodbye\n"
    assert "stdout missing substring 'ready'" in result.failure.message


# ---------------------------------------------------------------------------
# stdout: regex
# ---------------------------------------------------------------------------


def test_stdout_regex_passes_on_match(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stdout="step 1 of 5 complete\n",
    )
    result = Expect.stdout(regex=r"step \d+ of \d+ complete")(ctx)
    assert result.passed


def test_stdout_regex_fails_on_no_match(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stdout="hello world\n",
    )
    result = Expect.stdout(regex=r"^ERROR")(ctx)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.expected == {"regex": "^ERROR"}
    assert "stdout did not match regex '^ERROR'" in result.failure.message


# ---------------------------------------------------------------------------
# stdout: not_contains
# ---------------------------------------------------------------------------


def test_stdout_not_contains_passes_when_absent(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stdout="clean run\n",
    )
    result = Expect.stdout(not_contains="Traceback")(ctx)
    assert result.passed


def test_stdout_not_contains_fails_when_present(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stdout="Traceback (most recent call last)\n",
    )
    result = Expect.stdout(not_contains="Traceback")(ctx)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.expected == {"not_contains": "Traceback"}
    assert "stdout unexpectedly contained 'Traceback'" in result.failure.message


# ---------------------------------------------------------------------------
# stderr: contains / regex / not_contains
# ---------------------------------------------------------------------------


def test_stderr_contains_passes_when_substring_present(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stderr="warning: deprecated flag\n",
    )
    result = Expect.stderr(contains="deprecated")(ctx)
    assert result.passed
    assert result.name == "stderr"


def test_stderr_contains_fails_when_substring_absent(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stderr="warning: deprecated flag\n",
    )
    result = Expect.stderr(contains="fatal")(ctx)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.expect_name == "stderr"
    assert result.failure.expected == {"contains": "fatal"}


def test_stderr_regex_passes_on_match(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stderr="Error: missing config at /etc/foo.yaml\n",
    )
    result = Expect.stderr(regex=r"Error:\s+missing config")(ctx)
    assert result.passed


def test_stderr_regex_fails_on_no_match(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stderr="all clear\n",
    )
    result = Expect.stderr(regex=r"Error:")(ctx)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.expected == {"regex": "Error:"}


def test_stderr_not_contains_passes_when_absent(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stderr="benign log line\n",
    )
    result = Expect.stderr(not_contains="SecurityError")(ctx)
    assert result.passed


def test_stderr_not_contains_fails_when_present(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stderr="SecurityError: bad mount\n",
    )
    result = Expect.stderr(not_contains="SecurityError")(ctx)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.expected == {"not_contains": "SecurityError"}


# ---------------------------------------------------------------------------
# ANSI-strip invariant (COMP-011 / T02.17)
# ---------------------------------------------------------------------------


def test_stdout_strips_ansi_csi_before_match(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """Manifests feed raw transcripts that still carry CSI colour codes;
    the predicate engine re-strips ANSI so ``contains='ready'`` matches
    ``"\\x1b[32mready\\x1b[0m"`` verbatim."""
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stdout="\x1b[32mready\x1b[0m\n",
    )
    assert Expect.stdout(contains="ready")(ctx).passed
    # The reset code is stripped, so a substring assertion on the literal
    # escape never matches — the test pins the strip rather than the leak.
    assert not Expect.stdout(contains="\x1b[0m")(ctx).passed


def test_stderr_strips_ansi_osc_before_match(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """OSC bursts (title-set) are stripped too, so manifests asserting
    error text don't trip on the terminal-title escape that wraps it."""
    raw = "\x1b]0;claude\x07Error: subprocess died\n"
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path, stderr=raw)
    assert Expect.stderr(contains="Error: subprocess died")(ctx).passed


def test_stdout_not_contains_after_ansi_strip(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``not_contains`` operates on the stripped buffer so a manifest
    forbidding a phrase still rejects the same phrase wrapped in
    colour codes."""
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stdout="\x1b[31mTraceback\x1b[0m: oops\n",
    )
    result = Expect.stdout(not_contains="Traceback")(ctx)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.expected == {"not_contains": "Traceback"}


# ---------------------------------------------------------------------------
# Argument composition — predicates layer in declaration order
# ---------------------------------------------------------------------------


def test_stdout_contains_runs_before_regex(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """When both ``contains`` and ``regex`` are set, ``contains`` fires
    first; the failure payload pins the substring miss rather than the
    regex."""
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stdout="hello\n",
    )
    result = Expect.stdout(contains="missing", regex=r".*")(ctx)
    assert not result.passed
    assert result.failure is not None
    assert result.failure.expected == {"contains": "missing"}


def test_stdout_all_three_predicates_pass_together(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``contains`` + ``regex`` + ``not_contains`` may be combined; all
    three must hold for the assertion to pass."""
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stdout="step 3 of 5 complete\n",
    )
    result = Expect.stdout(
        contains="step",
        regex=r"\d+ of \d+",
        not_contains="ERROR",
    )(ctx)
    assert result.passed


# ---------------------------------------------------------------------------
# Declarative form / ExpectResult envelope
# ---------------------------------------------------------------------------


def test_from_mapping_threads_stdout_contains(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """``{stdout: {contains: 'ready'}}`` resolves to the same callable
    as the programmatic form."""
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stdout="ready\n",
    )
    decl = Expect.from_mapping({"stdout": {"contains": "ready"}})(ctx)
    prog = Expect.stdout(contains="ready")(ctx)
    assert decl.passed and prog.passed
    assert decl.name == prog.name == "stdout"


def test_from_mapping_threads_stderr_not_contains(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stderr="benign\n",
    )
    result = Expect.from_mapping({"stderr": {"not_contains": "SecurityError"}})(ctx)
    assert result.passed
    assert result.name == "stderr"


def test_stdout_result_carries_primitive_name_and_timing(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """ExpectResult envelope (DM-009) records ``name='stdout'`` and a
    non-negative ``duration_sec``."""
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stdout="hi\n",
    )
    callable_ = Expect.stdout(contains="hi")
    assert callable_.__name__ == "stdout"
    result = callable_(ctx)
    assert result.name == "stdout"
    assert result.duration_sec >= 0.0


def test_stderr_result_carries_primitive_name_and_timing(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(
        eval_spec=eval_spec,
        home=home,
        run_dir=tmp_path,
        stderr="hi\n",
    )
    callable_ = Expect.stderr(contains="hi")
    assert callable_.__name__ == "stderr"
    result = callable_(ctx)
    assert result.name == "stderr"
    assert result.duration_sec >= 0.0


# ---------------------------------------------------------------------------
# No-argument behaviour — degenerate predicate trivially passes
# ---------------------------------------------------------------------------


def test_stdout_no_args_passes_on_empty_buffer(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    """With no predicates supplied, the primitive trivially passes; this
    pins the contract for manifests that probe the stream is *reachable*
    without asserting content."""
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.stdout()(ctx)
    assert result.passed
    assert result.failure is None


def test_stderr_no_args_passes_on_empty_buffer(
    eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
) -> None:
    ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
    result = Expect.stderr()(ctx)
    assert result.passed
    assert result.failure is None
