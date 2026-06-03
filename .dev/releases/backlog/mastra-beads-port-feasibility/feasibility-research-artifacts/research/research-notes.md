# Research Notes: Mastra + Backlog.md + Beads Port Feasibility

**Date:** 2026-06-02
**Scenario:** A — explicit request with goal, target stack, output path, and substantial seed context
**Depth Tier:** Deep
**Status:** Complete

---

## EXISTING_FILES

### Requested output directory and existing enrichment

| Path | Purpose | Key contents / exports | Approx. line count | Notes |
|---|---|---:|---:|---|
| `.dev/releases/backlog/mastra-beads-port-feasibility/seed-brief.md` | Existing seed brief for the feasibility study | Problem statement, constraints, success criteria, open questions, enrichment pointers | 60 | [CODE-VERIFIED] Read during scope discovery. User-requested output directory already contains seed material. |
| `.dev/releases/backlog/mastra-beads-port-feasibility/enrichment/codebase-context.md` | Existing codebase context enrichment | Current orchestration architecture, porting seams, reuse inventory, feasibility implication | 80 | [CODE-VERIFIED] Read during scope discovery. Strong starting point but not a final feasibility report. |
| `.dev/releases/backlog/mastra-beads-port-feasibility/enrichment/research-deep.md` | Existing external research enrichment | Mastra, Backlog.md, Beads, MCP ecosystem findings and source URLs | 120 | [UNVERIFIED external] Useful seed, but Phase 4 web research must refresh/validate current external claims. |

### CLI orchestration source files

