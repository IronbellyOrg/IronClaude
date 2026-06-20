---
spec_id: SC-BRAINSTORM-V2-SPEC
version: 2.0.0
status: draft
created: 2026-05-25
target_release: v4.3.0
spec_type: behavioral-protocol
component_type: command + skill (sc-brainstorm-protocol)
parent_command: /sc:brainstorm
supersedes: src/superclaude/commands/brainstorm.md (monolithic, no skill)
complexity_score: 0.78
complexity_class: high
target_audience: SuperClaude framework developers, brainstorm users
---

# /sc:brainstorm v2 — Orchestrated Multi-Agent Brainstorm

## 1. Purpose & Identity

`/sc:brainstorm` v2 is a **smart orchestrator** that transforms an ambiguous topic into a unified requirements specification by:

1. Running a depth-tiered Socratic dialogue with the user to crystallize a **seed brief**
2. Auto-detecting and invoking **context enrichment** (codebase analysis, framework research) when valuable
3. Composing an **agent specification** that spans the available models × multiple domain personas
4. **Delegating** parallel proposal generation, structured debate, and merge to `/sc:adversarial` (Mode B or Pipeline Mode)
5. Optionally **handing off** the merged requirements to `/sc:design`, `/sc:tasklist`, or `/sc:task-builder` via a flag-gated extension

**v2 explicitly does NOT** re-implement debate, scoring, or merge logic. Those belong to `sc-adversarial-protocol`. v2's value is in the orchestration: dialogue, enrichment routing, agent-spec composition, and handoff.

### Key Differentiators vs v1

| Concern | v1 (current) | v2 (this spec) |
|---------|--------------|----------------|
| Architecture | Monolithic command file, no backing skill | Thin command + `sc-brainstorm-protocol` skill + 3 refs |
| Proposal generation | Single-agent multi-persona "coordination" (sequential, in-context) | N parallel proposals via `/sc:adversarial` (true sub-agent spawning) |
| Model diversity | Single-model (whatever powers the session) | 3 active aliases (HAIKU/SONNET/OPUS) rotated across N proposals |
| Persona diversity | 7-persona list in frontmatter (auto-activation soup) | Explicit per-proposal persona selection based on topic-domain classification |
| Merge mechanism | None — Socratic dialogue produces one doc | Adversarial debate + scoring + provenance-annotated merge |
| Codebase context | Auggie MCP single shot | Optional `/sc:analyze` invocation OR Auggie quick scan, gated by complexity |
| Research integration | WebSearch mentioned, not wired | Auto-invoke `/sc:research` (light) or `tech-research` skill (deep), gated by topic novelty |
| Handoff | Text suggestion only | Flag-gated invocation of `/sc:design`, `/sc:tasklist`, `/sc:task-builder` |
| Composability | None — terminal command | Structured return contract for downstream commands |

### Pipeline Position

```
topic (user)
   ↓
/sc:brainstorm  ← (this spec)
   ↓
   ├── enrichment: /sc:analyze | /sc:research | tech-research (optional, parallel)
   ↓
   ├── seed-brief.md (Socratic dialogue output)
   ↓
   ├── /sc:adversarial --source seed-brief.md --generate spec --agents <built-spec>
   ↓
   ├── merged-requirements.md  + 6 adversarial artifacts   # spec-shaped per §10
   ↓
   └── --handoff:
        ├── none      → STOP (default)
        ├── design    → recommend /sc:design (text only, user runs it)
        ├── tasklist  → invoke /sc:tasklist with merged-requirements.md
        └── task      → invoke /sc:task-builder with merged-requirements.md + template
```

---

## 2. Required Input

**Mandatory**: A topic string (free-form text in `$ARGUMENTS`).

```bash
/sc:brainstorm "<topic>" [flags...]
```

**Examples**:
- `/sc:brainstorm "add caching to the API layer"` (code-related, short)
- `/sc:brainstorm "AI-powered project management tool"` (greenfield, broad)
- `/sc:brainstorm "@docs/incident-2026-Q1.md what went wrong and how to prevent" --depth deep` (with file reference)

**STOP conditions**:
- Empty topic → emit error: `"Brainstorm requires a topic. Usage: /sc:brainstorm \"<topic>\""`
- Topic > 2000 chars → WARN, suggest summarizing or providing a file reference

---

## 3. Flags & Options

| Flag | Short | Required | Default | Description |
|------|-------|----------|---------|-------------|
| `<topic>` | | Yes | - | Brainstorm topic (free text or `@file` reference) |
| `--proposals` | `-p` | No | `3` | Number of parallel proposal variants to generate (2-7). Maps to `/sc:adversarial --agents` count. |
| `--depth` | `-d` | No | `standard` | Dialogue + debate depth: `quick`, `standard`, `deep`. Pass-through to `/sc:adversarial --depth`. |
| `--strategy` | `-s` | No | `auto` | Topic strategy: `systematic`, `agile`, `enterprise`, `auto` (heuristic-detected). |
| `--codebase` | | No | auto | Force codebase context enrichment (`/sc:analyze` invocation). |
| `--no-codebase` | | No | `false` | Skip codebase context enrichment even if topic is code-related. |
| `--research` | | No | auto | Force research enrichment. Values: `light` (→ `/sc:research --depth quick`), `deep` (→ `tech-research` skill), `none`. |
| `--no-research` | | No | `false` | Skip research enrichment. |
| `--personas` | | No | auto | Comma-separated persona list to use as advocates. Overrides auto-detection. Examples: `architect,security,frontend` (security is auto-excluded by default per §Auto-Exclusion; naming it here is how you opt in). |
| `--models` | | No | `auto` | Comma-separated model alias list to rotate across proposals. Defaults to `opus,sonnet,haiku` (the 3 active aliases). |
| `--blind` | | No | `false` | Pass-through to `/sc:adversarial --blind` (strip model identity before comparison). |
| `--convergence` | | No | `0.75` | Pass-through to `/sc:adversarial --convergence`. Threshold tuned slightly lower than adversarial default (0.80) because brainstorm variants are MORE divergent by design. |
| `--interactive` | `-i` | No | `false` | Pause for user input at Socratic checkpoints + adversarial decision points. |
| `--handoff` | | No | `none` | Post-merge action: `none`, `design`, `tasklist`, `task`. See §7. |
| `--output` | `-o` | No | `.dev/brainstorms/<timestamp>-<slug>/` | Output directory. |
| `--dry-run` | | No | `false` | Execute Waves 0-2 (dialogue + enrichment + agent-spec build), skip Wave 3 (adversarial). Print agent-spec preview. |
| `--resume-from` | | No | - | Resume from a saved seed-brief, skipping Socratic dialogue. |

