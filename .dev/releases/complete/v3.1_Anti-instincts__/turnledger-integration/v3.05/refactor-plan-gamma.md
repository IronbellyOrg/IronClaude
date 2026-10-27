# Refactoring Plan: Deterministic Fidelity Gates <-- TurnLedger Integration

**Plan version**: gamma
**Date**: 2026-03-20
**Proposal selected**: Proposal 1 — Ledger-Backed Convergence Shim (lowest disruption)
**Source documents**:
- Spec: `deterministic-fidelity-gate-requirements.md` (v1.1.0)
- Design: `turnledger-integration/v3.05/design.md`
- Analysis: `turnledger-integration/v3.05/analyze.md`
- Cross-release summary: `turnledger-integration/cross-release-summary.md`

---

## Sections Requiring Modification

### Section 1.2: Scope Boundary

- **Current content summary**: Defines in-scope (fidelity subsystem refactoring) and out-of-scope (upstream pipeline steps, test strategy, certification). Preserves `spec_patch.py`.
- **Required change**: Add TurnLedger as an in-scope integration dependency. Clarify that `sprint/models.py` is consumed (read-only) by roadmap code via cross-module import.
- **Specific edits**:
  - After the existing "In scope" paragraph, add:
    ```
    **In-scope dependency**: `TurnLedger` from `src/superclaude/cli/sprint/models.py`
    is consumed as a budget enforcement primitive within the convergence engine.
    The convergence engine receives a pre-constructed TurnLedger instance from the
    pipeline executor; it does not construct or modify TurnLedger itself.
    ```
  - Add to "Out of scope":
    ```
    TurnLedger class modifications. TurnLedger is consumed as-is; no fields or
    methods are added. Extensions (e.g., `max_convergence_runs`, `runs_completed`)
    are handled by a separate ConvergenceBudget composition model, NOT by extending
    TurnLedger.
    ```
- **Cross-references**: Section 1.3 (v3.0 Baseline inventory needs TurnLedger), FR-7 (convergence gate budget), design.md Section 5.4 (import boundary)
- **Risk**: If scope boundary omits TurnLedger, implementers may build a redundant custom budget model, duplicating existing infrastructure.

---

### Section 1.3: v3.0 Baseline — Pre-Existing Config & Pipeline Wiring

- **Current content summary**: Lists pre-existing modules to MODIFY (convergence.py, semantic_layer.py, remediate_executor.py), pre-existing config, genuinely new modules, and dead code.
- **Required change**: Add TurnLedger to the "Pre-Existing Config & Pipeline Wiring" table as a consumed external dependency. Add import annotation to the "Pre-Existing Modules (MODIFY)" entry for `convergence.py`.
- **Specific edits**:
  - Add row to "Pre-Existing Config & Pipeline Wiring (no work needed)" table:
    ```
    | `TurnLedger` class | sprint/models.py:488-525 | FR-7 (convergence budget enforcement) |
    | `TurnLedger.reimbursement_rate=0.8` | sprint/models.py:499 | FR-7 (convergence progress credit — first production consumer) |
    | `check_budget_guard()` | sprint/executor.py:337-350 | FR-7 (pre-launch guard pattern reused) |
    ```
  - Amend the `convergence.py` row in "Pre-Existing Modules (MODIFY)" to note new import:
    ```
    Adds import: `from superclaude.cli.sprint.models import TurnLedger`
    ```
- **Cross-references**: FR-7 (convergence gate), design.md Section 5.4 (import boundary justification)
- **Risk**: Without listing TurnLedger as baseline, the module disposition analysis is incomplete, and reviewers may question the cross-module import as unauthorized.

---

### Section `relates_to` (YAML Frontmatter)

- **Current content summary**: Lists 11 files in `src/superclaude/cli/roadmap/` that the spec relates to.
- **Required change**: Add TurnLedger source file and trailing_gate.py (where `attempt_remediation()` lives, referenced by design for remediation integration).
- **Specific edits**:
  - Add to `relates_to`:
    ```yaml
    - src/superclaude/cli/sprint/models.py
    - src/superclaude/cli/pipeline/trailing_gate.py
    ```
