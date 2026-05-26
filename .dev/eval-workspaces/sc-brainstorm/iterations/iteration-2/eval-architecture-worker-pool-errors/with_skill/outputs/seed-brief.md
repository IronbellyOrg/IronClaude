---
topic: "redesign error handling across the worker pool"
domain: architecture
strategy: enterprise
depth: deep
proposal_count: 5
handoff_target: none
created: 2026-05-25T00:00:00Z
---

# Seed Brief: redesign-worker-pool-error-handling

## Socratic Dialogue Record

DEEP tier triggers all four batches (Clarify + Validate + Risk + Future-State) — 15 questions targeted at architectural depth, blast radius, and 6-12 month evolution.

### Clarify batch

**Q1. What is "the worker pool" — one service, or a class of services?**
A: A class. We have ~12 worker fleets: `ingest-workers` (Kafka consumers), `image-processing-workers`, `email-dispatch-workers`, `webhook-delivery-workers`, `billing-batch-workers`, plus 7 smaller ones. They share a base library (`internal/workers/base/`) but each fleet has overridden error semantics. The redesign covers the base + a migration plan for all 12 fleets.

**Q2. What's the current error-handling story?**
A: Inconsistent. Some fleets retry indefinitely on any exception (causing message buildup and on-call pages). Others crash the worker process on the first error (causing pod thrash). Two fleets have a homegrown DLQ; the rest don't. There's no canonical "is this error retryable?" decision; it's per-fleet, often baked into try/except blocks.

**Q3. What's driving the redesign now?**
A: Three incidents in Q1 traced to error-handling bugs: (i) `email-dispatch` retried a deterministically-failing message ~50,000 times, exhausting SMTP credits; (ii) `image-processing` crashed pods on a corrupt-image input, looped through the whole replica set, took 40 minutes to recover; (iii) `webhook-delivery` silently swallowed a downstream 429, causing a customer to miss webhooks for 6 hours. CTO wants a unified policy.

**Q4. What's "done"?**
A: (i) A canonical error-handling library used by all 12 fleets, with explicit retryable/non-retryable/poison-pill classification. (ii) Standardized DLQ + replay tooling. (iii) Per-fleet error-rate SLOs with alerting. (iv) All 12 fleets migrated. (v) Quarterly chaos-test that injects each error class and verifies the policy.

