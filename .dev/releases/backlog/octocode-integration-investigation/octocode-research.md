# Octocode Research Report — Strengths & Weaknesses

**Date:** 2026-05-30
**Project:** IronClaude / SuperClaude Framework
**Purpose:** Stage 1 of the octocode-integration investigation. Feeds Stage 2 (`/sc:analyze` for fit) and Stage 3 (parallel brainstorm).
**Source files:**

- `research/web-01-octocode-tools-architecture.md` — canonical tool inventory + architecture
- `research/web-02-octocode-strengths.md` — validated use cases + token efficiency claims
- `research/web-03-octocode-weaknesses.md` — limitations, risks, supply-chain concerns
- `research/02-integration-points.md` — IronClaude integration surface (top 5 targets)

---

## Table of Contents

1. Identity & Positioning
2. Tool Surface (the 14 tools at a glance)
3. Strengths (what genuinely works)
4. Weaknesses & Risks (what to be careful of)
5. Overlap vs. IronClaude's Existing MCP Stack
6. Adoption Recommendations (scoped)
7. Open Questions

---

## 1. Identity & Positioning

**Octocode** is a Model Context Protocol (MCP) server by Guy Bary (@bgauryy) — a Tel Aviv-based software architect — that exposes **14 tools across 3 categories**: code-host search (GitHub/GitLab/Bitbucket), local filesystem (ripgrep + `find` + `ls`), and LSP semantic navigation (`gotoDefinition`, `findReferences`, `callHierarchy`).

- **License:** MIT. npm package `octocode-mcp` (currently v14.2.0, ~2,352 weekly downloads).
- **Manifesto:** "Code is Truth, but Context is the Map." — **Research Driven Development (RDD)** philosophy. Every tool call requires a `researchGoal` + `reasoning` field, pushing the LLM toward intentional research rather than ad-hoc tool calls.
- **Read-only by design** — never writes to GitHub.
- **Ships with a skills marketplace** — 19 bundled skills (`octocode-researcher`, `octocode-research`, `octocode-brainstorming`, `octocode-plan`, `octocode-engineer`, `octocode-pull-request-reviewer`, etc.) under `skills/` in the repo.

**Author traction signals:**

- GitHub: ~852 stars, 73 forks, 5 watchers, 0 open issues (suspicious low engagement)
- npm: 194 versions published in <12 months (rapid iteration)
- Contributors: ~97% of commits by bgauryy alone (combined with Wix work-account)
- HN launch (Nov 2025): 8 points, 7 comments — modest, not viral
- Production testimonial: one HN commenter integrated it into an internal AI assistant for PMs

---

## 2. Tool Surface (the 14 tools at a glance)

| # | Tool | Category | One-line purpose |
|---|---|---|---|
| 1 | `githubSearchCode` | Code-host: Search | Keyword search for code across GitHub repos |
| 2 | `githubSearchRepositories` | Code-host: Search | Discover repos by keywords/topics/stars |
| 3 | `githubSearchPullRequests` | Code-host: Search | Search PRs/MRs with metadata/diffs/comments |
| 4 | `githubGetFileContent` | Code-host: Content | Read file (or fetch directory to disk for LSP analysis) |
| 5 | `githubViewRepoStructure` | Code-host: Content | Display repo directory tree |
| 6 | `githubCloneRepo` | Code-host: Content | Shallow/sparse clone to `~/.octocode/repos/` (GitHub-only) |
| 7 | `packageSearch` | Code-host: Package | npm/PyPI lookup → repo URL, version, deprecation |
| 8 | `localSearchCode` | Local: Search | Ripgrep-backed pattern search (provides `lineHint` for LSP) |
| 9 | `localViewStructure` | Local: Discovery | `ls`-style directory listing with metadata |
| 10 | `localFindFiles` | Local: Discovery | `find`-style file/dir search with rich filters |
| 11 | `localGetFileContent` | Local: Content | Read local file with targeted extraction |
| 12 | `lspGotoDefinition` | LSP: Semantic | Jump to symbol definition |
| 13 | `lspFindReferences` | LSP: Semantic | All usages of a symbol |
| 14 | `lspCallHierarchy` | LSP: Semantic | Incoming/outgoing call graph (depth ≤ 3) |

**The "Funnel Method" canonical flow:** DISCOVER → SEARCH → LOCATE/ANALYZE → READ. Get `lineHint` from `localSearchCode` first, then pass to LSP tools. Never start with `localGetFileContent`.

