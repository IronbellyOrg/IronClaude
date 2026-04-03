# Synthesis Report: Problem Statement and Current State Analysis

**Date:** 2026-04-03
**Research Question:** How individual tasks within a tasklist phase are fed to worker agents, executed, verified, and tracked in the IronClaude sprint pipeline -- and whether verification gaps found in preliminary analysis are real or exist in an unexamined layer.
**Source Files:** `research/01` through `research/08`, `gaps-and-questions.md`

---

## Section 1: Problem Statement

### 1.1 Research Question

The sprint pipeline (`superclaude sprint run`) executes tasklist phases by spawning headless `claude --print -p` subprocesses. The central question is: **how are individual tasks within a tasklist phase fed to worker agents, executed, verified, and tracked** -- and whether verification gaps identified in preliminary analysis are genuine deficiencies or capabilities that exist in an unexamined layer (e.g., implicit governance via CLAUDE.md auto-loading, skill protocols, or the pipeline QA module).

### 1.2 Why This Matters

The sprint executor has a **two-path architecture** routed by the presence of `### T<PP>.<TT>` headings in phase files. Preliminary analysis suggested that Path A (per-task execution) sends a severely underspecified 3-line prompt to workers, while Path B (whole-phase execution) sends a rich ~40-line prompt with full behavioral governance. If true, this means the standard execution path for all protocol-generated phase files operates with fundamentally less guidance than the fallback path -- an architectural inversion.

### 1.3 Scope of Investigation

| Dimension | Coverage |
|-----------|----------|
| Executor path routing | How `execute_sprint()` decides per-task vs whole-phase (`research/01`) |
| Tasklist format alignment | Whether generated files always trigger per-task path (`research/02`) |
| Worker governance | What behavioral context a `claude --print -p` subprocess inherits (`research/03`) |
| Post-task verification | What the wiring and anti-instinct hooks actually check (`research/04`) |
| Pipeline QA systems | Why sprint does not use `execute_pipeline()` (`research/05`) |
| PM agent / execution modules | Whether pm_agent/ or execution/ participate in sprint (`research/06`) |
| Design intent and version history | What was planned vs implemented across v3.1-v3.2 (`research/07`) |
| Progress tracking and resume | What state survives crashes and at what granularity (`research/08`) |
| Cross-file gaps | Contradictions and missing cross-references (`gaps-and-questions.md`) |

### 1.4 Key Preliminary Findings (Resolved by Research)

| Preliminary Concern | Resolution | Source |
|---------------------|------------|--------|
| Path A prompt is a bare 3-line string with no governance | **Partially true, partially misleading.** The 3-line prompt IS minimal, but the worker subprocess inherits extensive governance via CLAUDE.md auto-loading, user settings, and all installed skills/agents. The prompt IS the gateway -- `/sc:task-unified` in Path B triggers a full behavioral protocol -- but Path A lacks this invocation entirely. | `research/01` Section 4b, `research/03` Sections 2-6 |
| Verification gates catch task-level acceptance criteria | **False.** Neither the wiring gate (codebase-level structural check) nor the anti-instinct gate (roadmap-artifact-specific frontmatter check) verifies whether a task accomplished its stated goal. The anti-instinct gate passes vacuously for sprint tasks. | `research/04` Section 4 |
| The pipeline module's QA systems handle sprint verification | **False.** Sprint does NOT call `execute_pipeline()`. It uses individual pipeline components directly (`gate_passed()`, `DeferredRemediationLog`) but bypasses retry, sequencing, and trailing gate machinery. This is a known, intentional deviation (BUG-009/P6). | `research/05` Section 3.1 |
| pm_agent/ or execution/ modules provide runtime sprint verification | **False.** pm_agent/ modules are pytest fixtures only. execution/ is an unused standalone prototype with zero external consumers. Neither is wired into sprint. | `research/06` Sections 2-4 |

---

## Section 2: Current State Analysis

### 2.1 Executor Path Routing

**Source:** `research/01-sprint-executor-path-routing.md`

#### Architecture Overview

