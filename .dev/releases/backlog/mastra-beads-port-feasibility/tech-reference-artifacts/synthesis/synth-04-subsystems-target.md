# Synthesis 04 — Section 5 Subsystems 5.4–5.8

> **Scope:** Section 5 Subsystem Reference, subsystems 5.4–5.8, for the *proposed* Mastra + Backlog.md + Beads hybrid adapter-first orchestration architecture.
> **Target template section:** §5.4–§5.8 (Subsystem Reference). Follows `technical_reference_template.md` v1.0.2 subsystem structure: Purpose → Key Files/Components → How It Works → Dependencies → Consumers → Conventions.
> **Demarcation contract (R2):** Every claim carries exactly one tag (the three canonical tags only). `[CODE-VERIFIED]` = existing Python at HEAD `9e864860`, real `path:line`. `[DESIGN — UNBUILT]` = proposed hybrid target, feasibility/research evidence only. `[EXTERNAL-VERIFIED]` = external substrate, cited URL. A "layer none of the three components supplies" is still tagged `[DESIGN — UNBUILT]`, with the **NOT PROVIDED by any of Mastra / Backlog.md / Beads — must be built net-new** meaning carried in prose, not in a separate tag.
> **Reading rule:** 5.4 is the only *built* subsystem in this group (existing instruction IP). 5.5, 5.6, 5.8 are **design**, not built — read them as target architecture. 5.7 is **external** — every fact is a third-party capability, not a SuperClaude fact.

**Status: Complete**

---

### 5.4 Reusable Harness Corpus (Skills / Agents / Commands / Core / Templates / Hooks / MCP)

**Purpose:** The harness corpus is the body of **instruction IP** — slash commands, agents, skill packages, core framework files, MDTM/document templates, hooks, and MCP configs — that encodes SuperClaude's orchestration discipline as natural-language protocol rather than as runtime code. In a Mastra+Backlog.md+Beads port this corpus is the *most portable and most reusable* asset: it is runtime-agnostic prose that any host capable of invoking Claude (or another model) can drive. `[CODE-VERIFIED]`

**Key Files / Components** (counts confirmed at HEAD `9e864860` per `spot-04-harness.md`; raw `*.md` directory counts include each directory README):

| Asset class | Count (HEAD `9e864860`) | Canonical location | Role in a port |
|---|---|---|---|
| Slash commands | **42** `*.md` (41 command defs + 1 README) | `src/superclaude/commands/` | Thin front-door manifests: parse flags, validate inputs, invoke skills; no embedded execution loops. `[CODE-VERIFIED]` (`commands/task.md:156-162`, `roadmap.md:82-92`) |
| Agents | **39** `*.md` (38 agent defs + 1 README) | `src/superclaude/agents/` | Role-prompt corpus (rf-team-lead, rf-task-researcher, rf-qa, rf-qa-qualitative, etc.). `[CODE-VERIFIED]` (`agents/rf-team-lead.md:36-48`) |
| Skill packages | **24** (each a dir with exactly one `SKILL.md` + refs/rules/templates/scripts) | `src/superclaude/skills/` | Main reusable instruction body (sc-task, task, task-builder, sc-tasklist, sc-cli-portify, …). `[CODE-VERIFIED]` (`spot-04-harness.md` (b); `skills/task/SKILL.md:83-105`) |
| Core instruction files | **12** `*.md` (+ `__init__.py`) | `src/superclaude/core/` | CLAUDE.md, COMMANDS.md, ORCHESTRATOR.md, MCP.md, RULES.md, FLAGS.md, MODES.md, PERSONAS.md, PRINCIPLES.md, RESEARCH_CONFIG.md, BUSINESS_*. `[CODE-VERIFIED]` (`core/MCP.md:269-304`, `RULES.md:5-82`) |
| Workflow templates | 8 | `src/superclaude/templates/workflow/` | MDTM generic (996 lines) + complex (1,204 lines) task templates with granular/self-contained constraints. `[CODE-VERIFIED]` (`01_mdtm_template_generic_task.md:1-159`) |
| Document templates | 7 | `src/superclaude/templates/documents/` | PRD, TDD, technical_reference, etc. — this document's own template lives here. `[CODE-VERIFIED]` |
| Hooks | `hooks.json` (2,110 B) + 9 scripts | `src/superclaude/hooks/` | Registers SessionStart/UserPromptSubmit/PreToolUse/PostToolUse/SubagentStart/SubagentStop; freshness-pre-edit, reject-workspace-writes, session-context injection. `[CODE-VERIFIED]` (`hooks/hooks.json:1-95`) |
| MCP assets | 11 MCP docs + 11 JSON configs | `src/superclaude/mcp/` | tavily/auggie/serena/sequential launch configs + circuit-breaker/fallback table. `[CODE-VERIFIED]` (`mcp/configs/*.json`, `core/MCP.md:269-304`) |

**How It Works:**

