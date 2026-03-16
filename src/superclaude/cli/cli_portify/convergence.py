"""Standalone convergence engine for the CLI Portify panel-review step.

Implements:
- ConvergenceState enum (RUNNING, CONVERGED, ESCALATED)
- EscalationReason enum (MAX_ITERATIONS, BUDGET_EXHAUSTED, USER_REJECTED)
- IterationResult dataclass with quality score aggregation
- SimpleBudgetGuard for optional budget tracking
- ConvergenceEngine state machine
- ConvergenceResult summary dataclass
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class ConvergenceState(Enum):
    """State of the convergence engine."""

    RUNNING = "RUNNING"
    CONVERGED = "CONVERGED"
    ESCALATED = "ESCALATED"


class EscalationReason(Enum):
    """Reason the convergence loop was escalated."""

    MAX_ITERATIONS = "max_iterations"
    BUDGET_EXHAUSTED = "budget_exhausted"
    USER_REJECTED = "user_rejected"


# ---------------------------------------------------------------------------
# IterationResult
# ---------------------------------------------------------------------------


@dataclass
class IterationResult:
    """Result of a single convergence iteration.

    Attributes:
        iteration: The 1-based iteration index.
        unaddressed_criticals: Count of unaddressed CRITICAL findings.
        quality_scores: Dict of {dimension: score} for clarity, completeness,
                        testability, consistency. Missing dimensions default to 0.
    """

    iteration: int = 0
    unaddressed_criticals: int = 0
    quality_scores: dict[str, float] = field(default_factory=dict)

    _DIMENSIONS: tuple[str, ...] = field(
        default=("clarity", "completeness", "testability", "consistency"),
        init=False,
        repr=False,
        compare=False,
    )

    @property
    def overall_score(self) -> float:
        """Compute the mean of the 4 quality dimensions (missing = 0)."""
        total = sum(self.quality_scores.get(d, 0.0) for d in self._DIMENSIONS)
        return total / 4.0


# ---------------------------------------------------------------------------
# SimpleBudgetGuard
# ---------------------------------------------------------------------------


@dataclass
class SimpleBudgetGuard:
    """Optional budget guard for the convergence engine.

    Tracks spending and determines whether there is enough budget for
    another iteration.
    """

    total_budget: float = 0.0
    per_iteration_cost: float = 0.0
    spent: float = 0.0

    def has_budget(self, required: float) -> bool:
        """Return True if remaining budget >= required."""
        return self.remaining_budget() >= required

    def remaining_budget(self) -> float:
        """Return the remaining budget."""
        return max(0.0, self.total_budget - self.spent)

    def record_spend(self, amount: float) -> None:
        """Record spending."""
        self.spent += amount


# ---------------------------------------------------------------------------
# ConvergenceResult
# ---------------------------------------------------------------------------


@dataclass
class ConvergenceResult:
    """Summary of a completed convergence run."""

    state: ConvergenceState = ConvergenceState.RUNNING
    iterations_completed: int = 0
    escalation_reason: Optional[EscalationReason] = None
    quality_scores: dict[str, float] = field(default_factory=dict)

    _DIMENSIONS: tuple[str, ...] = field(
        default=("clarity", "completeness", "testability", "consistency"),
        init=False,
        repr=False,
        compare=False,
    )

    @property
    def overall_score(self) -> float:
        """Compute mean of the 4 quality dimensions (missing = 0)."""
        total = sum(self.quality_scores.get(d, 0.0) for d in self._DIMENSIONS)
        return total / 4.0

    @property
    def is_converged(self) -> bool:
        return self.state == ConvergenceState.CONVERGED

    @property
    def is_escalated(self) -> bool:
        return self.state == ConvergenceState.ESCALATED


# ---------------------------------------------------------------------------
# ConvergenceEngine
# ---------------------------------------------------------------------------


class ConvergenceEngine:
    """State machine for the panel-review convergence loop (FR-030–FR-033).

    Usage::

        engine = ConvergenceEngine(max_iterations=3)
        for i in range(1, 4):
            result = IterationResult(iteration=i, unaddressed_criticals=count)
            state = engine.submit(result)
            if engine.is_done:
                break
        final = engine.result()

    States:
        RUNNING  → initial state; iterations may be submitted.
        CONVERGED → terminal; zero unaddressed CRITICALs achieved.
        ESCALATED → terminal; max iterations reached or budget/user escalation.
    """

    def __init__(
        self,
        max_iterations: int = 3,
        budget_guard: Optional[SimpleBudgetGuard] = None,
    ) -> None:
        self._max_iterations = max_iterations
        self._budget_guard = budget_guard
        self._state: ConvergenceState = ConvergenceState.RUNNING
        self._current_iteration: int = 0
        self._escalation_reason: Optional[EscalationReason] = None
        self._last_quality_scores: dict[str, float] = {}

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def state(self) -> ConvergenceState:
        return self._state

    @property
    def is_done(self) -> bool:
        return self._state != ConvergenceState.RUNNING

    @property
    def current_iteration(self) -> int:
        return self._current_iteration

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------

    def submit(self, iteration_result: IterationResult) -> ConvergenceState:
        """Submit the result of one iteration and advance the state machine.

        Args:
            iteration_result: Populated IterationResult for this iteration.

        Returns:
            The new ConvergenceState after evaluating the result.

        Raises:
            RuntimeError: If called when the engine is already in a terminal state.
        """
        if self.is_done:
            raise RuntimeError(
                f"Cannot submit to engine in terminal state {self._state.value}"
            )

        self._current_iteration = iteration_result.iteration
        self._last_quality_scores = dict(iteration_result.quality_scores)

        # CONVERGED: zero unaddressed CRITICALs
        if iteration_result.unaddressed_criticals == 0:
            self._state = ConvergenceState.CONVERGED
            return self._state

        # ESCALATED: max iterations exhausted
        if self._current_iteration >= self._max_iterations:
            self._state = ConvergenceState.ESCALATED
            self._escalation_reason = EscalationReason.MAX_ITERATIONS
            return self._state

        # Continue running
        return self._state

    def check_budget(self, required: float) -> bool:
        """Return True if budget guard allows the given spend (or if no guard)."""
        if self._budget_guard is None:
            return True
        return self._budget_guard.has_budget(required)

    def escalate_budget(self) -> None:
        """Force ESCALATED state due to budget exhaustion."""
        self._state = ConvergenceState.ESCALATED
        self._escalation_reason = EscalationReason.BUDGET_EXHAUSTED

    def escalate_user(self) -> None:
        """Force ESCALATED state due to user rejection."""
        self._state = ConvergenceState.ESCALATED
        self._escalation_reason = EscalationReason.USER_REJECTED

    def result(self) -> ConvergenceResult:
        """Return the final convergence result.

        Should be called after the engine is done (is_done == True).
        """
        return ConvergenceResult(
            state=self._state,
            iterations_completed=self._current_iteration,
            escalation_reason=self._escalation_reason,
            quality_scores=dict(self._last_quality_scores),
        )
