# Calibration Report

**Card under calibration**: /home/coder/workspaces/worktrees/IronClaude/issue-751/.dev/troubleshoot/bug-issue-watcher-never-retries-failed-20261123222116/tier1-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-23T22:22:28Z
(persisted by the orchestrator from the confidence-calibrator agent's returned report)

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 1.0 | Every cited file:line was read and matches: dispatch.py:415, 425-427 (only first_run call, gated on `generated`), 428-436 (`not_enabled` skip), generate.py:252/256, cycle.py:398-401, first_run.py:136-137, 138, 170, 176-183, 208-216. |
| Runtime check | 1.0 | static_defect / source_static inherits Evidence grounding; claim is call-site structure of run_sweep. |
| Symptom coverage | 1.0 | Ties the stuck `enabled: false` state to first_run running only on generation; label, state, lock and flag staying manual follow from that. Issue text not seen by the calibrator. |
| Reproducibility fit | 0.5 | Deterministic, but no reproducer or test run in Tier 1. |
| Fix directness | 0.5 | Targets the exact code near dispatch.py:428; the retry-eligibility marker (failed first-run report) is a design choice; back-off and step-restriction questions are open. |
| Domain coherence | 1.0 | Single module (dispatch.py). |

## Stage-2 trace

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.83 | (1.0+1.0+1.0+0.5+0.5+1.0)/6 |
| gate_M1: evidence_grounding + 0.30 | 1.30 | not binding |
| gate_M2: runtime_check + 0.30 | 1.30 | not binding |
| gated_min | 0.83 | the mean binds |
| verdict_cap | none | claim_class static_defect |
| **calibrated** | 0.83 | final |
| structural_flags | none | C6 and C8 skipped (inputs absent) |

## Confidence

- Self-reported (in card): 0.90
- **Calibrated (this report)**: 0.83
- Formula: min(0.83, 1.30, 1.30) = 0.83. Delta -0.07.

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence` (rubric rule 3, confidence < 0.85)
- Execution restriction: none

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| C1 | no | - | - | 0.83 is not below 0.50 |
| C2 | no | - | - | alternatives reject fix designs, not enum exits |
| C3 | no | - | - | no control arm cited |
| C3b | no | - | - | SAME-ENV: yes (execution-locus.md) |
| C4 | no | - | - | no measurement row |
| C5 | no | - | - | timestamp within mtime + 5 min |
| C6 | skipped | - | - | input absent: tasklist_path |
| C7 | no | - | - | no environment property named |
| C8 | skipped | - | - | input absent: behaviour_definitions_path |

## Notes

- "Only call site" claim confirmed afterwards by the orchestrator: `grep -rn "first_run(" src tests` shows one production call (dispatch.py:427).
- Escalation should target the two 0.5 dimensions: a reproducer or test of failed first run then second sweep, and the retry-eligibility marker choice.
