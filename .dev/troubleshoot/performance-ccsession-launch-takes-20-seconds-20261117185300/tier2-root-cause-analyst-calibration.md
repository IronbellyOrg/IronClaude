# Calibration Report

(Persisted by the parent from the confidence-calibrator return; justifications shortened, scores and trace as returned.)

**Card under calibration**: /home/coder/workspaces/IronClaude/.dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/tier2-root-cause-analyst-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-17T19:09:47Z

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 1.0 | I:1383 `local store want cwd first="" LC_ALL=C` and I:1396-1397 (`head -c 262144 / tail -c 1048576 \| grep -oE ... \| awk`) match the card verbatim; self times, process counts and Arms 1-3 match tier1-observation.md. Not read by the calibrator: I:1480-1483, 1554-1663, 1595-1600, 1718, install.sh, the test files. |
| Runtime check | 1.0 | `mixed` claim with `runtime_trace` evidence scores 1.0 in the cross-tab; captured xtrace, Arms 1-3 and the `env \| grep -c` probe (printed 0). |
| Symptom coverage | 0.5 | Explains the 20 s delay and the 27.07 s reproduction; the reported 5-10% CPU stays unexplained (about 2.5% of this machine; a core-count guess marked unverified). |
| Reproducibility fit | 1.0 | Reproducer run and matches the cited cause; the Arm 2 vs Arm 3 gap is one run under load 11.9, covered by the card's own discriminator. |
| Fix directness | 0.5 | Right area, but a new Python helper plus bash fallback touching 3-4 files; helper unwritten; prototype omits the matching rule and session_place; the card calls it "a written-plan change". |
| Domain coherence | 1.0 | One domain: process spawning and environment handling in one shell script. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.83 | (1.0+1.0+0.5+1.0+0.5+1.0)/6 = 0.833 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | does not bind |
| gate_M2: runtime_check + 0.30 | 1.30 | does not bind |
| gated_min | 0.83 | the mean binds |
| verdict_cap | none | claim_class `mixed`, runtime_check 1.0: M3a not triggered |
| **calibrated** | 0.83 | final |
| spot_check_unverifiable | none | no remote URLs cited |
| structural_flags | none | C1-C8 evaluated; none fired |

## Confidence

- **Self-reported (in card)**: 0.80 diagnosis, 0.65 fix savings (not used as input)
- **Calibrated (this report)**: 0.83
- **Formula applied**: `min(0.833, 1.30, 1.30)` = 0.83; no verdict cap; no structural cap.
- **Delta**: +0.03

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `forced_by_depth_deep` (rule 2; rule 3 `confidence < 0.85` would also match at 0.83)
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | none | none | calibrated 0.83 is not below 0.50 |
| C2 | no | none | none | rejections are of ranking alternatives, not enum exits |
| C3 | no | none | none | the Arms are measurements, not a control arm; no CONTROL-PROOF line (if Arm 2 counted as a control, C3 would cap Symptom coverage at 0.5, already 0.5) |
| C3b | no | none | none | runs-in is "coder workspace, one bash process"; execution-locus.md:4 |
| C4 | no | none | none | discriminator has both outcomes pre-registered; the post-fix re-run is verification, not a diagnostic row |
| C5 | no | none | none | card timestamp "unobserved"; card_mtime 2026-11-17T19:08:05Z |
| C6 | no | none | none | "about 14 processes per saved name" is an observed count; bracket.md does not exist |
| C7 | no | none | none | environment property (LANG=C.UTF-8, LC_ALL unset) backed by a captured probe and behaviour-definitions.md row 1 (judgement: no 2x2 artifact defined) |
| C8 | no | none | none | behaviour-definitions.md rows 1-3 exist with Status "observed in this run" |

## Notes

- `mixed` with `runtime_trace` accepted; no misdeclaration; no defaulted inputs.
- Weakest spots: Arms 2 and 3 are single runs under load 11.9; the 5-10% CPU figure; the helper's row-order and cwd-rule equivalence is unproven.
- Post-card probe (not graded): locale-probe.txt plain 23.586, 24.663, 22.471 s (median 23.586) vs `LC_ALL=C` 16.657, 16.244, 16.597 s: gap about 6.99 s, above the card's 4.0 s threshold, so hypothesis A is consistent and B refuted at that size.
