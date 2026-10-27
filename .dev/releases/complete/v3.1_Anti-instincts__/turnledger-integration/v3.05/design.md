---
title: "TurnLedger Integration Design for v3.05 Convergence Engine"
status: draft
created: 2026-03-20
agent: 1C (Architect/Designer)
relates_to:
  - src/superclaude/cli/sprint/models.py (TurnLedger, lines 488-525)
  - src/superclaude/cli/roadmap/convergence.py (DeviationRegistry, ConvergenceResult)
  - src/superclaude/cli/roadmap/executor.py (_check_remediation_budget, _print_terminal_halt)
  - src/superclaude/cli/pipeline/trailing_gate.py (attempt_remediation)
key_finding: "TurnLedger.reimbursement_rate=0.8 is defined but NEVER consumed by production code"
---

# TurnLedger Integration Design for `execute_fidelity_with_convergence()`

## 1. Constructor Signature

```python
def execute_fidelity_with_convergence(
    config: RoadmapConfig,
    registry: DeviationRegistry,
    spec_path: Path,
    roadmap_path: Path,
    output_dir: Path,
    ledger: TurnLedger,
    *,
    run_checkers: Callable[[Path, Path], tuple[list[Finding], list[Finding]]] | None = None,
    run_remediation: Callable[[list[Finding], RoadmapConfig], dict] | None = None,
    handle_regression_fn: Callable[..., RegressionResult] | None = None,
) -> ConvergenceResult:
    """Orchestrate up to 3 fidelity runs within step 8 of the pipeline.

    The TurnLedger provides budget enforcement for the convergence loop,
    replacing the legacy _check_remediation_budget() 2-attempt state file
    mechanism with an in-memory economic model.

    Args:
        config: Roadmap pipeline configuration (convergence_enabled must be True).
        registry: Active DeviationRegistry for this release.
        spec_path: Path to the spec document.
        roadmap_path: Path to the merged roadmap.
        output_dir: Pipeline output directory.
        ledger: TurnLedger instance governing budget for all fidelity runs
            and intra-loop remediation. The caller (pipeline executor) constructs
            this with initial_budget calibrated to the convergence workload.
        run_checkers: Optional injectable checker suite (default: real structural +
            semantic checkers). Signature: (spec, roadmap) -> (structural, semantic).
        run_remediation: Optional injectable remediation executor (default:
            execute_remediation from remediate_executor.py).
        handle_regression_fn: Optional injectable regression handler (default:
            handle_regression from convergence.py). Enables testing without
            spawning real parallel agents.

    Returns:
        ConvergenceResult with pass/fail, run count, and diagnostic logs.
    """
```

### Why TurnLedger as parameter (not internally constructed)

The convergence engine operates _within_ step 8 of the pipeline. The pipeline
executor owns the overall budget and passes a pre-allocated TurnLedger slice
to the convergence engine. This preserves the existing ownership pattern where
`execute_phase_tasks()` in `sprint/executor.py` owns the ledger and passes it
to subtask orchestrators.

The convergence engine does not construct its own TurnLedger because:
1. The pipeline may have consumed budget in steps 1-7 already.
2. The caller may want to reserve budget for step 9 (certification).
3. Budget isolation (FR-7: convergence budget vs legacy budget) is enforced
   by the caller choosing whether to pass a ledger at all.

---

## 2. Debit/Credit Points Within the Convergence Loop

The convergence loop has 5 distinct budget-consuming operations across up to
3 runs. Each operation maps to a `ledger.debit()` or `ledger.credit()` call.

### 2.1 Run Flow with Debit/Credit Annotations

```
execute_fidelity_with_convergence(ledger):
    for run_number in [1, 2, 3]:

        # ---- PRE-CHECK ----
        if not ledger.can_launch():                    # (A) Budget guard
            return ConvergenceResult(passed=False,
                halt_reason="convergence_budget_exhausted")

        # ---- RUN N: Checker Suite ----
        ledger.debit(CHECKER_COST)                     # (B) Debit: checker suite
        structural, semantic = run_checkers(spec, roadmap)
        registry.merge_findings(structural, semantic, run_number)
        registry.save()

        # ---- GATE CHECK ----
        if registry.get_active_high_count() == 0:
            ledger.credit(CONVERGENCE_PASS_CREDIT)     # (C) Credit: early exit
            return ConvergenceResult(passed=True, run_count=run_number)

        # ---- REGRESSION CHECK (Run 2+) ----
        if run_number > 1 and _check_regression(registry):
            ledger.debit(REGRESSION_VALIDATION_COST)   # (D) Debit: FR-8 parallel validation
            regression_result = handle_regression(...)
            # Regression validation + remediation = 1 budget unit (FR-7.1)
            # No separate debit for post-regression remediation

        # ---- REMEDIATION (between runs) ----
        if run_number < 3:                             # No remediation after final run
            if not ledger.can_remediate():              # (E) Budget guard
                return ConvergenceResult(passed=False,
                    halt_reason="remediation_budget_exhausted")
            ledger.debit(REMEDIATION_COST)             # (F) Debit: remediation
            run_remediation(registry.get_active_highs(), config)

    # ---- BUDGET EXHAUSTED ----
    return ConvergenceResult(passed=False, run_count=3,
        halt_reason="max_runs_exhausted")
```

