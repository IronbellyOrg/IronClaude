# Brainstorm 01: Declarative Purist Integration

## Lens

**Declarative Purist** — The integration is *exclusively* a frontmatter update and a textual extension of the existing "Tool Selection Policy" section in `src/superclaude/agents/deep-research.md`. No new agents. No new hooks. No new routing code. No new sub-skills. No Python helpers. The LLM that already reads the agent definition is trusted to apply the prose policy, because that is *precisely* what the existing definition format is designed for.

**Why this is defensible:**

1. The current `deep-research.md:30-36` Tool Selection Policy is itself prose that the LLM follows. It already encodes a 3-axis decision tree (Tavily / WebSearch fallback / Context7) entirely in markdown. Adding a 4th axis is a like-for-like extension — the *same* mechanism that has demonstrably worked for the Tavily-first rule.
2. The fit-analysis (Score 45, Cost⁻¹ 5/5) calls out "Pure declarative change (~15 lines in one file). No new code paths. The Tool Selection Policy pattern is already in place." This proposal takes that observation literally.
3. PR audit time is **the** governance constraint when adopting a high-risk dependency (bus-factor-1, 194 npm versions in <12 months, telemetry leakage). A reviewer must be able to read the entire change, understand what it does, and verify that nothing is "smuggled in" via code. A declarative-purist diff is the only shape that survives that audit in 5 minutes.
4. Reversibility: a future PR can delete the added tools from frontmatter + delete the added policy section, and the agent returns to its current 3-axis behavior. No state, no cache, no DB migration, no hook un-registration. This is the maximally reversible integration.
5. The cost of *every* other lens (router, persona, hook, sub-agent) is **forever** — even if octocode is dropped in 6 months because bgauryy's npm account is compromised, you'd still be ripping out routing code, hook handlers, or a sub-agent file. The declarative-purist lens leaves nothing behind on removal.

The trade-off you accept under this lens: you cannot mechanically enforce rate-limit fallback, you cannot mechanically guarantee the LLM picks the right tool, and you cannot mechanically prevent telemetry leakage in-session. Those are environment / install-time concerns, handled at MCP-server-registration time (Phase A of the fit-analysis rollout — out of scope for this brainstorm) — not at agent-definition time.

---

## Proposed Implementation

**Files touched: 1.**

`src/superclaude/agents/deep-research.md` — frontmatter `tools:` list extended with 5 octocode tools, and the `## Tool Selection Policy` section extended with a 4th axis describing when to pick octocode vs Tavily vs Context7 vs auggie vs serena.

That is the entire change set under this lens. No edits to:

- `install_mcp.py` — out of scope for this brainstorm (Phase A precursor, handled separately)
- Any skill SKILL.md — downstream consumers (`tech-research`, `troubleshoot`, `brainstorm`) inherit the new axis automatically because they all delegate to `deep-research`. That propagation is the whole *point* of editing the workhorse agent.
- Any hook in `.claude/settings.json` — no new behavioral triggers
- Any agent other than `deep-research` itself

**Specific line targets** (against current `src/superclaude/agents/deep-research.md`):

