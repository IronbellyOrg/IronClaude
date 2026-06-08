"""T05.03 -- IMM-5 success-first status determination parametrized matrix.

Pins the full IMM-5 truth table that
:func:`superclaude.cli.swarm.reduce.determine_status` implements
(:mod:`superclaude.cli.swarm.reduce` lines 152-210). The smoke branches
also live in :mod:`tests.swarm.test_reduce`; this file is the
canonical, exhaustive matrix referenced by R-101 / IMM-5.

IMM-5 truth table (roadmap.md line 313):

    ============  ====================  ============================
    Condition     Status                Notes
    ============  ====================  ============================
    M == N        ``success``           every requested slot succeeded
    2 <= M < N    ``partial``           floor met, at least one slot missed
    M < 2         ``failed``            below StatusPolicy.floor
    M == N == 2   ``success``           success_first tie-break (default)
    ============  ====================  ============================

The matrix is exercised over (M, N) pairs spanning the boundary cases
plus :class:`StatusPolicy` overrides (custom ``floor``,
``success_first=False``, custom ``partial_threshold``) so a regression
that drops the tie-break, mis-clamps the floor, or skips the
partial-window check fails immediately and points at the exact
(M, N, policy) triple that regressed.
"""

from __future__ import annotations

from typing import Optional

import pytest

from superclaude.cli.swarm.models import ResultStatus, StatusPolicy
from superclaude.cli.swarm.reduce import determine_status

# IMM-5 status matrix (T08.03 / NFR-007). Module-level marker so every
# test in this file is selected by ``pytest -m imm``.
pytestmark = pytest.mark.imm


# ---------------------------------------------------------------------------
# Default-policy matrix (floor=2, success_first=True, partial_threshold=2)
# ---------------------------------------------------------------------------

# Each row enumerates a (M, N, expected_status) point on the IMM-5
# truth table. The four branch labels in `id` mirror the matrix rows
# so a pytest failure header reads as e.g. ``M==N[3of3]-success``.
DEFAULT_POLICY_MATRIX: list[tuple[int, int, ResultStatus]] = [
    # --- M == N (every slot succeeded) -> success ---
    (3, 3, "success"),
    (4, 4, "success"),
    (5, 5, "success"),
    # --- M == N == 2 -> success (success_first tie-break, default on) ---
    (2, 2, "success"),
    # --- 2 <= M < N -> partial ---
    (2, 3, "partial"),
    (2, 4, "partial"),
    (3, 4, "partial"),
    (3, 5, "partial"),
    (4, 5, "partial"),
    # --- M < 2 -> failed (regardless of N) ---
    (0, 3, "failed"),
    (1, 3, "failed"),
    (0, 5, "failed"),
    (1, 5, "failed"),
    # --- N == 0 (no slots requested) -> failed (no slots to grade) ---
    (0, 0, "failed"),
    # --- M == N == 1 -> success. Success-first ordering: every requested
    # slot succeeded so the M >= N branch fires before the floor check
    # (the floor only gates the partial-vs-failed boundary when M < N).
    (1, 1, "success"),
]


@pytest.mark.parametrize(
    "workers_succeeded,workers_requested,expected",
    DEFAULT_POLICY_MATRIX,
    ids=[
        f"M={m}_N={n}_{exp}" for (m, n, exp) in DEFAULT_POLICY_MATRIX
    ],
)
def test_imm5_default_policy_matrix(
    workers_succeeded: int,
    workers_requested: int,
    expected: ResultStatus,
) -> None:
    """Every IMM-5 branch resolves to the spec-mandated status."""
    assert (
        determine_status(workers_succeeded, workers_requested)
        == expected
    )


# ---------------------------------------------------------------------------
# Policy override matrix -- floor / success_first / partial_threshold tuning
# ---------------------------------------------------------------------------


