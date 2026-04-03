# Structural Comparison: anti-instinct-audit.md

**Test 2**: `.dev/test-fixtures/results/test2-spec-modified/anti-instinct-audit.md`
**Test 3**: `.dev/test-fixtures/results/test3-spec-baseline/anti-instinct-audit.md`

---

## Frontmatter Field Comparison

| Field Name | Test 2 | Test 3 | Status |
|---|---|---|---|
| undischarged_obligations | PRESENT | PRESENT | MATCH |
| uncovered_contracts | PRESENT | PRESENT | MATCH |
| fingerprint_coverage | PRESENT | PRESENT | MATCH |
| total_obligations | PRESENT | PRESENT | MATCH |
| total_contracts | PRESENT | PRESENT | MATCH |
| fingerprint_total | PRESENT | PRESENT | MATCH |
| fingerprint_found | PRESENT | PRESENT | MATCH |
| generated | PRESENT | PRESENT | MATCH |
| generator | PRESENT | PRESENT | MATCH |

**Field Count**: Test 2 = 9, Test 3 = 9 -- MATCH

---

## Body Section Header Comparison

| Section Header | Test 2 | Test 3 | Status |
|---|---|---|---|
| ## Anti-Instinct Audit Report | PRESENT | PRESENT | MATCH |
| ### Obligation Scanner | PRESENT | PRESENT | MATCH |
| ### Integration Contract Coverage | PRESENT | PRESENT | MATCH |
| ### Fingerprint Coverage | PRESENT | PRESENT | MATCH |

**Header Count**: Test 2 = 4, Test 3 = 4 -- MATCH

---

## Value Comparison (for context)

| Metric | Test 2 | Test 3 | Notes |
|---|---|---|---|
| fingerprint_coverage | 0.72 | 0.67 | Test 2: PASS (0.72 >= 0.7); Test 3: FAIL (0.67 < 0.7) |
| uncovered_contracts | 3 | 0 | Varies by run |
| total_obligations | 0 | 1 | Varies by run |
| undischarged_obligations | 0 | 0 | Both PASS |
| fingerprint_total | 18 | 18 | MATCH |

---

## Notes

- Both anti-instinct audits FAILed, but for different reasons: Test 2 failed on uncovered_contracts (3 > 0) despite passing fingerprint_coverage (0.72 >= 0.7); Test 3 failed on fingerprint_coverage (0.67 < 0.7) with uncovered_contracts passing (0).
- All 9 frontmatter fields are identical in name between both runs.
- All 4 section headers are identical.
- Value differences (0.72 vs 0.67 fingerprint coverage, 3 vs 0 uncovered contracts) reflect different upstream merged roadmap content. Expected.
- No TDD-specific content found in either version.

---

## Overall Verdict: MATCH

Structural equivalence confirmed. Identical frontmatter schema (9 fields) and identical section structure (4 headers). Both FAILed the anti-instinct gate (Test 2: uncovered_contracts > 0; Test 3: fingerprint_coverage < 0.7). Different failure reasons are expected since the gate checks multiple criteria and upstream roadmap content differs between LLM runs.
