# Web Research: In-Process Import vs CLI-Subprocess Fan-Out

Topic: External grounding for TDD on re-wiring internal CLI reviewer fan-out
Date: 2026-06-20
Backend: Tavily MCP (mcp__tavily__tavily-search)
Status: Complete

Scope note: This is LIGHT supplementary grounding for §21 Alternatives and §6
design-decision rationale ONLY. The codebase is the source of truth; nothing
below overrides verified code behavior.

---

## Topic (a): In-process import vs CLI-subprocess fan-out (nested-subprocess avoidance)

### Finding A1 — Nested sub-agent/sub-process spawning silently fails; flat in-process is the reliable workaround [HIGH]
A Claude Code issue documents that sub-agents cannot spawn other sub-agents (the
`Task`/`Agent` primitive is not exposed in nested contexts); the nested spawn does
not error loudly — it "silently fail[s]" / "silently halt[s] at runtime," behaving
as if the tool was never requested. The community workaround is a "flat agent pool
with file-based handoffs" rather than hierarchical nesting. Directly mirrors the
TDD's premise.
URL: https://github.com/anthropics/claude-code/issues/61993
Relevance: HIGH

### Finding A2 — In-process mode can LOSE the spawn primitive entirely; corroborates "import, don't nest" [HIGH]
A second Claude Code issue reports in-process team agents "lack the Agent tool
(cannot spawn subagents)." The design must do the fan-out work directly
(in-process library calls / a thread pool) rather than delegating to spawned
children.
URL: https://github.com/anthropics/claude-code/issues/31977
Relevance: HIGH

### Finding A3 — "import is generally vastly preferable to spawning a separate process" [HIGH]
Canonical Stack Overflow guidance: running a separate process from within Python
"is frequently an antipattern… in the absence of factors which force the other
choice, `import` is generally vastly preferable" for usability and performance.
Supports the in-process-import direction.
URL: https://stackoverflow.com/questions/48862112/subprocess-or-import-to-invoke-a-script-in-python
Relevance: HIGH

### Finding A4 — Real multi-agent run: "Nested execution failed in practice" [MEDIUM]
A 16-agent documentation-refactor write-up lists "Nested execution failed in
practice" and "Rate limits hit 2 of 9 interviews" under what didn't work.
Independent corroboration that nested spawning is unreliable and API rate limits
are a first-class fan-out constraint.
URL: https://jonnyzzz.com/blog/2026/01/24/16-ai-agents-documentation-refactor
Relevance: MEDIUM

### Finding A5 — Subprocess/CLI fan-out's legitimate cost: per-process startup + serialization overhead [MEDIUM]
Replacing an in-process call with a subprocess "adds serialization overhead… [and]
the extra cost of starting the process." Honest §21 entry: subprocess fan-out is
simpler to isolate but pays a startup + IPC tax per reviewer.
URL: https://ricardoanderegg.com/posts/replace-ffi-cli-subprocess-call
Relevance: MEDIUM

---

## Topic (b): Python concurrent.futures / thread-pool fan-out idioms

### Finding B1 — ThreadPoolExecutor is the recommended executor for I/O-bound (network/API) fan-out [HIGH]
Std-lib docs + guides converge: for I/O-bound tasks (HTTP/API calls) use
`ThreadPoolExecutor`; reserve `ProcessPoolExecutor` for CPU-bound work. Multi-model
review calls are I/O-bound → ThreadPoolExecutor is the idiomatic fit.
URL: https://docs.python.org/3/library/concurrent.futures.html
Relevance: HIGH

