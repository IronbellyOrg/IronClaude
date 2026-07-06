# Research: Template and PR Discipline
**Topic type:** Template & Examples
**Scope:** Template 02 PART 1, project CLAUDE.md PR/staging discipline, validation command set, sibling task model
**Status:** Complete
**Date:** 2026-06-04
---

## 1. Canonical Template 02 requirements to encode

### 1.1 Canonical source-of-truth and frontmatter

Use `/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` as the template source of truth. The template itself says Template 02 is for complex tasks requiring "discovery, testing, review, conditional logic, or aggregation between checklist items" (`/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:60-64`).

Required frontmatter fields visible in the template are: `id`, `title`, `description`, `status`, `type`, `priority`, `created_date`, `updated_date`, `assigned_to`, `autogen`, `autogen_method`, `coordinator`, `parent_task`, `depends_on`, `related_docs`, `tags`, `template_schema_doc`, `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings`, `review_info.last_reviewed_by`, `review_info.last_review_date`, `review_info.next_review_date`, and `task_type` (`/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:1-44`). For OQ-1 Opt-2a, set `type: "🐛 Bug Fix"`, `priority: "🔼 High"`, `task_type: static`, and `template_schema_doc: "src/superclaude/templates/workflow/02_mdtm_template_complex_task.md"`.

### 1.2 Mandatory sections and no-pre-Phase-1 checkboxes

Part 1 requires mandatory task sections and forbids actionable items before Phase 1: "NO CHECKLIST ITEMS may appear before Phase 1 begins" (`/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:269-273`). The generated task should therefore keep overview/prerequisites/previous-stage outputs/handoff convention/frontmatter protocol informational, then put all executable work under `## Detailed Task Instructions` phases.

### 1.3 B2 self-contained item pattern

B2 is the key checklist-item contract. Every checklist item must include: "Context Reference with WHY", "Action with WHY", "Output Specification", "Integrated Verification", "Evidence on Failure Only", and "Explicit Completion Gate" (`/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:142-149`). B3 further requires each item to be "ONE FULL PARAGRAPH" executable independently across session rollover (`/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:150-153`). B5 forbids standalone read-context items, missing source-of-truth context, multi-line/bulleted checklist items, separate verification items, and separate reminder blocks (`/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:164-184`).

Builder implication: each OQ-1 checklist item should be a single paragraph that embeds exact context reads, exact action, output path under `phase-outputs/`, an `ensuring...` clause, blocker logging, and the literal closeout gate "Once done, mark this item as complete." Do not create separate verification-only checkboxes for compile/test/lint evidence when they can be integrated into the action item; command/test items are valid when they produce captured output.

### 1.4 Rule A3 and granular bug-fix item breakdown

A3 requires atomic granularity: "Break down EVERY workflow phase into atomic, verifiable checklist items", "Create individual checklist items for EVERY file, component, or iteration", and "NO high-level or bulk operations allowed" (`/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:91-96`). A4 adds that multi-item work must pre-enumerate items, create individual checklist items for each item, require incremental updates, and only consolidate after all items complete (`/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:97-116`).

Builder implication: Phase 2 should discover/pin the exact current Signal B lines/predicates first, then Phase 3 should edit the Opt-2a recovered-tail exemption as its own precise source item. Do not write a bulk item like "fix integrity.py" if the work can be split into locate, edit, RED/GREEN test, validation, QA, and PR phases.

### 1.5 Phase-gate QA pattern

Worker-agent rules prohibit skipping phase-gate QA: agents must not proceed across dependent phases without passing QA (`/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:405-412`). I15 requires a phase-gate QA checkpoint for tasks with 2+ phases and defines it as aggregation, QA-agent spawn, and conditional proceed/fix-cycle (`/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:599-607`). I16 requires binary PASS/FAIL verdicts, says any severity causes FAIL, and gives `task-integrity` max 2 fix cycles (`/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:609-624`). M1 repeats the phase-gate sequence: aggregation, rf-qa spawn, conditional proceed/fix-cycle (`/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:843-850`).

