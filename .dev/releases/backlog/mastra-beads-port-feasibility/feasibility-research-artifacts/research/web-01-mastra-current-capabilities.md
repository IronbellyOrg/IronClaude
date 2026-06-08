# Web Agent 01 — Mastra Current Capabilities and Licensing

**Date:** 2026-06-02
**Status:** Complete
**Topic:** Mastra current workflow, agent, storage, observability, deployment, auth/RBAC, MCP capabilities, 1.0+ claims, and Enterprise licensing
**Provenance:** Tavily search/extract first, Context7 for Mastra docs. No WebSearch/WebFetch fallback used.

---

## Methodology and Provenance

External research used Tavily search/extract first, prioritizing official Mastra docs, official blog/changelog/release pages, official pricing/licensing information, and the official GitHub repository. Context7 was then used for current Mastra documentation and code-reference confirmation. Provenance tags: `tavily` (web search/extraction), `context7` (Mastra library docs).

## Key External Findings

### 1. Workflow durability, suspend/resume, snapshots, and retries — HIGH

Mastra workflows support pause/resume through `suspend()` and `resume()`/`resumeStream()`. On suspend, Mastra stores a snapshot in the configured storage provider; official docs state snapshots persist across deployments and application restarts and can resume from a specific step ID. Deployment docs describe workflow runners: built-in runner, Inngest integration (step memoization, automatic retries, monitoring, suspend/resume), and Temporal integration (durable execution, retries) — but `@mastra/temporal` is identified as experimental/not production-ready in at least one current deployment page. 1.0+ materials mention per-step execution, `startAsync()`, `onError`/`onFinish` callbacks, cron/scheduled workflows, retry visibility in traces, and a workflow scheduler with multi-instance claiming/CAS.

- Sources: https://mastra.ai/docs/workflows/suspend-and-resume ; https://mastra.ai/docs/deployment/workflow-runners ; https://mastra.ai/docs/workflows/overview ; https://mastra.ai/blog/changelog-2026-01-20 ; https://github.com/mastra-ai/mastra/releases ; Context7 `/mastra-ai/mastra`
- Relationship to codebase: Supports/extends codebase need for durable workflow orchestration. Mastra can model SuperClaude-style phase/task pipelines with durable snapshots and human gates. Production retry/durability depends on runner choice and storage configuration. Treat Temporal cautiously.

### 2. Workflow composition, agent/tool invocation, deterministic orchestration — HIGH

Step-based, type-safe pipelines via `createWorkflow()`/`createStep()` with `inputSchema`/`outputSchema`. Steps can call functions, APIs, agents, tools, and other workflows. Registered workflows can be called from agents, tools, Mastra Client, or CLI. Docs distinguish workflows (deterministic/inspectable control flow) from agents (probabilistic LLM/tool execution).

- Sources: https://mastra.ai/docs/workflows/overview ; https://mastra.ai/reference/configuration ; https://mastra.ai/blog/announcing-mastra-1
- Relationship to codebase: Supports porting SuperClaude CLI orchestration as explicit workflow graphs; phases/tasks become steps; agent/tool calls isolated as steps.

### 3. Subprocess/tool invocation and workspace command execution — HIGH

Mastra Workspace abstraction gives agents a persistent environment for files and command execution. `WorkspaceSandbox` interface includes `executeCommand(command, args?, options?)`, `start()`, `stop()`, `destroy()`, process management, timeouts, and status/resource reporting. Added in `@mastra/core@1.1.0`. Recent release notes mention `stdout`, `stderr`, `wait()`, and bounded retention via `maxRetainedBytes`.

- Sources: https://mastra.ai/docs/workspace/overview ; https://mastra.ai/reference/workspace/sandbox ; https://mastra.ai/reference/workspace/workspace-class ; https://github.com/mastra-ai/mastra/releases
- Relationship to codebase: Extends subprocess/tool invocation seam. Mastra Workspaces may provide the runtime substrate for CLI-like operations, but SuperClaude hook enforcement, UV-only Python rules, git safety, and `.claude/` source-of-truth discipline must be recreated/integrated explicitly. **Does NOT prove parity with Claude Code's hook/permission model.**

### 4. Storage capabilities and durability substrate — HIGH

