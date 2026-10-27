# v3.05 TurnLedger Integration — Execution Tasklist

**Generated**: 2026-03-20
**Source**: `adversarial/merged-output.md` (merged refactoring plan from Alpha/Beta/Gamma adversarial compare)
**Target**: `deterministic-fidelity-gate-requirements.md` (spec v1.1.0 -> v1.2.0)
**Executor**: `/sc:task-unified`

## Summary

| Metric | Value |
|--------|-------|
| **Total tasks** | 24 |
| **Waves** | 6 |
| **Edit tasks** | 17 |
| **Add-section tasks** | 4 |
| **Verify tasks** | 3 |
| **High priority** | 12 |
| **Medium priority** | 8 |
| **Low priority** | 4 |

## Execution Order

```
Wave 1: Frontmatter + Scope + Baseline (no interdependencies)
  └── Verify Wave 1
Wave 2: FR-7 Core Edits (function signature, budget model, budget isolation)
  └── Verify Wave 2
Wave 3: FR-7 New Subsections + FR-7.1 (depend on Wave 2 establishing FR-7 structure)
  └── Verify Wave 3
Wave 4: Downstream FRs + Module Disposition (depend on FR-7 being complete)
  └── Verify Wave 4
Wave 5: Appendix, User Stories, Handoff (depend on FR content being final)
Wave 6: Final Verification (full spec coherence check)
```

---

## Wave 1: Frontmatter, Scope Boundary, Baseline

These tasks modify independent spec sections with no cross-dependencies. All can execute in parallel.

---

### Task W1-01: YAML Frontmatter — Add `relates_to` entries
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: YAML frontmatter (`relates_to` block, lines 10-22)
- **Description**: Append two new entries to the `relates_to` list: `src/superclaude/cli/sprint/models.py` and `src/superclaude/cli/pipeline/trailing_gate.py`. These reflect the new TurnLedger import dependency and the trailing_gate pattern source.
- **Depends on**: none
- **Acceptance criteria**: Both paths appear in `relates_to`; existing entries unchanged; YAML parses cleanly.
- **Risk**: Low. Omission degrades traceability only.
- **Wave**: 1

---

### Task W1-02: YAML Frontmatter — Add `module_disposition` CONSUME entry
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: YAML frontmatter (`module_disposition` block, lines 24-49)
- **Description**: Add a new module_disposition entry for `src/superclaude/cli/sprint/models.py` with `action: CONSUME`, note explaining TurnLedger is imported into convergence.py with no modifications to sprint/models.py, and `extends_frs: [FR-7]`.
- **Depends on**: none
- **Acceptance criteria**: New CONSUME entry present; existing disposition entries unchanged; YAML parses cleanly.
- **Risk**: Low.
- **Wave**: 1

---

### Task W1-03: YAML Frontmatter — Version bump and amendment_source
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: YAML frontmatter (`version` field line 3, `amendment_source` field line 9)
- **Description**: Bump `version` from `"1.1.0"` to `"1.2.0"`. Append `turnledger-integration/v3.05/design.md` to the `amendment_source` field (preserve existing value, make it a list or comma-separated if needed).
- **Depends on**: none
- **Acceptance criteria**: Version reads `1.2.0`; amendment_source references both the adversarial review and the turnledger design.
- **Risk**: Low.
- **Wave**: 1

---

### Task W1-04: Section 1.2 — Add TurnLedger scope boundary
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: Section 1.2 (Scope Boundary, lines 78-91)
- **Description**: Append to **In scope**: "Budget enforcement for the convergence loop via TurnLedger (imported from sprint/models.py as a pure-data economic primitive). The convergence engine receives a pre-allocated TurnLedger instance from the pipeline executor; it does not construct its own." Append to **Out of scope**: "TurnLedger class modifications (consumed as-is). TurnLedger migration to pipeline/models.py (future cleanup). Sprint-level budget wiring (execute_sprint, execute_phase_tasks). Gate-pass reimbursement activation in the sprint loop (v3.1 scope). Convergence-specific tracking (run counting, monotonic progress) is handled by the convergence loop and DeviationRegistry, not by a separate budget dataclass."
- **Depends on**: none
- **Acceptance criteria**: In-scope paragraph mentions TurnLedger injection pattern; Out-of-scope explicitly lists TurnLedger class modifications, migration, sprint wiring, v3.1 scope items, and rejects ConvergenceBudget dataclass. Existing scope text preserved.
- **Risk**: Without explicit scope, implementers may build redundant budget models.
- **Wave**: 1

