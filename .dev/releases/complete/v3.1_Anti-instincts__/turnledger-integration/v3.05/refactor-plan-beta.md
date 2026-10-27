# Refactoring Plan: Deterministic Spec-Fidelity Gate v1.1.0 <- TurnLedger Integration

**Source spec**: `deterministic-fidelity-gate-requirements.md` (v1.1.0)
**Design source**: `turnledger-integration/v3.05/design.md` (Proposal 1: Ledger-Backed Convergence Shim)
**Date**: 2026-03-20

---

## Sections Requiring Modification

### Section: YAML Frontmatter (`relates_to`, `module_disposition`)

- **Current content summary**: Lists 12 related source files and their dispositions (MODIFY, CREATE, DELETE). Does not reference `sprint/models.py` or `pipeline/trailing_gate.py`.
- **Required change**: The design introduces a cross-module import of `TurnLedger` from `sprint/models.py` into `convergence.py`, and references `trailing_gate.py` as a pattern source (though not directly consumed). The frontmatter must reflect these new dependencies.
- **Specific edits**:
  - Add to `relates_to` list:
    ```yaml
    - src/superclaude/cli/sprint/models.py
    ```
  - Add to `module_disposition`:
    ```yaml
    - file: src/superclaude/cli/sprint/models.py
      action: IMPORT_ONLY
      note: "TurnLedger imported into convergence.py as budget primitive; no modifications to sprint/models.py"
    ```
- **Cross-references**: Section 1.3 (v3.0 Baseline) -- the "Pre-Existing Config & Pipeline Wiring" table may need a row acknowledging TurnLedger's existence.
- **Risk**: If the import boundary is not documented, a future reader may not understand why `convergence.py` imports from `sprint/models.py`, or may incorrectly flag it as a layering violation.

---

### Section 1.2: Scope Boundary

- **Current content summary**: Defines in-scope (fidelity comparison, severity, deviation tracking, remediation, convergence control) and out-of-scope (upstream pipeline steps, test strategy, certification). Mentions `spec_patch.py` coexistence.
- **Required change**: Add `TurnLedger` integration to the in-scope list and note the cross-module import boundary as a deliberate architectural decision.
- **Specific edits**:
  - Append to in-scope paragraph:
    ```
    Budget enforcement for the convergence loop via TurnLedger (imported from
    sprint/models.py as a pure-data economic primitive). The convergence engine
    receives a pre-allocated TurnLedger instance from the pipeline executor;
    it does not construct its own.
    ```
  - Append to out-of-scope paragraph:
    ```
    TurnLedger migration to pipeline/models.py (future cleanup). Sprint-level
    budget wiring (execute_sprint, execute_phase_tasks). Gate-pass reimbursement
    activation in the sprint loop (v3.1 scope).
    ```
- **Cross-references**: FR-7 (convergence gate budget), Section 5.4 of design.md (import boundary justification).
- **Risk**: Without explicit scope boundary documentation, implementers may attempt to wire TurnLedger into the sprint executor as part of v3.05, which is out of scope.

---

### Section 1.3: v3.0 Baseline

- **Current content summary**: Four tables documenting pre-existing modules, config/pipeline wiring, preserved legacy modules, genuinely new modules, and dead code. Verified against commit `f4d9035`.
- **Required change**: Add TurnLedger to the "Pre-Existing Config & Pipeline Wiring" table as a dependency that v3.05 consumes (not modifies).
- **Specific edits**:
  - Add row to "Pre-Existing Config & Pipeline Wiring (no work needed)" table:
    ```
    | `TurnLedger` dataclass | sprint/models.py:488-525 | FR-7 (convergence budget enforcement) |
    ```
  - Add row to "Pre-Existing Config & Pipeline Wiring (no work needed)" table:
    ```
    | `TurnLedger.reimbursement_rate` field | sprint/models.py:499 | FR-7 (convergence progress credit via `reimburse_for_progress()`) |
    ```
- **Cross-references**: Frontmatter `module_disposition`, FR-7 acceptance criteria.
- **Risk**: Low. These are informational rows. Omission only affects traceability.

---

### FR-7: Convergence Gate (Section 3, lines 564-731)

This is the **primary target** of the TurnLedger integration. Multiple sub-sections require modification.

#### FR-7 Description Paragraph

