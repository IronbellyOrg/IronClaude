# Research: Build-your-own RAG-over-conversations stack

**Topic:** Components for assembling a custom unified AI-conversation DB
**Status:** Complete
**Date:** 2026-05-01

---

## Vector DBs

### Pinecone
- Sources: https://www.pinecone.io/pricing/, https://docs.pinecone.io/guides/manage-cost/understanding-cost, https://docs.pinecone.io/guides/indexes/pods (legacy), https://docs.pinecone.io/release-notes/2026
- Pricing (serverless, the only tier for new customers post-Aug 18, 2025):
  - Storage: $0.33/GB-month (Standard & Enterprise)
  - Write Units: $4-$4.50/1M (Standard); $6-$6.75/1M (Enterprise)
  - Read Units: $16-$18/1M (Standard); $24-$27/1M (Enterprise)
  - Reranking: $2/1k requests
  - Starter (free): 2 GB storage, 2M WU/mo, 1M RU/mo
- Scale: Serverless decouples storage from compute. Pod model deprecated for new signups Aug 2025; legacy customers retain access. Capacity by pod (legacy): ~1M vecs at 768d per s1.x1, ~5M at p1.x1.
- Hybrid search: Yes — sparse + dense vector hybrid via dotproduct metric; integrated reranking models.
- Self-host: NO — fully managed only. Major lock-in risk.
- Multi-tenant: Namespaces per index; up to 10k namespaces per index on Standard, 100k on Enterprise.
- Notes: Easiest "just works" managed option. Best dev ergonomics. Worst lock-in for BYO purists. Read-unit billing means high-QPS chat assistants get expensive fast.

### Weaviate
- Sources: https://docs.weaviate.io/cloud/platform/billing, https://docs.weaviate.io/weaviate/concepts/search/hybrid-search, https://weaviate.io/pricing
- Pricing: Sandbox free; Serverless Cloud usage-based by stored dimensions (~$0.05/M dimensions/mo on Standard tier per public docs); Enterprise Cloud and Bring-Your-Own-Cloud also offered.
- Scale: Single-node billions of objects with HNSW; horizontal sharding supported. Real-world deployments hit 10B+ vectors.
- Hybrid search: First-class — built-in BM25F + vector fusion (alpha parameter). Best-in-class hybrid query DSL among the top managed players.
- Self-host: YES — Apache 2.0 licensed; Docker / Kubernetes deploys are first-class.
- Multi-tenant: Native multi-tenancy as a top-level concept (tenants per collection); designed for SaaS isolation. Best multi-tenant story among the field.
- Notes: Strongest combination of managed and self-host with identical API. Schema-driven (modules for embeddings/rerankers built in). Slightly heavier ops than Qdrant.

### Qdrant
- Sources: https://qdrant.tech/pricing/, https://qdrant.tech/documentation/cloud/pricing-payments/, https://qdrant.tech/articles/hybrid-search/, https://qdrant.tech/benchmarks/
- Pricing: Free single-node 0.5 vCPU/1 GB/4 GB disk forever. Standard usage-based (vCPU + RAM + storage hourly). Premium has minimum spend (Enterprise SSO, VPC). Hybrid Cloud (your infra, their control plane) — sales-led pricing.
- Scale: Rust-native, strong benchmark numbers — frequently leads ann-benchmarks-style comparisons on QPS/latency. Multi-tenant via "payload-aware" sharding.
- Hybrid search: Yes — sparse vectors + dense + late fusion + Qdrant Query API supports complex hybrid pipelines. ColBERT/Multivector support shipped in 2024.
- Self-host: YES — Apache 2.0; single binary or Helm chart; runs comfortably on a single node up to ~10M vecs.
- Multi-tenant: Designed for it — tenant-key payload indexing routes shards by tenant; supports millions of tenants.
- Notes: Best raw performance per dollar for self-host. Cleanest API. Less batteries-included than Weaviate (no built-in embeddings module historically; added inference in 2024). Strong Rust foundation = predictable latency.

