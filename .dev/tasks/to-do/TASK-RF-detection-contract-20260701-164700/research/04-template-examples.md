# Template & Examples Research

Status: Complete

## Scope and sources checked

- [CODE-VERIFIED] Primary source-of-truth template: `/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`; active dev mirror checked at `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md`.
- [CODE-VERIFIED] Fallback/generic source-of-truth template checked for frontmatter parity: `/config/workspace/IronClaude/src/superclaude/templates/workflow/01_mdtm_template_generic_task.md`; active dev mirror checked at `/config/workspace/IronClaude/.claude/templates/workflow/01_mdtm_template_generic_task.md`.
- Representative examples checked: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-tasklist-rfmerge-20260619-041423/TASK-RF-tasklist-rfmerge-20260619-041423.md`, `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260602-135209/TASK-RF-20260602-135209.md`, plus prior research notes under `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/`, `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-uc2-reachability-gate-20260620-043410/`, and `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-STDIN-RECON-REMEDIATION-20260501/`.

## Template 02 required structure and sections

- Template 02 is the correct generated-tasklist base for complex MDTM tasks because it explicitly says it extends Template 01 with intra-task handoff patterns and is for tasks requiring discovery, testing, review, conditional logic, or aggregation between checklist items. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:77-80`.
- The generated task must preserve the frontmatter schema. Important fields for this detection-contract tasklist include `spec_path`, `reflect_pre`, `reflect_post`, `related_docs`, `template_schema_doc`, and `task_type: static`. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:1-61`. Template 01 has the same top-level frontmatter shape, including `reflect_post`, so Template 02 does not weaken generic schema expectations. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/01_mdtm_template_generic_task.md:1-61`.
- Part 1 is builder-only and must not appear in the generated output; Part 2 is the copyable task-file body starting at `# [Task Title]`. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:63-80` and `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:1139-1157`.
- Part 2 required body sections to mirror: `Task Overview`, `Key Objectives`, `Prerequisites & Dependencies`, `Execution Context` with `References`, `Source Areas`, `Key Constraints`, `Handoff File Convention`, `Frontmatter Update Protocol`, then `Detailed Task Instructions`. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:1157-1233`.
- Handoff files are first-class: the task should name the task workspace and use `phase-outputs/discovery/`, `test-results/`, `reviews/`, `plans/`, and `reports/` so outputs survive session rollovers. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:1209-1221`.

## B2 self-contained item pattern

- Every checklist item must be self-contained for session rollover protection: context is not assumed to survive later batches. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:151-157`.
- B2 requires six elements in every checklist item: context reference with why, action with why, exact output specification, integrated `ensuring...` verification, evidence-on-failure-only logging, and the explicit completion gate sentence. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:159-165`.
- B3 says checklist items should be one full paragraph, not multi-line/bulleted mini-prompts. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:167-170`.
- Forbidden patterns to avoid in generated detection-contract tasks: standalone read-context items, missing source-of-truth references, multi-line/bulleted checklist items, separate verification items, overly granular standalone directory items, and reminder blocks between items. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:181-200`.
- The Part 2 examples provide ready shapes for discovery, build-from-discovery, test/execute, and conditional assess items, all using output files under `phase-outputs/` and integrated verification. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:1278-1286` and `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:1349-1363`.

## QA gate patterns to mirror

