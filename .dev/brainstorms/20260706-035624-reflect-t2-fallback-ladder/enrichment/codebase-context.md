---
source: codebase
quality_tier: primary
created: 2026-07-06T03:56:24+00:00
---

# Codebase Context: Reflect T2 Fallback Ladder

Auggie retrieval confirmed the relevant seams for the design:

- `src/superclaude/cli/reflect/ensemble.py` owns the reflect ensemble driver. It builds `WorkerSpec(count=reviewers, models=[], timeout_sec=config.timeout_seconds)`, dispatches workers through `dispatch_wave1`, normalizes them with `normalize_wave2`, reduces them through `reduce_wave3`, and computes `reviewer_count`, `tier_reached`, `merge_method`, model-class diversity, and vendor diversity from successful workers.
- `compute_model_class_diversity()` returns `full` only when at least two successful workers have distinct `model_id` values.
- `compute_vendor_diversity()` returns `multi` only when at least two successful workers resolve to distinct vendors; with fewer than two successful workers, it returns `None` so single-reviewer fallback owns the degrade reason.
- `src/superclaude/cli/reflect/contract.py` derives the final verdict. Its FR-11 degraded chain checks chain-critical degraded components first, then expected Tier-2 runs that only reached Tier-1, then model-class diversity, single-reviewer fallback, single-vendor, and verification-skipped conditions.
- `src/superclaude/cli/swarm/commands.py` has lens shortcut retry defaults: 5xx retry enabled once, 4xx retry disabled, timeout retry disabled. It binds OpenAI-compatible transport to `T2ProxyUrl` / `T2ProxyKey` and relies on the T2Model slot contract for real model IDs.
- Prior reflect hardening docs describe the intended swarm-driven fan-out: reflect imports the swarm dispatch/reduce libraries in process, uses a per-slot transport factory, and preserves one `WorkerResult` per requested slot, including synthesized failure records.

Design implication: the fallback ladder should live at the reflect/swarm seam after primary worker outcomes are known but before reduce/contract derivation is finalized, so fallback attempts can be recorded as additional/substituted reviewer attempts and diversity can be computed over the final successful reviewer set without changing the verdict rules.