- **Cross-references**: Section 1.3 (baseline inventory)
- **Risk**: Minimal. Frontmatter omission has no behavioral impact but degrades traceability.

---

### Section `module_disposition` (YAML Frontmatter)

- **Current content summary**: Lists files to MODIFY, CREATE, DELETE, REMOVE_FROM_MANIFEST with line counts and FR references.
- **Required change**: Add a CONSUME entry for TurnLedger (read-only dependency, not modified).
- **Specific edits**:
  - Add:
    ```yaml
    - file: src/superclaude/cli/sprint/models.py
      action: CONSUME
      note: "TurnLedger class imported into convergence.py; no modifications to sprint/models.py"
      extends_frs: [FR-7]
    ```
- **Cross-references**: Section 1.3, FR-7
- **Risk**: If omitted, implementers may assume TurnLedger is modified, conflicting with cross-release summary recommendation to keep TurnLedger unchanged for v3.05.

---

### FR-7: Convergence Gate

- **Current content summary**: Describes the convergence engine: 3-run loop (catch/verify/backup), monotonic progress, budget exhaustion, regression detection, gate authority model, budget isolation between convergence and legacy modes. 23 acceptance criteria.
- **Required change**: This is the primary integration point. The design.md specifies that TurnLedger replaces the bespoke budget model. Six sub-changes required:

#### FR-7 Edit 1: Function Signature

- **Specific edits**: Add `ledger: TurnLedger` parameter to the `execute_fidelity_with_convergence()` description. After the existing sentence "v3.05 adds: `execute_fidelity_with_convergence()` (orchestrator), `handle_regression()` (FR-8 interface)" (line 586), add:
  ```
  The `execute_fidelity_with_convergence()` function receives a `TurnLedger`
  instance as an injected parameter. The pipeline executor constructs the
  ledger with `initial_budget` calibrated to the convergence workload
  (see Budget Calibration below). The convergence engine does not construct
  its own TurnLedger because:
  1. The pipeline may have consumed budget in steps 1-7 already.
  2. The caller may want to reserve budget for step 9 (certification).
  3. Budget isolation (convergence vs legacy) is enforced by the caller
     choosing whether to pass a ledger at all.
  ```
- **Cross-references**: design.md Section 1 (constructor signature), FR-7 budget isolation paragraph
- **Risk**: If the signature change is wrong (e.g., internally constructed instead of injected), the convergence engine violates separation of concerns and cannot be tested without a pipeline.

#### FR-7 Edit 2: Budget Model — Replace Bespoke with TurnLedger

- **Specific edits**: Replace the "Hard budget: Maximum 3 runs (catch -> verify -> backup)" bullet (line 571, G2 reference) with:
  ```
  **Hard budget**: Maximum 3 convergence runs, enforced via `TurnLedger`
  budget accounting. Each run debits `CHECKER_COST` turns from the ledger;
  remediation between runs debits `REMEDIATION_COST` turns. The ledger's
  `can_launch()` guard replaces bespoke run-count arithmetic. Budget
  constants (CHECKER_COST=10, REMEDIATION_COST=8, REGRESSION_VALIDATION_COST=15,
  CONVERGENCE_PASS_CREDIT=5) are module-level constants in `convergence.py`.
  ```
- **Cross-references**: design.md Section 2 (debit/credit points), Section 6 (cost constants)
- **Risk**: If cost constants are miscalibrated, the ledger may exhaust budget before 3 runs complete. The design.md provides MAX_CONVERGENCE_BUDGET=61 to handle worst case.

#### FR-7 Edit 3: Budget Isolation — TurnLedger Integration

