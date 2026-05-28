---
variant: 2
agent_spec: sonnet:analyzer
persona: analyzer
custom_instruction: "focus on root-cause analysis and evidence-based reasoning for architecture"
generated_for: explore-graphql-for-public-api
---

# Public GraphQL API Specification: Root-Cause-Driven Architecture

## 1. Executive Position

This specification takes an evidence-first stance: GraphQL is the correct choice for a public API **only when the organization can name, with specificity, the failure mode in the current REST (or absent) surface that GraphQL uniquely prevents**. Where that failure mode cannot be articulated, REST with OpenAPI is the safer, cheaper, and more operationally predictable default.

The seed brief identifies symptoms -- over-fetching, under-fetching, version proliferation, DX differentiation -- but does not establish that these symptoms have caused measurable harm. Before this organization commits to GraphQL, it must distinguish between **symptoms** (observable complaints) and **root causes** (the structural deficiency that produces them):

| Symptom | Plausible Root Cause | Does GraphQL Address the Root Cause? |
|---------|---------------------|--------------------------------------|
| Over-fetching | Monolithic REST endpoints returning fixed projections | Yes -- field-level selection eliminates fixed projections |
| Under-fetching | Endpoint granularity mismatched to client needs | Yes -- nested queries collapse multiple round-trips |
| Version proliferation | Breaking-change policy absent, not REST-specific | Partially -- schema evolution discipline applies to both |
| DX differentiation | Absent docs, no playground, no SDK generation | No -- DX tooling is orthogonal to query language choice |

If the root cause of "version proliferation" is actually "we have no breaking-change policy," adopting GraphQL does not fix it -- the same organizational failure will produce schema bloat and zombie fields instead of `/v3` URLs. This specification proceeds assuming the organization has validated that at least two of the first three root causes (over-fetching, under-fetching, version proliferation from fixed projections) are real and quantified.

**If that validation has not occurred, the specification's recommendation is: do not adopt GraphQL. Stop here. Instrument the existing API, measure actual payload waste and round-trip counts, and return with evidence.**

---

## 2. Topology: Single-Graph vs. Federated Supergraph

### Decision: Monolithic single graph for MVP, federation as a migration target, not a starting point.

### Evidence

The 2026 landscape presents two viable topologies:

- **Monolithic single graph**: One schema, one server, one team owns the full surface area. Production-proven for Shopify, GitHub, and most sub-10-team API platforms.
- **Federated supergraph**: Apollo Federation v2 or WunderGraph Cosmo, multiple subgraphs composed by a router. Dominant at scale (multiple backend teams, service-boundary alignment).

The codebase scan confirms this project has **zero existing API surface** -- no HTTP server, no REST endpoints, no microservice boundaries. Federation solves a problem (schema ownership across team boundaries) that does not yet exist.

### Failure-Mode Analysis

| Choice | Failure Mode Prevented | Failure Mode Introduced |
|--------|----------------------|------------------------|
| Monolithic graph | Premature distribution complexity; router operational burden before it earns its cost | Schema becomes a coordination bottleneck once >2 teams contribute; refactor to federation is non-trivial |
| Federated supergraph | Schema ownership conflicts across teams | Operational overhead (router, subgraph health, distributed tracing) from day one with no team-boundary justification; 3-5x infrastructure complexity |

### Premortem (18-month horizon)

**Most likely failure for monolithic**: The schema grows to 80+ types, two or three teams begin stepping on each other's field naming conventions, and schema review becomes a serialization point. The telltale sign is PR review latency exceeding 2 days on schema changes.

**Most likely failure for federation**: The router introduces a latency regression that takes 3 weeks to diagnose because the team lacks subgraph-level distributed tracing. The telltale sign is p99 latency spikes that don't correlate with any single subgraph's metrics.

### Migration Trigger

Adopt federation when **both** conditions are true:
1. Two or more backend teams are contributing fields to the graph.
2. Schema review PR latency exceeds 48 hours on average over a 4-week window.

Do not adopt federation based on projected team growth. Adopt it on demonstrated coordination pain.

---

## 3. Schema Evolution Policy

### Decision: Additive-only with enforced deprecation windows, schema governance tooling as a launch requirement.

### Root-Cause Framing

The root cause of "version proliferation" is not REST vs. GraphQL -- it is the absence of a **governed contract-change process**. A GraphQL schema without evolution discipline is strictly worse than versioned REST, because consumers build tighter couplings to specific field shapes and the blast radius of an uncontrolled removal is larger.

