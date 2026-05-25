<!-- markdownlint-disable MD013 MD040 -->

# Handoff Routing — Enrichment Sources + Adversarial Invocation + Downstream Handoff

## §Enrichment-Sources

Loaded in Wave 2A. Defines the matrix of enrichment options and quality-tier fallbacks.

### Codebase enrichment

**Trigger conditions**:

- `domain ∈ {code, architecture, incident}` AND NOT `--no-codebase`, OR
- `--codebase` (forced) regardless of domain

**Tier 1 (primary)**: `mcp__auggie__codebase-retrieval`

- Two parallel queries (per existing brainstorm v1 pattern):
  - Query 1: `"{topic} - find relevant code, existing implementations, related components, and integration points"`
  - Query 2: `"Project architecture, structure, patterns, and conventions related to {topic_domain_area}"`
- Output budget: ~800-1200 tokens summary per query
- quality_tier: `primary`

**Tier 2 (fallback_1)**: Serena MCP

- `mcp__serena__get_symbols_overview` on relevant directories (depth: 1)
- `mcp__serena__find_symbol` for known entity names in topic
- Output budget: ~500-800 tokens summary
- quality_tier: `fallback_1`
- Activation: if Tier 1 returns error OR empty result

**Tier 3 (fallback_2)**: Native Glob/Grep

- Glob for files matching topic keywords
- Grep for symbol/entity names mentioned in topic
- Output budget: ~300-500 tokens (raw file list + grep hits)
- quality_tier: `fallback_2`
- Activation: if Tier 2 also fails

**Final fallback**: skip enrichment, set quality_tier: `skipped`, log to seed-brief Note section.

### Research enrichment (light)

**Trigger conditions**:

- `--research light`, OR
- Auto-detect: topic mentions framework/library/tool names not present in project (cross-check via Glob)

**Tier 1 (primary)**: `Skill sc:research-protocol` (the protocol behind `/sc:research`)

- Invoke with: `<topic-as-research-query> --depth quick`
- Output: `enrichment/research-light.md` (~1000-2000 tokens)
- quality_tier: `primary`

**Tier 2 (fallback_1)**: Direct WebSearch tool

- Single query: `{topic} best practices`
- Output: condensed search results (~500 tokens)
- quality_tier: `fallback_1`

**Final fallback**: skip; quality_tier: `skipped`.

### Research enrichment (deep)

**Trigger conditions**:

- `--research deep`, OR
- Auto-detect: `--strategy enterprise` AND topic mentions novel external technology

**Tier 1 (primary)**: `Skill tech-research`

- Heavier research workflow with structured output
- Output: `enrichment/research-deep.md` (~3000-5000 tokens)
- quality_tier: `primary`

**Tier 2 (fallback_1)**: `Skill sc:research-protocol` with `--depth deep`

- quality_tier: `fallback_1`

**Final fallback**: degrade to research-light tier 1 (with INFO log); quality_tier inherits.

### Parallel execution

All applicable enrichment sources are invoked in parallel via `Task` agents in the same turn. Per-source timeout: 120s (configurable per source). On timeout: WARN + record quality_tier: `skipped`.

**Token cap (combined)**: 3000 tokens of summary in seed-brief.md. Truncate by priority: codebase > research-light > research-deep.

## §Adversarial-Invocation

Loaded in Wave 3. Defines how brainstorm calls `sc-adversarial-protocol` and consumes the return contract.

### Invocation arguments

Build the following argument string to pass to `Skill sc-adversarial-protocol`:

```
--source <output>/seed-brief.md
--generate spec
--agents <composed-agent-spec>
--depth <passthrough from --depth flag>
--convergence <passthrough from --convergence flag, default 0.75>
--output <output>/adversarial/
```

Optional pass-throughs:

- `--blind` (if brainstorm `--blind` was set)
- `--interactive` (if brainstorm `--interactive` was set)

### Return contract consumption (inline from Skill response)

Expected response fields (from sc-adversarial-protocol):

- `status`: `success` | `partial` | `failed`
- `merged_output_path`: string path
- `convergence_score`: float 0.0-1.0
- `artifacts_dir`: string path
- `unresolved_conflicts`: list[string]

### Guard sequence (apply in order — ALL must pass before status routing)

1. **Empty-response guard**: If response is empty or has no parseable structure → **FAIL** (no synthetic 0.5 fallback). This is a critical change from naive routing: empty ≠ partial success.

2. **Partial-parse guard**: If response is structured (YAML/JSON shape) but `convergence_score` field is missing or unparseable → use fallback `convergence: 0.5` ONLY IF `merged_output_path` is non-null AND the file exists on disk. Otherwise FAIL.

