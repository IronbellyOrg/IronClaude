# Prompt: Generate Atomic-Commit Release Specs for v3.7a and v3.7b

> **Purpose**: This prompt produces TWO release specification documents following the template at `src/superclaude/examples/release-spec-template.md`. Each spec must be complete enough that a junior engineer can execute every task by reading the spec alone, with no tribal knowledge or codebase exploration required.
>
> **Core constraint**: Every task must be implementable as a single atomic commit that leaves the codebase in a passing state (`uv run pytest` green). No task may depend on uncommitted work from another task. Every intermediate state must be testable.

---

## YOUR ASSIGNMENT

Produce two release specification documents:

1. **R1: v3.7a -- Pipeline Reliability & Naming Consolidation** (~480 LOC)
2. **R2: v3.7b -- Sprint TUI v2** (~800 LOC)

Both specs MUST follow the exact section structure in `src/superclaude/examples/release-spec-template.md`. Both are `spec_type: refactoring`. Include Section 9 (Migration & Rollout) and Section 4.3 (Removed Files) for both.

---

## SOURCE DOCUMENTS (read all before writing)

You MUST read and incorporate ALL of the following source documents. They contain the validated decisions, adversarial rulings, dependency graphs, and task details that govern these specs. Do not invent tasks, change assignments, or override rulings.

| Document | Path | Contains |
|----------|------|----------|
| Merged Refactoring Recommendation | `docs/generated/sprint-cli/v3.7-refactor/MERGED-REFACTORING-RECOMMENDATION.md` | Unified task list, implementation order, file impact matrix, dependency graph, risk register, LOC estimates |
| Path A Partition Document | `docs/generated/sprint-cli/v3.7-refactor/path-a-partition-document.md` | R1/R2 task assignments, cross-release integration points, hard/soft prerequisites, boundary justifications |
| Context 1: Path A Deficiencies | `docs/generated/sprint-cli/v3.7-refactor/context-01-path-a-deficiencies.md` | The 7 validated deficiencies, the two execution paths, bug evidence with line numbers |
| Context 2: Adversarial Debate Rulings | `docs/generated/sprint-cli/v3.7-refactor/context-02-debate-rulings.md` | 5 rulings: per-task block INTEGRATE, scope boundary INTEGRATE, result file REJECT, sprint context INTEGRATE, stop-on-STRICT-fail REJECT |
| Context 3: Spec Gap Analysis | `docs/generated/sprint-cli/v3.7-refactor/context-03-v37-spec-gap-analysis.md` | Which v3.7 features target Path B only, the 6 gaps, refactoring principles |
| Chunk 1: Checkpoint Enforcement | `docs/generated/sprint-cli/v3.7-refactor/chunk-01-checkpoint-enforcement.md` | Per-task checkpoint analysis, Wave 1-4 path applicability |
| Chunk 2: Sprint TUI v2 | `docs/generated/sprint-cli/v3.7-refactor/chunk-02-sprint-tui-v2.md` | F1-F10 per-feature path applicability, OutputMonitor architecture, Strategy A vs B |
| Chunk 3: Naming Consolidation | `docs/generated/sprint-cli/v3.7-refactor/chunk-03-naming-consolidation.md` | N1-N12 path applicability, verdict that Path A should NOT invoke /sc:task |
| Chunk 4: Data Model Changes | `docs/generated/sprint-cli/v3.7-refactor/chunk-04-data-model-changes.md` | Section 7 per-change analysis, the three zeroing bugs, token extraction design |
| Chunk 5: Cross-Cutting Concerns | `docs/generated/sprint-cli/v3.7-refactor/chunk-05-cross-cutting.md` | Revised Sections 5/6/14, new dependency domains, implementation order insertion |
| Chunk 6: Path A Enrichment | `docs/generated/sprint-cli/v3.7-refactor/chunk-06-path-a-enrichment.md` | PA-01 through PA-08 implementation details, code sketches, step-by-step instructions |
| Monitor Adaptation Debates | `docs/generated/sprint-cli/v3.7-refactor/debates-monitor-adaptation.md` | Strategy B wins 6-1-1, append-mode compromise, shared MonitorState ruling |
| Monitor Design Document | `docs/generated/sprint-cli/v3.7-refactor/design-monitor-per-task.md` | Strategy A/B/C comparison, MonitorState field reference, current data flow diagrams |
| Debate: Split vs Re-Split | `docs/generated/sprint-cli/v3.7-refactor/debate-split-vs-resplit.md` | Option C (Hybrid) wins: complete analysis then partition |
| Incremental Fidelity Validation | `docs/generated/sprint-cli/v3.7-refactor/incremental-fidelity-validation.md` | R1/R2 gap analysis, what sections NEED ADDITION/MODIFICATION |
| Partition Validation Audit | `docs/generated/sprint-cli/v3.7-refactor/partition-validation-audit.md` | Zero-trust verification: 11/11 new tasks present, 15/15 modified tasks present |

