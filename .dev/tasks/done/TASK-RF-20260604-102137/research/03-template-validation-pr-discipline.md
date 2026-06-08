# Template Validation and PR Discipline Research

- Topic: Template & Examples
- Status: Complete
- Date: 2026-06-04

---

## 1. Template 02 Part 1 requirements to encode

### 1.1 Required frontmatter fields

Template 02's frontmatter defines these fields and should be mirrored for the new high-priority bug-fix MDTM task: `id`, `title`, `description`, `status`, `type`, `priority`, `created_date`, `updated_date`, `assigned_to`, `autogen`, `autogen_method`, `coordinator`, `parent_task`, `depends_on`, `related_docs`, `tags`, `template_schema_doc`, `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings`, `review_info.last_reviewed_by`, `review_info.last_review_date`, `review_info.next_review_date`, and `task_type` (`.claude/templates/workflow/02_mdtm_template_complex_task.md:1-44`). For this task, use `type: "🐛 Bug Fix"`, `priority: "🔼 High"`, `task_type: static` unless the task-builder intentionally adds dynamic markers, and include research/source/validation docs under `related_docs`.

### 1.2 Mandatory task sections and output structure

Part 1 states that every task must include mandatory sections and that no actionable checklist items may appear before Phase 1: "NO CHECKLIST ITEMS may appear before Phase 1 begins" (`.claude/templates/workflow/02_mdtm_template_complex_task.md:269-273`). Template Part 2's task body structure includes: task title, `## Task Overview`, `## Key Objectives`, `## Prerequisites & Dependencies`, `### Parent Task & Dependencies`, `### Previous Stage Outputs (MANDATORY INPUTS)`, `### Handoff File Convention`, `### Frontmatter Update Protocol`, `## Detailed Task Instructions`, phased execution sections, `### Phase Gate: Quality Verification`, testing/verification phases, `## Post-Completion Actions`, and `## Task Log / Notes` with summary/execution/finding subsections (`.claude/templates/workflow/02_mdtm_template_complex_task.md:890-1197`).

For a code-modifying bug-fix task, also include the required testing checklist item because Part 1 says source-code modifications must specify the test command, pass criteria, result-capture location, and B2 pattern compliance (`.claude/templates/workflow/02_mdtm_template_complex_task.md:637-646`).

### 1.3 B2 self-contained checklist item pattern

B2 is mandatory. Every checklist item must be a complete, self-contained prompt containing six elements: (1) "Context Reference with WHY", (2) "Action with WHY", (3) "Output Specification", (4) "Integrated Verification", (5) "Evidence on Failure Only", and (6) "Explicit Completion Gate" (`.claude/templates/workflow/02_mdtm_template_complex_task.md:142-149`). B3 further requires each item to be "ONE FULL PARAGRAPH" that can execute independently across session rollovers (`.claude/templates/workflow/02_mdtm_template_complex_task.md:150-153`). B5 forbids standalone read-context items, missing source-of-truth context, multi-line/bulleted checklist items, separate verification items, and separate reminder blocks (`.claude/templates/workflow/02_mdtm_template_complex_task.md:164-184`).

The task-builder should therefore write every actionable item in the bug-fix task as a single paragraph with embedded reads, exact action, output artifact path under the task's `phase-outputs/`, an `ensuring...` verification clause, blocker logging instructions, and the literal completion gate "Once done, mark this item as complete." Do not add separate "verify this item" checkboxes.

### 1.4 Rule A3: granular per-file/per-site items

Rule A3 requires complete granular breakdown: "Break down EVERY workflow phase into atomic, verifiable checklist items," "Create individual checklist items for EVERY file, component, or iteration," and "NO high-level or bulk operations allowed" (`.claude/templates/workflow/02_mdtm_template_complex_task.md:91-96`). For this PASS_RECOVERED follow-up, Phase 3 must therefore be split by exact source site, not by broad file family; each target predicate or call site gets its own B2 item. Phase 2 should locate exact current lines/predicates first because the user's stated bug-fix may land on a new branch off `origin/master` and line numbers may drift.

### 1.5 Phase-gate QA pattern

