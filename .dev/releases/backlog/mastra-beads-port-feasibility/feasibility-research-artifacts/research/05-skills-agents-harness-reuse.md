# Research: 05 - Skills, Agents, Harness Reuse
**Investigation type:** Integration Mapper / Pattern Investigator
**Scope:** src/superclaude/skills/, src/superclaude/agents/, src/superclaude/commands/, src/superclaude/core/, src/superclaude/templates/, src/superclaude/hooks/, src/superclaude/mcp/
**Status:** Complete
**Date:** 2026-06-02
---

**Target-stack caveat:** Mentions of Mastra, Backlog.md, and Beads in reuse/adaptation implications are target hypotheses for a possible port. Unless a sentence is explicitly tagged `[CODE-VERIFIED]` against this repository, target-stack capability and fit claims are `[UNVERIFIED external — pending Phase 4 web research]`, not current SuperClaude code facts.

## Section 2 — Source-of-Truth and Slash-Command Front Doors

### Source-of-truth conventions

| Asset class | Current source path | Evidence | Reuse implication for Mastra/Backlog.md/Beads |
|---|---|---|---|
| Distributable framework corpus | `src/superclaude/` | `src/superclaude/core/CLAUDE.md:17-23` identifies `core/`, `commands/`, `skills/`, `agents/`, `cli/`, and `pm_agent/` under `src/superclaude/`; `src/superclaude/core/CLAUDE.md:45-48` says edit `src/superclaude/` first and sync dev copies afterward. | Treat `src/superclaude/` as canonical instruction-corpus input for any Mastra/Beads port. Do not scrape `.claude/` dev copies as primary source. |
| Slash-command definitions | `src/superclaude/commands/*.md` | `src/superclaude/core/CLAUDE.md:19` and `src/superclaude/core/CLAUDE.md:97-102` distinguish commands from backing skills/agents. | Commands are thin front-door manifests: parse flags, validate inputs, and invoke skills. A port should preserve them as route manifests or command adapters rather than as execution engines. |
| Skill packages | `src/superclaude/skills/*/SKILL.md` plus `refs/`, `rules/`, `templates/`, `scripts/` | `src/superclaude/core/CLAUDE.md:20` lists package layout; command files repeatedly route to protocol skills, e.g. `src/superclaude/commands/task.md:156-162`, `src/superclaude/commands/tasklist.md:70-84`, `src/superclaude/commands/roadmap.md:82-92`, `src/superclaude/commands/adversarial.md:143-149`. | Skills are the main reusable instruction body. Mastra/Beads should load the skill body as workflow policy/instructions and translate Claude Code `Skill` calls into orchestration dispatch. |
| Agent definitions | `src/superclaude/agents/*.md` | `src/superclaude/core/CLAUDE.md:21`, `src/superclaude/core/CLAUDE.md:99-102` identify agents delegated by skills/commands. | Agent markdown can be reused as role prompt corpus, but Claude Code `Task`-tool semantics must be reimplemented as Mastra agent runs/jobs. |

### Slash-command inventory and integration surfaces

| Command file | Lines | Front-door pattern | Integration implication |
|---|---:|---|---|
| `src/superclaude/commands/task.md` | 186 | Unified task command with classification header, compliance tiers, TFEP, then mandatory `Skill sc:task-protocol` for STANDARD/STRICT (`src/superclaude/commands/task.md:50-69`, `src/superclaude/commands/task.md:95-103`, `src/superclaude/commands/task.md:156-162`). | Port needs a pre-dispatch classifier and a structured event/result contract for compliance tier, not just a text prompt. |
| `src/superclaude/commands/tasklist.md` | 118 | Validates roadmap/spec/output, derives `TASKLIST_ROOT`, then mandatory `Skill sc:tasklist-protocol` (`src/superclaude/commands/tasklist.md:40-47`, `src/superclaude/commands/tasklist.md:48-84`). | This is a strong candidate for deterministic CLI orchestration: convert command manifest into Beads/Backlog job that validates input before invoking LLM generation skill. |
| `src/superclaude/commands/roadmap.md` | 104 | Mirrors `superclaude roadmap run` flags and requires `Skill sc:roadmap-protocol`; line 92 explicitly states relationship to deterministic CLI counterpart (`src/superclaude/commands/roadmap.md:21-44`, `src/superclaude/commands/roadmap.md:82-92`). | Port should keep CLI parity as a compatibility boundary; Mastra workflow can call deterministic CLI stages and delegate inference-only steps to agents. |
| `src/superclaude/commands/adversarial.md` | 182 | Supports compare, generate, and DAG pipeline modes, then invokes `Skill sc:adversarial-protocol` (`src/superclaude/commands/adversarial.md:13-33`, `src/superclaude/commands/adversarial.md:74-77`, `src/superclaude/commands/adversarial.md:143-149`). | DAG semantics map naturally to Mastra workflows/Beads dependencies; artifact contract must include the six named outputs from `src/superclaude/commands/adversarial.md:74-77`. |

