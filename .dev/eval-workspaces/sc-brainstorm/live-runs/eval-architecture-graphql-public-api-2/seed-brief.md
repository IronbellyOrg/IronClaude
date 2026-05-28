---
topic: "explore GraphQL for public API"
domain: architecture
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: design
created: 2026-05-25T19:59:00Z
dialogue_mode: auto-proceed (non-interactive)
---

# Seed Brief: explore-graphql-for-public-api

## Problem Statement

The organization is evaluating GraphQL as the technology for a public-facing API surface that external developers (third-party integrators, mobile/web clients, partner organizations) will consume. The current API surface — assumed to be REST/JSON or absent — has friction around over-fetching, under-fetching, version proliferation, and developer-experience differentiation. The brainstorm needs to surface the **architectural shape** of a GraphQL public API, the **tradeoffs against REST**, and the **operational/security obligations** that change when the API is exposed publicly rather than internally.

## Known Context

- API is **public** — external consumers, not just internal services. This raises the bar on stability, documentation, abuse prevention, and contract evolution.
- "Explore" framing implies the decision is **not yet made**. Both REST-style and GraphQL paths are still live; the brainstorm should produce decision-grade requirements, not jump to a federated-Apollo implementation.
- The host project's existing API conventions and stack are not surfaced in the topic. The merged requirements must either be stack-agnostic or surface stack as an open question.
- "For public API" carries an implicit promise of **stable contracts** — schema evolution discipline is a first-class requirement, not an afterthought.

## Constraints

- **Backward compatibility is non-negotiable** for any existing public surface — GraphQL adoption must be additive (parallel run) before any deprecation.
- **Public exposure dictates abuse-resistance** — query complexity limits, depth limits, persisted queries, rate limiting, and authentication must be designed-in, not bolted-on.
- **Schema is the contract** — schema evolution policy (deprecation windows, breaking-change definition, version cadence) must be defined before launch.
- **Operational story must exist** — observability (query-level metrics, slow-query detection, N+1 detection) is required before public traffic.
- **Tooling and DX expectations are high for public APIs** — playground, generated SDKs, docs site, introspection policy must be addressed.

## Success Criteria

- A decision-grade architectural brief that names: (a) the API server pattern (single-graph / federated / schema-stitched), (b) the schema-evolution policy, (c) the auth model, (d) the abuse-protection envelope, (e) the operational/observability surface.
- An explicit comparison against the REST alternative on at least three axes (DX, cost, operational complexity).
- A migration / rollout plan if an existing REST API is being augmented or replaced.
- Identification of the smallest viable shipping unit (MVP scope) vs. the full vision.
- Named risks that would justify rejecting GraphQL entirely.

## Open Questions

- Does the host project already have a public REST API, or is GraphQL the first public surface? (Affects coexistence vs. greenfield framing.)
- Who are the primary external consumers — partner integrations (small N, deep contracts), third-party developers (large N, shallow contracts), or both?
- What is the expected query volume / shape? (Drives single-graph vs. federation decision and infrastructure sizing.)
- Is there a multi-team backend that would push toward federation, or a single backend team that favors a monolithic schema?
- What is the authentication / authorization context — public anonymous, API-key, OAuth, mTLS for partners?
- What is the deprecation tolerance of consumers — can fields be removed on a 6-month clock, or is forever-stable required?
- Is there a budget/timeline forcing function, or is this a strategic exploration?
- What language/framework is the backend in? (Server library choice — Apollo Server, GraphQL Yoga, Hot Chocolate, gqlgen, async-graphql — depends on this.)

## Enrichment Context

(Full artifacts: `enrichment/codebase-context.md`, `enrichment/research-light.md`.)

### From codebase scan (Auggie, primary tier)

- **The host SuperClaude repo has no public API surface today.** It is a Click-based CLI (`src/superclaude/cli/main.py:20`) + pytest plugin, distributed via `pipx install`. No HTTP server, no REST endpoints, no GraphQL code. Only mention of GraphQL is inside a test fixture (`src/superclaude/cli/eval/suites/adversarial_merge_consistency.yaml:199`).
- **Target ambiguity becomes critical**: brainstorming a "public API" against this codebase is greenfield — there is no existing API to coexist with. The merged requirements must either (a) declare the host project (SuperClaude itself adding a public API), or (b) remain stack-agnostic for use elsewhere.
- **Stack constraints introduced if target = SuperClaude**: no HTTP framework dep, no auth, no persistence, no long-running process model. A public GraphQL API would be a substantial scope expansion requiring deployment-model decisions (separate server package, container, hosted service).

### From research-light (Tavily, primary tier, 2026 best practices)

- **Schema-first is non-negotiable for public GraphQL** — unlike REST where OpenAPI is optional, the schema *is* the contract.
- **Federation has become the dominant pattern** at scale by 2026 (Apollo Federation, WunderGraph Cosmo). Schema stitching is legacy. Federation is correct for multi-team / multi-service backends; monolithic graph is correct for single-team APIs.
- **Public exposure mandates query-shape control**: depth limits + cost analysis + **persisted operations allowlist** is the 2026 production posture. Leaving GraphQL "fully open" is now considered unsafe per WunderGraph's 2026 guidance.
- **Introspection should be disabled in production**; expose schema via docs site / SDL.
- **DataLoader and pagination are still the two biggest performance footguns** — unbounded list fields make rate limiting structurally impossible.
- **Caching is multi-layer** (client normalized + persisted-query HTTP cache + server-side resolver cache + federation distributed cache) — significantly more complex than REST's HTTP cache.
- **Schema evolution is "versionless" only with discipline**: 6-12 month deprecation windows for public APIs, schema lint/governance tooling (GraphQL Inspector, Apollo Studio) is a launch requirement, not nice-to-have.
- **Server library is stack-driven**, not GraphQL-driven (Strawberry for Python, Apollo/Yoga for TS, gqlgen for Go, etc.).
- **Subscriptions are opt-in** — don't ship in v1 unless real-time IS the value-prop.

### Constraints these enrichments add to the brainstorm

1. **Persisted Operations posture must be decided in the requirements** — open queries vs allowlisted-only is a security fork, not a deployment detail.
2. **Federation vs monolith must be named** — defaulting to "we'll figure it out later" is a known failure mode.
3. **Schema evolution policy is launch-blocking** — must be written before public exposure, not bolted on.
4. **Operational/observability surface (query metrics, slow-query detection, N+1 alerts) is a launch requirement** for public GraphQL — significantly heavier than REST's "200/4xx/5xx" baseline.
5. **Target project must be declared** — host codebase has nothing to migrate; the brainstorm result is decision-grade only if the target product is specified.