### Policy Requirements

| Aspect | Requirement | Enforcement |
|--------|-------------|-------------|
| Additive changes | New fields, new types, new arguments -- always allowed without review beyond naming conventions | CI lint check (GraphQL Inspector or Apollo Studio schema diff) |
| Field deprecation | `@deprecated(reason: "...")` with a removal-date annotation in the reason string | Mandatory in PR template; CI rejects `@deprecated` without a date |
| Deprecation window | 6 months minimum for public fields; 12 months for fields used by named partner integrations | Tracked in a schema-registry metadata store; automated alerts at T-30 and T-7 days |
| Breaking changes | Removal of a field, type, or argument before its deprecation window expires; changing a field's type; renaming | **Treated as an incident.** Requires post-mortem, consumer impact analysis, and VP-level sign-off |
| Schema governance tooling | Apollo Studio schema checks (or GraphQL Inspector in CI) are **required before launch**, not after | CI pipeline blocks merge on schema-breaking diff |

### Failure-Mode Analysis

| Policy Choice | Failure Mode Prevented | Failure Mode Introduced |
|---------------|----------------------|------------------------|
| 6-month deprecation window | Consumers break without warning; trust erosion | Schema accumulates deprecated fields; resolver maintenance burden grows |
| Governance tooling in CI | Breaking changes ship silently | Schema review adds latency to every PR touching the graph; teams may circumvent by pushing logic to resolvers instead |

### Premortem (18-month horizon)

**Most likely failure**: The organization treats deprecation as "we added the annotation" but never actually removes deprecated fields. After 18 months, 30% of the schema is deprecated-but-present, and resolver code is littered with conditional branches. The telltale sign is deprecated-field count exceeding 15% of total fields.

### Discipline Requirement

Every quarter, run a "deprecation hygiene" review. Any field deprecated for longer than its window that has zero recorded usage in the trailing 30 days must be removed in the next sprint. This is not optional -- it is the only mechanism that prevents schema rot.

---

## 4. Authentication and Authorization Model

### Decision Branch: This is the single largest open question. The answer depends on consumer profile, which the seed brief does not specify.

### Decision Tree

| Consumer Profile | Auth Model | Rationale |
|-----------------|------------|-----------|
| Partner integrations (small N, deep contracts) | mTLS + scoped API keys | High-trust, low-volume, contractual relationship; mTLS provides mutual identity verification |
| Third-party developers (large N, shallow contracts) | OAuth 2.0 with PKCE + API keys for server-to-server | Standard public-API pattern; OAuth for user-delegated access, API keys for machine-to-machine |
| Both | OAuth 2.0 + API keys + optional mTLS tier for premium partners | Tiered auth; do not force mTLS on low-trust consumers |

### Minimum Viable Auth

Regardless of consumer profile, the following are non-negotiable for a public GraphQL API:

1. **Every request must authenticate.** No anonymous access to the graph. Anonymous access is the #1 enabler of abuse in public GraphQL APIs.
2. **Auth is enforced at the gateway/router layer**, not inside resolvers. Resolver-level auth checks are fragile -- a single missed resolver leaks data. The gateway must validate tokens/keys before the query reaches the execution engine.
3. **Field-level authorization is a resolver concern** -- but only for fine-grained access control (e.g., "this user can see this field"). Coarse-grained access ("is this request authenticated?") is the gateway's job.

### Failure-Mode Analysis

| Auth Choice | Failure Mode Prevented | Failure Mode Introduced |
|-------------|----------------------|------------------------|
| Gateway-layer auth | Unauthenticated queries reach resolvers; data exfiltration | Gateway becomes a single point of failure; auth logic duplicated if resolvers also check |
| Resolver-only auth | None -- this is the failure mode | Any resolver missing an auth check is a data leak. Proven catastrophic in every public GraphQL post-mortem |
| OAuth 2.0 + API keys | Covers both user-delegated and machine-to-machine flows | Token management complexity; refresh-token rotation edge cases |

### Premortem (18-month horizon)

**Most likely failure**: A partner integration shares an API key across environments and it leaks. The organization has no key-rotation mechanism that does not require partner code changes. The telltale sign is API keys with no expiration date and no rotation history.

---

## 5. Abuse-Protection Envelope

### Decision: Layered defense-in-depth. Persisted operations as the default production posture.

### Root-Cause Framing

