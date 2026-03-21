---
title: "TurnLedger Integration Refactoring Proposal for v3.05 Requirements Spec"
status: draft
created: 2026-03-20
agent: "Agent 1 (Refactoring Expert)"
source_spec: "deterministic-fidelity-gate-requirements.md v1.1.0"
source_design: "turnledger-integration/v3.05/design.md"
---

# TurnLedger Integration Refactoring Proposal

## Executive Summary

The TurnLedger design addendum (`design.md`) proposes replacing the v3.05 spec's
implicit "3-run hard budget" model with an explicit economic model governed by
`TurnLedger` (from `sprint/models.py`). This affects FR-7 (convergence gate),
FR-7.1 (FR-7/FR-8 interface), FR-8 (regression detection), and FR-9
(remediation). The design is additive and feature-flagged behind
`convergence_enabled`, but it introduces new concepts (turn-based costing,
reimbursement semantics, budget guards) that must be reconciled with the
existing requirements text.

---

## 1. Section-by-Section Diff Summary

### Section 1 (Problem Statement) -- NO CHANGE
The problem statement, evidence, scope boundary, and v3.0 baseline are
unaffected. TurnLedger does not alter the problem definition.

### Section 2 (Clarified User Goals) -- NO CHANGE
Goals G1-G6 remain intact. TurnLedger is an implementation mechanism for G2
(convergence termination) but does not change the user-facing goal.

### FR-1 (Structural Checkers) -- NO CHANGE
Checkers are pure functions. TurnLedger does not interact with them.

### FR-2 (Spec & Roadmap Parser) -- NO CHANGE
Parser is upstream of the convergence loop. No TurnLedger interaction.

### FR-3 (Anchored Severity Rules) -- NO CHANGE
Severity rules are static lookup tables. No TurnLedger interaction.

### FR-4 (Semantic Layer) -- NO CHANGE
The semantic layer itself is not budget-governed by TurnLedger. The existing
FR-4.2 prompt budget enforcement (byte-based, 30KB cap) remains distinct from
TurnLedger's turn-based budget.

### FR-5 (Sectional Comparison) -- NO CHANGE
Section splitting is a data preparation step. No TurnLedger interaction.

### FR-6 (Deviation Registry) -- MINOR SUPPLEMENT
The design addendum references `registry.merge_findings()` and
`registry.get_active_highs()` but does not propose changes to the registry's
data model or persistence format. The addendum's `registry.runs[-2]` access
pattern implies RunMetadata is stored in an ordered list, which is compatible
with FR-6's existing run metadata tracking.

**What stays**: All FR-6 acceptance criteria. Registry data model unchanged.
**What's new**: Nothing explicit, but the design assumes `merge_findings()` is
a single call accepting both structural and semantic lists -- this is not
currently specified in FR-6's acceptance criteria.

### FR-7 (Convergence Gate) -- SIGNIFICANT MODIFICATION
This is the primary integration point. The design replaces the spec's implicit
"3 fixed runs" model with TurnLedger-governed budget management.

**What stays**:
- Pass condition: `active_high_count == 0`
- Monotonic progress check on structural HIGHs only
- Semantic fluctuation logged as warnings
- Maximum 3 runs (catch/verify/backup)
- Gate authority model (registry-only in convergence mode)
- Pipeline integration within step 8
- Steps 1-7 and step 9 unaffected
- Wiring-verification bypass preserved
- `spec_fidelity_file` decorative in convergence mode

**What changes**:
- Budget enforcement moves from implicit run counter to `ledger.can_launch()` / `ledger.can_remediate()` guards
- Budget exhaustion returns `ConvergenceResult(halt_reason=...)` instead of counting runs
- Early convergence produces a credit via `ledger.credit(CONVERGENCE_PASS_CREDIT)`
- Forward progress (fewer structural HIGHs) produces partial credit via `reimburse_for_progress()`
- The `_check_remediation_budget()` / `_print_terminal_halt()` exclusion (already in FR-7) now has a positive replacement: TurnLedger budget guards

