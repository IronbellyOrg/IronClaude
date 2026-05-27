---
proposal_id: 2
persona: devops
model: sonnet
lens: rollout sequencing and operational surface
---

# Proposal 2 — DevOps: Operationally Safe Migration and Replay Controls

## Position

Prioritize rollout safety, observability, and operator controls. The redesign succeeds only if operators can diagnose, replay, quarantine, and roll back worker failures without guessing what happened.

## Requirements Emphasis

- Add compatibility emission so old status and new envelope can coexist during migration.
- Provide dashboards for terminal status, retry storms, quarantine growth, cancellation, and rollback failures.
- Require runbooks for replay, quarantine review, and rollback decisions.
- Rate-limit replay and require justification for manual replay of non-idempotent work.
- Roll out executor by executor with feature flags and explicit rollback criteria.

## Risks

- Replay can amplify incidents if it lacks rate limits.
- Metrics that aggregate all failures together hide actionable failure modes.
- Operator workflows fail if audit and runbooks lag behind code migration.

## Acceptance Focus

Operators can identify a failed work item, understand the terminal reason, safely retry or quarantine it, and prove the intervention through audit records.
