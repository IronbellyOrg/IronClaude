---
name: sc-recommend
description: "Build a refined, paste-ready prompt that hands the user's request off to the right local skill, command, agent, or native-tool sequence — only when delegation adds net value. Use this skill whenever the user asks 'which command should I use', 'how do I best prompt for X', 'help me invoke the right skill for Y', 'recommend a workflow for Z', or describes a task without naming a command. Also use proactively whenever the user pastes a goal that could plausibly map onto multiple skills/agents/commands in this repo and you would otherwise have to choose blindly. With --plugin, switches to ecosystem search (Claude plugin marketplaces + community skill repos) instead of the local project surface."
allowed-tools: Read, Glob, Grep, Bash, mcp__auggie__codebase-retrieval, mcp__tavily__tavily-search, mcp__tavily__tavily-extract, WebFetch, WebSearch, Edit, Write, Agent, Task
argument-hint: "[goal description] [--plugin] [--minstar <N>]"
category: utility
---

# /sc:recommend — Refined-Prompt Builder

## Triggers

`sc-recommend` is invoked by the `/sc:recommend` command via its `## Activation` section. It is not invoked directly.

Activation conditions:

- User runs `/sc:recommend <goal>` in Claude Code
- `--plugin` flag may be passed to switch to ecosystem-search mode

## Purpose

Generate the **single best refined, paste-ready prompt** (occasionally a small set of clearly-distinguished prompts) that delegates the user's goal to whichever existing local skill / command / agent / native-tool sequence will execute it with the lowest waste and highest fidelity. Surface the project's *actual* current capability surface — not a stale mapping. Default to the smallest delegation that wins; recommend native tooling when delegation does not earn its overhead.

This skill **builds prompts**, it does not execute them. Output is a fenced prompt block the user can copy verbatim.

## Output

Every successful invocation emits one of:

1. **Refined-prompt block** — a fenced `text` block containing the paste-ready prompt to invoke a target skill/command/agent. Includes explicit parameters, deliverable shape, and file/agent handoffs. Single-line bash commands only (no heredocs, no `\` continuations); the prompt body itself may be multi-line because it is an argument string.
2. **Native-tooling recommendation** — when delegation adds no net value, a short paragraph naming the native tools (`Read`, `Grep`, `Glob`, `Edit`, `Write`, `Bash`) and the order to run them in. No skill is invoked.
3. **Plugin-search result** (`--plugin` only) — one or more plugin/skill candidates with capability summary, install command, repo URL, and citations.

If multiple distinct paths are reasonable (e.g., "either /sc:tasklist or task-builder fits"), emit each as its own clearly-labeled prompt block with a one-line disambiguator — never as a flat "alternatives" list.

The skill never restates the target's internal logic (see Rule R3).

## Hot-Path Cache Lookup (try the amortized cache before the cold path)

Before running the full Phase 0–3 **cold path** below, attempt the **hot path** — the lazily-populated YAML lookup cache that drops a repeat delegation request from ~91K to ~5–10K tokens. The cold path (Phase 0–3) only runs on a cache miss.

Under the resolved **Option P** layering, the `cli/recommend/` Python module owns the deterministic dispatch (scan / source_hash validation / budget gate); this skill owns only the Agent spawns (the `anthropic` SDK is banned, so the CLI cannot spawn Agents).

1. **Classify (ONE Haiku subagent).** Spawn exactly **one** `model: haiku` subagent via the Agent tool, using the classifier prompt at `src/superclaude/cli/recommend/prompts.py::CLASSIFIER_PROMPT`. Pass the verbatim user request. It returns `{classification_key, native_likely, confidence_top2_delta}` — nothing else. Do not classify in the parent.

2. **Deterministic dispatch (shell to the CLI).** The CLI owns the scan/validate/budget under Option P:

   `uv run superclaude recommend dispatch --key <classification_key> --delta <confidence_top2_delta> [--native-likely] [--budget-used <cumulative_hot_tokens>]`

   It prints a JSON `DispatchResult`. The source_hash validation is the CLI's deterministic Read + sha256 compare — **never** trust a Haiku-computed hash.

3. **Interpret the outcome (the 5 fall-throughs):**
   - `outcome: "hit"` → emit `recommendation` **verbatim** (it is the row's filled `prompt_envelope_template` plus any `best_model_hint`). Then append exactly one telemetry event: `uv run superclaude recommend telemetry append --mode delegate --cache-result hit --classification-key <key> --duration-ms <ms>`. **DONE — do not run the cold path.**
   - `outcome: "native"` (classifier `native_likely`, or a `native_fallback` row) → recommend native tooling per Phase 1; **no cold path, no table write, and no telemetry event** (native is not a cache-table event — it has no `cache_result` enum member, so the appender has nothing valid to log).
   - `outcome: "miss"` with `cache_result` ∈ {`miss_no_key`, `miss_low_confidence`, `miss_validation_stale`, `miss_budget_exceeded`} → **fall through to the cold path** (Phase 0–3). Carry the miss reason into the cold-path write-back.

The skill spawns exactly **one** Haiku subagent here (the classifier); the cold-path Haiku subagent is spawned only on a miss (see the Cold-Path Write-Back section after Phase 3). The emitted hot-hit recommendation reuses the row's hand-off envelope unchanged — it restates no target protocol (R3). The hot and cold paths emit the **same Return Contract** shape for caller parity.

## Phase 0 — Mandatory Surface Enumeration + Auggie Sweep (GATE)

**Hard gate. Do not advance to Phase 1 until BOTH steps have landed or the documented degradation notice has been emitted.**

The old skill failed because its discovery layer was a hand-curated 10-row keyword table that went stale (it failed to surface `/sc:spec-panel` even though that command file was sitting in `src/superclaude/commands/`). The fix is to enumerate the actual surface every invocation and let auggie semantically rank it. There is no static mapping in this skill.

### Step A — Live surface enumeration (Glob)

Enumerate the project's *actual* current surface. Read every result lazily — Glob first, Read only what the candidate set later requires.

- `src/superclaude/commands/*.md` → live command index
- `src/superclaude/skills/*/SKILL.md` → live skill index
- `src/superclaude/agents/*.md` and `.claude/agents/*.md` → live agent index
- `src/superclaude/templates/**/*.md` and `examples/*-template.md` → templates

Commands are thin dispatchers that delegate to skills via `## Activation`. Treat `src/superclaude/commands/*.md` as the fast-path discovery surface for `/sc:*` slash commands.

If the user's cwd is a worktree under `.claude/worktrees/<name>/`, all paths above resolve relative to **that worktree**, not `/config/workspace/IronClaude/`. The skill must remain worktree-aware.

See `refs/surface-enumeration.md` for the full algorithm, the verification record schema, and worked examples.

### Step B — MANDATORY auggie semantic ranking

After enumeration, issue **one** `mcp__auggie__codebase-retrieval` query to semantically rank the enumerated surface against the user's request. Auggie is the speed lever: one semantic query ranks the whole surface; do not iterate file-by-file.

Query shape:

> Given the user request "<verbatim user request>", and the enumerated surface (commands: <names>; skills: <names>; agents: <names>; templates: <names>), rank the top 3-5 candidates by capability fit. For each, summarize: what it does, when it wins over native Read/Edit/Glob/Grep/Bash, what flags or required inputs it expects, and any known caveats or recent behavioral changes.

### Step C — Per-candidate verification (the prerequisite gate)

For each candidate auggie returns, **before** it is allowed into the recommendation:

1. **Direct read** — Read the candidate's source file (`src/superclaude/commands/<name>.md`, or `src/superclaude/skills/<name>/SKILL.md`, or `src/superclaude/agents/<name>.md`). Extract: flag table, required-input rules, activation handoff, return contract.
2. **Auggie record** — record the usage notes, related skills, and caveats auggie surfaced in Step B for this candidate.

A candidate that fails Step 1 (source file does not resolve) is a ghost. Drop it silently. Do not warn the user about candidates that did not survive verification; the user does not need that noise.

Verification is **exempt** for built-in tools (`Read`, `Grep`, `Glob`, `Edit`, `Write`, `Bash`, `TodoWrite`, `WebFetch`, `WebSearch`) and for MCP server names referenced abstractly. Those have stable interfaces and verifying them adds overhead with no fabrication-risk return.

### Graceful degradation

| Failure | Response |
|---|---|
| Auggie MCP unavailable | Proceed with Glob+Read only. Emit a one-line header notice on the output: `Auggie unavailable — ranking falls back to literal Glob+Read; usage nuance may be thin.` Do not silently skip the gate. |
| Auggie returns empty | Note the gap in the output (`no auggie matches; ranking from file content only`) and proceed. The candidate may be new or rarely exercised — flag it rather than fake confidence. |
| Candidate source missing | Drop the candidate. Do not surface it. |
| User request is too vague to enumerate against | Ask one clarifying question. Do not emit a recommendation built on a guess. |

## Phase 1 — Net-Value Evaluation (anti-bloat default)

For **every** surviving candidate, answer explicitly before recommending:

1. Does invoking `<skill/agent/command>` add value beyond a 2-3 step Read/Grep/Glob/Edit/Write sequence?
2. Is the overhead (token cost of the skill body, subagent spawn time, protocol complexity, hook gates) justified by specialized capability the model lacks natively in this context?
3. Would a senior engineer reading the user's request choose this delegation, or roll the equivalent themselves in less time?

If the honest answer to any of these is "no" or "barely", **default to native tooling**. The skill is allowed — and expected — to emit:

> No skill/agent delegation adds net value here. Use Read on `<file>`, then Edit. Reason: <one-line why>.

as a complete, valid recommendation. Anti-bloat is **core**, not optional. A recommendation engine that recommends delegation reflexively trains users to over-invoke and burns tokens for no gain.

When delegation **does** win, the recommended prompt must invoke the smallest delegation that earns its cost. Prefer `/sc:<x>` → skill → agent over `/sc:<x>` → skill → agent → sub-skill chains unless the longer chain is the documented best path.

See `refs/delegation-vs-native-heuristics.md` for the full rubric (when commands beat skills, when skills beat agents, when parallel `Agent` calls beat sequential skills, when native is strictly best).

## Phase 2 — Refined Prompt Construction

Build the prompt as a **hand-off envelope**, not a specification. The prompt carries:

- the target invocation (`/sc:<command>` or `Skill <skill-name>` or `Agent <agent-name>` or native tool sequence)
- the user's verified parameters / file paths / flags
- the expected deliverable shape (what the user wants back)
- worktree-aware paths (relative to cwd if cwd is `.claude/worktrees/<name>/`)

The prompt MUST NOT restate the target's protocol logic — phase breakdown, scoring rules, agent roster, debate format, return contract internals. That belongs to the target skill. Trust the hand-off.

### Output template

````text
Goal: <one-line restatement of the user's intent>

Recommended delegation: <target name + why this wins net-value>

Paste-ready prompt:

```text
<the actual prompt — a hand-off envelope, not a specification>
```

Sources verified:

- <path/to/command.md> (Read)
- auggie semantic rank: <one-line summary>
````

If the recommendation is "use native tooling", drop the prompt block and emit the native-tool sequence as a numbered list instead.

## Phase 3 — `--plugin` Mode (ecosystem search)

When `--plugin` is set, **ignore the entire local surface enumeration** and search the plugin / community-skill ecosystem instead. Local skills and plugins must not bleed into each other's outputs.

In-scope sources (this configuration):

- Claude Code plugin marketplaces (`claude-plugins-official`, anthropic-managed listings)
- Community skill repos (`anthropic/skills`, `sammcj/agentic-tools`, etc.)

Out-of-scope (this configuration): raw MCP server marketplaces. Do not surface MCP servers under `--plugin` unless the user explicitly asks for one in their request.

Search via (in priority order): `tech-research` skill, the `deep-research` agent, or Tavily MCP directly. WebFetch / WebSearch are last-resort fallbacks.

For every candidate, return:

- plugin / skill name
- one-sentence capability summary
- install command (single-line bash)
- repo URL
- GitHub star count + source URL (or `unranked: <curated|non-github|nested>` for bonus candidates)
- integration notes (what the user needs to wire up themselves)
- version / compatibility caveats
- citation (the URL the claim came from)

See `refs/plugin-ecosystem-sources.md` for the full source list, query patterns, and result-format template.

### Minimum-star floor + two-tier output (`--minstar`)

`--minstar <N>` sets the minimum GitHub-star floor for `--plugin` candidates. Resolve the floor as `N = --minstar value if passed else 500` — the **500 floor applies even when the flag is omitted** (default-on). `--minstar 0` disables the floor. A negative or non-integer value is a STOP: `"--minstar requires a non-negative integer (e.g. --minstar 500). Use --minstar 0 to disable the floor."`

**Local-mode guard (warn-and-ignore)**: `--minstar` only has meaning in `--plugin` mode. If `--minstar` is passed WITHOUT `--plugin`, emit exactly one notice — `"--minstar has no effect without --plugin (the local surface has no stars); ignoring it."` — then run the normal local recommendation (Phase 0-2). Never a STOP.

**Delegated star capture**: because the ecosystem search is delegated (not run inline), the generated search prompt MUST instruct the delegate to capture each candidate's GitHub star count and its source URL. The skill then enforces the floor and the two-tier split on the returned set. A star count is a claim — Rule R1/citation discipline forbids inventing one; an undiscoverable count routes the candidate to the bonus section, never to a guessed number.

**Two-tier output**:

- **Primary** — candidates with a discoverable own-repo star count `>= N`, sorted by stars **descending**. Each shows a `Stars` field with its source URL. Keep the top-3 disambiguator discipline.
- **Bonus — not ranked by GitHub stars** — credible candidates with no own-repo star count, **never filtered by the floor**, each labeled with the reason: `curated` (Anthropic-curated marketplace entry), `non-github` (source is not a GitHub repo), or `nested` (skill/plugin lives inside a larger repo whose stars are not attributable to it). Same top-3 discipline.

If the floor removes every GitHub candidate but bonus candidates exist, surface the bonus section with a one-line note: `"No candidate met the >= N star floor; showing unranked credible matches below. Lower the floor with --minstar <smaller>."` If nothing credible survives at all, reuse the existing "found nothing credible" guidance.

### `--plugin --eval` adoption lifecycle (4 phases)

When `--plugin` is combined with `--eval <mode>` (mode ≠ `none`), the skill runs the plugin adoption gate. The CLI owns the deterministic half (precondition HARD-BLOCK, adoption verdict, plugin-row patch); the skill owns the Agent-spawned eval panels. The four phases (spec `merged-requirements.md:211-220`):

1. **Discovery** — `--plugin <query>` with no eval mode surfaces the candidate plugin/MCP resource + metadata (install command, `setup_steps`, repo URL, citations). No row is committed (browse mode).
2. **Adoption proposal** — `--plugin <query> --eval <mode>` runs the eval pipeline twice per panel cell: with the resource INSTALLED vs UNINSTALLED, on synthetic cases generated from the plugin's stated capabilities (the cold-path `--eval` fan-out below produces the per-(model,run) deliverables for each configuration). Install steps that need OAuth / API keys / env vars are EMITTED for the user to run — the skill never auto-completes auth flows; the user confirms readiness before the with-resource runs.
3. **Decision gate** — after the panels finalize, the parent shells the CLI:

   `uv run superclaude recommend eval plugin --key <plugin-key> --preconditions-file <path> --with-resource-file <agg.json> --without-resource-file <agg.json>`

   `run_preconditions` runs FIRST and **HARD-BLOCKS** on any `failure_mode: hard` precondition (e.g. the MCP server is not installed) — the CLI exits non-zero, no degraded fallback. On pass, `evaluate_adoption` applies the threshold (`pass_rate +≥0.10` **OR** `token −≤−0.20`, with `pass_rate` must-not-regress) and `patch_plugin_row` writes `adoption_status` (`evaluated_positive` / `evaluated_negative`) + an `eval_history` entry to `.claude/cache/sc-recommend-plugin.yaml` via the atomic writer.
4. **Hot-path use** — a later `--plugin <query>` matching the row reads its `adoption_status`: `evaluated_positive` rows emit the install command (if not locally installed) + best-model hint; `evaluated_negative` rows are kept (30-day TTL) but never surfaced as a hot-path recommendation.

## Cold-Path Write-Back (populate the cache on a miss)

The cold path **is** Phase 0–3 above — run when the Hot-Path Cache Lookup returned `outcome: "miss"` (any of the four miss reasons: `miss_no_key`, `miss_low_confidence`, `miss_validation_stale`, `miss_budget_exceeded`). A `native` outcome does **not** reach the cold path. Phase 0–3 run inside a **second** `model: haiku` subagent so the expensive enumerate→auggie→verify work happens in an isolated context, not the parent.

1. **Spawn the cold-path Haiku subagent.** Use the Agent tool, `model: haiku`, handing it the condensed runbook at `src/superclaude/cli/recommend/prompts.py::COLD_PATH_RUNBOOK` as its system context — **not** the full SKILL.md body (inlining the full skill would recreate the exact ~91K cost the cache exists to remove). The subagent runs Phase 0–3 (Glob → auggie → Read-verify → net-value → prompt) and returns the recommendation **plus** a structured `cache_update` payload (the row to commit: `key`, `candidate`, `flags`, `prompt_envelope_template`, `rationale`, `source_path`, `native_fallback`).

2. **Parent commits the cache_update.** Haiku **cannot write files**, so the parent (this skill, the Claude session) commits the row by shelling to the CLI atomic writer:

   `uv run superclaude recommend cache put --row-json '<the cache_update row as a single-line JSON object>'`

   This routes through `LookupCache.save()` (atomic tmp + `os.replace`). The CLI recomputes the current `surface_hash` and the full per-row `source_hash` on write — the parent never trusts a Haiku-computed hash.

3. **Optional `--eval` trigger (Agent fan-out + finalize).** If the invocation carried `--eval <mode>` (mode ≠ `none`), evaluate the just-inserted row's `best_model`. Opt-in only. Under Option P the CLI cannot spawn Agents (anthropic SDK banned), so the **skill (parent session) emits the fan-out** and the CLI does the deterministic finalize:

   a. **Resolve the panel** for `<mode>` from `MODE_MATRIX`: `quick` = `opus`×1 (**1** Agent call); `normal` = `opus`+`sonnet`×2 (**4** Agent calls); `deep` = `opus`+`sonnet`+`haiku`×3 (**9** Agent calls). `none` = no-op.

   b. **Fan out** — emit one parallel Agent-tool call per `(model, run)` cell, each with the corresponding `model:` (e.g. `deep` → opus run-1/2/3 + sonnet run-1/2/3 + haiku run-1/2/3). Each Agent produces the real deliverable for the row and writes **both** files at the EXACT path the finalizer reads:

      - `.claude/cache/eval-runs/iteration-<N>/<key>/<model>/run-<i>/outputs/recommendation.md`
      - `.claude/cache/eval-runs/iteration-<N>/<key>/<model>/run-<i>/timing.json`

      (the `<i>` is the 1-based run number; tokens are NOT auto-captured, so each Agent MUST emit `timing.json` itself.)

   c. **Finalize (CLI, deterministic).** After all Agent calls complete, the parent shells: `uv run superclaude recommend eval run --key <key> --mode <mode> --iteration <N>`. This grades each deliverable, aggregates per model, selects `best_model` by tier, writes `row-<key>-results.json`, and patches the lookup row's `best_model` + `eval_history` via the atomic writer. The finalizer assumes the deliverables already exist on disk — the fan-out in (b) must have produced them at the exact layout above, or grading sees empty text.

4. **Emit + telemetry.** Surface the recommendation verbatim, then append exactly one telemetry event with `--cache-result cold_inserted` (or the original miss reason if no row was inserted): `uv run superclaude recommend telemetry append --mode delegate --cache-result cold_inserted --classification-key <key> --duration-ms <ms>`.

The cold path emits the **same Return Contract** shape as the hot path (caller parity). No protocol of any recommended target is restated in the `cache_update` (R3) — the `prompt_envelope_template` is a hand-off envelope.

## Output Constraints — Anti-Fabrication Rules

These rules are non-negotiable. They survived from the old skill because they were the only parts that held up under scrutiny.

### Rule R1 — No unverified flags

A flag may appear in the recommended prompt **only if** it is present in the verified target's flag table (or `argument-hint`). Example: `/sc:adversarial` has a fixed flag set in `src/superclaude/commands/adversarial.md`; no flag may be attached to it that is not in that file. Fabricated flags (`--rounds`, `--measure-first`, `--verdict-per-claim`, etc., when they do not exist) are forbidden.

### Rule R2 — No unverified commands or skills

A command or skill may appear **only if** its source file was resolved in Phase 0 Step C. Auggie-mentioned but not file-resolved → drop. Memory-recalled but not file-resolved → drop.

### Rule R3 — No protocol reimplementation (the load-bearing rule)

When a verified target has `activation_style: skill-indirected` (its command file delegates to a protocol skill via `## Activation > Skill <name>`), the generated prompt MUST be a **hand-off**, not a **specification**.

- **Allowed**: `Run: /sc:adversarial --compare fileA.md,fileB.md --focus structure --depth standard`
- **Forbidden**: any inline content that restates the target's protocol — debate rules, phase counts, scoring formulas, "steelman strategy", artifact lists. The protocol skill owns that behavior; the prompt invokes and trusts.

R3 enforces: **invoke, don't reimplement**. Duplicating a target's protocol inline causes drift, wastes tokens, and produces prompts that disagree with the actual command when the command is run.

### Rule R4 — Built-ins exempt

`Read`, `Grep`, `Glob`, `Edit`, `Write`, `Bash`, `TodoWrite`, `WebFetch`, `WebSearch` are harness primitives. Recommend them by name without verification.

## Return Contract

| Field | Type | Description |
|---|---|---|
| `status` | string | `success`, `clarification_needed`, `degraded`, `plugin_search` |
| `mode` | string | `local` (default) or `plugin` |
| `recommendation_kind` | string | `delegation_prompt`, `native_tooling`, `multi_path`, `plugin_candidate` |
| `prompt_block` | string | The paste-ready prompt (empty for `native_tooling`) |
| `verified_sources` | list | Paths Read during Phase 0 Step C |
| `auggie_status` | string | `ok`, `unavailable`, `empty` |
| `degradation_notes` | string | One-line note when degraded |

## Boundaries

**Will:**

- Enumerate the live project surface (commands, skills, agents, templates) on every invocation
- Use auggie to semantically rank candidates against the user's request
- Verify every candidate against its source file before emitting
- Emit refined paste-ready prompts that hand off to existing skills/commands/agents
- Recommend native tooling when delegation does not add net value
- Switch to ecosystem search when `--plugin` is set
- Apply the `--minstar` floor (default 500) + star-descending sort in `--plugin` mode, with a separate bonus section for credible candidates that have no own-repo star count; warn-and-ignore `--minstar` in local mode
- Cite every source it read

**Will Not:**

- Use a static keyword → category mapping table (root cause of the old skill's discovery failure)
- Invent flags or commands not present in source files (R1, R2)
- Restate a target's protocol logic inline in the prompt (R3)
- Mix local-surface candidates with `--plugin` ecosystem results
- Execute the recommended prompt (the user pastes it manually)
- Estimate time, budget, or token cost (out of scope for prompt generation)
- Detect user language (English-only — Turkish detection from old skill is dropped)
- Detect project framework from file system heuristics (this skill ships in the SuperClaude repo; the relevant context is the source tree, not which JS framework is present)

## Related References

- `refs/surface-enumeration.md` — Phase 0 glob set, auggie sweep algorithm, verification record schema
- `refs/delegation-vs-native-heuristics.md` — the net-value rubric (Phase 1)
- `refs/plugin-ecosystem-sources.md` — `--plugin` search targets and result template
