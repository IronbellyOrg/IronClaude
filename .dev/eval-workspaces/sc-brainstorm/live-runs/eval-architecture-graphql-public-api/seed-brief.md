---
topic: "explore GraphQL for public API"
domain: architecture
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: design
created: 2026-05-25T00:00:00Z
---

# Seed Brief: explore-graphql-for-public-api

## Problem Statement

Partners and mobile clients are asking for a public API shape that reduces over-fetching and multi-endpoint orchestration, and GraphQL is one candidate architecture. The decision must be framed as requirements discovery for v3 API planning, not a premature commitment to a GraphQL gateway. The brainstorm should clarify whether a public graph, partner-only graph, REST evolution, BFF aggregation, or no-go path best satisfies the underlying API-product and operational goals.

## Known Context

- Existing repository templates and documentation examples lean REST/OpenAPI, so public API requirements must preserve existing consumers and documentation workflows.
- GraphQL introduces a schema contract, typed validation, and client-selected fields, but public exposure requires implementation-level demand controls outside the base specification.
- Research and existing eval context highlight persisted queries, query cost analysis, schema governance, deprecation policy, and REST evolution alternatives as key decision areas.
- Codebase enrichment is saved at `enrichment/codebase-context.md`; research-light enrichment is saved at `enrichment/research-light.md`.

## Constraints

- Existing REST/OpenAPI consumers and SDK-generation workflows must continue unless a deliberate migration plan is approved.
- Public API exposure requires rate limiting, abuse controls, observability, and support/runbook requirements before launch.
- Requirements must compare GraphQL against lower-risk alternatives such as sparse fieldsets, compound documents, and BFF aggregation.
- Design handoff should receive decision criteria and open questions, not an already-finalized gateway choice.
- Do not implement code in this brainstorm; produce requirements only.

## Success Criteria

- Requirements define which API pain points GraphQL must solve and which can be solved without GraphQL.
- Requirements specify public-contract governance: schema ownership, versioning/deprecation, changelog, consumer contracts, and query registration policy.
- Requirements include operational controls for query cost, depth/breadth, pagination, persisted queries, rate limits, caching, tracing, and incident response.
- Requirements identify success metrics such as reduced endpoint round-trips, lower client payload size, stable latency/error budgets, and partner adoption.
- Requirements provide a clear `/sc:design` handoff path.

## Open Questions

- Is the target consumer public developers, named integration partners, first-party clients, or all three?
- Which specific high-value screens or workflows suffer enough over-fetching to justify a graph?
- Can REST evolution solve the top pain points at materially lower cost?
- Should public GraphQL allow arbitrary ad-hoc queries, or require persisted/registered operations only?
- Who owns schema governance, deprecation policy, and partner communication?
- What operational experience gap must be closed before launch?

## Enrichment Context

- GraphQL validation is schema-based, but demand control is an implementation and governance responsibility.
- Trusted/persisted documents, query-cost analysis, pagination limits, depth/breadth controls, and field-level observability should be requirements if public GraphQL remains in scope.
- REST/OpenAPI continuity is a hard constraint because existing repository templates and likely consumers depend on it.
