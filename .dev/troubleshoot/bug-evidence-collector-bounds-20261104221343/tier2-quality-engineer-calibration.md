# Calibration Report

**Card under calibration**: .dev/troubleshoot/bug-evidence-collector-bounds-20261104221343/tier2-quality-engineer-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-04T22:30:13Z
(persisted by the orchestrator on receipt from the confidence-calibrator agent; content condensed, scores and verdict verbatim)

## Per-dimension scores

`code_path` is not a rubric claim_class: scored as `runtime_behavior` (fail-safe).

| Dimension | Score | Justification |
|---|---|---|
| Evidence grounding | 1.0 | E1 :69 strict `-lt`; E3 fallback loop now :88-103; E4 callers now :204, :212-213 (pre-amendment numbering +2); amendment present at :77-80 |
| Runtime check | 0.5 | `timeout 0 sleep 2` measured (audit.log summary line); the race itself and the amended bounded() not executed; the 22 passing tests predate the amendment |
| Symptom coverage | 0.5 | covers A2; not C1; the timeout-0 race is a new finding |
| Reproducibility fit | 0.5 | premise deterministic; the trigger is a sub-second window, no reproducer |
| Fix directness | 1.0 | two lines in bounded() |
| Domain coherence | 1.0 | one domain |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|---|---|---|
| arithmetic_mean(all_six) | 0.75 | |
| gate_M1: evidence_grounding + 0.30 | 1.30 | |
| gate_M2: runtime_check + 0.30 | 0.80 | |
| gated_min | 0.75 | |
| verdict_cap | 0.84 | M3a (runtime_behavior, runtime_check < 1.0, AFFIRM); not binding |
| structural cap (C7) | 0.50 | uncited, binding |
| **calibrated** | 0.50 | |
| spot_check_unverifiable | none | |
| structural_flags | uncited | |

## Confidence

- **Self-reported (in card)**: 0.80
- **Calibrated (this report)**: 0.50
- **Formula applied**: min(0.75, 1.30, 0.80) = 0.75; M3a 0.84 not binding; C7 cap min(0.75, 0.50) = 0.50

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: rule 3 confidence < 0.85
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | — | — | 0.50 not below 0.50 |
| C2 | no | — | — | no enum excluded |
| C3 | no | — | — | no control arm |
| C3b | no | — | — | runs-in known |
| C4 | no | — | — | measurement row has true prediction and a false mapping (borderline) |
| C5 | no | — | — | no Timestamp value; card_mtime 22:28:38Z |
| C6 | no | — | — | no numeric threshold |
| C7 | yes | uncited | capped at <= 0.50 | names `timeout` on PATH, GNU vs BusyBox, macOS bash 3.2 without citing a discriminator row (D-3, D-4 exist at diagnosability-tasklist.md:11-12) |
| C8 | no | — | — | rows 1 and 3 exist with non-empty Status |

## Notes

- Line numbers are pre-amendment (+2 now); content matches.
- No behaviour-definition row for GNU `timeout` with a zero duration; the card relies on the parent's measurement.