Part 1 prohibits skipping phase-gate QA: worker agents must not proceed across dependent phases without a passing QA gate (`.claude/templates/workflow/02_mdtm_template_complex_task.md:405-412`). I15 requires at least one phase-gate checkpoint for tasks with 2+ execution phases, consisting of aggregation, QA-agent spawn, and conditional proceed/fix-cycle items (`.claude/templates/workflow/02_mdtm_template_complex_task.md:599-607`). I16 defines binary PASS/FAIL verdicts and max fix cycles, including `task-integrity` max 2 cycles (`.claude/templates/workflow/02_mdtm_template_complex_task.md:609-624`). M1 restates the composite pattern: aggregation, rf-qa spawn, then conditional proceed/fix-cycle (`.claude/templates/workflow/02_mdtm_template_complex_task.md:843-850`).

For this bug-fix task, include a Phase Gate after implementation/test evidence and before commit/push/PR. Use `rf-qa` in `task-integrity` mode with adversarial stance and `fix_authorization: true`, and require a report under `phase-outputs/reviews/`. Encode the conditional item: PASS proceeds; FAIL fixes findings, re-runs affected `py_compile`/pytest/ruff, and re-spawns QA up to 2 cycles.

### 1.6 Anti-orphaning rule: completion items stay in the final phase/post-completion area

Part 1's completion rules say task completion is handled by final Post-Completion items only: include frontmatter updates and execution-log completion there, and do not create a separate "Task Completion and Handoff Protocol" section (`.claude/templates/workflow/02_mdtm_template_complex_task.md:225-230`, `.claude/templates/workflow/02_mdtm_template_complex_task.md:580-585`). I17 also requires post-completion validation items before setting status to Done: verify no unchecked items, expected outputs exist, blockers have resolutions, and relevant tests pass for source modifications (`.claude/templates/workflow/02_mdtm_template_complex_task.md:626-633`).

To avoid orphaned closeout work, keep all task-summary, output-existence, validation-verdict, frontmatter `status: "🟢 Done"`, `completion_date`, and execution-log completion items inside `## Post-Completion Actions` or the final phase, not as separate floating sections earlier in the file.

---

## 2. Fork PR and staging discipline from CLAUDE.md

### 2.1 Fork target discipline, verbatim

The new task must quote/enforce this repository target discipline from `/config/workspace/IronClaude/CLAUDE.md`:

> "This repository is a **fork**. `origin` = `IronbellyOrg/IronClaude` (the user's private fork). `upstream` = `SuperClaude-Org/SuperClaude_Framework` (the public parent)." (`/config/workspace/IronClaude/CLAUDE.md:35-38`)

It must also encode the forbidden operations verbatim:

> "Run a bare `gh pr create` without `--repo IronbellyOrg/IronClaude`. The GitHub CLI defaults `gh pr create` to the **parent repo of a fork**, which means PRs silently land on the public upstream — exposing private fork work and misrouting reviews." (`/config/workspace/IronClaude/CLAUDE.md:39-42`)
>
> "Open PRs against `SuperClaude-Org/SuperClaude_Framework` without explicit user authorization in the same session. Treat that target as forbidden." (`/config/workspace/IronClaude/CLAUDE.md:42-43`)
>
> "Push to `upstream` (the `upstream` remote name above). The `origin` remote is the correct push target." (`/config/workspace/IronClaude/CLAUDE.md:43-44`)
>
> "Assume the upstream is the right target because gh's interactive flow suggests it. The interactive flow is the trap." (`/config/workspace/IronClaude/CLAUDE.md:44-44`)

Mandatory PR creation command shape, verbatim:

```bash
gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "..." --body "..."
```

Source: `/config/workspace/IronClaude/CLAUDE.md:46-50`.

### 2.2 Mandatory pre-PR checks

The task must encode the three pre-PR checks exactly as required:

1. `git remote -v` — confirm `origin` = `IronbellyOrg/IronClaude.git` (`/config/workspace/IronClaude/CLAUDE.md:52-55`).
2. `git fetch origin && git log master..origin/master` — if fork master is ahead, **rebase the branch onto `origin/master`** before pushing (`/config/workspace/IronClaude/CLAUDE.md:54-56`).
3. After PR creation, verify the URL points to `https://github.com/IronbellyOrg/IronClaude/pull/N`, not `SuperClaude-Org`; if wrong, close and reopen with `--repo IronbellyOrg/IronClaude` (`/config/workspace/IronClaude/CLAUDE.md:56-56`).