**Flag interactions**:
- `--strategy enterprise` implies `--depth deep` unless overridden
- `--depth quick` caps `--proposals` at 2 (cost guardrail)
- `--depth deep` allows up to 7 proposals
- `--handoff task` requires the unified merged output to be a structured requirements doc (validated in Wave 4)

---

## 4. Wave Architecture

5 waves: 0 (prereqs) → 1 (dialogue) → 2 (enrichment + agent-spec) → 3 (adversarial delegation) → 4 (handoff).

### Wave 0 — Prerequisites

**Purpose**: Validate inputs, environment, downstream skills.

**Behavioral Instructions**:
1. Parse `$ARGUMENTS` into topic + flags. Reject empty topic.
2. Validate `--proposals` is in `[2, 7]`. Apply depth caps (quick→2, standard→5, deep→7). Silent clamp on excess + INFO log.
3. Validate `--personas` (if provided): non-empty after trim. STOP on empty.
4. Validate `--models` (if provided): non-empty after trim, each alias resolvable to env var or LiteLLM model ID. STOP on unknown.
5. Verify `sc-adversarial-protocol` skill exists at `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`. STOP if not: `"sc:adversarial skill not installed. Required by /sc:brainstorm v2."`
6. **Skill version compatibility check** (Newman P1): Read first 30 lines of `sc-adversarial-protocol/SKILL.md` frontmatter. Validate `version >= 1.0.0` if present. If `version` field absent, assume compatible (legacy mode) + INFO log. If version too low → STOP with `"sc-adversarial version <X> incompatible. Required: >= 1.0.0."`
7. If `--handoff task`: verify `task-builder` skill exists. STOP if not (per §6 — no silent downgrade).
8. If `--handoff tasklist`: verify `sc-tasklist-protocol` skill exists. STOP if not.
9. Create output directory. If exists and non-empty, append `-N` suffix. Cap N at 99 (STOP on N=100); emit WARN at N≥10.
10. Validate model aliases: read available env vars (`ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`). Default model set = `opus, sonnet, haiku` (the 3 active aliases).

**Exit Criteria**: All prereqs validated. Output dir ready. Emit: `"Wave 0 complete: prerequisites validated. Models available: opus, sonnet, haiku. Proposals: N. Depth: D."`

### Wave 1 — Socratic Dialogue (Seed Brief Generation)

**Purpose**: Transform ambiguous topic into a concrete, debatable **seed brief**.

**Refs Loaded**: `refs/socratic-templates.md` (depth-tiered question banks).

**Behavioral Instructions**:
1. Load Socratic template matching `--depth`:
   - `quick`: 3-5 questions, single-pass, ~500 tokens of dialogue
   - `standard`: 6-10 questions, 2 passes (clarify → validate), ~2000 tokens
   - `deep`: 10-20 questions, 3 passes (clarify → validate → adversarial probe), ~5000 tokens
2. Classify topic against the **domain taxonomy** (from `refs/socratic-templates.md`):
   - `code` (file paths, language constructs, framework names, dev verbs)
   - `architecture` (system design, scalability, integration)
   - `product` (features, user stories, market positioning)
   - `process` (workflow, methodology, organizational)
   - `incident` (post-mortem, debugging, root cause)
   - `research` (exploration, comparison, decision support)
3. Dialogue loop:
   - Present questions in batches of 3-5
   - User responds (or skips with `next` / `skip`)
   - If `--interactive` is false, run a single batch and proceed (user can re-run with `--interactive` for richer brief)
4. Synthesize responses into a structured `seed-brief.md` with frontmatter:
   ```yaml
   ---
   topic: "..."
   domain: code|architecture|product|process|incident|research
   strategy: systematic|agile|enterprise
   depth: quick|standard|deep
   constraints: [...]
   open_questions: [...]
   ---
   ```
   Plus sections: Problem Statement, Known Context, Constraints, Success Criteria, Open Questions.
5. If `--resume-from <path>` was provided: skip steps 1-4. Read existing `seed-brief.md` from path. Validate frontmatter. **Staleness check**: re-classify topic against current domain taxonomy. If result differs from saved `domain` field → emit WARN with both values and require `--force-stale` to proceed (STOP otherwise). Proceed to Wave 2.

**Exit Criteria**: `seed-brief.md` written to output dir. Domain classification stored in state. Emit: `"Wave 1 complete: seed brief generated. Domain: D. Strategy: S."`

### Wave 2A — Context Enrichment (partial-OK)

**Purpose**: Parallel enrichment fetches. Failures are degradations, not aborts.

**Refs Loaded**: `refs/handoff-routing.md` §Enrichment (enrichment-source matrix only).

**Behavioral Instructions**:

Spawn enrichment tasks in parallel via `Task` tool, based on domain + flags:

| Condition | Action | Tool | Output |
|-----------|--------|------|--------|
| `domain ∈ {code, architecture, incident}` AND NOT `--no-codebase` | Invoke `/sc:analyze <relevant-paths> --focus quality --depth quick` OR direct `mcp__auggie__codebase-retrieval` for a quick scan | Skill / MCP | `enrichment/codebase-context.md` |
| `--codebase` (forced) | Same as above, regardless of domain | Skill / MCP | Same |
| `--research light` OR (auto-detect: topic mentions framework/library names not in project) | Invoke `/sc:research "<topic-research-query>" --depth quick` | Skill | `enrichment/research-light.md` |
| `--research deep` OR (auto-detect: `--strategy enterprise` + novel topic) | Invoke `tech-research` skill with topic | Skill | `enrichment/research-deep.md` |
| Otherwise | Skip enrichment | - | - |

