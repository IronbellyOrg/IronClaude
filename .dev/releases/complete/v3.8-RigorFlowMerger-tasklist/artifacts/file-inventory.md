# File Inventory: SC Tasklist + Adversarial vs RF Taskbuilder/Pipeline

**Generated**: 2026-04-02
**Scope**: Exhaustive inventory of all files participating in tasklist generation (SC) and task building/execution (RF), grouped by framework.

---

## A) SuperClaude Framework

All SC files live in the user's global Claude config (`/config/.claude/`) and the installed `superclaude` Python package. They are **not part of the llm-workflows repo**.

### A1. Commands (2 files)

| File | Location | Lines | Purpose |
|------|----------|-------|---------|
| `tasklist.md` | `/config/.claude/commands/sc/tasklist.md` | 114 | Thin command wrapper. Parses `<roadmap-path>`, `--spec`, `--output`. Derives `TASKLIST_ROOT` via 3-step priority algorithm. Validates inputs. Delegates all generation to `sc:tasklist-protocol` skill. |
| `adversarial.md` | `/config/.claude/commands/sc/adversarial.md` | 165 | Thin command wrapper. Parses `--compare` (Mode A), `--source`+`--generate`+`--agents` (Mode B), `--pipeline` (DAG mode). Delegates all logic to `sc:adversarial-protocol` skill. |

### A2. Protocol Skills

#### sc-tasklist-protocol/ (6 files)

| File | Location | Size | Purpose |
|------|----------|------|---------|
| `SKILL.md` | `/config/.claude/skills/sc-tasklist-protocol/SKILL.md` | 51KB | Full 10-stage deterministic generation algorithm. Stages 1-6: parse roadmap → determine phases → convert to tasks → enrich (effort/risk/tier/confidence) → assemble registries → emit files. Stages 7-10: validate against source roadmap → patch drift → spot-check → emit validation artifacts. Contains non-leakage/truthfulness rules, task format spec, tier classification algorithm, checkpoint cadence, deliverable registry, traceability matrix. |
| `tier-classification.md` | `rules/tier-classification.md` | ~2KB | Read-only reference: STRICT/STANDARD/LIGHT/EXEMPT tier keyword lists, compound phrase overrides, priority order (`STRICT > EXEMPT > LIGHT > STANDARD`), confidence boost rules. Extracted from SKILL.md Section 5.3. |
| `file-emission-rules.md` | `rules/file-emission-rules.md` | ~1KB | Read-only reference: N+1 file convention, `phase-N-tasklist.md` naming, phase heading format (`# Phase N -- <Name>`), content boundary (phase files = only tasks, no cross-phase metadata). Extracted from SKILL.md Section 3.3. |
| `index-template.md` | `templates/index-template.md` | ~2KB | Template for `tasklist-index.md`: metadata table, artifact paths table, phase files table, source snapshot, deterministic rules, roadmap item registry, deliverable registry, traceability matrix, execution log template, checkpoint template, feedback template, glossary. |
| `phase-template.md` | `templates/phase-template.md` | ~2KB | Template for `phase-N-tasklist.md`: phase heading/goal, task format `T<PP>.<TT>` with 13-field metadata block (roadmap IDs, effort, risk, tier, confidence, MCP requirements, etc.), deliverables, steps (PLANNING/EXECUTION/VERIFICATION/COMPLETION phases), acceptance criteria (4 bullets), validation (2 bullets), near-field completion criterion. |
| `__init__.py` | `__init__.py` | 0B | Python package marker. |

#### sc-adversarial-protocol/ (6 files)