---

### Task W1-05: Section 1.3 — Add TurnLedger baseline table rows
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: Section 1.3 (v3.0 Baseline), "Pre-Existing Config & Pipeline Wiring" table (lines 107-119)
- **Description**: Add three new rows to the baseline table: (1) `TurnLedger` class at sprint/models.py:488-525 extending FR-7; (2) `TurnLedger.reimbursement_rate=0.8` at sprint/models.py:499 extending FR-7 as first production consumer; (3) `check_budget_guard()` at sprint/executor.py:337-350 extending FR-7 as pre-launch guard pattern. Also add a note listing specific TurnLedger methods consumed: `debit()`, `credit()`, `can_launch()`, `can_remediate()`, `reimbursement_rate`. Amend the `convergence.py` row to note the new import `from superclaude.cli.sprint.models import TurnLedger`.
- **Depends on**: none
- **Acceptance criteria**: Three new rows present in table; methods consumed listed; convergence.py row annotated with import; existing rows unchanged.
- **Risk**: Low. Informational traceability rows.
- **Wave**: 1

---

### Task W1-V: Verify Wave 1
- **Type**: verify
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: Frontmatter, Section 1.2, Section 1.3
- **Description**: Verify all Wave 1 edits: (1) YAML frontmatter parses correctly with new relates_to, module_disposition, version 1.2.0, and amendment_source; (2) Section 1.2 has both in-scope and out-of-scope TurnLedger additions; (3) Section 1.3 has three new baseline rows, method list, and convergence.py annotation. No existing content was removed or altered.
- **Depends on**: W1-01, W1-02, W1-03, W1-04, W1-05
- **Acceptance criteria**: All five edits present; YAML valid; no broken table formatting; no existing content missing.
- **Risk**: None.
- **Wave**: 1

---

## Wave 2: FR-7 Core Edits

These three tasks modify the core FR-7 section. They edit different paragraphs within FR-7 and can execute in parallel, but all must complete before Wave 3 adds new subsections.

---

### Task W2-01: FR-7 Edit 1 — Function signature and TurnLedger description
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: FR-7 (Convergence Gate), after line 586 ("v3.05 adds: ...")
- **Description**: After the existing "v3.05 adds" sentence, append a paragraph explaining TurnLedger injection rationale: the caller owns the budget, the pipeline may have consumed budget in steps 1-7, and the caller may reserve budget for step 9. Then insert the full function signature for `execute_fidelity_with_convergence()` with parameters: `config: RoadmapConfig`, `registry: DeviationRegistry`, `spec_path: Path`, `roadmap_path: Path`, `output_dir: Path`, `ledger: TurnLedger`, plus keyword-only optional callable overrides: `run_checkers`, `run_remediation`, `handle_regression_fn` (all typed with `Callable[...] | None = None`), returning `ConvergenceResult`.
- **Depends on**: none
- **Acceptance criteria**: Description paragraph present explaining injection rationale covering three specific points: (a) caller owns the budget, (b) pipeline may have consumed budget in prior steps 1-7, (c) caller may reserve budget for step 9; full Python signature present as fenced code block; `ledger: TurnLedger` is a required positional parameter; three optional callable overrides are keyword-only.
- **Risk**: Mandatory `ledger` parameter means all callers must construct TurnLedger. Limited risk since this is a new function.
- **Wave**: 2

---