The root cause of GraphQL abuse is not "malicious actors" -- it is **unbounded query cost**. GraphQL allows any consumer to compose arbitrarily expensive queries by nesting and multiplying fields. This is not a design flaw; it is the mechanism that makes GraphQL powerful. But it is also the mechanism that makes public GraphQL dangerous without constraints.

The 2026 WunderGraph guidance is explicit and well-supported by evidence: leaving GraphQL "fully open" is unsafe for any public surface. The mitigation stack is:

### Required Controls (in order of deployment priority)

| Priority | Control | Configuration | Failure Mode if Absent |
|----------|---------|---------------|----------------------|
| P0 | **Query depth limit** | Maximum 7 levels of nesting (adjust after measuring actual query patterns) | Nested circular-reference queries exhaust server resources |
| P0 | **Query cost analysis** | Static cost estimation per field; reject queries exceeding cost threshold (e.g., 1000 cost units) | A single query can request O(n^2) data by multiplying list fields |
| P0 | **Rate limiting** | Per-consumer, sliding-window rate limit on query cost units (not request count -- request-count rate limiting is useless for GraphQL) | A consumer can issue many cheap queries that individually pass limits but collectively exhaust resources |
| P1 | **Persisted operations allowlist** | In production, only execute queries whose SHA-256 hash is registered in the allowlist | Adversarial query crafting; zero-day query shapes not covered by depth/cost limits |
| P2 | **Introspection disabled in production** | Disable `__schema` and `__type` in production; provide SDL via docs site | Schema exposure gives attackers a complete map of available types and relationships |

### Persisted Operations Posture

This is the largest security fork in the specification. The decision:

**Default: persisted operations only in production. Ad-hoc queries accepted only in sandbox/staging environments.**

| Posture | When to Use | Tradeoff |
|---------|------------|----------|
| Fully open queries | Internal APIs, prototyping phase | Maximum flexibility; maximum abuse surface |
| Persisted operations only | Public production APIs where the consumer surface is finite (mobile apps, partner SDKs, first-party web) | Near-zero abuse surface; consumers must register query shapes before deployment |
| Hybrid (allowlisted + signed ad-hoc) | Public APIs that must support exploratory queries from unknown consumers | Complex to implement correctly; signing infrastructure adds operational burden |

### Failure-Mode Analysis

| Control | Failure Mode Prevented | Failure Mode Introduced |
|---------|----------------------|------------------------|
| Persisted operations | Arbitrary query abuse, schema exploration by attackers | Consumer deployment friction: every new query must be registered before it works in production; slows iteration for third-party developers |
| Cost analysis | Single expensive query exhausts server resources | Cost estimates are approximations; a "cheap" query with expensive resolver logic (e.g., aggregation) may pass cost limits but still be slow |
| Depth limiting | Deeply nested recursive queries | Legitimate queries that need 8+ levels of nesting are rejected; requires monitoring false-positive rate |

### Premortem (18-month horizon)

**Most likely failure**: The cost-analysis weights are set at launch based on synthetic benchmarks. Six months later, a resolver that was "cheap" at launch now calls a downstream service that has grown 10x slower. The cost analysis approves the query, but the resolver times out. The telltale sign is a growing gap between estimated query cost and actual query latency.

### Discipline Requirement

Monthly review of cost-analysis accuracy: compare estimated cost vs. actual wall-clock latency for the top-100 queries by volume. If the correlation coefficient drops below 0.7, recalibrate weights.

---

## 6. Operational and Observability Surface

### Decision: Query-level observability is a launch requirement, not a post-launch improvement.

### Root-Cause Framing

The root cause of GraphQL operational incidents is not "the server is slow" -- it is **the inability to attribute latency to a specific resolver within a specific query shape**. In REST, a slow endpoint is trivially identified by URL. In GraphQL, every request hits the same URL (`/graphql`), and a single query may invoke 20+ resolvers. Without query-level tracing, debugging performance degradation is guesswork.

### Required Observability Stack

| Layer | What to Observe | Tool | Alert Threshold |
|-------|-----------------|------|-----------------|
| Gateway | Request rate, error rate, p50/p95/p99 latency by operation name | Apollo Router telemetry / custom gateway metrics | p99 > 2s sustained for 5 min |
| Query execution | Per-resolver latency, per-field error rate | Apollo Tracing / OpenTelemetry spans | Any resolver p95 > 500ms |
| N+1 detection | Consecutive identical data-loader batch misses | Custom middleware counting DataLoader dispatch patterns | >10 sequential loads of the same type in one query |
| Query plan | Persisted operation hash, query shape signature | Gateway logging | Unknown operation hash (unregistered query) |
| Schema health | Deprecated-field usage count, field-usage frequency | Apollo Studio analytics / custom schema registry | Deprecated field still receiving >100 req/day at T-30 before removal |

