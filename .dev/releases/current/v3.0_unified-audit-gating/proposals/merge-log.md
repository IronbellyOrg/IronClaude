# Merge Log — Spec Refactoring Plans A + B

**Date**: 2026-03-17
**Merge executor**: Claude Opus 4.6 (1M context)
**Plan A**: `spec-refactor-plan.md` (P05/P04/P02 behavioral gate extensions)
**Plan B**: `spec-refactoring-plan.md` (branch decision C1-C7, adversarial delta review, delta analysis)
**Output**: `spec-refactor-plan-merged.md`

---

## Per-Change Execution Log

| # | Section | Source | Classification | Action Taken | Validation |
|---|---------|--------|----------------|--------------|------------|
| 1 | SS1.1 Scope | A+B-merged | OVERLAP-COMPATIBLE | Plan A items 4-6 appended first, then Plan B branch (b) scope amendment appended after | OK -- additions are independent; Plan A adds behavioral gate scope, Plan B constrains task-scope |
| 2 | SS1.3 Out-of-scope | UNIQUE-A | No conflict | Included verbatim from Plan A | OK |
| 3 | SS2.1 Locked decisions | UNIQUE-B (R2) | No conflict | Included verbatim from Plan B as locked decision #6 | OK |
| 4 | SS2.2 Non-goals | UNIQUE-A | No conflict | Included verbatim from Plan A | OK |
| 5 | SS2.3 Contradictions | A+B-merged | OVERLAP-COMPATIBLE | 2 rows from Plan A (C-1, C-2) + 2 rows from Plan B (MF-1, M1 recalibration) appended | OK -- all 4 rows address different contradictions |
| 6 | SS3.1 Canonical terms | UNIQUE-B (R4) | No conflict | Included verbatim from Plan B (6 new terms) | OK |
| 7 | SS4.1 Legal transitions | UNIQUE-B (R5) | No conflict | Included verbatim from Plan B (deferral annotation) | OK |
| 8 | SS4.4 Timeout/retry | UNIQUE-B (R6) | No conflict | Included verbatim from Plan B (major rewrite) | OK |
| 9 | SS5.1 Failure classes | UNIQUE-A | No conflict | Included verbatim from Plan A (policy sub-types) | OK |
| 10 | SS5.2 Pass/fail rules | A+B-merged | OVERLAP-COMPATIBLE | Plan B modifies item 4 (freshness language), Plan A adds item 5 (C-1 rule) | OK -- Plan B touches item 4, Plan A adds item 5; no overlap |
| 11 | SS6.1 GateResult | A+B-merged | OVERLAP-COMPATIBLE | Plan A behavioral gate blocks appended first, then Plan B implementation notes appended after | OK -- Plan A adds schema blocks, Plan B adds naming/hashing notes |
| 12 | SS7.2 Promotion criteria | UNIQUE-B (R9) | No conflict | Included verbatim from Plan B (M1/M8 recalibration) | OK |
| 13 | SS8.3 Warning/fail bands | UNIQUE-A | No conflict | Included verbatim from Plan A (M13, M14) | OK |
| 14 | SS8.5 KPI instrumentation | UNIQUE-B (R10) | No conflict | Included verbatim from Plan B (new subsection) | OK |
| 15 | SS9.2 Owner responsibilities | UNIQUE-B (R11) | No conflict | Included verbatim from Plan B (tasklist owner) | OK |
| 16 | SS9.3 Decision deadlines | UNIQUE-B (R12) | No conflict | Included verbatim from Plan B (locked decision record) | OK |
| 17 | SS10.1 Phase plan | synthesized | OVERLAP-CONFLICT | Plan B phase structure used as base; Plan A P0-A/P0-B/P0-C merged into Phase 0; Plan A G-012/SilentSuccessDetector/S2 merged into Phase 2 | OK -- verified phase assignments are internally consistent |
| 18 | SS10.2 File-level change map | synthesized | OVERLAP-CONFLICT | Plan B structural rewrite (no line citations) used as base; Plan A P0 files added to Phase 0 section; Plan A Phase 2 files added to Phase 2 section | OK -- verified no line citations remain; all files assigned to correct phase |
| 19 | SS10.3 Acceptance criteria | A+B-merged | OVERLAP-COMPATIBLE | Plan A adds Phase 0 and Phase 2 criteria; Plan B extends Phase 1 criterion; both included | OK -- criteria target different phases |
| 20 | SS11 Checklist | A+B-merged | OVERLAP-COMPATIBLE | Plan B updates row 9 evidence; Plan A updates row 10 to PARTIAL-GO and adds rows 11-12 | OK -- different rows modified |
| 21 | SS12.3 Blocker list | synthesized | OVERLAP-CONFLICT | Original 4 retained with Plan B note on blocker 2; Plan B adds blockers 5-6; Plan A adds blockers 7-9; renumbered sequentially | OK -- 9 total blockers, all non-overlapping |
| 22 | SS12.4 Required decisions | A+B-merged | OVERLAP-COMPATIBLE | Plan B adds decision 6 (C3); Plan A adds decisions 7-9 (S2, mock-llm, D-03/D-04) | OK -- all additions are independent |
| 23 | New SS13 | UNIQUE-A | No conflict | Included verbatim from Plan A (complete section 13.1-13.4) | OK -- blocker references updated to merged numbering (blocker 7, 9) |
| 24 | Top 5 Immediate | A+B-merged | OVERLAP-COMPATIBLE | Plan A prepends 0a/0b/0c; Plan B appends item 6 (C3 checkpoint) | OK -- item 5 updated to reference blockers 5-9 and decisions 6-9 |
| 25 | Top 5 Deferred | UNIQUE-B (R20) | No conflict | Included verbatim from Plan B (item 6: execute_phase_tasks) | OK |
| 26 | Open Decisions | UNIQUE-B (R21) | No conflict | Included verbatim from Plan B (6 new rows) | OK |
| 27 | Implementation Order Summary | UNIQUE-A (extended) | No conflict | Plan A visual tree extended to include Plan B Phase 0-4 items | OK |
| 28 | Contradiction Check | UNIQUE-A | No conflict | Included verbatim from Plan A (LD-1 through LD-5 check table + C-1/C-2 resolutions) | OK |
| 29 | What This Plan Does NOT Change | UNIQUE-B (updated) | No conflict | Plan B table included with correction note for sections that Plan A does change (SS1.3, SS2.2, SS5.1, SS8.3) | OK |
| 30 | Dependency Order | UNIQUE-B (extended) | No conflict | Plan B dependency order extended to include Plan A change references | OK |
| 31 | Verification Checklist | UNIQUE-B (extended) | No conflict | Plan B 11-item checklist extended with 16 Plan A invariants + 5 cross-plan consistency checks | OK -- blocker/decision counts updated (9/9/11) |
| 32 | Files Not Changed | UNIQUE-A | No conflict | Included verbatim from Plan A | OK |