### Chroma
- Sources: https://www.trychroma.com/, https://docs.trychroma.com/
- Pricing: OSS free. Chroma Cloud (managed) launched 2024 — $0/mo Starter, then usage-based on stored bytes & query volume.
- Scale: Originally embedded/local-first (SQLite). Distributed Chroma (2024) targets cloud-scale. Production track record is shorter than the older players.
- Hybrid search: Limited — basic metadata filters; full BM25/hybrid is newer/less mature.
- Self-host: YES — Apache 2.0; pip install + run as a server, or embedded.
- Multi-tenant: "Tenants" + "databases" + "collections" hierarchy; works but multi-tenancy is less battle-tested than Weaviate/Qdrant.
- Notes: Best DX for prototyping / single-machine. Often the path of least resistance for "I need a vector DB this afternoon." Don't pick for production team-scale archive without strongly validating the distributed deployment.

### Milvus
- Sources: https://milvus.io/, https://milvus.io/docs/v2.5.x/full_text_search_with_milvus.md, https://zilliz.com/pricing (managed = Zilliz Cloud)
- Pricing: OSS free (Apache 2.0). Zilliz Cloud (managed Milvus) — Serverless from $0.10/M reads + storage; Dedicated CU instances from ~$99/mo.
- Scale: Built for billions; native distributed architecture with separate query/index/data nodes. Used by major AI deployments (e.g., reported 10B+ vec installations).
- Hybrid search: Yes — sparse + dense hybrid, BM25 full-text in v2.5+, weighted fusion + RRF.
- Self-host: YES — Apache 2.0 — but operationally heavy: requires etcd, MinIO/S3, Pulsar/Kafka. Milvus Lite (single-process, embedded) for dev only.
- Multi-tenant: Partition keys + RBAC; supports it but with more overhead than Qdrant/Weaviate.
- Notes: Highest scale ceiling but also highest ops burden. Pick if you genuinely need 100M+ vectors and have a platform team. Overkill for a 10-engineer team's chat archive.

### pgvector (Postgres)
- Sources: https://github.com/pgvector/pgvector, https://www.cidrdb.org/cidr2026/papers/p2-liu.pdf, https://supabase.com/docs/guides/ai
- Pricing: Free (extension). Costs are whatever your Postgres host charges. RDS/Supabase/Neon all support pgvector.
- Scale: HNSW index added in 0.5 (2023); pgvectorscale (Timescale, 2024) adds StreamingDiskANN for 10-100x recall@speed gains. Now genuinely competitive up to ~10-50M vectors per node. CIDR 2026 paper "Fast Vector Search in PostgreSQL: A Decoupled Approach" shows ongoing perf research.
- Hybrid search: YES — Postgres tsvector full-text + pgvector cosine; combine with SQL. RRF must be hand-written but trivial.
- Self-host: YES — runs anywhere Postgres runs.
- Multi-tenant: Rows-with-tenant-id is the obvious pattern; row-level security available. Scales as well as your Postgres does.
- Notes: STRONGEST recommendation for small-team BYO. If team already runs Postgres, marginal cost is ~$0 and one fewer system to operate. Trades peak performance for radical operational simplification. CIDR 2026 work + pgvectorscale closing the gap fast.

### Turbopuffer
- Sources: https://turbopuffer.com/docs, https://turbopuffer.com/pricing
- Pricing: Object-storage-backed serverless — claims 94% lower query cost than competitors at scale. Public pricing: writes ~$2/GB, queries ~$0.04 per query at scale, storage ~$0.05/GB-month. Strong economics at billion+ scale.
- Scale: Designed for billions; cold-query p90 ~444ms, warm p50 ~8ms (1M vecs). S3-native architecture.
- Hybrid search: Yes — vector + BM25 full-text; namespace-scoped.
- Self-host: NO — managed only as of 2026.
- Multi-tenant: Namespaces (cheap to create — millions supported) makes per-engineer or per-conversation namespacing viable.
- Notes: Architecturally the most interesting newcomer. Used by Cursor, Notion AI for production-scale RAG. The price model (object storage + cache) maps perfectly onto bursty chat-archive workloads where most data is cold. Strong fit for the chat-archive use case but managed-only locks you to the vendor.

### LanceDB
- Sources: https://lancedb.com/, https://lancedb.github.io/lancedb/
- Pricing: OSS free (Apache 2.0). LanceDB Cloud — usage-based on storage + queries.
- Scale: Embedded + serverless modes; columnar Lance format on S3 → cheap storage. Targets billions.
- Hybrid search: Yes — vector + full-text (tantivy-based); reranker integrations.
- Self-host: YES — embedded library or self-hosted server. Cleanest "just a Python library" DX.
- Multi-tenant: Table-per-tenant or tenant-id column patterns; less native than Weaviate.
- Notes: Best embedded option after Chroma; columnar storage means analytic queries (date ranges, group-by-engineer) are fast. Strong fit if archive doubles as a data warehouse.