**Token budget for enrichment**: ~3000 tokens total (sum of all enrichment artifacts). If exceeded, truncate by priority: codebase > research-light > research-deep.

**Append enrichment summary** to `seed-brief.md` under a new `## Enrichment Context` section (~500-800 tokens summary, full artifacts saved separately).

**Quality-tier tracking**: Each enrichment source records its quality_tier in state (per §5 return contract):
- `primary` — first-choice source ran cleanly (Auggie for codebase, Tavily for research)
- `fallback_1` — primary failed, used Serena (codebase) or WebSearch (research)
- `fallback_2` — both primary and fallback_1 failed, used native Glob/Grep
- `skipped` — enrichment was not invoked (by flag or by domain decision)

**Exit Criteria**: Enrichment artifacts present in state (any quality_tier counts as "present"). Wave proceeds even if all enrichment sources failed (degraded mode). Emit: `"Wave 2A complete: enrichment done (sources: X, degraded: Y)."`

### Wave 2B — Agent-Spec Composition (must-succeed)

**Purpose**: Compose the `--agents` spec for adversarial. Errors here abort the run.

**Refs Loaded**: `refs/agent-spec-builder.md` (model rotation + persona mapping algorithm + escaping rules).

**Behavioral Instructions**:

1. **Persona selection** (priority order):
   - If `--personas` flag provided AND non-empty after trim: use literal list (already validated in Wave 0)
   - Else if `--strategy enterprise`: `architect, analyzer, devops, scribe, qa`
   - Else: domain-aware default per `refs/agent-spec-builder.md` §Persona-Matrix (authoritative location — SPEC.md does not duplicate the table)
   - **Apply `§Auto-Exclusion`** (`refs/agent-spec-builder.md`): `auto_excluded_personas = { security }`. Strip any excluded persona NOT named in an explicit `--personas` list, backfilling from the same priority list; emit one INFO per drop. Security is therefore never auto-selected (no domain default, no enterprise override, no pad/cycle) — it is reachable ONLY via explicit `--personas …,security`. This is a runtime backstop independent of the persona tables.
   - Pad/truncate to `--proposals` count
2. **Model rotation**:
   - Read `--models` (default `opus,sonnet,haiku` — the 3 active aliases)
   - Round-robin assign: `(persona_i, model_(i mod len(models)))`
   - For `--depth deep`: prefer `opus` for first 2 personas (analyzer + architect typically), then rotate
3. **Custom instructions** (optional, per-persona):
   - Pull from `refs/agent-spec-builder.md` persona-instruction templates
   - Templates may reference `{domain}` and `{strategy}` placeholders — NEVER reference the raw user topic string (injection risk)
4. **Serialization with sanitization** (mandatory):
   - Wrap each instruction in single-quoted strings
   - Sanitize all interpolated parameters (`{domain}`, `{strategy}`): strip `,`, `:`, `'`, `"`, and control characters before substitution
   - Escape any embedded single-quotes in templates as `\'`
   - Validate the final agent-spec string round-trips through the adversarial parser (per `refs/agent-spec-builder.md` §Validation): split on `,`, then on `:` (max 3 segments per agent, with the 3rd segment respecting single-quote boundaries)
   - If validation fails → STOP with `"Agent-spec serialization produced invalid output. This is a bug — please report. Spec: <serialized>"`
5. **Token-budget pre-flight**:
   - Estimate Wave 3 token cost: `estimate = proposals × depth_multiplier × persona_weight`
     - `depth_multiplier`: quick=8K, standard=15K, deep=35K per proposal
     - `persona_weight`: 1.0 default, 1.3 for architect/analyzer (heavier reasoning)
   - If `estimate > 250000` AND `depth == deep`: auto-downgrade `proposals` to 3 + emit WARN: `"Estimated token cost (X) exceeds deep-mode budget. Auto-downgraded --proposals to 3. Override with --proposals=N to force."`
   - If `estimate > 350000` after downgrade: STOP with `"Token budget exhausted. Reduce --proposals or --depth."`
   - Hard kill: mid-Wave-3 abort if measured cumulative tokens > 1.25 × estimate
6. **Output**: validated agent-spec string suitable for `/sc:adversarial --agents`. Example:
   ```
   opus:architect:'prioritize maintainability and scaffolding',sonnet:refactorer:'focus on technical debt + minimal-risk transformation paths',haiku:devops:'deployment + observability'
   ```

**Dry-run gate**: If `--dry-run`:
- Print composed agent-spec
- Print token-budget estimate
- If `--handoff != none`: print `"Intended handoff: <value> (skipped in dry-run mode)."`
- Skip Wave 3/4. Exit cleanly.

**Exit Criteria**: Validated agent-spec available in state. Token budget pre-flight passed. Emit: `"Wave 2B complete: agent-spec composed (Y agents across Z models, estimated XK tokens)."`

### Wave 3 — Adversarial Delegation

**Purpose**: Hand off to `sc-adversarial-protocol` for parallel proposal generation, debate, merge.

**Refs Loaded**: `refs/handoff-routing.md` (return-contract consumption + error fallbacks).

**Behavioral Instructions**:

1. Build adversarial invocation arguments:
   ```
   --source <output>/seed-brief.md
   --generate spec                   # Reframed as "spec-style requirements" per §10
   --agents <composed-spec>
   --depth <passthrough>
   --convergence <passthrough, default 0.75>
   --output <output>/adversarial/
   [--blind, --interactive as flagged]
   ```
