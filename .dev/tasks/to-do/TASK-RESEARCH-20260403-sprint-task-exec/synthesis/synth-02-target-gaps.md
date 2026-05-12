# Synthesis: Target State and Gap Analysis

**Synthesized from:** Research files 01-08, gaps-and-questions.md
**Date:** 2026-04-03
**Scope:** Per-task verification in sprint execution pipeline

---

## Section 3 — Target State

### 3.1 Desired Behavior: Per-Task Semantic Verification

The target state is a sprint execution pipeline where each task, after subprocess completion, undergoes semantic verification against its acceptance criteria before the next task begins. This verification must go beyond exit-code checking to evaluate whether the task accomplished what it was supposed to accomplish.

| Aspect | Target Behavior |
|--------|----------------|
| **Prompt enrichment** | Every per-task subprocess receives a rich prompt equivalent to Path B: `/sc:task-unified` invocation, Sprint Context block, Execution Rules, Scope Boundary, Result File instructions, and prior-task context via `build_task_context()` [01 Section 4b, 5b] |
| **Acceptance criteria field** | `TaskEntry` model includes a structured `acceptance_criteria` field parsed from the phase file, available to both the worker prompt and the post-task verification gate [04 Section 5] |
| **Semantic verification gate** | A post-task hook evaluates whether the task's output satisfies its acceptance criteria, using either LLM-based evaluation or deterministic checks depending on criteria type [04 Section 5, Extension Path B] |
| **Per-task output isolation** | Each task writes to a unique output file path (e.g., `phase-N-task-T01.02-output.txt`) so earlier task artifacts are not overwritten [01 Section 4d] |
| **Context injection** | `build_task_context()` is wired into the per-task prompt builder, giving each worker visibility into what prior tasks in the phase accomplished [01 Section 6] |
| **Progress persistence** | Task-level events (`task_start`, `task_complete`) are written to `execution-log.jsonl` as they occur, enabling crash recovery at task granularity [08 Section 1, 4] |
| **Scope enforcement** | Per-task prompts include explicit scope boundaries ("complete this task and STOP") and result file instructions matching Path B behavior [01 Section 4b] |
| **4-layer isolation** | All four isolation layers (`CLAUDE_WORK_DIR`, `GIT_CEILING_DIRECTORIES`, `CLAUDE_PLUGIN_DIR`, `CLAUDE_SETTINGS_DIR`) are applied per worker subprocess [03 Section 3] |
| **PM agent integration** | `ConfidenceChecker` runs pre-task (skip tasks below threshold), `SelfCheckProtocol` runs post-task (validate evidence), `ReflexionPattern` records failures for cross-session learning [06 Section 4.2] |
| **Pipeline gate wiring** | Sprint uses `execute_pipeline()` or its gate infrastructure (`attempt_remediation()`, `TrailingGateRunner`) for per-task gate evaluation with retry-once semantics [05 Section 6.2, 6.3] |

### 3.2 Success Criteria

| # | Criterion | Measurement |
|---|-----------|-------------|
| SC-1 | Every per-task subprocess receives behavioral instructions equivalent to Path B | Prompt includes `/sc:task-unified`, Sprint Context, Execution Rules, Scope Boundary, Result File path |
| SC-2 | Task completion is evaluated against acceptance criteria, not just exit code | Post-task hook returns PASS/FAIL based on semantic criteria check, not `exit_code == 0` |
| SC-3 | No output file collision between tasks in the same phase | Each task has a unique `output_file` and `error_file` path; all artifacts survive on disk |
| SC-4 | Task-level progress survives process crash | JSONL log contains `task_complete` events; resume can skip completed tasks within a phase |
| SC-5 | Prior-task context is available to subsequent tasks | `build_task_context()` or equivalent injects prior task summaries into the prompt |
| SC-6 | Gate failures trigger retry-once remediation when budget allows | `attempt_remediation()` is called from the sprint execution path, not inline fail logic |
| SC-7 | Worker subprocesses operate under full 4-layer isolation | All four env vars (`CLAUDE_WORK_DIR`, `GIT_CEILING_DIRECTORIES`, `CLAUDE_PLUGIN_DIR`, `CLAUDE_SETTINGS_DIR`) are set per subprocess |