- **Current content summary**: Describes extending `convergence.py` with `execute_fidelity_with_convergence()` and `handle_regression()`. Lists convergence criteria (0 HIGHs, monotonic progress, 3-run budget, regression detection).
- **Required change**: Add TurnLedger as the budget enforcement mechanism, replacing the implicit "hard budget of 3 runs" language with ledger-backed budget accounting.
- **Specific edits**:
  - After "v3.05 adds: `execute_fidelity_with_convergence()` (orchestrator), `handle_regression()` (FR-8 interface)." append:
    ```
    Budget enforcement within the convergence loop is delegated to a `TurnLedger`
    instance injected by the pipeline executor. The convergence engine calls
    `ledger.debit()` for each checker suite run, remediation cycle, and regression
    validation; `ledger.credit()` for convergence progress and early-exit refunds;
    and `ledger.can_launch()` / `ledger.can_remediate()` as pre-operation budget
    guards. This replaces the bespoke run-counting approach with the established
    economic model from `sprint/models.py`.
    ```

#### FR-7 `execute_fidelity_with_convergence()` Signature

- **Current content summary**: The spec mentions the function name but does not provide its full signature (unlike FR-4.1's `validate_semantic_high()` and FR-7.1's `handle_regression()`).
- **Required change**: Add the full function signature from design.md Section 1, including the `ledger: TurnLedger` parameter and injectable test seams.
- **Specific edits**:
  - Insert after the "v3.05 adds" paragraph, before "Gate Authority Model":
    ```
    **Orchestrator Function**:

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
    ```
- **Cross-references**: FR-7.1 (handle_regression interface), FR-8 (regression handling), FR-9 (remediation).
- **Risk**: The signature introduces a mandatory `ledger` parameter. Any caller of `execute_fidelity_with_convergence()` must construct a TurnLedger. Since this is a new function (not modifying existing code), the risk is limited to documentation accuracy.

#### FR-7 Budget Isolation Paragraph (lines 635-643)

- **Current content summary**: States two budget systems coexist (convergence: 3 runs, legacy: 2 attempts) and MUST never overlap. States `_check_remediation_budget()` and `_print_terminal_halt()` are NOT invoked in convergence mode.
- **Required change**: Rewrite to specify that TurnLedger replaces the bespoke run counter in convergence mode, and that TurnLedger is never constructed in legacy mode. Add the dispatch pattern from design.md Section 4.4.
- **Specific edits**:
  - Replace the "Budget isolation" paragraph with:
    ```
    **Budget isolation**: Two different budget systems coexist:
    - Convergence mode: `TurnLedger` governs all budget decisions within the
      convergence loop. `_check_remediation_budget()` and `_print_terminal_halt()`
      are NOT invoked. The pipeline executor constructs a `TurnLedger` with
      `initial_budget` calibrated to the convergence workload (see cost constants
      below) and injects it into `execute_fidelity_with_convergence()`.
    - Legacy mode: State-file budget (`_check_remediation_budget()`) governs
      remediation attempts. TurnLedger is NEVER constructed for the fidelity step.

    The two budget systems MUST never overlap. `convergence_enabled=true` disables
    the legacy remediation budget check; `convergence_enabled=false` prevents
    TurnLedger construction for step 8.

    **Pipeline executor dispatch** (step 8):

    ```python
    if config.convergence_enabled:
        # Convergence mode: TurnLedger governs budget
        convergence_ledger = TurnLedger(
            initial_budget=MAX_CONVERGENCE_BUDGET,
            minimum_allocation=CHECKER_COST,
            minimum_remediation_budget=REMEDIATION_COST,
            reimbursement_rate=0.8,
        )
        result = execute_fidelity_with_convergence(
            config=config, registry=registry, ledger=convergence_ledger, ...
        )
    else:
        # Legacy mode: state-file budget governs
        if _check_remediation_budget(output_dir):
            execute_remediation(...)
    ```
    ```
- **Cross-references**: Section 6 cost constants (new section), FR-9 (remediation), NFR-7 (backward compat).
- **Risk**: If the dispatch pattern is incorrect, either both budget systems run (double-charging) or neither runs (no budget enforcement). The mutual exclusion via `convergence_enabled` is the critical invariant.

#### FR-7 Acceptance Criteria

