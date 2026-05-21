# Research Synthesis — TASK-RF-20260518-181333

- **Task:** Branch QA + commit + PR workflow for `feat/hook-sync-and-matcher-fix`
- **Date:** 2026-05-18
- **Status:** Complete
- **Inputs:** R1 (file-inventory), R2 (patterns), R3 (integration-points), R6 (test-verification), R7 (gap-fill)
- **Purpose:** Single consolidated reference for later phases — replaces re-reading the five source research files.

---

## 1. 9-Group → PR Mapping Table

Derived from R1 §5 (Commit Group Summary) cross-referenced with R7 §GAP 5 (multi-PR split table). Branch-name pattern follows R2 §2.4 precedent (`<type>/<area>-pr<N>-<slug>`).

| Group Name                  | Target PR Letter | File Count | Branch Name                                              |
|-----------------------------|------------------|------------|----------------------------------------------------------|
| c1-c4-sprint-runner         | PR-A             | ~10        | `feat/sprint-runner-pr1-c1c4`                            |
| audit-tests                 | PR-B             | ~33        | `test/audit-suite-pr2-nfr-invariants`                    |
| task-builder-merge-evidence (batch 1, D-0054-D-0067) | PR-C | ~50 | `docs/task-builder-merge-pr3-evidence-d0054-d0067`       |
| task-builder-merge-evidence (batch 2, D-0068-D-0100) | PR-D | ~60 | `docs/task-builder-merge-pr4-evidence-d0068-d0100`       |
| task-builder-merge-evidence (log refresh) | PR-E | ~3 | `docs/task-builder-merge-pr5-execution-log-refresh`      |
| hooks-and-matcher-fix (release evidence + nfr-conv-2 doc) | PR-F | ~5 | `docs/reference-pr6-nfr-conv-2-prose-determinism` |
| task-housekeeping (done/ snapshot, optional) | PR-G | ~7 | `chore/tasks-archive-pr7-done-snapshot`                  |
| docs-pollution (revert + delete) | — (local hygiene) | 1 mod + 3 del | (not a PR — gitignore + revert)                  |
| repo-root-garbage + clieval-design + gitignore-add | — (local hygiene / deferred) | 3 del + 5 deferred + 1 gitignore line | (not a PR — gitignore + delete; cliEval deferred to separate branch) |

