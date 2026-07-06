# Full impacted-suite summary (Step 5.1)

**Command:** `make sync-dev && uv run pytest tests/pr_submit/ tests/cli/reflect/ tests/audit/ -v`
**Overall:** 1672 passed, 7 failed, 1 skipped, 1 xpassed. EXIT 1.
**All 7 failures are PRE-EXISTING environmental issues — ZERO regressions from the FX3/FX5/FX7/FX2/FX1 changes.**

## FX deliverables — all green
| Surface | Result |
|---------|--------|
| FX3 + FX5 (`test_setup_questions_resolution`, `test_gate_helper_differentials`, `test_gate_helper_coverage`) | 37 / 37 PASSED |
| FX7 (`test_fx7_*`) | 6 / 6 PASSED |
| Preserved routing (`test_r2f2`, `test_i1`, `test_i3`, `test_verification_skip_exemption_not_degraded`) | 4 / 4 PASSED |
| FX2 audit tripwires + FX1 reviewer guards (`test_five_axes_overlay`, `test_axis_column_populated`, `test_severity_floor_unweakened`, `test_reviewer_readonly_tools`, …) | 33 / 33 PASSED |

## The 7 failures — classified PRE-EXISTING (not regressions)

### (1) 6 × missing-hook-script failures (documented at Step 2.8)
`test_hook_update.py` (×4: `test_hook_points_at_src_source`, `test_t701_offer_mentions_both_commands`,
`test_t702_non_matching_command_exits_zero`, `test_t703_failed_pr_create_exits_zero`) +
`test_static_grep.py` (×2: `test_t104_every_gh_call_is_repo_scoped`, `test_tn40_no_depth_quick_fix_anywhere`).
Root cause: `src/superclaude/hooks/scripts/offer-pr-review.sh` is NOT git-tracked and absent at HEAD 46a787da
(a pre-existing worktree gap). None of the FX changes touch hooks.

### (2) 1 × pre-existing old-task-dir naming failure (new to this run's scope)
`test_invariant_preservation_NFR_6_through_10.py::TestInvariant3_PersistentArtifact::test_task_id_naming_pattern_preserved`.
Root cause: the test scans EVERY dir in `.dev/tasks/{to-do,done}/` and asserts `^TASK-(E2E|PRD|RESEARCH|RF|TDD|RC|MERGE|SC)-...`.
It flags 5 **pre-existing OLD** task dirs (`TASK-pr-submit-defaults-20260616`, `TASK-RF-pr-submit-v11-20260612-013419`,
`TASK-STDIN-RECON-REMEDIATION-20260501`, `TASK-RF-tasklist-rfmerge-20260619-041423`,
`TASK-RF-reflect-d1d4-fix-20260623-192000`) that predate this task by weeks/months and carry git-tracked files.
**This task's own dir `TASK-RF-qa-reflect-harden-20260703-044500` MATCHES the pattern (it is NOT in the failing list).**
This failure is independent of the FX changes — the offending dirs existed before this task and the FX work
touches neither `.dev/tasks/` naming nor the audit test. It was simply not in scope until this step ran the
full `tests/audit/` set (earlier steps ran only the specific FX2 tripwires).

## Verdict inputs
- All FX deliverable tests + all FX2/FX1 tripwire/guard tests green.
- No pre-existing `test_contract_setup_*`, `tests/cli/reflect/*`, or FX2-guarded audit test regressed.
- The 7 failures are pre-existing worktree-state issues (missing untracked hook + old non-conforming task
  dirs), NOT non-additive regressions — no FX revert applies under Step 5.1's clause.
- The POST reflect wrapper (Step PC.11) audits only changes since `start_commit` 46a787da, so these
  pre-existing failures are outside its diff scope. Flagged for final-gate/operator awareness.
