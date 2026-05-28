# Synthesis: Open Questions + Evidence Trail

**Source files:** all research files + qa/gaps-and-questions.md + research-notes.md
**Target sections:** 9 (Open Questions), 10 (Evidence Trail)
**Date:** 2026-05-01

---

## 9. Open Questions

The questions below capture real residual uncertainty in this report. They are grouped into:
(a) UNVERIFIED claims surfaced by the research-completeness gate that the synthesis chose to retain rather than excise; (b) two scoping judgment calls flagged in `research-notes.md` AMBIGUITIES_FOR_USER (addressed by the synth-04 Section 7 recommendation, but worth confirming with stakeholders before implementation); (c) competitive-landscape items that could materially affect the build/buy/adopt decision over the next 6–12 months; and (d) cross-partition reconciliation choices that synthesis made on its own authority and should be sanity-checked.

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|---------------------|
| 1 | What is SpecStory's actual paid-tier pricing? `/pricing` returns 404 and the Teams page is a Design Partner application form. (Gap I1) | Blocks an apples-to-apples adopt-vs-build cost comparison in Section 6/7. Recommendation currently assumes "free OSS today + custom enterprise pricing TBD." | Submit a Design Partner application via `specstory.com/teams`, or contact SpecStory sales directly, before committing to an adopt-path budget. |
| 2 | Has SpecStory's "RAG coming soon" actually shipped, and on what timeline? Roadmap rests on unreachable `beta.specstory.com` references; no shipped product to verify. (Gap I2) | Synth-04 Section 7 recommends NOT waiting on SpecStory RAG. If it ships in <90 days with strong team-aggregation, the build-vs-adopt calculus flips. | Track SpecStory's GitHub releases, blog, and X/Twitter weekly through the planned implementation horizon. Re-evaluate the recommendation if RAG ships before Phase 2 of the build plan completes. |
| 3 | Is the Voyage / MongoDB acquisition claim (web-07) accurate as stated, and what license/availability changes followed? Claim appears in web-07 without a primary URL citation. (Gap I4 — `[UNVERIFIED]`) | If Voyage embeddings are recommended in Section 6/8 but acquisition altered terms (e.g., MongoDB-Atlas-only access), the BYO stack guidance breaks. | Verify against MongoDB's official press release archive and Voyage's current pricing/licensing docs before any embedding-vendor commitment. |
| 4 | Are Cursor and Notion AI confirmed Turbopuffer customers? (web-07 claim, no URL citation. Gap I4 — `[UNVERIFIED]`) | Used as social-proof in vector-DB selection. If false, Turbopuffer's positioning weakens and BYO ranking shifts. | Search Turbopuffer's customer page / case studies; check Cursor and Notion AI engineering blogs for stack disclosures. |
| 5 | Is Mastra's claimed "10x cost reduction" reproducible, on what workload, vs. what baseline? (web-07 claim, no URL citation. Gap I4 — `[UNVERIFIED]`) | Cost claims that don't survive scrutiny would weaken any Mastra-anchored BYO recommendation. | Locate the original Mastra benchmark post or whitepaper; reproduce on an internal representative workload before relying on the figure. |
| 6 | Does Open WebUI's license actually contain a clause requiring branding preservation for deployments >50 users? Sourced to an unlinked Reddit thread. (Gap I6 — `[UNVERIFIED]`) | If the clause exists, Open WebUI as an adopt-path option in Section 6 carries a re-branding constraint that affects internal rollout. If it does not, that risk drops out. | Read the actual `LICENSE` file in the Open WebUI GitHub repo at the version under consideration; confirm with their maintainers if ambiguous. |
| 7 | What is the exact license of the `arize-phoenix-otel` adjacent package? web-04 notes "Elastic-2.0 in some channels — verify per package." (Gap I7) | Phoenix is short-listed as an observability option. An Elastic-2.0 sub-package would constrain self-hosted commercial use. | Check the package's PyPI metadata and the Arize GitHub repo `LICENSE` for that specific package, not just the umbrella `arize-phoenix` repo. |
| 8 | Is Voyage's "+13.8% over text-embedding-3-large on code retrieval" a single benchmark or an average across several? web-07 wording is imprecise ("+13.8% to +16.3% average"). (Gap I5) | Affects how confidently we cite the uplift in Section 6/8 vendor comparison. | Locate Voyage's primary benchmark post for `voyage-code-3` and pin the exact metric, dataset, and baseline. |
| 9 | Should LLM observability platforms (LangSmith, Langfuse, Helicone, Phoenix, etc.) be in scope as comparables? They capture LLM conversations between IDE and model — but they instrument the call path rather than harvest IDE chat archives. (research-notes AMBIGUITY 1) | Synth-04 Section 7 evaluates both architectures and includes observability as a partial comparable, but stakeholders may want to narrow scope to "harvest existing IDE chat archives only." | Confirm with the user/sponsor: should the project capture LLM calls at the proxy boundary, harvest existing local chat files, or both? Decision changes the bucket weighting in Section 5/6. |
| 10 | What does "unified single database" mean operationally? (a) one product covering everything, (b) one pipeline assembling outputs from many tools into a shared store, or (c) team-wide deployment of one of the above. (research-notes AMBIGUITY 2) | Synth-04 Section 7 evaluates all three; the recommendation leans toward (b) the pipeline model. If the sponsor expects (a) a single off-the-shelf product, the recommendation must change. | Confirm with the sponsor in writing before kicking off the implementation plan. The answer determines whether the work is integration engineering or vendor selection. |
| 11 | When does Cursor ship, or expand, its "Generate Cursor Rules from chat history" feature, and how broadly? Identified by web-02 as the biggest medium-term competitive threat. (Gap M3) | If Cursor's native feature evolves into team-wide chat aggregation + RAG, much of the build-path value disappears. The decision window for "build" narrows. | Subscribe to the Cursor changelog (track v0.50+ releases) and watch their docs/forum for any "team chat history" or "rules from team history" expansion. Re-evaluate at each Cursor minor version. |
| 12 | Is the cross-partition deduplication choice (AnythingLLM → web-05 primary; Pieces → web-08 primary; Cline Memory Bank → web-08 primary; MCP memory → substrate not competitor; Spool → web-07 primary; Onyx → web-05 primary) the right framing for Section 5? Synthesis decided this on its own authority per Gap M1. | If a primary-source choice is wrong, Section 5 entries may underweight or miss key capabilities (e.g., treating Pieces only as adjacent and missing its LTM-as-substrate angle, or vice versa). | Have a domain reviewer (or the rf-qa synthesis-gate) sanity-check the primary-source assignments before final assembly. Adjust if any product was materially miscategorized. |
| 13 | Are all web-07 sources actually Official-or-Repo reliability, as synthesis treats them by default? (Gap I9 — file lacks per-row Reliability tags) | If a load-bearing claim in Section 5/6/8 originated from a lower-reliability source, downstream confidence is overstated. | When citing any specific web-07 claim in the final report, re-open the source and tag it explicitly; default-Official is a synthesis convenience, not a verified file-level property. |

