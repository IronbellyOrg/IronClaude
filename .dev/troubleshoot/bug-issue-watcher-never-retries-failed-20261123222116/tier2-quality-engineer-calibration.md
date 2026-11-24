# Calibration Report

**Card under calibration**: /home/coder/workspaces/worktrees/IronClaude/issue-751/.dev/troubleshoot/bug-issue-watcher-never-retries-failed-20261123222116/tier2-quality-engineer-hypothesis.md
**Rubric**: /home/coder/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-23T22:25:13Z
(persisted by the orchestrator from the confidence-calibrator agent's returned report)

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 1.0 | Cited ranges read and match (dispatch.py:425-429; first_run.py:78-83, 86-95, 136-137, 141-145, 154-161, 180-185, 211-212; test_dispatch.py:141-152, 421-426). Not read by card or calibrator: tests/sweep/test_probes_allowlist.py, full test_first_run.py and test_security_invariants.py (card lists these as gaps). |
| Runtime check | 1.0 | static_defect / source_static inherits Evidence grounding; no executed reproducer. |
| Symptom coverage | 0.5 | Explains why a failed first run is never retried; by its own admission leaves out failures that write no report (crash between ensure_config and first_run, unwritable report directory, stale report). |
| Reproducibility fit | 0.5 | Deterministic, but no reproducer attempted. |
| Fix directness | 0.5 | Fix is in the right place; marker choice is an owner design decision and an explicit "needs first run" marker is offered as possibly better. |
| Domain coherence | 1.0 | One module plus its test file. |

## Stage-2 trace

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | 0.75 | (1.0+1.0+0.5+0.5+0.5+1.0)/6 |
| gate_M1 / gate_M2 | 1.30 / 1.30 | not binding |
| gated_min | 0.75 | |
| verdict_cap | none | static_defect |
| **calibrated** | 0.75 | no structural cap lowers it |
| structural_flags | timestamp_invalid | C5 fired (drop the Timestamp line only) |

## Confidence

- Self-reported: 0.85. **Calibrated: 0.75.** Delta -0.10 (the card's own dimension scores average 0.75, not 0.85).

## Escalation recommendation

- **Verdict**: `ESCALATE`; **Reason**: `low_confidence` (rule 3); execution restriction: none.
- Card agrees with Tier 1, so it is not an independent competing cluster; no split_pending applies.

## Structural assertions

| id | fired | flag | consequence | evidence |
|---|---|---|---|---|
| C1 | no | - | - | 0.75 is not below 0.50 |
| C2 | no | - | - | no enum excluded |
| C3 | skipped | - | - | SAME-ENV yes, no control arm cited |
| C3b | no | - | - | runs-in known (execution-locus.md:3) |
| C4 | no | - | - | no measurement rows |
| C5 | yes | timestamp_invalid | Timestamp line `2026-11-23T22:40:00Z` dropped, not load-bearing | later than card_mtime 22:24:52Z + 5 min |
| C6 | skipped | - | - | input absent: tasklist_path |
| C7 | no | - | - | no environment property |
| C8 | skipped | - | - | input absent: behaviour_definitions_path |

## Notes

- Claim-class borderline: if treated as runtime_behavior, Runtime check would be 0.0 and the cap would be 0.30; ESCALATE holds either way.
- The card never cites where the generated config gets `enabled: false` (generate.py:252, cited in Tier 1).
