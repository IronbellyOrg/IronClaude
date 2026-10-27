---
title: "TurnLedger Integration — Cross-Release Summary"
date: 2026-03-20
releases: [v3.05, v3.1, v3.2]
agents: [1A, 1B, 1C, 2A, 2B, 2C, 3A, 3B, 3C]
status: complete
---

# TurnLedger Integration — Cross-Release Summary

## 1. Universal Finding: `reimbursement_rate=0.8` Is Dead Code

All 9 agents independently confirmed: `TurnLedger.reimbursement_rate=0.8` (models.py:499) is defined but **never consumed by any production code path**. It is exercised only in test code (`test_full_flow.py:102-103, 318`). The field has been dead since its introduction.

Every release proposes to be its first production consumer, but through different semantics:

| Release | Proposed reimbursement_rate semantics |
|---------|--------------------------------------|
| v3.05   | Convergence progress credit — partial refund when structural HIGHs decrease between runs |
| v3.1    | Gate-pass reimbursement — credit `floor(actual_turns * 0.8)` when a trailing gate passes |
| v3.2    | Wiring gate credit — credit via `credit_wiring()` when wiring analysis finds zero issues |

**Decision required:** These are complementary, not conflicting. All three can coexist because they operate at different scopes (convergence run vs task gate vs wiring check). The v3.1 gate-pass reimbursement is the most general and should be wired first; v3.05 and v3.2 then consume `reimbursement_rate` through domain-specific helpers.

---

## 2. TurnLedger Extensions Needed Across ALL Releases

### 2.1 Extensions Required by Multiple Releases (Unified)

| Extension | Needed By | Purpose |
|-----------|-----------|---------|
| `execute_sprint()` must instantiate a TurnLedger | v3.1, v3.2 | Currently the main sprint loop has zero budget tracking |
| Gate-pass reimbursement wired into `execute_phase_tasks()` | v3.1, v3.2 | Activate `reimbursement_rate` after gate evaluation |
| `SprintGatePolicy` instantiation in sprint loop | v3.1, v3.2 | Currently defined but never instantiated in production |
| `attempt_remediation()` called from sprint execution | v3.05, v3.1, v3.2 | Currently only tested, never called from production |
| `DeferredRemediationLog` wired into sprint executor | v3.1, v3.2 | Single failure journal replacing fragmented tracking |
| `build_kpi_report()` called at sprint completion | v3.1, v3.2 | Currently exists but never invoked from production |

### 2.2 Extensions Required by Single Releases

| Extension | Release | Purpose |
|-----------|---------|---------|
| `max_convergence_runs: int = 3` field | v3.05 | Run-count budget (orthogonal to turn budget) |
| `runs_completed: int` counter | v3.05 | Track convergence iterations separately from turns |
| `ConvergenceBudget` composition model | v3.05 | Quality budget alongside resource budget |
| `debit_wiring()` / `credit_wiring()` methods | v3.2 | Wiring-gate-specific budget tracking for KPI |
| `wiring_gate_cost` / `wiring_gate_credits` fields | v3.2 | Per-gate-type accounting |
| `gate_rollout_mode` on SprintConfig | v3.1 | Shadow/soft/full for general gate evaluation |
| `wiring_gate_scope: GateScope` on SprintConfig | v3.2 | Replace string mode switches with scope-based resolution |

### 2.3 Shared Infrastructure That Should Be Built Once

| Component | Current State | Required State |
|-----------|--------------|----------------|
| `TurnLedger` location | `sprint/models.py` | Should migrate to `pipeline/models.py` (shared economic primitive) |
| Gate-pass reimbursement loop | Test-only (`test_full_flow.py`) | Production in `execute_phase_tasks()` |
| `TrailingGateRunner` sprint wiring | Never called from sprint loop | Per-phase instantiation in `execute_phase_tasks()` |
| `resolve_gate_mode()` usage | Only in trailing_gate.py | Replace all `wiring_gate_mode` string switches |

---

## 3. Lowest-Conflict Proposal Per Release

### v3.05: Proposal 1 — Ledger-Backed Convergence Shim (1B)

**Why:** Lowest disruption. Keeps FR-7 semantics intact while replacing custom budget accounting with TurnLedger debit/credit cycles. The convergence engine gets TurnLedger as an injected parameter (not internally constructed), maintaining separation of concerns.

**Key insight from 1A:** TurnLedger is a *resource budget*; v3.05 needs a *quality budget*. These are orthogonal. The recommended architecture is **composition**: TurnLedger for resource guardrails + a new `ConvergenceBudget` for quality guardrails (monotonic progress, run counting). Don't merge them.

**Cross-release impact:** Minimal. v3.05 adds a new `execute_fidelity_with_convergence()` function behind `convergence_enabled` flag. No modifications to existing `execute_phase_tasks()` or `execute_sprint()`.

### v3.1: Proposal 1 — Gate-Coupled Reimbursement Ledger (2B)

**Why:** Highest ROI. Closes the most critical gap: activating `reimbursement_rate` in production by crediting budget on gate pass. This is the foundational change that all other releases benefit from.

**Key insight from 2A:** Three separate retry/remediation systems exist in parallel (pipeline executor retry, `attempt_remediation()`, convergence engine). v3.1 should unify the sprint-level systems, not all three.

