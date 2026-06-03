# Synthesis 03: External Research Findings (Report Section 5)

**Status:** Complete
**Date:** 2026-06-02
**Scope:** Synthesis of fresh web research (web-01..04, 2026-06-02) reconciled against the older external enrichment seed (`research-deep.md`, Stack D deep research).

---

## 5.0 Reading Guide and Ground Rules

This section synthesizes EXTERNAL research only. It does not override the codebase findings elsewhere in this report.

**Authority order (per task rules):**

1. **Codebase is source of truth.** External research adds context and options; where external claims touch the actual SuperClaude/IronClaude code, the verified-code findings in Sections 1-4 govern. Discrepancies are noted explicitly here.
2. **Fresh web research (web-01..04, dated 2026-06-02) supersedes the older enrichment seed (`research-deep.md`)** wherever the two differ. The seed encoded several Stack D assumptions that the fresh research corrects or qualifies; those corrections are called out in dedicated "Seed Correction" callouts below.

**Reliability ratings** are the per-finding ratings carried from the source web agents (HIGH / MEDIUM-HIGH / MEDIUM), reflecting source authority (official docs/repo > vendor blog > third-party writeup) and corroboration.

**Relationship-to-codebase** is one of: **Supports** (external evidence reinforces a codebase need/seam), **Extends** (adds capability/option beyond current code), **Contradicts** (external reality conflicts with a codebase assumption or a prior seed claim), or **Neutral/Context**.

**Provenance:** All fresh findings used Tavily search/extract first (plus Context7 for Mastra docs); no WebSearch/WebFetch fallback fired. `provider=tavily`.

---

## 5.1 Mastra (Runtime / Workflow / ACP Seam)

Mastra is the candidate TypeScript runtime and workflow engine, and — critically — the candidate replacement for the SuperClaude `ClaudeProcess`/stream-json subprocess seam (via `@mastra/acp` `AcpAgent`).

### 5.1.1 Capability Findings

