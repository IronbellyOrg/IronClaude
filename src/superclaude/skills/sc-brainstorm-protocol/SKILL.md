---
name: sc:brainstorm-protocol
description: "Full behavioral protocol for sc:brainstorm — Socratic dialogue + parallel proposals + adversarial merge"
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
argument-hint: "<topic> [--proposals N] [--depth quick|standard|deep] [--strategy ...] [--handoff ...] [--output dir]"
---

<!-- markdownlint-disable MD013 MD040 -->

# /sc:brainstorm — Orchestrated Multi-Agent Brainstorm Protocol

<!-- Extended metadata (for documentation, not parsed):
category: orchestration
complexity: advanced
mcp-servers: [sequential, serena, auggie-mcp, tavily]
personas: [architect, analyzer, scribe]
version: 2.0.0
spec: .dev/eval-workspaces/sc-brainstorm/SPEC.md
-->

## Triggers

sc:brainstorm-protocol is invoked ONLY by the `sc:brainstorm` command via `Skill sc:brainstorm-protocol` in its `## Activation` section. Never invoked directly by users.

Activation conditions:

- User runs `/sc:brainstorm <topic> [flags...]` in Claude Code
- All flag arguments are passed through from the command

Do NOT invoke this skill directly. Use the `/sc:brainstorm` command.

## 1. Purpose & Identity

Orchestrate parallel brainstorming via:

1. Socratic dialogue → structured seed brief
2. Optional codebase + research enrichment (parallel, partial-OK)
3. Composed agent-spec (3 active models × N personas)
4. Delegation to `sc-adversarial-protocol` for parallel proposal generation + debate + merge
5. Optional handoff to `/sc:design`, `/sc:tasklist`, or `/sc:task-builder`

**Pipeline Position**: `topic → /sc:brainstorm → seed-brief + merged-requirements → (optional handoff) → tasklist or task files`

**Core Capabilities**:

- Depth-tiered Socratic dialogue (quick/standard/deep)
- Auto-detected domain classification driving persona selection
- Parallel enrichment via `/sc:analyze`, `/sc:research`, `tech-research`
- Model rotation across 3 active aliases (opus, sonnet, haiku)
- Versioned return contract (stable + telemetry)
- Token-budget pre-flight with auto-downgrade

**Output Artifacts** (per invocation):

1. `seed-brief.md` — Socratic dialogue synthesis with frontmatter
2. `merged-requirements.md` — Adversarial-merged unified spec
3. `enrichment/codebase-context.md` (if applicable) — Auggie/Serena/Glob output
4. `enrichment/research-light.md` or `research-deep.md` (if applicable)
5. `adversarial/` — 6 standard adversarial artifacts (debate-transcript, diff-analysis, base-selection, refactor-plan, merge-log, merged-output)
6. `return-contract.yaml` — Versioned return contract

## 2. Required Input

**MANDATORY**: A topic string (free text or `@file` reference) in `$ARGUMENTS`.

```
/sc:brainstorm "<topic>"
```

**STOP** on empty topic with: `"Brainstorm requires a topic. Usage: /sc:brainstorm \"<topic>\""`

## 3. Wave Architecture

6 waves total: 0, 1, 2A, 2B, 3, 4. Each has entry criteria, behavioral instructions, exit criteria. Refs are loaded **on-demand per wave** to prevent context bloat.

### Execution Vocabulary

| Verb | Tool | Scope |
|------|------|-------|
| Invoke Skill | `Skill` | Cross-skill invocation (e.g., `Skill sc:adversarial-protocol`) |
| Dispatch Task agent | `Task` | Parallelized sub-agent work (enrichment) |
| Read / Load ref | `Read` | File reads, ref loading, artifact inspection |
| Write artifact | `Write` | Creating new files (seed-brief.md, merged-requirements.md) |
| Validate | `Read` + `Bash` | File existence checks, prerequisite validation |
| Parse | (inline) | In-memory parsing of YAML, flags, agent specs — no tool, pure logic |
| Compose | (inline) | In-memory agent-spec composition — no tool, pure logic |
| Edit | `Edit` | Modifying existing files (seed-brief enrichment append, frontmatter updates) |

