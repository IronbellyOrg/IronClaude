# Reflection Report: v3.1 Tasklist Validation (Agent B)

> **Date**: 2026-03-20
> **Validator**: Agent B
> **Spec**: `anti-instincts-gate-unified.md` (16 sections, ~1509 lines)
> **Merged Plan**: `adversarial/merged-output.md` (Alpha/Beta/Gamma consensus)
> **Tasklist**: `tasklist.md` (22 tasks, 6 waves)

---

## Coverage Check

### Merged Plan Edits vs Tasklist Mapping

| Merged Plan Edit | Tasklist Task(s) | Status |
|-----------------|-----------------|--------|
| Section 3: Add dual-context note after architecture diagram | Task 001 | COVERED |
| Section 8: Add `gate_scope: GateScope.TASK` to ANTI_INSTINCT_GATE | Task 002 | COVERED |
| Section 8: Add Coexistence with Sprint-Pipeline subsection (dual-context, enforcement tier vs rollout mode, rollout mode behavior, gate_passed() note) | Task 003 | COVERED |
| Section 9 Change 2: Add `gate_scope=GateScope.TASK` to Step definition | Task 004 | COVERED |
| Section 9 Change 2: Expand `retry_limit=0` comment with remediation/BUDGET_EXHAUSTED | Task 004 | COVERED |
| Section 9 Change 3: Add KPI Reporting Boundary note | Task 005 | COVERED |
| Section 9 Change 4: Add TrailingGateResult + DeferredRemediationLog imports | Task 006 | COVERED |
| Section 9.5 (new): Sprint Executor Integration (6-step lifecycle, reimbursement, None-safety, threading, rollout matrix) | Task 008 | COVERED |
| Section 9.6 (new): KPI Report Integration | Task 009 | COVERED |
| Section 12: Add coordination table | Task 012 | COVERED |
| Section 12: Add sprint-side files to modified/test file lists, update LOC/model changes count | Task 013 | COVERED |
| Section 13: Add parallelism note (Branch A/B) | Task 014 | COVERED |
| Section 13: Split task 6 into 6a/6b, add task 9 (shadow-mode validation), default "off" | Task 015 | COVERED |
| Section 13 Phase 2: Add deferred item for sprint-pipeline reimbursement | Task 016 | COVERED |
| Section 14: Add assumptions A-011 through A-014 | Task 017 | COVERED |
| Section 16.5 (new): TurnLedger Integration Contract | Task 010 | COVERED |

### GAPS (Merged Plan Edits with No Corresponding Task)

**GAP-1: Migration/Backward Compatibility Notes not explicitly tasked**

The merged plan includes 9 specific backward compatibility notes (lines 476-493) that are substantive design commitments. While several are implicitly addressed by individual tasks (e.g., `gate_rollout_mode` defaults to "off" is in Task 015, None-safety is in Task 008/010), the merged plan treats these as a consolidated checklist. No task explicitly ensures all 9 notes are embedded in the spec text. Task 021 (verify backward compatibility invariants) checks them post-hoc, but there is no edit task that adds the ones not covered by other tasks. Specifically:

- Note 4 (implementation can be staged) -- no edit task adds this text to the spec
- Note 5 (execution order unconstrained) -- no edit task adds this text to the spec
- Note 7 (`pipeline/gates.py` additive change is safe) -- partially covered by Task 012's coordination table but not as an explicit invariant statement
- Note 8 (TurnLedger migration to `pipeline/models.py` is separate) -- no edit task adds this to the spec
- Note 9 (existing tests pass without modification) -- no edit task adds this to the spec

**Severity**: MEDIUM. Task 021 verifies these as "explicitly stated or implied by the spec edits" which allows implicit coverage. But Notes 4, 5, 8, 9 are not implied by any edit -- they are design decisions that should be stated somewhere.

**GAP-2: Interaction Effect 3 (anti-instinct x wiring gate ordering) has no dedicated edit task**

The merged plan's interaction effect #3 states: "Both run post-task sequentially. Wiring hook fires first, then gate hook. Shared `DeferredRemediationLog` and `ledger`." Task 020 checks that this is documented, but no edit task creates the documentation. The rollout mode behavior matrix in Task 008 (Section 9.5) covers the gate lifecycle but does not explicitly address ordering relative to the v3.0 wiring gate.