| Line range | Edit type | Purpose |
|---|---|---|
| Line 1-16 (frontmatter block) | Insert 5 `tools:` entries before line 15 (`mcp__sequential-thinking__sequentialthinking`) | Expose octocode tools to the agent's tool surface |
| Line 3 (description) | Append clause about cross-repo code research via octocode | Surface the new capability in the agent description (so callers know it's there) |
| Line 30-36 (Tool Selection Policy block) | Replace section header from "### Tavily-first rule (web search / extraction)" + add new `### Octocode for cross-repo code research` subsection between the Tavily-first rule and "### Detecting Tavily unavailable" | Add the 4th axis with explicit trigger phrases and explicit *anti*-triggers |
| End of "Tool Selection Policy" section (currently line 51) | Insert new `### Detecting "octocode unavailable"` subsection mirroring the Tavily fallback pattern | Tells the LLM what to do when octocode rate-limits or fails auth |

---

## Concrete Diff Sketch

Here is what the agent file looks like **after** the change. Original lines 1-16 (frontmatter) and 30-51 (Tool Selection Policy) are shown verbatim where unchanged, with `+` markers for inserts:

```yaml
 ---
 name: deep-research
-description: Adaptive research specialist for external knowledge gathering. Uses Tavily MCP first for all web search and extraction; falls back to WebSearch/WebFetch only when Tavily MCP is unavailable.
+description: Adaptive research specialist for external knowledge gathering. Uses Tavily MCP first for web search/extraction; Context7 for canonical library docs; octocode MCP for cross-repo GitHub/GitLab/Bitbucket source-code patterns, package→repo resolution, and PR archaeology. Falls back to WebSearch/WebFetch only when Tavily MCP is unavailable.
 category: analysis
 tools:
   - mcp__tavily__tavily-search
   - mcp__tavily__tavily-extract
   - WebSearch
   - WebFetch
   - mcp__context7__resolve-library-id
   - mcp__context7__query-docs
+  - mcp__octocode__githubSearchCode
+  - mcp__octocode__githubGetFileContent
+  - mcp__octocode__githubViewRepoStructure
+  - mcp__octocode__githubSearchPullRequests
+  - mcp__octocode__packageSearch
   - Read
   - Grep
   - Glob
   - mcp__sequential-thinking__sequentialthinking
 ---
```

And the Tool Selection Policy section (current lines 30-51) gains a new sub-section between the Tavily-first rule and the Tavily fallback detection logic, plus a parallel fallback-detection subsection at the end. Diff against the current section header is structural; full replacement text is shown in the next section.

---

## Tool Selection Decision Logic (added to agent policy text)

The full proposed replacement for the `## Tool Selection Policy` section (current lines 30-51 in `deep-research.md`):

```markdown
## Tool Selection Policy

This agent operates across four research axes. Pick the correct axis from the *shape* of the question before issuing any tool call.

### Axis 1 — Tavily-first rule (web search / extraction)

1. **Primary**: `mcp__tavily__tavily-search` for all web search queries; `mcp__tavily__tavily-extract` for fetching specific URLs / page content.
2. **Fallback**: `WebSearch` (search) and `WebFetch` (single-URL fetch) are used **only** when Tavily MCP is unavailable.

### Axis 2 — Context7 for canonical library/framework/SDK documentation

`mcp__context7__resolve-library-id` → `mcp__context7__query-docs` remains primary for **maintainer-published** documentation. Examples: "How do I configure a Next.js middleware?", "What's the Prisma migrate command?", "Show me the Stripe SDK's webhook verification API". Context7 returns canonical docs, not source code.

### Axis 3 — Octocode for cross-repo GitHub source-code patterns

Use the octocode tools when the question is shaped like **"how do real projects actually implement X"** or **"what does package Y do internally"** — i.e. questions answered by *reading other repositories' source code*, not by reading docs and not by reading our own repo.

**Trigger phrases** (use octocode when the user / upstream skill asks):

- "how does package X actually implement Y" → `packageSearch(X)` → `githubViewRepoStructure(owner/repo)` → `githubSearchCode("Y")` → `githubGetFileContent(matched paths)`
- "show me N real production examples of Z" → `githubSearchCode(query="Z", limit=N)` → fan-out `githubGetFileContent` reads, grouped by repo
- "what changed in this PR / why was this change made" → `githubSearchPullRequests(repo=owner/X, query=...)` → inspect diffs + comments
- "find the upstream repo for npm/PyPI package P" → `packageSearch(P)` → returns repo URL, version, deprecation status
- "compare how React vs Vue vs Svelte solve hydration" → bulk `githubViewRepoStructure` + targeted `githubSearchCode` across N repos
- "find GitHub issues / PRs from similar projects that match this error signature" → `githubSearchPullRequests` + issue-shaped queries

**Canonical octocode flow (the "Funnel Method"):** DISCOVER → SEARCH → LOCATE/ANALYZE → READ. Start with `packageSearch` or `githubViewRepoStructure` to get the repo + path skeleton. Use `githubSearchCode` to find candidate matches (it returns `lineHint`-style snippets). Only then call `githubGetFileContent` with `charOffset` / `charLength` for surgical extraction. Never start with `githubGetFileContent` on a path you haven't first discovered — that pattern burns context.

**Mandatory `researchGoal` + `reasoning` fields:** Octocode requires both on every call. Treat them as required prose, not boilerplate. Each `researchGoal` should be a one-sentence statement of what fact you are trying to extract. Each `reasoning` should explain *why this specific tool call advances that goal*. This is octocode's Research Driven Development contract and the LLM must honor it. Empty / generic values ("research the code") defeat the agent's audit trail.

**Anti-triggers — DO NOT pick octocode when:**

- The question is about the **local codebase** (`/config/workspace/IronClaude/` and its children). Use `mcp__auggie__codebase-retrieval` (free, low-token, indexed) for semantic local search; use `mcp__serena__find_symbol` / `find_referencing_symbols` for symbol-level local navigation; use `Read` / `Grep` / `Glob` for direct file reads. Auggie is HIGHEST PRIORITY for local context per project CLAUDE.md and is faster than any GitHub round-trip.
- The question is about **canonical library documentation** (e.g. "what does `useEffect` do" or "how do I configure Tailwind"). Use Context7 (Axis 2). Source code is not docs — reading `react/src/ReactHooks.js` to answer "what does useEffect do" is the wrong axis.
- The question is about **general web content** (blog posts, conference talks, vendor announcements, current events). Use Tavily (Axis 1). Octocode does not index the open web.
- The question is about **a single specific file in a known location in a known repo where the user already gave you the path**. Use `Read` (if local) or `githubGetFileContent` directly — `packageSearch` and `githubViewRepoStructure` are wasted hops in that case.

**Whitelisted tool surface for octocode:**

This agent exposes only 5 octocode tools: `githubSearchCode`, `githubGetFileContent`, `githubViewRepoStructure`, `githubSearchPullRequests`, `packageSearch`. The agent must not assume any `local*` or `lsp*` octocode tool is available — those overlap with serena / auggie / Read and were intentionally not added to this agent's frontmatter. If a workflow tempts you toward `localSearchCode` or `lspGotoDefinition`, switch axes back to auggie / serena instead.

### Axis 4 — Sequential for multi-step synthesis

`mcp__sequential-thinking__sequentialthinking` remains the synthesis backbone for combining findings across axes. It is not a research source; it is the reasoning glue.

### Detecting "Tavily unavailable"

Treat Tavily MCP as unavailable, and fall back to WebSearch/WebFetch, when **any** of the following holds:

- The `mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract` tools are not present in the available tool surface for this session (not loaded / not configured).
- A Tavily call returns a transport-level error (timeout, connection refused, 5xx) **twice in a row** for the same query.
- A Tavily call returns an explicit rate-limit / quota-exceeded error.
- A Tavily call returns an authentication error (missing/invalid API key).

In every fallback event, record in the source citation table: `fallback_reason: <tavily_missing | tavily_error | tavily_rate_limit | tavily_auth>`.

### Detecting "octocode unavailable"

Treat octocode MCP as unavailable when **any** of the following holds:

- The `mcp__octocode__*` tool names are not present in the available tool surface for this session (server not installed / not loaded).
- A call returns a GitHub Search API rate-limit error (HTTP 403 with rate-limit headers, or octocode's wrapped equivalent). The GitHub Search API limit is **30 req/min** — this *will* be hit during fan-out workloads.
- A call returns an authentication error (missing/invalid `GITHUB_TOKEN`, or `gh auth` not configured).
- A call returns a transport-level error (timeout, 5xx) **twice in a row** for the same query.

When octocode is unavailable, **fall back to Tavily** with a GitHub-targeted search query (e.g. `site:github.com <query>`), and record in the citation table: `fallback_reason: <octocode_missing | octocode_rate_limit | octocode_auth | octocode_error>`. Do **not** silently substitute auggie for octocode — they answer different questions (local vs cross-repo).

If rate-limited, also note in the report's "Open questions / suggested follow-up" section that the GitHub Search budget was exhausted, so the operator can decide whether to retry in the next minute or accept the Tavily fallback.

### Never silent fallback

Always state in the report which research backend was used per source. If fallback occurred (Tavily → WebSearch, or octocode → Tavily), note it in the "Open questions / suggested follow-up" section so the operator knows the primary tool was not exercised.
```

The key load-bearing pieces of prose for the LLM:

1. **Shape-of-question routing** — "Pick the correct axis from the *shape* of the question before issuing any tool call." This forces a planning step before tool calls, mirroring the existing Workflow step 2 ("Plan").
2. **Trigger phrases** — explicit example queries paired with explicit tool chains. The LLM pattern-matches the user's question against these phrases.
3. **Anti-triggers** — 4 explicit "do not use octocode when" clauses that cover the *exact* overlap surfaces called out in the research doc (local codebase → auggie, library docs → Context7, web → Tavily, known specific file → Read).
4. **Whitelisted tool surface paragraph** — disambiguates which octocode tools are available (only the 5 cross-repo ones) and explicitly instructs the LLM not to attempt the redundant ones, *even if it remembers them from training*.
5. **Mandatory researchGoal + reasoning** — codifies octocode's RDD contract so the LLM doesn't fill those fields with junk.
6. **Octocode-unavailable fallback** — mirrors the Tavily-fallback section symmetrically, gives the LLM a concrete rule for what to do under HTTP 403, missing tool, or auth failure.

---

## Pros

Specific to the Declarative Purist lens:

- **5-minute PR review.** Single file diff. Reviewer reads the frontmatter additions (5 lines) and the policy section additions (~70 lines of prose). No code to audit, no test harness to evaluate, no behavioral side-effects to reason about. The reviewer asks one question: "Does this prose correctly describe when to use octocode?" That is a markdown-grade review, not a code-grade review.
- **Maximally reversible.** Removal is one `git revert` away. No state to migrate, no hook to unregister, no MCP routing layer to peel apart. If octocode supply-chain risk materializes (bgauryy npm account compromise, breaking v15 release, unmaintained for 6 months), removal is *trivial*.
- **Propagates automatically.** Because `tech-research`, `tech-reference`, `troubleshoot`, `brainstorm`, and other downstream skills delegate research to the `deep-research` agent, this single edit changes the behavior of *all* downstream consumers without per-skill PRs. The fit-analysis explicitly calls this out as the reason this target scored highest (Value 5/5).
- **No new failure modes introduced at the framework level.** The only new failure mode is "octocode call failed" — and the prose teaches the LLM to fall back to Tavily with `site:github.com`. No new exception handling, no new retries, no new logging.
- **Honors the existing pattern.** The Tavily-first rule and Tavily-fallback detection logic already exist as prose. Adding octocode as a parallel axis follows exactly the same pattern — same shape of trigger rules, same shape of fallback rules. A reviewer who has audited the Tavily section can audit the octocode section by structural analogy.
- **Trust-the-LLM is empirically validated for this surface.** The current Tavily-first rule *works* — the deep-research agent reliably picks Tavily over WebSearch. There is no reason to believe the LLM cannot apply a 4-axis policy when it already applies a 3-axis one.
- **Future-proofs against octocode's own evolution.** When octocode adds a 15th tool, or renames a tool, the agent definition needs *only* prose edits — never code edits. Hook-driven or routing-driven approaches would need code rewrites for each octocode upgrade.
- **No new context tax in skills that don't use octocode.** Only consumers that actually trigger the deep-research agent pay the cost. Skills that bypass deep-research (e.g. local-only flows like cleanup-audit) see zero impact.

---

## Cons

Specific to the Declarative Purist lens:

- **Cannot mechanically enforce rate-limit fallback.** If the LLM ignores the "fall back to Tavily on HTTP 403" instruction, there is no code-level guardrail to catch it. We rely on the LLM honoring the policy text. *Mitigation*: the fallback prose is structurally identical to the Tavily-fallback prose, which has empirically worked. *Residual risk*: real.
- **Cannot mechanically prevent the LLM from picking octocode for the wrong axis.** A poorly-phrased user question ("what does useEffect do") could trigger octocode when Context7 is correct. *Mitigation*: the anti-triggers list is explicit and uses the exact phrasing of likely-bad queries. *Residual risk*: nonzero, but no different from current 3-axis ambiguity.
- **Cannot block telemetry leakage in-session.** Octocode telemetry (Issue #321 Finding #2: research goals + repo names sent to external server, opt-out via `LOG=false`) is an environment-variable concern handled at MCP server registration time. The agent definition cannot enforce `LOG=false`. *Mitigation*: handled in Phase A (install_mcp.py registration), out of scope for this proposal.
- **Cannot version-pin octocode from the agent definition.** Pinning to `octocode-mcp@14.2.0` happens in `install_mcp.py`. If a user installs with `@latest`, the agent definition has no way to refuse — it just calls whatever tools are present. *Mitigation*: out of scope, handled at registration.
- **Cannot enforce the `TOOLS_TO_RUN` whitelist.** The agent definition can list only 5 tools in its frontmatter, but if the MCP server exposes all 14 tools, the LLM *could* try to call (e.g.) `mcp__octocode__localSearchCode` if it remembers the name. Frontmatter is a per-agent allowlist, not a global ban. *Mitigation*: the policy text explicitly tells the LLM "do not assume any `local*` or `lsp*` tool is available" — relies on LLM compliance.
- **Cannot A/B test outcomes.** Because there is no instrumentation, there is no way to compare "with-octocode" vs "without-octocode" research quality empirically. The change either works (subjective operator judgment) or it doesn't. *Mitigation*: out of scope; A/B harness is a separate concern.
- **Prose policy bloat.** The Tool Selection Policy section grows from ~20 lines to ~100 lines. Future axes (octocode v2, alternative cross-repo tools) would push it further. There is a long-term readability ceiling around 5-6 axes. *Mitigation*: at that point, refactor into a sub-doc; not relevant for a single addition.
- **No place for octocode-specific telemetry in the report.** The synthesis report format (lines 59-66) doesn't currently distinguish octocode-sourced findings from Tavily-sourced ones beyond the `backend` column. *Mitigation*: the existing `backend` column already accepts `tavily|websearch|webfetch|context7` — extending to `octocode` is implicit. (Minor edit to the example report block in the Workflow section may also be warranted; included optionally.)

---

## What This Approach Cannot Do

Honest enumeration:

- **Cannot route based on session state.** If a previous turn already used octocode and got rate-limited, the LLM only knows this if it remembers it in context. No persistent state.
- **Cannot orchestrate parallel octocode + Tavily for the same query.** Wave-pattern parallelism would require a sub-skill or routing layer. This proposal's LLM chooses one axis at a time per sub-question. Parallel multi-axis fan-out would be a different lens.
- **Cannot enforce `researchGoal` / `reasoning` quality.** The prose says "treat them as required prose, not boilerplate", but there is no validator. The LLM may still fill `researchGoal: "research"`.
- **Cannot pre-emptively limit GitHub Search API consumption.** A deep-tier research run could plausibly fan out 10+ `githubSearchCode` calls. The 30 req/min cap *will* throttle. The prose tells the LLM what to do when throttled, but doesn't prevent the throttling.
- **Cannot guard against telemetry / supply-chain risk at the agent layer.** Those are install-layer (Phase A) concerns. This proposal scope-limits to the agent layer.
- **Cannot benefit consumers that bypass `deep-research`.** Skills like `cleanup-audit` that operate purely on local repo don't go through `deep-research` and won't see any octocode behavior. (This is correct — those skills don't *need* octocode.)
- **Cannot retrofit historical research artifacts.** Existing research markdown files in `.dev/tasks/` won't gain citations to octocode-sourced findings. Going-forward only.
- **Cannot prevent the LLM from hallucinating an octocode tool name** that doesn't exist (e.g. `mcp__octocode__searchEverywhere`). The frontmatter is the only allowlist; if the LLM invents a name, the MCP server will reject the call, but the LLM may waste a turn discovering that.

---

## Specific Risk Mitigations

Concrete handling for the 4 risks named in the prompt:

### Rate limits (GitHub Search API: 30 req/min)

- **Prose:** The Axis 3 anti-triggers explicitly route local-codebase queries away from octocode (so they never hit the search budget). The "Detecting octocode unavailable" subsection codifies HTTP 403 + rate-limit-error as a fallback trigger, with Tavily `site:github.com` as the named alternative.
- **What this cannot do:** Cannot batch / debounce / pre-budget calls. A deep-tier run that legitimately needs 10 cross-repo searches will burn through the minute budget. The prose tells the LLM to *expect* this, fall back gracefully, and note it in the open-questions section so the operator can decide whether to retry.
- **Out of scope:** Per-session call counter, per-skill budget caps, automatic 60-second backoff. Those belong in a routing layer (different lens).

### Auth failures

- **Prose:** Auth failure is one of 4 trigger conditions in "Detecting octocode unavailable" (missing/invalid `GITHUB_TOKEN`, or `gh auth` not configured). The fallback target is the same as for rate-limits: Tavily with a GitHub-targeted search.
- **What this cannot do:** Cannot prompt the user to run `gh auth login`. The LLM observes the failure, falls back, and logs the fallback_reason. Operator must notice the report's open-questions note and act.

### Telemetry leakage

- **Acknowledged out-of-scope:** Telemetry opt-out is `LOG=false` env var, set at MCP server registration time. The agent definition cannot enforce it.
- **What the agent CAN do:** The prose tells the LLM that `researchGoal` is sent to octocode's telemetry endpoint (implicitly — the LLM has the Stage-1 research doc as context if invoked with it). For sensitive queries, the LLM is instructed in the report-format step (Workflow step 5) to redact sensitive entity names before issuing octocode calls — but only when the operator pre-declares the query is sensitive. Default is "telemetry on, behave as if public".
- **Strong recommendation in the corresponding PR description:** "This PR assumes Phase A registration set `LOG=false`. If `LOG=false` is not set, telemetry will receive research goals and repo names. Do not merge this PR without Phase A first."

### Version pinning

- **Acknowledged out-of-scope:** Pinning is `install_mcp.py` (`command: npx -y octocode-mcp@14.2.0`).
- **What the agent CAN do:** The frontmatter lists 5 specific tool names. If a future octocode renames `packageSearch` to `npmSearch`, the agent will silently lose that capability (the renamed tool won't be in the allowlist) — which is *desirable* fail-safe behavior, vs. the wildcard alternative.
- **Documented expectation in PR:** "Tool names in this frontmatter are pinned to octocode-mcp v14.2.0. Any version bump must re-verify each name and update the frontmatter accordingly. See `feedback_pr_target_fork_only.md` for the version-bump gate."

---

## Test Plan

How to validate this works, *without* writing code:

### Pre-merge validation (manual, ~30 min)

1. **Markdownlint pass:** Run `make lint` after sync — the agent file must parse cleanly. (`make sync-dev` first to propagate to `.claude/`.)
2. **Frontmatter parse check:** Spawn a one-shot Claude Code session and ask it to list `deep-research` agent's tools. All 14 tools (9 existing + 5 new octocode) should appear.
3. **Trigger-phrase walkthrough:** For each of the 6 trigger phrases in the proposed policy text, pose a query that matches the phrase to a Claude Code instance that has loaded this agent, and observe whether it picks octocode. Pass criterion: ≥5/6 correctly route to octocode on first attempt.
4. **Anti-trigger walkthrough:** For each of the 4 anti-trigger clauses, pose a query that matches the anti-trigger, and observe whether the agent picks the correct alternative axis (auggie / Context7 / Tavily / Read). Pass criterion: 4/4 correctly route *away* from octocode.
5. **Fallback walkthrough:** Simulate octocode-unavailable by removing `octocode` from the MCP server registry temporarily; pose a trigger-phrase query; observe whether the agent falls back to Tavily with a `site:github.com` query and records the fallback in the citation table. Pass criterion: fallback fires, citation column reads `octocode_missing`.

### Post-merge regression checks (passive)

6. **Existing tech-research outputs.** Re-run an existing tech-research task (one from `.dev/tasks/`) and diff the resulting research markdown against the prior run. The new run should still produce a Tavily-sourced bulk of findings *plus* octocode-sourced findings where the question involves cross-repo code patterns. Pass criterion: no regression in Tavily / Context7 coverage; new octocode-sourced rows present where appropriate.
7. **Citation table integrity.** Verify the `backend` column in newly generated research reports correctly identifies sources as `octocode` vs `tavily` vs `context7` vs `webfetch`. Pass criterion: every row has a non-empty `backend` value.

### Tests deliberately NOT included

- Unit tests on the agent file (markdown — not testable as code).
- Integration tests against the live octocode MCP server (rate-limit-sensitive, would burn CI budget, and the *agent definition* isn't what they'd test — they'd test octocode itself).
- A/B comparison harness (out of scope; would require instrumentation that this lens explicitly disclaims).

---

## Effort Estimate

| Dimension | Estimate |
|---|---|
| Files touched | 1 (`src/superclaude/agents/deep-research.md`) |
| Lines added | ~95 (5 frontmatter + 1 description + ~89 policy prose) |
| Lines deleted | ~3 (description rewrite, section-header reshape) |
| Net diff | ~+90 lines |
| Author time | 30-45 min (most time is policy-prose drafting) |
| Reviewer time | 5 min (single-file markdown review) |
| `make sync-dev` runs | 1 |
| `make verify-sync` runs | 1 (pre-commit) |
| Tests to write | 0 |
| Test plan execution time (manual) | 30 min |
| Total PR cycle | ~1.5 hr author + 5 min review |

**Prerequisites (NOT part of this PR):**

- Phase A: octocode registered in `install_mcp.py` with pinned version `@14.2.0`, `LOG=false`, `TOOLS_TO_RUN` whitelist of the 5 cross-repo tools, `GITHUB_TOKEN` documented. (Separate PR, separate brainstorm.)
- Operator has run `superclaude mcp --servers octocode` and verified the MCP server is healthy.

**Reversibility cost:** ~5 minutes — `git revert` the single commit, `make sync-dev`, push. No state to undo.

**Forward compatibility:** If octocode is later replaced by another cross-repo tool (e.g. `code-graph-mcp`), only Axis 3 prose + frontmatter tool names need editing. The 4-axis structure is the *durable* abstraction.

---

## Summary

This proposal does exactly one thing: it teaches the existing `deep-research` agent — via prose policy alone — when to pick octocode and when not to. No new code, no new agents, no new hooks. The change is auditable in a single PR by a markdown-grade reviewer in 5 minutes, removable in a single revert, and propagates automatically to every downstream consumer of the `deep-research` agent. The trade-off accepted is that supply-chain, rate-limit, and telemetry enforcement live at the MCP-server-registration layer (Phase A), not at the agent-definition layer. That is the correct seam: agents describe *intent*, registration describes *trust boundary*.
