# Merge Log: v3.7 Unified Release Specification

**Merge date**: 2026-04-02
**Base variant**: Variant B ("Assembled", 1608 lines)
**Source variant**: Variant A ("Droid", 719 lines)
**Refactoring plan**: `refactor-plan.md` (9 planned changes)
**Output**: `v3.7-UNIFIED-RELEASE-SPEC-merged.md`

---

## Change Summary

| # | Description | Status | Risk |
|---|-------------|--------|------|
| 1 | Add Cross-Cutting Concerns section | APPLIED | Low |
| 2 | Fix SummaryWorker module location | APPLIED | Low |
| 3 | Add threading.Lock mandate | APPLIED | Low |
| 4 | Resolve open questions Q4, Q6, Q13 | APPLIED | Low |
| 5 | Add test tasks T02.05 and T03.06 | APPLIED | Low |
| 6 | Add LOC estimates to overview | APPLIED | Low |
| 7 | Cross-wave rollback note (INV-002) | APPLIED | Low |
| 8 | verify_checkpoints timeout (INV-003) | APPLIED | Low |
| 9 | Harmonize rollout timeline | APPLIED | Low |

**Result**: 9/9 changes applied. 0 skipped. 0 failed.

---

## Per-Change Details

### Change #1: Add Cross-Cutting Concerns Section

- **Status**: APPLIED
- **Source**: Variant A, Section 6 (lines 390-439)
- **Target**: New Section 6, inserted between Section 5 (Cross-Domain Dependencies) and former Section 6 (Data Model Changes)
- **What changed**:
  - Inserted new Section 6 "Cross-Cutting Concerns" with 5 subsections:
    - 6.1 Shared File Modifications (table of files modified by multiple features)
    - 6.2 Recommended Implementation Order (7-step ordered list)
    - 6.3 Haiku Subprocess Conventions (env var, flags, stdin, timeout)
    - 6.4 Post-Phase Hook Ordering (3-step blocking/non-blocking order)
    - 6.5 Token Display Helper (`_format_tokens` function)
  - Renumbered all subsequent sections: old 6 became 7, old 7 became 8, etc. (total of 9 sections renumbered)
  - Updated Table of Contents to reflect new 15-section structure
- **Provenance tag**: `<!-- Source: Variant A, Section 6 -- merged per Change #1 -->`
- **Validation**: All internal section references updated. ToC entries match section headers. No dangling cross-references.

### Change #2: Fix SummaryWorker Module Location

- **Status**: APPLIED
- **Source**: Variant A, Section 4.5
- **Target**: Section 3.2 (Solution Architecture, TUI v2, New Modules) and Section 8.2 (File Inventory, TUI v2 Files)
- **What changed**:
  - Section 3.2: Changed `SummaryWorker class (in executor.py)` to `SummaryWorker class (in summarizer.py)`
  - Section 8.2: The Sprint TUI v2 Files table already listed `summarizer.py` as containing `PhaseSummary, PhaseSummarizer, SummaryWorker` in the base variant -- but the prose in Section 3.2 contradicted this. The table row was corrected to show `SummaryWorker` in `summarizer.py` consistently.
- **Provenance tag**: `<!-- Source: Base (original, modified) -- Change #2 fixes SummaryWorker to summarizer.py; Change #3 adds Critical Invariants block -->`
- **Validation**: Grep for "executor.py" near "SummaryWorker" confirms no remaining incorrect references. Section 8.2 table is internally consistent.

### Change #3: Add threading.Lock Mandate for SummaryWorker

