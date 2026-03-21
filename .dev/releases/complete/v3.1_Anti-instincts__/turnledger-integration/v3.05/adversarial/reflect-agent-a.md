# Tasklist Validation: v3.05 Deterministic Fidelity Gates

**Agent**: Reflect Agent A
**Date**: 2026-03-20
**Inputs**:
- TASKLIST: `tasklist.md` (24 tasks, 6 waves)
- MERGED PLAN: `adversarial/merged-output.md` (20 edits, 9 interaction effects)
- ORIGINAL SPEC: `deterministic-fidelity-gate-requirements.md` (v1.1.0)

---

## 1. Coverage Analysis

### Merged Plan Edit-to-Task Mapping

| # | Merged Plan Edit | Tasklist Task | Match Quality |
|---|-----------------|---------------|---------------|
| 1 | YAML frontmatter: `relates_to` additions | W1-01 | EXACT |
| 2 | YAML frontmatter: `module_disposition` CONSUME entry | W1-02 | EXACT |
| 3 | YAML frontmatter: version bump + amendment_source | W1-03 | EXACT |
| 4 | Section 1.2: Scope boundary | W1-04 | EXACT |
| 5 | Section 1.3: v3.0 baseline table rows | W1-05 | EXACT |
| 6 | FR-7 Edit 1: Description + function signature | W2-01 | EXACT |
| 7 | FR-7 Edit 2: Budget model replacement | W2-02 | EXACT |
| 8 | FR-7 Edit 3: Budget isolation dispatch | W2-03 | EXACT |
| 9 | FR-7 Edit 4: Reimbursement semantics (NEW SUBSECTION) | W3-01 | EXACT |
| 10 | FR-7 Edit 5: Budget calibration constants (NEW SUBSECTION) | W3-02 | EXACT |
| 11 | FR-7 Edit 6: Acceptance criteria additions | W3-03 | EXACT |
| 12 | FR-7 NEW: Import boundary justification | W3-04 | EXACT |
| 13 | FR-7 NEW: Pipeline executor wiring | W3-05 | EXACT |
| 14 | FR-7.1: Budget accounting rule rewrite | W3-06 | EXACT |
| 15 | FR-9: Clarification note | W4-01 | EXACT |
| 16 | FR-10: Run metadata + progress logging | W4-02 | EXACT |
| 17 | Section 4.2: Module disposition annotations | W4-03 | EXACT |
| 18 | Appendix A: Convergence loop diagram replacement | W5-01 | EXACT |
| 19 | US-5: Budget exhaustion note | W5-02 | EXACT |
| 20 | Section 7: Handoff TurnLedger notes | W5-03 | EXACT |

### GAPS: Merged plan edits with NO matching task

**GAP-1: Section 7 Key Risks -- missing dedicated edit**

The merged plan's Completeness Assessment (item 1 under "Were any spec sections missed by ALL plans?") identifies that no plan recommended adding a TurnLedger cross-module import risk to the Section 7 key implementation risks list. **However**, the tasklist DOES include Task W5-04 which adds risk item 6 to the key risks list. This is a tasklist addition that goes beyond the merged plan's explicit edit list.

**Verdict**: No true gaps. The tasklist actually covers one item the merged plan flagged as missed by all three plans. This is correct behavior -- the tasklist author caught the completeness gap.

**GAP-2: Appendix C (Amendment Traceability)**

The merged plan's Completeness Assessment notes: "if the spec bumps to v1.2.0, a new row documenting the TurnLedger amendment provenance would be appropriate." The merged plan lists Appendix C as "unchanged" in the Sections Unchanged table, and the tasklist's "Unchanged Sections" list also excludes it from modification. No task adds a v1.2.0 traceability row to Appendix C.

**Verdict**: Minor gap. The merged plan does not mandate this edit (calls it "optional"), and the tasklist correctly reflects the merged plan. However, a v1.2.0 version bump without a corresponding Appendix C row creates a traceability discontinuity. Recommend adding a low-priority Wave 5 task or noting it in the W6-V verification checklist.