Because the current goal says the task must land on a NEW branch off `origin/master` with its own fork PR, Phase 1 should fetch `origin`, create an isolated worktree/branch from `origin/master`, and Phase 6 should push that new branch to `origin` and create the PR with the mandatory `--repo IronbellyOrg/IronClaude --base master --head <branch>` shape.

### 2.3 `.claude/` staging prohibition, verbatim

The task must include the `.claude/` staging prohibition even though this bug-fix should not touch `.claude/` mirrors:

> "`.claude/{skills,commands,agents,hooks,templates}/*` is **gitignored sync-dev output** of `src/superclaude/`. The ONLY tracked file under `.claude/` is `.claude/settings.json`" (`/config/workspace/IronClaude/CLAUDE.md:16-19`).
>
> "NEVER", including: "`git add .claude/skills/...`, `.claude/commands/...`, `.claude/agents/...`, `.claude/hooks/...`, `.claude/templates/...`"; "`git add -f` on any `.claude/` path"; and "Suggest staging `.claude/` mirrors in paste-ready commit commands" (`/config/workspace/IronClaude/CLAUDE.md:20-25`).
>
> "If `git add` requires `-f` on any `.claude/` path, that `-f` is the violation siren. STOP. Move the change to `src/superclaude/` first, run `make sync-dev`, and stage only the `src/` side." (`/config/workspace/IronClaude/CLAUDE.md:27-27`).
>
> "Exceptions: ONLY `.claude/settings.json`." (`/config/workspace/IronClaude/CLAUDE.md:29-29`).

Commit/push items should explicitly stage only the edited `src/` and `tests/` files and must include a `git status --porcelain` check that rejects any staged `.claude/` path except `.claude/settings.json`.

### 2.4 Worktree guidance and dirty-tree awareness

`CLAUDE.md` explicitly says parallel sessions should use `git worktree` to avoid conflicts, with benefits including independent working directories and no branch switching conflicts (`/config/workspace/IronClaude/CLAUDE.md:256-286`). The existing PR #124 task model also warns that the master working tree may be dirty and must not be disturbed; it routes all git operations to an isolated worktree (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:56-57`, `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:137-139`).

For this new task, Phase 1 should explicitly create a new isolated worktree/branch off `origin/master`, operate only inside that worktree, and never stash/reset/checkout over the primary checkout's unrelated changes.

---

## 3. Exact validation command set and baseline attribution

### 3.1 Commands the task must encode

The task must include these validation commands exactly, with the worktree's repository root as the command working directory where appropriate:

- `uv run python -m py_compile <file>` for every edited Python source/test file. The prior research lists this as the per-file compile pattern (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/research/03-validation-and-test-surface.md:249-253`), and the example task encodes concrete compile items for edited files (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:181-191`, `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:216-238`, `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:252-254`).
- `uv run pytest tests/sprint/ -q` for the full sprint test surface (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/research/03-validation-and-test-surface.md:242-247`).
- `uv run ruff check src/ tests/` as the CI lint gate (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/research/03-validation-and-test-surface.md:255-265`).
- `uv run ruff format --check src/ tests/` as the separate CI format gate (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/research/03-validation-and-test-surface.md:255-266`).

### 3.2 CI format check is separate from `make lint`

Memory `reference_make_lint_vs_ci_ruff_format.md` says: "`make lint` runs only `uv run ruff check .` (lint rules) — it does **NOT** run `ruff format --check`" and "Before pushing Python changes, run `uv run ruff format --check src/ tests/` locally" (`/config/.claude/projects/-config-workspace-IronClaude/memory/reference_make_lint_vs_ci_ruff_format.md:10-14`). The prior research independently confirms CI runs `ruff check src/ tests/` and `ruff format --check src/ tests/` separately, and concludes: "Therefore `make lint` (green) ≠ CI format gate (green)" (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/research/03-validation-and-test-surface.md:255-267`).

