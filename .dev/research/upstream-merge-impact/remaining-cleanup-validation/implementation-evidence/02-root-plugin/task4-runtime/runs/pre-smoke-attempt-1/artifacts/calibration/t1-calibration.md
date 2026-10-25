<!-- Persisted verbatim-in-substance by orchestrator from sc:confidence-calibrator (model slot: opus = claude-opus-5-5[1m]) returned report. -->
<!-- Calibrator received only card_path, rubric_path, tier, flags; no formation context. -->
# Calibration Report

**Card under calibration**: runs/pre-smoke-attempt-1/artifacts/reflection-card.yaml
**Rubric**: plugin/skills/sc-reflect-protocol/refs/reflection-rubric.md
**Card tier**: 1
**Timestamp**: 2026-10-24T19:30:00Z
**calibration_failed**: false
**calibrator_model_slot**: opus (claude-opus-5-5[1m]); card author slot: sonnet -> calibrator_diversity: full

## Per-dimension scores

| Dimension | Score | Justification (summary of calibrator's returned text) |
|---|---|---|
| Citation grounding | 0.92 | All 22 citations_index entries re-Read and matched exactly; absence claims honestly [INFERRED]. Deductions: RK-06 absence claim marked inferred:false; RK-02 top-level inferred:false while its key stub risk is [INFERRED]; RK-05/RK-06 lack descriptions. |
| Coverage completeness | 1.00 | coverage_pct 1.0, coverage_undefined false; all 3 requirements and 3 tasks checked against source; no durable_sink annotations so no reachability cap. |
| Deviation-classification clarity | 0.90 | No deviations (UC-1, no executed work); gaps single-kind. Met only vacuously; rubric lacks an N/A path; RUBRIC:28 citation does not support the N/A ruling. |
| Risk surface coverage | 0.90 | RK-02 stub regression candidate, RK-01/RK-03 untested invariants, RK-04 verification gap; secondary risks thin (non-str inputs not considered beyond None). |
| Recommendation actionability | 0.92 | REC-01..05 have file/change/verifier; REC-06 advisory with no success criterion. |

## Calculation trace

- Inputs: 0.92, 1.00, 0.90, 0.90, 0.92
- Unrounded mean: 4.64 / 5 = 0.928
- **Calibrated**: 0.93
- Self-reported: absent; Delta: null

## Escalation recommendation

ORCHESTRATOR_DECIDES (C >= 0.85; above 0.90 ceiling). Flags --tier 1 pin.

## Notes

- Citation mismatches: none. Remote URLs: none.
- MATRIX path has a doubled `artifacts/` segment (output dir is named `artifacts` and the protocol places snapshot/matrix under `<output>/artifacts/`); evidence unaffected.
- Inconsistent inferred flags: RK-02, RK-06 (labelling, not fabrication).
