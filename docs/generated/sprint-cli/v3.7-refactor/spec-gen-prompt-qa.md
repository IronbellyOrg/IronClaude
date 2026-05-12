# Spec Generation Prompt: Quality Engineering Perspective

> **Agent**: Quality Engineer (QA)
> **Output**: TWO release spec documents following release-spec-template.md
> **Angle**: Testability, edge cases, failure modes, verification rigor, blast radius analysis

---

## PROMPT BEGIN

You are a Quality Engineer generating two release specification documents. Your mandate: every requirement must answer three questions before it is written: (1) How do we PROVE this works? (2) What could go wrong? (3) What is the blast radius if it fails?

You will produce two documents:

1. **R1: v3.7a -- Pipeline Reliability & Naming** (~480 LOC, spec_type: refactoring)
2. **R2: v3.7b -- Sprint TUI v2** (~800 LOC, spec_type: new_feature)

Both documents MUST follow the template structure at `src/superclaude/examples/release-spec-template.md` exactly, including YAML frontmatter, all numbered sections, and conditional sections appropriate to each spec type.

---

### STEP 0: Read Before You Write

Before writing any specification text, you MUST read the following source files in order. Do not paraphrase from memory. Open each file, read the relevant lines, and cite line numbers in your spec where applicable.

**Source code files (read these FIRST -- they are ground truth)**:
- `src/superclaude/cli/sprint/executor.py` -- lines 956-1100 (Path A loop), lines 1201-1254 (path branching), lines 1017-1025 (TaskResult construction), line 1091 (turns_consumed bug)
- `src/superclaude/cli/sprint/process.py` -- line 114 (file open mode "w"), lines 123-204 (build_prompt), lines 245-307 (build_task_context)
- `src/superclaude/cli/sprint/models.py` -- line 176 (output_path default), line 329 (gate_rollout_mode default), TaskResult dataclass, PhaseResult dataclass, MonitorState class
- `src/superclaude/cli/sprint/monitor.py` -- lines 114-141 (count_turns_from_output), OutputMonitor class
- `src/superclaude/cli/sprint/config.py` -- lines 342-380 (parse_tasklist, TaskEntry), lines 389-394 (dependencies)
- `src/superclaude/cli/sprint/tui.py` -- line 107-108 (monitor_state binding)

**Analysis documents (read these SECOND -- they provide validated design decisions)**:
- `docs/generated/sprint-cli/v3.7-refactor/context-01-path-a-deficiencies.md` -- 7 validated deficiencies
- `docs/generated/sprint-cli/v3.7-refactor/context-02-debate-rulings.md` -- 5 adversarial debate rulings
- `docs/generated/sprint-cli/v3.7-refactor/context-03-v37-spec-gap-analysis.md` -- gap analysis
- `docs/generated/sprint-cli/v3.7-refactor/MERGED-REFACTORING-RECOMMENDATION.md` -- unified recommendation
- `docs/generated/sprint-cli/v3.7-refactor/path-a-partition-document.md` -- task-to-release assignment
- `docs/generated/sprint-cli/v3.7-refactor/debates-monitor-adaptation.md` -- 3 debates on OutputMonitor strategy
- `docs/generated/sprint-cli/v3.7-refactor/design-monitor-per-task.md` -- Strategy A vs B vs C design doc
- `docs/generated/sprint-cli/v3.7-refactor/debate-split-vs-resplit.md` -- split process debate (Option C won)
- `docs/generated/sprint-cli/v3.7-refactor/chunk-01-checkpoint-enforcement.md` -- checkpoint analysis
- `docs/generated/sprint-cli/v3.7-refactor/chunk-02-sprint-tui-v2.md` -- TUI feature analysis
- `docs/generated/sprint-cli/v3.7-refactor/chunk-03-naming-consolidation.md` -- N1-N12 analysis
- `docs/generated/sprint-cli/v3.7-refactor/chunk-04-data-model-changes.md` -- data model analysis
- `docs/generated/sprint-cli/v3.7-refactor/chunk-05-cross-cutting.md` -- cross-cutting concerns
- `docs/generated/sprint-cli/v3.7-refactor/chunk-06-path-a-enrichment.md` -- Path A enrichment analysis
- `docs/generated/sprint-cli/v3.7-refactor/incremental-fidelity-validation.md` -- fidelity audit
- `docs/generated/sprint-cli/v3.7-refactor/partition-validation-audit.md` -- partition validation

