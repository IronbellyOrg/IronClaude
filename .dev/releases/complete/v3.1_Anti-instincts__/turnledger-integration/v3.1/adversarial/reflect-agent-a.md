# Tasklist Validation: v3.1 Anti-Instincts Gate

> **Validator**: Reflect Agent A
> **Date**: 2026-03-20
> **Files reviewed**:
> - Tasklist: `v3.1/tasklist.md` (22 tasks, 6 waves)
> - Merged Plan: `v3.1/adversarial/merged-output.md`
> - Original Spec: `v3.1_Anti-instincts__/anti-instincts-gate-unified.md`

---

## 1. Coverage Analysis

### Merged Plan Edits -> Tasklist Mapping

| Merged Plan Edit | Tasklist Task(s) | Status |
|---|---|---|
| Section 3: Add dual-context note after pipeline position paragraph | Task 001 | COVERED |
| Section 8: Add `gate_scope` to `ANTI_INSTINCT_GATE` definition | Task 002 | COVERED |
| Section 8: Add Coexistence with Sprint-Pipeline subsection (dual-context, enforcement_tier vs rollout_mode, mode table, `gate_passed()` note) | Task 003 | COVERED |
| Section 9 Change 2: Add `gate_scope` to Step definition | Task 004 | COVERED |
| Section 9 Change 2: Expand `retry_limit=0` comment (remediation path, BUDGET_EXHAUSTED) | Task 004 | COVERED |
| Section 9 after Change 3: Add KPI Reporting Boundary note | Task 005 | COVERED |
| Section 9 Change 4: Add `TrailingGateResult` and `DeferredRemediationLog` imports | Task 006 | COVERED |
| Section 9.5 (New): Sprint Executor Integration (6-step lifecycle, reimbursement, None-safety, threading, rollout mode matrix) | Task 008 | COVERED |
| Section 9.6 (New): KPI Report Integration | Task 009 | COVERED |
| Section 12: Add coordination table (4-row conflict analysis) | Task 012 | COVERED |
| Section 12: Add sprint-side files to modified files list, update LOC, update model changes count | Task 013 | COVERED |
| Section 12: Add new test files (`test_shadow_mode.py`, `test_full_flow.py`) | Task 013 | COVERED |
| Section 13: Add parallelism note (Branch A/B) | Task 014 | COVERED |
| Section 13: Split task 6 into 6a/6b, add task 9 (shadow validation), default to "off" | Task 015 | COVERED |
| Section 13 Phase 2: Add deferred item for sprint-pipeline gate reimbursement | Task 016 | COVERED |
| Section 14: Add assumptions A-011 through A-014 | Task 017 | COVERED |
| Section 16.5 (New): TurnLedger Integration Contract (5 economic paths, None-safety, invariant) | Task 010 | COVERED |

### GAPS (merged-plan edits with NO matching task)

**None found.** Every edit specified in the merged plan has a corresponding task in the tasklist. All 10 sections targeted by the merged plan (3, 8, 9, 9.5, 9.6, 12, 13, 14, 16.5) are covered by at least one task.

### ORPHANS (tasks with NO merged-plan mapping)

| Task | Classification | Assessment |
|---|---|---|
| Task 007 | Verify Wave 1 | VALID ORPHAN -- verification task, not an edit. No merged-plan edit expected. |
| Task 011 | Verify Wave 2 | VALID ORPHAN -- verification task. |
| Task 018 | Verify Wave 3 | VALID ORPHAN -- verification task. |
| Task 019 | Verify unchanged sections | VALID ORPHAN -- corresponds to merged plan "Sections Unchanged" table. |
| Task 020 | Validate interaction effects | VALID ORPHAN -- corresponds to merged plan "Interaction Effects" table (10 effects). |
| Task 021 | Validate backward compatibility | VALID ORPHAN -- corresponds to merged plan "Migration / Backward Compatibility Notes" (9 notes). |
| Task 022 | End-to-end coherence test | VALID ORPHAN -- holistic validation, no specific merged-plan edit. |

**All orphans are verification/test tasks that serve the tasklist's quality assurance structure. No spurious orphans detected.**

---

## 2. Fidelity Check

### Accurate Descriptions

Tasks 001-006, 008-010, 012-017 all contain descriptions that faithfully reproduce the merged plan's intent, including specific content to insert, cross-references to add, and field values to use. The descriptions are sufficiently detailed for `/sc:task-unified` execution.

### Flagged Issues

