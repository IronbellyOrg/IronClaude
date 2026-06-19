"""Stage-3 — TurnLedger atomic try_launch prevents budget over-commit under K>1.

The pre-Stage-3 gate was a check-then-act: ``can_launch()`` then ``debit(...)``,
a TOCTOU spanning two calls. Under concurrency two workers could both pass the
check and both debit, over-committing the budget. The atomic ``try_launch`` makes
check-and-debit one operation. This test drives far more concurrent launch
attempts than the budget allows and asserts EXACTLY N succeed.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import pytest

from superclaude.cli.sprint.models import TurnLedger


@pytest.mark.slow
def test_try_launch_grants_exactly_n_under_concurrency() -> None:
    minimum = 5
    n_allowed = 20
    # Budget allows EXACTLY n_allowed launches of `minimum` turns each.
    ledger = TurnLedger(initial_budget=n_allowed * minimum, minimum_allocation=minimum)

    n_attempts = 400  # far more than n_allowed → exposes any over-commit race

    def _attempt(_i: int) -> bool:
        return ledger.try_launch()

    with ThreadPoolExecutor(max_workers=16) as pool:
        outcomes = list(pool.map(_attempt, range(n_attempts)))

    granted = sum(1 for ok in outcomes if ok)
    assert granted == n_allowed, (
        f"budget over-committed: {granted} launches granted, expected exactly {n_allowed}"
    )
    # Consumed exactly the granted allocations; never more than the budget.
    assert ledger.consumed == n_allowed * minimum
    assert ledger.available() < minimum  # no room for another launch


@pytest.mark.thread_safety
def test_try_launch_admits_exactly_task_count_under_kgt1() -> None:
    """TM-12 (R-9): K>1 launch admission with a per-phase-shaped pool.

    Sizes ``initial_budget = task_count × minimum_allocation`` (the per-phase
    pool shape), then fans ``2 × task_count`` ``try_launch()`` calls across a
    ThreadPoolExecutor. The RLock-protected atomic check-and-debit admits EXACTLY
    ``task_count`` launches under contention — no over-admission.

    Asserts EXACTLY: exactly ``task_count`` ``try_launch()`` calls succeed.
    """
    task_count = 8
    minimum = 5
    ledger = TurnLedger(initial_budget=task_count * minimum, minimum_allocation=minimum)

    n_attempts = 2 * task_count  # twice the admissible count → exposes any race

    def _attempt(_i: int) -> bool:
        return ledger.try_launch()

    with ThreadPoolExecutor(max_workers=min(16, n_attempts)) as pool:
        outcomes = list(pool.map(_attempt, range(n_attempts)))

    granted = sum(1 for ok in outcomes if ok)
    assert granted == task_count, (
        f"expected exactly {task_count} launches, got {granted}"
    )
