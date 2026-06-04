# Brainstorm 06: Skill-Level Integration (Alternate Path)

**Date:** 2026-05-30
**Author:** Brainstorm agent #6 — Skill-Level lens
**Status:** Proposal
**Relationship to fit-analysis:** Argues against the fit-analysis's top pick (#1, `deep-research` agent integration, score 45) and in favor of #2 + #4 + #6 (skill-level integrations totaling score 40+32+28 = 100) as a coordinated alternate.

---

## Lens

**Each skill owns its own tool surface, prompt template, routing matrix, and quality-tier rules. Integration at the skill level — not the agent level — is the correct seam for octocode because:**

1. **Skills are workflows; agents are workers.** A workflow controls *which* questions get asked. A worker just answers them. Octocode's whole value-add is changing *what kind of question is feasible* ("how do 3 production repos solve X"). That belongs in the workflow author's hands — i.e., the skill — not delegated to a worker the skill cannot fully observe.

2. **Skills are versioned with the framework via `make sync-dev`.** They have CODEOWNERS, lint hooks, sync-verification, and downstream consumers. Agent definitions in `src/superclaude/agents/deep-research.md` are also versioned, but they are loaded **opportunistically** by 5+ skills with different needs. Modifying `deep-research.md` changes behavior for `tech-research`, `tech-reference`, `troubleshoot`, `brainstorm`, and any future caller simultaneously — a global mutation with no per-caller A/B handle.

3. **Different skills want different octocode subsets.** `tech-research` Phase 4 wants `githubSearchCode` + `packageSearch` for community-precedent discovery. `sc:troubleshoot` Wave 3 wants `githubSearchPullRequests` for "who else hit this error" archaeology. `sc:brainstorm` Wave 2A wants `githubSearchRepositories` for "what other projects in this space exist." Agent-level integration forces all three through one Tool Selection Policy, biasing the agent's choice on a per-invocation basis with no skill-side control.

4. **A/B testing requires a flag per skill, not a flag in the agent.** Skills already have `--no-codebase`, `--no-doc-discovery`, `--research light|deep`, `--depth quick|standard|deep`. Adding `--octocode` (or making it conditional on `--research deep`) at the **skill** is a natural extension. Adding it at the agent means every caller inherits the same default — no graduated rollout.

5. **Skill-level integration is the right altitude for the hallucination contract.** `sc:troubleshoot` SKILL.md:24 says *"Every claim in the final report must cite a real `file:line` or a real diagnostic command and its output. Findings that cannot be grounded are dropped, not downgraded."* Octocode returns external GitHub code — that grounding contract differs from local-code citations. The skill is the only place where the citation-style rule can be enforced *for this specific tool*. Pushing octocode into the agent loses the local context for citation policy.

6. **The skill author can decide when octocode is allowed to fire.** `tech-research` Phase 2 (Deep Investigation) is the wrong place for cross-repo lookup — that's local-code-only by design. Phase 4 (Web Research) is the right place. The agent has no concept of "Phase 2 vs Phase 4" — that's purely a skill construct. Embedding octocode at the agent layer collapses this phase-aware distinction.

---

## Why NOT the deep-research agent path

The fit-analysis ranks `deep-research` agent integration #1 with score 45. The argument is "one change propagates to all 5+ downstream skills." **That is precisely the problem, not the benefit.**

**Critique 1 — One-size-fits-all routing destroys skill-specific intent.**
The fit-analysis (lines 68-73) proposes adding a 4th axis to the agent's Tool Selection Policy:

> Axis 4: GitHub code-pattern discovery
> Primary: octocode (cross-repo semantic search, PR archaeology, package→repo resolution)
> Use when: question is "how do real projects implement X" or "what does package Y actually do"

This is too generic. `sc:troubleshoot` calling `deep-research` is asking *"what does the docs say about retry semantics in httpx"* — that's a Context7 question, not octocode. But because the agent now has 4 axes and a vague "Use when" clause, the agent may decide to fire octocode for a question that didn't need it. The skill can no longer enforce its tool preference because the agent owns the routing.

**Critique 2 — Blast radius asymmetry.**
The fit-analysis says (line 79): *"Risk⁻¹ 4/5 — Adding to one agent's frontmatter is reversible."* True for the *frontmatter*. False for the *behavioral consequence*. If octocode hits a rate limit during a `tech-research` Deep-tier run that has 8 parallel Phase 4 agents, all 8 fail simultaneously because they all routed through the same agent. The skill has no per-agent fallback policy because the routing logic is hidden inside the agent's prompt.

**Critique 3 — A/B testing is structurally impossible.**
With agent-level integration, you cannot run an experiment where `tech-research` has octocode and `sc:troubleshoot` does not — they share the agent. You'd need to fork the agent (`deep-research-with-octocode.md`) which destroys the "one change" benefit the fit-analysis claims. Skill-level integration gives you 5 independent dials.

**Critique 4 — The agent definition is a user-facing surface.**
`src/superclaude/agents/deep-research.md` ships in the `superclaude install` payload to `~/.claude/agents/`. Users who don't have octocode installed will see the agent reference `mcp__octocode__*` tools that don't resolve, producing confusing fallback behavior. The skill is *also* shipped, but `tech-research` already has graceful enrichment-fallback machinery (Wave 2A quality-tier `primary | fallback_1 | fallback_2 | skipped` per SKILL.md:189-193 of `sc-brainstorm-protocol`) that the agent definition lacks.

