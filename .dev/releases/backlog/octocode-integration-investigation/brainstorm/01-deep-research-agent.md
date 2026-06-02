# Brainstorm — Target #1: deep-research Agent

**Date:** 2026-05-30
**Agent:** Brainstorm #1 of 5 (parallel `/sc:brainstorm`)
**Target file:** `src/superclaude/agents/deep-research.md`
**Task:** Cast a wide net, then converge on the most beneficial way to integrate octocode into the `deep-research` agent.

---

## Target Context

### What `deep-research` is today

`deep-research` is the **workhorse external-knowledge agent** for the SuperClaude framework. It is invoked (directly or transitively) by:

- `tech-research` skill (Phase 4 spawns N parallel deep-research agents)
- `tech-reference` skill (when an existing feature needs external context)
- `sc-troubleshoot-protocol` (for prior-art lookups on errors)
- `sc-brainstorm-protocol` Wave 2A (one of the enrichment paths)
- `sc:research` command (direct front-door)
- `rf-task-builder` and `task-builder` (sometimes, for unfamiliar deps)

The current frontmatter (`deep-research.md:1–16`):

```yaml
name: deep-research
description: Adaptive research specialist for external knowledge gathering. Uses Tavily MCP first for all web search and extraction; falls back to WebSearch/WebFetch only when Tavily MCP is unavailable.
category: analysis
tools:
  - mcp__tavily__tavily-search
  - mcp__tavily__tavily-extract
  - WebSearch
  - WebFetch
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
  - Read
  - Grep
  - Glob
  - mcp__sequential-thinking__sequentialthinking
```

The body (lines 30–51) defines a **Tool Selection Policy** structured as three axes:

| Axis | Primary | Fallback | Used for |
|---|---|---|---|
| Web | Tavily MCP | WebSearch / WebFetch | General web pages, blogs, HN, Reddit |
| Library docs | Context7 | (none — Tavily for unofficial) | Maintainer-published API docs |
| Synthesis | Sequential | (n/a) | Multi-step reasoning across findings |

The "Tavily-first rule" (lines 32–47) is **explicit and prescriptive**: defines what counts as "unavailable," requires `fallback_reason` annotation in the source table, forbids silent fallback. This rigor is the file's distinctive design feature — it's not just a tool list, it's a **routing policy**.

The output contract (lines 60–66) requires a sources table with a `backend` column: `[tavily|websearch|webfetch|context7]` — so any new tool family must declare itself in that taxonomy.

### What `deep-research` is missing

The fit analysis (Stage 2) made the case crisply: there is **no axis for cross-repo GitHub code investigation**. Today, when an agent needs "show me 3 real production usages of `pydantic_ai.Agent`," it falls back to Tavily web search, which returns blog posts, Stack Overflow answers, and partial snippets — not first-party source code from real projects.

The three octocode-unique capabilities (cross-repo code search, package→repo resolution, PR archaeology) are exactly the gap.

---

## The Integration Question

> **What is the most beneficial way to integrate octocode into `deep-research.md` such that (a) downstream consumers automatically benefit, (b) the new capability is selected only when genuinely better than the existing axes, (c) the file's distinctive "routing policy" rigor is preserved or improved, and (d) supply-chain / rate-limit / failure modes are handled at the policy layer rather than left implicit?**

Sub-questions worth surfacing:

1. **Declarative or behavioral?** Add octocode to the tool list and a 4th axis (declarative), or introduce a new behavioral concept like a "code-pattern axis" with its own decision rules?
2. **Per-agent or via persona?** Should octocode be wired into `deep-research` directly, or accessed via a delegated sub-agent (e.g., `code-pattern-researcher`) that `deep-research` calls when appropriate?
3. **Always-on or invocation-gated?** Should the policy default to including octocode in every Tavily query that smells like "code patterns," or require a positive trigger (mode flag, question shape)?
4. **Schema integration?** The output `Sources table` has a `backend` column — does that grow to include `octocode`, or do octocode findings flow through a different output shape?

---

## Wave 1: Divergent Ideation (cast a wide net)

I deliberately span declarative ↔ behavioral ↔ delegated ↔ hook-driven ↔ prompt-only ↔ hybrid.

### Candidate A — "Pure declarative 4th axis" (the obvious one)

**One-line:** Add octocode tools to the `tools:` list and append a fourth section to the Tool Selection Policy.

**How it works:** Mirror the structure of "Tavily-first rule" with a new "Octocode-for-code-patterns rule." Five new tool entries in frontmatter; ~15-20 lines of policy text; one new value (`octocode`) added to the `backend` enum in the output contract.

