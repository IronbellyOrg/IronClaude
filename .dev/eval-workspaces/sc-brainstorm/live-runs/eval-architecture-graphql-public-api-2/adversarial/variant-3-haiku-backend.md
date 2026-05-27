---
variant: 3
agent_spec: haiku:backend
persona: backend
custom_instruction: "focus on API contracts, data integrity, idempotency, and operational concerns"
generated_for: explore-graphql-for-public-api
---

# Variant 3: Operations-First Public GraphQL API Specification

## 1. Executive Decision

This specification recommends a **public GraphQL API only if the organization treats GraphQL as an operational product, not only a developer-experience layer**. The v1 API should launch as a **single graph** with strict schema governance, authenticated access, persisted operations, query cost controls, idempotent mutations, explicit consistency guarantees, and on-call-ready observability. Federation, subscriptions, and broad schema coverage should wait until there is proven organizational and product need.

The seed brief states that the host SuperClaude repository has no public HTTP API today. This spec therefore treats the API as a **declared-target greenfield public API**, not an implementation plan for the current CLI package. If the target is SuperClaude itself, the API must be a separate service with deployment, persistence, authentication, and operations capabilities that do not exist in the current package. If the target is another product, these requirements remain stack-agnostic.

The distinctive stance is conservative: **GraphQL is acceptable only when every caller-visible behavior is contractually bounded**. Public GraphQL without allowlisted operations, retry-safe mutations, pagination rules, error semantics, timeout budgets, and schema governance should be rejected in favor of REST until the organization can run it safely.

## 2. Goals, Non-Goals, and Assumptions

| Area | Position |
|---|---|
| Primary goal | Reduce over-fetching and under-fetching while preserving stable public contracts. |
| Public contract | The schema is the contract; governance tooling is launch-blocking. |
| Security posture | Authenticated by default, deny-by-default authorization, no broad production introspection. |
| Operational posture | Every operation is costed, timed, traced, logged, rate-limited, and attributable to a client. |
| Data integrity | Mutations are idempotent, consistency semantics are documented, and conflicts are explicit. |
| Non-goal | This spec does not choose a concrete server framework or implementation language. |
| REST stance | Existing REST remains supported until GraphQL proves parity and reliability. |
| Consumer assumption | Both partner integrations and third-party developers are expected. |
| Team assumption | One API platform team owns v1; domain-team federation is a later possibility. |
| Deprecation assumption | Public consumers require long windows: 12 months for most removals, 18 months for mutation and enum removals. |

## 3. Topology Decision: Single Graph First, Federation Later

### Decision

Launch v1 as a **single public graph** owned by one API platform team. Do not launch a federated supergraph unless there are already multiple independently deploying domain teams with mature schema ownership practices.

### Justification

Federation is valuable when organizational boundaries are the scaling problem. It is also an operational multiplier: composition checks, subgraph versioning, entity ownership, distributed tracing, cross-subgraph authorization, gateway reliability, and partial failure semantics all become part of the public contract. For a greenfield public API with no existing HTTP surface in the scanned host repository, federation adds complexity before there is enough traffic, schema breadth, or team topology to justify it.

A single graph gives v1 one schema contract, one release train, one authorization model, one rate-limit envelope, simpler query cost estimation, and clearer incident ownership. This matters more than theoretical scale during the first public launch.

### Federation Trigger

Move to a federated supergraph only when at least three conditions are true:

1. Three or more domain teams independently own schema areas and deploy weekly or faster.
2. The graph exceeds roughly 250 types or 500 fields and schema review throughput becomes a bottleneck.
3. At least two backend services already expose stable internal GraphQL subgraphs.
4. Cross-domain changes delay releases by more than two weeks per quarter.
5. Public traffic exceeds 2,000 requests per second sustained and gateway isolation materially improves reliability.

If federation is adopted, Apollo Federation or WunderGraph Cosmo-class federation is preferred. Schema stitching is treated as legacy integration glue, not the public architecture target. Even in a single graph, public types must represent stable business capabilities rather than internal tables, REST DTOs, or service boundaries.

## 4. Schema Contract and Evolution Policy

