# Web Agent 04 — MCP and Multi-Tenant Governance

**Date:** 2026-06-02
**Status:** Complete
**Topic:** MCP enterprise limitations, tenancy, audit, cost attribution gaps, governance/control-plane patterns for AI orchestration systems, and whether Mastra+Backlog+Beads needs extra governance services
**Provenance:** Tavily search/extract only; no WebSearch/WebFetch fallback used.

---

## Findings

### 1. MCP host/client/server model is deliberately narrow; does not define enterprise governance — HIGH

MCP uses a client-server architecture (host creates one client per server; servers expose tools/resources/prompts; clients can expose sampling/elicitation/logging). MCP focuses on context exchange and explicitly does not dictate how AI apps use LLMs or manage context.

- Source: https://modelcontextprotocol.io/docs/concepts/architecture [tavily]
- Relationship to codebase: Supports concern that skills/harness ownership and company-wide orchestration cannot be delegated to MCP alone.

### 2. MCP authorization optional but strongly recommended for enterprise/audit/rate-limiting/per-user tracking — HIGH

Official guidance: authorization is optional but strongly recommended when servers access user-specific data, require auditability, need consent, are enterprise, or need rate limiting/usage tracking per user.

- Source: https://modelcontextprotocol.io/docs/tutorials/security/authorization [tavily]
- Relationship to codebase: Any company-wide SuperClaude recreation must require auth for remote/shared MCP servers.

### 3. MCP remote-server auth is OAuth 2.1-based (PRM, resource indicators, token validation, audience binding) — HIGH

Protected MCP servers act as OAuth 2.1 resource servers; HTTP authorization should use OAuth 2.1, DCR where supported, OAuth Protected Resource Metadata, Authorization Server Metadata, resource indicators, bearer headers, token validation. Servers must validate tokens were issued for them and reject invalid/expired tokens.

- Source: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization [tavily]
- Relationship to codebase: A production remote MCP-backed orchestration service needs a dedicated auth/resource-server implementation.

### 4. Token passthrough explicitly forbidden — creates audit/accountability gaps — HIGH

Token passthrough (accepting client tokens without validating issuance, passing to downstream APIs) is an anti-pattern: bypasses rate limits/monitoring, breaks accountability/audit, confuses downstream logs, enables exfiltration, violates trust boundaries. Servers must not accept tokens not explicitly issued for them.

- Source: https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices [tavily]
- Relationship to codebase: Tool execution/authority must be explicit and logged; downstream services need separate tokens + attribution metadata, not forwarded credentials.

### 5. Official MCP guidance highlights multi-tenant/realm mix-ups and session-ID misuse — HIGH

Pitfalls: unauthenticated DCR, multi-tenant/realm mix-ups, generic audience/resource indicators, error detail leakage, treating session IDs as auth. Guidance: pin to single issuer/tenant unless explicitly multi-tenant, reject tokens from other realms, require resource/audience match, never tie authorization to `Mcp-Session-Id`.

- Source: https://modelcontextprotocol.io/docs/tutorials/security/authorization [tavily]
- Relationship to codebase: Needs tenant-aware auth broker/gateway with issuer pinning, audience validation, session/auth separation.

### 6. MCP scope minimization implies tool-/capability-level scopes — HIGH

Broad scopes (`files:*`, `db:*`, `admin:*`) expand blast radius, obscure audit, increase revocation friction. Mitigations: minimal initial scopes, incremental elevation via `WWW-Authenticate` challenges, logging elevation with correlation IDs, no wildcard scopes.

- Source: https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices [tavily]
- Relationship to codebase: Map slash command/skill privileges to granular tool/capability scopes, not one broad "agent can do everything" permission.

### 7. Enterprise governance sources: MCP's missing layer is identity, policy, visibility, audit, catalog, change control — MEDIUM

Tray.ai: MCP describes how clients/servers exchange resources/tools but not who acts, when, or under what conditions — analogous to early REST needing API-management layers. Recommends recording caller identity/session, tool name/version/schema, inputs, target account, outcome, policy evaluation, approvals.

- Source: https://tray.ai/blog/mcp-security-governance-enterprise [tavily]

### 8. Enterprise MCP needs method-level governance aligned to SSO/RBAC — MEDIUM