**Octocode tools used:** `githubSearchCode`, `githubSearchRepositories`, `githubSearchPullRequests`, `githubGetFileContent`, `githubViewRepoStructure`, `packageSearch` (6 tools — the cross-repo whitelist).

**Where in the file:** Frontmatter `tools:` (line 5–15), new policy section after line 47, sources table enum on line 66.

---

### Candidate B — "Behavioral router with question-shape triggers"

**One-line:** Add octocode but gate it behind explicit **question-shape triggers** — only fires when the question matches one of N declared archetypes.

**How it works:** Instead of a 4th axis with "use when X," introduce a new section called **"Backend routing by question shape"** that maps question patterns to backends:

- `"how does <package> implement <feature>?"` → octocode primary
- `"show me real usages of <symbol>"` → octocode primary
- `"why did <repo> change <X>?"` → octocode (PRs) primary
- `"what does <package> do?"` → packageSearch → Context7 fallback
- `"<concept> best practices"` → Tavily primary (octocode would just return scattered code)
- `"<framework> API for <thing>"` → Context7 primary

The policy is **anti-trigger-heavy**: octocode is the chosen backend only when the question is literally about cross-repo code. This is the only candidate that handles the "octocode is bad at conceptual research" failure mode at the policy layer.

**Octocode tools used:** Same 6 tools, but invoked through pattern dispatch rather than free-form selection.

**Where in the file:** Replace lines 30–47 with a new "Backend routing by question shape" subsection, OR add it as Section 3 with the existing axes as Section 2.

---

### Candidate C — "Delegated sub-agent" (`code-pattern-researcher`)

**One-line:** Don't put octocode in `deep-research` at all. Create a new sibling agent `code-pattern-researcher` that owns octocode, and have `deep-research` delegate to it via Task tool when the question is code-shaped.

**How it works:** A new file `src/superclaude/agents/code-pattern-researcher.md` with octocode in its `tools:` list. `deep-research.md` gains one sentence in the policy: "For questions whose answer is 'real code from real repos,' invoke `code-pattern-researcher` via the Task tool and synthesize its findings into the sources table with `backend: code-pattern-researcher`."

**Octocode tools used:** All 6 cross-repo tools, plus the local LSP tools made available (since the sub-agent could specialize in both cross-repo and serena-augmented local).

**Where in the file:** Tiny change to `deep-research.md` (~5 lines, a new sub-rule); large net addition (a new 80-line agent file).

---

### Candidate D — "Prompt-template-only enrichment"

**One-line:** Don't change the tool list at all. Add a new **"Code-pattern enrichment hint"** to the workflow section that tells the agent: "If the question involves real-code patterns, suggest in your report that the operator follow up with `/sc:research --mode github` or invoke the `code-pattern-researcher` agent."

**How it works:** Pure prose change. Acknowledges that octocode is available framework-wide (via the MCP registry) but doesn't grant `deep-research` direct access. The agent surfaces *recommendations* rather than executing octocode calls itself.

**Octocode tools used:** None directly. Octocode is referenced by name in the policy as a downstream tool the operator could use.

**Where in the file:** ~5 lines added to the Workflow section (line 53–58), nothing in frontmatter.

---

### Candidate E — "Confidence-driven hybrid"

**One-line:** Octocode is invoked **after** the initial Tavily/Context7 pass when the confidence-check on findings is < 80%.

**How it works:** Modify the Workflow section to add a new step between "Validate" and "Report": "If after primary search the synthesis has confidence < 0.80 due to lack of first-party source citations, escalate to octocode for cross-repo code lookups." This makes octocode a **second-line tool**, used only when the first line fails to produce high-confidence answers.

This is the most aligned with the framework's existing ConfidenceChecker pattern (`pm_agent/confidence.py`).

**Octocode tools used:** Same 6, but on an escalation path rather than a parallel one. Avoids burning Search-API budget on questions Tavily could have answered.

**Where in the file:** Frontmatter tools list grows by 6; Workflow section gains a new step 4.5; Tool Selection Policy gains a 4th axis but with explicit "secondary on confidence-trigger" framing.

---

### Candidate F — "Modal axes" (research-depth-aware)

**One-line:** Tool Selection Policy becomes a function of the `depth` parameter (`quick`, `standard`, `deep`, `exhaustive`) the agent already accepts on line 24.

**How it works:** Today the `depth` parameter is mentioned but doesn't actually change behavior in the policy. Make it load-bearing:

- `quick` → Tavily only, no octocode (octocode's setup time + Search-API budget is wasted for shallow questions)
- `standard` → Tavily + Context7, octocode opt-in via question shape
- `deep` → Tavily + Context7 + octocode (parallel) for code-shaped questions
- `exhaustive` → all backends fan out; octocode includes PR archaeology and `githubSearchPullRequests`

**Octocode tools used:** Same 6, with the heaviest tools (`githubSearchPullRequests`, `githubCloneRepo` if ever whitelisted) gated to `exhaustive`.

**Where in the file:** Restructure Tool Selection Policy into a depth-keyed table (lines 30–47 rewritten as a matrix).

---

### Candidate G — "Persona-aware" (research-axis routing per consumer persona)

**One-line:** The Tool Selection Policy reads the calling skill/persona and routes differently — `tech-research` gets octocode by default, `brainstorm` gets it for code-domain only, `troubleshoot` gets PR archaeology, `tech-reference` gets package→repo for any third-party reference.

**How it works:** Adds a Section "Per-persona backend preferences" that calling skills can rely on as an implicit contract. Calling skills don't have to know about octocode — they just call `deep-research` and the policy decides.

**Octocode tools used:** Subset depends on caller. `tech-research` → all 6. `troubleshoot` → `githubSearchPullRequests` + `githubSearchCode`. `tech-reference` → `packageSearch` + `githubGetFileContent`.

**Where in the file:** New section after the existing axes. Risk: introduces hidden coupling between agent and caller.

---

## Wave 2: Adversarial Evaluation

| Candidate | Pros | Cons | Risks | Effort |
|---|---|---|---|---|
| **A — Pure declarative 4th axis** | Smallest diff. Mirrors existing structure exactly. Easy to review. Easy to revert. No new agents. Drops cleanly into the existing Tavily-first rigor. | Doesn't capture **when** octocode is worse than Tavily (conceptual/best-practices questions). Agent's free-form judgment may overuse it. Doesn't address rate-limit handling. | LLM picks octocode for the wrong question shape (e.g., "Python async best practices") and wastes Search-API budget; cascades to all downstream consumers since they share this agent. | **Low.** ~25 lines in one file. |
| **B — Behavioral router with question-shape triggers** | **Addresses the failure mode head-on** by encoding when octocode is wrong. Mirrors how a senior researcher actually thinks ("is this question about code or about concepts?"). Easy to add new patterns later. | More prescriptive — risk that real questions don't match any pattern and the policy is ambiguous. Pattern list will grow stale. Harder to grep for. | New patterns added haphazardly over time; the policy becomes a tangle. Anti-trigger patterns may be too aggressive and never invoke octocode at all. | **Medium-low.** ~50 lines, denser thinking, but still one file. |
| **C — Delegated sub-agent (`code-pattern-researcher`)** | Clean separation of concerns. `deep-research` stays small and focused. The new agent can own LSP + cross-repo together and be reused by `auggie-reviewer`, `rf-task-researcher`. Failure isolation. | Adds **a new agent file** — requires `make sync-dev`, new tests, and discovery via slash commands. Doubles the "where is octocode wired" surface. Task-tool overhead per delegation. | New agent becomes orphaned if rarely invoked. Two researcher agents creates confusion ("which do I call?"). | **Medium-high.** New 80-line agent file + small edit + tests + sync. |
| **D — Prompt-template-only enrichment** | **Zero risk.** Surfaces awareness without granting access. Lets operators decide. Trivially reversible. | Provides essentially zero leverage on the framework. Defeats the whole point of the integration. Downstream skills can't rely on the capability being there. | Operator confusion ("the agent told me to use a tool I don't have"). | **Trivial.** ~5 lines. |
| **E — Confidence-driven hybrid** | Aligns beautifully with the framework's existing `ConfidenceChecker` pattern. Octocode used only when needed. Saves rate-limit budget. Natural fit for "evidence-based development" philosophy. | Implementing confidence-check inside the agent's workflow adds complexity. "Confidence < 0.8" is fuzzy — when is it actually triggered? Risk that the trigger never fires and octocode is dead weight. | Subtle bugs in the threshold; agent stays at 0.79 forever and never escalates. | **Medium.** ~30 lines + harder to spec. |
| **F — Modal axes (depth-aware)** | Uses an existing parameter (`depth`) that is currently inert. Excellent rate-limit story (no octocode in `quick` mode). Discoverable — the matrix is explicit. | Restructures the existing policy from prose to a matrix — bigger diff to review. `depth` is set by the caller, which is sometimes opaque. Many callers default to `standard` and never see octocode. | Most invocations stay at `standard`; octocode benefit lost in practice. | **Medium.** ~40 lines but restructures a stable section. |
| **G — Persona-aware (caller-keyed routing)** | Tailors backend selection to the actual use case. Maximally smart. | Introduces hidden coupling — the agent has to "know" its callers, violating encapsulation. Hard to maintain as the caller list grows. Difficult to test. | Coupling between agent and N skills becomes a refactoring blocker. | **High.** Touches the policy + every caller's documented invocation. |

### Adversarial cross-cuts

**The supply-chain question** (Stage 1 §4.1): all candidates are equally exposed to the npm-credential-compromise risk. None of A–G adds defense at the agent level — that defense has to live in `install_mcp.py` (pinned version, `LOG=false`, `TOOLS_TO_RUN` whitelist). The candidates differ only in **how often** octocode is invoked, which affects blast radius but not initial vulnerability.

**The rate-limit question** (Stage 1 §4.3): Candidates A, B, G allow octocode to be invoked freely. Candidate E gates by confidence (saves budget when first-line works). Candidate F gates by depth (saves budget for `quick` queries). Candidate C delegates to a sub-agent that could implement its own rate-limit awareness. Candidate D never invokes — no risk.

**The context-tax question** (Stage 1 §4.4): Candidates A, B, E, F, G all add 5–6 tools to `deep-research`'s frontmatter → all consumers pay ~3-7K extra context tokens per invocation. Candidate C isolates the cost to the sub-agent (consumers of `deep-research` don't pay). Candidate D adds zero context.

