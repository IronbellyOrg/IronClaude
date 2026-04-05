# Spec Generation Prompt: Merged Adversarial (Architecture + QA + Incremental)

> **Purpose**: Paste this prompt into a fresh Claude session with access to the IronClaude repository. It will produce two complete release spec documents following the template at `src/superclaude/examples/release-spec-template.md`.
>
> **Generated**: 2026-04-03
> **Merge source**: Adversarial comparison of Architect (A), QA (B), and Incremental (C) variants
> **Core constraint**: Every task must be implementable as a single atomic commit that leaves the codebase in a passing state (`uv run pytest` green). No task may depend on uncommitted work from another task. Every intermediate state must be testable.

---

## PROMPT START

You are producing TWO release specification documents for the SuperClaude Sprint CLI. Each spec MUST follow the template structure at `src/superclaude/examples/release-spec-template.md` exactly -- every section, every table, zero remaining `{{SC_PLACEHOLDER:*}}` sentinels. The spec type for both is `refactoring`.

Before writing ANY implementation detail, you MUST read the actual source code for every file you reference. Do not guess at line numbers, function signatures, or variable names. Every before/after code snippet must be verifiable against the current codebase.

### OUTPUT FILES

1. **R1**: `.dev/releases/backlog/v3.7-task-unified-v2/release-split/v3.7a-pipeline-reliability-SPEC.md`
2. **R2**: `.dev/releases/backlog/v3.7-task-unified-v2/release-split/v3.7b-sprint-tui-v2-SPEC.md`

---

## 1. SOURCE DOCUMENTS (read all before writing)

You MUST read and incorporate ALL of the following source documents. They contain the validated decisions, adversarial rulings, dependency graphs, and task details that govern these specs. Do not invent tasks, change assignments, or override rulings.

### 1.1 Source Code (ground truth -- read FIRST)

| File | Key Areas |
|------|-----------|
| `src/superclaude/cli/sprint/executor.py` | Lines 1064-1092 (_run_task_subprocess: prompt, output file, hardcoded turns=0), lines 1017-1025 (TaskResult construction missing output_path), lines 1042-1048 (per-task TUI update hook), lines 1086-1087 (blocking proc.start/wait), lines 826-831 (anti-instinct gate), lines 956-1100 (Path A loop), lines 1201-1254 (path branching) |
| `src/superclaude/cli/sprint/process.py` | Lines 123-204 (build_prompt with sprint context, skill invocation), line 170 (/sc:task-unified reference), lines 245-307 (build_task_context) |
| `src/superclaude/cli/pipeline/process.py` | Line 114 (output file open mode "w" -- the append-mode bug) |
| `src/superclaude/cli/sprint/monitor.py` | Lines 114-141 (count_turns_from_output), class OutputMonitor (lifecycle, _parse_event) |
| `src/superclaude/cli/sprint/models.py` | TaskResult (output_path field), PhaseResult, SprintResult, MonitorState, SprintConfig (gate_rollout_mode at ~line 329), PhaseStatus enum, line 176 (output_path default) |
| `src/superclaude/cli/sprint/tui.py` | STATUS_STYLES, STATUS_ICONS, phase table rendering, terminal panel rendering, line 107-108 (monitor_state binding) |
| `src/superclaude/cli/sprint/config.py` | parse_tasklist(), _TASK_HEADING_RE, lines 342-380 (TaskEntry), lines 389-394 (dependencies) |

### 1.2 Analysis Documents