```
execute_sprint()                          [executor.py:1112]
  |
  +-- for phase in config.active_phases:
       |
       +-- _parse_phase_tasks(phase, config)    [executor.py:1095]
       |     |
       |     +-- parse_tasklist(content)         [config.py:306]
       |           uses _TASK_HEADING_RE         [config.py:281]
       |
       +-- if tasks:  -----> PATH A: execute_phase_tasks()      [executor.py:912]
       |                       |
       |                       +-- per task: _run_task_subprocess()  [executor.py:1053]
       |                       |     constructs ClaudeProcess via __new__ bypass
       |                       |     sends 3-line prompt
       |                       |
       |                       +-- run_post_task_wiring_hook()       [executor.py:450]
       |                       +-- run_post_task_anti_instinct_hook() [executor.py:787]
       |
       +-- else:      -----> PATH B: ClaudeProcess(config, phase)   [process.py:97]
                               calls build_prompt() -> rich ~40-line prompt
                               full lifecycle hooks + env_vars isolation
```

#### Path Decision Matrix

| Condition | Path | Prompt Quality | Lifecycle Hooks | Output Isolation |
|-----------|------|----------------|-----------------|------------------|
| Phase file has `### T<PP>.<TT>` headings | A (per-task) | 3-line minimal | None (bypassed via `__new__`) | Collision -- all tasks share `config.output_file(phase)` |
| Phase file lacks task headings | B (whole-phase) | ~40-line rich with `/sc:task-unified` | Full (spawn, signal, exit) | Per-phase isolation dir |
| Phase file does not exist | B (whole-phase) | ~40-line rich | Full | Per-phase isolation dir |

#### Critical Code Points

| Symbol | File | Line | Role |
|--------|------|------|------|
| `execute_sprint()` | `src/superclaude/cli/sprint/executor.py` | 1112 | Main orchestration loop |
| `_parse_phase_tasks()` | `src/superclaude/cli/sprint/executor.py` | 1095 | Gate function: returns `list[TaskEntry] | None` |
| `_TASK_HEADING_RE` | `src/superclaude/cli/sprint/config.py` | 281 | Regex: `^###\s+(T\d{2}\.\d{2})\s*(?:--\|-\u2014\|\u2014)\s*(.+)` |
| `parse_tasklist()` | `src/superclaude/cli/sprint/config.py` | 306 | Extracts `TaskEntry` list from phase file content |
| `execute_phase_tasks()` | `src/superclaude/cli/sprint/executor.py` | 912 | Per-task loop with budget, hooks, gate evaluation |
| `_run_task_subprocess()` | `src/superclaude/cli/sprint/executor.py` | 1053 | Sends 3-line prompt via `__new__` bypass pattern |
| `build_prompt()` | `src/superclaude/cli/sprint/process.py` | 123 | Rich prompt builder (Path B only) |
| `build_task_context()` | `src/superclaude/cli/sprint/process.py` | 245 | **Dead code** -- 0 callers, designed for cross-task context injection |

#### Confirmed Gaps (from `research/01`)

| Gap ID | Description | Severity |
|--------|-------------|----------|
| R01-G1 | Path A prompt is 3 lines: task ID, phase file path, description. No behavioral instructions, no compliance tier, no scope boundary, no result file contract. | CRITICAL |
| R01-G2 | `build_task_context()` + 2 helper functions (~130 lines) are dead code with 0 callers. Cross-task context injection was designed but never wired. | CRITICAL |
| R01-G3 | All per-task outputs collide on `config.output_file(phase)` -- only last task's output survives on disk. | IMPORTANT |
| R01-G4 | `_run_task_subprocess()` uses `__new__` + base `__init__()` to bypass sprint `ClaudeProcess.__init__()`, skipping lifecycle hooks and env_vars isolation. | IMPORTANT |

---

### 2.2 Tasklist Generation Format

**Source:** `research/02-tasklist-generation-format.md`

#### Format Chain of Custody

