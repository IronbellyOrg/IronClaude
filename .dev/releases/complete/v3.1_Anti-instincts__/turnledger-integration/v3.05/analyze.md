# v3.05 Deterministic Fidelity Gates -- TurnLedger Integration Analysis

**Agent**: 1A (Analyzer)
**Date**: 2026-03-20
**Spec Version**: v3.05 1.1.0
**TurnLedger Source**: `src/superclaude/cli/sprint/models.py:488-525`

---

## 1. TurnLedger Current State

### Fields and Methods

| Field/Method | Type | Purpose |
|---|---|---|
| `initial_budget` | `int` | Total turn budget allocated at sprint start |
| `consumed` | `int` | Monotonically increasing counter of debited turns |
| `reimbursed` | `int` | Credited turns (gate-pass reimbursement) |
| `reimbursement_rate` | `float` (0.8) | Fraction of turns credited back on gate pass |
| `minimum_allocation` | `int` (5) | Minimum turns required for subprocess launch |
| `minimum_remediation_budget` | `int` (3) | Minimum turns required for remediation |
| `available()` | method | `initial_budget - consumed + reimbursed` |
| `debit(turns)` | method | Consume turns; enforces non-negative |
| `credit(turns)` | method | Reimburse turns; enforces non-negative |
| `can_launch()` | method | `available() >= minimum_allocation` |
| `can_remediate()` | method | `available() >= minimum_remediation_budget` |

### Critical Gap: Reimbursement Loop Not Wired

`reimbursement_rate=0.8` is defined on TurnLedger but is **never consumed by production code**. In `executor.py`:

- `execute_phase_tasks()` calls `ledger.credit()` only for pre-allocation reconciliation (line 589: crediting back unused pre-allocated turns when `actual < pre_allocated`). This is accounting reconciliation, NOT gate-pass reimbursement.
- `execute_sprint()` uses phase-level orchestration, not the per-task loop. No reimbursement logic at all.
- The gate-pass reimbursement pattern (`pass gate -> credit(turns * reimbursement_rate)`) exists ONLY in `tests/pipeline/test_full_flow.py` (lines 102-103, 318).

### Budget Guard

`check_budget_guard()` in `executor.py:337-350` wraps `ledger.can_launch()` returning a halt message string or None. This is a pre-launch guard, not a convergence budget.

---

## 2. Concept Mapping Table

