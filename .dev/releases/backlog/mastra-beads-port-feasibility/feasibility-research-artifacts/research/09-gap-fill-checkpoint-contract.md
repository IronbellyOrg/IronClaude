# Research: 09 - Gap Fill - Checkpoint Contract
**Investigation Type:** Targeted Code Tracer / Integration Mapper
**Scope:** sc-tasklist-protocol checkpoint generation/template shape; sprint parser, prompt logic, checkpoint verifier/executor behavior; directly referenced tests/docs/examples
**Status:** Complete
**Date:** 2026-06-02
---

## Assigned Gap

RG-C2 investigates a checkpoint-contract contradiction between `/sc:tasklist` generation output and Sprint CLI execution/checkpoint validation. The suspected contradiction is: `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` says checkpoints are numbered `### T<PP>.<NN> -- Checkpoint:` task entries, while `src/superclaude/cli/sprint/process.py` prompt text tells phase agents to scan for sibling `### Checkpoint:` sections.

## Files Investigated

### `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`

[CODE-VERIFIED] Lines 343-391 define checkpoint generation as numbered task entries, not sibling checkpoint headings. The required heading form is `### T<PP>.<NN> -- Checkpoint: ...`, with mid-phase checkpoint tasks after every 5 regular tasks and exactly one end-of-phase checkpoint task as the last numbered task in the phase.

[CODE-VERIFIED] Lines 947-1027 restate the phase-file checkpoint template in numbered task form and require `**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/<deterministic-name>.md` inside each checkpoint task block. Lines 1062-1117 make this a pre-write Sprint compatibility self-check, specifically rejecting sibling `### Checkpoint:` headings in check 18.

[CODE-VERIFIED] Lines 793-812 define the checkpoint report template in the index and lines 1466-1480 list `Write` and `Task`/`Skill` usage, but this is a skill-generation protocol rather than Sprint CLI runtime code.

### `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md`

[CODE-CONTRADICTED] This extracted human-review template is stale relative to the source-of-truth `SKILL.md`. Lines 101-105 still show inline checkpoints as sibling headings: `### Checkpoint: Phase <P> / Tasks <start>-<end>`. Lines 117-125 still require the phase file to end with `### Checkpoint: End of Phase <N>`. That conflicts with `SKILL.md` lines 343-391 and 947-1027, which require numbered task-form checkpoint headings.

[CODE-VERIFIED] The file itself warns at lines 1-3 that it is a read-only reference extracted from SKILL.md and that “the skill uses its own inline copy.” Current code therefore should treat this template as documentation/reference only, not as the executable generation contract.

### `src/superclaude/cli/sprint/process.py`

[CODE-CONTRADICTED] `ClaudeProcess.build_prompt()` lines 187-195 instructs the phase-level agent to scan the phase file for ``### Checkpoint:`` sections and skip checkpoint report writing if no such sections exist. That literal prompt wording does not match the numbered task-form checkpoint contract in `SKILL.md` lines 343-391 and 947-1027.

[CODE-VERIFIED] This prompt path only applies to freeform phase execution through `ClaudeProcess`; in the current executor, phases with parseable `### T<PP>.<TT>` headings are routed through per-task execution rather than through this full-phase prompt. The per-task routing is in `executor.py` lines 1259-1301, which calls `_parse_phase_tasks()` and then `execute_phase_tasks()` when tasks are present.

[CODE-VERIFIED] `process.py` line 170 launches `/sc:task Execute all tasks in @<phase_file> --compliance strict --strategy systematic` for freeform phase execution, then appends the stale checkpoint-scanning instructions at lines 187-195.

### `src/superclaude/cli/sprint/config.py`

[CODE-VERIFIED] Phase discovery is filename-based. `PHASE_FILE_PATTERN` at lines 15-26 accepts `phase-N-tasklist.md`, `pN-tasklist.md`, `phase_N_tasklist.md`, and `tasklist-pN.md`. `discover_phases()` scans index text for these names at lines 120-127 and falls back to directory scan at lines 128-140.

