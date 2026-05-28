---
base_variant: opus-architect
variant_scores: "A:84 B:74"
---

# Roadmap Variant Scoring & Base Selection

## 1. Scoring Criteria (derived from debate)

Six criteria emerged from the transcript, weighted by debate emphasis:

| # | Criterion | Weight | Source |
|---|-----------|--------|--------|
| C1 | Per-FR rollback granularity & co-revert visibility | 20% | D1, D3, D12 + Opus rebuttal on mutual-coupling |
| C2 | Contract-freeze timing & change-detection points | 15% | D2, D8, D9 |
| C3 | Mutual-coupling visibility (FR-CONV.5↔.6, FR-CONV.3↔.1) | 15% | Convergence assessment "decisive" call |
| C4 | Architectural-surface enumeration (COMP-001..006) | 10% | Convergence assessment "decisive" call |
| C5 | Schedule honesty vs stakeholder commitment | 10% | D4 |
| C6 | Governance consolidation (FLAG/MET/OPS) | 10% | D5, D10 |
| TDD-T1 | Technical completeness (DM/API/COMP coverage from TDD §7, §8, §10) | 10% | TDD §7 (5 entities), §8 (5 contracts), §10 (6 components) |
| TDD-T2 | Testing strategy alignment (TDD §15.2 25-fixture catalogue) | 5% | TDD §15.2 |
| TDD-T3 | Migration feasibility (TDD §19 phasing + co-revert matrix) | 5% | TDD §19.1, §19.4 |

## 2. Per-Criterion Scores

| Criterion | Variant A (Opus) | Variant B (Haiku) | Evidence |
|---|---|---|---|
| C1 Rollback granularity | 95 | 75 | A: 7 milestones = 7 rollback units with per-FR MIG-001..007 + explicit co-revert in §19.4. B: 5 milestones bundle FR-CONV.5+.6 into M4; per-FR rollback survives via PRs but milestone-boundary alignment is lost |
| C2 Contract-freeze timing | 70 | 85 | A: Just-in-time DM placement (DM-001 in M2, DM-002 in M3, DM-003 in M6); contract drift only catchable at commit time. B: M1 freezes DM-001..005 + API-001..004 + COMP-001..006 + NFR-CONV.1..10 (26 rows) before any FR work — strongest change-detection point |
| C3 Mutual-coupling visibility | 90 | 65 | A: Dependency graph explicitly annotates "M5/M6 mutual-shape coupling" and "TB-Add catalogue INV-010" cross-edges. B: Flat linear graph M1→M2→M3→M4→M5 hides INV-010 (FR-CONV.3↔.1) and INV-012 (FR-CONV.5↔.6) coupling |
| C4 Component enumeration | 70 | 90 | A: Inline "Comp" column scattered across milestones (rf-qa.md in M1, rf-task-builder.md in M2/M5, rf-qa-qualitative.md in M3/M4/M6). B: M1 rows 10-15 enumerate COMP-001..006 as a single architectural-surface map matching TDD §6.2 component diagram |
| C5 Schedule honesty | 80 | 80 | A: Calendar dates (2026-05-15 → 2026-08-21) give stakeholders commitments. B: Week-relative anchored to "TDD Design Complete 2026-05-21 + Q-DM-1 ownership" honors actual blocker. Both 14-week total; Q-DM-1 risk identical |
| C6 Governance consolidation | 75 | 85 | A: Per-FR FLAG_* placement (FF_TB_ADD_1_THROUGH_8 in M1, etc.) + risk register at end. B: M5 consolidates FLAG-TB-ADD-1-8, FLAG-EXECUTION-CONTEXT, FLAG-INHERITED-VERDICT, FLAG-FIVE-AXES, FLAG-RETRY-GUARDS, FLAG-DNSP-EMISSION + MET-001..006 as numbered rows |
| TDD-T1 Technical completeness | 95 | 90 | A: Maps all 5 DMs to specific milestones with field-by-field rows (DM-001.References, DM-001.SourceAreas, DM-001.KeyConstraints, etc.); explicit API-001..004 in landing milestones. B: M1 enumerates DM-001..005 + API-001..004 + COMP-001..006 as rows but defers field-level decomposition to FR landings |
| TDD-T2 Testing alignment | 95 | 90 | A: TEST-001..025 distributed to milestone of consuming FR; explicit fixture-to-AC mapping per row. B: TEST-001..025 grouped in M2-M5; fixture-to-FR clear but milestone-fixture binding looser |
| TDD-T3 Migration feasibility | 90 | 85 | A: MIG-001..007 one per FR + M7 audit; matches TDD §19.1 M1.1..M1.7 phasing exactly; §19.4 co-revert matrix surfaced in dependency graph. B: MIG-001..006 in landing milestones + MIG-007 in M5; co-revert matrix only in risk register, not in structure |

