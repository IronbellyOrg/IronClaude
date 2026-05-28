# Template and Task Patterns Research

Status: Complete

## Scope Reviewed

- Primary dev template: `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.claude/templates/workflow/02_mdtm_template_complex_task.md`.
- Source template equivalent: `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` exists and identifies itself as Template 02 for complex tasks, extending Template 01 with Section L for discovery, testing, review, conditional logic, and aggregation patterns (`src/.../02_mdtm_template_complex_task.md:51-63`).
- Representative task files reviewed:
  - `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/tasks/to-do/TASK-RF-20260522-151622/TASK-RF-20260522-151622.md`
  - `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/tasks/to-do/TASK-RF-20260522-153212/TASK-RF-20260522-153212.md`
  - `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/tasks/to-do/TASK-RF-20260522-180000-pr73-review/TASK-RF-20260522-180000-pr73-review.md`
  - `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/tasks/to-do/TASK-RF-20260522-194500-pr75-review/TASK-RF-20260522-194500-pr75-review.md`

## MDTM Structure Required for Executable Tasklists

1. **Frontmatter is required and metadata-rich.** Template 02 frontmatter includes `id`, `title`, `description`, `status`, `type`, `priority`, dates, assignee, coordinator, parent/dependency fields, related docs, tags, `template_schema_doc`, review metadata, and `task_type` (`.claude/.../02_mdtm_template_complex_task.md:1-44`). Existing RF tasks follow this pattern and set `template_schema_doc` to `.claude/templates/workflow/02_mdtm_template_complex_task.md`, e.g. TASK-RF-20260522-151622 lines 1-44 and TASK-RF-20260522-153212 lines 1-52.
2. **Human-readable body starts with title, overview, objectives, prerequisites/context, then phases.** TASK-RF-20260522-153212 uses `#` title and `## Task Overview`, resolved questions, key objectives, dependencies, previous-stage outputs, handoff file convention, frontmatter update protocol, execution context, then `## Detailed Task Instructions` and phases (`TASK-RF-20260522-153212.md:54-190`). TASK-RF-20260522-151622 uses title, overview, objectives, prerequisites, execution context, then phase sections (`TASK-RF-20260522-151622.md:46-84`).
3. **Phase-oriented execution is sequential.** The template requires every actionable item to be a checkbox, no nested checkboxes, no parent checkbox summaries before components, step headers for grouping, and top-to-bottom completion (`.claude/.../02_mdtm_template_complex_task.md:278-292`, `.claude/.../02_mdtm_template_complex_task.md:294-365`). Existing RF tasks encode phases as `## Phase N` / `### Phase N` headings with `**Step X.Y:**` labels followed by checkbox items, e.g. TASK-RF-20260522-151622 lines 84-179 and TASK-RF-20260522-153212 lines 191-217.
4. **Handoff workspace convention is expected for complex tasks.** Template 02 states complex handoff files go under `.dev/tasks/TASK-NAME/phase-outputs/` with `discovery/`, `test-results/`, `reviews/`, `plans/`, and `reports/` subdirectories (`.claude/.../02_mdtm_template_complex_task.md:718-730`). Current RF tasks adapt this to `.dev/tasks/to-do/TASK-RF-.../phase-outputs/`; TASK-RF-20260522-153212 documents the same five subdirectories and their purposes (`TASK-RF-20260522-153212.md:153-166`).

## Required Sections and Content Blocks

- **Task Overview / Key Objectives**: Template PART 2 includes these sections before execution (`.claude/.../02_mdtm_template_complex_task.md:890-903`). Representative tasks use objectives as acceptance criteria rollups; TASK-RF-20260522-151622 lists concrete deliverables and gates in objectives (`TASK-RF-20260522-151622.md:54-65`), while TASK-RF-20260522-153212 lists seven numbered objectives including final regression and QA gates (`TASK-RF-20260522-153212.md:113-123`).
- **Prerequisites & Dependencies / Previous Stage Outputs**: Template includes `## Prerequisites & Dependencies`, parent/dependency bullets, and previous-stage outputs as informational-only input inventory (`.claude/.../02_mdtm_template_complex_task.md:904-927`). TASK-RF-20260522-153212 includes concrete required previous-stage outputs with paths and purpose lines (`TASK-RF-20260522-153212.md:141-151`).
- **Execution Context / Key constraints**: Existing RF tasks add an `## Execution Context` reader-aid section with references/source areas/key constraints before phases; TASK-RF-20260522-151622 lines 74-80 and TASK-RF-20260522-153212 lines 179-185 show the pattern.
- **Detailed Task Instructions / Phases**: Template PART 2 uses `## Detailed Task Instructions`, `### Phase 1`, `### Phase 2`, optional phase gates, optional testing phase, `### Phase 3`, `## Post-Completion Actions`, and `## Task Log / Notes` (`.claude/.../02_mdtm_template_complex_task.md:954-1128`). Existing tasks may use `## Phase N` headings directly for shorter issue-fix tasks (TASK-RF-20260522-180000-pr73-review lines 77-87) or `### Phase N` under `## Detailed Task Instructions` for larger tasks (TASK-RF-20260522-153212 lines 189-193).
- **Task Log / Notes**: Template requires Task Summary, Execution Log, per-phase findings, Phase Gate Findings, Follow-Up Items, and Deviations from Process (`.claude/.../02_mdtm_template_complex_task.md:1128-1204`). Existing tasks implement these sections and populate them with evidence and deviations, e.g. TASK-RF-20260522-153212 lines 495-661.

