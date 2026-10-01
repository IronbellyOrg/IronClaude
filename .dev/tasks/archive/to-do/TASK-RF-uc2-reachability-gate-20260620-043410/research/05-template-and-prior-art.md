# Research 05: Template & Prior Art

Status: Complete

## Scope

Research topic: Template & Examples.

Source files reviewed:
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md`

Goal for downstream builder: use Template 02 and prior FR-RSR task only for MDTM structure/patterns while avoiding FR-RSR runtime-surface semantics in the new FR-RH1 contracted-sink reachability and oracle-admissibility gate task.

## Template 02 requirements to carry forward

### A3 granular breakdown

Template 02 requires every workflow phase to be decomposed into atomic, verifiable checklist items, with individual items for every file/component/iteration and exact file paths, specific requirements, and measurable outcomes. It explicitly bans high-level/bulk operations. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:108-112`.

The template also requires pre-enumeration for multi-item work, one checklist item per discovered/known item, incremental updates after each item, and consolidation only after all item-level work completes. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:114-132`.

### B2 self-contained checklist items

Every checklist item must be a complete self-contained prompt with: context reference and why, action and why, exact output specification, integrated verification, failure-only evidence logging, and an explicit completion gate. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:159-165`.

Template 02 explains the reason: Rigorflow runs across sessions, so prior context may be unavailable in later batches; standalone context-reading items without action are useless after rollover. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:151-157`.

Checklist items should be one verbose paragraph that could be executed independently; verification belongs in the item's `ensuring...` clause. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:167-179`.

Forbidden B2 patterns relevant to FR-RH1 task building:
- standalone read/context items with no output;
- missing source-of-truth context;
- multi-line checklist items;
- separate verification/confirmation items;
- overly granular no-op items;
- separate reminder blocks between checklist items.
Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:181-200`.

Template 02's key principles: context embedded in action items, verification embedded in action items, outputs as evidence of completion, log only failures/blockers, and QA process handles inter-batch verification. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:206-213`.

### QA gates and final validation

Any task with 2+ execution phases must include at least one phase-gate QA checkpoint between the primary execution phase and later dependent phases. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:635-636`.

QA gates with only 1-2 agents are prohibited at full intensity; final document/assembled-output gates require at least 6 agents and intermediate gates require at least 5 agents. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:638-638`.

A phase-gate QA checkpoint must follow M3 and consist of: L6 aggregation, multiple report-only lens agents, findings consolidation, exactly one fix agent, verification round, conditional proceed/fix-cycle control, and M4 fidelity items when applicable. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:640-647`.

Each QA agent spawn must be a self-contained B2 item with agent type, assigned lens, inputs, output report path, `fix_authorization: false`, and adversarial framing. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:649-649`.

Every QA step must be an explicit checklist item; no implicit/prose-only QA is allowed. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:651-651`.

QA verdicts are binary PASS/FAIL and any issue of any severity yields FAIL. Consolidated verdict is FAIL if any lens report has any issue. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:653-657`.

Fix cycles must be serialized: all lens agents report with `fix_authorization: false`, findings are consolidated, one fix agent applies all fixes with `fix_authorization: true`, and a verification round confirms; every step must be encoded as explicit checklist items. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:669-673`.

Before setting Done, the task must verify all checkboxes are complete, outputs exist, blockers have resolution notes, relevant tests pass for source changes, primary outputs undergo M3 lens-based QA, and source-document fidelity validation runs when applicable. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:675-684`.

For code-modifying tasks, M2 says code tasks need M3 after implementation or after combined implement+test, and fidelity only if code was derived from spec documents. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:1047-1057`.

M3 sequence details to mirror in task structure: aggregation, structural lens agents in parallel, content lens agents in parallel, optional domain-specific lenses, findings consolidation, one fix agent, verification round, and conditional proceed/repeat. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:1059-1096`.

M4 source fidelity, when applicable, runs after M3 and checks external fidelity rather than internal quality; it explicitly requires source-document identification, parallel fidelity agents, optional cross-source contradiction agent, consolidation, one fix agent, and fidelity verification. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:1098-1121`.

## Prior-task structural patterns worth reusing

### Frontmatter and execution context shape

The FR-RSR prior task uses rich frontmatter with `id`, `title`, `description`, `parent_doc`, `parent_task`, `spec_path`, `start_commit`, `executor_model_class`, `reflect_pre`, `reflect_post`, `related_docs`, `tags`, `template_schema_doc`, and `task_type`. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:1-65`.

Useful carry-forward pattern: set `reflect_post: ""` and include a warning that it is written by the POST reflect wrapper, not hand-authored. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:21-30`.

The prior task's Overview and Key Objectives establish load-bearing invariants before task phases and enumerate concrete objectives by phase/output. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:67-88`.

The prior task explicitly lists internal blocker ordering, including which phase blocks later phases and which acceptance/eval phases are terminal. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:90-100`.

The prior task has an `Execution Context` section with References, Source Areas, and Key Constraints. This is useful for FR-RH1 because it can record the patched REPORT as driving source, identify exact source areas, and state non-copy constraints from FR-RSR. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:115-136`.

