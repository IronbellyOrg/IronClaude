---
title: "Phase 11 — Final QA Input Manifest"
date: "2026-05-18"
phase: 11
---

# Final QA Input Manifest

## 8 Branches (all off master `ff99449`)

| PR | Branch | HEAD | Commits ahead |
|----|--------|------|---------------|
| cleanup | `chore/repo-cleanup-pre-pr-split` | `fe11bd8` | 1 |
| PR-A | `feat/sprint-runner-pr1-c1c4` | `57006bf` | 1 |
| PR-B | `test/audit-suite-pr2-nfr-invariants` | `82b7ce0` | 2 |
| PR-C | `docs/task-builder-merge-pr3-evidence-d0054-d0067` | `e4d8497` | 1 |
| PR-D | `docs/task-builder-merge-pr4-evidence-d0068-d0100` | `f577a0e` | 1 |
| PR-E | `chore/task-builder-merge-pr5-log-refresh` | `a72b030` | 1 |
| PR-F | `docs/hook-sync-pr6-release-and-aux` | `b63cbd7` | 3 |
| PR-G | `chore/task-archive-pr7-snapshot` | `ff99449` | **0 (SKIPPED — no content)** |

## 7 PR Body Files (one per non-skipped PR)

- `phase-outputs/prs/PR-cleanup-repo-pre-split.md`
- `phase-outputs/prs/PR-A-sprint-runner-c1c4.md`
- `phase-outputs/prs/PR-B-audit-suite-nfr-invariants.md`
- `phase-outputs/prs/PR-C-task-builder-merge-evidence-d0054-d0067.md`
- `phase-outputs/prs/PR-D-task-builder-merge-evidence-d0068-d0100.md`
- `phase-outputs/prs/PR-E-task-builder-merge-log-refresh.md`
- `phase-outputs/prs/PR-F-hook-sync-release-and-aux.md`

## 9 Verdict Files (triplet + Phase 2 + skip note)

- `phase-outputs/plans/phase-2-verdict.md`
- `phase-outputs/plans/chore-cleanup-triplet-verdict.md`
- `phase-outputs/plans/pr-a-triplet-verdict.md`
- `phase-outputs/plans/pr-b-triplet-verdict.md`
- `phase-outputs/plans/pr-d-triplet-verdict.md` (no `pr-c-triplet-verdict.md` because PR-C's triplet is summarized inline in body file)
- `phase-outputs/plans/pr-e-triplet-verdict.md`
- `phase-outputs/plans/pr-f-triplet-verdict.md`
- `phase-outputs/plans/pr-g-triplet-verdict.md` (skip reason)

## Cross-Phase QA Reports

- `qa/qa-phase-2-report.md` — PASS 19/19
- `qa/qa-phase-3-report.md` — PASS 20/20 (1 in-place fix)
- `reviews/artifact-rereview-pre-phase-4.md` — PASS 5/5 + cross-consistency (1 in-place fix for "80+" overcount → "40")

## Stash Safety (CRITICAL — must remain through merge)

- `stash@{0}: On feat/hook-sync-and-matcher-fix: task-RF-20260518-181333 pre-cleanup stash`
- Tag: `stash-backup-task-rf-20260518` → same commit
- Branch: `backup/task-rf-pre-cleanup-stash` → same commit
- Patch dump: `phase-outputs/baseline/full-stash-patch.txt` (18.7 MB)
- /tmp duplicates: `/tmp/task-rf-stash-full.patch` + `/tmp/task-rf-backup/`

## Deletions Performed

- Local branch `fix/auggie-flag-clear-mcp-prefix` deleted (unique commit `adb7d36` cherry-picked into PR-F)

## Branches Preserved with Unique Commits (user to triage)

- `feat/mig-002-execution-context-header` (7 unique commits — likely already represented on master via PR #49)
- `chore/task-cleanup-20260517` (1 commit, likely equivalent to master `c18879c (#48)`)
- `chore/task-merge-consolidate-roadmap-to-release` (1 commit, likely equivalent to master `516bb46 (#46)`)

## Known Acceptable Failures

- **PR-B audit tests 30 failures + 5 errors**: dependent on PR-F content; cleared when PR-F merges to master
- **Most branches verify-sync drift on `reject-workspace-writes.sh`**: cleared by PR-F (commit `b63cbd7`)
- **49 pre-existing ruff errors on master baseline**: out of scope for this PR split
- **`make test` re-pollution**: re-creates `docs/mistakes/test_*.md` and `solutions_learned.jsonl` entries; cleared by the 3 follow-up source-code tasks (Phase 12 items)
