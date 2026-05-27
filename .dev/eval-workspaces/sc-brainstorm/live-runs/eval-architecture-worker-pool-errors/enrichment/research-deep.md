---
source: research-deep
quality_tier: primary
topic: "redesign error handling across worker pool"
---

# Research Deep: Worker-Pool Error Handling Patterns

## Pattern 1: Typed Error Taxonomy

Mature worker systems separate retryable/transient failures from deterministic failures and poison inputs. Requirements should force classification at the worker boundary and prevent ambiguous outcomes. Recommended classes:

- Retryable/transient: dependency timeout, rate limit, network interruption, temporary resource exhaustion.
- Non-retryable/deterministic: invalid input, invariant violation, authorization failure, missing required state.
- Poison/unclassifiable: inputs or handler states that repeatedly crash classification or deserialization.
- Cancellation/timeout: work intentionally stopped by shutdown, budget exhaustion, or operator action.

## Pattern 2: Bounded Retries and Promotion

Retries need explicit attempt limits, backoff, jitter, and promotion rules. A retryable error that exhausts policy becomes terminal and should be routed to quarantine or manual review rather than retried forever. Policies should be idempotency-aware.

## Pattern 3: Failure Envelope / Dead-Letter Contract

Worker pools should emit a stable failure envelope for failed or quarantined units. Requirements-level envelope fields include work item id, worker id, error class, cause chain, attempt count, terminal status, retry policy applied, timestamps, idempotency key, redaction marker, and replay eligibility.

## Pattern 4: Safe Replay Controls

Replay should be explicit, rate-limited, auditable, and dry-run capable. Non-idempotent tasks require manual approval. Poison inputs require quarantine review before replay. Replay results should create a second envelope linked to the original failure.

## Pattern 5: Observability at Terminal State

Metrics and logs should report terminal states separately: success, failed-non-retryable, retry-exhausted, quarantined, cancelled, timed out, rollback-succeeded, rollback-failed, and unknown. Dashboards should show retry storms and quarantine growth.

## Pattern 6: Incremental Migration

A common migration path is: introduce envelope contract, wrap existing pool boundary, emit both legacy and new status during compatibility window, migrate callers, then remove legacy ambiguity. This avoids a flag day and allows subsystem-specific rollback.
