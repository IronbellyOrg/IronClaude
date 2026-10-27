# Cross-Release Consistency Check: TurnLedger Integration

**Date**: 2026-03-20
**Releases compared**: v3.1 (Anti-Instincts Gate), v3.2 (Wiring Verification Gate), v3.05 (Deterministic Fidelity Gates)
**Planned execution order**: v3.1 -> v3.2 -> v3.05

---

## Execution Order Validation

### Is the planned order (v3.1 -> v3.2 -> v3.05) still valid?

**Yes, with caveats.** The planned order is valid and is in fact the most natural sequence, but all three plans explicitly state they are architecturally independent and can land in any order. The key evidence:

- **v3.1 (Anti-Instincts)**: Establishes `gate_rollout_mode` on `SprintConfig`, `TrailingGateRunner`, `DeferredRemediationLog`, `run_post_task_gate_hook()`, and the `resolve_gate_mode()` consumption pattern. This is foundational sprint-pipeline infrastructure.
- **v3.2 (Wiring Verification)**: Consumes `resolve_gate_mode()`, `TrailingGateRunner.submit()`, `DeferredRemediationLog`, and `attempt_remediation()`. If v3.1 lands first, v3.2 wires into existing infrastructure. If v3.2 lands first, it self-contains via `ledger is None` fallback.
- **v3.05 (Fidelity Gates)**: Operates in the roadmap pipeline's convergence engine, not the sprint pipeline's trailing gate infrastructure. Uses TurnLedger as an injected budget tracker. Fully gated behind `convergence_enabled`. No dependency on v3.1 or v3.2.

### Does any plan assume work from a later release as a prerequisite?

**No hard prerequisites detected.** Each plan includes explicit backward-compatibility contracts:

| Release | Fallback when predecessors absent | Evidence |
|---------|-----------------------------------|----------|
| v3.1 | `gate_rollout_mode="off"` default; `TurnLedger` None-safe throughout | v3.1 BC notes 1, 2 |
| v3.2 | `ledger is None` path preserves phase-level execution; `wiring_gate_mode` migration is defensive only | v3.2 BC-2, BC-1 |
| v3.05 | `convergence_enabled=False` means no TurnLedger constructed, all existing tests pass | v3.05 BC note 1 |

**Soft preference**: v3.1 landing first is recommended by both v3.2 (BC-5: "v3.1-first is recommended") and v3.05 (note 10: "Recommended order is v3.1 -> v3.2 -> v3.05"). v3.2 benefits from v3.1 establishing `TrailingGateRunner` and `resolve_gate_mode()` infrastructure. v3.05 benefits from TurnLedger location migration coordination.

### Are there circular dependencies?

**No.** The dependency graph is strictly acyclic:

```
v3.1 (Anti-Instincts) -- establishes sprint gate infrastructure
    |
    v
v3.2 (Wiring Verification) -- consumes sprint gate infrastructure
    |
    (no dependency)
    |
v3.05 (Fidelity Gates) -- independent convergence engine path
```

v3.05 has zero dependency on v3.1 or v3.2. v3.2 has a soft dependency on v3.1 (infrastructure it consumes). v3.1 has no dependencies on either.

---

## Conflicting TurnLedger Extensions

### Do the 3 plans propose conflicting modifications to TurnLedger or its API?

**No conflicts. All modifications are additive and non-overlapping.**

| Release | TurnLedger Modifications | Scope |
|---------|-------------------------|-------|
| v3.1 | **None** -- consumes existing `TurnLedger` as-is; adds `gate_rollout_mode` to `SprintConfig` | Sprint config only |
| v3.2 | Adds 3 fields (`wiring_gate_cost`, `wiring_gate_credits`, `wiring_gate_scope`) and 3 methods (`debit_wiring()`, `credit_wiring()`, `can_run_wiring_gate()`) to TurnLedger | TurnLedger class extension |
| v3.05 | **None** -- consumes existing `TurnLedger` as-is; all convergence logic lives in `convergence.py` | No TurnLedger modification |

**Assessment**: v3.05 and v3.1 both explicitly state "TurnLedger class itself is NOT modified." Only v3.2 extends TurnLedger, and its extensions are wiring-specific fields/methods that do not conflict with existing fields. The three plans touch entirely different surfaces of the TurnLedger API.

