# Validation Checklists Reference

> Synthesis Quality Review, Assembly Process, Validation Checklist, and Content Rules, loaded during Stage A.7 by the builder subagent.

---

## Synthesis Quality Review Checklist

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

**This checklist is enforced by the rf-analyst and rf-qa agents** (see Phase 5 in the task phases). The rf-analyst applies these 9 criteria as its Synthesis Quality Review analysis type, and the rf-qa agent independently verifies the analyst's findings with its expanded 13-item Synthesis Gate checklist. The QA agent can fix issues in-place when authorized.

The 9 criteria (used by rf-analyst):

1. Template section headers match the TDD template exactly (`src/superclaude/examples/tdd_template.md`)
2. Tables use the correct column structure (FR/NFR ID numbering, entity tables with Field/Type/Required/Description/Constraints, SLO/SLI/Error Budget tables)
3. No content was fabricated beyond what research files contain
4. Findings cite actual file paths and evidence (not vague descriptions)
5. Architecture sections include at least one diagram (ASCII or Mermaid) with component relationships
6. Requirements use FR-001/NFR-001 ID numbering with priority and acceptance criteria
7. All cross-references between sections are consistent (requirements trace to architecture decisions, risks trace to mitigations, dependencies trace to integration points)
8. **No doc-only claims in Architecture (Section 6), Data Models (Section 7), or API Specs (Section 8).** Only `[CODE-VERIFIED]` findings may appear as current architecture. If the only evidence is a documentation file, reject and flag as `[UNVERIFIED — doc-only]`
9. **Stale documentation discrepancies are surfaced.** Any `[CODE-CONTRADICTED]` or `[STALE DOC]` findings from research files should appear in Open Questions (Section 22), not silently omitted

The rf-qa agent's Synthesis Gate adds 4 additional checks:

10. Content rules compliance (tables over prose, no code reproductions)
11. Section completeness (no placeholders)
12. Hallucinated file path detection (verify parent directories exist)
13. **FR traceability** — spot-check 3 FRs in the synth-04 output: each must cite a PRD epic ID in its Source column. If any FR lacks a PRD epic citation and is not marked "[NO PRD TRACE]", flag as FAIL.

If synthesis QA fails, the QA agent fixes issues in-place (when authorized) and issues remaining unfixed trigger re-synthesis of the affected files.

---

## Assembly Process

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction. This section provides supplementary context for understanding the workflow.

### Step 8: Assemble the TDD

Read all synth files in order and assemble the final document:

1. **Start with the template frontmatter** — fill in all fields from the template. Set `status: "🟡 Draft"`, populate `created_date`, `parent_doc` (link to PRD if applicable), `depends_on`, `tags`, etc.

2. **Write the document header** — the purpose block with document type, relationship to PRD, and tiered usage table.

3. **Write the Document Information table** — Component Name, Component Type, Tech Lead, Engineering Team, Target Release, Last Updated, Status. Include the Approvers table.

4. **Assemble sections in template order** — paste each synth file's content into the correct position. Sections that weren't assigned a synth file (27. References, 28. Glossary) get written directly during assembly from patterns observed in the synth files.

5. **Write the Table of Contents** — generate from actual section headers.

6. **Add Appendices** — Detailed API Specifications, Database Schema, Wireframes, Performance Test Results as applicable.

7. **Add Document History** — initial entry.

8. **Add Document Provenance** — if the TDD was created by consolidating existing docs or from a PRD, add an `Appendix: Document Provenance` subsection documenting the source materials and creation method. Zero content loss: every piece of metadata from source documents must appear somewhere in the TDD.

See the standalone `## Validation Checklist` section below for the full pre-presentation validation checklist.

### Step 10: Present to User

Notify the user:
- Where the final document was written
- Line count and tier classification
- Number of sections populated vs skipped
- Where the research/synth artifacts live (for future reference)
- Any gaps or areas that need manual review

### Step 11: Clean Up Consolidation Sources

If the TDD was created by consolidating existing docs:
- Do NOT delete the source docs automatically
- Present the source docs to the user and confirm they can be archived
- Archive approved sources to `docs/archive/[appropriate-subdir]/`
- Update any references to the archived files in other documents
- Check off items in the stub's consolidation checklist if one exists

---

## Validation Checklist

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