### Key Takeaways

- Reuse boundary: `src/superclaude/commands/*.md` should become front-door route/flag specs; `src/superclaude/skills/*` should become workflow instruction packs; `src/superclaude/agents/*.md` should become role prompts.
- The command layer is intentionally thin and repeatedly warns not to execute protocol from command files alone. Any port that embeds only command markdown will be incomplete.
- [CODE-VERIFIED] Source-of-truth is `src/superclaude/` first, with `.claude/` as synced dev copies, verified in `src/superclaude/core/CLAUDE.md:17-29` and `src/superclaude/core/CLAUDE.md:45-48`.

## Section 3 — Skill and Rigorflow Harness Reuse

### Skill inventory by reuse category

| Skill package | Lines / major refs | Current behavior evidence | Reuse strategy |
|---|---:|---|---|
| `src/superclaude/skills/sc-task-protocol/SKILL.md` | 397 | Execution-only for `/sc:task` after classification (`src/superclaude/skills/sc-task-protocol/SKILL.md:7-10`, `src/superclaude/skills/sc-task-protocol/SKILL.md:50-62`); tier-specific execution/verification (`src/superclaude/skills/sc-task-protocol/SKILL.md:80-129`); TFEP escalation (`src/superclaude/skills/sc-task-protocol/SKILL.md:133-261`); MCP tier requirements (`src/superclaude/skills/sc-task-protocol/SKILL.md:271-284`). | Reuse as compliance-policy engine. Port must externalize tool availability, tier blockers, and TFEP artifacts into explicit workflow state. |
| `src/superclaude/skills/task/SKILL.md` | 402 | Generic MDTM executor reads first unchecked item, executes exactly, marks complete, repeats (`src/superclaude/skills/task/SKILL.md:83-105`); prohibits delegating the F1 loop (`src/superclaude/skills/task/SKILL.md:110-123`, `src/superclaude/skills/task/SKILL.md:371-373`); supports parallel agent spawning for independent consecutive items (`src/superclaude/skills/task/SKILL.md:125-151`). | High-value harness reuse: implement F1 loop as deterministic Beads/Backlog state machine; use agents only for item execution. |
| `src/superclaude/skills/task-builder/SKILL.md` | 2,190 | Orchestrates scope discovery, parallel researchers, QA gates, builder, structural and qualitative validation (`src/superclaude/skills/task-builder/SKILL.md:143-162`); writes task artifacts under `.dev/tasks/to-do/` (`src/superclaude/skills/task-builder/SKILL.md:108-140`). | Reuse as Backlog.md/Beads task-generation pipeline. Convert directory/artifact conventions into job workspace schema. |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | 1,491 | Deterministic roadmap-to-tasklist generator with no discretionary choices (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:12-17`, `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:20-28`); emits `tasklist-index.md` + `phase-N-tasklist.md` compatible with `superclaude sprint run` (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:91-123`). | Port as deterministic compiler from roadmap to Backlog.md/Beads tasks, but preserve truthfulness/no-browsing constraints when prompt input is the only source. |
| `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` | 529 | Skill-only inference layer invoked by `sc:roadmap` (`src/superclaude/skills/sc-roadmap-protocol/SKILL.md:19-29`); includes a Wave-to-CLI crosswalk and marks CLI gates as canonical for CLI parity (`src/superclaude/skills/sc-roadmap-protocol/SKILL.md:107-147`). | Reuse selectively. Prefer deterministic CLI gates as runtime authority; use skill text as orchestration guidance and compatibility documentation. |

### Rigorflow agents and role prompts

