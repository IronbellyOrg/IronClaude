# Reflection Report: v3.05 Tasklist Validation (Agent B)

**Date**: 2026-03-20
**Reviewer**: Agent B (validation review)
**Spec**: `deterministic-fidelity-gate-requirements.md` (v1.1.0)
**Merged Plan**: `adversarial/merged-output.md`
**Tasklist**: `tasklist.md` (24 tasks, 6 waves)

---

## Coverage Check

### Merged Plan Edits -> Tasklist Mapping

| # | Merged Plan Edit | Tasklist Task | Status |
|---|-----------------|---------------|--------|
| 1 | YAML frontmatter `relates_to` additions | W1-01 | COVERED |
| 2 | YAML frontmatter `module_disposition` CONSUME entry | W1-02 | COVERED |
| 3 | YAML frontmatter version bump 1.1.0 -> 1.2.0 | W1-03 | COVERED |
| 4 | YAML frontmatter `amendment_source` update | W1-03 | COVERED |
| 5 | Section 1.2 scope boundary (in-scope + out-of-scope) | W1-04 | COVERED |
| 6 | Section 1.3 baseline table rows + method list + convergence.py annotation | W1-05 | COVERED |
| 7 | FR-7 Edit 1: function signature + TurnLedger description | W2-01 | COVERED |
| 8 | FR-7 Edit 2: replace bespoke budget with TurnLedger | W2-02 | COVERED |
| 9 | FR-7 Edit 3: budget isolation dispatch | W2-03 | COVERED |
| 10 | FR-7 Edit 4: reimbursement semantics subsection | W3-01 | COVERED |
| 11 | FR-7 Edit 5: budget calibration constants subsection | W3-02 | COVERED |
| 12 | FR-7 Edit 6: 15 TurnLedger acceptance criteria + budget-exhaustion split | W3-03 | COVERED |
| 13 | FR-7 new subsection: import boundary justification | W3-04 | COVERED |
| 14 | FR-7 new subsection: pipeline executor wiring | W3-05 | COVERED |
| 15 | FR-7.1: budget accounting rule in TurnLedger terms + 3 criteria | W3-06 | COVERED |
| 16 | FR-9: clarification note on budget non-interaction | W4-01 | COVERED |
| 17 | FR-10: ledger snapshots + progress logging + 3 criteria | W4-02 | COVERED |
| 18 | Section 4.2: module disposition annotations | W4-03 | COVERED |
| 19 | Appendix A: replace convergence loop diagram | W5-01 | COVERED |
| 20 | US-5: budget exhaustion note | W5-02 | COVERED |
| 21 | Section 7: handoff TurnLedger notes | W5-03 | COVERED |

### GAPS (merged plan edits with NO tasklist coverage)

**GAP-1: NFR-2 enforcement mechanism language update**
The merged plan's completeness assessment (line 238) identifies that NFR-2's measurement language should reference `ledger.can_launch()` instead of a run counter. No task covers this. All three plans noted this gap, but it was not elevated to the edit summary table.

- **Severity**: Low. The merged plan's "Sections Unchanged" table explicitly lists NFR-1 through NFR-7 as unchanged, so this is arguably intentional. However, the completeness assessment flags it, creating an internal contradiction within the merged plan itself.

**GAP-2: Appendix C amendment traceability row for v1.2.0**
The merged plan's completeness assessment (line 237) notes that a version bump to v1.2.0 should be accompanied by a new Appendix C row documenting the TurnLedger amendment provenance. No task covers this. The merged plan's "Sections Unchanged" table lists Appendix C as unchanged ("Historical record; v1.2.0 amendment tracked separately"), but "tracked separately" is unresolved -- where?

- **Severity**: Low. Traceability gap only. However, the spec already has Appendix C for exactly this purpose (documenting amendment provenance), so omitting the v1.2.0 row is inconsistent with the established pattern.

### ORPHANS (tasks with no merged plan trace)

