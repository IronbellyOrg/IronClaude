# Prompt 4 Refactor Notes

## Date: 2026-03-19

## Change Applied: Promote "Measurable Delta" from REQUIRED to CRITICAL

### What changed

Criterion 7 (MEASURABLE DELTA) was moved from the REQUIRED tier to the CRITICAL tier as new criterion 5. The remaining REQUIRED criteria (A/B COMPARABLE, NO MOCKS) were renumbered to 6 and 7. The BLOCKING GATE clause was updated to include criterion 5, and the forward-context template was updated to reflect the new split (5 CRITICAL, 2 REQUIRED).

Additionally, the criterion text was strengthened with a pre-declared hypothesis requirement: evals must state their expected delta direction BEFORE execution. Post-hoc metric selection (choosing which metric to report after seeing results) is now a FAIL condition.

### Why this was the best improvement

Three improvements were proposed and debated:

1. **Checkpoint eval detection** (add explicit FAIL condition for partial-stage execution) -- ADOPTED in debate but ranked second due to maintenance cost of hardcoded stage lists.

2. **Content fingerprinting / temporal uniqueness** (require non-identical LLM output across consecutive runs) -- REJECTED in debate due to double-execution cost, arbitrary thresholds, and low probability of the adversarial scenario it addresses.

3. **Promote Measurable Delta to CRITICAL** (this change) -- ADOPTED with highest confidence. It closes the timing-only delta escape hatch, which is the most fundamental threat to eval validity: an eval that proves execution happened but not that it mattered is functionally identical to the rejected 168-test approach.

### Risk accepted

A bug in metric extraction code will now BLOCK the entire validation rather than being a fix-later item. This is acceptable because metric extraction IS the eval -- without quality measurement, there is no eval.

### Criteria renumbering

| Old # | New # | Name | Tier |
|-------|-------|------|------|
| 1 | 1 | REAL EXECUTION | CRITICAL |
| 2 | 2 | REAL ARTIFACTS | CRITICAL |
| 3 | 3 | THIRD-PARTY VERIFIABLE | CRITICAL |
| 4 | 4 | ARTIFACT PROVENANCE | CRITICAL |
| 7 | 5 | MEASURABLE DELTA | CRITICAL (promoted) |
| 5 | 6 | A/B COMPARABLE | REQUIRED |
| 6 | 7 | NO MOCKS | REQUIRED |