## 3. Overall Scores

**Variant A (Opus): 84.25**
- Weighted: (95×0.20) + (70×0.15) + (90×0.15) + (70×0.10) + (80×0.10) + (75×0.10) + (95×0.10) + (95×0.05) + (90×0.05) = 19.0 + 10.5 + 13.5 + 7.0 + 8.0 + 7.5 + 9.5 + 4.75 + 4.5 = **84.25**

**Variant B (Haiku): 81.0**
- Weighted: (75×0.20) + (85×0.15) + (65×0.15) + (90×0.10) + (80×0.10) + (85×0.10) + (90×0.10) + (90×0.05) + (85×0.05) = 15.0 + 12.75 + 9.75 + 9.0 + 8.0 + 8.5 + 9.0 + 4.5 + 4.25 = **81.0**

**Justification:** A wins on the three highest-weighted criteria (C1 rollback granularity, C3 mutual-coupling visibility, TDD-T1 technical completeness = 45% combined weight) by margins of 20+15+5 = 40 points. B wins on C2, C4, C6 (35% combined) by margins of 15+20+10 = 45 points but at lower weights. The decisive factor is that Opus's structural commitments to mutual coupling and per-FR rollback are *technically load-bearing* per the debate ("Opus is decisively stronger on mutual-coupling visibility"), while Haiku's wins are *presentational* (consolidated tables, contract-freeze ceremony) that the merge can incorporate without changing structure.

## 4. Base Variant Selection: **opus-architect**

**Rationale:**

1. **Mutual-coupling visibility is non-negotiable.** The convergence assessment names this as one of two "decisively stronger" findings. INV-012 (FR-CONV.5↔.6 dedup-key) and INV-010 (FR-CONV.3↔.1 enumeration) coupling drive co-revert decisions per TDD §19.4. Haiku's flat M1→M5 graph cannot encode this without bundling FR-CONV.5 and FR-CONV.6 into one milestone — which Haiku does (M4), but at the cost of hiding the equally-important FR-CONV.3↔.1 coupling.

2. **Per-FR rollback granularity matches TDD §19.1 phasing.** TDD §19.1 specifies M1.1..M1.7 (seven phases, one per FR + audit). Opus's 7-milestone structure is the literal structural translation; Haiku's 5-milestone structure requires a mental mapping from "M2 contains FR-CONV.1 then FR-CONV.2" back to the TDD phases.

3. **Co-revert matrix is structurally encoded.** Opus surfaces the FR-CONV.5/.6 joint-revertability in the dependency graph annotation; Haiku relegates it to a single line in the M4 dependency note.

4. **Technical completeness edges higher.** Opus's field-level DM rows (DM-001.References, DM-001.SourceAreas, etc.) give implementers a per-field acceptance row; Haiku's M1 DM rows are entity-level only.