### Finding B2 — Canonical submit + as_completed fan-out/fan-in with per-future error isolation [HIGH]
Submit each task, iterate `as_completed(futures)`, wrap each `future.result()` in
try/except so one reviewer's failure doesn't abort the batch. Exactly the
fan-out → collect → isolate-failures shape a reviewer ensemble needs (mirrors how
swarm's ParallelExecutor synthesizes a proxy_error result per failed slot).
URL: https://stackoverflow.com/questions/79390382/parallelize-a-list-of-subsequent-api-calls-in-python
Relevance: HIGH

### Finding B3 — executor.map vs submit/as_completed; rate-limited executor for API quotas [MEDIUM]
Prefer `submit`+`as_completed` when reviewers fail independently; wrap the executor
with a rate-limiter for provider quotas.
URL: https://oneuptime.com/blog/post/2026-01-30-python-concurrent-futures-thread-pools/view
Relevance: MEDIUM

### Finding B4 — ThreadPoolExecutor applied to parallel LLM API calls [MEDIUM]
Direct precedent: `ThreadPoolExecutor` to issue LLM API calls concurrently. The
thread-pool idiom is standard practice for parallelizing model calls.
URL: https://cloudaen.com/blogs/view/supercharge_llm_with_python_multithreading
Relevance: MEDIUM

### Finding B5 — Deadlock caveat: a pooled callable must not block on another Future in the same pool [MEDIUM]
Keep each reviewer task independent; do not have a pooled task block on a sibling.
URL: https://docs.python.org/3/library/concurrent.futures.html
Relevance: MEDIUM

---

## Topic (c): OpenAI-compatible multi-model parallel review / ensemble patterns

### Finding C1 — OpenAI-compatible proxy: one client, swap model=, fan out over N models [HIGH]
Instantiate a single OpenAI client with `base_url=<proxy>` and issue
`chat.completions.create(model=<name>, …)` once per model name to fan out across
heterogeneous providers behind one OpenAI-dialect endpoint — matches the project's
`~/.aienv` proxy contract (T2Model0N over a single base).
URL: https://www.truefoundry.com/blog/what-is-multi-model-orchestration
Relevance: HIGH

### Finding C2 — LiteLLM batch_completion_models — purpose-built parallel multi-model call [HIGH]
`batch_completion_models(models=[...], messages=[...])` makes parallel calls to
several models (fastest-response race or all-responses ensemble). Off-the-shelf
alternative to a hand-rolled thread pool. (Verify proxy-vs-SDK config + model IDs
against the live surface before adopting — do NOT probe the proxy API.)
URL: https://docs.litellm.ai/docs/completion/batching
Relevance: HIGH

### Finding C3 — Ensemble aggregation: statistical vote/mean vs meta-model reasoning aggregator [MEDIUM]
Statistical combination (majority/mean/weighted) is simple but uses fixed weights;
a meta-model that reasons over base outputs + original input adds per-instance
flexibility at extra cost. In this TDD the aggregator is `/sc:adversarial` Mode A
(a meta-model reasoning aggregator), not statistical voting.
URL: https://www.mdpi.com/1999-5903/18/2/112
Relevance: MEDIUM

### Finding C4 — Async/quota realities for parallel OpenAI-style calls [MEDIUM]
Budget ~half the official rate limit; implement retries ("1 retry fixes 90%… 2
retries fix 100%"). Reinforces bounded concurrency + retry/backoff — which swarm's
dispatch retry matrix (5xx→retry once) already implements.
URL: https://community.openai.com/t/parallelise-calls-to-the-api-is-it-possible-and-how/35498
Relevance: MEDIUM

---

## Key External Findings

1. Nested sub-agent/sub-process spawning is documented to fail *silently*; the
   field-tested remedy is a flat / in-process model with handoffs (A1, A2, A4) —
   strongest external validation of the TDD's core premise.
2. "Prefer import over spawning a subprocess" is long-standing Python consensus
   (A3); subprocess fan-out's honest cost is per-process startup + IPC (A5).
3. For I/O-bound parallel model calls, `ThreadPoolExecutor` + `submit`/`as_completed`
   + per-future try/except is the idiomatic std-lib fan-out/fan-in (B1, B2, B4);
   avoid in-pool Future-waits-on-Future deadlocks (B5). (Swarm's ParallelExecutor
   already embodies this — reflect imports it rather than re-implementing.)
4. An OpenAI-compatible proxy lets one client fan out across N heterogeneous models
   by swapping `model=`, the proxy normalizing responses (C1, C2).
5. Aggregation is a real design axis; here the aggregator is `/sc:adversarial`
   Mode A (meta-model), not statistical voting (C3). Bounded concurrency +
   retry/backoff is mandatory under quotas (B3, C4, A4).

## Recommendations from External Research (supplementary; codebase still governs)

- §6 rationale: cite A1/A2/A3 to justify in-process library import over
  CLI-subprocess fan-out (nesting unreliable; import lower-risk/lower-overhead).
- §21 Alternatives: (i) in-process import of swarm's existing thread-pool fan-out
  [recommended/chosen], (ii) CLI-subprocess/nested fan-out [reject: silent nesting
  failures A1/A2, startup+IPC tax A5], (iii) adopt a library (LiteLLM) [viable but
  duplicates swarm's hardened seam].
- Validate any external library's proxy config + `~/.aienv` model IDs against the
  live tool surface before adopting; do NOT probe the proxy API.

## Open questions / suggested follow-up

- All findings Tavily-sourced; no second-backend cross-check this session.
- Whether the internal proxy exposes a batch endpoint or only per-call
  `chat.completions` (determines library-vs-threadpool) — verify against codebase +
  `~/.aienv`, do NOT probe.
- Aggregation policy is settled by the spec: `/sc:adversarial` Mode A is the scorer.
