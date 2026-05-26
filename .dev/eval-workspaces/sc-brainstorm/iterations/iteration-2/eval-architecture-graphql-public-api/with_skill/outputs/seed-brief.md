---
topic: "explore using GraphQL for public API"
domain: architecture
strategy: systematic
depth: quick
proposal_count: 2
handoff_target: design
created: 2026-05-25T00:00:00Z
---

# Seed Brief: architecture-graphql-public-api

## Socratic Dialogue Record (architecture-domain QUICK tier — 6 questions, Clarify batch only)

**Q1. What's driving the question — a current pain point, a partner request, or strategic exploration?**
A: All three, weighted as: (a) partner request — two enterprise integration partners have asked for "fewer round-trips on our mobile clients" and explicitly named GraphQL; (b) current pain — our REST API has 80+ endpoints with significant over-fetching for typical mobile screens (a "merchant dashboard" screen pulls from 6 endpoints); (c) strategic — we are starting to plan the next major API version (v3) and "should we keep REST" is a genuine open question, not a foregone conclusion.

**Q2. What's the scope: a parallel API (REST + GraphQL coexist), a replacement, or a layer in front of existing services?**
A: Most likely a layer in front (BFF / federation gateway). We are NOT considering removing the REST API in any horizon we can plan to today. The question is whether we add a GraphQL gateway that wraps the existing services and exposes a typed schema, OR whether we extend the existing REST API with the now-standard "sparse fieldsets / compound documents" patterns (JSON:API / GraphQL-on-REST hybrid).

**Q3. Who consumes the API and which clients matter most?**
A: Three consumer segments. (i) Our own first-party clients (web SPA, iOS, Android, internal admin tooling) — about 40% of traffic. (ii) Integration partners (~50 partners, 35% of traffic) — these are the ones asking for GraphQL. (iii) Public developers using our marketing-site-documented API (~25% of traffic) — these are typically using SDK-generated clients in Ruby / Python / Node, used to REST conventions.

**Q4. What non-negotiables exist (latency, auth, versioning, observability)?**
A: (i) Auth: existing OAuth2 + API-key flows must continue to work; we are NOT going to ask partners to re-auth for a GraphQL endpoint. (ii) Latency: typical query end-to-end ≤ 200ms P95 for our own clients, ≤ 500ms P95 for partners (cross-region). (iii) Versioning: REST currently uses URL-path versioning (v1, v2); whatever we do with GraphQL, partners need a way to know "what shape of response am I getting and how stable is it?". (iv) Observability: per-resolver latency, error rate, and field-usage analytics are non-optional (one of the reasons GraphQL is interesting at all).

**Q5. What's the test/expertise surface — do we have any GraphQL experience in-house?**
A: Limited. Two engineers have built GraphQL servers at previous jobs (one used Apollo, one used GraphQL Yoga). Nobody has run a public-facing GraphQL service at our traffic scale. Internal admin tooling has a small GraphQL endpoint used by 3 internal users — battle-tested only in that small surface. Significant learning curve at the operational level (caching, query cost analysis, persisted queries, rate limiting on a per-field basis vs per-endpoint).

**Q6. Is there a deadline or other forcing function?**
A: Soft. Two partners have raised the request in their last QBR (Q1 2026). They are not threatening to leave; they are signaling that "fewer round-trips" is on their roadmap. Our next API version (v3) planning starts in Q3 2026 — we want this brainstorm + a design recommendation in hand by then so that the v3 conversation includes "is the foundation REST or GraphQL" as a first-class question, not an afterthought.

## Problem Statement

Two enterprise integration partners are asking for GraphQL specifically (to reduce mobile client round-trips); our REST API has documented over-fetching pain (typical mobile screens pull from 6+ endpoints); and we are about to begin v3 planning where the choice of API style is foundational. This brainstorm scopes the question of whether to (a) add a GraphQL gateway in front of existing services, (b) extend REST with sparse-fieldset / compound-document patterns, or (c) do neither and address the over-fetching pain another way. The output should be a design-ready recommendation that the v3 planning conversation can build on; it is explicitly NOT a commitment to ship GraphQL.

## Known Context

- ~80 REST endpoints, URL-path-versioned (v1, v2).
- Three consumer segments: first-party (40%), integration partners (35%), public developers (25%).
- Two enterprise partners have asked for GraphQL; one mobile screen pulls from 6 endpoints (over-fetching is documented).
- Auth: OAuth2 + API-key, must remain compatible.
- Latency budgets: 200ms P95 first-party, 500ms P95 partners.
- In-house GraphQL experience: limited — 2 engineers with prior background; 1 small internal admin endpoint.
- v3 planning starts Q3 2026; this output is input to that.

## Constraints

- Existing OAuth2 / API-key auth flows continue to work for whatever is built.
- No removal of REST API in any current planning horizon.
- Public REST API documented contract is not changing as part of this brainstorm.
- Forcing-function timeline: design-ready recommendation before Q3 2026 v3 planning kickoff.
- Limited in-house GraphQL operational expertise — recommendations must include either training/hiring plan or explicitly use of a managed gateway.

## Success Criteria

- Clear recommendation: GraphQL gateway / REST-evolution / neither, with explicit reasoning.
- Cost/effort estimate at design-grade fidelity (engineering weeks, infrastructure footprint, operational ramp-up).
- Identified risks and migration story for both first-party clients and partners.
- Articulation of what "v3" looks like under each option, so the v3 planning team can use this as input.
- Two or more proposals with substantive disagreement (this brainstorm is exploratory; lock-in to one direction here would be premature).

## Open Questions (carried forward to design)

- Federation vs single-schema gateway: if GraphQL wins, do we build a single schema gateway or a federated graph from per-service subgraphs?
- Query cost / depth limits: what's the right cost model for partners (per-field, per-resolver, per-query, per-second)?
- Schema governance: who owns "the schema", what's the deprecation policy, how do we avoid the "Walmart Labs experience" of a partner-facing graph diverging from internal needs?
- Persisted queries vs ad-hoc queries: which is the public default for partners?
- Versioning under GraphQL: schema evolution + deprecation vs the REST-style v1/v2/v3 model — what works for our developer ecosystem?

## Enrichment Context

Research-light enrichment ran (`quality_tier: primary`, simulated for non-interactive eval). Full output at `enrichment/research-light.md`. Key signals folded into the brief:

- Apollo Federation v2, GraphQL Yoga, and Hasura are the three mature managed/self-hosted options; Apollo Federation is the most enterprise-deployed at our scale band.
- The "BFF as adapter over existing REST" pattern is well-trodden and lower-risk than schema-first GraphQL.
- JSON:API and OpenAPI 3.1 both have first-class sparse-fieldset support; "GraphQL-on-REST" patterns exist (e.g., `?fields[merchant]=name,plan_tier`) that address ~60% of the over-fetching pain at <5% of the cost.
- Public-facing GraphQL has known operational pitfalls at scale: N+1 resolver patterns, query cost explosions, cache-key granularity, schema governance debt. None are blockers; all are real.
- Enterprise GraphQL adopters (Shopify, GitHub) ship persisted-queries-only for public consumers; ad-hoc queries are first-party-only.

Confidence on enrichment: medium-high. A real web-deep pass would tighten cost-model and operational-experience claims.

## Personas Selected

Per `agent-spec-builder.md` §Persona-Matrix for `domain=architecture` at quick/proposal_count=2: **architect** (long-horizon API-shape decision, ecosystem fit) and **backend** (operational reality of running GraphQL at scale, performance/caching concerns). Two proposals, no within-persona variant rotation at this depth.
