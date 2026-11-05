# Calibration Report

**Card under calibration**: tier2-quality-engineer-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-04T16:28:06Z
**Provenance**: confidence-calibrator agent; persisted by the parent on receipt (condensed)

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 1.0 | all ranges verified (E2's split at :339, just outside the cited range) |
| Runtime check | 1.0 | static_defect + source_static inherits grounding |
| Symptom coverage | 1.0 | constraint (a) covers :332; (b)-(d) cover the loop |
| Reproducibility fit | 0.5 | no reproducer or tests run by the card |
| Fix directness | 0.5 | broad change; "write nothing" vs _write_catalog at :326; fixture change vs "tests unchanged" |
| Domain coherence | 1.0 | one domain |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.83 | |
| gate_M1: evidence_grounding + 0.30 | 1.30 | |
| gate_M2: runtime_check + 0.30 | 1.30 | |
| gated_min | 0.83 | |
| verdict_cap | none | |
| **calibrated** | 0.83 | |
| spot_check_unverifiable | none | |
| structural_flags | none | |

## Confidence

- **Self-reported (in card)**: 0.85
- **Calibrated (this report)**: 0.83
- **Formula applied**: min(0.83, 1.30, 1.30)
- **Delta**: -0.02

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: rule 3 (0.83 < 0.85)
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| C1 | no | — | — | no enum token |
| C2 | no | — | — | no enum excluded |
| C3 | no | — | — | no control arm |
| C3b | no | — | — | runs-in known |
| C4 | no | — | — | no measurement rows |
| C5 | no | — | — | Timestamp equals card_mtime |
| C6 | no | — | — | no numeric threshold |
| C7 | no | — | — | borderline; non-binding |
| C8 | no | — | — | row 1 present |

## Notes

- Reconcile: catalog write happens before the source check; the existing `_pinned_home` fixture must change.
