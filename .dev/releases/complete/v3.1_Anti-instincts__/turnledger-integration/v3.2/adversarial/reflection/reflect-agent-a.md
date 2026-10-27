# Reflection Report: v3.2 Tasklist Validation (Agent A)

**Date**: 2026-03-20
**Tasklist**: `tasklist.md` (28 tasks, 7 waves)
**Merged Plan**: `adversarial/merged-output.md`
**Original Spec**: `wiring-verification-gate-v1.0-release-spec.md`

---

## Coverage Check

### Merged Plan Edits -> Tasklist Mapping

| Merged Plan Edit | Tasklist Task | Status |
|-----------------|---------------|--------|
| Section 4.1: Add TurnLedger Extensions subsection | T01 | COVERED |
| Section 4.4: Update WIRING_GATE.required_frontmatter_fields | T05 | COVERED |
| Section 4.5: Rewrite sprint integration pseudocode | T11 | COVERED |
| Section 5: Update file manifest | T12 | COVERED |
| Section 6.2: Replace wiring_gate_mode with scope-based fields | T02 | COVERED |
| Section 6.3: Update frontmatter contract table | T06 | COVERED |
| Section 7: Add R7 and R8 | T03 | COVERED |
| Section 8: Rewrite rollout plan | T13 | COVERED |
| Section 9: Add budget integration tests | T14 | COVERED |
| Section 10: Add SC-012 through SC-015 | T04 | COVERED |
| Section 11: Update dependency map | T15 | COVERED |
| Section 12: Rewrite tasklist index | T16 | COVERED |
| NEW Section 4.5.1: TurnLedger Budget Flow | T07 | COVERED |
| NEW Section 4.5.2: Backward Compatibility (ledger is None) | T08 | COVERED |
| NEW Section 4.5.3: Remediation Path | T09 | COVERED |
| NEW Section 4.5.4: KPI Report Extensions | T10 | COVERED |

### GAPS (merged plan edits with NO corresponding task)

1. **Section 4.3 frontmatter example update**: The merged plan (Section 6.3 entry) explicitly states "Update Section 4.3 report format example to replace `enforcement_mode: shadow` with `enforcement_scope: task` and `resolved_gate_mode: shadow`." Task T06 mentions this in its description ("Also update the report format example in Section 4.3"), so this is technically covered within T06. However, T06's target section is listed as "6.3 Gate Contract" -- the Section 4.3 edit is a secondary target buried in the description. **Minor gap**: T06 should list Section 4.3 as a secondary target section.

2. **Spec frontmatter `estimated_scope` update**: The merged plan (Section 5 entry) increases the production code estimate from ~360-430 to ~410-500. Task V05 mentions updating the frontmatter scope in its description, but this is a Wave 7 final verification task, not an edit task. **Minor gap**: The frontmatter update is deferred to verification rather than being an explicit edit task. This is acceptable if V05 is permitted to make edits, but verify tasks are typically read-only.

3. **Section 6.1 `emit_report()` signature**: The merged plan replaces `enforcement_mode` with new fields. The original spec's Section 6.1 shows `emit_report(..., enforcement_mode: str = "shadow")`. If `enforcement_mode` is being replaced everywhere, this signature should also be updated. **Neither the merged plan nor the tasklist address this.** The merged plan's "Sections Unchanged" table lists Section 6.1 as unchanged, but the `emit_report()` signature references `enforcement_mode` directly. This is a real gap in both the merged plan and the tasklist.

### ORPHANS (tasks with no merged plan traceability)

1. **V01 (Wave 2)**: Cross-reference verification for Wave 1. No explicit merged plan source, but this is a process task (verify internal consistency). **Acceptable orphan** -- verification tasks are process artifacts.

2. **V02 (Wave 4)**: Cross-reference verification for Waves 3-4. Same rationale. **Acceptable orphan.**

3. **V03 (Wave 6)**: Full spec coherence verification. **Acceptable orphan.**

4. **V04 (Wave 6)**: Section numbering verification. **Acceptable orphan.**

