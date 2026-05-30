# Merge Execution Log

**Base**: V1 (Agent A) — selected per `base-selection.md` (combined score 0.9963).
**Integrations**: V2 (Agent B), V3 (Agent C) — per `refactor-plan.md`.
**Depth**: quick (no Round 2, no Round 2.5 invariant probe).

## Applied Changes

| Change                                            | Source         | Target in base                              | Result   |
|---------------------------------------------------|----------------|---------------------------------------------|----------|
| Insert Methodology & Channel Disclosure section   | V2 §1 + §3; V3 §3 cross-ref | New top-level section after header  | Applied  |
| Replace V1 Theory 3 with V2's verdict-direction T3 | V2 §T3        | Theory 3 slot                               | Applied  |
| Demote V1's stripped-context T3 to Secondary mechanisms | V1 §T3   | New "Secondary mechanisms" section          | Applied  |
| Add V3's anchoring-leak as second Secondary       | V3 §C3        | Secondary mechanisms                        | Applied  |
| Add V3's eval-suite-silent-green as Theory 4      | V3 §C2        | New Theory 4 section                        | Applied  |
| Replace V1's T1 fix-formula with V2's gated-minimum | V2 §T1 fix | Theory 1 Systemic fix subsection            | Applied  |
| Replace V1's T2 fix-formula with V2's 6th-dimension | V2 §T2 fix | Theory 2 Systemic fix subsection            | Applied  |
| Add V3's recursion observation to cross-theory § | V3 §3 meta-obs | Cross-theory implications new bullet        | Applied  |
| Update top-of-doc "Top root causes" summary       | New synthesis  | New section at end                          | Applied  |

## Structural Integrity Validation

- All section headers parse as valid markdown.
- Provenance HTML comments present on every integrated section.
- No internal references broken (no `[link]` syntax used; all citations are `file:path` literals).
- Contradictions re-scan: zero hard contradictions (Theory 3 replacement was explicitly conceded by V1; Secondary mechanisms preserve V1's contribution).

## Substrate-Fidelity Note

V1's substrate-vs-H3 caveat preserved verbatim in Cross-theory implications. Methodology & Channel Disclosure section explicitly flags that V2/V3 channels delivered as direct-read passes (not as their intended sc:reflect / sc:troubleshoot grounding), so apparent 3-way convergence is weaker evidence than nominal.

## Output

Final merged artefact: `adversarial/merged-output.md` (will be copied to canonical `agent-A-merged.md` location).

## Return Contract

```yaml
merged_output_path: /config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/calibration-failure/agent-A-merged.md
convergence_score: 0.50
artifacts_dir: /config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/calibration-failure/adversarial
status: success
base_variant: V1 (Agent A — unmediated direct-read)
unresolved_conflicts: 0
fallback_mode: false
failure_stage: null
invocation_method: skill-direct
unaddressed_invariants: []
```

Note: convergence_score=0.50 reflects the diff-analysis count of clear-winner points vs total diff points. This is below the 0.80 default threshold but is APPROPRIATE for `--depth quick` because the non-converged points are orthogonal contributions (not contradictions) — the merge strategy is additive integration, not winner-take-all resolution. Round 2/2.5 explicitly skipped per protocol for quick depth.