**What's new**:
- `execute_fidelity_with_convergence()` signature gains `ledger: TurnLedger` parameter
- Pre-run budget guard (`ledger.can_launch()`) as a gate before each run
- Pre-remediation budget guard (`ledger.can_remediate()`) as a gate before each remediation
- Cost constants: `CHECKER_COST`, `REMEDIATION_COST`, `REGRESSION_VALIDATION_COST`, `CONVERGENCE_PASS_CREDIT`
- Derived budget constants: `MIN_CONVERGENCE_BUDGET`, `STD_CONVERGENCE_BUDGET`, `MAX_CONVERGENCE_BUDGET`
- `reimburse_for_progress()` helper consuming `reimbursement_rate`
- TurnLedger construction in `executor.py` step 8 dispatch

### FR-7.1 (FR-7/FR-8 Interface) -- MINOR MODIFICATION
**What stays**: `handle_regression()` signature, `RegressionResult` dataclass, budget accounting rule, ownership boundaries.
**What changes**: The budget accounting is now expressed in turns (`ledger.debit(REGRESSION_VALIDATION_COST)`) rather than abstract "budget units."

### FR-8 (Regression Detection) -- MINOR SUPPLEMENT
**What stays**: All acceptance criteria. Parallel agent spawning, merge logic, debate, cleanup.
**What's new**: Regression validation has an explicit cost (`REGRESSION_VALIDATION_COST = 15 turns`) debited from the ledger before spawning agents.

### FR-9 (Remediation) -- MINOR SUPPLEMENT
**What stays**: All acceptance criteria. Patch format, diff-size guard, rollback, MorphLLM compatibility.
**What's new**: Each remediation cycle has an explicit cost (`REMEDIATION_COST = 8 turns`) debited from the ledger. Pre-remediation budget guard prevents remediation when budget is insufficient.

### FR-10 (Run-to-Run Memory) -- NO CHANGE
Memory mechanism is the registry. TurnLedger does not interact with it.

### NFRs -- MINOR SUPPLEMENT
**What stays**: All 7 NFRs.
**What's new**: Turn-based budget enforcement could be considered an extension of NFR-2 (convergence in 3 runs), providing a more granular measurement than run count alone.

### User Stories -- NO CHANGE
US-1 through US-6 remain valid. TurnLedger is invisible at the user story level.

### Appendices -- MINOR UPDATE NEEDED
The convergence loop detail in Appendix A needs updating to show TurnLedger debit/credit points.

---

## 2. Exact Requirement IDs Affected

### FR-7: Convergence Gate

**FR-7 acceptance criterion (new)**:
- BEFORE: (not present)
- AFTER: `[ ] execute_fidelity_with_convergence() accepts a ledger: TurnLedger parameter for turn-based budget enforcement`

**FR-7 acceptance criterion (new)**:
- BEFORE: (not present)
- AFTER: `[ ] Pre-run budget guard: ledger.can_launch() checked before each fidelity run; returns ConvergenceResult(halt_reason="convergence_budget_exhausted") on failure`

**FR-7 acceptance criterion (new)**:
- BEFORE: (not present)
- AFTER: `[ ] Pre-remediation budget guard: ledger.can_remediate() checked before each remediation cycle; returns ConvergenceResult(halt_reason="remediation_budget_exhausted") on failure`

**FR-7 acceptance criterion (modified)**:
- BEFORE: `[ ] If budget exhausted without convergence: halt, write diagnostic report, exit non-zero`
- AFTER: `[ ] If budget exhausted without convergence (ledger.can_launch() returns False or max 3 runs reached): halt, write diagnostic report via ConvergenceResult(halt_reason=...), exit non-zero`

**FR-7 acceptance criterion (new)**:
- BEFORE: (not present)
- AFTER: `[ ] Early convergence (0 HIGHs before run 3) credits unused budget via ledger.credit(CONVERGENCE_PASS_CREDIT)`

