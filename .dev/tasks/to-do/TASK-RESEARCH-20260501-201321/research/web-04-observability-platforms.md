# Research: LLM observability platforms

**Topic:** Observability/tracing tools as conversation-context platforms
**Status:** Complete
**Date:** 2026-05-01

---

## LangSmith (LangChain)

- **Positioning:** Closed-source SaaS observability + eval platform from LangChain; LangChain's commercial offering for tracing/dataset/eval workflows.
- **Sources:** https://www.langchain.com/pricing-langsmith ; https://docs.langchain.com/langsmith/observability-concepts ; https://langchain-5e9cc07a.mintlify.app/langsmith/data-export ; https://support.langchain.com/articles/6059731320-how-do-i-connect-claude-computer-cursor-to-langsmith-cloud-for-trace-investigation
- **Reliability:** Official
- **Relevance:** HIGH
- **Trace granularity:** Full conversation traces — captures inputs, outputs, tool calls, intermediate LLM steps, retrieval steps. Threaded conversation views supported.
- **Team aggregation:** Yes — workspaces, projects, organizations; RBAC on paid tiers.
- **Search:** Hybrid — UI filters, full-text, attribute filters, run/thread query language. No native semantic search (must export).
- **Dataset/RAG export:** Yes — first-class "convert traces to dataset" feature; bulk export (JSONL, CSV) via UI and API; datasets used for evals and prompt regression. RAG re-injection requires user code.
- **Self-host:** Yes — paid Enterprise/hybrid only ("self-hosted LangSmith"); not free for self-host.
- **Pricing:** Developer free tier (~5k traces/mo); Plus ($39/seat/mo + usage); Enterprise (contact). Trace overage $0.50/1k base traces, more for extended retention.
- **Coding-tool integration:** Officially documented — LangChain support article shows connecting Claude Code and Cursor to LangSmith via env vars / proxy / OTLP. Not a packaged "click-install" — requires routing the LLM-side traffic.
- **OSS license:** None (LangSmith is closed-source). LangChain SDK that emits traces is MIT.
- **Activity signal:** Backed by LangChain (Series B, large active company); LangChain repo ~95k+ stars.
- **Architectural fit:** Instrumentation-only. Cannot ingest existing chat archives without a custom shim that reads SpecStory-style files and replays them as trace events into the API. Must capture at API call site.

## Langfuse

