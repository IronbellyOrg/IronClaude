# MEDIUM Issue Resolution Summary

> Source: 9 MEDIUM issues (ISS-011 through ISS-019) from `issues-classified.md`
> Generated: 2026-03-20
> Method: Parallel brainstorm agents, one per issue

---

## Per-Issue Decisions

### ISS-011 — spec_patch.py not mentioned in v3.05 spec
**Selected**: Proposal #1 — Add to `relates_to` frontmatter + "Preserved and coexisting" clause in Section 1.2 Scope Boundary
**Rationale**: Minimal correct fix. Documents spec_patch.py's dual-mode behavior (legacy vs convergence) and `spec_hash` interaction with FR-6 without modifying any FR. Purely descriptive, no code changes.
**Spec sections touched**: Frontmatter, Section 1.2
**Risk**: LOW

### ISS-012 — Convergence loop vs linear pipeline tension undocumented
**Selected**: Proposal #1 + #3 — "Pipeline Integration" subsection in FR-7 + Appendix A convergence detail diagram
**Rationale**: Adds the critical missing information (convergence runs within step-8 boundary, not as new phase) as normative text plus visual diagram. 4 new acceptance criteria make it testable. Follows the existing wiring-verification bypass pattern as precedent.
**Spec sections touched**: FR-7 (new subsection + 4 ACs), Appendix A (new subsection)
**Risk**: LOW
**Note**: If ISS-001 Proposal #5 (full FR-7 rewrite) is adopted at CRITICAL tier, use Proposal #2 instead (fold pipeline integration into the rewritten description).

### ISS-013 — SPEC_FIDELITY_GATE + wiring step ordering semantics undocumented
**Selected**: Proposal #1 + #2 — Step Ordering table in FR-7 Gate Authority Model + 3 acceptance criteria
**Rationale**: Documents three undocumented ordering semantics: (1) step 9's `spec_fidelity_file` input is decorative, (2) wiring-verification bypasses `_embed_inputs()`, (3) convergence mode does not affect step 9. Combined normative prose + testable ACs.
**Spec sections touched**: FR-7 Gate Authority Model (new subsection + 3 ACs)
**Risk**: LOW
**Note**: Documentation-only gap — code already implements this correctly.

### ISS-014 — validate_semantic_high() referenced but never defined
**Selected**: Proposal #1 — Add function signature + 2 ACs to FR-4.1
**Rationale**: Specifies the orchestrator function that connects existing debate primitives (score_argument, judge_verdict, wire_debate_verdict). Includes `claude_process_factory` parameter for testability. Low disruption, fills the gap between ISS-002's module-level fix and the function-level spec omission.
**Spec sections touched**: FR-4.1 (function spec inserted after protocol table, 2 new ACs)
**Risk**: LOW
**Requires code**: YES — implement `validate_semantic_high()` in semantic_layer.py
**Interaction**: If ISS-002 is also resolved, this proposal's ACs replace ISS-002's single `validate_semantic_high()` AC with more specific criteria.

### ISS-015 — spec_parser.py critical path risk not surfaced
**Selected**: Proposal #1 — Add 5 robustness ACs to FR-2 + Critical Path Note
**Rationale**: FR-2 has zero error-handling ACs despite being the spec's own risk #1. Adds graceful degradation requirements (malformed YAML, irregular tables, missing language tags), `ParseWarning` collection, and real-spec validation. Critical Path Note makes the FR-2→FR-1→FR-4→FR-7 dependency chain explicit.
**Spec sections touched**: FR-2 (5 new ACs + Critical Path Note + Dependencies annotation)
**Risk**: LOW
**Requires code**: YES — spec_parser.py is genuinely new

### ISS-016 — FR-7/FR-8 circular interface not designed
**Selected**: Proposal #1 — New FR-7.1 subsection with interface contract
**Rationale**: Centralizes the calling convention (`handle_regression()` signature), return contract (`RegressionResult` dataclass), lifecycle within convergence loop, budget accounting rule, and ownership boundaries (FR-7 owns budget, FR-8 owns agents, FR-6 is shared). 6 new ACs.
**Spec sections touched**: FR-7 (new FR-7.1 subsection + 6 ACs), FR-7 Dependencies, FR-8 Dependencies
**Risk**: LOW
**Note**: The budget accounting example (Run 1→regression→Run 2 with FR-8→Run 3) makes the abstract rule concrete.

### ISS-017 — TRUNCATION_MARKER missing heading name
**Selected**: Proposal B — Add explicit AC to FR-4.2 + code fix
**Rationale**: Spec prose already says the right thing (`from '<heading>'`) but has no dedicated AC. Adding one makes it independently testable. Code fix updates `TRUNCATION_MARKER` constant and `_truncate_to_budget()` signature with `heading` parameter.
**Spec sections touched**: FR-4.2 (1 new AC)
**Risk**: LOW
**Requires code**: YES — update `semantic_layer.py:28` constant and `_truncate_to_budget()` function