| Document | Path | Contains |
|----------|------|----------|
| Merged Refactoring Recommendation | `docs/generated/sprint-cli/v3.7-refactor/MERGED-REFACTORING-RECOMMENDATION.md` | Unified task list, implementation order, file impact matrix, dependency graph, risk register, LOC estimates |
| Path A Partition Document | `docs/generated/sprint-cli/v3.7-refactor/path-a-partition-document.md` | R1/R2 task assignments, cross-release integration points, hard/soft prerequisites, boundary justifications |
| Context 1: Path A Deficiencies | `docs/generated/sprint-cli/v3.7-refactor/context-01-path-a-deficiencies.md` | 7 validated deficiencies |
| Context 2: Debate Rulings | `docs/generated/sprint-cli/v3.7-refactor/context-02-debate-rulings.md` | 5 adversarial rulings |
| Context 3: Spec Gap Analysis | `docs/generated/sprint-cli/v3.7-refactor/context-03-v37-spec-gap-analysis.md` | Gap analysis, refactoring principles |
| Chunk 1: Checkpoint Enforcement | `docs/generated/sprint-cli/v3.7-refactor/chunk-01-checkpoint-enforcement.md` | Per-task checkpoint analysis, Wave 1-4 path applicability |
| Chunk 2: Sprint TUI v2 | `docs/generated/sprint-cli/v3.7-refactor/chunk-02-sprint-tui-v2.md` | F1-F10 per-feature path applicability, OutputMonitor architecture |
| Chunk 3: Naming Consolidation | `docs/generated/sprint-cli/v3.7-refactor/chunk-03-naming-consolidation.md` | N1-N12 path applicability, Path A should NOT invoke /sc:task |
| Chunk 4: Data Model Changes | `docs/generated/sprint-cli/v3.7-refactor/chunk-04-data-model-changes.md` | Section 7 per-change analysis, three zeroing bugs, token extraction design |
| Chunk 5: Cross-Cutting Concerns | `docs/generated/sprint-cli/v3.7-refactor/chunk-05-cross-cutting.md` | Revised Sections 5/6/14, new dependency domains |
| Chunk 6: Path A Enrichment | `docs/generated/sprint-cli/v3.7-refactor/chunk-06-path-a-enrichment.md` | PA-01 through PA-08 implementation details, code sketches, before/after snippets |
| Monitor Adaptation Debates | `docs/generated/sprint-cli/v3.7-refactor/debates-monitor-adaptation.md` | Strategy B wins 6-1-1, append-mode ruling, shared MonitorState ruling |
| Monitor Design Document | `docs/generated/sprint-cli/v3.7-refactor/design-monitor-per-task.md` | Strategy A/B/C comparison, MonitorState field reference, current data flow diagrams |
| Debate: Split vs Re-Split | `docs/generated/sprint-cli/v3.7-refactor/debate-split-vs-resplit.md` | Option C (Hybrid) wins |
| Incremental Fidelity Validation | `docs/generated/sprint-cli/v3.7-refactor/incremental-fidelity-validation.md` | R1/R2 gap analysis |
| Partition Validation Audit | `docs/generated/sprint-cli/v3.7-refactor/partition-validation-audit.md` | Zero-trust verification: 11/11 new tasks, 15/15 modified tasks present |
| Boundary Rationale | `.dev/releases/backlog/v3.7-task-unified-v2/release-split/boundary-rationale.md` | Split rationale: pipeline infrastructure vs presentation layer |
| Current R1 Draft | `.dev/releases/backlog/v3.7-task-unified-v2/release-split/release-1-spec.md` | Checkpoint + naming scope draft |
| Current R2 Draft | `.dev/releases/backlog/v3.7-task-unified-v2/release-split/release-2-spec.md` | TUI v2 scope draft |
| Checkpoint Tasklist | `.dev/releases/backlog/v3.7-task-unified-v2/artifacts/tasklist-checkpoint-enforcement.md` | Existing MDTM tasklist for checkpoint waves |

### 1.3 Verification Command Discipline

Before including ANY verification command in the spec (e.g., `uv run pytest ...`, `grep -c ...`), run the command yourself in the working directory to confirm it executes without error. If it fails, fix the command or note it as "requires implementation" rather than presenting a broken command as a test.

---

## 2. KEY DECISIONS (validated -- do not re-debate)

These decisions were reached through adversarial debate with convergence scores. Incorporate them as settled facts in Section 2.1 of both specs.

