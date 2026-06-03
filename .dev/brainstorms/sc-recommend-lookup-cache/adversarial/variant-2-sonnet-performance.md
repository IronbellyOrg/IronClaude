# Variant 2 — Sonnet Performance Proposal

## Summary

The cheapest cache worth building is not a second recommendation engine. It is a small, hash-validated lookup table that removes the repeated 91K-token discovery loop from common requests while preserving the current anti-fabrication gate. Iteration 1 measured the current with-skill path at 91,535 tokens and 72.3s mean latency, with a worst observed local eval of 107,818 tokens / 62.0s and a 109.9s outlier on eval 1. Eval 2's timing file shows 91,590 tokens, 94.1s, and 11 tool uses for a case that ultimately recommended one auggie sweep plus native Reads; that is exactly the kind of stable answer a cache should amortize.

Performance target: hot path under 8K tokens and under 15s p95 after warmup; cold path can remain close to today's 91K / 72s because it should be under 20% of traffic and should write the row that prevents repeat misses. If hit rate is below 60% after two weeks of real usage, disable the cache and keep only the instrumentation.

## Table Schema (what fields, what storage format — but argue for the choices on cost grounds, not architecture)

Use two compact JSON files, not YAML and not SQLite:

- `.dev/sc-recommend-cache/local-surface.json`
- `.dev/sc-recommend-cache/plugin-ecosystem.json`

JSON is cheaper for a Haiku worker to validate deterministically: parse succeeds or fails, object keys are explicit, and no YAML indentation ambiguity burns reasoning tokens. SQLite is overbuilt until there are thousands of rows; the local surface is currently bounded by roughly 41 commands, 24 skills, 38 agents, and 15 templates. A single JSON file under 100KB is cheaper to Read than setting up query machinery.

Minimum fields per row:

- `schema_version`: integer; reject unknown versions.
- `mode`: `local` or `plugin`; prevents table bleed.
- `classification_key`: short enum-like key such as `structured-spec-generation`, `small-native-edit`, `parallel-agent-research`.
- `input_shape`: 1-2 sentence description of requests this row covers.
- `recommendation_kind`: `delegation_prompt`, `native_tooling`, `multi_path`, `plugin_candidate`.
- `target`: command, skill, agent, built-in tool sequence, or plugin name.
- `target_source_path`: only for local source-backed targets.
- `target_source_hash`: SHA256 of source content at last validation.
- `verified_flags`: flags or argument hints copied from source.
- `prompt_envelope_template`: hand-off skeleton, not protocol text.
- `native_fallback_reason`: required for native rows.
- `quality_notes`: known eval wins/failures.
- `last_hit_at`, `hit_count`, `miss_count`, `last_validated_at`.

Do not cache full source excerpts. Store only the hashes and compact extracted affordances. Every extra KB is paid on every hot-path Read.

## Hot-Path Control Flow

1. Parent spawns a Haiku worker with the user request and mode only.
2. Haiku Reads the correct table: local by default, plugin only with `--plugin`.
3. Haiku classifies request into one `classification_key` plus confidence.
4. If confidence is below 0.75, miss immediately.
5. Scan rows with matching `mode` and key; pick highest `hit_score`/quality row.
6. Validate one source-backed target by Reading `target_source_path` and checking SHA256 against `target_source_hash`. Built-ins are exempt.
7. If hash matches, emit the prompt envelope or native-tool sequence.
8. Append a tiny JSONL telemetry event: hit/miss, key, latency, tokens if available, validation result.

Budget: table Read 500-2,000 tokens, classifier 500-1,000, one source Read 1,500-4,000, output 500-1,000. Target total 4K-8K tokens and 6-15s. Compared with the 91,535-token mean, that is a 91-96% hot-path token reduction.

## Cold-Path Control Flow

Cold path is the existing Phase 0 pipeline with one extra responsibility: produce a row proposal. It should run when classification confidence is low, no row exists, validation hash mismatches, output would require an unverified flag, or the user request is genuinely novel.