5. **V05 (Wave 7)**: Final sign-off. **Acceptable orphan.**

6. **T17 (Wave 7)**: BC-1 through BC-7 validation. Traces to merged plan's "Migration / Backward Compatibility Notes" section. **Not an orphan** -- has clear traceability.

7. **T18 (Wave 7)**: IE-1 through IE-7 validation. Traces to merged plan's "Interaction Effects" section. **Not an orphan.**

8. **T19 (Wave 7)**: "Sections Unchanged" validation. Traces to merged plan's "Sections Unchanged" table. **Not an orphan.**

**Verdict**: Zero true orphans. All verification tasks (V01-V05) are legitimate process tasks. All test tasks (T17-T19) trace to specific merged plan sections.

---

## Dependency Validation

### Dependency Correctness

| Task | Declared Dependencies | Assessment |
|------|----------------------|------------|
| T01 | none | CORRECT -- foundational data model, no prerequisites |
| T02 | none | CORRECT -- independent config contract edit |
| T03 | none | CORRECT -- independent risk table edit |
| T04 | none | CORRECT -- independent success criteria edit |
| V01 | T01, T02, T03, T04 | CORRECT -- verifies all Wave 1 outputs |
| T05 | T02 | CORRECT -- needs field names from 6.2 config |
| T06 | T05 | CORRECT -- frontmatter must match WIRING_GATE definition |
| T07 | T01, T02 | CORRECT -- references TurnLedger fields (T01) and config fields (T02) |
| T08 | T07 | CORRECT -- references budget flow from 4.5.1 |
| T09 | T07, T08 | CORRECT -- depends on budget flow and null-ledger behavior |
| T10 | T01 | CORRECT -- KPI fields reference TurnLedger field names |
| T11 | T02, T07, T08, T09 | CORRECT -- largest edit, depends on config, budget flow, null-ledger, remediation |
| V02 | T05, T06, T07, T08, T09, T10, T11 | CORRECT -- verifies all Wave 3-4 outputs |
| T12 | T10, T11 | CORRECT -- manifest must reflect KPI and executor changes |
| T13 | T02, T11 | CORRECT -- rollout uses config fields and sprint integration |
| T14 | T01, T09, T11 | CORRECT -- test scenarios reference TurnLedger methods, remediation, sprint integration |
| T15 | T12 | CORRECT -- dependency map must match file manifest |
| T16 | T12, T14 | CORRECT -- tasklist index references manifest and test scenarios |
| V03 | All T01-T16 | CORRECT -- full coherence check |
| V04 | V03 | CORRECT -- numbering check after coherence is confirmed |
| T17 | V03 | CORRECT -- BC validation after coherence check |
| T18 | V03 | CORRECT -- IE validation after coherence check |
| T19 | V03 | CORRECT -- unchanged-sections validation after coherence check |
| V05 | T17, T18, T19 | CORRECT -- final sign-off after all validations |

### Missing Dependencies

1. **T05 may need T01**: T05 updates `WIRING_GATE.required_frontmatter_fields`. While T05 declares dependency on T02 (for new field names from config), it should arguably also depend on T01 if the TurnLedger extensions introduce any new frontmatter requirements. **Low risk** -- the frontmatter field changes come from T02 (config rename), not T01 (model extensions).

2. **T13 should depend on V01**: T13 rewrites Section 8 rollout using config fields from T02. V01 verifies T02's correctness. If T13 runs before V01 completes, it could propagate errors from T02. **Low risk** -- T13 is in Wave 5, V01 is in Wave 2, so wave ordering already enforces this implicitly.

### Circular Dependencies

None detected.

### Parallelism Opportunities

1. **Wave 3: T05 and T06 are sequential** (T06 depends on T05), but **T07 and T08 could partially overlap with T05/T06**. T07 depends on T01 and T02 (Wave 1), not on T05. T08 depends on T07. Current wave assignment is correct -- T05, T06, T07, T08 are all in Wave 3, with T07/T08 running in parallel with T05/T06 where dependencies allow.