| Decision | Choice | Alternatives Rejected | Rationale | Source |
|----------|--------|----------------------|-----------|--------|
| Path A TUI strategy | Strategy B (synthetic MonitorState) | Strategy A (per-task OutputMonitor) | Blocking subprocess at executor.py:1086-1087 makes real-time TUI unreachable; B delivers same cadence at 45 LOC vs 103 LOC. Convergence 87.5% | debates-monitor-adaptation.md Debate 1 |
| Output file mode | Append ("a") within phase | Per-task files; keep "w" mode | 1 LOC fix, zero downstream consumer changes, preserves all NDJSON. Convergence 88.9% | debates-monitor-adaptation.md Debate 2 |
| MonitorState sharing | Shared MonitorState via PhaseAccumulator adapter | Path-specific data types | TUI has single data contract; adapter is ~10 LOC; zero TUI changes on v3.8 migration. Convergence 85% | debates-monitor-adaptation.md Debate 3 |
| stall_status fix | Adapter sets `last_event_time = monotonic()` | Modify MonitorState.stall_status property | Fix in adapter, not in shared class; Path B unaffected | debates-monitor-adaptation.md Debate 3 |
| Per-task prompt enrichment | Extract task block + scope boundary + sprint context | Full `@{phase_file}` preload; result file contract; stop-on-STRICT-fail | 3 of 5 proposed additions validated via adversarial debate | context-02-debate-rulings.md |
| Release split boundary | R1 = data contracts/pipeline, R2 = presentation | Single release; three-way split | Boundary validated at 0.83 convergence | debate-split-vs-resplit.md Option C |
| gate_rollout_mode default | `"off"` -> `"shadow"` (PA-06) | Keep "off"; go straight to "soft" | Shadow logs but does not block; promotion to "soft" is v3.8 | path-a-partition-document.md |
| Path A and /sc:task | Path A should NOT invoke /sc:task | Invoke /sc:task per task | Skill protocol designed for Path B single-subprocess architecture; 3 lightweight enrichments achieve same quality at ~280 tokens vs ~2,000-4,000 | chunk-03-naming-consolidation.md |
| Deferred items | PA-07, PA-08 to v3.8 | Include in R1 | 75% confidence (below 90% threshold); behind config flags; evaluate after shadow-mode data | path-a-partition-document.md |

---

## 3. R1 TASK INVENTORY (v3.7a -- Pipeline Reliability & Naming, ~480 LOC)

### Phase 0: Path A Bug Fixes + Block Extraction (all independent, parallelizable)

| Task | Description | LOC | File(s) | Line Range |
|------|-------------|-----|---------|------------|
| PA-04 | Fix `turns_consumed` to call `count_turns_from_output()` | ~3 | `executor.py` | 1091-1092 |
| PA-05 | Wire `TaskResult.output_path = str(config.output_file(phase))` | ~1 | `executor.py` | 1017-1025 |
| PA-01 | Implement `_extract_task_block()` and wire into per-task prompt | ~30 | `executor.py` (1064-1068), `config.py` | |
| DM-04 | Implement `extract_token_usage()` in `monitor.py` | ~25 | `monitor.py` | |
| MA-03 | Append-mode fix: `process.py:114` change `"w"` to `"a"` | ~1 | `pipeline/process.py` | 114 |

### Phase 0.5: Prompt Enrichment + Token Infrastructure (depends on Phase 0)

| Task | Description | LOC | File(s) | Dependencies |
|------|-------------|-----|---------|-------------|
| PA-02 | Add scope boundary to per-task prompt | ~5 | `executor.py` (1064-1068) | PA-01 |
| PA-03 | Add sprint context header (shared `build_sprint_context_header()`) | ~25 added, ~15 modified | `executor.py`, `process.py` | PA-01 |
| PA-06 | Change `gate_rollout_mode` default `"off"` -> `"shadow"` | ~1 | `models.py` (line 329) | PA-04, PA-05 |
| DM-05 | Add `tokens_in`/`tokens_out` to `TaskResult`, wire extraction | ~5 | `models.py`, `executor.py` | DM-04 |

### Phase 1: Naming Consolidation (N1-N12, parallelizable with Phase 0)

All 12 mechanical rename tasks. Dependency chain: N1 then N2 then N3 then N4 then N5+N6 parallel then N7+N8+N9+N10 parallel then N11 then N12. No runtime behavior changes.

### Phases 2-4: Checkpoint Enforcement Waves 1-3

- **Phase 2 (W1 -- Prompt Prevention)**: T01.01 (`build_prompt()` `## Checkpoints` section), T01.02 (`_warn_missing_checkpoints()` helper)
- **Phase 3 (W2 -- Detection Gate)**: T02.01-T02.05 (create `checkpoints.py`, `PhaseStatus.PASS_MISSING_CHECKPOINT`, `checkpoint_gate_mode`, wire `_verify_checkpoints()`)
- **Phase 4 (W3 -- Manifest, Recovery, CLI)**: T03.01-T03.06 (`CheckpointEntry`, `build_manifest()`, `recover_missing_checkpoints()`, `verify-checkpoints` CLI subcommand)

---

## 4. R2 TASK INVENTORY (v3.7b -- Sprint TUI v2, ~800 LOC)

### Wave 1: Data Model + Monitor Adaptation