Before presenting the TDD to the user, validate against this checklist (this is encoded in the task file's Assembly phase):

**Structural Completeness:**
- [ ] Frontmatter has all required fields from the template (id, title, status, created_date, parent_doc, depends_on, tags)
- [ ] Document purpose block with tiered usage table present
- [ ] Document Information table has all 7 rows (Component Name, Component Type, Tech Lead, Engineering Team, Target Release, Last Updated, Status) plus Approvers table
- [ ] Table of Contents present and matches actual section headers exactly — no orphaned or missing entries
- [ ] All 28 template sections present (or explicitly marked as N/A with rationale per tier)
- [ ] Total line count within tier budget (Lightweight: 300-600, Standard: 800-1400, Heavyweight: 1400-2200)

**Architecture & Design Quality:**
- [ ] Architecture section (Section 6) includes at least one diagram (ASCII or Mermaid) showing component relationships
- [ ] Data model definitions complete with entity tables (Field / Type / Required / Description / Constraints columns)
- [ ] API contracts specified with endpoint overview tables, request/response examples, and error response format
- [ ] Integration points mapped — system boundaries table populated with upstream, downstream, and external boundaries
- [ ] Key Design Decisions table populated with rationale and alternatives considered
- [ ] Alternative 0: Do Nothing is present in Alternatives Considered (Section 21)

**Requirements & Specifications:**
- [ ] Requirements use FR-001/NFR-001 ID numbering with priority (Must Have / Should Have / Could Have) and acceptance criteria
- [ ] SLO/SLI/Error Budget tables present for Standard and Heavyweight tiers
- [ ] Performance budgets specified with concrete metrics and measurement methods
- [ ] Security considerations documented — threat model, security controls, sensitive data handling

**Evidence & Integrity:**
- [ ] No fabricated claims — all architecture and implementation descriptions backed by `[CODE-VERIFIED]` tags
- [ ] No doc-sourced architectural claims presented as verified without cross-validation tags
- [ ] All `[CODE-CONTRADICTED]` or `[STALE DOC]` findings surfaced in Open Questions (Section 22)
- [ ] All file paths reference actual files that exist (spot-check 5+ paths)
- [ ] No full source code reproductions (interfaces, function bodies, config files)
- [ ] Web research findings include source URLs for every external claim

**Document Quality:**
- [ ] Document History table present with initial entry
- [ ] Tables use correct column structure from template
- [ ] Internal consistency — no contradictions between sections (requirements trace to architecture, risks to mitigations, dependencies to integration points)
- [ ] Readability — scannable structure with tables, headers, bullets; no walls of prose

---

## Content Rules (From Template — Non-Negotiable)

These rules come from the template's structure and conventions. Every TDD must follow them.

| Rule | Do | Don't |
|------|-----|-------|
| **Architecture** | ASCII or Mermaid diagrams with component tables | Multi-paragraph prose for what could be a diagram |
| **Data models** | Entity tables with Field / Type / Required / Description / Constraints | Full TypeScript interface reproductions |
| **API specs** | Endpoint overview tables plus key endpoint details with request/response examples | Reproducing entire OpenAPI specs inline |
| **Requirements** | Functional/Non-functional split with ID numbering (FR-001, NFR-001) | Prose paragraphs mixing requirement types |
| **Testing** | Test pyramid tables by level with coverage targets and tools | Generic "write tests" instructions |
| **Performance** | Budget tables with specific metrics and measurement methods | Vague "should be fast" requirements |
| **Security** | Threat model tables plus security controls with verification methods | General security platitudes without specifics |
| **Alternatives** | Structured Pros/Cons with mandatory "Why Not Chosen" and Do Nothing option | Surface-level dismissal of alternatives |
| **Dependencies** | Tables with Version / Purpose / Risk Level / Fallback | Inline dependency mentions scattered through prose |
| **SLOs** | SLO / SLI / Error Budget tables with burn-rate alerts | Undefined or aspirational reliability targets |
| **Source code** | Summarize behavior with key signatures | Reproduce full function bodies or config files |
| **Evidence** | Inline citations: `file.cpp:123`, `ClassName::method()` | Say "the code does X" without citing where |
| **Uncertainty** | Explicit "Unverified" or "Open Question" markers | Present uncertain findings as verified facts |

**General content principles:**
- Tables over prose whenever presenting multi-item data
- Conciseness over comprehensiveness — the TDD should be scannable, not exhaustive prose
- Every claim needs evidence — if you can't cite a file path or URL, it belongs in Open Questions
- Prefer ASCII/Mermaid diagrams for visual relationships over paragraph descriptions