| Path / directory | Purpose | Key exports / components | Approx. line count | Notes |
|---|---|---|---:|---|
| `src/superclaude/cli/main.py` | Click root command registration | `main`, deferred command registration for sprint, roadmap, cleanup-audit, tasklist, cli-portify, prd, eval | ~430 | [CODE-VERIFIED via codebase retrieval + scope agents] Entry point for CLI surface inventory. |
| `src/superclaude/cli/pipeline/` | Shared pipeline engine | `Step`, `StepResult`, `PipelineConfig`, `GateCriteria`, `GateMode`, `execute_pipeline`, gate validation, trailing gates, process wrapper, diagnostics passes | ~22 files | Highest-value porting seam; model vocabulary can map to TypeScript/Zod/Mastra contracts. |
| `src/superclaude/cli/pipeline/executor.py` | Generic step sequencer | Sequential/parallel groups, retry, blocking/trailing gate evaluation, cosmetic remediation lane, cancel propagation | ~469 | [CODE-VERIFIED in existing enrichment] Domain-independent orchestration kernel. |
| `src/superclaude/cli/pipeline/models.py` | Shared pipeline dataclasses | `StepStatus`, `GateMode`, `GateCriteria`, `Step`, `StepResult`, `Deliverable`, `SemanticCheck` | ~250 | Contract vocabulary to preserve in any port. |
| `src/superclaude/cli/pipeline/process.py` | Claude subprocess boundary | `ClaudeProcess`, prompt-over-stdin, process groups, stdout/stderr file capture, tool write mode validation | ~200 | Compatibility boundary for hybrid Mastra adapter. |
| `src/superclaude/cli/pipeline/gates.py` | Generic gate enforcement | EXEMPT/LIGHT/STANDARD/STRICT tier cascade, frontmatter checks, semantic checks | ~200 | Candidate for provider-neutral validators/scorers. |
| `src/superclaude/cli/pipeline/trailing_gate.py` | Async/trailing gate support | `TrailingGateRunner`, `GateResultQueue`, `DeferredRemediationLog`, `TrailingGatePolicy`, `resolve_gate_mode` | ~300 | Important for Mastra async validation semantics. |
| `src/superclaude/cli/roadmap/` | Roadmap generation and validation pipeline | `roadmap run`, `roadmap validate`, extraction, parallel generation, debate, merge, convergence, remediation, certification | ~22 files | Natural first/second Mastra workflow candidate after smaller validators. |
| `src/superclaude/cli/roadmap/commands.py` | Roadmap CLI surface | `run`, `validate`, `accept-spec-change`; input routing, flags, config creation | ~400 | Must be inventoried for compatibility/flag parity. |
| `src/superclaude/cli/roadmap/executor.py` | Roadmap orchestration | Multi-step pipeline, A/B generation, diff/debate/score/merge, validation, convergence, compression sidecars | ~3700 | Large and contract-heavy; likely reimplement in phases rather than direct rewrite. |
| `src/superclaude/cli/roadmap/gates.py` | Roadmap gate definitions | 15 named gates including extraction/generation/diff/debate/merge/test-strategy/spec-fidelity/wiring/deviation/remediate/certify | ~300 | Must verify which gates are wired and which remain defined-only. |
| `src/superclaude/cli/roadmap/prompts.py` | Roadmap prompt builders | Prompt builders with incremental writing wrappers | ~900 | Reuse as prompt assets or translate to declarative templates. |
| `src/superclaude/cli/sprint/` | Long-running sprint execution from tasklists | `sprint run`, tmux/TUI/status/logs/kill, phase discovery, task parsing, process supervision, turn ledger, checkpoints | ~18 files | Hardest port because it couples workflow, process supervision, terminal UX, budgets, and isolation. |
| `src/superclaude/cli/sprint/commands.py` | Sprint CLI surface | `run`, `attach`, `status`, `logs`, `kill`, `verify-checkpoints` | ~350 | Must inventory CLI compatibility and operational modes. |
| `src/superclaude/cli/sprint/executor.py` | Sprint orchestration loop | `execute_sprint`, phase loop, preflight, task delegation, TUI/logging, stalls, checkpoint and hook integrations | ~2148 | Primary stress test for Mastra migration. |
| `src/superclaude/cli/sprint/models.py` | Sprint models | `SprintConfig`, `Phase`, `TaskEntry`, `TaskResult`, `PhaseResult`, `TurnLedger`, checkpoint/gate display state | ~700 | Budget/state model must be preserved or intentionally replaced. |
| `src/superclaude/cli/sprint/config.py` | Phase/tasklist parsing and config loading | Phase discovery, task parsing, `load_sprint_config` | ~500 | Maps Backlog/Beads issue/task graph to current tasklist index semantics. |
| `src/superclaude/cli/sprint/process.py` | Sprint-specific Claude process | Context injection, compression, signal handling | ~500 | Determines how hybrid wrappers retain Claude Code execution safety. |
| `src/superclaude/cli/sprint/monitor.py` | NDJSON output monitor | Stall detection, token/turn counting, output parsing | ~300 | Candidate for Mastra observability replacement/adapter. |
| `src/superclaude/cli/sprint/tmux.py`, `tui.py` | Terminal UX/session management | tmux launch/attach/kill; Rich dashboard | ~700 combined | Low direct reuse in web/server runtime. |
| `src/superclaude/cli/sprint/checkpoints.py` | Checkpoint manifest support | Build/recover/verify checkpoint entries | ~300 | Reusable semantics for durable workflow checkpoints. |
| `src/superclaude/cli/tasklist/` | Tasklist validation CLI | `tasklist validate`, fidelity prompt/gate/model | ~5-7 files | Small candidate for early adapter/prototype. |
| `src/superclaude/cli/cleanup_audit/` | Cleanup audit CLI runner | 6-step supervised audit loop, gates, prompts, TUI, diagnostics | ~11-13 files | Good pattern for multi-pass fan-out/consolidate/validate, but less generic than pipeline core. |
| `src/superclaude/cli/cli_portify/` | Workflow-to-CLI portification runner | Commands, executor, registry, contract, convergence, resume, steps, gates/prompts | ~16-20 files | Highly relevant because it already studies converting inference workflows to deterministic pipelines. |
| `src/superclaude/cli/prd/` | PRD pipeline runner | 15-step PRD pipeline with dynamic Stage B, QA fix cycles, sentinel detection | ~14 files | Useful analog for staged investigation + synthesis pipelines. |
| `src/superclaude/cli/eval/` | Evaluation harness | Parallel eval orchestrator, HOME isolation, PTY driver, capability gates, suites/schemas | ~22-25 files | Important for validating future Mastra port parity. |
| `src/superclaude/cli/audit/` | Audit infrastructure | Wiring validation, classification, profiler, dependency graph, dead code, duplication, coverage | ~33-42 files | Validation and code-analysis capability that may become Mastra tools/scorers. |

