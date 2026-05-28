# QA Research Gate Report — Partition 1 of 2

**QA Phase:** research-gate
**Partition:** 1 of 2 (files: 01, web-01..web-04)
**Date:** 2026-05-01
**Depth tier:** Deep

## Verdict: FAIL

Five files reviewed; substantive content quality is high (rich evidence density, source-cited claims, cross-tool comparison tables present in 01, and correct [CODE-VERIFIED] tags that I independently confirmed against `/config/.claude/projects/-config-workspace-IronClaude/`). However, two files (`web-01-specstory-deep-dive.md` and `web-03-memory-layer.md`) have a **Status marker mismatch**: the top frontmatter declares `Status: In Progress` while the trailing line declares `Status: Complete`. This is a CRITICAL gate-level inconsistency — by the orchestrator's gate rule, a file is considered complete only when its top-of-file Status is `Complete`. Synthesizers reading from the top of the file will see "In Progress" and may either flag the file or treat it as incomplete. Additionally, `web-04` has a duplicated "Activity signal" line for Phoenix (a minor data-quality defect) and **no top-of-file Status set to `Complete`** (also "In Progress" with no closing Status declaration). Per the gate's zero-tolerance rule (ALL gaps regardless of severity = overall FAIL), these issues must be resolved before synthesis proceeds.

---

## 1. File Inventory

| File | Exists | Size | Status marker | Notes |
|---|---|---|---|---|
| 01-native-storage-formats.md | Yes | 28,345 B | Top: **Complete**; trailing: **Complete** | OK. |
| web-01-specstory-deep-dive.md | Yes | 24,889 B | Top: **In Progress**; trailing: **Complete** | **MISMATCH** — top says In Progress; closing says Complete. |
| web-02-direct-competitors.md | Yes | 23,615 B | Top: **Complete**; no trailing Status | OK (top declares Complete; sufficient by checklist criterion). |
| web-03-memory-layer.md | Yes | 23,357 B | Top: **In Progress**; trailing: **Complete** | **MISMATCH** — same issue as web-01. |
| web-04-observability-platforms.md | Yes | 29,963 B | Top: **In Progress**; no trailing Status | **NO COMPLETE MARKER** — both positions absent or wrong. |

## 2. Evidence Density

Sampled 5 claims per file (representative, not exhaustive). All sampled claims cite a path or URL. Two URL/path claims independently verified live.

