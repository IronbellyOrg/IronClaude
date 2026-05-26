---
proposal_id: 2
persona: analyzer
model: sonnet
lens: cross-incident pattern detection, alternative root-cause framing
---

# Proposal 2 — Analyzer (sonnet): The Common Root Cause Is Architectural — Three Tiers of Retry Hide Three Tiers of Cascading Failure

## Position

I read the same evidence as Proposal 1 and reach a different root cause. The latency-drift signal is real, but it's a **leading indicator** — not a root cause. The actual root cause is **architectural**: a three-tier retry pipeline (in-process → Redis Streams → PostgreSQL DLQ) where each tier's failure cascades into the next, amplifying the original disturbance into a Sev-2. Add all the observability you want; if the architecture amplifies disturbances by design, you will alert faster and still page at 3am.

## Required investigation steps

1. **Trace each Q1 incident through the three retry tiers** with timestamped queue depths. I predict you will see the same shape every time: small disturbance at tier-1 → tier-1 backlog → producers (the API handlers) blocked → tier-2 fills with whatever tier-1 spills → tier-3 (DLQ) becomes the safety valve and is itself unbounded.
2. **Model the system as a flow-control problem.** Each tier has a finite throughput; cascading failure happens when an upstream tier's max-output exceeds the downstream tier's max-input. Compute the actual ratios from production data. I expect they're 5-10× the design assumptions on Mondays.
3. **Audit the merchant-side pathologies as adversarial inputs, not bugs.** The 200-OK-then-drop and auth-rotation merchants are not edge cases; they are the steady-state behavior of N% of merchants and the system should be designed to absorb them rather than treat them as anomalies.
4. **Investigate whether per-merchant queue isolation would have prevented any of the three incidents.** I suspect Jan 18 (large-merchant spike) yes, Feb 9 (slow query) no, Mar 27 (malformed payload) yes. Two out of three is meaningful.

## Architectural remediations (ranked by structural impact)

- **R1** — **Per-merchant queue isolation (bulkhead pattern).** One bad merchant cannot starve the others. The Jan 18 large-merchant spike becomes a one-merchant slowdown instead of a system-wide Sev-2. Cost: ~4 engineer-weeks (queue routing + capacity allocation + per-merchant metrics — large because it touches the dispatcher core).
- **R2** — **Bounded DLQ with explicit overflow policy.** TTL = 7 days, max size = 500K rows, overflow policy = oldest-evicted-with-audit-log-entry. The "no TTL, no compaction" status quo IS the structural bug Mar 27 exposed. Cost: ~1 engineer-week.
- **R3** — **Back-pressure from each tier to its upstream.** When tier-2 is at 80% capacity, tier-1 throttles. When DLQ is at 80% of its max-size, tier-2 throttles. Failure surfaces upstream where it is observable and recoverable, instead of cascading into a system-wide Sev-2. Cost: ~3 engineer-weeks.
- **R4** — **Latency-drift alert** (Proposal 1's R1). Agreed and adopted as-is, but in this framing it is a leading indicator on the structural-fix progress, not a root-cause remediation in itself.

## What I'd push back on

Proposal 1's framing is correct as far as it goes — observability ownership IS a real gap and the latency-drift alert IS the cheapest high-leverage fix. But naming "unowned observability" as the root cause sets up a remediation that will give you 36 hours of warning before the next 3am page **for the same incident pattern that would have paged you anyway**. Better warning is not the same as fewer incidents. The architecture has to absorb the disturbances, not just announce them earlier.

## What I'd concede to Proposal 1

If forced to ship only one thing in Q2, ship R1 from Proposal 1 (the latency-drift alert). It's cheap, it's high-leverage as a stopgap, and it gives the team breathing room to do the architectural work in Q3 without another 3am page. But "ship only one thing" is the wrong frame — the architectural work and the observability work are complementary, not alternatives.

## Confidence

Medium-high on the cascading-failure framing. Lower on the specific cost estimates for R1 and R3 — these are real engineering projects that will turn up unknowns. The bulkhead pattern is well-established (Hystrix, Resilience4j, every payments platform that's been bitten by this); applying it here is not novel, it's overdue.

## Cost

R1-R4 together: ~2 engineering-quarters of work for a team of 2 dedicated engineers. Not single-quarter. This is the honest answer; treating it as smaller will produce another Mar 27.
