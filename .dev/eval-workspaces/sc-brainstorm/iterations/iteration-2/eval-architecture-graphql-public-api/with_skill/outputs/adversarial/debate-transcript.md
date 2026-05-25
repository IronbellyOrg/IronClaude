---
debate_round: 1
proposals: [proposal-1-architect, proposal-2-backend]
convergence_score: 0.62
adversarial_status: pass
---

# Adversarial Debate Transcript — GraphQL for Public API

Two proposals, sharp disagreement on the **same axis**: should we commit to GraphQL as v3 foundation now (Architect), or measure first and let evidence drive the v3 conversation (Backend)? The disagreement is genuine and load-bearing; both proposals are internally coherent and well-grounded.

## Tension 1 — Strategic Commitment vs Measurement Discipline

**Architect's position**: v3 planning starts in Q3 2026; we want a built-and-running GraphQL gateway in hand so the v3 conversation can be "REST stays for public long-tail, GraphQL is the foundation for partners and first-party" rather than "should we have GraphQL?". Build now; the strategic angle dominates.

**Backend's position**: v3 planning needs a *credible recommendation backed by measurement*, not a built gateway. Phase A (HTTP/2 + cache tuning) + Phase B (REST sparse-fields) measures whether the documented over-fetching pain is actually GraphQL-shaped. If it isn't, we will have saved 6-9 months and ~$60K/year. If it is, Phase C builds a focused GraphQL endpoint, triggered by evidence rather than anticipation.

**Resolution**: **Backend's measurement discipline wins as the lead, but the Architect's strategic framing is correctly weighted into the recommendation.** Merged plan:

- **Now → Q2 end**: Phase A (HTTP/2 + cache tuning + payload audit). Cheap, fast, measurement-producing. ~2-4 engineer-weeks.
- **Q2 → Q3 start**: Phase B (REST sparse-fields on top 12 endpoints, partner pilot). ~6-10 engineer-weeks. **Partner engagement is the load-bearing step.**
- **Q3 v3 planning kickoff**: bring measured data + partner feedback into v3 conversation. If Phase A+B closes ≥70% of partner-reported pain and partners are satisfied with the REST evolution: v3 is "REST + sparse fields + persistent improvement". If partners explicitly require GraphQL specifically (not "fewer round-trips"), OR if measured residual pain is structurally GraphQL-shaped: Phase C is triggered.
- **Phase C (if triggered, post-v3 planning)**: build the focused GraphQL endpoint per Architect's plan; possibly with Apollo GraphOS, possibly with Yoga + Mesh, depending on what we learned from Phase A+B about which 3-5 queries are the real targets.

## Tension 2 — In-House Expertise: Solvable Or Dominant Risk?

**Architect's position**: Operational ramp is the dominant risk; mitigation is hiring 1 senior engineer with public GraphQL operational experience + partnering with Apollo PS.

**Backend's pushback**: That engineer-profile is thin in the market AND operational competence is a team-level property, not a single-hire property. Even Apollo GraphOS doesn't eliminate the need for the team to have 3am-debugging competence on query cost spikes, schema deprecations, N+1 patterns.

**Resolution**: **Backend wins the framing; Architect's mitigation is necessary-but-not-sufficient.** If Phase C is triggered, the senior hire is a precondition for Phase C launch, not a parallel activity. Apollo PS engagement is also required if Phase C uses Apollo GraphOS. Phase A + B do not require either, so the in-house expertise question is deferred until the GraphQL-shape need is confirmed.

## Tension 3 — Vendor Lock-In: Acceptable Trade Or Premature Commitment?

**Architect's position**: Apollo GraphOS lock-in is the deliberate cost we pay for operational velocity; portable away to OSS Router if needed.

**Backend's position**: $30-60K/year is cheap; the *organizational* lock-in (every future API decision filtered through "how does this fit the federated schema") is the cost — premature when we haven't confirmed GraphQL is the foundation.

**Resolution**: **Defer the question until Phase C trigger.** If Phase C is triggered, evaluate Apollo GraphOS vs Yoga + Mesh vs Hasura at that point, with one quarter of operational data and a more precise understanding of which queries matter. Locking in now is premature; the question is good-but-future.

## Tension 4 — Partner Satisfaction: REST-Sparse-Fields Or "GraphQL Specifically"?

**Architect's implicit position**: Partners asked for GraphQL specifically; honoring that ask is the path to partner satisfaction.

**Backend's explicit position**: Partners asked for "fewer round-trips on our mobile clients"; the *solution* they named (GraphQL) is one of several. Measure satisfaction with the cheaper solution (REST sparse-fields, addresses ~60% of over-fetching pain per the enrichment) before assuming the named solution is the required one.

**Resolution**: **This is the operational crux of Phase B.** Partner engagement in Phase B must explicitly ask: "If sparse-field REST closes 80% of the round-trip pain, is that sufficient, or is GraphQL specifically a hard requirement?" Their answer determines whether Phase C is triggered. Both proposals agree this is the correct question; they disagree on whether to ask it before or after building.

## Remaining disagreements (logged for transparency)

- **Persisted-queries-only vs ad-hoc for partners**: if Phase C is triggered, both proposals agree on persisted-queries-only for the public partner surface. No tension on this sub-question.
- **Schema governance ownership**: if Phase C is triggered, both proposals identify this as a real concern; neither has a confident answer for our org structure. Carried forward as open question for the design phase.
- **First-party vs partner exposure ordering for Phase C**: Architect wants first-party first then partners; Backend agrees if Phase C is triggered. No tension.

## Convergence rationale

Two proposals, four tensions, all resolved with explicit positions. The merged recommendation is **Backend's phased measurement plan WITH the Architect's Phase C contingency design ready to trigger**. This preserves the strategic option the Architect rightly identifies (v3 can land on GraphQL) without paying the up-front cost the Backend rightly questions (commitment before evidence). Both proposals would accept this merged shape; that's the convergence signal.

Convergence score **0.62** — solid PASS for a 2-proposal exploratory brainstorm. Lower than a same-topic 3-or-5-proposal run might score because the structural disagreement (build-now vs measure-first) is genuine, and the merge resolves by sequencing rather than synthesis. Open questions reduced from 5 in seed brief to 3 in merged.

This is exactly the shape `--handoff design` is for: the design phase takes "measurement plan + Phase C contingency design" as its input and produces a more detailed architecture for whichever path lands.
