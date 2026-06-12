"""NEW=CATCH skip-guard -- gates the proxy half on impl-ref existence (research/06 §C).

The NEW H-gate logic is PURE MARKDOWN (refs under the skill dir, authored by the sibling impl
branch ``feat/troubleshoot-pipeline-hardening``). There is NOTHING importable to probe, so the
NEW=CATCH half is guarded by ``pytest.mark.skipif`` keyed on impl-ref FILE EXISTENCE -- never
``importorskip`` (nothing to import) and never ``xfail`` (zero occurrences in this repo; SKIP is the
lower-noise, self-clearing choice). The OLD=MISS half runs UNCONDITIONALLY (no impl-ref dependency).

REPO_ROOT depth is ``parents[3]`` (NOT the impl suite's ``parents[2]``): our files live at
``tests/troubleshoot/backtest/<file>.py`` -- backtest -> troubleshoot -> tests -> repo root.
"""

from __future__ import annotations

from pathlib import Path

import pytest

# tests/troubleshoot/backtest/_impl_guard.py -> parents[3] == repo/worktree root.
# (test_path_resolution.py asserts (REPO_ROOT / "pyproject.toml").exists() to pin this depth.)
REPO_ROOT = Path(__file__).resolve().parents[3]

HARDENING_REFS = (
    REPO_ROOT / "src" / "superclaude" / "skills" / "sc-troubleshoot-protocol" / "refs"
)

# The two most foundational refs: a partial landing still guards correctly.
_FOUNDATION_REFS = ("pipeline-hardening-closure.md", "hardening-output-contract.md")

_IMPL_LANDED = all((HARDENING_REFS / name).exists() for name in _FOUNDATION_REFS)

requires_hardening_impl = pytest.mark.skipif(
    not _IMPL_LANDED,
    reason=(
        "NEW=CATCH half: sc-troubleshoot-protocol hardening refs not landed yet "
        f"({', '.join(_FOUNDATION_REFS)} absent under {HARDENING_REFS}). The OLD=MISS half runs "
        "unconditionally. Un-skips automatically once feat/troubleshoot-pipeline-hardening lands "
        "the refs."
    ),
)


def requires_impl_ref(ref_filename: str) -> pytest.MarkDecorator:
    """Build a ``skipif`` keyed on a SPECIFIC impl ref existing (e.g. ``unmask-and-sweep.md`` for H3).

    Used per NEW=CATCH proxy so each escape's proxy un-skips exactly when its own catch-mechanism ref
    lands. Self-documenting + self-clearing: the reason names the missing ref and the un-skip trigger.
    """
    ref_path = HARDENING_REFS / ref_filename
    return pytest.mark.skipif(
        not ref_path.exists(),
        reason=(
            f"NEW=CATCH proxy: impl ref {ref_filename!r} not landed yet (absent at {ref_path}). "
            "The matching OLD=MISS half runs unconditionally. Un-skips automatically once "
            "feat/troubleshoot-pipeline-hardening lands this ref."
        ),
    )
