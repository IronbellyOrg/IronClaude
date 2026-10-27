# Tasklist Validation: v3.2 Wiring Verification Gate (Agent B)

**Date**: 2026-03-20
**Reviewer**: Independent Agent B
**Artifacts reviewed**:
- TASKLIST: `v3.2/tasklist.md` (28 tasks across 7 waves)
- MERGED PLAN: `v3.2/adversarial/merged-output.md` (3-plan adversarial merge)
- ORIGINAL SPEC: `v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`

---

## 1. Coverage Analysis

### Merged Plan Edits -> Tasklist Mapping

| Merged Plan Edit | Tasklist Task(s) | Status |
|------------------|-----------------|--------|
| Section 4.1: Add TurnLedger Extensions subsection | T01 (Wave 1) | COVERED |
| Section 4.4: Update WIRING_GATE.required_frontmatter_fields | T05 (Wave 3) | COVERED |
| Section 4.5: Replace wiring_gate_mode pseudocode | T11 (Wave 4) | COVERED |
| Section 4.5.1 (NEW): TurnLedger Budget Flow | T07 (Wave 3) | COVERED |
| Section 4.5.2 (NEW): Backward Compat / Null-Ledger | T08 (Wave 3) | COVERED |
| Section 4.5.3 (NEW): Remediation Path | T09 (Wave 4) | COVERED |
| Section 4.5.4 (NEW): KPI Report Extensions | T10 (Wave 4) | COVERED |
| Section 5: File Manifest update | T12 (Wave 5) | COVERED |
| Section 6.2: Config Contract replacement | T02 (Wave 1) | COVERED |
| Section 6.3: Gate Contract / Frontmatter update | T06 (Wave 3) | COVERED |
| Section 7: Risk Assessment R7+R8 | T03 (Wave 1) | COVERED |
| Section 8: Rollout Plan rewrite | T13 (Wave 5) | COVERED |
| Section 9: Testing Strategy (Section 9.4 + 9.1 updates) | T14 (Wave 5) | COVERED |
| Section 10: Success Criteria SC-012 through SC-015 | T04 (Wave 1) | COVERED |
| Section 11: Dependency Map additions | T15 (Wave 5) | COVERED |
| Section 12: Tasklist Index rewrite | T16 (Wave 5) | COVERED |
| BC-1 through BC-7 validation | T17 (Wave 7) | COVERED |
| IE-1 through IE-7 validation | T18 (Wave 7) | COVERED |
| Sections Unchanged assertion | T19 (Wave 7) | COVERED |
| 17 consensus + 8 majority + 4 contradiction sign-off | V05 (Wave 7) | COVERED |
| Frontmatter scope update (300-400 -> 410-500) | V05 (Wave 7) | COVERED |

### GAPS: Merged-Plan Edits with No Matching Task

1. **Section 4.3 frontmatter example update**: The merged plan (Section 6.3 entry) specifies: "Update Section 4.3 report format example." Task T06 description includes this ("Also update the report format example in Section 4.3 to replace `enforcement_mode: shadow` with `enforcement_scope: task` and `resolved_gate_mode: shadow`"). **STATUS: Covered within T06** -- no gap, but the task is doing double duty across two sections (6.3 and 4.3). This increases T06 blast radius. Consider noting this cross-section edit explicitly in a verify step.

2. **`emit_report()` signature update in Section 6.1**: The merged plan replaces `enforcement_mode` in frontmatter, but `emit_report()` in Section 6.1 (spec line 638) has parameter `enforcement_mode: str = "shadow"`. The merged plan lists Section 6.1 as "unchanged" and the tasklist follows suit. However, if `enforcement_mode` is replaced by `enforcement_scope` + `resolved_gate_mode`, the `emit_report()` signature in 6.1 arguably needs updating. **STATUS: POTENTIAL GAP.** The merged plan may have an internal inconsistency here -- it says 6.1 is unchanged, but the parameter name should logically change. If the intent is that 6.1 documents the public API as-is (with the old parameter name retained in the function signature, producing the new frontmatter fields internally), this is defensible but should be explicitly called out.

3. **CLI argument parser for `wiring_gate_mode`**: The merged plan (IE-7) mentions "CLI argument parsers" as a potential downstream consumer. No task addresses CLI flag updates. The merged plan notes Beta confirms only v3.2-new code reads this, and the tasklist relies on that. **STATUS: Acceptable risk** -- no CLI flags exist yet for `wiring_gate_mode` since v3.2 is unshipped. But this should be verified during V03.

