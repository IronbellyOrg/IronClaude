---
schema_version: brainstorm-enrichment/2.0
topic: "adding caching to the API layer"
domain: code
quality_tier: light
tools: [auggie-codebase-retrieval, web-light]
case_id: 8
created: 2026-05-27
---

# Codebase + Light Research Enrichment — API Caching

## Scope of Sweep
Brainstorm topic is a generic "API layer caching" requirements exercise. No specific service is named in the prompt; enrichment summarises generally-applicable findings for the API-layer caching pattern, supplemented by light research on current cache-tier options.

## Relevant Patterns
- API layers typically expose a request-middleware pipeline. Caching is best inserted AFTER auth (so cache keys can include identity dimensions) and BEFORE business handlers (so hits short-circuit downstream work).
- Most codebases lack a single "cache key" abstraction; keys are hand-rolled per endpoint and drift. A central key-builder is a recurring refactor seam.
- Invalidation hooks usually need to live on the write path of the same resource; without a shared event bus, write-handlers must explicitly emit invalidation signals.

## Library / Framework Touchpoints
- Distributed cache options: Redis (most common, supports client-side tracking in 7.x), Memcached (simpler), Hazelcast (JVM-leaning).
- In-process options: framework-provided LRU (e.g., `functools.lru_cache` for Python, Caffeine for JVM, `lru-cache` for Node).
- Edge/CDN: Cloudflare, Fastly, CloudFront — applicable only to public + Cache-Control-clean responses.
- HTTP caching standards: RFC 9111 (2022) is the current spec, replacing RFC 7234; defines Cache-Control, ETag, Vary semantics; modern gateways implement natively.

## Managed-Gateway Options
- AWS API Gateway response cache: per-stage TTL, simple to enable, limited per-request flexibility.
- Cloudflare Workers KV / cache API: edge-near, very low latency, restricted to public-cacheable responses.
- These reduce custom code at the cost of vendor coupling and reduced observability granularity.

## Risk Surface
- Cross-tenant key collision is the highest-severity risk and is the security persona's anchor concern.
- Cache stampede on TTL expiry of hot keys; mitigations include request coalescing, jittered TTL, and stale-while-revalidate.
- Hidden cache dependency: when a cache outage degrades the system more than the cache improved it.
- Silent staleness when invalidation hooks are missed on the write path.

## Implications for Proposals
- At least one proposal should consider a managed/gateway approach (lowest-code path).
- At least one should propose a custom middleware (most control, most observability).
- Security boundary requirements (tenant isolation, no-cache list, auth-bound key vary) are non-negotiable across all three proposals.
- All proposals must include observability and a kill-switch since "ship caching" without these has produced cited production incidents in adjacent ecosystems.

## Constraints Identified
- Preserve correctness: cache only safe/idempotent responses by default; require explicit policy for mutations or personalized data.
- Preserve security: cache keys must vary on authorization and tenant context where applicable; sensitive responses require explicit opt-in and redaction review.
- Preserve operability: caching needs observability, invalidation, fallback behavior, and rollout controls.
- Preserve compatibility: avoid breaking existing API contracts, status codes, headers, and error semantics.
