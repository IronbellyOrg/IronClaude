---
proposal_id: 3
persona: qa
model: haiku
lens: test surface, edge cases, regression risk, failure-mode coverage
---

# Proposal 3 — QA: The Chaos Harness Is the Gate, Not an Add-on

## Position

The architect treats the chaos harness as component #5 of the subsystem and the DevOps proposal defers it until "3 fleets are on it." Both are wrong. **The chaos harness ships as part of MVP — before any fleet migration claims completion** — because it is the *only* way to verify that the new error handling actually changes behavior under the failure conditions that caused the Q1 incidents. Without the harness, "migrated" is an unverified claim.

## Test taxonomy (mandatory before any fleet declares migration done)

Eight test classes; every fleet's migration PR must demonstrate all eight against its own handler:

1. **Transient-error retry**: Inject a transient `RetryableError` (e.g., simulated 503). Assert: retried with exponential backoff, succeeds within max-attempts, no DLQ entry.

2. **Deterministic-error fail-fast**: Inject a `NonRetryableError` (e.g., schema validation). Assert: no retry, DLQ entry written, alert fires within SLO window.

3. **Poison-message quarantine**: Inject a message that crashes the handler *before* classification (e.g., a payload that causes an unhandled `RecursionError`). Assert: message is quarantined, worker recovers without pod restart, audit log records the quarantine event.

4. **Downstream rate-limit storm**: Inject a `Retryable(429)` flood from a mocked downstream. Assert: retry respects `Retry-After` if present, falls back to exponential backoff with jitter if not. Critically: **does NOT amplify** — the retry rate must be ≤ the original injection rate.

5. **DLQ unavailability** (Cloudflare-pattern test): Kill the DLQ mid-test. Assert: worker behavior matches the documented fallback (per-fleet config: block-and-page, local-buffer-with-bound, or drop-with-audit). Test asserts the *documented* behavior actually happens.

6. **Stripe-pattern attempt-bounded retry**: Inject an error that's `Retryable(promote_after_attempts=3)`. Assert: attempts 1-3 retry, attempt 4 promotes to non-retryable → DLQ. Verifies the taxonomy's most subtle feature.

7. **Replay-rate-limit enforcement**: Trigger a replay of 10k DLQ messages with default rate limit. Assert: replay rate ≤ 100 msg/sec, downstream sees no original-load-spike re-creation. (Validates DevOps proposal's mitigation.)

8. **Replay-audit completeness**: Replay 100 messages with operator ID `alice`. Assert: audit log has 100 entries each tagged with `alice` + timestamp + filter expression.

## Why the chaos harness ships at MVP

The Q1 incidents were not "retries weren't exponential" — they were "the *interaction* between retry, DLQ, classification, and downstream behavior produced an outcome no single component owned." Unit tests of `retry.py` would have passed; integration tests of `worker + DLQ` would have passed. The chaos harness is the *only* test surface that catches these interaction failures, and it must exist *before* fleet migrations can credibly claim completion.

## Acceptance criteria (per-fleet)

- **AC-Q1** — All 8 chaos tests green for the fleet's specific handler. Recorded as CI artifacts.
- **AC-Q2** — Per-fleet error-rate SLO defined: numerator (`RetryableError-promoted-to-NonRetryable`), denominator (total messages processed), budget (varies per fleet: 0% for billing-critical, 0.1% for customer-facing, 1% for best-effort).
- **AC-Q3** — Runbook entry exists at `docs/runbooks/workers/<fleet>.md` covering: "DLQ has N messages — diagnose", "DLQ is unavailable — failover", "Replay these N messages — procedure".
- **AC-Q4** — Per-fleet observability: dashboard panel showing real-time `error_class_total{error_class}` rates; alert fires when `RetryableError` rate exceeds 10× rolling p95 for >5 min (early-warning for "retry storm").
- **AC-Q5** — Soak test: ≥2 weeks at canary 5% traffic with the new code path, zero billing-critical message loss (verified via idempotency-key replay-counts matching production counts).

## Where I push back on both prior proposals

**Architect**: chaos as component #5 of an architecture diagram is decorative; it must be a *gate* in CI.

**DevOps**: "build chaos harness once 3 fleets are migrated" is exactly the order the Q1 incidents disprove. If we'd had the harness *before* `email-dispatch`, the infinite-retry bug would have been a development-time finding, not a $50k incident.

## Cost

~1.5 sprints to build the harness scaffolding + the 8 test classes. ~0.5 sprint per fleet to wire its handler into the chaos suite. Total: ~9 sprints across 12 fleets — overlaps with migration work; not additive.