The schema is the public contract. Every public field, argument, input object, enum value, mutation, directive, and error type must be reviewed before release. Launch requires a schema registry, version history, automated breaking-change detection, persisted-operation registry, generated documentation, ownership metadata, and contract tests using representative partner operations.

### Breaking-Change Definition

A change is breaking if a previously valid client operation can fail validation, return incompatible data, or observe materially different authorization behavior without opt-in. Breaking changes include removing or renaming schema elements, changing field or argument types, tightening nullability, adding required inputs, changing enum semantics, invalidating active cursors inside the cursor TTL, changing error category names, or reducing public limits without notice except for abuse response.

Non-breaking changes include adding nullable fields, adding optional arguments with defaults, adding new types reachable only through new fields, adding enum values when clients are told to handle unknown values defensively, and deprecating fields without removing them.

### Deprecation Windows

| Change Type | Minimum Window | Requirement |
|---|---:|---|
| Field removal after deprecation | 12 months | Replacement path required. |
| Mutation removal after deprecation | 18 months | Longer window because workflows depend on mutations. |
| Enum value removal | 18 months | Prefer never removing; add replacements. |
| Input field removal | 12 months | Field should be ignored or tolerated during window. |
| Beta field removal | 30 days | Only if clearly labeled beta and excluded from GA SDKs. |
| Security-driven removal | 0-30 days | Requires incident review and direct partner notification where possible. |

Deprecated fields must include a reason and earliest removal date, for example `@deprecated(reason: "Use resourceV2. Removal no earlier than 2027-06-01.")`. Documentation must show deprecations prominently. Registered app owners must be notified when their persisted operations use deprecated fields.

The graph is **versionless at the endpoint level**: `/graphql` remains stable. A `/v2/graphql` endpoint is a last resort for incompatible product shifts, not routine evolution.

## 5. Authentication and Authorization

All production requests must be authenticated unless a field is explicitly classified as public metadata. Production introspection is disabled for anonymous and general API clients; schema access is provided through the docs site, downloadable SDL, and sandbox environments.

| Mode | Use Case | Requirement |
|---|---|---|
| OAuth 2.1 Authorization Code + PKCE | User-delegated apps | Token includes subject, scopes, audience, and expiry. |
| OAuth 2.1 Client Credentials | Server-to-server integrations | Client identity maps to organization, plan, and scopes. |
| Scoped API key with HMAC signing | Simpler partner integrations | Rotatable, scoped, auditable, and optionally IP/origin-bound. |
| mTLS | High-trust enterprise partners | Additional control, not a replacement for OAuth scopes. |

Access tokens should default to 15-minute TTLs. API keys must support overlapping rotation with at least two active keys per application.

Authorization is enforced at three layers: operation, object, and field. Operation policy decides whether a client may execute the operation category. Object policy decides whether the principal may access the resource instance. Field policy protects sensitive fields inside otherwise visible objects. The default is deny-by-default. Each protected schema field must have scope and data-classification metadata or equivalent policy configuration.

Resolver context must include client ID, user ID when present, organization ID, scopes, partner tier, request ID, and correlation/trace ID. Mutations require write scopes. Administrative mutations require both admin scopes and organization-role checks. Authorization failures for top-level resources should be explicit errors; nullable sensitive subfields may return null only when that behavior is documented.

## 6. Abuse-Protection Envelope

Public GraphQL treats query shape as an attack surface. The default posture is **persisted operations required for production public clients**, with raw query documents allowed only in sandbox, internal tooling, or short-lived approved debug sessions.

| Control | Default |
|---|---:|
| Max query depth | 10 |
| Max query complexity | 1,000 cost units |
| Max selection set fields | 250 unique fields |
| Max aliases | 25 |
| Max query document size | 64 KB |
| Max variables payload | 32 KB |
| Default query timeout | 10 seconds |
| Maximum approved query timeout | 30 seconds |
| Default mutation timeout | 30 seconds |
| Maximum approved mutation timeout | 60 seconds |
| Default page size | 25 edges |
| Maximum page size | 100 edges |

Cost calculation must account for pagination arguments and resolver expense. A connection requested with `first: 100` costs more than one requested with `first: 10`; a field that calls an expensive upstream costs more than a scalar field.

### Persisted Operations

