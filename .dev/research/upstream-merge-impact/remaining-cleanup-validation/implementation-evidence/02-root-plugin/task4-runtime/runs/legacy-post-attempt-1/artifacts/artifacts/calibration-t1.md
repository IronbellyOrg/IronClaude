# Calibration Report
<!-- Persisted by orchestrator from sc:confidence-calibrator (model slot: opus; card author slot: sonnet) returned report. Condensed justifications; scores verbatim. -->

**Card under calibration**: <output>/reflection-card.yaml
**Rubric**: plugin/skills/sc-reflect-protocol/refs/reflection-rubric.md
**Card tier**: 1
**calibration_failed**: false

| Dimension | Score | Justification (condensed) |
|---|---|---|
| Citation grounding | 0.92 | All spec/task/log/work quotes verified at cited lines; RK-6 path mis-rooted (file is at artifacts/artifacts/task-to-work-map.yaml:34, content matches); GG-2 "tool unavailable" uncited |
| Coverage completeness | 0.95 | 3/3 reqs, 3/3 tasks, both work hunks covered; changes.patch out-of-scope status not stated |
| Deviation-classification clarity | 0.88 | deviations: [] with rationale; gaps separate; hedge on tests/ "authorized"; R-003 satisfied:true sits uneasily with GG-1/RK-1 |
| Risk surface coverage | 0.90 | regression candidate + 3 untested invariants + weak test + process risk; no blast-radius reasoning |
| Recommendation actionability | 0.88 | REC-1 concrete; REC-2 optional; REC-3 conditional with weak verifier |

- Five inputs: 0.92, 0.95, 0.88, 0.90, 0.88
- Unrounded mean: 0.906
- **Calibrated**: 0.91
- Self-reported: absent; Delta: null
- Recommendation: ORCHESTRATOR_DECIDES
- Notes: no durable_sink annotations; now_iso absent; read-only.
