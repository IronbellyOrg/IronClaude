---
title: Reflect Tier-2 Fallback Model Ladder Design
domain: architecture
strategy: systematic
status: success
convergence_score: 0.88
created: 2026-07-06T04:12:23+00:00
source_seed: /config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/.dev/brainstorms/20260706-035624-reflect-t2-fallback-ladder/seed-brief.md
adversarial_artifacts: /config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/.dev/brainstorms/20260706-035624-reflect-t2-fallback-ladder/adversarial/
---

# Reflect Tier-2 Fallback Model Ladder Design

## Executive Recommendation

Design the reflect Tier-2 reviewer fallback as a **post-primary, post-normalization quorum top-up controller** with an **append-only reviewer-attempt ledger**.

The controller should run after the existing primary T2 reviewer fan-out, retry policy, and normalization/salvage pipeline have produced terminal worker outcomes, but before reflect finalizes the semantic reviewer set and derives the return contract. It should dispatch `T1Model01` and, when required, `T1Model02` as bounded fallback reviewer attempts. It must never weaken the reflect verdict gate: a deep run certifies at Tier-2 only when the final contributing reviewer set has at least two successful, heterogeneous reviewers and still satisfies model-class and vendor-diversity requirements.

Recommended short name:

```text
reflect-t2-fallback-ladder-v1
```

Recommended human-facing phrasing:

```text
Tier-2 certified with fallback reviewer quorum.
```

This phrasing is intentionally different from “primary T2 pool succeeded.” A fallback-augmented pass means the final reviewer set was strong enough; it does not hide the original primary reviewer failures.

## Non-Negotiable Semantics

1. **Primary pool:** configured T2 reviewer slots, `T2Model01..N`.
2. **Fallback 1:** `T1Model01`, engaged when at least one primary reviewer reaches a terminal fallback-eligible failure and the current successful primary set cannot already certify Tier-2.
3. **Fallback 2:** `T1Model02`, engaged when any of these are true:
   - more than one primary T2 reviewer reaches terminal fallback-eligible failure;
   - `T1Model01` itself reaches terminal fallback-eligible failure;
   - `T1Model01` succeeds but the final candidate reviewer set still lacks quorum or diversity.
4. **Quorum:** final contributing reviewer count must remain `>= 2` for Tier-2.
5. **Heterogeneity:** final contributing reviewer set must still satisfy `t2_model_class_diversity == full` and vendor diversity must remain `multi` unless an existing explicit single-vendor allowance applies.
6. **Verdict honesty:** inability to reach quorum/diversity after bounded fallback remains `degraded` / exit 11.
7. **Audit honesty:** all primary failures and fallback attempts remain visible in metadata even when fallback restores Tier-2 certification.

## Chosen Architecture

### Pipeline Placement

Place fallback between primary normalization and final semantic reviewer selection:

```text
primary T2 dispatch
  -> existing dispatch retry policy
  -> existing normalize/salvage path
  -> terminal attempt classification
  -> fallback quorum top-up controller
  -> final contributing reviewer set selection
  -> semantic adversarial merge/scorer over contributors
  -> return-contract derivation using unchanged verdict rules
```

### Why Post-Primary Top-Up Wins

Use **post-primary top-up**, not immediate per-slot substitution.

Reasons:

- It lets the existing retry matrix and normalization/salvage path finish before fallback is considered.
- It avoids racing fallback calls against slow-but-valid primary reviewers.
- It prevents unnecessary fallback spend when the remaining primaries already satisfy quorum/diversity.
- It creates a deterministic planning point: primary outcomes are known, failures are counted, fallback reasons are stable.
- It makes return-contract metadata explainable.

Trade-off: a failed primary wave can take one or two additional reviewer timeouts. For `--depth deep`, this is acceptable because correctness and auditability matter more than shaving latency from an already-failing ensemble. Eager fallback can be a later optimization if telemetry proves the latency cost is too high.

## Attempt Classification

Fallback must trigger only on **terminal attempt failures** after existing retry and normalization have completed.