### Why This Is Heavier Than REST

In REST, the observability baseline is HTTP status codes by endpoint. That is ~10 metrics. In GraphQL, the baseline is per-resolver latency across N resolvers across M query shapes. That is N x M metrics. This is not a nice-to-have -- it is the cost of admission for public GraphQL.

### Failure-Mode Analysis

| Observability Choice | Failure Mode Prevented | Failure Mode Introduced |
|---------------------|----------------------|------------------------|
| Per-resolver tracing | Cannot diagnose which resolver in a 20-resolver query is slow | High cardinality metrics; storage costs scale with resolver count |
| N+1 detection | Silent performance degradation as schema grows | False positives from legitimate multi-fetch patterns |
| Schema health tracking | Deprecated fields become permanent zombies | Additional CI pipeline complexity; alert fatigue if thresholds are poorly tuned |

### Premortem (18-month horizon)

**Most likely failure**: The observability pipeline was built for the initial 30 resolvers. After 18 months, there are 200 resolvers. The tracing backend (Jaeger, Datadog, etc.) is now ingesting 10x the volume, costs have ballooned, and the team starts sampling traces to reduce cost -- which means they miss the slow resolver when it matters. The telltale sign is observability cost growing faster than query volume.

---

## 7. REST Coexistence and Deprecation Strategy

### Decision: Greenfield -- no coexistence required for this project.

### Evidence

The codebase scan confirms the host project (SuperClaude) has **no existing REST API**. There is nothing to coexist with, migrate from, or deprecate. This is the simplest possible starting condition.

### However: If the organization later exposes REST endpoints alongside the GraphQL API

The coexistence policy must be:

| Concern | Policy |
|---------|--------|
| Data model | Both REST and GraphQL must derive from the same canonical data model. Drift is a defect. |
| Feature parity | GraphQL is the primary surface. REST provides a compatibility layer for consumers that cannot adopt GraphQL. New features ship in GraphQL first; REST follows only if consumer demand exists. |
| Deprecation | REST endpoints have a 12-month deprecation window. GraphQL fields have a 6-month window. The asymmetry reflects REST's versioned nature vs. GraphQL's additive-only model. |
| Documentation | One docs site, two tabs. Schema reference for GraphQL; OpenAPI spec for REST. Do not split documentation into separate sites. |

### Failure-Mode Analysis

| Coexistence Choice | Failure Mode Prevented | Failure Mode Introduced |
|-------------------|----------------------|------------------------|
| Shared data model | REST and GraphQL return inconsistent data for the same entity | Data-model changes must be validated against both surfaces; deployment coupling |
| GraphQL-first, REST-follows | Dual maintenance burden for every feature | REST consumers become second-class citizens; feature gaps erode trust |

---

## 8. MVP Scope vs. Full Vision

### Decision: Ship queries and mutations only. Subscriptions, federation, and advanced caching are post-MVP.

### MVP Scope (Ship This First)

| Component | Scope | Excluded (Post-MVP) |
|-----------|-------|---------------------|
| Query type | Core entity queries with Relay-style cursor pagination | Aggregation queries, search, faceted filtering |
| Mutation type | CRUD operations for the primary domain | Batch mutations, optimistic concurrency |
| Auth | API-key authentication + gateway-layer enforcement | OAuth flow, mTLS, field-level authorization |
| Abuse protection | Depth limit (7) + static cost analysis + rate limiting by cost units | Persisted operations allowlist (enable after MVP stabilizes) |
| Observability | Per-query latency, error rate, top-10 slow queries | Per-resolver tracing, N+1 detection, schema health analytics |
| Schema evolution | Deprecation annotations required; manual removal tracking | Automated schema registry with usage analytics |
| Introspection | Enabled in sandbox, disabled in production | N/A |
| Documentation | Auto-generated schema docs (GraphQL Markdown / Magidoc) | Interactive playground, generated SDKs |

### Full Vision (Post-MVP, Ordered by Priority)

