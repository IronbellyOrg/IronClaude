---
title: "v3.05 Deterministic Fidelity Gates — Implementation Tasklist"
source_report: ../postv3.0Review/CompatibilityReport-Merged.md
source_spec: ../deterministic-fidelity-gate-requirements.md
version: 1.0.0
total_tasks: 28
total_phases: 6
status: ready
executor: sc:task-unified
---

# v3.05 Deterministic Fidelity Gates — Implementation Tasklist

## Overview

Generated from the validated CompatibilityReport-Merged.md and cross-referenced against deterministic-fidelity-gate-requirements.md v1.1.0. All Priority 3 decisions are resolved; all FRs (FR-1 through FR-10) are accounted for.

## Phase Structure

| Phase | Name | Tasks | Dependencies | Parallelizable |
|-------|------|-------|-------------|----------------|
| 1 | Spec Rewrite | 5 | None | Yes (within phase) |
| 2 | Dead Code Cleanup | 2 | None (parallel with Phase 1) |  Yes |
| 3 | Foundation Modules | 4 | Phase 1 (spec must be accurate before building) |  Partial |
| 4 | Modifications to Existing Code | 5 | Phase 3 (FR-3 severity rules needed for threshold semantics) | Yes (within phase) |
| 5 | New Orchestration Functions | 8 | Phase 3 + Phase 4 | Partial |
| 6 | Integration & Wiring | 4 | Phase 5 | Sequential |

## Dependency Graph

```
Phase 1 (Spec Rewrite) ──────────────┐
                                      ├──→ Phase 3 (Foundation) ──→ Phase 4 (Modifications) ──→ Phase 5 (Orchestration) ──→ Phase 6 (Integration)
Phase 2 (Dead Code) ─────────────────┘
```

Phase 1 and Phase 2 are fully independent and can execute in parallel.

## Resolved Decisions (from validation)

These decisions are embedded in task descriptions — do not re-debate during implementation:

1. **Diff threshold**: 30% per spec (adversarial-reviewed BF-5 decision)
2. **Remediation engine**: ClaudeProcess with MorphLLM-compatible patch format
3. **validate_semantic_high() location**: semantic_layer.py
4. **Prosecutor/defender execution**: semantic_layer.py via ClaudeProcess

## Phase Files

- [Phase 1: Spec Rewrite](phase-1-spec-rewrite.md)
- [Phase 2: Dead Code Cleanup](phase-2-dead-code-cleanup.md)
- [Phase 3: Foundation Modules](phase-3-foundation-modules.md)
- [Phase 4: Modifications](phase-4-modifications.md)
- [Phase 5: New Orchestration](phase-5-new-orchestration.md)
- [Phase 6: Integration & Wiring](phase-6-integration.md)