The corpus is layered. Slash commands are **thin manifests** that parse flags and delegate to skills — they do not embed the execution loop (`commands/task.md:156-162`, `tasklist.md:70-84`, `roadmap.md:82-92`, `adversarial.md:143-149`). `[CODE-VERIFIED]` Skill packages carry the actual behavioral protocol: e.g. the generic MDTM `task` skill runs an F1 loop (read first unchecked item → execute exactly → mark complete → repeat), explicitly prohibits delegating the loop, and supports parallel agent spawning for independent items (`skills/task/SKILL.md:83-105`, `110-123`, `371-373`). `[CODE-VERIFIED]` `task-builder` (2,190 lines) orchestrates scope discovery → parallel researchers → QA gates → builder → structural+qualitative validation, writing to `.dev/tasks/to-do/` (`skills/task-builder/SKILL.md:108-162`). `[CODE-VERIFIED]` Agents are role prompts addressed by an orchestration vocabulary (rf-team-lead dispatches rf-task-researcher/builder/executor via message vocabulary + task prefixes; `agents/rf-team-lead.md:79-103`). `[CODE-VERIFIED]` Core files (ORCHESTRATOR.md detection/complexity/domain matrices, MCP.md server selection + circuit breakers, RULES.md verification-before-recommendation) are the global instruction substrate the skills reference (`core/ORCHESTRATOR.md:5-130`, `MCP.md:5-304`, `RULES.md:5-82`). `[CODE-VERIFIED]`

A crucial portability property: this corpus assumes **Claude Code tool semantics** (Skill / Task / Glob / Grep / TodoWrite / TeamCreate / SendMessage). Any non-Claude-Code host must supply an adapter vocabulary that maps these tool invocations onto the new runtime (`agents/rf-team-lead.md:79-103`). `[CODE-VERIFIED]` An in-repo precedent for converting inference workflows into deterministic CLI pipelines already exists — `/sc:cli-portify` + `sc-cli-portify-protocol` (component inventory → step graph → gates → executor/workflow spec) — and is the natural reuse seam for porting (`commands/cli-portify.md:20-91`, `sc-cli-portify-protocol/SKILL.md:12-28`). `[CODE-VERIFIED]`

**Dependencies:**

| Depends On | Type | Description |
|---|---|---|
| Claude Code tool runtime | Tool vocabulary | Skill/Task/Glob/Grep/TodoWrite/TeamCreate/SendMessage are assumed; a port must adapt them. `[CODE-VERIFIED]` (`agents/rf-team-lead.md:79-103`) |
| `src/superclaude/` canonical tree | Source-of-truth | Per `core/CLAUDE.md:17-29,45-48`, edit `src/` first then `make sync-dev`; `.claude/` are synced dev copies. `[CODE-VERIFIED]` |
| MCP servers (tavily/auggie/serena/sequential) | External tools | Skills reference MCP per `core/MCP.md` circuit-breaker table; strict-tier blocking on unavailability. `[CODE-VERIFIED]` (`core/MCP.md:269-304`) |

**Consumers:**

| Used By | How |
|---|---|
| Pipeline runtimes (sprint / roadmap / tasklist) | Sprint Path B prompt invokes `/sc:task ... --compliance strict --strategy systematic`; roadmap/tasklist steps deliver skill-defined prompts. `[CODE-VERIFIED]` (`sprint/process.py:123-216`) |
| A future Mastra step runner | Would deliver the same skill/agent prompts through a Mastra step instead of `ClaudeProcess`. `[DESIGN — UNBUILT]` (see 5.6) |

**Conventions & Patterns:**

- **`src/superclaude/` is canonical; `plugins/superclaude/` is a divergent mirror — do NOT scrape the mirror as primary.** At HEAD `9e864860`, `plugins/superclaude/` is git-tracked but materially out of sync: 30 commands / 20 agents / **1** skill / 6 core files vs `src/`'s 42 / 39 / 24 / 12. `diff -qr` reports many `Only in src` commands (adversarial, auggie-review, cleanup-audit, cli-portify, release-split, review-translation, roadmap) and many differing shared files. The plugin-tree READMEs ("edit `plugins/superclaude/` first") are a stale v5-transition artifact, not operative policy. `[CODE-VERIFIED]` (`spot-04-harness.md` (c); `core/CLAUDE.md:45-48` vs `commands/README.md:13-23`)
- **READMEs are stale and must not be used for counts.** `commands/README.md` lists 5 command files (dir has 42); `agents/README.md` lists 3 (dir has 39). `[CODE-VERIFIED]` (`commands/README.md:5-11`, `agents/README.md:5-10`)
- **Slash commands stay thin; behavior lives in skills.** Never push an execution loop into a command manifest. `[CODE-VERIFIED]`
- **Dependency gap to flag, not invent:** `/sc:forensic` is invoked by the TFEP escalation in `sc-task-protocol/SKILL.md:181-261` but no such command/skill exists in the inventory — a real unverified dependency a port must resolve. `[CODE-VERIFIED]`

---

### 5.5 Target Data Model & Ownership

> **CRITICAL:** This subsystem is **`[DESIGN — UNBUILT]`**. No source file in the repository implements any Backlog.md / Beads / Mastra integration today. The current-code contracts cited below as `[CODE-VERIFIED]` are the *existing* models the design must preserve; the ownership split, join semantics, and adapter targets are *proposed architecture*, not built behavior.

