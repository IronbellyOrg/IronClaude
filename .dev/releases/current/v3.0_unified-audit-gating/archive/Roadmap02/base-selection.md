

---
base_variant: "A (Opus Architect)"
variant_scores: "A:81 B:74"
---

# Scoring Criteria

Derived from the debate's convergence points and remaining disputes, weighted by impact on a 0.92-complexity implementation program:

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| **Actionability** | 25% | Can a team start sprint planning directly from this roadmap? |
| **Requirement Traceability** | 20% | Are FR/NFR/SC codes linked to specific deliverables? |
| **Risk Treatment Specificity** | 15% | Are mitigations owned, scheduled, and measurable? |
| **Architectural Precision** | 15% | Does the roadmap reduce implementation ambiguity? |
| **Timeline Realism** | 10% | Are estimates honest about uncertainty without false precision? |
| **Rollout Safety** | 10% | Are promotion gates well-defined with clear criteria? |
| **Maintainability** | 5% | Can the roadmap be updated without cascading rewrites? |

---

# Per-Criterion Scores

## 1. Actionability (25%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| File manifest with line estimates | Yes (7+7 files, line counts) | No manifest |
| Phase task decomposition | Numbered sub-tasks per phase | Workstream groupings |
| Go/no-go checklists | Checkbox format per phase | Exit criteria prose |
| Sprint-ready granularity | Directly translatable | Requires decomposition step |

**A: 88 / B: 68**

Opus provides an enumerated file manifest (debate concession: Haiku acknowledged this is "immediately actionable for sprint planning"), numbered implementation steps within each phase, and checkbox-style go/no-go criteria. Haiku's workstream groupings are well-organized but require an additional decomposition step before sprint planning can begin.

## 2. Requirement Traceability (20%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Inline FR/NFR/SC codes | Extensive (FR-001 through FR-047, NFR-001 through NFR-018, SC-001 through SC-016) | Sparse (SC codes in exit criteria only) |
| Validation matrix | Full SC-to-phase-to-method mapping | Concern-grouped validation strategy |
| Blocker-to-phase linkage | Explicit (Blocker 6, 8, 9 with phase gates) | Referenced but not systematically linked |

**A: 90 / B: 65**

Opus's inline traceability is a clear strength acknowledged in the debate (Haiku conceded "Opus's FR/NFR/SC inline codes make audit and compliance straightforward"). Haiku's concern-based validation grouping (Foundation/Integration/Reliability/Governance/Rollout) is valuable for test strategy but does not substitute for per-item traceability.

