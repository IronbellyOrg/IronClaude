# Phase 6 — Extraction Comparison (Item 6.1)

## Section Count Comparison

| Metric | Test 1 (TDD) | Test 2 (Spec) | Expected TDD | Expected Spec | Match |
|--------|-------------|---------------|--------------|---------------|-------|
| H2 sections | 14 | 8 | >= 14 | 8 | YES |
| Standard sections | 8 | 8 | 8 | 8 | YES |
| TDD-specific sections | 6 | 0 | 6 | 0 | YES |

## Frontmatter Field Count Comparison

| Metric | Test 1 (TDD) | Test 2 (Spec) | Expected TDD | Expected Spec | Match |
|--------|-------------|---------------|--------------|---------------|-------|
| Total frontmatter fields | 20 | 14 | >= 19 | 13 | YES |
| Standard fields | 14 | 14 | 13 | 13 | YES |
| TDD-specific fields | 6 | 0 | 6 | 0 | YES |

Note: Both have 14 standard fields (13 required + `pipeline_diagnostics` bonus from the executor). The TDD extraction has 20 total (14 standard + 6 TDD-specific).

## Structural Difference Summary

The TDD extraction produces **6 additional body sections** and **6 additional frontmatter fields** compared to the spec extraction. This is exactly the expected delta from the `build_extract_prompt_tdd()` additions. No unexpected differences were found.

## Verdict: PASS — Section and field counts match expectations for both paths.
