"""Unit tests for the ReplayExecutor seam (so it is no longer an orphaned seam).

These exercise the spawn -> observe driver (``ReplayExecutor`` /
``InProcessReplayExecutor`` / ``ReplayResult`` / ``ResolvedCallable`` / ``resolve_callable``)
WITHOUT any real git or subprocess work -- pure stub-invoker + inspection unit tests, so
they run fast and unconditionally (no skip-guard). The per-escape Phase 4 runners drive the
seam through ``run_prefix_replay_snippet`` / ``read_source_from_worktree`` instead; this file
covers the in-process executor contract directly.
"""

from __future__ import annotations

import inspect
from pathlib import Path

from tests.troubleshoot.backtest.git_replay import escape_by_id
from tests.troubleshoot.backtest.replay_executor import (
    VERDICT_ERROR,
    VERDICT_MISS,
    InProcessReplayExecutor,
    ReplayEscape,
    ReplayExecutor,
    ReplayResult,
    resolve_callable,
)


def test_backtest_executor_stub_invoker_returns_result() -> None:
    """A registered stub invoker -> ``replay(...)`` returns exactly the ReplayResult it yields."""
    escape = escape_by_id("E1")
    expected = ReplayResult(
        escape_id=escape.escape_id,
        verdict=VERDICT_MISS,
        observed=["--file", "x.md"],
        detail="stub: old protocol let the escape through",
    )

    def stub_invoker(esc: ReplayEscape, wt: Path) -> ReplayResult:
        assert esc.escape_id == "E1"
        assert isinstance(wt, Path)
        return expected

    executor = InProcessReplayExecutor(invokers={"E1": stub_invoker})
    result = executor.replay(escape, Path("/tmp/does-not-matter"))

    assert result is expected
    assert result.verdict == VERDICT_MISS
    assert result.escape_id == "E1"


def test_backtest_executor_missing_invoker_yields_error() -> None:
    """No invoker registered for the escape -> ``replay(...)`` returns VERDICT_ERROR."""
    escape = escape_by_id("E1")
    executor = InProcessReplayExecutor(invokers={})

    result = executor.replay(escape, Path("/tmp/does-not-matter"))

    assert result.verdict == VERDICT_ERROR
    assert result.escape_id == "E1"
    assert "no invoker registered" in result.detail


def test_backtest_executor_raising_invoker_folds_into_error() -> None:
    """A raising invoker -> the exception is folded into a VERDICT_ERROR (type named in detail)."""
    escape = escape_by_id("E2")

    def boom_invoker(esc: ReplayEscape, wt: Path) -> ReplayResult:
        raise ValueError("simulated invoker explosion")

    executor = InProcessReplayExecutor(invokers={"E2": boom_invoker})
    result = executor.replay(escape, Path("/tmp/does-not-matter"))

    assert result.verdict == VERDICT_ERROR
    assert result.escape_id == "E2"
    # The fold mentions the exception TYPE (mirrors run_eval classifying a raised executor).
    assert "ValueError" in result.detail


def test_backtest_resolve_callable_module_level_function() -> None:
    """``resolve_callable`` on a MODULE-LEVEL function: not class-bound, signature read."""
    from superclaude.cli.prd import gates

    resolved = resolve_callable(gates, "_check_parallel_instructions")

    assert resolved.is_class_bound is False
    assert resolved.owning_class is None
    assert resolved.qualname == "_check_parallel_instructions"
    assert resolved.signature is not None
    assert isinstance(resolved.signature, inspect.Signature)
    # The real signature was read from the live module (one positional ``content`` param).
    assert "content" in resolved.signature.parameters


class _LocalOwner:
    """A tiny local class-bound target -- avoids HEAD-drift on impl-owned class methods."""

    def _build_args(self, prefix: str, *, flag: bool = False) -> list[str]:
        out = [prefix]
        if flag:
            out.append("--flag")
        return out


def test_backtest_resolve_callable_class_bound_method() -> None:
    """``resolve_callable`` on a ``Class.method`` qualname: class-bound, owning class + signature."""
    # Resolve against THIS module (resolve_callable reads ``Class`` off the passed module object).
    import tests.troubleshoot.backtest.test_replay_executor as self_module

    resolved = resolve_callable(self_module, "_LocalOwner._build_args")

    assert resolved.is_class_bound is True
    assert resolved.owning_class is _LocalOwner
    assert resolved.qualname == "_LocalOwner._build_args"
    assert resolved.signature is not None
    assert isinstance(resolved.signature, inspect.Signature)
    # Real signature read: ``self``, ``prefix``, and the keyword-only ``flag``.
    assert "prefix" in resolved.signature.parameters
    assert "flag" in resolved.signature.parameters


def test_backtest_in_process_executor_satisfies_replay_executor_protocol() -> None:
    """``ReplayExecutor`` is a runtime_checkable Protocol that ``InProcessReplayExecutor`` satisfies."""
    executor = InProcessReplayExecutor()
    assert isinstance(executor, ReplayExecutor)
    assert hasattr(executor, "replay")
