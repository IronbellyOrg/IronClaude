# Brainstorm 05: Sub-Agent Delegate Integration

## Lens

The four other brainstorms in this fan-out all share a structural assumption: that octocode lives **inside** `deep-research`'s tool surface. That assumption inherits three pathologies from octocode's own design:

1. **The 14-tool context tax** (8–17K tokens, per Stage 1 research §4.4) lands on every `deep-research` invocation regardless of whether the query is "how do React vs Vue solve hydration" (octocode shines) or "what's the current OWASP recommendation for JWT rotation" (octocode irrelevant — pure Tavily/Context7 work). Every consumer of `deep-research` — `tech-research`, `troubleshoot`, `brainstorm`, `tech-reference`, every PR review, every roadmap — pays the tax.
2. **Octocode's failure modes** (Search API 30-req/min cap, telemetry leakage if `LOG` flips, supply-chain compromise of the bgauryy package, MCP STDIO command-injection CVE family) attach themselves directly to the workhorse research agent. A bad day for octocode = a bad day for every research pipeline.
3. **Octocode's mandatory `researchGoal` + `reasoning` fields** (the Research Driven Development discipline) are designed for an LLM that runs *only* octocode tools. Bolting them onto `deep-research`'s Tavily-first protocol forces the parent agent to context-switch between two competing tool philosophies on every call.

**Isolating octocode in a dedicated sub-agent (`github-pattern-researcher`) resolves all three.** The parent `deep-research` agent never loads octocode's schema. The sub-agent's context window is the *only* place octocode tools exist. Failures are bounded — if the sub-agent times out, errors, or rate-limits, the parent receives a structured "I couldn't reach external repos, falling back to Tavily for community-solution lookup" message and continues. The RDD discipline is *inside* the sub-agent's system prompt, where it belongs, and never pollutes the parent's Tavily-first rule.

Structurally this is the same pattern IronClaude already uses for `rf-task-researcher` (the parent `rf-task-builder` delegates codebase exploration to a focused sub-agent instead of doing it inline) and for `auggie-reviewer` (parent commands invoke a specialist for review rather than loading auggie tools globally). Octocode fits the same mold: a narrow, expensive, externally-dependent capability that should be summoned, used, and dismissed — not mounted permanently to the workhorse agent.

The lens this proposal defends: **octocode is a tool with an unusual context-tax profile and a single-maintainer risk profile that makes it a poor candidate for permanent residency in `deep-research`'s tool list. Sub-agent delegation is the architectural pattern designed exactly for this trade-off.**

---

## New Agent Definition

Full proposed content of `src/superclaude/agents/github-pattern-researcher.md`:

````markdown
---
name: github-pattern-researcher
description: Cross-repository GitHub/GitLab/Bitbucket pattern research specialist. Uses octocode MCP to investigate how real projects implement a given concept, archaeology of merged PRs, and package-to-source resolution. Read-only across code hosts. Delegated to by deep-research, tech-research, sc-brainstorm, sc-troubleshoot, and tech-reference when the question requires external-repo evidence (not local code, not canonical docs, not general web).
category: research
memory: project
tools:
  - mcp__octocode__githubSearchCode
  - mcp__octocode__githubSearchRepositories
  - mcp__octocode__githubSearchPullRequests
  - mcp__octocode__githubGetFileContent
  - mcp__octocode__githubViewRepoStructure
  - mcp__octocode__packageSearch
  - Read
  - Write
  - mcp__sequential-thinking__sequentialthinking
---

# GitHub Pattern Researcher

You are a narrow-scope specialist. Your ONLY job is to answer cross-repository GitHub/GitLab/Bitbucket research questions using the octocode MCP server. You do not answer local-codebase questions, canonical-docs questions, or general-web questions — those belong to auggie, Context7, and Tavily respectively. You receive a structured query from a parent agent and return a structured evidence pack.

## Scope Discipline (HARD BOUNDARIES)

You **WILL** handle:

- "How do real production projects implement X?" (cross-repo pattern discovery)
- "What does package Y actually do, at the source-code level?" (package → repo resolution → targeted reads)
- "Why was decision Z made in project P?" (PR archaeology — search PR titles, bodies, diffs)
- "Show me 3+ concrete callsites of API Q in the wild" (usage examples)
- "How do other projects solve error pattern E?" (cross-repo problem-solution mapping)

You **WILL NOT** handle:

- Local-codebase exploration → return `OUT_OF_SCOPE: use auggie or serena`
- Canonical library docs lookups → return `OUT_OF_SCOPE: use Context7`
- General web search (blog posts, articles, conference talks) → return `OUT_OF_SCOPE: use Tavily`
- Writing or modifying source code → you are read-only

