# Synthesis Report: Options Analysis and Recommendation

**Date:** 2026-04-03
**Sections:** 6 (Options Analysis), 7 (Recommendation)
**Source Files:** `research/01` through `research/08`, `gaps-and-questions.md`
**Research Question:** Based on identified gaps, propose at least 3 options for closing the per-task verification gap in the sprint execution pipeline.

---

## Section 6: Options Analysis

### 6.0 Gap Summary (Context for Options)

The research established five confirmed gaps in the sprint executor's Path A (per-task execution). For readability, this section uses short IDs (G1-G5) that map to the full Gap Analysis IDs in Section 4 as follows:

| # | Section 4 ID | Gap | Evidence |
|---|-------------|-----|----------|
| G1 | G-01 | **3-line prompt**: `_run_task_subprocess()` sends only task ID, title, and description -- no `/sc:task-unified` invocation, no Sprint Context, no Execution Rules, no scope boundary | `executor.py:1053-1070` (File 01, Section 4b) |
| G2 | G-07 | **Output file collision**: All tasks in a phase write to the same `config.output_file(phase)`, destroying earlier task artifacts | `executor.py:1070-1085` (File 01, Section 4d) |
| G3 | G-05 | **`build_task_context()` dead code**: 3 functions (~130 lines) for cross-task context injection exist but have zero callers | `process.py:245-370` (File 01, Section 6) |
| G4 | G-02, G-03 | **Anti-instinct gate is a no-op for sprint tasks**: Passes vacuously because sprint task outputs lack roadmap-specific frontmatter fields. No semantic verification or acceptance criteria checking exists. | `executor.py:828-830` (File 04, Section 2.3) |
| G5 | G-06 | **No per-task progress logging**: `SprintLogger` writes phase-level events only; `TaskResult` objects are in-memory only; crash loses all intra-phase state | `logging_.py:12-184` (File 08, Sections 1-4) |

Each option below addresses a subset of these gaps. All three options are additive -- Option B includes Option A, Option C includes Option B.

---

### 6.1 Option A: Minimal -- Enrich Path A Prompt + Fix Output File Collision

**Closes:** G1 (3-line prompt), G2 (output file collision)
**Does NOT close:** G3, G4, G5

#### Description

Replace the 3-line prompt in `_run_task_subprocess()` with a rich prompt that mirrors Path B's `build_prompt()` output, scoped to a single task. Fix the output file path to include the task ID so each task writes to a unique file.

#### How It Works

**Prompt enrichment** (modifies `_run_task_subprocess()` at `executor.py:1053`):

The current prompt is:
```
Execute task {task.task_id}: {task.title}
From phase file: {phase.file}
Description: {task.description}
```

The enriched prompt would prepend `/sc:task-unified` and append Sprint Context, Execution Rules, and scope boundary instructions, matching the structure in `ClaudeProcess.build_prompt()` at `process.py:123`. The key difference from Path B is that the prompt targets a single task rather than "Execute all tasks in @{phase_file}". The existing `build_prompt()` method in `process.py` would NOT be reused directly (it targets whole-phase execution), but its structure would be replicated in a new `build_task_prompt()` helper or by parameterizing the existing function.

**Output file fix** (modifies `_run_task_subprocess()` at `executor.py:1070-1085`):

Replace:
```python
output_file=config.output_file(phase)
error_file=config.error_file(phase)
```
With task-scoped paths. This requires either:
- A new `SprintConfig.task_output_file(phase, task_id)` method (add to `models.py`), or
- Inline path construction: `config.results_dir / f"phase-{phase.number}-{task.task_id}-output.txt"`

The `TaskResult` dataclass already has an `output_path` field (`models.py:26`) that can store the per-task path.

**ClaudeProcess construction fix** (modifies `_run_task_subprocess()` at `executor.py:1070-1085`):