| File | Location | Size | Purpose |
|------|----------|------|---------|
| `SKILL.md` | `/config/.claude/skills/sc-adversarial-protocol/SKILL.md` | 123KB | Full 5-step adversarial pipeline specification. Step 1: diff analysis (structural, content, contradiction, unique contribution, shared assumptions). Step 2: adversarial debate (3-level taxonomy L1/L2/L3, steelman requirement, 1-3 rounds by depth, convergence detection). Step 3: hybrid scoring (50% quantitative + 50% qualitative 30-criterion rubric, position bias mitigation, tiebreaker). Step 4: refactoring plan. Step 5: merge execution with provenance annotations. Plus: Pipeline Mode (DAG orchestration), error handling matrix, interactive mode, return contract, configurable parameters. |
| `agent-specs.md` | `refs/agent-specs.md` | — | Agent specification format: `model[:persona[:"instruction"]]`. Supported models, persona mapping, instruction embedding. |
| `artifact-templates.md` | `refs/artifact-templates.md` | — | Templates for all 6 output artifacts: diff-analysis.md (Section 1), debate-transcript.md (Section 2), base-selection.md (Section 3), refactor-plan.md (Section 4), merge-log.md (Section 5), merged output format. |
| `debate-protocol.md` | `refs/debate-protocol.md` | — | Debate round structure: round 1 (parallel advocate presentations), round 2 (sequential rebuttals), round 3 (conditional final arguments). Steelman strategy rules. Convergence measurement. |
| `scoring-protocol.md` | `refs/scoring-protocol.md` | — | Complete scoring algorithm: quantitative formula (RC×0.30 + IC×0.25 + SR×0.15 + DC×0.15 + SC×0.15), qualitative 30-criterion binary rubric (6 dimensions × 5 criteria), Claim-Evidence-Verdict protocol, edge-case floor threshold, combined scoring formula, tiebreaker protocol. |
| `__init__.py` | `__init__.py` | 0B | Python package marker. |

### A3. Python CLI Implementation (6 files)

All at: `/config/.local/lib/python3.12/site-packages/superclaude/_src/superclaude/cli/tasklist/`

| File | Lines | Purpose | Dependencies |
|------|-------|---------|-------------|
| `__init__.py` | — | Package init | — |
| `commands.py` | ~60 | Click command group `superclaude tasklist validate`. Flags: `--roadmap-file`, `--tasklist-dir`, `--model`, `--max-turns`, `--debug`. FR-016/FR-017 compliance. | click |
| `executor.py` | ~100+ | Orchestrates validation: reads roadmap + tasklist files, builds fidelity prompt, applies `TASKLIST_FIDELITY_GATE`, writes fidelity report. Context isolation: each subprocess receives only prompt + `--file` inputs. Embed size limit: 100KB before switching to `--file` flags. | `pipeline.executor.execute_pipeline`, `pipeline.process.ClaudeProcess`, `pipeline.models.PipelineConfig/Step/StepResult/StepStatus` |
| `models.py` | 25 | `TasklistValidateConfig` dataclass extending `PipelineConfig`. Fields: `output_dir`, `roadmap_file`, `tasklist_dir`. | `pipeline.models.PipelineConfig` |
| `gates.py` | 43 | `TASKLIST_FIDELITY_GATE` constant: requires 6 frontmatter fields (`high_severity_count`, `medium_severity_count`, `low_severity_count`, `total_deviations`, `validation_complete`, `tasklist_ready`), 2 semantic checks (`high_severity_count_zero`, `tasklist_ready_consistent`). Enforcement tier: STRICT. | `pipeline.models.GateCriteria/SemanticCheck`, `roadmap.gates._high_severity_count_zero/_tasklist_ready_consistent` |
| `prompts.py` | ~80+ | `build_tasklist_fidelity_prompt()`: pure function, no I/O. Validates roadmap→tasklist alignment ONLY (validation layering guard). Embeds severity definitions (HIGH/MEDIUM/LOW) to reduce LLM classification drift (RSK-007). Reuses deviation report format from Phase 2. | `roadmap.prompts._OUTPUT_FORMAT_BLOCK` |

### A4. Python CLI Cross-Dependencies

The tasklist CLI module imports from these sibling modules:

| Module | Files Imported | What's Used |
|--------|---------------|-------------|
| `pipeline/` | `executor.py`, `process.py`, `models.py` | `execute_pipeline()`, `ClaudeProcess`, `PipelineConfig`, `Step`, `StepResult`, `StepStatus`, `GateCriteria`, `SemanticCheck` |
| `roadmap/` | `gates.py`, `prompts.py` | `_high_severity_count_zero()`, `_tasklist_ready_consistent()`, `_OUTPUT_FORMAT_BLOCK` |

---

## B) Rigorflow Framework

All RF files live in the llm-workflows repo at `/config/workspace/llm-workflows/`.

### B1. Commands (1 primary + 6 related)