**Purpose:** Define a single, drift-resistant ownership model for the hybrid stack so that prose, dependency graph, and run/trace state each have exactly one source of truth, joined by stable IDs. The design exists to prevent the central failure mode of a three-store stack: two systems both believing they own task status or dependencies, silently diverging until execution order changes. `[DESIGN — UNBUILT]`

**Key Components — three model groups** (current representation is `[CODE-VERIFIED]`; the target owner is `[DESIGN — UNBUILT]`):

| Model Group | Current representation (HEAD `9e864860`) | Proposed target owner | Tag |
|---|---|---|---|
| **A. Prose / task / doc / decision concepts** | MDTM markdown w/ YAML frontmatter (id/title/status/type/priority/dates/deps/tags) + ordered checklist phases; handoff artifacts in task subdirs | **Backlog.md** (prose owner) | current `[CODE-VERIFIED]` (`02_mdtm_template_complex_task.md:1-44`, `394-430`, `718-731`); target `[DESIGN — UNBUILT]` |
| **B. State / status / telemetry / quality signals** | StepStatus / TaskStatus / GateOutcome / SprintOutcome enums; `MonitorState` high-volume telemetry; `TurnLedger` budget; execution-log.jsonl / phase-*-result.md / per-task output files | **Mastra** (run/trace/gate-execution owner) | current `[CODE-VERIFIED]` (`pipeline/models.py:40-67`, `sprint/models.py:39-124`, `622-690`, `692-777`); target `[DESIGN — UNBUILT]` |
| **C. Tasklist-generation & sprint-parser contract** | phase-file name aliases, Execution Mode (claude/python/skip), `### T<PP>.<TT> -- Title` headings, `**Dependencies:**`/`**Command:**` extraction, release-dir resolution | **Beads** (dependency graph) + Backlog.md (visible dep text) | current `[CODE-VERIFIED]` (`sprint/config.py:15-26`, `67-119`, `374-492`, `236-272`); target `[DESIGN — UNBUILT]` |

**How It Works (proposed):**

The design splits **work-of-record** along two axes: **Backlog.md owns prose** (human-readable task body, acceptance criteria, checklist instructions, decisions) while **Beads owns the graph + gates** (normalized dependencies, ready-queue, external gates). **Mastra owns run/trace state** (retries, step status, model/provider calls, traces) — but only after a validation phase proves its durability/replay/observability; until then, current Python result files remain the source of truth. `[DESIGN — UNBUILT]`

The **join key** across all three stores is the set of **stable IDs** that already exist verbatim in current file formats and parsers: `TASK-*`, `T<PP>.<TT>`, `D-####` (deliverable), `D-CP…` (checkpoint deliverable), `R-###` (roadmap item). These are `[CODE-VERIFIED]` as current IDs (`sc-tasklist-protocol/SKILL.md:161-164`, `441-487`; `sprint/config.py:374-377`); their use as a cross-system reconciliation key is `[DESIGN — UNBUILT]`. The ownership matrix below is the proposed boundary:

| Data / artifact class | Current owner | Proposed target owner | Mirror owners | Sync direction |
|---|---|---|---|---|
| Human task body / AC / decisions | `.dev/tasks` markdown | Backlog.md | Mastra trace links, Beads metadata | Backlog.md → adapters |
| Machine dependency graph (`depends_on`, `Txx.yy` edges) | frontmatter + `**Dependencies:**` text | Beads | Backlog.md retains visible text; Mastra reads for scheduling | Backlog.md/tasklist → Beads |
| Workflow run state / retries / step status / traces | Python dataclasses / process outputs | Mastra | Backlog.md summaries; Beads status updates | Mastra → Backlog/Beads summaries |
| Logs / checkpoint reports / validation reports | files under release/task workspace | Backlog.md docs or artifact files w/ Mastra trace refs | Beads links only | files → Backlog docs; Beads stores pointers |
| Gate definitions / enforcement tiers | Python models + skill protocols | Mastra (execution) + Backlog.md (policy docs) | Beads fail/remediation issues | Backlog policy → Mastra config |
| Stable IDs / traceability | markdown / tasklist generator | shared cross-system IDs; Backlog.md assigns/preserves canonical | Mastra + Beads store as metadata | Backlog/tasklist → all |
| Multi-tenant auth / RBAC / cost | **absent** beyond `TurnLedger` budget | unresolved — governance service (see 5.8) | — | TBD |

*(All target-owner cells `[DESIGN — UNBUILT]`; "current owner" and "absent" cells `[CODE-VERIFIED]` per `pipeline/models.py`, `sprint/models.py` read ranges.)*

**Dependencies:**

| Depends On | Type | Description |
|---|---|---|
| Stable-ID contract | Current code fact | IDs must already exist and be parseable — they do (`sprint/config.py:374-377`). `[CODE-VERIFIED]` |
| Sprint parser compatibility | Current code constraint | Any adapter writing tasklists must satisfy `discover_phases()` / `parse_tasklist_file()` (see 5.6 Contract 1). `[CODE-VERIFIED]` (`sprint/config.py:399-492`) |
| Backlog.md schema | External | Target prose fields constrained by Backlog.md `Task` schema (see 5.7). `[EXTERNAL-VERIFIED]` |

**Consumers:**

