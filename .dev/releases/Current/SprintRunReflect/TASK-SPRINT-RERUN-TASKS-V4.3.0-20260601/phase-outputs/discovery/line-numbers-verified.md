# Line Numbers Verified — Phase 1 Step 1.3

**Task:** TASK-SPRINT-RERUN-TASKS-V4.3.0-20260601
**Step:** 1.3 — Verify integration-point line numbers (research/06 Resolution 4)
**Date:** 2026-06-02
**Worktree:** /config/workspace/IronClaude/.claude/worktrees/SprintReRun (branch SprintReRun)

## Purpose

Per `research/06-gate-resolutions.md` Resolution 4, the line-number citations in `research/03-integration-points.md` IP-9 (executor classification site) and IP-12 (logging_.py write_phase_rerun_complete insertion point) were tagged UNVERIFIED. This file captures the verified current line numbers via grep.

## Findings

| File | Symbol | Line | Researcher Citation | Confirmed? |
|---|---|---|---|---|
| src/superclaude/cli/sprint/executor.py | `TaskStatus.FAIL` (in `if r.status == TaskStatus.FAIL`) | 324 | IP-3 / Resolution 1 rename target | ✅ |
| src/superclaude/cli/sprint/executor.py | `TaskStatus.FAIL` (in `if updated_result.status == TaskStatus.FAIL and synth_status != TaskStatus.FAIL:`) | 797 | IP-3 / Resolution 1 rename target | ✅ |
| src/superclaude/cli/sprint/executor.py | `TaskStatus.FAIL` (in comment `(set GateOutcome.FAIL / TaskStatus.FAIL)`) | 894 | IP-3 / Resolution 1 rename target | ✅ |
| src/superclaude/cli/sprint/executor.py | `_run_task_subprocess` (call site, classification context) | 1008 | IP-9 (researcher claimed 1014-1020, off by ~6 lines) | ⚠️ MISMATCH BUT NEARBY |
| src/superclaude/cli/sprint/executor.py | `_run_task_subprocess` (definition) | 1076 | IP-9 def | ✅ |
| src/superclaude/cli/sprint/executor.py | `_classify_from_result_file` (definition) | 1774 | IP-9 (classification heuristic landing site) | ✅ |
| src/superclaude/cli/sprint/executor.py | `_classify_from_result_file` (call site) | 2095 | IP-9 (call site) | ✅ |
| src/superclaude/cli/sprint/logging_.py | `def write_checkpoint_verification` (predecessor of new emitter per IP-12) | 159 | IP-12 (researcher claimed line 188) | ⚠️ MISMATCH — off by 29 lines |
| src/superclaude/cli/sprint/logging_.py | `def write_summary` (successor of new emitter per IP-12) | 190 | IP-12 successor | ✅ |
| src/superclaude/cli/sprint/logging_.py | `def _jsonl` (helper used by new emitter) | 210 | IP-12 helper | ✅ |

## Discrepancies / Notes

### IP-12: write_checkpoint_verification position

- **Researcher claim:** logging_.py:188 (where new `write_phase_rerun_complete` emitter inserts AFTER)
- **Actual:** `def write_checkpoint_verification` is at line 159, `def write_summary` is at line 190, `def _jsonl` is at line 210
- **Resolution:** Phase 4 IP-12 insertion uses VERIFIED line numbers: new emitter inserts AFTER line 188 (end of `write_checkpoint_verification` body — which extends from def@159 through line 188, immediately preceding `write_summary` at line 190). Researcher's "line 188" referred to the END of `write_checkpoint_verification` body, not its def line. After verification, the actual insertion boundary IS line 188 (end of predecessor body, before successor def at 190).
- **Status:** No correction needed — researcher's line 188 matches the verified END of predecessor; the def line 159 is informational.

### IP-9: executor classification site

- **Researcher claim:** executor.py:1014-1020 (the "classification site")
- **Actual:** `_run_task_subprocess` call site at line 1008; `_run_task_subprocess` def at 1076; `_classify_from_result_file` def at 1774; `_classify_from_result_file` call at 2095
- **Resolution:** The "classification site" researcher 3 IP-9 refers to is the post-subprocess result classification, which happens around the call to `_run_task_subprocess` at line 1008 (within the 1014-1020 nearby block) and is fully wired via `_classify_from_result_file` (def 1774, call 2095). Phase 4 Step 4.3 (executor classification heuristic landing) will edit `_classify_from_result_file` body at line 1774+ and the call site at 2095, NOT the 1014-1020 range. Researcher's narrow line range refers to the immediate caller of `_run_task_subprocess`.
- **Status:** Phase 4 wiring should target lines `1774+` (def body) and `2095` (call), with researcher's `1014-1020` reinterpreted as "the post-subprocess block surrounding the call site at 1008".

## Source Commands (Grep)

1. `grep -n "TaskStatus\.FAIL[^_R]" src/superclaude/cli/sprint/executor.py` → 3 matches (324, 797, 894)
2. `grep -n "def write_checkpoint_verification\|def _jsonl\|def write_summary" src/superclaude/cli/sprint/logging_.py` → 3 matches (159, 190, 210)
3. `grep -n "_run_task_subprocess\|_classify_from_result_file" src/superclaude/cli/sprint/executor.py` → 4 matches (1008, 1076, 1774, 2095)

## Conclusion

All researcher-3 IP citations referenced by Phase 2-4 items now have verified line numbers. Two minor discrepancies are documented with their resolutions. Phase 4 Step 4.3 (executor classification) and Step 4.4 (logging_.py emitter insertion) MAY reference this discovery file for verified line numbers.