**FR-7 acceptance criterion (new)**:
- BEFORE: (not present)
- AFTER: `[ ] Forward progress (fewer structural HIGHs) credits partial run cost via reimburse_for_progress(ledger, run_cost, prev_highs, curr_highs)`

**FR-7 acceptance criterion (new)**:
- BEFORE: (not present)
- AFTER: `[ ] Cost constants defined as module-level integers in convergence.py: CHECKER_COST, REMEDIATION_COST, REGRESSION_VALIDATION_COST, CONVERGENCE_PASS_CREDIT`

**FR-7 acceptance criterion (new)**:
- BEFORE: (not present)
- AFTER: `[ ] Derived budget constants defined: MIN_CONVERGENCE_BUDGET, STD_CONVERGENCE_BUDGET, MAX_CONVERGENCE_BUDGET`

**FR-7 acceptance criterion (modified)**:
- BEFORE: `[ ] _check_remediation_budget() and _print_terminal_halt() are NOT invoked when convergence_enabled=true`
- AFTER: `[ ] _check_remediation_budget() and _print_terminal_halt() are NOT invoked when convergence_enabled=true; TurnLedger budget guards replace their function`

**FR-7 acceptance criterion (modified)**:
- BEFORE: `[ ] Convergence budget (3 runs) and legacy budget (2 attempts) never overlap`
- AFTER: `[ ] Convergence budget (TurnLedger-governed, up to 3 runs) and legacy budget (_check_remediation_budget, 2 attempts) never overlap; convergence_enabled=True constructs TurnLedger, convergence_enabled=False never constructs TurnLedger`

### FR-7.1: FR-7/FR-8 Interface Contract

**FR-7.1 acceptance criterion (modified)**:
- BEFORE: `[ ] Regression validation + remediation counts as one budget unit`
- AFTER: `[ ] Regression validation + remediation counts as one budget unit; regression validation debits REGRESSION_VALIDATION_COST from ledger, with no separate debit for post-regression remediation`

### FR-8: Regression Detection

**FR-8 acceptance criterion (new)**:
- BEFORE: (not present)
- AFTER: `[ ] Regression validation debits REGRESSION_VALIDATION_COST from the TurnLedger before spawning parallel agents`

### FR-9: Edit-Only Remediation

**FR-9 acceptance criterion (new)**:
- BEFORE: (not present)
- AFTER: `[ ] Each remediation cycle debits REMEDIATION_COST from the TurnLedger before execution`

### Module Disposition (frontmatter)

**convergence.py entry (modified)**:
- BEFORE: `extends_frs: [FR-6, FR-7, FR-8, FR-10]`
- AFTER: `extends_frs: [FR-6, FR-7, FR-7.1, FR-8, FR-10]` (FR-7.1 explicitly affected by TurnLedger integration)

**relates_to (new entry)**:
- BEFORE: (not present)
- AFTER: `- src/superclaude/cli/sprint/models.py` (TurnLedger source)

---

## 3. New Requirements Introduced by TurnLedger Integration

### NR-1: TurnLedger as Convergence Budget Engine
**Description**: The convergence engine uses TurnLedger (from `sprint/models.py`) as its budget enforcement mechanism. The pipeline executor constructs a TurnLedger with `initial_budget` calibrated to the convergence workload and passes it to `execute_fidelity_with_convergence()`.

**Acceptance Criteria**:
- [ ] TurnLedger imported from `superclaude.cli.sprint.models` in convergence.py (conditional on convergence_enabled)
- [ ] Pipeline executor (executor.py) constructs TurnLedger with MAX_CONVERGENCE_BUDGET when convergence_enabled=True
- [ ] TurnLedger is NEVER constructed when convergence_enabled=False
- [ ] Cross-module import (sprint -> roadmap) is documented as acceptable with future migration path noted