| Used By | How |
|---|---|
| Adapter / seam-replacement layer (5.6) | Adapters read/write each store per the ownership matrix. `[DESIGN — UNBUILT]` |
| Governance plane (5.8) | Adds tenant/actor/audit identity that the matrix's bottom row leaves unresolved — **NOT PROVIDED by any of Mastra / Backlog.md / Beads; must be built net-new.** `[DESIGN — UNBUILT]` |

**Conventions & Patterns (ownership rules to preserve):**

- **One prose owner, one graph owner, one run owner.** Backlog.md (prose) / Beads (graph) / Mastra (run). Mirrors link or summarize; they never fork the canonical copy. `[DESIGN — UNBUILT]`
- **Stable IDs are non-negotiable.** Every adapter preserves current IDs verbatim and never regenerates them on import/export. `[DESIGN — UNBUILT]`
- **Checkpoint reports remain artifacts.** A checkpoint is both a task node and a report body; never conflate the two. `[DESIGN — UNBUILT]`
- **Tenant/actor/audit identity is ABSENT today.** `PipelineConfig`/`SprintConfig`/`TaskResult`/`PhaseResult`/`MonitorState`/`TurnLedger` carry model/permission/budget but **no** tenant or actor field — governance dimensions must be added, not assumed. `[CODE-VERIFIED]` (absence; `sprint/models.py:692-777`)
- **Known current-code conflict to carry forward, not silently fix:** `sc-tasklist-protocol/SKILL.md:343-391` specifies numbered `### T<PP>.<NN> -- Checkpoint:` tasks, but the extracted `phase-template.md:101-125` still documents sibling `### Checkpoint:` sections, and sprint `build_prompt()` (`sprint/process.py:187-195`) still instructs scanning for the sibling form. Adapters must emit the **numbered** form for sprint compatibility. `[CODE-VERIFIED]` (doc-contradicted)

---

### 5.6 Adapter / Seam-Replacement Layer

> **CRITICAL:** This subsystem is **`[DESIGN — UNBUILT]`**. No source file implements Mastra/Backlog.md/Beads integration. The reusable orchestration *patterns* cited as `[CODE-VERIFIED]` are existing in-repo precedents (cli_portify, prd, cleanup_audit, eval, audit) that the adapter design draws on; the four adapter contracts and the Mastra-step/CLI-shell-out hybrid are *proposed*.

**Purpose:** Define the thin translation layer that lets the existing Python orchestration and instruction corpus drive — and be driven by — the external substrate without a big-bang rewrite. The adapter layer is where the "hybrid, adapter-first" strategy lives: it wraps the one narrow runtime seam (`ClaudeProcess` / `StepRunner`) and adds four data adapters that move task/graph/run state between stores. `[DESIGN — UNBUILT]`

**Key Components — the four adapter contracts:** `[DESIGN — UNBUILT]`

| # | Adapter contract | Direction | Validation contract |
|---|---|---|---|
| **1** | Tasklist bundle → Backlog.md import | tasklist files → Backlog prose | Import must export back such that `discover_phases()` + `parse_tasklist_file()` succeed and counts match `count_tasks_in_file()`. |
| **2** | Backlog.md / tasklist → Beads graph sync | prose/IDs → Beads issues+edges | Graph export must reproduce a dependency list identical to parser-extracted `TaskEntry.dependencies` unless a human-approved patch exists. |
| **3** | Backlog.md / Beads → Mastra workflow plan | task+graph → Mastra plan | Plan generation must be deterministic and produce a dry-run plan (task order, gates, expected artifacts, provider commands) before execution. |
| **4** | Mastra run results → Backlog.md + Beads reconciliation | run state → prose+graph updates | Reconciliation must be idempotent (re-applying the same result is a no-op). |

*(All four `[DESIGN — UNBUILT]`, sketched in `07-target-data-model-and-ownership.md` Contracts 1-4; each maps onto current models — Contract 4 maps `StepStatus.PASS`/`TaskStatus.FAIL`/`GateOutcome.DEFERRED` which are `[CODE-VERIFIED]` at `pipeline/models.py:40-67`, `sprint/models.py:39-124`.)*

**How It Works (proposed):**

The **central replatforming act** is replacing the runtime seam. Today `ClaudeProcess` constructs `claude --print --verbose <perm> --no-session-persistence --tools default --max-turns N --output-format <fmt>`, delivers the prompt over **stdin** (not argv, to avoid Linux `MAX_ARG_STRLEN`), maps timeout→exit 124, and tears down the process group SIGTERM→SIGKILL (`pipeline/process.py:73-95`, `97-112`, `159-214`). `[CODE-VERIFIED]` The executor owns retry/gates/ordering while the runner owns subprocess+timeout, joined by the `StepRunner` protocol `__call__(step, config, cancel_check) -> StepResult` (`pipeline/executor.py:41-60`). `[CODE-VERIFIED]` In the target design **a Mastra step becomes the `StepRunner`**: `execute_pipeline()` (which already accepts an injected `run_step`, proven by roadmap/validate/tasklist consumers at `roadmap/executor.py:26`, `tasklist/executor.py:259-263`) would receive a Mastra-backed runner instead of `ClaudeProcess`. `[CODE-VERIFIED]` (seam exists) / `[DESIGN — UNBUILT]` (Mastra runner).