2. **Wave 4: T10 could run in Wave 3**. T10 depends only on T01 (Wave 1). It does not depend on any Wave 3 task. Moving T10 to Wave 3 would reduce the critical path. **Recommendation**: Move T10 to Wave 3.

3. **Wave 5: T12 and T13 could partially parallel**. T12 depends on T10 and T11. T13 depends on T02 and T11. Both share the T11 dependency but have different secondary dependencies. They are already in the same wave, which is correct.

---

## Acceptance Criteria Quality

### Specific and Verifiable Criteria

Most acceptance criteria are well-specified with concrete, countable outcomes. Strengths:

- T01: "Section 4.1 contains a subsection documenting all 3 fields and 3 methods with type signatures" -- specific count, verifiable
- T02: "Mapping table present. `SHADOW_GRACE_INFINITE` constant defined" -- concrete artifacts
- T03: "Risk table contains R1-R8 (previously R1-R6, now +2)" -- countable
- T04: "Success criteria table has SC-001 through SC-015" -- countable
- T14: "Scenario 5 explicitly asserts `== 0` for credits" -- specific assertion value

### Vague or Unmeasurable Criteria

1. **V01**: "All cross-references resolve. No contradictions between Wave 1 sections." -- The word "contradictions" is subjective. What constitutes a contradiction? **Recommendation**: Define specific checks (e.g., "field name X in Section A matches field name X in Section B").

2. **V02**: "Zero inconsistencies found." -- Same concern. However, V02 provides 8 specific sub-checks, which partially compensates.

3. **V03**: "Zero inconsistencies. All cross-references resolve." -- V03 provides 10 specific sub-checks, which is thorough. The summary criterion is redundant but acceptable.

4. **T07**: "Must stay consistent with Section 4.1.1 field definitions" appears in Risk rather than acceptance criteria. The AC says "All TurnLedger method names match Section 4.1.1" which is equivalent but better placed.

5. **T11**: "No references to `wiring_gate_mode` remain in Section 4.5" -- excellent negative criterion. All edit tasks should have similar "no orphaned references" checks. **Gap**: T02 lacks a "no remaining references to old field in Section 6.2" criterion. T02's AC focuses on what IS present, not what should be ABSENT.

---

## Section Reference Accuracy

### Task Section References vs Original Spec Structure

| Task | Referenced Section | Spec Has This Section? | Match? |
|------|-------------------|----------------------|--------|
| T01 | 4.1 Data Models | Yes (line 157) | YES |
| T02 | 6.2 Configuration Contract | Yes (line 654) | YES |
| T03 | 7 Risk Assessment | Yes (line 708) | YES |
| T04 | 10 Success Criteria | Yes (line 882) | YES |
| T05 | 4.4 Gate Definition | Yes (line 486) | YES |
| T06 | 6.3 Gate Contract | Yes (line 687) | YES |
| T07 | 4.5.1 (NEW) | N/A -- new section after 4.5 (line 537) | YES |
| T08 | 4.5.2 (NEW) | N/A -- new section after 4.5.1 | YES |
| T09 | 4.5.3 (NEW) | N/A -- new section after 4.5.2 | YES |
| T10 | 4.5.4 (NEW) | N/A -- new section after 4.5.3 | YES |
| T11 | 4.5 Sprint Integration | Yes (line 537) | YES |
| T12 | 5 File Manifest | Yes (line 596) | YES |
| T13 | 8 Rollout Plan | Yes (line 721) | YES |
| T14 | 9 Testing Strategy | Yes (line 796) | YES |
| T15 | 11 Dependency Map | Yes (line 900) | YES |
| T16 | 12 Tasklist Index | Yes (line 934) | YES |

### Section Numbering Mismatches