[CODE-VERIFIED] Task counting and parsing are numbered-task-heading based. `_TASK_ID_HEADING_RE` at lines 28-34 counts `### T<PP>.<TT>` headings, and `count_tasks_in_file()` returns that count at lines 37-49. `_TASK_HEADING_RE` at lines 374-377 parses `### T<PP>.<TT> -- <title>` task blocks. `parse_tasklist()` lines 420-492 emits a `TaskEntry` for every such heading, including checkpoint tasks because their heading has the same numbered task form.

[CODE-VERIFIED] `parse_tasklist()` does not special-case checkpoint tasks. It extracts IDs, titles, dependencies, command, classifier, and deliverable descriptions from every numbered heading at lines 426-490. A numbered checkpoint task therefore becomes a normal executable `TaskEntry` with title `Checkpoint: ...`.

### `src/superclaude/cli/sprint/checkpoints.py`

[CODE-VERIFIED] Runtime checkpoint path parsing is path-line based, not sibling-heading-only. `CHECKPOINT_PATH_PATTERN` at lines 18-25 matches `Checkpoint Report Path:` with optional bold/backticks and captures the declared path.

[CODE-VERIFIED] Runtime checkpoint heading recognition supports both contracts. `CHECKPOINT_HEADING_PATTERN` at lines 27-33 matches legacy `### Checkpoint: <name>` and Wave-4 numbered task form `### T<PP>.<NN> -- Checkpoint: <name>`.

[CODE-VERIFIED] `extract_checkpoint_paths()` lines 36-94 reads every `Checkpoint Report Path:` declaration, strips the portable `TASKLIST_ROOT/` prefix at lines 70-77, names each checkpoint from the nearest preceding supported checkpoint heading at lines 57-63 and 78-80, then resolves relative paths against `release_dir` at lines 82-91.

[CODE-VERIFIED] Manifest and recovery also support numbered task-form checkpoints. `build_manifest()` lines 135-166 uses `discover_phases()` and `extract_checkpoint_paths()` for every phase. `_extract_verification_block()` lines 293-331 explicitly documents and matches both legacy `### Checkpoint:` and Wave-4 `### T<PP>.<NN> -- Checkpoint:` headings.

### `src/superclaude/cli/sprint/executor.py`

[CODE-VERIFIED] Current sprint execution has two execution paths. `_parse_phase_tasks()` lines 1118-1133 parses a phase file for numbered task inventory; `execute_sprint()` lines 1259-1301 uses per-task execution when such tasks are present and does not enter the freeform `ClaudeProcess.build_prompt()` branch for that phase.

[CODE-VERIFIED] Per-task execution runs each parsed task independently. `execute_phase_tasks()` lines 927-1073 iterates over `TaskEntry` objects, and `_run_task_subprocess()` lines 1076-1115 prompts Claude with `Execute task <task_id>: <title>`, the phase file path, and the parsed description. This includes numbered checkpoint tasks parsed from `config.py`; they are not separately handled as checkpoint sections.

[CODE-VERIFIED] Checkpoint file enforcement exists only in the phase-level freeform branch. `_verify_checkpoints()` is called after `_determine_phase_status()` at lines 1512-1531 in the branch entered after `ClaudeProcess` finishes. The per-task branch at lines 1259-1301 aggregates task results and continues without calling `_verify_checkpoints()`.

[CODE-VERIFIED] `_verify_checkpoints()` itself is compatible with numbered checkpoint tasks because it imports `extract_checkpoint_paths()` and `verify_checkpoint_files()` at lines 1837-1838. It verifies all declared `Checkpoint Report Path:` entries and can downgrade status to `PASS_MISSING_CHECKPOINT` in full mode at lines 1848-1891.

[CODE-VERIFIED] End-of-sprint manifest generation is path-parser based and therefore compatible with numbered checkpoints. Lines 1702-1721 call `build_manifest(config.index_path, config.release_dir)` and write `manifest.json` with total/found/missing counts.

[CODE-VERIFIED] Crash recovery’s non-zero-exit checkpoint inference expects only the end-of-phase file path `release_dir/checkpoints/CP-P<phase>-END.md` and PASS markers, independent of heading shape. See `_check_checkpoint_pass()` lines 1894-1905 and `_determine_phase_status()` lines 2101-2109.

### `tests/sprint/test_checkpoints.py`