**GAP-3: NFR-2 measurement language**

The merged plan's Completeness Assessment notes: "none suggest amending NFR-2's measurement/verification language to reference `ledger.can_launch()` instead of a run counter." The merged plan does not include this as an edit. The tasklist does not include it either.

**Verdict**: Minor gap. NFR-2 currently says "Run counter in registry" for measurement. After TurnLedger integration, budget exhaustion via `can_launch()` is the actual enforcement mechanism. The existing language is not technically wrong (run counting still happens) but is incomplete. Consider a low-priority additive note to NFR-2 in Wave 5, or flag in W6-V.

### ORPHANS: Tasks with no merged-plan edit

**ORPHAN-1: Task W5-04 (Section 7 key risks -- cross-module import)**

This task adds risk item 6 to the key implementation risks. The merged plan does NOT include this as an explicit edit in the "Edit Summary" table (items 1-20) or in the Section 7 edit description. The merged plan's Section 7 edit only covers "handoff notes," not the separate "key risks" list.

**Verdict**: Beneficial orphan. This task fills a gap the merged plan's own Completeness Assessment identified. It should remain in the tasklist. However, the task description says "This was identified by the completeness assessment as missed by all three plans" -- this is accurate and the provenance is clear.

**ORPHAN-2: Verify tasks (W1-V, W2-V, W3-V, W4-V, W6-V)**

These are structural verification tasks not present in the merged plan (which is an edit plan, not an execution plan). They are appropriate for a tasklist.

**Verdict**: Correct. Verify tasks are a tasklist concern, not a merged-plan concern.

### Coverage Summary

| Category | Count |
|----------|-------|
| Exact matches (merged plan -> task) | 20/20 |
| True gaps (merged plan edit with no task) | 0 |
| Advisory gaps (completeness items not mandated) | 2 (Appendix C, NFR-2) |
| Beneficial orphans | 1 (W5-04) |
| Structural orphans (verify tasks) | 5 |

---

## 2. Fidelity Check

### Task descriptions vs. merged plan intent

| Task | Fidelity | Notes |
|------|----------|-------|
| W1-01 | FAITHFUL | Correctly specifies both `sprint/models.py` and `trailing_gate.py` paths |
| W1-02 | FAITHFUL | Correctly specifies CONSUME action, note text, and `extends_frs` |
| W1-03 | FAITHFUL | Version bump and amendment_source both covered |
| W1-04 | FAITHFUL | In-scope and out-of-scope text matches merged plan verbatim. Correctly includes ConvergenceBudget rejection language from contradiction resolution X3 |
| W1-05 | FAITHFUL | Three rows + method list + convergence.py annotation all present |
| W2-01 | FAITHFUL | Injection rationale + full signature with `ledger: TurnLedger` and three keyword-only callables |
| W2-02 | FAITHFUL | Correctly replaces "3 runs" with TurnLedger terms; preserves catch/verify/backup framing |
| W2-03 | FAITHFUL | Convergence vs. legacy dispatch; mutual exclusion emphasized; references Wave 3 for dispatch code subsection |
| W3-01 | FAITHFUL | Mapping table with 4 scenarios; helper signature; 5+ acceptance criteria |
| W3-02 | FAITHFUL | Both tables; module-level location; overridability; Beta's risk note about locking calibration values |
| W3-03 | **MINOR CONCERN** | Task says "15 new acceptance criteria" but the merged plan's FR-7 Edit 6 lists 15 criteria. The task also says "amend existing budget-exhaustion criterion to split into two." This is correct but the description should note the net new count is 15 + 1 split = 16 line items changed. |
| W3-04 | FAITHFUL | 4 justification points; references design.md Section 5.4 and Section 1.2 |
| W3-05 | FAITHFUL | Dispatch code block; both branches; 3 acceptance criteria; references design.md Section 5.3 |
| W3-06 | FAITHFUL | Budget accounting rule rewrite; "subsumes" language; 3 new criteria; `handle_regression_fn` injectable. Correctly implements contradiction resolution X1 (bundled, not separate debits) |
| W4-01 | FAITHFUL | Clarification note; non-behavioral; references `REMEDIATION_COST` |
| W4-02 | FAITHFUL | `budget_snapshot` field with `None` default; 3 new criteria with format strings; backward compat note. Correctly routes through FR-10 per contradiction resolution X2 |
| W4-03 | **MINOR CONCERN** | Task description says "this section is in the YAML frontmatter `module_disposition` block" but the merged plan's Section 4.2 edit heading says "Module Disposition (frontmatter/design)." The spec's frontmatter `module_disposition` (lines 24-49) and a separate Section 4.2 may be the same thing or different. The original spec does NOT have a Section 4.2 heading -- the module disposition lives entirely in the YAML frontmatter. This is internally consistent but the section reference "Section 4.2" is a misnomer since that section number does not exist in the spec. Executors should target the YAML frontmatter block. |
| W5-01 | FAITHFUL | All debit/credit points; TurnLedger construction at top; Run 1/2/3 preserved |
| W5-02 | FAITHFUL | Non-breaking note; references TurnLedger state fields |
| W5-03 | FAITHFUL | 4 integration notes; risk about cross-module import |
| W5-04 | FAITHFUL | Risk item 6 with migration reference; correctly depends on W5-03 |