### Wave 0 — Prerequisites

**Purpose**: Validate inputs, environment, downstream skills.

**Behavioral Instructions**:

1. Parse `$ARGUMENTS` into topic + flags. Reject empty topic. STOP if empty: `"Brainstorm requires a topic. Usage: /sc:brainstorm \"<topic>\""`
2. Validate `--proposals` in `[2, 7]`. Apply depth caps:
   - `quick` → max 2
   - `standard` → max 5
   - `deep` → max 7
   - Silent clamp on excess + INFO log: `"--proposals clamped to <N> by --depth <depth>"`
3. Validate `--personas` (if provided): non-empty after trim. STOP on empty: `"--personas requires at least one persona or omit the flag for auto-detection."`
4. Validate `--models` (if provided): non-empty after trim. STOP on empty similarly. Default model set: `opus, sonnet, haiku`.
5. Verify `sc-adversarial-protocol` skill exists at `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` (Read tool). STOP if not: `"sc:adversarial skill not installed. Required by /sc:brainstorm v2. Install via: superclaude install"`
6. **Skill version compatibility check**: Read first 30 lines of `sc-adversarial-protocol/SKILL.md`. Look for `version:` field. If present, require `>= 1.0.0`. If absent → assume compatible (legacy mode) + INFO log. If too low → STOP.
7. **Handoff prereq validation** (no silent downgrade):
   - If `--handoff task` AND `task-builder` skill missing → STOP: `"task-builder skill missing. Re-run with --handoff tasklist (if sc-tasklist-protocol installed) or --handoff design (text-only)."`
   - If `--handoff tasklist` AND `sc-tasklist-protocol` missing → STOP similarly
8. Create output directory (default `.dev/brainstorms/<ts>-<slug>/`). If exists and non-empty, append `-N` suffix. Cap N at 99 (STOP on N=100); WARN at N≥10.
9. Validate model aliases: check env vars `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL` are set. If `--models` provided, validate each alias resolves to one of the known aliases.
10. If `--strategy enterprise` and `--depth` not explicitly set → set `--depth deep` + INFO log.

**Exit Criteria**: All prerequisites validated. Output dir ready. Emit: `"Wave 0 complete: prereqs validated. Models: <list>. Proposals: <N>. Depth: <D>. Output: <path>."`

### Wave 1 — Socratic Dialogue (Seed Brief Generation)

**Purpose**: Transform ambiguous topic into a concrete, debatable seed brief.

**Refs Loaded**: Read `refs/socratic-templates.md` (depth-tiered question banks + domain taxonomy).

**Behavioral Instructions**:

1. **Domain classification**: Apply the domain taxonomy from `refs/socratic-templates.md` §Domain-Taxonomy. Classify topic into one of: `code`, `architecture`, `product`, `process`, `incident`, `research`. Cache result in state as `domain`.
2. **Strategy auto-detection** (if `--strategy auto`): Apply heuristics from `refs/socratic-templates.md` §Strategy-Detection. Pick `systematic`, `agile`, or `enterprise`. Cache as `strategy`.
3. **Resume path**: If `--resume-from <path>`:
   - Read existing `seed-brief.md` from path
   - Validate frontmatter has `topic`, `domain`, `strategy`, `depth` fields
   - **Staleness check**: re-classify topic against current domain taxonomy. If result differs from saved `domain` → emit WARN with both values; require `--force-stale` to proceed (STOP otherwise).
   - Skip steps 4-6, proceed to Wave 2A.
4. **Dialogue loop**:
   - Load Socratic template matching `--depth`:
     - `quick`: 3-5 questions, single batch, ~500 tokens
     - `standard`: 6-10 questions, 2 batches (clarify → validate), ~2000 tokens
     - `deep`: 10-20 questions, 3 batches (clarify → validate → adversarial probe), ~5000 tokens
   - Present batch via chat. Wait for user response if `--interactive`; otherwise auto-proceed using best-available context.
   - Apply domain-specific question variations from `refs/socratic-templates.md` §Domain-Questions.