### Skills, agents, commands, templates, and harness assets

| Path / directory | Purpose | Key exports / components | Approx. line count | Notes |
|---|---|---|---:|---|
| `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` | Inference-layer roadmap protocol | Roadmap waves, adversarial integration, output artifacts | ~hundreds | Need compare with CLI roadmap divergence. |
| `src/superclaude/skills/sc-tasklist-protocol/` | Roadmap-to-tasklist generator skill | 10-stage pipeline, file emission rules, tier classification, phase/index templates | skill + rules/templates | Feeds `superclaude sprint run`; important for Backlog/Beads mapping. |
| `src/superclaude/skills/sc-adversarial-protocol/` | Debate/score/merge protocol | Agent specs, debate protocol, scoring, artifact templates | skill + refs | Reusable workflow pattern for Mastra multi-agent workflows. |
| `src/superclaude/skills/sc-cli-portify-protocol/` | Protocol for converting skills to CLI pipelines | Analysis protocol, pipeline spec, code templates, decisions | skill + refs | Directly relevant as migration-method reference. |
| `src/superclaude/skills/tech-research/SKILL.md` | Current deep research protocol | MDTM task creation/execution, research/synthesis/QA/assembly phases | ~1390 | The current investigation itself uses this protocol. |
| `src/superclaude/skills/task-builder/SKILL.md` | MDTM task builder protocol | Task-file generation, research handoff, QA workflow | ~2191 | Key reusable methodology for Backlog/Beads task record mapping. |
| `src/superclaude/agents/rf-task-builder.md` | Rigorflow task file builder | Builds MDTM files from research notes and templates | agent file | Reusable as Mastra agent definition content. |
| `src/superclaude/agents/rf-task-executor.md` | Rigorflow task executor | Executes MDTM task files | agent file | Maps to workflow executor role. |
| `src/superclaude/agents/rf-analyst.md` | Completeness verifier | Coverage audit, evidence quality, contradiction/gap analysis | agent file | Reusable QA agent. |
| `src/superclaude/agents/rf-qa.md` | Structural QA | Research/synthesis/report/task validation, in-place fixes | agent file | Reusable QA agent. |
| `src/superclaude/agents/rf-qa-qualitative.md` | Qualitative QA | Product/engineering sense check | agent file | Reusable QA agent. |
| `src/superclaude/agents/rf-assembler.md` | Report/document assembler | Consolidates component files into final outputs | agent file | Reusable assembly workflow. |
| `src/superclaude/agents/debate-orchestrator.md` | Debate coordinator | Coordinates adversarial debate pipeline | agent file | Mastra agent/workflow role candidate. |
| `src/superclaude/core/ORCHESTRATOR.md` | Routing/intelligence rules | Detection engine, wave routing, tier classification, decision trees | core doc | Useful as routing policy source but requires code verification. |
| `src/superclaude/core/RULES.md`, `PRINCIPLES.md`, `MCP.md`, `FLAGS.md` | Framework rules and interfaces | Core behavioral rules, MCP table, flags/personas/modes | core docs | Reusable instruction corpus. |
| `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` | Complex MDTM task template | Granular checklist, B2 self-contained items, execution loop | template | Must be read by task builder. |
| `src/superclaude/commands/roadmap.md`, `tasklist.md`, `adversarial.md`, `cleanup-audit.md`, `cli-portify.md` | Slash-command front doors | Skill invocation and argument surfaces | command markdown | Need mapping from slash command to skill/CLI/Mastra entrypoints. |
| `src/superclaude/hooks/` | Hook definitions/scripts | Freshness, auggie, PR review, workspace write guards | hooks/scripts | Multi-tenant port must decide what hook logic moves to policy gates. |
| `src/superclaude/mcp/` | MCP configs and docs | Server definitions for auggie/context7/playwright/serena/tavily/magic/etc. | configs/docs | Integration boundaries for target runtime. |

