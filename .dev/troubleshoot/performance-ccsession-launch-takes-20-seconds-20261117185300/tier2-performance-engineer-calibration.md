# Calibration Report

(Persisted by the parent from the confidence-calibrator return; justifications shortened, scores, trace and rule rows as returned.)

**Card under calibration**: /home/coder/workspaces/IronClaude/.dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/tier2-performance-engineer-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-17T19:09:47Z

Declared `claim_class: mixed`, `evidence_class: runtime_trace`, `verdict_direction: AFFIRM`; no static_defect misdeclaration.

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 1.0 | Every ccsession citation read and matching: I:1383, I:1396-1397 (no `LC_ALL=` prefix on grep or awk), I:1594-1627, I:1636, I:686/689/694 (command-prefix form), I:1405, I:1386-1389, I:1490, I:1516. |
| Runtime check | 1.0 | Cross-tab mixed x runtime_trace = 1.0; the reproducer was executed with captured output (27.069 s, a bash -x trace, Arms 1-3). The card scores itself 0.5 because the proposed change was never run; the calibrator treats that as a Fix directness matter. |
| Symptom coverage | 0.5 | Explains the wall time and list-size dependence; says plainly it does not explain the reported 5-10% CPU (about 2.5% of this machine); leaves a user-time inconsistency unresolved (whole-run user 5.823 s vs Arm 3 user 9.992 s). |
| Reproducibility fit | 1.0 | Reproduced on the same machine and user; execution-locus.md says SAME-ENV: yes. |
| Fix directness | 0.5 | One file, about 45 lines; most savings estimates borrow `date`'s 1.53 ms per spawn for dirname, basename and head (unverified); the `ls -t` to glob-plus-`-nt` tie-break is unmeasured; test file not read. |
| Domain coherence | 1.0 | One domain: performance in one bash script. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.83 | (1.0 + 1.0 + 0.5 + 1.0 + 0.5 + 1.0) / 6 = 0.8333 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | does not bind |
| gate_M2: runtime_check + 0.30 | 1.30 | does not bind |
| gated_min | 0.83 | min(0.8333, 1.30, 1.30) |
| verdict_cap | none | M3a applies only to a declared `runtime_behavior` claim; this card is `mixed`; a 0.84 AFFIRM cap would not have bound anyway |
| **calibrated** | 0.50 | 0.83 reduced by the C7 cap (0.5) |
| spot_check_unverifiable | none | no remote URLs cited |
| structural_flags | C3 (`control_unproven`, no numeric effect), C7 (`uncited`, cap 0.5) | caps applied after the formula; C3 effect nil because Symptom coverage was already 0.5 |

## Confidence

- **Self-reported (in card)**: 0.62 cost model and ranking; 0.55 that lever (a) alone delivers 6.2-6.8 s; 0.75 that (a)+(b) lands in 11.6-14.1 s (not used as input)
- **Calibrated (this report)**: 0.50
- **Formula applied**: `min(0.83, 1.30, 1.30)` = 0.83; no verdict-direction cap; the C7 cap of 0.5 gives min(0.83, 0.50) = 0.50; C6 and C8 did not fire.
- **Delta**: -0.12 against the headline self-report of 0.62; without the C7 cap the figure would be 0.83.

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `forced_by_depth_deep` (rule 2; rule 3 `confidence < 0.85` would also fire)
- **Execution restriction**: none

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| C1 | no | none | none | headline has no enum token; calibrated 0.50 is not below 0.50 |
| C2 | no | none | none | the card excludes approaches (python helper, N-row bound, disk cache), not enums |
| C3 | yes | `control_unproven` | Symptom coverage <= 0.5 (already 0.5, no change) | the card uses Arm 2 (the C-locale arm) as the counterfactual for lever (a); execution-locus.md has no `CONTROL-PROOF: yes: <file:line>` line |
| C3b | no | none | none | runs-in "coder workspace, one bash process"; execution-locus.md:4 |
| C4 | no | none | none | locale-gain discriminator has pre-registered outcomes and a falsifier |
| C5 | no | none | none | Timestamp line says time of day not observed; card_mtime 2026-11-17T19:08:35Z |
| C6 | no | none | none | headline numbers are estimated savings ranges, not an asserted threshold or bracket; bracket.md does not exist |
| C7 | yes | `uncited` | calibrated <= 0.5 (cap) | the card names environment properties (LANG=C.UTF-8, load average 11.9, a 28-core machine) and cites no 2x2 row; none appears in tier1-observation.md, diagnosability-tasklist.md or execution-locus.md |
| C8 | no | none | none | behaviour-definitions.md row 1 matches the card's `bash -c ... printed 0` citation; Status "observed in this run" |

## Notes

- C7 decides the final number. The rule needs a "2x2 row" and none exists in any supplied artifact; the card does cite Arm 2 vs Arm 3 and behaviour-definition row 1 for the locale property. If a 2x2 row covers locale, C7 does not fire and the calibrated score is 0.83. The verdict is ESCALATE either way (depth deep; 0.83 < 0.85).
- C6: if the parent reads the savings ranges as a bracket, C6 would cap at 0.3.
- Runtime check divergence: the card self-scores 0.5, the calibrator 1.0 (unrun change and the unresolved user-time inconsistency are carried in Symptom coverage and Fix directness).
- Post-card probe (not scored): locale-probe.txt plain 23.586, 24.663, 22.471 s vs `LC_ALL=C` 16.657, 16.244, 16.597 s; gains 6.93, 8.42, 5.87 s, all at or above the card's 3.38 s threshold; the observed gains are somewhat larger than the card's 6.2-6.8 s estimate, from alternating end-to-end runs while machine load fell from about 9.8 to 4.2.
- Parent note on consistency (not part of the calibrator's report): the other two Tier 2 calibrators evaluated the same kind of environment mentions (LANG, load average 11.9) in their cards and did not fire C7 (judgement call, no 2x2 artifact defined); the 0.50 here is the value returned and is kept unchanged, and Wave 4 weighting treats it as the effective confidence of this card.
