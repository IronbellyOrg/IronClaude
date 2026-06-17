# Research 03: Template & Examples

Status: Complete

## Scope

Research topic: Template & Examples for building `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-pr167-verdict-regex-20260613-000000/TASK-RF-pr167-verdict-regex-20260613-000000.md`.

Reviewed sources:

- `/config/workspace/IronClaude/.claude/templates/workflow/01_mdtm_template_generic_task.md`
- `/config/workspace/IronClaude/src/superclaude/templates/workflow/01_mdtm_template_generic_task.md`
- `/config/workspace/IronClaude/CLAUDE.md`
- `/config/.claude/CLAUDE.md`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-pr167-verdict-regex-20260613-000000/research-notes.md`
- Nearby task examples:
  - `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/TASK-RF-reflect-marker-leak-20260611-175724.md`
  - `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/TASK-RF-reflect-post-gate-wiring-20260611-022409.md`

## Findings

### 1. Use MDTM Template 01 from the source-of-truth mirror

- [CODE-VERIFIED] The dev mirror exists at `/config/workspace/IronClaude/.claude/templates/workflow/01_mdtm_template_generic_task.md`. Its frontmatter defines the generic task schema, including `id`, `title`, `description`, status/type/priority options, `parent_task`, `depends_on`, `spec_path`, `reflect_pre`, `reflect_post`, `related_docs`, `template_schema_doc`, dates, and `task_type` fields at lines 1-61.
- [CODE-VERIFIED] The canonical source file also exists at `/config/workspace/IronClaude/src/superclaude/templates/workflow/01_mdtm_template_generic_task.md` with the same frontmatter opening at lines 1-61. For a generated task, use this template schema path in frontmatter rather than inventing a custom shape.
- [CODE-VERIFIED] The task-builder planning notes explicitly say to use MDTM Template 01 because this remediation is a bounded two-file bug fix with known inputs, outputs, and deterministic tests; the notes also require a standard post-execution reflect gate item because `/sc:troubleshoot --fix` needs a reviewable task artifact rather than direct code edits (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-pr167-verdict-regex-20260613-000000/research-notes.md:44-47`).

Recommended frontmatter values for the task file:

- `id`: `TASK-RF-pr167-verdict-regex-20260613-000000`
- `title`: concise action such as `Fix PR #167 verdict regex decorations`
- `type`: `🐛 BugFix` or `⚙️ Maintenance` (bug fix is more accurate)
- `priority`: `🔼 High`
- `created_date` / `updated_date`: `2026-06-13`
- `assigned_to`: `rf-task-executor` or `orchestrator`
- `autogen_method`: `task-builder`
- `template_schema_doc`: `/config/workspace/IronClaude/src/superclaude/templates/workflow/01_mdtm_template_generic_task.md` only; the `.claude/` dev mirror may be read as parity evidence but must not be encoded as the source-of-truth schema path.
- `task_type`: `static`, because the research notes identify a known two-file remediation surface, not dynamic discovery (`research-notes.md:13-14`, `research-notes.md:31-36`)

### 2. MDTM checklist items must be self-contained execution prompts

Template requirements to encode in the task file:

- [CODE-VERIFIED] Every checklist item must be self-contained for session rollover protection: context from earlier batches may not be available later (`01_mdtm_template_generic_task.md:147-153`).
- [CODE-VERIFIED] Each item must include context reference with why, action with why, output specification, integrated verification, failure-only evidence logging, and an explicit completion gate (`01_mdtm_template_generic_task.md:155-162`).
- [CODE-VERIFIED] Checklist items should be one full paragraph, not multi-line/bulleted mini-plans (`01_mdtm_template_generic_task.md:163-166`).
- [CODE-VERIFIED] Forbidden patterns include standalone “read context” items, missing source-of-truth references, multi-line checklist items, separate verification-only items, overly granular items such as directory creation alone, and separate reminder blocks between checklist items (`01_mdtm_template_generic_task.md:177-197`).
- [CODE-VERIFIED] Verification belongs inside each action via an “ensuring...” clause, not as separate verification checkboxes (`01_mdtm_template_generic_task.md:232-236`, `01_mdtm_template_generic_task.md:607-612`).

Task-building implication for this PR #167 fix:

- Do not create separate items like “Read gates.py” or “Verify tests.” Instead, make each implementation/test item read the relevant research/source file, perform the edit, and include its own verification clause.
- For this bounded code task, use phases such as:
  1. Preparation and status update.
  2. Implement verdict regex and tests.
  3. Run targeted validation.
  4. Final review/reflect and completion.

### 3. Execution order and task-file mutation constraints are strict

Template execution constraints to include or preserve:

- [CODE-VERIFIED] The five-step worker pattern is `READ → IDENTIFY → EXECUTE → UPDATE → REPEAT`; workers must read the task, find the first unchecked item, execute only that item, mark only that item complete, then repeat (`01_mdtm_template_generic_task.md:407-416`).
- [CODE-VERIFIED] Prohibited worker actions include working from memory, executing multiple checklist items at once, skipping phases, assuming completion without verification, delegating across phase boundaries, skipping phase-gate QA, and skipping post-completion validation (`01_mdtm_template_generic_task.md:418-425`).
- [CODE-VERIFIED] Universal requirements include completing all steps sequentially, reviewing referenced files before use, avoiding assumptions, and marking every checkbox complete (`01_mdtm_template_generic_task.md:445-452`).
- [CODE-VERIFIED] Worker agents may only modify the task file to check off items, update frontmatter, add Task Log entries, or add dynamic items inside dynamic marker regions (`01_mdtm_template_generic_task.md:453-459`).
- [CODE-VERIFIED] Frontmatter status protocol is mandatory: task start sets status to `🟠 Doing` and `start_date`; completion sets status to `🟢 Done` and `completion_date`; blocked state sets `⚪ Blocked` and `blocker_reason`; each work session updates `updated_date` (`01_mdtm_template_generic_task.md:460-464`).
- [CODE-VERIFIED] The template says status update must be the first action (`01_mdtm_template_generic_task.md:603-605`), and the Part 2 task body starts Phase 1 with a status-update checklist item (`01_mdtm_template_generic_task.md:1141-1142`).

Recommended task-file wording:

- [CODE-VERIFIED] Add a “Detailed Task Instructions” paragraph: “YOU MUST complete every checklist item in order, one item at a time. Do not skip ahead. Mark only the current item complete before proceeding.” This mirrors nearby task examples (`TASK-RF-reflect-marker-leak-20260611-175724.md:164-167`).
- [CODE-VERIFIED] Ensure every checklist item ends with: “This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.” This is the template’s explicit gate (`01_mdtm_template_generic_task.md:161-162`) and is used in nearby examples (`TASK-RF-reflect-marker-leak-20260611-175724.md:170-177`).

### 4. Required execution rules for this PR #167 task

The generated task file must include these project/task constraints:

1. [CODE-VERIFIED] **UV only for Python commands.** Project instructions prohibit `python -m`, bare `pip install`, and `python script.py`; examples are `uv run pytest`, `uv pip install`, and `uv run python` (`/config/workspace/IronClaude/CLAUDE.md:5-8`, `/config/workspace/IronClaude/CLAUDE.md:62-70`; global instructions repeat this at `/config/.claude/CLAUDE.md:3-12`).
2. [CODE-VERIFIED] **Work in the PR branch worktree, not repo root.** The PR branch worktree is `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473`, and research notes say it is checked out at PR #167 head `65bac7ed3b267faabcf3ea7844a6fd0cd412e97b` (`research-notes.md:21-23`). All implementation and validation checklist items should use absolute paths under that worktree, e.g. `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py` and `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py`.
3. [CODE-VERIFIED] **Do not edit, stage, or commit `.claude/` generated output.** Project instructions state `.claude/{skills,commands,agents,hooks,templates}/*` is gitignored sync-dev output and only `.claude/settings.json` is tracked (`/config/workspace/IronClaude/CLAUDE.md:16-19`). They prohibit `git add .claude/...`, `git add -f` on `.claude/`, suggesting such staging commands, or authoring task instructions/follow-ups that tell the user to stage `.claude/` paths (`/config/workspace/IronClaude/CLAUDE.md:20-29`). The PR #167 research notes reiterate that this task should only touch `src/superclaude/cli/prd/gates.py` and `tests/cli/prd/test_gates.py` in the PR worktree (`research-notes.md:21-23`).
4. [CODE-VERIFIED] **No commit, push, or PR actions unless explicitly instructed by the user/task.** The current research assignment explicitly forbids staging, committing, and pushing; the generated execution task should preserve this as a Key Constraint and should stop after validation plus task-log summary unless a later instruction authorizes git operations. If PR work is ever requested later, project rules require targeting the fork with `gh pr create --repo IronbellyOrg/IronClaude ...`, never upstream (`/config/workspace/IronClaude/CLAUDE.md:35-60`).
5. [CODE-VERIFIED] **Feature branches/worktrees avoid parallel-session conflicts.** Project guidance says multiple Claude Code sessions should use git worktrees to avoid conflicts and allow independent working directories (`/config/workspace/IronClaude/CLAUDE.md:256-274`). For this task, the worktree already exists; do not switch the main repo working tree or edit `/config/workspace/IronClaude/src/...` for the PR fix.
6. [CODE-VERIFIED] **Do not broaden scope.** Research notes define the exact code/test surfaces: `gates.py` and `test_gates.py` (`research-notes.md:13-14`) and say there are no ambiguities (`research-notes.md:27-29`, `research-notes.md:48-50`).

