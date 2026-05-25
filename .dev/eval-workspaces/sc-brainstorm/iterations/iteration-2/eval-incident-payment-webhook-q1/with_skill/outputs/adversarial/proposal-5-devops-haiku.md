---
proposal_id: 5
persona: devops
model: haiku
lens: SLO contracts, runbook, rollout safety, on-call readiness
---

# Proposal 5 — DevOps (haiku): The Organizational Surface — Runbook, On-Call, SLO Contract — Is the Half of This Story Nobody Else Has Written

## Position

Proposals 1-4 cover the technical surface: observability gaps (P1), architectural amplification (P2), compliance evidence chain (P3, P4). All true; none of them by themselves fix the **3am page** problem. The 3am page happens because (a) the runbook is 3 years old, (b) half the on-call rotation has never solo-triaged this surface, (c) the SLO contract with merchants creates incentives that don't match the operational reality. Ship the best architecture in the world; if the people on-call at 3am cannot operate it, you will still be paging the EM.

## Required investigation steps

1. **Runbook drift audit.** What's in the current 3-year-old runbook vs. what the system actually does today? I predict large gaps on Redis Streams (added 2 years ago), the DLQ replay procedure (added 18 months ago), and the per-merchant kill switch (added in Q4 last year). Each gap is a 3am-paging surface.
2. **On-call competence audit.** For each of the 4 rotation members, when did they last touch this system? Tabletop or real? **Score honestly** — escalation to EM is a quiet "this rotation doesn't actually work" signal that has been ignored.
3. **SLO contract reality check.** Public docs say 60s/99%; enterprise contracts say 30s/99.9%; actual P99 in Q1 was significantly worse on the three incident windows AND quietly worse than public docs claim during the "good" weeks. **What we promise** vs **what we measure** vs **what we deliver** is a three-way mismatch and each contracting team should know it.
4. **Rollout-safety audit on the remediations being proposed.** Each Proposals 1-4 remediation needs a per-region, per-merchant, feature-flagged rollout plan with a documented rollback. A remediation that ships without one is itself an incident-in-waiting.

## Required remediations

- **D1** — **Runbook rewrite, owned and dated.** Step-by-step for each of the three Q1 incident patterns. Each step has an expected output. Each runbook entry has a "last verified by tabletop" date. Older than 6 months = stale = paged for re-verification. Cost: ~2 engineer-weeks initial + ongoing rotation.
- **D2** — **Quarterly tabletop drills.** Each rotation member must solo-triage a simulated Q1-pattern incident within 2 quarters of joining the rotation. Failure = additional training, not rotation removal. Cost: 1 engineer-day per drill per quarter.
- **D3** — **SLO contract alignment.** Public docs → measure what we promise (P99/30s for Tier-1, P99/60s for the rest). Internal dashboards → display the same number a merchant sees. Quarterly review of contracted SLOs vs. delivered. Cost: ~1 engineer-week for the dashboard alignment; the contract rewrite is a CS/Legal cost outside engineering scope.
- **D4** — **Per-merchant SLO observability** (overlaps with Proposal 1 R2 and Proposal 3 S2). Each Tier-1 merchant has a self-service dashboard showing **their** delivery percentile. Removes the "we say 99.9%, you say we missed three" debate. Cost: shared with P1/P3 — ~1 engineer-week marginal.
- **D5** — **Rollout playbook for all remediations.** Per-region (US-East → US-West → EU → APAC, 1 week minimum between regions), feature-flag-gated, with shadow-mode for any path-changing remediation. Define rollback triggers explicitly: "rollback if P99 increases > 10%, if DLQ growth rate increases > 2x, or if any merchant files a kill-switch request within 24h of region rollout." Cost: ~3 engineer-days per remediation rollout, amortized.
- **D6** — **Owner field on every dashboard panel and alert.** No metric without an owner. RACI documented in the on-call workspace. Quarterly review. The structural fix Proposal 1 implies but doesn't operationalize. Cost: ~1 engineer-week initial sweep.

## What I'd push back on

Proposals 1-4 are well-written technical proposals from teams that get to leave at 6pm. The reality is that the value of each technical fix is gated on whether the on-call at 3am can use it. A latency-drift alert with no runbook entry tells the engineer "something is wrong" and not "here's the next 5 steps". A bulkhead architecture with no rollout playbook becomes the source of the next Sev-2. The compliance fix is meaningless if the operator who has to access the DLQ at 3am for a customer-success escalation can't find the access-logging procedure.

## What I'd concede

Every technical recommendation in P1-P4 should ship. My contribution is the **wrapper** around them — operability is not "polish", it is "whether the engineering work landed."

## Confidence

High on every recommendation. The on-call competence audit is the one that gets political; the EM should pull it personally rather than asking the rotation members to self-assess.

## Cost

D1-D6 together: ~5 engineer-weeks of platform engineering + ongoing rotation overhead (~5% of on-call's time, recurring). Cross-functional cost: customer-success owns merchant SLO communication; legal owns the contract rewrite. Total org cost: less than a single Sev-2 incident response.