| Authority | Location | Rule |
|-----------|----------|------|
| SKILL.md Section 4.5 | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` lines 276-280 | Task IDs are zero-padded `T<PP>.<TT>` -- no alternative format |
| Phase template | `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` lines 22-24 | `### T<PP>.<TT> -- <Task Title>` heading format |
| File emission rules | `src/superclaude/skills/sc-tasklist-protocol/rules/file-emission-rules.md` line 18 | Sprint CLI-compatible naming |
| Sprint regex | `src/superclaude/cli/sprint/config.py` line 281 | `_TASK_HEADING_RE` matches `### T<PP>.<TT>` with `--`/em-dash variants |

#### Empirical Verification

6 actual generated phase files sampled across releases v2.24.5 through v3.1 all use `### T<PP>.<TT> -- <Title>` with zero deviations. 100% match rate against `_TASK_HEADING_RE`.

#### Path A/B Implications

- **Path A is the standard path** for ALL protocol-generated phase files (they always contain `### T<PP>.<TT>` headings).
- **Path B is effectively unreachable** for well-formed generated files. It exists as a safety net for manually-authored or legacy content.
- **No runtime validator** checks generated phase files against the regex before emission. Generation is LLM-driven (inference-based), so format correctness depends entirely on the SKILL.md prescription and template adherence.

---

### 2.3 Worker Session Governance

**Source:** `research/03-worker-session-governance.md`

#### What the Worker Subprocess Receives

```
claude --print --verbose --dangerously-skip-permissions \
       --no-session-persistence --tools default \
       --max-turns <N> --output-format stream-json -p <prompt>
```

**Critical absences in the command:**

| Flag NOT Used | Governance Impact |
|---------------|-------------------|
| `--bare` | CLAUDE.md auto-discovery, hooks, plugin sync, auto-memory, skills ALL remain active |
| `--disable-slash-commands` | All installed skills resolve normally |

#### 4-Layer Governance Stack

| Layer | Source | Active in Worker? |
|-------|--------|-------------------|
| User CLAUDE.md | `~/.claude/CLAUDE.md` | Yes -- full SuperClaude framework rules (UV-only, parallel-first, confidence checks, 10 core rules) |
| Project CLAUDE.md | `<working-dir>/CLAUDE.md` | Likely yes if Claude Code traverses upward from `CLAUDE_WORK_DIR` isolation dir (S4/S5 unresolved) |
| User settings.json | `~/.claude/settings.json` | Yes -- model, effort, thinking mode, agent teams flag |
| Installed skills | `~/.claude/skills/` (15 packages) | Yes -- all available for invocation; `/sc:task-unified` triggers full behavioral protocol |

#### Isolation Implementation vs Design

| Isolation Layer | Designed? | Implemented? | Source |
|-----------------|-----------|-------------|--------|
| `CLAUDE_WORK_DIR` | Yes (`IsolationLayers` dataclass, executor.py:108) | Yes (applied at executor.py:1252) | `research/03` Section 3 |
| `GIT_CEILING_DIRECTORIES` | Yes (defined in dataclass) | **No** -- dead code | `research/03` Section 3 |
| `CLAUDE_PLUGIN_DIR` | Yes (defined in dataclass) | **No** -- dead code | `research/03` Section 3 |
| `CLAUDE_SETTINGS_DIR` | Yes (defined in dataclass) | **No** -- dead code | `research/03` Section 3 |

#### Key Nuance: Path A vs Path B Governance

| Governance Element | Path A (per-task) | Path B (whole-phase) |
|--------------------|-------------------|----------------------|
| CLAUDE.md rules | Inherited implicitly | Inherited implicitly |
| `/sc:task-unified` invocation | **NOT in prompt** | In prompt (line 1 of `build_prompt()`) |
| Sprint Context block | **NOT in prompt** | In prompt |
| Execution Rules (tier behavior) | **NOT in prompt** | In prompt |
| Scope Boundary ("STOP after completing") | **NOT in prompt** | In prompt |
| Result File instructions | **NOT in prompt** | In prompt |

**Resolution of preliminary concern:** The worker IS NOT a bare LLM call -- it operates under full SuperClaude governance via auto-loaded CLAUDE.md and settings. However, Path A workers lack the explicit behavioral instructions that Path B workers receive via `build_prompt()`. The implicit governance (CLAUDE.md rules, skill availability) does not compensate for the missing `/sc:task-unified` invocation, Sprint Context, or scope boundaries in Path A.

