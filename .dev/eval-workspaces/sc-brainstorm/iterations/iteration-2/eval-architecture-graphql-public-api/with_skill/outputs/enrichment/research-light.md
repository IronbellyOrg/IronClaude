---
source: research-light
quality_tier: primary
simulated: true
created: 2026-05-25T00:00:00Z
topic: "explore using GraphQL for public API"
---

# Research-Light: GraphQL for Public APIs in 2026

## Mature Options (Gateway + Schema)

**1. Apollo Federation v2 (managed via Apollo GraphOS or self-hosted Router)** — The most enterprise-deployed federation pattern. Subgraphs per service, single client-facing schema. Mature schema-registry, query planner, and contracts/governance tooling. Cost: managed pricing scales with operations volume; self-hosted Router is OSS but operational overhead is real (Rust router, schema registry, CI integration). Strengths: best-in-class governance tooling, persisted queries, query cost / depth control out of the box, contract testing built in. Weaknesses: lock-in to Apollo's federation directive set; Apollo's commercial pivot in 2023-2024 made the OSS story slightly less clear.

**2. GraphQL Yoga (The Guild) + Mesh** — OSS, modular. Yoga is a server framework; Mesh stitches existing APIs (REST, gRPC, GraphQL) into a single graph. Lower cost, more assembly required, more flexibility. Strengths: vendor-neutral, modular, good for "wrap existing REST" patterns. Weaknesses: governance tooling is do-it-yourself; query cost control is bring-your-own.

**3. Hasura** — Auto-generated GraphQL over Postgres + other data sources. Excellent for database-first GraphQL. Strengths: instant productivity for CRUD; great RBAC story. Weaknesses: opinionated and tightly coupled to data layer — does not naturally fit "wrap existing REST services" use case; commercial license terms for the cloud product are restrictive for some enterprise use.

**4. AppSync (AWS)** — managed GraphQL gateway. Strengths: AWS-native, scaling and caching baked in. Weaknesses: ties to AWS ecosystem, less flexible schema governance, fewer enterprise governance tools than Apollo GraphOS.

## REST Evolution Alternatives

**1. JSON:API (jsonapi.org)** — Sparse-fieldset support (`?fields[merchant]=name,plan_tier`), compound documents (include related resources in one response), well-specified. Mature, widely deployed (RIPE NCC, GitHub uses elements). Cost: schema discipline + library adoption per server framework; ~weeks not months.

**2. OpenAPI 3.1 + sparse-field extensions** — Conventional REST with documented field selection. Less prescriptive than JSON:API but better-supported by existing tooling (SDK generators, API gateways, client libraries). Cost: adopt-as-you-go per endpoint.

**3. HTTP/2 + multiplexing + Cache-Control** — Operational tuning rather than API design change. Many "too many round-trips" complaints are 50% solved by HTTP/2 multiplexing and aggressive cache headers, without any API surface change. Cost: weeks of operational tuning; near-zero API change.

## Real-World Enterprise Adoption Patterns (2024-2025)

**Shopify** — Public-facing GraphQL Admin API; persisted-queries-only for public partners (ad-hoc queries are first-party-only). Schema governance via internal review process. Per-query cost model: a "calculated cost" assigned at query parse time, partner is billed per cost-unit-per-second.

**GitHub** — REST v3 and GraphQL v4 coexist (8+ years now). Public GraphQL is rate-limited by query cost (separate from REST rate limits). Schema deprecation handled via documented sunset dates and changelog entries; never breaking removals.

**Netflix** — Uses GraphQL Federation internally; does NOT expose GraphQL to public partners (REST + gRPC for public, GraphQL for first-party clients). Operational position: "GraphQL is great for clients you control; it's hard to get right for clients you don't."

**Atlassian** — REST primary for public partners; GraphQL gateway for first-party clients (Jira, Confluence apps). Stated reasoning: GraphQL operational ramp-up was multi-quarter even with strong in-house expertise.

**Walmart Labs (caveat: cautionary tale circa 2022-2023)** — Publicized struggles with a partner-facing graph diverging from internal needs; led to schema-as-contract pain and eventual scope reduction. The reference case for "don't ship public GraphQL without strong schema governance from day one."

## Operational Considerations Specific to Public GraphQL

**Query cost analysis** — A single permissive GraphQL query can fan out to thousands of resolver calls. Cost-budget per query (parse-time calculated) is non-optional for public exposure. Apollo's "operation registry" + cost directive is one pattern; Shopify's "calculated cost" is another. Yoga + custom cost plugin is the assembly-required path.

**N+1 resolver patterns** — Default GraphQL resolution invites N+1 database queries (or service calls). DataLoader (the canonical pattern) batches at the request scope. Mandatory for any non-trivial public deployment.

**Cache key granularity** — GraphQL responses are per-query, not per-resource. Standard HTTP caching is materially harder than with REST. Persisted queries + GET-style requests + response-level caching is the common pattern; ad-hoc POST queries are typically uncacheable.

**Rate limiting** — Per-endpoint rate limits don't translate to GraphQL. Per-cost-unit rate limits are the equivalent. Implementing this on top of an existing per-endpoint rate-limit infrastructure is non-trivial; often a separate enforcement layer.

**Schema governance** — Who owns "the schema"? Walmart-Labs-style divergence happens when partner needs and internal needs are not reconciled. Apollo GraphOS has contracts (variant graphs per consumer); other gateways require manual discipline.

**Persisted queries vs ad-hoc** — Public GraphQL deployments at scale tend toward persisted-only for partners (registered query, deployed via developer console, executed by ID). Removes cost-analysis surprises, enables aggressive caching, hardens the surface. Loses some of the "GraphQL flexibility" pitch — but that flexibility was always more honored in the first-party-client breach than in the partner-API observance.

## Cost / Operational Ramp Estimates (in-house, 2026 pricing)

- **GraphQL gateway over existing REST (e.g., Yoga + Mesh + custom cost plugin)**: 8-12 engineer-weeks for MVP serving the over-fetching pain on 6-12 highest-value queries; 4-6 quarters of operational ramp to be confident at full partner traffic.
- **Apollo Federation v2 (managed GraphOS)**: 4-8 engineer-weeks for MVP plus managed-service cost (~$2-5K/mo at our scale band, growing with operations); 2-4 quarters of operational ramp because the platform handles much of the operational concern. Vendor lock-in trade-off explicit.
- **REST evolution to JSON:API or OpenAPI sparse-fields**: 6-10 engineer-weeks to extend the 12 highest-pain endpoints; 1-2 quarters of customer adoption (partners need SDK updates). Operational ramp: near-zero — same operational surface as today.
- **HTTP/2 + cache tuning alone**: 2-4 engineer-weeks of operational tuning; no API surface change. Closes ~50% of the over-fetching pain for screens that are dominated by network round-trips rather than payload size.

## Implications for Brainstorm

- "Public-facing GraphQL" is operationally distinct from "internal GraphQL"; in-house experience on the latter does NOT transfer to the former.
- The over-fetching pain is real but NOT uniquely a GraphQL-solution problem; REST-evolution patterns address ~60% at <50% of the cost.
- The strategic angle (v3 foundation) is the strongest argument for going deeper than HTTP/2 tuning — but lock-in to one direction at this brainstorm is premature; design recommendation should preserve optionality.
- The two-persona debate is expected to surface tensions on: ecosystem fit (architect lens) vs operational reality (backend lens), greenfield-vs-evolution, and persisted-query-default vs ad-hoc-permissive.
