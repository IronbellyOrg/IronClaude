# Static architecture analysis: src/superclaude/cli/issue_pipeline

Command: `/sc:analyze src/superclaude/cli/issue_pipeline --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/6/analyze`
Checked 2026-11-24T22:18:04Z against master `f2894fc44f6e68a7dd6a78c75f59683cb0b5acb9`, worktree `/home/coder/workspaces/worktrees/IronClaude/Realign`.
Codegraph: index_state=fresh, checked_at=2026-11-24T22:18:04Z; degraded: none

The path is the narrowest source home shared by issues 799, 800 and 801: it holds the only coordinator-side code on master (adoption rows, plan approval, `release-worker`, `complete`). Everything else those issues need is not built.

## Layout (codegraph_files, 10 files)

`cli.py` (41 symbols) is the Click group `issue_pipeline_group`; its commands are `plan-hash`, `check-approval`, `init`, `adopt-create`, `adopt-mark`, `record-create`, `record-show`, `record-mark`, `release-worker`, `complete`, `stage-status` (Grep `cli.py:62-409`). `approval_record.py` (48), `complete.py` (38), `stage_predicates.py` (20), `reads.py` (25), `brief.py` (11), `release.py` (11), `plan_hash.py` (10), `approval_line.py` (13).

## Findings

1. **No hand-back, branch-per-round or worktree check (issue 799).** Grep of the package for `worktree|branch` finds only prose: `brief.py:59` (pending note), `release.py:5,19,43,56` (the guard's worktree-level session record) and `templates/worker-brief.txt:6,15` (`Worktree: path:<existing worktree>`). No verb names a branch `issue-<N>-r<n>`, no `handback` verb exists, and nothing checks tracked-only changes. Severity: gap, as expected.
2. **No terminal settling (issue 800).** Grep for `terminal|reclaimable` in the package: no hit. The package has no call to Orca `worker-release`, `worker-retain` or `worker-list`. `release.py` is a different thing: it removes the launch-level guard's session record (`release(session_id, store)` at `release.py:38`, CLI `release-worker` at `cli.py:201`). Naming clash is real and lives in this package: `release-worker` (guard) versus Orca `worker-release` (terminal).
3. **No refuse list (issue 801).** The package has no `refuse(argv)`. The only text-matching guard is the shell hook `src/superclaude/hooks/scripts/launch-level-guard.sh` (outside this package), which already pattern-matches `release-worker` and `issue-pipeline ... adopt-`. Its `rm` hits (lines 295-344) are its own temp-file cleanup, not a deletion rule for a coordinator.
4. **Dependency direction is clean.** `release.py` is used by `cli.py`, `tests/hooks/test_launch_level_guard_worker.py` and `tests/issue_pipeline/test_release.py` (codegraph_node). Any new coordinator verb group would sit beside this package, not inside it, because R38 (requirements.md R38) keeps `issue-pipeline` as the adopted baseline.
5. **Architecture risk (medium).** `complete.py` (431 lines) and `approval_record.py` (416 lines) are the large files. A settle step for 800 or a round counter for 799 should be a new small module, not an addition to `complete.py`.

## Recommendations

- Treat the three items as additions beside `issue_pipeline`, not edits to it.
- Keep the Orca verb `worker-release` and the guard verb `release-worker` visibly different in any new text and test.