**Verification commands -- test them first**:
Before including ANY verification command in the spec (e.g., `uv run pytest ...`, `grep -c ...`), run the command yourself in the working directory to confirm it executes without error. If it fails, fix the command or note it as "requires implementation" rather than presenting a broken command as a test.

---

### STEP 1: Frontmatter and Problem Statement

For each spec, populate the YAML frontmatter completely. Use these values:

**R1 frontmatter**:
- title: "v3.7a -- Pipeline Reliability & Naming Consolidation"
- spec_type: refactoring
- complexity_score: 0.45
- complexity_class: MEDIUM
- target_release: v3.7a
- feature_id: FR-37A

**R2 frontmatter**:
- title: "v3.7b -- Sprint TUI v2"
- spec_type: new_feature
- complexity_score: 0.70
- complexity_class: HIGH
- target_release: v3.7b
- feature_id: FR-37B

For Section 1 (Problem Statement), cite specific line numbers and actual code from the source files you read. Do not describe problems abstractly. Show the code that is broken.

For Section 1.1 (Evidence), every row must have:
- A file path and line number
- The actual current behavior (not what you think it does -- read it)
- The measured or observable impact

---

### STEP 2: Functional Requirements with Verification Rigor

For EACH functional requirement in Section 3, you must include the following sub-sections beyond what the template requires:

#### 2a. Standard requirement fields (from template)
- Description, Acceptance Criteria, Dependencies

#### 2b. Verification Contract (REQUIRED for every FR)

For each FR, add a `**Verification:**` block containing:

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

#### 2c. R1 Functional Requirements

Include these task groups with full verification contracts:

**Phase 0 (Foundation -- all parallelizable)**:
- **FR-37A.1**: PA-04 -- Fix `turns_consumed` at `executor.py:1091`. Currently hardcoded to 0. Must call `count_turns_from_output()` from `monitor.py:114-141`.
  - Test: What does `count_turns_from_output()` return on an empty file? On a file with 0 assistant events? On a file with 500 events?
  - Failure mode: If the output file was overwritten (process.py:114 "w" mode), `count_turns_from_output()` sees only the last task's output. How does this interact with the append-mode fix (MA-03)?
  - Blast radius: TurnLedger reimbursement math, R2's F2/F6 display, budget exhaustion halts

- **FR-37A.2**: PA-05 -- Wire `TaskResult.output_path` at `executor.py:1017`. Currently defaults to empty string "".
  - Test: What is `output_path` when `config.output_file(phase)` returns a path that does not yet exist? When it returns None?
  - Failure mode: Anti-instinct gate at `executor.py:826-831` checks `output_path.exists()` -- what happens if the path is set but the file was deleted between task completion and gate evaluation?
  - Blast radius: Anti-instinct gate evaluation, R2's F8 PhaseSummarizer, MonitorState adapter

- **FR-37A.3**: PA-01 -- Extract task block via new `_extract_task_block()` function. Parses `### T<PP>.<TT>` boundaries from phase file.
  - Test: Phase file with 0 tasks (empty). Phase file with 1 task. Phase file with 50 tasks. Task ID that does not exist in phase file. Task heading exists but body is empty. Task block contains markdown code fences (triple backtick edge case in parsing).
  - Failure mode: If phase file path is invalid, what exception? If task_id format is wrong (e.g., "T1.1" instead of "T01.01"), does regex match?
  - Blast radius: All downstream prompt enrichment (PA-02, PA-03), R2's monitoring data richness

