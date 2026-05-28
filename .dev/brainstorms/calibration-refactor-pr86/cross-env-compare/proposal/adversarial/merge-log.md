# Merge Log: REFACTOR-PROPOSAL Cross-Env

**Base**: V1 (pr86-substrate, this environment)
**Merged in**: V2 (T4-environment with original artifacts)
**Output**: `/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md`

## Applied Changes (per refactor-plan.md)

| # | Change | Source | Target Section | Status |
| - | ------ | ------ | -------------- | ------ |
| 1 | Adopt V1 base wholesale | V1 | All sections (Change A-E + matrix + counter-args + migration) | DONE |
| 2 | Add Change F (audit gate) | V2 Change 4 | New §Change F | DONE — migrated path from `.claude/skills/` to `src/superclaude/skills/` per CLAUDE.md SoT rule |
| 3 | Extend Change B frontmatter with V2 evidence_class | V2 Change 1 | §Change B frontmatter | DONE — added 5-value `evidence_class` enum alongside V1's `claim_class` + `verdict_direction`; added cross-tab table to §Change A |
| 4 | Add WebFetch URL detection note | V2 hard-fail rule 4 | §Change C Responsibilities step 3a | DONE |
| 5 | Add real-card replay fixtures | V2 §5 V1-V3 tests | §Change E (Fixtures 7-9) | DONE |
| 6 | Update Cause → Fix matrix to include Cause #1 | V2 framing | §Cause → Fix coverage matrix | DONE — prepended Cause #1 row, marked Change F as closer |
| 7 | Add cross-environment synthesis section | merge-time net-new | §Cross-environment refactor synthesis | DONE |

## Rejected V2 contributions (per refactor-plan.md)

- V2's hard-cap "override the arithmetic mean entirely" — V1's gated-minimum is more auditable.
- V2's Change 6 (modify confidence.ts) — Markdown-only scope.
- V2's hard-fail rule 2 (REFUTE > sibling CONFIRM wave-relative) — V1's M3a achieves equivalent without wave-sibling input.
- V2's hard-fail rule 5 (negative-existential regex) — V1's M3a covers the case structurally.
- V2's Change 5 (6th check in confidence-check SKILL.md) — V1's Change D is the load-bearing fix; V2's duplicates the rubric Runtime check dimension.

## File-path migrations applied

V2's original paths were all under `/config/.claude/skills/...` and `/config/.claude/agents/...`. Per CLAUDE.md ABSOLUTE RULE ("Never Stage or Commit `.claude/` Contents — `.claude/skills,commands,agents,hooks` is gitignored sync-dev output of `src/superclaude/`"), all V2 contributions were migrated to:

| V2 original path                                                                       | Migrated to                                                                                    |
| -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `/config/.claude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`     | `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`             |
| `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`            | `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`                    |
| `/config/.claude/agents/confidence-calibrator.md`                                       | `src/superclaude/agents/confidence-calibrator.md`                                                |
| `/config/.claude/skills/sc-troubleshoot-protocol/SKILL.md`                              | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`                                       |
| `/config/.claude/skills/confidence-check/SKILL.md`                                      | `src/superclaude/skills/confidence-check/SKILL.md`                                               |
| `/config/.claude/skills/confidence-check/confidence.ts`                                 | (not migrated — Change 6 rejected per refactor-plan)                                              |

This is a paste-error-class fix at the path layer; V2's semantic content is sound.

## Validation

- [x] All 6 changes (A-F) present and target `src/superclaude/*` only.
- [x] Cross-tab table in §Change A is consistent with the (claim_class, evidence_class) enums in §Change B.
- [x] Cause → Fix matrix includes Cause #1 (V2-merged) and all V1 causes.
- [x] §Cross-environment refactor synthesis section present per Agent B brief.
- [x] No internal contradictions detected on re-scan.
- [x] Provenance section enumerates per-section sources.
- [x] All rejected V2 contributions explained in §Counter-arguments considered.

## Return Contract

```yaml
return_contract:
  merged_output_path: "/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md"
  convergence_score: 1.00
  artifacts_dir: "/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/proposal/adversarial/"
  status: "success"
  base_variant: "V1 (pr86-substrate)"
  unresolved_conflicts: 0
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants: []  # Round 2.5 skipped per --depth quick
```
