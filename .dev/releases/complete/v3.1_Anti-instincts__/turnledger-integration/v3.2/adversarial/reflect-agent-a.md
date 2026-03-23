# Tasklist Validation: v3.2 Wiring Verification Gate

**Date**: 2026-03-20
**Validator**: Reflect Agent A
**Inputs**:
- Tasklist: `v3.2/tasklist.md` (28 tasks across 7 waves)
- Merged Plan: `v3.2/adversarial/merged-output.md` (3-plan adversarial merge)
- Original Spec: `v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`

---

## 1. Coverage Analysis

### Merged Plan Edits -> Tasklist Mapping

| Merged Plan Section | Change Description | Tasklist Task(s) | Status |
|---|---|---|---|
| Section 4.1: Data Models | Add subsection 4.1.1 TurnLedger Extensions (3 fields, 3 methods) | T01 | COVERED |
| Section 4.4: Gate Definition | Update `WIRING_GATE.required_frontmatter_fields` | T05 | COVERED |
| Section 4.5: Sprint Integration | Replace `wiring_gate_mode` pseudocode with TurnLedger-aware budget flow | T11 | COVERED |
| Section 5: File Manifest | Update LOC estimates, add rows | T12 | COVERED |
| Section 6.2: Configuration Contract | Replace `wiring_gate_mode` with 3 fields, mapping table, migration note | T02 | COVERED |
| Section 6.3: Gate Contract (Frontmatter) | Replace `enforcement_mode` with `enforcement_scope` + `resolved_gate_mode` | T06 | COVERED |
| Section 7: Risk Assessment | Add R7 and R8 | T03 | COVERED |
| Section 8: Rollout Plan | Reframe as config profiles with budget effects | T13 | COVERED |
| Section 9: Testing Strategy | Add Section 9.4, update 9.1, update LOC | T14 | COVERED |
| Section 10: Success Criteria | Add SC-012 through SC-015 | T04 | COVERED |
| Section 11: Dependency Map | Add 3 nodes, 1 edge | T15 | COVERED |
| Section 12: Tasklist Index | Decompose T07, add T12, update critical path | T16 | COVERED |
| NEW Section 4.5.1: TurnLedger Budget Flow | Budget flow diagram, accounting table, hook signature | T07 | COVERED |
| NEW Section 4.5.2: Backward Compatibility (ledger is None) | Null-ledger behavioral matrix | T08 | COVERED |
| NEW Section 4.5.3: Remediation Path | attempt_remediation(), helpers, DeferredRemediationLog adapter | T09 | COVERED |
| NEW Section 4.5.4: KPI Report Extensions | 6 GateKPIReport fields, build_kpi_report() update | T10 | COVERED |
| Sections Unchanged (merged) | Verify no unintended modifications to Sections 1, 2, 3.1-3.3, 4.2, 4.3 body, 4.6, 6.1, Appendix A/B | T19 | COVERED |
| BC-1 through BC-7 | Backward compatibility validation | T17 | COVERED |
| IE-1 through IE-7 | Interaction effects validation | T18 | COVERED |
| Consensus items (17) + Majority items (8) + Contradictions (4) | Final sign-off coverage | V05 | COVERED |

### GAPS: Merged Plan Edits with No Matching Task

1. **Section 4.3 frontmatter example update**: The merged plan (Section 6.3 entry) explicitly states "Update Section 4.3 report format example to replace `enforcement_mode: shadow` with `enforcement_scope: task` and `resolved_gate_mode: shadow`." Task T06 covers this as part of its description ("Also update the report format example in Section 4.3"), so this is technically covered but bundled into T06 rather than being its own task. **Risk**: Low. T06's description explicitly includes this. However, the acceptance criteria for T06 do mention "Section 4.3 example frontmatter updated to match" so this is adequately addressed.

