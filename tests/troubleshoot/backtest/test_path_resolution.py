"""Pin the ``parents[3]`` repo-root depth -- an off-by-one would silently break every impl-ref
probe (``_impl_guard``) and the no-leaked-worktree assertions. Explicit guard test per research/06.
"""

from __future__ import annotations

from tests.troubleshoot.backtest import _impl_guard


def test_backtest_repo_root_resolves_to_pyproject() -> None:
    # parents[3] must land on the repo/worktree root that carries pyproject.toml.
    assert (_impl_guard.REPO_ROOT / "pyproject.toml").exists(), (
        f"REPO_ROOT {_impl_guard.REPO_ROOT} has no pyproject.toml -- parents[N] depth is wrong "
        "(must be parents[3] for tests/troubleshoot/backtest/<file>.py)"
    )
    # And it is the ROOT, not an intermediate tests/ or troubleshoot/ directory.
    assert _impl_guard.REPO_ROOT.name not in {"tests", "troubleshoot", "backtest"}, (
        f"REPO_ROOT resolved to {_impl_guard.REPO_ROOT.name!r}, not the repo root -- depth is wrong"
    )
