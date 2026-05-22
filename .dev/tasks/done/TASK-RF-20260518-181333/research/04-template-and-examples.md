# Researcher 4 — Template & Examples

**Status:** Complete
**Researcher:** R4 of 7
**Scope:** PR template, CONTRIBUTING.md, CI workflows, multi-PR split priors, MDTM template rules, analogous prior task
**Branch under audit:** `feat/hook-sync-and-matcher-fix`

---

## 0. CRITICAL UPSTREAM FINDING — Branch Already Has a Merged PR

Before any builder action, the orchestrator MUST know:

- **PR #49** on this exact branch (`feat/hook-sync-and-matcher-fix`) **was already merged to `master` on 2026-05-18T02:21:08Z** (title: `feat(hooks): widen auggie-flag-clear matcher and add verify-sync hook coverage`).
- Source: `gh pr list --state merged --limit 30 | head -1` → row `49 ... MERGED 2026-05-18T02:21:08Z`.
- Full PR #49 body retrieved via `gh pr view 49 --json` documents three "Parts" (Part 1 test coverage, Part 2 user-impact bug fix, Part 3 structural prevention) already shipped against `master`.
- Working-tree `git status` shows `M Makefile`, `M src/superclaude/hooks/hooks.json`, `M src/superclaude/hooks/scripts/auggie-flag-clear.sh`, plus uncommitted `.dev/releases/current/hook-sync-and-matcher-fix/` and `.dev/releases/current/task-builder-merge/` artifacts.

**Implication for the task builder:** the "branch QA + commits + PR plan" being scoped here is for a **post-merge follow-up** on top of an already-merged PR #49 — not the initial PR. The new task file should explicitly state this, and the PR-plan items should target a NEW branch cut from latest `master` (or be additive commits to be opened as a *second* PR), never reopen #49.

---

## 1. `.github/PULL_REQUEST_TEMPLATE.md` — Verbatim

**Path:** `/config/workspace/IronClaude/.github/PULL_REQUEST_TEMPLATE.md`
**Length:** 52 lines

### Section inventory

| Line | Heading | Required? | Notes |
|---|---|---|---|
| 1 | `# Pull Request` | required | top-level H1 |
| 3 | `## Summary` | required | free-text, "Briefly explain the purpose of this PR" |
| 7 | `## Changes` | required | bulleted list, starts with `-` placeholder on line 10 |
| 11 | `## Related Issues` | required | `Closes #` placeholder on line 14 |
| 16 | `## Checklist` | required | 4 sub-sections of checkboxes |
| 18 | `### Git Workflow` | required | 4 checkbox items |
| 24 | `### Code Quality` | required | 5 checkbox items |
| 31 | `### Security` | required | 3 checkbox items |
| 36 | `### Documentation` | required | 3 checkbox items |
| 41 | `## Testing Methods` | required | free-text "How to verify this PR works" |
| 45 | `## Screenshots (if applicable)` | optional-conditional | |
| 49 | `## Notes` | optional | reviewer-facing context |

### Verbatim content (byte-for-byte, the builder must mirror this exactly)

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