5. **Synthesize seed brief**: Build `seed-brief.md` with:

   ```yaml
   ---
   topic: "<verbatim topic>"
   domain: code|architecture|product|process|incident|research
   strategy: systematic|agile|enterprise
   depth: quick|standard|deep
   proposals_target: <N>
   handoff_target: <value or none>
   created: <ISO-timestamp>
   ---

   # Seed Brief: <topic-slug>

   ## Problem Statement
   <synthesized from dialogue>

   ## Known Context
   <facts established during dialogue>

   ## Constraints
   - <each constraint as bullet>

   ## Success Criteria
   - <each criterion as bullet>

   ## Open Questions
   - <each open question as bullet>
   ```

6. Write to `<output>/seed-brief.md` via Write tool.

**Exit Criteria**: `seed-brief.md` exists. `domain` + `strategy` cached. Emit: `"Wave 1 complete: seed brief generated. Domain: <D>. Strategy: <S>."`

### Wave 2A — Context Enrichment (partial-OK)

**Purpose**: Parallel enrichment fetches. Failures degrade quality but do not abort.

**Refs Loaded**: Read `refs/handoff-routing.md` §Enrichment-Sources (enrichment-source matrix only — do NOT load full handoff routing yet).

**Behavioral Instructions**:

1. **Enrichment routing matrix** (apply in parallel via `Task` agents):

   | Condition | Action | Output |
   |-----------|--------|--------|
   | `domain ∈ {code, architecture, incident}` AND NOT `--no-codebase` | Invoke `/sc:analyze <relevant-paths> --focus quality --depth quick` OR `mcp__auggie__codebase-retrieval` for quick scan | `enrichment/codebase-context.md` |
   | `--codebase` (forced) | Same as above regardless of domain | Same |
   | `--research light` OR (auto: topic mentions framework/library names not in project) | Invoke `Skill sc-research-protocol` with `--depth quick` (or `/sc:research` if standalone) | `enrichment/research-light.md` |
   | `--research deep` OR (auto: `--strategy enterprise` + novel topic) | Invoke `Skill tech-research` with topic | `enrichment/research-deep.md` |
   | Otherwise | Skip enrichment | — |

2. **Quality-tier tracking** (mandatory per enrichment source):
   - `primary` — first-choice source ran cleanly
   - `fallback_1` — primary failed, used Serena (codebase) or WebSearch (research)
   - `fallback_2` — both primary and fallback_1 failed, used native Glob/Grep
   - `skipped` — enrichment not invoked
   - Record as `enrichment_used: [{source, quality_tier}, ...]` in state.

3. **Token budget for enrichment**: ~3000 tokens total cap. Priority order if exceeded: codebase > research-light > research-deep. Truncate by priority.

4. **Append enrichment summary** to `seed-brief.md` via Edit tool under new `## Enrichment Context` section (~500-800 tokens summary, full artifacts saved separately).

**Exit Criteria**: Enrichment artifacts present in state (any quality_tier counts). Wave proceeds even if all sources failed (degraded mode). Emit: `"Wave 2A complete: enrichment done (sources: <X>, degraded: <Y>)."`

### Wave 2B — Agent-Spec Composition (must-succeed)

**Purpose**: Compose the `--agents` spec for adversarial. Errors abort the run.

**Refs Loaded**: Read `refs/agent-spec-builder.md` (persona-matrix + model rotation + escaping rules + validation).

**Behavioral Instructions**:

1. **Persona selection** (priority order, per `refs/agent-spec-builder.md` §Persona-Matrix):
   - If `--personas` flag provided AND non-empty: use literal list (validated in Wave 0)
   - Else if `--strategy enterprise`: `architect, analyzer, devops, scribe, qa`
   - Else: domain-aware default per `refs/agent-spec-builder.md` §Persona-Matrix table
   - **Apply `§Auto-Exclusion`** (`refs/agent-spec-builder.md`): strip any `auto_excluded_personas` member (currently `security`) that is NOT present in an explicit `--personas` list, backfilling from the same priority list; emit one INFO per drop. This forbids a security lens unless the user explicitly names it.
   - Pad/truncate to `--proposals` count

