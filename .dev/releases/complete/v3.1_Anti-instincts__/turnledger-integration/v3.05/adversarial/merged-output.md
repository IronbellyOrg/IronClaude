# Adversarial Compare: v3.05 Deterministic Fidelity Gates <- TurnLedger Integration

**Date**: 2026-03-20
**Plans compared**:
- **Alpha** (Design-First strategy)
- **Beta** (Spec-First strategy)
- **Gamma** (Interleaved strategy)

---

## Consensus (all 3 agree)

These findings appear in all three plans with matching section identification and change nature. **High confidence**.

### C1: FR-7 is the primary integration target
All three plans identify FR-7 (Convergence Gate) as the core section requiring modification, with TurnLedger replacing the bespoke "hard budget of 3 runs" model.

### C2: `execute_fidelity_with_convergence()` gains `ledger: TurnLedger` parameter
All three specify the ledger as an **injected** parameter (not internally constructed), with the pipeline executor owning construction.

### C3: Budget isolation paragraph requires rewrite
All three replace the existing budget isolation paragraph (lines 635-643) with a TurnLedger-backed convergence mode vs. legacy state-file mode dispatch pattern, gated by `convergence_enabled`.

### C4: Cost constants table required
All three specify the same 4 constants (CHECKER_COST=10, REMEDIATION_COST=8, REGRESSION_VALIDATION_COST=15, CONVERGENCE_PASS_CREDIT=5) and 3 derived budgets (MIN=28, STD=46, MAX=61), sourced from design.md Section 6.

### C5: `reimburse_for_progress()` helper specification
All three specify this new helper function in `convergence.py` with identical signature: `(ledger, run_cost, prev_structural_highs, curr_structural_highs) -> int`. All identify this as the first production consumer of `reimbursement_rate=0.8`.

### C6: FR-7.1 budget accounting rule needs TurnLedger expression
All three modify FR-7.1 to express the "regression validation + remediation = 1 budget unit" rule in TurnLedger terms (`ledger.debit(REGRESSION_VALIDATION_COST)`), with budget ownership staying in FR-7 (not FR-8).

### C7: FR-10 gains ledger snapshot fields
All three add `budget_consumed`, `budget_reimbursed`, `budget_available` to run metadata, with backward-compatible defaults.

### C8: Sections FR-1 through FR-5 are unchanged
All three confirm structural checkers, parsers, severity rules, semantic layer, and chunked comparison have no TurnLedger interaction.

### C9: FR-8, FR-9, FR-9.1 are unchanged
All three confirm regression detection and remediation executors remain budget-unaware; the convergence loop owns all debit/credit operations externally.

### C10: NFR-1 through NFR-7, US-1 through US-6 are unchanged
All three confirm non-functional requirements and user stories remain valid as-is (TurnLedger is implementation-level, not user-facing).

### C11: Section 6 (Resolved Questions) and Appendix B/C are unchanged
All three confirm no impact to resolved questions or historical appendices.

### C12: Cross-module import boundary is documented and acceptable
All three document the `convergence.py` -> `sprint/models.py` import as architecturally acceptable (pure data class, conditional import, future migration to `pipeline/models.py`).

### C13: Legacy mode zero-impact guarantee
All three confirm: `convergence_enabled=False` means no TurnLedger constructed, no new code paths execute, all existing tests pass.

### C14: `reimbursement_rate` has two future consumers (v3.05 + v3.1) on different code paths
All three identify the cross-release concern and confirm the two consumers are complementary, not conflicting.

### C15: TurnLedger location migration is out of scope for v3.05
All three note `sprint/models.py` -> `pipeline/models.py` migration is deferred.

---

## Majority Agreement (2 of 3 agree)

### M1: YAML Frontmatter requires `relates_to` and `module_disposition` updates
**Agree**: Beta, Gamma
**Dissent**: Alpha (omits frontmatter modifications entirely)

Beta adds `sprint/models.py` to `relates_to` and a new `IMPORT_ONLY` disposition entry. Gamma adds both `sprint/models.py` and `trailing_gate.py` to `relates_to` and a `CONSUME` disposition entry. Alpha focuses only on Section 4.2 (module disposition in the design frontmatter), not the spec's YAML frontmatter.

**Assessment**: Beta and Gamma are correct. The spec's own YAML frontmatter must reflect the new dependency. Gamma's inclusion of `trailing_gate.py` in `relates_to` is justified by the design referencing it as a pattern source.

### M2: Section 1.2 (Scope Boundary) needs TurnLedger additions
**Agree**: Beta, Gamma
**Dissent**: Alpha (omits Section 1.2 changes)

Both Beta and Gamma add TurnLedger to in-scope and explicitly declare out-of-scope items (TurnLedger class modifications, sprint-level wiring, migration). Alpha skips scope boundary updates entirely.

**Assessment**: Beta and Gamma are correct. Scope boundaries prevent implementers from over-reaching.

### M3: Section 1.3 (v3.0 Baseline) needs TurnLedger rows
**Agree**: Beta, Gamma
**Dissent**: Alpha (omits Section 1.3 changes)

Both add TurnLedger and `reimbursement_rate` to the "Pre-Existing Config & Pipeline Wiring" table. Gamma also adds `check_budget_guard()` from `sprint/executor.py` as a reused pattern.

**Assessment**: Beta and Gamma are correct. Gamma's extra row for `check_budget_guard()` is a useful traceability link.

### M4: FR-7 acceptance criteria for injectable callables
**Agree**: Alpha, Gamma
**Dissent**: Beta (mentions injectable signature in the function spec but does not add a dedicated acceptance criterion)