- **FR-37A.4**: PA-02 -- Scope boundary text addition (~50 tokens)
- **FR-37A.5**: PA-03 -- Shared `build_sprint_context_header()` (~80 tokens). This function is used by BOTH Path A and Path B. Test that Path B's `build_prompt()` can also call it without regression.
- **FR-37A.6**: PA-06 -- Change `gate_rollout_mode` default from `"off"` to `"shadow"` at `models.py:329`.
  - Test: Existing tests that assume default is "off" WILL BREAK. Enumerate them. Decide: update tests or provide migration path.
  - Failure mode: If shadow mode causes gate evaluation on every sprint (it will), what is the performance cost? Does gate evaluation depend on `output_path` being valid (PA-05)?
  - Blast radius: Every existing sprint run now evaluates gates in shadow mode. If gate code has bugs, shadow mode exposes them on every run.

- **FR-37A.7**: DM-04 -- Implement `extract_token_usage()` in `monitor.py`. Parses NDJSON for token usage data.
  - Test: NDJSON with no token fields. NDJSON with partial token data (tokens_in present, tokens_out missing). Malformed JSON lines interspersed with valid ones. Empty file.
  - Failure mode: If NDJSON parsing throws on malformed input, does it crash the phase or gracefully return 0?

- **FR-37A.8**: DM-05 -- Add `tokens_in`/`tokens_out` fields to `TaskResult` dataclass and wire extraction.
  - Test: Do existing `TaskResult` construction sites (there may be multiple) still work with new fields that have defaults? Run `grep -rn "TaskResult(" src/superclaude/` to find all construction sites.

- **FR-37A.9**: MA-03 -- Append mode fix: `process.py:114` change `"w"` to `"a"`.
  - Test: After 10 tasks in a phase, the output file contains NDJSON from ALL 10 tasks (not just the last). File size grows monotonically across tasks.
  - Failure mode: On phase retry/restart, the file now APPENDS to stale data from a previous run. Is there a truncation point at phase start? If not, `count_turns_from_output()` counts turns from a previous failed attempt.
  - CRITICAL EDGE CASE: Phase restart after partial failure. File has tasks 1-5 from failed run + tasks 1-10 from retry. Turn count is 15 tasks' worth of turns, not 10. This MUST be addressed in the spec.

- **FR-37A.10 through FR-37A.21**: N1-N12 naming consolidation tasks. For each rename:
  - Test: After rename, `grep -rn "old_name" src/superclaude/` returns 0 hits. `grep -rn "new_name" src/superclaude/` returns expected count.
  - Failure mode: Import statement references old name -- causes ImportError at runtime. Test suite references old name -- tests pass (because they import old name which still resolves due to Python caching) but production fails.

**Phases 1-4 (Checkpoint Enforcement W1-W3)**:
- For each checkpoint task (T01.01 through T04.03), include verification contracts. Key verification focus:
  - T02.04: The gate fires for BOTH Path A and Path B post-phase flows. Write a test that simulates a Path A phase (multiple TaskResult objects) and verifies the gate evaluates.
  - T04.01: Checkpoint normalization -- when a `### Checkpoint:` heading is renormalized to `### T<PP>.<NN> -- Checkpoint:`, does `parse_tasklist()` now parse it as a regular task? If yes, it executes as a subprocess in Path A's loop. Test this.

#### 2d. R2 Functional Requirements

Include these with full verification contracts:

**Wave 1 (Data Model)**:
- **FR-37B.1**: MonitorState 8 new fields. For each field: what is its default value? What populates it under Path A? Under Path B? What happens if it is read before population?
- **FR-37B.2**: PhaseResult extensions. Test that `SprintResult` aggregate properties still compute correctly when `PhaseResult` has the new fields.
- **FR-37B.3**: SprintResult aggregate properties. Test with 0 phases, 1 phase, 10 phases. Test with a phase that has 0 turns and 0 tokens (edge case: division by zero in averages?).
- **FR-37B.4**: PhaseAccumulator adapter. Test the stall_status false alarm fix: a task running for 180 seconds must NOT show "STALLED". Test that `last_event_time` is set to `monotonic()` on adapter creation.
- **FR-37B.5**: DM-06 aggregation: `list[TaskResult]` -> `PhaseResult` fields.
  - Test with empty TaskResult list. Test with TaskResults where all `turns_consumed` are 0 (PA-04 not yet fixed). Test with mixed success/failure TaskResults.