2. **Model rotation**:
   - Read `--models` (default `opus,sonnet,haiku`)
   - Round-robin assign: `(persona_i, model_(i mod len(models)))`
   - For `--depth deep`: prefer `opus` for first 2 personas (typically analyzer + architect), then rotate

3. **Custom instructions** (optional, per-persona):
   - Pull templates from `refs/agent-spec-builder.md` §Instruction-Templates
   - Templates may reference `{domain}` and `{strategy}` placeholders — NEVER reference the raw user topic string (injection risk per spec §4 Wave 2B step 3)

4. **Serialization with sanitization** (mandatory):
   - Wrap each instruction in single-quoted strings
   - Sanitize all interpolated parameters (`{domain}`, `{strategy}`): strip `,`, `:`, `'`, `"`, and control characters before substitution
   - Escape any embedded single-quotes in templates as `\'`
   - Validate the final agent-spec string round-trips through the adversarial parser (per `refs/agent-spec-builder.md` §Validation): split on `,`, then on `:` (max 3 segments per agent, with the 3rd segment respecting single-quote boundaries)
   - If validation fails → STOP with `"Agent-spec serialization produced invalid output. This is a bug — please report. Spec: <serialized>"`

5. **Token-budget pre-flight**:
   - Estimate Wave 3 cost: `estimate = proposals × depth_multiplier × persona_weight`
     - depth_multiplier: quick=8K, standard=15K, deep=35K per proposal
     - persona_weight: 1.0 default, 1.3 for architect/analyzer
   - If `estimate > 250000` AND `depth == deep`: auto-downgrade `proposals` to 3 + emit WARN. Re-validate agent-spec with new count.
   - If `estimate > 350000` post-downgrade: STOP with `"Token budget exhausted. Reduce --proposals or --depth."`
   - Hard kill threshold (Wave 3): abort if cumulative tokens > 1.25 × estimate

6. **Final output**: validated agent-spec string. Example:

   ```
   opus:architect:'prioritize maintainability and scaffolding',sonnet:refactorer:'focus on technical debt + minimal-risk transformation paths',haiku:devops:'deployment + observability'
   ```

**Dry-run gate**: If `--dry-run`:

- Print composed agent-spec
- Print token-budget estimate
- If `--handoff != none`: print `"Intended handoff: <value> (skipped in dry-run mode)."`
- Skip Wave 3 + 4. Exit cleanly with partial return contract (`status: dry-run`).

**Exit Criteria**: Validated agent-spec in state. Token budget pre-flight passed. Emit: `"Wave 2B complete: agent-spec composed (<Y> agents across <Z> models, ~<XK> tokens estimated)."`

### Wave 3 — Adversarial Delegation

**Purpose**: Hand off to `sc-adversarial-protocol` for parallel proposal generation, debate, merge.

**Refs Loaded**: Read `refs/handoff-routing.md` §Adversarial-Invocation (return-contract consumption + error fallbacks).

**Behavioral Instructions**:

1. **Build adversarial invocation arguments**:

   ```
   --source <output>/seed-brief.md
   --generate spec
   --agents <composed-spec-from-Wave-2B>
   --depth <passthrough>
   --convergence <passthrough, default 0.75>
   --output <output>/adversarial/
   [--blind if flagged]
   [--interactive if flagged]
   ```

   (NOTE: `--generate spec` not `--generate requirements` per spec §10 decision; brainstorm reframes spec output as requirements.)

2. **Invoke**: `Skill sc-adversarial-protocol` with above arguments. Direct skill invocation, not command — per sc:roadmap pattern.

3. **Consume return contract** (inline from Skill response):
   - Extract: `status`, `merged_output_path`, `convergence_score`, `artifacts_dir`, `unresolved_conflicts`
   - **Empty-response guard**: If response is empty or has no parseable structure → **FAIL Wave 3** (no synthetic 0.5 fallback). Emit: `"Adversarial returned empty response — invocation likely failed at transport. See sc:adversarial logs."`
   - **Partial-parse guard**: If response is structured but `convergence_score` missing/unparseable → use fallback `convergence: 0.5` ONLY IF `merged_output_path` is present AND file exists on disk. Otherwise FAIL.
   - **Missing-file guard**: Verify `merged_output_path` exists via Read. If not → FAIL: `"Adversarial merge artifact missing at <path>. Check sc:adversarial logs."` This guard runs BEFORE 3-status routing.