| Agent definition | Lines | Current role | Port implication |
|---|---:|---|---|
| `src/superclaude/agents/rf-team-lead.md` | 483 | Orchestrates `rf-task-researcher`, `rf-task-builder`, and `rf-task-executor` (`src/superclaude/agents/rf-team-lead.md:36-48`); defines message vocabulary and task prefixes (`src/superclaude/agents/rf-team-lead.md:79-103`); does scope discovery with Glob/Grep/codebase-retrieval before spawning researchers (`src/superclaude/agents/rf-team-lead.md:139-160`). | Reuse as coordinator prompt or replace with deterministic workflow engine. TeamCreate/SendMessage concepts need Mastra-native queues/events. |
| `src/superclaude/agents/rf-task-researcher.md` | 541 | Researches codebase and reports `RESEARCH_READY`, `RESEARCH_PARTIAL`, or `BLOCKED` (`src/superclaude/agents/rf-task-researcher.md:30-57`); requires structured findings: files, exports, patterns, templates, issues (`src/superclaude/agents/rf-task-researcher.md:123-150`). | Reuse nearly directly as a research-agent role. Adapt tool names from Claude Code Glob/Grep/Read to Mastra/Beads tool bindings. |
| `src/superclaude/agents/rf-task-builder.md` | 586 | Receives BUILD_REQUEST, uses researcher context, reads MDTM template first, then builds task (`src/superclaude/agents/rf-task-builder.md:40-58`, `src/superclaude/agents/rf-task-builder.md:59-85`, `src/superclaude/agents/rf-task-builder.md:88-145`). | Reuse as task compiler prompt, but update template paths from `.claude/templates/...` to canonical `src/superclaude/templates/...` or installed resource resolver. |
| `src/superclaude/agents/rf-qa.md` | 552 | Zero-tolerance verification agent with partitioning (`src/superclaude/agents/rf-qa.md:35-40`, `src/superclaude/agents/rf-qa.md:52-84`); research gate verifies evidence density, doc cross-validation tags, gaps, integration points, incremental writing (`src/superclaude/agents/rf-qa.md:125-166`). | Reuse as adversarial validation role. Port must implement partition merge and synthetic-dnsp contracts as structured data, not only markdown text. |
| `src/superclaude/agents/rf-qa-qualitative.md` | 1,139 | Complements structural QA with product/engineering sense-making (`src/superclaude/agents/rf-qa-qualitative.md:35-40`); supports partitioning and Tavily-first external lookup (`src/superclaude/agents/rf-qa-qualitative.md:53-83`, `src/superclaude/agents/rf-qa-qualitative.md:104-129`). | Reuse as qualitative review role after deterministic validation. External lookup provenance must be preserved in workflow logs. |

### Key Takeaways

- The Rigorflow corpus already encodes a reusable harness: task builder, MDTM executor, research/QA subagents, phase gates, partitioning, artifact directories, and status messages.
- [UNVERIFIED external — pending Phase 4 web research] Mastra/Backlog.md/Beads feasibility appears plausible if the port treats these prompts as policy/specs and moves loop control, dependencies, retries, and artifact state into deterministic workflow code; target-stack capability assumptions still require current external docs validation.
- Highest-risk direct reuse is any instruction that assumes Claude Code-specific tools (`Skill`, `Task`, `TeamCreate`, `SendMessage`, `TodoWrite`) or `.claude/` dev-copy paths.

## Section 4 — Core Rules, Templates, Hooks, and MCP Adaptation Boundaries

### Core instruction corpus inventory