| Outcome | Counts toward quorum? | Fallback-eligible? | Notes |
|---|---:|---:|---|
| `success_normalized` | yes | no | Normal successful reviewer output. |
| `success_salvaged` | yes | no | Initial parse/schema issue recovered by existing normalization/salvage. |
| `transport_retry_exhausted` | no | yes | Retryable transport failure exhausted existing retry policy. |
| `transport_nonretryable` | no | yes | 4xx or other non-retryable transport outcome under current policy. |
| `timeout_terminal` | no | yes | Timeout after current timeout policy. |
| `proxy_error_terminal` | no | yes | Proxy/provider failure after current policy says terminal. |
| `parse_error_terminal` | no | yes | Parse/schema failure after normalization/salvage cannot recover valid reviewer output. |
| `schema_invalid_terminal` | no | yes | Required reviewer fields missing after salvage. |
| `cancelled_or_aborted` | no | no | Do not hide operator/system cancellation with fallback. |
| `config_invalid` | no | no | Missing/invalid model config should be surfaced honestly. |
| `blocked_precondition` | no | no | Preflight/snapshot/dirty-tree gates should stop before reviewer fallback. |

Important: `parse_error` is fallback-eligible **only after** the normalizer has had its chance. A salvageable model output should become `success_salvaged`, not trigger fallback.

## Fallback State Machine

### High-Level Controller

```text
PRIMARY_COMPLETE
  -> CLASSIFY_PRIMARY_OUTCOMES
  -> EVALUATE_CURRENT_QUORUM
  -> FALLBACK_NOT_NEEDED
  -> PLAN_FALLBACK_1
  -> RUN_FALLBACK_1
  -> EVALUATE_CURRENT_QUORUM
  -> PLAN_FALLBACK_2
  -> RUN_FALLBACK_2
  -> EVALUATE_CURRENT_QUORUM
  -> FINALIZE_CERTIFIED_T2
  -> FINALIZE_DEGRADED
```

### Transition Rules

```text
PRIMARY_COMPLETE -> CLASSIFY_PRIMARY_OUTCOMES
  when all primary attempts have reached success or terminal failure after retry + normalization.

CLASSIFY_PRIMARY_OUTCOMES -> EVALUATE_CURRENT_QUORUM
  after terminal primary failures are counted and successful primaries are diversity-scored.

EVALUATE_CURRENT_QUORUM -> FALLBACK_NOT_NEEDED
  if the successful primary set already has reviewer_count >= 2,
  t2_model_class_diversity == full,
  and vendor diversity == multi.

EVALUATE_CURRENT_QUORUM -> PLAN_FALLBACK_1
  if quorum/diversity is not satisfied,
  at least one fallback-eligible primary failure exists,
  T1Model01 is configured,
  and fallback budget remains.

PLAN_FALLBACK_1 -> RUN_FALLBACK_1
  dispatch one fallback attempt using T1Model01 with the same reflect-review prompt and normalizer contract.

RUN_FALLBACK_1 -> EVALUATE_CURRENT_QUORUM
  after T1Model01 reaches success or terminal failure.

EVALUATE_CURRENT_QUORUM -> PLAN_FALLBACK_2
  if quorum/diversity is still not satisfied and any of these are true:
  - terminal_primary_failure_count > 1;
  - T1Model01 reached terminal failure;
  - T1Model01 succeeded but did not repair quorum/diversity;
  and T1Model02 is configured and budget remains.

PLAN_FALLBACK_2 -> RUN_FALLBACK_2
  dispatch one fallback attempt using T1Model02.

RUN_FALLBACK_2 -> EVALUATE_CURRENT_QUORUM
  after T1Model02 reaches success or terminal failure.

EVALUATE_CURRENT_QUORUM -> FINALIZE_CERTIFIED_T2
  if final contributing reviewer set satisfies unchanged Tier-2 gate.

EVALUATE_CURRENT_QUORUM -> FINALIZE_DEGRADED
  if fallback pool is exhausted, fallback config is missing, wall-clock budget is exhausted,
  or no remaining fallback can repair quorum/diversity.
```

### Terminal States

