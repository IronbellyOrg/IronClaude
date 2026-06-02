# Proposal B — Analyzer Lens

**Persona:** analyzer
**Model:** sonnet
**Status:** Complete
---

## Design Thesis

**A centralized octocode skill is only worth its orchestration cost if — and ONLY if — it gives us measurement, budget enforcement, and failure observability that distributed integration structurally cannot.**

The v2 plan defers ALL of these concerns to "pilot phase" (per FINAL-RECOMMENDATIONS-v2.md §"What This Investigation Did NOT Cover" #2, #3, #6). It distributes octocode across 6 surfaces, each with its own rate-limit cap (T2: 5 searchCode + 3 searchPullRequests per agent; T4: 4-tool whitelist; T5: type-gated; T6: tier-gated). Every surface reasons about its OWN budget. No surface has a global view. This is the fundamental observability gap.

A centralized skill — call it `octocode-funnel` — is justified iff it converts these 6 independent budget-tracking blind spots into ONE instrumented choke point. The lens here is NOT cleanliness (architect proposal A's territory) or contract-purity (scribe proposal C's territory). It is: **you cannot manage what you cannot measure, and right now we cannot measure octocode at all.**

If the centralized skill cannot demonstrate measurement gains the distributed plan can't match, this proposal collapses. The defense rests entirely on instrumentation.

---

## Skill Name + Purpose

**Name:** `octocode-funnel`

**One-line purpose:** A single instrumented choke point for ALL cross-repo octocode invocations across the framework, enforcing a global GitHub Search budget, emitting per-invocation telemetry, and surfacing rate-limit + outage signals to every caller through one canonical interface.

**Explicit non-goals:**
- NOT a research replacement for tech-research (it sits DOWNSTREAM of tech-research's scope discovery)
- NOT a router for local-codebase work (auggie/serena/Read keep that turf)
- NOT a workflow scaffold like `octocode-research` (v2 already declined that ontology import — see octocode-research.md §6 "Strong NO")
- NOT a place to put new investigation logic — it is a metered execution layer

**The skill's job, stripped down:** "Given a scoped investigation request from a caller (codebase set + question + budget hint), execute octocode tool calls, return findings, and write metrics. Everything else is the caller's problem."

This minimalism is deliberate. Every behavior the skill takes on is one more thing the instrumentation has to model. Keep it small so the metrics stay legible.

---

## Measurement-First Architecture

The skill's defining characteristic is that EVERY invocation writes a structured metrics record. Not as a debug feature. As the primary output, alongside findings.

### What gets instrumented (per invocation)

| Dimension | Measurement | Why it matters |
|---|---|---|
| **Input scope size** | N codebases requested, N keywords, depth flag, caller-supplied budget hint | Detect scope creep over time |
| **Tool calls fired** | Count per tool: `packageSearch`, `githubSearchCode`, `githubSearchPullRequests`, `githubGetFileContent`, `githubViewRepoStructure` | Catch funnel-method violations (e.g., `githubGetFileContent` without prior `viewRepoStructure`) |
| **Tokens consumed** | Input prompt tokens, octocode response tokens, total session delta | Compare against v2's projected 3K schema-load tax per surface |
| **Wall-clock** | Skill invocation start, first-tool start, last-tool end, return | Detect serialization regressions |
| **Rate-limit budget consumed** | Searches issued in current 60s window, budget remaining, % of 30/min ceiling | The CRITICAL metric — central skill can do this; distributed cannot |
| **Cache hits** | `~/.octocode/repos/` reuse signals (24h disk cache per octocode-research.md §3.3) | Justifies repeat-invocation patterns |
| **Failures** | HTTP 403 count, timeout count, "no useful results" reformulation count, tool errors | Drives circuit-breaker decisions |
| **Caller identity** | Which skill/command/agent invoked (e.g., `tech-research:phase-4-agent-2`, `sc-troubleshoot:precedent-finder`) | Per-caller hit-rate analysis |
| **Output reuse rate** | Did downstream phases cite this output? Tracked via post-invocation hook | Detects wasted invocations |

### What gets instrumented (per session aggregate)

| Dimension | Measurement | Why it matters |
|---|---|---|
| **Cumulative octocode tokens** | Sum across all invocations vs total session token budget | Detect cumulative tax overrun |
| **Cumulative rate-limit budget** | Total searches across all invocations / minute window | The GLOBAL budget that distributed integration cannot enforce |
| **Per-caller invocation count** | Heatmap of which surfaces invoke most | Validates v2's "top 5 targets" hypothesis empirically |
| **Failure rate by tool** | `githubSearchCode` 403 rate, `packageSearch` not-found rate, etc. | Drives per-tool retry/fallback policy |

### Where the metrics land

Per invocation: `${TASK_DIR}.octocode-metrics/invocation-${ULID}.yaml` (when running in MDTM context)
Per session: `~/.octocode-funnel/sessions/${SESSION_ID}.jsonl` (append-only line-delimited JSON, one record per invocation)
Daily rollup: `~/.octocode-funnel/daily/${YYYY-MM-DD}.json` (cumulative budget tracking across sessions)

This is the part the distributed v2 plan has NO equivalent for. There is no global session-aggregate file in v2. Each T1-T6 surface is invocation-local.

---

## Instrumentation Schema

The skill writes a deterministic YAML record per invocation. Schema (concrete, not aspirational):

```yaml
# .octocode-metrics/invocation-01HXYZ123ABC.yaml
schema_version: 1
invocation_id: 01HXYZ123ABC      # ULID
session_id: 01HXAAA00000          # ULID for the parent Claude Code session
timestamp_start: 2026-05-30T05:47:12.034Z
timestamp_end: 2026-05-30T05:47:38.891Z
wall_clock_ms: 26857

caller:
  type: skill | command | agent
  name: tech-research
  surface: phase-4-agent-2        # caller-supplied sub-identifier
  invocation_context:             # optional, caller-supplied
    task_dir: .dev/tasks/to-do/TASK-RESEARCH-20260530-044428/
    parent_task_id: TASK-RESEARCH-20260530-044428

input:
  scope:
    codebases_requested:          # explicit, from caller
      - owner: pydantic
        repo: pydantic-ai
      - owner: openai
        repo: openai-python
    keywords: ["agent registration", "tool dispatch"]
    depth: standard               # quick | standard | deep
  budget_hint:
    max_search_code: 5
    max_search_pr: 3
    max_wall_clock_s: 60

tool_calls:
  - tool: packageSearch
    timestamp_offset_ms: 12
    success: true
    response_bytes: 1843
    response_tokens_est: 460
  - tool: githubViewRepoStructure
    timestamp_offset_ms: 1284
    success: true
    response_bytes: 4201
    response_tokens_est: 1050
  - tool: githubSearchCode
    timestamp_offset_ms: 3120
    success: true
    response_bytes: 8932
    response_tokens_est: 2233
    rate_limit_window_consumed_after: 4   # 4 of 30 used in current minute
  - tool: githubSearchCode
    timestamp_offset_ms: 4521
    success: false
    error: "HTTP 403: rate-limited"
    rate_limit_window_consumed_after: 30
    retry_attempted: true
    retry_succeeded: false

tool_call_counts:
  packageSearch: 1
  githubViewRepoStructure: 1
  githubSearchCode: 6              # 5 success + 1 failure
  githubSearchPullRequests: 2
  githubGetFileContent: 3

token_consumption:
  input_prompt_tokens: 1240
  octocode_response_tokens: 11_847
  total_invocation_tokens: 13_087
  cumulative_session_tokens_after: 47_220

rate_limit:
  searches_in_window_at_start: 0
  searches_in_window_at_end: 8
  window_ceiling: 30
  budget_consumed_pct: 26.7
  global_budget_consumed_pct: 41.2    # across ALL skill invocations this minute
  throttle_events: 1
  circuit_breaker_tripped: false

cache:
  disk_cache_hits: 0
  disk_cache_misses: 1
  cache_age_max_hours: null

outcome:
  status: partial_success           # success | partial_success | failed | rate_limited
  findings_written_to: ${TASK_DIR}research/web-02-github-pydantic-ai.md
  findings_bytes: 14_220
  precedents_emitted: 3              # count of `owner/repo@branch:path:line` citations
  fallback_to_tavily_triggered: false

post_invocation:
  consumer_phases_observed: []       # populated by downstream hook
  output_reuse_count: null           # populated when synthesis phase reads file
```

This schema is the contract Wave 5 and post-pilot retrospectives need. The distributed v2 plan produces NONE of this — each T1-T6 surface emits its own ad-hoc footer (T2's "Octocode Tool Usage Log") at best.

---

## Rate-Limit Budget Tracking (Central vs Distributed)

**This is the single strongest argument for centralization.**

### The math

GitHub Search API limit: **30 requests / minute** (octocode-research.md §4.3, the binding constraint per the Tavily-tier benchmark of bulk-parallel fan-out).

V2's per-surface caps:
- T2 (tech-research Phase 4): "max 8 github-flavored items per Phase 4 Deep tier × 5 searchCode each = 40 searches/minute IF all fire simultaneously" (per brainstorm/02 §Rate-limit / failure handling, line 464)
- T4 (sc-brainstorm Wave 2A): restrictive 4-tool whitelist, no explicit per-phase cap in fit analysis
- T5 (sc-troubleshoot Tier 2): "precedent-finder" uses `githubSearchPullRequests` + `githubSearchCode` + `githubGetFileContent` — no documented per-invocation cap
- T6 (/tdd): tier-gated, inherits T2's classification + Phase 4 caps
- T1 (deep-research agent): no per-invocation cap, behavioral router only
- T3 (/sc:research): user-explicit, "no auto-magic routing"

### The blind spot

If at minute T:00 the user runs `/sc:research --source octocode` (T3) while their previous turn's `tech-research` Phase 4 (T2) finished 30 seconds ago at minute (T-1):30, AND a background `sc-brainstorm` Wave 2A (T4) precedent enrichment is still running... what is the actual rate-limit budget consumed in window T:00?

**Distributed v2 cannot answer.** Each surface has its own cap that it respects in isolation. None of them know about each other. The user discovers the collision via HTTP 403, with no diagnostic trail.

### The math, concretely

Scenario: a user is doing a Deep-tier tech-research while also keeping `/sc:troubleshoot` open in a sibling session (both are common in IronClaude workflows).

| Surface | Per-invocation budget | Concurrent invocations | Searches/min upper bound |
|---|---|---|---|
| T2 Phase 4 (Deep) | 5 searchCode + 3 searchPullRequests | 8 parallel agents | 40 + 24 = **64** |
| T5 Tier 2 precedent-finder | unbounded in spec | 1 | ~10 (typical) |
| T4 Wave 2A precedent | unbounded in spec | 1-2 | ~6 |
| **Theoretical max** | | | **~80 searches/min** |
| **GitHub Search ceiling** | | | **30/min** |
| **Over-budget by** | | | **+167%** |

The distributed plan tries to manage this with per-surface caps that ASSUME each surface is the only consumer. It is not. The actual upper bound is 80, with no enforcement mechanism.

### What centralization buys

A single `octocode-funnel` skill maintains the canonical 60-second sliding window:

```python
# Sketch of the budget guard
class RateLimitBudget:
    WINDOW_SECONDS = 60
    CEILING = 30                 # GitHub Search API
    SOFT_CEILING = 24            # 80% — start throttling
    HARD_CEILING = 28            # 93% — refuse + queue

    def request_slot(self, caller_id) -> SlotDecision:
        consumed = self._count_in_window()
        if consumed < self.SOFT_CEILING:
            return SlotDecision.PROCEED
        if consumed < self.HARD_CEILING:
            return SlotDecision.PROCEED_WITH_WARNING(
                f"{consumed}/30 used, caller={caller_id}, throttling soon"
            )
        return SlotDecision.QUEUE_OR_FALLBACK(
            wait_seconds=self._seconds_until_slot()
        )
```

Now every caller — T1, T2, T3, T4, T5, T6 — gets a unified throttle decision before issuing a search. No coordination needed in the callers. The skill is the coordinator.

**Quantified benefit:** with a hard global cap, rate-limit failures drop from "potentially 80 searches in a 30-search window" to "guaranteed ≤30 with throttling kicking in at 24." That is mathematically the difference between zero 403 cascades and several per busy session.

The distributed v2 plan literally cannot implement this. There is no shared state across T1-T6.

---

## Token Cost Centralization

The context-tax math is the second strongest argument.

### Schema-load tax in the v2 plan

Per octocode-research.md §4.4: 14 tools × ~600-1200 tokens of schema each = 8,000-17,000 tokens of MCP context tax when octocode is loaded into an agent's available tool set.

V2 restricts to 5 cross-repo tools via `TOOLS_TO_RUN` (FINAL-RECOMMENDATIONS-v2.md §Common Risk Mitigations), reducing this to ~3,000-7,000 tokens per surface that loads octocode tools.

V2 loads octocode tools into:
- T1 deep-research agent (frontmatter `tools:` list — every invocation pays the tax)
- T2 Phase 4 github-flavored agents (each spawned agent pays the tax)
- T3 `/sc:research --source octocode` flag (when invoked, pays the tax)
- T4 sc-brainstorm Wave 2A precedent agents (when invoked, pays the tax)
- T5 precedent-finder Tier 2 agent (per-invocation tax)
- T6 /tdd Stage A + Phase 4 github-flavored agents (per-invocation tax)

**Per-session worst case (Deep tier, all surfaces fire once):**
- T1: ~3,000-7,000 tokens (one schema load in main agent)
- T2: ~3,000-7,000 × 8 parallel agents = **24,000-56,000 tokens** (each parallel agent loads its own schema)
- T3: ~3,000-7,000 tokens
- T4: ~3,000-7,000 × 2 agents = ~6,000-14,000 tokens
- T5: ~3,000-7,000 tokens
- T6: ~3,000-7,000 × 4 parallel agents = ~12,000-28,000 tokens

**Total tax (Deep-tier, all-surfaces session):** ~54,000-126,000 tokens of pure schema overhead before any actual search is performed.

### Centralized schema-load tax

The `octocode-funnel` skill loads octocode tools ONCE in its own context. Callers invoke the skill via a thin contract (a structured request) and receive a structured response. Callers do NOT load octocode tool schemas into their own agent contexts.

**Centralized worst case:** ~3,000-7,000 tokens, ONE TIME, in the funnel skill's context. Plus ~200-500 tokens per caller for the invocation contract (a few-line YAML request schema). Plus the orchestration overhead of skill invocation.

### Quantitative comparison

| Scenario | Distributed (v2) | Centralized (this proposal) | Savings |
|---|---|---|---|
| Deep-tier session, all 6 surfaces fire once each | 54,000-126,000 tok | 3,000-7,000 + (6 × 500) = 6,000-10,000 tok | **88-92%** |
| Standard-tier, only T2 fires (4 parallel agents) | 12,000-28,000 tok | 3,000-7,000 + (4 × 500) = 5,000-9,000 tok | **58-68%** |
| Quick-tier, only T4 fires (2 agents) | 6,000-14,000 tok | 3,000-7,000 + 1,000 = 4,000-8,000 tok | **33-43%** |
| Session with NO octocode use | 54,000-126,000 tok (still loaded everywhere) | 0 (skill not invoked) | **100%** |

The last row is the killer: in the v2 plan, EVERY session that touches T1-T6 pays the schema tax even when no octocode invocation happens, because the schemas are loaded with the agent's tool list. In this proposal, the schemas are loaded ONLY when the funnel skill is actually invoked.

### Honest counter-cost: per-call orchestration overhead

Centralization adds per-call cost: ~200-500 tokens for the invocation contract serialization, ~1-3s wall-clock for skill spawn (if implemented as a subagent), plus the funnel skill's own meta-prompt (~500-1500 tokens of skill-load overhead).

**Net cost (centralized) per invocation:** ~700-2000 tokens of overhead vs ~0 for a direct tool call in the distributed plan.

**Break-even point:** at ~10 invocations per session, the centralized plan's amortized cost per invocation is lower IF every caller would have otherwise loaded the full schema. Below 10 invocations, the orchestration overhead can exceed the schema-tax savings.

**Empirical question for the pilot:** what is the typical octocode invocation count per session? If it's 1-3, the centralized plan loses on tokens. If it's 5-15+, the centralized plan wins dramatically. The metrics schema above captures exactly this question.

---

## Failure Mode Observability

The third argument: outage and degradation visibility.

### V2's distributed failure model

Each T1-T6 surface implements its own failure handling:
- T2: "Tavily fallback on HTTP 403, 'Octocode Tool Usage Log' footer for Phase 6 QA"
- T4: "Fail-open per existing Wave 2A semantics; quality-tier degrades on failure"
- T5: "Hybrid Tier 1 conditional + Tier 2 type-gated"
- T6: "rf-qa-qualitative spot-checks precedents"

Each surface's failure path is bespoke. When octocode-mcp goes down at 03:14 UTC, the user sees:
1. T2 Phase 4 agents emit "Tavily fallback" markers in their files
2. T4 Wave 2A produces a thinner precedent.md
3. T5 troubleshoot reports a missing Precedent Card
4. T6 /tdd's Stage A returns empty
5. T1's behavioral router emits `fallback_reason: "octocode unavailable"`

Each surface separately surfaces the same root cause through 5 different artifacts in 5 different formats. There is no central log saying "OCTOCODE-MCP UNAVAILABLE 03:14-03:38 (24min outage)." The retrospective requires correlating 5 surfaces' artifacts manually.

### Centralized failure model

One circuit breaker. One log. One health check.

```
~/.octocode-funnel/health.log
2026-05-30T03:14:22Z STATUS=degraded REASON=mcp_unavailable CONSECUTIVE_FAILURES=3
2026-05-30T03:14:55Z STATUS=open REASON=circuit_breaker_tripped FAILURE_RATE=100%
2026-05-30T03:14:55Z BROADCAST callers=[tech-research, sc-troubleshoot, sc-brainstorm, /tdd, /sc:research, deep-research-agent] message="octocode unavailable, all invocations will fall through to caller-defined fallback"
2026-05-30T03:38:14Z STATUS=half_open RECOVERY_TEST=initiated
2026-05-30T03:38:16Z STATUS=closed RECOVERY=verified DOWNTIME_SECONDS=1434
```

**Quantified benefit:**
- Time-to-detect octocode breakage: distributed = "varies per surface, typically discovered when user reads the report and notices missing Precedent Cards" = minutes to hours. Centralized = first invocation after failure, ≤1 second.
- Mean-time-to-recovery on octocode outage: distributed = each surface independently retries on its own schedule. Centralized = single half-open probe + broadcast.
- Time to root-cause analysis: distributed = correlate 5 artifacts. Centralized = read health.log.

### What centralization enables that distributed cannot

1. **Cross-session outage detection** — daily rollup files (`~/.octocode-funnel/daily/2026-05-30.json`) reveal sustained issues invisible to single-session telemetry.
2. **Per-tool failure rate trending** — "githubSearchPullRequests has 12% failure rate this week vs 2% last week" — actionable signal.
3. **Caller-specific issue isolation** — "tech-research:phase-4 has 30% no-useful-results rate" → classifier is over-triggering on bad topics.

---

## Cost-Benefit Analysis (Quantitative)

A quantitative comparison of v2 distributed vs this centralized design:

| Dimension | v2 Distributed | Centralized (this) | Delta | Confidence |
|---|---|---|---|---|
| **Tool-schema tokens per session (Deep, all surfaces)** | 54,000-126,000 | 6,000-10,000 | **−88 to −92%** | High (math from §4.4) |
| **Tool-schema tokens per session (Standard, 1 surface)** | 12,000-28,000 | 5,000-9,000 | −58 to −68% | High |
| **Tool-schema tokens per session (zero octocode use)** | 12,000-28,000 (still loaded) | 0 | **−100%** | High |
| **Per-call orchestration overhead** | ~0 tokens | ~700-2,000 tokens | +700-2,000 tok/call | High |
| **Break-even invocations/session** | n/a | ~10 invocations | n/a | Medium (empirical) |
| **Rate-limit failures per Deep-tier session (theoretical max)** | Up to several 403s | 0 (hard global cap) | **−100%** | High (deterministic) |
| **Time-to-detect octocode outage** | Minutes-hours (per-surface) | <1 second (centralized health) | **−99%+** | High |
| **Mean-time-to-recovery on outage** | Per-surface retry schedules | Single half-open + broadcast | ~50% faster | Medium |
| **Effort to fix a bug in octocode-handling code** | Touch 1-6 files depending on bug | Touch 1 file (the skill) | **−83% touch surface** | High |
| **Effort to add a new octocode-using caller** | New octocode tool list + anti-trigger rules + fallback per caller | Add invocation contract call (~10 LoC) | **−95% per new caller** | High |
| **Time to fix a misuse (e.g., caller invokes for local question)** | Re-train all 6 surfaces' anti-trigger rules | Centralize anti-pattern detection in skill (one place) | −83% | High |
| **LoC for initial integration** | ~510 LoC across 6 files + Phase 0 | ~400-600 LoC for skill + ~30 LoC × N callers | Net wash for N=4; **−40%** for N≥6 | Medium |
| **Observability artifacts per session** | 0 (no central metrics file) | 1 metrics file + 1 rollup append | n/a | High |
| **Per-pilot data availability** | "deferred to pilot phase" | First-class output every run | Pilot phase becomes optional | High |

### Where centralization LOSES

| Dimension | v2 Distributed | Centralized | Delta |
|---|---|---|---|
| **Per-call wall-clock for cheap single-call use case** | ~1-3s direct call | ~2-5s with skill spawn | +1-2s |
| **Per-call tokens for 1-invocation sessions** | ~0 schema tax (if tool whitelist tight) | ~700-2,000 overhead | +700-2,000 tok |
| **Complexity of the skill itself** | n/a (no skill) | ~400-600 LoC skill + schema | Adds one component |
| **Reviewer cognitive load (one-time)** | Distributed = 6 small diffs | Centralized = 1 large diff | Up-front concentration of risk |

### The honest verdict

**Centralized wins decisively on:** rate-limit budget tracking, schema-tax for multi-call sessions, observability, outage recovery, per-caller-addition cost.

**Distributed wins on:** single-call wall-clock, zero-overhead for sessions that fire octocode exactly once, no new component to maintain.

**The empirical question is invocation density.** At 5+ octocode invocations per session, centralized dominates. At 1-2, the math is closer. The centralized skill's own metrics answer this question definitively after one week of real use — the distributed plan would require a separate instrumentation project.

---

## What This Means for Pilot Phase

V2 defers measurement to "pilot phase" (FINAL-RECOMMENDATIONS-v2.md §Common Risk Mitigations + §"What This Investigation Did NOT Cover" #2, #3, #6). The recommended roadmap says:

> Week 3-4: Phase 1 + Phase 2 PILOT (8 weeks accumulated experience)
> Measure: octocode invocation rate, hallucination count, context tax, user-visible quality improvement

**The v2 plan provides no instrumentation for any of these measurements.** It assumes the pilot will somehow produce data. The data sources are:
- "octocode invocation rate" — not centrally logged anywhere
- "hallucination count" — manual qualitative review per surface
- "context tax" — measurable only via ad-hoc token counting
- "user-visible quality improvement" — manual qualitative review

A centralized skill makes the pilot **a measurement consumer rather than a measurement infrastructure project.** Day-1 invocations produce structured metrics. Week-2 retrospective is a `jq` query over the JSONL rollup. Pilot phase decisions ("widen Heavyweight tier to Standard for T6" — exactly the F-as-rollout-gate from T6) become data-driven instead of judgment-driven.

**Specifically, the centralized metrics enable these pilot questions to be answered with data, not vibes:**

1. *What is the actual invocation count per session?* → `jq 'group_by(.session_id) | map(length)'` over JSONL
2. *Which caller surfaces show high failure rate?* → `jq 'group_by(.caller.name) | map({caller, failure_rate})'`
3. *What's the typical rate-limit headroom at peak?* → `jq 'max_by(.rate_limit.global_budget_consumed_pct)'`
4. *Are precedents being cited downstream?* → `output_reuse_count` aggregation
5. *Where is schema-tax math actually landing?* → token consumption rollup vs theoretical

The v2 plan cannot answer any of these without bolt-on instrumentation. This proposal answers all of them by construction.

---

## Anti-Pattern Detection

A centralized skill can programmatically reject misuse — distributed integration can only document it.

### Anti-patterns the skill detects and rejects

**AP1: Local-codebase question routed to octocode**
```yaml
input:
  scope:
    codebases_requested: []         # NO external codebases
    keywords: ["find the function that handles auth"]
```
The skill detects: empty codebases list + keywords reading as "find X in our code." Rejects with:
```yaml
outcome:
  status: rejected
  reason: anti_pattern_AP1_local_query
  redirect: "Use auggie (mcp__auggie__codebase-retrieval) for local codebase queries.
            octocode is for CROSS-REPO investigation only."
```

**AP2: Canonical API surface question routed to octocode**
The skill detects: keywords matching "what does X function do" + a recognized library name → suggests context7.
```yaml
outcome:
  status: rejected
  reason: anti_pattern_AP2_canonical_docs
  redirect: "Use context7 (mcp__context7__query-docs) for canonical maintainer docs.
            octocode reads implementations; context7 reads docs."
```

**AP3: News/announcements/pricing routed to octocode**
Detect keywords: "announced," "released," "pricing," "roadmap" without code-shape qualifiers → suggest Tavily.

**AP4: Rate-limit exhaustion repeat-invocation**
If caller invokes within 60s after a previous invocation that left budget at >90%, the skill returns a queued response with backoff timer rather than firing a new search batch.

**AP5: Stale precedent re-fetch**
If caller requests the same `owner/repo` + keyword tuple a second time within 24h (cache window), the skill returns the cached findings without re-fetching, but increments the `cache.disk_cache_hits` metric. Distributed plan cannot share cache across surfaces.

**AP6: Funnel-method violation**
If caller requests `githubGetFileContent` without prior `githubViewRepoStructure` or `githubSearchCode` in the invocation, the skill warns: "Funnel-method violation — prefer SEARCH/LOCATE before READ." Tracked in metrics for retrospective pattern analysis.

### Why this matters

Each anti-pattern represents a class of wasted invocation. In v2, anti-trigger rules are documented in 6 different files (T1's "4 explicit anti-triggers," T2's per-bucket triggers, T4's "6 anti-trigger rules," T5's type-gating, T6's tier-gating). Compliance is best-effort and varies per caller.

In this proposal, anti-patterns are **executable code in one place** that any caller automatically benefits from. Adding AP7 next quarter requires editing one file, not six.

---

## What This Cannot Do

Honest limits where centralization doesn't help — or hurts.

1. **Cannot eliminate per-call orchestration cost.** ~700-2,000 tokens and ~1-2s of overhead per invocation are real. For sessions with exactly one cheap invocation, distributed is genuinely cheaper.

2. **Cannot reduce schema bloat WITHIN the skill itself.** The funnel skill still loads all 5 cross-repo octocode tool schemas in its own context. We saved schema tax at callers, not at the skill.

3. **Cannot survive octocode-mcp's supply-chain risks.** Bus factor = 1, 194 npm versions in <12 months, telemetry leakage — these are inherent to octocode (octocode-research.md §4.1). Centralization doesn't help; it just means one place to swap when the rug pulls.

4. **Cannot make pilot phase faster.** Centralization adds upfront work (the skill itself, the metrics schema, the budget guard, the anti-pattern detector). The break-even on engineering hours is somewhere around 3-6 months of operational use, depending on how much instrumentation the team would have built anyway.

5. **Cannot prevent caller-side misuse of returned findings.** The skill can tag precedents with `evidence_quality: advisory_only`, but if a downstream synthesis agent treats them as evidence, the skill cannot intercept that. The "precedent ≠ evidence" boundary from T5 still requires caller discipline.

6. **Cannot bypass the LLM's natural-fallback-to-familiar bias.** T2's W1-B build-time classification fights this bias at task-build time. A centralized skill that callers invoke at run-time still has the same problem: if a caller's LLM doesn't think to invoke the skill, no centralization helps. (Mitigation: the skill is invoked from a small number of well-defined surfaces, each with explicit invocation triggers — but adoption discipline is still a caller-side concern.)

7. **Cannot retroactively instrument the existing v2 surfaces.** If v2 ships first and this proposal lands as a refactor later, the historical pre-skill invocations are unmeasured. Centralization is only as old as its first-day deployment.

8. **Cannot solve the "1-invocation session" cost.** For Quick-tier runs that fire octocode exactly once, the skill's overhead is pure overhead. The break-even math is honest about this.

9. **Cannot replace caller-side anti-trigger discipline entirely.** AP1-AP6 catch the worst misuse, but subtle misclassifications (e.g., "this is an architecture question, do I want precedent?") still require caller judgment. The skill helps the caller fail faster on obvious wrong-tool choices; it does not make all routing decisions.

---

## Bottom Line

If we cannot measure octocode usage, we cannot decide whether to expand or contract its footprint, whether to tighten or relax its rate-limit budget, whether v2's per-surface caps are too generous or too stingy, or whether any of T1-T6 is producing value worth the schema-tax.

The v2 plan distributes octocode access across 6 surfaces and bets the pilot phase will somehow produce these measurements. It will not, without separate instrumentation work that v2 doesn't scope.

A centralized `octocode-funnel` skill is justified — and ONLY justified — because it makes measurement a first-class output of every invocation. The architectural cleanliness (proposal A's territory) and contract-purity (proposal C's territory) are downstream consequences. The lens here is: nothing matters if we can't measure it, and right now we cannot.

If this proposal is rejected, the right next step is to add the same instrumentation to v2's distributed plan — at which point distributed loses its core advantage (small per-surface diffs) because each surface now needs to emit the same metrics schema. The centralized plan amortizes that cost across one component.

The measurement is the point.

## Status: Complete