### Ambiguity or Underspecification Flags

**FLAG-1**: Task W2-03 says "Replace the existing budget isolation paragraph" but does not specify whether the replacement should include the pipeline executor dispatch code block that the merged plan's FR-7 Edit 3 shows. The merged plan's Edit 3 says "Include pipeline executor dispatch code block showing TurnLedger construction." However, Task W3-05 is a separate task that adds the "Pipeline Executor Wiring" subsection. There is a potential overlap: W2-03 might include inline dispatch code that W3-05 then redundantly adds as a subsection.

**Resolution**: The merged plan's Edit 3 includes dispatch code inline, while the "Pipeline Executor Wiring" new subsection (Gamma's unique finding U8) elevates it. The tasklist's W2-03 says "Include a note that the pipeline executor dispatch code is specified in a dedicated subsection (added in Wave 3)." This is a clean separation -- W2-03 references but does not duplicate W3-05. RESOLVED.

**FLAG-2**: Task W3-03 description lists 15 acceptance criteria by number (1-15) plus the split of one existing criterion. An executor would need to carefully count to verify all 15 are present. The merged plan lists them as a code block with checkboxes. Recommend the task description include the checkbox block verbatim or reference it explicitly.

**FLAG-3**: Task W4-03 references "Section 4.2" which does not exist as a numbered heading in the spec. The target is the YAML frontmatter `module_disposition` block (lines 24-49). The task description correctly identifies this in its parenthetical, but the task title "Section 4.2" could confuse executors.

---

## 3. Dependency Validation

### Wave Assignment Correctness

| Task | Wave | Dependencies | Valid? |
|------|------|-------------|--------|
| W1-01 | 1 | none | YES |
| W1-02 | 1 | none | YES |
| W1-03 | 1 | none | YES |
| W1-04 | 1 | none | YES |
| W1-05 | 1 | none | YES |
| W1-V | 1 | W1-01..W1-05 | YES |
| W2-01 | 2 | none (listed) | YES -- no dependency on Wave 1 content |
| W2-02 | 2 | none (listed) | YES |
| W2-03 | 2 | none (listed) | YES |
| W2-V | 2 | W2-01..W2-03 | YES |
| W3-01 | 3 | W2-03 | YES -- reimbursement semantics follows budget isolation |
| W3-02 | 3 | W2-02 | YES -- calibration constants follow budget model |
| W3-03 | 3 | W2-01, W2-02, W2-03 | YES -- acceptance criteria reference all W2 edits |
| W3-04 | 3 | W2-01 | YES -- import justification follows function signature |
| W3-05 | 3 | W2-03 | YES -- pipeline wiring follows budget isolation |
| W3-06 | 3 | W2-01 | YES -- FR-7.1 references function signature |
| W3-V | 3 | W3-01..W3-06 | YES |
| W4-01 | 4 | W3-02 | YES -- FR-9 note references REMEDIATION_COST constant |
| W4-02 | 4 | W3-01, W3-02 | YES -- FR-10 references reimbursement semantics and constants |
| W4-03 | 4 | W3-01 | YES -- disposition references reimburse_for_progress() |
| W4-V | 4 | W4-01..W4-03 | YES |
| W5-01 | 5 | W3-01, W3-02, W3-05 | YES -- diagram references all FR-7 subsections |
| W5-02 | 5 | W3-02 | YES -- US-5 note references constants |
| W5-03 | 5 | W3-04 | YES -- handoff references import boundary documentation |
| W5-04 | 5 | W5-03 | YES -- risk item references handoff notes; sequential within wave |
| W6-V | 6 | W5-01..W5-04 | YES |