### ISS-018 — Section splitter for chunked comparison does not exist
**Selected**: Proposal #1 — Full splitter specification in FR-5
**Rationale**: Defines `SpecSection` dataclass, `split_into_sections()` function, splitting rules, and dimension-to-section mapping table. This is the complete specification an implementer needs. The `SpecSection` type resolves `semantic_layer.py`'s `list[Any]` typing.
**Spec sections touched**: FR-5 (expanded Description, new splitter spec, 12 ACs replacing original 6)
**Risk**: LOW-MEDIUM
**Requires code**: YES — `spec_parser.py` must implement `SpecSection` and `split_into_sections()`
**Dependency**: Requires FR-2 to be built first or concurrently (ISS-015 critical path)

### ISS-019 — No "existing baseline from v3.0" section in spec
**Selected**: Proposal #1 — Section 1.3 "v3.0 Baseline" in Problem Statement
**Rationale**: Global inventory of pre-existing modules (MODIFY vs CREATE), pre-satisfied requirements (19 items), genuinely new code, and dead code. Positioned before any FR so every reader encounters it. Complements ISS-001/002/003 per-FR fixes without replacing them.
**Spec sections touched**: New Section 1.3 (~45 lines after Section 1.2)
**Risk**: LOW
**Note**: Includes `[x]`/`[ ]` reading convention for downstream per-FR baseline marking.

---

## SUPERSEDED Issues

No MEDIUM issues are fully superseded by CRITICAL or HIGH resolutions. However, partial overlaps exist:

| MEDIUM Issue | Overlapping Resolution | Status |
|--------------|----------------------|--------|
| ISS-014 | ISS-002 (CRITICAL) reclassifies semantic_layer.py as MODIFY and mentions validate_semantic_high() | **NOT SUPERSEDED** — ISS-002 addresses module existence; ISS-014 addresses the spec omission of function signature/contract |
| ISS-017 | ISS-002 mentions truncation fix as "same minor change" | **NOT SUPERSEDED** — ISS-002 provides no standalone spec text or AC for ISS-017 |
| ISS-019 | ISS-001/002/003 reclassify individual FRs from CREATE to MODIFY | **NOT SUPERSEDED** — per-FR fixes do not provide a global baseline inventory; ISS-019 adds the missing overview |

---

## Batch-Applicable Changes

Several MEDIUM issues can be combined into a single spec editing pass per section:

### Batch 1: FR-7 Edits (ISS-012 + ISS-013 + ISS-016)
All three add subsections or ACs to FR-7. Apply as one edit:
1. ISS-012: Pipeline Integration subsection (after Gate Authority Model)
2. ISS-013: Step Ordering table (after Pipeline Integration)
3. ISS-016: FR-7.1 Interface Contract (after Acceptance Criteria)
4. Combined: 4 + 3 + 6 = **13 new ACs** for FR-7

**Ordering constraint**: ISS-012's Pipeline Integration subsection should come before ISS-013's Step Ordering table in the spec, as the pipeline context sets up the step ordering explanation.

### Batch 2: FR-4/FR-4.1/FR-4.2 Edits (ISS-014 + ISS-017)
Both touch the FR-4 family:
1. ISS-014: Function spec + 2 ACs in FR-4.1
2. ISS-017: 1 AC in FR-4.2
Apply in one pass through FR-4.

### Batch 3: Problem Statement + Scope Boundary (ISS-011 + ISS-019)
Both add to Section 1:
1. ISS-019: New Section 1.3 v3.0 Baseline
2. ISS-011: "Preserved and coexisting" clause in Section 1.2
Apply together. ISS-011's spec_patch.py can also be listed in ISS-019's module inventory as a preserved legacy module.

### Batch 4: FR-2 + FR-5 (ISS-015 + ISS-018)
Both relate to the parser/splitter pipeline:
1. ISS-015: FR-2 robustness ACs + Critical Path Note
2. ISS-018: FR-5 splitter specification
These share a dependency chain (FR-5 depends on FR-2). Apply FR-2 changes first, then FR-5.

### Standalone
- ISS-012 Appendix A diagram (additive, no conflict with any batch)

---

## Implementation Priority

| Priority | Issues | Rationale |
|----------|--------|-----------|
| 1 | ISS-019 + ISS-011 (Batch 3) | Foundational context — all other changes are more meaningful with the baseline section in place |
| 2 | ISS-015 + ISS-018 (Batch 4) | Critical path — FR-2 parser robustness and FR-5 splitter unblock the structural checker pipeline |
| 3 | ISS-012 + ISS-013 + ISS-016 (Batch 1) | FR-7 completeness — convergence engine integration, step ordering, and FR-8 interface |
| 4 | ISS-014 + ISS-017 (Batch 2) | FR-4 family — semantic layer orchestrator and truncation marker |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total MEDIUM issues | 9 |
| Superseded by upstream | 0 |
| Spec-only changes | 6 (ISS-011, ISS-012, ISS-013, ISS-015, ISS-016, ISS-019) |
| Spec + code changes | 3 (ISS-014, ISS-017, ISS-018) |
| New spec subsections | 4 (Section 1.3, FR-7 Pipeline Integration, FR-7 Step Ordering, FR-7.1) |
| New acceptance criteria | ~25 total across all FRs |
| Batch groups | 4 (+ 1 standalone appendix addition) |
| Risk: LOW | 7 |
| Risk: LOW-MEDIUM | 2 (ISS-018, ISS-019 Proposal #2 rejected) |