| # | Finding | Rating | Relationship | Source |
|---|---------|--------|--------------|--------|
| M1 | Durable workflows: `suspend()`/`resume()`/`resumeStream()` serialize a full snapshot (runId, per-step status, payloads, output) to configured storage; snapshots persist across deployments and restarts. Direct analog to MDTM checkpoints and recoverable reruns (`sprint rerun-tasks` ≈ resume-from-step). | HIGH | Supports | [suspend-and-resume](https://mastra.ai/docs/workflows/suspend-and-resume) ; Context7 `/mastra-ai/mastra` |
| M2 | Code-defined workflow graph: `createWorkflow()`/`createStep()` with `.then()`, `.branch()`, `.parallel()`, `.map()`, loops (`.dountil()`/`.dowhile()`/`.foreach()`), Zod-typed step IO, nested workflows. Covers sprint/roadmap/pipeline phase-graph control flow. | HIGH | Supports | [workflows/overview](https://mastra.ai/docs/workflows/overview) |
| M3 | `@mastra/acp` `AcpAgent` spawns an ACP coding-agent CLI as a subprocess subagent (streaming, runtime model selection, persistent sessions, sandboxed workspace). Example drives Claude Code via `npx -y @agentclientprotocol/claude-agent-acp`. **The decisive structural replacement for `ClaudeProcess` spawning `claude --print --verbose` with stream-json.** Requires `@mastra/core@1.34.0+`. | HIGH | Extends | [research-deep.md] (ACP intro blog, PR #16423); GitHub releases |
| M4 | Mastra Workspace / `WorkspaceSandbox`: persistent filesystem + `executeCommand(command, args?, options?)`, `start()/stop()/destroy()`, timeouts, status/resource reporting, bounded retention (`maxRetainedBytes`). Added `@mastra/core@1.1.0`. Candidate subprocess/command-execution layer. | HIGH | Extends | [workspace/overview](https://mastra.ai/docs/workspace/overview) ; [workspace/sandbox](https://mastra.ai/reference/workspace/sandbox) |
| M5 | Storage: libSQL/Turso, PostgreSQL, MongoDB, Redis/Upstash, DynamoDB, MSSQL, ClickHouse, Cloudflare; `MastraCompositeStore` routes memory/workflows/scores/observability to different backends. ClickHouse for prod observability, libSQL for local dev. | HIGH | Supports | [memory/storage](https://mastra.ai/docs/memory/storage) ; [storage/composite](https://mastra.ai/reference/storage/composite) |
| M6 | Observability: OpenTelemetry-native, auto-instruments agent runs/LLM gen/tool calls/workflow steps with token/cost attribution; exporters (Datadog, Langfuse, Arize, Braintrust, SigNoz, Mastra platform). Studio visualizes workflow graphs/traces, runs tools in isolation. 1.0 unified schema (`entityId`/`entityType`/`entityName`). | HIGH | Supports | [observability/tracing/overview](https://mastra.ai/docs/observability/tracing/overview) ; [studio/overview](https://mastra.ai/docs/studio/overview) |
| M7 | MCP: `MCPClient` (stdio/HTTP/SSE outbound) and `MCPServer` (expose agents/tools/workflows over HTTP). `requireToolApproval` for HITL approval of MCP tool execution; recent FGA enforcement for MCP tool execution. | HIGH | Supports | [mcp/overview](https://mastra.ai/docs/mcp/overview) |
| M8 | Deployment: `mastra dev`/`build`/`start`, `mastra server deploy` (Docker image + URL). Hono-based generated server; adapters for Express/Hono/Fastify/Koa; agents/workflows become REST endpoints with OpenAPI. Self-host Node/Bun, Vercel, Cloudflare, Render, K8s/EKS. Node ≥22.13.0. | HIGH | Extends | [server/mastra-server](https://mastra.ai/docs/server/mastra-server) ; [research-deep.md] |
| M9 | Durability extras: `DurableAgent` + resumable streams survive client disconnect and server crash via cached events + `observe(runId,{offset})`. Inngest integration adds durable step memoization, retries, and **per-tenant concurrency/backpressure** (3rd-party engine). | HIGH | Extends | [research-deep.md] (release ~2026-04-28) |

### 5.1.2 Licensing and Multi-Tenancy (Key Risk)

| # | Finding | Rating | Relationship | Source |
|---|---------|--------|--------------|--------|
| M10 | **Dual license.** Apache-2.0 governs the main framework (agents, workflows, storage adapters, Server, observability core). A separate **Mastra Enterprise Edition (EE) License** (`ee/LICENSE`, a bespoke commercial license — NOT Elastic 2.0 / BSL) governs everything under any `ee/` directory. EE "production" = any use beyond dev+testing on your own systems; requires a written commercial agreement; redistribution/sublicense/sell forbidden. | HIGH | Contradicts (seed framing) | [research-deep.md] (ee/LICENSE verified); Context7 `/mastra-ai/mastra` |
| M11 | **Production RBAC/SSO/FGA is EE-gated.** `server.auth` (who) is separate from `server.rbac` (what). SimpleAuth (API-key→{id,name,role}) works license-free. But `StaticRBACProvider`, `DEFAULT_ROLES` (owner/admin/member/viewer), WorkOS/Okta SSO, permission-based Studio UI, and Agent Builder multi-tenant workflows import from `@mastra/core/auth/ee` and **require a paid EE license in production**. | HIGH | Contradicts (Stack-D "feasible OSS multi-tenant" assumption) | [server/auth](https://mastra.ai/docs/server/auth) ; [studio/auth](https://mastra.ai/docs/studio/auth) ; [pricing](https://mastra.ai/pricing) |
| M12 | Without auth, Studio and API routes are public. Agent Builder without RBAC grants every authenticated user full access. Real per-tenant concurrency isolation / noisy-neighbor protection is NOT in Apache core — it comes from the Inngest engine integration. | HIGH | Contradicts (governance gap) | [server/auth](https://mastra.ai/docs/server/auth) ; [research-deep.md] |

> **SEED CORRECTION / CONFIRMATION (Mastra licensing).** Task rule 3 calls out: *"Mastra production RBAC/auth is Enterprise-licensed."* Both the fresh web research (web-01 finding 6) and the enrichment seed AGREE on this — it is the single biggest strategic gate for any company-wide multi-tenant SuperClaude port. The fresh research SHARPENS the seed by confirming via official docs that EE is a bespoke commercial license (not Elastic/BSL) and that production use of `ee/` requires a written agreement. **Net: a multi-tenant RBAC platform on Mastra is feasible but commercially gated; the OSS Apache path yields only SimpleAuth (flat API-key→role) + application-level storage scoping, with the RBAC/tenant layer DIY.**

### 5.1.3 Maturity Claims and Open Questions

| # | Finding | Rating | Note |
|---|---------|--------|------|
| M13 | 1.0.0 reached 2026-01-20; verified later core releases through 1.16.0 (2026-03-23); ACP floor `@mastra/core@1.34.0+`. ~300k weekly npm downloads, 22-24k GitHub stars, 300+ contributors. Production claims (Replit, PayPal, Sanity). | MEDIUM | Vendor claims; PRECISE current-latest core version UNVERIFIED beyond the `>=1.34.0` floor. |
| M14 | `@mastra/temporal` marked experimental/not-production-ready in at least one current deployment page; treat Temporal cautiously vs. Inngest. | MEDIUM | Runner choice affects production retry/durability semantics. |

**UNVERIFIED / needs hands-on validation (carried forward to Gaps):**

- Workflow restart/replay/partial-rerun/idempotency semantics (claimed analog to MDTM, not empirically proven against SuperClaude reruns).
- Whether `@mastra/acp` itself sits under Apache or an `ee/` path is UNVERIFIED.
- `max_turns` / permission-flag / model parity between `AcpAgent` (ACP contract) and the current `ClaudeProcess` stream-json knobs is UNVERIFIED.
- Cursor / Gemini CLI / Copilot driving via Mastra `AcpAgent` is plausible (they speak ACP) but NOT explicitly validated in Mastra's own docs.
- **Claude Code hook parity is NOT established.** Mastra Workspace command execution does NOT replicate SuperClaude/Claude Code hooks (UserPromptSubmit session-context injection, freshness-pre-edit, verify-sync), UV-only Python rule, git-safety, `.claude/` source-of-truth/staging discipline, or fork-PR-target enforcement. These would need re-implementation as Mastra processors/middleware or be dropped.

---

## 5.2 Backlog.md (Markdown Task-of-Record)

Backlog.md is the candidate human-readable, repo-local task/docs/decision work-of-record, mapped onto the MDTM tasklist-index format.

### 5.2.1 Capability Findings

| # | Finding | Rating | Relationship | Source |
|---|---------|--------|--------------|--------|
| B1 | Markdown-native tasks in a project-local `backlog/` folder (committed `.md` files w/ YAML frontmatter, `task-10 - Add core search.md`); CLI + TUI Kanban (`backlog board`) + web UI (`backlog browser`) + fuzzy search + docs + decisions + MCP, all over one source of truth. MIT license. v1.45.2 (released 2026-05-30), TypeScript/Bun, active (~5.7k stars, 185 releases). | HIGH | Supports | [github.com/MrLesk/Backlog.md](https://github.com/MrLesk/Backlog.md) |
| B2 | Rich first-class task schema maps onto MDTM phase items: `status`, `assignee`, `labels`, `priority`, acceptance criteria (per-criterion `--check-ac N`), `--plan`, `--notes`, `--final-summary`, `dependencies` (`--dep`, with circular-dependency guard), parent/subtasks, `ordinal`, `modifiedFiles`. Concurrency-hardened (BACK-404 task-ID locking). | HIGH | Supports | [src/types/index.ts](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/types/index.ts) ; [CLI-INSTRUCTIONS.md](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/CLI-INSTRUCTIONS.md) |
| B3 | Docs (`backlog doc create -p guides`) and decisions/ADR (`backlog decision create -s proposed`) are first-class at the CLI/data layer — candidate host for roadmap/adversarial `decision.add` obligations. Absolute paths / `..` traversal rejected. | HIGH | Supports | [CLI-INSTRUCTIONS.md](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/CLI-INSTRUCTIONS.md) |
| B4 | Git is optional: `backlog init --no-git` creates a filesystem-only project; config `remoteOperations`, `autoCommit` (default false), `filesystemOnly`. Supports both repo-native and no-git orchestration. | HIGH | Extends | [ADVANCED-CONFIG.md](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/ADVANCED-CONFIG.md) |
| B5 | Built-in MCP server (`backlog mcp start`, stdio); `backlog init` can auto-configure it. Agent workflow guidance (decompose → AC → one-task-per-session/PR → research/plan → implement/verify → rerun fresh) aligns with SuperClaude tasklist discipline. | HIGH | Supports | [github.com/MrLesk/Backlog.md](https://github.com/MrLesk/Backlog.md) ; [src/mcp/README.md](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/README.md) |

### 5.2.2 Limitations and Contradictions

| # | Finding | Rating | Relationship | Source |
|---|---------|--------|--------------|--------|
| B6 | **MCP is an MVP stdio surface**, smaller than older "75+ tools" claims. README: "minimal stdio MCP surface" routing through Core APIs. Current MCP task tools: `task_create/list/search/edit/view/archive/complete`; plus `milestone_*`, `definition_of_done_defaults_*`, `document_*`. | HIGH | Contradicts (older claims) | [src/mcp/README.md](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/README.md) ; [src/mcp/tools/tasks/index.ts](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/tools/tasks/index.ts) |
| B7 | **MCP task schemas reject unknown properties (`additionalProperties: false`).** SuperClaude-specific orchestration metadata CANNOT simply be added as arbitrary MCP fields — must use supported fields, body sections, docs, references, or extend Backlog.md. | HIGH | Contradicts (arbitrary-frontmatter assumption) | [src/mcp/tools/tasks/schemas.ts](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/tools/tasks/schemas.ts) |
| B8 | **CLI > MCP coverage.** Decisions are first-class in CLI but NOT clearly exposed in the current MCP MVP README — a CLI-vs-MCP coverage gap. Use CLI for decisions until MCP decision support is verified at runtime. | HIGH | Contradicts (seed "decisions via MCP" assumption) | [CLI-INSTRUCTIONS.md](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/CLI-INSTRUCTIONS.md) |
| B9 | No built-in sprint/roadmap pipeline equivalent; no dependency-GRAPH engine (intra-project `--dep` edges only, not a queryable graph DB); no execution/orchestration runtime. Backlog.md replaces the MDTM tasklist-index FORMAT, NOT the ~65K-LOC pipeline logic or the `ClaudeProcess` seam. | HIGH | Neutral/Context | web-02 finding 2/8; [research-deep.md] |
| B10 | Browser UI open state-loss bug #578: "UI state resets if files change while browser UI is running" — unsaved draft text cleared when an agent updates files concurrently (BACK-429 open). | HIGH | Neutral/Context | [issue #578](https://github.com/MrLesk/Backlog.md/issues/578) |
| B11 | Local-file/git-centric, NOT a centralized multi-user transactional PM backend. `proper-lockfile` dependency; single-writer-per-repo git model can contend under true concurrent multi-user write load. **NO native multi-tenancy / RBAC / auth / remote-HTTP transport in the official server — stdio + single-repo + single-trust-domain by design.** | MEDIUM-HIGH | Contradicts (multi-tenant expectation) | web-02 finding 12; [research-deep.md] |
| B12 | Beads ↔ Backlog.md integration is NOT mature. Open feature request #588; maintainer: *"This needs a narrower integration decision before tasking... start by choosing one workflow, such as import/export sync with Beads, rather than committing to a broad integration surface."* | HIGH | Contradicts (seed "shared repo metadata references" claim) | [issue #588](https://github.com/MrLesk/Backlog.md/issues/588) |

### 5.2.3 The BACK-407 Conflict (Seed vs. Fresh Research)

> **SEED CORRECTION (BACK-407 specifically UNVERIFIED).** Task rule 3 calls out: *"Backlog.md MCP is an MVP surface and BACK-407 specifically unverified (BACK-408 found)."* The two external sources DISAGREE:
>
> | Source | Claim about BACK-407 | Strength |
> |--------|----------------------|----------|
> | Enrichment seed (`research-deep.md`) | BACK-407 ("Align MCP server with latest spec") is **MERGED in v1.43.0 (2026-03-21)**, plus a companion chain BACK-406/403/408/434/436/465. Cites release notes + newreleases.io. | Asserted as verified. |
> | Fresh web-02 (2026-06-02) | BACK-407 **could NOT be confirmed**; search surfaced **BACK-408** (consolidate MCP workflow guide tools) instead. The MCP README presents only an **MVP** surface. Doc drift observed (`agent-nudge.md` resource selectors vs. README `backlog://docs/task-workflow`). | Marked `[UNVERIFIED]`. |
>
> **Resolution for this report:** Per task rule 2, the fresh research governs. Treat BACK-407's specific scope/merge status as **UNVERIFIED** and the Backlog.md MCP as an **MVP surface with active churn and doc drift**. Do NOT build the integration decision on an assumed "spec-aligned, BACK-407-complete" MCP. **Action:** verify the live MCP tool catalog with `backlog mcp start` + an `/mcp` probe (and check decision/milestone tool exposure) before committing any `decision.add` / metadata-mapping dependency. BACK-408 (workflow-guide consolidation) IS the corroborated item across both sources.

---

## 5.3 Beads (Dependency Graph / Agent Memory)

Beads is the candidate machine-facing dependency graph, ready-work scheduler, and cross-session agent memory.

### 5.3.1 Capability Findings

| # | Finding | Rating | Relationship | Source |
|---|---------|--------|--------------|--------|
| BD1 | Current repo `gastownhall/beads` (Steve Yegge's org). "Distributed graph issue tracker for AI agents, powered by Dolt." High activity (24.3k stars, 91 releases). Packages: npm `@beads/bd`, PyPI `beads-mcp`. | HIGH | Neutral/Context | [github.com/gastownhall/beads](https://github.com/gastownhall/beads) |
| BD2 | Agent-native CLI: `bd ready` (unblocked + priority-sorted work), `bd create -p 0`, `bd update <id> --claim` (atomic claim: assignee + in_progress), `bd dep add <child> <parent>`, `bd show <id>` (details + audit trail), `bd prime` (agent context + memories), `bd remember` (persistent project memory). Maps directly to SuperClaude orchestration primitives. | HIGH | Supports | [github.com/gastownhall/beads](https://github.com/gastownhall/beads) ; SETUP.md |
| BD3 | Dependency graph richer than simple blockers. Blocking (affect `bd ready`): `blocks`, `parent-child`, `conditional-blocks`, `waits-for`. Non-blocking: `related`, `tracks`, `discovered-from`, `caused-by`, `validates`, `supersedes`. `bd dep add` rejects cycles at write time. Maps to SuperClaude wave/planning dependencies. | HIGH | Supports | [DEPENDENCIES.md](https://github.com/gastownhall/beads/blob/main/docs/DEPENDENCIES.md) |
| BD4 | **Gates bridge Beads state to external code/CI state**: `gh:pr` (PR merged), `gh:run` (CI success), `timer`, `bead` (cross-rig issue closed), `human` (manual approval). `bd gate check`/`discover`. Directly maps to SuperClaude's "work done" vs "merged/validated" distinction — validation/PR-merge phases could be encoded as gates. | HIGH | Extends | [DEPENDENCIES.md](https://github.com/gastownhall/beads/blob/main/docs/DEPENDENCIES.md) |
| BD5 | `bd --json` is the stable integration contract (use `--json`, not `--format json`). Schema version `1`; `BD_JSON_ENVELOPE=1` opts into a uniform envelope (planned default v2.0). Legacy list commands emit raw arrays; `bd export --json` emits JSONL (not envelope-wrapped). Integrations need a dual parser (legacy + envelope). | HIGH | Supports | [JSON_SCHEMA.md](https://github.com/gastownhall/beads/blob/main/docs/JSON_SCHEMA.md) |
| BD6 | Hash-based collision-resistant IDs (`bd-a1b2`, dotted epics `bd-a3f8.1.1`) purpose-built for concurrent multi-agent/multi-branch writes. 5 priority levels P0-P4. Higher-level primitives: Formulas (workflow templates), Molecules (work graphs), Gates, GitHub Issues sync. | HIGH | Extends | [research-deep.md] (pkg.go.dev + README) |

### 5.3.2 Storage Backend — Seed Correction

> **SEED CORRECTION (Beads is Dolt-first, NOT SQLite/JSONL).** Task rule 3 calls out: *"Beads is Dolt-first (not SQLite/JSONL)."* This is the most consequential correction in this section.
>
> | Claim | Status |
> |-------|--------|
> | Seed-brief / Stack-D framing: "embedded SQLite or Dolt server-mode", "`.beads/` Dolt or SQLite + JSONL" | **CONTRADICTED** by current official docs. |
> | Current reality (web-03 + research-deep.md verified facts): **Beads uses Dolt ONLY** as of the 1.0 line. The classic SQLite+JSONL+git backend was REMOVED (early Feb 2026). "The local Dolt database is the source of truth for `bd list/show/ready` and every write command." | **VERIFIED** (official README, DOLT.md, SYNC_CONCEPTS.md). |
> | `.beads/issues.jsonl` role | **Export/interop/migration/backup ONLY** — NOT canonical cross-machine sync; does not capture Dolt branches/history/working-set. Tools reading old JSONL directly are **incompatible** with current versions. Use `bd backup` for restorable backups. |
> | Why the seed was wrong | Third-party writeups (Peter Warnock, Better Stack) still describe the older SQLite+JSONL architecture and are **stale**. A Rust fork (`beads_rust`) deliberately freezes the classic SQLite+JSONL architecture — confirming the divergence. |
>
> **Implication for the port:** Any integration must (1) drive `bd ... --json` rather than read `.beads/issues.jsonl`, (2) treat Dolt (embedded or server) as the store of record, and (3) use Dolt-native sync/backup (`bd dolt push/pull`, `bd bootstrap`, `bd backup`). Exclude JSONL-direct community tools unless updated for Dolt.

### 5.3.3 Concurrency, Modes, and Risk

| # | Finding | Rating | Relationship | Source |
|---|---------|--------|--------------|--------|
| BD7 | Two Dolt modes: **Embedded** (default, in-process, `.beads/embeddeddolt/`, **single-writer** with file lock — "database is locked" under contention, solo only) vs **Server** (external `dolt sql-server`, `.beads/dolt/`, multiple concurrent writers, `bd init --server`). History: v0.56.1 removed embedded → v0.63.0 reintroduced as default → v1.0.0 stable. | HIGH | Neutral/Context | [DOLT.md](https://github.com/gastownhall/beads/blob/main/docs/DOLT.md) |
| BD8 | **Server mode is REQUIRED for SuperClaude parallel/multi-agent orchestration**; embedded is insufficient for concurrent writers. Atomic claim `bd update <id> --claim --assignee <agent>`; sync via Dolt remotes under `refs/dolt/data`. Shared-server mode (`~/.beads/shared-server/`, port 3308) hosts multiple projects by prefix. | HIGH | Supports | [DOLT.md](https://github.com/gastownhall/beads/blob/main/docs/DOLT.md) ; SYNC_CONCEPTS.md |
| BD9 | Session attribution is actively changing (issues #3400/#3583: `--claim` could lose session info; acceptance criteria added `--session`/`CLAUDE_SESSION_ID`/`BEADS_SESSION_ID`). Multi-agent observability is in flux. | HIGH | Neutral/Context | [issues #3400/#3583](https://github.com/gastownhall/beads/issues/3400) |
| BD10 | **Version/release caution.** v1.0.5 shown as pre-release/gated with "do not upgrade" warning — migration `0043` can silently/unrecoverably break multi-machine `bd dolt` sync (issue #4259); v1.0.4 had a server-mode data-clobber regression (#3870). Operational instability on the Dolt-only line: orphaned `dolt sql-server` daemons, nil-pointer panics in `bd ready`/`bd list`, migration PK forks blocking `bd dolt pull` (#2573 "made beads unusable for me"). | MEDIUM-HIGH | Contradicts (production-ready assumption) | [releases](https://github.com/gastownhall/beads/releases) ; [issue #3870](https://github.com/gastownhall/beads/issues/3870) ; DoltHub blog 2026-05-29 |
| BD11 | **Production readiness:** usable but fast-moving with sharp edges. FAQ: core stable, dogfooded, safe for dev/internal WITH backup/sync hygiene; NOT recommended as sole record for mission-critical without tested backup/restore. **Mandatory: version-pin + an abstraction seam + `bd doctor`/backup/push-pull smoke tests in adoption gates.** | HIGH | Contradicts (drop-in assumption) | [FAQ.md](https://github.com/gastownhall/beads/blob/main/docs/FAQ.md) ; [issue #2938](https://github.com/gastownhall/beads/issues/2938) |
| BD12 | NO multi-tenancy / RBAC at the Beads layer. "Multi-writer" (Dolt server mode) is concurrency, not tenancy — one shared un-permissioned graph per Dolt DB. Tenant isolation must be imposed ABOVE Beads (separate Dolt DBs / issue-prefixes per tenant + gating in the orchestration layer). First-party MCP server maturity UNVERIFIED — the `--json` CLI is the most stable agent interface. | HIGH | Contradicts (governance) | web-03 + [research-deep.md] |

> **Version discrepancy note (for runtime verification):** web-03 reports the current line at **v1.0.5** (with the "do not upgrade" gating); the older enrichment seed (fetched same day) recorded **v1.0.4** as latest (2026-05-09). The seed also flags a separate "Beads v0.60.0" Gas Town product-line version track. **Confirm the exact current release and its safety gating against the live releases page at use time before pinning.**

---

## 5.4 MCP and Multi-Tenant Governance

This area answers a structural question: can a Mastra + Backlog.md + Beads stack serve as a company-wide, multi-tenant SuperClaude replacement on its own?

### 5.4.1 MCP Is a Protocol, Not a Governance Platform

| # | Finding | Rating | Relationship | Source |
|---|---------|--------|--------------|--------|
| G1 | MCP is a deliberately narrow host/client/server context-exchange protocol. It explicitly does NOT dictate how AI apps use LLMs, manage context, or govern access. | HIGH | Contradicts (seed "MCP as governance" assumption) | [modelcontextprotocol.io/architecture](https://modelcontextprotocol.io/docs/concepts/architecture) |
| G2 | MCP authorization is OPTIONAL but strongly recommended for enterprise / audit / consent / rate-limiting / per-user tracking. Remote-server auth is OAuth 2.1-based (Protected Resource Metadata, resource indicators, audience binding, token validation). | HIGH | Extends (requirement) | [authorization tutorial](https://modelcontextprotocol.io/docs/tutorials/security/authorization) ; [spec/authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) |
| G3 | **Token passthrough explicitly forbidden** — breaks accountability/audit, bypasses rate limits, enables exfiltration. Servers must validate tokens were issued for them. Downstream services need separate tokens + attribution metadata, not forwarded credentials. | HIGH | Extends (requirement) | [security best practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) |
| G4 | Official MCP guidance flags multi-tenant/realm mix-ups, generic audience/resource indicators, session-ID-as-auth misuse, broad wildcard scopes. Guidance: pin to single issuer/tenant unless explicitly multi-tenant; minimize scopes (no `files:*`/`db:*`/`admin:*`); incremental elevation via `WWW-Authenticate`. | HIGH | Extends (requirement) | [authorization tutorial](https://modelcontextprotocol.io/docs/tutorials/security/authorization) ; [security best practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) |

### 5.4.2 The Missing Governance Layer

| # | Finding | Rating | Relationship | Source |
|---|---------|--------|--------------|--------|
| G5 | Enterprise governance is MCP's missing layer: identity, policy, visibility, audit, tool catalog, change control. Analogous to early REST needing API-management. Record caller identity/session, tool name/version/schema, inputs, target, outcome, policy decision, approvals. | MEDIUM | Extends | [tray.ai](https://tray.ai/blog/mcp-security-governance-enterprise) ; [scalekit](https://www.scalekit.com/blog/enterprise-mcp-how-identity-sso-and-scoped-auth-actually-work) |
| G6 | **Multi-tenant agents need FIVE separate identities: trigger, execution, authorization, tenant, attribution.** Access-control bugs surface silently when execution and tenant identities are conflated. Config-driven RBAC; no inference from user messages. | MEDIUM (very high relevance) | Supports (SuperClaude ownership/attribution semantics) | [scalekit multi-tenant](https://www.scalekit.com/blog/access-control-multi-tenant-ai-agents) |
| G7 | An AI control plane is broader than an LLM gateway (model routing/rate limits) or an MCP gateway (tool-calling paths) — it unifies connection, identity, policy, observability across all agents/systems. | MEDIUM | Extends | [speakeasy](https://www.speakeasy.com/resources/ai-control-plane) |
| G8 | Cost attribution / FinOps is NOT native to MCP — requires host/gateway/control-plane metering (model tokens + tool calls + retries + workflow runs by tenant/team/user/agent/task). | MEDIUM-HIGH | Extends | [finops.org](https://www.finops.org/wg/model-context-protocol-mcp-ai-for-finops-use-case) |
| G9 | CSA/minimum maturity: all MCP connections authenticated; remote uses OAuth 2.1 + PKCE; maintain server inventory (name/version/location/owner); least-privilege service accounts; basic audit logging of all tool invocations. Curated approved tool catalog with versioned/reviewed contracts. | MEDIUM-HIGH | Extends | [CSA agentic MCP](https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1) ; [tray.ai](https://tray.ai/blog/mcp-security-governance-enterprise) |

> **SEED CORRECTION / KEY CONCLUSION (MCP is not a governance platform).** Task rule 3 calls out: *"MCP is not a governance platform."* Confirmed strongly by official MCP docs (G1) and enterprise guidance (G5-G9). **Net structural finding:** Mastra (runtime/workflow/observability/MCP primitives, EE-gated RBAC), Backlog.md (single-tenant markdown store), and Beads (un-permissioned shared graph per Dolt DB) together provide an orchestration/task SUBSTRATE — **none of them, alone or combined, is a complete multi-tenant governance control plane.** A company-wide deployment requires an ADDITIONAL governance layer for: tenant isolation; the five-identity attribution model (G6); per-invocation audit; cost attribution; rate/budget limits; tool catalog + change control; approval gates; cross-app authorization (downstream tokens, no passthrough). This directly supports preserving SuperClaude's existing target-ownership/attribution semantics rather than compressing them into a single "agent identity."

### 5.4.3 Component-Level Governance Reality

| Component | Governance role | What it does NOT provide |
|-----------|-----------------|--------------------------|
| **Mastra** | Runtime, workflow, HITL suspend/resume, MCP client+server, OTel observability, EE RBAC/SSO/FGA (paid) | Complete tenant governance, policy/budget/approval/catalog, cost attribution; Apache core = SimpleAuth only |
| **Backlog.md** | Repo-local markdown task/spec/decision records | Cross-tenant auth, enterprise audit, rate limiting, cost attribution, remote/HTTP transport |
| **Beads** | Dolt-backed dependency graph, ready-work scheduler, agent memory, gates, audit trail | Cross-tenant IAM, policy enforcement, MCP server inventory, cost attribution; one shared graph per DB |
| **MCP (protocol)** | Context/tool/resource exchange; optional OAuth 2.1 auth | Identity, policy, visibility, catalog, audit, rate limits, cost — all left to implementers |

---

## 5.5 External Research Summary

**Capability verdict.** The fresh external research supports the *technical feasibility* of a Mastra + Backlog.md + Beads orchestration substrate: Mastra supplies durable workflows (a direct MDTM-checkpoint analog) plus the `AcpAgent` subprocess seam that structurally replaces `ClaudeProcess`/stream-json; Backlog.md supplies a MIT-licensed markdown task-of-record whose schema maps onto MDTM phase items; Beads supplies a dependency-aware ready-work graph with gates and agent memory. **The blockers are not capability gaps but governance, licensing, parity, and maturity gaps.**

**Four seed corrections the fresh research forces (per task rule 3):**

| Corrected claim | Stack-D seed framing | Verified current reality |
|-----------------|----------------------|--------------------------|
| Beads storage | "embedded SQLite or Dolt server-mode"; "`.beads/` SQLite + JSONL" | **Dolt-first ONLY**; classic SQLite+JSONL removed; JSONL is export/interop only; drive `bd --json`, never read JSONL. |
| Mastra RBAC/auth | feasible OSS multi-tenant platform | **Production RBAC/SSO/FGA is Enterprise-licensed** (paid `ee/` commercial agreement); OSS path = SimpleAuth + DIY tenant scoping. |
| Backlog.md MCP / BACK-407 | "BACK-407-aligned, spec-complete" MCP server | **MVP stdio surface**; BACK-407 specifically **UNVERIFIED** (BACK-408 found); decisions CLI-only in MVP; `additionalProperties: false` rejects arbitrary metadata. Probe live before relying on it. |
| Backlog.md ↔ Beads | "shared repo metadata references" integration | **Immature** — open request #588; maintainer recommends narrow import/export sync first, not a broad integration surface. |

**Fifth structural correction:** **MCP is not a governance platform.** A company-wide multi-tenant SuperClaude port needs an additional governance/control-plane layer (tenant isolation, five-identity attribution, audit, cost attribution, rate/budget, tool catalog, approvals) above all three components.

**Authority reminder (task rule 4).** Everything above is EXTERNAL context. Where these findings touch the actual SuperClaude/IronClaude code (the `ClaudeProcess` seam, MDTM tasklist/rerun semantics, hook/freshness/verify-sync/`.claude`-source-of-truth discipline, fork-PR-target enforcement, the ~65K-LOC roadmap/pipeline domain logic), the verified-code findings in Sections 1-4 are authoritative. The external research adds options and risk framing; it does NOT establish parity, and notably does NOT prove Claude Code hook/permission parity, workflow-rerun/idempotency parity, or production stability of Beads/Mastra-EE for this use case. Those remain hands-on-validation items.

**Net recommendation posture (external view, not a decision):** treat the stack as a *substrate*, scope a focused Mastra ACP + durable-workflow spike, version-pin Beads behind an abstraction seam, drive Backlog.md/Beads via CLI/`--json` (not file reads), and budget for either Mastra EE or a DIY governance/control-plane layer before any multi-tenant rollout. "Do not port / keep the Python harness" remains a live, defensible option for the heavy domain logic.

---

**Status:** Complete
