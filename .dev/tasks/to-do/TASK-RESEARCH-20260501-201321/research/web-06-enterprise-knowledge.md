# Research: Enterprise org-memory & knowledge platforms

**Topic:** Could enterprise knowledge tools ingest AI conversation transcripts?
**Status:** Complete
**Date:** 2026-05-01

---

## Glean

- **Positioning:** Enterprise AI search platform that unifies internal knowledge across SaaS apps, with built-in connectors and a custom indexing/push API.
- **Sources:**
  - https://docs.glean.com/connectors/custom/about
  - https://docs.glean.com/connectors/custom/glean-apis
  - https://docs.glean.com/connectors/crawler-and-indexing-limits
  - https://www.glean.com/product/api
- **Reliability:** Official vendor docs.
- **Relevance:** HIGH — Glean is purpose-built for ingesting heterogeneous text artifacts and exposes a documented push/indexing API with per-document permissions. AI conversation transcripts map cleanly onto a Glean custom datasource doc.
- **Custom ingestion API:** YES. Indexing API (a.k.a. Push API) for custom data sources. Push documents with title, body (HTML/text), author, ACL, datasource ID, owner, timestamps. Auth via Glean-issued API tokens (indexing scope, separate from search scope). Recommended pattern: define a custom datasource "ai-chat" then bulk push docs with permission lists.
- **Volume limits:** Files >64 MB are not indexed for content (metadata + perms still indexed). Indexed text content capped ~16.875 MB after conversion. Ample for chat transcripts. Bulk ingest endpoints exist; rate limits not publicly stated, customer-tier dependent.
- **Search:** Hybrid (lexical + semantic / vector + ranking), permission-aware. Personalized result ranking per user.
- **RAG/QA:** YES — Glean Assistant generates grounded answers with citations over indexed content; Custom datasources participate by default.
- **Visibility model:** Strong RBAC; per-doc ACLs at push time (allow lists, group lists, public-to-org). Permission-aware search is a core selling point.
- **Pricing tier for API:** Enterprise-only. No public pricing; sales-led contract. API access (indexing + search) is included with platform license but is not available to a free/trial tier.
- **Data residency:** SaaS multi-tenant; enterprise data residency options (US, EU). On-prem not advertised; private VPC / dedicated tenancy available for enterprise contracts.
- **Precedent for chat-transcript ingestion:** Indirect — Glean already indexes Slack, Teams, etc. Customers ingesting AI assistant transcripts as a custom datasource is plausible but no widely-publicized reference. Glean's own "Glean Apps" / agent runs are stored, but third-party AI chat ingestion is a custom-build.
- **Architectural fit:** Excellent for a company that already runs Glean — chat transcripts become first-class search/RAG citizens with enterprise auth. High integration cost for orgs that don't have Glean (license + setup).

## Mem (mem.ai)

- **Positioning:** AI-native personal/team notes app with an LLM "second brain" that auto-organizes captured content; consumer/prosumer with team plans.
- **Sources:**
  - https://help.mem.ai/features/api
  - https://docs.mem.ai/
  - https://docs.mem.ai/api-reference
  - https://docs.mem.ai/guides/get-started/quickstart
  - https://docs.mem.ai/guides/use-cases/mem-it
- **Reliability:** Official docs.
- **Relevance:** MEDIUM — exposes a working ingestion endpoint, but Mem is fundamentally a personal-first product; team/RBAC story is thin compared to Glean/Notion.
- **Custom ingestion API:** YES. REST API; primary ingestion endpoint is `mem-it` (single document push, accepts markdown/text). Bearer-token auth from user account. Designed for "save this article/snippet" use cases — a per-transcript POST is straightforward.
- **Volume limits:** Per-account rate limits (not prominently published). No clear bulk-ingest endpoint; one-doc-per-call pattern. Document size limits not explicitly published — practical limit is "a long note."
- **Search:** Lexical + AI semantic recall built into the app. Search via REST is available.
- **RAG/QA:** YES — "Chat with Mem" answers questions over your notes with citations.
- **Visibility model:** Per-user account; sharing/team features secondary. RBAC limited compared to enterprise tools.
- **Pricing tier for API:** Paid plan required (Mem+); API access historically gated to paying users. No clear enterprise SKU.
- **Data residency:** SaaS-only, US-hosted. No on-prem.
- **Precedent for chat-transcript ingestion:** No widely-cited precedent. Plausible because mem-it accepts arbitrary markdown.
- **Architectural fit:** Weak as a team-wide AI-conversation DB — owner-centric model and per-user accounts make org-level rollout awkward. Could fit a single engineer who already lives in Mem.