**Severity**: LOW. This is a narrow interaction that could be a one-line note in Section 9.5.

**GAP-3: Interaction Effect 7 (structural audit budget impact) has no dedicated edit task**

The merged plan identifies: "Phase 2 STRICT enforcement failure in sprint context debits turns with no reimbursement." Task 020 checks this is documented, but no edit task adds it. The structural audit (Section 7/9 Change 1) is Phase 1 warning-only, so the budget impact is a Phase 2 concern. However, the merged plan flags it at Medium confidence as something that should be documented now.

**Severity**: LOW. Phase 2 concern; could be a note in Section 9.5 or Section 14.

### ORPHANS (Tasks Not Traceable to Merged Plan)

No orphan tasks found. All 22 tasks trace directly to merged plan edits, new sections, or verification activities.

---

## Dependency Validation

### Dependency Correctness

| Task | Declared Dependencies | Assessment |
|------|----------------------|------------|
| 001-006 | none | CORRECT -- Wave 1 tasks are independent of each other |
| 007 | 001-006 | CORRECT -- verification requires all Wave 1 edits complete |
| 008 | 003, 004, 005 | CORRECT -- uses dual-context terms, gate_scope, KPI boundary from Wave 1 |
| 009 | 008 | CORRECT -- references Section 9.5 concepts |
| 010 | 003 | CORRECT -- references enforcement_tier vs rollout_mode from Section 8 |
| 011 | 008, 009, 010 | CORRECT -- verifies all new sections |
| 012 | 008 | CORRECT -- coordination table motivated by sprint executor integration |
| 013 | 012 | CORRECT -- expanded file list needs coordination table context |
| 014 | 012 | CORRECT -- parallelism note relies on zero-conflict conclusion |
| 015 | 014 | CORRECT -- task split aligns with Branch A/B from parallelism note |
| 016 | none | CORRECT -- additive table row, no dependencies |
| 017 | none | CORRECT -- additive table rows, no dependencies |
| 018 | 012-017 | CORRECT -- verifies all Wave 3 edits |
| 019 | 018 | CORRECT -- must verify after all edits complete |
| 020 | 019 | CORRECT -- interaction effects check after unchanged sections verified |
| 021 | 020 | CORRECT -- backward compat check after interaction effects |
| 022 | 021 | CORRECT -- final coherence after all verification |

### Missing Dependencies

**MISSING-DEP-1**: Task 008 should also depend on Task 002 (not just 003, 004, 005). Section 9.5's lifecycle references `GateScope.TASK` which is introduced in Task 002. Currently the dependency is transitive (008 depends on 003 which is in the same wave as 002, and Wave 2 depends on Wave 1 verification via Task 007), so this is not a functional gap, but the explicit dependency is missing.

**MISSING-DEP-2**: Task 010 should also depend on Task 008 (Section 9.5). Section 16.5's economic paths reference Section 9.5's lifecycle steps. The merged plan's cross-refs for Section 16.5 list "Section 9.5" as a cross-ref. Currently Task 010 only depends on Task 003. Since 008 and 010 are both Wave 2, and Task 011 (verify) catches inconsistencies, this is a sequencing concern within the wave rather than a blocking error.

**Severity**: LOW for both. The wave structure and verification tasks provide implicit ordering.

### Circular Dependencies

None found.

### Sequential Tasks That Could Run in Parallel

**PARALLEL-1**: Tasks 016 and 017 have `none` dependencies and are placed in Wave 3. They could technically run in Wave 1 or Wave 2 since they have no dependencies on any other task. However, their placement in Wave 3 is defensible: they are downstream-referencing sections (Section 13 Phase 2, Section 14) that are more coherent when edited after the upstream content they reference exists.

**PARALLEL-2**: Within Wave 3, Tasks 012, 016, and 017 can all run in parallel (no inter-dependencies). Tasks 013 and 014 depend on 012. Task 015 depends on 014. The tasklist's dependency graph correctly shows this. However, the header says "Wave 3 (parallel, after 011)" which may mislead -- not all Wave 3 tasks are parallel. Tasks 013 and 015 are sequential within the wave.

---

## Acceptance Criteria Quality

### Specific and Verifiable Criteria

Most acceptance criteria are well-specified with concrete, checkable conditions. Highlights:

- Task 002: "The `GateCriteria(...)` constructor includes `gate_scope=GateScope.TASK`. No other fields in the gate definition are modified." -- Binary, verifiable.
- Task 008: Lists all 5 required components (lifecycle steps, reimbursement note, None-safety, threading note, rollout matrix) plus cross-refs. -- Enumerated checklist.
- Task 019: "Diff shows zero modifications to the listed sections." -- Mechanically verifiable.

### Vague or Unmeasurable Criteria

**VAGUE-1**: Task 022, criterion (5): "Document reads coherently as a unified spec (not as a patchwork of adversarial plan fragments)." This is subjective. "Coherently" has no objective measure. Consider adding: "No paragraph repeats content from another section verbatim. Terminology is consistent (same term used for same concept throughout)."

**VAGUE-2**: Task 018, criterion (6): "Section 12 LOC estimate increase (~150-200 LOC) is plausible given the sprint-side additions." "Plausible" is subjective. Consider: "LOC estimate accounts for sprint/executor.py (~80-120 LOC), sprint/models.py (~10 LOC), and two test files (~60-80 LOC each)."

**VAGUE-3**: Task 007, criterion (2): "Dual-context terminology is consistent across Section 3 note, Section 8 subsection, and Section 9 KPI boundary note." "Consistent" needs a reference terminology list. What are the canonical terms? The merged plan uses "standalone roadmap" and "sprint-invoked roadmap" -- these should be the canonical terms in the acceptance criteria.

---

## Section Reference Accuracy

### Spec Section Structure (actual)

| # | Section Title |
|---|--------------|
| 1 | Problem Statement |
| 2 | Evidence: The cli-portify Bug |
| 3 | Architecture |
| 4 | Module 1: Obligation Scanner |
| 5 | Module 2: Integration Contract Extractor |
| 6 | Module 3: Fingerprint Extraction |
| 7 | Module 4: Spec Structural Audit |
| 8 | Gate Definition |
| 9 | Executor Integration |
| 10 | Prompt Modifications |
| 11 | Contradiction Resolutions |
| 12 | File Change List |
| 13 | Implementation Phases |
| 14 | Shared Assumptions and Known Risks |
| 15 | V5-3 AP-001 Subsumption by V2-A |
| 16 | Rejected Alternatives |

### Mismatches

**MISMATCH-1**: Task 003 references "spec lines 1077-1083" for the D-03/D-04 paragraph. The actual spec has the D-03/D-04 content at lines 1079-1083. The line reference is approximately correct but not exact. Since the spec is a living document, line references are fragile. The section reference ("after Coexistence with Unified Audit Gating D-03/D-04 paragraph") is the reliable anchor.

**MISMATCH-2**: Task 001 references "line 99, Key design property paragraph." The actual spec has the "Key design property" text at line 101. Same fragility concern -- section-relative positioning is the reliable anchor.

**Severity**: LOW. Both tasks also include section-relative descriptions that are accurate. Line numbers are supplementary.

---

## Wave Ordering

### Current Structure

```
Wave 1 (6 edit tasks) -> Verify -> Wave 2 (3 add-section tasks) -> Verify -> Wave 3 (6 edit tasks) -> Verify -> Wave 4 (4 verify/test tasks)
```

### Assessment

The wave ordering is well-designed. The principle is sound:
1. Wave 1 establishes terminology and field definitions in existing sections
2. Wave 2 creates new sections that reference Wave 1 terms
3. Wave 3 updates downstream sections (file lists, phases, assumptions) that reference Waves 1-2
4. Wave 4 performs cross-cutting verification

### Optimization Opportunities

**OPT-1: Tasks 016 and 017 could move to Wave 1.** They have zero dependencies and are simple additive edits (table rows). Moving them to Wave 1 would reduce Wave 3 from 6 tasks to 4 tasks. The verification in Task 018 would need to be split accordingly. However, the current placement is defensible for readability (all Section 13/14 edits grouped together).

**OPT-2: Wave 4 tasks 019-022 are strictly sequential.** Each depends on the previous. This is correct for verification (each check builds on prior confirmation). However, Task 019 (unchanged sections verification) and Task 020 (interaction effects verification) could potentially run in parallel since they check different things. Task 021 (backward compat) genuinely depends on both.

