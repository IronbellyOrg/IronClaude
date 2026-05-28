# Research: AI agent memory layer products

**Topic:** Persistent memory / RAG-over-conversation backends
**Status:** Complete
**Date:** 2026-05-01

---

## Mem0

- **Positioning:** "Universal memory layer" for LLM apps — extracts, stores, and retrieves user/agent memories from conversations; positioned as a self-improving memory store with optional graph layer.
- **Sources:** https://mem0.ai, https://docs.mem0.ai/introduction, https://github.com/mem0ai/mem0, https://mem0.ai/pricing
- **Reliability:** Official + Repo
- **Relevance:** HIGH
- **Abstraction model:** Hybrid — core is memory-record (LLM-extracted "facts" from messages) backed by vector store; optional graph memory layer (Neo4j/Memgraph integration).
- **Ingestion API:** Both. Primary API is `memory.add(messages, user_id=...)` accepting an arbitrary list of role/content messages — meaning historical transcripts CAN be batch-ingested by simply chunking and POSTing them. There is no requirement for the LLM call to be routed through Mem0; it is a pure memory CRUD service. Live use also supported via async `add` after each turn.
- **Self-host:** Yes. Apache-2.0. Self-host stack includes REST server, OSS SDK, and OpenMemory dashboard. Cloud uses an enterprise-on-prem path for hosted parity.
- **Multi-tenant:** Yes via `user_id` / `agent_id` / `run_id` / `app_id` scoping. Pro tier adds "multiple projects". No per-seat team RBAC documented in standard tiers (Enterprise adds SSO/audit logs).
- **Pricing:** Hobby free (10k adds, 1k retrievals/mo); Starter $19/mo (50k/5k); Pro $249/mo (500k/50k, multi-project, Slack, analytics); Enterprise custom (unlimited, SSO, on-prem). 3-month free Pro for startups.
- **IDE integration:** No first-party IDE plug-in. Integrates via SDKs (Python, TS) inside any agent framework (LangChain, CrewAI, Vercel AI SDK, AutoGen, LlamaIndex). Has an MCP server option (OpenMemory MCP) — the closest path to IDE injection.
- **Activity signal:** ~54.5k GitHub stars; very active.
- **Production users:** Mem0 markets "Zero-ops production use" but no named logos visible on the homepage snippet pulled; site lists customer testimonials in marketing pages. Widely cited in agent-framework tutorials.
- **Critical fit:** STRONG. Because `add()` accepts arbitrary message arrays, captured Cursor / Claude Code / SpecStory transcripts can be replayed into Mem0 in batch as historical memory. No instrumentation of the live LLM call is required. This is the cleanest "BYO memory" candidate among hosted options.

## Letta (formerly MemGPT)

- **Positioning:** Stateful-agent platform with hierarchical memory ("MemFS"-style). Less a passive memory store, more a full agent runtime where memory is a first-class agent attribute.
- **Sources:** https://www.letta.com, https://docs.letta.com/concepts/memory-management, https://docs.letta.com/guides/agents/architectures/memgpt, https://github.com/letta-ai/letta
- **Reliability:** Official + Repo
- **Relevance:** MEDIUM
- **Abstraction model:** Hybrid — structured `memory_blocks` (e.g., `human`, `persona`) inside an agent, plus archival vector memory for overflow + recall search.
- **Ingestion API:** Primarily live. Letta's design is "send messages to the agent, it manages memory itself." There is no first-class "import 50,000 historical messages as memory" API in the public surface; you would have to send them as agent messages or use the Sources/archival APIs. This makes batch-replay of captured transcripts awkward and expensive (each replay invokes the agent loop).
- **Self-host:** Yes. Apache-2.0. Docker/compose available; Letta Code SDK runs locally; managed cloud also exists.
- **Multi-tenant:** Letta Cloud has org/project scoping; OSS version is single-instance and you would shard agents per user.
- **Pricing:** Open-source free; Letta Cloud pricing not on the page snippet pulled — third-party reports indicate a free tier + usage-based paid plan. Enterprise via sales.
- **IDE integration:** No first-party IDE plug-in. Integrates via REST/Python/TS SDKs. Letta Code is a terminal-based agent (similar to Claude Code itself).
- **Activity signal:** ~22.4k GitHub stars, very active.
- **Production users:** No prominent named logos in fetched content; widely cited in academic/agent-memory literature (origin: MemGPT paper, UC Berkeley).
- **Critical fit:** WEAK-to-MEDIUM. Letta is an agent framework with memory built in, not a memory CRUD service. Replaying captured transcripts requires either (a) instantiating an agent and feeding messages, which mutates state through the agent loop, or (b) using archival sources (file/document upload) which discards turn structure. Not a natural fit for "ingest captured chats as RAG corpus."

