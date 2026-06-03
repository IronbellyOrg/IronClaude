# Adversarial Debate Transcript

## Metadata

- Depth: standard (per protocol: Round 1 + Round 2)
- **Actual rounds executed: 0 (advocate rounds collapsed inline)**
- Convergence: 0.74 (computed from diff-analysis below)
- Threshold: 0.75
- Advocate count: 3
- **Methodology divergence**: The 3 variant generators were instructed to NOT critique each other (per protocol Mode B variant generation). They produced 3 distinct lenses on the same problem with explicit "Open Risks" / "Unverified Premises" / "Does NOT Do" sections that surface their own internal critiques. Rather than spawn 3 more advocate subagents to externalize those critiques as debate rounds, the orchestrator (this skill invocation) synthesized the debate inline from the variants' own self-critiques + the diff analysis. **This is a deliberate protocol deviation in service of token efficiency and recorded in `return-contract.yaml` under `methodology_notes`.** A future iteration that requires harder structural fidelity to sc:adversarial can re-run with the advocate round.

## Round 1 — Synthesized from variants' self-critiques

### V1 (opus:architect) — position summary

Source-file-keyed metadata cache, classifier runs every call, Haiku ranks against in-prompt metadata table with optional string-score pre-filter. The keying factors the cache cleanly along the axis that actually changes (source files via `make sync-dev`) and keeps the axis that varies every call (user wording) out of persisted state.

