# Calibration Report

(Persisted by the parent from the confidence-calibrator return; text kept as returned, shortened only in the Notes.)

**Card under calibration**: /home/coder/workspaces/IronClaude/.dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/tier1-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-17T19:04:15Z

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 1.0 | Cited lines in the installed script were read and match the card: session_home I:1377-1399 (pipeline 1396-1397), session_transcript I:1480-1483, get_btime/get_mtime I:1488-1531, format_epoch I:1533-1537 (`date -r` first, then `date -d`), I:1594-1617 (per-row spawns). Timing and process-count tables E1-E3 agree with tier1-observation.md. |
| Runtime check | 1.0 | Card declares `runtime_behavior` with `runtime_trace` (cross-tab 1.0): the parent ran `bash -x` with a PS4 timestamp and captured per-function self time, process counts and wall times; the 0.75 s prototype is a second executed run. |
| Symptom coverage | 0.5 | Explains the 27 s wall time and growth with list size; does not explain the reported 5-10% CPU (measured about 2.5% of this machine, marked unverified); spawn-versus-scan split inside the 12.16 s unresolved. |
| Reproducibility fit | 1.0 | `--here` (27.069 s) and `--list` (14.473 s) reproduced on the same machine; read-only reproducer and preregistered probe named. |
| Fix directness | 0.5 | Fix targets the identified code but needs a new helper script, tests and possibly installer manifest and README (at least three files); helper unwritten and must match pinned output formats. |
| Domain coherence | 1.0 | One cause domain: performance from per-session process spawning. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.83 | (1.0+1.0+0.5+1.0+0.5+1.0)/6 = 0.8333 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | does not bind |
| gate_M2: runtime_check + 0.30 | 1.30 | does not bind |
| gated_min | 0.83 | the mean binds |
| verdict_cap | none | runtime_check is 1.0, so M3a does not apply; verdict AFFIRM |
| **calibrated** | 0.83 | final |
| spot_check_unverifiable | none | no remote-URL citations |
| structural_flags | none | C7 and C8 skipped; no other C-rule fired |

## Confidence

- **Self-reported (in card)**: 0.80 (not used as input)
- **Calibrated (this report)**: 0.83
- **Formula applied**: `min(0.83, 1.30, 1.30) = 0.83`; no verdict cap, no structural cap; no assertion adjusted any dimension.
- **Delta**: +0.03

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `forced_by_depth_deep`
- **Rubric rule fired**: Rule 2 (`--depth deep` forces escalation); Rule 3 (`confidence < 0.85`, 0.83) would also fire but rule 2 is first.
- **Execution restriction**: none.

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| C1 | no | none | none | headline has no enum token; calibrated 0.83 is not below 0.50 |
| C2 | no | none | none | alternatives ruled out with measured shares, not by excluding an enum |
| C3 | no | none | none | no control arm cited; execution-locus.md has no CONTROL-PROOF line |
| C3b | no | none | none | execution-locus.md gives RUN-SITE and SAME-ENV: yes; card header has runs-in |
| C4 | no | none | none | falsification table maps all three outcomes; diagnosability-tasklist.md says `discriminator-required: no` |
| C5 | no | none | none | card has no Timestamp line; now_iso 19:04:15Z, card_mtime 19:04:01Z |
| C6 | no | none | none | 45% and about 14 per row are measured shares and counts |
| C7 | skipped | none | none | input absent: no 2x2 environment-comparison rows supplied |
| C8 | skipped | none | none | input absent: behaviour_definitions_path is null |

## Notes

- Every cited line read matches the card. Not read by the calibrator: I:1554-1589, I:1430-1478 (session_place), I:1733-1735; the card's own gaps list says tests, README and retention.py were not read.
- C7 skipped: environment properties (28 cores, load average 11.9, cold cache, smaller machine) appear only as unverified alternative explanations. If the orchestrator treated them as claims needing a 2x2 row, C7 would cap calibrated at 0.5; the recommendation would not change because depth deep forces ESCALATE.
- Post-card evidence, not graded: parent's probe Arm 1 1.44 s, Arm 2 6.46 s, Arm 3 13.23 s supports the card's second falsification row; the locale finding (I:1383 `local LC_ALL=C` not reaching grep) is a more specific cause inside the 12.16 s component, not a contradiction. Re-scoring would raise Symptom coverage, but the card as written stands at 0.83.