2. **Invoke**: `Skill sc:adversarial-protocol` with above arguments. (Direct skill invocation, not command — per sc:roadmap pattern.)
3. **Consume return contract** (inline from Skill response):
   - Extract: `status`, `merged_output_path`, `convergence_score`, `artifacts_dir`, `unresolved_conflicts`
   - **Empty-response guard**: If response is completely empty or has no parseable structure → **route directly to FAIL** with `"Adversarial returned empty response — invocation likely failed at transport. See sc:adversarial logs."` Do NOT fall back to a synthetic 0.5 score.
   - **Partial-parse guard**: If response is structured (has YAML/JSON shape) but `convergence_score` field is missing or unparseable → use fallback `convergence_score: 0.5` ONLY IF `merged_output_path` is present AND the file exists. Otherwise route to FAIL.
   - **Missing-file guard**: Verify `merged_output_path` exists on disk via Read. If not → FAIL with `"Adversarial merge artifact missing at <path>. Check sc:adversarial logs."` This guard runs BEFORE 3-status routing — no PARTIAL path bypasses it.
4. **3-status routing** (executed only after all guards above pass):
   - `convergence_score >= 0.65` → PASS: copy `merged_output_path` to `<output>/merged-requirements.md`. Proceed to Wave 4.
   - `convergence_score >= 0.50` → PARTIAL: copy with warning frontmatter `adversarial_status: partial`. Proceed to Wave 4 with caution flag. Surface in chat: `"Brainstorm converged partially (convergence: X.XX). Output may have unresolved tensions — review debate-transcript.md."`
   - `convergence_score < 0.50` → FAIL: emit `"Variants too divergent (convergence: X). Brainstorm did not converge. Review adversarial/debate-transcript.md for irreconcilable differences. Try re-running with narrower topic or --depth deep."` Skip Wave 4.
5. **Fallback protocol** (F1-F3 per sc:roadmap pattern):
   - F1: Skill tool error → retry once with `--depth quick`
   - F2: Retry fails → abort Wave 3, emit error with adversarial logs path
   - F3: All variants fail → write `<output>/brainstorm-failed.md` with partial state, exit

**Exit Criteria**: `merged-requirements.md` available in output dir. Adversarial artifacts archived under `<output>/adversarial/`. Emit: `"Wave 3 complete: adversarial merge done (convergence: X.XX, status: PASS|PARTIAL)."`

### Wave 4 — Handoff (Flag-Gated)

**Purpose**: Optional invocation of downstream commands.

**Refs Loaded**: `refs/handoff-routing.md` (handoff selection + validation).

**Behavioral Instructions**:

Based on `--handoff` value:

- **`none`** (default): Print summary. Suggest next steps in text. Exit.
- **`design`**: Print recommendation: `"To design the architecture: /sc:design @<output>/merged-requirements.md"`. Do NOT invoke (design is interactive).
- **`tasklist`**:
  1. Validate `merged-requirements.md` has actionable requirements (≥3 enumerated requirements)
  2. Invoke `Skill sc-tasklist-protocol` with `--source <output>/merged-requirements.md`
  3. Capture tasklist output path, append to return contract
- **`task`**:
  1. Same validation as tasklist
  2. Detect template from domain (code → `feature-template`, incident → `bugfix-template`, etc.)
  3. Invoke `Skill task-builder` with `--source <output>/merged-requirements.md --template <detected>`
  4. Capture task file path(s)

**Exit Criteria**: Handoff complete (or skipped). Return contract finalized. Emit: `"Wave 4 complete: handoff=<value>. Output: <path>."`

---

## 5. Return Contract

The skill returns a versioned, two-block contract. **Stable block** is the inter-skill API surface (downstream commands MAY rely on these fields). **Telemetry block** is for cost analysis and debugging (downstream commands MUST NOT depend on these fields).

### 5.1 Stable Contract (contract_version: 1.0)

| Field | Type | Description |
|-------|------|-------------|
| `contract_version` | string | Currently `"1.0"`. Bump on breaking changes. |
| `status` | string | `success`, `partial`, `failed` |
| `seed_brief_path` | string | Path to `seed-brief.md` |
| `merged_output_path` | string | Path to `merged-requirements.md` (PASS/PARTIAL only) |
| `convergence_score` | float | 0.0-1.0 from adversarial pipeline |
| `adversarial_artifacts_dir` | string | Path to `<output>/adversarial/` |
| `domain` | string | Detected topic domain |
| `proposal_count` | int | Number of variants generated |
| `enrichment_used` | list[{source, quality_tier}] | Each entry: `{source: "codebase"\|"research-light"\|"research-deep", quality_tier: "primary"\|"fallback_1"\|"fallback_2"\|"skipped"}` |
| `handoff_action` | string | `none`, `design`, `tasklist`, `task` |
| `handoff_output_path` | string \| null | Path to handoff artifact (tasklist or task file) |
| `unresolved_conflicts` | list[string] | From adversarial; items needing user decision |

### 5.2 Telemetry Block (non-stable)

| Field | Type | Description |
|-------|------|-------------|
| `wave_durations_ms` | dict | Per-wave timing for cost analysis |
| `token_usage` | dict | Per-wave token usage estimate |
| `agent_spec` | string | The composed agent-spec passed to adversarial (for debugging) |
| `enrichment_artifact_sizes` | dict | Per-source byte counts |

### 5.3 Downstream Consumers (current + planned)

| Consumer | Reads | Failure mode if field missing |
|----------|-------|-------------------------------|
| `/sc:tasklist` (via `--handoff tasklist`) | `merged_output_path`, `domain` | Refuses invocation, returns to brainstorm Wave 4 with error |
| `/sc:task-builder` (via `--handoff task`) | `merged_output_path`, `domain`, `proposal_count` | Same as above |
| `/sc:design` (text recommendation only) | (none — text only) | N/A |
| Future composers | `status`, `merged_output_path`, `convergence_score` | Should treat `status: failed` as no-go signal |

---