### Task W2-02: FR-7 Edit 2 — Replace bespoke budget model with TurnLedger
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: FR-7, G2 budget bullet (line 571: "Hard budget: Maximum 3 runs")
- **Description**: Replace the "Hard budget: Maximum 3 runs (catch -> verify -> backup)" language with TurnLedger-backed budget accounting. New text should reference: `CHECKER_COST` debit before each run, `REMEDIATION_COST` debit before each remediation, `can_launch()` guard replacing the run counter, and module-level constants defined in `convergence.py`. Preserve the catch/verify/backup semantic framing but express it in budget terms.
- **Depends on**: none
- **Acceptance criteria**: No remaining "3 runs" hard-coded language in the budget bullet; TurnLedger terms (`CHECKER_COST`, `can_launch()`, etc.) used; catch/verify/backup framing preserved as budget scenario descriptions.
- **Risk**: Miscalibrated constants could cause premature halts. MAX_CONVERGENCE_BUDGET=61 covers worst case.
- **Wave**: 2

---

### Task W2-03: FR-7 Edit 3 — Budget isolation dispatch with TurnLedger
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: FR-7, Budget isolation paragraph (lines 635-643)
- **Description**: Replace the existing budget isolation paragraph with TurnLedger convergence vs. legacy dispatch pattern. New content must specify: (1) Convergence mode: `TurnLedger` governs all budget decisions; `_check_remediation_budget()` and `_print_terminal_halt()` NOT invoked. (2) Legacy mode: state-file budget governs; TurnLedger NEVER constructed. (3) Mutual exclusion via `convergence_enabled` is the critical invariant. Include a note that the pipeline executor dispatch code is specified in a dedicated subsection (added in Wave 3).
- **Depends on**: none
- **Acceptance criteria**: Old budget isolation paragraph replaced; convergence mode and legacy mode clearly delineated; mutual exclusion emphasized as critical invariant; `_check_remediation_budget()` and `_print_terminal_halt()` explicitly excluded from convergence mode.
- **Risk**: If both budget systems run simultaneously, double-charging occurs. Mutual exclusion is critical.
- **Wave**: 2

---

### Task W2-V: Verify Wave 2
- **Type**: verify
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: FR-7
- **Description**: Verify all Wave 2 edits: (1) Function signature present with `ledger: TurnLedger` and injectable callables; (2) G2 budget bullet uses TurnLedger terms, not "3 runs" hard-coded; (3) Budget isolation paragraph replaced with dispatch pattern. No existing FR-7 acceptance criteria removed. No content from other FR sections affected.
- **Depends on**: W2-01, W2-02, W2-03
- **Acceptance criteria**: All three edits present; FR-7 section reads coherently; no orphaned references to old budget model.
- **Risk**: None.
- **Wave**: 2

---

## Wave 3: FR-7 New Subsections and FR-7.1 Amendment

These tasks add new subsections to FR-7 and amend FR-7.1. They depend on Wave 2 having established the core FR-7 TurnLedger structure. Tasks within this wave can execute in parallel since they target distinct subsections.

---

### Task W3-01: FR-7 Edit 4 — Reimbursement semantics subsection
- **Type**: add-section
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: FR-7, new subsection after budget isolation
- **Description**: Add a new subsection titled "Reimbursement Semantics" specifying `reimburse_for_progress()` as the first production consumer of `reimbursement_rate`. Include: (1) Reimbursement mapping table with 4 scenarios (converges to 0 HIGHs -> `credit(CONVERGENCE_PASS_CREDIT)`; forward progress -> `credit(int(CHECKER_COST * reimbursement_rate))`; stalls -> no credit; regresses -> no credit + extra debit via FR-8). (2) Helper function signature: `reimburse_for_progress(ledger, run_cost, prev_structural_highs, curr_structural_highs) -> int`. (3) Acceptance criteria: uses `ledger.reimbursement_rate` not hardcoded, returns 0 when no progress, calls `ledger.credit()` only when credit > 0, progress credit logged to diagnostic log.
- **Depends on**: W2-03
- **Acceptance criteria**: Subsection present with mapping table, function signature, and 5+ acceptance criteria; `reimbursement_rate` sourced from ledger, never hardcoded.
- **Risk**: If reimbursement_rate semantics differ from v3.1 gate-pass reimbursement, consumers may diverge. Confirmed complementary (different code paths).
- **Wave**: 3