**LSP coverage:** TypeScript/JavaScript bundled out-of-box. All others (Python, Go, Rust, Java, C/C++, Ruby, etc.) require user-installed language servers + `OCTOCODE_*_SERVER_PATH` env vars.

---

## 3. Strengths (what genuinely works)

### 3.1 Cross-repo GitHub search at LLM-ergonomic granularity

This is octocode's biggest single differentiator vs. everything else in the IronClaude stack. The benchmark (vendor-published BENCHMARK.md, 5 task archetypes R1–R5 extracted from 4.5k Claude Code sessions):

- **MCP variant: 77k tokens vs 90k baseline (−14%)**
- **40/40 accuracy vs 39/40 baseline**
- **Wall-clock parity (42s vs 39s)**

Validated use cases:

| Archetype | Example query | Tool chain |
|---|---|---|
| R1 — Package investigation | "What does `pydantic-ai` actually do?" | `packageSearch` → `view-structure` → `get-file` |
| R2 — Library usage examples | "Show me real callsites of `useEffect` cleanup" | `search-code` fan-out → `get-file` |
| R3 — Deep repo orientation | "I'm new to `transformers`, where does X live?" | `view-structure` → targeted `get-file` |
| R4 — PR archaeology | "Why was this change made?" | `searchPullRequests` → `get-file` |
| R5 — Comparative research | "How do React vs Vue solve hydration?" | Bulk `view-structure` + `get-file` across N repos |

### 3.2 Multi-provider unification (GitHub + GitLab + Bitbucket)

Same schema (`owner` / `repo` / `branch` / `prNumber`) across providers, with auto-detection. The Tool Selection Policy already in `deep-research.md:30-36` could gain a 4th "code patterns" axis instead of needing separate per-provider integrations.

### 3.3 Token-optimized response envelopes

- `verbosity` parameter (`compact` / `verbose` / `ultra`) on local + LSP tools
- Response field stripping (drops `cached`, `expiresAt`, `html_url`, etc.)
- Auto-truncation of PR bodies based on batch size (2000ch at limit=2-3, 800ch at limit=4+)
- `charOffset` / `charLength` universal pagination
- 24h disk cache at `~/.octocode/repos/` for cloned repos

### 3.4 "Research Driven Development" enforcement

The mandatory `researchGoal` + `reasoning` fields on every tool call are the most interesting design choice. They force the agent to articulate intent, which:

- Improves the agent's own planning quality
- Provides an audit trail in logs
- Pairs naturally with IronClaude's MDTM task-file pattern (each checklist item already has a "why" — octocode would extend that into tool-call provenance)

### 3.5 Skills marketplace as a workflow scaffold

19 bundled skills push octocode beyond "tools" toward "workflows":