[CODE-VERIFIED] Tests explicitly cover Wave-4 numbered checkpoint tasks. `test_wave4_numbered_checkpoint_task_form()` lines 92-104 verifies that `### T01.06 -- Checkpoint: ...` is parsed by `extract_checkpoint_paths()` with the heading label and expected path. `test_wave4_mid_and_end_mixed_with_legacy()` lines 106-120 verifies mixed numbered and legacy forms.

[CODE-VERIFIED] Gate tests still seed legacy sibling checkpoint headings at lines 155-176 and verify off/shadow/soft/full mode behavior at lines 186-257. These tests prove `_verify_checkpoints()` behavior for path existence, but they do not exercise the per-task execution branch in `executor.py`.

[CODE-VERIFIED] Manifest/recovery tests mostly seed legacy headings in `_seed_sprint()` lines 288-315, but `test_wave4_verification_block_copied_into_recovered_report()` lines 463-502 verifies numbered checkpoint tasks round-trip through `build_manifest()` and `recover_missing_checkpoints()` with verification/exit criteria copied into the recovered report.

### `src/superclaude/cli/sprint/commands.py` (directly referenced via checkpoint tests)

[CODE-VERIFIED] The `verify-checkpoints` CLI command lines 376-415 uses `build_manifest()` and `recover_missing_checkpoints()` from `checkpoints.py`, so its actual behavior accepts numbered task-form checkpoints. However, `_print_checkpoint_table()` line 426 emits a stale no-checkpoints message that says `No ### Checkpoint: sections declared`, even though numbered checkpoint tasks are also supported.

### Directly related docs and examples

[CODE-CONTRADICTED] `docs/analysis-sc-tasklist.md` line 452 shows a legacy phase example ending with `### Checkpoint: End of Phase N`. This is contradicted by current `SKILL.md` lines 343-391 and 947-1027, which require numbered checkpoint task headings.

[CODE-VERIFIED] `docs/generated/sprint-cli/v3.7-refactor/chunk-01-checkpoint-enforcement.md` lines 121-140 accurately documents the intended Path A effect of converting `### Checkpoint:` headings into `### T<PP>.<NN> -- Checkpoint:` tasks: Path A’s `_parse_phase_tasks()` should include checkpoint tasks in the per-task loop and each checkpoint task should write the checkpoint file as its primary deliverable. Current `config.py` lines 420-492 and `executor.py` lines 1259-1301 verify the parsing/routing side of that claim.

[CODE-CONTRADICTED] The same generated v3.7 docs still contain a now-inaccurate implementation-state claim: `MERGED-REFACTORING-RECOMMENDATION.md` lines 61-62 and 74 say `_verify_checkpoints()` should be inserted in the Path A block. Current `executor.py` lines 1259-1301 do not call `_verify_checkpoints()` in the per-task branch; it is only called in the freeform branch at lines 1512-1531.

[CODE-VERIFIED] Current sample tasklists include both shapes. `rg` over `.dev/test-sprints`, `.dev/test-fixtures`, and `.dev/releases/complete` found legacy sibling checkpoint headings such as `.dev/test-sprints/smoke-test/phase-1-tasklist.md:172`, and numbered checkpoint headings such as `.dev/releases/complete/cliEval/phase-1-tasklist.md:251`, `.dev/releases/complete/task-builder-merge/phase-1-tasklist.md:258`, and `.dev/releases/complete/v3.7-task-unified-v2/test-run/tasklists/phase-1-tasklist.md:245`.

### `src/superclaude/cli/sprint/models.py` (checkpoint data model referenced by checkpoint utilities)

[CODE-VERIFIED] `PhaseStatus.PASS_MISSING_CHECKPOINT` is defined at lines 223-228 and treated as terminal success at lines 235-260. `SprintConfig.checkpoint_gate_mode` defaults to `shadow` at lines 389-392.

[CODE-CONTRADICTED] Model comments are partly stale: line 223 says reports are declared by `### Checkpoint:` reports, and line 322 says `CheckpointEntry.name` comes from a `### Checkpoint:` heading. Runtime parser support in `checkpoints.py` lines 27-33 accepts both legacy sibling and numbered task-form checkpoint headings.

## Findings

1. The checkpoint-contract contradiction is real in documentation/prompt surfaces, but not in the shared runtime checkpoint parser.
   - `SKILL.md` canonical generation contract requires numbered checkpoint task entries.
   - `phase-template.md`, `process.py` prompt text, `docs/analysis-sc-tasklist.md`, and several comments/messages still refer to sibling `### Checkpoint:` sections.