**Cross-release impact:** This is the **prerequisite** for v3.2. Once gate-pass reimbursement is wired into `execute_phase_tasks()`, v3.2's wiring gate simply plugs into the same mechanism.

### v3.2: Proposal A — Documentation-Only TurnLedger Overlay (3B)

**Why:** Fewest spec edits. Makes rollout phases (shadow/soft/full) explicit as TurnLedger reimbursement profiles without restructuring the spec. If v3.1's gate-pass reimbursement is already landed, v3.2 inherits it.

**Key insight from 3A:** The entire `wiring_gate_mode` switch operates with zero TurnLedger interaction. The infrastructure exists (`TrailingGateRunner`, `SprintGatePolicy`, `DeferredRemediationLog`, `attempt_remediation()`) but is all disconnected from the sprint loop. v3.2's job is *wiring*, not *building*.

**Cross-release impact:** Minimal if v3.1 lands first. The 3C design shows how `run_post_task_wiring_hook()` gains a `ledger` parameter and uses `resolve_gate_mode()` instead of string switches.

---

## 4. Recommended Execution Order

```
v3.1 (Unified Audit Gating — Gate-Coupled Reimbursement)
  ↓
v3.2 (Wiring Verification Gate — TurnLedger-Native)
  ↓
v3.05 (Deterministic Fidelity Gates — Convergence Budget Composition)
```

### Rationale

1. **v3.1 first** because it establishes the foundational wiring:
   - `execute_sprint()` creates a TurnLedger
   - Gate-pass reimbursement activates `reimbursement_rate`
   - `TrailingGateRunner` per-phase in `execute_phase_tasks()`
   - `DeferredRemediationLog` as single failure journal
   - `build_kpi_report()` called at sprint completion
   - `gate_rollout_mode` on SprintConfig

2. **v3.2 second** because it consumes what v3.1 built:
   - `run_post_task_wiring_hook()` gets `ledger` parameter (threads from v3.1's wiring)
   - Wiring gate plugs into the same `TrailingGateRunner` + `DeferredRemediationLog`
   - `resolve_gate_mode()` replaces string switches (v3.1 already demonstrates the pattern)
   - `attempt_remediation()` called from wiring hook (v3.1 already calls it from gate hook)

3. **v3.05 last** because it's the most independent:
   - Operates in the roadmap/convergence domain, not the sprint domain
   - Uses `TurnLedger` as an injected parameter (doesn't depend on sprint-level wiring)
   - Gated entirely behind `convergence_enabled` flag
   - The only v3.1 dependency is that `TurnLedger` may have moved to `pipeline/models.py`

---

## 5. Mutually Exclusive Proposals

### Within releases — no conflicts

All three "lowest-conflict" proposals are compatible:
- v3.05 Proposal 1 (shim) only touches convergence.py behind a flag
- v3.1 Proposal 1 (gate reimbursement) only touches execute_phase_tasks() + new hook
- v3.2 Proposal A (documentation overlay) only adds spec language + minor hook changes

### Cross-release conflicts to watch

| Conflict | Releases | Resolution |
|----------|----------|------------|
| Both v3.1 and v3.2 add a `run_post_task_gate_hook()` | v3.1, v3.2 | v3.1 builds the generic hook; v3.2 extends it with wiring-specific logic |
| Both v3.1 and v3.2 propose `gate_rollout_mode` field | v3.1, v3.2 | v3.1 adds it; v3.2 uses it (or uses `wiring_gate_scope` which resolves to the same semantics) |
| v3.05's `reimburse_for_progress()` and v3.1's gate-pass credit both consume `reimbursement_rate` | v3.05, v3.1 | Non-conflicting: different code paths, different callers, same field |
| v3.2 proposes `debit_wiring()`/`credit_wiring()` helper methods on TurnLedger | v3.2 only | Consider making these generic (`debit_gate(gate_name, turns)`) so future gates reuse the pattern |
| v3.05 proposes moving TurnLedger to `pipeline/models.py` | All | Should be done as a pre-requisite or alongside v3.1, before v3.05 imports it into roadmap code |

### Mutually exclusive higher-disruption proposals

If the more aggressive proposals are chosen instead:
- v3.05 Proposal 3 (TurnLedger as Registry Currency) **conflicts** with v3.1 Proposal 1 because it redefines what TurnLedger events mean (ledger events become registry events, not just budget events)
- v3.2 Proposal C (TurnLedger as Rollout Authority) **conflicts** with v3.1's `gate_rollout_mode` approach by replacing mode strings entirely with `GateRolloutBudgetProfile` objects

**Recommendation:** Stick with the lowest-disruption proposals per release. They are architecturally compatible and can be composed without coordination beyond the execution order above.

---

## 6. Key Metrics

| Metric | Value |
|--------|-------|
| Total TurnLedger extensions needed (shared) | 6 |
| Total TurnLedger extensions needed (release-specific) | 7 |
| Dead code components activated | 4 (`reimbursement_rate`, `SprintGatePolicy`, `attempt_remediation` from sprint, `TrailingGateRunner` from sprint) |
| New files needed | 0 (all changes are to existing files) |
| Spec sections requiring revision | v3.05: FR-7/FR-7.1/FR-10; v3.1: executor integration; v3.2: Section 4.5/6.2/8/10 |
| Backward compatibility risk | Low (all changes gated behind flags or None-safe) |
