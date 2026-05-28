# Analyst Completeness Report — Partition 1 of 2

**Analyst:** rf-analyst
**Partition:** 1 of 2 (files: 01-native-storage-formats.md, web-01..web-04)
**Date:** 2026-05-01
**Depth tier:** Deep

---

## Verdict: FAIL (remediable — 3 critical gaps)

The five assigned files are substantively strong on content depth and source diversity — typically Deep-tier in coverage and citation density. However, two web research files (web-01 SpecStory deep-dive and web-03 Memory Layer) carry a `Status: In Progress` marker rather than `Status: Complete`, which is a hard completeness checkpoint failure under check #4. A third critical issue is web-01's Question 7 (pricing) where the agent stopped at "no public pricing page" without attempting the SpecStory account-signup path that the brief implicitly authorizes for definitive pricing. Several minor data gaps and one minor internal inconsistency exist (web-04 lists `~/Library/Application Support/Cursor` etc. only via web-01 — fine — but mis-categorizes Helicone license as "MIT-style" in prose vs "Apache-2.0" in table). Overall: fix Status markers, attempt one signup-walled pricing pull for SpecStory, address the listed minor gaps, and the partition becomes PASS-grade. Synthesis can proceed only after these fixes — a `Status: In Progress` file violates the gate even if its content is rich.