### 5. Validation commands to encode

The task file should include targeted validation using UV. Researcher 2 covers test details, but this template/execution pass should require task items to run commands from the PR worktree with absolute paths or an explicit working-directory instruction.

Recommended validation items:

- Targeted pytest for the verdict parser tests, e.g. run from `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473`: `uv run pytest tests/cli/prd/test_gates.py::TestCheckVerdictField -q`.
- Broader PRD gate regression, e.g. from the same worktree: `uv run pytest tests/cli/prd/test_gates.py -q`.
- [CODE-VERIFIED] If the code edit changes formatting-sensitive Python, include CI-parity ruff checks: `uv run ruff format --check src/ tests/` and `uv run ruff check src/ tests/`. This is consistent with project UV/ruff guidance (`/config/workspace/IronClaude/CLAUDE.md:109-119`) and nearby task examples requiring UV-only ruff/pytest validation (`TASK-RF-reflect-marker-leak-20260611-175724.md:134-138`).

[CODE-VERIFIED] Each validation item should capture or summarize results in the Task Log or a task-local `phase-outputs/test-results/` file. Nearby task examples create task-local handoff subdirectories under their task dir for discovery, test-results, reviews, plans, and reports (`TASK-RF-reflect-marker-leak-20260611-175724.md:141-152`). For a quick, bounded fix, it is acceptable to keep this simpler: log command, exit code, and pass/fail in Task Log unless the builder wants durable raw outputs.

### 6. QA and post-completion requirements

Template requirements:

- [CODE-VERIFIED] Every task must include Post-Completion Actions (`01_mdtm_template_generic_task.md:614-619`).
- [CODE-VERIFIED] Post-completion validation must verify all checklist items are complete, all output files exist, blocker entries have resolution notes, relevant tests pass if source code was modified, and QA/validation gates run as applicable (`01_mdtm_template_generic_task.md:659-668`).
- [CODE-VERIFIED] Code-modifying tasks must include at least one testing item specifying the command, pass criteria, result capture location, and B2-style self-contained prompt (`01_mdtm_template_generic_task.md:672-679`).
- [CODE-VERIFIED] The template includes optional lens-based QA and source-fidelity gates in post-completion actions (`01_mdtm_template_generic_task.md:1251-1267`). For this quick two-file bug fix, the task-builder can use a lighter final review/reflect posture if the controlling workflow allows, but it must still include the standard post-execution reflect gate noted by the task research (`research-notes.md:44-47`).

Recommended post-completion items for PR #167:

1. Verify no unchecked items remain except the current post-completion item; verify blockers have resolution statuses.
2. Verify only intended files changed in the PR worktree: `src/superclaude/cli/prd/gates.py` and `tests/cli/prd/test_gates.py`.
3. Confirm targeted tests and ruff checks passed or log exact unresolved failures.
4. Run/record the standard post-execution reflect gate required by the task-builder notes, but do not mark status Done if the gate surfaces unresolved regressions.
5. Update task summary and frontmatter status/date.
6. Stop without staging, committing, pushing, or opening a PR unless later explicit instructions authorize it.

