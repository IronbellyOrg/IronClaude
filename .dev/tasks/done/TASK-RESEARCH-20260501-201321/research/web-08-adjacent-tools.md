# Research: Adjacent / less-direct tools

**Topic:** Tools that don't fit buckets A-G but may still be relevant
**Status:** Complete
**Date:** 2026-05-01

---

## Charlie Mnemonic (GoodAI)

- **Positioning:** Open-source personal LLM assistant with long-term memory; not a code-context tool, but an early agent-with-memory reference design.
- **Sources:** https://github.com/GoodAI/charlie-mnemonic, https://www.goodai.com/charlie-mnemonic/, https://www.goodai.com/introducing-charlie-mnemonic/
- **Reliability:** Official (GoodAI repo + GoodAI announcement)
- **Relevance:** LOW
- **Captures conversation?:** Yes — but personal/single-user agent context, not engineer-AI-pair-programming sessions
- **Team-aware:** No (explicitly positioned as a personal assistant)
- **RAG over its captures:** Implicit retrieval over stored memory; not explicitly framed as RAG, no team-search surface
- **Composability with SpecStory-style ingestion:** Could not — it is a self-contained agent runtime, not a capture pipeline; would require re-using its memory subsystem in isolation, which is more effort than worth
- **Verdict:** ignore (interesting reference architecture only)
- **Notes:** The original GitHub link in the prompt (`amadad/charliemnemonic`) returns 404. Canonical repo is `GoodAI/charlie-mnemonic`. The "personal" framing means it explicitly does not solve the team-shared transcript-database problem.

---


## Pieces for Developers

- **Positioning:** Cross-IDE/cross-app capture layer for code snippets, AI conversations, and OS-level context, with on-device LTM and "continue this chat in another tool" workflows.
- **Sources:** https://pieces.app/features/copilot, https://pieces.app/features/context-switching, https://pieces.app/features/generate
- **Reliability:** Official product pages
- **Relevance:** HIGH
- **Captures conversation?:** Yes — explicitly captures AI Copilot chats and supports continuing the same chat across IDEs/browsers
- **Team-aware:** Partial — primarily individual/local-first; team sharing is via snippet/chunk sharing rather than a shared chat database
- **RAG over its captures:** Yes — Pieces Copilot uses local context (LTM, files, snippets) as RAG context for chats; queryable
- **Composability with SpecStory-style ingestion:** Could (partial) — Pieces is itself an ingestion+retrieval product; unclear if it exposes a clean export/API for piping captures into a separate unified store. Most likely **competes with**, rather than feeds, a custom unified DB. May be worth testing as a frontend over a SpecStory-style backend if exports are usable.
- **Verdict:** further-investigation-needed
- **Notes:** This is the closest *architectural* analogue to "engineer-AI context bus" — it captures across many tools, not just one IDE. Worth a bench evaluation specifically for: (1) export format, (2) ability to ingest external transcripts, (3) team workspace SKU.

---

## Continue.dev Hub