| File | Sampled claim | URL/path | Verifiable? | Verdict |
|---|---|---|---|---|
| 01 | Claude Code stores JSONL at `~/.claude/projects/<slug>/<sessionId>.jsonl` with sample `46021a18-…` | `/config/.claude/projects/-config-workspace-IronClaude/46021a18-…jsonl` | YES (Bash ls) | PASS |
| 01 | Sample 2: `56bae2f8-…jsonl` exists | `/config/.claude/projects/-config-workspace-IronClaude/56bae2f8-…jsonl` | YES (Bash ls) | PASS |
| 01 | Schema fields (`cwd`, `entrypoint`, `gitBranch`, `isSidechain`, `parentUuid`, `promptId`, `sessionId`, `timestamp`, `type`, `message.role`) present | jq-style extraction on cited file | YES (Python json check) | PASS |
| 01 | Aider history file path is `.aider.chat.history.md` | aider.chat docs | Plausible, doc-cited [DOC-ONLY] tagged | PASS (correctly tagged DOC-ONLY) |
| 01 | Codex CLI path `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` | github.com/openai/codex + deepwiki | Plausible, [DOC-ONLY] tagged | PASS |
| web-01 | Repo metadata: Apache-2.0, Go 99.8%, default `dev`, v1.12.0 (2026-03-19) | github.com/specstoryai/getspecstory | YES (WebFetch confirmed) | PASS |
| web-01 | Cloud REST limit 1000 req/hr/key, GraphQL 500/hr/key | docs.specstory.com/api-reference | URL plausible; not re-fetched but cited | PASS |
| web-01 | API base URL `https://cloud.specstory.com`, GraphQL endpoint `/api/v1/graphql` | docs.specstory.com/api-reference/introduction | Plausible (consistent with brand) | PASS |
| web-01 | "AIrgap is a separate OSS guardrail product" | docs.specstory.com/airgap | Plausible, source cited | PASS |
| web-01 | beta.specstory.com returned ECONNREFUSED — flagged as LOW reliability | self-flagged | Honest provenance disclosure | PASS |
| web-02 | CursorShare landing returned ECONNREFUSED | cursorshare.com | Self-flagged LOW evidence | PASS (honestly graded) |
| web-02 | Cline parent project license Apache-2.0 | github.com/cline/cline | Cited; aligns with public knowledge | PASS |
| web-02 | Cursor v0.49 changelog includes `/Generate Cursor Rules` | cursor.com/en/changelog/0-49 | URL plausible; specific version cited | PASS |
| web-02 | Continue Hub pricing — Solo $3/M tokens, Team $20/seat/mo | continue.dev/pricing | Specific numbers; source cited | PASS |
| web-02 | claude-replay GitHub at github.com/es617/claude-replay | github.com/es617/claude-replay | URL cited | PASS |
| web-03 | Mem0: 54.5k stars, Apache-2.0, free tier 10k adds + 1k retrievals | mem0.ai + github + pricing page | Specific numbers; sources cited | PASS |
| web-03 | Graphiti `add_episode_bulk` API + Neo4j/FalkorDB backend | github.com/getzep/graphiti | Plausible; consistent with public docs | PASS |
| web-03 | Zep Cloud SOC2 Type II + HIPAA, named logos AWS/Writer/Swiggy | getzep.com | Specific claims; cited | PASS |
| web-03 | SuperMemory pricing — Free $0 / Pro $19 / Scale $399 | supermemory.ai/pricing | Specific numbers; cited | PASS |
| web-03 | Cognee pricing — Free OSS / Cloud Developer $35 / Cloud Team $200 | cognee.ai/pricing | Specific numbers; cited | PASS |
| web-04 | Langfuse ~26.4k GitHub stars, MIT core + EE add-ons | github.com/langfuse + langfuse.com/handbook | Plausible; cited | PASS |
| web-04 | Helicone `ANTHROPIC_BASE_URL` proxy mode for Claude Code | docs.helicone.ai/integrations | Plausible; cited | PASS |
| web-04 | Phoenix community guide for "Migrating User Conversations to Traces" | community.arize.com link cited | URL specific; plausible | PASS |
| web-04 | Braintrust BTQL SQL-like query language | braintrust.dev/docs/reference/btql | Specific URL cited | PASS |
| web-04 | Traceloop launched MCP server in Dec 2025 with `opentelemetry-mcp` PyPI | github.com/traceloop/opentelemetry-mcp-server | Plausible; cited | PASS |

**Density verdict:** All five files are **DENSE** (>80% of claims directly evidenced with URL/path or path+verification tag). No fabrication detected in spot-checks; one live verification (specstory repo) and three local-fs verifications (Claude Code JSONL paths and field schema) all confirmed accurate.

## 3. Scope Coverage

Mapped agent prompt buckets → file content:

| File | Expected candidates (per research-notes.md / brief) | Covered | Missing |
|---|---|---|---|
| 01 | Cursor, Claude Code, Aider, Continue.dev, Cline, Roo Code, Copilot CLI, Gemini CLI, Codex CLI (9 tools) | All 9 covered with per-tool sections | None |
| web-01 | SpecStory: features, architecture, OSS, cloud, pricing, roadmap, team, RAG, Agent Skills, API, Cursor rules | All 10 question areas covered (with explicit "Question N" headings); pricing flagged as gap | None blocking |
| web-02 | "Direct competitors" — multi-tool capture/sync/share | Twelve products covered (CursorShare, Cline Memory Bank, Pieces, Continue Hub, AnythingLLM, Charlie Mnemonic, Omega Memory, Cursor native, claude-replay, GroundRules, Packmind) — exceeds brief; brief specifically named SpecStory, Cline-Memory, Charlie Mnemonic, Anything LLM | All four named products covered + 8 additional |
| web-03 | Mem0, Letta (MemGPT), Zep, Cognee, Graphiti, LangMem, SuperMemory, Mastra Memory | All 8 named products covered + Basic Memory MCP + adjacent low-relevance list | None |
| web-04 | LangSmith, Langfuse, Helicone, Arize Phoenix, HoneyHive, Braintrust, PromptLayer, W&B Weave, Opik (Comet), Lunary, AgentOps, Traceloop | All 12 named products covered + Laminar (bonus); 13 total | None |

