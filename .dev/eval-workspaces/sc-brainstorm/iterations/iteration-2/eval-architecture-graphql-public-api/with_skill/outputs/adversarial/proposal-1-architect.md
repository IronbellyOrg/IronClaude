---
proposal_id: 1
persona: architect
model: opus
lens: long-horizon ecosystem fit, API evolution, schema governance
---

# Proposal 1 — Architect: Build a GraphQL Gateway as the v3 Foundation, REST Remains for Public Long-Tail

## Position

The strategic angle (v3 planning starts Q3 2026) is the strongest argument in the seed brief, and it points clearly toward GraphQL — **not as a replacement for REST**, but as the **foundation of v3**. The over-fetching pain is real; the partner requests are real; the in-house expertise gap is real but bounded; the worst outcome is starting v3 planning in 9 months with no concrete answer on API shape and defaulting to "REST again because we know it" by inertia.

## Recommendation

**Build a GraphQL gateway in front of existing REST services**, using **Apollo Federation v2 (managed GraphOS)** for the schema governance and ops surface, **persisted-queries-only for partners**, and **REST continues to serve the public long-tail and SDK-generated clients unchanged**. v3 becomes "first-party + integration-partners use GraphQL, public-developer REST stays". This is the same shape GitHub, Shopify, and Atlassian have converged on for similar consumer segmentation.

## Why this shape

**Ecosystem fit, on a 3-5 year horizon.** The next 3 years will see continued migration of partner-facing APIs to GraphQL. By 2028, partners asking for GraphQL will be the majority, not the leading edge. Building the foundation now means v4 / v5 planning is unburdened by "should we have GraphQL?" — that question is answered.

**Apollo GraphOS, not OSS-from-scratch.** The in-house expertise gap is the dominant operational risk. Managed schema registry, query planner, operation cost analysis, and contracts/governance reduce the surface that requires deep GraphQL operational expertise. The ~$2-5K/mo cost is small relative to the engineer-month savings on operational ramp-up. **Vendor lock-in is the deliberate trade** — we accept it for 2-3 years to buy operational velocity; if the cost or governance model degrades, the schema and resolvers are portable to OSS Router or Yoga.

**Persisted-queries-only for partners, ad-hoc for first-party.** This is the Shopify/GitHub pattern and it solves the operational hardest parts: query cost predictability (parse-time-known cost), aggressive response caching (persisted queries can be GET requests), and surface hardening (no string-parsing attacks on partner queries). The "GraphQL flexibility" pitch lives in first-party clients where we control the deploy cadence.

**REST remains for public long-tail, unchanged.** ~25% of traffic is SDK-generated public-developer clients used to REST conventions. Forcing this segment onto GraphQL is a hostile migration with no upside; they don't have the over-fetching pain (their use cases are typically single-resource fetches), and the SDK ecosystem assumes REST. v3 = "GraphQL for the high-value high-customization segments, REST for the well-served REST-native segment".

## Migration story

- **Phase 0** — Bring in Apollo GraphOS, design schema for the top 12 over-fetching pain points (the merchant-dashboard query plus 11 others). ~6 engineer-weeks.
- **Phase 1** — Wrap those 12 query paths as Federation v2 subgraphs over existing REST services; expose to first-party iOS / Android with feature-flag. ~8 engineer-weeks.
- **Phase 2** — Expose to the 2 partners who asked, persisted-queries-only, registered queries in a developer console. ~4 engineer-weeks.
- **Phase 3** — Operational ramp at 2 partners' production traffic, schema governance process matures. ~2 quarters of calendar time before broader partner exposure.
- **Phase 4** — v3 planning kicks off in Q3 with concrete data on partner satisfaction, cost-per-query, and operational confidence.

Total to "ready for v3 planning": ~18 engineer-weeks engineering + 2 quarters operational calendar. Fits the Q3 2026 forcing function.

## What I'd push back on

A proposal that says "REST evolution is good enough" is solving the over-fetching pain locally and ignoring the strategic question. The brainstorm explicitly asks for an input to v3 planning — defaulting to REST-evolution gives v3 nothing new to plan around, and partners who asked for GraphQL learn that we heard them and chose not to act. The cost in partner relationship is invisible but real.

## Risks

- **R1 (high)** — Operational ramp underestimated. Managed gateway helps; doesn't eliminate. *Mitigation*: hire 1 senior engineer with public GraphQL operational experience before Phase 1; partner with Apollo PS for the first 6 months.
- **R2 (medium)** — Apollo commercial model shifts (recent history: 2023-2024 pivot). *Mitigation*: contractual exit clauses; document portability path to OSS Router quarterly.
- **R3 (medium)** — Schema governance debt at the partner boundary. *Mitigation*: contracts (per-partner schema variants) from day one; no "single graph for all partners" deployment.
- **R4 (low)** — First-party clients prefer to keep REST; GraphQL added complexity for marginal gain. *Mitigation*: opt-in per app; do not force migration.

## Confidence

High on the strategic framing. Medium on the operational ramp estimate (this is the largest unknown). Low on whether Apollo specifically is the right managed gateway in 18 months — but the schema and resolvers are portable, so this is a recoverable choice.

## Cost

~18 engineer-weeks of engineering + ~$30K-60K/year managed gateway + 1 senior hire + ongoing operational ramp. ~6-9 months calendar.
