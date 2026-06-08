# Brainstorm 02: Behavioral Router Integration

**Lens:** BEHAVIORAL ROUTER — embed explicit, deterministic routing logic in
`deep-research.md` so any LLM (Opus, Sonnet, Haiku) can pick the right tool
from query signals alone, with rate-limit fallback chains baked in.

**Target file:** `src/superclaude/agents/deep-research.md`
**Diff size estimate:** +180 / -8 lines, single-file change.

---

## Lens

The current `deep-research.md` Tool Selection Policy (lines 30-51) is a
**prose policy** — "Tavily-first rule", "fall back when…", "never silent
fallback". That style works for Opus 4.7 but is structurally weak for three
reasons:

1. **Prose is interpretable.** Sonnet and Haiku read the same prose and
   reach different conclusions about "is this query about a library?"
   vs. "is this query about a GitHub pattern?". The agent's behavior
   becomes model-dependent.
2. **Octocode has 5 tools, not 1.** Adding it as "axis 4" the way the
   declarative-purist proposal does still leaves the LLM to decide *which*
   of `githubSearchCode`, `packageSearch`, `githubSearchPullRequests`,
   `githubViewRepoStructure`, `githubGetFileContent` to fire — and in what
   order. Prose policy gives the LLM no scoring rubric.
3. **Rate limits are a routing event, not an error.** The 30 req/min
   GitHub Search ceiling (research §4.3) means octocode WILL get throttled
   on any deep-tier run. A prose policy that says "fall back if it fails"
   ignores that the agent needs a *pre-emptive* degradation plan once it
   has seen N octocode calls in the current session.

A **behavioral router** addresses all three: it converts the policy from
prose into a **signal → tool → fallback chain** decision tree, plus a
**rate-budget tracker**. The cost is +120 lines of explicit rules; the
payoff is model-invariant behavior and graceful degradation.

The router lives in `deep-research.md` because that's where the existing
Tool Selection Policy already lives — colocating it preserves the agent's
single-file ergonomics and is the smallest delta that achieves the lens's
goal.

---

## Routing Decision Tree

The router runs **once per research hop**. A "hop" = one logical question
the agent decides to investigate (the existing Workflow step 3 already
talks about "hops").

```text
┌──────────────────────────────────────────────────────────────────────┐
│ INPUT: research hop (a question + optional source URLs/repo hints)   │
└──────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────────┐
        │ Step 1: SIGNAL EXTRACTION                 │
        │ Run regex/keyword detectors on hop text   │
        │ Output: signal set ⊆ {URL, PKG, GH_REPO,  │
        │   PR, LIB_NAME, ERROR_MSG, REAL_USAGE,    │
        │   CURRENT_EVENT, LOCAL_FILE, CONCEPT}     │
        └───────────────────────────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────────┐
        │ Step 2: PRIMARY TOOL SELECTION            │
        │ Apply Trigger Matrix (see §Trigger Matrix)│
        │ Pick highest-confidence match.            │
        │ If tie, prefer cheapest tier (LOCAL >     │
        │ DOCS > GH_SEARCH > WEB_SEARCH).           │
        └───────────────────────────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────────┐
        │ Step 3: BUDGET CHECK                      │
        │ If primary tool is octocode/githubSearch* │
        │ AND session_gh_search_count ≥ 20:         │
        │   → DEMOTE primary to fallback-1          │
        │ (Pre-emptive: leaves 10 req/min headroom  │
        │ for the next 2 hops.)                     │
        └───────────────────────────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────────┐
        │ Step 4: EXECUTE w/ FALLBACK CHAIN         │
        │ Call primary. On failure (see §Failure    │
        │ Classifier), advance one step in the      │
        │ tool's fallback chain.                    │
        └───────────────────────────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────────┐
        │ Step 5: RECORD ROUTING DECISION           │
        │ Append to citation table: signal set,     │
        │ primary tool, fallback events, backend.   │
        └───────────────────────────────────────────┘
```

The five signals are extracted by pattern, not LLM judgment:

| Signal | Detection pattern (case-insensitive) |
|---|---|
| `URL` | Hop text contains `https?://` |
| `PKG` | Phrases: `package X`, `npm X`, `pypi X`, `pip install X`, `import X from`, backticks around lowercase token that looks like a package |
| `GH_REPO` | `github.com/<owner>/<repo>` literal, OR `<owner>/<repo>` token where owner is known (langchain-ai, anthropic, vercel, etc.) |
| `PR` | Phrases: `PR #N`, `pull request`, `merged`, `why was X changed`, `commit history`, `archaeology` |
| `LIB_NAME` | Hop names a library / framework / SDK by canonical name (React, Django, httpx, etc.) without ambiguity |
| `ERROR_MSG` | Hop contains a stack trace, error class name (`*Error`, `*Exception`), HTTP status code |
| `REAL_USAGE` | Phrases: `real examples`, `in the wild`, `how do real projects`, `production examples`, `actual implementations` |
| `CURRENT_EVENT` | Phrases: `latest`, `recent`, `as of <date>`, `current best practice`, `2026`, names a release date |
| `LOCAL_FILE` | Hop references a path under `src/`, `tests/`, `.dev/`, or any path that exists in the current repo |
| `CONCEPT` | None of the above — pure conceptual question ("what is X", "how does Y work in principle") |

---

## Trigger Matrix

Each row is a complete routing rule: signal pattern → primary tool →
confidence → fallback chain. Confidence levels are HIGH (deterministic,
unambiguous), MED (signal-rich but tool choice has 2+ reasonable options),
LOW (signal-sparse, primary is a guess).

| # | Signal pattern | Primary tool | Confidence | Fallback chain |
|---|---|---|---|---|
| R1 | `PKG` AND NOT `LOCAL_FILE` | `mcp__octocode__packageSearch` | **HIGH** | → `mcp__context7__resolve-library-id` → `mcp__tavily__tavily-search` |
| R2 | `GH_REPO` AND NOT `PR` | `mcp__octocode__githubViewRepoStructure` | **HIGH** | → `mcp__octocode__githubGetFileContent` (if hop names a file) → `mcp__tavily__tavily-extract` (with constructed github.com URL) → `WebFetch` |
| R3 | `GH_REPO` AND `PR` | `mcp__octocode__githubSearchPullRequests` | **HIGH** | → `Bash:gh pr list` → `mcp__tavily__tavily-search` site-filtered to github.com |
| R4 | `REAL_USAGE` AND (`LIB_NAME` OR `PKG`) | `mcp__octocode__githubSearchCode` | **HIGH** | → `mcp__tavily__tavily-search` (with `site:github.com`) → `WebSearch` |
| R5 | `LIB_NAME` AND NOT (`REAL_USAGE` OR `GH_REPO`) | `mcp__context7__resolve-library-id` → `mcp__context7__query-docs` | **HIGH** | → `mcp__tavily__tavily-search` (with library name + "docs") → `mcp__octocode__packageSearch` (last-ditch — find the repo to read the README) |
| R6 | `URL` AND single URL in hop | `mcp__tavily__tavily-extract` | **HIGH** | → `WebFetch` |
| R7 | `ERROR_MSG` | `mcp__tavily__tavily-search` (verbatim error + library name) | **MED** | → `mcp__octocode__githubSearchPullRequests` (search closed PRs for fix) → `mcp__octocode__githubSearchCode` (find the raise site) → `WebSearch` |
| R8 | `CURRENT_EVENT` AND NOT (`PKG` OR `GH_REPO`) | `mcp__tavily__tavily-search` (`time_range: "month"`) | **HIGH** | → `WebSearch` → octocode only if event is a release/version question |
| R9 | `LOCAL_FILE` | **DELEGATE** — not this agent's job; emit instruction to caller: "use auggie or serena" | **HIGH** | (no fallback — refuse rather than degrade) |
| R10 | `CONCEPT` only | `mcp__sequential-thinking__sequentialthinking` (decompose) → R1-R8 on each sub-question | **MED** | n/a — meta-rule |
| R11 | No signal extracted OR multiple HIGH conflicts | `mcp__tavily__tavily-search` (broad query) | **LOW** | → `WebSearch`; re-run signal extraction on the top result snippet |

