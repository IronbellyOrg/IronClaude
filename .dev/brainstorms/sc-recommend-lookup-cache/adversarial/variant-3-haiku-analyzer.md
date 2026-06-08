---
variant: 3
author: haiku-analyzer
date: 2026-06-02
---

# Variant 3: Haiku Analyzer — Minimal Validation Cache

## Summary

The 91K / 72s cost is dominated by a single step: the Auggie semantic-ranking query (Phase 0, Step B). A lookup cache that removes only that one step — replacing it with a classification-driven table scan — captures the majority of the savings. No separate plugin table on day 1. No schema evolution. A single YAML file with a `source_hash` per row, validated by a single Read on hit.

## Cost Root-Cause Analysis

No per-step token trace exists in the eval data (`timing.json` files contain only totals; see `eval-2/with_skill/timing.json`: `total_tokens: 91590`). The breakdown below is reconstructed from tool-call counts and the SKILL.md pipeline definition (`src/superclaude/skills/sc-recommend/SKILL.md`, lines 38-103).

| Phase 0 step | Evidence | Est. tokens | % of 91K |
|---|---|---|---|
| A. Glob enumeration | 4 Glob calls per eval (commands, skills, agents, templates). File lists are short. | ~2K | 2% |
| B. Auggie semantic ranking | 1 `codebase-retrieval` call with the full enumerated surface (~120 names) in-context. Eval 2 output names 6 candidates with detailed justifications. Eval 5 (`--plugin`) skips Auggie entirely and costs 94K with only 7 tool calls vs eval 2's 92K with 11 calls — the difference is not Auggie itself but the Tavily search replacing it. The key evidence is eval 4 (native recommendation): the skill explicitly skipped Auggie ("Phase 1 net-value rubric pre-resolved the case; agent explicitly skipped Auggie sweep"), dropping to 78K tokens with 5 tool calls. Eval 6 also skipped Auggie and hit 71K / 4 tool calls. The 20-36K delta between Auggie-skipped and Auggie-invoked runs maps directly to the Auggie query + its context window. | ~42K | 46% |
| C. Per-candidate Read | Eval 2 Read 5 files (tech-research SKILL.md, deep-research-agent.md, MCP_Auggie.md, surface-enumeration.md, delegation-vs-native-heuristics.md). Eval 1 Read 3 files. Eval 3 Read 3 files. Average ~3-4 Reads at ~5K each. | ~18K | 20% |
| D. Net-value evaluation (Phase 1) | In-context reasoning, no tool calls. Baked into the model response. | ~6K | 7% |
| E. Skill body + prompt overhead | The SKILL.md itself is 225 lines. System prompt + skill body in context for the entire conversation. Diff vs baseline (63.8K avg) = 27.7K; subtract Auggie (~20K) and Reads (~6K) = ~2K overhead. | ~12K | 13% |
| F. Output construction | Formatting the recommendation block. | ~11K | 12% |

**Dominant cost driver: Auggie semantic ranking at ~46% of the 91K budget.** The second largest is per-candidate Read at ~20%. Together they account for two-thirds of the spend. A cache that eliminates both on the hot path reduces an invocation from 91K to roughly 15-20K.

## Skeptical Pressure on "Hot Path > 80%"

The seed brief assumes >= 80% of invocations will hit the cache. There is no empirical basis for this number in the eval data. The eval set contains 6 test cases covering fundamentally different request patterns:

- **Spec generation from matrices** (eval 1): Would hit a cache keyed on "spec generation" if one exists.
- **Codebase research** (eval 2): Would hit a cache keyed on "research codebase" if one exists.
- **Tasklist from spec** (eval 3): Would hit a cache keyed on "tasklist generation" if one exists.
- **Small util refactor** (eval 4): This is a **native-tooling case**. The skill explicitly rejected delegation ("Phase 1 net-value rubric pre-resolved the case"). A cache keyed on "refactor small util" would return "native: Read + Edit" — but that is trivially derivable without any cache. Caching native-tooling recommendations buys nothing.
- **Plugin mode** (eval 5): The cache layer explicitly does not apply to `--plugin` mode (separate tables, per seed-brief constraint).
- **Parallel research** (eval 6): Would hit a cache keyed on "parallel multi-file research" if one exists.

So of the 6 evals: 1 is plugin-mode (cache N/A), 1 is native-tooling (cache buys nothing), and 4 would plausibly benefit from a cache. That is 4/6 = 67%, not 80%. And those are carefully crafted eval cases. Real user requests will include ambiguous, multi-intent, or genuinely novel requests that no table row covers.

**Assessment:** 60-70% is a more defensible hit-rate estimate after warmup. Below 70%, the cache layer's complexity must justify itself purely on the 46% token saving from eliminating Auggie, not on eliminating the full pipeline.

## Table Schema

The smallest schema that removes the dominant cost:

```yaml
# .dev/cache/sc-recommend-lookup.yaml
schema_version: 1
rows:
  - key: "spec-generation"          # classification output (not keyword)
    candidate: "/sc:spec-panel"     # the recommended target
    flags: []                       # flags verified from source
    rationale: "builds specs from matrices; panel review"
    source_hash: "sha256:abc123..." # SHA256 of the candidate source file
    last_validated: "2026-06-02T..."
    native_fallback: false          # true if this row recommends native tooling
```

Five fields beyond the key. `source_hash` follows the `.roadmap-state.json` precedent (`src/superclaude/cli/roadmap/convergence.py`). No `eval_history`, no `last_hit_at`, no `related_skills`. If a row's hash mismatches the source file on validation, the row is stale and the cold path fires.

## Hot-Path Control Flow

