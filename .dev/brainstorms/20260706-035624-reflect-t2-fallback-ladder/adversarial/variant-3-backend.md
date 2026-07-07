# Variant 3 — Post-Normalization Quorum Top-Up Ladder

## Summary

Design the fallback ladder as a reflect-owned, post-normalization top-up step inside `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/reflect/ensemble.py`.

Core idea:

1. Run the existing primary Tier-2 fan-out exactly as today.
2. Let existing dispatch retry policy and Wave-2 normalization/salvage finish first.
3. Inspect normalized primary outcomes.
4. If fewer than two usable heterogeneous reviewers survived, launch bounded fallback reviewer attempts from `T1Model01`, then `T1Model02`.
5. Append fallback attempts to the attempt ledger, but derive the final quorum from a separate explicit `contributing_reviewers` selection.
6. Leave `contract.derive_verdict()` unchanged.

## Minimal-Risk Refactor Shape

Prefer keeping the first pass localized:

- `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/reflect/ensemble.py`

Extract later only if the helper block becomes large:

- `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/cli/reflect/fallback.py`

Suggested helper boundaries:

```text
run_tier2_ensemble()
  primary dispatch
  primary normalize
  fallback_plan = plan_fallback_ladder(...)
  fallback_results = run_fallback_ladder(...)
  all_attempts = primary + fallback
  contributing = select_contributing_reviewers(all_attempts)
  reduce all attempts for audit visibility
  build reflect contract from contributing reviewers plus fallback metadata
```

## Proposed Data Structures

- `FallbackSlot`: slot name, reason, max uses.
- `ReviewerAttempt`: attempt id, role, source slot, replaces attempt id, worker index, status, model metadata, elapsed time, final path, trigger reason, contribution flag.
- `FallbackPlan`: enabled flag, primary failures, slots to run, reason.
- `ContributingReviewerSet`: selected workers, attempt IDs, count/diversity summaries, selection reason.

## Dispatch Strategy

Wait for full primary fan-out, then top up. This preserves deterministic planning and lets parse salvage succeed before fallback is considered.

Trigger from normalized statuses after `normalize_wave2()`:

| Normalized outcome | Fallback-triggering? |
|---|---:|
| `success` | no |
| `proxy_error` | yes |
| `timeout` | yes |
| `parse_error` | yes |

## State Machine

```text
START
 -> PRIMARY_DISPATCH
 -> PRIMARY_NORMALIZE
 -> ASSESS_PRIMARY_QUORUM
 -> FINALIZE_NO_FALLBACK | PLAN_FALLBACK
 -> FALLBACK_DISPATCH
 -> FALLBACK_NORMALIZE
 -> ASSESS_FINAL_QUORUM
 -> FINALIZE_T2_WITH_FALLBACK | FINALIZE_DEGRADED
```

## Contract Metadata

Keep existing verdict-bearing fields unchanged and add non-breaking metadata:

```yaml
fallback_ladder:
  enabled: true
  policy_version: reflect-t2-fallback-ladder-v1
  strategy: post-normalization-quorum-top-up
  primary_reviewers_requested: 3
  fallback_slots_configured: [T1Model01, T1Model02]
  fallback_slots_used: [T1Model01]
  fallback_triggered: true
  fallback_reason: primary-normalized-failure
reviewer_attempts: []
contributing_reviewer_attempt_ids: []
primary_failures_preserved: []
tier2_certification_basis: primary-plus-fallback-quorum
```

## Cheap Alternatives

- Add `T2Model04` to deep primary fan-out: useful but not sufficient.
- Improve parse-error salvage only: useful but does nothing for proxy failures/timeouts.
- Treat one reviewer as enough: rejected.
- Re-run failed primary regardless of error class: rejected for v1.
- Generalize fallback pools into swarm core now: rejected for v1.

## Rollout

1. Add fallback planning helper.
2. Add contributor-selection helper.
3. Add contract metadata parameters with no caller changes.
4. Add helper tests.
5. Wire fallback ladder for stub transport.
6. Add stub integration tests.
7. Wire openai-compatible fallback resolution.
8. Add contract/audit metadata tests.
9. Update source docs.
10. Run targeted tests and sync checks.