## 6. Error Handling Matrix

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| Empty topic | STOP with usage hint | None |
| `sc-adversarial-protocol` missing | STOP with install instruction | None |
| `--handoff task` but `task-builder` missing | STOP with `"task-builder skill missing. Re-run with --handoff tasklist (if sc-tasklist-protocol installed) or --handoff design."` | No auto-downgrade (user explicitly chose handoff type) |
| `--handoff tasklist` but `sc-tasklist-protocol` missing | STOP with similar message | No auto-downgrade |
| Codebase enrichment fails (Auggie down) | WARN, fall back to Serena `get_symbols_overview` (quality_tier=fallback_1) | Native Glob/Grep if Serena also down (quality_tier=fallback_2) |
| Research enrichment fails (Tavily down) | WARN, fall back to WebSearch (quality_tier=fallback_1); if WebSearch also fails, skip enrichment (quality_tier=skipped) | Note in seed-brief that research was unavailable |
| Adversarial returns `convergence < 0.50` | FAIL Wave 3, skip Wave 4, surface debate transcript path | None |
| Adversarial returns empty/unparseable response | **FAIL Wave 3** (no synthetic 0.5 fallback). Surface logs path. | None |
| Adversarial returns structured response with missing convergence_score AND valid merged_output_path | Use fallback `convergence: 0.5`, route to PARTIAL | Continue with explicit warning |
| Adversarial returns `merged_output_path` to non-existent file | FAIL Wave 3 (file guard runs before status routing) | None |
| User interrupts Socratic dialogue mid-batch | Save partial state to `seed-brief-partial.md`, exit cleanly | `--resume-from` to continue |
| `--proposals > 7` | Cap at 7, WARN | Auto-clamp |
| `--proposals` exceeds depth-cap (quick: 2, standard: 5) | Silent clamp to depth-cap + INFO log | User can override with `--depth deep` |
| `--personas ""` (empty after trim) | STOP with `"--personas requires at least one persona or omit the flag for auto-detection."` | None |
| `--models ""` (empty after trim) | STOP with similar message | None |
| `--resume-from` seed-brief domain mismatch | WARN with old/new domain values; require `--force-stale` to proceed | None |
| Topic > 2000 chars | WARN, accept | None |
| Topic contains adversarial-flag-like content (`:`, `,`, raw quotes) | Sanitized during agent-spec serialization (Wave 2B step 4) — NOT a STOP | None |
| Output dir collision | Append `-N` suffix, continue | Increment until free; cap at N=99 with STOP; WARN at N≥10 |
| Mid-Wave-3 token usage > 1.25 × estimate | Hard abort with partial-state preservation | Run `--resume-from <seed-brief>` after fixing |

---

## 7. Handoff Routing Detail

| Handoff | Trigger | Skill invoked | Validation pre-invoke | Output |
|---------|---------|---------------|----------------------|--------|
| `none` | Default | - | - | Text summary in chat |
| `design` | `--handoff design` | (none) | - | Recommendation text only — user runs `/sc:design` |
| `tasklist` | `--handoff tasklist` | `sc-tasklist-protocol` | Requirements doc has ≥3 enumerated requirements | Tasklist artifact |
| `task` | `--handoff task` | `task-builder` | Same + domain has a matching template | Task file(s) |

**Why `design` is text-only**: `/sc:design` is itself a dialogue-heavy command. Auto-invoking it would conflict with the user's intent to review brainstorm output first. The text recommendation pattern preserves user control.

---

## 8. Cost / Time Estimation

Per-wave estimates (rough; will be refined in eval phase):

| Wave | Duration (s) | Tokens | Notes |
|------|--------------|--------|-------|
| 0 | <2 | ~200 | File checks, env validation |
| 1 (quick) | 30-60 | ~2K | 3-5 Socratic questions, single batch |
| 1 (standard) | 90-180 | ~5K | 6-10 questions, 2 passes |
| 1 (deep) | 300-600 | ~12K | 10-20 questions, 3 passes |
| 2 | 30-180 | 3-8K | Depends on enrichment (codebase + research = max) |
| 3 (quick) | 60-180 | 15-30K | N=2 proposals, shallow debate |
| 3 (standard) | 180-600 | 40-80K | N=3-5 proposals, standard debate |
| 3 (deep) | 600-1800 | 100-200K | N=5-7 proposals, deep debate |
| 4 (none) | <2 | ~200 | Text summary |
| 4 (tasklist) | 60-180 | 5-15K | Tasklist generation |
| 4 (task) | 180-600 | 15-40K | Task-builder full workflow |

**Total typical run** (standard depth, 3 proposals, codebase enrichment, no handoff): ~5-10 minutes wall clock, ~50-90K tokens.

**Cost guardrails**:
- `--depth quick` should never exceed 30K tokens total
- `--depth deep` should not exceed 250K tokens total (forces Wave 3 to back off if approaching)

---

## 9. File Layout

```
src/superclaude/
  commands/
    brainstorm.md                          # Thin command stub (~120 lines)
  skills/
    sc-brainstorm-protocol/
      SKILL.md                             # Behavioral protocol (~450 lines)
      refs/
        socratic-templates.md              # Depth-tiered question banks + domain taxonomy
        agent-spec-builder.md              # Persona selection + model rotation algorithm
        handoff-routing.md                 # Return-contract consumption + downstream invocation

.dev/eval-workspaces/sc-brainstorm/        # Eval workspace (this work)
  SPEC.md                                  # This document
  evals/evals.json                         # Eval prompts + assertions
  iterations/
    iteration-1/
      eval-<name>/
        with_skill/outputs/                # v2 outputs
        old_skill/outputs/                 # v1 baseline outputs
        eval_metadata.json
        grading.json
        timing.json
      benchmark.json
      benchmark.md
      review.html                          # generate_review.py --static output

.dev/brainstorms/                          # Runtime output (per-invocation)
  <timestamp>-<slug>/
    seed-brief.md
    merged-requirements.md
    enrichment/
      codebase-context.md
      research-light.md
      research-deep.md
    adversarial/
      diff-analysis.md
      debate-transcript.md
      base-selection.md
      refactor-plan.md
      merge-log.md
      [merged output]
    return-contract.yaml
```

---

## 10. Adversarial Integration: `--generate` Value Decision

**Decision (post-spec-panel review)**: v2 ships using `--generate spec` and reframes its contract as **"spec-style requirements"**. No blocker on adding `--generate requirements` to `/sc:adversarial`.

**Implications**:
- v2's merged output is a spec-shaped document (frontmatter + structured sections), reframed in §1 and §11 as requirements-shaped.
- Eval assertions in §11.2 grade against spec-shape fields (frontmatter `spec_type`, structured sections), not requirements-shape fields.
- Future enhancement: add `--generate requirements` to `/sc:adversarial` and switch v2 to it (tracked in §16 Followups).