- Any task with 2+ execution phases needs at least one phase-gate QA checkpoint between the primary execution phase and dependent later phases. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:635-647`.
- New task files must use M3 lens-based QA, not deprecated single-agent M1. Every gate step is explicit: aggregation, report-only lens agents, consolidation, one serialized fix agent, verification agents, and conditional proceed/repeat. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:1048-1057` and `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:1059-1097`.
- QA agent spawn items must themselves follow B2 and include the exact agent type, assigned lens, inputs, output report path, `fix_authorization: false`, and adversarial framing. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:649-651`.
- Serialized fix authorization is mandatory: all lens agents report with `fix_authorization: false`, findings consolidate, exactly one `rf-qa` fix agent applies fixes with `fix_authorization: true`, then verification runs. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:745-757`.
- QA intensity can be tuned. Standard intensity gives 3 intermediate agents and 7 final agents; full intensity follows the larger I19 floors. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:793-840`.
- Strong example: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-tasklist-rfmerge-20260619-041423/TASK-RF-tasklist-rfmerge-20260619-041423.md` encodes phase gates as many explicit checklist items: aggregate outputs, spawn named structural/content lenses with adversarial prompts, consolidate, single fix agent, two verification agents, then conditional proceed. Citation: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-tasklist-rfmerge-20260619-041423/TASK-RF-tasklist-rfmerge-20260619-041423.md:364-402`.

## Post-reflect wrapper item requirements

- Template frontmatter reserves `reflect_post`; the wrapper/executor writes the final result, so generated tasks should leave room rather than hand-authoring a final verdict. Citation: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md:32`.
- Current prior research says the old subagent `/sc:reflect --mode post` item is obsolete for the wrapper rewrite. The desired generated item is a flat Bash shell-out with the recursion breaker and `superclaude reflect run <ABS_TASKLIST> --depth deep --fix --promote`; it consumes the exit code and keeps the item penultimate before `Update task status to Done`. Citation: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/research/01-o1-taskbuilder-edit-surface.md:34-38`.
- The same research keeps the rerun convention: use `/task`, never `/sc:task`, for any re-execution of task-builder tasklists. Citation: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/research/01-o1-taskbuilder-edit-surface.md:49-52`.
- A later prior-art note gives the structural pattern to reuse: penultimate item, `git -C <worktree> add -A` before reflect so untracked files are visible, no `--base`, no `--reflect`, no range, no agent spawn, wrapper writes `reflect_post`, exit 0 proceeds, exits 10/11/2 halt, and Done runs only after wrapper success plus recorded `reflect_post`. Citation: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-uc2-reachability-gate-20260620-043410/research/05-template-and-prior-art.md:104-108`.

## Effective examples and conventions to mirror

- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-tasklist-rfmerge-20260619-041423/TASK-RF-tasklist-rfmerge-20260619-041423.md` is the best current example for a large source-editing task: rich frontmatter with `start_commit`, `executor_model_class`, `reflect_pre`, populated `reflect_post`, source-of-truth `template_schema_doc`, and source-first related docs. Citation: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-tasklist-rfmerge-20260619-041423/TASK-RF-tasklist-rfmerge-20260619-041423.md:1-75`.
- That RFMerger task also demonstrates clear source-of-truth discipline in the overview: edit `src/superclaude/...` first, run `make sync-dev` and `make verify-sync`, regenerate `.claude/` mirrors, never stage `.claude/`. Citation: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-tasklist-rfmerge-20260619-041423/TASK-RF-tasklist-rfmerge-20260619-041423.md:82-86`.
- Good B2 examples in RFMerger include long single-paragraph items that read handoff files, source files, and design notes, then perform an exact edit or test, write outputs, and include blocker logging plus completion gate. Citation: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-tasklist-rfmerge-20260619-041423/TASK-RF-tasklist-rfmerge-20260619-041423.md:337-362`.
- `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260602-135209/TASK-RF-20260602-135209.md` is an older but still useful documentation/source-sync example: objectives explicitly include source-of-truth discipline, eval scaffold boundaries, and per-phase QA gates. Citation: `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260602-135209/TASK-RF-20260602-135209.md:55-65`.
- The same completed task shows good end-state notes: challenges, deviations, blockers, follow-ups, execution log, and per-phase findings are captured under `Task Log / Notes`, with unresolved non-blockers moved into follow-up/open-question structures rather than silently dropped. Citation: `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260602-135209/TASK-RF-20260602-135209.md:520-564`.

## Pitfalls to encode as constraints

- No `/sc:task` on generated task-builder tasklists. If the task must be rerun, say `/task <absolute-task-path>`; prior post-reflect research explicitly preserves `/task` and rejects `/sc:task` for re-execution. Citation: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/research/01-o1-taskbuilder-edit-surface.md:49-52`.
- No `.claude/` staging or direct mirror edits. Generated source-editing tasks should state that `.claude/` is sync output and only `src/superclaude/...` plus tests/task artifacts are staged. RFMerger states this in both overview and sync items. Citation: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-tasklist-rfmerge-20260619-041423/TASK-RF-tasklist-rfmerge-20260619-041423.md:82-86` and `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-tasklist-rfmerge-20260619-041423/TASK-RF-tasklist-rfmerge-20260619-041423.md:346-350`.
- Avoid one-shot output generation for long generated artifacts. A tracked issue recommends incremental file writing because one-shot generation truncated TDD/PRD extraction and correlated with duplicate heading failures. Citation: `/config/workspace/IronClaude/.dev/tasks/to-do/ISSUE-pipeline-one-shot-output.md:24-38`.
- Anti-orphaning: final status/frontmatter update must live inside the final phase, not as an orphaned section after the executable phase. Citation: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-STDIN-RECON-REMEDIATION-20260501/qa/gap-resolution.md:35-46`.
- For detection-contract tasklists specifically, include constraints that prevent stale ranges and uncaptured files in reflect: stage new files before post-reflect; do not pass `--base`, `--reflect`, or `A..HEAD` ranges in the generated wrapper item; rely on wrapper writeback. Citation: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-uc2-reachability-gate-20260620-043410/research/05-template-and-prior-art.md:104-108`.

## Recommendations for the generated MDTM tasklist

1. Use Template 02, not Template 01, because this task involves discovery, implementation, verification, QA gates, and post-reflect handoff.
2. Populate `Execution Context` with explicit references, source areas, and constraints, including: UV-only Python commands; source-of-truth `src/superclaude/` edits; no `.claude/` staging; `/task` not `/sc:task`; flat post-reflect wrapper; and anti-orphaning.
3. Make every implementation/test/QA item a single B2 paragraph. Do not add standalone read-context or verification-only items.
4. Use `phase-outputs/` handoff files for inventories, anchor maps, test results, QA reports, and final summaries.
5. Encode QA gates explicitly with named lenses and serialized fix authorization. Do not put QA only in prose.
6. Put the post-reflect wrapper item immediately before the final Done/status item. The final Done item must require wrapper exit 0 and non-empty `reflect_post`.

## Gaps and Questions

- [CODE-VERIFIED] Template source-of-truth is `/config/workspace/IronClaude/src/superclaude/templates/workflow/`; `.claude/templates/workflow/` is an active dev mirror only.
- [UNVERIFIED prior-art] Post-reflect wrapper conventions cited from older `.dev/tasks` research should be treated as prior-art constraints to carry into the tasklist, then verified by the task executor against current task-builder/reflect wrapper surfaces before implementation is marked done.
- [UNVERIFIED design decision] The generated task should include OQ-1/OQ-2/OQ-3 decision gates before source-edit phases, even though Template 02 itself does not prescribe this project-specific decision policy.

## Key Takeaways

- [CODE-VERIFIED] Use Template 02 because this task has design decisions, implementation, tests, QA gates, command/skill sync, and post-reflect validation.
- [CODE-VERIFIED] The tasklist must use `/task <absolute path>` for execution/re-execution and must not suggest `/sc:task`.
- [CODE-VERIFIED] The tasklist must stage new files before the post-reflect wrapper so untracked implementation files are included in the audit.
