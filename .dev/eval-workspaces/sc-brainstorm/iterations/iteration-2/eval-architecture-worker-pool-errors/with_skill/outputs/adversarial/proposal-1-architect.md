---
proposal_id: 1
persona: architect
model: opus
lens: long-term system fit, extensibility, future-proofing
---

# Proposal 1 — Architect: Typed-Error Subsystem with Per-Fleet DLQ + Shared Replay Plane

## Position

Build an `internal/workers/errors/` subsystem as a tier-1 platform concern, not a base-library helper. The subsystem owns: (a) the typed-error taxonomy, (b) a per-fleet DLQ contract, (c) a shared replay plane (CLI day-one, web UI follow-up), (d) per-fleet SLO templates, (e) chaos-test scaffolding. The 12 fleets become *consumers* of this subsystem, each migrating by replacing fleet-local try/except sprawl with subsystem calls.

## Architecture

Five components under `internal/workers/errors/`:

1. **`taxonomy.py`** — typed error classes: `RetryableError`, `NonRetryableError`, `PoisonError`. Each carries `cause`, `context`, `attempt_number`. Supports Stripe-style attempt-bounded retryability: `RetryableError(promote_after_attempts=3)`.

2. **`policy.py`** — per-fleet retry policy (exponential backoff with jitter, max attempts, max wall-clock retry window). Refactors `base/retry.py` in place (preserves 4 existing callers; no breaking change).

3. **`dlq.py`** — `DLQClient` interface with two implementations: `KafkaDLQ` (for fleets already on Kafka, matches the `ingest-workers` shape) and `PostgresDLQ` (matches `webhook-delivery-workers` shape). Both write the same envelope schema. Drains the old DLQs by replaying them through the new client during migration.

4. **`replay.py`** — replay engine, DLQ-shape-agnostic. CLI invocation day one (`python -m workers.errors.replay --fleet=email-dispatch --filter='error_class=RetryableError'`). Audit log writes via `internal/audit/event_log.py` (existing).

5. **`chaos.py`** — chaos-test harness with fixture helpers: inject-poison-message, inject-429-storm, kill-dlq. Integrates with the existing `chaos/network/` test pattern.

## Why this shape

**Per-fleet DLQ + shared replay plane** matches the industry consensus surfaced in `research-deep.md` (Shopify, Slack, Asana 2024). Shared DLQ is rejected on Cloudflare-2023 grounds (cross-fleet blast radius). The replay plane is shared because operators don't want to learn 12 different replay tools.

**Typed-error subsystem, not a function library.** The 140 try/except blocks aren't replaced one-to-one — they're refactored into `raise NonRetryableError(...)` / `raise RetryableError(...)` calls at the *source* of the error, and a single catch-classify-route block at the worker loop boundary. This is a structural change, not a sprinkle of helpers.

**Refactor `base/retry.py` in place** to avoid forking. The 4 existing callers get a same-shape API with the new policy semantics underneath. No big-bang breakage.

## Per-fleet migration shape

Per-fleet PR (≤2 weeks per the constraint):

1. Adopt subsystem in the fleet's `worker.py` entrypoint (feature-flagged off).
2. Refactor try/except blocks to typed-error raises.
3. Wire fleet's DLQ to `dlq.py` (drain old DLQ in same PR if applicable).
4. Add per-fleet SLO + alert.
5. Flip feature flag in canary, soak ≥2 weeks, flip in prod, remove deprecated path in follow-up PR.

12 fleets in 3 quarters at 2 fleets parallel per sprint = feasible by end of Q4 (one quarter past Q3 soft deadline). Q3 milestone: top-5 fleets (the billing-critical ones + the 3 that had incidents) migrated.

## Cost

~6-8 engineer-weeks for the subsystem itself. ~2-3 engineer-weeks per fleet migration × 12 = ~30 engineer-weeks. Total ~9 engineer-months spread over 2-3 quarters with 2-3 platform engineers.

## What I'd push back on

Any proposal that says "just put a try/except in the base loop and call it done" is solving the symptom (worker crashes) and not the system (140 try/except sprawl, incompatible DLQs, no replay tooling, no chaos coverage). The Q1 incidents prove we need taxonomy + tooling, not better error suppression.