| Task | Issue | Severity |
|---|---|---|
| Task 001 | Description says "line 99" for the pipeline position paragraph. The original spec line 99 is the "Pipeline position" paragraph, which is correct. However, line numbers will shift after any edit. The section anchor ("After the pipeline position paragraph") is the reliable reference. | LOW -- the section anchor is present alongside the line number, so execution will not be confused. |
| Task 003 | Description says "spec lines 1077-1083" for the D-03/D-04 paragraph. In the original spec, lines 1077-1083 correspond to the "Coexistence with Unified Audit Gating D-03/D-04" paragraph (spec lines 1077-1083). This is correct. Same line-shift caveat as Task 001, but the section heading anchor is also present. | LOW |
| Task 004 | Description says to add `gate_scope=GateScope.TASK,` "after the `gate=ANTI_INSTINCT_GATE,` line". The merged plan's code block shows it after `gate=ANTI_INSTINCT_GATE,` which is correct. The description is unambiguous. | NONE |
| Task 008 | Description references "exact content from the merged plan's Section 9.5" but does not inline the full content. This relies on the executor having access to `merged-output.md`. If the executor does not load the merged plan, the task description alone is insufficient to produce the full 6-step lifecycle, rollout mode matrix, etc. | MEDIUM -- The task description lists all 5 content components (lifecycle, reimbursement, None-safety, threading, matrix) which is sufficient to reconstruct, but the "exact content" directive is stronger. Recommend: either inline the content or ensure `/sc:task-unified` loads `merged-output.md` as context. |
| Task 009 | Same "exact content" directive issue as Task 008. The description does list all 4 content components, which is sufficient. | MEDIUM -- same recommendation. |
| Task 010 | Same "exact content" directive issue. The description lists all 5 economic paths. | MEDIUM -- same recommendation. |
| Task 013 | Description bundles 4 sub-edits: (1) add modified files, (2) add test files, (3) update LOC, (4) update model changes count. This is dense for a single task execution but all edits target the same section and are interdependent. | LOW -- splitting would create unnecessary dependency complexity. |
| Task 015 | Description bundles 3 sub-edits: (1) split task 6, (2) add task 9, (3) add default mode note. All target the same Phase 1 block. | LOW -- same assessment as Task 013. |

### Divergences from Merged Plan

| Task | Divergence | Assessment |
|---|---|---|
| Task 003 | The merged plan's Section 8 edit includes a `gate_passed()` note ("The `gate_passed()` function from `pipeline/gates.py` is shared..."). Task 003's acceptance criteria mention this note. No divergence. | NONE |
| Task 017 | The merged plan's Section 14 edits include cross-refs to "design.md Section 10". Task 017's acceptance criteria say "Cross-refs to Sections 8, 9.5, and design.md Section 10 are present." Matches. | NONE |

**No material divergences found.**

---

## 3. Dependency Validation

### Wave Assignment Correctness

| Task | Wave | Dependencies | Valid? |
|---|---|---|---|
| 001-006 | 1 | None | YES -- all are independent edits to existing sections |
| 007 | 1-verify | 001-006 | YES -- verifies all Wave 1 edits |
| 008 | 2 | 003, 004, 005 | YES -- references dual-context terms from Wave 1 |
| 009 | 2 | 008 | YES -- references Section 9.5 concepts |
| 010 | 2 | 003 | YES -- references enforcement_tier vs rollout_mode from Section 8 |
| 011 | 2-verify | 008, 009, 010 | YES -- verifies all Wave 2 sections |
| 012 | 3 | 008 | YES -- coordination table references Sprint Executor Integration |
| 013 | 3 | 012 | YES -- expanded file list contextualizes coordination table |
| 014 | 3 | 012 | YES -- parallelism note references zero-conflict conclusion |
| 015 | 3 | 014 | YES -- task split references Branch A/B from parallelism note |
| 016 | 3 | None | YES -- additive table row, no dependencies |
| 017 | 3 | None | YES -- additive table rows, no dependencies |
| 018 | 3-verify | 012-017 | YES -- verifies all Wave 3 edits |
| 019 | 4 | 018 | YES -- requires all edits complete to diff |
| 020 | 4 | 019 | YES -- requires unchanged sections verified first |
| 021 | 4 | 020 | YES -- requires interaction effects documented |
| 022 | 4 | 021 | YES -- final coherence test |

### Missing Dependencies

| Issue | Assessment |
|---|---|
| Task 010 depends on 003 only, but Section 16.5 also references Section 9.5 (Task 008) concepts like reimbursement lifecycle and None-safety. | MINOR GAP -- Task 010 could be executed without 008 since Section 16.5's content is self-contained in the merged plan, but the cross-references to Section 9.5 won't resolve until 008 completes. In practice, both are in Wave 2 and 008 will execute before or alongside 010. The dependency graph already shows 010 waiting on 007 (Wave 1 verify) which gates Wave 2 start. **No functional risk.** |
| Task 016 and 017 have "no deps" but are in Wave 3. They could theoretically execute in Wave 1 since they are purely additive. | OPTIMIZATION OPPORTUNITY -- Moving 016 and 017 to Wave 1 would reduce Wave 3 breadth. However, this is minor since Wave 1 already has 6 tasks and the total execution time difference is negligible for spec-editing tasks. |

