# Refactoring Plan: v3.7 Release Specification Merge

## Overview

- **Base variant**: Variant B ("Assembled", 1608 lines)
- **Incorporating from**: Variant A ("Droid", 719 lines)
- **Planned changes**: 9
- **Changes NOT being made**: 3
- **Overall risk**: Low (all changes are additive or correctional)

---

## Planned Changes

### Change #1: Add Cross-Cutting Concerns Section

| Field | Value |
|-------|-------|
| Source | Variant A, Section 6 (lines 390-439) |
| Target | After Section 5 (Cross-Domain Dependencies), before Section 6 (Data Model Changes) — renumber subsequent sections |
| Rationale | A's Section 6 consolidates shared file modification table, post-phase hook ordering, Haiku subprocess conventions, and token display helper. B identifies the cross-domain conflicts (Section 5) but provides no resolution ordering. Debate evidence: C-009 won by A with 95% confidence, B conceded. |
| Integration approach | INSERT — new section between existing sections 5 and 6 |
| Risk level | Low — additive, no existing content modified |

### Change #2: Resolve SummaryWorker Module Location (X-001)

| Field | Value |
|-------|-------|
| Source | Variant A, Section 4.5 |
| Target | B's Section 3.2 (Solution Architecture, TUI v2) and Section 7.2 (File Inventory) |
| Rationale | B places SummaryWorker in executor.py. A places it in summarizer.py. B conceded in Round 2 rebuttal: "summarizer.py is the cleaner home." Module cohesion principle. |
| Integration approach | REPLACE — change "SummaryWorker class (in executor.py)" to "SummaryWorker class (in summarizer.py)" throughout |
| Risk level | Low — text change, no structural impact |

### Change #3: Add threading.Lock Mandate for SummaryWorker

| Field | Value |
|-------|-------|
| Source | Variant A, Section 4.5 critical invariants |
| Target | B's Section 3.2 (TUI v2 new modules) after SummaryWorker description |
| Rationale | A mandates "SummaryWorker._summaries dict MUST be guarded by threading.Lock." B lists this as open question TUI-Q3 and risk TUI-2. Debate: X-004 won by A with 90% confidence, B conceded. |
| Integration approach | APPEND — add critical invariants block after SummaryWorker description; move TUI-Q3 to resolved |
| Risk level | Low — additive |

### Change #4: Resolve Open Questions Q4, Q6, Q13

| Field | Value |
|-------|-------|
| Source | Variant A, Section 11.1 items 4, 6, 13 (marked RESOLVED) |
| Target | B's Section 13.2 (TUI Open Questions) — TUI-Q3 and TUI-Q5 |
| Rationale | A resolves: SummaryWorker in summarizer.py (Q4), threading.Lock mandated (Q6), output_bytes/files_changed already exist on PhaseResult (Q13). Debate: C-006 won by A with 85% confidence. |
| Integration approach | MODIFY — mark TUI-Q3 as RESOLVED (threading.Lock), add note to TUI-Q5 (resolved: tui.py), remove Q13 equivalent where applicable |
| Risk level | Low |

### Change #5: Add Test Tasks T02.05 and T03.06 to Checkpoint Implementation Plan

| Field | Value |
|-------|-------|
| Source | Variant A, Section 3.2 Wave 2 (T02.05) and Wave 3 (T03.06) |
| Target | B's Section 4.1 Phase 2 and Phase 3 task lists |
| Rationale | A adds dedicated test-writing tasks. B identifies the gap (CE-Q1) but doesn't add tasks. Debate: C-007/C-011 won by A with 80% confidence. This resolves CE-Q1. |
| Integration approach | INSERT — add T02.05 after T02.04 and T03.06 after T03.05 with full MDTM detail |
| Risk level | Low — additive |

### Change #6: Add LOC Estimates to Overview