---

### 2.4 Post-Task Verification Gates

**Source:** `research/04-post-task-verification-gates.md`

#### Hook #1: Wiring Gate (`run_post_task_wiring_hook`)

| Aspect | Detail |
|--------|--------|
| File | `src/superclaude/cli/sprint/executor.py` lines 450-611 |
| Scope | Scans `config.release_dir` (entire codebase), NOT individual task output |
| Checks | G-001: Unwired callables (AST), G-002: Orphan modules (imports), G-003: Broken registries |
| Task-aware? | **No** -- identical analysis regardless of which task ran |
| Mode matrix | off/shadow/soft/full; only `full` can set `TaskStatus.FAIL` |
| Remediation | Prompt formatted by `_format_wiring_failure()` but **never sent to a subprocess** -- stub for v3.3 |

#### Hook #2: Anti-Instinct Gate (`run_post_task_anti_instinct_hook`)

| Aspect | Detail |
|--------|--------|
| File | `src/superclaude/cli/sprint/executor.py` lines 787-909 |
| Scope | Reads individual task's `output_path` |
| Checks | YAML frontmatter: `undischarged_obligations` (must be 0), `uncovered_contracts` (must be 0), `fingerprint_coverage` (must be >= 0.7) |
| Task-aware? | File-specific, but criteria are **hardcoded for roadmap audit artifacts** |
| Sprint task behavior | **Passes vacuously** -- sprint tasks produce code, not markdown with this frontmatter |
| Mode matrix | off/shadow/soft/full |
| Remediation | Deferred to v3.2 per SPEC-DEVIATION BUG-009 |

#### Cross-Reference Resolution (Gap S1 from `gaps-and-questions.md`)

`research/01` lists the anti-instinct hook as "functioning" in the execution flow. `research/04` found it passes vacuously for sprint tasks. **Resolution:** The hook fires and executes its logic correctly, but its criteria are domain-specific to roadmap artifacts. For sprint tasks, it is architecturally a no-op.

#### Verification Gap Summary

| Question | Answer |
|----------|--------|
| Do the gates verify task acceptance criteria? | **No** -- neither gate checks whether the task accomplished its stated goal |
| Do the gates catch regressions introduced by a task? | Wiring gate: partially (catches structural breakage). Anti-instinct: no. |
| Is there any semantic completion check? | **No** -- `TaskEntry` has no `acceptance_criteria` field |
| Is extension feasible? | Yes -- `gate_passed()` + `GateCriteria` + `SemanticCheck` pattern is cleanly extensible (`research/04` Section 5) |

---

### 2.5 Pipeline QA Systems

**Source:** `research/05-pipeline-qa-systems.md`

#### Pipeline Module Components

| File | Purpose | Used by Sprint? |
|------|---------|-----------------|
| `src/superclaude/cli/pipeline/executor.py` | Generic step sequencer with retry, gates, parallel dispatch | **No** |
| `src/superclaude/cli/pipeline/gates.py` | Pure-Python gate validation (`gate_passed()`) | **Yes** -- called directly |
| `src/superclaude/cli/pipeline/models.py` | Shared dataclasses (Step, GateCriteria, GateMode, etc.) | **Yes** -- types used |
| `src/superclaude/cli/pipeline/deliverables.py` | Behavioral detection and Implement/Verify decomposition | **No** |
| `src/superclaude/cli/pipeline/trailing_gate.py` | Async gate evaluation, deferred remediation, `attempt_remediation()` | **Partially** -- `DeferredRemediationLog` used, `attempt_remediation()` not called |
| `src/superclaude/cli/pipeline/process.py` | Claude subprocess wrapper (base class) | **Yes** -- base for sprint `ClaudeProcess` |

#### Who Calls `execute_pipeline()`

| Consumer | File | Used? |
|----------|------|-------|
| Roadmap executor | `src/superclaude/cli/roadmap/executor.py` line 2328 | Yes |
| Roadmap validate | `src/superclaude/cli/roadmap/validate_executor.py` line 407 | Yes |
| Tasklist executor | `src/superclaude/cli/tasklist/executor.py` line 256 | Yes |
| **Sprint executor** | `src/superclaude/cli/sprint/executor.py` | **Never** |