The current `__new__` bypass pattern skips sprint `ClaudeProcess.__init__()`. Option A does NOT fix this -- it enriches the prompt string passed to the base `_Base.__init__()` call. The bypass pattern remains as-is. This is deliberate: fixing the construction pattern is higher risk and not required for prompt enrichment.

#### Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| **Effort** | Low (1-2 days) | ~50 lines changed across 2 files |
| **Risk** | Low | Prompt change is additive; output path change is isolated |
| **Reuse** | Medium | New prompt structure can be extracted into a shared helper |
| **Files affected** | 2 | `executor.py` (prompt + output path), `models.py` (optional: `task_output_file()` method) |

| Pros | Cons |
|------|------|
| Immediate behavioral improvement -- workers receive compliance tier, scope boundary, and context | Does not add any verification of task completion |
| Fixes data loss from output file collision | `build_task_context()` remains dead code; no cross-task context |
| Low risk -- changes are in a single function | Anti-instinct gate still passes vacuously for sprint tasks |
| Path A prompt parity with Path B | No crash recovery improvement; no per-task logging |

---

### 6.2 Option B: Moderate -- Option A + Pipeline Gate Integration + Task Context + Progress Logging

**Closes:** G1 (prompt), G2 (output collision), G3 (dead context code), G4 (vacuous gate), G5 (progress logging)
**Does NOT close:** Full checkpoint/resume (addressed in Option C)

#### Description

Everything in Option A, plus: wire the pipeline gate system into the sprint per-task loop, activate `build_task_context()` for cross-task context injection, and add per-task progress logging to the JSONL log.

#### How It Works

**Component 1: Pipeline gate integration into per-task loop**

The pipeline module's `gate_passed()` function (`pipeline/gates.py:20`) is already called by the anti-instinct hook (`executor.py:819`). The problem is that `ANTI_INSTINCT_GATE` criteria (`roadmap/gates.py:1043`) check for roadmap-specific frontmatter fields that sprint tasks never produce.

Option B adds a task-aware gate as a **third post-task hook** in `execute_phase_tasks()` (`executor.py:912+`), following the pattern established by the existing two hooks:

```python
# Existing hooks (executor.py, after each task subprocess completes):
task_result = run_post_task_wiring_hook(task, config, task_result, ...)
task_result, gate_result = run_post_task_anti_instinct_hook(task, config, task_result, ...)
# NEW:
task_result = run_post_task_verification_hook(task, config, task_result, ...)
```

The new hook uses Extension Path B from File 04 (Section 5): a new `run_post_task_verification_hook()` that reads the task's output file and evaluates it against the task's description/deliverables. Since acceptance criteria are natural-language (not pure-Python checkable), this hook would either:
- Use a lightweight `GateCriteria` with STANDARD tier (file exists + non-empty + min lines) as a structural quality check, OR
- Delegate to a brief Claude subprocess that reads the task output and answers "Did this output satisfy the task description?" (more expensive but semantically meaningful)

The `GateCriteria` + `gate_passed()` engine (`pipeline/gates.py`) supports both approaches via its tiered architecture. For the structural approach, a new `SPRINT_TASK_GATE` criteria instance would be defined (analogous to `ANTI_INSTINCT_GATE` but with sprint-appropriate checks). For the subprocess approach, the hook would use the same `ClaudeProcess` pattern as `_run_task_subprocess()` but with a verification prompt.

The hook follows the existing 4-mode rollout pattern (off/shadow/soft/full) via `_resolve_wiring_mode()` (`executor.py:421-447`) and `resolve_gate_mode()` (`pipeline/trailing_gate.py:598`), ensuring it can be activated gradually.

**Component 2: Activate `build_task_context()`**

`build_task_context()` (`process.py:245`) is dead code with zero callers (File 01, Section 6). It was designed to inject prior task results into prompts. Option B wires it into `_run_task_subprocess()`:

1. `execute_phase_tasks()` (`executor.py:912`) already accumulates `results: list[TaskResult]` in its loop
2. Pass `prior_results=results` to `_run_task_subprocess()` (new parameter)
3. Inside `_run_task_subprocess()`, call `build_task_context(prior_results)` to generate a context summary
4. Prepend the context summary to the enriched prompt from Option A

This also activates the two helper functions that are currently dead code:
- `get_git_diff_context()` (`process.py:310`) -- summarizes git changes from prior tasks
- `compress_context_summary()` (`process.py:335`) -- truncates context to fit token budget

**Component 3: Per-task progress logging**

Add `task_start` and `task_complete` events to `SprintLogger` (`logging_.py`):

New methods:
```python
def write_task_start(self, phase: int, task_id: str, task_title: str): ...
def write_task_complete(self, phase: int, task_id: str, status: TaskStatus,
                        duration_seconds: float, gate_outcome: GateOutcome | None): ...
```

Call sites: Inside `execute_phase_tasks()` (`executor.py:912`), before and after each task subprocess. This requires passing the `SprintLogger` instance into `execute_phase_tasks()` (it currently does not receive it -- the logger is held by the caller `execute_sprint()` at `executor.py:1145`).

The JSONL events enable post-mortem analysis of which tasks completed within a crashed phase, even though Option B does not implement task-level resume (that is Option C).

#### Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| **Effort** | Medium (3-5 days) | ~200-300 lines across 4-5 files |
| **Risk** | Medium | Gate integration touches the hot path; context injection adds prompt size; logger threading needs care |
| **Reuse** | High | New gate hook follows established pattern; logger events are generic; `build_task_context()` is already implemented |
| **Files affected** | 5 | `executor.py` (hook call site, logger wiring, context passing), `process.py` (wire `build_task_context()` call), `logging_.py` (new event methods), `models.py` (optional: gate criteria), `gates.py` or new file (SPRINT_TASK_GATE criteria) |

| Pros | Cons |
|------|------|
| Closes all 5 identified gaps at structural level | Verification hook choice (structural vs LLM) has design tradeoffs |
| Activates ~130 lines of purpose-built dead code (`build_task_context()` subsystem) | Context injection increases prompt size per task (token cost) |
| Per-task JSONL logging enables crash forensics | Does not enable task-level resume (crash still re-runs entire phase) |
| Gate rollout modes (shadow/soft/full) allow gradual activation | Medium effort -- more files touched, more integration surface |
| Follows all existing patterns -- no new architectural concepts | `attempt_remediation()` still not wired (deferred to v3.3 per BUG-009) |

---

### 6.3 Option C: Comprehensive -- Option B + Acceptance Criteria Gate + PM Agent + Checkpoint/Resume

**Closes:** G1-G5, plus: acceptance criteria verification using TaskEntry metadata, PM agent integration, per-task checkpoint with task-level resume

#### Description

Everything in Option B, plus: extend `TaskEntry` with structured acceptance criteria, implement a semantic acceptance gate using task metadata, connect PM agent systems for cross-session error learning, and implement per-task checkpoint files enabling task-level crash recovery.

#### How It Works

**Component 1: Extend TaskEntry with acceptance criteria**

