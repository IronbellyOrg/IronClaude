# Refactoring Plan (adapted — Decision Plan, not Artifact Merge)

## Overview

This adversarial run compared two skill specifications as **competing tool choices** for a downstream decision, not as artifacts to merge into a unified document. The "refactor plan" therefore takes a non-standard form: instead of integrating sections from non-base into base, it documents the recommended tool choice and the surrounding integration steps.

- Base variant: A (`/sc:tasklist`)
- Non-base variant: B (`/task-builder`)
- Total decision points: 1 (which tool to use)
- Risk: Low (the choice is reversible — failed `/sc:tasklist` output can be deleted and `/task-builder` invoked)

## Planned Decisions

### Decision #1 — Use `/sc:tasklist` for the current roadmap

- **Source:** Variant A (sc:tasklist)
- **Target location:** Pipeline-downstream step from already-completed roadmap validation
- **Integration approach:** Direct invocation
- **Rationale:** Debate evidence — A wins 16/22 resolved diff points (Round 2 transcript); base-selection.md shows A scores 0.902 vs B at 0.871; INV-007 identifies HIGH-severity atomicity-binding violation risk if Variant B is used.
- **Risk level:** Low (deterministic transform; auto-validated by `superclaude tasklist validate`)

### Decision #2 — Reserve `/task-builder` for future novel-feature scenarios

- **Source:** Variant B (task-builder)
- **Target location:** Project knowledge — not applied to current pipeline
- **Integration approach:** Documentation note (not a code or config change)
- **Rationale:** B's evidence-engine design is the correct tool when input is uncertain or codebase-validation is the binding constraint. Current roadmap does not meet either condition. Concession from Variant A advocate (Round 1): "For a *novel* feature request with no roadmap, Variant B is the correct tool."
- **Risk level:** Low (no current action; informational only)

## Changes NOT Being Made

### Rejected: Run both tools in parallel and compare outputs

- **Diff point:** Implicit alternative considered
- **Non-base approach:** Generate via both, manually pick the better tasklist
- **Rationale for rejection:** Two outputs land in different `.dev/` subtrees (INV-006). Manual reconciliation is high-effort and the resulting tasklist would be neither sprint-CLI-compatible (if B-derived) nor evidence-research-enriched (if A-derived). Hybrid output would lose both skills' integrity guarantees.

### Rejected: Inject `/task-builder`'s research subagents into `/sc:tasklist` generation

- **Diff point:** C-005 (quality gates) and U-004 (zero-trust QA)
- **Non-base approach:** Add rf-analyst + rf-qa gates to `/sc:tasklist`'s pipeline
- **Rationale for rejection:** Would violate `/sc:tasklist`'s determinism guarantee (C-001). LLM-driven gates inject variability. The existing post-generation validator (`superclaude tasklist validate`) already provides drift detection. If three-gate validation is desired, the right place is to extend `validate-roadmap` *upstream* of `/sc:tasklist`, not to retrofit `/sc:tasklist` itself.

### Rejected: Wait and harden the roadmap further before invoking either tool

- **Diff point:** Implicit alternative considered
- **Non-base approach:** Iterate roadmap to clear all 3 WARNINGs in addition to the 0 BLOCKINGs
- **Rationale for rejection:** Validator says `tasklist_ready: true`. The 3 WARNINGs are non-blocking by design: ancillary NFR-ME absence is authorized by extraction; M5 test-back-loading is structural; compound-deliverable density is atomicity-binding, which Variant A preserves correctly.

## Risk Summary

| Decision | Risk | Impact | Rollback |
|----------|------|--------|----------|
| #1 (use /sc:tasklist) | Low | Tasklist may inherit roadmap WARNINGs (e.g., compound rows requiring split) | Delete tasklist bundle, re-invoke after additional roadmap patches |
| #2 (reserve /task-builder) | None | Informational only | N/A |

## Review Status

- Approval: Auto-approved (non-interactive mode)
- Timestamp: 2026-05-17T02:55:00+00:00
- Reviewer: debate-orchestrator + invariant-probe agent (analytic consensus)