The **CLI shell-out hybrid** is the lower-risk first move: rather than reimplement gate/convergence/diagnostic logic (which is pure runtime-agnostic Python — `gates.py` imports only `re`/`Path`/`GateCriteria` at `pipeline/gates.py:1-17`), the adapter calls the existing `superclaude` CLI as a subprocess from a Mastra step, preserving runner-authored truth and gate semantics while gaining Mastra's durable orchestration shell. `[CODE-VERIFIED]` (Python portability) / `[DESIGN — UNBUILT]` (shell-out wrapper).

In-repo precedents the adapter design reuses (all `[CODE-VERIFIED]`): **cli_portify** emits a `return-contract.yaml` on every path (outcome/completed_steps/remaining_steps/suggested_resume_budget/resume_command) — a ready-made bridge record for Backlog/Beads (`cli_portify/executor.py:283-372`); its deterministic output classification (timeout→TIMEOUT, exit0+marker+artifact→PASS, artifact-no-marker→PASS_NO_SIGNAL) is the model for Contract 4 (`cli_portify/executor.py:224-257`). **prd** demonstrates tier-sized parallel fan-out + QA→fix→re-QA loops (`prd/executor.py:862-958`, `963-1047`). **eval** demonstrates HOME-dir isolation with a three-check containment guard and a retry-once policy (`eval/isolation.py:224-260`, `eval/retry.py:41-165`) — directly relevant to safe subprocess parity. **audit** demonstrates content-hash caching, atomic checkpoint writes, and calibrated validation that explicitly states self-agreement is *not* ground-truth correctness (`audit/validation.py:42-151`). The verified migration method: single typed graph as SoT → attach artifact/gate contracts → preflight before side effects → run with isolation+supervision → persist → QA/convergence loops → calibrated validation → retire duplicated resume/review matrices. `[CODE-VERIFIED]` (synthesis)

**Dependencies:**

| Depends On | Type | Description |
|---|---|---|
| `StepRunner` / `execute_pipeline` seam | Current code | The injection point a Mastra runner plugs into. `[CODE-VERIFIED]` (`pipeline/executor.py:41-60`, `63-188`) |
| Target data model (5.5) | Design | Adapters move state per the ownership matrix. `[DESIGN — UNBUILT]` |
| Mastra `createStep` / Workspace | External | Step + subprocess substrate the runner targets (see 5.7). `[EXTERNAL-VERIFIED]` |
| Backlog.md CLI/MCP, Beads `bd --json` | External | Mutation interfaces for Contracts 1-4. `[EXTERNAL-VERIFIED]` |

**Consumers:**

| Used By | How |
|---|---|
| Harness corpus (5.4) | Skills/agents are delivered through the new step runner unchanged. `[DESIGN — UNBUILT]` |
| Sprint/roadmap/tasklist runtimes | Their injected `run_step` is swapped for the adapter runner. `[DESIGN — UNBUILT]` |

**Conventions & Patterns:**

- **Contract-first, gated, resumable, source-verified.** The cli_portify evolution is the cautionary precedent: early code-gen/spec-drift failed; the contract-first/gated pattern became the safe one — favoring strangler/hybrid over big-bang. `[CODE-VERIFIED]` (synthesis)
- **Preserve runner-authored truth.** Current orchestration is artifact/gate-centric: Python owns sequencing/retry/halt/state/gates, Claude fills structured content. A Mastra port must re-host that division, not just re-host prompts. `[CODE-VERIFIED]` (`pipeline/gates.py`, `executor.py`)
- **Start read-only.** First adapters import existing `.dev/tasks` and tasklist bundles into target metadata *without changing current files*; add round-trip parser tests before any ownership transfer. `[DESIGN — UNBUILT]`
- **Reconciliation must be idempotent** (Contract 4) so retries/replays do not double-apply status or duplicate remediation issues. `[DESIGN — UNBUILT]`
- **DRIFT hazards to carry forward, not silently fix:** cli_portify `resume.py` legacy matrix uses conceptual step names that contradict the live `STEP_REGISTRY` (`resume.py:45-95` vs `executor.py:105-183`); cleanup_audit docstring claims ThreadPoolExecutor parallelism but executes sequentially (`cleanup_audit/executor.py:11-13`). A port must retire these duplicated matrices, not replicate them. `[CODE-VERIFIED]` (contradicted)

---

### 5.7 External Component Substrate (Mastra / Backlog.md / Beads / MCP)

> **Note:** Every fact in this subsystem is **`[EXTERNAL-VERIFIED]`** — a third-party capability sourced via Tavily/Context7 web research (web-01..web-04), **not** a SuperClaude code fact. Inline URLs are the provenance. These describe what the substrate *can* do today; whether SuperClaude *uses* them is `[DESIGN — UNBUILT]` (5.5/5.6).

**Purpose:** Document the current, externally-verified capabilities and risks of the three substrate components plus MCP, so the design (5.5/5.6/5.8) rests on what these tools actually provide rather than on the seed brief's assumptions (several of which are corrected below). `[EXTERNAL-VERIFIED]`

**Key Components / Capabilities:**

**Mastra** (runtime / workflow / observability) `[EXTERNAL-VERIFIED]`

