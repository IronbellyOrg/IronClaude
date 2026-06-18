# Closed PR Lane Cleanup Manifest

Scope: closed/merged PR worktrees for mms/fr028/tfep/SprintRun429. No worktrees removed; no source files touched; no staging/commits; no stash operations. Artifact preservation copies were written only under this directory.

## Summary Table

| Worktree | PR | Merged? | Branch / HEAD observed | Clean? | Artifact residue? | Archived copy count | Safe to remove? | Blocker |
|---|---:|---|---|---|---|---:|---|---|
| `/config/workspace/IronClaude/.dev/worktrees/SprintRun429` | #183 | Yes (`state=MERGED`, `mergedAt=2026-06-18T14:13:09Z`) | `SprintRun429` / `d33a52ea95a3aa58a0c160d7da46a9f6c8dceeb1` | Source clean; tracked artifact dirty: 3 `.dev/...` files; untracked artifact files: 103 | Yes: `.dev/brainstorms/sprint-429-recovery-spec.md`; `.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/`; tracked dirty eval/perf artifacts | 106 | No, not yet | Worktree HEAD differs from PR #183 head (`87a066241a36359817de5b5e518a9a989f4f266b`) and is not an ancestor of current `origin/master`; decide whether stale local branch commit plus tracked artifact drift can be discarded. Unique untracked task/spec artifacts have been copied here. |
| `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9` | #178 | Yes (`state=MERGED`, `mergedAt=2026-06-17T16:51:30Z`) | `feat/sc-bare-review-m8m9-migration` / `adafd61dc0ad96fb34359227daca629c22f5e44a` | Source clean; tracked artifact dirty: 3 `.dev/...` files; untracked artifact files: 16 | Yes: post-FR028 reflect, M8/M9 task reflect, troubleshoot report, MultiModelSwarm release tasklist | 19 | Yes, after accepting discard of artifact-only tracked drift | No source blocker found. Artifact-only residue was copied here; remaining tracked dirt is eval/perf artifact drift only. |
| `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend` | #180 | Yes (`state=MERGED`, `mergedAt=2026-06-17T16:54:31Z`) | `feat/tfep-troubleshoot-backend` / `c8363739ce8f634ab3c65862a96428dd6b0d6d66` | Source clean; no tracked dirty files; untracked artifact files: 6 | Yes: `.dev/reviews/pr-180-20260617-1250/` | 7 | Yes | No blocker found after review bundle copy. |
| `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028` | #179 | Yes (`state=MERGED`, `mergedAt=2026-06-17T16:54:10Z`) | `fix/swarm-normalize-perworker-status-fr028` / `d2ad3cbd556f93f2ff9aeef208b9c6d6a9f496d6` | Source clean; no tracked dirty files; no untracked files | No unique residue found | 0 | Yes | No blocker found. |

## Preserved Artifact Copies

- `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/closed-pr-lanes/SprintRun429/` — 106 files copied:
  - `sprint-429-recovery-spec.md`
  - `TASK-RF-429-recovery-20260615-040144/` including research, QA, phase output, test-result, and reflect artifacts.
- `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/closed-pr-lanes/mms-m8m9/` — 19 files copied:
  - `post-fr028-20260617_0400/`
  - `TASK-RF-bare-review-migration-20260616-045915/reflect/post/93f613de3ec6/`
  - `troubleshoot/bug-reviewers-models-clobber-20260617055915/REPORT.md`
  - `releases/complete/MultiModelSwarm/`
- `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/closed-pr-lanes/tfep-troubleshoot-backend/` — 7 files copied:
  - `pr-180-20260617-1250/` review bundle.
- `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/closed-pr-lanes/fr028-fr028/` — 0 files copied; no residue found.

## Notes

- All four PRs are merged in `IronbellyOrg/IronClaude`.
- Stash list was inspected only; no stash was applied, dropped, or cleared.
- Remote branches for the worktrees appear gone in `git status --short --branch`.
- `SprintRun429` is the only lane kept conservative because the local worktree HEAD does not match the merged PR head and is not an ancestor of current `origin/master`, even though tracked source files are clean.
