# Calibration Report
(Returned by confidence-calibrator; persisted by the parent on receipt.)
**Card under calibration**: tier1-hypothesis.md (this directory) — **Card tier**: 1 — **Timestamp**: 2026-11-04T16:49:35Z

## Per-dimension scores
| Dimension | Score | Justification |
|---|---|---|
| Evidence grounding | 1.0 | lines 126-130, 206, 218-219, 336, 340 and test :101 verified |
| Runtime check | 1.0 | trace-probe.out cmdword + hook_exit; reference rows observed |
| Symptom coverage | 1.0 | both findings and reference rows explained |
| Reproducibility fit | 1.0 | deterministic, re-runnable probe |
| Fix directness | 0.5 | right area; lookahead part (a) underspecified and untested |
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
- **Rubric rule fired**: Rule 4 (Default)
- **Execution restriction**: none

## Structural assertions
| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | — | — | 0.92; no enum headline |
| C2 | no | — | — | cites exit statements :336/:340 |
| C3 | no | — | — | no control arm in locus (SAME-ENV yes) |
| C3b | no | — | — | runs-in known |
| C4 | no | — | — | rows preregistered |
| C5 | no | — | — | timestamp equals mtime |
| C6 | no | — | — | no threshold claim |
| C7 | no | — | — | no environment-property claim |
| C8 | no | — | — | rows 1-2 present |

## Notes
Finding 2 is a missing fd-prefix form, not a missing lookahead (Claim states it correctly). C3 sensitivity if reference rows were read as a control arm (0.83). Behaviour row 2: `fd=` printed empty; the load-bearing half (command word follows `{fd}>`) is observed. Digits in branch/venue identity are stripped by design (counter key rule).