---

### Task W3-02: FR-7 Edit 5 — Budget calibration constants subsection
- **Type**: add-section
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: FR-7, new subsection after reimbursement semantics
- **Description**: Add a new subsection titled "Budget Calibration Constants" with: (1) Cost constants table: `CHECKER_COST=10`, `REMEDIATION_COST=8`, `REGRESSION_VALIDATION_COST=15`, `CONVERGENCE_PASS_CREDIT=5`. (2) Derived budgets table: `MIN_CONVERGENCE_BUDGET=28`, `STD_CONVERGENCE_BUDGET=46`, `MAX_CONVERGENCE_BUDGET=61` with formulas. (3) Note that constants are module-level in `convergence.py`, overridable via `TurnLedger(initial_budget=N)`. (4) Risk note (from Beta): these are recommended defaults; acceptance criteria should validate existence and overridability rather than exact numeric values.
- **Depends on**: W2-02
- **Acceptance criteria**: Both tables present with correct values and formulas; module-level location noted; overridability noted; risk note about locking in calibration values present.
- **Risk**: Over-specification of constants may lock in calibration. Risk note mitigates.
- **Wave**: 3

---

### Task W3-03: FR-7 Edit 6 — TurnLedger acceptance criteria additions
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: FR-7, Acceptance Criteria block (lines 644-666)
- **Description**: Append 15 new acceptance criteria to the existing FR-7 acceptance criteria list. Criteria cover: (1) `ledger: TurnLedger` injection (not internally constructed); (2) optional callable overrides for testing; (3) pipeline executor constructs TurnLedger with MAX_CONVERGENCE_BUDGET; (4) legacy mode never constructs TurnLedger; (5) `_check_remediation_budget()` never called in convergence mode; (6) CHECKER_COST debit before checkers; (7) REMEDIATION_COST debit before remediation; (8) `can_launch()` checked before each run; (9) `can_remediate()` checked before remediation; (10) early pass credits CONVERGENCE_PASS_CREDIT; (11) forward progress credits via `reimburse_for_progress()`; (12) helper encapsulates reimbursement policy; (13) `reimbursement_rate` consumed as first production consumer; (14) cost constants are module-level and overridable; (15) TurnLedger imported from `superclaude.cli.sprint.models`. Also amend existing budget-exhaustion criterion to split into two: `can_launch()` -> "convergence_budget_exhausted" and `can_remediate()` -> "remediation_budget_exhausted".
- **Depends on**: W2-01, W2-02, W2-03, W3-01, W3-02
- **Acceptance criteria**: 15 new criteria present as unchecked `[ ]` items; existing criteria unchanged; budget-exhaustion criterion split into two distinct halt reasons.
- **Risk**: None. Additive.
- **Wave**: 3

---

### Task W3-04: FR-7 — Import boundary justification subsection
- **Type**: add-section
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: FR-7, new subsection after acceptance criteria
- **Description**: Add a new subsection titled "Import Boundary Justification" documenting the cross-module import as a deliberate architectural decision. Content: (1) TurnLedger is a pure data class with no sprint-specific dependencies; (2) Import is conditional (convergence mode only); (3) `trailing_gate` module already imports from pipeline (precedent); (4) Long-term migration to `pipeline/models.py` tracked by cross-release summary.
- **Depends on**: W2-01
- **Acceptance criteria**: Subsection present with 4 numbered justification points; references design.md Section 5.4 and Section 1.2 scope boundary.
- **Risk**: Without this, reviewers may flag the import as a layering violation.
- **Wave**: 3

---

