---
title: "Agent 2A Analysis: v3.0/v3.1 Unified Audit Gating -- TurnLedger Overlap Map"
agent: 2A-Analyzer
date: 2026-03-20
status: complete
sources:
  - src/superclaude/cli/sprint/models.py (TurnLedger, lines 488-526)
  - src/superclaude/cli/sprint/executor.py (execute_phase_tasks, check_budget_guard, SprintGatePolicy, execute_sprint)
  - src/superclaude/cli/pipeline/trailing_gate.py (TrailingGateRunner, attempt_remediation, DeferredRemediationLog)
  - src/superclaude/cli/pipeline/gates.py (gate_passed)
  - src/superclaude/cli/pipeline/executor.py (execute_pipeline, _execute_single_step)
  - src/superclaude/cli/sprint/kpi.py (GateKPIReport, build_kpi_report)
  - src/superclaude/cli/roadmap/convergence.py (ConvergenceResult, DeviationRegistry)
  - tests/pipeline/test_full_flow.py (4 integration scenarios)
  - .dev/releases/complete/unified-audit-gating-v1.2.1/adversarial/brainstorm-turn-reimbursement.md
  - .dev/releases/complete/v3.0_unified-audit-gating/adversarial/merged-spec.md
  - .dev/releases/complete/v3.0_unified-audit-gating/v3.0_wiring-gate/spec.md
---

# v3.0/v3.1 Unified Audit Gating -- TurnLedger Overlap Analysis

## 1. Executive Summary

The v3.0 unified audit gating release introduced a wiring-verification gate that detects unwired code (dead callables, orphan modules, broken dispatch). This system plugs into the existing `gate_passed()` / `GateCriteria` / `SemanticCheck` substrate. The TurnLedger was designed alongside this work (brainstormed in v1.2.1, implemented in models.py) but its gate-pass reimbursement loop is **never wired into `execute_sprint()`**. The reimbursement_rate=0.8 field exists only in tests and the brainstorm doc.

There are **three distinct retry/remediation systems** operating in parallel, each with its own budget/counter semantics, creating significant overlap and integration debt.

---

## 2. Gate Evaluation Pipeline

### 2.1 `gate_passed()` -- The Universal Gate Check

**Location**: `src/superclaude/cli/pipeline/gates.py:20-74`
**Signature**: `(Path, GateCriteria) -> tuple[bool, str | None]`

Tiered validation:
- **EXEMPT**: always passes
- **LIGHT**: file exists + non-empty
- **STANDARD**: + min lines + YAML frontmatter fields
- **STRICT**: + semantic checks (`Callable[[str], bool]`)

This is the single point of gate evaluation. Both the pipeline executor and trailing gate runner funnel through it. It is pure Python, no subprocess, no LLM -- deterministic file content validation.

### 2.2 Pipeline Executor Retry (Generic)

**Location**: `src/superclaude/cli/pipeline/executor.py:174-294`

The generic pipeline executor (`execute_pipeline`) handles steps with a built-in retry loop:
- `retry_limit` field on `Step` (default=1, meaning 2 total attempts)
- On gate failure, re-runs `run_step()` up to `max_attempts = retry_limit + 1`
- No budget tracking -- retry cost is invisible
- Gate mode branching: BLOCKING (sync check) vs TRAILING (async submit to `TrailingGateRunner`)
- Deferred TRAILING steps execute even after pipeline halt (lines 124-156)

**Budget blind spot**: The pipeline executor has zero awareness of TurnLedger. Every retry consumes real subprocess turns that are never accounted for.

### 2.3 Sprint Executor -- Per-Task Orchestration

**Location**: `src/superclaude/cli/sprint/executor.py:506-606`

`execute_phase_tasks()` is the sprint-specific task loop. It does integrate TurnLedger:
- Pre-launch budget guard: `ledger.can_launch()` check (line 542)
- Pre-debit `minimum_allocation` turns upfront (line 558)
- Post-task reconciliation: adjusts for actual vs pre-allocated turns (lines 582-589)
- Budget exhaustion marks remaining tasks as SKIPPED

