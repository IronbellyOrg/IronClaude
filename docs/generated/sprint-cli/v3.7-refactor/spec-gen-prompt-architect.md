# Spec Generation Prompt -- Architecture-First v3.7a/v3.7b

> **Purpose**: Paste this prompt into a fresh Claude session with access to the IronClaude repository. It will produce two complete release spec documents following the template at `src/superclaude/examples/release-spec-template.md`.
>
> **Generated**: 2026-04-03
> **Persona**: System Architect (structural analysis, impact tracing, implementation ranking)

---

## PROMPT START

You are producing TWO release specification documents for the SuperClaude Sprint CLI. Each spec MUST follow the template structure at `src/superclaude/examples/release-spec-template.md` exactly -- every section, every table, zero remaining `{{SC_PLACEHOLDER:*}}` sentinels. The spec type for both is `refactoring`.

Before writing ANY implementation detail, you MUST read the actual source code for every file you reference. Do not guess at line numbers, function signatures, or variable names. Every before/after code snippet must be verifiable against the current codebase.

### OUTPUT FILES

1. **R1**: `.dev/releases/backlog/v3.7-task-unified-v2/release-split/v3.7a-pipeline-reliability-SPEC.md`
2. **R2**: `.dev/releases/backlog/v3.7-task-unified-v2/release-split/v3.7b-sprint-tui-v2-SPEC.md`

---

## PART 1: CONTEXT YOU MUST INTERNALIZE

### 1.1 The Two Releases

**R1 (v3.7a -- Pipeline Reliability and Naming, ~480 LOC)** makes the Sprint CLI pipeline deterministically reliable. It has five phases executed sequentially:

- **Phase 0 (Path A Bug Fixes + Data Foundations)**: PA-04 (fix hardcoded `turns_consumed=0` at executor.py:1091), PA-05 (wire `TaskResult.output_path` at executor.py:1017), PA-01 (extract per-task markdown block via `_extract_task_block()`), PA-02 (scope boundary in prompt), PA-03 (shared `build_sprint_context_header()`), PA-06 (change `gate_rollout_mode` default from `"off"` to `"shadow"` at models.py), DM-04 (implement `extract_token_usage()` in monitor.py), DM-05 (add `tokens_in`/`tokens_out` to TaskResult and wire extraction), MA-03 (append-mode fix: process.py:114 `"w"` to `"a"`)
- **Phase 1 (Naming Consolidation)**: N1-N12. Delete deprecated `task.md`, rename `task-unified.md` to `task.md`, rename skill directory `sc-task-unified-protocol/` to `sc-task-protocol/`, update all cross-references (~21 files). Dependency chain: N1 then N2 then N3 then N4 then N5+N6 parallel then N7+N8+N9+N10 parallel then N11 then N12.
- **Phase 2 (Checkpoint W1 -- Prompt Prevention)**: T01.01 (add `## Checkpoints` section to `build_prompt()` in process.py), T01.02 (add `_warn_missing_checkpoints()` helper to executor.py)
- **Phase 3 (Checkpoint W2 -- Detection Gate)**: T02.01-T02.05. Create `checkpoints.py`, add `PASS_MISSING_CHECKPOINT` to `PhaseStatus`, add `checkpoint_gate_mode` to `SprintConfig`, wire `_verify_checkpoints()` into executor.py post-phase flow.
- **Phase 4 (Checkpoint W3 -- Manifest, Recovery, CLI)**: T03.01-T03.06. `CheckpointEntry` dataclass, `build_manifest()`, `recover_missing_checkpoints()`, `verify-checkpoints` CLI subcommand.

**R2 (v3.7b -- Sprint TUI v2, ~800 LOC)** makes the pipeline visible. It has four waves:

- **Wave 1 (Data Infrastructure)**: MonitorState gets 8 new fields (activity_log, turns, errors, last_assistant_text, total_tasks_in_phase, completed_task_estimate, tokens_in, tokens_out). PhaseResult gets 3 fields (turns, tokens_in, tokens_out). SprintResult gets 5 computed properties. SprintConfig gets `total_tasks`. PhaseAccumulator class bridges TaskResult lists to MonitorState interface. DM-06 aggregation logic.
- **Wave 2 (TUI Rendering, F1-F7)**: Activity stream (3-line FIFO), enhanced phase table (Turns/Output columns replace Tasks), dual progress bar, conditional error panel, LLM context lines, enhanced terminal panels, sprint name in title.
- **Wave 3 (Summary Infrastructure, F8+F10)**: PhaseSummarizer with dual input (TaskResult list OR NDJSON), SummaryWorker daemon thread pool, Haiku narrative pipeline (claude --print --model claude-haiku-4-5), ReleaseRetrospective generator. F8 accepts `list[TaskResult]` as alternative to NDJSON path.
- **Wave 4 (Tmux Integration, F9)**: 3-pane layout (TUI 50% + summary 25% + tail 25%), summary pane updates via `tmux send-keys`, pane index shift from `:0.1` to `:0.2`.

### 1.2 Key Design Decisions (MUST appear in Section 2.1 of both specs)

These decisions were made through adversarial debate and are FINAL. Do not re-evaluate them. Document them as settled rulings.

**Decision 1: Strategy B (Synthetic MonitorState) over Strategy A (Per-Task OutputMonitor)**
- The blocking subprocess architecture (`proc.start()` then `proc.wait()` at executor.py:1086-1087) makes real-time TUI updates structurally unreachable without a non-blocking rewrite not in scope.
- Strategy B uses a PhaseAccumulator that builds MonitorState from completed TaskResult data between tasks. Same update cadence as Strategy A under blocking arch, but 45 LOC vs 103 LOC and zero downstream adaptation sites.
- Strategy A deferred to v3.8 when non-blocking subprocess is considered.

**Decision 2: Append-Mode Fix over Per-Task Output Files**
- `process.py:114` opens the output file with `"w"` (truncate). In multi-task phases, each task overwrites the previous task's NDJSON. 90% of data is silently destroyed.
- Fix: change `"w"` to `"a"` (append). 1 LOC. Preserves all tasks' NDJSON in the phase file. Zero downstream consumer changes. `count_turns_from_output()` sees all tasks.
- Per-task output files deferred to v3.8 (requires naming convention, downstream audit, aggregation shim).

**Decision 3: PhaseAccumulator.to_monitor_state() Adapter**
- Shared MonitorState interface used by TUI regardless of execution path.
- Path B populates MonitorState via OutputMonitor (live NDJSON parsing).
- Path A populates MonitorState via PhaseAccumulator (post-task TaskResult aggregation).
- The adapter MUST set `last_event_time = time.monotonic()` to suppress false STALLED alarms from the TUI's staleness detector.

**Decision 4: R1 provides data contracts that R2 consumes (one-directional dependency)**
- R1 -> R2, never reverse. R1 delivers: correct `turns_consumed` (PA-04), valid `output_path` (PA-05), `tokens_in`/`tokens_out` on TaskResult (DM-04/05), `PhaseStatus.PASS_MISSING_CHECKPOINT`, post-phase hook site, append-mode output.
- R2 consumes these contracts for display. R2 never modifies process.py.

### 1.3 Cross-Release Integration Points

There are 10 integration points between R1 and R2. Document these in both specs:

1. `executor.py` post-phase hook ordering: `_verify_checkpoints()` (R1) then `summary_worker.submit()` (R2) then manifest update (R1)
2. `PhaseStatus.PASS_MISSING_CHECKPOINT` enum (R1) consumed by TUI STATUS_STYLES/STATUS_ICONS dicts (R2)
3. `models.py` dataclass coexistence: R1 adds CheckpointEntry + checkpoint_gate_mode; R2 adds MonitorState fields + PhaseResult fields + SprintResult properties
4. `process.py` ownership: R1 modifies (naming + checkpoint prompt + append-mode); R2 does not touch
5. `TaskResult.output_path` (R1 PA-05) consumed by R2 F8 PhaseSummarizer
6. `TaskResult.turns_consumed` (R1 PA-04) consumed by R2 F2/F6 phase table and terminal panels
7. `TaskResult.tokens_in/tokens_out` (R1 DM-04/05) consumed by R2 F2/F6 and DM-06 aggregation
8. `_extract_task_block()` (R1 PA-01) enriches NDJSON output that R2 F1/F4 consume (indirect)
9. `gate_rollout_mode="shadow"` (R1 PA-06) makes R2 gate column display meaningful
10. Append-mode output (R1 MA-03) lets R2 F8 see all tasks' output