## Zep (Cloud)

- **Positioning:** Managed "context engineering platform" — a hosted Graph RAG memory layer with temporal knowledge graph (built on Graphiti), explicitly marketed for agent context unification across chat + business data + behavior.
- **Sources:** https://www.getzep.com/, https://www.getzep.com/pricing/, https://www.getzep.com/product/open-source, https://arxiv.org/abs/2501.13956
- **Reliability:** Official
- **Relevance:** HIGH
- **Abstraction model:** Hybrid — temporal knowledge graph (entities, relationships, fact invalidation with time validity) plus vector retrieval over messages/documents. Graph-RAG positioning.
- **Ingestion API:** Both. Zep accepts chat messages, JSON business data, and documents via REST API. Historical chat transcripts can be ingested via the `messages.add` / `graph.add` endpoints — there is no requirement that the live LLM call route through Zep. Live mode also supported; SDKs intended to wrap conversation turns.
- **Self-host:** Cloud OSS (the original "Zep OSS" v1) was deprecated in favor of Graphiti as the OSS path. Today: Zep cloud is managed; full self-host = Graphiti (see next entry). Enterprise tier offers BYOC (your AWS VPC) and BYOK/BYOM deployment.
- **Multi-tenant:** Yes via users / sessions / threads. Enterprise plan adds team features, SSO, dedicated AM.
- **Pricing:** Free Starter (1k credits/mo); Flex $125/mo (50k credits); Flex Plus $375/mo (200k credits); Enterprise custom. Credit-based, no per-seat published.
- **IDE integration:** No first-party IDE plug-in; SDKs (Python/TS/Go) for embedding in any agent.
- **Activity signal:** Zep cloud is closed-source; OSS surface is Graphiti.
- **Production users:** Named logos: AWS, Writer, Swiggy, Torq, AlphaSignal, Flockx, Axtria. SOC2 Type II + HIPAA claimed.
- **Critical fit:** STRONG. Zep's API is explicitly designed to ingest conversation history as data, not require LLM-call routing. The temporal graph model is well-suited to "engineer-AI conversation history with time-aware fact invalidation." Strongest hosted candidate alongside Mem0 for ingesting `.specstory/history/` style archives.

## Graphiti (Zep OSS)