### Documentation to read and cross-validate

| Path | Purpose | Verification status / risk |
|---|---|---|
| `docs/guides/cli-portify-and-pipeline-runner-guide.md` | Existing design guide for pipeline runner and porting skill workflows to CLI runners | [UNVERIFIED doc] Must cross-check against current `cli/pipeline`, `cli/cli_portify`, and roadmap/tasklist code. |
| `docs/generated/cli-portify-release-guide.md` | Generated CLI portify release/reference guide | [UNVERIFIED doc] Useful but must cross-check release claims. |
| `docs/generated/sprint-cli/` | Generated sprint CLI architecture docs | [UNVERIFIED doc] Useful as inventory; needs code-verification because sprint evolved. |
| `docs/generated/contributor-knowledge-base/` | Contributor architecture map and CLI API inventory | [UNVERIFIED doc] Good broad map; not sufficient for current-state claims. |
| `docs/analysis/skill-vs-cli-divergence-roadmap.md` | Skill-vs-CLI divergence analysis for roadmap | [UNVERIFIED doc] High-value but dated; must verify. |
| `docs/analysis/claude-task-master-vs-superclaude-comparison.md` | Competitive comparison including SuperClaude CLI architecture summary | [UNVERIFIED doc] Use for framing, not current state. |
| `.dev/releases/complete/v2.15-cli-portify/` through `.dev/releases/complete/v2.25-cli-portify-cli/` | Historical CLI portify release artifacts | [Historical] Useful for evolution and rationale. |
| `.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/artifacts/dependency-map.md` | Cross-framework integration points between SC/RF/tasklist/sprint | [UNVERIFIED doc] Likely useful for task-system mapping. |

## PATTERNS_AND_CONVENTIONS

### Code and artifact patterns

| Pattern | Evidence / paths | Port implication |
|---|---|---|
| Click command package per CLI domain | `src/superclaude/cli/main.py`, `src/superclaude/cli/<domain>/commands.py` | Mastra front doors can preserve CLI compatibility via wrapper commands while workflows move server-side. |
| Standard CLI package shape | `commands.py`, `executor.py`, `models.py`, `gates.py`, `prompts.py`, plus `config.py`, `process.py`, `monitor.py`, `tui.py`, `logging_.py`, `diagnostics.py` where needed | Port should preserve domain boundaries and contracts; not everything belongs in a generic workflow layer. |
| Generic step/gate pipeline core | `src/superclaude/cli/pipeline/` | Strongest TypeScript contract extraction target. |
| Parallel groups modeled as nested step lists | `execute_pipeline()` semantics from scope agents and enrichment | Maps to Mastra workflow parallelism; must verify exact failure/retry semantics. |
| Blocking vs trailing gates | `pipeline/gates.py`, `pipeline/trailing_gate.py` | Maps to synchronous validation and async/advisory evaluations/scorers. |
| File-first artifacts with frontmatter | Roadmap, tasklist, research, release artifacts, MDTM templates | Backlog.md can own human-readable markdown artifacts; Mastra should not replace the artifact model prematurely. |
| Incremental writing and resumability | `tech-research`, `task-builder`, MDTM templates, roadmap state files | Mastra workflows need durable snapshots and file/DB state reconciliation. |
| Subprocess boundary via Claude Code | `pipeline/process.py`, `sprint/process.py`, executor files | Hybrid adapter should preserve Claude Code subprocess execution before native reimplementation. |
| Fan-out → consolidate → verify workflows | `sc-adversarial`, `sc-cleanup-audit`, `tech-research`, `prd`, `roadmap` | Mastra is likely a good fit if workflows can support durable fan-out and QA gates. |
| Agent/skill markdown as instruction corpus | `src/superclaude/skills/`, `src/superclaude/agents/`, `src/superclaude/core/` | High reuse as prompt/instruction assets; adaptation needed for tool names and runtime APIs. |
| MDTM checklist as persistent progress record | `.dev/tasks/to-do/TASK-*/`, `templates/workflow/02_mdtm_template_complex_task.md` | Backlog.md tasks and Beads issue graph can mirror or replace parts of this, but ownership boundaries must be explicit. |

