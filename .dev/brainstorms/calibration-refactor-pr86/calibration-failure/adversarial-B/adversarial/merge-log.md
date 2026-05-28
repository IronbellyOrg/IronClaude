# Merge Log

## Applied changes (per refactor-plan.md)

| # | Change | Source | Target section | Status |
|---|---|---|---|---|
| 1 | Adopt B B1/B2/B3 as M1/M2/M3 | Variant B base | §2 (Three core theories) | Applied |
| 2 | Add C C2 as Theory M4 (GUARDRAIL tier) | Variant C, U-001 winner | §2 M4 | Applied |
| 3 | Add A's cross-theory implications | Variant A, U-003 winner | §3 | Applied |
| 4 | Promote A's substrate-vs-H3 fidelity caveat | Variant A | §4 (own section) | Applied |
| 5 | Preserve B's channel-degradation note | Variant B §1 (compressed) | §5 | Applied |

## Validation

- Structural integrity: ✓ — five top-level sections, consistent heading depth
- Internal references: ✓ — all theory IDs M1/M2/M3/M4 referenced consistently
- Contradiction re-scan: ✓ — no internal contradictions; M1+M2 explicitly framed as compounding (multiplicative not additive) with cross-theory section §3
- Provenance map: ✓ — included at document end
- Per-theory confidences: averaged across channels where convergent (M1: 0.85/0.92/0.85 → 0.90; M2: 0.80/0.88 → 0.84); M3 and M4 single-channel ratings preserved

## Canonical output location

`/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/calibration-failure/agent-B-merged.md`

## Return contract

```yaml
merged_output_path: "/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/calibration-failure/agent-B-merged.md"
convergence_score: 0.85
artifacts_dir: "/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/calibration-failure/adversarial-B/adversarial"
status: "success"
base_variant: "B (sc:reflect-degraded direct-read)"
unresolved_conflicts: 0
fallback_mode: false
failure_stage: null
invocation_method: "skill-direct"
unaddressed_invariants: []
```