The cold worker performs live enumeration, one auggie ranking, per-candidate Reads, net-value evaluation, and prompt construction. Then it writes a candidate cache row with the observed classification key, verified target, source hash, extracted flags, and a compact prompt envelope. Use atomic write via temp file plus replace. If two workers race, last writer wins only when source hash and schema version match; otherwise preserve both as separate candidate rows until a cleanup pass merges them.

Cold path success is not judged by latency; it is judged by whether the next semantically similar request hits.

## Haiku Invocation Pattern

All actual work must be in Haiku. The parent should not classify, scan, summarize, or repair malformed rows. Parent responsibilities are limited to spawning Haiku and relaying the result. If Haiku returns malformed JSON or confidence below threshold, the parent should report `clarification_needed` or `degraded`, not silently run Opus. That constraint keeps eval honest: the design either works on Haiku or it does not.

Use one Haiku worker for hot path. Do not split classification, validation, and emission into three subagents; spawn overhead would consume the latency savings. Cold path may use one Haiku worker that performs the full current procedure sequentially.

## Plugin Table

The plugin table is only read when `--plugin` is present. Its rows should be more conservative because external metadata changes without `make sync-dev`. Fields add `source_url`, `source_fetched_at`, `ttl_hours`, `install_command`, `compatibility_notes`, and `citation_url`. TTL defaults to 7 days for GitHub/community repos and 24 hours for hosted MCP endpoints or marketplace pages.

Cost rule: never Read plugin table in local mode. Eval 5 already proved plugin mode can pass but costs 93,802 tokens / 80.0s with the skill. A warm plugin row for common asks like Notion MCP should return in under 10K tokens, but only if stale citations trigger cold refresh instead of dragging web search into every call.

## Invalidation Strategy

Local invalidation is per-target SHA256, not mtime. Mtime is cheap but noisy across checkouts and sync-dev; hash directly answers whether the verified source changed. If table-level `surface_manifest_hash` changes, do not discard all rows. Instead, validate only the selected row's target source on hot path. Full manifest refresh can run during cold path or maintenance.

Plugin invalidation is TTL plus source URL refresh. If expired, miss to cold path. Do not emit stale install commands.

## Minimum Viable Cache

MVP should include only local mode and only the six eval-shaped rows from iteration 1:

1. spec/matrix to spec-panel or PRD decision row
2. codebase research path row
3. roadmap-to-tasklist handoff row
4. small native edit row
5. plugin mode row can be deferred unless `--plugin` is in MVP scope
6. parallel agent fan-out row

The first deliverable should not build a crawler, embedding index, or automatic bulk parser. Hand-seed these rows from the eval artifacts, run Haiku-vs-Opus eval, then add cold-path row insertion only after hot-path quality is proven.

## Scaling Path

After MVP passes, add lazy cold-path insertion for real misses. After at least 50 telemetry events, add ranking among multiple rows per key using observed pass/fix outcomes. Only after 200+ events and sustained hit rate above 80% should the table be eagerly precomputed from all commands/skills/agents. Premature eager indexing risks rebuilding the stale static mapping that the current skill intentionally removed.

## Eval Methodology — Haiku vs Opus (this is YOUR section — the deepest treatment goes here)

Run the same six iteration-1 cases under two model configs:

- Config H: Haiku-only cache worker.
- Config O: Opus-only cache worker with identical table, prompts, thresholds, and tools.

Each config runs each case twice: warm miss then warm hit. The miss run may cold-path and write/refresh the row; the hit run must use the table. That yields 24 runs: 6 cases × 2 models × 2 cache states. If budget is tight, prioritize the 12 hit runs because hot-path performance is the design objective, but do at least one miss run per eval to verify row creation.

Record for every run:

- pass/fail per existing assertions
- selected classification key
- confidence score
- hit/miss/stale/malformed
- table file read (`local` vs `plugin`)
- source file validated
- token count
- duration
- output length
- whether any unverified flag/command appeared

Haiku wins if all are true:

1. Hit-run pass rate is at least 86.1% overall, matching the current with-skill mean.
2. Haiku is within one assertion failure of Opus across the six hit runs.
3. No R1/R2/R3 safety failure occurs.
4. Mean hit tokens are below 8K and p95 hit latency below 15s.
5. For eval 4, Haiku emits native Read/Edit and stays under the 1,500-character anti-bloat assertion.
6. For eval 6, Haiku recommends parallel Agent fan-out explicitly, not sequential `/sc:research`.

Opus is not the production fallback. It is the diagnostic ceiling. If Opus passes and Haiku fails, the design has a Haiku capability problem. If both fail, the schema/keying is wrong. If Haiku passes but Opus is wordier/slower, that supports Haiku-only routing.

## Cost Analysis (token budget breakdown: hot-path target vs current 91K baseline; latency target vs current 72s)

Current with-skill mean: 91,535 tokens, 72.3s, 8.5 tool calls average. Baseline without skill: 63,781 tokens, 37.9s. The skill buys +5.55 percentage points pass rate for +27,754 tokens and +34.5s.

Hot-path target:

- parent spawn/envelope: 300-700 tokens
- Haiku classification: 500-1,000
- table Read/scan: 500-2,000
- one validation Read/hash: 1,500-4,000
- output: 500-1,000
- telemetry write: negligible

Expected total: 3.3K-8.7K tokens. Use 8K as the budget gate. Savings versus 91,535: about 83.5K tokens per hit, or 91.3%. At 80% hit rate with cold misses still costing 91.5K, blended cost is roughly 24.7K tokens: `0.8*8K + 0.2*91.5K`. That still saves about 66.8K tokens per invocation, or 73% blended.

Latency target: under 15s p95 hot path, under 10s median. At 80% hits and 72.3s cold misses, blended latency is about 26.5s if hot path is 15s; still better than the 37.9s no-skill baseline and far better than 72.3s current skill.

## Hit-Rate Measurement (how to instrument it; what counts as a hit; how to know when the cache is actually paying off)

Append one JSONL event per invocation to `.dev/sc-recommend-cache/events.jsonl`:

- `timestamp`
- `mode`
- `classification_key`
- `classification_confidence`
- `cache_result`: `hit`, `miss_no_key`, `miss_low_confidence`, `miss_stale_hash`, `miss_malformed_row`, `cold_inserted`
- `selected_target`
- `validated_source_path`
- `duration_ms`
- `tokens_estimated_or_reported`
- `quality_outcome` when eval-graded

A hit means: row selected, confidence >= 0.75, mode-correct table only, source validation passed or built-in exempt, and output emitted without cold path. A row that is read but fails hash validation is not a hit.

The cache pays off when rolling 50-invocation metrics show hit rate >= 80%, hot p95 < 15s, blended mean tokens < 35K, and no safety regression. Between 60-80% hit rate, keep measuring but do not expand scope. Below 60%, the cache is likely classifying too narrowly or real requests are too diverse.

## Unverified Premises (call out things the seed brief assumes that you are NOT confident hold — be skeptical)

1. The biggest unverified premise is that Haiku can reliably map free-form requests to stable classification keys without recreating a brittle keyword table. If this fails, hit rate collapses or wrong rows pass validation.
2. The 80% hit-rate target is assumed, not evidenced. The six evals are curated, not representative traffic.
3. Token counts for hot path are estimates. Actual Haiku subagent overhead may exceed the 8K target.
4. One source-file hash validation may not catch semantic drift across command + skill pairs when a command delegates to a skill whose file changed.
5. The current benchmark has only one run per configuration, so the 91.5K / 72.3s mean may be noisy.
6. Eval 2's 94.1s outlier may reflect subagent scheduling/tool latency rather than algorithmic work; caching may not remove all wall-clock variance.
7. Plugin cache freshness is harder than local cache freshness; TTL may either stale too long or refresh too often.
8. Cold-path self-writing by Haiku may create low-quality rows unless row proposals are validated by eval or a strict schema checker.