---

## 10. Evidence Trail

### 10.1 Codebase Research

| File | Topic | Agent Type | Status |
|------|-------|------------|--------|
| `research/01-native-storage-formats.md` | Native conversation storage formats of mainstream AI coding tools (Cursor, Claude Code, Aider, Continue.dev, Cline, Roo Code, Copilot CLI, Gemini CLI, Codex CLI): on-disk paths, file format (JSON/Markdown/SQLite), schema fields captured, per-machine vs. synced, deprecation flags. Establishes the "as-is" baseline that any unified-context system must ingest from. | Pattern Investigator | Complete |

### 10.2 Web Research

| File | Topic | Status |
|------|-------|--------|
| `research/web-01-specstory-deep-dive.md` | SpecStory deep-dive: features, architecture, OSS license, cloud product, pricing (unobtainable — Design Partner gated), team-aggregation status, RAG-coming-soon roadmap, Agent Skills, Cursor-rules generation, API surface. | Complete |
| `research/web-02-direct-competitors.md` | Direct competitors positioned as "capture AI coding chats, sync, search across team" — landscape, deployment models, supported tools, RAG/team aggregation status, pricing. Includes Cursor's own "Generate Rules from chat history" as a medium-term threat. | Complete |
| `research/web-03-memory-layer.md` | AI agent memory layer: Mem0, Letta (MemGPT), Zep, Cognee, Graphiti, LangMem, SuperMemory, Mastra Memory, Basic Memory MCP. Abstraction model, multi-user/team support, self-host options, pricing, ingestion shape. | Complete |
| `research/web-04-observability-platforms.md` | LLM observability platforms: LangSmith, Langfuse, Helicone, Arize Phoenix, HoneyHive, Braintrust, PromptLayer, W&B Weave, Opik (Comet), Lunary, AgentOps, Traceloop. Conversation capture, search, replay, dataset/RAG export, self-host vs. SaaS, license per platform. | Complete |
| `research/web-05-self-hosted-chat.md` | Self-hosted / OSS chat platforms: Open WebUI, LibreChat, AnythingLLM, Onyx (formerly Danswer), Chatbox. Chat-history storage, multi-user, RAG over chat history, external-chat ingestion APIs, team aggregation. | Complete |
| `research/web-06-enterprise-knowledge.md` | Enterprise org-memory & knowledge platforms: Glean, Mem (mem.ai), Notion AI, Coda AI, Slack AI, Confluence AI, Slite. Can they index AI conversation transcripts as another data source? Connectors, custom-ingestion APIs, pricing tier required. | Complete |
| `research/web-07-byo-rag-stack.md` | Build-your-own RAG-over-conversations: vector DBs (Pinecone, Weaviate, Qdrant, Chroma, Milvus, pgvector, Turbopuffer); embedding APIs (OpenAI, Voyage, Cohere); pipeline tools (LlamaIndex, LangChain, Haystack, txtai, Mastra); reference architectures and cost-precedent (Spool). | Complete |
| `research/web-08-adjacent-tools.md` | Adjacent / less-direct tools: Charlie Mnemonic, Pieces for Developers (LTM cross-IDE), Continue Hub, Cursor team features, Cline Memory Bank, MCP-memory servers (mcp-memory, basic-memory), Sourcegraph Cody history, JetBrains AI Assistant team features. Brief positioning + relevance to the unified-context goal. | Complete |

