# Research: Classifier and Dispatch

Status: Complete
Date: 2026-06-03

Topic: Classifier + Hot/Cold-Path Dispatch + Cold-Path runbook condensation + Python-vs-prose boundary evidence.

---

## Section 1 — The CURRENT Cold-Path (sc-recommend SKILL.md + 3 refs)

Source files (all verified, Read in full this turn):

- `src/superclaude/skills/sc-recommend/SKILL.md` (227 lines — note: brief says 226, actual 227)
- `src/superclaude/skills/sc-recommend/refs/surface-enumeration.md` (108 lines)
- `src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md` (98 lines)
- `src/superclaude/skills/sc-recommend/refs/plugin-ecosystem-sources.md` (103 lines)

This is the COLD-PATH that must (a) condense to a ~50-line runbook and (b) survive as the fallback.

### 1.1 — Frontmatter (SKILL.md:1-7) — LOAD-BEARING, keep verbatim

- `name: sc-recommend`
- `description:` (SKILL.md:3) — the long delegation-prompt-builder description with `--plugin` ecosystem-search clause.
- `allowed-tools: Read, Glob, Grep, Bash, mcp__auggie__codebase-retrieval, mcp__tavily__tavily-search, mcp__tavily__tavily-extract, WebFetch, WebSearch` (SKILL.md:4)
- `argument-hint: "[goal description] [--plugin]"` (SKILL.md:5)
- `category: utility` (SKILL.md:6)

The new lookup-cache hot path will need `model:haiku` Agent invocation + deterministic Python (sha256, YAML, JSONL). Note `allowed-tools` does NOT currently list `Edit`/`Write`/`Agent`/`Task` — the hot-path cache-write + Haiku-dispatch will require expanding this. (Evidence flag for boundary question, Section 5.)

### 1.2 — Phase 0: Mandatory Surface Enumeration + Auggie Sweep — THE GATE (SKILL.md:38-85)

Hard gate: "Do not advance to Phase 1 until BOTH steps have landed or the documented degradation notice has been emitted." (SKILL.md:40)

Rationale baked in (SKILL.md:42): old skill failed because discovery was a hand-curated 10-row keyword table that went stale (missed `/sc:spec-panel`). "There is no static mapping in this skill."

- **Step A — Live surface enumeration (Glob)** (SKILL.md:44-57). Globs (from surface-enumeration.md:13-24, 8 patterns):
  - `src/superclaude/commands/*.md` (command index)
  - `src/superclaude/skills/*/SKILL.md` (skills src-of-truth)
  - `.claude/skills/*/SKILL.md` (skills dev mirror)
  - `src/superclaude/agents/*.md` + `.claude/agents/*.md` (agents)
  - `src/superclaude/templates/workflow/*.md`, `src/superclaude/templates/documents/*.md`, `examples/*-template.md` (templates)
  - Drift rule: if src/ and .claude/ disagree, trust `src/`, note in `degradation_notes` (surface-enumeration.md:26).
  - Worktree-aware: paths relative to cwd, not `/config/workspace/IronClaude/` (SKILL.md:55, surface-enumeration.md:28-30).
- **Step B — MANDATORY auggie semantic ranking** (SKILL.md:59-65). ONE `mcp__auggie__codebase-retrieval` query ranks the whole enumerated surface; query shape returns top 3-5 candidates with (1) summary, (2) when-it-wins-over-native, (3) flags/inputs, (4) caveats, (5) related skills. Full query template surface-enumeration.md:36-51. "One query. One." (surface-enumeration.md:34).
- **Step C — Per-candidate verification (prerequisite gate)** (SKILL.md:67-76). For each auggie candidate, BEFORE recommendation: (1) Direct Read of source file (extract flag table, required-inputs, activation handoff, return contract); (2) record auggie usage notes. Source missing = ghost, drop silently. Exempt: built-in tools + abstract MCP names (SKILL.md:76).
- **Graceful degradation table** (SKILL.md:80-85): auggie unavailable → Glob+Read only + header notice; auggie empty → note gap + proceed; candidate source missing → drop; request too vague → ask ONE clarifying question.

Supporting detail in surface-enumeration.md: verified-candidate-record YAML schema (lines 75-92), cardinality bound (3 candidates max into Phase 2, 1 auggie call total — lines 97-99), clarify-vs-guess rule (<50% fit confidence → one clarifying question — lines 101-107).

### 1.3 — Phase 1: Net-Value Evaluation (anti-bloat default) (SKILL.md:87-103)

Three explicit questions per surviving candidate (SKILL.md:91-93): (1) does invoking add value beyond a 2-3 step Read/Grep/Glob/Edit/Write seq? (2) is overhead justified by capability the model lacks natively? (3) would a senior engineer choose this delegation or roll it themselves faster?

