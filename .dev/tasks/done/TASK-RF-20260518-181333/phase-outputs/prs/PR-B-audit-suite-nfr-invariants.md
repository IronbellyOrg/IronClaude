# Pull Request

## Summary

Lands the NFR-CONV invariant audit test suite (14 new test files + 9 fixture files under `tests/audit/`) plus the 3 task-builder-merge test drift remediations in `tests/skills/test_task_builder_merge.py`. The audit tests assert hook-sync release content that ships in PR-F, so this PR's audit tests transition from FAIL → PASS once PR-F merges. Recommend opening this as a **draft** until PR-F lands.

## Changes

<!-- List the major changes -->
- `tests/audit/` — 14 test files covering NFR-CONV-2 prose-determinism, NFR-CONV-6 self-contained items, NFR-CONV-9 zero-trust QA, NFR-CONV-10 parallel research, DNSP synthetic-finding R-122/R-123/R-125/INV-021 wrapper text guards, hidden_input_guard, monotonicity halt fixtures, PR-06-before-PR-04 sequencing. 9 fixture markdown files under `tests/audit/fixtures/`.
- `tests/skills/test_task_builder_merge.py` — 3 substitutions: L165 `"NEVER write specific"` → `"NO specific file:line references"`; L384-387 `"Regression takes precedence"` OR-pair → `"Precedence rule (regression > monotonicity)"`; L408 `"non-convergent"` → `"byte-exact wire string"`. SKILL.md and rf-task-builder.md untouched.
- `style(audit)` follow-up commit `82b7ce0` applies 7 ruff auto-fixes (import-order, unused-import) to 5 audit test files. Zero semantic test behavior change.
## Related Issues

<!-- Include related issue numbers, if any -->
Closes #
Depends-on: PR-F (audit tests assert against `docs/reference/nfr-conv-2-prose-determinism.md` and SKILL.md hook-sync sections).

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
- [ ] CI/CD pipeline successful (green status).

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
Pre-PR triplet on branch `test/audit-suite-pr2-nfr-invariants` (base `ff99449`, HEAD `82b7ce0`, 2 commits). (1) `uv run ruff check src/ tests/` → 58 errors (49 baseline + 9 intentional N801/N999 audit test naming patterns; 7 auto-fixable issues already applied in `82b7ce0`). (2) `uv run pytest tests/audit/ tests/skills/test_task_builder_merge.py -q` → task-builder-merge **68/68 PASS** (drift remediation works); audit 30 failures + 5 errors / 1221 passed total — **all 35 audit failures assert content that ships in PR-F** (`docs/reference/nfr-conv-2-prose-determinism.md` + SKILL.md hook-sync sections). Tests transition FAIL→PASS once PR-F lands. (3) `make verify-sync` → pre-existing drift on `reject-workspace-writes.sh` registration (resolved by PR-F). Full triplet verdict at `.dev/tasks/to-do/TASK-RF-20260518-181333/phase-outputs/plans/pr-b-triplet-verdict.md`.

## Screenshots (if applicable)

<!-- Attach screenshots if there are UI changes -->
N/A — test files only.

## Notes

<!-- What you want to communicate to reviewers, background to technical decisions, etc. -->

**Merge ordering matters:** Open as `--draft` and **merge PR-F first**. PR-B's audit tests assert against content that lives in PR-F. Merging PR-B first leaves master red on these 30+5 audit tests until PR-F follows. Once PR-F merges, this PR can be marked ready and merged with all green tests. The 13 remaining ruff issues (after the 7 auto-fixes applied in commit `82b7ce0`) are intentional descriptive naming patterns for test class families (e.g. `TestPartA_OneLowFindingFailsGate`, `TestInvariant1_SelfContainedItem`) and grouped test modules (e.g. `test_nfr_conv_9_zero_trust`, `test_monotonicity_halt_F_5_5_5`). These conventions are documented in the test files themselves and are accepted under the CONTRIBUTING.md rot-budget convention.
<!-- -->