#### Why Sprint Diverges (5 reasons from `research/05` Section 5)

1. **TUI integration** -- `execute_pipeline()` has no TUI callback hooks for `SprintTUI`/`OutputMonitor`
2. **Phase-task hierarchy** -- pipeline operates on flat `Step` lists, not phases containing tasks
3. **Output monitoring** -- sprint interleaves stall detection and watchdog logic at ~2 Hz
4. **Signal handling** -- sprint installs its own `SignalHandler` with `shutdown_requested` checks
5. **Preflight phases** -- sprint has python-mode preflight execution orthogonal to pipeline Step model

#### Sprint's Direct-Call Gate Integration

Sprint uses pipeline components individually rather than through `execute_pipeline()`:

| Component | Sprint Usage | Integration Style |
|-----------|-------------|-------------------|
| `gate_passed()` | Called at executor.py:819 in anti-instinct hook | Direct function call |
| `DeferredRemediationLog` | Instantiated at executor.py:1154-1156 | Direct construction |
| `TrailingGateResult` | Built manually at executor.py:844 | Manual construction |
| `resolve_gate_mode()` | Imported at executor.py:428 | Direct function call |
| `SprintGatePolicy` | Implements `TrailingGatePolicy` protocol at executor.py:1159 | Protocol implementation |
| `attempt_remediation()` | **Not called** | Deferred (BUG-009/P6) |

---

### 2.6 PM Agent and Execution Systems

**Source:** `research/06-pm-agent-execution-systems.md`

#### pm_agent/ -- Pytest Fixtures Only

| Module | Purpose | Runtime Consumers |
|--------|---------|-------------------|
| `ConfidenceChecker` (`src/superclaude/pm_agent/confidence.py`, 273 lines) | Pre-implementation confidence scoring (5 weighted boolean dimensions) | pytest plugin only |
| `SelfCheckProtocol` (`src/superclaude/pm_agent/self_check.py`, 250 lines) | Post-implementation evidence validation ("The Four Questions") | pytest plugin only |
| `ReflexionPattern` (`src/superclaude/pm_agent/reflexion.py`, 345 lines) | Error learning via JSONL (`solutions_learned.jsonl`) with Jaccard matching | pytest plugin only |
| `TokenBudgetManager` (`src/superclaude/pm_agent/token_budget.py`, 86 lines) | Simple counter with complexity tiers | pytest plugin only |

#### execution/ -- Unused Standalone Prototype

| Module | Purpose | External Consumers |
|--------|---------|-------------------|
| `ReflectionEngine` (`src/superclaude/execution/reflection.py`, 401 lines) | 3-stage pre-execution confidence (clarity 50%, mistakes 30%, context 20%) | **Zero** |
| `SelfCorrectionEngine` (`src/superclaude/execution/self_correction.py`, 426 lines) | Failure categorization + prevention rules via keyword matching | **Zero** |
| `ParallelExecutor` (`src/superclaude/execution/parallel.py`, 330 lines) | Dependency-aware parallel execution via topological sort + ThreadPoolExecutor | **Zero** |
| `intelligent_execute` (`src/superclaude/execution/__init__.py`, 228 lines) | Top-level orchestrator: Reflect -> Plan -> Execute -> Self-Correct | **Zero** |

#### Redundancy Across Error-Learning Systems

| System | Storage | Used by Sprint? |
|--------|---------|-----------------|
| `ReflexionPattern` (pm_agent) | `docs/memory/solutions_learned.jsonl` | No |
| `SelfCorrectionEngine` (execution) | `docs/memory/reflexion.json` | No |
| `DiagnosticCollector` + `FailureClassifier` (sprint) | Sprint's own format | Yes (purpose-built) |

**Verdict:** Neither pm_agent/ nor execution/ participates in sprint task execution. Sprint has its own purpose-built equivalents. The execution/ package is effectively dead code from a runtime perspective.

---

### 2.7 Design Intent and Version History

**Source:** `research/07-design-intent-version-history.md`

#### Verification Layers: Planned vs Implemented