- **Positioning:** Open-source Python framework for building temporal knowledge graphs from streaming or batch episodes. The OSS core powering Zep's hosted product.
- **Sources:** https://github.com/getzep/graphiti, https://www.getzep.com/product/open-source
- **Reliability:** Official + Repo
- **Relevance:** HIGH
- **Abstraction model:** Temporal knowledge graph (Neo4j or FalkorDB backend) with bi-temporal validity, entity/relation extraction via LLM, hybrid semantic + BM25 + graph traversal retrieval.
- **Ingestion API:** Batch and incremental. The `add_episode` / `add_episode_bulk` API accepts arbitrary text or structured JSON episodes with a reference timestamp — perfect for replaying a `.specstory/history/` archive. Each episode is processed for entity extraction and graph update; no LLM-call instrumentation required.
- **Self-host:** Yes; self-host is the only deployment model. Apache-2.0. Requires Neo4j or FalkorDB and an LLM provider for extraction.
- **Multi-tenant:** Group-id scoping (`group_id` per episode). Logical multi-tenancy via group partitioning rather than physical isolation.
- **Pricing:** Free OSS. LLM extraction costs (OpenAI/Anthropic) and Neo4j hosting costs apply.
- **IDE integration:** None natively; consumed via Python SDK. Available as MCP server (third-party `graphiti-mcp` references exist).
- **Activity signal:** ~25.6k GitHub stars, 825+ commits, very active (2025-2026).
- **Production users:** Powers Zep cloud (which lists the AWS/Writer/Swiggy logos above).
- **Critical fit:** EXCELLENT for self-host BYO. The `add_episode_bulk` API and time-aware ingestion match the captured-transcript replay use case almost exactly. Strongest OSS candidate for the storage+retrieval layer in a SpecStory-style ingestion pipeline.

## Cognee

- **Positioning:** "AI memory engine" — open-source library that builds a hybrid vector + knowledge graph memory from arbitrary input data. Focus on deep ETL pipelines (cognify → memify) over heterogeneous content.
- **Sources:** https://www.cognee.ai/, https://www.cognee.ai/pricing, https://docs.cognee.ai/api-reference, https://github.com/topoteretes/cognee
- **Reliability:** Official + Repo
- **Relevance:** HIGH
- **Abstraction model:** Hybrid (vector + knowledge graph). LLM-driven entity extraction; plugin model for graph backends (Neo4j, Kuzu, etc.) and vector stores (LanceDB, Qdrant, etc.).
- **Ingestion API:** Both. Cognee's `add()` accepts strings, files, URLs, or directories — explicitly supports bulk ingestion of existing data, "any format or structure". Pipeline runs `cognify` to build the graph + embeddings. Live agent loops can also call `add()` per-turn but it is not the primary use case.
- **Self-host:** Yes. Apache-2.0. Multiple deploy paths (Modal, Railway, Fly.io, Render, Daytona); also runs locally.
- **Multi-tenant:** Yes — explicit "user/tenant isolation" in feature list.
- **Pricing:** Free OSS; Cloud Developer $35/mo (1k docs / 1 GB / 1 user); Cloud Team $200/mo (2.5k docs / 2 GB / 10 users); On-Prem Enterprise custom. Top-up packs for cloud (e.g., +1k docs $35).
- **IDE integration:** No first-party IDE plug-in; consumed via Python SDK or REST API. MCP server exists in repo.
- **Activity signal:** ~17k GitHub stars, 7,000+ commits, very active.
- **Production users:** Not prominently listed in the snapshot pulled.
- **Critical fit:** STRONG. Bulk ingestion of arbitrary text/files is a first-class capability — captured `.specstory/history/` Markdown can be passed directly to `cognee.add()`. Heavier-weight than Mem0/Graphiti due to broader "any data" ETL scope, but fits the BYO replay model cleanly.

## LangMem (LangChain)

- **Positioning:** Python library for adding long-term memory and prompt optimization to LangGraph agents. Not a managed service — sits on top of LangGraph's `BaseStore`.
- **Sources:** https://langchain-ai.github.io/langmem/, https://github.com/langchain-ai/langmem, https://docs.langchain.com/oss/python/langgraph/add-memory
- **Reliability:** Official + Repo
- **Relevance:** MEDIUM
- **Abstraction model:** Memory record (LLM-extracted facts) backed by any LangGraph store (InMemoryStore, AsyncPostgresStore, etc.). Supports semantic search over stored memories.
- **Ingestion API:** Library. `create_memory_manager` and `create_memory_store_manager` extract memories from message lists — so historical transcripts CAN be processed in batch by feeding them through the manager. Requires running LangGraph + an LLM to do extraction. No first-party hosted ingest API.
- **Self-host:** Yes (always). MIT license. Ships as a Python package; backend is whatever store you wire up.
- **Multi-tenant:** Implementation-defined (use namespace tuples in `BaseStore`); LangGraph's store API supports per-user/per-org partitioning.
- **Pricing:** Free OSS. LangSmith / LangGraph Cloud have separate paid plans if you use the hosted runtime.
- **IDE integration:** None first-party; consumed via Python.
- **Activity signal:** ~1.4k GitHub stars, 119 commits — niche compared to Mem0/Graphiti/Cognee.
- **Production users:** Not prominently listed; LangChain ecosystem adoption applies broadly.
- **Critical fit:** MEDIUM. Capable of batch-processing transcripts but only as part of a LangGraph stack, and requires LLM extraction passes. Useful as a building block for a custom solution if you are already on LangGraph; less compelling as a standalone product choice.

