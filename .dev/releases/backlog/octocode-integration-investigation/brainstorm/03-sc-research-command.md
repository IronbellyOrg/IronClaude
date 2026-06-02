# Brainstorm — Target #3: /sc:research Command

**Date:** 2026-05-30
**Agent:** Brainstorm 3 of 5 (parallel)
**Target:** `src/superclaude/commands/research.md`
**Question framing:** "What is the most beneficial way to integrate octocode into the user-facing `/sc:research` command?"

---

## Target Context

### What the command is today

`/sc:research` is the **front door** for ad-hoc deep web research in SuperClaude. It is a user-typed slash command — high signal because the user is *explicitly* asking for research right now, and high visibility because failures land directly in front of the user with no intermediate skill or pipeline to mask them.

**Current frontmatter (literal):**

```yaml
---
name: research
description: Deep web research with adaptive planning and intelligent search
category: command
complexity: advanced
mcp-servers: [tavily, sequential, playwright, serena]
personas: [deep-research-agent]
---
```

**Current invocation pattern:**

```
/sc:research "[query]" [--depth quick|standard|deep|exhaustive] [--strategy planning|intent|unified]
```

**Current depth tiers:**

- **Quick** — 1 hop, summary output
- **Standard** — 2-3 hops, structured report
- **Deep** — 3-4 hops, detailed analysis
- **Exhaustive** — 5 hops, complete investigation

**Current MCP stack:**

- **Tavily** — primary search + extraction engine
- **Sequential** — synthesis / multi-step reasoning
- **Playwright** — JavaScript-heavy page extraction
- **Serena** — research session persistence (write checkpoints, resume)

**Who invokes it and why:**

| Caller | Typical query shape | What they expect |
|---|---|---|
| Developer at a terminal | "latest developments in quantum computing 2026" | Web-first concept research, structured report |
| Architect prepping a TDD | "compare GraphQL federation strategies" | Multi-source synthesis with citations |
| Operator debugging | "is `httpx` async client thread-safe?" | Authoritative library answer |
| Researcher | "how do production projects implement rate limiting in FastAPI?" | **<-- This is where octocode wins** |

The fourth row is the key insight: the **current command has no good answer for "show me how real projects actually do X."** Tavily returns blog posts and Stack Overflow threads about X; it does not return *the actual code that does X in production*. That is octocode's killer feature.

**Output contract (load-bearing):**

- Writes to `claudedocs/research_[topic]_[timestamp].md`
- Includes executive summary, confidence levels, sources with citations
- **STOP AFTER RESEARCH REPORT** — explicit no-implementation boundary
- Downstream: user manually invokes `/sc:design` or `/sc:implement`

