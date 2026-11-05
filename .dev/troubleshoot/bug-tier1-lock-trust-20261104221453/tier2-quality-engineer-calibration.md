# Calibration Report

**Card under calibration**: .dev/troubleshoot/bug-tier1-lock-trust-20261104221453/tier2-quality-engineer-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-04T22:30:13Z
(persisted by the orchestrator on receipt from the confidence-calibrator agent; content condensed, scores and verdict verbatim)

## Per-dimension scores

| Dimension | Score | Justification |
|---|---|---|
| Evidence grounding | 1.0 | E1-E8 all match |
| Runtime check | 1.0 | mixed x runtime_repro; the test-design claims have no captured output |
| Symptom coverage | 0.5 | covers the secondary test-design gap; primary symptom by delegation to the root-cause card |
| Reproducibility fit | 0.5 | probe reproduces the upstream defect, not the test-design cause |
| Fix directness | 0.5 | multi-file; C4 caps at 0.5 (no change) |
| Domain coherence | 0.5 | security logic, test design, protocol pin, CI versions |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|---|---|---|
| arithmetic_mean(all_six) | 0.67 |  |
| gate_M1: evidence_grounding + 0.30 | 1.30 |  |
| gate_M2: runtime_check + 0.30 | 1.30 |  |
| gated_min | 0.67 |  |
| verdict_cap | none (C7 cap 0.50 binding) |  |
| **calibrated** | 0.50 |  |
| spot_check_unverifiable | none |  |
| structural_flags | uncited, no_prereg_falsifier |  |

## Confidence

- **Self-reported (in card)**: 0.86
- **Calibrated (this report)**: 0.50
- **Formula applied**: min(0.67, 1.30, 1.30) = 0.67; C7 cap -> 0.50

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: rule 3 confidence < 0.85 (multi_domain also matches)
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | — | — | 0.50 not below 0.50 |
| C2 | no | — | — | none |
| C3 | no | — | — | no control arm |
| C3b | no | — | — | runs-in stated |
| C4 | yes | no_prereg_falsifier | Fix directness <= 0.5 (no change) | P-1/P-2 lack true/false predictions |
| C5 | no | — | — | no Timestamp value |
| C6 | no | — | — | version labels, not thresholds |
| C7 | yes | uncited | calibrated <= 0.5 | names CI 3.10 / local 3.11 without a 2x2 row |
| C8 | no | — | — | rows 2 and 3 exist |

## Notes

- behaviour-definitions.md row 1 and tier1-observation.md cite probe-lock-trust.out:5; the marker is line 6.
- ESCALATE means narrow and under-evidenced, not wrong.
