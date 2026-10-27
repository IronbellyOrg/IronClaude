# Consolidated Execution Order

> Generated: 2026-03-20
> Input: dedup-report.md + 4 tier summaries
> Surviving issues: 23 (ISS-004 superseded by ISS-003)

---

## Execution Phases

### Phase 0: Frontmatter Updates (atomic, no dependencies)

| Order | Issue ID | Severity | Spec Section | Proposal Summary | Dependencies |
|-------|----------|----------|-------------|-----------------|-------------|
| 0.1 | ISS-020 | LOW | YAML frontmatter line 16 | Delete `fidelity.py` from `relates_to` | None |
| 0.2 | ISS-001/003 supplement | CRITICAL | YAML frontmatter (new keys) | Add `module_disposition` table + `baseline_commit` | None |

**Rationale**: Frontmatter is machine-parseable metadata. Both edits are additive/delete-only and cannot conflict with body text changes. Apply first to signal intent.

**Total spec sections modified**: 1 (YAML frontmatter)

---

### Phase 1: Global Baseline Context (no FR dependencies)

| Order | Issue ID | Severity | Spec Section | Proposal Summary | Dependencies |
|-------|----------|----------|-------------|-----------------|-------------|
| 1.1 | ISS-019 | MEDIUM | New Section 1.3 (after 1.2) | Insert "v3.0 Baseline" — module inventory, pre-satisfied requirements, genuinely new code, dead code | None |
| 1.2 | ISS-011 | MEDIUM | Section 1.2 + frontmatter | Add spec_patch.py to `relates_to` + "Preserved and coexisting" clause in Scope Boundary | ISS-019 (so spec_patch.py can be listed in 1.3 inventory too) |

**Rationale**: Establishes the global "this is not greenfield" context that all subsequent per-FR changes reference. ISS-019 first, ISS-011 second (adds spec_patch.py which can be cross-listed in 1.3).

**Total spec sections modified**: 3 (Section 1.2, new Section 1.3, frontmatter `relates_to`)

---

### Phase 2: CRITICAL FR Reclassifications (ISS-001, ISS-002, ISS-003)

Apply in order: FR-9 first (most complex, establishes pattern), then FR-4, then FR-7.

| Order | Issue ID | Severity | Spec Section | Proposal Summary | Dependencies |
|-------|----------|----------|-------------|-----------------|-------------|
| 2.1 | ISS-003 | CRITICAL | FR-9 Description | Replace FR-9 description with extended version: v3.0 Baseline inventory + Delta list. Subsumes ISS-004 threshold delta. | Phase 0 (frontmatter disposition) |
| 2.2 | ISS-002 | CRITICAL | FR-4, FR-4.1, FR-4.2 | Add "Existing baseline" paragraph to FR-4. Mark 3 ACs as `[x]` in FR-4.1, 5 ACs as `[x]` in FR-4.2, add new AC items. | Phase 0 |
| 2.3 | ISS-001 | CRITICAL | FR-7 + new baseline subsection | Edit FR-7 description (2 sentences), insert FR-7 Baseline subsection listing 7 existing components. | Phase 0 |

**Rationale**: Critical-summary recommends FR-9 first (hardest case, validates pattern). FR-4 moderate complexity. FR-7 simplest. All three share the baseline/delta pattern.

**Total spec sections modified**: 5 (FR-9 Description, FR-4 Description, FR-4.1 ACs, FR-4.2 ACs, FR-7 + new subsection)

---

### Phase 3: HIGH — Independent (no CRITICAL dependency)

| Order | Issue ID | Severity | Spec Section | Proposal Summary | Dependencies |
|-------|----------|----------|-------------|-----------------|-------------|
| 3.1 | ISS-009 | HIGH | FR-3 | Add canonical machine keys to severity rule table, implementation contract (`SEVERITY_RULES` dict, `get_severity()`), baseline statement, 4 missing mismatch types | None (FR-3 is genuinely new) |

**Rationale**: ISS-009 is the only HIGH issue with no CRITICAL dependency. Can run in parallel with Phase 2.

**Total spec sections modified**: 1 (FR-3)

---

### Phase 4: HIGH — FR-9 Cluster (depends on Phase 2.1 / ISS-003)

Apply in strict sequence: ISS-007 → ISS-005 → ISS-006. ISS-004 is verification-only.