1. **Persisted operations allowlist** -- upgrade from open queries to allowlisted-only in production
2. **Per-resolver tracing with OpenTelemetry** -- full observability stack
3. **OAuth 2.0 flow** -- if consumer base includes third-party developers
4. **Subscriptions** -- only if real-time data is a stated value proposition
5. **Federation migration** -- only when team-structure trigger is met (see Section 2)
6. **Generated SDKs** -- Apollo Client codegen for TypeScript, Swift, Kotlin
7. **Advanced caching** -- persisted-query HTTP caching, CDN integration

### Failure-Mode Analysis

| Scope Choice | Failure Mode Prevented | Failure Mode Introduced |
|-------------|----------------------|------------------------|
| Ship queries/mutations only | Over-engineering; 6-month launch delay | Early consumers cannot subscribe to real-time updates; may build polling workarounds |
| Skip persisted operations in MVP | Faster time-to-market | Abuse window during MVP; mitigated by depth/cost limits as interim controls |
| Skip subscriptions | Simpler server; no WebSocket/ broker infrastructure | If real-time IS the value-prop, this MVP is useless. This decision must be validated against the product brief |

### Premortem (18-month horizon)

**Most likely failure**: The MVP ships without persisted operations. The interim depth/cost limits are "good enough" and the team never circulates back to implement the allowlist. Eighteen months later, a novel query-abuse pattern bypasses the cost-analysis weights. The telltale sign is persisted operations remaining in the backlog for more than two quarters after launch.

---

## 9. Risks Justifying Rejection of GraphQL Entirely

This section is not boilerplate. If any of the following conditions are true, the organization should not adopt GraphQL:

### Condition 1: No Measurable Problem with REST

If the organization does not have an existing REST API (confirmed by codebase scan), and the consumer base has not articulated over-fetching or under-fetching as a measurable pain point, then GraphQL solves a problem that does not exist. **The cost of GraphQL's operational complexity (see Section 6) is not justified by speculative DX improvement.**

Decision criterion: Before committing to GraphQL, instrument the current API (or absence thereof) for 30 days. Quantify: payload waste percentage, round-trip count per page load, consumer complaints about API friction. If none of these metrics are measurable, do not adopt GraphQL.

### Condition 2: Consumer Base Is Predominantly Server-to-Server Integration

If the primary consumers are backend services performing simple CRUD operations against known resources, REST with OpenAPI is superior on every axis: caching, idempotency, tooling maturity, operational simplicity. GraphQL's value proposition (client-driven query shaping) is irrelevant when the consumer is another service with a known, stable data requirement.

### Condition 3: Team Cannot Commit to Schema Governance

If the organization cannot staff a schema-review process (minimum: one reviewer, 24-hour SLA on schema-change PRs, CI-enforced breaking-change detection), then GraphQL's "versionless" promise is a lie. Without governance, the schema will rot faster than versioned REST endpoints, because the accumulation mechanism (additive-only fields) is more insidious than explicit version bumps.

### Condition 4: Operational Maturity Is Insufficient

If the team does not have experience with distributed tracing, query-cost analysis, or resolver-level performance debugging, the learning curve for operating public GraphQL is 3-6 months of production incidents before competency. REST's operational model (HTTP status codes, endpoint-level latency) is familiar to any engineer. GraphQL's operational model (query-shape-level latency, per-resolver tracing, N+1 detection) is a different skill set.

### Condition 5: Timeline Pressure Precludes Governance Setup

If the API must ship in less than 3 months, and the team cannot simultaneously build the API surface AND the governance tooling AND the observability stack, then GraphQL should be deferred. A REST API with OpenAPI can be governed with lighter tooling (Swagger UI, schema diff in CI) and requires less operational infrastructure.

### Quantified Decision Matrix

| Factor | Favors GraphQL | Favors REST |
|--------|---------------|-------------|
| Consumer type | Mobile/web clients, composite UIs | Server-to-server, simple CRUD |
| Data shape | Deeply nested, relational, variable projections | Flat resources, predictable shapes |
| Team structure | 1-2 teams, schema ownership clear | >3 teams, would need federation immediately |
| Operational maturity | Experience with distributed tracing, resolver debugging | HTTP-centric observability only |
| Timeline | >= 4 months to launch + governance | < 3 months to ship |
| Existing surface | Over-fetching/under-fetching is measured and painful | No existing API, or existing API has no measured pain |

---

## 10. Open Questions as Decision Branches

The seed brief surfaces eight open questions. This specification takes a position on each, with residual uncertainty noted.

