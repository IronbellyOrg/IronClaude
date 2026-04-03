# Research Notes: Sprint Task Execution Flow Investigation

**Date:** 2026-04-03
**Scenario:** A (explicit request with detailed findings and specific files)
**Depth Tier:** Deep

---

## EXISTING_FILES

### Sprint Execution Core (`src/superclaude/cli/sprint/`)
| Path | Purpose | Key Exports |
|------|---------|-------------|
| `executor.py` (~1850 lines) | Main orchestration loop, per-task subprocess, hooks | `execute_sprint()`, `execute_phase_tasks()`, `_run_task_subprocess()`, `run_post_task_wiring_hook()`, `run_post_task_anti_instinct_hook()` |
| `process.py` (~300 lines) | Sprint-specific ClaudeProcess, prompt construction, context injection | `ClaudeProcess`, `build_prompt()`, `build_task_context()`, `SignalHandler` |
| `config.py` (~410 lines) | Phase discovery, tasklist parsing | `discover_phases()`, `parse_tasklist()`, `parse_tasklist_file()`, `_TASK_HEADING_RE` |
| `models.py` (~650 lines) | Data models | `TaskEntry`, `TaskResult`, `TaskStatus`, `TurnLedger`, `SprintConfig`, `SprintResult`, `Phase` |
| `logging_.py` (~200 lines) | Dual-format JSONL + Markdown execution logs | `SprintLogger` |
| `commands.py` (~300 lines) | Click CLI | `run`, `attach`, `status`, `logs` subcommands, `--start`/`--end` flags |
| `diagnostics.py` | Post-failure analysis | `DiagnosticCollector`, `FailureClassifier`, `ReportGenerator` |
| `classifiers.py` | Subprocess result classification | `empirical_gate_v1` (exit code 0 = pass) |
| `kpi.py` | Post-sprint KPI report | `build_kpi_report()`, `GateKPIReport` |
| `monitor.py` | Output monitor thread | `OutputMonitor` |
| `preflight.py` | Python-mode phase executor | `execute_preflight_phases()` |
| `tui.py` | Terminal UI | `SprintTUI` |
| `notify.py` | Desktop notifications | `notify_phase_complete()`, `notify_sprint_complete()` |
| `tmux.py` | Tmux session management | `launch_in_tmux()`, `update_tail_pane()` |

### Pipeline Base (`src/superclaude/cli/pipeline/`)
| Path | Purpose | Key Exports |
|------|---------|-------------|
| `process.py` | Base ClaudeProcess class | `ClaudeProcess`, `build_command()`, `start()`, `wait()` |
| `executor.py` | Generic pipeline executor with gates/retry | `execute_pipeline()` — NOT used by sprint |
| `gates.py` | Gate validation (pure Python) | `gate_passed()` |
| `deliverables.py` | Behavioral deliverable decomposition | `is_behavioral()`, `decompose_deliverables()` — NOT used by sprint |
| `trailing_gate.py` | Trailing gate runner | `TrailingGateRunner`, `DeferredRemediationLog` |
| `models.py` | Pipeline models | `Step`, `StepResult`, `GateCriteria`, `SemanticCheck` |

### Tasklist Generation
| Path | Purpose |
|------|---------|
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | Tasklist generation algorithm (10 stages) |
| `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` | Phase file template — confirms `### T<PP>.<TT>` format |
| `src/superclaude/skills/sc-tasklist-protocol/templates/index-template.md` | Index file template |
| `src/superclaude/skills/sc-tasklist-protocol/rules/file-emission-rules.md` | File structure rules |
| `src/superclaude/skills/sc-tasklist-protocol/rules/tier-classification.md` | Tier classification rules |
| `src/superclaude/cli/tasklist/executor.py` | CLI tasklist validate executor |
| `src/superclaude/cli/tasklist/prompts.py` | Validation prompts |
| `src/superclaude/cli/tasklist/gates.py` | Tasklist-specific gates |

### Verification/QA Systems (potentially related)
| Path | Purpose | Connected to Sprint? |
|------|---------|---------------------|
| `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` | Full verification protocol (TFEP, forensic, adversarial) | Only via Path B (fallback) |
| `src/superclaude/cli/audit/wiring_gate.py` | Wiring analysis | YES — via post-task hook |
| `src/superclaude/cli/roadmap/gates.py` | ANTI_INSTINCT_GATE definition | YES — via post-task hook |
| `src/superclaude/pm_agent/self_check.py` | SelfCheckProtocol | NO — not imported in sprint |
| `src/superclaude/pm_agent/confidence.py` | ConfidenceChecker | NO — not imported in sprint |
| `src/superclaude/execution/reflection.py` | Pre-execution confidence | NO — not imported in sprint |
| `src/superclaude/execution/self_correction.py` | Failure learning | NO — not imported in sprint |

### Design Docs & Specs
| Path | Purpose |
|------|---------|
| `.dev/releases/complete/v3.1_Anti-instincts__/` | v3.1 release with gap-remediation tasklist, roadmap gap analysis |
| `.dev/releases/complete/v3.2_fidelity-refactor___/` | v3.2 release with fidelity refactor, outstanding tasklist |
| `docs/developer-guide/sprint-tui-reference.md` | Sprint TUI documentation |
| `docs/generated/sprint-cli-tools-release-guide.md` | Sprint CLI release guide |