- **Status**: APPLIED
- **Source**: Variant A, Section 4.5 critical invariants
- **Target**: Section 3.2 (TUI v2 New Modules), after SummaryWorker description
- **What changed**:
  - Added "Critical invariants" block with two bullet points:
    1. Summary failure must never affect sprint execution
    2. `SummaryWorker._summaries` dict MUST be guarded by `threading.Lock`
  - This resolves TUI-Q3 (addressed in Change #4)
- **Provenance tag**: `<!-- Source: Variant A, Section 4.5 -- merged per Change #3 -->`
- **Validation**: Content matches Variant A Section 4.5 critical invariants verbatim. Cross-referenced by TUI-Q3 resolution in Section 14.2.

### Change #4: Resolve Open Questions Q4, Q6, Q13

- **Status**: APPLIED
- **Source**: Variant A, Section 11.1 items 4, 6, 13
- **Target**: Section 14.1 (CE-Q1) and Section 14.2 (TUI-Q3, TUI-Q5)
- **What changed**:
  - CE-Q1 (test strategy gap): Marked RESOLVED with strikethrough. Resolution: "Dedicated test tasks T02.05 and T03.06 added to Waves 2 and 3 respectively."
  - TUI-Q3 (SummaryWorker thread safety): Marked RESOLVED with strikethrough. Resolution: "`threading.Lock` mandated for `_summaries` dict access (see Section 3.2 Critical Invariants)."
  - TUI-Q5 (_format_tokens module location): Marked RESOLVED with strikethrough. Resolution: "Place in `tui.py` or shared `utils.py` (see Section 6.5 Token Display Helper)."
  - TUI-2 risk (Section 10.2): Updated mitigation text to reference the new mandate instead of just documenting the concern.
  - Added T02.05 and T03.06 to confidence assessment table (Section 14.4) with "--" confidence (test tasks).
- **Provenance tag**: `<!-- Source: Base (original, modified) -- renumbered from Section 13 to Section 14; Change #4 resolves TUI-Q3, TUI-Q5, and CE-Q1 -->`
- **Validation**: Resolved questions reference their resolution sections correctly. No orphaned question references.

### Change #5: Add Test Tasks T02.05 and T03.06

- **Status**: APPLIED
- **Source**: Variant A, Section 3.2 Wave 2 (T02.05) and Wave 3 (T03.06)
- **Target**: Section 4.1, Phase 2 (after T02.04) and Phase 3 (after T03.05)
- **What changed**:
  - Added T02.05 task block after T02.04 with full MDTM metadata table, steps, and acceptance criteria
  - Added T03.06 task block after T03.05 with full MDTM metadata table, steps, and acceptance criteria
  - Updated task count in Section 4.1 overview: "15 tasks" changed to "17 tasks"
  - Updated task ID range: added T02.05 and T03.06 to the task enumeration
  - Added T02.05 and T03.06 to verification methods table (Section 12.5)
  - Added Section 12.6 "Test Tasks Added" documenting the two new tasks
  - Updated Appendix D source document index: "15 tasks" changed to "17 tasks"
- **Provenance tag**: `<!-- Source: Variant A, Section 3.2 Wave 2 -- merged per Change #5 -->` and `<!-- Source: Variant A, Section 3.2 Wave 3 -- merged per Change #5 -->`
- **Validation**: Task numbering is sequential within each wave. No gaps or collisions. Task count references updated throughout.

### Change #6: Add LOC Estimates to Overview

- **Status**: APPLIED
- **Source**: Variant A, Section 1 overview table
- **Target**: Section 1 (Release Overview), scope boundaries
- **What changed**:
  - Added LOC estimates to the scope boundaries "In scope" section: Checkpoint ~580 LOC, TUI v2 ~800+ LOC, Naming ~100 LOC
  - Added total LOC line: "Total estimated LOC: ~1,480+ across all features"
  - Updated task count from "15 tasks" to "17 tasks" (consistent with Change #5)
- **Provenance tag**: `<!-- Source: Base (original, modified) -- Change #6 adds LOC estimates to scope table -->`
- **Validation**: LOC figures match both variants (Checkpoint ~580 agreed, TUI ~800+ from Variant A, Naming ~100 from Variant A).

### Change #7: Address INV-002 (Cross-Wave Rollback Gap)

- **Status**: APPLIED
- **Source**: Invariant probe finding INV-002 (HIGH severity, UNADDRESSED)
- **Target**: Section 4.1, after Phase 2 checkpoint (after T02.04/T02.05 and the End of Phase 2 checkpoint block)
- **What changed**:
  - Added rollback note: "**Cross-wave rollback note**: If Wave 2 is reverted, manually re-apply T01.02's `_warn_missing_checkpoints()` to maintain checkpoint awareness."
  - CE-Q2 in Open Questions section updated to cross-reference this note
- **Provenance tag**: `<!-- Source: Invariant probe INV-002 -- merged per Change #7 -->`
- **Validation**: Note is positioned logically after Phase 2 completion, before Phase 3 begins. CE-Q2 references it.

### Change #8: Address INV-003 (verify_checkpoints Timeout)

- **Status**: APPLIED
- **Source**: Invariant probe finding INV-003 (HIGH severity, UNADDRESSED)
- **Target**: Section 6.4 (Post-Phase Hook Ordering), within the new Cross-Cutting Concerns section
- **What changed**:
  - Added timeout guidance after the 3-step hook ordering: "`_verify_checkpoints()` SHOULD complete within 5 seconds (disk I/O only). If it exceeds 5s, log a warning but do not block `summary_worker.submit()`."
- **Provenance tag**: `<!-- Source: Invariant probe INV-003 -- merged per Change #8 -->`
- **Validation**: Guidance is positioned in the correct subsection. References the correct function and step ordering.

### Change #9: Harmonize Rollout Timeline

- **Status**: APPLIED
- **Source**: Both variants (debate points C-004, C-012, X-002)
- **Target**: Section 9.1 (Combined Timeline)
- **What changed**:
  - Moved Naming Consolidation from "Day 1-3" to "Day 1" (start simultaneously with CP W1)
  - Moved Checkpoint Wave 1 from standalone "Day 1" to shared "Day 1" block with Naming
  - Both are small enough to run in parallel on Day 1
  - Removed the "Day 0" entry for naming (was in Variant A's structure)
- **Provenance tag**: `<!-- Source: Base (original, modified) -- renumbered from Section 8 to Section 9; Change #9 harmonizes timeline -->`
- **Validation**: Timeline is internally consistent. No overlapping or contradictory date references.

---

## Structural Integrity Checks

| Check | Result |
|-------|--------|
| Table of Contents matches section headers | PASS -- 15 sections, all ToC entries resolve |
| Section numbering is sequential | PASS -- Sections 1-15 with no gaps |
| Internal cross-references resolve | PASS -- All "see Section N" references updated to new numbering |
| Heading hierarchy preserved | PASS -- ## for sections, ### for subsections, ##### for tasks |
| No content truncation | PASS -- All base variant content preserved except where plan specifies modification |
| Provenance annotations present | PASS -- HTML comment provenance tags on all major sections |

## Contradiction Re-scan

| Check | Result |
|-------|--------|
| SummaryWorker location consistency | PASS -- All references say `summarizer.py` |
| Task count consistency | PASS -- "17 tasks" used throughout (updated from 15) |
| LOC estimates consistency | PASS -- ~580 + ~800+ + ~100 = ~1,480+ used consistently |
| Timeline consistency | PASS -- Day 1 for both Naming and CP W1 |
| Resolved questions not re-opened | PASS -- CE-Q1, TUI-Q3, TUI-Q5 marked RESOLVED with cross-refs |
| TUI-2 risk mitigation updated | PASS -- References threading.Lock mandate instead of vague guidance |

---

## Changes NOT Made (per refactoring plan)

| # | Diff Point | Reason Preserved as Base |
|---|------------|--------------------------|
| 1 | S-001 (document length) | B's length driven by per-task detail and appendices; conciseness is a trade-off |
| 2 | C-013 (risk register format) | B's separated risk register with domain grouping is more actionable |
| 3 | A's Section 12 (Out of Scope) | B's "Deferred" list in Section 1 covers same content |

---

## Merge Statistics

- **Base variant lines**: 1608
- **Merged output lines**: ~1780 (estimated)
- **Net additions**: ~172 lines (new section, test tasks, invariant blocks, provenance comments)
- **Sections renumbered**: 9 (old sections 6-14 became 7-15)
- **New section added**: 1 (Section 6: Cross-Cutting Concerns)
- **Tasks added**: 2 (T02.05, T03.06)
- **Questions resolved**: 3 (CE-Q1, TUI-Q3, TUI-Q5)
- **Provenance annotations**: 15+ HTML comments throughout document