Alpha adds `run_checkers`, `run_remediation`, `handle_regression_fn` as acceptance criteria. Gamma adds a criterion for "optional callable overrides" enabling unit testing. Beta includes the full signature with these parameters but does not elevate them to separate acceptance criteria.

**Assessment**: Alpha and Gamma are correct. Injectable callables must be testable acceptance criteria, not just signature details.

### M5: Appendix A convergence loop diagram needs TurnLedger annotations
**Agree**: Beta, Gamma
**Dissent**: Alpha (lists Appendix A as unchanged)

Beta identifies the forced change but does not provide replacement content. Gamma provides a complete replacement ASCII diagram with debit/credit annotations at each operation.

**Assessment**: Beta and Gamma are correct. Alpha's classification of Appendix A as unchanged is an error -- the convergence loop diagram must show budget flow.

### M6: Version bump 1.1.0 -> 1.2.0
**Agree**: Beta, Gamma
**Dissent**: Alpha (does not mention version bump)

Both Beta and Gamma recommend bumping the spec version and updating `amendment_source` in YAML frontmatter.

**Assessment**: Beta and Gamma are correct. A spec amendment warrants a version bump.

### M7: FR-6 (Deviation Registry / RunMetadata) needs `budget_snapshot`
**Agree**: Alpha, Beta (indirectly via FR-10 amendment noting RunMetadata is FR-6's concern)
**Dissent**: Gamma (explicitly routes budget snapshot to FR-10 / ConvergenceResult, NOT RunMetadata)

Alpha adds `budget_snapshot: dict | None = None` to the `RunMetadata` dataclass. Beta acknowledges RunMetadata gains budget fields but routes the edit through FR-10. Gamma argues ledger state can be captured in `ConvergenceResult` instead, avoiding `RunMetadata` changes.

**Assessment**: Alpha's approach (RunMetadata with optional field) is most auditable. Gamma's ConvergenceResult approach is viable but less granular for per-run analysis. Alpha wins on auditability.

### M8: Section 4.2 module disposition for `convergence.py`
**Agree**: Alpha, Gamma
**Dissent**: Beta (covers this via frontmatter changes, not design-side module disposition)

Alpha adds import annotation and `reimburse_for_progress()` as new helper to the convergence.py disposition. Gamma adds import annotation via frontmatter. Both agree `convergence.py` disposition must reference TurnLedger import.

**Assessment**: All three effectively agree; the difference is organizational (where the note lives).

---

## Unique Findings (only 1 plan identified)

### U1: Alpha -- `attempt_remediation()` parallel path analysis (Interaction Effect 4)
Alpha identifies that `attempt_remediation()` in `trailing_gate.py` (analyze.md Finding 3) has retry-once semantics (2 max) vs. convergence's own retry logic (3 runs), and explicitly notes these two remediation paths remain parallel by design. Neither Beta nor Gamma surface this distinction.

**Flag**: Valuable insight. Include in merged plan.

### U2: Alpha -- ConvergenceBudget composition rejection (Interaction Effect 5)
Alpha explicitly rejects the separate `ConvergenceBudget` dataclass recommended by analyze.md Section 5, following design.md's approach (quality tracking in DeviationRegistry, resource tracking in TurnLedger). Beta and Gamma do not address this rejected alternative.

**Flag**: Important architectural decision. Include in merged plan.

### U3: Beta -- Interaction effect: FR-7 TurnLedger injection <-> Appendix A diagrams as forced change
Beta uniquely frames the Appendix A diagram update as a "forced change" driven by the FR-7 injection pattern, creating a causal chain. Gamma identifies the same edit but not the causal linkage.

**Flag**: Good traceability reasoning. Include causal framing.

### U4: Beta -- Interaction effect: Section 1.3 baseline <-> FR-7 acceptance criteria traceability
Beta uniquely identifies that the baseline table must list specific TurnLedger methods consumed (`debit()`, `credit()`, `can_launch()`, `can_remediate()`, `reimbursement_rate`) so acceptance criteria are verifiable against the baseline.

**Flag**: Strengthens traceability. Include.

### U5: Beta -- Risk: Over-specification of cost constants
Beta uniquely flags the risk that making cost constants into acceptance criteria "locks them in" and suggests marking them as "recommended defaults." Alpha and Gamma treat them as firm values.

**Flag**: Valid concern. Include as risk note.

### U6: Gamma -- Cross-cutting concern: Budget domain confusion (turns vs runs)
Gamma uniquely identifies the semantic mismatch between TurnLedger's original design (subprocess turn tracking) and v3.05's usage (convergence run budgeting, where each "turn" = 8-15 actual turns). Recommends not referencing raw TurnLedger field names without convergence-domain mapping.

**Flag**: Important maintainability concern. Include.

### U7: Gamma -- Cross-cutting concern: US-5 needs a TurnLedger note
Gamma uniquely identifies that US-5 ("budget exhausted") is slightly incomplete because budget exhaustion can now occur mid-run (not just after 3 runs). Recommends adding a non-breaking note.

**Flag**: Valid. Include as low-priority addition.

### U8: Gamma -- NEW section: Pipeline Executor Wiring specification
Gamma uniquely specifies the exact `executor.py` step 8 dispatch code as a new spec subsection with its own acceptance criteria. Alpha and Beta describe the dispatch pattern within FR-7's budget isolation paragraph but do not elevate it to its own subsection.

**Flag**: Valuable for implementer clarity. Include.

### U9: Gamma -- NEW section: Section 7 Handoff TurnLedger notes
Gamma uniquely recommends appending TurnLedger integration notes to the Handoff section, surfacing cross-release concerns for downstream releases.

**Flag**: Good practice. Include.

### U10: Gamma -- Summary table of all edits with priorities
Gamma uniquely provides a numbered summary table (18 edits, each with location, type, priority). Neither Alpha nor Beta provide this.

**Flag**: Excellent for implementation tracking. Include.

### U11: Gamma -- `check_budget_guard()` from sprint/executor.py as reused pattern
Gamma uniquely adds `check_budget_guard()` to the Section 1.3 baseline table as a pattern source for the `can_launch()` guard. Alpha and Beta do not reference this existing function.

**Flag**: Useful traceability. Include.

---

## Contradictions

### X1: FR-7.1 Budget Accounting Rule -- bundled vs. separate debits

**Alpha**: "The '1 budget unit' rule means no separate remediation debit follows a regression validation -- they are bundled."

**Gamma**: "A regression validation debits REGRESSION_VALIDATION_COST from the TurnLedger. [...] The subsequent remediation (if any) debits REMEDIATION_COST separately. Both debits are charged against the same TurnLedger instance."

**Beta**: "No separate debit occurs for post-regression remediation within the same budget unit."

**Analysis**: Alpha and Beta agree (bundled). Gamma contradicts (separate debits). The design.md Section 2.2 point D specifies `REGRESSION_VALIDATION_COST` as subsuming the remediation within that cycle. Gamma's walk-through example (Run 2: debit(CHECKER_COST=10) + regression -> debit(REGRESSION_VALIDATION_COST=15)) does NOT show a separate REMEDIATION_COST debit for that run, which is consistent with the bundled interpretation despite Gamma's prose.

**Resolution**: Alpha/Beta interpretation is correct. REGRESSION_VALIDATION_COST subsumes post-regression remediation within the same run. Gamma's prose contradicts its own example; the example is correct.

### X2: FR-6 (Deviation Registry) -- changed or unchanged?

**Alpha**: Lists FR-6 as requiring modification (add `budget_snapshot` to RunMetadata).

**Beta**: Lists FR-6 as unchanged ("the registry dataclass itself is unchanged [...] this is an additive change to RunMetadata, not to DeviationRegistry itself").

**Gamma**: Lists FR-6 as unchanged, routes budget snapshot to ConvergenceResult or FR-10.

**Analysis**: The contradiction is definitional. RunMetadata is defined within FR-6's acceptance criteria. Alpha treats RunMetadata extension as an FR-6 change. Beta and Gamma treat it as an FR-10 change (since run-to-run memory is FR-10's domain). The design.md says "DeviationRegistry -- no modification needed."