Instance-level and agent-level storage. Providers: libSQL/Turso, PostgreSQL, MongoDB, Redis/Upstash, DynamoDB, MSSQL, ClickHouse, Cloudflare integrations, and composite storage. `MastraCompositeStore` routes domains (memory, workflows, scores, observability) to different backends. ClickHouse recommended for production observability; libSQL for local dev; in-memory resets on process change.

- Sources: https://mastra.ai/docs/memory/storage ; https://mastra.ai/reference/storage/composite ; https://mastra.ai/reference/storage/clickhouse
- Relationship to codebase: Supports persisting SuperClaude pipeline state, task records, workflow snapshots, traces. Backlog.md/Beads integration is NOT native and needs adapter design.

### 5. Observability, traces, Studio, production debugging — HIGH

AI-focused tracing auto-instruments agent runs, LLM generations, tool calls, and workflow steps with token usage, model params, tool details, and conversation flows. Exporters send to Mastra platform or storage-backed Studio. Studio visualizes workflow graphs, runs step-by-step, inspects traces, lists MCP servers, runs tools in isolation. 1.0 unified observability schema uses `entityId`, `entityType`, `entityName`.

- Sources: https://mastra.ai/docs/observability/tracing/overview ; https://mastra.ai/docs/studio/overview ; https://mastra.ai/blog/changelog-2026-01-20
- Relationship to codebase: Supports observability/diagnosability sections. SuperClaude-specific artifacts/compliance/tasklist state need custom trace attributes or storage integration.

### 6. Auth, RBAC, FGA, Enterprise licensing, multi-user access — HIGH (key risk)

Auth is optional; without it, Studio and API routes are public. Providers: Simple Auth, JWT, Auth0, Better Auth, Clerk, Firebase, Okta, Supabase, WorkOS. RBAC/FGA exist but are tied to Enterprise Edition in important cases: imports from `@mastra/core/auth/ee`, `StaticRBACProvider`, `DEFAULT_ROLES`, `MastraFGAPermissions`, WorkOS FGA. Studio Auth SSO/RBAC and Agent Builder require a valid EE license in production. GitHub README/Context7: dual license — Apache 2.0 for core/vast majority, Mastra Enterprise License for `ee/` directories. Enterprise pricing includes RBAC, audit logs, SLAs, dedicated support, VPC/on-prem data locality.

- Sources: https://mastra.ai/docs/server/auth ; https://mastra.ai/docs/studio/auth ; https://mastra.ai/docs/agent-builder/access-control ; https://mastra.ai/pricing ; https://mastra.ai/blog/changelog-2026-03-23 ; Context7 `/mastra-ai/mastra`
- Relationship to codebase: **Critical decision point.** Local/single-user port may not need EE RBAC. Team/multi-user hosted SuperClaude replacement likely depends on Enterprise-licensed features for production RBAC, SSO, audit logs, FGA, on-prem/VPC.

### 7. MCP support — HIGH

`MCPClient` connects agents to external MCP servers (stdio/HTTP/SSE). `MCPServer` exposes agents, tools, workflows over HTTP(S). `@mastra/mcp-docs-server` for IDE/assistant docs. `requireToolApproval` integrates human-in-the-loop approval for MCP tool execution. Recent release notes: "MCP Apps" interactive UI resources, resource listing/reading APIs, FGA enforcement for MCP tool execution.

- Sources: https://mastra.ai/docs/mcp/overview ; https://mastra.ai/docs/build-with-ai/mcp-docs-server ; https://github.com/mastra-ai/mastra/releases
- Relationship to codebase: Supports orchestrating MCP tool surfaces; Mastra can be both MCP client and server. Need hands-on validation for Claude Code-specific MCP/hook behavior.

### 8. Deployment and runtime options — HIGH

`mastra dev` (local), `mastra build`/`mastra start` (self-contained server), `mastra server deploy`/`mastra studio deploy` (platform). Generated server is Hono-based; adapters for Express, Hono, Fastify, Koa. Registered agents/workflows become REST endpoints with OpenAPI/Swagger. Platform Organizations are multi-tenant containers. Deployment models: fully managed, self-hosted server with managed Studio, self-hosted runtime+observability.

