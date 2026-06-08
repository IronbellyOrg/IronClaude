# Variant 1 — Opus / Architect

## Summary

Treat the lookup table as a **per-source-file parsed-metadata cache** keyed by `source_path` with `spec_hash` invalidation — not as a request-keyed classifier cache. The classifier runs on every invocation (in a Haiku subagent) and produces a free-text intent label that is matched against the **already-cached** surface metadata via auggie or a cheap embedding-free string score. This factors the cache cleanly along the axis that actually changes (source files via `make sync-dev`) and keeps the axis that varies every call (user wording) out of the persisted state. MVP is a single `.dev/cache/sc-recommend/local-surface.yaml`, populated lazily, refreshed by `spec_hash` mismatch — borrowing the schema almost verbatim from `src/superclaude/cli/roadmap/convergence.py:DeviationRegistry`.

## Table Schema

Stored at `.dev/cache/sc-recommend/local-surface.yaml` (gitignored; not under `.claude/`, not under `src/`). Mirrors the `.roadmap-state.json` convention.

```yaml
schema_version: 1
generated: 2026-06-02T13:50:00Z
generator: sc-recommend/v0.1
surface_root: src/superclaude        # for worktree resolution
entries:
  - id: cmd:sc-adversarial            # kind:name
    kind: command                     # command | skill | agent | template
    source_path: src/superclaude/commands/adversarial.md
    spec_hash: 9f3a...e21d            # sha256 of file content
    mtime: 2026-05-29T11:04:18Z
    last_validated_at: 2026-06-02T13:50:00Z
    name: sc:adversarial
    description: "Structured adversarial debate..."
    category: utility
    activation_style: skill-indirected   # or inline | direct
    delegates_to: skill:sc-adversarial-protocol
    flags:                             # extracted from Options table
      - { name: "--compare", required: true,  type: "csv-of-paths" }
      - { name: "--focus",   required: false, type: "enum", values: ["structure","content"] }
      - { name: "--depth",   required: false, type: "enum", values: ["fast","standard","deep"] }
    argument_hint: "<files> [--focus ...] [--depth ...]"
    when_it_wins: "comparing 2-10 artifacts where debate-then-merge beats single review"
    when_native_beats_it: "single file, single concern — Read + judgement is cheaper"
    related: [skill:sc-reflect-protocol, agent:rf-qa]
    intent_tags: [adversarial-debate, compare-artifacts, merge-proposals]
    classifier_score_hints:            # cheap matchers for hot-path scoring
      keywords_hint: ["compare", "debate", "merge", "adversarial"]
      anti_keywords: ["single file", "summarize"]
```

`intent_tags` is the load-bearing field for matching. It is **derived once on insert** by the cold-path Haiku writer from the source file — not hand-curated. `classifier_score_hints` is an optimization: the hot path uses it for an O(N) string-score pre-filter before invoking the Haiku ranker, dropping ~80% of entries before any LLM work.

A parallel `plugin-ecosystem.yaml` exists with the same skeleton plus `source_url`, `install_command`, `fetched_at`, `ttl_days`.

## Hot-Path Control Flow

Parent (main model) holds **no recommend logic**. It does exactly two things: spawn the Haiku worker, surface its result.

