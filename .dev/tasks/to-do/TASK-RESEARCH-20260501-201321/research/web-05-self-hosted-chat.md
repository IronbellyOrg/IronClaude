# Research: Self-hosted / OSS chat platforms

**Topic:** Chat platforms that could serve as unified conversation store
**Status:** Complete
**Date:** 2026-05-01

---

## Open WebUI

- **Positioning:** Most popular self-hosted ChatGPT-style frontend; supports many backends (Ollama, OpenAI-compat) with multi-user, RAG, and import/export.
- **Sources:**
  - https://github.com/open-webui/open-webui
  - https://docs.openwebui.com/features
  - https://docs.openwebui.com/getting-started/advanced-topics/scaling/
  - https://docs.openwebui.com/features/chat-conversations/data-controls/import-export/
  - https://docs.openwebui.com/reference/api-endpoints/
  - https://github.com/yetanotherchris/openwebui-importer
- **Reliability:** Official docs + repo
- **Relevance:** HIGH — has both an import API and a RAG layer; the closest off-the-shelf "unified chat store" candidate.
- **Storage backend:** SQLite by default (single-file at `/app/backend/data/webui.db`), pluggable to PostgreSQL via `DATABASE_URL` for multi-user/scale. Vectors stored in ChromaDB by default; Qdrant/Milvus/pgvector supported.
- **Multi-user:** Yes — built-in local accounts, RBAC (admin/user/pending), OAuth (Google, Microsoft, OIDC), LDAP. Group permissions and per-model access control.
- **RAG-over-own-chat:** PARTIAL/INDIRECT — RAG ("Knowledge") is designed over uploaded files/URLs. Saved chats are not automatically indexed for retrieval; you must export a chat and re-ingest it as a Knowledge document. There is no native "search my past conversations semantically" toggle as of 4.x.
- **External-chat ingestion API:** YES — two paths. (1) UI/API import accepts Open WebUI's own JSON format and auto-converts ChatGPT exports; community converter (`openwebui-importer`) targets Claude/Grok/ChatGPT exports. (2) Knowledge API (`/api/v1/knowledge/...`, `/api/v1/files/`) lets you POST arbitrary text/JSON as documents; a SpecStory-style transcript can be ingested as a Knowledge file. Direct "create a chat object from external transcript" endpoint exists but is undocumented and brittle.
- **LLM providers:** Ollama native, any OpenAI-compatible endpoint (Anthropic via proxy, OpenRouter, vLLM, llama.cpp, LM Studio), Azure OpenAI, custom pipelines via "Functions"/"Pipelines" plugin system.
- **License:** BSD-3-Clause-ish — recently moved to a modified license (post-2024) that requires preserving branding for deployments serving >50 users without commercial license. Self-hosted internal team usage is fine.
- **Activity signal:** ~95k+ GitHub stars; very active (daily commits); largest mind-share in self-hosted LLM UI category.
- **Deployment story:** One-line Docker (`docker run ghcr.io/open-webui/open-webui:main`), Helm chart for k8s, Railway/Render templates, native pip package.
- **Production users:** Heavy enterprise/internal use — adopted by many engineering teams as their internal Ollama/OpenAI gateway. No public marquee logos but extensive HN/Reddit testimony.
- **Architectural fit:** STRONG candidate as a *frontend* over a unified chat store, but WEAK as the chat store itself. Its data model is "chats started in this UI", not "all chats my team has had with any tool". You'd need to ingest external chats as Knowledge docs (loses chat structure → becomes RAG corpus) or hack the chat-creation API. Adopt-as-product is plausible only if losing turn-by-turn structure is OK.

---

## LibreChat

- **Positioning:** Open-source ChatGPT clone with strong multi-provider support, agents, and a built-in RAG API; aimed at teams.
- **Sources:**
  - https://github.com/danny-avila/LibreChat
  - https://www.librechat.ai/docs
  - https://www.librechat.ai/docs/features
  - https://www.librechat.ai/docs/configuration/mongodb/mongodb_auth
  - https://www.librechat.ai/docs/features/access_control
  - https://www.librechat.ai/docs/features/import_convos
  - https://www.librechat.ai/docs/features/agents_api