### ORPHANS: Tasks with No Merged-Plan Edit

1. **V01 (Wave 2)**: Cross-reference verification of Wave 1. Not directly a merged-plan edit, but a valid verification task. **STATUS: Legitimate verification task, not an orphan.**

2. **V02 (Wave 4)**: Cross-reference verification of Waves 3-4. Same. **STATUS: Legitimate.**

3. **V03 (Wave 6)**: Full spec coherence verification. **STATUS: Legitimate.**

4. **V04 (Wave 6)**: Section numbering verification. **STATUS: Legitimate.**

No true orphan tasks found. All tasks map to either a merged-plan edit or a verification/test activity implied by the merged plan's structure.

---

## 2. Fidelity Check

### Task Descriptions vs. Merged Plan Intent

| Task | Fidelity | Notes |
|------|----------|-------|
| T01 | HIGH | Description accurately captures 3 fields, 3 methods, floor-to-zero note, v3.3 deferral. Matches merged plan Section 4.1 exactly. |
| T02 | HIGH | Description captures field replacement, mapping table, migration note, `SHADOW_GRACE_INFINITE` constant. Matches merged plan Section 6.2. |
| T03 | HIGH | R7 and R8 descriptions match merged plan Section 7. |
| T04 | HIGH | SC-012 through SC-015 match merged plan Section 10. |
| T05 | HIGH | Frontmatter field replacement matches merged plan Section 4.4. List count "increases from 10 to 11" is correct (`enforcement_mode` removed = -1, `enforcement_scope` + `resolved_gate_mode` added = +2, net +1). |
| T06 | HIGH | Covers both Section 6.3 table and Section 4.3 example update. Matches merged plan. |
| T07 | HIGH | Budget flow diagram, accounting table, hook signature all match merged plan Section 4.5.1. |
| T08 | HIGH | Null-ledger behavioral matrix matches merged plan Section 4.5.2. "Direct FAIL" for blocking failures explicitly called out. |
| T09 | HIGH | All 6 content items match merged plan Section 4.5.3. DeferredRemediationLog adapter with TrailingGateResult field mapping included. |
| T10 | HIGH | 6 KPI fields, `build_kpi_report()` signature, v3.3 deferral note all match merged plan Section 4.5.4. |
| T11 | HIGH | 8 pseudocode replacement items match merged plan Section 4.5. Largest edit, correctly identified as highest-risk. |
| T12 | HIGH | LOC updates and new rows match merged plan Section 5. |
| T13 | HIGH | Phase config profiles, budget effect columns, transition checklist all match merged plan Section 8. |
| T14 | HIGH | Scenarios 5-8 match merged plan Section 9. Critical floor assertion (`== 0`) for Scenario 5 included. Section 9.1 model test additions noted. |
| T15 | HIGH | 3 new nodes and executor->trailing_gate edge match merged plan Section 11. |
| T16 | HIGH | T07 decomposition and T12 addition match merged plan Section 12. |
| T17 | HIGH | BC-1 through BC-7 mapping to spec sections is complete. |
| T18 | HIGH | IE-1 through IE-7 mapping to spec sections is complete. |
| T19 | HIGH | Unchanged sections list matches merged plan. Section 4.3 frontmatter exception correctly noted. |
| V05 | HIGH | Frontmatter scope update and merged-plan coverage summary included. |

### Ambiguity/Underspecification Issues

1. **T01 -- "after line 224"**: The description references a specific line number in the spec. This is fragile if any Wave 1 task executes out of order or if the spec has been edited since the line numbers were captured. However, since T01 has no dependencies and targets Section 4.1 (which no other Wave 1 task touches), this is acceptable. The section-level anchor ("after the `WiringReport` dataclass definition") is sufficient for `/sc:task-unified` execution.

2. **T11 -- "lines 546-569 in original spec"**: Same line-number fragility. However, T11 depends on T02, T07, T08, T09, all of which insert content BEFORE Section 4.5 (in 4.1, 4.5.1, 4.5.2, 4.5.3) or AFTER (6.2), so the line numbers in Section 4.5 itself will have shifted. The description should rely on the section heading anchor ("Section 4.5 Sprint Integration pseudocode block") rather than line numbers. **MINOR ISSUE**: The executor agent should locate the pseudocode block by content pattern, not line number.

