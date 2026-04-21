# Technical Research Report: Sprint Task Execution Pipeline Verification Layers

**Date:** 2026-04-03
**Depth:** Deep
**Research files:** 8 codebase
**Scope:** src/superclaude/cli/sprint/, src/superclaude/cli/pipeline/, src/superclaude/pm_agent/, src/superclaude/execution/, .dev/releases/

---

## Table of Contents

1. [Section 1: Problem Statement](#section-1-problem-statement)
   - 1.1 Research Question
   - 1.2 Why This Matters
   - 1.3 Scope of Investigation
   - 1.4 Key Preliminary Findings (Resolved by Research)
2. [Section 2: Current State Analysis](#section-2-current-state-analysis)
   - 2.1 Executor Path Routing
   - 2.2 Tasklist Generation Format
   - 2.3 Worker Session Governance
   - 2.4 Post-Task Verification Gates
   - 2.5 Pipeline QA Systems
   - 2.6 PM Agent and Execution Systems
   - 2.7 Design Intent and Version History
   - 2.8 Progress Tracking and Resume
   - 2.9 Consolidated Gap Registry (Raw)
3. [Section 3: Target State](#section-3-target-state)
   - 3.1 Desired Behavior: Per-Task Semantic Verification
   - 3.2 Success Criteria
   - 3.3 Constraints
4. [Section 4: Gap Analysis](#section-4-gap-analysis)
   - 4.1 Gap Table (G-01 through G-10)
   - 4.2 Severity Distribution
   - 4.3 Dependency Relationships Between Gaps
   - 4.4 Dead Code Inventory (Existing But Unwired)
5. [Section 5: External Research Findings](#section-5-external-research-findings) -- N/A
6. [Section 6: Options Analysis](#section-6-options-analysis)
   - 6.1 Option A: Minimal
   - 6.2 Option B: Moderate
   - 6.3 Option C: Comprehensive
   - 6.4 Options Comparison
   - 6.5 Key Tradeoff: Verification Depth vs. Execution Cost
7. [Section 7: Recommendation](#section-7-recommendation)
   - 7.1 Recommended Option: Option B (Moderate)
   - 7.2 Rationale
   - 7.3 Implementation Sequence
   - 7.4 Path to Option C
8. [Section 8: Implementation Plan](#section-8-implementation-plan)
   - Phase 1: Prompt Enrichment
   - Phase 2: Output Isolation
   - Phase 3: Context Injection
   - Phase 4: Semantic Verification Gate (includes Option C scope -- annotated)
   - Phase 5: Per-Task Progress Logging (includes Option C scope -- annotated)
   - Integration Checklist
9. [Section 9: Open Questions](#section-9-open-questions) -- 23 questions (6 HIGH, 11 MEDIUM, 6 LOW)
10. [Section 10: Evidence Trail](#section-10-evidence-trail) -- Research files, QA files, synthesis files, source code, design documents

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

The following table merges all confirmed gaps across research files, with cross-references resolved per `gaps-and-questions.md`. These are raw research findings with research-file-local IDs. The authoritative, curated gap analysis with canonical IDs (G-01 through G-10) is in Section 4. Severity labels here use research-file vocabulary (CRITICAL/IMPORTANT/MINOR); Section 4 uses the standard scale (CRITICAL/HIGH/MEDIUM).

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

## Section 3: Target State

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

## Section 4: Gap Analysis

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

## Section 5: External Research Findings

N/A -- All findings in this report are from codebase investigation. Phase 4 web research (planned for Claude `--print -p` subprocess behavior and worker governance patterns) was started but not completed. Research stubs exist at `research/web-01-claude-print-subprocess.md` and `research/web-02-worker-governance-patterns.md` with research questions only. Open questions Q-03 and Q-04 (Section 9) capture the unresolved items that web research was intended to answer.

---

## Section 6: Options Analysis

### 6.0 Gap Summary (Context for Options)

The research established ten confirmed gaps in Section 4 (G-01 through G-10). For the options analysis, five are prioritized as the highest-impact gaps directly affecting Path A per-task execution correctness. The remaining five (G-04 scope enforcement -- implicitly closed via G-01 dependency per Section 4.3; G-08 isolation, G-09 PM agent, G-10 pipeline gate wiring -- all MEDIUM severity) are not core targets of any option but are noted in Section 4 for future work. For readability, this section uses short IDs (G1-G5) that map to the full Gap Analysis IDs in Section 4 as follows:

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

Replace `config.output_file(phase)` / `config.error_file(phase)` with task-scoped paths. This requires either a new `SprintConfig.task_output_file(phase, task_id)` method (add to `models.py`), or inline path construction: `config.results_dir / f"phase-{phase.number}-{task.task_id}-output.txt"`.

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

The new hook uses Extension Path B from File 04 (Section 5): `run_post_task_verification_hook()` reads the task's output file and evaluates it against the task's description/deliverables. Since acceptance criteria are natural-language (not pure-Python checkable), this hook would either:
- Use a lightweight `GateCriteria` with STANDARD tier (file exists + non-empty + min lines) as a structural quality check, OR
- Delegate to a brief Claude subprocess that reads the task output and answers "Did this output satisfy the task description?" (more expensive but semantically meaningful)

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
| | `/sc:task-unified` invocation in the enriched prompt triggers a full behavioral protocol (SKILL.md) that expects specific input formats -- prompt-skill interaction mismatches may cause unexpected worker behavior. Recommend validating prompt structure (Sprint Context + Scope Boundary) independently before adding `/sc:task-unified` invocation. |

---

### 6.3 Option C: Comprehensive -- Option B + Acceptance Criteria Gate + PM Agent + Checkpoint/Resume

**Closes:** G1-G5, plus: acceptance criteria verification using TaskEntry metadata, PM agent integration, per-task checkpoint with task-level resume

#### Description

Everything in Option B, plus: extend `TaskEntry` with structured acceptance criteria, implement a semantic acceptance gate using task metadata, connect PM agent systems for cross-session error learning, and implement per-task checkpoint files enabling task-level crash recovery.

#### How It Works

**Component 1: Extend TaskEntry with acceptance criteria**

The `TaskEntry` dataclass (`models.py:26`) currently has: `task_id`, `title`, `description`, `dependencies`, `command`, `classifier`. File 04 (Section 6, gap #4) confirmed there is no `acceptance_criteria` field.

Option C adds `acceptance_criteria: list[str]` and `tier: str` fields. The `parse_tasklist()` function (`config.py:306`) already extracts fields from the task block using regex. Adding parsers for `**Acceptance Criteria:**` and `| Tier | value |` fields extends the existing pattern.

**Component 2: Semantic acceptance gate**

The third hook from Option B (`run_post_task_verification_hook()`) is enhanced with an LLM-based acceptance check:

1. Read the task's output file (now at a unique per-task path from Option A)
2. Read `task.acceptance_criteria` (now populated from Option C's TaskEntry extension)
3. Construct a verification prompt: "Given these acceptance criteria: [...], and this task output: [...], does the output satisfy all criteria? Answer YES/NO with reasons."
4. Spawn a brief Claude subprocess (low `--max-turns`, e.g., 3) to evaluate
5. Parse the verification result and set `GateOutcome.PASS` or `GateOutcome.FAIL`

Budget impact: Each verification subprocess consumes turns from `TurnLedger`. The hook checks `ledger.can_launch()` before spawning and debits `verification_cost`. Under budget pressure, the gate degrades to structural-only checks (Option B behavior).

**Component 3: PM agent cross-session error learning**

Connect `ReflexionPattern` (`pm_agent/reflexion.py`) as a cross-session error memory for sprint task failures:

1. On task FAIL: call `reflexion_pattern.record_error()` with a dict built from `TaskResult` fields
2. Before each task: call `reflexion_pattern.get_solution()` with the task description to check if a similar task previously failed and was resolved
3. If a solution exists, append it to the task prompt as a "Known Issue" section

File 06 confirmed that `ConfidenceChecker` and `SelfCheckProtocol` are less useful for sprint integration because they require pre-populated evidence dicts rather than doing actual checks. `ReflexionPattern` is the exception -- it has a functional file-based search (`get_solution()`) and persistent JSONL storage.

**Component 4: Per-task checkpoint and resume**

Add per-task checkpoint files written after each task completes:

1. After each task in `execute_phase_tasks()`, write a checkpoint file: `results/.checkpoints/phase-{N}-task-{task_id}.json` containing serialized `TaskResult` fields
2. On resume (new `--resume-from <task_id>` CLI flag on `commands.py:73`), read checkpoint files to determine which tasks in a phase already completed, and skip them
3. Restore `TurnLedger` state from checkpoints (sum of `turns_consumed` across completed tasks)

The dead code `build_resume_output()` (`models.py:633`) already generates `--resume <task_id>` commands but references a CLI flag that does not exist. Option C implements the flag and the checkpoint reader.

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

Option B is recommended because it closes all five prioritized gaps (G1-G5, mapping to 6 of the 10 canonical gaps in Section 4 -- G-04 scope enforcement is implicitly closed via G-01 dependency per Section 4.3) at an appropriate effort/risk balance, follows every existing architectural pattern in the codebase, and positions the system for incremental enhancement toward Option C without premature commitment. The remaining MEDIUM-severity canonical gaps (G-08 isolation, G-09 PM agent integration, G-10 pipeline gate wiring) are not addressed by Option B and remain as future work items.

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

5. **Gate rollout modes provide a safe deployment path** -- The existing `gate_rollout_mode` system (File 04, Section 1.3; File 05, Section 5.2) allows the new gate to start in `shadow` mode (evaluate but do not fail tasks), collect metrics via `ShadowGateMetrics`, and promote to `soft` then `full` once confidence is established.

**Dependency caveat:** This recommendation assumes that project-level CLAUDE.md loads in worker subprocesses operating under `CLAUDE_WORK_DIR` isolation (Q-03 in Section 9 is unresolved). If empirical testing reveals that CLAUDE.md does not load in the isolation directory, Option B should include explicit governance injection in the enriched prompt to compensate for the missing framework rules. The prompt enrichment in Phase 1 partially mitigates this risk by embedding Sprint Context and Execution Rules directly in the prompt, but the broader SuperClaude framework rules (UV-only, parallel-first, confidence checks) would be absent.

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

## Section 8: Implementation Plan

> **Advisory (from synthesis QA):** The implementation plan below includes some scope from Option C (Phase 4: acceptance criteria field, Phase 5: checkpoint/resume) while the recommendation in Section 7 is Option B. Phases 1-3 and 5 (logging only) align with Option B. Phases 4 and 5 (steps 4.1-4.3, 5.5-5.8) extend into Option C territory. If implementing Option B only, scope Phases 4 and 5 accordingly.

### Phase 1 -- Prompt Enrichment

**Goal:** Replace the 3-line prompt in `_run_task_subprocess()` with a rich prompt modeled on Path B's `build_prompt()`, including `/sc:task-unified` invocation, sprint context, scope boundary, and result file contract.

**Current state:** `_run_task_subprocess()` at `src/superclaude/cli/sprint/executor.py:1053` sends only task ID, title, phase file path, and description (Research 01, Section 4b). Path B's `build_prompt()` at `src/superclaude/cli/sprint/process.py:123` sends a ~40-line prompt with full behavioral governance (Research 01, Section 5b).

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 1.1 | Create `build_task_prompt()` function | `src/superclaude/cli/sprint/process.py` (new function, after `build_prompt()` at line 123) | Model on `build_prompt()` (process.py:123) but scoped to a single task. Accept `task: TaskEntry`, `phase: Phase`, `config: SprintConfig`, `prior_results: list[TaskResult]`. Return a `str` prompt. |
| 1.2 | Include `/sc:task-unified` invocation | `src/superclaude/cli/sprint/process.py` (inside `build_task_prompt()`) | Emit `"/sc:task-unified Execute task {task.task_id} in @{phase.file} --compliance strict --strategy systematic"`. This matches Path B's command format (process.py:123, Research 01 Section 5b) and triggers loading of `sc-task-unified-protocol/SKILL.md` (Research 03, Section 6). |
| 1.3 | Include Sprint Context block | `src/superclaude/cli/sprint/process.py` (inside `build_task_prompt()`) | Emit sprint name (`config.sprint_name`), phase number (`phase.number`), artifact root (`config.results_dir`), prior-phase dirs -- identical fields to Path B's Sprint Context (process.py:123, Research 01 Section 5b). |
| 1.4 | Include Execution Rules block | `src/superclaude/cli/sprint/process.py` (inside `build_task_prompt()`) | Emit tier-based behavior rules: STRICT stops on fail, others log and continue. Mirror Path B's Execution Rules section (process.py:123, Research 01 Section 5b). Include task classifier from `task.classifier` (parsed by `parse_tasklist()` at config.py:306, Research 01 Section 3). |
| 1.5 | Include Scope Boundary | `src/superclaude/cli/sprint/process.py` (inside `build_task_prompt()`) | Emit `"After completing task {task.task_id}, STOP immediately. Do NOT proceed to other tasks."`. Path B says "After completing all tasks, STOP immediately" (Research 01 Section 5b) -- this is the single-task equivalent. |
| 1.6 | Include Result File contract | `src/superclaude/cli/sprint/process.py` (inside `build_task_prompt()`) | Emit exact output path (Phase 2 will define per-task paths) and required content format including `EXIT_RECOMMENDATION: CONTINUE/HALT`. Mirrors Path B's Result File instructions (Research 01 Section 5b). |
| 1.7 | Replace 3-line prompt in `_run_task_subprocess()` | `src/superclaude/cli/sprint/executor.py:1053-1068` | Replace the inline `prompt = (f"Execute task...")` block with a call to `build_task_prompt(task, phase, config, prior_results)`. Import `build_task_prompt` from `process.py`. |
| 1.8 | Fix the `__new__` bypass pattern | `src/superclaude/cli/sprint/executor.py:1070-1085` | Replace the `ClaudeProcess.__new__()` + `_Base.__init__()` bypass (Research 01 Section 4c) with proper sprint `ClaudeProcess` construction. Either: (a) add a `task_prompt` parameter to the sprint `ClaudeProcess.__init__()` that overrides `build_prompt()`, or (b) create a `TaskClaudeProcess` subclass that calls `build_task_prompt()` instead of `build_prompt()`. Option (a) is less invasive. |

---

### Phase 2 -- Output Isolation

**Goal:** Give each task its own output file instead of all tasks in a phase sharing `config.output_file(phase)`, which causes file collision (Research 01, Section 4d).

**Current state:** `_run_task_subprocess()` at executor.py:1070-1085 passes `config.output_file(phase)` and `config.error_file(phase)` to `ClaudeProcess.__init__()`. Since multiple tasks per phase invoke this with the same phase, each task overwrites the previous (Research 01, Section 4d).

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 2.1 | Add `task_output_file()` method to SprintConfig | `src/superclaude/cli/sprint/models.py` (after `output_file()` method, approx line 420) | `def task_output_file(self, phase: Phase, task_id: str) -> Path:` returns `self.results_dir / f"phase-{phase.number}-{task_id}-output.txt"`. Follows the existing `output_file()` pattern (models.py, used at executor.py:1076, Research 01 Section 4c). |
| 2.2 | Add `task_error_file()` method to SprintConfig | `src/superclaude/cli/sprint/models.py` (adjacent to `task_output_file()`) | `def task_error_file(self, phase: Phase, task_id: str) -> Path:` returns `self.results_dir / f"phase-{phase.number}-{task_id}-errors.txt"`. Mirrors `error_file()` pattern. |
| 2.3 | Add `task_result_file()` method to SprintConfig | `src/superclaude/cli/sprint/models.py` (adjacent) | `def task_result_file(self, phase: Phase, task_id: str) -> Path:` returns `self.results_dir / f"phase-{phase.number}-{task_id}-result.md"`. The result file contract from Phase 1 Step 1.6 will reference this path. |
| 2.4 | Update `_run_task_subprocess()` to use per-task paths | `src/superclaude/cli/sprint/executor.py:1076-1078` | Replace `config.output_file(phase)` with `config.task_output_file(phase, task.task_id)` and `config.error_file(phase)` with `config.task_error_file(phase, task.task_id)`. |
| 2.5 | Store output path on TaskResult | `src/superclaude/cli/sprint/models.py` (TaskResult dataclass, approx line 95) | Ensure `TaskResult.output_path` is populated with the per-task output file path. Currently `output_path` exists on the dataclass (Research 04 Section 2.1) but may not be set correctly in `_run_task_subprocess()`. Verify and fix at executor.py where TaskResult is constructed (approx line 990-1010). |
| 2.6 | Update anti-instinct hook file reference | `src/superclaude/cli/sprint/executor.py:828` | The anti-instinct gate reads `task_result.output_path` (Research 04 Section 2.3). Since Step 2.5 ensures this is correctly set to the per-task path, verify that the hook reads the right file. No code change expected if 2.5 is correct, but verify. |

---

### Phase 3 -- Context Injection

**Goal:** Wire `build_task_context()` into the per-task prompt so each task has visibility into what prior tasks accomplished.

**Current state:** `build_task_context()` at `src/superclaude/cli/sprint/process.py:245` is confirmed dead code with zero callers (Research 01, Section 6). It was purpose-built for cross-task context injection. Related dead code: `get_git_diff_context()` (line 310) and `compress_context_summary()` (line 335).

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 3.1 | Verify `build_task_context()` API compatibility | `src/superclaude/cli/sprint/process.py:245-308` | Read the function signature and return type. It accepts prior task results and returns a context string. Confirm it can accept `list[TaskResult]` (from `execute_phase_tasks()` accumulation at executor.py:949, Research 08 Section 4). |
| 3.2 | Call `build_task_context()` from `build_task_prompt()` | `src/superclaude/cli/sprint/process.py` (inside `build_task_prompt()` created in Phase 1) | If `prior_results` is non-empty, call `build_task_context(prior_results)` and prepend the returned context string to the prompt. This activates the existing dead code with zero new logic. |
| 3.3 | Pass accumulated results through the call chain | `src/superclaude/cli/sprint/executor.py:912-1050` | In `execute_phase_tasks()`, the per-task loop accumulates results at line 949 (`results.append(task_result)`). Pass the current `results` list to `_run_task_subprocess()` as a new `prior_results` parameter. Update `_run_task_subprocess()` signature at line 1053 to accept `prior_results: list[TaskResult] = []`. |
| 3.4 | Update `_run_task_subprocess()` to pass results to prompt builder | `src/superclaude/cli/sprint/executor.py:1053` | Pass `prior_results` to `build_task_prompt()` (created in Phase 1, Step 1.7). |
| 3.5 | Validate `get_git_diff_context()` and `compress_context_summary()` | `src/superclaude/cli/sprint/process.py:310, 335` | These are only called by `build_task_context()` (Research 01 Section 6). Once `build_task_context()` is activated, verify they still function correctly. `get_git_diff_context()` runs `git diff` -- confirm it works in the isolation directory context (Research 03 Section 3: only `CLAUDE_WORK_DIR` is set, `GIT_CEILING_DIRECTORIES` is NOT set). |

---

### Phase 4 -- Semantic Verification Gate

> **Scope note:** Steps 4.1-4.3 (extending `TaskEntry` with `acceptance_criteria` and `deliverable_paths`, extending `parse_tasklist()`) are Option C scope. For Option B only, begin at Step 4.4 and use task description/title for the structural gate rather than parsed acceptance criteria.

**Goal:** Add a post-task hook that checks whether the task produced its required deliverables and met acceptance criteria keywords, filling the gap identified in Research 04 (neither existing gate verifies task-specific acceptance criteria).

**Current state:** Two post-task hooks exist (Research 04). The wiring gate (executor.py:450) checks codebase structural integrity but is completely task-agnostic. The anti-instinct gate (executor.py:787) reads the task output file but checks roadmap-specific frontmatter fields (`undischarged_obligations`, etc.), making it a no-op for sprint tasks (Research 04, Section 4). Extension Path B (new third hook) was identified as the cleanest approach (Research 04, Section 5).

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 4.1 | Extend `TaskEntry` with `acceptance_criteria` field | `src/superclaude/cli/sprint/models.py:26` | Add `acceptance_criteria: list[str] = field(default_factory=list)` to the `TaskEntry` dataclass. Currently the dataclass has `task_id`, `title`, `description`, `dependencies`, `command`, `classifier` (Research 01 Section 3). The new field will hold parsed acceptance criteria strings. |
| 4.2 | Extend `parse_tasklist()` to extract acceptance criteria | `src/superclaude/cli/sprint/config.py:306-364` | After existing field extraction (description from `**Deliverables:**`, dependencies from `**Dependencies:**`, classifier from table row -- Research 01 Section 3), add extraction of `**Acceptance Criteria:**` section content. Parse bullet points as individual criteria strings. |
| 4.3 | Extend `TaskEntry` with `deliverable_paths` field | `src/superclaude/cli/sprint/models.py:26` | Add `deliverable_paths: list[str] = field(default_factory=list)` to TaskEntry. Parsed from `**Deliverables:**` section file path references (e.g., lines matching `src/...` or `tests/...`). |
| 4.4 | Create `run_post_task_semantic_hook()` | `src/superclaude/cli/sprint/executor.py` (after `run_post_task_anti_instinct_hook()` at line 909) | New function with same signature pattern as existing hooks (Research 04 Section 1.1): `run_post_task_semantic_hook(task, config, task_result, ledger) -> TaskResult`. |
| 4.5 | Implement deliverable path existence check | Inside `run_post_task_semantic_hook()` | For each path in `task.deliverable_paths`, check `(config.release_dir / path).exists()`. This is a pure-Python check compatible with the `gate_passed()` model (Research 04 Section 3). Report missing deliverables as `failure_reason`. |
| 4.6 | Implement acceptance criteria keyword check | Inside `run_post_task_semantic_hook()` | Read `task_result.output_path` content. For each string in `task.acceptance_criteria`, check if key terms appear in the output (simple substring/regex match). This follows the `SemanticCheck` pattern from `GateCriteria` (Research 04 Section 3, Research 05 Section 2.1). |
| 4.7 | Build `GateCriteria` dynamically per task | `src/superclaude/cli/sprint/executor.py` (inside `run_post_task_semantic_hook()`) | Use `GateCriteria` from `src/superclaude/cli/pipeline/models.py:68` with `enforcement_tier="STANDARD"` and dynamic `semantic_checks` built from the task's acceptance criteria. Call `gate_passed()` from `src/superclaude/cli/pipeline/gates.py:20`. This reuses the existing gate engine (Research 04 Section 5, Extension Path C). |
| 4.8 | Wire the new hook into `execute_phase_tasks()` | `src/superclaude/cli/sprint/executor.py:1028-1040` | Add `task_result = run_post_task_semantic_hook(task, config, task_result, ledger)` after the existing wiring hook (line 1028) and before the anti-instinct hook (line 1034). Follow the same mode resolution pattern (`_resolve_wiring_mode()` defined at line 421, called at line 475, or add a new `_resolve_semantic_mode()`). |
| 4.9 | Honor gate rollout modes | Inside `run_post_task_semantic_hook()` | Support `off`/`shadow`/`soft`/`full` modes matching the existing pattern (Research 04 Sections 1.3, 2.4). In `shadow` mode, log findings to `DeferredRemediationLog` without affecting task status. In `full` mode, set `TaskStatus.FAIL` on blocking findings. |

---

### Phase 5 -- Per-Task Progress Logging

> **Scope note:** Steps 5.1-5.4 align with Option B. Steps 5.5-5.8 (checkpoint files, resume flag, `build_resume_output()` activation) are Option C scope.

**Goal:** Write task results to `execution-log.jsonl` as they complete, enabling task-level resume and crash recovery.

**Current state:** The JSONL log records only phase-level events: `sprint_start`, `phase_start`, `phase_complete`, `sprint_complete` (Research 08, Section 1). Individual `TaskResult` objects are accumulated in memory only (Research 08, Section 4). `build_resume_output()` at models.py:633 generates `--resume <task_id>` commands but is dead code (Research 08, Section 4). The `--resume` flag does not exist on the CLI (Research 08, Section 3).

| Step | Action | Files | Details |
|------|--------|-------|---------|
| 5.1 | Add `write_task_start()` to SprintLogger | `src/superclaude/cli/sprint/logging_.py` (after `write_phase_start()` at line 58) | New method: `write_task_start(self, phase: int, task_id: str, task_title: str)`. Emit `{"event": "task_start", "phase": N, "task_id": "T01.01", "task_title": "...", "timestamp": "..."}`. Follow the existing `_jsonl()` append pattern (logging_.py:173, Research 08 Section 1). |
| 5.2 | Add `write_task_complete()` to SprintLogger | `src/superclaude/cli/sprint/logging_.py` (after `write_task_start()`) | New method: `write_task_complete(self, phase: int, task_id: str, status: TaskStatus, duration_seconds: float, gate_outcome: str, output_path: str)`. Emit `{"event": "task_complete", ...}`. Include all `TaskResult` fields needed for resume decisions. |
| 5.3 | Pass SprintLogger to `execute_phase_tasks()` | `src/superclaude/cli/sprint/executor.py:912` | Add `logger: SprintLogger | None = None` parameter to `execute_phase_tasks()`. The logger is created at executor.py:1140 (approx) and is available in `execute_sprint()`. Pass it through. |
| 5.4 | Call logger in per-task loop | `src/superclaude/cli/sprint/executor.py:950-1000` (inside per-task loop) | Before subprocess launch: `logger.write_task_start(phase.number, task.task_id, task.title)`. After result determination: `logger.write_task_complete(phase.number, task.task_id, task_result.status, ...)`. Place these adjacent to existing TUI update calls (lines 979-984, Research 08 Section 4). |
| 5.5 | Write per-task result file to disk | `src/superclaude/cli/sprint/executor.py` (in per-task loop, after task completion) | Write a minimal result file to `config.task_result_file(phase, task.task_id)` (from Phase 2 Step 2.3) containing task status, duration, and gate outcome. This provides a filesystem checkpoint that survives crashes (Research 08 Section 5 identifies this as the critical missing piece). |
| 5.6 | Add task-level skip logic for resume | `src/superclaude/cli/sprint/executor.py:912-950` (top of per-task loop) | Before launching a task subprocess, check if `config.task_result_file(phase, task.task_id).exists()`. If it does and contains `status: PASS`, skip the task. This enables task-level resume within a phase that was interrupted. Log skipped tasks to both JSONL and TUI. |
| 5.7 | Add `--resume-tasks` flag to CLI | `src/superclaude/cli/sprint/commands.py:73-86` | Add `--resume-tasks` boolean flag (default False). When True, enable the task-level skip logic from Step 5.6. When False (default), preserve current behavior of re-executing entire phases. This is safer than always resuming because some tasks may have partial output. |
| 5.8 | Activate `build_resume_output()` | `src/superclaude/cli/sprint/models.py:633` | Currently dead code (Research 08 Section 4). Wire it into `SprintResult` construction so the resume command includes the last completed task ID when `--resume-tasks` is available. |

---

### Integration Checklist

This checklist must be verified after all phases are implemented.

**Prompt Enrichment (Phase 1)**
- [ ] `build_task_prompt()` exists in `process.py` and produces a prompt containing `/sc:task-unified`, Sprint Context, Execution Rules, Scope Boundary, and Result File contract
- [ ] `_run_task_subprocess()` at executor.py:1053 calls `build_task_prompt()` instead of inline 3-line prompt
- [ ] The `__new__` bypass pattern at executor.py:1070-1085 is replaced with proper `ClaudeProcess` construction
- [ ] Sprint `ClaudeProcess.__init__()` at process.py:97 accepts an optional `task_prompt` parameter or `TaskClaudeProcess` subclass exists

**Output Isolation (Phase 2)**
- [ ] `SprintConfig.task_output_file()`, `task_error_file()`, `task_result_file()` methods exist in models.py
- [ ] `_run_task_subprocess()` uses per-task output paths, not phase-level paths
- [ ] `TaskResult.output_path` is correctly set to the per-task output file
- [ ] No two tasks in the same phase write to the same output file

**Context Injection (Phase 3)**
- [ ] `build_task_context()` at process.py:245 is called from `build_task_prompt()`
- [ ] `execute_phase_tasks()` passes accumulated `results` list to `_run_task_subprocess()`
- [ ] `_run_task_subprocess()` passes `prior_results` to `build_task_prompt()`
- [ ] `get_git_diff_context()` and `compress_context_summary()` are validated in the isolation directory context

**Semantic Verification Gate (Phase 4)**
- [ ] `TaskEntry` dataclass has `acceptance_criteria` and `deliverable_paths` fields
- [ ] `parse_tasklist()` extracts acceptance criteria and deliverable paths from phase files
- [ ] `run_post_task_semantic_hook()` exists and follows the existing hook signature pattern
- [ ] The hook checks deliverable path existence and acceptance criteria keyword presence
- [ ] The hook supports `off`/`shadow`/`soft`/`full` rollout modes
- [ ] The hook is called from `execute_phase_tasks()` between the wiring hook and anti-instinct hook
- [ ] `GateCriteria` is built dynamically per task and evaluated via `gate_passed()`

**Per-Task Progress Logging (Phase 5)**
- [ ] `SprintLogger` has `write_task_start()` and `write_task_complete()` methods
- [ ] `execution-log.jsonl` contains `task_start` and `task_complete` events when per-task execution is used
- [ ] Per-task result files are written to `config.task_result_file(phase, task_id)` after each task completes
- [ ] `--resume-tasks` CLI flag exists and enables task-level skip logic
- [ ] Task-level skip logic checks for existing result files and skips PASS tasks
- [ ] `build_resume_output()` is activated and includes last completed task ID
- [ ] Crash mid-phase followed by `--resume-tasks` re-runs only uncompleted tasks

**Cross-Cutting Concerns**
- [ ] No circular imports introduced (sprint imports from pipeline are already lazy -- executor.py:819, Research 05 Section 7.2)
- [ ] All new code follows the existing `NFR-007` boundary: pipeline modules do NOT import from sprint (Research 05 Section 1.2)
- [ ] `make test` passes with no new test failures
- [ ] `make lint && make format` passes
- [ ] New functions have type annotations matching existing codebase conventions
- [ ] Dead code activated in Phase 3 (`build_task_context`, `get_git_diff_context`, `compress_context_summary`) has tests covering the activated paths

---

## Section 9: Open Questions

Questions compiled from the Gaps and Questions sections of all eight research files (01-08) and the consolidated gaps log. Ordered by impact (HIGH first, then MEDIUM, then LOW). Questions already resolved within the research itself are excluded.

| # | Question | Impact | Source | Suggested Resolution |
|---|----------|--------|--------|---------------------|
| Q-01 | Should Path A use `build_prompt()` (or a task-scoped variant) to generate richer prompts per task, closing the prompt fidelity gap between Path A and Path B? | HIGH | File 01 (Design Question 1) | Design a `build_task_prompt(task, phase, config, prior_results)` function that combines task metadata with Sprint Context, Execution Rules, and scope boundaries. Implement as part of the Path A enrichment effort. |
| Q-02 | Should `build_task_context()` be wired into `_run_task_subprocess()` to give each task visibility into prior task results? | HIGH | File 01 (Design Question 2) | Wire the existing dead-code function into `execute_phase_tasks()` by passing accumulated `task_results` to `_run_task_subprocess()`. The function already exists and is well-designed. |
| Q-03 | Does Claude Code resolve CLAUDE.md relative to `CLAUDE_WORK_DIR` (the isolation directory) or does it traverse upward to the git root? | HIGH | File 03 (Gap 2), Gaps Log S4/S5 | Deferred to Phase 4 web research (web-01). Empirical test needed: set `CLAUDE_WORK_DIR` to a subdirectory and check whether project-level CLAUDE.md loads. This determines whether workers in isolation directories inherit project governance. |
| Q-04 | Are MCP servers configured in user-level settings loaded in `--print` mode? If so, workers have access to web search, sequential thinking, codebase retrieval, etc. | HIGH | File 03 (Gap 3) | Deferred to Phase 4 web research (web-01). Empirical test or documentation review needed. |
| Q-05 | Was the `setup_isolation()` / `IsolationLayers` dead code (3 of 4 isolation layers never applied) intentional or an incomplete implementation? | HIGH | File 03 (Gap 1) | Code review of git history for `setup_isolation()`. If intentional, document rationale. If incomplete, wire remaining layers (`CLAUDE_SETTINGS_DIR`, `CLAUDE_PLUGIN_DIR`, `GIT_CEILING_DIRECTORIES`). |
| Q-06 | Should per-task output files use task-specific paths (e.g., `config.task_output_file(phase, task_id)`) to avoid the output file collision in Path A? | HIGH | File 01 (Design Question 3), Gaps Log S8 | Extend `SprintConfig` with a `task_output_file(phase, task_id)` method. Minimal change with high impact on post-mortem analysis and crash recovery. |
| Q-07 | Is the `__new__` bypass pattern in `_run_task_subprocess()` intentional or temporary tech debt? Should it construct a proper sprint `ClaudeProcess` with lifecycle hooks? | MEDIUM | File 01 (Design Question 4) | Refactor to construct a proper sprint `ClaudeProcess` via `__init__()` with a task-scoped `build_prompt()` override. This eliminates the bypass pattern and enables lifecycle hooks in Path A. |
| Q-08 | Why was the hybrid integration approach (Option C: sprint uses `execute_pipeline()` for per-task execution within `execute_phase_tasks()`) not pursued in v3.1? Was this a deliberate architectural decision or time-constrained? | MEDIUM | File 05 (Gap 1) | Review v3.1 sprint planning artifacts or consult the architect. Option C remains the most natural integration path for future work. |
| Q-09 | Is `decompose_deliverables()` intended for sprint task execution, or is it exclusively a roadmap feature? | MEDIUM | File 05 (Gap 2) | Clarify in architecture documentation. Sprint tasks come from tasklist files (already decomposed); behavioral decomposition may be redundant for sprint. |
| Q-10 | The codebase has three separate error-learning systems (`ReflexionPattern` in pm_agent, `SelfCorrectionEngine` in execution, `DiagnosticCollector`/`FailureClassifier` in sprint). Are all three needed? Should they be consolidated? | MEDIUM | File 06 (Gap 1) | Audit usage patterns. `ReflexionPattern` is pytest-only, `SelfCorrectionEngine` is dead code, sprint diagnostics are production. Consider deprecating execution/ and making ReflexionPattern available to sprint via adapter. |
| Q-11 | The entire `execution/` package (`intelligent_execute`, `ReflectionEngine`, `SelfCorrectionEngine`, `ParallelExecutor`) has zero external consumers. Should it be deprecated or removed? | MEDIUM | File 06 (Gap 2) | Run `/sc:cleanup-audit` focused on execution/. If no integration path is planned, mark as deprecated. No tests exist for these modules, increasing removal safety. |
| Q-12 | When were v3.1-T04, v3.1-T05, and v3.2-T02 actually implemented? They were SKIPPED in the 2026-03-21 QA reflections but exist in the current codebase. Was this a subsequent sprint pass or manual implementation? | MEDIUM | File 07 (Open Question 1) | Trace git history for `executor.py` lines 1201, 843, 1222, and 1432. Identify the commit(s) that added these features. |
| Q-13 | Are there any tests specifically covering the per-task delegation path in `execute_sprint()`? The outstanding tasklist (OT-08) suggests not, but new tests may have been added since. | MEDIUM | File 07 (Open Question 3) | Grep test files for `execute_phase_tasks` and `_parse_phase_tasks` references. The outstanding tasklist was generated 2026-03-22; verify whether tests were added after that date. |
| Q-14 | Does the current TUI surface per-task verification results (anti-instinct gate, wiring gate) when `execute_phase_tasks()` is used? The `execute_phase_tasks()` function accepts optional `tui` and `monitor` params. | MEDIUM | File 07 (Gap 4) | Code trace of `execute_phase_tasks()` TUI integration. Check if gate pass/fail results are displayed in the TUI dashboard during per-task execution. |
| Q-15 | `build_resume_output()` generates `--resume <task_id>` commands but is dead code, and the `--resume` CLI flag does not exist. Should task-level resume be implemented? | MEDIUM | File 08 (Gap 2) | Decide whether task-level resume is a v3.3 feature. If yes, wire `build_resume_output()` and add the `--resume` flag to the CLI. If no, remove the dead code. |
| Q-16 | Should task-level events (`task_start`, `task_complete`) be added to `execution-log.jsonl`? Currently only phase-level events are logged. | MEDIUM | File 08 (Gap 1) | Add `SprintLogger` calls within `execute_phase_tasks()` loop. Minimal code change (pass logger, add 2 write calls per task) with high impact on crash diagnostics. |
| Q-17 | The anti-instinct gate passes vacuously for sprint tasks (code outputs lack roadmap-specific frontmatter). Should a sprint-specific gate be created, or should the anti-instinct gate be parameterized? | MEDIUM | File 04 (Gap 1), Gaps Log S1 | Extension Path B (add a third post-task hook for acceptance criteria) is cleanest. See File 04 Section 5 for three extension paths. |
| Q-18 | `read_status_from_log()` and `tail_log()` are stubs that print placeholder messages. When will the `status` and `logs` CLI subcommands be implemented? | LOW | File 08 (Gap 6) | Low priority. These are user-facing convenience commands, not production-critical. Implement when task-level JSONL logging is added (Q-16). |
| Q-19 | `TaskEntry` has no `acceptance_criteria` field. Should the model be extended to support structured acceptance criteria for verification gates? | LOW | File 04 (Gap 4) | Extend `TaskEntry` dataclass if Q-17 leads to acceptance criteria verification. Parse from `**Acceptance Criteria:**` section in phase files. |
| Q-20 | Does the `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` env var in user settings enable multi-agent delegation features within worker subprocesses? | LOW | File 03 (Gap 6) | Empirical test or documentation review. This is a governance question -- if agent teams are active in workers, the execution model is more complex than documented. |
| Q-21 | File 06 asserts "no tests for execution/" without citing grep evidence. Is this accurate? | LOW | Gaps Log S7 | Run `grep -r "from superclaude.execution" tests/`. Low impact -- execution/ modules confirmed as dead code regardless of test existence. |
| Q-22 | The `_format_wiring_failure()` function returns a remediation prompt string that is never sent to a subprocess. Is this a stub for v3.3's `attempt_remediation()` integration? | LOW | File 04 (Gap 3) | Confirm via code comment or git history. The function's output is currently unused. Will become relevant when `attempt_remediation()` is wired in (v3.3). |
| Q-23 | File 05 claims "42+ symbols" in the pipeline `__init__.py` public API without explicit count. Is this accurate? | LOW | Gaps Log S9 | Run `grep -c "^[A-Z]" src/superclaude/cli/pipeline/__init__.py` or count exports. Plausible approximation, non-critical. |

**Summary**: 23 open questions compiled. 6 are HIGH impact (affecting production execution correctness or crash recovery), 11 are MEDIUM impact (affecting test coverage, code quality, or feature completeness), and 6 are LOW impact (affecting documentation or minor dead code).

---

## Section 10: Evidence Trail

### 10.1 Research Files

All research was conducted on 2026-04-03 via parallel investigation agents spawned from the research-notes.md plan. Phase 4 (web research) was started but not completed -- web-01 and web-02 are stubs with research questions only.

| File | Topic | Agent Type | Status |
|------|-------|-----------|--------|
| `research/research-notes.md` | Research plan, file inventory, phase design, agent assignments | Planning (Phase 1) | Complete |
| `research/01-sprint-executor-path-routing.md` | Path A vs Path B routing in `execute_sprint()`, prompt construction, `_run_task_subprocess()` bypass pattern, output file collision, `build_task_context()` dead code | Code Tracer | Complete |
| `research/02-tasklist-generation-format.md` | Tasklist generation algorithm, `### T<PP>.<TT>` format mandate, `_TASK_HEADING_RE` regex alignment, empirical verification across 6 release samples | Code Tracer + Doc Analyst | Complete |
| `research/03-worker-session-governance.md` | `claude --print -p` subprocess inheritance: CLAUDE.md, skills, settings, env vars, isolation layers (3 of 4 dead code) | Architecture Analyst | Complete |
| `research/04-post-task-verification-gates.md` | Wiring gate (AST-based codebase analysis), anti-instinct gate (roadmap-specific frontmatter validation, vacuous pass for sprint tasks), extension paths | Code Tracer | Complete |
| `research/05-pipeline-qa-systems.md` | Pipeline `execute_pipeline()` architecture, gate tiers, trailing gates, why sprint does not use it, integration options (A/B/C) | Integration Mapper | Complete |
| `research/06-pm-agent-execution-systems.md` | pm_agent/ (pytest fixtures only), execution/ (unused prototype), neither wired to sprint, three redundant error-learning systems | Integration Mapper | Complete |
| `research/07-design-intent-version-history.md` | v3.1/v3.2 gap analyses, planned vs implemented verification layers, outstanding tasklist (22 items, 10 test tasks deferred), cross-release architecture intent | Doc Analyst | Complete |
| `research/08-progress-tracking-resume.md` | JSONL logging (phase-level only), resume via `--start` (phase granularity), crash state loss, `build_resume_output()` dead code, `.roadmap-state.json` is unrelated to sprint | Code Tracer | Complete |
| `research/web-01-claude-print-subprocess.md` | Claude `--print -p` subprocess behavior, CLAUDE.md loading, skill resolution, settings inheritance | Web Researcher | **Not Completed** (stub only) |
| `research/web-02-worker-governance-patterns.md` | AI orchestration framework patterns for worker governance, task verification, prompt engineering for subprocess workers | Web Researcher | **Not Completed** (stub only) |

### 10.2 QA and Gaps Files

| File | Topic | Purpose |
|------|-------|---------|
| `gaps-and-questions.md` | Consolidated gaps from analyst and QA completeness reports | Merged from 4 QA reports: 3 procedural gaps (P1-P3), 9 substantive gaps (S1-S9), 3 cross-reference issues |

### 10.3 Synthesis Files

| File | Sections | Status |
|------|----------|--------|
| `synthesis/synth-01-problem-current-state.md` | Sections 1-2 (Problem Statement, Current State) | Complete |
| `synthesis/synth-02-target-gaps.md` | Sections 3-4 (Target State, Gap Analysis) | Complete |
| `synthesis/synth-03-external-findings.md` | Section 5 (External / Web Research Findings) | **N/A** -- Phase 4 web research was skipped. File was not created (Section 5 content is inline N/A). |
| `synthesis/synth-04-options-recommendation.md` | Sections 6-7 (Options, Recommendation) | Complete |
| `synthesis/synth-05-implementation-plan.md` | Section 8 (Implementation Plan) | Complete |
| `synthesis/synth-06-questions-evidence.md` | Sections 9-10 (Open Questions, Evidence Trail) | Complete |

### 10.4 Key Source Code Files Investigated

The research agents collectively examined the following source files (with line-level citations throughout the research documents):

| Module | Files | Primary Findings |
|--------|-------|-----------------|
| Sprint Executor | `src/superclaude/cli/sprint/executor.py` (~1850 lines) | Path A/B divergence at line 1201, per-task hooks, dead code (`build_task_context`, `aggregate_task_results`, `setup_isolation`) |
| Sprint Process | `src/superclaude/cli/sprint/process.py` (~300 lines) | `build_prompt()` (Path B only), `build_task_context()` dead code |
| Sprint Config | `src/superclaude/cli/sprint/config.py` (~410 lines) | `_TASK_HEADING_RE` regex, `parse_tasklist()` |
| Sprint Models | `src/superclaude/cli/sprint/models.py` (~650 lines) | `TaskEntry`, `TaskResult`, `TurnLedger`, `build_resume_output()` dead code |
| Sprint Logging | `src/superclaude/cli/sprint/logging_.py` (~200 lines) | Phase-only JSONL events, no per-task logging |
| Sprint Commands | `src/superclaude/cli/sprint/commands.py` (~300 lines) | `--start`/`--end` flags, no `--resume` flag |
| Pipeline Process | `src/superclaude/cli/pipeline/process.py` | Base `ClaudeProcess`, `build_command()`, `build_env()` |
| Pipeline Executor | `src/superclaude/cli/pipeline/executor.py` | `execute_pipeline()` -- not used by sprint |
| Pipeline Gates | `src/superclaude/cli/pipeline/gates.py` | `gate_passed()` tiered validation |
| Pipeline Trailing | `src/superclaude/cli/pipeline/trailing_gate.py` | `TrailingGateRunner`, `attempt_remediation()` -- not wired to sprint |
| Audit Wiring | `src/superclaude/cli/audit/wiring_gate.py` | Wiring analysis (G-001, G-002, G-003) |
| Roadmap Gates | `src/superclaude/cli/roadmap/gates.py` | `ANTI_INSTINCT_GATE` definition |
| PM Agent | `src/superclaude/pm_agent/*.py` (4 files) | Pytest fixtures only, not used by sprint |
| Execution | `src/superclaude/execution/*.py` (4 files) | Unused prototype, zero external consumers |
| Tasklist Protocol | `src/superclaude/skills/sc-tasklist-protocol/` | SKILL.md, templates, rules -- format mandate |

### 10.5 Design Documents Analyzed

| Document | Path | Key Findings |
|----------|------|-------------|
| v3.1 Gap Remediation Tasklist | `.dev/releases/complete/v3.1_Anti-instincts__/v3.1/gap-remediation-tasklist.md` | T04 (per-task delegation) was the critical architectural fix |
| v3.1 Merged Gap Analysis | `.dev/releases/complete/v3.1_Anti-instincts__/v3.1/roadmap-gap-analysis-merged.md` | Identified execute_sprint/execute_phase_tasks disconnect |
| v3.2 Merged Gap Analysis | `.dev/releases/complete/v3.2_fidelity-refactor___/v3.2/roadmap-gap-analysis-merged.md` | 18 gaps in sprint integration layer |
| v3.2 Outstanding Tasklist | `.dev/releases/complete/v3.2_fidelity-refactor___/outstanding-tasklist.md` | 22 consolidated tasks, 10 test tasks all deferred |
| Sprint CLI Release Guide | `docs/generated/sprint-cli-tools-release-guide.md` | Original per-phase subprocess model |
| Sprint TUI Reference | `docs/developer-guide/sprint-tui-reference.md` | No task-level verification in TUI |
| TurnLedger Cross-Release Summary | `.dev/releases/complete/v3.1_Anti-instincts__/turnledger-integration/cross-release-summary.md` | Intended 4-layer verification architecture |
| v3.1 QA Execution Reflection | `.dev/releases/complete/v3.1_Anti-instincts__/v3.1/execution-qa-reflection.md` | T04, T05 were SKIPPED during v3.1 (later implemented) |
| v3.2 QA Execution Reflection | `.dev/releases/complete/v3.2_fidelity-refactor___/v3.2/execution-qa-reflection.md` | T02 was PARTIAL during v3.2 (later implemented) |

### 10.6 Empirical Phase File Samples

Six actual generated phase files were sampled across releases to verify format consistency:

| Release | File | Format Match |
|---------|------|-------------|
| v2.24.5-SpecFidelity | `phase-1-tasklist.md` | `### T01.01 -- <Title>` -- matches `_TASK_HEADING_RE` |
| v2.25.5-PreFlightExecutor | `phase-1-tasklist.md` | `### T01.01 -- <Title>` -- matches |
| v2.26-roadmap-v5 | `phase-1-tasklist.md` | `### T01.01 -- <Title>` -- matches |
| v3.05-DeterministicFidelityGates | `phase-1-tasklist.md` | `### T01.01 -- <Title>` -- matches |
| v3.1-Anti-instincts | `phase-1-tasklist.md` | `### T01.01 -- <Title>` -- matches |
| unified-audit-gating-v2 | `phase-1-tasklist.md` | `### T01.01 -- <Title>` -- matches |

100% format consistency across all samples. Path A is the standard execution path for all protocol-generated phase files.

---

*Assembled from 5 synthesis files on 2026-04-03. All findings sourced from 8 codebase research files (research/01-08), consolidated gaps log, and 9 design documents across v3.1-v3.2 releases.*

---

## Addendum: Architect Corrections and Revised Analysis (Post-Review)

**Date:** 2026-04-03
**Source:** Feedback from system architect (Ryan Wiancko) during report review

This addendum corrects the report's framing based on the architect's clarifications. The raw technical findings (code paths, line numbers, dead code) remain accurate. What changes is the **interpretation** of Path A's minimal prompt and the **priority** of the identified gaps.

### A.1 Key Architect Corrections

#### Correction 1: Path A's Minimal Prompt Is Partly By Design

The report frames Path A's 3-line prompt as a gap. The architect clarifies this is **intentional** — the tasklist has already done the heavy lifting:

> "With Path A, the tasklist has already done all of the heavy lifting upfront and you can save time and tokens on the task execution by using a simpler execution protocol and having more of this live in the programmatic layer as part of the orchestration contract."

Each task in the phase file already contains concrete, task-specific instructions:
- `Tier: STANDARD` (explicit, not inferred)
- `Verification Method: Direct test execution` (explicit)
- `MCP Requirements: Preferred: Sequential, Context7` (explicit)
- Numbered `[PLANNING]`/`[EXECUTION]`/`[VERIFICATION]`/`[COMPLETION]` steps
- Specific validation commands (e.g., `uv run pytest tests/v3.3/ -v --co`)

Injecting Path B's generic tier-to-behavior rules alongside these specific instructions would create **ambiguity about which takes precedence**, potentially degrading execution quality rather than improving it.

#### Correction 2: The Intra-Task QA System Exists But Is Functionally Inert

The report states "no semantic QA exists." The accurate statement is: **an intra-task QA system exists, is architecturally wired, but is functionally inert due to three compounding input-side issues:**

1. **Zero turn counts** — `_run_task_subprocess()` returns `(exit_code, 0, output_bytes)` at `executor.py:1092`. The `0` means turn-based budget tracking never engages, and reimbursement on gate PASS (`turns_consumed * reimbursement_rate`) always credits 0.

2. **Unset output paths** — `TaskResult.output_path` defaults to `""`. The anti-instinct gate at `executor.py:823-829` checks `output_path`, finds it empty, and passes vacuously ("No output artifact to evaluate — gate passes vacuously").

3. **Default-off gate mode** — `config.gate_rollout_mode` defaults to `"off"`, which means `run_post_task_anti_instinct_hook()` returns immediately at `executor.py:814` without evaluating.

The economic model (budget math, reimbursement rates, monotonicity) has been validated by 50 tests in v3.7. The gates work mechanically; they just don't receive the inputs they need to do real work.

#### Correction 3: Path B's Execution Rules Would Be Harmful in Path A

The report recommends enriching Path A's prompt with Path B's content. The architect specifically warns against this:

> "The execution rules are generic tier-to-behavior mappings. The tasklist has already made those decisions concretely per task."

Example: Path B says "STANDARD tasks: run direct test execution per acceptance criteria." The tasklist says "run `uv run pytest tests/audit-trail/test_audit_writer.py -v`." The specific instruction is **more valuable** than the generic one.

### A.2 The Real Gap: Parsed Task Data Doesn't Reach the Worker

The architect's design assumes the worker has access to the full task specification. This is true — **if the worker reads the phase file**. But the programmatic layer already parsed that file and could feed the rich data directly.

Currently, `parse_tasklist()` (`config.py:306`) extracts from each task block:

| Field | What's Extracted | What's Lost |
|-------|-----------------|-------------|
| `task_id` | `"T01.02"` | — |
| `title` | `"Implement session-scoped audit_trail fixture"` | — |
| `description` | `**Deliverables:**` lines until empty line or `**` heading | Acceptance criteria, Steps, Verification commands, Artifact paths, Tier, MCP requirements |
| `dependencies` | `**Dependencies:**` task IDs | — |
| `command` | `**Command:**` (for python-mode) | — |
| `classifier` | `| Tier |` table value | — |

The worker prompt includes only `task_id`, `title`, `description`, and the phase file path. Whether the deliverables text alone is sufficient depends on the task:

**Sufficient cases** — deliverables describe what to create with enough detail:
```
tests/v3.3/conftest.py — session-scoped audit_trail fixture that opens JSONL
in results_dir, provides record() method, auto-flushes after each test
```

**Insufficient cases** — verification requires specific commands not in deliverables:
```
CLI availability confirmation: claude --print -p "hello" --max-turns 1 exits 0
```
(The verification command `uv run pytest tests/v3.3/ -v --co` is in the Validation section, not Deliverables.)

**The core question for the next release:** Can the parsed `TaskEntry` data be made rich enough — either by extracting more fields (acceptance criteria, verification commands) or by enriching the `description` field — so that the 3-line prompt carries sufficient task context without the worker needing to read the phase file? This would honor the architect's design (programmatic layer does heavy lifting, worker gets concrete instructions) while closing the information gap.

### A.3 Revised Gap Priorities

Based on architect feedback, the gap priorities shift:

| Gap | Original Priority | Revised Priority | Rationale |
|-----|-------------------|------------------|-----------|
| G-01: Prompt lacks `/sc:task-unified` | CRITICAL | **LOW** | By design — generic rules are less specific than per-task instructions |
| G-02: No semantic verification | CRITICAL | **HIGH** | The QA system exists but is inert due to input-side issues (turn counts, output paths, gate mode) |
| G-03: No acceptance criteria checking | HIGH | **HIGH** | Valid — but solution is enriching parsed TaskEntry data, not adding Path B rules |
| G-07: Output file collision | CRITICAL | **CRITICAL** | Unchanged — all tasks overwrite the same file, breaking gate evaluation |
| G-05: `build_task_context()` dead | HIGH | **MEDIUM** | Valid but lower priority than input-side fixes |
| G-06: Per-task progress memory-only | HIGH | **MEDIUM** | Valid — `build_resume_output()` is dead code with a non-existent `--resume` flag |

### A.4 Revised Recommendation

Instead of Option B (enriching the prompt with Path B content), the recommended approach becomes:

**Option B-Revised: Fix Input-Side Gaps + Enrich TaskEntry Parsing**

1. **Fix turn counting** — `_run_task_subprocess()` should return actual turns consumed, not hardcoded 0
2. **Fix output paths** — give each task its own output file (fixes G-07) and set `TaskResult.output_path` so gates can evaluate
3. **Activate gate mode** — change default from `"off"` to `"shadow"` (or make it configurable), so the anti-instinct gate actually runs
4. **Enrich `parse_tasklist()`** — extract acceptance criteria, verification commands, and artifact paths into `TaskEntry` fields
5. **Enrich the prompt** — include the extracted acceptance criteria and verification commands in the 3-line prompt (making it a ~10-line prompt), NOT the generic Path B execution rules
6. **Wire `build_task_context()`** — so each worker knows what prior tasks produced

This approach honors the architect's design intent (tasklist does the heavy lifting, worker gets concrete instructions) while fixing the three input-side issues that make the existing QA system inert.

### A.5 Architect's Planned Next Steps

The architect has confirmed:
- A task executor release is planned as the next priority
- All critiques from this research will go through adversarial debate
- Proposed solutions will be incorporated into the new version of the task pipeline