Production clients submit operations during app registration or CI integration. The registry validates schema compatibility, required scopes, complexity, depth, and deprecated-field usage, then assigns an operation ID and SHA-256 hash. Runtime accepts only `{ operationId, variables }` for production clients. This enables stable metrics, CDN cache keys, precomputed cost, auditability, and fast containment of abusive operations.

### Rate Limiting

Rate limits apply by client app, user, organization, IP/CIDR, operation ID, and mutation category.

| Tier | Query Limit | Mutation Limit | Burst |
|---|---:|---:|---:|
| Sandbox anonymous | 30/min/IP | 0 | 10 |
| Developer free | 300/min/app | 30/min/app | 100 |
| Partner standard | 3,000/min/app | 300/min/app | 500 |
| Enterprise | Contractual | Contractual | Contractual |

Responses must include `Retry-After`, `RateLimit-Limit`, `RateLimit-Remaining`, and `RateLimit-Reset`. GraphQL errors must include `category: RATE_LIMITED` and `retryable: true`.

## 7. Mutation Idempotency and Data Integrity

All public mutations that create, update, delete, enqueue, bill, send, invite, publish, or otherwise cause side effects must support retry-safe execution through an explicit idempotency key. Every side-effecting mutation input embeds an idempotency object conceptually equivalent to:

```graphql
input IdempotencyInput {
  key: ID!
  clientRequestId: String
}
```

The key is scoped by authenticated client ID, principal, mutation name, and target tenant. Reusing the same key with the same semantic request returns the original result. Reusing the same key with a different payload returns an idempotency conflict. Default server-side deduplication TTL is **24 hours**. For billing, irreversible external sends, or contractual partner workflows, TTL is **7 days**. The idempotency store persists request hash, response envelope, mutation status, creation time, and expiry time.

If a mutation is still in progress and the same key is retried, the API returns the completed result if available or a retryable `IDEMPOTENCY_IN_PROGRESS` error with `Retry-After`. The server must not execute duplicate side effects.

### Consistency Guarantees

| API Area | Guarantee | Caller Contract |
|---|---|---|
| Mutation acknowledgment | Strict for accepted write transaction | Success means primary write committed or durable job enqueued. |
| Immediate read after write | Read-your-write within 2 seconds for same principal | If unavailable, response includes consistency warning. |
| Aggregates/search/reporting | Eventual, target 60 seconds | Fields document `eventualConsistencyWindowSeconds`. |
| Webhook/job status | Eventual, target 5 minutes | Exposed as state machine. |
| Cross-region reads | Eventual by default | Response includes region and observed version where relevant. |

Objects that can be concurrently modified expose `version` or `updatedAt`. Update mutations support optional `expectedVersion`. Version mismatch returns `CONFLICT` and is not retryable without caller action. Mutations touching multiple systems must either commit atomically, create a durable asynchronous job, or expose partial-failure state explicitly. Public mutations must not silently complete partial work while returning success.

## 8. Error Contract

The API uses **typed mutation payload errors for business failures** and standard `errors[].extensions` for validation, auth, rate-limit, abuse, upstream, and unexpected failures. Mutation payloads should include nullable success data, a non-null error list, and request ID. Domain errors should be represented by unions or interfaces such as `ValidationError`, `ConflictError`, `PermissionError`, and `IdempotencyError`.

Top-level error extensions must include:

| Field | Requirement |
|---|---|
| `code` | Stable machine-readable code such as `QUERY_COMPLEXITY_EXCEEDED`. |
| `category` | `AUTHENTICATION`, `AUTHORIZATION`, `VALIDATION`, `CONFLICT`, `RATE_LIMITED`, `ABUSE_PROTECTION`, `UPSTREAM`, or `INTERNAL`. |
| `retryable` | Boolean, required for every public error. |
| `retryAfterSeconds` | Required when retryable due to throttling or temporary failure. |
| `requestId` | Required for support and trace lookup. |
| `operationId` | Required when using persisted operations. |
| `fieldPath` | Included when the error maps to a specific field. |
| `documentationUrl` | Included for stable public errors. |