4. **3-status routing** (only after all guards pass):
   - `convergence_score >= 0.65` → PASS: copy `merged_output_path` to `<output>/merged-requirements.md`. Proceed to Wave 4.
   - `convergence_score >= 0.50` → PARTIAL: copy with frontmatter `adversarial_status: partial`. Surface: `"Brainstorm converged partially (convergence: X.XX). Output may have unresolved tensions — review debate-transcript.md."` Proceed to Wave 4 with caution flag.
   - `convergence_score < 0.50` → FAIL: emit `"Variants too divergent (convergence: X). Brainstorm did not converge. Review adversarial/debate-transcript.md for irreconcilable differences. Try re-running with narrower topic or --depth deep."` Skip Wave 4.

5. **Fallback protocol** (F1-F3 per sc:roadmap pattern):
   - **F1** — Skill tool error → retry once with `--depth quick` and reduced proposal count. If retry succeeds, route to step 3.
   - **F2** — Retry fails → abort Wave 3. Emit error with adversarial logs path. Set `status: failed`. Skip Wave 4.
   - **F3** — All variants fail mid-generation → write `<output>/brainstorm-failed.md` with partial state for forensic review. Exit.

**Exit Criteria**: `merged-requirements.md` available (PASS/PARTIAL) OR run terminated (FAIL). Adversarial artifacts archived under `<output>/adversarial/`. Emit: `"Wave 3 complete: adversarial merge done (convergence: X.XX, status: <PASS|PARTIAL|FAIL>)."`

### Wave 4 — Handoff (Flag-Gated)

**Purpose**: Optional invocation of downstream commands.

**Refs Loaded**: Read `refs/handoff-routing.md` §Handoff-Routing (handoff selection + validation rules).

**Behavioral Instructions**:

Based on `--handoff` value:

- **`none`** (default): Print summary table of artifacts. Suggest text-only next steps: `"Next: /sc:design @<output>/merged-requirements.md, or /sc:tasklist for sprint planning, or /sc:implement for direct execution."` Exit.

- **`design`**: Print recommendation: `"To design the architecture: /sc:design @<output>/merged-requirements.md"`. Do NOT invoke (design is interactive — user-initiated only). Set `handoff_action: design`, `handoff_output_path: null`.

- **`tasklist`**:
  1. Validate `merged-requirements.md` has ≥3 enumerated requirements (regex check for bullets, numbered items, or headings). If not → STOP: `"--handoff tasklist requires merged-requirements.md to have ≥3 enumerated requirements. Found <N>."`
  2. Invoke `Skill sc-tasklist-protocol` with `--source <output>/merged-requirements.md`
  3. Capture tasklist output path. Append to return contract as `handoff_output_path`.

- **`task`**:
  1. Same validation as tasklist.
  2. Detect template from domain (per `refs/handoff-routing.md` §Domain-Template-Mapping):
     - `code` → `feature-template`
     - `incident` → `bugfix-template`
     - `architecture` → `migration-template`
     - `product` → `feature-template`
     - `process` → `documentation-template`
     - `research` → `decision-record-template`
  3. Invoke `Skill task-builder` with `--source <output>/merged-requirements.md --template <detected>`
  4. Capture task file path(s). Append to return contract.

**Exit Criteria**: Handoff complete (or skipped). Return contract finalized. Emit: `"Wave 4 complete: handoff=<value>. Output: <path>."`

## 4. Return Contract

Versioned two-block contract written to `<output>/return-contract.yaml` AND returned inline as Skill response.

### Stable Contract (contract_version: 1.0)