### Do they propose conflicting extensions to shared infrastructure?

**Shared file analysis:**

| File | v3.1 Changes | v3.2 Changes | v3.05 Changes | Conflict? |
|------|-------------|-------------|--------------|-----------|
| `sprint/models.py` | Add `gate_rollout_mode` to `SprintConfig` | Add 3 fields + 3 methods to `TurnLedger`; replace `wiring_gate_mode` with 3 fields on `SprintConfig` | No changes (import only) | **LOW RISK** -- see note below |
| `sprint/executor.py` | Add `run_post_task_gate_hook()`, `TrailingGateRunner`, `build_kpi_report()` | Add wiring hook integration, `resolve_gate_mode()` calls | No changes | **NONE** -- v3.2 consumes v3.1's infrastructure |
| `pipeline/gates.py` | Add `ANTI_INSTINCT_GATE`, 3 check functions, update `ALL_GATES` | `gate_passed()` consumed (read-only) | No changes | **NONE** -- additive vs read-only |
| `pipeline/trailing_gate.py` | Consumed (read-only) | Consumed: `resolve_gate_mode()`, `attempt_remediation()`, `GateScope`, `GateMode` | Referenced as pattern source (read-only) | **NONE** -- all read-only |
| `sprint/kpi.py` | Add `build_kpi_report()` call | Add 6 wiring-specific `GateKPIReport` fields | No changes | **NONE** -- additive |
| `convergence.py` | No changes | No changes | Add `reimburse_for_progress()`, TurnLedger import, budget dispatch | **NONE** -- exclusive to v3.05 |
| `roadmap/executor.py` | Add anti-instinct step + audit runner | No changes | No changes | **NONE** -- exclusive to v3.1 |

**SprintConfig note**: v3.1 adds `gate_rollout_mode: Literal["off","shadow","soft","full"] = "off"` to `SprintConfig`. v3.2 proposes replacing `wiring_gate_mode` (its own field) with `wiring_gate_enabled` + `wiring_gate_scope` + `wiring_gate_grace_period`. These are different fields on the same dataclass -- no conflict. However, if v3.2 lands after v3.1, it should follow v3.1's pattern (using `resolve_gate_mode()` rather than a mode string), which it already does.

### Are there naming conflicts or semantic disagreements?

**One naming concern identified:**

- v3.1 adds `gate_rollout_mode` (singular mode string for all gates)
- v3.2 adds `wiring_gate_scope` + `wiring_gate_grace_period` (per-gate-type config)

These represent two different configuration philosophies: v3.1 uses a single global rollout mode, v3.2 uses per-gate-type fields. This is not a conflict (they coexist), but it creates a configuration surface area concern. Future gates would need to choose between using the global `gate_rollout_mode` or adding gate-specific fields.

**Recommendation**: Document that `gate_rollout_mode` is the global default, and per-gate-type fields (like `wiring_gate_scope`) override it. This should be coordinated between v3.1 and v3.2.

---

## Shared Assumptions

### What assumptions does each plan make about the TurnLedger API?

| Assumption | v3.1 | v3.2 | v3.05 |
|-----------|------|------|-------|
| `TurnLedger` exists at `sprint/models.py` | Yes (A-011) | Yes (models.py:488-525) | Yes (C12, Section 1.3) |
| `TurnLedger` has `reimbursement_rate=0.8` field | Yes (A-013) | Yes (IE-1) | Yes (C5, C14) |
| `TurnLedger` has `debit()` method | No (uses 0 LLM turns) | Yes (via `debit_wiring()`) | Yes (C6, FR-7 Edit 3) |
| `TurnLedger` has `credit()` method | Yes (reimbursement on pass) | Yes (via `credit_wiring()`) | Yes (C5, FR-7 Edit 4) |
| `TurnLedger` has `can_launch()` method | No | No | Yes (FR-7 acceptance criteria) |
| `TurnLedger` has `can_remediate()` method | No | Yes (via `can_run_wiring_gate()`) | Yes (FR-7 acceptance criteria) |
| `TurnLedger` has `initial_budget` constructor param | No | No | Yes (FR-7 Edit 3) |
| `TurnLedger` has `minimum_allocation` field | No | No | Yes (FR-7 Edit 3) |
| `TurnLedger` has `minimum_remediation_budget` field | No | No | Yes (FR-7 Edit 3) |
| `ledger is None` is a valid state | Yes (all paths None-safe) | Yes (BC-2, design Section 6.2) | No (convergence mode always constructs one) |
| `resolve_gate_mode()` exists in `trailing_gate.py` | Yes (Section 8, contradiction 2 resolution) | Yes (IE-2, Section 4.5) | No (not consumed) |
| `TrailingGateRunner` exists | Yes (Section 9.5) | Yes (IE-4) | No (not consumed) |
| `DeferredRemediationLog` exists | Yes (Section 9.5) | Yes (IE-4) | No (not consumed) |