- **Current content summary**: 22 acceptance criteria covering gate behavior, monotonic progress, budget, regression, pipeline integration, and budget isolation.
- **Required change**: Add TurnLedger-specific acceptance criteria. Amend existing budget-related criteria to reference TurnLedger.
- **Specific edits**:
  - Add after the existing acceptance criteria list:
    ```
    - [ ] `execute_fidelity_with_convergence()` accepts a `ledger: TurnLedger` parameter
    - [ ] `ledger.debit(CHECKER_COST)` called before each checker suite run
    - [ ] `ledger.debit(REMEDIATION_COST)` called before each remediation cycle
    - [ ] `ledger.can_launch()` checked before each run; returns HALT if False
    - [ ] `ledger.can_remediate()` checked before each remediation; returns HALT if False
    - [ ] `reimburse_for_progress()` credits partial refund when structural HIGHs decrease between runs
    - [ ] `reimburse_for_progress()` uses `ledger.reimbursement_rate` as the credit fraction
    - [ ] `CONVERGENCE_PASS_CREDIT` credited via `ledger.credit()` on early convergence pass (before max runs)
    - [ ] TurnLedger is NEVER constructed when `convergence_enabled=False`
    - [ ] `_check_remediation_budget()` is NEVER called when `convergence_enabled=True`
    - [ ] Cost constants (`CHECKER_COST`, `REMEDIATION_COST`, `REGRESSION_VALIDATION_COST`, `CONVERGENCE_PASS_CREDIT`) are module-level in `convergence.py`
    ```
  - Amend existing criterion "If budget exhausted without convergence: halt, write diagnostic report, exit non-zero" to:
    ```
    - [ ] If `ledger.can_launch()` returns False before a run: halt with `ConvergenceResult(halt_reason="convergence_budget_exhausted")`, write diagnostic report, exit non-zero
    - [ ] If `ledger.can_remediate()` returns False before remediation: halt with `ConvergenceResult(halt_reason="remediation_budget_exhausted")`, write diagnostic report, exit non-zero
    ```
- **Cross-references**: FR-7.1 (regression budget accounting), design.md Section 2.2 (debit/credit summary).
- **Risk**: Over-specification of cost constants at the spec level. The constants are calibration defaults; making them acceptance criteria locks them in. Consider marking them as "recommended defaults" rather than hard requirements.

---

### FR-7.1: FR-7/FR-8 Interface Contract (lines 668-731)

- **Current content summary**: Specifies `handle_regression()` calling convention, `RegressionResult` dataclass, lifecycle within convergence loop, budget accounting rule, and ownership boundaries.
- **Required change**: Add TurnLedger charging for regression validation. The design specifies `ledger.debit(REGRESSION_VALIDATION_COST)` when regression is detected (design.md Section 2.1, point D).
- **Specific edits**:
  - In the "Budget Accounting Rule" paragraph, append:
    ```
    The regression validation is charged to the TurnLedger as a single
    `ledger.debit(REGRESSION_VALIDATION_COST)` call before `handle_regression()`
    is invoked. No separate debit occurs for post-regression remediation within
    the same budget unit. The `handle_regression()` function does not call
    `ledger.debit()` internally -- all budget accounting is owned by the
    convergence loop orchestrator.
    ```
  - Add acceptance criterion:
    ```
    - [ ] `ledger.debit(REGRESSION_VALIDATION_COST)` called before `handle_regression()` invocation
    - [ ] `handle_regression()` does not perform any ledger operations internally (budget ownership stays with FR-7)
    ```
- **Cross-references**: FR-7 budget isolation, FR-8 (regression detection), design.md Section 2.1.
- **Risk**: If `handle_regression()` independently debits the ledger, double-charging occurs. The ownership boundary (FR-7 owns budget, FR-8 owns validation) must be strictly enforced.

---

### FR-7 Intra-Loop Remediation Paragraph (lines 629-633)

- **Current content summary**: States `execute_fidelity_with_convergence()` calls `execute_remediation()` between runs. `remediate_executor.py` is a pure execution engine, not convergence-aware.
- **Required change**: Add that remediation is budget-gated via `ledger.can_remediate()` and charged via `ledger.debit(REMEDIATION_COST)`.
- **Specific edits**:
  - Replace "The convergence loop owns the budget (3 runs) and translates remediation results into DeviationRegistry updates." with:
    ```
    The convergence loop owns the budget via `TurnLedger` and gates each
    remediation cycle behind `ledger.can_remediate()`. Each remediation is
    charged as `ledger.debit(REMEDIATION_COST)`. Remediation results are
    translated into `DeviationRegistry` updates by the convergence orchestrator.
    ```