**Critical gap**: `execute_sprint()` (line 651) -- the main orchestration loop -- does NOT instantiate or pass a TurnLedger. It calls `ClaudeProcess` directly per-phase, not `execute_phase_tasks()`. The TurnLedger-aware path is only exercised through `execute_phase_tasks()` which is called by consumers who explicitly pass a ledger.

### 2.4 Wiring Gate Hook (v3.0 Addition)

**Location**: `src/superclaude/cli/sprint/executor.py:418-503`

`run_post_task_wiring_hook()` runs after each task in `execute_phase_tasks()`. Modes:
- **off**: skip entirely
- **shadow**: log findings, no status change (SC-006)
- **soft**: warn on critical, no status change
- **full**: block on critical+major, mark FAIL

This is a post-task gate that operates independently of the pipeline's gate_passed() system. It uses `WiringReport` from the audit subsystem rather than `GateCriteria`.

---

## 3. Retry/Remediation Mechanisms

### 3.1 Pipeline Executor Retry

| Property | Value |
|----------|-------|
| Location | `pipeline/executor.py:192` |
| Max attempts | `step.retry_limit + 1` (default: 2) |
| Budget awareness | None |
| Gate check | `gate_passed()` synchronous |
| Scope | Per-step, generic |

### 3.2 Trailing Gate Remediation (`attempt_remediation`)

| Property | Value |
|----------|-------|
| Location | `pipeline/trailing_gate.py:354-449` |
| Max attempts | 2 (hardcoded) |
| Budget awareness | Accepts `can_remediate()` and `debit()` callables |
| Gate check | Consumer-injected `check_gate` callable |
| Scope | Per-gate-failure, sprint-specific |
| Status enum | `RemediationRetryStatus` (PASS_FIRST/PASS_SECOND/PERSISTENT_FAILURE/BUDGET_EXHAUSTED) |

This is the only retry mechanism that integrates with TurnLedger -- but via injected callables, not direct coupling.

### 3.3 SprintGatePolicy

| Property | Value |
|----------|-------|
| Location | `sprint/executor.py:54-97` |
| Purpose | Build remediation steps from gate failures |
| Status | **Defined but never instantiated** in production code |
| Called by | Nothing in src/ -- only tests |

`SprintGatePolicy` implements the `TrailingGatePolicy` protocol but is a dead symbol. The v3.0 spec explicitly identified this as a known unwired component.

### 3.4 Convergence Engine (Roadmap-Specific)

| Property | Value |
|----------|-------|
| Location | `roadmap/convergence.py` |
| Purpose | Multi-run spec-fidelity gate with regression detection |
| Budget awareness | None (run-count based, not turn-count based) |
| Gate model | `DeviationRegistry` with stable finding IDs, structural vs semantic HIGH tracking |
| Halt condition | Structural regression (FR-8): structural HIGHs increased between runs |

The convergence engine is a completely separate retry/convergence system from TurnLedger. It uses:
- Run numbering (not turn counting)
- File-backed `DeviationRegistry` (not in-memory ledger)
- Structural/semantic split tracking (BF-3)
- No concept of reimbursement or budget

---

## 4. The Reimbursement Gap

### 4.1 Design Intent (from brainstorm doc)

The brainstorm (`unified-audit-gating-v1.2.1/adversarial/brainstorm-turn-reimbursement.md`) specified:

```
Transaction flow:
5. TRAILING GATE:  audit(output) -> PASS or FAIL
6. REIMBURSE:      if PASS: ledger.credit(actual_turns)
                   if FAIL: no credit (turns permanently spent)
```

The reimbursement_rate (0.8-0.9) creates "natural budget decay" -- even perfect phases drain the budget slowly, making infinite runs mathematically impossible.

### 4.2 What Was Implemented

- `TurnLedger.reimbursement_rate = 0.8` -- field exists (models.py:499)
- `TurnLedger.credit(turns)` -- method exists, adds to `reimbursed` counter
- `TurnLedger.can_remediate()` -- budget guard for remediation exists

### 4.3 What Is NOT Wired