### 2.2 Debit/Credit Summary Table

| Point | Operation | Ledger Call | Cost Constant | When |
|-------|-----------|-------------|---------------|------|
| (A) | Pre-run budget guard | `ledger.can_launch()` | `minimum_allocation` | Before each run |
| (B) | Checker suite execution | `ledger.debit(CHECKER_COST)` | Configurable, ~10 turns | Each run |
| (C) | Early convergence pass | `ledger.credit(CONVERGENCE_PASS_CREDIT)` | Partial refund of unused budget | When 0 HIGHs before max runs |
| (D) | Regression validation (FR-8) | `ledger.debit(REGRESSION_VALIDATION_COST)` | ~15 turns (3 parallel agents) | When structural regression detected |
| (E) | Pre-remediation budget guard | `ledger.can_remediate()` | `minimum_remediation_budget` | Before remediation |
| (F) | Intra-loop remediation | `ledger.debit(REMEDIATION_COST)` | Configurable, ~8 turns | Between runs 1-2, 2-3 |

### 2.3 Concrete Walk-Through: 3-Run Sequence

```
Initial state: ledger = TurnLedger(initial_budget=60)

Run 1 (catch):
  ledger.debit(10)           # Checker suite            consumed=10, available=50
  3 HIGHs found -> no pass
  ledger.debit(8)            # Remediation              consumed=18, available=42

Run 2 (verify):
  ledger.debit(10)           # Checker suite            consumed=28, available=32
  1 HIGH found (structural regression!) -> regression detected
  ledger.debit(15)           # FR-8 parallel validation  consumed=43, available=17
  0 HIGHs after debate downgrades -> PASS
  ledger.credit(5)           # Early exit credit         consumed=43, reimbursed=5, available=22

Result: ConvergenceResult(passed=True, run_count=2)
```

---

## 3. Reimbursement Rate Semantics

### 3.1 Current State: Dead Code

The `reimbursement_rate=0.8` field on TurnLedger (models.py:499) is **never
consumed by any production code path**. Evidence:

- `reimbursement_rate` is defined as a field with default `0.8`.
- The only consumer is `test_full_flow.py` (test code), where tests manually
  compute `int(10 * ledger.reimbursement_rate)` and call `ledger.credit()`.
- No production code in `executor.py`, `trailing_gate.py`, or any other module
  reads `ledger.reimbursement_rate`.
- The `credit()` method accepts raw turn counts -- it does not reference
  `reimbursement_rate` internally.

### 3.2 Proposed Convergence Semantics

For the convergence engine, `reimbursement_rate` maps to **convergence
progress credit**: when a run demonstrates forward progress (fewer structural
HIGHs than the previous run), the engine credits back a fraction of the run's
cost as a reward for convergence.

```python
# Inside the convergence loop, after monotonic progress confirmed:
if run_number > 1 and not regression_detected:
    prev_highs = registry.runs[-2].get("structural_high_count", 0)
    curr_highs = registry.runs[-1].get("structural_high_count", 0)
    if curr_highs < prev_highs:
        # Partial credit for forward progress
        run_cost = CHECKER_COST  # cost of this run's checker suite
        credit = int(run_cost * ledger.reimbursement_rate)
        ledger.credit(credit)
        result.structural_progress_log.append(
            f"Run {run_number}: progress credit {credit} turns "
            f"(structural {prev_highs} -> {curr_highs})"
        )
```

**Semantic mapping:**

| Scenario | Reimbursement | Rationale |
|----------|--------------|-----------|
| Run converges to 0 HIGHs (PASS) | `credit(CONVERGENCE_PASS_CREDIT)` | Full early-exit credit; unused runs refunded |
| Run shows forward progress (fewer structural HIGHs) | `credit(int(CHECKER_COST * reimbursement_rate))` | Partial credit; convergence is working |
| Run stalls (same HIGH count) | No credit | No forward progress; budget consumed |
| Run regresses (more structural HIGHs) | No credit + extra debit for FR-8 | Regression costs more than neutral |

**Key design choice:** Successful run = **partial credit** (not no credit).
The reimbursement rate acts as a convergence incentive -- progress is cheaper
than stalling. This is analogous to the sprint executor pattern where
`execute_phase_tasks()` credits back the difference between pre-allocated and
actual turns consumed (executor.py:587-589).