### Actual Generated Phase Files (to verify format)
| Path | Notes |
|------|-------|
| `.dev/releases/complete/v2.24.5-SpecFidelity/phase-1-tasklist.md` | Previously read — confirmed `### T01.01` format |
| `.dev/releases/complete/v3.1_Anti-instincts__/phase-1-tasklist.md` | v3.1 phase file |
| `.dev/releases/complete/v3.2_fidelity-refactor___/phase-1-tasklist.md` | v3.2 phase file |

### Configuration
| Path | Notes |
|------|-------|
| `.claude/settings.json` | No hooks, no pre/post prompt hooks found |

## PATTERNS_AND_CONVENTIONS

1. **Two execution paths diverge at `executor.py:1203`**: `_parse_phase_tasks()` returns task list → Path A (per-task); returns None → Path B (whole-phase). Phase file format determines routing.
2. **Phase template mandates `### T<PP>.<TT>` headings** (`phase-template.md:23`). All generated phase files use this format. This means Path A is the standard path, Path B is the fallback.
3. **Version tags in comments** (`v3.1-T04`, `v3.2-T02`) suggest incremental development of the per-task feature. The per-task path was added in v3.1 (T04), post-phase wiring was added in v3.2 (T02).
4. **`T02.06` in executor comment references cli_portify**, not a sprint task — this was a red herring.
5. **Pipeline executor exists with proper gates/retry** (`pipeline/executor.py`) but sprint does NOT use it. Sprint has its own orchestration loop.
6. **`build_task_context()` exists but has zero callers** — dead code in `process.py:245`.
7. **PM Agent systems (confidence, self_check, reflexion) are not connected to sprint** — no imports.
8. **Execution systems (reflection, self_correction, parallel) are not connected to sprint** — no imports.
9. **`decompose_deliverables()` is not connected to sprint** — no imports.

## SOLUTION_RESEARCH

N/A — pure investigation, not implementation.

## RECOMMENDED_OUTPUTS

| File | Purpose |
|------|---------|
| `research/01-sprint-executor-path-routing.md` | Deep trace of Path A vs Path B routing, prompt construction, what each path sends to the worker |
| `research/02-tasklist-generation-format.md` | Trace tasklist generation → phase file format → regex match → path selection |
| `research/03-worker-session-governance.md` | What a `claude -p` subprocess inherits: CLAUDE.md, skills, settings, hooks |
| `research/04-post-task-verification-gates.md` | Deep analysis of wiring hook, anti-instinct hook, what they actually check |
| `research/05-pipeline-qa-systems.md` | Pipeline executor, gates, deliverables — what exists but isn't wired to sprint |
| `research/06-pm-agent-execution-systems.md` | SelfCheck, Confidence, Reflection, SelfCorrection — what exists but isn't wired |
| `research/07-design-intent-version-history.md` | v3.1/v3.2 gap analyses, tasklists, specs — what the intended design was |
| `research/08-progress-tracking-resume.md` | Execution log content, resume mechanism, per-task persistence gaps |
| `synthesis/synth-01-problem-current-state.md` | Sections 1-2 of final report |
| `synthesis/synth-02-target-gaps.md` | Sections 3-4 |
| `synthesis/synth-03-external-findings.md` | Section 5 (Claude Code subprocess behavior, --print mode docs) |
| `synthesis/synth-04-options-recommendation.md` | Sections 6-7 |
| `synthesis/synth-05-implementation-plan.md` | Section 8 |
| `synthesis/synth-06-questions-evidence.md` | Sections 9-10 |
| `RESEARCH-REPORT-sprint-task-execution.md` | Final assembled report |

## SUGGESTED_PHASES

### Phase 2 — Deep Investigation (8 parallel research agents)

**Agent 1: Sprint Executor Path Routing** (Code Tracer)
- Files: `src/superclaude/cli/sprint/executor.py`, `src/superclaude/cli/sprint/process.py`, `src/superclaude/cli/sprint/config.py`
- Focus: Trace the exact code path from `execute_sprint()` → `_parse_phase_tasks()` → Path A/B divergence. Document what each path sends to the worker. Trace `_run_task_subprocess()` vs `ClaudeProcess.build_prompt()`.
- Output: `research/01-sprint-executor-path-routing.md`

**Agent 2: Tasklist Generation Format** (Code Tracer + Doc Analyst)
- Files: `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`, `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md`, `src/superclaude/skills/sc-tasklist-protocol/rules/file-emission-rules.md`, `.dev/releases/complete/v2.24.5-SpecFidelity/phase-1-tasklist.md`, `.dev/releases/complete/v3.1_Anti-instincts__/phase-1-tasklist.md`
- Focus: Confirm that the tasklist generator ALWAYS produces `### T<PP>.<TT>` formatted files. Check actual generated files. Trace format → regex match → path selection.
- Output: `research/02-tasklist-generation-format.md`