| Order | Issue ID | Severity | Spec Section | Proposal Summary | Dependencies |
|-------|----------|----------|-------------|-----------------|-------------|
| 4.1 | ISS-007 | HIGH | FR-9 Description + Patch Format + ACs 1,3 | Reframe to ClaudeProcess-primary with MorphLLM-compatible format. Replace "Patch Format (MorphLLM Lazy Snippets)" with "Patch Format (Engine-Agnostic Lazy Snippets)". Add Applicator Selection subsection. | ISS-003 (Phase 2.1) |
| 4.2 | ISS-005 | HIGH | FR-9 AC bullet 5 | Replace terse AC with multi-line per-patch contract. Explicitly retire v3.0 `_check_diff_size()` whole-file approach. | ISS-003 (Phase 2.1) |
| 4.3 | ~~ISS-004~~ | ~~HIGH~~ | ~~FR-9~~ | ~~SUPERSEDED by ISS-003. Verify only: threshold delta in ISS-003 output, 30% consistent across ACs/NFR-5/US-4.~~ | ISS-003 |
| 4.4 | ISS-006 | HIGH | FR-9 AC bullets 9-10 | Replace all-or-nothing rollback ACs with per-file rollback + coherence check specification. | ISS-003 (Phase 2.1), ISS-005 (Phase 4.2 — per-patch rejection determines per-file outcomes) |