| File | Location | Lines | Purpose |
|------|----------|-------|---------|
| **`taskbuilder.md`** | `.claude/commands/rf/taskbuilder.md` | 359 | **Primary**. Full interactive task builder: 3-stage interview (Core Intent → Phases & Steps → Guardrails), template discovery, self-contained checklist item synthesis with session-rollover protection, 12-point pre-write validation checklist. |
| `pipeline.md` | `.claude/commands/rf/pipeline.md` | 897 | Agent team orchestrator: Parse/Triage/Split → TeamCreate → spawn researcher(s) → review research → spawn builder(s) → spawn executor(s) → monitor → report → cleanup. Supports N parallel tracks (max 5). |
| `project.md` | `.claude/commands/rf/project.md` | 498 | Multi-phase project: Phase 0 planning artifacts (feature brief, PRD, architecture proposal) → sequential `/rf:pipeline` invocations per implementation phase. |
| `task.md` | `.claude/commands/rf/task.md` | 49 | Execution wrapper: user selects task file, batch size, iterations → invokes `automated_qa_workflow.sh`. |
| `run.md` | `.claude/commands/rf/run.md` | 203 | Simple build+execute without agent teams: spawns builder then executor directly. |
| `opinion.md` | `.claude/commands/rf/opinion.md` | 246 | Anti-sycophancy analysis: 3-layer model (Constitutional AI, CoVe, Adversarial Debate). |
| `opinion_v2_deterministic.md` | `.claude/commands/rf/opinion_v2_deterministic.md` | 357 | Deterministic evidence-scoring replacement for v1 adversarial debate. |

### B2. Agent Definitions (4 files)

| File | Location | Lines | Model | Key Behaviors |
|------|----------|-------|-------|---------------|
| **`rf-task-builder.md`** | `.claude/agents/rf-task-builder.md` | 369 | opus | Receives `BUILD_REQUEST` from team lead. Reads MDTM template (01 or 02). Uses researcher context. Builds self-contained checklist items. Broadcasts `TASK_READY`. Supports WebSearch for unfamiliar tech. |
| `rf-task-researcher.md` | `.claude/agents/rf-task-researcher.md` | 447 | opus | Explores codebase (Glob/Grep/Read). External research via WebSearch. Trade-off analysis via `/rf:opinion`. Writes research notes to `.dev/tasks/`. Sends `RESEARCH_READY`. Solution research section for new implementations. |
| `rf-task-executor.md` | `.claude/agents/rf-task-executor.md` | 370 | opus | Validates task file. Runs `bash .gfdoc/scripts/automated_qa_workflow.sh <task> <batch_size> 0`. Reports `EXECUTION_COMPLETE`. Never uses timeout. Never runs in background. |
| `rf-team-lead.md` | `.claude/agents/rf-team-lead.md` | ~500+ | opus | Spawns and coordinates team. Parallel track support (researcher-N, builder-N, executor-N). Reviews research quality before spawning builders. Relays user input. Per-track state management. Has TeamCreate/TeamDelete tools. |

### B3. Agent Memory (3 directories)

| Directory | Purpose |
|-----------|---------|
| `.claude/agent-memory/rf-task-builder/MEMORY.md` | Learned task-building patterns, batch size recommendations, template notes |
| `.claude/agent-memory/rf-task-researcher/MEMORY.md` | Codebase structure knowledge, file location patterns |
| `.claude/agent-memory/rf-task-executor/MEMORY.md` | Execution patterns, error recovery notes |

### B4. Templates (8 files)

| File | Location | Purpose |
|------|----------|---------|
| **`01_mdtm_template_generic_task.md`** | `.gfdoc/templates/` | Simple tasks: straightforward file creation. PART 1 = building instructions, PART 2 = file template. |
| **`02_mdtm_template_complex_task.md`** | `.gfdoc/templates/` | Complex tasks: 6 handoff patterns (L1: Discovery, L2: Build-from-Discovery, L3: Test/Execute, L4: Review/QA, L5: Conditional-Action, L6: Aggregation). Phase-outputs directory structure. |
| `03_project_plan_template.md` | `.gfdoc/templates/` | Project management tracking document (NOT an MDTM task). Used by `/rf:project` Phase 0. |
| `04_feature_brief_template.md` | `.gfdoc/templates/` | Feature brief planning artifact. `/rf:project` Phase 0. |
| `05_prd_template.md` | `.gfdoc/templates/` | Product Requirements Document. `/rf:project` Phase 0. |
| `06_architecture_proposal_template.md` | `.gfdoc/templates/` | Architecture and implementation plan. `/rf:project` Phase 0. |
| `99_mdtm_template_generic_task_old.md` | `.gfdoc/templates/` | Deprecated v1 template (pre-self-contained items). |
| `changelog_template.md` | `.gfdoc/templates/` | Changelog entry template. |
| `qa_validation_checklist_template.md` | `.gfdoc/templates/` | QA validation checklist template. |

### B5. Core Scripts (10 files)

