# Research Notes: Branch QA + Commit + PR Workflow for feat/hook-sync-and-matcher-fix

**Date:** 2026-05-18
**Scenario:** A (Explicit — scope and concerns specified by user)
**Depth Tier:** Deep
**Track Count:** 1 (all concerns target one branch's commit/PR strategy; cross-cutting QA spans the whole branch)

---

## EXISTING_FILES

### Branch state (verified 2026-05-18 18:13Z)

**Commit lineage:**
- HEAD = `efaa33d` on `feat/hook-sync-and-matcher-fix`
- 15 commits ahead of `master` (`516bb46`)
- NO local `integration` branch; NO `origin/integration` remote ref → upstream's "integration" model documented in CLAUDE.md is not currently set up in this clone
- Remote tracking: only `remotes/origin/feat/hook-sync-and-matcher-fix` exists for this branch's remote

**The 15 commits since master (newest → oldest):**
- `efaa33d` chore(hooks): resolve OQ-2 (archive+delete bash-gate orphan) and OQ-3 (register reject-workspace-writes.sh)
- `87c8254` feat(task-builder): MIG-006 land FR-CONV.6 Synthetic-DNSP on Partition Exhaust (M6)
- `5439ea1` feat(hooks): widen auggie-flag-clear matcher to mcp__auggie-mcp__; add verify-sync hook coverage and cross-consistency checks
- `edd3ddd` docs(task-builder): D-0067 T05.16 MIG-005 evidence + FF governance entry
- `db6166e` feat(task-builder): MIG-005 land FR-CONV.5 Retry Monotonicity + Regression Halts (M5)
- `0dcc947` test(task-builder): D-0066 T05.15 TEST-024 sequencing inversion fixture (K-007 mitigation)
- `c9e2b12` test(task-builder): D-0065 T05.14 TEST-017 + TEST-022 slow-shrink + cross-cycle dedup fixtures
- `20b58f6` test(task-builder): D-0064 T05.13 TEST-015 + TEST-016 monotonicity + regression halt fixtures
- `487e76b` feat(task-builder): MIG-004 land FR-CONV.4 Five Adversarial Axes overlay (M4)
- `8b7fe5f` docs(task-builder): D-0039 T03.16 MIG-003 evidence + FF governance entry
- `ad083b6` feat(task-builder): MIG-003 land FR-CONV.3 Inherited Structural Verdict + Self-Audit (M3)
- `de7829d` test(task-builder): D-0038 T03.15 TEST-010 dynamic enumeration INV-010 fixture
- `bb5d751` test(task-builder): D-0037 T03.14 TEST-009 Self-Audit INV-019 fixture
- `79644fa` docs(task-builder): D-0025 T02.11 MIG-002 evidence + FF governance entry
- `2648be8` feat(task-builder): MIG-002 land FR-CONV.2 Execution Context header (M2)

**Logical grouping of committed work:**
- Group A: task-builder-merge milestones M2-M6 (most of the 15 commits — `2648be8`, `79644fa`, `bb5d751`, `de7829d`, `ad083b6`, `8b7fe5f`, `487e76b`, `20b58f6`, `c9e2b12`, `0dcc947`, `db6166e`, `edd3ddd`, `87c8254`) = 13 commits
- Group B: hook-sync-and-matcher-fix proper (`5439ea1`, `efaa33d`) = 2 commits

### Uncommitted scope (verified 2026-05-18 18:13Z)

**Modified files (14):**
- **Sprint runner C1-C4 source (4):** `src/superclaude/cli/sprint/{commands,config,executor,models}.py`
- **Sprint runner C1-C4 tests (5):** `tests/sprint/{test_config,test_executor,test_models,test_regression_gaps,test_watchdog}.py`
- **Pipeline C2 test (1):** `tests/pipeline/test_process.py`
- **task-builder-merge sprint logs (3):** `.dev/releases/current/task-builder-merge/{execution-log.jsonl, execution-log.md, results/phase-4-output.txt}` (mid-sprint updates)
- **Reflexion test pollution (1):** `docs/memory/solutions_learned.jsonl` (16 duplicate test fixture entries appended at `2026-05-18T01:54` and `2026-05-18T12:23` — NOT real solutions, simulated test data from reflexion test runs)

**Untracked paths (123):**
- `.dev/releases/current/task-builder-merge/artifacts/D-00**/` (12 hr sprint artifacts D-0053..D-0100 — release evidence, spec.md + evidence.md per deliverable)
- `.dev/releases/current/task-builder-merge/checkpoints/CP-P0*-*` (18 of 21 expected — Phase 1 checkpoints `CP-P01-END`, `CP-P01-T01-T05`, `CP-P01-T07-T11` ABSENT)
- `.dev/releases/current/task-builder-merge/{adversarial,analysis,checkpoints,context-digests,prompt-refactor,proposals,reflection,results}/...`
- `.dev/releases/current/hook-sync-and-matcher-fix/` (hook release work artifacts)
- `.dev/tasks/done/` (3 new build-request / research-prompt files just added)
- `.dev/tasks/to-do/TASK-RF-20260518-015659/` (C1-C4 task file + 33 phase-outputs already complete and validated)
- `.dev/tasks/to-do/TASK-RF-20260518-181333/` (THIS task being built)
- `.dev/eval-runs/research` (eval workspace)
- `tests/audit/test_*.py` (8 new audit tests: `test_dnsp_*`, `test_hidden_input_guard`, `test_invariant_preservation_NFR_6_through_10`, `test_nfr_conv_*`) + `tests/audit/fixtures/`
- `tests/sprint/*.py` (a few new untracked sprint tests beyond the 5 modified)
- `tests/pipeline/*.py` (new untracked pipeline test beyond the 1 modified)
- `docs/mistakes/test_database_connection-2026-05-18.md`, `test_reflexion_with_real_exception-2026-05-18.md`, `unknown-2026-05-18.md` (test artifacts — same pollution as solutions_learned.jsonl)
- `docs/reference/nfr-conv-2-prose-determinism.md` (real spec document)
- **3 repo-root garbage paths:** `0.20` (empty 0-byte file from misparsed `>=0.20` install string), `prd-test-product/` (PRD skill test-output dir, only `execution-log.md` inside), `prd-dry-run-test/` (same shape)

**Untracked breakdown by top-level dir:**
- `.dev/` — 105 paths (sprint artifacts + task files + eval workspace; mostly DON'T need PR review)
- `tests/` — 11 paths (8 audit + 2-3 sprint/pipeline = new tests requiring review)
- `docs/` — 4 paths (1 real spec doc + 3 test artifacts to delete)
- repo root — 3 paths (all garbage to delete or .gitignore)

### Key context files
- `CONTRIBUTING.md` — exists at repo root
- `.github/PULL_REQUEST_TEMPLATE.md` — exists, defines PR convention
- `CLAUDE.md` — describes branch model `master ← integration ← feature/*` (integration apparently not currently set up on origin)
- `.github/` — has workflows but no CODEOWNERS detected
- `.gitignore` — exists, needs review for `0.20`, `prd-*-test/`, `.dev/eval-runs/` patterns

### Already-complete task that informs this one
- `.dev/tasks/to-do/TASK-RF-20260518-015659/` — C1-C4 sprint runner fixes task, status=🟢 Done, 47/47 items checked, 5/5 gates PASS, 13/13 new tests green. Production code + tests are the C1-C4 portion of the uncommitted set.
- `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/reviews/qualitative-review.md` — surfaced C7 follow-up (per-task watchdog coverage gap).

### Already-investigated symptoms
- task-builder-merge manifest reports `total: 21, found: 0, missing: 21` because manifest expected `TASKLIST_ROOT/checkpoints/` but actual checkpoints live at `checkpoints/` (no `TASKLIST_ROOT` subfolder). Of the 21 expected items, 18 exist on disk; 3 truly absent (all Phase 1: `CP-P01-END`, `CP-P01-T01-T05`, `CP-P01-T07-T11`).
- Phase 1's commits (`2648be8` MIG-002 + ancestors) landed BEFORE this branch's current head — Phase 1 of the sprint correspondingly preceded the checkpoint-writing convention.

---

## PATTERNS_AND_CONVENTIONS

### Commit message convention (from 15-commit history)
- Prefix-typed: `feat(scope)`, `test(scope)`, `docs(scope)`, `chore(scope)` per Conventional Commits
- Scope names observed: `task-builder`, `hooks`
- Subject line often includes deliverable ID (`MIG-004`, `D-0039`, `T03.16`) and phase relation (`(M3)`, `(M4)`)
- Format: `<type>(<scope>): <subject>` with deliverable ID typically embedded in subject

### Branch naming convention (from local + remote branches)
- `feat/<topic-kebab-case>` for features
- `fix/<topic-kebab-case>` for fixes
- `chore/<topic-kebab-case>` (sometimes with date suffix `-20260517`)
- `feat/<topic>-<id>` for sub-feature branches (e.g., `feat/mig-002-execution-context-header`)

### File staging discipline
- Per CLAUDE.md global instructions: "When staging files, prefer adding specific files by name rather than using `git add -A` or `git add .`, which can accidentally include sensitive files (.env, credentials) or large binaries"
- Critical for this task: do NOT bulk-add — must group by logical commit

### PR template structure
- `.github/PULL_REQUEST_TEMPLATE.md` exists — researchers should read full content and document required sections.

### CONTRIBUTING workflow
- `CONTRIBUTING.md` at root — researchers should extract PR/review/merge rules.

---

## GAPS_AND_QUESTIONS

1. **Integration branch existence**: No local `integration`, no `origin/integration`. Was the integration branch ever set up? Researchers must check `git config branch.*.merge`, the GitHub project page (if accessible), and CONTRIBUTING.md for whether `integration` is real. If not, the branching strategy must adapt — maybe just `feature → master` PRs.

2. **Untracked sprint+pipeline tests overlap**: Some tests in `tests/sprint/` and `tests/pipeline/` are MODIFIED (C1-C4 work I committed mentally but didn't `git commit`) and others appear UNTRACKED. Need exact file-by-file breakdown to know which tests belong to which logical group.

3. **task-builder-merge artifact strategy**: 105 untracked paths under `.dev/releases/current/task-builder-merge/`. Should release artifacts be:
   - Committed to the branch as evidence trail (project convention seems to do this — see existing committed artifacts D-0001..D-0040 are already in git history)?
   - Excluded from PR via .gitignore additions?
   - Squashed to a single "release evidence" commit?
   Researchers should look at how prior releases (e.g., `unified-audit-gating-v1.2.1` in `.dev/releases/complete/`) handled artifact commits.

4. **3 missing Phase 1 checkpoints**: Were they written but to a different path, or never written? Sprint runner pre-checkpoint convention investigation needed. Are the corresponding work products (D-0001..D-0010 artifacts) committed already (per the MIG-002 commit `2648be8`)?

5. **prd-test-product / prd-dry-run-test origin**: These are PRD-skill test runs that landed at repo root instead of `.dev/eval-runs/`. Was this a one-time accident or a real PRD CLI bug? Researchers should check `src/superclaude/cli/prd/` for output-path defaults.

6. **docs/memory/solutions_learned.jsonl pollution**: 16 simulated entries appended on 2026-05-18 by test runs (reflexion test fixtures). Should this file be:
   - Reverted to its pre-test state?
   - .gitignored entirely?
   - Filtered to remove only test-pattern entries?

7. **C7 follow-up integration**: The per-task watchdog coverage gap surfaced by G5 qualitative review of TASK-RF-20260518-015659 — should this become a separate PR or just a follow-up issue in the C1-C4 PR description?

8. **Test failure attribution**: The 57 pre-existing `.stdin AttributeError` failures (commit 4799719, 2026-04-20) are NOT this branch's issue. The PR should document this attribution clearly so reviewers don't blame this branch.

9. **Stale local branches**: `feat/mig-002-execution-context-header`, `fix/auggie-flag-clear-mcp-prefix`, `chore/task-cleanup-20260517`, `chore/task-merge-consolidate-roadmap-to-release` may all be merged-into-current-branch work that can be deleted. Researchers should verify.

10. **Working merge-conflict surface**: This branch is 15 commits ahead of master. We need to know which files conflict against master. Researchers should run `git merge-tree` or `git merge --no-commit --no-ff` (in worktree) to identify conflicts before PR planning.

---

## RECOMMENDED_OUTPUTS

The task file should produce these logical commit groups + branching strategy + PR plan. The 7 researchers' outputs feed into a single task file with phases:

| Phase Class | What | Who covers it |
|---|---|---|
| Branch + git lineage | Define base for new sub-branches; verify integration model | R3 Integration |
| Uncommitted inventory + grouping | Per-file decision: commit / .gitignore / delete; group into N logical commits | R1 File Inventory + R3 Integration |
| Branching strategy | Decide: stay-on-current-branch vs split-into-sub-branches; choose base branches | R4 Template & Examples (PR template + CONTRIBUTING + similar prior splits) |
| PR sequence + dependencies | Title, base, body, dependencies per PR | R4 + R7 Solution Research (web for multi-PR best practices) |
| Merge conflict resolution | Identify conflicts against master (and any sub-branches that get split off) | R3 + R5 Data Flow Tracer (git merge-tree analysis) |
| QA pass | What QA needs to run on each logical group before PR open (lint, tests, sync verification) | R6 Test & Verification |
| Garbage cleanup | 0.20 file, prd-test-product/, prd-dry-run-test/, solutions_learned.jsonl pollution, docs/mistakes/ test artifacts | R1 + R2 Patterns |

### Researcher assignments

| # | Topic | Scope | Output file |
|---|---|---|---|
| R1 | File Inventory | Full git status — every modified & untracked path; per-path classification (commit/gitignore/delete) | `research/01-file-inventory.md` |
| R2 | Patterns & Conventions | Existing commit-message style + branch naming + .gitignore patterns + how prior releases (unified-audit-gating-v1.2.1 in .dev/releases/complete/) handled artifact commits | `research/02-patterns-and-conventions.md` |
| R3 | Integration Points | Branch lineage: integration branch existence (local + remote); merge-base against master; merge-tree conflict analysis; stale local branches to clean | `research/03-integration-points.md` |
| R4 | Template & Examples | `.github/PULL_REQUEST_TEMPLATE.md` full content; CONTRIBUTING.md full content; prior multi-PR splits if any in git history; MDTM template 02 conventions | `research/04-template-and-examples.md` |
| R5 | Data Flow Tracer | Where do sprint artifacts go (release skill output paths)? Where do prd-skill outputs go (src/superclaude/cli/prd/)? Where does reflexion put solutions? — diagnose root causes of garbage paths so the cleanup is informed | `research/05-data-flow-tracer.md` |
| R6 | Test & Verification | What's the right QA pass per logical group? — `make lint`, `make test`, `uv run pytest tests/<area>/`; what's the C1-C4 internal QA verdict already known; what's the test-pollution scope (16 entries in solutions_learned.jsonl); pre-existing failure attribution to surface in PR descriptions | `research/06-test-and-verification.md` |
| R7 | Solution Research (WEB) | Multi-PR splitting best practices for long-lived branches; trunk-based dev vs gitflow guidance for this scenario; how to write PR descriptions that surface dependency chains; conventional commits scope guidance | `research/web-01-multi-pr-strategy.md` |

7 researchers spawned in parallel. Auggie codebase-retrieval should be used by R3, R5, and R6 for codebase-spanning queries (session-context auggie_first_required=1).

---

## SUGGESTED_PHASES

(Builder will construct the actual phases. This is the recommended shape.)

| Phase | Purpose | Items |
|---|---|---|
| **P1 Preparation** | Status update + handoff dirs + branch baseline snapshot (git status, git log master..HEAD captured into evidence files for PR descriptions) | 3-4 items |
| **P2 Discovery — Per-File Classification** | Walk every modified + untracked path; classify as: commit-this-PR / commit-different-PR / .gitignore / delete. Output: a comprehensive classification table to `phase-outputs/discovery/file-classification.md` | 1 large discovery item (could split per-area) |
| **P3 Garbage Cleanup** | Delete `0.20`, `prd-test-product/`, `prd-dry-run-test/`; revert `docs/memory/solutions_learned.jsonl` to pre-test state; delete docs/mistakes/ test artifacts; verify `.gitignore` covers root-level test outputs to prevent recurrence | 5-7 items |
| **P4 Branching Strategy Decision** | Choose: stay on current branch, OR split into N sub-branches. Decision criteria documented. New branch names (if splitting) created via `git checkout -b` from clean baseline | 3-5 items |
| **P5 Logical Commit Grouping** | For each logical group (sprint-runner-c1-c4, task-builder-merge-evidence, hooks, audit tests, docs/reference, solutions-learned-cleanup), stage files with `git add <specific-files>` (no `-A` or `.`) and commit with Conventional Commits message. Each group = one focused commit | 5-8 items (one per group) |
| **P6 QA Pass per Commit** | After each logical commit, run targeted QA: lint changed files only, run targeted pytest, verify `make verify-sync` if `.claude/` touched. Use phase-7 evidence from C1-C4 task as baseline | 4-6 items |
| **P7 Merge Conflict Analysis** | Run `git merge-tree master HEAD HEAD~N` for each commit; or `git rebase --interactive master --exec 'git status'` (in worktree) to detect conflicts. Document conflicts per file, propose resolution | 3-4 items |
| **P8 PR Plan Authoring** | Write per-PR description files at `phase-outputs/prs/PR-<n>-<title>.md` using the project PR template format. Each PR description must include: title, base, summary, test plan, breaking changes, related issues/PRs, dependencies on other PRs in this sequence | 1 item per PR (5-7 items) |
| **P9 PR Sequencing + Dependencies** | Build a dependency graph: which PRs must merge first; document with mermaid diagram or DAG textual form. Identify which PRs can land in parallel | 2-3 items |
| **P10 Final QA Gate (rf-qa-qualitative)** | Verify whole plan would actually succeed if executed; sanity-check the PR sequence + base-branch choices + conflict resolutions | 1 QA gate spawn item + 1 verdict item |
| **P11 Post-Completion** | Update task status to Done; write Task Summary; document outstanding items as follow-ups (PR opening itself is OUT OF SCOPE for this task — this task PRODUCES the plan, the user executes the plan) | 3-4 items |

Expected total items: 30-45 (well within TB-Add-2 single-track bound of ≤50).

---

## TEMPLATE_NOTES

- **Template selection: 02 (Complex Task)** — Reasoning:
  - Multi-phase work with discovery (per-file classification) → decision (branching) → execution (commits) → verification (QA) → planning (PR specs).
  - Conditional flows (if integration doesn't exist, fallback to feature → master).
  - Multiple QA gates required (PER_PHASE for the commit phases; final qualitative gate).
  - Subagent delegation likely needed for: web research on multi-PR strategy, possibly rf-qa for per-commit verification.

- **QA_GATE_REQUIREMENTS: FINAL_ONLY** — Reasoning: This task is PLANNING + EXECUTING git-level operations + producing PR description docs. It does NOT modify production code. A heavy per-phase QA-gate cadence (like the C1-C4 task used) would be overkill; instead, a single final rf-qa-qualitative gate verifying the plan + executed commits + PR specs is appropriate. The MERGE-CONFLICT detection phase has its own implicit verification (the `git merge-tree` output IS the verification).

- **TESTING_REQUIREMENTS: NONE** — Reasoning: This task does NOT add new functionality. It packages existing committed/uncommitted work for PR review. The "testing" is per-commit QA passes (`make lint` + targeted pytest) executed during P6, not new test code.

- **VALIDATION_REQUIREMENTS:** For each logical commit, validate: (a) `make lint` runs ruff-clean on changed files (per the C1-C4 task pattern — checks only changed files, ignores repo-wide pre-existing failures); (b) targeted pytest passes for tests in the commit's scope; (c) commit message follows Conventional Commits format; (d) commit doesn't accidentally include garbage files. NO repo-wide `make test` requirement (would surface 57 pre-existing failures that aren't this branch's concern, per C1-C4 phase-7 evidence).

- **EXECUTION_CONTEXT_REQUIREMENTS: AUTO** — Should emit (≥3 inferable source areas: branch state + uncommitted scope, commit message + branch naming conventions, PR template + CONTRIBUTING workflow, garbage cleanup, sprint runner C1-C4 portion).

---

## AMBIGUITIES_FOR_USER

1. **Integration branch absence**: No local or remote `integration` ref. CLAUDE.md describes `master ← integration ← feature/*` but the actual setup may have changed. The task proceeds with the assumption that PRs will target `master` directly. If the user uses `integration` (perhaps in upstream `SuperClaude_Framework` repo not visible from this fork), they should redirect base branches accordingly before opening PRs.

2. **Sprint-artifact commit policy**: Whether 105 sprint artifact files under `.dev/releases/current/task-builder-merge/` should be:
   - (a) Committed in full as evidence trail (matches the project's apparent convention — `.dev/releases/complete/` directories appear to be committed historically),
   - (b) Compressed to a `release-evidence` archive and committed as a single file,
   - (c) Excluded from PR via `.gitignore` addition.
   **Default in this task: (a) commit in full**, splitting into multiple commits to keep each <500 files. User may override before PR open.

3. **PR splitting depth**: User said "some should become separate feature branches". Decision criteria default proposed:
   - SPLIT when: independent reviewers / different review areas / different ship cadence / cross-functional concerns (e.g., hooks vs Python sprint code vs tests vs release artifacts)
   - DON'T SPLIT when: tightly coupled / shared reviewer / shared landing date
   **Default split (5-7 PRs proposed)** — user may merge or further split.

4. **Branching strategy — fresh branches off master vs off current branch**: If we split into sub-PRs, do new branches branch from `master` (clean slate, may require cherry-picking the 15 existing commits into the right sub-branch) or from `feat/hook-sync-and-matcher-fix` (inheriting all 15 commits, then carving out subsets via cherry-pick to other branches)? **Default: branch from master, cherry-pick relevant commits into each sub-branch.** Cleaner history but more cherry-picks.

5. **Stale-branch cleanup scope**: 4 stale local branches identified. Should the task delete them as part of cleanup? **Default: NO — out of scope. Document as follow-up.** User can `git branch -d` after confirming.

6. **Reflexion test pollution remediation**: 16 simulated entries in `docs/memory/solutions_learned.jsonl` and 3 test artifacts in `docs/mistakes/`. Should the test infrastructure that produces these be fixed in this task or just clean up the artifacts? **Default: clean artifacts now, file follow-up for test infra fix.** Test-infra fix is a separate concern from "package this branch for PR".

7. **PR-opening execution**: This task PRODUCES the plan + executes commits + writes PR description files. Does the user want this task to ALSO open the PRs via `gh pr create`? **Default: NO — task ends with plan + commits + PR description files. User reviews and opens PRs manually via `gh pr create --body-file <path>`.** Opens are reversible/state-changing operations that warrant human confirmation.
