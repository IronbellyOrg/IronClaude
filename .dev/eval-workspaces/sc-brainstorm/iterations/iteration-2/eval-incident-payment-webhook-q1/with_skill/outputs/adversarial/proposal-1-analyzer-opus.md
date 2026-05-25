---
proposal_id: 1
persona: analyzer
model: opus
lens: cross-incident root-cause pattern detection, evidence-based reasoning
---

# Proposal 1 — Analyzer (opus): The Common Root Cause Is Unowned Observability, Not Three Different Bugs

## Position

All three Q1 PIRs name a different proximate cause (Redis lag, DB pool exhaustion, DLQ crash-loop). All three miss the **common upstream signal**: webhook-delivery-latency P99 drifted upward for ~36 hours before each incident, and the metric had no owner, no dashboard, no alert. The proximate causes are symptoms; the root cause is **structural blindness** in the on-call surface. Fix the structural blindness and the next three incidents — different proximate causes again — show up on a dashboard 24-36h before they page.

## Required investigation steps

1. **Re-PIR each incident with the latency-drift series in hand.** Pull the 7 days preceding each Sev-2, overlay P99-latency, retry rate, DLQ growth, and merchant-side response-time distributions. Confirm or falsify the "36-hour upstream signal" hypothesis empirically before building remediations on top of it.
2. **Build a unified "webhook health" timeline** for Q1 — latency P50/P99, retry rate, DLQ size, merchant error rate (4xx vs 5xx split), per-merchant top-10 contributors. This is the dataset that should have been on the on-call's screen for the last year.
3. **Audit metric ownership across the platform**, not just webhooks. The pattern "metric exists, no owner, no alert" is almost certainly not isolated to webhook latency. Treat this incident as a leading indicator for a platform-wide observability-ownership gap.
4. **Cross-reference merchant-side reconciliation logs** with our delivery records for the 412 affected merchants. The 200-OK-then-drop pattern (Q8) means our "delivered" count is over-counted by an unknown margin — the PCI evidence chain claim is structurally weaker than we've been telling auditors.

## Architectural remediations (ranked by leading-indicator power)

- **R1 (highest leverage)** — **Latency-drift alert on P99 webhook-delivery-latency.** +25% over a 7-day rolling baseline, sustained 30 minutes, pages on-call with a runbook link. This single alert would have given 24-36 hours of lead time on all three Q1 incidents. Cost: ~2 engineer-days (PromQL + alert routing + runbook stub).
- **R2** — **Per-merchant delivery-percentile observability.** Surfaces the 200-OK-then-drop pattern by making "merchant claims they didn't get it" a debuggable query, not a manual reconciliation. Cost: ~1 engineer-week (per-merchant labels are high-cardinality; needs a sampling strategy).
- **R3** — **DLQ size as a Prometheus gauge with alert at 100K and 500K thresholds.** The Mar 27 producer back-pressure happened at ~2M rows; we need to be alerted three orders of magnitude before that. Cost: ~0.5 engineer-day.
- **R4** — **Webhook-health dashboard adopted by the on-call as the primary surface for this system.** Not just "available", but defaulted-to-on-call-screen-from-page. Cost: ~3 engineer-days (dashboard + on-call workflow change).

## What I'd push back on

A remediation plan that focuses on the three named proximate causes (rewriting the Redis-streams consumer, tightening the DB pool config, adding a parser limit to the DLQ) is treating the symptoms. Those fixes are worth doing, but as **second-priority follow-ups**, not the headline of this remediation. The Engineering Director's instinct ("you keep telling me each incident is different and they're not") is correct, and the answer should match the question.

## Confidence

High on the latency-drift pattern hypothesis (concrete data exists in the metric store, just unsurfaced). Medium on the per-merchant observability shape — high-cardinality metrics are easy to design badly. Lower on whether the structural fix is "metric ownership as RACI" vs "platform observability redesign"; that's a Refactorer / DevOps call.

## Cost

R1-R4 together: ~3 engineer-weeks. Single-quarter deliverable.
