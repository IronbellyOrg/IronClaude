# Calibration Report

**Card under calibration**: tier1-hypothesis.md (this directory)
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-04T16:23:30Z
**Provenance**: confidence-calibrator agent; persisted by the parent on receipt (justifications condensed, scores and verdict verbatim)

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 1.0 | E1 (:332-337), E2 (:347-352, :356-374), E4 (installation.md:370-379, merged-requirements.md:36) re-read and match |
| Runtime check | 1.0 | runtime_repro with run/arm/commit provenance (tier1-observation.md) |
| Symptom coverage | 1.0 | both behaviours (D1, D2) match cited lines and output |
| Reproducibility fit | 1.0 | deterministic, executed on failing arm |
| Fix directness | 0.5 | needs a helper, tuple-shape change and fixture change; rests on the directory-source shape |
| Domain coherence | 1.0 | one function, one domain |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.92 | 5.5/6 = 0.9167 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | does not bind |
| gate_M2: runtime_check + 0.30 | 1.30 | does not bind |
| gated_min | 0.92 | |
| verdict_cap | none | M3a not binding |
| **calibrated** | 0.92 | |
| spot_check_unverifiable | none | |
| structural_flags | none | C1-C7 not fired; C8 skipped |

## Confidence

- **Self-reported (in card)**: 0.90
- **Calibrated (this report)**: 0.92
- **Formula applied**: min(0.92, 1.30, 1.30) = 0.92
- **Delta**: +0.02

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `security_caution`
- **Rubric rule fired**: rule 3: `--type security` AND confidence < 0.95 → ESCALATE (security_caution)
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| C1 | no | — | — | no headline enum; 0.92 ≥ 0.50 |
| C2 | no | — | — | no enum excluded |
| C3 | no | — | — | no control arm cited |
| C3b | no | — | — | runs-in known |
| C4 | no | — | — | no measurement rows |
| C5 | no | — | — | Timestamp equals card_mtime |
| C6 | no | — | — | no numeric threshold |
| C7 | no | — | — | no environment property as cause |
| C8 | skipped | — | — | input absent: behaviour_definitions_path |

## Notes

- claim_class declared static_defect but the claim reads as runtime_behavior; no score change.
- The repro uses a fake claude CLI: it proves the installer's command sequence, not real Claude Code handling of a foreign source.
- Two independent defects (D1, D2) bundled; review them separately.