| File | Location | Lines | Purpose |
|------|----------|-------|---------|
| **`automated_qa_workflow.sh`** | `.gfdoc/scripts/` | 5,997 | Core orchestration engine. Batch management, worker/QA Claude subprocess loops, DNSP protocol (Detect-Nudge-Synthesize-Proceed), PABLOV evidence collection (fs snapshots, conversation mining, programmatic handoffs), session management (dual-threshold rollover: 375 messages OR 175K tokens), correction loops (max 5), UID-based batch refresh, security validation. |
| `input_validation.sh` | `.gfdoc/scripts/` | ~287 | Three-layer path traversal defense. Sourced by `automated_qa_workflow.sh` at startup. |
| `rollover_context_functions.sh` | `.gfdoc/scripts/` | — | Session context rollover utilities. Generates context for new sessions after threshold roll. |
| `session_message_counter.sh` | `.gfdoc/scripts/` | — | JSONL-based session message counting. Dual-threshold checking (messages + tokens). |
| `compute_uid_index.py` | `.gfdoc/scripts/` | — | UID index computation for batch item tracking. Enables stable batch identity across user edits. |
| `parse_checklist.py` | `.gfdoc/scripts/` | — | MDTM checklist parser. Extracts `- [ ]` and `- [x]` items with line numbers. |
| `health_analyzer.py` | `.gfdoc/scripts/` | — | Task health metrics scanner. Scans MDTM files, computes health metrics, outputs JSON. Python 3 stdlib only. |
| `dashboard_generator.py` | `.gfdoc/scripts/` | — | Self-contained HTML dashboard generator. Charts, filters, sortable tables. No external deps. |
| `UID_fail_item_match_fallback.py` | `.gfdoc/scripts/` | — | Fallback UID matching for failed items when primary UID matching fails. |
| `compute_uid_index_backup_20251022_1220p.py` | `.gfdoc/scripts/` | — | Backup of UID index computation (pre-refactor). |

### B6. Core Rules (8 files, session-loaded)

| File | Location | Size | Purpose |
|------|----------|------|---------|
| `ib_agent_core.md` | `.gfdoc/rules/core/` | 48KB | Core execution principles, Five-step pattern (READ→IDENTIFY→EXECUTE→UPDATE→REPEAT), agent contracts, PABLOV methodology. |
| `file_conventions.md` | `.gfdoc/rules/core/` | 52KB | Naming standards, YAML frontmatter schema, metadata conventions. |
| `quality_gates.md` | `.gfdoc/rules/core/` | 16KB | Quality verification standards, pass/fail criteria, gate definitions. |
| `anti_sycophancy.md` | `.gfdoc/rules/core/` | 8KB | Professional objectivity protocol, evidence-based assessment rules. |
| `anti_hallucination_task_completion_rules.md` | `.gfdoc/rules/core/` | 8KB | Evidence-based completion rules, anti-fabrication controls. |
| `changelog_maintenance.md` | `.gfdoc/rules/core/` | 8KB | Changelog standards, version tracking conventions. |
| `tool_selection.md` | `.gfdoc/rules/core/` | 8KB | Tool usage guidelines, selection criteria. |
| `DIRECTORY_STRUCTURE.md` | `.gfdoc/rules/core/` | 12KB | Directory layout reference for the framework. |

### B7. Agent Prompts (9 files)

| File | Location | Purpose |
|------|----------|---------|
| `agent_library.md` | `.gfdoc/rules/prompts/` | Reference for 4 worker/QA agent pairs: automated_qa_workflow, doc_code_analyst, documentation_expert, recruiting_expert. |
| `automated_qa_workflow_worker_prompt.md` | `.gfdoc/rules/prompts/` | Worker agent prompt template for automated QA workflow. |
| `automated_qa_workflow_qa_prompt.md` | `.gfdoc/rules/prompts/` | QA agent prompt template for automated QA workflow. |
| `doc_code_analyst_worker_prompt.md` | `.gfdoc/rules/prompts/` | Worker prompt for C++ code analysis specialist. |
| `doc_code_analyst_qa_prompt.md` | `.gfdoc/rules/prompts/` | QA prompt for code analysis review. |
| `documentation_expert_worker_prompt.md` | `.gfdoc/rules/prompts/` | Worker prompt for documentation specialist. |
| `documentation_expert_qa_prompt.md` | `.gfdoc/rules/prompts/` | QA prompt for documentation review. |
| `recruiting_expert_worker_prompt.md` | `.gfdoc/rules/prompts/` | Worker prompt for candidate evaluation. |
| `recruiting_expert_qa_prompt.md` | `.gfdoc/rules/prompts/` | QA prompt for recruiting review. |

