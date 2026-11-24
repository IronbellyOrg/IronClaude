# Calibration Report

**Card under calibration**: ./tier1-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-23T19:23:18Z

Resolved claim_class=static_defect, evidence_class=source_static, verdict_direction=AFFIRM from card body; none defaulted. No dynamic-control-flow misdeclaration found. Parent persistence of independent confidence-calibrator result.

## Per-dimension scores

| Dimension | Score | Justification |
|---|---|---|
| Evidence grounding | 1.0 | Read commands.py:438,3785; command-reference.md:56-60; producers.md:7-8; both captured help passages and run-rejection.txt:4; cited tests at test_commands_run.py:192-216 all match. |
| Runtime check | 1.0 | Static defect/source_static inherits EG. Parent captures corroborate only. Proposed tests and five pending tasklist rows not counted. |
| Symptom coverage | 1.0 | Both help producers and run rejection covered. run-help path placeholder is not the advertised flag. |
| Reproducibility fit | 1.0 | Deterministic wording and supplied public CLI captures match current worktree. |
| Fix directness | 1.0 | Two localized wording changes, no new flag. |
| Domain coherence | 1.0 | CLI help wording/interface domain; verification tests do not add another cause domain. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|---|---|---|
| arithmetic_mean(all_six) | 1.00 | Six scores of1.0. |
| gate_M1: evidence_grounding + 0.30 | 1.30 | Not binding. |
| gate_M2: runtime_check + 0.30 | 1.30 | Not binding. |
| gated_min | 1.00 | min(1.00,1.30,1.30). |
| verdict_cap | none | Not runtime_behavior. |
| **calibrated** | 1.00 | No structural cap fired. |
| spot_check_unverifiable | none | No remote URLs cited. |
| structural_flags | none | C8 skipped, input absent. |

## Confidence

- **Self-reported (in card)**: 0.95, not scoring input.
- **Calibrated (this report)**: 1.00
- **Formula applied**: min(mean(all_six),evidence_grounding+0.30,runtime_check+0.30)=min(1.00,1.30,1.30)=1.00. No assertion adjustment or verdict/structural cap.
- **Delta**: +0.05; all rubric anchors met for bounded literal wording claim, not repair or job semantics.

## Escalation recommendation

- **Verdict**: STOP
- **Reason**: none
- **Rubric rule fired**: Rule1, depth quick stops at Tier1. Default rule4 also stops on confidence>=0.85, single-domain, reproducible.
- **Execution restriction**: depth quick forbids Tier2 fan-out.

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | none | none | Wording headline is not enum, calibrated1.00. |
| C2 | no | none | none | No enum excluded. Adding a flag is a rejected alternative, not enum exclusion. |
| C3 | no | none | none | No control arm cited as proven; card/tasklist explicitly deny it. |
| C3b | no | none | none | runs-in=current-worktree, not unknown; SAME-ENV field is separate. |
| C4 | no | none | none | All tasklist rows have true/false or justified unknown predictions and mappings; equal predictions legitimate. No enabling task. |
| C5 | no | none | none | Card19:18:41Z is earlier than supplied mtime19:23:12Z+5min, not midnight. |
| C6 | no | none | none | No numeric threshold/bracket headline. |
| C7 | no | none | none | No environment property asserted; different installation is a falsifier only. |
| C8 | skipped | none | none | input absent: behaviour_definitions_path=null. |

## Notes

- Captured help and rejection outputs were read; exit statuses are parent-reported (capture files contain text, not exits). This does not drive static-defect score.
- Five tasklist rows, new regressions and repaired-state witness remain unexecuted/unobserved, never counted as passing.
- Sensitivity only, not retained alternate scores: source-plus-tests domain score0.5 would yield0.92 and multi_domain; asserting the installation alternative rather than listing a falsifier would fire C7 cap0.5. Neither reading was selected.
- Adjacent run-help contains <custom-prompt-dir>/system.txt as a path placeholder, not the option; outside two-passage defect, no unsolicited change recommended.
- Input absent behaviour_definitions_path; C8 skipped. Other supplied metadata/locus/tasklist/rubric inputs read.
- Zero findings: all cited snippets verified independently; no rule fired, no quota findings invented.