- **Reliability:** Official docs + repo
- **Relevance:** HIGH — explicit "Import Conversations" feature plus a packaged RAG API; closest competitor to Open WebUI for team deployments.
- **Storage backend:** MongoDB (chats, users, messages, presets, prompts). MeiliSearch for full-text chat search. Separate `rag_api` service uses pgvector (Postgres) for embeddings. File storage local or S3.
- **Multi-user:** Yes — local auth, OAuth (Google/GitHub/Discord/Facebook/Apple), OpenID Connect, LDAP. Role-based access control with admin/user roles and granular per-feature permissions ("Access Control" page). Multi-tenant deployments documented.
- **RAG-over-own-chat:** NO (native). Built-in MeiliSearch indexes conversations for keyword search across own history, but vector/semantic RAG over saved chats is not a first-class feature. The bundled `rag_api` operates on uploaded files only.
- **External-chat ingestion API:** YES, partial — official "Import Conversations" supports ChatGPT's `conversations.json` format, LibreChat's own JSON, and (per docs) a normalized schema. Conversations API exposes endpoints for programmatic management. So a SpecStory-style transcript could be transformed into ChatGPT-shape JSON and imported. No first-class "ingest agent CLI transcript" endpoint.
- **LLM providers:** OpenAI, Anthropic (native), Google Vertex/Gemini, AWS Bedrock, Azure, Mistral, Ollama, any OpenAI-compatible. Plugins for tools/agents.
- **License:** MIT
- **Activity signal:** ~22k+ GitHub stars; very active development (multiple commits/day); strong contributor base.
- **Deployment story:** Docker Compose (recommended, includes Mongo + Meilisearch + RAG API), Helm chart, Render/Railway templates, manual install supported.
- **Production users:** Reportedly used by several mid-size engineering orgs as internal AI hub; cited on HN as "what we deployed instead of ChatGPT Teams". No marquee public reference.
- **Architectural fit:** GOOD as an internal AI hub but POOR as the unified-chat-context store for *agent* conversations. MongoDB schema is opinionated around interactive UI chats; agent transcripts (with tool calls, large context, cache hits) don't map cleanly. RAG is over docs, not over its own chat history. You'd be fighting the data model.

---

## AnythingLLM

- **Positioning:** "All-in-one AI app" — chat UI + workspace-scoped RAG; aimed at SMBs/teams who want chat-with-your-docs without ops overhead.
- **Sources:**
  - https://github.com/Mintplex-Labs/anything-llm
  - https://anythingllm.com/
  - https://deepwiki.com/Mintplex-Labs/anything-llm/3.1-system-api-and-authentication
  - https://deepwiki.com/Mintplex-Labs/anything-llm/7-workspace-management
  - https://github.com/Mintplex-Labs/anything-llm/issues/4598
