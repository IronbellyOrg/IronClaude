# Calibration Report

**Card under calibration**: .dev/troubleshoot/bug-tier1-lock-trust-20261104221453/tier2-root-cause-analyst-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-04T22:30:13Z
(persisted by the orchestrator on receipt from the confidence-calibrator agent; content condensed, scores and verdict verbatim)

## Per-dimension scores

| Dimension | Score | Justification |
|---|---|---|
| Evidence grounding | 1.0 | every cited file:line matches (probe fields, parse_probe, regen_only, precheck, step 5, :296, docstring, pyproject.toml:16, probe-lock-trust.out:6) |
| Runtime check | 1.0 | mixed x runtime_repro; captured probe; the card's new claims (gate, --no-sync) not executed by the card |
| Symptom coverage | 1.0 | all three triggers gated at the only point that sees the file; Tier 2-resolved pyproject covered |
| Reproducibility fit | 1.0 | deterministic reproducer |
| Fix directness | 0.5 | exact location but multi-file; invocation depends on an unverified import assumption |
| Domain coherence | 0.5 | security gate + core + docs + tests + 3.10/3.11 constraint |

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

- **Self-reported (in card)**: 0.86
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
| C2 | no | — | — | design alternatives only |
| C3 | no | — | — | no control arm |
| C3b | no | — | — | runs-in known |
| C4 | no | — | — | no measurement row |
| C5 | no | — | — | no Timestamp value |
| C6 | no | — | — | no threshold |
| C7 | no | — | — | judgement: environment facts tied to behaviour-definition rows |
| C8 | no | — | — | rows 1-3 non-empty |

## Notes

- Same step, different evaluation mechanism from the security-engineer card: the parent's clustering must check it.
- Runtime check at 0.5 would give 0.79, same verdict.
