---
handoff_type: design
source_brainstorm: ../merged-requirements.md
source_seed: ../seed-brief.md
debate_transcript: ../adversarial/debate-transcript.md
created: 2026-05-25T00:00:00Z
target_command: "/sc:design"
output_mode: text-only
---

# Design Handoff Brief: GraphQL Exploration → Design Phase

## Context

The brainstorm phase produced a phased measurement plan (Phase A: HTTP/2 + cache tuning; Phase B: REST sparse-fields with partner pilot) with a Phase C GraphQL contingency design ready to trigger under documented conditions. The design phase takes this as input and produces detailed, text-only architecture documents for each phase. No code; no infrastructure changes; design output is input to v3 planning in Q3 2026.

## Inputs

- `../merged-requirements.md` — functional + non-functional requirements, acceptance criteria, risks, open questions, provenance.
- `../seed-brief.md` — Socratic dialogue, problem statement, constraints.
- `../adversarial/debate-transcript.md` — the architect vs backend debate; the resolved sequencing approach.
- `../enrichment/research-light.md` — competitive landscape (Apollo Federation, Yoga + Mesh, Hasura, REST evolution patterns, enterprise GraphQL adoption case studies).

## Design Deliverables (text-only)

### D1 — Phase A Instrumentation Design

The load-bearing data-collection step. Produce a design document specifying:

- Which metrics are captured (per-screen round-trip count, per-screen wall-clock latency, per-endpoint payload size distribution, HTTP/2 multiplexing utilization, cache hit rate by endpoint).
- Where each metric is captured (gateway-side, client-side, both).
- How the baseline is measured before any tuning lever is pulled (this matters: "we don't know how much the HTTP/2 tuning helped" is a Phase A failure mode).
- Per-cause attribution methodology: how do we distinguish "HTTP/2 multiplexing helped" from "ETag discipline helped" from "N+1 elimination helped"?
- Concrete reporting artifact format: what does the Phase A report look like at end of Phase A? (It is the input to the Phase B / Phase C decision.)

### D2 — Phase B Sparse-Field Schema Design

For each of the top 12 over-fetching-pain endpoints, specify:

- Sparse-field query parameter shape: JSON:API style (`?fields[merchant]=name,plan_tier`) vs OpenAPI 3.1 extension style. Decide and document the trade-off.
- Compound-document inclusion shape (if adopted): `?include=plan,billing_summary` style relationship-fetching.
- Backward compatibility guarantees: omitting the parameter returns existing response shape exactly.
- SDK update story for the 2 pilot partners: what changes do their SDKs need? Who maintains them — partner or first-party?
- Per-endpoint specification document (12 documents, one per endpoint) that the engineering team can implement against.

### D3 — Phase C Contingency Architecture (GraphQL, designed-but-not-built)

If FR5 trigger fires, this is what gets built. Specify:

- Gateway choice trade-off matrix: Apollo Federation v2 (managed GraphOS) vs Yoga + Mesh vs Hasura. Decision deferred to trigger time, BUT the trade-off matrix is documented here so trigger-time decision is fast.
- Schema shape for the 3-5 specific queries Phase C would serve: merchant-dashboard + the 2-4 equivalent multi-endpoint screens identified in Phase A measurement.
- Persisted-queries-only enforcement design for partners: query registration developer-console UX, query ID generation, query versioning, query deprecation.
- Schema governance design: who owns the schema; deprecation policy; contracts per consumer (Walmart-Labs avoidance).
- Per-cost-unit rate limiting design: how query cost is calculated at parse time; how cost-units-per-second is configured per partner; how the existing per-endpoint rate-limit infrastructure integrates (or doesn't).
- N+1 mitigation: DataLoader pattern adoption; resolver-level caching design; per-resolver observability.
- Operational requirements document: dashboards, alerts, runbook entries, on-call training plan, senior-hire job description.
- First-party-clients-first rollout phase plan: which client (iOS, Android, internal admin, web SPA) integrates first; what's the kill-switch path; what's the success metric for "ready for partner exposure".

### D4 — v3 Planning Input Document

A concise (≤4 pages) document combining D1's Phase A measurement results (when available), D2's Phase B sparse-field architecture, and D3's Phase C contingency, framed as v3-planning input. The document explicitly states the trigger conditions under which v3 should adopt GraphQL vs REST + sparse fields as foundation. This is the document the v3 planning team builds their conversation on.

## Constraints on the Design Phase

- **Text-only output**: no code, no infrastructure changes, no migrations. The design phase produces documents the engineering team implements against in subsequent phases.
- **Preserve optionality**: D3's Phase C design must be ready-to-trigger but the design phase does NOT pre-commit to triggering it. The trade-off matrices and trigger conditions are the load-bearing pieces.
- **Reference the enrichment**: D3's gateway choice trade-off matrix MUST cite the real-world adoption patterns in `../enrichment/research-light.md` (Shopify, GitHub, Atlassian, Netflix, Walmart Labs).
- **Reference the debate**: D1-D4 must trace key decisions back to the debate-transcript tensions; the design phase carries forward the brainstorm's discipline about measuring before committing.

## Personas Recommended for Design Phase

- **architect** (primary): D2, D3, D4 — schema design, gateway choice trade-off, v3-planning framing.
- **backend** (primary): D1, D3 operational requirements — measurement instrumentation, operational design.
- **devops** (supporting): D1, D3 operational requirements — observability and rollout phases.
- **scribe** (supporting): D4 v3-planning input document — clarity, audience-fit for the planning team.

Recommended invocation:

```
/sc:design --source .dev/eval-workspaces/sc-brainstorm/iterations/iteration-2/eval-architecture-graphql-public-api/with_skill/outputs/merged-requirements.md --output-mode text-only --personas architect,backend,devops,scribe
```

## Success Criteria for Design Phase

- D1-D4 produced as text documents in the design phase output directory.
- D1 specifies a measurement methodology rigorous enough that Phase A's report at end-of-Phase-A definitively answers "what closed the pain and what didn't".
- D2 produces 12 per-endpoint specifications detailed enough for direct engineering implementation.
- D3 produces a contingency architecture detailed enough that engineering can begin Phase C within 2 weeks of trigger.
- D4 is ≤4 pages and ready as a Q3 v3-planning-kickoff agenda item.