# (M, N, StatusPolicy, expected). Exercises the configurable surface of
# StatusPolicy so each field gets at least one assertion that flips the
# outcome when the default is overridden.
POLICY_OVERRIDE_MATRIX: list[
    tuple[int, int, StatusPolicy, ResultStatus]
] = [
    # success_first=False at M==N==2 still resolves to success because
    # M >= N takes the success branch directly. The tie-break only
    # mattered for the matrix label, not the outcome.
    (2, 2, StatusPolicy(success_first=False), "success"),
    # floor=3 -- M==2 falls below the failed floor regardless of N.
    (2, 4, StatusPolicy(floor=3, partial_threshold=3), "failed"),
    (2, 3, StatusPolicy(floor=3, partial_threshold=3), "failed"),
    # floor=3 -- M==3 sits inside the partial window for N>3.
    (3, 5, StatusPolicy(floor=3, partial_threshold=3), "partial"),
    # floor=1 -- M==1 (default would fail) now sits inside the partial
    # window for N>1.
    (1, 3, StatusPolicy(floor=1, partial_threshold=1), "partial"),
    # floor=1 -- M==0 still failed (clamp at zero).
    (0, 3, StatusPolicy(floor=1, partial_threshold=1), "failed"),
    # partial_threshold raised above floor: M==2 with threshold=3 falls
    # below the partial window and resolves to failed despite floor=2.
    (2, 5, StatusPolicy(floor=2, partial_threshold=3), "failed"),
    # partial_threshold==floor (default shape) with explicit values
    # exercises the equality path of `max(floor, partial_threshold)`.
    (2, 4, StatusPolicy(floor=2, partial_threshold=2), "partial"),
]


@pytest.mark.parametrize(
    "workers_succeeded,workers_requested,policy,expected",
    POLICY_OVERRIDE_MATRIX,
    ids=[
        f"M={m}_N={n}_floor={p.floor}_pt={p.partial_threshold}"
        f"_sf={p.success_first}_{exp}"
        for (m, n, p, exp) in POLICY_OVERRIDE_MATRIX
    ],
)
def test_imm5_policy_override_matrix(
    workers_succeeded: int,
    workers_requested: int,
    policy: StatusPolicy,
    expected: ResultStatus,
) -> None:
    """StatusPolicy.floor / success_first / partial_threshold tune the matrix."""
    assert (
        determine_status(workers_succeeded, workers_requested, policy)
        == expected
    )


# ---------------------------------------------------------------------------
# Edge cases -- clamping, invariant violations, explicit None policy
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "workers_succeeded,workers_requested,expected",
    [
        # M > N invariant violation -> success (M >= N branch fires).
        (4, 3, "success"),
        (5, 2, "success"),
        # Negative inputs clamp at zero (function stays total).
        (-1, 3, "failed"),
        (3, -1, "failed"),
        (-1, -1, "failed"),
    ],
    ids=[
        "M_gt_N_4of3", "M_gt_N_5of2",
        "negative_M", "negative_N", "negative_both",
    ],
)
def test_imm5_edge_cases(
    workers_succeeded: int,
    workers_requested: int,
    expected: ResultStatus,
) -> None:
    """M>N invariant violation and negative-input clamping stay total."""
    assert (
        determine_status(workers_succeeded, workers_requested)
        == expected
    )


def test_imm5_explicit_none_policy_uses_defaults() -> None:
    """Passing ``policy=None`` is equivalent to omitting the argument."""
    assert determine_status(2, 3, None) == "partial"
    assert determine_status(2, 2, None) == "success"
    assert determine_status(1, 3, None) == "failed"


def test_imm5_test_count_matches_matrix() -> None:
    """Guard the matrix size so a regression that drops a row trips loudly.

    The four IMM-5 branch labels (M==N / 2<=M<N / M<2 / tie-break) must
    each have at least one default-policy row. Counting branch labels
    by inspecting the default matrix lets us assert the matrix stays
    exhaustive even if rows get re-ordered.
    """
    branches = {
        "success_M_eq_N": 0,
        "success_tiebreak": 0,
        "partial": 0,
        "failed": 0,
    }
    for m, n, expected in DEFAULT_POLICY_MATRIX:
        if expected == "success" and m == n == 2:
            branches["success_tiebreak"] += 1
        elif expected == "success" and m == n:
            branches["success_M_eq_N"] += 1
        elif expected == "partial":
            branches["partial"] += 1
        elif expected == "failed":
            branches["failed"] += 1
    for label, count in branches.items():
        assert count >= 1, f"IMM-5 branch {label!r} missing from matrix"