- `octocode-research` — stateful multi-phase investigation (analogous to IronClaude's `tech-research` skill)
- `octocode-brainstorming` — evidence-first idea validation (analogous to `sc-brainstorm-protocol`)
- `octocode-plan` — turns research into implementation steps (analogous to `sc-roadmap-protocol`)
- `octocode-engineer` — architecture-aware engineering loop
- `octocode-pull-request-reviewer` — analogous to `sc-auggie-review-protocol`

The overlap with IronClaude's skill set is striking — octocode and SuperClaude have parallel workflow ontologies. This is either an opportunity (cross-pollination) or a duplication risk (two competing skill systems).

### 3.6 Cursor head-to-head benchmark (author-published)

On a Linux kernel (100k+ files) test:

- Octocode wins **27-5 on granular metrics** (byte offsets, pagination, research-context preservation, file metadata, smart `matchString` extraction)
- Cursor wins on subtree analysis and extension breakdowns

Bias caveat: bgauryy authored both the benchmark and the tool — treat as suggestive, not definitive.

---

## 4. Weaknesses & Risks

### 4.1 Supply-chain & maintainer risk (the single biggest concern)

| Risk | Detail |
|---|---|
| **Bus factor = 1** | ~97% of commits by bgauryy alone (combined with his Wix work-account `guybary-wix`). No co-maintainers, no foundation, no published succession plan. |
| **194 npm versions in <12 months** | High churn rate. Adopting v14.x means a high probability of v15+ breaking changes within the integration's first quarter. |
| **`@latest` install pattern in all docs** | Every official snippet (Cursor, Claude Code, VS Code, etc.) uses `npx octocode-mcp@latest`. A compromise of bgauryy's npm credentials = silent backdoor into every install. This is the *exact* pattern that hit `event-stream`, `ua-parser-js`, `colors`/`faker`, and the Sept 2025 MCP ecosystem attack. |
| **No containerized distribution** | Standalone binary install via `curl | sh` is itself a supply-chain anti-pattern. |
| **MCP STDIO command-injection family (OX Security 2026)** | Octocode-mcp inherits a CVE-class flaw in the STDIO transport. 200k+ servers vulnerable ecosystem-wide. Anthropic declined to modify the protocol. |
| **Maintainer declined a free Harness Doctor audit** | Marked "Not planned (skipped)" in the repo. Negative governance signal. |

### 4.2 Self-disclosed security audit findings (Issue #321, Feb 23 2026)

| Finding | Severity | Detail |
|---|---|---|
| #2 | MEDIUM (by-design) | Telemetry sends **repo names + research goals** to external server. Opt-out via `LOG=false`. |
| #3 | MEDIUM | CLI writes MCP config files with **world-readable permissions**. |
| #5 | LOW | Skills marketplace downloads **without SHA pinning / integrity verification**. |
| #6 | LOW | Credential env vars passed to child processes without filtering. |

The telemetry finding is the most concerning for a security-conscious environment — research goals can be domain-sensitive (e.g., "find all auth implementations in our private monorepo").

### 4.3 GitHub API rate limits (operational)

- Authed: 5,000 req/hr (per user)
- **Search API: 30 req/min** (the binding constraint for octocode's bulk-parallel pattern)
- Hitting the limit returns HTTP 403; octocode's backoff behavior is undocumented

A "deep research" workflow that fans out 5–10 parallel `githubSearchCode` calls can exhaust the Search budget fast.

### 4.4 Context tax

- 14 tools at ~600–1200 tokens per schema = **8,000–17,000 tokens of context burned before the first user turn**
- Comparable to GitHub's official MCP (documented at 17,600 tokens)
- IronClaude already loads auggie + serena + tavily + context7 + sequential + magic + playwright — adding octocode pushes total MCP context tax higher

### 4.5 LSP language gaps

- Bundled: TypeScript + JavaScript only
- All others require host-installed language servers (`pyright`, `gopls`, `rust-analyzer`, `jdtls`, `clangd`, etc.)
- No warning surfaced to the LLM when LSP falls back to lexical search — agent may state false-confident claims about call hierarchies that are actually text matches

### 4.6 Limited community validation

- 0 open issues + only 12 closed issues = either very small user base, or issues being closed without surfacing
- No HN/Reddit/independent benchmark surfaced in adversarial search
- The most prominent comparison article (Wix Engineering) was written by bgauryy himself, using octocode to research octocode — marketing as evaluation

---

## 5. Overlap vs. IronClaude's Existing MCP Stack

| Octocode tool category | IronClaude equivalent | Overlap verdict |
|---|---|---|
| **Local file read** (`localGetFileContent`) | Native `Read` tool | **100% redundant** |
| **Local file search** (`localSearchCode`) | Native `Grep`, ripgrep via Bash | **Redundant** but adds metadata convenience |
| **Local symbol nav** (`lspGotoDefinition`, `lspFindReferences`, `lspCallHierarchy`) | `serena` MCP (`find_symbol`, `find_referencing_symbols`) | **Strong overlap.** Serena is already symbol-aware and project-memory-aware. Octocode's LSP only adds value if serena fails on a language serena doesn't support. |
| **Local codebase semantic search** | `auggie` MCP (`codebase-retrieval`) — tagged HIGHEST PRIORITY in IronClaude CLAUDE.md, "free, costs little to no tokens" | **Strong overlap for local.** auggie is faster and free. Octocode wins ONLY when scope extends to external GitHub repos. |
| **Library/framework docs** | `context7` MCP | **No overlap.** Octocode searches source code; context7 returns canonical maintainer-published docs. Context7 is more accurate for "what does this API do." |
| **Web search** | `tavily` MCP + WebSearch | **No overlap.** Octocode doesn't do general web search. |
| **GitHub repo/PR/issue interaction** | `gh` CLI shelled out via Bash | **Functional overlap.** `gh` is already authed, OS-package-pinned, and adds zero MCP context tax. |
| **Cross-repo GitHub semantic search** | **Nothing equivalent in the IronClaude stack** | **Genuine value-add.** This is octocode's killer feature. |
| **`packageSearch` (npm/PyPI → repo URL)** | **Nothing equivalent** | **Genuine value-add.** Particularly useful when investigating third-party deps. |
| **Cross-repo PR archaeology** | **Nothing equivalent** | **Genuine value-add.** Useful for "how do other projects solve X" research. |

**Net position:** Octocode adds **~3 genuinely unique capabilities** (cross-repo GitHub search, package ecosystem lookup, cross-repo PR archaeology) at the cost of significant overlap with auggie + serena + Read for local operations. The right adoption model is to **disable octocode's local tools and use only its cross-repo capabilities** (via `TOOLS_TO_RUN` whitelist or `DISABLE_TOOLS`).

---

## 6. Adoption Recommendations (Scoped)

### Strong YES — adopt with restrictions

1. **Adopt octocode's cross-repo tools only** — whitelist `githubSearchCode`, `githubSearchRepositories`, `githubSearchPullRequests`, `githubGetFileContent`, `githubViewRepoStructure`, `packageSearch`. Disable all `local*` and `lsp*` tools (they overlap with serena + auggie + Read). This drops context tax to ~3,000–7,000 tokens.
2. **Pin a specific version** — never use `@latest`. Use `octocode-mcp@14.2.0` (or whatever is current at adoption time) and document upgrade gates.
3. **Set `LOG=false`** — opt out of telemetry that leaks research goals + repo names.
4. **Restrict scope** — use `ALLOWED_PATHS` and `ENABLE_CLONE=false` to limit blast radius if compromised.

### Strong NO — do not adopt

- **Do not adopt the skills marketplace.** IronClaude already has parallel skill systems (tech-research, sc-brainstorm-protocol, sc-roadmap-protocol, etc.) that are deeper, more enforced, and already integrated with the MDTM task file pattern. Importing octocode's skills creates two competing ontologies.
- **Do not adopt the `npx add-skill` mechanism.** Web-04 flagged uncertainty about whether this is octocode's own tool or a third-party (`ahmadawais/add-skill`) — either way, IronClaude's `make sync-dev` pipeline is the canonical install path.

### Highest-value integration targets (from code-02)

1. **MCP server registration** (`install_mcp.py:29`) — 5-line config entry; framework-wide availability.
2. **deep-research agent Tool Selection Policy** (`agents/deep-research.md:30-36`) — add octocode as a 4th "GitHub code patterns" axis alongside Tavily/Context7/Sequential.
3. **tech-research skill Phase 4 Web Research** (`skills/tech-research/SKILL.md:415-419`) — Phase 4 explicitly targets "GitHub issues and discussions" — octocode operationalizes this.
4. **brainstorm Wave 2A enrichment matrix** (`skills/sc-brainstorm-protocol/SKILL.md:179-187`) — add octocode row for `domain in {code, architecture}`.
5. **PostToolUse hook for auggie** (`hooks/hooks.json:59-68`) — when auggie searches the local repo, fire octocode in parallel for "how do other repos solve this."

---

## 7. Open Questions

| # | Question | Why it matters | Suggested resolution |
|---|---|---|---|
| 1 | Is `npx add-skill` an octocode tool or a third-party (`ahmadawais/add-skill`)? | Determines whether octocode's skill install path is part of its trust boundary. | Read `octocode-cli` source under `packages/octocode-cli/`. |
| 2 | What is octocode's actual response-size distribution on real workloads? | "LLM-optimized" is a self-claim; no third-party benchmark exists. | Instrument context usage in a 1-week pilot. |
| 3 | How does octocode behave when GitHub Search API returns 403 (rate limit)? | Determines fallback strategy. | Test by exhausting search budget; observe behavior. |
| 4 | Are there empirical workloads where octocode + auggie outperforms auggie alone (for non-cross-repo tasks)? | Decides whether to enable local tools or only cross-repo. | A/B test on 5 representative IronClaude tasks. |
| 5 | What is the impact of `LOG=false` on octocode's caching / metrics? | Telemetry opt-out may degrade UX. | Read source; test pilot. |
| 6 | Does octocode handle GitHub Enterprise correctly with the IronClaude team's typical config? | Important for any enterprise adoption. | Test against a GHE instance if available. |

---

**Source agents:**

- `research/web-01-octocode-tools-architecture.md` (Tavily — comprehensive)
- `research/web-02-octocode-strengths.md` (Tavily — testimonials + benchmarks)
- `research/web-03-octocode-weaknesses.md` (Tavily + WebFetch — supply chain + maturity)
- `research/02-integration-points.md` (Explore — IronClaude integration surface)
- `research/web-04-octocode-skills-marketplace.md` — **FAILED** (agent stalled); partial finding: `npx add-skill` may be third-party not octocode-native

**Status:** Complete
