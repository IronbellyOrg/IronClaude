---
spec_type: architecture-exploration
domain: architecture
strategy: systematic
adversarial_status: pass
convergence_score: 0.62
proposal_count: 2
source_proposals: [proposal-1-architect, proposal-2-backend]
debate_transcript: ./adversarial/debate-transcript.md
source_seed: ../seed-brief.md
handoff_target: design
---

# Merged Requirements: Explore GraphQL for Public API

## Problem Statement

Two enterprise integration partners have asked for GraphQL to reduce mobile-client round-trips; the existing REST API has documented over-fetching pain (typical mobile screens pull from 6+ endpoints); and v3 API planning begins Q3 2026, where API style is a foundational decision. This brainstorm produces a design-ready recommendation that the v3 planning conversation builds on; it is explicitly NOT a commitment to ship GraphQL. The two-proposal adversarial debate (Architect: build now; Backend: measure first) resolved by **sequencing**: a phased measurement plan (Phase A: HTTP/2 + cache tuning; Phase B: REST sparse-fields with partner pilot) precedes any GraphQL commitment, with a Phase C GraphQL contingency design ready to trigger if Phase A+B measurement and partner engagement confirm GraphQL-shaped residual pain.

## Functional Requirements

- **FR1** — **Phase A: HTTP/2 + Cache-Control + payload audit** on the 12 highest-traffic endpoints. Verify HTTP/2 multiplexing enabled at the gateway; audit `Cache-Control` and `ETag` discipline; eliminate any server-side N+1 patterns. **No API surface change.** Measure: per-screen round-trip count, per-screen wall-clock latency before vs after, per-endpoint payload size distribution. *(Backend Phase A, ratified)*
- **FR2** — **Phase B: REST evolution to sparse-fieldsets + compound documents** on the 12 highest-pain endpoints. JSON:API or OpenAPI 3.1 sparse-field convention (`?fields[merchant]=name,plan_tier`). Backward compatible (omitting the parameter returns existing response shape). *(Backend Phase B)*
- **FR3** — **Partner pilot in Phase B**: engage the 2 partners who requested GraphQL; give them sparse-field REST as the first delivery; explicitly ask "is this sufficient, or is GraphQL specifically a hard requirement?" Capture their answer. *(debate Tension 4 resolution)*
- **FR4** — **Phase C contingency design** (ready, not built): a focused GraphQL endpoint serving 3-5 specific queries (the merchant-dashboard "6 endpoints in 1 call" pattern + the equivalents). Persisted-queries-only for partners. First-party-clients first, partner exposure after operational confidence. *(Architect Phase 0-2, kept as contingency)*
- **FR5** — **Trigger conditions for Phase C, documented explicitly**: (a) Phase A+B closes < 70% of partner-reported round-trip pain measured at end of Phase B; OR (b) Partners explicitly confirm GraphQL specifically (not "fewer round-trips") is a hard requirement; OR (c) v3 planning conversation in Q3 produces an architectural direction that requires GraphQL foundation. *(merged shape)*
- **FR6** — **Phase C technology choice deferred**: if triggered, evaluate Apollo GraphOS vs Yoga+Mesh vs Hasura at trigger time, with measurement data and a more precise scope. Do not pre-commit. *(Tension 3 resolution)*
- **FR7** — **Phase C operational preconditions**: senior engineer hire with public-GraphQL operational experience + (if Apollo) GraphOS PS engagement. Both are required *before* Phase C launch, not parallel to it. *(Tension 2 resolution)*

## Non-Functional Requirements

- **NFR1** — Existing OAuth2 + API-key auth flows continue to work unchanged across all phases. *(seed C1)*
- **NFR2** — REST API existing endpoints remain backward compatible at every phase. Sparse-field parameter is additive. *(seed constraint)*
- **NFR3** — Phase A+B latency: typical-screen wall-clock latency improves by ≥25% on the merchant-dashboard reference query OR the assumption of "round-trip-dominated pain" is disproved. *(measurement-driven)*
- **NFR4** — Public REST API documented contract not breaking during this brainstorm's execution. *(seed constraint)*
- **NFR5** — All measurement instrumentation (request count per screen, wall-clock latency, payload size) deployed before Phase A behavior changes. *(Phase A baseline requirement)*
- **NFR6** — Phase C, if triggered, must persist-only for partners; ad-hoc query mode is first-party-clients-only. *(Architect + Backend agree on sub-question)*

## Acceptance Criteria

- **AC1** — Phase A complete: instrumentation deployed, HTTP/2 confirmed multiplexing, cache-headers audited on top 12 endpoints, N+1 patterns audited. Measurement baseline captured. *(FR1)*
- **AC2** — Phase A measurement report shows quantitative latency / round-trip delta from each tuning lever, attributable per-cause. *(FR1 measurement)*
- **AC3** — Phase B complete: top 12 endpoints support sparse-fieldset query parameter; existing response shape preserved when parameter is absent; partner SDKs updated for the 2 pilot partners. *(FR2 + FR3)*
- **AC4** — Phase B partner engagement: documented yes/no answer from each pilot partner on "is sparse-field REST sufficient?" Written in partner-success notes. *(FR3)*
- **AC5** — Phase C trigger decision documented at end of Phase B, with explicit reasoning citing FR5 conditions. Decision artifact stored as input to v3 planning. *(FR5)*
- **AC6** — v3 planning (Q3 2026) receives the Phase A+B measurement report and the Phase C trigger decision as inputs; brainstorm output is referenced in v3 kickoff agenda. *(forcing function alignment)*