### Task W3-05: FR-7 — Pipeline executor wiring subsection
- **Type**: add-section
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: FR-7, new subsection after import boundary justification
- **Description**: Add a new subsection titled "Pipeline Executor Wiring" specifying the exact step 8 dispatch code. Include fenced Python code block showing: `if step.id == "spec-fidelity" and config.convergence_enabled:` branch constructing `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET, minimum_allocation=CHECKER_COST, minimum_remediation_budget=REMEDIATION_COST, reimbursement_rate=0.8)` and calling `execute_fidelity_with_convergence()`, else legacy branch calling `_check_remediation_budget()` / `execute_remediation()`. Add 3 acceptance criteria: dispatch constructs TurnLedger only when convergence_enabled; legacy branch does not import/reference TurnLedger; convergence result mapped to StepResult.
- **Depends on**: W2-03
- **Acceptance criteria**: Dispatch code block present; both branches shown; 3 acceptance criteria present; references design.md Section 5.3.
- **Risk**: If dispatch logic is wrong, either both budget systems run or neither runs.
- **Wave**: 3

---

### Task W3-06: FR-7.1 — Budget accounting rule in TurnLedger terms
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: FR-7.1 (FR-7/FR-8 Interface Contract), Budget Accounting Rule paragraph (lines 710-714) and acceptance criteria (lines 721-728)
- **Description**: Rewrite the "Budget Accounting Rule" paragraph to express in TurnLedger terms: regression validation debits `REGRESSION_VALIDATION_COST` from TurnLedger; this debit subsumes post-regression remediation within the same run (bundled, not separate); `handle_regression()` does NOT perform any ledger operations internally — budget ownership stays with FR-7. Add 3 new acceptance criteria: (1) `ledger.debit(REGRESSION_VALIDATION_COST)` called before `handle_regression()` invocation; (2) `handle_regression()` does not perform any ledger operations internally; (3) No separate remediation debit for post-regression remediation within the same run. Add `handle_regression_fn: Callable` to signature description as injectable for testing.
- **Depends on**: W2-01
- **Acceptance criteria**: Budget accounting rule rewritten with TurnLedger debit; "subsumes" language present; 3 new acceptance criteria; handle_regression_fn injectable parameter noted; existing acceptance criteria preserved.
- **Risk**: Double-charging if handle_regression() independently debits. Ownership boundary must be strict.
- **Wave**: 3

---

### Task W3-V: Verify Wave 3
- **Type**: verify
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: FR-7 (all subsections), FR-7.1
- **Description**: Verify all Wave 3 edits: (1) Reimbursement semantics subsection with mapping table and helper spec; (2) Budget calibration constants with both tables and risk note; (3) 15 new acceptance criteria + split budget-exhaustion criterion; (4) Import boundary justification with 4 points; (5) Pipeline executor wiring with dispatch code and 3 criteria; (6) FR-7.1 budget accounting rule rewritten with 3 new criteria. Verify subsection ordering is logical. Verify no existing content was removed.
- **Depends on**: W3-01, W3-02, W3-03, W3-04, W3-05, W3-06
- **Acceptance criteria**: All 6 edits present; subsections ordered logically within FR-7; cross-references between subsections are consistent; no orphaned references.
- **Risk**: None.
- **Wave**: 3

---

## Wave 4: Downstream FRs and Module Disposition

These tasks modify sections outside FR-7 that reference the TurnLedger integration established in Waves 2-3. They can execute in parallel with each other.

---

### Task W4-01: FR-9 — Clarification note on budget non-interaction
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: FR-9 (Edit-Only Remediation), description area (after line 781)
- **Description**: Add a clarifying note: "The convergence engine debits `REMEDIATION_COST` before calling `execute_remediation()`; the remediation executor itself does not interact with TurnLedger." This is a non-behavioral clarification.
- **Depends on**: W3-02 (constants defined)
- **Acceptance criteria**: Clarification note present; no behavioral changes to FR-9; `REMEDIATION_COST` referenced by name.
- **Risk**: None. Clarification only.
- **Wave**: 4

---

