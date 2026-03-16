---
spec_source: sprint-preflight-executor-spec.md
complexity_score: 0.55
primary_persona: architect
---

# 1. Executive summary

This roadmap delivers a **pre-sprint Python preflight execution path** for the sprint runner, allowing selected phases to run local commands before Claude-driven phases begin. The architecture is moderate in complexity because it crosses four domains—**phase discovery/config parsing, task parsing, subprocess execution, and result/status integration**—but remains contained within the existing `src/superclaude/cli/sprint/` package.

## Architectural priorities

1. **Preserve the existing Claude execution path unchanged.**
2. **Insert preflight as a clean pre-loop hook** in `execute_sprint()`.
3. **Reuse existing result/reporting contracts** rather than inventing parallel formats.
4. **Enforce safe command execution** with `subprocess.run(..., shell=False)` and `shlex.split()`.
5. **Keep rollback trivial** by making the orchestration hook removable in one line.
6. **Prove compatibility through tests**, especially around `_determine_phase_status()`.

## Target outcome

At completion, the sprint runner will:

- Parse `Execution Mode` from phase metadata.
- Parse `**Command:**` and `Classifier` task metadata.
- Execute all `python` phases before Claude phases.
- Skip `skip` phases deterministically.
- Emit evidence artifacts and compatible phase result files.
- Combine preflight and Claude outcomes into one correct sprint status.

# 2. Phased implementation plan with milestones

## Phase 0. Architecture confirmation and design freeze

### Objectives
- Confirm insertion points, data model extensions, and compatibility boundaries.
- Resolve open questions that could affect implementation shape.

### Work items
1. Confirm existing symbol ownership and call flow for:
   - `discover_phases()`
   - `parse_tasklist()`
   - `execute_sprint()`
   - `AggregatedPhaseReport.to_markdown()`
   - `_determine_phase_status()`
2. Freeze data model changes:
   - `Phase.execution_mode: str = "claude"`
   - `TaskEntry.command: str = ""`
   - `TaskEntry.classifier: str` or equivalent optional/defaulted field
   - `PhaseStatus.PREFLIGHT_PASS = "preflight_pass"`
3. Confirm file placement:
   - New module: `src/superclaude/cli/sprint/classifiers.py`
   - Preflight executor logic in existing sprint execution module or a tightly scoped new module under `src/superclaude/cli/sprint/`
4. Decide handling for low-risk open questions:
   - Multi-line commands: explicitly unsupported unless already present
   - `--phases` filter: define whether preflight respects filtered active phases
   - Classifier exceptions: treat as task failure and record evidence

### Milestone
- **M0:** Finalized architecture notes and implementation boundaries with no ambiguity on parser, executor, and reporting integration.

### Timeline estimate
- **0.5 day**

---

## Phase 1. Data model and parser extensions

### Objectives
- Extend phase and task parsing without disturbing existing behavior when annotations are absent.

### Work items
1. Update phase discovery/config parsing to support `Execution Mode` column:
   - Default all phases to `"claude"` when column is missing.
   - Normalize case-insensitively.
   - Accept only `claude`, `python`, `skip`.
   - Raise `click.ClickException` on invalid values.
2. Extend `TaskEntry` parsing:
   - Extract `**Command:**`
   - Strip wrapping backticks only
   - Preserve pipes, redirects, and quoted arguments verbatim
   - Default missing command to `""`
3. Extend task metadata parsing for classifier lookup metadata:
   - Parse `Classifier` field from task block/table metadata as specified
   - Store on `TaskEntry.classifier`
4. Add parser-level unit tests for:
   - Missing execution mode column
   - Invalid execution mode value
   - Command extraction with quoting/pipes/redirection
   - Missing command/classifier behavior

### Milestone
- **M1:** Configuration and task parsers produce the complete metadata required for preflight execution.

### Timeline estimate
- **1-1.5 days**

---

## Phase 2. Classifier registry foundation

### Objectives
- Introduce a minimal but extensible classification mechanism with deterministic behavior.

### Work items
1. Create `src/superclaude/cli/sprint/classifiers.py`
2. Implement:
   - `CLASSIFIERS: dict[str, Callable[[int, str, str], str]]`
   - Built-in classifier `empirical_gate_v1`