**ORPHAN-1: Task W5-04 (Section 7 -- Add TurnLedger cross-module import to key risks)**
This task adds a risk item #6 to the key implementation risks list. The description states this was "identified by the completeness assessment as missed by all three plans." While the completeness assessment (merged-output.md line 236) does note this gap, the edit summary table (lines 690-711) does NOT include this as a numbered edit. The merged plan has 20 numbered edits in its summary; the tasklist has 21 edit/add-section tasks (excluding verify tasks). This orphan accounts for the discrepancy.

- **Assessment**: This is a valid addition sourced from the merged plan's completeness assessment section, but it lacks a formal edit entry. Acceptable but should be noted. The task description correctly attributes its source.

---

## Dependency Validation

### Correctly Specified Dependencies

All intra-wave dependencies are correctly specified:
- Wave 1 tasks have no dependencies (correct -- independent frontmatter/scope/baseline edits)
- Wave 2 tasks have no dependencies (correct -- they edit different paragraphs within FR-7)
- Wave 3 tasks depend on appropriate Wave 2 tasks
- Wave 4 tasks depend on appropriate Wave 3 tasks
- Wave 5 tasks depend on appropriate Wave 3/4 tasks
- Wave 6 depends on all Wave 5 tasks

### Missing Dependencies

**DEP-1: W3-03 should depend on W3-01 and W3-02 (not just W2-01, W2-02, W2-03)**
W3-03 adds 15 acceptance criteria, several of which reference concepts introduced by W3-01 (reimbursement semantics: `reimburse_for_progress()`, `reimbursement_rate`) and W3-02 (budget calibration constants: `CHECKER_COST`, `CONVERGENCE_PASS_CREDIT`). The criteria reference these by name, so W3-03 should logically depend on W3-01 and W3-02 to ensure the concepts exist before criteria reference them.

- **Impact**: Medium. Within the same wave, execution ordering is flexible, but if W3-03 executes before W3-01/W3-02, the acceptance criteria will reference subsections that don't yet exist, causing potential confusion for the executor.
- **Mitigation**: Since all Wave 3 tasks are within the same wave, executors will likely process them in order. The verify task (W3-V) catches inconsistencies. But the dependency should be explicit.

**DEP-2: W5-01 (Appendix A diagram) should also depend on W3-03**
The diagram must show budget-related annotations that correspond to acceptance criteria added by W3-03. The tasklist lists dependencies as W3-01, W3-02, W3-05 but omits W3-03.

- **Impact**: Low. The diagram's annotations are derived from FR-7 Edit 4 and Edit 5 content (W3-01, W3-02), not directly from the acceptance criteria (W3-03). The existing dependencies are sufficient in practice.

### Circular Dependencies

None found.

### Parallelism Opportunities

**PAR-1: W5-02 and W5-03 could run in parallel with W5-01**
W5-02 (US-5 note) depends on W3-02 only. W5-03 (handoff notes) depends on W3-04 only. Neither depends on W5-01. All three are already marked as parallel within Wave 5, which is correct.

**PAR-2: W4-01 could potentially run in Wave 3 instead of Wave 4**
W4-01 (FR-9 clarification note) depends on W3-02 (constants defined). It does not depend on W3-03, W3-04, W3-05, or W3-06. It could execute as soon as W3-02 completes, potentially in a late Wave 3 sub-batch. However, the current Wave 4 placement is simpler and the cost of one extra wave for a single-sentence edit is negligible.

---

## Acceptance Criteria Quality

### Well-Specified Criteria

The majority of tasks have specific, verifiable acceptance criteria. Particularly strong:
- W1-01 through W1-05: "YAML parses cleanly", "existing entries unchanged" -- testable
- W2-02: "No remaining '3 runs' hard-coded language" -- searchable/verifiable
- W3-03: "15 new criteria present as unchecked `[ ]` items" -- countable
- W6-V: 8 specific verification checks, each independently testable

### Vague or Unmeasurable Criteria

**AC-1: W2-01 -- "Description paragraph present explaining injection rationale"**
What constitutes adequate "injection rationale"? The merged plan specifies three points (caller owns budget, pipeline may have consumed budget in steps 1-7, caller may reserve for step 9). The tasklist description mentions these but the acceptance criteria don't enumerate them.