**Resolution**: FR-6 (DeviationRegistry class) is unchanged. RunMetadata gains optional budget fields, documented as an FR-10 amendment (where run metadata is consumed). Alpha's edit content is correct but misplaced -- route it through FR-10.

### X3: Gamma scope boundary -- ConvergenceBudget composition model

**Gamma Section 1.2**: States out-of-scope includes "Extensions (e.g., `max_convergence_runs`, `runs_completed`) are handled by a separate ConvergenceBudget composition model."

**Alpha Interaction Effect 5**: Explicitly rejects a separate `ConvergenceBudget` dataclass, following design.md.

**Analysis**: Gamma's scope boundary language implies a ConvergenceBudget will exist (just out of v3.05 scope). Alpha correctly identifies that design.md subsumes this into the convergence loop logic itself. No separate ConvergenceBudget dataclass is planned.

**Resolution**: Follow Alpha. Rewrite Gamma's out-of-scope to say "Extensions to TurnLedger are out of scope; convergence-specific tracking (run counting, monotonic progress) is handled by the convergence loop and DeviationRegistry, not by a separate budget dataclass."

---

## Completeness Assessment

### Which plan was most thorough?
**Gamma** was the most thorough, identifying 18 distinct edits across the most spec sections (including frontmatter, scope boundary, baseline, FR-7 [6 sub-edits], FR-7.1, FR-10, Appendix A, US-5, Section 7 Handoff), plus 5 cross-cutting concerns and a prioritized summary table.

### Which plan identified the most cross-cutting concerns?
**Gamma** with 5 explicit cross-cutting concerns (reimbursement_rate consumers, TurnLedger location, budget domain confusion, US-5 incompleteness, test strategy). Alpha had 5 interaction effects but some were architectural decisions rather than cross-cutting concerns. Beta had 4 interaction effects with the strongest causal chain reasoning.

### Were any spec sections missed by ALL plans?
1. **Section 7 (Handoff) risk inventory**: None of the plans recommend adding "TurnLedger cross-module import" to the existing key implementation risks list in Section 7. Gamma adds handoff notes but not a risk entry.
2. **Appendix C (Amendment Traceability)**: All three mark this unchanged. However, if the spec bumps to v1.2.0 (as Beta and Gamma recommend), a new row documenting the TurnLedger amendment provenance would be appropriate. Beta notes this as "optional" but none mandate it.
3. **NFR-2 enforcement mechanism change**: All three note NFR-2 (convergence <= 3 runs) is now enforced by TurnLedger, but none suggest amending NFR-2's measurement/verification language to reference `ledger.can_launch()` instead of a run counter.

---

## Merged Refactoring Plan

The authoritative merged plan, resolving contradictions in favor of the most evidence-backed position.

---

### Section: YAML Frontmatter (`relates_to`, `module_disposition`, `version`)