## SuperMemory

- **Positioning:** "Memory and context engine for AI" — managed memory layer with strong IDE-coding-tool integration story (Cursor, Windsurf, VS Code, Claude Code listed as supported clients).
- **Sources:** https://supermemory.ai, https://docs.supermemory.ai/overview/why-supermemory, https://supermemory.ai/pricing, https://github.com/supermemoryai/supermemory, https://github.com/supermemoryai/supermemory-mcp
- **Reliability:** Official + Repo
- **Relevance:** HIGH
- **Abstraction model:** Hybrid (RAG + memory in single query, "persistent memory graph" UX). Vector-based retrieval with graph overlay for entities.
- **Ingestion API:** Live + arbitrary. `client.add()` accepts text, conversations, URLs, HTML — meaning conversation transcripts can be batch-uploaded. Dedicated batch endpoint not explicitly documented in the page snippet but the per-item add is unrestricted.
- **Self-host:** Partial. Core repo is MIT-licensed and the MCP server is OSS; the full managed pipeline (queries, dashboard, plugins) is the paid hosted product. Self-host of the complete stack is less polished than Mem0/Cognee.
- **Multi-tenant:** Plans advertise "unlimited users" across all tiers; multi-user organisation features in Scale/Enterprise.
- **Pricing:** Free $0 (1M tokens/mo, 10k queries); Pro $19/mo (3M tokens, 100k queries); Scale $399/mo (80M tokens, 20M queries); Enterprise custom.
- **IDE integration:** STRONG — explicitly lists Cursor, Windsurf, VS Code, Claude Code as supported clients via MCP and plugins. This is unique among memory-layer products.
- **Activity signal:** ~22.4k GitHub stars on main repo, 1,539 commits, very active.
- **Production users:** Indie/SMB-heavy positioning; specific enterprise logos not enumerated.
- **Critical fit:** STRONG for IDE-side. The first-party Cursor/Claude-Code MCP integration plus arbitrary-content ingestion makes it the closest off-the-shelf product to the SpecStory + RAG vision. The trade-off vs Mem0/Zep is that the OSS surface is narrower; full feature parity requires the hosted plan.

## Mastra Memory

- **Positioning:** Memory module of Mastra, a TypeScript-first agent framework. Not a standalone memory product — bundled with the agent runtime.
- **Sources:** https://mastra.ai/docs/storage/overview, https://mastra.ai/blog/agent-memory-guide, https://mastra.ai/reference/memory/Memory
- **Reliability:** Official
- **Relevance:** LOW-MEDIUM
- **Abstraction model:** Working memory (recent thread context) + semantic recall (vector search over past interactions). Storage abstraction over LibSQL/Postgres/Upstash/MongoDB.
- **Ingestion API:** Live-oriented. Memory accumulates as the agent processes messages; messages are stored by thread/resource ID. Bulk ingestion of historical transcripts is not a first-class API surface.
- **Self-host:** Yes; OSS framework (license not stated on snippet but the repo is publicly accessible). Mastra Cloud is the managed offering.
- **Multi-tenant:** Via thread/resource keys.
- **Pricing:** Framework free; Mastra Cloud has separate hosted pricing (not extracted here).
- **IDE integration:** None first-party.
- **Activity signal:** Active TypeScript repo; smaller footprint than Mem0/Graphiti.
- **Production users:** Not enumerated.
- **Critical fit:** WEAK for our use case. Coupled to the Mastra agent framework. Better suited to teams already building TypeScript agents on Mastra; not a natural fit for ingesting captured `.specstory/history/` archives independently.