- **Recommendation**: Add "paragraph explains: (a) caller owns budget, (b) prior budget consumption in steps 1-7, (c) step 9 budget reservation."

**AC-2: W3-04 -- "references design.md Section 5.4 and Section 1.2 scope boundary"**
This is in the acceptance criteria, but the description doesn't mention these cross-references. The criterion is verifiable but the executor might miss it.

- **Impact**: Low. The executor has both the description and acceptance criteria.

**AC-3: W5-01 -- "Diagram shows all debit/credit points"**
What constitutes "all"? The description enumerates 7 specific annotations. The criterion should say "Diagram shows all 7 debit/credit points enumerated in description."

- **Impact**: Low. The description is sufficiently detailed.

---

## Section Reference Accuracy

### Correct References

Most line number references are accurate against the spec:
- W1-01: "lines 10-22" for `relates_to` block -- CORRECT (spec lines 10-22)
- W1-02: "lines 24-49" for `module_disposition` -- CORRECT (spec lines 24-49)
- W1-04: "lines 78-91" for Section 1.2 -- CORRECT (spec lines 78-91)
- W1-05: "lines 107-119" for baseline table -- CORRECT (spec lines 107-119)
- W2-01: "after line 586" for FR-7 -- CORRECT (spec line 586)
- W2-02: "line 571" for G2 budget bullet -- CORRECT (spec line 571)
- W2-03: "lines 635-643" for budget isolation -- CORRECT (spec lines 635-643)

### Inaccuracies

**REF-1: W3-03 references "lines 644-666" for FR-7 acceptance criteria**
The actual FR-7 acceptance criteria block runs from line 644 to line 666 in the spec. This is CORRECT.

**REF-2: W3-06 references "lines 710-714" for Budget Accounting Rule and "lines 721-728" for acceptance criteria**
FR-7.1 Budget Accounting Rule paragraph is at lines 703-714. The acceptance criteria block is at lines 721-728. These are CORRECT.

**REF-3: W4-01 references "after line 781" for FR-9 description**
FR-9 description begins around line 779. The "after line 781" reference points into the middle of the description paragraph. This is APPROXIMATELY CORRECT but imprecise -- the clarification note should go after the description area, not mid-paragraph.

**REF-4: W4-03 references "Section 4.2 (Module Disposition)"**
The task description notes "this section is in the YAML frontmatter `module_disposition` block, specifically the `convergence.py` entry (lines 25-28)." The spec does NOT have a separate "Section 4.2" for module disposition -- the module_disposition is entirely within the YAML frontmatter. The merged plan's "Section 4.2: Module Disposition (frontmatter/design)" heading is a merged-plan organizational label, not a spec section. The tasklist correctly identifies the actual location (YAML frontmatter lines 25-28) in the description body, but the task title "Section 4.2" is misleading.

- **Impact**: Low. The description body has the correct location. The title follows the merged plan's labeling.

---

## Wave Ordering

### Current Wave Structure Assessment

| Wave | Tasks | Purpose | Assessment |
|------|-------|---------|------------|
| 1 | 5 edit + 1 verify | Frontmatter, scope, baseline | CORRECT. Independent, no cross-deps. |
| 2 | 3 edit + 1 verify | FR-7 core structure | CORRECT. Must precede Wave 3 subsections. |
| 3 | 6 edit/add + 1 verify | FR-7 subsections + FR-7.1 | CORRECT. Depends on Wave 2 structure. |
| 4 | 3 edit + 1 verify | Downstream FRs + disposition | CORRECT. References FR-7 content. |
| 5 | 4 edit | Appendix, US, handoff | CORRECT. References finalized FR content. |
| 6 | 1 verify | Full coherence check | CORRECT. Terminal verification. |

### Could Any Waves Be Collapsed?

**Wave 4 and Wave 5 could potentially merge.** Wave 5 tasks depend on Wave 3 tasks (not Wave 4), except W5-04 which depends on W5-03. If W5-04 were moved to a post-merge sub-batch, the remaining W5-01/W5-02/W5-03 could run in parallel with Wave 4. However, this saves minimal time (one wave boundary) and adds complexity.