| Capability | Detail | Source URL |
|---|---|---|
| Durable workflows | `suspend()`/`resume()`/`resumeStream()`; snapshots persist across deploys/restarts; resume from a specific step ID; runners = built-in, Inngest, Temporal (Temporal **experimental/not prod-ready**) | https://mastra.ai/docs/workflows/suspend-and-resume ; https://mastra.ai/docs/deployment/workflow-runners |
| Typed step pipelines | `createWorkflow()`/`createStep()` w/ input/outputSchema; steps call functions/APIs/agents/tools/workflows; workflows deterministic vs agents probabilistic | https://mastra.ai/docs/workflows/overview |
| Workspace subprocess | `WorkspaceSandbox` (`executeCommand`/start/stop/destroy, timeouts, stdout/stderr/wait, `maxRetainedBytes`), added `@mastra/core@1.1.0` — **NOT proven parity** with Claude Code hook/permission model | https://mastra.ai/reference/workspace/sandbox |
| Storage | libSQL/Turso, PostgreSQL, MongoDB, Redis/Upstash, DynamoDB, MSSQL, ClickHouse, Cloudflare; `MastraCompositeStore` routes domains; in-memory resets | https://mastra.ai/docs/memory/storage ; https://mastra.ai/reference/storage/composite |
| Observability / Studio | auto-instruments agent runs/LLM gens/tool calls/workflow steps (tokens, model params); Studio visualizes graphs/traces/MCP servers; 1.0 schema entityId/entityType/entityName | https://mastra.ai/docs/observability/tracing/overview ; https://mastra.ai/docs/studio/overview |
| Auth / RBAC / EE (**key risk**) | Auth optional (Studio/API public without it); providers Simple/JWT/Auth0/Better/Clerk/Firebase/Okta/Supabase/WorkOS; **RBAC/FGA tied to Enterprise Edition** (`@mastra/core/auth/ee`, StaticRBACProvider, WorkOS FGA); dual license Apache-2.0 core + Mastra EE for `ee/` dirs | https://mastra.ai/docs/server/auth ; https://mastra.ai/pricing |
| MCP | `MCPClient` (stdio/HTTP/SSE) + `MCPServer` (expose agents/tools/workflows over HTTP); `requireToolApproval` HITL; FGA enforcement for MCP tool execution | https://mastra.ai/docs/mcp/overview |
| Deployment | `mastra dev/build/start`, `server deploy`; Hono-based server, Express/Hono/Fastify/Koa adapters; agents/workflows → REST + OpenAPI; Platform Organizations = multi-tenant containers | https://mastra.ai/docs/server/mastra-server ; https://mastra.ai/docs/mastra-platform/overview |

> **Important:** Mastra's risk is **parity/governance, not capability**: Claude Code hook parity is NOT established; workflow rerun/replay/idempotency needs hands-on validation; Temporal is experimental; Backlog/Beads are not native concepts. `[EXTERNAL-VERIFIED]` (https://mastra.ai/docs, synthesis)

**Backlog.md** (markdown-native work-of-record) `[EXTERNAL-VERIFIED]`