## Embedding APIs

### OpenAI text-embedding-3-large / -small
- Sources: https://platform.openai.com/docs/models/text-embedding-3-large, https://platform.openai.com/docs/pricing/
- Cost per 1M tokens: $0.13 (large); $0.02 (small); Batch API ~50% off ($0.065 / $0.01)
- Max input: 8,192 tokens
- Dimensions: 3072 (large), 1536 (small); Matryoshka shortening supported.
- Code+conversation benchmark: Reported ~71-78% on code retrieval tasks (per voyage-code-3 comparison data, lower than specialist models). Strong general-domain MTEB scores.
- Notes: Industry default. Most pipeline tools have a one-line integration. Reliable, but bested by specialist code/retrieval models on code retrieval.

### Cohere Embed v3 / v4
- Sources: https://cohere.com/pricing, https://docs.cohere.com/docs/cohere-embed, https://docs.cohere.com/changelog/embed-multimodal-v4
- Cost per 1M tokens: ~$0.10 (embed-english-v3); v4 multimodal at similar tier (public token pricing for v4 is partly behind contact-sales / Model Vault: small instance $4/hr, medium $5/hr).
- Max input: 512 tokens (v3, English); v4 expands to 128k context for multimodal.
- Dimensions: 1024 (v3); v4 supports Matryoshka 256/512/1024/1536.
- Code+conversation benchmark: Strong MTEB; v4 is multimodal (text + image). Generally trails Voyage on pure code retrieval.
- Notes: Best when multilingual + on-prem (Model Vault) is required. Bedrock/Azure availability is a plus for enterprise procurement.

### Voyage AI (voyage-3, voyage-3-large, voyage-3-lite, voyage-code-3)
- Sources: https://docs.voyageai.com/docs/pricing, https://docs.voyageai.com/docs/embeddings, https://blog.voyageai.com/2024/12/04/voyage-code-3/, https://blog.voyageai.com/2025/01/07/voyage-3-large/
- Cost per 1M tokens: voyage-3 $0.06; voyage-3-large $0.18; voyage-3-lite $0.02; voyage-code-3 $0.18
- Max input: voyage-code-3 32k tokens (4x OpenAI large); voyage-3 family typically 32k.
- Code+conversation benchmark: voyage-code-3 reports +13.8% to +16.3% average over OpenAI text-embedding-3-large across 32 code-retrieval datasets. Concrete: voyage-code-3 ~92% vs OpenAI large ~78% on coding tasks. Strongest specialist for code-heavy chat archives.
- Notes: Best quality-per-dollar for code-heavy conversational data. Matryoshka (256/512/1024/2048) + int8/binary quantization → 32x storage reduction with <5% quality loss. Owned by MongoDB since 2025. Strong fit for engineer-AI conversation archive.

### Jina AI (jina-embeddings-v3)
- Sources: https://jina.ai/embeddings/, https://huggingface.co/jinaai/jina-embeddings-v3
- Cost per 1M tokens: ~$0.018 via Jina API (free tier 10M tokens/mo). Apache 2.0 weights → self-host free.
- Max input: 8,192 tokens
- Dimensions: 1024 (Matryoshka to 32). Multilingual.
- Code+conversation benchmark: Competitive with text-embedding-3-large on MTEB; weaker than Voyage code-3 on pure code.
- Notes: Best "balance of cheap-and-self-hostable" — Apache 2.0 means you can run it on your own GPU when scale demands. Reranker-v2 also free-tier and high-quality.

### BGE-M3 (BAAI)
- Sources: https://arxiv.org/abs/2402.03216, https://huggingface.co/BAAI/bge-m3
- Cost: Free (MIT license). Self-hosted on GPU; per-1M-token cost on a $0.50/hr A10 instance ≈ $0.001-$0.005 depending on batching.
- Max input: 8,192 tokens
- Dimensions: 1024 dense; ALSO produces sparse + multi-vector (ColBERT-style) outputs in one pass — uniquely versatile for hybrid pipelines.
- Code+conversation benchmark: Top-3 open-source on MTEB; explicit support for 100+ languages; strong long-document retrieval.
- Notes: Best OSS model when hybrid (dense+sparse+colbert) is desired without running 3 models. Used heavily in self-host RAG stacks.