### NR-2: Reimbursement Rate Consumption
**Description**: The `reimbursement_rate` field on TurnLedger (currently dead code) gains its first production consumer through the `reimburse_for_progress()` helper in the convergence engine.

**Acceptance Criteria**:
- [ ] `reimburse_for_progress()` function defined in convergence.py
- [ ] Function consumes `ledger.reimbursement_rate` to compute partial credit
- [ ] Credit issued only when `curr_structural_highs < prev_structural_highs`
- [ ] Credit amount: `int(run_cost * ledger.reimbursement_rate)`
- [ ] Zero credit for stalled or regressed runs
- [ ] Progress log entry appended to ConvergenceResult for auditability

### NR-3: Cost Constant Calibration
**Description**: Module-level constants in convergence.py define the turn cost for each convergence operation. These are calibration defaults, overridable via TurnLedger constructor arguments.

**Acceptance Criteria**:
- [ ] CHECKER_COST = 10 (turns per checker suite run)
- [ ] REMEDIATION_COST = 8 (turns per remediation cycle)
- [ ] REGRESSION_VALIDATION_COST = 15 (turns for FR-8 parallel validation)
- [ ] CONVERGENCE_PASS_CREDIT = 5 (turns credited on early pass)
- [ ] MIN_CONVERGENCE_BUDGET = 28 (2 runs + 1 remediation)
- [ ] STD_CONVERGENCE_BUDGET = 46 (3 runs + 2 remediations)
- [ ] MAX_CONVERGENCE_BUDGET = 61 (standard + regression validation)
- [ ] Constants are module-level integers, not config fields (to prevent runtime misconfiguration)

### NR-4: Pipeline Executor Step 8 Dispatch
**Description**: The pipeline executor's step 8 handling gains a conditional branch for convergence mode that constructs a TurnLedger, calls `execute_fidelity_with_convergence()`, and maps the result to a StepResult.

**Acceptance Criteria**:
- [ ] Step 8 dispatch checks `config.convergence_enabled` before execution
- [ ] Convergence branch constructs TurnLedger with MAX_CONVERGENCE_BUDGET
- [ ] ConvergenceResult mapped to StepResult(status=PASS|FAIL)
- [ ] Legacy branch is byte-identical to pre-v3.05 (no TurnLedger involvement)

---

## 4. Risks and Conflicts

### CONFLICT-1: Budget Model Duality (MEDIUM risk)

**Conflict**: FR-7 currently describes budget as "Maximum 3 runs (catch -> verify -> backup)" -- a discrete run counter. The design addendum replaces this with a continuous turn-based budget that _approximates_ 3 runs but can terminate earlier (if turn budget runs out) or behave differently (if credits extend effective budget beyond 3 runs).

**Evidence in spec**: FR-7 says "Hard budget: Maximum 3 runs" and the convergence loop detail (Appendix A) shows exactly 3 iterations. The design addendum's `for run_number in [1, 2, 3]` preserves the 3-iteration cap, but `ledger.can_launch()` could terminate at run 2 if budget is exhausted.

**Specific tension**: If CHECKER_COST + REMEDIATION_COST + REGRESSION_VALIDATION_COST consume enough turns in runs 1-2, the ledger may refuse to launch run 3 even though the spec guarantees "3 runs max." Conversely, `reimburse_for_progress()` credits could theoretically allow the ledger to fund more work than expected, though the `for run_number in [1, 2, 3]` cap prevents a 4th run.

**Severity**: MEDIUM. The 3-run cap is preserved by the loop structure, but early budget exhaustion via `can_launch()` is a new failure mode not described in the original spec.

**Recommended Resolution**: FR-7 should explicitly state that the 3-run cap is a structural invariant (enforced by loop bounds) AND that turn-based budget provides a secondary guard that can halt before 3 runs if the convergence workload is more expensive than calibrated. Add an acceptance criterion: "The convergence loop iterates at most 3 times regardless of TurnLedger state; TurnLedger provides an additional budget guard that can halt before 3 runs but never extends beyond 3."