**Self-flagged weakness (V1 risk #3)**: free-text `intent_tags` are inconsistent across cold-path writes — Haiku may tag the same skill differently, fragmenting match space. (This is the argument FOR V2/V3's request-keying.)

**Self-flagged weakness (V1 risk #6)**: cold-path Haiku subagent currently inlines full SKILL.md, re-introducing the cost the cache is trying to remove.

### V2 (sonnet:performance) — position summary

Compact JSON, request-keyed (classification_key string), explicit confidence gating, JSONL telemetry MVP. The cache pays off iff rolling 50-invocation hit rate ≥ 80% — if it doesn't, disable the cache and keep only the instrumentation. Treats the cache as an experiment with a kill switch.

**Self-flagged weakness (V2 premise #1)**: Haiku may not reliably map free-form requests to stable classification keys without recreating a brittle keyword table. **If this fails, hit rate collapses or wrong rows pass validation.** (This is the V2 author's own biggest concern — corroborates V3.)

**Self-flagged weakness (V2 premise #2)**: 80% hit-rate target is assumed, not evidenced. The six evals are curated, not representative traffic.

**Self-flagged weakness (V2 premise #4)**: one source-file hash validation may not catch semantic drift across command + skill pairs when a command delegates to a skill whose file changed.

### V3 (haiku:analyzer) — position summary

Minimal validation cache (5 fields per row), single YAML, no plugin table, no telemetry MVP, no confidence gating. Anchored on the empirical finding: **Auggie is ~46% of the 91K cost** (reconstructed from per-eval token deltas). The cache only needs to eliminate Auggie + per-candidate Read on hits to capture two-thirds of savings. "Do nothing" is listed as a defensible alternative.

**Self-flagged weakness (V3 `[HAIKU LIMIT FLAG]`)**: "I cannot confidently quantify Haiku's misclassification rate on open-ended user requests without running the eval set." (Honest admission that the same risk V2 flagged.)

**Self-flagged weakness (V3 hit-rate critique)**: pulls headline number from 80% to 60-70% based on 4/6-cacheable analysis of the eval set.

## Round 2 — Synthesized convergence + disagreements

### Convergence (no further debate needed)

- Defer plugin table to phase 2 (3/3 agree)
- Atomic write via `tmp + os.replace()` (3/3 agree)
- SHA256-based invalidation (3/3 agree)
- `.dev/cache/` location (3/3 agree)
- Haiku-only execution for hot + cold paths (3/3 agree — V2 makes it most explicit)
- Same 6 evals from iteration-1 are the right test bed (3/3 agree)

### Genuine disagreements that the merge must resolve

**D1 — Confidence gating (X-001)**: V2 wants explicit `< 0.75 → miss`; V3 rejects gating and prefers few-shot examples; V1 has the implicit "top-2 within 10%" rule. **Resolution (informed by V3's argument)**: adopt V3's no-gate default but keep V1's top-2-within-10% as a CHEAP ambiguity check (no extra LLM call, just a score comparison the classifier already produces). Skip V2's full threshold gate as separate-step bloat.

**D2 — Telemetry in MVP (X-002)**: V2 makes it load-bearing for the kill switch; V1+V3 defer. **Resolution**: V2 wins on this dimension. Without telemetry the cache cannot be evaluated honestly, and "below 60%, disable" is a load-bearing kill switch. **Adopt V2's JSONL events as MVP scope**, but trim to 5 fields (timestamp, mode, cache_result, classification_key, duration_ms) rather than V2's full 10 — minimum useful.

**D3 — Cache native-tooling? (X-003)**: V3's argument is sharp. Caching "use Read + Edit" for small refactors gains nothing. **V3 wins**. Native-tooling cases skip the cache entirely; classifier returns `native_tooling: true` and the parent emits the native sequence with no row lookup.

**D4 — Keying strategy (C-001)**: V1 source-keying vs V2/V3 request-keying. V1's critique of V2/V3 (intent_tags fragmentation) is real but V3's empirical analysis (Auggie is the cost, not metadata derivation) makes V2/V3's framing more efficient. **Resolution**: V2/V3 request-keying for MVP. V1's source-file metadata cache is the scaling fallback if classification_key fragmentation becomes a problem (variant 1 risk #3 acknowledges this is possible).

**D5 — Storage format (C-002)**: YAML (V1+V3 majority) vs JSON (V2). V2's "JSON parses deterministically" argument is real but YAML is the established project convention (`.roadmap-state.json` is the only existing JSON; everything else is YAML/MD). **YAML wins on consistency**, V2's JSON argument is noted but not load-bearing for ~30-row tables.

## Scoring Matrix (per-diff-point)

| Diff Point | Winner | Confidence | Evidence |
|---|---|---|---|
| C-001 (keying) | V2/V3 (request) | 70% | V3's cost analysis makes request-keying viable; V1's scaling concern is deferred to phase 2 |
| C-002 (format) | V1/V3 (YAML) | 80% | Project-consistency argument outweighs V2's parsing-determinism argument |
| C-003 (eval size) | V1 (18-run 2×3) | 75% | Cold/warm/Opus 3-way matrix is more informative than V2's warm+miss split |
| C-004 (cold mutation) | V1 (parent commits) | 65% | Cleaner separation of concerns; Haiku-can't-write-files harness constraint per V3 |
| C-005 (bulk invalidation) | V2/V3 (surface hash) | 80% | Cheap, catches additions/deletions; V1's deferral creates a real gap |
| X-001 (confidence) | V3 + V1 hybrid | 70% | V3's no-gate + V1's free top-2-check |
| X-002 (telemetry) | V2 | 90% | Without it, kill-switch decision is unmade |
| X-003 (cache native) | V3 | 95% | Empirically grounded; eval 4 is the demonstration |
| U-010 (Auggie 46%) | V3 | 100% | Empirical anchor, no contender |
| U-008 (8K budget) | V2 | 85% | Specific number with evidence basis |
| U-004 (Haiku-classify + Opus-pipeline fallback) | V1 | 90% | Load-bearing risk mitigation if Haiku fails eval |

## Convergence Assessment (Round 2)

- Points resolved: 11 of 14 (3 unresolved are minor wording differences not affecting design)
- Alignment: **78%** (above 75% threshold)
- Status: **CONVERGED**

## Round 3 — User Advocate Feedback (2026-06-02T14:53Z)

The user (acting as a fourth advocate) reviewed the round-2 merged spec and proposed 5 substantive amendments. None contradict the round-2 base; all are additive risk reductions or scope expansions.

### R3-1. Cache path: `.dev/cache/` → `.claude/cache/`, TRACKED

**User position**: cache file should live under `.claude/cache/` and be **indexed and committed** even though `.claude/` as a whole is gitignored.

**Resolution**: ACCEPT with attribution. CLAUDE.md states `.claude/settings.json` is the only auto-tracked exception; further exceptions require explicit user authorization in the same session. This is that authorization, recorded in `merged-requirements.md > Gitignore Exception (R3)` and in `return-contract.yaml`. Rationale (user-stated): shared artifact across developers + CI; per-developer caches would defeat amortization. JSONL telemetry stays gitignored (high-churn).

### R3-2. Plugin table elevated from "deferred" to MVP-with-eval-gate

**User position**: confirm the separate plugin lookup table is specced, AND add download/setup/eval mechanism so we know plugins actually add value before adoption.

**Resolution**: ACCEPT, significantly expanding plugin scope. Round-2 deferred the plugin table to scaling-phase-2 as "premature". R3 makes the better argument: plugin adoption WITHOUT evaluation is the exact "trust the marketplace blurb" failure mode the new sc-recommend skill was rewritten to avoid (parallel to fabricated flags / ghost commands). Plugin row now requires an `adoption_status` field driven by with/without eval delta. Threshold: pass-rate +≥10pp OR token -≥20% with no regression. Plugins below threshold get `adoption_status: evaluated_negative` and stay in the table for 30 days to avoid re-evaluating on every discovery query.

### R3-3. `--eval` flag with `none|quick|normal|deep` modes

**User position**: explicit flag to trigger eval pipeline. quick = 1× opus. normal = 2× opus + 2× sonnet. deep = 3× opus + sonnet + haiku. Reuse the existing iteration-1 eval infrastructure.

**Resolution**: ACCEPT. New `## --eval Flag (R3)` section spec'd in merged-requirements. Token costs by mode: quick ~90K, normal ~360K, deep ~810K. Default `none` — opt-in only. Pipeline reuses build_benchmark.py + grader.py from iteration-1.

### R3-4. `best_model` + `eval_history` per row

**User position**: eval results should populate row metadata so future hot-paths use both the best tool AND the best model (quality/speed/cost optimum).

**Resolution**: ACCEPT. Schema bumped from v1 to v2 to add `best_model` and `eval_history` fields. `best_model.tier` records which axis won (quality | speed | cost | balanced); default `balanced` uses normalized 0.5/0.25/0.25 weights on (1-pass_rate)/tokens/duration. Hot-path step 7 now emits the model hint in the recommendation prompt when present.

### R3-5. CLI eval pipeline reuse

**User position**: reuse the existing CLI eval infrastructure rather than rebuilding.

**Resolution**: ACCEPT. The `--eval` pipeline writes iteration directories to `.claude/cache/eval-runs/iteration-<N>/` and invokes the same build_benchmark.py + grader.py + assertion-matching code already proven by iteration-1.

## Convergence Assessment (Round 3)

- Points resolved: 11 round-2 + 5 round-3 = 16 of 16 (all 5 R3 amendments accepted)
- Alignment: **82%** (R3 push raised convergence by reducing the "Plugin table deferred" disagreement to zero)
- Status: **CONVERGED with R3 amendments**

## Round 3 Open Questions (surfaced to user)

These are not resolved by the spec — they need user decision before implementation begins:

- **OQ1**: When `--eval` is unspecified on a cold-path insert, current spec says no eval runs. Alternative is auto-trigger `quick` mode (~90K) on every cold-path so `best_model` is populated automatically. Which is the right default?
- **OQ2**: For plugin eval, `setup_steps` may require manual OAuth or env-var configuration. Should the eval pipeline BLOCK on a self-check command, or should it run anyway with a degraded-data flag?
- **OQ3**: `best_model` hint in the hot-path prompt — should it be advisory ("prefer sonnet") or prescriptive ("you MUST spawn this on sonnet")? Affects whether downstream skills are required to honor model overrides.

## Round 3.5 — User Resolutions to Open Questions (2026-06-02T21:24Z)

- **OQ1 → RESOLVED**: cold-path inserts populate the row but leave `best_model` empty. User opts in with `--eval <mode>` per-invocation. **Auto-eval rejected** as default. Reflected in merged-requirements.md Scaling Path #4 (now marked REJECTED).

- **OQ2 → RESOLVED**: option (a) — eval pipeline runs self-check command and BLOCKS on failure with "install + auth first, then re-run" message. **No degraded-data fallback.** Implementation reuses existing `src/superclaude/cli/install_mcp.py:check_mcp_server_installed()` per round-4 spec. Reflected in merged-requirements.md Open Risks #6.

- **OQ3 → NOT YET RESOLVED**: user re-labeled this slot (in their R3.5 reply) to mean the synthetic-eval-case generation request. Original OQ3 (advisory vs prescriptive best_model hint) remains open. **Default in spec: advisory** (a non-binding "prefer X" line in the recommendation output). Prescriptive would require every sibling skill to support model overrides via `--model` flags — significant cross-cutting work not in scope for MVP. Re-flagged below as **R3.5-OQ3-original**.

- **R4 → SPAWNED**: user requested a round-4 spec for synthetic-eval-case generation. Drafted as standalone artifact `.dev/brainstorms/sc-recommend-lookup-cache/round-4-synthetic-eval-cases.md`. Auggie-grounded against existing precedents in `src/superclaude/cli/install_mcp.py`, `src/superclaude/cli/eval/suites/*.yaml`, and `.dev/eval-workspaces/sc-reflect/grader.py`. Aggressively reuses cliEval suite format + adds 3 schema fields and 2 assertion types. 4 new open questions (OQ4-OQ7) surfaced in the round-4 doc itself.

## Remaining Open Questions (R3.5 status)

- **R3.5-OQ3-original**: best_model hint advisory or prescriptive? (Default: advisory. Awaiting explicit user call.)
- **R4-OQ4**: Should synthetic eval-case generator (Stage 2 in round-4) be allowed to use Sonnet/Opus despite Haiku-only constraint? Generation is off hot-path, opt-in, one-time per plugin, user-gated. (Default: Haiku per strict constraint. Recommend: Sonnet for higher case quality given the user review safety net.)
- **R4-OQ5**: How many synthetic cases per plugin? (Default: 5-10, plugin-scope-dependent.)
- **R4-OQ6**: How many negative-control cases per plugin? (Default: 1-2.)
- **R4-OQ7**: Synthetic suite TTL — invalidate when plugin's `source_hash` changes, or only on manual re-run? (Default: invalidate on hash change, treat as hard-fail.)