- **Specific edits**: Replace the "Budget isolation" paragraph (lines 635-642) with:
  ```
  **Budget isolation**: Two different budget systems coexist:
  - Convergence mode: TurnLedger governs budget. The pipeline executor
    constructs a `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET,
    minimum_allocation=CHECKER_COST, minimum_remediation_budget=REMEDIATION_COST,
    reimbursement_rate=0.8)` and passes it to
    `execute_fidelity_with_convergence()`. `_check_remediation_budget()` and
    `_print_terminal_halt()` are NOT invoked.
  - Legacy mode: State-file budget governs. TurnLedger is NEVER constructed.
    `_check_remediation_budget()` operates exactly as in pre-v3.05.

  The two budget systems MUST never overlap. `convergence_enabled=true`
  disables the legacy remediation budget check entirely.
  ```
- **Cross-references**: design.md Section 4.4 (budget isolation guarantee), Section 4.2 (TurnLedger equivalent mapping)
- **Risk**: If both budget systems run simultaneously, double-charging occurs and the convergence loop halts prematurely.

#### FR-7 Edit 4: Reimbursement Semantics (NEW SUBSECTION)

- **Specific edits**: Add a new subsection after the "Budget isolation" paragraph:
  ```
  **Convergence progress credit**: When a run demonstrates forward progress
  (fewer structural HIGHs than the previous run), the convergence engine
  credits back a fraction of the run's checker cost via
  `reimburse_for_progress()`. This is the first production consumer of
  `TurnLedger.reimbursement_rate=0.8` (currently dead code — defined on
  models.py:499 but never read by any production path).

  Reimbursement mapping:
  | Scenario | Ledger Action | Rationale |
  |----------|--------------|-----------|
  | Converges to 0 HIGHs (PASS) | `credit(CONVERGENCE_PASS_CREDIT)` | Early exit; unused runs refunded |
  | Forward progress (fewer structural HIGHs) | `credit(int(CHECKER_COST * reimbursement_rate))` | Convergence is working; partial credit |
  | Stalls (same HIGH count) | No credit | No forward progress |
  | Regresses (more structural HIGHs) | No credit + extra debit (FR-8) | Regression costs more than neutral |

  Helper function:
  ```python
  def reimburse_for_progress(
      ledger: TurnLedger,
      run_cost: int,
      prev_structural_highs: int,
      curr_structural_highs: int,
  ) -> int:
      """Credit partial refund when convergence shows forward progress.
      Returns turns credited (0 if no progress).
      Uses ledger.reimbursement_rate as the credit fraction.
      """
  ```
  ```
- **Cross-references**: design.md Section 3 (reimbursement rate semantics), analyze.md Finding 2 (orphaned code)
- **Risk**: If `reimbursement_rate` semantics differ from the eventual v3.1 gate-pass reimbursement, the two consumers may conflict. Cross-release summary confirms they are complementary (different code paths, different callers).

#### FR-7 Edit 5: Budget Calibration Constants (NEW SUBSECTION)

- **Specific edits**: Add after the reimbursement subsection:
  ```
  **Budget calibration**:

  | Constant | Value | Purpose |
  |----------|-------|---------|
  | `CHECKER_COST` | 10 | Turns per checker suite run (structural + semantic) |
  | `REMEDIATION_COST` | 8 | Turns per remediation cycle |
  | `REGRESSION_VALIDATION_COST` | 15 | Turns for FR-8 (3 parallel agents + debate) |
  | `CONVERGENCE_PASS_CREDIT` | 5 | Turns credited on early convergence pass |

  Derived budgets:
  | Budget | Formula | Value |
  |--------|---------|-------|
  | `MIN_CONVERGENCE_BUDGET` | CHECKER_COST*2 + REMEDIATION_COST | 28 |
  | `STD_CONVERGENCE_BUDGET` | CHECKER_COST*3 + REMEDIATION_COST*2 | 46 |
  | `MAX_CONVERGENCE_BUDGET` | STD + REGRESSION_VALIDATION_COST | 61 |

  Constants are module-level in `convergence.py`. The pipeline executor
  may override via `TurnLedger(initial_budget=N)` based on operational
  requirements.
  ```
- **Cross-references**: design.md Section 6 (cost constants)
- **Risk**: Under-budgeting prevents 3 full runs; over-budgeting wastes resources. MAX_CONVERGENCE_BUDGET=61 covers worst case (3 runs + 2 remediations + 1 regression validation).

