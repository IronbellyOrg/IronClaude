# QA Report — Phase 3 Garbage Cleanup on Throwaway Branch

**Topic:** TASK-RF-20260518-181333 Phase 3 (Steps 3.1–3.14)
**Date:** 2026-05-18
**Phase:** phase-gate (post-Phase-3 verification)
**Fix cycle:** 1
**Fix authorization:** true

---

## Overall Verdict: PASS (after in-place re-cleanup)

The cleanup commit (`fe11bd8`) itself is structurally correct. The .gitignore deviation from the BUILD_REQUEST (anchoring patterns to repo root) is **justified** and **necessary** to preserve tracked files. The PR body, triplet verdict, and all phase-output artefacts are well-formed.

**One critical execution gap was found and fixed in-place:** the Step 3.13 test runs re-created the garbage paths AFTER the Step 3.12 commit. Acceptance criteria 3.4 and 3.5–3.10 were violated at the time QA opened. Re-cleanup has been performed; working tree now matches the intended post-Phase-3 state. Branch contents (the single `fe11bd8` commit on `.gitignore` only) were never affected.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | 3.1 — Stash created; stash@{0} still exists with expected message | PASS | `git stash list` shows `stash@{0}: On feat/hook-sync-and-matcher-fix: task-RF-20260518-181333 pre-cleanup stash`; baseline/stash-list-after-stash.txt confirms post-stash state. |
| 2 | 3.1 — Working tree clean post-stash | PASS | `baseline/post-stash-status.txt` contains only `?? .dev/tasks/to-do/TASK-RF-20260518-181333/` (the task workspace itself, intentionally untracked). |
| 3 | 3.2 — Cleanup branch off master HEAD | PASS | `branches/chore-repo-cleanup-pre-pr-split-base-sha.txt` = `ff99449...` (master HEAD); current HEAD `fe11bd8` is exactly 1 commit ahead of master. |
| 4 | 3.2 — Branch starts clean | PASS | `branches/chore-repo-cleanup-pre-pr-split-clean-status.txt` shows only the task workspace untracked file. |
| 5 | 3.3 — Cleanup targets present in stash | PASS | stash-files.txt has 978 entries; grep -cE on cleanup targets returns 7 (solutions_learned.jsonl + 3 docs/mistakes/*.md + prd-test-product + prd-dry-run-test + 0.20 family). |
| 6 | 3.4 — solutions_learned.jsonl reverted; diff vs HEAD empty | PASS (after fix) | At QA-open time: `git diff HEAD docs/memory/solutions_learned.jsonl` showed +8 simulated entries with `2026-05-18T20:47:59` timestamps (post-commit re-pollution by Step 3.13 pytest run). Reverted in-place via `git checkout HEAD --`; diff now 0 lines. delete-time evidence `solutions-learned-revert-diff.txt` is empty (correct at delete time). |
| 7 | 3.5–3.10 — 6 garbage paths no longer exist on disk | PASS (after fix) | At QA-open time: `0.20` gone ✓, but `prd-test-product/`, `prd-dry-run-test/`, and 3 `docs/mistakes/test_*.md` files re-created by Step 3.13 test run (verified by mtime `20:47:59` post-dating commit at `20:46:29`). Re-deleted in-place. All 6 now absent. delete-*.txt evidence files all report "deleted" (correct at delete time). |
| 8 | 3.11 — .gitignore entries added | PASS | `git show fe11bd8 -- .gitignore` shows +17 lines with 6 anchored patterns. |
| 9 | 3.11 — .gitignore deviation (anchoring) justified | PASS | `discovery/gitignore-check.txt` evidences that anchored `/prd-*-test/` / `/prd-dry-run-*/` / `/.sprint-exitcode` correctly classify `.dev/eval-workspaces/prd-test-product/execution-log.md`, `.dev/eval-workspaces/prd-dry-run-test/execution-log.md`, and `.dev/releases/complete/foo/.sprint-exitcode` as NOT IGNORED. `git ls-files \| grep -E '(prd-(test\|dry-run)\|\.sprint-exitcode\|^0\.[0-9])'` returns 2 tracked `.dev/eval-workspaces/prd-{test,dry-run}-*/execution-log.md` files plus **40** `.dev/releases/**/.sprint-exitcode` files — all confirmed safe under the anchored patterns. Unanchored patterns from the BUILD_REQUEST would have shadowed all of these. Deviation is necessary and well-evidenced. [CORRECTED 2026-05-18 by pre-Phase-4 re-review: prior version of this row claimed "80+" tracked `.sprint-exitcode` files; actual count per `git ls-files \| grep -c '\.sprint-exitcode$'` is 40. Defense remains valid because 40 > 0 tracked files would still have been shadowed by an unanchored pattern.] |
| 10 | 3.11 — No tracked files newly ignored | PASS | `git check-ignore` confirms none of the 40 matching tracked paths are ignored under the anchored patterns. |
| 11 | 3.12 — Commit uses Conventional Commits (`chore(tests):` scope) | PASS | `git show fe11bd8` subject: `chore(tests): add defensive .gitignore guards for repo-pollution sources`. |
| 12 | 3.12 — Co-Authored-By signoff present | PASS | `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>` present in commit body. |
| 13 | 3.12 — `git add -A` was NOT used; only .gitignore staged | PASS | `commits/chore-cleanup-staged.txt` shows ` M .gitignore` plus 2 untracked dirs that were correctly NOT staged. Commit stat: 1 file changed, 17 insertions(+), 0 deletions. |
| 14 | 3.12 — Only .gitignore in the commit | PASS | `git show fe11bd8 --stat`: only `.gitignore \| 17 +++++++++++++++++`. The 6 deleted paths correctly do NOT appear as deletions (they were never tracked on master). |
| 15 | 3.13 — Triplet verdict based on actual command outputs | PASS | `plans/chore-cleanup-triplet-verdict.md` references real exit codes (1, 1, 2) matching `chore-cleanup-{ruff,pytest,verify-sync}.txt` raw outputs. Failure counts cross-check: pytest = 63 failed + 1 error (matches raw); ruff = 49 errors; verify-sync = `MISSING from _FRESHNESS_SCRIPTS: reject-workspace-writes.sh`. No fabrication detected. |
| 16 | 3.13 — Zero NEW failures introduced by THIS branch | PASS | All 63 pytest failures are in `tests/sprint/...` (pre-existing C1-C4 regressions tracked for PR-A). Ruff: `.gitignore` is not Python — 49 errors all pre-existing. verify-sync: drift is `reject-workspace-writes.sh` registration gap fixed in feat-branch commit `efaa33d` (lands via PR-F). Cleanup commit touches only `.gitignore` → cannot cause any of these. Cross-verified by `git diff ff99449..HEAD --stat`: 1 file, .gitignore only. |
| 17 | 3.14 — PR body file populated from canonical 51-line template | PASS | Template at `.github/PULL_REQUEST_TEMPLATE.md` is 51 lines. PR body is 56 lines (51 template + 5 lines content additions: tail `<!-- -->`, expanded Changes/Summary/Testing-Methods bodies). All 15 checkboxes preserved across 4 sub-sections (Git Workflow: 4, Code Quality: 5, Security: 3, Documentation: 3). NOTE: acceptance criterion text said "14 checkbox items" — that count is itself wrong; the template has 15 and the PR body correctly preserves all 15. |
| 18 | 3.14 — First line is `# Pull Request` | PASS | `head -1` confirms `# Pull Request`. |
| 19 | 3.14 — Last line preserves `-->` | PASS | `tail -1` confirms `<!-- -->`. |
| 20 | Stash safety — stash@{0} still present | PASS | `git stash list \| head -3` shows the pre-cleanup stash intact. |

## Summary
- Checks passed: 20 / 20 (after in-place fixes)
- Checks failed at QA-open: 2 (3.4 + 3.5-3.10)
- Critical issues found: 1 (Step 3.13 test re-pollution)
- Issues fixed in-place: 1

## Confidence

- **Verified:** 20/20 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%
- **Tool engagement:** Read: 13 | Grep: 5 (within Bash) | Glob: 0 | Bash: 12

Tool engagement (Read + Grep + Glob within Bash + standalone) exceeds the 20-item checklist count; each check has at least one explicit tool call cited in the Evidence column.

## Issues Found

| # | Severity | Location | Issue | Required Fix | Status |
|---|----------|----------|-------|-------------|--------|
| 1 | CRITICAL | Working tree (post-Step-3.13) | `make test` in Step 3.13 re-created the 5 garbage paths (`prd-test-product/`, `prd-dry-run-test/`, 3 `docs/mistakes/test_*.md` files) and re-polluted `docs/memory/solutions_learned.jsonl` with 8 new simulated entries (timestamps `2026-05-18T20:47:59`, post-dating commit at `20:46:29`). Acceptance criteria 3.4 and 3.5–3.10 require clean working tree post-Phase-3. | Re-revert solutions_learned.jsonl; re-delete the 5 garbage paths. The .gitignore guards correctly prevent these from polluting `git status` (prd-*-test/ and prd-dry-run-*/ are now IGNORED), but the docs/mistakes/test_*.md files have no .gitignore guard and solutions_learned.jsonl is a tracked file the guards cannot protect. | FIXED |

## Actions Taken

- **Fix 1.1:** Reverted `docs/memory/solutions_learned.jsonl` to HEAD via `git checkout HEAD -- docs/memory/solutions_learned.jsonl`. Post-fix verification: `git diff HEAD docs/memory/solutions_learned.jsonl \| wc -l` returns 0.
- **Fix 1.2:** Deleted recreated `prd-test-product/` and `prd-dry-run-test/` directories via `rm -rf`.
- **Fix 1.3:** Deleted 3 recreated `docs/mistakes/test_*.md` files via `rm -f`.
- **Post-fix git status:** `?? .dev/releases/current/cliEval/` and `?? .dev/tasks/to-do/TASK-RF-20260518-181333/` only (both expected — listed as intentionally untracked in the prompt).

## Notes for Phase 4+ Planning

The Step 3.13 re-pollution event is informative for downstream PRs:
1. **Source bugs remain unfixed.** Pytest currently re-creates `docs/mistakes/test_*.md` and re-pollutes `solutions_learned.jsonl` on every `make test` run. The cleanup commit only adds .gitignore guards for 2 of the 3 recurring pollution sources (`prd-*` + `0.[0-9]*` + `.sprint-exitcode`). The `docs/mistakes/` pollution and `solutions_learned.jsonl` pollution have NO .gitignore protection because (a) `docs/mistakes/` may legitimately hold tracked mistake reports in the future, and (b) `solutions_learned.jsonl` is a tracked memory file that must remain writable.
2. **Implication:** Any reviewer or downstream agent who runs `make test` on this branch will re-trigger the pollution. The follow-up tasks named in the commit body — TASKLIST_ROOT manifest bug, reflexion writer cwd-isolation, PRD-skill output-routing — must land before the underlying issue is fully resolved. Until then, post-test re-cleanup is a manual step.
3. **PR-readiness unaffected.** The commit itself is correct and well-scoped. The triplet verdict's "zero new failures" claim is structurally valid (this branch only touches `.gitignore`).

## Recommendations

- **Green light for Phase 4.** Branch is in correct post-Phase-3 state with stash@{0} preserved and working tree clean (modulo expected untracked task workspace).
- Consider adding `docs/mistakes/test_*.md` to .gitignore in a follow-up if the reflexion-writer cwd-isolation fix proves non-trivial.
- The acceptance-criterion typo ("14 checkbox items" — actual is 15) should be corrected in any future BUILD_REQUEST template.

## QA Complete
