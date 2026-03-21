# Refactoring Plan: Deterministic Fidelity Gates <- TurnLedger Integration (alpha Design-First)

**Date**: 2026-03-20
**Approach**: Design-first (design.md is authoritative; spec adapts to it)
**Selected Proposal**: Brainstorm Proposal 1 (Ledger-Backed Convergence Shim) + design.md's composition model

---

## Sections Requiring Modification

### Section FR-7: Convergence Gate

- **Current**: FR-7 describes a bespoke "hard budget = 3 runs" model with custom run counting, budget isolation from legacy mode, and halt-on-exhaustion semantics -- all without referencing TurnLedger.
- **Change**: Design.md demands TurnLedger as an injected parameter to `execute_fidelity_with_convergence()`, replacing the bespoke budget model with `ledger.can_launch()`, `ledger.debit()`, and `ledger.credit()` calls at 5 distinct points in the loop (Section 2.1 of design.md). Budget isolation (FR-7 lines 635-643) is preserved via caller-side dispatch: `convergence_enabled=true` constructs a TurnLedger; `false` uses `_check_remediation_budget()`.
- **Edits**:
  - Add `ledger: TurnLedger` to the `execute_fidelity_with_convergence()` signature in the spec (matching design.md Section 1)
  - Replace "hard budget of 3 runs" language with TurnLedger budget constants: `CHECKER_COST=10`, `REMEDIATION_COST=8`, `REGRESSION_VALIDATION_COST=15`, `CONVERGENCE_PASS_CREDIT=5` (design.md Section 6)
  - Add pre-run guard: `ledger.can_launch()` before each run (point A)
  - Add pre-remediation guard: `ledger.can_remediate()` before each remediation (point E)
  - Replace "halt with diagnostic report" with `ConvergenceResult(halt_reason="convergence_budget_exhausted")` or `"remediation_budget_exhausted"` (design.md Section 2.1)
  - Add acceptance criteria: "TurnLedger is injected, not internally constructed" and "pipeline executor owns budget allocation"
  - Add acceptance criteria for early-exit credit: `ledger.credit(CONVERGENCE_PASS_CREDIT)` on convergence pass before max runs
- **Cross-refs**: FR-7.1 (budget accounting rule), FR-8 (regression debit), FR-9 (remediation debit), Section 5.2 (migration phase 1)
- **Risk**: Budget constants are calibration values; wrong defaults could cause premature halts or uncapped runs. Mitigated by making constants module-level and overridable.

### Section FR-7.1: FR-7/FR-8 Interface Contract

- **Current**: States "regression validation + remediation = 1 budget unit" without defining what a "budget unit" is in TurnLedger terms.
- **Change**: Design.md (Section 2.2, point D) specifies `ledger.debit(REGRESSION_VALIDATION_COST=15)` as a separate debit from the checker suite run. The "1 budget unit" rule means no separate remediation debit follows a regression validation -- they are bundled.
- **Edits**:
  - Rewrite budget accounting rule to reference `ledger.debit(REGRESSION_VALIDATION_COST)` explicitly
  - Clarify: regression validation debit subsumes any post-regression remediation debit for that run
  - Add `handle_regression_fn: Callable` to `execute_fidelity_with_convergence()` signature (design.md Section 1, injectable for testing)
- **Cross-refs**: FR-7 (convergence loop), FR-8 (regression detection)
- **Risk**: If regression validation cost is set too low, the system undercharges for expensive parallel agent work. If too high, a single regression exhausts the budget.

### Section FR-10: Run-to-Run Memory

- **Current**: Describes prior findings summary in semantic prompt but has no concept of economic history or budget state across runs.
- **Change**: Design.md Section 3.2 introduces `reimburse_for_progress()` which logs progress credit events to `result.structural_progress_log`. FR-10 should include ledger snapshots (budget consumed, reimbursed, available) in run metadata for auditability.
- **Edits**:
  - Add to run metadata: `budget_consumed`, `budget_reimbursed`, `budget_available` fields
  - Add to acceptance criteria: "Run metadata includes TurnLedger snapshot at run completion"
  - Add `structural_progress_log` entries to convergence diagnostics
- **Cross-refs**: FR-6 (RunMetadata dataclass), FR-7 (convergence loop)
- **Risk**: Minimal -- additive metadata fields with defaults for backward compatibility.

### Section FR-6: Deviation Registry