**OPT-3: Wave 2 could partially overlap with Wave 3.** Task 010 (Section 16.5) depends only on Task 003, so it could start before Task 008 completes. Task 012 depends on Task 008 but not on Tasks 009 or 010. In theory, 010 and 012 could run in parallel if 008 is complete. The current wave boundaries are conservative but safe.

**Recommendation**: The current ordering is acceptable. The conservative approach reduces risk of cross-contamination between edits. The total overhead of the extra synchronization points is minimal for a spec-editing task (not code execution).

---

## Risk Assessment

### High-Risk Edits

1. **Task 003 (Section 8 coexistence subsection)**: This is the longest single edit and introduces the enforcement_tier vs rollout_mode distinction that all subsequent sections reference. If the terminology here is wrong, it propagates to 9.5, 16.5, and all verification tasks. **Properly sequenced in Wave 1** with verification in Task 007.

2. **Task 008 (Section 9.5)**: The rollout mode behavior matrix is the single most referenced artifact. If the matrix columns are wrong (e.g., "Reimbursement on pass?" for shadow mode), the economic model is incorrect. **Properly sequenced in Wave 2** with verification in Task 011.

3. **Task 015 (task split 6a/6b + task 9)**: Modifies the implementation sequence which is the primary implementation guide. If the split is wrong, implementers work on wrong scope. **Properly sequenced in Wave 3** after parallelism note (Task 014) establishes context.

### Interaction Effects Coverage

| Interaction Effect | Covered By Task(s) | Status |
|---|---|---|
| 1. Enforcement tier x rollout mode | 003, 008 | COVERED |
| 2. Dual execution context | 001, 003, 008 | COVERED |
| 3. Anti-instinct x wiring gate ordering | No edit task | GAP (see GAP-2) |
| 4. Anti-instinct x spec-fidelity ordering | Implicit in Section 8 ALL_GATES (pre-existing) | COVERED (pre-existing) |
| 5. Reimbursement x pre-allocation | 010 | COVERED |
| 6. DeferredRemediationLog x retry_limit=0 | 004, 010 | COVERED |
| 7. Structural audit budget impact | No edit task | GAP (see GAP-3) |
| 8. Per-gate-type reimbursement rate | 017 (A-013) | COVERED |
| 9. Section 8 <-> Section 14 pairing | 003, 017 | COVERED |
| 10. Section 12 <-> Section 13 parallelism | 012, 014 | COVERED |

---

## Summary

| Metric | Count |
|--------|-------|
| **Merged plan edits mapped** | 16/16 primary edits covered |
| **Gaps found** | 3 (1 MEDIUM, 2 LOW) |
| **Orphan tasks** | 0 |
| **Missing dependencies** | 2 (both LOW -- covered by wave structure) |
| **Circular dependencies** | 0 |
| **Parallelization opportunities** | 3 (minor optimizations, current structure acceptable) |
| **Vague acceptance criteria** | 3 (Tasks 022, 018, 007) |
| **Section reference mismatches** | 2 (line numbers, not section names -- LOW) |
| **Interaction effects with no edit task** | 2 (effects 3 and 7 -- both LOW) |
| **Total issues** | 10 |

### Confidence Level: **HIGH**

The tasklist faithfully represents the merged plan. All 16 primary edits from the merged plan have corresponding tasks. The 3 gaps are minor: backward compatibility notes that are either implicit in other tasks or are Phase 2 concerns. The dependency graph is correct with two minor missing explicit dependencies that are covered by wave structure. The wave ordering is sound and conservative. Acceptance criteria are mostly specific and verifiable with 3 instances of subjective language.

### Recommended Fixes (prioritized)

1. **(MEDIUM)** Add a Task 017.5 or expand Task 017 to include a "Migration/Backward Compatibility" subsection in Section 14 (or as a new Section 14.5) that explicitly states Notes 4, 5, 8, and 9 from the merged plan's backward compatibility section.
2. **(LOW)** Tighten Task 022 criterion (5) to include objective measures of coherence (no verbatim repetition, consistent terminology).
3. **(LOW)** Add a one-line note about wiring gate ordering (interaction effect 3) to Task 008's content specification.
4. **(LOW)** Add explicit dependency of Task 010 on Task 008 to ensure Section 16.5 cross-refs to 9.5 are valid at write time.