**The downstream-cascade question** (the original fit-analysis argument for picking target #1): A, B, E, F, G all propagate to every consumer. C requires consumers to opt into the sub-agent. D propagates only as a textual suggestion.

**The "anti-trigger rules" question** (when octocode would be the wrong choice): Only B and E explicitly handle this. A, F, G leave it to LLM judgment. C delegates the judgment to the sub-agent. D sidesteps entirely.

---

## Wave 3: Convergence

### The winner: **Candidate B — Behavioral router with question-shape triggers**

### Why B beats the others for THIS specific target

The `deep-research` agent's distinctive design feature is **its routing policy rigor**. The Tavily-first rule (lines 30–47) reads like a piece of infrastructure code — it specifies what "unavailable" means, mandates `fallback_reason` annotation, forbids silent fallback. The file's strength is that it doesn't say "use Tavily" — it says **when** Tavily applies, **when** it doesn't, and **what to do when it fails**.

The single biggest weakness of octocode in this surface is that the LLM will be tempted to reach for it on **conceptual questions** ("how should I architect a queue?") where it returns scattered code that doesn't actually answer the question, when Tavily would have returned a high-quality blog post that does. This is the failure mode that destroys the integration's ROI. None of the other candidates encode this failure mode at the policy level — they all defer it to LLM judgment.

Candidate B is the only one that **uses the file's existing strength** (declarative routing rigor) to **defend against octocode's primary failure mode** (overuse on conceptual questions). It is also the only one that scales naturally — adding a new question-shape pattern later is a one-line append, exactly like adding new fallback triggers to the Tavily-first rule.

Candidate B also preserves the file's review-friendliness: the policy is still all in `deep-research.md`, still ~50 lines, still greppable, still revertible.

### Runner-up: **Candidate E (confidence-driven hybrid)**

E lost narrowly. Its alignment with the existing `ConfidenceChecker` pattern is genuinely elegant, and "octocode as second-line tool when first-line confidence < 0.8" is a beautiful framing.

E lost on two grounds:
1. **Confidence-threshold operationalization is harder than question-shape matching.** Question shape is something the LLM can pattern-match on the user's prompt directly. Confidence requires the agent to first do a search, score the result, and decide to escalate — that's three subjective judgments stacked. Question shape is one.
2. **The escalation pattern delays octocode's value.** In B, "show me real usages of useEffect cleanup" goes directly to octocode. In E, it goes to Tavily first, the agent realizes Tavily returns blog posts, and *then* escalates. That's 2× latency and 2× tokens for the questions where octocode is obviously right.

If we revisit the design in 6 months and the question-shape patterns are not catching all the cases, Candidate E is the natural evolution: keep B's patterns for unambiguous cases, layer E's confidence-trigger on top for the ambiguous ones.

### Honorable mentions for what they teach us

- **Candidate C** (delegated sub-agent) is the right answer if octocode usage explodes in scope to include LSP tools and serena-augmentation. Today it's premature.
- **Candidate F** (depth-aware) has the best rate-limit story — we should steal one line from it: "in `quick` depth, skip octocode."
- **Candidate A** is what we'd ship if we had 10 minutes. B is what we ship if we have 2 hours.

---

## Recommended Design (Deep Dive)

### Full description

Add octocode as a fourth research backend, but introduce it via **question-shape routing** rather than a free-form axis. The Tool Selection Policy gains a new top-level section titled **"Backend routing by question shape"** that maps prompt archetypes to primary/fallback backends. The existing axes (Tavily-first, Context7 for library docs, Sequential for synthesis) become **default-when-no-pattern-matches** rather than the only routing logic.

Specifically:

1. The agent first attempts to classify the user's question into one of seven shapes (six positive + one explicit anti-pattern set).
2. If the shape matches, the policy prescribes a primary octocode tool, a fallback, and an explicit `anti-trigger` clause.
3. If no shape matches, the agent falls through to the existing Tavily/Context7/Sequential axes.
4. Output sources table grows `backend` to include `octocode`, with the existing `fallback_reason` annotation pattern reused for octocode-specific failure modes (rate-limit, search-API-403, repo-not-found).

### Concrete diff sketch

Below is what the actual file change would look like. The diff is bounded to `deep-research.md` and is fully reversible.

**Frontmatter** (lines 1–16) — add 5 new tools (`githubSearchCode`, `githubSearchPullRequests`, `githubGetFileContent`, `githubViewRepoStructure`, `packageSearch`):

```diff
 name: deep-research
-description: Adaptive research specialist for external knowledge gathering. Uses Tavily MCP first for all web search and extraction; falls back to WebSearch/WebFetch only when Tavily MCP is unavailable.
+description: Adaptive research specialist for external knowledge gathering. Routes by question-shape across Tavily (web), Context7 (library docs), and Octocode (cross-repo code patterns), with WebSearch/WebFetch as final fallback when Tavily MCP is unavailable.
 category: analysis
 tools:
   - mcp__tavily__tavily-search
   - mcp__tavily__tavily-extract
   - WebSearch
   - WebFetch
   - mcp__context7__resolve-library-id
   - mcp__context7__query-docs
+  - mcp__octocode__githubSearchCode
+  - mcp__octocode__githubSearchPullRequests
+  - mcp__octocode__githubGetFileContent
+  - mcp__octocode__githubViewRepoStructure
+  - mcp__octocode__packageSearch
   - Read
   - Grep
   - Glob
   - mcp__sequential-thinking__sequentialthinking
```

**Body** (after line 47, before the Workflow section on line 53) — insert a new subsection. The existing "Tavily-first rule" subsection stays in place; this new one sits *above* it logically (question-shape classification runs first, then falls through to axis-by-axis defaults):

```diff
+### Backend routing by question shape (run this BEFORE the axes below)
+
+Before applying the axis-by-axis defaults, classify the question against the table below. If exactly one row matches, that row's `primary` backend is the chosen entry point; the existing axes serve as fallbacks per the per-row policy.
+
+| Question shape (regex/intent) | Primary | Fallback | Anti-trigger |
+|---|---|---|---|
+| "how does <package\|library> implement <feature>" | `packageSearch` → `githubViewRepoStructure` → `githubSearchCode` → `githubGetFileContent` | Context7 (if package has canonical docs) | Question is about *concept* not specific implementation (e.g., "how does async work" — use Tavily) |
+| "show me real (production\|usage) examples of <symbol\|API>" | `githubSearchCode` → `githubGetFileContent` | Tavily (blog posts with snippets) | <symbol> is too generic (`map`, `filter`); use Context7 |
+| "why did <repo> change <X>" / "what was the rationale for <PR>" | `githubSearchPullRequests` → `githubGetFileContent` | Tavily (engineering blog posts) | Repo not on GitHub; use Tavily |
+| "what does <package> actually do" / "is <package> deprecated" | `packageSearch` | Context7 | Question is about choosing between packages — use Tavily for comparison reviews |
+| "compare how <projectA> vs <projectB> solve <X>" | `githubSearchCode` (fan-out across repos) → `githubViewRepoStructure` | Tavily (comparison blog posts) | One project isn't on a code host — use Tavily |
+| "find a reference implementation of <pattern>" | `githubSearchCode` → `githubGetFileContent` | Tavily (curated lists) | <pattern> is conceptual (e.g., "CQRS pattern") — use Tavily for theory, octocode for code |
+| **Anti-pattern (use Tavily, NOT octocode):** | | | |
+| "what are best practices for <X>" | Tavily | Context7 | — |
+| "<framework> tutorial / getting started" | Tavily / Context7 | — | — |
+| "<error message> debugging" | Tavily | octocode `githubSearchPullRequests` only as 3rd line | — |
+| "<concept> explained" | Tavily | — | — |
+
+If no row matches, fall through to the per-axis policy below.
+
+### Octocode failure handling
+
+Treat octocode as unavailable, and fall back to Tavily, when **any** of the following holds:
+
+- The `mcp__octocode__*` tools are not present in the available tool surface (server not installed/configured).
+- An octocode call returns a transport-level error (timeout, connection refused, 5xx) twice in a row for the same query.
+- An octocode call returns a GitHub `403` (rate-limit) or `404` (repo-not-found).
+- An octocode call returns an authentication error (missing/invalid `GITHUB_TOKEN`).
+
+In every fallback event, record in the source citation table: `fallback_reason: <octocode_missing | octocode_error | octocode_rate_limit | octocode_auth | octocode_not_found>`.
+
+### Octocode rate-limit budget
+
+Octocode's GitHub Search API is capped at 30 req/min. Budget heuristics for this agent:
+
+- A single research session SHOULD NOT issue more than 10 `githubSearchCode` calls in 60 seconds.
+- Prefer `packageSearch` (REST API, higher limit) over `githubSearchRepositories` for package→repo resolution.
+- Always pass `researchGoal` + `reasoning` fields on octocode calls (octocode requires them, and they pair with our MDTM audit trail).
+
+### Never silent fallback
+
+Per the existing Tavily-first rule, every source in the output table MUST declare its backend. The `backend` enum on the sources table grows to: `[tavily | websearch | webfetch | context7 | octocode]`.
```

**Output contract** (line 64) — update the `backend` enum:

```diff
- 🔗 Sources table (URL, title, credibility score, backend [tavily|websearch|webfetch|context7], note)
+ 🔗 Sources table (URL, title, credibility score, backend [tavily|websearch|webfetch|context7|octocode], note)
```

**Net file delta:** ~55 added lines, ~3 modified lines, 0 deleted lines. Single file.

### Tool subset used (explicit)

From octocode's 14 tools, this design uses **5 of the cross-repo subset**:

1. `mcp__octocode__githubSearchCode` — keyword search across GitHub repos
2. `mcp__octocode__githubSearchPullRequests` — PR archaeology
3. `mcp__octocode__githubGetFileContent` — read file contents from any GitHub repo
4. `mcp__octocode__githubViewRepoStructure` — repo tree exploration
5. `mcp__octocode__packageSearch` — npm/PyPI → repo URL + version + deprecation status

**Explicitly excluded** (and the reason for each):

- `githubSearchRepositories` — Tavily does this better for "find a tool that does X"; octocode adds little.
- `githubCloneRepo` — writes to `~/.octocode/repos/`, disk-bound, no benefit for research.
- `localSearchCode`, `localViewStructure`, `localFindFiles`, `localGetFileContent` — overlap 100% with native Read/Grep/Glob and auggie.
- `lspGotoDefinition`, `lspFindReferences`, `lspCallHierarchy` — overlap with serena's symbol tools; serena is already wired into the framework.

This 5-tool whitelist is also what should be passed as `TOOLS_TO_RUN` in the MCP server registration (`install_mcp.py:29` per Stage 2 Phase A).

### Anti-trigger rules (the load-bearing piece)

The anti-triggers below are why Candidate B wins. Without them, the LLM will overuse octocode on conceptual questions and burn rate-limit budget. With them, octocode is reached for **only** when first-party source code is the right answer.

**Never use octocode (use Tavily/Context7 instead) when:**

1. Question is about **best practices** without a specific implementation in mind. ("What are best practices for error handling in Python?") → Tavily returns curated guidance; octocode returns 50 scattered try/except blocks.
2. Question is a **tutorial / getting started** ask. → Tavily / Context7 are better.
3. Question is about a **concept** ("what is CQRS"). → Tavily.
4. Question is about an **error message** from a specific stack trace. → Tavily first (Stack Overflow has the high-density answers); fall to octocode only if Tavily produces nothing AND the error references a specific library where reading the source would help.
5. Question is **comparative across approaches** ("REST vs GraphQL"). → Tavily.
6. Question's `<symbol>` is too **generic** to discriminate (`map`, `filter`, `i`, `len`). → octocode would return millions of hits.
7. Question targets a **non-GitHub host without a public mirror**. → Tavily.

These anti-triggers are encoded in the policy table above; they are not LLM-implicit.

### Rate-limit / failure handling

The "Octocode failure handling" subsection in the diff above mirrors the structure of the existing Tavily-first rule. Five named failure modes, all annotated with `fallback_reason` in the output table. The fallback target for every octocode failure mode is Tavily — octocode never falls back to itself, and never fails silently.

The rate-limit budget heuristics (≤10 `githubSearchCode` calls / 60s) are advisory because the agent can't enforce them mechanically, but they give the LLM a number to plan against. If the agent issues 8 calls in the first 30s, it should choose to read deeply into existing results rather than fan out further.

### Test plan

**Validation that this works:**

1. **Smoke test — frontmatter parse.** `uv run python -c "import yaml; yaml.safe_load(open('src/superclaude/agents/deep-research.md').read().split('---')[1])"` — confirm the YAML parses. Run `make sync-dev` and `make verify-sync` to confirm `.claude/agents/deep-research.md` reflects the change.

2. **Tool surface presence.** Spawn a `deep-research` agent in a session with octocode MCP installed; confirm all 5 octocode tools appear in its tool list. Spawn another in a session without octocode; confirm the agent reports `octocode_missing` and falls back to Tavily.

3. **Question-shape routing — positive cases.** Run a fixture set of 6 prompts (one per question shape) and verify:
   - The agent's reported `backend` for each source matches the table.
   - The actual MCP calls made (visible in the agent's tool-call log) are octocode calls for the positive shapes.
   - Example fixtures:
     - "How does httpx implement retry logic?" → expect `packageSearch` + `githubGetFileContent`
     - "Show me 3 production examples of pydantic_ai.Agent registration" → expect `githubSearchCode`
     - "Why did langchain change their tool-calling API?" → expect `githubSearchPullRequests`

4. **Anti-trigger enforcement — negative cases.** Run prompts that match the anti-triggers and verify the agent does NOT invoke octocode:
   - "What are Python error-handling best practices?" → expect Tavily only
   - "Explain CQRS" → expect Tavily only
   - "React tutorial" → expect Context7 or Tavily

5. **Failure-mode handling.** Simulate octocode rate-limit by issuing 30 fast queries in a session and confirm the agent records `fallback_reason: octocode_rate_limit` and continues with Tavily.

6. **Output contract.** Confirm every source in the agent's output table has a `backend` field, and that the value is from the enlarged enum `[tavily | websearch | webfetch | context7 | octocode]`.

7. **Downstream propagation — sanity.** Spawn `tech-research` skill on a question that should route to octocode (e.g., "research how OpenTelemetry instruments async tasks across libraries"). Confirm the Phase 4 deep-research sub-agents actually pick octocode for the appropriate sub-questions.

8. **No regression on non-code questions.** Run the existing `deep-research` test suite (if any; otherwise run a representative non-code prompt) and confirm octocode is not invoked — pure Tavily/Context7 behavior preserved.

**Acceptance gate:** All 8 above pass. The integration is "done" when a `tech-research` Deep tier run consuming `deep-research` agents produces a sources table with mixed backends (`tavily` + `octocode` + `context7`) for a code-heavy research question.

---

## What This Cannot Do

Honest limits of the recommended design:

1. **It doesn't help with octocode's supply-chain risk.** That defense lives in `install_mcp.py` (pinned version, `LOG=false`, telemetry off, whitelist of 5 tools). This design assumes those are in place.

2. **It doesn't help with the npm-credential-compromise scenario.** If bgauryy's npm account is compromised and a malicious `octocode-mcp@14.2.1` ships, this design provides no defense — the version is pinned in `install_mcp.py`, not here.

3. **It doesn't expose octocode's LSP tools.** The 3 LSP tools (`lspGotoDefinition`, `lspFindReferences`, `lspCallHierarchy`) overlap with serena and stay disabled. If we later find serena gaps on, say, Ruby projects, we'd need to revisit.

4. **It doesn't reduce context tax.** Adding 5 tools to `deep-research`'s frontmatter costs ~3-5K tokens per invocation of every consumer (`tech-research`, `troubleshoot`, etc.). That is the cost of the cascade-by-design benefit.

5. **It cannot prevent the LLM from overusing octocode.** Question-shape patterns are guidance, not a hard gate. If the LLM mis-classifies a question, octocode will be invoked anyway. We rely on the anti-trigger explicit list to make over-invocation rare, but it isn't enforced.

6. **It does not specify a `quick`-depth opt-out.** Candidate F's depth-aware framing was the right answer to "save rate-limit budget on shallow queries." We don't adopt it here to keep the diff small, but we should add a single line — "If depth=quick, skip the question-shape routing and use only Tavily" — as a follow-up. Flagged in cross-target dependencies below.

7. **It doesn't help when the question is genuinely cross-platform** (npm AND PyPI AND Maven). `packageSearch` covers npm + PyPI only.

8. **It doesn't add value for organizations using GitLab or Bitbucket exclusively.** Octocode supports them but the `packageSearch` and PR-archaeology coverage is GitHub-strongest. Bitbucket users get less.

---

## Cross-Target Dependencies

This design's interaction with the other 4 parallel brainstorm targets:

1. **Depends on Target #5 (MCP server registration in `install_mcp.py`)** being completed first. The recommended design assumes:
   - octocode-mcp is installed via `superclaude mcp --servers octocode`
   - Version is pinned to `14.2.0` (not `@latest`)
   - `LOG=false` is set
   - `TOOLS_TO_RUN=githubSearchCode,githubSearchPullRequests,githubGetFileContent,githubViewRepoStructure,packageSearch` is set
   - If Target #5 lands with a different whitelist, this design's tool list MUST match.

2. **Affects Target #2 (`tech-research` skill Phase 4)** because `tech-research`'s Phase 4 web-research agents are spawned with the `deep-research` agent's policy. Once this lands, Phase 4 automatically benefits from question-shape routing — Target #2 becomes a *smaller* edit (just adjusting the agent-prompt template to mention octocode-shaped questions).

3. **Affects Target #4 (`sc-brainstorm-protocol` Wave 2A)** similarly. The Wave 2A enrichment matrix dispatches to multiple research agents; once `deep-research` knows about octocode, brainstorm enrichment gets it for free for `domain in {code, architecture}`.

4. **May overlap with Target #3 (`sc:research` command)** depending on what that brainstorm proposes. If Target #3 proposes a new `--mode github` flag, that flag could trigger this agent with a hint to force the question-shape route. The interface point is the command-to-agent contract — Target #3's design must consume `deep-research`'s policy, not redefine it.

5. **Independent of any decision on whether to fork/customize octocode's bundled skills marketplace.** This design uses only octocode's MCP tools, not its skills.

**Recommended sequencing if all 5 land:**

- PR-A: Target #5 (MCP registration) — foundational, blocks everything else.
- PR-B: Target #1 (this design) — propagates to all consumers.
- PR-C: Target #2 + Target #4 in parallel — both benefit from PR-B's cascade.
- PR-D: Target #3 — last, because it's user-facing and needs the agent contract stable.

---

## Effort Estimate

| Item | Estimate |
|---|---|
| **Files touched** | 1 file (`src/superclaude/agents/deep-research.md`) — and after `make sync-dev`, the synced `.claude/agents/deep-research.md` mirror. |
| **Lines of change** | ~55 added, ~3 modified, 0 deleted in `src/superclaude/agents/deep-research.md`. |
| **New files** | None. |
| **Test-fixture work** | 8 fixture prompts + expected backend per Section "Test plan" above. ~30 lines of test data. Optional: add a `tests/agents/test_deep_research_routing.py` smoke test that asserts the agent's frontmatter parses and the policy table contains the expected rows. |
| **Documentation** | 1 paragraph in `docs/agents/deep-research.md` (or wherever agent docs live) explaining the question-shape routing. Optional `KNOWLEDGE.md` entry: "octocode is reached via deep-research question-shape routing, not by direct tool invocation in skills." |
| **Review time** | 30–45 min. The diff is mostly a routing table; reviewers should verify (a) the anti-triggers cover the obvious overuse cases, (b) the failure-mode handling mirrors the Tavily-first rule structure, (c) the new tools in the frontmatter exactly match Target #5's whitelist. |
| **Hours to implement** | **3–4 hours.** Breakdown: 30 min reading current policy + Stage 1/2 docs (already done in this brainstorm), 60 min drafting the routing table + anti-triggers, 30 min wiring frontmatter, 30 min `make sync-dev` + `make verify-sync`, 60 min writing the 8 test fixtures + spot-checking, 30 min PR description + cross-references to Target #5. |
| **Dependencies** | Blocks on Target #5 landing first. Otherwise pure-declarative — no Python code changes, no new agents, no breaking API changes. |
| **Reversibility** | Trivially reversible. `git revert` the single-file PR; downstream consumers fall back to the current 3-axis policy. No data migration, no state to clean up. |

---

**Brainstorm complete.**

Convergent answer: **Candidate B — Behavioral router with question-shape triggers.** It exploits the file's existing routing-policy rigor to defend against octocode's primary failure mode (overuse on conceptual questions), at low effort, in a single file, with a clean reversal path.

The single-file, ~55-line diff is small enough to ship in one PR, and propagates the cross-repo capability to every downstream consumer of `deep-research` automatically. The anti-trigger list is the load-bearing piece that distinguishes this design from a naive "add octocode as a 4th axis" change.

Runner-up Candidate E (confidence-driven hybrid) is the right v2 if question-shape patterns prove insufficient in practice — they compose, they don't conflict.