**Critique 5 — The fit-analysis's "propagates to all consumers" framing is the worst-case scenario, not the best-case.**
Tech-research's Phase 4 wants 2-4 octocode calls per investigation. Sc:troubleshoot's Wave 3 wants at most 1 ("show me a similar bug in another repo"). Sc:brainstorm's Wave 2A wants 1 fan-out search ("how do similar projects solve this?"). These call-budget profiles are wildly different. Centralizing in the agent means all three get the same default, leading to either over-fetching in troubleshoot or under-fetching in tech-research.

**Bottom line:** The agent-level path is fast to ship and easy to reason about. It is also a coarse routing decision that removes per-skill control of the most expensive new tool the framework has adopted in a year. The skill-level path takes 3 PRs instead of 1, but each PR is small, scoped, and reversible — and the resulting system is observably better.

---

## Per-Skill Integration Specifications

### tech-research Phase 4

**Target:** `src/superclaude/skills/tech-research/SKILL.md`, lines 415-419 (Phase 4 description in BUILD_REQUEST) AND lines 674-719 (Web Research Agent Prompt template).

**Current Phase 4 description (SKILL.md:415-419):**

```text
Phase 4 — Web Research (PARALLEL SPAWNING MANDATORY):
- One checklist item PER web research topic (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with the web research agent prompt from SKILL.md
- Each item specifies: topic, context from codebase findings, output file path
- Web research targets should include (as applicable): official framework/engine documentation, design patterns and best practices, third-party tools/libraries/APIs, community solutions to similar problems, GitHub issues and discussions, conference talks and technical blog posts from recognized experts
```

**Proposed Phase 4 description (replace lines 415-419):**

```text
Phase 4 — Web Research + Cross-Repo Research (PARALLEL SPAWNING MANDATORY):
- One checklist item PER research topic (from research notes SUGGESTED_PHASES)
- Each item spawns an Agent subagent with EITHER the Web Research Agent Prompt
  or the Cross-Repo Research Agent Prompt (see Agent Prompt Templates section)
- Topic routing rule (applied by the orchestrator when building Phase 4 items):
  | Topic shape                                          | Prompt to use         |
  |------------------------------------------------------|----------------------|
  | "Official docs for X" / "API reference for Y"        | Web Research          |
  | "Best-practice survey of X" / "blog posts on Y"      | Web Research          |
  | "How do real projects implement X" / "callsites of Y"| Cross-Repo Research   |
  | "What does package Z actually do internally"         | Cross-Repo Research   |
  | "PR archaeology for the X API change in repo Y"      | Cross-Repo Research   |
  | "GitHub issues matching error signature E"           | Cross-Repo Research   |
- For Cross-Repo Research, the orchestrator MUST embed a tool-budget directive in
  the agent prompt: max 3 githubSearchCode calls, max 2 packageSearch calls,
  max 2 githubSearchPullRequests calls, max 5 githubGetFileContent calls per agent.
- If octocode is unavailable (mcp registration missing or rate-limited), fall
  back to the Web Research Agent Prompt with a note in the output file:
  "[OCTOCODE-FALLBACK] cross-repo investigation degraded to Tavily web search".
```

**Proposed Cross-Repo Research Agent Prompt (new section, insert after line 719):**

```text
### Cross-Repo Research Agent Prompt

Research this topic across external repositories and package ecosystems and write findings to [output-path].

Topic: [cross-repo investigation topic]
What we already know from codebase: [brief summary]
Research question context: [overall question]

CRITICAL — Incremental File Writing Protocol:
[Same as Web Research Agent Prompt — create file with header, append findings,
never accumulate.]

Tool budget (HARD CAP — exceeding is a protocol violation):
- mcp__octocode__githubSearchCode: max 3 calls
- mcp__octocode__packageSearch: max 2 calls
- mcp__octocode__githubSearchPullRequests: max 2 calls
- mcp__octocode__githubGetFileContent: max 5 calls
- mcp__octocode__githubViewRepoStructure: max 3 calls
- Local-tool family (mcp__octocode__localSearchCode, lspGotoDefinition, etc.):
  DISABLED for this prompt (auggie + serena own local).

Research Protocol — Funnel Method (from octocode RDD philosophy):
1. DISCOVER: packageSearch to resolve package name → repo URL
   (only when the topic names a package by name)
2. SEARCH: githubSearchCode with a focused query
   (must include researchGoal + reasoning per octocode RDD; orchestrator
    SHOULD log these to the output file as audit trail)
3. LOCATE: githubViewRepoStructure to identify the relevant file
4. READ: githubGetFileContent with charOffset/charLength to extract
   the relevant snippet only — do NOT fetch entire files

For each finding, document:
- Source URL (GitHub link with permalink commit SHA, NOT @main)
- Repo name + star count (for credibility weighting)
- Key information extracted (snippet, not full file)
- How it relates to our codebase findings
- Whether it supports, extends, or contradicts what we found locally

Mark every finding with the octocode tag [OCTOCODE-VERIFIED <SHA>] and
include the commit SHA so the citation is reproducible. A finding without
a SHA is treated as [UNVERIFIED] downstream by synthesis.

Reliability ranking:
- HIGH: official maintainer org (e.g., facebook/react, pallets/flask), 1k+ stars, recent commits
- MEDIUM: community fork or rewrite, 100-1k stars, maintained
- LOW: archived repos, forks-of-forks, <100 stars

Output Format:
- Use descriptive headers for each external repo investigated
- Always include GitHub permalink (with SHA, not @main/@master)
- Mark relevance: HIGH / MEDIUM / LOW
- End with:

## Key Cross-Repo Findings
  [Bullet list of the most important discoveries with permalinks]

## Recommendations from Cross-Repo Research
  [How external precedent should influence our approach]

IMPORTANT: Cross-repo code is precedent, not authority. A pattern used by
3 projects is suggestive; a pattern used by the official library maintainer
is stronger. Our codebase remains the source of truth. If you find a
discrepancy, note it explicitly with [CONTRADICTS-LOCAL] tag.
```