- **Cross-references**: FR-9 (remediation), FR-7 budget isolation.
- **Risk**: Low. This is a precision refinement of existing language.

---

### FR-10: Run-to-Run Memory (lines 880-896)

- **Current content summary**: Describes prior-run access via deviation registry, semantic prompt inclusion of prior findings, and summary bounding (max 50).
- **Required change**: Add ledger state to the run metadata/reporting per design.md and cross-release summary (Section 3, v3.05 recommendation).
- **Specific edits**:
  - Add acceptance criterion:
    ```
    - [ ] Run metadata includes ledger snapshot: `budget_consumed`, `budget_reimbursed`, `budget_available` at run completion
    - [ ] Progress proof logging includes ledger state alongside finding counts: `structural: {n} -> {m}, semantic: {n} -> {m}, budget: {consumed}/{initial}`
    ```
  - Amend the existing progress proof criterion in FR-7 (line 652) to include budget state:
    ```
    - [ ] Progress proof logged with split counts and budget state: `structural: {n} -> {n+1}, semantic: {n} -> {n+1}, budget: {consumed}/{initial} (reimbursed: {r})`
    ```
- **Cross-references**: FR-6 (run metadata), FR-7 (progress proof logging).
- **Risk**: Adding budget state to run metadata may affect registry serialization schema. However, since `RunMetadata` is a typed dataclass (FR-6 acceptance criterion), new fields with defaults are backward-compatible.

---

## New Sections Required

### New: Cost Constants Table (Appendix or within FR-7)

- **Rationale**: The design.md (Section 6) specifies 4 cost constants and 3 derived budget levels that the convergence engine uses. These are calibration defaults referenced by multiple acceptance criteria.
- **Placement**: Either as a new subsection within FR-7 (after the budget isolation paragraph) or as Appendix D.
- **Content**:
  ```
  ### Convergence Budget Constants (Recommended Defaults)

  | Constant | Value | Purpose |
  |----------|-------|---------|
  | `CHECKER_COST` | 10 turns | Cost per checker suite run (structural + semantic) |
  | `REMEDIATION_COST` | 8 turns | Cost per remediation cycle |
  | `REGRESSION_VALIDATION_COST` | 15 turns | Cost for FR-8 parallel validation (3 agents + debate) |
  | `CONVERGENCE_PASS_CREDIT` | 5 turns | Credit on early convergence pass |

  **Derived budgets**:

  | Budget Level | Formula | Value | Use Case |
  |-------------|---------|-------|----------|
  | `MIN_CONVERGENCE_BUDGET` | `CHECKER_COST * 2 + REMEDIATION_COST` | 28 | Catch + verify, no regression |
  | `STD_CONVERGENCE_BUDGET` | `CHECKER_COST * 3 + REMEDIATION_COST * 2` | 46 | Full 3-run sequence |
  | `MAX_CONVERGENCE_BUDGET` | `STD + REGRESSION_VALIDATION_COST` | 61 | Full sequence with regression handling |

  Constants are module-level in `convergence.py`. The pipeline executor may override
  via `TurnLedger(initial_budget=N)` based on operational requirements.
  ```
- **Cross-references**: FR-7 acceptance criteria, FR-7.1 budget accounting, design.md Section 6.

### New: `reimburse_for_progress()` Helper Specification