- **Current**: RunMetadata includes `structural_high_count`, `semantic_high_count`, `total_high_count` but no budget state.
- **Change**: Design.md's `reimburse_for_progress()` (Section 3.3) compares `structural_high_count` across runs via registry data. RunMetadata must carry budget snapshot fields so convergence decisions are auditable.
- **Edits**:
  - Extend `RunMetadata` dataclass with optional `budget_snapshot: dict | None = None` field
  - Add acceptance criteria: "RunMetadata includes budget snapshot when TurnLedger is active"
- **Cross-refs**: FR-7 (convergence loop reads registry), FR-10 (run-to-run memory)
- **Risk**: Schema migration -- pre-v3.05 registries will lack `budget_snapshot`. Mitigated by `None` default.

### Section 4.2 (Module Disposition, frontmatter)

- **Current**: Lists `convergence.py` as MODIFY with `extends_frs: [FR-6, FR-7, FR-8, FR-10]` but does not mention the TurnLedger import dependency.
- **Change**: Design.md Section 5.4 explicitly addresses the sprint/roadmap import boundary. `convergence.py` will import `TurnLedger` from `sprint/models.py` (conditional, behind `convergence_enabled`).
- **Edits**:
  - Add to `convergence.py` disposition: `imports: [superclaude.cli.sprint.models.TurnLedger]`
  - Add note: "Import is conditional; long-term migration target is `pipeline/models.py`"
  - Add `reimburse_for_progress()` as a new helper function in convergence.py
- **Cross-refs**: Section 5.4 of design.md (import boundary), models.py TurnLedger definition
- **Risk**: Cross-module import couples roadmap to sprint. Acceptable per design.md rationale (TurnLedger is a pure data class). Must not import sprint executor logic.

### Section FR-9: Edit-Only Remediation with Diff-Size Guard

- **Current**: `execute_remediation()` is described as a standalone execution engine with no budget awareness.
- **Change**: Design.md Section 2.1 shows `ledger.debit(REMEDIATION_COST)` before each remediation call (point F). The convergence loop owns the budget; `execute_remediation()` remains budget-unaware.
- **Edits**:
  - Add clarifying note: "The convergence engine debits `REMEDIATION_COST` before calling `execute_remediation()`; the remediation executor itself does not interact with TurnLedger"
  - No changes to `execute_remediation()` signature or behavior
- **Cross-refs**: FR-7 (debit point F), design.md Section 2.1
- **Risk**: None -- this is a clarification, not a behavioral change.

---

## New Sections Required

### NEW: Appendix D — TurnLedger Budget Constants and Calibration

- **Purpose**: Centralizes the cost constants from design.md Section 6 as normative spec content.
- **Content**: Table of `CHECKER_COST`, `REMEDIATION_COST`, `REGRESSION_VALIDATION_COST`, `CONVERGENCE_PASS_CREDIT` with derived budgets (`MIN_CONVERGENCE_BUDGET=28`, `STD_CONVERGENCE_BUDGET=46`, `MAX_CONVERGENCE_BUDGET=61`). States that constants are module-level in `convergence.py` and overridable via `TurnLedger(initial_budget=N)`.

### NEW: Appendix E — Reimbursement Rate Activation

- **Purpose**: Documents the first production consumer of `reimbursement_rate=0.8` (design.md Section 3).
- **Content**: Specifies `reimburse_for_progress()` helper semantics: partial credit when structural HIGHs decrease between runs; no credit on stall; no credit + extra debit on regression. Maps to design.md Section 3.2 scenario table.

### NEW: FR-7 Acceptance Criteria Additions (inline, not separate section)

- `execute_fidelity_with_convergence()` accepts `ledger: TurnLedger` parameter
- `execute_fidelity_with_convergence()` accepts `run_checkers`, `run_remediation`, `handle_regression_fn` as injectable callables
- Pipeline executor constructs TurnLedger with `MAX_CONVERGENCE_BUDGET` when `convergence_enabled=true`
- Legacy mode (`convergence_enabled=false`) never constructs a TurnLedger

---

## Sections Unchanged