The new MDTM task should not use `make lint` as a substitute for the two explicit ruff commands above.

### 3.3 Baseline test attribution rule

The prior validation research documents exactly one acceptable pre-existing baseline failure: `tests/sprint/test_e2e_success.py::test_jsonl_events_for_each_phase` (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/research/03-validation-and-test-surface.md:228-239`). The new task should encode the same attribution rule: the full sprint suite may be clean, or it may fail only this exact node id if independently confirmed as baseline. Any other failing test is owned by this bug-fix task and must be investigated/fixed before final validation.

### 3.4 Validation artifact capture

Follow Template 02 L3: command/test items should capture both raw output and a structured summary (`.claude/templates/workflow/02_mdtm_template_complex_task.md:761-771`). The example task writes pytest output/summary and ruff results under `phase-outputs/test-results/` (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:260-274`). Mirror this: raw outputs to `phase-outputs/test-results/`, verdicts/fix plans to `phase-outputs/plans/`, final validation report to `phase-outputs/reports/`.

---

## 4. Example TASK-RF-20260604-035221 structure to mirror

The recent PR #124 bug-fix task is a strong structure model. Its frontmatter uses `type: "🐛 Bug Fix"`, `priority: "🔼 High"`, a concrete parent task, research files under `related_docs`, tags for the affected area, and `task_type: static` (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:1-43`). Its overview separates deliverables and warns about dirty working-tree isolation (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:47-57`). Its key objectives include mergeable/fix/test/validation/PR discipline in one list (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:58-67`).

The example also models the handoff file convention: `phase-outputs/` with `discovery/`, `test-results/`, `reviews/`, `plans/`, and `reports/`, and states that these files persist across batches/session rollovers (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:89-103`). Reuse this directory shape for the new task.

Useful phase structure from the example:

- Phase 1: worktree/rebase/conflict confirmation, beginning with status update and handoff directory creation (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:141-163`).
- Phase 2: one item per conflict hunk/file, with per-file compile checks (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:165-191`).
- Phase 3: one item per PASS-family predicate site, locating by predicate text rather than brittle line number (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:193-238`).
- Phase 4: RED→GREEN regression test with explicit RED and GREEN evidence capture (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:240-254`).
- Phase 5: full sprint pytest plus ruff lint and separate ruff format gates (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:256-274`).
- Phase Gate: final rf-qa structural validation with PASS/FAIL and fix cycle (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:276-284`).
- Phase 6: commit/push/PR with fork-only discipline and no `.claude/` staging (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:286-300`).
- Post-Completion Actions: output existence, validation verdict reread, summary creation, and final frontmatter completion (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:302-310`).

The example's final summary is also a good target shape: completed work, validation results, decisions/open questions, challenges, deviations, blockers, out-of-scope follow-ups, and execution log (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:314-356`).

---

## 5. Recommended phase plan for the new PASS_RECOVERED sprint rerun/handoff task

Because this is a high-priority code bug-fix task landing on a new branch off `origin/master`, use Template 02 and mirror the PR #124 model while adapting the branch/PR flow:

### Phase 1: Setup, status update, worktree/branch