## Notion AI / Notion API

- **Positioning:** Block-based docs/wiki with a public REST API and a layered "Notion AI" Q&A across workspace content.
- **Sources:**
  - https://developers.notion.com/reference/request-limits
  - https://developers.notion.com/reference/post-page
  - https://developers.notion.com/docs/working-with-page-content
  - https://developers.notion.com/guides/data-apis
  - https://developers.notion.com/guides/data-apis/working-with-markdown-content
- **Reliability:** Official docs.
- **Relevance:** HIGH — many engineering teams already run Notion; pushing transcripts as pages is technically trivial.
- **Custom ingestion API:** YES. `POST /v1/pages` creates pages under a parent page or database; `PATCH /v1/blocks/{id}/children` appends blocks. Internal integration token (workspace-installed) or OAuth. JSON block schema; markdown-to-blocks conversion required (Notion publishes a guide). Pages can be tagged/property-rich via database parents.
- **Volume limits:** Rate limit ~3 requests/sec average per integration (bursts allowed), 429 backoff. Per-request payload caps: arrays max 100 elements, rich-text max 2000 chars per element, URL max 2000 chars, code blocks max ~2000 chars per block (longer content must be split into multiple blocks). No hard daily document cap, but ingest of multi-MB transcripts requires chunking into blocks — can produce 100s of API calls per long transcript.
- **Search:** Built-in lexical search; Notion AI adds semantic/RAG layer. Public Search API exists but is limited to title/property matches and is not full-text-grade.
- **RAG/QA:** YES via Notion AI (paid add-on). Q&A across all workspace content the user has access to.
- **Visibility model:** Page/database-level permissions inherited from Notion's sharing model — strong RBAC at workspace, group, and page level.
- **Pricing tier for API:** API itself is free on all paid plans (and free plans for personal). Notion AI is a per-seat paid add-on. No "API tier" gatekeeper, but workspace plan dictates user/page limits.
- **Data residency:** SaaS, US/EU options on Enterprise plan. No on-prem.
- **Precedent for chat-transcript ingestion:** YES — many integrations push ChatGPT/Claude conversation logs to Notion (community templates, Zapier/Make recipes, "save chat to Notion" extensions). Well-trodden path.
- **Architectural fit:** Strong for "ingest into the wiki we already use." Friction is block-schema chunking, rate limits at scale, and that Notion AI Q&A scope follows Notion's permission graph (so transcripts must live in a shared workspace area). Not built for high-volume programmatic chat-log streams.

## Coda AI / Coda

- **Positioning:** Hybrid doc + database product with API and a Pack SDK ecosystem; Coda AI for in-doc generative actions and Q&A.
- **Sources:**
  - https://coda.io/developers
  - https://help.coda.io/en/articles/2199620-does-coda-have-an-api
  - https://coda.io/packs/build/latest/reference/sdk/
  - https://coda.io/packs/build/latest/guides/overview/
  - https://www.postman.com/codaio/coda-workspace/documentation/0vy7uxn/coda-api
- **Reliability:** Official docs.
- **Relevance:** MEDIUM — has APIs and a developer SDK, but Coda is structured-doc-first; transcripts fit awkwardly as either rows or canvas blocks.
- **Custom ingestion API:** YES. REST API at `https://coda.io/apis/v1`. Rows: `POST /docs/{docId}/tables/{tableIdOrName}/rows` (insert/upsert). Pages: `POST /docs/{docId}/pages` (create page with markdown content). Pack SDK lets you build connector-style ingestion that surfaces inside Coda.
- **Volume limits:** Coda enforces per-doc object/row limits and per-account rate limits (10 req/sec typical, 429 backoff). Doc size caps are stricter than Notion (older docs hit the "doc too large" wall). Long transcripts as rows are fine if columns are bounded; as pages, content is chunked similarly to Notion.
- **Search:** Lexical search inside docs. Cross-doc search is weaker than Glean/Notion.
- **RAG/QA:** YES — Coda AI Block / Coda Brain answer questions over doc content; scope is the doc/workspace.
- **Visibility model:** Doc-level sharing; workspace RBAC. Less granular than Notion at the section level.
- **Pricing tier for API:** API access available on paid tiers (Pro and above for unlimited docs). Coda AI is a paid add-on. No special "API enterprise" gate.
- **Data residency:** SaaS only.
- **Precedent for chat-transcript ingestion:** Limited precedent. Some users build "chat log" tables via Pack SDK against OpenAI/Anthropic, but it's not a common pattern.
- **Architectural fit:** Weaker than Notion for transcript ingestion — Coda's strength is structured operational data, not narrative text retrieval. Possible but not the path of least resistance.