### 3.3 Explicit `reimburse_for_progress()` Helper

Rather than scattering credit logic, a helper method encapsulates the policy:

```python
def reimburse_for_progress(
    ledger: TurnLedger,
    run_cost: int,
    prev_structural_highs: int,
    curr_structural_highs: int,
) -> int:
    """Credit partial refund when convergence shows forward progress.

    Returns the number of turns credited (0 if no progress).
    Uses ledger.reimbursement_rate as the credit fraction.
    """
    if curr_structural_highs >= prev_structural_highs:
        return 0
    credit = int(run_cost * ledger.reimbursement_rate)
    if credit > 0:
        ledger.credit(credit)
    return credit
```

This gives `reimbursement_rate` its first production consumer and aligns
its semantics with the convergence domain.

---

## 4. Legacy Budget Mapping

### 4.1 Legacy System: `_check_remediation_budget()`

The existing roadmap executor uses a state-file-based budget system
(executor.py:786-830):

```
_check_remediation_budget(output_dir, max_attempts=2):
    reads .roadmap-state.json -> remediation_attempts
    if attempts >= 2: _print_terminal_halt() -> return False
    return True
```

**Properties:**
- Budget: 2 remediation attempts (hard-coded default)
- State: persisted in `.roadmap-state.json` (survives process restarts)
- Granularity: counts whole remediation cycles, not turns
- Enforcement: called before each remediation cycle in the pipeline loop
- Halt mechanism: `_print_terminal_halt()` writes diagnostic and exits

### 4.2 TurnLedger Equivalent

| Legacy Concept | TurnLedger Equivalent | Notes |
|----------------|----------------------|-------|
| `max_attempts=2` | `initial_budget` calibrated for 2 remediation cycles | e.g., `initial_budget = 2 * REMEDIATION_COST` |
| `remediation_attempts` counter | `ledger.consumed` (derived) | Implicit from debit history |
| `.roadmap-state.json` persistence | TurnLedger is in-memory only | Convergence runs are single-process; no resume needed |
| `_print_terminal_halt()` | `ConvergenceResult(halt_reason=...)` | Structured return instead of side-effect print |
| `attempts >= max_attempts` | `not ledger.can_remediate()` | Uses `minimum_remediation_budget` threshold |

### 4.3 Budget Calibration for Different `initial_budget` Values

The convergence engine's 3-run budget maps to TurnLedger as follows:

```python
# Minimum viable convergence budget (catch + verify, no regression):
MIN_CONVERGENCE_BUDGET = (
    CHECKER_COST * 2          # 2 checker suite runs
    + REMEDIATION_COST * 1    # 1 remediation cycle
)  # ~28 turns

# Standard convergence budget (catch + verify + backup):
STD_CONVERGENCE_BUDGET = (
    CHECKER_COST * 3          # 3 checker suite runs
    + REMEDIATION_COST * 2    # 2 remediation cycles
)  # ~46 turns

# Maximum convergence budget (with regression validation):
MAX_CONVERGENCE_BUDGET = (
    CHECKER_COST * 3
    + REMEDIATION_COST * 2
    + REGRESSION_VALIDATION_COST  # FR-8 parallel agents
)  # ~61 turns
```

The pipeline executor constructs the TurnLedger with the appropriate budget:

```python
# In roadmap/executor.py, when convergence_enabled=True:
convergence_ledger = TurnLedger(
    initial_budget=MAX_CONVERGENCE_BUDGET,
    minimum_allocation=CHECKER_COST,
    minimum_remediation_budget=REMEDIATION_COST,
    reimbursement_rate=0.8,
)
```

### 4.4 Budget Isolation Guarantee (FR-7)

The two budget systems MUST never overlap:

```python
# In the pipeline step 8 dispatch:
if config.convergence_enabled:
    # Convergence mode: TurnLedger governs budget
    # _check_remediation_budget() is NEVER called
    result = execute_fidelity_with_convergence(
        config=config,
        registry=registry,
        ledger=convergence_ledger,
        ...
    )
else:
    # Legacy mode: state-file budget governs
    # TurnLedger is NEVER constructed
    if _check_remediation_budget(output_dir):
        execute_remediation(...)
```

---

## 5. Migration Path: Adopting TurnLedger Without Breaking Legacy

### 5.1 Strategy: Additive, Behind Feature Flag

The migration is gated entirely behind `config.convergence_enabled` (already
exists in `RoadmapConfig`, models.py:107). No code path changes when
`convergence_enabled=False`.

### 5.2 Phase 1: Internal Adoption (No Public API Change)

```python
# convergence.py -- new function, does not modify any existing function

def execute_fidelity_with_convergence(
    config: RoadmapConfig,
    registry: DeviationRegistry,
    spec_path: Path,
    roadmap_path: Path,
    output_dir: Path,
    ledger: TurnLedger,
    **kwargs,
) -> ConvergenceResult:
    """New function. Does not replace or modify any existing function."""
    ...
```

