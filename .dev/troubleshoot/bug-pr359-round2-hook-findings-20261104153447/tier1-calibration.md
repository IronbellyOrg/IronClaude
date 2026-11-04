# Calibration Report
(Returned by confidence-calibrator; persisted by the parent on receipt.)
**Card under calibration**: tier1-hypothesis.md (this directory) — **Card tier**: 1 — **Timestamp**: 2026-11-04T15:40:01Z

## Per-dimension scores
| Dimension | Score | Justification |
|---|---|---|
| Evidence grounding | 1.0 | lines 120, 125, 153, 196, 219, 267, 270, 326 verified; trace agrees |
| Runtime check | 1.0 | trace-probe.out hook_exit=0 x3; fake-python3 bash run captured |
| Symptom coverage | 1.0 | all three findings explained; quoted "[[" variant via bash only |
| Reproducibility fit | 1.0 | reproducer executed, deterministic |
| Fix directness | 0.5 | right lines, broader state change (quoted-word flag, psub context, reserved-word gating, mirror) |
| Domain coherence | 1.0 | one scanner |

## Stage-2 trace
| Step | Value | Notes |
|---|---|---|
| arithmetic_mean(all_six) | 0.92 | 5.5/6 |
| gate_M1 | 1.30 | no bind |
| gate_M2 | 1.30 | no bind |
| gated_min | 0.92 | |
| verdict_cap | none | AFFIRM, runtime_check 1.0 |
| **calibrated** | 0.92 | |
| spot_check_unverifiable | none | |
| structural_flags | none | |

## Confidence
- **Self-reported (in card)**: 0.90
- **Calibrated (this report)**: 0.92
- **Formula applied**: min(0.92, 1.30, 1.30) = 0.92

## Escalation recommendation
- **Verdict**: `STOP`
- **Reason**: `none`
- **Rubric rule fired**: Rule 4 (Default): >= 0.85, single-domain, reproducible.
- **Execution restriction**: none

## Structural assertions
| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | — | — | 0.92 >= 0.50 |
| C2 | no | — | — | P1-P3 excluded via observed exit :326 |
| C3 | no | — | — | no control arm cited |
| C3b | no | — | — | runs-in known |
| C4 | no | — | — | D1 preregistered; no enabling tasks |
| C5 | no | — | — | timestamp equals mtime |
| C6 | no | — | — | no threshold claim |
| C7 | no | — | — | no environment-property claim |
| C8 | no | — | — | rows 1-3 present with Status |

## Notes
Mechanism 2 needs both parts (clear skn on open; leave need on close). Gaps: trace feeds the scanner without jq (end-to-end hook_exit goes through jq); quoted "[[" variant captured in bash only; mawk only.
