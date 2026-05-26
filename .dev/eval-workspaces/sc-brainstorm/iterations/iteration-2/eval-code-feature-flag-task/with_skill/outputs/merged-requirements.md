---
spec_type: requirements
adversarial_status: pass
convergence_score: 0.76
proposal_count: 3
source_proposals: 3
debate_transcript: adversarial/debate-transcript.md
handoff_target: task
---

# Merged Requirements — Feature Flag System

## Functional Requirements

1. **FR1 — Typed registry**: define every flag with `key`, `owner`, `expiry_date`, `default_variant`, `allowed_variants`, and `rollout_rule`; registry validation fails on duplicate keys or missing owners.
2. **FR2 — Safe evaluator**: expose one evaluator API that accepts a whitelisted context object and returns a declared variant within 5 ms p95 for 1,000 sequential evaluations in unit tests.
3. **FR3 — Deterministic rollout**: percentage rules must bucket by stable actor identifier and remain deterministic across process restarts with ≥100 fixed test vectors.
4. **FR4 — Kill switch**: support per-flag safe default plus emergency override that takes effect on next registry reload and emits an audit event.
5. **FR5 — Expiry enforcement**: CI fails when an active flag is past `expiry_date` or when a removed flag is still referenced by application code.
6. **FR6 — Task handoff**: output an implementation task artifact with concrete implementation steps and test targets.

## Non-Functional Requirements

1. **NFR1 — No dynamic execution**: rollout rules are declarative predicates only; no eval, shell, or plugin execution is allowed.
2. **NFR2 — Privacy**: context schema forbids raw email, full name, token, and IP address fields; tests include at least 12 rejected PII examples.
3. **NFR3 — Observability**: unknown flag, fallback-to-default, and rule-evaluation failure emit structured telemetry with flag key, reason, and safe default used.
4. **NFR4 — Reviewability**: v1 flag definitions live in source-controlled files and require normal code review.
5. **NFR5 — Cleanup**: expired flags have an owner-visible failure message with the owning team and removal deadline.

## Acceptance Criteria

1. Add at least 40 evaluator tests covering defaults, variants, percentage rollout, unknown flags, and invalid rules.
2. Add at least 12 schema tests proving PII fields are rejected.
3. Demonstrate deterministic rollout with 100 fixed actor IDs and stable assignments across two evaluator instances.
4. Prove CI fails for an expired active flag and for a removed flag still referenced by code.
5. Verify emergency override emits an audit event and changes evaluation result on next registry reload.
6. Verify `handoff/task.md` exists and contains implementation steps.

## Risks

1. **Flag debt**: stale flags accumulate unless expiry enforcement is mandatory; mitigated by CI failure and owner fields.
2. **Rule injection**: expressive predicates can become code execution; mitigated by declarative rule grammar only.
3. **PII leakage**: targeting context can collect sensitive identifiers; mitigated by context schema rejection tests.
4. **Operational surprise**: emergency overrides can mask bugs; mitigated by audit event and safe-default logging.

## Open Questions

1. Should v2 add a hosted UI after source-backed v1 proves audit semantics?
2. Should percentage rollout use user ID, workspace ID, or both for multi-tenant products?
3. What retention period should apply to flag evaluation telemetry?

## Provenance

| Requirement | Source |
|-------------|--------|
| FR1, FR2 | Architect proposal + Tension 1 resolution |
| FR3, FR5 | Refactorer proposal + cleanup concern |
| FR4, NFR1, NFR2 | Security proposal + Tension 2 resolution |
| FR6 | User-selected `--handoff task` eval case |
| AC1-AC6 | Debate transcript convergence decisions |