2. **Spec frontmatter `estimated_scope` update**: The merged plan implies the frontmatter scope estimate needs updating (from "300-400 lines production code" to "410-500 lines production code"). This is covered by V05's description item (1). **Risk**: None.

3. **`SHADOW_GRACE_INFINITE` constant definition**: The merged plan (Section 6.2, BC-7) calls for defining `SHADOW_GRACE_INFINITE = 999_999` as a named constant. Task T02 includes this in its description. **Risk**: None -- covered.

4. **Section 3.3 minor annotation**: The merged plan notes "minor annotation possible in 3.3" under Sections Unchanged. No task creates this annotation, which is consistent with the merged plan's classification of Section 3.3 as unchanged. T19 validates this remains unchanged. **Risk**: None.

**No true gaps found.** All merged plan edits map to at least one task.

### ORPHANS: Tasks with No Merged Plan Edit

| Task | Purpose | Orphan? |
|---|---|---|
| V01 | Verify Wave 1 cross-refs | No -- verification task for T01-T04 |
| V02 | Verify Sections 4.4-4.5.4 and 6.3 consistency | No -- verification task for T05-T11 |
| V03 | Full spec coherence verification | No -- comprehensive cross-check |
| V04 | Verify section numbering and document structure | No -- structural integrity check |
| V05 | Final sign-off | No -- maps to merged plan's consensus/majority/contradiction resolution |

**No orphans found.** All tasks trace to either a merged plan edit or a necessary verification/validation step.

---

## 2. Fidelity Check

### Task Descriptions vs. Merged Plan Intent

| Task | Fidelity | Notes |
|---|---|---|
| T01 | HIGH | Description matches merged plan Section 4.1 exactly. Floor-to-zero behavior, method signatures, field types, and v3.3 deferral note all present. `models.py:488-525` reference included per Gamma. |
| T02 | HIGH | Description matches merged plan Section 6.2 exactly. All 3 replacement fields, mapping table, migration note, `SHADOW_GRACE_INFINITE` constant, and Beta's confirmation of v3.2-only consumers all present. |
| T03 | HIGH | Matches merged plan Section 7. R7 and R8 descriptions faithful to merged plan. |
| T04 | HIGH | Matches merged plan Section 10. SC-012 through SC-015 descriptions faithful. |
| T05 | HIGH | Matches merged plan Section 4.4. Replacement of `enforcement_mode` with two new fields specified. Field count increase from 10 to 11 noted. |
| T06 | HIGH | Matches merged plan Section 6.3. Includes 4.3 example update. |
| T07 | HIGH | Matches merged plan New Section 4.5.1. Budget flow diagram, accounting table, hook signature, null-ledger guard all specified. |
| T08 | HIGH | Matches merged plan New Section 4.5.2. All 6 behavioral matrix rows enumerated. "Direct FAIL" for blocking + no ledger explicitly called out. |
| T09 | HIGH | Matches merged plan New Section 4.5.3. All 6 content items enumerated. DeferredRemediationLog adapter with TrailingGateResult field mapping (Gamma IE-4) present. |
| T10 | HIGH | Matches merged plan New Section 4.5.4. All 6 KPI fields, build_kpi_report() signature, v3.3 deferral note present. |
| T11 | HIGH | Matches merged plan Section 4.5. All 8 change items enumerated. Largest edit correctly flagged. |
| T12 | HIGH | Matches merged plan Section 5. LOC updates, new rows, totals all specified. |
| T13 | HIGH | Matches merged plan Section 8. Config profiles, budget effect columns, transition checklist all specified. |
| T14 | HIGH | Matches merged plan Section 9. Scenarios 5-8, model unit tests, LOC update, and critical floor assertion all specified. |
| T15 | HIGH | Matches merged plan Section 11. 3 nodes, 1 edge, manifest alignment note all present. |
| T16 | HIGH | Matches merged plan Section 12. T07a/T07b/T07c split, T12 addition, dependency graph and critical path updates all specified. |
| T17 | HIGH | BC-1 through BC-7 mapping fully specified with section cross-references. |
| T18 | HIGH | IE-1 through IE-7 mapping fully specified with section cross-references. |
| T19 | HIGH | Unchanged sections list matches merged plan. Section 4.3 frontmatter exception noted. |
| V01-V05 | HIGH | Verification tasks are thorough with specific check items enumerated. |