### Q1: Does the host project already have a public REST API?

**Position**: No. The codebase scan confirms zero public API surface. This is a greenfield exercise.
**Residual uncertainty**: None. The evidence is definitive.

### Q2: Who are the primary external consumers?

**Position**: Not specified. This is the single most impactful open question. The auth model (Section 4), abuse-protection posture (Section 5), and DX investment (Section 8) all depend on the answer.
**Decision criterion**: The organization must answer this before MVP scoping is finalized. If the answer is "we don't know yet," default to the partner-integration profile (small N, deep contracts, API keys) because it is the least operationally complex and the most forgiving of incomplete DX tooling.

### Q3: Expected query volume / shape?

**Position**: Unknown. The single-graph vs. federation decision hinges on team structure, not query volume (federation is a team-structure solution, not a performance solution). Query volume affects infrastructure sizing, not topology.
**Decision criterion**: Design for 100 RPS per consumer as a planning assumption. Instrument actual volume post-launch and resize.

### Q4: Multi-team backend or single team?

**Position**: Single team. The codebase has no microservice boundaries. Federation is not justified.
**Residual uncertainty**: Low. If the organization plans to hire a second backend team within 12 months, this should be revisited.

### Q5: Authentication context?

**Position**: API-key-only for MVP. See Section 4. OAuth/mTLS are post-MVP based on consumer profile.
**Decision criterion**: If any consumer requires user-delegated access (acting on behalf of an end user), OAuth 2.0 is required and should be elevated to MVP.

### Q6: Deprecation tolerance?

**Position**: 6-month minimum window for public fields. See Section 3.
**Decision criterion**: If the organization has named partner integrations with contractual SLAs on field stability, extend to 12 months for those fields only.

### Q7: Budget/timeline forcing function?

**Position**: Not specified. This specification's MVP scope (Section 8) assumes >= 4 months. If the timeline is < 3 months, see Condition 5 in Section 9.
**Decision criterion**: If the timeline is < 3 months AND the team lacks GraphQL operational experience, defer GraphQL in favor of REST + OpenAPI.

### Q8: Language/framework?

**Position**: Stack-agnostic for this specification. If targeting the host codebase (Python), the server library is Strawberry (type-hint-native, best DX for new projects in 2026) or Ariadne (schema-first, if the team prefers SDL-first workflow). FastAPI as the ASGI host.
**Decision criterion**: Choose based on team familiarity. Do not let GraphQL drive the language choice -- let the existing stack drive the GraphQL library choice.

---

## 11. Summary of Decisions

| Decision Area | Position | Confidence | Reversibility |
|--------------|----------|------------|---------------|
| Topology | Monolithic single graph | High (90%) | Reversible -- migrate to federation when team-structure trigger is met |
| Schema evolution | Additive-only, 6-month deprecation window, CI-enforced governance | High (95%) | Partially reversible -- deprecation windows can be extended, not shortened |
| Auth model | API-key at gateway layer for MVP | Medium (75%) | Reversible -- add OAuth/mTLS as post-MVP tiers |
| Abuse protection | Depth + cost analysis + rate limiting for MVP; persisted operations post-MVP | High (85%) | Reversible -- persisted operations can be deployed at any time |
| Observability | Per-query latency + error rate as MVP; per-resolver tracing post-MVP | High (90%) | Additive -- more observability is always possible |
| REST coexistence | Not applicable (greenfield) | High (95%) | N/A |
| MVP scope | Queries + mutations + API-key auth + depth/cost limits + basic metrics | Medium (80%) | Adjustable -- scope can grow or shrink based on timeline |
| GraphQL adoption | Conditional on measurable pain with current surface | High (85%) | Reversible -- GraphQL can be deprecated in favor of REST if operational costs outweigh DX benefits |

---

## 12. Recommended Next Step

Before a single line of GraphQL code is written, the organization must answer **Question 2** (who are the consumers?) and validate at least one measurable pain point with the current API surface (or absence thereof). This specification is decision-grade, but it is grounded in the assumption that GraphQL is the right tool. That assumption must be tested before the organization incurs the operational cost this specification describes.

The cheapest validation: expose three REST endpoints with OpenAPI docs to a pilot consumer group. Measure payload utilization and round-trip counts for 30 days. If over-fetching exceeds 40% of payload bytes and round-trip counts per page load exceed 5, proceed with GraphQL. Otherwise, invest in REST improvement -- it will be faster and cheaper.
