# Calibration Report
<!-- Returned by sc:confidence-calibrator (model slot: opus, agentId afab755a1eb0e3f27); persisted by orchestrator. Card author class: sonnet -> calibrator_diversity: full -->

**Card under calibration**: /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/legacy-pre-attempt-1/artifacts/reflection-card.yaml
**Rubric**: /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/plugin/skills/sc-reflect-protocol/refs/reflection-rubric.md
**Card tier**: 1
**Timestamp**: 2026-10-24T19:40:00Z
**calibration_failed**: false

## Per-dimension scores
| Dimension | Score | Justification |
|---|---|---|
| Citation grounding | 0.90 | spec.md:6/:9/:12, proposed.md:3/:4/:7/:10, coverage-matrix.yaml:4/5/8/10/11/12/14/16, requirements-analyst-output.md:28-29 verified verbatim. Minor stretch: grounding_gaps[1] cites requirements-analyst-output.md:30 for framework claim; line 30 covers paths/module names only. |
| Coverage completeness | 1.00 | coverage_pct 1.0, coverage_undefined false; all 3 requirements and 3 tasks have findings. |
| Deviation-classification clarity | 0.95 | DEV-1/DEV-2 single class (Drift) with rationale; gaps separate. Minor: R-003 partial vs analyst covered-loosely (disclosed); "regression candidate" risk wording. |
| Risk surface coverage | 0.90 | Regression candidates + structural/metric risks; no explicit blast-radius reasoning (small scope). |
| Recommendation actionability | 0.92 | All recs name file/change/verifier; REC-2 verifier looser; REC-3 bundles changes. |

## Calculation trace
- Five inputs: 0.90, 1.00, 0.95, 0.90, 0.92
- Unrounded mean: 0.934
- **Calibrated**: 0.93
- **Self-reported**: 0.85 (not used)
- **Delta**: +0.08

## Escalation recommendation
- Recommendation: ORCHESTRATOR_DECIDES
- Execution restrictions: --mode pre (legacy --type task --analyze) --tier 1 --no-promote

## Notes
- Path legend `<output>/artifacts/...` is literally correct (files live in artifacts/artifacts/).
- Minor citation mismatch grounding_gaps[1] -> requirements-analyst-output.md:30 (framework claim not on that line).
- No remote URLs; no annotated sinks; no absent optional inputs.