For OQ-1 Opt-2a, include a final Phase Gate before commit/push/PR: spawn `rf-qa` with `QA_MODE: task-integrity`, `fix_authorization: true`, and adversarial stance to verify source edit, tests, validation artifacts, fork PR discipline, `.claude/` staging prohibition, and `python -m` prohibition. The gate should write a report under `phase-outputs/reviews/`, require `VERDICT: PASS` before Phase 6, and rerun affected validations for every fix.

### 1.6 Anti-orphaning and completion items

Completion work belongs at the end. C4 says task completion is handled by final post-completion task items for frontmatter updates and execution-log completion, and says not to create a separate completion/handoff section (`/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:225-230`). I13 repeats that every task must include post-completion actions and must not create a separate "Task Completion and Handoff Protocol" section (`/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:580-585`). I17 requires pre-Done checks for all checkboxes complete, output files present, blocker resolution notes, and tests passing for source modifications (`/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:626-633`).

Builder implication: put final artifact checks, final QA verdict reread, task summary, execution-log entry, `status: "🟢 Done"`, `completion_date`, and `updated_date` in Phase 6 or a final closeout phase. Do not leave them as orphaned floating instructions after the task log.

---

## 2. Fork PR, `.claude/`, UV, and worktree discipline from CLAUDE.md

### 2.1 Fork target discipline, verbatim

The task must embed the fork-only PR rule from `/config/workspace/IronClaude/CLAUDE.md`:

> "This repository is a **fork**. `origin` = `IronbellyOrg/IronClaude` (the user's private fork). `upstream` = `SuperClaude-Org/SuperClaude_Framework` (the public parent)." (`/config/workspace/IronClaude/CLAUDE.md:35-38`)

Forbidden operations to encode:

> "Run a bare `gh pr create` without `--repo IronbellyOrg/IronClaude`. The GitHub CLI defaults `gh pr create` to the **parent repo of a fork**, which means PRs silently land on the public upstream — exposing private fork work and misrouting reviews." (`/config/workspace/IronClaude/CLAUDE.md:39-42`)
>
> "Open PRs against `SuperClaude-Org/SuperClaude_Framework` without explicit user authorization in the same session. Treat that target as forbidden." (`/config/workspace/IronClaude/CLAUDE.md:42-43`)
>
> "Push to `upstream` (the `upstream` remote name above). The `origin` remote is the correct push target." (`/config/workspace/IronClaude/CLAUDE.md:43-44`)
>
> "Assume the upstream is the right target because gh's interactive flow suggests it. The interactive flow is the trap." (`/config/workspace/IronClaude/CLAUDE.md:44-44`)

Mandatory command shape:

```bash
gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "..." --body "..."
```

Source: `/config/workspace/IronClaude/CLAUDE.md:46-50`.

### 2.2 Mandatory pre-PR checks and branch base

Pre-PR checks from CLAUDE.md must be encoded as task items:

1. `git remote -v` — confirm `origin` = `IronbellyOrg/IronClaude.git` (`/config/workspace/IronClaude/CLAUDE.md:52-55`).
2. `git fetch origin && git log master..origin/master` — if the fork master is ahead, rebase the branch onto `origin/master` before pushing (`/config/workspace/IronClaude/CLAUDE.md:54-56`).
3. After PR creation, verify the URL points at `https://github.com/IronbellyOrg/IronClaude/pull/N`, not `SuperClaude-Org`; if wrong, close/reopen with `--repo IronbellyOrg/IronClaude` (`/config/workspace/IronClaude/CLAUDE.md:56-56`).

Because the user explicitly requires a NEW branch off `origin/master`, Phase 1 should run `git fetch origin` and create the isolated branch/worktree from `origin/master`; Phase 6 should push only to `origin` and then create the PR with `--repo IronbellyOrg/IronClaude --base master --head <branch>`.