If "no"/"barely" → DEFAULT TO NATIVE. Anti-bloat is core, not optional (SKILL.md:99). The valid native output form is at SKILL.md:97. Smallest-delegation-that-wins (SKILL.md:101).

Rubric detail in delegation-vs-native-heuristics.md: 5 net-value axes (capability/scope/output-structure/token-budget/repeatability, lines 19-54), command-vs-skill-vs-agent tier choice (56-72) incl. parallel agent fan-out special case, explicit native-only cases (74-87), tie-break heuristic (89-97).

### 1.4 — Phase 2: Refined Prompt Construction (SKILL.md:105-135)

Prompt is a HAND-OFF ENVELOPE, not a specification. Carries: target invocation, verified params/paths/flags, deliverable shape, worktree-aware paths. MUST NOT restate target protocol logic (SKILL.md:114). Output template SKILL.md:118-133 (Goal / Recommended delegation / Paste-ready prompt fenced block / Sources verified). Native recommendation → drop prompt block, numbered tool list (SKILL.md:135).

### 1.5 — Phase 3: `--plugin` Mode (ecosystem search) (SKILL.md:137-160)

When `--plugin` set, IGNORE local surface entirely; search plugin/community-skill ecosystem. In-scope: Claude Code plugin marketplaces, community skill repos. Out-of-scope: raw MCP server marketplaces (unless user explicitly asks). Search priority: tech-research skill → deep-research agent → Tavily MCP → WebFetch/WebSearch. Per-candidate return: name, capability summary, install command (single-line bash), repo URL, integration notes, version/compat caveats, citation. Full detail plugin-ecosystem-sources.md (scope 5-17, search priority 19-27, query patterns 29-44, result format 46-94, citation discipline 96-98, anti-bleed 100-102).

### 1.6 — Rules R1-R4 (Anti-Fabrication) (SKILL.md:162-185) — ALL LOAD-BEARING

- **R1 — No unverified flags** (SKILL.md:166-168): a flag may appear only if in verified target's flag table / `argument-hint`. Fabricated flags forbidden.
- **R2 — No unverified commands or skills** (SKILL.md:170-172): only if source file resolved in Phase 0 Step C. Auggie-mentioned-but-not-resolved → drop. Memory-recalled-but-not-resolved → drop.
- **R3 — No protocol reimplementation (THE load-bearing rule)** (SKILL.md:174-181): when target is `activation_style: skill-indirected`, generated prompt MUST be hand-off not specification. Allowed vs Forbidden examples at 178-179. "invoke, don't reimplement."
- **R4 — Built-ins exempt** (SKILL.md:183-185): Read/Grep/Glob/Edit/Write/Bash/TodoWrite/WebFetch/WebSearch recommended by name without verification.

### 1.7 — Return Contract (SKILL.md:187-197) + Boundaries (199-220)

Return contract table fields: `status` (success|clarification_needed|degraded|plugin_search), `mode` (local|plugin), `recommendation_kind` (delegation_prompt|native_tooling|multi_path|plugin_candidate), `prompt_block`, `verified_sources`, `auggie_status` (ok|unavailable|empty), `degradation_notes`. Boundaries Will/Will-Not lists (201-220) — notably Will-Not: static keyword→category mapping, invent flags/commands, restate protocol inline, mix local+plugin, execute the prompt, estimate time/budget/tokens, detect language, detect framework.

### 1.8 — Load-bearing vs cuttable for the ~50-line condensed runbook

LOAD-BEARING (must survive condensation — these ARE the fallback correctness guarantees):

1. The Phase 0 GATE itself: enumerate-live-surface → auggie-rank → verify-against-source. This is the anti-staleness contract; it is the whole reason the skill was rewritten (SKILL.md:42, surface-enumeration.md:7-9).
2. Rules R1-R4 (anti-fabrication). R3 especially — drift-prevention.
3. Phase 1 anti-bloat default (native-first). Without it the engine over-recommends delegation.
4. Graceful degradation when auggie unavailable.
5. Return contract field set (the hot path must emit the same contract shape for parity).

CUTTABLE / MOVABLE TO REFS (already partially in refs — runbook can cite, not inline):

- Verbose rationale paragraphs (the spec-panel war-story can compress to one clause).
- The full auggie query template (lives in surface-enumeration.md:36-51 already — runbook cites ref).
- The 5-axis net-value rubric detail (lives in delegation-vs-native-heuristics.md — runbook keeps the 3 questions, cites ref for axes).
- The full `--plugin` source list (lives in plugin-ecosystem-sources.md — runbook keeps the one-line "if --plugin, see ref").
- Output-template ASCII blocks (can compress; the shape is the contract, the formatting is not).
- Boundaries Will/Will-Not prose (the Will-Not list is partly redundant with R1-R4).

