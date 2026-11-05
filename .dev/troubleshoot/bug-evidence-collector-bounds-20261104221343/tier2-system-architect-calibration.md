# Calibration Report

**Card under calibration**: .dev/troubleshoot/bug-evidence-collector-bounds-20261104221343/tier2-system-architect-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-04T22:30:13Z
(persisted by the orchestrator on receipt from the confidence-calibrator agent; content condensed, scores and verdict verbatim)

## Per-dimension scores

| Dimension | Score | Justification |
|---|---|---|
| Evidence grounding | 1.0 | E1-E4, E6-E10 match; E5 slip: the len()+1 derivation is at conflict-mechanical.md:71, not conflicts.py:1146-1154 |
| Runtime check | 1.0 | mechanism (not a rubric class) defaulted to runtime_behavior; runtime_repro probe-evidence.out:4-5 |
| Symptom coverage | 1.0 | explains the failure token, exit 2, Tier 3 escalation and the overwrite/stale-evidence side effects |
| Reproducibility fit | 1.0 | deterministic reproducer |
| Fix directness | 0.5 | right area but wide: core function + export, two refs, e2e, unit tests |
| Domain coherence | 0.5 | protocol-contract collision; fix spans Python core, refs and tests |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|---|---|---|
| arithmetic_mean(all_six) | 0.83 |  |
| gate_M1: evidence_grounding + 0.30 | 1.30 |  |
| gate_M2: runtime_check + 0.30 | 1.30 |  |
| gated_min | 0.83 |  |
| verdict_cap | none |  |
| **calibrated** | 0.83 |  |
| spot_check_unverifiable | none |  |
| structural_flags | none |  |

## Confidence

- **Self-reported (in card)**: 0.82
- **Calibrated (this report)**: 0.83
- **Formula applied**: min(0.8333, 1.30, 1.30) = 0.83

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: rule 3 confidence < 0.85 (multi_domain also matches)
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | — | — | 0.83 |
| C2 | no | — | — | borderline: 'Only Tier 2 fails today' uncited, confirmed from conflict-mechanical.md:82-95 |
| C3 | no | — | — | no control arm |
| C3b | no | — | — | runs-in known |
| C4 | no | — | — | falsification maps outcomes |
| C5 | no | — | — | placeholder Timestamp |
| C6 | no | — | — | no threshold |
| C7 | no | — | — | no environment property |
| C8 | no | — | — | row 2 exists |

## Notes

- Verdict hinges on Domain coherence 0.5 vs 1.0 (0.92 at 1.0).
- Falsification items (i)-(iv) unexecuted at calibration time.
- Script line refs in execution-locus.md/tier1-observation.md shifted by the draft edits.
