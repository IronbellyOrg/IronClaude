---
title: "PR URLs — TASK-RF-20260518-181333"
created: "2026-05-18"
account: "ironbelly @ github.com"
repo: "IronbellyOrg/IronClaude"
---

# 7 PRs Opened

**Review order (recommended):** PR-F first (load-bearing green), then cleanup, then PR-A in parallel, then PR-C → PR-D → PR-E, then convert PR-B from draft after PR-F merges.

| # | Stage | PR | Status | URL |
|---|-------|----|----|-----|
| 51 | 1 | **PR-F** — hook-sync release + NFR-CONV-2 + matcher tests + freshness reg | **Ready** (triplet all-green) | https://github.com/IronbellyOrg/IronClaude/pull/51 |
| 52 | 0 | Cleanup — defensive .gitignore guards | Ready (optional, can fold into PR-F if preferred) | https://github.com/IronbellyOrg/IronClaude/pull/52 |
| 53 | 2a | **PR-A** — Sprint runner C1-C4 fixes | Ready (-6 sprint test failures vs master) | https://github.com/IronbellyOrg/IronClaude/pull/53 |
| 54 | 2b | **PR-B** — Audit suite + task-builder-merge test fixes | **DRAFT** (waits for PR-F to merge → tests go green) | https://github.com/IronbellyOrg/IronClaude/pull/54 |
| 55 | 2c | **PR-C** — task-builder-merge evidence batch 1 (D-0053..D-0063) | Ready | https://github.com/IronbellyOrg/IronClaude/pull/55 |
| 56 | 2d | **PR-D** — task-builder-merge evidence batch 2 (D-0068..D-0100) | Ready | https://github.com/IronbellyOrg/IronClaude/pull/56 |
| 57 | 3 | **PR-E** — execution log + phase-4 output refresh | Ready (3 files) | https://github.com/IronbellyOrg/IronClaude/pull/57 |

## Notes

- **"Warning: 3 uncommitted changes"** appeared on each `gh pr create` — refers to the untracked `.dev/releases/current/cliEval/`, untracked task tracker dir, and the working-tree state of the parallel cliEval session. These untracked files are NOT part of any PR.
- **PR-G (task-archive) was SKIPPED** — branch `chore/task-archive-pr7-snapshot` has 0 unique commits (all 667 `.dev/tasks/done/` files in the stash were already on master).
- **After PR-F merges**: convert PR-B from draft to ready (`gh pr ready 54`); PR-B's audit tests will go from FAIL → PASS in CI automatically.
- **After all 7 PRs merge**: see `paste-ready-gh-pr-commands.md` POST-MERGE section for stash cleanup + stale-branch cleanup (still ⚠️ gated on cliEval session resumption).

## Stash Status (Unchanged)

`stash@{0}` + tag `stash-backup-task-rf-20260518` + branch `backup/task-rf-pre-cleanup-stash` + 18.7 MB patch file all intact. Do NOT drop until the paused `/sc:tasklist` cliEval session has been resumed and recovered.
