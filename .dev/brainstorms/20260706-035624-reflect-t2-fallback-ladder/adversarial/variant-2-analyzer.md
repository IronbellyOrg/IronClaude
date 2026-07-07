# Variant 2 — Quorum Top-Up Fallback Ladder with an Auditable Attempt Ledger

## Thesis

Add a bounded post-primary quorum top-up controller between reflect/swarm worker normalization and reflect reduction. The controller should not weaken the Tier-2 verdict contract. It should preserve honest Tier-2 certification only when fallback reviewers produce enough successful, heterogeneous reviewer outputs to satisfy the existing deep reflect requirements.

## Core Recommendation

```text
primary dispatch
  -> existing transport retry policy
  -> existing normalization / parse salvage
  -> attempt classification
  -> fallback quorum top-up controller
  -> final reviewer set selection
  -> existing reduce / verdict contract
```

## Failure Taxonomy

Fallback eligibility is based on terminal reviewer-attempt failure after existing retry and normalization policy:

- `transport_retry_exhausted`
- `transport_nonretryable`
- `timeout_terminal`
- `proxy_error_terminal`
- `parse_error_terminal`
- `schema_invalid_terminal`

Non-eligible categories include successful normalized/salvaged output, cancellation/abort, invalid config, and precondition blocks.

## Ladder Semantics

1. Launch `T1Model01` when at least one primary T2 reviewer reaches a fallback-eligible terminal failure and current candidate set cannot already satisfy Tier-2 quorum/diversity.
2. Launch `T1Model02` when more than one primary failed, or `T1Model01` failed, or `T1Model01` succeeded but final candidate-set evaluation still lacks quorum/diversity.
3. Never launch more than the configured fallback pool.
4. Never relaunch the same fallback slot for the same reflect run outside the existing per-attempt retry policy.

## Attempt Ledger

Fallbacks are appended, not silent replacements:

```yaml
reviewer_attempts:
  - attempt_id: primary:T2Model01
    role: primary
    model_slot: T2Model01
    status: success_normalized
    contributes_to_quorum: true
  - attempt_id: primary:T2Model02
    role: primary
    model_slot: T2Model02
    status: parse_error_terminal
    contributes_to_quorum: false
  - attempt_id: fallback:T1Model01
    role: fallback
    model_slot: T1Model01
    fallback_for: [primary:T2Model02]
    fallback_reason: primary_terminal_failure
    status: success_normalized
    contributes_to_quorum: true
```

## State Machine

```text
PRIMARY_COMPLETE -> CLASSIFY_PRIMARY_OUTCOMES -> EVALUATE_CURRENT_QUORUM
  -> FALLBACK_NOT_NEEDED
  -> PLAN_FALLBACK_1 -> RUN_FALLBACK_1 -> EVALUATE_CURRENT_QUORUM
  -> PLAN_FALLBACK_2 -> RUN_FALLBACK_2 -> EVALUATE_CURRENT_QUORUM
  -> FINALIZE_CERTIFIED_T2 | FINALIZE_DEGRADED
```

## Contract Additions

```yaml
t2_fallback:
  enabled: true
  ladder: [T1Model01, T1Model02]
  engaged: true
  certified_with_fallback: true
  fallback_attempt_count: 1
  exhausted: false
  terminal_reason: certified_t2_with_fallback
final_reviewer_set: []
t2_certification_basis: fallback_augmented
```

Recommended terminal-reason enum:

- `not_needed_primary_quorum_met`
- `certified_t2_with_fallback`
- `fallback_config_missing`
- `fallback_pool_exhausted`
- `fallback_wall_clock_exhausted`
- `fallback_attempts_failed`
- `diversity_unrepairable`
- `no_fallback_eligible_primary_failure`
- `aborted_or_cancelled`

## Boundaries

- New reflect helper: `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/reflect/fallback.py`.
- Reflect ensemble calls the helper and emits metadata.
- Swarm exposes T1 model slots as model-slot descriptors.
- Verdict contract remains unchanged in pass/degrade semantics.

## Rejected Alternatives

- Lower Tier-2 quorum.
- Relabel Tier-1 fallback reviewers as T2 primaries.
- Immediate fallback on first failure.
- Use `T2Model04` as the only fix.
- Treat parse errors as soft success.
- Hide original primary failures.
- Put fallback logic inside verdict contract.

## Test Emphasis

Test terminal classification, ladder planning, final reviewer selection, return-contract metadata, stubbed integration, the 2026-07-05 incident shape, and negative cases where quorum/diversity still cannot be met.
