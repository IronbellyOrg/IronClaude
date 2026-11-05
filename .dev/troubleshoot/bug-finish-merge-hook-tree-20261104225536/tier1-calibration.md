# Calibration Report

**Card under calibration**: .dev/troubleshoot/bug-finish-merge-hook-tree-20261104225536/tier1-hypothesis.md
**Rubric**: ~/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-04T22:59:31Z
(persisted by the orchestrator on receipt from the confidence-calibrator agent; content condensed, scores and verdict verbatim)

## Per-dimension scores

| Dimension | Score | Justification |
|---|---|---|
| Evidence grounding | 1.0 | E1 matches probe-c4.out:1-5; E2 finish-merge.sh:261-270; E3/E4 by quoted content (tier1-observation.md:2; working-copy commit line 278, step 8 checks 299-302 unchanged); E5 conflict-mechanical.md:124; E6 test_conflict_scripts.py:960-979 |
| Runtime check | 1.0 | runtime_behavior x runtime_repro; executed probe with captured output against the unfixed script |
| Symptom coverage | 1.0 | exit 0, differing tree, clean work tree all explained (behaviour (a), (b)) |
| Reproducibility fit | 1.0 | deterministic trigger |
| Fix directness | 1.0 | write-tree after step 5 and a HEAD^{tree} comparison in step 8 |
| Domain coherence | 1.0 | one script's missing post-condition (stricter reading 0.5 would ESCALATE multi_domain; recorded) |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|---|---|---|
| arithmetic_mean(all_six) | 1.00 | |
| gate_M1: evidence_grounding + 0.30 | 1.30 | |
| gate_M2: runtime_check + 0.30 | 1.30 | |
| gated_min | 1.00 | |
| verdict_cap | none | runtime_check 1.0 |
| **calibrated** | 1.00 | |
| spot_check_unverifiable | none | |
| structural_flags | none | |

## Confidence

- **Self-reported (in card)**: 0.93
- **Calibrated (this report)**: 1.00
- **Formula applied**: min(1.00, 1.30, 1.30) = 1.00

## Escalation recommendation

- **Verdict**: `STOP`
- **Reason**: `none`
- **Rubric rule fired**: Rule 4 (confidence >= 0.85, single-domain, reproducible -> STOP at Tier 1)
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | — | — | no enum token; 1.00 |
| C2 | no | — | — | no enum exclusion |
| C3 | no | — | — | no control arm cited |
| C3b | no | — | — | runs-in stated, matches execution-locus.md:2-3 |
| C4 | no | — | — | P-1/P-2 carry true and false outcomes (diagnosability-tasklist.md:6-7) |
| C5 | no | — | — | no Timestamp value |
| C6 | no | — | — | no threshold |
| C7 | no | — | — | no environment-dependence claim (SAME-ENV yes) |
| C8 | no | — | — | row 1 observed:probe-c4.out:3-5 |

## Notes

- Verdict sensitivity: Domain coherence read strictly as "logic + tests" (0.5) gives 0.92 and ESCALATE multi_domain.
- Fix-side verification (P-1 negative witness, P-1/P-2 pass) rests on the audit.log entry; the tasklist rows still read pending.
- audit.log "on the fixed script at 62121669" means the round-1 fix commit, before this C4 fix.