| Terminal state | Meaning | Verdict behavior |
|---|---|---|
| `CERTIFIED_T2_PRIMARY_ONLY` | Primaries alone satisfy Tier-2. | Existing pass behavior. |
| `CERTIFIED_T2_WITH_FALLBACK` | At least one fallback reviewer contributes to final Tier-2 quorum. | Pass only if unchanged Tier-2 facts are satisfied. |
| `DEGRADED_INSUFFICIENT_QUORUM` | Fewer than two successful contributing reviewers after all fallback. | Existing degraded / exit 11. |
| `DEGRADED_INSUFFICIENT_DIVERSITY` | Reviewer count exists but model/vendor diversity fails. | Existing degraded / exit 11. |
| `DEGRADED_FALLBACK_UNAVAILABLE` | Fallback config/slot resolution unavailable and primary quorum failed. | Existing degraded / exit 11 with explanatory metadata. |
| `BLOCKED_PRECONDITION` | Run stopped before ensemble can be trusted. | Existing preflight/block behavior. |

## Attempt Ledger vs Contributing Reviewer Set

The design must maintain two separate views.

### Attempt Ledger

The attempt ledger includes every primary and fallback reviewer attempt:

```yaml
reviewer_attempts:
  - attempt_id: primary:T2Model01
    role: primary
    model_slot: T2Model01
    model_id: <safe-resolved-model-id>
    vendor: <derived-vendor>
    status: success_normalized
    retry_count: 0
    normalization: normal
    contributes_to_quorum: true

  - attempt_id: primary:T2Model02
    role: primary
    model_slot: T2Model02
    model_id: <safe-resolved-model-id>
    vendor: <derived-vendor>
    status: parse_error_terminal
    retry_count: 0
    normalization: failed
    failure_class: parse_error
    contributes_to_quorum: false

  - attempt_id: fallback:T1Model01
    role: fallback
    model_slot: T1Model01
    model_id: <safe-resolved-model-id>
    vendor: <derived-vendor>
    status: success_normalized
    fallback_for:
      - primary:T2Model02
    fallback_reason: primary_terminal_failure
    contributes_to_quorum: true
```

The ledger is diagnostic and audit-oriented. It must preserve failed primaries even when fallback succeeds.

### Contributing Reviewer Set

The contributing reviewer set is the selected successful subset used to certify Tier-2 facts:

```yaml
contributing_reviewer_attempt_ids:
  - primary:T2Model01
  - fallback:T1Model01
```

Recommended selection order:

1. successful primary attempts in primary slot order;
2. successful fallback attempts in fallback ladder order;
3. prefer the smallest passing set that satisfies count + model-class + vendor diversity;
4. prefer more primary reviewers when multiple valid sets exist;
5. otherwise use deterministic slot order.

`reviewer_count`, `tier_reached`, `t2_model_class_diversity`, `t2_vendor_diversity`, `merge_method`, and semantic adversarial scorer inputs should be derived from the contributing reviewer set, not from all attempts.

## Diversity Invariants

A fallback success does not automatically repair Tier-2.

It contributes only if:

- status is success after the same normalizer contract used for primaries;
- it has a usable final reviewer artifact;
- its resolved `model_id` is distinct enough for model-class diversity;
- its resolved vendor preserves vendor diversity;
- it is selected into the contributing reviewer set.

Examples:

```text
T2Model01 succeeds on vendor A.
T2Model02 fails.
T1Model01 succeeds on vendor A.

Result: reviewer_count may be 2, but vendor diversity is not multi. The run remains degraded unless an existing explicit single-vendor allowance applies.
```

```text
T2Model01 succeeds.
T2Model02 fails.
T2Model03 fails.
T1Model01 succeeds with distinct model/vendor.

Result: Tier-2 can certify only if T2Model01 + T1Model01 satisfy both model-class and vendor diversity.
```

## Config Surface

### Recommended v1 Config

Use the existing `T1Model0N` environment model slots as the fallback pool and add a reflect-owned policy wrapper.

```yaml
reflect:
  tier2_fallback:
    enabled: true
    policy_version: reflect-t2-fallback-ladder-v1
    dispatch_policy: post_primary_top_up
    ladder:
      - T1Model01
      - T1Model02
    max_attempts: 2
    record_attempt_ledger: true
    require_model_class_diversity: true
    require_vendor_diversity: true
```