### 1.4 Source Code You MUST Read Before Writing

Read these files in their entirety. Your spec must reference actual line numbers from the current code:

| File | Key Areas |
|------|-----------|
| `src/superclaude/cli/sprint/executor.py` | Lines 1064-1092 (_run_task_subprocess: prompt, output file, hardcoded turns=0), lines 1017-1025 (TaskResult construction missing output_path), lines 1042-1048 (per-task TUI update hook), lines 1086-1087 (blocking proc.start/wait) |
| `src/superclaude/cli/sprint/process.py` | Lines 123-204 (build_prompt with sprint context, skill invocation), line 170 (/sc:task-unified reference) |
| `src/superclaude/cli/sprint/monitor.py` | Lines 114-141 (count_turns_from_output), class OutputMonitor (lifecycle, _parse_event) |
| `src/superclaude/cli/sprint/models.py` | TaskResult (output_path field), PhaseResult, SprintResult, MonitorState, SprintConfig (gate_rollout_mode at ~line 329), PhaseStatus enum |
| `src/superclaude/cli/sprint/tui.py` | STATUS_STYLES, STATUS_ICONS, phase table rendering, terminal panel rendering |
| `src/superclaude/cli/sprint/config.py` | parse_tasklist(), _TASK_HEADING_RE |
| `src/superclaude/cli/pipeline/process.py` | Line 114 (output file open mode "w" -- the append-mode bug) |

### 1.5 Reference Documents (Read for context, not for code)

| Document | Contains |
|----------|----------|
| `docs/generated/sprint-cli/v3.7-refactor/MERGED-REFACTORING-RECOMMENDATION.md` | Unified analysis of all 6 chunks. Task lists, scope, implementation order. |
| `docs/generated/sprint-cli/v3.7-refactor/chunk-06-path-a-enrichment.md` | PA-01 through PA-08 detailed specs with before/after code, acceptance criteria, rollback plans |
| `docs/generated/sprint-cli/v3.7-refactor/chunk-04-data-model-changes.md` | DM-04 through DM-06 specs, three-bug analysis, MonitorState field applicability |
| `docs/generated/sprint-cli/v3.7-refactor/debates-monitor-adaptation.md` | 3 adversarial debates: Strategy A vs B (B wins 6-1-1), per-task output files (append-mode wins), MonitorState as shared interface (PhaseAccumulator wins) |
| `docs/generated/sprint-cli/v3.7-refactor/path-a-partition-document.md` | Task-to-release assignment with boundary justifications, 10 cross-release integration points |
| `.dev/releases/backlog/v3.7-task-unified-v2/release-split/boundary-rationale.md` | Split rationale: pipeline infrastructure vs presentation layer |
| `.dev/releases/backlog/v3.7-task-unified-v2/release-split/release-1-spec.md` | Current R1 draft (checkpoint + naming scope) |
| `.dev/releases/backlog/v3.7-task-unified-v2/release-split/release-2-spec.md` | Current R2 draft (TUI v2 scope) |
| `.dev/releases/backlog/v3.7-task-unified-v2/artifacts/tasklist-checkpoint-enforcement.md` | Existing MDTM tasklist for checkpoint waves |

---

## PART 2: WHAT YOU MUST PRODUCE FOR EACH TASK

For EVERY task in both specs (PA-01 through PA-06, DM-04, DM-05, MA-03, N1-N12, T01.01-T01.02, T02.01-T02.05, T03.01-T03.06 for R1; MonitorState fields, PhaseResult fields, SprintResult properties, PhaseAccumulator, DM-06, F1-F7, F8, F10, F9, STATUS_STYLES/ICONS for R2), you must provide:

### 2.1 Deep Code Reading (do this BEFORE writing)

Read the actual source file. Identify:
- The exact function or class being modified
- The exact line numbers in the current code
- What other functions CALL the code being changed (grep for callers)
- What tests REFERENCE the code being changed (grep test files)