## Slack AI / Slack API

- **Positioning:** Team chat platform with Slack AI add-on (search, summaries, recap) over channel/DM history; not a knowledge platform per se but an *implicit* org memory.
- **Sources:**
  - https://api.slack.com/methods/chat.postMessage
  - https://docs.slack.dev/reference/methods/chat.postMessage
  - https://api.slack.com/web
  - https://api.slack.com/docs/messages
- **Reliability:** Official docs.
- **Relevance:** MEDIUM — feasible to mirror AI conversation transcripts as Slack messages in a dedicated channel; Slack AI then indexes them automatically. But Slack message size limits are tight for long transcripts.
- **Custom ingestion API:** YES (indirectly). `chat.postMessage` posts arbitrary text/Block Kit messages; `files.upload` for larger artifacts; Canvas API for richer structured docs. Bot token auth (`xoxb-…`). No formal "ingest to Slack AI" endpoint — Slack AI indexes whatever messages already exist in channels the user can access.
- **Volume limits:** `chat.postMessage` text limit ~40,000 chars per message (effectively ~4000 visible without "show more"); Block Kit hard cap 50 blocks per message; file upload up to 1 GB. Tier 1-4 rate limits: ~1 msg/sec per channel sustained. Long transcripts must be chunked across multiple messages or attached as files (which Slack AI may not index as deeply).
- **Search:** Lexical search.modifiers (in:, from:, has:); Slack AI adds semantic search and conversational Q&A on Enterprise+ tier.
- **RAG/QA:** YES via Slack AI ("Ask anything about this channel/workspace"). Requires Enterprise Grid + Slack AI add-on (per-seat).
- **Visibility model:** Channel membership = visibility; private channels, shared channels, DMs all respected. Strong workspace boundaries; RBAC handled by channel ACLs.
- **Pricing tier for API:** API is free on all plans. Slack AI search/RAG requires paid Slack AI add-on (Enterprise Grid).
- **Data residency:** SaaS; Enterprise Grid offers EKM, residency in US/EU/JP/AU.
- **Precedent for chat-transcript ingestion:** Common pattern — many bots post LLM responses as Slack messages, and orgs treat #ai-logs channels as an informal corpus. No widely cited "Slack AI as canonical AI conversation DB" reference, but mechanically supported.
- **Architectural fit:** Reasonable as a "shadow" capture layer because Slack is already deployed everywhere. Mediocre as a primary store: message size limits, rate limits, awkward thread structure for long sessions, and Slack AI search quality is workspace-bounded.

## Confluence AI / Confluence Cloud

- **Positioning:** Atlassian's enterprise wiki with REST API and "Atlassian Intelligence" / "Rovo" AI overlay for Q&A and summarization across Confluence + Jira.
- **Sources:**
  - https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/
  - https://developer.atlassian.com/cloud/confluence/rest/v2/intro/
  - https://support.atlassian.com/organization-administration/docs/atlassian-intelligence-features-in-confluence/
  - https://confluence.atlassian.com/confkb/how-to-detect-5mb-of-text-on-page-858576591.html
  - https://community.developer.atlassian.com/t/is-there-a-size-limit-for-body-storge-when-updating-a-page-with-the-rest-api/58055