### 10.3 Synthesis Files

| File | Sections produced |
|------|-------------------|
| `synthesis/synth-01-problem-current-state.md` | Section 1 (Problem Statement), Section 2 (Current State Analysis) |
| `synthesis/synth-02-target-gaps.md` | Section 3 (Target State), Section 4 (Gap Analysis) |
| `synthesis/synth-03-external-findings.md` | Section 5 (External Research Findings — the consolidated comparables landscape, with cross-partition reconciliation per Gap M1/M2) |
| `synthesis/synth-04-options-recommendation.md` | Section 6 (Options Analysis), Section 7 (Recommendation — addresses the two AMBIGUITIES_FOR_USER) |
| `synthesis/synth-05-implementation-plan.md` | Section 8 (Implementation Plan) |
| `synthesis/synth-06-questions-evidence.md` | Section 9 (Open Questions), Section 10 (Evidence Trail) — this file |

### Gaps Log

The research-completeness gate (Phase 3) initially returned **FAIL** on both partition reports. The failures were gate-driven rather than substantive: 5 files (web-01, web-03, web-04, web-05, web-08) carried `Status: In Progress` markers that needed flipping to `Complete`, plus 2 minor content corrections in web-04 (the Helicone OSS license needed correction from "MIT-style" to Apache-2.0, and a duplicated "Activity signal" line under Phoenix needed merging). Exactly **one fix-cycle** was applied: 5 status flips and 2 in-place content fixes in web-04. After that fix-cycle, the merged research-gate verdict was **PASS (post-fix)**, and Phase 5 synthesis was authorized to proceed. Both QA partition reports explicitly noted that, with status fields corrected, remaining minor findings could be deferred to synthesis (Sections 4, 6, and 9) without re-spawning research — which is what happened: Important gaps I1–I9 and Minor gaps M1–M6 from `qa/gaps-and-questions.md` are carried forward into Sections 4, 5, 6, and the Section 9 Open Questions table above. **No synthesis-gate fix cycles have been run yet** — those are scheduled as part of Phase 5 QA and will be appended to this Gaps Log if/when triggered.
