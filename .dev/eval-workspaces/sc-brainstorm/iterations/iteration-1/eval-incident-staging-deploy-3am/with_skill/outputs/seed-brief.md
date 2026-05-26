---
topic: "post-mortem: staging deployment broke at 3am, manual revert was the only mitigation"
domain: incident
strategy: systematic
depth: quick
proposals_target: 2
handoff_target: none
created: 2026-05-25T00:00:00Z
---

# Seed Brief: post-mortem-staging-deploy-3am

## Problem Statement

A staging deployment at approximately 03:00 local time broke the staging
environment. The only effective mitigation was a manual revert performed
by the on-caller. This post-mortem must reconstruct the timeline,
identify the root cause and contributing factors, and surface the
detection and recovery gaps that turned an off-hours deploy into a
hand-rolled rollback.

## Known Context

- Failure occurred in the staging environment during an off-hours
  (~03:00) deployment window.
- Detection-to-mitigation path depended on a human operator; no
  automated rollback path was exercised.
- Manual revert succeeded, indicating the previous build was known-good
  and reachable.
- Scope of impact (which services, downstream consumers, data writes)
  is not yet established and is an Open Question.

## Socratic Dialogue Answers (incident — Clarify batch, quick tier)

1. **When did it start? When was it detected? When was it resolved?**
   Started at ~03:00 with the deploy. Detection time is uncertain
   (likely several minutes to tens of minutes after the deploy completed
   based on the on-call lag). Resolution followed the manual revert,
   which is plausibly 30-90 minutes after first failure.
2. **What's the user-visible impact?**
   Staging-only — no end-user impact, but blocked the staging gate for
   any team relying on it for verification (QA, integration test
   suites, downstream service contract checks).
3. **Was this a single event or a pattern?**
   Treated as a single event for this post-mortem, but recurrence risk
   is explicitly an Open Question — similar revert-only mitigations in
   prior deploys would escalate priority of structural prevention.

## Constraints

- Staging-environment scope means lower urgency for customer comms but
  high urgency for engineering velocity (other teams blocked).
- Manual revert as the only known mitigation indicates an
  automated-rollback gap that must be addressed.
- Post-mortem must be blameless and produce actionable prevention items,
  not just narrative.

## Success Criteria

- Timeline reconstructed with timestamps for: deploy start, first
  failure signal, detection, on-caller engagement, revert initiation,
  revert completion, all-clear.
- Root cause identified with supporting evidence (logs, metrics, diff
  of the deployed change vs. last-known-good).
- At least one detection gap and one automated-recovery gap named with
  owner + due date.
- Prevention items prioritized by leverage (catches future incidents of
  the same class, not just this one bug).

## Open Questions

- What changed in the deploy — code, config, infra, or dependency?
- What was the blast radius (which services / data writes) and is any
  staging data corrupted or merely unavailable?
- Was the failure deterministic or load/timing-dependent?
- Has this category of failure (revert-only mitigation) happened before
  in the last 90 days?
- Why did the deploy happen at 03:00 — scheduled, accidental trigger,
  or chasing a previous failed deploy?

## Enrichment Context

`enrichment_used: [{source: codebase, quality_tier: skipped}]` — the
incident topic is hypothetical for this run; there is no concrete
codebase artifact to scan against. Codebase enrichment intentionally
skipped per Wave 2A routing matrix (no `--codebase` force flag, no
real incident artifacts to ingest).