- **Rationale**: The design.md (Section 3.3) specifies a helper function that encapsulates the reimbursement policy. This is the first production consumer of `TurnLedger.reimbursement_rate`.
- **Placement**: Within FR-7 (after the convergence budget constants), or as a sub-requirement FR-7.2.
- **Content**:
  ```
  **Progress Reimbursement Helper**:

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
  ```

  **Reimbursement policy**:

  | Scenario | Reimbursement | Rationale |
  |----------|--------------|-----------|
  | Run converges to 0 HIGHs (PASS) | `credit(CONVERGENCE_PASS_CREDIT)` | Early-exit credit; unused runs refunded |
  | Fewer structural HIGHs than previous run | `credit(int(CHECKER_COST * reimbursement_rate))` | Forward progress rewarded |
  | Same HIGH count (stall) | No credit | No progress; budget fully consumed |
  | More structural HIGHs (regression) | No credit + extra debit for FR-8 | Regression costs more than neutral |

  **Acceptance Criteria**:
  - [ ] `reimburse_for_progress()` defined in `convergence.py`
  - [ ] Uses `ledger.reimbursement_rate` (not a hardcoded fraction)
  - [ ] Returns 0 when `curr_structural_highs >= prev_structural_highs`
  - [ ] Calls `ledger.credit()` only when credit > 0
  - [ ] Progress credit logged to `ConvergenceResult` diagnostic log
  ```
- **Cross-references**: FR-7 (convergence gate), FR-10 (progress proof logging), design.md Section 3.2-3.3.

---

## Sections Unchanged

### Section 1.1: Evidence
- **Reasoning**: Documents failure modes from v3.0 runs. TurnLedger integration does not change the problem statement or evidence base.

### Section 2: Clarified User Goals (G1-G6)
- **Reasoning**: All 6 goals (determinism, convergence, edit preservation, anchored severity, scalability, auditability) remain valid. TurnLedger changes the *implementation mechanism* for G2 (convergence) but not the goal itself.

### FR-1: Decomposed Structural Checkers
- **Reasoning**: Checkers are stateless callables that take `(spec_path, roadmap_path) -> List[Finding]`. They have no budget awareness. The convergence loop calls them; they do not call the ledger.

### FR-2: Spec & Roadmap Parser
- **Reasoning**: Pure extraction logic. No budget or convergence interaction.

### FR-3: Anchored Severity Rules
- **Reasoning**: Deterministic rule tables mapping `(dimension, mismatch_type) -> severity`. No budget interaction.

### FR-4: Residual Semantic Layer
- **Reasoning**: Receives uncovered dimensions, produces findings. Called by the convergence loop but has no budget awareness. The lightweight debate protocol (FR-4.1) and prompt budget enforcement (FR-4.2) are per-finding concerns, not per-run budget concerns.

### FR-5: Sectional/Chunked Comparison
- **Reasoning**: Section splitting and dimension mapping. No budget interaction.

### FR-6: Deviation Registry
- **Reasoning**: The design explicitly states "DeviationRegistry -- no modification needed" (design.md Section 5.2). Run metadata gains budget snapshot fields (handled via FR-10 amendment), but the registry dataclass itself is unchanged. The `RunMetadata` typed dataclass is the correct place for budget fields, which is already an FR-6 acceptance criterion -- but this is an additive change to `RunMetadata`, not to `DeviationRegistry` itself.

### FR-8: Regression Detection & Parallel Validation
- **Reasoning**: FR-8 owns agent spawning, result merging, and adversarial debate. It does not own budget decisions (FR-7.1 ownership boundaries). The only budget interaction is that the convergence loop debits `REGRESSION_VALIDATION_COST` *before* calling `handle_regression()` -- this is documented in the FR-7.1 amendment, not in FR-8. FR-8's acceptance criteria remain unchanged.

### FR-9: Edit-Only Remediation with Diff-Size Guard
- **Reasoning**: `remediate_executor.py` remains a pure execution engine. The convergence loop calls `execute_remediation()` and manages the budget externally. FR-9's patch format, diff-size guard, rollback semantics, and `--allow-regeneration` flag are all unchanged. The only interaction is that the convergence loop gates remediation behind `ledger.can_remediate()` -- but this is FR-7's responsibility, not FR-9's.

### FR-9.1: `--allow-regeneration` Flag
- **Reasoning**: Binary flag on `RoadmapConfig`. No budget interaction.

### Section 4: Non-Functional Requirements (NFR-1 through NFR-7)
- **Reasoning**: All NFRs remain valid. NFR-2 (convergence in 3 runs) is now enforced via TurnLedger budget exhaustion rather than a run counter, but the NFR target and measurement are unchanged. NFR-7 (backward compat) is strengthened by the `convergence_enabled` feature flag gating.

### Section 5: User Stories (US-1 through US-6)
- **Reasoning**: All 6 user stories describe observable behavior, not implementation mechanism. US-5 ("budget exhausted") now maps to `ledger.can_launch() == False` but the user-facing behavior (halt with diagnostic report, exit non-zero) is unchanged.

### Section 6: Resolved Questions (Q1-Q11)
- **Reasoning**: All 11 resolved questions remain valid. None address budget enforcement mechanism. Q8 (SPEC_FIDELITY_GATE coexistence) is compatible with TurnLedger integration since budget isolation is additive to gate authority isolation.

### Section 7: Handoff
- **Reasoning**: Next steps, completed prior steps, and key implementation risks are unchanged. A new risk could be added (TurnLedger cross-module import boundary) but the existing 5 risks remain valid.

### Appendix B: Structural Checkability Evidence
- **Reasoning**: Analysis of real deviations from v3.0 runs. No budget interaction.

### Appendix C: v1.1.0 Amendment Traceability
- **Reasoning**: Documents BF-1 through BF-7 resolutions. TurnLedger integration is a new amendment (not a BF resolution), so this appendix is unchanged. A new row could be added to document the TurnLedger amendment provenance, but this is optional.

---

## Interaction Effects

### FR-7 Budget Isolation <-> FR-7.1 Interface Contract
The TurnLedger dispatch pattern in FR-7 (convergence vs legacy) determines whether `handle_regression()` (FR-7.1) ever has budget context. Since FR-7.1 specifies that `handle_regression()` does NOT perform ledger operations (budget ownership stays with FR-7), the interaction is clean: FR-7 debits before calling FR-7.1, FR-7.1 returns results, FR-7 decides next action.

**Forced change**: FR-7.1's "Budget Accounting Rule" paragraph must explicitly state that the debit happens in FR-7, not in FR-8/`handle_regression()`.

### FR-7 Cost Constants <-> FR-10 Progress Proof Logging
The cost constants (`CHECKER_COST`, `REMEDIATION_COST`, etc.) appear in both FR-7 (budget enforcement) and FR-10 (progress proof logging with budget state). If constants change, both sections must be consistent.

**Forced change**: FR-10's progress proof format must include budget state fields that reference the same constants.

### FR-7 TurnLedger Injection <-> Appendix A Architecture Diagrams
The "Proposed Convergence Loop Detail" diagram in Appendix A does not show TurnLedger debit/credit points.

**Forced change**: Amend the Appendix A convergence loop diagram to annotate debit/credit points at each operation, matching design.md Section 2.1.

### Section 1.3 Baseline <-> FR-7 Acceptance Criteria
Adding TurnLedger to the baseline table creates a traceability link. FR-7 acceptance criteria that reference `ledger.debit()` and `ledger.credit()` must be verifiable against the TurnLedger API in the baseline table.

**Forced change**: Baseline table row must list the specific TurnLedger methods consumed by v3.05 (`debit()`, `credit()`, `can_launch()`, `can_remediate()`, `reimbursement_rate`).

---

## Migration / Backward Compatibility Notes

### 1. Feature Flag Gating
All TurnLedger integration code is gated behind `config.convergence_enabled` (default `False`). When `convergence_enabled=False`:
- No TurnLedger is constructed for step 8
- `_check_remediation_budget()` operates exactly as in pre-v3.05
- No new imports are triggered (conditional import in executor.py)
- All existing tests pass without modification

### 2. Cross-Module Import Boundary
`convergence.py` will import `TurnLedger` from `superclaude.cli.sprint.models`. This crosses the sprint/roadmap module boundary. Acceptable because:
- TurnLedger is a pure dataclass with no sprint-specific dependencies
- Import is conditional (convergence mode only)
- Long-term, TurnLedger should migrate to `pipeline/models.py` (out of scope for v3.05)

### 3. `reimbursement_rate` Activation
v3.05 becomes the first production consumer of `TurnLedger.reimbursement_rate=0.8` via `reimburse_for_progress()`. The field already exists with default `0.8`; no schema change needed. Existing TurnLedger tests continue to pass because `reimbursement_rate` is a read-only field consumed by callers, not by TurnLedger methods internally.

### 4. Registry Serialization
`DeviationRegistry` serialization is unchanged. Budget state is carried in `ConvergenceResult` (returned to the pipeline executor), not persisted in the registry. `RunMetadata` gains optional budget snapshot fields (`budget_consumed`, `budget_reimbursed`, `budget_available`) with defaults for backward compatibility.

### 5. State File Coexistence
The legacy `.roadmap-state.json` state file is untouched. Convergence mode does not read or write it. Legacy mode does not interact with TurnLedger. The two persistence mechanisms are fully isolated by the `convergence_enabled` flag.

### 6. Version Bump
This integration constitutes a spec amendment. Recommended version: `1.1.0 -> 1.2.0`. The frontmatter `amendment_source` field should reference the TurnLedger integration design:
```yaml
amendment_source: "adversarial-design-review (7 blocking findings resolved); turnledger-integration/v3.05/design.md"
```