---

## KEY DECISIONS (already validated -- do not re-debate)

These decisions were reached through adversarial debate with convergence scores. Incorporate them as settled facts.

1. **Strategy B (synthetic MonitorState population)** for Path A TUI integration. NOT per-task OutputMonitor. Convergence 87.5%. Reason: blocking subprocess at `executor.py:1086-1087` (`proc.wait()`) makes real-time TUI structurally unreachable without architectural changes not in scope.

2. **Append mode** (`process.py:114` change `"w"` to `"a"`) for output file. NOT per-task output files. Convergence 88.9%. Per-task output files deferred to v3.8.

3. **Shared MonitorState** as the interface between Path A data and TUI. NOT path-specific data structures. Convergence 85%. The adapter pattern (`TaskResult` -> `MonitorState` fields) keeps TUI code path-agnostic.

4. **`stall_status` fix**: `MonitorState` must track `stall_status` per-task under Path A. Between tasks, status resets. The TUI reads this field for the activity indicator.

5. **`gate_rollout_mode` default**: `"off"` -> `"shadow"` (PA-06). Shadow mode logs metrics but does not block. Promotion to `"soft"` is a separate decision for v3.8.

6. **Path A should NOT invoke `/sc:task`**. The skill protocol was designed for Path B's single-subprocess architecture. Three lightweight prompt enrichments (block extraction, scope boundary, sprint context) achieve the same quality goals at ~280 tokens instead of ~2,000-4,000.

---

## R1 TASK INVENTORY (v3.7a -- Pipeline Reliability)

### Phase 0: Path A Bug Fixes + Block Extraction (all independent, parallelizable)

| Task | Description | LOC | File(s) | Line Range |
|------|-------------|-----|---------|------------|
| PA-04 | Fix `turns_consumed` to call `count_turns_from_output()` | ~3 | `executor.py` | 1091-1092 |
| PA-05 | Wire `TaskResult.output_path = str(config.output_file(phase))` | ~1 | `executor.py` | 1017-1025 |
| PA-01 | Implement `_extract_task_block()` and wire into per-task prompt | ~30 | `executor.py` (1064-1068), `config.py` (alongside `parse_tasklist`) | |

### Phase 0.5: Prompt Enrichment + Token Infrastructure (depends on Phase 0)

| Task | Description | LOC | File(s) | Dependencies |
|------|-------------|-----|---------|-------------|
| PA-02 | Add scope boundary to per-task prompt | ~5 | `executor.py` (1064-1068) | PA-01 |
| PA-03 | Add sprint context header (shared `build_sprint_context_header()`) | ~25 added, ~15 modified | `executor.py`, `process.py` | PA-01 |
| PA-06 | Change `gate_rollout_mode` default `"off"` -> `"shadow"` | ~1 | `models.py` (line 329) | PA-04, PA-05 |
| DM-04 | Implement `extract_token_usage()` in `monitor.py` | ~25 | `monitor.py` | None |
| DM-05 | Add `tokens_in`/`tokens_out` to `TaskResult`, wire extraction | ~5 | `models.py`, `executor.py` | DM-04 |

### Phase 0.75: Append Mode Fix

