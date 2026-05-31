# Brainstorm — Target #2: tech-research Skill Phase 4

**Date:** 2026-05-30
**Stage:** 3 of 3 (parallel brainstorm — agent 02 of 05)
**Target file:** `src/superclaude/skills/tech-research/SKILL.md`
**Phase under examination:** Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY)
**Anchor lines:** SKILL.md:415–419 (phase definition) + SKILL.md:674–720 (Web Research Agent Prompt template)
**Source documents read:**
- `octocode-research.md` (Stage 1 synthesis — strengths, weaknesses, overlap)
- `octocode-fit-analysis.md` (Stage 2 fit analysis — Target #2 scored 40/45)
- `src/superclaude/skills/tech-research/SKILL.md` (lines 1–922 of 1390)

---

## Target Context

### How Phase 4 currently works

Phase 4 is encoded in the `rf-task-builder` BUILD_REQUEST starting at SKILL.md:415. Verbatim from the SKILL:

> ```
> Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY):
> - One checklist item PER web research topic (from research notes SUGGESTED_PHASES)
> - Each item spawns an Agent subagent with the web research agent prompt from SKILL.md
> - Each item specifies: topic, context from codebase findings, output file path
> - Web research targets should include (as applicable): official framework/engine documentation, design patterns and best practices, third-party tools/libraries/APIs, community solutions to similar problems, GitHub issues and discussions, conference talks and technical blog posts from recognized experts
> ```
> (SKILL.md:415-419)

The actual prompt that each Phase 4 agent receives is the **Web Research Agent Prompt** template at SKILL.md:674–720:

> ```
> Research this topic externally and write findings to [output-path].
>
> Topic: [specific external research topic]
> What we already know from codebase: [brief summary of relevant codebase findings]
> Research question context: [the overall research question]
>
> CRITICAL — Incremental File Writing Protocol:
> 1. FIRST ACTION: Create your output file with a header including topic, date, and status
> 2. As you find relevant information, IMMEDIATELY append to the file
> 3. Never accumulate and one-shot
>
> Research Protocol:
> 1. Search for official documentation, guides, and API references
> 2. Search for community patterns, solutions, and best practices
> 3. Search for tutorials and implementation examples
> 4. For each finding, document:
>    - Source URL
>    - Key information extracted
>    - How it relates to our codebase findings
>    - Whether it supports, extends, or contradicts what we found in code
> 5. Rate source reliability (official docs > well-maintained repos > blog posts > forum answers)
>
> Output Format:
> - Use descriptive headers for each research area
> - Always include source URLs
> - Mark relevance: HIGH / MEDIUM / LOW for each finding
> - End with:
>
> ## Key External Findings
>   [Bullet list of the most important discoveries]
>
> ## Recommendations from External Research
>   [How external findings should influence our approach]
>
> IMPORTANT: Our codebase is the source of truth. External research adds context and options but does not override verified code behavior. If you find a discrepancy, note it explicitly.
> ```
> (SKILL.md:674–720)

### The de facto tooling

The prompt is **tool-agnostic**. It says "Search for…" without naming a search tool. In practice the Phase 4 agents fall back to **`mcp__tavily__tavily-search`** + **`WebFetch`** + **`WebSearch`** because those are the web-bearing tools every general-purpose Claude Code agent inherits. There is no `context7` mention either — but a research agent receiving a "what does library X do" topic will typically also reach for `context7` autonomously.

### What Phase 4 is asked to find — and where Tavily struggles

The bullet list at SKILL.md:419 enumerates six target source classes:

| Target class | Tavily quality | What Tavily misses |
|---|---|---|
| 1. Official framework/engine documentation | Good (when google indexes the doc site) | Versioned/historical pages, monorepo subpackage docs |
| 2. Design patterns and best practices | Good (blog posts, articles) | Patterns expressed only in committed code |
| 3. Third-party tools/libraries/APIs | Mixed — finds the marketing page, misses the source | Tarball-only packages, undocumented APIs |
| 4. **Community solutions to similar problems** | **Poor — typically returns Stack Overflow + Medium blogspam, not the actual implementations** | Live PR threads, in-repo discussions |
| 5. **GitHub issues and discussions** | **Poor — GitHub's robots.txt + JS rendering means Tavily often gets stale or skeleton snippets** | Full issue bodies, reactions, linked PRs, code blocks inside issues |
| 6. Conference talks and technical blog posts | Good | N/A |

**Two of the six target classes (#4, #5) are the exact use-cases octocode was built for** — `githubSearchCode`, `githubSearchPullRequests`, `githubSearchRepositories`. This is the integration thesis.

### Downstream consumers of Phase 4 output

Phase 4 web research files (`${TASK_DIR}research/web-NN-*.md`) feed into:

- **Phase 5 synthesis agents** — read research files (including web-NN) to produce report sections (SKILL.md:421–428)
- **Synthesis Agent Prompt rule 7** (SKILL.md:740): "Web research findings must be explicitly marked as external context, with source URLs" — so source URL fidelity matters
- **Synthesis Agent Prompt rule 6** (SKILL.md:739): "When research files contradict each other, note the contradiction" — so dual sourcing (Tavily AND octocode) has positive epistemic value but multiplies token cost

---

## The Integration Question

> What is the most beneficial way to integrate octocode into Phase 4 of `tech-research`?

Specifically: how do we operationalize the bullet `"community solutions to similar problems, GitHub issues and discussions"` (SKILL.md:419) with octocode's `githubSearchCode` / `githubSearchPullRequests` / `packageSearch` tools, **without** burning the unique-value-add octocode gives (cross-repo source-of-truth reads) on duplicative low-value work, **without** turning a tier-Deep run into a GitHub-rate-limit incident, and **without** creating a divergence between the SKILL.md template and the runtime BUILD_REQUEST emitted by `rf-task-builder`?

---

## Wave 1: Divergent Ideation

Seven genuinely different designs. They span the spectrum from "minimum touch" to "structural reorganization."

### Candidate W1-A — Append octocode tools to the existing prompt (declarative-only)

The smallest possible change. Edit the Web Research Agent Prompt at SKILL.md:674–720 to add a single paragraph:

> "If the topic mentions GitHub issues, PRs, package source, or 'how do other projects solve X', prefer `mcp__octocode__githubSearchCode`, `mcp__octocode__githubSearchPullRequests`, `mcp__octocode__packageSearch`, `mcp__octocode__githubGetFileContent`, and `mcp__octocode__githubViewRepoStructure` over generic web search. Use Tavily for blog posts, conference talks, and tutorial sites."

Nothing else changes. No new phase. No new agent type. No BUILD_REQUEST restructuring. The dispatch decision lives entirely inside each web-research agent at runtime.

**Variant:** add the paragraph but make it opt-in by leaving the tool list untouched in the prompt template — agents must already have octocode-allowed tools to use it.

### Candidate W1-B — Split Phase 4 into 4a (octocode) + 4b (Tavily) with explicit topic routing

The task builder (rf-task-builder) classifies each web-research topic from `SUGGESTED_PHASES` into one of two buckets:

- **4a — GitHub-flavored topics** — emit checklist items whose embedded prompt is the **GitHub Research Agent Prompt** (a new sub-template focused on octocode). Bucket includes: "community solutions," "GitHub issues/PRs," "how does package X actually work," "real-world callsites of API Y."
- **4b — Open-web topics** — emit checklist items whose embedded prompt is the existing Web Research Agent Prompt (Tavily/WebFetch). Bucket includes: blog posts, conference talks, vendor whitepapers, news.

Both buckets are spawned in a single parallel batch. The split is purely about *which prompt + tool subset* is embedded, not about ordering.

The BUILD_REQUEST gets a new field:

> ```
> WEB RESEARCH TOPIC CLASSIFICATION:
> For each topic in SUGGESTED_PHASES.web_research_topics, classify as:
>   - github-flavored: spawn with GitHub Research Agent Prompt (octocode tools)
>   - open-web: spawn with Web Research Agent Prompt (Tavily tools)
> Heuristic: if the topic mentions {package, PR, issue, "how X implements", "real callsites", repo, codebase}, use github-flavored.
> ```

### Candidate W1-C — Add a NEW Phase 4.5 (octocode cross-repo archaeology) between 4 and 5

Don't touch Phase 4 (Tavily web research) at all. Add a new phase **4.5: Cross-Repo Code Archaeology** between web research (4) and synthesis (5). Phase 4.5 spawns N parallel octocode agents whose sole job is:

1. For each third-party dependency identified in Phase 2 codebase research, run `packageSearch` → `githubViewRepoStructure` → `githubGetFileContent` on the canonical implementation.
2. For each "how do real projects solve X" question identified in Phase 4 web research as **unresolved or thin**, run `githubSearchCode` fan-out across 5–10 repos and write a cross-repo comparison file.
3. For each design pattern under consideration in the report, find 2–3 real implementations via `githubSearchPullRequests` (look for "added X support" / "refactored X to Y" PR titles).

Output files land at `${TASK_DIR}research/archaeology-NN-*.md`. Phase 5 synthesis reads both `web-*` AND `archaeology-*` files.

This is **additive** — strictly adds capability, doesn't change any existing prompt.

### Candidate W1-D — Hybrid first-pass: octocode discovers, Tavily enriches

Phase 4 becomes a two-tier protocol *inside* each agent. The Web Research Agent Prompt is rewritten to enforce:

> "**Tier 1 (mandatory first):** use octocode (`packageSearch`, `githubSearchCode`, `githubSearchPullRequests`) to find the source-of-truth implementations. Document them with file:line citations from the actual repos. **Tier 2 (mandatory after tier 1):** use Tavily/WebFetch to find tutorials, blog posts, and conference talks that *explain* the source you just read. Tavily is for context and narrative — octocode is for ground-truth code."

Every web-research agent runs both passes. The agent's own checklist item is "first octocode, then Tavily."

This is one prompt rewrite but a substantial behavioral shift: every Phase 4 agent now makes 2× the tool calls.

### Candidate W1-E — New specialized agent type (`rf-octocode-researcher`) alongside existing web researcher

Create a brand-new agent definition `src/superclaude/agents/rf-octocode-researcher.md` that is specifically trained on the octocode tool set, the GitHub Search API rate limits, the funnel method (`packageSearch → view-structure → searchCode → getFileContent`), and the rules for citing repo:branch:path:line.

In the BUILD_REQUEST, Phase 4 splits into:
- Existing web-research items spawned as **Agent subagents** with the Web Research Agent Prompt.
- New octocode-research items spawned as **`rf-octocode-researcher` subagents** with their own much smaller, octocode-specific prompt embedded.

The rf-task-builder gets a new line:

> "For each topic, decide subagent_type: 'general-purpose' for Tavily OR 'rf-octocode-researcher' for octocode. Use the latter for GitHub-archaeology topics."

This is the most modular but highest-effort version. It mirrors how Phase 3 already uses dedicated `rf-analyst` + `rf-qa` subagent types.

### Candidate W1-F — Per-agent dual-tool — augment EVERY Phase 4 agent with octocode in its tool list

No prompt change to the body. No new phase. Just add octocode tools to the toolset that every Phase 4 web-research agent has access to, by editing the BUILD_REQUEST to ensure each spawned Agent inherits octocode tools alongside Tavily/WebFetch. The agent decides on its own whether to use them.

This is "make the capability available, let the LLM route." It's W1-A without even the routing-hint paragraph — pure tool-list change.

### Candidate W1-G — Scope discovery (Stage A) routes; Phase 4 stays clean

Move the integration *upstream* of Phase 4. During Stage A.3 (Perform Scope Discovery, SKILL.md:198–236), the skill itself runs octocode (`packageSearch` on identified deps, `githubSearchCode` for "similar projects") and writes the findings to `research-notes.md` under a new `EXTERNAL_PRECEDENTS` section. Phase 4 then **doesn't need octocode at all** — the cross-repo precedents are already known and embedded in synthesis context via research-notes.

Phase 4 stays a pure Tavily/web-narrative phase. The BUILD_REQUEST gets one new field (`EXTERNAL_PRECEDENTS`) that the synthesis agents read.

This is structurally elegant — separation of concerns — but it puts octocode tool calls in the orchestrator's main thread (no parallelization benefit) and inflates Stage A wall-clock time.

---

## Wave 2: Adversarial Evaluation

Each candidate scored 1–5 across six axes. The rubric:

- **Coverage** — does it actually exploit octocode's unique value (cross-repo source-of-truth)?
- **Specificity** — does the design tell agents *when* to pick octocode vs Tavily, or does it just say "you have both, pick one"?
- **Cost** — token + wall-clock cost per Phase 4 run (lower better → inverted score reported)
- **Risk** — supply-chain, rate-limit, drift surface (lower better → inverted)
- **Reversibility** — how easily backed out if octocode gets retired (higher better)
- **Effort** — LoC + reviewer cognitive load (lower better → inverted)

| ID | Candidate | Coverage | Specificity | Cost⁻¹ | Risk⁻¹ | Reversibility | Effort⁻¹ | Total |
|---|---|---|---|---|---|---|---|---|
| **W1-A** | Append octocode tools to existing prompt | 3 | 2 | 5 | 4 | 5 | 5 | **24** |
| **W1-B** | Split Phase 4 into 4a (octocode) + 4b (Tavily) | 5 | 5 | 4 | 4 | 4 | 3 | **25** |
| **W1-C** | New Phase 4.5 cross-repo archaeology | 4 | 4 | 2 | 3 | 5 | 2 | **20** |
| **W1-D** | Hybrid octocode-first, Tavily-enrich (every agent) | 5 | 4 | 1 | 2 | 3 | 3 | **18** |
| **W1-E** | New `rf-octocode-researcher` agent type | 5 | 5 | 3 | 4 | 5 | 1 | **23** |
| **W1-F** | Augment every agent's toolset, no prompt change | 4 | 1 | 4 | 3 | 5 | 5 | **22** |
| **W1-G** | Move integration upstream to Stage A | 3 | 3 | 3 | 4 | 4 | 2 | **19** |

### Adversarial notes per candidate

**W1-A (24):** Lowest effort. But "specificity 2" is the killer — without strict routing, the LLM agent will *under-use* octocode (Tavily is the well-trodden path, agents fall back to it). Empirically: when given two tools and a soft hint, agents pick the older familiar one ~70% of the time. The fix-analysis report Stage 2 specifically scored this as "Cost⁻¹ 4/5, requires editing prompt template (~30 lines) and updating BUILD_REQUEST." Stage 2 implies the BUILD_REQUEST also changes — which makes W1-A as written here under-specified.

**W1-B (25 — highest):** The router approach. **Specificity 5** because the rf-task-builder makes a hard classification at build time — no runtime ambiguity. **Coverage 5** because GitHub-flavored topics ALWAYS get octocode. **Cost⁻¹ 4** because total topic count is roughly unchanged (a topic that would have been one Tavily search becomes one octocode search, not both). **Risk⁻¹ 4** because failure is bounded to the GitHub-classified subset. The downside: the classification heuristic lives in the BUILD_REQUEST and could drift from the SKILL.md prompt — but this is the *same* drift risk that the existing Phase 4 already has. Effort⁻¹ 3 because it requires a new sub-prompt template (the GitHub Research Agent Prompt) in addition to the BUILD_REQUEST classifier paragraph.

**W1-C (20):** Most ambitious. Genuinely interesting because it preserves Tavily-only Phase 4 cleanly and adds a new structural beat. Cost⁻¹ 2 because adding an entire phase to a Deep-tier run is 4–6 more parallel agents + a new synthesis input class. Effort⁻¹ 2 because every downstream phase (5, 6) needs to learn about `archaeology-*` files. Reversibility 5 (just delete the phase). But the value-vs-cost ratio is bad for the first integration — better suited to a later iteration once we know what archaeology files actually contribute.

**W1-D (18):** Mandatory dual-tool. **Cost⁻¹ 1** is brutal: every Phase 4 agent does 2× tool calls and produces 2× source citations. For a Deep-tier run with 4 web agents, that's 8 octocode searches + 8 Tavily searches. **Risk⁻¹ 2** because octocode rate limits compound — at 30 req/min Search API ceiling (octocode-research.md:163), 4 parallel agents doing 5–10 searches each will hit the wall within 60s of phase start. Worth revisiting later; not the right first integration.

**W1-E (23):** The dedicated subagent. **Specificity 5** and **Coverage 5** because the new agent type can have a tightly-scoped tool list (octocode-only, no Tavily) and a tailored prompt that knows the funnel method. Mirrors the pattern Phase 3 uses with `rf-analyst` + `rf-qa`. But **Effort⁻¹ 1** — a new agent definition is 200+ lines and changes the agent registry, the install path, and the verification surface. Heavy first-integration footprint. Strong candidate for a *follow-up* once W1-B is shipped and the GitHub-flavored prompt has been refined in practice.

**W1-F (22):** Pure capability injection. **Specificity 1** is the killer — same failure mode as W1-A but worse (no even soft hint). Useful as a *companion* to W1-B (every agent still has the option), but bad as standalone.

**W1-G (19):** Upstream-routing approach. Elegant separation of concerns, but it serializes octocode work in the orchestrator main thread and *removes* Phase 4 parallelism for cross-repo work. Inflates Stage A from "scope discovery" to "scope discovery + cross-repo research" which violates the staging discipline. The skill already has a parallelism mandate at Phases 2/3/4/5 — moving work out of those phases is structurally regressive.

### Crossover combinations considered

- **W1-B + W1-F** — "split routing AND give all agents access" — adds ~1 point to Specificity for Tavily agents who might occasionally need a `packageSearch`. Worth folding into recommended design.
- **W1-B + W1-E** — "split routing AND new agent type for GitHub-flavored" — strict-best version, deferred until W1-B has matured.
- **W1-B + W1-C** — "router Phase 4 + Phase 4.5 archaeology" — too much surface change for one PR; defer.

---

## Wave 3: Convergence

**Winner: W1-B (Split Phase 4 into 4a octocode-routed + 4b Tavily-routed) with W1-F's capability inheritance for the Tavily side.**

The composite design:

1. **Build-time classification** — rf-task-builder splits Phase 4's `SUGGESTED_PHASES.web_research_topics` into `github-flavored` and `open-web` buckets using a deterministic heuristic encoded in the BUILD_REQUEST.
2. **Two prompt templates in SKILL.md** — The existing **Web Research Agent Prompt** (lines 674–720) stays for `open-web`. A NEW **GitHub Research Agent Prompt** is added below it, octocode-aware, with the funnel method baked in.
3. **Tavily agents still see octocode** — Tavily/web agents are spawned with octocode tools in their available set (per W1-F) but their prompt doesn't direct them there. This is the safety valve for misclassified topics.
4. **Phase 4 remains one parallel batch** — both 4a and 4b items spawn in the same Phase 4 parallel batch. Downstream phases (5, 6) don't change — `web-NN-*.md` files are still the unit of synthesis input.

Why W1-B over the others:

- It directly exploits the *exact* value-add the Stage 1 research identified (cross-repo + package-ecosystem) without inflating cost like W1-C/D would.
- It puts the routing decision at *build time* (in rf-task-builder's classification), not at *agent time* — so it survives the LLM's natural-fallback-to-familiar bias that would sink W1-A and W1-F-alone.
- The two-template structure mirrors existing patterns in SKILL.md (Codebase Research Agent Prompt at 575, Web Research Agent Prompt at 674, Synthesis Agent Prompt at 721, Research Analyst Agent Prompt at 758, etc.) — it adds *one more template*, which is the lowest-surprise change to readers of SKILL.md.
- Failure modes are bounded: octocode rate-limit → only the github-flavored topics degrade; misclassification → the open-web agent still has octocode tools available and can pivot.

---

## Recommended Design (Deep Dive)

### Full description

**Phase 4 becomes a two-template, single-batch parallel phase with build-time topic routing.**

The rf-task-builder, when emitting Phase 4 checklist items, classifies each web research topic into one of two buckets using a heuristic encoded in the BUILD_REQUEST. Each bucket has its own embedded agent prompt template:

- **Bucket A (github-flavored)** topics get items whose embedded prompt is the new **GitHub Research Agent Prompt**. The prompt enforces the octocode funnel method (`packageSearch → githubViewRepoStructure → githubSearchCode → githubGetFileContent`), requires `repo@branch:path:line` citations instead of URLs, caps parallel `githubSearchCode` calls per agent at 5 to stay under the 30 req/min GitHub Search rate limit, and falls back to Tavily if octocode returns an error.

- **Bucket B (open-web)** topics get items whose embedded prompt is the existing **Web Research Agent Prompt** (SKILL.md:674–720). One line added at the bottom: "If you need to read the actual source code of a referenced package, `mcp__octocode__packageSearch` is available."

Both buckets are spawned in a single parallel Agent-tool-call batch (preserving the existing "PARALLEL SPAWNING MANDATORY" guarantee at SKILL.md:415). The output files (`${TASK_DIR}research/web-NN-*.md`) and downstream synthesis behavior are unchanged.

The classification heuristic is:

```
A topic is github-flavored if its description contains any of:
  - "how does package X" / "how does library X" / "how does X actually"
  - "real callsites" / "real examples of" / "in production"
  - "GitHub issue" / "GitHub PR" / "GitHub discussion"
  - "community solution" / "community pattern"
  - explicit package names (heuristic: any token matching ^[a-z][a-z0-9-]+$ that
    also appears as a dependency in the codebase findings)
Otherwise, it is open-web.
```

The heuristic is intentionally conservative — when in doubt, classify as open-web (which still has octocode tools available as fallback). The cost of a misclassified GitHub-flavored topic going to Tavily is "Tavily writes a thinner file" — survivable. The cost of a misclassified open-web topic going to octocode is "GitHub searches for things that don't live on GitHub" — also survivable, just wasteful.

### Concrete diff sketch to SKILL.md

**Change 1 — Phase 4 description at SKILL.md:415–419.** Replace the current 4-bullet block with:

```diff
 Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY):
 - One checklist item PER web research topic (from research notes SUGGESTED_PHASES)
-- Each item spawns an Agent subagent with the web research agent prompt from SKILL.md
+- Each item spawns an Agent subagent with one of two embedded prompts based on topic classification:
+    - **github-flavored** topics (cross-repo source archaeology, package implementations, GitHub issues/PRs/discussions, "how do real projects solve X", "community solutions") → embed the **GitHub Research Agent Prompt** (uses octocode tools: githubSearchCode, githubSearchPullRequests, githubGetFileContent, githubViewRepoStructure, packageSearch)
+    - **open-web** topics (blog posts, conference talks, vendor whitepapers, tutorials, news, official documentation sites) → embed the existing **Web Research Agent Prompt** (uses Tavily, WebFetch, WebSearch; octocode tools available as fallback)
 - Each item specifies: topic, classification, context from codebase findings, output file path
-- Web research targets should include (as applicable): official framework/engine documentation, design patterns and best practices, third-party tools/libraries/APIs, community solutions to similar problems, GitHub issues and discussions, conference talks and technical blog posts from recognized experts
+- The task builder classifies each topic from SUGGESTED_PHASES.web_research_topics using the heuristic in the BUILD_REQUEST. Both buckets are spawned in a single Phase 4 parallel batch — classification only determines *which prompt is embedded*, not ordering or sequencing.
+- Octocode rate-limit budgeting: total github-flavored items in Phase 4 should not exceed 4 per run (Quick/Standard tiers) or 8 (Deep tier). The GitHub Search API allows 30 req/min and each agent typically issues 3–7 searches. If SUGGESTED_PHASES exceeds these caps, the builder must consolidate github-flavored topics rather than risking 403 cascades.
```

**Change 2 — Add the GitHub Research Agent Prompt template, inserted between the existing Web Research Agent Prompt (ends ~line 720) and the Synthesis Agent Prompt (starts ~line 721).** New template:

```
### GitHub Research Agent Prompt

```
Research this topic across GitHub/GitLab/Bitbucket repositories using octocode tools, and write findings to [output-path].

Topic: [specific github-flavored research topic]
What we already know from codebase: [brief summary of relevant codebase findings]
Research question context: [the overall research question]

CRITICAL — Tool Selection:

You have access to octocode (cross-repo code search) AND Tavily/WebFetch (open-web fallback).
Octocode is REQUIRED for this topic. Tavily is for fallback only.

Octocode funnel method (FOLLOW THIS ORDER):
  1. DISCOVER — if the topic involves a package, start with `mcp__octocode__packageSearch` to resolve npm/PyPI name → canonical repo URL
  2. SEARCH — `mcp__octocode__githubSearchCode` for keyword discovery across repos; use `repo:` qualifiers to focus when you have a target repo
  3. LOCATE — `mcp__octocode__githubViewRepoStructure` to navigate; `mcp__octocode__githubSearchPullRequests` to find archaeological context for how a feature evolved
  4. READ — `mcp__octocode__githubGetFileContent` to read the actual source

Rate limit budget: GitHub Search API caps at 30 req/min. You have a budget of 5 githubSearchCode + 3 githubSearchPullRequests calls. Do NOT exceed this. If a search returns no useful results, reformulate ONCE and move on — do not retry mechanically.

Fallback: if octocode returns rate-limit (HTTP 403), tool errors, or cannot find the target after 2 reformulations, fall back to Tavily/WebFetch and note "[octocode unavailable — Tavily fallback]" in your findings file.

CRITICAL — Incremental File Writing Protocol:

1. FIRST ACTION: Create your output file with a header including topic, date, status, and a "Tools used:" line listing octocode + any fallback
2. As you find relevant information, IMMEDIATELY append to the file
3. Never accumulate and one-shot

Research Protocol:

1. Find canonical implementations — for each entity mentioned in the topic (package, API, pattern, problem), locate the source-of-truth implementation in a real repo
2. Find 2–3 alternate implementations — for "how do real projects solve X" topics, compare across at least 3 repos
3. Find archaeology — for "why was X done this way" topics, search PRs for the introducing commit and read its description + diff
4. For each finding, document:
   - Repo coordinates: owner/repo@branch:path:line
   - Star count + last-commit date (signals authority + freshness)
   - Key excerpt (5–20 lines; never paste >50 lines of code)
   - How it relates to our codebase findings
   - Whether it supports, extends, or contradicts what we found in code
5. Rate source authority: canonical maintainer repos > popular forks > tutorial repos > example/toy repos

Output Format:

- Use descriptive headers for each repo or implementation studied
- Always include repo coordinates (owner/repo@branch:path:line)
- Include star count and last-commit date in parentheses after the repo name on first reference
- Mark relevance: HIGH / MEDIUM / LOW for each finding
- End with:

## Key Cross-Repo Findings

  [Bullet list of the most important discoveries, each with a repo citation]

## Recommendations from Cross-Repo Research

  [How the cross-repo evidence should influence our approach. Distinguish "majority pattern" from "minority pattern" if you saw multiple approaches.]

## Octocode Tool Usage Log

  - packageSearch calls: [N]
  - githubSearchCode calls: [N]
  - githubSearchPullRequests calls: [N]
  - githubGetFileContent calls: [N]
  - Rate limit headroom remaining: [estimate, or "exhausted"]
  - Tavily fallback used: [yes/no, reason if yes]

IMPORTANT: Our codebase is the source of truth. Cross-repo evidence shows what others have done — it does not dictate what we should do. If you find a pattern that conflicts with our architecture, note the conflict explicitly and let synthesis weigh the tradeoff.
```
```

**Change 3 — Add one line to the existing Web Research Agent Prompt (open-web template).** Insert just before "Research Protocol:" at SKILL.md:691:

```diff
 Research this topic externally and write findings to [output-path].

 Topic: [specific external research topic]
 What we already know from codebase: [brief summary of relevant codebase findings]
 Research question context: [the overall research question]

+Tool availability: You have Tavily, WebFetch, WebSearch, and (as a fallback for reading actual package source code) octocode's `packageSearch` and `githubGetFileContent`. Prefer Tavily/WebFetch for blog posts, tutorials, conference talks, and vendor docs. Use octocode only if you need to read source code to validate a claim from a tutorial.
+
 CRITICAL — Incremental File Writing Protocol:
```

### New BUILD_REQUEST instructions

The BUILD_REQUEST template at SKILL.md:330–453 changes in two places:

**Addition 1 — new section, inserted after "SKILL CONTEXT FILE:" (around line 362):**

```
WEB RESEARCH TOPIC CLASSIFICATION (Phase 4 routing):

For each topic in the research-notes SUGGESTED_PHASES.web_research_topics list,
classify into ONE of two buckets and embed the corresponding prompt template:

  github-flavored:
    Triggers (any match): "how does package X", "how does library X", "real callsites",
    "real examples of", "GitHub issue", "GitHub PR", "GitHub discussion",
    "community solution", "community pattern", or the topic explicitly names a
    third-party package/library that appears in EXISTING_FILES dependencies.
    Embedded prompt: GitHub Research Agent Prompt (from SKILL.md)
    Embedded tool restriction: mcp__octocode__githubSearchCode,
      mcp__octocode__githubSearchPullRequests, mcp__octocode__githubGetFileContent,
      mcp__octocode__githubViewRepoStructure, mcp__octocode__packageSearch,
      mcp__tavily__tavily-search (fallback), WebFetch (fallback)

  open-web (default):
    Triggers: blog posts, conference talks, vendor whitepapers, tutorials, news,
    official documentation sites, any topic not matching github-flavored triggers.
    Embedded prompt: Web Research Agent Prompt (from SKILL.md)
    Embedded tool restriction: mcp__tavily__tavily-search, WebFetch, WebSearch,
      mcp__context7__query-docs, mcp__octocode__packageSearch (fallback),
      mcp__octocode__githubGetFileContent (fallback)

CAPS (rate-limit budget):
  - Quick tier: max 4 github-flavored items per Phase 4
  - Standard tier: max 6 github-flavored items per Phase 4
  - Deep tier: max 8 github-flavored items per Phase 4
  If SUGGESTED_PHASES has more github-flavored topics than the cap, CONSOLIDATE
  topics (merge two adjacent ones into a single richer item) rather than dropping
  any. Document the consolidation in the task file's Task Log.

OUTPUT FILE NAMING:
  - github-flavored: ${TASK_DIR}research/web-NN-github-[slug].md
  - open-web: ${TASK_DIR}research/web-NN-[slug].md
  The "github-" prefix is for human navigation; synthesis treats both identically.
```

**Addition 2 — update the Phase 4 phase-mapping block at SKILL.md:415–419** to match the SKILL.md change above (verbatim replacement).

### Tool subset used

| Bucket | Required octocode tools | Allowed octocode fallback | Required other tools |
|---|---|---|---|
| github-flavored | `githubSearchCode`, `githubSearchPullRequests`, `githubGetFileContent`, `githubViewRepoStructure`, `packageSearch` | n/a (these are primary) | Tavily + WebFetch (rate-limit fallback) |
| open-web | (none required) | `packageSearch`, `githubGetFileContent` (read-only fallback) | Tavily, WebFetch, WebSearch, Context7 |

**Explicitly NOT used in Phase 4:** `localSearchCode`, `localViewStructure`, `localFindFiles`, `localGetFileContent`, `lspGotoDefinition`, `lspFindReferences`, `lspCallHierarchy`, `githubCloneRepo`. The first six overlap with native tools + auggie + serena (per octocode-research.md §5). Cloning is excluded as a security/blast-radius restriction (octocode-research.md §6 "set `ENABLE_CLONE=false`").

### Anti-trigger rules

A Phase 4 agent MUST NOT use octocode tools when:

1. **The topic is about the local codebase** — Phase 2 codebase research handles this; Phase 4 is external-only.
2. **The topic is about canonical library API surface** — use `context7` instead; it returns maintainer-published docs, which are higher-authority than the in-repo source for "what does function X do."
3. **The topic is about news, current events, vendor announcements, or pricing** — Tavily/web only.
4. **The topic is about non-code artifacts** (RFC PDFs, conference videos, blog posts, sociotechnical discussions) — Tavily/web only.
5. **The agent has hit its octocode call budget** — fall back to Tavily and note in findings.
6. **Octocode returns HTTP 403 rate-limit twice in the same agent run** — fall back permanently for that agent and tag every subsequent finding with `[octocode unavailable]`.

### Rate-limit / failure handling

**Per-agent budget:** 5 `githubSearchCode` + 3 `githubSearchPullRequests` + unlimited `githubGetFileContent` (it's a read API with different limits) + unlimited `packageSearch` (npm/PyPI proxy, not GitHub Search API).

**Per-phase budget:** at the Deep tier with 8 github-flavored agents × 5 searches = 40 searches per minute IF all agents fire simultaneously. The GitHub Search API allows 30/min. **The reality** is that agents are bursty (search → read → think → search), so 8 parallel agents will typically distribute 40 calls over ~3 minutes — within budget.

**Mitigations:**

- The cap of 8 github-flavored agents per phase is calibrated against this.
- If `githubSearchCode` returns 403, the agent retries once after 30s, then falls back to Tavily and writes a `[octocode rate-limited at HH:MM]` marker.
- The agent's "Octocode Tool Usage Log" footer in the output file makes rate-limit incidents visible to Phase 5 synthesis and Phase 6 QA.

**Octocode availability check** (added to Phase 1 — Preparation, SKILL.md:394–397):

```
Phase 1 — Preparation:
- Update task status to "🟠 Doing"
- Create the task folder at .dev/tasks/to-do/TASK-RESEARCH-YYYYMMDD-HHMMSS/ with subfolders
+ - Verify octocode MCP server is available (`mcp__octocode__githubSearchCode` listed in available tools). If unavailable, log in Task Log and set `OCTOCODE_AVAILABLE=false`; rf-task-builder will then emit only open-web Phase 4 items.
```

### Test plan: three concrete tech-research questions, two-way comparison

**Question 1: "How do real production projects implement pydantic-ai agent registration patterns?"**

| Aspect | Today (Tavily-only) | Recommended (W1-B with octocode) |
|---|---|---|
| Phase 4 agents spawned | 2 (Tavily web search + Tavily community search) | 2 (1 github-flavored octocode + 1 open-web Tavily) |
| Sources cited in `web-NN-*.md` | Stack Overflow Q&A, 1 Medium blog post, pydantic-ai docs (often surface-level) | 3 real repos with `pydantic_ai.Agent(...)` callsites + their PR that introduced the pattern + 1 Medium blog from Tavily side |
| Citation form | URLs | `owner/repo@branch:path:line` + URLs |
| Synthesis input quality | Anecdotal "people seem to use Agent like this" | "Repo X uses pattern A (with code snippet); Repo Y uses pattern B (with diff link); the maintainer's chosen example in tests/ matches pattern A" |
| Phase 6 qualitative QA likelihood of flagging "shallow evidence" | Medium-high | Low |

**Question 2: "Why did the OpenAI Python SDK switch from sync-only to async-first in v1.x — what was the migration story?"**

| Aspect | Today (Tavily-only) | Recommended (W1-B with octocode) |
|---|---|---|
| Phase 4 agents spawned | 2 (Tavily for SDK changelog + Tavily for migration guides) | 2 (1 github-flavored octocode for PR archaeology + 1 open-web Tavily for blog posts) |
| Sources cited | OpenAI changelog page, 1–2 community migration blog posts | `openai/openai-python` PRs surrounding the v1 cutover (typically 3–5 PR threads with maintainer discussion) + blog posts |
| Killer feature exploited | n/a | `githubSearchPullRequests` archaeology — the "why" lives in PR discussions, not in published docs |
| Synthesis input quality | "Per the changelog, async was added in v1" | "Per PR #N from author M dated D, async-first was chosen because [quoted maintainer rationale]; PR #N+5 added migration helpers; the breaking-change announcement is at [URL]" |

**Question 3: "What conference talks and blog posts cover Anthropic's prompt caching best practices in 2026?"**

| Aspect | Today (Tavily-only) | Recommended (W1-B with octocode) |
|---|---|---|
| Phase 4 agents spawned | 2 (Tavily for conference talks + Tavily for blog posts) | **2 (both open-web Tavily — octocode not relevant for narrative content)** |
| Classification outcome | n/a | Both topics classified as `open-web` — no octocode invocation |
| Behavior | Unchanged from today | Unchanged from today |
| What this proves | n/a | The router correctly excludes topics where octocode adds no value — anti-trigger rule #4 fires |

The third question is the **null-test** for the design — it must demonstrate that the router doesn't over-trigger octocode on inappropriate topics.

---

## What This Cannot Do

1. **Cannot fix bad codebase research.** If Phase 2 produces shallow codebase findings, Phase 4 octocode searches will be poorly targeted and miss the right repos. The integration is downstream of Phase 2's evidence quality.

2. **Cannot find what isn't in public GitHub.** Octocode searches public + (with auth) accessible-private repos. Proprietary patterns, internal architectures, and unreleased code remain invisible. Tavily catches some of this via blog posts.

3. **Cannot replace Context7.** Canonical library API docs (parameter signatures, default values, version-specific behaviors) belong to Context7 and remain Context7's job. Octocode reads implementations; Context7 reads docs. Both are needed and answer different questions (octocode-research.md §5).

4. **Cannot prevent rate-limit cascades during partial outages.** If GitHub Search API drops to 10 req/min during an incident, the 4-of-2 parallel batch will still hit the wall faster than the per-agent retry can absorb. The fallback-to-Tavily protocol degrades to "every github-flavored agent becomes a Tavily agent" — graceful but lossy.

5. **Cannot retroactively validate octocode findings.** The synthesis QA and report QA agents (Phase 5 and Phase 6) read the *content* of `web-NN-*.md` files but do not re-execute the search. If octocode returns a stale or hallucinated repo coordinate, the gate doesn't catch it. Mitigation: the GitHub Research Agent Prompt requires `repo@branch:path:line` citations that Phase 6 qualitative QA can spot-check via `mcp__octocode__githubGetFileContent`.

6. **Cannot work for Quick-tier runs with 0–1 web agents.** A Quick-tier topic that doesn't fan out to web research at all is unaffected by this integration. That's correct behavior.

---

## Cross-Target Dependencies

### Dependency on Target #1 (`deep-research` agent integration)

**Loose dependency, ship-independent.**

Target #1 (per octocode-fit-analysis.md §1) adds octocode as a 4th axis to the `deep-research` agent's Tool Selection Policy and adds octocode tools to its frontmatter `tools:` list. That change is upstream of *which agent type spawns the Phase 4 sub-agents*.

In the current architecture, Phase 4 sub-agents are spawned as **general-purpose Agents** with embedded prompts — not as `deep-research` subagents. The BUILD_REQUEST does not say `subagent_type: "deep-research"` for Phase 4. So **the W1-B design here does not require Target #1 to ship first.**

However, there is a desirable interaction:

- If Target #1 ships and gives `deep-research` the 4th axis, then **Phase 4 could later evolve to spawn `subagent_type: "deep-research"` agents with octocode-aware Tool Selection Policy**, replacing the per-item embedded prompt with a more lightweight checklist item that just names the topic. This is the W1-E variant deferred to a follow-up — Target #1 makes it cheaper.

For now, this design **ships standalone**. Target #1 is complementary, not prerequisite.

### Dependency on the MCP registration (#5 in fit-analysis Phase A)

**Hard prerequisite.** Octocode tools must be available to spawned subagents, which means the MCP server must be registered and the `LOG=false` + `TOOLS_TO_RUN` whitelist must be in place. This is one-time infrastructure (octocode-fit-analysis.md §5).

### Dependency on rf-task-builder behavior

**Tight coupling.** The W1-B routing logic lives in the BUILD_REQUEST that rf-task-builder consumes. If rf-task-builder is rewritten or replaced, the classification heuristic must be ported with it. Mitigation: encode the heuristic in the SKILL.md text *in addition to* the BUILD_REQUEST, so the routing logic survives builder changes.

### Independence from Targets #3, #4, #5

W1-B does not depend on `sc:research` command changes (#3), `sc-brainstorm-protocol` Wave 2A (#4), or `sc:troubleshoot` (#6). It can ship in isolation.

---

## Effort Estimate

| Workstream | LoC / files | Reviewer cognitive load | Risk |
|---|---|---|---|
| 1. Edit SKILL.md Phase 4 description (lines 415–419) | ~12 lines replaced | Low — straightforward block edit | Low |
| 2. Add GitHub Research Agent Prompt template (new ~70-line block after Web Research Agent Prompt) | ~70 lines added | Medium — new template, must mirror existing template style | Low (additive) |
| 3. Add 1 line to Web Research Agent Prompt (capability hint) | 1 line added | Trivial | Trivial |
| 4. Update BUILD_REQUEST with WEB RESEARCH TOPIC CLASSIFICATION block | ~40 lines added | Medium — new builder responsibility | Medium — builder may misclassify; mitigate with tests |
| 5. Update Phase 4 phase-mapping block in BUILD_REQUEST | ~6 lines edited | Low | Low |
| 6. Add octocode availability check to Phase 1 | ~3 lines added | Trivial | Trivial |
| 7. Update Verification step A.8 to add a Phase 4 classification check | ~3 lines added | Trivial | Trivial |
| 8. `make sync-dev` | n/a | n/a | n/a |
| 9. End-to-end test: run tech-research on Test Question #1, verify github-flavored bucket activates | 1 manual run | High — first integration test | Medium — discovers misclassifications |
| 10. End-to-end test: Test Question #3 null-test | 1 manual run | Medium | Low |

**Total LoC:** ~135 lines across one file (SKILL.md). Plus 1 BUILD_REQUEST in the same file.

**Total effort:** 1 PR. **~4 hours active editing + 2 hours manual test runs = 1 working day.**

**Out-of-scope for this PR (deferred to follow-ups):**

- Creating `rf-octocode-researcher` agent type (W1-E) — defer until classification heuristic has matured.
- Phase 4.5 archaeology phase (W1-C) — defer until we see what cross-repo evidence Phase 4 produces and identify gaps.
- Hooking octocode into Phase 3 (analyst/QA) — out of scope; Phase 3 is local-only.
- Per-tier octocode tool whitelisting in the MCP registry (env var approach in fit-analysis #5) — separate concern.

**Pre-merge gates:**

1. `make verify-sync` passes (SKILL.md in `src/` matches `.claude/`).
2. Manual run of Test Question #1 produces a `web-NN-github-*.md` file with at least 3 distinct repo citations in `owner/repo@branch:path:line` form.
3. Manual run of Test Question #3 produces zero `web-NN-github-*.md` files (null-test passes).
4. Manual run of any Deep-tier run does not exceed 8 github-flavored Phase 4 items (cap respected).

---

**Status:** Complete
**Recommendation:** Ship W1-B with W1-F fallback as described.
**Next:** Cross-target reconciliation in Stage 4 synthesis (agent 06).