- **Positioning:** OSS-first LLM observability and evaluation platform; closest direct comparable to "open conversation log store" — broad ecosystem, MIT core.
- **Sources:** https://langfuse.com/ ; https://github.com/langfuse/langfuse ; https://langfuse.com/docs/tracing ; https://langfuse.com/self-hosting ; https://langfuse.com/integrations/other/claude-code ; https://langfuse.com/handbook/chapters/open-source ; https://langfuse.com/pricing-self-host
- **Reliability:** Official
- **Relevance:** HIGH
- **Trace granularity:** Full — sessions, traces, spans, generations, observations; conversation/threaded view (`session.id`); captures input messages, tool calls, output, latency, cost, metadata.
- **Team aggregation:** Yes — orgs, projects, members, RBAC. Multi-project aggregation native.
- **Search:** Hybrid — UI filters, full-text on prompts/outputs, metadata filtering, time-window, tag-based. No native vector/semantic search; saved views.
- **Dataset/RAG export:** Yes — explicit "Datasets" feature converts traces into evaluation datasets. Public API (REST + Python/TS SDK) for export. Used as a context source for prompts and evals. RAG re-injection is user-code (export then index).
- **Self-host:** Yes — full-featured self-host under MIT (Docker, Helm); enterprise-only features (audit logs, project-level RBAC, retention policies, SCIM, support) live in `/ee` and require a license key.
- **Pricing:** OSS self-host free. Cloud: Hobby (free, 50k observations/mo), Core ($59/mo + usage), Pro ($199/mo + usage), Enterprise. Per-1k-observation overage.
- **Coding-tool integration:** Yes, first-class — official Claude Code integration page (uses Claude Code's OTLP hooks); Cursor integration; Continue, Aider via OpenLLMetry / OpenTelemetry. Plugin index (`langfuse-pack`) ships a Claude Code plugin.
- **OSS license:** MIT for core (`/`), commercial EE license required for `/ee` modules (RBAC at project level, audit log, retention, SCIM, etc.).
- **Activity signal:** ~26.4k GitHub stars, very active (weekly releases as of 2026).
- **Architectural fit:** Primarily instrumentation-side. However, Langfuse's REST `/api/public/ingestion` endpoint accepts arbitrary trace events — a SpecStory-style harvester could post historical chats as traces. So ingest-existing-chats is feasible with adapter code (not turnkey).

## Helicone

- **Positioning:** Open-source AI gateway / LLM proxy + observability — sits in front of provider APIs as a transparent proxy.
- **Sources:** https://www.helicone.ai/ ; https://www.helicone.ai/pricing ; https://github.com/Helicone/helicone ; https://docs.helicone.ai/integrations/overview ; https://docs.helicone.ai/integrations/tools/mcp ; https://helicone.mintlify.app/gateway/overview
- **Reliability:** Official
- **Relevance:** HIGH (architecturally distinct — proxy model, easiest "drop-in" capture)
- **Trace granularity:** Full request/response, multi-turn sessions, tool-call payloads, cost, latency, errors. Supports "Sessions" feature for grouping multi-turn.
- **Team aggregation:** Yes — orgs, projects, member roles. Aggregates across keys/projects.
- **Search:** Hybrid — UI filters, request body search, tags/properties, semantic search (vector index over prompts/responses) on Pro+.
- **Dataset/RAG export:** Yes — datasets feature; Jobs API to export request bodies; can fine-tune or re-inject. Webhooks supported.
- **Self-host:** Yes — open-source under Apache-2.0; Docker Compose + Helm; full-featured.
- **Pricing:** Hobby free (10k req/mo, 1 GB storage); Pro $79/mo + usage; Team $799/mo + usage; Enterprise.
- **Coding-tool integration:** Strong — Helicone MCP Server officially supports Claude Code and Cursor. Proxy pattern (`api.anthropic.com` → `anthropic.helicone.ai`) means any tool that allows a custom Anthropic base URL is captured (Claude Code via `ANTHROPIC_BASE_URL`, Cursor via custom OpenAI/Anthropic proxy, Continue, Cline, Aider all support custom base URLs).
- **OSS license:** Apache-2.0 (per repo).
- **Activity signal:** ~3-4k stars, active development; commercial team.
- **Architectural fit:** **Best architectural fit of this bucket for "minimal-instrumentation capture"** — proxy mode means engineers only change a base URL env var. Cannot ingest existing chat archives directly, but going forward, all coding-tool LLM traffic can be captured automatically.

## Arize Phoenix

- **Positioning:** Open-source, OpenTelemetry-native LLM tracing and evaluation; can run fully local (laptop) or as managed Arize AX.
- **Sources:** https://phoenix.arize.com/ ; https://github.com/arize-ai/phoenix ; https://arize.com/docs/phoenix ; https://arize.com/docs/phoenix/tracing/tutorial/sessions ; https://community.arize.com/x/phoenix-support/0ja85s8ctatc/migrating-user-conversations-to-traces-in-phoenix
- **Reliability:** Official
- **Relevance:** HIGH
- **Trace granularity:** Full — OpenTelemetry / OpenInference spans for LLM, retriever, tool, agent, embedding. Sessions for multi-turn conversation grouping.
- **Team aggregation:** Self-hosted Phoenix is single-tenant by default; enterprise multi-tenant via Arize AX (the paid SaaS). Phoenix-Cloud has projects/users.
- **Search:** Hybrid — UI filters, full-text, span attribute query; semantic search over inputs/outputs (vector embeddings) is a built-in feature; pandas-style export to Jupyter.
- **Dataset/RAG export:** Yes — Phoenix has a "Datasets" first-class concept; community guide explicitly covers "Migrating User Conversations to Traces in Phoenix" (i.e., importing pre-existing convos). Pandas DataFrame export, REST API, OTLP.
- **Self-host:** Yes — Apache-2.0 (Phoenix core); fully self-hostable Docker; runs locally as a notebook companion.
- **Pricing:** Free OSS. Phoenix Cloud has free tier; Arize AX (enterprise) has contact-sales pricing.
- **Coding-tool integration:** Indirect — any tool emitting OTLP can target Phoenix's OTLP endpoint (Claude Code OTLP exports, Cursor via OpenLLMetry, etc.). No turnkey coding-tool plugin.
- **OSS license:** Apache-2.0 for `phoenix` core; some adjacent packages (`arize-phoenix-otel`) listed as Elastic-2.0 in some channels — verify per package.
- **Activity signal:** ~5k+ stars on the Phoenix repo, strong release cadence; very active OpenInference ecosystem; backed by Arize.
- **Architectural fit:** Excellent for ingestion of historical chats — community-documented path to convert archived conversations into traces. OTEL-native means minimal lock-in. Instrumentation-side capture, but ingest is well-supported.

## HoneyHive

- **Positioning:** Closed-source enterprise AI observability + evaluation platform; positioned for compliance-heavy/regulated environments.
- **Sources:** https://www.honeyhive.ai/ ; https://www.honeyhive.ai/pricing ; https://docs.honeyhive.ai/v2/introduction/what-is-hhai
- **Reliability:** Official
- **Relevance:** MEDIUM
- **Trace granularity:** Full — sessions, traces, tool calls, retrieval steps. OpenInference compatible.
- **Team aggregation:** Yes — orgs, projects, RBAC; enterprise focus.
- **Search:** Hybrid — UI filters; semantic search; SQL query support on enterprise.
- **Dataset/RAG export:** Yes — datasets, eval suites; export via API.
- **Self-host:** Yes — multi-tenant SaaS, dedicated cloud, self-hosting, air-gapped (per pricing FAQ).
- **Pricing:** Free tier; Pro tier (~$300+/mo per official pricing page); Enterprise (contact). Event-based metering.
- **Coding-tool integration:** None advertised explicitly for Cursor/Claude Code/Cline/Aider; OTEL/OpenInference path possible but not turnkey.
- **OSS license:** None (closed source).
- **Activity signal:** Active commercial product, smaller user base than Langfuse/Helicone.
- **Architectural fit:** Instrumentation-only; weaker integration story for IDE/coding tooling. Better suited if comparable is "enterprise eval suite" not "engineer chat history store."

## Braintrust

- **Positioning:** Closed-source eval-and-logging platform for LLM apps with strong developer ergonomics; SQL/BTQL-driven query layer.
- **Sources:** https://www.braintrust.dev/docs/plans-and-limits ; https://www.braintrust.dev/docs/admin/self-hosting ; https://www.braintrust.dev/docs/observe/filter ; https://www.braintrust.dev/docs/annotate/export ; https://www.braintrust.dev/docs/reference/btql ; https://www.braintrust.dev/foundations/how-to-read-a-trace ; https://www.braintrust.dev/docs/annotate/datasets
- **Reliability:** Official
- **Relevance:** HIGH (search story is strongest among the closed-source SaaS)
- **Trace granularity:** Full — input messages, tool calls, output, span tree, metadata, cost.
- **Team aggregation:** Yes — orgs, projects, RBAC.
- **Search:** Hybrid — UI filters + **SQL/BTQL** (first-class SQL query language over logs/datasets/experiments) + semantic ("deep") search + structured filters.
- **Dataset/RAG export:** Yes — annotated export to JSON/Parquet via UI/SDK/API; explicit datasets concept; BTQL endpoint for ad-hoc export. Strong export story.
- **Self-host:** Yes — documented self-host (AWS Terraform module typically); enterprise-tier feature.
- **Pricing:** Free tier (limited rows/seats); Pro per-seat + usage; Enterprise (contact). Processed-data billing.
- **Coding-tool integration:** No turnkey integration documented for Claude Code/Cursor; SDK can be wired into any caller. OpenLLMetry can route to Braintrust as a backend.
- **OSS license:** None (closed source); SDK is permissive.
- **Activity signal:** Well-funded (Series A), active growth as enterprise eval platform.
- **Architectural fit:** Instrumentation-only; SDK or OTEL ingestion. Best-in-class search/SQL story. Existing chat archives can be ingested via SDK `bt logs upload` style writes.

## PromptLayer

- **Positioning:** Prompt management + observability — long-running (one of the earliest LLM logging tools).
- **Sources:** https://docs.promptlayer.com/features/observability ; https://docs.promptlayer.com/why-promptlayer/how-it-works ; https://docs.promptlayer.com/quickstart ; https://docs.promptlayer.com/features/faq
- **Reliability:** Official
- **Relevance:** MEDIUM
- **Trace granularity:** Request-level — input prompts, completions, metadata, function/tool calls. OTEL-compatible tracing for span-level.
- **Team aggregation:** Yes — workspaces, members.
- **Search:** UI filters + tags + full-text; SQL-like filtering on logs.
- **Dataset/RAG export:** Yes — "Datasets from history" is a documented feature; CSV/API export; can flow into prompt registry/evals.
- **Self-host:** Enterprise tier only (limited public info).
- **Pricing:** Free tier (limited requests); Pro $50/seat/mo; Enterprise.
- **Coding-tool integration:** Not explicitly for IDE coding tools; SDK-based, REST log endpoint (any caller can post). OTEL path supported.
- **OSS license:** Closed source; SDK MIT.
- **Activity signal:** Established but lower visibility vs. newer entrants; mature SDK.
- **Architectural fit:** Instrumentation-side. Historical chats can be POSTed via REST (`log_request`), so a harvest-and-replay shim is straightforward.

## Weights & Biases Weave

- **Positioning:** W&B's LLM-tracing module within the broader W&B ML platform.
- **Sources:** https://docs.wandb.ai/weave ; https://docs.wandb.ai/weave/guides/tracking ; https://docs.wandb.ai/weave/guides/tracking/tracing ; https://docs.wandb.ai/weave/guides/evaluation/export_eval ; https://docs.wandb.ai/weave/guides/core-types/datasets/ ; https://wandb.ai/site/wp-content/uploads/2025/05/Weights_Biases_Deployment_Guide.pdf
- **Reliability:** Official
- **Relevance:** MEDIUM
- **Trace granularity:** Full — Ops/Calls/Traces model; structured span tree; tool-call capture.
- **Team aggregation:** Yes — W&B teams/projects/RBAC; mature multi-tenant.
- **Search:** UI filters, attribute filters, latency/cost/token plots; export to pandas via SDK; not a strong semantic-search story.
- **Dataset/RAG export:** Yes — Datasets, evaluations export REST API.
- **Self-host:** Yes — W&B has long-standing on-prem / dedicated cloud (CoreWeave-managed since acquisition); Weave inherits these deploy options.
- **Pricing:** W&B free tier (single user); Teams ~$50/seat/mo; Enterprise. Weave is bundled.
- **Coding-tool integration:** Not first-class; relies on SDK instrumentation or OTEL.
- **OSS license:** SDK is Apache-2.0; backend is closed.
- **Activity signal:** Backed by W&B (now CoreWeave); large user base from the broader ML platform.
- **Architectural fit:** Instrumentation-side. Strong fit if the team already lives in W&B; otherwise the trace UX is less LLM-conversation-shaped than Langfuse/Phoenix.

## Opik (Comet)

- **Positioning:** Comet's open-source LLM evaluation and observability platform, Apache-2.0; strong RAG focus.
- **Sources:** https://www.comet.com/site/products/opik/ ; https://www.comet.com/site/products/opik/features/ ; https://github.com/comet-ml/opik ; https://www.comet.com/docs/opik/ ; https://docs.ragas.io/en/v0.4.0/howtos/integrations/_opik/
- **Reliability:** Official
- **Relevance:** HIGH
- **Trace granularity:** Full — traces, spans, conversation threads, tool calls, retrieval; OpenTelemetry-friendly.
- **Team aggregation:** Yes — workspaces, projects, members.
- **Search:** UI filters, full-text on inputs/outputs, attribute filters; pandas/SDK export.
- **Dataset/RAG export:** Yes — first-class datasets, prompt management, RAG-eval integrations (e.g., Ragas integration documented).
- **Self-host:** Yes — full Apache-2.0 self-host (Docker, Helm, Kubernetes). Comet Cloud also offered.
- **Pricing:** OSS self-host free. Cloud Free tier; Pro tier (per-seat + usage); Enterprise.
- **Coding-tool integration:** OTEL/OpenLLMetry compatible; no first-class IDE plugin.
- **OSS license:** Apache-2.0 (core). Permissive.
- **Activity signal:** ~19k GitHub stars (rapid growth), very active.
- **Architectural fit:** Instrumentation-side; SDK-based replay path for historical chats is supported (any auth'd POST to the trace endpoint). Apache-2.0 license is the most permissive of the OSS options.

## Lunary

- **Positioning:** Open-source LLM observability with light-touch SDK; analytics + prompt management.
- **Sources:** https://lunary.ai/ ; https://lunary.ai/pricing ; https://lunary.ai/products/logs ; https://github.com/lunary-ai/lunary ; https://lunary.mintlify.app/docs/features/observability
- **Reliability:** Official
- **Relevance:** MEDIUM
- **Trace granularity:** Full — runs, threads (conversation grouping), tool calls, costs, feedback signals.
- **Team aggregation:** Yes — orgs, projects.
- **Search:** UI filters, tags, run/thread search; full-text on prompts.
- **Dataset/RAG export:** Yes — datasets, exports; prompt registry. RAG re-injection requires user code.
- **Self-host:** Yes — Apache-2.0 self-host (Docker).
- **Pricing:** Free OSS; cloud Free tier (1k events/day), Team ($20/seat/mo + usage), Enterprise.
- **Coding-tool integration:** None first-class; SDK-based.
- **OSS license:** Apache-2.0.
- **Activity signal:** ~1-2k stars, smaller community than Langfuse/Opik but active.
- **Architectural fit:** Instrumentation-only; smaller ecosystem; archive-replay possible via SDK.

## AgentOps

- **Positioning:** Agent-focused observability — emphasizes multi-step agent traces, tool-use accounting, session replay.
- **Sources:** https://www.agentops.ai/ ; https://docs.agentops.ai/v1/introduction ; https://github.com/agentops-ai/agentops
- **Reliability:** Official
- **Relevance:** MEDIUM
- **Trace granularity:** Full — sessions, events, LLM calls, tool calls, errors; agent-step replay.
- **Team aggregation:** Yes — orgs, projects.
- **Search:** UI filters, session search; less mature than Langfuse/Braintrust.
- **Dataset/RAG export:** Limited — session export via API; no first-class "datasets to RAG" workflow advertised.
- **Self-host:** Available on AWS/GCP/Azure (per official site); details require enterprise contact.
- **Pricing:** Free dev tier; Pro paid per-seat + usage; Enterprise.
- **Coding-tool integration:** None first-class for IDE coding tools; SDK aimed at agent frameworks (CrewAI, AutoGen, LangGraph).
- **OSS license:** SDK MIT; backend closed.
- **Activity signal:** Active but agent-framework-centric; smaller GA traction.
- **Architectural fit:** Instrumentation-side; weaker fit for IDE conversation capture (focus is autonomous-agent runs).

## Traceloop / OpenLLMetry

- **Positioning:** OpenTelemetry-native LLM observability — Traceloop (commercial backend) + OpenLLMetry (Apache-2.0 open standard / SDK).
- **Sources:** https://www.traceloop.com/pricing ; https://www.traceloop.com/docs/openllmetry/ ; https://traceloop.com/blog/openllmetry ; https://github.com/traceloop/openllmetry ; https://github.com/traceloop/opentelemetry-mcp-server ; https://www.traceloop.com/docs/openllmetry/integrations/langfuse
- **Reliability:** Official
- **Relevance:** HIGH (as the standard for OTEL-based LLM tracing)
- **Trace granularity:** Full — OpenLLMetry spans (LLM, vector DB, embedding, agent, tool); Traceloop backend visualizes trees.
- **Team aggregation:** Yes — Traceloop SaaS has orgs/projects; OpenLLMetry is just instrumentation, can route anywhere.
- **Search:** Traceloop UI offers filter + semantic search; OTEL backends (Langfuse, Phoenix, Datadog, Honeycomb, etc.) determine search UX.
- **Dataset/RAG export:** Traceloop supports dataset/eval flows; OpenLLMetry export is standard OTLP.
- **Self-host:** OpenLLMetry is Apache-2.0 SDK (free, self-host-anywhere); Traceloop backend is SaaS (with limited self-host options).
- **Pricing:** OpenLLMetry free; Traceloop has free tier + paid (per span/trace).
- **Coding-tool integration:** **Strongest standard-based path** — Traceloop launched an MCP server (Dec 2025) that brings OpenTelemetry into Cursor and Claude Code workflows; PyPI `opentelemetry-mcp` package documents this directly.
- **OSS license:** OpenLLMetry: Apache-2.0. Traceloop backend: closed.
- **Activity signal:** OpenLLMetry repo is very active, ~7k+ stars; widely cited as de-facto standard.
- **Architectural fit:** Instrumentation-side, but as the OTLP standard it is the *transport* for many other backends. If we adopt OTEL, any backend (Langfuse, Phoenix, Honeycomb) can be the store. Existing chat archives can be replayed as OTLP spans.

## Laminar (lmnr.ai)

- **Positioning:** Open-source LLM tracing + eval with strong developer-experience focus; OTEL-compatible.
- **Sources:** https://www.lmnr.ai/ ; https://www.lmnr.ai/pricing ; https://docs.lmnr.ai/index-agent/tracing ; https://github.com/lmnr-ai/lmnr
- **Reliability:** Official
- **Relevance:** MEDIUM
- **Trace granularity:** Full — sessions, traces, spans, tool calls; OTEL ingest.
- **Team aggregation:** Yes — workspaces, projects.
- **Search:** UI filters, semantic search on input/output, tags.
- **Dataset/RAG export:** Yes — datasets, evals; SDK-based export.
- **Self-host:** Yes — open-source self-host (Apache-2.0).
- **Pricing:** OSS free. Cloud free tier (limited spans); Pro tier; Enterprise.
- **Coding-tool integration:** OTEL-based (OpenLLMetry path); no first-class IDE plugin.
- **OSS license:** Apache-2.0.
- **Activity signal:** ~3k+ stars, active YC-backed startup.
- **Architectural fit:** Instrumentation-side via OTEL; replayable, similar profile to Langfuse but smaller ecosystem.


## Observability-Platform Comparison Table

| Product | Trace | Team | Search | RAG export | Self-host | Price | OSS | Tool integ | Captured-chat fit |
|---|---|---|---|---|---|---|---|---|---|
| LangSmith | Full (sessions) | Yes (RBAC) | UI+filters+thread query | Datasets, JSONL/CSV | Enterprise only | Free→$39/seat+usage→Ent | Closed | Claude Code, Cursor (docs) | Instrument-only; replay possible via SDK |
| Langfuse | Full (sessions) | Yes (orgs/proj) | UI+filters+full-text | Datasets, REST | **Yes (MIT)** | Free OSS / $59→$199 cloud | MIT (+EE) | **Native Claude Code, Cursor** | Instrument; ingest viable via `/api/public/ingestion` |
| Helicone | Full (sessions) | Yes | UI+semantic+filters | Datasets, Jobs API | **Yes (Apache-2.0)** | Free→$79→$799 | Apache-2.0 | **MCP for Claude Code/Cursor + proxy mode** | Proxy = best forward capture; no archive ingest |
| Arize Phoenix | Full (OTEL sessions) | Limited OSS / yes via AX | UI+semantic | Datasets + community import guide | **Yes (Apache-2.0)** | Free OSS / AX contact | Apache-2.0 | OTEL only | **Best historical-ingest story (community-documented)** |
| HoneyHive | Full | Yes (RBAC) | UI+semantic+SQL (ent) | Datasets | Yes (incl. air-gap) | Free→$300+→Ent | Closed | None first-class | Instrument-only |
| Braintrust | Full | Yes | **SQL/BTQL + semantic** | **Strong (JSON/Parquet, BTQL)** | Yes (ent) | Free→per-seat+usage→Ent | Closed | None first-class | Instrument-only; SDK upload |
| PromptLayer | Request-level | Yes | UI+filters+SQL-like | Datasets-from-history | Enterprise | Free→$50/seat→Ent | Closed | None first-class | Instrument; REST replay easy |
| W&B Weave | Full (Ops/Calls) | Yes (mature) | UI+filters | Datasets, REST | **Yes (mature on-prem)** | Free→$50/seat→Ent | SDK Apache; backend closed | None first-class | Instrument-only |
| Opik (Comet) | Full (threads) | Yes | UI+full-text | Datasets, Ragas integ | **Yes (Apache-2.0)** | Free OSS / cloud tiers | Apache-2.0 | OTEL/OpenLLMetry | Instrument; SDK replay |
| Lunary | Full (threads) | Yes | UI+filters | Datasets | **Yes (Apache-2.0)** | Free OSS / $20/seat | Apache-2.0 | None first-class | Instrument; SDK replay |
| AgentOps | Full (sessions) | Yes | UI+filters | Limited (session export) | Yes (ent) | Free→Pro→Ent | SDK MIT; backend closed | None first-class | Instrument-only; agent-frame focus |
| Traceloop / OpenLLMetry | Full (OTEL) | Yes (Traceloop) | Backend-dependent | Backend-dependent | OpenLLMetry yes (Apache-2.0) | OpenLLMetry free; Traceloop tiered | OpenLLMetry Apache-2.0 | **MCP server for Claude Code, Cursor (Dec 2025)** | OTEL replay path is the standard |
| Laminar | Full (OTEL) | Yes | UI+semantic | Datasets | **Yes (Apache-2.0)** | Free OSS / cloud tiers | Apache-2.0 | OTEL/OpenLLMetry | Instrument; OTEL replay |

## Key External Findings

- **Two distinct architectures dominate Bucket C** for capturing engineer-AI traffic at the API layer:
  1. **Proxy/gateway** (Helicone): change a base URL, capture transparently. Lowest engineering lift; works for any coding tool that supports custom Anthropic/OpenAI base URLs (Claude Code via `ANTHROPIC_BASE_URL`, Cursor, Continue, Cline, Aider — all support it).
  2. **OTLP / OpenLLMetry instrumentation** (Phoenix, Langfuse, Traceloop, Opik, Laminar): emit OpenTelemetry spans. Requires the coding tool itself to support OTLP export (Claude Code does — official OTEL hooks; others vary).
- **Claude Code and Cursor both have first-class integrations with Langfuse and Helicone today** (Langfuse integration page; Helicone MCP server). LangSmith has documented but more manual setup. Traceloop launched an MCP server in Dec 2025 specifically to bring OpenTelemetry into Cursor and Claude Code.
- **Cline, Aider, Continue do not have published first-class observability-platform plugins**; they do support custom base URLs (Helicone proxy-mode covers them) and SDK-level instrumentation by user code.
- **OSS leaders by stars/license attractiveness (2026):** Langfuse (~26.4k, MIT core), Opik (~19k, Apache-2.0), Phoenix (~5k+, Apache-2.0), Laminar (~3k+, Apache-2.0), Helicone (~3-4k, Apache-2.0), Lunary (~1-2k, Apache-2.0). All five offer non-paid self-host suitable for an internal team store.
- **Strongest search story:** Braintrust (SQL/BTQL + semantic), Phoenix (semantic + OTEL attribute filters), Helicone (semantic on Pro+). Most others are UI-filters + full-text only.
- **Strongest dataset/RAG export story:** Braintrust (BTQL + Parquet), Langfuse (datasets + REST), Phoenix (pandas + datasets + community import guide), Opik (Ragas integ).
- **Critical capability gap for "ingest existing IDE chat archives":** Only Phoenix has a community-documented playbook for migrating user conversations into traces post-hoc. All others can be done via SDK/REST replay but require custom adapter code (e.g., a SpecStory→Langfuse shim writing to `/api/public/ingestion`).
- **None of these platforms harvest IDE-side artifacts natively.** They all expect to sit at the API call site. SpecStory's architectural niche (post-hoc IDE-archive harvesting) is not duplicated by any Bucket-C platform.
- **OpenLLMetry has emerged as the de-facto OTEL standard for LLM tracing**; using it as the transport keeps the team backend-agnostic (can route to Langfuse, Phoenix, Traceloop, Honeycomb, etc.).

## Recommendations from External Research

For an architecture recommending a unified engineer-AI conversation context store, the observability-bucket findings shape the comparables analysis as follows:

1. **Two viable Bucket-C architectures emerge as serious comparables** — not one. Treat them separately in the comparables matrix:
   - **C-Proxy:** Helicone-style gateway. Pros: zero code change, captures all coding tools that support custom base URLs, ingests everything Claude Code / Cursor / Cline / Aider send. Cons: must maintain proxy infra; outage = no LLM; cannot ingest historical chat archives.
   - **C-OTEL:** Langfuse / Phoenix / Opik with OpenLLMetry. Pros: vendor-neutral via OTEL; rich span model; backend-swappable; Phoenix has a documented historical-ingest path. Cons: requires per-tool instrumentation or OTLP support; Cline/Aider/Continue lack first-class hooks today.

2. **If the team's goal is "capture all IDE-AI traffic going forward, minimal lift":** Helicone (OSS/Apache-2.0 self-host) is the strongest single recommendation for the proxy axis. Langfuse is the strongest if first-class Claude Code support and richer dataset/eval features matter more than zero-code capture.

3. **If the goal includes "ingest the existing SpecStory-style archive":** Phoenix is the only platform with a documented, community-validated path. Langfuse and Opik can do it via SDK/REST replay but no turnkey adapter.

4. **A hybrid is plausible and probably superior**: SpecStory-style harvester for IDE-side artifacts (covers free-tier Cursor chats, .specstory files, etc.) + Helicone/Langfuse for forward API-side capture (covers Claude Code via OTEL/proxy and any tool routing through proxy). Two pipelines, one unified backend (Langfuse with custom adapter, or Phoenix with documented import). This combines Bucket-A and Bucket-C strengths.

5. **License-and-control axis ranking for self-hosted internal store**: Apache-2.0 OSS leaders (Phoenix, Opik, Helicone, Laminar, Lunary) > MIT-with-EE (Langfuse) > Closed-source-with-self-host-tier (LangSmith Enterprise, Braintrust, HoneyHive, W&B). For a "we own the data" architecture, the Apache-2.0 group is preferable.

6. **Search/dataset story matters for the "RAG re-injection" requirement.** If the end-state is searchable + queryable + re-injectable conversation history, Braintrust (closed, but BTQL/SQL is unmatched) and Langfuse (open, with Datasets API) are the two strongest. Helicone's search is improving but trails. Phoenix's pandas-export model is great for data scientists but heavier for engineers wanting a quick query.

7. **Recommend explicitly noting in the comparables analysis** that none of these platforms offers a turnkey replacement for SpecStory's IDE-archive scrape — they are complementary, not competitive, in the architectural sense even though they share the end-state goal.
