# FR-DRS TDD — Presentation Summary

**Date:** 2026-06-21

## Where the TDD lives
**`.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/tdd.md`** (sibling to spec.md, matching
the issue-2 pattern — NOT under `docs/`).

## Document profile
- **Lines:** 1,549 (Heavyweight tier; budget 1,200–1,800, cap 2,000 — within budget).
- **Sections:** 28 numbered template sections + a `## Reuse & Consolidation Audit` section, all present in order.
- **Populated:** §1-8, §11-15, §17-28 fully populated.
- **N/A with rationale (backend/library + CLI component, no frontend surface):** §9 State Management,
  §10 Component Inventory, §16 Accessibility.
- **Repurposed:** §8 API Specifications = the module/function API of the sweep + the six `runtime_surface_*`
  contract scalars (NOT HTTP endpoints). §7 Data Models = the `runtime-surface-ledger.yaml` schema +
  `RuntimeSurfaceLedgerRow` TypedDict + reduction precedence + count invariant.
- **Light (local-only, no infra):** §13 Security, §14 Observability, §17 Performance, §25 Ops, §26 Cost.

## What the TDD specifies
A deterministic, pure-Python, LLM-free sweep module `src/superclaude/cli/reflect/runtime_surface.py` (6 logical
units: surface-tagger, referrer-finder, partitioner, degrade-oracle, entrypoint-rootwalk, ledger+scalar reducer)
that computes `runtime-surface-ledger.yaml` + the six `runtime_surface_*` contract scalars deterministically on
every UC-2 run — removing the LLM from the structured-emission path while preserving its narration/verdict role.
Integration across three paths: product (`runner._audit_once` writes the fields before `parse_contract`), eval
(grader invokes the same module), and SKILL prose demotion (§6.1 4b/4b′ → narration-only, safety behavior preserved).

## Artifact locations
- Research corpus: `.dev/tasks/to-do/TASK-TDD-20260621-124414/research/` (00-06 + web-01/02 + reuse-audit.yaml)
- Synthesis: `.dev/tasks/to-do/TASK-TDD-20260621-124414/synthesis/` (synth-01..09)
- QA gate reports: `.dev/tasks/to-do/TASK-TDD-20260621-124414/qa/` (25 reports across 4 gates)
- Gate verdicts: `.dev/tasks/to-do/TASK-TDD-20260621-124414/phase-outputs/plans/`

## Open questions / areas needing manual review (TDD §22 + §6.4)
- **OQ-DRS.1 (referrer engine):** ripgrep/AST floor (determinism-safe default, recommended) vs optional Serena/LSP
  precision overlay (must DEGRADE-to-floor on unavailability).
- **OQ-DRS.2 (invocation site):** recommended `runner._audit_once` (covers `superclaude reflect run`) + a Wave-1A
  skill shell-out for the bare `claude -p /sc:reflect` path (which the Python wrapper does not cover). Needs
  ratification at implementation.
- **OQ-DRS.3 (contract version):** recommended NO bump (producer-only change; stays 1.6.0). Reconcile the stale
  `ensemble.REFLECT_CONTRACT_VERSION="1.0"` vs SKILL 1.6.0 (Q4).
- **reflect→audit import boundary (§6.4 D1):** recommended Option C (reflect-local copy of the `_bfs_reachable`
  rootwalk skeleton) for v1, Option B (boundary-neutral shared helper) long-term, avoid Option A (direct import).
- **Deferred (FR-006a):** the sprint-executor read of the deterministic scalars is NOT in v1 scope (the executor
  reads no reflect contract today); only the §5.3 forbid-STOP pre-filter read (via the derived `surface_unreached`
  field) is in scope. The C-5 `evals.json→eval_metadata.json` materializer must be located in Phase 1 (gates AC-2).

## Downstream
This TDD can feed directly into implementation task files (`/task` skill) or `/sc:roadmap` — the research files
and design specifications are already in place. The TDD was verified implementation-ready by the actionability
lens after fixes (an engineer can build `runtime_surface.py` from §6/§7/§8 alone).
