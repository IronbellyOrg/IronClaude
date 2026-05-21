---
title: "Paste-Ready `gh pr create` Commands — TASK-RF-20260518-181333"
date: "2026-05-18"
---

# Paste-Ready PR Creation Commands

**Recommended merge order:** PR-F → cleanup → PR-A → PR-B → PR-C → PR-D → PR-E.

PR-F is the load-bearing GREEN PR (provides PR-B's audit-test targets + clears verify-sync drift). Merging PR-F first lets every other PR's CI go green on merge.

## STAGE 0 — Optional: Open Cleanup PR (or fold into PR-F)

```bash
gh pr create \
  --title "chore(tests): add defensive .gitignore guards for repo-pollution sources" \
  --body-file .dev/tasks/to-do/TASK-RF-20260518-181333/phase-outputs/prs/PR-cleanup-repo-pre-split.md \
  --base master \
  --head chore/repo-cleanup-pre-pr-split
```

## STAGE 1 — Open PR-F FIRST (load-bearing, triplet ALL-GREEN)

```bash
gh pr create \
  --title "docs(hook-sync): release artifacts + NFR-CONV-2 reference + matcher regression tests + freshness registration" \
  --body-file .dev/tasks/to-do/TASK-RF-20260518-181333/phase-outputs/prs/PR-F-hook-sync-release-and-aux.md \
  --base master \
  --head docs/hook-sync-pr6-release-and-aux
```

## STAGE 2 — Open in parallel after PR-F merges

```bash
# PR-A: Sprint runner C1-C4 fixes (-6 sprint failures vs master baseline)
gh pr create \
  --title "feat(sprint): C1-C4 deterministic runner fixes" \
  --body-file .dev/tasks/to-do/TASK-RF-20260518-181333/phase-outputs/prs/PR-A-sprint-runner-c1c4.md \
  --base master \
  --head feat/sprint-runner-pr1-c1c4

# PR-B: Audit suite + task-builder test fixes (open as DRAFT until PR-F merges)
gh pr create \
  --title "test(audit): NFR-CONV invariant suite + task-builder-merge test fixes" \
  --body-file .dev/tasks/to-do/TASK-RF-20260518-181333/phase-outputs/prs/PR-B-audit-suite-nfr-invariants.md \
  --base master \
  --head test/audit-suite-pr2-nfr-invariants \
  --draft

# PR-C: task-builder-merge evidence batch 1 (D-0053..D-0063)
gh pr create \
  --title "docs(task-builder): task-builder-merge evidence batch 1 (D-0053..D-0063) + phase-5 output" \
  --body-file .dev/tasks/to-do/TASK-RF-20260518-181333/phase-outputs/prs/PR-C-task-builder-merge-evidence-d0054-d0067.md \
  --base master \
  --head docs/task-builder-merge-pr3-evidence-d0054-d0067

# PR-D: task-builder-merge evidence batch 2 (D-0068..D-0100)
gh pr create \
  --title "docs(task-builder): task-builder-merge evidence batch 2 (D-0068..D-0100) + phase-6/7 outputs" \
  --body-file .dev/tasks/to-do/TASK-RF-20260518-181333/phase-outputs/prs/PR-D-task-builder-merge-evidence-d0068-d0100.md \
  --base master \
  --head docs/task-builder-merge-pr4-evidence-d0068-d0100
```

## STAGE 3 — After PR-C + PR-D merge

```bash
# PR-E: log refresh (small — 3 files)
gh pr create \
  --title "chore(releases): refresh task-builder-merge execution log + phase-4 output" \
  --body-file .dev/tasks/to-do/TASK-RF-20260518-181333/phase-outputs/prs/PR-E-task-builder-merge-log-refresh.md \
  --base master \
  --head chore/task-builder-merge-pr5-log-refresh
```

## SKIPPED — PR-G

`chore/task-archive-pr7-snapshot` branch holds zero unique commits — all 667 `.dev/tasks/done/` files in the stash were already on master. Delete or repurpose:

```bash
# Either delete the empty branch:
git branch -d chore/task-archive-pr7-snapshot
# Or keep it as a placeholder for the next archive batch.
```

## POST-MERGE — Stash + Branch Cleanup

⚠️ **CRITICAL ORDERING — IRREVERSIBLE OPERATIONS BELOW** ⚠️

DO NOT run any stash-drop / tag-delete / backup-branch-delete commands until ALL of these are true:
1. All 7 PRs from STAGE 0-3 above are MERGED to master.
2. The paused `/sc:tasklist` cliEval session in the parallel chat has been RESUMED.
3. That session has applied the stash to its working tree (via `git stash apply 'stash@{0}'` or by recovering specific paths from the stash) and confirmed its 53 cliEval files plus any newer files are intact.
4. You have personally verified the cliEval session's work is checkpointed (committed to a branch or saved elsewhere). The 5 post-stash cliEval files (phase-5-tasklist.md, phase-6-tasklist.md, 3 .log files) are NOT in the stash — they live in working trees of the PR branches.

Only after all four conditions are confirmed:

```bash
# Drop the redundant stash refs (IRREVERSIBLE — verify §1-4 above first):
git tag -d stash-backup-task-rf-20260518
git branch -D backup/task-rf-pre-cleanup-stash
git stash drop 'stash@{0}'   # the 'task-RF-20260518-181333 pre-cleanup stash'

# Remove the 18.7 MB patch dump from .dev/ (also remove the /tmp duplicates):
rm .dev/tasks/to-do/TASK-RF-20260518-181333/phase-outputs/baseline/full-stash-patch.txt
rm /tmp/task-rf-stash-full.patch
rm -rf /tmp/task-rf-backup

# Push origin --delete on the cherry-picked branch:
git push origin --delete fix/auggie-flag-clear-mcp-prefix

# After verifying content equivalence:
# (verify each branch's unique commits are duplicated in merged master commits)
git branch -D chore/task-cleanup-20260517  # if equivalent to master c18879c (#48)
git branch -D chore/task-merge-consolidate-roadmap-to-release  # if equivalent to master 516bb46 (#46)
git branch -D feat/mig-002-execution-context-header  # if MIG-002..MIG-004 reach master via PR-D
```