#### FR-7 Edit 6: Acceptance Criteria Additions

- **Specific edits**: Add the following acceptance criteria to FR-7:
  ```
  - [ ] `execute_fidelity_with_convergence()` accepts a `ledger: TurnLedger` parameter (injected, not internally constructed)
  - [ ] Each convergence run debits `CHECKER_COST` from the ledger before running checkers
  - [ ] Each remediation cycle debits `REMEDIATION_COST` from the ledger before executing
  - [ ] `ledger.can_launch()` is checked before each run; returns HALT if insufficient budget
  - [ ] `ledger.can_remediate()` is checked before each remediation; returns HALT if insufficient budget
  - [ ] Early convergence pass credits `CONVERGENCE_PASS_CREDIT` back to ledger
  - [ ] Forward progress (fewer structural HIGHs) credits `int(CHECKER_COST * ledger.reimbursement_rate)` via `reimburse_for_progress()`
  - [ ] `reimburse_for_progress()` helper encapsulates reimbursement policy (not scattered inline)
  - [ ] `reimbursement_rate` field on TurnLedger is consumed by convergence engine (first production consumer)
  - [ ] Convergence TurnLedger constructed by pipeline executor, not by convergence engine
  - [ ] Cost constants (CHECKER_COST, REMEDIATION_COST, REGRESSION_VALIDATION_COST, CONVERGENCE_PASS_CREDIT) are module-level in convergence.py
  - [ ] TurnLedger imported from `superclaude.cli.sprint.models` (cross-module import; acceptable per design.md Section 5.4)
  ```
- **Cross-references**: All design.md sections
- **Risk**: Missing acceptance criteria means TurnLedger wiring is not testable against the spec.

---

### FR-7.1: FR-7/FR-8 Interface Contract

- **Current content summary**: Specifies `handle_regression()` signature, `RegressionResult` return contract, and the budget accounting rule that regression validation + remediation = 1 budget unit.
- **Required change**: Express the "1 budget unit" rule in TurnLedger terms. Clarify that FR-8 regression validation debits from the same TurnLedger.
- **Specific edits**:
  - Replace the "Budget Accounting Rule" paragraph (lines 712-714):
    ```
    **Budget Accounting Rule**: A regression validation debits
    `REGRESSION_VALIDATION_COST` from the TurnLedger. This debit occurs
    within the same run that triggered regression detection. The subsequent
    remediation (if any) debits `REMEDIATION_COST` separately. Both debits
    are charged against the same TurnLedger instance. Example walk-through:

    Run 1: debit(CHECKER_COST=10) + debit(REMEDIATION_COST=8)
    Run 2: debit(CHECKER_COST=10) + regression detected -> debit(REGRESSION_VALIDATION_COST=15)
    -> 0 HIGHs after debate -> credit(CONVERGENCE_PASS_CREDIT=5) -> PASS
    Total consumed: 43, reimbursed: 5, net: 38 of 61 budget
    ```
  - Add acceptance criterion:
    ```
    - [ ] Regression validation debits `REGRESSION_VALIDATION_COST` from the convergence TurnLedger
    - [ ] No separate debit for post-regression remediation when it is part of the same run
    ```
- **Cross-references**: FR-7 (budget constants), design.md Section 2.3 (walk-through)
- **Risk**: If regression validation is double-debited (once for validation, once for remediation within the same run), the 3-run budget is consumed in 2 runs.

---

### FR-10: Run-to-Run Memory

- **Current content summary**: Each run has access to prior findings and outcomes via the registry. Semantic layer prompt includes prior findings summary.
- **Required change**: Add ledger snapshots to run metadata so reimbursement decisions are auditable.
- **Specific edits**:
  - Add acceptance criterion:
    ```
    - [ ] Run metadata includes ledger snapshot: `budget_consumed`, `budget_reimbursed`, `budget_available` at run completion
    - [ ] Progress credit events logged in `structural_progress_log` with format: "Run N: progress credit C turns (structural X -> Y)"
    ```
  - Add to the existing description paragraph:
    ```
    Each run's metadata additionally captures the TurnLedger state at run
    completion (consumed, reimbursed, available) so budget consumption
    patterns are auditable across runs. This does NOT require modifying
    the `RunMetadata` dataclass if ledger state is captured in the
    `ConvergenceResult` instead.
    ```
