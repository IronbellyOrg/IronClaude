# Calibration Report

(Persisted by the parent from the confidence-calibrator return; justifications shortened, scores and trace as returned.)

**Card under calibration**: /home/coder/workspaces/IronClaude/.dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/tier2-system-architect-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-17T19:09:47Z

Declared `claim_class: runtime_behavior`, `evidence_class: runtime_trace`, `verdict_direction: AFFIRM`; not a misdeclared static defect.

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 1.0 | Read at each spot-check: I:1383, I:1403, I:1594-1609, I:1610-1618, I:520 (`python3 - "$PROJECTS_DIR" <<'PY'`), I:1674-1675 (retention.py guard). The `stat`, `date` and `ls -t` spawns sit inside helper functions, not the cited range (small imprecision). Not re-read: I:132, I:934, I:1851, I:2054-2055. |
| Runtime check | 1.0 | Cross-tab (`runtime_behavior`, `runtime_trace`) gives 1.0: captured `bash -x` trace, Arms 1-3 and the `local`/export probe (behaviour-definitions.md row 1); the proposed savings (2.7 s to 14.6 s) are derived arithmetic and no patch was executed, carried into Fix directness. |
| Symptom coverage | 0.5 | Explains the 27.07 s wall time, not the reported 5-10% CPU (the card says so). |
| Reproducibility fit | 1.0 | Listing is deterministic and was re-run by trace and probe arms. |
| Fix directness | 0.5 | Right place but two stages; helper unwritten; cold-cache cost unknown; `ensure_names_migrated` unverified. |
| Domain coherence | 1.0 | Single domain: performance of a bash script. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.83 | (1.0+1.0+0.5+1.0+0.5+1.0)/6 = 0.8333 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | not binding |
| gate_M2: runtime_check + 0.30 | 1.30 | not binding |
| gated_min | 0.83 | |
| verdict_cap | none | runtime_check is 1.0: M3a does not apply |
| **calibrated** | 0.83 | no structural cap fired |
| spot_check_unverifiable | none | no remote URLs cited |
| structural_flags | none | C1-C8 evaluated; none fired |

## Confidence

- **Self-reported (in card)**: 0.72 (not used as input)
- **Calibrated (this report)**: 0.83
- **Formula applied**: `min(0.83, 1.30, 1.30)` = 0.83; no verdict cap; no structural cap.
- **Delta**: +0.11 (the card scored its own Runtime check at 0.5 because the savings were not executed; the cross-tab scores the evidence class at 1.0).

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `forced_by_depth_deep` (rule 2; rule 3 would give `low_confidence` at 0.83)
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | none | none | calibrated 0.83 is not below 0.50 |
| C2 | no | none | none | the card excludes design options, not enum tokens |
| C3 | no | none | none | no control arm with a CONTROL-PROOF claim; the reference-arm value is explicitly "not captured" (card lines 68, 70) |
| C3b | no | none | none | `runs-in=coder workspace, one bash process` (card line 9); execution-locus.md:4-5 |
| C4 | no | none | none | discriminator has pre-registered outcomes and a falsifier (card lines 69-70); success measure stated (line 82) |
| C5 | no | none | none | card says "Timestamp: not supplied"; card_mtime 2026-11-17T19:09:33Z |
| C6 | no | none | none | the headline asserts no numeric threshold; 13.5 s is in the falsification standard |
| C7 | no | none | none | environment facts cite tier1-observation.md and behaviour-definitions.md rows 1-3; no separate 2x2 artifact |
| C8 | no | none | none | behaviour-definitions.md:7-9 rows 1-3 exist with Status "observed in this run" |

## Notes

- No defaulted or missing inputs.
- Unverified on the card: BSD `date -d`, Python birth time, the macOS `python3` stub, bash 3.2 behaviour, cold-cache cost; none is load-bearing for the 1.0 scores; the BSD `date -d` and Python birth-time rows are not in behaviour-definitions.md (only the three observed rows).
- The card admits the discriminator's reference arm was never captured, so Runtime check was scored on the trace and arms evidence.
- Post-card probe (not graded): plain 22.5-24.7 s vs `LC_ALL=C` 16.2-16.7 s: about 6-7 s saved, close to the card's derived 6.22 s stage 1 locale saving.
- Main residual risk (the card's own): cold-cache disk reads may dominate session_home, which would shrink stage 2's gain.
