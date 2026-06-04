---
topic: "Cache/lookup-table layer for sc:recommend: hot-path classify→table-scan→validate→emit, cold-path research→insert/update. Separate tables for local skills/commands/agents vs plugins/MCP servers. Hard requirement: all work runs on Haiku, never main model. Evals must compare Haiku vs Opus."
domain: architecture
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-06-02T13:50:00Z
---

# Seed Brief: sc-recommend lookup-table cache

## Problem Statement

The current `sc-recommend` skill (just rewritten — see `src/superclaude/skills/sc-recommend/SKILL.md`) executes its full enumeration → auggie sweep → per-candidate Read → net-value evaluation pipeline on **every** invocation. Iteration 1 evals show this costs ~91K tokens and ~72s per call versus a ~64K / 38s baseline, for only a 6% headline pass-rate lift. The work is dominated by re-deriving facts that almost never change between invocations: which commands exist, what their flag tables look like, which skill each command activates, and how each skill is typically used.

A lookup-table layer should:

1. **Hot path** (target: > 80% of invocations): classify the user request, do a cheap table scan to identify the best skill/command/agent + the right flags + the right hand-off envelope, validate the table row against the current source file (single Read), and emit the refined prompt.
2. **Cold path** (target: < 20%): when the table cannot answer (low classification confidence, new surface element, or stale row), fall through to the existing full pipeline (enumerate + auggie + per-candidate verify + net-value), then **insert / update the lookup row** so the next caller hits the hot path.
3. **Separate tables**:
   - `local-surface.yaml` (or similar) — skills, commands, agents, templates from the local project surface.
   - `plugin-ecosystem.yaml` — plugin / MCP server metadata cached from external sources (only consulted on `--plugin` invocations).
   - The two tables NEVER mix; the local hot path never ingests the plugin table and vice versa.
4. **All inference runs on Haiku**. The main / parent model never does sc-recommend work directly. Classification, table lookup, validation, and prompt emission all delegate to a Haiku subagent (or to a Haiku-routed inline call where supported).
5. **Eval methodology compares Haiku vs Opus** on the same eval set used in iteration 1 (the 6 test cases under `.dev/eval-workspaces/sc-recommend/iteration-1/`), so we know empirically whether Haiku-only loses accuracy.

## Known Context

- The skill being optimized: `src/superclaude/skills/sc-recommend/SKILL.md` (225 lines, just committed at `c5e227dd`).
- Existing eval set: 6 test cases under `.dev/eval-workspaces/sc-recommend/iteration-1/evals.json` with drafted assertions and one full iteration of with-skill vs baseline runs.
- Iteration 1 results: with-skill 86% / baseline 81% pass; with-skill 91.5K tok / 72.3s; baseline 63.8K tok / 37.9s. The skill currently costs ~28K extra tokens and ~34 extra seconds per invocation.
- Available persistence patterns in the project: `.roadmap-state.json`, `manifest.json`, `execution-log.jsonl`, `serena memory`, `auggie-projects.txt`. No existing project-wide lookup-table convention for skill metadata, so this is greenfield.
- Auggie MCP is the current Phase-0 ranker; it already does semantic ranking across the surface. The lookup table's role is to remove the need to re-ask auggie when the answer is stable.
- The local surface size is bounded and visible: 41 commands, 24 skills, 38 agents, 15 templates (as of 2026-06-02). It changes only on `make sync-dev`. This is the lever that makes a cache viable — invalidation can be tied to source-file mtime or git rev.

## Constraints