**Why this path**: Adding `--generate requirements` is a coordinated change to a separate skill that would block v2. The spec-shape vs requirements-shape gap is semantic, not structural — the same output can serve both purposes.

---

## 11. Eval Plan

### 11.1 Stratified test cases (saved to `evals/evals.json`)

Cases cover 6 domains × 3 strategies × 3 depths × {with/without enrichment} × {none/design/tasklist/task handoff}. Iteration-1 ships with 12 cases; cases 13-15 added in iteration-2 once iter-1 patterns are visible.

| ID | Topic | Domain | Strategy | Depth | Handoff | Special |
|----|-------|--------|----------|-------|---------|---------|
| 1 | "add rate limiting to public API endpoints" | code | systematic | standard | none | Codebase enrichment expected |
| 2 | "post-mortem: deployment broke staging at 3am" | incident | systematic | deep | none | Analyzer/devops personas (security only via explicit --personas) |
| 3 | "AI-powered changelog summarizer feature" | product | agile | standard | none | Light research expected |
| 4 | "migrate test suite from pytest to vitest" | code | systematic | quick | none | 2-proposal cap, quick depth |
| 5 | "redesign error handling across the worker pool" | architecture | enterprise | deep | none | Codebase + research, 5 proposals |
| 6 | "improve onboarding workflow for new contributors" | process | agile | standard | none | No codebase, no research auto |
| 7 | "evaluate Bun vs Node for our backend services" | research | systematic | standard | none | Deep research expected, no codebase |
| 8 | "add caching to the API layer" | code | systematic | standard | tasklist | Validates --handoff tasklist invocation |
| 9 | "implement feature flag system" | code | systematic | standard | task | Validates --handoff task invocation |
| 10 | "Q1 incident: payment webhook delivery failures" | incident | enterprise | deep | none | `--interactive` simulated, deep dialogue |
| 11 | "consolidate three duplicate auth modules" | code | systematic | deep | none | Validates `--blind` mode (model anonymization) |
| 12 | "explore using GraphQL for public API" | architecture | systematic | quick | design | Validates --handoff design (text-only recommendation) |
| 13 | v1-compat: "build dashboard" | (varies) | systematic | deep | none | **Regression**: only v1-era flags, must produce v1-compatible chat surface |
| 14 | v1-compat: "real-time collab features" | (varies) | agile | normal | none | **Regression**: `--depth normal` was v1 spelling (maps to `standard` in v2) |
| 15 | edge: "fix typo in error message" | code | systematic | quick | none | Trivial input — should still produce coherent (if brief) output, not crash |

**Stratification coverage**:
- 6 domains covered: code (1,4,8,9,11,13,15), incident (2,10), product (3), architecture (5,12,14), process (6), research (7)
- 3 strategies: systematic (most), agile (3,6,14), enterprise (5,10)
- 3 depths: quick (4,12,15), standard (1,3,6,7,8,9,11), deep (2,5,10,13)
- 4 handoff variants: none (most), tasklist (8), task (9), design (12)
- 2 v1-compat regression cases: 13, 14
- 1 edge case: 15

**Intentionally NOT tested in iter-1** (deferred to iter-2):
- `--resume-from <path>` flow
- `--dry-run` preview output validation
- Adversarial FAIL routing (convergence < 0.50) — requires manufactured divergent topics
- Token-budget hard-kill mid-Wave-3 — requires synthetic large topic

### 11.2 Quality Score Rubric (5 dimensions × 1-10 scale = 5-50 total) — STRICT MODE v2

**Why v2 strict mode**: iteration-2 produced perfect 25/25 scores across all 3 pilot cases, which is implausible for a second iteration and indicates the v1 5-point rubric was too coarse. Strict mode uses a 10-point scale, explicit ceiling controls, critique-first scoring, penalty arithmetic, and hostile-reviewer framing.

Each `merged-requirements.md` output is scored on the same 5 quality dimensions:

| Dimension | What is being scored |
|-----------|----------------------|
| **Concreteness** | Specific thresholds, examples, test criteria, and absence of vague generalities |
| **Adversarial Diversity** | Distinct proposal perspectives preserved, tensions reconciled, rationale visible |
| **Coverage** | Functional requirements, non-functional requirements, risks, open questions, and domain-specific concerns |
| **Actionability** | Whether a reader can immediately plan and execute next work, with acceptance criteria defining done-ness |
| **Provenance** | Traceability from each key requirement to seed brief, enrichment, proposal, or debate decision |

#### Score bin anchors (10-point scale)

| Score | Bucket | Description | What it looks like |
|-------|--------|-------------|--------------------|
| 1-2 | **FAIL** | Dimension is absent or actively wrong | Vague platitudes only; major contradictions; document does not address the dimension |
| 3-4 | **WEAK** | Attempts the dimension but with significant gaps | Surface-level attempt, but most content still vague or incomplete |
| 5-6 | **ACCEPTABLE** | Journeyman handling with no major flaws | Would survive review, but contains hedging, gaps, or unclear tradeoffs |
| 7-8 | **STRONG** | Exceptional handling beyond average team output | Requirements are measurable, tensions are reconciled, and evidence is easy to inspect |
| 9 | **NEAR-PERFECT** | Teaching example | Reads like a reference-quality spec; a reviewer learns from it |
| 10 | **RESERVED** | Actively advances the field | Introduces a novel framework or insight beyond what a domain expert would normally produce; almost never awarded |

**Quality Score** = sum of 5 dimensions ∈ [5, 50].

#### Strict-mode procedures (mandatory)

1. **Critique-first scoring**: For any dimension score ≥7, the grader MUST list at least 2 specific weaknesses in that dimension before awarding the score. If the grader cannot identify 2 weaknesses, cap that dimension at 6.
2. **Penalty arithmetic**: Each dimension starts from 10 and deductions are applied for observed flaws. The final score is the post-penalty value, floored at 1.
3. **Hostile reviewer persona**: The grader is framed as a skeptical senior engineer trying to find reasons not to ship the document. Before final scores, the grader MUST produce at least 3 specific objections per output.
4. **Bin-anchor justification**: For every dimension score ≥7, the grader MUST cite the relevant bin-anchor language and explain why the evidence justifies crossing from acceptable into strong or better.

