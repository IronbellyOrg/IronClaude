# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | guard_conditions | Cache key generation must include all response-shaping authorization and tenant dimensions. | ADDRESSED | HIGH | Diff C-001/X-001 resolved by merged eligibility and key requirements. |
| INV-002 | interaction_effects | Stale-if-error can conflict with permission revocation or sensitive responses. | ADDRESSED | HIGH | Variant 2 limits stale-if-error to safe endpoints; Variant 3 requires security gating. |
| INV-003 | state_variables | Invalidation must account for both resource mutation state and policy-version state. | ADDRESSED | MEDIUM | Variant 1 includes policy version observability; Variant 2 includes mutation hooks. |
| INV-004 | collection_boundaries | Bulk/list endpoints can contain mixed-resource freshness and authorization boundaries. | ADDRESSED | MEDIUM | Merged requirements require endpoint class policies and tenant/auth key tests. |

## Summary

- **Total findings**: 4
- **ADDRESSED**: 4
- **UNADDRESSED**: 0
  - HIGH: 0
  - MEDIUM: 0
  - LOW: 0
