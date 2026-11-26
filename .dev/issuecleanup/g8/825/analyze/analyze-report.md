# /sc:analyze report: launch-level-guard.sh (issue 825)

Target: src/superclaude/hooks/scripts/launch-level-guard.sh. Focus: architecture. Depth: quick. Read against origin/integration at 4e35750e7 (the local worktree HEAD a7ae3dd30 differs from it only in launch-level-pre-push.sh and orca_worktree.py, per `git diff --stat`; the guard file is identical).

Codegraph: index_state=fresh, checked_at=2026-11-25T00:56:58Z; degraded: none (status only; findings below were confirmed by Grep and git show, no graph row is cited)

## Findings

| # | Severity | Finding | Evidence |
|---|---|---|---|
| 1 | Medium | The protected-branch set is hard-coded twice and the two layers disagree. L1 treats only `master` and `main` as protected; L2 treats `main`, `master`, `integration`. | guard.sh:736 `case $LL_D in master | main) ... PROTECTED`; pre-push.sh:17 `L2_PROTECTED=(refs/heads/main refs/heads/master refs/heads/integration)`; orca_worktree.py:1363 lists all three |
| 2 | Low | Refusal text names only master or main. | guard.sh:59,60 |
| 3 | Low | Stale L2 conflict message prints the `rm` command but not the version found. | orca_worktree.py:1278-1283 `_l2_conflict`, 1306 (`stale` vs `foreign` by prefix only) |
| 4 | Low | No L1 test covers `integration`; L2 test does. | tests/hooks/test_launch_level_guard.py: 0 hits; test_launch_level_pre_push.py:49 BRANCHES includes integration |
| 5 | Low | Design doc still describes L2 version 1 and a two-ref list. | docs/designs/sc-issue-launch-level-hook.md:516 (`version: 1`), :32, :241, :379, :522 |

## Architecture note

Layering is intact: L1 (text classifier) assigns class PROTECTED (guard.sh:736) and denies it for levels W, WA, F, FS (guard.sh:812). L2 (git pre-push) is the structural backstop. The gap is a single list in L1 that was not updated when PR 824 moved the default branch to integration. The guard version line is `# launch-level-guard-version: 2` (orca_worktree.py:876), unchanged by PR 824.

## Recommendation

Add `integration` to guard.sh lines 59, 60, 736 and the plugins mirror, bump the guard version to 3 in the guard and orca_worktree.py, extend the L1 tests, update the design doc.
