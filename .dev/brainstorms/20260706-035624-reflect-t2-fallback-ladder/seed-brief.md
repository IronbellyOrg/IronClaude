---
topic: "Design a refactor of the SuperClaude reflect Tier-2 reviewer ensemble so it has a fallback model ladder that preserves reviewer quorum when primary reviewers fail, instead of degrading the whole gate."
domain: architecture
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-07-06T03:56:24+00:00
---

# Seed Brief: reflect-t2-fallback-ladder

## Problem Statement

SuperClaude reflect `--depth deep` currently loses Tier-2 certification when the reviewer fan-out yields fewer than two successful heterogeneous reviewers, even when the audited code is clean. The triggering incident on 2026-07-05 had three primary T2 reviewers dispatched, but two failed (`proxy_error` and `parse_error`), leaving one success and causing `degraded-tier1` / exit 11. The design goal is to preserve honest Tier-2 quorum by adding a bounded fallback model ladder, not by weakening the verdict gate.

## Known Context

- Primary reviewer pool is the configured T2 model slots (`T2Model01..N`).
- Fallback Model 1 is `T1Model01`; it engages when a primary reviewer fails.
- Fallback Model 2 is `T1Model02`; it engages when more than one primary T2 model fails, or when `T1Model01` itself fails.
- A successful deep run needs at least two successful, heterogeneous reviewers so `reviewer_count >= 2`, `tier_reached == 2`, `t2_model_class_diversity == full`, and vendor diversity remains multi.
- Existing retry policy does not retry 4xx or timeout; 5xx has a bounded retry. Fallback must compose with, not silently replace, that policy.
- Current swarm config reads the T2 model-slot contract and does not yet expose a T1 fallback pool to reflect/swarm.
- `parse_error` is a recurrent weakness for one T2 model shape and should be treated as reviewer failure for quorum purposes after existing normalization/salvage has had its chance.
- `T2Model04` exists but is not used by the current deep run shape, so adding the fourth primary slot is a cheaper adjacent mitigation but does not satisfy the explicit T1 fallback semantics.

## Constraints

- Do not weaken, relabel, or bypass the reflect verdict contract: genuine inability to reach quorum must still produce `degraded` / exit 11.
- Do not touch TUIBBS code; the edit surface is SuperClaude under `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/src/superclaude/`.
- Keep proxy keys masked; only model slot names and model IDs may appear in artifacts.
- Preserve deterministic and auditable return-contract behavior: record which primaries failed, which fallbacks ran, why each fallback engaged, and which reviewer attempts contributed to quorum.
- Keep fallback bounded by attempt count and wall-clock; no unbounded retry loops.
- Preserve component source-of-truth discipline: design edits land in `src/superclaude/`, then `make sync-dev`; deployed pipx copy must be refreshed after implementation.

## Success Criteria

- A single transient primary reviewer failure no longer collapses a deep reflect run to Tier-1 if a fallback reviewer succeeds and diversity remains valid.
- Multiple primary failures trigger the second fallback according to the stated escalation rule.
- A failure of `T1Model01` triggers `T1Model02` even if only one primary failed.
- Fallback attempts are visible in return-contract and swarm metadata without hiding original primary failures.
- Final verdict logic remains unchanged: it evaluates the final successful reviewer set and still degrades when quorum/diversity cannot be met.
- The design identifies concrete module boundaries, config changes, contract fields, tests, and deployment sync steps.

## Open Questions

- Should fallback dispatch start as soon as any primary worker fails, or should reflect wait for the full primary fan-out and then top up to quorum?
- Should fallback attempts be represented as replacement attempts for failed slots, appended worker attempts, or both with a derived final reviewer set?
- What exact `WorkerStatus` values should trigger fallback after normalization?
- Should `T1Model0N` be a general swarm model-slot contract or a reflect-only config read by the reflect ensemble?
- How should the return-contract name the fact that Tier-2 was certified with fallback reviewers without implying the original T2 primary pool fully succeeded?

## Enrichment Context

Primary codebase enrichment succeeded. See `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/.dev/brainstorms/20260706-035624-reflect-t2-fallback-ladder/enrichment/codebase-context.md`.