- **Positioning:** Continue's hub for discovering, creating, and sharing custom AI coding assistants ("blocks" and "bundles") with private/team/public visibility.
- **Sources:** https://hub.continue.dev/, https://docs.continue.dev/hub/blocks/bundles, https://docs.continue.dev/guides/understanding-assistants, https://techcrunch.com/2025/02/26/continue-wants-to-help-developers-create-and-share-custom-ai-coding-assistants/
- **Reliability:** Official docs + reputable press
- **Relevance:** LOW
- **Captures conversation?:** No — Hub shares *configurations* (rules, prompts, model setups, MCP blocks), not chat transcripts
- **Team-aware:** Yes — explicit team/org governance for assistant sharing
- **RAG over its captures:** No (over the hub itself; assistants built on Continue can do their own RAG, but that's a separate question)
- **Composability with SpecStory-style ingestion:** Could not for chats; Hub is the wrong layer. However, an assistant defined in Continue Hub could *consume* a SpecStory-style RAG store as an MCP block — relevant as a distribution surface, not a capture layer
- **Verdict:** ignore (for the chat-capture goal); pipeline-with on the publishing side if we want devs to plug a unified-history MCP block into their Continue assistants
- **Notes:** Useful framing: Continue Hub demonstrates that **shared assistant configuration** is a separate market from **shared conversation history**. SpecStory occupies the latter; Continue Hub the former.

---

## Cursor — team features and `.cursor/rules`

- **Positioning:** Cursor offers per-project `.cursor/rules` (which can be checked into the repo and thus team-shared) and local SQLite chat history with `@Past Chats` retrieval; cross-device chat sync and team-shared chat history are still community-requested.
- **Sources:** https://docs.cursor.com/agent/chat/history, https://docs.cursor.com/context/rules, https://forum.cursor.com/t/is-cross-device-sync-possible/147030, https://forum.cursor.com/t/ability-to-share-conversations-with-other-people/151763
- **Reliability:** Official docs + community forum
- **Relevance:** MEDIUM
- **Captures conversation?:** Yes — locally, in SQLite, with `@Past Chats` retrieval inside Cursor
- **Team-aware:** Partial — `.cursor/rules` files travel with the repo (team-shareable) and there are some read-only conversation-link share affordances; cross-device chat sync not officially supported
- **RAG over its captures:** Limited — `@Past Chats` provides retrieval inside Cursor, but no external RAG API and no team-wide search surface
- **Composability with SpecStory-style ingestion:** Could (partial) — local SQLite is a known SpecStory ingestion target for the Cursor flavor. The rules files are not transcripts and don't belong in the chat DB.
- **Verdict:** pipeline-with — keep as one of the capture sources feeding the unified store
- **Notes:** Cursor's stance reinforces the gap SpecStory fills: chat history is local-only and rules are repo-only. There is no first-party "team chat search" product from Cursor today.

---

## Cline Memory Bank

- **Positioning:** A "persistent rules pattern" — a curated set of markdown files (`projectbrief.md`, `productContext.md`, `activeContext.md`, `progress.md`, etc.) that Cline reads at the start of every session to reconstruct project context.
- **Sources:** https://www.mintlify.com/cline/cline/features/memory-bank, https://www.mintlify.com/cline/cline/customization/cline-rules, https://deepwiki.com/cline/prompts/4.2-memory-bank-system
- **Reliability:** Official docs
- **Relevance:** LOW (architectural reference; not a transcript store)
- **Captures conversation?:** No — captures distilled *project state* in markdown files, not raw chat transcripts
- **Team-aware:** Yes by accident — files are checked into the repo and shared via git
- **RAG over its captures:** No — these are read whole-file at session start, not retrieved
- **Composability with SpecStory-style ingestion:** Could (partial) — Memory Bank files are an interesting *write target* for a unified system that summarizes recent chats into project state, but they are not raw transcripts
- **Verdict:** ignore (as a transcript source); reference-only for "git-versioned project memory" pattern
- **Notes:** Cline Memory Bank is a manual discipline pattern, not a product. Useful as inspiration for "what an LLM should write back to the repo as durable summaries" but does not solve the capture problem.

---

## MCP Memory Servers (general category)

- **Positioning:** A growing class of MCP servers that give LLM agents persistent memory primitives — knowledge graphs, markdown notebooks, vector stores, or project-scoped JSON banks — accessible via MCP tool calls.
- **Sources:** https://github.com/modelcontextprotocol/servers, https://mcpservers.org/servers/modelcontextprotocol/servers, https://github.com/TensorBlock/awesome-mcp-servers, https://model-context-protocol.com/servers/awesome-mcp-servers
- **Reliability:** Official MCP repo + community-curated lists
- **Relevance:** HIGH (as a substrate / alternative architecture)
- **Captures conversation?:** Indirectly — agents *write* facts/observations into the memory server during conversations; raw transcripts are not the unit of capture
- **Team-aware:** Depends on the server — most reference impls are local; some (Memory Bank MCP variants) support PostgreSQL/Qdrant/MongoDB backends suitable for team deployment
- **RAG over its captures:** Yes for vector-backed and graph-backed servers (e.g., the official Memory server is knowledge-graph based; Memory Bank MCP has pgvector/Qdrant variants)
- **Composability with SpecStory-style ingestion:** Could — an MCP memory server is a plausible **substrate** for a unified store. SpecStory-style ingestion would write transcripts into it; agents would query it via MCP. This is the most architecturally interesting alternative architecture in this bucket.
- **Verdict:** further-investigation-needed (as substrate, not as competitor)
- **Notes:** See the dedicated table below for the top servers. Important architectural insight: **MCP-memory + custom ingestion** is a plausible build path that piggybacks on a standard protocol layer.

---

## Sourcegraph Cody — chat history and team features

- **Positioning:** Enterprise code-AI with team/admin tooling, repo-aware retrieval, and per-user chat session history; chat history is per-user, not a team-shared search surface.
- **Sources:** https://sourcegraph.com/docs/cody/enterprise/features, https://sourcegraph.com/docs/cody/capabilities/chat, https://sourcegraph.com/docs/cody
- **Reliability:** Official docs
- **Relevance:** MEDIUM
- **Captures conversation?:** Yes — Cody keeps chat session history for each user
- **Team-aware:** Partial — Enterprise plans have admin/team management, but chat history itself is per-user; no documented "team chat search" feature comparable to SpecStory's vision
- **RAG over its captures:** Cody does heavy RAG over **code**, not over **chat history**
- **Composability with SpecStory-style ingestion:** Could not directly — Cody's chat history surface is closed; no documented export API for transcripts
- **Verdict:** ignore (for the chat-capture goal); known gap, not a candidate
- **Notes:** Reinforces the pattern: enterprise code-AI vendors (Cody, Copilot Enterprise, JetBrains AI) all have per-user chat history but **none ship a team-shared, indexed chat-history search product**. That is exactly the SpecStory-shaped gap.

---

## JetBrains AI Assistant — team features

- **Positioning:** JetBrains' in-IDE AI with per-project, per-user chat history stored across IDE sessions.
- **Sources:** https://www.jetbrains.com/help/ai-assistant/chat-mode.html, https://www.jetbrains.com/help/ai-assistant/ai-chat.html, https://blog.jetbrains.com/ai/2025/04/jetbrains-ai-assistant-2025-1-2/, https://blog.jetbrains.com/ai/2025/08/jetbrains-ai-assistant-2025-2/
- **Reliability:** Official docs and blog
- **Relevance:** LOW
- **Captures conversation?:** Yes — per-project chat history persists across IDE sessions
- **Team-aware:** Not documented — no first-party "team chat search" feature found in 2025 releases
- **RAG over its captures:** No (over chat history); standard code-aware retrieval otherwise
- **Composability with SpecStory-style ingestion:** Could (partial) if the local store is reachable; would need a SpecStory-style adapter to read JetBrains chat persistence
- **Verdict:** pipeline-with (as a future capture source if/when JetBrains usage matters)
- **Notes:** Same pattern as Cody — local per-user chat history, no team surface.

---

## Tabnine — team and enterprise features

- **Positioning:** Code AI with strong privacy/private-deployment posture, an Enterprise Context Engine doing RAG over team code, and a chat product (GA); supports shared custom commands/personalization for teams.
- **Sources:** https://docs.tabnine.com/, https://docs.tabnine.com/main/welcome/readme/architecture, https://docs.tabnine.com/main/welcome/readme/personalization, https://www.tabnine.com/blog/control-every-interaction-introducing-tabnines-new-personalization-features/, https://www.tabnine.com/blog/december-changelog/, https://www.globenewswire.com/news-release/2025/11/05/3181534/0/en/Tabnine-Launches-Enterprise-Fit-Agentic-AI-Powered-by-Its-Enterprise-Context-Engine.html
- **Reliability:** Official docs/blog + press release
- **Relevance:** LOW
- **Captures conversation?:** Yes (chat product), but the team value-prop is *shared commands/rules*, not shared chat history
- **Team-aware:** Yes (shared commands, admin context controls); but the team feature set is about shared *customization*, not shared *conversation transcripts*
- **RAG over its captures:** Tabnine RAGs heavily over **team code** via the Enterprise Context Engine; not a documented RAG over chat history
- **Composability with SpecStory-style ingestion:** Could not — the chat persistence surface is closed; private-installation deployments may make export possible but would be bespoke
- **Verdict:** ignore (for chat-capture goal)
- **Notes:** Tabnine's "Enterprise Context Engine" branding is interesting — it is what most code-AI vendors call their RAG-over-code substrate. None of them are calling it RAG-over-chat.

---

## Codeium / Windsurf — Cascade Memories and team context

- **Positioning:** Windsurf's Cascade has auto-generated **Memories** (workspace-local) and **Rules / `AGENTS.md`** (recommended for durable team-shared context); marketing claims include shared conversations and curated team knowledge.
- **Sources:** https://docs.windsurf.com/windsurf/cascade/memories, https://docs.windsurf.com/windsurf/cascade/cascade, https://windsurf.com/cascade, https://codeium.mintlify.app/context-awareness/overview
- **Reliability:** Official docs + product page
- **Relevance:** MEDIUM
- **Captures conversation?:** Partial — Memories are *distilled facts* derived from chats, not raw transcripts. Cascade chat history exists but team-share surface is unclear from docs
- **Team-aware:** Partial — Rules/`AGENTS.md` are explicitly recommended for team-shared context; auto-Memories are local
- **RAG over its captures:** Memories are retrieved by Cascade at runtime; no external RAG API documented
- **Composability with SpecStory-style ingestion:** Could (partial) — `AGENTS.md` is a write-target for distilled summaries, similar to Cline Memory Bank; raw conversation export not documented
- **Verdict:** pipeline-with on the write-side (`AGENTS.md`); ignore on the chat-capture side until export is documented
- **Notes:** Reinforces the industry pattern of distinguishing **distilled team rules** (sharable, in-repo) from **raw chat history** (local, per-user, closed).

---

## Devin / Cognition Labs — Knowledge feature

- **Positioning:** Devin is an autonomous engineering agent; the **Knowledge** feature lets organizations share docs/instructions with Devin to improve future tasks. Persistent memory is org-scoped knowledge, not raw chat transcripts.
- **Sources:** https://cognition.ai/, https://docs.devin.ai/enterprise/overview, https://cognitionai.mintlify.app/, https://cognitionai.mintlify.app/product-guides/knowledge
- **Reliability:** Official site + docs
- **Relevance:** LOW
- **Captures conversation?:** Conversations with Devin happen, but the durable memory unit is **Knowledge entries** (curated org docs/instructions), not searchable chat archives
- **Team-aware:** Yes — Knowledge is org-scoped
- **RAG over its captures:** Yes over Knowledge entries; no documented RAG-over-chat-history surface
- **Composability with SpecStory-style ingestion:** Could not — closed SaaS, no documented export of raw session transcripts
- **Verdict:** ignore (for chat-capture goal)
- **Notes:** Same pattern: vendors invest in **curated org knowledge** (cleaner, smaller, retrievable) rather than **raw transcript archives** (messy, large, harder to retrieve cleanly). This is a real signal that SpecStory's "raw transcript indexing" thesis is a distinct market.

---

## Augment Code — Context Engine

- **Positioning:** Augment Code's **Context Engine** is a semantic index over team code, commit history, and team coding patterns, exposed to agents via MCP, SDK, and connectors. IDE agents support team-shared rules/memories.
- **Sources:** https://www.augmentcode.com/context-engine/, https://docs.augmentcode.com/context-services/overview, https://docs.augmentcode.com/context-services/mcp/overview, https://www.augmentcode.com/product/ide-agents, https://docs.augmentcode.com/introduction
- **Reliability:** Official site + docs
- **Relevance:** MEDIUM
- **Captures conversation?:** Indirectly — IDE agents use the Context Engine; team-shared memories/rules are mentioned, but raw chat transcripts are not the indexing unit
- **Team-aware:** Yes — Context Engine is explicitly team-scoped, indexing across team code/history
- **RAG over its captures:** Yes — over team code/patterns/commit history; chat history specifically is not called out as a target
- **Composability with SpecStory-style ingestion:** Could (partial) — the Context Engine MCP surface could in principle accept additional sources beyond code, but this is not documented as a public capability. Worth a deeper look as a *retrieval substrate* if we ever want to push transcripts into a managed system.
- **Verdict:** further-investigation-needed
- **Notes:** Augment is the closest competitor to building a "team RAG over everything engineering produces." If they ever ingest chat transcripts, they become a direct competitor to SpecStory; today they're a code-RAG product.

---

## MCP Memory Servers — Detailed Survey

The following are the most relevant memory-flavored MCP servers as of late 2025 / early 2026. Use these as candidate substrate options if we go the "MCP server + custom ingestion" route.

| Server | Source | Positioning | Activity |
|---|---|---|---|
| `@modelcontextprotocol/server-memory` | https://github.com/modelcontextprotocol/servers (official reference) | Knowledge-graph-based persistent memory; canonical reference impl | Active — maintained by MCP org |
| Basic Memory | https://github.com/basicmachines-co/basic-memory (linked from mcp.directory) | Persistent semantic-graph memory backed by **local Markdown** files; Obsidian-compatible | Active |
| Memory Bank MCP (protocol-lattice) | https://mcpservers.org/servers/protocol-lattice/memory-bank-mcp | Production-ready, vector-native memory bank with **PostgreSQL/pgvector, Qdrant, MongoDB** backends | Active — strongest team-deploy posture |
| Memory Bank MCP (Roo Code variant) | https://www.mcplane.com/mcp_servers/roo-code-memory-bankserver-1 | File-based project context persistence via structured markdown | Less mature |
| `mcp-memory-bank` (PyPI) | https://pypi.org/project/mcp-memory-bank/ | Python-package memory MCP, project-local storage | Active — small footprint |
| Filesystem (reference) | https://github.com/modelcontextprotocol/servers | Not memory per se, but used as durable file substrate by many memory tools | Active |
| TensorBlock awesome-mcp-servers (catalog) | https://github.com/TensorBlock/awesome-mcp-servers | Community-maintained curated list with a Knowledge & Memory section | Active aggregation |
| MCP Registry (official) | https://modelcontextprotocol.io/registry (referenced via mcpfind.org/) | Official discovery layer for MCP servers, including memory | Live |

**Architectural takeaway:** the **Memory Bank MCP (protocol-lattice)** server with pgvector/Qdrant is the most production-credible team-grade substrate. Most of the others are single-user / local-Markdown.

---

## Adjacent-Tools Comparison Table

| Tool | Captures? | Team | RAG | Composable | Verdict |
|---|---|---|---|---|---|
| Charlie Mnemonic | Personal-only | No | Implicit | Could not | ignore |
| Pieces for Developers | Yes (chats + snippets, cross-IDE) | Partial | Yes | Could (partial) | further-investigation-needed |
| Continue Hub | No (configs only) | Yes | No | Could not (chats); pipeline-with on publish | ignore (chat) |
| Cursor team / `.cursor/rules` | Yes (local SQLite) | Partial (rules in repo) | Limited (`@Past Chats`) | Could (partial) | pipeline-with |
| Cline Memory Bank | No (distilled state) | Yes (via git) | No | Could (write-target) | ignore (transcript); reference |
| MCP memory servers | Indirect (facts/observations) | Depends | Yes (graph/vector) | Could (substrate) | further-investigation-needed |
| Sourcegraph Cody | Yes (per-user) | Partial (admin) | No (over chat) | Could not | ignore |
| JetBrains AI Assistant | Yes (per-project local) | No | No | Could (partial) | pipeline-with |
| Tabnine | Yes (chat GA) | Yes (commands/rules) | Code-only | Could not | ignore |
| Codeium / Windsurf Cascade | Partial (Memories distilled) | Partial (Rules/`AGENTS.md`) | Memories at runtime | Could (write-side) | pipeline-with (write); ignore (chat) |
| Devin / Cognition | Curated knowledge only | Yes (org) | Yes (knowledge) | Could not | ignore |
| Augment Code | Indirect (code + patterns) | Yes (org) | Yes (code) | Could (partial) | further-investigation-needed |

---

## Key External Findings

- **The dominant industry pattern is *distilled knowledge*, not *raw chat archives*.** Vendors as a class (Cody, Tabnine, Devin, Augment, Cline, Cascade) invest in curated rules / memory files / org knowledge entries — small, retrievable, hand-maintained — rather than indexing raw conversation transcripts. SpecStory's thesis (index the raw stream) is genuinely contrarian, and the market gap is real.
- **No mainstream code-AI vendor ships a team-shared, indexed, RAG-capable chat-history product today.** Every major IDE-AI keeps chat history per-user/local. Cross-device chat sync is a frequent forum request even for Cursor.
- **Pieces for Developers is the only product in this bucket whose architecture genuinely overlaps with the user's goal.** It captures across IDEs/browsers, supports continuing the same chat across tools, and has on-device LTM. Whether its team SKU and export surface meet the requirement is the open question worth a follow-up evaluation.
- **MCP memory servers are a credible *substrate* layer, not a competitor.** Memory Bank MCP (protocol-lattice) with pgvector/Qdrant is the strongest team-deploy candidate. An "MCP memory server + SpecStory-style ingestion + custom search UI" stack is a plausible build path that rides standard protocol rails.
- **`AGENTS.md` / `.cursor/rules` / Cline Memory Bank are convergent patterns** for distilled, git-versioned, team-shared *project memory*. They are complementary to a transcript store: distill outputs of conversations, write back to repo, but don't replace raw archives.
- **Continue Hub demonstrates a real but separate market** — shared *assistant configurations* (rules, prompts, MCP block bundles). A unified-history product could ship a "Continue Hub block" for distribution, but Hub itself is not a candidate substrate.
- **Cognition's Devin Knowledge feature is the cleanest articulation of the alternate philosophy:** "give the agent curated org knowledge, don't try to mine raw transcripts." This is a real product hypothesis competing with the SpecStory hypothesis.

## Recommendations from External Research

1. **Treat Pieces for Developers as the one tool in this bucket worth a deep-dive evaluation.** Specifically test: (a) chat export format/API, (b) team workspace SKU posture, (c) whether external transcripts can be ingested into Pieces' LTM. If yes to any two, it changes the build/buy/adopt math materially.
2. **Treat MCP memory servers as a candidate *substrate*, not a competitor.** If we build, the Memory Bank MCP (protocol-lattice) variant on pgvector/Qdrant is the strongest off-the-shelf storage+retrieval layer. SpecStory-style capture would write into it via MCP; agents would read via MCP.
3. **Add Cursor local SQLite, JetBrains per-project chat persistence, and Cascade Memories as future ingestion sources** for any unified-store build. They are local-only today, which is exactly the gap a unified store fills.
4. **Do *not* try to compete with Continue Hub, Cline Memory Bank, or `AGENTS.md`.** They occupy the "distilled team rules" market; we should integrate with them as *write-back targets* (the unified store summarizes recent chats and emits `AGENTS.md` updates / Memory Bank patches) rather than replace them.
5. **Mark Cody, Tabnine, JetBrains AI, Devin, and Augment as orthogonal.** They prove the gap (none ship team-shared chat search) but are not candidates we can pipeline with for capture; their chat surfaces are closed.
6. **Architectural takeaway for the build/buy/adopt recommendation:** the most defensible build path is **MCP memory server (substrate) + multi-source ingestion (Cursor SQLite, Claude Code transcripts, etc.) + RAG search UI**, with write-back into the convergent `AGENTS.md` / Memory Bank pattern. SpecStory occupies this exact slot today; the question for buy-vs-build collapses to whether SpecStory's coverage of capture sources and team-search ergonomics is good enough to skip the build.