| Task | Description | LOC | File(s) | Dependencies |
|------|-------------|-----|---------|-------------|
| MA-03 | Change output file open mode `"w"` -> `"a"` at `process.py:114` | ~1 | `process.py` | None (independent) |

### Phase 1: Naming Consolidation (N1-N12, parallelizable with Phase 0)

All 12 mechanical rename tasks from the original spec. These are file/directory renames, frontmatter updates, cross-reference updates, and the `process.py:170` prompt string rename. No runtime behavior changes.

### Phases 2-4: Checkpoint Enforcement Waves 1-3

Original spec tasks T01.01, T01.02, T02.01-T02.05, T03.01-T03.06, with the following modifications:
- T02.04: Reframed as PRIMARY defense for Path A (add documentation note)
- T02.05: Extended unit tests to cover Path A `TaskResult` accumulation flow
- T04.01: Add Path A impact note (checkpoint becomes regular task in Path A loop)

---

## R2 TASK INVENTORY (v3.7b -- Sprint TUI v2)

### Wave 1: Data Model + Monitor Adaptation

| Task | Description | LOC | Dependencies (R1) |
|------|-------------|-----|--------------------|
| 7.1 | 8 new MonitorState fields, Path A population via synthetic adapter | ~40 | PA-04, PA-05 (R1 data contracts) |
| 7.2 | PhaseResult.turns/tokens_in/tokens_out, Path A aggregation | ~15 | PA-04, DM-05 (R1 data contracts) |
| DM-06 | Path A aggregation: `TaskResult` list -> `PhaseResult` fields | ~10 | PA-04, PA-05, DM-05 (all R1) |
| 7.3 | SprintResult aggregate properties | ~20 | 7.2 |
| 7.4 | SprintConfig.total_tasks, checkpoint_gate_mode | ~10 | None |
| 7.5 | PhaseStatus.PASS_MISSING_CHECKPOINT display integration | ~5 | R1 checkpoint W2 |

### Wave 2: TUI Rendering (F1-F7)

| Task | Description | Path A Adaptation |
|------|-------------|-------------------|
| F7 | Sprint name in TUI title | None (reads SprintConfig.release_name) |
| F3 | Task-level progress bar | 2-line change: `total_tasks_in_phase = len(tasks)`, `completed_task_estimate = i+1` |
| F2 | Enhanced phase table (turns/output columns) | Wire MonitorState.turns from accumulated TaskResult |
| F6 | Enhanced terminal panels | Aggregate from TaskResult list post-phase |
| F4 | Conditional error panel | Task-level errors from TaskResult.status + exit_code |
| F1 | Activity stream | Synthetic entries per completed task (Strategy B) |

### Wave 3: Summary Infrastructure (F8-F10)

| Task | Description |
|------|-------------|
| F8 | PhaseSummarizer accepts `list[TaskResult]` OR NDJSON path |
| F9 | Tmux summary pane (depends on F8) |
| F10 | Release retrospective (depends on F8) |

### Wave 4: Deferred / Lower Priority

| Task | Description |
|------|-------------|
| F5 | LLM context lines (Path B only in v3.7) |
| 7.7 | SprintTUI.latest_summary_notification |

---

## MANDATORY SPEC REQUIREMENTS

### Requirement 1: Atomic Commit Boundaries (Section 4.6)

For EACH task in Section 4.6 (Implementation Order), you MUST provide all of the following. This is the most important section of each spec. A task entry that lacks any of these fields is incomplete.