### 7. Nearby example patterns worth copying

- [CODE-VERIFIED] `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/TASK-RF-reflect-marker-leak-20260611-175724.md` is a good modern example for:
  - [CODE-VERIFIED] Filled `Execution Context` with References, Source Areas, Key Constraints, and frontmatter protocol (`lines 117-162`).
  - [CODE-VERIFIED] Absolute-path source areas and task-local handoff outputs (`lines 126-152`).
  - [CODE-VERIFIED] Self-contained checklist items with explicit context, action, verification, failure logging, and completion gate (`lines 170-191`).
  - [CODE-VERIFIED] UV-only validation and no `.claude/` mirror staging in key constraints (`lines 134-138`).
- [CODE-VERIFIED] `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/TASK-RF-reflect-post-gate-wiring-20260611-022409.md` is a useful example for:
  - [CODE-VERIFIED] Capturing branch/worktree prerequisites and `make sync-dev`/`make verify-sync` only when source-of-truth component mirrors are involved (`lines 92-97`).
  - [CODE-VERIFIED] Dense Key Objectives with exact pass criteria (`lines 84-90`).
  - [CODE-VERIFIED] Clear “do not touch” constraints in Execution Context (`lines 99-104`).

For PR #167, do not copy the complex multi-agent QA volume wholesale. This is a quick bounded fix; use the generic-template structure and the local constraints above.

## Recommended task skeleton

```markdown
# Fix PR #167 verdict regex decorations

## Task Overview
[Explain that this fixes the PRD semantic gate verdict parser so markdown verdict labels with numeric-list prefixes or underscore/bold decorations are accepted while invalid shapes remain rejected.]

## Key Objectives
1. Update `_check_verdict_field` in `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py` only as needed.
2. Add/adjust `TestCheckVerdictField` coverage in `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py`.
3. Run targeted UV pytest/ruff validation from `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473`.
4. Stop without staging, committing, pushing, or opening a PR unless explicitly authorized.

## Execution Context
### References
- [Research synthesis](/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-pr167-verdict-regex-20260613-000000/research-notes.md)
- [File inventory](/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-pr167-verdict-regex-20260613-000000/research/01-file-inventory.md)
- [Patterns and tests](/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-pr167-verdict-regex-20260613-000000/research/02-patterns-and-tests.md)
- [Template and execution](/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-pr167-verdict-regex-20260613-000000/research/03-template-and-execution.md)

### Source Areas
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py`

### Key Constraints
- Use UV only for Python commands.
- Work only in `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473` for code/test edits and validation.
- Do not edit, stage, or commit `.claude/` generated mirrors.
- Do not stage, commit, push, or open/update a PR unless explicitly instructed.
- Preserve existing invalid verdict protections.
```

## Open Questions

[CODE-VERIFIED] None identified for the template/execution surface. The task research already states there are no ambiguities and the intent is clear from the review URL, report, and codebase context (`research-notes.md:27-29`, `research-notes.md:48-50`).

## Documentation verification tags

- [CODE-VERIFIED] `/config/workspace/IronClaude/CLAUDE.md` and `/config/.claude/CLAUDE.md` both require UV-only Python operations; the generated task must use `uv run pytest`, `uv run ruff`, and must not use bare `python -m`, `pip install`, or `python script.py`.
- [CODE-VERIFIED] `/config/workspace/IronClaude/CLAUDE.md` defines `.claude/` generated-output source-of-truth restrictions; the generated task must not edit, stage, or commit `.claude/` mirrors.
- [CODE-VERIFIED] `/config/workspace/IronClaude/src/superclaude/templates/workflow/01_mdtm_template_generic_task.md` is the canonical template schema path for this task; the `.claude/` mirror is parity/read-only context only.
- [CODE-VERIFIED] Nearby task examples demonstrate useful phrasing for Execution Context and self-contained items, but the generated task should rely on the canonical template and the PR #167 research files for actual requirements.

## Summary

[CODE-VERIFIED] The task should be generated from Template 01 using the canonical source template path, not the `.claude/` mirror. It must instruct execution in the PR #167 worktree, require UV-only validation, forbid `.claude/` staging and any commit/push action, and include self-contained checklist items plus a final post-execution reflection/status-update sequence.