### 2.3 `.claude/` staging prohibition, verbatim

The task must include the `.claude/` staging prohibition, even if OQ-1 should only touch `src/` and `tests/`:

> "`.claude/{skills,commands,agents,hooks,templates}/*` is **gitignored sync-dev output** of `src/superclaude/`. The ONLY tracked file under `.claude/` is `.claude/settings.json`" (`/config/workspace/IronClaude/CLAUDE.md:16-19`)
>
> "`git add .claude/skills/...`, `.claude/commands/...`, `.claude/agents/...`, `.claude/hooks/...`, `.claude/templates/...`"; "`git add -f` on any `.claude/` path"; "Suggest staging `.claude/` mirrors in paste-ready commit commands"; and "Author task-file instructions, follow-ups, or risk notes telling the user to stage `.claude/` paths" are all listed under **NEVER** (`/config/workspace/IronClaude/CLAUDE.md:20-25`).
>
> "If `git add` requires `-f` on any `.claude/` path, that `-f` is the violation siren. STOP. Move the change to `src/superclaude/` first, run `make sync-dev`, and stage only the `src/` side." (`/config/workspace/IronClaude/CLAUDE.md:27-27`)
>
> "Exceptions: ONLY `.claude/settings.json`." (`/config/workspace/IronClaude/CLAUDE.md:29-29`)

Commit/staging item should run `git status --porcelain`, stage only exact allowed source/test files, run `git diff --cached --name-only`, reject any staged `.claude/` path except `.claude/settings.json`, and never use `git add -f` for `.claude/`.

### 2.4 Worktree guidance for current dirty primary checkout

CLAUDE.md says parallel sessions should use `git worktree` to avoid conflicts and lists independent working directories and no branch-switching conflicts as benefits (`/config/workspace/IronClaude/CLAUDE.md:256-286`). The session's current primary checkout is dirty per the supplied git status, so the task should explicitly avoid stash/reset/checkout in `/config/workspace/IronClaude` and do all implementation, validation, commit, push, and PR work inside a new worktree path under `.dev/worktrees/` or a similarly isolated task-local worktree.

### 2.5 UV-only and `python -m` prohibition

CLAUDE.md line 7 is explicit: "Never use `python -m`, `pip install`, or `python script.py` directly" (`/config/workspace/IronClaude/CLAUDE.md:5-8`). Required command examples use UV for tests and execution (`/config/workspace/IronClaude/CLAUDE.md:62-70`). Therefore compile checks must NOT use `uv run python -m py_compile`. Use the compliant one-liner form:

```bash
uv run python -c "import py_compile; py_compile.compile('<path>', doraise=True)"
```

or rely on pytest import/collection where appropriate. The sibling gap-fill research corrected the same mistake: "NEVER `python -m py_compile`" and recommends `uv run python -c "import py_compile; py_compile.compile(..., doraise=True)"` (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/research/04-gate-resolutions.md:12-23`).

---

## 3. Validation command set to encode

### 3.1 Required commands

For OQ-1 Opt-2a, encode these validation commands as task items, run from the isolated worktree root unless a task item explicitly says otherwise:

- Python syntax/import pre-check for edited Python files, using only the compliant `python -c` shape: `uv run python -c "import py_compile; py_compile.compile('<path>', doraise=True)"`. If multiple files are edited, compile them in one single-line `python -c` command by repeating `py_compile.compile(...)`. This mirrors the sibling task's python-m-free source and test compile items (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:156-158`, `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:170-172`).
- `uv run pytest tests/sprint/ -q` for the full sprint validation surface, as required by the user and modeled by the sibling task (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:176-178`).
- `uv run ruff check src/ tests/` as the explicit lint gate (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:180-182`).
- `uv run ruff format --check src/ tests/` as the separate format gate (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:184-186`).

### 3.2 `make lint` is not enough

Memory `reference_make_lint_vs_ci_ruff_format.md` says `make lint` only runs `uv run ruff check .` and "does **NOT** run `ruff format --check`"; it explicitly says to run `uv run ruff format --check src/ tests/` before pushing Python changes (`/config/.claude/projects/-config-workspace-IronClaude/memory/reference_make_lint_vs_ci_ruff_format.md:10-14`). Therefore the task must treat `uv run ruff check src/ tests/` and `uv run ruff format --check src/ tests/` as separate required gates; do not substitute `make lint` for either gate.

### 3.3 Baseline failure attribution

The task should allow attribution to exactly one documented pre-existing baseline node if the full sprint suite fails: `tests/sprint/test_e2e_success.py::test_jsonl_events_for_each_phase`. The sibling task encodes the same rule in its full-sprint pytest item: the suite must either pass cleanly or fail only that documented baseline node, while any other failure is owned by the task and must be fixed before proceeding (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:176-178`).