**Tie-breaking precedence** (when two HIGH rows match):
`R9 > R6 > R3 > R2 > R1 > R4 > R5 > R7 > R8 > R10 > R11`. Local-file delegation
(R9) always wins; URL-extraction (R6) wins over keyword-based rules; octocode
specific-target rules (R1-R4) outrank octocode generic search; Context7
(R5) outranks Tavily for known libraries; Tavily outranks WebSearch
because it's the project's tavily-first standard.

---

## Concrete Implementation in `deep-research.md`

Replace the current "Tool Selection Policy" section (lines 30-51) with the
following. This is the literal markdown the change would emit. The
"Tavily-first" rule is preserved as **R8/R11 base behavior**, so the
existing semantics still hold for queries that don't trigger octocode
rules.

```markdown
## Tool Selection Policy

Deep-research uses a **behavioral router** to select tools deterministically
from query signals. Run the router once per research hop; record the
routing decision in the citation table. Do not deviate from the matrix
unless the rule's HIGH-confidence pattern fails to match the hop, in which
case fall through to R11 (broad search).

### Step 1 — Extract signals

Pattern-match the hop text against the signal table below. A hop may
produce multiple signals (e.g., `LIB_NAME + REAL_USAGE`). Empty signal set
falls through to R11.

| Signal | Detection pattern |
|---|---|
| `URL` | Hop text contains `https?://` |
| `PKG` | "package X", "npm X", "pypi X", "pip install X", `import X from`, backticked lowercase token |
| `GH_REPO` | `github.com/<owner>/<repo>` literal, or `<owner>/<repo>` token with known owner |
| `PR` | "PR #N", "pull request", "merged", "why was X changed", "commit history", "archaeology" |
| `LIB_NAME` | Names a library/framework/SDK unambiguously (React, Django, httpx, etc.) |
| `ERROR_MSG` | Stack trace, `*Error`, `*Exception`, HTTP status code |
| `REAL_USAGE` | "real examples", "in the wild", "production examples", "how do real projects" |
| `CURRENT_EVENT` | "latest", "recent", "as of <date>", "current best practice", explicit year |
| `LOCAL_FILE` | References a path under `src/`, `tests/`, `.dev/`, or any path in the current repo |
| `CONCEPT` | None of the above — pure conceptual question |

### Step 2 — Apply the trigger matrix

| # | When | Primary | Fallback chain |
|---|---|---|---|
| R1 | `PKG` AND NOT `LOCAL_FILE` | `mcp__octocode__packageSearch` | → `mcp__context7__resolve-library-id` → `mcp__tavily__tavily-search` |
| R2 | `GH_REPO` AND NOT `PR` | `mcp__octocode__githubViewRepoStructure` | → `mcp__octocode__githubGetFileContent` → `mcp__tavily__tavily-extract` → `WebFetch` |
| R3 | `GH_REPO` AND `PR` | `mcp__octocode__githubSearchPullRequests` | → `Bash:gh pr list` → `mcp__tavily__tavily-search` site-filtered |
| R4 | `REAL_USAGE` AND (`LIB_NAME` OR `PKG`) | `mcp__octocode__githubSearchCode` | → `mcp__tavily__tavily-search` site:github.com → `WebSearch` |
| R5 | `LIB_NAME` AND NOT (`REAL_USAGE` OR `GH_REPO`) | `mcp__context7__query-docs` | → `mcp__tavily__tavily-search` "docs" → `mcp__octocode__packageSearch` |
| R6 | Single `URL` in hop | `mcp__tavily__tavily-extract` | → `WebFetch` |
| R7 | `ERROR_MSG` | `mcp__tavily__tavily-search` (verbatim) | → `mcp__octocode__githubSearchPullRequests` → `mcp__octocode__githubSearchCode` → `WebSearch` |
| R8 | `CURRENT_EVENT` AND NOT (`PKG` OR `GH_REPO`) | `mcp__tavily__tavily-search` (`time_range: "month"`) | → `WebSearch` |
| R9 | `LOCAL_FILE` | **REFUSE** — return to caller: "use auggie or serena" | (no fallback) |
| R10 | `CONCEPT` only | `mcp__sequential-thinking__sequentialthinking` to decompose, then re-run router on each sub-hop | n/a |
| R11 | No signal OR HIGH-conflict | `mcp__tavily__tavily-search` (broad) | → `WebSearch` |