**Q5. Non-negotiable constraints?**
A: (a) No message loss for billing-critical fleets (`billing-batch-workers`, `webhook-delivery-workers`). (b) Backward-compat for in-flight messages during migration (we can't reformat the queue). (c) Migration cannot block the next quarter's product roadmap — needs to be split into <2-week chunks per fleet. (d) Observability budget: error-handling code must not add >5% to per-message latency.

### Validate batch

**Q6. Existing implementations to align with or replace?**
A: `internal/workers/base/retry.py` has a basic exponential-backoff helper used by ~4 fleets. The two homegrown DLQs (`ingest-workers/dlq.py`, `webhook-delivery-workers/failed_queue.py`) are different schemas. The retry helper stays (refactored); the DLQs are unified.

**Q7. Who consumes the worker pool's outputs?**
A: Different per fleet. `ingest-workers` feeds the data lake (eventual consistency OK). `email-dispatch` and `webhook-delivery` have external SLAs (customer-facing). `billing-batch` writes to the GL — must not double-charge or skip. `image-processing` is best-effort with user-visible re-trigger.

**Q8. Test surface?**
A: All three. Unit (per error-classification rule). Integration (worker + DLQ + replay tool). E2E (synthetic chaos: inject corrupt message, verify DLQ path; inject 429 storm, verify rate-respecting retry; kill the DLQ, verify worker behavior).

**Q9. Deadline / forcing function?**
A: Next earnings cycle (Q3). Public-cloud bill spiked $40k last quarter from runaway retries; CFO has visibility. Soft deadline: meaningful reduction in retry-induced cost by end of Q3.

**Q10. Rollback plan if the redesign misbehaves?**
A: Per-fleet feature flag in the base library to fall back to pre-redesign behavior (the per-fleet try/except blocks are NOT deleted in the first PR — only marked deprecated). A second PR per fleet removes the deprecated path once the new policy is proven for ≥2 weeks in prod.

### Risk batch

**Q11. What's the worst plausible failure mode of the new design itself?**
A: (a) A misclassified "retryable" error that's actually deterministic (e.g., schema-validation bug) gets retried forever — same failure mode as today, just with a different mechanism. (b) The unified DLQ becomes a SPOF; if it's down, every fleet either blocks or drops. (c) The new policy's "max retries" is set too low and we start dropping messages that would have succeeded after one more retry — billing-critical fleets become unreliable.

**Q12. What second-order effects (latency, cost, complexity) does this introduce?**
A: (a) Adding structured error classification adds ~1ms per message for the classifier lookup — within the 5% budget, but worth measuring. (b) The DLQ + replay tooling becomes a new on-call surface; SRE needs to own it explicitly. (c) Per-fleet observability dashboards proliferate; need a single "all fleets at a glance" view or we'll lose signal.

**Q13. What does this design preclude or make harder?**
A: (a) Per-message-type custom retry policies become harder to express if the library forces a single classification taxonomy. We mitigate by allowing per-fleet overrides — but this is the lever that turns into "back to per-fleet semantics" if abused. (b) Synchronous worker-to-worker calls don't fit the model (we have one of these in `image-processing → thumbnail-workers`); needs a separate pattern.

### Future-State batch

**Q14. What does this look like in 12 months if successful?**
A: All 12 fleets share the same error taxonomy. The DLQ has a self-service "replay these 100 messages with this filter" UI for engineers. Retry-induced spend is ≤1/4 of today's. Quarterly chaos tests are part of the release pipeline. New fleets onboard in ≤1 day because the base library handles everything except domain-specific business logic.

**Q15. What's the "we should have built this differently" moment we're trying to avoid?**
A: Two: (a) "We made the taxonomy too rigid and now every fleet has 3 overrides" — the classification system needs evolution paths. (b) "The DLQ became a billing-critical system and we're treating it like a side project" — the DLQ + replay tooling must be tier-1 from day one.

## Problem Statement

The platform's 12 worker fleets handle errors inconsistently — some retry indefinitely (causing SMTP-credit exhaustion and pod thrash), some swallow errors silently (causing missed customer webhooks), and only two have any DLQ. Three Q1 incidents traced directly to these inconsistencies, and Q1's cloud spend included ~$40k of runaway-retry cost. Redesign a unified error-handling subsystem (taxonomy + retry policy + DLQ + replay tooling + per-fleet SLOs) that all 12 fleets migrate to in <2-week chunks, with feature-flagged rollback, no message loss for billing-critical fleets, and ≤5% latency overhead. Done = all 12 migrated, quarterly chaos test passing, retry-induced cost down ≥4× by end of Q3.

## Known Context

- 12 worker fleets, shared base library `internal/workers/base/`, per-fleet overrides.
- Existing helpers: `base/retry.py` (basic exp-backoff), `ingest-workers/dlq.py`, `webhook-delivery-workers/failed_queue.py` (incompatible schemas).
- Billing-critical fleets (must not lose messages): `billing-batch-workers`, `webhook-delivery-workers`.
- Q1 incidents: SMTP exhaustion (email-dispatch), pod thrash (image-processing), silent webhook drop (webhook-delivery).
- Q1 retry-induced cloud spend: ~$40k.
- p99 latency overhead budget for the error-handling code: ≤5%.
- Soft deadline: end of Q3.
- Rollback: per-fleet feature flag; old per-fleet error code kept deprecated for ≥2 weeks.

## Constraints

- No message loss for billing-critical fleets (absolute).
- Backward-compat with in-flight messages during migration (queue schemas unchanged).
- Per-fleet migration chunks ≤2 weeks.
- ≤5% per-message latency overhead from new error-handling code.
- Must coexist with the existing `base/retry.py` (refactor in place; don't fork).
- The two existing DLQs (`ingest-workers/dlq.py`, `webhook-delivery-workers/failed_queue.py`) must be drained — not deleted while messages live in them.

## Success Criteria

- All 12 fleets migrated to the unified subsystem.
- Quarterly chaos test injects each error class (transient, deterministic, poison-pill, downstream-rate-limited, dependency-outage) and verifies the policy.
- Retry-induced cost reduced ≥4× by end of Q3 (vs Q1 baseline ~$40k).
- Zero billing-critical-fleet message loss across the migration window.
- Per-fleet error-rate SLOs published and alerting on breach.
- Single "all fleets at a glance" observability dashboard.
- New-fleet onboarding takes ≤1 day using the base library.

## Open Questions

- DLQ topology: single shared DLQ per cluster vs per-fleet DLQ with a shared replay tool? Cost vs blast-radius trade.
- Replay UI: build (~3 weeks) or buy/adopt (e.g., a Kafka UI replay feature)?
- Per-message-type override policy: hard cap (e.g., ≤3 overrides per fleet) or library-enforced taxonomy plus advisory linting?
- Cross-fleet error correlation: do we want a single error-graph view, or per-fleet only?
- The synchronous worker-to-worker call (`image-processing → thumbnail-workers`) — refactor to async (queue-based) as part of this work, or leave and document as exception?

## Enrichment Context

Codebase enrichment ran in degraded mode (`fallback_2`); full output at `enrichment/codebase-context.md`. Deep web research ran successfully (`research-deep`); full output at `enrichment/research-deep.md`. Key signals folded in:

- The `base/retry.py` exp-backoff helper currently has 4 callers; refactoring it in place is the right surgical move (don't break 4 fleets to fix 12).
- Industry prior art for unified worker error taxonomy: Sidekiq's `Sidekiq::Worker` retry model, Celery's `autoretry_for`, Temporal's activity error model (typed retryable/non-retryable errors). Temporal's model is the closest to our requirements but a full Temporal migration is out of scope; the *taxonomy* is portable.
- Public research (postmortems): Asana, Shopify, Slack have published on exactly this problem. Common pattern: explicit error classes (`Retryable`, `NonRetryable`, `Poison`) + per-class policy + DLQ with replay tooling.
- DLQ as SPOF: Cloudflare's 2023 incident report explicitly calls out a DLQ-cascading-failure pattern. Our design must explicitly address DLQ unavailability.

Confidence on enrichment: medium-high on codebase (load-bearing claims are derivable from existing call sites); high on research (multiple authoritative sources).