**Wave 2 (TUI Features F1-F7 with Path A adaptations)**:
- **FR-37B.6**: F1 Activity stream with synthetic entries for Path A.
  - Test: Synthetic entry format matches what TUI rendering expects. 0 tasks produces 0 entries. 50 tasks produces 50 entries (does the 3-line FIFO correctly show only the last 3?).
  - Manual test: Run a sprint with a 3-task phase and visually confirm activity stream updates between tasks.

- **FR-37B.7**: F2 Enhanced phase table. Running-phase columns show accumulated data from completed tasks. Test that turns column shows sum of completed task turns, not 0.

- **FR-37B.8**: F3 Task-level progress bar. Path A sets exact counts (`total_tasks_in_phase = len(tasks)`, `completed_task_estimate = i+1`). Test that progress shows "3/10" after 3 of 10 tasks complete.

- **FR-37B.9**: F4 Conditional error panel. Task-level errors from `TaskResult` when `status.is_failure`.
  - Edge case: All 10 tasks fail. Does the error panel overflow? Is there a max display limit?
  - Edge case: Task fails with exit_code 0 but status is failure (possible?). Task succeeds with non-zero exit code.

- **FR-37B.10**: F5 -- Deprioritized for Path A per MERGED Section 1.4. Implement for Path B only. Test that Path A does not crash when F5 rendering encounters empty `prompt_preview`.

- **FR-37B.11**: F6 Enhanced terminal panels. Aggregate from `PhaseResult` which is populated from `TaskResult` list via DM-06.

- **FR-37B.12**: F7 Sprint name in TUI title. Path-agnostic. Test with sprint names containing special characters (quotes, ampersands, unicode).

**Wave 3**:
- **FR-37B.13**: F8 PhaseSummarizer with dual input.
  - MUST accept `list[TaskResult]` (Path A) OR NDJSON file path (Path B).
  - Test: Path A input with 0 TaskResults. Path A input with 1 TaskResult that has empty output. Path B input with NDJSON file that does not exist. Path B input with NDJSON file that is 0 bytes.
  - Test: Haiku API call -- what if Haiku is unavailable? Timeout? Rate limited? The summarizer must not crash the sprint.
  - Failure mode: If summarizer throws, does the sprint continue or halt? It MUST continue (summary is non-critical).

- **FR-37B.14**: F10 Release retrospective. Consumes F8 summary files.
  - Test: Sprint with 0 phases (edge case -- should not happen but what if it does?). Sprint with 1 phase. Sprint where F8 failed for some phases (missing summary files).

**Wave 4**:
- **FR-37B.15**: F9 tmux summary pane. Display-only, consumes F8 output.
  - Manual test: Verify pane renders correctly in tmux. Verify graceful degradation when not running in tmux.
  - Failure mode: tmux not installed. tmux session not found. Pane creation fails silently vs crashes.

---

### STEP 3: Architecture (Section 4)

For Section 4 (Architecture), include:

**4.1 New Files**: List every new file with its purpose and which tests cover it.

**4.2 Modified Files**: For each modified file, list:
- Exact line ranges being changed
- What existing tests cover those line ranges (run `uv run pytest --co -q` to list test names, then grep for the file being modified)
- Whether the change is additive (new code) or mutative (changing existing behavior)

**4.3 Removed Files** (R1 only -- refactoring type): List any deprecated names/aliases being removed by N1-N12.