The `TaskEntry` dataclass (`models.py:26`) currently has: `task_id`, `title`, `description`, `dependencies`, `command`, `classifier`. File 04 (Section 6, gap #4) confirmed there is no `acceptance_criteria` field.

Option C adds:
```python
@dataclass
class TaskEntry:
    task_id: str
    title: str
    description: str = ""
    dependencies: list[str] = field(default_factory=list)
    command: str = ""
    classifier: str = ""
    acceptance_criteria: list[str] = field(default_factory=list)  # NEW
    tier: str = ""  # NEW -- from tasklist Tier field
```

The `parse_tasklist()` function (`config.py:306`) already extracts fields from the task block using regex. Adding parsers for `**Acceptance Criteria:**` and `| Tier | value |` fields extends the existing pattern.

The tasklist template (`sc-tasklist-protocol/templates/phase-template.md`) already defines these fields in the task block structure -- they are generated but not consumed by the sprint executor.

**Component 2: Semantic acceptance gate**

The third hook from Option B (`run_post_task_verification_hook()`) is enhanced with an LLM-based acceptance check:

1. Read the task's output file (now at a unique per-task path from Option A)
2. Read `task.acceptance_criteria` (now populated from Option C's TaskEntry extension)
3. Construct a verification prompt: "Given these acceptance criteria: [...], and this task output: [...], does the output satisfy all criteria? Answer YES/NO with reasons."
4. Spawn a brief Claude subprocess (low `--max-turns`, e.g., 3) to evaluate
5. Parse the verification result and set `GateOutcome.PASS` or `GateOutcome.FAIL`

This uses the `GateCriteria` extension path from File 04 (Section 5, Extension Path B) -- a new hook specifically for acceptance criteria, since the evaluation requires LLM judgment that does not fit the pure-Python constraint of `gate_passed()`.

Budget impact: Each verification subprocess consumes turns from `TurnLedger`. The hook checks `ledger.can_launch()` before spawning and debits `verification_cost` (a new `SprintConfig` field). Under budget pressure, the gate degrades to structural-only checks (Option B behavior).

**Component 3: PM agent cross-session error learning**

Connect `ReflexionPattern` (`pm_agent/reflexion.py`) as a cross-session error memory for sprint task failures:

1. On task FAIL: call `reflexion_pattern.record_error()` with a dict built from `TaskResult` fields (task_id, title, description, exit_code, failure output snippet)
2. Before each task: call `reflexion_pattern.get_solution()` with the task description to check if a similar task previously failed and was resolved
3. If a solution exists, append it to the task prompt as a "Known Issue" section

This is the most plausible PM agent integration point identified in File 06 (Section 4.2, ReflexionPattern assessment). The adapter layer translates between sprint's `TaskResult` format and `ReflexionPattern`'s `error_info` dict format.

File 06 confirmed that `ConfidenceChecker` and `SelfCheckProtocol` are less useful for sprint integration because they require pre-populated evidence dicts rather than doing actual checks. `ReflexionPattern` is the exception -- it has a functional file-based search (`get_solution()`) and persistent JSONL storage (`docs/memory/solutions_learned.jsonl`).

**Component 4: Per-task checkpoint and resume**

Add per-task checkpoint files written after each task completes:

1. After each task in `execute_phase_tasks()`, write a checkpoint file: `results/.checkpoints/phase-{N}-task-{task_id}.json` containing `TaskResult` serialized fields (status, gate_outcome, turns_consumed, output_path, timing)
2. On resume (new `--resume-from <task_id>` CLI flag on `commands.py:73`), read checkpoint files to determine which tasks in a phase already completed, and skip them
3. Restore `TurnLedger` state from checkpoints (sum of `turns_consumed` across completed tasks)

The dead code `build_resume_output()` (`models.py:633`) already generates `--resume <task_id>` commands but references a CLI flag that does not exist. Option C implements the flag and the checkpoint reader.

Additionally, `aggregate_task_results()` (`executor.py:298`) is dead code that would produce structured per-task reports. Option C activates this function by calling it at the end of each phase within `execute_phase_tasks()`, writing the aggregated report to disk.

#### Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| **Effort** | High (7-10 days) | ~500-700 lines across 7-8 files; new CLI flag; new checkpoint system |
| **Risk** | High | LLM-based verification adds latency + cost; checkpoint/resume is a new state management system; PM agent adapter is untested territory |
| **Reuse** | Very High | Acceptance criteria gate is reusable across pipeline types; checkpoint system generalizes; PM agent adapter establishes a pattern |
| **Files affected** | 8+ | `executor.py`, `process.py`, `logging_.py`, `models.py`, `config.py` (parser), `commands.py` (CLI flag), new checkpoint module, PM agent adapter |

| Pros | Cons |
|------|------|
| Complete solution -- closes all gaps and adds semantic verification | High effort and high risk for a first iteration |
| Activates all dead code: `build_task_context()`, `build_resume_output()`, `aggregate_task_results()` | LLM-based acceptance gate adds per-task latency and turn cost |
| Task-level resume prevents work duplication on crash | Checkpoint/resume is a new state management system with its own failure modes |
| Cross-session error learning via ReflexionPattern | PM agent adapter introduces a new integration surface |
| Establishes patterns for v3.3 `attempt_remediation()` integration | May conflict with planned v3.3 work if design assumptions diverge |

---

### 6.4 Options Comparison

| Dimension | Option A (Minimal) | Option B (Moderate) | Option C (Comprehensive) |
|-----------|--------------------|---------------------|--------------------------|
| **Gaps closed** | G1, G2 | G1, G2, G3, G4, G5 | G1-G5 + acceptance criteria + checkpoint/resume |
| **Effort** | Low (1-2 days) | Medium (3-5 days) | High (7-10 days) |
| **Risk** | Low | Medium | High |
| **Files changed** | 2 | 5 | 8+ |
| **Lines added (est.)** | ~50 | ~200-300 | ~500-700 |
| **Dead code activated** | None | `build_task_context()` + 2 helpers (~130 lines) | + `build_resume_output()` + `aggregate_task_results()` (~200 more lines) |
| **New infrastructure** | None | Per-task JSONL events, verification hook | + Checkpoint files, CLI flag, PM agent adapter, LLM verification |
| **Prompt quality** | Rich (matches Path B) | Rich + cross-task context | Rich + context + known-issue injection |
| **Verification** | None (exit code only) | Structural gate (file exists, non-empty, min lines) | Structural + semantic (LLM acceptance check) |
| **Crash recovery** | Phase-level only | Phase-level (but with per-task forensics) | Task-level resume |
| **Rollout risk** | Deploy immediately | Gate rollout modes (shadow first) | Phased rollout across multiple iterations |
| **v3.3 alignment** | Neutral | Establishes hook pattern for `attempt_remediation()` | May overlap or conflict with v3.3 scope |
| **Test surface** | 1 function modified | 3-4 new test targets | 6+ new test targets |

### 6.5 Key Tradeoff: Verification Depth vs. Execution Cost

The central design tension across options is **verification depth vs. execution cost**:

- **Option A** adds zero verification overhead. Workers receive better instructions but completion is still judged by exit code alone.
- **Option B** adds a structural verification gate. This is fast (pure Python, no subprocess) but can only check "did the task produce output?" -- not "did the task produce the RIGHT output?"
- **Option C** adds a semantic verification gate via an LLM subprocess. This answers the right question ("did the output satisfy acceptance criteria?") but costs 2-3 additional turns per task and adds 10-30 seconds of latency per task.

For a sprint with 5 phases x 4 tasks = 20 tasks, the overhead of Option C's LLM verification is ~60 additional turns and ~5-10 minutes of wall-clock time. Whether this is acceptable depends on the sprint's total turn budget and time constraints.

---

## Section 7: Recommendation

### 7.1 Recommended Option: **Option B (Moderate)**

### 7.2 Rationale

Option B is recommended because it closes all five identified gaps at an appropriate effort/risk balance, follows every existing architectural pattern in the codebase, and positions the system for incremental enhancement toward Option C without premature commitment.

**Why not Option A:**

Option A fixes the most visible symptom (the 3-line prompt) and the most damaging data loss (output file collision), but it leaves the verification layer entirely absent. After Option A, the sprint executor still has no way to detect whether a task actually completed its deliverables -- it can only check exit code 0. The anti-instinct gate remains a vacuous no-op. The research found that the "very extensive system" the architect referenced is real but operates at the prompt-governance layer (CLAUDE.md, skill protocols) rather than at the verification layer. Option A enriches the prompt but does not add verification. This leaves a known gap that will require another implementation pass.

**Why not Option C:**

Option C is the complete solution, but it introduces three high-risk subsystems in a single change:

1. **LLM-based acceptance verification** -- This is architecturally novel in the sprint executor. The existing gate system (`gate_passed()`, `GateCriteria`, `SemanticCheck`) is deliberately pure-Python with no LLM calls. Adding an LLM verification subprocess establishes a new pattern that needs careful design (turn budget, timeout, failure handling, prompt engineering for reliable YES/NO answers). Doing this as part of a 7-10 day implementation carries risk of under-engineering the verification prompt and producing noisy results that degrade trust in the gate system.

2. **Checkpoint/resume** -- This is a new state management system. The current sprint executor has no task-level state persistence, and adding it requires careful handling of partial writes, checkpoint corruption, and state reconciliation on resume. The dead code `build_resume_output()` generates `--resume` commands but was never wired in, suggesting the original authors also considered this a significant undertaking. Building this correctly requires dedicated design and testing, not inclusion as one component of a larger change.

3. **PM agent integration** -- File 06 confirmed that pm_agent/ modules are pytest fixtures, not runtime components. Adapting `ReflexionPattern` for sprint integration requires a new adapter layer and introduces a dependency between the sprint executor and a module that was not designed for this purpose. The value is real (cross-session error learning) but the integration risk is elevated because the modules have never been used outside pytest.

**Why Option B:**

Option B achieves the maximum gap closure (5 of 5) at moderate effort while staying entirely within established patterns:

1. **The verification hook follows the exact pattern of the two existing hooks** -- `run_post_task_wiring_hook()` and `run_post_task_anti_instinct_hook()` are the template. A third hook at the same call site, with the same signature, using the same 4-mode rollout matrix (off/shadow/soft/full), is the lowest-risk way to add verification. File 04 (Section 5, Extension Path B) explicitly identified this as "the cleanest extension point."

2. **`build_task_context()` is already implemented and tested** -- Activating dead code is lower risk than writing new code. The three functions (`build_task_context()`, `get_git_diff_context()`, `compress_context_summary()` at `process.py:245-370`) were purpose-built for this exact use case. Wiring them into `_run_task_subprocess()` requires passing `prior_results` through the call chain and calling one function. The implementation is already done; only the plumbing is missing.

3. **Per-task JSONL logging is a minimal extension of SprintLogger** -- Adding two event types (`task_start`, `task_complete`) to an existing logger class, following the exact pattern of `write_phase_start()` and `write_phase_result()`, is straightforward. The logger already manages the JSONL file handle and timestamp formatting.

4. **The structural verification gate (file exists, non-empty, min lines) is a pragmatic first step** -- It does not answer "did the task do the right thing?" but it answers "did the task produce any output at all?" This catches silent failures (tasks that exit 0 but produce nothing) and gross failures (tasks that crash mid-output). The gate can be upgraded to semantic verification (Option C's LLM approach) in a subsequent iteration once the hook infrastructure is proven.

5. **Gate rollout modes provide a safe deployment path** -- The existing `gate_rollout_mode` system (File 04, Section 1.3; File 05, Section 5.2) allows the new gate to start in `shadow` mode (evaluate but do not fail tasks), collect metrics via `ShadowGateMetrics`, and promote to `soft` then `full` once confidence is established. This is the same graduated rollout used for the wiring gate and anti-instinct gate.

### 7.3 Implementation Sequence

If Option B is adopted, the recommended implementation order is:

| Step | Description | Files | Dependency |
|------|-------------|-------|------------|
| B1 | Enrich `_run_task_subprocess()` prompt (Option A, Component 1) | `executor.py` | None |
| B2 | Fix per-task output file paths (Option A, Component 2) | `executor.py`, `models.py` | None |
| B3 | Wire `build_task_context()` into `_run_task_subprocess()` | `executor.py`, `process.py` | B2 (needs per-task output paths for prior task artifacts) |
| B4 | Add per-task JSONL logging to SprintLogger | `logging_.py`, `executor.py` | None |
| B5 | Add `run_post_task_verification_hook()` with SPRINT_TASK_GATE | `executor.py`, new gate criteria | B2 (needs per-task output file to validate) |

Steps B1, B2, and B4 are independent and can be implemented in parallel. B3 depends on B2. B5 depends on B2.

### 7.4 Path to Option C

Option B is designed as a foundation for Option C. If the structural verification gate in B5 proves insufficient (too many false passes), the upgrade path is:

1. **B5 -> C2**: Replace the structural `SPRINT_TASK_GATE` with an LLM subprocess verification call inside `run_post_task_verification_hook()`. The hook signature, call site, and rollout mode integration remain unchanged.
2. **B4 -> C4**: Extend the per-task JSONL events from B4 into checkpoint files that enable task-level resume. The logging infrastructure provides the foundation.
3. **Independent: C1**: Extend `TaskEntry` with `acceptance_criteria` and update `parse_tasklist()`. This can be done at any time and is consumed by C2.
4. **Independent: C3**: PM agent adapter can be developed and tested in isolation, then wired into the task loop.

This incremental path avoids the "big bang" risk of implementing all of Option C at once.

---

## Appendix: File Reference Index

All files and functions cited in this report, organized by option component:

| Component | File | Function/Symbol | Line (approx.) |
|-----------|------|-----------------|-----------------|
| All options | `src/superclaude/cli/sprint/executor.py` | `_run_task_subprocess()` | 1053 |
| All options | `src/superclaude/cli/sprint/executor.py` | `execute_phase_tasks()` | 912 |
| All options | `src/superclaude/cli/sprint/models.py` | `TaskEntry` dataclass | 26 |
| Option A | `src/superclaude/cli/sprint/process.py` | `ClaudeProcess.build_prompt()` | 123 |
| Option A | `src/superclaude/cli/sprint/models.py` | `SprintConfig.output_file()` | (config method) |
| Option B | `src/superclaude/cli/sprint/executor.py` | `run_post_task_wiring_hook()` | 450 |
| Option B | `src/superclaude/cli/sprint/executor.py` | `run_post_task_anti_instinct_hook()` | 787 |
| Option B | `src/superclaude/cli/sprint/process.py` | `build_task_context()` | 245 |
| Option B | `src/superclaude/cli/sprint/process.py` | `get_git_diff_context()` | 310 |
| Option B | `src/superclaude/cli/sprint/process.py` | `compress_context_summary()` | 335 |
| Option B | `src/superclaude/cli/sprint/logging_.py` | `SprintLogger` | 12 |
| Option B | `src/superclaude/cli/pipeline/gates.py` | `gate_passed()` | 20 |
| Option B | `src/superclaude/cli/pipeline/models.py` | `GateCriteria` dataclass | 68 |
| Option B | `src/superclaude/cli/pipeline/trailing_gate.py` | `resolve_gate_mode()` | 598 |
| Option C | `src/superclaude/cli/sprint/config.py` | `parse_tasklist()` | 306 |
| Option C | `src/superclaude/cli/sprint/commands.py` | `run` subcommand | 73 |
| Option C | `src/superclaude/cli/sprint/models.py` | `build_resume_output()` | 633 |
| Option C | `src/superclaude/cli/sprint/executor.py` | `aggregate_task_results()` | 298 |
| Option C | `src/superclaude/pm_agent/reflexion.py` | `ReflexionPattern` | (class) |
| Option C | `src/superclaude/cli/pipeline/trailing_gate.py` | `attempt_remediation()` | 359 |