```markdown
#### Task [ID]: [Title]

**Commit boundary**: What goes into this commit and what does NOT. Be explicit about what is excluded even if it seems obvious. Example: "This commit adds the `_extract_task_block()` function and its call site. It does NOT modify the prompt string itself -- that is PA-02."

**Git diff footprint**:
- `src/superclaude/cli/sprint/executor.py`: lines [N-M] (function `X`)
- `src/superclaude/cli/sprint/config.py`: lines [N-M] (new function after `parse_tasklist`)

**Test commands that MUST pass after this commit**:
```bash
uv run pytest tests/ -x -q                           # full suite green
uv run pytest tests/path/to/specific_test.py -v      # new/modified tests
uv run pytest -k "test_name_pattern" -v               # targeted validation
```

**Depends on commits**: [list of task IDs that must be committed first, or "None"]

**Blocks commits**: [list of task IDs that cannot be committed until this lands]

**Broader impact analysis**:
- Callers of modified functions: [list every function/method that calls the function you are changing, with file:line references]
- Tests that import modified modules: [list every test file that imports from the module you are changing]
- Downstream behavior assumptions: [does any consumer assume the old behavior? Example: "Anti-instinct gate at executor.py:826-831 assumes output_path is empty string -- after PA-05, it will be a real path, causing the gate to actually evaluate"]
- Config/CLI default changes: [does this change any default that users may depend on?]

**Rejected approaches** (for non-trivial tasks only):
| Approach | LOC | Risk | Why Rejected |
|----------|-----|------|-------------|
| [Alternative 1] | ~N | [level] | [reason] |
| [Alternative 2] | ~N | [level] | [reason] |

**Selected approach**: [name]
**Rationale**: [why this approach over the alternatives]
```

### Requirement 2: Candidate Approach Analysis (Section 2)

For each task that involves a design choice (not mechanical renames or 1-line fixes), Section 2.1 (Key Design Decisions) must present 2-3 candidate approaches with:
- Estimated LOC for each
- Risk assessment (interaction effects with other tasks in the same spec and the OTHER spec)
- Test surface (what new tests each approach requires)
- The selected approach with explicit rationale
- What the REJECTED approaches would have looked like (enough detail that someone could implement them if the selection proves wrong)

Tasks that are mechanical (N1-N12 renames, 1-line default changes) do not need candidate analysis. Flag them as "mechanical -- no design choice."

### Requirement 3: Broader Impact Analysis

For EVERY task (including mechanical ones), grep the codebase and document:
1. All callers of every modified function (with `file:line` references)
2. All test files that import from modified modules
3. Whether any downstream consumer assumes the old behavior
4. Whether any config flag or CLI default changes observable behavior

This analysis must be specific enough that a reviewer can verify it by running the same grep commands. Include the grep patterns used.

### Requirement 4: Section 2.2 Data Flow Diagrams

Include THREE ASCII diagrams in Section 2.2:

**Diagram A -- Current State (with bugs)**:
Show Path A's data flow from `execute_phase_tasks` through `_run_task_subprocess` to `TaskResult` to `PhaseResult`, highlighting where `turns_consumed=0`, `output_path=""`, and `gate_rollout_mode="off"` break the chain. Show the output file overwrite (`"w"` mode). Show the MonitorState dead fields.

**Diagram B -- After R1 (bugs fixed, prompts enriched)**:
Same flow but with PA-04/05/06 fixes active, append mode, enriched prompts. Show that MonitorState fields are still dead (R2 has not landed). Show that gate evaluates in shadow mode.

**Diagram C -- After R2 (TUI integrated)**:
Full flow with synthetic MonitorState population, TUI rendering, PhaseSummarizer dual-input, tmux summary pane. Show the Strategy B adapter converting TaskResult data into MonitorState fields.

### Requirement 5: Section 9 (Migration & Rollout)

**For R1**:
- `gate_rollout_mode` changes from `"off"` to `"shadow"`. Document: What happens to in-flight sprints that have already started with `"off"` default? Answer: The mode is read from `SprintConfig` at sprint start, not per-phase. A sprint started before R1 will continue with `"off"` until restarted. Document this explicitly.
- Append mode (`"w"` -> `"a"`): What happens to existing phase output files if a sprint is resumed after R1 lands? The file will be appended to instead of truncated. If the file contains partial NDJSON from a pre-R1 run, the new output will be concatenated. Document whether `count_turns_from_output()` handles mixed content gracefully.
- `_extract_task_block()`: What happens if the phase file does not contain a matching `### T<PP>.<TT>` heading? Document the fallback behavior (return empty string, prompt falls back to description-only).