2. Sprint CLI currently recognizes numbered checkpoint tasks in structural parsing.
   - `config.py` parses any `### T<PP>.<TT> -- ...` heading into a task, so numbered checkpoint tasks become normal `TaskEntry` objects.
   - `checkpoints.py` recognizes both legacy sibling headings and numbered task-form checkpoint headings for checkpoint path extraction and recovery.

3. The largest current runtime gap is executor branch coverage, not checkpoint path parsing.
   - Per-task phases (`Path A`) parse and execute numbered checkpoint tasks as normal tasks, but the per-task branch does not call `_verify_checkpoints()` after aggregating task results.
   - Freeform phases (`Path B`) call `_verify_checkpoints()`, but their prompt text still tells the agent to scan only for legacy `### Checkpoint:` sections.

4. The adapter-safe contract is to emit numbered checkpoint task entries with `Checkpoint Report Path:` lines. This satisfies current `parse_tasklist()`, `extract_checkpoint_paths()`, `build_manifest()`, `recover_missing_checkpoints()`, and current Wave-4 tests.

## Evidence Table

| Claim | Evidence | Staleness Tag |
|---|---|---|
| `/sc:tasklist` canonical checkpoint generation is numbered task form. | `SKILL.md` lines 343-391, 947-1027, 1062-1117. | [CODE-VERIFIED] |
| Extracted phase template still shows legacy sibling checkpoint sections. | `phase-template.md` lines 101-125. | [CODE-CONTRADICTED] |
| Freeform sprint prompt still scans for ``### Checkpoint:`` sections only. | `process.py` lines 187-195. | [CODE-CONTRADICTED] |
| Phase/task parser counts and parses numbered task headings. | `config.py` lines 28-49 and 374-492. | [CODE-VERIFIED] |
| Checkpoint path parser supports both legacy and numbered task-form checkpoint headings. | `checkpoints.py` lines 18-33 and 36-94. | [CODE-VERIFIED] |
| Per-task executor branch does not call `_verify_checkpoints()`. | `executor.py` lines 1259-1301 versus `_verify_checkpoints()` call at lines 1512-1531. | [CODE-VERIFIED] |
| End-of-sprint manifest uses shared parser and is compatible with numbered checkpoints. | `executor.py` lines 1702-1721; `checkpoints.py` lines 135-166. | [CODE-VERIFIED] |
| Tests cover Wave-4 numbered checkpoint parsing/recovery. | `tests/sprint/test_checkpoints.py` lines 92-120 and 463-502. | [CODE-VERIFIED] |
| Some docs still show legacy checkpoint shape. | `docs/analysis-sc-tasklist.md` line 452. | [CODE-CONTRADICTED] |
| Current examples include both old and new shapes. | `rg` evidence: legacy `.dev/test-sprints/smoke-test/phase-1-tasklist.md:172`; numbered `.dev/releases/complete/cliEval/phase-1-tasklist.md:251`. | [CODE-VERIFIED] |

## Canonical Checkpoint Contract

Sprint-compatible checkpoint output should use this canonical shape:

1. Phase files are discovered from `tasklist-index.md` by literal phase filenames such as `phase-1-tasklist.md`.
2. Every executable task, including checkpoints, uses `### T<PP>.<TT> -- <Title>`.
3. Checkpoints are first-class numbered tasks:
   - Mid-phase: `### T<PP>.<NN> -- Checkpoint: Phase <P> / Tasks T<PP>.<start>-T<PP>.<end>`.
   - End-of-phase: `### T<PP>.<last> -- Checkpoint: End of Phase <P>`.
4. The end-of-phase checkpoint is the last numbered task in the phase file.
5. Every checkpoint task includes a `Checkpoint Report Path:` line. The path should be deterministic and release-root relative through the `TASKLIST_ROOT/` placeholder:
   - Mid-phase: `TASKLIST_ROOT/checkpoints/CP-P<PP>-T<start>-T<end>.md`.
   - End-of-phase: `TASKLIST_ROOT/checkpoints/CP-P<PP>-END.md`.