**Powered by:** `deep-research-agent` (frontmatter `personas:` field) — meaning any change to the agent (target #1 in this brainstorm series) propagates here automatically *unless* `/sc:research` short-circuits the agent for octocode-specific work.

---

## The Integration Question

**How should octocode appear in the `/sc:research` user surface?** Four dimensions of design choice:

1. **Discoverability** — Does the user have to know octocode exists, or does the command auto-route?
2. **Composition** — Does octocode *replace* Tavily for certain queries, *augment* it, or *run in parallel*?
3. **Reporting** — Are octocode findings a separate report section, interleaved citations, or invisible (merged)?
4. **Failure surface** — When octocode rate-limits or returns nothing, does the command fail, degrade silently, or warn?

The constraint stack (from `octocode-research.md` §4 + §6):

- Octocode has supply-chain + maintainer risk → integration must be opt-in or trivially disable-able.
- Octocode's GitHub Search API limit is **30 req/min** (binding) → bulk parallel fan-out must be rate-aware.
- Octocode adds **~3-7k tokens** of context tax (after `TOOLS_TO_RUN` whitelist) → only load when the query warrants it.
- Octocode does **no general web search** → must coexist with Tavily, never replace it for concept research.

The user-facing layer cares most about: **predictability** (same flag → same behavior), **transparency** (which backend produced which citation), and **graceful failure** (rate limit doesn't kill the report).

---

## Wave 1: Divergent Ideation

### Candidate A — `--mode code` flag (explicit opt-in mode)

Introduce a new orthogonal flag:

```
/sc:research "<query>" --mode code [--depth ...]
```

- `--mode code` → octocode-only routing (skip Tavily, use `githubSearchCode`/`packageSearch`/etc.).
- Default (`--mode web` implicit) → unchanged Tavily-first flow.
- Hypothetical `--mode hybrid` (Wave 2 may merge) → both engines in parallel.

The frontmatter gains `octocode` in `mcp-servers`. The command file gains a "Mode Selection" subsection. The deep-research-agent's tool list is extended (relies on target #1 being landed).

**Spirit:** Make the user choose. Don't make octocode invisible — it has different rate limits, different cost profile, and different output shape from Tavily, so the user should know which engine they invoked.

### Candidate B — `--source octocode` flag (MCP-source override)

Mirror the existing implicit "Tavily is the source" with explicit source selection:

```
/sc:research "<query>" --source octocode
/sc:research "<query>" --source tavily       # explicit; current default behavior
/sc:research "<query>" --source all          # fan out to both
```

Differs from Candidate A by being source-named rather than mode-named — communicates "you are choosing a backend" rather than "you are choosing a topic flavor." Easier to extend later (`--source context7`, `--source auggie`).

**Spirit:** Treat backends as first-class. Aligns with how the deep-research-agent's Tool Selection Policy already distinguishes Tavily/Context7/Sequential as axes.

### Candidate C — Auto-engage on query keywords (no flag)

Heuristic router inside the command:

```
if query matches /implement|implementation|how does .* work in code|production example|callsite/i
    → activate octocode + Tavily in parallel
elif query matches /package|library|npm|pypi|cargo/i
    → activate packageSearch as a first step, then Tavily
else
    → current Tavily-only behavior
```

No new flags. The user gets octocode "for free" when their query smells like a code-pattern question.

**Spirit:** Maximum convenience, zero learning curve. Risk: opaque behavior — user can't predict which backend ran without reading the report's backend column.

### Candidate D — New `--depth deep+code` tier

Extend the depth ladder rather than adding an orthogonal axis:

```
--depth quick           # 1 hop, Tavily-only
--depth standard        # 2-3 hops, Tavily + Context7
--depth deep            # 3-4 hops, Tavily + Context7 + Sequential (current "deep")
--depth deep+code       # NEW: deep + octocode fan-out for code patterns
--depth exhaustive      # 5 hops, all backends including octocode
```

**Spirit:** Stay within the existing knob (`--depth`). Don't multiply the flag surface. Octocode = a "thicker" research run.

### Candidate E — New sub-command `/sc:research code <query>`

Split the verb-noun surface:

```
/sc:research "<query>"               # default — web research (Tavily-first, unchanged)
/sc:research code "<query>"          # NEW — code research (octocode-first)
/sc:research package <name>          # NEW — package investigation (packageSearch → repo)
/sc:research pr <repo> <query>       # NEW — PR archaeology (githubSearchPullRequests)
```

Sub-command pattern is familiar (`git remote add`, `gh pr create`, `npm install`). Each sub-command can have its own frontmatter + tool selection.

**Spirit:** Verb-noun disambiguation. Forces the user to declare *what kind* of research up-front, which makes routing trivial and the output contract crisper. Trade-off: scope creep — three new sub-commands is a substantial expansion of the command's surface area.

### Candidate F — Hybrid by default, no flag, octocode auto-engages for "code research"

A more aggressive form of Candidate C: octocode is *always* loaded (frontmatter), and the deep-research-agent's planner phase decides whether to dispatch octocode tools based on the query. The user never sees a flag; the planner reasons about source selection.

**Spirit:** "The agent is smart enough to choose." Maximum encapsulation. Risk: planner mistakes are silent and the user can't override.

### Candidate G — Separate octocode results section in report (presentation-only)

Don't change command surface at all. Just modify the **output contract** so that when the deep-research-agent (via target #1) happens to use octocode, those findings get their own section:

```markdown
## Findings (Web)
[Tavily-sourced bullets]

## Findings (Cross-Repo Code)
[Octocode-sourced bullets — "as seen in stripe/stripe-python:client.py:142"]

## Sources
| URL/Repo | Backend | Credibility |
```

**Spirit:** Defer the routing question entirely to target #1 (deep-research-agent). The command itself only changes the report template to make octocode findings *attributable*. Lowest-risk change, but lowest user agency.

---

## Wave 2: Adversarial Evaluation

### Candidate A — `--mode code`

| Dimension | Verdict |
|---|---|
| **Discoverability** | Good — `--help` listing shows the flag |
| **User predictability** | Excellent — same flag → same backend |
| **Learning curve** | Low — one flag, two values |
| **Composability** | Mediocre — `code` vs `web` as modes implies they're mutually exclusive; what about "compare React vs Vue" which is hybrid? |
| **Implementation cost** | Low — ~30 LoC in research.md, no agent change required if target #1 lands |
| **Failure handling** | Clear — if `--mode code` and octocode is down, fail loudly |
| **Anti-trigger risk** | Medium — users may pick `--mode code` for the wrong query and get nothing useful |
| **Scope discipline** | Good — adds one flag, doesn't restructure command |
| **Risk if octocode is yanked from npm** | Trivial — remove flag, document deprecation |

**Adversarial critique:** Mode-naming bakes in a worldview (code vs web are the two modes). What happens when someone wants to add a third backend (e.g., scholarly search via Semantic Scholar)? Three modes get crowded. The flag scales poorly.

### Candidate B — `--source octocode`

| Dimension | Verdict |
|---|---|
| **Discoverability** | Good — `--source` is a familiar pattern |
| **User predictability** | Excellent |
| **Learning curve** | Low |
| **Composability** | **Better than A** — `--source all`, `--source octocode,tavily` is a natural extension |
| **Implementation cost** | Low — ~40 LoC including the "all" fan-out logic |
| **Failure handling** | Clear — per-source failure becomes per-source warning in the report |
| **Anti-trigger risk** | Low — user is explicitly naming a backend |
| **Scope discipline** | Excellent — names what the change actually is |
| **Risk if octocode is yanked** | Trivial |

**Adversarial critique:** Slightly more verbose to type (`--source octocode` vs `--mode code`). Users might not realize that a "source" is also implicitly a routing decision (not just a filter).

### Candidate C — Auto-engage on keywords

| Dimension | Verdict |
|---|---|
| **Discoverability** | **Poor** — magic behavior, only documented in the command's "Behavioral Flow" section |
| **User predictability** | **Bad** — different queries trigger different backends with no visible signal |
| **Learning curve** | None (which is good) |
| **Composability** | None — can't override without a flag |
| **Implementation cost** | Medium — needs a keyword regex matrix maintained alongside the command |
| **Failure handling** | Confusing — user didn't ask for octocode and got an octocode failure |
| **Anti-trigger risk** | **High** — false positives ("how do I implement DI in my head" matches `/implement/i`) |
| **Scope discipline** | Mediocre — sneaks behavior change into a no-flag-change PR |
| **Risk if octocode is yanked** | Medium — regex matrix becomes dead code |

**Adversarial critique:** This violates the user-facing principle of "predictability." The user types the same thing twice and might get different backends because they accidentally used a trigger word. The "magic" feels clever in demos and frustrating in daily use.

### Candidate D — `--depth deep+code` tier

| Dimension | Verdict |
|---|---|
| **Discoverability** | Good — listed in `--depth` enum |
| **User predictability** | Mediocre — `deep+code` is one knob that bundles two decisions (depth + backend) |
| **Learning curve** | Low |
| **Composability** | **Bad** — can't get `--depth quick` + octocode, or `--depth exhaustive` *without* octocode |
| **Implementation cost** | Low |
| **Failure handling** | Mediocre — if octocode fails, does `deep+code` degrade to `deep`? Silent or loud? |
| **Anti-trigger risk** | Medium |
| **Scope discipline** | Bad — conflates depth (a quantitative knob) with backend choice (a qualitative knob) |
| **Risk if octocode is yanked** | Medium — `deep+code` becomes a synonym for `deep`, confusing |

**Adversarial critique:** Conflating orthogonal axes is a known anti-pattern. Today `--depth` controls *how many hops*; suddenly `deep+code` also controls *which backends*. Future users will need to remember which depth tiers include octocode and which don't. This rots quickly.

### Candidate E — Sub-command `/sc:research code <query>`

| Dimension | Verdict |
|---|---|
| **Discoverability** | Good — `/sc:research --help` lists sub-commands |
| **User predictability** | Excellent — sub-command names the intent crisply |
| **Learning curve** | Medium — three new sub-commands is more to learn than one flag |
| **Composability** | Mediocre — sub-commands are mutually exclusive; can't `/sc:research code+pr` |
| **Implementation cost** | **High** — three new behavior sections in research.md, possibly three new frontmatter blocks or three new files |
| **Failure handling** | Excellent — per-sub-command tool list scopes failures |
| **Anti-trigger risk** | Low — sub-command explicitly declares intent |
| **Scope discipline** | **Bad** — expands command surface area substantially |
| **Risk if octocode is yanked** | High — three sub-commands become broken, big deprecation surface |

**Adversarial critique:** Sub-commands add structural weight. Users now have to remember three new verbs. For a single-purpose research command, this feels like a redesign rather than an integration. Also: if `/sc:research package <name>` exists, is it different from `packageSearch` available inside `/sc:research code <query>`? Surface area sprawl.

### Candidate F — Hybrid by default, planner-driven

| Dimension | Verdict |
|---|---|
| **Discoverability** | **Worst** — invisible |
| **User predictability** | **Worst** — planner non-determinism |
| **Learning curve** | None |
| **Composability** | None |
| **Implementation cost** | Medium — pushes work into target #1 (deep-research-agent planner) |
| **Failure handling** | Confusing — user has no mental model of when octocode is invoked |
| **Anti-trigger risk** | **Worst** — planner LLM decides; rate-limit thrash possible |
| **Scope discipline** | Mediocre |
| **Risk if octocode is yanked** | High — planner logic needs surgery |

**Adversarial critique:** Maximum magic = maximum support burden. When a user reports "my research didn't include code patterns even though it should have," debugging requires inspecting the planner's reasoning trace, not just reading flag values. Untenable for a user-facing command.

### Candidate G — Report section only (deferred to target #1)

| Dimension | Verdict |
|---|---|
| **Discoverability** | None — no surface change |
| **User predictability** | Good — behavior unchanged |
| **Learning curve** | None |
| **Composability** | N/A |
| **Implementation cost** | **Lowest** — ~10 LoC in the Output Standards section |
| **Failure handling** | Inherited from target #1 |
| **Anti-trigger risk** | None |
| **Scope discipline** | Excellent — defers the hard question |
| **Risk if octocode is yanked** | Trivial — section becomes empty |

**Adversarial critique:** This isn't really an integration — it's a presentation polish that depends on target #1 doing the actual work. If we ship *only* G, the user has no way to *deliberately* request a code-research-flavored investigation; they're at the mercy of the planner.

### Comparison summary

| Candidate | Predictability | Cost | Risk | Scope | Composability | Net |
|---|---|---|---|---|---|---|
| A — `--mode code` | High | Low | Low | Good | Mediocre | **Solid** |
| B — `--source octocode[,...]` | High | Low | Low | Excellent | Excellent | **Strongest** |
| C — Keyword auto-engage | Low | Medium | Medium | Mediocre | None | Weak |
| D — `--depth deep+code` | Mediocre | Low | Medium | Bad | Bad | Weak |
| E — Sub-command split | High | High | High | Bad | Mediocre | Mixed |
| F — Planner-driven hybrid | Low | Medium | High | Mediocre | None | **Weakest** |
| G — Report section only | N/A | Trivial | Trivial | Excellent | N/A | **Complementary** |

---

## Wave 3: Convergence

**Winner:** **Candidate B (`--source octocode`) + Candidate G (report section)** as a layered pair.

**Why B wins over A:** Both are good. B wins on three points:

1. **Composability** — `--source octocode,tavily` (the hybrid case) is a natural extension of B but requires inventing `--mode hybrid` (a third magic word) in A.
2. **Scope honesty** — B names what is actually changing (the source/backend), not a worldview (the "mode"). When Semantic Scholar shows up next year, `--source semscholar` slots in; in A you'd be inventing `--mode academic`.
3. **Alignment with `deep-research-agent`** — The agent's Tool Selection Policy already treats Tavily/Context7/Sequential as *axes* (sources). B mirrors that ontology in the user surface. A introduces a new ontology (modes).

**Why G complements B:** Even with B in place, two scenarios produce octocode output:

- User explicitly invokes `--source octocode` or `--source all`.
- User invokes default `/sc:research` and target #1 (the deep-research-agent change) routes some sub-investigation to octocode internally.

In **both** cases, the report needs to *attribute* octocode findings cleanly so the user knows what came from where. G is the presentation contract that makes B's output legible.

**Why not C, D, E, F:**

- **C, F** — Magic routing fails the user-facing predictability test. The front door must be deterministic.
- **D** — Conflates orthogonal axes (depth × backend). Will be regretted within a quarter.
- **E** — Sub-command split is a bigger redesign than needed. The cost is not justified by the marginal benefit over B.

---

## Recommended Design (Deep Dive)

### Full description

Add **`--source`** as a new flag to `/sc:research`, accepting `tavily` (default), `octocode`, `context7`, or comma-separated combinations (e.g., `--source octocode,tavily`, `--source all`).

Add **`octocode`** to the command's `mcp-servers:` frontmatter list.

Add a **"Source Selection"** subsection under "Behavioral Flow" documenting routing semantics, rate-limit behavior, and failure handling.

Add a **"Findings by Backend"** subsection to the Output Standards so reports separate web-sourced findings from cross-repo code findings, with per-citation backend tagging.

Keep the existing `--depth` and `--strategy` flags unchanged — they remain orthogonal knobs (depth = how thorough; strategy = how to plan; source = which backend(s)).

### Concrete diff sketch to `research.md`

**Frontmatter change (line 6):**

```yaml
# BEFORE
mcp-servers: [tavily, sequential, playwright, serena]

# AFTER
mcp-servers: [tavily, octocode, sequential, playwright, serena]
```

**Context Trigger Pattern (line 25):**

```diff
- /sc:research "[query]" [--depth quick|standard|deep|exhaustive] [--strategy planning|intent|unified]
+ /sc:research "[query]" [--depth quick|standard|deep|exhaustive] [--strategy planning|intent|unified] [--source tavily|octocode|context7|all|<comma-list>]
```

**New section after "Adaptive Depth" (after line 91), before "MCP Integration":**

```markdown
### Source Selection

Choose which research backends to invoke. Sources are orthogonal to `--depth` and `--strategy`.

| Source | Backend | Best for | Rate limit |
|---|---|---|---|
| `tavily` (default) | Tavily MCP | Concept research, news, blogs, current events | Generous |
| `octocode` | Octocode MCP (GitHub semantic) | "How do real projects implement X", PR archaeology, package investigation | **30 req/min** on GitHub Search API |
| `context7` | Context7 MCP | Canonical library/framework/SDK docs | Library-side |
| `all` | All three in parallel | Comprehensive triangulation; expect 2-3x token cost | Slowest source binds |
| `<comma-list>` | e.g., `octocode,tavily` | Cross-source comparison | As above |

**Defaults:** `--source tavily` if omitted. This preserves existing behavior.

**Source failure handling:**

- A single-source invocation (`--source octocode`) that fails surfaces the error to the user explicitly. The report is *not* emitted.
- A multi-source invocation (`--source all`, `--source octocode,tavily`) that has one source fail emits a partial report with a "Sources unavailable" callout. Successful sources still produce findings.
- Octocode rate-limit (HTTP 403 from GitHub Search) → command waits up to 30s for the limit window, then reports as a soft failure.

**Anti-triggers — do NOT use `--source octocode` when:**

- The query is about concepts, definitions, news, or non-code topics.
- The query targets a specific library's documented API — use `--source context7` instead.
- The query is about the local repository — use `auggie` via `/sc:analyze` or `/sc:troubleshoot`, not `/sc:research`.
```

**MCP Integration section (replace lines 93-98):**

```diff
 ## MCP Integration

 - **Tavily**: Primary search and extraction engine (default `--source tavily`)
+- **Octocode**: Cross-repo GitHub code research — opt-in via `--source octocode` (or `all`). Tools used: `githubSearchCode`, `githubSearchPullRequests`, `githubGetFileContent`, `githubViewRepoStructure`, `packageSearch`. Pinned version + telemetry disabled per project policy.
 - **Sequential**: Complex reasoning and synthesis
 - **Playwright**: JavaScript-heavy content extraction
 - **Serena**: Research session persistence
```

**Output Standards section (replace lines 100-105):**

```diff
 ## Output Standards

 - Save reports to `claudedocs/research_[topic]_[timestamp].md`
 - Include executive summary
 - Provide confidence levels
-- List all sources with citations
+- List all sources with citations **tagged by backend**: `[tavily]`, `[octocode]`, `[context7]`, `[websearch fallback]`
+- When `--source` includes multiple backends, emit findings under separate H2 sections:
+  - `## Findings (Web — Tavily)`
+  - `## Findings (Cross-Repo — Octocode)`
+  - `## Findings (Library Docs — Context7)`
+- Sources table includes a `backend` column matching the deep-research-agent's source citation contract.
```

**Examples section (replace lines 107-113):**

```diff
 ## Examples

 ```
 /sc:research "latest developments in quantum computing 2024"
 /sc:research "competitive analysis of AI coding assistants" --depth deep
 /sc:research "best practices for distributed systems" --strategy unified
+/sc:research "how do production FastAPI projects implement rate limiting" --source octocode
+/sc:research "compare React vs Vue server-side hydration" --source all --depth deep
+/sc:research "what does pydantic-ai actually do under the hood" --source octocode,context7
 ```
```

### New flags / sub-commands defined

| Flag | Values | Default | Semantics |
|---|---|---|---|
| `--source` | `tavily` \| `octocode` \| `context7` \| `all` \| comma-list (e.g. `octocode,tavily`) | `tavily` | Selects backend(s) for the run. Multiple sources fan out in parallel. |

No sub-commands. No new modes. No keyword auto-routing.

### Tool subset used

When `--source octocode` (or `all`, or a list including `octocode`) is active, the deep-research-agent gains access to:

- `mcp__octocode__githubSearchCode`
- `mcp__octocode__githubSearchPullRequests`
- `mcp__octocode__githubGetFileContent`
- `mcp__octocode__githubViewRepoStructure`
- `mcp__octocode__packageSearch`

Explicitly **excluded** (per `octocode-research.md` §6 — these overlap with auggie/serena/Read):

- `localSearchCode`, `localViewStructure`, `localFindFiles`, `localGetFileContent`
- `lspGotoDefinition`, `lspFindReferences`, `lspCallHierarchy`
- `githubCloneRepo` (writes to disk; not needed for research)

This is enforced via `TOOLS_TO_RUN=githubSearchCode,githubSearchPullRequests,githubGetFileContent,githubViewRepoStructure,packageSearch` in the MCP server registration (target #5 in the fit analysis), not in `research.md`.

### User-facing examples — 3 concrete invocations showing different behaviors

**Example 1 — Default (unchanged behavior):**

```
/sc:research "current state of WebAssembly component model standardization" --depth standard
```

Backend: Tavily-only. Report has one `## Findings` section. Identical to today's behavior. Smoke test: confirms no regression.

**Example 2 — Code-focused investigation:**

```
/sc:research "how do production Rust web servers handle graceful shutdown" --source octocode --depth deep
```

Backend: Octocode-only. The agent invokes `githubSearchCode("graceful shutdown")` filtered to Rust repos, fans out `githubGetFileContent` reads on top-K hits, optionally cross-references via `githubSearchPullRequests("graceful shutdown")` on `tokio-rs/axum`, `hyperium/hyper`, `actix/actix-web`. Report has one `## Findings (Cross-Repo — Octocode)` section with citations like `tokio-rs/axum:examples/graceful-shutdown/src/main.rs:42`.

**Example 3 — Triangulation across backends:**

```
/sc:research "best practices for FastAPI dependency injection" --source all --depth deep
```

Backends: Tavily (blog posts, tutorials) + Octocode (real codebases using `Depends()`) + Context7 (canonical FastAPI docs). Three `## Findings` sections in the report, each backend-tagged. The Sequential MCP synthesis pass produces a final `## Synthesis` section reconciling all three. Highest-quality output, ~2-3x token cost of single-source runs.

### Anti-trigger rules

The command itself does not auto-engage octocode. The user must explicitly include it in `--source`. Reasons:

- User-facing predictability is paramount.
- The 30 req/min GitHub Search API limit means accidental octocode invocations on irrelevant queries waste a rate-limit slot that a deliberate later query needs.
- Telemetry concerns (per `octocode-research.md` §4.2) — even with `LOG=false`, opt-in is the conservative default.

### Rate-limit / failure handling (user-visible)

**Tavily failure (single-source `--source tavily`):** Existing behavior — fall back to WebSearch/WebFetch per the deep-research-agent's Fallback Policy.

**Octocode failure (single-source `--source octocode`):**

| Condition | Behavior |
|---|---|
| Octocode MCP not installed / not registered | Command refuses to run, prints install hint: `superclaude mcp --servers octocode` |
| Octocode MCP installed but `GITHUB_TOKEN` missing | Command refuses, prints `gh auth status` hint |
| GitHub Search API 403 (rate limit) | Wait up to 30s for window reset; if still failing, emit partial report with rate-limit callout |
| GitHub Search API 5xx | Retry twice with exponential backoff; if still failing, emit failure report |
| Octocode returns 0 results across all tools | Emit report with explicit "no cross-repo findings — try `--source tavily` for conceptual search" callout |

**Multi-source failure (`--source all` or comma-list):**

- Each source runs in parallel and is failure-isolated.
- Report includes a `## Sources Unavailable` section listing any backend that didn't return.
- Report is emitted with whichever sources succeeded — no all-or-nothing.

**Citation contract:** Every fact in the report has a `[backend]` tag matching its source. Sources table has explicit `backend` column. If the deep-research-agent silently falls back (e.g., octocode→WebSearch), the fallback is annotated in the source row (`fallback_reason: octocode_rate_limit`), per the existing `deep-research.md:46-47` policy extended to octocode.

### Test plan — 5 example queries and expected behavior

| # | Query | Expected backend | Expected report shape | Pass criteria |
|---|---|---|---|---|
| 1 | `/sc:research "history of the OAuth 2.0 specification"` | Tavily (default) | Single `## Findings` section, all citations tagged `[tavily]` | Backward compat — no octocode invocation |
| 2 | `/sc:research "show me three production examples of pydantic-ai agent registration" --source octocode` | Octocode-only | `## Findings (Cross-Repo — Octocode)` with file:line citations | Octocode tools invoked; no Tavily call in trace |
| 3 | `/sc:research "compare GraphQL federation strategies" --source all --depth deep` | Tavily + Octocode + Context7 in parallel | Three findings sections + `## Synthesis` | All three backends invoked; report emitted even if one fails |
| 4 | `/sc:research "explain my codebase's auth flow" --source octocode` | Octocode invoked but should warn | Report includes anti-trigger callout: "for local codebase questions use `/sc:analyze` or `/sc:troubleshoot`" | Anti-trigger guidance surfaces |
| 5 | `/sc:research "production rate limiting in FastAPI" --source octocode` *(simulated rate limit)* | Octocode rate-limited | Partial report with rate-limit callout + suggestion to retry in 30s | Failure surfaces to user; no silent degradation |

---

## What This Cannot Do

- **Cannot make octocode "as easy as Tavily."** Octocode requires `GITHUB_TOKEN` (or `gh auth login`) and a one-time MCP install. The `--source octocode` path will hard-fail with a helpful error if either is missing — that's intentional but is friction the user will hit.
- **Cannot fix the supply-chain risk.** Pinning a version + `LOG=false` + tool whitelisting (handled in target #5) reduces blast radius but does not eliminate the bus-factor-of-1 maintainer concern. The `/sc:research` user surface can only choose to expose or hide this; we expose it via opt-in.
- **Cannot turn `/sc:research` into a code-modification tool.** The `STOP AFTER RESEARCH REPORT` boundary (lines 122-140) is preserved verbatim. Octocode is read-only by design (`octocode-research.md` §1), so this aligns naturally.
- **Cannot guarantee cross-source coherence.** When `--source all` is used, the three backends may produce contradictory findings (e.g., Tavily blog says "use approach X," octocode shows everyone uses approach Y, Context7 says approach Z is canonical). The synthesis section flags contradictions but does not resolve them — the user does.
- **Cannot replace `auggie` for local codebase research.** The anti-trigger rule explicitly redirects local-repo queries away from this command, because octocode is for *external* GitHub repos and auggie is for the *local* repo.

---

## UX Considerations

### Failure visibility (user-facing front door)

The user typed `/sc:research`. They expect a report. Three failure modes need explicit handling:

1. **Hard fail (single-source unavailable):** Show a 4-line message with the install/auth fix. Don't write a partial report — the user asked for a specific source and didn't get it.
2. **Soft fail (one source in a multi-source run):** Write the report. Lead with a callout box: "Source `octocode` was unavailable (rate-limited); findings below are from Tavily + Context7 only." Suggest retry in N seconds.
3. **Empty result (source returned nothing):** Write a report with an explicit "no findings from `<source>`" section, plus a suggestion of which `--source` value might fit better.

### Provenance — "which source produced what?"

Every finding in the report carries a `[backend]` tag at the end of its bullet:

```markdown
- Production Rust web servers commonly use `tokio::signal::ctrl_c()` for graceful shutdown,
  paired with a broadcast channel to notify worker tasks.
  [tokio-rs/axum:examples/graceful-shutdown/src/main.rs:42] [octocode]
```

```markdown
- The official Rust async book recommends pairing graceful shutdown with structured concurrency
  patterns.
  [https://rust-lang.github.io/async-book/...] [tavily]
```

The Sources table at the end of the report has explicit columns: `Source | Backend | Credibility | Notes`. This matches the deep-research-agent's existing citation contract (line 64) — `/sc:research` does not invent a new contract, it just inherits it.

### Discoverability

`--source` is documented in:

- The command's `Context Trigger Pattern` line (visible in `--help`)
- A dedicated `### Source Selection` section under Behavioral Flow
- The Examples section (three examples cover three different `--source` shapes)
- The MCP Integration section (per-source description)

Users who don't read docs and just type `/sc:research "query"` get unchanged default behavior. Discoverability is "pull" (look it up when you need it), not "push" (no auto-prompts).

### Cognitive load

Adding `--source` to a command that already has `--depth` and `--strategy` is a third orthogonal knob. To keep cognitive load manageable:

- `--source` is **optional** with a sensible default (`tavily`).
- The three knobs are **independent** — every combination is valid.
- The Examples section shows that 90% of users will never pass `--source`.
- Power users (the target audience for `--source octocode`) self-select.

---

## Cross-Target Dependencies

### Hard dependency on Target #1 (deep-research-agent integration)

`/sc:research`'s frontmatter declares `personas: [deep-research-agent]` (line 7). The command **delegates** to that agent. If the agent doesn't know how to use octocode tools, `--source octocode` has nothing to dispatch to.

**Therefore:** Target #1 MUST land before Target #3 ships, OR Target #3 must bundle the relevant agent change.

Two ways to sequence:

| Sequencing | Pros | Cons |
|---|---|---|
| **#1 then #3** (recommended) | #3 is a small declarative diff; #1 does the heavy lifting once and propagates everywhere | #3 must wait |
| **#3 bundles #1 changes** | Single PR, no sequencing risk | Conflates two separate scopes; harder review |

### Hard dependency on Target #5 (MCP server registration in `install_mcp.py`)

`octocode` must be installable as an MCP server before `--source octocode` can resolve to a real backend. This is foundational (per `octocode-fit-analysis.md` §Phase A) and must land first regardless of which targets follow.

### Soft dependency on Target #2 (tech-research skill Phase 4)

Independent — `/sc:research` is the ad-hoc/interactive front door; `tech-research` is the formal stateful skill. They share the `deep-research-agent` persona via different surfaces, so both benefit from target #1, but neither depends on the other.

### Bypass option

`/sc:research` could short-circuit the deep-research-agent and invoke octocode tools directly when `--source octocode` is set. This is **not recommended** because:

- It duplicates the agent's Tool Selection Policy / Fallback Policy / citation contract in the command file.
- It creates two code paths (with-agent vs without-agent) that drift.
- It makes target #1's changes invisible to `/sc:research` users.

Keep the delegation pattern. Make octocode a first-class tool in the agent.

---

## Effort Estimate

| Phase | Work | LoC | Effort | Notes |
|---|---|---|---|---|
| **Prereq A** | Target #5 — MCP server registration in `install_mcp.py` | ~15 | 1h | Pinned version + tool whitelist + `LOG=false` |
| **Prereq B** | Target #1 — deep-research-agent gains octocode tools + 4th axis in Tool Selection Policy | ~30 | 2h | Brainstormed separately as target #1 |
| **This target — research.md edits** | Frontmatter `mcp-servers` extension + `--source` flag docs + Source Selection section + Output Standards update + examples | ~50 | 1.5h | Pure declarative; no code |
| **Tests** | Add 5 test queries to `tests/` (smoke + per-source + multi-source + anti-trigger + rate-limit-sim) | ~80 | 2h | Most are smoke tests against a recorded MCP fixture |
| **Docs** | Update `docs/user-guide/commands.md` for `--source` flag | ~15 | 0.5h | One paragraph + example block |
| **Sync** | `make sync-dev` + `make verify-sync` | — | 0.1h | Mechanical |
| **Total (this target only)** | | **~145** | **~4h** | Excluding prereqs |
| **Total with prereqs** | | **~190** | **~7h** | One PR for prereqs, one PR for this |

**Risk-adjusted estimate:** 1.5x → **6h for this target alone, 10h with prereqs**, allowing for:

- Discovery that the rate-limit detection in deep-research-agent needs extension for octocode's GitHub Search 403 (different from Tavily's quota error)
- One round of UX iteration on the report's `## Findings (Backend)` section heading conventions
- One round of CLAUDE.md guidance update if the `--source` flag interacts with existing rules

**No new agents, no new skills, no new CLI sub-commands.** Pure declarative integration aligned with existing patterns.

---

**Status:** Brainstorm complete. Ready for Wave 3 synthesis across all 5 parallel agents.
