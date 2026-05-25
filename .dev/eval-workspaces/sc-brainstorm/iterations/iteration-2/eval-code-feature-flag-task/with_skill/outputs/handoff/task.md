# Task Handoff — Implement Feature Flag System

## Objective

Implement a source-backed, typed feature flag evaluator with audit-safe defaults.

## Implementation tasks

1. Add a flag definition schema with key, owner, expiry, default, variants, and rollout rules.
2. Add a registry loader that validates definitions and fails on duplicate keys or expired active flags.
3. Add an evaluator interface that accepts a whitelisted context object and returns a typed variant.
4. Add telemetry for unknown flag, default fallback, and rule evaluation failure.
5. Add tests for defaults, percentage rollout determinism, expired flag CI failure, and PII rejection.

## Done

- All acceptance criteria in merged requirements pass.
- No expired active flag can merge.
- Unknown flags return safe defaults and emit telemetry.