[PARTITION NOTE: Cross-file checks (contradictions, cross-references, coverage audit against scope) are limited to the 5 files in this partition. Full cross-partition checks require merging with Partition 2's report.]

---

## 1. Coverage Audit

For each file, "Expected items" come from research-notes.md SUGGESTED_PHASES table (key questions / candidate list). "Covered" reflects substantive treatment in the file; "Missing" flags items that are absent or only superficially treated.

| File | Expected items (from brief) | Covered | Missing | Severity |
|---|---|---|---|---|
| 01-native-storage-formats | Cursor, Claude Code, Aider, Continue.dev, Cline, Roo Code, Copilot CLI, Gemini CLI, Codex CLI; for each: storage path, file format, schema fields, what's captured, what's missing, per-machine vs synced, team aggregation OOB | All 9 tools covered with all 7 fields each + cross-tool table + key-takeaways | Note: Cursor is `[DOC-ONLY]` — agent did not attempt empirical SQLite dump even though Cursor is the highest-stakes storage target (largest install base per web-02). Mild schema underspec for Cline/Roo/Copilot CLI (all `[DOC-ONLY]` / `[UNVERIFIED]` at field level) | Minor |
| web-01 SpecStory deep-dive | Storage format, sync, cloud schema, search, API surface, Agent Skills, OSS license, paid tiers, team features (current+roadmap), RAG roadmap, Cursor-rules generation | Storage (HIGH), sync (HIGH), cloud schema (HIGH), API surface incl. auth+errors (HIGH), Agent Skills incl. install (HIGH), OSS license (HIGH), team features (HIGH for current; ROADMAP partial), RAG roadmap (PARTIAL — beta site unreachable), Cursor-rules (LOW detail — closed-source) | (a) Pricing — author concluded "not externally available" without attempting account signup or `/settings` post-login walk. The brief lists pricing as a key question. (b) RAG roadmap — beta.specstory.com fetch failed with ECONNREFUSED, no retry attempted; agent inferred from snippets. | Critical (pricing) + Important (RAG roadmap) |
| web-02 Direct competitors | "Capture-AI-coding-chats-and-share-with-team" tools with deployment / supported tools / storage / search / RAG / team / pricing | 12 products covered (CursorShare, Cline Memory Bank, Pieces LTM, Continue Hub, AnythingLLM, Charlie Mnemonic, Omega Memory, Cursor native, claude-replay/CC Replay/vibe-replay, GroundRules, Packmind) + comparison table + scoping note deferring memory-layer to web-03 | (a) `https://www.g2.com/products/specstory/competitors/alternatives` flagged in own recommendations as "not enumerated" — agent acknowledged the gap but did not attempt the fetch. (b) CursorShare and Packmind both have "ECONNREFUSED" / "too little public detail" — author marks them as low-evidence but does not retry. (c) AnythingLLM is included with note "frequently confused" but its presence in this bucket vs web-05 (self-hosted chat platforms, where it correctly belongs per scope) creates partition overlap. | Important (G2 fetch) + Minor (overlap with web-05) |
| web-03 Memory layer | Mem0, Letta, Zep, Cognee, Graphiti, LangMem, SuperMemory, Mastra Memory + abstraction model / multi-user/team / self-host / pricing / can-it-ingest-captured-conversations | All 8 named products covered + Graphiti split out separately + Basic Memory MCP added + 6 adjacent products surveyed + comparison table + ingestion-fit ranking | Letta cloud pricing not extracted ("not on the page snippet pulled — third-party reports indicate"). SuperMemory production users vague ("indie/SMB-heavy"). Mastra license "not stated on snippet" — could be confirmed by 1 click on repo LICENSE file. | Minor (3 items, all low-stakes) |
| web-04 Observability | LangSmith, Langfuse, Helicone, Arize Phoenix, HoneyHive, Braintrust, PromptLayer, W&B Weave, Opik, Lunary, AgentOps, Traceloop + capture conversation-traces / multi-user / search / RAG export / self-host / coding-tool integration | All 12 named products covered + Laminar added (bonus) + comparison matrix + 4 take-away architectures (Proxy/OTEL/Hybrid/License-axis) | (a) HoneyHive has `null` first-class IDE integration but agent did not search Helicone-style proxy compatibility. (b) PromptLayer self-host — "limited public info" not retried. (c) Phoenix license inconsistency flagged: "core Apache-2.0, some adjacent packages Elastic-2.0" — agent correctly raised the issue but did not resolve it. | Minor |

**Coverage rating: STRONG overall** — every named candidate from the brief is treated. Misses are at the depth-of-evidence margin, not the candidate-coverage margin.

## 2. Evidence Quality

Sampling 5 claims per file and rating evidence strength (Strong = specific URL/path/line/quote; Adequate = named source + quoted detail but no anchor; Weak = vague "per docs" / inferential / "apparent").

| File | Sampled claim | Evidence quality | Notes |
|---|---|---|---|
| 01 | "`~/.claude/projects/<slugified-cwd>/<sessionId>.jsonl`" with full schema dump | Strong | Cited with `[CODE-VERIFIED at /config/.claude/projects/...46021a18...jsonl]` — actual file paths sampled |
| 01 | Cursor `state.vscdb` keys (`aiService.prompts`, `workbench.panel.aichat.view.aichat.chatdata`) | Adequate | Tagged `[DOC-ONLY]`; sources cited (cursor.fan, forum.cursor.com, SO) but no version anchor |
| 01 | Codex CLI `RolloutItem` variant names | Adequate | Tagged `[DOC-ONLY]`; "high confidence — schema item names match Rust types" but no commit/file:line citation in the Rust source |
| 01 | "Continue.dev `data` block was explicitly built for shipping events to a team HTTP endpoint" | Strong | Tagged `[DOC-ONLY]` but cites docs.continue.dev/development-data and config reference |
| 01 | "GitHub `gh-copilot` deprecated 2025-10-25" | Strong | Specific date + repo migration path named |
| web-01 | "Apache-2.0, 1.2k stars, Go 99.8%, default branch `dev`, 385 commits, 34 releases, latest v1.12.0 on 2026-03-19" | Strong | Quantified; specific repo URL |
| web-01 | Six Agent Skills enumerated by name with consumption pattern | Strong | Cites github.com/specstoryai/agent-skills + docs.specstory.com/agent-skills |
| web-01 | "REST 1000 req/hour/key, GraphQL 500 queries/hour/key, headers `X-RateLimit-*`" | Strong | Specific numerics + header names from docs.specstory.com/api-reference |
| web-01 | "`https://cloud.specstory.com/api/v1/graphql`" GraphQL endpoint | Strong | Verbatim URL |
| web-01 | "RAG roadmap = beta site reference to memory retrieval" | Weak | Author admits ECONNREFUSED on direct fetch; cites only "search snippet" — and labels (LOW reliability) honestly |
| web-02 | "Continue main repo ~31k+ GitHub stars (per third-party research summary)" | Weak | Hedged "per third-party research summary" — should pull a direct GitHub API number |
| web-02 | "Cursor v0.49 `/Generate Cursor Rules`" | Strong | Cites cursor.com/en/changelog/0-49 directly |
| web-02 | "claude-replay: HN Showcase post... well-received" | Adequate | Cites hnshowcase.com URL but no quote, no comment-count figure |
| web-02 | "CursorShare ECONNREFUSED at research time" | Weak (unavoidable) | Honest about evidence absence; explicitly downgrades reliability |
| web-02 | "G2 lists a SpecStory alternatives page" | Weak | Lists URL but acknowledges "actual G2 list could not be enumerated" — open gap |
| web-03 | Mem0 ~54.5k stars; Graphiti 25.6k; Letta 22.4k; SuperMemory 22.4k; Cognee 17k; LangMem 1.4k | Strong | Quantified per repo |
| web-03 | "Graphiti `add_episode_bulk` API accepts arbitrary text or structured JSON episodes with reference timestamp" | Strong | Specific API name; cites github.com/getzep/graphiti |
| web-03 | "Mem0 Hobby free 10k adds, 1k retrievals/mo; Starter $19/mo (50k/5k); Pro $249/mo" | Strong | Specific tier numbers; cites mem0.ai/pricing |
| web-03 | "Zep customer logos: AWS, Writer, Swiggy, Torq, AlphaSignal, Flockx, Axtria. SOC2 Type II + HIPAA claimed" | Strong | Named logos + compliance specific |
| web-03 | "Mastra Memory license not stated on snippet" | Weak | Author admits gap; one click on the repo would resolve |
| web-04 | "Helicone proxy: `api.anthropic.com` → `anthropic.helicone.ai`" | Strong | Specific URL pattern + env var mechanism named |
| web-04 | "Langfuse ~26.4k stars, weekly releases as of 2026" | Strong | Quantified |
| web-04 | Phoenix "community-documented playbook for migrating user conversations into traces" | Strong | URL cited: community.arize.com/x/phoenix-support/0ja85s8ctatc/migrating-user-conversations-to-traces-in-phoenix |
| web-04 | Braintrust "BTQL — first-class SQL query language over logs/datasets/experiments" | Strong | Cites braintrust.dev/docs/reference/btql |
| web-04 | "AgentOps ~smaller GA traction" | Weak | No quantification; "smaller" relative claim without comparator |

**Evidence quality rating per file:**

| File | Strong | Adequate | Weak | Verdict |
|---|---|---|---|---|
| 01 | 3/5 | 2/5 | 0/5 | Strong |
| web-01 | 4/5 | 0/5 | 1/5 | Strong |
| web-02 | 1/5 | 1/5 | 3/5 | **Adequate (borderline)** — multiple "could not fetch" / "third-party summary" instances |
| web-03 | 4/5 | 0/5 | 1/5 | Strong |
| web-04 | 4/5 | 0/5 | 1/5 | Strong |

Web-02 is the weakest on evidence rigor — it's a function of the bucket (newer/smaller products with limited public data), but the agent should retry the failed fetches before declaring final.

## 3. Documentation Staleness Compliance

For file 01 (codebase agent): expected verification tags `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, `[UNVERIFIED]`, `[DOC-ONLY]`, `[PARTIAL]` on every architectural claim. For web agents (web-01..04): expected source-reliability tags (HIGH/MEDIUM/LOW with parenthetical Official/Repo/Blog/Forum) per Phase-4 web research convention.

| File | Tags used? | Spot-check claims | Result |
|---|---|---|---|
| 01 | Yes — every tool block ends with explicit `[CODE-VERIFIED]` / `[DOC-ONLY]` / `[UNVERIFIED]` / `[PARTIAL]`. Plus dedicated "Stale Documentation Found" section with 5 entries (Aider docs, Cursor community guidance, gh-copilot deprecation, Roo Code docs sparseness, Continue.dev docs deferring fields to source) | Claude Code = `[CODE-VERIFIED]`; Cursor = `[DOC-ONLY]`; Aider = `[DOC-ONLY]`; Continue.dev = `[DOC-ONLY]`; Cline = `[DOC-ONLY]`; Roo = `[DOC-ONLY]`; Copilot CLI = `[DOC-ONLY]`; Gemini = `[DOC-ONLY]`; Codex = `[DOC-ONLY]` | PASS |
| web-01 | Yes — section-level reliability ratings ("HIGH/PARTIAL/LOW") + dedicated **Source Reliability Summary** table at end | Question 6 = HIGH (official OSS); Question 1 = PARTIAL→HIGH (FAQ confirmation); Question 7 = LOW (no public pricing); Question 9 = PARTIAL (beta unreachable) | PASS |
| web-02 | Yes — each product entry has explicit `Reliability:` line | CursorShare: "ECONNREFUSED — reputational signal weak"; Cline Memory Bank: "Official docs + maintained community MCP repo"; Pieces: "Official product pages"; etc. | PASS |
| web-03 | Yes — `Reliability:` line on each product (Official / Repo / Official+Repo) | Mem0 = Official+Repo; Zep = Official; Graphiti = Official+Repo; Mastra = Official | PASS |
| web-04 | Yes — `Reliability:` line on each product; all marked Official | LangSmith = Official; Langfuse = Official; Helicone = Official; Phoenix = Official; etc. | PASS |

Staleness compliance: **PASS for all 5 files.** File 01 properly uses verification tags AND has a dedicated stale-docs section. Web files use the source-reliability convention.

**Spot issue (web-04):** Helicone is described in prose as "open-source under MIT-style" (line 53) but the comparison table lists it as "Apache-2.0 (per repo)" (line 56). The OSS license at the end of Helicone's section says Apache-2.0. The "MIT-style" prose phrase is loose/ambiguous — should be tightened to just "Apache-2.0." Minor inconsistency, not a contradiction with external truth.

## 4. Completeness Markers

| File | Status | Summary | Findings | Gaps | Tables |
|---|---|---|---|---|---|
| 01 | **Complete** ✓ | Yes (final "Summary" para) ✓ | "Key Takeaways" section ✓ | "Gaps and Questions" section + "Stale Documentation Found" ✓ | Cross-tool comparison table ✓ |
| web-01 | **In Progress** ✗ | Yes ("Key External Findings") ✓ | "Key External Findings" + "Recommendations" ✓ | Implicit per-question (Q7 LOW, Q9 PARTIAL); no dedicated Gaps section ✗ | Capability Matrix + Capture Mechanics + Source Reliability ✓ |
| web-02 | **Complete** ✓ | "Key External Findings" ✓ | Yes ✓ | Recommendations call out gaps (CursorShare/Packmind validation, G2 fetch) — no dedicated Gaps section ✗ | Direct-Competitor Comparison Table ✓ |
| web-03 | **In Progress** ✗ | "Key External Findings" ✓ | Yes ✓ | No dedicated Gaps section ✗ (Letta cloud pricing / SuperMemory logos / Mastra license noted in-line) | Memory-Layer Comparison Table ✓ |
| web-04 | **In Progress** ✗ | "Key External Findings" ✓ | Yes ✓ | No dedicated Gaps section ✗ (HoneyHive proxy compat / PromptLayer self-host / Phoenix license noted in-line) | Observability-Platform Comparison Table ✓ |

**CRITICAL FINDING — Status markers:** Three of five files (web-01, web-03, web-04) carry `Status: In Progress` rather than `Status: Complete`. Web-01 has `**Status:** Complete.` at the very end (line 319), but the frontmatter line 4 still says `**Status:** In Progress`. Web-03 ends with `**Status:** Complete` at line 199 but frontmatter line 4 says `**Status:** In Progress`. Web-04 has no closing Status line at all — frontmatter says `In Progress`, no end-of-file completion stamp. The orchestrator's gate logic should treat a file as Complete only when both markers agree; right now all three are technically ambiguous.

**Mild finding — no dedicated Gaps section:** Files web-01, web-02, web-03, web-04 do not have a labeled "Gaps and Questions" / "Open Questions" / "Open Items" section. They embed gap signals in question-specific reliability ratings (web-01) or in the Recommendations section (web-02, web-03, web-04). For analyst-merge purposes, this means I have to read every paragraph to compile the gap list — which violates the "make gaps machine-readable" intent. File 01 demonstrates the right pattern.

## 5. Cross-Reference & Deferrals

Within the partition, multiple files touch overlapping product surfaces. Acknowledged or unacknowledged:

| Overlap | Files | Acknowledged? | Action |
|---|---|---|---|
| **Continue.dev** appears in 01 (storage format), web-01 (not directly named — but SpecStory captures via Continue.dev's output indirectly), and web-02 (Continue Hub). | 01, web-02 | Partially. File 01 documents Continue.dev's `dev_data` JSONL; web-02's Continue Hub entry is about *configs* not *chats* and explicitly says "complementary not competing." Different artifact, no contradiction. | None — handled cleanly |
| **AnythingLLM** appears in web-02 (with explicit "Relevance: LOW for direct competition") and is also a candidate for web-05 (self-hosted chat platforms — Partition 2). | web-02 | Web-02's scoping note says "Adjacent categories (general agent memory layers, observability, self-hosted chat UIs, enterprise org-memory, BYO RAG) are deferred to sister buckets web-03 through web-08" — but then includes AnythingLLM anyway, justifying with "frequently confused." | **Defer-to-merger:** confirm web-05 (Partition 2) is also covering AnythingLLM, then keep one canonical entry. Likely retain in web-05. |
| **Pieces for Developers** in web-02 — also a candidate for web-08 (adjacent tools — Partition 2). | web-02 | Brief explicitly lists Pieces in web-08 ("Adjacent / less-direct tools") but web-02 includes it as HIGH-relevance. The author justified inclusion based on "overlapping shape." | **Defer-to-merger:** confirm web-08 covers Pieces and dedupe. The web-02 treatment is more thorough; possibly canonicalize there. |
| **Cline Memory Bank** in web-02 — also a candidate for web-08. | web-02 | Brief lists Cline Memory Bank in web-08; web-02 included it. | **Defer-to-merger:** dedupe with web-08. |
| **Omega Memory** in web-02 — explicit author note "sister bucket web-03 (agent memory layer) is a better fit. Listed here because the brief named it." | web-02, web-03 | YES — author explicitly defers; web-03 should also cover. | **Verify:** web-03 does NOT list Omega Memory by name (cross-checked). web-02 implicitly cover-shadows web-03. Acceptable; could be relocated. |
| **MCP-memory servers / Mem0 MCP / Cline Memory Bank as MCP** — partially covered in web-03 (Mem0 MCP) and web-02 (Cline Memory Bank, Omega Memory MCP). | web-02, web-03 | Implicit. | **Defer-to-merger:** confirm web-08 (Partition 2) covers MCP-memory servers as the brief assigns. |
| **Helicone "MCP server"** in web-04 vs **Helicone Mem** noted as "no standalone memory product found" in web-03 | web-03, web-04 | Both mention; consistent. | None — clean |
| **Continue.dev observability** — no first-class plugin, web-04 says "supports custom base URLs (Helicone proxy-mode covers them) and SDK-level instrumentation." 01 says Continue.dev's `data` block ships events to HTTP destinations. | 01, web-04 | Partially. File 01 frames Continue.dev's HTTP fan-out as the team-aggregation mechanism; web-04 frames it as instrumentation gap. These are not in conflict — they describe different layers (Continue's own dev_data telemetry vs LLM API observability). Could be more explicit about the distinction. | Minor — synthesis should clarify the two layers |

**Bucket discipline summary:** Web-02 over-includes (Pieces, Cline Memory Bank, AnythingLLM, Omega Memory) but author transparently notes which are "adjacent" or "out of category." This is defensible (better over-coverage with deferral than misses) but creates dedup work for the merger.

## 6. Contradictions Found

| # | Claim A | Claim B | Files | Verdict |
|---|---|---|---|---|
| 1 | Helicone OSS license: "open-source under MIT-style" (web-04 prose, Helicone section). | Helicone OSS license: "Apache-2.0 (per repo)" (web-04 table + own license summary line). | web-04 (intra-file) | **Internal contradiction** — author appears to have used "MIT-style" loosely meaning "permissive." Fix: change prose to "Apache-2.0." |
| 2 | SpecStory team workspace: "Move useful conversations into a shared team space" (cloud landing) vs "Single-user workspaces — explicitly stated" (cloud-overview docs). | n/a | web-01 (intra-file) | **Surfaced** — author explicitly flagged this discrepancy ("cloud-overview doc qualifies workspace as single-user, suggesting team-space is either nascent or a Pro/beta feature"). Not a research contradiction; it's a real product-doc inconsistency the agent correctly surfaced. No action needed beyond ensuring synthesis carries the flag forward. |
| 3 | Cursor "cloud sync of chats is not built in" (file 01) vs Cursor "Cursor's cloud has chat features (e.g., shareable chats, account-bound prompts in newer versions), but the canonical historical store is the per-workspace SQLite" (file 01) vs web-02 "Cursor (native team chat features) — Storage: Local SQLite for foreground chats; remote storage for background-agent chats... Team aggregation: Not yet natively." | 01, web-02 | 01 vs web-02 | **No contradiction, but partial.** File 01 says "Storage path is local SQLite," web-02 says "Local SQLite + remote storage for background-agent chats." Web-02 is more specific (background-agent chats are remote). Ideal synthesis combines both. Note: file 01 was last verified as `[DOC-ONLY]` from forum sources that may pre-date the background-agent feature. |
| 4 | Mem0 stars: "~54.5k" (web-03) — claim is high for a memory layer; web-02 reports "Continue main repo ~31k+ stars (per third-party research summary)" with hedged confidence. | n/a | web-02, web-03 | **Not a contradiction** but Mem0's 54.5k figure is unverified against GitHub directly in web-03 — a single GitHub API call would confirm. Author marked "Activity signal" without source URL on the figure itself. |
| 5 | SpecStory cloud sync mechanism: web-01 says "push from local → cloud. Pull / merge from cloud → local is not advertised." File 01 (Claude Code section) says Anthropic's hosted `claude.ai/projects` "does not ingest these JSONL files." | 01, web-01 | None — these are about different products | None |

**Net contradictions: 1 internal (Helicone license phrasing in web-04). All other surfaced inconsistencies are product-side (i.e., the products themselves have conflicting marketing vs docs), correctly flagged by the agents.**

## 7. Compiled Gaps

| # | Gap | Severity | File | Remediation action |
|---|---|---|---|---|
| 1 | `Status: In Progress` in frontmatter despite end-of-file `Status: Complete` | Critical | web-01, web-03, web-04 | Update frontmatter line 4 to `**Status:** Complete` in all three files (mechanical fix; no research needed) |
| 2 | SpecStory pricing data declared "not externally available" without attempting account signup or post-login `/settings` walk | Critical | web-01 | Either (a) attempt SpecStory free signup and capture Settings → Plans page, OR (b) explicitly downgrade to "deferred — requires SpecStory contact" with rationale why signup was deemed out-of-scope. The current treatment leaves a hole the user explicitly asked about |
| 3 | SpecStory RAG roadmap: beta.specstory.com unreachable (ECONNREFUSED), no retry | Critical | web-01 | Retry beta.specstory.com directly OR confirm the Wayback Machine archive of the same URL. The "AI knowledge base coming soon" claim is a centerpiece of the synthesis recommendation — it must rest on direct evidence |
| 4 | G2 SpecStory alternatives page never fetched | Important | web-02 | Direct fetch `https://www.g2.com/products/specstory/competitors/alternatives`; integrate any new candidates into web-02 table |
| 5 | CursorShare: ECONNREFUSED at research time; Packmind: too little public detail | Important | web-02 | Retry both URLs; if still down, explicitly mark "deferred — site unreachable on 2026-05-01" with rationale |
| 6 | No dedicated Gaps section in 4 of 5 files (web-01, web-02, web-03, web-04) | Important | all 4 web | Add an explicit `## Gaps and Questions` (or `## Open Items`) section to each, listing the unresolved items already embedded in-line |
| 7 | Continue Hub stars hedged: "~31k+ (per third-party research summary)" | Minor | web-02 | One direct fetch of github.com/continuedev/continue confirms |
| 8 | Mem0 ~54.5k stars unverified against GitHub directly | Minor | web-03 | Cite specific GitHub repo URL in the activity-signal line |
| 9 | Letta cloud pricing "third-party reports indicate" | Minor | web-03 | One pass on letta.com/pricing or the Letta docs |
| 10 | SuperMemory production users vague ("indie/SMB-heavy") | Minor | web-03 | Either name a logo or label "no enterprise logos visible" |
| 11 | Mastra Memory license "not stated on snippet" | Minor | web-03 | One click on the Mastra repo LICENSE file |
| 12 | HoneyHive: no Helicone-style proxy-compat investigation | Minor | web-04 | One sentence on whether HoneyHive supports proxy-mode capture |
| 13 | PromptLayer self-host: "limited public info" | Minor | web-04 | One pass on docs.promptlayer.com or sales-tier page |
| 14 | Phoenix license inconsistency (Apache-2.0 core vs Elastic-2.0 adjacent packages) flagged but not resolved | Minor | web-04 | One pass on the specific packages (`arize-phoenix-otel`) PyPI/repo |
| 15 | Helicone described as "open-source under MIT-style" in prose vs Apache-2.0 in table — internal inconsistency | Minor | web-04 | Tighten prose to "Apache-2.0" |
| 16 | Cursor `state.vscdb` schema [UNVERIFIED] — Cursor is the largest install base, highest-stakes target | Minor | 01 | Author already flagged in Gaps section. If a Cursor install becomes available, dump the relevant keys; otherwise inherit risk |
| 17 | Cline / Roo / Copilot CLI per-file field schemas not enumerated (all `[DOC-ONLY]` or `[UNVERIFIED]`) | Minor | 01 | Author flagged. Acceptable for this depth tier; deeper reverse-engineer is out-of-scope unless synthesis lands on Cline/Copilot-CLI as primary ingest source |

**Counts: 3 Critical / 4 Important / 10 Minor = 17 total gaps.** All Critical items are mechanically remediable in <1 hour of agent work.

## 8. Depth Assessment

Deep tier expectation: substantive investigation beyond surface positioning, comparison-grade detail, schema-level insight, multi-source corroboration, fluent integration of architectural implications.

| File | Expected for Deep | Actual | Verdict |
|---|---|---|---|
| 01 | Per-tool storage format with field-level schema, capture detail, gap analysis, cross-tool synthesis | All 9 tools with schema + tool-call format + cross-tool table + 5 stale-doc findings + key-takeaways drawing engineering conclusions | **Above Deep** — could publish as a standalone reference. Claude Code is even `[CODE-VERIFIED]` against actual local JSONL files. |
| web-01 | Full SpecStory product surface incl. API, OSS license, pricing, RAG roadmap, team features today vs roadmap | Comprehensive on architecture/API/skills/license/team-features; pricing and RAG roadmap deferred (acknowledged); 22 sections + 3 tables + reliability summary | **Matches Deep** for the items investigated; **Below Deep** for pricing & RAG-roadmap gaps |
| web-02 | All direct competitors with deployment / tools / storage / search / RAG / team / pricing | 12 products + comparison table + scoping discipline + recommendations including defense-against-incumbent analysis | **Matches Deep** — strong synthesis (Cursor incumbency threat, "category is underbuilt") that goes beyond enumeration. Evidence quality drag is the weak link, not coverage |
| web-03 | All 8 named memory products + abstraction model + ingestion API + multi-tenant + IDE integration + captured-chat fit ranking | All 8 + Graphiti split out + Basic Memory MCP + 6 adjacent products + comparison table + ingestion-fit ranking + bake-off shortlist | **Above Deep** — recommendations are architecturally specific (which 3 to bake off, why Letta/Mastra/LangMem are not eligible) |
| web-04 | All 12 named platforms + trace granularity + multi-tenant + search + dataset/RAG export + self-host + coding-tool integ + license | All 12 + Laminar bonus + comparison matrix + Proxy-vs-OTEL architecture takeaway + license-axis ranking + hybrid-architecture recommendation | **Above Deep** — explicit architectural framing of two C-bucket sub-architectures (C-Proxy / C-OTEL) is a synthesis insight that downstream synth-04 will inherit directly |

Overall depth: **All five files match or exceed Deep tier on content density.** The FAIL verdict is driven by completeness markers and a small number of evidence-quality / fetch-retry gaps — not by depth.

## Final Verdict & Required Actions

**Verdict: FAIL — partition cannot pass to synthesis until 3 critical fixes land.**

### Must-fix before synthesis (Critical)
1. **Update Status frontmatter** in web-01, web-03, web-04 to `**Status:** Complete`. Mechanical edit, no research required. (Severity: Critical because the gate checks frontmatter.)
2. **Resolve SpecStory pricing gap (web-01).** Either attempt a free SpecStory signup and screenshot the in-product pricing/plans page, OR explicitly downgrade the deliverable with rationale ("requires direct SpecStory contact — design-partner signup is the only path to pricing visibility as of 2026-05-01"). Synthesis will need to recommend build/buy with pricing as an input — current state cannot defensibly do that.
3. **Resolve SpecStory RAG roadmap gap (web-01).** Retry beta.specstory.com OR pull a Wayback Machine archive of the same URL OR explicitly mark the "memory retrieval / AI knowledge base coming soon" claim as inferential. The "RAG is roadmap-shaped but not concretely scoped" conclusion is load-bearing for the synthesis recommendation and currently rests on a search-snippet of an unreachable host.

### Should-fix before synthesis (Important)
4. Direct fetch of G2 alternatives page (web-02) — likely surfaces 2-4 candidates not in current list.
5. Retry CursorShare and Packmind (web-02) or explicitly mark "deferred — site unreachable on 2026-05-01."
6. Add explicit `## Gaps and Questions` sections to web-01, web-02, web-03, web-04 — currently gap signals are embedded in-line and require re-reading.

### Nice-to-fix (Minor — synthesis can proceed with these as known-issues)
7. Items 7-17 in the Compiled Gaps table — small precision improvements, none of which alter the architectural conclusions.

### Partition merger handoff
- 4 cross-bucket overlaps need partition-2 merger handling: AnythingLLM (web-02 vs web-05), Pieces (web-02 vs web-08), Cline Memory Bank (web-02 vs web-08), MCP-memory servers (web-02/03 vs web-08). Web-02 over-included with explicit deferral; canonicalize in the destination buckets per brief.
- No cross-partition contradictions detected within partition 1's scope. Partition 2 should re-check for cross-partition contradictions on the four overlapping products.

### Sign-off statement
Once items 1-3 land, this partition is PASS-grade for Deep tier. The depth and synthesis quality of the 5 files is genuinely strong — the FAIL is about gate-tripping completeness signals, not substantive research deficits.