## Risks

- **R1** (severity: MEDIUM) — **Partners reject Phase B as "not what we asked for"** even if it solves the measurable pain. *Mitigation*: engage early in Phase B; if they explicitly need GraphQL specifically, Phase C trigger is satisfied — for known reasons (FR5 trigger b), not for anticipated ones.
- **R2** (severity: MEDIUM) — **v3 planning produces a foundation requirement that requires GraphQL but Phase A+B has not yet built it.** *Mitigation*: FR5 trigger c covers this; Phase C contingency design is design-grade ready (per FR4), so Phase C engineering can start immediately after v3 decision without re-planning.
- **R3** (severity: MEDIUM) — **HTTP/2 + cache tuning underdelivers in production** (e.g., the over-fetching is payload-size-dominated rather than round-trip-dominated). *Mitigation*: AC2's "attributable per-cause" requirement surfaces this empirically; if payload size is the dominant cost, Phase B sparse-fields is the targeted answer; if neither addresses the pain, Phase C trigger condition (a) is met.
- **R4** (severity: LOW) — **Phase C, if triggered, costs more than starting GraphQL today would have.** *Acknowledged*; the trade-off is paying only if needed, with better-targeted scope and team competence.
- **R5** (severity: LOW) — **Senior-engineer hire for Phase C is slow.** *Mitigation*: if Phase C trigger looks likely by end of Phase A measurement, begin sourcing in parallel.

## Open Questions (for design phase)

- **OQ1** — **Schema governance ownership** (if Phase C triggers): who owns "the schema"; what's the deprecation policy; how do we avoid the Walmart-Labs partner-graph-divergence pattern? *Not resolvable in this brainstorm; design phase decides.*
- **OQ2** — **Phase C technology choice** (if triggered): Apollo GraphOS (managed, vendor-locked, fastest operational ramp) vs Yoga + Mesh (OSS, more assembly, more flexibility) vs Hasura (database-first, less aligned with "wrap existing REST"). *Design phase decides with measurement data in hand.*
- **OQ3** — **Versioning model under GraphQL** (if Phase C triggers): URL-path versioning is REST-native; GraphQL deployments more commonly use schema-evolution + deprecation. *Design phase decides; partner ecosystem affects choice.*

## Out of Scope (explicit)

- Removal of REST API. *(seed C: not in planning horizon)*
- Forcing public-developer segment (~25% of traffic) onto GraphQL. *(Architect agreed; Backend agreed; not contested)*
- A built-and-running GraphQL gateway as an outcome of this brainstorm. *(merged plan: this is Phase C, gated.)*
- Walmart-Labs-style federated graph with per-partner contracts as a v1 outcome. *(deferred to design phase if Phase C triggers.)*

## Provenance

| Requirement | Origin |
|---|---|
| FR1 (Phase A: HTTP/2 + cache tuning) | Backend Phase A; ratified by Architect in debate |
| FR2 (Phase B: REST sparse-fields) | Backend Phase B; partner-engagement framing from debate Tension 4 |
| FR3 (Phase B partner pilot question) | Debate Tension 4 resolution |
| FR4 (Phase C contingency design) | Architect Phases 0-2 retained as contingency |
| FR5 (Phase C trigger conditions) | Merged plan structure |
| FR6 (Phase C tech choice deferred) | Debate Tension 3 resolution |
| FR7 (Phase C operational preconditions) | Debate Tension 2 resolution |
| NFR1-NFR2 (auth + backward compat) | Seed brief constraints |
| NFR3 (latency improvement target) | Backend measurement framing |
| NFR4 (no breaking changes) | Seed brief |
| NFR5 (measurement-before-behavior-change) | Backend Phase A baseline requirement |
| NFR6 (persisted-queries-only for partners) | Both proposals agree |
| AC1-AC6 | Mapped above; AC6 ties to seed forcing function |
| R1 (partners reject Phase B) | Backend Phase B own risk |
| R2 (v3 forces GraphQL before built) | Architect critique of measurement-first |
| R3 (HTTP/2 tuning underdelivers) | Phase A trigger to escalate |
| R4 (Phase C costlier if delayed) | Backend acknowledged trade-off |
| R5 (slow hire) | Architect mitigation, sequencing |
| OQ1-OQ3 | Carried forward to design phase |

## Handoff to Design

This brainstorm outputs a phased measurement plan with a Phase C contingency. The `--handoff design` action produces a design brief (`handoff/design-brief.md`) instructing the design agent to:

1. Produce detailed Phase A instrumentation design (the load-bearing data-collection step).
2. Produce a Phase B sparse-field schema design for the top 12 endpoints (JSON:API vs OpenAPI 3.1 extension trade-off).
3. Produce a Phase C **contingency** architecture (GraphQL gateway shape, schema governance plan, persisted-queries-only operational model) ready to trigger if FR5 conditions are met.

The design output is text-only — no code, no infrastructure changes. It is the input to v3 planning in Q3 2026.