**Notes:**
- Groups `docs-pollution`, `repo-root-garbage`, `clieval-design`, and `gitignore-add` (per R1 §5) are NOT PRs — they are local-hygiene / deferred work per R7 §GAP 5 final row.
- `clieval-design` (R1 §3.3 / §3.4) is explicitly out-of-scope for this branch — deferred to a separate follow-up branch.
- Authoritative artifacts/ subtree count per R7 §GAP 2 = 85 D-NNNN dirs / 44 untracked porcelain entries (NOT R1's 56).

---

## 2. 3 Failing Tests (task-builder-merge phrase drift)

Derived from R6 §2.2 and §6.3. All three failures are **NOT pre-existing** — they are caused by Phase 6 (`87c8254` MIG-006) rewriting SKILL.md / agent text and removing literals that earlier-milestone (M2/M5) tests still pin. Adjudication direction for all three: **update the test expectations to match the final SKILL.md / agent text** — NOT the reverse. The SKILL.md/agent text is the artifact under review and is canonical; the tests are the gate that must be aligned.

### Test 1

- **Full test ID:** `tests/skills/test_task_builder_merge.py::TestPR01ExecutionContextHeader::test_execution_context_uses_source_areas_not_paths`
- **File:line of assertion:** Not pinned to specific line in R6 source (R6 cites the test by ID; specific assertion line not captured in the research). The test resides within class `TestPR01ExecutionContextHeader` in `tests/skills/test_task_builder_merge.py`.
- **What it asserts vs current text:** Asserts the literal string `"NEVER write specific"` is present in `src/superclaude/skills/task-builder/SKILL.md`. Current state: phrase was **removed** by later edits during Phase 6.
- **Adjudication direction:** Update the test expectation in `tests/skills/test_task_builder_merge.py` to match the final SKILL.md text — not the reverse.

### Test 2

- **Full test ID:** `tests/skills/test_task_builder_merge.py::TestPR02RetryMonotonicityGuards::test_skill_regression_detection_precedence`
- **File:line of assertion:** Not pinned to specific line in R6 source. Test resides within class `TestPR02RetryMonotonicityGuards` in `tests/skills/test_task_builder_merge.py`.
- **What it asserts vs current text:** Asserts the literal `"Regression takes precedence"` (or lower-case variant) is present in `src/superclaude/skills/task-builder/SKILL.md`. Current state: phrase was **rewritten** by Phase 6.
- **Adjudication direction:** Update the test expectation in `tests/skills/test_task_builder_merge.py` to match the final SKILL.md text — not the reverse.

### Test 3

- **Full test ID:** `tests/skills/test_task_builder_merge.py::TestPR02RetryMonotonicityGuards::test_rf_task_builder_has_protocol`
- **File:line of assertion:** Not pinned to specific line in R6 source. Test resides within class `TestPR02RetryMonotonicityGuards` in `tests/skills/test_task_builder_merge.py`.
- **What it asserts vs current text:** Asserts the literal `"non-convergent"` is present in `src/superclaude/agents/rf-task-builder.md` (and synced `.claude/agents/rf-task-builder.md`). Current state: phrase was **rewritten** by Phase 6.
- **Adjudication direction:** Update the test expectation in `tests/skills/test_task_builder_merge.py` to match the final agent text — not the reverse.

**Gate:** Per R6 §2.3, the task-builder-merge PR (PR-C / PR-D) cannot open until `tests/skills/test_task_builder_merge.py` shows **68/68 PASS** (currently 65/68).

**Lint companion (R6 §4.3):** Audit tests carry **16 ruff issues** (10× N801 underscore class names, 1× N999 NFR uppercase module name, 4× F401 unused imports, 1× I001 unsorted import) — 6 are auto-fixable with `uv run ruff check tests/audit/ --fix`; the remaining N801/N999 must be renamed or annotated `# noqa: N801,N999`.

---

## 3. Stale Branches (dispositions)

Derived from R3 §3 (Stale Local Branches — Cleanup Recommendations). Local-branch inventory at session start (R3 §3 table):

| Local Branch                                          | Unique Commits vs HEAD | Disposition                                                                                                                                                                                          |
|-------------------------------------------------------|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `fix/auggie-flag-clear-mcp-prefix`                    | 2 (`f9a7e34`, `adb7d36`) | **Cherry-pick `adb7d36`** (175-line regression test `tests/hooks/test_auggie_flag_clear_mcp_prefix.py`) **into PR-F, then delete the branch.** `f9a7e34` is content-identical to merged PR #47; `adb7d36` is unique work not on HEAD nor on origin/master. |
| `feat/mig-002-execution-context-header`               | 0                      | **Delete after verifying no unique commits** (`git branch -D feat/mig-002-execution-context-header`). Fully merged into current branch (commits `2648be8` MIG-002 + `79644fa` D-0025 evidence both on HEAD). |
| `chore/task-cleanup-20260517`                         | 1 (`c9c35c3`)          | **Delete after verifying no unique commits** — content-identical to merged PR #48 (`c18879c`); diffstat matches (667 files, +110 lines). Superseded.                                                  |
| `chore/task-merge-consolidate-roadmap-to-release`     | 1 (`c1c1447`)          | **Delete after verifying no unique commits** — R3 §3 flagged this branch for "investigate before delete" because its unique commit is not on master nor on HEAD. Per task spec direction: delete-after-verify-no-unique (verify the commit content is either covered elsewhere or genuinely orphaned). |
| `master` (local)                                      | 0 (stale)              | Fast-forward: `git fetch && git branch -f master origin/master` (origin/master is 3 commits ahead per R3 §2.2: PRs #47, #48, #49). |

**Critical preservation note (R3 §3.1):** `tests/hooks/test_auggie_flag_clear_mcp_prefix.py` (175 lines) exists ONLY on `fix/auggie-flag-clear-mcp-prefix@adb7d36` — not on current HEAD's `tests/hooks/`, not on origin/master's `tests/hooks/`. Must be cherry-picked into PR-F before that branch is deleted.

---

## 4. Byte-Exact 51-Line PR Template

Verbatim from `.github/PULL_REQUEST_TEMPLATE.md` per R7 §GAP 3 (line count = 51, final line ends with `-->`):

```markdown
# Pull Request

## Summary

<!-- Briefly explain the purpose of this PR -->

## Changes

<!-- List the major changes -->
-
## Related Issues

<!-- Include related issue numbers, if any -->
Closes #

## Checklist

### Git Workflow
- [ ] For external contributions: Followed the flow of fork → topic branch → upstream PR.
- [ ] For collaborators: Used a topic branch (not directly committed to main).
- [ ] `git rebase upstream/main` completed (no conflicts).
- [ ] Commit messages conform to Conventional Commits (`feat:`, `fix:`, `docs:`, etc.).

### Code Quality
- [ ] Changes are limited to a single purpose (not a large PR, guideline: ~200 lines of difference).
- [ ] Follows existing code conventions and patterns.
- [ ] Add appropriate tests for new features/fixes.
- [ ] Lint/Format/Typecheck all pass.
- [ ] CI/CD pipeline successful (green status).

### Security
- [ ] Secrets and authentication information not committed.
- [ ] Necessary files excluded with `.gitignore`.
- [ ] No breaking changes, or if there are, commit with `!` and include in MIGRATION.md.

### Documentation
- [ ] Update documentation as needed (README, CLAUDE.md, docs/, etc.).
- [ ] Add comments to complex logic.
- [ ] Properly document API changes.

## Testing Methods

<!-- How to verify this PR works -->

## Screenshots (if applicable)

<!-- Attach screenshots if there are UI changes -->

## Notes

<!-- What you want to communicate to reviewers, background to technical decisions, etc. -->
```

---

## 5. Pre-PR Triplet

Verbatim from `CONTRIBUTING.md` lines 33-35 per R7 §GAP 4 (pinned at lines 33-35 inside the fenced bash block opened on line 32 and closed on line 36):

```bash
uv run ruff check src/ tests/
uv run pytest tests/<changed-area>/ -v
make verify-sync
```

**What each one checks (R7 §GAP 4 from CONTRIBUTING.md body):**
- `uv run ruff check src/ tests/` — Ruff lint over the whole source + tests tree. Catches new F-class, E-class, I-class, N-class, and W-class violations introduced by your branch.
- `uv run pytest tests/<changed-area>/ -v` — Pytest for the specific subtree your PR modifies (e.g. `tests/audit/` if you touched audit code). Faster than the full suite; catches functional regressions in the area you changed.
- `make verify-sync` — Drift check between `src/superclaude/` (source of truth for skills/agents/commands) and `.claude/` (the synced dev copies). If you edit `src/superclaude/skills/`, `src/superclaude/agents/`, or `src/superclaude/commands/`, run `make sync-dev` before this check.

**Important caveat (R7 §GAP 4):** CONTRIBUTING.md line 46 explicitly says: "This rot-budget rule is a **social convention** agreed by maintainers, **NOT** a CI-enforced gate." Do not assert it as a hard CI gate.

---

## 6. Conventional Commits Scope Vocabulary

Derived from R2 §1.2 (Repo-wide scope vocabulary, top scopes across all branches):

| Scope             | Use Case                                                                                       | Frequency (all branches) |
|-------------------|------------------------------------------------------------------------------------------------|--------------------------|
| `sprint`          | Sprint-runner CLI work (`src/superclaude/cli/sprint/**`) — **scope for PR-A (C1-C4)**          | 7 commits (`feat`)       |
| `task-builder`    | task-builder skill / agent / merge-release work                                                | 11 (`feat`) + 5 (`test`) + 3 (`docs`) |
| `hooks`           | Hook scripts / matcher / verify-sync — scope for PR-F hook-sync release evidence              | 3 (`feat`) + 2 (`fix`) + 1 (`chore`) |
| `release`         | Singular — close-out commits (e.g. `chore(release): close out <name>`)                         | 2 (`chore`)              |
| `releases`        | Plural — archive ops for release artifacts (e.g. `chore(releases): archive ...`)               | 6 (`chore`)              |
| `tests`           | Test-suite fixes (use composite `fix(sprint,tests)` if cross-cutting)                          | 2 (`fix`)                |
| `audit`           | (Implied scope for audit-test suite — derived from `tests/audit/` location; use composite or `test(audit)` style) | not in R2 top-scope list — recommended scope for PR-B per task spec |
| `commands`        | Slash-command surface changes                                                                  | 3 (`feat`)               |
| `skills`          | Skill packages (SKILL.md + refs/ + rules/)                                                     | 2 (`feat`)               |
| `ci`              | CI workflow / GitHub Actions                                                                   | 2 (`fix`)                |

**Composite scope precedent (R2 §1.2):** `feat(spawn,adversarial)`, `test(roadmap,sprint)`, `refactor(commands,skills)` — comma-separated, no spaces; pipe-separator `test(pipeline|roadmap|sprint)` is an outlier.

**Subject conventions (R2 §1.3):** Deliverable IDs embed in subject without separator — `MIG-NN`, `D-NNNN`, `T0N.NN`, `TEST-NNN`, `INV-NNN`, `FR-CONV.N`. Milestone tags as parenthesized suffix: `(M2)`..`(M6)`. Resolution markers: `resolve OQ-N (...)`, `close out <release-name>`, `land <FR-id>`. No hard 72-char rule (median ~80, max ~253).

**Co-Authored-By signoff (R2 §1.5):** canonical form — `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>` (preceded by a blank line).

---

**End of synthesis.**