### Parallelization Opportunities

- **Wave 2**: Tasks 008 and 010 can execute in parallel (different sections, 010's dependency on 003 is satisfied by Wave 1). Task 009 must wait for 008. The dependency graph correctly shows this: 008 and 010 are parallel; 009 is sequential after 008.
- **Wave 3**: Tasks 012, 016, and 017 can execute in parallel. Tasks 013 and 014 depend on 012. Task 015 depends on 014. The dependency graph correctly shows this cascading structure.
- **Wave 4**: Tasks 019-022 are correctly sequential (each builds on the prior verification).

**No further parallelization is possible without relaxing correctness constraints.**

---

## 4. Spec Consistency

### Internal Consistency After Execution

| Check | Result |
|---|---|
| Section numbering (1-16, with 9.5, 9.6, 16.5 interleaved) | Task 022 explicitly validates this. The tasklist creates 9.5 (Task 008), 9.6 (Task 009), and 16.5 (Task 010) which will be inserted at the correct positions. CONSISTENT. |
| `gate_scope=GateScope.TASK` appears in both Section 8 and Section 9 | Tasks 002 and 004 add this field to both locations. Task 007 explicitly cross-checks. CONSISTENT. |
| `enforcement_tier` vs `gate_rollout_mode` terminology | Task 003 defines the distinction in Section 8. Tasks 008 and 010 reference it in Sections 9.5 and 16.5. Task 011 cross-checks. CONSISTENT. |
| Rollout mode semantics (off/shadow/soft/full) | Task 003 defines modes in Section 8. Task 008 provides the behavior matrix in Section 9.5. Task 010 defines economic paths in Section 16.5. Task 011 verifies consistency. CONSISTENT. |
| Cross-references resolve | Task 001 adds cross-refs to 9.5 and 16.5. These sections are created by Tasks 008 and 010. Task 020 validates all cross-refs. CONSISTENT. |
| LOC estimate update | Task 013 updates from ~1,040 to ~1,190-1,240. The merged plan specifies the same range. CONSISTENT. |
| Model changes count | Task 013 updates from 0 to 1 (`SprintConfig` gains `gate_rollout_mode`). The merged plan specifies the same. CONSISTENT. |

### Unchanged Sections at Risk

| Section | Risk of Inadvertent Modification |
|---|---|
| Sections 1-2 (Problem Statement, Evidence) | NONE -- no task targets these sections. |
| Sections 4-7 (Modules 1-4) | NONE -- no task targets these sections. The merged plan explicitly states these are pure-Python modules with zero TurnLedger interaction. |
| Section 10 (Prompt Modifications) | NONE -- no task targets this section. |
| Section 11 (Contradiction Resolutions) | LOW -- Task 003 adds a cross-ref to X-007 in the new Section 8 subsection, but this is a reference FROM the new content, not a modification OF Section 11. |
| Section 15 (V5-3 AP-001 Subsumption) | NONE -- no task targets this section. |
| Section 16 (Rejected Alternatives) | NONE -- no task targets this section. Note that Section 16.5 is a NEW section inserted after Section 16, not a modification of Section 16 itself. |

**Task 019 explicitly validates that all "unchanged" sections remain unchanged. This is a strong safeguard.**

### Acceptance Criteria Alignment with Spec Conventions

The original spec uses:
- Markdown headings (`##`, `###`) for section/subsection structure
- Code blocks with Python syntax highlighting
- Tables with pipe-delimited columns
- Frontmatter YAML blocks for audit report format
- Source attribution comments (`<!-- Source: ... -->`)

The tasklist's acceptance criteria align with these conventions. Tasks 008, 009, and 010 (new sections) will need source attribution comments; this is not explicitly mentioned in the task descriptions but is implied by "Use the exact content from the merged plan's Section X."

**MINOR NOTE**: The merged plan's content blocks for Sections 9.5, 9.6, and 16.5 do not include `<!-- Source: ... -->` comments. If the executor adds them, this is fine. If not, the new sections will lack source attribution, which breaks a minor spec convention. This is cosmetic and does not affect correctness.

---

## 5. Risk Assessment

### Highest Execution Risk

| Rank | Task | Risk | Rationale |
|---|---|---|---|
| 1 | Task 008 (Section 9.5) | HIGH | Largest single content addition (~30 lines of structured content including a behavior matrix table). Most cross-references. If the rollout mode matrix semantics conflict with Section 8's definitions, downstream tasks (011, 018, 020) will fail. |
| 2 | Task 003 (Section 8 Coexistence) | HIGH | Second-largest content addition. Defines the enforcement_tier vs rollout_mode distinction that all downstream tasks reference. If terminology is wrong here, it cascades through Sections 9.5, 16.5, and assumptions. |
| 3 | Task 013 (Section 12 File List Expansion) | MEDIUM | Bundles 4 sub-edits with specific numerical values (LOC estimates, model change counts). Incorrect values would be caught by Task 018's verification but would require rework. |
| 4 | Task 010 (Section 16.5) | MEDIUM | Defines economic paths that must be consistent with Section 9.5's lifecycle. If credit/debit semantics diverge from the merged plan, the integration contract is unreliable. |
| 5 | Task 015 (Section 13 Task Split) | MEDIUM | Modifies an existing numbered task list (splitting task 6 into 6a/6b and adding task 9). If the split point is wrong or the numbering is off, the implementation sequence becomes confusing. |

### Tasks That Should Be Split

No tasks require splitting. The bundled tasks (013, 015, 017) target single sections with interdependent edits. Splitting them would create artificial dependencies and increase verification overhead without reducing risk.

### Blast Radius Analysis

| Failure Scenario | Blast Radius | Mitigation |
|---|---|---|
| Task 002 fails (gate_scope missing from Section 8) | Task 004 becomes inconsistent (Section 9 has gate_scope but Section 8 doesn't). Tasks 008, 010 reference gate_scope. Task 007 catches this. | LOW -- Wave 1 verify (Task 007) is a checkpoint. |
| Task 003 fails (Section 8 coexistence subsection wrong) | Tasks 008, 010, 017 build on incorrect terminology. All of Wave 2 and some of Wave 3 are affected. | HIGH -- Task 003 is load-bearing. If it fails, Wave 2 should not proceed. Task 007 is the checkpoint. |
| Task 008 fails (Section 9.5 incomplete or incorrect) | Tasks 009, 012, 013, 014, 015 reference Section 9.5. Essentially all of Waves 2-3 are affected. | HIGH -- Task 008 is the highest-impact single task. Task 011 is the checkpoint. |
| Task 010 fails (Section 16.5 wrong) | Limited downstream impact. Section 16.5 is referenced by other sections but nothing builds on it structurally. | LOW -- self-contained economic contract. |
| Task 017 fails (assumptions A-011 through A-014 wrong) | Limited downstream impact. Assumptions are referenced but not structurally depended on. Task 018 verifies cross-references. | LOW -- additive content. |
| Any Wave 4 task fails | No downstream tasks exist. Failure indicates a real inconsistency that should be fixed before implementation handoff. | MEDIUM -- these are the final quality gates. Failure here means the spec has inconsistencies. |

---

## 6. Verdict

### **PASS WITH NOTES**

The tasklist is faithful and complete. Every merged-plan edit has a corresponding task. Dependencies are correctly ordered. Wave assignments are sound. Verification tasks provide adequate quality gates between waves.

### Notes

1. **MEDIUM: "Exact content" directives in Tasks 008, 009, 010** -- These tasks reference "exact content from the merged plan" but do not inline the full content in the task description. The `/sc:task-unified` executor must load `merged-output.md` as context for these tasks, or the executor must reconstruct the content from the descriptions (which are detailed enough to do so). Recommendation: ensure the executor's context includes the merged plan, or inline the full content blocks.

2. **LOW: Line number references in Tasks 001 and 003** -- These tasks reference spec line numbers (99, 1077-1083) that will shift after any edit. The section heading anchors are present alongside the line numbers, which makes execution robust. No action needed, but future tasklists should prefer section anchors over line numbers as primary references.

3. **LOW: Source attribution comments** -- The merged plan's content for new Sections 9.5, 9.6, and 16.5 does not include `<!-- Source: ... -->` comments that the original spec uses consistently. The executor should add these for convention consistency (e.g., `<!-- Source: Merged plan (Alpha+Beta+Gamma consensus) -->`).

4. **OPTIMIZATION: Tasks 016 and 017 could move to Wave 1** -- Both are purely additive table rows with no dependencies on Wave 1 or 2 content. Moving them to Wave 1 would reduce Wave 3 breadth. This is a minor optimization that does not affect correctness.

5. **OBSERVATION: Task 010 dependency is technically incomplete** -- Task 010 (Section 16.5) depends only on Task 003 but cross-references Section 9.5 (Task 008). Both are in Wave 2 and gated by Task 007, so there is no functional risk. However, if the dependency graph were strictly enforced, Task 010 should also depend on Task 008. This does not affect execution since Wave 2 tasks all wait for Wave 1 verification.

### Confidence

**95%** -- The tasklist is well-structured, comprehensive, and faithfully maps the merged plan. The notes above are process improvements, not correctness issues. The tasklist is ready for execution.