### 3.3 Constraints

| Constraint | Source | Rationale |
|------------|--------|-----------|
| NFR-007: Pipeline module must not import from sprint or roadmap | 05 Section 1.2 | Architectural boundary; pipeline is consumer-agnostic |
| Sprint must retain TUI integration | 05 Section 5.1 | Real-time progress display is a core sprint feature |
| Gate evaluation must respect `gate_rollout_mode` (off/shadow/soft/full) | 04 Section 1.3, 2.4 | Gradual rollout prevents breaking existing workflows |
| Budget-guarded: verification skipped when TurnLedger exhausted | 04 Section 2.5, Gap #5 | Verification quality must degrade gracefully, not crash |
| Acceptance criteria verification likely requires LLM evaluation | 04 Section 5, Path B | Natural-language criteria cannot be checked by pure-Python `gate_passed()` |
| `TaskEntry` parser must remain compatible with `_TASK_HEADING_RE` regex | 02 Section 4 | All generated phase files use `### T<PP>.<TT> -- <Title>` format |
| Phase-level resume via `--start` must continue to work | 08 Section 3 | Task-level resume supplements but does not replace phase-level |

---

## Section 4 — Gap Analysis

### 4.1 Gap Table

| # | Gap | Current State | Target State | Severity | Notes |
|---|-----|---------------|--------------|----------|-------|
| G-01 | **Prompt enrichment** | Path A sends a 3-line prompt (`Execute task T01.01: Title / From phase file: /path / Description: ...`). No `/sc:task-unified`, no Sprint Context, no Execution Rules, no Scope Boundary, no Result File instructions. `_run_task_subprocess()` bypasses `build_prompt()` via `__new__` + base `__init__` pattern. [01 Sec 4b-4c] | Every per-task subprocess receives the same rich ~40-line prompt as Path B: `/sc:task-unified` invocation, Sprint Context block, Execution Rules (tier-based), Scope Boundary, and Result File instructions. [01 Sec 5b] | CRITICAL | Path A is the standard path for all protocol-generated phase files [02 Sec 6]. Path B is unreachable for well-formed tasklist output [02 Sec 7]. This means production sprint runs always use the impoverished 3-line prompt. |
| G-02 | **Semantic verification** | Task pass/fail is determined solely by subprocess exit code: `0=PASS`, `124=INCOMPLETE`, else `FAIL`. No evaluation of whether the task accomplished its stated objective. [01 Sec 4a] | Post-task semantic verification evaluates task output against acceptance criteria. Uses LLM-based evaluation or deterministic checks as appropriate. Returns PASS/FAIL on whether the task delivered what it was supposed to deliver. [04 Sec 5, Path B] | CRITICAL | The two existing post-task hooks do not fill this gap: wiring gate checks codebase structure (task-agnostic) [04 Sec 4], anti-instinct gate checks roadmap-specific frontmatter (vacuous pass for sprint tasks) [04 Sec 2.3]. |
| G-03 | **Acceptance criteria checking** | `TaskEntry` model has `task_id`, `title`, `description`, `dependencies`, `command`, `classifier`. No `acceptance_criteria` field exists. Neither the parser (`parse_tasklist`) nor the post-task hooks consume acceptance criteria. [04 Sec 5, Gap #4] | `TaskEntry` includes an `acceptance_criteria` field parsed from the phase file. A post-task acceptance hook consumes this field to evaluate task completion semantically. [04 Sec 5] | CRITICAL | The `GateCriteria` + `gate_passed()` pattern is extensible [04 Sec 3] but pure-Python semantic checks cannot evaluate natural-language acceptance criteria. LLM evaluation subprocess is required [04 Sec 5, Path B]. |
| G-04 | **Scope enforcement** | Per-task prompts contain no scope boundary instruction. Workers have no instruction to stop after task completion, no result file contract, no compliance tier guidance. [01 Sec 4b] | Prompt includes explicit "After completing this task, STOP immediately" and result file instructions with `EXIT_RECOMMENDATION: CONTINUE/HALT` contract. [01 Sec 5b] | HIGH | Path B includes these instructions. Path A omits them entirely. Workers may drift or continue beyond their assigned task. |
| G-05 | **Context injection** | `build_task_context()` (process.py line 245) is confirmed dead code with zero callers. Related functions `get_git_diff_context()` and `compress_context_summary()` are also dead. [01 Sec 6] | `build_task_context()` or equivalent is wired into the per-task prompt builder. Each worker sees a summary of prior task results (what changed, what was decided, what files were modified). [01 Sec 6, Integration Opp #2] | HIGH | The function is fully implemented (~130 lines, 3 functions) and well-designed. It was purpose-built for this exact use case but never connected to the execution path. Wiring requires passing accumulated `task_results` to `_run_task_subprocess()`. |
| G-06 | **Progress persistence** | Logging is phase-level only. `SprintLogger` writes 4 event types: `sprint_start`, `phase_start`, `phase_complete`, `sprint_complete`. No `task_start` or `task_complete` events. `TaskResult` objects exist only in-memory within `execute_phase_tasks()`. [08 Sec 1, 4] | Task-level events are written to `execution-log.jsonl` as each task starts and completes. `build_resume_output()` generates task-granularity resume commands. Crash recovery can skip completed tasks within a phase. [08 Sec 4, Gap #1] | HIGH | `build_resume_output()` (models.py line 633) already generates `--resume <task_id>` commands but is dead code. `aggregate_task_results()` (executor.py line 298) would produce structured per-task reports but is also dead code. The `--resume` CLI flag does not exist. [08 Sec 4, Gap #2-3] |
| G-07 | **Output file collision** | All tasks in a phase write to the same `config.output_file(phase)` and `config.error_file(phase)`. Each task overwrites the previous task's output. Only the last task's artifacts survive on disk. [01 Sec 4d] | Each task writes to a unique file path (e.g., `config.task_output_file(phase, task_id)`). All per-task artifacts survive for post-mortem analysis and crash recovery. [01 Integration Opp #3] | HIGH | `SprintConfig` could be extended with `task_output_file(phase, task_id)` and `task_error_file(phase, task_id)` methods. Minimal change required. |
| G-08 | **4-layer isolation** | `IsolationLayers` dataclass and `setup_isolation()` function are defined (executor.py lines 108-184) but never called. Only 1 of 4 layers is applied: `CLAUDE_WORK_DIR`. Missing: `GIT_CEILING_DIRECTORIES`, `CLAUDE_PLUGIN_DIR`, `CLAUDE_SETTINGS_DIR`. [03 Sec 3] | All four isolation layers are applied per worker subprocess. Workers cannot traverse git above the isolation directory, do not load user plugins, and use isolated settings. [03 Sec 3] | MEDIUM | The implementation exists as dead code. Wiring requires calling `setup_isolation()` from the subprocess construction path and passing the resulting env vars to `ClaudeProcess`. Risk: over-isolation may break CLAUDE.md discovery and skill loading [03 Sec 2.1, Gap #2]. |
| G-09 | **PM agent integration** | `ConfidenceChecker`, `SelfCheckProtocol`, `ReflexionPattern`, `TokenBudgetManager` are pytest fixtures only. Zero imports from any CLI command, sprint executor, or runtime code. The `execution/` package (`intelligent_execute`, `ReflectionEngine`, `SelfCorrectionEngine`, `ParallelExecutor`) has zero external consumers. [06 Sec 2.1-2.2] | Pre-task confidence assessment gates task execution. Post-task self-check validates evidence. Cross-session error memory records failures and prevents repeat mistakes. [06 Sec 4.2] | MEDIUM | pm_agent modules were designed as pytest fixtures, not runtime components [06 Sec 5]. Their APIs require pre-populated boolean dicts -- they do not DO checking, they validate that someone else already did [06 Sec 4.2]. Sprint has its own purpose-built equivalents: `DiagnosticCollector`, `FailureClassifier`, phase gates [06 Sec 4.3]. Integration would require adapter layers of uncertain value. |
| G-10 | **Pipeline gate wiring** | Sprint does NOT call `execute_pipeline()`. It has its own orchestration loop. Sprint uses individual pipeline components directly (`gate_passed()`, `DeferredRemediationLog`, `TrailingGateResult`, `resolve_gate_mode()`) but bypasses the executor's retry, sequencing, and trailing gate machinery. `attempt_remediation()` is never called from sprint (BUG-009/P6 deferral). [05 Sec 3.1, 5.2-5.3] | Sprint uses `attempt_remediation()` for retry-once semantics on gate failures. `TrailingGateRunner` evaluates gates asynchronously. `SprintGatePolicy.build_remediation_step()` generates remediation prompts. The full pipeline gate infrastructure is connected to the sprint execution path. [05 Sec 6.2] | MEDIUM | Known and intentional deferral (BUG-009/P6). Building blocks exist: `SprintGatePolicy` is instantiated (executor.py line 1106), `attempt_remediation()` has a 6-arg callable API. Main work is wiring sprint's `TurnLedger` and `ClaudeProcess` into the callable interface. Option C hybrid approach (pipeline for task-level, custom for phase-level) is most natural [05 Sec 6.3]. |

### 4.2 Severity Distribution

| Severity | Count | Gaps |
|----------|-------|------|
| CRITICAL | 3 | G-01 (prompt enrichment), G-02 (semantic verification), G-03 (acceptance criteria) |
| HIGH | 4 | G-04 (scope enforcement), G-05 (context injection), G-06 (progress persistence), G-07 (output collision) |
| MEDIUM | 3 | G-08 (isolation), G-09 (PM agent), G-10 (pipeline gate wiring) |

### 4.3 Dependency Relationships Between Gaps

```
G-01 (prompt enrichment) ──> G-04 (scope enforcement)
   Enriching the prompt inherently adds scope boundaries.

G-03 (acceptance criteria field) ──> G-02 (semantic verification)
   Verification gate requires criteria to check against.

G-07 (output collision) ──> G-06 (progress persistence)
   Per-task output files are a prerequisite for meaningful task-level logging.

G-05 (context injection) depends on G-07 (output collision)
   Prior-task context requires prior-task outputs to exist on disk.

G-10 (pipeline gate wiring) depends on G-02 (semantic verification)
   Retry-once remediation only matters if there is meaningful verification to fail.
```

### 4.4 Dead Code Inventory (Existing But Unwired)

These components were purpose-built for the target state but have zero callers in production:

| Component | Location | Purpose | Lines |
|-----------|----------|---------|-------|
| `build_task_context()` | process.py:245 | Inject prior task results into prompts | ~50 |
| `get_git_diff_context()` | process.py:310 | Git diff for context injection | ~25 |
| `compress_context_summary()` | process.py:335 | Summarize context for token budget | ~55 |
| `setup_isolation()` + `IsolationLayers` | executor.py:108-184 | 4-layer subprocess isolation | ~76 |
| `build_resume_output()` | models.py:633 | Task-granularity resume commands | ~40 |
| `aggregate_task_results()` | executor.py:298 | Structured per-task report generation | ~50 |
| `attempt_remediation()` | pipeline/trailing_gate.py:359 | Retry-once gate failure remediation | ~80 |
| `intelligent_execute()` | execution/__init__.py | Reflect-Plan-Execute-Correct orchestrator | ~60 |
| `ReflectionEngine` | execution/reflection.py | Pre-execution confidence check | ~400 |
| `SelfCorrectionEngine` | execution/self_correction.py | Failure analysis and prevention | ~426 |

**Total dead code directly relevant to the target state: ~1,262 lines across 10 components.**

---

*End of synthesis sections 3-4. All facts sourced from research files 01-08 and gaps-and-questions.md.*