### Documentation staleness findings from scope discovery

| Claim / source | Status | Required follow-up |
|---|---|---|
| Existing enrichment says pipeline executor, models, and process boundary are primary seams | [CODE-VERIFIED by existing enrichment + scope agents] | Deep research agents should re-read exact files and cite current line numbers. |
| Docs claim roadmap uses `execute_pipeline()` while sprint/cleanup_audit/cli_portify use bespoke executors | [CODE-VERIFIED by scope agents] | Deep research should verify directly with file reads. |
| Docs claim several roadmap/cli_portify/sprint gates/components are unwired | [UNVERIFIED / likely stale] | Dedicated agent must re-check current HEAD; do not build recommendations on stale unwired counts. |
| External claims about Mastra 1.0, Backlog.md BACK-407, Beads v1.0 and Dolt/SQLite storage | [UNVERIFIED external] | Web research agents must validate current docs/repos and licensing. |
| P3/P4 proposal docs marked approved | [UNVERIFIED / possible stale] | Codebase doc analyst must verify whether proposals landed in code. |

## SOLUTION_RESEARCH

This is a feasibility/roadmap investigation, not an implementation. Scope discovery identified the following approaches to evaluate in the final report:

| Approach | Description | Initial stance | Research needed |
|---|---|---|---|
| Option A — Hybrid adapter-first | Mastra orchestrates high-level workflows and traces while existing Python CLIs continue to execute through compatibility adapters; Backlog.md records markdown tasks/specs/decisions; Beads mirrors execution dependency graph and agent memory. | Most plausible and lowest migration risk. | Verify Mastra workflow/process invocation capabilities, state durability, subprocess/tool adapter patterns, Backlog/Beads ownership boundaries. |
| Option B — Native Mastra reimplementation | Translate pipeline core, roadmap, tasklist, sprint, PRD/audit workflows into TypeScript Mastra workflows and agents; replace most Python orchestration. | High long-term value but high complexity/risk. | Extract TypeScript contracts, gate semantics, prompt assets, process replacement, auth/RBAC, tests/evals. |
| Option C — Preserve Python CLI, add Backlog/Beads only | Keep SuperClaude Python orchestration as primary runtime; add Backlog.md and Beads adapters for task/spec/dependency memory; no Mastra runtime initially. | Good incremental tooling upgrade, but less of a multi-tenant control plane. | Verify whether multi-tenant needs can be satisfied without Mastra Studio/server. |
| Option D — Defer / not recommended | Determine that target stack cannot meet parity, licensing, tenancy, or workflow durability needs. | Must remain possible; user explicitly does not assume upgrade is worthwhile. | Identify hard blockers and decision gates. |

External research topics required before recommendation:

1. Current Mastra workflow, agent, storage, observability, auth/RBAC, MCP, and deployment capabilities and licensing.
2. Current Backlog.md CLI/MCP/task/docs/decision schema, metadata extensibility, and multi-user/git behavior.
3. Current Beads storage model, JSON/CLI contract, dependency semantics, server/multi-writer behavior, and UI ecosystem.
4. Comparative governance: MCP limitations for tenancy/audit/cost attribution; whether target stack needs an explicit control-plane layer.

## RECOMMENDED_OUTPUTS

### Task-folder artifacts