| Core file | Lines | Purpose / evidence | Adaptation boundary |
|---|---:|---|---|
| `src/superclaude/core/CLAUDE.md` | 150 | Defines project structure, dev commands, source-of-truth sync, MCP servers, personas, and freshness discipline (`src/superclaude/core/CLAUDE.md:14-29`, `src/superclaude/core/CLAUDE.md:32-48`, `src/superclaude/core/CLAUDE.md:50-75`, `src/superclaude/core/CLAUDE.md:104-150`). | Reuse as top-level system/project instructions. Replace Claude Code-specific command references with CLI/agent-runtime equivalents where Mastra cannot enforce them directly. |
| `src/superclaude/core/COMMANDS.md` | 188 | Describes command pipeline: input parsing, context resolution, wave eligibility, execution strategy, and quality gates (`src/superclaude/core/COMMANDS.md:5-24`); includes `/sc:task` compliance flags and classification flow (`src/superclaude/core/COMMANDS.md:86-149`). | Use as command registry metadata and routing policy. Some command lists are generic docs; validate against actual `src/superclaude/commands/*.md` before generating runtime routes. |
| `src/superclaude/core/ORCHESTRATOR.md` | 389 | Defines detection engine, complexity/domain/operation matrices, resource zones, and wave routing (`src/superclaude/core/ORCHESTRATOR.md:5-33`, `src/superclaude/core/ORCHESTRATOR.md:42-94`, `src/superclaude/core/ORCHESTRATOR.md:95-130`). | Reuse as scoring heuristics. Mastra/Beads should implement complexity/domain scores as deterministic fields, not rely on prose-only routing. |
| `src/superclaude/core/MCP.md` | 304 | Server-selection algorithm (`src/superclaude/core/MCP.md:5-15`), Auggie integration (`src/superclaude/core/MCP.md:166-199`), and circuit breakers / task-tier dependencies (`src/superclaude/core/MCP.md:269-304`). | Use as MCP routing policy. Runtime must provide server registry, availability checks, fallback logging, and strict-tier blocking. |
| `src/superclaude/core/RULES.md` | 260 | Defines conflict hierarchy (`src/superclaude/core/RULES.md:5-17`), agent orchestration (`src/superclaude/core/RULES.md:18-50`), workflow/parallelism rules (`src/superclaude/core/RULES.md:51-68`), and verification-before-recommendation (`src/superclaude/core/RULES.md:69-82`). | Reuse as global policy, but split enforceable rules from advisory rules. Hookable rules should become workflow guards. |

### MDTM and document templates

| Template path | Lines | Evidence / purpose | Port implication |
|---|---:|---|---|
| `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md` | 996 | Generic MDTM task frontmatter (`src/superclaude/templates/workflow/01_mdtm_template_generic_task.md:1-44`) and task-builder-only Part 1 instructions; requires complete granular breakdown (`src/superclaude/templates/workflow/01_mdtm_template_generic_task.md:87-112`) and self-contained checklist items (`src/superclaude/templates/workflow/01_mdtm_template_generic_task.md:127-159`). | Reuse directly for Backlog.md/Beads task materialization, but map frontmatter fields into Backlog/Beads issue schema where possible. |
| `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` | 1,204 | Complex template extends generic with discovery/testing/review/conditional/aggregation use cases (`src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:60-64`); repeats granular/self-contained constraints (`src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:91-116`, `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:130-197`). | Use for multi-phase Beads task graphs and Backlog.md epics. Preserve Section L/M semantics after reading later sections in full during implementation. |
| `src/superclaude/templates/documents/*` | 7 files, 3,308 total lines | Inventory includes `GFxAI_Master_Documentation_Template.md`, `operational_guide_template.md`, `readme_template.md`, `release-spec-template.md`, `supplemental_doc_template.md`, `technical_reference_template.md`, and checklist. | Reusable as artifact templates for Mastra document-generation workflows; no runtime coupling observed in this investigation beyond task-builder/document skills needing template access. |

### Hook and policy migration inventory

