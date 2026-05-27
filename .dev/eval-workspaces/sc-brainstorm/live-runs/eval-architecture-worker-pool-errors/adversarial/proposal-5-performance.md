---
proposal_id: 5
persona: performance
model: sonnet
lens: latency budget and throughput
---

# Proposal 5 — Performance: Low-Overhead Classification and Backpressure

## Position

The failure contract must not make the hot path expensive. Success-path overhead should be minimal, and failure-path persistence must apply backpressure rather than causing retry storms.

## Requirements Emphasis

- Keep success-path classification lightweight and avoid serializing large envelopes unless failure occurs.
- Batch audit/error persistence where safe, with sync mode for critical failures.
- Bound retry concurrency and apply jitter to prevent synchronized storms.
- Expose latency overhead and throughput impact as migration gates.
- Quarantine persistence must degrade safely if its backing store is slow or unavailable.

## Risks

- Rich envelopes can bloat memory or logs under mass failure.
- Synchronous persistence on all outcomes can reduce throughput.
- Unbounded retries can saturate dependencies and workers.

## Acceptance Focus

The redesign preserves throughput under normal operation and remains stable under failure spikes through bounded retries, batching, and backpressure.