**Tie-breaking precedence:** R9 > R6 > R3 > R2 > R1 > R4 > R5 > R7 > R8 > R10 > R11.

### Step 3 — Budget-aware demotion

Track `session_gh_search_count` = total calls to any `mcp__octocode__*Search*`
tool in this session. Before executing a primary that begins with
`mcp__octocode__`:

- If `session_gh_search_count < 20` → execute primary.
- If `20 ≤ session_gh_search_count < 28` → execute primary but emit a
  warning in the citation table (`budget: warning`).
- If `session_gh_search_count ≥ 28` → **demote** to fallback-1 (skip
  primary entirely). Record `routing_demotion: gh_budget_exhausted`.

The 30 req/min GitHub Search ceiling is the binding constraint
(see octocode research §4.3). The 28-call cutoff leaves 2 req/min headroom
for retries.

### Step 4 — Failure classifier

A primary call counts as "failed" (and triggers fallback) when:

- Transport-level error (timeout, connection refused, 5xx) **twice** for
  the same query.
- Explicit rate-limit / quota-exceeded error.
- Authentication error (missing/invalid API key / PAT).
- Tool returns empty result AND hop has HIGH-confidence signal that
  predicted a non-empty result (e.g., `PKG` signal + `packageSearch`
  empty = package likely doesn't exist on npm/PyPI → fall back to
  Context7 / Tavily).

**Not a failure:** A non-empty but low-relevance result. The agent must
evaluate relevance and either accept or run a refined query against the
same tool (not advance the fallback chain).

### Step 5 — Record the routing decision

Every citation table row must include:

| Field | Example |
|---|---|
| `signal_set` | `[PKG, REAL_USAGE]` |
| `rule_fired` | `R4` |
| `primary_tool` | `mcp__octocode__githubSearchCode` |
| `backend_used` | `mcp__octocode__githubSearchCode` (or fallback name) |
| `fallback_events` | `[]` or `[{from: octocode, reason: rate_limit, to: tavily}]` |
| `budget_state` | `ok | warning | demoted` |

This replaces the prior "Never silent fallback" rule with a structured
record per source.
```

(End of replacement section.)

The frontmatter also gains the five octocode tools:

```yaml
tools:
  - mcp__tavily__tavily-search
  - mcp__tavily__tavily-extract
  - WebSearch
  - WebFetch
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
  - mcp__octocode__githubSearchCode           # NEW
  - mcp__octocode__githubGetFileContent       # NEW
  - mcp__octocode__githubSearchPullRequests   # NEW
  - mcp__octocode__packageSearch              # NEW
  - mcp__octocode__githubViewRepoStructure    # NEW
  - Read
  - Grep
  - Glob
  - mcp__sequential-thinking__sequentialthinking
  - Bash  # NEW — for R3 gh CLI fallback