- **Reliability:** Official docs + KB.
- **Relevance:** HIGH — Atlassian-shop enterprises will already have Confluence; pushing transcripts as pages is well-supported.
- **Custom ingestion API:** YES. Confluence Cloud REST v2: `POST /pages` (creates page in space/parent with `storage` or `atlas_doc_format` body). OAuth2 (3LO) or API token + email auth. Attachments via separate endpoint. Markdown not native; requires conversion to storage format (XHTML) or ADF.
- **Volume limits:** ~5 MB REST save-request limit per page (Atlassian KB). Pagination caps results at 50 by default. Typical page rate limit governed by per-tenant plan. For long transcripts you'd split across multiple pages or attach as files.
- **Search:** Lexical search via CQL; Atlassian Intelligence (Rovo) adds semantic + agentic Q&A across Confluence/Jira on Premium/Enterprise plans.
- **RAG/QA:** YES via Atlassian Intelligence/Rovo — answers questions across spaces with citations, respects permissions.
- **Visibility model:** Space → page restrictions → group/user permissions. Robust enterprise RBAC.
- **Pricing tier for API:** API is available on all paid tiers (Free/Standard/Premium/Enterprise). Atlassian Intelligence features require Premium or higher; Rovo agents typically Enterprise-tier.
- **Data residency:** SaaS with data residency options (US, EU, AU, DE, etc.) on Premium+. Confluence Data Center (self-hosted) still available for on-prem with separate REST API.
- **Precedent for chat-transcript ingestion:** Some teams archive standups/meeting summaries (incl. AI-generated) to Confluence pages. No widely cited "AI conversation log" reference, but mechanically routine.
- **Architectural fit:** Strong for Atlassian-shop orgs; the storage-format conversion + 5 MB limit + page-creation rate make it less ideal for high-frequency chat ingestion. Better for daily/weekly digest pages than per-turn capture.

## Slite

- **Positioning:** Lightweight team knowledge base / docs product with "Ask" AI assistant for team Q&A.
- **Sources:**
  - https://slite.com/integrations/api
  - https://developers.slite.com/reference/createnote
  - https://developers.slite.com/
  - https://slite.slite.page/p/06Fmm1hluSnD3X/Ask
- **Reliability:** Official.
- **Relevance:** MEDIUM — straightforward note-creation API; "Ask" gives basic RAG. Smaller scale than Notion/Confluence.
- **Custom ingestion API:** YES. `POST /v1/notes` (createNote) accepts markdown + parentNoteId/folderId. API-key auth. OpenAPI spec published.
- **Volume limits:** Not prominently published; presumed permissive markdown body. Per-account rate limits expected (standard 429 backoff).
- **Search:** Lexical + Ask (semantic).
- **RAG/QA:** YES — "Ask" answers across team knowledge base with citations.
- **Visibility model:** Workspace + channel + note-level permissions; team RBAC.
- **Pricing tier for API:** API available on Standard/Premium/Enterprise paid plans. Ask AI usually requires Premium+.
- **Data residency:** SaaS only; EU hosting options on Enterprise.
- **Precedent for chat-transcript ingestion:** No notable public precedent.
- **Architectural fit:** Decent if Slite is already the team wiki; otherwise low value relative to Notion/Confluence.

## Outline (getoutline.com)

- **Positioning:** Open-source-licensed (BSL) team wiki with strong API; can be self-hosted.
- **Sources:**
  - https://docs.getoutline.com/s/guide/doc/api-1rEIXDfLF6
  - https://docs.getoutline.com/s/guide/doc/import-D2ZvLqz411
  - https://www.getoutline.com/
  - https://github.com/outline
- **Reliability:** Official + GitHub.
- **Relevance:** MEDIUM-HIGH — uniquely on-prem-capable in this bucket; markdown-native API.
- **Custom ingestion API:** YES. `documents.create` (markdown body, collectionId, parentDocumentId) and `documents.import` (file upload). API key auth. JSON-RPC-ish style (POST endpoints with action names).
- **Volume limits:** Self-hosted = limits are your DB. Cloud has plan-based document/storage caps but no aggressive per-page size limit on markdown text.
- **Search:** Postgres full-text (lexical); newer cloud builds add AI features. Self-hosted does not include managed RAG by default.
- **RAG/QA:** Limited — Outline cloud has experimental AI features; self-hosted requires you to bolt on your own (e.g., via `documents.search` API + your own embeddings).
- **Visibility model:** Collection + document permissions, group ACLs. Decent RBAC.
- **Pricing tier for API:** API is free on all cloud tiers and free in self-hosted (open source).
- **Data residency:** **On-prem / self-host supported** (Docker, Postgres, Redis). Cloud SaaS also offered (US/EU).
- **Precedent for chat-transcript ingestion:** Minor — open-source nature means custom integrations exist in community, but no flagship reference.
- **Architectural fit:** Strong if you want a self-hosted wiki to own AI conversation logs with markdown-native ingestion; weaker on built-in RAG/AI compared to managed peers.

## Guru (getguru.com)

