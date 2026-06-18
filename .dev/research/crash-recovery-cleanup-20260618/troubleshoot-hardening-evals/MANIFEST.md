# troubleshoot-hardening-evals cleanup manifest

Archive created: 2026-06-18

## Source lane

- Worktree: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals`
- Branch: `feat/troubleshoot-hardening-evals`
- HEAD: `f210cf16d2f2c09c42d1a399a364686ba7779e6f` (`f210cf16`)
- Initial tracked status before archive: clean; untracked roots remained in source worktree
- Final tracked status after archive verification: 29 tracked deletions reported under `.dev/releases/current/MultiModelSwarm/`; these were not modified or repaired by this cleanup agent because source edits were forbidden
- Remote tracking: `origin/feat/troubleshoot-hardening-evals` is gone

## PR state

- PR: `https://github.com/IronbellyOrg/IronClaude/pull/168`
- State: `MERGED`
- Base: `master`
- Head: `feat/troubleshoot-hardening-evals`
- Head owner: `IronbellyOrg`
- Draft: `false`
- Merged at: `2026-06-12T21:51:11Z`
- Merge commit: `0f6862b3770b3df37993e16aed78ecd02f39c8ae`

## Archived artifact roots

Copied into this archive preserving worktree-relative structure under `.dev/`.

| Source path | Archive path | Files | Dirs | Bytes | Verified |
|---|---|---:|---:|---:|---|
| `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/eval-workspaces/cli-eval/` | `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/troubleshoot-hardening-evals/.dev/eval-workspaces/cli-eval/` | 74 | 41 | 449642 | source/dest counts match |
| `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/reflect/post-cli-eval-20260612/` | `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/troubleshoot-hardening-evals/.dev/reflect/post-cli-eval-20260612/` | 3 | 3 | 15921 | source/dest counts match |
| `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/troubleshoot-meta/` | `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/troubleshoot-hardening-evals/.dev/troubleshoot-meta/` | 89 | 10 | 1061786 | source/dest counts match |

Totals for archived untracked roots: 166 files, 54 directories, 1527349 bytes.

Note: the handoff reported 165 untracked files. Fresh count at archive time found 166 files across the three named roots; source and archive counts match exactly.

## Context copied

- Handoff copied to: `/config/workspace/IronClaude/.dev/research/crash-recovery-cleanup-20260618/troubleshoot-hardening-evals/HANDOFF.md`

## Stash warning

A lane-specific stash exists and was not touched:

- `stash@{0}: On feat/troubleshoot-hardening-evals: pre-merge-local-changes-before-pr162-master-ff-2026-06-12`

Do not apply, drop, or clear this stash during cleanup unless a human explicitly requests it. Other repository stashes also exist; none were modified.

## Removal assessment

- `safe_to_remove`: false at final verification time.
- Artifact archive status: complete; all three requested untracked artifact roots were copied and verified.
- Blockers: final source worktree status reported 29 tracked deletions under `.dev/releases/current/MultiModelSwarm/`; source edits/restoration were outside this cleanup agent's authorization. Main agent should resolve or explicitly decide to discard those tracked deletions before removing the worktree.
- Caution: if a human still wants to recover the lane-specific stash contents, inspect it read-only before any separate stash decision. Worktree removal must not be combined with stash apply/drop/clear.