| Layer | Version | Status | Key Evidence |
|-------|---------|--------|-------------|
| 1. Phase-level (exit code, EXIT_RECOMMENDATION, status classification) | Original | **Implemented** | executor.py main loop |
| 2. Per-task delegation + anti-instinct gate + TurnLedger budget | v3.1 | **Implemented** | executor.py:1201 (`# v3.1-T04`), executor.py:787-909 |
| 3. Post-phase wiring verification + scope-based gate modes | v3.2 | **Implemented** | executor.py:735-784, executor.py:1222/1432 (`# v3.2-T02`) |
| 4. Full retry-once remediation via `attempt_remediation()` | v3.3 (planned) | **Deferred** | BUG-009/P6; inline fail logic used instead |

#### Deferred Task Inventory (from outstanding tasklist)

| Category | Count | Examples |
|----------|-------|---------|
| Integration tests for production sprint path | 3 | OT-08 (execute_sprint E2E), OT-10 (TurnLedger threading), OT-13 (shadow mode E2E) |
| Unit tests for gate/KPI systems | 3 | OT-09 (budget scenarios), OT-11 (resolve_wiring_mode), OT-12 (KPI fields) |
| Regression/performance | 2 | OT-14 (p95 < 5s benchmark), OT-17 (full regression) |
| Audit | 1 | OT-18 (gap closure audit) |

#### Implementation Timeline Anomaly

Tasks T04 (v3.1, per-task delegation) and T02 (v3.2, wire post-phase hook) were both marked SKIPPED/PARTIAL in their respective QA reflections (2026-03-21) but exist in the current codebase with version-tagged comments. They were implemented in a subsequent pass, not during the original gap remediation sprints.

---

### 2.8 Progress Tracking and Resume

**Source:** `research/08-progress-tracking-resume.md`

#### Logging Granularity

| Event Type | Written to JSONL? | Written to MD? | Granularity |
|------------|-------------------|----------------|-------------|
| `sprint_start` | Yes | Yes (header) | Sprint-level |
| `phase_start` | Yes | No | Phase-level |
| `phase_complete` | Yes | Yes (table row) | Phase-level |
| `phase_interrupt` | Yes | No | Phase-level |
| `sprint_complete` | Yes | Yes (footer) | Sprint-level |
| `task_start` | **No** | **No** | -- |
| `task_complete` | **No** | **No** | -- |

#### State Persistence on Crash

| State Category | Persisted? | Mechanism |
|----------------|-----------|-----------|
| Phase completion events | Yes | Append-mode JSONL (`execution-log.jsonl`) |
| Phase output/error files | Yes | Subprocess I/O redirection |
| Phase result files | Yes | `_write_executor_result_file()` after phase completes |
| `DeferredRemediationLog` | Yes (if flushed) | `remediation.json` |
| Individual `TaskResult` objects | **No** | In-memory list in `execute_phase_tasks()` |
| `TurnLedger` state | **No** | In-memory only |
| `ShadowGateMetrics` | **No** | In-memory only |
| Which task within a phase last completed | **No** | No checkpoint mechanism |

#### Resume Mechanism

| Aspect | Current State |
|--------|---------------|
| CLI flag | `--start <phase_number>` (skips entire phases) |
| Granularity | **Phase-level only** |
| `--resume` flag | Does not exist on CLI |
| `build_resume_output()` | Defined at models.py:633, generates `--resume <task_id>` commands -- **dead code** |
| `aggregate_task_results()` | Defined at executor.py:298 -- **dead code** |
| `read_status_from_log()` | Stub (prints placeholder message) |
| Crash scenario | Mid-phase crash loses all intra-phase task progress; resume re-executes entire phase |

#### `.roadmap-state.json` Clarification

`.roadmap-state.json` is a **roadmap pipeline artifact**, NOT a sprint progress tracker. Sprint neither reads from nor writes to this file during execution. It is used only as a pre-flight fidelity gate (`_check_fidelity()` in commands.py:36-68) and a directory detection heuristic.

---

### 2.9 Consolidated Gap Registry (Raw)