1. **T01 references "after line 224"**: Line 224 in the spec is the closing ``` of the WiringReport class. This is correct -- the new subsection goes after the data model code block.

2. **T02 references "line 575-576 in Section 4.5"**: Lines 574-575 in the spec show `wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"`. T02's description says "currently at line 575-576 in Section 4.5 and implied in 6.2". The spec does not have `wiring_gate_mode` in Section 6.2 -- it is in Section 4.5 (line 575) and the `WiringConfig` class in Section 6.2 does not contain it. **Minor concern**: T02 conflates the `SprintConfig` field (4.5) with the `WiringConfig` class (6.2). The description is slightly misleading but the edit target (Section 6.2) is where the new fields should be documented as part of the configuration contract, which is reasonable.

3. **T11 references "lines 546-569"**: Lines 546-569 in the spec correspond to the shadow mode pseudocode block (lines 546: `# In execute_phase_tasks()...` through line 569: `...`). This is accurate.

4. **T06 references Section 4.3 frontmatter example**: The spec's Section 4.3 (line 389) contains a report format example with `enforcement_mode: shadow` at line 404. T06 correctly identifies this needs updating.

**No section numbering mismatches found.**

---

## Wave Ordering

### Current Wave Structure

```
Wave 1 (4 tasks): T01, T02, T03, T04 -- foundation edits
Wave 2 (1 task):  V01 -- verify Wave 1
Wave 3 (4 tasks): T05, T06, T07, T08 -- gate def, frontmatter, new sections
Wave 4 (4 tasks): T09, T10, T11, V02 -- remaining sections, sprint integration, verify
Wave 5 (5 tasks): T12, T13, T14, T15, T16 -- manifest, rollout, testing, deps, tasklist
Wave 6 (2 tasks): V03, V04 -- full verification
Wave 7 (4 tasks): T17, T18, T19, V05 -- validation tests, final sign-off
```

### Optimization Opportunities

1. **Wave 2 is a single verification task (V01)**. This creates a bottleneck. V01 checks cross-references between Wave 1 outputs. Given that Wave 1 tasks are independent edits to different sections (4.1, 6.2, 7, 10), the risk of cross-reference errors is low. **Recommendation**: Collapse V01 into Wave 3 as a parallel task. Wave 3 tasks (T05, T06) depend on T02 (Wave 1) directly, so they already implicitly validate T02's output. This would save one wave.

2. **T10 (KPI extensions) in Wave 4**: T10 depends only on T01 (Wave 1). It could move to Wave 3. **Recommendation**: Move T10 to Wave 3 to reduce Wave 4 load and critical path.

3. **Wave 6 (V03, V04) and Wave 7 (T17, T18, T19, V05)**: V04 depends on V03. T17, T18, T19 all depend on V03. V05 depends on T17, T18, T19. This is a 3-wave dependency chain (V03 -> V04 + T17/T18/T19 -> V05). V04 could run in parallel with T17/T18/T19 in Wave 7, reducing to 2 waves. **Recommendation**: Merge V04 into Wave 7 alongside T17/T18/T19.

### Proposed Optimized Wave Structure

```
Wave 1 (4 tasks): T01, T02, T03, T04
Wave 2 (5 tasks): V01, T05, T06, T07, T10  (V01 merged in; T10 moved up)
Wave 3 (3 tasks): T08, T09, T11            (T08 depends on T07 from Wave 2)
Wave 4 (1 task):  V02
Wave 5 (5 tasks): T12, T13, T14, T15, T16
Wave 6 (1 task):  V03
Wave 7 (5 tasks): V04, T17, T18, T19, V05  (V04 merged into Wave 7)
```

This reduces from 7 waves to 7 waves but with better task distribution and reduced bottlenecks. The original structure is not suboptimal enough to warrant changes -- the primary concern is the single-task Wave 2.

---

## Risk Assessment

### High-Risk Edits Sequencing

1. **T11 (Section 4.5 rewrite)** is identified as the "largest single edit" and is correctly placed in Wave 4 after all prerequisite new sections (T07, T08, T09) are complete. **Properly sequenced.**

2. **T09 (Remediation Path)** is identified as "the most integration-sensitive new section" and depends on T07 and T08. **Properly sequenced.**