- **Reliability:** Repo + DeepWiki (3rd-party reflection of repo)
- **Relevance:** MEDIUM — has API auth and workspaces but RAG is doc-centric, not chat-centric.
- **Storage backend:** SQLite by default for app metadata/chat history (Prisma ORM); switchable to Postgres. Vector DB pluggable: LanceDB (default, file-based), Chroma, Pinecone, Weaviate, Qdrant, Milvus, AstraDB, pgvector.
- **Multi-user:** Yes — "Multi-user mode" toggle. Roles: admin / manager / default. Local accounts; OAuth and SSO available in cloud tier; community-contributed SSO patches. RBAC scoped per workspace.
- **RAG-over-own-chat:** NO. Chat history is stored as conversation rows for replay/UI but is not embedded into the vector store. RAG retrieval pulls from documents pinned to a workspace, not from prior chat turns.
- **External-chat ingestion API:** YES, via document ingestion. POST `/api/v1/document/upload` or `/api/v1/document/raw-text` accepts arbitrary text/JSON which gets embedded into a workspace. So a SpecStory transcript could be POSTed as a document and become RAG-retrievable. Native "import these as past chats" is not supported.
- **LLM providers:** OpenAI, Anthropic, Azure, AWS Bedrock, Cohere, Mistral, Groq, Ollama, LM Studio, Together AI, OpenRouter, Generic OpenAI-compat, Hugging Face, KoboldAI.
- **License:** MIT
- **Activity signal:** ~30k+ GitHub stars; very active; commercial backer (Mintplex Labs).
- **Deployment story:** Docker (`mintplexlabs/anythingllm`), desktop app (Electron) for solo use, Render/Railway templates, k8s via Helm.
- **Production users:** Used by SMBs and individuals; smaller enterprise footprint than Open WebUI/LibreChat. Featured in many "local RAG" blog posts.
- **Architectural fit:** WEAK as unified chat-context store. The strength is "chat with these docs", not "search every prior chat my team has had". Ingesting transcripts as documents loses turn structure and conflates them with knowledge-base content. Bug history (e.g. issue #4598 — `user_id = NULL` for API-key chats) signals multi-user audit trail is still maturing.

---

## Onyx (formerly Danswer)

- **Positioning:** Open-source enterprise search + chat over your company's data. Strong connector ecosystem; explicitly aimed at "ChatGPT for your team's docs/Slack/Jira/Confluence".
- **Sources:**
  - https://github.com/onyx-dot-app/onyx
  - https://docs.onyx.app/overview/core_features/connectors
  - https://docs.onyx.app/overview/core_features/internal_search
  - https://docs.onyx.app/developers/guides/create_connector
  - https://docs.onyx.app/developers/guides/index_files_ingestion_api
  - https://docs.onyx.app/admins/connectors/official/slack/slack_indexed
- **Reliability:** Official docs + repo
- **Relevance:** HIGH — has a documented JSON ingestion API designed for exactly the "ingest external content as searchable documents" use case, and a real connector framework for ongoing sync.
- **Storage backend:** Postgres (metadata, chats, users, ACLs), Vespa (default vector + keyword index; alternative engines being added), Redis (queues), MinIO/S3 (file blobs). Most production-shaped storage stack in this category.
- **Multi-user:** Yes — local auth, OAuth, OIDC, SAML SSO, Google Workspace. RBAC with admin/curator/basic roles. Per-document ACL inheritance from source connectors (e.g. Slack channel ACLs propagate to search).
- **RAG-over-own-chat:** PARTIAL. Onyx's own chat sessions are stored in Postgres and are visible/searchable in the UI, but they aren't (by default) re-indexed into Vespa as documents. There's a community pattern of running a connector against your own chat exports to feed them back in.
- **External-chat ingestion API:** YES — first-class. The "Index Files with the Ingestion API" endpoint accepts arbitrary JSON documents (`{document_id, sections[], metadata, semantic_identifier, ...}`), pairs them with a `cc_pair_id`, and indexes them into Vespa. SpecStory-style transcripts map well: each conversation = one document, each turn = one section. This is exactly the integration shape needed.
- **LLM providers:** OpenAI, Anthropic, Azure OpenAI, AWS Bedrock, Vertex/Gemini, Cohere, custom OpenAI-compatible.
- **License:** MIT (core); enterprise features (advanced RBAC, audit, SSO upgrades) gated behind paid plan.
- **Activity signal:** ~14k+ GitHub stars; active; venture-backed (Y Combinator); rebranded from Danswer in 2024.
- **Deployment story:** Docker Compose (canonical), Helm chart for k8s, Terraform modules for AWS, managed cloud option.
- **Production users:** Several public references (Ramp, mid-size SaaS); used internally at multiple YC companies per public threads.
- **Architectural fit:** STRONGEST candidate of the eight as a *unified searchable conversation store*. The ingestion API + connector framework + ACL-aware Vespa index is purpose-built for "ingest stuff from N sources, search across all of it, optionally chat over it". Adopting Onyx as the chat-context substrate is genuinely viable — though it's a search-first product, so the chat UI is secondary and may not match what engineers want when they want to actively converse. Best fit if the goal is "team-wide retrieval over all AI conversations" rather than "shared chat UI".

---

## Lobe Chat

- **Positioning:** Polished, design-forward open-source chat UI; emphasis on plugins/agents, supports server-side multi-user mode with Postgres.
- **Sources:**
  - https://github.com/lobehub/lobe-chat
  - https://lobehub.com/docs/self-hosting/start
  - https://deepwiki.com/lobehub/lobe-chat
- **Reliability:** Official docs + repo
- **Relevance:** MEDIUM — has knowledge base and multi-user but ingestion is doc-focused.
- **Storage backend:** Two modes. (1) Client-side: chats stored in browser IndexedDB (single-user). (2) Server-side: Postgres + pgvector for chats and embeddings, Redis for cache, S3-compatible blob storage for files. NextAuth/Clerk for auth.
- **Multi-user:** Yes (server mode only) — Clerk or NextAuth with OAuth providers; per-user data isolation. No formal RBAC/team roles — closer to "many individual accounts" than "team workspace".
- **RAG-over-own-chat:** NO native. Knowledge base RAG operates on uploaded files; saved chats are not indexed for retrieval.
- **External-chat ingestion API:** UNCLEAR / minimal. Has chat export (JSON, Markdown) and import in the UI; programmatic ingestion endpoints are not prominently documented. Most "API" surface is OpenAI-compatible passthrough rather than a transcript-storage API.
- **LLM providers:** 40+ providers — OpenAI, Anthropic, Google, AWS Bedrock, Azure, Mistral, Groq, Ollama, Perplexity, DeepSeek, Qwen, Moonshot, Zhipu, plus many regional Chinese providers. Largest provider matrix in this category.
- **License:** Apache-2.0 (core); some advanced features (auth providers, observability) require LobeHub Cloud or commercial config.
- **Activity signal:** ~50k+ GitHub stars; very active; strong design/UX reputation.
- **Deployment story:** Docker (`lobehub/lobe-chat-database` for server mode), Vercel one-click, Railway/Zeabur templates. Server-mode deployment is more involved than Open WebUI.
- **Production users:** Strong individual/prosumer adoption; less enterprise traction than LibreChat or Open WebUI.
- **Architectural fit:** WEAK as unified chat store. Server mode has the right pieces (Postgres + pgvector + multi-user) but the data model assumes interactive UI sessions and the ingestion path is "upload a file as knowledge", not "ingest a transcript". UX-driven, not platform-driven.

---

## Chatbox

- **Positioning:** Cross-platform desktop client (Win/Mac/Linux/iOS/Android/Web) for chatting with LLM APIs. Local-first, single-user.
- **Sources:**
  - https://github.com/chatboxai/chatbox
  - https://releases.chatboxai.app/en/guide/faq/data-storage
  - https://www.reddit.com/r/LLMDevs/comments/1kipl18/alternatives_to_chatbox_ai_with_api_conversation/
- **Reliability:** Official FAQ + repo
- **Relevance:** LOW — not a server platform; effectively out of scope for "team chat store".
- **Storage backend:** Local only — IndexedDB (web), local filesystem (desktop). No server component in OSS edition.
- **Multi-user:** No. Single-user desktop app. (Chatbox Cloud is a paid hosted offering with login, separate codebase concerns.)
- **RAG-over-own-chat:** No native RAG.
- **External-chat ingestion API:** No API. Manual import/export of chat data via UI only.
- **LLM providers:** OpenAI, Anthropic, Google, Ollama, Azure, Groq, plus any OpenAI-compatible.
- **License:** GPLv3 (community edition); commercial editions exist.
- **Activity signal:** ~30k+ GitHub stars; active; primarily a polished UX over BYO API keys.
- **Deployment story:** Native installers; no server-side self-host.
- **Production users:** Individuals; not a team product.
- **Architectural fit:** NONE for the unified-store use case. Useful only as a possible *client* that talks to whatever store you build.

---

## Khoj

- **Positioning:** "Personal AI" — open-source assistant that indexes your notes/docs/email and lets you chat with that knowledge across web/desktop/Obsidian/Emacs/WhatsApp.
- **Sources:**
  - https://github.com/khoj-ai/khoj
  - https://docs.khoj.dev/
  - https://docs.khoj.dev/get-started/setup/
  - https://docs.khoj.dev/features/chat/
  - https://docs.khoj.dev/privacy
- **Reliability:** Official docs + repo
- **Relevance:** MEDIUM — closest to "RAG over my own past chats" in spirit but personal-scale.
- **Storage backend:** Postgres (with pgvector) for users, conversations, and embeddings; local file/cloud blob storage for source documents; Redis optional.
- **Multi-user:** Yes — Khoj supports multi-user self-hosted with email magic-link or Google OAuth, per-user data isolation. Not "team workspaces" with shared knowledge — each user has their own Khoj.
- **RAG-over-own-chat:** PARTIAL — Khoj indexes your synced documents (notes, PDFs, etc.) for retrieval. Conversation memory is summarized and used as context for follow-ups, but past conversations across sessions aren't fully indexed for cross-conversation semantic search by default. There are open issues/discussions about deeper "memory of past chats".
- **External-chat ingestion API:** WEAK — has APIs for syncing files/notes (Obsidian plugin, Emacs sync, file uploads) but not a documented "POST a chat transcript JSON" endpoint. You could push transcripts as Markdown notes via the file API.
- **LLM providers:** OpenAI, Anthropic, Google Gemini, local via Ollama / llama.cpp.
- **License:** AGPLv3 — copyleft; matters for any commercial fork.
- **Activity signal:** ~25k+ GitHub stars; active; small core team.
- **Deployment story:** Docker Compose (recommended), pip install for local dev, native installers for desktop, hosted cloud option.
- **Production users:** Mostly individual/prosumer; some small-team self-hosted instances reported.
- **Architectural fit:** WEAK-to-MEDIUM. The personal-assistant framing means data model is per-user; team aggregation isn't the design goal. AGPL license is a friction for embedding inside a commercial product. Useful as inspiration (its conversation+note RAG is one of the cleaner OSS implementations) more than as a substrate.

---

## BetterChatGPT

- **Positioning:** Lightweight ChatGPT-style web UI; BYO OpenAI API key; runs entirely client-side.
- **Sources:**
  - https://github.com/ztjhz/BetterChatGPT
- **Reliability:** Repo
- **Relevance:** LOW — single-user client, no server, no ingestion API.
- **Storage backend:** Browser localStorage / IndexedDB. No backend.
- **Multi-user:** No.
- **RAG-over-own-chat:** No.
- **External-chat ingestion API:** No. Import/export JSON via UI only.
- **LLM providers:** OpenAI (primary); custom endpoints supported.
- **License:** CC0-1.0 (public domain dedication).
- **Activity signal:** ~8k+ stars; lightly maintained — original author moved on; activity has slowed since 2024.
- **Deployment story:** Static site (Vercel/Netlify). No server.
- **Production users:** Individuals.
- **Architectural fit:** NONE. Not a viable substrate.

---

## Self-Hosted Chat Comparison Table

| Platform | Storage | Multi-user | RAG-own-chat | Ext. ingestion | License | Stars | Fit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Open WebUI | SQLite/Postgres + Chroma | Yes (RBAC, OAuth, LDAP) | Indirect (chat→Knowledge) | Yes (import API + Knowledge API) | BSD-ish (modified, branding clause) | ~95k | MEDIUM-HIGH |
| LibreChat | MongoDB + Meilisearch + pgvector | Yes (RBAC, OAuth, OIDC, LDAP) | Keyword only (Meili); no semantic | Yes (Import Convos API, ChatGPT format) | MIT | ~22k | MEDIUM |
| AnythingLLM | SQLite/Postgres + LanceDB/many | Yes (3 roles, workspaces) | No | Yes (doc upload API) | MIT | ~30k | LOW-MEDIUM |
| Onyx (Danswer) | Postgres + Vespa + Redis + S3 | Yes (SAML/OIDC, RBAC, ACL) | Partial (chats stored, not re-indexed by default) | YES — first-class JSON ingestion API + connector framework | MIT (core) | ~14k | HIGH |
| Lobe Chat | IndexedDB OR Postgres+pgvector | Yes (server mode, Clerk/NextAuth) | No | Weak (UI only) | Apache-2.0 | ~50k | LOW |
| Chatbox | Local (IndexedDB / FS) | No | No | No | GPLv3 | ~30k | NONE |
| Khoj | Postgres+pgvector | Yes (per-user, not team) | Partial (notes yes, chats summarized) | Weak (file API) | AGPLv3 | ~25k | LOW-MEDIUM |
| BetterChatGPT | Browser localStorage | No | No | No | CC0 | ~8k | NONE |

---

## Key External Findings

- Onyx is the only platform in this set with a documented, first-class JSON ingestion API designed for "POST a structured document, have it become searchable across users with ACLs". Everything else in this category was built UI-first and treats external ingestion as either (a) one-time UI import or (b) "upload as a file/document" — both of which lose conversation structure.
- The pattern across all eight platforms is identical: RAG = "chat with your uploaded documents". None of them ship native semantic RAG over the user's *own past chats*. The closest is Khoj (summarizes prior conversations) and Open WebUI (you can manually re-import chats as Knowledge). This is a real product gap in OSS land.
- Open WebUI moved off pure BSD/MIT to a license that requires preserving "Open WebUI" branding for deployments serving >50 users without a commercial agreement (per /r/opensource thread, May 2025). For a commercial team product wanting to embed/re-skin, this is a non-trivial constraint.
- LibreChat's bundled `rag_api` is a separate Python service using pgvector — architecturally clean, but it's wired only to the file upload path, not to the conversation collection. The MeiliSearch integration provides keyword search over conversations, which is a much weaker substitute for semantic retrieval.
- AnythingLLM has a known multi-user audit-trail bug (issue #4598: API-key-authed messages stored with `user_id = NULL`). For a team-of-record system this is disqualifying until fixed.
- Lobe Chat's "server-side database mode" is recent and less battle-tested than its single-user browser mode; HN/Reddit posts reflect prosumer adoption, not team deployments.
- HN sentiment on Onyx is positive: "Onyx actually finds things" was the recurring phrase in the Launch HN thread (item 46045987 / 46049095). Search quality, not chat UX, is its differentiator.
- Reddit consensus on Open WebUI vs LibreChat: Open WebUI wins on ease of deployment and ecosystem; LibreChat wins on multi-provider polish and team-feature maturity (access control panel). Both are credible internal-AI-hub choices; neither is designed to ingest external coding-tool transcripts.
- Chatbox and BetterChatGPT are out of scope as substrates — they have no server. They could be candidates for the *client* end of a custom architecture but contribute nothing to the storage problem.

## Recommendations from External Research

1. **Adopt-as-product is only realistically viable with Onyx.** It is the one platform that has (a) a proper JSON ingestion API, (b) ACL-aware multi-tenant search, (c) Postgres + Vespa storage that can be queried independently of its UI. SpecStory-style transcripts map cleanly to its document/section model. Recommendation: include Onyx as the leading "buy/adopt" comparable in the architecture decision.
2. **Open WebUI is the strongest "deploy as the team's chat front door" choice but a poor unified-store choice.** If the architecture decision separates the storage substrate from the user-facing chat UI, Open WebUI is the obvious recommendation for the UI layer (largest mind-share, ecosystem, multi-provider, RBAC) — but it should not be load-bearing for ingested external transcripts.
3. **LibreChat is the runner-up UI choice** with arguably better team-features (access control panel) but fewer plugins and tighter MongoDB coupling. Choose between LibreChat and Open WebUI on operational preference (Mongo+Meili+rag_api vs SQLite/Postgres+Chroma).
4. **AnythingLLM, Lobe Chat, Khoj are weak comparables for this specific architecture.** They show up in any "self-hosted AI chat" survey, but their data models are wrong-shaped for the unified-conversation-DB use case. They should be mentioned in the comparables matrix but not as serious adoption candidates.
5. **Chatbox and BetterChatGPT should be cited only as desktop-client examples** — proof that there's a market for thick clients over a shared backend, but contribute nothing to the substrate decision.
6. **Universal gap: RAG-over-own-chat is unsolved in OSS chat platforms.** This is a real differentiator opportunity. Whatever architecture is recommended should treat "semantic search across all team AI conversations" as a green-field capability, not something an off-the-shelf platform delivers.
7. **License hygiene matters:** Open WebUI's branding clause and Khoj's AGPLv3 are real constraints if the output is meant to be a commercial product; Onyx (MIT core), LibreChat (MIT), AnythingLLM (MIT), Lobe Chat (Apache-2.0) are the cleaner licenses for embedding.