### 3.4 Capture artifacts for QA and PR review

Template 02 L3 says command/test items should capture both raw output and a structured summary; raw output preserves full detail and the summary supports later assessment (`/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:761-771`). The OQ-1 task should write raw command outputs to `phase-outputs/test-results/`, write concise summaries next to them, and aggregate final validation into `phase-outputs/reports/validation-report.md` before the final rf-qa gate.

---

## 4. Structural model from sibling task TASK-RF-20260604-102137

The sibling task is a close model because it is also a high-priority sprint bug-fix task landing on a new branch with fork PR discipline. Its frontmatter uses `type: "🐛 Bug Fix"`, `priority: "🔼 High"`, related research/QA docs, `template_schema_doc: "src/superclaude/templates/workflow/02_mdtm_template_complex_task.md"`, `template: "02"`, and `task_type: static` (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:1-53`). Its overview scopes the bug, names source/test/validation/PR objectives, and requires a new branch off `origin/master` with fork PR (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:57-70`).

Reusable structural features:

- Handoff file convention: the task uses `phase-outputs/` with `discovery/`, `test-results/`, `reviews/`, `plans/`, and `reports/` subdirectories, and says these persist across batches/session rollovers (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:92-99`).
- Frontmatter update protocol: task start sets `status` to `"🟠 Doing"`, `start_date`, and `updated_date`; completion sets `"🟢 Done"` and `completion_date`; blocked state uses `"⚪ Blocked"` and `blocker_reason` (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:96-99`).
- Phase 1 creates persistent handoff directories, verifies remotes without disturbing the dirty primary checkout, then creates a branch worktree from `origin/master` (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:114-126`).
- Phase 2 discovery reads research and worktree source/test files to produce current source/test inventories before editing, then runs a discovery QA gate before source edits (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:128-140`).
- Phase 3 applies source fixes per site and runs python-m-free compile checks (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:142-158`).
- Phase 4 adds RED→GREEN regression tests and runs python-m-free compile checks for edited tests (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:160-172`).
- Phase 5 runs full sprint pytest, explicit ruff check, explicit ruff format check, aggregates validation evidence, and runs final adversarial `rf-qa` task-integrity before commit (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:174-194`).
- Phase 6 stages only allowed source/test files, commits, pushes to origin, creates the fork PR with mandatory `--repo IronbellyOrg/IronClaude`, and verifies the returned URL owner (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:196-212`).
- Final closeout verifies artifacts, confirms checklist/blocker/QA state, writes task summary, and updates frontmatter to Done (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:214-226`).

The sibling compile items are the exact python-m-free shape to mirror: source compile uses `uv run python -c "import py_compile; py_compile.compile('src/...', doraise=True); ..."` and explicitly ensures no `python -m` command is used (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:156-158`); test compile does the same for edited test files (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-102137/TASK-RF-20260604-102137.md:170-172`).

---

## 5. Recommended phasing for OQ-1 Opt-2a Signal B recovered-tail exemption

Recommended Template 02 phase plan:

1. **Phase 1: Setup, status update, and isolated origin/master worktree.** Update the task frontmatter to Doing, create `phase-outputs/` subdirectories, verify remotes, fetch origin, and create a new branch/worktree off `origin/master`. Do not stash, reset, checkout, or otherwise disturb the dirty primary checkout.
2. **Phase 2: Locate exact Signal B lines (discovery).** Read researcher-1 source findings, researcher-2 test findings, and current worktree `integrity.py`/test files to locate exact Signal B recovered-tail logic by stable text/symbol, not stale line numbers. Write `phase-outputs/discovery/source-site-inventory.md` and `phase-outputs/discovery/test-site-inventory.md`, then optionally run a discovery QA gate if the builder wants per-phase QA.
3. **Phase 3: Apply the Opt-2a edit.** Modify only the verified Signal B recovered-tail exemption in the worktree, preserving unrelated integrity behavior. Run python-m-free compile pre-checks for edited source/tests using `uv run python -c "import py_compile; ..."` or rely on targeted pytest import proof where simpler.
4. **Phase 4: RED→GREEN test.** Add/adjust focused tests from researcher-2's test surface. Capture RED evidence against old behavior, then restore the Opt-2a fix and capture GREEN evidence. Write raw outputs and summaries under `phase-outputs/test-results/`.
5. **Phase 5: Full validation.** Run `uv run pytest tests/sprint/ -q`, `uv run ruff check src/ tests/`, and `uv run ruff format --check src/ tests/`. Attribute only `tests/sprint/test_e2e_success.py::test_jsonl_events_for_each_phase` to pre-existing baseline if it appears; investigate/fix any other failure.
6. **Phase Gate: adversarial rf-qa task-integrity.** Aggregate discovery/test/validation artifacts, spawn `rf-qa` with `QA_MODE: task-integrity`, `fix_authorization: true`, and adversarial stance, and require PASS before git operations. On FAIL, fix all findings regardless of severity, rerun affected validations, and re-run QA up to the template's `task-integrity` max 2 cycles.
7. **Phase 6: Commit, push, and fork PR.** Inspect diff, stage only allowed `src/`/`tests/` files, reject `.claude/` staging, commit on the new branch, push to `origin`, create the PR with `gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch>`, and verify the URL owner.
8. **Final closeout inside the final phase.** Verify required artifacts exist, confirm checklist/blocker/QA state, summarize the work and validation outcomes, update `status` to `"🟢 Done"`, set `completion_date`, and update the task log. This satisfies anti-orphaning.

---

## Summary

- Template 02 canonical source is `/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`; use Template 02 because OQ-1 requires discovery, source edit, testing, QA, validation, and PR handoff.
- Required task-file properties: full frontmatter, no checkboxes before Phase 1, B2 one-paragraph self-contained items with context/action/output/verification/completion gate, A3 granular per-file/per-site breakdown, phase-gate QA, and final-phase anti-orphaning closeout.
- Fork PR discipline is mandatory: `origin` is `IronbellyOrg/IronClaude`, `upstream`/`SuperClaude-Org` is forbidden, PR creation must use `gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch>`, and returned URL must be verified.
- `.claude/` staging is forbidden except `.claude/settings.json`; `git add -f` for `.claude/` is the violation siren.
- Validation command set: python-m-free `uv run python -c "import py_compile; py_compile.compile('<path>', doraise=True)"` if explicit compile checks are used, `uv run pytest tests/sprint/ -q`, `uv run ruff check src/ tests/`, and `uv run ruff format --check src/ tests/`.
- Mirror the sibling task's phase structure: setup/worktree, discovery, edit, RED→GREEN tests, full validation, adversarial rf-qa gate, commit/push/fork PR, final closeout.
