---
proposal_id: 2
persona: backend
model: sonnet
lens: operational reality at scale, performance/caching, in-house expertise gap
---

# Proposal 2 — Backend: Solve The Over-Fetching Pain With REST Evolution + HTTP/2; Don't Buy a Multi-Quarter Operational Ramp We Don't Need

## Position

The architect frames the question strategically (v3 foundation) and arrives at "build a GraphQL gateway". I read the same seed brief and the same enrichment and arrive at: **solve the documented pain with REST evolution + HTTP/2 tuning first**, **then re-evaluate GraphQL with one quarter of operational data** rather than 6-9 months of architectural buildout. The strategic angle is real but it does not require committing to GraphQL *now*; it requires having a credible answer ready for Q3 planning. A credible "we measured, here's what helped, here's what didn't" is stronger v3 input than a fresh GraphQL gateway with 2 quarters of operational ramp ahead of it.

## Recommendation

**Three-phase exploratory plan, with each phase a real decision gate:**

- **Phase A — HTTP/2 + cache tuning + payload audit** (2-4 engineer-weeks). Measure first. The enrichment notes "~50% of the over-fetching pain" for screens dominated by round-trip latency is addressable here without any API surface change. Specifically: enable HTTP/2 multiplexing if not already, audit `Cache-Control` / `ETag` discipline on the 12 highest-traffic endpoints, eliminate any pathological N+1 patterns on the server side. **Cheap, no migration cost to clients, immediate measurement.**
- **Phase B — REST evolution to sparse-field/compound-document for the worst-offender endpoints** (6-10 engineer-weeks). Extend the 12 highest-pain endpoints to support `?fields[...]=...` selection (JSON:API or OpenAPI 3.1 style). Coordinate with the 2 partners who asked for GraphQL — give them a sparse-field implementation and measure satisfaction. **If they're happy: question answered.** Most likely outcome based on the enrichment's ~60%-of-pain estimate.
- **Phase C (gated)** — Only if Phase A + B leaves real, measured pain that REST evolution provably cannot address: build a focused GraphQL endpoint for the 3-5 specific queries that benefit most (the merchant-dashboard "6 endpoints in 1 call" style). Keep it first-party-clients-only first; expose to partners only after operational confidence is real. This is the architect's plan, **but only triggered by measured residual pain, not by strategic anticipation.**

## Why this shape

**The in-house GraphQL expertise gap is dominant operational risk.** Two engineers with prior experience + one small internal endpoint ≠ ready to run public-facing GraphQL at our partner traffic scale. Even with Apollo GraphOS, the *team* needs the operational competence to debug query-cost spikes at 3am, design schema deprecations, and have an opinion about N+1 patterns under load. **Operational competence is not buy-able.** The architect's "hire 1 senior engineer with public GraphQL operational experience before Phase 1" is one mitigation; the engineer market for that profile is thin and slow.

**The pain is concrete, not abstract.** "Mobile screen pulls from 6 endpoints" has a numeric answer: how many ms is that costing? How much of that ms is round-trip vs. payload size? **Measure before you architect.** I will be very surprised if the answer is "you must have GraphQL"; I will not be surprised if the answer is "HTTP/2 multiplexing + ETags + sparse fields buys you 80% for 10% of the cost".

**The Apollo cost is not the issue; the lock-in mindset is.** $30-60K/year is rounding error. The lock-in cost is *organizational*: once Apollo GraphOS is the integrating layer, every future API decision is filtered through "how does this fit the federated schema". That filter is appropriate when you know GraphQL is right; premature when you don't.

**The "v3 planning needs a clear answer" framing is a real but rebuttable concern.** v3 planning starting in Q3 does NOT need a built GraphQL gateway; it needs a *credible recommendation backed by measurement*. Phase A + B + (Phase C decision) is *that recommendation*, with the added benefit of being grounded in production data rather than hypothesis. If Phase A + B closes the pain, v3 input is "REST with sparse fields, here's the evidence" — a stronger position than "we built GraphQL because we thought we should, here's a 6-month operational ramp ahead of us".

## What I'd push back on

The architect's plan commits ~18 engineer-weeks + ongoing managed-gateway cost + a senior hire + 2 quarters of operational ramp, **before measuring whether the cheaper path closes the pain.** That's not architecture, that's procurement. The right architecture decision *includes the measurement that disconfirms the assumption*. Without Phase A + B as a gate, we are spending 9 months building an answer to a question we haven't asked precisely enough.

**Specific disagreement with the architect**: "Building the foundation now means v4 / v5 planning is unburdened" assumes GraphQL IS the foundation. If we measure and find REST + sparse fields is the foundation, the architect's plan has burdened v4 / v5 with a GraphQL gateway nobody needed. Optionality is preserved by *measuring*, not by *building*.

## Cost

- Phase A: 2-4 engineer-weeks. ~$0 incremental infra.
- Phase B: 6-10 engineer-weeks. ~$0 incremental infra.
- Phase C (if triggered): 8-12 engineer-weeks for a focused GraphQL endpoint, plus operational ramp. Possibly never triggered.

**Total to "ready for v3 planning": ~8-14 engineer-weeks worst case (Phases A + B), comfortably inside Q3 2026 forcing function with measurement in hand.**

## Risks

- **R1 (medium)** — Phase B is rejected by partners as "not what we asked for" even if it solves their measurable pain. *Mitigation*: engage early; if they explicitly need GraphQL specifically (not "fewer round-trips"), then Phase C becomes triggered, but for known reasons, not anticipated ones.
- **R2 (medium)** — Phase A + B may close partner-relationship messaging but leave the strategic v3 question open. *Mitigation*: v3 planning treats "REST with sparse fields" as a valid foundation; brainstorm output explicitly states "GraphQL deferred, conditions for revisiting documented".
- **R3 (low)** — Phase C, if triggered, has higher cost than starting GraphQL today would. *Acknowledged*; the trade-off is that you only pay it if it's actually needed.

## Confidence

High on Phase A's leverage (HTTP/2 + cache tuning is consistently underrated). High on Phase B's coverage (60%+ of REST over-fetching pain is sparse-field-addressable per industry norms). Medium on whether the 2 partners will accept Phase B specifically — that's where this proposal's risk concentrates.