3. Enforce failure mode:
   - Missing classifier name raises `KeyError`
4. Add classifier-focused tests:
   - Expected classification on pass/fail outputs
   - Missing classifier lookup behavior
   - Classifier exception behavior if adopted as formal handling rule

### Architectural notes
- Keep registry static and explicit.
- Avoid plugin discovery or dynamic imports in this iteration.
- Preserve future extension path by making registry-based dispatch the only access path.

### Milestone
- **M2:** Registry-backed classification works independently and is covered by deterministic unit tests.

### Timeline estimate
- **0.5-1 day**

---

## Phase 3. Preflight executor implementation

### Objectives
- Build the pre-sprint execution engine for `python` phases with safe subprocess handling and structured results.

### Work items
1. Implement `execute_preflight_phases()` with:
   - Iteration over `config.active_phases`
   - Selection of `execution_mode == "python"`
   - Task parsing via `parse_tasklist()`
   - Command extraction from `TaskEntry.command`
2. Execute commands using:
   - `shlex.split(command)`
   - `subprocess.run(shell=False, capture_output=True, timeout=120)`
3. Capture execution evidence:
   - `stdout`
   - `stderr`
   - `exit_code`
   - wall-clock duration
4. Resolve classifier and generate task-level classification label.
5. Build `TaskResult` objects for each task.
6. Handle failures safely:
   - Timeout becomes task failure
   - Classifier errors become task failure if this behavior is approved
   - Missing command in a python-mode task should be treated explicitly as failure or validation error

### Architectural notes
- No `ClaudeProcess` instantiation in this path.
- No mutation of the Claude-mode executor.
- Keep execution localized and side-effect-aware.

### Milestone
- **M3:** Preflight executor runs python-mode tasks end-to-end and returns `list[PhaseResult]`.

### Timeline estimate
- **1.5-2 days**

---

## Phase 4. Evidence artifact and result file generation

### Objectives
- Emit outputs that are both useful for diagnosis and fully compatible with existing downstream status parsing.

### Work items
1. Write task evidence files to:
   - `artifacts/D-NNNN/evidence.md` or `artifacts/<task_id>/evidence.md`
2. Include in evidence:
   - Command executed
   - Exit code
   - Truncated stdout (10KB)
   - Truncated stderr (2KB)
   - Duration
   - Classification label
3. Generate `phase-N-result.md` via `AggregatedPhaseReport.to_markdown()`
4. Ensure frontmatter includes:
   - `source: preflight`
5. Ensure `EXIT_RECOMMENDATION` rules:
   - `CONTINUE` when all pass
   - `HALT` when any fail
6. Verify `_determine_phase_status()` parses generated results with no modifications.

### Architectural notes
- This is the highest compatibility-risk area.
- Reuse existing reporting model rather than duplicating format logic.
- Treat report generation as a contract boundary.

### Milestone
- **M4:** Preflight output artifacts are diagnosable, stable, and parser-compatible.

### Timeline estimate
- **1 day**

---

## Phase 5. Main sprint orchestration integration

### Objectives
- Merge preflight results into the sprint lifecycle cleanly and with minimal blast radius.

### Work items
1. Insert `execute_preflight_phases()` before the main Claude phase loop in `execute_sprint()`.
2. Update main loop behavior:
   - Skip already executed `python` phases
   - Skip `skip` phases and mark `PhaseStatus.SKIPPED`
3. Add `PhaseStatus.PREFLIGHT_PASS`
   - `is_success == True`
   - `is_failure == False`
4. Ensure logger/TUI tolerate and display the new status.
5. Ensure combined sprint outcome correctly reflects:
   - preflight pass/fail
   - skipped phases
   - remaining Claude phases

### Architectural notes
- This phase must preserve **single-line rollback**.
- The orchestration diff should remain small and obvious.
- Avoid distributing preflight logic across multiple call sites.

### Milestone
- **M5:** Sprint orchestration supports preflight, skip semantics, and unified status evaluation.

### Timeline estimate
- **1 day**

---

## Phase 6. Test hardening, performance validation, and rollback proof

### Objectives
- Validate that the feature is correct, fast, safe, and reversible.

