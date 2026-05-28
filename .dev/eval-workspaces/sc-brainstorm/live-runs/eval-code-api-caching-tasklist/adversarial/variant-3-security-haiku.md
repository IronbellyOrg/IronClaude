---
schema_version: brainstorm-variant/2.0
variant: 3
agent: security:haiku
focus: security, privacy, compliance, failure modes
case_id: 8
---

# Proposal Variant 3 — Security-Gated API Caching (security:haiku)

## Position
Treat endpoint caching as a security-sensitive data-replication feature. Default posture: deny-by-default. Explicit classification + review before any response body is cached.

## Functional Requirements
- FR1. Classify each candidate endpoint by sensitivity: public, tenant-scoped, user-scoped, confidential, non-cacheable.
- FR2. Security approval required before caching confidential / tenant-scoped / user-scoped responses.
- FR3. All response-shaping authorisation and tenant attributes are included in keys.
- FR4. Forbid caching of secrets, tokens, credentials, payment data, regulated personal data unless explicitly approved + encrypted.
- FR5. Cache entries expire and are purgeable across all replicas.
- FR6. Log cache-policy changes, manual purges, security overrides, stale-if-error usage.

## Non-Functional Requirements
- NFR1. Zero cross-tenant or cross-user cache leakage.
- NFR2. Cache storage obeys existing encryption, retention, and data-residency policies.
- NFR3. Security review must not block low-risk public/reference endpoints when policy proves globally identical content.

## Abuse / Failure Scenarios
- User receives another tenant's cached response (missing tenant/role in key).
- Sensitive response cached beyond retention window.
- Stale authorisation state grants access after permission revocation.
- Cache purge misses a replica during incident response.
- Debug logs expose cache keys containing sensitive identifiers.

## Acceptance Criteria
- Endpoint classification recorded before caching is enabled.
- Tests prove authorisation, tenant, API version, and content-negotiation dimensions vary cache entries.
- Manual purge emits audit event with actor + scope.
- Security can disable caching for any endpoint without a deployment.
- Regulated / secret-bearing responses remain non-cacheable unless explicitly approved.

## Open Questions
- Are cache keys considered sensitive under current logging policy?
- Does the cache backend support encryption + data-residency controls?
- How fast must revocation-sensitive responses be invalidated after permission changes?