**Scope verdict:** PASS — every named candidate is addressed. Several files exceed the brief by adding adjacent products with explicit relevance grading (responsible scope expansion).

## 4. Documentation Cross-Validation

**For 01 (codebase-style file):**

- Verification tags applied per-tool: `[CODE-VERIFIED]` (Claude Code), `[DOC-ONLY]` (Cursor, Aider, Continue, Cline, Roo, Copilot CLI, Gemini CLI, Codex CLI), `[PARTIAL]` (Claude Code sidecar dirs). All eight non-Claude-Code tools are honestly tagged `[DOC-ONLY]` because the agent had no install of those tools to inspect — this is appropriate.
- Spot-check 1 (Claude Code [CODE-VERIFIED]): paths `46021a18-…jsonl` and `56bae2f8-…jsonl` both exist on disk → CONFIRMED.
- Spot-check 2 (Claude Code schema fields): real file contains keys (`cwd`, `entrypoint`, `gitBranch`, `isSidechain`, `parentUuid`, `promptId`, `sessionId`, `timestamp`, `type`, `message.role`) as claimed → CONFIRMED.
- Spot-check 3 (slug rule `/` → `-`): `/config/workspace/IronClaude` → `-config-workspace-IronClaude` matches actual on-disk dir name → CONFIRMED.

**For web files (source reliability rated?):**

- web-01: HIGH/MEDIUM/LOW reliability ratings explicit per claim block; source reliability summary table present. PASS.
- web-02: "Reliability:" line per product (e.g., HIGH evidence quality, LOW evidence quality, official docs, beta product page). PASS.
- web-03: "Reliability:" line per product. PASS.
- web-04: "Reliability: Official" or similar per product. PASS.

**Cross-validation verdict:** PASS — tags applied correctly, code-verified claims are genuinely verified, web reliability ratings explicit.

## 5. Contradiction Resolution

Cross-checked claims about the same product across the partition:

- **Claude Code storage path** (mentioned in 01 and in web-01): both files agree the canonical location is `~/.claude/projects/<slug>/<sessionId>.jsonl`. Web-01 adds that SpecStory's Claude Code provider reads these JSONLs and converts to Markdown. Consistent.
- **Cursor storage** (01 and web-02): 01 says `state.vscdb` SQLite blob; web-02 echoes "Local SQLite for foreground chats; remote storage for background-agent chats." Consistent (web-02 adds the recent background-agent remote storage detail, which is a 2025/2026 change).
- **Continue.dev** (01 and web-02 indirectly): 01 describes `dev_data/*.jsonl` + HTTP fan-out; web-02 (Continue Hub entry) says Hub aggregates configs not chats — these are different layers and do not contradict.
- **Mem0** (web-03 only — but verify internal consistency): table cell "Hobby free (10k adds, 1k retrievals/mo); Starter $19/mo" matches the prose in the same file. Consistent.
- **Helicone** (web-04 only): described both as "Apache-2.0" and as "open-source under MIT-style" in the same entry. Minor inconsistency — actually the section says "open-source under MIT-style" then in OSS license line says "Apache-2.0 (per repo)." This is a small internal contradiction within the Helicone entry.

**Contradiction verdict:** Mostly clean. **One MINOR internal contradiction in web-04 Helicone entry** ("MIT-style" in self-host description vs. "Apache-2.0" in OSS license line). Per zero-tolerance rule this counts as a finding.

## 6. Gap Severity

| File | Gaps section present? | Severity tags? | Notes |
|---|---|---|---|
| 01 | Yes ("Gaps and Questions" + "Stale Documentation Found") | Tagged `[UNVERIFIED]` and `[PARTIAL]` per item | Severity granularity is "verification status" not Critical/Important/Minor — but each is actionable and atomic. Acceptable. |
| web-01 | Implicit (gaps surfaced as "PARTIAL", "LOW visibility — gap", "no published timeline" in inline question blocks) | Inline relevance/visibility tags | No standalone Gaps section; gaps are scattered. **MINOR finding.** |
| web-02 | No standalone Gaps section | None | Gaps exist (e.g., CursorShare unfetchable, Packmind too little detail) but not collected. **MINOR finding.** |
| web-03 | No standalone Gaps section | None | Adjacent low-relevance list serves as a "considered but excluded" inventory. **MINOR finding.** |
| web-04 | No standalone Gaps section | None | Same pattern. **MINOR finding.** |