```

---

## Rate-Limit Handling

The router's Step 3 (budget-aware demotion) is the *primary* rate-limit
defense — it prevents hitting the 30 req/min ceiling at all on a single
deep-tier run by demoting after 20 calls and forcing fallback after 28.
This is **pre-emptive** rather than reactive.

When pre-emption fails (e.g., the agent is invoked twice in close
succession from two different skills, or another tool consumed the GH
budget in parallel), the **reactive** fallback chain handles it:

1. Octocode returns 403 / rate-limit error.
2. Step 4 classifies as failure → advance fallback chain.
3. For R1 (packageSearch): → Context7 resolves the library → query its
   docs. This is often a *better* result than octocode would have given,
   because Context7 returns canonical documentation rather than source
   code grep results.
4. For R4 (githubSearchCode): → Tavily search with `site:github.com`
   filter. This loses octocode's structured pagination and `lineHint`
   guarantees, but recovers the surface-level "find me code in GitHub
   that matches X" capability.
5. For R3 (searchPullRequests): → `Bash: gh pr list` shells out to the
   already-authed `gh` CLI. This bypasses the MCP transport entirely and
   uses the user's separate rate budget — clean separation.

**Budget reset:** The session counter does not auto-reset. If the operator
runs `/sc:save` and `/sc:load`, the new session starts at zero. There is
**no time-based reset** inside the router — that's the LLM's job to
estimate, and overestimating is safer than underestimating.

**Telemetry note:** Per the octocode research §4.2, `LOG=false` should be
set at install time (MCP registration phase). The router assumes this is
already done; it does not attempt to enforce telemetry settings.

---

## Pros

- **Model-invariant.** A Haiku-class model running this matrix produces
  the same tool choice as Opus, because every rule is a pattern match,
  not a judgment call. (Test: see Test Plan §1.)
- **Explicit rate-limit handling.** Pre-emptive demotion at 20 calls,
  reactive fallback at the actual error. The agent never silently bursts
  past the ceiling and gets blocked mid-investigation.
- **Audit trail.** Step 5's structured citation row gives operators a
  per-source forensics record — they can re-run the same hop manually and
  validate whether the router picked correctly.
- **Composes with existing Tavily-first rule.** R8/R11 are literally
  "use Tavily for current events / unknown queries", so the agent's
  existing reputation for Tavily-as-primary holds for the long tail. The
  router *adds* octocode-aware behavior only where signals are clear.
- **Forward-compatible.** New rules can be added as new rows in the
  trigger matrix without restructuring the agent. If a 5th MCP server
  joins later, the same pattern applies.
- **Single-file change.** Lives entirely in `deep-research.md`. No new
  skills, no new agents, no hooks.

---

## Cons

- **+120 lines in one agent definition.** The agent file goes from ~70
  lines to ~190. Reading-time cost on every invocation = ~600 tokens of
  context tax just for the agent surface (before any tool schema is
  loaded). This is acceptable for `deep-research` but would be expensive
  if replicated across every research-style agent.
- **Pattern detection is fragile.** Regex/keyword rules are brittle vs.
  natural language. A hop phrased as "what does the pydantic library
  actually do under the hood" would trigger `LIB_NAME` but might *also*
  trigger `REAL_USAGE` if the agent over-reads "actually do". The
  tie-breaking precedence handles this, but the rule will sometimes pick
  the "wrong" tool from a human standpoint.
- **No learning loop.** The router is static. It does not learn from
  prior hops in the session ("the last 3 R5 calls all required fallback
  to Tavily — maybe Context7 is down today"). Adding that would require
  per-session state beyond the call counter.
- **Tie-breaking precedence is opinionated.** Why does R3 (PRs) outrank
  R2 (repo structure)? Because the lens picked it. A different lens
  might disagree. The order is documented but not derived.
- **Budget counter is global to the session, not the agent invocation.**
  If two parallel `deep-research` agents both share the same session,
  they double-count or under-count. (Mitigation: in parallel-spawn
  contexts, the orchestrator should pass `--gh_search_budget N` as a
  param. The router schema is ready for this but the implementation
  hooks aren't.)
- **Refusal in R9 might be unexpected.** A user who asks
  `deep-research` "find references to `foo()` in src/" today gets a
  best-effort answer (probably a Grep). After this change, the router
  refuses and tells them to use auggie. That's the correct behavior per
  the lens, but it's a behavior change.

---

## What This Approach Cannot Do

- **Cannot make octocode itself more reliable.** The router only routes;
  if octocode's underlying GitHub Search API is degraded, the router will
  detect failure and fall through, but won't recover the data octocode
  would have returned. Tavily site-filtered search is a 60–70% recovery,
  not 100%.
- **Cannot prevent over-fetch.** If the agent chooses to issue 5
  parallel `githubSearchCode` calls within R4 (each a separate hop), the
  router counts each call but doesn't enforce intra-hop parallelism
  limits. The 28-call budget gets hit faster than expected. (Mitigation:
  a future Step 3.5 could add "per-hop max 2 octocode searches".)
- **Cannot serve as the *only* policy.** The router covers tool *choice*
  per hop. It does not cover credibility scoring, source de-duplication,
  citation synthesis, or "is this answer complete enough to stop?". The
  rest of `deep-research.md`'s Workflow section (lines 53-68) handles
  those concerns and is preserved unchanged.
- **Cannot route based on *cost*.** R1-R11 don't account for "this query
  would take 8 octocode tool calls vs. 1 Tavily call". A future
  enhancement could add an `estimated_tool_calls` column to the matrix.
- **Cannot replace human override.** If the operator's prompt explicitly
  says "use Tavily for this", the router does not check that. The agent
  is still responsible for honoring explicit overrides as a higher
  precedent than R1-R11.

---

## Specific Risk Mitigations

| Risk (from octocode research §4) | Router-level mitigation |
|---|---|
| §4.1 Supply-chain (bgauryy bus factor, @latest install) | Router does not change install; relies on MCP registration phase to pin v14.2.0 (per fit-analysis Phase A). If MCP install is misconfigured, the router still works — falls through to Tavily for everything because tools are absent from the surface. **Failure mode: degraded, not catastrophic.** |
| §4.2 Telemetry leakage (research goals → external server) | Router does not transmit additional data. It DOES record signal sets in the citation table, but that's local-only. Sensitive operators should set `LOG=false` at install. The router could also gate R1/R4 on a per-hop `--no-telemetry-tools` flag in a future enhancement. |
| §4.3 GitHub API rate limits (30 req/min Search) | **Direct mitigation:** Step 3 budget tracking + Step 4 reactive fallback. This is the lens's strongest contribution. |
| §4.4 Context tax (8–17k tokens for octocode schema) | Router only loads the 5 cross-repo tools listed in the frontmatter (per fit-analysis recommendation to whitelist). The 9 local/LSP tools are excluded → context tax drops to ~3–5k. |
| §4.5 LSP language gaps | Router never picks an LSP tool. R9 refuses local-file questions outright → LSP irrelevance for `deep-research`. |
| §4.6 Limited community validation | Router treats octocode as *one tool among several*, not the default. R8 (Tavily) and R11 (broad Tavily) catch the long tail. If octocode underperforms in production, the operator's exit cost is removing 5 rows from the trigger matrix. |

---

## Test Plan

### §1 — Cross-model determinism (the lens's headline test)

Run the same 10 example queries through 3 model classes (Opus 4.7,
Sonnet 4.6, Haiku 4) with only the `deep-research.md` agent surface
loaded. For each query, capture the first tool invoked. Pass criterion:
**identical tool choice across all 3 models for ≥9/10 queries.**

If any model disagrees on >1 query, the router is under-specified for
that case — refine the rule.

### §2 — The 10 example queries and expected routing

| # | Hop text | Signal set extracted | Rule fired | Expected primary tool |
|---|---|---|---|---|
| 1 | "What does the `httpx` package actually do?" | `PKG`, `LIB_NAME` | R1 (PKG > LIB_NAME by precedence) | `mcp__octocode__packageSearch` |
| 2 | "Show me 3 production examples of `pydantic-ai` agent registration" | `PKG`, `LIB_NAME`, `REAL_USAGE` | R4 (REAL_USAGE+PKG dominates R1) | `mcp__octocode__githubSearchCode` |
| 3 | "Why did langchain change their tool calling API in PR #1234?" | `GH_REPO` (langchain known owner), `PR` | R3 | `mcp__octocode__githubSearchPullRequests` |
| 4 | "What is React's `useEffect` cleanup function?" | `LIB_NAME` | R5 | `mcp__context7__query-docs` |
| 5 | "How does async work in Python in principle?" | `CONCEPT` | R10 | `mcp__sequential-thinking__sequentialthinking` (decompose) |
| 6 | "Extract the changelog from https://github.com/vercel/next.js/releases/tag/v15.0.0" | `URL`, `GH_REPO` | R6 (URL > GH_REPO by precedence) | `mcp__tavily__tavily-extract` |
| 7 | "What's the latest best practice for FastAPI dependency injection as of 2026?" | `LIB_NAME`, `CURRENT_EVENT` | R8 (CURRENT_EVENT dominates R5 because "latest" implies non-canonical-docs answer) | `mcp__tavily__tavily-search` (`time_range: "month"`) |
| 8 | "Find references to the `ConfidenceChecker` class in src/superclaude/pm_agent/" | `LOCAL_FILE` | R9 | **REFUSE** — emit "use auggie or serena" |
| 9 | "I'm getting `TypeError: cannot pickle '_thread.RLock' object` when using multiprocessing.Pool — has anyone fixed this?" | `ERROR_MSG`, `LIB_NAME` (multiprocessing) | R7 | `mcp__tavily__tavily-search` (verbatim error) |
| 10 | "Compare hydration strategies between react and vue" | `LIB_NAME` (multiple), no `REAL_USAGE` | R5 (decompose into 2 sub-hops, each runs R5) | `mcp__context7__query-docs` per library |

**Tie-breaking trace for query #6:** Both R6 (URL) and R2 (GH_REPO) match HIGH. Precedence says R6 > R2 → Tavily extract wins. This matches user intent ("extract the changelog" = read the page, not browse the repo).

**Tie-breaking trace for query #1:** R1 and R5 both HIGH. R1 > R5. The router picks packageSearch, which returns `httpx` → `encode/httpx` repo URL → the agent then runs a follow-up hop with `GH_REPO` signal → R2 fires. Two-step plan, intentional.

### §3 — Rate-limit simulation

Mock the octocode MCP to return 403 rate-limit after the 10th call.
Verify:

- Calls 1–20 run as primary (R1, R2, R3, R4 as triggered).
- Call 11 returns 403 → Step 4 classifies as failure → fallback chain
  executes → next call uses fallback (e.g., Tavily for R4).
- Call 21 (if reached) → Step 3 emits `budget: warning` but still runs
  primary.
- Call 29 (if reached) → Step 3 demotes pre-emptively, primary is
  skipped, fallback-1 runs directly. Citation row records
  `routing_demotion: gh_budget_exhausted`.

### §4 — Single-file diff validation

Run `make verify-sync` after editing `src/superclaude/agents/deep-research.md`.
Confirm `.claude/agents/deep-research.md` regenerates correctly.

Run the existing deep-research test suite (`uv run pytest tests/agents/test_deep_research*.py` if present, else manual smoke test via `/sc:research`-style invocation) and confirm no regression on Tavily-only queries (R8, R11 paths).

### §5 — Refusal behavior (R9)

Invoke `deep-research` with a hop that contains a local path token. Confirm
the agent emits a structured refusal pointing to auggie/serena rather than
attempting a Grep. This is a behavior change — document it in the
agent's README / changelog entry.

### §6 — Citation table schema

Verify the citation table emitted by Workflow step 5 includes the new
fields (`signal_set`, `rule_fired`, `primary_tool`, `backend_used`,
`fallback_events`, `budget_state`). Update any downstream consumer that
parses the citation table (search for "Sources table" references in
skills that ingest `deep-research` output).

---

## Effort Estimate

| Task | Effort |
|---|---|
| Author the replacement `## Tool Selection Policy` section in `src/superclaude/agents/deep-research.md` | 1.5 h |
| Update frontmatter `tools:` list (add 5 octocode tools + Bash) | 5 min |
| Run `make sync-dev` + `make verify-sync` | 5 min |
| Author Test Plan §1 cross-model determinism harness (3 queries × 3 models = 9 runs) | 2 h |
| Author Test Plan §3 rate-limit simulation (mock octocode MCP) | 2 h |
| Manual smoke test of all 10 example queries (Test Plan §2) | 1 h |
| Update citation table schema in any downstream consumer skills | 1 h |
| Documentation: changelog entry + brief note in `KNOWLEDGE.md` | 30 min |
| **Total** | **~8 h (one focused day)** |

**Prereqs (separate effort, blocks this work):**

- MCP server registration in `install_mcp.py` per fit-analysis #5
  (~30 min).
- Operator install: `superclaude mcp --servers octocode` + set
  `LOG=false` env (~10 min).

**Reversibility:** The change is a single-file diff. Revert =
`git revert <sha>`. No data migration, no schema lock-in. If the router
turns out to be wrong, the prior prose policy is two commits away.

---

## Closing note on the lens

The behavioral router is not the *cheapest* way to wire octocode into
`deep-research` — the declarative-purist approach (just add tools to
frontmatter and let the LLM figure it out) is ~10 lines instead of ~180.
The router is justified only if you believe that **model-invariant
behavior** and **explicit rate-limit handling** matter more than minimal
LoC. For an agent that gets invoked by every research-style skill in the
framework, that trade-off is favorable. For a one-off command, it would
not be.