## Basic Memory MCP

- **Positioning:** Local-first MCP server that turns a folder of Markdown notes into an MCP-accessible knowledge base for AI tools. Tool-side, not a true memory layer for agent runtimes.
- **Sources:** https://docs.basicmemory.com/, https://mcp.directory/servers/basic-memory
- **Reliability:** Official + Directory
- **Relevance:** MEDIUM
- **Abstraction model:** Markdown files + semantic graph derived from internal links. Local SQLite DB for indexing.
- **Ingestion API:** Filesystem. You write Markdown into a watched folder; the server indexes it. Captured chat transcripts can be transformed to Markdown and dropped in — straightforward batch ingest.
- **Self-host:** Local-only by default; cloud option with sync. "Fully open source" (specific license not visible on the page).
- **Multi-tenant:** Not described; designed for individual use.
- **Pricing:** Free OSS; cloud sync may have separate pricing.
- **IDE integration:** Yes — MCP-native, so works with any MCP client (Claude Desktop, Cursor, Claude Code).
- **Activity signal:** Smaller footprint; no exact star count from snippet.
- **Production users:** Individual/personal-knowledge use case.
- **Critical fit:** MEDIUM. Good for individual engineers wanting AI-tool access to their own captured chats, weak for team-scale unified context with multi-user retrieval and ranking.

## Adjacent products surveyed (low-relevance)

- **Context.ai** — Originally an LLM analytics product (not a memory layer); brand has shifted to enterprise workflows. Not a fit.
- **Helicone Mem** — No standalone "memory" product found; Helicone is an LLM observability/proxy. Could *enable* live capture if calls route through it, but is not a memory-retrieval layer.
- **Arcade.dev** — MCP runtime / tool-calling platform; not a memory layer.
- **Rememberall** — Niche/early-stage long-term memory product; no production track record visible.
- **OpenAI Agents SDK Memory** — In-framework memory primitives, not a standalone product.
- **Cloudflare Agent Memory** — Edge-runtime memory primitive, not a captured-transcript ingest target.

## Memory-Layer Comparison Table

| Product | Model | Ingestion | Self-host | Team | Price | IDE | Captured-chat fit |
|---|---|---|---|---|---|---|---|
| Mem0 | Hybrid (record + vector + opt graph) | Batch + live via `add(messages)` | Yes (Apache-2.0) | user/agent/project scoping | Free / $19 / $249 / Ent | MCP (OpenMemory) | STRONG |
| Letta (MemGPT) | Hybrid (memory_blocks + archival) | Live agent loop only | Yes (Apache-2.0) | Cloud orgs/projects | OSS free; Cloud usage | None | WEAK-MEDIUM |
| Zep Cloud | Temporal knowledge graph + vectors | Batch + live | Enterprise BYOC only | users/sessions/threads | Free / $125 / $375 / Ent | None | STRONG |
| Graphiti (Zep OSS) | Temporal KG (Neo4j/FalkorDB) | `add_episode_bulk` batch + incremental | Yes (Apache-2.0) | group_id partition | Free OSS | MCP (third-party) | EXCELLENT |
| Cognee | Hybrid (vector + KG) | Bulk `add()` over files/text/URLs | Yes (Apache-2.0) | tenant isolation | Free / $35 / $200 / Ent | MCP server | STRONG |
| LangMem | Memory record over LangGraph store | Library batch via memory manager | Yes (MIT) | namespace tuples | Free OSS | None | MEDIUM |
| SuperMemory | Hybrid (RAG + memory graph) | Arbitrary `add()` | Partial (MCP OSS) | unlimited users | Free / $19 / $399 / Ent | Cursor / Claude Code / VSCode / Windsurf | STRONG |
| Mastra Memory | Working memory + semantic recall | Live agent calls | Yes (OSS framework) | thread/resource | Framework free | None | WEAK |
| Basic Memory MCP | Markdown + link graph | Filesystem drop | Yes (OSS, local) | Single user | Free | MCP-native | MEDIUM |