| Capability | Detail | Source URL |
|---|---|---|
| Core | markdown task store (`backlog/` dir), CLI + TUI board + browser UI + fuzzy search + docs + decisions + MCP; MIT; **v1.45.2**; TypeScript/Bun | https://github.com/MrLesk/Backlog.md ; .../package.json |
| Task schema | rich first-class fields (id/title/status/assignee/reporter/dates/labels/milestone/dependencies/references/documentation/modifiedFiles/description/implementationPlan/Notes/finalSummary/AC/DoD/parent-subtasks/priority/branch/ordinal) | https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/types/index.ts |
| MCP constraint (**key**) | MCP task schemas use `additionalProperties:false` — **arbitrary SuperClaude metadata cannot be added as MCP fields**; must use supported fields / body sections / docs or extend | https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/tools/tasks/schemas.ts |
| MCP MVP | current MCP is a minimal stdio surface (`task_*`/`milestone_*`/`definition_of_done_*`/`document_*`); decision tools are CLI-only, not MCP; contradicts older "75+ tools" claims | https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/README.md |
| Git optional | `backlog init --no-git` = filesystem-only; `autoCommit` default false; remoteOperations/bypassGitHooks/filesystemOnly config | https://raw.githubusercontent.com/MrLesk/Backlog.md/main/ADVANCED-CONFIG.md |
| Maturity limits | local-file/git-centric, **not** a centralized multi-user transactional PM backend (`proper-lockfile`; one-task-per-agent discipline); no built-in sprint/roadmap pipeline; Beads integration immature (FR #588); browser state-loss bug #578 | https://github.com/MrLesk/Backlog.md/issues/588 ; .../issues/578 |

**Beads** (Dolt-backed dependency graph) `[EXTERNAL-VERIFIED]`

| Capability | Detail | Source URL |
|---|---|---|
| Core | `gastownhall/beads` "distributed graph issue tracker for AI agents, powered by Dolt"; npm `@beads/bd`, PyPI `beads-mcp`; high churn (~24.3k stars, 227 open issues) | https://github.com/gastownhall/beads |
| CLI | `bd ready` (unblocked), `bd create`, `bd update --claim` (atomic assignee+in_progress), `bd dep add`, `bd show`, `bd prime` (context+memories), `bd remember`; always `--json` | https://github.com/gastownhall/beads ; SETUP.md |
| Dependency / gate semantics | blocking (blocks/parent-child/conditional-blocks/waits-for) + non-blocking annotations; cycles rejected at write; **gates** bridge to external state (`gh:pr`/`gh:run`/`timer`/`bead`/`human`) | https://github.com/gastownhall/beads/blob/main/docs/DEPENDENCIES.md |
| Storage (**corrects seed brief**) | **Dolt-first** (version-controlled SQL, cell-level merge, branching); `.beads/issues.jsonl` is **export/interchange only**, NOT canonical sync — corrects the "SQLite + JSONL" framing | https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md ; .../DOLT.md |
| Deployment modes | embedded (default, in-process Dolt, single-writer, solo) vs server (`dolt sql-server`, concurrent writers, `bd init --server`) — **server REQUIRED for multi-agent** | https://github.com/gastownhall/beads/blob/main/docs/DOLT.md |
| JSON contract | `--json` stable (schema v1); `BD_JSON_ENVELOPE=1` opts into uniform envelope (planned v2.0 default); legacy lists=raw arrays | https://github.com/gastownhall/beads/blob/main/docs/JSON_SCHEMA.md |
| Version caution (**pin**) | v1.0.5 pre-release/gated ("do not upgrade"; migration 0043 can break multi-machine sync, #4259); v1.0.4 server data-clobber regression — pin + gate versions | https://github.com/gastownhall/beads/releases ; .../issues/3870 |

**How It Works (relationship to the design):** The substrate provides three complementary stores that map onto the 5.5 ownership split — Mastra for run/trace (durable workflows + observability), Backlog.md for prose (markdown task/doc/decision records), Beads for graph (typed dependencies + ready-queue + gates). That substrate-capability mapping is `[EXTERNAL-VERIFIED]` (web-01..web-03; https://mastra.ai/docs ; https://github.com/MrLesk/Backlog.md ; https://github.com/gastownhall/beads). The narrow current seam they would replace is `ClaudeProcess` at `pipeline/process.py:73-147` `[CODE-VERIFIED]`. Markdown tasklists are currently **ordered execution records, not active dependency graphs** — sprint parses deps but executes in document order at `sprint/config.py:379-384` `[CODE-VERIFIED]` — so adopting Beads graph semantics is a *behavioral change*, not a runtime swap.

**Dependencies:** Each component is independently deployable; Backlog.md↔Beads integration is **not mature** (FR #588, maintainer suggests narrow import/export sync first — https://github.com/MrLesk/Backlog.md/issues/588). `[EXTERNAL-VERIFIED]`

**Consumers:** The adapter layer (5.6) is the sole intended consumer; nothing in the current repo consumes any of these today. `[DESIGN — UNBUILT]`

**Conventions & Patterns:**

- **Pin and gate versions** for all three (Mastra `@core` 1.1.0+, Backlog.md 1.45.2 MVP, Beads 1.x churn); runtime-verify schemas because docs drift. `[EXTERNAL-VERIFIED]`
- **Mutate via CLI/MCP, not hand-edited files** for Backlog.md (keeps field types consistent) and Beads (`--json`, never read legacy JSONL directly). `[EXTERNAL-VERIFIED]`
- **Server mode is mandatory for any multi-agent writer** scenario in Beads; embedded is solo-only. `[EXTERNAL-VERIFIED]`
- **Production RBAC/SSO/FGA/audit/on-prem are Mastra Enterprise-licensed**, not Apache-2.0 core — a gating commercial decision for multi-tenant deployment. `[EXTERNAL-VERIFIED]`

---

### 5.8 Governance / Multi-Tenant Control Plane

> **CRITICAL:** This subsystem is **`[DESIGN — UNBUILT]`** and is specifically **NOT PROVIDED by any of Mastra / Backlog.md / Beads — it must be built net-new.** It is the net-new layer that **none of the three components supplies** and that the current SuperClaude code does not contain. It is not "unbuilt SuperClaude work" in the sense of a planned SuperClaude feature; it is a category of capability that must be sourced or built separately before any company-wide multi-tenant deployment. External governance facts carry `[EXTERNAL-VERIFIED]` with URLs; current-code absence carries `[CODE-VERIFIED]`.

**Purpose:** Establish that a Mastra+Backlog.md+Beads stack — even fully integrated — is **not** a complete multi-tenant platform, and enumerate the governance/control-plane layer (identity, tenant isolation, policy, tool catalog, audit, cost/budget attribution, approvals) that must sit above the substrate. The subsystem exists to prevent the dangerous assumption that MCP or any single component is a governance layer. This layer is **NOT PROVIDED by any of Mastra / Backlog.md / Beads — it must be built net-new.** `[DESIGN — UNBUILT]`

**Key Components — the missing layer** (**NOT PROVIDED by any of Mastra / Backlog.md / Beads — must be built net-new**): `[DESIGN — UNBUILT]`

| Control-plane capability | Why none of the 3 components supplies it | Source URL |
|---|---|---|
| Tenant registry + isolation | Mastra Organizations are containers, not full tenant governance; Backlog.md is repo-local; Beads is project-scoped | https://github.com/MrLesk/Backlog.md ; https://github.com/gastownhall/beads |
| Identity mapping (5 identities) | Multi-tenant agents need **separate** trigger / execution / authorization / tenant / attribution identities; access-control bugs surface silently when execution+tenant are conflated; config-driven RBAC, not inferred from user messages | https://www.scalekit.com/blog/access-control-multi-tenant-ai-agents |
| RBAC/ABAC policy store | Mastra production RBAC/FGA is Enterprise-licensed, not core | https://mastra.ai/pricing |
| Tool/skill catalog + change control | Enterprise MCP needs a curated approved catalog with versioned contracts, staging, consumer tracking, review-like-code, rollback | https://tray.ai/blog/mcp-security-governance-enterprise |
| Audit log (per-invocation) | record caller identity/session, tool name+version+schema, inputs, target, outcome, policy decision, approval, cost, correlation ID | https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1 |
| Cost / rate / budget attribution | FinOps: cost attribution is a governance-layer concern outside MCP; meter model tokens + tool calls by tenant/team/user/agent/workflow/task | https://www.finops.org/wg/model-context-protocol-mcp-ai-for-finops-use-case |
| Approval engine + env separation | progressive elevation via `WWW-Authenticate`, approval gates for higher-risk actions, environment separation/rollout controls | https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices |

**How It Works (why MCP is NOT the governance layer):**

The decisive point: **MCP is a narrow integration protocol — host/client/server tool-resource exchange — and explicitly does NOT define enterprise governance.** Authorization is *optional* in MCP; it focuses on context exchange and does not dictate who acts, when, or under what conditions (https://modelcontextprotocol.io/docs/concepts/architecture). `[EXTERNAL-VERIFIED]` (web-04 #1) Where MCP authorization *is* used for enterprise, it is OAuth 2.1-based (PRM, resource indicators, audience binding, token validation), and **token passthrough is explicitly forbidden** because it breaks accountability/audit and enables exfiltration — downstream services need separate tokens + attribution, not forwarded credentials (https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). `[EXTERNAL-VERIFIED]` (web-04 #2, #3) Official MCP guidance itself warns of multi-tenant/realm mix-ups, generic audiences, session-ID-as-auth, and broad scopes — confirming MCP needs an API-management/control-plane layer above it, analogous to early REST (https://tray.ai/blog/mcp-security-governance-enterprise ; https://www.speakeasy.com/resources/ai-control-plane). `[EXTERNAL-VERIFIED]` (web-04 #4, #7, #10)

Consequently the three components are an **orchestration/task substrate, not the complete platform**: Mastra is runtime/workflow/MCP/observability (NOT a full tenant-governance/policy/budget/approval/catalog/cost plane — https://mastra.ai/docs); Backlog.md and Beads are task/memory substrates with no cross-tenant IAM, enterprise audit, rate limiting, or cost attribution (https://github.com/MrLesk/Backlog.md ; https://github.com/gastownhall/beads). `[EXTERNAL-VERIFIED]` (web-04 #13, #14, #15) A Mastra+Backlog.md+Beads port therefore needs an **additional** governance/control-plane layer before company-wide multi-tenant deployment. `[EXTERNAL-VERIFIED]` (web-04 #11, synthesis)

**Dependencies:**

| Depends On | Type | Description |
|---|---|---|
| Target data model (5.5) | Design | Governance adds the tenant/actor/audit identity the ownership matrix leaves unresolved — **NOT PROVIDED by any of Mastra / Backlog.md / Beads; must be built net-new.** `[DESIGN — UNBUILT]` |
| Mastra observability | External (telemetry source) | Mastra traces can *feed* the governance plane (join traces with Backlog.md/Beads IDs) but do not *constitute* it. `[EXTERNAL-VERIFIED]` (web-04 #8) |

**Consumers:** All orchestration actions in a multi-tenant deployment would route policy/identity/audit/cost decisions through this layer — a layer **NOT PROVIDED by any of Mastra / Backlog.md / Beads; it must be built net-new.** `[DESIGN — UNBUILT]`

**Conventions & Patterns:**

- **MCP is not a governance platform.** Never delegate identity/policy/audit/cost to MCP alone. `[EXTERNAL-VERIFIED]` (web-04 #1, https://modelcontextprotocol.io/docs/concepts/architecture)
- **Five separate identities.** Keep trigger / execution / authorization / tenant / attribution distinct; never conflate execution and tenant. `[EXTERNAL-VERIFIED]` (https://www.scalekit.com/blog/access-control-multi-tenant-ai-agents)
- **No token passthrough; granular scopes only.** Map command/skill privileges to least-privilege tool-level scopes (no `superclaude:*` wildcards); use progressive elevation + approval for higher-risk actions. `[EXTERNAL-VERIFIED]` (https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)
- **Current-code GAP (the starting point):** `TurnLedger` is sprint-local budget only; tenant/actor/audit identity is **ABSENT** from the scoped models (`PipelineConfig`/`SprintConfig` have model/permission/budget but no tenant/actor). Governance dimensions must be added, not assumed present. `[CODE-VERIFIED]` (absence; `sprint/models.py:692-777`)