### Missing Dependencies

**MISSING-DEP-1**: Task W3-04 (Import Boundary Justification) lists dependency on W2-01 only. However, the justification references Section 1.2 scope boundary (W1-04) and the import itself (established conceptually in W2-03). Since W1-04 is Wave 1 and W2-03 is Wave 2, both complete before Wave 3 -- so the dependency is implicitly satisfied by wave ordering. No functional issue, but explicit dependency on W1-04 would improve traceability.

**MISSING-DEP-2**: Task W5-01 (Appendix A diagram) should arguably depend on W3-06 (FR-7.1 budget accounting rule) since the diagram needs to show `REGRESSION_VALIDATION_COST` debit. The dependency on W3-02 (constants) partially covers this, but the "subsumes" semantics from W3-06 should be reflected in the diagram. Again, wave ordering makes this a non-issue functionally.

### Parallelization Opportunities

All waves are correctly structured for maximum parallelism within each wave:

- **Wave 1**: 5 tasks target independent spec sections. Fully parallel. CORRECT.
- **Wave 2**: 3 tasks target different paragraphs within FR-7. Parallel with care (no overlapping line ranges). CORRECT.
- **Wave 3**: 6 tasks target distinct subsections/locations within FR-7 and FR-7.1. Parallel. CORRECT.
- **Wave 4**: 3 tasks target FR-9, FR-10, and YAML frontmatter. Fully independent. CORRECT.
- **Wave 5**: 4 tasks, but W5-04 depends on W5-03. The other 3 (W5-01, W5-02, W5-03) can run in parallel. W5-04 must follow W5-03. CORRECT as described.
- **Wave 6**: Single verification task. N/A.

**Could waves be combined?** Wave 1 and Wave 2 target different spec sections and could theoretically run in parallel. However, the verify step (W1-V) before Wave 2 provides a safety checkpoint that the frontmatter/scope changes are correct before modifying FR-7. This is a reasonable safety tradeoff.

---

## 4. Spec Consistency

### Will the tasks produce an internally consistent spec?

**YES, with the following observations:**

**CONSISTENCY-1: FR-7 acceptance criteria cross-reference integrity**

After Wave 3, FR-7 will have ~38 acceptance criteria (23 existing + 15 new). The new criteria reference TurnLedger terms (`CHECKER_COST`, `can_launch()`, etc.) that are defined in the new "Budget Calibration Constants" subsection (W3-02). The cross-references are consistent: criteria reference constants by the same names used in the subsection.

**CONSISTENCY-2: FR-7.1 budget accounting rule alignment with FR-7 budget isolation**

W2-03 (budget isolation) establishes that convergence mode owns all budget decisions. W3-06 (FR-7.1 rewrite) establishes that `handle_regression()` does NOT perform ledger operations. These are consistent: FR-7 debits before calling FR-7.1, and FR-7.1 returns results without touching the ledger.

**CONSISTENCY-3: FR-10 budget_snapshot alignment with FR-6 RunMetadata**