<!-- What you want to communicate to reviewers, background to technical decisions, etc.
```

### Footer / signoff observations

- **No** `🤖 Generated with [Claude Code]` footer in the template itself.
- The **actual merged PR #49** body **does** include `🤖 Generated with [Claude Code](https://claude.com/claude-code)` as the final line (per `gh pr view 49` retrieval) — this is a project convention layered on top of the template, not in the template.
- **No `Co-Authored-By` footer** in template, but global instructions (Claude Code default) require `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>` on commits.

### Template deviation observed in PR #49 actual body

PR #49 substantially **deviated** from the template structure:
- Used `## Summary` (matches template) → `## Changes` (matches) → `## Test plan` (NOT in template; template says `## Testing Methods`) → `## Open Questions / Expected Failures` (NOT in template) → `## Deliberate spec deviations` (NOT in template) → `## Acceptance Criteria` (NOT in template).
- The 18-item checkbox checklist (`### Git Workflow`, `### Code Quality`, etc.) was **omitted entirely** from PR #49's body.

**Builder implication:** the template is descriptive, not enforced. The PR #49 body is the *de facto* convention for substantive feature PRs in this repo. The builder should produce PR descriptions in the **PR #49 style** for technical PRs, while leaving the checklist as a fallback for trivial PRs.

---

## 2. `CONTRIBUTING.md` — Verbatim

**Path:** `/config/workspace/IronClaude/CONTRIBUTING.md`
**Length:** 49 lines
**Created:** PR #41 on 2026-05-17 (`docs(ci): add CONTRIBUTING.md CI Hygiene + fix pull-sync push target`)

### Verbatim content

```markdown
# Contributing to SuperClaude Framework

This document captures lightweight contributor conventions for the IronClaude fork. It is intentionally short — the goal is to make it easy to do the right thing by default, not to encode every possible rule.

## CI Hygiene

### The rot-budget rule

**No PR may introduce a *new* lint or test failure.** Pre-existing failures on `master` are allowed to remain — they will be addressed in dedicated rot-cleanup PRs — but a PR that *adds* a failure must fix it before it merges.

This rule keeps two things separate:

- **New regressions** — strictly disallowed; the PR author owns the fix.
- **Inherited rot** — acceptable in any individual PR; tracked separately and cleaned up in focused PRs.

### What counts as a "new failure"

A "new failure" is any lint or test failure that is **NOT present in the most recent CI run on `master`** at the time the PR branch was created.

To check whether a failure in your PR is new or inherited:

1. Look at the latest CI run on `master` (the merge commit your branch was cut from).
2. If the same test ID or lint rule + file:line is failing on `master`, it is **inherited** (acceptable for your PR).
3. If the failure appears on your branch but NOT on the `master` baseline, it is **new** (must be fixed before merge).

When in doubt, run the same check locally on master (`git stash && git checkout master && <run check>`) and compare.

### Pre-PR local checks

Before opening a PR, run these three commands from the repo root:

\`\`\`bash
uv run ruff check src/ tests/
uv run pytest tests/<changed-area>/ -v
make verify-sync
\`\`\`

What each one checks:

- `uv run ruff check src/ tests/` — Ruff lint over the whole source + tests tree. Catches new F-class, E-class, I-class, N-class, and W-class violations introduced by your branch.
- `uv run pytest tests/<changed-area>/ -v` — Pytest for the specific subtree your PR modifies (e.g. `tests/audit/` if you touched audit code). Faster than the full suite; catches functional regressions in the area you changed.
- `make verify-sync` — Drift check between `src/superclaude/` (source of truth for skills/agents/commands) and `.claude/` (the synced dev copies). If you edit `src/superclaude/skills/`, `src/superclaude/agents/`, or `src/superclaude/commands/`, run `make sync-dev` before this check.

### Disclaimer: social convention, not a CI-enforced gate

This rot-budget rule is a **social convention** agreed by maintainers, **NOT** a CI-enforced gate. CI will still pass PRs that violate the rot-budget if the underlying job is green (or if the underlying job has been failing on master and continues to fail at the same level). Enforcement relies on PR reviewers checking the rule during code review.

If you find a PR that violates the rule (a new failure that wasn't present on master), call it out in the review and ask the author to either fix the regression or document why it's acceptable.
```

### Extracted rules / conventions

| Rule | Source | Builder action |
|---|---|---|
| **Rot-budget**: no PR may introduce a *new* lint or test failure | `CONTRIBUTING.md:9` | Builder must add an explicit "rot-budget" check item in Phase QA: compare branch CI vs latest master baseline; classify as new/inherited |
| **Pre-PR local checks (mandatory triplet)** | `CONTRIBUTING.md:30-36` | Builder must include these three commands as separate self-contained items in QA phase: `uv run ruff check src/ tests/`, `uv run pytest tests/<changed-area>/ -v`, `make verify-sync` |
| **Sync discipline**: edits to `src/superclaude/{skills,agents,commands}` require `make sync-dev` before `make verify-sync` | `CONTRIBUTING.md:42` | Builder must include a `make sync-dev` item BEFORE the `make verify-sync` item if the branch modifies any `src/superclaude/{skills,agents,commands}` path |
| **No commit-message format mandated in CONTRIBUTING.md itself** — but PR template line 22 mandates Conventional Commits (`feat:`, `fix:`, `docs:`) | `.github/PULL_REQUEST_TEMPLATE.md:22` | Cross-reference R2 |
| **No DCO / signoff requirement** | absence | none |
| **No PR sizing rule in CONTRIBUTING** — but PR template line 25 advises "~200 lines of difference" | `.github/PULL_REQUEST_TEMPLATE.md:25` | Builder should flag PRs > 200 LOC for split |
| **No CODEOWNERS file** | `ls .github/` → absent | No mandatory reviewer routing |
| **No ISSUE_TEMPLATE directory** | `ls .github/` → absent | none |

---

## 3. `.github/workflows/` — CI Workflows Triggered by PRs

**Path:** `/config/workspace/IronClaude/.github/workflows/`
**Files (5):**

| Workflow | File | Triggers | What it runs | Required for PRs? |
|---|---|---|---|---|
| Quick Check | `quick-check.yml` | `pull_request` to `master, integration` | Python 3.10: `pytest tests/unit/ -v --tb=short -x`, `ruff check src/ tests/`, `ruff format --check src/ tests/`, `pytest --trace-config \| grep superclaude`, `make verify-sync` | **YES** — runs on every PR to master/integration; fast (≤10 min timeout) |
| Tests (full matrix) | `test.yml` | `push` AND `pull_request` to `master, integration` + manual | Matrix Python 3.10/3.11/3.12: full `pytest -v --tb=short`, coverage on 3.10, Codecov upload, separate `lint` job | **YES** — runs on every PR |
| README Quality Check | `readme-quality-check.yml` | `pull_request` with paths filter `README*.md`, `Docs/**/*.md` + push to `main, master, develop` | Multi-language README quality assessment | **CONDITIONAL** — only fires if PR touches README/Docs markdown |
| Pull Sync from Framework | `pull-sync-framework.yml` | `schedule: '0 */6 * * *'` + manual | Cross-repo sync from upstream `SuperClaude_Framework` | **NO** — scheduled cron, not PR-triggered |
| Publish to PyPI | `publish-pypi.yml` | `release: published` + manual | PyPI publish | **NO** — release-triggered |

### Required status checks on PRs

The CI surface a PR must pass before merge is the **union of `quick-check.yml` + `test.yml`** (both `pull_request: [master, integration]`). For README/Docs-only PRs, `readme-quality-check.yml` also runs.

Key commands inside `quick-check.yml` that the task-builder must mirror as local-verify items:

```yaml
- pytest tests/unit/ -v --tb=short -x
- ruff check src/ tests/
- ruff format --check src/ tests/
- pytest --trace-config 2>&1 | grep -q "superclaude"
- make verify-sync
```

Key commands inside `test.yml`:

```yaml
- pytest -v --tb=short --color=yes
- pytest --cov=superclaude --cov-report=xml --cov-report=term   # Python 3.10 only
```

---

## 4. Other `.github/` Files

| File | Status | Builder impact |
|---|---|---|
| `.github/FUNDING.yml` | exists | none — sponsorship metadata |
| `.github/CODEOWNERS` | **MISSING** | No auto-assigned reviewers; PR author can self-route |
| `.github/ISSUE_TEMPLATE/` | **MISSING** | Issue creation is freeform; not relevant to PR plan |

---

## 5. Prior Multi-PR Split Examples — The 5-PR CI Rot Remediation Sequence

**There IS strong precedent** for multi-PR splits in this repo. The most recent and analogous is the **5-PR CI rot remediation sequence** (PRs #37 → #41, merged 2026-05-17):

| PR # | Title | Branch | Merged |
|---|---|---|---|
| #37 | `fix(lint): ruff --fix sweep — F401 unused imports + I001 import order` | `fix/ci-rot-pr1-ruff-autofix` | 2026-05-17T04:21:42Z |
| #38 | `style(lint): ruff format --check now passes` | `fix/ci-rot-pr2-ruff-format` | 2026-05-17T04:39:21Z |
| #39 | `fix(lint): rename ambiguous identifiers (E741) and naming-convention violations (N806/N811/F811/F841)` | `fix/ci-rot-pr3-manual-renames` | 2026-05-17T05:07:34Z |
| #40 | `fix(tests): repair tests/audit/ fixtures + xfail genuinely-broken cases` | `fix/ci-rot-pr4-test-fixture-repair` | 2026-05-17T05:19:14Z |
| #41 | `docs(ci): add CONTRIBUTING.md CI Hygiene + fix pull-sync push target` | `fix/ci-rot-pr5-contributing-and-pullsync` | 2026-05-17T05:28:45Z |

### Patterns the builder must mirror

1. **Branch naming**: `<type>/ci-rot-pr<N>-<slug>` — sequential PR numbers embedded in branch name; type prefix matches conventional-commit type of the PR.
2. **Base branch**: all 5 PRs targeted `master` directly (NOT stacked on each other) — confirmed by `baseRefName:"master"` on PR #49 and the merge timing (all 5 merged within 67 minutes, suggesting they were rebased onto each other's merge commits as they landed).
3. **Dependency order**: PR1 (autofix) → PR2 (formatter, depends on PR1 baseline) → PR3 (manual renames, depends on PR1+PR2 clean baseline) → PR4 (tests) → PR5 (docs). Each prior PR's task file documents: `**This task blocks:** TASK-RF-track-N+1-...`.
4. **Task files**: each PR had a corresponding `TASK-RF-track-N-20260517-032112` directory in `.dev/tasks/done/` — 5 tracks, identical timestamp suffix, monotonically increasing track number.
5. **Single shared research-notes.md per task**: each track's task references `.dev/tasks/.../research-notes.md` containing the multi-PR sequence rationale (`Q2 chose bulk auto-fix strategy`).
6. **AC4 explicitly names branch, base, title, body structure** — e.g. PR1's AC4: *"A PR exists on branch `fix/ci-rot-pr1-ruff-autofix` targeting `master` with the exact title ... and a body matching the structure in Step 4.2."*

### Other relevant prior-split markers in git log

- `git log --grep="part 1 of\|split\|stack"`: PR #49 itself (commit `feat(task-builder): MIG-005 land FR-CONV.5 Retry Monotonicity`) and the 9d1e51b `feat(task-builder): PR-06 structural gate additions (TB-Add-1 through TB-Add-7)` — but these are intra-skill PR numbering, not multi-PR sequences.

### Builder structural recommendation

For this task's PR plan, mirror the CI-rot pattern:

- **Branch naming:** `<type>/<scope>-pr<N>-<slug>` (e.g., `feat/hook-followup-pr1-foo`).
- **Base branch:** `master` for each (NOT stacked).
- **Dependency declaration:** each task frontmatter has `blocks: ["<next-track-id>"]` and `blockedBy: ["<prior-track-id>"]`.
- **AC pattern:** mandate exact branch name, exact PR title, base = master, body structure.

---

## 6. MDTM Template 02 Rules (PART 1)

**Source:** `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md`
**Total length:** ~1000+ lines (PART 1 = orchestrator instructions, PART 2 = task file template)

### Section A — Core Principles (lines 68-128)

| Rule | Summary | Builder action |
|---|---|---|
| **A1** | Check if governing workflow docs exist; if not, use direct user requirements but maintain detail | This task has no specific workflow doc → omit WORKFLOW-DEPENDENT sections (D1, D2, A2, A5, A6) |
| **A2** | [WORKFLOW-DEPENDENT] Extract every requirement from workflow doc | **N/A here** |
| **A3** | **COMPLETE GRANULAR BREAKDOWN** — break every phase into atomic verifiable checkboxes; NO bulk operations; exact file paths, specific requirements, measurable outcomes | Builder must produce per-PR, per-commit, per-CI-check items — NOT "open all PRs" as one item |
| **A4** | **ITERATIVE PROCESS STRUCTURE** — for any multi-item process: enumerate all items first, then individual checklist item per item, then consolidate. Pattern: `Step X.1` enumerate → `Step X.2` per-item → `Step X.3` consolidate | Use this pattern for the PR-creation loop |
| **A5/A6** | [WORKFLOW-DEPENDENT] | **N/A here** |

### Section B — Self-Contained Checklist Items (lines 130-197) — CRITICAL

| Rule | Summary |
|---|---|
| **B1** | Session rollover protection — every item must be self-contained because batch 3+ won't have batch 1's context |
| **B2** | **5-FIELD SELF-CONTAINED PATTERN** every checklist item MUST embed: (1) Context Reference with WHY, (2) Action with WHY, (3) Output Specification (exact path + content + template), (4) Integrated Verification ("ensuring..." clause), (5) Evidence on Failure Only, (6) Explicit Completion Gate ("This item cannot be marked as done until..." closing) |
| **B3** | One full paragraph per item — not multi-line/bulleted; verbose and explanatory |
| **B4** | Correct example provided (lines 156-159) — single 100+ word paragraph |
| **B5** | **FORBIDDEN**: standalone "read context" items; missing context reference; multi-line/bulleted items; separate verification items; overly granular items; REMINDER blocks between items |
| **B6/B7** | Preferential includes + Key principles (one paragraph, complete prompt, embedded verification, output file = evidence) |

**Builder enforcement:** every item the builder produces MUST satisfy all 6 B2 fields in a single paragraph.

### Section L — Intra-Task Handoff Patterns (lines 711-836)

| Pattern | When | Used in this task? |
|---|---|---|
| **L1 Discovery** | Explore codebase/data, produce structured findings file | Phase 1: branch/CI state discovery |
| **L2 Build-from-Discovery** | Create output using prior discovery's findings | Phase 2: build per-PR descriptions |
| **L3 Test/Execute** | Run command/test, capture raw + structured summary | QA phase: run ruff/pytest/verify-sync |
| **L4 Review/QA** | Assess quality of prior output → PASS/FAIL verdict | QA gate |
| **L5 Conditional-Action** | Branch on prior result (handle BOTH success+failure branches) | Fix-cycle loop |
| **L6 Aggregation** | Consolidate multiple outputs via Glob discovery | Final consolidation |

**Handoff dir convention (line 719):** `.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}/`.

### Section M — Phase-Gate Composite Patterns (lines 837-861)

**M1 PHASE-GATE QA SEQUENCE** — 2-3 items inserted between phases:
1. **Item 1 (Aggregation, L6):** Glob-collect outputs from preceding phase.
2. **Item 2 (QA Agent Spawn):** Spawn `rf-qa` with phase type, inputs, output report path, verdict handling, error clause.
3. **Item 3 (Conditional Proceed, L5):** Read QA report — PASS → next phase; FAIL → fix cycle (max cycles per I16).

**M2 PHASE-GATE APPLICABILITY** table — for **task-building tasks**: gates required *"After research phase (research-gate), after task file creation (task-integrity)"*. For **code-modifying tasks**: gates required *"After implementation phase and before testing phase (if testing is separate), or after combined implement+test phase"*.

**Pin for the builder's QA gate selection (BUILD_REQUEST quoted in this RP):**
> *"this task uses FINAL_ONLY (not PER_PHASE) so the M1 pattern may not apply"*

Confirmed by the analogous TASK-RF-track-1 (line 88-89): *"FINAL_ONLY QA gate"* — reviews/ and plans/ subdirs are unused; only `discovery/`, `test-results/`, `reports/` are populated. The single QA gate sits between Phase N (final-execute) and Post-Completion, not between every phase.

### Section I — Additional Guidelines (key items)

| Rule | Pin |
|---|---|
| **I12** | Verification is integrated via "ensuring..." clause — NO separate verify items |
| **I13** | Post-Completion Actions section is the only completion handler |
| **I15** | Phase-gate QA mandatory for tasks with 2+ phases (BUT FINAL_ONLY mode collapses this to one gate) |
| **I16** | Fix-cycle rules: task-integrity gate = max 2 cycles, then unresolved becomes Open Question |
| **I17** | Post-completion validation must verify: all items `[x]`, all output files exist (via Glob), blocker entries have resolution notes, code-modifying tests pass |
| **I18** | Code-modifying tasks MUST include test items (command + pass criteria + results path) |

### TB-Add-1 through TB-Add-8 — Structural Gate Additions

From `.claude/skills/task-builder/SKILL.md:1133-1141`:

| Check | Rule |
|---|---|
| **TB-Add-1** | Placeholder scan — no item contains `TBD`/`TODO`/`FIXME`; no title-only items (5-field schema enforced) |
| **TB-Add-2** | Item count bounds — track ≥3 and ≤40 items; single-track ≥3 and ≤50 (ADVISORY until calibrated) |
| **TB-Add-3** | Clarification adjacency — each blocked item references its blocking Open Question by index in Context |
| **TB-Add-4** | Circular dependency detection — item-to-item dependencies form a DAG; no cycles |
| **TB-Add-5** | Granularity / XL splitting — items flagged complex/multi-file are either split or carry justifying comment |
| **TB-Add-6** | Confidence/Verification format consistency — uniform `Verify: ...` prefix and `- ✅`/`- [x]` AC form |
| **TB-Add-7** | Execution Context source areas reappear in items — every "Source areas:" header entry reappears in ≥1 item's Context; header itself has NO specific file:line references. INACTIVE if no Execution Context block exists |
| **TB-Add-8** | Per-item Context evidence binding — every item Context field referencing a code surface includes file:line OR an `<!-- evidence-absence: ... -->` justified-absence comment (INV-015 scope-confinement) |

**Builder action:** all TB-Add-1 through TB-Add-8 must be evaluable on the produced task file; the rf-qa gate will FAIL any task that violates one.

---

## 7. Analogous Prior Task — TASK-RF-track-1-20260517-032112

**Path:** `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-track-1-20260517-032112/TASK-RF-track-1-20260517-032112.md`

This is the **closest analogue** for the current task: a single-track PR-creation task (PR1 of the 5-PR CI-rot sequence) involving multi-phase git operations (branch creation → execute → commit → PR) with planning artifacts written under `phase-outputs/`.

### Frontmatter (verbatim, lines 1-45)

```yaml
---
id: "TASK-RF-track-1-20260517-032112"
title: "PR1 — ruff auto-fix sweep (F401 unused imports + I001 import order + F841 unused locals)"
description: "Execute the mechanical ruff auto-fix sweep across src/ and tests/ to clear 934 of 1036 master ruff failures (646 F401 + 242 I001 + 46 F841) in a single PR. This is PR1 of a 5-PR CI rot remediation sequence. Pre-existing ruff failures on master have been making post-merge CI untrustworthy (6/8 checks red on every PR). PR1 handles the mechanically auto-fixable rule classes first so subsequent PRs (manual fixes, formatter, config tightening, branch protection) operate on a clean baseline."
status: "🟢 Done"
type: "🔧 Refactor"
priority: "🔼 High"
created_date: "2026-05-17"
updated_date: "2026-05-17"
assigned_to: "rf-implementer"
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_task: ""
depends_on: []
related_docs:
- path: ".dev/tasks/to-do/TASK-RF-track-1-20260517-032112/research-notes.md"
  description: "Research notes for this PR — scope, CI evidence, baseline counts, branch/PR conventions, ambiguities"
- path: "https://github.com/IronbellyOrg/IronClaude/actions/runs/25979540639"
  description: "CI failure run on PR #35 (job 76365604439) — source of the 1036 ruff error baseline and rule-class breakdown"
- path: ".dev/tasks/to-do/TASK-RF-track-1-20260517-032112/research-notes.md"
  description: "Brainstorm decisions (Q2 chose bulk auto-fix strategy) and 5-PR sequence rationale are captured in research-notes.md"
tags:
- "ci-rot"
- "ruff"
- "autofix"
- "pr1"
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"
estimation: ""
sprint: ""
due_date: ""
start_date: "2026-05-17"
completion_date: "2026-05-17"
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: static
blockedBy: []
blocks:
- "TASK-RF-track-2-20260517-032112"
---
```

### First two phases — verbatim structure

**Title + Overview + Key Objectives + Prerequisites (lines 47-119):**

```markdown
# PR1 — ruff auto-fix sweep (F401 + I001 + F841)

## Task Overview

Pre-existing CI rot on master is masking real failures on every PR — the same 1036 ruff errors fail `quick-check.yml` on PRs that don't touch any of the offending files. Per `/sc:brainstorm` Q2 (user-chosen strategy), this is remediated by a 5-PR sequence; this task is **PR1**, the mechanical bulk auto-fix sweep.

The work is intentionally mechanical: run `uv run ruff check src/ tests/ --fix --select F401,I001,F841`, verify the targeted rules report zero violations afterward, confirm the existing test suite still passes (no behavioral regression), then commit on a feature branch and open a PR. No manual code edits, no scope creep into other rule classes, no test additions.

This PR clears **934 of 1036** baseline ruff failures (646 F401 + 242 I001 + 46 F841). The remaining ~102 violations (N806, N811, F811, E741, formatter issues, etc.) are routed to PR2–PR5.

## Key Objectives

The following objectives MUST be achieved by this task:

1. **Clear all auto-fixable lint violations in the F401, I001, and F841 rule classes:** After execution, `uv run ruff check src/ tests/ --select F401,I001,F841` MUST exit 0.
2. **Preserve all existing behavior:** Full test suite (`uv run pytest -v`) MUST pass with the same pass count as the pre-fix baseline (no new failures attributable to the auto-fix).
3. **Preserve the source-of-truth invariant:** `make verify-sync` MUST report `src/superclaude/` and `.claude/` in sync at the end of the task (the auto-fix touches `src/`, so a `make sync-dev` may be required mid-task).
4. **Ship as a single reviewable PR:** Open one PR on branch `fix/ci-rot-pr1-ruff-autofix` against `master` with title `fix(lint): ruff --fix sweep — F401 unused imports + I001 import order + F841 unused locals` and a body that documents scope, rule classes, baseline counts, and the AC checklist from research-notes.md.

## Prerequisites & Dependencies

### Parent Task & Dependencies
- **Parent Task:** None (this is the first task in the 5-PR CI rot remediation sequence)
- **Blocking Dependencies:** None
- **This task blocks:** `TASK-RF-track-2-20260517-032112` (PR2 — manual fixes for N806/N811/F811/E741 — depends on PR1's clean baseline)

### Previous Stage Outputs (MANDATORY INPUTS)

**INFORMATIONAL ONLY - NO CHECKLIST ITEMS HERE**

**Required Previous Stage Outputs:**
- **Research notes:** `.dev/tasks/to-do/TASK-RF-track-1-20260517-032112/research-notes.md` — Purpose: provides the CI evidence baseline (run `25979540639`), rule-class breakdown, affected directories, branch/PR naming convention, the documented scope-vs-AC mismatch resolution (wider scope chosen), and confirmation that F841 is in scope. Embedded into Phase 1 (preparation + baseline) and Phase 2 (execute) items below.

### Handoff File Convention

This task uses intra-task handoff patterns. Items write intermediate outputs to:
**`.dev/tasks/to-do/TASK-RF-track-1-20260517-032112/phase-outputs/`**

Subdirectories:
- `discovery/` — Baseline ruff snapshot (before auto-fix)
- `test-results/` — Post-fix ruff snapshot, pytest output
- `reviews/` — (unused for this task; mechanical work, FINAL_ONLY gate)
- `plans/` — (unused for this task)
- `reports/` — PR body draft, final summary

These files persist across all batches and session rollovers. Later items read them by path.

### Frontmatter Update Protocol

YOU MUST update the frontmatter at these MANDATORY checkpoints:
- **Upon Task Start:** Update `status` to "🟠 Doing" and `start_date` to current date
- **Upon Completion:** Update `status` to "🟢 Done" and `completion_date` to current date
- **If Blocked:** Update `status` to "⚪ Blocked" and populate `blocker_reason`
- **After Each Work Session:** Update `updated_date` to current date

DO NOT modify any other frontmatter fields unless explicitly directed by the user.
```

**Execution Context block + Phase 1 — verbatim (lines 105-149):**

```markdown
## Execution Context

**Acceptance Criteria (from research-notes.md, restated here for execution reference):**

- **AC1:** `uv run ruff check src/ tests/ --select F401,I001,F841` exits 0 after the fix.
- **AC2:** `uv run pytest -v` exits 0 with no new failures vs. the pre-fix baseline.
- **AC3:** `make verify-sync` exits 0 (source-of-truth invariant preserved).
- **AC4:** A PR exists on branch `fix/ci-rot-pr1-ruff-autofix` targeting `master` with the exact title specified in Key Objective 4 and a body matching the structure in Step 4.2.

**Granularity note (documented deviation from MDTM A3):** This task uses phase-level granularity, not per-file granularity. The auto-fix touches ~291 files across 8 directories mechanically — a per-file checklist would be 291 identical items providing zero additional value or safety. Per the BUILD_REQUEST: one Discovery item, one Execute item, multiple Verify items (one per AC), one Commit item, one PR item. This is explicitly authorized for the mechanical-bulk-edit case.

**Open Questions:**

1. **Scope-vs-AC mismatch (resolved, documented per BUILD_REQUEST):** ... [details elided in this RP, see source file]
2. **F841 inclusion:** ... [details elided]

## Detailed Task Instructions

### Phase 1: Preparation and Baseline

YOU MUST complete EVERY item in this checklist IN ORDER. DO NOT skip ahead. Mark each item as complete before proceeding to the next.

**Step 1.1:** Update task status

- [x] Update status to "🟠 Doing" and start_date to today's date (2026-05-17) in the frontmatter of this file, then add a timestamped entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[YYYY-MM-DD HH:MM]** - Task started: Updated status to "🟠 Doing" and start_date.` Once done, mark this item as complete.

**Step 1.2:** Create handoff directories

- [x] Create the phase-outputs directory structure at `.dev/tasks/to-do/TASK-RF-track-1-20260517-032112/phase-outputs/` with subdirectories `discovery/`, `test-results/`, and `reports/` (other subdirectories are not needed — this is a mechanical bulk-fix task with FINAL_ONLY QA gating) to enable intra-task handoff between items, ensuring all directories exist on disk after this step. Use `mkdir -p .dev/tasks/to-do/TASK-RF-track-1-20260517-032112/phase-outputs/{discovery,test-results,reports}` from the repo root `/config/workspace/IronClaude/`. Once done, mark this item as complete.

**Step 1.3:** Create the feature branch

- [x] From the repo root `/config/workspace/IronClaude/`, verify the current branch is `master` (or `integration`) and the working tree is clean with `git status`; if either check fails, stop and log the blocker in the ### Phase 1 - Preparation Findings section of the ## Task Log / Notes at the bottom of this task file (do NOT proceed with a dirty tree because `ruff --fix` would mix with unrelated changes); otherwise create and switch to the feature branch with the exact command `git checkout -b fix/ci-rot-pr1-ruff-autofix`, then verify `git branch --show-current` returns `fix/ci-rot-pr1-ruff-autofix`. Once done, mark this item as complete.

**Step 1.4:** Install dev dependencies so ruff is on PATH

- [x] From the repo root `/config/workspace/IronClaude/`, install the project with dev extras using the exact command `uv pip install --system -e ".[dev]"` (per research-notes.md the local `.venv` is missing ruff and `make dev` or `uv pip install -e ".[dev]"` is required before running ruff locally), then verify ruff is reachable by running `uv run ruff --version` and capturing the version string. If installation fails (e.g., uv not available, network issue), log the blocker in the ### Phase 1 - Preparation Findings section of the ## Task Log / Notes at the bottom of this task file, then stop — do not proceed without ruff. Once installation succeeds and `uv run ruff --version` prints a version, mark this item as complete.

**Step 1.5:** Capture pre-fix ruff baseline (whole-tree, all rules)

- [x] From the repo root `/config/workspace/IronClaude/`, run `uv run ruff check src/ tests/ --statistics 2>&1` and write the full output to `.dev/tasks/to-do/TASK-RF-track-1-20260517-032112/phase-outputs/discovery/baseline-ruff-all.txt`, then run `uv run ruff check src/ tests/ --select F401,I001,F841 --statistics 2>&1` and write the full output to `.dev/tasks/to-do/TASK-RF-track-1-20260517-032112/phase-outputs/discovery/baseline-ruff-target.txt`, then create a summary file `.dev/tasks/to-do/TASK-RF-track-1-20260517-032112/phase-outputs/discovery/baseline-summary.md` containing: the total error count from `baseline-ruff-all.txt`, the per-rule breakdown for F401/I001/F841 from `baseline-ruff-target.txt`, and an explicit comparison against the research-notes.md expected baseline (1036 total, 646 F401, 242 I001, 46 F841). If the actual counts differ from the expected baseline by more than ±5%, log a notice in the ### Phase 1 - Preparation Findings section of the ## Task Log / Notes at the bottom of this task file (do NOT stop — proceed with the actual counts; the divergence may simply reflect interim merges) and reference the actual counts in the PR body in Step 4.2. Once both raw output files and the summary file exist on disk, mark this item as complete.

**Step 1.6:** Capture pre-fix pytest baseline

- [x] From the repo root `/config/workspace/IronClaude/`, run `uv run pytest -v --tb=short 2>&1` and write the full output to `.dev/tasks/to-do/TASK-RF-track-1-20260517-032112/phase-outputs/discovery/baseline-pytest.txt`, then extract the pass/fail/error/skipped counts from the final summary line (e.g., `===== N passed, M failed, K skipped in T.Ts =====`) and append a single line at the top of the file in the format `BASELINE: N passed, M failed, K skipped`. This baseline is the comparison reference for AC2 — the post-fix pytest run must show the same pass count and no new failures attributable to the auto-fix. If pytest itself fails to start (collection error not caused by lint), log the blocker in the ### Phase 1 - Preparation Findings section of the ## Task Log / Notes at the bottom of this task file and stop. Once the baseline file exists with the summary line, mark this item as complete.

### Phase 2: Execute Auto-Fix
```

### Mirror-this patterns the builder must follow

| Pattern | Source line(s) | Builder use |
|---|---|---|
| `id` follows `TASK-RF-track-N-YYYYMMDD-HHMMSS` for multi-PR; or `TASK-RF-YYYYMMDD-HHMMSS` for single | line 2 | Builder picks scheme based on PR-count |
| `title` is the **commit-message-shape** PR title (`type(scope): subject`) | line 3 | Builder copies the conventional-commit pattern |
| `description` is a paragraph explaining the PR and its sequence position | line 4 | Pin the PR-of-N context in description |
| `assigned_to: "rf-implementer"` (default) | line 11 | |
| `coordinator: orchestrator` | line 14 | |
| `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"` | line 28 | Mandatory |
| `task_type: static` (this task is static; no dynamic discovery) | line 43 | |
| `blockedBy: []` + `blocks: [next-track-id]` outside the main `depends_on:` block | lines 42-44 | Used to express multi-PR DAG |
| Key Objectives are 4 numbered objectives, last one always "Ship as a single reviewable PR with branch=X, title=Y, body=Z" | lines 60-64 | **Replicate verbatim shape for the PR plan** |
| Acceptance Criteria block named `AC1..AC4` in `## Execution Context` | lines 107-111 | |
| **AC4 always names branch + base + title + body structure** | line 111 | Builder MUST do the same |
| Granularity-deviation note when phase-level not per-file | line 113 | Use when applicable |
| Open Questions are numbered + resolution-documented | lines 115-118 | |
| Phase 1 always begins with: Step 1.1 status update → 1.2 dir creation → 1.3 branch creation → 1.4 dep install → 1.5/1.6 baseline capture | lines 122-148 | **Mirror this 6-step Phase 1 boilerplate** |

---

## 8. Builder Hand-Off Summary

### What the builder must produce (synthesizing R4 findings)

1. **Task file using MDTM Template 02** (`02_mdtm_template_complex_task.md`).
2. **Frontmatter** in the exact shape of TASK-RF-track-1 (see §7 above) — `id`, `title`, `description`, `template_schema_doc`, `task_type: static`, `blockedBy`/`blocks` for multi-PR DAG.
3. **B2 self-contained checklist items** (6-field paragraph each) — no items violate B5 forbidden patterns.
4. **Phase 1 boilerplate** mirroring TASK-RF-track-1 §7 — status update, dir creation, branch creation, dep install, baselines.
5. **QA phase using FINAL_ONLY** (single M1 gate after final execute phase, NOT per-phase) — confirmed by BUILD_REQUEST.
6. **TB-Add-1..8 compliance** — task file must pass all 8 structural checks (rf-qa will enforce).
7. **PR descriptions per PR** mirroring **PR #49 actual body style** (Summary → Changes table → Test plan → Open Questions → Acceptance Criteria → footer with `🤖 Generated with [Claude Code]`), NOT the template's checkbox style. Use PR template as fallback only for trivial PRs.
8. **Branch naming** following CI-rot precedent: `<type>/<scope>-pr<N>-<slug>` where type matches conventional-commit type. Each branch cut from latest `master`, not stacked.
9. **CI commands** as separate self-contained items in QA phase: `uv run ruff check src/ tests/`, `uv run pytest tests/<changed-area>/ -v`, `make verify-sync` (per CONTRIBUTING `:30-36`), plus `make sync-dev` immediately before `make verify-sync` if `src/superclaude/{skills,agents,commands}` was touched.
10. **Rot-budget check** as explicit QA item — compare branch CI vs master baseline.

### Cross-references to other researchers

- **R1 file inventory** — feeds the per-PR file-grouping decision.
- **R2 conventions** — Conventional Commits (PR template line 22) cross-confirms R2's commit-message rules.
- **R3 integration** — `make sync-dev` + `make verify-sync` are integration touchpoints.
- **R5 data flow** — phase-outputs handoff convention is data-flow infra.
- **R6 test QA** — the L3 test-execute pattern + rot-budget rule are QA-phase inputs.
- **R7 web** — external multi-PR-split best practices; this R4 covers internal precedent only.

---

## Status: Complete

All 7 investigation items addressed:
- ✅ §1 PR template verbatim with section inventory + deviation note
- ✅ §2 CONTRIBUTING.md verbatim with extracted rules
- ✅ §3 CI workflows listed with required-status-check identification
- ✅ §4 .github/ other files (CODEOWNERS/ISSUE_TEMPLATE absent — documented)
- ✅ §5 Prior multi-PR split = CI-rot 5-PR sequence (PRs #37-#41); patterns extracted
- ✅ §6 MDTM Template 02 rules A1-A4, B2, L1-L6, M1, I12-I18, TB-Add-1..8 all documented
- ✅ §7 Closest analogue TASK-RF-track-1 frontmatter + first 2 phases pasted verbatim

Plus §0 critical finding: PR #49 on this exact branch is **already merged** — the builder's PR plan must reflect post-merge follow-up, not initial PR.