- **Haiku-only execution.** No part of the recommend hot path or cold path may run on the parent / main model. All real work happens in a Haiku subagent. The parent's role is to spawn the Haiku worker and surface its output.
- **No table-driven hallucination.** A table row is a *cache*, not a *source of truth*. The hot path MUST validate the table's claim about a command/skill against the actual source file (one Read) before emitting. If the row disagrees with the source, fall to the cold path and update the row.
- **Separate tables.** Local-surface and plugin-ecosystem tables are physically and logically separate. The default-mode hot path never reads the plugin table; `--plugin` mode never reads the local table.
- **No new static keyword mapping.** The lookup table is keyed on classification output, NOT on a hand-curated keyword → skill mapping. The classifier produces the lookup key dynamically each call. (The Phase-0-failure mode of the previous skill must NOT return through the cache layer.)
- **Source-of-truth discipline preserved.** Tables live under `.dev/` or a similar non-distributable path. The skill source remains `src/superclaude/skills/sc-recommend/`. `make sync-dev` and the `.claude/` gitignore rules still apply.
- **No regression on the 6 existing evals.** The new design's pass rate must match or beat the current 86%, ideally while reducing tokens.
- **Eval comparison is non-optional.** Haiku-vs-Opus eval comparison on the same 6 test cases must run as part of validation. The brainstorm output must specify how that comparison is structured.

## Success Criteria

- **Hot path is genuinely cheap.** Target: < 10K tokens and < 15s per hot-path invocation. (vs current 91K / 72s).
- **Hot-path hit rate is high.** Target: ≥ 80% of invocations after warmup. (Below ~60% the cache layer is not earning its complexity.)
- **Quality matches or beats current skill.** Pass rate on the 6 evals ≥ 86% with the new design; ideally clearer wins on evals 4 and 6 where the qualitative gain was largest.
- **Haiku-only is verified empirically.** Haiku-vs-Opus eval comparison surfaces whether Haiku regresses on any of the 6 cases. If Haiku is within ~5% pass-rate of Opus, the constraint is validated.
- **Cold-path self-updates the table.** A new skill added to the local surface, or a renamed flag, is reflected in the table after exactly one cold-path invocation without manual intervention.
- **Separate tables stay separate.** `--plugin` invocations never read the local table; default-mode invocations never read the plugin table. This is verified by table-file-access telemetry.

## Open Questions

1. **Table schema.** Per-skill row vs per-classification-key row? YAML, JSON, JSONL, SQLite? What fields are load-bearing (flags, activation handoff, related skills, usage examples) vs nice-to-have (eval-history pointers, last-validated-at)?
2. **Classification keying.** How does the parent's request get translated into a stable lookup key? A free-text classifier output (`spec-generation`, `tasklist-build`, `small-refactor`, etc.)? An embedding hash? A discrete category enum? This is the single biggest design question — the choice cascades into invalidation logic, hit rate, and Haiku's success on classification.
3. **Validation step.** What does "validate the row against the source file" mean concretely? Read the command file's flag-table-line range and string-compare with the table's `flags` field? mtime check? git rev check? Each has different staleness windows and cost profiles.
4. **Cold-path table mutation.** Does the Haiku cold-path writer write the row, or does it produce a structured suggestion that the parent commits? Concurrency: do we need a lock if two `/sc:recommend` invocations cold-path simultaneously?
5. **Plugin-table refresh strategy.** Plugins / MCP servers evolve outside the repo. TTL-based refresh? On-demand refresh per `--plugin` call? Manifest-version-pinning?
6. **Bootstrapping.** Is the local-surface table populated lazily (only as requests come in) or eagerly seeded by a one-time bulk auggie sweep at commit time? Both have trade-offs (lazy is simpler; eager makes the first 20 invocations fast).
7. **Haiku failure modes.** What happens if Haiku misclassifies, mis-validates, or produces malformed output? Does the parent fall back to Opus inline? Does it fail the invocation and ask the user to retry? Per-eval Haiku-vs-Opus comparison should make this concrete.
8. **Eval design for Haiku-vs-Opus.** Same 6 cases × 2 model configs = 12 runs (or 24 with baseline). What does "Haiku wins" mean — equal pass rate, or pass rate within a tolerance plus a token-cost ratio? Brainstorm must specify the success bar.

