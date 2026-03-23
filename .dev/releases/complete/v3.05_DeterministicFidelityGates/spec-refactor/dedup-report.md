# Deduplication & Conflict Report

> Generated: 2026-03-20
> Input: 4 tier summaries (CRITICAL, HIGH, MEDIUM, LOW) covering 24 issues (ISS-001–ISS-024)
> Focus: deduplication, conflicts, ordering

---

## 1. DEDUPLICATION ANALYSIS

### 1.1 Full Supersessions

| Superseded Issue | Superseded By | Overlap Type | Action |
|-----------------|---------------|--------------|--------|
| ISS-004 (HIGH) | ISS-003 (CRITICAL) | ISS-003 Proposal #1 delta item 5 explicitly lists `MODIFY _DIFF_SIZE_THRESHOLD_PCT: 50 -> 30 (ISS-004)`. The 30% value is already specified in 6 places in the spec. | **SUPERSEDED** — Close ISS-004. Verify ISS-003 resolution covers threshold. No standalone spec edit needed. |
| ISS-022 FR-4/FR-7/FR-9 portion (LOW) | ISS-001 + ISS-002 + ISS-003 (CRITICAL) | ISS-001 fixes FR-7 "create→extend", ISS-002 fixes FR-4, ISS-003 fixes FR-9. Three of four FR targets are fully covered. | **PARTIALLY SUPERSEDED** — Only FR-8 acknowledgment remains (see Section 1.2). |

### 1.2 Partial Overlaps (Non-Superseding)

| Issue Pair | Overlap | Resolution |
|-----------|---------|------------|
| ISS-002 (CRITICAL) ↔ ISS-014 (MEDIUM) | ISS-002 adds a one-line AC for `validate_semantic_high()`. ISS-014 adds a full function signature + 2 specific ACs. | **Both survive.** ISS-002 addresses module-level CREATE→MODIFY. ISS-014 adds the function-level spec. When both are applied, ISS-014's ACs **replace** ISS-002's single `validate_semantic_high()` AC line. |
| ISS-002 (CRITICAL) ↔ ISS-017 (MEDIUM) | ISS-002 mentions TRUNCATION_MARKER fix as "same minor change" but provides no standalone spec text or AC. | **Both survive.** ISS-017 provides the dedicated AC in FR-4.2 that ISS-002 does not. |
| ISS-001/002/003 (CRITICAL) ↔ ISS-019 (MEDIUM) | CRITICAL issues add per-FR baseline acknowledgments. ISS-019 adds a global Section 1.3 baseline inventory. | **Both survive.** Per-FR fixes provide micro-level detail; ISS-019 provides macro-level overview. Neither replaces the other. |
| ISS-001 (CRITICAL) ↔ ISS-008 (HIGH) | ISS-001 establishes convergence.py as MODIFY. ISS-008 removes phantom `deviation_registry.py` from manifest. | **Both survive.** ISS-001 is prerequisite context; ISS-008 is a distinct cleanup. If ISS-001 Proposal #3 (frontmatter disposition table) is adopted, ISS-008's manifest removal is reinforced. |
| ISS-003 (CRITICAL) ↔ ISS-005 (HIGH) | ISS-003 rewrites FR-9 description with baseline/delta. ISS-005 replaces FR-9 AC bullet 5 with per-patch contract. | **Both survive.** ISS-003 modifies the Description block; ISS-005 modifies an AC bullet. No text collision. ISS-003 must be applied first. |
| ISS-003 (CRITICAL) ↔ ISS-006 (HIGH) | ISS-003 rewrites FR-9 description. ISS-006 modifies FR-9 AC bullets 9-10 for per-file rollback. | **Both survive.** Same rationale as ISS-005 — different text targets within FR-9. |
| ISS-003 (CRITICAL) ↔ ISS-007 (HIGH) | ISS-003 rewrites FR-9 description. ISS-007 refines MorphLLM→ClaudeProcess language within that description. | **Both survive, but order matters.** ISS-003 creates the rewritten description; ISS-007 refines it. ISS-007 must read ISS-003's output as its "before" state. |
| ISS-022 (LOW) ↔ ISS-001 (CRITICAL) | ISS-022 FR-8 temp dir acknowledgment overlaps with ISS-001 if ISS-001 includes a baseline section listing temp dir isolation. | **Conditional.** If ISS-001's baseline section covers temp dir isolation, ISS-022 is FULLY superseded. Otherwise, ISS-022 Proposal A (FR-8 only) survives. Decision: **ISS-022 survives** since ISS-001's selected Proposal #2 adds a baseline subsection before FR-7, not FR-8. |
| ISS-019 (MEDIUM) ↔ ISS-001 Proposal #3 (CRITICAL) | ISS-001 Proposal #3 adds `module_disposition` frontmatter. ISS-019 Proposal #3 also proposes frontmatter disposition. But ISS-001 selected Proposal #2, not #3. | **No collision.** ISS-001's selected proposal (#2) adds a baseline subsection. ISS-019's selected proposal (#1) adds Section 1.3. Both include the frontmatter `module_disposition` table from ISS-001 Proposal #3 as a supplement. Combine: frontmatter from ISS-001 #3 + body from ISS-019 #1. |

### 1.3 No Overlap Detected

The following issues have zero overlap with any other tier:

| Issue | Reason |
|-------|--------|
| ISS-009 (HIGH) | FR-3 severity rule tables — genuinely new, no existing code, no CRITICAL dependency |
| ISS-010 (HIGH) | Remediation ownership — unique integration concern between FR-7/FR-9 |
| ISS-011 (MEDIUM) | spec_patch.py scoping — unique module not mentioned elsewhere |
| ISS-012 (MEDIUM) | Convergence loop documentation — unique FR-7 gap |
| ISS-013 (MEDIUM) | Step ordering semantics — unique FR-7 gap |
| ISS-015 (MEDIUM) | spec_parser.py robustness — unique FR-2 gap |
| ISS-016 (MEDIUM) | FR-7/FR-8 interface contract — unique design gap |
| ISS-018 (MEDIUM) | Section splitter specification — unique FR-5 gap |
| ISS-020 (LOW) | fidelity.py dead code removal — standalone frontmatter edit |
| ISS-021 (LOW) | RunMetadata wiring — standalone FR-6 AC addition |
| ISS-023 (LOW) | prompts.py documentation — standalone FR-7 sentence addition |
| ISS-024 (LOW) | Finding dataclass extension — standalone FR-6 subsection |

---

## 2. CONFLICT DETECTION

### Conflict 1: FR-9 Description Multi-Writer — RESOLVED

**Proposals involved**: ISS-003 (rewrites FR-9 description) + ISS-007 (refines MorphLLM→ClaudeProcess in FR-9 description) + ISS-004 (threshold in FR-9 description)

**Incompatibility**: Three proposals all modify the FR-9 Description block. If applied independently against the current spec text, they would produce three different versions.

**Resolution**: **Sequential application required.** ISS-003 goes first (creates baseline/delta framing), then ISS-007 refines the MorphLLM language within ISS-003's output. ISS-004 is SUPERSEDED by ISS-003's delta item 5. The merged plan (Section 4 of `merged-refactoring-plan.md`) produces a single unified FR-9 Description edit.

**Risk**: LOW — sequential ordering eliminates the conflict.

### Conflict 2: FR-4.1 AC List Dual-Addition — RESOLVED

**Proposals involved**: ISS-002 (adds `validate_semantic_high()` AC to FR-4.1) + ISS-014 (adds 2 more specific ACs to FR-4.1 for the same function)

**Incompatibility**: If both applied independently, FR-4.1 would have a vague AC ("exists and is callable") AND two specific ACs ("implements protocol steps 1-7" + "accepts claude_process_factory"). The vague AC is redundant.

**Resolution**: **ISS-014's ACs replace ISS-002's single AC.** ISS-002's module-level reclassification survives intact; only the one `validate_semantic_high()` AC line is replaced by ISS-014's more specific pair.

**Risk**: LOW — ISS-014 explicitly documents this interaction.

### Conflict 3: Frontmatter `module_disposition` Dual-Source — RESOLVED

**Proposals involved**: ISS-001 Proposal #3 (adds `module_disposition` to frontmatter) + ISS-019 Proposal #3 (also proposes `module_disposition` in frontmatter)

**Incompatibility**: Both propose the same frontmatter key with slightly different schemas.

**Resolution**: ISS-001's selected Proposal #2 does NOT include frontmatter `module_disposition`. The critical-summary recommends supplementing with ISS-001 #3's frontmatter table. ISS-019's selected Proposal #1 is a body section, not frontmatter. **Combine**: Use ISS-001 #3's `module_disposition` YAML in frontmatter (Phase 1 of critical-summary execution order) + ISS-019 #1's Section 1.3 in body. No schema conflict.

**Risk**: LOW — one source for frontmatter, one source for body.

### Conflict 4: ISS-012 Conditional on ISS-001 Proposal Selection — RESOLVED

**Proposals involved**: ISS-012 (Pipeline Integration subsection in FR-7) + ISS-001 (CRITICAL FR-7 reclassification)

**Incompatibility**: ISS-012 medium-summary notes: "If ISS-001 Proposal #5 (full FR-7 rewrite) is adopted, use Proposal #2 instead." ISS-001 selected Proposal #2 (baseline subsection), NOT #5.

**Resolution**: ISS-001's selected proposal (#2) does NOT rewrite FR-7 entirely. ISS-012 Proposal #1 (new Pipeline Integration subsection) is the correct choice. No conflict.

**Risk**: NONE — the conditional does not fire.

### Conflict 5: ISS-017 FR-4.2 vs FR-5 Scope — RESOLVED

**Proposals involved**: ISS-017 Proposal B (AC in FR-4.2) + ISS-017 Proposal C (ACs in both FR-4.2 and FR-5) + ISS-018 (FR-5 splitter specification)

**Incompatibility**: ISS-017 Proposal C adds ACs to FR-5 that depend on ISS-018's section splitter. ISS-017 selected Proposal B (FR-4.2 only).

**Resolution**: Selected proposal (B) is scoped to FR-4.2 only. FR-5 heading propagation deferred to ISS-018. No conflict.

**Risk**: NONE.

### No Other Conflicts Detected

All remaining issues modify distinct spec sections with no text overlap. The only ordering constraints are dependency-based (documented in Section 3 of `execution-order.md`).

---

## Summary

| Metric | Count |
|--------|-------|
| Total issues analyzed | 24 |
| Fully superseded | 1 (ISS-004 by ISS-003) |
| Partially superseded | 1 (ISS-022: 3/4 FRs covered, FR-8 remains) |
| Partial overlaps (both survive) | 7 pairs |
| Conflicts detected | 5 |
| Conflicts resolved | 5 (all resolved via ordering or AC replacement) |
| Unresolved conflicts | 0 |
| Issues with no overlap | 12 |
| **Surviving issues for execution** | **23** (24 - 1 fully superseded) |