| Section | Reason |
|---------|--------|
| FR-1 (Structural Checkers) | No budget interaction; checkers are stateless callables |
| FR-2 (Spec Parser) | Pure data extraction; no budget concept |
| FR-3 (Severity Rules) | Static rule table; no budget interaction |
| FR-4 (Semantic Layer) | Budget is prompt-size budget (NFR-3), not turn budget |
| FR-4.1 (Debate Protocol) | Token budget is separate from TurnLedger turn budget |
| FR-4.2 (Prompt Budget) | Prompt byte budget is orthogonal to TurnLedger |
| FR-5 (Sectional Comparison) | Chunking strategy; no budget interaction |
| FR-8 (Regression Detection) | Called via `handle_regression()`; internal mechanics unchanged. Debit happens in FR-7 before the call. |
| FR-9.1 (`--allow-regeneration`) | CLI flag; no budget interaction |
| NFR-1 through NFR-7 | All unchanged; TurnLedger integration is implementation-level |
| US-1 through US-6 | User stories remain valid as-is; TurnLedger is infrastructure beneath them |
| Appendix A (Architecture) | Diagrams show convergence loop; TurnLedger is an internal detail |
| Appendix B (Checkability Evidence) | Static evidence table |
| Appendix C (Amendment Traceability) | Historical record |

---

## Interaction Effects

1. **reimbursement_rate activation order**: Cross-release summary recommends v3.1 first (gate-pass reimbursement), then v3.05 (convergence progress credit). If v3.05 ships before v3.1, `reimburse_for_progress()` becomes the *first* production consumer of `reimbursement_rate`. Both are valid; they operate on different code paths.

2. **TurnLedger location**: Design.md Section 5.4 imports from `sprint/models.py`. Cross-release summary recommends migrating TurnLedger to `pipeline/models.py`. If migration happens before v3.05, the import path changes. The spec should reference TurnLedger by class name, not module path, to be migration-safe.

3. **Budget isolation vs unified economy**: Design.md Section 4.4 enforces strict isolation between convergence budget and legacy budget. Brainstorm Proposal 2 (Unified Remediation Economy) would collapse this isolation. The refactoring plan follows Proposal 1 (shim), preserving isolation. Switching to Proposal 2 later requires rewriting FR-7 budget isolation language.

4. **`attempt_remediation()` reuse**: Analyze.md Finding 3 identifies `attempt_remediation()` in `trailing_gate.py` as the strongest integration point. Design.md does NOT use it -- convergence calls `execute_remediation()` directly. This is intentional: `attempt_remediation()` has retry-once semantics (2 max), while convergence owns its own retry logic (3 runs). No conflict, but the two remediation paths remain parallel.

5. **ConvergenceBudget composition**: Analyze.md Section 5 recommends a separate `ConvergenceBudget` dataclass for quality-side guardrails (monotonic progress, run counting). Design.md subsumes this into the convergence loop logic itself (registry comparisons, not a separate budget object). The spec should follow design.md: no new `ConvergenceBudget` dataclass. Quality tracking stays in `DeviationRegistry`; resource tracking stays in `TurnLedger`.

---

## Migration / Backward Compatibility Notes

1. **Default behavior unchanged**: `convergence_enabled=False` (default on `RoadmapConfig`) means no TurnLedger is constructed, no new code paths execute, and legacy `_check_remediation_budget()` operates identically to pre-v3.05. Zero behavioral change for non-convergence users.

2. **TurnLedger field defaults preserved**: `reimbursement_rate=0.8`, `minimum_allocation=5`, `minimum_remediation_budget=3` remain unchanged. Convergence mode overrides `minimum_allocation` and `minimum_remediation_budget` via constructor args (design.md Section 4.3).

3. **Registry schema migration**: New `budget_snapshot` field on `RunMetadata` defaults to `None`. Pre-v3.05 registries load without error. New `rule_id`, `spec_quote`, `roadmap_quote` fields on `Finding` default to empty strings (already specified in FR-6).

4. **No existing function signatures change**: `execute_fidelity_with_convergence()` is a new function. `_check_remediation_budget()`, `_print_terminal_halt()`, `execute_remediation()`, `DeviationRegistry`, `ConvergenceResult` -- all unchanged.

5. **Import boundary**: `convergence.py` gains `from superclaude.cli.sprint.models import TurnLedger`. This is a new cross-module dependency. If TurnLedger moves to `pipeline/models.py` in a future release, the import path updates but the integration is unchanged.

6. **Test compatibility**: All existing tests pass without modification. New tests cover the TurnLedger-backed convergence path. The test code in `test_full_flow.py` that manually exercises `reimbursement_rate` remains valid and now has a production analog in `reimburse_for_progress()`.
