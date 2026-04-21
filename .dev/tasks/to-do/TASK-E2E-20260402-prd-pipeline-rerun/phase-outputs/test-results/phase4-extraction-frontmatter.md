# Phase 4.2 — Extraction Frontmatter Verification

**Artifact:** `.dev/test-fixtures/results/test1-tdd-prd/extraction.md`
**Date:** 2026-04-02

## Checks

| # | Check | Expected | Actual | Result |
|---|-------|----------|--------|--------|
| 1 | Frontmatter present | yes | yes (lines 1-22) | PASS |
| 2 | spec_source field | present | `"test-tdd-user-auth.md"` | PASS |
| 3 | generated field | present | `"2026-04-02T12:00:00Z"` | PASS |
| 4 | generator field | present | `"requirements-design-extraction-agent"` | PASS |
| 5 | functional_requirements | present | 5 | PASS |
| 6 | nonfunctional_requirements | present | 9 | PASS |
| 7 | total_requirements | present | 14 | PASS |
| 8 | complexity_score | present | 0.55 | PASS |
| 9 | complexity_class | LOW/MEDIUM/HIGH | `"MEDIUM"` | PASS |
| 10 | domains_detected | present | [backend, security, frontend, testing, devops] | PASS |
| 11 | risks_identified | present | 7 | PASS |
| 12 | dependencies_identified | present | 8 | PASS |
| 13 | success_criteria_count | present | 10 | PASS |
| 14 | extraction_mode | "standard" or "chunked*" | `standard` | PASS |
| 15 | data_models_identified | > 0 | 2 | PASS |
| 16 | api_surfaces_identified | > 0 | 4 | PASS |
| 17 | components_identified (TDD-specific) | present | 9 | PASS |
| 18 | test_artifacts_identified (TDD-specific) | present | 6 | PASS |
| 19 | migration_items_identified (TDD-specific) | present | 15 | PASS |
| 20 | operational_items_identified (TDD-specific) | present | 9 | PASS |
| 21 | pipeline_diagnostics (TDD-specific) | present | elapsed_seconds: 327.2 | PASS |

## Field Count

- **Standard fields (13):** spec_source, generated, generator, functional_requirements, nonfunctional_requirements, total_requirements, complexity_score, complexity_class, domains_detected, risks_identified, dependencies_identified, success_criteria_count, extraction_mode
- **TDD-specific fields (6):** data_models_identified, api_surfaces_identified, components_identified, test_artifacts_identified, migration_items_identified, operational_items_identified
- **Extra field (1):** pipeline_diagnostics (bonus diagnostic field)
- **Total: 20 fields** (19 required + 1 bonus)

## Summary

**PASS** -- All 19 required frontmatter fields present (13 standard + 6 TDD-specific). data_models_identified = 2 (> 0), api_surfaces_identified = 4 (> 0), complexity_class = "MEDIUM" (valid), extraction_mode = "standard" (valid). One bonus field (pipeline_diagnostics) also present.