```
1. Haiku classifies the user request into a discrete category string
   (e.g., "spec-generation", "codebase-research", "tasklist-build").
   This follows the sc:task compliance-tier classifier pattern
   (seed-brief enrichment context, line 97-102).

2. Table scan: find row where key == classification output.

3. If no row found -> cold path.

4. If row found: Read the candidate source file (one Read).
   Compute SHA256 of the source content.
   Compare with row.source_hash.

5. If hash matches: emit recommendation from row (candidate + flags).
   Done. ~3-5K tokens (classify prompt + table scan + 1 Read).

6. If hash mismatches: cold path (row is stale). Update row on return.
```

No Auggie. No Glob enumeration. No per-candidate multi-read. The single Read serves both validation and the R1/R2 anti-fabrication gate (the flags come from the file itself, not from the cache).

## Cold-Path Control Flow

```
1. Run the existing full pipeline (Phase 0: Glob + Auggie + Read + Phase 1).
2. The winner's classification key + candidate + flags + source_hash
   become a new row (or update the existing stale row).
3. Emit recommendation as normal.
```

The cold path is the current skill unchanged. The only addition is the write-back step (2). No new logic.

## Haiku Invocation Pattern

From the inside (Haiku executing this task):

**What works well:**
- Free-text to discrete-category classification. Haiku handled the sc:task compliance-tier analog reliably in prior evals (seed-brief line 97-98). The classifier prompt is short and deterministic.
- Table scanning. YAML key lookup is trivial.
- SHA256 comparison. String equality check, no reasoning.

**What is fragile:**
- Classification ambiguity. If a user request could map to two categories ("help me design and build a feature"), Haiku will pick one and the table lookup will return the wrong row. This is not detectable without a confidence score, which adds a step. **[HAIKU LIMIT FLAG]** I cannot confidently quantify Haiku's misclassification rate on open-ended user requests without running the eval set. On the 6 eval cases, the requests are narrow and unambiguous — a favorable sample.
- Table mutation. Haiku cannot write files directly. The cold path needs the parent to commit the row. This is not a Haiku limitation per se but a harness constraint.

**Key risk:** The classifier prompt must produce the same key for semantically equivalent but syntactically different user requests. "Help me build a spec from these matrices" and "generate specs from matrices" must both map to `"spec-generation"`. Without a canonical key vocabulary and few-shot examples in the classifier prompt, this is brittle.

## Plugin Table

**Does not need to exist on day 1.** The `--plugin` mode (eval 5) uses Tavily search, not a cached table. Plugin ecosystem data evolves externally and a cache would require a TTL + refresh strategy that adds complexity for a mode that represents a minority of invocations. The seed-brief constraint (separate tables) is satisfied by not having a plugin table at all initially. It can be added when a pattern emerges from real `--plugin` invocations.

## Invalidation Strategy

Two signals, both cheap:

1. **`source_hash` mismatch on validation Read.** Per row. If the cached SHA256 of `src/superclaude/commands/spec-panel.md` differs from the current file, that row is stale. The cold path fires and updates it. This is the `.roadmap-state.json` precedent (`spec_hash` field).

2. **Surface-level hash.** A single SHA256 of the concatenated Glob output (sorted file list) can be stored at the top of the YAML file. If a new command file is added or one is deleted, the surface hash changes and all rows are suspect. This catches renames and deletions that per-row hashes would miss.

No mtime checks. No git rev parsing. No cron. Invalidation is lazy and happens at the point of use.

## Minimum Viable Cache

The absolute smallest thing that earns its complexity:

1. One YAML file (`.dev/cache/sc-recommend-lookup.yaml`) with ~10 rows after warmup.
2. A Haiku classifier prompt (<= 20 lines) that maps user requests to keys.
3. A single Read per hot-path invocation for validation.
4. Cold path = current skill + write-back.

That is it. No plugin table. No row-level TTL. No confidence scoring on the classifier. No concurrency locks. No telemetry. The MVP eliminates the 46% Auggie cost on hit and the 20% per-candidate Read cost on hit, reducing hot-path invocations from ~91K to ~5-10K.

**"Do nothing" is defensible** if the use case is infrequent. But `/sc:recommend` is a utility skill that runs before other skills — if users invoke it repeatedly across a session (e.g., "what skill for X?" then "what skill for Y?"), the cumulative savings (40K per hit) justifies the ~200-line implementation.

## Eval Methodology — Haiku vs Opus

Same 6 eval cases, two model configurations:

| Configuration | Model for classifier + hot path | Model for cold path |
|---|---|---|
| A | Haiku | Haiku |
| B | Opus | Opus |

Success bar: Haiku pass rate >= Opus pass rate - 5 percentage points, with Haiku token cost < 50% of Opus token cost. If Haiku drops more than 5pp, the classifier prompt needs more few-shot examples or the key vocabulary needs to be constrained to a documented enum.

Run order: warmup (seed the cache with 3 rows from evals 1-3), then run all 6 evals under both configurations. Compare pass rate, tokens, and time. The without_skill baseline from iteration 1 (81% / 63.8K) serves as the floor — both configurations must beat it.

## Things This Proposal Does NOT Do

- **Does not cache native-tooling recommendations.** Eval 4 proved those are derivable without enumeration. Caching "use Read + Edit" for small refactors is overhead with zero return.
- **Does not pre-seed the table.** Lazy population (cold-path write-back) is simpler and the eval set shows only 4 cacheable cases. Eager seeding would cost one full pipeline run per row.
- **Does not add a plugin table.** Per the "Plugin Table" section above.
- **Does not implement confidence scoring on the classifier.** If misclassification is a problem, the fix is a better few-shot prompt, not a confidence gate that adds another LLM step.
- **Does not handle concurrent writes.** Two simultaneous cold paths might write the same row. Race condition is benign (same data) or results in a redundant row (dedup on next cold path). No lock needed at this scale.
