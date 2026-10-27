# Tasklist Validation: v3.1 Anti-Instincts Gate (Agent B)

> **Reviewer**: Agent B (Independent Reviewer)
> **Date**: 2026-03-20
> **Tasklist**: `v3.1/tasklist.md` (22 tasks, 6 waves)
> **Merged Plan**: `v3.1/adversarial/merged-output.md`
> **Original Spec**: `v3.1_Anti-instincts__/anti-instincts-gate-unified.md`

---

## Coverage Analysis

### Merged Plan Edits -> Tasklist Mapping

| Merged Plan Edit | Tasklist Task(s) | Status |
|---|---|---|
| Section 3: Add dual-context note after pipeline position paragraph | Task 001 | COVERED |
| Section 8: Add `gate_scope` field to `ANTI_INSTINCT_GATE` | Task 002 | COVERED |
| Section 8: Add Coexistence with Sprint-Pipeline subsection (dual-context, enforcement_tier vs rollout_mode, mode table, `gate_passed()` note) | Task 003 | COVERED |
| Section 9 Change 2: Add `gate_scope=GateScope.TASK` to Step definition | Task 004 | COVERED |
| Section 9 Change 2: Expand `retry_limit=0` comment with remediation path and BUDGET_EXHAUSTED | Task 004 | COVERED |
| Section 9: KPI Reporting Boundary note after Change 3 | Task 005 | COVERED |
| Section 9 Change 4: Add `TrailingGateResult` and `DeferredRemediationLog` imports | Task 006 | COVERED |
| Section 9.5 (New): Sprint Executor Integration (6-step lifecycle, reimbursement, None-safety, threading, rollout mode behavior matrix) | Task 008 | COVERED |
| Section 9.6 (New): KPI Report Integration (GateKPIReport, metrics, data source, sprint-only) | Task 009 | COVERED |
| Section 12: Coordination table (4-row file conflict analysis) | Task 012 | COVERED |
| Section 12: Add sprint-side files to modified files list + test files + LOC update + model changes update | Task 013 | COVERED |
| Section 13: Parallelism note (Branch A/B) | Task 014 | COVERED |
| Section 13: Split task 6 into 6a/6b, add task 9 (shadow validation), default "off" | Task 015 | COVERED |
| Section 13 Phase 2: Add deferred item for sprint-pipeline gate reimbursement | Task 016 | COVERED |
| Section 14: Add assumptions A-011 through A-014 | Task 017 | COVERED |
| Section 16.5 (New): TurnLedger Integration Contract (5 economic paths, invariant) | Task 010 | COVERED |

### GAPS (Merged Plan Edits with No Matching Task)

**None found.** Every edit specified in the merged plan has a corresponding task in the tasklist. The coverage is complete.

### ORPHANS (Tasks with No Merged Plan Edit)

| Task | Type | Assessment |
|---|---|---|
| Task 007 | verify (Wave 1) | NOT AN ORPHAN -- verification task validating Wave 1 edits. Justified by the merged plan's requirement for terminology consistency across Sections 3/8/9. |
| Task 011 | verify (Wave 2) | NOT AN ORPHAN -- verification task validating new sections 9.5/9.6/16.5 against Wave 1 definitions. |
| Task 018 | verify (Wave 3) | NOT AN ORPHAN -- verification task validating Sections 12-14 consistency with earlier waves. |
| Task 019 | verify (Wave 4) | NOT AN ORPHAN -- validates unchanged sections remain untouched. Derived from merged plan's "Sections Unchanged" table. |
| Task 020 | verify (Wave 4) | NOT AN ORPHAN -- validates all 10 interaction effects are addressed. Derived from merged plan's "Interaction Effects (merged)" table. |
| Task 021 | verify (Wave 4) | NOT AN ORPHAN -- validates 9 backward compatibility invariants. Derived from merged plan's "Migration / Backward Compatibility Notes" section. |
| Task 022 | test (Wave 4) | NOT AN ORPHAN -- end-to-end coherence test. Necessary for implementation handoff quality assurance. |

**No orphans found.** All tasks map to either a specific merged plan edit or a verification/consistency check derived from the merged plan's structural requirements.

---

## Fidelity Check

### Task-by-Task Description Accuracy