**4.6 Implementation Order**: Must respect these validated dependency chains:
- R1: PA-04, PA-05, PA-01 are all parallelizable (Phase 0). PA-02 and PA-03 depend on PA-01. PA-06 depends on PA-04 + PA-05. DM-05 depends on DM-04. N1-N12 can start with Phase 0.
- R2: Wave 1 (data model) must complete before Wave 2 (TUI features). DM-06 depends on PA-04 + PA-05 + DM-05 (all R1). F8 depends on correctly populated TaskResult (R1 prereqs). F9 depends on F8. F10 depends on F8.

---

### STEP 4: Interface Contracts (Section 5)

**R1 provides -> R2 consumes**. Document these contracts explicitly:

| R1 Provides | R2 Consumes | Contract Type | What Breaks If Wrong |
|---|---|---|---|
| `TaskResult.output_path` (PA-05) | F8 summarizer, MonitorState adapter | Data field, non-empty string | F8 cannot locate output, adapter produces empty state |
| `TaskResult.turns_consumed` (PA-04) | F2, F6, PhaseResult.turns, DM-06 | Data field, integer >= 0 | Display shows 0 turns, aggregation is wrong |
| `TaskResult.tokens_in/out` (DM-05) | F2, F6, PhaseResult.tokens, DM-06 | Data field, integer >= 0 | Token display shows 0 |
| `_extract_task_block()` (PA-01) | Richer NDJSON for F1/F4 | Indirect enrichment | F1/F4 work but with less data |
| `gate_rollout_mode="shadow"` (PA-06) | Gate column display | Configuration default | Gate column shows "off" |
| Append-mode output (MA-03) | F8 summary sees all tasks | File content completeness | F8 sees only last task |
| Post-phase hook site (executor.py) | `summary_worker.submit()` insertion | Code location, ordering | Summary runs before checkpoint (wrong order) |
| `PhaseStatus.PASS_MISSING_CHECKPOINT` | TUI STATUS_STYLES, STATUS_ICONS | Enum value | KeyError in TUI rendering |

---

### STEP 5: Non-Functional Requirements (Section 6)

Include these NFRs with MEASURABLE targets:

**For R1:**

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-37A.1 | Token budget per task | Max 200 turns per task (existing TurnLedger limit) | `TurnLedger.check_budget()` returns False when exceeded |
| NFR-37A.2 | Prompt enrichment token cost | < 300 tokens added per task prompt | Count tokens in `_extract_task_block()` output + scope boundary + sprint context |
| NFR-37A.3 | Backwards compatibility | Existing sprint runs with `gate_rollout_mode=off` must produce identical behavior | Run existing test suite; 0 failures |
| NFR-37A.4 | Append-mode phase restart safety | Phase restart must not double-count turns from previous attempt | Truncate output file at phase start, append within phase |
| NFR-37A.5 | Naming consolidation completeness | 0 references to old names in src/ after N1-N12 | `grep -rn "old_name" src/superclaude/` returns empty |
| NFR-37A.6 | No regression in sprint execution time | < 5% increase in total sprint wall time | Benchmark 3-phase sprint before and after |

**For R2:**

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-37B.1 | TUI render latency | < 100ms per frame update | Profile `tui.update()` with 50-task MonitorState |
| NFR-37B.2 | TUI memory usage | < 50MB additional RSS for TUI state | Measure RSS before/after TUI initialization with 100-phase sprint state |
| NFR-37B.3 | PhaseSummarizer timeout | 30-second timeout on Haiku API call | Timer in summarizer; fallback to "summary unavailable" |
| NFR-37B.4 | Backwards compatibility | Sprints run without TUI (`--no-tui`) must produce identical results | Run existing test suite with TUI disabled |
| NFR-37B.5 | Graceful degradation | If any TUI feature throws, sprint continues | Try/except around all TUI update calls; log error, continue |
| NFR-37B.6 | Path A total turns per phase | Max `sum(task_budgets)` per phase | TurnLedger aggregate check |

---

### STEP 6: Risk Assessment (Section 7)

For EACH risk, you MUST provide all four columns plus these additional sub-items:

```
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| <risk description> | <L/M/H> | <L/M/H> | <mitigation> |

**Failure scenario**: <Exact sequence of events that causes this risk to materialize>
**Detection mechanism**: <How would you notice? Automated test? Log message? User report?>
**Blast radius**: <List every module, feature, and downstream consumer affected>
**Recovery steps**: <Specific actions, not "rollback". What code change fixes it? What data is lost?>
```

**R1 Mandatory Risks** (include at minimum):
1. Append-mode phase restart double-counting (MA-03 + PA-04 interaction)
2. Shadow gate default exposing latent bugs in gate evaluation code
3. `_extract_task_block()` regex failing on edge-case markdown formatting
4. Naming consolidation breaking import paths in tests vs production code
5. `count_turns_from_output()` returning incorrect count on malformed NDJSON

**R2 Mandatory Risks** (include at minimum):
1. stall_status false alarm in MonitorState adapter (user kills healthy process)
2. PhaseSummarizer Haiku API failure mid-sprint
3. TUI rendering crash with unexpected MonitorState field values (None, negative, overflow)
4. DM-06 aggregation producing incorrect totals when tasks have mixed success/failure status
5. tmux pane creation failing when tmux is not installed
6. Race condition: TUI reads MonitorState while PhaseAccumulator writes it (thread safety)

---

### STEP 7: Test Plan (Section 8)

This is the most critical section. Structure it as follows:

#### 8.1 Unit Tests

For EVERY task in both specs, provide at least 2 unit tests with:
- Test function name (e.g., `test_extract_task_block_single_task`)
- File location (e.g., `tests/cli/sprint/test_executor.py`)
- What it asserts (specific condition, not "it works")
- Setup requirements (fixtures, mocks, test data)

Minimum unit test counts:
- R1: At least 25 unit tests across all tasks
- R2: At least 40 unit tests across all tasks

#### 8.2 Integration Tests

For each wave/phase, provide integration tests that verify multiple components working together:

**R1 integration tests**:
- `test_phase0_bug_fixes_enable_turnledger()` -- After PA-04 + PA-05 + MA-03, run a 3-task phase and verify TurnLedger receives non-zero turn data and output_path is valid.
- `test_prompt_enrichment_end_to_end()` -- After PA-01 + PA-02 + PA-03, run a single task and verify the prompt contains task block, scope boundary, and sprint context.
- `test_shadow_gate_evaluates_without_crash()` -- With PA-06 default, run a phase and verify gate evaluation completes (even if gate result is logged, not enforced).
- `test_naming_consolidation_no_old_references()` -- After N1-N12, grep entire codebase for old names.
- `test_append_mode_phase_restart_safety()` -- Run a phase, simulate failure at task 5, restart phase, verify output file contains only the retry's data (not stale + retry).

**R2 integration tests**:
- `test_tui_renders_path_a_phase()` -- Run a 5-task phase through Path A with TUI enabled, verify all F1-F7 features display non-default data.
- `test_phase_summarizer_dual_input()` -- Feed PhaseSummarizer a `list[TaskResult]` and separately an NDJSON file, verify both produce summaries.
- `test_monitor_state_adapter_no_stall_false_alarm()` -- Create adapter, wait 180 seconds (simulated), verify `stall_status` does not show "STALLED".
- `test_dm06_aggregation_mixed_results()` -- 10 TaskResults with 3 failures, verify PhaseResult aggregates correctly and failure count is 3.
- `test_sprint_result_with_zero_phases()` -- SprintResult with empty phase list, verify no division by zero or crash.

#### 8.3 Manual / E2E Tests (R2)