The prior task uses a handoff directory convention under its task directory, with `phase-outputs/` subdirectories for `discovery/`, `test-results/`, `reviews/`, `plans/`, and `reports/`, plus a `qa/` directory for gate reports. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:138-150` and `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:172-178`.

The prior task embeds source-of-truth discipline and sync discipline directly in a baseline item: confirm branch/status, record start commit, state that edits land under `src/superclaude/`, and `.claude/` mirrors are never staged. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:176-178`.

### Phase pattern and verification cadence

The prior task structures implementation as ordered phases, with each phase carrying a short phase purpose/dependency paragraph before item prompts. Example: Phase 2 defines the source-of-truth file as a critical-path predecessor and blocks SKILL.md edits until verified. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:180-190`.

The prior task follows a useful rhythm: implement item(s) for a phase, then a phase verification item that re-reads changed regions, checks spec/TDD acceptance boxes, runs `make sync-dev` and `make verify-sync`, and logs blockers on failure. Example citations: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:208-210`, `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:220-222`, `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:236-238`, and `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:252-254`.

The prior task uses a dedicated final M3 gate over the whole change after evals and before sync/POST-reflect. The gate text explicitly states the reviewed surface, agent counts, adversarial framing, consolidation, one fix agent, verification, and max cycles. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:296-298`.

Concrete prior-task QA lens patterns worth adapting structurally, not semantically:
- structural conformance/additivity lens with report-only `rf-qa`: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:304-306`;
- blocker-ordering/counter-hygiene lens: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:308-310`;
- evidence-citation-accuracy lens: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:312-314`;
- fail-loud doctrine lens: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:316-318`;
- eval-falsifiability lens: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:320-322`;
- no-scope-expansion lens: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:324-326`.

The prior task then consolidates all lens reports, runs exactly one serialized fix agent, and performs a two-agent verification round with conditional repeat and halt controls. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:328-338`.

The prior task's release phase combines final sync (`make sync-dev`, `make verify-sync`), optional `uv run ruff format --check src/ tests/` for touched Python, and git-status source-of-truth checks. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:340-350`.

### Final POST reflect wrapper item

The prior task's Post-Completion Actions include output existence checks, eval/test confirmation, a note that the final M3 gate satisfied I17 lens QA, a Task Summary, the POST reflect wrapper shell-out as the penultimate item, and the final status update as the terminal item. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:352-364`.

The POST reflect wrapper pattern to reuse structurally: penultimate item, flat shell-out through `superclaude reflect run <taskfile> --depth deep --fix --promote`, recursion-breaker guard, `git -C <worktree> add -A`, no `--base`, no `--reflect`, no range, no agent-spawn, wrapper writes `reflect_post`, exit 0 is required to proceed, exits 10/11/2 halt, and final Done item may only run after wrapper exit 0 and `reflect_post` is recorded. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:362-364`.

## Prior-task FR-RSR semantics that MUST NOT be copied into FR-RH1

The FR-RSR prior task implements a runtime-surface reachability escalation for UC-2; FR-RH1 is a new contracted-sink reachability and oracle-admissibility gate from the patched REPORT. Reuse FR-RSR structure, not its semantics.

Do NOT copy these FR-RSR-specific semantics into FR-RH1 unless independently required by the patched REPORT:

1. Do not copy the runtime-surface problem statement or FR-S9-04 motivation. FR-RSR's motivating incident is a user-reachable `/ai`/Spawn surface passing despite unreachable implementation; its blind spot is STOP rubric/evidence chain/coverage/taxonomy around runtime surface reachability. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:71-75`.

2. Do not copy FR-RSR's `refs/runtime-surface.md` deliverable as a required FR-RH1 file. FR-RSR's P1 objective is a runtime-surface ref with allowlist, language table, degrade oracle, rootwalk, and `runtime-surface-ledger.yaml`. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:81-82`.

3. Do not copy FR-RSR's symbol-anchored runtime-surface tagger and production-caller sweep semantics. FR-RSR's gather objective adds §6.1 steps 4b'/4b, using a surface allowlist, production-vs-test/comment partitioning, degrade oracle, and entrypoint-rootwalk. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:82-83` and `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:196-202`.

4. Do not copy FR-RSR's six additive `runtime_surface_*` fields or FR-RSR-specific rationale for its version bump. FR-RSR explicitly adds `runtime_surface_*` fields and bumps `contract_version` from 1.5.0 to 1.6.0. FR-RH1 independently requires its own `contract_version: "1.6.0"` bump for patched REPORT R4; the task must implement FR-RH1's `reachability_*` schema, not FR-RSR's runtime-surface schema. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:83-84` and `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:204-210`; FR-RH1 source is `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md:91-101`.

5. Do not copy FR-RSR's STOP pre-filter trigger `runtime_surface_unreached ≥ 1`, `surface_unreached` reason, or degrade-only non-escalation semantics. FR-RSR's gate phase is tied to decided UNREACHED runtime surfaces, not contracted-sink semantics. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:84-85` and `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:212-222`.

6. Do not copy FR-RSR's §10.9 UNREACHED finding-modifier or its by-evidence mapping branches. FR-RSR's classify phase maps UNREACHED findings onto existing taxonomy classes and has specific counter hygiene around `deviation_count_by_class.regression` vs `verification_regressions_detected`. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:85-86` and `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:224-238`.