NET: the ~50-line runbook = frontmatter + Phase 0 gate (compressed, citing surface-enumeration.md) + Phase 1 three-question native-first default + Phase 2 hand-off rule + Phase 3 one-liner + R1-R4 (kept tight) + Return Contract table. Everything else delegates to refs.

---

## Section 2 — Hot/Cold-Path Dispatch Design (merged-requirements.md)

Source: `.dev/brainstorms/sc-recommend-lookup-cache/merged-requirements.md` (435 lines, Read in full).

### 2.1 — The ROI lever (Headline findings, lines 21-29)

- Auggie semantic ranking ≈ 46% of current ~91K-token cost (~42K); per-candidate Read ≈ 20% (~18K). Together ~two-thirds (line 25).
- Cache removes Auggie + per-candidate Read on hits → hot-path drops from ~91K to ~5-10K tokens (line 26).
- Hit rate target 60-70%, not 80% (line 27). Of 6 iteration-1 evals: 4 cacheable, 1 plugin-mode (N/A), 1 native-tooling (cache buys nothing).
- Caching native-tooling recs buys nothing → cache scope = delegation-prompt rows ONLY (line 28).
- (R3) Recommendations are model-conditional, not just tool-conditional → `best_model` per row (line 29).

### 2.2 — HOT-PATH control flow (10 steps, lines 107-122) — VERBATIM STRUCTURE

Target: 5-10K tokens, <15s p95 (line 111).

1. Parent receives `/sc:recommend <goal>`. Spawns ONE Haiku subagent (Agent tool, `model: haiku`), passing: user request, mode (local|plugin), worktree root, inlined contents of the relevant cache YAML (~30 rows × ~12 lines ≈ 3-4K tokens at MVP). (line 113)
2. Haiku classifies → `{classification_key, native_likely: bool, confidence_top2_delta: float}`. Pattern: `sc:task` compliance-tier classifier in `src/superclaude/skills/sc-task-protocol/`. (line 114)
3. If `native_likely == true` (40-line refactor, single-line edit, file-read-and-explain): Haiku emits native sequence directly. NO table lookup, NO source Read. (Eval 4.) (line 115)
4. If `confidence_top2_delta < 10%` (top-2 close): ambiguous → `cache_miss: low_confidence`, fall to cold path. NO extra LLM call — delta already in step-2 output. (line 116)
5. Table scan: find row where `key == classification_key`. No row → `cache_miss: no_key`, fall to cold. (line 117)
6. Validate: Read `row.candidate` source file (one Read), compute SHA256, compare vs `row.source_hash`. Mismatch → `cache_miss: validation_stale`, fall to cold AND mark row stale. (line 118)
7. (R3) Best-model hint: include `row.best_model` in emitted recommendation; refined prompt states which model to spawn the tool on. If `best_model` absent (never evaluated), omit hint. (line 119)
8. Emit recommendation: use `row.prompt_envelope_template` with substitutions for verified `row.flags`, user file paths, best-model hint. Add `verified_sources` block citing the Read. (line 120)
9. Budget gate: if cumulative hot-path tokens > 10K, fall to cold path. Circuit breaker, not expected case. (line 121)
10. Write telemetry event. (line 122)

Note the 5 cache-miss exits funnel to cold path: `low_confidence` (step4), `no_key` (step5), `validation_stale` (step6), `budget_exceeded` (step9); plus `native_likely` (step3) which exits WITHOUT cold path (emits native directly).

### 2.3 — COLD-PATH control flow (6 steps, lines 124-135)

Cold path = existing `sc-recommend` skill CONDENSED, run inside a Haiku subagent, + write-back + optional eval trigger (line 128).