Retryability is part of the contract. Authentication, authorization, validation, and conflict errors are not retryable without caller action. Rate limits and temporary upstream failures are retryable with backoff. Mutations must be retried with the same idempotency key. The API must never expose stack traces, SQL errors, internal service names, or raw exception messages.

## 9. Pagination and List Semantics

All public list fields use **Relay-style cursor pagination** unless an exception is explicitly approved. Unbounded lists are prohibited. Connections accept `first` and `after` for forward pagination, may accept `last` and `before` only when reverse pagination is efficient, default to `first: 25`, and cap `first` at 100.

Cursors are opaque strings. Clients must not parse or construct them. Cursors are stable for at least 24 hours for the same filter and sort request. Cursor invalidation returns `CURSOR_EXPIRED` or `CURSOR_INVALID`. Every connection must define deterministic ordering. Supported sort fields must be indexed and documented. Arbitrary filter expressions are not allowed in v1. `totalCount` is exposed only when cheap and accurate; expensive counts should be omitted or represented as eventually consistent aggregate fields.

## 10. Cache Semantics

Only persisted, authenticated query operations with no viewer-specific sensitive data are eligible for shared CDN caching. Cache keys include operation ID, variables hash, authorization partition, locale, and relevant feature flags.

| Operation Class | Cache-Control |
|---|---|
| Public reference data | `public, max-age=300, stale-while-revalidate=60` |
| Organization-scoped reads | `private, max-age=60` or tenant-partitioned CDN cache |
| User-specific reads | `private, no-store` unless explicitly safe |
| Mutations | `no-store` |
| Error responses | `no-store`, except controlled edge handling for rate-limit metadata |

Invalidation triggers include mutations affecting cached objects, administrative data changes, schema deployment, persisted-operation metadata changes, and authorization or tenant membership changes. Resolver caches may be used for read-heavy reference data only when they respect authorization, tenant isolation, and consistency labels. Cache hit rate, stale serve rate, and invalidation failures are operational metrics.

## 11. Subscriptions Decision

Subscriptions are **not included in v1**. Public subscriptions require persistent connection management, broker operations, fan-out controls, replay semantics, token refresh, topic authorization, mobile network behavior, and backpressure. The seed problem is public API exploration, not real-time product differentiation.

The v2 trigger is a validated product requirement where polling or webhooks are insufficient, such as collaborative state, live telemetry, or user-facing notifications with latency SLO under five seconds. If v2 ships subscriptions, the broker must be named and operated as part of the API platform. Kafka is preferred for durable event streams; NATS is preferred for low-latency ephemeral fan-out. Until then, v1 should support webhooks for asynchronous notifications.

## 12. Operational and Observability Surface

### SLOs

| Measure | GA Target |
|---|---:|
| Monthly availability for `/graphql` | 99.9% |
| Query p95 latency for persisted reads | < 500 ms |
| Query p99 latency | < 2,000 ms |
| Mutation p95 latency for synchronous writes | < 1,500 ms |
| Mutation p99 latency | < 5,000 ms |
| Error rate excluding caller validation/auth failures | < 0.5% |
| Persisted-operation registry availability | 99.95% |

### Telemetry

Every request emits structured logs, metrics, and traces with request ID, trace ID, client ID, tenant ID, user hash where applicable, operation name, operation ID, complexity, depth, field count, alias count, resolver timings, response category, error codes, rate-limit decision, idempotency key hash for mutations, cache status, upstream calls, and retry counts. Raw query text is not logged in production except in controlled debug sampling with PII scrubbing.

### Alerts and Runbooks

Page the API on-call for SLO burn rate, p99 latency above 5 seconds for 10 minutes, internal error rate above 2% for 5 minutes, idempotency store unavailability, persisted-operation registry outage above 2 minutes, authorization policy failure rate above 0.1%, query-complexity rejection spikes above 5x baseline, dependency saturation causing error-budget burn, or cache invalidation backlog older than 5 minutes for strongly labeled data.

Runbooks must cover high latency, error-rate spikes, abuse events, idempotency store incidents, authorization incidents, schema rollout failures, and cache invalidation failures. The idempotency runbook must fail closed for high-risk mutations, allow read-only traffic, restore the store, and run reconciliation. The authorization runbook must disable affected operations or fields, purge caches, rotate policy bundles, and audit exposure.