## Key External Findings

- The market splits cleanly into two architectures: **memory-record + vector** (Mem0, LangMem, Mastra) and **temporal knowledge graph** (Graphiti, Zep, Cognee). SuperMemory straddles both. The KG approaches add bi-temporal fact validity, which matters for engineering conversations where decisions and facts evolve.
- **Batch ingestion of arbitrary transcripts is supported by most products as a side effect of an open `add()` API** (Mem0, Graphiti, Cognee, SuperMemory, Zep). The exception is Letta, which is agent-loop-centric and does not expose a clean replay path.
- **No memory-layer product *requires* LLM-call routing through itself.** They all sit beside the LLM rather than as a proxy. This is the opposite of observability tools (Helicone) and means captured-transcript ingestion is architecturally available across the field.
- **OSS licensing is permissive across the field**: Apache-2.0 (Mem0, Letta, Graphiti, Cognee) or MIT (LangMem, SuperMemory). Self-host is viable for all major candidates.
- **IDE integration is rare**: SuperMemory is the standout with first-party Cursor / Claude Code / VS Code / Windsurf support. Most others rely on generic MCP server adapters or framework SDKs.
- **Activity ranking by stars** (rough proxy for ecosystem momentum): Mem0 (54.5k) > Graphiti (25.6k) > Letta (22.4k) ≈ SuperMemory (22.4k) > Cognee (17k) > LangMem (1.4k).
- **Pricing is credit / quota-based**, not seat-based, across hosted offerings — favourable for small-team adoption since unlimited users are typical.
- **Graphiti's `add_episode_bulk` API is the cleanest direct match** for replaying timestamped historical conversations into a queryable temporal graph; this is the single most precise architectural fit for the SpecStory-style ingestion use case.

## Recommendations from External Research

1. **For BYO storage+retrieval layer in a SpecStory-style architecture, the top three are Graphiti (OSS), Mem0 (OSS or hosted), and Zep (hosted).** All three accept arbitrary message arrays / episodes via API and do not require LLM-call instrumentation. Graphiti wins on temporal-graph fidelity for engineering decision history; Mem0 wins on simplicity and ecosystem adoption; Zep wins on managed enterprise readiness.
2. **For complete adoption (skip BYO entirely), SuperMemory is the only product with a mature multi-IDE integration story today.** Trade-off: less OSS surface and less polished self-host than Mem0/Graphiti. Worth a serious bake-off if integration UX dominates the requirements.
3. **Letta and Mastra are agent runtimes with bundled memory, not memory layers.** Exclude them from the storage+retrieval bake-off unless the team is also adopting the underlying agent framework.
4. **LangMem is a building block, not a product choice.** Useful inside a custom LangGraph implementation; does not stand alone as a memory backend.
5. **Basic Memory MCP is a useful low-effort first-pass option for individual engineers** (drop captured chat as Markdown, expose via MCP). Not a team-scale solution but a good interim or fallback.
6. **The architectural posture of the comparable set strongly validates SpecStory's "capture then ingest" design.** Every credible memory-layer product treats ingestion as data-shaped, not call-shaped — meaning a SpecStory-style capture pipeline can compose with any of them, and the choice becomes about retrieval quality, graph richness, and integration UX rather than capture mechanics.
7. **Recommended bake-off shortlist for the engineering-team unified-context architecture:** Graphiti (OSS, self-host) and Mem0 (managed or self-host) as primary candidates; Zep cloud as enterprise-managed alternative; SuperMemory as wildcard if first-party IDE integration is a hard requirement.

---

**Status:** Complete