### Are these assumptions mutually consistent?

**Yes.** The assumptions are mutually consistent because:

1. **v3.05 assumes more TurnLedger methods** (`can_launch()`, `can_remediate()`, constructor params) than v3.1 or v3.2. These are existing methods on TurnLedger (defined in sprint/models.py), not new additions. All three plans agree the TurnLedger class is consumed as-is by v3.05 and v3.1; only v3.2 extends it.

2. **v3.2's extensions do not remove or rename anything** v3.05 or v3.1 depend on. v3.2 adds new wiring-specific fields/methods; existing fields/methods are untouched.

3. **The None-safety divergence is not a conflict**: v3.05 always constructs a TurnLedger (gated by `convergence_enabled`), while v3.1 and v3.2 handle `ledger is None`. These are different execution contexts (convergence engine vs sprint trailing gate).

### Does any plan assume TurnLedger fields/methods that another plan would remove or rename?

**No.** No plan removes or renames any existing TurnLedger field or method. All changes are additive.

---

## Cross-Plan Contradictions

### Spec edits in one plan that contradict assumptions in another

**CONTRADICTION 1: `reimbursement_rate` first production consumer**

- v3.05 states: "`reimbursement_rate=0.8` gains its first production consumer" via `reimburse_for_progress()` (C5, BC note 5)
- v3.2 states: "`credit_wiring()` becomes the first production consumer of `reimbursement_rate`" (IE-1)
- v3.1 states: Reimbursement applies to upstream merge step turn cost (Section 9.5, step 4)

All three claim to be the "first production consumer." This is an execution-order-dependent claim, not a true contradiction. **Resolution**: Whichever lands first is the first consumer. Given the planned order (v3.1 -> v3.2 -> v3.05), v3.1's sprint-level gate-pass reimbursement would activate first. However, v3.1's merged plan shows the anti-instinct gate consumes 0 LLM turns, so the effective first meaningful consumer depends on whether any other gate in v3.1 triggers reimbursement. v3.2's `credit_wiring()` and v3.05's `reimburse_for_progress()` are both concrete consumers with explicit formulas.

**Amendment needed**: All three plans should say "one of the first production consumers" rather than "the first," or explicitly state the activation depends on execution order.

### Configuration field conflicts

**CONCERN: `gate_rollout_mode` vs per-gate configuration**

- v3.1 adds `gate_rollout_mode: Literal["off","shadow","soft","full"] = "off"` on `SprintConfig` as a global setting
- v3.2 replaces its own `wiring_gate_mode` with `wiring_gate_enabled` + `wiring_gate_scope` + `wiring_gate_grace_period` -- per-gate-type configuration

These are not conflicting (different fields), but they create an architectural tension: is rollout mode global or per-gate? The v3.1 plan's rollout mode behavior matrix (Section 9.5) applies globally. The v3.2 plan's `resolve_gate_mode(scope, grace_period)` resolves per-gate.

**Resolution**: `gate_rollout_mode` is the global default. Per-gate fields like `wiring_gate_scope` feed into `resolve_gate_mode()` which combines the global mode with per-gate scope. This is consistent but should be explicitly documented as a coordination point.

### Rollout/migration strategy conflicts

**No conflicts.** All three plans use the same rollout philosophy:
- Default to backward-compatible behavior (off/disabled/legacy mode)
- Shadow validation before activation
- Graduation criteria before advancing rollout phases

---

## reimbursement_rate Activation Sequence