- **Cross-references**: FR-7 (reimbursement semantics), design.md Section 3.2 (progress logging)
- **Risk**: Without ledger snapshots in run metadata, post-mortem analysis of budget exhaustion is opaque.

---

### Appendix A: Current vs Proposed Architecture

- **Current content summary**: ASCII diagrams showing current (monolithic LLM) vs proposed (structural checkers + semantic layer + convergence gate) architecture, remediation flow, and convergence loop detail.
- **Required change**: Add TurnLedger annotations to the convergence loop diagram.
- **Specific edits**: Replace the "Proposed Convergence Loop Detail" diagram with:
  ```
  Step 8 (Fidelity Gate) with convergence_enabled=true:
  +---------------------------------------------------+
  | Pipeline executor constructs:                      |
  |   convergence_ledger = TurnLedger(                 |
  |     initial_budget=61,                             |
  |     minimum_allocation=10,                         |
  |     minimum_remediation_budget=8,                  |
  |     reimbursement_rate=0.8)                        |
  |                                                     |
  | execute_fidelity_with_convergence(ledger=...):      |
  |                                                     |
  |  Run 1 (catch):                                     |
  |    ledger.can_launch()? -> ledger.debit(10)         |
  |    Structural checkers (parallel) -> findings       |
  |    Semantic layer (chunked) -> findings             |
  |    -> Registry update                               |
  |    -> 0 active HIGHs? -> credit(5) -> PASS -> exit  |
  |                                                     |
  |  ledger.can_remediate()? -> ledger.debit(8)         |
  |  Remediation (structured patches, diff-guarded)     |
  |                                                     |
  |  Run 2 (verify):                                    |
  |    ledger.can_launch()? -> ledger.debit(10)         |
  |    Checkers -> findings                             |
  |    -> Monotonic check (structural only)             |
  |    -> If regression: ledger.debit(15) + FR-8        |
  |    -> If progress: reimburse_for_progress()         |
  |    -> 0 active HIGHs? -> credit(5) -> PASS -> exit  |
  |                                                     |
  |  ledger.can_remediate()? -> ledger.debit(8)         |
  |  Remediation                                        |
  |                                                     |
  |  Run 3 (backup -- final):                           |
  |    ledger.can_launch()? -> ledger.debit(10)         |
  |    Checkers -> final findings                       |
  |    -> 0 active HIGHs? -> credit(5) -> PASS -> exit  |
  |    -> Else: HALT with diagnostic report             |
  |                                                     |
  |  Pipeline sees: PASS or HALT (never intermediate)   |
  +---------------------------------------------------+
  ```
- **Cross-references**: FR-7 (budget model), design.md Section 2.1 (annotated flow)
- **Risk**: Stale diagram misleads implementers about the budget flow.

---

## New Sections Required

### NEW: FR-7 Subsection — TurnLedger Import Boundary Justification

**Location**: After FR-7 acceptance criteria, before FR-7.1.

**Content**:
```
**Import boundary**: `execute_fidelity_with_convergence()` imports TurnLedger
from `superclaude.cli.sprint.models`. This crosses the sprint/roadmap module
boundary. This is acceptable because:

1. TurnLedger is a pure data class with no sprint-specific dependencies
2. The import is conditional (only when convergence_enabled)
3. The trailing_gate module already imports from pipeline (not sprint-specific)
4. Long-term, TurnLedger should migrate to `superclaude.cli.pipeline.models`
   as a shared economic primitive (out of scope for v3.05; tracked by
   cross-release summary Section 2.3)
```