## Enrichment Context — Codebase (auggie primary, quality_tier: primary)

### Existing persistence patterns directly reusable for a lookup table

- **`.roadmap-state.json`** (`src/superclaude/cli/roadmap/convergence.py`) is the closest existing precedent. Schema: `schema_version`, `spec_hash` (SHA256 invalidation key), `agents: [{model, persona}]`, per-step status with `started_at`/`completed_at` timestamps. Atomic write convention: `tmp + os.replace()`. **This is the right structural blueprint for the lookup table.**
- **Serena memory writes** (per `sc-roadmap` SKILL.md) use a `sc-<skill>:<artifact-name>:<timestamp>` key pattern for progressive state accumulation across waves. Could be the in-session cache; less suitable for the persistent table.
- **Roadmap markdown frontmatter** (`sc-roadmap-protocol/refs/templates.md`) already encodes per-roadmap metadata: `schema_version`, `generated`, `generator`, `complexity_score`, `complexity_class`, `primary_persona`, `consulting_personas`, `milestone_index[]`. The "explicit schema_version on every artifact" convention is well-established.

### Existing skill metadata already in frontmatter (free for the table to mirror)

Every command and skill already declares structured frontmatter:
- Required: `name`, `description`, `allowed-tools`.
- Common: `category`, `complexity`, `mcp-servers`, `personas`, `argument-hint`.
- Advanced: per-flag tables in the command body's Options section.

**The lookup table does not need to derive metadata — it can parse it from the source file once and cache the parse.** Validation reduces to "did the source file's frontmatter change since last parse?", which is cheap.

### Invalidation precedents

- `spec_hash` (SHA256 of source content) in roadmap state — the canonical invalidation signal in this codebase. When content changes, hash changes, re-derive. Same primitive should drive the lookup table.
- `freshness-pre-edit.sh` hook enforces re-Read before Edit on stale-mtime files — there is a project-wide culture of "verify before trust" for cached facts.
- `auggie-flag-clear.sh` hook clears an in-memory flag after every auggie call — precedent for "consume-and-clear" cache patterns.

### Haiku / model-routing precedents

- **No general "route the whole skill to Haiku" precedent exists.** The closest is the adversarial agent-spec format which assigns `model: haiku` per-agent in the `agents` array (e.g., test fixtures show `agents: [{model: opus, persona: architect}, {model: haiku, persona: architect}]`).
- The brainstorm protocol's own model rotation (opus/sonnet/haiku) is the most relevant template.
- The Task/Agent subagent system supports model overrides — Haiku routing for sc-recommend would invoke an Agent subagent with `model: haiku` rather than running inline.

### Classification precedents (free-text → discrete-category, established here)

- **`/sc:task` compliance-tier classifier** (STRICT / STANDARD / LIGHT / EXEMPT) — keyword weight × tier + context boosters (file count, security path detection, doc-only) + confidence threshold (< 0.7 → ask user). The most directly analogous classifier to what sc-recommend's hot path would need.
- **`/sc:brainstorm` domain classifier** (code / architecture / product / process / incident / research) — LLM-driven, taxonomy in a ref file, cached as state field.
- **`/sc:roadmap` complexity classifier** (LOW / MEDIUM / HIGH from a 0.0-1.0 score) — heuristic + LLM hybrid.

All three are LLM-driven, not regex. "Free-text request → discrete-category enum" is a solved pattern in this codebase and Haiku can plausibly handle it.

### Implications for the brainstorm

1. The lookup table can copy `.roadmap-state.json`'s schema almost verbatim.
2. Invalidation should use `spec_hash` (SHA256 of source file content) per established convention.
3. Haiku routing is achievable via Agent-with-model-override; no new infrastructure required.
4. The classifier step should follow the sc:task compliance-tier pattern rather than reinventing.
5. Atomic write via `tmp + os.replace()` is the established convention.