3. **Missing-file guard**: Verify `merged_output_path` exists on disk via Read. If not → FAIL: `"Adversarial merge artifact missing at <path>. Check sc:adversarial logs."`

### 3-status routing (only after all guards pass)

| convergence_score | Status | Action |
|-------------------|--------|--------|
| `≥ 0.65` | PASS | Copy `merged_output_path` → `<output>/merged-requirements.md`. Proceed to Wave 4. |
| `0.50 ≤ x < 0.65` | PARTIAL | Copy with frontmatter `adversarial_status: partial`. Surface warning in chat. Proceed to Wave 4 with caution flag. |
| `< 0.50` | FAIL | Emit divergence message. Skip Wave 4. |

### Fallback protocol (F1-F3)

**F1 — Skill tool error**: Retry once with reduced payload (`--depth quick`, `--proposals` clamped to 3). If retry succeeds, route through normal status pipeline.

**F2 — Retry fails**: Abort Wave 3. Emit error with adversarial logs path. Set `status: failed`. Skip Wave 4. Write `<output>/brainstorm-failed.md` with partial state.

**F3 — All variants fail mid-generation**: Same as F2 outcome but with `failure_stage: generation` field in failure record.

## §Handoff-Routing

Loaded in Wave 4. Defines what happens after merge succeeds based on `--handoff` value.

### `none` (default)

Print artifact summary table:

```
Artifact                            Path
------------------------------------+----------------------------------
seed-brief.md                       <output>/seed-brief.md
merged-requirements.md              <output>/merged-requirements.md
adversarial/                        <output>/adversarial/ (6 artifacts)
enrichment/                         <output>/enrichment/ (if any)
return-contract.yaml                <output>/return-contract.yaml
```

Print text-only next-step suggestions:

- `/sc:design @<output>/merged-requirements.md` — architecture
- `/sc:tasklist @<output>/merged-requirements.md` — sprint planning
- `/sc:implement @<output>/merged-requirements.md` — direct execution

Set `handoff_action: none`, `handoff_output_path: null`. Exit.

### `design`

Print recommendation only (do NOT invoke):

```
Next: /sc:design @<output>/merged-requirements.md

(/sc:design is interactive — it should be user-initiated, not auto-invoked
from brainstorm. The merged requirements are ready as input.)
```

Set `handoff_action: design`, `handoff_output_path: null`. Exit.

### `tasklist`

**Pre-invoke validation**:

- Open `<output>/merged-requirements.md` and count enumerated requirements (regex: bullet-list items in sections like "Functional Requirements", "Acceptance Criteria", or numbered items). If count < 3 → STOP: `"--handoff tasklist requires merged-requirements.md to have ≥3 enumerated requirements. Found <N>. Brainstorm output may be too abstract — re-run with --depth deep or narrower topic."`

**Invoke**: `Skill sc-tasklist-protocol` with arguments:

```
--source <output>/merged-requirements.md
--output <output>/tasklist/
```

**Consume return**: Extract tasklist artifact path. Append to brainstorm return contract as `handoff_output_path`.

Set `handoff_action: tasklist`. Exit.

### `task`

**Pre-invoke validation**: Same as tasklist.

**Template detection** (from `merged-requirements.md` frontmatter `domain` field — falls back to brainstorm state `domain`):

| Domain | Template |
|--------|----------|
| `code` | `feature-template` |
| `incident` | `bugfix-template` |
| `architecture` | `migration-template` |
| `product` | `feature-template` |
| `process` | `documentation-template` |
| `research` | `decision-record-template` |

If detected template is unavailable in task-builder skill → STOP with: `"task-builder does not have template <X> for domain <Y>. Available templates: <list>."`

**Invoke**: `Skill task-builder` with arguments:

```
--source <output>/merged-requirements.md
--template <detected-template>
--output <output>/tasks/
```

**Consume return**: Extract task file path(s). Append to brainstorm return contract as `handoff_output_path` (single file or list).

Set `handoff_action: task`. Exit.

## §Domain-Template-Mapping

Authoritative mapping used by `--handoff task` template detection (also referenced from SKILL.md Wave 4):

| Domain | Template name | Rationale |
|--------|---------------|-----------|
| `code` | `feature-template` | Code work is typically additive feature/refactor |
| `incident` | `bugfix-template` | Incident work needs root-cause + fix + prevention |
| `architecture` | `migration-template` | Arch changes involve migration paths and rollout |
| `product` | `feature-template` | Product features map to feature template |
| `process` | `documentation-template` | Process changes are largely documentation + comms |
| `research` | `decision-record-template` | Research output → ADR format |

**Update protocol**: When new templates are added to `task-builder`, update this table AND `Domain-Template-Mapping` table in SKILL.md Wave 4. Both must stay in sync.