### Task W4-02: FR-10 — Ledger snapshots and progress logging
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: FR-10 (Run-to-Run Memory, lines 880-896)
- **Description**: Add to FR-10: (1) Description paragraph explaining each run's metadata captures TurnLedger state at completion (consumed, reimbursed, available). (2) Optional `RunMetadata` field: `budget_snapshot: dict | None = None`. (3) `structural_progress_log` entries for convergence diagnostics. (4) Three new acceptance criteria: run metadata includes ledger snapshot (`budget_consumed`, `budget_reimbursed`, `budget_available`); progress proof logging includes budget state format; progress credit events logged with specific format. Note backward compat via `None` default.
- **Depends on**: W3-01 (reimbursement semantics), W3-02 (constants)
- **Acceptance criteria**: Description paragraph present; `budget_snapshot` field specified with `None` default; 3 new acceptance criteria with format strings; backward compatibility note.
- **Risk**: Schema migration: pre-v3.05 registries lack `budget_snapshot`. Mitigated by `None` default.
- **Wave**: 4

---

### Task W4-03: Section 4.2 — Module disposition annotations
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: Section 4.2 (Module Disposition) — note: this section is in the YAML frontmatter `module_disposition` block, specifically the `convergence.py` entry (lines 25-28)
- **Description**: Amend the `convergence.py` module_disposition entry to add: `imports: [superclaude.cli.sprint.models.TurnLedger]`; a note that import is conditional with long-term migration target `pipeline/models.py`; and `reimburse_for_progress()` as a new helper function. Add these as additional YAML fields or notes within the existing disposition entry.
- **Depends on**: W3-01 (reimburse_for_progress defined)
- **Acceptance criteria**: convergence.py disposition entry shows TurnLedger import; conditional import noted; new helper function listed; existing disposition fields preserved.
- **Risk**: Cross-module import couples roadmap to sprint. Acceptable per design.md (pure data class).
- **Wave**: 4

---

### Task W4-V: Verify Wave 4
- **Type**: verify
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: FR-9, FR-10, module_disposition
- **Description**: Verify all Wave 4 edits: (1) FR-9 has clarification note about REMEDIATION_COST debit; (2) FR-10 has budget_snapshot field, progress logging criteria, and backward compat note; (3) convergence.py disposition annotated with import and new helper. No existing content removed.
- **Depends on**: W4-01, W4-02, W4-03
- **Acceptance criteria**: All three edits present; cross-references to FR-7 constants are consistent.
- **Risk**: None.
- **Wave**: 4

---

## Wave 5: Appendix, User Stories, Handoff

Low-priority additive tasks that depend on all FR content being finalized. Can execute in parallel.

---

### Task W5-01: Appendix A — Replace convergence loop diagram
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: Appendix A, "Proposed Convergence Loop Detail" diagram (lines 1022-1052)
- **Description**: Replace the existing convergence loop ASCII diagram with a TurnLedger-annotated version showing: pipeline executor TurnLedger construction (`initial_budget=61`); `can_launch()` / `debit(CHECKER_COST)` before each run; `can_remediate()` / `debit(REMEDIATION_COST)` before each remediation; `reimburse_for_progress()` on forward progress; `credit(CONVERGENCE_PASS_CREDIT)` on early pass; `debit(REGRESSION_VALIDATION_COST)` on regression detection; HALT with diagnostic report on budget exhaustion. Preserve the Run 1/2/3 structure and overall box format.
- **Depends on**: W3-01, W3-02, W3-05
- **Acceptance criteria**: Diagram shows all 7 debit/credit points enumerated in description (`can_launch()`/`debit(CHECKER_COST)`, `can_remediate()`/`debit(REMEDIATION_COST)`, `reimburse_for_progress()`, `credit(CONVERGENCE_PASS_CREDIT)`, `debit(REGRESSION_VALIDATION_COST)`); TurnLedger construction at top; budget-related annotations at each operation; Run 1/2/3 structure preserved; HALT condition shown.
- **Risk**: Stale diagram misleads implementers about budget flow.
- **Wave**: 5

---

