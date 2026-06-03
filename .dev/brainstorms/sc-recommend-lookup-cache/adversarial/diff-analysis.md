# Diff Analysis — sc-recommend Lookup-Cache Brainstorm

## Metadata

- Generated: 2026-06-02T14:20:00Z
- Variants compared: 3 (opus:architect, sonnet:performance, haiku:analyzer)
- Total differences found: 11 (3 structural, 5 content, 3 contradictions, 14 unique contributions, 6 shared assumptions)

## Structural Differences

| # | Area | V1 opus:architect | V2 sonnet:performance | V3 haiku:analyzer | Severity |
|---|---|---|---|---|---|
| S-001 | Section count | 11 sections | 13 sections (deepest eval-methodology) | 12 sections (distinct "Does NOT Do") | Low |
| S-002 | Cost-driver section | Implicit in scaling path | Quantified in Cost Analysis | Section 2 — dominant section, ~46% finding | High |
| S-003 | Open-risks framing | "Open Risks" (6 items) | "Unverified Premises" (8 items) | Inline `[HAIKU LIMIT FLAG]` markers + "Does NOT Do" | Medium |

## Content Differences

| # | Topic | V1 approach | V2 approach | V3 approach | Severity |
|---|---|---|---|---|---|
| C-001 | Keying strategy | Source-file-keyed (per-skill metadata cache); classifier runs every call to match request → cached metadata | Request-keyed (classification_key like `structured-spec-generation`) | Request-keyed (discrete category string) | **High** — central architectural divergence |
| C-002 | Storage format | YAML (one file) | JSON (two files) — argues JSON parses deterministically for Haiku | YAML (one file) | Medium |
| C-003 | Eval matrix size | 2×3 = 18 runs (Opus-cold, Haiku-cold, Haiku-warm) | 6×2×2 = 24 runs (model × cache-state warm+cold) | 2 configs = 12 runs (Haiku/Haiku vs Opus/Opus) | Low (all yield comparable signal) |
| C-004 | Cold-path mutation owner | Parent writes after Haiku returns structured `cache_update` | Cold Haiku worker writes directly via atomic temp+replace | Implies parent commits on Haiku return | Medium |
| C-005 | Bulk-invalidation primitive | Deferred to scaling (post-sync-dev hook) | `surface_manifest_hash` at table top | Surface-level SHA256 of sorted Glob output at YAML top | Low (V2 + V3 converge; V1 punts) |

## Contradictions