## Checklist Item Pattern Needed

Executable checklist items should be **single self-contained prompts** with enough context to execute after session rollover. Template B2 requires six elements: context reference with why, action with why, output specification, integrated verification via an `ensuring...` clause, failure-only evidence logging, and explicit completion gate (`.claude/.../02_mdtm_template_complex_task.md:142-148`). Template B3 requires one full paragraph, not bullets, and B4 demonstrates action plus verification integrated in one checkbox (`.claude/.../02_mdtm_template_complex_task.md:150-158`).

Practical item style observed in RF tasks:

- **Edit item**: names the exact file, tool, local region, `old_string`, `new_string`, preservation constraints, failure logging, then completion. TASK-RF-20260522-151622 Step 2.1 is a full example (`TASK-RF-20260522-151622.md:104-121`). TASK-RF-20260522-180000-pr73-review uses the same old/new string pattern for targeted source edits (`TASK-RF-20260522-180000-pr73-review.md:89-103`).
- **Command/gate item**: lists exact commands, output capture path, pass criteria, and failure handling. TASK-RF-20260522-151622 Step 2.5 uses four grep checks, a capture file, and `OK`/`FAIL` pass criteria (`TASK-RF-20260522-151622.md:177-179`). TASK-RF-20260522-153212 Step 6.1 encodes five static grep gates with expected hit counts and hard-blocker behavior (`TASK-RF-20260522-153212.md:451-453`).
- **Creation item**: uses Write to create a concrete file with an exact section schema and verification criteria. TASK-RF-20260522-151622 Step 3.1 creates `doc-discovery.md`, specifies four top-level sections, allowed placeholders, and no TODOs (`TASK-RF-20260522-151622.md:183-373`).
- **Execution hygiene**: Items often embed project-specific command constraints (e.g. `uv run`, `make verify-sync`, `make sync-dev`) rather than relying on memory. TASK-RF-20260522-153212 Step 1.3 embeds `unset VIRTUAL_ENV` and `uv run pytest` capture details (`TASK-RF-20260522-153212.md:203-205`).

## QA Gate Encoding

Template rules:

- Any task with 2+ execution phases must include at least one phase-gate QA checkpoint between a primary execution phase and dependent subsequent phase (`.claude/.../02_mdtm_template_complex_task.md:599-600`).
- A phase-gate checkpoint consists of aggregation, QA agent spawn, and conditional-action items (`.claude/.../02_mdtm_template_complex_task.md:602-607`).
- QA verdicts are binary PASS/FAIL; any issue severity fails the gate. Fix-cycle limits vary by gate type: research-gate 3, synthesis-gate 2, report-validation 3, task-integrity 2, qualitative 3 (`.claude/.../02_mdtm_template_complex_task.md:609-624`).
- Composite M1 gate pattern is: aggregation item, QA spawn item, conditional proceed/fix-cycle item (`.claude/.../02_mdtm_template_complex_task.md:843-850`). Task-building tasks require gates after research and task file creation (`.claude/.../02_mdtm_template_complex_task.md:852-858`).

Observed task encodings:

- TASK-RF-20260522-153212 encodes named gates `PG-1`, `PG-2`, and `PG-FINAL`; `PG-FINAL` has an input aggregation item, rf-qa spawn item, and conditional proceed/retry item (`TASK-RF-20260522-153212.md:471-483`).
- The rf-qa spawn item includes `ADVERSARIAL STANCE`, `fix_authorization: true`, QA mode, gate name, input file, full acceptance criteria, report output path, and PASS/FAIL requirements (`TASK-RF-20260522-153212.md:477-479`).
- Final PR review task uses a simpler final QA gate: spawn `rf-qa` with `phase_type: task-integrity`, `fix_authorization: true`, adversarial stance, explicit inputs, acceptance criteria, output report path, and max two fix cycles (`TASK-RF-20260522-180000-pr73-review.md:395-399`).
- Current tasklist should use the richer PG pattern when there are research outputs feeding synthesis/task creation; for a small issue-fix task, a final task-integrity gate may be sufficient if no intermediate phase depends on unverified outputs.

## Validation Item Style