### Swarm Awareness

Swarm should gain a **model-slot resolution capability** for `T1Model0N`, but not a global fallback policy.

Responsibility split:

- swarm/config resolves model slots and transport bindings;
- reflect/fallback policy decides when fallback slots are used;
- reflect/contract derives verdict from final facts.

This avoids changing unrelated swarm users while still avoiding direct proxy/env parsing inside reflect fallback logic.

### Model Slot Descriptors

Internally, expose safe descriptors such as:

```yaml
model_slots:
  T2Model01:
    role: primary_t2
    model_id: <safe-resolved-model-id>
    vendor: <derived-vendor>
  T1Model01:
    role: fallback_t1
    model_id: <safe-resolved-model-id>
    vendor: <derived-vendor>
```

Never emit proxy keys.

## Return-Contract Additions

Add metadata; do not change verdict enum meanings.

Recommended additive block:

```yaml
t2_fallback:
  enabled: true
  policy_version: reflect-t2-fallback-ladder-v1
  strategy: post_primary_quorum_top_up
  ladder:
    - T1Model01
    - T1Model02
  engaged: true
  certified_with_fallback: true
  fallback_attempt_count: 1
  exhausted: false
  terminal_reason: certified_t2_with_fallback
  original_primary_pool_fully_succeeded: false
```

Recommended reviewer fields:

```yaml
reviewer_attempts: []
contributing_reviewer_attempt_ids: []
primary_failures_preserved: []
tier2_certification_basis: primary_plus_fallback_quorum
```

Recommended `terminal_reason` enum:

```text
not_needed_primary_quorum_met
certified_t2_with_fallback
fallback_config_missing
fallback_pool_exhausted
fallback_wall_clock_exhausted
fallback_attempts_failed
diversity_unrepairable
no_fallback_eligible_primary_failure
aborted_or_cancelled
```

When fallback cannot certify Tier-2, the return contract should explain why while still letting the existing degraded chain determine the final verdict.

Example:

```yaml
status: degraded
tier_reached: 1
t2_fallback:
  enabled: true
  engaged: true
  certified_with_fallback: false
  fallback_attempt_count: 2
  exhausted: true
  terminal_reason: fallback_pool_exhausted
```

## Module and File Surface

Potential implementation surface:

- `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/reflect/ensemble.py` — orchestrates primary dispatch, fallback controller call, final reviewer-set selection, and contract metadata wiring.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/reflect/fallback.py` — optional/new pure helper module for fallback classification, planning, attempt ledger construction, and contributor selection.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/reflect/contract.py` — verdict semantics remain unchanged; may receive additive metadata only.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/swarm/config.py` — add `T1Model0N` slot constants/resolution if not already present.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/swarm/commands.py` — expose/extend model-slot transport resolver for fallback slot families.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/swarm/models.py` — only widen shared models if reflect-local metadata is insufficient.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/tests/` — focused unit, contract, and stub integration tests.

Implementation should prefer pure helper functions first. If `ensemble.py` grows too large, extract the helper block to `reflect/fallback.py` early in the implementation branch.

## Bounds

Recommended v1 bounds:

```yaml
fallback:
  max_attempts: 2
  per_attempt_timeout_seconds: <same-as-reviewer-timeout>
  aggregate_wall_clock_policy: bounded_by_reflect_run_budget
```

Operational rules:

- At most one `T1Model01` attempt per reflect run.
- At most one `T1Model02` attempt per reflect run.
- Fallback attempts use the same per-attempt retry/timeout behavior as primaries.
- No recursive fallback beyond `T1Model02`.
- If remaining wall-clock budget cannot support another fallback attempt, stop and derive the honest degraded outcome.

## Interaction with Existing Retry Matrix

Fallback is not a retry policy replacement.

Layering:

```text
transport retry policy handles retryable errors for a single model slot
normalization/salvage handles malformed output from that slot
fallback ladder handles terminal reviewer unavailability/malformed output after those layers are exhausted
```