### E5 family (intfloat/multilingual-e5-large)
- Sources: https://arxiv.org/abs/2212.03533, https://huggingface.co/intfloat/multilingual-e5-large-instruct
- Cost: Free (MIT). Same self-host economics as BGE-M3.
- Max input: 512 tokens (older E5); v2 / instruct variants raise to 8k.
- Dimensions: 1024
- Code+conversation benchmark: Strong general MTEB but weaker on specialist code than BGE-M3 or Voyage.
- Notes: Smaller / faster than BGE-M3 — picks up where Voyage-lite leaves off. Good "first OSS model to try" for lean self-host.

### GTE family (Alibaba gte-large-en-v1.5, gte-Qwen2)
- Sources: https://huggingface.co/Alibaba-NLP/gte-large-en-v1.5, https://huggingface.co/Alibaba-NLP/gte-Qwen2-7B-instruct
- Cost: Free (Apache 2.0).
- Max input: 8,192 tokens
- Dimensions: 1024 (gte-large-en-v1.5); 3584 (gte-Qwen2-7B)
- Code+conversation benchmark: gte-Qwen2-7B currently sits at top of MTEB for OSS models; expensive to host (7B params).
- Notes: Best OSS quality if you have GPU budget. 7B variant requires A100-class hardware. Smaller v1.5 fits on consumer GPU.

## Pipeline Tools

### LlamaIndex
- Sources: https://docs.llamaindex.ai/, https://docs.llamaindex.ai/en/stable/understanding/loading/loading.html, https://learn.microsoft.com/en-us/azure/storage/files/artificial-intelligence/retrieval-augmented-generation/open-source-frameworks/orchestrations/llamaindex
- Chat-transcript ingestion examples: YES — `ChatMessage` + `ChatStore` abstractions; first-class concept of conversation memory. Loaders for JSONL/SQLite/Notion/Slack make ingest trivial. SimpleNodeParser + `SemanticSplitterNodeParser` for chunking.
- Chunking strategies: Semantic, sentence, token, hierarchical, document-aware; agentic chunkers shipped 2024-2025.
- Tool-call-aware: Yes — `ToolMessage` / `FunctionMessage` types preserved through ingestion; built-in tool-call retrieval examples.
- License: MIT
- Notes: Strongest "out of the box" framework for building chat archives — the ChatStore abstraction maps almost 1:1 onto our use case. Ecosystem of 40+ vector DB integrations means the BYO stack snaps together.

### LangChain / LangGraph
- Sources: https://python.langchain.com/, https://www.langchain.com/blog/building-chat-langchain-2, https://python.langchain.com/docs/concepts/chat_history/
- Chat-transcript ingestion examples: YES — `ChatMessageHistory` + `SQLChatMessageHistory` + `RedisChatMessageHistory`; `SQLRecordManager` for incremental re-indexing. LangGraph adds checkpointing for stateful agents.
- Chunking strategies: RecursiveCharacterTextSplitter (default); MarkdownHeaderTextSplitter, semantic_chunker.
- Tool-call-aware: Yes — `ToolMessage` natively; LangGraph state graphs preserve full tool-call traces.
- License: MIT
- Notes: Largest community, most integrations, but heaviest abstraction tax. Better as orchestrator than as ingestion library. LangSmith (paid) gives observability over chat-archive lookups.

### Haystack (deepset)
- Sources: https://docs.haystack.deepset.ai/docs/pipelines, https://docs.haystack.deepset.ai/docs/migrating-from-langgraphlangchain-to-haystack
- Chat-transcript ingestion examples: YES — `ChatMessage` (text + tool_calls + tool_call_results); explicit indexing-vs-query pipeline separation. Strong production patterns.
- Chunking strategies: DocumentSplitter (word/sentence/passage); custom splitters easy to add.
- Tool-call-aware: Yes — `ToolMessage` and tool_call/tool_call_results are first-class fields in `ChatMessage`.
- License: Apache 2.0
- Notes: Best architecture (separate indexing & query pipelines); production-ready. Slightly smaller community than LC/LI but more disciplined codebase. Good fit for teams that want fewer moving parts.