| Task | Description | LOC | Dependencies (R1) |
|------|-------------|-----|--------------------|
| 7.1 | 8 new MonitorState fields + Path A synthetic adapter | ~40 | PA-04, PA-05 |
| 7.2 | PhaseResult.turns/tokens_in/tokens_out + Path A aggregation | ~15 | PA-04, DM-05 |
| DM-06 | Path A aggregation: `TaskResult` list -> `PhaseResult` fields | ~10 | PA-04, PA-05, DM-05 |
| 7.3 | SprintResult aggregate properties | ~20 | 7.2 |
| 7.4 | SprintConfig.total_tasks, checkpoint_gate_mode | ~10 | None |
| 7.5 | PhaseStatus.PASS_MISSING_CHECKPOINT display integration | ~5 | R1 checkpoint W2 |

### Wave 2: TUI Rendering (F1-F7)

| Task | Description | Path A Adaptation |
|------|-------------|-------------------|
| F7 | Sprint name in TUI title | None (reads SprintConfig.release_name) |
| F3 | Task-level progress bar | `total_tasks_in_phase = len(tasks)`, `completed_task_estimate = i+1` |
| F2 | Enhanced phase table (turns/output columns) | Wire MonitorState.turns from accumulated TaskResult |
| F6 | Enhanced terminal panels | Aggregate from TaskResult list post-phase |
| F4 | Conditional error panel | Task-level errors from TaskResult.status + exit_code |
| F1 | Activity stream | Synthetic entries per completed task (Strategy B) |

### Wave 3: Summary Infrastructure (F8, F10)

| Task | Description |
|------|-------------|
| F8 | PhaseSummarizer accepts `list[TaskResult]` OR NDJSON path; Haiku narrative pipeline |
| F10 | Release retrospective (depends on F8) |

### Wave 4: Tmux Integration + Lower Priority

| Task | Description |
|------|-------------|
| F9 | Tmux 3-pane layout (depends on F8) |
| F5 | LLM context lines (Path B only in v3.7) |
| 7.7 | SprintTUI.latest_summary_notification |

---

## 5. CROSS-RELEASE INTEGRATION POINTS (document in both specs)

There are 10 integration points. Both specs must include these with: what R1 provides, what R2 consumes, integration type, what breaks if wrong.

1. `executor.py` post-phase hook ordering: `_verify_checkpoints()` (R1) then `summary_worker.submit()` (R2) then manifest update (R1)
2. `PhaseStatus.PASS_MISSING_CHECKPOINT` enum (R1) consumed by TUI STATUS_STYLES/STATUS_ICONS (R2)
3. `models.py` dataclass coexistence: R1 adds CheckpointEntry + checkpoint_gate_mode; R2 adds MonitorState fields + PhaseResult fields + SprintResult properties
4. `process.py` ownership: R1 modifies (naming + checkpoint prompt + append-mode); R2 does not touch
5. `TaskResult.output_path` (R1 PA-05) consumed by R2 F8 PhaseSummarizer
6. `TaskResult.turns_consumed` (R1 PA-04) consumed by R2 F2/F6 phase table and terminal panels
7. `TaskResult.tokens_in/tokens_out` (R1 DM-04/05) consumed by R2 F2/F6 and DM-06 aggregation
8. `_extract_task_block()` (R1 PA-01) enriches NDJSON that R2 F1/F4 consume (indirect)
9. `gate_rollout_mode="shadow"` (R1 PA-06) makes R2 gate column display meaningful
10. Append-mode output (R1 MA-03) lets R2 F8 see all tasks' output

---

## 6. PER-TASK ANALYSIS STANDARD

For EVERY task in both specs, you MUST complete ALL of the following stages. No task is complete without all stages.

### 6.1 Deep Code Reading (do this BEFORE writing)

Read the actual source file. Identify:
- The exact function or class being modified
- The exact line numbers in the current code
- What other functions CALL the code being changed (grep for callers)
- What tests REFERENCE the code being changed (grep test files)

### 6.2 Before/After Code Snippets

Show the EXACT current code and the EXACT proposed replacement. Not pseudocode. Not summaries. Actual Python with correct indentation, imports, and variable names matching the codebase.

### 6.3 Broader Impact Analysis (with grep patterns)

For each change, answer with specific `file:line` references. Include the grep patterns used so a reviewer can verify.