### Task W5-02: US-5 — Budget exhaustion note
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: US-5 (Budget exhausted without convergence, lines 935-938)
- **Description**: Append a non-breaking note: "Note: Budget exhaustion may also occur before all 3 runs complete if individual operations (checker suite, remediation, regression validation) consume more budget than anticipated. The diagnostic report includes TurnLedger state (consumed, reimbursed, available) for root-cause analysis."
- **Depends on**: W3-02 (constants established)
- **Acceptance criteria**: Note appended after existing US-5 text; non-breaking (no change to Given/When/Then); references TurnLedger state fields.
- **Risk**: None. Non-breaking additive note.
- **Wave**: 5

---

### Task W5-03: Section 7 — Handoff TurnLedger integration notes
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: Section 7 (Handoff, lines 965-983)
- **Description**: Append TurnLedger integration notes to the Handoff section. Content: (1) `reimbursement_rate=0.8` activated as first production consumer; (2) TurnLedger class itself is NOT modified; (3) Cross-release dependency: v3.1 wires gate-pass reimbursement via same field, different code path; (4) Future cleanup: TurnLedger migration sprint/models.py -> pipeline/models.py (coordinate with v3.1). Also add risk: "Cross-module import (convergence.py -> sprint/models.py) becomes a one-line fix if TurnLedger migrates."
- **Depends on**: W3-04 (import boundary documented)
- **Acceptance criteria**: 4 integration notes present; risk about cross-module import present; existing handoff content (next steps, completed steps, key risks) preserved.
- **Risk**: Low. Informational.
- **Wave**: 5

---

### Task W5-04: Section 7 — Add TurnLedger cross-module import to key risks
- **Type**: edit
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: Section 7, "Key implementation risks" list (lines 977-982)
- **Description**: Add risk item 6: "Cross-module import (convergence.py -> sprint/models.py) — one-line migration fix if TurnLedger moves to pipeline/models.py; tracked in handoff notes." This was identified by the completeness assessment as missed by all three plans.
- **Depends on**: W5-03
- **Acceptance criteria**: New risk item #6 present in key risks list; references migration path.
- **Risk**: None. Informational.
- **Wave**: 5

---

## Wave 6: Final Verification

---

### Task W6-V: Full spec coherence verification
- **Type**: verify
- **Target file**: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- **Section**: Entire document
- **Description**: Full-document verification: (1) YAML frontmatter parses cleanly at v1.2.0; (2) All TurnLedger terms used consistently (`CHECKER_COST`, `REMEDIATION_COST`, `REGRESSION_VALIDATION_COST`, `CONVERGENCE_PASS_CREDIT`, `MAX_CONVERGENCE_BUDGET`); (3) FR-7 subsection ordering is logical; (4) Cross-references between FR-7, FR-7.1, FR-9, FR-10, Section 1.2, Section 1.3, Appendix A, Section 7 are all consistent; (5) No sections listed as "unchanged" in the merged plan were accidentally modified (FR-1 through FR-5, FR-6, FR-8, FR-9.1, NFR-1 through NFR-7, US-1 through US-4, US-6, Section 6, Appendix B, Appendix C); (6) Legacy mode zero-impact guarantee: search for any unconditional TurnLedger references that would execute in legacy mode; (7) Budget accounting rule in FR-7.1 uses "subsumes" (bundled) interpretation, NOT separate debits; (8) No reference to a separate ConvergenceBudget dataclass anywhere in the spec.
- **Depends on**: W5-01, W5-02, W5-03, W5-04
- **Acceptance criteria**: All 8 verification checks pass; document reads coherently end-to-end; no contradictions between sections.
- **Risk**: None.
- **Wave**: 6

---

## Cross-Cutting Notes for Executors

### Contradiction Resolutions (from merged plan — apply consistently)

1. **FR-7.1 bundled debits**: `REGRESSION_VALIDATION_COST` subsumes post-regression remediation. Do NOT add separate `REMEDIATION_COST` debit for post-regression remediation within the same run.
2. **FR-6 unchanged**: `DeviationRegistry` class is NOT modified. `RunMetadata.budget_snapshot` is routed through FR-10, not FR-6.
3. **No ConvergenceBudget dataclass**: Convergence-specific tracking lives in the convergence loop and DeviationRegistry, not a separate budget model.

### Interaction Effects to Monitor

