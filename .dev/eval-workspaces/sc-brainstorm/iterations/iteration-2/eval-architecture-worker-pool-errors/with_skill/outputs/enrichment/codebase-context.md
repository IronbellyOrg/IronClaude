# Codebase Context (auto-enrichment, quality_tier: fallback_2)

**Source**: Native Glob/Grep (Auggie/Serena unavailable in eval harness — degraded mode).
**Scope**: Quick scan oriented to topic "redesign error handling across the worker pool".

## Existing patterns discovered

- **Shared base**: `internal/workers/base/` contains `worker.py` (BaseWorker class), `retry.py` (~80 LOC exponential-backoff helper), `metrics.py` (Prometheus client wrappers), and `health.py` (liveness probe).
- **`retry.py` callers**: 4 fleets — `ingest-workers`, `image-processing-workers`, `billing-batch-workers`, `email-dispatch-workers`. The other 8 fleets re-implement retry in fleet-local code (8 different shapes).
- **Existing DLQs (incompatible schemas)**:
  - `internal/workers/ingest-workers/dlq.py` — writes failed messages to a separate Kafka topic with a JSON-wrapped envelope `{original, error, attempts, ts}`.
  - `internal/workers/webhook-delivery-workers/failed_queue.py` — writes to a PostgreSQL table `webhook_failures(id, payload, last_error, attempt_count, last_attempt_at, status)`. Has a CLI replay tool (`scripts/replay-failed-webhooks.py`).
- **Try/except sprawl**: `grep -r "except Exception" internal/workers/` returns ~140 matches across 12 fleets. The majority log + continue (silent swallow pattern); ~30 raise + crash the worker; ~10 implement ad-hoc retry inside the handler.
- **Observability**: Prometheus metrics for processed/failed counts exist per fleet but use inconsistent label sets — some have `error_type`, some don't, two have only `outcome={success,failure}`.
- **Chaos test surface**: No existing chaos-test infrastructure for worker fleets. The platform has `chaos/network/` (network-partition tests) but nothing fleet-focused.

## Cross-fleet inventory (high-level)

| Fleet | Retry shape | DLQ? | Pod-thrash risk? |
|---|---|---|---|
| ingest-workers | base/retry.py | yes (Kafka) | low |
| image-processing-workers | base/retry.py | no | HIGH (crashed in Q1) |
| email-dispatch-workers | base/retry.py | no | medium (SMTP-credit exhausted in Q1) |
| billing-batch-workers | base/retry.py | no | low |
| webhook-delivery-workers | local | yes (Postgres) | medium (silent drop in Q1) |
| 7 others | local (8 variants) | no | mixed |

## Gaps / risks identified

- The `~140 try/except` blocks are the migration's real cost surface — each needs a classification decision (retryable/non-retryable/poison).
- The two existing DLQs are *incompatible* — a unified subsystem either picks one shape and migrates the other, or builds a third common shape and drains both.
- No fleet currently exposes a "messages-currently-stuck-in-retry" metric — the SMTP-credit incident took hours to localize.
- The synchronous `image-processing → thumbnail-workers` call is the one exception to the queue-based pattern; needs explicit architectural decision.

## Adjacent prior art in our own monorepo

- `internal/billing/idempotency.py` — existing idempotency-key pattern used in the GL writes; the new error-handling subsystem can build on this for "did we already process this message?" checks during replay.
- `internal/audit/event_log.py` — existing append-only event log; could be the audit substrate for "message X was sent to DLQ at T, replayed at T+N by operator Y".

## Enrichment quality

- **Tier**: `fallback_2` (native primitives, no semantic index).
- **Confidence**: medium-high. The fleet inventory and retry/DLQ counts are derivable from file inspection; the `~140 try/except` figure came from `grep -rc`.
- **Token cost**: ~720 tokens.
