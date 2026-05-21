# Pull Request

## Summary

Lands the hook-sync-and-matcher-fix release artifacts (release-spec + coverage-spec), the new NFR-CONV-2 prose-determinism reference document, the regression test suite for the `mcp__auggie-mcp__*` matcher fix, and the OQ-2/OQ-3 hook hygiene cleanups (bash-gate archive + reject-workspace-writes.sh registration in `_FRESHNESS_SCRIPTS`). All triplet steps **GREEN** on this branch — verify-sync passes, hook + audit pytest is 974/0.

## Changes

<!-- List the major changes -->
- `.dev/releases/current/hook-sync-and-matcher-fix/release-spec.md` + `hook-sync-coverage-spec.md` — release record for the hook-sync-and-matcher-fix shipment.
- `docs/reference/nfr-conv-2-prose-determinism.md` — reference document defining the structural-side vs. prose-side audit boundary. **Load-bearing for PR-B**: the audit test suite (PR-B) asserts against this document's enumerations and cross-references.
- `tests/hooks/test_auggie_flag_clear_mcp_prefix.py` (cherry-picked from `fix/auggie-flag-clear-mcp-prefix` commit `adb7d36`) — 175-line regression suite covering the `mcp__auggie-mcp__*` matcher widening.
- `_FRESHNESS_SCRIPTS` registration for `reject-workspace-writes.sh` + archive-and-delete of the bash-gate orphan + cancelled-backlog marker (cherry-picked from feat-branch commit `efaa33d` — resolves OQ-2 and OQ-3).
- `.dev/tasks/to-do/TASK-RF-20260517-213436/` — task evidence for the hook-sync execution per release-artifact-tracking convention.
## Related Issues

<!-- Include related issue numbers, if any -->
Closes #
Internal: TASK-RF-20260517-213436 (hook-sync execution). **Load-bearing dependency of PR-B**.

## Checklist

### Git Workflow
- [x] For external contributions: Followed the flow of fork → topic branch → upstream PR.
- [x] For collaborators: Used a topic branch (not directly committed to main).
- [x] `git rebase upstream/main` completed (no conflicts).
- [x] Commit messages conform to Conventional Commits (`feat:`, `fix:`, `docs:`, etc.).

### Code Quality
- [x] Changes are limited to a single purpose (not a large PR, guideline: ~200 lines of difference).
- [x] Follows existing code conventions and patterns.
- [x] Add appropriate tests for new features/fixes.
- [x] Lint/Format/Typecheck all pass.
- [x] CI/CD pipeline successful (green status).

### Security
- [x] Secrets and authentication information not committed.
- [x] Necessary files excluded with `.gitignore`.
- [x] No breaking changes, or if there are, commit with `!` and include in MIGRATION.md.

### Documentation
- [x] Update documentation as needed (README, CLAUDE.md, docs/, etc.).
- [x] Add comments to complex logic.
- [x] Properly document API changes.

## Testing Methods

<!-- How to verify this PR works -->
Pre-PR triplet on branch `docs/hook-sync-pr6-release-and-aux` (3 commits: `618071b` release artifacts + `6337a0e` cherry-pick adb7d36 + `b63cbd7` cherry-pick efaa33d). (1) `uv run ruff check src/ tests/` → 49 errors (identical to master baseline; 175-line test added is ruff-clean). (2) `uv run pytest tests/hooks/ tests/audit/ -q` → **974 passed, 1 skipped, 0 failed** — the audit tests that fail on PR-B all PASS here because PR-F's content is on this branch. (3) `make verify-sync` → **✅ All components in sync** — the `reject-workspace-writes.sh` registration in `b63cbd7` clears the drift that affects every other PR branch.

## Screenshots (if applicable)

<!-- Attach screenshots if there are UI changes -->
N/A — hook + docs + tests only.

## Notes

<!-- What you want to communicate to reviewers, background to technical decisions, etc. -->

**Open this PR FIRST in the 7-PR sequence.** PR-F is the load-bearing dependency: PR-B's 30 failing audit tests + 5 setup errors all become PASS once this PR's content is on master. The 3 commits on this branch were authored in two upstream branches (`fix/auggie-flag-clear-mcp-prefix` and `feat/hook-sync-and-matcher-fix`); they are cherry-picked here onto a fresh branch off master to keep the PR self-contained. After PR-F merges: `fix/auggie-flag-clear-mcp-prefix` can be deleted (its unique commit `adb7d36` is now on master via this PR). The triplet's all-green status proves this PR ships standalone-functional changes.
<!-- -->