| # | v3.05 Concept | Spec Location | TurnLedger Equivalent | Gap Classification |
|---|---|---|---|---|
| 1 | **Hard budget of 3 runs** | FR-7 (G2, line 571) | `initial_budget` field | **EXTEND** -- TurnLedger counts turns (subprocess launches), not convergence runs. Need a `max_convergence_runs: int = 3` field or a separate counter. TurnLedger's `initial_budget` is denominated in turns, not fidelity-run iterations. |
| 2 | **Monotonic progress (structural HIGHs must decrease)** | FR-7 (line 647-648) | No equivalent | **NO_MATCH** -- TurnLedger tracks economic budget (turns consumed/remaining). It has no concept of directional quality metrics. Monotonic progress requires comparing `structural_high_count` across runs, which is a convergence-domain concept with no budget analog. |
| 3 | **Run counter (catch/verify/backup)** | FR-7 (lines 604-611) | `consumed` field (partial) | **EXTEND** -- `consumed` tracks total turns spent but not the number of distinct convergence runs. Need a `runs_completed: int` counter. The 3-run naming (catch/verify/backup) is semantic labeling over a simple counter. |
| 4 | **Budget exhaustion -> HALT with diagnostic** | FR-7 (line 651), US-5 | `can_launch()`, `check_budget_guard()` | **DIRECT_REPLACEMENT** -- `can_launch()` returns False when budget insufficient. `check_budget_guard()` produces a halt message. The v3.05 "budget exhausted -> halt with diagnostic report" maps directly to this pattern. The diagnostic report content differs (v3.05 lists active findings with run history; TurnLedger just reports turns), but the halt mechanism is identical. |
| 5 | **Remediation retry (up to 2 attempts per remediation)** | FR-9 (remediate_executor.py) | `attempt_remediation()` in `trailing_gate.py` | **DIRECT_REPLACEMENT** -- `attempt_remediation()` implements retry-once semantics (2 max attempts) with budget integration via `can_remediate()` and `debit()` callbacks. v3.05's remediation retry within the convergence loop maps cleanly to this existing function. |
| 6 | **Gate-pass reimbursement (credit 80% on pass)** | Not in v3.05 spec | `reimbursement_rate=0.8`, `credit()` | **NO_MATCH (reverse)** -- TurnLedger has this concept but v3.05 does NOT. The v3.05 convergence model has no reimbursement concept; runs are counted discretely (1, 2, 3) with no partial credit. This is a TurnLedger feature with no v3.05 consumer. |
| 7 | **Regression detection (structural HIGH increase)** | FR-8 (line 760) | No equivalent | **NO_MATCH** -- TurnLedger has no concept of quality regression. Regression in v3.05 means `current_run.structural_high_count > previous_run.structural_high_count`. TurnLedger's monotonicity is on `consumed` (can only increase), which is the opposite direction -- it enforces that spending never decreases, not that quality never regresses. |
| 8 | **Regression validation counts as 1 budget unit** | FR-7.1 (lines 706, 712-714) | `debit()` | **EXTEND** -- `debit()` can charge 1 unit for the regression validation. But TurnLedger has no concept of "a run that includes regression validation costs the same as a normal run." Need accounting rules that treat regression-validation + remediation as a single budget debit, not separate debits per subprocess. |
| 9 | **Dual budget system (convergence vs legacy)** | FR-7 (lines 635-643) | No equivalent | **NO_MATCH** -- TurnLedger is a single-budget model. v3.05 requires two mutually exclusive budget systems: convergence mode (3 fidelity runs) and legacy mode (2 remediation attempts). The two must never overlap. TurnLedger would need a mode discriminator to select which budget semantics apply. |
| 10 | **Convergence pass = 0 active HIGHs** | FR-7 (line 569) | `can_launch()` (structural analog only) | **NO_MATCH** -- `can_launch()` checks remaining turns, not finding counts. The v3.05 gate evaluates `registry.get_active_high_count() == 0`, which is a quality metric, not a resource metric. Completely different domain. |
| 11 | **Per-task budget debit with pre-allocation** | execute_phase_tasks (lines 557-589) | `debit()`, `credit()` | **DIRECT_REPLACEMENT** -- `execute_phase_tasks()` already debits `minimum_allocation` upfront, then reconciles after actual consumption. This per-task budget pattern works for v3.05's convergence runs if each run is treated as a "task" in the ledger. |
| 12 | **Semantic HIGH fluctuation (warning, not regression)** | FR-7 (lines 648-649) | No equivalent | **NO_MATCH** -- TurnLedger has no concept of warning-level budget events. It either debits or doesn't. The v3.05 distinction between structural regression (triggers FR-8) and semantic fluctuation (logged as warning) is a quality-domain concept. |
| 13 | **Run metadata (structural/semantic split counts)** | FR-6 (lines 542-545) | No equivalent | **NO_MATCH** -- TurnLedger tracks aggregate turns only. v3.05 requires per-run metadata with `structural_high_count`, `semantic_high_count`, `total_high_count`. This is convergence-domain state, not budget-domain state. |
| 14 | **Progress proof logging** | FR-7 (line 652) | No equivalent | **NO_MATCH** -- TurnLedger has no logging of progress proofs. v3.05 requires: `"structural: {n} -> {n+1}, semantic: {n} -> {n+1}"`. This is observability over quality metrics, not budget metrics. |
| 15 | **Convergence enabled flag** | FR-7 (line 655), models.py:107 | No equivalent on TurnLedger | **EXTEND** -- `RoadmapConfig.convergence_enabled` already exists in models.py. TurnLedger could carry a `convergence_mode: bool` to select which budget semantics apply, but the existing config field is the correct place for this. |

---

## 3. Summary by Classification

### DIRECT_REPLACEMENT (3 concepts)

These TurnLedger features can replace v3.05 concepts as-is:

1. **Budget exhaustion -> HALT** (#4): `can_launch()` + `check_budget_guard()` directly maps to v3.05's halt-on-budget-exhaustion.
2. **Remediation retry** (#5): `attempt_remediation()` in trailing_gate.py is a direct match for v3.05's remediation retry pattern.
3. **Per-task budget debit** (#11): The pre-allocate/reconcile pattern in `execute_phase_tasks()` works for convergence runs.

### EXTEND (3 concepts)

TurnLedger needs minor additions:

1. **Hard budget of 3** (#1): Add `max_convergence_runs: int = 3` field. TurnLedger currently counts turns, not convergence iterations.
2. **Run counter** (#3): Add `runs_completed: int = 0` field to track distinct convergence runs vs raw turn consumption.
3. **Regression as 1 budget unit** (#8): Add accounting rules that bundle regression-validation + remediation into a single budget debit.

### NO_MATCH (9 concepts)

These are genuinely new convergence-domain concepts with no TurnLedger analog:

1. **Monotonic progress** (#2): Quality-direction enforcement, not budget enforcement.
2. **Gate-pass reimbursement** (#6): Exists in TurnLedger but NOT in v3.05 -- the reverse gap.
3. **Regression detection** (#7): Quality regression, not budget regression.
4. **Dual budget system** (#9): Mode-switching between two mutually exclusive budget models.
5. **Convergence pass criteria** (#10): Quality metric (`active_high_count == 0`), not resource metric.
6. **Semantic fluctuation handling** (#12): Warning-level quality event, no budget analog.
7. **Run metadata with split counts** (#13): Per-run quality state, not budget state.
8. **Progress proof logging** (#14): Quality observability, not budget observability.
9. **Convergence enabled flag** (#15): Already exists on `RoadmapConfig`, not TurnLedger's concern.

---

## 4. Key Findings

### Finding 1: TurnLedger is a Resource Budget; v3.05 Needs a Quality Budget

TurnLedger tracks **resource consumption** (turns spent, turns remaining). v3.05's convergence model tracks **quality convergence** (HIGH findings decreasing across runs). These are orthogonal concerns. TurnLedger can enforce "stop after N resource units spent" but cannot enforce "stop after N quality-improvement iterations" or "quality must monotonically improve."

**Implication**: TurnLedger should not be extended to carry quality metrics. A separate `ConvergenceState` or `ConvergenceLedger` is needed for the quality dimension, with TurnLedger optionally providing resource-side guardrails.

### Finding 2: Reimbursement Rate is Orphaned Code

`reimbursement_rate=0.8` on TurnLedger is:
- Defined in production code (`models.py:499`)
- Tested extensively in test code (`test_full_flow.py`, `test_models.py`)
- **Never consumed by any production orchestration code**

The tests demonstrate the intended pattern (gate pass -> credit 80% of turns), but `execute_sprint()` and `execute_phase_tasks()` do not implement it. v3.05 also does not need it -- the convergence model uses discrete run counting, not fractional reimbursement.

**Implication**: `reimbursement_rate` is either pre-built infrastructure for a future sprint feature, or dead code. v3.05 does not activate it.

### Finding 3: `attempt_remediation()` is the Strongest Integration Point

The `attempt_remediation()` function in `trailing_gate.py` is the closest existing code to v3.05's remediation retry within the convergence loop:
- Retry-once semantics (2 max attempts)
- Budget-integrated via `can_remediate()` and `debit()` callbacks
- State machine with clear outcomes (PASS_FIRST, PASS_SECOND, PERSISTENT_FAILURE, BUDGET_EXHAUSTED)

v3.05's `execute_fidelity_with_convergence()` could delegate remediation to this function, treating each fidelity run's remediation phase as an `attempt_remediation()` call.

### Finding 4: Dual Budget System Requires Mode Isolation

v3.05 explicitly states (FR-7, lines 635-643):
- Convergence mode: 3 fidelity runs. `_check_remediation_budget()` and `_print_terminal_halt()` are NOT invoked.
- Legacy mode: 2 remediation attempts. Completely untouched by convergence mode.
- The two MUST never overlap.

TurnLedger is a single-budget model. If both systems need TurnLedger, two separate TurnLedger instances would be needed (one per mode), or TurnLedger needs a mode discriminator. The simpler path is: TurnLedger stays as the sprint-level resource budget; v3.05 uses its own `ConvergenceBudget` dataclass with `max_runs=3, runs_completed=0`.

---

## 5. Recommended Architecture

```
TurnLedger (resource budget, sprint-level)
  |
  +-- execute_phase_tasks() -- per-task subprocess budget
  |
  +-- attempt_remediation() -- retry with budget callbacks
  |
  +-- [NOT WIRED] gate-pass reimbursement loop

ConvergenceBudget (quality budget, v3.05-specific, NEW)
  |
  +-- max_runs: int = 3
  +-- runs_completed: int = 0
  +-- structural_high_counts: list[int]  # per-run
  +-- semantic_high_counts: list[int]    # per-run
  +-- can_run() -> bool  # runs_completed < max_runs
  +-- record_run(structural_highs, semantic_highs) -> None
  +-- is_monotonic() -> bool  # structural HIGHs non-increasing
  +-- is_converged() -> bool  # total HIGHs == 0
```

TurnLedger provides resource-side guardrails (don't spend infinite turns on remediation). ConvergenceBudget provides quality-side guardrails (don't run more than 3 times, enforce monotonic progress). The two are composed, not merged.