**What changes:**
- `convergence.py` gains one new top-level function and one helper
  (`reimburse_for_progress`)
- `convergence.py` adds import: `from superclaude.cli.sprint.models import TurnLedger`
- `executor.py` step 8 dispatch adds the `convergence_enabled` branch
  (already partially wired: line 521 sets `gate=None` for convergence mode)

**What does NOT change:**
- `_check_remediation_budget()` -- untouched, still used in legacy mode
- `_print_terminal_halt()` -- untouched
- `DeviationRegistry` -- no modification needed
- `ConvergenceResult` -- no modification needed
- `_check_regression()` -- no modification needed (called within new function)
- `attempt_remediation()` in trailing_gate.py -- not consumed by convergence
  (convergence uses `execute_remediation()` from `remediate_executor.py`)
- All existing tests -- no behavioral change

### 5.3 Phase 2: Wire Into Pipeline Executor

```python
# executor.py -- in the step execution loop, step 8 handling:

if step.id == "spec-fidelity" and config.convergence_enabled:
    from .convergence import execute_fidelity_with_convergence
    from superclaude.cli.sprint.models import TurnLedger

    convergence_ledger = TurnLedger(
        initial_budget=MAX_CONVERGENCE_BUDGET,
        minimum_allocation=CHECKER_COST,
        minimum_remediation_budget=REMEDIATION_COST,
        reimbursement_rate=0.8,
    )
    convergence_result = execute_fidelity_with_convergence(
        config=config,
        registry=registry,
        spec_path=config.spec_file,
        roadmap_path=merge_file,
        output_dir=out,
        ledger=convergence_ledger,
    )
    # Map convergence result to StepResult for pipeline
    step_result = StepResult(
        step=step,
        status=StepStatus.PASS if convergence_result.passed else StepStatus.FAIL,
        started_at=...,
        finished_at=...,
    )
    # Skip normal step execution; convergence engine handled everything
    continue
```

### 5.4 Import Boundary

TurnLedger lives in `superclaude.cli.sprint.models`. Importing it into
`superclaude.cli.roadmap.convergence` crosses the sprint/roadmap boundary.

**Acceptable because:**
1. TurnLedger is a pure data class with no sprint-specific dependencies
2. The import is conditional (only when convergence_enabled)
3. The trailing_gate module already imports from pipeline (not sprint-specific)
4. Long-term, TurnLedger should migrate to `superclaude.cli.pipeline.models`
   as a shared economic primitive

**Future cleanup (out of scope for v3.05):**
Move `TurnLedger` to `superclaude.cli.pipeline.models` alongside `Step`,
`StepResult`, `GateCriteria`, and other shared pipeline primitives. This
makes the cross-module import clean and establishes TurnLedger as pipeline
infrastructure rather than sprint-specific.

### 5.5 Backward Compatibility Checklist

| Concern | Mitigation | Verification |
|---------|-----------|--------------|
| Legacy mode behavior unchanged | `convergence_enabled=False` (default) skips all new code | Existing integration tests pass without modification |
| `_check_remediation_budget()` still works | Function untouched; called only when `convergence_enabled=False` | Unit test for legacy budget path |
| TurnLedger not required by legacy callers | Ledger constructed only inside convergence branch | No new required parameters on existing public functions |
| State file `.roadmap-state.json` unaffected | Convergence mode does not read or write state file | Legacy state management tests pass |
| `reimbursement_rate` field backward-compatible | Default 0.8 preserved; field already existed | Existing TurnLedger tests pass |
| DeviationRegistry serialization unchanged | No new fields on registry; convergence status flows through ConvergenceResult | Registry load/save round-trip tests |

---

## 6. Cost Constants (Recommended Defaults)

```python
# convergence.py module-level constants
CHECKER_COST: int = 10        # Turns per checker suite run (structural + semantic)
REMEDIATION_COST: int = 8     # Turns per remediation cycle
REGRESSION_VALIDATION_COST: int = 15  # Turns for FR-8 (3 parallel agents + debate)
CONVERGENCE_PASS_CREDIT: int = 5      # Turns credited on early convergence pass

# Derived budgets
MIN_CONVERGENCE_BUDGET: int = CHECKER_COST * 2 + REMEDIATION_COST      # 28
STD_CONVERGENCE_BUDGET: int = CHECKER_COST * 3 + REMEDIATION_COST * 2  # 46
MAX_CONVERGENCE_BUDGET: int = STD_CONVERGENCE_BUDGET + REGRESSION_VALIDATION_COST  # 61
```

These are calibration constants, not hard limits. The pipeline executor
may override via `TurnLedger(initial_budget=N)` based on operational
requirements.