W4-02 adds `budget_snapshot: dict | None = None` to RunMetadata. The spec defines RunMetadata within FR-6's scope. The contradiction resolution (X2) correctly routes this through FR-10 -- but the actual `RunMetadata` dataclass is defined in FR-6. The task description and acceptance criteria correctly specify this as an FR-10 amendment, which is organizationally appropriate since FR-10 is about run-to-run memory.

**CONSISTENCY-4: Section 1.2 scope boundary and the ConvergenceBudget rejection**

W1-04 explicitly rejects a separate ConvergenceBudget dataclass in the out-of-scope text. This aligns with contradiction resolution X3 and interaction effect IE-9. No other task introduces such a dataclass. Consistent.

### Sections marked "unchanged" -- inadvertent modification risk

The merged plan lists 26 sections as unchanged. The tasklist's "Unchanged Sections" list matches exactly:

> FR-1, FR-2, FR-3, FR-4, FR-4.1, FR-4.2, FR-5, FR-6, FR-8, FR-9.1, NFR-1 through NFR-7, US-1 through US-4, US-6, Section 1.1, Section 2, Section 6, Appendix B, Appendix C.

**Risk assessment**: No task targets any of these sections. The only adjacent edits are:
- W4-01 targets FR-9 (not FR-9.1) -- safe, different subsection
- W5-02 targets US-5 (not US-1 through US-4 or US-6) -- safe
- W4-02 targets FR-10 (not FR-6) -- safe per contradiction resolution

**NFR-2 is listed as unchanged** but its measurement language ("Run counter in registry") becomes partially inaccurate after TurnLedger integration. This is noted in Gap-3 above but does not constitute an inadvertent modification -- no task touches NFR-2.

### Acceptance criteria conventions

The original spec uses:
- `[x]` for v3.0 baseline items (verify, do not rebuild)
- `[ ]` for items requiring implementation

The tasklist's W3-03 correctly specifies "15 new criteria present as unchecked `[ ]` items; existing criteria unchanged." This preserves the spec's convention.

---

## 5. Risk Assessment

### Highest Execution Risk Tasks

**RISK-1: Task W2-03 (FR-7 Budget Isolation Dispatch) -- HIGH**

This task replaces the existing budget isolation paragraph (lines 635-643) with entirely new content. It establishes the mutual exclusion invariant between convergence and legacy modes. If the replacement text is incorrect or incomplete:
- Both budget systems could run simultaneously (double-charging)
- Legacy mode could break if the replacement accidentally conditions it on `convergence_enabled`
- The "note that pipeline executor dispatch code is specified in a dedicated subsection" must be precise to avoid confusion

**Blast radius**: FR-7 behavior, FR-9 remediation budget, NFR-7 backward compatibility. High.

**RISK-2: Task W3-03 (FR-7 Acceptance Criteria Additions) -- MEDIUM-HIGH**

Adding 15 acceptance criteria and splitting one existing criterion is the highest line-count edit. Risks:
- Numbering or formatting errors in the 15 new items
- Accidentally modifying or removing an existing criterion
- The split budget-exhaustion criterion must correctly replace the existing one without losing the original intent

**Blast radius**: Verification and testing scope for the entire FR-7 implementation. Medium-high.

**RISK-3: Task W5-01 (Appendix A Diagram Replacement) -- MEDIUM**

Replacing an ASCII diagram while preserving structure and adding budget annotations requires careful formatting. ASCII art is fragile and easy to break in markdown.

**Blast radius**: Implementer understanding of convergence flow. Medium (diagram is informational, not normative).

**RISK-4: Task W3-06 (FR-7.1 Budget Accounting Rule) -- MEDIUM**

Rewriting the budget accounting rule involves the contradiction resolution (X1: bundled vs. separate debits). If the "subsumes" interpretation is not clearly expressed, implementers may double-debit.

**Blast radius**: FR-8 regression validation cost accounting. Medium.

### Tasks that should be split

No tasks require splitting. The granularity is appropriate:
- The largest conceptual task (W3-03, 15 criteria) is already a single-section additive edit
- W1-05 (3 table rows + annotation) could theoretically split but the rows are in the same table
- W5-01 (diagram replacement) is atomic by nature