```yaml
contract_version: "1.0"
status: success | partial | failed | dry-run
seed_brief_path: <path>
merged_output_path: <path> | null  # null on FAIL or dry-run
convergence_score: <float 0.0-1.0> | null
adversarial_artifacts_dir: <path> | null
domain: code | architecture | product | process | incident | research
proposal_count: <int>
enrichment_used:
  - source: codebase | research-light | research-deep
    quality_tier: primary | fallback_1 | fallback_2 | skipped
handoff_action: none | design | tasklist | task
handoff_output_path: <path> | null
unresolved_conflicts: [<list of strings>]
```

### Telemetry Block (non-stable)

```yaml
wave_durations_ms:
  wave_0: <ms>
  wave_1: <ms>
  wave_2a: <ms>
  wave_2b: <ms>
  wave_3: <ms>
  wave_4: <ms>
token_usage:
  wave_0: <est>
  wave_1: <est>
  wave_2a: <est>
  wave_2b: <est>
  wave_3: <measured from Task notification>
  wave_4: <est>
agent_spec: "<the composed agent-spec string>"
enrichment_artifact_sizes:
  codebase-context.md: <bytes>
  research-light.md: <bytes>
```

## 5. Error Handling Matrix

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| Empty topic | STOP with usage hint | None |
| `sc-adversarial-protocol` missing | STOP with install instruction | None |
| `--handoff task/tasklist` skill missing | STOP (no silent downgrade) | User must choose alternate handoff |
| Codebase enrichment fails (Auggie down) | WARN, fall back to Serena `get_symbols_overview` (quality_tier=fallback_1) | Native Glob/Grep (quality_tier=fallback_2) |
| Research enrichment fails (Tavily down) | WARN, fall back to WebSearch (quality_tier=fallback_1) | Skip (quality_tier=skipped) |
| Adversarial returns `convergence < 0.50` | FAIL Wave 3, skip Wave 4 | None |
| Adversarial empty/unparseable response | **FAIL** (no synthetic 0.5 fallback) | None |
| Adversarial structured but missing convergence_score, valid merged_output_path | PARTIAL with fallback 0.5 + warning | Continue |
| Adversarial `merged_output_path` non-existent | FAIL (file guard before status routing) | None |
| User interrupts Socratic dialogue | Save partial to `seed-brief-partial.md`, exit | `--resume-from` to continue |
| `--proposals > 7` | Cap at 7, WARN | Auto-clamp |
| `--proposals` exceeds depth-cap | Silent clamp + INFO | User can use `--depth deep` to lift |
| `--personas ""` or `--models ""` | STOP with clear message | None |
| `--resume-from` domain staleness | WARN, require `--force-stale` | None |
| Topic contains adversarial-flag-like chars (`:`, `,`, quotes) | Sanitized in Wave 2B step 4 — NOT a STOP | None |
| Output dir collision | Append `-N` suffix; cap at 99 with STOP; WARN at N≥10 | None |
| Mid-Wave-3 token usage > 1.25 × estimate | Hard abort with partial-state preservation | `--resume-from` to retry |

## 6. Will Do / Will Not Do

**Will:**

- Orchestrate Socratic dialogue + enrichment + adversarial delegation + handoff
- Compose validated, sanitized agent-spec strings for `/sc:adversarial`
- Rotate across 3 active model aliases (opus, sonnet, haiku)
- Auto-detect domain + strategy from topic when not specified
- Produce versioned, two-block return contract for composability
- FAIL fast on empty/malformed adversarial responses (no silent success)

**Will Not:**

- Re-implement adversarial debate, scoring, or merge logic
- Auto-invoke `/sc:design` (text recommendation only)
- Modify source code or implement features (produces requirements only)
- Silently downgrade missing handoff skills (STOPs and asks user)
- Activate ANTHROPIC_DEFAULT_* env var swapping for commented-out models
- Inject raw user topic strings into agent-spec custom instructions (sanitization gate)

## 7. Spec Reference

Full spec at `.dev/eval-workspaces/sc-brainstorm/SPEC.md` (684 lines, 17 sections) — authoritative for all behavioral decisions. This SKILL.md is the working protocol; the spec is the design rationale + acceptance criteria.