### Ambiguity Assessment for /sc:task-unified Execution

1. **T01 -- "after line 224"**: The description specifies insertion "after the `WiringReport` dataclass definition (after line 224)." Line numbers are fragile -- by the time T01 executes, the line number may have shifted if any prior edit touched this file. However, since T01 is Wave 1 (no prior edits to this file), the line reference is valid for the first execution. **Recommendation**: The anchor phrase "after the `WiringReport` dataclass definition" is sufficient; the line number is supplementary.

2. **T11 -- "lines 546-569 in original spec"**: Same fragility concern, but T11 is Wave 4. By this point, T01 will have inserted content earlier in Section 4.1, which shifts line numbers. **Risk**: Medium. The section heading "4.5 Sprint Integration" and the code block starting with `if config.wiring_gate_mode == "off":` are better anchors. The task description does include "the `wiring_gate_mode` string-switch pseudocode block" as a semantic anchor, which is sufficient.

3. **T06 -- dual-section edit**: T06 modifies both Section 6.3 (frontmatter contract table) AND Section 4.3 (report format example). This is a cross-section edit in a single task. For `/sc:task-unified`, this is acceptable but slightly increases execution complexity. **Risk**: Low.

4. **T16 -- renaming in-spec tasks**: T16 renames spec-internal task IDs (T07 -> T07a/T07b/T07c, adds T12). These are SPEC DOCUMENT task IDs in Section 12, not the tasklist's own T-numbers. This distinction is clear in the description but could confuse an executor that conflates the two ID spaces. **Risk**: Low -- the description explicitly says "Decompose T07 into: T07a..."

**No descriptions are underspecified to the point of risking incorrect execution.**

---

## 3. Dependency Validation

### Wave Assignment Correctness

| Task | Wave | Dependencies | Dependencies in Earlier Wave? | Valid? |
|---|---|---|---|---|
| T01 | 1 | none | N/A | YES |
| T02 | 1 | none | N/A | YES |
| T03 | 1 | none | N/A | YES |
| T04 | 1 | none | N/A | YES |
| V01 | 2 | T01, T02, T03, T04 | All Wave 1 | YES |
| T05 | 3 | T02 | Wave 1 | YES |
| T06 | 3 | T05 | Wave 3 (same wave) | **FLAG** |
| T07 | 3 | T01, T02 | Wave 1 | YES |
| T08 | 3 | T07 | Wave 3 (same wave) | **FLAG** |
| T09 | 4 | T07, T08 | Wave 3 | YES |
| T10 | 4 | T01 | Wave 1 | YES |
| T11 | 4 | T02, T07, T08, T09 | Waves 1, 3, 4 (same wave for T09) | **FLAG** |
| V02 | 4 | T05-T11 | Waves 3-4 (same wave for T09-T11) | **FLAG** |
| T12 | 5 | T10, T11 | Wave 4 | YES |
| T13 | 5 | T02, T11 | Waves 1, 4 | YES |
| T14 | 5 | T01, T09, T11 | Waves 1, 4 | YES |
| T15 | 5 | T12 | Wave 5 (same wave) | **FLAG** |
| T16 | 5 | T12, T14 | Wave 5 (same wave) | **FLAG** |
| V03 | 6 | T01-T16 | Waves 1-5 | YES |
| V04 | 6 | V03 | Wave 6 (same wave) | **FLAG** |
| T17 | 7 | V03 | Wave 6 | YES |
| T18 | 7 | V03 | Wave 6 | YES |
| T19 | 7 | V03 | Wave 6 | YES |
| V05 | 7 | T17, T18, T19 | Wave 7 (same wave) | **FLAG** |

