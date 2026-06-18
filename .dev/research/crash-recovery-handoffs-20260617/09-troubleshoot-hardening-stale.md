# troubleshoot-hardening stale handoff

## Current state

- Target lane: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening`.
- Branch: `feat/troubleshoot-pipeline-hardening`.
- HEAD: `b9378c72e2d5acc12607316b10ef377110f7c5a3` (`feat(troubleshoot): Pipeline Hardening Closure mode (H0-H5 + waiver latch)`).
- Working tree state: clean for tracked and untracked files in the target lane. `git status --short --branch` reports only `## feat/troubleshoot-pipeline-hardening...origin/feat/troubleshoot-pipeline-hardening [gone]`.
- Upstream/tracking state: local branch still tracks `origin/feat/troubleshoot-pipeline-hardening`, but that remote ref is gone.
- Remote: `origin` is `https://github.com/IronbellyOrg/IronClaude.git`.
- Origin master currently points at `d12cad1d126b43c5f58199f600b36a276b3ed2e6` (`feat(pr-submit): default monitor to L1 (#177)`). Local `master` is older (`02582ca0`) and behind origin/master.
- Task state: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening/.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-20260611-023739/TASK-RF-troubleshoot-hardening-20260611-023739.md` is marked `🟢 Done`, with post-reflect `pass` and completion date `2026-06-11`.
- Recorded validation in the task artifacts:
  - `uv run pytest tests/troubleshoot/ -q` passed: 18 collected, 18 passed.
  - `make verify-sync` passed: `All components in sync`.
  - markdownlint passed across the 9 new/modified `src/` skill markdown files.
  - post-reflect report status is `COMPLETE` with `VERDICT: PASS`.

## Merge/duplicate analysis

- The local branch commit hash differs from the merged PR #173-like commit on origin/master: local `b9378c72` vs merged `71f16e13` (`feat(troubleshoot): Pipeline Hardening Closure mode (H0-H5 + waiver latch) (#173)`).
- `git cherry -v origin/master HEAD` reports `+ b9378c72...`, so Git does not consider the stale local commit patch-equivalent to origin/master. This appears to be because the stale lane is based on old `8cefefde` while origin/master contains the squashed/merged PR and later commits.
- Path-limited comparison shows the actual troubleshoot-hardening deliverables are already represented on origin/master:
  - `git diff --name-status origin/master..HEAD -- /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening/src/superclaude/commands/troubleshoot.md /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening/src/superclaude/skills/sc-troubleshoot-protocol /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening/tests/troubleshoot ':!tests/troubleshoot/backtest'` produced no output.
  - `git diff --name-status 71f16e13..HEAD -- /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening/src/superclaude/commands/troubleshoot.md /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening/src/superclaude/skills/sc-troubleshoot-protocol /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening/tests/troubleshoot ':!tests/troubleshoot/backtest'` produced no output.
  - The hardening task/meta artifact directories also produced no path-limited diff versus `71f16e13`.
- The stale branch is missing later origin/master work, notably `tests/troubleshoot/backtest/**` from the subsequent backtest harness. A path-limited diff against origin/master shows 27 deleted `tests/troubleshoot/backtest/**` files from the stale branch perspective.
- No tracked file exists only in the stale branch tree relative to origin/master: `comm -23 <(git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening ls-tree -r --name-only HEAD | sort) <(git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening ls-tree -r --name-only origin/master | sort) | wc -l` returned `0`.
- The branch is duplicated in another registered worktree: `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12` is also on `feat/troubleshoot-pipeline-hardening` at the same HEAD `b9378c72e2d5acc12607316b10ef377110f7c5a3`.
- Duplicate worktree caveat: `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12` has one untracked file: `.dev/pr-monitor/pr-173-augment-remediation-2026-06-12/monitor-run-173.jsonl`. Preserve or explicitly discard that file before removing the duplicate worktree.
- The target worktree and duplicate worktree have separate git metadata dirs: `/config/workspace/IronClaude/.git/worktrees/troubleshoot-hardening` and `/config/workspace/IronClaude/.git/worktrees/wf_3cd03e8d-30a-12`.

## Safe cleanup prerequisites

1. Do not remove anything yet. This handoff is verification-only.
2. Fetch origin first so the gone/up-to-date conclusion is fresh.
3. Reconfirm the target lane has no tracked, staged, or untracked changes.
4. Reconfirm the duplicate `wf_3cd03e8d-30a-12` lane is not an active session and preserve its untracked PR-monitor JSONL if it is needed.
5. Reconfirm the branch still has zero tracked files that exist only on the stale branch relative to origin/master.
6. Reconfirm path-limited diffs for the troubleshoot-hardening deliverables are empty against origin/master, excluding `tests/troubleshoot/backtest/**` because that is newer origin/master work missing from the stale lane rather than unique stale-lane work.
7. Reconfirm the Done task artifacts and recorded validation are sufficient for historical audit; if preserving artifacts elsewhere is desired, copy before worktree removal.
8. Because the same branch is registered in two worktrees, cleanup should remove or retire the duplicate worktree registrations before deleting the branch. Branch deletion will be blocked while any worktree still has it checked out.

## Validation commands

- `git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening fetch origin --prune`
- `git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening status --short --branch`
- `git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening branch -vv | grep 'feat/troubleshoot-pipeline-hardening'`
- `git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening rev-parse HEAD origin/master`
- `git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening log --oneline --decorate --grep='Pipeline Hardening Closure' --all --max-count=10`
- `git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening cherry -v origin/master HEAD`
- `git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening diff --name-status origin/master..HEAD -- src/superclaude/commands/troubleshoot.md src/superclaude/skills/sc-troubleshoot-protocol tests/troubleshoot ':!tests/troubleshoot/backtest'`
- `comm -23 <(git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening ls-tree -r --name-only HEAD | sort) <(git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening ls-tree -r --name-only origin/master | sort) | wc -l`
- `git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening ls-files --others --exclude-standard`
- `git -C /config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12 status --short --branch`
- `git -C /config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12 ls-files --others --exclude-standard`
- `git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening worktree list --porcelain`
- `uv run pytest /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening/tests/troubleshoot/ -q`

## Risks

- Git reports the stale commit as unmerged (`git cherry` shows `+`) even though the path-limited hardening deliverables are already present on origin/master. Do not use cherry output alone as the cleanup decision.
- The stale branch is behind origin/master and lacks later work, including the `tests/troubleshoot/backtest/**` harness. Do not rebase or push this branch unless deliberately reviving it; doing so would mix stale branch state with later master changes.
- The duplicate `.claude/worktrees/wf_3cd03e8d-30a-12` worktree has an untracked PR-monitor artifact. Removing it without preserving or confirming irrelevance would lose that untracked JSONL.
- `.claude/` content is generated/sync-dev output and must not be staged. Any preservation should target `.dev/` or another explicit archive path, not tracked `.claude/` mirrors.
- The target worktree is clean, but the same branch being checked out in two registered worktrees means branch cleanup is a two-worktree operation.

## New-session prompt

Continue crash-recovery cleanup verification for the stale troubleshoot-hardening lane. Inspect `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening` on branch `feat/troubleshoot-pipeline-hardening` at `b9378c72e2d5acc12607316b10ef377110f7c5a3`, and its duplicate `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12` at the same HEAD. Do not remove anything until verification is complete. First run `git -C /config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening fetch origin --prune`, then verify target status, duplicate status, gone upstream, zero target untracked files, duplicate untracked PR-monitor artifact, zero files unique to stale HEAD relative to origin/master, and empty path-limited diffs for `src/superclaude/commands/troubleshoot.md`, `src/superclaude/skills/sc-troubleshoot-protocol`, and `tests/troubleshoot` excluding `tests/troubleshoot/backtest`. Treat local `b9378c72` as stale/duplicate of merged PR #173-like commit `71f16e13` only after those checks pass; preserve or explicitly discard `/config/workspace/IronClaude/.claude/worktrees/wf_3cd03e8d-30a-12/.dev/pr-monitor/pr-173-augment-remediation-2026-06-12/monitor-run-173.jsonl` before any duplicate worktree removal.