### Work items
1. Deliver unit test coverage for:
   - Models/status behavior
   - Config parsing
   - Task parsing
   - Classifier registry
   - Result compatibility
2. Deliver integration tests for:
   - Preflight execution flow
   - Timeout handling
   - Evidence file generation
   - Combined preflight + Claude result handling
   - Skip-phase behavior
   - Zero-token path assurance by verifying no Claude process creation
3. Validate NFRs:
   - `<30s` for 5 EXEMPT-tier tasks
   - zero Claude API token consumption for python phases
   - parser compatibility without modifying `_determine_phase_status()`
   - rollback by removing one call site only
4. Run project verification:
   - relevant unit/integration suites with `uv run pytest`
   - sync workflow if component files affect dev copies

### Milestone
- **M6:** Feature passes all acceptance criteria and is ready for merge.

### Timeline estimate
- **1-1.5 days**

# 3. Risk assessment and mitigation strategies

## Risk 1. Result file format drift
**Severity:** High

### Why it matters
If preflight-generated phase results differ from Claude-generated results, `_determine_phase_status()` may fail, causing false halts or broken sprint completion logic.

### Mitigation
1. Reuse `AggregatedPhaseReport.to_markdown()` directly.
2. Add a compatibility fixture tested against `_determine_phase_status()`.
3. Treat result format as a locked contract in this release.
4. Add one integration test covering both preflight and Claude-origin result files.

### Contingency
- If compatibility issues appear, block release until report generation is aligned; do not patch `_determine_phase_status()` as a shortcut.

---

## Risk 2. Environment mismatch for local commands
**Severity:** Medium

### Why it matters
Preflight commands may depend on tools, environment variables, current working directory, or binary availability.

### Mitigation
1. Capture stderr and exit code in evidence artifacts.
2. Record exact command and duration for every task.
3. Execute in a predictable working directory.
4. Document environmental assumptions for python-mode phases.

### Contingency
- Fail the affected task cleanly and emit actionable evidence rather than retrying implicitly.

---

## Risk 3. Command parsing and quoting issues
**Severity:** Medium

### Why it matters
Commands containing quotes, pipes, redirects, or nested CLI strings may break if parsing alters their content.

### Mitigation
1. Preserve command strings verbatim in parsing.
2. Tokenize only at execution time with `shlex.split()`.
3. Add test cases for:
   - quoted arguments
   - nested quoted commands
   - pipe and redirect tokens preserved in parsing
4. Clarify that shell metacharacters are preserved textually but not shell-expanded under `shell=False`.

### Contingency
- If actual workflows require shell features, require explicit spec revision rather than silently enabling `shell=True`.

---

## Risk 4. Classifier misclassification
**Severity:** Low-Medium

### Why it matters
A flawed classifier can incorrectly promote or halt downstream work.

### Mitigation
1. Keep classifier logic simple and deterministic.
2. Unit test built-ins against known fixtures.
3. Fail closed on missing classifiers.
4. Treat classifier exceptions as task failure and log them in evidence.

### Contingency
- Allow registry updates in subsequent releases without executor redesign.

---

## Risk 5. Orchestration regression in existing Claude flow
**Severity:** Medium

### Why it matters
A poorly placed hook could unintentionally alter current sprint behavior.

### Mitigation
1. Insert preflight in one orchestrator location only.
2. Avoid changes to Claude-mode execution code.
3. Add regression tests for all-Claude tasklists.
4. Verify one-line rollback property before merge.

### Contingency
- Remove the preflight hook call to revert immediately if late-stage regression is found.

# 4. Resource requirements and dependencies

## Engineering resources

1. **Primary backend/CLI engineer**
   - Parser updates
   - executor implementation
   - orchestration integration
2. **QA/test engineer or implementation owner**
   - unit/integration coverage
   - compatibility validation
   - performance validation
3. **Architect/reviewer**
   - contract review for result/report compatibility
   - rollback path validation
   - status model review

## Code areas impacted

1. `src/superclaude/cli/sprint/process.py`
2. `src/superclaude/cli/sprint/config.py` or equivalent phase/task parsing module
3. `src/superclaude/cli/sprint/classifiers.py` (new)
4. Models/status/reporting definitions touched by `Phase`, `TaskEntry`, `TaskResult`, `PhaseStatus`