- All callers of modified functions: `grep -rn "function_name(" src/superclaude/`
- All test files importing modified modules: `grep -rn "from.*module.*import" tests/`
- Does this change alter any function signature? If yes, what callers must be updated?
- Does this change introduce a new import? Circular dependency risk?
- Does this change affect serialization/deserialization (JSONL events, dataclass fields)?
- Does any downstream consumer assume the old behavior? (Example: "Anti-instinct gate at executor.py:826-831 assumes output_path is empty string -- after PA-05, it will be a real path, causing the gate to actually evaluate")
- Does any config flag or CLI default change observable behavior?

### 6.4 Implementation Approach Evaluation

For non-trivial tasks (anything over 10 LOC), evaluate at least 2 approaches:

| Approach | LOC | Risk | Why Selected / Rejected |
|----------|-----|------|------------------------|
| [Approach A] | ~N | [level] | [rationale] |
| [Approach B] | ~N | [level] | [rationale] |

**Selected**: [name]
**Rationale**: [why, with reference to debate rulings where applicable]

Tasks that are mechanical (N1-N12 renames, 1-line default changes) should be flagged as "mechanical -- no design choice."

### 6.5 Unintended Consequence Analysis

Think through:
- Could this change cause a test to fail that is NOT testing the changed behavior? (e.g., a test asserting exact prompt strings breaks when prompt content changes)
- Could this change cause a runtime error in a code path not covered by tests? (e.g., Path B exercising a shared function that Path A modified)
- Could this change interact badly with concurrent execution? (e.g., append-mode and OutputMonitor both writing/reading the same file)

### 6.6 Verification Contract (REQUIRED for every FR)

For each FR, add a `**Verification:**` block:

```
**Verification:**
- Unit tests:
  - `test_<name>_happy_path()` -- asserts <specific condition>
  - `test_<name>_<edge_case>()` -- asserts <specific condition>
- Edge cases tested:
  - Empty input: <what happens when input is None/empty/[]/0>
  - Boundary: <minimum and maximum valid values>
  - Scale: <behavior with 1 task vs 50 tasks>
- Failure modes:
  - If <function> throws <exception>: <what breaks downstream>
  - If <file> does not exist: <what happens>
  - If <field> is None when expected non-None: <cascade effect>
- Interaction effects:
  - Existing test <test_name> must still pass because <reason>
  - Change to <file:line> could affect <other_module> via <mechanism>
- Blast radius: <list of modules/features that break if this FR has a bug>
```

### 6.7 Atomic Commit Boundary

For each task, define:

```
**Commit boundary**: What goes into this commit and what does NOT.
Example: "This commit adds _extract_task_block() and its call site. It does NOT
modify the prompt string itself -- that is PA-02."

**Git diff footprint**:
- `src/superclaude/cli/sprint/executor.py`: lines [N-M] (function `X`)
- `tests/cli/sprint/test_executor.py`: lines [N-M] (new test)

**Test commands that MUST pass after this commit**:
uv run pytest tests/ -x -q                        # full suite green
uv run pytest tests/path/to/specific_test.py -v   # new/modified tests

**Depends on commits**: [list of task IDs, or "None"]
**Blocks commits**: [list of task IDs that cannot be committed until this lands]
```

### 6.8 Rollback Plan

Specific to each task. Not "revert the commit." State exactly which lines to change and what to change them to. If the task creates a new file, state "delete file X." If the task modifies a dataclass, state which field to remove and whether migration is needed.

---

## 7. TEMPLATE COMPLIANCE: SECTION-BY-SECTION MAPPING

Fill in ALL sections from the template. Here is the mapping with specific guidance.

### Section 1: Problem Statement

- R1: Sprint pipeline has three classes of reliability defects -- hardcoded zeros in telemetry (PA-04/05/06 bugs), absent checkpoint enforcement, and naming collisions. Evidence: OntRAG R0+R1 missing Phase 3 checkpoints discovered 24h late; `turns_consumed` returns 0 for every production sprint; 3 naming variants create command resolution ambiguity.
- R2: Sprint execution produces no real-time operator visibility. Turns, tokens, errors, and activity are invisible until log inspection. Evidence: operators must manually grep NDJSON after sprint completion; error detection latency is "end of phase" (could be 30+ minutes).

### Section 1.1: Evidence

Every row MUST have: file path and line number, actual current behavior (read it, do not guess), measured or observable impact.

### Section 1.2: Scope Boundary