| Output path | Purpose |
|---|---|
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/01-pipeline-core-contracts.md` | Code-traced analysis of shared pipeline core, gates, process boundary, and reusable contracts. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/02-roadmap-tasklist-pipelines.md` | Code-traced analysis of roadmap run/validate, tasklist validation/generation adjacency, adversarial pipeline semantics. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/03-sprint-execution-runtime.md` | Code-traced analysis of sprint run, task parsing, subprocess delegation, tmux/TUI, ledgers, checkpoints, monitoring. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/04-cli-portify-prd-cleanup-audit-eval.md` | Analysis of adjacent orchestration tools and validation/eval patterns. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/05-skills-agents-harness-reuse.md` | Inventory of reusable skill/agent/core/template/hook assets and adaptation needs. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/06-docs-and-existing-feasibility-artifacts.md` | Documentation analyst report cross-validating existing seed/enrichment/docs against code and marking stale claims. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/07-target-data-model-and-ownership.md` | Architecture analysis of mapping current artifacts/tasks/states to Mastra, Backlog.md, and Beads ownership boundaries. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/web-01-mastra-current-capabilities.md` | External research on Mastra current docs, workflows, auth/RBAC/licensing, storage, MCP, deployment. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/web-02-backlog-md-current-capabilities.md` | External research on Backlog.md CLI/MCP/task/docs/decision capabilities and metadata. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/web-03-beads-current-capabilities.md` | External research on Beads CLI/schema/dependencies/storage/server mode/UI. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/web-04-mcp-multitenancy-governance.md` | External research on MCP boundaries, multi-tenancy, audit, cost attribution, governance implications. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/synthesis/synth-01-problem-current-state.md` | Report Sections 1-2. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/synthesis/synth-02-target-gaps.md` | Report Sections 3-4. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/synthesis/synth-03-external-findings.md` | Report Section 5. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/synthesis/synth-04-options-recommendation.md` | Report Sections 6-7. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/synthesis/synth-05-implementation-roadmap.md` | Report Section 8. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/synthesis/synth-06-risk-questions-evidence.md` | Report Sections 9-10 plus risk register support. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/RESEARCH-REPORT-mastra-beads-port-feasibility.md` | Final report assembled by `rf-assembler` in task folder. |

### User-requested release/backlog outputs

| Output path | Purpose |
|---|---|
| `.dev/releases/backlog/mastra-beads-port-feasibility/FEASIBILITY-STUDY.md` | Final user-facing feasibility study and high-level roadmap, copied/assembled from the validated task-folder research report. |
| `.dev/releases/backlog/mastra-beads-port-feasibility/ROADMAP.md` | Concise phased roadmap extracted from report Section 8 for backlog/release planning. |
| `.dev/releases/backlog/mastra-beads-port-feasibility/RISK-REGISTER.md` | Concise risk register extracted from report Sections 4, 6, 7, and 9. |
| `.dev/releases/backlog/mastra-beads-port-feasibility/DECISION-SUMMARY.md` | Executive decision memo: feasibility verdict, recommended option, go/no-go gates, next pilot. |

## SUGGESTED_PHASES

### Phase 2 — Deep codebase investigation assignments

1. **Agent 01 — Pipeline Core Contracts**
   - Type: Code Tracer / Integration Mapper
   - Topic: Shared pipeline models, executor, gates, trailing gates, process boundary, diagnostics contracts.
   - Files/directories: `src/superclaude/cli/pipeline/`, especially `models.py`, `executor.py`, `gates.py`, `process.py`, `trailing_gate.py`, `deliverables.py`, `diagnostic_chain.py`.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/01-pipeline-core-contracts.md`
   - Synthesis mapping: Sections 2, 4, 6, 8.

2. **Agent 02 — Roadmap and Tasklist Pipelines**
   - Type: Code Tracer / Architecture Analyst
   - Topic: Roadmap run/validate pipeline, adversarial workflow, convergence/remediation, tasklist validation and sprint-compatible tasklist output adjacency.
   - Files/directories: `src/superclaude/cli/roadmap/`, `src/superclaude/cli/tasklist/`, `src/superclaude/skills/sc-roadmap-protocol/`, `src/superclaude/skills/sc-tasklist-protocol/`, `src/superclaude/commands/roadmap.md`, `src/superclaude/commands/tasklist.md`.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/02-roadmap-tasklist-pipelines.md`
   - Synthesis mapping: Sections 2, 4, 6, 8.

