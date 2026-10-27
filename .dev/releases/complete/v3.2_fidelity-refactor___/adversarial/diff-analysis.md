# Diff Analysis: Spec-Fidelity Resolution Proposals

## Metadata
- Generated: 2026-03-20
- Variants compared: 3
- Total differences found: 8
- Categories: structural (1), content (5), contradictions (1), unique (1)
- Depth: quick

## Context

Three proposals to resolve 3 HIGH-severity spec-fidelity deviations (DEV-001, DEV-002, DEV-003) blocking the v3.2 roadmap pipeline.

### Deviations Being Resolved

| ID | Deviation | Spec Says | Roadmap Says |
|----|-----------|-----------|--------------|
| DEV-001 | `files_skipped` frontmatter field | Not in §4.4 11-field contract | Introduces it for degraded-run observability |
| DEV-002 | Whitelist scope | §4.2.1: `unwired_callables` only | Extends to all 3 finding types (~10 LOC) |
| DEV-003 | Provider directory heuristic | §4.2.2: includes "3+ files with common prefix" | Excludes from v1.0 as unspecified/untested |

## Structural Differences

| # | Area | Variant A (Amend Spec) | Variant B (Amend Roadmap) | Variant C (Regenerate) | Severity |
|---|------|------------------------|---------------------------|------------------------|----------|
| S-001 | Change target | Modifies source spec document | Modifies generated roadmap | Regenerates roadmap from scratch | High |

## Content Differences

| # | Topic | Variant A | Variant B | Variant C | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | DEV-001 resolution | Add `files_skipped` to spec §4.4 + §6.3 | Remove `files_skipped` from roadmap; rely on `analysis_complete` | Hope regeneration omits it | High |
| C-002 | DEV-002 resolution | Add `orphan_modules` + `unwired_registries` keys to spec §4.2.1 whitelist schema | Revert to single-type whitelist in roadmap | Hope regeneration limits scope | High |
| C-003 | DEV-003 resolution | Remove heuristic from spec §4.2.2 (defer to v1.1) | Restore heuristic in roadmap | Hope regeneration includes it | High |
| C-004 | Determinism | 3 targeted spec edits; outcome certain | Roadmap edits; may cascade to downstream artifacts | Non-deterministic; may fail again | Medium |
| C-005 | Effort estimate | ~15 min, 3 edits | ~30 min, must validate cascade | ~10 min but may require multiple attempts | Medium |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Variant C Position | Impact |
|---|-------------------|--------------------|--------------------|--------------------|--------|
| X-001 | Whether roadmap scope decisions are correct | Validates roadmap decisions as improvements | Rejects roadmap decisions as unauthorized scope changes | Defers judgment entirely | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | Variant A | Explicitly acknowledges roadmap decisions as well-reasoned (per spec-fidelity report's own assessment at lines 117-123) | High — aligns resolution with the report's own recommendation |

## Summary
- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 1
- Total unique contributions: 1
- Highest-severity items: S-001, C-001, C-002, C-003, X-001