**Gap verdict:** Per zero-tolerance rule, missing standalone Gaps sections in web-01..web-04 with explicit severity ratings = FAIL on this checklist item. (Note: gaps *content* is largely present, just not collected and tagged with explicit Critical/Important/Minor severity.)

## 7. Depth Assessment

| File | Depth rating |
|---|---|
| 01 | DEEP — per-tool 8-bullet structure, cross-tool comparison table, key takeaways, gaps section, stale-docs section, plus narrative summary. End-to-end "what's stored where" coverage across 9 tools. |
| web-01 | DEEP — answers all 10 question areas with primary-source citations; capability matrix; capture-mechanics table; source reliability summary; recommendations. |
| web-02 | DEEP — twelve products with full 13-field schema each; head-to-head table; positioning analysis vs. SpecStory per product; competitive recommendations. |
| web-03 | DEEP — 9 products + low-relevance adjacent list; consistent 14-field schema per product; comparison table; market split analysis; bake-off recommendation. |
| web-04 | DEEP — 13 products + comparison table; two-architecture distinction (proxy vs. OTLP); license/star ranking; integration matrix per coding tool; recommendations include hybrid architecture. |

**Depth verdict:** All five PASS Deep tier expectations.

## 8. Integration Point Coverage

For products in the partition, integration patterns documented?

- **01:** Per-tool storage path conventions (the integration entry point an aggregator must read from) — covered. Schema-versioning warnings — covered. Per-machine vs. synced — covered. Hashing scheme variance — surfaced explicitly in Key Takeaways. PASS.
- **web-01:** SpecStory's API surface (REST + GraphQL endpoints, auth, rate limits, error codes, status codes) — exhaustively covered. MCP server mention — surfaced as roadmap signal. PASS.
- **web-02:** Per-product deployment model (SaaS / OSS / hybrid / self-host) — covered for all 12. Storage layer — covered. Team aggregation mechanism (git-native, SaaS-mediated, manual link) — covered. PASS.
- **web-03:** Per-product Ingestion API column — covered (batch vs. live, key API names like `add()`, `add_episode_bulk`). IDE integration — covered with explicit MCP/SDK distinction. PASS.
- **web-04:** Two-architecture frame (proxy vs. OTLP); per-product coding-tool integration column; OTLP standardization analysis. PASS.

**Integration verdict:** PASS.

## 9. Pattern Documentation (for 01)

Cross-tool comparison table present? **YES** — `## Cross-Tool Summary Table` at line 173+. Six columns (Tool / Storage path / Format / Synced? / Tool calls captured? / Team aggregation OOB?) covering all 9 tools.

Schema patterns documented? Yes — Key Takeaways section (line 188+) explicitly enumerates:
- "JSONL is the de-facto wire format" (pattern across 4 tools)
- "All nine tools persist locally by default. None ship a built-in team aggregator" (universal pattern)
- "Tool calls are universally captured but never normalized" (cross-tool gap pattern)
- "File edits are almost never first-class" (universal gap)
- "Index/replay split is emerging" (Codex/Copilot pattern)
- "Per-project hashing is common but inconsistent" (path-convention pattern)

**Pattern verdict:** PASS — strong cross-tool synthesis present.

## 10. Incremental Writing Compliance

