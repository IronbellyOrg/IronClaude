# Calibration Report

**Card under calibration**: .dev/troubleshoot/bug-finish-merge-marker-gate-20261104215930/tier1-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-04T22:06:00Z
(persisted by the orchestrator on receipt from the confidence-calibrator agent; content condensed, scores and verdict verbatim)

## Per-dimension scores

`runtime_observed` mapped to `runtime_repro` (executed probe with captured output).

| Dimension | Score | Justification |
|---|---|---|
| Evidence grounding | 1.0 | finish-merge.sh:208 (width-7 regex used at :224, :229); conflict-mechanical.md:76 (no marker-size override); finish-merge.sh:246-249 (ids only); test_conflict_scripts.py:775-827 (F2-F5 7-wide/content-only) |
| Runtime check | 1.0 | mixed = min(static 1.0, runtime_repro 1.0); probe-finish.out:1-4 (A1 exit 0 with 9-wide markers), :5-9 (C2 mode change committed as 100644) |
| Symptom coverage | 1.0 | both findings explained and reproduced |
| Reproducibility fit | 1.0 | deterministic; falsification prediction matched |
| Fix directness | 1.0 | exact sites and forms in finish-merge.sh:205-251 plus regression tests |
| Domain coherence | 1.0 | single domain (finish-gate index inspection) |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|---|---|---|
| arithmetic_mean(all_six) | 1.00 | |
| gate_M1: evidence_grounding + 0.30 | 1.30 | |
| gate_M2: runtime_check + 0.30 | 1.30 | |
| gated_min | 1.00 | |
| verdict_cap | none | M3a needs claim_class runtime_behavior |
| **calibrated** | 1.00 | |
| spot_check_unverifiable | none | |
| structural_flags | none | C6/C7/C4 borderline, not fired |

## Confidence

- **Self-reported (in card)**: 0.65
- **Calibrated (this report)**: 1.00
- **Formula applied**: min(1.00, 1.30, 1.30) = 1.00

## Escalation recommendation

- **Verdict**: `STOP`
- **Reason**: `none`
- **Rubric rule fired**: Rule 4 (confidence >= 0.85 AND single-domain AND reproducible -> STOP at Tier 1)
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | — | — | headline has no enum token; calibrated 1.00 |
| C2 | no | — | — | no enum excluded |
| C3 | no | — | — | no control arm cited |
| C3b | no | — | — | runs-in known (tier1-hypothesis.md:11; execution-locus.md:2) |
| C4 | no | — | — | borderline: preregistered prediction (card Falsification standard); tasklist P-1/P-2 |
| C5 | no | — | — | card Timestamp line carries no value |
| C6 | no | — | — | borderline: no bracket.md; 7 is a code constant |
| C7 | no | — | — | borderline: SAME-ENV yes; no env-dependent claim |
| C8 | no | — | — | behaviour-definitions.md rows 1-3 with Status matching probe-finish.out |

## Notes

- Card scope covers :208 and :246-249 (C2) though flags_context.scope names :208 only; orchestrator accepts both (the dispatch seed names both findings).
- Unobserved sub-claims: symlink swap (F6b), widths other than 9, `{7,}` missing widths below 7; regression tests P-1/P-2 close the reported gaps.
- Test naming: test_f6_foreign_merge_and_no_merge_head already exists (test_conflict_scripts.py:830); new cases need different names.