| Field | Value |
|-------|-------|
| Source | Variant A, Section 1 overview table (Checkpoint ~580, TUI v2 ~800+, Naming ~100) |
| Target | B's Section 1 (Release Overview) scope boundaries table |
| Rationale | A provides explicit LOC estimates per feature area. B quantifies checkpoint (580) but not TUI or naming. Debate: C-003 won by A with 70% confidence. |
| Integration approach | APPEND — add LOC column to B's scope table |
| Risk level | Low |

### Change #7: Address INV-002 (Cross-Wave Rollback Gap)

| Field | Value |
|-------|-------|
| Source | Invariant probe finding INV-002 (HIGH severity, UNADDRESSED) |
| Target | B's Section 4.1 Phase 2, after T02.04 |
| Rationale | Neither variant addresses what happens when Wave 2 is rolled back without re-applying Wave 1. Add a rollback note: "If Wave 2 is reverted, manually re-apply T01.02 _warn_missing_checkpoints() to maintain checkpoint awareness." |
| Integration approach | APPEND — add rollback note to Phase 2 checkpoint |
| Risk level | Low |

### Change #8: Address INV-003 (verify_checkpoints Timeout)

| Field | Value |
|-------|-------|
| Source | Invariant probe finding INV-003 (HIGH severity, UNADDRESSED) |
| Target | Cross-Cutting Concerns section (new Section 6, from Change #1), post-phase hook ordering subsection |
| Rationale | verify_checkpoints has no timeout bound. Add: "verify_checkpoints SHOULD complete within 5 seconds (disk I/O only). If it exceeds 5s, log a warning but do not block summary_worker.submit." |
| Integration approach | APPEND — add timeout guidance to hook ordering subsection |
| Risk level | Low |

### Change #9: Harmonize Rollout Timeline

| Field | Value |
|-------|-------|
| Source | Both variants (C-004, C-012, X-002 — unresolved tie points) |
| Target | B's Section 8.1 (Combined Timeline) |
| Rationale | A starts naming Day 0, B starts Day 1-3. Both are reasonable. Merge: Day 1 for both naming and CP W1 (both are small, can run in parallel). |
| Integration approach | MODIFY — adjust timeline to start naming and CP W1 on Day 1 simultaneously |
| Risk level | Low |

---

## Changes NOT Being Made

| # | Diff Point | Non-Base Approach | Why Base Approach is Superior |
|---|------------|-------------------|-------------------------------|
| 1 | S-001 (document length) | A is more concise at 719 lines | B's length is driven by per-task detail and appendices, both of which won debate points. Conciseness is a trade-off, not a universal improvement. |
| 2 | C-013 (risk register format) | A combines risks + open questions in one section | B's separated risk register with domain grouping is more actionable and won the debate point. |
| 3 | A's Section 12 (Out of Scope) | A has a dedicated Out of Scope section with numbered items | B's "Deferred" list in Section 1 covers the same content. The merged document preserves B's format. However, the items from A's Section 12 will be verified present in B's deferred list. |

---

## Risk Summary

| Change # | Description | Risk | Impact if Failed | Rollback |
|----------|-------------|------|-----------------|----------|
| 1 | Cross-cutting concerns section | Low | Missing integration guidance; implementers consult A directly | Remove section |
| 2 | SummaryWorker location fix | Low | Incorrect module reference; easily corrected | Revert text changes |
| 3 | threading.Lock mandate | Low | Missing concurrency guidance | Remove invariant block |
| 4 | Resolve open questions | Low | False uncertainty persists | Re-open questions |
| 5 | Add test tasks | Low | Missing test coverage in plan | Remove added tasks |
| 6 | LOC estimates | Low | Missing planning data | Remove column |
| 7 | INV-002 rollback note | Low | Rollback gap remains | Remove note |
| 8 | INV-003 timeout guidance | Low | Potential timing issue remains | Remove guidance |
| 9 | Timeline harmonization | Low | Minor scheduling inconsistency | Revert to B's timeline |

---

## Review Status

- **Approval**: Auto-approved (non-interactive mode)
- **Timestamp**: 2026-04-02T12:30:00Z