### CONFLICT-2: ConvergenceResult.halt_reason Not in Spec (LOW risk)

**Conflict**: The design addendum returns `ConvergenceResult(halt_reason="convergence_budget_exhausted")` and `halt_reason="remediation_budget_exhausted"`, but the existing `ConvergenceResult` dataclass (convergence.py:228-237) is not specified to have a `halt_reason` field.

**Evidence in spec**: FR-7 says "halt, write diagnostic report, exit non-zero" but does not specify how halt reasons are communicated. The addendum introduces structured halt reasons.

**Severity**: LOW. This is an additive field on an existing dataclass with a default value.

**Recommended Resolution**: Add `halt_reason: str = ""` to the ConvergenceResult specification in FR-7. Define allowed values: `""` (no halt), `"convergence_budget_exhausted"`, `"remediation_budget_exhausted"`, `"max_runs_exhausted"`. This makes the diagnostic report requirement in FR-7 more concrete.

### CONFLICT-3: Cross-Module Import Boundary (LOW risk)

**Conflict**: TurnLedger lives in `superclaude.cli.sprint.models`. Importing it into `superclaude.cli.roadmap.convergence` crosses the sprint/roadmap package boundary.

**Evidence in spec**: The spec's `relates_to` frontmatter lists only `roadmap/` modules. The addendum explicitly addresses this (Section 5.4) and proposes a future migration to `pipeline.models`.

**Severity**: LOW. The import is conditional and the design acknowledges the boundary concern.

**Recommended Resolution**: Accept the cross-module import for v3.05 with a documented tech debt item: "Migrate TurnLedger to `superclaude.cli.pipeline.models` in a future release." Add `src/superclaude/cli/sprint/models.py` to the `relates_to` frontmatter.

### CONFLICT-4: reimbursement_rate Semantic Drift (MEDIUM risk)

**Conflict**: The design gives `reimbursement_rate` production semantics ("convergence progress credit") that may not align with its original sprint-domain intent. The field was designed for sprint task cost recovery, not fidelity convergence incentives.

**Evidence in design**: Section 3.1 documents that `reimbursement_rate` is currently dead code. Section 3.2 repurposes it for convergence credits. The analogy to `execute_phase_tasks()` (executor.py:587-589) is suggestive but not binding.

**Severity**: MEDIUM. If sprint-domain code later consumes `reimbursement_rate` with different semantics, the shared field becomes ambiguous. The default value (0.8) is preserved, but its meaning diverges.

**Recommended Resolution**: Two options:
  1. **(Preferred)** Accept the design as-is for v3.05 since the field is dead code. Document that `reimbursement_rate` is consumed by both sprint credit recovery (future) and convergence progress credit (v3.05), and that the semantic is "fraction of cost returned on success." If the semantics diverge later, introduce a separate field.
  2. **(Conservative)** Define a separate `convergence_credit_rate: float = 0.8` constant in convergence.py rather than consuming the TurnLedger field. This avoids semantic coupling but loses the benefit of having TurnLedger be the single budget configuration point.

### CONFLICT-5: Budget Guard vs. Run Counter for Regression (LOW risk)

**Conflict**: FR-7.1 states "Regression validation + remediation counts as one budget unit." The design addendum debits `REGRESSION_VALIDATION_COST` separately from `REMEDIATION_COST`, which could cause the budget to be consumed faster than the spec's "one budget unit" abstraction implies.

**Evidence in design**: Section 2.1, point (D) debits `REGRESSION_VALIDATION_COST` for FR-8 and notes "No separate debit for post-regression remediation." This aligns with the spec's intent but replaces a conceptual "1 unit" with "15 turns" that is distinct from the normal remediation debit.

**Severity**: LOW. The design correctly implements the spec's intent (regression + remediation = 1 conceptual unit) by omitting the remediation debit after regression.

