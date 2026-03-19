# Split Proposal — Unified Audit Gating Spec Refactor Plan

**Date**: 2026-03-18
**Input artifact**: `spec-refactor-plan-merged.md`
**Analysis type**: Release split discovery

---

## Recommendation: DO NOT SPLIT

**Confidence**: 0.85

---

## Analysis Summary

### Artifact Nature

The input is a **document refactoring plan** — not a code release or implementation spec. Its own header declares:

> "Plan type: Document refactoring plan only — no files modified here"
> "Status: PLAN ONLY — do not edit spec until this plan is approved"

All 28 section changes target a single document (`unified-audit-gating-release-spec.md`). The "phases" described within the spec (Phase 0-4) refer to *future implementation work*, not work items in this plan.

### Two-Stream Architecture Identified

The plan contains two analytically distinct streams:

1. **Plan B (Foundation)**: Branch decisions, scope constraints (branch b deferral), canonical terms (6 new), locked decisions, transition annotations, timeout/retry semantics, promotion criteria, KPI instrumentation, owner responsibilities, decision deadlines — 11 unique changes
2. **Plan A (Behavioral Extensions)**: Silent Success Detection (P05), Smoke Test Gate G-012 (P04), Spec Fidelity D-03/D-04 (P02), failure class sub-types, GateResult extension blocks, new SS13 section, Phase 0 prerequisites — 6 unique changes

Plus **8 compatible merges** and **3 synthesized conflict resolutions** that combine both streams.

### Why Splitting Is NOT Recommended

#### 1. Shared sections prevent clean separation

8 sections contain `A+B-merged` changes: SS1.1, SS2.3, SS5.2, SS6.1, SS10.3, SS11, SS12.4, and Top 5 Immediate Actions. 3 sections contain `synthesized` resolutions: SS10.1, SS10.2, SS12.3. Splitting these would require:
- Applying partial changes in R1 (Plan B portions only)
- Completing them in R2 (Plan A additions)
- Maintaining temporary inconsistency between editing sessions

This is fragile and error-prone for no meaningful benefit.

#### 2. Dependency order is designed for single-pass editing

The plan provides a careful dependency order (Phase 0 → Phase 1 → Any Time) for editing. Splitting this into two passes means re-opening already-edited sections to add Plan A content — violating the dependency ordering and creating opportunities for inconsistency.

#### 3. Verification checklist requires both streams

The 29 verification invariants (lines 1236-1279) include cross-plan consistency checks:
- "SS12.3 has 9 blockers (original 4 + 2 Plan B + 3 Plan A)"
- "SS12.4 has 9 required decisions (original 5 + 1 Plan B + 3 Plan A)"
- "No contradictions between Plan A behavioral gate additions and Plan B branch (b) scope constraints"

These can only be verified when both streams are applied. An intermediate state (Plan B only) would fail these checks by design.

#### 4. No real-world validation opportunity between passes

Splitting a document refactoring plan only enables: "Review the partially-edited spec." This is achievable without splitting — reviewers can focus on Plan B sections first in a single pass.

#### 5. Synthesized resolutions are indivisible

The 3 synthesized conflict resolutions (SS10.1, SS10.2, SS12.3) were produced by adversarial debate merging Plan A and Plan B positions. They are inherently cross-stream — applying only one stream would leave the synthesized text referencing content that doesn't exist yet.

#### 6. Coordination overhead exceeds benefit

Splitting a single-document editing plan into two releases creates:
- Two review cycles instead of one
- Tracking which merged sections need a second pass
- Risk of forgetting to apply the second pass
- Temporary verification failures that must be manually acknowledged

### Counterargument: Implementation Work IS Separable

The spec does describe separable implementation work — P0-B and P0-C are explicitly "no dependency" items. But this separability exists *within the implementation phases*, not in the spec document itself. The spec should describe the complete scope; the implementation schedule already handles sequencing via the Phase 0-4 structure.

## Alternative Strategy: Prioritized Review

Instead of splitting the spec editing, use the existing dependency order for **prioritized review**:

1. **Priority 1 — Phase 0 blocking changes**: SS2.1 (locked decisions), SS4.1 (deferral annotations), SS1.1 (scope), SS9.3 (decision deadlines), SS12.3 (blockers), SS12.4 (decisions), Open Decisions table
2. **Priority 2 — Phase 1 structural changes**: SS3.1 (terms), SS4.4 (timeout/retry), SS5.1-5.2 (failure classes/rules), SS6.1 (GateResult), SS7.2 (promotion), SS8.3-8.5 (KPIs)
3. **Priority 3 — Phase 1 continued**: SS9.2 (owners), SS10.1-10.3 (phase plan/files/acceptance), SS11 (checklist), SS13 (behavioral gates), Top 5 Actions

This enables early feedback on foundational decisions without the overhead of a formal release split.

## Risks of Keeping Intact

| Risk | Severity | Mitigation |
|------|----------|------------|
| Large review scope (28 changes) | Medium | Use prioritized review order; reviewers focus on Phase 0 first |
| Plan A additions may change during review of Plan B sections | Low | Plan A and Plan B are additive, not conflicting (verified by 3 synthesized resolutions) |
| Delayed feedback on behavioral gate extensions | Low | P0-B and P0-C implementation can begin before spec editing completes (they have no spec dependency) |

## Next Steps (if no-split confirmed)

1. Apply all 28 changes to `unified-audit-gating-release-spec.md` in the documented dependency order
2. Run the 29-point verification checklist
3. Review using the prioritized review strategy above
4. Begin P0-B and P0-C implementation immediately (no spec dependency)
