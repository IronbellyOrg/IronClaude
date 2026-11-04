# Calibration Report

**Card under calibration**: tier2-root-cause-analyst-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-04T16:28:06Z
**Provenance**: confidence-calibrator agent; persisted by the parent on receipt (condensed)

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 1.0 | E1 :332-337, E2 :321/:347-352/:371-374, E4 :266-271, E3 tier1-observation.md:3-12 all match |
| Runtime check | 1.0 | runtime_repro on HEAD 50123581 |
| Symptom coverage | 1.0 | name-only trust and missing dependency link both explained |
| Reproducibility fit | 1.0 | deterministic repro |
| Fix directness | 0.5 | helper, broken set, tuple shape, refusal branch, tests |
| Domain coherence | 1.0 | one function, one domain |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.92 | 0.9167 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | |
| gate_M2: runtime_check + 0.30 | 1.30 | |
| gated_min | 0.92 | |
| verdict_cap | none | |
| **calibrated** | 0.92 | |
| spot_check_unverifiable | none | |
| structural_flags | none | C1-C8 none fired |

## Confidence

- **Self-reported (in card)**: 0.90
- **Calibrated (this report)**: 0.92
- **Formula applied**: min(0.9167, 1.30, 1.30)
- **Delta**: +0.02

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `security_caution`
- **Rubric rule fired**: rule 3 (--type security and confidence < 0.95); card already Tier 2
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| C1 | no | — | — | no headline enum; 0.92 ≥ 0.50 |
| C2 | no | — | — | no enum excluded |
| C3 | no | — | — | no control arm |
| C3b | no | — | — | runs-in matches execution-locus.md:2 |
| C4 | no | — | — | no measurement rows |
| C5 | no | — | — | Timestamp equals card_mtime |
| C6 | no | — | — | no numeric threshold |
| C7 | no | — | — | no environment property asserted as fact |
| C8 | no | — | — | behaviour-definition row 1 present, Status observed:this-run |

## Notes

- Claim reads as runtime_behavior for the second half; no score change.
- E4's "add fails against an existing name" is contradicted by behaviour row 2 (add rebinds, exit 0); the defect is still shown by repro case 2.
- E3 is a stub harness; the real-CLI side is the parent's discriminator probe.