## 3. Risk Treatment Specificity (15%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Risk table format | Tabular with #, risk, mitigation, owner | Numbered list with impact/mitigation |
| Owner assignment | Named roles per risk | General role references |
| Governance risks | Implicit in open decisions table | Explicit governance risk category (#11, #12) |
| Scope creep protection | Deferred markers mentioned | Explicit anti-scope-creep mitigation |

**A: 76 / B: 78**

Roughly even. Opus's tabular format with owner columns is more scannable. Haiku's explicit governance risk category and scope-creep mitigation (#12) are stronger on the policy dimension. The debate's partial convergence on merging Opus's owner-assignment with Haiku's governance-risk category is well-founded.

## 4. Architectural Precision (15%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Module placement guidance | Explicit file paths with rationale | Deferred to implementation |
| Data model specification | Field-level detail for AuditLease, AuditGateResult | Same fields, less inline detail |
| Integration point enumeration | Dependency table with file locations | Numbered dependency list |
| Failure class taxonomy | Detailed sub-types with routing rules | Referenced but not enumerated inline |

**A: 85 / B: 70**

Opus provides more implementation-ready architectural detail. The debate's unresolved dispute on module placement is real, but for a 0.92-complexity program, Opus's argument that "reducing ambiguity at every level is worth the maintenance cost" is persuasive. The debate's compromise recommendation — include as "Architect Recommendation" appendix — is the right call.

## 5. Timeline Realism (10%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Estimate format | Day ranges per phase (e.g., "10-14 days") | Week ranges with schedule drivers |
| Variance acknowledgment | Implicit in ranges | Explicit "primary schedule drivers" list |
| Overall program estimate | Not explicitly stated | "10 weeks best-case, 12-16 expected" |
| Sequencing guardrails | Embedded in go/no-go criteria | Standalone numbered rules |

**A: 68 / B: 82**

Haiku wins here. The debate produced a clear concession from Opus: "week-level estimates with named schedule drivers are more appropriate for program-level communication." Haiku's standalone sequencing guardrails and explicit schedule driver enumeration are superior for stakeholder communication. Opus's day-level ranges, while useful for sprint planning, are program-level false precision.

## 6. Rollout Safety (10%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Promotion gate criteria | KPI codes (M1, M4, M5, M7, M9) per transition | Prose criteria per transition |
| Shadow window specification | "Minimum 2-week observation window" | Reliability Owner discretion |
| Rollback drill | Referenced in M10 | Explicitly sequenced in Phase 4 |
| Post-promotion hardening | Not explicitly addressed | Workstream 3 in Phase 4 |

**A: 80 / B: 75**

Opus's KPI-coded promotion gates are more auditable. The shadow window debate converged on "provisional 2-week floor, Reliability Owner can override with documented justification" — closer to Opus's position. Haiku's post-promotion hardening workstream is a valuable addition missing from Opus.

## 7. Maintainability (5%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Document structure | Flat phases with subsections | Numbered hierarchical sections |
| Implementation detail coupling | High (file paths, line estimates) | Low (responsibilities and contracts) |
| Stakeholder readability | Engineer-focused | Mixed audience |

**A: 65 / B: 78**

Haiku's cleaner separation of concerns makes it easier to maintain as implementation details change. Opus's embedded file paths create update obligations. However, per the debate compromise, marking implementation details as "Architect Recommendation" appendix mitigates this.

---

# Overall Scores

| Criterion | Weight | A (Opus) | B (Haiku) | A Weighted | B Weighted |
|-----------|--------|----------|-----------|------------|------------|
| Actionability | 25% | 88 | 68 | 22.0 | 17.0 |
| Requirement Traceability | 20% | 90 | 65 | 18.0 | 13.0 |
| Risk Treatment Specificity | 15% | 76 | 78 | 11.4 | 11.7 |
| Architectural Precision | 15% | 85 | 70 | 12.8 | 10.5 |
| Timeline Realism | 10% | 68 | 82 | 6.8 | 8.2 |
| Rollout Safety | 10% | 80 | 75 | 8.0 | 7.5 |
| Maintainability | 5% | 65 | 78 | 3.3 | 3.9 |
| **Total** | **100%** | | | **82.3** | **71.8** |

**Rounded: A: 82, B: 72**

---

# Base Variant Selection Rationale

**Variant A (Opus Architect)** is selected as the merge base for three reasons:

1. **Sprint-readiness gap is decisive.** The roadmap's primary consumer is the implementation team. Opus's file manifest, numbered task decomposition, inline requirement codes, and checkbox go/no-go criteria mean a team can begin sprint planning immediately. Haiku requires an intermediate decomposition step that adds latency and interpretation risk at 0.92 complexity.

2. **Traceability is structural, not cosmetic.** Opus's FR/NFR/SC inline codes are woven throughout every phase. Retrofitting these into Haiku's structure would require touching nearly every section. Incorporating Haiku's improvements into Opus requires additive changes (new sections, reformatted timelines) rather than structural rewrites.

3. **Debate concessions favor Opus's foundation.** Haiku conceded on file manifest value, requirement traceability format, and shadow window floor — all structural elements already present in Opus. Opus's concessions (timeline granularity, sequencing guardrails format, shadow window flexibility) are additive changes easily merged into Opus's structure.

---

# Specific Improvements to Incorporate from Variant B (Haiku)

### Must incorporate

1. **Week-level timeline estimates with named schedule drivers** (debate convergence). Replace Opus's day ranges at program level. Add Haiku's "primary schedule drivers" list and "10-16 week expected range" framing. Reserve day-level for sprint planning appendix.

2. **Standalone sequencing guardrails** (debate convergence, ~90%). Add Haiku's four numbered rules as a dedicated section, supplementing Opus's per-phase go/no-go criteria rather than replacing them.

3. **Explicit governance risk items** (#11 unowned blockers, #12 scope creep into task-gating). Add to Opus's risk table as distinct entries with mitigations.

4. **Post-promotion hardening workstream** (Phase 4, Workstream 3). Opus's Phase 4 lacks explicit post-promotion review. Add Haiku's false-positive/false-negative review, operator workflow clarity check, and v1.3 handoff.

5. **Shadow window compromise language**: "Minimum observation window determined by Reliability Owner, with a provisional floor of 2 weeks pending calibration data. Reliability Owner may shorten with documented statistical justification."

6. **Concern-based validation grouping** (Foundation/Integration/Reliability/Governance/Rollout). Add as a companion to Opus's SC-to-phase matrix — both perspectives aid different audiences.

7. **Required roles section**. Haiku's 9-role enumeration with responsibility descriptions is more complete than Opus's "Roles Required" list. Incorporate as the roles section in the merged document.

### Should incorporate

8. **Module placement as "Architect Recommendation" appendix** (debate compromise on D-04). Keep Opus's file path guidance but move to a clearly labeled appendix with "guidance, not mandate" framing.

9. **Haiku's strategic objectives and architectural priorities** from the executive summary. Opus's executive summary is implementation-focused; Haiku's adds strategic framing useful for stakeholder buy-in.

10. **Explicit scope boundaries section** (Haiku §1, "In scope / Explicitly deferred"). Opus mentions deferral markers but doesn't have a clean scope boundary block.

### Resolve per debate recommendation

11. **G-012 phase placement**: Include in merge as Phase 1 (gate logic + unit tests) with Phase 2 integration wiring. Note: "If single implementer, defer gate logic to Phase 2."

12. **TUI placement**: Default to Phase 3 in merge. Note: "If dedicated TUI engineer available, Phase 2 parallel workstream is feasible."