| Task | Fidelity | Notes |
|---|---|---|
| 001 | HIGH | Description accurately locates "line 99" and specifies the exact paragraph content from the merged plan. Cross-refs to 9.5 and 16.5 match. |
| 002 | HIGH | Description specifies `gate_scope: GateScope = GateScope.TASK` which matches merged plan. Correctly notes roadmap pipeline bypasses scope resolution. |
| 003 | HIGH | Description enumerates all 4 required components (dual-context, enforcement_tier vs rollout_mode, mode behavior summary, `gate_passed()` note). Cross-refs match merged plan. |
| 004 | HIGH | Description includes both `gate_scope` addition and the expanded `retry_limit=0` comment. Remediation path and BUDGET_EXHAUSTED are specified. |
| 005 | HIGH | Description quotes the KPI boundary note verbatim from merged plan. References `TrailingGateResult` and `_all_gate_results`. |
| 006 | HIGH | Description correctly identifies `TrailingGateResult` and `DeferredRemediationLog` as new imports for Change 4. |
| 007 | HIGH | Verification checks are well-defined with 4 specific criteria. |
| 008 | HIGH | Description is comprehensive: 6-step lifecycle, reimbursement clarification, None-safety, threading note, rollout mode behavior matrix. All match merged plan Section 9.5. |
| 009 | HIGH | Description covers GateKPIReport, 3 metric categories, data source clarification, sprint-only note. Matches merged plan Section 9.6. |
| 010 | HIGH | Description covers all 5 economic paths (PASS, FAIL, FAIL+full, off/standalone, invariant). Matches merged plan Section 16.5. |
| 011 | HIGH | 5 verification checks are specific and traceable to content in Waves 1-2. |
| 012 | HIGH | Description specifies exact 4-row table content and "Zero merge conflicts" conclusion. Matches merged plan Section 12. |
| 013 | HIGH | Description covers sprint-side files, test files, LOC update (1,190-1,240), model changes (0->1). All match merged plan. |
| 014 | HIGH | Description quotes the parallelism note content. Branch A/B definitions match merged plan. |
| 015 | HIGH | Description covers task 6 split (6a/6b), task 9 addition with graduation criteria, default "off". Matches merged plan. |
| 016 | HIGH | Description specifies exact deferred item text. Matches merged plan. |
| 017 | HIGH | Description provides full detail for A-011 through A-014 including ID, assumption, risk, and mitigation columns. Matches merged plan. |
| 018 | HIGH | 6 verification checks are well-specified and reference correct source sections. |
| 019 | HIGH | Lists all unchanged sections correctly (1, 2, 4-7, 10, 11, 15, 16). Matches merged plan's "Sections Unchanged" table. |
| 020 | HIGH | Lists all 10 interaction effects with correct section mappings. Matches merged plan. |
| 021 | HIGH | Lists all 9 backward compatibility invariants. Matches merged plan. |
| 022 | HIGH | 5 coherence checks cover numbering, cross-refs, deduplication, unchanged verification, and readability. |

### Ambiguity Assessment

**No significant ambiguities found.** All task descriptions include:
- Exact target section/location within the spec
- Specific content to add or modify (often verbatim or paraphrased from merged plan)
- Clear acceptance criteria
- Risk assessment

**Minor note**: Task 003 says "Use the exact content from the merged plan's Section 8 edits" which is appropriate for `/sc:task-unified` execution since the executor can reference the merged plan directly. Tasks 008, 009, and 010 use the same pattern. This is a strength, not a weakness -- it prevents the tasklist from diverging from the merged plan by pointing the executor to the canonical source.

### Divergences

**None found.** Task descriptions are faithful reproductions of merged plan intent. No task contradicts or misrepresents the merged plan's specifications.

---

## Dependency Validation

### Wave Assignment Correctness

| Wave | Tasks | Dependencies Satisfied? |
|---|---|---|
| Wave 1 | 001-006 | YES -- all marked "Depends on: none". These are independent edits to existing Sections 3, 8, 9. No inter-dependencies. |
| Wave 1-verify | 007 | YES -- depends on 001-006, all in Wave 1. |
| Wave 2 | 008, 009, 010 | MOSTLY -- see note below |
| Wave 2-verify | 011 | YES -- depends on 008, 009, 010, all in Wave 2. |
| Wave 3 | 012-017 | MOSTLY -- see note below |
| Wave 3-verify | 018 | YES -- depends on 012-017, all in Wave 3. |
| Wave 4 | 019-022 | YES -- sequential chain after Wave 3-verify. |

### Dependency Issues

**Issue 1 (MINOR): Task 009 depends on Task 008 -- correct but limits Wave 2 parallelism.**

Task 009 (Section 9.6 KPI Report Integration) depends on Task 008 (Section 9.5 Sprint Executor Integration) because 9.6 references 9.5 concepts. This is correctly declared. However, Task 010 (Section 16.5) depends only on Task 003 (Section 8 enforcement_tier vs rollout_mode), not on 008. This means Tasks 008 and 010 can run in parallel within Wave 2, but Task 009 must wait for 008.

**Assessment**: The dependency graph in the tasklist correctly shows this:
```
008 (needs 003,004,005) ─┐
009 (needs 008)          ├──> 011 (verify)
010 (needs 003)          ─┘
```

