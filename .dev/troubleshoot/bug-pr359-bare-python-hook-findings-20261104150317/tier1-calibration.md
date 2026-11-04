# Calibration Report

**Card under calibration**: tier1-hypothesis.md (this directory)
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-04T15:16:53Z
(Returned by confidence-calibrator; persisted by the parent on receipt.)

## Per-dimension scores
| Dimension | Score | Justification |
|---|---|---|
| Evidence grounding | 1.0 | every cited line (98, 101, 190, 191, 206, 234-239, 275) matches the source; hand trace gives 160ython3, 30, [[ then python, matching trace-probe.out |
| Runtime check | 1.0 | mixed/runtime_trace; probe-baseline.out, trace-probe.out and the fake-python3 bash observation captured |
| Symptom coverage | 1.0 | all three findings and the control inputs explained by observed outputs |
| Reproducibility fit | 1.0 | deterministic; reproducer ran |
| Fix directness | 0.5 | right lines, but a multi-part change (decode helpers, long-option tables with abbreviation, clustered short options, [[ state, mirror, docs, tests) |
| Domain coherence | 1.0 | one scanner, one fix site |

## Stage-2 trace
| Step | Value | Notes |
|---|---|---|
| arithmetic_mean(all_six) | 0.92 | 5.5/6 |
| gate_M1 | 1.30 | does not bind |
| gate_M2 | 1.30 | does not bind |
| gated_min | 0.92 | |
| verdict_cap | none | claim_class mixed, runtime_check 1.0 |
| **calibrated** | 0.92 | |
| spot_check_unverifiable | none | |
| structural_flags | none | |

## Confidence
- **Self-reported (in card)**: 0.90
- **Calibrated (this report)**: 0.92
- **Formula applied**: min(mean, EG+0.30, RC+0.30) = min(0.92, 1.30, 1.30) = 0.92

## Escalation recommendation
- **Verdict**: `STOP`
- **Reason**: `none`
- **Rubric rule fired**: Rule 4 (Default): confidence >= 0.85 AND single-domain AND reproducible -> STOP at Tier 1.
- **Execution restriction**: none

## Structural assertions
| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | — | — | calibrated 0.92 >= 0.50; headline not an enum token |
| C2 | no | — | — | P1-P3 excluded with exit statement :275 observed taken (producers.md) |
| C3 | no | — | — | SAME-ENV yes; no reference arm cited |
| C3b | no | — | — | runs-in known (execution-locus.md) |
| C4 | no | — | — | D1 has predictions and outcome mapping; no enabling tasks |
| C5 | no | — | — | card Timestamp 15:16:29Z before mtime 15:16:52Z |
| C6 | no | — | — | no threshold/bracket claim |
| C7 | no | — | — | no environment-property causal claim |
| C8 | no | — | — | behaviour-definitions rows 1-5 present with Status |

## Notes
- Unverified: probe.sh/trace-probe.sh not supplied to the calibrator; \x70/p forms shown by hook exit only; other long options shown by --help only.
- Sensitivities: C3 or C7 read broadly would lower confidence (0.83 / 0.50); neither applies by intent.
- Minor: raw grep for `exit 0` also matches comment lines 10 and 12 (4 executable hits, table complete); repro-venue-id has digits stripped by design.
