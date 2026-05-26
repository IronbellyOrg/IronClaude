---
domain: code
strategy: systematic
depth: standard
proposal_count: 3
handoff: task
---

# Seed Brief — Implement Feature Flag System

## Socratic synthesis

1. **Primary outcome**: let product and engineering roll out behavior behind typed flags without redeploying or editing application code.
2. **Control plane**: start with repository-backed flag definitions plus a runtime evaluator; defer hosted UI until audit and propagation semantics are proven.
3. **Evaluation boundary**: every flag must declare owner, expiry, default, allowed variants, rollout rule, and kill-switch behavior.
4. **Safety invariant**: unknown flags resolve to declared safe defaults and emit telemetry; no dynamic code execution in flag rules.
5. **Task handoff**: produce an implementation task because the requirements are concrete enough for execution planning.

## Chosen advocate set

- `opus:architect` — control-plane/data-model boundaries.
- `sonnet:refactorer` — integration seams and stale-flag cleanup.
- `haiku:security` — authorization, audit, and injection resistance.