### Which release first activates reimbursement_rate as a production field?

**Depends on execution order.** Each plan's consumption pattern:

| Release | Formula | Base Value | Effective Credit |
|---------|---------|-----------|-----------------|
| v3.1 | `int(upstream_merge_turns * 0.8)` | Variable (merge step turn count) | Variable, likely > 0 |
| v3.2 | `int(WIRING_ANALYSIS_TURNS * 0.8)` where WIRING_ANALYSIS_TURNS=1 | 1 turn | **0** (floor-to-zero) |
| v3.05 | `int(CHECKER_COST * 0.8)` where CHECKER_COST=10 | 10 turns | **8** |

### Do the plans agree on the activation sequence?

**Partially.** All three plans acknowledge `reimbursement_rate=0.8` already exists as a default field on TurnLedger with no current production consumers. They agree the field is consumed (not modified). They disagree on which release "activates" it first because each claims primacy.

### Are there conflicts in how reimbursement_rate is consumed?

**No functional conflict, but a semantic divergence:**

- v3.1 applies reimbursement to **upstream step turn cost** (gate pass reimburses the work that preceded the gate)
- v3.2 applies reimbursement to **wiring analysis turn cost** (gate pass reimburses the analysis itself)
- v3.05 applies reimbursement to **checker suite cost** (convergence progress reimburses the checker run)

These are three different base values multiplied by the same rate. The consumers are on different code paths and never interact. **This is consistent** -- `reimbursement_rate` is a policy parameter that each consumer applies to its own domain-specific base cost.

**Risk**: If `reimbursement_rate` is changed globally, all three consumers are affected. v3.05's IE-5 correctly identifies this and mitigates via `reimburse_for_progress()` encapsulation. v3.2 mitigates via `credit_wiring()` encapsulation. v3.1 should similarly encapsulate its reimbursement logic in a named helper.

---

## Shared Infrastructure Modifications

### Which files are modified by multiple releases?

| File | v3.1 | v3.2 | v3.05 | Overlap Nature |
|------|------|------|-------|---------------|
| **`sprint/models.py`** | Add `gate_rollout_mode` to SprintConfig | Add 3 fields + 3 methods to TurnLedger; replace `wiring_gate_mode` on SprintConfig | Import TurnLedger (no modification) | **Additive -- no conflict** |
| **`sprint/executor.py`** | Add `run_post_task_gate_hook()`, TrailingGateRunner, build_kpi_report() | Add wiring hook, resolve_gate_mode() calls, remediation path | No changes | **Sequential dependency -- v3.2 builds on v3.1** |
| **`sprint/kpi.py`** | Add build_kpi_report() infrastructure | Add 6 wiring-specific GateKPIReport fields | No changes | **Additive -- no conflict** |
| **`pipeline/gates.py`** | Add ANTI_INSTINCT_GATE + functions | Read-only consumption | No changes | **Additive vs read-only -- no conflict** |

### Are the modifications additive/compatible or conflicting?

**All additive/compatible.** The highest-risk overlap is `sprint/executor.py` where both v3.1 and v3.2 add significant code. However:
- v3.1 establishes the infrastructure (`run_post_task_gate_hook()`, `TrailingGateRunner`)
- v3.2 wires into that infrastructure (calls `resolve_gate_mode()`, `attempt_remediation()`)
- If v3.2 lands before v3.1, it self-contains via `ledger is None` fallback

### Merge conflict risk assessment

| File | Risk Level | Rationale |
|------|-----------|-----------|
| `sprint/models.py` | **LOW** | v3.1 touches SprintConfig; v3.2 touches TurnLedger class + SprintConfig (different fields). v3.05 is import-only. |
| `sprint/executor.py` | **MEDIUM** | v3.1 and v3.2 both add code to the same file. If merged in order, no conflict. If merged out of order, v3.2's hooks may reference v3.1 infrastructure that doesn't exist yet. Fallback paths handle this. |
| `sprint/kpi.py` | **LOW** | v3.1 adds the function; v3.2 adds fields to the report. Additive to different parts of the file. |
| `pipeline/gates.py` | **NONE** | v3.1 adds; v3.2/v3.05 read-only. |
| `convergence.py` | **NONE** | Only v3.05 modifies. |
| `roadmap/executor.py` | **NONE** | Only v3.1 modifies. |

