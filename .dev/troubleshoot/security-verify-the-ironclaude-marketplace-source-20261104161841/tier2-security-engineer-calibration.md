# Calibration Report

**Card under calibration**: tier2-security-engineer-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-04T16:28:06Z
**Provenance**: confidence-calibrator agent; persisted by the parent on receipt (condensed)

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 0.5 | lines match, but the headline add-path bypass is refuted by the parent probe; E4's "refusal" describes a proposed fix, not current code |
| Runtime check | 0.0 | mixed + source_static; the executed probe counts against the claim |
| Symptom coverage | 0.5 | agrees with D1/D2; its own additions refuted or unobserved |
| Reproducibility fit | 0.5 | probe reproduces the opposite (rebind, rc=0) |
| Fix directness | 0.5 | post-add gate unnecessary on 2.1.318; no concrete change |
| Domain coherence | 1.0 | one domain |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.50 | |
| gate_M1: evidence_grounding + 0.30 | 0.80 | |
| gate_M2: runtime_check + 0.30 | 0.30 | binding |
| gated_min | 0.30 | |
| verdict_cap | none | |
| **calibrated** | 0.30 | |
| spot_check_unverifiable | none | |
| structural_flags | none | |

## Confidence

- **Self-reported (in card)**: 0.55
- **Calibrated (this report)**: 0.30
- **Formula applied**: min(0.50, 0.80, 0.30)
- **Delta**: -0.25

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: rule 3 (confidence < 0.85; security_caution also applies)
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| C1 | no | — | — | headline is not a definite enum token |
| C2 | no | — | — | no enum exclusion |
| C3 | no | — | — | no control arm |
| C3b | no | — | — | runs-in known |
| C4 | no | — | — | card gives predictions and outcome mapping |
| C5 | no | — | — | Timestamp equals card_mtime |
| C6 | no | — | — | no numeric threshold |
| C7 | no | — | — | borderline (CLAUDE_CONFIG_DIR named); non-binding at 0.30 |
| C8 | no | — | — | row 2 present, observed:this-run |

## Notes

- Add-path half is effectively REFUTE by the card's own discriminator; only "a refused workspace keeps a foreign enabled install" survives, unobserved.
- The card's discriminator is not registered in the tasklist (informational inconsistency).