7. Do not copy FR-RSR's reviewer-spec ledger routing for `<output>/artifacts/runtime-surface-ledger.yaml` or the `FR-RSR.9` grounding-hunk entry. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:86-86` and `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:240-254`.

8. Do not copy FR-RSR eval case names/ids/fixtures: `uc2-unwired-surface-passes`, `uc2-surface-positive-control`, `uc2-surface-dynamic-dispatch`, `uc2-surface-degraded-backend`, `uc2-surface-test-only-ref`, ids 37-41. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:87-88` and `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:256-294`.

9. Do not copy FR-RSR's explicit load-bearing invariants: symbol-anchored-not-requirement-anchored tagger and dynamic/registry/decorator/reflection/packaging-entrypoint DEGRADE default. Citation: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:73-75` and `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:130-136`.

10. Do not copy prior task's phase names as semantic commitments (`Source of Truth — refs/runtime-surface.md`, `Gather + Contract`, `Gate`, `Classify`, `Surface`, `Falsify`) unless renamed and repurposed for FR-RH1. The phase skeleton is useful; the FR-RSR labels and FR ids are not. Citations: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md:180-258`.

## Recommended task-item breakdown for FR-RH1 builder

The downstream FR-RH1 MDTM should use this structural breakdown, with content filled from R1-R4 research and the patched REPORT:

1. **Phase 1: Preparation and baseline**
   - Update frontmatter status/start date and execution log.
   - Create `phase-outputs/{discovery,test-results,reviews,plans,reports}` and `qa/`.
   - Capture branch, status, `start_commit`, and source-of-truth rules.

2. **Phase 2: Source/context anchoring for FR-RH1**
   - Read patched REPORT and R1/R2 research anchors; extract only FR-RH1 contracted-sink and oracle-admissibility obligations.
   - Create a phase-output requirements map for FR-RH1: contracted sink definition, admissible oracle conditions, gate trigger, contract/report fields if any, and non-goals.
   - Verification item: re-read patched REPORT/R1 anchors and confirm no FR-RSR runtime-surface semantics leaked.

3. **Phase 3: Implement FR-RH1 protocol changes**
   - One self-contained item per target file/section identified by R2/R3/R4.
   - Each item must read its source anchors, perform one surgical edit, include exact output/modified path, and embed verification with an `ensuring...` clause.
   - Include a phase verification item that re-reads changed regions, checks FR-RH1 acceptance criteria, and runs `make sync-dev && make verify-sync` where source components changed.

4. **Phase 4: Implement FR-RH1 tests/evals/fixtures**
   - One item per eval/fixture/test file; use real fixture names/ids from R4, not FR-RSR ids 37-41.
   - Add a test-run item using UV for Python, with raw output and summary written to `phase-outputs/test-results/`.
   - Add an assessment/fix item that reads failures, fixes the correct source/fixture/assertion, and reruns.

5. **Phase Gate: final M3 QA over whole FR-RH1 change**
   - L6 aggregate full diff/change inventory.
   - Spawn report-only structural/content lens agents with FR-RH1-specific lenses. Suggested lenses: template conformance/actionability, evidence-citation accuracy, FR-RH1 contract-sink semantics, oracle-admissibility semantics, no-FR-RSR-semantic-leakage, eval/test falsifiability.
   - Consolidate findings, run exactly one serialized fix agent if needed, run verification round, and conditionally repeat/halt per M3/I20.

6. **Phase 5 or Release phase: sync and release checklist**
   - Run `make sync-dev && make verify-sync`.
   - If Python touched, run `uv run ruff format --check src/ tests/`.
   - Confirm `git status --short` does not include staged `.claude/` mirrors.
   - Write release/verdict artifacts under the FR-RH1 task directory.

7. **Post-Completion Actions**
   - Verify every output exists.
   - Confirm tests/evals passed from actual artifacts.
   - Record how final M3 gate satisfies post-completion lens QA; state whether M4 fidelity applies based on whether outputs are source-derived documents or code/spec implementation.
   - Write task summary.
   - Run POST reflect wrapper as penultimate item.
   - Update frontmatter status/completion date only after POST reflect wrapper succeeds.

## Gaps and Questions

None blocking. The only important caution is semantic separation: reuse the prior FR-RSR task's MDTM structure, but implement FR-RH1's independent `contract_version: "1.6.0"` and `reachability_*` schema from the patched REPORT.

## Summary

Template 02 imposes granular, self-contained, top-to-bottom checklist construction with explicit M3/I20 QA gates and POST-completion validation. The FR-RSR prior task is valuable as a structural exemplar for frontmatter, execution context, phase verification cadence, final M3 gate, release sync, and POST reflect wrapper. Its runtime-surface semantics, contract fields, FR ids, eval names/ids, and UNREACHED/degrade/counter behavior must not be copied into FR-RH1; the FR-RH1 task must derive all substantive semantics from the patched REPORT and the other research files.
