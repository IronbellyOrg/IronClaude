# Structural Comparison: extraction.md

**Test 2**: `.dev/test-fixtures/results/test2-spec-modified/extraction.md`
**Test 3**: `.dev/test-fixtures/results/test3-spec-baseline/extraction.md`

---

## Frontmatter Field Comparison

| Field Name | Test 2 | Test 3 | Status |
|---|---|---|---|
| spec_source | PRESENT | PRESENT | MATCH |
| generated | PRESENT | PRESENT | MATCH |
| generator | PRESENT | PRESENT | MATCH |
| functional_requirements | PRESENT | PRESENT | MATCH |
| nonfunctional_requirements | PRESENT | PRESENT | MATCH |
| total_requirements | PRESENT | PRESENT | MATCH |
| complexity_score | PRESENT | PRESENT | MATCH |
| complexity_class | PRESENT | PRESENT | MATCH |
| domains_detected | PRESENT | PRESENT | MATCH |
| risks_identified | PRESENT | PRESENT | MATCH |
| dependencies_identified | PRESENT | PRESENT | MATCH |
| success_criteria_count | PRESENT | PRESENT | MATCH |
| extraction_mode | PRESENT | PRESENT | MATCH |
| pipeline_diagnostics | PRESENT | PRESENT | MATCH |

**Field Count**: Test 2 = 14, Test 3 = 14 -- MATCH

---

## Body Section Header Comparison

| Section Header | Test 2 | Test 3 | Status |
|---|---|---|---|
| ## Functional Requirements | PRESENT | PRESENT | MATCH |
| ### FR-AUTH.1: User Login | PRESENT | PRESENT | MATCH |
| ### FR-AUTH.2: User Registration | PRESENT | PRESENT | MATCH |
| ### FR-AUTH.3: Token Refresh | PRESENT | PRESENT | MATCH |
| ### FR-AUTH.4: Profile Retrieval | PRESENT | PRESENT | MATCH |
| ### FR-AUTH.5: Password Reset | PRESENT | PRESENT | MATCH |
| ## Non-Functional Requirements | PRESENT | PRESENT | MATCH |
| ### NFR-AUTH.1 (Latency/Response Time) | PRESENT | PRESENT | MATCH (minor title variation) |
| ### NFR-AUTH.2: Service Availability | PRESENT | PRESENT | MATCH |
| ### NFR-AUTH.3: Password Hashing Security | PRESENT | PRESENT | MATCH |
| ## Complexity Assessment | PRESENT | PRESENT | MATCH |
| ## Architectural Constraints | PRESENT | PRESENT | MATCH |
| ## Risk Inventory | PRESENT | PRESENT | MATCH |
| ## Dependency Inventory | PRESENT | PRESENT | MATCH |
| ### External Libraries | ABSENT | PRESENT | DIFF (Test 3 subsections) |
| ### External Services | ABSENT | PRESENT | DIFF (Test 3 subsections) |
| ### Internal Dependencies | ABSENT | PRESENT | DIFF (Test 3 subsections) |
| ### Infrastructure Assumptions | ABSENT | PRESENT | DIFF (Test 3 subsections) |
| ## Success Criteria | PRESENT | PRESENT | MATCH |
| ## Open Questions | PRESENT | PRESENT | MATCH |

**Header Count**: Test 2 = 16, Test 3 = 20 -- DIFF (+4 in Test 3)

---

## Notes

- Test 3 breaks the Dependency Inventory into 4 subsections (External Libraries, External Services, Internal Dependencies, Infrastructure Assumptions) while Test 2 uses a single flat section. This is expected LLM non-determinism in section organization -- the same content is present in both.
- NFR-AUTH.1 title differs slightly: "Authentication Endpoint Latency" (Test 2) vs "Authentication Endpoint Response Time" (Test 3). Expected LLM variation.
- All 14 frontmatter fields are identical between runs.
- No TDD-specific content (Data Models, API Specifications, etc.) found in either version.

---

## Overall Verdict: MATCH

Structural equivalence confirmed. The +4 header difference is due to Test 3 using subsections under Dependency Inventory -- a cosmetic organizational choice, not a structural schema difference. All core sections and all frontmatter fields are present in both.