### 2.2 Before/After Code Snippets

Show the EXACT current code and the EXACT proposed replacement. Not pseudocode. Not summaries. Actual Python with correct indentation, imports, and variable names matching the codebase.

### 2.3 Impact Analysis

For each change, answer:
- What functions call the changed function? List them with file:line references.
- What tests exercise the changed code? List them with file:line references.
- Does this change alter any function signature? If yes, what callers must be updated?
- Does this change introduce a new import? If yes, is there a circular dependency risk?
- Does this change affect serialization/deserialization (e.g., JSONL events, dataclass fields)?

### 2.4 Implementation Approach Evaluation

For non-trivial tasks (anything over 10 LOC), evaluate at least 2 implementation approaches:
- **Approach A**: Description, LOC estimate, risk level, downstream impact
- **Approach B**: Description, LOC estimate, risk level, downstream impact
- **Selected**: Which and why (with reference to debate rulings where applicable)

### 2.5 Unintended Consequence Analysis

Think through:
- Could this change cause a test to fail that is NOT testing the changed behavior? (e.g., a test that asserts on the exact prompt string would break if prompt content changes)
- Could this change cause a runtime error in a code path not covered by tests? (e.g., Path B exercising a shared function that Path A modified)
- Could this change interact badly with concurrent execution? (e.g., append-mode and OutputMonitor both writing/reading the same file)

### 2.6 Verification Commands

Provide TESTED verification commands. Not generic "run the tests." Specific commands:
```bash
uv run pytest tests/sprint/test_executor.py::TestRunTaskSubprocess -v
uv run pytest tests/sprint/test_checkpoints.py -v
grep -rn "sc:task-unified" src/superclaude/ --include="*.py" --include="*.md" | wc -l  # expect 0
```

### 2.7 Rollback Plan

Specific to each task. Not "revert the commit." State exactly which lines to change and what to change them to. If the task creates a new file, state "delete file X." If the task modifies a dataclass, state which field to remove and whether any migration is needed.

---

## PART 3: TEMPLATE COMPLIANCE

Fill in ALL sections from the template. Here is the mapping:

### Section 1: Problem Statement
- R1: Sprint pipeline has three classes of reliability defects -- hardcoded zeros in telemetry (PA-04/05/06 bugs), absent checkpoint enforcement, and naming collisions. Evidence: OntRAG R0+R1 missing Phase 3 checkpoints discovered 24h late; `turns_consumed` returns 0 for every production sprint; 3 naming variants create command resolution ambiguity.
- R2: Sprint execution produces no real-time operator visibility. Turns, tokens, errors, and activity are invisible until log inspection. No post-phase summary. No retrospective. Evidence: operators must manually grep NDJSON after sprint completion; error detection latency is "end of phase" (could be 30+ minutes).

### Section 1.1: Evidence
Provide concrete evidence table. For R1: link to executor.py:1091 (hardcoded 0), executor.py:1017-1025 (missing output_path), models.py:329 (gate default "off"), process.py:114 ("w" mode). For R2: describe current TUI limitations by reading tui.py.

### Section 1.2: Scope Boundary
- R1 IN: PA-01-06, DM-04-05, MA-03, N1-N12, T01-T03 waves
- R1 OUT: TUI rendering, MonitorState population, summarizer, retrospective, tmux
- R2 IN: MonitorState fields, PhaseAccumulator, DM-06, F1-F10, tmux 3-pane
- R2 OUT: Checkpoint enforcement, naming, non-blocking subprocess rewrite

### Section 2: Solution Overview
Describe the layered approach. R1 is foundation (data contracts + enforcement). R2 is presentation (rendering + summaries).

### Section 2.1: Key Design Decisions
Use the 4 decisions from Section 1.2 of this prompt. Format as the template's table.

### Section 2.2: Workflow / Data Flow
Draw ASCII diagrams showing:
- R1: Task execution flow with enriched prompt, turn counting, token extraction, gate evaluation
- R2: Data flow from TaskResult through PhaseAccumulator to MonitorState to TUI rendering