**Wave 1 could potentially overlap with Wave 2.** Wave 2 tasks have no dependencies on Wave 1 (they target different spec sections). However, the W1-V verification step depends on all Wave 1 tasks, and interleaving waves makes the execution flow harder to follow. Current sequencing is cleaner.

### Is the Ordering Optimal?

Yes. The current 6-wave structure follows a logical progression:
1. Metadata and context (frontmatter, scope, baseline)
2. Core structural changes (FR-7 paragraphs)
3. New content and extensions (FR-7 subsections, FR-7.1)
4. Downstream references (FR-9, FR-10, disposition)
5. Peripheral content (appendix, US, handoff)
6. Holistic verification

This is a well-structured execution plan.

---

## Risk Assessment

### High-Risk Edits Properly Sequenced?

**YES.** The three highest-risk edits are:
1. W2-02 (budget model replacement) -- Wave 2. This is the most semantically significant change.
2. W2-03 (budget isolation dispatch) -- Wave 2. Mutual exclusion is critical per merged plan.
3. W3-05 (pipeline executor wiring) -- Wave 3. Incorrect dispatch causes both or neither budget system to run.

All three are in early waves with dedicated verification steps, which is correct.

### Interaction Effects Captured?

The tasklist's "Cross-Cutting Notes for Executors" section captures IE-1, IE-2, IE-3, and IE-7 from the merged plan. However:

**RISK-1: IE-5 (reimbursement_rate multiple consumers) not in executor notes**
The merged plan documents IE-5 (v3.05 and v3.1 both consume `reimbursement_rate`). The tasklist's Cross-Cutting Notes section omits this. Task W3-01 mentions it in its risk field, but the cross-cutting notes section should include it for executor awareness.

**RISK-2: IE-8 (attempt_remediation parallel path) not in executor notes**
The merged plan documents IE-8 (two parallel remediation paths). Not mentioned in the tasklist's cross-cutting notes. Low risk since no task modifies this area, but executor awareness is valuable.

**RISK-3: IE-4, IE-6, IE-9 omitted from executor notes**
IE-4 (baseline <-> acceptance criteria traceability), IE-6 (TurnLedger location migration), and IE-9 (ConvergenceBudget rejection) are also not in the executor notes. IE-9 is partially covered by contradiction resolution #3 (no ConvergenceBudget dataclass).

---

## Summary

| Metric | Count |
|--------|-------|
| **Gaps (merged plan edits missing from tasklist)** | 2 (both Low severity) |
| **Orphans (tasks without merged plan trace)** | 1 (justified, sourced from completeness assessment) |
| **Missing dependencies** | 2 (1 Medium, 1 Low) |
| **Circular dependencies** | 0 |
| **Vague acceptance criteria** | 3 (all Low impact) |
| **Section reference inaccuracies** | 1 (W4-03 "Section 4.2" label is misleading but description has correct location) |
| **Wave ordering issues** | 0 (ordering is optimal) |
| **Missing interaction effects in executor notes** | 5 (IE-4, IE-5, IE-6, IE-8, IE-9) |
| **Total issues** | 14 |

### Confidence Level: **HIGH**

The tasklist faithfully represents the merged plan with strong coverage. All 20 numbered edits from the merged plan's summary table have corresponding tasks. The two gaps (NFR-2 language update, Appendix C traceability row) are both explicitly flagged in the merged plan's completeness assessment but intentionally omitted from the edit summary -- meaning the merged plan itself chose not to include them. The one orphan (W5-04) is justified and properly attributed.

The dependency structure is sound with one medium-severity missing dependency (W3-03 should depend on W3-01/W3-02) that is mitigated by wave-level ordering. Wave structure is optimal. Acceptance criteria are specific and verifiable with minor improvements possible.

The primary improvement area is the Cross-Cutting Notes for Executors section, which omits 5 of 9 interaction effects from the merged plan. While the omitted effects are lower-priority, complete coverage would reduce executor surprise.
