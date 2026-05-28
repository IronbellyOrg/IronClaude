---
proposal_id: 3
persona: qa
model: haiku
lens: failure-mode coverage and gate enforcement
---

# Proposal 3 — QA: Failure Matrix and Contract Gates

## Position

Define the redesign through testable failure modes. Every worker-pool implementation must pass the same contract tests before migration is considered complete.

## Requirements Emphasis

- Contract tests cover transient retry, retry exhaustion, non-retryable failure, poison input, cancellation, timeout, rollback failure, replay success, replay denial, and partial success.
- Each task must end in one terminal state and no task may disappear from the result contract.
- Legacy `None`-style ambiguity must be explicitly tested as deprecated behavior behind compatibility mode.
- Chaos tests should inject dependency failures, cancellation, queue drain, and executor shutdown.
- CI must record artifacts proving migration readiness per executor.

## Risks

- Without contract gates, one executor may claim compatibility while still dropping causality.
- Tests that only assert pool-level failure miss mixed success/failure batches.
- Replay tests can create false confidence unless idempotency and duplicate protection are exercised.

## Acceptance Focus

A contract test suite can prove that no failure class is silently swallowed, retried indefinitely, or reported under the wrong terminal status.
