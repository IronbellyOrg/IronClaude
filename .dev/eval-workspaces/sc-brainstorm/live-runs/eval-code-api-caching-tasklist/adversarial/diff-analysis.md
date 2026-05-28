# Diff Analysis: API Endpoint Caching Requirements

## Metadata

- Generated: 2026-05-25T00:00:00Z
- Variants compared: 3
- Total differences found: 10
- Categories: structural (2), content (4), contradictions (1), unique (2), shared assumptions (1)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Primary organization | Policy registry first | Middleware/invalidation first | Security classification first | Medium |
| S-002 | Testing placement | Acceptance criteria only | Dedicated testing section | Security acceptance tests | Low |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Variant 3 Approach | Severity |
|---|---|---|---|---|---|
| C-001 | Eligibility model | Opt-in policy registry | Approved read-through endpoints | Deny-by-default sensitivity classification | High |
| C-002 | Invalidation | TTL plus event-driven invalidation | Mutation hooks and purge scopes | Purge across replicas and revocation-sensitive invalidation | High |
| C-003 | Resilience | Origin fallback on cache failures | Stampede protection and stale-if-error | Security-gated stale behavior | Medium |
| C-004 | Observability | Endpoint/cohort/policy version metrics | Detailed cache and fallback metrics | Audit logs for policy and purge actions | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact |
|---|---|---|---|---|---|
| X-001 | Default posture | Cache idempotent reads by default if policy exists | Approved GET/list/detail endpoints | Deny-by-default until classification and review | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | Variant 2 | Single-flight/per-key locking for stampede protection | High |
| U-002 | Variant 3 | Sensitivity classification and data-residency/encryption requirements | High |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | The target system can associate endpoints with policy metadata before serving requests. | All variants depend on endpoint-level policy decisions. | Without this, cache behavior becomes scattered and unreviewable. | UNSTATED promoted |

## Summary

- Highest severity items: C-001, C-002
- Debate should resolve default eligibility posture, invalidation strictness, and whether stale-if-error can be included in first release.