- R1 IN: PA-01-06, DM-04-05, MA-03, N1-N12, T01-T03 waves
- R1 OUT: TUI rendering, MonitorState population, summarizer, retrospective, tmux
- R2 IN: MonitorState fields, PhaseAccumulator, DM-06, F1-F10, tmux 3-pane
- R2 OUT: Checkpoint enforcement, naming, non-blocking subprocess rewrite

### Section 2.1: Key Design Decisions

Use the decisions from Section 2 of this prompt, formatted as the template's table.

### Section 2.2: Data Flow Diagrams

Include THREE ASCII diagrams:

**Diagram A -- Current State (with bugs)**: Show Path A data flow from `execute_phase_tasks` through `_run_task_subprocess` to `TaskResult` to `PhaseResult`, highlighting where `turns_consumed=0`, `output_path=""`, and `gate_rollout_mode="off"` break the chain. Show the output file overwrite (`"w"` mode). Show MonitorState dead fields.

**Diagram B -- After R1 (bugs fixed, prompts enriched)**: Same flow with PA-04/05/06 fixes active, append mode, enriched prompts. Show that MonitorState fields are still dead (R2 not landed). Show shadow gate evaluation.

**Diagram C -- After R2 (TUI integrated)**: Full flow with synthetic MonitorState population via PhaseAccumulator, TUI rendering, PhaseSummarizer dual-input, tmux summary pane. Show Strategy B adapter converting TaskResult -> MonitorState.

### Section 3: Functional Requirements

Each task becomes an FR. Use FR-R1.01 through FR-R1.xx for R1, FR-R2.01 through FR-R2.xx for R2. Each FR must include: description, acceptance criteria (checkboxes), dependencies, AND the full Verification Contract from Section 6.6 of this prompt.

### Section 4: Architecture

- 4.1 New Files: R1 creates `checkpoints.py`. R2 creates `summarizer.py`, `retrospective.py`. List which tests cover each.
- 4.2 Modified Files: For each, list exact line ranges, existing test coverage, and whether change is additive or mutative.
- 4.3 Removed Files: R1 removes deprecated `task.md`, renames `task-unified.md`.
- 4.4 Module Dependency Graph: ASCII diagram of sprint module dependencies after changes.
- 4.5 Data Models: New/modified dataclasses with field definitions. Include PhaseAccumulator for R2.
- 4.6 Implementation Order: Use the phase/wave structure from the task inventories. MUST include full atomic commit boundary definitions (Section 6.7) for every task.

### Section 5: Interface Contracts

R1 -> R2 contract table (all 10 integration points). CLI surface for R1 (`verify-checkpoints` subcommand). Post-phase hook ordering.

### Section 6: Non-Functional Requirements

Include these NFRs with MEASURABLE targets:

**R1 NFRs:**

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-37A.1 | Token budget per task | Max 200 turns per task (TurnLedger limit) | `TurnLedger.check_budget()` returns False when exceeded |
| NFR-37A.2 | Prompt enrichment token cost | < 300 tokens added per task prompt | Token count of `_extract_task_block()` output + scope boundary + sprint context |
| NFR-37A.3 | Backwards compatibility | Existing sprints with `gate_rollout_mode=off` produce identical behavior | Run existing test suite; 0 failures |
| NFR-37A.4 | Append-mode phase restart safety | Phase restart must not double-count turns | Truncate output file at phase start, append within phase |
| NFR-37A.5 | Naming consolidation completeness | 0 references to old names in src/ | `grep -rn "old_name" src/superclaude/` returns empty |
| NFR-37A.6 | No regression in sprint execution time | < 5% increase in total sprint wall time | Benchmark 3-phase sprint before and after |

**R2 NFRs:**

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-37B.1 | TUI render latency | < 100ms per frame update | Profile `tui.update()` with 50-task MonitorState |
| NFR-37B.2 | TUI memory usage | < 50MB additional RSS | Measure RSS before/after TUI init with 100-phase sprint state |
| NFR-37B.3 | PhaseSummarizer timeout | 30-second timeout on Haiku API call | Timer in summarizer; fallback to "summary unavailable" |
| NFR-37B.4 | Backwards compatibility | `--no-tui` produces identical results | Run existing test suite with TUI disabled |
| NFR-37B.5 | Graceful degradation | Any TUI feature throw -> sprint continues | Try/except around all TUI update calls |
| NFR-37B.6 | Path A total turns per phase | Max `sum(task_budgets)` per phase | TurnLedger aggregate check |

