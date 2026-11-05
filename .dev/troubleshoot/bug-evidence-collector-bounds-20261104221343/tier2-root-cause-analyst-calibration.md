# Calibration Report

**Card under calibration**: .dev/troubleshoot/bug-evidence-collector-bounds-20261104221343/tier2-root-cause-analyst-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-04T22:30:13Z
(persisted by the orchestrator on receipt from the confidence-calibrator agent; content condensed, scores and verdict verbatim)

## Per-dimension scores

| Dimension | Score | Justification |
|---|---|---|
| Evidence grounding | 1.0 | draft bounded() collector :75-107; fail fd 3/4 :49-53; check_deadline :68-70; header :25-26; probe-evidence.out:8, :11; tests :1490-1546 match |
| Runtime check | 1.0 | environment_dependent x runtime_repro; unfixed 65s and post-fix 61s captured; P-1 passed (audit.log) |
| Symptom coverage | 0.5 | A2 fully explained; C1 not on this card (sibling card); 'If I'm wrong' line mis-explains the 61 s (61 < 65; it is deadline + 1 s grace) |
| Reproducibility fit | 1.0 | executed reproducer; the environment property is pinned by the 2x2 |
| Fix directness | 1.0 | one function plus two regression tests |
| Domain coherence | 1.0 | shell process control in one function |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|---|---|---|
| arithmetic_mean(all_six) | 0.92 |  |
| gate_M1: evidence_grounding + 0.30 | 1.30 |  |
| gate_M2: runtime_check + 0.30 | 1.30 |  |
| gated_min | 0.92 |  |
| verdict_cap | none |  |
| **calibrated** | 0.92 |  |
| spot_check_unverifiable | none |  |
| structural_flags | none |  |

## Confidence

- **Self-reported (in card)**: 0.85
- **Calibrated (this report)**: 0.92
- **Formula applied**: min(0.9167, 1.30, 1.30) = 0.92; no caps

## Escalation recommendation

- **Verdict**: `STOP`
- **Reason**: `none`
- **Rubric rule fired**: Rule 4 (confidence >= 0.85, single-domain, reproducible)
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | — | — | 0.92; no enum token |
| C2 | no | — | — | rejects fixes, not an enum |
| C3 | no | — | — | SAME-ENV yes; no control arm cited |
| C3b | no | — | — | runs-in known |
| C4 | no | — | — | P-1 states its expected outcome; falsification maps failures |
| C5 | no | — | — | no Timestamp value |
| C6 | no | — | — | 60 s is the configured constant, not an inferred bracket |
| C7 | no | — | — | 2x2 rows D-1..D-4 cited (diagnosability-tasklist.md:9-12) |
| C8 | no | — | — | rows 1 and 3 non-empty Status |

## Notes

- Negative witness: P-1 fails on HEAD at the '60-second budget' wording assertion (before the elapsed check); the elapsed difference rests on the 65 s probe.
- Post-fix probe stdout discarded; P-1 covers the EVIDENCE_FAIL timeout token.
- Judgement calls: C4 or C6 read as firing would ESCALATE.
- behaviour-definitions.md row 3 Status is stale (P-1 has since passed).