- **`execute_sprint()` does not create a TurnLedger** -- the main loop has no budget tracking at all
- **`execute_phase_tasks()` never calls `ledger.credit()` based on gate pass** -- it only debits and reconciles pre-allocation vs actual consumption (lines 582-589), which is accounting correction, not reimbursement
- **The gate-pass reimbursement loop exists only in tests** -- `test_full_flow.py` manually calls `ledger.credit(int(10 * ledger.reimbursement_rate))` in test code (lines 102-103, 318), demonstrating the design but not testing actual production wiring
- **`attempt_remediation()` debits but never credits** -- even when remediation passes, no reimbursement occurs

### 4.4 Consequence

The TurnLedger is a pure debit instrument in production. The revolving-credit economic model that motivated its design is entirely unwired. Budget exhaustion happens faster than intended because successful work earns nothing back.

---

## 5. Overlap Map: What TurnLedger Could Subsume

### 5.1 Direct Overlaps

| Existing Mechanism | TurnLedger Equivalent | Integration Path |
|---|---|---|
| `Step.retry_limit` (pipeline executor) | `TurnLedger.can_remediate()` + `attempt_remediation()` | Replace fixed retry count with budget-gated retry |
| `AggregatedPhaseReport.budget_remaining` | `TurnLedger.available()` | Already uses ledger when passed; wire into execute_sprint |
| `RemediationRetryStatus.BUDGET_EXHAUSTED` | `TurnLedger.can_remediate() == False` | Already connected via callable injection |
| Manual accounting in `execute_phase_tasks` (lines 582-589) | `TurnLedger.debit(actual) + TurnLedger.credit(reimbursement)` | Add reimbursement call after gate pass |

### 5.2 Parallel Systems (No Overlap, Different Domain)

| System | Domain | Why It Does Not Overlap |
|---|---|---|
| Convergence Engine (`roadmap/convergence.py`) | Multi-run fidelity | Tracks run-to-run finding regression, not turn budgets |
| Wiring Gate Hook (`run_post_task_wiring_hook`) | Code-integrity gate | Binary pass/fail on code analysis, no retry budget |
| `DeferredRemediationLog` | Failure persistence | Logging layer, not decision layer |

### 5.3 Custom Budget Tracking Outside TurnLedger

The following budget/counter patterns exist independently of TurnLedger:

1. **`AggregatedPhaseReport.total_turns_consumed`** (executor.py:206) -- aggregated from TaskResult, duplicates what ledger.consumed tracks
2. **`AggregatedPhaseReport.budget_remaining`** (executor.py:205) -- set from ledger.available() when present, but zero otherwise
3. **`PhaseResult.output_bytes`** / `MonitorState.output_bytes` -- size-based tracking, orthogonal to turn budget
4. **`Step.retry_limit`** -- fixed integer, not budget-aware

---

## 6. Key Finding: The Reimbursement Integration Point

The single highest-value integration is wiring the reimbursement loop into `execute_phase_tasks()`. The change is small:

**Current** (lines 573-589): Only reconciles pre-allocation vs actual.
**Required**: After gate evaluation (which already happens via `run_post_task_wiring_hook` at line 602), if the task passed, call:
```python
if status == TaskStatus.PASS and ledger is not None:
    reimbursement = int(turns_consumed * ledger.reimbursement_rate)
    ledger.credit(reimbursement)
```

**Upstream dependency**: `execute_sprint()` must instantiate a `TurnLedger` and pass it to the phase loop. Currently it does not.

---

## 7. Summary of Findings

| # | Finding | Severity |
|---|---------|----------|
| F-1 | `reimbursement_rate=0.8` field is never consumed by production code | HIGH -- core economic model unwired |
| F-2 | `execute_sprint()` does not instantiate TurnLedger | HIGH -- main loop has no budget tracking |
| F-3 | `SprintGatePolicy` is defined but never instantiated | MEDIUM -- dead code, known in v3.0 spec |
| F-4 | Pipeline executor retry (`Step.retry_limit`) has no budget awareness | MEDIUM -- retries are free, violating economic model |
| F-5 | Three separate retry/remediation systems with no unified budget | MEDIUM -- architectural fragmentation |
| F-6 | `attempt_remediation()` debits but never credits on success | LOW -- by design (only original task earns reimbursement per brainstorm), but undocumented |
| F-7 | Convergence engine is a separate system with no TurnLedger overlap | INFO -- no integration needed |
| F-8 | `GateKPIReport` tracks gate metrics but not budget impact | LOW -- observability gap |
