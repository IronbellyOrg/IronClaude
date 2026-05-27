---
proposal_id: 1
persona: architect
model: opus
lens: long-term system fit and extensibility
---

# Proposal 1 — Architect: Unified Error Envelope and Boundary Classifier

## Position

Make the worker boundary the authoritative place where every task outcome becomes a typed terminal record. The core requirement is a stable `WorkerErrorEnvelope` contract and a classifier that maps exceptions, cancellations, retry exhaustion, and poison inputs into explicit states.

## Requirements Emphasis

- Replace ambiguous pool results with terminal states: succeeded, failed, cancelled, quarantined, skipped, unknown.
- Classify failures at the worker boundary rather than in each caller.
- Preserve per-task causality, retry policy, attempt count, and affected unit identity.
- Support adapters for existing result shapes during migration.
- Allow pool policies to choose partial success or atomic rollback.

## Risks

- If migration requires all callers to change at once, adoption will stall.
- If the envelope is too implementation-specific, other executors cannot reuse it.
- If partial success and rollback are conflated, downstream gates may misreport state.

## Acceptance Focus

A downstream workflow can inspect a pool result and know which tasks succeeded, which failed, why they failed, and what recovery policy was applied.