- IE-1: FR-7 budget isolation must be consistent with FR-7.1 interface contract (debit happens in FR-7, not FR-7.1).
- IE-2: Cost constants in FR-7 subsection must match references in FR-10 progress logging.
- IE-3: Appendix A diagram must reflect the FR-7 TurnLedger injection pattern.
- IE-4: Baseline table rows (W1-05) must trace to FR-7 acceptance criteria — verify AC references match method list.
- IE-5: `reimbursement_rate` has multiple consumers — v3.05 activates it for convergence-loop reimbursement (`reimburse_for_progress()`), v3.1 wires it for gate-pass reimbursement via a different code path. Cross-version coordination required to ensure semantics remain complementary.
- IE-6: TurnLedger physical location (sprint/models.py) vs. logical consumer (pipeline convergence) — W3-04 documents the boundary justification, W5-03 documents the migration path. Ensure both stay consistent.
- IE-7: Budget domain confusion — use named constants (CHECKER_COST), not raw TurnLedger field names (minimum_allocation), in the spec.
- IE-8: `attempt_remediation` parallel path — no task in this tasklist modifies the remediation executor's internal budget logic. If a future edit touches `attempt_remediation`, verify it does not duplicate TurnLedger debits already handled by the convergence engine (FR-7).
- IE-9: `ConvergenceBudget` rejection — the merged plan explicitly rejects a separate ConvergenceBudget dataclass (contradiction #3). Any future proposal to introduce one must reconcile with the TurnLedger-only decision documented in Section 1.2 out-of-scope and FR-7.

### Unchanged Sections (do NOT modify)

FR-1, FR-2, FR-3, FR-4, FR-4.1, FR-4.2, FR-5, FR-6, FR-8, FR-9.1, NFR-1 through NFR-7, US-1 through US-4, US-6, Section 1.1, Section 2, Section 6, Appendix B, Appendix C.

---

## Post-Reflection Amendments

- **W3-03 dependency addition**: Added W3-01 and W3-02 as explicit dependencies for W3-03. Motivated by DEP-1 (MEDIUM) — W3-03 acceptance criteria reference `reimburse_for_progress()` and `reimbursement_rate` by name, which are defined in W3-01 and W3-02 respectively. Without explicit deps, executor confusion is possible.
- **W2-01 acceptance criteria sharpened**: Enumerated the three specific injection rationale points: (a) caller owns the budget, (b) prior consumption in steps 1-7, (c) step 9 reservation. Motivated by AC-1 (LOW) — the merged plan specifies 3 points but the original AC only said "description paragraph present."
- **W5-01 acceptance criteria sharpened**: Changed "all debit/credit points" to "all 7 debit/credit points enumerated in description" with explicit list. Motivated by AC-3 (LOW) — the original AC was ambiguous about count and identity of debit/credit points.
- **Added IE-4 to Cross-Cutting Notes**: Baseline-to-AC traceability for W1-05 method list. Motivated by G3 — both reflection agents identified this as missing from Cross-Cutting Notes.
- **Added IE-5 to Cross-Cutting Notes**: `reimbursement_rate` multiple-consumer coordination concern between v3.05 and v3.1. Motivated by G3 (MEDIUM priority) — highest-priority missing interaction effect due to cross-version dependency.
- **Added IE-6 to Cross-Cutting Notes**: TurnLedger physical vs. logical location consistency between W3-04 and W5-03. Motivated by G3.
- **Added IE-8 to Cross-Cutting Notes**: `attempt_remediation` parallel path — no task modifies it, but future edits must not duplicate TurnLedger debits. Motivated by G3.
- **Added IE-9 to Cross-Cutting Notes**: `ConvergenceBudget` rejection rationale and cross-reference to scope boundary. Motivated by G3.
- **G1 (NFR-2) and G2 (Appendix C) intentionally not addressed**: Per the merged reflection's own finding, these gaps exist within the merged plan's internal logic (completeness assessment contradicts "Sections Unchanged" table). Accepted as intentionally deferred.

Date: 2026-03-20