3. **T02 (config field rename)** is a breaking change but correctly identified as low-risk since only v3.2 development code is affected. Placed in Wave 1 with no dependencies. **Properly sequenced.**

### Interaction Effects Coverage

| Interaction Effect | Tasklist Coverage | Assessment |
|-------------------|-------------------|------------|
| IE-1: reimbursement_rate activation | T01 (floor note), T03 (R7), T14 (Scenario 5) | COVERED |
| IE-2: resolve_gate_mode replaces strings | T11 (pseudocode rewrite) | COVERED |
| IE-3: attempt_remediation activation | T09 (remediation path section) | COVERED |
| IE-4: DeferredRemediationLog type mismatch | T09 (adapter pattern) | COVERED |
| IE-5: SprintGatePolicy instantiation | T11 (pseudocode includes SprintGatePolicy) | COVERED |
| IE-6: GateKPIReport extensions | T10 (KPI section) | COVERED |
| IE-7: SprintConfig field rename downstream | T02 (migration note), T11 (field replacement) | COVERED |

All 7 interaction effects are addressed. **No gaps.**

### Backward Compatibility Coverage

| BC Item | Tasklist Coverage | Assessment |
|---------|-------------------|------------|
| BC-1: SprintConfig field rename | T02 | COVERED |
| BC-2: TurnLedger is None | T08 | COVERED |
| BC-3: Report frontmatter | T06 | COVERED |
| BC-4: Test compatibility | T14 | COVERED |
| BC-5: Cross-release order | T07 (budget flow mentions cross-release) | PARTIALLY COVERED -- no explicit mention in T07 description |
| BC-6: DeferredRemediationLog adapter | T09 | COVERED |
| BC-7: SHADOW_GRACE_INFINITE | T02 | COVERED |

**One partial gap**: BC-5 (cross-release execution order) is not explicitly addressed in any task description. T17 (Wave 7) validates BC-1 through BC-7 and specifically checks "BC-5 (cross-release order) -> mention in Section 4.5.1 or 8", but no edit task explicitly adds this content. The tasklist assumes T07 or T13 will include cross-release ordering notes, but neither task description mentions it explicitly.

---

## Summary

| Metric | Count |
|--------|-------|
| Total merged plan edits | 16 (12 section edits + 4 new sections) |
| Tasks covering merged plan edits | 16 (T01-T16) |
| Gaps (missing coverage) | 2 real gaps |
| Orphans (untraceable tasks) | 0 |
| Dependency errors | 0 |
| Missing dependencies | 1 minor (T10 could move earlier) |
| Circular dependencies | 0 |
| Vague acceptance criteria | 2 (V01, T02 missing negative criterion) |
| Section reference errors | 0 |
| Wave ordering issues | 1 (Wave 2 single-task bottleneck) |
| Interaction effects uncovered | 0 of 7 |
| BC items uncovered | 0 fully uncovered; 1 partially (BC-5) |

### Real Gaps

1. **Section 6.1 `emit_report()` signature**: The original spec's `emit_report()` at line 638 takes `enforcement_mode: str = "shadow"`. If `enforcement_mode` is being replaced throughout the spec, this signature needs updating. Neither the merged plan nor the tasklist address this. This is a gap in the merged plan itself that propagated to the tasklist.

2. **BC-5 cross-release ordering**: No edit task explicitly adds cross-release ordering documentation. T17 validates its presence but no task creates it.

### Confidence Level

**HIGH** -- The tasklist faithfully represents the merged plan with thorough coverage. The 28 tasks map cleanly to all 16 merged plan edits plus 5 verification tasks, 3 validation tests, and 4 process tasks. The two real gaps are minor: one is a gap in the merged plan itself (Section 6.1 signature), and the other (BC-5) is likely to be addressed incidentally by T07 or T13 even though not explicitly stated. Dependency ordering is correct. Wave structure is reasonable with minor optimization opportunities. Acceptance criteria are predominantly specific and verifiable.