- **Change**: Add new dependency references and version bump.
- **Edits**:
  - Add to `relates_to`:
    ```yaml
    - src/superclaude/cli/sprint/models.py
    - src/superclaude/cli/pipeline/trailing_gate.py
    ```
  - Add to `module_disposition`:
    ```yaml
    - file: src/superclaude/cli/sprint/models.py
      action: CONSUME
      note: "TurnLedger class imported into convergence.py; no modifications to sprint/models.py"
      extends_frs: [FR-7]
    ```
  - Bump version: `1.1.0` -> `1.2.0`
  - Update `amendment_source`: append `turnledger-integration/v3.05/design.md`
- **Cross-refs**: Section 1.3 (baseline), FR-7 (convergence gate)
- **Risk**: Omission degrades traceability but has no behavioral impact. Low risk.

---

### Section 1.2: Scope Boundary

- **Change**: Add TurnLedger as in-scope integration dependency; clarify out-of-scope items.
- **Edits**:
  - Append to in-scope:
    ```
    Budget enforcement for the convergence loop via TurnLedger (imported from
    sprint/models.py as a pure-data economic primitive). The convergence engine
    receives a pre-allocated TurnLedger instance from the pipeline executor;
    it does not construct its own.
    ```
  - Append to out-of-scope:
    ```
    TurnLedger class modifications (consumed as-is). TurnLedger migration to
    pipeline/models.py (future cleanup). Sprint-level budget wiring
    (execute_sprint, execute_phase_tasks). Gate-pass reimbursement activation
    in the sprint loop (v3.1 scope). Convergence-specific tracking (run
    counting, monotonic progress) is handled by the convergence loop and
    DeviationRegistry, not by a separate budget dataclass.
    ```
- **Cross-refs**: FR-7 (convergence gate budget), design.md Section 5.4 (import boundary)
- **Risk**: Without explicit scope, implementers may build redundant budget models or wire TurnLedger into sprint executor.

---

### Section 1.3: v3.0 Baseline

- **Change**: Add TurnLedger to "Pre-Existing Config & Pipeline Wiring" table.
- **Edits**:
  - Add rows to baseline table:
    ```
    | `TurnLedger` class | sprint/models.py:488-525 | FR-7 (convergence budget enforcement) |
    | `TurnLedger.reimbursement_rate=0.8` | sprint/models.py:499 | FR-7 (convergence progress credit -- first production consumer) |
    | `check_budget_guard()` | sprint/executor.py:337-350 | FR-7 (pre-launch guard pattern reused) |
    ```
  - Baseline row must list specific TurnLedger methods consumed: `debit()`, `credit()`, `can_launch()`, `can_remediate()`, `reimbursement_rate`
  - Amend `convergence.py` row: note new import `from superclaude.cli.sprint.models import TurnLedger`
- **Cross-refs**: YAML frontmatter `module_disposition`, FR-7 acceptance criteria
- **Risk**: Low. Informational rows for traceability.

---

### Section 4.2: Module Disposition (frontmatter/design)

- **Change**: Annotate `convergence.py` disposition with TurnLedger import and new helper.
- **Edits**:
  - Add to `convergence.py` disposition: `imports: [superclaude.cli.sprint.models.TurnLedger]`
  - Add note: "Import is conditional; long-term migration target is `pipeline/models.py`"
  - Add `reimburse_for_progress()` as new helper function in convergence.py
- **Cross-refs**: Section 5.4 of design.md (import boundary), models.py TurnLedger definition
- **Risk**: Cross-module import couples roadmap to sprint. Acceptable per design.md (pure data class). Must not import sprint executor logic.

---

### FR-7: Convergence Gate

This is the primary integration target. Six sub-edits required.

#### FR-7 Edit 1: Description and Function Signature

