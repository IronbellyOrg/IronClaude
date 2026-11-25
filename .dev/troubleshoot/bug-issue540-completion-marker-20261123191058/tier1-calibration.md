# Calibration Report

**Card under calibration**: /home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s/.dev/troubleshoot/bug-issue540-completion-marker-20261123191058/tier1-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-23T19:25:41Z

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|---|---|---|
| Evidence grounding | 1.0 | Calibrator read all source evidence ranges: commands.py:2145-2178,2578-2599 omit marker call; models.py:563-573 and commands.py:931-937 define/enable policy; reduce.py:701-704 emits contract and returns. Quotes match. |
| Runtime check | 1.0 | mixed/runtime_repro components each score1.0. Raw foreground/resume stdout, file-presence JSON, contract status and import-path artifacts match cited captures. Claim excludes detached/unsuccessful execution. |
| Symptom coverage | 1.0 | Explains exit0, success contract, terminal state and absent marker in both observed paths; does not claim unobserved paths. |
| Reproducibility fit | 1.0 | Two separate real CLI/stub runs with command provenance in tier1-observation.md:10-37 reproduce omission. |
| Fix directness | 1.0 | Proposal targets owning continuations using existing writer, plus tests/docs; no enabling-task or measurement C4 cap. |
| Domain coherence | 1.0 | Single completion-policy domain; dependent tests/docs are not separate cause domains. |

## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|---|---|---|
| arithmetic_mean(all_six) | 1.00 | (1+1+1+1+1+1)/6; no dimension adjustment |
| gate_M1: evidence_grounding + 0.30 | 1.30 | unconditional |
| gate_M2: runtime_check + 0.30 | 1.30 | unconditional |
| gated_min | 1.00 | min(1.00,1.30,1.30) |
| verdict_cap | none | mixed, runtime_check1.0, AFFIRM: M3a not binding |
| **calibrated** | 1.00 | no fired structural cap |
| spot_check_unverifiable | none | no remote evidence URLs |
| structural_flags | none | no fired C-rule; C8 skipped for absent optional input |

## Confidence

- **Self-reported (in card)**: 0.90 (read, not used as scoring input).
- **Calibrated (this report)**: 1.00
- **Formula applied**: min(mean(all_six), evidence_grounding+0.30, runtime_check+0.30)=min(1.00,1.30,1.30)=1.00. No dimension adjustment, verdict cap or structural cap changes the result.
- **Delta**: +0.10. All rubric anchors verified for the scoped integration cause; this is not a claim of repaired production readiness.
- **Retained bounds**: first valid independent calibration; no prior score/cap to carry forward.

## Escalation recommendation

- **Verdict**: `STOP`
- **Reason**: `none`
- **Rubric rule fired**: Rule4 Default: confidence>=0.85 AND single-domain AND reproducible -> STOP at Tier1. No Rule3 signal: confidence1.00, domain1.0, deterministic, reproducibility1.0, typebug, runtime1.0, no split cluster.
- **Execution restriction**: none; no_escalate=false, depth=standard; C1 not fired.

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| C1 | no | none | none | confidence1.00; headline at tier1-hypothesis.md:1 has no definite low-confidence enum |
| C2 | no | none | none | tier1-hypothesis.md:47,50 exclude no enum; writer/library is an alternative mechanism |
| C3 | no | none | none | tier1-hypothesis.md:47 cites no passing control; locus CONTROL-PROOF unknown |
| C3b | no | none | none | tier1-hypothesis.md:10 known runs-in; execution-locus.md:12 local SAME-ENV=yes |
| C4 | no | none | none | diagnosability-tasklist.md:16,28 zero measurement/enabling tasks; fix candidate is inert repair proposal |
| C5 | no | none | none | tier1-hypothesis.md:4 timestamp19:22:11 is before supplied mtime19:25:31, not midnight |
| C6 | no | none | none | tier1-hypothesis.md:1 asserts no numeric bracket; sibling bracket.md absent but no trigger |
| C7 | no | none | none | no environment-property cause; fresh output roots in Risks are mitigation, not mechanism |
| C8 | skipped | none | none | input absent: behaviour_definitions_path=null |

## Notes

No claim/evidence/verdict defaults applied; all declared. input_absent: behaviour_definitions_path; assertion_skipped:C8. bracket.md absent, C6 evaluated and not fired (no bracket asserted). Declared mixed is not a disguised static-defect claim: runtime wording has captured execution evidence. All cited evidence source ranges/artifacts were read and matched. The calibrator did not re-read reduce.py:383-440, tests/swarm/test_commands_run.py or README:116-120 because they are proposed targets, not evidence for the omission. Residual alternate publisher/failure possibility is disclosed in the card's falsification standard. Partial tasklist reflects missing built-in diagnostics, not unresolved observations, and does not alter rubric scores. Returned read-only report persisted by parent; no tests rerun by calibrator.
