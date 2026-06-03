---
artifact: merged-requirements
brainstorm_topic: "sc-recommend lookup-table cache layer (Haiku-only)"
generated: 2026-06-02T14:25:00Z
revised: 2026-06-02T15:00:00Z
revision: round-3 (user feedback merge)
generator: sc:brainstorm v2.0 → sc:adversarial Mode B + round-3 user advocate
base_variant: V3 (haiku:analyzer)
incorporated_from: [V1 opus:architect, V2 sonnet:performance, R3 user advocate]
convergence_score: 0.82
adversarial_status: converged
---

<!-- Provenance: produced by /sc:brainstorm via /sc:adversarial Mode B + round-3 user merge -->
<!-- Base: Variant 3 (haiku:analyzer) — anchored on the 46% Auggie cost finding -->
<!-- Round 2 merge: 2026-06-02T14:25:00Z -->
<!-- Round 3 merge: 2026-06-02T15:00:00Z (user advocate: cache-path location, plugin eval pipeline, --eval flag, best_model per-row) -->

# Merged Requirements: sc-recommend Lookup-Cache Layer

## Headline Findings (load-bearing)

<!-- Source: V3 (Cost Root-Cause Analysis) — anchors the entire design -->

1. **Auggie semantic ranking is ~46% of the current 91K-token cost** (~42K). Per-candidate Read is ~20% (~18K). Together two-thirds of the spend. Reconstructed from per-eval token deltas: eval-2 (91K, 11 tool calls, auggie invoked) vs eval-4 (78K, 5 calls, auggie explicitly skipped) vs eval-6 (71K, 4 calls, auggie skipped).
2. **A cache that removes only Auggie + per-candidate Read on hits reduces a hot-path invocation from ~91K to ~5-10K tokens.** That is the single ROI lever.
3. **Hot-path hit rate is more defensibly 60-70%, not 80%.** Of the 6 iteration-1 evals: 4 are plausibly cacheable, 1 is plugin-mode (cache N/A), 1 is native-tooling (cache buys nothing). Real user traffic includes ambiguous and novel requests no row covers.
4. **Caching native-tooling recommendations buys nothing.** Eval 4 is the demonstration: "use Read + Edit" is trivially derivable. The cache scope is explicitly delegation-prompt rows only.
5. **(R3 user)** **Recommendations are model-conditional**, not just tool-conditional. The same recommended tool may be best invoked on different models depending on the task. The cache should encode `best_model` per row, populated from per-row evals, so future hot-path invocations get "use `/sc:X` AND spawn it on `<model>` because eval showed that's the quality/speed/cost optimum here."

## MVP Architecture

### Storage

<!-- Source: V3 + V2 + R3 (path location, schema additions for best_model + eval_history) -->

Two YAML files, both at `.claude/cache/` (a TRACKED location — see Gitignore Exception below):

- `.claude/cache/sc-recommend-lookup.yaml` — local-surface rows (commands, skills, agents, templates from `src/superclaude/`)
- `.claude/cache/sc-recommend-plugin.yaml` — external resources (plugins, MCP servers, community skills, agents from outside the project)

Mirrors `.roadmap-state.json` conventions per `src/superclaude/cli/roadmap/convergence.py`.

```yaml
schema_version: 2                              # bumped from 1 in round-3 (adds best_model + eval_history)
surface_hash: sha256:<hash of sorted Glob output>
generated: 2026-06-02T...
generator: sc-recommend-cache/v0.2

rows:
  - key: "spec-generation"                     # classification output (discrete category, not keyword)
    candidate: "/sc:spec-panel"                 # the recommended target
    flags: []                                   # verified from source
    prompt_envelope_template: |                 # hand-off skeleton, NOT protocol restatement
      Use /sc:spec-panel on the matrices at <PATH1>,<PATH2>.
      Expected deliverable: a structured release spec following release-spec-template.md.
    rationale: "panel review of specs built from matrix inputs"
    source_hash: sha256:abc123...               # SHA256 of the candidate source file
    last_validated_at: 2026-06-02T...
    native_fallback: false                      # true rows are SKIPPED — never reach the table scan

    # ── (R3) Eval-driven metadata — populated by --eval runs ──────────────
    best_model:
      model: "sonnet"                           # winner across quality/speed/cost
      tier: "balanced"                          # quality | speed | cost | balanced
      based_on: "iteration-3/run-007"           # eval run that produced this verdict
      confidence: 0.85                          # eval delta vs runners-up
    eval_history:
      - run_id: "iteration-3/run-007"
        date: "2026-06-15T..."
        eval_mode: "normal"                     # quick | normal | deep
        models_tested: ["opus", "sonnet"]       # one entry per model in the panel
        results:
          opus:    { pass_rate: 1.0, mean_tokens: 11800, mean_duration_s: 18, n_runs: 2 }
          sonnet:  { pass_rate: 1.0, mean_tokens:  8900, mean_duration_s: 12, n_runs: 2 }
        verdict: "sonnet: identical pass rate at 75% tokens and 67% time vs opus"
```