- Sources: https://mastra.ai/docs/server/mastra-server ; https://mastra.ai/docs/mastra-platform/overview ; https://mastra.ai/blog/deployment-models
- Relationship to codebase: Extends analysis beyond CLI-only. Mastra can host SuperClaude orchestration as APIs/Studio workflows; CLI-native parity may need wrappers or hybrid design.

### 9. Mastra 1.0+ maturity claims — MEDIUM

Official 1.0 announcement claims production usage at Replit, PayPal, Sanity, Marsh McLennan; ~300k weekly npm downloads, ~19.8k GitHub stars at 1.0 (later ~24k), 300+ contributors. 1.0 introduced server adapters, observability integrations (Langfuse, Braintrust, Arize, LangSmith), and breaking changes with codemods. Vendor claims; need independent validation.

- Sources: https://mastra.ai/blog/announcing-mastra-1 ; https://github.com/mastra-ai/mastra

### 10. Multi-user and multi-tenant implications — HIGH

Organizations = multi-tenant containers; Projects span Observability/Studio/Server deployments. Auth secures Studio + API; RBAC/FGA restricts agents/workflows/tools/datasets/memory/Agent Builder — but production-grade RBAC/FGA/SSO/audit/on-prem features are Enterprise-linked. Agent Builder without RBAC grants every authenticated user full access; without auth, open to anyone who can reach the server.

- Sources: https://mastra.ai/docs/mastra-platform/overview ; https://mastra.ai/docs/server/auth ; https://mastra.ai/pricing

## Limitations and Open Questions

1. Hands-on validation required for workflow restart/replay/partial-rerun/idempotency semantics.
2. Temporal integration maturity is ambiguous (marked experimental in deployment docs).
3. Claude Code hook parity is NOT established; Workspace command execution does not replicate Claude Code project hooks, freshness checks, staging restrictions, or permission prompts.
4. Enterprise licensing may gate team deployment (production SSO/RBAC/FGA/Studio auth/Agent Builder/audit/on-prem).
5. Backlog.md and Beads are not native Mastra concepts; need adapters and state synchronization.
6. Subprocess safety (allowlists, env isolation, secret redaction, timeout, retention, approval) must be designed for parity.
7. Data residency/prompt/trace privacy depends on deployment model.

## Key External Findings (Summary)

Mastra is externally capable of supporting a SuperClaude orchestration port in principle: durable workflows with snapshots/suspend-resume, typed steps and nested workflows, agent/tool/workflow invocation, workspace filesystem/command execution, rich observability and Studio, MCP client/server, flexible deployment, and auth/RBAC/FGA paths. The main risks are not capability gaps but **parity and governance gaps**: recreating Claude Code hook behavior and SuperClaude safety rules, safe subprocess/workspace operations, Backlog.md/Beads adapters, proving workflow rerun/recovery semantics, and Enterprise licensing for production team RBAC/SSO/audit/FGA/on-prem.

## Recommendations from External Research

1. Prototype Mastra as a durable orchestration layer, not just an agent wrapper. Model phases/tasks as typed steps and nested workflows; test suspend/resume, failed-step restart, partial rerun, scheduled workflows, step trace inspection. (HIGH)
2. Treat Workspaces as the candidate subprocess/filesystem layer, but require a safety spike before assuming CLI parity. (HIGH)
3. Separate local/open-source and team/enterprise architecture tracks; assume Enterprise conversations for hosted multi-user RBAC/SSO/audit/FGA/on-prem. (HIGH)
4. Use composite storage in any serious prototype (PostgreSQL/libSQL for snapshots, ClickHouse for observability; avoid in-memory except tests). (HIGH)
5. Preserve SuperClaude-specific governance outside Mastra defaults (UV-only Python, `.claude/` source-of-truth/staging, fork PR target, freshness checks, safe command execution, Backlog/Beads consistency, tasklist rerun). (HIGH)
6. Use Mastra observability/Studio for diagnosability with custom trace attributes (task/phase/Backlog/Beads IDs, agent/tool names, git branch/commit). (MEDIUM-HIGH)
7. Validate MCP inbound and outbound, with approval-gated and auth/FGA-enforced tool execution. (HIGH)

## Bottom Line

External research supports a focused Mastra spike, especially around durable workflow orchestration plus workspace command execution. It does NOT justify a full migration without hands-on validation.