- **Positioning:** Card-based knowledge management with verification workflows; Guru Answers AI delivers RAG over connected sources.
- **Sources:**
  - https://help.getguru.com/docs/gurus-api
  - https://developer.getguru.com/reference/postv1answerscreateanswer
  - https://developer.getguru.com/docs/guru-mcp-server-overview
  - https://help.getguru.com/docs/linking-sources-for-guru-answers
  - https://developer.getguru.com/docs/syncing-cards
- **Reliability:** Official.
- **Relevance:** MEDIUM-HIGH — Guru explicitly supports custom-source ingestion for Answers and ships an MCP server, so AI conversation transcripts as a source is unusually well-aligned.
- **Custom ingestion API:** YES. Card creation/update endpoints; Sources for Answers can be linked from external systems. Guru also publishes an MCP server (read/write to cards from Claude/ChatGPT/Cursor). Auth via API token (user + collection).
- **Volume limits:** Card content is HTML; practical card size in tens of KB. Bulk card sync supported but rate-limited per tenant.
- **Search:** Hybrid (lexical + Guru Answers semantic). Permission-aware.
- **RAG/QA:** YES — Guru Answers is a first-class feature with cited responses. `POST /v1/answers` lets you ask programmatically.
- **Visibility model:** Collection + group permissions; trust score / verification metadata is a Guru-specific concept.
- **Pricing tier for API:** API access on Builder/Enterprise plans (paid). Guru Answers (AI) typically Enterprise tier.
- **Data residency:** SaaS; Enterprise data residency options.
- **Precedent for chat-transcript ingestion:** Indirect — MCP server precedent suggests Guru is leaning into AI-tool integration; no flagship "ingest your AI chat history" case study yet.
- **Architectural fit:** Solid for verified-knowledge cultures; less ideal as a high-volume raw-transcript sink because cards are meant to be curated/verified, not append-only logs.

## Bloomfire

- **Positioning:** Enterprise knowledge engagement platform aimed at support/CX/insights teams; AI search and contributor analytics.
- **Sources:**
  - https://bloomfire.com/build-with-bloomfire/
  - https://bloomfire.com/integrations/
  - https://bloomfire.com/platform/ai-authoring-tools/
  - https://docs.celigo.com/hc/en-us/articles/21882754723099-Available-Bloomfire-APIs
- **Reliability:** Official + Celigo (third-party iPaaS docs).
- **Relevance:** LOW-MEDIUM — APIs exist (REST) but documentation is gated/sales-led; ecosystem and developer momentum are smaller than peers.
- **Custom ingestion API:** YES (limited public visibility). Public REST endpoints documented via partner integrations (Celigo) include create-post / upload-content operations. Direct developer portal is sparse; full API reference often shared under NDA / customer success.
- **Volume limits:** Not publicly published.
- **Search:** Hybrid (lexical + AI semantic / "AI Authoring" features).
- **RAG/QA:** YES — AI search and answers over the corpus.
- **Visibility model:** Series + group permissions; enterprise RBAC.
- **Pricing tier for API:** Enterprise-only; sales-led.
- **Data residency:** SaaS multi-tenant; enterprise residency on request.
- **Precedent for chat-transcript ingestion:** None publicly documented.
- **Architectural fit:** Weak general fit — Bloomfire is optimized for vetted Q&A/insight content for support orgs, not raw engineer-AI dialog. Possible but inferior to Glean/Notion/Confluence for this purpose.

## Enterprise-Knowledge Comparison Table

| Platform | Ingestion API | Search | RAG | Visibility | API tier | Residency | Fit |
|---|---|---|---|---|---|---|---|
| Glean | Indexing/Push API (custom datasource) | Hybrid | Yes (Glean Assistant) | Permission-aware ACLs | Enterprise-only | SaaS (US/EU, dedicated) | Excellent if already deployed |
| Mem (mem.ai) | `mem-it` REST | Lexical + AI recall | Yes | Per-user | Paid (Mem+) | SaaS US | Weak (personal-first) |
| Notion AI | Pages/Blocks REST API | Lexical + Notion AI | Yes (paid AI add-on) | Page/DB RBAC | Free (paid plans for AI) | SaaS US/EU | Strong (low friction) |
| Coda AI | REST + Pack SDK | Lexical, doc-scoped | Yes (Coda AI/Brain) | Doc-level | Paid (Pro+) | SaaS | Mediocre |
| Slack AI | `chat.postMessage`, files, canvas | Lexical + Slack AI | Yes (Enterprise + AI add-on) | Channel ACL | API free; AI Enterprise | SaaS (residency on Grid) | OK as shadow capture |
| Confluence AI | Pages REST v2 (storage/ADF) | CQL + Atlassian Intelligence | Yes (Premium+/Rovo) | Space/page RBAC | Paid (AI Premium+) | SaaS + Data Center | Strong for Atlassian shops |
| Slite | Notes REST | Lexical + Ask | Yes (Ask) | Workspace RBAC | Paid (Standard+) | SaaS (EU on Ent) | Decent |
| Outline | Documents REST (markdown) | Postgres FTS | Limited (cloud only) | Collection/doc RBAC | Free (OSS / cloud) | **On-prem + SaaS** | Strong if self-hosted needed |
| Guru | Cards API + MCP server | Hybrid + Answers | Yes (Guru Answers) | Collection RBAC + verify | Paid (Builder+/Ent) | SaaS | Solid for curated KB |
| Bloomfire | REST (private docs) | Hybrid + AI | Yes | Series/group RBAC | Enterprise-only | SaaS | Weak general fit |