**Why this is the right diff:**

- Octocode is gated to a *specific topic shape* (4 of the 6 row types in the routing table), not "any web research topic." This prevents the agent-level scattergun problem.
- Tool budget is enforced in the prompt itself — the orchestrator does not need a separate enforcement mechanism, because the agent will refuse to exceed the cap.
- Local tools are explicitly disabled in this prompt, matching the research's Section 6 recommendation (lines 209-212): "whitelist `githubSearchCode`, `githubSearchRepositories`, `githubSearchPullRequests`, `githubGetFileContent`, `githubViewRepoStructure`, `packageSearch`. Disable all `local*` and `lsp*` tools." We do this *per skill*, not via global MCP env var, because other skills may want different subsets.
- SHA-pinned permalinks (not `@main`) make the citation reproducible — addresses the hallucination contract from troubleshoot SKILL.md:24 ("Every claim must cite a real file:line").
- Fallback to Web Research is explicit and graceful, matching the Wave 2A quality-tier pattern (`fallback_1`, `fallback_2`).

---

### sc-troubleshoot external-pattern

**Target:** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, Wave 3 step 1 (MCP enrichment lines 251-254).

**Current Wave 3 step 1 (lines 251-254):**

```text
1. **MCP enrichment in parallel with agent spawn** — issue any of the following that match the signals (parallel calls, all kicked off in the same turn):
   - `mcp__context7__resolve-library-id` + `mcp__context7__query-docs` when the issue mentions a framework / library by name or the stack trace is in third-party code
   - `mcp__tavily__tavily-search` for the exact error message string + "github issue", or for `<library> <version> <symptom>` (rate-limited — at most 2 queries in this wave)
   - `mcp__auggie__codebase-retrieval` with a more targeted query than Tier 1 (e.g. "find every call site of `<symbol>` and how they handle the error case")
```

**Proposed Wave 3 step 1 (add octocode as 4th bullet, only when type is `bug | build | test`):**

```text
1. **MCP enrichment in parallel with agent spawn** — issue any of the following that match the signals (parallel calls, all kicked off in the same turn):
   - `mcp__context7__resolve-library-id` + `mcp__context7__query-docs` when the issue mentions a framework / library by name or the stack trace is in third-party code
   - `mcp__tavily__tavily-search` for the exact error message string + "github issue", or for `<library> <version> <symptom>` (rate-limited — at most 2 queries in this wave)
   - `mcp__auggie__codebase-retrieval` with a more targeted query than Tier 1 (e.g. "find every call site of `<symbol>` and how they handle the error case")
   - **`mcp__octocode__githubSearchPullRequests` for cross-repo error-signature archaeology** when (a) `--type` is `bug | build | test`, AND (b) the issue includes a recognizable error string / stack trace fragment / exception class name, AND (c) the framework / library is identifiable. Query shape: `(stable error fragment) repo:<framework-org>/<framework-repo>` to find PRs that mention this error. Rate-limited: at most 1 octocode call per Wave 3 (Search API budget is 30/min — the 1-call cap leaves headroom for other concurrent skill invocations). If `--type` is `performance | security | deployment`, SKIP this enrichment — octocode adds no signal for those types.
```

**And update Wave 3 agent dispatch (lines 256-262) to pass octocode findings:**

Change:

```text
2. **Spawn hypothesis agents** in parallel via `Task` (single message with multiple Task calls). Each agent receives:
   - The original issue + Tier 1 hypothesis card (so they can agree, disagree, or extend)
   - The **Documentation Context Card** at `<output-dir>/doc-context.md` (the same single card produced by Wave 1.5 — agents do NOT re-run discovery). If `--no-doc-discovery` was set, this path is `null` and agents set `consistency_with_docs: not_applicable` in their hypothesis cards.
   - The MCP enrichment results
```

To (insert one new bullet between "Documentation Context Card" and "MCP enrichment results"):

```text
   - The **Cross-Repo Pattern Index** at `<output-dir>/wave3-octocode-patterns.md` (the synthesized output from octocode's githubSearchPullRequests call, OR an empty index containing the literal line "No cross-repo patterns relevant" when octocode was skipped or returned nothing). Each entry includes: repo, PR number, PR title, link with commit SHA, and a 1-line "why it might apply here." Hypothesis agents MAY reference these patterns in their hypothesis cards but MUST mark such references with `[CROSS-REPO-PATTERN]` tag and a permalink. The patterns are precedent, NOT evidence — only local `file:line` citations count toward the hallucination contract.
```

**Update the Tool Coordination Summary table (line 391-403):** add a row for octocode tools:

```text
| `mcp__octocode__githubSearchPullRequests` | — | ✓ rate-limited (1 call max, type-gated to bug/build/test) | — |
| `mcp__octocode__githubSearchCode` | — | ✓ optional per hypothesis-agent budget | — |
```

**Update the Will Not Do section (lines 415-425):** add one bullet:

```text
- Cite an octocode `[CROSS-REPO-PATTERN]` as load-bearing evidence in the Diagnosis section. Cross-repo patterns are precedent and may inform hypothesis selection, but the chosen fix must always cite a local `file:line` or a diagnostic command output. The `evidence-validator` agent (Wave 5 step 3) MUST verify that every Evidence-section citation is a local path, not a GitHub permalink.
```

**Why this is the right diff:**