### Intra-Wave Dependency Issues

Eight tasks have dependencies on other tasks within the same wave. This means those waves cannot be fully parallelized as presented:

**Wave 3**: T06 depends on T05; T08 depends on T07. This means Wave 3 has two parallel chains: `T05 -> T06` and `T07 -> T08`. T05 and T07 can run in parallel, then T06 and T08 can run in parallel. **This is correct execution behavior -- the wave notation implies parallel start but respects declared dependencies.** If the executor honors dependency declarations, this is fine. If the executor treats all wave members as unconditionally parallel, T06 and T08 would execute before their dependencies complete.

**Wave 4**: T11 depends on T09 (same wave). V02 depends on T09, T10, T11 (same wave). This means the actual execution order within Wave 4 is: `T09 + T10 (parallel)` -> `T11` -> `V02`. The wave is effectively sequential for T11 and V02.

**Wave 5**: T15 depends on T12; T16 depends on T12 and T14. Execution order: `T12 + T13 + T14 (parallel, T13 independent)` -> `T15 + T16 (parallel after T12 completes; T16 also waits for T14)`.

**Wave 6**: V04 depends on V03. Sequential within wave.

**Wave 7**: V05 depends on T17, T18, T19. Execution: `T17 + T18 + T19 (parallel)` -> `V05`.

**Assessment**: The intra-wave dependencies are all correctly declared. The wave structure is valid IF the executor treats dependency declarations as authoritative and wave assignments as "earliest possible wave." This is the standard interpretation for `/sc:task-unified`. **No incorrect wave assignments found.**

### Missing Dependencies