**Rationale**: The design.md explicitly calls out this import boundary concern (Section 5.4). Omitting it from the spec leaves the cross-module import as an unaddressed architectural decision.

---

### NEW: FR-7 Subsection — Pipeline Executor Wiring

**Location**: After the import boundary justification.

**Content**:
```
**Pipeline executor wiring**: In `executor.py`, step 8 handling gains a
convergence branch:

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
      # Legacy mode: state-file budget, no TurnLedger
      if _check_remediation_budget(output_dir):
          execute_remediation(...)

Acceptance criteria:
- [ ] Step 8 dispatch constructs TurnLedger only when `convergence_enabled=true`
- [ ] Legacy branch does not import or reference TurnLedger
- [ ] Convergence result mapped to `StepResult` for pipeline consumption
```

**Rationale**: The design.md Section 5.3 specifies exact wiring code. Without this in the spec, the integration point between pipeline executor and convergence engine is unspecified.

---

### NEW: Section 7 (Handoff) — TurnLedger Integration Notes

**Location**: Append to existing Section 7 (Handoff).

**Content**:
```
**TurnLedger integration notes**:
- `reimbursement_rate=0.8` activated as first production consumer (convergence
  progress credit)
- TurnLedger class itself is NOT modified; all v3.05-specific budget logic is
  in `convergence.py`
- Cross-release dependency: v3.1 will wire gate-pass reimbursement into
  `execute_phase_tasks()` using the same `reimbursement_rate` field, through a
  different code path (non-conflicting)
- Future cleanup: TurnLedger migration from `sprint/models.py` to
  `pipeline/models.py` should be coordinated with v3.1 (see cross-release
  summary Section 2.3)
```

**Rationale**: Cross-release concerns must be surfaced at handoff so downstream releases can plan accordingly.

---

## Sections Unchanged

The following sections have been verified against the design.md and require NO modification:

| Section | Reason Unchanged |
|---------|-----------------|
| **Section 1.1 (Evidence)** | Describes v3.0 failure modes. TurnLedger integration is a solution mechanism, not a problem statement. |
| **Section 2 (Clarified User Goals)** | G1-G6 are user-facing goals. TurnLedger is an implementation detail invisible to users. |
| **FR-1 (Decomposed Structural Checkers)** | Checkers are pure functions taking (spec, roadmap) -> findings. They have no budget awareness. TurnLedger operates at the convergence loop level above checkers. |
| **FR-2 (Spec & Roadmap Parser)** | Parser extracts structured data. No budget or economic model interaction. |
| **FR-3 (Anchored Severity Rules)** | Severity rules are static lookup tables. No TurnLedger dependency. |
| **FR-4 (Residual Semantic Layer)** | Semantic layer produces findings. Budget enforcement is at the convergence loop level, not within the semantic layer. |
| **FR-4.1 (Lightweight Debate Protocol)** | Debate protocol is self-contained. TurnLedger does not govern debate token budgets (which use `MAX_PROMPT_BYTES`). |
| **FR-4.2 (Prompt Budget Enforcement)** | Prompt budget (30KB) is orthogonal to TurnLedger's turn budget. Different budget domains. |
| **FR-5 (Sectional/Chunked Comparison)** | Section splitting is a parsing concern. No budget interaction. |
| **FR-6 (Deviation Registry)** | Registry stores findings. The design.md explicitly states "DeviationRegistry -- no modification needed" (Section 5.2). Run metadata gains ledger snapshots but this is captured under FR-10, not FR-6. |
| **FR-8 (Regression Detection)** | FR-8 spawns parallel agents and merges results. It is called BY the convergence engine (which owns the ledger). FR-8 itself does not interact with TurnLedger directly; the debit happens in the convergence loop before calling `handle_regression()`. Confirmed by design.md Section 2.1 point (D). |
| **FR-9 (Edit-Only Remediation)** | Remediation executor is a pure execution engine. The design.md explicitly states: "`remediate_executor.py` remains a pure execution engine -- it is not modified for convergence awareness" (design.md FR-7 description). |
| **FR-9.1 (`--allow-regeneration`)** | CLI flag operates at the patch level. No TurnLedger interaction. |
| **Section 4 (Non-Functional Requirements)** | NFR-1 through NFR-7 are quality attributes. TurnLedger does not change any NFR target or measurement. NFR-2 (convergence <= 3 runs) is now enforced by TurnLedger but the requirement itself is unchanged. |
| **US-1 through US-4, US-6** | User stories describe observable behavior. TurnLedger is an internal mechanism. |
| **Section 6 (Resolved Questions)** | All 11 resolved questions remain valid. TurnLedger integration does not reopen any. |
| **Appendix B (Structural Checkability Evidence)** | Empirical analysis of v3.0 failures. No TurnLedger relevance. |
| **Appendix C (v1.1.0 Amendment Traceability)** | Historical record of BF resolutions. TurnLedger is a v1.2.0 amendment, tracked separately. |