## 13. REST Coexistence and Deprecation Strategy

If REST exists, GraphQL is additive. Existing REST clients are not forced to migrate until GraphQL proves reliability, parity, and economic value. REST and GraphQL must share authorization, audit logging, business validation, idempotency behavior, and conflict semantics. GraphQL may wrap REST internally at first, but the public schema must not mechanically mirror endpoint paths.

| Phase | Duration | Exit Criteria |
|---|---:|---|
| Private alpha | 1-2 months | Internal consumers validate schema and operational controls. |
| Partner beta | 3 months | Selected partners run production-like traffic with no P0/P1 contract issues. |
| Public GA additive | 6 months | SLOs met, SDKs stable, support volume manageable. |
| REST deprecation notice | 12-24 months | Only for endpoints with GraphQL parity and migration tooling. |
| REST removal | After notice | No contractual blockers and usage below agreed threshold. |

If no REST API exists, GraphQL can be first public API only if the organization still provides REST-like affordances where useful: webhooks, simple examples for common workflows, SDKs, and stable HTTP behavior for authentication and rate limiting.

## 14. MVP Scope vs. Full Vision

### MVP Scope

The smallest viable launch includes one `/graphql` endpoint, a single graph, schema registry, CI schema checks, persisted operations, OAuth/client-credential or API-key auth, query controls, Relay pagination, typed mutation errors, standard error extensions, idempotency keys, operation-level dashboards, documentation, sandbox environment, production introspection disabled for ordinary clients, and no subscriptions.

The MVP should expose a narrow domain: roughly 5-10 core queries and 3-5 mutations. It should prove the operational model before expanding schema breadth.

### Full Vision

The full vision may add federation, partner-specific operation registries, generated SDKs for TypeScript/Python/Go/Java, webhook and asynchronous job management APIs, field-level privacy classifications, advanced deprecation analytics, optional subscriptions, regional routing, enterprise strong-read options, and a developer portal for app registration, key rotation, operation submission, and usage analytics.

## 15. REST Alternative Comparison

| Axis | GraphQL | REST |
|---|---|---|
| Developer experience | Strong for flexible clients, typed schema, fewer round trips. | Strong for simple resource workflows and familiar HTTP semantics. |
| Operational complexity | Higher: cost analysis, resolver tracing, N+1 prevention, persisted operations. | Lower: endpoint-level limits, simpler caching, simpler logs. |
| Caching | More complex: operation and variable-aware partitioning. | Easier: URL-based HTTP caching. |
| Contract evolution | Additive schema evolution can avoid endpoint versions but requires discipline. | Versioned endpoints are explicit but can proliferate. |
| Abuse resistance | Must control query shape; unsafe if open-ended. | Easier to bound per endpoint. |
| Data fetching | Excellent for varied client data shapes. | Can over-fetch or under-fetch unless many tailored endpoints exist. |

GraphQL wins when clients have varied data-shape needs and the organization can invest in governance and operations. REST wins when workflows are simple, cacheability dominates, consumers prefer resource semantics, or the team cannot yet operate GraphQL safely.

## 16. Risks That Justify Rejecting GraphQL Entirely

Reject or postpone GraphQL if the organization will not enforce persisted operations; cannot staff schema governance and operation registry ownership; mainly needs simple CRUD; expects mostly anonymous high-volume traffic; lacks query-level observability and N+1 detection; cannot enforce field/object authorization; cannot honor 12-18 month deprecation windows; cannot make mutations idempotent; cannot state consistency guarantees; or is choosing GraphQL primarily for market signaling.

In those cases, a well-designed REST API with OpenAPI, SDK generation, cursor pagination, idempotency keys, webhooks, and targeted composite endpoints is safer and cheaper.

## 17. Final Recommendation

Proceed with GraphQL only as a controlled, single-graph MVP with strict production guardrails. The initial launch should prioritize operational correctness over schema breadth: persisted operations, idempotent mutations, bounded pagination, explicit consistency, typed errors, cache rules, and on-call-ready observability are the product contract. Federation, subscriptions, and broad domain coverage should wait until demand and organizational maturity justify their operational cost.
