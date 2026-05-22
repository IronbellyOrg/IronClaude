---
title: "Phase 10 — Stale-Branch Cleanup Report"
date: "2026-05-18"
phase: 10
---

# Phase 10 — Stale-Branch Cleanup Report

## Summary

| Branch | Disposition | Action Taken | Follow-Up |
|--------|-------------|--------------|-----------|
| `fix/auggie-flag-clear-mcp-prefix` | unique commit `adb7d36` cherry-picked into PR-F | **DELETED** (local) | User can run `git push origin --delete fix/auggie-flag-clear-mcp-prefix` after PR-F merges |
| `feat/mig-002-execution-context-header` | 7 unique MIG-002/003/004 commits | **SKIPPED** — preserved for user review | User should compare commit content against master HEAD; the MIG-* landings may be represented on master via PR #49 with different SHAs |
| `chore/task-cleanup-20260517` | 1 unique commit `c9c35c3 chore(tasks): triage and archive 22 completed task tracks to done/` | **SKIPPED** — likely equivalent to master's `c18879c (#48)` (same title) | User should verify content equivalence with `git diff` then delete if equivalent |
| `chore/task-merge-consolidate-roadmap-to-release` | 1 unique commit `c1c1447 chore(task-merge): consolidate docs/docs-product/tech/task-merge →` | **SKIPPED** — likely equivalent to master's `516bb46 (#46)` (same title) | User should verify content equivalence with `git diff` then delete if equivalent |

## Overall

- **1 branch deleted locally** (`fix/auggie-flag-clear-mcp-prefix` — its unique commit is now in PR-F).
- **3 branches preserved** — each has unique commits that may or may not be equivalent to merged-PR versions on master. The cleanup script declines to destroy commits without user-verified content equivalence.

## Paste-Ready User Commands

After verifying content equivalence:

```bash
# After PR-F merges, delete the remote tracking branch for the cherry-picked branch:
git push origin --delete fix/auggie-flag-clear-mcp-prefix

# After verifying unique-commit content is duplicated in merged master commits, delete the equivalents:
# (verify each with: git diff master..chore/task-cleanup-20260517 -- '.dev/tasks/done/' )
git branch -D chore/task-cleanup-20260517  # if equivalent to c18879c
git push origin --delete chore/task-cleanup-20260517

git branch -D chore/task-merge-consolidate-roadmap-to-release  # if equivalent to 516bb46
git push origin --delete chore/task-merge-consolidate-roadmap-to-release

# For feat/mig-002-execution-context-header — verify each of the 7 unique commits is represented:
git log master..feat/mig-002-execution-context-header --oneline
# Compare to: git log master --grep="MIG-002\|MIG-003\|MIG-004" --oneline
# If all represented in master via PR #49: git branch -D feat/mig-002-execution-context-header
```

## Stash Status (Critical)

`stash@{0}` (and its 3 redundant refs: tag `stash-backup-task-rf-20260518`, branch `backup/task-rf-pre-cleanup-stash`, patch dump `phase-outputs/baseline/full-stash-patch.txt`) remains intact. **Do not drop the stash until the 7 PRs are merged AND the parallel cliEval session has resumed and recovered its working state.**