1. **Parent** receives `/sc:recommend <goal>`. Reads `.dev/cache/sc-recommend/local-surface.yaml` (or the plugin file if `--plugin`) — a single file Read, ~200 lines for the current surface.
2. **Parent** spawns one Haiku subagent via the Agent tool with `model: haiku`, passing: the user request, the loaded table contents (inlined as YAML in the prompt), and the worktree root.
3. **Haiku** classifies the request into a free-text intent label + 1-3 intent_tags (no enum constraint — it's a hint, not a key). Cost: small. Pattern: `sc:task` compliance-tier classifier (`src/superclaude/skills/sc-task-protocol/`).
4. **Haiku** runs the cheap score-then-rank over the in-prompt table: keyword/anti-keyword match on `classifier_score_hints` produces top ~5 candidates; then a single ranking pass over those 5 picks the winner + 1 runner-up.
5. **Haiku** performs the R1/R2/R3 validation: for the winner only, Read the `source_path` and confirm `sha256(content) == spec_hash`.
   - **Match** → emit the refined prompt using the cached `flags`/`argument_hint`/`when_it_wins`, plus a `verified_sources` block citing the Read.
   - **Mismatch** → mark this entry stale (`status: stale`), return a `cache_miss: validation_stale` signal to the parent.
6. **Haiku** also returns `cache_miss: low_confidence` if its top candidate scored below a threshold (e.g., the second-best score was within 10% — ambiguous), or `cache_miss: unrecognized_surface` if the user's request mentions a name not in the table.
7. **Parent** writes the emitted prompt verbatim to the user. Cost target: < 10K tokens, < 15s. No cold-path machinery runs.

If step 5 or 6 signals `cache_miss`, the parent falls through to cold path — never re-runs Haiku in place.

## Cold-Path Control Flow

Cold path is the **existing skill, unchanged**, run inside a Haiku subagent, plus a writer step at the end.

1. **Parent** spawns a second Haiku subagent with the full current `sc-recommend` SKILL.md as the system context and the user request.
2. **Haiku** runs Phase 0 (Glob + auggie + per-candidate Read), Phase 1 (net-value), Phase 2 (prompt construction). This is the expensive path — but now isolated to misses.
3. **Haiku** returns the recommendation block to the parent **and** a structured `cache_update` payload: a list of `{id, kind, source_path, spec_hash, flags, intent_tags, when_it_wins, ...}` records for every candidate it verified (winner + runners-up + any new surface elements it discovered).
4. **Parent** merges the `cache_update` into `.dev/cache/sc-recommend/local-surface.yaml` using the atomic-write pattern from `convergence.py:DeviationRegistry.save()` (write `local-surface.yaml.tmp`, then `os.replace()`). Concurrency: take a `.lock` sentinel file with `O_EXCL`; if held, the second writer skips the update (the next caller will re-derive — losing a write is harmless because the next cold-path will redo it).
5. **Parent** emits the recommendation. Total cost is roughly today's number plus a small write — acceptable because this is < 20% of invocations.

The cold path **owns** schema evolution. If the parent loads a table with `schema_version` lower than the current code expects, it treats every entry as stale and lets the cold path repopulate naturally — no migration code.

## Haiku Invocation Pattern

Both hot and cold paths use the same shape, differing only in the system prompt and the auxiliary inputs:

```
Tool: Task (Agent)
Parameters:
  model: haiku                  # explicit model override
  subagent_type: general-purpose
  description: "sc-recommend hot-path lookup" | "sc-recommend cold-path miss"
  prompt: |
    <ROLE>
    You are the sc-recommend worker. You produce a refined paste-ready prompt.
    The parent model will surface your output verbatim — do not address the user
    conversationally. Respect rules R1/R2/R3 from sc-recommend SKILL.md.
    </ROLE>
    <REQUEST>
    User request: "<verbatim>"
    Worktree root: <cwd>
    Mode: local | plugin
    </REQUEST>
    <TABLE>
    <inlined YAML or "EMPTY — run cold path">
    </TABLE>
    <INSTRUCTIONS>
    [hot-path or cold-path instructions, conditional on TABLE presence]
    </INSTRUCTIONS>
    <RETURN>
    Emit a single JSON object: {status, mode, recommendation_kind, prompt_block,
    verified_sources, auggie_status, cache_miss?: ..., cache_update?: [...]}
    </RETURN>
```

The return contract reuses the SKILL.md `Return Contract` fields verbatim plus the two cache-specific fields. No new schema invented. The Agent-with-model-override pattern is the precedent cited in the seed brief (adversarial agent-spec).

## Plugin Table

Separate file: `.dev/cache/sc-recommend/plugin-ecosystem.yaml`. Same schema as local-surface plus `source_url`, `install_command`, `fetched_at`, `ttl_days` (default 14).

- `--plugin` mode loads **only** this file. The hot path never opens `local-surface.yaml` in plugin mode, and vice versa — enforced by a single `mode` parameter passed into the Haiku worker.
- Invalidation is TTL-based, not hash-based — the upstream content lives outside the repo, so `spec_hash` of a fetched-and-cached snapshot is meaningless after the upstream changes.
- Cold-path writer is the same flow but populates via `tech-research` / Tavily (per Phase 3 of SKILL.md). Cache update writes the snapshot.

## Invalidation Strategy

Two-layer invalidation, both cheap:

1. **Per-entry `spec_hash`**: when the hot path validates the winner (step 5 above), it re-hashes the source file and compares. SHA256 of a ~200-line markdown file is sub-millisecond.
2. **Bulk staleness via `make sync-dev` hook (later, scaling)**: a post-sync hook can mark the whole table stale by bumping a top-level `surface_generation` integer. The hot path compares table.surface_generation vs `.claude/.surface-generation`; mismatch triggers cold path for any entry that's been validated before this generation.

For MVP, only the per-entry hash check exists. The bulk hook is a scaling addition.

## Minimum Viable Cache

The smallest version that earns its keep:

- **One file**: `.dev/cache/sc-recommend/local-surface.yaml`. No plugin table yet.
- **Lazy population**: empty at start. First N invocations are pure cold path. Each cold path appends entries.
- **No `classifier_score_hints` field**: hot path just inlines the entire table and lets Haiku rank with no pre-filter. Works at current surface size (~118 entries × ~10 lines each ≈ 1200 lines ≈ ~6K tokens — comfortably under hot-path budget).
- **`spec_hash` invalidation only**: no `surface_generation`, no mtime checks, no bulk refresh.
- **No `--plugin` cache**: `--plugin` mode falls through to the existing skill every time. Local cache earns its complexity first.
- **No concurrency lock**: single-user dev environment; last-writer-wins is acceptable.

Total new code: one YAML reader/writer (~80 lines mirroring `DeviationRegistry`), one Haiku subagent prompt template, one parent-side dispatcher. Estimated ~250 LoC. Earns its keep on the first 5 hot-path hits.

## Scaling Path

In order of value:

1. **`classifier_score_hints` pre-filter** — drop in once MVP shows the inlined-table token cost climbing past 8K.
2. **`--plugin` table** — once `--plugin` usage is non-trivial and TTL refresh logic is justified.
3. **`make sync-dev` post-hook for bulk invalidation** — once we see stale-row hot-path validations failing often enough to matter.
4. **Concurrency lock** — once multi-session dev (multiple worktrees) shows cache corruption.
5. **Per-entry `eval_history` pointer** — link entries to the eval set so a failing eval can target-invalidate the offending row.
6. **Migration to SQLite** — only if YAML parse+load exceeds 1K tokens per invocation. Unlikely before surface > 500 entries.

Each addition is a leaf change — no rewrite of the MVP loop.

## Eval Methodology — Haiku vs Opus

Reuse the 6 cases at `.dev/eval-workspaces/sc-recommend/iteration-1/evals.json`. Run a **2×3 matrix**:

| Config | Model | Cache state |
|---|---|---|
| A | Opus | cold (no table) — baseline / iter-1 floor |
| B | Haiku | cold (no table) — Haiku-only on full pipeline |
| C | Haiku | warm (table pre-populated from one cold run) — the target |

6 evals × 3 configs = **18 runs**. Each eval is scored on the existing assertion set (binary per-assertion pass/fail), plus tokens and wall-time.

**Haiku wins** when:

- **Necessary**: pass rate ≥ Opus pass rate − 5% across all 6 evals (i.e., Haiku regresses on at most ~1.7 assertions out of 34 total — within tolerance).
- **AND tokens reduce ≥ 50%** in warm config (C) vs Opus cold (A). Below 50% the cache isn't earning the architecture cost.
- **AND no eval drops below 60%** individually (no catastrophic regression on a single case).

**Haiku loses** if pass rate gap > 5%, OR token reduction < 50% in warm config, OR any single eval drops below 60%. In any loss case, the fallback is: parent allows Haiku for classification only, hands the full pipeline to Opus on cache miss — a soft degradation, not project abandonment.

Run them with the existing eval harness; record results to `.dev/eval-workspaces/sc-recommend/iteration-2/` so iter-1 and iter-2 stay comparable.

## Open Risks

1. **Haiku's classification confidence may be miscalibrated** — it may emit "high confidence" on misclassifications, denying the cache the chance to fall through. Mitigation: the hot-path Read+hash validation catches misrouting at the source level, but cannot catch a *plausible-but-wrong* recommendation (recommending `/sc:tasklist` when the user wanted `/sc:roadmap`, where both exist and both validate). The 18-run eval is the only honest answer here.
2. **The inlined-table-in-prompt approach scales linearly with surface size**. At 118 entries it's fine; at 500 entries the hot-path prompt itself becomes the new cost center. The `classifier_score_hints` pre-filter is the planned answer, but the cutover threshold isn't proven.
3. **Free-text `intent_tags` are inconsistent across cold-path writes** — Haiku may tag the same skill differently on different cold-path invocations, fragmenting the match space. May require a normalization pass or a closed-enum migration in a later iteration.
4. **Worktree concurrency**: two worktrees on the same repo cold-path simultaneously will both append to `.dev/cache/sc-recommend/local-surface.yaml` (which lives at the repo root, not per-worktree). MVP punts via last-write-wins; if this causes real corruption, the lock comes in earlier than planned.
5. **`--plugin` cache TTL semantics are undefined** — 14 days is a guess. The plugin ecosystem may churn faster than that, and a stale install command is worse than no recommendation. MVP avoids the question by deferring the plugin cache entirely.
6. **The Haiku subagent's prompt currently inlines SKILL.md** for cold path, which puts the skill body inside a Haiku context window every miss. That re-introduces the same cost the cache is trying to remove. Mitigation: only inline a condensed cold-path runbook, not the full skill.