3. **T06 -- dual-section edit**: T06 modifies both Section 6.3 AND Section 4.3. For `/sc:task-unified` execution, this is fine as long as the agent understands it must touch two sections. The description is clear about both edits. No issue.

4. **T16 -- spec-internal tasklist vs. this tasklist**: T16 rewrites Section 12 of the spec (the spec's internal implementation tasklist). This is NOT the same as the refactoring tasklist being validated. The description is clear about this distinction. No ambiguity.

### Divergences from Merged Plan

No material divergences found. All task descriptions faithfully translate the merged plan's edits into actionable task specifications.

---

## 3. Dependency Validation

### Wave Assignment Correctness

| Task | Wave | Dependencies | Dependencies in Earlier Wave? | Status |
|------|------|-------------|------------------------------|--------|
| T01 | 1 | none | N/A | OK |
| T02 | 1 | none | N/A | OK |
| T03 | 1 | none | N/A | OK |
| T04 | 1 | none | N/A | OK |
| V01 | 2 | T01, T02, T03, T04 | All Wave 1 | OK |
| T05 | 3 | T02 | Wave 1 | OK |
| T06 | 3 | T05 | Wave 3 (same wave) | **FLAG** |
| T07 | 3 | T01, T02 | Wave 1 | OK |
| T08 | 3 | T07 | Wave 3 (same wave) | **FLAG** |
| T09 | 4 | T07, T08 | Wave 3 | OK |
| T10 | 4 | T01 | Wave 1 | OK |
| T11 | 4 | T02, T07, T08, T09 | Wave 1, 3, 4 (same wave for T09) | **FLAG** |
| V02 | 4 | T05, T06, T07, T08, T09, T10, T11 | Wave 3, 4 (same wave) | **FLAG** |
| T12 | 5 | T10, T11 | Wave 4 | OK |
| T13 | 5 | T02, T11 | Wave 1, 4 | OK |
| T14 | 5 | T01, T09, T11 | Wave 1, 4 | OK |
| T15 | 5 | T12 | Wave 5 (same wave) | **FLAG** |
| T16 | 5 | T12, T14 | Wave 5 (same wave) | **FLAG** |
| V03 | 6 | T01-T16 | All earlier waves | OK |
| V04 | 6 | V03 | Wave 6 (same wave) | **FLAG** |
| T17 | 7 | V03 | Wave 6 | OK |
| T18 | 7 | V03 | Wave 6 | OK |
| T19 | 7 | V03 | Wave 6 | OK |
| V05 | 7 | T17, T18, T19 | Wave 7 (same wave) | **FLAG** |

### Intra-Wave Dependency Analysis

Multiple tasks depend on other tasks within the same wave. This means those tasks are NOT truly parallel within their wave -- they must execute sequentially within the wave. This is a systematic pattern:

- **Wave 3**: T06 depends on T05; T08 depends on T07. So Wave 3 has two parallel chains: (T05 -> T06) and (T07 -> T08). These chains are independent of each other. Effective parallelism: 2 chains, not 4 independent tasks.

- **Wave 4**: T11 depends on T09 (same wave). V02 depends on all Wave 4 tasks. Effective ordering: T09 and T10 can run in parallel -> T11 -> V02. Not 4-way parallel.

- **Wave 5**: T15 depends on T12; T16 depends on T12 and T14. Effective ordering: T12, T13, T14 can run in parallel -> T15, T16 can run in parallel. Not 5-way parallel.

- **Wave 6**: V04 depends on V03. Sequential, not parallel.

- **Wave 7**: V05 depends on T17, T18, T19. Those 3 are parallel -> V05 sequential.

**Assessment**: The intra-wave dependencies are logically correct but the summary table's "estimated parallel speedup" of ~2.5x may be optimistic. The actual parallelism is lower than the wave listing suggests. This is not a correctness issue -- it is a scheduling accuracy issue.

### Missing Dependencies

1. **T05 should depend on V01 (Wave 2)**: T05 updates `WIRING_GATE.required_frontmatter_fields` and needs to know the new field names from Section 6.2 (T02). V01 verifies Wave 1 consistency. T05 lists dependency on T02 only, which is technically sufficient since V01 is a verification step that doesn't produce new content. **STATUS: Acceptable** -- V01 is a gate, not a content producer.

2. **T13 (Rollout Plan) should arguably depend on T07 (Budget Flow)**: T13 adds "budget effect columns" to the rollout table, which should be consistent with the budget flow documented in Section 4.5.1 (T07). T13 lists dependencies on T02 and T11 but not T07. Since T11 depends on T07, this is transitively covered. **STATUS: Acceptable** via transitive dependency.

3. **V03 listing "All T01-T16" as dependencies**: This is correct but means V03 cannot start until the entire Wave 5 completes. No issue.

### Further Parallelization Opportunities

1. **T10 (KPI, Wave 4) could move to Wave 3**: T10 depends only on T01 (Wave 1). It has no dependency on any Wave 2 or Wave 3 task. Moving it to Wave 3 would allow it to execute in parallel with T05/T06/T07/T08. **RECOMMENDATION: Move T10 to Wave 3.**

2. **T03 (Risk R7/R8) and T04 (Success Criteria) are truly independent**: Already correctly placed in Wave 1. No improvement possible.

3. **Wave 2 (V01 alone) is light**: V01 could potentially be folded into the beginning of Wave 3 as a pre-step, reducing total wave count by 1. However, keeping it as a separate wave provides a clear verification gate. **No recommendation to change** -- the verification gate pattern is valuable.

---

## 4. Spec Consistency

### Will the edited spec remain internally consistent?

**Yes, with one caveat.**

The tasklist, when executed in order, produces a spec where:
- All `wiring_gate_mode` references are replaced (T02, T05, T06, T11, T13, verified by V03)
- All `enforcement_mode` references are replaced (T05, T06, verified by V03)
- New subsections 4.1.1, 4.5.1-4.5.4, and 9.4 are properly nested
- Cross-references between new and existing sections are verified (V01, V02, V03, V04)
- Risk table, success criteria, file manifest, dependency map, and tasklist index are all updated consistently

**Caveat -- Section 6.1 `emit_report()` signature**:

The original spec (line 638) has:
```python
def emit_report(report: WiringReport, output_path: Path, enforcement_mode: str = "shadow") -> None:
```

The merged plan lists Section 6.1 as "unchanged." No task modifies it. But if `enforcement_mode` is being replaced throughout the spec, this signature arguably needs updating to accept `enforcement_scope` and `resolved_gate_mode` as parameters instead.

Possible interpretations:
- The function internally derives the new frontmatter fields from its own logic, and the parameter name is an implementation detail not yet changed. This is coherent if `emit_report()` is treated as a stable API whose internals adapt.
- The parameter should be renamed, and this is a gap.

**Recommendation**: Add a note to V03's checklist to explicitly verify Section 6.1's `emit_report()` signature against the frontmatter changes and document the decision (keep or update).

### Sections Marked "Unchanged" -- Risk of Inadvertent Modification

T19 (Wave 7) explicitly validates that unchanged sections remain unmodified. The only exception is Section 4.3's frontmatter example (modified by T06), which is correctly noted. No other task targets an "unchanged" section. **No risk of inadvertent modification.**

### Acceptance Criteria Alignment with Spec Conventions

All acceptance criteria follow the spec's existing patterns:
- Table entries follow existing column formats
- Code blocks use existing Python annotation style
- Cross-references use "Section X.Y" format
- Risk entries follow the Likelihood/Impact/Mitigation pattern

**No convention violations found.**

---

## 5. Risk Assessment

### Highest Execution Risk Tasks

| Rank | Task | Risk Level | Reason |
|------|------|-----------|--------|
| 1 | **T11** (Section 4.5 pseudocode rewrite) | **HIGH** | Largest single edit. 8 discrete changes to a pseudocode block. Must stay consistent with 6 other sections (4.1.1, 4.5.1-4.5.4, 6.2). Most cross-references of any task. |
| 2 | **T09** (Section 4.5.3 Remediation Path) | **MEDIUM-HIGH** | Most integration-sensitive new section. DeferredRemediationLog adapter pattern, helper function signatures, budget flow during remediation, and 3 edge cases. Incorrect specification here propagates to T11. |
| 3 | **T07** (Section 4.5.1 Budget Flow) | **MEDIUM** | Largest documentation addition. Budget flow diagram and accounting table must exactly match TurnLedger methods from T01. Foundation for T08, T09, and T11. |
| 4 | **T02** (Section 6.2 Config Contract) | **MEDIUM** | Field replacement propagates to T05, T06, T11, T13, and V03 old-reference check. If field names are wrong here, cascade failure across multiple waves. |
| 5 | **T13** (Section 8 Rollout Plan rewrite) | **MEDIUM** | Complete rewrite of 3 phase subsections. Must correctly reference `SHADOW_GRACE_INFINITE` constant from T02 and budget effects from T07/T11. |

### Tasks That Should Be Split Further

1. **T11 should be considered for splitting**: It performs 8 discrete changes to Section 4.5. However, all 8 changes are to a single pseudocode block and its surrounding notes within one section. Splitting would create artificial boundaries within a cohesive edit. **Recommendation: Keep as-is but flag as requiring careful review in V02.**

2. **T06 operates on two sections (6.3 and 4.3)**: Could be split into T06a (Section 6.3 frontmatter contract table) and T06b (Section 4.3 frontmatter example). **Recommendation: Keep as-is** -- the two edits must be consistent with each other and splitting them risks divergence.

3. **T14 adds content to two subsections (9.4 new + 9.1 existing)**: Could be split. **Recommendation: Keep as-is** -- same rationale as T06.

### Blast Radius Analysis

| Task Failure | Blast Radius | Downstream Impact |
|-------------|-------------|-------------------|
| T01 fails | HIGH | T05, T07, T08, T09, T10, T11, T14 all reference TurnLedger field/method names from T01. Entire Wave 3-5 chain is compromised. |
| T02 fails | HIGH | T05, T06, T11, T13 all reference config field names from T02. Wave 3-5 edits use wrong field names. |
| T07 fails | MEDIUM-HIGH | T08, T09, T11 depend on budget flow from T07. Section 4.5 pseudocode (T11) will be inconsistent. |
| T09 fails | MEDIUM | T11 references remediation path from T09. T14 Scenario 6 references remediation. |
| T11 fails | MEDIUM | T12 LOC estimates and T16 tasklist index depend on T11 output. V02 will catch inconsistencies. |
| T05 fails | LOW-MEDIUM | T06 depends on T05 for field names. V02 catches mismatch between 4.4 and 6.3. |
| Any Wave 1 task fails | Variable | V01 (Wave 2) catches it before Wave 3 proceeds. Wave 2 verification is an effective blast shield. |
| Any Wave 5 task fails | LOW | V03 (Wave 6) catches it. Wave 5 tasks are mostly bookkeeping (manifest, rollout, dependency map). |

**Key observation**: T01 and T02 are the highest-leverage tasks. Their correctness propagates through the entire tasklist. The Wave 2 verification gate (V01) is critical for catching errors before they cascade.

---

## 6. Verdict

### **PASS WITH NOTES**

The tasklist is faithful and complete with respect to the merged refactoring plan. All 12 section-level edits and 4 new sections from the merged plan have corresponding tasks. All 7 backward compatibility items, 7 interaction effects, and the "sections unchanged" assertion have dedicated validation tasks. The wave structure is logically sound with proper verification gates.

### Notes

**Minor Issues (3)**:

1. **Section 6.1 `emit_report()` signature**: Neither the merged plan nor the tasklist addresses whether the `enforcement_mode` parameter in the `emit_report()` public API signature (spec line 638) should be updated. This is likely an oversight in the merged plan that the tasklist inherited. Add an explicit check to V03's description: verify Section 6.1 `emit_report()` signature is consistent with the frontmatter field changes, and document the decision.

2. **Intra-wave dependencies understate true sequencing**: The execution order summary implies 3-5 parallel tasks per wave, but intra-wave dependencies (T06->T05, T08->T07, T11->T09, T15->T12, T16->T12+T14, V04->V03, V05->T17+T18+T19) reduce actual parallelism. The "~2.5x parallel speedup" estimate should be adjusted to ~1.8-2.0x. This is cosmetic, not a correctness issue.

3. **T10 (KPI, Wave 4) could be Wave 3**: T10 depends only on T01 (Wave 1). Moving it to Wave 3 would slightly improve parallelism and reduce Wave 4 load without introducing any dependency violation.

**No critical gaps or errors found.**
