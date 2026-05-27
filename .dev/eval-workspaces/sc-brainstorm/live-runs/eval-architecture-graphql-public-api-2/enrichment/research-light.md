# Research-Light: GraphQL for Public API (2026 best practices)

**Quality tier**: primary (Tavily, advanced depth, time_range=year)
**Date**: 2026-05-25

## Synthesized findings

### 1. Schema-first design is non-negotiable

Unlike REST (where an OpenAPI spec is optional), a GraphQL schema is the contract — every public-facing GraphQL API must invest in schema discipline from day one. Conway's Law applies: a single team can own a monolithic schema, but multiple teams pushing to one graph generally indicates federation is needed (Source: WunderGraph "10 Principles for Designing Good GraphQL Schemas").

### 2. Federation has become the default at scale (2026)

By 2026, **Apollo Federation** (or open-source equivalents like WunderGraph Cosmo) is the dominant pattern for multi-service GraphQL. Schema stitching is considered legacy. For a *new* public API, the choice is:

- **Monolithic single graph** — suitable if one team owns it end-to-end and the data model fits one schema.
- **Federated supergraph** — suitable if multiple teams contribute subgraphs, or if the API spans existing service boundaries.

Federation requires a router (Apollo Router, Cosmo Router) and adds operational complexity. Don't adopt it speculatively — adopt it when the team structure or service boundaries demand it.

### 3. Public exposure mandates query-shape control

The #1 production failure mode for public GraphQL APIs is **arbitrary query cost**. Mitigations, in increasing strictness:

| Control | What it does | When to use |
|---------|--------------|-------------|
| **Depth limiting** | Reject queries beyond N nested levels (`graphql-depth-limit`) | Minimum bar for any public API |
| **Query cost analysis** | Assign computational cost per field, reject above threshold | Production minimum for unbounded public APIs |
| **Persisted queries (allowlist)** | Only execute pre-approved query shapes (hash-identified) | **Strongly recommended for any public API where the client surface is finite** (mobile app, partner SDK, public site) |
| **Persisted operations as the only mode** | Disable ad-hoc queries entirely in production | Recommended unless you genuinely need open-ended discovery |

WunderGraph's 2026 guidance is explicit: leaving GraphQL fully open "isn't safe." Persisted Operations are now considered the table-stakes security posture for production public GraphQL.

### 4. Introspection should be disabled in production

By default GraphQL exposes the entire schema via introspection — giving any attacker a complete map. Best practice in 2026: disable in production; expose the schema via docs site / SDL download instead (Source: tech-insider.org "GraphQL vs REST 2026").

### 5. Pagination + N+1 are still the biggest performance footguns

- **Always paginate list fields** (`first`/`after` Relay-style cursor pagination is the standard). Unbounded lists make rate limiting impossible.
- **Always use DataLoader** (or per-language equivalent) for N+1 prevention — even for fields that "seem unlikely" to be called in list context (Source: iamraghuveer.com).

### 6. Caching is a multi-layer story

REST's HTTP-cache simplicity is GraphQL's biggest operational gap. The 2026-recommended stack:

1. Client-side normalized cache (Apollo Client, Relay, urql)
2. Persisted-query HTTP caching (with hash-based URLs, you regain CDN cacheability)
3. Server-side per-resolver caching (Redis distributed)
4. CDN/edge caching for persisted queries

Federation adds a layer: shared distributed cache across subgraphs.

### 7. Schema evolution: "versionless" only with discipline

GraphQL's "versionless" promise (additive changes via field deprecation, no /v1/v2 URLs) works **only** with strict policy:

- **Additive change is free** (new fields, new types).
- **Field deprecation requires a window** (industry norm: 6 months minimum for public APIs, 12 months for partner/enterprise).
- **Breaking changes are an explicit, governed event** — schema reviews, consumer impact analysis, comms plan.
- **Schema linting / governance tools** (GraphQL Inspector, Apollo Studio schema checks, Cosmo) are operational requirements, not nice-to-haves.

### 8. Server library landscape (2026)

| Language | Production-grade options |
|----------|--------------------------|
| Node.js / TypeScript | Apollo Server 4 (federation-native), Yoga (GraphQL Yoga 5), Mercurius (Fastify) |
| Python | Strawberry (recommended for new projects, type-hint-native), Ariadne (schema-first), Graphene (legacy but maintained) |
| Go | gqlgen (schema-first, codegen) |
| Rust | async-graphql |
| Java/Kotlin | DGS (Netflix), graphql-java |
| .NET | HotChocolate |

Choice is mostly driven by stack alignment, not GraphQL-specific differentiation.

### 9. Subscriptions (real-time) are an opt-in concern

GraphQL subscriptions exist but have caveats:

- Default `PubSub` implementations are single-instance only (in-memory) — useless for production at scale.
- Production requires an external broker (Redis pub/sub, NATS, Kafka) and an adapter.
- WebSocket vs Server-Sent Events choice matters for proxy/CDN compatibility.

For a v1 public API, **don't ship subscriptions unless they are the primary value-prop**.

### 10. Where GraphQL clearly beats REST in 2026

- **Mobile clients** on slow networks — single round-trip, no over-fetching, battery-friendly.
- **Frontend-heavy apps with composite UIs** that pull from many sources.
- **E-commerce / catalog APIs** with deeply nested relational data (Shopify is the reference public API).
- **Aggregation layers** in front of microservices (one schema, many services).

### 11. Where REST still wins

- **Simple resource CRUD with HTTP semantics** — caching, conditional requests, idempotency keys.
- **File upload / streaming** — GraphQL's multipart spec is workable but awkward.
- **Public APIs with very large/diverse consumer sets** — OpenAPI tooling ecosystem is broader, REST is more familiar to integrators.
- **Webhook fan-out, server-initiated calls** — GraphQL has no natural answer.

## Decision-grade tradeoffs surfaced

1. **Monolith vs Federation** is the largest architectural fork — choose deliberately based on team structure, not aspiration.
2. **Open queries vs Persisted Operations only** is the largest security fork — public APIs should default to persisted operations.
3. **Server framework choice** is mostly stack-driven — pick what matches your existing backend language.
4. **Schema evolution policy** is the largest organizational fork — must be written down and enforced before launch, not after.

## Top primary sources (2026)

- WunderGraph — "10 Principles for Designing Good GraphQL Schemas"
- WunderGraph — "MCP Gateway with Curated GraphQL Persisted Operations" (2026 take on locking down public GraphQL)
- Apollo GraphQL — "Caching Strategies in a Federated GraphQL Architecture"
- Render — "How to build and deploy a GraphQL API" (Jan 2026)
- iamraghuveer.com — "Building Production-Ready GraphQL APIs" (Feb 2026)
