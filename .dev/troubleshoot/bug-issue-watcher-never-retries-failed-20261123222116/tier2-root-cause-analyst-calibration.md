# Calibration Report

**Card under calibration**: /home/coder/workspaces/worktrees/IronClaude/issue-751/.dev/troubleshoot/bug-issue-watcher-never-retries-failed-20261123222116/tier2-root-cause-analyst-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-23T22:25:13Z
(persisted by the orchestrator from the confidence-calibrator agent's returned report)

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 1.0 | Every cited range read and matched: dispatch.py:421-436, 210-215, 45; first_run.py:78-85, 138-145, 158-170, 180-185; cycle.py:59-71, 396-402; generate.py:249-258; the three cited tests at the stated lines. |
| Runtime check | 1.0 | static_defect / source_static inherits Evidence grounding; card states runtime check not performed. |
| Symptom coverage | 1.0 | Explains the whole symptom and covers the report location and unwritable-state-dir cases. |
| Reproducibility fit | 0.5 | Deterministic from control flow, but no reproducer run; falsification test proposed, not executed. |
| Fix directness | 0.5 | Right area (dispatch.py near :428 plus a first_run.py helper) but the retry gate/back-off is a design choice and the change reaches docs, skip-reason text and tests. |
| Domain coherence | 1.0 | Single domain: issue_watch dispatcher control flow. |

## Stage-2 trace

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.83 | (1.0+1.0+1.0+0.5+0.5+1.0)/6 |
| gate_M1 / gate_M2 | 1.30 / 1.30 | not binding |
| gated_min | 0.83 | |
| verdict_cap | none | static_defect |
| **calibrated** | 0.83 | final |
| structural_flags | none | C6 and C8 skipped (inputs absent) |

## Confidence

- Self-reported: 0.85. **Calibrated: 0.83.** Delta -0.02.

## Escalation recommendation

- **Verdict**: `ESCALATE`; **Reason**: `low_confidence` (rule 3); execution restriction: none.

## Structural assertions

| id | fired | flag | consequence | evidence |
|---|---|---|---|---|
| C1 | no | - | - | 0.83 is not below 0.50 |
| C2 | no | - | - | no enum excluded |
| C3 | no | - | - | no control arm cited |
| C3b | no | - | - | runs-in known |
| C4 | no | - | - | no measurement rows |
| C5 | no | - | - | timestamp 22:24:52Z within mtime + 5 min |
| C6 | skipped | - | - | input absent: tasklist_path |
| C7 | no | - | - | no environment property |
| C8 | skipped | - | - | input absent: behaviour_definitions_path |

## Notes

- "Generated configs always carry an absolute state_dir" holds only if `base.state_dir.expanduser()` is absolute (generate.py:249); minor, `_report_dir` falls back to `<stem>-first-run.txt` beside the config.
- Claim class static_defect accepted.