**For R2**:
- MonitorState new fields: If R2 code runs against data from a pre-R1 sprint (where `turns_consumed=0` and `output_path=""`), what does the TUI display? All synthetic fields will show zeros/defaults. Document that this is acceptable degraded behavior, not a crash.
- `PhaseSummarizer` dual-input: What happens if both `list[TaskResult]` AND NDJSON path are provided? Document the precedence rule: `list[TaskResult]` takes priority when present (Path A); NDJSON path is used when TaskResult list is empty (Path B).
- F8/F9/F10 tmux integration: What happens if tmux is not installed? Document graceful degradation (summary written to file only, no pane created).

### Requirement 6: Section 8 (Test Plan) Specificity

For each test listed in Section 8.1 or 8.2, include:
- The exact test function name
- The exact test file path
- What it validates (input -> expected output)
- Which task it traces to

Do not write "test that X works" without specifying the test function name and file.

### Requirement 7: Cross-Release Integration Points (both specs)

Both specs must include a section documenting the 10 cross-release integration points from the partition document's "R1 Provides -> R2 Consumes" table. Each integration point must state:
- What R1 provides (field, function, config value)
- What R2 consumes (which feature, which code path)
- Integration type (enum value, code location, data field, configuration, indirect)
- How to verify the integration works (test command or manual check)

---

## FORMAT REQUIREMENTS

1. Follow `src/superclaude/examples/release-spec-template.md` section structure EXACTLY. Every section must be present. Mark conditional sections with the appropriate `[CONDITIONAL: refactoring]` tag.
2. Fill ALL `{{SC_PLACEHOLDER:*}}` sentinels. Run `grep -c '{{SC_PLACEHOLDER:' <output-file>` at the end -- result must be 0.
3. YAML frontmatter must include all fields from the template.
4. Use the task IDs from the source documents (PA-01, PA-02, DM-04, N1-N12, F1-F10, T01.01, etc.). Do not invent new IDs.
5. Quality scores should reflect honest self-assessment of the spec's completeness, not aspirational values.

---

## ANTI-PATTERNS TO AVOID

1. **"Read the codebase to understand"** -- Every task must contain enough context that the implementer does not need to explore. Include line numbers, function signatures, and data flow descriptions.
2. **"This task is straightforward"** -- Even 1-line changes (PA-05, PA-06, MA-03) need broader impact analysis. A 1-line default change can activate a dormant code path.
3. **"Tests TBD"** -- Every task must have specific test commands listed. If new tests are needed, specify the test function name and what it validates.
4. **Implicit dependency chains** -- If task B reads a field that task A adds, state this explicitly. "Depends on PA-04" is not enough; say "Depends on PA-04 because this task reads `TaskResult.turns_consumed` which is hardcoded to 0 until PA-04 lands."
5. **Missing rejected approaches** -- For any task with a design choice, the spec must document what was NOT chosen and why. This prevents future engineers from re-discovering and re-debating settled questions.
6. **Overwriting validated decisions** -- The adversarial debates produced binding rulings. Do not present Strategy A (per-task OutputMonitor) as a viable option for v3.7. Do not propose `/sc:task` invocation for Path A. Do not propose per-task output files for v3.7. These are deferred to v3.8 with documented rationale.

---

## OUTPUT

Write two files:
1. `R1-v3.7a-pipeline-reliability-spec.md`
2. `R2-v3.7b-sprint-tui-v2-spec.md`

Each file must be self-contained (readable without the other) but must cross-reference the other where integration points exist. R2 must list its R1 prerequisites explicitly in Section 4.6 with commit hashes or task IDs.

After writing both specs, perform these self-checks:
1. `grep -c '{{SC_PLACEHOLDER:' R1-*.md` returns 0
2. `grep -c '{{SC_PLACEHOLDER:' R2-*.md` returns 0
3. Every task in R1's Phase 0/1 appears in R2's prerequisites section
4. Every cross-release integration point from the partition document appears in both specs
5. Every task in Section 4.6 has: commit boundary, git diff footprint, test commands, depends-on, blocks, broader impact analysis
6. Section 9 addresses all three R1 migration scenarios and all three R2 migration scenarios listed above
7. Section 2.2 contains exactly three ASCII diagrams (current/after-R1/after-R2)