**Agent 3: Worker Session Governance** (Architecture Analyst)
- Files: `src/superclaude/cli/pipeline/process.py` (build_command), `.claude/settings.json`, `CLAUDE.md`
- Focus: What does a `claude --print -p` subprocess inherit? Does it load CLAUDE.md? Does it load skills from `.claude/skills/`? Does `--no-session-persistence` affect skill loading? Does `--tools default` restrict behavior? What governance exists even without explicit prompt instructions?
- Output: `research/03-worker-session-governance.md`

**Agent 4: Post-Task Verification Gates** (Code Tracer)
- Files: `src/superclaude/cli/sprint/executor.py` (hooks at lines 450-910), `src/superclaude/cli/audit/wiring_gate.py`, `src/superclaude/cli/roadmap/gates.py`, `src/superclaude/cli/pipeline/gates.py`
- Focus: Deep analysis of what the two post-task hooks actually check. What does the anti-instinct gate expect the worker to produce? What does the wiring gate analyze? Are these task-specific or generic? Could they be extended to check acceptance criteria?
- Output: `research/04-post-task-verification-gates.md`

**Agent 5: Pipeline QA Systems** (Integration Mapper)
- Files: `src/superclaude/cli/pipeline/executor.py`, `src/superclaude/cli/pipeline/gates.py`, `src/superclaude/cli/pipeline/deliverables.py`, `src/superclaude/cli/pipeline/trailing_gate.py`
- Focus: Map the full pipeline gate system. Why doesn't sprint use `execute_pipeline()`? What would it take to wire it in? Is `decompose_deliverables()` used by anything? Who calls `execute_pipeline()`?
- Output: `research/05-pipeline-qa-systems.md`

**Agent 6: PM Agent & Execution Systems** (Integration Mapper)
- Files: `src/superclaude/pm_agent/*.py`, `src/superclaude/execution/*.py`
- Focus: What do SelfCheck, Confidence, Reflection, SelfCorrection provide? Are they used by ANY part of the system? Are they designed to be pluggable into sprint?
- Output: `research/06-pm-agent-execution-systems.md`

**Agent 7: Design Intent & Version History** (Doc Analyst)
- Files: `.dev/releases/complete/v3.1_Anti-instincts__/v3.1/gap-remediation-tasklist.md`, `.dev/releases/complete/v3.1_Anti-instincts__/v3.1/roadmap-gap-analysis-merged.md`, `.dev/releases/complete/v3.2_fidelity-refactor___/v3.2/roadmap-gap-analysis-merged.md`, `.dev/releases/complete/v3.2_fidelity-refactor___/outstanding-tasklist.md`, `docs/developer-guide/sprint-tui-reference.md`, `docs/generated/sprint-cli-tools-release-guide.md`
- Focus: What was the INTENDED design for task-level verification? What do v3.1 and v3.2 specs say about per-task execution? Is there a planned but unimplemented verification layer? What's in the outstanding tasklist?
- Output: `research/07-design-intent-version-history.md`

**Agent 8: Progress Tracking & Resume** (Code Tracer)
- Files: `src/superclaude/cli/sprint/logging_.py`, `src/superclaude/cli/sprint/models.py` (SprintResult, resume_command), `src/superclaude/cli/sprint/commands.py` (--start flag)
- Focus: What gets logged to `execution-log.jsonl`? Is it phase-level or task-level? How does `--start` work for resume? What state is lost on crash? What about `.roadmap-state.json`?
- Output: `research/08-progress-tracking-resume.md`

### Phase 3 — Research Completeness Verification
- Spawn `rf-analyst` + `rf-qa` in parallel to verify all 8 research files
- Output: `qa/analyst-completeness-report.md`, `qa/qa-research-gate-report.md`

### Phase 4 — Web Research (2 agents)

**Web Agent 1: Claude Code --print subprocess behavior**
- Topic: What does `claude --print -p` actually do? What does the subprocess inherit? CLAUDE.md loading? Skill loading? Settings?
- Output: `research/web-01-claude-print-subprocess.md`

**Web Agent 2: Claude Code worker isolation and governance patterns**
- Topic: Best practices for governing headless AI worker subprocesses. Prompt engineering for subprocess workers. Task verification patterns.
- Output: `research/web-02-worker-governance-patterns.md`

### Phase 5 — Synthesis (6 agents) + QA Gate

Synth mapping per RECOMMENDED_OUTPUTS table above.

### Phase 6 — Assembly & Validation
- rf-assembler → rf-qa (report-validation) → rf-qa-qualitative (report-qualitative)
- Output: `RESEARCH-REPORT-sprint-task-execution.md`

## TEMPLATE_NOTES

Template 02 (Complex Task) — this investigation requires parallel subagent spawning, multiple phases, QA gates, and conditional flows.

## AMBIGUITIES_FOR_USER

None — intent is clear from the BUILD REQUEST. The investigation is explicitly scoped to the sprint task execution pipeline, the specific code paths, and the question of whether verification layers exist that were missed.

**Status:** Complete