If the parent's query is ambiguous between scopes, return `CLARIFY_NEEDED:` with a specific question. Never guess scope.

## Operating Discipline

### The Funnel Method (mandatory)

Octocode's design enforces a DISCOVER → SEARCH → LOCATE → READ flow. You **must** follow it:

1. **DISCOVER** — `packageSearch` (if starting from a package name) or `githubSearchRepositories` (if starting from a concept). Output: a small set of candidate repos.
2. **SEARCH** — `githubSearchCode` and/or `githubSearchPullRequests` within those candidates. Output: file paths + line hints + PR numbers.
3. **LOCATE** — `githubViewRepoStructure` to understand context around the hits.
4. **READ** — `githubGetFileContent` with `charOffset` / `charLength` for targeted extraction. **Never** read full files when partial reads suffice.

Skipping the funnel (e.g., calling `githubGetFileContent` first without a search step) is a protocol violation.

### Research Driven Development discipline

Every octocode tool call requires a `researchGoal` and `reasoning` field. Treat these as mandatory thinking artifacts, not bureaucracy. The `researchGoal` should be a one-sentence statement of what you're trying to learn from this specific call. The `reasoning` should justify why this tool with these parameters is the right next step given prior results. If you cannot articulate both, do not make the call.

### Token discipline

- Always set `verbosity: "compact"` unless the parent explicitly requests verbose results.
- Use `charOffset` + `charLength` for partial file reads. A 200-line file fetched in full when 20 lines suffice is waste.
- Auto-truncate PR bodies — accept octocode's default truncation at `limit ≥ 4`.
- Cap evidence pack at **5 cited examples per claim**. More is not better.

### Rate-limit awareness

GitHub Search API limit is 30 requests/minute. Octocode's bulk-parallel pattern can exhaust this fast.

- Hard cap: **20 octocode tool calls per delegation**. If you need more, return `PARTIAL: hit call cap` with what you have.
- Sequence search calls; do not fan out >3 in parallel.
- If you receive a 403 from the Search API, immediately stop searching and return `RATE_LIMITED: <calls_used>` with whatever evidence you've gathered.

### Failure modes (return these structured codes)

| Code | When | Parent's next move |
|---|---|---|
| `OUT_OF_SCOPE: <reason>` | Query is not a cross-repo question | Parent uses Tavily/Context7/auggie |
| `CLARIFY_NEEDED: <question>` | Query is ambiguous | Parent re-asks the user or refines payload |
| `RATE_LIMITED: <calls_used>` | 403 from GitHub Search | Parent retries later or falls back to Tavily for community examples |
| `NO_EVIDENCE: <searched>` | Funnel ran clean but found nothing | Parent reports null result honestly |
| `PARTIAL: <reason>` | Hit call cap or timed out mid-search | Parent uses what's returned + decides whether to re-delegate |
| `OCTOCODE_UNAVAILABLE` | MCP server not loaded / connection failed | Parent falls back to Tavily for community examples |

## Input Contract (from parent agent)

The parent agent (typically `deep-research`) sends a structured payload:

```yaml
DELEGATION:
  research_question: "<one-sentence question — must be cross-repo in nature>"
  scope_hint: "<package | concept | error_pattern | api_usage | pr_archaeology>"
  candidate_repos: ["owner/repo", ...]   # optional, may be empty
  candidate_packages: ["pkg-name", ...]  # optional, may be empty
  max_evidence: 5                         # default 5, cap at 10
  verbosity: "compact" | "verbose"        # default compact
  parent_context: "<short paragraph — why is parent asking this>"
```

If `candidate_repos` and `candidate_packages` are both empty, your first action is `githubSearchRepositories` or `packageSearch` (the DISCOVER step).

## Output Contract (back to parent)

Return a single Markdown document with this structure:

````markdown
## GitHub Pattern Research Result

**Question:** <verbatim from input>
**Status:** OK | PARTIAL | NO_EVIDENCE | OUT_OF_SCOPE | RATE_LIMITED | OCTOCODE_UNAVAILABLE
**Calls used:** <N> / 20
**Repos investigated:** ["owner/repo", ...]

### Evidence

#### 1. <one-line claim>
- **Repo:** `owner/repo` @ branch
- **File:** `path/to/file.ext` (lines A–B)
- **PR (if archaeology):** #N "title" (merged YYYY-MM-DD)
- **Why this is evidence:** <one sentence>
- **Excerpt:**
  ```<lang>
  <minimal code excerpt, ≤20 lines>
  ```
- **Permalink:** github.com/owner/repo/blob/<sha>/path#LA-LB

#### 2. ...
(up to `max_evidence` items)

### Pattern Synthesis (if ≥3 evidence items)

<2–4 sentence synthesis: what's common across the examples, what varies>

### Open Questions / Gaps