- Octocode is gated 3 ways: by `--type`, by issue-content heuristic (recognizable error fragment), and by framework identifiability. This stops octocode from firing on every troubleshoot invocation.
- Rate limit is 1 call (vs Tavily's 2) because the Search API is more constrained (30/min, per research lines 162-164).
- The new artifact `wave3-octocode-patterns.md` follows the same pattern as `doc-context.md` from Wave 1.5 — separate file, structured, lazy-loaded by agents.
- Critically: cross-repo patterns are explicitly demoted to "precedent, not evidence." This preserves the hallucination contract from troubleshoot SKILL.md:24 — only local `file:line` citations count. The `evidence-validator` (Wave 5 step 3) is updated to enforce this.
- The fallback path is "empty index file with literal sentinel string" — agents can read it unconditionally without branching, matching the Wave 1.5 `no_docs_found` pattern.

---

### sc-brainstorm Wave 2A

**Target:** `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, Wave 2A enrichment routing matrix (lines 179-187).

**Current Wave 2A enrichment routing matrix (lines 181-187):**

```text
   | Condition | Action | Output |
   |-----------|--------|--------|
   | `domain ∈ {code, architecture, incident}` AND NOT `--no-codebase` | Invoke `/sc:analyze <relevant-paths> --focus quality --depth quick` OR `mcp__auggie__codebase-retrieval` for quick scan | `enrichment/codebase-context.md` |
   | `--codebase` (forced) | Same as above regardless of domain | Same |
   | `--research light` OR (auto: topic mentions framework/library names not in project) | Invoke `Skill sc-research-protocol` with `--depth quick` (or `/sc:research` if standalone) | `enrichment/research-light.md` |
   | `--research deep` OR (auto: `--strategy enterprise` + novel topic) | Invoke `Skill tech-research` with topic | `enrichment/research-deep.md` |
   | Otherwise | Skip enrichment | — |
```

**Proposed Wave 2A enrichment routing matrix (insert a new row between the codebase and research-light rows):**

```text
   | Condition | Action | Output |
   |-----------|--------|--------|
   | `domain ∈ {code, architecture, incident}` AND NOT `--no-codebase` | Invoke `/sc:analyze <relevant-paths> --focus quality --depth quick` OR `mcp__auggie__codebase-retrieval` for quick scan | `enrichment/codebase-context.md` |
   | `--codebase` (forced) | Same as above regardless of domain | Same |
   | `domain ∈ {code, architecture}` AND `--strategy ∈ {enterprise, default}` AND NOT `--no-precedent` | Spawn ONE `Task` agent for cross-repo precedent. Tools allowed: `mcp__octocode__githubSearchRepositories` (max 1 call, find 3 similar projects in this space), `mcp__octocode__githubSearchCode` (max 2 calls, find pattern implementations across those repos), `mcp__octocode__githubGetFileContent` (max 3 calls, extract focused snippets). Agent prompt: "Find 3 production projects that have solved problems analogous to: <topic>. For each, identify the approach taken and link to a representative file with SHA. Output: ≤500 tokens summary." | `enrichment/precedent.md` |
   | `--research light` OR (auto: topic mentions framework/library names not in project) | Invoke `Skill sc-research-protocol` with `--depth quick` (or `/sc:research` if standalone) | `enrichment/research-light.md` |
   | `--research deep` OR (auto: `--strategy enterprise` + novel topic) | Invoke `Skill tech-research` with topic | `enrichment/research-deep.md` |
   | Otherwise | Skip enrichment | — |
```

**And update the token budget bullet (line 196) from:**

```text
3. **Token budget for enrichment**: ~3000 tokens total cap. Priority order if exceeded: codebase > research-light > research-deep. Truncate by priority.
```

**To:**

```text
3. **Token budget for enrichment**: ~3500 tokens total cap (raised by 500 to accommodate precedent enrichment). Priority order if exceeded: codebase > precedent > research-light > research-deep. Truncate by priority. Precedent is between codebase (highest) and research-light because it's cheap-per-token (max ~500 token summary) and high-uniqueness — it provides signal neither codebase nor research-light can.
```

**And update the quality-tier tracking bullet (lines 189-194) to list precedent:**

```text
2. **Quality-tier tracking** (mandatory per enrichment source):
   - `primary` — first-choice source ran cleanly
   - `fallback_1` — primary failed, used Serena (codebase), WebSearch (research), or Tavily search for OSS examples (precedent)
   - `fallback_2` — both primary and fallback_1 failed, used native Glob/Grep (codebase) or skipped (precedent)
   - `skipped` — enrichment not invoked
   - Record as `enrichment_used: [{source, quality_tier}, ...]` in state.
```

**And add a new entry to the failure-handling table (line 384-385):**

```text
| Codebase enrichment fails (Auggie down) | WARN, fall back to Serena `get_symbols_overview` (quality_tier=fallback_1) | Native Glob/Grep (quality_tier=fallback_2) |
| Research enrichment fails (Tavily down) | WARN, fall back to WebSearch (quality_tier=fallback_1) | Skip (quality_tier=skipped) |
| Precedent enrichment fails (octocode rate-limited or unavailable) | WARN, fall back to Tavily search with query "github.com <topic> example" (quality_tier=fallback_1) | Skip (quality_tier=skipped) |
```

**Why this is the right diff:**

- Octocode is gated on `domain ∈ {code, architecture}` — explicitly excluded for incident, product, ops, etc. Matches the fit-analysis's framing (line 124) that precedent is most useful for code+architecture brainstorms.
- The new strategy/flag gate `--strategy ∈ {enterprise, default}` AND `NOT --no-precedent` gives users a kill switch and limits the feature to non-light strategies. Quick brainstorms don't pay the precedent-fetch cost.
- Tool budget is tight: 1 + 2 + 3 = 6 octocode calls maximum per brainstorm, well under the 30/min Search API rate cap.
- The artifact `enrichment/precedent.md` lives alongside the existing enrichment files, matching the established pattern in lines 56-58 of the SKILL.md.
- Fallback to Tavily is explicit and graceful (matches the existing pattern for research enrichment failure).
- The token budget is raised by 500 specifically — small enough that it doesn't materially impact the brainstorm's overall cost profile, large enough to hold a useful precedent summary.

---

## Rollout Sequencing

**This is the A/B-test plan. The whole point of skill-level integration is that we can roll out one at a time and measure.**

### Phase 0 — Prerequisite (1 PR, ~50 LoC)

Add octocode to `MCP_SERVERS` registry in `src/superclaude/cli/install_mcp.py:29`. Pin to v14.2.0. Default-disabled (`required: False`). `LOG=false` and `TOOLS_TO_RUN=githubSearchCode,githubGetFileContent,githubSearchPullRequests,packageSearch,githubViewRepoStructure,githubSearchRepositories` per the research recommendations (lines 209-212). Document install in `docs/configuration/`.

This is the only step the fit-analysis and this proposal agree on. It's foundational; nothing else can ship until octocode is installable.

### Phase 1 — tech-research Phase 4 (1 PR, ~120 LoC)

Land the tech-research diff first because:

1. It is the lowest-risk skill to instrument. Phase 4 is already explicitly external-research, so adding a cross-repo path is a natural extension (not a new behavior).
2. Tech-research has the strongest existing quality gates (rf-analyst + rf-qa at Phase 3 and Phase 5, rf-qa-qualitative at Phase 6). If octocode produces garbage, those gates catch it before it reaches the user.
3. Deep-tier tech-research runs are infrequent (manual user invocation) — low blast radius for telemetry collection.
4. The artifacts (research files in `research/web-*.md`) are persistent and inspectable — easy to A/B compare quality.

**Metrics to measure during 2-week A/B:**

| Metric | Hypothesis to test |
|---|---|
| % of Phase 4 web research files containing `[OCTOCODE-VERIFIED <SHA>]` tags | ≥30% — demonstrates octocode is actually firing on the topic shapes we expect |
| % of synthesis files that cite an octocode finding | ≥20% — demonstrates findings are load-bearing, not vestigial |
| % of Phase 4 agents that hit the tool budget cap | <10% — confirms our caps are correctly sized |
| Median Phase 4 wall-clock (with vs without octocode) | ≤+30s — confirms acceptable latency cost |
| Median Phase 4 token cost (Claude tokens only) | ≤+5% — confirms cross-repo enrichment is not a token sink |
| qa-qualitative review verdict | No regression in PASS rate vs baseline |
| Octocode rate-limit hits per week | <2 — confirms tool budget caps protect the 30/min Search API ceiling |

**Decision gate after 2 weeks:** if 4 of 7 metrics pass, proceed to Phase 2. If <4 pass, iterate on the prompt template / topic routing rules before unblocking Phase 2.

### Phase 2 — sc-brainstorm Wave 2A (1 PR, ~60 LoC)

Land brainstorm second because:

1. Wave 2A is explicitly "partial-OK" (SKILL.md:173). Octocode failure cannot abort the brainstorm — the quality-tier system already handles this gracefully.
2. Brainstorms are short-lived; the value-per-token of an external precedent is higher than in long tech-research runs (less context overhead to amortize).
3. The new artifact (`enrichment/precedent.md`) is bounded to ~500 tokens, easy to A/B compare ("is the precedent useful?" is a quick read).

**Metrics to measure during 2-week A/B:**

| Metric | Hypothesis to test |
|---|---|
| % of brainstorm Wave 2A runs where precedent.md is non-empty | ≥40% on code/architecture-domain brainstorms — confirms octocode finds relevant patterns |
| % of proposal cards (Wave 2C) that cite precedent.md | ≥15% — confirms precedent feeds proposals, isn't just vestigial |
| Token cost delta vs baseline | ≤+300 tokens per brainstorm (within budget raise) |
| User-flagged false precedents (subjective review) | <5% — confirms quality of precedent matches |

**Decision gate:** if 3 of 4 pass, proceed to Phase 3.

### Phase 3 — sc-troubleshoot Wave 3 (1 PR, ~80 LoC)

Land troubleshoot last because:

1. Troubleshoot has the strictest hallucination contract (every claim cites real `file:line`). Octocode findings are explicitly NOT load-bearing — they are precedent only. This is the most subtle behavioral contract in the framework.
2. `evidence-validator` (Wave 5 step 3) needs to be updated to reject GitHub permalinks as Evidence citations — that's a non-trivial cross-cutting change.
3. The `--type` gating (only `bug | build | test`) is heuristic; Phase 1+2 telemetry will inform whether the heuristic is correct.

**Metrics to measure during 2-week A/B:**

| Metric | Hypothesis to test |
|---|---|
| % of Wave 3 runs that fire octocode | ≥50% on bug/build/test types — confirms type-gating is well-tuned |
| % of hypothesis cards that reference `[CROSS-REPO-PATTERN]` | ≥10% — confirms agents use the precedent |
| `evidence-validator` rejections of permalinks | 0 — confirms hypothesis agents respect the precedent-not-evidence contract |
| Tier 2 confidence-calibration scores | No regression vs baseline |
| User-reported "this fix worked" rate | No regression vs baseline; ideally +5% on bug/test |

**Decision gate:** if 4 of 5 pass, mark skill-level integration complete.

### Phase 4 (optional — deferred decision) — `sc:research` standalone

The fit-analysis ranks this #3 (score 36). This proposal defers it. The `sc:research` command already wraps `tech-research` internally — once Phase 1 lands, `sc:research` inherits the octocode integration transitively. Adding a separate `--mode github` flag is double-counting. Revisit only if telemetry shows direct `sc:research` invocations (not via `tech-research`) where octocode would clearly add value.

### Total scope across 4 PRs

| PR | LoC | Risk | Rollback cost |
|---|---|---|---|
| 0. MCP registration | ~50 | Negligible (opt-in) | Revert one dict entry |
| 1. tech-research Phase 4 | ~120 | Low (Phase 4 already external) | Revert prompt template + routing rule |
| 2. brainstorm Wave 2A | ~60 | Very low (partial-OK wave) | Revert one matrix row |
| 3. troubleshoot Wave 3 | ~80 | Medium (citation contract) | Revert MCP enrichment bullet + Will-Not-Do bullet |
| **Total** | **~310** | **Per-PR low-medium** | **Each PR independently revertible** |

Compare to the fit-analysis's agent-level path (~50 LoC in 1 PR, but with global blast radius and no per-skill A/B handle). Our path is 6× the LoC but each PR can be measured, debugged, and reverted independently — and the final system has 3 independent control surfaces, not 1.

---

## Pros (including controllability)

1. **Per-skill control of when octocode fires.** Each skill's author decides the topic shapes / type filters / domain filters that gate octocode. The agent does not opaquely route on the agent's own heuristic.
2. **Per-skill tool budget.** tech-research Phase 4 gets up to 15 octocode calls per investigation. brainstorm Wave 2A gets 6. troubleshoot Wave 3 gets 1. Agent-level integration cannot express these per-caller budgets.
3. **A/B testing is structurally trivial.** Land Phase 1, measure, land Phase 2, measure. The fit-analysis's agent-level path requires forking the agent or feature-flagging within the agent prompt — neither is clean.
4. **Hallucination contract is preserved.** troubleshoot's "every claim is local file:line" rule is enforced at the skill level via the updated evidence-validator behavior and the explicit Will-Not-Do bullet. Agent-level integration cannot enforce this — the agent doesn't know it's being called by troubleshoot.
5. **Fallback paths are explicit per skill.** tech-research falls back to Tavily-only Web Research. brainstorm falls back to Tavily search for OSS examples. troubleshoot just omits the cross-repo enrichment. Each fallback is appropriate to the skill's failure mode.
6. **Skills are the right altitude for the SHA-pinned permalink rule.** Every octocode citation must include a commit SHA (not `@main`) so the citation is reproducible. The skill enforces this in the agent prompt; the agent definition has no concept of "reproducible citation."
7. **Telemetry is observable per skill.** We can answer "is octocode adding value to tech-research?" independently from "is octocode adding value to troubleshoot?" Agent-level integration collapses these into one signal.
8. **Skill versioning + `make sync-dev`.** Each PR is a localized change to one skill file. CODEOWNERS for that skill review. Lint hooks catch regressions. The change is small enough to actually be read in review.
9. **The `--no-precedent` (brainstorm) / `--no-doc-discovery`-style (troubleshoot) opt-outs are natural skill-level flags.** Users who don't want octocode firing can disable per-skill without uninstalling the MCP.

---

## Cons (including duplication across skills)

1. **3× the LoC.** ~310 LoC across 3 skills vs ~50 LoC at one agent. Cost is real but front-loaded; future skills don't pay it.
2. **Some duplication in tool budget enforcement.** Each skill's prompt template repeats the "max N calls per tool" pattern. We could extract this to `refs/octocode-budget.md` and have each skill reference it, but that adds a new ref file. Initial proposal: accept the duplication; refactor if a 4th skill wants octocode.
3. **The Cross-Repo Research Agent Prompt template (tech-research) is ~80 lines of new content.** It's parallel to the existing Web Research Agent Prompt (~45 lines). Some content (Incremental File Writing Protocol) is verbatim duplicated. Initial proposal: accept the duplication; the templates are skill-internal and the duplication is bounded.
4. **3 PRs to land vs 1.** Slower time-to-first-octocode-result. Mitigation: Phase 1 (tech-research) alone is high-value and ships independently. Phases 2-3 are pure expansion.
5. **The fit-analysis's "downstream consumers inherit automatically" claim is genuinely true for the agent path.** If a future 6th skill calls `deep-research`, it inherits octocode immediately. With our path, the 6th skill author must explicitly opt in. We consider this a *feature* (explicit > implicit) but acknowledge it as a cost.
6. **Two paths could coexist long-term.** Nothing prevents adding octocode to `deep-research.md` *later* as a graduation step, once skill-level telemetry validates the integration. This proposal does not foreclose the agent-level path; it sequences it.
7. **Per-skill fallback policies are independent.** If they diverge in subtle ways (e.g., tech-research uses `[OCTOCODE-FALLBACK]` tag, troubleshoot uses different sentinel), downstream consumers (synthesis, evidence-validator) need to handle both. Initial proposal: standardize the tag once Phase 1 ships; before then, accept the divergence.

---

## What This Approach Cannot Do

1. **Cannot make octocode usable from agents that aren't called by skills.** Any standalone agent invocation (e.g., a user manually summoning `deep-research`) gets no octocode access. This proposal leaves `deep-research.md` pure. The fit-analysis path would address this; we explicitly do not.
2. **Cannot retroactively octocode-enable a 6th skill without writing skill-specific glue.** New skills need to add their own routing matrix row / Phase 4 routing rule / Wave 3 MCP enrichment bullet. The agent-level path is one change; ours is N.
3. **Cannot enforce a global tool-call budget across skills.** If tech-research and brainstorm run concurrently, they can collectively exhaust the GitHub Search API budget (30/min). Per-skill budgets are local. A global rate-limiter would require infrastructure work (e.g., a shared SQLite-backed token bucket) that is out of scope here. Mitigation: skills run mostly sequentially in practice; in 2 weeks of telemetry we observe how often this happens.
4. **Cannot expose octocode to ad-hoc Claude Code conversations.** Octocode is gated to skills. A user asking Claude Code "find similar repos that solve X" in a free-form chat will NOT get octocode automatically — they'd need to invoke `/sc:research` or `/sc:brainstorm`. We consider this acceptable: the framework is the affordance; ad-hoc usage is what raw `gh` CLI is for.
5. **Cannot solve the underlying supply-chain risk.** Octocode is bgauryy/Wix-owned, v14.x with 194 npm versions in <12 months, no co-maintainers. Skill-level integration doesn't change this — the same pinning + telemetry-opt-out + tool-whitelist applies. But limiting the integration to 3 skills means a future supply-chain incident affects 3 skill files instead of being baked into the agent that everything else routes through.

---

## Specific Risk Mitigations

1. **Citation contract preservation (troubleshoot).** The `evidence-validator` agent (Wave 5 step 3) must be updated to reject GitHub permalinks as Evidence citations. Add a unit test that feeds a draft REPORT.md containing a `[CROSS-REPO-PATTERN]` line in the Evidence section and verifies the validator strips it. Without this test, the contract erodes over time.

2. **Tool budget enforcement.** Each agent prompt declares "max N calls per tool" as a HARD CAP. We rely on the agent to honor this. Risk: agents sometimes ignore caps. Mitigation: track per-Phase-4 octocode call counts in the audit log (`research-notes.md` SUGGESTED_PHASES section appends `octocode_call_count`). After 2 weeks, audit: are agents respecting the cap? If not, escalate to programmatic enforcement (wrapper around the MCP tool call).

3. **Topic-routing miscalibration (tech-research Phase 4).** The 6-row routing table is heuristic. Risk: orchestrator routes "Best-practice survey of X" to Cross-Repo when Web Research would have served better. Mitigation: in Phase 1 metrics, track which routing rule fired per Phase 4 item. If any rule fires <10% of the time, it's vestigial; if any fires >70%, it's miscalibrated. Tune the routing in a follow-up patch.

4. **SHA-pinning compliance.** Octocode's `githubGetFileContent` accepts a `branch` parameter; agents sometimes default to `@main` or `@master` which is NOT reproducible. Mitigation: in the agent prompt, explicitly say "MUST pass a `branch=<SHA>` parameter where `<SHA>` comes from the prior `githubViewRepoStructure` or `githubSearchCode` call's response. A request without a SHA is a protocol violation." Add a unit test asserting prompt content includes this rule.

5. **Octocode rate-limit blowback.** GitHub Search API is 30/min, octocode's backoff is undocumented (research line 163). Risk: a Deep-tier tech-research run with 8 Phase 4 agents could collectively hit the cap. Mitigation: tool budget caps are sized to ensure 8 concurrent Phase 4 Cross-Repo agents max out at 8 × 3 = 24 githubSearchCode calls, leaving 6 calls/min headroom for other skill invocations. If telemetry shows we're hitting the cap, reduce per-agent budget from 3 to 2.

6. **Telemetry-opt-out compliance.** Research line 152 documents that octocode telemetry sends research goals + repo names to bgauryy's external server. Mitigation: the MCP registration (Phase 0) pins `LOG=false`. Add a `make verify-octocode-config` Makefile target that asserts `LOG=false` is set in the user's MCP config. Refuse to ship Phase 1 until this gate exists.

7. **`make verify-sync` discipline.** Each PR modifies a skill file in `src/superclaude/skills/`. After every edit, `make sync-dev` and `make verify-sync` must pass. Mitigation: include `make verify-sync` in CI gate; mark sync-failure as blocking.

8. **Octocode supply-chain pinning.** Pin to a specific version (v14.2.0 at time of writing). Document upgrade gates: any v15+ upgrade requires re-running the Phase 1-3 metrics regression suite. Without this, a silent backdoor (research line 142) could land via auto-update.

9. **Skill divergence over time.** Three skills will accumulate slightly different octocode usage patterns. Mitigation: at the 6-month mark, audit the three integrations and consider whether `refs/octocode-budget.md` and `refs/cross-repo-research-prompt.md` shared refs should be extracted.

---

## Test Plan

### Unit tests (per skill, in `tests/`)

1. **tech-research**:
   - `test_phase4_routing_rule_cross_repo_topic_shape` — feed a SUGGESTED_PHASES entry with topic "callsites of pydantic.Agent in OSS" and assert the orchestrator dispatches Cross-Repo Research Agent Prompt, not Web Research.
   - `test_phase4_routing_rule_official_docs_topic_shape` — feed "Official docs for httpx" and assert Web Research is dispatched.
   - `test_cross_repo_agent_prompt_includes_tool_budget` — load the prompt template, assert "max 3 githubSearchCode calls" string is present.
   - `test_cross_repo_agent_prompt_disables_local_tools` — assert "DISABLED for this prompt" string is present alongside `localSearchCode`.
   - `test_cross_repo_agent_prompt_requires_sha_pinning` — assert "SHA, not @main" string is present.

2. **sc-brainstorm**:
   - `test_wave2a_precedent_row_gated_on_domain` — assert that `domain=incident` does NOT route to precedent.
   - `test_wave2a_precedent_row_gated_on_strategy` — assert that `--strategy light` does NOT route to precedent.
   - `test_wave2a_precedent_row_respects_no_precedent_flag` — assert `--no-precedent` skips even on `domain=code`.
   - `test_wave2a_token_budget_raised_to_3500` — assert the token-budget bullet states 3500.

3. **sc-troubleshoot**:
   - `test_wave3_mcp_enrichment_gated_on_type_bug` — `--type=bug` enables octocode.
   - `test_wave3_mcp_enrichment_skipped_on_type_performance` — `--type=performance` skips octocode.
   - `test_wave3_hypothesis_card_template_allows_cross_repo_pattern_tag` — assert the template accepts `[CROSS-REPO-PATTERN]` lines in the rationale section.
   - `test_evidence_validator_rejects_github_permalinks_in_evidence_section` — feed a draft REPORT.md with a permalink in `## Evidence`, assert it's stripped.

### Integration tests (in `tests/integration/`)

1. **End-to-end tech-research Deep tier with octocode mocked.**
   Mock the octocode MCP to return canned `githubSearchCode` results. Run a Deep-tier tech-research invocation. Assert:
   - Phase 4 produces ≥1 web research file with `[OCTOCODE-VERIFIED <SHA>]` tag
   - Phase 5 synthesis files contain the SHA-pinned citation
   - Phase 6 qa-qualitative does NOT flag the citation as fabricated

2. **End-to-end brainstorm with octocode mocked.**
   Mock the octocode MCP. Run a Wave 2A enrichment with `domain=code`. Assert:
   - `enrichment/precedent.md` is non-empty
   - The seed-brief's `## Enrichment Context` section references the precedent
   - Wave 2C proposal cards can cite the precedent

3. **End-to-end troubleshoot Tier 2 with octocode mocked.**
   Mock octocode. Run a Tier 2 troubleshoot on a `--type=bug` issue. Assert:
   - `wave3-octocode-patterns.md` is generated
   - Hypothesis agents reference the patterns with `[CROSS-REPO-PATTERN]` tag
   - The final REPORT.md's Evidence section contains ONLY local `file:line` citations (no GitHub permalinks)

### Smoke tests (manual, run after each PR lands)

1. Run `/sc:research "How does httpx implement retries"` (Phase 1) — manually inspect the resulting research file for an octocode citation.
2. Run `/sc:brainstorm "design a rate-limiting decorator" --strategy default` (Phase 2) — manually inspect `enrichment/precedent.md` for ≥1 relevant project.
3. Run `/sc:troubleshoot --type bug "RuntimeError: Event loop is closed in asyncio"` (Phase 3) — manually inspect `wave3-octocode-patterns.md` for ≥1 relevant PR archaeology link.

### Telemetry assertions (per-skill, post-launch)

Each skill's audit log gains a structured comment block per the existing pattern (e.g., `<!-- SC:TROUBLESHOOT:SUMMARY ... -->`). Add:

```text
octocode_calls: <N>
octocode_call_breakdown: searchCode=<N>,searchPRs=<N>,packageSearch=<N>,getFile=<N>,viewStructure=<N>,searchRepos=<N>
octocode_rate_limit_hits: <N>
octocode_fallback_invoked: <bool>
```

A nightly script aggregates these from `.dev/troubleshoot/`, `.dev/tasks/to-do/TASK-RESEARCH-*/`, and `.dev/brainstorm/` audit logs. Output: `.dev/metrics/octocode-weekly.md`. Used as input to the decision gates between phases.

---

## Effort Estimate

| Phase | Description | LoC | Engineering hours | Calendar weeks |
|---|---|---|---|---|
| 0 | MCP registration in `install_mcp.py` + docs | ~50 | 2 | 0.5 |
| 1 | tech-research Phase 4 diff + Cross-Repo Research Agent Prompt template + unit tests + integration test | ~120 + ~80 test | 8 | 1.0 |
| 1-A | 2-week A/B telemetry collection + metrics analysis | 0 | 4 | 2.0 |
| 2 | brainstorm Wave 2A row + budget bump + quality-tier update + unit tests + integration test | ~60 + ~50 test | 5 | 0.75 |
| 2-A | 2-week A/B telemetry collection + metrics analysis | 0 | 3 | 2.0 |
| 3 | troubleshoot Wave 3 MCP enrichment bullet + Cross-Repo Pattern Index artifact + evidence-validator update + unit tests + integration test | ~80 + ~70 test | 8 | 1.0 |
| 3-A | 2-week A/B telemetry collection + metrics analysis | 0 | 3 | 2.0 |
| **Total** | | **~510 (incl. tests)** | **33 hours** | **9.25 weeks** |

Compared to the fit-analysis's path (1 PR, ~50 LoC, ~6 hours, 1 week):
- This approach is **5.5× the engineering hours** and **9× the calendar time**
- This approach delivers **3 independent A/B-validated integrations** vs **1 global integration with no per-caller telemetry**
- This approach has **3 independent revert points** vs **1 all-or-nothing revert**

**Recommendation:** The slower path is the correct path for a framework with downstream consumers, hallucination contracts, and rate-limited external services. Speed-to-first-octocode is not the constraint; correctness and observability are.

---

## Open questions for the merge stage

1. Should the Cross-Repo Research Agent Prompt template be extracted to `src/superclaude/skills/tech-research/refs/cross-repo-research-prompt.md` so other skills could reuse it later, or kept inline?
2. Should the per-skill `--no-octocode` flag be a single framework-wide env var (`SUPERCLAUDE_NO_OCTOCODE=1`) instead of per-skill flags, to make global opt-out easier?
3. For the evidence-validator update (Wave 5 step 3 in troubleshoot), do we update the validator's prompt in-place or add a new validator variant? In-place is simpler but couples concerns; new variant is cleaner but adds an agent.
4. The fit-analysis suggests `sc:research` as a separate integration target (#3, score 36). This proposal defers it. Should we revisit by Phase 3?
5. If Phase 1 telemetry shows octocode tool-budget violations are common, do we escalate to programmatic enforcement (wrapper agent that counts calls and aborts), or accept the violations and re-budget?

---

**End of proposal 06.**