First executable item updates frontmatter to `status: "🟠 Doing"`, sets `start_date`, and logs task start, matching I11's first-action status update rule (`.claude/templates/workflow/02_mdtm_template_complex_task.md:569-572`). Then create `phase-outputs/{discovery,test-results,reviews,plans,reports}/`. Then fetch `origin`, verify remotes, and create a new isolated worktree on a new branch off `origin/master` (not the existing dirty checkout). Require all subsequent git commands to use that worktree. This matches the goal's "NEW branch off origin/master" requirement and the worktree caution from the example task (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:153-159`).

### Phase 2: Locate exact current lines/sites by discovery

Do not hardcode stale line numbers. Use discovery items to read the source files identified by researcher-1 and locate the current predicates/call sites by stable text/symbol context. Write a site inventory to `phase-outputs/discovery/` containing file path, function/symbol, current predicate/text, current line number, expected replacement shape, and whether the site is in scope. This follows L1 discovery handoff rules: the discovery file is the deliverable and later items read it directly (`.claude/templates/workflow/02_mdtm_template_complex_task.md:737-747`).

### Phase 3: Apply per-site fixes

Create one B2 item per site discovered in Phase 2. Each item reads the site inventory and the specific source file, edits only that site, ensures the replacement is PASS-family/None-safe as specified by researcher-1, and records blockers if the predicate cannot be found or appears ambiguously. This satisfies A3's per-file/per-site granularity (`.claude/templates/workflow/02_mdtm_template_complex_task.md:91-96`). Include per-file `uv run python -m py_compile <file>` checks either immediately after each edited file or as grouped compile items after all sites in that file, but do not proceed past syntax failure.

### Phase 4: RED→GREEN regression test

Add or update tests based on researcher-2's fixtures. Include a RED demonstration item that proves the new/changed test fails against the unfixed behavior without leaving the worktree in the unfixed state, then a GREEN item that compiles the test file and runs the targeted test successfully. Capture raw and summary output under `phase-outputs/test-results/`. The PR #124 example's Phase 4 is the model for RED→GREEN evidence (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:240-254`).

### Phase 5: Full validation

Run and capture the complete validation command set:

1. `uv run python -m py_compile <file>` for every edited Python file.
2. `uv run pytest tests/sprint/ -q`.
3. `uv run ruff check src/ tests/`.
4. `uv run ruff format --check src/ tests/`.

If `tests/sprint/test_e2e_success.py::test_jsonl_events_for_each_phase` fails, it may be attributed to the documented baseline only if it is the sole failing node id; if it passes, record that the baseline is clean. Any other failing test must be fixed in scope.

### Phase Gate QA

Insert a final structural `rf-qa` task-integrity gate after Phase 5 and before commit/push/PR. The gate should verify all source sites, tests, RED/GREEN evidence, full suite, both ruff gates, `.claude/` staging prohibition, and fork PR discipline. Encode PASS/FAIL verdict handling and max 2 fix cycles, matching I16 and the example final QA gate (`.claude/templates/workflow/02_mdtm_template_complex_task.md:609-624`, `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md:276-284`).

### Phase 6: Commit, push, and create fork PR

Stage only source/test/task-output files required by the task; never stage `.claude/{skills,commands,agents,hooks,templates}`. Confirm `git remote -v`, confirm branch is based on `origin/master`, commit with a conventional bug-fix message, push to `origin`, and create the fork PR with:

```bash
gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "..." --body "..."
```

Then verify the returned PR URL starts with `https://github.com/IronbellyOrg/IronClaude/pull/`, not `SuperClaude-Org` (`/config/workspace/IronClaude/CLAUDE.md:46-56`).

### Post-Completion Actions

Before marking Done, verify all expected `phase-outputs/` artifacts exist, reread validation/QA/PR verdict files, create the Task Summary, update `completion_date`/`updated_date`, set `status: "🟢 Done"`, and add an execution-log completion entry. Keep these completion items inside the final post-completion area to satisfy the anti-orphaning rule (`.claude/templates/workflow/02_mdtm_template_complex_task.md:626-633`).

---

## Summary

Template 02 requires a high-granularity, self-contained MDTM task: B2-compliant one-paragraph checklist prompts, no executable checkboxes before Phase 1, per-site implementation items, a phase-gate QA checkpoint, and final completion/post-completion items kept inside the final closeout section. The new bug-fix task should be phased as: Phase 1 setup/worktree/new branch off `origin/master`; Phase 2 discovery to locate exact current lines/sites; Phase 3 per-site fixes; Phase 4 RED→GREEN regression test; Phase 5 `py_compile`, `pytest tests/sprint/ -q`, `ruff check`, and `ruff format --check`; Phase Gate QA; Phase 6 fork-only commit/push/PR. Fork PR discipline is mandatory: `origin` is `IronbellyOrg/IronClaude`, `upstream` is forbidden, `gh pr create` must use `--repo IronbellyOrg/IronClaude --base master --head <branch>`, pre-PR remote/fetch/rebase checks are required, and `.claude/` mirrors must never be staged except `.claude/settings.json`.

Status: Complete