---

## Interaction Effects

### Cross-Cutting Concern 1: `reimbursement_rate` Has Multiple Future Consumers

**Affected sections**: FR-7 (v3.05), cross-release summary Section 1

`reimbursement_rate=0.8` is consumed by v3.05 as "convergence progress credit" and will later be consumed by v3.1 as "gate-pass reimbursement." These are complementary (different callers, different code paths) but use the same field with potentially different semantic expectations:

- v3.05: `int(CHECKER_COST * 0.8)` = 8 turns credited when structural HIGHs decrease
- v3.1: `floor(actual_turns * 0.8)` credited when a trailing gate passes

**Mitigation**: The `reimburse_for_progress()` helper encapsulates v3.05's interpretation. v3.1 will have its own helper. Both read `reimbursement_rate` but apply it to different base values. No conflict as long as neither helper modifies the rate.

### Cross-Cutting Concern 2: TurnLedger Location (sprint vs pipeline)

**Affected sections**: Section 1.2 (scope), FR-7 (import), Handoff

TurnLedger currently lives in `sprint/models.py`. The cross-release summary recommends migrating it to `pipeline/models.py` as a shared economic primitive. v3.05 does NOT perform this migration (out of scope) but introduces a cross-module import that becomes cleaner after migration.

**Mitigation**: v3.05 uses a conditional import. Document the future migration in the handoff section so v3.1 can coordinate.

### Cross-Cutting Concern 3: Budget Domain Confusion (Turns vs Runs)

**Affected sections**: FR-7 (budget model), FR-7.1 (budget accounting rule)

TurnLedger was designed for subprocess turn tracking (integer turns). v3.05 uses it for convergence run budgeting (where each "turn" represents a multi-step operation costing 8-15 actual turns). This reinterpretation works because TurnLedger's API is denominated in abstract integer units, but the semantic mismatch could confuse maintainers.

**Mitigation**: The cost constants (CHECKER_COST, REMEDIATION_COST, etc.) provide named abstractions. The spec should NOT reference raw TurnLedger field names (`minimum_allocation`) without mapping them to convergence-domain concepts.

### Cross-Cutting Concern 4: US-5 (Budget Exhausted) Needs TurnLedger Context

**Affected sections**: US-5

US-5 currently says: "3 runs completed without reaching 0 active HIGHs -> halt with diagnostic report." With TurnLedger integration, budget exhaustion can also occur mid-run (e.g., insufficient budget for remediation between runs). The user story is still correct but slightly incomplete.

**Recommendation**: Add a note to US-5 (not a rewrite):
```
**Note**: Budget exhaustion may also occur before all 3 runs complete if
individual operations (checker suite, remediation, regression validation)
consume more budget than anticipated. The diagnostic report includes
TurnLedger state (consumed, reimbursed, available) for root-cause analysis.
```

### Cross-Cutting Concern 5: Test Strategy Implications

**Affected sections**: None directly in spec (spec does not define tests)

The design.md specifies injectable parameters (`run_checkers`, `run_remediation`, `handle_regression_fn`) on `execute_fidelity_with_convergence()`. This enables testing the convergence loop with mock operations and a real TurnLedger, validating budget flow without spawning actual agents. The spec should surface these injection points.