Scalekit: five foundations — identity boundaries (humans/clients/agents), governance mapping MCP methods to enterprise permissions, observability/auditability, policy enforcement at MCP boundaries, SSO/IdP integration. Map methods (`logs.read`, `analytics.query`, `incidents.trigger`) to scopes and RBAC.

- Source: https://www.scalekit.com/blog/enterprise-mcp-how-identity-sso-and-scoped-auth-actually-work [tavily]

### 9. Multi-tenant agents require explicit trigger/execution/authorization/tenant/attribution identities — MEDIUM (very high relevance)

Scalekit: agent systems need separate trigger, execution, authorization, tenant, and attribution identities. Access-control bugs surface silently when execution and tenant identities are conflated. Patterns: explicit parameter translation from config, no inference from user messages, tenant boundary enforcement, separate execution/attribution identity, config-driven RBAC with validation.

- Source: https://www.scalekit.com/blog/access-control-multi-tenant-ai-agents [tavily]
- Relationship to codebase: Strongly supports preserving SuperClaude target ownership/attribution semantics rather than compressing into a single "agent identity."

### 10. Control-plane pattern: AI governance is broader than an MCP gateway or LLM gateway — MEDIUM

Speakeasy: an AI control plane governs between every agent and every system — unifying connection, identity, policy enforcement, observability. Distinguishes LLM gateway (model calls/routing/rate limits) from MCP gateway (tool-calling paths) from a broader AI control plane (identity, policy, observability across all agents).

- Source: https://www.speakeasy.com/resources/ai-control-plane [tavily]
- Relationship to codebase: Supports needing a separate governance/control-plane layer beyond Mastra + Backlog.md + Beads.

### 11. Cost attribution/FinOps not native MCP; requires host/gateway/control-plane metering — MEDIUM-HIGH

FinOps Foundation: cost attribution, continuous usage auditing, drift detection are governance-layer concerns. MCP governs context/action flow; FinOps/FOCUS governs spend. MCP host responsibilities: observability, logging, usage metering, centralized governance, routing.

- Source: https://www.finops.org/wg/model-context-protocol-mcp-ai-for-finops-use-case [tavily]
- Relationship to codebase: Add usage metering for skills/agents/model calls/tool invocations for company-wide use.

### 12. CSA draft: MCP inventory, authenticated connections, least privilege, audit logging as minimum maturity — MEDIUM-HIGH

CSA draft: all MCP connections authenticated; local servers validate clients; remote uses OAuth 2.1 + PKCE; maintain MCP server inventory (name, version, location, business owner); minimum-permission service accounts; no broad personal/admin tokens; basic audit logging of all tool invocations.

- Source: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1 [tavily]

### 13. Mastra is runtime/workflow/MCP/observability substrate, NOT a complete multi-tenant governance control plane — HIGH

Mastra supports graph workflows, HITL suspend/resume, MCP servers, runtime context/auth, guardrails, logging/tracing/evals, OpenTelemetry observability, and can secure agent endpoints with an identity system — but reviewed docs do not present it as a full enterprise tenant governance, policy, budget, approval, catalog, or cost-attribution control plane.

- Sources: https://mastra.ai/docs ; https://mastra.ai/ai-agent-observability ; https://github.com/mastra-ai/mastra [tavily]

### 14. Backlog.md is project-local markdown/Git-native task management, not enterprise tenancy/audit governance — HIGH

Markdown-native task manager/Kanban for Git repos; CLI, web UI, MCP integration, agent workflow instructions, docs/decisions, optional Git, private/offline, repo-local. Does not provide cross-tenant auth, enterprise audit, rate limiting, or cost attribution.

- Source: https://github.com/MrLesk/Backlog.md [tavily]

### 15. Beads is AI-native, Dolt-backed issue/memory coordination with multi-agent primitives, not org-wide governance — HIGH

Dolt-powered issue tracker for AI-supervised coding: hash-based IDs, dependency-aware execution (`bd ready`), gates, routing, multi-agent coordination, JSON agent usage, embedded/server modes, Dolt push/pull, audit trails, project memory. Not sufficient for cross-tenant IAM, policy enforcement, MCP server inventory, or cost attribution.

- Sources: https://gastownhall.github.io/beads ; https://github.com/gastownhall/beads [tavily]

### 16. Enterprise MCP/gateway patterns emphasize curated approved tool catalog + schema/version change control — MEDIUM