Examples:

- 5xx then retry success: no fallback.
- 5xx then retry failure: terminal transport failure; fallback eligible.
- 4xx: no retry under current policy; fallback eligible after terminal classification.
- timeout: no retry under current policy; fallback eligible after terminal classification.
- parse issue: normalization/salvage first; fallback only if terminal parse/schema failure remains.
- fallback attempt fails: existing retry policy applies to that attempt; then `T1Model02` may engage according to the ladder.

## Alternatives Considered

### Alternative A: Use `T2Model04` as a fourth primary reviewer

Useful but insufficient as the main design.

Pros:

- Cheap and likely improves resilience against one primary loss.
- Preserves all successes as T2 primaries.

Cons:

- Does not satisfy the explicit `T1Model01` / `T1Model02` fallback semantics.
- Still may collapse under multiple failures.
- Does not address fallback-pool awareness in swarm/reflect.

Recommendation: consider as a separate adjacent mitigation after the fallback ladder.

### Alternative B: Improve parse-error salvage only

Useful but incomplete.

Pros:

- Directly addresses the recurrent malformed-output weakness.
- Reduces fallback calls for salvageable outputs.

Cons:

- Does nothing for proxy failures or timeouts.
- Over-loosening salvage risks accepting unusable reviewer output.

Recommendation: keep salvage strict; fallback handles terminal parse failures.

### Alternative C: Add bounded 429 retry

Potentially useful but not sufficient.

Pros:

- Helps retryable/rate-limit-like failures if they are transient.

Cons:

- The current policy intentionally does not retry 4xx.
- It does not address parse failures.
- It repeats the same reviewer/model instead of preserving heterogeneity through a different fallback model.

Recommendation: treat as a separate retry-policy discussion, not a replacement for fallback ladder.

### Alternative D: Lower Tier-2 quorum to one reviewer

Rejected. This weakens the gate and reintroduces false-green risk.

### Alternative E: Treat fallback success as invisible replacement

Rejected. It hides primary failures and makes the return contract misleading.

### Alternative F: Global swarm fallback for every lens

Rejected for v1. Reflect has specific Tier-2 quorum/diversity requirements. Global fallback would expand blast radius into unrelated swarm users.

### Alternative G: Immediate fallback on first primary failure

Rejected for v1. It complicates deterministic auditability and can race with slow successful primaries or normalization salvage.

## Test Plan

### Unit: Attempt Classification

Required cases:

- 5xx succeeds after existing retry -> success, fallback not eligible.
- 5xx fails after existing retry -> terminal transport failure, fallback eligible.
- 4xx -> terminal non-retryable transport failure, fallback eligible.
- timeout -> terminal timeout, fallback eligible.
- proxy error -> terminal proxy error, fallback eligible.
- parse error salvaged -> success, fallback not eligible.
- parse error not salvaged -> terminal parse error, fallback eligible.
- config invalid -> fallback unavailable, honest degraded metadata.

### Unit: Ladder Planning

Required cases:

- zero primary failures and two heterogeneous successes -> no fallback.
- one primary failure and one survivor -> dispatch `T1Model01`.
- two primary failures and one survivor -> dispatch `T1Model01`; dispatch `T1Model02` if needed by rule/quorum/diversity.
- one primary failure plus `T1Model01` failure -> dispatch `T1Model02`.
- `T1Model01` success but same vendor/model as survivor -> dispatch `T1Model02` if it can repair diversity.
- missing fallback config -> terminal `fallback_config_missing`.
- both fallbacks fail -> terminal `fallback_pool_exhausted` or `fallback_attempts_failed`.
- wall-clock exhausted -> terminal `fallback_wall_clock_exhausted`.

### Unit: Contributing Reviewer Selection

Required cases:

- two distinct primary successes -> select primaries.
- one primary success + one distinct fallback success -> select primary + fallback.
- two primary successes same vendor + fallback different vendor -> select valid primary/fallback pair.
- fallback success same model ID as survivor -> diversity insufficient.
- fallback success same vendor as survivor -> vendor diversity insufficient.
- three successes available -> deterministic smallest passing set, preferring primaries.