Six core fields per row, plus `prompt_envelope_template` (V2 graft), plus `best_model` + `eval_history` (R3 grafts). Native-tooling cases skip the table entirely (Hot-Path step 3).

### Gitignore Exception (R3)

The cache lives under `.claude/cache/` — a TRACKED directory, explicit user-authorized exception to the project's "never commit `.claude/` contents" rule (per CLAUDE.md). Rationale: the lookup table is a SHARED ARTIFACT that benefits all developers and CI; per-developer caches would defeat the cross-session amortization. Eval-run artifacts are equally shared (a Haiku-vs-Opus comparison done in one developer's session informs every other developer's hot path).

Required `.gitignore` additions (companion to the existing `!.claude/settings.json` exception):

```
# Existing
.claude/
!.claude/settings.json

# (R3) Lookup-cache tracked artifacts
!.claude/cache/
!.claude/cache/sc-recommend-lookup.yaml
!.claude/cache/sc-recommend-plugin.yaml
!.claude/cache/eval-runs/
!.claude/cache/eval-runs/**

# But re-ignore high-churn telemetry (per-session local data)
.claude/cache/sc-recommend-events.jsonl
```

The JSONL telemetry log stays gitignored (per-session, high-churn, noisy commits otherwise). The lookup tables and eval-runs are tracked.

**Per CLAUDE.md**: this exception is explicitly user-authorized in the same session — recorded here for audit. Future skill maintainers MUST NOT extend the exception further without equivalent user authorization.

### Hot-Path Control Flow

<!-- Source: V3 base + V1 ambiguity check + V2 budget gate + R3 best_model dispatch -->

Target: 5-10K tokens, <15s p95.

1. Parent receives `/sc:recommend <goal>`. Spawns ONE Haiku subagent (via Agent tool with `model: haiku`), passing: user request, mode (`local` or `plugin`), worktree root, contents of `.claude/cache/sc-recommend-lookup.yaml` or `.claude/cache/sc-recommend-plugin.yaml` (inlined; ~30 rows × ~12 lines = ~3-4K tokens at MVP surface size).
2. Haiku classifies request → `{classification_key, native_likely: bool, confidence_top2_delta: float}`. Pattern: the `sc:task` compliance-tier classifier in `src/superclaude/skills/sc-task-protocol/`.
3. **If `native_likely == true`** (e.g., 40-line refactor, single-line edit, file-read-and-explain): Haiku emits the native sequence directly. NO table lookup. NO source Read. (Eval 4 demonstration.)
4. **If `confidence_top2_delta < 10%`** (top-2 classifications scored close): treat as ambiguous → `cache_miss: low_confidence`, fall to cold path. **No extra LLM call for this check — the delta is already in step-2 output.**
5. Table scan: find row where `key == classification_key`. If no row → `cache_miss: no_key`, fall to cold path.
6. Validate: Read `row.candidate`'s source file (one Read), compute SHA256, compare against `row.source_hash`. Mismatch → `cache_miss: validation_stale`, fall to cold path AND mark row stale.
7. **(R3) Best-model hint**: include `row.best_model` in the emitted recommendation. The refined prompt the user pastes will explicitly state which model to spawn the recommended tool on (e.g., "Run `/sc:tasklist <spec>` — and per row-eval, sonnet is the quality/speed/cost optimum: prefer `--model sonnet` if the target skill honors model overrides"). If `best_model` is absent (row never evaluated), omit the hint and let the user/parent decide.
8. Emit recommendation: use `row.prompt_envelope_template` with substitutions for verified `row.flags`, user-provided file paths, and the best-model hint. Add a `verified_sources` block citing the Read.
9. **Budget gate**: if cumulative hot-path tokens exceed 10K (e.g., classifier verbose, table large after warmup), fall to cold path. Circuit breaker, not the expected case.
10. Write telemetry event (see Telemetry).