- **Change**: Add TurnLedger description and full function signature to FR-7.
- **Edits**:
  - After "v3.05 adds: `execute_fidelity_with_convergence()` (orchestrator), `handle_regression()` (FR-8 interface)." append description paragraph explaining TurnLedger injection rationale (caller owns budget, pipeline may have consumed budget in steps 1-7, caller may reserve for step 9).
  - Insert full function signature:
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
    ```
- **Cross-refs**: FR-7.1 (handle_regression interface), FR-8, FR-9, design.md Section 1
- **Risk**: Mandatory `ledger` parameter means all callers must construct TurnLedger. Since this is a new function, risk is limited to documentation accuracy.

#### FR-7 Edit 2: Budget Model -- Replace Bespoke with TurnLedger

- **Change**: Replace "Hard budget: Maximum 3 runs" language with TurnLedger budget accounting.
- **Edits**:
  - Replace the G2 budget bullet with TurnLedger-backed description referencing `CHECKER_COST`, `REMEDIATION_COST`, `can_launch()` guard, and module-level constants in `convergence.py`.
- **Cross-refs**: design.md Section 2 (debit/credit points), Section 6 (cost constants)
- **Risk**: Miscalibrated constants could cause premature halts or uncapped runs. MAX_CONVERGENCE_BUDGET=61 covers worst case.

#### FR-7 Edit 3: Budget Isolation -- TurnLedger Dispatch

- **Change**: Replace budget isolation paragraph with TurnLedger convergence vs. legacy dispatch.
- **Edits**:
  - Replace lines 635-643 with:
    - Convergence mode: `TurnLedger` governs all budget decisions; `_check_remediation_budget()` and `_print_terminal_halt()` NOT invoked.
    - Legacy mode: state-file budget governs; TurnLedger NEVER constructed.
    - Mutual exclusion via `convergence_enabled` is the critical invariant.
  - Include pipeline executor dispatch code block showing TurnLedger construction with `MAX_CONVERGENCE_BUDGET`, `CHECKER_COST`, `REMEDIATION_COST`, `reimbursement_rate=0.8`.
- **Cross-refs**: design.md Section 4.4, FR-9, NFR-7
- **Risk**: If both budget systems run simultaneously, double-charging occurs. Mutual exclusion is critical.

#### FR-7 Edit 4: Reimbursement Semantics (NEW SUBSECTION)

- **Change**: Add `reimburse_for_progress()` specification as first production consumer of `reimbursement_rate`.
- **Edits**:
  - Add reimbursement mapping table:
    | Scenario | Ledger Action | Rationale |
    |----------|--------------|-----------|
    | Converges to 0 HIGHs (PASS) | `credit(CONVERGENCE_PASS_CREDIT)` | Early exit; unused runs refunded |
    | Forward progress (fewer structural HIGHs) | `credit(int(CHECKER_COST * reimbursement_rate))` | Convergence working; partial credit |
    | Stalls (same HIGH count) | No credit | No forward progress |
    | Regresses (more structural HIGHs) | No credit + extra debit (FR-8) | Regression costs more than neutral |
  - Add helper function signature and acceptance criteria:
    - `reimburse_for_progress()` defined in `convergence.py`
    - Uses `ledger.reimbursement_rate` (not hardcoded fraction)
    - Returns 0 when `curr_structural_highs >= prev_structural_highs`
    - Calls `ledger.credit()` only when credit > 0
    - Progress credit logged to `ConvergenceResult` diagnostic log
- **Cross-refs**: design.md Section 3, analyze.md Finding 2, FR-10 (progress proof logging)
- **Risk**: If `reimbursement_rate` semantics differ from eventual v3.1 gate-pass reimbursement, two consumers may diverge. Cross-release summary confirms they are complementary (different code paths, different callers).

#### FR-7 Edit 5: Budget Calibration Constants (NEW SUBSECTION)

- **Change**: Add cost constants table and derived budgets.
- **Edits**:
  - Cost constants table:
    | Constant | Value | Purpose |
    |----------|-------|---------|
    | `CHECKER_COST` | 10 turns | Cost per checker suite run (structural + semantic) |
    | `REMEDIATION_COST` | 8 turns | Cost per remediation cycle |
    | `REGRESSION_VALIDATION_COST` | 15 turns | Cost for FR-8 parallel validation (3 agents + debate) |
    | `CONVERGENCE_PASS_CREDIT` | 5 turns | Credit on early convergence pass |
  - Derived budgets table:
    | Budget | Formula | Value | Use Case |
    |--------|---------|-------|----------|
    | `MIN_CONVERGENCE_BUDGET` | CHECKER_COST*2 + REMEDIATION_COST | 28 | Catch + verify, no regression |
    | `STD_CONVERGENCE_BUDGET` | CHECKER_COST*3 + REMEDIATION_COST*2 | 46 | Full 3-run sequence |
    | `MAX_CONVERGENCE_BUDGET` | STD + REGRESSION_VALIDATION_COST | 61 | Full sequence with regression |
  - Note: Constants are module-level in `convergence.py`, overridable via `TurnLedger(initial_budget=N)`.
  - **Risk note** (from Beta): These are **recommended defaults**, not hard requirements. Marking them as acceptance criteria locks in calibration values. Consider acceptance criteria that validate the *existence* and *overridability* of constants rather than their exact values.
- **Cross-refs**: design.md Section 6, FR-7 acceptance criteria

#### FR-7 Edit 6: Acceptance Criteria Additions

- **Change**: Add 12+ TurnLedger-specific acceptance criteria.
- **Edits**:
  ```
  - [ ] `execute_fidelity_with_convergence()` accepts `ledger: TurnLedger` (injected, not internally constructed)
  - [ ] `execute_fidelity_with_convergence()` accepts optional callable overrides (`run_checkers`, `run_remediation`, `handle_regression_fn`) for testing
  - [ ] Pipeline executor constructs TurnLedger with MAX_CONVERGENCE_BUDGET when convergence_enabled=true
  - [ ] Legacy mode (convergence_enabled=false) never constructs a TurnLedger
  - [ ] `_check_remediation_budget()` is NEVER called when convergence_enabled=true
  - [ ] Each convergence run debits CHECKER_COST before running checkers
  - [ ] Each remediation cycle debits REMEDIATION_COST before executing
  - [ ] `ledger.can_launch()` checked before each run; HALT if insufficient budget
  - [ ] `ledger.can_remediate()` checked before each remediation; HALT if insufficient budget
  - [ ] Early convergence pass credits CONVERGENCE_PASS_CREDIT back to ledger
  - [ ] Forward progress credits `int(CHECKER_COST * ledger.reimbursement_rate)` via `reimburse_for_progress()`
  - [ ] `reimburse_for_progress()` helper encapsulates reimbursement policy
  - [ ] `reimbursement_rate` field on TurnLedger is consumed (first production consumer)
  - [ ] Cost constants are module-level in convergence.py and overridable
  - [ ] TurnLedger imported from `superclaude.cli.sprint.models` (documented cross-module import)
  ```
  - Amend existing budget-exhaustion criterion to split into two:
    - `ledger.can_launch()` returns False -> `ConvergenceResult(halt_reason="convergence_budget_exhausted")`
    - `ledger.can_remediate()` returns False -> `ConvergenceResult(halt_reason="remediation_budget_exhausted")`
- **Cross-refs**: All design.md sections, FR-7.1

---

### FR-7 NEW SUBSECTION: Import Boundary Justification

- **Change**: Document the cross-module import as a deliberate architectural decision.
- **Edits**:
  - Add subsection after FR-7 acceptance criteria explaining:
    1. TurnLedger is a pure data class with no sprint-specific dependencies
    2. Import is conditional (convergence mode only)
    3. `trailing_gate` module already imports from pipeline (precedent)
    4. Long-term migration to `pipeline/models.py` tracked by cross-release summary
- **Cross-refs**: design.md Section 5.4, Section 1.2 (scope boundary)
- **Risk**: Without this, reviewers may flag the import as a layering violation.

---

### FR-7 NEW SUBSECTION: Pipeline Executor Wiring

- **Change**: Specify the exact `executor.py` step 8 dispatch for convergence mode.
- **Edits**:
  - Add dispatch code block:
    ```python
    if step.id == "spec-fidelity" and config.convergence_enabled:
        convergence_ledger = TurnLedger(
            initial_budget=MAX_CONVERGENCE_BUDGET,
            minimum_allocation=CHECKER_COST,
            minimum_remediation_budget=REMEDIATION_COST,
            reimbursement_rate=0.8,
        )
        convergence_result = execute_fidelity_with_convergence(
            config=config, registry=registry, ledger=convergence_ledger, ...
        )
    else:
        if _check_remediation_budget(output_dir):
            execute_remediation(...)
    ```
  - Acceptance criteria:
    - Step 8 dispatch constructs TurnLedger only when `convergence_enabled=true`
    - Legacy branch does not import or reference TurnLedger
    - Convergence result mapped to `StepResult` for pipeline consumption
- **Cross-refs**: design.md Section 5.3, FR-7 budget isolation
- **Risk**: If dispatch logic is wrong, either both budget systems run or neither runs.

---

### FR-7.1: FR-7/FR-8 Interface Contract

- **Change**: Express "1 budget unit" rule in TurnLedger terms. Clarify budget ownership.
- **Edits**:
  - Rewrite "Budget Accounting Rule" paragraph:
    - Regression validation debits `REGRESSION_VALIDATION_COST` from TurnLedger
    - This debit **subsumes** any post-regression remediation within the same run (bundled, not separate)
    - `handle_regression()` does NOT perform any ledger operations internally -- budget ownership stays with FR-7
  - Add acceptance criteria:
    - `ledger.debit(REGRESSION_VALIDATION_COST)` called before `handle_regression()` invocation
    - `handle_regression()` does not perform any ledger operations internally
    - No separate remediation debit for post-regression remediation within the same run
  - Add `handle_regression_fn: Callable` to `execute_fidelity_with_convergence()` signature description (injectable for testing)
- **Cross-refs**: FR-7 (budget isolation, convergence loop), FR-8 (regression detection), design.md Section 2.2
- **Risk**: Double-charging if `handle_regression()` independently debits. Ownership boundary must be strictly enforced.

---

### FR-9: Edit-Only Remediation with Diff-Size Guard

- **Change**: Clarification only -- no behavioral change.
- **Edits**:
  - Add clarifying note: "The convergence engine debits `REMEDIATION_COST` before calling `execute_remediation()`; the remediation executor itself does not interact with TurnLedger."
- **Cross-refs**: FR-7 (debit point), design.md Section 2.1
- **Risk**: None. Clarification.

---

### FR-10: Run-to-Run Memory

- **Change**: Add ledger snapshots to run metadata for auditability.
- **Edits**:
  - Add description paragraph: Each run's metadata captures TurnLedger state at completion (consumed, reimbursed, available).
  - Add `RunMetadata` optional field: `budget_snapshot: dict | None = None`
  - Add `structural_progress_log` entries to convergence diagnostics
  - Add acceptance criteria:
    - Run metadata includes ledger snapshot: `budget_consumed`, `budget_reimbursed`, `budget_available` at run completion
    - Progress proof logging includes budget state: `structural: {n} -> {m}, budget: {consumed}/{initial} (reimbursed: {r})`
    - Progress credit events logged with format: "Run N: progress credit C turns (structural X -> Y)"
- **Cross-refs**: FR-6 (RunMetadata dataclass), FR-7 (convergence loop, reimbursement)
- **Risk**: Schema migration -- pre-v3.05 registries will lack `budget_snapshot`. Mitigated by `None` default.

---

### US-5: Budget Exhaustion Note

- **Change**: Add non-breaking note about mid-run budget exhaustion.
- **Edits**:
  - Append note:
    ```
    Note: Budget exhaustion may also occur before all 3 runs complete if
    individual operations (checker suite, remediation, regression validation)
    consume more budget than anticipated. The diagnostic report includes
    TurnLedger state (consumed, reimbursed, available) for root-cause analysis.
    ```
- **Cross-refs**: FR-7 (budget model)
- **Risk**: None. Non-breaking additive note.

---

### Appendix A: Current vs Proposed Architecture

- **Change**: Replace convergence loop diagram with TurnLedger-annotated version.
- **Edits**: Replace "Proposed Convergence Loop Detail" diagram with annotated version showing:
  - Pipeline executor TurnLedger construction (initial_budget=61)
  - `can_launch()` / `debit()` before each run
  - `can_remediate()` / `debit()` before each remediation
  - `reimburse_for_progress()` on forward progress
  - `credit(CONVERGENCE_PASS_CREDIT)` on early pass
  - `debit(REGRESSION_VALIDATION_COST)` on regression detection
  - HALT with diagnostic report on budget exhaustion
- **Cross-refs**: FR-7 (budget model), design.md Section 2.1
- **Risk**: Stale diagram misleads implementers about budget flow.

---

### Section 7: Handoff

- **Change**: Append TurnLedger integration notes for downstream releases.
- **Edits**:
  - Add:
    ```
    TurnLedger integration notes:
    - reimbursement_rate=0.8 activated as first production consumer
    - TurnLedger class itself is NOT modified
    - Cross-release dependency: v3.1 wires gate-pass reimbursement via same field, different code path
    - Future cleanup: TurnLedger migration sprint/models.py -> pipeline/models.py (coordinate with v3.1)
    ```
  - Add risk: "Cross-module import (convergence.py -> sprint/models.py) becomes a one-line fix if TurnLedger migrates"
- **Cross-refs**: Cross-release summary Section 2.3
- **Risk**: Low. Informational.

---

## New Sections Required (merged)

| New Section | Location | Source Plans |
|-------------|----------|-------------|
| Cost Constants & Calibration | FR-7 subsection (inline, not appendix) | All 3 |
| `reimburse_for_progress()` Specification | FR-7 subsection (after cost constants) | All 3 |
| Import Boundary Justification | FR-7 subsection (after acceptance criteria) | Gamma; implicit in Alpha/Beta |
| Pipeline Executor Wiring | FR-7 subsection (after import boundary) | Gamma; described in Alpha/Beta budget isolation |
| Section 7 Handoff Notes | Appended to existing Section 7 | Gamma only |

**Rejected new sections**:
- Separate Appendix D/E for cost constants and reimbursement (Alpha). Merged into FR-7 subsections for locality. Appendices are too distant from the acceptance criteria they support.
- Separate `ConvergenceBudget` dataclass (Gamma scope boundary implied). Rejected per design.md -- quality tracking stays in DeviationRegistry, resource tracking in TurnLedger.

---

## Sections Unchanged (merged, verified by majority)

All three plans agree these sections require NO modification:

| Section | Reason |
|---------|--------|
| Section 1.1 (Evidence) | Problem statement, not solution mechanism |
| Section 2 (Clarified User Goals G1-G6) | User-facing goals; TurnLedger is implementation detail |
| FR-1 (Structural Checkers) | Stateless callables; no budget awareness |
| FR-2 (Spec & Roadmap Parser) | Pure data extraction |
| FR-3 (Anchored Severity Rules) | Static rule tables |
| FR-4 (Residual Semantic Layer) | Called by convergence loop; no budget awareness |
| FR-4.1 (Lightweight Debate Protocol) | Self-contained; uses MAX_PROMPT_BYTES, not TurnLedger |
| FR-4.2 (Prompt Budget Enforcement) | Prompt byte budget orthogonal to turn budget |
| FR-5 (Sectional/Chunked Comparison) | Parsing concern; no budget interaction |
| FR-6 (Deviation Registry) | Registry class unchanged; RunMetadata extension routed through FR-10 |
| FR-8 (Regression Detection) | Called by convergence engine; does not interact with TurnLedger directly |
| FR-9.1 (`--allow-regeneration`) | CLI flag; no budget interaction |
| NFR-1 through NFR-7 | Quality attributes unchanged; TurnLedger is implementation-level |
| US-1 through US-4, US-6 | Observable behavior unchanged |
| Section 6 (Resolved Questions Q1-Q11) | No questions reopened |
| Appendix B (Checkability Evidence) | Empirical analysis; no TurnLedger relevance |
| Appendix C (Amendment Traceability) | Historical record; v1.2.0 amendment tracked separately |

---

## Interaction Effects (merged)

### IE-1: FR-7 Budget Isolation <-> FR-7.1 Interface Contract
The TurnLedger dispatch pattern determines whether `handle_regression()` has budget context. FR-7.1 specifies `handle_regression()` does NOT perform ledger operations. Interaction is clean: FR-7 debits before calling FR-7.1, FR-7.1 returns results, FR-7 decides next action. **Forced change**: FR-7.1's "Budget Accounting Rule" must explicitly state the debit happens in FR-7.

### IE-2: FR-7 Cost Constants <-> FR-10 Progress Proof Logging
Cost constants appear in both FR-7 (enforcement) and FR-10 (logging). If constants change, both must be consistent. **Forced change**: FR-10's progress proof format must reference the same constants.

### IE-3: FR-7 TurnLedger Injection <-> Appendix A Architecture Diagrams
The convergence loop diagram must show debit/credit points. **Forced change**: Amend diagram to annotate budget flow.

### IE-4: Section 1.3 Baseline <-> FR-7 Acceptance Criteria
Baseline table rows create traceability links to acceptance criteria. **Forced change**: Baseline must list specific TurnLedger methods consumed.

### IE-5: `reimbursement_rate` Multiple Future Consumers
v3.05 uses `int(CHECKER_COST * 0.8)` for convergence progress credit. v3.1 will use `floor(actual_turns * 0.8)` for gate-pass reimbursement. Different callers, different base values, same field. **Mitigation**: `reimburse_for_progress()` encapsulates v3.05's interpretation; v3.1 will have its own helper.

### IE-6: TurnLedger Location (sprint vs pipeline)
Cross-module import from `sprint/models.py` becomes cleaner after migration to `pipeline/models.py`. **Mitigation**: Conditional import; document future migration in handoff.

### IE-7: Budget Domain Confusion (Turns vs Runs)
TurnLedger was designed for subprocess turn tracking. v3.05 uses it for convergence run budgeting where each "turn" = 8-15 actual turns. **Mitigation**: Cost constants provide named abstractions. Spec should NOT reference raw TurnLedger field names (`minimum_allocation`) without mapping to convergence-domain concepts.

### IE-8: `attempt_remediation()` Parallel Path
`attempt_remediation()` in `trailing_gate.py` has retry-once semantics (2 max). Convergence owns its own retry logic (3 runs). Two remediation paths remain parallel by design. No conflict.

### IE-9: ConvergenceBudget Composition -- Rejected
analyze.md Section 5 recommends a separate `ConvergenceBudget` dataclass. Design.md subsumes this into convergence loop logic. No new `ConvergenceBudget` dataclass. Quality tracking stays in `DeviationRegistry`; resource tracking stays in `TurnLedger`.

---

## Migration / Backward Compatibility Notes (merged)

### 1. Zero-Impact on Legacy Mode
All TurnLedger code is gated behind `convergence_enabled=true` (default: `false`). When off: no TurnLedger constructed, no new imports triggered, `_check_remediation_budget()` operates identically, state file untouched, all existing tests pass.

### 2. TurnLedger Class Unchanged
v3.05 does NOT add fields or methods to `TurnLedger`. All convergence-specific logic lives in `convergence.py` (new function + helper) and `executor.py` (step 8 dispatch). v3.1 and v3.2 can independently extend TurnLedger without conflict.

### 3. Cross-Module Import Boundary
`convergence.py` imports `TurnLedger` from `superclaude.cli.sprint.models`. New dependency but architecturally acceptable (pure data class, conditional import). If TurnLedger migrates to `pipeline/models.py`, the import path is a one-line fix.

### 4. TurnLedger Field Defaults Preserved
`reimbursement_rate=0.8`, `minimum_allocation=5`, `minimum_remediation_budget=3` remain unchanged. Convergence mode overrides `minimum_allocation` and `minimum_remediation_budget` via constructor args.

### 5. Reimbursement Rate Activation
`reimbursement_rate=0.8` gains its first production consumer. No behavior change to existing code -- field already exists with default, no existing production code reads it.

### 6. Registry Serialization
`DeviationRegistry` serialization unchanged. Budget state carried in `ConvergenceResult` and optional `RunMetadata.budget_snapshot` field (defaults to `None` for backward compat).

### 7. State File Coexistence
Legacy `.roadmap-state.json` untouched. Convergence mode does not read/write it. The two persistence mechanisms are fully isolated by `convergence_enabled`.

### 8. No Existing Function Signatures Change
`execute_fidelity_with_convergence()` is a new function. `_check_remediation_budget()`, `_print_terminal_halt()`, `execute_remediation()`, `DeviationRegistry`, `ConvergenceResult` -- all unchanged.

### 9. Version Bump
Spec version `1.1.0` -> `1.2.0`. Non-breaking amendment (additive changes, no acceptance criteria removed, no behavioral change to legacy mode).

### 10. Cross-Release Execution Order
Recommended order is v3.1 -> v3.2 -> v3.05, but v3.05 is architecturally independent (gated, uses injection not modification). Can land before v3.1 without conflict. Only dependency: if v3.1 migrates TurnLedger, v3.05's import path changes (one-line fix).

### 11. Test Compatibility
All existing tests pass without modification. New tests cover TurnLedger-backed convergence path. Injectable callables (`run_checkers`, `run_remediation`, `handle_regression_fn`) enable testing without live LLM calls.

---

## Edit Summary (prioritized)

| # | Spec Location | Edit Type | Priority | Source |
|---|---------------|-----------|----------|--------|
| 1 | FR-7: function signature | ADD paragraph + signature | High | All 3 |
| 2 | FR-7: budget model (G2 bullet) | REPLACE paragraph | High | All 3 |
| 3 | FR-7: budget isolation | REPLACE paragraph + add dispatch | High | All 3 |
| 4 | FR-7: reimbursement semantics | ADD new subsection | High | All 3 |
| 5 | FR-7: budget calibration constants | ADD new subsection | High | All 3 |
| 6 | FR-7: acceptance criteria | ADD 15 criteria + amend 1 | High | All 3 |
| 7 | FR-7: pipeline executor wiring | ADD new subsection | High | Gamma |
| 8 | FR-7.1: budget accounting rule | REPLACE paragraph + ADD 3 criteria | High | All 3 |
| 9 | FR-7: import boundary justification | ADD new subsection | Medium | Gamma |
| 10 | FR-10: run metadata + progress logging | ADD 3 criteria + 1 paragraph | Medium | All 3 |
| 11 | Section 1.2: scope boundary | ADD 2 paragraphs | Medium | Beta, Gamma |
| 12 | Section 1.3: v3.0 baseline | ADD 3 table rows + 1 annotation | Medium | Beta, Gamma |
| 13 | Appendix A: convergence loop diagram | REPLACE diagram | Medium | Beta, Gamma |
| 14 | Section 4.2: module disposition | ADD import + helper annotations | Medium | Alpha, Gamma |
| 15 | FR-9: clarification note | ADD 1 sentence | Low | Alpha |
| 16 | US-5: budget exhaustion note | ADD note | Low | Gamma |
| 17 | Section 7: handoff notes | ADD paragraph | Low | Gamma |
| 18 | YAML frontmatter: relates_to | ADD 2 entries | Low | Beta, Gamma |
| 19 | YAML frontmatter: module_disposition | ADD 1 CONSUME entry | Low | Beta, Gamma |
| 20 | YAML frontmatter: version bump | 1.1.0 -> 1.2.0 | Low | Beta, Gamma |