**Recommendation**: Add to FR-7 acceptance criteria:
```
- [ ] `execute_fidelity_with_convergence()` accepts optional callable overrides for checkers, remediation, and regression handling (enables unit testing of budget flow without live LLM calls)
```
(Note: this is already in the design.md constructor signature but not in the spec's acceptance criteria.)

---

## Migration / Backward Compatibility Notes

### 1. Zero-Impact on Legacy Mode

All TurnLedger code is gated behind `convergence_enabled=true` (default: `false`). When the flag is off:
- No TurnLedger is constructed
- No new imports are triggered (conditional import in executor.py)
- `_check_remediation_budget()` and `_print_terminal_halt()` operate unchanged
- State file `.roadmap-state.json` is untouched
- All existing tests pass without modification

### 2. TurnLedger Class Itself Is Unchanged

v3.05 does NOT add fields or methods to `TurnLedger`. All convergence-specific logic lives in:
- `convergence.py` (new function + helper)
- `executor.py` (step 8 dispatch branch)

This means v3.1 and v3.2 can independently extend TurnLedger without conflicting with v3.05.

### 3. Import Boundary

The cross-module import (`roadmap/convergence.py` imports from `sprint/models.py`) is new but architecturally acceptable. TurnLedger is a pure data class with no sprint-specific side effects. The import is conditional. Long-term, TurnLedger should migrate to `pipeline/models.py`.

### 4. Reimbursement Rate Activation

`reimbursement_rate=0.8` gains its first production consumer. This does not change existing behavior because:
- The field already exists with default 0.8
- No existing production code reads it
- Existing tests that exercise it continue to work (they manually compute credits, which matches the new `reimburse_for_progress()` pattern)

### 5. Version Bump

The spec version should bump from `1.1.0` to `1.2.0` to reflect TurnLedger integration as a non-breaking amendment (additive changes, no acceptance criteria removed, no behavioral change to legacy mode).

### 6. Cross-Release Execution Order

Per cross-release summary Section 4, the recommended execution order is v3.1 -> v3.2 -> v3.05. However, v3.05's TurnLedger integration is architecturally independent (gated behind `convergence_enabled`, uses injection not modification). It CAN land before v3.1 without conflict. The only dependency is that if v3.1 migrates TurnLedger to `pipeline/models.py`, v3.05's import path changes (a one-line fix).

---

## Summary of All Edits

| # | Spec Location | Edit Type | Priority |
|---|---------------|-----------|----------|
| 1 | YAML frontmatter `relates_to` | ADD 2 entries | Low |
| 2 | YAML frontmatter `module_disposition` | ADD 1 CONSUME entry | Low |
| 3 | Section 1.2 (Scope Boundary) | ADD 2 paragraphs | Medium |
| 4 | Section 1.3 (v3.0 Baseline) | ADD 3 table rows + 1 annotation | Medium |
| 5 | FR-7 description (function signature) | ADD paragraph | High |
| 6 | FR-7 G2 budget model | REPLACE paragraph | High |
| 7 | FR-7 budget isolation | REPLACE paragraph | High |
| 8 | FR-7 reimbursement semantics | ADD new subsection | High |
| 9 | FR-7 budget calibration | ADD new subsection | High |
| 10 | FR-7 acceptance criteria | ADD 12 criteria | High |
| 11 | FR-7 import boundary | ADD new subsection | Medium |
| 12 | FR-7 pipeline executor wiring | ADD new subsection | High |
| 13 | FR-7.1 budget accounting rule | REPLACE paragraph + ADD 2 criteria | High |
| 14 | FR-10 run metadata | ADD 2 criteria + 1 paragraph | Medium |
| 15 | US-5 note | ADD note | Low |
| 16 | Appendix A convergence loop diagram | REPLACE diagram | Medium |
| 17 | Section 7 handoff | ADD TurnLedger integration notes | Low |
| 18 | YAML frontmatter version | BUMP 1.1.0 -> 1.2.0 | Low |