### Cold-Path Control Flow

<!-- Source: V3 base + V1 condensed-runbook + R3 --eval trigger + R3 best_model population -->

Cold path is the **existing `sc-recommend` skill, condensed**, run inside a Haiku subagent, plus a write-back step + optional eval trigger.

1. Parent spawns a second Haiku subagent. **System context is a ~50-line condensed cold-path runbook**, NOT the full 225-line SKILL.md. (V1 risk #6: full inlining re-creates the cost the cache removes.)
2. Haiku runs the condensed pipeline: Glob enumeration → one auggie semantic-rank call → per-candidate Read → net-value evaluation → prompt construction.
3. Haiku returns the recommendation block AND a structured `cache_update` payload: `{key, candidate, flags, prompt_envelope_template, source_hash, last_validated_at, native_fallback}`.
4. **Parent commits** the update to `.claude/cache/sc-recommend-lookup.yaml` (or `-plugin.yaml`) via atomic write (`tmp + os.replace()` per `convergence.py:DeviationRegistry.save()`). Haiku cannot write files; parent commits.
5. **(R3) If `--eval <mode>` was passed to the current invocation**: parent triggers the per-row eval pipeline (see `## --eval Flag` section). The eval populates `best_model` and appends an `eval_history` entry to the row, then re-commits.
6. Parent emits recommendation. Cost: ~today's number (~91K) plus one write, plus eval cost if `--eval` set.

### Haiku Invocation Pattern

<!-- Source: V3 + V1 + V2's "no parent fallback to Opus" framing -->

Both paths use the Agent tool with `model: haiku`. Prompt shape:

```text
<ROLE>
You are the sc-recommend worker. Produce a refined paste-ready prompt.
Parent surfaces your output verbatim — no conversational addressing.
Respect rules R1/R2/R3 from sc-recommend SKILL.md (no unverified flags,
no unverified commands, no protocol reimplementation).
</ROLE>
<REQUEST>
User request: "<verbatim>"
Mode: local | plugin
Worktree root: <cwd>
Eval mode (R3): none | quick | normal | deep
</REQUEST>
<TABLE>
<inlined YAML>   OR   <EMPTY — run cold-path>
</TABLE>
<INSTRUCTIONS>
[hot-path lookup runbook OR cold-path condensed pipeline]
</INSTRUCTIONS>
<RETURN>
JSON: {status, mode, recommendation_kind, prompt_block,
       verified_sources, native_likely, confidence_top2_delta,
       best_model_hint?: <model>,
       cache_miss?: <reason>, cache_update?: [<row>]}
</RETURN>
```

Parent's role: spawn, surface, commit cache update, trigger eval if `--eval` set. **Parent does not classify, scan, repair malformed rows, or silently fall back to Opus for the work itself.**

### Plugin Table (R3 — elevated from "deferred" to MVP-with-eval-mechanism)

<!-- Source: R3 user advocate — download/setup/eval mechanism added; status changed from "defer to phase 2" to "MVP with strict eval gate" -->

Separate file: `.claude/cache/sc-recommend-plugin.yaml`. Same schema as local-surface PLUS:

```yaml
rows:
  - key: "notion-mcp-server"                  # plugin name as the row key
    candidate: "notion-mcp-server (hosted)"   # human-readable identifier
    resource_kind: "mcp_server"                # mcp_server | plugin | community_skill | community_agent
    source_url: "https://mcp.notion.com/mcp"
    repo_url: "https://github.com/makenotion/notion-mcp-server"
    install_command: "claude mcp add --transport http notion https://mcp.notion.com/mcp"
    setup_steps:                               # ordered list, single-line bash
      - "claude mcp add --transport http notion https://mcp.notion.com/mcp"
      - "browser: complete OAuth flow at https://mcp.notion.com/auth"
    fetched_at: 2026-06-02T...
    ttl_hours: 24                              # 24h for hosted, 7d for community repos
    license: "MIT"
    citation_url: "https://developers.notion.com/docs/mcp"
    # ── R3: Eval-driven adoption gate ────────────────────────────────────
    adoption_status: "evaluated_positive"      # candidate | evaluated_positive | evaluated_negative | uninstalled
    eval_history:
      - run_id: "iteration-3/plugin-runs/notion-mcp-001"
        date: 2026-06-15T...
        eval_mode: "normal"
        ran_with_resource:
          pass_rate: 0.95, mean_tokens: 12000, n_runs: 4
        ran_without_resource:
          pass_rate: 0.65, mean_tokens: 18000, n_runs: 4
        delta: "pass +30pp, tokens -33%"
        verdict: "ADOPT — clear value delta on 4 Notion-touching eval cases"
    best_model:                                # same shape as local-surface rows
      model: "haiku"
      tier: "cost"
      based_on: "iteration-3/plugin-runs/notion-mcp-001"
```

**Plugin lifecycle** — 4 phases:

1. **Discovery**: `/sc:recommend --plugin <query>` (no eval mode) — same as current Phase 3 in `sc-recommend/SKILL.md`. Returns candidate(s) with metadata. **Does NOT commit a row.** This is the "browse" mode.
2. **Adoption proposal**: `/sc:recommend --plugin <query> --eval <mode>` — invokes the eval pipeline (next section) with the plugin INSTALLED vs UNINSTALLED on **synthetic eval cases generated from the plugin's stated capabilities and reviewed by the user**. Full pipeline spec in `round-4-synthetic-eval-cases.md` (Stages 1-3: capability extraction → case generation → user review gate). Round-3's "subset of local eval set" framing was wrong — local evals test the recommend skill itself, not external resources — and is superseded by the synthetic-case spec.
3. **Decision gate**: if eval delta meets adoption threshold (pass-rate +≥10pp OR token-cost -≥20% with pass-rate not regressing), row is committed with `adoption_status: evaluated_positive`. Otherwise written with `adoption_status: evaluated_negative` and surfaced to user with explanation — NOT used by future hot-path lookups for that key.
4. **Hot-path use**: future `/sc:recommend --plugin <query>` matches the row, emits the install command (if not already installed locally — detection via a `which`-style check) and the best-model hint.

**Critical scope notes:**

- Plugin install steps MAY require manual intervention (OAuth flows, env vars, API keys). The skill emits the install command and a `setup_steps` checklist; it does NOT attempt to auto-complete auth flows. User runs the install and confirms readiness before the eval runs.
- Plugin eval uses a SUBSET of the iteration-1 eval set relevant to the resource's domain (e.g., a Notion plugin gets evaluated against any eval case that touches notes/docs workflows). Not all 6 cases — that would be both expensive and meaningless for narrow-scope plugins.
- A plugin in `evaluated_negative` state stays in the table for 30 days (TTL field) so we don't re-evaluate the same plugin on every discovery query.

## `--eval` Flag (R3)

<!-- Source: R3 user advocate — new section -->

`/sc:recommend <goal> [--eval <mode>]` triggers a per-row / per-resource evaluation pipeline after the cold-path inserts (or refreshes) the lookup row. Default is `none` — no eval runs.

| Mode | Models tested | Runs per model | Total runs | Approx token cost | Approx wall time |
|---|---|---|---|---|---|
| `none` (default) | — | 0 | 0 | 0 | 0 |
| `quick` | opus only | 1 | 1 | ~90K | ~70s |
| `normal` | opus + sonnet | 2 each | 4 | ~360K | ~3 min |
| `deep` | opus + sonnet + haiku | 3 each | 9 | ~810K | ~10 min |

### Pipeline shape

For each model in the panel:
1. Spawn N parallel subagents on that model (N = runs per model).
2. Each subagent receives the same eval prompt (the user request that triggered the cold-path insert; this is the canonical request the row is supposed to handle).
3. Each subagent uses the SAME recommendation (the just-inserted row + its `prompt_envelope_template`) and produces the actual deliverable the user wanted (e.g., the spec from /sc:spec-panel).
4. Grade each subagent's output against assertions (the same assertion mechanism iteration-1 used).
5. Aggregate per-model metrics: pass rate, mean tokens, mean duration.

For plugins: each model runs are repeated TWICE — once with the plugin installed/enabled, once without — to compute the with/without delta.

### Selecting `best_model` from results

Three tiers, picked deterministically:

- `quality`: model with highest pass rate. Tie-break: lower mean tokens.
- `speed`: model with lowest mean duration above 70% pass rate (cannot win speed if quality floor missed).
- `cost`: model with lowest mean tokens above 70% pass rate.
- `balanced` (default): normalize (1 - pass_rate), tokens, duration each to [0,1] across the panel, sum with weights 0.5/0.25/0.25, lowest score wins.

The `best_model.tier` field records which tier was selected. If user runs `--eval` without specifying a tier preference, default `balanced` is used. Future addition: `--eval-tier quality|speed|cost|balanced` for explicit tier selection.

### CLI eval integration

Where possible, reuse the existing eval harness at `.dev/eval-workspaces/sc-recommend/iteration-N/` plus the build_benchmark.py / grader.py scripts already in this repo (from the iteration-1 work). The `--eval` flag should:

1. Generate (or reuse) an iteration directory `.claude/cache/eval-runs/iteration-<N>/` with the eval prompt + assertions.
2. Spawn parallel subagents per the mode matrix above.
3. Run the existing grader and aggregate scripts.
4. Write a per-row eval result JSON into `.claude/cache/eval-runs/iteration-<N>/row-<key>-results.json`.
5. The orchestrator extracts the `best_model` verdict and inserts it into the lookup-table row.

The eval-run JSON itself is tracked (committed). It's the historical evidence for future re-runs or audits.

### When `--eval` is NOT triggered

- Default mode (`none`): cold-path inserts a row without `best_model` populated. Future hot-path users get a recommendation without a model hint. They can re-run with `--eval` later to fill it in.
- Hot-path hits: never trigger eval. The whole point of the cache is to AVOID work.
- Cold-path misses where `--eval none`: same as a regular cold-path miss in the round-2 design.

The eval cost is opt-in and deliberate. Most invocations stay cheap.

## Invalidation Strategy

<!-- Source: V3 base + V1+V2 surface-hash convergence -->

Two signals, both cheap:

1. **Per-row `source_hash`** on hot-path Read (step 6 above). Free.
2. **`surface_hash` at YAML top**: SHA256 of `sorted(Glob('src/superclaude/{commands/*.md,skills/*/SKILL.md,agents/*.md}'))`. On hot-path start, Haiku checks current surface hash vs stored. Mismatch catches additions/renames/deletions.

For plugin rows: TTL-based per-row (`fetched_at + ttl_hours < now` → stale; trigger cold-path refresh on next match).

## Telemetry (MVP, load-bearing)

<!-- Source: V2 -->

Single JSONL log at `.claude/cache/sc-recommend-events.jsonl` (GITIGNORED — see Gitignore Exception). One line per `/sc:recommend` invocation:

```json
{"ts":"2026-06-02T...","mode":"local","cache_result":"hit","classification_key":"spec-generation","duration_ms":8240}
```

5 fields only: `ts`, `mode`, `cache_result` (one of `hit | miss_no_key | miss_low_confidence | miss_validation_stale | miss_budget_exceeded | cold_inserted`), `classification_key`, `duration_ms`.

### Kill switch (V2)

Rolling 50-invocation hit rate after 2 weeks:

- **≥ 80%** → cache paying off; consider scaling
- **60-80%** → keep measuring; don't expand scope
- **< 60%** → **disable cache**, keep instrumentation

## Eval Methodology — Two contexts

<!-- Source: V1's 2×3 matrix + R3 distinction between architecture eval and per-row eval -->

There are now TWO distinct eval contexts:

### Context A: Architecture eval (one-time, validates the cache design)

Reuse the 6 cases at `.dev/eval-workspaces/sc-recommend/iteration-1/evals.json`. Run a **2×3 matrix = 18 runs**:

| Config | Model | Cache state | Purpose |
|---|---|---|---|
| A | Opus | cold (no table) | Baseline / iteration-1 floor (86% / 91.5K / 72.3s) |
| B | Haiku | cold (no table) | Haiku capability ceiling |
| C | Haiku | warm (table from prior B run) | **The target — production cache** |

This runs ONCE during the rollout (iteration-2). Determines whether the cache architecture works.

### Context B: Per-row eval (continuous, populates best_model)

Triggered by `--eval <mode>` per `## --eval Flag` section. Runs whenever a new row is inserted or a user explicitly re-evaluates an existing row. Populates `best_model` and appends to `eval_history` per row.

This is a continuous, opt-in process. It's how the cache LEARNS over time.

### What "Haiku wins" means for Context A (must all hold)

1. C pass rate ≥ A pass rate − 5pp
2. Blended C tokens ≤ 35K mean
3. No eval drops below 60% pass
4. No R1/R2/R3 violation
5. Eval 4: NATIVE bypass works
6. Eval 6: parallel Agent fan-out works

### Failure-mode fallback ladder (Context A failure)

<!-- Source: V1 risk-mitigation -->

If Context A fails: soft degradation. Haiku stays as hot-path classifier; Opus runs cache-miss cold-paths only. If even classification fails: disable cache, return to iteration-1 baseline.

## Scaling Path

<!-- Source: V1 + V2 + R3 plugin elevation -->

In order of likely value, AFTER MVP Context A eval passes:

1. **`classifier_score_hints` field** — when inlined-table tokens > 8K or surface > 200 entries.
2. ~~`--plugin` cache table~~ — **R3 promoted to MVP** with eval gate.
3. **`make sync-dev` post-hook** to bump `surface_hash` eagerly.
4. **(R3) ~~Auto-eval on cold-path insert~~ — REJECTED by user (OQ1 round-3 resolution)**. Cold-path inserts populate the row with `best_model: null`; user must opt in with `--eval <mode>` per-invocation. Auto-eval was rejected because the ~90K-per-cold-path tax is unjustified when many cold-path rows will be looked up infrequently and never need a best_model verdict. Future hot-path callers get an "unevaluated" hint and can choose to re-run with `--eval` to populate.
5. **(R3) Cross-tier `best_model` selection** — currently `balanced` tier uses fixed weights (0.5/0.25/0.25). Surface a per-row override if a row's task is unambiguously quality- or cost-dominated.
6. **Per-row `eval_history` trimming** — keep last 3 eval runs per row to bound row size.
7. **Concurrency lock** — when multi-worktree development causes cache corruption.
8. **SQLite migration** — only if YAML parse > 1K tokens per call.

## Open Risks (load-bearing — read before implementing)

<!-- Source: V3 + V1 + V2 + R3 new risks from plugin eval mechanism -->

1. **Classifier stability (highest risk)**: see round-2. Mitigation: closed-enum key vocabulary, deliberate human-reviewed expansion.

2. **Hot-path hit rate may be < 70%**. Mitigation: kill switch.

3. **Haiku misclassification → plausible-but-wrong recommendation**. Mitigation: 18-run eval + fallback ladder.

4. **Cold-path SKILL.md inlining undoes the win**. Mitigation: condensed ~50-line runbook.

5. **One source-file hash misses cmd→skill delegation drift**. Mitigation: validate both files when `activation_style: skill-indirected`.

6. **(R3 — OQ2 user-resolved) Plugin install failures silently break the eval pipeline**. **Mitigation (user-confirmed, OQ2 round-3 resolution)**: `preconditions:` block in the synthetic eval suite YAML runs a self-check BEFORE any eval. For MCP servers, reuse `src/superclaude/cli/install_mcp.py:check_mcp_server_installed(server_name)` (already parses `claude mcp list`). For binary-based plugins, reuse `check_binary_available()`. **Failure mode is HARD-BLOCK** with an explicit message: "Plugin '<key>' not installed/configured. Run `<install_command>` and complete auth steps, then re-run with --eval <mode>." This is option (a) from OQ2 — no degraded-data flag fallback. Full precondition schema spec'd in `round-4-synthetic-eval-cases.md`.

7. **(R3) `--eval deep` cost (~810K tokens, ~10 min) is significant**. Users running it casually will burn budget. **Mitigation**: the flag default is `none`; the help text explicitly states cost per mode. Consider adding a "are you sure?" prompt for `deep` mode in interactive use.

8. **(R3) `best_model` may be miscalibrated by small N**. `--eval quick` uses 1 run per model — single-sample variance can produce wrong best_model verdicts. **Mitigation**: `best_model.confidence` field records eval delta vs runners-up; if confidence < 0.5, the hot-path hint is suppressed and the row is treated as "model-agnostic" until re-evaluated at higher mode.

9. **(R3) Eval-run artifacts under `.claude/cache/eval-runs/` will grow over time**. After 100 plugins evaluated × 9 runs each = 900 eval artifacts. **Mitigation**: trim policy — keep last 3 eval runs per row in `eval_history`, garbage-collect older artifacts in a maintenance pass (not on every invocation).

10. **80% hit-rate assumption not evidenced**. Mitigation: V3 60-70% working target + V2 kill switch.

11. **Plugin TTL semantics**: 24h hosted vs 7d community. May refresh too eagerly or stale too long. Mitigation: track via `eval_history` whether refreshed rows actually differ.

12. **Worktree concurrency**. MVP punts via last-write-wins.

## Things This Proposal Does NOT Do (intentional)

<!-- Source: V3 + R3 updates -->

- **Does not cache native-tooling recommendations.** Native cases skip the table.
- **Does not pre-seed the table.** Lazy population via cold-path write-back.
- **(R3 changed)** ~~Does not include a plugin table at MVP.~~ → **Plugin table is now MVP** with strict eval gate (R3).
- **Does not implement confidence-score gating on the classifier.** Uses free top-2-within-10% check.
- **Does not handle concurrent writes with a lock.** Single-user assumption.
- **Does not parent-fall-back to Opus inline.** Fallback is the explicit ladder (Context A failure mode).
- **Does not embedding-index the surface.** YAML scan is fine at MVP scale.
- **Does not derive `intent_tags` from sources.** Single `classification_key` per row.
- **(R3) Does not auto-trigger `--eval` on cold-path inserts.** Default is `--eval none`; user opts in. Auto-eval is listed in scaling path #4.
- **(R3) Does not auto-install plugins.** Setup commands are EMITTED, not executed. User runs the install + auth flow.
- **(R3) Does not adopt plugins with `adoption_status: evaluated_negative`.** Rows in that state are recorded (for "don't re-evaluate every discovery query" reasons) but never surfaced as hot-path recommendations.

## Implementation Order

1. **(R3)** Update `.gitignore`: add `!.claude/cache/`, `!.claude/cache/sc-recommend-lookup.yaml`, `!.claude/cache/sc-recommend-plugin.yaml`, `!.claude/cache/eval-runs/**`, and re-ignore `.claude/cache/sc-recommend-events.jsonl`.
2. Build the YAML reader/writer (~80 LoC mirroring `convergence.py:DeviationRegistry`).
3. Write the Haiku classifier prompt with closed-enum key vocabulary (~20 lines, ~10 keys, 3-5 few-shot examples per key from the eval set).
4. Write the condensed cold-path runbook (~50 lines distilled from current SKILL.md).
5. Wire the hot-path / cold-path dispatch in the parent (~150 LoC).
6. Wire JSONL telemetry append (~20 LoC).
7. **(R3)** Wire the `--eval` flag pipeline:
   - Parse `--eval <mode>`
   - Generate iteration dir under `.claude/cache/eval-runs/iteration-<N>/`
   - Spawn parallel subagents per the mode matrix
   - Run grader + aggregate
   - Compute `best_model` via deterministic tier selection
   - Insert into the just-written row
   - Estimate: ~200 LoC, reusing iteration-1's build_benchmark.py + grader.py.
8. **(R3)** Wire the plugin eval gate:
   - `--plugin --eval <mode>` triggers plugin discovery + install hint + self-check + with/without eval
   - Adoption-threshold logic (pass-rate +≥10pp OR token -≥20% no regression)
   - `adoption_status` writeback
   - Estimate: ~150 LoC.
9. Hand-validate the first 6 invocations against eval-1 cases (sanity).
10. Run the 18-run Context-A architecture eval matrix → iteration-2 results.
11. Compare to iteration-1 baseline.
12. **Decision gate**: if eval passes, commit. If close-fail, deploy fallback ladder. If bad-fail, disable cache, keep iteration-1 skill.

Estimated total new code: ~700 LoC (up from ~300 in round-2 due to --eval + plugin gate). Most of the new code reuses iteration-1 infrastructure. Risk surface still bounded by the kill switch + the explicit `evaluated_negative` plugin-rejection path.