- <anything the funnel did NOT resolve>
- <known unknowns that warrant further research>

### Provenance

| Tool call | researchGoal | result-size | hit/miss |
|---|---|---|---|
| `packageSearch(httpx)` | resolve package to source repo | 1 hit | hit |
| `githubSearchCode(repo=encode/httpx, query=...)` | locate retry logic | 4 hits | hit |
| ... | ... | ... | ... |
````

## What This Sub-Agent Does NOT Do

- Does NOT call Tavily, WebSearch, WebFetch, or Context7. If those are needed, return `OUT_OF_SCOPE` so the parent can route correctly.
- Does NOT read local files outside what's required to understand the input payload itself. Local-code questions belong to auggie/serena.
- Does NOT cache results across delegations. Each invocation is stateless from the parent's perspective. (Octocode itself maintains a 24h disk cache at `~/.octocode/repos/` — that's transparent infrastructure, not stateful agent memory.)
- Does NOT make recommendations or judgments about the patterns it finds. It reports evidence; the parent agent synthesizes.
- Does NOT write to GitHub. Octocode is read-only and this agent is read-only.

## Telemetry / Privacy Note

The octocode server, by default, sends repo names + research goals to its telemetry endpoint. The MCP install path **must** set `LOG=false` (enforced at `install_mcp.py`). This sub-agent's prompt does NOT need to enforce that — it's a server-config concern. But: if you observe that telemetry is leaking sensitive repo names (e.g., names mentioning private internal services), return `OCTOCODE_UNAVAILABLE: telemetry-suspected-on` and let the parent escalate.

## Critical Rules

1. **Stay in scope.** If the question isn't cross-repo, return `OUT_OF_SCOPE` immediately. Do not "be helpful" by reaching for Tavily — that's the parent's job.
2. **Follow the funnel.** DISCOVER → SEARCH → LOCATE → READ. Never invert the order.
3. **Cap calls at 20.** Hard limit. If you hit it, return `PARTIAL`.
4. **Cite everything.** Every claim needs a `owner/repo@sha:path#L-L` style citation. No paraphrasing without source.
5. **Compact by default.** Verbose mode is opt-in by the parent.
6. **No synthesis without evidence.** If you have <3 evidence items, do not produce a Pattern Synthesis section.
7. **Report what you DON'T find.** `NO_EVIDENCE` is a legitimate, valuable result. Do not hallucinate patterns to fill a quota.
````

(End of `src/superclaude/agents/github-pattern-researcher.md`.)

---

## Delegation Pattern in deep-research

### What triggers delegation

Add to `src/superclaude/agents/deep-research.md` Tool Selection Policy a **new section** between current §"Library docs" and §"Detecting Tavily unavailable":

````markdown
### Axis 4: Cross-repo GitHub pattern research (delegated)

The `deep-research` agent does NOT call octocode tools directly. Cross-repo GitHub research is delegated to the `github-pattern-researcher` sub-agent via the `Task` tool.

**Delegate to `github-pattern-researcher` when ALL of the following hold:**

1. The research question is about how **real projects** implement, decide, or use a thing — not about a canonical spec (Context7) or a current blog post (Tavily) or local code (auggie).
2. The question has at least one of these shapes:
   - "How does package X actually implement Y?"
   - "Show me production examples of API Z in use."
   - "Why did project P make change C?" (PR archaeology)
   - "How do projects A, B, C compare on approach D?"
   - "What does package X (from npm/PyPI) actually do at source level?"
3. The answer requires **first-party source evidence**, not third-party commentary.

**Do NOT delegate** (handle with existing axes):

- Library docs and canonical API references → Context7
- Best-practices articles, blog posts, conference talks, StackOverflow → Tavily
- Local codebase exploration → auggie (in the calling skill, not deep-research)

**Delegation payload (Task tool subagent_type: `github-pattern-researcher`):**

```yaml
DELEGATION:
  research_question: "<verbatim user-facing question>"
  scope_hint: <one of: package | concept | error_pattern | api_usage | pr_archaeology>
  candidate_repos: []          # populate if known, else let sub-agent discover
  candidate_packages: []
  max_evidence: 5
  verbosity: compact
  parent_context: |
    The user (or upstream skill) is researching <topic>. This delegation is
    one axis of a broader research pass; results will be merged with Tavily
    and Context7 findings.
```

**Receiving the result:**

The sub-agent returns a structured Markdown evidence pack. Treat its top-level `Status:` field as authoritative:

| Status | Action |
|---|---|
| `OK` | Merge the evidence section into your research report under "Cross-repo evidence". Cite per-item. |
| `PARTIAL` | Merge what's returned; note in Open Questions that the cross-repo pass was incomplete. |
| `NO_EVIDENCE` | Note explicitly in the report that cross-repo search found nothing. Do not silently drop. |
| `OUT_OF_SCOPE` | Re-route the question to Tavily or Context7. Do NOT re-delegate with the same payload. |
| `RATE_LIMITED` | Fall back to Tavily for the "how do other projects" portion of the question. Note in Open Questions. |
| `OCTOCODE_UNAVAILABLE` | Fall back to Tavily for the "how do other projects" portion. Note in Open Questions. |
| `CLARIFY_NEEDED` | Refine the payload using the sub-agent's question. Re-delegate at most once. |

**Provenance:** When you merge sub-agent results into your final report, attribute them as `backend=octocode (via github-pattern-researcher)` in the Sources table. Never present cross-repo findings without that attribution.
````

### Concrete delegation example (operational)

When `deep-research` receives a query like:

> "What's the current best-practice implementation of retry logic for HTTP clients in Python?"

The agent's planning step (workflow §2) identifies three axes:

1. **Tavily** — blog posts, articles on retry best practices in 2026
2. **Context7** — canonical docs for `httpx`, `tenacity`, `urllib3`
3. **github-pattern-researcher** — actual source-code patterns in the top retry libraries

The deep-research agent fires all three in parallel (one `Task` tool call to the sub-agent + two direct MCP calls), waits for all three to return, and synthesizes. The sub-agent payload looks like:

```yaml
DELEGATION:
  research_question: "How do production-grade HTTP clients in Python implement retry logic with exponential backoff?"
  scope_hint: api_usage
  candidate_repos: []
  candidate_packages: ["httpx", "tenacity", "urllib3", "requests"]
  max_evidence: 5
  verbosity: compact
  parent_context: |
    User is researching retry logic for a new HTTP client. They want
    real-world patterns from production-grade libraries, not blog posts.
    Tavily + Context7 are handling docs/articles in parallel.
```

The sub-agent runs its funnel: `packageSearch` on each package → `githubViewRepoStructure` on the matched repos → `githubSearchCode("retry|backoff", repo=encode/httpx)` etc. → `githubGetFileContent` with line-hints → assembles evidence pack → returns. Total: ~8–12 octocode calls, well under the 20-call cap.

---

## Parent-Child Interface

### What the parent sends

A single `DELEGATION:` YAML block (shown above). All fields are typed; `candidate_*` lists may be empty (sub-agent discovers); `max_evidence` and `verbosity` have defaults.

### What the sub-agent returns

A single Markdown document with the structure shown in the agent's Output Contract section. Parsable by simple regex (`^## ... Result`, `^**Status:**`, `^### Evidence`) or treated as opaque text the parent inlines into its synthesis.

### Structured output schema (for programmatic consumers)

For CLI pipelines that want machine-readable output, the sub-agent additionally writes a side-car JSON file when invoked with `verbosity: verbose`:

```json
{
  "status": "OK | PARTIAL | NO_EVIDENCE | OUT_OF_SCOPE | RATE_LIMITED | OCTOCODE_UNAVAILABLE | CLARIFY_NEEDED",
  "question": "<verbatim>",
  "calls_used": 12,
  "calls_cap": 20,
  "repos_investigated": ["encode/httpx", "jd/tenacity"],
  "evidence": [
    {
      "claim": "httpx uses tenacity-style stop-after-attempt strategy",
      "repo": "encode/httpx",
      "ref": "abc123def",
      "path": "httpx/_transports/retry.py",
      "lines": [42, 78],
      "permalink": "https://github.com/encode/httpx/blob/abc123/httpx/_transports/retry.py#L42-L78",
      "excerpt": "...",
      "why": "Canonical implementation in a widely-used HTTP client."
    }
  ],
  "synthesis": "All three production libraries (httpx, tenacity, urllib3) ...",
  "gaps": ["No evidence found for jitter strategies."],
  "provenance": [
    {"tool": "packageSearch", "args": {"query": "httpx"}, "researchGoal": "...", "hits": 1}
  ]
}
```

This JSON contract is **the actual interoperability surface** — the Markdown is for human consumption when a parent agent dumps the result into a report.

### Statelessness

Each delegation is stateless from the parent's perspective. The sub-agent's `memory: project` directive only allows it to accumulate **internal** notes about its own behavior (e.g., "this repo's main branch is `master` not `main`"). It does NOT persist user-facing research findings across delegations — that's the parent's job.

---

## Reusability

The whole point of factoring octocode into a sub-agent is reuse. Consumers:

| Consumer | How it uses `github-pattern-researcher` |
|---|---|
| **`deep-research` agent** | Axis 4 of Tool Selection Policy (described above). Primary consumer. |
| **`tech-research` skill** (Phase 4 Web Research) | Spawns a `github-pattern-researcher` agent per investigation that has a cross-repo dimension. Replaces 2-4 Tavily searches per investigation with first-party source evidence. (Stage 1 §3.1 R2/R5 archetypes.) |
| **`sc-brainstorm-protocol` skill** (Wave 2A enrichment) | When `domain ∈ {code, architecture}`, fan out a `github-pattern-researcher` delegation in parallel with auggie enrichment, asking "how have similar projects solved this?" Pure-add to the routing matrix; no octocode tools loaded in the brainstorm orchestrator itself. |
| **`sc-troubleshoot-protocol` skill** (Tier 2 hypothesis agents) | When the error signature looks generic (e.g., stack-trace text patterns), one of the parallel hypothesis agents delegates to `github-pattern-researcher` asking "find issues + PRs with this signature in any public repo." |
| **`tech-reference` skill** | When documenting a feature that has known external precedents, delegate to find 2-3 cross-repo implementations of the same pattern for the "Prior Art" section. |
| **`sc-auggie-review-protocol` skill** | When reviewing a PR that introduces a new pattern, delegate to find similar patterns in other repos for "is this the standard way?" check. |
| **`sc-roadmap-protocol` skill** (Wave 1B reference-roadmap discovery) | For novel domains, delegate to find reference roadmaps in similar projects. (Stage 1 fit-analysis target #7.) |

That's **seven consumers** sharing one sub-agent. Each consumer pays the octocode context tax (~8K tokens) only when it actually delegates, not on every invocation. If a `deep-research` query never triggers cross-repo work, octocode tools never load into any agent's context that session.

This is precisely the multiplier effect described in fit-analysis §1: a single change propagates to all downstream consumers — but with the additional property that **the propagation is opt-in per query**, not blanket-loaded into every agent.

---

## Context Tax Analysis

### Baseline (no octocode)

`deep-research` currently loads ~10 tools: `mcp__tavily__*` (2), `WebSearch`, `WebFetch`, `mcp__context7__*` (2), `Read`, `Grep`, `Glob`, `mcp__sequential-thinking__*` (1). Per Stage 1 estimate, that's roughly 6–8K tokens of tool schemas at session start.

### Naïve integration (Brainstorms 01–04 territory)

Adding octocode's 5 cross-repo tools directly to `deep-research.md` frontmatter:

- Tool schemas: +5 octocode tools × ~600–1200 tokens each ≈ **+3,000–6,000 tokens** loaded for **every** `deep-research` invocation, including the many that never need cross-repo evidence.
- Parent prompt expansion: Tool Selection Policy gains a 4th axis with full description of when to use vs. when not (~200 tokens) — that's unavoidable.

Total: **+3,200–6,200 tokens × every invocation**.

### Sub-agent delegate (this proposal)

- `deep-research.md` frontmatter: unchanged tool list. **+0 tokens** of octocode schemas.
- `deep-research.md` Tool Selection Policy: gains Axis 4 description (~250 tokens — slightly larger than naïve because it documents the delegation payload format).
- `github-pattern-researcher.md` agent file: ~5,500 tokens (frontmatter + body). This file is only loaded **when delegation fires** via the `Task` tool, not at session start.

Cost breakdown per invocation type:

| Query type | Naïve cost | Sub-agent cost | Savings |
|---|---|---|---|
| Pure Tavily query | +3,200–6,200 (wasted) | +250 (Policy text only) | **2,950–5,950** |
| Pure Context7 query | +3,200–6,200 (wasted) | +250 | **2,950–5,950** |
| Cross-repo delegation | +3,200–6,200 + tool-call tokens | +250 + ~5,500 (sub-agent load) + tool-call tokens | **−2,300 to +700** (mild net cost on hot path) |
| Mixed (Tavily + cross-repo) | +3,200–6,200 + tool-call tokens | +250 + ~5,500 + tool-call tokens | **−2,300 to +700** |

**The sub-agent costs slightly more on the cross-repo-query hot path but saves dramatically on every non-cross-repo query.** Given that fit-analysis Stage 2 estimates only ~20–30% of `deep-research` queries are genuinely cross-repo, the expected-value math favors the sub-agent strongly:

- Expected cost (naïve) = (1.0) × 4,700 = **4,700 tokens/invocation average**
- Expected cost (sub-agent) = (0.25 × 5,500 + 0.75 × 0) + 250 = **1,625 tokens/invocation average**

**~3,000-token savings per invocation, averaged across query mix.** Over a session with 20 research calls, that's ~60K tokens saved.

### Bonus: blast-radius reduction

Naïve approach: a bad octocode response (rate limit, hallucinated repo, MCP server crash) can corrupt the synthesis of any `deep-research` call. Sub-agent approach: the parent receives a clean `RATE_LIMITED` or `OCTOCODE_UNAVAILABLE` status and falls back gracefully without ever having octocode's schemas pollute its context.

---

## Pros

1. **Context tax isolation.** Octocode's 14-tool schema burden lives in one agent file, loaded only when actually used. Pure-Tavily queries pay zero octocode cost. (~3K tokens average savings per `deep-research` invocation, per the math above.)
2. **Failure isolation.** Octocode supply-chain compromise, rate limits, telemetry issues, MCP STDIO CVE family — all bounded to the sub-agent. Parent has structured recovery codes. The "bus factor = 1 maintainer" risk (Stage 1 §4.1) becomes a sub-agent-level risk, not a research-pipeline-wide risk.
3. **Reusability across 7 consumers.** One sub-agent serves `deep-research`, `tech-research`, `troubleshoot`, `brainstorm`, `tech-reference`, `auggie-review`, `roadmap` — without duplicating octocode tool configuration in each consumer.
4. **Scope discipline enforcement.** The sub-agent's hard-bounded scope ("only cross-repo questions") makes it physically impossible to misuse octocode for local-codebase or canonical-docs questions — exactly the overlap risks flagged in Stage 1 §5.
5. **RDD discipline lives where it makes sense.** Octocode's mandatory `researchGoal`/`reasoning` discipline (a major design feature) is enforced in the sub-agent's prompt instead of polluting the parent agent's Tavily-first protocol.
6. **Funnel method enforcement.** The sub-agent's prompt encodes the DISCOVER → SEARCH → LOCATE → READ flow as a hard rule. Parent agents using octocode directly may skip the funnel and produce expensive, unfocused queries.
7. **Structured output contract.** The Markdown + JSON output schema makes results consumable by both LLM parents and CLI pipelines without reparsing.
8. **Reversible adoption.** Removing octocode = deleting one agent file + reverting Axis 4 of Tool Selection Policy. Nothing else in the framework needs to change. Naïve integration scatters octocode references across many files.
9. **Rate-limit budgeting at sub-agent boundary.** The 20-call cap per delegation prevents one rogue query from exhausting the 30-req/min Search API budget for everyone else.
10. **Telemetry containment.** If the `LOG=false` config slips, the sub-agent boundary makes it easier to audit which delegations leaked which repo names — there's a clear log line per delegation rather than a diffuse trace through every `deep-research` call.

---

## Cons

1. **Sub-agent latency.** Each delegation incurs a `Task` tool call setup cost (~1-2s) plus the sub-agent's own planning overhead (~1-3s before the first octocode call). For a query needing only 2-3 octocode calls, the overhead is proportionally large. Estimated overhead: **+3-5s per delegation** vs. direct in-parent calls.
2. **Context-double-pay on hot path.** When the query genuinely needs cross-repo work, the parent loads its tools AND the sub-agent's context loads octocode. Total tokens slightly higher (~700 worst case) than naïve on the hot path. The math only wins on aggregate because non-hot-path queries dominate.
3. **One more file to maintain.** Adding `github-pattern-researcher.md` increases the agent file count from 40 → 41. Versus naïve which edits one existing file.
4. **Parent-child interface drift risk.** If the delegation payload schema or output schema evolves and consumers aren't updated in lockstep, results may parse partially or be misattributed. Requires versioned schema discipline.
5. **Loss of fine-grained tool-mix control in parent.** A parent agent that wants to interleave one octocode call with three Tavily calls in a tight feedback loop pays the delegation overhead per round-trip. Workarounds: parent batches all cross-repo work into one delegation per pass.
6. **Debugging indirection.** When a research result looks wrong, the operator now has two contexts to inspect (parent's reasoning + sub-agent's reasoning). Adds one hop to root-cause analysis.
7. **The "fall back to Tavily" path needs explicit testing.** If `OCTOCODE_UNAVAILABLE` returns and the parent's fallback logic is buggy, the user sees no error, just degraded results. Easy to miss in QA.
8. **Sub-agent has no access to the parent's working memory.** If the parent has already discovered "the user is investigating httpx" through earlier turns, the sub-agent only knows what the `parent_context` field tells it. Brevity in that field can lead to off-target results.
9. **Cannot use octocode for cross-cutting hooks.** The PostToolUse-hook integration mentioned in Stage 1 §6 target #5 (fire octocode in parallel with auggie on local searches) is structurally incompatible with this approach — hooks can't easily delegate to sub-agents.

---

## What This Approach Cannot Do

- **Cannot make octocode tools available to direct user invocation.** If a user explicitly types "use octocode to search for X," the parent agent must still understand the delegation pattern; the tools are not directly callable from any non-sub-agent context. (Mitigation: this is a feature for safety reasons, but operators wanting raw octocode access need to know about the sub-agent.)
- **Cannot share an in-flight octocode session across multiple parent calls.** Each delegation is stateless. If `deep-research` makes three sequential research passes in one turn, each pass that needs cross-repo work spins up a fresh sub-agent context (the 24h octocode-server disk cache helps amortize the cost, but the agent-level context is fresh each time).
- **Cannot opportunistically use octocode mid-Tavily-search.** The parent decides axis routing up front in its planning step. A Tavily result that reveals "this is actually a cross-repo question" requires the parent to issue a new delegation, not seamlessly switch.
- **Cannot integrate at the hook level.** PostToolUse hooks can't invoke sub-agents practically. Integrations that need hook-level octocode firing (Stage 1 §6 target #5) need a different approach.
- **Cannot help with octocode's local + LSP tool features.** This sub-agent intentionally excludes `local*` and `lsp*` octocode tools because they overlap with auggie + serena. Operators wanting those tools would need a separate agent (which fit-analysis §5 explicitly recommends against).

---

## Specific Risk Mitigations

| Stage 1 risk | This proposal's mitigation |
|---|---|
| **Supply-chain / `@latest` pattern (§4.1)** | Sub-agent's prompt does not mention `@latest`; install path pins `octocode-mcp@14.2.0`. Sub-agent boundary means a poisoned octocode update affects only the sub-agent's execution, not the parent's planning. |
| **Bus factor = 1 maintainer (§4.1)** | Easy removal path: delete one agent file. Parent agent has structured `OCTOCODE_UNAVAILABLE` fallback to Tavily. If bgauryy stops maintaining octocode, the sub-agent can be deprecated atomically. |
| **MCP STDIO command-injection family (§4.1)** | Sub-agent's process is the only context where the vulnerable transport runs for research queries. Compromise scope is bounded to one sub-agent invocation, not every deep-research call. |
| **Telemetry leakage (`LOG=false`, §4.2)** | Sub-agent prompt explicitly flags telemetry concern; per-delegation auditing surface for operators. If a sensitive repo name appears in telemetry, the offending delegation is identifiable from the provenance table. |
| **Search API rate limits (§4.3)** | Hard 20-call cap per delegation, hard 3-parallel cap. `RATE_LIMITED` structured response triggers parent's Tavily fallback. The cap also prevents one runaway delegation from starving other concurrent research workflows. |
| **Context tax (§4.4)** | Tax paid only on delegation, not on every `deep-research` invocation. Expected ~3K tokens saved per average invocation (math in §Context Tax Analysis). |
| **LSP language gaps (§4.5)** | This sub-agent doesn't use LSP tools at all — serena covers symbol nav. Risk eliminated. |
| **Limited community validation (§4.6)** | Bounded blast radius: if octocode's behavior turns out to be subtly wrong, only cross-repo evidence is affected. Tavily/Context7/auggie paths remain pristine. |
| **Overlap with auggie + serena + Read (§5)** | Sub-agent's "OUT_OF_SCOPE" returns for non-cross-repo questions force correct routing. The 14-tool octocode surface is reduced to 5 cross-repo-only tools in the sub-agent's frontmatter. |
| **Skills marketplace duplication (§6 "Strong NO")** | Sub-agent does NOT use any octocode skill. Its prompt encodes the funnel directly, not via `octocode-research` skill import. No risk of two competing skill ontologies. |

---

## Test Plan

### Unit-level (agent contract)

1. **Scope discipline** — Send the sub-agent 10 queries: 5 in-scope cross-repo questions, 5 out-of-scope (local code, canonical docs, web search). Expected: 5 `OK`/`PARTIAL`/`NO_EVIDENCE` and 5 `OUT_OF_SCOPE` results. Any false positive (sub-agent attempts to handle an out-of-scope query) is a P0 prompt bug.
2. **Funnel discipline** — Inspect provenance tables across 10 invocations. Expected: every invocation starts with `packageSearch` or `githubSearchRepositories` or has explicit `candidate_repos` from input. Any invocation starting with `githubGetFileContent` is a protocol violation.
3. **Call-cap enforcement** — Construct a query that would naturally require >20 calls (e.g., "compare retry logic across 30 HTTP libraries"). Expected: `PARTIAL: hit call cap` with ≤20 calls used.
4. **Citation completeness** — For every evidence item, verify `permalink` + `repo` + `path` + `lines` all present and parseable.

### Integration-level (parent ↔ sub-agent)

5. **`deep-research` delegation routing** — Issue 10 research questions to `deep-research`; check that the cross-repo subset triggers `Task` calls to `github-pattern-researcher` and the rest don't. Check that delegation payloads are well-formed YAML matching the input contract.
6. **`OCTOCODE_UNAVAILABLE` fallback** — Disable the octocode MCP server. Issue a cross-repo query. Expected: sub-agent returns `OCTOCODE_UNAVAILABLE`; parent falls back to Tavily for the cross-repo portion and clearly notes the fallback in its final report.
7. **`RATE_LIMITED` fallback** — Pre-exhaust the GitHub Search API budget by external script. Issue a cross-repo query. Expected: sub-agent returns `RATE_LIMITED`; parent falls back and notes in Open Questions.
8. **Parallel delegation** — Issue a mixed query that triggers Tavily + Context7 + sub-agent delegation in parallel. Expected: all three complete; results merge correctly into final report with backend attribution.

### Reusability validation

9. **Multi-consumer test** — Invoke `tech-research`, `sc-brainstorm`, and `sc-troubleshoot` skills each with a question that triggers cross-repo lookup. Verify all three successfully delegate to `github-pattern-researcher` without code duplication or per-consumer config drift.

### Context-tax measurement

10. **Token-cost A/B** — Run 50 representative `deep-research` queries under both naïve (octocode tools in parent) and sub-agent designs. Measure: total input tokens per query, total output tokens per query, octocode calls per query, wall-clock time per query. Validate the expected-value model (~3K tokens saved average).

### Security / privacy

11. **Telemetry audit** — With `LOG=true` temporarily (in a non-production env), issue 20 cross-repo queries with synthetic sensitive-repo-name queries. Confirm the telemetry endpoint sees only the queries we expect, then set `LOG=false` and re-confirm no telemetry fires.
12. **Supply-chain version pin** — Verify `install_mcp.py` pins `octocode-mcp@14.2.0` (or current pinned version) and that `npx -y octocode-mcp@latest` is **not** invokable anywhere in the codebase.

### Edge cases

13. **Empty result handling** — Query for an intentionally obscure pattern. Expected: `NO_EVIDENCE` with the provenance table showing the searches attempted, not a hallucinated "I found nothing but here's a plausible-sounding paragraph anyway."
14. **Ambiguous scope** — Send a question that could be either local or cross-repo. Expected: `CLARIFY_NEEDED` with a specific question, not a guess.
15. **Multi-language LSP fallback non-claim** — The sub-agent does not load LSP tools. Send a query that would tempt LSP use ("what's the call graph for this function in repo X"). Expected: sub-agent uses `githubSearchCode` for callsites rather than claiming structural call-hierarchy data it can't actually produce.

---

## Effort Estimate

| Work item | Effort | Risk |
|---|---|---|
| Write `src/superclaude/agents/github-pattern-researcher.md` (this proposal as starting point) | 3-4 hrs | Low — content largely drafted above |
| Update `src/superclaude/agents/deep-research.md` Tool Selection Policy (add Axis 4) | 1-2 hrs | Low — declarative edit |
| Update `src/superclaude/cli/install_mcp.py` to register octocode MCP (pinned to v14.2.0, `LOG=false`, tools whitelist) | 1 hr | Low — single dict entry |
| Update `src/superclaude/skills/tech-research/SKILL.md` Phase 4 to use the sub-agent | 2 hrs | Med — interplay with Phase 4 agent-prompt template needs care |
| Update `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` Wave 2A enrichment matrix | 1 hr | Low — additive routing rule |
| `make sync-dev` + `make verify-sync` | 5 min | Low — mechanical |
| Update CLAUDE.md if needed (reference to new agent) | 0.5 hr | Low |
| Test plan unit/integration tests (items 1-15) | 6-8 hrs | Med — test fixtures for MCP unavailable/rate-limited scenarios need setup |
| Token-cost A/B measurement (item 10) | 2 hrs | Low — straightforward instrumentation |
| Documentation: `docs/user-guide/octocode-research.md` mentioning the delegation pattern | 1-2 hrs | Low |

**Total estimate: ~17-22 engineering hours (2-3 working days for one engineer).** Highest-confidence subset (just agent file + deep-research Axis 4 + MCP registration + basic unit tests) is **8-10 hours** — could ship as a minimum viable adoption in 1 working day, with skill-level integrations as follow-up PRs.

**Sequencing recommendation:**

- PR 1 (foundational, ~8 hrs): MCP registration + `github-pattern-researcher.md` + `deep-research.md` Axis 4 + unit tests 1-4 + integration test 5
- PR 2 (highest-leverage skill consumer, ~4 hrs): `tech-research` Phase 4 + integration test 9
- PR 3 (enrichment, ~3 hrs): `sc-brainstorm-protocol` Wave 2A + final A/B test + docs
- PR 4 (security & fallbacks, ~3 hrs): tests 6, 7, 11, 12 + production-readiness review

This phased rollout matches the highest-ROI integration path in fit-analysis §"Highest-ROI Integration Path" but threads octocode through a sub-agent boundary at every stop.