## External and internal dependencies

1. **subprocess** (stdlib)
   - Command execution engine
2. **shlex** (stdlib)
   - Safe argument splitting
3. **click**
   - Validation errors for unsupported execution modes
4. **AggregatedPhaseReport**
   - Required for result-file compatibility
5. **_determine_phase_status()**
   - Must remain unchanged
6. **parse_tasklist() / discover_phases()**
   - Must be extended, not replaced

## Operational dependencies

1. Local tools referenced by preflight commands must exist.
2. CI/runtime environment must permit subprocess execution.
3. Artifact directories must be writable.
4. UV-based test execution must remain the only Python execution workflow.

# 5. Success criteria and validation approach

## Success criteria mapping

1. **SC-001:** Python-mode Phase 1 completes in under 30 seconds with zero Claude token usage.
2. **SC-002:** Nested command invocation such as `claude --print -p "hello"` executes successfully without deadlock.
3. **SC-003:** `_determine_phase_status()` parses preflight result files unchanged.
4. **SC-004:** Unit test target passes.
5. **SC-005:** Integration test target passes.
6. **SC-006:** `execution_mode: skip` produces `PhaseStatus.SKIPPED` with no subprocess launch.
7. **SC-007:** Removing the `execute_preflight_phases()` call fully reverts behavior.
8. **SC-008:** Evidence artifacts contain all required fields.

## Validation approach

### Functional validation
1. Parser tests for `Execution Mode`, `Command`, and `Classifier`.
2. Executor tests for successful, failing, and timing-out commands.
3. Status tests for `PREFLIGHT_PASS` and `SKIPPED`.
4. Integration tests for mixed preflight + Claude sprint runs.

### Non-functional validation
1. Time-boxed benchmark for 5 EXEMPT-tier tasks.
2. Verification that python-mode phases do not instantiate Claude execution objects.
3. Rollback validation by removing the preflight hook call and rerunning existing Claude-only tests.

### Release gate
Ship only when:
- compatibility tests pass,
- performance is within threshold,
- rollback is demonstrated,
- and no regression is observed in all-Claude tasklists.

# 6. Timeline estimates per phase

## Recommended implementation sequence

1. **Phase 0 — Architecture confirmation and design freeze:** 0.5 day
2. **Phase 1 — Data model and parser extensions:** 1-1.5 days
3. **Phase 2 — Classifier registry foundation:** 0.5-1 day
4. **Phase 3 — Preflight executor implementation:** 1.5-2 days
5. **Phase 4 — Evidence artifact and result generation:** 1 day
6. **Phase 5 — Main sprint orchestration integration:** 1 day
7. **Phase 6 — Test hardening, performance validation, rollback proof:** 1-1.5 days

## Total estimated timeline
- **6.5-8.5 engineering days**

## Milestone checkpoints
1. **End of Day 1:** parser/model design finalized and partly implemented
2. **Midpoint:** executor and classifier registry working in isolation
3. **Before final merge:** compatibility, rollback, and performance proof complete

# 7. Recommended architectural decisions

1. **Keep preflight phase-scoped, not task-scoped.**
   - Matches current requirements.
   - Avoids premature mixed-mode orchestration complexity.

2. **Treat report compatibility as the core contract.**
   - This reduces integration risk more than any other decision.

3. **Fail closed on invalid configuration.**
   - Invalid `Execution Mode` and missing classifier names should stop execution early.

4. **Keep executor security conservative.**
   - Maintain `shell=False`.
   - Never enable shell interpretation to “fix” quoting issues.

5. **Optimize for reversibility.**
   - One orchestration hook, minimal branching, and isolated new code paths.

# 8. Final recommendation

Proceed with implementation as a **single moderate-sized feature branch** organized around the phases above. From an architecture standpoint, the safest path is to:

1. extend parsing first,
2. build the classifier registry second,
3. implement preflight execution third,
4. then integrate only after report compatibility is proven.

The decisive success factor is not subprocess execution itself; it is **maintaining exact compatibility with existing sprint status/report contracts while introducing a zero-token, pre-sprint execution path**.