---

## Conflict Resolution Summary

### Conflict 1: SS10.1 Phase Plan
- **Plan A**: Extended existing phases with P0-A/P0-B/P0-C prerequisites and Phase 2 behavioral gate integration
- **Plan B**: Replaced entire phase plan with detailed 5-phase plan (branch decisions, adversarial review)
- **Resolution**: Plan B structure used as base; Plan A items merged at appropriate phase boundaries (P0-A/P0-B/P0-C into Phase 0; G-012/SilentSuccessDetector/S2 into Phase 2)
- **Rationale**: Plan B phases are derived from the primary branch decision C1-C7 inputs. Plan A phases address a complementary work stream that fits naturally within Plan B's structure.

### Conflict 2: SS10.2 File-Level Change Map
- **Plan A**: Added P0 and Phase 2 subsections to existing line-citation format
- **Plan B**: Replaced entire section with behavioral descriptions (no line citations)
- **Resolution**: Plan B structural rewrite used as base; Plan A files added as labeled subsections within Plan B's phase structure
- **Rationale**: Adversarial review consensus requires removing line citations. Plan A files are organized by the same phase structure Plan B uses.

### Conflict 3: SS12.3 Blocker List
- **Plan A**: Added blockers 5-7 (S2 calibration, mock-llm, P0-A scheduling)
- **Plan B**: Added blockers 5-6 (branch(b) record, reimbursement_rate)
- **Resolution**: Both sets included, renumbered sequentially (Plan B 5-6, Plan A 7-9)
- **Rationale**: All blockers are legitimate, actionable, and non-overlapping. Plan B blockers ordered first because they are Phase 0 blocking items.

---

## Items Dropped

None. All items from both plans are present in the merged output.

---

## Cross-Reference Integrity

- SS12.3 blocker references in SS13.3 updated from "blocker 7" (Plan A numbering) to "blocker 9" (merged numbering)
- SS12.4 decision references in Top 5 Immediate updated from "6-8" (Plan A numbering) to "6-9" (merged numbering)
- SS12.3 blocker count in Verification Checklist updated from "6" (Plan B) to "9" (merged)
- SS12.4 decision count in Verification Checklist updated from "6" (Plan B) to "9" (merged)
- Open Decisions row count in Verification Checklist updated from "9" (Plan B) to "11" (merged: 5 original + 6 new)
- "What This Plan Does NOT Change" table corrected: SS1.3, SS2.2, SS5.1, SS8.3 removed from "unchanged" list (Plan A modifies these)
