# Tasklist Validation: v3.05 Deterministic Fidelity Gates (Agent B)

**Reviewer**: Independent Agent B
**Date**: 2026-03-20
**Tasklist**: `turnledger-integration/v3.05/tasklist.md` (24 tasks, 6 waves)
**Merged Plan**: `turnledger-integration/v3.05/adversarial/merged-output.md` (20 edits)
**Original Spec**: `v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md` (v1.1.0)

---

## Coverage Analysis

### Merged Plan Edit -> Tasklist Mapping

| # | Merged Plan Edit | Tasklist Task(s) | Status |
|---|-----------------|------------------|--------|
| 1 | FR-7 Edit 1: Description + function signature | W2-01 | COVERED |
| 2 | FR-7 Edit 2: Budget model (G2 bullet) | W2-02 | COVERED |
| 3 | FR-7 Edit 3: Budget isolation dispatch | W2-03 | COVERED |
| 4 | FR-7 Edit 4: Reimbursement semantics (NEW SUBSECTION) | W3-01 | COVERED |
| 5 | FR-7 Edit 5: Budget calibration constants (NEW SUBSECTION) | W3-02 | COVERED |
| 6 | FR-7 Edit 6: Acceptance criteria additions | W3-03 | COVERED |
| 7 | FR-7 NEW: Pipeline executor wiring | W3-05 | COVERED |
| 8 | FR-7.1: Budget accounting rule | W3-06 | COVERED |
| 9 | FR-7 NEW: Import boundary justification | W3-04 | COVERED |
| 10 | FR-10: Run metadata + progress logging | W4-02 | COVERED |
| 11 | Section 1.2: Scope boundary | W1-04 | COVERED |
| 12 | Section 1.3: v3.0 baseline | W1-05 | COVERED |
| 13 | Appendix A: Convergence loop diagram | W5-01 | COVERED |
| 14 | Section 4.2: Module disposition | W4-03 | COVERED |
| 15 | FR-9: Clarification note | W4-01 | COVERED |
| 16 | US-5: Budget exhaustion note | W5-02 | COVERED |
| 17 | Section 7: Handoff notes | W5-03 | COVERED |
| 18 | YAML frontmatter: `relates_to` | W1-01 | COVERED |
| 19 | YAML frontmatter: `module_disposition` | W1-02 | COVERED |
| 20 | YAML frontmatter: version bump + amendment_source | W1-03 | COVERED |

### GAPS (merged plan edits with NO matching task)

**None found.** All 20 edits in the merged plan's Edit Summary table have corresponding tasks.

However, the merged plan contains content beyond the 20 numbered edits that deserves scrutiny:

1. **Section 7 key risks list (risk #6)**: The merged plan's Completeness Assessment notes that no plan recommended adding the TurnLedger cross-module import to the existing Section 7 key risks list. The tasklist addresses this via **W5-04** (Add TurnLedger cross-module import to key risks). This is an *additive task not derived from the merged plan's Edit Summary table* -- it comes from the Completeness Assessment gap analysis. This is correct and commendable; the tasklist author identified and closed this gap.

2. **Merged plan "Interaction Effects" section (IE-1 through IE-9)**: These are analytical notes, not discrete edits. The tasklist's "Cross-Cutting Notes for Executors" section (IE-1, IE-2, IE-3, IE-7) captures the actionable subset. IE-4 through IE-9 are either resolved by the edits themselves or are architectural background. **No gap.**

3. **Merged plan "Migration/Backward Compatibility Notes" (11 items)**: These are informational constraints, not edits. They are implicitly encoded in task acceptance criteria (e.g., W2-03 encodes the legacy-mode zero-impact guarantee). **No gap.**

### ORPHANS (tasks with NO matching merged plan edit)

| Task | Assessment |
|------|-----------|
| W1-V, W2-V, W3-V, W4-V, W6-V | Verification tasks -- no merged plan edit expected. Valid. |
| W5-04 | Adds risk item #6 to Section 7 key risks. Sourced from merged plan's Completeness Assessment gap, not the Edit Summary. Valid and well-motivated. |

**No true orphans found.** All non-verification tasks map to merged plan edits or to documented gaps in the Completeness Assessment.

---

## Fidelity Check

### Task Description Accuracy

| Task | Fidelity | Notes |
|------|----------|-------|
| W1-01 | ACCURATE | Correctly specifies both `sprint/models.py` and `trailing_gate.py` per merged plan. |
| W1-02 | ACCURATE | CONSUME action matches merged plan. |
| W1-03 | ACCURATE | Version bump and amendment_source match. |
| W1-04 | ACCURATE | In-scope and out-of-scope text matches merged plan verbatim, including the corrected ConvergenceBudget rejection language from contradiction X3 resolution. |
| W1-05 | ACCURATE | Three rows + method list + convergence.py annotation all present. |
| W2-01 | ACCURATE | Function signature with `ledger: TurnLedger` and 3 keyword-only callable overrides matches merged plan. |
| W2-02 | ACCURATE | References correct constants and `can_launch()` guard. |
| W2-03 | ACCURATE | Convergence vs. legacy dispatch with mutual exclusion. Correctly notes Wave 3 dependency for pipeline executor subsection. |
| W3-01 | ACCURATE | 4-scenario reimbursement table, helper signature, 5+ acceptance criteria all specified. |
| W3-02 | ACCURATE | Both tables (cost constants + derived budgets), module-level note, overridability, Beta's risk note all present. |
| W3-03 | ACCURATE | 15 criteria enumerated; budget-exhaustion split into two halt reasons. |
| W3-04 | ACCURATE | 4 justification points; cross-references to design.md and Section 1.2. |
| W3-05 | ACCURATE | Dispatch code block, both branches, 3 acceptance criteria, design.md reference. |
| W3-06 | ACCURATE | "Subsumes" language, budget ownership, 3 new criteria, handle_regression_fn injectable. Matches X1 contradiction resolution (bundled, not separate). |
| W4-01 | ACCURATE | Clarification-only note with REMEDIATION_COST reference. |
| W4-02 | ACCURATE | budget_snapshot field, progress logging format strings, backward compat note. |
| W4-03 | ACCURATE | Import annotation, conditional import note, reimburse_for_progress() helper. |
| W5-01 | ACCURATE | All debit/credit annotation points listed; Run 1/2/3 structure preserved. |
| W5-02 | ACCURATE | Non-breaking note text matches merged plan. |
| W5-03 | ACCURATE | 4 integration notes + risk about cross-module import. |
| W5-04 | ACCURATE | Risk item #6 with migration reference. |

### Ambiguity / Underspecification Flags

1. **W2-02 (G2 budget bullet replacement)**: The task says "Replace the 'Hard budget: Maximum 3 runs' language" but does not provide exact replacement text. The merged plan also does not provide exact prose -- it lists concepts to include. This is acceptable for a `/sc:task-unified` executor that can compose prose, but is the **most ambiguous task** in the list. The executor must infer the exact wording. **MINOR**: Consider adding a prose template or at minimum specifying that the catch/verify/backup framing must be preserved as named budget scenarios (the task does say "Preserve the catch/verify/backup semantic framing" -- this is sufficient).

2. **W3-03 (15 acceptance criteria)**: The task lists all 15 by number but the executor must format them as `[ ]` checklist items matching the spec's existing convention. The task description does specify "unchecked `[ ]` items" -- **adequate**.

3. **W4-03 (Module disposition annotations)**: The task says "Section 4.2 (Module Disposition)" but then clarifies this is in the YAML frontmatter `module_disposition` block. The original spec has no "Section 4.2" -- the module disposition lives in the YAML frontmatter. The merged plan's "Section 4.2" heading is a reference to the merged plan's own organizational heading, not the spec's structure. The task correctly identifies the target as "the `convergence.py` entry (lines 25-28)" in frontmatter. **The section reference "Section 4.2" could confuse an executor** that looks for a markdown section. However, the line-level targeting mitigates this. **MINOR**.

4. **W5-01 (Appendix A diagram replacement)**: The task describes what the new diagram should show but does not provide the actual ASCII art. The executor must compose a replacement diagram. This is intentional (the merged plan's Gamma provides a template but the merged plan itself does not include it). **ACCEPTABLE** but this is the **highest creative burden** task.

### Divergences from Merged Plan

**W2-03 vs. Merged Plan FR-7 Edit 3**: The merged plan's Edit 3 includes: "Include pipeline executor dispatch code block showing TurnLedger construction." The tasklist's W2-03 does NOT include the dispatch code block -- instead it adds a note that "the pipeline executor dispatch code is specified in a dedicated subsection (added in Wave 3)." This is a **deliberate decomposition decision**: the tasklist splits FR-7 Edit 3 into two parts (W2-03 for the budget isolation concept, W3-05 for the dispatch code). The merged plan bundles both into Edit 3. **The decomposition is valid** -- it avoids a single task doing too much -- but it means W2-03 is not a 1:1 match to merged plan Edit 3. The coverage is complete across W2-03 + W3-05.

**No other divergences found.**

---

## Dependency Validation

### Wave Dependency Graph

```
Wave 1: W1-01, W1-02, W1-03, W1-04, W1-05 (independent) -> W1-V
Wave 2: W2-01, W2-02, W2-03 (independent) -> W2-V
Wave 3: W3-01(->W2-03), W3-02(->W2-02), W3-03(->W2-01,W2-02,W2-03),
         W3-04(->W2-01), W3-05(->W2-03), W3-06(->W2-01) -> W3-V
Wave 4: W4-01(->W3-02), W4-02(->W3-01,W3-02), W4-03(->W3-01) -> W4-V
Wave 5: W5-01(->W3-01,W3-02,W3-05), W5-02(->W3-02), W5-03(->W3-04),
         W5-04(->W5-03) -> W6-V
Wave 6: W6-V(->W5-01,W5-02,W5-03,W5-04)
```

### Forward Dependency Violations

**None found.** No task depends on a task in a later wave. All dependency arrows point backward.

### Missing Dependencies

1. **W3-03 (acceptance criteria) should depend on W3-01 and W3-02**: The task adds criteria about reimbursement (`reimburse_for_progress()`) and cost constants (`CHECKER_COST`, etc.). These criteria reference concepts introduced in W3-01 and W3-02. However, since all three are in the same wave and the criteria are additive (appended to an existing list), the executor can compose them independently. The listed dependencies (W2-01, W2-02, W2-03) are correct as the *hard* dependencies. W3-01 and W3-02 are *co-wave* tasks, not blocking. **Not a violation**, but a subtle interaction to monitor.

2. **W5-04 depends on W5-03**: Correctly listed. W5-04 adds a risk item to the list that W5-03 extends. This is a **within-wave sequential dependency**. The tasklist does not explicitly mark Wave 5 as having an internal ordering constraint. **MINOR GAP**: The Wave 5 header says "Can execute in parallel" but W5-04 depends on W5-03. This should be called out.

### Parallelization Opportunities

- **Wave 1**: All 5 tasks are truly independent. Maximally parallel. Good.
- **Wave 2**: All 3 tasks edit different paragraphs within FR-7. Parallel is correct, though executors must be careful about line-number drift if editing the same file. The tasks target different line ranges (line 586, line 571, lines 635-643). **Acceptable**.
- **Wave 3**: 6 tasks editing different subsections and a different FR (FR-7.1). Parallel is correct.
- **Wave 4**: 3 tasks editing different sections (FR-9, FR-10, frontmatter). Parallel is correct.
- **Wave 5**: 4 tasks, but W5-04 depends on W5-03. The other 3 (W5-01, W5-02, W5-03) can run in parallel, then W5-04 after W5-03. **Could be expressed as Wave 5a + Wave 5b**, but the cost of the extra wave is negligible.
- **Wave 6**: Single verification task. Cannot be parallelized.

**No further parallelization opportunities** beyond the W5-03/W5-04 split noted above.

---

## Spec Consistency

### Internal Consistency of Resulting Spec

1. **FR-7 subsection ordering**: Tasks add 5 new subsections to FR-7. The tasklist specifies ordering: reimbursement semantics -> budget calibration constants -> acceptance criteria additions -> import boundary justification -> pipeline executor wiring. This is **logically sound**: concepts build from specific (reimbursement) to general (import justification) to operational (wiring). The merged plan's "New Sections Required" table specifies a slightly different order (cost constants before reimbursement, import boundary before pipeline wiring). The tasklist's order is: reimbursement (W3-01) then constants (W3-02), which reverses the merged plan's table order. **This is acceptable** -- the subsections are largely self-contained and cross-reference each other regardless of order. However, budget calibration constants are referenced by reimbursement semantics (e.g., `CHECKER_COST` in the reimbursement formula), which argues for constants first. **MINOR NOTE**: Consider swapping W3-01 and W3-02 ordering if subsection placement is sequential in the document.

2. **TurnLedger term consistency**: The tasklist uses consistent terminology throughout: `CHECKER_COST`, `REMEDIATION_COST`, `REGRESSION_VALIDATION_COST`, `CONVERGENCE_PASS_CREDIT`, `MAX_CONVERGENCE_BUDGET`, `can_launch()`, `can_remediate()`, `reimburse_for_progress()`. These match the merged plan exactly. **Consistent.**

3. **Contradiction X1 resolution (bundled debits)**: W3-06 correctly implements the Alpha/Beta "subsumes" interpretation. W3-03 criterion #7 ("Each remediation cycle debits REMEDIATION_COST before executing") applies to intra-loop remediation, NOT post-regression remediation. The distinction is maintained by W3-06 saying "No separate remediation debit for post-regression remediation within the same run." **Consistent but requires executor attention** to ensure criterion #7 and the FR-7.1 subsumes rule don't contradict.

4. **Contradiction X2 resolution (FR-6 unchanged)**: The tasklist correctly routes `budget_snapshot` through FR-10 (W4-02), not FR-6. No task modifies FR-6. **Consistent.**

5. **Contradiction X3 resolution (no ConvergenceBudget)**: W1-04 out-of-scope text explicitly rejects a separate budget dataclass. **Consistent.**

### Unchanged Sections Risk

The tasklist's "Unchanged Sections" list matches the merged plan's "Sections Unchanged" table. Cross-checking against all 24 tasks:

- **FR-1 through FR-5**: No tasks target these. **Safe.**
- **FR-6**: No tasks target FR-6 directly. W4-02 targets FR-10 (RunMetadata), not the DeviationRegistry class. **Safe.**
- **FR-8**: No tasks modify FR-8. W3-06 modifies FR-7.1 (the interface contract), not FR-8 itself. **Safe.**
- **FR-9**: W4-01 adds a clarification note. The merged plan explicitly states "no behavioral change." **Safe** if the executor treats it as additive.
- **FR-9.1**: Not targeted. **Safe.**
- **NFR-1 through NFR-7**: Not targeted. **Safe.** (Note: The merged plan's Completeness Assessment flags that NFR-2's measurement language could be updated to reference `ledger.can_launch()`. The tasklist does not do this, matching the merged plan's decision not to mandate it. **Acceptable gap**.)
- **US-1 through US-4, US-6**: Not targeted. **Safe.**
- **Section 6 (Resolved Questions)**: Not targeted. **Safe.**
- **Appendix B, C**: Not targeted. **Safe.** (Note: Appendix C could gain a v1.2.0 amendment row. The merged plan marks this as optional. The tasklist does not include it. **Acceptable gap**.)

### Acceptance Criteria Convention Alignment

The original spec uses two conventions:
- `[x]` for v3.0 baseline items (pre-satisfied)
- `[ ]` for v3.05 implementation items

The tasklist's W3-03 specifies new criteria as "unchecked `[ ]` items." **Matches convention.**

---

## Risk Assessment

### Highest Execution Risk Tasks

| Rank | Task | Risk | Blast Radius |
|------|------|------|-------------|
| 1 | **W2-03** (Budget isolation rewrite) | Replaces the most safety-critical paragraph in FR-7. If convergence/legacy mutual exclusion is not expressed clearly, the spec permits double-charging. | HIGH -- downstream tasks W3-05 (wiring) and W4-01 (FR-9 clarification) depend on this being correct. |
| 2 | **W5-01** (Appendix A diagram replacement) | Highest creative burden -- executor must compose ASCII art from scratch. If the diagram misrepresents budget flow, implementers will build wrong logic. | MEDIUM -- diagram is informational but heavily referenced during implementation. |
| 3 | **W3-03** (15 acceptance criteria) | Largest single task by content volume. If any criterion contradicts another or contradicts FR-7.1's bundled-debit rule, the spec becomes internally inconsistent. | HIGH -- acceptance criteria are the executable contract. |
| 4 | **W2-02** (G2 budget bullet replacement) | Most ambiguous task (no exact prose provided). If the executor preserves "3 runs" language while also introducing TurnLedger budget language, the spec will contain two contradictory budget models. | MEDIUM -- the acceptance criterion "No remaining '3 runs' hard-coded language" mitigates. |
| 5 | **W3-06** (FR-7.1 budget accounting rule) | Must correctly implement X1 contradiction resolution. If "subsumes" is misinterpreted, post-regression remediation gets double-charged. | MEDIUM -- but failure is a spec-level logic error, not just a formatting issue. |

### Tasks That Should Be Split

1. **W3-03 (15 criteria + split budget-exhaustion)**: This task does two things: (a) append 15 new criteria and (b) amend an existing criterion (split budget-exhaustion into two). The "amend" is qualitatively different from "append" and could go wrong independently. **Recommendation**: Consider splitting into W3-03a (append 15 criteria) and W3-03b (split budget-exhaustion criterion). However, the blast radius of a failed split is low (it's additive), so this is a **soft recommendation**.

2. **W1-05 (Baseline table)**: This task does four things: add 3 rows, add a methods-consumed note, and amend the convergence.py row. The amendment could conflict with existing text. **Recommendation**: Acceptable as-is given the low risk, but the convergence.py row amendment should be flagged as requiring extra care.

### Single-Task Failure Blast Radius

- **W2-03 failure**: Blocks W3-01, W3-05. Budget isolation is undefined. Wave 3 cannot proceed for 2 of 6 tasks.
- **W2-01 failure**: Blocks W3-03 (partially), W3-04, W3-06. Function signature undefined. Wave 3 loses 3 of 6 tasks.
- **W2-02 failure**: Blocks W3-02, W3-03 (partially). Cost constants have no anchor point. Wave 3 loses 2 of 6 tasks.
- **Any Wave 1 task failure**: No cascading effect on Waves 2+. Only W1-V verification is affected.
- **Any Wave 4/5 task failure**: No cascading effect (except W5-04 on W5-03). Low blast radius.

**Critical path**: Wave 2 tasks are the bottleneck. All three Wave 2 tasks feed into Wave 3. A failure in any Wave 2 task degrades Wave 3 substantially.

---

## Additional Observations

### Positive Design Decisions

1. **Decomposition of merged plan Edit 3**: Splitting the budget isolation rewrite (W2-03) from the pipeline executor wiring (W3-05) reduces per-task complexity and aligns with the merged plan's own organizational separation.

2. **W5-04 as gap closure**: Adding the key risks list item that all three adversarial plans missed demonstrates thorough cross-referencing.

3. **Cross-Cutting Notes section**: The tasklist includes contradiction resolutions, interaction effects, and unchanged sections as executor guidance. This is excellent practice for `/sc:task-unified` execution.

4. **Line number references**: Tasks include approximate line numbers for target sections, which aids executor precision.

### Minor Concerns

1. **Wave 5 parallelism claim**: The Wave 5 header says "Can execute in parallel" but W5-04 depends on W5-03. This is a documentation inaccuracy, not a logic error.

2. **Appendix C omission**: The merged plan notes that a v1.2.0 amendment row in Appendix C would be appropriate. The tasklist omits this. Given the merged plan marks it as optional, this is acceptable but worth noting for completeness.

3. **NFR-2 measurement language**: The merged plan's Completeness Assessment notes NFR-2 could reference `ledger.can_launch()`. Neither the merged plan nor the tasklist mandates this change. The gap is documented but intentionally deferred.

---

## Verdict

### **PASS WITH NOTES**

The tasklist is faithful to the merged plan and complete in its coverage. All 20 merged plan edits have corresponding tasks. The additional task (W5-04) closes a gap identified in the Completeness Assessment. Dependency ordering is correct with one minor documentation issue. Task descriptions are accurate and sufficiently detailed for `/sc:task-unified` execution.

**Notes requiring attention before execution**:

1. **Wave 5 parallelism documentation** (MINOR): W5-04 depends on W5-03 but the wave header claims full parallelism. Amend the header or add a note.

2. **FR-7 subsection ordering** (MINOR): Consider whether budget calibration constants (W3-02) should precede reimbursement semantics (W3-01) in the document, since reimbursement formulas reference the constants.

3. **W2-02 ambiguity** (MINOR): The G2 budget bullet replacement is the least specified task. The acceptance criterion ("No remaining '3 runs' hard-coded language") provides a negative constraint but no positive template. The executor has latitude; this is acceptable but carries mild risk.

4. **Appendix C gap** (OPTIONAL): No task creates a v1.2.0 amendment traceability row in Appendix C. Consider adding if completeness is valued over minimalism.

**None of these notes are blocking.** The tasklist can proceed to execution as-is.