| Hook asset | Lines | Current behavior evidence | Port/adaptation boundary |
|---|---:|---|---|
| `src/superclaude/hooks/hooks.json` | 95 | Registers `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `SubagentStart`, and `SubagentStop` hooks (`src/superclaude/hooks/hooks.json:1-95`). | Direct Claude Code hooks are not portable as-is. Reimplement as Mastra middleware / workflow guards around prompt submission, tool calls, and agent lifecycle. |
| `src/superclaude/hooks/scripts/freshness-user-prompt.sh` | 266 | Emits `<session-context>` with timestamp, turn, git dirty state, changed paths, resumed flag, and Auggie-first warnings (`src/superclaude/hooks/scripts/freshness-user-prompt.sh:20-30`, `src/superclaude/hooks/scripts/freshness-user-prompt.sh:66-80`, `src/superclaude/hooks/scripts/freshness-user-prompt.sh:127-192`, `src/superclaude/hooks/scripts/freshness-user-prompt.sh:200-264`). | Reuse behavior, not shell implementation. Mastra should create per-turn metadata events and persist them in workflow state. |
| `src/superclaude/hooks/scripts/freshness-pre-edit.sh` | 140 | Blocks edits without a recent Read, reads older than 30 minutes, or external changes after read (`src/superclaude/hooks/scripts/freshness-pre-edit.sh:63-106`, `src/superclaude/hooks/scripts/freshness-pre-edit.sh:121-138`). | High-value safety gate. Port as file-state guard around write operations with explicit read-token/mtime validation. |
| `src/superclaude/hooks/scripts/reject-workspace-writes.sh` | 64 | Rejects `.claude/skills/*-workspace/**` writes and repo-root `prd-*` writes, redirecting to `.dev/eval-workspaces/...` (`src/superclaude/hooks/scripts/reject-workspace-writes.sh:25-37`, `src/superclaude/hooks/scripts/reject-workspace-writes.sh:39-62`). | Port as artifact-location policy; important for keeping eval workspaces separate from distributable packages. |
| `src/superclaude/hooks/README.md` | 19 | Says hooks are copies from `plugins/superclaude/hooks/` and both locations must stay in sync (`src/superclaude/hooks/README.md:9-19`). | [CODE-VERIFIED] `plugins/superclaude/hooks/` exists and contains matching hook file names in this repo. Verify content sync before changing hooks; this research did not byte-compare files. |

### MCP configuration inventory

| MCP config / doc | Evidence | Runtime implication |
|---|---|---|
| `src/superclaude/mcp/configs/tavily.json` | Uses `npx -y mcp-remote https://mcp.tavily.com/mcp/?tavilyApiKey=${TAVILY_API_KEY}` with env `TAVILY_API_KEY` (`src/superclaude/mcp/configs/tavily.json:1-12`). | Port needs secret injection and remote MCP client support; preserve Tavily-first provenance rules from agents. |
| `src/superclaude/mcp/configs/auggie.json` | Uses `auggie --mcp --mcp-auto-workspace` (`src/superclaude/mcp/configs/auggie.json:1-9`). | Requires local Auggie binary/session. For Mastra, either wrap as MCP server or replace with equivalent semantic retrieval. |
| `src/superclaude/mcp/configs/serena.json` | Uses `uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant` (`src/superclaude/mcp/configs/serena.json:1-13`). | Port must support uvx process launch or preconfigured server; strict-tier task policy may block without Serena per `src/superclaude/core/MCP.md:288-295`. |
| `src/superclaude/mcp/configs/sequential.json` | Uses `npx -y @modelcontextprotocol/server-sequential-thinking` (`src/superclaude/mcp/configs/sequential.json:1-9`). | Port can install/launch as MCP dependency; also may replace with native planner if MCP unavailable for non-strict tiers. |
| `src/superclaude/core/MCP.md` | Circuit breaker table lists server fallbacks and strict task behavior (`src/superclaude/core/MCP.md:269-304`). | Convert to runtime health checks, fallback routes, and audit log entries. |

### Key Takeaways

- Hooks and MCP configs are behaviorally reusable but runtime-specific. The port should not shell out blindly; it should implement equivalent event hooks, guards, and server lifecycle abstractions.
- MDTM templates are reusable with minimal transformation, but existing agent references to `.claude/templates/...` should resolve through a source-of-truth-aware template loader.
- [CODE-VERIFIED] Hook README's `plugins/superclaude/hooks/` path exists in this repository; content sync was not fully validated and remains a gap.

## Section 6 — Port Feasibility Mapping for Mastra + Backlog.md + Beads

### External solution research

| System | External finding | Source | Fit for this corpus |
|---|---|---|---|
| Mastra | [UNVERIFIED external — pending Phase 4 web research] Tavily results describe Mastra as an open-source TypeScript framework for agents, workflows, RAG, memory, evals, telemetry, and MCP support; this is an external target-stack claim, not a current SuperClaude code fact. | https://www.generative.inc/mastra-ai-the-complete-guide-to-the-typescript-agent-framework-2026; https://mastra.ai/blog/changelog-2026-02-04 | [UNVERIFIED external — pending Phase 4 web research] Potential fit for replacing Claude Code-specific `Skill`/`Task` invocations with typed agents + workflows, especially for DAGs, tool access, memory, evals, and MCP. |
| Backlog.md | [UNVERIFIED external — pending Phase 4 web research] Tavily result for `MrLesk/Backlog.md` describes a Markdown/Git-native project board, local `backlog/` or `.backlog/`, zero-config CLI, and MCP integration for AI coding assistants; this is an external target-stack claim, not a current SuperClaude code fact. | https://github.com/MrLesk/Backlog.md | [UNVERIFIED external — pending Phase 4 web research] Potential fit for human-visible task/roadmap artifacts. Existing MDTM markdown may map to Backlog.md tasks/docs/decisions with frontmatter translation after schema verification. |
| Beads / `br` | [UNVERIFIED external — pending Phase 4 web research] Tavily results describe Beads as local-first, Git-friendly issue tracking for AI agents, with local SQLite in `.beads/` and JSONL export for Git synchronization; `br` is described externally as a Rust port using SQLite + JSONL. These are external target-stack claims, not current SuperClaude code facts. | https://betterstack.com/community/guides/ai/beads-issue-tracker-ai-agents; https://github.com/Dicklesworthstone/beads_rust | [UNVERIFIED external — pending Phase 4 web research] Potential fit for dependency-aware machine task state. Existing Rigorflow task dependencies and phase gates may become issue graph nodes with status/dependency edges after schema verification. |

**WEB SEARCH PROVENANCE:** provider=tavily.

### Recommended reuse architecture

The mappings below are target-stack hypotheses derived from the SuperClaude code inventory plus unverified external research above. Treat Mastra/Backlog.md/Beads capability assumptions as [UNVERIFIED external — pending Phase 4 web research], not as current SuperClaude code facts, until official docs/repos are extracted and checked.

| Existing SuperClaude surface | Mastra mapping | Backlog.md mapping | Beads mapping | Notes |
|---|---|---|---|---|
| `src/superclaude/commands/*.md` | Command router manifests / workflow entrypoints. | Optional docs for available commands. | Issue templates for command runs. | Front doors should validate flags and dispatch; do not embed execution loop. |
| `src/superclaude/skills/*/SKILL.md` | Agent/workflow instruction packs; LLM-assisted steps. | Skill docs / runbooks. | For repeatable workflows, each phase/step becomes issue nodes. | Preserve `allowed-tools`, `mcp-servers`, `personas`, and `argument-hint` frontmatter as metadata. |
| `src/superclaude/agents/*.md` | Mastra agent definitions/prompts. | Team role docs. | Worker-role labels and assignment hints. | Claude Code-only tool names require an adapter layer. |
| `src/superclaude/templates/workflow/*.md` | Task-generation templates and validation schemas. | Markdown task files / checklist bodies. | Issue descriptions, acceptance criteria, dependencies. | MDTM frontmatter should be normalized into Backlog/Beads fields. |
| `src/superclaude/hooks/*` | Middleware/guards around prompt/tool lifecycle. | N/A except policy docs. | Guard failure records / blocker issues. | Freshness-pre-edit and workspace-write rules should be hard runtime guards. |
| `src/superclaude/mcp/configs/*.json` | MCP server launch config for Mastra tools. | MCP integration docs if Backlog server is used. | May coexist with Beads CLI/MCP integration. | Need secret/env injection and health/circuit breaker abstraction. |

### Portification pattern already exists in-repo

| Asset | Evidence | Reuse implication |
|---|---|---|
| `/sc:cli-portify` command | Validates a workflow argument, output dir, name collision, then invokes `sc:cli-portify-protocol` (`src/superclaude/commands/cli-portify.md:20-35`, `src/superclaude/commands/cli-portify.md:45-91`). | This command is directly relevant to Mastra/Beads porting: it already frames workflow conversion from command+skill+agent markdown to deterministic pipelines. |
| `sc-cli-portify-protocol` | Purpose is converting inference workflows into programmatic CLI pipelines with deterministic control flow, gates, resume/retry, monitoring, budget ledger, and consistent behavior (`src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:12-28`). | Use the same decomposition method for Mastra workflow generation: component inventory, step graph, agent handoff map, gates, data flow. |
| Pipeline specification ref | Defines `Step` graph, gate modes, parallel groups, dependency rules, config/result models, and resume logic (`src/superclaude/skills/sc-cli-portify-protocol/refs/pipeline-spec.md:15-68`, `src/superclaude/skills/sc-cli-portify-protocol/refs/pipeline-spec.md:69-128`). | Provides concrete patterns for mapping Rigorflow phases to Beads dependencies and Mastra workflow steps. |

### Integration implications

| Boundary | Current assumption | Required adaptation |
|---|---|---|
| Tool invocation | Instructions assume Claude Code tools: `Skill`, `Task`, `Glob`, `Grep`, `TodoWrite`, `TeamCreate`, `SendMessage`. | Define a tool adapter contract. Mastra should expose equivalent tools or map operations to filesystem, MCP, process, and agent-run APIs. |
| Agent communication | Rigorflow agents use `RESEARCH_READY`, `TASK_READY`, `BLOCKED`, shared task lists, and sometimes team messaging (`src/superclaude/agents/rf-team-lead.md:79-103`). | Convert messages to structured workflow events and Beads/Backlog status updates. |
| State persistence | MDTM task files and artifacts are source-of-truth for progress (`src/superclaude/skills/task/SKILL.md:18-28`, `src/superclaude/skills/task/SKILL.md:282-299`). | Store workflow state in Beads/Backlog plus artifact files. Keep markdown artifacts for auditability. |
| Quality gates | Rigorflow relies on rf-qa/rf-qa-qualitative and per-phase gates (`src/superclaude/skills/task/SKILL.md:192-263`). | Model gates as explicit workflow steps with structured PASS/FAIL/fix-cycle output. Agent reports remain attached artifacts. |
| Source-of-truth | Core project instructions say `src/superclaude/` first (`src/superclaude/core/CLAUDE.md:45-48`), while some package READMEs say edit `plugins/superclaude/...` first (`src/superclaude/commands/README.md:13-23`, `src/superclaude/agents/README.md:11-21`, `src/superclaude/hooks/README.md:9-19`). | Resolve before port. Treat source-of-truth as a policy variable; current user/project instructions and core CLAUDE.md favor `src/superclaude/` for this branch, but plugin READMEs may reflect v5 transition. |

### Key Takeaways

- [UNVERIFIED external — pending Phase 4 web research] Feasibility appears high for harness reuse if Mastra owns deterministic orchestration and Beads/Backlog owns task-state persistence; this remains a target-stack hypothesis until current Mastra/Backlog.md/Beads docs are directly validated.
- Existing `sc-cli-portify-protocol` is the best internal pattern for the port: inventory → step graph → gates → executor/workflow model → reviewed spec.
- Do not directly translate Claude Code hooks/tools one-for-one; translate their contracts into runtime middleware and structured event/state schemas.

## Section 8 — Inventory Summary and Migration Boundaries

### Asset inventory totals

| Asset group | Count / size | Notes |
|---|---:|---|
| Command markdown files | 42 files under `src/superclaude/commands/` | Thin slash-command front doors with frontmatter and activation sections. |
| Agent markdown files | 39 files under `src/superclaude/agents/` | Includes Rigorflow roles, audit roles, architect/QA/scribe personas, and research roles. |
| Skill packages | 24 `SKILL.md` files under `src/superclaude/skills/` | 31,820 total lines across skill `SKILL.md`, refs, rules, and templates included in the initial inventory. |
| Core instruction files | 12 markdown files under `src/superclaude/core/` | Central policy corpus: commands, flags, MCP, modes, orchestrator, personas, principles, rules. |
| Workflow templates | 8 files under `src/superclaude/templates/workflow/` | Includes MDTM templates 01/02 and project/release/PRD templates. |
| Document templates | 7 files under `src/superclaude/templates/documents/` | Reusable documentation output templates. |
| Hook assets | `hooks.json` + 9 scripts + README/example | Event-driven policy layer for session context, freshness, subagent lifecycle, and write-location guardrails. |
| MCP assets | 11 MCP docs + 11 JSON configs | Tool/server configuration and reference docs for Context7, Sequential, Tavily, Serena, Auggie, Playwright, Magic, Mindbase, MorphLLM, Airis. |

### Instruction-corpus adaptation boundaries

| Boundary | Reusable as-is? | Required change |
|---|---|---|
| Markdown prompt content | Mostly yes | Replace absolute assumptions about Claude Code-specific tool names with an adapter vocabulary, or annotate each tool requirement with a runtime binding. |
| Frontmatter metadata | Yes | Parse into structured registry: name, description, allowed tools, MCP servers, personas, argument hints, category, complexity. |
| Slash-command invocation surface | Partially | Preserve `/sc:*` as UX aliases if desired, but dispatch to Mastra workflows or CLI subcommands rather than Claude Code `Skill` invocations. |
| MDTM file format | Yes | Map to Backlog.md Markdown and/or Beads issue fields while preserving original artifact files for evidence and resumption. |
| Rigorflow phase gates | Yes | Make QA gates first-class state transitions with retry/fix-cycle counters, not hidden prompt text. |
| Hooks | Behavior only | Rebuild as runtime middleware, file guards, prompt-enrichment hooks, and write-location policies. |
| MCP configs | Mostly | Secret/env handling, process supervision, health checks, and fallback/circuit breaker logic need runtime-specific implementation. |

### Gaps and Questions

1. **Source-of-truth conflict needs owner decision.** [CODE-CONTRADICTED] `src/superclaude/core/CLAUDE.md:45-48` says edit `src/superclaude/` first; `src/superclaude/commands/README.md:13-23`, `src/superclaude/agents/README.md:11-21`, and `src/superclaude/hooks/README.md:9-19` say these assets are copies from `plugins/superclaude/...` and should be edited there first. Both path families exist, but current project/user instructions favor `src/superclaude/` as source of truth. A port needs one authoritative resolver.
2. **Need content sync verification for plugin mirrors.** [UNVERIFIED] I verified `plugins/superclaude/hooks/`, `plugins/superclaude/commands/`, and `plugins/superclaude/agents/` exist, but did not byte-compare mirrors against `src/superclaude/...`.
3. **Mastra runtime APIs need direct docs validation before implementation.** External Tavily results establish broad Mastra fit, but exact current TypeScript APIs for agents/workflows/tools/MCP should be verified from official Mastra docs during design.
4. **Backlog.md and Beads schema details need direct extraction before field mapping.** External results establish fit, but exact CLI commands, file naming, and issue fields should be pulled from the current repos/docs before writing adapters.
5. **Some skill references point at `.claude/templates/...`.** [CODE-VERIFIED] `src/superclaude/agents/rf-task-builder.md:59-85` and `src/superclaude/agents/rf-task-builder.md:106-113` reference `.claude/templates/workflow/...`; dev-copy template files exist in this repo, but port code should resolve canonical `src/superclaude/templates/...` first.
6. **`/sc:forensic` referenced by TFEP was not in the requested path inventory.** [UNVERIFIED] `src/superclaude/skills/sc-task-protocol/SKILL.md:181-261` invokes `/sc:forensic`, but this investigation did not find or validate a corresponding command/skill in the requested file list. Treat as a dependency gap until searched explicitly.

### Stale Documentation Found

- **[STALE DOC] `src/superclaude/commands/README.md` available-command list is incomplete.** It lists only five files (`agent.md`, `index-repo.md`, `recommend.md`, `research.md`, `sc.md`) at `src/superclaude/commands/README.md:5-11`, but the current directory contains 42 command markdown files. The sync/source note at `src/superclaude/commands/README.md:13-23` may also be transitional because core instructions say `src/superclaude/` first.
- **[STALE DOC] `src/superclaude/agents/README.md` available-agent list is incomplete.** It lists only `deep-research.md`, `repo-index.md`, and `self-review.md` at `src/superclaude/agents/README.md:5-10`, but the current directory contains 39 agent markdown files including Rigorflow roles. The plugin-copy note at `src/superclaude/agents/README.md:11-21` conflicts with current source-of-truth instructions.
- **[POTENTIALLY STALE / TRANSITIONAL DOC] `src/superclaude/hooks/README.md` says edit `plugins/superclaude/hooks/` first.** [CODE-VERIFIED] That directory exists, but this conflicts with `src/superclaude/core/CLAUDE.md:45-48` for current SoT discipline. Mark as transitional until repo owner clarifies v5 plugin-source migration.

## Summary

The reusable corpus is substantial; [UNVERIFIED external — pending Phase 4 web research] suitability for a Mastra + Backlog.md + Beads orchestration port remains a target-stack hypothesis, contingent on separating **instruction reuse** from **runtime control** and validating current target-stack APIs/schemas. Commands should become front-door manifests; skills should become workflow/prompt packs; agents should become role definitions; MDTM templates should become task/issue schemas; hooks should become middleware/guards; MCP configs should become managed tool-server dependencies. The strongest in-repo pattern for this migration is `sc-cli-portify-protocol`, which already decomposes inference workflows into component inventories, step graphs, parallel groups, gates, and deterministic executor patterns. The major blockers are source-of-truth ambiguity between `src/superclaude/` and `plugins/superclaude/`, Claude Code-specific tool assumptions, and the need to translate markdown-only gates into structured Mastra/Beads/Backlog state transitions.