### Section 7: Risk Assessment

For EACH risk, provide the standard table columns PLUS these mandatory sub-items:

```
**Failure scenario**: <Exact sequence of events that causes this risk to materialize>
**Detection mechanism**: <How would you notice? Automated test? Log message? User report?>
**Blast radius**: <Every module, feature, and downstream consumer affected>
**Recovery steps**: <Specific code changes to fix, not "rollback". What data is lost?>
```

**R1 Mandatory Risks** (minimum):
1. Append-mode phase restart double-counting (MA-03 + PA-04 interaction)
2. Shadow gate default exposing latent bugs in gate evaluation code
3. `_extract_task_block()` regex failing on edge-case markdown formatting
4. Naming consolidation breaking import paths in tests vs production
5. `count_turns_from_output()` returning incorrect count on malformed NDJSON

**R2 Mandatory Risks** (minimum):
1. stall_status false alarm in MonitorState adapter (user kills healthy process)
2. PhaseSummarizer Haiku API failure mid-sprint
3. TUI rendering crash with unexpected MonitorState field values (None, negative, overflow)
4. DM-06 aggregation producing incorrect totals with mixed success/failure status
5. tmux pane creation failing when tmux is not installed
6. Race condition: TUI reads MonitorState while PhaseAccumulator writes it (thread safety)

### Section 8: Test Plan

**Minimum test counts**: R1: at least 25 unit tests. R2: at least 40 unit tests.

For EVERY test, specify:
- Test function name (e.g., `test_extract_task_block_single_task`)
- File location (e.g., `tests/cli/sprint/test_executor.py`)
- What it asserts (specific condition, not "it works")
- Which task/FR it traces to

Include integration tests per phase/wave and a regression test matrix listing every existing test file that touches modified files.

### Section 9: Migration & Rollout

Include these 6 specific migration scenarios:

**R1 Migration Scenarios:**
1. **Phase restart with append mode**: A sprint is killed at phase 2 task 3, then restarted with `--start 2`. The output file has stale data from the failed run. Document: Is there a truncation point at phase start? If not, `count_turns_from_output()` counts turns from the failed attempt. This MUST be addressed.
2. **In-flight sprint with gate default change**: Sprint started before R1 with `"off"` default. Mode is read from `SprintConfig` at sprint start, not per-phase. Sprint continues with `"off"` until restarted. Document this.
3. **`_extract_task_block()` fallback**: Phase file does not contain matching `### T<PP>.<TT>` heading. Document fallback behavior (return empty string, prompt falls back to description-only).

**R2 Migration Scenarios:**
4. **Pre-R1 data display**: R2 code runs against data from a pre-R1 sprint where `turns_consumed=0` and `output_path=""`. TUI displays zeros/defaults. Document as acceptable degraded behavior, not a crash.
5. **PhaseSummarizer input precedence**: Both `list[TaskResult]` and NDJSON path provided. `list[TaskResult]` takes priority when present (Path A); NDJSON used when list is empty (Path B).
6. **tmux not installed**: Summary written to file only, no pane created. Graceful degradation.

### Section 10: Downstream Inputs

Describe how `sc:roadmap` and `sc:tasklist` consume each spec. Include tier assignments (STRICT for data model, STANDARD for TUI features, RELAXED for F9 tmux).

### Section 11: Open Items

Carry open questions from existing drafts. Resolve any that code reading answers.

### Section 12: Brainstorm Gap Analysis

Answer ALL 10 mandatory gap questions. For each: if it is a gap, assign severity and identify which spec section it affects. If not a gap, explain why.