## Key External Findings

- Every platform in this bucket exposes a documented REST ingestion path; the question is fit, not feasibility. The decision hinges on whether transcripts can be pushed at the *cadence* and *granularity* the platform expects.
- Glean is the only one purpose-built for *arbitrary corporate text artifact ingestion with permission-aware enterprise search*; it is the strongest "drop transcripts in and get RAG for free" option, but is enterprise-only and sales-gated.
- Notion and Confluence are the most likely "already deployed" targets and have well-trodden write APIs, but rate limits, block-schema chunking, and 5 MB page caps make per-turn streaming awkward — they suit batched/digest ingestion.
- Slack's `chat.postMessage` is the cheapest possible "drop transcripts somewhere indexable" path because Slack is ubiquitous, but Slack AI quality is workspace-bounded and message size limits force chunking.
- Outline is the standout if **on-prem / self-host** is a hard requirement — it has the only fully open-source, markdown-native API in the bucket. Trade-off: you bring your own RAG layer.
- Guru's MCP server is a notable signal: Guru is actively building bidirectional AI-tool integration, suggesting AI conversation transcripts could land naturally as Guru cards or sources.
- Mem and Bloomfire are tail options. Mem is personal-first; Bloomfire is support-team-first with sales-gated API docs.
- Coda is feasible but its sweet spot is structured operational docs, not narrative transcript retrieval.
- None of these platforms ships a publicized "AI conversation transcript" connector out of the box. Every implementation would be custom, but Glean/Notion/Confluence/Outline/Guru would each take days, not months.

## Recommendations from External Research

- Position Bucket E as **a low-cost adoption path for orgs that already operate one of these platforms**, not a primary architectural target. The comparables analysis should treat them as *integration sinks*, not standalone solutions.
- Distinguish two sub-tiers within Bucket E:
  - **Tier E1 — Enterprise-grade, RAG-native, high friction to adopt fresh:** Glean, Confluence AI, Bloomfire. Recommend only if already deployed.
  - **Tier E2 — Wiki/notes APIs with simpler ingestion, broader deployment:** Notion, Outline, Slite, Guru, Coda, Slack. Lower friction; Notion/Slack/Outline are the realistic universal options.
- For the unified-engineer-AI-conversation architecture, the strongest "bring-your-own enterprise sink" recommendation is a **pluggable ingestion adapter** that targets, in priority order: Glean (if available) → Notion → Confluence → Outline (self-host) → Slack (fallback shadow). This matches where engineering teams actually put knowledge.
- For self-hosted / data-residency-sensitive customers, Outline is the only realistic in-bucket fit. All other on-prem stories require Confluence Data Center or vendor-specific dedicated deployments.
- The MCP server pattern Guru ships is the right interoperability signal for the future; recommend the project's ingestion adapters expose an MCP-compatible surface so any of these tools can consume AI transcripts symmetrically.
- Markdown is the lingua franca for ingestion across this bucket (Notion supports it via guide, Outline native, Slite native, Slack via mrkdwn, Glean accepts text/HTML, Confluence requires storage/ADF). Standardize transcript export as Markdown + structured metadata to maximize fan-out compatibility.
- Rate limits and per-document size caps mean the ingestion design should batch transcripts into digest documents (per session or per day), not stream per-turn — this is universally true across Notion (3 rps), Confluence (5 MB), Slack (1 msg/s/channel), and even Glean (bulk preferred).