### Section 3: Functional Requirements
Each task becomes an FR. Use FR-R1.01 through FR-R1.xx for R1, FR-R2.01 through FR-R2.xx for R2. Each FR must have acceptance criteria (as checkboxes) and dependencies.

### Section 4: Architecture
- 4.1 New Files: R1 creates `checkpoints.py`. R2 creates `summarizer.py`, `retrospective.py`.
- 4.2 Modified Files: List every file with nature of change.
- 4.3 Removed Files: R1 removes deprecated `task.md`, renames `task-unified.md`.
- 4.4 Module Dependency Graph: ASCII diagram of sprint module dependencies after changes.
- 4.5 Data Models: Show the new/modified dataclasses with field definitions. Include PhaseAccumulator for R2.
- 4.6 Implementation Order: Use the phase/wave structure from Part 1 of this prompt. Show parallelization opportunities within each phase/wave. This is critical -- tasks within a phase that can be executed in parallel MUST be marked as such.

### Section 5: Interface Contracts
Include CLI surface for R1 (`verify-checkpoints` subcommand). Include phase contracts for both (post-phase hook ordering).

### Section 6: Non-Functional Requirements
- Performance: append-mode must not degrade I/O. SummaryWorker must not block sprint execution. Haiku calls have 30s timeout.
- Reliability: summary failure must never affect sprint execution. All SummaryWorker exceptions caught.
- Thread safety: `SummaryWorker._summaries` guarded by `threading.Lock`.

### Section 7: Risk Assessment
Merge risk registers from the existing R1 and R2 drafts. Add risks for the new PA-01-06 and DM-04-05 tasks.

### Section 8: Test Plan
For each FR, specify unit tests and integration tests. Include file paths for new test files. Include the specific pytest commands to run each test group.

### Section 9: Migration and Rollout
- R1: Day 1 naming + Phase 0 bug fixes, Days 2-5 checkpoint W1+W2 (shadow mode), Days 5-10 checkpoint W3.
- R2: Blocked until R1 validation passes. Wave 1 first (data infra), Wave 2+3 parallel, Wave 4 last.
- Breaking changes: R1 naming change breaks `/sc:task-unified` references. R2 has no breaking changes.

### Section 10: Downstream Inputs
Describe how `sc:roadmap` and `sc:tasklist` consume each spec.

### Section 11: Open Items
Carry open questions from existing drafts. Resolve any that the code reading answers.

### Section 12: Brainstorm Gap Analysis
Identify any gaps between what the existing planning documents specify and what the code actually shows. Flag any tasks where the planning documents reference line numbers that have drifted.

### Appendix A: Glossary
Define: Path A, Path B, PhaseAccumulator, TurnLedger, NDJSON, MonitorState, shadow mode, gate rollout.

### Appendix B: Reference Documents
List all source documents from Section 1.5 of this prompt with relevance descriptions.

---

## PART 4: QUALITY GATES

Before declaring each spec complete:

1. **Zero sentinels**: `grep -c '{{SC_PLACEHOLDER:' <output-file>` returns 0
2. **All sections present**: Every numbered section from the template exists in the output
3. **Every task has before/after code**: No task is specified with only prose
4. **Every task has impact analysis**: No task is specified without caller/test tracing
5. **Every task has verification commands**: No task ends without a runnable pytest or grep command
6. **Every task has a rollback plan**: No task ends without specific revert instructions
7. **Cross-references are bidirectional**: Every R1 task that R2 depends on is marked as a dependency in R2's FR, and every R2 FR that consumes R1 data is listed in R1's downstream inputs
8. **Implementation order is acyclic**: No task depends on a task that comes after it in the implementation order
9. **Line numbers verified**: Every line number reference has been confirmed against the current source code (not copied from planning documents that may have drifted)

---

## EXECUTION INSTRUCTIONS

1. Read ALL source code files listed in Section 1.4. Do not skip any.
2. Read ALL reference documents listed in Section 1.5. Cross-reference task assignments against the partition document.
3. Write R1 spec first (it is the foundation).
4. Write R2 spec second (it consumes R1 contracts).
5. After writing each spec, run the quality gates from Part 4.
6. Use parallel tool calls wherever independent reads are possible (Wave strategy).

Begin.

## PROMPT END