---

## Recommendations

### Required Sequencing Constraints

1. **No hard constraints exist.** All three plans include backward-compatible fallbacks. Any execution order is technically valid.

2. **Strong recommendation: v3.1 first.** v3.1 establishes the sprint-pipeline gate infrastructure (`TrailingGateRunner`, `run_post_task_gate_hook()`, `resolve_gate_mode()` consumption, `DeferredRemediationLog`, `build_kpi_report()`) that v3.2 consumes. Landing v3.2 before v3.1 means v3.2's sprint integration code runs entirely through `ledger is None` fallback paths until v3.1 lands -- functional but untestable in production.

3. **v3.05 is truly independent.** It can land at any point without affecting or being affected by v3.1 or v3.2. Its TurnLedger usage is entirely within the convergence engine, behind `convergence_enabled`, using injection rather than modification.

### Suggested Coordination Points Between Releases

1. **`reimbursement_rate` ownership**: Establish in v3.1 that `reimbursement_rate` is a shared policy parameter. All three releases should encapsulate their consumption in named helpers (`reimburse_for_progress()` in v3.05, `credit_wiring()` in v3.2, a similarly named helper in v3.1) so rate changes propagate cleanly.

2. **`gate_rollout_mode` vs per-gate config**: Document in v3.1 that `gate_rollout_mode` is the global default, and v3.2's `wiring_gate_scope`/`wiring_gate_grace_period` are per-gate overrides resolved via `resolve_gate_mode()`. This prevents future gates from being confused about which pattern to follow.

3. **TurnLedger location migration**: All three plans note that `TurnLedger` should migrate from `sprint/models.py` to `pipeline/models.py`. This should be a coordinated refactor, ideally before v3.2 lands (since v3.2 adds the most TurnLedger extensions). v3.05 documents this as a one-line import fix.

4. **`DeferredRemediationLog` type adapter pattern**: v3.2 (Gamma IE-4) identifies that `DeferredRemediationLog.append()` requires `TrailingGateResult`, not domain-specific report types. This adapter pattern should be established in v3.1's infrastructure so v3.2 can reuse it.

5. **"First production consumer" language**: Amend all three plans to remove claims of being "the first" consumer of `reimbursement_rate`. Replace with "a production consumer" or make the claim conditional on execution order.

### Plan Amendments Needed for Cross-Release Consistency

| # | Amendment | Affected Plan(s) | Priority |
|---|-----------|------------------|----------|
| 1 | Remove/qualify "first production consumer" claims for `reimbursement_rate` | All three | Medium |
| 2 | v3.1 should encapsulate its reimbursement logic in a named helper (matching v3.05's `reimburse_for_progress()` and v3.2's `credit_wiring()` pattern) | v3.1 | Medium |
| 3 | Document `gate_rollout_mode` (global) vs per-gate config (v3.2) relationship | v3.1, v3.2 | High |
| 4 | v3.2 should reference v3.1's `TrailingGateRunner`/`DeferredRemediationLog` as optional infrastructure (present after v3.1, absent before) rather than assumed infrastructure | v3.2 | Low (already handled by `ledger is None` fallback) |
| 5 | Coordinate TurnLedger migration timing -- recommend as a pre-v3.2 cleanup task | All three (handoff sections) | Low |
| 6 | v3.05 Section 7 handoff should reference v3.2's wiring-specific TurnLedger extensions as a non-conflicting parallel extension | v3.05 | Low |
| 7 | v3.2's `debit_wiring`/`credit_wiring` genericity concern (Alpha unique finding) should be visible to v3.05 -- if generalized to `debit_gate()`/`credit_gate()`, v3.05's convergence engine could potentially use the same pattern | v3.2, v3.05 | Low (deferred to v3.3) |

### Overall Consistency Verdict

**The three plans are mutually consistent.** No blocking contradictions, no circular dependencies, no conflicting TurnLedger modifications. The planned execution order (v3.1 -> v3.2 -> v3.05) is optimal but not mandatory. The primary coordination concern is the `gate_rollout_mode` global-vs-per-gate configuration pattern, which should be explicitly documented in v3.1 before v3.2 lands.