1. Parent spawns a SECOND Haiku subagent. System context = ~50-line condensed cold-path runbook, NOT the full 225-line SKILL.md. (V1 risk #6: full inlining re-creates the cost the cache removes.) (line 130)
2. Haiku runs condensed pipeline: Glob enumeration → ONE auggie semantic-rank call → per-candidate Read → net-value eval → prompt construction. (line 131)
3. Haiku returns recommendation block AND structured `cache_update` payload: `{key, candidate, flags, prompt_envelope_template, source_hash, last_validated_at, native_fallback}`. (line 132)
4. PARENT commits the update to the YAML via atomic write (`tmp + os.replace()` per `convergence.py:DeviationRegistry.save()`). Haiku CANNOT write files; parent commits. (line 133)
5. (R3) If `--eval <mode>` passed: parent triggers per-row eval pipeline → populates `best_model` + appends `eval_history`, re-commits. (line 134)
6. Parent emits recommendation. Cost: ~91K + one write + eval cost if `--eval`. (line 135)

### 2.4 — Haiku Invocation Prompt Shape (lines 137-170) — VERBATIM 5-block envelope

Both paths use Agent tool, `model: haiku`. Prompt blocks (lines 143-168):

- `<ROLE>`: "You are the sc-recommend worker. Produce a refined paste-ready prompt. Parent surfaces your output verbatim — no conversational addressing. Respect rules R1/R2/R3 from sc-recommend SKILL.md."
- `<REQUEST>`: User request "<verbatim>"; Mode: local|plugin; Worktree root: <cwd>; Eval mode (R3): none|quick|normal|deep.
- `<TABLE>`: `<inlined YAML>` OR `<EMPTY — run cold-path>`.
- `<INSTRUCTIONS>`: [hot-path lookup runbook OR cold-path condensed pipeline].
- `<RETURN>`: JSON `{status, mode, recommendation_kind, prompt_block, verified_sources, native_likely, confidence_top2_delta, best_model_hint?: <model>, cache_miss?: <reason>, cache_update?: [<row>]}`.

Parent role (line 170): spawn, surface, commit cache update, trigger eval if `--eval` set. "Parent does not classify, scan, repair malformed rows, or silently fall back to Opus for the work itself." — KEY boundary statement (see Section 5).

### 2.5 — Local-surface YAML row schema (schema_version 2, lines 44-79)

File header fields: `schema_version: 2`, `surface_hash: sha256:<hash of sorted Glob output>`, `generated`, `generator: sc-recommend-cache/v0.2`.

Per-row fields (`rows:`):
- `key` — classification output (discrete category, NOT keyword). e.g. `"spec-generation"`.
- `candidate` — recommended target. e.g. `"/sc:spec-panel"`.
- `flags` — verified from source. (list)
- `prompt_envelope_template` — hand-off skeleton, NOT protocol restatement (multiline `|`).
- `rationale` — one-line why.
- `source_hash` — SHA256 of candidate source file.
- `last_validated_at` — timestamp.
- `native_fallback` — bool; `true` rows are SKIPPED, never reach table scan (line 60).
- `best_model` (R3): `{model, tier: quality|speed|cost|balanced, based_on: <eval run>, confidence: <delta vs runners-up>}`.
- `eval_history` (R3): list of `{run_id, date, eval_mode: quick|normal|deep, models_tested: [...], results: {<model>: {pass_rate, mean_tokens, mean_duration_s, n_runs}}, verdict}`.

"Six core fields per row, plus `prompt_envelope_template` (V2 graft), plus `best_model` + `eval_history` (R3 grafts)." (line 79)

### 2.6 — Plugin-table schema (lines 172-222)

File: `.claude/cache/sc-recommend-plugin.yaml`. Same schema as local-surface PLUS (lines 178-209):
- `key` — plugin name as row key. `candidate` — human-readable identifier.
- `resource_kind` — `mcp_server | plugin | community_skill | community_agent`.
- `source_url`, `repo_url`, `install_command`, `setup_steps` (ordered single-line bash list).
- `fetched_at`, `ttl_hours` (24 hosted / 7d community), `license`, `citation_url`.
- `adoption_status` — `candidate | evaluated_positive | evaluated_negative | uninstalled`.
- `eval_history` with `ran_with_resource` / `ran_without_resource` deltas, `delta`, `verdict`.
- `best_model` — same shape as local rows.

Plugin lifecycle 4 phases (lines 211-216): Discovery (`--plugin <query>`, no commit) → Adoption proposal (`--plugin <query> --eval <mode>`, installed-vs-uninstalled synthetic eval) → Decision gate (threshold: pass +≥10pp OR token -≥20% no regression → `evaluated_positive`; else `evaluated_negative`) → Hot-path use. `evaluated_negative` rows stay 30 days (TTL) so they aren't re-evaluated every discovery query (line 222).

### 2.7 — Invalidation strategy (lines 279-288)

Two cheap signals:
1. Per-row `source_hash` on hot-path Read (step 6). Free.
2. `surface_hash` at YAML top = `SHA256(sorted(Glob('src/superclaude/{commands/*.md,skills/*/SKILL.md,agents/*.md}')))`. On hot-path start, Haiku checks current surface hash vs stored; mismatch catches additions/renames/deletions.
Plugin rows: TTL-based per-row (`fetched_at + ttl_hours < now` → stale → cold-path refresh on next match).
Risk #5 (line 376): one source-file hash misses cmd→skill delegation drift → mitigation: validate BOTH files when `activation_style: skill-indirected`.

### 2.8 — Telemetry JSONL (lines 290-300) + Kill switch (302-308)

File: `.claude/cache/sc-recommend-events.jsonl` (GITIGNORED — high-churn). One line per invocation. EXACTLY 5 fields: `ts`, `mode`, `cache_result`, `classification_key`, `duration_ms`.
`cache_result` enum (line 300): `hit | miss_no_key | miss_low_confidence | miss_validation_stale | miss_budget_exceeded | cold_inserted`.

Kill switch (rolling 50-invocation hit rate after 2 weeks): ≥80% paying off / 60-80% keep measuring, don't expand / <60% DISABLE cache, keep instrumentation.

### 2.9 — `--eval` flag (lines 224-277) — dispatch-relevant summary

`/sc:recommend <goal> [--eval <mode>]`, default `none`. Modes: `quick` (opus only, 1 run, ~90K), `normal` (opus+sonnet, 2 each, ~360K), `deep` (opus+sonnet+haiku, 3 each, ~810K). Pipeline: spawn N parallel subagents per model → each produces the actual deliverable using the just-inserted row → grade vs assertions → aggregate per-model metrics → deterministic tier selection (quality/speed/cost/balanced, lines 250-255) → write `best_model` into row. Reuses iteration-1 `build_benchmark.py` + `grader.py` (line 261). Eval-run JSON tracked under `.claude/cache/eval-runs/iteration-<N>/row-<key>-results.json`.

---

## Section 3 — Closed-enum `classification_key` vocabulary

Spec mandate (Implementation Order #3, line 412): "Write the Haiku classifier prompt with closed-enum key vocabulary (~20 lines, ~10 keys, 3-5 few-shot examples per key from the eval set)." Risk #1 (line 368): "Classifier stability (highest risk)... Mitigation: closed-enum key vocabulary, deliberate human-reviewed expansion."

The spec gives only ONE concrete key in the schema example: `key: "spec-generation"` (line 51) → `candidate: "/sc:spec-panel"`. The rest must be DERIVED. This is a researcher-derived candidate set, NOT a spec-stated set — marked as a DESIGN PROPOSAL the builder/human must review.

### 3.1 — Evidence base: the 6 iteration-1 eval cases (verified from grading.json `eval_name` + `expectations`)

| Eval | eval_name | Request intent | Target recommendation | Cacheable? | Derived key |
|---|---|---|---|---|---|
| eval-1 | spec-from-matrices-must-surface-spec-panel | build a release spec from matrix inputs | `/sc:spec-panel` (delegation) | YES | `spec-generation` (spec-confirmed) |
| eval-2 | research-codebase-must-pick-among-three-research-paths | research how codebase works | deep-research agent / Explore / auggie / tech-research | YES | `codebase-research` |
| eval-3 | tasklist-must-handoff-not-reimplement | generate a tasklist | `/sc:tasklist` or task-builder | YES | `tasklist-generation` |
| eval-4 | small-util-refactor-must-recommend-native | refactor a 40-line util | native Read+Edit (NO delegation) | NO (native — skips table, `native_fallback: true`) | (native — no row) |
| eval-5 | plugin-mode-must-search-ecosystem-not-local | find an MCP server (`--plugin`) | external MCP server + install cmd | plugin-table only | `<plugin-name>` (plugin table) |
| eval-6 | parallel-research-must-recommend-multi-agent-fanout | research 3 things independently + synthesize | parallel Agent fan-out (single message) | YES | `parallel-agent-fanout` |

So the 6 evals yield 4 cacheable local keys (`spec-generation`, `codebase-research`, `tasklist-generation`, `parallel-agent-fanout`), 1 native (no key), 1 plugin (plugin-table key).

### 3.2 — Candidate closed key set (~10) — DESIGN PROPOSAL, derived from 4 eval keys + 42-command surface

Surface basis (verified `ls src/superclaude/commands/*.md`, 42 commands): adversarial, agent, analyze, auggie-review, brainstorm, build, business-panel, cleanup-audit, cleanup, cli-portify, design, document, estimate, explain, git, help, implement, improve, index, index-repo, load, pm, recommend, reflect, release-split, research, review-translation, roadmap, save, sc, select-tool, spawn, spec-panel, tasklist, task, tdd, test, troubleshoot, validate-roadmap, validate-tests, workflow.

Proposed ~10-key vocabulary (clustering high-traffic delegation intents to a discrete category each; few-shot examples drawn from eval set + command descriptions):

1. `spec-generation` → `/sc:spec-panel` / `/sc:tdd` / prd skill (eval-1 confirmed).
2. `codebase-research` → deep-research / tech-research / Explore / auggie (eval-2).
3. `tasklist-generation` → `/sc:tasklist` / task-builder (eval-3).
4. `parallel-agent-fanout` → multi Agent calls single message (eval-6).
5. `roadmap-generation` → `/sc:roadmap` / `/sc:validate-roadmap`.
6. `adversarial-review` → `/sc:adversarial` / `/sc:reflect` / `/sc:auggie-review`.
7. `cleanup-audit` → `/sc:cleanup-audit` / `/sc:cleanup`.
8. `troubleshoot-debug` → `/sc:troubleshoot`.
9. `web-research` → `/sc:research` / deep-research agent (external-facing, distinct from codebase-research).
10. `cli-portify` / `pipeline-orchestration` → `/sc:cli-portify` / `/sc:spawn` / `/sc:pm`.

Plus the implicit non-keys: native cases (`native_fallback: true`, no row — eval-4) and plugin keys live in the SEPARATE plugin table keyed by plugin name (eval-5).

CAVEAT (evidence-based): only `spec-generation` is spec-confirmed. Keys 2-4 are eval-derived (strong). Keys 5-10 are surface-derived PROPOSALS — the spec says "~10 keys" and "deliberate human-reviewed expansion" (line 368), so the exact set is a `needs_human_decision`-adjacent design choice. The closed-enum property (classifier may ONLY emit a key in this set, else `cache_miss: no_key` → cold path) is the load-bearing invariant; the precise membership is tunable and grows via human review, not classifier improvisation.

### 3.3 — Few-shot requirement

Spec: "3-5 few-shot examples per key from the eval set" (line 412). Only 4 keys have direct eval-set examples (evals 1,2,3,6). Keys 5-10 lack iteration-1 eval coverage → few-shot examples for them must be hand-authored (the builder should flag that the eval set currently covers only 4 of the ~10 keys; the others need synthetic few-shots or eval-set expansion before the classifier is reliable on them).

---

## Section 4 — CRITICAL: Python-vs-skill-prose boundary (EVIDENCE ONLY — do not decide)

This is the flagged open question feeding the `needs_human_decision` item. The user provided the boundary as an OPEN QUESTION and did NOT specify the resolution. Below is the evidence for each step's natural home. I present both sides; I do NOT decide.

### 4.1 — Per-step classification table (from hot/cold flow)

| Step | Operation | Natural home | Evidence |
|---|---|---|---|
| Spawn Haiku subagent | Agent tool, `model:haiku` | CLAUDE-ORCHESTRATED | Agent/Task spawning is a harness action; only Claude can invoke the Agent tool. Spec line 113 "Parent... Spawns ONE Haiku subagent (via Agent tool)". |
| Classify request → key | LLM judgment | CLAUDE (Haiku) | Inherently a model call (line 114). Not deterministic. |
| `native_likely` decision | LLM judgment | CLAUDE (Haiku) | Step 3, emitted in classifier output (line 115). |
| `confidence_top2_delta < 10%` check | numeric compare on classifier output | EITHER (see 4.3) | Spec line 116: "No extra LLM call for this check — the delta is already in step-2 output." A pure float compare — trivially Python OR trivially prose. |
| Table scan (`key == classification_key`) | dict/list lookup over inlined YAML | EITHER (see 4.3) | If table is INLINED into Haiku's prompt (line 113), Haiku does the scan in-context (prose). If parent holds the YAML, Python does it. Spec inlines the table → leans prose, BUT see tension 4.4. |
| Read `row.candidate` source + SHA256 + compare `source_hash` | file read + hashlib.sha256 + string compare | DETERMINISTIC PYTHON | Step 6, line 118. sha256 is canonical deterministic work; `convergence.py` precedent. (A Haiku-computed hash would be unverifiable/fabrication-prone — strong evidence for Python.) |
| Inject `best_model` hint into prompt | string substitution | CLAUDE (prose) | Step 7-8: composing the refined paste-ready prompt is the model's deliverable (lines 119-120). |
| Emit recommendation / surface output | text generation + surfacing verbatim | CLAUDE | Lines 120, 170 "Parent surfaces your output verbatim." |
| Budget gate (>10K tokens → cold) | token accounting compare | DETERMINISTIC PYTHON (likely) | Step 9, line 121 "cumulative hot-path tokens exceed 10K". Token counting is a harness/Python measurement, not a model judgment. |
| Telemetry JSONL append | open file, append 1 line | DETERMINISTIC PYTHON | Step 10, line 122; file write. Haiku cannot write files (line 133, 170). |
| YAML read (load table) | parse YAML | DETERMINISTIC PYTHON | Reader/writer ~80 LoC mirroring `convergence.py:DeviationRegistry` (line 411). |
| YAML write-back (commit cache_update) | atomic `tmp + os.replace()` | DETERMINISTIC PYTHON | Step 4 cold path, line 133 "Parent commits... atomic write per convergence.py:DeviationRegistry.save(). Haiku cannot write files; parent commits." UNAMBIGUOUS. |
| `surface_hash` compute/compare | Glob + sort + sha256 | DETERMINISTIC PYTHON | Line 286; sha256 of sorted Glob output. |
| Eval aggregation (pass_rate, mean_tokens, tier selection) | arithmetic + deterministic tie-break | DETERMINISTIC PYTHON | Lines 250-269; "picked deterministically"; reuses grader.py/build_benchmark.py. |
| Cold-path condensed pipeline (Glob→auggie→Read→net-value→prompt) | LLM-orchestrated tool sequence | CLAUDE (Haiku) | Line 131; this is the skill body running inside the subagent. |

### 4.2 — Evidence FOR a heavier Python orchestration layer (parent-as-Python)

- Spec explicitly mandates a Python reader/writer (~80 LoC mirroring `convergence.py:DeviationRegistry`, line 411) and a parent dispatch layer (~150 LoC, line 414).
- Atomic write, sha256, JSONL append, eval aggregation are CALLED OUT as parent/deterministic, and "Haiku cannot write files; parent commits" (lines 133, 170) is stated twice.
- Implementation Order (lines 408-432) enumerates discrete Python components: YAML reader/writer, hot/cold dispatch in parent, JSONL telemetry, `--eval` pipeline, plugin eval gate — all framed as LoC estimates, i.e., code.
- `convergence.py:DeviationRegistry.save()` is an existing Python precedent the spec says to mirror.
- Total estimate ~700 LoC (line 434) — clearly a substantial Python surface, not pure skill prose.

### 4.3 — Evidence FOR keeping classification/scan/delta in skill prose (thin Python)

- The TABLE is INLINED into the Haiku prompt (`<TABLE><inlined YAML></TABLE>`, lines 113, 156-158). If Haiku already has the table in-context, the scan + key-match + top2-delta check are zero-marginal-cost in-prompt operations — adding a Python layer for them duplicates work and adds a round-trip.
- Spec line 116 explicitly says the delta check needs "No extra LLM call... the delta is already in step-2 output" — i.e., it piggybacks on the classifier, suggesting it lives where the classifier lives (the Haiku subagent), not in a separate Python gate.
- `sc-recommend` is fundamentally a SKILL (prose-driven). The existing cold path (Section 1) is 100% skill prose with zero Python. Pushing scan logic into Python is a departure from the skill's nature.
- The classifier pattern reference is `sc-task-protocol/` (line 114) which is itself a SKILL (`src/superclaude/skills/sc-task-protocol/SKILL.md` — verified exists), i.e., a prose classifier, not a Python classifier. (researcher-02 covers this pattern's mechanics.)

### 4.4 — The genuine tension (the crux of the human decision)

The inlined-table design (prose scan) collides with the deterministic-validation design (Python sha256/write). Two coherent resolutions exist:

- **Resolution H (Haiku-heavy / thin parent):** Haiku does classify + scan + match + delta + native-decision + prompt-build all in one subagent call (table inlined). Parent Python is THIN: spawn, surface, sha256-validate the one candidate Read, append telemetry, commit YAML on cold-path. ~Lower LoC. Risk: hash validation must still be parent-side (Haiku can't be trusted to sha256), so step 6 splits awkwardly across the Haiku/parent boundary mid-flow.
- **Resolution P (Python-heavy / thin Haiku):** Parent Python loads YAML, does the scan/key-match/delta-gate/validation/budget in code; Haiku is ONLY called for (a) classification and (b) cold-path prompt construction. Cleaner determinism, easier to test, matches the ~700 LoC framing. Risk: the table is then NOT needed inlined in the hot-path classifier prompt (contradicts line 113's inlining), and you pay a parent↔Haiku round-trip to get the key before scanning.

EVIDENCE SUMMARY for the decision-maker:
- Pure-deterministic operations (sha256, atomic YAML write, JSONL append, surface_hash, eval aggregation) → UNAMBIGUOUSLY Python. No evidence supports prose here; "Haiku cannot write files" is stated twice.
- Pure-judgment operations (classify, native_likely, cold-path pipeline, prompt construction) → UNAMBIGUOUSLY Claude/Haiku.
- The CONTESTED middle: table scan, key-match, top2-delta gate, budget gate. Spec inlines the table (→ prose) yet frames dispatch as ~150 LoC parent code (→ Python). This is the unresolved seam. The `needs_human_decision` item should present Resolution H vs Resolution P with the line-113-inlining-vs-line-414-dispatch-LoC tension as the deciding axis.

DO NOT DECIDE — surfaced as evidence per task instructions.

---

## Section 5 — Cross-cutting flags for the builder

1. `allowed-tools` expansion required: current SKILL.md:4 lacks `Edit`/`Write`/`Agent`/`Task`. Hot path needs Agent (Haiku spawn) + the parent needs Write (YAML/JSONL). The skill frontmatter (or the parent command that hosts the Python) must gain these. (Section 1.1.)
2. The cold-path runbook (~50 lines) is a NEW artifact distinct from the current 227-line SKILL.md; the current SKILL.md is the DISTILLATION SOURCE, not the runbook itself. Load-bearing content to preserve listed in Section 1.8.
3. Eval-set coverage gap: only 4 of the proposed ~10 classification keys have iteration-1 eval examples for few-shots (Section 3.3). Flag for the builder.
4. Gitignore exception (lines 81-105) is user-authorized in-spec: `.claude/cache/` tracked EXCEPT `sc-recommend-events.jsonl`. This crosses the CLAUDE.md "never commit .claude/" absolute rule and is explicitly noted as user-authorized — the builder must NOT extend it further (line 105).
5. Return-contract parity: the hot path must emit the SAME return contract shape as the cold path / current SKILL.md (Section 1.7) so callers don't branch on path. The `<RETURN>` JSON (Section 2.4) is a superset (adds `native_likely`, `confidence_top2_delta`, `cache_miss`, `cache_update`, `best_model_hint`).

There is also a companion file `.dev/brainstorms/sc-recommend-lookup-cache/return-contract.yaml` (7.5KB, not read in full — flagged for the template/contract researcher-05) and `round-4-synthetic-eval-cases.md` (19.8KB — plugin synthetic-eval pipeline, owned by researcher-03 per scope).

---

## Summary

The COLD-PATH is the current 227-line `sc-recommend/SKILL.md` + 3 refs: a Phase-0 GATE (live Glob enumeration → ONE auggie semantic-rank → per-candidate source Read verification) feeding Phase 1 (native-first net-value), Phase 2 (hand-off-envelope prompt), Phase 3 (`--plugin` ecosystem search), governed by anti-fabrication rules R1-R4 (R3 = no protocol reimplementation is THE load-bearing rule). Condensing to ~50 lines must preserve: the Phase-0 gate, R1-R4, the native-first default, graceful degradation, and the return-contract field set; everything else (rationale prose, full auggie query, 5-axis rubric, --plugin source list, ASCII templates) moves to / stays in refs.

The lookup-cache adds a HOT path: parent spawns ONE `model:haiku` subagent with the inlined YAML cache; Haiku returns `{classification_key, native_likely, confidence_top2_delta}`; 5 miss reasons (`no_key`, `low_confidence`, `validation_stale`, `budget_exceeded`) fall through to the COLD path (the condensed runbook in a second Haiku subagent that also returns a `cache_update` the PARENT commits via atomic YAML write). Schema_version 2 rows add `best_model` + `eval_history` (R3); a separate plugin table adds `resource_kind`/`adoption_status`/install metadata with a 4-phase eval-gated lifecycle. Invalidation = per-row `source_hash` + top-level `surface_hash`. Telemetry = 5-field JSONL with a 6-value `cache_result` enum and a <60%-hit-rate kill switch.

The closed-enum key vocabulary is spec-confirmed for only `spec-generation`; the other ~9 keys are derived (4 eval-backed: `codebase-research`, `tasklist-generation`, `parallel-agent-fanout`; ~6 surface-proposed). The classifier may ONLY emit an in-set key (closed-enum invariant); membership grows by human review, not classifier improvisation.

The Python-vs-prose BOUNDARY (the `needs_human_decision` seam): deterministic ops (sha256, atomic YAML write, JSONL append, surface_hash, eval aggregation) are unambiguously Python ("Haiku cannot write files", stated twice); judgment ops (classify, native_likely, cold pipeline, prompt build) are unambiguously Haiku; the CONTESTED middle (table scan / key-match / top2-delta gate / budget gate) has the spec inlining the table into the Haiku prompt (→ prose) while framing dispatch as ~150 LoC parent code (→ Python). Resolution H (Haiku-heavy) vs Resolution P (Python-heavy) presented with evidence; NOT decided per task scope.