5. **The merge can absorb Haiku's wins cheaply.** Adding an M1 architectural-surface map (Haiku's COMP-001..006 enumeration) and an M7 consolidated FLAG-*/MET-*/OPS-* governance table to Opus's structure requires inserting ~12 rows; restructuring Haiku's M1→M5 into 7 per-FR milestones requires re-decomposing every row.

## 5. Improvements from Variant B (Haiku) to Incorporate in Merge

| # | Element to Port | Source in B | Target in Merged Roadmap | Rationale |
|---|---|---|---|---|
| I1 | **M1 Architectural-Surface Map** — add COMP-001..006 as numbered rows enumerating the 6 modification points (task-builder/SKILL.md orchestrator, rf-task-builder, rf-qa, rf-qa-qualitative, rf-analyst, rf-team-lead preservation) | B M1 rows 10-15 | Insert as a "Pre-M1: Architectural Surface" section before Opus M1, OR as M0 rows 1-6 | Gives reviewers a single page showing all 6 modification points (TDD §6.2 component diagram) before per-FR work begins |
| I2 | **M1 Contract-freeze rows for DM-001..005, API-001..004, NFR-CONV.1..10** | B M1 rows 1-9, 16-26 | Add to Opus M1 (or new M0) as entity-level rows; keep Opus's field-level rows in their FR milestones | Catches contract drift at the milestone gate rather than at commit time; addresses Haiku's strongest argument (C2 contract-freeze timing) without losing field-level traceability |
| I3 | **Consolidated FLAG-*/MET-*/OPS-* tables in M7** | B M5 rows 12-22 (FLAG-TB-ADD-1-8, FLAG-EXECUTION-CONTEXT, FLAG-INHERITED-VERDICT, FLAG-FIVE-AXES, FLAG-RETRY-GUARDS, FLAG-DNSP-EMISSION; MET-001..006; OPS-001..007) | Add to Opus M7 as a consolidated "GA Readiness Checklist" table | Single-page GA-tagging audit artifact; Opus already places governance items in M7 but scatters them across rows — consolidate into one table per type |
| I4 | **Week-relative scheduling option in Timeline Estimates** | B Timeline Estimates table | Add a second "Week-relative" column alongside Opus's calendar column in §Timeline Estimates | Honors Q-DM-1 resolution uncertainty without losing stakeholder-facing dates; both views available |
| I5 | **Self-contained AC strings using `:` separators** (e.g. `severity:HIGH-fixed; source:synthetic-dnsp-fixed`) | B AC column throughout | Apply to Opus AC cells where Opus uses prose | Compresses AC cells, reduces row height, improves table scannability |
| I6 | **Phase Contract DM-005 explicit row** | B M1 row 5 with 10 fields enumerated | Move Opus's DM-005 inline reference in M3 row 6 to a standalone numbered row | TDD §7.1 Entity 5 has 10 named fields; Opus references but doesn't enumerate. Haiku does — port the enumeration |
| I7 | **OPEN-INV-017, OPEN-PR05 explicit tracking in M5/M7 Open Questions** | B M5 Open Questions table | Add to Opus M7 Open Questions (Opus has OPEN-TOKEN but misses OPEN-INV-017 + OPEN-PR05) | TDD §22 lists 6 OPEN questions; Opus carries 4, Haiku carries 5. Merge to cover all 6 |
| I8 | **Risk register IDs prefixed with milestone** (e.g. `R-M1-1`, `R-M3-1`) | B Risk Register table | Apply to Opus K-001..K-010 as suffix annotations | Improves traceability when scanning per-milestone risks |

**Do NOT port from Haiku:**
- Flat 5-milestone structure (loses C1 + C3)
- M1 NFR-CONV.1..10 as deliverable rows (Opus rebuttal is correct: NFR-CONV.10 only testable in M6 where partition concurrency surfaces; aspirational labels in M1 are documentation theater)
- 3-week M2 / 4-week M5 schedule (Opus's uniform 2-week milestones better support per-FR audit cadence)