| Scenario | Steps | Expected Outcome | Failure Symptom |
|----------|-------|-----------------|-----------------|
| TUI with 3-task phase | Run `superclaude sprint run <tasklist>` with 3-task phase | Activity stream shows 3 synthetic entries; progress bar reaches 3/3; phase table shows non-zero turns | Blank activity stream; 0/0 progress; turns column shows 0 |
| TUI with all tasks failing | Run sprint where all tasks exit non-zero | Error panel shows all task IDs and exit codes; sprint continues to next phase | Error panel empty; sprint halts unexpectedly |
| PhaseSummarizer Haiku timeout | Run sprint with Haiku API endpoint unreachable | Sprint completes; summary shows "unavailable"; F9/F10 gracefully handle missing data | Sprint hangs; crash; F9/F10 crash with missing file |
| tmux pane outside tmux | Run sprint with F9 enabled outside tmux session | Graceful skip; log message "tmux not available"; sprint continues | Crash; unhandled exception; sprint halts |
| Phase restart with append mode | Start sprint, kill at phase 2 task 3, restart with `--start 2` | Output file contains only restart tasks' data; turn count reflects only current run | Double-counted turns; file has stale + new data |

#### 8.4 Regression Test Matrix

List every existing test file that touches files modified by R1 or R2. For each:
- File path
- Number of tests
- Expected impact (none / needs update / will break)
- Action required

Run `uv run pytest --co -q 2>/dev/null | grep "test_" | wc -l` to get total test count. Then for each modified source file, find its test coverage.

---

### STEP 8: Migration & Rollout (Section 9)

**R1 Migration**:
- Breaking changes: `gate_rollout_mode` default changes from "off" to "shadow". Any CI/CD pipeline or script that relies on gates being off by default will now see shadow evaluation. Document the `--gate-mode off` escape hatch.
- Append mode: `process.py:114` change from "w" to "a" means output files grow within a phase. Document the phase-start truncation mechanism.
- Naming: Old names must have deprecation aliases OR all references must be updated atomically.

**R2 Migration**:
- No breaking changes expected -- TUI features are additive.
- `--no-tui` flag must continue to work identically to pre-R2 behavior.

---

### STEP 9: Key Design Decisions (Section 2.1)

Include ALL of these validated decisions with their debate sources:

| Decision | Choice | Alternatives Considered | Rationale | Source |
|----------|--------|------------------------|-----------|--------|
| Path A TUI strategy | Strategy B (synthetic state) | Strategy A (per-task OutputMonitor) | Blocking subprocess makes real-time TUI unreachable; B delivers same cadence at 45 LOC vs 103 LOC | debates-monitor-adaptation.md Debate 1 |
| Output file mode | Append ("a") within phase | Per-task files; keep "w" mode | 1 LOC fix, zero downstream consumer changes, preserves all NDJSON | debates-monitor-adaptation.md Debate 2 |
| MonitorState sharing | Shared MonitorState via PhaseAccumulator adapter | Path-specific data types | TUI has single data contract; adapter is 10 LOC; zero TUI changes on v3.8 migration | debates-monitor-adaptation.md Debate 3 |
| stall_status fix | Adapter sets `last_event_time = monotonic()` | Modify MonitorState.stall_status property | Fix in adapter, not in shared class; Path B unaffected | debates-monitor-adaptation.md Debate 3 |
| Per-task prompt enrichment | Extract task block + scope boundary + sprint context | Full `@{phase_file}` preload; result file contract; stop-on-STRICT-fail | Adversarial debate validated 3 of 5 proposed additions | context-02-debate-rulings.md |
| Release split boundary | R1 = data contracts/pipeline, R2 = presentation | Single release; three-way split | Boundary validated at 0.83 convergence; Path A work decomposes along same axis | debate-split-vs-resplit.md Option C |
| Deferred items | PA-07 (build_task_context) and PA-08 (deliverable check) to v3.8 | Include in R1 | 75% confidence (below 90% threshold); behind config flags; evaluate after shadow-mode data | path-a-partition-document.md |

---

### STEP 10: Brainstorm Gap Analysis (Section 12)

After completing all sections, perform a gap analysis. For each gap, assign a severity and identify which spec section it affects.

**Mandatory gaps to evaluate** (answer each -- if not a gap, say why):

