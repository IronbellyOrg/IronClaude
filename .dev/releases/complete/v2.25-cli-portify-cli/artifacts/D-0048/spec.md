# D-0048: ConvergenceLoop State Machine — Implementation Spec

## Task

T08.01 — Implement Convergence State Machine in review.py (R-052)

## Deliverable

`src/superclaude/cli/cli_portify/convergence.py` — `ConvergenceEngine` class implementing the convergence state machine.

## Implementation

**File:** `src/superclaude/cli/cli_portify/convergence.py`

### States

- `ConvergenceState.RUNNING` — initial state; iterations may be submitted
- `ConvergenceState.CONVERGED` — terminal; zero unaddressed CRITICALs achieved
- `ConvergenceState.ESCALATED` — terminal; max iterations reached, budget exhausted, or user rejected

### Key Classes

- `ConvergenceEngine(max_iterations=3, budget_guard=None)` — main state machine
- `IterationResult(iteration, unaddressed_criticals, quality_scores)` — per-iteration data
- `ConvergenceResult(state, iterations_completed, escalation_reason)` — final result summary
- `EscalationReason` enum: `MAX_ITERATIONS`, `BUDGET_EXHAUSTED`, `USER_REJECTED`
- `SimpleBudgetGuard(total_budget, per_iteration_cost, spent)` — optional budget tracking

### State Transitions

1. `submit(IterationResult)` → if `unaddressed_criticals == 0` → `CONVERGED`
2. `submit(IterationResult)` → if `iteration >= max_iterations` → `ESCALATED (MAX_ITERATIONS)`
3. `escalate_budget()` → `ESCALATED (BUDGET_EXHAUSTED)`
4. `escalate_user()` → `ESCALATED (USER_REJECTED)`
5. `submit()` after terminal → raises `RuntimeError("terminal state")`

## Verification

```
uv run pytest tests/cli_portify/test_convergence.py -v
```

**Result:** 19/19 passed