Task 009 is correctly serialized after 008. Tasks 008 and 010 are correctly parallelized. **No error here.**

**Issue 2 (MINOR): Task 016 declares "no deps" but logically should reference nothing -- confirmed correct.**

Task 016 adds a Phase 2 deferred item. The content is self-contained and does not reference any Wave 1 or Wave 2 content. "Depends on: none" is accurate. It is placed in Wave 3 for organizational reasons (it modifies Section 13 alongside Tasks 014 and 015), which is acceptable.

**Issue 3 (MINOR): Task 017 declares "no deps" but adds assumptions that reference Sections 8, 9.5.**

Task 017 adds A-011 through A-014 to Section 14. These assumptions reference `resolve_gate_mode()` (Section 8, Task 003), `gate_rollout_mode` (Section 8, Task 003), and `SprintGatePolicy` (Section 9.5, Task 008). Strictly, Task 017 should depend on Tasks 003 and 008 to ensure the referenced content exists. However, since Task 017 is in Wave 3 (which runs after Waves 1 and 2), these dependencies are implicitly satisfied by the wave ordering.

**Assessment**: Not a structural error. The wave ordering provides the implicit guarantee. However, for defense-in-depth, explicitly declaring `Depends on: 003, 008` would be more robust.

### Missing Dependencies

**None found.** All dependencies are either explicitly declared or implicitly satisfied by wave ordering.

### Further Parallelization Opportunities

**Wave 3** could potentially split into sub-waves:
- Wave 3a: Tasks 012, 016, 017 (no inter-dependencies among these three)
- Wave 3b: Tasks 013, 014 (both depend on 012)
- Wave 3c: Task 015 (depends on 014)

However, this optimization is marginal since all Wave 3 tasks target the same file. The current flat Wave 3 with dependency tracking is sufficient for `/sc:task-unified` execution, which handles intra-wave dependencies.

**Wave 4** is correctly sequential (019 -> 020 -> 021 -> 022) since each verification builds on the previous one's assurance.

---

## Spec Consistency

### Will Executed Tasks Produce an Internally Consistent Spec?

**YES**, with the following analysis:

1. **Terminology consistency**: Task 007 (Wave 1-verify) explicitly checks for terminology drift between Sections 3, 8, and 9 (dual-context, enforcement_tier, rollout_mode). Task 011 (Wave 2-verify) checks new sections against Wave 1 definitions. This provides a two-layer consistency guarantee.

2. **Cross-reference integrity**: Tasks reference specific sections for cross-refs (e.g., Task 001 adds cross-refs to 9.5 and 16.5). Task 011 verifies these resolve. Task 022 does a final cross-reference audit.

3. **Numerical consistency**: Task 013 updates LOC estimates and model change counts. Task 018 verifies the LOC increase is plausible.

4. **Section numbering**: Task 022 explicitly verifies section numbering is correct with 9.5, 9.6, and 16.5 properly interleaved.

### Unchanged Sections at Risk of Inadvertent Modification

| Section | Risk | Assessment |
|---|---|---|
| Section 3 (Architecture) | LOW | Task 001 adds a note but explicitly states "The architecture diagram itself is unchanged." Task 019 verifies. |
| Section 8 (Gate Definition) | MEDIUM | Tasks 002 and 003 modify Section 8. Risk that modifications bleed into the existing `ANTI_INSTINCT_GATE` code block (beyond `gate_scope` addition) or the D-03/D-04 coexistence paragraph. Task 002's acceptance criteria ("No other fields in the gate definition are modified") mitigates this. |
| Sections 4-7 (Modules 1-4) | NONE | No tasks target these sections. Task 019 explicitly verifies they are untouched. |
| Section 11 (Contradictions) | NONE | No tasks target this section. Task 019 verifies. |

**All "unchanged" sections from the merged plan's table are protected by Task 019's explicit diff verification.**

### Acceptance Criteria Alignment with Spec Conventions

The original spec uses:
- Markdown code blocks for Python definitions
- Tables for structured data
- Cross-references via section numbers
- YAML frontmatter for gate artifacts

The tasklist's acceptance criteria are consistent with these conventions:
- Tasks 002/004 add fields to Python code blocks within markdown
- Tasks 003/008/009/010/012 add tables and structured subsections
- Tasks 001/003/008/009/010/012/017 specify cross-references by section number
- No task introduces a format alien to the existing spec

---

## Risk Assessment

### Highest Execution Risk Tasks