3. **Agent 03 — Sprint Execution Runtime**
   - Type: Code Tracer / Architecture Analyst
   - Topic: Sprint run execution semantics, phase/task parsing, subprocess/session management, TUI/tmux, TurnLedger, checkpoints, monitoring, stall handling, recovery.
   - Files/directories: `src/superclaude/cli/sprint/`, generated sprint docs for comparison only.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/03-sprint-execution-runtime.md`
   - Synthesis mapping: Sections 2, 4, 6, 8.

4. **Agent 04 — Adjacent Orchestration Tools**
   - Type: Pattern Investigator / Integration Mapper
   - Topic: CLI portify, PRD, cleanup-audit, eval, audit infrastructure and what they reveal about reusable orchestration patterns, evaluation, QA, and migration methodology.
   - Files/directories: `src/superclaude/cli/cli_portify/`, `src/superclaude/cli/prd/`, `src/superclaude/cli/cleanup_audit/`, `src/superclaude/cli/eval/`, `src/superclaude/cli/audit/`.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/04-cli-portify-prd-cleanup-audit-eval.md`
   - Synthesis mapping: Sections 2, 4, 6, 8.

5. **Agent 05 — Skills, Agents, Harness Reuse**
   - Type: Integration Mapper / Pattern Investigator
   - Topic: Reuse strategy for skills, agents, commands, core rules, templates, hooks, MCP configs, Rigorflow agents, MDTM templates, and slash-command invocation surfaces.
   - Files/directories: `src/superclaude/skills/`, `src/superclaude/agents/`, `src/superclaude/commands/`, `src/superclaude/core/`, `src/superclaude/templates/`, `src/superclaude/hooks/`, `src/superclaude/mcp/`.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/05-skills-agents-harness-reuse.md`
   - Synthesis mapping: Sections 2, 3, 4, 6, 8.

6. **Agent 06 — Documentation and Existing Feasibility Artifacts**
   - Type: Doc Analyst
   - Topic: Cross-validate existing seed/enrichment files and generated docs against current code; surface stale claims and prior analysis useful for the final feasibility report.
   - Files/directories: `.dev/releases/backlog/mastra-beads-port-feasibility/`, `docs/guides/cli-portify-and-pipeline-runner-guide.md`, `docs/generated/cli-portify-release-guide.md`, `docs/generated/sprint-cli/`, `docs/generated/contributor-knowledge-base/`, `docs/analysis/skill-vs-cli-divergence-roadmap.md`, `.dev/releases/complete/v2.*cli-portify*`, `.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/artifacts/dependency-map.md`.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/06-docs-and-existing-feasibility-artifacts.md`
   - Synthesis mapping: Sections 1, 2, 4, 9, 10.

7. **Agent 07 — Target Data Model and Ownership Mapping**
   - Type: Architecture Analyst / Integration Mapper
   - Topic: Map current artifact/state/task concepts to Mastra workflows/traces, Backlog.md markdown tasks/docs/decisions, and Beads issue/dependency graph; recommend ownership boundaries and sync/adapter contracts.
   - Files/directories: current research notes, `.dev/tasks/` task folder patterns, `.dev/releases/backlog/mastra-beads-port-feasibility/seed-brief.md`, `src/superclaude/cli/sprint/config.py`, `src/superclaude/cli/sprint/models.py`, `src/superclaude/cli/pipeline/models.py`, `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`, `src/superclaude/skills/sc-tasklist-protocol/`.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/07-target-data-model-and-ownership.md`
   - Synthesis mapping: Sections 3, 4, 6, 7, 8.

### Phase 4 — Web research assignments

1. **Web Agent 01 — Mastra Current Capabilities and Licensing**
   - Topic: Mastra current workflow/agent/storage/observability/deployment/auth/RBAC/MCP capabilities; verify 1.0+ claims and Enterprise licensing.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/web-01-mastra-current-capabilities.md`
   - Synthesis mapping: Sections 3, 4, 5, 6, 7, 8, 9.