#### Penalty table

| Flaw | Deduction |
|------|-----------|
| Each vague generality found, such as "handle gracefully" or "improve performance" | -1 |
| Each requirement lacking a measurable threshold or test criterion | -1 |
| Each unresolved tension that should have converged at the selected depth | -1 |
| Each missing standard section: FRs, NFRs, ACs, Open Questions, Risks | -1 |
| Each frontmatter field promised by the protocol but missing | -2 |
| Each key claim without a source or provenance tag | -1 |
| Each section with fewer enumerated items than the protocol requires | -1 |
| Repetition across sections without added value | -1 |

Penalties apply to the dimension they affect. For example, vague functional requirements deduct from Concreteness, missing risks deduct from Coverage, unresolved debate tensions deduct from Adversarial Diversity, and missing source tags deduct from Provenance.

**Grader**: Spawn a `general-purpose` subagent with `opus` model, given the strict rubric + the output to grade, returns JSON `{scores: {concreteness: N, ...}, total: N, objections: [...], penalties: {...}, evidence: [...]}`. The grader does NOT see whether the output is v1 or v2 (`--blind` style).

**Calibration step (mandatory before trusting deltas)**:
- Pick 2 eval cases (Case 1 and Case 5).
- Have grader subagent score independently using strict-mode procedures.
- Author scores manually using the same rubric.
- Compute Cohen's kappa or simple agreement rate. If agreement < 0.6 → revise rubric anchor points; re-calibrate.
- Only after calibration passes are bulk delta scores trusted.

### 11.3 Quantitative Assertions (per-case, machine-checkable)

For each eval:
- `merged_requirements_has_acceptance_criteria` — output contains ≥3 acceptance criteria (regex/heading-based check)
- `merged_requirements_has_open_questions_section` — output has explicit open-questions section
- `convergence_score_meets_threshold` — score ≥ 0.50 (PARTIAL or PASS)
- `enrichment_artifact_present` — when expected (codebase/research), at least one enrichment artifact exists
- `enrichment_quality_tier_recorded` — return contract `enrichment_used` has quality_tier on each entry
- `agent_spec_uses_multiple_models` — agent-spec rotates across ≥2 model aliases
- `agent_spec_well_formed` — agent-spec passes adversarial parser round-trip
- `handoff_output_present` — when `--handoff` is set, downstream artifact exists at `handoff_output_path`
- `wall_clock_within_budget` — total run time within expected band per depth tier (see §8)
- `token_usage_within_budget` — total tokens within expected band per depth tier
- `no_partial_failures` — no wave aborts mid-execution
- `contract_version_present` — return contract has `contract_version: "1.0"`
- `no_silent_pass_on_empty_adversarial` — if adversarial returned empty, status must be `failed` (not `partial`)

### 11.4 Qualitative Reviewer Protocol

**Reviewers**: 2 reviewers per case (spec author + one non-author colleague when available; if non-author unavailable, single-reviewer with explicit caveat in benchmark.md).

**Scoring sheet** (per reviewer, per case):
- 1-10 strict-mode score on each of the 5 quality dimensions (§11.2)
- Free-text observation for each dimension
- At least 3 hostile-reviewer objections per output
- Penalty ledger showing deductions applied before final score
- Overall thumbs-up / thumbs-down / revise

**Disagreement resolution**:
- If reviewers disagree by >2 points on any single dimension → third reviewer or author re-reads and adjudicates
- Final score = mean of all reviewers
- All scoring sheets archived in `iterations/iteration-N/eval-<id>/qualitative-review.md`

### 11.5 Baseline

v1 baseline = run the OLD `/sc:brainstorm` (current `src/superclaude/commands/brainstorm.md`) on the same topics. Snapshot the old command file to `iterations/skill-snapshot/brainstorm-v1.md` before refactoring.

### 11.6 Cost/time accounting + Decision threshold

Capture per-eval:
- `total_tokens`, `duration_ms` (from Task notification)
- Per-wave breakdown (from skill telemetry block, §5.2)
- Compare v2 vs v1 baseline as `delta_tokens`, `delta_time`, `delta_quality_score` (from §11.2 grader)

**Decision threshold** (operationalized):
- Quality: mean v2 quality score (5-50 scale) − mean v1 quality score ≥ 12.0 points (~27% relative improvement on the 45-point active range 5-50)
- Cost: mean v2 tokens ≤ 5 × mean v1 tokens AND mean v2 wall-clock ≤ 5 × mean v1 wall-clock
- Per-case: no v2 case may score LOWER than its v1 counterpart by more than 4 quality points (regression guard)
- Calibration: §11.2 calibration step must pass before this threshold is evaluated

**Outcome routing**:
- All gates pass → v2 ships
- Quality gate passes, cost gate fails → user decides per use-case; consider `--depth` defaults adjustment
- Quality gate fails → revise skill, re-run evals (return to iteration loop)
- Regression on any case → root-cause before ship

---

## 12. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Adversarial pipeline cost balloons with N=7 deep | High | Token budget exhaustion | Cap proposals by depth; hard token budget per Wave 3; auto-downgrade to N=3 if budget exceeded |
| Socratic dialogue feels interrogative / hostile in interactive mode | Medium | Bad UX, user abandons | User testing in iteration 2; tune templates based on feedback |
| `convergence < 0.50` happens often on open-ended product topics | Medium | Many FAILs | Lower default convergence to 0.65 for `product` domain; surface "agree to disagree" UX as PARTIAL output |
| Model alias rotation produces "GLM agreeing with GLM" pseudo-diversity | Medium | Fake adversarial signal | `--blind` mode in evals; manually verify variant diversity in iteration 1 |
| Auggie/Tavily MCP downtime kills enrichment frequently | Low-Medium | Reduced quality | Graceful fallbacks to Serena/WebSearch; never block on enrichment |
| Refactor breaks downstream commands depending on v1 behavior | Low | Composability break | Audit grep for `/sc:brainstorm` callers before merge; preserve v1 CLI surface |
| Eval framework can't measure "brainstorm quality" objectively | High | False confidence | Combine quantitative (structural) + qualitative (user) + adversarial (LLM grader) — explicit triangulation |

