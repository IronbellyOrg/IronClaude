# Brainstorm — Target #4: sc-brainstorm Wave 2A Enrichment

**Date:** 2026-05-30
**Target file:** `/config/workspace/IronClaude/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` (lines 171-200 — Wave 2A behavioral block) + `/config/workspace/IronClaude/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` (lines 1-86 — `§Enrichment-Sources`)
**Question framed:** *What is the most beneficial way to integrate octocode into Wave 2A enrichment of the brainstorm protocol?*
**Stage:** 3 of 3 — parallel `/sc:brainstorm` agent #4 of 5
**Score from fit-analysis (Stage 2):** 32/45 — "Strong fit" (rank #4 overall)

---

## Target Context

### What Wave 2A actually does (quoted from current code)

Wave 2A is the **parallel, partial-OK enrichment phase** that runs after Wave 1 (Socratic dialogue → `seed-brief.md`) and before Wave 2B (agent-spec composition). Its declared purpose, from `SKILL.md:172`:

> "Parallel enrichment fetches. Failures degrade quality but do not abort."

Three core behavioral mechanisms govern this wave:

#### 1. The routing matrix (SKILL.md:179-187)

```text
| Condition | Action | Output |
|-----------|--------|--------|
| `domain ∈ {code, architecture, incident}` AND NOT `--no-codebase` | Invoke `/sc:analyze <relevant-paths> --focus quality --depth quick` OR `mcp__auggie__codebase-retrieval` for quick scan | `enrichment/codebase-context.md` |
| `--codebase` (forced) | Same as above regardless of domain | Same |
| `--research light` OR (auto: topic mentions framework/library names not in project) | Invoke `Skill sc-research-protocol` with `--depth quick` (or `/sc:research` if standalone) | `enrichment/research-light.md` |
| `--research deep` OR (auto: `--strategy enterprise` + novel topic) | Invoke `Skill tech-research` with topic | `enrichment/research-deep.md` |
| Otherwise | Skip enrichment | — |
```

#### 2. Quality-tier tracking (SKILL.md:189-194)

```text
- `primary` — first-choice source ran cleanly
- `fallback_1` — primary failed, used Serena (codebase) or WebSearch (research)
- `fallback_2` — both primary and fallback_1 failed, used native Glob/Grep
- `skipped` — enrichment not invoked
- Record as `enrichment_used: [{source, quality_tier}, ...]` in state.
```

This is reified in the **return contract** at `SKILL.md:346-348`:

```yaml
enrichment_used:
  - source: codebase | research-light | research-deep
    quality_tier: primary | fallback_1 | fallback_2 | skipped
```

#### 3. Fail-open semantics (SKILL.md:200)

> "Wave proceeds even if all sources failed (degraded mode). Emit: `Wave 2A complete: enrichment done (sources: <X>, degraded: <Y>).`"

And from the error matrix (`SKILL.md:384-385`):

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| Codebase enrichment fails (Auggie down) | WARN, fall back to Serena `get_symbols_overview` (quality_tier=fallback_1) | Native Glob/Grep (quality_tier=fallback_2) |
| Research enrichment fails (Tavily down) | WARN, fall back to WebSearch (quality_tier=fallback_1) | Skip (quality_tier=skipped) |

#### 4. Token budget cap (SKILL.md:196)

> "Token budget for enrichment: ~3000 tokens total cap. Priority order if exceeded: codebase > research-light > research-deep. Truncate by priority."

#### 5. Cascaded ref — `handoff-routing.md` §Enrichment-Sources (lines 5-67)

The matrix-row routing is *also* defined in the cascaded ref. The behavioral block in SKILL.md is the summary; the ref is the authoritative tier ladder. Any integration MUST modify *both files in tandem*. The ref defines the Tier 1/2/3 ladders per source, exact tool calls (two parallel auggie queries with specific prompts), per-source budgets, and explicit fallback chain ordering.

### What this means for octocode integration

The integration surface is narrow and well-defined:

- **A row** in the SKILL.md matrix (one literal-table edit)
- **A subsection** under `§Enrichment-Sources` in the ref (one append)
- **A quality-tier entry** in the return contract (one enum extension)
- **An error-matrix row** (one append)
- A new artifact path: `enrichment/<something>.md`

All of these are **declarative** — no new code, no state machine changes, no orchestration logic. The fail-open semantics already protect against octocode flakiness, rate-limits, or supply-chain shocks (downgrade to `skipped` and proceed).

---

## The Integration Question

> What is the most beneficial way to integrate octocode into Wave 2A enrichment of the brainstorm protocol, given:
>
> 1. Wave 2A is **already parallel and fail-open**, so adding a fourth enrichment lane is structurally cheap
> 2. Octocode's killer feature is **cross-repo precedent discovery** (`how have other projects solved this?`) — exactly the gap in current Wave 2A, which only inspects the local codebase + general web search
> 3. The 3000-token enrichment budget and 30/min GitHub Search API ceiling are the binding constraints
> 4. The fit-analysis (Stage 2) scored this target at Value=4, Cost⁻¹=4, Risk⁻¹=4 (Total=32). Wave 2A is the *only* one of the top-4 targets where octocode lands without touching `deep-research` or `tech-research`

The question splits into three sub-questions:

- **Where in the matrix?** A new row, a new column, an annotation on the existing codebase row, or a new wave entirely?
- **What triggers it?** Domain-only, strategy-only, flag-gated, opt-in, opt-out?
- **What does it produce?** A precedent-search artifact, a per-proposal annotation, a Wave-3 ammunition cache, or a unified "external evidence" file?

The seven Wave 1 candidates below explore these dimensions.

---

## Wave 1: Divergent Ideation

### Candidate A — Drop-in matrix row (the "minimum-viable" path)

Add a single new row to the Wave 2A routing matrix:

```text
| `domain ∈ {code, architecture}` AND NOT `--no-precedent` | Invoke `Task: octocode-precedent-search` with the topic | `enrichment/precedent.md` |
```

The `octocode-precedent-search` task runs `githubSearchCode` + `packageSearch` against the topic keywords, producing a single artifact summarizing 3-5 cross-repo references. Quality tier is `primary` if octocode runs cleanly; `skipped` if it fails (no fallback). Triggers in **parallel with the existing codebase row**, not as a replacement.

**Rationale:** Mirrors the existing pattern exactly. Lowest possible cost. The fail-open mechanism absorbs all octocode-specific risks (rate limit, telemetry, supply chain) without touching brainstorm core logic.

**Trade-off:** Octocode runs on *every* `code`/`architecture` brainstorm — even quick/standalone solo brainstorms where the value is marginal. Token tax is consistent.

### Candidate B — Auggie-parallel "twin" row (precedent as 1st-class co-equal)

Treat octocode as a *co-equal twin* of auggie, not a separate concern. The row becomes:

```text
| `domain ∈ {code, architecture, incident}` AND NOT `--no-codebase` | (parallel) `mcp__auggie__codebase-retrieval` → `enrichment/codebase-context.md` AND `octocode-precedent-search` → `enrichment/precedent.md` | both files |
```

The codebase enrichment quality-tier system extends to track *both* sides: `quality_tier` becomes `{local: primary, precedent: primary}` etc. If only auggie succeeds → `{local: primary, precedent: skipped}` and brainstorm continues. If only octocode succeeds → `{local: fallback_2, precedent: primary}` and Wave 2B downweights local context.

**Rationale:** Two halves of the same coin — "what do *we* do here?" + "what do *others* do here?". Forces a complete external-internal context picture for every code-style brainstorm.

**Trade-off:** Roughly doubles the codebase-enrichment token budget. Couples the two tools' availability — even though one is local-free and the other is rate-limited external.

### Candidate C — Strategy-gated only (enterprise + deep only)

Octocode enrichment is only triggered when the brainstorm is *expensive enough* to warrant external precedent search:

```text
| `--strategy enterprise` OR `--depth deep` AND `domain ∈ {code, architecture}` | Invoke `octocode-precedent-search` | `enrichment/precedent.md` |
```

For quick/standard/solo brainstorms, octocode never fires.

**Rationale:** Octocode burns 2-5K tokens of external API and counts toward the 3000-token enrichment cap. For a `quick` brainstorm aiming at 8K tokens per proposal × 2 proposals = 16K total, eating 30% on external precedent is poor ROI. Reserve it for the deep/enterprise tier where 35K × 7 proposals = 245K total → 5K precedent is 2%.

**Trade-off:** Loses the lighter-weight case where precedent is exactly what would *upgrade* a shallow brainstorm to something useful. The user who already knew they wanted enterprise depth was the user least in need of precedent suggestions.

### Candidate D — Per-proposal precedent (deferred to Wave 2B / hands-off to Wave 3)

Wave 2A does *not* call octocode directly. Instead, it produces a small `precedent-queries.md` artifact (~200 tokens) listing the top 3-5 keyword clusters from the seed brief. **Wave 3 (adversarial)** then spawns one octocode agent *per proposal* during the proposal-generation step, using the seed brief + the proposal's specific architectural choice as the search anchor.

**Rationale:** Precedent should be specific to a *proposal*, not the *topic*. Asking "how do projects solve retry logic?" is much weaker than asking "how do projects implement an exponential-backoff retry registry using a circuit-breaker decorator pattern?" because the latter is what proposal A actually committed to. Each proposal gets its own real-world ammunition.

**Trade-off:** Moves logic out of Wave 2A entirely (so this candidate technically *doesn't* integrate at Wave 2A — see "What This Cannot Do"). Multiplies octocode invocations by N proposals (2-7), which is exactly the GitHub Search-API rate-limit failure mode (30/min). 7-proposal × 3 queries each = 21 calls in a tight window.

### Candidate E — Hybrid pre-discovery (octocode runs *before* the routing matrix evaluates)

A new pre-step at the start of Wave 2A:

1. Run a single fast `packageSearch` + `githubSearchRepositories` query against topic keywords (~500 tokens, 2 API calls).
2. Inspect results. If any popular packages/repos surface, **inject them into the routing matrix** as additional context: "topic mentions [pydantic-ai, langchain]" → auto-trigger `--research light` (because cross-repo precedent exists).
3. Cache the discovery output as `enrichment/precedent-discovery.md`.
4. Then run the existing routing matrix.

**Rationale:** Octocode is uniquely good at "*is there an ecosystem around this topic?*" — exactly the question the existing auto-detect rule asks ("topic mentions framework/library names not in project"). Octocode could *replace* that brittle keyword check with a real lookup.

**Trade-off:** Adds a pre-Wave step → not a pure routing-matrix change. Increases Wave 2A latency floor (forces a serial step before the parallel fan-out). If octocode fails at pre-discovery, the auto-routing logic loses its driver and falls back to user-specified flags.

### Candidate F — Cross-wave ammunition feed (Wave 2A discovers, Wave 3 consumes)

Wave 2A behaves as Candidate A (a new matrix row producing `precedent.md`). But the *real* consumer is Wave 3: the adversarial agent-spec is augmented with a `--precedent-source <output>/enrichment/precedent.md` flag. Each adversarial persona reads precedent in addition to the seed brief; debate transcripts can cite "GitHub project X solved this differently" as a real adversarial axis.

**Rationale:** Precedent should *fuel* debate, not just contextualize the seed brief. The strongest argument for octocode in this protocol is that it provides debate ammunition that's *evidence-grounded* (real PRs, real production code) rather than model-internal recall.

**Trade-off:** Requires coordinated changes in `sc-adversarial-protocol` (a separate skill) to accept the new flag. Cross-skill integration breaks the "Wave 2A is self-contained" property and elevates the integration from "drop-in row" to "two-skill protocol upgrade."

### Candidate G — Octocode as Tier 2 fallback for `auggie` failure only

Insert octocode into the *tier ladder*, not as a parallel lane:

```text
Codebase enrichment tier ladder:
  Tier 1 (primary):    mcp__auggie__codebase-retrieval
  Tier 2 (fallback_1): NEW — octocode githubSearchRepositories + githubSearchCode (the local repo on GitHub)
  Tier 3 (fallback_2): mcp__serena__get_symbols_overview
  Tier 4 (fallback_3): native Glob/Grep
```

**Rationale:** When auggie is down, the user still wants codebase context. Octocode can search the local repo *as a GitHub project* (if the repo is on GitHub) and provide useful structure/content. Conservative — only activates when the primary fails.

**Trade-off:** This is the *opposite* of octocode's strength. Octocode's value is **cross-repo**, not single-repo. Using it as a single-repo auggie-failure fallback wastes its strength and discards the precedent-search use case entirely. Strong NO from this brainstormer, but listed for completeness.

---

## Wave 2: Adversarial Evaluation

Each candidate scored along five axes (1-5, higher = better). "Δ" = sum.

### A — Drop-in matrix row

| Axis | Score | Reasoning |
|---|---|---|
| Architectural fit | 5 | Mirrors existing matrix-row pattern exactly; zero new concepts |
| Fail-open compatibility | 5 | Plugs into existing quality-tier slot; failure path identical to existing rows |
| Value delivered | 3 | "Generic precedent for every code brainstorm" — useful but undirected |
| Token efficiency | 3 | Adds ~1-2K to enrichment budget always; counts vs 3K cap |
| Risk surface | 4 | Single new row; reversible by deleting; supply-chain risk constrained by fail-open |
| **Δ** | **20** | |

**Adversarial critique:** *Boring. Maximally safe but underutilizes octocode's differentiator. A drop-in row produces a "generic precedent dump" that the proposals may not even reference.*

### B — Auggie-parallel twin row

| Axis | Score | Reasoning |
|---|---|---|
| Architectural fit | 4 | Extends existing row rather than adding a new one; requires quality-tier compound state |
| Fail-open compatibility | 4 | Compound quality-tier `{local, precedent}` adds complexity but stays fail-open |
| Value delivered | 5 | Forces complete external-internal picture; strongest "what do we know" framing |
| Token efficiency | 2 | Roughly doubles codebase enrichment budget; ~4K total |
| Risk surface | 3 | Couples two unrelated dependencies; auggie failure mode changes |
| **Δ** | **18** | |

**Adversarial critique:** *Conceptually elegant but violates the "loose coupling" implicit in Wave 2A's row structure. Making octocode a co-equal of auggie elevates supply-chain + rate-limit risk to first-class operational concerns.*

### C — Strategy-gated (enterprise/deep only)

| Axis | Score | Reasoning |
|---|---|---|
| Architectural fit | 5 | Single matrix-row addition with a tighter gate |
| Fail-open compatibility | 5 | Same as A; rate-limit risk drops because volume drops |
| Value delivered | 4 | High-leverage when triggered — exactly when brainstorms benefit most from external precedent |
| Token efficiency | 5 | Octocode budget only consumed when Wave 3 budget supports it |
| Risk surface | 5 | Lowest blast radius; rate-limit + supply-chain risk only on enterprise-tier runs |
| **Δ** | **24** | |

**Adversarial critique:** *Conservative to a fault — denies the "shallow brainstorm" user the very help octocode could provide. But the gate matches the cost profile better than any other candidate.*

### D — Per-proposal precedent in Wave 3

| Axis | Score | Reasoning |
|---|---|---|
| Architectural fit | 1 | Not a Wave 2A integration; belongs in a different brainstorm |
| Fail-open compatibility | 3 | Requires sc-adversarial protocol-level rate-limit handling |
| Value delivered | 5 | Strongest possible match between precedent and proposal |
| Token efficiency | 2 | N proposals × M queries = potential rate-limit blowout |
| Risk surface | 2 | Cross-skill change; new failure modes during proposal generation |
| **Δ** | **13** | |

**Adversarial critique:** *Out of scope by definition. Worth recording as a follow-up but disqualified for this target.*

### E — Hybrid pre-discovery

| Axis | Score | Reasoning |
|---|---|---|
| Architectural fit | 3 | Adds a pre-step to Wave 2A — partially breaks parallelism |
| Fail-open compatibility | 3 | Pre-step failure cascades to routing-matrix evaluation |
| Value delivered | 5 | Octocode plays to its strength: ecosystem-discovery |
| Token efficiency | 4 | ~500 tokens pre-step is small; downstream costs unchanged |
| Risk surface | 3 | New serial bottleneck; auto-routing logic depends on octocode availability |
| **Δ** | **18** | |

**Adversarial critique:** *Architecturally interesting — uses octocode where it's irreplaceable (discovery) rather than where it's redundant (precedent). But violates Wave 2A's parallel-first design and creates a soft dependency.*

### F — Cross-wave ammunition feed

| Axis | Score | Reasoning |
|---|---|---|
| Architectural fit | 3 | Requires coordinated changes in sc-adversarial-protocol |
| Fail-open compatibility | 4 | Wave 2A side is fail-open; Wave 3 side gracefully ignores missing precedent file |
| Value delivered | 5 | Best possible use of precedent — feeds the *debate* not just the *context* |
| Token efficiency | 3 | Precedent is read N times (once per adversarial agent) |
| Risk surface | 3 | Cross-skill protocol upgrade; needs two coordinated PRs |
| **Δ** | **18** | |

**Adversarial critique:** *Highest theoretical ceiling but multi-PR rollout. The right "v2" but not the right "v1".*

### G — Tier-2 fallback for auggie failure

| Axis | Score | Reasoning |
|---|---|---|
| Architectural fit | 4 | Fits existing tier ladder |
| Fail-open compatibility | 5 | Identical pattern to existing Serena fallback |
| Value delivered | 1 | Misuses octocode's cross-repo strength as a single-repo fallback |
| Token efficiency | 4 | Only activates on auggie failure; rare |
| Risk surface | 4 | Limited blast radius |
| **Δ** | **18** | |

**Adversarial critique:** *Discards octocode's killer feature. Strong NO.*

### Wave 2 ranking

| Rank | Candidate | Δ | Verdict |
|---|---|---|---|
| 1 | **C — Strategy-gated** | **24** | **Winner** |
| 2 | A — Drop-in row | 20 | Solid backup |
| 3 (tie) | B / E / F / G | 18 | Each has a fatal flaw for v1 |
| 7 | D — Per-proposal | 13 | Out of scope |

---

## Wave 3: Convergence

### Winner: Candidate C with a small concession from Candidate A

**Final design: Strategy-gated by default + opt-in flag for lighter tiers**

The pure Candidate C (enterprise/deep only) is correct for the *default behavior* but should not be the *only* behavior. The hybrid synthesizes both:

> **Default trigger:** `domain ∈ {code, architecture}` AND (`--strategy ∈ {enterprise, default}` OR `--depth deep`) AND NOT `--no-precedent`.
>
> **Manual trigger:** `--precedent` flag forces octocode regardless of strategy/depth.
>
> **Opt-out:** `--no-precedent` suppresses octocode in all cases.

This unifies Candidate C's cost discipline with Candidate A's user agency. Quick-and-cheap brainstorms can opt in if the user knows they want precedent; expensive brainstorms get precedent by default because the cost ratio favors it.

### Why C-with-concession wins on net

- **Cost-aware by default:** Wave 2A's 3K-token enrichment budget is preserved for the cheap/medium cases that don't need external API
- **GitHub Search rate limit (30/min) is bounded:** only deep/enterprise runs hit octocode, and those are infrequent (rate of `enterprise brainstorms × deep brainstorms` ≤ tens per hour)
- **Fail-open semantics preserved without modification:** same quality-tier ladder pattern as auggie
- **Single matrix row:** still a one-row edit to SKILL.md + one section in handoff-routing.md
- **No cross-skill coordination:** Wave 3 doesn't need to change; that upgrade can come later as a separate "v2" iteration

### What was deliberately rejected

- **B (twin row):** Operationally over-coupled; doubles cost for marginal added value in non-deep cases
- **D (per-proposal):** Out of scope — belongs in a separate Wave 3 brainstorm
- **E (pre-discovery):** Architecturally interesting but breaks Wave 2A's parallel-first design
- **F (cross-wave feed):** Right "v2", wrong "v1"
- **G (auggie fallback):** Misuses octocode's strength

---

## Recommended Design (Deep Dive)

### Full description

Add a fourth row to Wave 2A's routing matrix called the **precedent-discovery enrichment**. The row triggers when the brainstorm is *expensive enough* to warrant the octocode cost (default: enterprise strategy or deep depth) OR when the user explicitly requests it via `--precedent`. The row spawns a single `Task` agent running a *restricted* octocode tool subset — only `packageSearch`, `githubSearchCode`, `githubSearchPullRequests`, and `githubGetFileContent` — against the topic keywords from `seed-brief.md`'s `Problem Statement` and `Known Context` sections. The agent produces a structured `enrichment/precedent.md` artifact summarizing 3-5 most-relevant cross-repo references with rationale.

The artifact is appended to the seed-brief's `## Enrichment Context` section (along with the existing codebase + research summaries), and counted toward the 3K-token enrichment cap with **lowest priority** (codebase > research-light > research-deep > precedent). On octocode failure, the row records `quality_tier: skipped` and Wave 2A proceeds — exactly like existing rows.

### Concrete diff sketch to SKILL.md

**BEFORE (SKILL.md:179-187):**

```text
1. **Enrichment routing matrix** (apply in parallel via `Task` agents):

   | Condition | Action | Output |
   |-----------|--------|--------|
   | `domain ∈ {code, architecture, incident}` AND NOT `--no-codebase` | Invoke `/sc:analyze <relevant-paths> --focus quality --depth quick` OR `mcp__auggie__codebase-retrieval` for quick scan | `enrichment/codebase-context.md` |
   | `--codebase` (forced) | Same as above regardless of domain | Same |
   | `--research light` OR (auto: topic mentions framework/library names not in project) | Invoke `Skill sc-research-protocol` with `--depth quick` (or `/sc:research` if standalone) | `enrichment/research-light.md` |
   | `--research deep` OR (auto: `--strategy enterprise` + novel topic) | Invoke `Skill tech-research` with topic | `enrichment/research-deep.md` |
   | Otherwise | Skip enrichment | — |
```

**AFTER (SKILL.md:179-189):**

```text
1. **Enrichment routing matrix** (apply in parallel via `Task` agents):

   | Condition | Action | Output |
   |-----------|--------|--------|
   | `domain ∈ {code, architecture, incident}` AND NOT `--no-codebase` | Invoke `/sc:analyze <relevant-paths> --focus quality --depth quick` OR `mcp__auggie__codebase-retrieval` for quick scan | `enrichment/codebase-context.md` |
   | `--codebase` (forced) | Same as above regardless of domain | Same |
   | `--research light` OR (auto: topic mentions framework/library names not in project) | Invoke `Skill sc-research-protocol` with `--depth quick` (or `/sc:research` if standalone) | `enrichment/research-light.md` |
   | `--research deep` OR (auto: `--strategy enterprise` + novel topic) | Invoke `Skill tech-research` with topic | `enrichment/research-deep.md` |
   | `domain ∈ {code, architecture}` AND (`--strategy ∈ {enterprise, default}` OR `--depth deep` OR `--precedent`) AND NOT `--no-precedent` | Invoke `Task: octocode-precedent-search` with topic keywords (restricted tool subset: `packageSearch`, `githubSearchCode`, `githubSearchPullRequests`, `githubGetFileContent`) | `enrichment/precedent.md` |
   | Otherwise | Skip enrichment | — |
```

**Update token budget priority (SKILL.md:196):**

BEFORE:
> Priority order if exceeded: codebase > research-light > research-deep. Truncate by priority.

AFTER:
> Priority order if exceeded: codebase > research-light > research-deep > precedent. Truncate by priority.

**Add to Wave 0 flag validation (SKILL.md:96-110, between steps 7 and 8):**

```text
7b. **Precedent flag validation**: `--precedent` and `--no-precedent` are mutually exclusive. If both → STOP: `"--precedent and --no-precedent cannot be used together."`
```

**Extend the return contract (SKILL.md:344-348):**

BEFORE:
```yaml
enrichment_used:
  - source: codebase | research-light | research-deep
    quality_tier: primary | fallback_1 | fallback_2 | skipped
```

AFTER:
```yaml
enrichment_used:
  - source: codebase | research-light | research-deep | precedent
    quality_tier: primary | fallback_1 | fallback_2 | skipped
```

**Add row to Error Handling Matrix (SKILL.md:380, between codebase + research rows):**

```text
| Precedent enrichment fails (octocode down / rate-limited) | WARN, record quality_tier=skipped, proceed | Skip (no tier 2 — precedent is opportunistic) |
```

### Concrete diff sketch to `refs/handoff-routing.md`

Append a new subsection under `§Enrichment-Sources` (after the "Research enrichment (deep)" block, line ~58):

```markdown
### Precedent enrichment (cross-repo)

**Trigger conditions**:

- `domain ∈ {code, architecture}` AND (`--strategy ∈ {enterprise, default}` OR `--depth deep`) AND NOT `--no-precedent`, OR
- `--precedent` (forced) regardless of strategy/depth

**Tier 1 (primary)**: `Task: octocode-precedent-search`

- Restricted tool subset (set via the agent's `tools:` frontmatter):
  - `mcp__octocode__packageSearch`
  - `mcp__octocode__githubSearchCode`
  - `mcp__octocode__githubSearchPullRequests`
  - `mcp__octocode__githubGetFileContent`
- LSP tools, clone, and local-search tools are NOT exposed (they overlap with serena+auggie).
- Sub-agent prompt template (full prompt at `refs/precedent-agent-prompt.md`):
  - Extract top 3-5 keyword/concept clusters from `seed-brief.md` (Problem Statement + Known Context + Constraints)
  - For each cluster: `packageSearch` → `githubSearchCode` → at most 2 `githubGetFileContent` reads
  - Synthesize a one-paragraph "precedent summary" per cluster with reasoning + citations
- Output: `enrichment/precedent.md` (~800-1200 tokens summary, structured below)
- quality_tier: `primary`

**Tier 2 (fallback)**: none. Precedent is opportunistic — if octocode fails, skip.

- Activation: if Tier 1 errors, rate-limits (HTTP 403), or returns empty → set quality_tier: `skipped`, continue Wave 2A.

**Token cap**: 1000 tokens of summary in seed-brief.md. Lowest priority for the 3K combined cap (truncated first).

**Rate-limit guard**: Octocode uses GitHub Search API (30 req/min binding constraint). The precedent agent MUST cap its total tool calls at 8 (≈ 1 packageSearch + 4 githubSearchCode + 3 githubGetFileContent). Beyond 8 → terminate early and emit best-effort summary.

**Anti-trigger rules** (precedent NOT routed):

- `domain ∈ {product, process, incident, research}` — non-code domains don't benefit from cross-repo code precedent
- `--no-precedent` set
- `--depth quick` AND `--strategy ∈ {agile, systematic}` AND no `--precedent` — cost ratio too poor
- `--dry-run` — precedent search is skipped under dry-run (consistent with how dry-run skips Wave 3)
- No GitHub Token available (`GITHUB_TOKEN` env unset AND `gh auth status` fails) — STOP precedent only, not the whole wave
```

### New artifact file structure: `enrichment/precedent.md`

```markdown
---
source: octocode-precedent-search
created: <ISO-8601>
quality_tier: primary
keyword_clusters_searched: ["<cluster-1>", "<cluster-2>", "<cluster-3>"]
octocode_version: 14.2.0
api_calls_used: <N>/8
---

# Precedent Discovery — <topic-slug>

## Summary

<2-3 sentence overall framing — what kind of precedent was found and how it relates to the topic>

## Cluster 1: <keyword cluster name>

### Reference: <owner/repo> — <relevant file path>

**Relevance:** <one-line justification>

**Pattern observed:**
<2-4 sentences describing how this project solved the relevant problem>

**Citation:** [<file path>](<github URL>#L<line-start>-L<line-end>)

### Reference: <...next reference in cluster, max 2 per cluster...>

## Cluster 2: <...>

(repeated structure)

## Cluster 3: <...>

(repeated structure)

## Out-of-Scope Findings

<Any interesting hits that don't fit the clusters but the agent flagged as potentially valuable for adversarial debate.>

## Failed Searches

<List queries that returned 0 hits, with rationale — useful for the Wave 3 debate to argue "no precedent exists" claims>
```

### Quality-tier semantics

| Outcome | Tier | Wave 2A behavior |
|---|---|---|
| Octocode runs, finds ≥1 reference | `primary` | Append summary to seed-brief, full file in `enrichment/precedent.md` |
| Octocode runs, returns 0 references after all clusters | `primary` (success, just empty) | Append note "no cross-repo precedent found" to seed-brief; full file records failed searches |
| Octocode errors (network, MCP transport) | `skipped` | Log WARN, continue |
| Octocode rate-limited (HTTP 403 from GitHub Search) | `skipped` | Log WARN with retry-after hint, continue |
| No `GITHUB_TOKEN` available | `skipped` | Log INFO once per session: "Precedent enrichment requires GitHub authentication" |
| `--no-precedent` set | `skipped` | Silent (expected user choice) |
| `--dry-run` | `skipped` | Silent |
| Tool-call budget exceeded (>8 calls) | `primary` (best-effort) | Append summary with `partial: true` flag in file frontmatter |

**Critical:** Octocode failure is NEVER a tier-2 fallback target; precedent is fully opportunistic. This is the *only* enrichment source without a fallback ladder — chosen because (a) the killer feature is irreplaceable (no substitute provides cross-repo precedent), and (b) lacking precedent gracefully degrades the brainstorm rather than breaking it.

### Token budget impact

| Scenario | Budget added | % of 3K cap |
|---|---|---|
| Default (no precedent) | 0 | 0% |
| `--depth deep` brainstorm | 800-1200 (summary) | 27-40% |
| `--strategy enterprise` brainstorm | 800-1200 | 27-40% |
| Both | 800-1200 (same agent) | 27-40% |
| `--precedent` forced on quick | 800-1200 | 27-40% (truncates research-deep first) |

**Octocode MCP context tax** (already paid if octocode is registered): ~5-7K tokens *system-prompt-level* (the 14 tool schemas). This is per-session, not per-brainstorm — amortized across all uses.

### Tool subset used (restrictive whitelist)

The precedent sub-agent's `tools:` frontmatter lists ONLY:

```yaml
tools:
  - mcp__octocode__packageSearch
  - mcp__octocode__githubSearchCode
  - mcp__octocode__githubSearchPullRequests
  - mcp__octocode__githubGetFileContent
  - Read    # to read seed-brief.md
  - Write   # to write precedent.md
```

**Explicitly excluded** (and why):

- `localSearchCode`, `localFindFiles`, `localViewStructure`, `localGetFileContent` — overlap with native Grep + auggie
- `lspGotoDefinition`, `lspFindReferences`, `lspCallHierarchy` — overlap with serena, and brainstorm shouldn't need symbol-level analysis
- `githubCloneRepo` — disk-write side effect; not needed for summary-style precedent
- `githubSearchRepositories` — used in pre-discovery (Candidate E), not in precedent

This restriction is enforceable via the sub-agent's `allowed-tools` field and is the *primary* security control for the supply-chain risk identified in Stage 1 (§4.1) — the agent can read, but cannot clone or write anywhere on disk except its designated output.

### Anti-trigger rules (when does the matrix NOT route to octocode?)

1. Domain is `product`, `process`, `incident`, or `research` — no code-precedent value
2. `--no-precedent` set
3. `--depth quick` + `--strategy ∈ {agile, systematic}` + no explicit `--precedent` — cost ratio too poor
4. `--dry-run` mode — consistent with sc:roadmap dry-run semantics
5. No GitHub authentication available — precedent skipped, other enrichments unaffected
6. `--resume-from` an existing brainstorm whose `enrichment_used` already records `precedent` — don't re-run (idempotency)

### Rate-limit / failure handling (fail-open is critical here)

| Failure | Handling | User-facing impact |
|---|---|---|
| `npx octocode-mcp` fails to start (binary not installed) | Log WARN once per session, skip precedent | "Precedent enrichment unavailable (octocode-mcp not installed)." |
| GitHub Search API 403 (rate limit) | Catch exception, set quality_tier=skipped, log retry-after | "Precedent enrichment rate-limited; skipped." |
| GitHub Search API 401 (token expired) | Catch exception, set quality_tier=skipped | "Precedent enrichment requires fresh GitHub token; skipped." |
| Network timeout (per-search 30s, total 120s) | Best-effort: return whatever clusters completed | "Precedent enrichment partial: <N>/<M> clusters returned." |
| MCP transport error | Treat as Tier-1 failure → quality_tier=skipped | "Precedent enrichment failed (transport)." |
| Octocode tool returns malformed JSON | Skip that one tool call, continue cluster | Silent (recoverable per cluster) |
| Tool-call budget (8) exhausted | Stop calling tools, return current state with `partial: true` | "Precedent enrichment partial (budget exhausted)." |

**The key invariant:** *Precedent never blocks the brainstorm.* This is structurally enforced — the row uses the same fail-open pattern as the existing rows, and the sub-agent's max runtime is the standard 120s per-source timeout from `handoff-routing.md:64`.

### Test plan: 3 example brainstorm questions

**Test 1: `/sc:brainstorm "redesign our retry logic for HTTP clients"` (default strategy, standard depth)**

Wave 2A behavior:
1. Domain classifier → `code`
2. Routing matrix evaluated:
   - Codebase row: `domain=code ∈ {code, architecture, incident}` AND NOT `--no-codebase` → **fires** → auggie quickly returns local retry implementations
   - Precedent row: `domain=code ∈ {code, architecture}` AND `--strategy=default` ∈ `{enterprise, default}` → **fires** → octocode searches `packageSearch("httpx retry"), githubSearchCode("retry exponential backoff client")`, produces 3 clusters: tenacity, urllib3 retry, axios-retry
   - Research-light row: topic mentions no specific framework → does not fire
3. Both artifacts produced in parallel; total enrichment ~2K tokens (within 3K cap)
4. Seed brief enriched with `## Enrichment Context` summarizing both
5. Wave 2B proceeds with richer context; adversarial proposals can cite local + cross-repo
6. Quality tiers in return contract: `[{codebase, primary}, {precedent, primary}]`

**Test 2: `/sc:brainstorm "what should our team standup format look like" --depth quick` (process domain, quick depth)**

Wave 2A behavior:
1. Domain classifier → `process`
2. Routing matrix evaluated:
   - Codebase row: `domain=process ∉ {code, architecture, incident}` → does not fire
   - Precedent row: `domain=process ∉ {code, architecture}` → does not fire (anti-trigger rule #1)
   - Research-light row: topic mentions no framework → does not fire
3. Enrichment skipped entirely (per "Otherwise" row)
4. Wave 2B proceeds without enrichment
5. Quality tiers in return contract: `[]` (empty list)

This test confirms the anti-trigger rules prevent octocode from firing on non-code domains, preserving the GitHub Search budget for cases where it adds value.

**Test 3: `/sc:brainstorm "migrate from Webpack to Rspack" --strategy enterprise --depth deep --precedent` (explicit precedent on code domain)**

Wave 2A behavior:
1. Domain classifier → `code` (or `architecture`)
2. Wave 0 sets `--depth deep` because `--strategy enterprise` (per SKILL.md:110)
3. Routing matrix evaluated:
   - Codebase row: fires → auggie searches local webpack config
   - Precedent row: fires (multiple conditions met) → octocode searches `packageSearch("rspack")`, `githubSearchPullRequests("webpack rspack migration")`, finds Vercel/Vite migration PRs
   - Research-deep row: `--strategy enterprise` + novel topic → fires → tech-research dispatched in parallel
4. All three artifacts produced; total enrichment hits ~2.8K (close to 3K cap)
5. Token budget check: precedent has lowest priority — its summary is truncated to ~600 tokens (from 1200) to keep budget under cap
6. Quality tiers: `[{codebase, primary}, {precedent, primary, partial}, {research-deep, primary}]`

This is the *highest-value scenario* — the brainstorm gets local code, external precedent (Vercel's actual migration PRs), and deep research synthesis all feeding Wave 3's adversarial debate.

**Bonus test 4: octocode unavailable, same Test 1 invocation**

- Codebase row: fires (auggie OK) → quality_tier=primary
- Precedent row: fires → octocode fails (e.g., no `GITHUB_TOKEN`) → quality_tier=skipped → WARN logged: `"Precedent enrichment requires GitHub authentication; skipped."`
- Brainstorm proceeds with codebase enrichment only
- Quality tiers: `[{codebase, primary}, {precedent, skipped}]`
- **The brainstorm completes successfully** — confirming fail-open invariant.

---

## What This Cannot Do

This integration deliberately does *not*:

1. **Per-proposal precedent (Candidate D):** Each adversarial proposal in Wave 3 gets the same shared `precedent.md`. If you want per-proposal targeted precedent ("how does *proposal A specifically* match other projects?"), that requires a separate Wave 3 integration in `sc-adversarial-protocol`. Logged as future work.

2. **Replace `--research light` for framework discovery:** Octocode is precedent-focused, not docs-focused. Context7 + Tavily still handle "what does this framework officially recommend." Octocode answers "what do real projects actually do."

3. **Drive auto-routing logic (Candidate E):** The pre-discovery use case where octocode *decides* which other rows fire is deferred. The current design treats each row's trigger condition independently.

4. **Feed Wave 3 debate transcript as first-class ammunition (Candidate F):** The precedent artifact is in the seed brief's enrichment section, where Wave 3 personas read it during proposal generation. But it's not a first-class flag to `sc-adversarial-protocol`. Future v2 could add `--precedent-source` to adversarial. Logged.

5. **Cross-repo PR archaeology beyond keyword search:** Deep PR-history mining ("why did langchain remove their old tool registry?") is a `tech-research` Phase 4 capability (integration target #2), not a Wave 2A enrichment. The two integrations are complementary, not overlapping.

6. **Solve the supply-chain risk identified in Stage 1 §4.1:** Bus-factor=1, 194 npm versions, `@latest` install. Mitigations belong in the `install_mcp.py` registration (target #5), not here. This integration *assumes* octocode is already pinned to a vetted version.

7. **Provide a UI for octocode tool subset overrides:** The whitelist is hardcoded in `refs/precedent-agent-prompt.md`. Users wanting to expose more octocode tools must edit the ref. Intentional — prevents tool-surface bloat.

---

## Cross-Target Dependencies

### Does Wave 2A go through deep-research, or is it independent?

**Independent path.** Wave 2A currently calls auggie *directly* (line 183: `mcp__auggie__codebase-retrieval`), not via `deep-research` agent. The proposed precedent row similarly calls a small dedicated `Task` agent directly via the MCP tool subset, not via `deep-research`. **This integration can ship standalone**, before or after the `deep-research` integration (target #1).

### What if `deep-research` (target #1) ships first?

If `deep-research` has been upgraded to know about octocode (per target #1's brainstorm), then the `--research deep` row of Wave 2A *transitively* gets octocode access via `tech-research → deep-research`. In that case:

- The dedicated precedent row in this brainstorm is *still valuable* because it runs independently and in parallel (precedent != deep-research)
- Precedent agent stays focused (cross-repo code only), while research-deep does broader synthesis
- No conflict — they produce different artifacts (`precedent.md` vs `research-deep.md`)

### What if this brainstorm ships first?

Octocode lands in Wave 2A's precedent row only. `deep-research` remains unchanged. `tech-research` continues using Tavily. **No downstream breakage.** Target #1 can land independently later.

### Hard prerequisites

Both of:

1. **Target #5 (octocode MCP server registration in `install_mcp.py`) MUST ship first.** Without this, octocode tools are not exposed. The implementation cannot land without the server registered.
2. **A GitHub PAT or `gh auth login` token is required at brainstorm-runtime.** Without it, the precedent row records `quality_tier=skipped` (never blocks the run).

### Soft prerequisites (nice-to-have)

- Target #2 (`tech-research` Phase 4 octocode integration) and Target #1 (`deep-research` octocode axis) are *independent* but valuable. Either can land before or after this without conflict.
- Documentation update for `octocode-precedent-search` Task agent pattern in `.dev/eval-workspaces/sc-brainstorm/`.

### Coupling matrix

| Target | Coupling to this brainstorm | Ship order |
|---|---|---|
| #5 install_mcp.py | **Hard prereq** | Must land first |
| #1 deep-research | None (independent) | Either order |
| #2 tech-research Phase 4 | None (independent) | Either order |
| #3 sc:research command | None | Either order |
| #6 sc:troubleshoot | None | Either order |

---

## Effort Estimate

| Task | Effort | Notes |
|---|---|---|
| Edit `SKILL.md` Wave 2A matrix + budget priority + Wave 0 flag + return contract + error matrix | **45 min** | ~25 lines of declarative edits across 4 sections |
| Append `§Enrichment-Sources::Precedent enrichment` to `refs/handoff-routing.md` | **30 min** | ~40-line subsection following existing format |
| Author `refs/precedent-agent-prompt.md` (new ref file for the sub-agent prompt template) | **45 min** | New file, ~80 lines |
| Wire up the `octocode-precedent-search` Task agent definition (could live in `agents/` or be inline in the prompt ref) | **30 min** | Decision needed: agent file vs inline prompt |
| Run `make sync-dev` + `make verify-sync` | **5 min** | Standard |
| Write unit-style validation: `seed-brief.md` produced with `enrichment_used` correctly populated for each of the 3 test scenarios | **2 hours** | Mock octocode responses for deterministic testing |
| Manually run 3 brainstorms (the test plan above) and verify the matrix evaluates correctly | **45 min** | Real-API validation; uses GitHub Search budget |
| Update `.dev/eval-workspaces/sc-brainstorm/SPEC.md` (the 684-line spec referenced in SKILL.md:421) with the new enrichment source | **30 min** | Section update for spec consistency |
| Compose PR description tying back to fit-analysis target #4 | **20 min** | Reference Stage 1 + Stage 2 docs |
| **Total** | **~5.5 hours** | One PR, single developer, declarative-only changes |

**Critical path:** SKILL.md edit + handoff-routing.md edit + precedent-agent-prompt.md authoring = ~2 hours. Everything else is validation + docs.

**Risk multiplier:** Add 1-2 hours if the sub-agent prompt requires iteration to produce reliably-structured `precedent.md` artifacts. Recommend a 1-day pilot with 5-10 representative brainstorms before declaring "done."

**Hard prerequisite:** Target #5 (`install_mcp.py:29` registration with `LOG=false` + `TOOLS_TO_RUN` whitelist + pinned version) must land first. Estimate ~1 hour for that target alone.

---

**End of brainstorm — Target #4 (sc-brainstorm Wave 2A enrichment).**

Recommendation: **Adopt Candidate C-with-concession (strategy-gated by default + `--precedent` opt-in)** as the v1 integration path. It maximizes octocode's killer feature (cross-repo precedent) while respecting the 3K-token enrichment budget and GitHub Search rate-limit ceiling. The fail-open invariant of Wave 2A absorbs every octocode-specific failure mode without protocol changes. Ship after target #5 (MCP registration); independent of all other targets. Estimated effort: 5.5 hours single-PR.