| Gap ID | Question | Severity if Unanswered |
|--------|----------|----------------------|
| GAP-01 | Does `count_turns_from_output()` handle the append-mode file correctly, or does it need a separator/marker between tasks? | HIGH -- wrong turn counts cascade to TurnLedger math |
| GAP-02 | When PA-06 changes gate default to "shadow", do all existing TurnLedger tests still pass? Some may assert on "off" default. | HIGH -- test suite regression |
| GAP-03 | Does `_extract_task_block()` handle `### Checkpoint:` headings (which PA-01 might encounter but should skip)? | MEDIUM -- could inject checkpoint text into task prompt |
| GAP-04 | What happens to the PhaseAccumulator adapter when a task takes >120 seconds (stall_status)? Is the fix in the adapter or MonitorState? | MEDIUM -- false "STALLED" display |
| GAP-05 | Does PhaseSummarizer have a circuit breaker / retry policy for Haiku API calls, or just a timeout? | MEDIUM -- could hang sprint on transient API failures |
| GAP-06 | Are there any tests that directly assert `gate_rollout_mode == "off"` as default? | HIGH -- PA-06 breaks them |
| GAP-07 | Does F8 dual-input PhaseSummarizer need different prompt templates for TaskResult input vs NDJSON input? | LOW -- same summary goal, different source format |
| GAP-08 | Is thread safety guaranteed when PhaseAccumulator writes to MonitorState while TUI reads it? | MEDIUM -- race condition in concurrent access |
| GAP-09 | What is the behavior of `_extract_task_block()` when the phase file uses CRLF line endings? | LOW -- could cause regex mismatch |
| GAP-10 | Does append mode interact with the `--start` flag for phase resume? If user resumes from phase 3, does the phase-3 output file get truncated first? | HIGH -- data integrity on resume |

### Appendix A: Glossary

Define: Path A, Path B, PhaseAccumulator, TurnLedger, NDJSON, MonitorState, OutputMonitor, shadow mode, soft mode, full mode, gate rollout, stall_status.

### Appendix B: Reference Documents

List all source documents from Section 1.2 of this prompt with relevance descriptions.

---

## 8. QUALITY GATES

Before declaring each spec complete, verify ALL of the following:

1. **Zero sentinels**: `grep -c '{{SC_PLACEHOLDER:' <output-file>` returns 0
2. **All sections present**: Every numbered section from the template exists in the output
3. **Every task has before/after code**: No task is specified with only prose
4. **Every task has impact analysis**: No task is specified without caller/test tracing with grep patterns
5. **Every task has verification contract**: Every FR has the structured Verification block (unit tests, edge cases, failure modes, interaction effects, blast radius)
6. **Every task has verification commands**: No task ends without a runnable pytest or grep command
7. **Every task has a rollback plan**: No task ends without specific revert instructions
8. **Every task has commit boundary**: No task in Section 4.6 lacks commit boundary, git diff footprint, depends-on, and blocks
9. **Cross-references are bidirectional**: Every R1 task that R2 depends on is marked in R2's FR, and vice versa
10. **Implementation order is acyclic**: No task depends on a task that comes after it
11. **Line numbers verified**: Every line reference confirmed against current source code
12. **Test minimums met**: R1 has >= 25 unit tests, R2 has >= 40 unit tests
13. **NFRs measurable**: Every NFR in Section 6 has a numeric target and measurement method
14. **Risks complete**: Every risk in Section 7 has failure scenario, detection, blast radius, and recovery sub-items
15. **Gap analysis complete**: All 10 gap questions answered in Section 12
16. **Three diagrams present**: Section 2.2 contains exactly 3 ASCII data flow diagrams

---

## 9. ANTI-PATTERNS TO AVOID

1. **"Read the codebase to understand"** -- Every task must contain enough context that the implementer does not need to explore. Include line numbers, function signatures, and data flow descriptions.
2. **"This task is straightforward"** -- Even 1-line changes (PA-05, PA-06, MA-03) need broader impact analysis. A 1-line default change can activate a dormant code path.
3. **"Tests TBD"** -- Every task must have specific test commands listed. If new tests are needed, specify the test function name and what it validates.
4. **Implicit dependency chains** -- If task B reads a field that task A adds, state this explicitly. "Depends on PA-04" is not enough; say "Depends on PA-04 because this task reads `TaskResult.turns_consumed` which is hardcoded to 0 until PA-04 lands."
5. **Missing rejected approaches** -- For any task with a design choice, the spec must document what was NOT chosen and why. This prevents re-discovering and re-debating settled questions.
6. **Overwriting validated decisions** -- The adversarial debates produced binding rulings. Do not present Strategy A as viable for v3.7. Do not propose `/sc:task` invocation for Path A. Do not propose per-task output files. These are deferred to v3.8.

---

## 10. EXECUTION INSTRUCTIONS

1. Read ALL source code files listed in Section 1.1. Do not skip any.
2. Read ALL reference documents listed in Section 1.2. Cross-reference task assignments against the partition document.
3. Write R1 spec first (it is the foundation).
4. Write R2 spec second (it consumes R1 contracts).
5. After writing each spec, run the quality gates from Section 8.
6. Use parallel tool calls wherever independent reads are possible (Wave strategy).

Begin.

## PROMPT END