### txtai
- Sources: https://github.com/neuml/txtai, https://neuml.github.io/txtai/
- Chat-transcript ingestion examples: Yes — embeddings-database supports incremental upserts; conversation chunking demonstrated in their RAG tutorials.
- Chunking strategies: Configurable; supports sentence/segment-level + custom.
- Tool-call-aware: Less explicit; needs custom adapter to preserve tool calls as metadata.
- License: Apache 2.0
- Notes: Single-process embeddings DB + RAG framework — simplest deploy of the field. Best when you want one Python process to do everything (embed + index + retrieve + LLM). Vector store, SQLite-backed metadata, graph all built-in.

### Mastra (TypeScript)
- Sources: https://mastra.ai/en/docs/rag/overview, https://mastra.ai/blog/rag-tutorial
- Chat-transcript ingestion examples: Yes — chunking + embedding helpers; "observational memory" feature targets long-running agent histories specifically (positioned as alternative to traditional RAG for agent histories).
- Chunking strategies: text/markdown/code/json/html splitters; recursive chunker.
- Tool-call-aware: Yes — Agent SDK preserves tool calls in conversation state.
- License: Elastic License v2 (source-available; commercial restrictions for SaaS reselling)
- Notes: TypeScript-native, which matters if your engineer team's tooling is TS. The "observational memory" pattern (storing structured observations rather than raw chat) is interesting for agent transcripts — claims 10x cost reduction vs naive RAG (per VentureBeat coverage). Younger ecosystem.

## Reference Architectures

