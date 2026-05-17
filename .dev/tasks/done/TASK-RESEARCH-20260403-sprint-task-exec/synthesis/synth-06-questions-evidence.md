# Synthesis Report: Open Questions and Evidence Trail

**Date:** 2026-04-03
**Sections:** 9 (Open Questions), 10 (Evidence Trail)
**Research Question:** How individual tasks within a tasklist phase are fed to worker agents, executed, verified, and tracked in the IronClaude sprint pipeline -- and whether verification gaps found in preliminary analysis are real or exist in an unexamined layer.
**Source Files:** `research/01` through `research/08`, `research/web-01`, `research/web-02`, `gaps-and-questions.md`

---

## Section 9 — Open Questions

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

## Section 10 — Evidence Trail

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
| `synthesis/synth-03-external-findings.md` | Section 5 (External / Web Research Findings) | **N/A** -- Phase 4 web research was skipped |
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

*End of Sections 9 and 10.*