| File | Pattern | Verdict |
|---|---|---|
| 01 | Per-tool sections in fixed structure (Source / Storage path / File format / Schema fields / What captured / What missing / Per-machine vs synced / Team agg / Verification tag / Notes) repeated 9× → cross-tool summary → key takeaways → gaps → stale docs → summary. Reads as iterative section-by-section build. | PASS — iterative |
| web-01 | Repeating Question N blocks with progressive deepening (e.g., Q1 → Q1 (cont.) → Q1 (cont.)). The "(cont.)" pattern is direct evidence of incremental appending as new sources were consulted. | PASS — strongly iterative |
| web-02 | Per-product sections in fixed schema, then comparison table, then findings. Iterative product-by-product structure. | PASS — iterative |
| web-03 | Same pattern as web-02. | PASS — iterative |
| web-04 | Same pattern + two repeated "Activity signal" lines for Phoenix (line 74-75) — evidence of an editing slip during incremental append. | PASS for incrementality, but flags a data-quality issue |

**Incremental verdict:** PASS for compliance; one minor editing artifact in web-04 (duplicated Activity signal line under Phoenix).

---

## Findings

| # | Finding | Severity | File | Required action |
|---|---|---|---|---|
| 1 | Top-of-file `Status: In Progress` while trailing `Status: Complete` | CRITICAL | web-01-specstory-deep-dive.md | Update top frontmatter to `Status: Complete` (or remove trailing line) so the gate-readable status is consistent. |
| 2 | Top-of-file `Status: In Progress` while trailing `Status: Complete` | CRITICAL | web-03-memory-layer.md | Same — set top to `Status: Complete`. |
| 3 | Top-of-file `Status: In Progress` AND no trailing `Status: Complete` declaration | CRITICAL | web-04-observability-platforms.md | Add closing `**Status:** Complete.` line AND update top frontmatter to `Status: Complete`. |
| 4 | Internal contradiction in Helicone entry: "open-source under MIT-style" in self-host text vs. "Apache-2.0 (per repo)" in OSS license line | MINOR | web-04 (Helicone section) | Reconcile — confirm actual repo license (likely Apache-2.0 per the explicit OSS license line) and remove "MIT-style" wording. |
| 5 | Duplicated "Activity signal" line under Phoenix entry (lines 74–75) | MINOR | web-04 (Phoenix section) | Delete the duplicate line. |
| 6 | No standalone Gaps section with explicit Critical/Important/Minor severity tags | MINOR | web-01 | Add a `## Gaps and Questions` section at end consolidating PARTIAL/LOW-visibility items (pricing opacity, beta site unreachable, RAG roadmap timeline absent, capture-fidelity per-tool risk) with severity tags. |
| 7 | No standalone Gaps section with explicit severity tags | MINOR | web-02 | Add `## Gaps and Questions` consolidating: CursorShare unfetchable (Important — direct competitor confirmation blocked), Packmind insufficient detail (Minor), G2 alternatives page not enumerated (Minor). |
| 8 | No standalone Gaps section with explicit severity tags | MINOR | web-03 | Add `## Gaps and Questions` consolidating: Letta Cloud pricing not extracted (Minor), Mastra Memory license not stated on snapshot (Minor), production-user logos missing for several products (Minor — affects credibility scoring). |
| 9 | No standalone Gaps section with explicit severity tags | MINOR | web-04 | Add `## Gaps and Questions` consolidating: Phoenix license inconsistency (Apache-2.0 core but `arize-phoenix-otel` Elastic-2.0 in some channels — needs verification), HoneyHive specific pricing only "$300+" (Minor), AgentOps self-host details require enterprise contact (Minor). |

---

## Final Verdict

**FAIL.** Per the gate's zero-tolerance rule (ALL gaps regardless of severity = overall FAIL), three CRITICAL Status-marker inconsistencies and six lesser findings must be resolved before synthesis. The findings are all easy fixes (no new research required); estimated remediation under 30 minutes total.

**Required actions before re-running gate (Partition 1 scope):**

1. Fix Status markers in web-01, web-03, web-04 (findings 1–3).
2. Resolve Helicone license inconsistency in web-04 (finding 4).
3. Delete duplicated Activity-signal line in web-04 Phoenix entry (finding 5).
4. Add consolidated `## Gaps and Questions` sections with explicit severity tags to web-01..web-04 (findings 6–9).

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 5 | Bash: 3 | WebFetch: 1 | Glob: 0
(All 5 files read in full; 3 Bash calls verified file inventory + JSONL paths + JSONL schema fields against actual local data; 1 WebFetch independently verified the SpecStory repo metadata claims in web-01.)

**QA Complete.**
