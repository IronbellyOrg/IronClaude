# Phase 8.3 -- Spec+PRD vs Spec-Only Extraction Comparison

**Date:** 2026-04-02
**Files Compared:**
- NEW: `.dev/test-fixtures/results/test2-spec-prd/extraction.md` (Spec+PRD enriched)
- PRIOR: `.dev/test-fixtures/results/test2-spec-modified/extraction.md` (Spec-only)

---

## Structural Comparison

| Dimension | Spec-Only | Spec+PRD | Delta | Assessment |
|-----------|-----------|----------|-------|------------|
| Total lines | 313 | 262 | -51 (-16.3%) | Spec+PRD is more concise |
| Frontmatter fields | 14 | 14 | 0 | Both have 13 spec fields + pipeline_diagnostics |
| Body sections (`## ` headers) | 8 | 8 | 0 | Identical section structure |
| `nonfunctional_requirements` (frontmatter) | 3 | 7 | +4 | PRD adds 4 compliance/metric NFRs |
| `risks_identified` (frontmatter) | 3 | 7 | +4 | PRD adds R4-R7 |
| `dependencies_identified` (frontmatter) | 7 | 9 | +2 | PRD adds dependencies |
| `success_criteria_count` (frontmatter) | 8 | 6 | -2 | Different enumeration granularity |

---

## TDD Cross-Contamination Check (CRITICAL)

| TDD-Specific Content | Spec-Only | Spec+PRD | Assessment |
|---------------------|-----------|----------|------------|
| `UserProfile` (backticked TDD entity) | 0 | 0 | CLEAN |
| `AuthToken` (backticked TDD entity) | 0 | 0 | CLEAN |
| `data_models_identified` (TDD frontmatter field) | 0 | 0 | CLEAN |
| `api_surfaces_identified` (TDD frontmatter field) | 0 | 0 | CLEAN |
| `components_identified` (TDD frontmatter field) | 0 | 0 | CLEAN |
| `test_artifacts_identified` (TDD frontmatter field) | 0 | 0 | CLEAN |
| `migration_items_identified` (TDD frontmatter field) | 0 | 0 | CLEAN |
| `operational_items_identified` (TDD frontmatter field) | 0 | 0 | CLEAN |

**VERDICT: ZERO TDD content leak in either spec-path extraction. Both files are clean.**

---

## PRD-Specific Content Analysis

| PRD Signal | Spec-Only | Spec+PRD | Delta | Assessment |
|------------|-----------|----------|-------|------------|
| Persona "Alex" | 0 | 1 | +1 | PRD persona injected |
| Persona "Jordan" | 0 | 2 | +2 | PRD persona injected |
| Persona "Sam" | 2 | 1 | -1 | Both reference Sam; slight variance |
| "GDPR" | 1 | 4 | +3 | Spec-only has 1 reference; PRD adds 3 more |
| "SOC2" | 0 | 5 | +5 | PRD compliance content injected |
| "conversion" | 0 | 2 | +2 | PRD business metric injected |
| "session duration" | 0 | 2 | +2 | PRD business metric injected |
| "session" (total) | 7 | 8 | +1 | Minimal increase |
| NFR sections (### NFR-) | 3 | 7 | +4 | PRD adds NFR-AUTH.4 through NFR-AUTH.7 |

---

## Key Findings

1. **Zero TDD cross-contamination**: Neither spec-path file contains TDD-specific entities (UserProfile, AuthToken) or TDD-specific frontmatter fields. The extraction pipeline correctly isolates spec-mode from TDD-mode.

2. **Frontmatter field count correct**: Both have exactly 14 frontmatter lines (13 spec fields + pipeline_diagnostics). No TDD-specific fields (data_models, api_surfaces, components, test_artifacts, migration_items, operational_items) appear.

3. **Section count preserved**: Both have exactly 8 body sections, confirming structural parity.

4. **PRD compliance layer added**: SOC2 (0 to 5), GDPR (1 to 4), and compliance NFRs are the primary enrichment. NFR count grows from 3 to 7.

5. **Risk inventory doubled**: 3 to 7 risks, with R4-R7 sourced from PRD risk analysis.

6. **Business metrics added**: Conversion rate and session duration success criteria are new in Spec+PRD.

**Assessment: PASS** -- PRD enrichment adds compliance and business content. Zero TDD contamination confirmed.