### Single-task failure blast radius

| Task | Blast Radius if Failed |
|------|----------------------|
| W2-03 | **Critical** -- budget isolation is the invariant that prevents dual-mode execution |
| W3-03 | **High** -- acceptance criteria define verification scope for all FR-7 implementation |
| W3-05 | **High** -- pipeline executor wiring is the integration point where TurnLedger enters the pipeline |
| W3-06 | **Medium-High** -- FR-7.1 budget accounting affects regression validation costs |
| W5-01 | **Low** -- diagram is informational |
| All W1 tasks | **Low** -- frontmatter and scope are traceability/documentation |
| W5-02, W5-03, W5-04 | **Low** -- additive notes |

---

## 6. Cross-Cutting Observations

### Interaction Effects Coverage

The merged plan identifies 9 interaction effects (IE-1 through IE-9). The tasklist's "Cross-Cutting Notes" section correctly documents IE-1, IE-2, IE-3, and IE-7 as items to monitor during execution. IE-5 (reimbursement_rate consumers) is addressed by W3-01. IE-6 (TurnLedger location) is addressed by W3-04. IE-8 (attempt_remediation parallel path) requires no spec edit. IE-9 (ConvergenceBudget rejection) is addressed by W1-04.

**All 9 interaction effects are covered by tasks or noted in cross-cutting documentation.**

### Contradiction Resolutions Application

| Contradiction | Resolution | Tasklist Implementation |
|--------------|------------|------------------------|
| X1: Bundled vs. separate debits | Alpha/Beta (bundled) | W3-06 uses "subsumes" language. Cross-cutting note #1 reinforces. CORRECT. |
| X2: FR-6 changed or unchanged | FR-6 unchanged; route through FR-10 | W4-02 targets FR-10. Cross-cutting note #2 reinforces. CORRECT. |
| X3: ConvergenceBudget dataclass | Rejected per design.md | W1-04 scope boundary explicitly rejects. Cross-cutting note #3 reinforces. CORRECT. |

---

## 7. Verdict

### **PASS WITH NOTES**

The tasklist is faithful, complete, and well-structured. All 20 merged-plan edits map to exactly one task. Wave ordering and dependencies are correct. Contradiction resolutions are properly applied. The tasklist even covers one gap the merged plan's own completeness assessment identified (Section 7 key risks via W5-04).

### Notes for Improvement

1. **Advisory: Appendix C traceability row** -- Consider adding a low-priority Wave 5 task to add a v1.2.0 amendment row to Appendix C, or add it as an item in the W6-V verification checklist. The version bump (W1-03) without a corresponding Appendix C entry creates a minor traceability gap.

2. **Advisory: NFR-2 measurement language** -- Consider adding a note to W6-V to verify that NFR-2's "Run counter in registry" measurement description remains accurate after TurnLedger integration, or add a low-priority Wave 5 task to append a clarifying note.

3. **Clarification: W4-03 section reference** -- Task W4-03 title says "Section 4.2" but the spec has no Section 4.2 heading. The target is the YAML frontmatter `module_disposition` block. The description's parenthetical correctly identifies this, but the title could confuse `/sc:task-unified` execution. Consider renaming to "YAML Frontmatter -- Module disposition annotations for convergence.py."

4. **Clarification: W3-03 criterion count** -- Task says "15 new acceptance criteria" but the actual work is 15 new criteria + 1 split of an existing criterion = 16 line items changed. Consider making this explicit to prevent an executor from thinking they are done after adding 15 items.

5. **Explicit dependency: W3-04** -- Add W1-04 as an explicit dependency (scope boundary is referenced in the import boundary justification). Functionally satisfied by wave ordering, but explicit is better for `/sc:task-unified` traceability.

### Confidence Level

**95%** -- The tasklist is production-ready. The notes above are all advisory improvements, not blocking issues. No task will produce incorrect spec content if executed as described.