| # | Point of conflict | V1 / V2 / V3 positions | Impact |
|---|---|---|---|
| X-001 | Confidence gating on classifier | V1: implicit (`cache_miss: low_confidence` when top-2 within 10%); V2: explicit threshold (`confidence < 0.75` → miss); V3: **NO confidence scoring** ("the fix is better few-shot examples, not a gate") | **High** — affects classifier prompt design and cost. V2 adds a step; V3 argues it's wasted work; V1 splits the difference. |
| X-002 | Telemetry in MVP | V1: not in MVP (scaling addition); V2: **yes, JSONL events with hit/miss/key/latency/tokens are load-bearing for measuring whether cache is paying off**; V3: no telemetry in MVP | **High** — if cache pays off cannot be measured, the kill-switch decision (V2's "below 60% hit rate, disable") cannot be made. |
| X-003 | Cache native-tooling recommendations? | V1: silent (doesn't explicitly cover); V2: yes (table has `recommendation_kind: native_tooling` rows); V3: **NO — "caching 'use Read + Edit' for small refactors is overhead with zero return"** | Medium — V3's anti-bloat insight sharpens scope; V2's row coverage is broader but pays cost without benefit on a documented case (eval 4). |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | `classifier_score_hints` field (keywords/anti_keywords) for O(N) string pre-filter before Haiku ranking — scales when surface > ~200 entries | Medium (scaling) |
| U-002 | V1 | `intent_tags` derived from source by cold-path Haiku writer — multi-tag matching beyond single key | Medium |
| U-003 | V1 | `cache_miss: low_confidence` signal when top-2 scores within 10% (ambiguity detection) | Medium |
| U-004 | V1 | Fallback ladder: Haiku-classify + Opus-pipeline as soft degradation if Haiku-pure fails eval | **High** (de-risks the Haiku-only constraint) |
| U-005 | V2 | `prompt_envelope_template` field — store hand-off skeleton directly in row, not just metadata | **High** (lets hot path emit without re-deriving the envelope) |
| U-006 | V2 | `last_hit_at`, `hit_count`, `miss_count`, `last_validated_at` per row | Medium (telemetry for tuning) |
| U-007 | V2 | Plugin TTL bands (24h hosted, 7d repos) when plugin table arrives | Medium (future) |
| U-008 | V2 | 4K-8K hot-path budget gate — concrete number, evidence-backed | **High** (decision criteria) |
| U-009 | V2 | JSONL telemetry schema for hit-rate measurement | **High** (the kill-switch enabler) |
| U-010 | V3 | **Auggie cost finding: ~46% of 91K (~42K), Read 20% (~18K). Together 66%.** Reconstructed from eval-2 (91K, 11 calls) vs eval-4 (78K, 5 calls, auggie skipped) vs eval-6 (71K, 4 calls). | **Highest — single most load-bearing insight** |
| U-011 | V3 | "Hot-path > 80%" critique: 4/6 evals plausibly cacheable, 1 plugin, 1 native → **60-70% is more defensible** | **High** (recalibrates success bar) |
| U-012 | V3 | "Caching native-tooling recommendations buys nothing" — scope sharpener | High (anti-bloat) |
| U-013 | V3 | `[HAIKU LIMIT FLAG]` markers — explicit "I (Haiku) cannot quantify X" honesty | Medium (process honesty; also evidence Haiku CAN do this work given that V3 itself is Haiku-authored) |
| U-014 | V3 | "Do nothing" listed as defensible alternative if usage is infrequent | High (forces justification before building) |

## Shared Assumptions (UNSTATED preconditions promoted to debate points)

| # | Assumption | Source agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | Classification step is feasible on Haiku | All 3 variants assume Haiku can map free-text → stable category | **Highest** — if false, entire design fails | UNSTATED in V1; STATED in V2 (biggest premise); STATED in V3 (`[HAIKU LIMIT FLAG]`) — promote because V1 didn't acknowledge |
| A-002 | SHA256-on-Read is sufficient anti-fabrication gate (R1/R2/R3 compatible) | All 3 variants treat one Read + hash as full validation | Medium — could miss semantic drift across cmd→skill pairs (V2 calls this out) | STATED in V2 (unverified premise 4); UNSTATED in V1/V3 |
| A-003 | `make sync-dev` is the only source-changing event between Reads | All 3 implicitly assume sources don't change between source-of-truth-edits | Low (source-of-truth discipline holds in this project) | UNSTATED in all 3 |
| A-004 | A few-shot classifier prompt produces stable categories across phrasings of same intent | V3 calls this out as the key risk; V1/V2 assume it | High | STATED in V3; UNSTATED in V1/V2 |
| A-005 | Concurrent writes are benign (same data, last-write-wins) at single-user scale | All 3 punt concurrency at MVP | Low | STATED in all 3 |
| A-006 | The cache file under `.dev/cache/` (vs `.claude/` vs `src/`) is the correct location | All 3 place cache under `.dev/` | Low (matches .dev/README.md convention) | STATED in all 3 |

## Summary

- Highest-severity items: C-001 (keying strategy), S-002 (cost-driver framing), X-001 (confidence gating), X-002 (telemetry MVP), X-003 (cache native?), U-010 (Auggie 46% finding), A-001 (Haiku classification feasibility)
- Strong convergence: defer plugin table (all 3), atomic write tmp+replace (all 3), SHA256 invalidation (all 3), `.dev/cache/` location (all 3)
- One load-bearing empirical finding (U-010) that should anchor the merged proposal
- One central architectural disagreement (C-001 keying) where the V2+V3 majority pulls toward request-keying but V1's source-keying has merit at scale