---

## 13. Migration & Compatibility

- v1 command file is overwritten in place (no parallel `brainstorm-v1`). Git history preserves v1.
- All v1 flags (`--strategy`, `--depth`, `--codebase`, `--no-codebase`) are preserved with identical semantics. New flags (`--proposals`, `--research`, `--personas`, `--models`, `--handoff`, `--convergence`, `--blind`, `--dry-run`, `--resume-from`) are additive.
- Behavioral change: v2 produces more artifacts (output dir vs chat-only). Document in command boundaries.
- `sc-brainstorm-protocol` skill is NEW — no v1 equivalent. Adding it does not break anything.

---

## 14. Out of Scope (Explicitly Will NOT)

- v2 will NOT implement adversarial debate / scoring / merge logic — that lives in `sc-adversarial-protocol`.
- v2 will NOT activate ANTHROPIC_DEFAULT_* env var swapping to access commented-out models — out of scope per user decision (use 3 active aliases).
- v2 will NOT auto-invoke `/sc:design` (text recommendation only) — design is dialogue-heavy and should be user-initiated.
- v2 will NOT modify code or implement features — produces requirements only.
- v2 will NOT replace `/sc:research` or `tech-research` — wraps them as enrichment.
- v2 will NOT support cross-session resume beyond `--resume-from <path>` — Serena-managed session persistence is a future enhancement.

---

## 15. Acceptance Criteria

For v2 to merge:
- [ ] Command stub at `src/superclaude/commands/brainstorm.md` (~120 lines) with all flags from §3 and `## Activation` section invoking `sc-brainstorm-protocol` skill
- [ ] Skill at `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` (<500 lines) implementing 5-wave protocol (Waves 0, 1, 2A, 2B, 3, 4) from §4
- [ ] 3 refs (`socratic-templates.md`, `agent-spec-builder.md`, `handoff-routing.md`) with on-demand loading per wave
- [ ] `make sync-dev && make verify-sync` passes
- [ ] All 15 eval cases from §11.1 run successfully on iteration ≥2 (12 in iter-1 + 3 in iter-2)
- [ ] §11.2 calibration step passes (grader/author agreement ≥ 0.6 on 2 calibration cases) BEFORE delta scores are trusted
- [ ] Quantitative gate (§11.6): mean quality delta ≥ 12.0 points (5-50 strict scale) AND mean cost ≤ 5× v1 AND no per-case quality regression > 4 points
- [ ] User sign-off on qualitative review of merged-requirements docs (per §11.4 protocol)
- [ ] No regressions on the 2 v1-compat eval cases (IDs 13, 14)
- [ ] All 13 §11.3 quantitative assertions pass on all cases
- [ ] No silent-success failure modes (validated by `no_silent_pass_on_empty_adversarial` assertion across runs)
- [ ] Agent-spec serialization passes round-trip parser validation on all generated spec strings
- [ ] Documentation updated: COMMANDS.md routing entry, FLAGS.md (if new flags added globally), ORCHESTRATOR.md entry

---

## 16. Followups (Post-Merge)

**Post-spec-panel P2 deferrals** (tracked here, not iteration-1 scope):
1. Add `--generate requirements` to `/sc:adversarial` and switch v2 to it (per §10)
2. Add `sc-brainstorm-protocol` to COMMANDS.md and ORCHESTRATOR.md routing tables
3. Wire `tech-research` invocation pattern into `refs/handoff-routing.md` (parallel `sc:research` integration)
4. Investigate enabling 5-model rotation via LiteLLM model_id pass-through (currently 3 active) — requires confirming endpoints
5. Cross-session Serena persistence for partial seed-briefs (separate enhancement)
6. `--resume-from --force-stale` semantics: should re-running with new flags also re-trigger Wave 2 enrichment? (deferred for iteration-2 if needed)
7. Iteration-2 expansion: add eval cases for `--dry-run`, adversarial FAIL routing, and token-budget hard-kill (currently deferred per §11.1 "intentionally NOT tested")
8. Telemetry block stability promotion: if downstream consumers come to rely on `wave_durations_ms` for legitimate reasons, promote to stable contract in v1.1

## 17. Spec-Panel Review History

This spec was reviewed by a focused /sc:spec-panel critique panel (Fowler, Nygard, Whittaker, Newman, Crispin) in critique mode prior to implementation. The review surfaced 4 CRITICAL findings and 11 MAJOR findings. All CRITICAL and most MAJOR findings were addressed in v2.0 of this spec. Key changes:

- Eliminated silent-success failure mode for empty adversarial response (§4 Wave 3 step 3)
- Decided on `--generate spec` path for adversarial integration (§10) — unblocks v2 ship
- Added 5-dimension strict 1-10 quality rubric with calibration, critique-first scoring, penalty arithmetic, and hostile-reviewer objections (§11.2)
- Added agent-spec serialization sanitization rules (§4 Wave 2B step 4)
- Split Wave 2 into 2A (enrichment, partial-OK) and 2B (agent-spec, must-succeed)
- Token-budget pre-flight + back-off mechanism (§4 Wave 2B step 5)
- Replaced silent handoff downgrade chain with explicit STOP (§6)
- Expanded eval matrix from 5 to 15 cases including v1-regression + edge cases (§11.1)
- Bifurcated return contract into stable (§5.1) and telemetry (§5.2) blocks
- Added `enrichment_used.quality_tier` field for degraded-mode observability
- Added skill version compatibility check in Wave 0
- Added `--resume-from` staleness check in Wave 1
- Output dir collision cap at N=99 with WARN at N≥10
- Explicit handling of `--personas ""` / `--models ""` / `--proposals` vs depth-cap edge cases

Full panel transcript: available on request from spec author.