### Contract Tests

Required assertions:

- `reviewer_count` equals contributing reviewer count, not attempt count.
- `tier_reached == 2` only when final contributing set satisfies Tier-2.
- fallback metadata never changes verdict by itself.
- primary failures remain visible when fallback certifies Tier-2.
- `certified_with_fallback` is true only when a fallback contributes to final quorum.
- `original_primary_pool_fully_succeeded` is false when any primary failed.
- no proxy keys appear in artifacts.

### Stub Integration

Stub scenarios:

- primary success + proxy error + success -> no fallback if diversity already passes.
- primary success + proxy error + parse error; `T1Model01` success -> fallback-certified Tier-2 if diversity passes.
- same as above but `T1Model01` fails and `T1Model02` succeeds -> fallback-certified Tier-2 if diversity passes.
- both fallbacks fail -> degraded / exit 11.
- fallback succeeds but same vendor/model -> degraded / exit 11 unless existing single-vendor allowance applies.

### Regression for Trigger Incident Shape

Simulate the 2026-07-05 shape:

```text
T2Model01: proxy_error_terminal
T2Model02: success
T2Model03: parse_error_terminal
T1Model01: success or failure depending test branch
T1Model02: success if needed
```

Expected:

- primary failures are preserved;
- fallback engages;
- deep reflect does not degrade solely because two primaries failed if fallbacks restore heterogeneous quorum;
- deep reflect still degrades if fallbacks fail or diversity remains insufficient.

## Rollout Plan

1. Add pure fallback classification/planning/selection helpers.
2. Add unit tests for helpers.
3. Add additive contract metadata parameters without changing existing caller behavior.
4. Wire fallback for stub transport first.
5. Add stub integration tests.
6. Add `T1Model0N` slot resolution for OpenAI-compatible transport.
7. Wire real fallback dispatch behind `reflect.tier2_fallback.enabled`.
8. Add contract/audit metadata tests.
9. Update source documentation for reflect reviewer behavior.
10. Run targeted reflect/swarm tests and sync checks.

Recommended verification commands for the implementation phase:

```text
cd /config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback && uv run pytest tests/ -k "reflect"
cd /config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback && uv run pytest tests/ -k "swarm"
cd /config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback && make sync-dev
cd /config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback && make verify-sync
```

Operator refresh after implementation lands:

```text
pipx install --force /config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback
```

## Source-of-Truth and Sync Discipline

Implementation must edit source files under:

```text
/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/
```

Then run:

```text
cd /config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback && make sync-dev
cd /config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback && make verify-sync
```

Do not stage generated `.claude/skills`, `.claude/commands`, `.claude/agents`, `.claude/hooks`, or `.claude/templates` mirrors. Only `.claude/settings.json` is a tracked exception, and this design does not require changing it.

## Acceptance Criteria

A future implementation satisfies this design when:

1. A single terminal primary reviewer failure can be repaired by `T1Model01`.
2. Multiple terminal primary reviewer failures can escalate to `T1Model02`.
3. `T1Model01` terminal failure escalates to `T1Model02`.
4. `T1Model01` success that does not repair quorum/diversity can still escalate to `T1Model02`.
5. Fallback never runs before existing retry and normalization/salvage finish for the triggering attempt.
6. Fallback attempts are bounded by configured attempt count and wall-clock policy.
7. Original primary failures remain visible in the return contract.
8. Fallback successes pass the same reviewer normalization contract as primary successes.
9. Final Tier-2 certification still requires at least two successful heterogeneous reviewers.
10. Genuine inability to certify Tier-2 remains `degraded` / exit 11.
11. Metadata distinguishes primary-only certification from fallback-augmented certification.
12. No proxy keys are emitted in artifacts.

## Final Design Decision

Choose the **post-primary quorum top-up controller with an append-only attempt ledger and explicit contributing reviewer set**.

This design avoids false-green verdicts, preserves the existing reflect gate, handles the triggering incident class, and keeps implementation risk bounded. The fallback ladder repairs reviewer availability only when it can honestly restore the same Tier-2 facts the gate already requires.