Tray: small approved catalog with stable schemas; versioned tool/resource contracts; staging through test environments; tracking which agents consume which versions; review like code; documented rollback. Reduce hundreds of raw tools to a smaller set of structured workflows.

- Source: https://tray.ai/blog/mcp-security-governance-enterprise [tavily]

## Synthesis and Implications

**MCP is not a governance platform.** It is a protocol for connecting hosts/clients/servers and exchanging tools/resources/prompts; authorization is optional and most governance controls are left to implementers.

Practical split for a SuperClaude recreation:
- **Mastra:** agent/workflow runtime, TypeScript orchestration, HITL, observability primitives, MCP integration.
- **Backlog.md:** repo-local task/spec/decision records.
- **Beads:** AI-native issue graph, memory, dependencies, multi-agent coordination.
- **Missing layer:** enterprise governance/control plane — identity, tenant isolation, policy, tool catalog, audit, cost attribution, budget/rate limits, approvals, cross-system traceability.

Core enterprise gaps if using only Mastra + Backlog.md + Beads: tenant isolation; attribution (separate trigger/execution/authorization/tenant/attribution identities); audit (per-invocation logs); cost attribution (model + tool-call metering by tenant/team/user/agent/workflow/task); rate limiting/budget enforcement; tool catalog/change control; approval gates; cross-app authorization (downstream tokens, no passthrough).

## Key External Findings

1. Official MCP architecture confirms MCP is an integration protocol, not governance.
2. MCP authorization is optional but enterprise use requires it (audit, tracking, consent, rate limiting).
3. MCP forbids token passthrough; requires audience/resource validation.
4. Official MCP guidance calls out multi-tenant/realm mix-ups, generic audiences, session-ID misuse, broad scopes.
5. Enterprise guidance: MCP needs an API-management/control-plane layer (identity, policy, visibility, catalog, rate limits, audit, analytics).
6. Multi-tenant agents must separate trigger/execution/authorization/tenant/attribution identities.
7. Cost attribution is outside MCP; needs host/gateway/control-plane telemetry + FinOps.
8. Mastra provides runtime/workflow/observability/MCP primitives but is not a complete governance control plane.
9. Backlog.md and Beads are task/memory/coordination substrates, not tenant-aware runtime governance.
10. A Mastra + Backlog.md + Beads SuperClaude port needs an **additional governance/control-plane layer** before company-wide multi-tenant deployment.

## Recommendations from External Research

1. Treat Mastra + Backlog.md + Beads as an orchestration/task substrate, not the complete enterprise platform.
2. Add a governance/control-plane service: tenant registry; user/team/agent identity mapping; RBAC/ABAC policy store; tool/skill catalog + ownership registry; MCP server inventory; approval policy engine; audit/event log; cost and rate/budget attribution; environment separation and rollout controls.
3. Add an MCP/AI gateway for production: enforce OAuth 2.1 for remote MCP; validate issuer/audience/scopes/expiry; reject passthrough; tool-level allowlists; OpenTelemetry traces + structured audit events; rate limits/budgets by tenant/team/user/agent/workflow.
4. Define granular scopes for SuperClaude capabilities (avoid `superclaude:*`); map commands/skills/tools to read-only/code-edit/git-write/external-search/infra-change/destructive-action/admin; require progressive elevation + approval for higher-risk actions.
5. Preserve/formalize SuperClaude ownership semantics (business+technical owner, version, schema, allowed tenants/environments, rollback plan per skill/tool/server).
6. Implement audit records for every orchestration action (timestamp, tenant, user, agent/client, workflow/task ID, tool/skill name+version+schema, input classification, target system/account, result, policy decision, approval ID, cost, correlation ID).
7. Implement cost attribution (model tokens, tool calls, retries, evaluations, workflow runs) by tenant/team/project/task/agent with budget alerts/limits.
8. Use Mastra observability as a telemetry source feeding the governance plane; join traces with Backlog.md/Beads IDs.
9. Keep Backlog.md (specs/tasks/decisions) and Beads (dependency graph, memory, coordination) scoped; neither owns runtime authorization or tenant isolation.
10. Do not expose raw MCP server/tool catalogs broadly; build curated workflow tools aligned to SuperClaude commands/skills, versioned and reviewed like APIs.