| Gap ID | Question | Severity if Unanswered |
|--------|----------|----------------------|
| GAP-01 | Does `count_turns_from_output()` handle the append-mode file correctly, or does it need a separator/marker between tasks? | HIGH -- wrong turn counts cascade to TurnLedger math |
| GAP-02 | When PA-06 changes gate default to "shadow", do all 50 existing TurnLedger tests still pass? Some may assert on "off" default. | HIGH -- test suite regression |
| GAP-03 | Does `_extract_task_block()` handle `### Checkpoint:` headings (which PA-01 might encounter but should skip)? | MEDIUM -- could inject checkpoint text into task prompt |
| GAP-04 | What happens to the PhaseAccumulator adapter when a task takes >120 seconds (stall_status)? Is the fix actually in the adapter or does it need to be in MonitorState? | MEDIUM -- false "STALLED" display |
| GAP-05 | Does the PhaseSummarizer have a circuit breaker / retry policy for Haiku API calls, or just a timeout? | MEDIUM -- could hang sprint on transient API failures |
| GAP-06 | Are there any tests that directly assert `gate_rollout_mode == "off"` as default? | HIGH -- PA-06 breaks them |
| GAP-07 | Does the F8 dual-input PhaseSummarizer need different prompt templates for TaskResult input vs NDJSON input? | LOW -- same summary goal, different source format |
| GAP-08 | Is thread safety guaranteed when PhaseAccumulator writes to MonitorState while TUI reads it? | MEDIUM -- race condition in concurrent access |
| GAP-09 | What is the behavior of `_extract_task_block()` when the phase file uses CRLF line endings? | LOW -- but could cause regex mismatch |
| GAP-10 | Does append mode interact with the `--start` flag for phase resume? If a user resumes from phase 3, does the phase-3 output file get truncated first? | HIGH -- data integrity on resume |

---

### STEP 11: Downstream Inputs (Section 10)

For each spec, describe what downstream consumers need:

**For sc:roadmap**: Themes and milestones derived from the spec. R1 provides a "Pipeline Reliability" theme. R2 provides a "TUI v2" theme.

**For sc:tasklist**: Task breakdown guidance. R1 tasks map 1:1 to PA-01 through PA-06, DM-04, DM-05, MA-03, N1-N12, and checkpoint tasks. R2 tasks map to Waves 1-4. Include tier assignments (STRICT for data model, STANDARD for TUI features, RELAXED for F9 tmux).

---

### FORMAT REQUIREMENTS

1. Both specs MUST be complete, standalone documents. Do not reference "see R1 spec" from R2 -- instead, state the dependency explicitly.
2. Every `{{SC_PLACEHOLDER:...}}` sentinel from the template must be replaced. Run `grep -c '{{SC_PLACEHOLDER:' <output-file>` and verify it returns 0.
3. Include Appendix A (Glossary) with: Path A, Path B, TurnLedger, MonitorState, OutputMonitor, PhaseAccumulator, NDJSON, shadow mode, soft mode, full mode.
4. Include Appendix B (Reference Documents) listing all source documents from the analysis document list above.
5. Use YAML frontmatter code blocks (triple backtick yaml), not raw YAML.
6. Section numbering must match the template exactly (1, 1.1, 1.2, 2, 2.1, 2.2, 3, 4, 4.1, 4.2, ...).

---

### OUTPUT

Write the two specs to:
- R1: `docs/generated/sprint-cli/v3.7-refactor/release-spec-v37a-pipeline-reliability.md`
- R2: `docs/generated/sprint-cli/v3.7-refactor/release-spec-v37b-sprint-tui-v2.md`

After writing both specs, run these self-checks:
1. `grep -c '{{SC_PLACEHOLDER:' <each-file>` -- must return 0
2. Verify every FR has a `**Verification:**` block
3. Verify Section 8 has at least 25 unit tests for R1 and 40 for R2
4. Verify Section 7 risks all have failure scenario, detection, blast radius, and recovery sub-items
5. Verify Section 6 NFRs all have measurable targets

## PROMPT END
