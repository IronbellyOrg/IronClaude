# Merge Log — Cross-Environment Causes

**Merge date**: 2026-05-27T00:38Z
**Base**: V1 (pr86-substrate FINAL-MERGED-CAUSES.md)
**Source of patches**: V2 (T4-substrate FINAL-MERGED-CAUSES.md)
**Output**: `/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-CAUSES-MERGED.md`

## Applied Changes

| # | Change | Source | Target Section | Status |
|---|--------|--------|----------------|--------|
| 1 | Promote calibrator-non-execution to top-cause M0 | V2 §1 #1 | New §M0 before M1 | APPLIED |
| 2 | Add agent-domain mismatch as M5 | V2 §1 #5 | New §M5 after M4 | APPLIED |
| 3 | Annotate each mechanism with layer tag | V2 throughout | Each M-section | APPLIED |
| 4 | Add INV-002 partial-calibration open invariant | V2 §2 INV-002 | Cross-mechanism implications bullet | APPLIED |
| 5 | Promote A-α/β/γ/δ to explicit shared-assumptions section | V2 §5 | New §Shared Assumptions | APPLIED |
| 6 | Add Cross-Environment Synthesis section | task-required | New § before Synthesis addendum | APPLIED |

## Provenance Annotations

All sections in the merged output carry HTML-comment provenance tags identifying their source (V1 / V2 / both / task-synthesized).

## Validation

- Structural integrity: 7 mechanism sections (M0-M5 + sub-mechanisms), Cross-mechanism implications, Shared Assumptions, Cross-Environment Synthesis, Synthesis addendum — all present.
- Internal references: every file:line citation retained from source variants.
- Contradiction re-scan: X-001 resolved as substrate-divergence (not a contradiction in the merged-output sense — both findings stand under substrate-tagging).
- Substrate-tagging: each top-7 cause tagged with applicability domain (pr86 / T4 / both).

## Return Contract

```yaml
return_contract:
  merged_output_path: "/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-CAUSES-MERGED.md"
  convergence_score: 0.14  # raw diff-point convergence; STRONG at the conceptual-pathology layer
  artifacts_dir: "/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/causes/adversarial/"
  status: "success"
  base_variant: "V1 (pr86-substrate, opus-merged)"
  unresolved_conflicts: 0  # X-001 resolved as substrate-divergence
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants: []  # --depth quick skips Round 2.5 invariant probe by protocol
```