The following table merges all confirmed gaps across research files, with cross-references resolved per `gaps-and-questions.md`. These are raw research findings with research-file-local IDs. The authoritative, curated gap analysis with canonical IDs (G-01 through G-10) is in Section 4 (synth-02-target-gaps.md). Severity labels here use research-file vocabulary (CRITICAL/IMPORTANT/MINOR); Section 4 uses the standard scale (CRITICAL/HIGH/MEDIUM).

| Synth-01 ID | Section 4 ID | Mapping Note |
|-------------|-------------|--------------|
| R-01 | G-01 | Prompt enrichment |
| R-02 | (included in G-05) | Dead code -- build_task_context |
| R-03 | G-07 | Output file collision |
| R-04 | (included in G-01) | __new__ bypass pattern |
| R-05 | G-02, G-03 | Vacuous anti-instinct gate / no acceptance criteria |
| R-06 | G-02, G-03 | No semantic verification |
| R-07 | G-10 | Remediation not wired |
| R-08 | G-08 | Dead isolation layers |
| R-09 | G-10 | attempt_remediation not called |
| R-10 | G-06 | No task-level logging |
| R-11 | G-06 | No task-level checkpoint |
| R-12 | (dead code inventory) | build_resume_output dead code |
| R-13 | G-09 | execution/ dead code |
| R-14 | (testing gap) | No integration tests |
| R-15 | (open question) | CLAUDE.md resolution unverified |

| ID | Gap | Severity | Component | Source |
|----|-----|----------|-----------|--------|
| R-01 | Path A sends 3-line prompt with no `/sc:task-unified`, no Sprint Context, no scope boundary | CRITICAL | Executor path routing | `research/01` Section 4b |
| R-02 | `build_task_context()` + 2 helpers (~130 lines) are dead code with 0 callers | CRITICAL | Executor path routing | `research/01` Section 6 |
| R-03 | Per-task outputs collide on same file path; only last task survives | IMPORTANT | Executor path routing | `research/01` Section 4d |
| R-04 | `_run_task_subprocess()` bypasses sprint `ClaudeProcess.__init__()` via `__new__` | IMPORTANT | Executor path routing | `research/01` Section 4c |
| R-05 | Anti-instinct gate passes vacuously for sprint tasks (expects roadmap-artifact frontmatter) | IMPORTANT | Verification gates | `research/04` Section 2.3 |
| R-06 | Neither gate verifies task acceptance criteria; `TaskEntry` has no `acceptance_criteria` field | CRITICAL | Verification gates | `research/04` Section 4 |
| R-07 | Remediation prompts formatted but never sent to subprocess (wiring + anti-instinct hooks) | IMPORTANT | Verification gates | `research/04` Sections 1.4, 2.5 |
| R-08 | 3 of 4 isolation layers are dead code (`GIT_CEILING_DIRECTORIES`, `CLAUDE_PLUGIN_DIR`, `CLAUDE_SETTINGS_DIR`) | IMPORTANT | Worker governance | `research/03` Section 3 |
| R-09 | `attempt_remediation()` exists in pipeline but is never called from sprint (BUG-009/P6) | IMPORTANT | Pipeline QA | `research/05` Section 5.3 |
| R-10 | Sprint has no task-level JSONL logging; all `TaskResult` data is in-memory only | IMPORTANT | Progress tracking | `research/08` Section 1 |
| R-11 | No task-level checkpoint; crash mid-phase loses all intra-phase progress | IMPORTANT | Progress tracking | `research/08` Section 5 |
| R-12 | `build_resume_output()` and `aggregate_task_results()` are dead code | MINOR | Progress tracking | `research/08` Section 4 |
| R-13 | execution/ package (4 modules, ~1385 lines) has zero external consumers | MINOR | PM agent systems | `research/06` Section 2.2 |
| R-14 | No integration tests for production sprint path (OT-08 through OT-18 all deferred) | CRITICAL | Design intent | `research/07` Finding 4 |
| R-15 | CLAUDE.md resolution behavior with `CLAUDE_WORK_DIR` is unverified (S4/S5 in gaps log) | IMPORTANT | Worker governance | `gaps-and-questions.md` S4/S5 |

---
