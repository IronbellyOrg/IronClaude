# Gate Compatibility Review

## spec_source gates (5 gates)
All 5 require `spec_source` as a frontmatter field name:
- EXTRACT_GATE: `required_frontmatter_fields` includes `spec_source`
- GENERATE_A_GATE: `required_frontmatter_fields=["spec_source", "complexity_score", "primary_persona"]`
- GENERATE_B_GATE: same as GENERATE_A_GATE
- MERGE_GATE: `required_frontmatter_fields=["spec_source", "complexity_score", "adversarial"]`
- TEST_STRATEGY_GATE: `required_frontmatter_fields` includes `spec_source`

**Verdict:** All 5 gates will PASS when `build_extract_prompt_tdd()` instructs Claude to emit `spec_source: <tdd_filename>`. No gate code changes needed.

## DEVIATION_ANALYSIS_GATE
**Pre-existing bug (B-1):** Required field `ambiguous_count` (in `required_frontmatter_fields`) vs semantic check `_no_ambiguous_deviations` reads `ambiguous_deviations` (via `fm.get("ambiguous_deviations")`). Field name mismatch means the gate can pass with `ambiguous_count` present but `ambiguous_deviations` absent.

**TDD compatibility:** NOT compatible. `routing_update_spec` field is spec-specific. `DEV-\d+` routing ID pattern assumes spec-deviation taxonomy. Redesign deferred to separate future work.

## ANTI_INSTINCT_GATE
Semantic checks (`_no_undischarged_obligations`, `_integration_contracts_covered`, `_fingerprint_coverage_check`) are all format-agnostic pure Python. They read content text, not format-specific fields. No changes needed.

**TDD performance hypothesis (I-5):** TDD inputs likely produce MORE fingerprint identifiers (TypeScript interfaces, component names) than specs, potentially improving `fingerprint_coverage` ratio. Unverified — needs empirical testing.