### B8. Contextual Rules (1 file, hook-loaded)

| File | Location | Purpose |
|------|----------|---------|
| `context_embedding.md` | `.gfdoc/rules/contextual/` | Context review protocol for task resumption. Loaded on-demand via hooks. Referenced by taskbuilder for context file guidance. |

### B9. Documentation Guides (7 files)

| File | Location | Size | Purpose |
|------|----------|------|---------|
| `rigorflow_workflow_deep_dive_guide.md` | `.gfdoc/docs/guides/` | 137KB | Line-by-line implementation reference for `automated_qa_workflow.sh`. |
| `RIGORFLOW_BATCH_STATE_FLOW_GUIDE.md` | `.gfdoc/docs/guides/` | 50KB | Batch lifecycle, state transitions, resume scenarios, manual resolution. |
| `rigorflow_framework_changes_guide.md` | `.gfdoc/docs/guides/` | 38KB | Safe modification patterns, testing procedures, diagnostic decision tree. |
| `qa_validation_guide.md` | `.gfdoc/docs/guides/` | 25KB | 8-metrics quality measurement system. |
| `anti_sycophancy_guide.md` | `.gfdoc/docs/guides/` | 12KB | Professional objectivity standards, 2-tier system. |
| `health-monitoring-guide.md` | `.gfdoc/docs/guides/` | — | Dashboard system, analyzer CLI, JSON schema. |
| `tool_performance_benchmarks_guide.md` | `.gfdoc/docs/guides/` | 2KB | Performance data and benchmarks. |

### B10. Runtime Artifacts (per-task execution)

| Artifact | Location Pattern | Format | Purpose |
|----------|-----------------|--------|---------|
| Task file | `.dev/tasks/TASK-RF-<timestamp>.md` | Markdown + YAML frontmatter | MDTM task with checklist items |
| Research notes | `.dev/tasks/research-notes-<timestamp>.md` | Markdown | Researcher findings for builder |
| Batch state | `.dev/tasks/TASK-RF-*/batch_N_state.json` | JSON | Per-batch state machine (`initialized` → `worker_in_progress` → `worker_complete` → `qa_in_progress` → `qa_complete`) |
| Expected set | `.dev/tasks/TASK-RF-*/expected_batchN.json` | JSON | Batch items with line numbers and UIDs |
| Worker handoff | `.dev/tasks/TASK-RF-*/handoffs/worker_handoff_batchN.md` | Markdown | Rich per-item evidence from conversation + filesystem |
| Programmatic handoff | `.dev/tasks/TASK-RF-*/programmatic_handoff_batchN.json` | JSON | Machine facts: verification results, items with evidence, conversation evidence, filtered file changes |
| QA report | `.dev/tasks/TASK-RF-*/qa_reports/qa_report_batchN.md` | Markdown | First line: `Overall Status: PASS\|FAIL`. Fail lines: `- Line <n>: FAIL — <reason>` |
| FS snapshots | `.dev/tasks/TASK-RF-*/fs_snapshot_pre_batchN.json`, `post` | JSON | Filesystem state before/after worker execution |
| Worker session | `.dev/tasks/TASK-RF-*/outputs/worker_session_batchN.json` | JSON | Raw Claude session data |
| QA session | `.dev/tasks/TASK-RF-*/outputs/qa_session_batchN.json` | JSON | Raw Claude QA session data |
| Progress log | `.dev/tasks/TASK-RF-*/logs/task_progress.log` | Text | Real-time progress: completion %, batch history, session timeline |
| Task state | `.dev/tasks/TASK-RF-*/task_state.json` | JSON | Current task checklist state (all items with check status and line numbers) |
| Task characteristics | `.dev/tasks/TASK-RF-*/task_characteristics.json` | JSON | Static vs dynamic task type, item count, phase count |
| Verification | `.dev/tasks/TASK-RF-*/verification_batchN.json` | JSON | Worker completion verification results |

---

## File Counts Summary

| Category | SC Files | RF Files |
|----------|---------|---------|
| Commands | 2 | 7 |
| Protocol/Skill packages | 12 (2 packages) | — |
| Agent definitions | — | 4 |
| Agent memory | — | 3 dirs |
| Python CLI modules | 6 | — |
| Templates | — | 9 |
| Scripts (orchestration) | — | 10 |
| Core rules | — | 8 |
| Agent prompts | — | 9 |
| Contextual rules | — | 1 |
| Documentation guides | — | 7 |
| **Total static files** | **20** | **58** |
| Runtime artifacts per task | — | ~14 per batch |