2. **Web Agent 02 — Backlog.md Current Capabilities**
   - Topic: Backlog.md CLI/MCP/schema/docs/decision/browser capabilities, metadata extensibility, no-git/git modes, agent workflow guidance, current maturity.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/web-02-backlog-md-current-capabilities.md`
   - Synthesis mapping: Sections 3, 4, 5, 6, 8, 9.

3. **Web Agent 03 — Beads Current Capabilities**
   - Topic: Beads CLI, issue graph, storage backend, JSON/CLI contract, Dolt/server mode, dependency semantics, UI options, multi-writer behavior.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/web-03-beads-current-capabilities.md`
   - Synthesis mapping: Sections 3, 4, 5, 6, 8, 9.

4. **Web Agent 04 — MCP and Multi-Tenant Governance**
   - Topic: MCP enterprise limitations, tenancy/audit/cost attribution gaps, governance/control-plane patterns for AI orchestration systems, and whether Mastra+Backlog+Beads needs extra governance services.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/web-04-mcp-multitenancy-governance.md`
   - Synthesis mapping: Sections 3, 4, 5, 6, 7, 8, 9.

### Phase 5 — Synthesis assignments

1. **Synthesis 01 — Problem and Current State**
   - Reads: research files 01-06, seed/enrichment artifacts, gaps log.
   - Produces: Sections 1 and 2.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/synthesis/synth-01-problem-current-state.md`

2. **Synthesis 02 — Target State and Gap Analysis**
   - Reads: all codebase research files, web research files, gaps log.
   - Produces: Sections 3 and 4.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/synthesis/synth-02-target-gaps.md`

3. **Synthesis 03 — External Findings**
   - Reads: web research files 01-04 and external portions of existing enrichment.
   - Produces: Section 5.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/synthesis/synth-03-external-findings.md`

4. **Synthesis 04 — Options and Recommendation**
   - Reads: all research files and gaps log.
   - Produces: Sections 6 and 7, including feasibility verdict and confidence bands.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/synthesis/synth-04-options-recommendation.md`

5. **Synthesis 05 — Implementation Roadmap**
   - Reads: all codebase research files, web research files, target ownership mapping.
   - Produces: Section 8 plus high-level roadmap extraction material.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/synthesis/synth-05-implementation-roadmap.md`

6. **Synthesis 06 — Risks, Open Questions, Evidence**
   - Reads: all research files, QA reports, gaps log.
   - Produces: Sections 9 and 10 plus risk-register extraction material.
   - Output: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/synthesis/synth-06-risk-questions-evidence.md`

## TEMPLATE_NOTES

Use MDTM Template 02 (`src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` / `.claude/templates/workflow/02_mdtm_template_complex_task.md`) because this investigation requires:

- Deep discovery across multiple CLI packages, skills, agents, docs, and external tools.
- Parallel codebase research agents.
- Parallel web research agents.
- Analyst + QA gates for research and synthesis.
- Synthesis, assembly, report validation, qualitative QA, and final release-directory outputs.
- Conditional gap-filling if QA fails.

The task file must also incorporate the user-requested release/backlog output directory. The canonical research artifacts can remain in the MDTM task folder, but Phase 6/7 must create or copy validated deliverables into `.dev/releases/backlog/mastra-beads-port-feasibility/`:

- `FEASIBILITY-STUDY.md`
- `ROADMAP.md`
- `RISK-REGISTER.md`
- `DECISION-SUMMARY.md`

## AMBIGUITIES_FOR_USER

None — intent is clear from the request and codebase context. The only strategic ambiguity is a required research output, not a blocker: the final report must explicitly decide the recommended work-of-record ownership model among Backlog.md, Beads, and Mastra, and must not assume the port is worthwhile until evidence supports it.