6. Checkpoint task content should instruct the executor agent to write the checkpoint report as the task deliverable, with verification/exit criteria copied into the task body.
7. Legacy sibling `### Checkpoint:` headings remain accepted by `checkpoints.py` as backwards compatibility, but should not be emitted by new generators/adapters.

## Adapter Implications

For a Mastra/Backlog/Beads adapter:

1. Emit numbered checkpoint task entries, not sibling `### Checkpoint:` sections.
2. Include checkpoint tasks in the same task numbering sequence as regular tasks. Do not create a separate checkpoint namespace.
3. Treat checkpoint reports as first-class deliverables with `D-CP<PP>` / `D-CP<PP>-MID...` style IDs if mirroring `/sc:tasklist` output.
4. Put `Checkpoint Report Path:` in every checkpoint task. `checkpoints.py` is path-line driven; the report path is the strongest compatibility anchor.
5. Preserve `TASKLIST_ROOT/checkpoints/...` paths when generating portable tasklists. Runtime parser strips `TASKLIST_ROOT/` and resolves against `release_dir`.
6. If the adapter consumes existing backlog/beads items, normalize any legacy checkpoint sections into numbered task entries before Sprint CLI execution.
7. Avoid relying on the freeform `process.py` checkpoint prompt. For numbered-task tasklists, current execution is routed through per-task execution, where checkpoint writing depends on the checkpoint task body itself.
8. If using Sprint CLI enforcement, prefer running or extending `verify-checkpoints` after execution because current per-task branch does not call `_verify_checkpoints()` inline.

## Gaps and Questions

1. Should `executor.py` call `_verify_checkpoints()` in the per-task branch after `execute_phase_tasks()` and phase status aggregation? Current generated docs recommend this, but current code does not do it.
2. Should `process.py` freeform prompt lines 187-195 be updated to say “scan for `Checkpoint Report Path:` declarations / checkpoint task entries” instead of only “scan for `### Checkpoint:` sections”?
3. Should `phase-template.md` be synced with `SKILL.md` numbered checkpoint task shape, or removed/renamed as a legacy reference?
4. Should `verify-checkpoints` no-checkpoints output in `commands.py` line 426 be changed from `No ### Checkpoint:` sections to `No Checkpoint Report Path declarations`?
5. Should `models.py` comments for `PASS_MISSING_CHECKPOINT` and `CheckpointEntry.name` be updated to mention both legacy and numbered checkpoint headings?
6. Current tests verify numbered parser/recovery support, but do not verify per-task `Path A` calls `_verify_checkpoints()` because current code does not. Add/adjust tests if remediation includes executor branch wiring.

## Stale Documentation Found

- `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` lines 101-125: legacy sibling checkpoint sections. [CODE-CONTRADICTED]
- `src/superclaude/cli/sprint/process.py` lines 187-195: freeform prompt scans only for legacy `### Checkpoint:` sections. [CODE-CONTRADICTED]
- `docs/analysis-sc-tasklist.md` line 452: legacy checkpoint example. [CODE-CONTRADICTED]
- `src/superclaude/cli/sprint/commands.py` line 426: no-checkpoints message names only `### Checkpoint:` sections. [CODE-CONTRADICTED]
- `src/superclaude/cli/sprint/models.py` lines 223 and 322: comments describe only legacy `### Checkpoint:` headings. [CODE-CONTRADICTED]
- `docs/generated/sprint-cli/v3.7-refactor/MERGED-REFACTORING-RECOMMENDATION.md` lines 61-62 and 74: recommends Path A `_verify_checkpoints()` insertion; current code has not implemented that insertion. [CODE-CONTRADICTED]

## Summary

The canonical checkpoint contract for new tasklists is numbered checkpoint task entries with explicit `Checkpoint Report Path:` declarations. The contradiction is real: source-of-truth `SKILL.md` now requires numbered task-form checkpoints, while several templates/docs/prompt strings still say or show legacy sibling `### Checkpoint:` sections. Runtime parser support is better than the stale prompt suggests: `checkpoints.py` already accepts both shapes, and `config.py` parses numbered checkpoint tasks as ordinary tasks. The remediation target should therefore be to align stale prompt/template/docs/comments with the numbered-task contract and, if Sprint CLI enforcement is in scope, add `_verify_checkpoints()` coverage to the per-task executor branch after task aggregation.