Validation is integrated into action items, not split into standalone `verify this file` items. Template C3 requires verification in action items via `ensuring...`, not separate verification checklist items (`.claude/.../02_mdtm_template_complex_task.md:219-223`). Template I17 separately requires post-completion validation before Done: all checkboxes complete, outputs exist, blockers resolved, and tests pass for code-modifying tasks (`.claude/.../02_mdtm_template_complex_task.md:626-633`). For code modifications, Template I18 requires a test item specifying command, pass criteria, capture location, and B2 pattern compliance (`.claude/.../02_mdtm_template_complex_task.md:637-644`).

Observed validation styles:

- **Inline integrity gates**: grep checks or command outputs are encoded as executable items with exact expected strings/counts, e.g. TASK-RF-20260522-180000-pr73-review Phase 2 grep gate (`TASK-RF-20260522-180000-pr73-review.md:121-123`) and Phase 6 grep gate (`TASK-RF-20260522-180000-pr73-review.md:377-379`).
- **Final regression sweep**: TASK-RF-20260522-153212 Step 6.3 runs pytest, ruff, verify-sync, and pyproject diff with explicit exit-code expectations (`TASK-RF-20260522-153212.md:459-461`).
- **Evidence matrix/report artifacts**: TASK-RF-20260522-153212 Step 6.4 creates an AC matrix mapping findings to remediation evidence; Step 6.5 aggregates phase outputs into a final regression report (`TASK-RF-20260522-153212.md:463-469`).
- **Post-completion output existence check**: Template starts post-completion with a Glob-based output existence check (`.claude/.../02_mdtm_template_complex_task.md:1118-1120`); TASK-RF-20260522-153212 instantiates this with a list of expected phase-output paths (`TASK-RF-20260522-153212.md:485-487`).

## Completion Item Pattern

Template post-completion actions are ordered before frontmatter Done: verify outputs, rerun or confirm tests, create task summary, then update completion date/status and log completion (`.claude/.../02_mdtm_template_complex_task.md:1118-1126`). Existing larger tasks follow this exactly: TASK-RF-20260522-153212 verifies outputs, reruns pytest, creates summary, then updates frontmatter to Done (`TASK-RF-20260522-153212.md:485-493`). Smaller issue-fix tasks may compress post-completion to a final frontmatter/log item after a final QA gate, as in TASK-RF-20260522-180000-pr73-review Phase 9 (`TASK-RF-20260522-180000-pr73-review.md:403-407`).

Recommended executable completion pattern for the current tasklist:

1. Post-completion output existence check using concrete expected paths.
2. If code changed, final `uv run pytest ...` or scoped validation command capture.
3. Task summary inserted into Task Log / Notes with work completed, challenges, deviations, blockers, and follow-up status.
4. Final frontmatter update to `status: "🟢 Done"`, `completion_date`, `updated_date`, plus Execution Log entry.

## Practical Build Guidance for This Tasklist

- Use Template 02 for complex task-building work because it is explicitly for discovery, testing, review, conditional logic, or aggregation (`src/.../02_mdtm_template_complex_task.md:60-63`).
- Put all worker-executable steps in ordered phase checklists; do not put checkboxes in prerequisite/context sections.
- For research-agent outputs, use L1/L6 patterns: write findings under `phase-outputs/discovery/` or `phase-outputs/reports/`, then aggregate before QA.
- For task creation from research, use L2 build-from-discovery: read all research files and source templates, then create/update the final task file, ensuring each checklist item is self-contained and cites sources.
- Insert a `research-gate` after research aggregation and a `task-integrity` gate after final task file assembly, matching Template M2 task-building applicability (`.claude/.../02_mdtm_template_complex_task.md:852-858`).
- Use adversarial rf-qa spawn items with `fix_authorization: true` when the gate is allowed to make small corrections, mirroring existing PG-FINAL and PR-review tasks (`TASK-RF-20260522-153212.md:477-479`; `TASK-RF-20260522-180000-pr73-review.md:397-399`).

## Verification Follow-Up

- [CODE-VERIFIED] The `.claude/templates/workflow/02_mdtm_template_complex_task.md` dev copy and `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` source template matched byte-for-byte when checked during QA with `cmp -s`.
- [CODE-VERIFIED] The `.dev/tasks/to-do/` directory contained four `TASK-RF-*.md` task examples at research-gate recheck time, and the four examples listed in Scope Reviewed cover that available sample set.

## Summary

Template 02 requires metadata-rich frontmatter, overview/objectives/prerequisites/context, sequential phase checklists, phase-output handoff directories, QA gates for dependent phases, post-completion validation, and a Task Log. Executable items should be one-paragraph self-contained prompts with source context, action, output path, embedded `ensuring...` verification, blocker logging, and completion gate. Existing RF task files consistently instantiate this with exact file paths, old/new strings for edits, grep/test gates with output captures, rf-qa gates with PASS/FAIL and fix-cycle rules, and final output/test/status completion items.