1. **T05 lists dependency on T02 only**: T05 modifies `WIRING_GATE.required_frontmatter_fields` to use `enforcement_scope` and `resolved_gate_mode`. These field names come from the Section 6.3 changes (T06's domain), but T05 actually derives them from the merged plan's contradiction resolution, not from T06's output. T05 needs to know the new field names, which are established in T02's mapping table. **The dependency on T02 is correct and sufficient.**

2. **T13 lists dependency on T02 and T11**: T13 rewrites Section 8 rollout phases using config profiles. It needs T02's field definitions (correct) and T11's sprint integration context (correct). However, T13 also references `SHADOW_GRACE_INFINITE` defined in T02's edit. This is already covered by the T02 dependency. **No missing dependency.**

3. **T14 lists dependency on T01, T09, T11**: T14 adds testing scenarios that reference TurnLedger methods (T01), remediation path (T09), and sprint integration (T11). It also needs to update the 9.1 unit test list with model tests. **No missing dependency.**

### Parallelization Opportunities

The current wave structure is already well-parallelized. The only potential improvement:

- **T10 could move to Wave 3**: T10 (KPI Report Extensions, Section 4.5.4) depends only on T01. It is currently in Wave 4. Moving it to Wave 3 would allow it to run parallel with T05/T06/T07/T08. However, placing it in Wave 4 keeps it adjacent to T09 and T11, which reference related content. **Recommendation**: Moving T10 to Wave 3 is safe but provides minimal speedup since Wave 3 already has 4 tasks. The current placement is defensible for readability.

---

## 4. Spec Consistency

### Internal Consistency After All Edits

Executing all 28 tasks in order produces a spec with the following structural changes:

1. **New subsections**: 4.1.1, 4.5.1, 4.5.2, 4.5.3, 4.5.4, 9.4 -- all correctly nested under their parents.
2. **Modified sections**: 4.4, 4.5, 5, 6.2, 6.3, 7, 8, 9 (9.1 list), 10, 11, 12 -- all with specific, bounded edits.
3. **Unchanged sections**: 1, 2, 3.1-3.3, 4.2, 4.3 body (frontmatter example changed per T06), 4.6, 6.1, Appendix A, Appendix B.

**Potential consistency risks**:

1. **`enforcement_mode` reference in Section 4.3 report example**: The original spec (line 404) shows `enforcement_mode: shadow` in the example report frontmatter. T06 updates this to `enforcement_scope: task` and `resolved_gate_mode: shadow`. T19 verifies Section 4.3 body is unchanged but explicitly excepts the frontmatter example. **Consistent.**

2. **`enforcement_mode` in Section 4.4 WIRING_GATE constant**: The original spec (line 499) lists `"enforcement_mode"` in `required_frontmatter_fields`. T05 replaces this with `"enforcement_scope"` and `"resolved_gate_mode"`. **Consistent with T06's Section 6.3 changes.**

3. **`enforcement_mode` in Section 6.3 frontmatter contract table**: The original spec (line 694-704) has no `enforcement_mode` row in the frontmatter contract table -- it was in `required_frontmatter_fields` but missing from the contract table. T06 adds `enforcement_scope` and `resolved_gate_mode` rows. **This actually fixes a pre-existing gap in the original spec.**

4. **`wiring_gate_mode` in Section 4.5**: The original spec (lines 549-576) uses `config.wiring_gate_mode` throughout. T11 replaces all references. V02 and V03 verify no orphaned references remain. **Consistent.**

5. **`wiring_gate_mode` in Section 6.2**: The original spec has no explicit `wiring_gate_mode` in Section 6.2 (it's a `WiringConfig` section, not `SprintConfig`). The field is defined in Section 4.5 (line 575). T02 targets "Section 6.2 Configuration Contract" but the actual `wiring_gate_mode` definition is at the end of Section 4.5. **Potential issue**: T02's section reference may be slightly inaccurate -- the original spec's Section 6.2 defines `WiringConfig`, not `SprintConfig`. The `wiring_gate_mode` field on `SprintConfig` is documented at the end of Section 4.5 (lines 572-576). However, it makes sense to move the SprintConfig fields to Section 6.2 as a configuration contract. **Risk**: Low -- the task executor must understand that the `SprintConfig` field currently lives in Section 4.5 and should be relocated/updated in Section 6.2.

6. **Section 12 task ID namespace**: T16 renames spec-internal tasks (T07 -> T07a/T07b/T07c). These are implementation task IDs within the spec document, not the tasklist's own IDs. Appendix A references T02, T03, T04, T05, T07, T08. After T16 executes, the spec's T07 reference in Appendix A may be stale. **Gap**: T16 does not mention updating Appendix A cross-references to reflect the T07 split. V03 check item (4) verifies "All file manifest entries in Section 5 have corresponding tasks in Section 12" but does not check Appendix A's task references. **Risk**: Low -- Appendix A is a forensic cross-reference and "T07" in that context refers to the original sprint task, not the decomposed sub-tasks.

### Sections Marked "Unchanged" That Could Be Inadvertently Modified

1. **Section 6.1 Public API**: `emit_report()` signature (line 636-644) includes `enforcement_mode: str = "shadow"` parameter. If the frontmatter field name changes from `enforcement_mode` to `enforcement_scope` + `resolved_gate_mode`, should the `emit_report()` parameter also change? The merged plan lists Section 6.1 as "unchanged" and T19 validates this. **However**, the `emit_report()` function generates frontmatter that includes the field. If the field name changes in the output but the parameter name stays `enforcement_mode`, there's a semantic mismatch. **Risk**: Medium. The merged plan may have intentionally kept the parameter name for backward compatibility (the parameter is the input concept; the frontmatter fields are the output). But this should be explicitly noted. **RECOMMENDATION**: Add a note to T06 or T11 clarifying that `emit_report()`'s `enforcement_mode` parameter is an internal input that gets mapped to `enforcement_scope` + `resolved_gate_mode` in frontmatter output.

2. **Section 4.2 Analysis Functions**: Listed as unchanged by all plans. No task modifies these sections. **Safe.**

3. **Section 4.6 Deviation Count Reconciliation**: Listed as unchanged. No task modifies this. **Safe.**

### Acceptance Criteria Alignment with Spec Conventions

The original spec uses specific patterns:
- Code blocks with Python syntax highlighting
- Tables with `|` delimiters
- Numbered lists for algorithms
- Frontmatter YAML format
- `SC-XXX` numbering for success criteria
- `R[N]` numbering for risks

All task acceptance criteria align with these conventions. SC-012 through SC-015 follow the SC-XXX pattern. R7 and R8 follow the R[N] pattern. New subsection numbering (4.1.1, 4.5.1-4.5.4, 9.4) follows the existing hierarchical scheme.

---

## 5. Risk Assessment

### Highest Execution Risk Tasks

| Task | Risk Level | Rationale |
|---|---|---|
| **T11** | HIGH | Largest single edit. Replaces entire Section 4.5 pseudocode. Must stay consistent with 6 other sections (4.1.1, 4.5.1-4.5.4, 6.2). Has 4 dependencies. If executed incorrectly, creates cascading inconsistencies caught only at V02/V03. |
| **T09** | MEDIUM-HIGH | Most integration-sensitive new section. DeferredRemediationLog adapter pattern, TrailingGateResult field mapping, and remediation budget flow are all novel specifications that must be precise. |
| **T07** | MEDIUM | Largest documentation addition (new section). Must be internally consistent with T01's field definitions and T02's config definitions. |
| **T02** | MEDIUM | Introduces the foundational config field change that propagates to T05, T06, T11, T13. If the mapping table or field names are slightly wrong, 5 downstream tasks inherit the error. |
| **T13** | MEDIUM | Rewriting Section 8 from prose to config profiles requires understanding the full scope/grace_period semantics. Must correctly map shadow/soft/full to field values. |

### Tasks That Should Be Split

1. **T11 (8 change items)**: This task lists 8 distinct modifications to Section 4.5. Each is conceptually distinct (signature change, conditional replacement, debit addition, credit addition, remediation path, shadow path, config field replacement, configuration note update). However, they all operate on a single contiguous pseudocode block, making splitting impractical -- partial edits would leave the section in an inconsistent state. **Recommendation**: Do not split, but ensure V02 is thorough.

2. **T14 (dual-section edit)**: T14 modifies both Section 9.4 (new) and Section 9.1 (existing list update) plus updates LOC estimates. These are three distinct actions. **Recommendation**: Acceptable as-is since all are in the same Section 9 family.

3. **T06 (dual-section edit)**: Modifies Section 6.3 AND Section 4.3 frontmatter example. **Recommendation**: Acceptable -- the two changes are tightly coupled (frontmatter contract must match frontmatter example).

### Blast Radius Analysis

| Failed Task | Blast Radius | Recovery |
|---|---|---|
| T01 fails | T07, T08 blocked; T05-T11 indirectly affected. Field names propagate everywhere. | Must fix before any Wave 3+ work. |
| T02 fails | T05, T07, T11, T13 blocked. Config field names propagate to 5+ sections. | Must fix before Wave 3+. |
| T11 fails | V02 fails. T12, T13, T14 may proceed but Section 4.5 is inconsistent. | Revert and re-execute. Wave 5 blocked. |
| T09 fails | T11's remediation path reference is dangling. T14 scenario 6 has no spec backing. | Fix T09, then T11 can proceed. |
| V01 fails | Inconsistency found. Must fix T01-T04 before Wave 3. | Identify which T0x has the error, fix, re-run V01. |
| V03 fails | Must identify root cause across all T01-T16 edits. Late-stage failure. | Potentially expensive; trace inconsistency back to source task. |

---

## 6. Specific Findings

### Finding F-1: Section 6.1 emit_report() parameter name mismatch (MEDIUM)

The original spec's Section 6.1 (line 638) defines:
```python
def emit_report(report: WiringReport, output_path: Path, enforcement_mode: str = "shadow") -> None:
```

The merged plan lists Section 6.1 as "unchanged." However, if frontmatter output changes from `enforcement_mode` to `enforcement_scope` + `resolved_gate_mode`, the `emit_report()` function's parameter interface has a semantic gap. Either:
- (a) The parameter should be renamed/refactored (but this contradicts "Section 6.1 unchanged")
- (b) The parameter name stays `enforcement_mode` as an internal concept, and the function maps it to the new frontmatter fields internally

**Recommendation**: Add a clarifying note to T06 or T11 that `emit_report()`'s `enforcement_mode` parameter is intentionally retained as an internal interface and mapped to the two new frontmatter fields at serialization time. Alternatively, add this as a note in T07 (Section 4.5.1 budget flow) where the hook signature is documented.

### Finding F-2: Appendix A task cross-references after T16 (LOW)

Appendix A references "T07: Sprint integration (shadow mode hook)" in the "Addressed By" column (line 963). After T16 splits T07 into T07a/T07b/T07c in Section 12, Appendix A's reference to "T07" is ambiguous. T19 checks that Appendix A is "unchanged," which means this stale reference persists.

**Recommendation**: Either (a) accept the minor staleness since Appendix A is a forensic cross-reference to the original spec's task structure, or (b) add a note to T16 to update Appendix A references.

### Finding F-3: Section 6.2 target accuracy (LOW)

T02 targets "Section 6.2 Configuration Contract" but the original spec's Section 6.2 contains `WiringConfig`, not `SprintConfig`. The `SprintConfig.wiring_gate_mode` field is defined at the end of Section 4.5 (lines 572-576). T02 is effectively creating new `SprintConfig` content within Section 6.2, which is a structural reorganization, not just a field replacement.

**Recommendation**: T02's description is self-consistent ("Replace `wiring_gate_mode: Literal[...]` in the `SprintConfig` reference (currently at line 575-576 in Section 4.5 and implied in 6.2)"). The parenthetical acknowledges the current location. This is adequate for execution, but the executor should understand they may need to move the SprintConfig field definition from Section 4.5 to Section 6.2.

### Finding F-4: V01 check item (5) references Section 4.5 future update (LOW)

V01 states: "No orphaned references to `wiring_gate_mode` remain in Sections 4.1 or 6.2 (Section 4.5 will be updated in Wave 3-4)." This is accurate -- Section 4.5's `wiring_gate_mode` references are not cleaned up until T11 (Wave 4). V01 correctly scopes its check to Sections 4.1 and 6.2 only. **No issue.**

---

## 7. Verdict

### **PASS WITH NOTES**

The tasklist is faithful and complete. All merged plan edits map to tasks. All tasks map to merged plan edits or necessary verification steps. Wave assignments respect dependencies. Acceptance criteria are specific and testable.

**Notes requiring attention before execution**:

1. **F-1 (MEDIUM)**: The `emit_report()` parameter name `enforcement_mode` in Section 6.1 creates a semantic gap when frontmatter fields change. Add a clarifying note to T06 or T07 about the intentional retention of the internal parameter name and its mapping to new frontmatter fields.

2. **F-2 (LOW)**: Appendix A task references will be stale after T16. Accept or add a minor update to T16.

3. **F-3 (LOW)**: T02's section target (6.2) vs. current field location (4.5) requires the executor to understand it may involve structural relocation. The description's parenthetical is adequate but could be more explicit.

4. **Intra-wave dependencies**: Waves 3, 4, 5, 6, and 7 all contain tasks that depend on other tasks in the same wave. The executor must honor dependency declarations within waves, not treat all wave members as unconditionally parallel. This is standard `/sc:task-unified` behavior but worth confirming.

**No critical gaps or errors found. The tasklist is ready for execution.**
