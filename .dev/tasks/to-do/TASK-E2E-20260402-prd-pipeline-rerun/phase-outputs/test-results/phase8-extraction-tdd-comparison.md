# Phase 8.1 -- TDD+PRD vs TDD-Only Extraction Comparison

**Date:** 2026-04-02
**Files Compared:**
- NEW: `.dev/test-fixtures/results/test1-tdd-prd/extraction.md` (TDD+PRD enriched)
- PRIOR: `.dev/test-fixtures/results/test1-tdd-modified/extraction.md` (TDD-only)

---

## Structural Comparison

| Dimension | TDD-Only | TDD+PRD | Delta | Assessment |
|-----------|----------|---------|-------|------------|
| Total lines | 462 | 567 | +105 (+22.7%) | PRD enrichment adds substantial content |
| Frontmatter fields | 20 | 20 | 0 | Both have 19 TDD fields + pipeline_diagnostics = 20 lines |
| Body sections (`## ` headers) | 14 | 14 | 0 | Same section structure preserved |
| `nonfunctional_requirements` (frontmatter) | 4 | 9 | +5 | PRD adds 4 compliance NFRs (COMP-001 to COMP-004) plus elevates existing NFRs |
| `risks_identified` (frontmatter) | 3 | 7 | +4 | PRD adds R-004 through R-007 |
| `dependencies_identified` (frontmatter) | 6 | 8 | +2 | PRD adds policy and frontend routing dependencies |
| `success_criteria_count` (frontmatter) | 7 | 10 | +3 | PRD adds session duration, failed login rate, password reset completion |
| `components_identified` (frontmatter) | 4 | 9 | +5 | PRD enrichment surfaces additional components |
| Generator name | `requirements-extraction-agent` | `requirements-design-extraction-agent` | Changed | New agent name reflects PRD-enriched pipeline |

---

## PRD-Specific Content Analysis

| PRD Signal | TDD-Only Count | TDD+PRD Count | Delta | Assessment |
|------------|----------------|---------------|-------|------------|
| Persona "Alex" | 0 | 1 | +1 | PRD persona injected |
| Persona "Jordan" | 0 | 2 | +2 | PRD persona injected |
| Persona "Sam" | 1 | 2 | +1 | Existing ref augmented by PRD persona |
| "GDPR" | 0 | 4 | +4 | PRD compliance content injected |
| "SOC2" | 0 | 4 | +4 | PRD compliance content injected |
| "conversion" | 1 | 1 | 0 | Present in both (TDD success criteria) |
| "session duration" | 0 | 2 | +2 | PRD business metric injected |
| "session" (total) | 2 | 4 | +2 | Additional session references from PRD |
| "PRD Trace" annotations | 0 | 5 | +5 | Traceability links to PRD requirements |
| "PRD Source" annotations | 0 | 4 | +4 | Source attribution to PRD sections |
| "from PRD" references | 0 | 10 | +10 | Explicit PRD provenance markers |
| "PRD S" section refs | 0 | 19 | +19 | PRD section cross-references throughout |
| NFR sections (### NFR-) | 5 (in table) | 9 (individual sections) | +4 | Compliance NFRs added as dedicated sections |

---

## Key Findings

1. **Structural fidelity preserved**: Both files have 20 frontmatter lines and 14 body sections. PRD enrichment adds content within sections rather than creating new top-level sections.

2. **Compliance layer is entirely new**: GDPR (4 mentions), SOC2 (4 mentions), and NIST compliance requirements are absent from TDD-only and present in TDD+PRD. This is the most significant enrichment.

3. **Persona-driven requirements injected**: Alex, Jordan, and Sam persona names appear only in the PRD-enriched version, driving architectural constraints (#9 in the extraction) and open questions (OQ-006 through OQ-008).

4. **Business metrics expanded**: Session duration, failed login rate, and password reset completion are new success criteria sourced from PRD S19.

5. **Risk inventory doubled**: TDD-only has 3 risks; TDD+PRD has 7 -- the 4 additional risks (R-004 through R-007) are all PRD-sourced.

6. **Traceability is strong**: 19 "PRD S" section references and 5 "PRD Trace" annotations provide clear provenance for enriched content.

**Assessment: PASS** -- PRD enrichment adds meaningful compliance, persona, and business metric content without disrupting the TDD structural baseline.