| Task | Risk Level | Rationale |
|---|---|---|
| **Task 003** | **HIGH** | Adds the largest single block of new content to Section 8 (dual-context definition, enforcement_tier vs rollout_mode distinction, 4-mode behavior summary). This is the conceptual linchpin -- if the content is imprecise, all downstream sections (9.5, 9.6, 16.5) inherit the imprecision. |
| **Task 008** | **HIGH** | Creates Section 9.5 with the most complex content (6-step lifecycle, reimbursement model, None-safety, threading, rollout mode behavior matrix). This section must be internally consistent and consistent with Task 003's Section 8 content. |
| **Task 010** | **MEDIUM-HIGH** | Creates Section 16.5 (TurnLedger Integration Contract). The 5 economic paths must not contradict the rollout mode behavior matrix in Section 9.5 (Task 008) or the enforcement_tier vs rollout_mode distinction in Section 8 (Task 003). |
| **Task 013** | **MEDIUM** | Modifies the file change list with specific numbers (LOC estimates, model change counts). If numbers are inconsistent with the content actually added, the spec loses credibility. |
| **Task 015** | **MEDIUM** | Splits task 6 and adds task 9 to implementation phases. The split must align with the parallelism note (Task 014) and the coordination table (Task 012). |

### Tasks That Should Be Split Further

**None.** The current granularity is appropriate:
- Each task modifies one section or subsection
- Task 003 is the largest but its content is tightly coupled (dual-context + enforcement_tier + mode table + gate_passed note all belong in the same subsection)
- Task 013 modifies multiple parts of Section 12 (modified files, test files, LOC, model changes) but these are all within the same "File Change List" section and interdependent

### Blast Radius Analysis

| Task Failure | Blast Radius | Recovery |
|---|---|---|
| Task 001 fails | LOW -- Only Section 3 affected. Downstream tasks do not depend on Section 3 content. | Re-run Task 001 independently. |
| Task 002 fails | MEDIUM -- Section 9 Step definition (Task 004) references `gate_scope`. Sections 9.5 (Task 008) and 16.5 (Task 010) reference scope resolution. | Fix Task 002, then verify Tasks 004, 008, 010 still hold. |
| Task 003 fails | HIGH -- Tasks 008, 009, 010, 012, 014, 015, 017 all reference concepts defined in Task 003. The enforcement_tier vs rollout_mode distinction is foundational. | Fix Task 003. Re-verify ALL downstream tasks via Tasks 011, 018, and Wave 4. |
| Task 008 fails | HIGH -- Task 009 directly depends on 008. Tasks 012, 013, 014, 017, 018 reference Section 9.5 concepts. | Fix Task 008. Re-run Tasks 009, 011, and all Wave 3 verifications. |
| Task 010 fails | MEDIUM -- Only Task 011 verification directly depends. Section 16.5 is referenced from Sections 3, 8, 9.5 (Tasks 001, 003, 008) but those references are forward pointers, not content dependencies. | Fix Task 010. Re-run Task 011. |
| Any Wave 4 verify task fails | LOW -- Verification tasks identify issues but do not create content. Failure means a previous task needs correction. | Fix the identified issue in the earlier task, re-run the failing verification. |

---

## Verdict

**PASS WITH NOTES**

### Justification

The tasklist is faithful to the merged refactoring plan and complete in coverage. Every merged plan edit maps to a task. No orphan tasks exist. Dependency ordering is correct. Wave assignments are sound. Acceptance criteria are specific and verifiable. The verification tasks (007, 011, 018, 019-022) provide layered consistency assurance.

### Notes

1. **Recommendation**: Task 017 should explicitly declare `Depends on: 003, 008` rather than relying on implicit wave ordering. This is a defense-in-depth improvement, not a structural error. Currently declared as "Depends on: none" which is technically safe due to wave ordering but obscures the logical dependency.

2. **Observation**: The tasklist correctly identifies that Alpha's Section 8.5 "Non-Applicability" section is NOT created (per the merged plan's Gamma-wins resolution). This is noted in the tasklist's Notes section. Good.

3. **Observation**: The summary table claims 6 waves, but the actual structure is 4 waves + 3 verify checkpoints. The wave count is semantically correct if verify checkpoints are counted as sub-waves (1, 1-verify, 2, 2-verify, 3, 3-verify, 4), yielding 7 logical phases. The "6 waves" count appears to exclude Wave 4's internal sequential chain as a single wave. This is a minor labeling ambiguity that does not affect execution.

4. **Strength**: The tasklist's instruction to "use the exact content from the merged plan" for Tasks 003, 008, 009, 010 is the correct approach. It prevents drift between the tasklist description and the canonical merged plan content. The `/sc:task-unified` executor should reference the merged plan file directly for verbatim content.

5. **Strength**: The dependency graph at the bottom of the tasklist is accurate and matches the declared dependencies in each task. This provides a visual verification path.

6. **Risk mitigation**: The highest-risk tasks (003, 008) are isolated in separate waves with verification checkpoints immediately following. This is the correct strategy -- if Task 003's content is wrong, Task 007 catches it before Wave 2 builds on it.
