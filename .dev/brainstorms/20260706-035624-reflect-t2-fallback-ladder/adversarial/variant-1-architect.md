# Variant 1 — Append-Only Fallback Attempt Ledger at the Reflect/Swarm Seam

## Thesis

Preserve honest Tier-2 certification by treating fallback reviewers as bounded, auditable reviewer attempts appended after the primary Tier-2 fan-out, not as hidden retries and not as verdict-rule exceptions.

## Recommended Flow

1. Let the primary `T2Model01..N` reviewer wave complete.
2. Normalize/salvage all primary outcomes using the existing swarm normalization path.
3. Compute whether the successful reviewer set can satisfy Tier-2 quorum and diversity.
4. If not, dispatch fallback reviewers from an explicit `T1Model01`, then `T1Model02` ladder.
5. Append fallback attempts to the worker result set with provenance metadata.
6. Re-run the existing reduce/contract derivation over the final successful reviewer set.
7. Keep `degraded` / exit 11 when quorum or diversity still cannot be honestly reached.

## Module Boundaries

- Reflect orchestration: `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/reflect/ensemble.py`.
- Fallback helper: `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/reflect/fallbacks.py`.
- Swarm model-slot resolution: `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/swarm/commands.py`.
- Worker/result metadata: `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/swarm/models.py` or reflect-side metadata if WorkerResult widening is too broad.
- Verdict derivation: `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/reflect/contract.py`, unchanged in semantics.

## Key Design Decisions

- Wait for full primary fan-out, then top up.
- Trigger fallback after existing retry and normalization/salvage are exhausted.
- Trigger on terminal `proxy_error`, `parse_error`, `timeout`, `retry_exhausted`, and normalization failure.
- Append fallback attempts; do not replace failed primaries in-place.
- Derive a final reviewer set from successful attempts and evaluate diversity from actual resolved model/vendor metadata.
- Keep detailed attempt ledger plus concise operator summary.

## State Machine

```text
START -> PRIMARY_DISPATCH -> PRIMARY_NORMALIZE -> EVALUATE_QUORUM
  if quorum/diversity valid -> REDUCE_AND_CONTRACT -> END
  if invalid and fallback left -> PLAN_FALLBACK -> FALLBACK_DISPATCH -> FALLBACK_NORMALIZE -> EVALUATE_QUORUM
  if invalid and no fallback left -> REDUCE_AND_CONTRACT -> existing degraded verdict -> END
```

Terminal states:

- `CERTIFIED_T2_PRIMARY_ONLY`
- `CERTIFIED_T2_WITH_FALLBACK`
- `DEGRADED_INSUFFICIENT_QUORUM`
- `DEGRADED_INSUFFICIENT_DIVERSITY`
- `BLOCKED_PRECONDITION`

## Config/Contract Shape

```yaml
tier2_fallbacks:
  enabled: true
  max_attempts: 2
  slots: [T1Model01, T1Model02]
  trigger_statuses: [proxy_error, parse_error, timeout, retry_exhausted, normalization_failed]
  dispatch_policy: after_primary_wave
```

Return contract should add fields such as:

```yaml
tier2_reviewer_attempts:
  primaries_requested: 3
  primary_attempts: []
  fallback_ladder:
    configured: [T1Model01, T1Model02]
    attempted: []
  final_successful_reviewers: []
  fallback_certification:
    tier2_certified_with_fallback: true
    original_primary_pool_fully_succeeded: false
```

## Rejected Alternatives

- Lower quorum to one reviewer.
- Treat fallback as invisible retry.
- Add `T2Model04` and skip T1 fallback support.
- Put fallback logic in `contract.py`.
- Make swarm globally auto-fallback all failed workers.
- Dispatch fallback immediately when any primary fails.

## Test Emphasis

Unit-test fallback planner, ensemble integration, swarm slot resolution, return-contract metadata, unchanged degrade chain, duplicate model/vendor cases, parse salvage success/failure, and no proxy-key leakage.