- **Spool (https://spooling.ai/)** — OSS local + paid cloud. Local pgvector on `:5434`, FastAPI cloud sync, $25/user/mo team tier. Closest direct precedent for our use case. Uses pgvector for both single-user and multi-tenant cloud.
- **MyChatArchive (https://mcpmarket.com/server/mychatarchive)** — Local-first; semantic search via local embeddings; ChatGPT/Claude/Cursor exports.
- **searchat (https://pypi.org/project/searchat/)** — PyPI package for semantic search over agent histories; reference for the ingestion contract.
- **claude-history (https://github.com/raine/claude-history)** — Pure-fuzzy, no vectors; useful baseline for "do we even need a vector DB?" comparison.
- **Claude Historian MCP (https://mcp.directory/mcp/details/346/claude-historian)** — MCP server pattern for surfacing chat history as a tool callable by other agents.
- **AgentsView (https://www.agentsview.io/)** — Cross-agent session history with optional Postgres sync — closest "team mode" pattern.
- **AWS multi-tenant vector search reference (https://aws.amazon.com/blogs/database/multi-tenant-vector-search-with-amazon-aurora-postgresql-and-amazon-bedrock-knowledge-bases/)** — Aurora pgvector + Bedrock KBs; metadata-filter tenant isolation.
- **Azure secure multi-tenant RAG (https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/secure-multitenant-rag)** — End-to-end auth-aware grounding architecture.
- **ChatRAG multi-tenant (https://www.chatrag.ai/docs/multi-tenant)** — pgvector + RLS pattern for shared KB + private chats.
- **Onyx (formerly Danswer) (https://github.com/onyx-dot-app/onyx)** — Open-source enterprise search; widely-cited reference for team-scale conversation/document RAG with auth.
- **LangChain "Building Chat LangChain" blog (https://www.langchain.com/blog/building-chat-langchain-2)** — Walkthrough of `SQLRecordManager` + Weaviate for an iteratively re-indexed chat over docs.
- **Microsoft Agent Framework chat history patterns (https://devblogs.microsoft.com/agent-framework/chat-history-storage-patterns-in-microsoft-agent-framework/)** — Tool-call-preserving conversation storage patterns with compaction.
- **Snowplow agent memory (https://snowplow.io/blog/ai-agent-memory-behavioral-patterns)** — Event-level memory indexed as vectors, retrieved during conversation; observability angle.

## Cost Model — Example 10-Engineer Team

**Workload assumptions:**
- 10 engineers × 50 conversations/week × 50 messages × 200 tokens = 50M tokens/year of new content (revised upward from 20M to account for tool-call output, which is often 5-10x message text in agent transcripts)
- ~500k chunks/year if chunking at ~100 tokens/chunk (reasonable for retrieval)
- Vector DB stored: 500k vectors × 1024 dims × 4 bytes = ~2 GB (raw float32). With HNSW overhead: ~3-5 GB.
- Query volume: 10 engineers × 20 retrieval-triggered queries/day × 250 working days = 50k queries/year (~140/day)
- Embeddings re-run on schema changes (~2x first-year volume budgeted)

### Embedding cost (one-time + ongoing, 100M tokens budget for safety)

| Provider | $/1M tokens | Year-1 cost (100M) | Steady-state (50M/yr) |
|---|---|---|---|
| OpenAI text-embedding-3-small | $0.02 | $2 | $1 |
| OpenAI text-embedding-3-large | $0.13 | $13 | $6.50 |
| Voyage voyage-3-lite | $0.02 | $2 | $1 |
| Voyage voyage-3 | $0.06 | $6 | $3 |
| Voyage voyage-code-3 (recommended) | $0.18 | $18 | $9 |
| Cohere Embed v3 (English) | $0.10 | $10 | $5 |
| Jina v3 (managed) | $0.018 | $1.80 | $0.90 |
| BGE-M3 self-hosted on $0.50/hr GPU | ~$0.003 | $0.30 | $0.15 (+ ~$50/mo idle GPU if not on-demand) |

**Embedding cost is essentially $0 at this scale regardless of provider.** Voyage code-3 is the rational choice — $18/yr for the best code retrieval quality is a rounding error.

### Vector DB cost (annual, 5 GB stored, ~50k queries/yr)

| Option | Year-1 cost | Notes |
|---|---|---|
| pgvector on existing Postgres | ~$0 | Marginal — uses existing infra |
| pgvector on Supabase Free | $0 | Up to 500MB free; team-tier plan ~$25/mo if exceeded |
| pgvector on Supabase Pro | $300 | $25/mo, dedicated |
| pgvector on Neon Pro | $228-$600 | $19/mo + storage |
| Qdrant Cloud (self-hosted on $20/mo VPS) | $240 | DIY single-node |
| Qdrant Cloud (managed, ~$0.10/hr 2 GB) | ~$700 | Includes HA |
| Weaviate Serverless (5M dimensions ≈ 5 GB) | ~$25-100 | $0.05/M dimensions/mo |
| Pinecone Serverless | ~$20-100 | Storage $0.33/GB/mo + 50k reads ≈ $1; bigger driver is namespace count |
| Turbopuffer | ~$10-50 | Object-storage backed; very cheap at this scale |
| Chroma Cloud | ~$0-50 | Generous free tier |
| LanceDB Cloud | ~$0-30 | Embedded-first; cloud is cheap |
| Milvus self-hosted | ~$1,200 | Needs etcd + S3 + Pulsar — overkill |

### Pipeline / orchestration cost
- LlamaIndex / LangChain / Haystack / txtai / Mastra: free OSS
- LangSmith (optional observability): $39/user/mo Plus, $0 Developer (1 free user) — **not required**
- Hosting orchestration code: 1 small VPS or 1 container on existing Kubernetes — ~$10-50/mo

### LLM cost for re-injection / reranking (often ignored — biggest cost driver)
- Reranker call per retrieval: ~500 tokens × 50k queries × $0.02/M (Cohere rerank-v3) = ~$0.50/yr (negligible)
- Voyage reranker ~$0.05/1k = $2.50/yr

### Total BYO Annual Cost (10-Engineer Team)

| Stack | Embeddings | Vector DB | Hosting | TOTAL |
|---|---|---|---|---|
| **Cheapest** (pgvector-on-existing-PG + Voyage-3-lite + LlamaIndex) | $1 | $0 | $0 | **$1/yr** |
| **Recommended baseline** (pgvector-on-Supabase + Voyage-code-3 + LlamaIndex) | $9 | $300 | $0 | **~$310/yr** |
| **Best quality** (Qdrant Cloud + Voyage-code-3 + LlamaIndex + Cohere reranker) | $9 | $700 | $50 | **~$760/yr** |
| **OSS-only / air-gapped** (self-host Qdrant + BGE-M3 on idle GPU + Haystack) | $0 | $240 (VPS) | included | **~$240/yr + GPU idle if dedicated** |

**Embedding API cost is irrelevant at 10-engineer scale.** Vector DB hosting + ops time dominates economics.

## Operational Complexity Assessment

**Initial build effort (single experienced backend engineer):**
- Cheapest stack (pgvector + LlamaIndex): **3-5 days** to working prototype, **2-3 weeks** to team-ready (auth, multi-tenant, deduplication, incremental ingest, monitoring)
- Recommended baseline: **1-2 weeks** prototype, **4-6 weeks** team-ready
- Best quality (Qdrant + reranker): **2 weeks** prototype, **6-8 weeks** team-ready
- OSS air-gapped (self-host Qdrant + BGE-M3 + Haystack): **3-4 weeks** prototype, **8-12 weeks** team-ready (GPU/inference ops adds significant complexity)

**Hidden complexity (where projects actually slow down):**
1. **Conversation chunking** — naive 512-token chunks shred tool-call/tool-result pairs; need custom splitter that preserves message boundaries. 1-2 week investment.
2. **Tool-call ingestion** — most pipeline tools' default loaders flatten ToolMessages incorrectly; need to preserve tool_call_id linkage so retrieval can fetch a tool result + its caller together.
3. **Incremental sync** — chat archives are append-mostly with rare in-place edits (Cursor's draft mode). Need content-addressed dedup; LangChain `SQLRecordManager` is the cleanest pattern.
4. **Authentication & multi-tenancy** — pgvector + RLS or Weaviate native multi-tenancy is easiest. Pinecone namespaces work but lock you in.
5. **Per-engineer privacy vs. team pooling** — typically two indexes per tenant (private + shared) with explicit publish step.
6. **Re-embedding cost on model upgrade** — when Voyage releases voyage-4, you re-embed everything. Budget 2-4x the steady-state embedding cost as a one-time event every ~12 months.
7. **Quality eval loop** — without an eval harness (golden-set queries → expected results), retrieval quality drifts silently. 1-2 weeks to set up properly.
8. **GDPR / data retention** — engineer transcripts may contain customer data, secrets, internal architecture. Redaction pipeline is non-trivial.

**Who runs it:**
- Cheapest stack on existing Postgres: **a single dev part-time** (1-2 days/month maintenance once stable)
- Recommended baseline: **a single dev quarter-time** (~1 day/week, primarily on quality eval and ingest debugging)
- Self-hosted GPU stack: **dedicated platform engineer half-time** plus on-call rotation; GPU ops + vector DB ops + auth = real platform burden

**Maintenance burden ranked:**
1. Lowest: pgvector on existing Postgres (no new system)
2. Low: Pinecone / Turbopuffer / Weaviate Cloud / Qdrant Cloud (managed)
3. Medium: Self-hosted Qdrant on managed Kubernetes
4. High: Self-hosted Milvus (etcd + S3 + Pulsar)
5. Highest: Self-hosted GPU embedding inference + self-hosted vector DB

## Stack Recommendation Matrix

| Pattern | Vector DB | Embedding | Pipeline | Cost/yr | Effort | When to choose |
|---|---|---|---|---|---|---|
| **Minimal cost** | pgvector on existing Postgres | OpenAI text-embedding-3-small | LlamaIndex | <$50 | 3-5 days | Team already runs Postgres; quality is "good enough" not critical; want one fewer system |
| **Best quality** | Qdrant Cloud | Voyage voyage-code-3 | LlamaIndex + Cohere rerank | ~$760 | 6-8 weeks | Code-heavy chat archive; quality of retrieval is core to value; team has cloud budget |
| **OSS-only / air-gapped** | Qdrant self-hosted | BGE-M3 self-hosted on idle GPU | Haystack | ~$240 hosting + GPU | 8-12 weeks | Compliance / data-sovereignty requirement; existing GPU infra; platform team capacity |
| **Team-of-10 baseline** | pgvector on Supabase Pro | Voyage voyage-code-3 | LlamaIndex (or Haystack) | ~$310 | 4-6 weeks | Default recommendation: best quality-per-effort tradeoff for the described workload |
| **Embedded / single-machine** | LanceDB or Chroma local | OpenAI text-embedding-3-small | txtai or LlamaIndex | <$10 | 1-2 days | Each engineer has their own private archive with optional team upload — closest to Spool OSS pattern |
| **Maximum scale / future-proof** | Turbopuffer or Weaviate | Voyage voyage-code-3 | LlamaIndex | ~$500-2000 | 4-6 weeks | Anticipating 100+ engineers / billions of vectors; Turbopuffer's object-storage economics dominate at scale |

## Key External Findings

1. **Embedding API cost is a non-issue at 10-engineer scale** — even the most expensive option (Voyage voyage-code-3) is $9-18/yr. Stop optimizing for $/1M tokens; optimize for retrieval quality.
2. **Voyage voyage-code-3 leads code retrieval by ~14-16% over OpenAI text-embedding-3-large** on 32 datasets — material quality gap for code-heavy chat archives.
3. **pgvector closed the performance gap dramatically** in 2024-2025 (pgvectorscale, HNSW maturity, CIDR 2026 paper). For <50M vectors, dedicated vector DB is no longer a clear win.
4. **Turbopuffer's object-storage architecture is structurally cheaper** for chat archive workloads where most data is cold and queries are bursty — but it's managed-only.
5. **Chunking is the hidden hard problem** — naive splitters destroy tool-call/tool-result linkage. LlamaIndex `ChatStore` and Haystack `ChatMessage` preserve structure; LangChain's default loaders historically flatten it.
6. **Spool (https://spooling.ai/) is the closest existing precedent** — OSS pgvector locally, $25/user/mo cloud, supports Claude Code + Cursor. Builds use case validation but also raises "build vs. buy" question.
7. **Incremental ingest dedup is non-trivial** — `SQLRecordManager` (LangChain) is the cleanest reusable pattern; rolling your own is a tax.
8. **Multi-tenancy is solved differently per DB** — Weaviate native > Pinecone namespaces > pgvector RLS > Qdrant payload-shard. Choice constrains team-vs-private model.
9. **Re-embedding on model upgrade is the largest amortized cost** — budget 2-4x steady-state embedding cost ~yearly.
10. **Tool-call-aware ingestion is rare** — Haystack and LlamaIndex are best; LangChain works but requires more glue. Mastra shines for TypeScript shops.
11. **Existing OSS tools (Spool, claude-history, searchat, MyChatArchive) suggest moderate market validation** — building from scratch competes with these directly.
12. **OSS embedding models (BGE-M3) are 80-90% as good as paid** for general retrieval but trail Voyage code-3 by 10-15% on code retrieval. Self-hosting saves money only if you already have GPU capacity.

## Recommendations from External Research

1. **The default BYO recommendation for a 10-engineer team is**: pgvector on Supabase Pro + Voyage voyage-code-3 + LlamaIndex with Haystack-style indexing/query pipeline separation. Annual cost ~$310; build effort 4-6 weeks.
2. **Frame BYO as the high-effort baseline in the comparables analysis.** $300-800/yr OPEX is dwarfed by 4-12 weeks of engineering build + ongoing maintenance (~1 day/week stable state). At a $200k/yr loaded engineer, build alone is $30-100k.
3. **Spool exists and addresses ~80% of the requirements**. The "build vs. buy" decision pivots heavily on whether the team needs (a) air-gap, (b) custom integrations beyond Claude Code/Cursor, or (c) tool-call-structure that Spool doesn't preserve. If none of those — Spool wins.
4. **Voyage voyage-code-3's 14-16% code retrieval lead is meaningful** for engineer-AI conversation archives. Recommend it as default embedding regardless of vector DB choice.
5. **Tool-call-aware chunking is a non-negotiable** for engineer-AI archives. Naive 512-token chunkers break tool_call_id ↔ tool_call_result linkage. Either pick a pipeline tool that preserves this (Haystack, LlamaIndex) or budget 1-2 weeks of custom chunker work.
6. **pgvector is a stronger 2026 default than the 2023 conventional wisdom suggested.** For team scales below 50M vectors, dedicated vector DB cost + ops + lock-in is rarely justified — and pgvectorscale closes the perf gap.
7. **For the Options Analysis: BYO is the LOWEST-recurring-cost path but HIGHEST upfront-cost path.** Crossover with managed/buy options depends entirely on engineer-time pricing. Make the explicit calculation: ~$60k engineer-time vs. $25/user/mo × 10 × 24 months = $6k.
8. **Hidden complexity warning for the report**: budget 2x quoted build estimates for first-time-RAG teams. Conversation ingestion is more annoying than document ingestion because of mutability, tool calls, and engineer-vs-team isolation logic.