**Internal ordering constraint**: ISS-007 first (modifies Description block written by ISS-003). ISS-005 second (modifies AC, independent of Description). ISS-006 last (extends AC, depends on ISS-005's per-patch infrastructure for per-file outcomes).

**Total spec sections modified**: 3 (FR-9 Description refinement, FR-9 Patch Format, FR-9 ACs)

---

### Phase 5: HIGH — Convergence Architecture (depends on Phase 2.1 + 2.3)

| Order | Issue ID | Severity | Spec Section | Proposal Summary | Dependencies |
|-------|----------|----------|-------------|-----------------|-------------|
| 5.1 | ISS-008 | HIGH | Frontmatter + FR-6 Description | Remove `deviation_registry.py` from `relates_to`. Update FR-6 description to reference DeviationRegistry's actual location in `convergence.py:50-225`. | ISS-001 (Phase 2.3) |
| 5.2 | ISS-010 | HIGH | FR-7 + FR-9 integration | Add convergence loop wrapping remediation: `execute_fidelity_with_convergence()` calls `execute_remediation()` between runs. Document dual budget systems (convergence 3 runs vs legacy 2 attempts). | ISS-001 (Phase 2.3), ISS-003 (Phase 2.1) |

**ISS-008 and ISS-010 are independent** of each other and can run in parallel.

**Total spec sections modified**: 3 (frontmatter, FR-6, FR-7/FR-9 integration text)

---

### Phase 6: MEDIUM — Batch 3: Problem Statement + Scope (depends on Phase 1)

Already handled in Phase 1 (ISS-019 + ISS-011). Noted here for batch-completeness tracking.

---

### Phase 7: MEDIUM — Batch 4: FR-2 + FR-5 Parser/Splitter Pipeline

| Order | Issue ID | Severity | Spec Section | Proposal Summary | Dependencies |
|-------|----------|----------|-------------|-----------------|-------------|
| 7.1 | ISS-015 | MEDIUM | FR-2 | Add 5 robustness ACs (malformed YAML, irregular tables, missing language tags), `ParseWarning` collection, Critical Path Note (FR-2→FR-1→FR-4→FR-7) | None |
| 7.2 | ISS-018 | MEDIUM | FR-5 | Expand FR-5: `SpecSection` dataclass, `split_into_sections()` function, splitting rules, dimension-to-section mapping table. 12 ACs replacing original 6. | ISS-015 (FR-2 must be scoped first) |

**Total spec sections modified**: 2 (FR-2, FR-5)

---

### Phase 8: MEDIUM — Batch 1: FR-7 Completeness Cluster

| Order | Issue ID | Severity | Spec Section | Proposal Summary | Dependencies |
|-------|----------|----------|-------------|-----------------|-------------|
| 8.1 | ISS-012 | MEDIUM | FR-7 (new subsection) + Appendix A | "Pipeline Integration" subsection: convergence runs within step-8 boundary, 4 new ACs. Appendix A convergence detail diagram. | ISS-001 (Phase 2.3 — FR-7 reclassification) |
| 8.2 | ISS-013 | MEDIUM | FR-7 Gate Authority Model (new subsection) | Step Ordering table documenting 3 undocumented ordering semantics + 3 ACs | ISS-012 (pipeline context sets up step ordering) |
| 8.3 | ISS-016 | MEDIUM | FR-7 (new FR-7.1 subsection) + FR-7/FR-8 Dependencies | Interface contract: `handle_regression()` signature, `RegressionResult` dataclass, lifecycle, budget accounting, ownership boundaries. 6 new ACs. | ISS-001 (Phase 2.3) |

**Ordering constraint**: ISS-012 before ISS-013 (pipeline context first, then step ordering). ISS-016 independent of both but logically follows.

**Combined**: 4 + 3 + 6 = **13 new ACs** for FR-7.

**Total spec sections modified**: 4 (FR-7 Pipeline Integration, FR-7 Step Ordering, FR-7.1, Appendix A)

---

### Phase 9: MEDIUM — Batch 2: FR-4 Family

| Order | Issue ID | Severity | Spec Section | Proposal Summary | Dependencies |
|-------|----------|----------|-------------|-----------------|-------------|
| 9.1 | ISS-014 | MEDIUM | FR-4.1 | Insert `validate_semantic_high()` function signature after protocol table. Add 2 ACs (replaces ISS-002's single AC). | ISS-002 (Phase 2.2) |
| 9.2 | ISS-017 | MEDIUM | FR-4.2 | Add 1 AC: truncation markers must include section heading. Code fix: update `TRUNCATION_MARKER` constant + `_truncate_to_budget()` signature. | ISS-002 (Phase 2.2) |

**Total spec sections modified**: 2 (FR-4.1, FR-4.2)

---

### Phase 10: LOW — Remaining Cleanups

| Order | Issue ID | Severity | Spec Section | Proposal Summary | Dependencies |
|-------|----------|----------|-------------|-----------------|-------------|
| 10.1 | ISS-021 | LOW | FR-6 ACs | Add AC: run metadata uses typed `RunMetadata` dataclass | None |
| 10.2 | ISS-024 | LOW | FR-6 (new subsection) | Add "Finding Dataclass Extension" subsection: `rule_id`, `spec_quote`, `roadmap_quote` fields + backward compat note | None (but ISS-009 defines severity rules that use `rule_id`) |
| 10.3 | ISS-023 | LOW | FR-7 Gate Authority Model | Expand legacy mode sentence with `build_spec_fidelity_prompt()` parenthetical + convergence-mode role sentence | ISS-001 (Phase 2.3) |
| 10.4 | ISS-022 | LOW | FR-8 Description + Isolation + Cleanup | Add "extends existing temp dir isolation in convergence.py" acknowledgment to 3 paragraphs | ISS-001 (Phase 2.3) |

**Total spec sections modified**: 4 (FR-6, FR-7, FR-8)

---

### Phase 11: Validation

After all phases, verify:

- [ ] All three MODIFY FR descriptions (FR-4, FR-7, FR-9) acknowledge "extends existing" not "create new"
- [ ] `module_disposition` frontmatter lists all 6 modules with correct actions
- [ ] `fidelity.py` removed from `relates_to`; `spec_patch.py` added
- [ ] `deviation_registry.py` removed from `relates_to`
- [ ] Section 1.3 baseline inventory present with module table, pre-satisfied requirements, new code, dead code
- [ ] FR-4.1 and FR-4.2 have `[x]`/`[ ]` split matching code reality
- [ ] FR-4.1 has `validate_semantic_high()` function signature and 2 specific ACs
- [ ] FR-4.2 has truncation marker heading AC
- [ ] FR-9 delta list covers ISS-005, ISS-006, ISS-007 explicitly
- [ ] FR-9 Patch Format section says "Engine-Agnostic" with ClaudeProcess-primary Applicator Selection
- [ ] FR-9 ACs reflect per-patch granularity (ISS-005) and per-file rollback (ISS-006)
- [ ] FR-7 baseline subsection lists all 7 existing components
- [ ] FR-7 has Pipeline Integration + Step Ordering + FR-7.1 Interface Contract subsections (13 new ACs)
- [ ] FR-3 severity rule table has canonical machine keys + implementation contract
- [ ] FR-2 has 5 robustness ACs + Critical Path Note
- [ ] FR-5 has expanded splitter specification with 12 ACs
- [ ] FR-6 has Finding Dataclass Extension subsection + RunMetadata AC
- [ ] FR-8 acknowledges existing temp dir isolation in convergence.py
- [ ] No dangling "create" or "build new" language remains for MODIFY-disposition modules
- [ ] All cross-references (FR-6→FR-9, FR-8→FR-7, etc.) still resolve
- [ ] ISS-004 is marked SUPERSEDED BY ISS-003 with validation checklist passed

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total issues | 24 |
| Superseded (no action) | 1 (ISS-004) |
| Surviving for execution | 23 |
| Execution phases | 11 (0–10 + validation) |
| Parallelizable phases | Phase 0+1 ∥ Phase 2+3; Phase 5.1 ∥ 5.2; Phase 8.1 ∥ 8.3 |
| Total spec sections modified | ~25 distinct locations |
| New spec subsections created | 6 (Section 1.3, FR-7 Pipeline Integration, FR-7 Step Ordering, FR-7.1, FR-5 splitter, FR-6 Finding Extension) |
| New acceptance criteria added | ~48 across all FRs |
| Estimated total lines added to spec | ~300 |
| Estimated total lines modified in spec | ~40 |
| Estimated total lines deleted from spec | ~5 |