**Recommended Resolution**: Accept as-is. Clarify in FR-7.1 that "one budget unit" in TurnLedger terms means "REGRESSION_VALIDATION_COST turns, with no additional REMEDIATION_COST debit for the same run."

### CONFLICT-6: Signature Change on execute_fidelity_with_convergence() (LOW risk)

**Conflict**: FR-7 does not currently specify a function signature for `execute_fidelity_with_convergence()`. The design addendum proposes a specific signature with `ledger: TurnLedger` as a required positional parameter plus three injectable callables.

**Evidence in spec**: FR-7 mentions `execute_fidelity_with_convergence()` and `handle_regression()` as new functions but does not specify their full signatures. FR-7.1 specifies `handle_regression()` signature but not the convergence orchestrator.

**Severity**: LOW. The spec is underspecified, not contradicted.

**Recommended Resolution**: Add the full signature to FR-7 as specified in the design addendum. The injectable callables (`run_checkers`, `run_remediation`, `handle_regression_fn`) are a testability pattern consistent with FR-4.1's `claude_process_factory` injection.

---

## 5. Recommended Resolutions Summary

| ID | Risk | Resolution | Spec Change Required |
|----|------|-----------|---------------------|
| CONFLICT-1 | MEDIUM | Add dual-guard acceptance criterion (loop cap + turn budget) | FR-7: 1 new AC, 1 modified AC |
| CONFLICT-2 | LOW | Add `halt_reason` field to ConvergenceResult spec | FR-7: 1 new AC |
| CONFLICT-3 | LOW | Accept cross-import, add to relates_to, document tech debt | Frontmatter: 1 new entry |
| CONFLICT-4 | MEDIUM | Accept for v3.05 with documented semantic note | FR-7: 1 new note paragraph |
| CONFLICT-5 | LOW | Accept; clarify budget unit in TurnLedger terms | FR-7.1: 1 modified AC |
| CONFLICT-6 | LOW | Add full signature to FR-7 | FR-7: 1 new code block |

---

## 6. Implementation Ordering Recommendation

The TurnLedger integration should be implemented AFTER the core v3.05
infrastructure (FR-1 through FR-6, FR-10) and DURING FR-7 implementation,
because:

1. FR-7 is the sole integration point for TurnLedger in the convergence loop.
2. FR-8 and FR-9 only need minor debiting calls added, which can be wired
   after their core logic is complete.
3. The cost constants (NR-3) require the checker/remediation/regression code
   to exist before calibration is meaningful.
4. The pipeline executor dispatch (NR-4) is the final wiring step.

**Suggested order**:
1. FR-1, FR-2, FR-3, FR-5, FR-6, FR-10 (no TurnLedger involvement)
2. FR-4 (semantic layer, no TurnLedger involvement)
3. FR-7 + NR-1 + NR-3 (convergence gate with TurnLedger budget engine and cost constants)
4. FR-7.1 + NR-2 (interface contract with reimbursement semantics)
5. FR-8 (regression detection, add debit call)
6. FR-9 (remediation, add debit call)
7. NR-4 (pipeline executor dispatch -- final wiring)

---

## 7. Files Affected by Integration

| File | Change Type | Description |
|------|------------|-------------|
| `src/superclaude/cli/roadmap/convergence.py` | MODIFY | Add `execute_fidelity_with_convergence()`, `reimburse_for_progress()`, cost constants, TurnLedger import |
| `src/superclaude/cli/roadmap/executor.py` | MODIFY | Add step 8 convergence dispatch with TurnLedger construction |
| `src/superclaude/cli/roadmap/models.py` | MODIFY | Add `halt_reason: str = ""` to ConvergenceResult |
| `src/superclaude/cli/sprint/models.py` | NO CHANGE | TurnLedger consumed as-is |
| `deterministic-fidelity-gate-requirements.md` | AMEND | Incorporate TurnLedger acceptance criteria per this proposal |
